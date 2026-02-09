from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class UserBase(SQLModel):
    """Base model for User with common fields"""
    email: str = Field(unique=True, nullable=False, max_length=255)
    email_verified: bool = Field(default=False)


class User(UserBase, table=True):
    """User model for database storage"""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    verification_token: Optional[str] = Field(default=None)
    reset_token: Optional[str] = Field(default=None)
    reset_token_expires: Optional[datetime] = Field(default=None)


class UserRead(UserBase):
    """Model for reading User data (without sensitive fields)"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    """Model for creating a new User"""
    password: str = Field(min_length=8)
    email_verification_required: bool = Field(default=True)


class UserUpdate(SQLModel):
    """Model for updating User data"""
    email: Optional[str] = Field(default=None, max_length=255)
    email_verified: Optional[bool] = None


class UserLogin(SQLModel):
    """Model for user login credentials"""
    email: str = Field(nullable=False)
    password: str = Field(min_length=1)


class UserPublic(UserBase):
    """Public representation of User (excluding sensitive data)"""
    id: uuid.UUID