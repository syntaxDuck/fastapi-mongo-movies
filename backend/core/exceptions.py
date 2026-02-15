from typing import Any

from .logging import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Base exception for the application."""

    def __init__(self, message: str, details: str | None = None):
        super().__init__(message)
        self.message = message
        self.details = details
        logger.error(f"AppError: {message}. Details: {details or 'None'}")


class DatabaseError(AppError):
    """Raised when database operations fail."""

    def __init__(
        self,
        message: str,
        details: str | None = None,
        operation: str | None = None,
    ):
        super().__init__(message, details)
        self.operation = operation
        logger.error(
            f"DatabaseError: {message}. Operation: {operation or 'None'}. Details: {details or 'None'}"
        )


class NotFoundError(AppError):
    """Raised when a resource is not found."""

    def __init__(
        self,
        message: str,
        resource_type: str | None = None,
        resource_id: str | None = None,
    ):
        super().__init__(message)
        self.resource_type = resource_type
        self.resource_id = resource_id
        logger.warning(
            f"NotFoundError: {message}. Type: {resource_type or 'None'}, ID: {resource_id or 'None'}"
        )


class ValidationError(AppError):
    """Raised when validation fails."""

    def __init__(self, message: str, field: str | None = None, value: Any = None):
        super().__init__(message)
        self.field = field
        self.value = value
        logger.warning(f"ValidationError: {message}. Field: {field or 'None'}, Value: {value}")


class DuplicateResourceError(AppError):
    """Raised when trying to create a duplicate resource."""

    def __init__(
        self,
        message: str,
        resource_type: str | None = None,
        identifier: str | None = None,
    ):
        super().__init__(message)
        self.resource_type = resource_type
        self.identifier = identifier
        logger.warning(
            f"DuplicateResourceError: {message}. Type: {resource_type or 'None'}, Identifier: {identifier or 'None'}"
        )
