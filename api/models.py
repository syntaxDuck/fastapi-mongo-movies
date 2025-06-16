from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, HttpUrl, ValidationError


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
    plot: str
    genres: list[str]
    runtime: int
    cast: list[str]
    num_mflix_comments: Optional[int] = None
    poster: Optional[HttpUrl] = None
    title: str
    fullplot: Optional[str] = None
    countries: list[str]
    released: datetime
    directors: list[str]
    writers: Optional[list[str]] = None
    awards: dict
    lastupdated: datetime
    year: int
    imdb: dict
    type: str
    tomatoes: dict

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
        try:
            return cls(**data)
        except ValidationError:
            return None
