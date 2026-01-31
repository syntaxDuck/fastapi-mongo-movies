from fasthtml.common import Nav, Ul, Li, Div, Img, B, P


def NavBar():
    return Nav(
        Ul(
            Li(
                "Home",
                hx_get="/",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_target=".content",
            ),
            Li(
                "Movies",
                hx_get="/movies",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_target=".content",
            ),
            Li(
                "Users",
                hx_get="/users",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_target=".content",
            ),
            Li(
                "Comments",
                hx_get="/comments",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_target=".content",
            ),
            Li(
                "Genres",
                hx_get="/genres",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_target=".content",
            ),
            Li(
                "Directors",
                hx_get="/directors",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_target=".content",
            ),
            Li(
                "Top Rated",
                hx_get="/top-rated",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_target=".content",
            ),
            Li(
                "Recent",
                hx_get="/recent",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_target=".content",
            ),
            Li(
                "About",
                hx_get="/about",
                hx_trigger="click",
                hx_swap="outerHTML",
                hx_target=".content",
            ),
            cls="nav-list",
        ),
        cls="nav-bar",
    )


def Rating(rating, review_count, source, style_class):
    return Div(
        Img(src=source),
        Div(
            B(f"{rating} / 10"),
            P(f"Votes: {review_count}" if review_count else "No votes"),
            cls="rating-info",
        ),
        cls=style_class,
    )


def TomatoesCriticRating(tomatoes_obj):
    if "critic" in tomatoes_obj and tomatoes_obj["critic"] is not None:
        return Rating(
            tomatoes_obj["critic"]["rating"],
            tomatoes_obj["critic"]["numReviews"],
            "frontend/assets/tomatoe.png",
            "tomatoes-critic-rating",
        )
    return ""


def TomatoesViewerRating(tomatoes_obj):
    if "viewer" in tomatoes_obj and tomatoes_obj["viewer"] is not None:
        return Rating(
            tomatoes_obj["viewer"]["rating"],
            tomatoes_obj["viewer"]["numReviews"],
            "frontend/assets/popcorn.png",
            "tomatoes-viewer-rating",
        )
    return ""


def ImdbRating(movie):
    if "imdb" in movie and movie["imdb"] is not None:
        return Rating(
            movie["imdb"]["rating"],
            movie["imdb"]["votes"],
            "frontend/assets/imdb.png",
            "imdb-rating",
        )
    return ""
