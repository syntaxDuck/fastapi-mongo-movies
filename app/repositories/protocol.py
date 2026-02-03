"""
Repository protocol definitions for type safety and dependency injection.
"""

from typing import Protocol, Dict, Any, List, Optional, runtime_checkable


@runtime_checkable
class RepositoryProtocol(Protocol):
    """Protocol defining the interface for repository operations."""

    database_name: str
    collection_name: str

    async def find_by_id(
        self, entity_id: str, id_field: str = "_id"
    ) -> Optional[Dict[str, Any]]: ...
    async def find_many(
        self,
        filter_query: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        skip: int = 0,
        **kwargs,
    ) -> List[Dict[str, Any]]: ...
    async def find_distinct(
        self, field: str, filter_query: Optional[Dict[str, Any]] = None
    ) -> List[str]: ...
    async def create_one(self, document: Dict[str, Any]) -> Optional[str]: ...
    async def update_many(
        self, filter_query: Dict[str, Any], update_query: Dict[str, Any]
    ) -> Optional[int]: ...
    async def delete_many(self, filter_query: Dict[str, Any]) -> Optional[int]: ...


@runtime_checkable
class MovieRepositoryProtocol(RepositoryProtocol, Protocol):
    """Protocol for movie-specific repository operations."""

    async def search_movies(self, **kwargs) -> List[Dict[str, Any]]: ...
    async def find_by_type(self, movie_type: str, **kwargs) -> List[Dict[str, Any]]: ...
    async def find_by_year(self, year: int, **kwargs) -> List[Dict[str, Any]]: ...
    async def find_by_genre(self, genre: str, **kwargs) -> List[Dict[str, Any]]: ...
    async def get_genres(self) -> List[str]: ...


@runtime_checkable
class UserRepositoryProtocol(RepositoryProtocol, Protocol):
    """Protocol for user-specific repository operations."""

    async def search_users(self, **kwargs) -> List[Dict[str, Any]]: ...
    async def find_by_email(self, email: str, **kwargs) -> List[Dict[str, Any]]: ...
    async def find_by_name(self, name: str, **kwargs) -> List[Dict[str, Any]]: ...
    async def email_exists(self, email: str) -> bool: ...


@runtime_checkable
class CommentRepositoryProtocol(RepositoryProtocol, Protocol):
    """Protocol for comment-specific repository operations."""

    async def search_comments(self, **kwargs) -> List[Dict[str, Any]]: ...
    async def find_by_movie_id(
        self, movie_id: str, **kwargs
    ) -> List[Dict[str, Any]]: ...
    async def find_by_email(self, email: str, **kwargs) -> List[Dict[str, Any]]: ...
    async def find_by_name(self, name: str, **kwargs) -> List[Dict[str, Any]]: ...
