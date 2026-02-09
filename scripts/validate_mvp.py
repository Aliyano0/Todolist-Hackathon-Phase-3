#!/usr/bin/env python3
"""
MVP Validation Script - Tests components that don't require Docker or SMTP

This script validates:
1. All imports work correctly
2. Configuration classes are properly structured
3. Email templates generate correctly
4. Email service interfaces are properly defined
5. Code structure and dependencies
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

def test_imports():
    """Test that all critical imports work"""
    print("Testing imports...")
    try:
        from core.config import SMTPConfig, AppConfig, get_config, init_config
        from core.services.email_service import EmailService, SMTPEmailService, EmailTemplate, EmailMessage
        from api.auth import router
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_smtp_config():
    """Test SMTP configuration structure"""
    print("\nTesting SMTP configuration...")
    try:
        from core.config import SMTPConfig

        # Test with valid config
        config = SMTPConfig(
            host="smtp.test.com",
            port=587,
            username="test@example.com",
            password="testpass",
            from_email="noreply@test.com",
            from_name="Test App",
            use_tls=True,
            timeout=30
        )

        assert config.host == "smtp.test.com"
        assert config.port == 587
        assert config.use_tls is True

        print("✅ SMTP configuration structure valid")
        return True
    except Exception as e:
        print(f"❌ SMTP configuration test failed: {e}")
        return False


def test_email_template():
    """Test email template generation"""
    print("\nTesting email template generation...")
    try:
        from core.services.email_service import EmailTemplate

        reset_url = "https://example.com/reset?token=abc123"
        user_email = "test@example.com"

        template = EmailTemplate.password_reset(reset_url, user_email)

        # Verify template structure
        assert hasattr(template, 'subject')
        assert hasattr(template, 'html_body')
        assert hasattr(template, 'text_body')

        # Verify content
        assert reset_url in template.html_body
        assert reset_url in template.text_body
        assert user_email in template.html_body
        assert "password" in template.subject.lower() or "reset" in template.subject.lower()

        # Verify HTML structure
        assert "<!DOCTYPE html>" in template.html_body or "<html>" in template.html_body
        assert "</html>" in template.html_body

        # Verify security warnings
        assert "ignore" in template.html_body.lower() or "didn't request" in template.html_body.lower()
        assert "expire" in template.html_body.lower() or "hour" in template.html_body.lower()

        # Verify plain text has no HTML tags
        assert "<html>" not in template.text_body
        assert "<body>" not in template.text_body

        print("✅ Email template generation successful")
        print(f"   Subject: {template.subject}")
        print(f"   HTML length: {len(template.html_body)} chars")
        print(f"   Text length: {len(template.text_body)} chars")
        return True
    except Exception as e:
        print(f"❌ Email template test failed: {e}")
        return False


def test_email_service_interface():
    """Test email service interface"""
    print("\nTesting email service interface...")
    try:
        from core.services.email_service import EmailService, SMTPEmailService, EmailMessage
        from core.config import SMTPConfig

        # Verify EmailService is abstract
        assert hasattr(EmailService, 'send_email')
        assert hasattr(EmailService, 'send_password_reset')

        # Verify SMTPEmailService can be instantiated
        smtp_config = SMTPConfig(
            host="smtp.test.com",
            port=587,
            username="test@example.com",
            password="testpass",
            from_email="noreply@test.com",
            from_name="Test App",
            use_tls=True,
            timeout=30
        )

        service = SMTPEmailService(smtp_config)
        assert service.config == smtp_config

        # Verify EmailMessage structure
        message = EmailMessage(
            to_email="user@example.com",
            subject="Test",
            html_body="<p>Test</p>",
            text_body="Test"
        )
        assert message.to_email == "user@example.com"

        print("✅ Email service interface valid")
        return True
    except Exception as e:
        print(f"❌ Email service interface test failed: {e}")
        return False


def test_dockerfile_exists():
    """Test that Dockerfile exists and has required instructions"""
    print("\nTesting Dockerfile...")
    try:
        dockerfile_path = backend_path / "Dockerfile"

        if not dockerfile_path.exists():
            print("❌ Dockerfile not found")
            return False

        content = dockerfile_path.read_text()

        # Check for required instructions
        required = [
            "FROM python:3.13-slim",
            "WORKDIR",
            "COPY requirements.txt",
            "RUN pip install",
            "COPY . .",
            "HEALTHCHECK",
            "CMD"
        ]

        missing = []
        for instruction in required:
            if instruction not in content:
                missing.append(instruction)

        if missing:
            print(f"❌ Dockerfile missing instructions: {', '.join(missing)}")
            return False

        print("✅ Dockerfile structure valid")
        print(f"   Size: {len(content)} bytes")
        return True
    except Exception as e:
        print(f"❌ Dockerfile test failed: {e}")
        return False


def test_dockerignore_exists():
    """Test that .dockerignore exists"""
    print("\nTesting .dockerignore...")
    try:
        dockerignore_path = backend_path / ".dockerignore"

        if not dockerignore_path.exists():
            print("❌ .dockerignore not found")
            return False

        content = dockerignore_path.read_text()

        # Check for important exclusions
        important = ["__pycache__", "*.pyc", ".git", "tests", ".env"]

        missing = []
        for pattern in important:
            if pattern not in content:
                missing.append(pattern)

        if missing:
            print(f"⚠️  .dockerignore missing patterns: {', '.join(missing)}")

        print("✅ .dockerignore exists")
        print(f"   Patterns: {len(content.splitlines())}")
        return True
    except Exception as e:
        print(f"❌ .dockerignore test failed: {e}")
        return False


def test_env_example_exists():
    """Test that .env.example exists with required variables"""
    print("\nTesting .env.example...")
    try:
        env_example_path = backend_path / ".env.example"

        if not env_example_path.exists():
            print("❌ .env.example not found")
            return False

        content = env_example_path.read_text()

        # Check for required variables
        required_vars = [
            "DATABASE_URL",
            "JWT_SECRET_KEY",
            "SMTP_HOST",
            "SMTP_PORT",
            "SMTP_USERNAME",
            "SMTP_PASSWORD",
            "SMTP_FROM_EMAIL",
            "FRONTEND_URL"
        ]

        missing = []
        for var in required_vars:
            if var not in content:
                missing.append(var)

        if missing:
            print(f"❌ .env.example missing variables: {', '.join(missing)}")
            return False

        print("✅ .env.example complete")
        print(f"   Variables: {len([l for l in content.splitlines() if '=' in l and not l.startswith('#')])}")
        return True
    except Exception as e:
        print(f"❌ .env.example test failed: {e}")
        return False


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("MVP VALIDATION - Code Structure Tests")
    print("=" * 60)

    tests = [
        test_imports,
        test_smtp_config,
        test_email_template,
        test_email_service_interface,
        test_dockerfile_exists,
        test_dockerignore_exists,
        test_env_example_exists
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100

    print(f"Tests passed: {passed}/{total} ({percentage:.1f}%)")

    if passed == total:
        print("\n✅ All validation tests passed!")
        print("\nNext steps:")
        print("1. Enable Docker Desktop WSL2 integration")
        print("2. Run: docker build -t todo-backend:mvp .")
        print("3. Configure SMTP credentials in .env")
        print("4. Test password reset email flow")
        return 0
    else:
        print("\n❌ Some validation tests failed")
        print("Please fix the issues above before proceeding")
        return 1


if __name__ == "__main__":
    sys.exit(main())
