"""
Movie Service layer for business logic using proper protocol-based dependency injection.
"""


import time

from ..core.exceptions import NotFoundError
from ..core.logging import get_logger
from ..core.validators import (
    validate_limit,
    validate_modifier,
    validate_non_empty_string,
    validate_rating,
    validate_skip,
    validate_year,
    validate_year_required,
)
from ..repositories.protocol import MovieRepositoryProtocol
from ..schemas.schemas import MovieResponse

logger = get_logger(__name__)


class MovieService:
    """Service layer for movie business logic."""

    # Class-level cache for slow-changing metadata
    _genres_cache: list[str] | None = None
    _genres_cache_time: float = 0
    _types_cache: list[str] | None = None
    _types_cache_time: float = 0
    CACHE_TTL = 3600  # 1 hour (3600 seconds)

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
        movie_id: str | None = None,
        title: str | None = None,
        movie_type: str | None = None,
        genres: list[str] | None = None,
        year: int | None = None,
        limit: int = 10,
        skip: int = 0,
        include_invalid_posters: bool = False,
        sort_by: str | None = None,
        sort_order: str | None = "asc",
    ) -> list[MovieResponse]:
        """Get movies with optional filtering."""

        limit = validate_limit(limit)
        skip = validate_skip(skip)
        year = validate_year(year)

        logger.debug(
            f"Getting movies with filters: movie_id={movie_id}, title={title}, "
            f"type={movie_type}, genres={genres}, year={year}, limit={limit}, skip={skip}, "
            f"include_invalid_posters={include_invalid_posters}, sort_by={sort_by}, sort_order={sort_order}"
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
            sort_by=sort_by,
            sort_order=sort_order,
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
        sort_by: str | None = None,
        sort_order: str | None = "asc",
    ) -> list[MovieResponse]:
        """Get movies by type."""

        movie_type = validate_non_empty_string(movie_type, "movie_type") or movie_type
        limit = validate_limit(limit)
        skip = validate_skip(skip)

        logger.debug(
            f"Getting movies by type: {movie_type}, limit={limit}, skip={skip}, include_invalid_posters={include_invalid_posters}, sort_by={sort_by}, sort_order={sort_order}"
        )

        movies = await self.movie_repository.find_by_type(
            movie_type,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
            sort_by=sort_by,
            sort_order=sort_order,
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

    async def get_movies_by_rating(
        self,
        rating: int,
        mod: str = "eq",
        limit: int = 10,
        skip: int = 0,
        include_invalid_posters: bool = False,
        sort_by: str | None = None,
        sort_order: str | None = "asc",
    ) -> list[MovieResponse]:
        """Get movies by rating."""

        rating = validate_rating(rating)
        mod = validate_modifier(mod)
        limit = validate_limit(limit)
        skip = validate_skip(skip)

        logger.debug(
            f"Getting movies by rating: {rating}, modifier: {mod}, limit={limit}, skip={skip}, include_invalid_posters={include_invalid_posters}, sort_by={sort_by}, sort_order={sort_order}"
        )

        movies = await self.movie_repository.find_by_rating(
            rating,
            mod,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        if not movies:
            logger.info(
                f"MovieService.get_movies_by_rating() no movies found for rating: {rating} (limit={limit}, skip={skip})"
            )
            raise NotFoundError(f"No movies found for rating {rating}")

        logger.info(
            f"MovieService.get_movies_by_rating() found {len(movies)} movies for rating: {rating}"
        )
        return movies

    async def get_movies_by_year(
        self,
        year: int,
        mod: str = "eq",
        limit: int = 10,
        skip: int = 0,
        include_invalid_posters: bool = False,
        sort_by: str | None = None,
        sort_order: str | None = "asc",
    ) -> list[MovieResponse]:
        """Get movies by year."""

        year = validate_year_required(year)
        mod = validate_modifier(mod)
        limit = validate_limit(limit)
        skip = validate_skip(skip)

        logger.debug(
            f"Getting movies by year: {year}, modifier: {mod}, limit={limit}, skip={skip}, include_invalid_posters={include_invalid_posters}, sort_by={sort_by}, sort_order={sort_order}"
        )

        movies = await self.movie_repository.find_by_year(
            year,
            mod,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
            sort_by=sort_by,
            sort_order=sort_order,
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

    async def get_all_genres(self) -> list[str]:
        """Get all movie genres with in-memory TTL caching."""
        current_time = time.time()
        if (
            MovieService._genres_cache is not None
            and (current_time - MovieService._genres_cache_time) < MovieService.CACHE_TTL
        ):
            logger.debug("Returning movie genres from cache")
            return list(MovieService._genres_cache)

        logger.info("Getting movie genres from repository")
        genres = await self.movie_repository.get_all_genres()

        # Update cache
        MovieService._genres_cache = genres
        MovieService._genres_cache_time = current_time

        logger.info(f"Found {len(genres)} movie genres (cached)")
        return list(genres)

    async def get_all_types(self) -> list[str]:
        """Get all movie types with in-memory TTL caching."""
        current_time = time.time()
        if (
            MovieService._types_cache is not None
            and (current_time - MovieService._types_cache_time) < MovieService.CACHE_TTL
        ):
            logger.debug("Returning movie types from cache")
            return list(MovieService._types_cache)

        logger.info("Getting movie types from repository")
        types = await self.movie_repository.get_all_types()

        # Update cache
        MovieService._types_cache = types
        MovieService._types_cache_time = current_time

        logger.info(f"Found {len(types)} movie types (cached)")
        return list(types)

    async def get_movies_by_genre(
        self,
        genre: str,
        limit: int = 10,
        skip: int = 0,
        include_invalid_posters: bool = False,
        sort_by: str | None = None,
        sort_order: str | None = "asc",
    ) -> list[MovieResponse]:
        """Get movies by genre."""

        genre = validate_non_empty_string(genre, "genre") or genre
        limit = validate_limit(limit)
        skip = validate_skip(skip)

        logger.debug(
            f"Getting movies by genre: {genre}, limit={limit}, skip={skip}, include_invalid_posters={include_invalid_posters}, sort_by={sort_by}, sort_order={sort_order}"
        )

        movies = await self.movie_repository.find_by_genre(
            genre,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
            sort_by=sort_by,
            sort_order=sort_order,
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
        sort_by: str | None = None,
        sort_order: str | None = "asc",
    ) -> list[MovieResponse]:
        """Search movies by text search."""

        search_text = validate_non_empty_string(search_text, "search_text") or search_text
        if search_text and len(search_text) > 200:
            logger.warning(
                f"MovieService.search_movies_by_text() very long search_text: {len(search_text)} characters"
            )
        limit = validate_limit(limit)
        skip = validate_skip(skip)

        logger.debug(
            f"Searching movies by text: {search_text}, limit={limit}, skip={skip}, include_invalid_posters={include_invalid_posters}, sort_by={sort_by}, sort_order={sort_order}"
        )

        movies = await self.movie_repository.search_movies_by_text(
            search_text,
            limit=limit,
            skip=skip,
            include_invalid_posters=include_invalid_posters,
            sort_by=sort_by,
            sort_order=sort_order,
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
