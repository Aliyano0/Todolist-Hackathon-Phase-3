"""
SendGrid email service implementation

This module provides email service using SendGrid API instead of SMTP.
Works on platforms that block SMTP ports (like Hugging Face Spaces).

Setup:
1. Sign up at https://sendgrid.com (free tier: 100 emails/day)
2. Create API key in Settings > API Keys
3. Set SENDGRID_API_KEY environment variable
"""

import logging
from typing import Optional
import httpx

from core.services.email_service import EmailService, EmailMessage, EmailTemplate

logger = logging.getLogger(__name__)


class SendGridEmailService(EmailService):
    """SendGrid API implementation of email service"""

    def __init__(self, api_key: str, from_email: str, from_name: str = "Todo App"):
        """
        Initialize SendGrid email service

        Args:
            api_key: SendGrid API key
            from_email: Sender email address (must be verified in SendGrid)
            from_name: Sender name
        """
        self.api_key = api_key
        self.from_email = from_email
        self.from_name = from_name
        self.api_url = "https://api.sendgrid.com/v3/mail/send"

    async def send_email(self, message: EmailMessage) -> bool:
        """
        Send email via SendGrid API

        Args:
            message: Email message to send

        Returns:
            True if successful, False if failed
        """
        try:
            # Mask email for logging (privacy)
            masked_email = self._mask_email(message.to_email)
            logger.info(f"Sending email via SendGrid to {masked_email}")

            # Build SendGrid API payload
            payload = {
                "personalizations": [
                    {
                        "to": [{"email": message.to_email}],
                        "subject": message.subject
                    }
                ],
                "from": {
                    "email": message.from_email or self.from_email,
                    "name": message.from_name or self.from_name
                },
                "content": [
                    {
                        "type": "text/plain",
                        "value": message.text_body
                    },
                    {
                        "type": "text/html",
                        "value": message.html_body
                    }
                ]
            }

            # Send request to SendGrid API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=30.0
                )

                if response.status_code == 202:
                    logger.info(f"Email sent successfully to {masked_email}")
                    return True
                else:
                    logger.error(f"SendGrid API error: {response.status_code} - {response.text}")
                    return False

        except httpx.TimeoutException:
            logger.error(f"Timeout sending email to {masked_email}")
            return False
        except Exception as e:
            logger.error(f"SendGrid error sending email: {str(e)}")
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
        try:
            # Generate email template
            template = EmailTemplate.password_reset(reset_url, to_email)

            # Create email message
            message = EmailMessage(
                to_email=to_email,
                subject=template.subject,
                html_body=template.html_body,
                text_body=template.text_body,
                from_email=self.from_email,
                from_name=self.from_name
            )

            # Send email
            return await self.send_email(message)

        except Exception as e:
            logger.error(f"Error sending password reset email: {str(e)}")
            return False

    def _mask_email(self, email: str) -> str:
        """
        Mask email address for logging (privacy)

        Args:
            email: Email address to mask

        Returns:
            Masked email address (e.g., "u***@example.com")
        """
        if "@" not in email:
            return "***"

        local, domain = email.split("@", 1)
        if len(local) <= 2:
            masked_local = "*" * len(local)
        else:
            masked_local = local[0] + "*" * (len(local) - 2) + local[-1]

        return f"{masked_local}@{domain}"
