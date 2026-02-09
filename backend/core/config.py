"""
Centralized configuration management for production deployment

This module provides:
- Environment variable loading and validation
- SMTP configuration for email service
- Application settings with sensible defaults
- Startup validation to fail fast on misconfiguration
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SMTPConfig:
    """SMTP email service configuration"""
    host: str
    port: int
    username: str
    password: str
    from_email: str
    from_name: str
    use_tls: bool
    timeout: int

    @classmethod
    def from_env(cls) -> "SMTPConfig":
        """Load SMTP configuration from environment variables"""
        return cls(
            host=os.getenv("SMTP_HOST", ""),
            port=int(os.getenv("SMTP_PORT", "587")),
            username=os.getenv("SMTP_USERNAME", ""),
            password=os.getenv("SMTP_PASSWORD", ""),
            from_email=os.getenv("SMTP_FROM_EMAIL", ""),
            from_name=os.getenv("SMTP_FROM_NAME", "Todo App"),
            use_tls=os.getenv("SMTP_USE_TLS", "true").lower() == "true",
            timeout=int(os.getenv("SMTP_TIMEOUT", "30")),
        )


@dataclass
class SendGridConfig:
    """SendGrid email service configuration"""
    api_key: str
    from_email: str
    from_name: str

    @classmethod
    def from_env(cls) -> "SendGridConfig":
        """Load SendGrid configuration from environment variables"""
        return cls(
            api_key=os.getenv("SENDGRID_API_KEY", ""),
            from_email=os.getenv("SENDGRID_FROM_EMAIL", os.getenv("SMTP_FROM_EMAIL", "")),
            from_name=os.getenv("SENDGRID_FROM_NAME", "Todo App"),
        )


@dataclass
class AppConfig:
    """Application configuration for production"""
    environment: str
    debug: bool
    frontend_url: str
    backend_url: str
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expiry_days: int

    # Email configuration (SMTP or SendGrid)
    smtp: SMTPConfig
    sendgrid: SendGridConfig
    email_provider: str  # "smtp" or "sendgrid"

    # Security settings
    allowed_origins: list[str]
    rate_limit_enabled: bool
    rate_limit_per_minute: int

    # Logging
    log_level: str
    log_format: str

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables"""
        environment = os.getenv("ENVIRONMENT", "development")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

        # Determine email provider (prefer SendGrid for production)
        email_provider = os.getenv("EMAIL_PROVIDER", "sendgrid" if os.getenv("SENDGRID_API_KEY") else "smtp")

        return cls(
            environment=environment,
            debug=environment == "development",
            frontend_url=frontend_url,
            backend_url=os.getenv("BACKEND_URL", "http://localhost:8000"),
            database_url=os.getenv("DATABASE_URL", ""),
            jwt_secret_key=os.getenv("JWT_SECRET_KEY", ""),
            jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            jwt_expiry_days=int(os.getenv("JWT_EXPIRY_DAYS", "7")),
            smtp=SMTPConfig.from_env(),
            sendgrid=SendGridConfig.from_env(),
            email_provider=email_provider,
            allowed_origins=[frontend_url],
            rate_limit_enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_format=os.getenv("LOG_FORMAT", "json"),
        )

    def validate(self) -> None:
        """
        Validate configuration on startup

        Raises:
            ValueError: If configuration is invalid with detailed error messages
        """
        errors = []

        # Validate required fields
        if not self.database_url:
            errors.append("DATABASE_URL is required")
        if not self.jwt_secret_key:
            errors.append("JWT_SECRET_KEY is required")
        if len(self.jwt_secret_key) < 32:
            errors.append("JWT_SECRET_KEY must be at least 32 characters")
        if not self.frontend_url:
            errors.append("FRONTEND_URL is required")

        # Validate SMTP configuration
        if not self.smtp.host:
            errors.append("SMTP_HOST is required")
        if not self.smtp.username:
            errors.append("SMTP_USERNAME is required")
        if not self.smtp.password:
            errors.append("SMTP_PASSWORD is required")
        if not self.smtp.from_email:
            errors.append("SMTP_FROM_EMAIL is required")

        if errors:
            raise ValueError(
                f"Configuration validation failed:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )


# Global configuration instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """
    Get the global configuration instance

    Returns:
        AppConfig: The application configuration

    Raises:
        RuntimeError: If configuration has not been initialized
    """
    global _config
    if _config is None:
        raise RuntimeError(
            "Configuration not initialized. Call init_config() first."
        )
    return _config


def init_config() -> AppConfig:
    """
    Initialize and validate the global configuration

    This should be called once at application startup.

    Returns:
        AppConfig: The initialized and validated configuration

    Raises:
        ValueError: If configuration validation fails
    """
    global _config
    _config = AppConfig.from_env()
    _config.validate()
    return _config
