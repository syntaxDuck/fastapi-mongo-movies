"""
User Service layer for business logic using proper protocol-based dependency injection.
"""

from typing import List, Optional, Dict, Any
from ..repositories.protocol import UserRepositoryProtocol
from ..core.exceptions import NotFoundError, DatabaseError, DuplicateResourceError
from ..core.logging import get_logger

logger = get_logger(__name__)


class UserService:
    """Service layer for user business logic."""

    def __init__(self, user_repository: UserRepositoryProtocol) -> None:
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        """Get a user by their ID."""
        logger.debug(f"Getting user by ID: {user_id}")

        user = await self.user_repository.find_by_id(user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise NotFoundError(f"User with ID {user_id} not found")

        logger.debug(f"Successfully retrieved user: {user_id}")
        return user

    async def get_users(
        self,
        user_id: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        limit: int = 10,
        skip: int = 0,
    ) -> List[Dict[str, Any]]:
        """Get users with optional filtering."""
        logger.debug(
            f"Getting users with filters: user_id={user_id}, name={name}, "
            f"email={email}, limit={limit}, skip={skip}"
        )

        users = await self.user_repository.search_users(
            user_id=user_id, name=name, email=email, limit=limit, skip=skip
        )

        if not users:
            logger.info("No users found matching the criteria")
            raise NotFoundError("No users found matching the criteria")

        logger.info(f"Found {len(users)} users")
        return users

    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user."""
        email = user_data.get("email")
        if not email:
            logger.error("Create user failed: Email is required")
            raise ValueError("Email is required")

        logger.debug(f"Creating user with email: {email}")

        # Check if user with email already exists
        if await self.user_repository.email_exists(email):
            logger.warning(f"User creation failed: Email '{email}' already exists")
            raise DuplicateResourceError(f"User with email '{email}' already exists")

        user_id = await self.user_repository.create_one(user_data)
        if not user_id:
            logger.error(f"Failed to create user with email: {email}")
            raise DatabaseError("Failed to create user")

        logger.info(f"Successfully created user with ID: {user_id}")
        return user_id

    async def get_users_by_email(self, email: str) -> List[Dict[str, Any]]:
        """Get users by email."""
        logger.debug(f"Getting users by email: {email}")

        users = await self.user_repository.find_by_email(email)
        if not users:
            logger.info(f"No users found with email: {email}")
            raise NotFoundError(f"No users found with email '{email}'")

        logger.info(f"Found {len(users)} users with email: {email}")
        return users

    async def get_users_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Get users by name."""
        logger.debug(f"Getting users by name: {name}")

        users = await self.user_repository.find_by_name(name)
        if not users:
            logger.info(f"No users found with name: {name}")
            raise NotFoundError(f"No users found with name '{name}'")

        logger.info(f"Found {len(users)} users with name: {name}")
        return users
