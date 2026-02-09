"""
JWT token verification utilities for Better Auth integration

This module provides JWT token verification functions for the FastAPI backend.
Better Auth (Next.js frontend) issues tokens, and this module verifies them.

Architecture:
- Authentication Authority: Better Auth (frontend)
- Verification Layer: FastAPI (backend)
- Token Storage: httpOnly cookies (managed by Better Auth)
- Stateless: No token storage in backend database
"""

from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt


# JWT Configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable must be set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Note: In production, Better Auth creates tokens. This function is for testing.

    Args:
        data: Dictionary containing claims to encode in the token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token as string

    Example:
        >>> token = create_access_token({"sub": "user-uuid-here"})
        >>> isinstance(token, str)
        True
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})

    # Encode JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token

    Args:
        token: JWT token string to verify

    Returns:
        Dictionary containing decoded token payload

    Raises:
        JWTError: If token is invalid, expired, or malformed

    Example:
        >>> token = create_access_token({"sub": "user-uuid"})
        >>> payload = verify_token(token)
        >>> "sub" in payload
        True
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise JWTError(f"Token verification failed: {str(e)}")


def extract_user_id(token: str) -> Optional[str]:
    """
    Extract user_id from JWT token

    Args:
        token: JWT token string

    Returns:
        User ID (UUID as string) if valid, None otherwise

    Example:
        >>> token = create_access_token({"sub": "550e8400-e29b-41d4-a716-446655440000"})
        >>> user_id = extract_user_id(token)
        >>> user_id == "550e8400-e29b-41d4-a716-446655440000"
        True
    """
    try:
        payload = verify_token(token)
        user_id: str = payload.get("sub")
        return user_id
    except JWTError:
        return None
