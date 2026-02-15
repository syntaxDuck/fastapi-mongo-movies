import hashlib
import secrets

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from .config import settings

admin_api_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)


async def verify_admin_api_key(api_key: str = Security(admin_api_key_header)):
    """
    Verify the admin API key provided in the request header.
    """
    #QUES: Probably could use error handlers here
    if not api_key:
        raise HTTPException(status_code=404, detail="Not Found")

    if not secrets.compare_digest(api_key, settings.ADMIN_API_KEY):
        raise HTTPException(status_code=404, detail="Not Found")

    return api_key


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
        100000,  # Number of iterations
    )
    return f"{salt}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    try:
        salt, stored_hash = hashed_password.split("$")
        key = hashlib.pbkdf2_hmac(
            "sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return key.hex() == stored_hash
    except (ValueError, AttributeError):
        return False
