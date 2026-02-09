"""
Edge Case Handling for Authentication

This module provides utilities for handling edge cases in authentication flows,
including validation, error handling, and security checks.
"""

from datetime import datetime, timedelta
from typing import Optional
import re
import logging

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Base exception for authentication errors"""
    pass


class TokenExpiredError(AuthenticationError):
    """Raised when a token has expired"""
    pass


class TokenRevokedError(AuthenticationError):
    """Raised when a token has been revoked"""
    pass


class InvalidTokenFormatError(AuthenticationError):
    """Raised when token format is invalid"""
    pass


class RateLimitExceededError(AuthenticationError):
    """Raised when rate limit is exceeded"""
    pass


def validate_email_format(email: str) -> bool:
    """
    Validate email format with comprehensive checks

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    if not email or len(email) > 254:
        return False

    # RFC 5322 compliant email regex (simplified)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        return False

    # Additional checks
    local, domain = email.rsplit('@', 1)

    # Local part should not exceed 64 characters
    if len(local) > 64:
        return False

    # Domain should not exceed 253 characters
    if len(domain) > 253:
        return False

    return True


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength with detailed feedback

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if len(password) > 128:
        return False, "Password must not exceed 128 characters"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    # Check for common weak passwords
    weak_passwords = [
        'password', 'password123', '12345678', 'qwerty123',
        'admin123', 'letmein123', 'welcome123'
    ]

    if password.lower() in weak_passwords:
        return False, "Password is too common, please choose a stronger password"

    return True, None


def is_token_format_valid(token: str) -> bool:
    """
    Validate JWT token format without decoding

    Args:
        token: JWT token string

    Returns:
        True if format is valid, False otherwise
    """
    if not token or not isinstance(token, str):
        return False

    # JWT should have 3 parts separated by dots
    parts = token.split('.')
    if len(parts) != 3:
        return False

    # Each part should be base64url encoded (alphanumeric, -, _)
    for part in parts:
        if not part or not re.match(r'^[A-Za-z0-9_-]+$', part):
            return False

    return True


def calculate_token_expiry_buffer(expires_at: datetime, buffer_minutes: int = 5) -> bool:
    """
    Check if token is within expiry buffer period

    Args:
        expires_at: Token expiration timestamp
        buffer_minutes: Buffer period in minutes before expiration

    Returns:
        True if within buffer period, False otherwise
    """
    buffer_time = datetime.utcnow() + timedelta(minutes=buffer_minutes)
    return expires_at <= buffer_time


def sanitize_error_message(error: Exception, expose_details: bool = False) -> str:
    """
    Sanitize error messages to prevent information leakage

    Args:
        error: Exception to sanitize
        expose_details: Whether to expose detailed error messages (dev mode)

    Returns:
        Sanitized error message
    """
    if expose_details:
        return str(error)

    # Generic messages for production
    error_type = type(error).__name__

    generic_messages = {
        'ValueError': 'Invalid input provided',
        'KeyError': 'Required field missing',
        'TypeError': 'Invalid data type',
        'AttributeError': 'Invalid request format',
        'ConnectionError': 'Service temporarily unavailable',
        'TimeoutError': 'Request timeout, please try again',
    }

    return generic_messages.get(error_type, 'An error occurred, please try again')


def validate_verification_token_age(created_at: datetime, max_age_hours: int = 24) -> bool:
    """
    Validate that verification token is not too old

    Args:
        created_at: Token creation timestamp
        max_age_hours: Maximum age in hours

    Returns:
        True if token is still valid, False if expired
    """
    expiry_time = created_at + timedelta(hours=max_age_hours)
    return datetime.utcnow() <= expiry_time


def validate_reset_token_age(created_at: datetime, max_age_hours: int = 1) -> bool:
    """
    Validate that password reset token is not too old

    Args:
        created_at: Token creation timestamp
        max_age_hours: Maximum age in hours (default 1 hour for security)

    Returns:
        True if token is still valid, False if expired
    """
    expiry_time = created_at + timedelta(hours=max_age_hours)
    return datetime.utcnow() <= expiry_time


def check_concurrent_login_limit(active_sessions: int, max_sessions: int = 5) -> bool:
    """
    Check if user has exceeded concurrent login limit

    Args:
        active_sessions: Number of active sessions
        max_sessions: Maximum allowed concurrent sessions

    Returns:
        True if within limit, False if exceeded
    """
    return active_sessions < max_sessions


def validate_user_id_format(user_id_str: str) -> tuple[bool, Optional[str]]:
    """
    Validate user_id format (UUID)

    Args:
        user_id_str: User ID string to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not user_id_str:
        return False, "User ID is required"

    # UUID format: 8-4-4-4-12 hexadecimal characters
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'

    if not re.match(uuid_pattern, user_id_str.lower()):
        return False, "Invalid user ID format"

    return True, None


def log_authentication_attempt(
    event_type: str,
    email: Optional[str] = None,
    user_id: Optional[str] = None,
    success: bool = True,
    reason: Optional[str] = None
):
    """
    Log authentication attempts for security monitoring

    Args:
        event_type: Type of authentication event (login, register, etc.)
        email: User email (if available)
        user_id: User ID (if available)
        success: Whether the attempt was successful
        reason: Reason for failure (if applicable)
    """
    log_data = {
        'event': event_type,
        'timestamp': datetime.utcnow().isoformat(),
        'success': success
    }

    if email:
        # Mask email for privacy (show first 2 chars and domain)
        parts = email.split('@')
        if len(parts) == 2:
            masked_email = f"{parts[0][:2]}***@{parts[1]}"
            log_data['email'] = masked_email

    if user_id:
        log_data['user_id'] = user_id

    if reason:
        log_data['reason'] = reason

    if success:
        logger.info(f"Auth event: {log_data}")
    else:
        logger.warning(f"Auth failure: {log_data}")
