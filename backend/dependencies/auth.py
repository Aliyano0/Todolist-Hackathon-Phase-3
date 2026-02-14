"""
Authentication dependencies for FastAPI with JWT authentication

This module provides JWT token verification for routes.
Custom JWT authentication with FastAPI.

Architecture:
- Stateless: No token storage in database
- Simple verification: Decode JWT and validate user exists
- User isolation: Verify path user_id matches token user_id
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Optional
import uuid
from database.session import get_session
from core.security.jwt import verify_token, extract_user_id
from models.user import User


# Initialize security scheme for Bearer token
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token

    This function:
    1. Extracts JWT token from Authorization header
    2. Verifies token signature and expiration
    3. Extracts user_id from token payload
    4. Verifies user exists in database
    5. Returns User object

    Args:
        credentials: HTTP Bearer token from Authorization header
        session: Async database session

    Returns:
        User object

    Raises:
        HTTPException 401: If token is missing, invalid, expired, or user not found

    Example:
        @router.get("/{user_id}/tasks")
        async def list_tasks(
            user_id: str,
            current_user: User = Depends(get_current_user)
        ):
            if user_id != str(current_user.id):
                raise HTTPException(status_code=403, detail="Access denied")
            # ... rest of endpoint
    """
    # Check if token is provided
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Verify token and extract user_id
    try:
        user_id = extract_user_id(token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify user exists in database
    try:
        user_uuid = uuid.UUID(user_id)
        result = await session.execute(select(User).where(User.id == user_uuid))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def verify_user_access(path_user_id: str, current_user: User = Depends(get_current_user)) -> bool:
    """
    Verify that the authenticated user matches the path user_id

    This enforces data isolation by ensuring users can only access their own resources.

    Args:
        path_user_id: User ID from the URL path parameter
        current_user: Authenticated User object from JWT token

    Returns:
        True if access is allowed

    Raises:
        HTTPException 403: If path user_id doesn't match authenticated user_id

    Example:
        @router.get("/{user_id}/tasks")
        async def list_tasks(
            user_id: str,
            _: bool = Depends(lambda user_id=user_id: verify_user_access(user_id))
        ):
            # user_id is guaranteed to match authenticated user
    """
    if path_user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return True


async def get_verified_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user with email verification check

    This function extends get_current_user() by also checking if the user's email
    is verified. Required for accessing chat and other premium features.

    Args:
        credentials: HTTP Bearer token from Authorization header
        session: Async database session

    Returns:
        User object with verified email

    Raises:
        HTTPException 401: If token is missing, invalid, expired, or user not found
        HTTPException 403: If email is not verified

    Example:
        @router.post("/{user_id}/chat")
        async def chat(
            user_id: str,
            current_user: User = Depends(get_verified_user)
        ):
            # user is guaranteed to have verified email
    """
    # First, get the authenticated user
    user = await get_current_user(credentials, session)

    # Check if email is verified
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required to access this feature"
        )

    return user


def verify_verified_user_access(path_user_id: str, current_user: User = Depends(get_verified_user)) -> bool:
    """
    Verify that the authenticated verified user matches the path user_id

    This combines email verification check with user access verification.
    Required for chat endpoint and other features that need verified users.

    Args:
        path_user_id: User ID from the URL path parameter
        current_user: Authenticated User object with verified email

    Returns:
        True if access is allowed

    Raises:
        HTTPException 401: If token is invalid or expired
        HTTPException 403: If email not verified or user_id doesn't match

    Example:
        @router.post("/{user_id}/chat")
        async def chat(
            user_id: str,
            _: bool = Depends(lambda user_id=user_id: verify_verified_user_access(user_id))
        ):
            # user_id is guaranteed to match authenticated verified user
    """
    if path_user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return True
