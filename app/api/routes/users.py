from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from ...schemas.schemas import UserResponse, UserQuery, UserCreate, MessageResponse
from ...services.user_service import UserService
from ...repositories.user_repository import UserRepository
from ...core.exceptions import NotFoundError, DuplicateResourceError
from ...core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_repository() -> UserRepository:
    """Dependency to get user repository instance."""
    return UserRepository()


async def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Dependency to get user service instance."""
    return UserService(repository)


@router.get("/", response_model=List[UserResponse])
async def get_users(
    query: Annotated[UserQuery, Query()],
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
    logger.info(
        f"API: get_users() called with query parameters: {query.model_dump(exclude_none=True)}"
    )

    try:
        users = await user_service.get_users(
            user_id=query.id,
            name=query.name,
            email=query.email,
            limit=query.limit or 10,
            skip=query.skip or 0,
        )

        logger.info(f"API: get_users() successfully retrieved {len(users)} users")
        return users

    except NotFoundError as e:
        logger.warning(f"API: get_users() no users found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_users() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str, user_service: UserService = Depends(get_user_service)
):
    """Get a specific user by ID."""
    logger.info(f"API: get_user_by_id() called with user_id={user_id}")

    try:
        user = await user_service.get_user_by_id(user_id)
        logger.info(
            f"API: get_user_by_id() successfully retrieved user: {user.name if hasattr(user, 'name') else 'Unknown'}"
        )
        return user

    except NotFoundError as e:
        logger.warning(f"API: get_user_by_id() user not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_user_by_id() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=MessageResponse)
async def create_user(
    user_data: Annotated[UserCreate, Query()],
    user_service: UserService = Depends(get_user_service),
):
    """
    Create a new user.

    - **name**: User name (required, 1-100 characters)
    - **email**: User email (required, must be valid email)
    - **password**: User password (required, 6-100 characters)
    """
    logger.info(
        f"API: create_user() called with user_data={{name: '{user_data.name}', email: '{user_data.email}'}}"
    )

    try:
        user_id = await user_service.create_user(user_data)
        logger.info(f"API: create_user() successfully created user with ID: {user_id}")
        return MessageResponse(message=f"User created successfully: {user_id}")

    except DuplicateResourceError as e:
        logger.warning(f"API: create_user() duplicate resource error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        logger.warning(f"API: create_user() validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"API: create_user() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/email/{email}", response_model=List[UserResponse])
async def get_users_by_email(
    email: str, user_service: UserService = Depends(get_user_service)
):
    """Get users by email."""
    logger.info(f"API: get_users_by_email() called with email='{email}'")

    try:
        users = await user_service.get_users_by_email(email)
        logger.info(
            f"API: get_users_by_email() found {len(users)} users with email '{email}'"
        )
        return users

    except NotFoundError as e:
        logger.warning(f"API: get_users_by_email() no users found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_users_by_email() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/name/{name}", response_model=List[UserResponse])
async def get_users_by_name(
    name: str, user_service: UserService = Depends(get_user_service)
):
    """Get users by name."""
    logger.info(f"API: get_users_by_name() called with name='{name}'")

    try:
        users = await user_service.get_users_by_name(name)
        logger.info(
            f"API: get_users_by_name() found {len(users)} users with name '{name}'"
        )
        return users

    except NotFoundError as e:
        logger.warning(f"API: get_users_by_name() no users found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"API: get_users_by_name() unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
