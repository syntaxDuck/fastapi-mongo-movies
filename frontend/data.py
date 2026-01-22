# import requests
from config import config
from api.models import MovieQuery, CommentQuery


def fetch_movies(query: MovieQuery = MovieQuery()):
    url = f"{config.API_URL}/movies"
    data = requests.get(url, params=query.model_dump(exclude_none=True, by_alias=True))
    return data.json()


def fetch_comments(query: CommentQuery = CommentQuery()):
    url = f"{config.API_URL}/comments"
    data = requests.get(url, params=query.model_dump(exclude_none=True, by_alias=True))
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
