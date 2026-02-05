"""
Simple test of the new context manager approach.
"""

import asyncio
import pytest
from app.core.database import get_database_client
from app.repositories.movie_repository import MovieRepository


@pytest.mark.asyncio
async def test_context_manager():
    """Test the context manager approach."""
    print("TEST: Testing context manager approach...")

    try:
        # Test repository that uses context manager
        movie_repo = MovieRepository()

        # This should work - each call creates its own connection
        async with get_database_client() as client:
            print("SUCCESS: Database connection established")
            # You can now use client directly
            db = client["sample_mflix"]
            stats = await db.command("ping")
            print(f"STATS: Database stats: {stats}")

        print("SUCCESS: Connection closed automatically")

        # Test repository method
        movies = await movie_repo.find_many(limit=5)
        print(f"Movies: Found {len(movies)} movies using repository")

    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    asyncio.run(test_context_manager())
