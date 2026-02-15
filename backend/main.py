"""Main application entry point."""

from .api.main import create_app
from .core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

app = create_app()

logger.info("FastAPI backend is ready")

__all__ = ["app"]
