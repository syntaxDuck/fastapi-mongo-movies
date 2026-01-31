import requests
from app.core.config import settings


def fetch_movies(query_params: dict | None = None):
    """Fetch movies from the API."""
    if query_params is None:
        query_params = {}

    url = f"{settings.API_URL}/movies"
    data = requests.get(url, params=query_params)
    return data.json()


def fetch_comments(query_params: dict | None = None):
    """Fetch comments from the API."""
    if query_params is None:
        query_params = {}

    url = f"{settings.API_URL}/comments"
    data = requests.get(url, params=query_params)
    return data.json()


def process_movies(movies: list):
    default_img = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg"
    for movie in movies:
        if movie["poster"]:
            response = requests.head(movie["poster"], allow_redirects=False)
            if response.status_code != 200:
                movie["poster"] = default_img
        else:
            movie["poster"] = default_img

    return movies
