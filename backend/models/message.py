"""
Message model for AI chatbot feature

Represents individual messages in a conversation between user and AI agent.
Stores message content, role (user/assistant/tool), and metadata.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Message(SQLModel, table=True):
    """
    Message model for database storage

    Represents a single message in a conversation.
    Can be from user, assistant (AI), or tool execution result.
    """
    __tablename__ = "message"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False, index=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    role: str = Field(max_length=20, nullable=False)  # 'user', 'assistant', 'tool'
    content: str = Field(nullable=False)  # Message text content
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)


class MessageCreate(SQLModel):
    """Model for creating a new Message"""
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    role: str = Field(max_length=20)
    content: str


class MessageRead(SQLModel):
    """Model for reading Message data"""
    id: uuid.UUID
    conversation_id: uuid.UUID
    user_id: uuid.UUID
    role: str
    content: str
    created_at: datetime


class MessageUpdate(SQLModel):
    """Model for updating Message data"""
    content: Optional[str] = None
