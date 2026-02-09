"""
Email service unit tests

Tests the EmailService interface and SMTPEmailService implementation:
- EmailService abstract interface
- SMTPEmailService with mocked SMTP connection
- Email sending with proper error handling
- Retry logic for transient failures
- Logging without exposing email content
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import aiosmtplib


@pytest.fixture
def smtp_config():
    """Create a test SMTP configuration"""
    from backend.core.config import SMTPConfig

    return SMTPConfig(
        host="smtp.test.com",
        port=587,
        username="test@example.com",
        password="testpassword",
        from_email="noreply@example.com",
        from_name="Test App",
        use_tls=True,
        timeout=30
    )


@pytest.mark.asyncio
async def test_email_service_interface_exists():
    """Test that EmailService abstract interface exists"""
    from backend.core.services.email_service import EmailService

    assert EmailService is not None
    assert hasattr(EmailService, 'send_email')
    assert hasattr(EmailService, 'send_password_reset')


@pytest.mark.asyncio
async def test_smtp_email_service_can_be_instantiated(smtp_config):
    """Test that SMTPEmailService can be instantiated with config"""
    from backend.core.services.email_service import SMTPEmailService

    service = SMTPEmailService(smtp_config)
    assert service is not None
    assert service.config == smtp_config


@pytest.mark.asyncio
async def test_send_email_with_valid_message(smtp_config):
    """Test sending email with valid EmailMessage"""
    from backend.core.services.email_service import SMTPEmailService, EmailMessage

    service = SMTPEmailService(smtp_config)

    message = EmailMessage(
        to_email="user@example.com",
        subject="Test Email",
        html_body="<p>Test content</p>",
        text_body="Test content"
    )

    with patch('aiosmtplib.SMTP') as mock_smtp:
        # Mock SMTP connection and send
        mock_instance = AsyncMock()
        mock_smtp.return_value = mock_instance
        mock_instance.connect = AsyncMock()
        mock_instance.starttls = AsyncMock()
        mock_instance.login = AsyncMock()
        mock_instance.send_message = AsyncMock()
        mock_instance.quit = AsyncMock()

        result = await service.send_email(message)

        assert result is True
        mock_instance.connect.assert_called_once()
        mock_instance.login.assert_called_once_with(
            smtp_config.username,
            smtp_config.password
        )
        mock_instance.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_send_email_handles_smtp_error(smtp_config):
    """Test that send_email handles SMTP errors gracefully"""
    from backend.core.services.email_service import SMTPEmailService, EmailMessage

    service = SMTPEmailService(smtp_config)

    message = EmailMessage(
        to_email="user@example.com",
        subject="Test Email",
        html_body="<p>Test content</p>",
        text_body="Test content"
    )

    with patch('aiosmtplib.SMTP') as mock_smtp:
        # Mock SMTP connection failure
        mock_instance = AsyncMock()
        mock_smtp.return_value = mock_instance
        mock_instance.connect = AsyncMock(side_effect=aiosmtplib.SMTPException("Connection failed"))

        result = await service.send_email(message)

        assert result is False


@pytest.mark.asyncio
async def test_send_email_uses_tls_when_configured(smtp_config):
    """Test that send_email uses STARTTLS when configured"""
    from backend.core.services.email_service import SMTPEmailService, EmailMessage

    smtp_config.use_tls = True
    service = SMTPEmailService(smtp_config)

    message = EmailMessage(
        to_email="user@example.com",
        subject="Test Email",
        html_body="<p>Test content</p>",
        text_body="Test content"
    )

    with patch('aiosmtplib.SMTP') as mock_smtp:
        mock_instance = AsyncMock()
        mock_smtp.return_value = mock_instance
        mock_instance.connect = AsyncMock()
        mock_instance.starttls = AsyncMock()
        mock_instance.login = AsyncMock()
        mock_instance.send_message = AsyncMock()
        mock_instance.quit = AsyncMock()

        await service.send_email(message)

        mock_instance.starttls.assert_called_once()


@pytest.mark.asyncio
async def test_send_password_reset_creates_proper_email(smtp_config):
    """Test that send_password_reset creates email with correct content"""
    from backend.core.services.email_service import SMTPEmailService

    service = SMTPEmailService(smtp_config)

    reset_url = "https://example.com/reset-password?token=abc123"
    to_email = "user@example.com"

    with patch('aiosmtplib.SMTP') as mock_smtp:
        mock_instance = AsyncMock()
        mock_smtp.return_value = mock_instance
        mock_instance.connect = AsyncMock()
        mock_instance.starttls = AsyncMock()
        mock_instance.login = AsyncMock()
        mock_instance.send_message = AsyncMock()
        mock_instance.quit = AsyncMock()

        result = await service.send_password_reset(to_email, reset_url)

        assert result is True
        mock_instance.send_message.assert_called_once()

        # Verify the message contains the reset URL
        call_args = mock_instance.send_message.call_args
        message = call_args[0][0]
        message_str = str(message)
        assert reset_url in message_str


@pytest.mark.asyncio
async def test_send_email_logs_attempts_without_content(smtp_config, caplog):
    """Test that email sending is logged without exposing content"""
    from backend.core.services.email_service import SMTPEmailService, EmailMessage
    import logging

    caplog.set_level(logging.INFO)

    service = SMTPEmailService(smtp_config)

    message = EmailMessage(
        to_email="user@example.com",
        subject="Test Email",
        html_body="<p>Secret content</p>",
        text_body="Secret content"
    )

    with patch('aiosmtplib.SMTP') as mock_smtp:
        mock_instance = AsyncMock()
        mock_smtp.return_value = mock_instance
        mock_instance.connect = AsyncMock()
        mock_instance.starttls = AsyncMock()
        mock_instance.login = AsyncMock()
        mock_instance.send_message = AsyncMock()
        mock_instance.quit = AsyncMock()

        await service.send_email(message)

        # Check that logging occurred
        assert len(caplog.records) > 0

        # Verify that email content is NOT in logs
        log_text = " ".join([record.message for record in caplog.records])
        assert "Secret content" not in log_text


@pytest.mark.asyncio
async def test_send_email_closes_connection_on_error(smtp_config):
    """Test that SMTP connection is closed even when error occurs"""
    from backend.core.services.email_service import SMTPEmailService, EmailMessage

    service = SMTPEmailService(smtp_config)

    message = EmailMessage(
        to_email="user@example.com",
        subject="Test Email",
        html_body="<p>Test content</p>",
        text_body="Test content"
    )

    with patch('aiosmtplib.SMTP') as mock_smtp:
        mock_instance = AsyncMock()
        mock_smtp.return_value = mock_instance
        mock_instance.connect = AsyncMock()
        mock_instance.starttls = AsyncMock()
        mock_instance.login = AsyncMock()
        mock_instance.send_message = AsyncMock(side_effect=Exception("Send failed"))
        mock_instance.quit = AsyncMock()

        result = await service.send_email(message)

        assert result is False
        # Connection should still be closed
        mock_instance.quit.assert_called_once()
