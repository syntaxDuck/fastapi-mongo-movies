from datetime import datetime
from typing import Optional

from bson import ObjectId
from fastapi import Query
from pydantic import BaseModel, EmailStr, Field, HttpUrl, ValidationError


class UserQuery(BaseModel):
    id: str = Query(None, alias="_id",description="Filter by user ID")
    name: str = Query(None, description="Filter by user name")
    password: str = Query(None, description="Filter by user password")
    email: EmailStr = Query(None, description="Filter by user email")
    limit: int = Query(10, description="Number of users to return")
    skip: int = Query(0, description="Number of records to skip")


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

class CommentQuery(BaseModel):
    id: Optional[str] = Query(None, alias="_id", description="Filter by comment ID")
    name: Optional[str] = Query(None, description="Filter by comment name")
    email: Optional[EmailStr] = Query(None, description="Filter by comment email")
    movie_id: Optional[str] = Query(None, alias="movie_id", description="Filter by movie ID")
    limit: Optional[int] = Query(10, description="Number of comments to return")
    skip: Optional[int] = Query(0, description="Number of records to skip")

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


class MovieQuery(BaseModel):
    id: Optional[str] = Query(None, alias="_id", description="Filter by movie ID")
    genres: Optional[list[str]] = Query(None, description="Filter by movie genres")
    runtime: Optional[int] = Query(None, description="Filter by movie runtime")
    cast: Optional[list[str]] = Query(None, description="Filter by movie cast")
    num_mflix_comments: Optional[int] = Query(None, description="Filter by number of comments")
    title: Optional[str] = Query(None, description="Filter by movie title")
    countries: Optional[list[str]] = Query(None, description="Filter by movie countries")
    released: Optional[datetime] = Query(None, description="Filter by movie release date")
    directors: Optional[list[str]] = Query(None, description="Filter by movie directors")
    writers: Optional[list[str]] = Query(None, description="Filter by movie writers")
    awards: Optional[dict] = Query(None, description="Filter by movie awards")
    lastupdated: Optional[datetime] = Query(None, description="Filter by last updated date")
    year: Optional[int] = Query(None, description="Filter by movie year")
    type: Optional[str] = Query(None, description="Filter by movie type (e.g., 'movie', 'series')")
    limit: Optional[int] = Query(10, description="Number of movies to return")
    skip: Optional[int] = Query(0, description="Number of records to skip")

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
