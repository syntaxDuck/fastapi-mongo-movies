"""
User Repository layer using context manager pattern.
"""

from typing import List, Optional, Any
from bson import ObjectId
from .base import BaseRepository
from app.core.logging import get_logger
from ..schemas.schemas import MessageResponse, UserCreate, UserResponse

logger = get_logger(__name__)


class UserRepository(BaseRepository):
    """Repository for user data operations."""

    def __init__(self) -> None:
        super().__init__("sample_mflix", "users")

    async def find_by_id(self, id: str, **kwargs) -> Optional[UserResponse]:
        """Find a user by their ID."""
        logger.debug(
            f"UserRepository.find_by_id() called with id={id}, kwargs={kwargs}"
        )
        user = await self._find_by_id(id, **kwargs)
        if user:
            logger.debug(
                f"UserRepository.find_by_id() found user: {user.get('name', 'Unknown')} ({user.get('email', 'Unknown Email')})"
            )
        else:
            logger.debug(f"UserRepository.find_by_id() no user found with id={id}")
        return UserResponse.from_dict(user) if user else None

    async def find_by_email(self, email: str, **kwargs) -> List[UserResponse]:
        """Find users by email."""
        logger.debug(
            f"UserRepository.find_by_email() called with email='{email}', kwargs={kwargs}"
        )
        filter_query = {"email": email}
        logger.debug(f"UserRepository.find_by_email() executing query: {filter_query}")
        users = await self._find_many(filter_query, **kwargs)
        logger.debug(
            f"UserRepository.find_by_email() found {len(users)} users with email '{email}'"
        )
        return [UserResponse.from_dict(user) for user in users]

    async def find_by_name(self, name: str, **kwargs) -> List[UserResponse]:
        """Find users by name."""
        logger.debug(
            f"UserRepository.find_by_name() called with name='{name}', kwargs={kwargs}"
        )
        filter_query = {"name": name}
        logger.debug(f"UserRepository.find_by_name() executing query: {filter_query}")
        users = await self._find_many(filter_query, **kwargs)
        logger.debug(
            f"UserRepository.find_by_name() found {len(users)} users with name '{name}'"
        )
        return [UserResponse.from_dict(user) for user in users]

    async def email_exists(self, email: str) -> bool:
        """Check if a user with given email exists."""
        logger.debug(f"UserRepository.email_exists() called with email={email}")
        users = await self.find_by_email(email)
        exists = len(users) > 0
        logger.debug(f"UserRepository.email_exists() result for {email}: {exists}")
        return exists

    async def search_users(self, **kwargs) -> List[UserResponse]:
        """Search users with multiple filters."""
        logger.debug(f"UserRepository.search_users() called with kwargs: {kwargs}")
        filter_query = {}

        if "user_id" in kwargs:
            try:
                filter_query["_id"] = ObjectId(kwargs["user_id"])
                logger.debug(f"Added user_id filter: {kwargs['user_id']}")
            except Exception as e:
                logger.warning(
                    f"Failed to convert user_id to ObjectId: {kwargs.get('user_id')}, error: {e}"
                )

        if "name" in kwargs:
            filter_query["name"] = kwargs["name"]
            logger.debug(f"Added name filter: {kwargs['name']}")

        if "email" in kwargs:
            filter_query["email"] = kwargs["email"]
            logger.debug(f"Added email filter: {kwargs['email']}")

        logger.debug(f"Final user filter_query: {filter_query}")
        users = await self._find_many(filter_query, **kwargs)
        return [UserResponse.from_dict(user) for user in users]

    async def create_user(
        self, user_data: UserCreate | dict[str, Any]
    ) -> Optional[MessageResponse]:
        """Create a new user."""
        if hasattr(user_data, "model_dump"):
            user_data_dict = user_data.model_dump()
        else:
            user_data_dict = user_data
        logger.debug(
            f"UserRepository.create_user() called with user_data keys: {list(user_data_dict)}"
        )

        safe_user_data = {k: v for k, v in user_data_dict.items() if k != "password"}
        logger.debug(
            f"UserRepository.create_user() creating user with data: {safe_user_data}"
        )

        if not user_data_dict.get("email"):
            logger.warning("UserRepository.create_user() missing email in user_data")

        user_id = await self._create_one(user_data_dict)
        if user_id:
            logger.debug(
                f"UserRepository.create_user() successfully created user with ID: {user_id}"
            )
        else:
            logger.error("UserRepository.create_user() failed to create user")

        return MessageResponse(message=str(user_id))
