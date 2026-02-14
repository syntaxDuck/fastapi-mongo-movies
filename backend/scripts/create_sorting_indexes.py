"""
Database index creation script for optimal sorting performance.
This script creates indexes that support the new sorting functionality.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from backend.core.logging import get_logger
from backend.core.database import get_database_client
import os

logger = get_logger(__name__)

# Recommended indexes for optimal sorting performance
SORTING_INDEXES = [
    # Basic sorting indexes
    {"year": -1, "title": 1},  # Year-filtered results sorted by title
    {"imdb.rating": -1, "title": 1},  # Rating-filtered results sorted by title
    {"released": -1, "title": 1},  # Release date filtered results sorted by title
    {
        "num_mflix_comments": -1,
        "title": 1,
    },  # Popularity filtered results sorted by title
    # Genre-specific sorting
    {"genres": 1, "imdb.rating": -1},  # Genre-filtered results sorted by rating
    {"genres": 1, "year": -1},  # Genre-filtered results sorted by year
    {"genres": 1, "released": -1},  # Genre-filtered results sorted by release date
    {"genres": 1, "title": 1},  # Genre-filtered results sorted alphabetically
    # Type-specific sorting
    {"type": 1, "imdb.rating": -1},  # Type-filtered results sorted by rating
    {"type": 1, "year": -1},  # Type-filtered results sorted by year
    {"type": 1, "released": -1},  # Type-filtered results sorted by release date
    # Global sorting indexes (most commonly used)
    {"imdb.rating": -1},  # Global rating sorting
    {"year": -1},  # Global year sorting
    {"released": -1},  # Global release date sorting
    {"title": 1},  # Global alphabetical sorting
    {"num_mflix_comments": -1},  # Global popularity sorting
    {"lastupdated": -1},  # Global last updated sorting
    # Rotten Tomatoes sorting indexes
    {
        "tomatoes.viewer.rating": -1,
        "title": 1,
    },  # Tomatoes viewer rating sorted by title
    {
        "tomatoes.critic.rating": -1,
        "title": 1,
    },  # Tomatoes critic rating sorted by title
    {
        "imdb.rating": -1,
        "tomatoes.viewer.rating": -1,
    },  # Combined IMDB + Tomatoes viewer rating
]

# Existing indexes that should be preserved (don't recreate)
EXISTING_INDEXES = [
    {"_id": 1},  # Default MongoDB index
    # Add any other existing indexes here
]


async def create_sorting_indexes():
    """Create indexes for optimal sorting performance."""
    logger.info("Starting database index creation for sorting performance...")

    try:
        async with get_database_client() as client:
            db = client.sample_mflix
            collection = db.movies

            # Get existing indexes to avoid duplicates
            existing_indexes = await collection.list_indexes()
            existing_index_specs = [idx["key"] for idx in existing_indexes]

            logger.info(f"Found {len(existing_indexes)} existing indexes")

            created_count = 0
            skipped_count = 0

            for index_spec in SORTING_INDEXES:
                # Check if index already exists
                if index_spec in existing_index_specs:
                    logger.debug(f"Index already exists: {index_spec}")
                    skipped_count += 1
                    continue

                try:
                    # Create the index
                    index_name = (
                        f"idx_{'_'.join(f'{k}_{v}' for k, v in index_spec.items())}"
                    )
                    await collection.create_index(
                        list(index_spec.items()),
                        name=index_name,
                        background=True,  # Don't block other operations
                    )
                    logger.info(f"Created index: {index_name} -> {index_spec}")
                    created_count += 1

                except Exception as e:
                    logger.error(f"Failed to create index {index_spec}: {e}")
                    continue

            logger.info(
                f"Index creation completed: {created_count} created, {skipped_count} skipped"
            )

            # Log final index status
            final_indexes = await collection.list_indexes()
            logger.info(f"Total indexes on movies collection: {len(final_indexes)}")

            for idx in final_indexes:
                logger.info(f"  - {idx['name']}: {idx['key']}")

            return created_count

    except Exception as e:
        logger.error(f"Failed to create sorting indexes: {e}")
        raise


async def drop_sorting_indexes():
    """Drop all sorting-related indexes (for cleanup/testing)."""
    logger.info("Dropping sorting indexes...")

    try:
        async with get_database_client() as client:
            db = client.sample_mflix
            collection = db.movies

            # Get existing indexes
            existing_indexes = await collection.list_indexes()

            dropped_count = 0
            for idx in existing_indexes:
                index_name = idx["name"]

                # Skip default MongoDB indexes
                if index_name in ["_id_"]:
                    logger.debug(f"Skipping protected index: {index_name}")
                    continue

                # Skip non-sorting indexes (add more as needed)
                if not any(
                    key in index_name
                    for key in [
                        "year",
                        "rating",
                        "released",
                        "title",
                        "comments",
                        "updated",
                        "tomatoes",
                        "imdb",
                    ]
                ):
                    logger.debug(f"Skipping non-sorting index: {index_name}")
                    continue

                try:
                    await collection.drop_index(index_name)
                    logger.info(f"Dropped index: {index_name}")
                    dropped_count += 1
                except Exception as e:
                    logger.error(f"Failed to drop index {index_name}: {e}")
                    continue

            logger.info(f"Index dropping completed: {dropped_count} indexes dropped")
            return dropped_count

    except Exception as e:
        logger.error(f"Failed to drop sorting indexes: {e}")
        raise


async def get_index_stats():
    """Get statistics about current indexes."""
    logger.info("Getting index statistics...")

    try:
        async with get_database_client() as client:
            db = client.sample_mflix
            collection = db.movies

            # Get collection stats
            stats = await db.command("collStats", "movies")
            logger.info(
                f"Collection stats: {stats['count']} documents, {stats['size']} bytes"
            )

            # Get index stats
            indexes = await collection.list_indexes()
            logger.info(f"Total indexes: {len(indexes)}")

            for idx in indexes:
                logger.info(f"  - {idx['name']}: {idx['key']}")

            return {
                "document_count": stats["count"],
                "collection_size": stats["size"],
                "index_count": len(indexes),
                "indexes": [
                    {"name": idx["name"], "key": idx["key"]} for idx in indexes
                ],
            }

    except Exception as e:
        logger.error(f"Failed to get index stats: {e}")
        raise


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "create":
            asyncio.run(create_sorting_indexes())
        elif command == "drop":
            asyncio.run(drop_sorting_indexes())
        elif command == "stats":
            asyncio.run(get_index_stats())
        else:
            print("Usage: python create_sorting_indexes.py [create|drop|stats]")
    else:
        # Default: create indexes
        asyncio.run(create_sorting_indexes())
