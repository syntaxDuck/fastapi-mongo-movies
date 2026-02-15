"""Common validation utilities for service layer."""


from .logging import get_logger

logger = get_logger(__name__)

DEFAULT_LIMIT = 10
MAX_LIMIT = 1000


def validate_limit(limit: int | None, default: int = DEFAULT_LIMIT) -> int:
    """Validate and normalize limit parameter."""
    if limit is None:
        return default
    if limit < 0 or limit > MAX_LIMIT:
        logger.warning(f"Invalid limit {limit}, using default {default}")
        return default
    return limit


def validate_skip(skip: int | None, default: int = 0) -> int:
    """Validate and normalize skip parameter."""
    if skip is None:
        return default
    if skip < 0:
        logger.warning(f"Invalid skip {skip}, using default {default}")
        return default
    return skip


def validate_year(year: int | None) -> int | None:
    """Validate year parameter."""
    if year is None:
        return None
    if year < 1800 or year > 2100:
        logger.warning(f"Suspicious year parameter: {year}")
    return year


def validate_year_required(year: int) -> int:
    """Validate required year parameter."""
    if year < 1800 or year > 2100:
        logger.warning(f"Suspicious year parameter: {year}")
    return year


def validate_rating(rating: int) -> int:
    """Validate rating parameter."""
    if rating < 0 or rating > 10:
        logger.warning(f"Suspicious rating parameter: {rating}")
    return rating


def validate_modifier(mod: str, valid_mods: list[str] | None = None) -> str:
    """Validate query modifier parameter."""
    if valid_mods is None:
        valid_mods = ["eq", "ne", "gt", "gte", "lt", "lte"]
    if mod not in valid_mods:
        logger.warning(f"Invalid mod {mod}, using default 'eq'")
        return "eq"
    return mod


def validate_non_empty_string(value: str | None, param_name: str) -> str | None:
    """Validate non-empty string parameter."""
    if value is None:
        return None
    if not value or not value.strip():
        logger.warning(f"Empty {param_name} parameter")
        return None
    return value


def validate_pagination(
    limit: int | None = None,
    skip: int | None = None,
) -> tuple[int, int]:
    """Validate and normalize pagination parameters."""
    return validate_limit(limit), validate_skip(skip)
