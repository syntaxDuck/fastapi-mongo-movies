from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


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
