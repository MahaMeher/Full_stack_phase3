from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class ConversationBase(SQLModel):
    user_id: str = Field(index=True, nullable=False)


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a logical thread of messages between user and AI assistant.
    """
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime