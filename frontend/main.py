from fasthtml.common import *
from .components import movie_details, movie_list, rating, detail
from .data import fetch_movies, process_movies, fetch_comments
from .helper import build_movie_list
from config import config

hdrs = []
hdrs.append(Link(rel="stylesheet", href="frontend/assets/styles.css"))

app, rt = fast_app(live=True, hdrs=hdrs)

movies = []


@app.route("/", methods="get")
def home():
    global movies
    movies = []
    return Div(movie_list(), movie_details(), cls="box")


@app.get("/details/{index}")
def get_details(index: int):
    movie = movies[index]

    info_data = f'{movie["year"]}・{movie["runtime"] // 60}h {movie["runtime"] % 60}m'

    if "tomatoes" in movie:
        tomatoes_obj = movie["tomatoes"]

        tomatoes_critic = ""
        if "critic" in tomatoes_obj and tomatoes_obj["critic"] is not None:
            tomatoes_critic = rating(
                tomatoes_obj["critic"]["rating"],
                tomatoes_obj["critic"]["numReviews"],
                "frontend/assets/tomatoe.png",
                "tomatoes-critic-rating",
            )

        tomatoes_viewer = ""
        if "viewer" in tomatoes_obj and tomatoes_obj["viewer"] is not None:
            tomatoes_viewer = rating(
                tomatoes_obj["viewer"]["rating"],
                tomatoes_obj["viewer"]["numReviews"],
                "frontend/assets/popcorn.png",
                "tomatoes-viewer-rating",
            )

    imdb = ""
    if "imdb" in movie and movie["imdb"] is not None:
        imdb = rating(
            movie["imdb"]["rating"],
            movie["imdb"]["votes"],
            "frontend/assets/imdb.png",
            "imdb-rating",
        )

    raw_comments = fetch_comments(movie["_id"], 0)
    comments = Ul(*raw_comments)

    return Div(
        Div(
            Div(
                H1(movie["title"]),
                Div(P(info_data)),
                cls="details-header-info",
            ),
            Div(
                Img(src=movie["poster"], cls="details-poster"),
                Div(
                    detail("Genres", "genres", movie),
                    Hr(),
                    detail("Directors", "directors", movie),
                    Hr(),
                    detail("Writers", "writers", movie),
                    Hr(),
                    detail("Cast", "cast", movie),
                    Hr(),
                    detail("Countries", "countries", movie),
                    Div(imdb, tomatoes_critic, tomatoes_viewer, cls="ratings"),
                    cls="details-info",
                ),
                cls="details-header-body",
            ),
            cls="details-header",
        ),
        Br(),
        (
            P(movie["fullplot"])
            if movie["fullplot"] is not None and len(movie["fullplot"]) > 0
            else P(movie["plot"])
        ),
        comments,
        cls="movie-details",
    )


@app.get("/comments/{movie_id}")
def get_comments(movie_id: str):
    raw_comments = fetch_comments(movie_id, 0)
    return Ul(*raw_comments)


@app.get("/movies")
def get_movies():
    global movies

    page = len(movies) // config.MOVIE_PAGE_SIZE
    raw_movies = fetch_movies(page)
    new_movies = process_movies(raw_movies)
    movies += new_movies

    return build_movie_list(movies)


serve()
