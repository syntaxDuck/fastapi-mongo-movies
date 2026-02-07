"""
Movie Repository layer using context manager pattern.
"""

from typing import Dict, Any, List, Optional
from .base import BaseRepository
from app.core.logging import get_logger
from app.schemas.schemas import MovieResponse

logger = get_logger(__name__)


# TODO: Create helper method to keep track of faulty movie records
class MovieRepository(BaseRepository):
    """Repository for movie data operations."""

    def __init__(self) -> None:
        super().__init__("sample_mflix", "movies")

    def _add_valid_poster_filter(
        self, filter_query: Dict[str, Any], include_invalid_posters: bool = False
    ) -> Dict[str, Any]:
        """Add valid_poster filter to ensure only movies with valid posters are returned."""
        if not include_invalid_posters:
            filter_query["valid_poster"] = True
            logger.debug("Added valid_poster=true filter to query")
        else:
            logger.debug("Skipping valid_poster filter - including all movies")
        return filter_query

    async def find_by_id(self, id: str, **kwargs) -> Optional[MovieResponse]:
        """Find a movie by its ID."""
        logger.debug(
            f"MovieRepository.find_by_id() called with id={id}, kwargs={kwargs}"
        )
        movie = await self._find_by_id(id, **kwargs)
        if movie:
            logger.debug(
                f"MovieRepository.find_by_id() found movie: {movie.get('title', 'Unknown')} ({movie.get('_id', 'Unknown ID')})"
            )
        else:
            logger.debug(f"MovieRepository.find_by_id() no movie found with id={id}")
        return MovieResponse.from_dict(movie) if movie else None

    async def find_by_title(
        self, title: str, include_invalid_posters: bool = False, **kwargs
    ) -> List[MovieResponse]:
        """Find movies by title (exact match)."""
        logger.debug(
            f"MovieRepository.find_by_title() called with title='{title}', include_invalid_posters={include_invalid_posters}, kwargs={kwargs}"
        )
        filter_query = {"title": title}
        filter_query = self._add_valid_poster_filter(
            filter_query, include_invalid_posters
        )
        logger.debug(f"MovieRepository.find_by_title() executing query: {filter_query}")
        movies = await self._find_many(filter_query, **kwargs)
        logger.debug(
            f"MovieRepository.find_by_title() found {len(movies)} movies with title '{title}'"
        )
        return [MovieResponse.from_dict(movie) for movie in movies]

    async def find_by_type(
        self, type: str, include_invalid_posters: bool = False, **kwargs
    ) -> List[MovieResponse]:
        """Find movies by type (e.g., 'movie', 'series')."""
        logger.debug(
            f"MovieRepository.find_by_type() called with type='{type}', include_invalid_posters={include_invalid_posters}, kwargs={kwargs}"
        )
        filter_query = {"type": type}
        filter_query = self._add_valid_poster_filter(
            filter_query, include_invalid_posters
        )
        logger.debug(f"MovieRepository.find_by_type() executing query: {filter_query}")
        movies = await self._find_many(filter_query, **kwargs)
        logger.debug(
            f"MovieRepository.find_by_type() found {len(movies)} movies of type '{type}'"
        )
        return [MovieResponse.from_dict(movie) for movie in movies]

    async def find_by_genre(
        self, genre: str, include_invalid_posters: bool = False, **kwargs
    ) -> List[MovieResponse]:
        """Find movies by genre."""
        logger.debug(
            f"MovieRepository.find_by_genre() called with genre='{genre}', include_invalid_posters={include_invalid_posters}, kwargs={kwargs}"
        )
        filter_query = {"genres": {"$in": [genre]}}
        filter_query = self._add_valid_poster_filter(
            filter_query, include_invalid_posters
        )
        logger.debug(f"MovieRepository.find_by_genre() executing query: {filter_query}")
        movies = await self._find_many(filter_query, **kwargs)
        logger.debug(
            f"MovieRepository.find_by_genre() found {len(movies)} movies in genre '{genre}'"
        )
        return [MovieResponse.from_dict(movie) for movie in movies]

    async def find_by_year(
        self, year: int, include_invalid_posters: bool = False, **kwargs
    ) -> List[MovieResponse]:
        """Find movies by release year."""
        logger.debug(
            f"MovieRepository.find_by_year() called with year={year}, include_invalid_posters={include_invalid_posters}, kwargs={kwargs}"
        )
        filter_query = {"year": year}
        filter_query = self._add_valid_poster_filter(
            filter_query, include_invalid_posters
        )
        logger.debug(f"MovieRepository.find_by_year() executing query: {filter_query}")
        movies = await self._find_many(filter_query, **kwargs)
        logger.debug(
            f"MovieRepository.find_by_year() found {len(movies)} movies from year {year}"
        )
        return [MovieResponse.from_dict(movie) for movie in movies]

    async def search_movies(self, **kwargs) -> List[MovieResponse]:
        """Search movies with multiple filters."""
        logger.debug(f"MovieRepository.search_movies() called with kwargs: {kwargs}")
        filter_query = {}

        if kwargs.get("movie_id", None):
            filter_query["id"] = kwargs["movie_id"]
            logger.debug(f"Added movie_id filter: {kwargs['movie_id']}")

        if kwargs.get("title", None):
            filter_query["title"] = kwargs["title"]
            logger.debug(f"Added title filter: {kwargs['title']}")

        if kwargs.get("movie_type", None):
            filter_query["type"] = kwargs["movie_type"]
            logger.debug(f"Added movie_type filter: {kwargs['movie_type']}")

        if kwargs.get("genres", None):
            filter_query["genres"] = {"$in": kwargs["genres"]}
            logger.debug(f"Added genres filter: {kwargs['genres']}")

        if kwargs.get("year", None):
            filter_query["year"] = kwargs["year"]
            logger.debug(f"Added year filter: {kwargs['year']}")

        include_invalid_posters = kwargs.pop("include_invalid_posters", False)
        filter_query = self._add_valid_poster_filter(
            filter_query, include_invalid_posters
        )

        limit = kwargs.get("limit", 10)
        skip = kwargs.get("skip", 0)
        logger.debug(
            f"MovieRepository.search_movies() executing query: {filter_query}, limit: {limit}, skip: {skip}"
        )
        movies = await self._find_many(filter_query, limit=limit, skip=skip)
        logger.debug(
            f"MovieRepository.search_movies() found {len(movies)} movies matching search criteria"
        )
        return [MovieResponse.from_dict(movie) for movie in movies]

    async def get_all_genres(self) -> List[str]:
        """Get all unique values in a field in movies."""
        logger.debug("MovieRepository.get_genres() called - Getting all movie genres")
        values = await self._find_distinct("genres")
        logger.debug(f"MovieRepository.get_genres() found {len(values)} genres")
        return values

    async def get_all_types(self) -> List[str]:
        """Get all unique values in a field in movies."""
        logger.debug("MovieRepository.get_types() called - Getting all movie types")
        values = await self._find_distinct("types")
        logger.debug(f"MovieRepository.get_types() found {len(values)} types")
        return values

    async def search_movies_by_text(
        self, search_text: str, include_invalid_posters: bool = False, **kwargs
    ) -> List[MovieResponse]:
        """Search movies by text in title, plot, and other fields."""
        logger.debug(
            f"MovieRepository.search_movies_by_text() called with search_text='{search_text}', include_invalid_posters={include_invalid_posters}, kwargs={kwargs}"
        )

        filter_query = {"$text": {"$search": search_text, "$caseSensitive": False}}

        filter_query = self._add_valid_poster_filter(
            filter_query, include_invalid_posters
        )

        limit = kwargs.get("limit", 10)
        skip = kwargs.get("skip", 0)
        logger.debug(
            f"MovieRepository.search_movies_by_text() executing text search query: {filter_query}, limit: {limit}, skip: {skip}"
        )

        movies = await self._find_many(filter_query, limit=limit, skip=skip)
        logger.debug(
            f"MovieRepository.search_movies_by_text() found {len(movies)} movies matching text search '{search_text}'"
        )
        return [MovieResponse.from_dict(movie) for movie in movies]
