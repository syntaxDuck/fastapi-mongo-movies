
from pydantic import BaseModel, EmailStr, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class UserQuery(BaseModel):
    """Query parameters for user endpoints."""

    id: str | None = Field(None, alias="_id", description="Filter by user ID")
    name: str | None = Field(None, description="Filter by user name")
    email: EmailStr | None = Field(None, description="Filter by user email")
    limit: int | None = Field(None, description="Number of users to return")
    skip: int | None = Field(0, description="Number of records to skip")


class UserCreate(BaseModel):
    """Request model for creating a user."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., min_length=6, max_length=100, description="User password"
    )


class UserResponse(BaseModel):
    """Response model for user data."""

    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "UserResponse":
        """Create UserResponse from dictionary."""
        logger.debug(
            f"Schemas.UserResponse.from_dict() called with data keys: {list(data.keys())}"
        )

        original_id = data.get("_id")
        if "_id" in data:
            data["_id"] = str(data["_id"])
            logger.debug(
                f"Schemas.UserResponse.from_dict() converted _id from {original_id} to {data['_id']}"
            )

        if "name" not in data:
            logger.warning(
                "Schemas.UserResponse.from_dict() missing required field: name"
            )
        if "email" in data:
            email = data["email"]
            if email and (" " in email or not email.count("@") or not email.count(".")):
                logger.warning(
                    f"Schemas.UserResponse.from_dict() clearly invalid email format: {email}"
                )

        try:
            result = cls(**data)
            logger.debug(
                f"Schemas.UserResponse.from_dict() successfully created UserResponse for user: {data.get('name', 'Unknown')}"
            )
            return result
        except Exception as e:
            logger.error(
                f"Schemas.UserResponse.from_dict() failed to create UserResponse: {e}"
            )
            raise
