import pytest
from backend.core.security import hash_password, verify_password

def test_password_hashing_basic():
    password = "test_password_123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_password_hashing_format():
    password = "test_password_123"
    hashed = hash_password(password)

    # Check if it has the expected parts
    parts = hashed.split("$")
    # Current format: salt$hash (2 parts)
    # Target format: iterations$salt$hash (3 parts)
    assert len(parts) >= 2

def test_backward_compatibility():
    # This is a hash generated with the old 100,000 iterations, salt$hash format
    old_hash = "2bf5a52392da46d74e1fe082dfb6d9ae$060e7975392791f5b94c5fa32aec1f9b643f1e79aa60b985cde917afcc5f3e10"
    assert verify_password("password123", old_hash) is True

def test_new_format_support():
    # This represents the target format: iterations$salt$hash
    # Using 600,000 iterations
    # We'll see if it can verify this once we implement it
    password = "new_secure_password"
    hashed = hash_password(password)
    assert hashed.count("$") == 2
    assert hashed.startswith("600000$")
    assert verify_password(password, hashed) is True
