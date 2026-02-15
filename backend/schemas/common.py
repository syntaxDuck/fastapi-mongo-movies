
from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Standard message response."""

    message: str


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str
    error_code: str | None = None
