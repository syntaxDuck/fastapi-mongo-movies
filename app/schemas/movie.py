from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl


# Movie schemas
class MovieQuery(BaseModel):
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
    limit: Optional[int] = Field(10, description="Number of movies to return")
    skip: Optional[int] = Field(0, description="Number of records to skip")


class MovieResponse(BaseModel):
    """Response model for movie data."""

    id: str = Field(..., alias="_id")
    plot: str
    genres: list[str]
    runtime: int
    cast: list[str]
    num_mflix_comments: Optional[int] = None
    poster: Optional[HttpUrl] = None
    title: str
    fullplot: Optional[str] = None
    countries: list[str]
    released: Optional[datetime] = None
    directors: list[str]
    writers: Optional[list[str]] = None
    awards: dict
    lastupdated: datetime
    year: int
    imdb: dict
    type: str
    tomatoes: dict

    @classmethod
    def from_dict(cls, data: dict) -> "MovieResponse":
        """Create MovieResponse from dictionary."""
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)


# User schemas
class UserQuery(BaseModel):
    """Query parameters for user endpoints."""

    id: Optional[str] = Field(None, alias="_id", description="Filter by user ID")
    name: Optional[str] = Field(None, description="Filter by user name")
    password: Optional[str] = Field(None, description="Filter by user password")
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
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)


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
