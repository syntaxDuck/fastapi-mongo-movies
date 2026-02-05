"""
Repository layer using context manager pattern.
"""

from typing import Dict, Any, List, Optional
from bson import ObjectId
from ..core.database import get_database_client
from ..core.logging import get_logger

logger = get_logger(__name__)


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
        logger.debug(f"Finding {self.collection_name} by {id_field}: {entity_id}")

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
                result = documents[0] if documents else None
                if result:
                    logger.debug(
                        f"Found {self.collection_name} with {id_field}: {entity_id}"
                    )
                else:
                    logger.debug(
                        f"No {self.collection_name} found with {id_field}: {entity_id}"
                    )
                return result
            except Exception as e:
                logger.error(
                    f"Error finding {self.collection_name} by {id_field} {entity_id}: {e}"
                )
                return None

    async def find_many(
        self,
        filter_query: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = 10,
        skip: Optional[int] = 0,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """Find multiple documents matching filter using context manager."""
        if filter_query is None:
            filter_query = {}

        filter_query = self.convert_id(filter_query)

        # Handle parameter priority (kwargs can override defaults)
        final_limit = limit if limit is not None else kwargs.get("limit", 10)
        final_skip = skip if skip is not None else kwargs.get("skip", 0)

        logger.debug(
            f"Finding {self.collection_name} with filter: {filter_query}, limit: {final_limit}, skip: {final_skip}"
        )

        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                cursor = (
                    collection.find(filter_query).skip(final_skip).limit(final_limit)
                )
                documents = await cursor.to_list(length=None)
                logger.info(f"Found {len(documents)} {self.collection_name} documents")
                return documents
            except Exception as e:
                logger.error(
                    f"Error finding {self.collection_name} with filter {filter_query}: {e}"
                )
                return []

    async def find_distinct(
        self, field: str, filter_query: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Get all distinct values of a field."""
        if filter_query is None:
            filter_query = {}

        logger.debug(f"Getting distinct {field}")

        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                distinct_values = await collection.distinct(field, filter_query)
                logger.info(
                    f"Found {len(distinct_values)} distinct {field} values in {self.collection_name}"
                )
                return distinct_values
            except Exception as e:
                logger.error(
                    f"Error getting distinct {field} from {self.collection_name}: {e}"
                )
                return []

    async def create_one(self, document: Dict[str, Any]) -> Optional[str]:
        """Create a single document using context manager."""
        logger.debug(
            f"Creating {self.collection_name} document: {document.get('_id', 'new document')}"
        )

        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                result = await collection.insert_one(document)
                document_id = str(result.inserted_id)
                logger.info(
                    f"Successfully created {self.collection_name} with ID: {document_id}"
                )
                return document_id
            except Exception as e:
                logger.error(f"Error creating {self.collection_name} document: {e}")
                return None

    async def update_one(
        self, filter_query: Dict[str, Any], update_query: Dict[str, Any]
    ) -> Optional[int]:
        """Update multiple documents using context manager."""
        logger.debug(
            f"Updating {self.collection_name} with filter: {filter_query}, update: {update_query}"
        )

        filter_query = self.convert_id(filter_query)

        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                result = await collection.update_one(filter_query, update_query)
                matched_count = result.matched_count if result else 0
                logger.info(f"Updated {matched_count} {self.collection_name} documents")
                return matched_count
            except Exception as e:
                logger.error(
                    f"Error updating {self.collection_name} with filter {filter_query}: {e}"
                )
                return None

    async def update_many(
        self, filter_query: Dict[str, Any], update_query: Dict[str, Any]
    ) -> Optional[int]:
        """Update multiple documents using context manager."""
        logger.debug(
            f"Updating {self.collection_name} with filter: {filter_query}, update: {update_query}"
        )

        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                result = await collection.update_many(filter_query, update_query)
                matched_count = result.matched_count if result else 0
                logger.info(f"Updated {matched_count} {self.collection_name} documents")
                return matched_count
            except Exception as e:
                logger.error(
                    f"Error updating {self.collection_name} with filter {filter_query}: {e}"
                )
                return None

    async def delete_many(self, filter_query: Dict[str, Any]) -> Optional[int]:
        """Delete multiple documents using context manager."""
        logger.debug(f"Deleting {self.collection_name} with filter: {filter_query}")

        async with get_database_client() as client:
            try:
                collection = await self.get_collection(client)
                result = await collection.delete_many(filter_query)
                deleted_count = result.deleted_count if result else 0
                logger.info(f"Deleted {deleted_count} {self.collection_name} documents")
                return deleted_count
            except Exception as e:
                logger.error(
                    f"Error deleting {self.collection_name} with filter {filter_query}: {e}"
                )
                return None

    @staticmethod
    def convert_id(query: Dict[str, Any]):
        id = None
        if "id" in query:
            id = query.pop("id", None)

        if "_id" in query:
            id = query["_id"]

        if id and not isinstance(id, ObjectId):
            try:
                id = ObjectId(id)
            except Exception as e:
                id = id
                logger.warning(
                    f"Failed to convert movie_id to ObjectId: {id}, error: {e}"
                )

        if id:
            query["_id"] = id

        return query
