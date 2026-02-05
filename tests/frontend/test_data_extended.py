import pytest
from unittest.mock import patch, MagicMock, Mock
import requests
import sys
import os

# Add frontend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../frontend"))

from frontend.data import fetch_movies, fetch_comments, process_movies
from api.models import MovieQuery, CommentQuery


class TestDataModuleExtended:
    """Extended test cases for frontend data module covering edge cases and error scenarios."""

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_movies_with_all_query_parameters(self, mock_get):
        """Test fetch_movies with all possible query parameters."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "_id": "movie123",
                "title": "Test Movie",
                "plot": "Test plot",
                "genres": ["Action", "Drama"],
                "runtime": 120,
                "cast": ["Actor 1", "Actor 2"],
                "num_mflix_comments": 5,
                "poster": "http://example.com/poster.jpg",
                "countries": ["USA"],
                "released": "2023-01-01T00:00:00Z",
                "directors": ["Director 1"],
                "writers": ["Writer 1"],
                "awards": {"nominations": 1, "text": "Best Picture", "wins": 1},
                "lastupdated": "2023-01-01T00:00:00Z",
                "year": 2023,
                "type": "movie",
                "imdb": {"rating": 8.5, "votes": 10000},
                "tomatoes": {"viewer": {"rating": 4.2, "numReviews": 500}},
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch("data.config.API_URL", "http://test-api.com"):
            query = MovieQuery(
                id="movie123",
                title="Test Movie",
                genres=["Action", "Drama"],
                runtime=120,
                cast=["Actor 1", "Actor 2"],
                num_mflix_comments=5,
                type="movie",
                year=2023,
                limit=10,
                skip=0,
            )
            result = fetch_movies(query)

            assert len(result) == 1
            assert result[0]["title"] == "Test Movie"
            assert result[0]["type"] == "movie"

            # Verify the request was made with correct parameters
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert call_args[0][0] == "http://test-api.com/movies"
            assert "id=movie123" in call_args[1]["params"]
            assert "title=Test+Movie" in call_args[1]["params"]

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_comments_with_all_query_parameters(self, mock_get):
        """Test fetch_comments with all possible query parameters."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "_id": "comment123",
                "name": "Test User",
                "email": "test@example.com",
                "movie_id": "movie456",
                "text": "Great movie!",
                "date": "2023-01-15T10:30:00Z",
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch("data.config.API_URL", "http://test-api.com"):
            query = CommentQuery(
                id="comment123",
                name="Test User",
                email="test@example.com",
                movie_id="movie456",
                limit=20,
                skip=5,
            )
            result = fetch_comments(query)

            assert len(result) == 1
            assert result[0]["name"] == "Test User"
            assert result[0]["movie_id"] == "movie456"

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_movies_timeout_error(self, mock_get):
        """Test fetch_movies with timeout error."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        with patch("data.config.API_URL", "http://test-api.com"):
            result = fetch_movies(MovieQuery())
            assert result == []

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_movies_connection_error(self, mock_get):
        """Test fetch_movies with connection error."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        with patch("data.config.API_URL", "http://test-api.com"):
            result = fetch_movies(MovieQuery())
            assert result == []

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_movies_invalid_json_response(self, mock_get):
        """Test fetch_movies with invalid JSON response."""
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        with patch("data.config.API_URL", "http://test-api.com"):
            result = fetch_movies(MovieQuery())
            assert result == []

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_comments_with_special_characters(self, mock_get):
        """Test fetch_comments with special characters in parameters."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "_id": "comment123",
                "name": "José García",
                "email": "jose@example.com",
                "movie_id": "movie456",
                "text": "¡Excelente película!",
                "date": "2023-01-15T10:30:00Z",
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch("data.config.API_URL", "http://test-api.com"):
            query = CommentQuery(name="José García", movie_id="movie456")
            result = fetch_comments(query)

            assert len(result) == 1
            assert result[0]["name"] == "José García"

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_movies_empty_response(self, mock_get):
        """Test fetch_movies with empty response."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch("data.config.API_URL", "http://test-api.com"):
            result = fetch_movies(MovieQuery())
            assert result == []

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_movies_with_none_query(self, mock_get):
        """Test fetch_movies with None query (should use default)."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch("data.config.API_URL", "http://test-api.com"):
            result = fetch_movies()
            assert result == []
            mock_get.assert_called_once()

    @pytest.mark.frontend
    def test_process_movies_with_valid_posters(self):
        """Test process_movies with valid poster URLs."""
        movies = [
            {
                "_id": "1",
                "title": "Movie 1",
                "poster": "http://example.com/poster1.jpg",
                "plot": "Plot 1",
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
            },
            {
                "_id": "2",
                "title": "Movie 2",
                "poster": "https://example.com/poster2.jpg",
                "plot": "Plot 2",
                "genres": ["Action"],
                "runtime": 90,
                "cast": ["Actor 2"],
                "countries": ["UK"],
                "released": "2023-02-01T00:00:00Z",
                "directors": ["Director 2"],
                "awards": {"nominations": 0, "text": "N/A", "wins": 0},
                "lastupdated": "2023-02-01T00:00:00Z",
                "year": 2023,
                "type": "movie",
                "imdb": {"rating": 7.5, "votes": 500},
                "tomatoes": {"viewer": {"rating": 3.8, "numReviews": 200}},
            },
        ]

        with patch("data.requests.head") as mock_head:
            # Mock successful HEAD requests for valid posters
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_head.return_value = mock_response

            result = process_movies(movies)

            assert len(result) == 2
            assert result[0]["poster"] == "http://example.com/poster1.jpg"
            assert result[1]["poster"] == "https://example.com/poster2.jpg"
            assert mock_head.call_count == 2

    @pytest.mark.frontend
    def test_process_movies_with_invalid_posters(self):
        """Test process_movies with invalid poster URLs."""
        default_img = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg"
        movies = [
            {
                "_id": "1",
                "title": "Movie 1",
                "poster": "http://example.com/broken.jpg",  # Will return 404
                "plot": "Plot 1",
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
            },
            {
                "_id": "2",
                "title": "Movie 2",
                "poster": None,  # No poster
                "plot": "Plot 2",
                "genres": ["Action"],
                "runtime": 90,
                "cast": ["Actor 2"],
                "countries": ["UK"],
                "released": "2023-02-01T00:00:00Z",
                "directors": ["Director 2"],
                "awards": {"nominations": 0, "text": "N/A", "wins": 0},
                "lastupdated": "2023-02-01T00:00:00Z",
                "year": 2023,
                "type": "movie",
                "imdb": {"rating": 7.5, "votes": 500},
                "tomatoes": {"viewer": {"rating": 3.8, "numReviews": 200}},
            },
        ]

        with patch("data.requests.head") as mock_head:
            # Mock failed HEAD request for broken poster
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_head.return_value = mock_response

            result = process_movies(movies)

            assert len(result) == 2
            # Both should have default image
            assert result[0]["poster"] == default_img
            assert result[1]["poster"] == default_img

    @pytest.mark.frontend
    def test_process_movies_with_poster_request_exception(self):
        """Test process_movies when poster HEAD request raises exception."""
        default_img = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg"
        movies = [
            {
                "_id": "1",
                "title": "Movie 1",
                "poster": "http://example.com/error.jpg",
                "plot": "Plot 1",
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

        with patch("data.requests.head") as mock_head:
            # Mock exception during HEAD request
            mock_head.side_effect = requests.exceptions.ConnectionError("Network error")

            result = process_movies(movies)

            assert len(result) == 1
            # Should have default image due to exception
            assert result[0]["poster"] == default_img

    @pytest.mark.frontend
    def test_process_movies_with_redirect_response(self):
        """Test process_movies with redirect response for poster."""
        default_img = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg"
        movies = [
            {
                "_id": "1",
                "title": "Movie 1",
                "poster": "http://example.com/redirect.jpg",
                "plot": "Plot 1",
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

        with patch("data.requests.head") as mock_head:
            # Mock redirect response (not 200)
            mock_response = MagicMock()
            mock_response.status_code = 301
            mock_head.return_value = mock_response

            result = process_movies(movies)

            assert len(result) == 1
            # Should have default image due to redirect
            assert result[0]["poster"] == default_img

    @pytest.mark.frontend
    def test_process_movies_mixed_poster_scenarios(self):
        """Test process_movies with mixed poster scenarios."""
        default_img = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg"
        movies = [
            {
                "_id": "1",
                "title": "Movie 1",
                "poster": "http://example.com/valid.jpg",  # Valid
                "plot": "Plot 1",
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
            },
            {
                "_id": "2",
                "title": "Movie 2",
                "poster": None,  # No poster
                "plot": "Plot 2",
                "genres": ["Action"],
                "runtime": 90,
                "cast": ["Actor 2"],
                "countries": ["UK"],
                "released": "2023-02-01T00:00:00Z",
                "directors": ["Director 2"],
                "awards": {"nominations": 0, "text": "N/A", "wins": 0},
                "lastupdated": "2023-02-01T00:00:00Z",
                "year": 2023,
                "type": "movie",
                "imdb": {"rating": 7.5, "votes": 500},
                "tomatoes": {"viewer": {"rating": 3.8, "numReviews": 200}},
            },
            {
                "_id": "3",
                "title": "Movie 3",
                "poster": "",  # Empty string
                "plot": "Plot 3",
                "genres": ["Comedy"],
                "runtime": 100,
                "cast": ["Actor 3"],
                "countries": ["Canada"],
                "released": "2023-03-01T00:00:00Z",
                "directors": ["Director 3"],
                "awards": {"nominations": 0, "text": "N/A", "wins": 0},
                "lastupdated": "2023-03-01T00:00:00Z",
                "year": 2023,
                "type": "movie",
                "imdb": {"rating": 7.0, "votes": 200},
                "tomatoes": {"viewer": {"rating": 3.5, "numReviews": 150}},
            },
        ]

        with patch("data.requests.head") as mock_head:
            # Mock HEAD responses
            def mock_head_response(url, **kwargs):
                response = MagicMock()
                if url == "http://example.com/valid.jpg":
                    response.status_code = 200
                else:
                    response.status_code = 404
                return response

            mock_head.side_effect = mock_head_response

            result = process_movies(movies)

            assert len(result) == 3
            assert result[0]["poster"] == "http://example.com/valid.jpg"  # Valid
            assert result[1]["poster"] == default_img  # None -> default
            assert result[2]["poster"] == default_img  # Empty string -> default

    @pytest.mark.frontend
    def test_process_movies_preserves_other_fields(self):
        """Test process_movies preserves all other movie fields."""
        movies = [
            {
                "_id": "1",
                "title": "Original Title",
                "poster": "http://example.com/valid.jpg",
                "plot": "Original Plot",
                "genres": ["Drama", "Romance"],
                "runtime": 135,
                "cast": ["Actor 1", "Actress 2"],
                "countries": ["USA", "France"],
                "released": "2023-01-01T00:00:00Z",
                "directors": ["Director 1"],
                "writers": ["Writer 1", "Writer 2"],
                "awards": {"nominations": 5, "text": "Won 3 Oscars", "wins": 8},
                "lastupdated": "2023-01-01T00:00:00Z",
                "year": 2023,
                "type": "movie",
                "imdb": {"rating": 8.7, "votes": 15000},
                "tomatoes": {"viewer": {"rating": 4.3, "numReviews": 800}},
                "num_mflix_comments": 42,
                "fullplot": "Full plot details here...",
            }
        ]

        with patch("data.requests.head") as mock_head:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_head.return_value = mock_response

            result = process_movies(movies)

            assert len(result) == 1
            movie = result[0]

            # Check all fields are preserved
            assert movie["title"] == "Original Title"
            assert movie["plot"] == "Original Plot"
            assert movie["genres"] == ["Drama", "Romance"]
            assert movie["runtime"] == 135
            assert movie["cast"] == ["Actor 1", "Actress 2"]
            assert movie["countries"] == ["USA", "France"]
            assert movie["directors"] == ["Director 1"]
            assert movie["writers"] == ["Writer 1", "Writer 2"]
            assert movie["awards"]["nominations"] == 5
            assert movie["year"] == 2023
            assert movie["type"] == "movie"
            assert movie["imdb"]["rating"] == 8.7
            assert movie["tomatoes"]["viewer"]["rating"] == 4.3
            assert movie["num_mflix_comments"] == 42
            assert movie["fullplot"] == "Full plot details here..."

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_comments_with_api_error_response(self, mock_get):
        """Test fetch_comments with API error response but valid JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_get.return_value = mock_response

        with patch("data.config.API_URL", "http://test-api.com"):
            result = fetch_comments(CommentQuery())
            assert result == {}

    @pytest.mark.frontend
    @patch("data.requests.get")
    def test_fetch_movies_with_unicode_in_title(self, mock_get):
        """Test fetch_movies with unicode characters in movie title."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "_id": "movie123",
                "title": "El Niño y la Guerra",
                "plot": "Una historia sobre la vida...",
                "genres": ["Drama"],
                "runtime": 120,
                "cast": ["Actor 1"],
                "countries": ["España"],
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

        with patch("data.config.API_URL", "http://test-api.com"):
            query = MovieQuery(title="El Niño y la Guerra")
            result = fetch_movies(query)

            assert len(result) == 1
            assert result[0]["title"] == "El Niño y la Guerra"
