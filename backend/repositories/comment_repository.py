from typing import List, Optional
from bson import ObjectId
from .base import BaseRepository
from backend.core.logging import get_logger
from ..schemas.schemas import CommentResponse

logger = get_logger(__name__)


class CommentRepository(BaseRepository):
    """Repository for comment data operations."""

    def __init__(self) -> None:
        super().__init__("sample_mflix", "comments")

    async def find_by_id(self, id: str, **kwargs) -> Optional[CommentResponse]:
        """Find a comment by its ID."""
        logger.debug(
            f"CommentRepository.find_by_id() called with id={id}, kwargs={kwargs}"
        )
        comment = await self._find_by_id(id, **kwargs)
        if comment:
            logger.debug(
                f"CommentRepository.find_by_id() found comment by {comment.get('name', 'Unknown')} on movie {comment.get('movie_id', 'Unknown')}"
            )
        else:
            logger.debug(
                f"CommentRepository.find_by_id() no comment found with id={id}"
            )
        return CommentResponse.from_dict(comment) if comment else None

    async def find_by_movie_id(self, movie_id: str, **kwargs) -> List[CommentResponse]:
        """Find comments by movie ID."""
        logger.debug(
            f"CommentRepository.find_by_movie_id() called with movie_id={movie_id}, kwargs={kwargs}"
        )
        try:
            filter_query = {"movie_id": ObjectId(movie_id)}
            logger.debug(
                f"CommentRepository.find_by_movie_id() converted movie_id to ObjectId: {movie_id}"
            )
            logger.debug(
                f"CommentRepository.find_by_movie_id() executing query: {filter_query}"
            )
            comments = await self._find_many(filter_query, **kwargs)
            logger.debug(
                f"CommentRepository.find_by_movie_id() found {len(comments)} comments for movie {movie_id}"
            )
            return [CommentResponse.from_dict(comment) for comment in comments]
        except Exception as e:
            logger.error(
                f"CommentRepository.find_by_movie_id() failed to convert movie_id to ObjectId: {movie_id}, error: {e}"
            )
            return []

    async def find_by_email(self, email: str, **kwargs) -> List[CommentResponse]:
        """Find comments by email."""
        logger.debug(
            f"CommentRepository.find_by_email() called with email='{email}', kwargs={kwargs}"
        )
        filter_query = {"email": email}
        logger.debug(
            f"CommentRepository.find_by_email() executing query: {filter_query}"
        )
        comments = await self._find_many(filter_query, **kwargs)
        logger.debug(
            f"CommentRepository.find_by_email() found {len(comments)} comments by email '{email}'"
        )
        return [CommentResponse.from_dict(comment) for comment in comments]

    async def find_by_name(self, name: str, **kwargs) -> List[CommentResponse]:
        """Find comments by name."""
        logger.debug(
            f"CommentRepository.find_by_name() called with name='{name}', kwargs={kwargs}"
        )
        filter_query = {"name": name}
        logger.debug(
            f"CommentRepository.find_by_name() executing query: {filter_query}"
        )
        comments = await self._find_many(filter_query, **kwargs)
        logger.debug(
            f"CommentRepository.find_by_name() found {len(comments)} comments by name '{name}'"
        )
        return [CommentResponse.from_dict(comment) for comment in comments]

    async def search_comments(self, **kwargs) -> List[CommentResponse]:
        """Search comments with multiple filters."""
        logger.debug(
            f"CommentRepository.search_comments() called with kwargs: {kwargs}"
        )
        filter_query = {}

        if "comment_id" in kwargs:
            try:
                filter_query["_id"] = ObjectId(kwargs["comment_id"])
                logger.debug(
                    f"CommentRepository.search_comments() added comment_id filter: {kwargs['comment_id']}"
                )
            except Exception as e:
                logger.warning(
                    f"CommentRepository.search_comments() failed to convert comment_id to ObjectId: {kwargs.get('comment_id')}, error: {e}"
                )

        if "movie_id" in kwargs:
            try:
                filter_query["movie_id"] = ObjectId(kwargs["movie_id"])
                logger.debug(
                    f"CommentRepository.search_comments() added movie_id filter: {kwargs['movie_id']}"
                )
            except Exception as e:
                logger.warning(
                    f"CommentRepository.search_comments() failed to convert movie_id to ObjectId: {kwargs.get('movie_id')}, error: {e}"
                )

        if "name" in kwargs:
            filter_query["name"] = kwargs["name"]
            logger.debug(
                f"CommentRepository.search_comments() added name filter: {kwargs['name']}"
            )

        if "email" in kwargs:
            filter_query["email"] = kwargs["email"]
            logger.debug(
                f"CommentRepository.search_comments() added email filter: {kwargs['email']}"
            )

        logger.debug(
            f"CommentRepository.search_comments() executing final filter_query: {filter_query}"
        )
        comments = await self._find_many(filter_query, **kwargs)
        logger.debug(
            f"CommentRepository.search_comments() found {len(comments)} comments matching search criteria"
        )
        return [CommentResponse.from_dict(comment) for comment in comments]
