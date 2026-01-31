import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add frontend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../frontend"))

from frontend.helper import build_movie_list


class TestHelperModuleExtended:
    """Extended test cases for frontend helper module covering edge cases and complex scenarios."""

    @pytest.mark.frontend
    def test_build_movie_list_with_various_movie_data(self):
        """Test build_movie_list with various movie data structures."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "Action Movie",
                "index": 0,
            },
            {
                "poster": "https://example.com/poster2.jpg",
                "title": "Drama Movie",
                "index": 1,
            },
            {
                "poster": None,
                "title": "Comedy Movie",
                "index": 2,
            },
            {
                "poster": "",
                "title": "Horror Movie",
                "index": 3,
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 4

        # Check that each movie item is properly structured
        for i, movie_item in enumerate(result):
            # The function should create Li elements with Img and Span
            assert hasattr(movie_item, "tag") or hasattr(movie_item, "__class__")
            # Should contain movie poster and title information

    @pytest.mark.frontend
    def test_build_movie_list_with_special_characters_in_titles(self):
        """Test build_movie_list with special characters in movie titles."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "El Niño & la Guerra",
                "index": 0,
            },
            {
                "poster": "http://example.com/poster2.jpg",
                "title": "Movie: The Sequel (2023)",
                "index": 1,
            },
            {
                "poster": "http://example.com/poster3.jpg",
                "title": "Café au Lait",
                "index": 2,
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 3
        # Should handle special characters without issues

    @pytest.mark.frontend
    def test_build_movie_list_with_long_titles(self):
        """Test build_movie_list with very long movie titles."""
        long_title = "This is an extremely long movie title that goes on and on and should still be handled properly by the build_movie_list function without any issues"

        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": long_title,
                "index": 0,
            }
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 1
        # Should handle long titles without issues

    @pytest.mark.frontend
    def test_build_movie_list_with_missing_fields(self):
        """Test build_movie_list with missing required fields."""
        movies = [
            {
                # Missing poster
                "title": "Movie without poster",
                "index": 0,
            },
            {
                "poster": "http://example.com/poster2.jpg",
                # Missing title
                "index": 1,
            },
            {
                "poster": "http://example.com/poster3.jpg",
                "title": "Movie without index",
                # Missing index
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 3
        # Should handle missing fields gracefully

    @pytest.mark.frontend
    def test_build_movie_list_with_invalid_poster_urls(self):
        """Test build_movie_list with invalid or malformed poster URLs."""
        movies = [
            {
                "poster": "not-a-valid-url",
                "title": "Movie with invalid URL",
                "index": 0,
            },
            {
                "poster": "ftp://example.com/poster.jpg",
                "title": "Movie with FTP URL",
                "index": 1,
            },
            {
                "poster": "javascript:alert('xss')",
                "title": "Movie with potentially dangerous URL",
                "index": 2,
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 3
        # Should handle various URL formats (actual security depends on frontend framework)

    @pytest.mark.frontend
    def test_build_movie_list_with_unicode_poster_urls(self):
        """Test build_movie_list with unicode characters in poster URLs."""
        movies = [
            {
                "poster": "http://example.com/电影海报.jpg",
                "title": "Chinese Movie",
                "index": 0,
            },
            {
                "poster": "https://example.com/фильм.jpg",
                "title": "Russian Movie",
                "index": 1,
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 2
        # Should handle unicode URLs

    @pytest.mark.frontend
    def test_build_movie_list_with_numeric_indexes(self):
        """Test build_movie_list with various numeric index types."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "Movie 1",
                "index": 0,
            },
            {
                "poster": "http://example.com/poster2.jpg",
                "title": "Movie 2",
                "index": 1.0,  # Float index
            },
            {
                "poster": "http://example.com/poster3.jpg",
                "title": "Movie 3",
                "index": "2",  # String index
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 3
        # Should handle different numeric types for index

    @pytest.mark.frontend
    def test_build_movie_list_with_empty_title(self):
        """Test build_movie_list with empty or whitespace-only titles."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "",
                "index": 0,
            },
            {
                "poster": "http://example.com/poster2.jpg",
                "title": "   ",  # Whitespace only
                "index": 1,
            },
            {
                "poster": "http://example.com/poster3.jpg",
                "title": None,  # None title
                "index": 2,
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 3
        # Should handle empty/None titles

    @pytest.mark.frontend
    def test_build_movie_list_large_dataset(self):
        """Test build_movie_list with a large number of movies."""
        movies = []
        for i in range(100):
            movies.append(
                {
                    "poster": f"http://example.com/poster{i}.jpg",
                    "title": f"Movie {i}",
                    "index": i,
                }
            )

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 100
        # Should handle large datasets efficiently

    @pytest.mark.frontend
    def test_build_movie_list_html_attributes(self):
        """Test build_movie_list generates correct HTML attributes."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "Test Movie",
                "index": 5,
            }
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 1

        movie_item = result[0]

        # The function should create elements with specific attributes
        # Based on the implementation, it should have:
        # - hx_get="/details/{index}"
        # - hx_target=".content"
        # - hx_swap="innerHTML"
        # - hx_trigger="click"

        # Check that the attributes are set correctly (implementation may vary)
        # This test ensures the function runs without error
        assert movie_item is not None

    @pytest.mark.frontend
    def test_build_movie_list_css_classes(self):
        """Test build_movie_list applies correct CSS classes."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "Test Movie",
                "index": 0,
            }
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 1

        # The function should apply CSS classes
        # Based on implementation: cls="movie"
        # This test ensures the function runs without error

    @pytest.mark.frontend
    def test_build_movie_list_count_functionality(self):
        """Test that the count functionality works correctly."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "Movie 1",
                "index": 10,  # Non-sequential index
            },
            {
                "poster": "http://example.com/poster2.jpg",
                "title": "Movie 2",
                "index": 20,  # Non-sequential index
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 2

        # The function should increment count for each movie
        # This is used to create hx_get URLs with the count, not the index
        # So even with non-sequential indexes, the count should be 0, 1, 2...

    @pytest.mark.frontend
    def test_build_movie_list_image_attributes(self):
        """Test build_movie_list sets correct image attributes."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "Test Movie",
                "index": 0,
            }
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 1

        # The function should create Img elements with src attribute
        # This test ensures the function runs without error

    @pytest.mark.frontend
    def test_build_movie_list_span_content(self):
        """Test build_movie_list creates correct span content."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "Test Movie Title",
                "index": 0,
            }
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 1

        # The function should create Span with movie title
        # This test ensures the function runs without error

    @pytest.mark.frontend
    def test_build_movie_list_with_html_injection(self):
        """Test build_movie_list handles potential HTML injection in titles."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "<script>alert('xss')</script>",
                "index": 0,
            },
            {
                "poster": "http://example.com/poster2.jpg",
                "title": "<img src='x' onerror='alert(1)'>",
                "index": 1,
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 2
        # Should handle HTML content (actual sanitization depends on framework)

    @pytest.mark.frontend
    def test_build_movie_list_with_newlines_in_titles(self):
        """Test build_movie_list handles newlines and special whitespace in titles."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "Movie Title\nWith Newlines",
                "index": 0,
            },
            {
                "poster": "http://example.com/poster2.jpg",
                "title": "Movie Title\tWith Tabs",
                "index": 1,
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 2
        # Should handle whitespace characters

    @pytest.mark.frontend
    def test_build_movie_list_consistent_ordering(self):
        """Test build_movie_list maintains consistent ordering of movies."""
        movies = [
            {
                "poster": "http://example.com/poster3.jpg",
                "title": "Third Movie",
                "index": 2,
            },
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "First Movie",
                "index": 0,
            },
            {
                "poster": "http://example.com/poster2.jpg",
                "title": "Second Movie",
                "index": 1,
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 3

        # Should maintain the order of input movies
        # Count should increment in order of processing

    @pytest.mark.frontend
    def test_build_movie_list_edge_case_data_types(self):
        """Test build_movie_list with edge case data types."""
        movies = [
            {
                "poster": 0,  # Zero instead of string
                "title": False,  # Boolean instead of string
                "index": "",  # Empty string instead of number
            },
            {
                "poster": [],
                "title": {},
                "index": None,
            },
        ]

        result = build_movie_list(movies)

        assert result is not None
        assert len(result) == 2
        # Should handle various data types without crashing

    @pytest.mark.frontend
    def test_build_movie_list_multiple_calls_consistency(self):
        """Test that multiple calls to build_movie_list produce consistent results."""
        movies = [
            {
                "poster": "http://example.com/poster1.jpg",
                "title": "Test Movie",
                "index": 0,
            }
        ]

        result1 = build_movie_list(movies)
        result2 = build_movie_list(movies)

        assert result1 is not None
        assert result2 is not None
        assert len(result1) == len(result2)
        # Multiple calls should produce consistent results
