"""
Repository layer using context manager pattern.
"""

from typing import Dict, Any, List, Optional
from bson import ObjectId
from app.core.logging import get_logger
from ..core.database import get_database_client


class BaseRepository:
    """Base repository class using modern context manager approach."""

    def __init__(self, database_name: str, collection_name: str) -> None:
        self.database_name = database_name
        self.collection_name = collection_name

    async def get_collection(self, client):
        """Get collection with proper naming."""
        if self.collection_name is None:
            raise ValueError("Collection name must be specified")
        return client[self.database_name][self.collection_name]

    async def find_by_id(
        self, entity_id: str, id_field: str = "_id"
    ) -> Optional[Dict[str, Any]]:
        """Find a document by its ID using context manager."""

        try:
            filter_query = {id_field: ObjectId(entity_id)}
        except Exception:
            filter_query = {id_field: entity_id}

        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                documents = (
                    await collection.find(filter_query).limit(1).to_list(length=None)
                )
                return documents[0] if documents else None
            except Exception:
                return None

    async def find_many(
        self,
        filter_query: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        skip: int = 0,
    ) -> List[Dict[str, Any]]:
        """Find multiple documents matching filter using context manager."""
        if filter_query is None:
            filter_query = {}

        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                cursor = collection.find(filter_query).skip(skip).limit(limit)
                documents = await cursor.to_list(length=None)
                return documents
            except Exception:
                return []

    async def create_one(self, document: Dict[str, Any]) -> Optional[str]:
        """Create a single document using context manager."""
        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                result = await collection.insert_one(document)
                document_id = str(result.inserted_id)
                return document_id
            except Exception:
                return None

    async def update_many(
        self, filter_query: Dict[str, Any], update_query: Dict[str, Any]
    ) -> Optional[int]:
        """Update multiple documents using context manager."""
        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                result = await collection.update_many(filter_query, update_query)
                matched_count = result.matched_count if result else 0
                return matched_count
            except Exception:
                return None

    async def delete_many(self, filter_query: Dict[str, Any]) -> Optional[int]:
        """Delete multiple documents using context manager."""
        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                result = await collection.delete_many(filter_query)
                deleted_count = result.deleted_count if result else 0
                return deleted_count
            except Exception:
                return None
