"""
Email template tests

Tests the EmailTemplate class:
- Password reset email template generation
- HTML body with inline CSS
- Plain text fallback
- Proper variable substitution
- Security warnings included
- Expiration notice included
"""

import pytest


def test_email_template_class_exists():
    """Test that EmailTemplate class exists"""
    from backend.core.services.email_service import EmailTemplate

    assert EmailTemplate is not None


def test_password_reset_template_method_exists():
    """Test that password_reset static method exists"""
    from backend.core.services.email_service import EmailTemplate

    assert hasattr(EmailTemplate, 'password_reset')
    assert callable(EmailTemplate.password_reset)


def test_password_reset_template_returns_template():
    """Test that password_reset returns EmailTemplate instance"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    assert template is not None
    assert hasattr(template, 'subject')
    assert hasattr(template, 'html_body')
    assert hasattr(template, 'text_body')


def test_password_reset_template_has_subject():
    """Test that password reset template has appropriate subject"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    assert template.subject is not None
    assert len(template.subject) > 0
    assert "password" in template.subject.lower() or "reset" in template.subject.lower()


def test_password_reset_template_includes_reset_url_in_html():
    """Test that HTML body includes the reset URL"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    assert reset_url in template.html_body


def test_password_reset_template_includes_reset_url_in_text():
    """Test that plain text body includes the reset URL"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    assert reset_url in template.text_body


def test_password_reset_template_includes_user_email():
    """Test that template includes user email for personalization"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    assert user_email in template.html_body


def test_password_reset_template_html_is_valid():
    """Test that HTML body is valid HTML"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    # Check for basic HTML structure
    assert "<!DOCTYPE html>" in template.html_body or "<html>" in template.html_body
    assert "</html>" in template.html_body
    assert "<body" in template.html_body
    assert "</body>" in template.html_body


def test_password_reset_template_html_uses_inline_css():
    """Test that HTML uses inline CSS for email client compatibility"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    # Check for inline styles
    assert 'style="' in template.html_body


def test_password_reset_template_includes_security_warning():
    """Test that template includes security warning"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    # Check for security-related text in both HTML and text versions
    html_lower = template.html_body.lower()
    text_lower = template.text_body.lower()

    # Should mention ignoring if not requested
    assert ("ignore" in html_lower or "didn't request" in html_lower)
    assert ("ignore" in text_lower or "didn't request" in text_lower)


def test_password_reset_template_includes_expiration_notice():
    """Test that template includes expiration notice"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    # Check for expiration-related text
    html_lower = template.html_body.lower()
    text_lower = template.text_body.lower()

    assert ("expire" in html_lower or "hour" in html_lower)
    assert ("expire" in text_lower or "hour" in text_lower)


def test_password_reset_template_text_is_readable():
    """Test that plain text version is readable without HTML tags"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    # Plain text should not contain HTML tags
    assert "<html>" not in template.text_body
    assert "<body>" not in template.text_body
    assert "<p>" not in template.text_body
    assert "<div>" not in template.text_body


def test_password_reset_template_html_has_clickable_link():
    """Test that HTML includes a clickable link (anchor tag)"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    # Should have an anchor tag with href
    assert '<a href="' in template.html_body
    assert reset_url in template.html_body


def test_password_reset_template_handles_special_characters_in_url():
    """Test that template handles special characters in reset URL"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset?token=abc123&user=test@example.com"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    # URL should be preserved correctly
    assert reset_url in template.html_body
    assert reset_url in template.text_body


def test_password_reset_template_is_mobile_responsive():
    """Test that HTML template uses mobile-responsive design"""
    from backend.core.services.email_service import EmailTemplate

    reset_url = "https://example.com/reset-password?token=abc123"
    user_email = "user@example.com"

    template = EmailTemplate.password_reset(reset_url, user_email)

    # Check for viewport meta tag or max-width styling
    assert ("max-width" in template.html_body or
            "viewport" in template.html_body or
            "width: 100%" in template.html_body)
