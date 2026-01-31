from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings configuration."""

    # Database settings
    DB_HOST: str = Field(default="", description="MongoDB host URL")
    DB_APP_NAME: str = Field(default="", description="MongoDB database name")
    DB_USER: str = Field(default="", description="MongoDB username")
    DB_PASS: str = Field(default="", description="MongoDB password")

    # Application settings
    API_URL: str = Field(
        default="http://localhost:8000", description="Base URL for API"
    )
    FRONTEND_URL: str = Field(
        default="http://localhost:3000", description="Base URL for frontend"
    )

    # Server settings
    API_HOST: str = Field(default="0.0.0.0", description="Host to bind the API server")
    API_PORT: int = Field(default=8000, description="Port for the API server")
    FRONTEND_HOST: str = Field(
        default="0.0.0.0", description="Host to bind the frontend server"
    )
    FRONTEND_PORT: int = Field(default=3000, description="Port for the frontend server")

    # Application behavior
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    RELOAD: bool = Field(
        default=True, description="Enable auto-reload during development"
    )

    # Pagination settings
    MOVIE_LIST_PAGE_SIZE: int = Field(
        default=10, ge=1, le=100, description="Number of movies per page"
    )
    COMMENT_PAGE_SIZE: int = Field(
        default=10, ge=1, le=100, description="Number of comments per page"
    )
    MAX_PAGE_SIZE: int = Field(
        default=100, ge=1, le=1000, description="Maximum page size allowed"
    )

    # MongoDB connection options
    MONGODB_TLS: str = Field(
        default="true", description="Enable TLS for MongoDB connection"
    )
    MONGODB_TLS_ALLOW_INVALID_CERTS: str = Field(
        default="true", description="Allow invalid TLS certificates"
    )
    MONGODB_CONNECTION_TIMEOUT: int = Field(
        default=30, ge=1, le=300, description="MongoDB connection timeout in seconds"
    )
    MONGODB_MAX_POOL_SIZE: int = Field(
        default=10, ge=1, le=100, description="Maximum MongoDB connection pool size"
    )

    # Security settings
    SECRET_KEY: Optional[str] = Field(
        default=None, description="Secret key for JWT tokens"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, ge=1, le=1440, description="Access token expiration in minutes"
    )

    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="detailed", description="Log format style")
    LOG_TO_FILE: bool = Field(default=True, description="Enable file logging")
    LOG_TO_CONSOLE: bool = Field(default=True, description="Enable console logging")
    LOG_FILE_PATH: str = Field(
        default="logs/app.log", description="Path to application log file"
    )
    ERROR_LOG_FILE_PATH: str = Field(
        default="logs/errors.log", description="Path to error log file"
    )

    # CORS settings
    CORS_ORIGINS: list[str] = Field(
        default=[
            "http://localhost:8080",
            "http://localhost:8000",
            "http://localhost:3000",
        ],
        description="Allowed CORS origins",
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True, description="Allow credentials in CORS"
    )
    CORS_ALLOW_METHODS: list[str] = Field(
        default=["GET", "POST", "PUT", "DELETE"], description="Allowed CORS methods"
    )

    # Performance settings
    ENABLE_CACHING: bool = Field(default=False, description="Enable response caching")
    CACHE_TTL: int = Field(
        default=300, ge=1, le=3600, description="Cache time-to-live in seconds"
    )

    # Feature flags
    ENABLE_METRICS: bool = Field(
        default=False, description="Enable application metrics"
    )
    ENABLE_DOCS: bool = Field(default=True, description="Enable API documentation")
    RATE_LIMITING: bool = Field(default=False, description="Enable rate limiting")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="",
    )

    @property
    def database_url(self) -> str:
        """Construct MongoDB connection URL."""
        return (
            f"mongodb+srv://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}"
            f"/{self.DB_APP_NAME}?tls={self.MONGODB_TLS}"
            f"&tlsAllowInvalidCertificates={self.MONGODB_TLS_ALLOW_INVALID_CERTS}"
        )

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.DEBUG or self.RELOAD

    @property
    def cors_config(self) -> dict:
        """Get CORS configuration dictionary."""
        return {
            "allow_origins": self.CORS_ORIGINS,
            "allow_credentials": self.CORS_ALLOW_CREDENTIALS,
            "allow_methods": self.CORS_ALLOW_METHODS,
        }


# Create global settings instance
settings = Settings()
