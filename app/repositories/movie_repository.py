"""
Repository layer using context manager pattern.
"""

from typing import Dict, Any, List, Optional
from bson import ObjectId
from .base import BaseRepository
from app.core.logging import get_logger

logger = get_logger(__name__)


class MovieRepository(BaseRepository):
    """Repository for movie data operations."""

    def __init__(self) -> None:
        super().__init__("sample_mflix", "movies")

    async def find_by_id(
        self, entity_id: str, id_field: str = "_id", **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Find a movie by its ID."""
        return await super().find_by_id(entity_id, id_field, **kwargs)

    async def find_by_title(self, title: str, **kwargs) -> List[Dict[str, Any]]:
        """Find movies by title (exact match)."""
        filter_query = {"title": title}
        return await self.find_many(filter_query, **kwargs)

    async def find_by_type(self, movie_type: str, **kwargs) -> List[Dict[str, Any]]:
        """Find movies by type (e.g., 'movie', 'series')."""
        filter_query = {"type": movie_type}
        return await self.find_many(filter_query, **kwargs)

    async def find_by_genre(
        self, genre: str, limit: int = 10, skip: int = 0, **kwargs
    ) -> List[Dict[str, Any]]:
        """Find movies by genre."""
        filter_query = {"genres": {"$in": [genre]}}
        return await self.find_many(filter_query, limit, skip, **kwargs)

    async def find_by_year(
        self, year: int, limit: int = 10, skip: int = 0, **kwargs
    ) -> List[Dict[str, Any]]:
        """Find movies by release year."""
        filter_query = {"year": year}
        return await self.find_many(filter_query, limit, skip, **kwargs)

    async def search_movies(self, **kwargs) -> List[Dict[str, Any]]:
        """Search movies with multiple filters."""
        filter_query = {}

        if kwargs.get("movie_id", None):
            try:
                filter_query["_id"] = ObjectId(kwargs["movie_id"])
            except Exception:
                pass

        if kwargs.get("title", None):
            filter_query["title"] = kwargs["title"]

        if kwargs.get("movie_type", None):
            filter_query["type"] = kwargs["movie_type"]

        if kwargs.get("genres", None):
            filter_query["genres"] = {"$in": kwargs["genres"]}

        if kwargs.get("year", None):
            filter_query["year"] = kwargs["year"]

        limit = kwargs.get("limit", 10)
        skip = kwargs.get("skip", 0)
        logger.info(filter_query)
        return await self.find_many(filter_query, limit, skip)


class UserRepository(BaseRepository):
    """Repository for user data operations."""

    def __init__(self) -> None:
        super().__init__("sample_mflix", "users")

    async def find_by_id(
        self, entity_id: str, id_field: str = "_id"
    ) -> Optional[Dict[str, Any]]:
        """Find a user by their ID."""
        return await super().find_by_id(entity_id, id_field)

    async def find_by_email(self, email: str, **kwargs) -> List[Dict[str, Any]]:
        """Find users by email."""
        filter_query = {"email": email}
        return await self.find_many(filter_query, **kwargs)

    async def find_by_name(self, name: str, **kwargs) -> List[Dict[str, Any]]:
        """Find users by name."""
        filter_query = {"name": name}
        return await self.find_many(filter_query, **kwargs)

    async def email_exists(self, email: str) -> bool:
        """Check if a user with given email exists."""
        users = await self.find_by_email(email)
        return len(users) > 0

    async def search_users(self, **kwargs) -> List[Dict[str, Any]]:
        """Search users with multiple filters."""
        filter_query = {}

        if "user_id" in kwargs:
            try:
                filter_query["_id"] = ObjectId(kwargs["user_id"])
            except Exception:
                pass

        if "name" in kwargs:
            filter_query["name"] = kwargs["name"]

        if "email" in kwargs:
            filter_query["email"] = kwargs["email"]

        return await self.find_many(filter_query, **kwargs)


class CommentRepository(BaseRepository):
    """Repository for comment data operations."""

    def __init__(self) -> None:
        super().__init__("sample_mflix", "comments")

    async def find_by_id(
        self, entity_id: str, id_field: str = "_id", **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Find a comment by its ID."""
        return await super().find_by_id(entity_id, id_field, **kwargs)

    async def find_by_movie_id(
        self, movie_id: str, limit: int = 10, skip: int = 0, **kwargs
    ) -> List[Dict[str, Any]]:
        """Find comments by movie ID."""
        limit = kwargs.get("limit", 10)
        skip = kwargs.get("skip", 0)
        try:
            filter_query = {"movie_id": ObjectId(movie_id)}
        except Exception:
            return []

        return await self.find_many(filter_query, limit, skip, **kwargs)

    async def find_by_email(
        self, email: str, limit: int = 10, skip: int = 0, **kwargs
    ) -> List[Dict[str, Any]]:
        """Find comments by email."""
        filter_query = {"email": email}
        return await self.find_many(filter_query, limit, skip, **kwargs)

    async def find_by_name(
        self, name: str, limit: int = 10, skip: int = 0, **kwargs
    ) -> List[Dict[str, Any]]:
        """Find comments by name."""
        filter_query = {"name": name}
        return await self.find_many(filter_query, limit, skip, **kwargs)

    async def search_comments(self, **kwargs) -> List[Dict[str, Any]]:
        """Search comments with multiple filters."""
        filter_query = {}

        if "comment_id" in kwargs:
            try:
                filter_query["_id"] = ObjectId(kwargs["comment_id"])
            except Exception:
                pass

        if "movie_id" in kwargs:
            try:
                filter_query["movie_id"] = ObjectId(kwargs["movie_id"])
            except Exception:
                pass

        if "name" in kwargs:
            filter_query["name"] = kwargs["name"]

        if "email" in kwargs:
            filter_query["email"] = kwargs["email"]

        return await self.find_many(filter_query, **kwargs)
