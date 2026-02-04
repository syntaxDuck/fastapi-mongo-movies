# from ..app.repositories.base import BaseRepository
from app.repositories.movie_repository import MovieRepository
from app.core.database import DatabaseManager
import asyncio
import logging
import requests


# logging.basicConfig(level=logging.INFO)


async def main():
    await DatabaseManager.get_client()
    mr = MovieRepository()
    movies = await mr.search_movies(limit=0)
    verified = []
    broken = []
    count = 0
    for movie in movies:
        count += 1
        if not movie.poster:
            broken.append(movie)
            print(f"{count} - {movie.title}:{movie.id} doesn't have a poster")
            continue

        try:
            r = requests.get(str(movie.poster))
            if r.status_code != 200:
                broken.append(movie)
            verified.append(movie)
            print(
                f"{count} - {movie.title}:{movie.id} poster url returned {r.status_code}"
            )
        except Exception:
            broken.append(movie)
            print(f"{count} - {movie.title}:{movie.id} Error getting poster")

    print(f"{len(verified)} movies with verified posters")
    print(f"{len(broken)} movies with broken posters")

    await DatabaseManager.close_all_connections()


if __name__ == "__main__":
    asyncio.run(main())
