from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query, Request
from slowapi import Limiter

from ...core.config import settings
from ...core.logging import get_logger
from ...core.rate_limiter import get_rate_limit_config, rate_limit_key
from ...repositories.movie_repository import MovieRepository
from ...schemas.schemas import MovieQuery, MovieResponse
from ...services.movie_service import MovieService

logger = get_logger(__name__)

rate_limit_config = get_rate_limit_config()

router = APIRouter(prefix="/movies", tags=["movies"])

limiter = Limiter(key_func=rate_limit_key)

DEFAULT_LIMIT = settings.MOVIE_LIST_PAGE_SIZE
MAX_LIMIT = settings.MAX_PAGE_SIZE


async def get_movie_repository() -> MovieRepository:
    """Dependency to get movie repository instance."""
    return MovieRepository()


async def get_movie_service(
    repository: MovieRepository = Depends(get_movie_repository),
) -> MovieService:
    """Dependency to get movie service instance."""
    return MovieService(repository)


@limiter.limit(rate_limit_config.general)
@router.get("/", response_model=List[MovieResponse])
async def get_movies(
    request: Request,
    query: Annotated[MovieQuery, Query()],
    movie_service: MovieService = Depends(get_movie_service),
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
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movie genres."""
    return await movie_service.get_all_genres()


@router.get("/genres/{movie_genre}", response_model=List[MovieResponse])
@limiter.limit(rate_limit_config.general)
async def get_movies_by_genre(
    request: Request,
    movie_genre: str,
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(False, description="Include movies with invalid posters"),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by genre."""
    return await movie_service.get_movies_by_genre(
        movie_genre, limit, skip, include_invalid_posters, sort_by, sort_order
    )


@router.get("/types")
@limiter.limit(rate_limit_config.general)
async def get_movie_types(
    request: Request,
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movie types."""
    return await movie_service.get_all_types()


@router.get("/types/{movie_type}", response_model=List[MovieResponse])
@limiter.limit(rate_limit_config.general)
async def get_movies_by_type(
    request: Request,
    movie_type: str,
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(False, description="Include movies with invalid posters"),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by type."""
    return await movie_service.get_movies_by_type(
        movie_type, limit, skip, include_invalid_posters, sort_by, sort_order
    )


@router.get("/year/{year}", response_model=List[MovieResponse])
@limiter.limit(rate_limit_config.general)
async def get_movies_by_year(
    request: Request,
    year: int,
    mod: str = Query("eq", description="Determin search modifier for query"),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(False, description="Include movies with invalid posters"),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by release year."""
    return await movie_service.get_movies_by_year(
        year, mod, limit, skip, include_invalid_posters, sort_by, sort_order
    )


@router.get("/rating/{rating}", response_model=List[MovieResponse])
@limiter.limit(rate_limit_config.general)
async def get_movies_by_rating(
    request: Request,
    rating: int,
    mod: str = Query("eq", description="Determin search modifier for query"),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(False, description="Include movies with invalid posters"),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by rating."""
    return await movie_service.get_movies_by_rating(
        rating, mod, limit, skip, include_invalid_posters, sort_by, sort_order
    )


@router.get("/{movie_id}", response_model=MovieResponse)
@limiter.limit(rate_limit_config.general)
async def get_movie_by_id(
    request: Request,
    movie_id: str,
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get a specific movie by ID."""
    return await movie_service.get_movie_by_id(movie_id)
