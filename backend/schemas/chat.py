"""
Chat Schemas

Pydantic schemas for chat request and response handling.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import uuid


class ChatRequest(BaseModel):
    """
    Request schema for chat endpoint

    Attributes:
        message: User's message content (required)
        conversation_id: UUID of existing conversation (optional, creates new if not provided)
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's message content"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="UUID of existing conversation (optional)"
    )

    @validator('message')
    def validate_message(cls, v):
        """Validate message is not empty or whitespace only"""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()

    @validator('conversation_id')
    def validate_conversation_id(cls, v):
        """Validate conversation_id is a valid UUID if provided"""
        if v is not None:
            try:
                uuid.UUID(v)
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid conversation_id format: {v}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Add task: buy groceries",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class ChatResponse(BaseModel):
    """
    Response schema for chat endpoint

    Attributes:
        conversation_id: UUID of the conversation
        message: Agent's response message
        timestamp: ISO 8601 timestamp of the response
    """
    conversation_id: str = Field(
        ...,
        description="UUID of the conversation"
    )
    message: str = Field(
        ...,
        description="Agent's response message"
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 timestamp of the response"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "message": "I've added 'buy groceries' to your tasks!",
                "timestamp": "2024-01-15T10:30:00.000Z"
            }
        }


class ChatErrorResponse(BaseModel):
    """
    Error response schema for chat endpoint

    Attributes:
        error: Error type/code
        message: Human-readable error message
        timestamp: ISO 8601 timestamp of the error
    """
    error: str = Field(
        ...,
        description="Error type or code"
    )
    message: str = Field(
        ...,
        description="Human-readable error message"
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 timestamp of the error"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "error": "email_not_verified",
                "message": "Email verification required to access chat",
                "timestamp": "2024-01-15T10:30:00.000Z"
            }
        }


__all__ = ['ChatRequest', 'ChatResponse', 'ChatErrorResponse']
