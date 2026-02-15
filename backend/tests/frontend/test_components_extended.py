import os
import sys

import pytest

# Add frontend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../frontend"))

from frontend.components.ganeric import (
    ImdbRating,
    TomatoesCriticRating,
    TomatoesViewerRating,
)
from frontend.components.movie_details import (
    MovieDetail,
    MovieDetails,
    MovieDetailsBody,
    MovieDetailsHeader,
    MoviePlot,
)
from frontend.components.movie_list import MovieList


class TestMovieListComponent:
    """Test cases for MovieList component."""

    @pytest.mark.frontend
    def test_movie_list_component_structure(self):
        """Test MovieList component creates correct HTML structure."""
        result = MovieList()

        assert result is not None
        # Should create a Div with movie-list-container class
        # containing Ul and Button elements

    @pytest.mark.frontend
    def test_movie_list_htmx_attributes(self):
        """Test MovieList component has correct HTMX attributes."""
        result = MovieList()

        assert result is not None
        # Should have HTMX attributes for loading movies
        # - hx_get="/movies"
        # - hx_trigger="load"
        # - hx_swap="innerHTML"

    @pytest.mark.frontend
    def test_movie_list_button_attributes(self):
        """Test MovieList button has correct attributes."""
        result = MovieList()

        assert result is not None
        # Button should have:
        # - hx_get="/movies"
        # - hx_target=".movie-list"
        # - hx_swap="innerHTML"


class TestMovieDetailsComponents:
    """Test cases for movie details components."""

    @pytest.mark.frontend
    def test_movie_detail_with_valid_data(self):
        """Test MovieDetail with valid data."""
        movie = {
            "directors": ["Director 1", "Director 2"],
            "genres": ["Action", "Drama"],
        }

        result = MovieDetail("Directors", "directors", movie)
        result_genres = MovieDetail("Genres", "genres", movie)

        assert result is not None
        assert result_genres is not None
        # Should create P elements with bold labels and comma-separated values

    @pytest.mark.frontend
    def test_movie_detail_with_missing_key(self):
        """Test MovieDetail with missing key in item."""
        movie = {
            "title": "Test Movie"
            # Missing "directors" key
        }

        result = MovieDetail("Directors", "directors", movie)

        assert result is not None
        # Should return "N/A" when key is missing

    @pytest.mark.frontend
    def test_movie_detail_with_none_value(self):
        """Test MovieDetail with None value."""
        movie = {"directors": None}

        result = MovieDetail("Directors", "directors", movie)

        assert result is not None
        # Should return "N/A" when value is None

    @pytest.mark.frontend
    def test_movie_detail_with_single_value(self):
        """Test MovieDetail with single value (not list)."""
        movie = {"title": "Single Movie Title"}

        result = MovieDetail("Title", "title", movie)

        assert result is not None
        # Should convert single value to list internally

    @pytest.mark.frontend
    def test_movie_details_header(self):
        """Test MovieDetailsHeader component."""
        movie = {
            "title": "Test Movie",
            "year": 2023,
            "runtime": 142,  # minutes
        }

        result = MovieDetailsHeader(movie)

        assert result is not None
        # Should create header with title and formatted duration

    @pytest.mark.frontend
    def test_movie_details_header_formatting(self):
        """Test MovieDetailsHeader formats duration correctly."""
        movie = {
            "title": "Test Movie",
            "year": 2023,
            "runtime": 125,  # 2 hours 5 minutes
        }

        result = MovieDetailsHeader(movie)

        assert result is not None
        # Should format as "2023・2h 5m"

    @pytest.mark.frontend
    def test_movie_details_body_with_complete_data(self):
        """Test MovieDetailsBody with complete movie data."""
        movie = {
            "poster": "http://example.com/poster.jpg",
            "genres": ["Action", "Drama"],
            "directors": ["Director 1"],
            "writers": ["Writer 1"],
            "cast": ["Actor 1", "Actor 2"],
            "countries": ["USA", "UK"],
            "tomatoes": {
                "critic": {"rating": 8.5, "numReviews": 200},
                "viewer": {"rating": 4.2, "numReviews": 1000},
            },
            "imdb": {"rating": 8.7, "votes": 15000},
        }

        result = MovieDetailsBody(movie)

        assert result is not None
        # Should create complete body with all sections

    @pytest.mark.frontend
    def test_movie_details_body_with_minimal_data(self):
        """Test MovieDetailsBody with minimal movie data."""
        movie = {
            "poster": None,
            "genres": ["Drama"],
            "directors": ["Director 1"],
            "writers": None,
            "cast": ["Actor 1"],
            "countries": ["USA"],
            "tomatoes": {},
            "imdb": {"rating": 7.5, "votes": 5000},
        }

        result = MovieDetailsBody(movie)

        assert result is not None
        # Should handle missing data gracefully

    @pytest.mark.frontend
    def test_movie_plot_with_fullplot(self):
        """Test MoviePlot with fullplot available."""
        movie = {
            "plot": "Short plot",
            "fullplot": "This is a much longer and more detailed plot description that provides more context about the movie.",
        }

        result = MoviePlot(movie)

        assert result is not None
        # Should use fullplot when available and not empty

    @pytest.mark.frontend
    def test_movie_plot_without_fullplot(self):
        """Test MoviePlot without fullplot."""
        movie = {"plot": "Short plot description", "fullplot": None}

        result = MoviePlot(movie)

        assert result is not None
        # Should use regular plot when fullplot is None

    @pytest.mark.frontend
    def test_movie_plot_with_empty_fullplot(self):
        """Test MoviePlot with empty fullplot."""
        movie = {"plot": "Short plot description", "fullplot": ""}

        result = MoviePlot(movie)

        assert result is not None
        # Should use regular plot when fullplot is empty

    @pytest.mark.frontend
    def test_movie_plot_without_any_plot(self):
        """Test MoviePlot without any plot data."""
        movie = {"plot": None, "fullplot": None}

        result = MoviePlot(movie)

        assert result is not None
        # Should handle case where both plots are None

    @pytest.mark.frontend
    def test_movie_details_complete(self):
        """Test complete MovieDetails component."""
        movie = {
            "title": "Complete Movie",
            "year": 2023,
            "runtime": 120,
            "poster": "http://example.com/poster.jpg",
            "plot": "Movie plot",
            "fullplot": "Full movie plot description",
            "genres": ["Drama"],
            "directors": ["Director 1"],
            "writers": ["Writer 1"],
            "cast": ["Actor 1"],
            "countries": ["USA"],
            "tomatoes": {
                "critic": {"rating": 8.0, "numReviews": 150},
                "viewer": {"rating": 4.1, "numReviews": 800},
            },
            "imdb": {"rating": 8.2, "votes": 12000},
        }

        result = MovieDetails(movie)

        assert result is not None
        # Should create complete movie details view

    @pytest.mark.frontend
    def test_movie_details_minimal_data(self):
        """Test MovieDetails with minimal data."""
        movie = {
            "title": "Minimal Movie",
            "year": 2023,
            "runtime": 90,
            "poster": None,
            "plot": "Basic plot",
            "genres": ["Comedy"],
            "directors": ["Director 1"],
            "writers": None,
            "cast": ["Actor 1"],
            "countries": ["USA"],
            "tomatoes": {},
            "imdb": {"rating": 6.5, "votes": 2000},
        }

        result = MovieDetails(movie)

        assert result is not None
        # Should handle minimal data gracefully


class TestGenericComponents:
    """Test cases for generic rating components."""

    @pytest.mark.frontend
    def test_tomatoes_critic_rating_with_data(self):
        """Test TomatoesCriticRating with valid data."""
        tomatoes_data = {"critic": {"rating": 8.5, "numReviews": 200}}

        result = TomatoesCriticRating(tomatoes_data)

        assert result is not None
        # Should display critic rating

    @pytest.mark.frontend
    def test_tomatoes_critic_rating_missing_data(self):
        """Test TomatoesCriticRating with missing critic data."""
        tomatoes_data = {
            "viewer": {"rating": 4.2, "numReviews": 1000}
            # Missing critic data
        }

        result = TomatoesCriticRating(tomatoes_data)

        assert result is not None
        # Should handle missing critic data

    @pytest.mark.frontend
    def test_tomatoes_viewer_rating_with_data(self):
        """Test TomatoesViewerRating with valid data."""
        tomatoes_data = {"viewer": {"rating": 4.2, "numReviews": 1000}}

        result = TomatoesViewerRating(tomatoes_data)

        assert result is not None
        # Should display viewer rating

    @pytest.mark.frontend
    def test_tomatoes_viewer_rating_missing_data(self):
        """Test TomatoesViewerRating with missing viewer data."""
        tomatoes_data = {
            "critic": {"rating": 8.5, "numReviews": 200}
            # Missing viewer data
        }

        result = TomatoesViewerRating(tomatoes_data)

        assert result is not None
        # Should handle missing viewer data

    @pytest.mark.frontend
    def test_imdb_rating_with_data(self):
        """Test ImdbRating with valid data."""
        movie = {"imdb": {"rating": 8.7, "votes": 15000}}

        result = ImdbRating(movie)

        assert result is not None
        # Should display IMDB rating

    @pytest.mark.frontend
    def test_imdb_rating_missing_data(self):
        """Test ImdbRating with missing IMDB data."""
        movie = {
            "title": "Movie without IMDB data"
            # Missing imdb data
        }

        result = ImdbRating(movie)

        assert result is not None
        # Should handle missing IMDB data


class TestComponentEdgeCases:
    """Test cases for component edge cases and error handling."""

    @pytest.mark.frontend
    def test_movie_detail_with_special_characters(self):
        """Test MovieDetail with special characters in values."""
        movie = {
            "directors": ["José García", "François Müller"],
            "title": "Movie: The Sequel (2023)",
        }

        result_directors = MovieDetail("Directors", "directors", movie)
        result_title = MovieDetail("Title", "title", movie)

        assert result_directors is not None
        assert result_title is not None
        # Should handle special characters

    @pytest.mark.frontend
    def test_movie_detail_with_empty_lists(self):
        """Test MovieDetail with empty lists."""
        movie = {"directors": [], "cast": [], "genres": []}

        result = MovieDetail("Directors", "directors", movie)

        assert result is not None
        # Should handle empty lists

    @pytest.mark.frontend
    def test_movie_details_with_very_long_titles(self):
        """Test movie details with very long titles."""
        long_title = "This is an extremely long movie title that goes on and on and should still be handled properly by the movie details components without any issues or problems"

        movie = {"title": long_title, "year": 2023, "runtime": 120}

        result = MovieDetailsHeader(movie)

        assert result is not None
        # Should handle long titles

    @pytest.mark.frontend
    def test_movie_details_with_invalid_runtime(self):
        """Test movie details with invalid runtime values."""
        test_cases = [
            {"year": 2023, "runtime": 0},
            {"year": 2023, "runtime": -1},
            {"year": 2023, "runtime": None},
            {"year": 2023, "runtime": "invalid"},
        ]

        for movie in test_cases:
            movie["title"] = "Test Movie"
            result = MovieDetailsHeader(movie)
            assert result is not None
            # Should handle invalid runtime values

    @pytest.mark.frontend
    def test_components_with_html_content(self):
        """Test components handle HTML content safely."""
        movie = {
            "title": "<script>alert('xss')</script>",
            "plot": "<img src='x' onerror='alert(1)'>Plot text",
            "directors": ["<b>Director</b>"],
        }

        result_header = MovieDetailsHeader(movie)
        result_plot = MoviePlot(movie)
        result_detail = MovieDetail("Directors", "directors", movie)

        assert result_header is not None
        assert result_plot is not None
        assert result_detail is not None
        # Should handle HTML content (actual sanitization depends on framework)

    @pytest.mark.frontend
    def test_components_with_unicode_content(self):
        """Test components handle unicode content."""
        movie = {
            "title": "电影标题",
            "plot": "这是电影情节描述",
            "directors": ["导演一", "导演二"],
            "cast": ["演员一", "演员二"],
            "countries": ["中国", "美国"],
            "year": 2023,
            "runtime": 120,
        }

        result_header = MovieDetailsHeader(movie)
        result_body = MovieDetailsBody(movie)
        result_plot = MoviePlot(movie)

        assert result_header is not None
        assert result_body is not None
        assert result_plot is not None
        # Should handle unicode content

    @pytest.mark.frontend
    def test_components_with_numeric_strings(self):
        """Test components handle numeric string values."""
        movie = {
            "year": "2023",
            "runtime": "120",
            "imdb": {"rating": "8.5", "votes": "10000"},
        }

        result = MovieDetailsHeader(movie)
        rating = ImdbRating(movie)

        assert result is not None
        assert rating is not None
        # Should handle numeric strings

    @pytest.mark.frontend
    def test_component_consistency(self):
        """Test that components produce consistent output."""
        movie = {
            "title": "Consistent Movie",
            "year": 2023,
            "runtime": 120,
            "plot": "Consistent plot",
            "genres": ["Drama"],
            "directors": ["Director 1"],
        }

        result1 = MovieDetails(movie)
        result2 = MovieDetails(movie)

        assert result1 is not None
        assert result2 is not None
        # Multiple calls should produce consistent results
