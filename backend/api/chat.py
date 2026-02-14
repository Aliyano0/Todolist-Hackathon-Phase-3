"""
Chat API Endpoints

Handles chat interactions with the AI agent for task management.
Requires email verification and enforces rate limiting.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
import uuid
import logging

from schemas.chat import ChatRequest, ChatResponse, ChatErrorResponse
from dependencies.auth import get_verified_user
from api.middleware.rate_limit import rate_limit_dependency
from core.services.chat_service import ChatService
from core.services.agent_service import AgentService
from models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])

# Initialize agent service once at module load for performance
agent_service = AgentService()


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    responses={
        401: {"model": ChatErrorResponse, "description": "Unauthorized - Invalid or expired token"},
        403: {"model": ChatErrorResponse, "description": "Forbidden - Email not verified or access denied"},
        429: {"model": ChatErrorResponse, "description": "Too Many Requests - Rate limit exceeded"},
        500: {"model": ChatErrorResponse, "description": "Internal Server Error"}
    }
)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_verified_user)
):
    """
    Send a message to the AI chatbot

    This endpoint allows verified users to interact with the AI agent for task management.

    **Requirements:**
    - Valid JWT token with email_verified=true
    - Rate limit: 10 messages per minute per user

    **Features:**
    - Natural language task creation, listing, completion, deletion, and updates
    - Conversation persistence across sessions
    - Multilingual support (English, Roman Urdu, Urdu)

    **Request Body:**
    - message: User's message (1-2000 characters)
    - conversation_id: Optional UUID of existing conversation

    **Response:**
    - conversation_id: UUID of the conversation
    - message: Agent's response
    - timestamp: ISO 8601 timestamp

    **Error Codes:**
    - 401: Invalid or expired JWT token
    - 403: Email not verified or attempting to access another user's chat
    - 429: Rate limit exceeded (10 messages/minute)
    - 500: Internal server error (OpenRouter API failure, database error, etc.)
    """
    try:
        # Verify path user_id matches authenticated user
        if user_id != str(current_user.id):
            logger.warning(f"User {current_user.id} attempted to access chat for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: cannot access other users' chat"
            )

        # Check rate limit
        await rate_limit_dependency(user_id)

        # Convert user_id to UUID
        user_uuid = current_user.id

        # Get or create conversation
        if request.conversation_id:
            # Load existing conversation
            try:
                conversation_uuid = uuid.UUID(request.conversation_id)
            except (ValueError, AttributeError):
                logger.warning(f"Invalid conversation_id format: {request.conversation_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid conversation_id format"
                )

            conversation = await ChatService.get_conversation(conversation_uuid, user_uuid)
            if not conversation:
                logger.warning(f"Conversation {request.conversation_id} not found for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or access denied"
                )

            # Load conversation history (last 5 messages for optimal performance)
            conversation_history = await ChatService.load_conversation_history(
                conversation_uuid,
                user_uuid,
                limit=5
            )
        else:
            # Create new conversation
            conversation = await ChatService.create_conversation(user_uuid)
            conversation_history = []

        # Save user message
        await ChatService.save_message(
            conversation_id=conversation.id,
            user_id=user_uuid,
            role="user",
            content=request.message
        )

        # Process message with agent (singleton instance initialized at module load)
        try:
            agent_response = await agent_service.process_message(
                user_id=user_id,
                user_message=request.message,
                conversation_history=conversation_history
            )
        except Exception as e:
            logger.error(f"Agent processing error for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service temporarily unavailable. Please try again later."
            )

        # Save assistant response
        await ChatService.save_message(
            conversation_id=conversation.id,
            user_id=user_uuid,
            role="assistant",
            content=agent_response
        )

        logger.info(f"Chat interaction completed for user {user_id} in conversation {conversation.id}")

        # Return response
        return ChatResponse(
            conversation_id=str(conversation.id),
            message=agent_response,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


__all__ = ['router']
