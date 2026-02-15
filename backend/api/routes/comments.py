"""
Comment Repository layer using context manager pattern.
"""

from typing import Annotated

from fastapi import APIRouter, Query, Request
from slowapi import Limiter

from ...core.config import settings
from ...core.rate_limiter import get_rate_limit_config, rate_limit_key
from ...repositories.comment_repository import CommentRepository
from ...schemas import CommentQuery, CommentResponse
from ...services.comment_service import CommentService

rate_limit_config = get_rate_limit_config()
limiter = Limiter(key_func=rate_limit_key)

router = APIRouter(prefix="/comments", tags=["comments"])

DEFAULT_LIMIT = settings.COMMENT_PAGE_SIZE
MAX_LIMIT = settings.MAX_PAGE_SIZE

_comment_repository: CommentRepository | None = None
_comment_service: CommentService | None = None


def _get_comment_repository() -> CommentRepository:
    global _comment_repository
    if _comment_repository is None:
        _comment_repository = CommentRepository()
    return _comment_repository


def _get_comment_service() -> CommentService:
    global _comment_service
    if _comment_service is None:
        _comment_service = CommentService(_get_comment_repository())
    return _comment_service


@router.get("/", response_model=list[CommentResponse])
@limiter.limit(rate_limit_config.comments)
async def get_comments(
    request: Request,
    query: Annotated[CommentQuery, Query()],
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
    comment_service = _get_comment_service()
    return await comment_service.get_comments(
        comment_id=query.id,
        movie_id=query.movie_id,
        name=query.name,
        email=query.email,
        limit=query.limit or DEFAULT_LIMIT,
        skip=query.skip or 0,
    )


@router.get("/movie/{movie_id}", response_model=list[CommentResponse])
@limiter.limit(rate_limit_config.comments)
async def get_comments_by_movie(
    request: Request,
    movie_id: str,
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
):
    """Get comments by movie ID."""
    comment_service = _get_comment_service()
    return await comment_service.get_comments_by_movie_id(movie_id, limit=limit, skip=skip)


@router.get("/email/{email}", response_model=list[CommentResponse])
@limiter.limit(rate_limit_config.comments)
async def get_comments_by_email(
    request: Request,
    email: str,
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
):
    """Get comments by email."""
    comment_service = _get_comment_service()
    return await comment_service.get_comments_by_email(email, limit=limit, skip=skip)


@router.get("/name/{name}", response_model=list[CommentResponse])
@limiter.limit(rate_limit_config.comments)
async def get_comments_by_name(
    request: Request,
    name: str,
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(0, ge=0),
):
    """Get comments by name."""
    comment_service = _get_comment_service()
    return await comment_service.get_comments_by_name(name, limit=limit, skip=skip)


@router.get("/{comment_id}", response_model=CommentResponse)
@limiter.limit(rate_limit_config.comments)
async def get_comment_by_id(
    request: Request,
    comment_id: str,
):
    """Get a specific comment by ID."""
    comment_service = _get_comment_service()
    return await comment_service.get_comment_by_id(comment_id)
