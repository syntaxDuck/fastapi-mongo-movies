"""
Comment Service layer for business logic using proper protocol-based dependency injection.
"""

from ..core.exceptions import NotFoundError
from ..core.logging import get_logger
from ..repositories.protocol import CommentRepositoryProtocol
from ..schemas import CommentCreate, CommentResponse

logger = get_logger(__name__)


class CommentService:
    """Service layer for comment business logic."""

    def __init__(self, comment_repository: CommentRepositoryProtocol) -> None:
        self.comment_repository = comment_repository

    async def get_comment_by_id(self, comment_id: str) -> CommentResponse:
        """Get a comment by its ID."""
        logger.debug(f"Getting comment by ID: {comment_id}")

        comment = await self.comment_repository.find_by_id(comment_id)
        if not comment:
            logger.warning(f"Comment not found: {comment_id}")
            raise NotFoundError(f"Comment with ID {comment_id} not found")

        logger.debug(f"Successfully retrieved comment: {comment_id}")
        return comment

    async def get_comments(
        self,
        comment_id: str | None = None,
        movie_id: str | None = None,
        name: str | None = None,
        email: str | None = None,
        limit: int = 10,
        skip: int = 0,
    ) -> list[CommentResponse]:
        """Get comments with optional filtering."""
        logger.debug(
            f"Getting comments with filters: comment_id={comment_id}, movie_id={movie_id}, "
            f"name={name}, email={email}, limit={limit}, skip={skip}"
        )

        comments = await self.comment_repository.search_comments(
            comment_id=comment_id,
            movie_id=movie_id,
            name=name,
            email=email,
            limit=limit,
            skip=skip,
        )

        if not comments:
            logger.info("No comments found matching the criteria")
            raise NotFoundError("No comments found matching the criteria")

        logger.info(f"Found {len(comments)} comments")
        return comments

    async def get_comments_by_movie_id(
        self, movie_id: str, limit: int = 10, skip: int = 0
    ) -> list[CommentResponse]:
        """Get comments by movie ID."""
        logger.debug(f"Getting comments by movie ID: {movie_id}, limit={limit}, skip={skip}")

        comments = await self.comment_repository.find_by_movie_id(movie_id, limit=limit, skip=skip)
        if not comments:
            logger.info(f"No comments found for movie ID: {movie_id}")
            raise NotFoundError(f"No comments found for movie ID '{movie_id}'")

        logger.info(f"Found {len(comments)} comments for movie ID: {movie_id}")
        return comments

    async def get_comments_by_email(
        self, email: str, limit: int = 10, skip: int = 0
    ) -> list[CommentResponse]:
        """Get comments by email."""
        logger.debug(f"Getting comments by email: {email}, limit={limit}, skip={skip}")

        comments = await self.comment_repository.find_by_email(email, limit=limit, skip=skip)
        if not comments:
            logger.info(f"No comments found for email: {email}")
            raise NotFoundError(f"No comments found for email '{email}'")

        logger.info(f"Found {len(comments)} comments for email: {email}")
        return comments

    async def get_comments_by_name(
        self, name: str, limit: int = 10, skip: int = 0
    ) -> list[CommentResponse]:
        """Get comments by name."""
        logger.debug(f"Getting comments by name: {name}, limit={limit}, skip={skip}")

        comments = await self.comment_repository.find_by_name(name, limit=limit, skip=skip)
        if not comments:
            logger.info(f"No comments found for name: {name}")
            raise NotFoundError(f"No comments found for name '{name}'")

        logger.info(f"Found {len(comments)} comments for name: {name}")
        return comments

    async def create_comment(self, comment_data: CommentCreate) -> CommentResponse:
        """Create a new comment."""
        logger.debug(f"Creating comment for movie: {comment_data.movie_id}")

        comment_id = await self.comment_repository.create_comment(comment_data)
        if not comment_id:
            logger.error("Failed to create comment")
            raise NotFoundError("Failed to create comment")

        logger.info(f"Successfully created comment with ID: {comment_id}")
        comment = await self.comment_repository.find_by_id(comment_id)
        if not comment:
            logger.error(f"Created comment not found: {comment_id}")
            raise NotFoundError(f"Created comment not found: {comment_id}")

        return comment
