from typing import List, Annotated
from fastapi import APIRouter, Depends, Query, Request
from slowapi import Limiter
from ...schemas.schemas import UserResponse, UserQuery, UserCreate, MessageResponse
from ...services.user_service import UserService
from ...repositories.user_repository import UserRepository
from ...core.config import settings
from ...core.logging import get_logger
from ...core.rate_limiter import rate_limit_key, get_rate_limit_config

logger = get_logger(__name__)

rate_limit_config = get_rate_limit_config()
limiter = Limiter(key_func=rate_limit_key)

router = APIRouter(prefix="/users", tags=["users"])

DEFAULT_LIMIT = settings.DEFAULT_LIST_PAGE_SIZE
MAX_LIMIT = settings.MAX_PAGE_SIZE


async def get_user_repository() -> UserRepository:
    """Dependency to get user repository instance."""
    return UserRepository()


async def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Dependency to get user service instance."""
    return UserService(repository)


@router.get("/", response_model=List[UserResponse])
@limiter.limit(rate_limit_config.users)
async def get_users(
    query: Annotated[UserQuery, Query()],
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    """
    Retrieve users with optional filtering and pagination.

    - **id**: Filter by user ID
    - **name**: Filter by user name
    - **email**: Filter by user email
    - **limit**: Number of users to return (default: 10)
    - **skip**: Number of users to skip (default: 0)
    """
    return await user_service.get_users(
        user_id=query.id,
        name=query.name,
        email=query.email,
        limit=query.limit or DEFAULT_LIMIT,
        skip=query.skip or 0,
    )


@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit(rate_limit_config.users)
async def get_user_by_id(
    request: Request,
    user_id: str,
    user_service: UserService = Depends(get_user_service),
):
    """Get a specific user by ID."""
    return await user_service.get_user_by_id(user_id)


@router.post("/", response_model=MessageResponse)
@limiter.limit(rate_limit_config.users)
async def create_user(
    request: Request,
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    """
    Create a new user.

    - **name**: User name (required, 1-100 characters)
    - **email**: User email (required, must be valid email)
    - **password**: User password (required, 6-100 characters)
    """
    logger.info(f"users.create | POST | email={user_data.email}")
    return await user_service.create_user(user_data)


@router.get("/email/{email}", response_model=List[UserResponse])
@limiter.limit(rate_limit_config.users)
async def get_user_by_email(
    request: Request,
    email: str,
    user_service: UserService = Depends(get_user_service),
):
    """Get users by email."""
    return await user_service.get_users_by_email(email)


@router.get("/name/{name}", response_model=List[UserResponse])
@limiter.limit(rate_limit_config.users)
async def get_user_by_name(
    request: Request,
    name: str,
    user_service: UserService = Depends(get_user_service),
):
    """Get users by name."""
    return await user_service.get_users_by_name(name)
