"""
Unit tests for configuration validation

Tests the AppConfig class to ensure:
- All required environment variables are validated
- Configuration loads correctly from environment
- Validation fails with clear error messages for missing/invalid values
- SMTP configuration is properly validated
"""

import pytest
import os
from unittest.mock import patch


def test_config_validates_required_database_url():
    """Test that DATABASE_URL is required"""
    from backend.core.config import AppConfig

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="DATABASE_URL is required"):
            config = AppConfig.from_env()
            config.validate()


def test_config_validates_required_jwt_secret():
    """Test that JWT_SECRET_KEY is required"""
    from backend.core.config import AppConfig

    with patch.dict(os.environ, {"DATABASE_URL": "postgresql://test"}, clear=True):
        with pytest.raises(ValueError, match="JWT_SECRET_KEY is required"):
            config = AppConfig.from_env()
            config.validate()


def test_config_validates_jwt_secret_length():
    """Test that JWT_SECRET_KEY must be at least 32 characters"""
    from backend.core.config import AppConfig

    with patch.dict(os.environ, {
        "DATABASE_URL": "postgresql://test",
        "JWT_SECRET_KEY": "short"
    }, clear=True):
        with pytest.raises(ValueError, match="JWT_SECRET_KEY must be at least 32 characters"):
            config = AppConfig.from_env()
            config.validate()


def test_config_validates_required_smtp_host():
    """Test that SMTP_HOST is required"""
    from backend.core.config import AppConfig

    with patch.dict(os.environ, {
        "DATABASE_URL": "postgresql://test",
        "JWT_SECRET_KEY": "a" * 32,
        "FRONTEND_URL": "http://localhost:3000"
    }, clear=True):
        with pytest.raises(ValueError, match="SMTP_HOST is required"):
            config = AppConfig.from_env()
            config.validate()


def test_config_validates_required_smtp_credentials():
    """Test that SMTP username and password are required"""
    from backend.core.config import AppConfig

    with patch.dict(os.environ, {
        "DATABASE_URL": "postgresql://test",
        "JWT_SECRET_KEY": "a" * 32,
        "FRONTEND_URL": "http://localhost:3000",
        "SMTP_HOST": "smtp.gmail.com"
    }, clear=True):
        with pytest.raises(ValueError, match="SMTP_USERNAME is required"):
            config = AppConfig.from_env()
            config.validate()


def test_config_validates_required_smtp_from_email():
    """Test that SMTP_FROM_EMAIL is required"""
    from backend.core.config import AppConfig

    with patch.dict(os.environ, {
        "DATABASE_URL": "postgresql://test",
        "JWT_SECRET_KEY": "a" * 32,
        "FRONTEND_URL": "http://localhost:3000",
        "SMTP_HOST": "smtp.gmail.com",
        "SMTP_USERNAME": "user@example.com",
        "SMTP_PASSWORD": "password"
    }, clear=True):
        with pytest.raises(ValueError, match="SMTP_FROM_EMAIL is required"):
            config = AppConfig.from_env()
            config.validate()


def test_config_loads_with_all_required_variables():
    """Test that config loads successfully with all required variables"""
    from backend.core.config import AppConfig

    with patch.dict(os.environ, {
        "DATABASE_URL": "postgresql://test",
        "JWT_SECRET_KEY": "a" * 32,
        "FRONTEND_URL": "http://localhost:3000",
        "SMTP_HOST": "smtp.gmail.com",
        "SMTP_USERNAME": "user@example.com",
        "SMTP_PASSWORD": "password",
        "SMTP_FROM_EMAIL": "noreply@example.com"
    }, clear=True):
        config = AppConfig.from_env()
        config.validate()  # Should not raise

        assert config.database_url == "postgresql://test"
        assert config.jwt_secret_key == "a" * 32
        assert config.frontend_url == "http://localhost:3000"
        assert config.smtp.host == "smtp.gmail.com"
        assert config.smtp.username == "user@example.com"
        assert config.smtp.from_email == "noreply@example.com"


def test_config_uses_default_values():
    """Test that config uses default values for optional variables"""
    from backend.core.config import AppConfig

    with patch.dict(os.environ, {
        "DATABASE_URL": "postgresql://test",
        "JWT_SECRET_KEY": "a" * 32,
        "FRONTEND_URL": "http://localhost:3000",
        "SMTP_HOST": "smtp.gmail.com",
        "SMTP_USERNAME": "user@example.com",
        "SMTP_PASSWORD": "password",
        "SMTP_FROM_EMAIL": "noreply@example.com"
    }, clear=True):
        config = AppConfig.from_env()

        assert config.environment == "development"
        assert config.smtp.port == 587
        assert config.smtp.use_tls is True
        assert config.log_level == "INFO"


def test_config_respects_custom_values():
    """Test that config respects custom environment variable values"""
    from backend.core.config import AppConfig

    with patch.dict(os.environ, {
        "DATABASE_URL": "postgresql://test",
        "JWT_SECRET_KEY": "a" * 32,
        "FRONTEND_URL": "http://localhost:3000",
        "SMTP_HOST": "smtp.gmail.com",
        "SMTP_PORT": "465",
        "SMTP_USERNAME": "user@example.com",
        "SMTP_PASSWORD": "password",
        "SMTP_FROM_EMAIL": "noreply@example.com",
        "SMTP_USE_TLS": "false",
        "ENVIRONMENT": "production",
        "LOG_LEVEL": "ERROR"
    }, clear=True):
        config = AppConfig.from_env()

        assert config.environment == "production"
        assert config.smtp.port == 465
        assert config.smtp.use_tls is False
        assert config.log_level == "ERROR"
