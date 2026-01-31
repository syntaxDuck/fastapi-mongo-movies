from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from ...schemas.movie import UserResponse, UserQuery, UserCreate, MessageResponse
from ...services.movie_service import UserService
from ...repositories.movie_repository import UserRepository
from ...core.exceptions import NotFoundError, DuplicateResourceError

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
    try:
        users = await user_service.get_users(
            user_id=query.id,
            name=query.name,
            email=query.email,
            limit=query.limit or 10,
            skip=query.skip or 0,
        )

        return [UserResponse.from_dict(user) for user in users]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str, user_service: UserService = Depends(get_user_service)
):
    """Get a specific user by ID."""
    try:
        user = await user_service.get_user_by_id(user_id)
        return UserResponse.from_dict(user)

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=MessageResponse)
async def create_user(
    user_data: UserCreate, user_service: UserService = Depends(get_user_service)
):
    """
    Create a new user.

    - **name**: User name (required, 1-100 characters)
    - **email**: User email (required, must be valid email)
    - **password**: User password (required, 6-100 characters)
    """
    try:
        user_id = await user_service.create_user(user_data.model_dump())
        return MessageResponse(message=f"User created successfully: {user_id}")

    except DuplicateResourceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/email/{email}", response_model=List[UserResponse])
async def get_users_by_email(
    email: str, user_service: UserService = Depends(get_user_service)
):
    """Get users by email."""
    try:
        users = await user_service.get_users_by_email(email)
        return [UserResponse.from_dict(user) for user in users]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/name/{name}", response_model=List[UserResponse])
async def get_users_by_name(
    name: str, user_service: UserService = Depends(get_user_service)
):
    """Get users by name."""
    try:
        users = await user_service.get_users_by_name(name)
        return [UserResponse.from_dict(user) for user in users]

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
