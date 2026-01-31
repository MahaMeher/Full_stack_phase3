from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from ..utils.exceptions import TaskNotFoundException, UnauthorizedUserException


class TaskService:
    """
    Service layer for handling Task-related operations with proper user isolation.
    """

    @staticmethod
    def create_task(session: Session, user_id: str, task_data: TaskCreate) -> Task:
        """
        Create a new task for the specified user.

        Args:
            session: Database session
            user_id: ID of the user creating the task
            task_data: Task creation data

        Returns:
            Created Task object
        """
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=getattr(task_data, 'completed', False)  # Use getattr to handle both old and new models
        )
        session.add(task)
        try:
            session.commit()
            session.refresh(task)
            return task
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def get_tasks_by_user_id(session: Session, user_id: str) -> List[Task]:
        """
        Get all tasks for the specified user.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve

        Returns:
            List of Task objects belonging to the user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user_id(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a specific task by its ID and user ID.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user requesting the task

        Returns:
            Task object if found and belongs to the user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        return task

    @staticmethod
    def update_task(session: Session, task_id: str, user_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update a task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user requesting the update
            task_data: Task update data

        Returns:
            Updated Task object if successful, None if task doesn't exist or doesn't belong to user

        Raises:
            UnauthorizedUserException: If task doesn't belong to the user
        """
        task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if not task:
            return None

        # Update only the fields that are provided in task_data
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        session.add(task)
        try:
            session.commit()
            session.refresh(task)
            return task
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user requesting the deletion

        Returns:
            True if task was deleted, False if task doesn't exist or doesn't belong to user
        """
        task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if not task:
            return False

        session.delete(task)
        try:
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def toggle_task_completion(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Toggle the completion status of a task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to toggle
            user_id: ID of the user requesting the toggle

        Returns:
            Updated Task object with toggled completion status if successful, None if task doesn't exist or doesn't belong to user
        """
        task = TaskService.get_task_by_id_and_user_id(session, task_id, user_id)
        if not task:
            return None

        task.completed = not task.completed
        session.add(task)
        try:
            session.commit()
            session.refresh(task)
            return task
        except Exception:
            session.rollback()
            raise