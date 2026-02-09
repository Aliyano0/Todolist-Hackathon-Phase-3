"""
Unit tests for password hashing utilities

Tests the bcrypt-based password hashing and verification functions.
"""

import pytest
from core.security.password import hash_password, verify_password


class TestPasswordHashing:
    """Test password hashing functionality"""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_different_for_same_input(self):
        """Test that hashing the same password twice produces different hashes (due to salt)"""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2  # Different salts should produce different hashes

    def test_verify_password_correct_password(self):
        """Test that verify_password returns True for correct password"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect_password(self):
        """Test that verify_password returns False for incorrect password"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty_password(self):
        """Test that verify_password handles empty password"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password("", hashed) is False

    def test_verify_password_invalid_hash(self):
        """Test that verify_password returns False for invalid hash format"""
        password = "TestPassword123!"
        invalid_hash = "not-a-valid-hash"

        assert verify_password(password, invalid_hash) is False

    def test_hash_password_special_characters(self):
        """Test that password hashing works with special characters"""
        password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_hash_password_unicode_characters(self):
        """Test that password hashing works with unicode characters"""
        password = "Pässwörd123!你好"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_hash_password_long_password(self):
        """Test that password hashing works with long passwords (up to 72 bytes)"""
        password = "A" * 50 + "1!"  # 52 characters, well within bcrypt's 72-byte limit
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password("testpassword123!", hashed) is False
        assert verify_password("TESTPASSWORD123!", hashed) is False
