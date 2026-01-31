from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationCreate
from typing import Optional
from datetime import datetime, timezone
import uuid


class ConversationService:
    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """Create a new conversation for a user."""
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        try:
            session.commit()
            session.refresh(conversation)
            return conversation
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: str) -> Optional[Conversation]:
        """Retrieve a conversation by its ID."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    @staticmethod
    def get_conversations_by_user(session: Session, user_id: str) -> list[Conversation]:
        """Retrieve all conversations for a specific user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def update_conversation_timestamp(session: Session, conversation_id: str) -> Optional[Conversation]:
        """Update the updated_at timestamp for a conversation."""
        conversation = ConversationService.get_conversation_by_id(session, conversation_id)
        if conversation:
            conversation.updated_at = datetime.now(timezone.utc)
            session.add(conversation)
            try:
                session.commit()
                session.refresh(conversation)
            except Exception:
                session.rollback()
                raise
        return conversation