from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from ...schemas.movie import MovieResponse, MovieQuery
from ...services.movie_service import MovieService
from ...repositories.movie_repository import MovieRepository
from ...core.exceptions import NotFoundError
from ...core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/movies", tags=["movies"])


async def get_movie_repository() -> MovieRepository:
    """Dependency to get movie repository instance."""
    return MovieRepository()


async def get_movie_service(
    repository: MovieRepository = Depends(get_movie_repository),
) -> MovieService:
    """Dependency to get movie service instance."""
    return MovieService(repository)


@router.get("/", response_model=List[MovieResponse])
async def get_movies(
    query: Annotated[MovieQuery, Query()],
    movie_service: MovieService = Depends(get_movie_service),
):
    """
    Retrieve movies with optional filtering and pagination.

    - **id**: Filter by movie ID
    - **title**: Filter by movie title (exact match)
    - **type**: Filter by movie type (e.g., 'movie', 'series')
    - **genres**: Filter by movie genres
    - **year**: Filter by release year
    - **limit**: Number of movies to return (default: 10)
    - **skip**: Number of movies to skip (default: 0)
    """
    logger.info(
        f"Movie request received with query: {query.model_dump(exclude_none=True)}"
    )

    try:
        movies = await movie_service.get_movies(
            movie_id=query.id,
            title=query.title,
            movie_type=query.type,
            genres=query.genres,
            year=query.year,
            limit=query.limit or 10,
            skip=query.skip or 0,
        )

        logger.info(f"Successfully retrieved {len(movies)} movies")
        return [MovieResponse.from_dict(movie) for movie in movies]

    except NotFoundError as e:
        logger.warning(f"Movies not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_movies: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/genres")
async def get_movie_genres(
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movie genres."""
    try:
        genres = await movie_service.get_all_genres()
        return genres

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/genres/{movie_genre}", response_model=List[MovieResponse])
async def get_movies_by_genre(
    movie_genre: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by genre."""
    try:
        movies = await movie_service.get_movies_by_genre(movie_genre, limit, skip)
        return [MovieResponse.from_dict(movie) for movie in movies]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/types")
async def get_movie_types(
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movie types."""
    try:
        genres = await movie_service.get_all_types()
        return genres

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/types/{movie_type}", response_model=List[MovieResponse])
async def get_movies_by_type(
    movie_type: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by type."""
    try:
        movies = await movie_service.get_movies_by_type(movie_type, limit, skip)
        return [MovieResponse.from_dict(movie) for movie in movies]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/year/{year}", response_model=List[MovieResponse])
async def get_movies_by_year(
    year: int,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by release year."""
    try:
        movies = await movie_service.get_movies_by_year(year, limit, skip)
        return [MovieResponse.from_dict(movie) for movie in movies]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie_by_id(
    movie_id: str, movie_service: MovieService = Depends(get_movie_service)
):
    """Get a specific movie by ID."""
    try:
        movie = await movie_service.get_movie_by_id(movie_id)
        return MovieResponse.from_dict(movie)

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
