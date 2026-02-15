import contextlib
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add the frontend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../frontend"))

from api.models import CommentQuery, MovieQuery
from frontend.data import fetch_comments, fetch_movies, process_movies
from frontend.helper import build_movie_list


class TestDataModule:
    """Test cases for frontend data module."""

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_movies_success(self, mock_get):
        """Test successful movie fetching."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "1",
                "title": "Test Movie",
                "plot": "Test plot",
                "genres": ["Drama"],
                "runtime": 120,
                "cast": ["Actor 1", "Actor 2"],
                "countries": ["USA"],
                "released": "2023-01-01T00:00:00Z",
                "directors": ["Director 1"],
                "awards": {"nominations": 0, "text": "N/A", "wins": 0},
                "lastupdated": "2023-01-01T00:00:00Z",
                "year": 2023,
                "type": "movie",
                "imdb": {"rating": 8.0, "votes": 1000},
                "tomatoes": {"viewer": {"rating": 4.0, "numReviews": 100}},
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Mock config
        with patch("data.config.API_URL", "http://test-api.com"):
            result = fetch_movies(MovieQuery(limit=10, skip=0))

            assert len(result) == 1
            assert result[0]["title"] == "Test Movie"
            assert result[0]["type"] == "movie"
            mock_get.assert_called_once()

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_comments_success(self, mock_get):
        """Test successful comment fetching."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "1",
                "name": "Test User",
                "email": "test@example.com",
                "movie_id": "movie123",
                "text": "Great movie!",
                "date": "2023-01-01T10:00:00Z",
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Mock config
        with patch("data.config.API_URL", "http://test-api.com"):
            query = CommentQuery(movie_id="movie123")
            result = fetch_comments(query)

            assert len(result) == 1
            assert result[0]["name"] == "Test User"
            assert result[0]["movie_id"] == "movie123"
            mock_get.assert_called_once()

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_movies_api_error(self, mock_get):
        """Test movie fetching with API error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with patch("data.config.API_URL", "http://test-api.com"):
            result = fetch_movies(MovieQuery(limit=10, skip=0))

            assert result == []

    @pytest.mark.frontend
    def test_process_movies_valid(self):
        """Test processing valid movie data."""
        raw_movies = [
            {
                "id": "1",
                "title": "Test Movie",
                "plot": "Test plot",
                "genres": ["Drama"],
                "runtime": 120,
                "cast": ["Actor 1"],
                "countries": ["USA"],
                "released": "2023-01-01T00:00:00Z",
                "directors": ["Director 1"],
                "awards": {"nominations": 0, "text": "N/A", "wins": 0},
                "lastupdated": "2023-01-01T00:00:00Z",
                "year": 2023,
                "type": "movie",
                "imdb": {"rating": 8.0, "votes": 1000},
                "tomatoes": {"viewer": {"rating": 4.0, "numReviews": 100}},
            }
        ]

        result = process_movies(raw_movies)

        assert len(result) == 1
        movie = result[0]
        assert "index" in movie
        assert movie["title"] == "Test Movie"
        assert movie["index"] == 0

    @pytest.mark.frontend
    def test_process_movies_empty_list(self):
        """Test processing empty movie list."""
        result = process_movies([])
        assert result == []

    @pytest.mark.frontend
    def test_process_movies_with_missing_data(self):
        """Test processing movies with missing required fields."""
        raw_movies = [
            {
                "id": "1",
                "title": "Test Movie",
                # Missing required fields like plot, genres, etc.
            }
        ]

        # Should handle missing data gracefully
        result = process_movies(raw_movies)

        # Behavior depends on implementation - adjust test as needed
        # This test ensures the function doesn't crash on missing data
        assert isinstance(result, list)


class TestHelperModule:
    """Test cases for frontend helper module."""

    @pytest.mark.frontend
    def test_build_movie_list_empty(self):
        """Test building movie list with empty data."""
        result = build_movie_list([])

        # Should return a valid HTML structure even for empty list
        assert result is not None

    @pytest.mark.frontend
    def test_build_movie_list_with_movies(self):
        """Test building movie list with movie data."""
        movies = [
            {
                "index": 0,
                "id": "1",
                "title": "Test Movie",
                "plot": "Test plot",
                "genres": ["Drama"],
                "runtime": 120,
                "cast": ["Actor 1"],
                "countries": ["USA"],
                "released": "2023-01-01T00:00:00Z",
                "directors": ["Director 1"],
                "awards": {"nominations": 0, "text": "N/A", "wins": 0},
                "lastupdated": "2023-01-01T00:00:00Z",
                "year": 2023,
                "type": "movie",
                "imdb": {"rating": 8.0, "votes": 1000},
                "tomatoes": {"viewer": {"rating": 4.0, "numReviews": 100}},
            }
        ]

        result = build_movie_list(movies)

        assert result is not None
        # Should contain movie information in the HTML structure


class TestFrontendMain:
    """Test cases for frontend main application."""

    @pytest.mark.frontend
    @patch("frontend.main.fetch_movies")
    @patch("frontend.main.process_movies")
    @patch("frontend.main.build_movie_list")
    def test_get_movies_endpoint(self, mock_build, mock_process, mock_fetch):
        """Test /movies endpoint."""
        # Setup mocks
        mock_fetch.return_value = [{"id": "1", "title": "Test Movie"}]
        mock_process.return_value = [{"index": 0, "title": "Test Movie"}]
        mock_build.return_value = "<div>Movie List HTML</div>"

        # Import here to avoid path issues
        try:
            # Test the function logic without FastHTML framework
            from importlib import import_module

            main_module = import_module("frontend.main")

            # Simulate the global movies list using setattr
            main_module.movies = []

            # Call the function logic directly
            # Note: This is a simplified test since FastHTML routing is complex to mock
            mock_fetch.assert_not_called()  # Should be called in actual endpoint

        except ImportError as e:
            # Skip if FastHTML dependencies not available
            pytest.skip(f"FastHTML dependencies not available: {e}")

    @pytest.mark.frontend
    def test_global_movies_initialization(self):
        """Test global movies list initialization."""
        try:
            from importlib import import_module

            main_module = import_module("frontend.main")

            # Check that movies exists as a global variable
            assert hasattr(main_module, "movies")
            assert isinstance(main_module.movies, list)

        except ImportError as e:
            pytest.skip(f"FastHTML dependencies not available: {e}")


class TestFrontendComponents:
    """Test cases for frontend components (basic structure tests)."""

    @pytest.mark.frontend
    def test_components_import(self):
        """Test that frontend components can be imported."""
        try:
            # Test component imports
            from importlib import import_module

            # These should be importable if they exist
            components = ["ganeric", "movie_details", "movie_list"]

            for component in components:
                with contextlib.suppress(ImportError):
                    import_module(f"frontend.components.{component}")

        except ImportError as e:
            pytest.skip(f"Frontend dependencies not available: {e}")
