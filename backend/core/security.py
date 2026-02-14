import hashlib
import secrets
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from .config import settings

# API Key configuration
admin_api_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)


async def verify_admin_api_key(api_key: str = Security(admin_api_key_header)):
    """
    Verify the admin API key provided in the request header.
    """
    if not api_key:
        raise HTTPException(status_code=404, detail="Not Found")

    if not secrets.compare_digest(api_key, settings.ADMIN_API_KEY):
        raise HTTPException(status_code=404, detail="Not Found")

    return api_key


PBKDF2_ITERATIONS = 600000


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2 with SHA-256 and a random salt.
    Format: iterations$salt$hash
    """
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PBKDF2_ITERATIONS,
    )
    return f"{PBKDF2_ITERATIONS}${salt}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Supports both legacy (salt$hash) and enhanced (iterations$salt$hash) formats.
    Uses secrets.compare_digest to prevent timing attacks.
    """
    try:
        parts = hashed_password.split("$")
        if len(parts) == 3:
            # Enhanced format: iterations$salt$hash
            iterations, salt, stored_hash = parts
            iterations = int(iterations)
        elif len(parts) == 2:
            # Legacy format: salt$hash
            salt, stored_hash = parts
            iterations = 100000
        else:
            return False

        key = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
        )
        return secrets.compare_digest(key.hex(), stored_hash)
    except (ValueError, AttributeError):
        return False
