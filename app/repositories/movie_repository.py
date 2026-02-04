"""
Movie Repository layer using context manager pattern.
"""

from typing import Dict, Any, List, Optional
from bson import ObjectId
from .base import BaseRepository
from app.core.logging import get_logger
from app.schemas.movie import MovieResponse

logger = get_logger(__name__)


# TODO: Create helper method to keep track of faulty movie records
class MovieRepository(BaseRepository):
    """Repository for movie data operations."""

    def __init__(self) -> None:
        super().__init__("sample_mflix", "movies")

    async def find_by_id(
        self, entity_id: str, id_field: str = "_id", **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Find a movie by its ID."""
        logger.debug(
            f"MovieRepository.find_by_id() called with entity_id={entity_id}, id_field={id_field}"
        )
        return await super().find_by_id(entity_id, id_field, **kwargs)

    async def find_by_title(self, title: str, **kwargs) -> List[Dict[str, Any]]:
        """Find movies by title (exact match)."""
        logger.debug(f"MovieRepository.find_by_title() called with title={title}")
        filter_query = {"title": title}
        return await self.find_many(filter_query, **kwargs)

    async def find_by_type(self, movie_type: str, **kwargs) -> List[Dict[str, Any]]:
        """Find movies by type (e.g., 'movie', 'series')."""
        logger.debug(
            f"MovieRepository.find_by_type() called with movie_type={movie_type}"
        )
        filter_query = {"type": movie_type}
        return await self.find_many(filter_query, **kwargs)

    async def find_by_genre(self, genre: str, **kwargs) -> List[Dict[str, Any]]:
        """Find movies by genre."""
        logger.debug(
            f"MovieRepository.find_by_genre() called with genre={genre}, kwargs={kwargs}"
        )
        filter_query = {"genres": {"$in": [genre]}}
        return await self.find_many(filter_query, **kwargs)

    async def find_by_year(self, year: int, **kwargs) -> List[Dict[str, Any]]:
        """Find movies by release year."""
        logger.debug(
            f"MovieRepository.find_by_year() called with year={year}, kwargs={kwargs}"
        )
        filter_query = {"year": year}
        return await self.find_many(filter_query, **kwargs)

    async def search_movies(self, **kwargs) -> List[MovieResponse]:
        """Search movies with multiple filters."""
        logger.debug(f"MovieRepository.search_movies() called with kwargs: {kwargs}")
        filter_query = {}

        if kwargs.get("movie_id", None):
            try:
                filter_query["_id"] = ObjectId(kwargs["movie_id"])
                logger.debug(f"Added movie_id filter: {kwargs['movie_id']}")
            except Exception as e:
                logger.warning(
                    f"Failed to convert movie_id to ObjectId: {kwargs.get('movie_id')}, error: {e}"
                )

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

        limit = kwargs.get("limit", 10)
        skip = kwargs.get("skip", 0)
        logger.debug(
            f"Final filter_query: {filter_query}, limit: {limit}, skip: {skip}"
        )
        movies = await self.find_many(filter_query, limit=limit, skip=skip)
        return [MovieResponse.from_dict(movie) for movie in movies]

    async def get_genres(self) -> List[str]:
        """Get all unique values in a field in movies."""
        logger.debug("MovieRepository.get_genres() called - Getting all movie genres")
        values = await self.find_distinct("gerne")
        logger.debug(f"MovieRepository.get_genres() found {len(values)} genres")
        return values
