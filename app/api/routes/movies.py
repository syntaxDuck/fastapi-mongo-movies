from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError
from ...schemas.schemas import MovieResponse, MovieQuery
from ...services.movie_service import MovieService
from ...repositories.movie_repository import MovieRepository
from ...core.exceptions import NotFoundError
from ...core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/movies", tags=["movies"])


# TODO: Might be nice to implement some sorting on the backend so the forntend doens't have to do it
# TODO: Need to improve endpoint flexability to allow for filtering parameters to be attached to specific parameters
# TODO: Create utility endpoint that will comb through all movies in dataset and mark the ones with valid posters
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
    logger.info(
        f"Movie request received with query: {query.model_dump(exclude_none=True)}"
    )

    try:
        # If search parameter is provided, use text search
        if query.search:
            movies = await movie_service.search_movies_by_text(
                search_text=query.search,
                limit=query.limit or 10,
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
                limit=query.limit or 10,
                skip=query.skip or 0,
                include_invalid_posters=query.include_invalid_posters or False,
                sort_by=query.sort_by,
                sort_order=query.sort_order or "asc",
            )

        logger.info(f"Successfully retrieved {len(movies)} movies")
        return movies

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
    logger.info("API: get_movie_genres() called")

    try:
        genres = await movie_service.get_all_genres()
        logger.info(
            f"API: get_movie_genres() successfully retrieved {len(genres)} genres"
        )
        return genres

    except NotFoundError as e:
        logger.warning(f"API: get_movie_genres() no genres found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_movie_genres() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/genres/{movie_genre}", response_model=List[MovieResponse])
async def get_movies_by_genre(
    movie_genre: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(
        False, description="Include movies with invalid posters"
    ),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by genre."""
    logger.info(
        f"API: get_movies_by_genre() called with genre='{movie_genre}', limit={limit}, skip={skip}, sort_by={sort_by}, sort_order={sort_order}, include_invalid_posters={include_invalid_posters}"
    )

    try:
        movies = await movie_service.get_movies_by_genre(
            movie_genre, limit, skip, include_invalid_posters, sort_by, sort_order
        )
        logger.info(
            f"API: get_movies_by_genre() found {len(movies)} movies in genre '{movie_genre}'"
        )
        return movies

    except NotFoundError as e:
        logger.warning(f"API: get_movies_by_genre() no movies found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        logger.error(f"API: get_movies_by_genre() error validating Movie data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        logger.error(f"API: get_movies_by_genre() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/types")
async def get_movie_types(
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movie types."""
    logger.info("API: get_movie_types() called")

    try:
        types = await movie_service.get_all_types()
        logger.info(f"API: get_movie_types() successfully retrieved {len(types)} types")
        return types

    except NotFoundError as e:
        logger.warning(f"API: get_movie_types() no types found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_movie_types() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/types/{movie_type}", response_model=List[MovieResponse])
async def get_movies_by_type(
    movie_type: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(
        False, description="Include movies with invalid posters"
    ),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by type."""
    logger.info(
        f"API: get_movies_by_type() called with type='{movie_type}', limit={limit}, skip={skip}, sort_by={sort_by}, sort_order={sort_order}, include_invalid_posters={include_invalid_posters}"
    )

    try:
        movies = await movie_service.get_movies_by_type(
            movie_type, limit, skip, include_invalid_posters, sort_by, sort_order
        )
        logger.info(
            f"API: get_movies_by_type() found {len(movies)} movies of type '{movie_type}'"
        )
        return movies

    except NotFoundError as e:
        logger.warning(f"API: get_movies_by_type() no movies found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_movies_by_type() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/year/{year}", response_model=List[MovieResponse])
async def get_movies_by_year(
    year: int,
    mod: str = Query("eq", description="Determin search modifier for query"),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(
        False, description="Include movies with invalid posters"
    ),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by release year."""
    logger.info(
        f"API: get_movies_by_year() called with year={year}, mod={mod}, limit={limit}, skip={skip}, sort_by={sort_by}, sort_order={sort_order}, include_invalid_posters={include_invalid_posters}"
    )

    try:
        movies = await movie_service.get_movies_by_year(
            year, mod, limit, skip, include_invalid_posters, sort_by, sort_order
        )
        logger.info(
            f"API: get_movies_by_year() found {len(movies)} movies from year {year}"
        )
        return movies

    except NotFoundError as e:
        logger.warning(f"API: get_movies_by_year() no movies found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_movies_by_year() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/rating/{rating}", response_model=List[MovieResponse])
async def get_movies_by_rating(
    rating: int,
    mod: str = Query("eq", description="Determin search modifier for query"),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    ),
    sort_order: str = Query(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    ),
    include_invalid_posters: bool = Query(
        False, description="Include movies with invalid posters"
    ),
    movie_service: MovieService = Depends(get_movie_service),
):
    """Get movies by rating."""
    logger.info(
        f"API: get_movies_by_rating() called with rating={rating}, mod={mod}, limit={limit}, skip={skip}, sort_by={sort_by}, sort_order={sort_order}, include_invalid_posters={include_invalid_posters}"
    )

    try:
        movies = await movie_service.get_movies_by_rating(
            rating, mod, limit, skip, include_invalid_posters, sort_by, sort_order
        )
        logger.info(
            f"API: get_movies_by_rating() found {len(movies)} movies from rating {rating}"
        )
        return movies

    except NotFoundError as e:
        logger.warning(f"API: get_movies_by_rating() no movies found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_movies_by_rating() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie_by_id(
    movie_id: str, movie_service: MovieService = Depends(get_movie_service)
):
    """Get a specific movie by ID."""
    logger.info(f"API: get_movie_by_id() called with movie_id={movie_id}")

    try:
        movie = await movie_service.get_movie_by_id(movie_id)
        logger.info(
            f"API: get_movie_by_id() successfully retrieved movie: {movie.title if hasattr(movie, 'title') else 'Unknown'}"
        )
        return movie

    except NotFoundError as e:
        logger.warning(f"API: get_movie_by_id() movie not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_movie_by_id() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
