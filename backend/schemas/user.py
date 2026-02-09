"""
User authentication schemas for the Todo API

This module defines the Pydantic schemas for user authentication,
including registration, login, and password reset operations.
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


class UserRegisterRequest(BaseModel):
    """Schema for user registration requests"""
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password meets requirements: 8+ chars, 1 uppercase, 1 number, 1 symbol"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')

        return v


class UserLoginRequest(BaseModel):
    """Schema for user login requests"""
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    """Schema for user login responses"""
    access_token: str
    refresh_token: str
    token_type: str
    user_id: str


class UserResponse(BaseModel):
    """Schema for user responses (public information only)"""
    id: str
    email: EmailStr
    email_verified: bool


class UserRegistrationResponse(BaseModel):
    """Schema for user registration responses (includes verification token for testing)"""
    id: str
    email: EmailStr
    email_verified: bool
    verification_token: Optional[str] = None
    message: Optional[str] = None


class TokenRefreshRequest(BaseModel):
    """Schema for token refresh requests"""
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """Schema for token refresh responses"""
    access_token: str
    refresh_token: str
    token_type: str


class EmailVerificationRequest(BaseModel):
    """Schema for email verification requests"""
    token: str


class PasswordResetRequest(BaseModel):
    """Schema for password reset requests (initiation)"""
    email: EmailStr


class PasswordResetConfirmRequest(BaseModel):
    """Schema for password reset confirmation requests"""
    token: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        """Validate password meets requirements: 8+ chars, 1 uppercase, 1 number, 1 symbol"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')

        return v


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str