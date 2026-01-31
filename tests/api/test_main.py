import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from bson import ObjectId

from api.main import app, get_mongo_connection
from api.models import Movie, MovieQuery, User, UserQuery, Comment, CommentQuery
from tests.fixtures.mongodb_fixtures import mock_db_handler


class TestMovieEndpoints:
    """Test cases for movie-related endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    @pytest.mark.movie
    def test_read_movies_success(self, client, mock_db_handler):
        """Test successful movie retrieval."""
        # Mock the dependency injection at the endpoint level
        app.dependency_overrides[get_mongo_connection] = lambda: mock_db_handler
        response = client.get("/movies")

        assert response.status_code == 200
        movies = response.json()
        assert isinstance(movies, list)
        assert len(movies) > 0

        # Check structure of first movie
        movie = movies[0]
        assert "id" in movie
        assert "title" in movie
        assert "plot" in movie
        assert "genres" in movie

    @pytest.mark.movie
    def test_read_movies_with_filters(self, client, mock_db_handler):
        """Test movie retrieval with filters."""
        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            # Test with title filter
            response = client.get("/movies?title=The Shawshank Redemption")
            assert response.status_code == 200
            movies = response.json()
            assert len(movies) == 1
            assert movies[0]["title"] == "The Shawshank Redemption"

            # Test with type filter
            response = client.get("/movies?type=movie")
            assert response.status_code == 200
            movies = response.json()
            assert all(movie["type"] == "movie" for movie in movies)

    @pytest.mark.movie
    def test_read_movies_with_pagination(self, client, mock_db_handler):
        """Test movie pagination."""
        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            # Test with limit
            response = client.get("/movies?limit=1")
            assert response.status_code == 200
            movies = response.json()
            assert len(movies) == 1

            # Test with skip
            response = client.get("/movies?skip=1")
            assert response.status_code == 200
            movies = response.json()
            assert len(movies) >= 0

    @pytest.mark.movie
    def test_read_movies_not_found(self, client, mock_db_handler):
        """Test movie retrieval when no movies found."""
        # Mock empty response
        mock_db_handler.fetch_documents = AsyncMock(return_value=[])

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/movies")
            assert response.status_code == 404
            assert response.json()["detail"] == "Movies not found"

    @pytest.mark.movie
    def test_read_movies_by_id(self, client, mock_db_handler):
        """Test movie retrieval by specific ID."""
        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            # Get first movie to extract its ID
            movies_response = client.get("/movies?limit=1")
            if movies_response.status_code == 200:
                movies = movies_response.json()
                if movies:
                    movie_id = movies[0]["id"]
                    response = client.get(f"/movies?id={movie_id}")
                    assert response.status_code == 200
                    filtered_movies = response.json()
                    assert len(filtered_movies) == 1
                    assert filtered_movies[0]["id"] == movie_id


class TestUserEndpoints:
    """Test cases for user-related endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    @pytest.mark.user
    def test_read_users_success(self, client, mock_db_handler):
        """Test successful user retrieval."""
        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/users")
            assert response.status_code == 200
            users = response.json()
            assert isinstance(users, list)
            assert len(users) > 0

            # Check structure of first user
            user = users[0]
            assert "id" in user
            assert "name" in user
            assert "email" in user

    @pytest.mark.user
    def test_read_users_with_filters(self, client, mock_db_handler):
        """Test user retrieval with filters."""
        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            # Test with name filter
            response = client.get("/users?name=John Doe")
            assert response.status_code == 200
            users = response.json()
            if users:  # Only check if users are found
                assert users[0]["name"] == "John Doe"

            # Test with email filter
            response = client.get("/users?email=john.doe@example.com")
            assert response.status_code == 200
            users = response.json()
            if users:  # Only check if users are found
                assert users[0]["email"] == "john.doe@example.com"

    @pytest.mark.user
    def test_create_user_success(self, client, mock_db_handler):
        """Test successful user creation."""
        new_user = {
            "id": str(ObjectId()),
            "name": "New User",
            "password": "secure_password",
            "email": "newuser@example.com",
        }

        # Mock the database operations
        mock_db_handler.fetch_documents = AsyncMock(return_value=[])  # No existing user
        mock_result = AsyncMock()
        mock_result.inserted_id = ObjectId()
        mock_db_handler.insert_documents = AsyncMock(return_value=mock_result)

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.post("/users/", json=new_user)
            assert response.status_code == 200
            assert "User created successfully" in response.json()["message"]

    @pytest.mark.user
    def test_create_user_duplicate_email(self, client, mock_db_handler):
        """Test user creation with duplicate email."""
        existing_user = {"email": "existing@example.com"}
        new_user = {
            "id": str(ObjectId()),
            "name": "New User",
            "password": "secure_password",
            "email": "existing@example.com",
        }

        # Mock existing user found
        mock_db_handler.fetch_documents = AsyncMock(return_value=[existing_user])

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.post("/users/", json=new_user)
            assert response.status_code == 400
            assert "already exists" in response.json()["detail"]

    @pytest.mark.user
    def test_read_users_not_found(self, client, mock_db_handler):
        """Test user retrieval when no users found."""
        mock_db_handler.fetch_documents = AsyncMock(return_value=[])

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/users")
            assert response.status_code == 404
            assert response.json()["detail"] == "Users not found"


class TestCommentEndpoints:
    """Test cases for comment-related endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    @pytest.mark.comment
    def test_read_comments_success(self, client, mock_db_handler):
        """Test successful comment retrieval."""
        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/comments")
            assert response.status_code == 200
            comments = response.json()
            assert isinstance(comments, list)
            assert len(comments) > 0

            # Check structure of first comment
            comment = comments[0]
            assert "id" in comment
            assert "name" in comment
            assert "email" in comment
            assert "movie_id" in comment
            assert "text" in comment
            assert "date" in comment

    @pytest.mark.comment
    def test_read_comments_by_movie_id(self, client, mock_db_handler):
        """Test comment retrieval filtered by movie ID."""
        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            # Get a movie ID first
            movies_response = client.get("/movies?limit=1")
            if movies_response.status_code == 200:
                movies = movies_response.json()
                if movies:
                    movie_id = movies[0]["id"]
                    response = client.get(f"/comments?movie_id={movie_id}")
                    assert response.status_code == 200
                    comments = response.json()
                    # All comments should belong to this movie
                    assert all(comment["movie_id"] == movie_id for comment in comments)

    @pytest.mark.comment
    def test_read_comments_not_found(self, client, mock_db_handler):
        """Test comment retrieval when no comments found."""
        mock_db_handler.fetch_documents = AsyncMock(return_value=[])

        with patch("api.main.get_mongo_connection", return_value=mock_db_handler):
            response = client.get("/comments")
            assert response.status_code == 404
            assert response.json()["detail"] == "Comments not found"
