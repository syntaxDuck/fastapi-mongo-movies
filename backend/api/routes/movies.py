from typing import Annotated

from fastapi import APIRouter, Query, Request
from slowapi import Limiter

from ...core.config import settings
from ...core.logging import get_logger
from ...core.rate_limiter import get_rate_limit_config, rate_limit_key
from ...repositories.movie_repository import MovieRepository
from ...schemas import MovieQuery, MovieResponse
from ...services.movie_service import MovieService

logger = get_logger(__name__)

rate_limit_config = get_rate_limit_config()

router = APIRouter(prefix="/movies", tags=["movies"])

limiter = Limiter(key_func=rate_limit_key)

DEFAULT_LIMIT = settings.MOVIE_LIST_PAGE_SIZE
MAX_LIMIT = settings.MAX_PAGE_SIZE

_movie_repository: MovieRepository | None = None
_movie_service: MovieService | None = None


def _get_movie_repository() -> MovieRepository:
    global _movie_repository
    if _movie_repository is None:
        _movie_repository = MovieRepository()
    return _movie_repository


def _get_movie_service() -> MovieService:
    global _movie_service
    if _movie_service is None:
        _movie_service = MovieService(_get_movie_repository())
    return _movie_service


@limiter.limit(rate_limit_config.general)
@router.get("/", response_model=list[MovieResponse])
async def get_movies(
    request: Request,
    query: Annotated[MovieQuery, Query()],
):
    """
    Retrieve movies with optional filtering, pagination, and sorting.

    - **id**: Filter by movie ID
    - **title**: Filter by movie title (exact match)
    - **search**: Search movies by text in title, plot, etc.
    - **type**: Filter by movie type (e.g., 'movie', 'series')
    - **genres**: Filter by movie genres
    - **year**: Filter by release year
    - **sort_by**: Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)
    - **sort_order**: Sort order 'asc' for ascending or 'desc' for descending (default: asc)
    - **limit**: Number of movies to return (default: 10)
    - **skip**: Number of movies to skip (default: 0)
    """
    movie_service = _get_movie_service()
    if query.search:
        movies = await movie_service.search_movies_by_text(
            search_text=query.search,
            limit=query.limit or DEFAULT_LIMIT,
            skip=query.skip or 0,
            include_invalid_posters=query.include_invalid_posters or False,
            sort_by=query.sort_by,
            sort_order=query.sort_order or "asc",
        )
    else:
        movies = await movie_service.search_movies_multiple_criteria(
            movie_id=query.id,
            title=query.title,
            movie_type=query.type,
            genres=query.genres,
            year=query.year,
            limit=query.limit or DEFAULT_LIMIT,
            skip=query.skip or 0,
            include_invalid_posters=query.include_invalid_posters or False,
            sort_by=query.sort_by,
            sort_order=query.sort_order or "asc",
        )

    return movies


@router.get("/genres")
@limiter.limit(rate_limit_config.general)
async def get_movie_genres(
    request: Request,
):
    """Get movie genres."""
    movie_service = _get_movie_service()
    return await movie_service.get_all_genres()


@router.get("/genres/{movie_genre}", response_model=list[MovieResponse])
@limiter.limit(rate_limit_config.general)
async def get_movies_by_genre(
    request: Request,
    movie_genre: str,
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
    sort_by: str | None = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(False, description="Include movies with invalid posters"),
):
    """Get movies by genre."""
    movie_service = _get_movie_service()
    return await movie_service.get_movies_by_genre(
        movie_genre, limit, skip, include_invalid_posters, sort_by, sort_order
    )


@router.get("/types")
@limiter.limit(rate_limit_config.general)
async def get_movie_types(
    request: Request,
):
    """Get movie types."""
    movie_service = _get_movie_service()
    return await movie_service.get_all_types()


@router.get("/types/{movie_type}", response_model=list[MovieResponse])
@limiter.limit(rate_limit_config.general)
async def get_movies_by_type(
    request: Request,
    movie_type: str,
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
    sort_by: str | None = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(False, description="Include movies with invalid posters"),
):
    """Get movies by type."""
    movie_service = _get_movie_service()
    return await movie_service.get_movies_by_type(
        movie_type, limit, skip, include_invalid_posters, sort_by, sort_order
    )


@router.get("/year/{year}", response_model=list[MovieResponse])
@limiter.limit(rate_limit_config.general)
async def get_movies_by_year(
    request: Request,
    year: int,
    mod: str = Query("eq", description="Determin search modifier for query"),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
    sort_by: str | None = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(False, description="Include movies with invalid posters"),
):
    """Get movies by release year."""
    movie_service = _get_movie_service()
    return await movie_service.get_movies_by_year(
        year, mod, limit, skip, include_invalid_posters, sort_by, sort_order
    )


@router.get("/rating/{rating}", response_model=list[MovieResponse])
@limiter.limit(rate_limit_config.general)
async def get_movies_by_rating(
    request: Request,
    rating: int,
    mod: str = Query("eq", description="Determin search modifier for query"),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
    sort_by: str | None = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(False, description="Include movies with invalid posters"),
):
    """Get movies by rating."""
    movie_service = _get_movie_service()
    return await movie_service.get_movies_by_rating(
        rating, mod, limit, skip, include_invalid_posters, sort_by, sort_order
    )


@router.get("/{movie_id}", response_model=MovieResponse)
@limiter.limit(rate_limit_config.general)
async def get_movie_by_id(
    request: Request,
    movie_id: str,
):
    """Get a specific movie by ID."""
    movie_service = _get_movie_service()
    return await movie_service.get_movie_by_id(movie_id)
