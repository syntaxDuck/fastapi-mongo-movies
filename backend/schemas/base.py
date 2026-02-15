from typing import Any

from bson import ObjectId

from backend.core.logging import get_logger

logger = get_logger(__name__)


class MongoQuery:
    @staticmethod
    def convert_id(query: dict[str, Any]) -> dict[str, Any]:
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
