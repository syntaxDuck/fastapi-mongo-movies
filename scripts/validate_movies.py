# from ..backend.repositories.base import BaseRepository
from backend.repositories.movie_repository import MovieRepository
from backend.core.database import DatabaseManager
import asyncio

import requests


LOGGING_ENABLED = False

if LOGGING_ENABLED:
    import logging

    logging.basicConfig(level=logging.INFO)


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

        retries = 0
        while retries < 100:
            try:
                r = requests.get(str(movie.poster))
                if r.status_code != 200:
                    broken.append(movie)
                else:
                    verified.append(movie)
                print(
                    f"{count} - {movie.title}:{movie.id} poster url returned {r.status_code}"
                )
                break
            except Exception:
                print(f"{count} - {movie.title}:{movie.id} Error getting poster")

            retries += 1

    print(f"{len(verified)} movies with verified posters")
    print(f"{len(broken)} movies with broken posters")

    failed = []
    for movie in broken:
        try:
            update_query = {"$set": {"valid_poster": False}}
            await mr.update_one({"id": movie.id}, update_query)
            print(f"Updating {movie.title}:{movie.id} to have a invalid poster")
        except Exception as e:
            print(f"Unable to update {movie.title}:{movie.id} - {e}")
            failed.append(movie)

    for movie in verified:
        try:
            update_query = {"$set": {"valid_poster": True}}
            await mr.update_one({"id": movie.id}, update_query)
            print(f"Updating {movie.title}:{movie.id} to have a valid poster")
        except Exception as e:
            print(f"Unable to update {movie.title}:{movie.id} - {e}")
            failed.append(movie)

    print(f"\n\n\n\n{failed}")
    with open("failed_updated.txt", "w") as file:
        for movie in failed:
            file.write("\n".join(map(str, failed)))

    await DatabaseManager.close_all_connections()


if __name__ == "__main__":
    asyncio.run(main())
