"""Main application entry point."""

from .api.main import create_app
from .core.logging import setup_logging, get_logger

# Initialize logging before creating the app
setup_logging()
logger = get_logger(__name__)

# Create FastAPI application instance
app = create_app()

logger.info("FastAPI MongoDB Movies application ready")

# For compatibility with existing imports
__all__ = ["app"]
