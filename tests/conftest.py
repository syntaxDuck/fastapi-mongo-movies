"""
Test configuration and fixtures for the restructured application.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from mongomock import MongoClient

from app.repositories.movie_repository import MovieRepository
from app.repositories.user_repository import UserRepository
from app.repositories.comment_repository import CommentRepository
from app.services.movie_service import MovieService
from app.services.user_service import UserService
from app.services.comment_service import CommentService


@pytest.fixture
def mock_mongo_client():
    """Mock MongoDB client for testing."""
    return MongoClient()


@pytest.fixture
def movie_repository():
    """Movie repository fixture."""
    return MovieRepository()


@pytest.fixture
def user_repository():
    """User repository fixture."""
    return UserRepository()


@pytest.fixture
def comment_repository():
    """Comment repository fixture."""
    return CommentRepository()


@pytest.fixture
def movie_service(movie_repository):
    """Movie service fixture."""
    return MovieService(movie_repository)


@pytest.fixture
def user_service(user_repository):
    """User service fixture."""
    return UserService(user_repository)


@pytest.fixture
def comment_service(comment_repository):
    """Comment service fixture."""
    return CommentService(comment_repository)


# Sample data fixtures
@pytest.fixture
def sample_movie_data():
    """Sample movie data."""
    return {
        "_id": "503f19d3767d81a2a1200003",
        "plot": "Three men hammer on an anvil and strike a melody...",
        "genres": ["Short"],
        "runtime": 15,
        "cast": ["Charles Gorman"],
        "num_mflix_comments": 1,
        "title": "Blacksmith Scene",
        "fullplot": "Three men hammer on an anvil and strike a melody...",
        "countries": ["USA"],
        "released": "1893-05-09T00:00:00.000Z",
        "directors": ["William K.L. Dickson"],
        "writers": None,
        "awards": {"wins": 0, "nominations": 0, "text": ""},
        "lastupdated": "2015-08-15T12:17:48.177Z",
        "year": 1893,
        "imdb": {"rating": 6.2, "votes": 1181, "id": 5},
        "type": "movie",
        "tomatoes": {"viewer": {"rating": 3.1, "numReviews": 59}, "dvd": None},
    }


@pytest.fixture
def sample_user_data():
    """Sample user data."""
    return {
        "_id": "507f1f77bcf86cd799439011",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "hashed_password",
    }


@pytest.fixture
def sample_comment_data():
    """Sample comment data."""
    return {
        "_id": "507f1f77bcf86cd799439012",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "movie_id": "503f19d3767d81a2a1200003",
        "text": "Great movie!",
        "date": "2015-08-15T12:17:48.177Z",
    }


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
