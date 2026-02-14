from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from ..core.config import settings
from ..core.database import DatabaseManager
from ..core.exceptions import (
    DatabaseError,
    DuplicateResourceError,
    NotFoundError,
    ValidationError,
)
from ..core.logging import get_logger, setup_logging
from ..core.middleware import handle_requests
from ..core.rate_limiter import limiter
from .routes.admin import router as admin_router
from .routes.comments import router as comments_router
from .routes.movies import router as movies_router
from .routes.users import router as users_router

setup_logging()
logger = get_logger(__name__)


async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def duplicate_handler(_: Request, exc: DuplicateResourceError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


async def validation_handler(_: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


async def database_error_handler(_: Request, exc: DatabaseError) -> JSONResponse:
    logger.error(f"Database error: {exc.message}")
    return JSONResponse(
        status_code=500, content={"detail": "Database operation failed"}
    )


async def rate_limit_exceeded_handler(
    _: Request, exc: RateLimitExceeded
) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": str(exc.detail),
            "retry_after": exc.detail,
        },
    )


async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unhandled exception {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@asynccontextmanager
async def lifespan(_: FastAPI):
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
        version=settings.__VERSION__,
        docs_url="/docs" if settings.ENABLE_DOCS else None,
        redoc_url="/redoc" if settings.ENABLE_DOCS else None,
        lifespan=lifespan,
    )

    app.state.limiter = limiter

    # Exception handlers with customer exception types make the linter sad
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)  # type: ignore[arg-type]
    app.add_exception_handler(NotFoundError, not_found_handler)  # type: ignore[arg-type]
    app.add_exception_handler(DuplicateResourceError, duplicate_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ValidationError, validation_handler)  # type: ignore[arg-type]
    app.add_exception_handler(DatabaseError, database_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, generic_exception_handler)

    app.middleware("http")(handle_requests)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=settings.RESPONSE_COMPRESSION_THRESHOLD,
        compresslevel=settings.RESPONSE_COMPRESSION_LEVEL,
    )

    logger.info("Including API routers")
    app.include_router(movies_router)
    app.include_router(users_router)
    app.include_router(comments_router)
    app.include_router(admin_router)

    logger.info("FastAPI application created successfully")
    return app
