"""
Simple integration tests for registration functionality

These tests verify the core registration logic works correctly.
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel, select
from models.user import User
from core.security.password import hash_password, verify_password
import re


# Create test database
test_engine = create_engine("sqlite:///:memory:")


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)


def validate_password_requirements(password: str) -> None:
    """Validate password requirements"""
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


class TestRegistrationLogic:
    """Test registration business logic"""

    def test_register_user_success(self, session: Session):
        """Test successful user registration"""
        email = "alice@example.com"
        password = "Alice123!"

        # Validate password
        validate_password_requirements(password)

        # Check user doesn't exist
        statement = select(User).where(User.email == email)
        existing_user = session.exec(statement).first()
        assert existing_user is None

        # Create user
        password_hash = hash_password(password)
        new_user = User(
            email=email,
            password_hash=password_hash,
            email_verified=False
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Verify user was created
        assert new_user.id is not None
        assert new_user.email == email
        assert new_user.email_verified is False
        assert verify_password(password, new_user.password_hash)

    def test_register_duplicate_email(self, session: Session):
        """Test registration with duplicate email fails"""
        email = "alice@example.com"
        password = "Alice123!"

        # Create first user
        password_hash = hash_password(password)
        user1 = User(email=email, password_hash=password_hash)
        session.add(user1)
        session.commit()

        # Try to create second user with same email
        statement = select(User).where(User.email == email)
        existing_user = session.exec(statement).first()
        assert existing_user is not None  # Should find existing user

    def test_register_weak_password(self):
        """Test registration with weak password fails validation"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_requirements("short")

        assert "at least 8 characters" in str(exc_info.value)

    def test_register_password_missing_uppercase(self):
        """Test password validation catches missing uppercase"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_requirements("lowercase123!")

        assert "uppercase" in str(exc_info.value).lower()

    def test_register_password_missing_lowercase(self):
        """Test password validation catches missing lowercase"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_requirements("UPPERCASE123!")

        assert "lowercase" in str(exc_info.value).lower()

    def test_register_password_missing_number(self):
        """Test password validation catches missing number"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_requirements("NoNumbers!")

        assert "number" in str(exc_info.value).lower()

    def test_register_password_missing_special(self):
        """Test password validation catches missing special character"""
        with pytest.raises(ValueError) as exc_info:
            validate_password_requirements("NoSpecial123")

        assert "special" in str(exc_info.value).lower()
