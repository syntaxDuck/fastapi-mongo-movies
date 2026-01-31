"""
Service layer for business logic using proper protocol-based dependency injection.
"""

from typing import List, Optional, Dict, Any
from ..repositories.protocol import (
    MovieRepositoryProtocol,
    UserRepositoryProtocol,
    CommentRepositoryProtocol,
)
from ..core.exceptions import NotFoundError, DatabaseError, DuplicateResourceError


class MovieService:
    """Service layer for movie business logic."""

    def __init__(self, movie_repository: MovieRepositoryProtocol) -> None:
        self.movie_repository = movie_repository

    async def get_movie_by_id(self, movie_id: str) -> Dict[str, Any]:
        """Get a movie by its ID."""
        movie = await self.movie_repository.find_by_id(movie_id)
        if not movie:
            raise NotFoundError(f"Movie with ID {movie_id} not found")
        return movie

    async def get_movies(
        self,
        movie_id: Optional[str] = None,
        title: Optional[str] = None,
        movie_type: Optional[str] = None,
        genres: Optional[List[str]] = None,
        year: Optional[int] = None,
        limit: int = 10,
        skip: int = 0,
    ) -> List[Dict[str, Any]]:
        """Get movies with optional filtering."""
        movies = await self.movie_repository.search_movies(
            movie_id=movie_id,
            title=title,
            movie_type=movie_type,
            genres=genres,
            year=year,
            limit=limit,
            skip=skip,
        )

        if not movies:
            raise NotFoundError("No movies found matching the criteria")

        return movies

    async def get_movies_by_type(
        self, movie_type: str, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get movies by type."""
        movies = await self.movie_repository.find_by_type(
            movie_type, limit=limit, skip=skip
        )
        if not movies:
            raise NotFoundError(f"No movies found of type '{movie_type}'")
        return movies

    async def get_movies_by_year(
        self, year: int, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get movies by year."""
        movies = await self.movie_repository.find_by_year(year, limit=limit, skip=skip)
        if not movies:
            raise NotFoundError(f"No movies found for year {year}")
        return movies

    async def get_movies_by_genre(
        self, genre: str, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get movies by genre."""
        movies = await self.movie_repository.find_by_genre(
            genre, limit=limit, skip=skip
        )
        if not movies:
            raise NotFoundError(f"No movies found for genre '{genre}'")
        return movies


class UserService:
    """Service layer for user business logic."""

    def __init__(self, user_repository: UserRepositoryProtocol) -> None:
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        """Get a user by their ID."""
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        return user

    async def get_users(
        self,
        user_id: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        limit: int = 10,
        skip: int = 0,
    ) -> List[Dict[str, Any]]:
        """Get users with optional filtering."""
        users = await self.user_repository.search_users(
            user_id=user_id, name=name, email=email, limit=limit, skip=skip
        )

        if not users:
            raise NotFoundError("No users found matching the criteria")

        return users

    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user."""
        email = user_data.get("email")
        if not email:
            raise ValueError("Email is required")

        # Check if user with email already exists
        if await self.user_repository.email_exists(email):
            raise DuplicateResourceError(f"User with email '{email}' already exists")

        user_id = await self.user_repository.create_one(user_data)
        if not user_id:
            raise DatabaseError("Failed to create user")

        return user_id

    async def get_users_by_email(self, email: str) -> List[Dict[str, Any]]:
        """Get users by email."""
        users = await self.user_repository.find_by_email(email)
        if not users:
            raise NotFoundError(f"No users found with email '{email}'")
        return users

    async def get_users_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Get users by name."""
        users = await self.user_repository.find_by_name(name)
        if not users:
            raise NotFoundError(f"No users found with name '{name}'")
        return users


class CommentService:
    """Service layer for comment business logic."""

    def __init__(self, comment_repository: CommentRepositoryProtocol) -> None:
        self.comment_repository = comment_repository

    async def get_comment_by_id(self, comment_id: str) -> Dict[str, Any]:
        """Get a comment by its ID."""
        comment = await self.comment_repository.find_by_id(comment_id)
        if not comment:
            raise NotFoundError(f"Comment with ID {comment_id} not found")
        return comment

    async def get_comments(
        self,
        comment_id: Optional[str] = None,
        movie_id: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        limit: int = 10,
        skip: int = 0,
    ) -> List[Dict[str, Any]]:
        """Get comments with optional filtering."""
        comments = await self.comment_repository.search_comments(
            comment_id=comment_id,
            movie_id=movie_id,
            name=name,
            email=email,
            limit=limit,
            skip=skip,
        )

        if not comments:
            raise NotFoundError("No comments found matching the criteria")

        return comments

    async def get_comments_by_movie_id(
        self, movie_id: str, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get comments by movie ID."""
        comments = await self.comment_repository.find_by_movie_id(
            movie_id, limit=limit, skip=skip
        )
        if not comments:
            raise NotFoundError(f"No comments found for movie ID '{movie_id}'")
        return comments

    async def get_comments_by_email(
        self, email: str, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get comments by email."""
        comments = await self.comment_repository.find_by_email(
            email, limit=limit, skip=skip
        )
        if not comments:
            raise NotFoundError(f"No comments found for email '{email}'")
        return comments

    async def get_comments_by_name(
        self, name: str, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get comments by name."""
        comments = await self.comment_repository.find_by_name(
            name, limit=limit, skip=skip
        )
        if not comments:
            raise NotFoundError(f"No comments found for name '{name}'")
        return comments
