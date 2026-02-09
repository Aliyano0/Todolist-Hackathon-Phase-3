"""
User service layer for the Todo API

This module provides business logic for user-related operations,
including user creation, authentication, and management.
"""

from sqlmodel import Session, select
from models.user import User, UserCreate, UserLogin
from typing import Optional
from passlib.context import CryptContext
import uuid
import secrets
from datetime import datetime, timedelta
from core.security.jwt import create_tokens_for_user
from core.security.edge_cases import (
    validate_email_format,
    validate_password_strength,
    validate_verification_token_age,
    validate_reset_token_age,
    log_authentication_attempt
)
from sqlmodel import update


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a hash for the given password"""
    return pwd_context.hash(password)


def create_user(db_session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password and validation"""
    # Validate email format
    if not validate_email_format(user_create.email):
        log_authentication_attempt('register', email=user_create.email, success=False, reason='Invalid email format')
        raise ValueError("Invalid email format")

    # Validate password strength
    is_valid, error_msg = validate_password_strength(user_create.password)
    if not is_valid:
        log_authentication_attempt('register', email=user_create.email, success=False, reason=error_msg)
        raise ValueError(error_msg)

    # Check if user with this email already exists
    existing_user = db_session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        log_authentication_attempt('register', email=user_create.email, success=False, reason='Email already exists')
        raise ValueError("User with this email already exists")

    # Hash the password
    password_hash = get_password_hash(user_create.password)

    # Generate verification token if email verification is required
    verification_token = None
    if user_create.email_verification_required:
        verification_token = secrets.token_urlsafe(32)

    # Create the user object
    user = User(
        email=user_create.email,
        password_hash=password_hash,
        email_verified=not user_create.email_verification_required,  # If verification required, set to False initially
        verification_token=verification_token
    )

    # Add to database
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    log_authentication_attempt('register', email=user.email, user_id=str(user.id), success=True)
    return user


def authenticate_user(db_session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password with edge case handling"""
    # Validate email format
    if not validate_email_format(email):
        log_authentication_attempt('login', email=email, success=False, reason='Invalid email format')
        return None

    statement = select(User).where(User.email == email)
    user = db_session.exec(statement).first()

    if not user:
        log_authentication_attempt('login', email=email, success=False, reason='User not found')
        return None

    if not verify_password(password, user.password_hash):
        log_authentication_attempt('login', email=email, user_id=str(user.id), success=False, reason='Invalid password')
        return None

    log_authentication_attempt('login', email=email, user_id=str(user.id), success=True)
    return user


def get_user_by_email(db_session: Session, email: str) -> Optional[User]:
    """Get a user by their email address"""
    statement = select(User).where(User.email == email)
    return db_session.exec(statement).first()


def get_user_by_id(db_session: Session, user_id: uuid.UUID) -> Optional[User]:
    """Get a user by their ID"""
    return db_session.get(User, user_id)


def create_user_tokens(db_session: Session, user: User):
    """Create authentication tokens for a user"""
    return create_tokens_for_user(user)


def update_user_email_verification(db_session: Session, user_id: uuid.UUID, verified: bool = True) -> bool:
    """Update the email verification status for a user"""
    user = db_session.get(User, user_id)
    if not user:
        return False

    user.email_verified = verified
    user.verification_token = None  # Clear verification token after verification
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return True


def verify_email_with_token(db_session: Session, token: str) -> Optional[User]:
    """Verify a user's email using the verification token with edge case handling"""
    if not token or len(token) < 10:
        log_authentication_attempt('email_verification', success=False, reason='Invalid token format')
        return None

    # Find user with the verification token
    statement = select(User).where(User.verification_token == token)
    user = db_session.exec(statement).first()

    if not user:
        log_authentication_attempt('email_verification', success=False, reason='Token not found')
        return None

    # Check if email is already verified
    if user.email_verified:
        log_authentication_attempt('email_verification', email=user.email, user_id=str(user.id), success=False, reason='Email already verified')
        return None

    # Validate token age (24 hours expiry)
    if user.created_at and not validate_verification_token_age(user.created_at, max_age_hours=24):
        log_authentication_attempt('email_verification', email=user.email, user_id=str(user.id), success=False, reason='Token expired')
        return None

    # Mark email as verified and clear the token
    user.email_verified = True
    user.verification_token = None
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    log_authentication_attempt('email_verification', email=user.email, user_id=str(user.id), success=True)
    return user


def set_password_reset_token(db_session: Session, user: User, token: str, expires_in_hours: int = 1) -> bool:
    """Set a password reset token for a user with expiration"""
    if not user:
        return False

    user.reset_token = token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=expires_in_hours)

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return True


def reset_user_password(db_session: Session, token: str, new_password: str) -> bool:
    """Reset a user's password using a reset token with edge case handling"""
    # Validate token format
    if not token or len(token) < 10:
        log_authentication_attempt('password_reset', success=False, reason='Invalid token format')
        return False

    # Validate new password strength
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        log_authentication_attempt('password_reset', success=False, reason=error_msg)
        return False

    # Find user with the reset token
    statement = select(User).where(
        User.reset_token == token,
        User.reset_token_expires >= datetime.utcnow()
    )
    user = db_session.exec(statement).first()

    if not user:
        log_authentication_attempt('password_reset', success=False, reason='Invalid or expired token')
        return False

    # Additional validation: check token age with stricter validation
    if user.reset_token_expires and not validate_reset_token_age(user.reset_token_expires - timedelta(hours=1), max_age_hours=1):
        log_authentication_attempt('password_reset', email=user.email, user_id=str(user.id), success=False, reason='Token expired')
        return False

    # Hash the new password
    user.password_hash = get_password_hash(new_password)

    # Clear the reset token
    user.reset_token = None
    user.reset_token_expires = None

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    log_authentication_attempt('password_reset', email=user.email, user_id=str(user.id), success=True)
    return True
    user = db_session.exec(statement).first()

    if not user:
        return False

    # Hash the new password
    password_hash = get_password_hash(new_password)

    # Update the user's password and clear the reset token
    user.password_hash = password_hash
    user.reset_token = None
    user.reset_token_expires = None

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return True