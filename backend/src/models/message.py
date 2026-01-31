from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class MessageBase(SQLModel):
    conversation_id: str = Field(foreign_key="conversation.id", index=True, nullable=False)
    role: str = Field(nullable=False)  # 'user' or 'assistant'
    content: str = Field(max_length=5000, nullable=False)


class Message(MessageBase, table=True):
    """
    Message model representing a single exchange in a conversation.
    """
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    metadata_json: Optional[str] = Field(default=None)  # JSON string for additional metadata


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: str
    timestamp: datetime
    metadata_json: Optional[str] = None