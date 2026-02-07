"""
Comment Repository layer using context manager pattern.
"""

from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from ...schemas.schemas import CommentResponse, CommentQuery
from ...services.comment_service import CommentService
from ...repositories.comment_repository import CommentRepository
from ...core.exceptions import NotFoundError
from ...core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/comments", tags=["comments"])


async def get_comment_repository() -> CommentRepository:
    """Dependency to get comment repository instance."""
    return CommentRepository()


async def get_comment_service(
    repository: CommentRepository = Depends(get_comment_repository),
) -> CommentService:
    """Dependency to get comment service instance."""
    return CommentService(repository)


@router.get("/", response_model=List[CommentResponse])
async def get_comments(
    query: Annotated[CommentQuery, Query()],
    comment_service: CommentService = Depends(get_comment_service),
):
    """
    Retrieve comments with optional filtering and pagination.

    - **id**: Filter by comment ID
    - **name**: Filter by comment name
    - **email**: Filter by comment email
    - **movie_id**: Filter by movie ID
    - **limit**: Number of comments to return (default: 10)
    - **skip**: Number of comments to skip (default: 0)
    """
    logger.info(
        f"API: get_comments() called with query parameters: {query.model_dump(exclude_none=True)}"
    )

    try:
        comments = await comment_service.get_comments(
            comment_id=query.id,
            movie_id=query.movie_id,
            name=query.name,
            email=query.email,
            limit=query.limit or 10,
            skip=query.skip or 0,
        )
        logger.info(
            f"API: get_comments() successfully retrieved {len(comments)} comments"
        )
        return comments

    except NotFoundError as e:
        logger.warning(f"API: get_comments() no comments found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_comments() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment_by_id(
    comment_id: str, comment_service: CommentService = Depends(get_comment_service)
):
    """Get a specific comment by ID."""
    logger.info(f"API: get_comment_by_id() called with comment_id={comment_id}")

    try:
        comment = await comment_service.get_comment_by_id(comment_id)
        logger.info(
            f"API: get_comment_by_id() successfully retrieved comment by {comment.name if hasattr(comment, 'name') else 'Unknown'}"
        )
        return comment

    except NotFoundError as e:
        logger.warning(f"API: get_comment_by_id() comment not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_comment_by_id() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/movie/{movie_id}", response_model=List[CommentResponse])
async def get_comments_by_movie_id(
    movie_id: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    comment_service: CommentService = Depends(get_comment_service),
):
    """Get comments by movie ID."""
    logger.info(
        f"API: get_comments_by_movie_id() called with movie_id={movie_id}, limit={limit}, skip={skip}"
    )

    try:
        comments = await comment_service.get_comments_by_movie_id(
            movie_id, limit=limit, skip=skip
        )
        logger.info(
            f"API: get_comments_by_movie_id() found {len(comments)} comments for movie {movie_id}"
        )
        return comments

    except NotFoundError as e:
        logger.warning(f"API: get_comments_by_movie_id() no comments found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_comments_by_movie_id() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/email/{email}", response_model=List[CommentResponse])
async def get_comments_by_email(
    email: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    comment_service: CommentService = Depends(get_comment_service),
):
    """Get comments by email."""
    logger.info(
        f"API: get_comments_by_email() called with email='{email}', limit={limit}, skip={skip}"
    )

    try:
        comments = await comment_service.get_comments_by_email(
            email, limit=limit, skip=skip
        )
        logger.info(
            f"API: get_comments_by_email() found {len(comments)} comments by email '{email}'"
        )
        return comments

    except NotFoundError as e:
        logger.warning(f"API: get_comments_by_email() no comments found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_comments_by_email() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/name/{name}", response_model=List[CommentResponse])
async def get_comments_by_name(
    name: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    comment_service: CommentService = Depends(get_comment_service),
):
    """Get comments by name."""
    logger.info(
        f"API: get_comments_by_name() called with name='{name}', limit={limit}, skip={skip}"
    )

    try:
        comments = await comment_service.get_comments_by_name(
            name, limit=limit, skip=skip
        )
        logger.info(
            f"API: get_comments_by_name() found {len(comments)} comments by name '{name}'"
        )
        return comments

    except NotFoundError as e:
        logger.warning(f"API: get_comments_by_name() no comments found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_comments_by_name() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
