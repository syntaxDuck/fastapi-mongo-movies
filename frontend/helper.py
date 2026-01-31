from fasthtml.common import Li, Img, Span


def build_movie_list(movies):
    count = 0
    list_movies = []
    for movie in movies:
        list_movies.append(
            Li(
                Img(
                    src=movie.get("poster", "https://via.placeholder.com/150x200"),
                ),
                Span(movie["title"], cls="movie-hover-text"),
                cls="movie",
                hx_get=f"/details/{count}",
                hx_target=".content",
                hx_swap="innerHTML",
                hx_trigger="click",
            )
        )
        count += 1

    return list_movies
