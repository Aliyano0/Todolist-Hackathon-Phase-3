"""
Authentication Token Model

This module defines the AuthenticationToken model for tracking JWT tokens
in the database, enabling token revocation and session management.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid


class AuthenticationToken(SQLModel, table=True):
    """
    Authentication Token entity for tracking issued JWT tokens

    Attributes:
        id: Unique identifier for the token record
        user_id: Foreign key to the user who owns this token
        token_type: Type of token (access or refresh)
        token_value: Hashed value of the token for verification
        expires_at: Expiration timestamp for the token
        created_at: Timestamp when the token was created
        revoked: Flag indicating if the token has been revoked
    """
    __tablename__ = "authentication_token"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    token_type: str = Field(max_length=10)  # 'access' or 'refresh'
    token_value: str = Field(max_length=500)  # Hashed token value
    expires_at: datetime = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked: bool = Field(default=False)

    # Relationship to User (optional, for convenience)
    # user: Optional["User"] = Relationship(back_populates="auth_tokens")
