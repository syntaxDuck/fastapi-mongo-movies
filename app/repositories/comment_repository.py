from typing import Dict, Any, List, Optional
from bson import ObjectId
from .base import BaseRepository
from app.core.logging import get_logger

logger = get_logger(__name__)


class CommentRepository(BaseRepository):
    """Repository for comment data operations."""

    def __init__(self) -> None:
        super().__init__("sample_mflix", "comments")

    async def find_by_id(
        self, entity_id: str, id_field: str = "_id", **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Find a comment by its ID."""
        logger.debug(
            f"CommentRepository.find_by_id() called with entity_id={entity_id}, id_field={id_field}"
        )
        return await super().find_by_id(entity_id, id_field, **kwargs)

    async def find_by_movie_id(self, movie_id: str, **kwargs) -> List[Dict[str, Any]]:
        """Find comments by movie ID."""
        logger.debug(
            f"CommentRepository.find_by_movie_id() called with movie_id={movie_id}, kwargs={kwargs}"
        )
        try:
            filter_query = {"movie_id": ObjectId(movie_id)}
            logger.debug(f"Converted movie_id to ObjectId: {movie_id}")
            return await self.find_many(filter_query, **kwargs)
        except Exception as e:
            logger.error(
                f"Failed to convert movie_id to ObjectId: {movie_id}, error: {e}"
            )
            return []

    async def find_by_email(self, email: str, **kwargs) -> List[Dict[str, Any]]:
        """Find comments by email."""
        logger.debug(
            f"CommentRepository.find_by_email() called with email={email}, kwargs={kwargs}"
        )
        filter_query = {"email": email}
        return await self.find_many(filter_query, **kwargs)

    async def find_by_name(self, name: str, **kwargs) -> List[Dict[str, Any]]:
        """Find comments by name."""
        logger.debug(
            f"CommentRepository.find_by_name() called with name={name}, kwargs={kwargs}"
        )
        filter_query = {"name": name}
        return await self.find_many(filter_query, **kwargs)

    async def search_comments(self, **kwargs) -> List[Dict[str, Any]]:
        """Search comments with multiple filters."""
        logger.debug(
            f"CommentRepository.search_comments() called with kwargs: {kwargs}"
        )
        filter_query = {}

        if "comment_id" in kwargs:
            try:
                filter_query["_id"] = ObjectId(kwargs["comment_id"])
                logger.debug(f"Added comment_id filter: {kwargs['comment_id']}")
            except Exception as e:
                logger.warning(
                    f"Failed to convert comment_id to ObjectId: {kwargs.get('comment_id')}, error: {e}"
                )

        if "movie_id" in kwargs:
            try:
                filter_query["movie_id"] = ObjectId(kwargs["movie_id"])
                logger.debug(f"Added movie_id filter: {kwargs['movie_id']}")
            except Exception as e:
                logger.warning(
                    f"Failed to convert movie_id to ObjectId: {kwargs.get('movie_id')}, error: {e}"
                )

        if "name" in kwargs:
            filter_query["name"] = kwargs["name"]
            logger.debug(f"Added name filter: {kwargs['name']}")

        if "email" in kwargs:
            filter_query["email"] = kwargs["email"]
            logger.debug(f"Added email filter: {kwargs['email']}")

        logger.debug(f"Final comment filter_query: {filter_query}")
        return await self.find_many(filter_query, **kwargs)
