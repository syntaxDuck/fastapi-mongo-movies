from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings configuration."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Basic config validation - use print to avoid circular import
        print("Configuration loaded successfully")
        if not self.DB_HOST:
            print("WARNING: DB_HOST not configured")
        if not self.DB_NAME:
            print("WARNING: DB_NAME not configured")
        if not self.DB_USER:
            print("WARNING: DB_USER not configured")

    # Database settings
    DB_HOST: str = Field(default="", description="MongoDB host URL")
    DB_NAME: str = Field(default="", description="MongoDB database name")
    DB_USER: str = Field(default="", description="MongoDB username")
    DB_PASS: str = Field(default="", description="MongoDB password")

    # Frontend settings
    FRONTEND_URL: str = Field(
        default="http://localhost:3000", description="Base URL for frontend"
    )
    FRONTEND_HOST: str = Field(
        default="0.0.0.0", description="Host to bind the frontend server"
    )
    FRONTEND_PORT: int = Field(default=3000, description="Port for the frontend server")

    # API settings
    API_URL: str = Field(
        default="http://localhost:8000", description="Base URL for API"
    )
    API_HOST: str = Field(default="0.0.0.0", description="Host to bind the API server")
    API_PORT: int = Field(default=8000, description="Port for the API server")

    # Application behavior
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    RELOAD: bool = Field(
        default=True, description="Enable auto-reload during development"
    )

    # Pagination settings
    DEFAULT_LIST_PAGE_SIZE: int = Field(
        default=10, ge=1, le=100, description="Number of movies per page"
    )
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
        default="false", description="Allow invalid TLS certificates"
    )
    MONGODB_CONNECTION_TIMEOUT: int = Field(
        default=10, ge=1, le=30, description="MongoDB connection timeout in seconds"
    )
    MONGODB_MAX_POOL_SIZE: int = Field(
        default=10, ge=1, le=100, description="Maximum MongoDB connection pool size"
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
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True, description="Allow credentials in CORS"
    )
    CORS_ORIGINS: list[str] = Field(
        default=["*"],
        description="Allowed CORS origins",
    )
    CORS_ALLOW_METHODS: list[str] = Field(
        default=["*"], description="Allowed CORS methods"
    )
    CORS_ALLOW_HEADERS: list[str] = Field(
        default=["*"], description="Allowed CORS headers"
    )

    # Security settings
    ADMIN_API_KEY: str = Field(
        default="dev-admin-key", description="API Key for admin operations"
    )

    # Feature flags
    ENABLE_DOCS: bool = Field(default=True, description="Enable API documentation")

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
            f"mongodb+srv://{self.DB_USER}:*****@{self.DB_HOST}"
            f"/{self.DB_NAME}?tls={self.MONGODB_TLS}"
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
