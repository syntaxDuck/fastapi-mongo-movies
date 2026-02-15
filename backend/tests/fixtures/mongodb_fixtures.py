import asyncio
from collections.abc import Generator
from unittest.mock import AsyncMock

import mongomock
import pytest
from bson import ObjectId

from backend.database import MongoDBConfig


@pytest.fixture
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_db_config() -> MongoDBConfig:
    """Create a mock MongoDB configuration for testing."""
    return MongoDBConfig(
        username="test_user",
        password="test_password",
        host="test.mongodb.com",
        tls="true",
        tlsAllowInvalidCertificates="true",
    )


@pytest.fixture
def mock_mongo_client() -> mongomock.MongoClient:
    """Create a mock MongoDB client using mongomock."""
    return mongomock.MongoClient()


@pytest.fixture
def mock_db_handler(
    mock_db_config: MongoDBConfig,
):
    """Create a mock MongoDB client handler for testing using mongomock."""
    # Use mongomock for realistic testing
    mock_client = mongomock.MongoClient()

    # Insert sample data for testing
    setup_test_data(mock_client)

    # Create a simple mock handler with type: ignore to bypass complex type checking
    class SimpleMockHandler:  # type: ignore
        def __init__(self, client):
            self._client = client

        async def fetch_documents(
            self,
            database_name=None,
            collection_name=None,
            filter_query=None,
            limit=10,
            skip=0,
        ):
            db = self._client[database_name or "sample_mflix"]
            collection = db[collection_name or "movies"]

            # Build query
            mongo_filter = {}
            if filter_query:
                mongo_filter = filter_query

            # Apply pagination
            cursor = collection.find(mongo_filter).skip(skip).limit(limit)

            # Convert to list and return
            result = []
            for doc in cursor:
                # Convert ObjectId to string for consistency and transform document
                transformed_doc = {}
                for key, value in doc.items():
                    if key == "_id":
                        transformed_doc["id"] = str(value)
                    else:
                        transformed_doc[key] = value
                result.append(transformed_doc)
            return result

        async def insert_documents(
            self, database_name=None, collection_name=None, documents=None
        ):
            db = self._client[database_name or "sample_mflix"]
            collection = db[collection_name or "movies"]

            if isinstance(documents, list):
                result = collection.insert_many(documents)
            else:
                result = collection.insert_one(documents)
            return result

        @property
        def client(self):
            return self._client

        def close(self):
            if self._client:
                self._client.close()

    yield SimpleMockHandler(mock_client)

    # Cleanup
    mock_client.close()


def setup_test_data_mock(mock_client: AsyncMock) -> None:
    """Set up test data in mock database using async mocks."""
    # This is a simplified mock setup for testing
    # The actual data will be mocked in individual tests as needed
    pass


def setup_test_data(client: mongomock.MongoClient) -> None:
    """Set up test data in the mock database."""
    db = client.sample_mflix

    # Sample movies
    movies = [
        {
            "_id": ObjectId(),
            "title": "The Shawshank Redemption",
            "plot": "Two imprisoned men bond over years, finding redemption.",
            "genres": ["Drama"],
            "runtime": 142,
            "cast": ["Tim Robbins", "Morgan Freeman"],
            "num_mflix_comments": 5,
            "poster": "http://example.com/poster1.jpg",
            "countries": ["USA"],
            "released": "1994-09-23T00:00:00Z",
            "directors": ["Frank Darabont"],
            "writers": ["Stephen King", "Frank Darabont"],
            "awards": {"nominations": 0, "text": "N/A", "wins": 0},
            "lastupdated": "2015-08-25T00:00:00Z",
            "year": 1994,
            "type": "movie",
            "imdb": {"rating": 9.3, "votes": 2000000},
            "tomatoes": {"viewer": {"rating": 4.9, "numReviews": 1000}},
        }
    ]

    # Insert movies into the database
    db.movies.insert_many(movies)


@pytest.fixture
def sample_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "_id": ObjectId(),
        "name": "Test User",
        "password": "test_password",
        "email": "test@example.com",
    }


@pytest.fixture
def sample_comment_data() -> dict:
    """Sample comment data for testing."""
    return {
        "_id": ObjectId(),
        "name": "Test User",
        "email": "test@example.com",
        "movie_id": ObjectId(),
        "text": "Great movie!",
        "date": "2023-01-01T10:00:00Z",
    }
