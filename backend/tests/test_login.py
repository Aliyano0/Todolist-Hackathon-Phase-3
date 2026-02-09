"""
Tests for login functionality

Tests password verification and login business logic.
"""

import pytest
from sqlmodel import Session, create_engine, SQLModel, select
from models.user import User
from core.security.password import hash_password, verify_password


# Create test database
test_engine = create_engine("sqlite:///:memory:")


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)


class TestLoginLogic:
    """Test login business logic"""

    def test_password_verification_success(self):
        """Test that password verification works correctly"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_password_verification_failure(self):
        """Test that password verification fails with wrong password"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_login_user_exists(self, session: Session):
        """Test login with existing user"""
        email = "alice@example.com"
        password = "Alice123!"

        # Create user
        password_hash = hash_password(password)
        user = User(
            email=email,
            password_hash=password_hash,
            email_verified=True
        )
        session.add(user)
        session.commit()

        # Verify user exists and password is correct
        statement = select(User).where(User.email == email)
        found_user = session.exec(statement).first()

        assert found_user is not None
        assert found_user.email == email
        assert verify_password(password, found_user.password_hash)

    def test_login_user_not_found(self, session: Session):
        """Test login with non-existent user"""
        email = "nonexistent@example.com"

        statement = select(User).where(User.email == email)
        found_user = session.exec(statement).first()

        assert found_user is None

    def test_login_invalid_credentials(self, session: Session):
        """Test login with invalid credentials"""
        email = "alice@example.com"
        password = "Alice123!"
        wrong_password = "WrongPassword456!"

        # Create user
        password_hash = hash_password(password)
        user = User(
            email=email,
            password_hash=password_hash,
            email_verified=True
        )
        session.add(user)
        session.commit()

        # Try to verify with wrong password
        statement = select(User).where(User.email == email)
        found_user = session.exec(statement).first()

        assert found_user is not None
        assert verify_password(wrong_password, found_user.password_hash) is False
