"""
Rate limiting configuration and utilities.
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException
from typing import Any, Callable


def get_real_ip(request: Request) -> str:
    """
    Get the real client IP address, handling proxies properly.

    Checks X-Forwarded-For header first (for hosted frontends like Render),
    then falls back to the direct client IP.
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    if request.client:
        return request.client.host

    return "unknown"


def rate_limit_key(request: Request) -> str:
    """
    Custom rate limit key function that properly handles proxied requests.

    Uses X-Forwarded-For for hosted frontends to get the real client IP.
    """
    return get_real_ip(request)


limiter = Limiter(
    key_func=rate_limit_key,
    default_limits=["100 per minute"],
    strategy="fixed-window",
)


async def rate_limit_exceeded_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Custom handler for rate limit exceeded errors.

    Returns a JSON error response instead of the default SlowAPI response.
    """
    if isinstance(exc, RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "detail": str(exc.detail),
                "retry_after": exc.detail,
            },
        )
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )


class RateLimitConfig:
    """Rate limit configuration with environment variable support."""

    def __init__(
        self,
        general: str = "100 per minute",
        search: str = "30 per minute",
        comments: str = "60 per minute",
        users: str = "30 per minute",
    ):
        self.general = general
        self.search = search
        self.comments = comments
        self.users = users

    @classmethod
    def from_settings(cls, settings) -> "RateLimitConfig":
        """Create config from settings object with defaults."""
        return cls(
            general=getattr(settings, "RATE_LIMIT_GENERAL", "100 per minute"),
            search=getattr(settings, "RATE_LIMIT_SEARCH", "30 per minute"),
            comments=getattr(settings, "RATE_LIMIT_COMMENTS", "60 per minute"),
            users=getattr(settings, "RATE_LIMIT_USERS", "30 per minute"),
        )


def get_rate_limit_config() -> RateLimitConfig:
    """Get rate limit configuration instance."""
    return RateLimitConfig()
