"""
Chat API endpoint for the AI chatbot integration.
Implements stateless architecture with conversation persistence.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from ...config.database import get_session
from ...auth.middleware import jwt_auth, get_current_user_id_from_request
from ...agents.runner import AgentRunner
from pydantic import BaseModel
from fastapi import Request


router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    conversation_id: str
    tool_calls: list
    tool_results: list
    has_tool_calls: bool


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: Request,
    chat_request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Chat endpoint that accepts user messages and returns AI responses.
    Implements stateless architecture by retrieving conversation history from database.
    """
    # Get user ID from authentication
    try:
        user_id = get_current_user_id_from_request(request)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Create agent runner with user context
    agent_runner = AgentRunner(db_session=session, user_id=user_id)

    # Run the conversation
    result = agent_runner.run_conversation(
        user_message=chat_request.message,
        conversation_id=chat_request.conversation_id
    )

    return ChatResponse(
        response=result["response"],
        conversation_id=result["conversation_id"],
        tool_calls=result["tool_calls"],
        tool_results=result["tool_results"],
        has_tool_calls=result["has_tool_calls"]
    )


@router.get("/conversations/{conversation_id}")
async def get_conversation_history(
    request: Request,
    conversation_id: str,
    session: Session = Depends(get_session)
):
    """
    Retrieve conversation history for a specific conversation.
    """
    # Get user ID from authentication
    try:
        user_id = get_current_user_id_from_request(request)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Verify conversation belongs to user (security check)
    from ...services.conversation_service import ConversationService
    conversation_service = ConversationService()
    conversation = conversation_service.get_conversation_by_id(session, conversation_id)

    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # Create agent runner to access message service
    agent_runner = AgentRunner(db_session=session, user_id=user_id)

    # Get conversation history
    history = agent_runner.get_conversation_history(conversation_id)

    return {
        "conversation_id": conversation_id,
        "messages": history
    }


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    request: Request,
    conversation_id: str,
    session: Session = Depends(get_session)
):
    """
    Delete a conversation and all associated messages.
    """
    # Get user ID from authentication
    try:
        user_id = get_current_user_id_from_request(request)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Verify conversation belongs to user (security check)
    from ...services.conversation_service import ConversationService
    conversation_service = ConversationService()
    conversation = conversation_service.get_conversation_by_id(session, conversation_id)

    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # Delete all messages in the conversation first
    from ...services.message_service import MessageService
    message_service = MessageService()
    messages = message_service.get_messages_by_conversation(session, conversation_id)

    for message in messages:
        session.delete(message)

    # Then delete the conversation
    session.delete(conversation)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return {"message": "Conversation deleted successfully"}