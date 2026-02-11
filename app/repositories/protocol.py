"""
Repository protocol definitions for type safety and dependency injection.
"""

from typing import Protocol, Dict, Any, List, Optional, runtime_checkable

from app.schemas.schemas import (
    MessageResponse,
    MovieResponse,
    CommentResponse,
    UserCreate,
    UserResponse,
)


@runtime_checkable
class RepositoryProtocol(Protocol):
    """Protocol defining the interface for repository operations."""

    database_name: str
    collection_name: str

    async def _find_by_id(self, id: str) -> Optional[Dict[str, Any]]: ...
    async def _find_many(
        self,
        filter_query: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        skip: int = 0,
        **kwargs,
    ) -> List[Dict[str, Any]]: ...
    async def _find_distinct(
        self, field: str, filter_query: Optional[Dict[str, Any]] = None
    ) -> List[str]: ...
    async def _create_one(self, document: Dict[str, Any]) -> Optional[str]: ...
    async def _update_one(
        self, filter_query: Dict[str, Any], update_query: Dict[str, Any]
    ) -> Optional[int]: ...
    async def _update_many(
        self, filter_query: Dict[str, Any], update_query: Dict[str, Any]
    ) -> Optional[int]: ...
    async def _delete_many(self, filter_query: Dict[str, Any]) -> Optional[int]: ...


@runtime_checkable
class MovieRepositoryProtocol(RepositoryProtocol, Protocol):
    """Protocol for movie-specific repository operations."""

    async def search_movies(self, **kwargs) -> List[MovieResponse]: ...
    async def search_movies_by_text(
        self, search_text: str, **kwargs
    ) -> List[MovieResponse]: ...
    async def find_by_id(self, id: str, **kwargs) -> Optional[MovieResponse]: ...
    async def find_by_type(
        self, type: str, include_invalid_posters: bool = False, **kwargs
    ) -> List[MovieResponse]: ...
    async def find_by_year(
        self, year: int, mod: str, include_invalid_posters: bool = False, **kwargs
    ) -> List[MovieResponse]: ...
    async def find_by_rating(
        self, rating: int, mod: str, include_invalid_posters: bool = False, **kwargs
    ) -> List[MovieResponse]: ...
    async def find_by_genre(self, genre: str, **kwargs) -> List[MovieResponse]: ...
    async def get_all_genres(self) -> List[str]: ...
    async def get_all_types(self) -> List[str]: ...


@runtime_checkable
class UserRepositoryProtocol(RepositoryProtocol, Protocol):
    """Protocol for user-specific repository operations."""

    async def search_users(self, **kwargs) -> List[UserResponse]: ...
    async def find_by_id(self, id: str, **kwargs) -> Optional[UserResponse]: ...
    async def find_by_email(self, email: str, **kwargs) -> List[UserResponse]: ...
    async def find_by_name(self, name: str, **kwargs) -> List[UserResponse]: ...
    async def email_exists(self, email: str) -> bool: ...
    async def create_user(
        self, user_data: UserCreate | Dict[str, Any]
    ) -> Optional[MessageResponse]: ...


@runtime_checkable
class CommentRepositoryProtocol(RepositoryProtocol, Protocol):
    """Protocol for comment-specific repository operations."""

    async def search_comments(self, **kwargs) -> List[CommentResponse]: ...
    async def find_by_id(self, id: str, **kwargs) -> Optional[CommentResponse]: ...
    async def find_by_movie_id(
        self, movie_id: str, **kwargs
    ) -> List[CommentResponse]: ...
    async def find_by_email(self, email: str, **kwargs) -> List[CommentResponse]: ...
    async def find_by_name(self, name: str, **kwargs) -> List[CommentResponse]: ...
