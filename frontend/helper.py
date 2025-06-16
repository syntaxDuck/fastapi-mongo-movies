from fasthtml.common import *


def build_movie_list(movies):
    count = 0
    list_movies = []
    for movie in movies:
        list_movies.append(
            Li(
                Img(
                    src=movie["poster"],
                ),
                cls="movie",
                hx_get=f"/details/{count}",
                hx_target=".content",
                hx_swap="outerHTML",
                hx_trigger="click",
            )
        )
        count += 1

    return list_movies
