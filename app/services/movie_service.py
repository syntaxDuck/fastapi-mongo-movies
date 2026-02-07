"""
Movie Service layer for business logic using proper protocol-based dependency injection.
"""

from typing import List, Optional

from ..schemas.schemas import MovieResponse
from ..repositories.protocol import MovieRepositoryProtocol
from ..core.exceptions import NotFoundError
from ..core.logging import get_logger

logger = get_logger(__name__)


class MovieService:
    """Service layer for movie business logic."""

    def __init__(self, movie_repository: MovieRepositoryProtocol) -> None:
        self.movie_repository = movie_repository

    async def get_movie_by_id(self, movie_id: str) -> MovieResponse:
        """Get a movie by its ID."""
        logger.debug(f"Getting movie by ID: {movie_id}")

        movie = await self.movie_repository.find_by_id(movie_id)
        if not movie:
            logger.warning(f"Movie not found - id:{movie_id}")
            raise NotFoundError(f"Movie with ID {movie_id} not found")

        logger.debug(f"Successfully retrieved movie: {movie_id}")
        return movie

    async def search_movies_multiple_criteria(
        self,
        movie_id: Optional[str] = None,
        title: Optional[str] = None,
        movie_type: Optional[str] = None,
        genres: Optional[List[str]] = None,
        year: Optional[int] = None,
        limit: int = 10,
        skip: int = 0,
        include_invalid_posters: bool = False,
    ) -> List[MovieResponse]:
        """Get movies with optional filtering."""

        if limit < 0 or limit > 1000:
            logger.warning(
                f"MovieService.get_movies() invalid limit parameter: {limit}, using default 10"
            )
            limit = 10
        if skip < 0:
            logger.warning(
                f"MovieService.get_movies() invalid skip parameter: {skip}, using default 0"
            )
            skip = 0
        if year is not None and (year < 1800 or year > 2100):
            logger.warning(
                f"MovieService.get_movies() suspicious year parameter: {year}"
            )

        logger.debug(
            f"Getting movies with filters: movie_id={movie_id}, title={title}, "
            f"type={movie_type}, genres={genres}, year={year}, limit={limit}, skip={skip}, "
            f"include_invalid_posters={include_invalid_posters}"
        )

        movies = await self.movie_repository.search_movies(
            movie_id=movie_id,
            title=title,
            movie_type=movie_type,
            genres=genres,
            year=year,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
        )

        if not movies:
            logger.info(
                f"MovieService.get_movies() no movies found matching criteria: movie_id={movie_id}, title={title}, type={movie_type}, genres={genres}, year={year}"
            )
            raise NotFoundError("No movies found matching the criteria")

        logger.info(f"MovieService.get_movies() found {len(movies)} movies")
        return movies

    async def get_movies_by_type(
        self,
        movie_type: str,
        limit: int = 10,
        skip: int = 0,
        include_invalid_posters: bool = False,
    ) -> List[MovieResponse]:
        """Get movies by type."""

        # Parameter validation logging
        if not movie_type or not movie_type.strip():
            logger.warning(
                "MovieService.get_movies_by_type() empty movie_type parameter"
            )
        if limit < 0 or limit > 1000:
            logger.warning(
                f"MovieService.get_movies_by_type() invalid limit parameter: {limit}, using default 10"
            )
            limit = 10
        if skip < 0:
            logger.warning(
                f"MovieService.get_movies_by_type() invalid skip parameter: {skip}, using default 0"
            )
            skip = 0

        logger.debug(
            f"Getting movies by type: {movie_type}, limit={limit}, skip={skip}, include_invalid_posters={include_invalid_posters}"
        )

        movies = await self.movie_repository.find_by_type(
            movie_type,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
        )
        if not movies:
            logger.info(
                f"MovieService.get_movies_by_type() no movies found for type: '{movie_type}' (limit={limit}, skip={skip})"
            )
            raise NotFoundError(f"No movies found of type '{movie_type}'")

        logger.info(
            f"MovieService.get_movies_by_type() found {len(movies)} movies of type: {movie_type}"
        )
        return movies

    async def get_movies_by_year(
        self,
        year: int,
        limit: int = 10,
        skip: int = 0,
        include_invalid_posters: bool = False,
    ) -> List[MovieResponse]:
        """Get movies by year."""

        # Parameter validation logging
        if year < 1800 or year > 2100:
            logger.warning(
                f"MovieService.get_movies_by_year() suspicious year parameter: {year}"
            )
        if limit < 0 or limit > 1000:
            logger.warning(
                f"MovieService.get_movies_by_year() invalid limit parameter: {limit}, using default 10"
            )
            limit = 10
        if skip < 0:
            logger.warning(
                f"MovieService.get_movies_by_year() invalid skip parameter: {skip}, using default 0"
            )
            skip = 0

        logger.debug(
            f"Getting movies by year: {year}, limit={limit}, skip={skip}, include_invalid_posters={include_invalid_posters}"
        )

        movies = await self.movie_repository.find_by_year(
            year,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
        )
        if not movies:
            logger.info(
                f"MovieService.get_movies_by_year() no movies found for year: {year} (limit={limit}, skip={skip})"
            )
            raise NotFoundError(f"No movies found for year {year}")

        logger.info(
            f"MovieService.get_movies_by_year() found {len(movies)} movies for year: {year}"
        )
        return movies

    async def get_all_genres(self) -> List[str]:
        """Get all movie genres"""
        logger.info("Getting movie genres")
        genres = await self.movie_repository.get_all_genres()
        logger.info(f"Found {len(genres)} movie genres")
        return genres

    async def get_all_types(self) -> List[str]:
        """Get all movie genres"""
        logger.info("Getting movie types")
        genres = await self.movie_repository.get_all_types()
        logger.info(f"Found {len(genres)} movie genres")
        return genres

    async def get_movies_by_genre(
        self,
        genre: str,
        limit: int = 10,
        skip: int = 0,
        include_invalid_posters: bool = False,
    ) -> List[MovieResponse]:
        """Get movies by genre."""

        # Parameter validation logging
        if not genre or not genre.strip():
            logger.warning("MovieService.get_movies_by_genre() empty genre parameter")
        if limit < 0 or limit > 1000:
            logger.warning(
                f"MovieService.get_movies_by_genre() invalid limit parameter: {limit}, using default 10"
            )
            limit = 10
        if skip < 0:
            logger.warning(
                f"MovieService.get_movies_by_genre() invalid skip parameter: {skip}, using default 0"
            )
            skip = 0

        logger.debug(
            f"Getting movies by genre: {genre}, limit={limit}, skip={skip}, include_invalid_posters={include_invalid_posters}"
        )

        movies = await self.movie_repository.find_by_genre(
            genre,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
        )
        if not movies:
            logger.info(
                f"MovieService.get_movies_by_genre() no movies found for genre: '{genre}' (limit={limit}, skip={skip})"
            )

        logger.info(
            f"MovieService.get_movies_by_genre() found {len(movies)} movies for genre: {genre}"
        )
        return movies

    async def search_movies_by_text(
        self,
        search_text: str,
        limit: int = 10,
        skip: int = 0,
        include_invalid_posters: bool = False,
    ) -> List[MovieResponse]:
        """Search movies by text search."""

        # Parameter validation logging
        if not search_text or not search_text.strip():
            logger.warning(
                "MovieService.search_movies_by_text() empty search_text parameter"
            )
        if len(search_text) > 200:
            logger.warning(
                f"MovieService.search_movies_by_text() very long search_text: {len(search_text)} characters"
            )
        if limit < 0 or limit > 1000:
            logger.warning(
                f"MovieService.search_movies_by_text() invalid limit parameter: {limit}, using default 10"
            )
            limit = 10
        if skip < 0:
            logger.warning(
                f"MovieService.search_movies_by_text() invalid skip parameter: {skip}, using default 0"
            )
            skip = 0

        logger.debug(
            f"Searching movies by text: {search_text}, limit={limit}, skip={skip}, include_invalid_posters={include_invalid_posters}"
        )

        movies = await self.movie_repository.search_movies_by_text(
            search_text,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
        )

        if not movies:
            logger.info(
                f"MovieService.search_movies_by_text() no movies found for text search: '{search_text}' (limit={limit}, skip={skip})"
            )
            raise NotFoundError(f"No movies found matching '{search_text}'")

        logger.info(
            f"MovieService.search_movies_by_text() found {len(movies)} movies for text search: {search_text}"
        )
        return movies
