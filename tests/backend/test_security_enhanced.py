import pytest
import hashlib
import secrets
from backend.core.security import hash_password, verify_password

def test_legacy_password_verification():
    """Test that verify_password still works with the legacy salt$hash format."""
    password = "secure_password123"
    salt = secrets.token_hex(16)
    # Replicate legacy hashing (100,000 iterations, no iteration count in string)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,
    )
    legacy_hash = f"{salt}${key.hex()}"

    # Verify legacy hash works
    assert verify_password(password, legacy_hash) is True
    assert verify_password("wrong_password", legacy_hash) is False

def test_new_password_hashing_and_verification():
    """Test that hash_password uses the new format and verify_password works with it."""
    password = "new_secure_password"
    new_hash = hash_password(password)

    # New format should have 3 parts: iterations$salt$hash
    assert new_hash.count("$") == 2
    parts = new_hash.split("$")
    assert parts[0] == "600000"

    # Verify new hash works
    assert verify_password(password, new_hash) is True
    assert verify_password("wrong_password", new_hash) is False

def test_verify_password_invalid_format():
    """Test that verify_password handles invalid formats gracefully."""
    assert verify_password("password", "invalid_format") is False
    assert verify_password("password", "part1$part2$part3$part4") is False
    assert verify_password("password", "") is False
