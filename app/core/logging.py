"""
Logging configuration for the application.
"""

import logging
import sys
from pathlib import Path
from .config import settings


def setup_logging() -> None:
    """Set up application logging configuration."""

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure logging format
    if settings.LOG_FORMAT == "simple":
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
    else:  # detailed
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

    # Create handlers
    handlers = []

    # Console handler
    if settings.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(console_handler)

    # File handlers
    if settings.LOG_TO_FILE:
        # Application log file handler
        app_handler = logging.FileHandler(
            filename=log_dir / "app.log", mode="a", encoding="utf-8"
        )
        app_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(app_handler)

        # Error log file handler
        error_handler = logging.FileHandler(
            filename=log_dir / "errors.log", mode="a", encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(error_handler)

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
        force=True,
    )

    # Set specific logger levels for different components
    configure_component_loggers()

    logging.info("Application logging initialized")


def configure_component_loggers() -> None:
    """Configure logging levels for different application components."""

    # Database operations - debug level for detailed queries
    logging.getLogger("app.core.database").setLevel(settings.LOG_LEVEL)

    # Repository operations - info level
    logging.getLogger("app.repositories").setLevel(settings.LOG_LEVEL)

    # Service layer - info level
    logging.getLogger("app.services").setLevel(settings.LOG_LEVEL)

    # API routes - info level
    logging.getLogger("app.api").setLevel(settings.LOG_LEVEL)

    logging.getLogger("app.schemas").setLevel(logging.WARNING)

    # HTTP requests - warning level (less noisy)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    # Suppress noisy third-party loggers
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific component."""
    return logging.getLogger(name)
