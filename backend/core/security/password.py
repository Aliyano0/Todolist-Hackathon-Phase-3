"""
Password hashing and verification utilities using bcrypt

This module provides secure password hashing and verification functions
for user authentication.
"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password as a string

    Example:
        >>> hashed = hash_password("MySecurePass123!")
        >>> isinstance(hashed, str)
        True
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Return as string for database storage
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("MySecurePass123!")
        >>> verify_password("MySecurePass123!", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        # Return False for any errors (invalid hash format, etc.)
        return False
