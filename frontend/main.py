from fasthtml.common import Link, Div, P, Ul, fast_app
from fasthtml import serve
from .components.ganeric import NavBar
from .components.movie_details import MovieDetails
from .components.movie_list import MovieList
from .data import fetch_movies, process_movies, fetch_comments
from .helper import build_movie_list
from app.core.config import settings

hdrs = Link(rel="stylesheet", href="frontend/assets/styles.css")

app, rt = fast_app(live=True, hdrs=hdrs)

movies = []


@rt
def index():
    global movies
    movies = []
    return Div(
        MovieList(),
        Div(NavBar(), Div(cls="content"), cls="view-port"),
        cls="main-container",
    )


@rt
def hello():
    return Div(P("Goodbye"))


@app.get("/details/{index}")
def details(index: int):
    movie = movies[index]

    return MovieDetails(movie)
    # #TODO: Finish comment loading
    # # raw_comments = fetch_comments(movie["_id"], 0)
    # # comments = Ul(*[Li(comment["name"]) for comment in raw_comments])
    # comments = None


@app.get("/comments/{movie_id}")
def get_comments(movie_id: str):
    raw_comments = fetch_comments({"movie_id": movie_id})
    return Ul(*raw_comments)


@app.get("/movies")
def get_movies():
    global movies

    page = len(movies) // settings.MOVIE_LIST_PAGE_SIZE
    query_params = {
        "type": "movie",
        "skip": page * settings.MOVIE_LIST_PAGE_SIZE,
        "limit": settings.MOVIE_LIST_PAGE_SIZE,
    }
    raw_movies = fetch_movies(query_params)
    new_movies = process_movies(raw_movies)
    movies += new_movies

    return build_movie_list(movies)


serve()
