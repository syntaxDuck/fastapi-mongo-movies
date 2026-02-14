"""
Logging configuration for the application.
"""

import logging
import sys
from pathlib import Path
from .config import settings


def setup_logging() -> None:
    """Set up application logging configuration."""

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    if settings.LOG_FORMAT == "simple":
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
    else:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

    handlers = []

    if settings.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(console_handler)

    if settings.LOG_TO_FILE:
        app_handler = logging.FileHandler(
            filename=log_dir / "app.log", mode="a", encoding="utf-8"
        )
        app_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(app_handler)

        error_handler = logging.FileHandler(
            filename=log_dir / "errors.log", mode="a", encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(log_format, date_format))
        handlers.append(error_handler)

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
        force=True,
    )

    configure_component_loggers()

    logging.info("Application logging initialized")


def configure_component_loggers() -> None:
    """Configure logging levels for different application components."""

    logging.getLogger("backend.core.database").setLevel(settings.LOG_LEVEL)
    logging.getLogger("backend.repositories").setLevel(settings.LOG_LEVEL)
    logging.getLogger("backend.services").setLevel(settings.LOG_LEVEL)
    logging.getLogger("backend.api").setLevel(settings.LOG_LEVEL)

    logging.getLogger("backend.schemas").setLevel(logging.WARNING)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific component."""
    return logging.getLogger(name)
