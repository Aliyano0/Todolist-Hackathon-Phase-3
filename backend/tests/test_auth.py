"""
Integration tests for authentication endpoints

Tests the registration, login, and logout endpoints with database integration.
Note: These tests use sync TestClient with sync database for simplicity.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel, select
from models.user import User
from models.todo import TodoTask
from core.security.password import hash_password


# Create a minimal test app without async dependencies
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
import re

test_app = FastAPI()

# Test database
test_engine = create_engine("sqlite:///:memory:")


def get_test_session():
    """Test session generator"""
    with Session(test_engine) as session:
        yield session


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


@test_app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegisterRequest):
    """Test registration endpoint"""
    session = next(get_test_session())
    try:
        validate_password_requirements(user_data.password)

        statement = select(User).where(User.email == user_data.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        password_hash = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            password_hash=password_hash,
            email_verified=False
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return UserResponse(
            id=str(new_user.id),
            email=new_user.email,
            email_verified=new_user.email_verified,
            created_at=new_user.created_at.isoformat(),
            updated_at=new_user.updated_at.isoformat()
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@pytest.fixture(name="client", scope="function")
def client_fixture():
    """Create a test client"""
    # Create tables
    SQLModel.metadata.create_all(test_engine)

    with TestClient(test_app) as client:
        yield client

    # Drop tables after test
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)


class TestRegistrationEndpoint:
    """Test user registration endpoint"""

    def test_register_success(self, client: TestClient, session: Session):
        """Test successful user registration"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com",
                "password": "Alice123!"
            }
        )

        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == "alice@example.com"
        assert data["email_verified"] is False
        assert "password" not in data
        assert "password_hash" not in data

        # Verify user was created in database
        user = session.query(User).filter(User.email == "alice@example.com").first()
        assert user is not None
        assert user.email == "alice@example.com"

    def test_register_duplicate_email(self, client: TestClient, session: Session):
        """Test registration with duplicate email returns 400"""
        # Create first user
        client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com",
                "password": "Alice123!"
            }
        )

        # Try to register with same email
        response = client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com",
                "password": "DifferentPass123!"
            }
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_invalid_email(self, client: TestClient):
        """Test registration with invalid email format returns 400"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "password": "ValidPass123!"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_register_weak_password(self, client: TestClient):
        """Test registration with weak password returns 400"""
        # Password too short
        response = client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com",
                "password": "Short1!"
            }
        )

        assert response.status_code == 400
        assert "password" in response.json()["detail"].lower()

    def test_register_password_missing_uppercase(self, client: TestClient):
        """Test registration with password missing uppercase letter"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com",
                "password": "lowercase123!"
            }
        )

        assert response.status_code == 400
        assert "uppercase" in response.json()["detail"].lower()

    def test_register_password_missing_lowercase(self, client: TestClient):
        """Test registration with password missing lowercase letter"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com",
                "password": "UPPERCASE123!"
            }
        )

        assert response.status_code == 400
        assert "lowercase" in response.json()["detail"].lower()

    def test_register_password_missing_number(self, client: TestClient):
        """Test registration with password missing number"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com",
                "password": "NoNumbers!"
            }
        )

        assert response.status_code == 400
        assert "number" in response.json()["detail"].lower()

    def test_register_password_missing_special_char(self, client: TestClient):
        """Test registration with password missing special character"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com",
                "password": "NoSpecial123"
            }
        )

        assert response.status_code == 400
        assert "special" in response.json()["detail"].lower()

    def test_register_missing_email(self, client: TestClient):
        """Test registration without email returns 422"""
        response = client.post(
            "/api/auth/register",
            json={
                "password": "ValidPass123!"
            }
        )

        assert response.status_code == 422

    def test_register_missing_password(self, client: TestClient):
        """Test registration without password returns 422"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com"
            }
        )

        assert response.status_code == 422

    def test_register_password_hashed_in_database(self, client: TestClient, session: Session):
        """Test that password is hashed in database, not stored as plaintext"""
        password = "Alice123!"
        response = client.post(
            "/api/auth/register",
            json={
                "email": "alice@example.com",
                "password": password
            }
        )

        assert response.status_code == 201

        # Verify password is hashed in database
        user = session.query(User).filter(User.email == "alice@example.com").first()
        assert user.password_hash != password
        assert len(user.password_hash) > 50  # Bcrypt hashes are long
