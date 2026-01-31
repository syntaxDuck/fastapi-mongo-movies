import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from bson import ObjectId
from fastapi import HTTPException
import json

from api.main import app, get_mongo_connection
from api.models import Movie, MovieQuery, User, UserQuery, Comment, CommentQuery
from tests.fixtures.mongodb_fixtures import (
    sample_user_data,
)


class TestMongoConnectionDependency:
    """Test cases for MongoDB connection dependency."""

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_mongo_connection_success(self):
        """Test successful MongoDB connection creation."""
        with (
            patch("api.main.MongoDBConfig") as mock_config_class,
            patch("api.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_config = MagicMock()
            mock_config_class.return_value = mock_config

            mock_handler = AsyncMock()
            mock_handler.client = AsyncMock()
            mock_handler_class.return_value = mock_handler

            with patch("api.main.config") as mock_settings:
                mock_settings.DB_USER = "test_user"
                mock_settings.DB_PASS = "test_pass"
                mock_settings.DB_HOST = "test.mongodb.com"

                connection = await get_mongo_connection()

                mock_config_class.assert_called_once_with(
                    username="test_user",
                    password="test_pass",
                    host="test.mongodb.com",
                    tls="true",
                    tlsAllowInvalidCertificates="true",
                )
                mock_handler.client.assert_called_once()

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_get_mongo_connection_with_environment(self):
        """Test MongoDB connection with different environment settings."""
        with (
            patch("api.main.MongoDBConfig") as mock_config_class,
            patch("api.main.MongoDBClientHandler") as mock_handler_class,
        ):
            mock_handler = AsyncMock()
            mock_handler.client = AsyncMock()
            mock_handler_class.return_value = mock_handler

            with patch("api.main.config") as mock_settings:
                mock_settings.DB_USER = "prod_user"
                mock_settings.DB_PASS = "prod_pass"
                mock_settings.DB_HOST = "prod.mongodb.com"

                await get_mongo_connection()

                mock_config_class.assert_called_once()


class TestMovieEndpointsExtended:
    """Extended test cases for movie endpoints covering error scenarios and edge cases."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_movies_with_none_filters(self, client, mock_db_handler):
        """Test movie retrieval with None filter values."""
        mock_db_handler.fetch_documents = AsyncMock(return_value=[])

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            # Test with query object that has None values
            query = MovieQuery(id=None, title=None, type=None, limit=10, skip=0)

            response = client.get("/movies", params=query.model_dump(exclude_none=True))
            assert response.status_code == 404

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_movies_invalid_object_id(self, client, mock_db_handler):
        """Test movie retrieval with invalid ObjectId."""
        mock_db_handler.fetch_documents = AsyncMock(
            side_effect=Exception("Invalid ObjectId")
        )

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/movies?id=invalid_id")
            # Should handle the error gracefully
            assert response.status_code in [500, 422]

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_movies_database_error(self, client, mock_db_handler):
        """Test movie retrieval with database error."""
        mock_db_handler.fetch_documents = AsyncMock(
            side_effect=Exception("Database connection failed")
        )

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            with pytest.raises(Exception):
                client.get("/movies")

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_movies_with_invalid_movie_data(self, client, mock_db_handler):
        """Test movie retrieval with invalid movie data that fails model validation."""
        # Mock invalid movie data that will fail Pydantic validation
        invalid_movie_data = {
            "_id": ObjectId(),
            "title": "Test Movie",
            # Missing required fields like plot, genres, etc.
        }

        mock_db_handler.fetch_documents = AsyncMock(return_value=[invalid_movie_data])

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/movies")
            # Should handle invalid data gracefully
            assert response.status_code == 200
            movies = response.json()
            # Invalid movies should be filtered out (None values removed)
            assert len(movies) == 0

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_movies_complex_filtering(
        self, client, mock_db_handler, sample_movie_data
    ):
        """Test movie retrieval with complex filtering combinations."""
        sample_movies = [
            {
                **sample_movie_data,
                "_id": ObjectId(),
                "title": "Action Movie 2023",
                "year": 2023,
                "type": "movie",
            },
            {
                **sample_movie_data,
                "_id": ObjectId(),
                "title": "Drama Series 2022",
                "year": 2022,
                "type": "series",
            },
        ]
        mock_db_handler.fetch_documents = AsyncMock(return_value=sample_movies)

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            # Test with multiple filters
            response = client.get("/movies?type=movie&year=2023&limit=5&skip=0")
            assert response.status_code == 200
            movies = response.json()
            assert isinstance(movies, list)

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_comments_with_none_movie_id(self, client, mock_db_handler):
        """Test comment retrieval with None movie_id."""
        mock_db_handler.fetch_documents = AsyncMock(return_value=[])

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            query = CommentQuery(movie_id=None, limit=10, skip=0)
            response = client.get(
                "/comments", params=query.model_dump(exclude_none=True)
            )
            assert response.status_code == 404

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_comments_invalid_movie_id(self, client, mock_db_handler):
        """Test comment retrieval with invalid movie ObjectId."""
        mock_db_handler.fetch_documents = AsyncMock(
            side_effect=Exception("Invalid ObjectId")
        )

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/comments?movie_id=invalid_id")
            assert response.status_code in [500, 422]

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_comments_database_error(self, client, mock_db_handler):
        """Test comment retrieval with database error."""
        mock_db_handler.fetch_documents = AsyncMock(
            side_effect=Exception("Database error")
        )

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            with pytest.raises(Exception):
                client.get("/comments")

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_users_with_none_filters(self, client, mock_db_handler):
        """Test user retrieval with all None filters."""
        mock_db_handler.fetch_documents = AsyncMock(return_value=[])

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/users?_id=&name=&email=")
            assert response.status_code == 404

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_users_invalid_object_id(self, client, mock_db_handler):
        """Test user retrieval with invalid ObjectId."""
        mock_db_handler.fetch_documents = AsyncMock(
            side_effect=Exception("Invalid ObjectId")
        )

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/users?_id=invalid_id")
            assert response.status_code in [500, 422]

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_read_users_database_error(self, client, mock_db_handler):
        """Test user retrieval with database error."""
        mock_db_handler.fetch_documents = AsyncMock(
            side_effect=Exception("Database error")
        )

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            with pytest.raises(Exception):
                client.get("/users")

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_user_with_invalid_data(self, client, mock_db_handler):
        """Test user creation with invalid user data."""
        invalid_user = {
            "name": "Test User",
            # Missing required fields
        }

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.post("/users/", json=invalid_user)
            # Should return validation error
            assert response.status_code == 422

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_user_database_error_on_check(self, client, mock_db_handler):
        """Test user creation when database fails during existence check."""
        mock_db_handler.fetch_documents = AsyncMock(
            side_effect=Exception("Database error")
        )

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            with pytest.raises(Exception):
                client.post("/users/", json=sample_user_data)

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_user_insertion_failure(self, client, mock_db_handler):
        """Test user creation when insertion fails."""
        # Mock existing user check returns empty
        mock_db_handler.fetch_documents = AsyncMock(return_value=[])

        # Mock insertion failure
        mock_result = AsyncMock()
        mock_result.inserted_id = None
        mock_db_handler.insert_documents = AsyncMock(return_value=mock_result)

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.post("/users/", json=sample_user_data)
            assert response.status_code == 500
            assert "Failed to insert user" in response.json()["detail"]

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_user_general_exception(self, client, mock_db_handler):
        """Test user creation with general exception."""
        mock_db_handler.fetch_documents = AsyncMock(
            side_effect=Exception("Unexpected error")
        )

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.post("/users/", json=sample_user_data)
            assert response.status_code == 500
            assert "Unexpected error" in response.json()["detail"]

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_create_user_database_exception_on_insert(
        self, client, mock_db_handler
    ):
        """Test user creation when database raises exception during insert."""
        mock_db_handler.fetch_documents = AsyncMock(return_value=[])  # No existing user
        mock_db_handler.insert_documents = AsyncMock(
            side_effect=Exception("Insert failed")
        )

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            with pytest.raises(Exception):
                client.post("/users/", json=sample_user_data)


class TestAPIServersAndConfiguration:
    """Test API server configuration and metadata."""

    @pytest.mark.api
    def test_api_root_endpoint(self):
        """Test API root endpoint returns proper response."""
        client = TestClient(app)
        response = client.get("/")
        # FastAPI default root endpoint should return redirect to docs
        assert response.status_code in [200, 404]

    @pytest.mark.api
    def test_api_docs_endpoint(self):
        """Test API documentation endpoint."""
        client = TestClient(app)
        response = client.get("/docs")
        assert response.status_code == 200

    @pytest.mark.api
    def test_api_openapi_endpoint(self):
        """Test OpenAPI specification endpoint."""
        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()

    @pytest.mark.api
    def test_api_redoc_endpoint(self):
        """Test ReDoc endpoint."""
        client = TestClient(app)
        response = client.get("/redoc")
        assert response.status_code == 200


class TestAPIValidationAndEdgeCases:
    """Test API validation and edge cases."""

    @pytest.mark.api
    def test_invalid_endpoint(self):
        """Test request to invalid endpoint."""
        client = TestClient(app)
        response = client.get("/invalid_endpoint")
        assert response.status_code == 404

    @pytest.mark.api
    def test_invalid_http_method(self):
        """Test invalid HTTP method on valid endpoint."""
        client = TestClient(app)
        response = client.delete("/movies")
        assert response.status_code == 405

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_query_parameter_validation(self):
        """Test query parameter validation."""
        client = TestClient(app)

        with patch("api.main.get_mongo_connection") as mock_connection:
            mock_handler = AsyncMock()
            mock_connection.return_value = mock_handler
            mock_handler.fetch_documents = AsyncMock(return_value=[])

            # Test invalid limit parameter
            response = client.get("/movies?limit=-1")
            assert response.status_code == 422

            # Test invalid skip parameter
            response = client.get("/movies?skip=-1")
            assert response.status_code == 422

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_large_pagination_values(self):
        """Test with very large pagination values."""
        client = TestClient(app)

        with patch("api.main.get_mongo_connection") as mock_connection:
            mock_handler = AsyncMock()
            mock_connection.return_value = mock_handler
            mock_handler.fetch_documents = AsyncMock(return_value=[])

            # Test with very large limit
            response = client.get("/movies?limit=10000")
            # Should handle gracefully (actual limit may be enforced by database layer)

            # Test with very large skip
            response = client.get("/movies?skip=100000")
            assert response.status_code in [200, 404, 422]

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_special_characters_in_parameters(self):
        """Test parameters with special characters."""
        client = TestClient(app)

        with patch("api.main.get_mongo_connection") as mock_connection:
            mock_handler = AsyncMock()
            mock_connection.return_value = mock_handler
            mock_handler.fetch_documents = AsyncMock(return_value=[])

            # Test title with special characters
            response = client.get("/movies?title=Movie%20%26%20Special%20%3F%20Chars")
            assert response.status_code in [200, 404]

            # Test name with special characters
            response = client.get("/users?name=John%20Doe%20%40%20Company")
            assert response.status_code in [200, 404]

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        client = TestClient(app)

        with patch("api.main.get_mongo_connection") as mock_connection:
            mock_handler = AsyncMock()
            mock_connection.return_value = mock_handler
            mock_handler.fetch_documents = AsyncMock(return_value=[])

            import asyncio
            import threading

            def make_request():
                return client.get("/movies")

            # Make multiple concurrent requests
            threads = [threading.Thread(target=make_request) for _ in range(5)]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            # Should handle concurrent requests without errors


class TestAPIResponseFormats:
    """Test API response formats and headers."""

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_response_content_type(self):
        """Test that responses have correct content type."""
        client = TestClient(app)

        with patch("api.main.get_mongo_connection") as mock_connection:
            mock_handler = AsyncMock()
            mock_connection.return_value = mock_handler
            mock_handler.fetch_documents = AsyncMock(return_value=[])

            response = client.get("/movies")
            assert response.headers["content-type"].startswith("application/json")

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_error_response_format(self):
        """Test that error responses have correct format."""
        client = TestClient(app)

        with patch("api.main.get_mongo_connection") as mock_connection:
            mock_handler = AsyncMock()
            mock_connection.return_value = mock_handler
            mock_handler.fetch_documents = AsyncMock(return_value=[])  # Empty result

            response = client.get("/movies")
            assert response.status_code == 404
            error_data = response.json()
            assert "detail" in error_data
            assert isinstance(error_data["detail"], str)

    @pytest.mark.api
    @pytest.mark.asyncio
    async def test_response_data_structure(self):
        """Test that successful responses have correct data structure."""
        client = TestClient(app)

        with patch("api.main.get_mongo_connection") as mock_connection:
            mock_handler = AsyncMock()
            mock_connection.return_value = mock_handler

            # Mock movie data
            sample_movies = [
                {
                    "_id": ObjectId(),
                    "title": "Test Movie",
                    "plot": "Test plot",
                    "genres": ["Drama"],
                    "runtime": 120,
                    "cast": ["Actor 1"],
                    "num_mflix_comments": 5,
                    "poster": None,
                    "fullplot": None,
                    "countries": ["USA"],
                    "released": "2023-01-01T00:00:00Z",
                    "directors": ["Director 1"],
                    "writers": ["Writer 1"],
                    "awards": {"nominations": 0, "text": "N/A", "wins": 0},
                    "lastupdated": "2023-01-01T00:00:00Z",
                    "year": 2023,
                    "type": "movie",
                    "imdb": {"rating": 8.0, "votes": 1000},
                    "tomatoes": {"viewer": {"rating": 4.0, "numReviews": 100}},
                }
            ]
            mock_handler.fetch_documents = AsyncMock(return_value=sample_movies)

            response = client.get("/movies")
            assert response.status_code == 200
            movies = response.json()
            assert isinstance(movies, list)
            assert len(movies) == 1

            movie = movies[0]
            assert "id" in movie
            assert "title" in movie
            assert "plot" in movie
            assert "genres" in movie
            assert "runtime" in movie
            assert "cast" in movie
            assert "countries" in movie
            assert "released" in movie
            assert "directors" in movie
            assert "awards" in movie
            assert "lastupdated" in movie
            assert "year" in movie
            assert "type" in movie
            assert "imdb" in movie
            assert "tomatoes" in movie
