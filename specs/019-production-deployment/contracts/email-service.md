# Email Service Contract

**Feature**: 019-production-deployment
**Date**: 2026-02-09
**Version**: 1.0.0

## Overview

This contract defines the interface for the email service used to send password reset emails and other transactional emails. The service abstracts SMTP implementation details and provides a clean interface for the application layer.

---

## Service Interface

### EmailService (Abstract Base Class)

**Purpose**: Define contract for email sending operations

**Methods**:

#### `send_email(message: EmailMessage) -> bool`

Send a generic email message.

**Parameters**:
- `message: EmailMessage` - Email message structure containing all required fields

**Returns**:
- `bool` - `True` if email sent successfully, `False` if failed but recoverable

**Raises**:
- `EmailServiceError` - Critical failure that cannot be recovered
- `ValidationError` - Invalid email address or message format

**Behavior**:
- MUST validate email address format before sending
- MUST use TLS/SSL for SMTP connection
- MUST handle SMTP errors gracefully
- MUST NOT expose SMTP credentials in error messages
- MUST log sending attempts (without email content)
- SHOULD retry on transient failures (connection timeout, etc.)
- SHOULD NOT retry on permanent failures (invalid recipient, etc.)

**Example**:
```python
message = EmailMessage(
    to_email="user@example.com",
    subject="Test Email",
    html_body="<p>Hello World</p>",
    text_body="Hello World",
    from_email="noreply@todoapp.com",
    from_name="Todo App"
)

success = await email_service.send_email(message)
if success:
    logger.info(f"Email sent to {message.to_email}")
else:
    logger.error(f"Failed to send email to {message.to_email}")
```

---

#### `send_password_reset(to_email: str, reset_url: str) -> bool`

Send password reset email with reset link.

**Parameters**:
- `to_email: str` - Recipient email address
- `reset_url: str` - Full password reset URL with token

**Returns**:
- `bool` - `True` if email sent successfully, `False` otherwise

**Raises**:
- `EmailServiceError` - Critical failure
- `ValidationError` - Invalid email address

**Behavior**:
- MUST use password reset email template
- MUST include both HTML and plain text versions
- MUST include security warnings in email
- MUST include expiration notice (1 hour)
- MUST validate email address format
- MUST NOT send if rate limit exceeded
- SHOULD personalize with user's email address

**Example**:
```python
reset_url = f"https://app.vercel.app/reset-password?token={token}"
success = await email_service.send_password_reset(
    to_email="user@example.com",
    reset_url=reset_url
)
```

---

## Data Structures

### EmailMessage

**Purpose**: Encapsulate email message data

**Fields**:
```python
@dataclass
class EmailMessage:
    to_email: str              # Recipient email (required)
    subject: str               # Email subject line (required)
    html_body: str             # HTML email body (required)
    text_body: str             # Plain text fallback (required)
    from_email: str | None     # Sender email (optional, uses config default)
    from_name: str | None      # Sender name (optional, uses config default)
```

**Validation**:
- `to_email` MUST be valid email format (RFC 5322)
- `subject` MUST be non-empty, max 998 characters
- `html_body` MUST be non-empty, valid HTML
- `text_body` MUST be non-empty
- `from_email` MUST be valid email format if provided

---

### SMTPConfig

**Purpose**: SMTP service configuration

**Fields**:
```python
@dataclass
class SMTPConfig:
    host: str                  # SMTP server hostname
    port: int                  # SMTP server port (587 or 465)
    username: str              # SMTP authentication username
    password: str              # SMTP authentication password (secret)
    from_email: str            # Default sender email
    from_name: str             # Default sender name
    use_tls: bool = True       # Use STARTTLS encryption
    timeout: int = 30          # Connection timeout in seconds
```

**Validation**:
- `host` MUST be non-empty
- `port` MUST be 1-65535
- `username` and `password` MUST be non-empty
- `from_email` MUST be valid email format
- `timeout` MUST be positive integer

---

## Implementation Contract

### SMTPEmailService

**Purpose**: SMTP implementation of EmailService interface

**Constructor**:
```python
def __init__(self, config: SMTPConfig):
    """
    Initialize SMTP email service

    Args:
        config: SMTP configuration

    Raises:
        ValueError: If configuration is invalid
    """
```

**Connection Management**:
- MUST establish TLS/SSL connection
- MUST authenticate with provided credentials
- SHOULD reuse connections for multiple emails
- MUST close connections properly on shutdown
- MUST handle connection timeouts gracefully

**Error Handling**:
- MUST catch and log SMTP exceptions
- MUST NOT expose credentials in error messages
- MUST distinguish between transient and permanent failures
- SHOULD retry transient failures with exponential backoff
- MUST return `False` for recoverable failures
- MUST raise `EmailServiceError` for critical failures

**Logging**:
- MUST log email sending attempts (INFO level)
- MUST log failures with error details (ERROR level)
- MUST NOT log email content or credentials
- SHOULD include recipient email (sanitized) in logs
- SHOULD include correlation ID for tracing

---

## Error Handling

### EmailServiceError

**Purpose**: Critical email service failure

**When to Raise**:
- SMTP server unreachable (after retries)
- Authentication failure
- Configuration error
- Unrecoverable SMTP error

**Example**:
```python
class EmailServiceError(Exception):
    """Critical email service error"""
    pass
```

### Transient Failures (Return False)

**When to Return False**:
- Temporary connection timeout
- Rate limit exceeded
- Recipient mailbox full
- Temporary server error (4xx SMTP codes)

**Retry Strategy**:
- Max retries: 3
- Backoff: Exponential (1s, 2s, 4s)
- Timeout: 30 seconds per attempt

### Permanent Failures (Return False)

**When to Return False**:
- Invalid recipient email
- Recipient does not exist
- Sender blocked by recipient
- Permanent server error (5xx SMTP codes)

**No Retry**: Do not retry permanent failures

---

## Rate Limiting

### Password Reset Emails

**Limits**:
- Max 3 password reset emails per email address per hour
- Max 10 password reset emails per IP address per hour
- Max 100 total password reset emails per hour (global)

**Implementation**:
- Check rate limit before sending email
- Return `False` if rate limit exceeded
- Log rate limit violations
- Do not expose rate limit details to users

**Storage**:
- Use in-memory cache (Redis in future)
- Key: `password_reset:{email}` or `password_reset:{ip}`
- TTL: 1 hour
- Increment on each attempt

---

## Security Requirements

### SMTP Security

**MUST**:
- Use TLS/SSL for all SMTP connections
- Validate server certificates
- Never send credentials over unencrypted connections
- Store SMTP password in environment variables only
- Rotate SMTP credentials regularly

**MUST NOT**:
- Log SMTP credentials
- Expose SMTP errors to end users
- Allow SMTP injection attacks
- Send emails without authentication

### Email Content Security

**MUST**:
- Sanitize all user input in email templates
- Validate URLs before including in emails
- Include security warnings in password reset emails
- Use HTTPS for all links in emails
- Include unsubscribe mechanism (future)

**MUST NOT**:
- Include sensitive data in email subject lines
- Send passwords or tokens in email body
- Use HTTP links in emails
- Include executable attachments

---

## Testing Contract

### Unit Tests

**Required Tests**:
- Email address validation
- Email template generation
- Configuration validation
- Error handling for invalid config
- Mock SMTP sending

**Example**:
```python
async def test_send_email_success():
    """Test successful email sending"""
    config = SMTPConfig(...)
    service = SMTPEmailService(config)

    message = EmailMessage(
        to_email="test@example.com",
        subject="Test",
        html_body="<p>Test</p>",
        text_body="Test"
    )

    success = await service.send_email(message)
    assert success is True
```

### Integration Tests

**Required Tests**:
- Send email to real SMTP server (test account)
- Test TLS connection
- Test authentication
- Test error handling with invalid credentials
- Test timeout handling

**Test SMTP Server**:
- Use Mailtrap, MailHog, or similar test SMTP service
- Do not use production SMTP in tests
- Clean up test emails after tests

### End-to-End Tests

**Required Tests**:
- Complete password reset flow with email delivery
- Verify email received in inbox
- Verify reset link works
- Test rate limiting
- Test error scenarios

---

## Performance Requirements

### Latency

**Targets**:
- Email sending: < 5 seconds (p95)
- SMTP connection: < 2 seconds
- Email delivery: < 30 seconds (end-to-end)

**Monitoring**:
- Track email sending duration
- Track SMTP connection time
- Track delivery success rate
- Alert on high latency or low success rate

### Throughput

**Targets**:
- Support 100 emails per minute
- Support 1000 emails per hour
- Handle burst traffic (password reset campaigns)

**Scaling**:
- Use connection pooling for high throughput
- Consider queue-based sending for large volumes
- Monitor SMTP provider rate limits

---

## Monitoring and Observability

### Metrics

**Required Metrics**:
- `email_sent_total` (counter) - Total emails sent
- `email_failed_total` (counter) - Total emails failed
- `email_send_duration_seconds` (histogram) - Email sending duration
- `smtp_connection_errors_total` (counter) - SMTP connection errors
- `rate_limit_exceeded_total` (counter) - Rate limit violations

**Labels**:
- `email_type`: "password_reset", "verification", etc.
- `status`: "success", "failed", "rate_limited"
- `error_type`: "connection", "auth", "timeout", etc.

### Logging

**Required Logs**:
- Email sending attempts (INFO)
- Email sending failures (ERROR)
- SMTP connection errors (ERROR)
- Rate limit violations (WARNING)
- Configuration validation (INFO)

**Log Format**:
```json
{
  "timestamp": "2026-02-09T12:00:00Z",
  "level": "INFO",
  "message": "Email sent successfully",
  "email_type": "password_reset",
  "recipient": "u***@example.com",
  "duration_ms": 1234,
  "correlation_id": "abc-123"
}
```

---

## Backward Compatibility

**Breaking Changes**: None (new feature)

**Deprecation**: Console-based token delivery will be deprecated in favor of email delivery

**Migration Path**:
1. Deploy email service alongside console delivery
2. Test email delivery in production
3. Switch to email-only delivery
4. Remove console delivery code

---

## Future Enhancements

**Planned**:
- Email verification emails
- Welcome emails for new users
- Task reminder emails
- Email templates management UI
- Email delivery tracking and analytics
- Bounce and complaint handling
- Unsubscribe mechanism

**Not Planned**:
- Marketing emails
- Bulk email campaigns
- Email list management
- A/B testing for emails
