"""
Comprehensive test suite for Authentication flows
Tests all authentication endpoints and security requirements per 017 specs
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from database.session import get_session
from sqlmodel import Session, SQLModel, create_engine
from models.user import User
from models.todo import TodoTask
import secrets
from datetime import datetime, timedelta


@pytest.fixture(scope="function")
def client():
    """Create a test client with a clean database for each test"""
    # Create an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)

    # Override the session dependency
    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def valid_user_data():
    """Valid user registration data"""
    return {
        "email": "test@example.com",
        "password": "SecurePass123!"
    }


@pytest.fixture
def registered_user(client, valid_user_data):
    """Create and return a registered user with verification token"""
    response = client.post("/api/auth/register", json=valid_user_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def verified_user(client, registered_user):
    """Create a verified user and return user data with tokens"""
    # Verify email
    verify_response = client.post(
        "/api/auth/verify-email",
        json={"token": registered_user["verification_token"]}
    )
    assert verify_response.status_code == 200

    # Login to get tokens
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": registered_user["email"],
            "password": "SecurePass123!"
        }
    )
    assert login_response.status_code == 200
    return login_response.json()


# ============================================================================
# FR-001: User Registration Tests
# ============================================================================

class TestUserRegistration:
    """Test user registration endpoint (FR-001)"""

    def test_register_valid_user(self, client, valid_user_data):
        """Test successful user registration"""
        response = client.post("/api/auth/register", json=valid_user_data)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == valid_user_data["email"]
        assert data["email_verified"] is False
        assert "verification_token" in data
        assert data["verification_token"] is not None
        assert "message" in data

    def test_register_duplicate_email(self, client, valid_user_data):
        """Test registration with duplicate email fails"""
        # Register first user
        response1 = client.post("/api/auth/register", json=valid_user_data)
        assert response1.status_code == 201

        # Try to register again with same email
        response2 = client.post("/api/auth/register", json=valid_user_data)
        assert response2.status_code == 400
        assert "detail" in response2.json()

    def test_register_invalid_password_too_short(self, client):
        """Test registration with password < 8 characters fails"""
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "Short1!"}
        )
        assert response.status_code == 422

    def test_register_invalid_password_no_uppercase(self, client):
        """Test registration without uppercase letter fails"""
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "lowercase123!"}
        )
        assert response.status_code == 422

    def test_register_invalid_password_no_number(self, client):
        """Test registration without number fails"""
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "NoNumbers!"}
        )
        assert response.status_code == 422

    def test_register_invalid_password_no_special_char(self, client):
        """Test registration without special character fails"""
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "NoSpecial123"}
        )
        assert response.status_code == 422

    def test_register_invalid_email_format(self, client):
        """Test registration with invalid email format fails"""
        response = client.post(
            "/api/auth/register",
            json={"email": "not-an-email", "password": "SecurePass123!"}
        )
        assert response.status_code == 422


# ============================================================================
# FR-014: Email Verification Tests
# ============================================================================

class TestEmailVerification:
    """Test email verification endpoint (FR-014)"""

    def test_verify_email_valid_token(self, client, registered_user):
        """Test email verification with valid token"""
        response = client.post(
            "/api/auth/verify-email",
            json={"token": registered_user["verification_token"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Email verified successfully"
        assert "user_id" in data
        assert "email" in data

    def test_verify_email_invalid_token(self, client):
        """Test email verification with invalid token fails"""
        response = client.post(
            "/api/auth/verify-email",
            json={"token": "invalid-token-12345"}
        )

        assert response.status_code == 400
        assert "Invalid or expired verification token" in response.json()["detail"]

    def test_verify_email_already_verified(self, client, registered_user):
        """Test verifying already verified email"""
        # First verification
        response1 = client.post(
            "/api/auth/verify-email",
            json={"token": registered_user["verification_token"]}
        )
        assert response1.status_code == 200

        # Try to verify again with same token
        response2 = client.post(
            "/api/auth/verify-email",
            json={"token": registered_user["verification_token"]}
        )
        assert response2.status_code == 400


# ============================================================================
# FR-002: User Login Tests
# ============================================================================

class TestUserLogin:
    """Test user login endpoint (FR-002)"""

    def test_login_valid_credentials(self, client, registered_user):
        """Test login with valid credentials after email verification"""
        # Verify email first
        client.post(
            "/api/auth/verify-email",
            json={"token": registered_user["verification_token"]}
        )

        # Login
        response = client.post(
            "/api/auth/login",
            json={"email": registered_user["email"], "password": "SecurePass123!"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user_id" in data

    def test_login_invalid_password(self, client, registered_user):
        """Test login with incorrect password fails"""
        # Verify email first
        client.post(
            "/api/auth/verify-email",
            json={"token": registered_user["verification_token"]}
        )

        # Try to login with wrong password
        response = client.post(
            "/api/auth/login",
            json={"email": registered_user["email"], "password": "WrongPassword123!"}
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_unverified_email(self, client, registered_user):
        """Test login with unverified email fails"""
        response = client.post(
            "/api/auth/login",
            json={"email": registered_user["email"], "password": "SecurePass123!"}
        )

        assert response.status_code == 401
        assert "Email not verified" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user fails"""
        response = client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "SecurePass123!"}
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]


# ============================================================================
# FR-015: Token Refresh Tests
# ============================================================================

class TestTokenRefresh:
    """Test token refresh endpoint (FR-015)"""

    def test_refresh_valid_token(self, client, verified_user):
        """Test refreshing access token with valid refresh token"""
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": verified_user["refresh_token"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        # Verify new tokens are different (sliding expiration)
        assert data["access_token"] != verified_user["access_token"]
        assert data["refresh_token"] != verified_user["refresh_token"]

    def test_refresh_invalid_token(self, client):
        """Test refresh with invalid token fails"""
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": "invalid-refresh-token"}
        )

        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]

    def test_refresh_sliding_expiration(self, client, verified_user):
        """Test that refresh returns new refresh token (sliding expiration)"""
        # First refresh
        response1 = client.post(
            "/api/auth/refresh",
            json={"refresh_token": verified_user["refresh_token"]}
        )
        assert response1.status_code == 200
        new_tokens1 = response1.json()

        # Second refresh with new refresh token
        response2 = client.post(
            "/api/auth/refresh",
            json={"refresh_token": new_tokens1["refresh_token"]}
        )
        assert response2.status_code == 200
        new_tokens2 = response2.json()

        # All tokens should be different
        assert new_tokens1["refresh_token"] != verified_user["refresh_token"]
        assert new_tokens2["refresh_token"] != new_tokens1["refresh_token"]


# ============================================================================
# FR-003, FR-004: Password Reset Tests
# ============================================================================

class TestPasswordReset:
    """Test password reset flow (FR-003, FR-004)"""

    def test_forgot_password_existing_user(self, client, registered_user):
        """Test password reset request for existing user"""
        response = client.post(
            "/api/auth/forgot-password",
            json={"email": registered_user["email"]}
        )

        assert response.status_code == 200
        assert "message" in response.json()

    def test_forgot_password_nonexistent_user(self, client):
        """Test password reset request for non-existent user (should not reveal)"""
        response = client.post(
            "/api/auth/forgot-password",
            json={"email": "nonexistent@example.com"}
        )

        # Should return same response for security (don't reveal if email exists)
        assert response.status_code == 200
        assert "message" in response.json()

    def test_reset_password_invalid_token(self, client):
        """Test password reset with invalid token fails"""
        response = client.post(
            "/api/auth/reset-password",
            json={"token": "invalid-token", "new_password": "NewSecure123!"}
        )

        assert response.status_code == 400
        assert "Invalid or expired reset token" in response.json()["detail"]

    def test_reset_password_invalid_new_password(self, client):
        """Test password reset with invalid new password fails"""
        response = client.post(
            "/api/auth/reset-password",
            json={"token": "some-token", "new_password": "weak"}
        )

        assert response.status_code == 422


# ============================================================================
# FR-005: Protected Endpoint Access Tests
# ============================================================================

class TestProtectedEndpoints:
    """Test protected endpoint access (FR-005)"""

    def test_access_me_with_valid_token(self, client, verified_user):
        """Test accessing /me endpoint with valid token"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {verified_user['access_token']}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data
        assert "email_verified" in data

    def test_access_me_without_token(self, client):
        """Test accessing /me endpoint without token fails"""
        response = client.get("/api/auth/me")

        assert response.status_code == 401

    def test_access_me_with_invalid_token(self, client):
        """Test accessing /me endpoint with invalid token fails"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid-token"}
        )

        assert response.status_code == 401


# ============================================================================
# FR-006: User Isolation Tests
# ============================================================================

class TestUserIsolation:
    """Test user isolation for task endpoints (FR-006)"""

    def test_user_cannot_access_other_users_tasks(self, client, valid_user_data):
        """Test that users can only access their own tasks"""
        # Create and verify first user
        user1_data = valid_user_data.copy()
        user1_response = client.post("/api/auth/register", json=user1_data)
        user1 = user1_response.json()
        client.post("/api/auth/verify-email", json={"token": user1["verification_token"]})
        user1_login = client.post("/api/auth/login", json=user1_data).json()

        # Create and verify second user
        user2_data = {"email": "user2@example.com", "password": "SecurePass123!"}
        user2_response = client.post("/api/auth/register", json=user2_data)
        user2 = user2_response.json()
        client.post("/api/auth/verify-email", json={"token": user2["verification_token"]})
        user2_login = client.post("/api/auth/login", json=user2_data).json()

        # User 1 tries to access User 2's tasks endpoint
        response = client.get(
            f"/api/{user2_login['user_id']}/tasks",
            headers={"Authorization": f"Bearer {user1_login['access_token']}"}
        )

        assert response.status_code == 403
        assert "Cannot access another user's tasks" in response.json()["detail"]

    def test_user_can_access_own_tasks(self, client, verified_user):
        """Test that users can access their own tasks"""
        response = client.get(
            f"/api/{verified_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {verified_user['access_token']}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)


# ============================================================================
# Integration Tests
# ============================================================================

class TestAuthenticationIntegration:
    """Integration tests for complete authentication flows"""

    def test_complete_registration_to_task_creation_flow(self, client):
        """Test complete flow: register -> verify -> login -> create task"""
        # 1. Register
        register_response = client.post(
            "/api/auth/register",
            json={"email": "integration@example.com", "password": "SecurePass123!"}
        )
        assert register_response.status_code == 201
        user_data = register_response.json()

        # 2. Verify email
        verify_response = client.post(
            "/api/auth/verify-email",
            json={"token": user_data["verification_token"]}
        )
        assert verify_response.status_code == 200

        # 3. Login
        login_response = client.post(
            "/api/auth/login",
            json={"email": "integration@example.com", "password": "SecurePass123!"}
        )
        assert login_response.status_code == 200
        tokens = login_response.json()

        # 4. Create a task
        task_response = client.post(
            f"/api/{tokens['user_id']}/tasks",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
            json={
                "title": "Integration test task",
                "description": "Test task",
                "completed": False,
                "priority": "high",
                "category": "work"
            }
        )
        assert task_response.status_code == 201

        # 5. Verify task was created
        get_tasks_response = client.get(
            f"/api/{tokens['user_id']}/tasks",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        assert get_tasks_response.status_code == 200
        tasks = get_tasks_response.json()["data"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Integration test task"
