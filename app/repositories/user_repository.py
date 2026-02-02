"""
User Repository layer using context manager pattern.
"""

from typing import Dict, Any, List, Optional
from bson import ObjectId
from .base import BaseRepository
from app.core.logging import get_logger

logger = get_logger(__name__)


class UserRepository(BaseRepository):
    """Repository for user data operations."""

    def __init__(self) -> None:
        super().__init__("sample_mflix", "users")

    async def find_by_id(
        self, entity_id: str, id_field: str = "_id"
    ) -> Optional[Dict[str, Any]]:
        """Find a user by their ID."""
        logger.debug(
            f"UserRepository.find_by_id() called with entity_id={entity_id}, id_field={id_field}"
        )
        return await super().find_by_id(entity_id, id_field)

    async def find_by_email(self, email: str, **kwargs) -> List[Dict[str, Any]]:
        """Find users by email."""
        logger.debug(f"UserRepository.find_by_email() called with email={email}")
        filter_query = {"email": email}
        return await self.find_many(filter_query, **kwargs)

    async def find_by_name(self, name: str, **kwargs) -> List[Dict[str, Any]]:
        """Find users by name."""
        logger.debug(f"UserRepository.find_by_name() called with name={name}")
        filter_query = {"name": name}
        return await self.find_many(filter_query, **kwargs)

    async def email_exists(self, email: str) -> bool:
        """Check if a user with given email exists."""
        logger.debug(f"UserRepository.email_exists() called with email={email}")
        users = await self.find_by_email(email)
        exists = len(users) > 0
        logger.debug(f"UserRepository.email_exists() result for {email}: {exists}")
        return exists

    async def search_users(self, **kwargs) -> List[Dict[str, Any]]:
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
        return await self.find_many(filter_query, **kwargs)
