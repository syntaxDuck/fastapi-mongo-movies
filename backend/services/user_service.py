"""
User Service layer for business logic using proper protocol-based dependency injection.
"""


from ..core.exceptions import DatabaseError, DuplicateResourceError, NotFoundError
from ..core.logging import get_logger
from ..core.security import hash_password
from ..repositories.protocol import UserRepositoryProtocol
from ..schemas.schemas import MessageResponse, UserCreate, UserResponse

logger = get_logger(__name__)


class UserService:
    """Service layer for user business logic."""

    def __init__(self, user_repository: UserRepositoryProtocol) -> None:
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: str) -> UserResponse:
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
        user_id: str | None = None,
        name: str | None = None,
        email: str | None = None,
        limit: int = 10,
        skip: int = 0,
    ) -> list[UserResponse]:
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

    async def create_user(self, user_data: UserCreate) -> MessageResponse:
        """Create a new user."""
        email = user_data.email
        if not email:
            logger.error("Create user failed: Email is required")
            raise ValueError("Email is required")

        logger.debug(f"Creating user with email: {email}")

        if email and (" " in email or not email.count("@") or not email.count(".")):
            logger.warning(
                f"UserService.create_user() clearly invalid email format: '{email}'"
            )

        password = user_data.password
        if len(password) < 6:
            logger.warning(
                f"UserService.create_user() weak password: length={len(password)} for email='{email}'"
            )
        if len(password) > 100:
            logger.warning(
                f"UserService.create_user() excessive password length: {len(password)} for email='{email}'"
            )
        if password.lower() in [
            "password",
            "123456",
            "qwerty",
            "admin",
            "letmein",
            "welcome",
        ]:
            logger.warning(
                f"UserService.create_user() common insecure password used for email='{email}'"
            )

        name = user_data.name
        if len(password) == len(name) and password.lower() == name.lower():
            logger.warning(
                f"UserService.create_user() password same as username for email='{email}'"
            )

        if name:
            if len(name.strip()) < 1:
                logger.warning(
                    f"UserService.create_user() empty name for email='{email}'"
                )
            if len(name) > 100:
                logger.warning(
                    f"UserService.create_user() long name: {len(name)} characters for email='{email}'"
                )
            if name.lower() in [
                "admin",
                "administrator",
                "root",
                "test",
                "user",
                "guest",
            ]:
                logger.warning(
                    f"UserService.create_user() potentially problematic name: '{name}' for email='{email}'"
                )
        else:
            logger.warning(
                f"UserService.create_user() missing name for email='{email}'"
            )

        if await self.user_repository.email_exists(email):
            logger.warning(
                f"UserService.create_user() failed: Email '{email}' already exists"
            )
            raise DuplicateResourceError(f"User with email '{email}' already exists")

        # Hash the password before storing
        user_data.password = hash_password(user_data.password)

        user_id = await self.user_repository.create_user(user_data)
        if not user_id:
            logger.error(
                f"UserService.create_user() failed: Could not create user with email: {email}"
            )
            raise DatabaseError("Failed to create user")

        logger.info(
            f"UserService.create_user() successfully created user with ID: {user_id}"
        )
        return user_id

    async def get_users_by_email(self, email: str) -> list[UserResponse]:
        """Get users by email."""
        logger.debug(f"Getting users by email: {email}")

        users = await self.user_repository.find_by_email(email)
        if not users:
            logger.info(f"No users found with email: {email}")
            raise NotFoundError(f"No users found with email '{email}'")

        logger.info(f"Found {len(users)} users with email: {email}")
        return users

    async def get_users_by_name(self, name: str) -> list[UserResponse]:
        """Get users by name."""
        logger.debug(f"Getting users by name: {name}")

        users = await self.user_repository.find_by_name(name)
        if not users:
            logger.info(f"No users found with name: {name}")
            raise NotFoundError(f"No users found with name '{name}'")

        logger.info(f"Found {len(users)} users with name: {name}")
        return users
