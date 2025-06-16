from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class User(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    password: str
    email: Optional[EmailStr] = None

    @classmethod
    def from_mongo(cls, data: dict) -> "User":
        """Convert MongoDB dict to Pydantic model."""
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)


class Comment(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: str
    movie_id: str = Field(..., alias="movie_id")
    text: str
    date: datetime

    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @classmethod
    def from_mongo(cls, data: dict) -> "Comment":
        """Convert MongoDB dict to Pydantic model."""
        if "_id" in data:
            data["_id"] = str(data["_id"])

        if "movie_id" in data:
            data["movie_id"] = str(data["movie_id"])
        return cls(**data)


class Movie(BaseModel):
    id: str = Field(..., alias="_id")
    plot: str = None
    genres: list[str] = None
    runtime: int = None
    cast: list[str] = None
    num_mflix_comments: Optional[int] = None
    poster: Optional[HttpUrl] = None
    title: str = None
    fullplot: str = None
    countries: list[str] = None
    released: datetime = None
    directors: list[str] = None
    writers: list[str] = None
    awards: dict = None
    lastupdated: datetime
    year: int = None
    imdb: dict = None
    type: str = None
    tomatoes: dict = None

    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @classmethod
    def from_mongo(cls, data: dict) -> "Movie":
        """Convert MongoDB dict to Pydantic model."""
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)
