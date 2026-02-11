import hashlib
import secrets

def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2 with SHA-256 and a random salt.
    Format: salt$hash
    """
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000  # Number of iterations
    )
    return f"{salt}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    try:
        salt, stored_hash = hashed_password.split("$")
        key = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        )
        return key.hex() == stored_hash
    except (ValueError, AttributeError):
        return False
