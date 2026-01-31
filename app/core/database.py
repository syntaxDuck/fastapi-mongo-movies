"""
Database connection management using context manager pattern.
"""

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
        self, username: str, password: str, host: str, app_name: str, **kwargs
    ) -> None:
        self._username = username
        self._password = password
        self._host = host
        self._options = kwargs
        self._options["appName"] = app_name

    # mongodb+srv://kamcomer96code:<db_password>@cluster0.hbc7yul.mongodb.net/?appName=Cluster0
    def get_connection_uri(self) -> str:
        """Builds a MongoDB URI based on the provided configuration."""
        encoded_username = quote(str(self._username))
        encoded_password = quote(str(self._password))

        base_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@{self._host}/"
        if self._options:
            query_params = urlencode(self._options)
            base_uri += "?" + query_params

        return base_uri


@asynccontextmanager
async def get_database_client():
    """
    FastAPI dependency context manager for database connections.

    Creates a fresh connection per request and ensures proper cleanup.
    """
    config = DatabaseConfig(
        username=settings.DB_USER,
        password=settings.DB_PASS,
        host=settings.DB_HOST,
        app_name=settings.DB_APP_NAME,
        tls=settings.MONGODB_TLS,
        tlsAllowInvalidCertificates=settings.MONGODB_TLS_ALLOW_INVALID_CERTS,
    )

    client = None
    try:
        logger.debug(f"Creating database connection to {settings.DB_HOST}")
        client = AsyncIOMotorClient(config.get_connection_uri())
        await client.admin.command("ping")
        logger.info("Successfully connected to MongoDB")
        yield client
    except PyMongoError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        raise
    finally:
        if client:
            try:
                client.close()
                logger.debug("Database connection closed")
            except Exception as e:
                logger.warning(f"Warning: Error closing database connection: {e}")
