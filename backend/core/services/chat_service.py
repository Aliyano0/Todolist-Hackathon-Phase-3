"""
Chat Service

Handles conversation and message persistence for the AI chatbot.
Provides conversation history loading and message storage with user isolation.
"""

from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from models.conversation import Conversation
from models.message import Message
from database.session import get_async_session
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing chat conversations and messages"""

    @staticmethod
    async def create_conversation(user_id: uuid.UUID) -> Conversation:
        """
        Create a new conversation for a user

        Args:
            user_id: UUID of the user

        Returns:
            Created Conversation object

        Raises:
            Exception: If conversation creation fails
        """
        try:
            async with get_async_session() as session:
                conversation = Conversation(
                    user_id=user_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(conversation)
                await session.commit()
                await session.refresh(conversation)

                logger.info(f"Created conversation {conversation.id} for user {user_id}")
                return conversation

        except Exception as e:
            logger.error(f"Error creating conversation for user {user_id}: {str(e)}")
            raise Exception(f"Failed to create conversation: {str(e)}")

    @staticmethod
    async def get_conversation(
        conversation_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Optional[Conversation]:
        """
        Get a conversation by ID with user isolation

        Args:
            conversation_id: UUID of the conversation
            user_id: UUID of the user (for isolation)

        Returns:
            Conversation object or None if not found

        Raises:
            Exception: If query fails
        """
        try:
            async with get_async_session() as session:
                statement = select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
                result = await session.execute(statement)
                conversation = result.scalar_one_or_none()

                if conversation:
                    logger.info(f"Retrieved conversation {conversation_id} for user {user_id}")
                else:
                    logger.warning(f"Conversation {conversation_id} not found for user {user_id}")

                return conversation

        except Exception as e:
            logger.error(f"Error retrieving conversation {conversation_id}: {str(e)}")
            raise Exception(f"Failed to retrieve conversation: {str(e)}")

    @staticmethod
    async def list_conversations(
        user_id: uuid.UUID,
        limit: int = 50
    ) -> List[Conversation]:
        """
        List conversations for a user, ordered by most recent first

        Args:
            user_id: UUID of the user
            limit: Maximum number of conversations to return (default: 50)

        Returns:
            List of Conversation objects

        Raises:
            Exception: If query fails
        """
        try:
            async with get_async_session() as session:
                statement = (
                    select(Conversation)
                    .where(Conversation.user_id == user_id)
                    .order_by(desc(Conversation.updated_at))
                    .limit(limit)
                )
                result = await session.execute(statement)
                conversations = result.scalars().all()

                logger.info(f"Listed {len(conversations)} conversations for user {user_id}")
                return list(conversations)

        except Exception as e:
            logger.error(f"Error listing conversations for user {user_id}: {str(e)}")
            raise Exception(f"Failed to list conversations: {str(e)}")

    @staticmethod
    async def save_message(
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        role: str,
        content: str
    ) -> Message:
        """
        Save a message to a conversation

        Args:
            conversation_id: UUID of the conversation
            user_id: UUID of the user
            role: Message role ('user', 'assistant', 'tool')
            content: Message content

        Returns:
            Created Message object

        Raises:
            ValueError: If role is invalid
            Exception: If message creation fails
        """
        try:
            # Validate role
            valid_roles = ['user', 'assistant', 'tool']
            if role not in valid_roles:
                raise ValueError(f"Invalid role: {role}. Must be one of {valid_roles}")

            async with get_async_session() as session:
                # Create message
                message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role=role,
                    content=content,
                    created_at=datetime.utcnow()
                )
                session.add(message)

                # Update conversation's updated_at timestamp
                conversation_statement = select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
                conversation_result = await session.execute(conversation_statement)
                conversation = conversation_result.scalar_one_or_none()

                if conversation:
                    conversation.updated_at = datetime.utcnow()

                await session.commit()
                await session.refresh(message)

                logger.info(f"Saved {role} message to conversation {conversation_id}")
                return message

        except ValueError as e:
            logger.warning(f"Validation error in save_message: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error saving message to conversation {conversation_id}: {str(e)}")
            raise Exception(f"Failed to save message: {str(e)}")

    @staticmethod
    async def load_conversation_history(
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Load conversation history (last N messages) for agent context

        Args:
            conversation_id: UUID of the conversation
            user_id: UUID of the user (for isolation)
            limit: Maximum number of messages to load (default: 20)

        Returns:
            List of message dictionaries with role and content

        Raises:
            Exception: If query fails
        """
        try:
            async with get_async_session() as session:
                # Verify conversation belongs to user
                conversation_statement = select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
                conversation_result = await session.execute(conversation_statement)
                conversation = conversation_result.scalar_one_or_none()

                if not conversation:
                    logger.warning(f"Conversation {conversation_id} not found for user {user_id}")
                    raise Exception("Conversation not found or access denied")

                # Load last N messages
                statement = (
                    select(Message)
                    .where(Message.conversation_id == conversation_id)
                    .order_by(desc(Message.created_at))
                    .limit(limit)
                )
                result = await session.execute(statement)
                messages = result.scalars().all()

                # Reverse to get chronological order (oldest first)
                messages = list(reversed(messages))

                # Format for agent context
                formatted_messages = [
                    {
                        "role": msg.role,
                        "content": msg.content
                    }
                    for msg in messages
                ]

                logger.info(f"Loaded {len(formatted_messages)} messages from conversation {conversation_id}")
                return formatted_messages

        except Exception as e:
            logger.error(f"Error loading conversation history {conversation_id}: {str(e)}")
            raise Exception(f"Failed to load conversation history: {str(e)}")

    @staticmethod
    async def get_or_create_conversation(user_id: uuid.UUID) -> Conversation:
        """
        Get the most recent conversation for a user, or create a new one if none exists

        Args:
            user_id: UUID of the user

        Returns:
            Conversation object (existing or newly created)

        Raises:
            Exception: If operation fails
        """
        try:
            # Try to get most recent conversation
            conversations = await ChatService.list_conversations(user_id, limit=1)

            if conversations:
                logger.info(f"Using existing conversation {conversations[0].id} for user {user_id}")
                return conversations[0]

            # Create new conversation if none exists
            logger.info(f"No existing conversations for user {user_id}, creating new one")
            return await ChatService.create_conversation(user_id)

        except Exception as e:
            logger.error(f"Error in get_or_create_conversation for user {user_id}: {str(e)}")
            raise Exception(f"Failed to get or create conversation: {str(e)}")


__all__ = ['ChatService']
