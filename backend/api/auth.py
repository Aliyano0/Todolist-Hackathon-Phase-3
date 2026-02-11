"""
Authentication API routes for JWT-based authentication

This module provides registration and login endpoints.
Uses custom JWT authentication with FastAPI.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from database.session import get_session
from models.user import User
from pydantic import BaseModel, EmailStr, Field
from core.security.password import hash_password, verify_password
from core.services.email_service import EmailService
from core.config import get_config
import logging
import re
import secrets

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


# Request/Response schemas
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: str
    email: str
    email_verified: bool
    created_at: str
    updated_at: str


def validate_password_requirements(password: str) -> None:
    """
    Validate password meets all requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")

    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")

    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")

    if errors:
        raise ValueError("; ".join(errors))


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterRequest, session: AsyncSession = Depends(get_session)):
    """
    Register a new user with email and password

    Password requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    try:
        logger.info(f"Registration attempt for email: {user_data.email}")

        # Validate password requirements
        validate_password_requirements(user_data.password)

        # Check if user already exists
        statement = select(User).where(User.email == user_data.email)
        result = await session.execute(statement)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.warning(f"Registration failed: Email already registered - {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        password_hash = hash_password(user_data.password)

        # Generate verification token
        verification_token = secrets.token_urlsafe(32)

        # Create new user
        new_user = User(
            email=user_data.email,
            password_hash=password_hash,
            email_verified=False,
            verification_token=verification_token
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        # Send verification email
        try:
            config = get_config()
            email_service = EmailService()
            verification_url = f"{config.frontend_url}/verify-email?token={verification_token}"

            await email_service.send_verification_email(
                to_email=new_user.email,
                verification_url=verification_url
            )
            logger.info(f"Verification email sent to: {new_user.email}")
        except Exception as e:
            logger.error(f"Failed to send verification email to {new_user.email}: {str(e)}")
            # Don't fail registration if email fails - user can resend later

        logger.info(f"User registered successfully: {user_data.email} (user_id: {new_user.id})")

        return UserResponse(
            id=str(new_user.id),
            email=new_user.email,
            email_verified=new_user.email_verified,
            created_at=new_user.created_at.isoformat(),
            updated_at=new_user.updated_at.isoformat()
        )

    except ValueError as e:
        # Password validation error
        logger.warning(f"Registration failed for {user_data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error for {user_data.email}: {str(e)}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class VerifyEmailRequest(BaseModel):
    token: str


@router.post("/verify-email")
async def verify_email(
    request: VerifyEmailRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Verify user's email address using verification token

    Args:
        request: Contains verification token
        session: Database session

    Returns:
        Success message if verification successful

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        logger.info(f"Email verification attempt with token: {request.token[:10]}...")

        # Find user with this verification token
        statement = select(User).where(User.verification_token == request.token)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"Invalid verification token: {request.token[:10]}...")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )

        # Check if already verified
        if user.email_verified:
            logger.info(f"Email already verified for user: {user.email}")
            return {
                "message": "Email already verified",
                "email": user.email
            }

        # Update user
        user.email_verified = True
        user.verification_token = None  # Clear token after use
        user.updated_at = datetime.utcnow()

        await session.commit()

        logger.info(f"Email verified successfully for user: {user.email}")

        return {
            "message": "Email verified successfully",
            "email": user.email
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification error: {str(e)}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during email verification"
        )


class ResendVerificationRequest(BaseModel):
    email: EmailStr


@router.post("/resend-verification")
async def resend_verification_email(
    request: ResendVerificationRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Resend verification email to user

    Args:
        request: Contains user email
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If user not found or already verified
    """
    try:
        logger.info(f"Resend verification request for email: {request.email}")

        # Find user by email
        statement = select(User).where(User.email == request.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            # Don't reveal if email exists for security
            logger.warning(f"Resend verification failed: User not found - {request.email}")
            return {
                "message": "If the email exists, a verification link has been sent"
            }

        # Check if already verified
        if user.email_verified:
            logger.info(f"Email already verified for user: {request.email}")
            return {
                "message": "Email is already verified"
            }

        # Generate new verification token
        verification_token = secrets.token_urlsafe(32)
        user.verification_token = verification_token
        user.updated_at = datetime.utcnow()

        await session.commit()

        # Send verification email
        try:
            config = get_config()
            email_service = EmailService()
            verification_url = f"{config.frontend_url}/verify-email?token={verification_token}"

            await email_service.send_verification_email(
                to_email=user.email,
                verification_url=verification_url
            )
            logger.info(f"Verification email resent to: {user.email}")
        except Exception as e:
            logger.error(f"Failed to resend verification email to {user.email}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send verification email"
            )

        return {
            "message": "Verification email sent successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resend verification error: {str(e)}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while resending verification email"
        )


@router.post("/login")
async def login_user(login_data: UserLoginRequest, session: AsyncSession = Depends(get_session)):
    """
    Authenticate user and return user information with JWT token

    Accepts email and password in request body, verifies credentials,
    and returns user information with JWT access token.
    """
    try:
        logger.info(f"Login attempt for email: {login_data.email}")

        # Find user by email
        statement = select(User).where(User.email == login_data.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"Login failed: User not found - {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            logger.warning(f"Login failed: Invalid password - {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        logger.info(f"Login successful for email: {login_data.email} (user_id: {user.id})")

        # Create JWT token for the user with email_verified claim
        from core.security.jwt import create_access_token
        token = create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "email_verified": user.email_verified
        })

        return {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "email_verified": user.email_verified
            },
            "access_token": token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {login_data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )


@router.post("/logout")
async def logout_user():
    """
    Logout endpoint for JWT-based authentication

    For stateless JWT, logout is handled client-side by removing the token.
    This endpoint returns success to confirm the logout action.

    Future enhancement: Implement token blacklisting for server-side revocation.
    """
    logger.info("Logout request received")
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user_info(session: AsyncSession = Depends(get_session)):
    """
    Get current authenticated user information

    Requires valid JWT token in Authorization header.
    Returns user profile information.
    """
    from dependencies.auth import get_current_user
    from fastapi import Depends as FastAPIDepends

    # This endpoint requires authentication
    # The actual implementation will be added when we need it
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint not yet implemented"
    )


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


@router.post("/password-reset/request")
async def request_password_reset(
    request_data: PasswordResetRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Request a password reset token

    Sends a password reset email to the user if the email exists.
    Always returns success to prevent email enumeration attacks.
    """
    try:
        logger.info(f"Password reset requested for email: {request_data.email}")

        # Find user by email
        statement = select(User).where(User.email == request_data.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if user:
            # Generate reset token (valid for 1 hour)
            import secrets
            from datetime import datetime, timedelta

            reset_token = secrets.token_urlsafe(32)
            user.reset_token = reset_token
            user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)

            await session.commit()

            logger.info(f"Password reset token generated for user: {user.id}")

            # Send password reset email
            try:
                # Get email service
                from main import get_email_service
                email_service = get_email_service()

                # Get frontend URL from config
                config = get_config()
                frontend_url = config.frontend_url

                # Build reset URL
                reset_url = f"{frontend_url}/reset-password?token={reset_token}"

                # Send email
                email_sent = await email_service.send_password_reset(
                    to_email=request_data.email,
                    reset_url=reset_url
                )

                if email_sent:
                    logger.info(f"Password reset email sent successfully to {request_data.email}")
                else:
                    logger.error(f"Failed to send password reset email to {request_data.email}")

            except RuntimeError as e:
                # Email service not initialized - fall back to console logging
                logger.warning(f"Email service not available: {str(e)}")
                logger.info(f"Password reset token (FALLBACK): {reset_token}")
                print(f"\n{'='*60}")
                print(f"PASSWORD RESET TOKEN (Email Service Unavailable)")
                print(f"Email: {request_data.email}")
                print(f"Token: {reset_token}")
                print(f"Reset URL: {config.frontend_url}/reset-password?token={reset_token}")
                print(f"Expires: {user.reset_token_expires.isoformat()}")
                print(f"{'='*60}\n")

            except Exception as e:
                # Email sending failed - log error but don't expose to user
                logger.error(f"Error sending password reset email: {str(e)}")
                # Fall back to console logging in development
                logger.info(f"Password reset token (EMAIL FAILED): {reset_token}")

        # Always return success to prevent email enumeration
        return {
            "message": "If the email exists, a password reset link has been sent"
        }

    except Exception as e:
        logger.error(f"Password reset request error: {str(e)}")
        # Still return success to prevent information leakage
        return {
            "message": "If the email exists, a password reset link has been sent"
        }


@router.post("/password-reset/confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    session: AsyncSession = Depends(get_session)
):
    """
    Reset password using a valid reset token

    Validates the token and updates the user's password.
    """
    try:
        logger.info("Password reset confirmation attempt")

        # Validate new password requirements
        validate_password_requirements(reset_data.new_password)

        # Find user with matching reset token
        statement = select(User).where(User.reset_token == reset_data.token)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            logger.warning("Password reset failed: Invalid token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        # Check if token is expired
        from datetime import datetime
        if not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
            logger.warning(f"Password reset failed: Expired token for user {user.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        # Update password
        user.password_hash = hash_password(reset_data.new_password)
        user.reset_token = None
        user.reset_token_expires = None

        await session.commit()

        logger.info(f"Password reset successful for user: {user.id}")

        return {
            "message": "Password has been reset successfully"
        }

    except ValueError as e:
        # Password validation error
        logger.warning(f"Password reset failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset confirmation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during password reset"
        )