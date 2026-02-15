"""
Unit tests for the restructured application services.
"""

from unittest.mock import AsyncMock

import pytest

from backend.core.exceptions import DuplicateResourceError, NotFoundError
from backend.schemas.schemas import MessageResponse, UserCreate


class TestMovieService:
    """Test cases for MovieService."""

    @pytest.mark.asyncio
    async def test_get_movie_by_id_success(self, movie_service, sample_movie_data):
        """Test getting a movie by ID successfully."""
        # Mock the repository response
        movie_service.movie_repository.find_by_id = AsyncMock(
            return_value=sample_movie_data
        )

        result = await movie_service.get_movie_by_id("503f19d3767d81a2a1200003")

        assert result == sample_movie_data
        movie_service.movie_repository.find_by_id.assert_called_once_with(
            "503f19d3767d81a2a1200003"
        )

    @pytest.mark.asyncio
    async def test_get_movie_by_id_not_found(self, movie_service):
        """Test getting a movie by ID that doesn't exist."""
        movie_service.movie_repository.find_by_id = AsyncMock(return_value=None)

        with pytest.raises(NotFoundError, match="Movie with ID 123 not found"):
            await movie_service.get_movie_by_id("123")

    @pytest.mark.asyncio
    async def test_search_movies_multiple_criteria_success(
        self, movie_service, sample_movie_data
    ):
        """Test getting movies with filters successfully."""
        movie_service.movie_repository.search_movies = AsyncMock(
            return_value=[sample_movie_data]
        )

        result = await movie_service.search_movies_multiple_criteria(
            title="Blacksmith Scene"
        )

        assert result == [sample_movie_data]
        movie_service.movie_repository.search_movies.assert_called_once_with(
            movie_id=None,
            title="Blacksmith Scene",
            movie_type=None,
            genres=None,
            year=None,
            limit=10,
            skip=0,
            include_invalid_posters=False,
            sort_by=None,
            sort_order="asc",
        )

    @pytest.mark.asyncio
    async def test_search_movies_multiple_criteria_no_results(self, movie_service):
        """Test getting movies with no matching results."""
        movie_service.movie_repository.search_movies = AsyncMock(return_value=[])

        with pytest.raises(
            NotFoundError, match="No movies found matching the criteria"
        ):
            await movie_service.search_movies_multiple_criteria(
                title="Nonexistent Movie"
            )


class TestUserService:
    """Test cases for UserService."""

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, user_service, sample_user_data):
        """Test getting a user by ID successfully."""
        user_service.user_repository.find_by_id = AsyncMock(
            return_value=sample_user_data
        )

        result = await user_service.get_user_by_id("507f1f77bcf86cd799439011")

        assert result == sample_user_data
        user_service.user_repository.find_by_id.assert_called_once_with(
            "507f1f77bcf86cd799439011"
        )

    @pytest.mark.asyncio
    async def test_create_user_success(self, user_service):
        """Test creating a user successfully with hashed password."""
        user_data = UserCreate(
            name="New User",
            email="newuser@example.com",
            password="password123",
        )

        user_service.user_repository.email_exists = AsyncMock(return_value=False)
        user_service.user_repository.create_user = AsyncMock(
            return_value=MessageResponse(message="new_user_id")
        )

        result = await user_service.create_user(user_data)

        assert result.message == "new_user_id"
        user_service.user_repository.email_exists.assert_called_once_with(
            "newuser@example.com"
        )

        # Verify repository was called and password was hashed
        called_user_data = user_service.user_repository.create_user.call_args[0][0]
        assert called_user_data.password != "password123"
        assert "$" in called_user_data.password

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, user_service):
        """Test creating a user with duplicate email."""
        user_data = UserCreate(
            name="Duplicate User",
            email="existing@example.com",
            password="password123",
        )

        user_service.user_repository.email_exists = AsyncMock(return_value=True)

        with pytest.raises(
            DuplicateResourceError,
            match="User with email 'existing@example.com' already exists",
        ):
            await user_service.create_user(user_data)

    @pytest.mark.asyncio
    async def test_create_user_missing_email(self, user_service):
        """Test creating a user without email."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            UserCreate(name="No Email User", password="password123")


class TestCommentService:
    """Test cases for CommentService."""

    @pytest.mark.asyncio
    async def test_get_comment_by_id_success(
        self, comment_service, sample_comment_data
    ):
        """Test getting a comment by ID successfully."""
        comment_service.comment_repository.find_by_id = AsyncMock(
            return_value=sample_comment_data
        )

        result = await comment_service.get_comment_by_id("507f1f77bcf86cd799439012")

        assert result == sample_comment_data
        comment_service.comment_repository.find_by_id.assert_called_once_with(
            "507f1f77bcf86cd799439012"
        )

    @pytest.mark.asyncio
    async def test_get_comments_by_movie_id_success(
        self, comment_service, sample_comment_data
    ):
        """Test getting comments by movie ID successfully."""
        comment_service.comment_repository.find_by_movie_id = AsyncMock(
            return_value=[sample_comment_data]
        )

        result = await comment_service.get_comments_by_movie_id(
            "503f19d3767d81a2a1200003"
        )

        assert result == [sample_comment_data]
        comment_service.comment_repository.find_by_movie_id.assert_called_once_with(
            "503f19d3767d81a2a1200003", limit=10, skip=0
        )

    @pytest.mark.asyncio
    async def test_get_comments_by_movie_id_not_found(self, comment_service):
        """Test getting comments by movie ID with no results."""
        comment_service.comment_repository.find_by_movie_id = AsyncMock(return_value=[])

        with pytest.raises(NotFoundError, match="No comments found for movie ID '123'"):
            await comment_service.get_comments_by_movie_id("123")
