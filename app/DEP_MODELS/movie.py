from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Movie(BaseModel):
    """Movie model representing database entity."""

    id: str = Field(..., alias="_id")
    plot: str
    genres: list[str]
    runtime: int
    cast: list[str]
    num_mflix_comments: Optional[int] = None
    title: str
    fullplot: Optional[str] = None
    countries: list[str]
    released: datetime
    directors: list[str]
    writers: Optional[list[str]] = None
    awards: Dict[str, Any]
    lastupdated: datetime
    year: int
    imdb: Dict[str, Any]
    type: str
    tomatoes: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Movie":
        """Create Movie instance from dictionary."""
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)


class User(BaseModel):
    """User model representing database entity."""

    id: str = Field(..., alias="_id")
    name: str
    email: Optional[str] = None
    password: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create User instance from dictionary."""
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)


class Comment(BaseModel):
    """Comment model representing database entity."""

    id: str = Field(..., alias="_id")
    name: str
    email: str
    movie_id: str = Field(..., alias="movie_id")
    text: str
    date: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Comment":
        """Create Comment instance from dictionary."""
        if "_id" in data:
            data["_id"] = str(data["_id"])
        if "movie_id" in data:
            data["movie_id"] = str(data["movie_id"])
        return cls(**data)
