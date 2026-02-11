from typing import Optional, Any
from .logging import get_logger

logger = get_logger(__name__)


class AppException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.details = details
        logger.error(f"AppException: {message}. Details: {details or 'None'}")


class DatabaseError(AppException):
    """Raised when database operations fail."""

    def __init__(
        self,
        message: str,
        details: Optional[str] = None,
        operation: Optional[str] = None,
    ):
        super().__init__(message, details)
        self.operation = operation
        logger.error(
            f"DatabaseError: {message}. Operation: {operation or 'None'}. Details: {details or 'None'}"
        )


class NotFoundError(AppException):
    """Raised when a resource is not found."""

    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
    ):
        super().__init__(message)
        self.resource_type = resource_type
        self.resource_id = resource_id
        logger.warning(
            f"NotFoundError: {message}. Type: {resource_type or 'None'}, ID: {resource_id or 'None'}"
        )


class ValidationError(AppException):
    """Raised when validation fails."""

    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        super().__init__(message)
        self.field = field
        self.value = value
        logger.warning(
            f"ValidationError: {message}. Field: {field or 'None'}, Value: {value}"
        )


class DuplicateResourceError(AppException):
    """Raised when trying to create a duplicate resource."""

    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        identifier: Optional[str] = None,
    ):
        super().__init__(message)
        self.resource_type = resource_type
        self.identifier = identifier
        logger.warning(
            f"DuplicateResourceError: {message}. Type: {resource_type or 'None'}, Identifier: {identifier or 'None'}"
        )
