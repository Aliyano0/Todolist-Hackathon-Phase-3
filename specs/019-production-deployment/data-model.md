# Data Model: Production Deployment Configuration

**Feature**: 019-production-deployment
**Date**: 2026-02-09
**Status**: Complete

## Overview

This document defines the data structures and configuration entities required for production deployment. Unlike typical data models that define database schemas, this model focuses on configuration entities, service interfaces, and deployment artifacts.

---

## Configuration Entities

### 1. SMTP Configuration

**Purpose**: Email service configuration for password reset functionality

**Structure**:
```python
class SMTPConfig:
    """SMTP email service configuration"""
    host: str                    # SMTP server hostname (e.g., smtp.gmail.com)
    port: int                    # SMTP server port (587 for TLS, 465 for SSL)
    username: str                # SMTP authentication username
    password: str                # SMTP authentication password (secret)
    from_email: str              # Sender email address
    from_name: str               # Sender display name
    use_tls: bool = True         # Use STARTTLS encryption
    timeout: int = 30            # Connection timeout in seconds

    @classmethod
    def from_env(cls) -> "SMTPConfig":
        """Load configuration from environment variables"""
        return cls(
            host=os.getenv("SMTP_HOST"),
            port=int(os.getenv("SMTP_PORT", "587")),
            username=os.getenv("SMTP_USERNAME"),
            password=os.getenv("SMTP_PASSWORD"),
            from_email=os.getenv("SMTP_FROM_EMAIL"),
            from_name=os.getenv("SMTP_FROM_NAME", "Todo App"),
            use_tls=os.getenv("SMTP_USE_TLS", "true").lower() == "true",
            timeout=int(os.getenv("SMTP_TIMEOUT", "30")),
        )
```

**Validation Rules**:
- `host` must be non-empty string
- `port` must be between 1 and 65535
- `username` and `password` must be non-empty for authenticated SMTP
- `from_email` must be valid email format
- `timeout` must be positive integer

**Environment Variables**:
- `SMTP_HOST` (required)
- `SMTP_PORT` (optional, default: 587)
- `SMTP_USERNAME` (required)
- `SMTP_PASSWORD` (required, secret)
- `SMTP_FROM_EMAIL` (required)
- `SMTP_FROM_NAME` (optional, default: "Todo App")
- `SMTP_USE_TLS` (optional, default: true)
- `SMTP_TIMEOUT` (optional, default: 30)

---

### 2. Application Configuration

**Purpose**: Production application settings and feature flags

**Structure**:
```python
class AppConfig:
    """Application configuration for production"""
    environment: str             # "development" | "production"
    debug: bool                  # Enable debug mode (false in production)
    frontend_url: str            # Frontend URL for CORS and email links
    backend_url: str             # Backend URL for health checks
    database_url: str            # PostgreSQL connection string (secret)
    jwt_secret_key: str          # JWT signing secret (secret)
    jwt_algorithm: str = "HS256" # JWT signing algorithm
    jwt_expiry_days: int = 7     # JWT token expiry in days

    # Email configuration
    smtp: SMTPConfig

    # Security settings
    allowed_origins: list[str]   # CORS allowed origins
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60

    # Logging
    log_level: str = "INFO"      # "DEBUG" | "INFO" | "WARNING" | "ERROR"
    log_format: str = "json"     # "json" | "text"

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables"""
        environment = os.getenv("ENVIRONMENT", "development")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

        return cls(
            environment=environment,
            debug=environment == "development",
            frontend_url=frontend_url,
            backend_url=os.getenv("BACKEND_URL", "http://localhost:8000"),
            database_url=os.getenv("DATABASE_URL"),
            jwt_secret_key=os.getenv("JWT_SECRET_KEY"),
            jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            jwt_expiry_days=int(os.getenv("JWT_EXPIRY_DAYS", "7")),
            smtp=SMTPConfig.from_env(),
            allowed_origins=[frontend_url],
            rate_limit_enabled=os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true",
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_format=os.getenv("LOG_FORMAT", "json"),
        )

    def validate(self) -> None:
        """Validate configuration on startup"""
        errors = []

        if not self.database_url:
            errors.append("DATABASE_URL is required")
        if not self.jwt_secret_key:
            errors.append("JWT_SECRET_KEY is required")
        if len(self.jwt_secret_key) < 32:
            errors.append("JWT_SECRET_KEY must be at least 32 characters")
        if not self.frontend_url:
            errors.append("FRONTEND_URL is required")

        # Validate SMTP config
        if not self.smtp.host:
            errors.append("SMTP_HOST is required")
        if not self.smtp.username:
            errors.append("SMTP_USERNAME is required")
        if not self.smtp.password:
            errors.append("SMTP_PASSWORD is required")
        if not self.smtp.from_email:
            errors.append("SMTP_FROM_EMAIL is required")

        if errors:
            raise ValueError(f"Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
```

**Environment Variables**:
- `ENVIRONMENT` (optional, default: "development")
- `FRONTEND_URL` (required in production)
- `BACKEND_URL` (optional, for health checks)
- `DATABASE_URL` (required, secret)
- `JWT_SECRET_KEY` (required, secret, min 32 chars)
- `JWT_ALGORITHM` (optional, default: "HS256")
- `JWT_EXPIRY_DAYS` (optional, default: 7)
- `RATE_LIMIT_ENABLED` (optional, default: true)
- `RATE_LIMIT_PER_MINUTE` (optional, default: 60)
- `LOG_LEVEL` (optional, default: "INFO")
- `LOG_FORMAT` (optional, default: "json")

---

### 3. Email Template

**Purpose**: Password reset email content structure

**Structure**:
```python
class EmailTemplate:
    """Email template for password reset"""
    subject: str
    html_body: str
    text_body: str

    @staticmethod
    def password_reset(reset_url: str, user_email: str) -> "EmailTemplate":
        """Generate password reset email template"""
        subject = "Reset Your Password - Todo App"

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background-color: #4F46E5; padding: 20px; text-align: center;">
            <h1 style="color: white; margin: 0;">Todo App</h1>
        </div>
        <div style="padding: 30px 20px;">
            <h2 style="color: #4F46E5; margin-top: 0;">Reset Your Password</h2>
            <p>Hello,</p>
            <p>You requested to reset your password for your Todo App account (<strong>{user_email}</strong>).</p>
            <p>Click the button below to reset your password:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" style="display: inline-block; padding: 14px 28px; background-color: #4F46E5; color: white; text-decoration: none; border-radius: 6px; font-weight: bold;">Reset Password</a>
            </div>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; background-color: #f3f4f6; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px;">{reset_url}</p>
            <div style="margin-top: 30px; padding: 15px; background-color: #FEF3C7; border-left: 4px solid #F59E0B; border-radius: 4px;">
                <p style="margin: 0; color: #92400E;"><strong>⚠️ Important:</strong> This link will expire in 1 hour.</p>
            </div>
            <div style="margin-top: 20px; padding: 15px; background-color: #F3F4F6; border-radius: 4px;">
                <p style="margin: 0; color: #6B7280; font-size: 14px;">If you didn't request this password reset, you can safely ignore this email. Your password will not be changed.</p>
            </div>
        </div>
        <div style="background-color: #F9FAFB; padding: 20px; text-align: center; border-top: 1px solid #E5E7EB;">
            <p style="margin: 0; color: #6B7280; font-size: 12px;">© 2026 Todo App. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

        text_body = f"""
Todo App - Reset Your Password

Hello,

You requested to reset your password for your Todo App account ({user_email}).

Click the link below to reset your password:
{reset_url}

⚠️ IMPORTANT: This link will expire in 1 hour.

If you didn't request this password reset, you can safely ignore this email. Your password will not be changed.

---
© 2026 Todo App. All rights reserved.
"""

        return EmailTemplate(
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )
```

**Template Variables**:
- `reset_url`: Full URL with token (e.g., `https://app.vercel.app/reset-password?token=abc123`)
- `user_email`: User's email address for personalization

**Design Principles**:
- Mobile-responsive (max-width: 600px)
- Inline CSS for email client compatibility
- Clear call-to-action button
- Plain text fallback for accessibility
- Security warnings prominently displayed
- Expiration notice clearly visible

---

### 4. Docker Configuration

**Purpose**: Container build and runtime configuration

**Structure**:
```dockerfile
# Multi-stage build configuration
FROM python:3.13-slim as builder
# Build stage: Install dependencies

FROM python:3.13-slim
# Runtime stage: Minimal production image
```

**Build Arguments**:
- None (all configuration via environment variables)

**Environment Variables** (runtime):
- All `AppConfig` environment variables
- `PORT` (optional, default: 8000)
- `WORKERS` (optional, default: 4)

**Exposed Ports**:
- `8000`: FastAPI application

**Health Check**:
- Endpoint: `GET /health`
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3

**Volume Mounts**:
- None required (stateless application)

---

### 5. Deployment Configuration

**Purpose**: Platform-specific deployment settings

#### Hugging Face Spaces Configuration

**File**: `README.md` (frontmatter)
```yaml
---
title: Todo Backend API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---
```

**Required Files**:
- `Dockerfile` in repository root or backend/
- `requirements.txt` with all dependencies
- `.dockerignore` to exclude unnecessary files

**Environment Variables** (configured in Space settings):
- All production environment variables from `AppConfig`

#### Vercel Configuration

**File**: `vercel.json` (optional)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@production-api-url"
  }
}
```

**Environment Variables** (configured in Vercel dashboard):
- `NEXT_PUBLIC_API_URL`: Backend API URL from Hugging Face

---

## Service Interfaces

### Email Service Interface

**Purpose**: Abstract email sending for testability and flexibility

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class EmailMessage:
    """Email message structure"""
    to_email: str
    subject: str
    html_body: str
    text_body: str
    from_email: str | None = None
    from_name: str | None = None

class EmailService(ABC):
    """Abstract email service interface"""

    @abstractmethod
    async def send_email(self, message: EmailMessage) -> bool:
        """
        Send an email message

        Args:
            message: Email message to send

        Returns:
            True if email sent successfully, False otherwise

        Raises:
            EmailServiceError: If email sending fails critically
        """
        pass

    @abstractmethod
    async def send_password_reset(self, to_email: str, reset_url: str) -> bool:
        """
        Send password reset email

        Args:
            to_email: Recipient email address
            reset_url: Password reset URL with token

        Returns:
            True if email sent successfully, False otherwise
        """
        pass

class SMTPEmailService(EmailService):
    """SMTP implementation of email service"""

    def __init__(self, config: SMTPConfig):
        self.config = config

    async def send_email(self, message: EmailMessage) -> bool:
        """Send email via SMTP"""
        # Implementation in backend/core/services/email_service.py
        pass

    async def send_password_reset(self, to_email: str, reset_url: str) -> bool:
        """Send password reset email"""
        template = EmailTemplate.password_reset(reset_url, to_email)
        message = EmailMessage(
            to_email=to_email,
            subject=template.subject,
            html_body=template.html_body,
            text_body=template.text_body,
            from_email=self.config.from_email,
            from_name=self.config.from_name,
        )
        return await self.send_email(message)
```

---

## State Transitions

### Email Sending State Machine

```
[Request Password Reset]
         ↓
[Generate Token] → [Token Stored in DB]
         ↓
[Send Email] → [Pending]
         ↓
    ┌────┴────┐
    ↓         ↓
[Success]  [Failed]
    ↓         ↓
[Delivered] [Retry] → [Max Retries] → [Log Error]
```

**States**:
- **Pending**: Email queued for sending
- **Sending**: SMTP connection in progress
- **Success**: Email accepted by SMTP server
- **Failed**: SMTP error occurred
- **Delivered**: Email confirmed delivered (if tracking enabled)

**Transitions**:
- Request → Pending: User requests password reset
- Pending → Sending: Email service processes queue
- Sending → Success: SMTP server accepts email
- Sending → Failed: SMTP error (connection, auth, etc.)
- Failed → Retry: Retry with exponential backoff
- Retry → Failed: Max retries exceeded, log error

---

## Validation Rules

### Configuration Validation

**On Application Startup**:
1. Validate all required environment variables are present
2. Validate environment variable formats (URLs, emails, integers)
3. Validate secret lengths (JWT secret ≥ 32 characters)
4. Test database connection
5. Test SMTP connection (optional, can be skipped)
6. Fail fast with clear error messages if validation fails

**Example Validation**:
```python
def validate_config(config: AppConfig) -> None:
    """Validate configuration on startup"""
    config.validate()  # Raises ValueError if invalid

    # Test database connection
    try:
        engine = create_async_engine(config.database_url)
        # Test connection
    except Exception as e:
        raise ValueError(f"Database connection failed: {e}")

    # Optionally test SMTP connection
    if config.environment == "production":
        try:
            # Test SMTP connection
            pass
        except Exception as e:
            logger.warning(f"SMTP connection test failed: {e}")
```

### Email Validation

**Before Sending**:
1. Validate recipient email format
2. Check email is not in blocklist (future)
3. Validate reset token exists and is valid
4. Check rate limits for recipient

---

## Relationships

```
AppConfig
    ├── SMTPConfig (composition)
    └── Database Connection (reference)

EmailService
    ├── SMTPConfig (dependency)
    └── EmailTemplate (uses)

EmailTemplate
    └── User Email (parameter)

Docker Container
    ├── AppConfig (environment variables)
    └── Application Code (contains)

Deployment
    ├── Hugging Face Space (backend)
    ├── Vercel Project (frontend)
    └── Neon Database (shared)
```

---

## Performance Considerations

### Email Sending
- **Async Operations**: Use `aiosmtplib` for non-blocking email sending
- **Connection Pooling**: Reuse SMTP connections for multiple emails
- **Timeout**: 30-second timeout to prevent hanging requests
- **Retry Logic**: Exponential backoff (1s, 2s, 4s, 8s, 16s)

### Docker Container
- **Image Size**: Target < 200MB with multi-stage builds
- **Startup Time**: Target < 30 seconds with health checks
- **Memory Usage**: Target < 512MB RAM under normal load
- **CPU Usage**: 4 workers for concurrent request handling

### Configuration Loading
- **Lazy Loading**: Load configuration once on startup
- **Caching**: Cache configuration in memory (immutable)
- **Validation**: Validate once on startup, not per request

---

## Security Considerations

### Secrets Management
- All secrets in environment variables (never in code)
- Use platform secret management (Vercel, Hugging Face)
- Rotate secrets regularly (JWT secret, SMTP password)
- Never log secrets or include in error messages

### Email Security
- Use TLS/SSL for SMTP connections
- Validate email addresses to prevent injection
- Rate limit password reset requests (max 3 per hour per email)
- Include security warnings in email templates
- Log email sending attempts (without content)

### Configuration Security
- Validate all inputs on startup
- Use strong defaults (TLS enabled, secure headers)
- Fail closed (reject requests if config invalid)
- Sanitize all log output

---

## Testing Strategy

### Unit Tests
- Test configuration loading from environment variables
- Test configuration validation (missing, invalid values)
- Test email template generation
- Test email service interface (mocked SMTP)

### Integration Tests
- Test SMTP email sending (with test SMTP server)
- Test Docker container build and startup
- Test health check endpoint
- Test configuration validation on startup

### End-to-End Tests
- Test password reset flow with real email delivery
- Test deployment to staging environment
- Test CORS configuration with frontend
- Test error handling and logging

---

## Migration Notes

**No Database Migrations Required**: This feature adds infrastructure components only, no database schema changes.

**Configuration Migration**:
1. Add new environment variables to deployment platforms
2. Update CORS configuration with production frontend URL
3. Configure SMTP credentials in platform secrets
4. Test email delivery in staging environment
5. Deploy to production

**Rollback Plan**:
- If email service fails: Revert to console-based token delivery
- If Docker deployment fails: Use direct Python deployment
- If configuration invalid: Fix environment variables and redeploy
- No data loss risk (infrastructure changes only)
