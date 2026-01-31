from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a user's todo item with properties and state.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Foreign key reference to user, extracted from JWT
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskRead(TaskBase):
    """
    Schema for reading task data (without internal fields).
    """
    id: uuid.UUID
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    # Inherit all fields from TaskBase
    pass


class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)