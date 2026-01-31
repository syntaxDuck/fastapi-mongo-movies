class AppException(Exception):
    """Base exception for the application."""

    pass


class DatabaseError(AppException):
    """Raised when database operations fail."""

    pass


class NotFoundError(AppException):
    """Raised when a resource is not found."""

    pass


class ValidationError(AppException):
    """Raised when validation fails."""

    pass


class DuplicateResourceError(AppException):
    """Raised when trying to create a duplicate resource."""

    pass
