from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .routes.movies import router as movies_router
from .routes.users import router as users_router
from .routes.comments import router as comments_router
from .routes.admin import router as admin_router
from ..core.config import settings
from ..core.middleware import log_requests
from ..core.logging import setup_logging, get_logger
from ..core.database import DatabaseManager

# Initialize logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for connection pool cleanup."""
    logger.info("Application starting up...")
    await DatabaseManager.get_client()
    yield
    logger.info("Application shutting down...")
    await DatabaseManager.close_all_connections()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    logger.info("Creating FastAPI application")

    app = FastAPI(
        title="FastAPI MongoDB Movies",
        description="A modular FastAPI application with MongoDB for movie data management",
        version="0.1.0",
        docs_url="/docs" if settings.ENABLE_DOCS else None,
        redoc_url="/redoc" if settings.ENABLE_DOCS else None,
        lifespan=lifespan,
    )

    app.middleware("http")(log_requests)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    app.add_middleware(GZipMiddleware, minimum_size=1000)

    logger.info("Including API routers")
    app.include_router(movies_router)
    app.include_router(users_router)
    app.include_router(comments_router)
    app.include_router(admin_router)

    @app.get("/health")
    async def health_check():
        logger.debug("Health check requested")
        pool_status = await DatabaseManager.get_pool_status()
        return {
            "status": "healthy",
            "service": "FastAPI MongoDB Movies",
            "version": "0.1.0",
            "database_pool": pool_status,
        }

    logger.info("FastAPI application created successfully")
    return app
