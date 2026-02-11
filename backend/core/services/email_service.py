"""
Email service for sending transactional emails

This module provides:
- EmailService abstract interface
- EmailMessage data structure
- EmailTemplate for password reset emails
- SMTPEmailService implementation using aiosmtplib
- Error handling and logging
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
import logging
from typing import Optional

from core.config import SMTPConfig


logger = logging.getLogger(__name__)


@dataclass
class EmailMessage:
    """Email message structure"""
    to_email: str
    subject: str
    html_body: str
    text_body: str
    from_email: Optional[str] = None
    from_name: Optional[str] = None


class EmailTemplate:
    """Email template generator"""

    def __init__(self, subject: str, html_body: str, text_body: str):
        self.subject = subject
        self.html_body = html_body
        self.text_body = text_body

    @staticmethod
    def password_reset(reset_url: str, user_email: str) -> "EmailTemplate":
        """
        Generate password reset email template

        Args:
            reset_url: Full URL with reset token
            user_email: User's email address for personalization

        Returns:
            EmailTemplate with HTML and plain text versions
        """
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
            text_body=text_body
        )

    @staticmethod
    def email_verification(verification_url: str, user_email: str) -> "EmailTemplate":
        """
        Generate email verification template

        Args:
            verification_url: Full URL with verification token
            user_email: User's email address for personalization

        Returns:
            EmailTemplate with HTML and plain text versions
        """
        subject = "Verify Your Email - Todo App"

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
            <h2 style="color: #4F46E5; margin-top: 0;">Verify Your Email Address</h2>
            <p>Hello,</p>
            <p>Thank you for registering with Todo App! Please verify your email address (<strong>{user_email}</strong>) to access all features, including the AI chatbot.</p>
            <p>Click the button below to verify your email:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}" style="display: inline-block; padding: 14px 28px; background-color: #4F46E5; color: white; text-decoration: none; border-radius: 6px; font-weight: bold;">Verify Email</a>
            </div>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; background-color: #f3f4f6; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px;">{verification_url}</p>
            <div style="margin-top: 20px; padding: 15px; background-color: #F3F4F6; border-radius: 4px;">
                <p style="margin: 0; color: #6B7280; font-size: 14px;">If you didn't create an account with Todo App, you can safely ignore this email.</p>
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
Todo App - Verify Your Email Address

Hello,

Thank you for registering with Todo App! Please verify your email address ({user_email}) to access all features, including the AI chatbot.

Click the link below to verify your email:
{verification_url}

If you didn't create an account with Todo App, you can safely ignore this email.

---
© 2026 Todo App. All rights reserved.
"""

        return EmailTemplate(
            subject=subject,
            html_body=html_body,
            text_body=text_body
        )


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

    @abstractmethod
    async def send_verification_email(self, to_email: str, verification_url: str) -> bool:
        """
        Send email verification email

        Args:
            to_email: Recipient email address
            verification_url: Email verification URL with token

        Returns:
            True if email sent successfully, False otherwise
        """
        pass


class SMTPEmailService(EmailService):
    """SMTP implementation of email service using aiosmtplib"""

    def __init__(self, config: SMTPConfig):
        self.config = config

    async def send_email(self, message: EmailMessage) -> bool:
        """
        Send email via SMTP

        Args:
            message: Email message to send

        Returns:
            True if successful, False if failed
        """
        try:
            # Create MIME message
            mime_message = MIMEMultipart("alternative")
            mime_message["Subject"] = message.subject
            mime_message["From"] = f"{message.from_name or self.config.from_name} <{message.from_email or self.config.from_email}>"
            mime_message["To"] = message.to_email

            # Attach plain text and HTML versions
            text_part = MIMEText(message.text_body, "plain")
            html_part = MIMEText(message.html_body, "html")
            mime_message.attach(text_part)
            mime_message.attach(html_part)

            # Log attempt (without exposing content)
            logger.info(f"Sending email to {message.to_email[:3]}***@{message.to_email.split('@')[1] if '@' in message.to_email else 'unknown'}")

            # Send email using aiosmtplib with proper TLS handling
            # For Gmail port 587, we need to use start_tls parameter
            # This function handles connection, authentication, and sending automatically
            await aiosmtplib.send(
                mime_message,
                hostname=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                start_tls=self.config.use_tls,  # Use STARTTLS for port 587
                timeout=self.config.timeout
            )

            logger.info(f"Email sent successfully to {message.to_email[:3]}***")
            return True

        except aiosmtplib.SMTPException as e:
            logger.error(f"SMTP error sending email: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}")
            return False

    async def send_password_reset(self, to_email: str, reset_url: str) -> bool:
        """
        Send password reset email

        Args:
            to_email: Recipient email address
            reset_url: Password reset URL with token

        Returns:
            True if successful, False if failed
        """
        template = EmailTemplate.password_reset(reset_url, to_email)

        message = EmailMessage(
            to_email=to_email,
            subject=template.subject,
            html_body=template.html_body,
            text_body=template.text_body,
            from_email=self.config.from_email,
            from_name=self.config.from_name
        )

        return await self.send_email(message)

    async def send_verification_email(self, to_email: str, verification_url: str) -> bool:
        """
        Send email verification email

        Args:
            to_email: Recipient email address
            verification_url: Email verification URL with token

        Returns:
            True if successful, False if failed
        """
        template = EmailTemplate.email_verification(verification_url, to_email)

        message = EmailMessage(
            to_email=to_email,
            subject=template.subject,
            html_body=template.html_body,
            text_body=template.text_body,
            from_email=self.config.from_email,
            from_name=self.config.from_name
        )

        return await self.send_email(message)

