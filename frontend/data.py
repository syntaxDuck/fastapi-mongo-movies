import requests
from config import config

def fetch_movies(page: int):
    url = f"{config.API_URL}/movies?limit=10&skip={page*config.MOVIE_PAGE_SIZE}"
    params = {"type": "movie"}
    data = requests.get(url, params=params)
    return data.json()


def fetch_comments(movie_id: str, page: int):
    url = f"{config.API_URL}/comments?limit=10&skip={page*config.MOVIE_PAGE_SIZE}"
    params = {"movie_id": movie_id}
    data = requests.get(url, params=params)
    return data.json()


def process_movies(movies: list):
    default_img = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg"
    for movie in movies:
        print(movie["poster"])
        if movie["poster"]:
            response = requests.head(movie["poster"], allow_redirects=False)
            if response.status_code != 200:
                movie["poster"] = default_img
        else:
            movie["poster"] = default_img

    return movies
