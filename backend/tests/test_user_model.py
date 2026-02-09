"""
Unit tests for User model validation

Tests the User model field validation and constraints.
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel
from models.user import User, UserCreate
import uuid
from datetime import datetime


# Create in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestUserModel:
    """Test User model validation and constraints"""

    def test_user_creation_with_valid_data(self, session: Session):
        """Test creating a user with valid data"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_here",
            email_verified=False
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.id is not None
        assert isinstance(user.id, uuid.UUID)
        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password_here"
        assert user.email_verified is False
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_email_unique_constraint(self, session: Session):
        """Test that email must be unique"""
        user1 = User(
            email="test@example.com",
            password_hash="hash1"
        )
        session.add(user1)
        session.commit()

        # Try to create another user with same email
        user2 = User(
            email="test@example.com",
            password_hash="hash2"
        )
        session.add(user2)

        with pytest.raises(Exception):  # Should raise IntegrityError
            session.commit()

    def test_user_email_required(self, session: Session):
        """Test that email is required"""
        user = User(password_hash="hash")
        session.add(user)

        with pytest.raises(Exception):  # Should raise IntegrityError when committing
            session.commit()

    def test_user_password_hash_required(self, session: Session):
        """Test that password_hash is required"""
        user = User(email="test@example.com")
        session.add(user)

        with pytest.raises(Exception):  # Should raise IntegrityError when committing
            session.commit()

    def test_user_default_values(self, session: Session):
        """Test that default values are set correctly"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password"
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.email_verified is False
        assert user.verification_token is None
        assert user.reset_token is None
        assert user.reset_token_expires is None

    def test_user_optional_fields(self, session: Session):
        """Test that optional fields can be set"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            email_verified=True,
            verification_token="token123",
            reset_token="reset456",
            reset_token_expires=datetime.utcnow()
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.email_verified is True
        assert user.verification_token == "token123"
        assert user.reset_token == "reset456"
        assert user.reset_token_expires is not None


class TestUserCreateSchema:
    """Test UserCreate schema validation"""

    def test_user_create_valid_data(self):
        """Test UserCreate with valid data"""
        user_data = UserCreate(
            email="test@example.com",
            password="TestPassword123!",
            email_verification_required=False
        )

        assert user_data.email == "test@example.com"
        assert user_data.password == "TestPassword123!"
        assert user_data.email_verification_required is False

    def test_user_create_password_min_length(self):
        """Test that password must be at least 8 characters"""
        with pytest.raises(Exception):  # Should raise ValidationError
            UserCreate(
                email="test@example.com",
                password="Short1!",  # Only 7 characters
                email_verification_required=False
            )

    def test_user_create_default_email_verification(self):
        """Test default value for email_verification_required"""
        user_data = UserCreate(
            email="test@example.com",
            password="TestPassword123!"
        )

        assert user_data.email_verification_required is True
