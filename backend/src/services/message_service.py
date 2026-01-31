from sqlmodel import Session, select
from ..models.message import Message, MessageCreate
from typing import Optional, List
from datetime import datetime


class MessageService:
    @staticmethod
    def create_message(session: Session, conversation_id: str, role: str, content: str, metadata_json: Optional[str] = None) -> Message:
        """Create a new message in a conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata_json=metadata_json
        )
        session.add(message)
        try:
            session.commit()
            session.refresh(message)
            return message
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def get_message_by_id(session: Session, message_id: str) -> Optional[Message]:
        """Retrieve a message by its ID."""
        statement = select(Message).where(Message.id == message_id)
        return session.exec(statement).first()

    @staticmethod
    def get_messages_by_conversation(session: Session, conversation_id: str) -> List[Message]:
        """Retrieve all messages for a specific conversation, ordered by timestamp."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
        return session.exec(statement).all()

    @staticmethod
    def get_recent_messages(session: Session, conversation_id: str, limit: int = 10) -> List[Message]:
        """Retrieve recent messages for a specific conversation, ordered by timestamp."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.desc()).limit(limit)
        messages = session.exec(statement).all()
        return list(reversed(messages))  # Return in chronological order