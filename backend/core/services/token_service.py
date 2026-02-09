"""
Authentication Token Service

This module provides service functions for managing authentication tokens,
including storage, validation, and revocation.
"""

from sqlmodel import Session, select
from models.auth_token import AuthenticationToken
from datetime import datetime, timedelta
import uuid
import hashlib
import logging

logger = logging.getLogger(__name__)


def hash_token(token: str) -> str:
    """
    Hash a token value for secure storage

    Args:
        token: The raw token string

    Returns:
        Hashed token value
    """
    return hashlib.sha256(token.encode()).hexdigest()


def store_token(
    session: Session,
    user_id: uuid.UUID,
    token: str,
    token_type: str,
    expires_at: datetime
) -> AuthenticationToken:
    """
    Store a token in the database

    Args:
        session: Database session
        user_id: ID of the user who owns the token
        token: The raw token string
        token_type: Type of token ('access' or 'refresh')
        expires_at: Expiration timestamp

    Returns:
        Created AuthenticationToken record
    """
    hashed_token = hash_token(token)

    auth_token = AuthenticationToken(
        user_id=user_id,
        token_type=token_type,
        token_value=hashed_token,
        expires_at=expires_at,
        revoked=False
    )

    session.add(auth_token)
    session.commit()
    session.refresh(auth_token)

    logger.info(f"Stored {token_type} token for user {user_id}")
    return auth_token


def is_token_revoked(session: Session, token: str) -> bool:
    """
    Check if a token has been revoked

    Args:
        session: Database session
        token: The raw token string

    Returns:
        True if token is revoked, False otherwise
    """
    hashed_token = hash_token(token)

    statement = select(AuthenticationToken).where(
        AuthenticationToken.token_value == hashed_token,
        AuthenticationToken.revoked == False
    )

    token_record = session.exec(statement).first()

    # If token not found in database, consider it invalid/revoked
    if not token_record:
        return True

    # Check if token is expired
    if token_record.expires_at < datetime.utcnow():
        return True

    return False


def revoke_token(session: Session, token: str) -> bool:
    """
    Revoke a token (mark as revoked in database)

    Args:
        session: Database session
        token: The raw token string

    Returns:
        True if token was revoked, False if not found
    """
    hashed_token = hash_token(token)

    statement = select(AuthenticationToken).where(
        AuthenticationToken.token_value == hashed_token
    )

    token_record = session.exec(statement).first()

    if not token_record:
        logger.warning(f"Attempted to revoke non-existent token")
        return False

    token_record.revoked = True
    session.add(token_record)
    session.commit()

    logger.info(f"Revoked {token_record.token_type} token for user {token_record.user_id}")
    return True


def revoke_all_user_tokens(session: Session, user_id: uuid.UUID) -> int:
    """
    Revoke all tokens for a specific user

    Args:
        session: Database session
        user_id: ID of the user

    Returns:
        Number of tokens revoked
    """
    statement = select(AuthenticationToken).where(
        AuthenticationToken.user_id == user_id,
        AuthenticationToken.revoked == False
    )

    tokens = session.exec(statement).all()

    count = 0
    for token in tokens:
        token.revoked = True
        session.add(token)
        count += 1

    session.commit()

    logger.info(f"Revoked {count} tokens for user {user_id}")
    return count


def cleanup_expired_tokens(session: Session) -> int:
    """
    Remove expired tokens from the database

    Args:
        session: Database session

    Returns:
        Number of tokens deleted
    """
    statement = select(AuthenticationToken).where(
        AuthenticationToken.expires_at < datetime.utcnow()
    )

    expired_tokens = session.exec(statement).all()

    count = 0
    for token in expired_tokens:
        session.delete(token)
        count += 1

    session.commit()

    logger.info(f"Cleaned up {count} expired tokens")
    return count


def get_user_active_tokens(session: Session, user_id: uuid.UUID) -> list[AuthenticationToken]:
    """
    Get all active (non-revoked, non-expired) tokens for a user

    Args:
        session: Database session
        user_id: ID of the user

    Returns:
        List of active AuthenticationToken records
    """
    statement = select(AuthenticationToken).where(
        AuthenticationToken.user_id == user_id,
        AuthenticationToken.revoked == False,
        AuthenticationToken.expires_at > datetime.utcnow()
    )

    return list(session.exec(statement).all())
