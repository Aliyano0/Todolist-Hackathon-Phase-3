"""
Health check endpoint integration tests

Tests to verify:
- /health endpoint returns correct status
- Database connection status is reported
- SMTP configuration status is reported
- Returns 200 when healthy
- Returns 503 when unhealthy
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    # Set required environment variables for testing
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

        # Initialize config for testing
        try:
            init_config()
        except:
            pass  # Config might already be initialized

        return TestClient(app)


def test_health_endpoint_exists(client):
    """Test that /health endpoint exists and responds"""
    response = client.get("/health")
    assert response.status_code in [200, 503], "Health endpoint should return 200 or 503"


def test_health_endpoint_returns_json(client):
    """Test that /health endpoint returns JSON response"""
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict), "Health check should return JSON object"


def test_health_endpoint_includes_status(client):
    """Test that /health endpoint includes status field"""
    response = client.get("/health")
    data = response.json()
    assert "status" in data, "Health check must include 'status' field"
    assert data["status"] in ["healthy", "unhealthy"], "Status must be 'healthy' or 'unhealthy'"


def test_health_endpoint_includes_timestamp(client):
    """Test that /health endpoint includes timestamp"""
    response = client.get("/health")
    data = response.json()
    assert "timestamp" in data, "Health check must include 'timestamp' field"
    assert isinstance(data["timestamp"], str), "Timestamp must be a string"
    # Verify ISO format
    assert "T" in data["timestamp"], "Timestamp should be in ISO format"


def test_health_endpoint_includes_version(client):
    """Test that /health endpoint includes version"""
    response = client.get("/health")
    data = response.json()
    assert "version" in data, "Health check must include 'version' field"
    assert isinstance(data["version"], str), "Version must be a string"


def test_health_endpoint_includes_database_status(client):
    """Test that /health endpoint includes database status"""
    response = client.get("/health")
    data = response.json()
    assert "database" in data, "Health check must include 'database' field"
    assert data["database"] in ["connected", "disconnected", "error"], \
        "Database status must be 'connected', 'disconnected', or 'error'"


def test_health_endpoint_includes_smtp_status(client):
    """Test that /health endpoint includes SMTP status"""
    response = client.get("/health")
    data = response.json()
    assert "smtp" in data, "Health check must include 'smtp' field"
    assert data["smtp"] in ["configured", "not_configured", "incomplete", "error", "not_initialized"], \
        "SMTP status must be valid"


def test_health_endpoint_returns_200_when_healthy(client):
    """Test that /health endpoint returns 200 when all checks pass"""
    with patch("main.get_config") as mock_config:
        # Mock healthy config
        mock_smtp = MagicMock()
        mock_smtp.host = "smtp.test.com"
        mock_smtp.username = "test"
        mock_smtp.from_email = "test@test.com"

        mock_cfg = MagicMock()
        mock_cfg.smtp = mock_smtp
        mock_config.return_value = mock_cfg

        response = client.get("/health")

        # If database is connected and SMTP is configured, should be 200
        if response.json().get("database") == "connected":
            assert response.status_code == 200, "Should return 200 when healthy"
            assert response.json()["status"] == "healthy"


def test_health_endpoint_returns_503_when_unhealthy(client):
    """Test that /health endpoint returns 503 when checks fail"""
    with patch("main.get_config") as mock_config:
        # Mock unhealthy config (missing SMTP)
        mock_smtp = MagicMock()
        mock_smtp.host = ""
        mock_smtp.username = ""
        mock_smtp.from_email = ""

        mock_cfg = MagicMock()
        mock_cfg.smtp = mock_smtp
        mock_config.return_value = mock_cfg

        response = client.get("/health")

        # Should return 503 when SMTP is incomplete
        assert response.status_code == 503, "Should return 503 when unhealthy"
        assert response.json()["status"] == "unhealthy"


def test_health_endpoint_includes_errors_when_unhealthy(client):
    """Test that /health endpoint includes error details when unhealthy"""
    with patch("main.get_config") as mock_config:
        # Mock unhealthy config
        mock_smtp = MagicMock()
        mock_smtp.host = ""
        mock_smtp.username = ""
        mock_smtp.from_email = ""

        mock_cfg = MagicMock()
        mock_cfg.smtp = mock_smtp
        mock_config.return_value = mock_cfg

        response = client.get("/health")
        data = response.json()

        if data["status"] == "unhealthy":
            assert "errors" in data, "Unhealthy response must include 'errors' field"
            assert isinstance(data["errors"], list), "Errors must be a list"
            assert len(data["errors"]) > 0, "Errors list must not be empty"


@pytest.mark.integration
def test_health_endpoint_with_real_database(client):
    """
    Integration test with real database connection

    This test requires a real database to be available
    """
    response = client.get("/health")
    data = response.json()

    # If DATABASE_URL is set to a real database, this should work
    if "postgresql" in os.getenv("DATABASE_URL", ""):
        assert data["database"] in ["connected", "error"], \
            "Database status should be 'connected' or 'error' with real database"
