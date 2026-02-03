"""
Database connection management using context manager pattern.
"""

from typing import Optional, Dict, Any
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote, urlencode
from contextlib import asynccontextmanager
from .config import settings
from .logging import get_logger

logger = get_logger(__name__)


class DatabaseConfig:
    """MongoDB configuration object."""

    def __init__(
        self, username: str, password: str, host: str, db_name: str, **kwargs
    ) -> None:
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


# Singleton pattern for shared pooled client
class DatabaseManager:
    """Singleton manager for MongoDB connection pool."""

    _client: Optional[AsyncIOMotorClient] = None

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        """Get shared MongoDB client with connection pooling."""
        if cls._client is None:
            config = DatabaseConfig(
                username=settings.DB_USER,
                password=settings.DB_PASS,
                host=settings.DB_HOST,
                db_name=settings.DB_NAME,
                tls=settings.MONGODB_TLS,
                tlsAllowInvalidCertificates=settings.MONGODB_TLS_ALLOW_INVALID_CERTS,
            )

            # Create client with connection pooling
            connection_uri = config.get_connection_uri()
            cls._client = AsyncIOMotorClient(
                connection_uri,
                # Connection Pool Settings
                maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,  # Max connections in pool
                minPoolSize=5,  # Always keep 5 connections ready
                maxIdleTimeMS=30000,  # Close idle connections after 30s
                connectTimeoutMS=settings.MONGODB_CONNECTION_TIMEOUT
                * 1000,  # 30s timeout
                socketTimeoutMS=30000,  # 30s socket timeout
                serverSelectionTimeoutMS=10000,  # 10s to find server
                retryWrites=True,  # Retry failed writes
                w="majority",  # Write concern
                readPreference="secondaryPreferred",  # Read from secondary when possible
            )

            logger.info(
                f"Created pooled MongoDB client with max connections: {settings.MONGODB_MAX_POOL_SIZE}"
            )

            # Test connection
            await cls._client.admin.command("ping")
            logger.info("Successfully connected to MongoDB with connection pooling")

        return cls._client

    @classmethod
    async def get_pool_status(cls) -> Dict[str, Any]:
        """Get connection pool status for monitoring."""
        if cls._client is None:
            return {"status": "not_initialized"}

        try:
            admin = cls._client.admin
            server_status = await admin.command("serverStatus")
            return {
                "status": "healthy",
                "connections": server_status.get("connections", {}),
                "pool": {"max_size": settings.MONGODB_MAX_POOL_SIZE, "min_size": 5},
            }
        except Exception as e:
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
    try:
        client = await DatabaseManager.get_client()
        logger.debug("Getting database client from pool")
        yield client
    except PyMongoError as e:
        logger.error(f"Failed to get database client: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting database client: {e}")
        raise
