from fasthtml.common import Div, H1, P, Img, B, Hr
from .ganeric import TomatoesCriticRating, TomatoesViewerRating, ImdbRating


def MovieDetail(name, key, item):
    if key not in item or item[key] is None:
        return (P(B(f"{name}:  "), "N/A"),)

    if not isinstance(item[key], list):
        item[key] = [item[key]]

    return (P(B(f"{name}:  "), ", ".join(item[key])),)


def MovieDetailsHeader(movie):
    data = f"{movie['year']}・{movie['runtime'] // 60}h {movie['runtime'] % 60}m"
    return (
        Div(
            H1(movie["title"]),
            Div(P(data)),
            cls="movie-details-header",
        ),
    )


def MovieDetailsBody(movie):
    tomatoes_critic = TomatoesCriticRating(movie.get("tomatoes", {}))
    tomatoes_viewer = TomatoesViewerRating(movie.get("tomatoes", {}))
    imdb = ImdbRating(movie)
    return Div(
        Img(src=movie["poster"], cls="movie-details-poster"),
        Div(
            MovieDetail("Genres", "genres", movie),
            Hr(),
            MovieDetail("Directors", "directors", movie),
            Hr(),
            MovieDetail("Writers", "writers", movie),
            Hr(),
            MovieDetail("Cast", "cast", movie),
            Hr(),
            MovieDetail("Countries", "countries", movie),
            Hr(),
            Div(imdb, tomatoes_critic, tomatoes_viewer, cls="movie-details-ratings"),
            cls="movie-details-info",
        ),
        cls="movie-details-body",
    )


def MoviePlot(movie):
    if movie["fullplot"] is not None and len(movie["fullplot"]) > 0:
        plot = P(movie["fullplot"])
    else:
        plot = P(movie["plot"])

    return Div(
        plot,
        cls="movie-details-plot",
    )


def MovieDetails(movie):
    return Div(
        MovieDetailsHeader(movie),
        MovieDetailsBody(movie),
        MoviePlot(movie),
        cls="movie-details",
    )
