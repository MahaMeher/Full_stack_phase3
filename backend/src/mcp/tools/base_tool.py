"""
Base classes for MCP tools that interact with the task system.
All tools must inherit from these base classes to ensure proper validation and user isolation.
"""

from abc import abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
from ...services.task_service import TaskService
from ...services.conversation_service import ConversationService
from ...services.message_service import MessageService
from ...models.task import Task
from ...mcp.server import MCPTool, ToolCallResult


class UserScopedMCPTool(MCPTool):
    """
    Base class for MCP tools that require user isolation.
    All tools that access user-specific data should inherit from this class.
    """

    def __init__(self, db_session, user_id: str):
        """
        Initialize the tool with a database session and user context.

        Args:
            db_session: SQLAlchemy session for database operations
            user_id: The ID of the authenticated user
        """
        self.db_session = db_session
        self.user_id = user_id
        self.task_service = TaskService
        self.conversation_service = ConversationService
        self.message_service = MessageService

    @abstractmethod
    def validate_input(self, **kwargs) -> bool:
        """
        Validate the input parameters for the tool.

        Args:
            **kwargs: Parameters passed to the tool

        Returns:
            bool: True if input is valid, False otherwise
        """
        pass

    @abstractmethod
    def execute_with_validation(self, **kwargs) -> ToolCallResult:
        """
        Execute the tool with user isolation and input validation.

        Args:
            **kwargs: Parameters passed to the tool

        Returns:
            ToolCallResult: Result of the tool execution
        """
        pass

    def execute(self, **kwargs) -> ToolCallResult:
        """
        Execute the tool with validation and user isolation.

        Args:
            **kwargs: Parameters passed to the tool

        Returns:
            ToolCallResult: Result of the tool execution
        """
        # Validate input first
        if not self.validate_input(**kwargs):
            return ToolCallResult(
                success=False,
                error="Invalid input parameters",
                tool_name=self.name
            )

        # Execute with validation and user isolation
        return self.execute_with_validation(**kwargs)

    def _verify_task_ownership(self, task_id: str) -> bool:
        """
        Verify that the given task belongs to the authenticated user.

        Args:
            task_id: ID of the task to verify

        Returns:
            bool: True if the task belongs to the user, False otherwise
        """
        task = self.task_service.get_task_by_id_and_user_id(self.db_session, task_id, self.user_id)
        return task is not None

    def _verify_conversation_ownership(self, conversation_id: str) -> bool:
        """
        Verify that the given conversation belongs to the authenticated user.

        Args:
            conversation_id: ID of the conversation to verify

        Returns:
            bool: True if the conversation belongs to the user, False otherwise
        """
        conversation = self.conversation_service.get_conversation_by_id(self.db_session, conversation_id)
        if not conversation:
            return False
        return conversation.user_id == self.user_id

    def _is_valid_uuid(self, val):
        """Check if a value looks like a UUID."""
        import uuid
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def _find_task_by_title(self, title: str):
        """
        Find a task by its title in the user's task list.

        Args:
            title: The title or partial title of the task to find

        Returns:
            Task object if found, None otherwise
        """
        # Get the user's tasks
        user_tasks = self.task_service.get_tasks_by_user_id(self.db_session, self.user_id)

        if not title:
            return None

        # Clean the search term
        search_term = title.strip().lower()

        # First, try exact match
        for task in user_tasks:
            task_title = task.title
            if task_title and str(task_title).lower().strip() == search_term:
                return task

        # Next, try partial match (search term contained in title)
        for task in user_tasks:
            task_title = task.title
            if task_title and search_term in str(task_title).lower():
                return task

        # Try reverse match (title contained in search term)
        for task in user_tasks:
            task_title = task.title
            if task_title and str(task_title).lower() in search_term:
                return task

        return None