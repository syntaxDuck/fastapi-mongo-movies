from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator
from bson import ObjectId
from backend.core.logging import get_logger

logger = get_logger(__name__)


class MongoQuery(BaseModel):
    @staticmethod
    def convert_id(query: dict[str, Any]):
        id = None
        if "id" in query:
            id = query.pop("id", None)

        if "_id" in query:
            id = query["_id"]

        if id and not isinstance(id, ObjectId):
            try:
                id = ObjectId(id)
            except Exception as e:
                id = id
                logger.warning(
                    f"Failed to convert movie_id to ObjectId: {id}, error: {e}"
                )

        if id:
            query["_id"] = id

        return query


# Movie schemas
class MovieQuery(MongoQuery, BaseModel):
    """Query parameters for movie endpoints."""

    id: Optional[str] = Field(None, alias="_id", description="Filter by movie ID")
    genres: Optional[list[str]] = Field(None, description="Filter by movie genres")
    runtime: Optional[int] = Field(None, description="Filter by movie runtime")
    cast: Optional[list[str]] = Field(None, description="Filter by movie cast")
    num_mflix_comments: Optional[int] = Field(
        None, description="Filter by number of comments"
    )
    title: Optional[str] = Field(None, description="Filter by movie title")
    countries: Optional[list[str]] = Field(
        None, description="Filter by movie countries"
    )
    released: Optional[datetime] = Field(
        None, description="Filter by movie release date"
    )
    directors: Optional[list[str]] = Field(
        None, description="Filter by movie directors"
    )
    writers: Optional[list[str]] = Field(None, description="Filter by movie writers")
    awards: Optional[dict] = Field(None, description="Filter by movie awards")
    lastupdated: Optional[datetime] = Field(
        None, description="Filter by last updated date"
    )
    year: Optional[int] = Field(None, description="Filter by movie year")
    type: Optional[str] = Field(None, description="Filter by movie type")
    search: Optional[str] = Field(
        None, description="Search movies by text in title, plot, etc."
    )
    include_invalid_posters: Optional[bool] = Field(
        False, description="Include movies with invalid posters"
    )
    sort_by: Optional[str] = Field(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    )
    sort_order: Optional[str] = Field(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    )
    limit: Optional[int] = Field(10, description="Number of movies to return")
    skip: Optional[int] = Field(0, description="Number of records to skip")

    @field_validator("sort_by")
    @classmethod
    def validate_sort_field(cls, v):
        if v is None:
            return v

        allowed_fields = [
            "title",
            "year",
            "released",
            "runtime",
            "num_mflix_comments",
            "lastupdated",
            "imdb.rating",
            "imdb.votes",
            "tomatoes.viewer.rating",
            "tomatoes.critic.rating",
        ]

        if v not in allowed_fields:
            raise ValueError(f"Sort field must be one of: {allowed_fields}")
        return v

    @field_validator("sort_order")
    @classmethod
    def validate_sort_order(cls, v):
        if v is None:
            return "asc"

        if v not in ["asc", "desc"]:
            raise ValueError("Sort order must be 'asc' or 'desc'")
        return v


class MovieResponse(BaseModel):
    """Response model for movie data."""

    id: str = Field(..., alias="_id")
    plot: Optional[str] = None
    genres: Optional[list[str]] = None
    runtime: Optional[int] = None
    cast: Optional[list[str]] = None
    num_mflix_comments: Optional[int] = None
    poster: Optional[HttpUrl] = None
    title: str
    fullplot: Optional[str] = None
    countries: Optional[list[str]] = None
    released: Optional[datetime] = None
    directors: Optional[list[str]] = None
    writers: Optional[list[str]] = None
    awards: Optional[dict] = None
    lastupdated: Optional[datetime] = None
    year: Optional[int] = None
    imdb: Optional[dict] = None
    type: Optional[str] = None
    tomatoes: Optional[dict] = None
    valid_poster: Optional[bool] = None

    @field_validator("year", mode="before")
    @classmethod
    def clean_year(cls, v):
        original_value = v
        if isinstance(v, str):
            logger.debug(
                f"Schemas.clean_year() converting string year: '{original_value}'"
            )
            digits = "".join(filter(str.isdigit, v))
            if digits:
                result = int(digits)
                logger.debug(
                    f"Schemas.clean_year() converted '{original_value}' to {result}"
                )
                return result
            else:
                logger.warning(
                    f"Schemas.clean_year() failed to extract digits from: '{original_value}'"
                )
        elif isinstance(v, int):
            if v < 1800 or v > 2100:
                logger.warning(f"Schemas.clean_year() suspicious year value: {v}")
        return original_value

    @classmethod
    def from_dict(cls, data: dict) -> "MovieResponse":
        """Create MovieResponse from dictionary."""
        logger.debug(
            f"Schemas.MovieResponse.from_dict() called with data keys: {list(data.keys())}"
        )

        original_id = data.get("_id")
        if "_id" in data:
            data["_id"] = str(data["_id"])
            logger.debug(
                f"Schemas.MovieResponse.from_dict() converted _id from {original_id} to {data['_id']}"
            )

        # Validate required fields
        if "title" not in data:
            logger.warning(
                "Schemas.MovieResponse.from_dict() missing required field: title"
            )

        if "year" in data and isinstance(data["year"], str):
            logger.warning(
                f"Schemas.MovieResponse.from_dict() year is string instead of int: {data['year']}"
            )

        try:
            result = cls(**data)
            logger.debug(
                f"Schemas.MovieResponse.from_dict() successfully created MovieResponse for movie: {data.get('title', 'Unknown')}"
            )
            return result
        except Exception as e:
            logger.error(
                f"Schemas.MovieResponse.from_dict() failed to create MovieResponse: {e}"
            )
            raise


# User schemas
class UserQuery(BaseModel):
    """Query parameters for user endpoints."""

    id: Optional[str] = Field(None, alias="_id", description="Filter by user ID")
    name: Optional[str] = Field(None, description="Filter by user name")
    email: Optional[EmailStr] = Field(None, description="Filter by user email")
    limit: Optional[int] = Field(10, description="Number of users to return")
    skip: Optional[int] = Field(0, description="Number of records to skip")


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
    email: Optional[EmailStr] = None

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

        # Validate required fields
        if "name" not in data:
            logger.warning(
                "Schemas.UserResponse.from_dict() missing required field: name"
            )
        if "email" in data:
            email = data["email"]
            # Pydantic EmailStr would handle validation at model creation
            # Log clearly invalid emails for debugging
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


# Comment schemas
class CommentQuery(BaseModel):
    """Query parameters for comment endpoints."""

    id: Optional[str] = Field(None, alias="_id", description="Filter by comment ID")
    name: Optional[str] = Field(None, description="Filter by comment name")
    email: Optional[EmailStr] = Field(None, description="Filter by comment email")
    movie_id: Optional[str] = Field(None, description="Filter by movie ID")
    limit: Optional[int] = Field(10, description="Number of comments to return")
    skip: Optional[int] = Field(0, description="Number of records to skip")


class CommentResponse(BaseModel):
    """Response model for comment data."""

    id: str = Field(..., alias="_id")
    name: str
    email: str
    movie_id: str = Field(..., alias="movie_id")
    text: str
    date: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "CommentResponse":
        """Create CommentResponse from dictionary."""
        if "_id" in data:
            data["_id"] = str(data["_id"])
        if "movie_id" in data:
            data["movie_id"] = str(data["movie_id"])
        return cls(**data)


# Common response schemas
class MessageResponse(BaseModel):
    """Standard message response."""

    message: str


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str
    error_code: Optional[str] = None
