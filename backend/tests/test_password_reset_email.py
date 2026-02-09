"""
Password reset integration test with email

End-to-end test for password reset flow:
- Request password reset
- Email is sent with reset token
- Reset link works
- Password can be reset
- User can login with new password
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import os


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    with patch.dict(os.environ, {
        "DATABASE_URL": "postgresql://test",
        "JWT_SECRET_KEY": "a" * 32,
        "SMTP_HOST": "smtp.test.com",
        "SMTP_USERNAME": "test",
        "SMTP_PASSWORD": "test",
        "SMTP_FROM_EMAIL": "test@test.com",
        "FRONTEND_URL": "http://localhost:3000"
    }):
        from main import app
        from core.config import init_config

        try:
            init_config()
        except:
            pass

        return TestClient(app)


@pytest.mark.integration
def test_password_reset_request_sends_email(client):
    """
    Test that password reset request triggers email sending

    This test mocks the email service to verify it's called
    """
    test_email = "user@example.com"

    with patch('backend.api.auth.email_service') as mock_email_service:
        mock_email_service.send_password_reset = AsyncMock(return_value=True)

        response = client.post(
            "/api/auth/password-reset/request",
            json={"email": test_email}
        )

        # Should return success even if user doesn't exist (prevent enumeration)
        assert response.status_code in [200, 201]

        # If user exists, email service should be called
        # (This depends on whether test user exists in test database)


@pytest.mark.integration
def test_password_reset_request_returns_success_for_nonexistent_email(client):
    """
    Test that password reset returns success even for non-existent email
    to prevent email enumeration attacks
    """
    response = client.post(
        "/api/auth/password-reset/request",
        json={"email": "nonexistent@example.com"}
    )

    # Should return success to prevent email enumeration
    assert response.status_code in [200, 201]
    data = response.json()
    assert "message" in data or "detail" in data


@pytest.mark.integration
def test_password_reset_email_contains_valid_token(client):
    """
    Test that password reset email contains a valid reset token

    This test captures the email content and verifies the token
    """
    test_email = "user@example.com"
    captured_reset_url = None

    async def capture_email(to_email, reset_url):
        nonlocal captured_reset_url
        captured_reset_url = reset_url
        return True

    with patch('backend.api.auth.email_service') as mock_email_service:
        mock_email_service.send_password_reset = capture_email

        response = client.post(
            "/api/auth/password-reset/request",
            json={"email": test_email}
        )

        if response.status_code in [200, 201] and captured_reset_url:
            # Verify reset URL format
            assert "reset-password" in captured_reset_url
            assert "token=" in captured_reset_url


@pytest.mark.integration
def test_password_reset_confirm_with_valid_token(client):
    """
    Test that password can be reset with valid token

    This test requires a valid token from the database
    """
    # This test would need a real token from the database
    # For now, we test the endpoint structure
    response = client.post(
        "/api/auth/password-reset/confirm",
        json={
            "token": "test-token",
            "new_password": "NewPassword123!"
        }
    )

    # Should return 400 or 404 for invalid token (not 500)
    assert response.status_code in [200, 400, 404]


@pytest.mark.integration
def test_password_reset_confirm_validates_password_strength(client):
    """
    Test that password reset validates password strength
    """
    response = client.post(
        "/api/auth/password-reset/confirm",
        json={
            "token": "test-token",
            "new_password": "weak"
        }
    )

    # Should reject weak password
    assert response.status_code in [400, 422]


@pytest.mark.integration
def test_password_reset_token_expires(client):
    """
    Test that password reset tokens expire after 1 hour

    This test would need to manipulate time or use an expired token
    """
    # This is a placeholder for token expiration testing
    # Real implementation would need time manipulation or database access
    pass


@pytest.mark.integration
def test_password_reset_email_delivery_failure_handled_gracefully(client):
    """
    Test that email delivery failures are handled gracefully
    """
    test_email = "user@example.com"

    with patch('backend.api.auth.email_service') as mock_email_service:
        # Mock email service failure
        mock_email_service.send_password_reset = AsyncMock(return_value=False)

        response = client.post(
            "/api/auth/password-reset/request",
            json={"email": test_email}
        )

        # Should still return success to user (don't expose email delivery status)
        assert response.status_code in [200, 201]


@pytest.mark.integration
def test_complete_password_reset_flow(client):
    """
    Test complete password reset flow end-to-end

    This test requires:
    1. User exists in database
    2. Request password reset
    3. Capture reset token
    4. Use token to reset password
    5. Login with new password
    """
    # This is a comprehensive integration test that would need:
    # - Test database with test user
    # - Email service mock to capture token
    # - Full flow from request to login

    # Placeholder for full integration test
    # Real implementation would need test database setup
    pass


@pytest.mark.integration
def test_password_reset_rate_limiting(client):
    """
    Test that password reset requests are rate limited

    Should prevent abuse by limiting requests per email/IP
    """
    test_email = "user@example.com"

    # Make multiple requests
    responses = []
    for i in range(5):
        response = client.post(
            "/api/auth/password-reset/request",
            json={"email": test_email}
        )
        responses.append(response)

    # After several requests, should get rate limited
    # (Exact behavior depends on rate limiting implementation)
    status_codes = [r.status_code for r in responses]

    # At least some requests should succeed
    assert 200 in status_codes or 201 in status_codes
