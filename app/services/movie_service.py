"""
Movie Service layer for business logic using proper protocol-based dependency injection.
"""

from typing import List, Optional, Dict, Any
from ..repositories.protocol import MovieRepositoryProtocol
from ..core.exceptions import NotFoundError
from ..core.logging import get_logger

logger = get_logger(__name__)


class MovieService:
    """Service layer for movie business logic."""

    def __init__(self, movie_repository: MovieRepositoryProtocol) -> None:
        self.movie_repository = movie_repository

    async def get_movie_by_id(self, movie_id: str) -> Dict[str, Any]:
        """Get a movie by its ID."""
        logger.debug(f"Getting movie by ID: {movie_id}")

        movie = await self.movie_repository.find_by_id(movie_id)
        if not movie:
            logger.warning(f"Movie not found: {movie_id}")
            raise NotFoundError(f"Movie with ID {movie_id} not found")

        logger.debug(f"Successfully retrieved movie: {movie_id}")
        return movie

    async def get_movies(
        self,
        movie_id: Optional[str] = None,
        title: Optional[str] = None,
        movie_type: Optional[str] = None,
        genres: Optional[List[str]] = None,
        year: Optional[int] = None,
        limit: int = 10,
        skip: int = 0,
    ) -> List[Dict[str, Any]]:
        """Get movies with optional filtering."""
        logger.debug(
            f"Getting movies with filters: movie_id={movie_id}, title={title}, "
            f"type={movie_type}, genres={genres}, year={year}, limit={limit}, skip={skip}"
        )

        movies = await self.movie_repository.search_movies(
            movie_id=movie_id,
            title=title,
            movie_type=movie_type,
            genres=genres,
            year=year,
            limit=limit,
            skip=skip,
        )

        if not movies:
            logger.info("No movies found matching the criteria")
            raise NotFoundError("No movies found matching the criteria")

        logger.info(f"Found {len(movies)} movies")
        return movies

    async def get_movies_by_type(
        self, movie_type: str, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get movies by type."""
        logger.debug(
            f"Getting movies by type: {movie_type}, limit={limit}, skip={skip}"
        )

        movies = await self.movie_repository.find_by_type(
            movie_type, limit=limit, skip=skip
        )
        if not movies:
            logger.info(f"No movies found of type: {movie_type}")
            raise NotFoundError(f"No movies found of type '{movie_type}'")

        logger.info(f"Found {len(movies)} movies of type: {movie_type}")
        return movies

    async def get_movies_by_year(
        self, year: int, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get movies by year."""
        logger.debug(f"Getting movies by year: {year}, limit={limit}, skip={skip}")

        movies = await self.movie_repository.find_by_year(year, limit=limit, skip=skip)
        if not movies:
            logger.info(f"No movies found for year: {year}")
            raise NotFoundError(f"No movies found for year {year}")

        logger.info(f"Found {len(movies)} movies for year: {year}")
        return movies

    async def get_all_genres(self) -> List[str]:
        """Get all movie genres"""
        logger.info("Getting movie genres")
        genres = await self.movie_repository.find_distinct("genres")
        logger.info(f"Found {len(genres)} movie genres")
        return genres

    async def get_all_types(self) -> List[str]:
        """Get all movie genres"""
        logger.info("Getting movie types")
        genres = await self.movie_repository.find_distinct("type")
        logger.info(f"Found {len(genres)} movie genres")
        return genres

    async def get_movies_by_genre(
        self, genre: str, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get movies by genre."""
        logger.debug(f"Getting movies by genre: {genre}, limit={limit}, skip={skip}")

        movies = await self.movie_repository.find_by_genre(
            genre, limit=limit, skip=skip
        )
        if not movies:
            logger.info(f"No movies found for genre: {genre}")

        logger.info(f"Found {len(movies)} movies for genre: {genre}")
        return movies
