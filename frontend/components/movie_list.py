from fasthtml.common import *

def MovieList():
    return Div(
        Ul(
            cls="movie-list",
            hx_get=f"/movies",
            hx_trigger="load",
            hx_swap="innerHTML",
        ),
        Button(
            "Next ▷",
            hx_get=f"/movies",
            hx_target=".movie-list",
            hx_swap="innerHTML",
        ),
        cls="movie-list-container",
    )