from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from slowapi import Limiter

from ...core.config import settings
from ...core.logging import get_logger
from ...core.rate_limiter import get_rate_limit_config, rate_limit_key
from ...core.security import verify_admin_api_key
from ...repositories.user_repository import UserRepository
from ...schemas import MessageResponse, UserCreate, UserQuery, UserResponse
from ...services.user_service import UserService

logger = get_logger(__name__)

rate_limit_config = get_rate_limit_config()
limiter = Limiter(key_func=rate_limit_key)

router = APIRouter(prefix="/users", tags=["users"])

DEFAULT_LIMIT = settings.DEFAULT_LIST_PAGE_SIZE
MAX_LIMIT = settings.MAX_PAGE_SIZE

_user_repository: UserRepository | None = None
_user_service: UserService | None = None


def _get_user_repository() -> UserRepository:
    global _user_repository
    if _user_repository is None:
        _user_repository = UserRepository()
    return _user_repository


def _get_user_service() -> UserService:
    global _user_service
    if _user_service is None:
        _user_service = UserService(_get_user_repository())
    return _user_service


@router.get(
    "/", response_model=list[UserResponse], dependencies=[Depends(verify_admin_api_key)]
)
@limiter.limit(rate_limit_config.users)
async def get_users(
    query: Annotated[UserQuery, Query()],
    request: Request,
):
    """
    Retrieve users with optional filtering and pagination.

    - **id**: Filter by user ID
    - **name**: Filter by user name
    - **email**: Filter by user email
    - **limit**: Number of users to return (default: 10)
    - **skip**: Number of users to skip (default: 0)
    """
    user_service = _get_user_service()
    return await user_service.get_users(
        user_id=query.id,
        name=query.name,
        email=query.email,
        limit=query.limit or DEFAULT_LIMIT,
        skip=query.skip or 0,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(verify_admin_api_key)],
)
@limiter.limit(rate_limit_config.users)
async def get_user_by_id(
    request: Request,
    user_id: str,
):
    """Get a specific user by ID."""
    user_service = _get_user_service()
    return await user_service.get_user_by_id(user_id)


@router.post("/", response_model=MessageResponse)
@limiter.limit(rate_limit_config.users)
async def create_user(
    request: Request,
    user_data: UserCreate,
):
    """
    Create a new user.

    - **name**: User name (required, 1-100 characters)
    - **email**: User email (required, must be valid email)
    - **password**: User password (required, 6-100 characters)
    """
    user_service = _get_user_service()
    logger.info(f"users.create | POST | email={user_data.email}")
    return await user_service.create_user(user_data)


@router.get(
    "/email/{email}",
    response_model=list[UserResponse],
    dependencies=[Depends(verify_admin_api_key)],
)
@limiter.limit(rate_limit_config.users)
async def get_user_by_email(
    request: Request,
    email: str,
):
    """Get users by email."""
    user_service = _get_user_service()
    return await user_service.get_users_by_email(email)


@router.get(
    "/name/{name}",
    response_model=list[UserResponse],
    dependencies=[Depends(verify_admin_api_key)],
)
@limiter.limit(rate_limit_config.users)
async def get_user_by_name(
    request: Request,
    name: str,
):
    """Get users by name."""
    user_service = _get_user_service()
    return await user_service.get_users_by_name(name)
