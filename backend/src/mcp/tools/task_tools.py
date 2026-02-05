"""
MCP Tools for task operations in the AI chatbot system.
All tools follow user isolation and validation requirements.
"""

from typing import Dict, Any, List
from pydantic import Field
from ...models.task import Task
from ...mcp.server import ToolCallResult
from .base_tool import UserScopedMCPTool


class AddTaskTool(UserScopedMCPTool):
    """Tool for adding a new task."""

    @property
    def name(self) -> str:
        return "add_task"

    @property
    def description(self) -> str:
        return "Add a new task for the authenticated user"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The title of the task"},
                "description": {"type": "string", "description": "The description of the task", "default": ""}
            },
            "required": ["title"]
        }

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters for adding a task."""
        if "title" not in kwargs or not kwargs["title"]:
            return False
        if len(str(kwargs["title"])) > 200:
            return False
        if "description" in kwargs and kwargs["description"] and len(str(kwargs["description"])) > 1000:
            return False
        return True

    def execute_with_validation(self, **kwargs) -> ToolCallResult:
        """Execute the add task operation with validation."""
        try:
            title = kwargs["title"]
            description = kwargs.get("description", "")

            # Create the task using TaskCreate model
            from ...models.task import TaskCreate
            task_create_obj = TaskCreate(
                title=title,
                description=description,
                completed=False
            )

            task = self.task_service.create_task(self.db_session, self.user_id, task_create_obj)

            return ToolCallResult(
                success=True,
                data={
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                },
                tool_name=self.name
            )
        except Exception as e:
            return ToolCallResult(
                success=False,
                error=f"Failed to add task: {str(e)}",
                tool_name=self.name
            )


class ListTasksTool(UserScopedMCPTool):
    """Tool for listing tasks."""

    @property
    def name(self) -> str:
        return "list_tasks"

    @property
    def description(self) -> str:
        return "List tasks for the authenticated user with optional filtering"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "filter_completed": {
                    "type": "boolean",
                    "description": "Filter tasks by completion status (true for completed, false for pending, null for all)"
                }
            },
            "required": []
        }

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters for listing tasks."""
        if "filter_completed" in kwargs and kwargs["filter_completed"] is not None and not isinstance(kwargs["filter_completed"], bool):
            return False
        return True

    def execute_with_validation(self, **kwargs) -> ToolCallResult:
        """Execute the list tasks operation with validation."""
        try:
            filter_completed = kwargs.get("filter_completed")

            # Get all tasks for the user
            all_tasks = self.task_service.get_tasks_by_user_id(self.db_session, self.user_id)

            # Apply filter if specified
            if filter_completed is not None:
                filtered_tasks = [task for task in all_tasks if task.completed == filter_completed]
            else:
                filtered_tasks = all_tasks

            # Convert to dict format
            tasks_data = []
            for task in filtered_tasks:
                tasks_data.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })

            return ToolCallResult(
                success=True,
                data=tasks_data,
                tool_name=self.name
            )
        except Exception as e:
            return ToolCallResult(
                success=False,
                error=f"Failed to list tasks: {str(e)}",
                tool_name=self.name
            )


class UpdateTaskTool(UserScopedMCPTool):
    """Tool for updating a task."""

    @property
    def name(self) -> str:
        return "update_task"

    @property
    def description(self) -> str:
        return "Update a task for the authenticated user"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The ID of the task to update"},
                "title": {"type": "string", "description": "The new title of the task (optional)"},
                "description": {"type": "string", "description": "The new description of the task (optional)"},
                "completed": {"type": "boolean", "description": "The new completion status (optional)"}
            },
            "required": ["task_id"]
        }

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters for updating a task."""
        if "task_id" not in kwargs or not kwargs["task_id"]:
            return False
        if "title" in kwargs and kwargs["title"] and len(str(kwargs["title"])) > 200:
            return False
        if "description" in kwargs and kwargs["description"] and len(str(kwargs["description"])) > 1000:
            return False
        if "completed" in kwargs and not isinstance(kwargs["completed"], bool):
            return False
        return True

    def execute_with_validation(self, **kwargs) -> ToolCallResult:
        """Execute the update task operation with validation."""
        try:
            task_id = kwargs["task_id"]

            # If the task_id doesn't look like a UUID, try to find it by title
            if not self._is_valid_uuid(task_id):
                # Use the helper method to find the task by title
                matched_task = self._find_task_by_title(task_id)

                if matched_task:
                    task_id = matched_task.id
                else:
                    return ToolCallResult(
                        success=False,
                        error=f"Task with title '{task_id}' not found. Please list your tasks to see available options.",
                        tool_name=self.name
                    )

            # Verify task ownership
            if not self._verify_task_ownership(task_id):
                return ToolCallResult(
                    success=False,
                    error="Task does not belong to the authenticated user",
                    tool_name=self.name
                )

            # Prepare update data using TaskUpdate model
            from ...models.task import TaskUpdate
            update_data = {}
            if "title" in kwargs and kwargs["title"] is not None:
                update_data["title"] = kwargs["title"]
            if "description" in kwargs and kwargs["description"] is not None:
                update_data["description"] = kwargs["description"]
            if "completed" in kwargs and kwargs["completed"] is not None:
                update_data["completed"] = kwargs["completed"]

            # If no updates were provided, return an error
            if not update_data:
                return ToolCallResult(
                    success=False,
                    error="No updates provided. Please specify at least one field to update (title, description, or completed status).",
                    tool_name=self.name
                )

            task_update_obj = TaskUpdate(**update_data)

            # Update the task
            updated_task = self.task_service.update_task(self.db_session, task_id, self.user_id, task_update_obj)

            if not updated_task:
                return ToolCallResult(
                    success=False,
                    error="Task not found",
                    tool_name=self.name
                )

            return ToolCallResult(
                success=True,
                data={
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "completed": updated_task.completed,
                    "created_at": updated_task.created_at.isoformat() if updated_task.created_at else None,
                    "updated_at": updated_task.updated_at.isoformat() if updated_task.updated_at else None,
                    "message": f"Task '{updated_task.title}' has been updated successfully"
                },
                tool_name=self.name
            )
        except Exception as e:
            return ToolCallResult(
                success=False,
                error=f"Failed to update task: {str(e)}",
                tool_name=self.name
            )


class CompleteTaskTool(UserScopedMCPTool):
    """Tool for completing a task."""

    @property
    def name(self) -> str:
        return "complete_task"

    @property
    def description(self) -> str:
        return "Mark a task as completed for the authenticated user"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The ID of the task to complete"}
            },
            "required": ["task_id"]
        }

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters for completing a task."""
        if "task_id" not in kwargs or not kwargs["task_id"]:
            return False
        return True

    def execute_with_validation(self, **kwargs) -> ToolCallResult:
        """Execute the complete task operation with validation."""
        try:
            task_id = kwargs["task_id"]

            # Pre-validate that the task_id looks like a valid identifier
            # If it's a long string with spaces and common sentence structures, it's likely a parsing error
            if isinstance(task_id, str) and len(task_id) > 50:
                # This looks like a sentence rather than a task ID
                # Check for common natural language patterns that indicate parsing errors
                if any(phrase in task_id.lower() for phrase in ['because the task', 'namely', 'is completed', 'as well', 'mark it as']):
                    return ToolCallResult(
                        success=False,
                        error="Invalid task identifier format. The AI may have misunderstood your request. Please specify the task name more directly.",
                        tool_name=self.name
                    )

            # Verify task ownership
            if not self._verify_task_ownership(task_id):
                return ToolCallResult(
                    success=False,
                    error="Task does not belong to the authenticated user",
                    tool_name=self.name
                )

            # Update the task to completed using TaskUpdate model
            from ...models.task import TaskUpdate
            task_update_obj = TaskUpdate(completed=True)

            updated_task = self.task_service.update_task(self.db_session, task_id, self.user_id, task_update_obj)

            if not updated_task:
                return ToolCallResult(
                    success=False,
                    error="Task not found",
                    tool_name=self.name
                )

            return ToolCallResult(
                success=True,
                data={
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "completed": updated_task.completed,
                    "created_at": updated_task.created_at.isoformat() if updated_task.created_at else None,
                    "updated_at": updated_task.updated_at.isoformat() if updated_task.updated_at else None,
                    "message": f"Task '{updated_task.title}' has been marked as completed successfully"
                },
                tool_name=self.name
            )
        except Exception as e:
            return ToolCallResult(
                success=False,
                error=f"Failed to complete task: {str(e)}",
                tool_name=self.name
            )


class DeleteTaskTool(UserScopedMCPTool):
    """Tool for deleting a task."""

    @property
    def name(self) -> str:
        return "delete_task"

    @property
    def description(self) -> str:
        return "Delete a task for the authenticated user"

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "The ID of the task to delete"}
            },
            "required": ["task_id"]
        }

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters for deleting a task."""
        if "task_id" not in kwargs or not kwargs["task_id"]:
            return False
        return True

    def execute_with_validation(self, **kwargs) -> ToolCallResult:
        """Execute the delete task operation with validation."""
        try:
            task_id = kwargs["task_id"]

            # Pre-validate that the task_id looks like a valid identifier
            # If it's a long string with spaces and common sentence structures, it's likely a parsing error
            if isinstance(task_id, str) and len(task_id) > 50:
                # This looks like a sentence rather than a task ID
                # Check for common natural language patterns that indicate parsing errors
                if any(phrase in task_id.lower() for phrase in ['because the task', 'namely', 'is completed', 'as well', 'mark it as']):
                    return ToolCallResult(
                        success=False,
                        error="Invalid task identifier format. The AI may have misunderstood your request. Please specify the task name more directly.",
                        tool_name=self.name
                    )

            # Verify task ownership
            if not self._verify_task_ownership(task_id):
                return ToolCallResult(
                    success=False,
                    error="Task does not belong to the authenticated user",
                    tool_name=self.name
                )

            # Delete the task - pass user_id as well
            success = self.task_service.delete_task(self.db_session, task_id, self.user_id)

            if not success:
                return ToolCallResult(
                    success=False,
                    error="Task not found or does not belong to user",
                    tool_name=self.name
                )

            return ToolCallResult(
                success=True,
                data={"success": True, "message": f"Task with ID {task_id} has been deleted successfully"},
                tool_name=self.name
            )
        except Exception as e:
            return ToolCallResult(
                success=False,
                error=f"Failed to delete task: {str(e)}",
                tool_name=self.name
            )