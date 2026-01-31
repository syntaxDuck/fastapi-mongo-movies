from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.movies import router as movies_router
from .routes.users import router as users_router
from .routes.comments import router as comments_router
from ..core.config import settings
from ..core.middleware import log_requests
from ..core.logging import setup_logging, get_logger

# Initialize logging
setup_logging()
logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    logger.info("Creating FastAPI application")

    app = FastAPI(
        title="FastAPI MongoDB Movies",
        description="A modular FastAPI application with MongoDB for movie data management",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add request logging middleware
    app.middleware("http")(log_requests)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=["*"],
    )

    # Include routers
    logger.info("Including API routers")
    app.include_router(movies_router)
    app.include_router(users_router)
    app.include_router(comments_router)

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        logger.debug("Health check requested")
        return {
            "status": "healthy",
            "service": "FastAPI MongoDB Movies",
            "version": "0.1.0",
        }

    logger.info("FastAPI application created successfully")
    return app
