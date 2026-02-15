from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, field_validator

from backend.core.logging import get_logger
from backend.schemas.base import MongoQuery

logger = get_logger(__name__)


class MovieQuery(MongoQuery, BaseModel):
    """Query parameters for movie endpoints."""

    id: str | None = Field(None, alias="_id", description="Filter by movie ID")
    genres: list[str] | None = Field(None, description="Filter by movie genres")
    runtime: int | None = Field(None, description="Filter by movie runtime")
    cast: list[str] | None = Field(None, description="Filter by movie cast")
    num_mflix_comments: int | None = Field(
        None, description="Filter by number of comments"
    )
    title: str | None = Field(None, description="Filter by movie title")
    countries: list[str] | None = Field(
        None, description="Filter by movie countries"
    )
    released: datetime | None = Field(
        None, description="Filter by movie release date"
    )
    directors: list[str] | None = Field(
        None, description="Filter by movie directors"
    )
    writers: list[str] | None = Field(None, description="Filter by movie writers")
    awards: dict | None = Field(None, description="Filter by movie awards")
    lastupdated: datetime | None = Field(
        None, description="Filter by last updated date"
    )
    year: int | None = Field(None, description="Filter by movie year")
    type: str | None = Field(None, description="Filter by movie type")
    search: str | None = Field(
        None, description="Search movies by text in title, plot, etc."
    )
    include_invalid_posters: bool | None = Field(
        False, description="Include movies with invalid posters"
    )
    sort_by: str | None = Field(
        None,
        description="Field to sort by (title, year, released, runtime, num_mflix_comments, lastupdated, imdb.rating, imdb.votes, tomatoes.viewer.rating, tomatoes.critic.rating)",
    )
    sort_order: str | None = Field(
        "asc", description="Sort order: 'asc' for ascending, 'desc' for descending"
    )
    limit: int | None = Field(10, description="Number of movies to return")
    skip: int | None = Field(0, description="Number of records to skip")

    @field_validator("sort_by")
    @classmethod
    def validate_sort_field(cls, v):
        if v is None:
            return v

        allowed_fields = [
            "title",
            "year",
            "released",
            "runtime",
            "num_mflix_comments",
            "lastupdated",
            "imdb.rating",
            "imdb.votes",
            "tomatoes.viewer.rating",
            "tomatoes.critic.rating",
        ]

        if v not in allowed_fields:
            raise ValueError(f"Sort field must be one of: {allowed_fields}")
        return v

    @field_validator("sort_order")
    @classmethod
    def validate_sort_order(cls, v):
        if v is None:
            return "asc"

        if v not in ["asc", "desc"]:
            raise ValueError("Sort order must be 'asc' or 'desc'")
        return v


class MovieResponse(BaseModel):
    """Response model for movie data."""

    id: str = Field(..., alias="_id")
    plot: str | None = None
    genres: list[str] | None = None
    runtime: int | None = None
    cast: list[str] | None = None
    num_mflix_comments: int | None = None
    poster: HttpUrl | None = None
    title: str
    fullplot: str | None = None
    countries: list[str] | None = None
    released: datetime | None = None
    directors: list[str] | None = None
    writers: list[str] | None = None
    awards: dict | None = None
    lastupdated: datetime | None = None
    year: int | None = None
    imdb: dict | None = None
    type: str | None = None
    tomatoes: dict | None = None
    valid_poster: bool | None = None

    @field_validator("year", mode="before")
    @classmethod
    def clean_year(cls, v):
        original_value = v
        if isinstance(v, str):
            logger.debug(
                f"Schemas.clean_year() converting string year: '{original_value}'"
            )
            digits = "".join(filter(str.isdigit, v))
            if digits:
                result = int(digits)
                logger.debug(
                    f"Schemas.clean_year() converted '{original_value}' to {result}"
                )
                return result
            else:
                logger.warning(
                    f"Schemas.clean_year() failed to extract digits from: '{original_value}'"
                )
        elif isinstance(v, int):
            if v < 1800 or v > 2100:
                logger.warning(f"Schemas.clean_year() suspicious year value: {v}")
        return original_value

    @classmethod
    def from_dict(cls, data: dict) -> "MovieResponse":
        """Create MovieResponse from dictionary."""
        logger.debug(
            f"Schemas.MovieResponse.from_dict() called with data keys: {list(data.keys())}"
        )

        original_id = data.get("_id")
        if "_id" in data:
            data["_id"] = str(data["_id"])
            logger.debug(
                f"Schemas.MovieResponse.from_dict() converted _id from {original_id} to {data['_id']}"
            )

        if "title" not in data:
            logger.warning(
                "Schemas.MovieResponse.from_dict() missing required field: title"
            )

        if "year" in data and isinstance(data["year"], str):
            logger.warning(
                f"Schemas.MovieResponse.from_dict() year is string instead of int: {data['year']}"
            )

        try:
            result = cls(**data)
            logger.debug(
                f"Schemas.MovieResponse.from_dict() successfully created MovieResponse for movie: {data.get('title', 'Unknown')}"
            )
            return result
        except Exception as e:
            logger.error(
                f"Schemas.MovieResponse.from_dict() failed to create MovieResponse: {e}"
            )
            raise
