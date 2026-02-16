from unittest.mock import AsyncMock, patch

import pytest

from backend.services.movie_service import MovieService


@pytest.mark.asyncio
async def test_movie_service_genres_cache():
    # Reset cache
    MovieService._genres_cache = None
    MovieService._genres_cache_time = 0

    repo = AsyncMock()
    repo.get_all_genres.return_value = ["Action", "Comedy"]
    service = MovieService(repo)

    # First call - should hit repository
    genres1 = await service.get_all_genres()
    assert genres1 == ["Action", "Comedy"]
    assert repo.get_all_genres.call_count == 1

    # Second call - should hit cache
    genres2 = await service.get_all_genres()
    assert genres2 == ["Action", "Comedy"]
    assert repo.get_all_genres.call_count == 1

@pytest.mark.asyncio
async def test_movie_service_types_cache():
    # Reset cache
    MovieService._types_cache = None
    MovieService._types_cache_time = 0

    repo = AsyncMock()
    repo.get_all_types.return_value = ["movie", "series"]
    service = MovieService(repo)

    # First call - should hit repository
    types1 = await service.get_all_types()
    assert types1 == ["movie", "series"]
    assert repo.get_all_types.call_count == 1

    # Second call - should hit cache
    types2 = await service.get_all_types()
    assert types2 == ["movie", "series"]
    assert repo.get_all_types.call_count == 1

@pytest.mark.asyncio
async def test_movie_service_cache_ttl():
    # Reset cache
    MovieService._genres_cache = None
    MovieService._genres_cache_time = 0

    repo = AsyncMock()
    repo.get_all_genres.return_value = ["Action"]
    service = MovieService(repo)

    # Initial time
    start_time = 1000000.0

    with patch("time.time", return_value=start_time):
        # First call
        await service.get_all_genres()
        assert repo.get_all_genres.call_count == 1

        # Second call within TTL
        with patch("time.time", return_value=start_time + 1000.0):
            await service.get_all_genres()
            assert repo.get_all_genres.call_count == 1

        # Third call outside TTL
        with patch("time.time", return_value=start_time + 4000.0):
            await service.get_all_genres()
            assert repo.get_all_genres.call_count == 2
