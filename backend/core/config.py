import tomllib
from pathlib import Path

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"

BACKEND_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings configuration."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__VERSION__: str = self.get_version_number
        print("Configuration loaded successfully")

    # Database settings
    DB_HOST: str = Field(default="", description="MongoDB host URL")
    DB_NAME: str = Field(default="", description="MongoDB database name")
    DB_USER: str = Field(default="", description="MongoDB username")
    DB_PASS: str = Field(default="", description="MongoDB password")

    # Application behavior
    DEBUG: bool = Field(default=False, description="Enable debug mode")

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
    MAX_PAGE_SIZE: int = Field(default=100, ge=1, le=1000, description="Maximum page size allowed")

    # MongoDB connection options
    MONGODB_TLS: str = Field(default="true", description="Enable TLS for MongoDB connection")
    MONGODB_TLS_ALLOW_INVALID_CERTS: str = Field(
        default="false", description="Allow invalid TLS certificates"
    )
    MONGODB_CONNECTION_TIMEOUT: int = Field(
        default=10, ge=1, le=30, description="MongoDB connection timeout in seconds"
    )
    MONGODB_MAX_POOL_SIZE: int = Field(
        default=10, ge=1, le=100, description="Maximum MongoDB connection pool size"
    )
    MONGODB_MAX_RETRIES: int = Field(
        default=3, ge=1, le=10, description="Maximum MongoDB connection retry attempts"
    )

    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="detailed", description="Log format style")
    LOG_TO_FILE: bool = Field(default=True, description="Enable file logging")
    LOG_TO_CONSOLE: bool = Field(default=True, description="Enable console logging")
    LOG_FILE_PATH: str = Field(default="logs/app.log", description="Path to application log file")
    ERROR_LOG_FILE_PATH: str = Field(
        default="logs/errors.log", description="Path to error log file"
    )

    # CORS settings
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="Allow credentials in CORS")
    CORS_ORIGINS: list[str] = Field(
        ...,
        description="Allowed CORS origins",
    )
    CORS_ALLOW_METHODS: list[str] = Field(..., description="Allowed CORS methods")
    CORS_ALLOW_HEADERS: list[str] = Field(..., description="Allowed CORS headers")

    # Security settings
    ADMIN_API_KEY: str = Field(..., description="API Key for admin operations")

    # Feature flags
    ENABLE_DOCS: bool = Field(default=True, description="Enable API documentation")

    RESPONSE_COMPRESSION_THRESHOLD: int = Field(
        default=1000, description="Minimum response size fore compression"
    )
    RESPONSE_COMPRESSION_LEVEL: int = Field(
        default=9, description="Compression Level for Responses"
    )

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
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
        return self.DEBUG

    @property
    def cors_config(self) -> dict:
        """Get CORS configuration dictionary."""
        return {
            "allow_origins": self.CORS_ORIGINS,
            "allow_credentials": self.CORS_ALLOW_CREDENTIALS,
            "allow_methods": self.CORS_ALLOW_METHODS,
        }

    @model_validator(mode="after")
    def validate_admin_key(self):
        if not self.is_development and len(self.ADMIN_API_KEY) < 32:
            raise ValueError("ADMIN_API_KEY must be at least 32 characters outside development")

        if self.is_development and len(self.ADMIN_API_KEY) < 4:
            raise ValueError("Dev ADMIN_API_KEY must still be at least 4 characters")

        return self

    @property
    def get_version_number(self):
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)

        return data["project"]["version"]


# Create global settings instance
settings = Settings()
