from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from ...schemas.movie import CommentResponse, CommentQuery
from ...services.movie_service import CommentService
from ...repositories.movie_repository import CommentRepository
from ...core.exceptions import NotFoundError

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
    try:
        comments = await comment_service.get_comments(
            comment_id=query.id,
            movie_id=query.movie_id,
            name=query.name,
            email=query.email,
            limit=query.limit or 10,
            skip=query.skip or 0,
        )

        return [CommentResponse.from_dict(comment) for comment in comments]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment_by_id(
    comment_id: str, comment_service: CommentService = Depends(get_comment_service)
):
    """Get a specific comment by ID."""
    try:
        comment = await comment_service.get_comment_by_id(comment_id)
        return CommentResponse.from_dict(comment)

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/movie/{movie_id}", response_model=List[CommentResponse])
async def get_comments_by_movie_id(
    movie_id: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    comment_service: CommentService = Depends(get_comment_service),
):
    """Get comments by movie ID."""
    try:
        comments = await comment_service.get_comments_by_movie_id(
            movie_id, limit=limit, skip=skip
        )
        return [CommentResponse.from_dict(comment) for comment in comments]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/email/{email}", response_model=List[CommentResponse])
async def get_comments_by_email(
    email: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    comment_service: CommentService = Depends(get_comment_service),
):
    """Get comments by email."""
    try:
        comments = await comment_service.get_comments_by_email(
            email, limit=limit, skip=skip
        )
        return [CommentResponse.from_dict(comment) for comment in comments]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/name/{name}", response_model=List[CommentResponse])
async def get_comments_by_name(
    name: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    comment_service: CommentService = Depends(get_comment_service),
):
    """Get comments by name."""
    try:
        comments = await comment_service.get_comments_by_name(
            name, limit=limit, skip=skip
        )
        return [CommentResponse.from_dict(comment) for comment in comments]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
