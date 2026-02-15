"""
Database connection management using context manager pattern.
"""

import asyncio
import time
from contextlib import asynccontextmanager
from threading import Lock
from typing import Any
from urllib.parse import quote, urlencode

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from .config import settings
from .exceptions import DatabaseError
from .logging import get_logger

logger = get_logger(__name__)


class DatabaseConfig:
    """MongoDB configuration object."""

    def __init__(self, username: str, password: str, host: str, db_name: str, **kwargs) -> None:
        self._username = username
        self._password = password
        self._host = host
        self._db_name = db_name
        self._options = kwargs
        self._options["appName"] = db_name

    def get_connection_uri(self) -> str:
        """Builds a MongoDB URI based on the provided configuration."""
        encoded_username = quote(str(self._username))
        encoded_password = quote(str(self._password))
        base_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@{self._host}/"
        if self._options:
            query_params = urlencode(self._options)
            base_uri += "?" + query_params

        return base_uri


class DatabaseManager:
    """Singleton manager for MongoDB connection pool."""

    _client: AsyncIOMotorClient | None = None
    _lock = Lock()

    def __new__(cls) -> "DatabaseManager":
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        """Get shared MongoDB client with connection pooling."""
        if cls._client is None:
            with cls._lock:
                if cls._client is None:
                    config = DatabaseConfig(
                        username=settings.DB_USER,
                        password=settings.DB_PASS,
                        host=settings.DB_HOST,
                        db_name=settings.DB_NAME,
                        tls=settings.MONGODB_TLS,
                        tlsAllowInvalidCertificates=settings.MONGODB_TLS_ALLOW_INVALID_CERTS,
                    )

                    connection_uri = config.get_connection_uri()
                    cls._client = AsyncIOMotorClient(
                        connection_uri,
                        maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
                        minPoolSize=5,
                        maxIdleTimeMS=30000,
                        connectTimeoutMS=settings.MONGODB_CONNECTION_TIMEOUT * 1000,
                        socketTimeoutMS=30000,
                        serverSelectionTimeoutMS=10000,
                        retryWrites=True,
                        w="majority",
                        readPreference="secondaryPreferred",
                    )

                    logger.info(
                        f"Created pooled MongoDB client with max connections: {settings.MONGODB_MAX_POOL_SIZE}"
                    )

                    retry_attempts = 0
                    max_retries = settings.MONGODB_MAX_RETRIES
                    while retry_attempts < max_retries:
                        try:
                            await cls._client.admin.command("ping")
                            logger.info(
                                f"Successfully connected to MongoDB with connection pooling (attempt {retry_attempts + 1})"
                            )
                            break
                        except Exception as e:
                            retry_attempts += 1
                            logger.warning(
                                f"MongoDB connection attempt {retry_attempts} failed: {e}"
                            )
                            if retry_attempts < max_retries:
                                await asyncio.sleep(
                                    2**retry_attempts
                                )  # Exponential backoff: 2s, 4s, 8s
                                logger.info(
                                    f"Retrying MongoDB connection in {2**retry_attempts} seconds..."
                                )
                            else:
                                logger.error(
                                    f"Failed to connect to MongoDB after {max_retries} attempts: {e}"
                                )
                                raise DatabaseError(
                                    f"Database connection failed after {max_retries} attempts",
                                    details=str(e),
                                ) from None

        return cls._client

    @classmethod
    async def get_pool_status(cls) -> dict[str, Any]:
        """Get connection pool status for monitoring."""
        logger.debug("DatabaseManager.get_pool_status() called")

        if cls._client is None:
            logger.warning("DatabaseManager.get_pool_status() client not initialized")
            return {"status": "not_initialized"}

        try:
            admin = cls._client.admin
            server_status = await admin.command("serverStatus")
            connections = server_status.get("connections", {})

            pool_status = {
                "status": "healthy",
                "connections": connections,
                "pool": {"max_size": settings.MONGODB_MAX_POOL_SIZE, "min_size": 5},
            }

            current_connections = connections.get("current", 0)
            available_connections = connections.get("available", 0)
            total_created = connections.get("totalCreated", 0)

            logger.debug(
                f"Database pool status - Current: {current_connections}, Available: {available_connections}, Total Created: {total_created}"
            )

            if current_connections > settings.MONGODB_MAX_POOL_SIZE * 0.8:
                logger.warning(
                    f"Database pool nearing capacity: {current_connections}/{settings.MONGODB_MAX_POOL_SIZE}"
                )

            if available_connections < 5:
                logger.warning(
                    f"Database pool low on available connections: {available_connections}"
                )

            logger.info("DatabaseManager.get_pool_status() returning healthy status")
            return pool_status

        except Exception as e:
            logger.error(f"DatabaseManager.get_pool_status() failed: {e}")
            return {"status": "error", "error": str(e)}

    @classmethod
    async def close_all_connections(cls):
        """Close all database connections (for shutdown)."""
        if cls._client:
            cls._client.close()
            cls._client = None
            logger.info("All database connections closed")


@asynccontextmanager
async def get_database_client():
    """
    FastAPI dependency context manager for database connections.

    Uses shared pooled client for optimal performance.
    """

    start_time = None
    try:
        start_time = time.time()
        client = await DatabaseManager.get_client()
        logger.debug("get_database_client() getting database client from pool")
        yield client
    except PyMongoError as e:
        logger.error(f"get_database_client() failed to get database client: {e}")
        raise
    except DatabaseError as e:
        logger.error(f"get_database_client() unexpected error getting database client: {e}")
        raise
    finally:
        if start_time:
            duration = time.time() - start_time
            logger.debug(f"get_database_client() database operation completed in {duration:.3f}s")
