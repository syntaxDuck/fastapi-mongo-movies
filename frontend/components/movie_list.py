from fasthtml.common import Ul, Div, Button


def MovieList():
    return Div(
        Ul(
            cls="movie-list",
            hx_get="/movies",
            hx_trigger="load",
            hx_swap="innerHTML",
        ),
        Button(
            "Next ▷",
            hx_get="/movies",
            hx_target=".movie-list",
            hx_swap="innerHTML",
        ),
        cls="movie-list-container",
    )
