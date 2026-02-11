"""
Conversation model for AI chatbot feature

Represents a chat session between a user and the AI agent.
Enables conversation persistence and resumption across sessions.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Conversation(SQLModel, table=True):
    """
    Conversation model for database storage

    Represents a chat session between a user and the AI agent.
    Groups related messages together and enables conversation resumption.
    """
    __tablename__ = "conversation"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)


class ConversationCreate(SQLModel):
    """Model for creating a new Conversation"""
    user_id: uuid.UUID


class ConversationRead(SQLModel):
    """Model for reading Conversation data"""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ConversationUpdate(SQLModel):
    """Model for updating Conversation data"""
    updated_at: datetime
