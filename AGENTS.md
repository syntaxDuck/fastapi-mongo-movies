# AGENTS.md - Development Guide for FastAPI MongoDB Movies

This file contains development guidelines, commands, and conventions for agentic coding agents working in this repository.

## Project Overview

FastAPI MongoDB Movies is a clean architecture application with:
- **Backend**: FastAPI with MongoDB (Motor async driver)
- **Frontend**: Python-FastHTML
- **Database**: MongoDB with sample_mflix dataset
- **Architecture**: Layered service-repository pattern with dependency injection

## Development Commands

### Environment Setup
```bash
# Install all dependencies
uv sync

# Install test dependencies
uv sync --group test
```

### Running the Application
```bash
# Run all services together (recommended)
uv run python main.py

# Run API service only
uv run uvicorn app.main:app --reload --port 8000

# Run frontend service only
uv run uvicorn frontend.main:app --reload --port 8080
```

### Testing Commands
```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_services.py

# Run tests by marker
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m api
uv run pytest -m backend
uv run pytest -m frontend

# Run single test
uv run pytest tests/test_services.py::TestMovieService::test_get_movie_by_id_success

# Run tests with coverage for specific modules
uv run pytest --cov=app --cov=frontend

# Quick test without coverage
uv run pytest -x -v

# Generate coverage report
uv run pytest --cov=app --cov=frontend --cov-report=html
```

### Linting and Type Checking
```bash
# Note: No ruff configuration found - add to pyproject.toml if needed
# Use standard Python type checking
uv run python -m py_compile app/**/*.py
uv run python -m py_compile frontend/**/*.py
```

## Code Style Guidelines

### Emoji Usage Policy
- **STRICTLY PROHIBITED**: No emojis in Python source code, logging statements, or test files
- **Logging**: Use text-based prefixes like "SUCCESS:", "ERROR:", "TEST:", "STATS:"
- **Documentation**: Emojis may be used sparingly for visual clarity (max 1-2 per section)
- **Frontend**: Emojis may be used sparingly in UI components (prefer text labels or proper icon libraries)
- **CSS**: Avoid emoji in content properties; use text or remove decorative elements
- **Priority**: Function over decoration - ensure code remains professional and accessible

### Import Organization
```python
# Standard library imports first
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

# Third-party imports next
from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient

# Local imports last (use relative imports within the app)
from .core.exceptions import NotFoundError
from ..services.movie_service import MovieService
from ...repositories.movie_repository import MovieRepository
```

### Type Hints
- **Always** use type hints for function signatures and class attributes
- Use `Optional[T]` for nullable types
- Use `Dict[str, Any]` for flexible MongoDB documents
- Use `List[T]` for collections
- Use `async def` for async functions

```python
async def get_movie_by_id(
    self, 
    movie_id: str, 
    limit: int = 10, 
    skip: int = 0
) -> List[Dict[str, Any]]:
    """Get movies with optional filtering."""
```

### Naming Conventions
- **Classes**: PascalCase (e.g., `MovieService`, `DatabaseConfig`)
- **Functions/Methods**: snake_case (e.g., `get_movie_by_id`, `create_user`)
- **Variables**: snake_case (e.g., `movie_repository`, `sample_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DB_HOST`, `MAX_LIMIT`)
- **Private methods**: prefix with underscore (e.g., `_validate_input`)

### Error Handling
```python
# Custom exceptions from app.core.exceptions
from ..core.exceptions import NotFoundError, DatabaseError, DuplicateResourceError

# Raise appropriate exceptions in services
if not movie:
    raise NotFoundError(f"Movie with ID {movie_id} not found")

# Handle exceptions in API routes
try:
    result = await service.get_movie(movie_id)
except NotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
except Exception as e:
    raise HTTPException(status_code=500, detail="Internal server error")
```

### Dependency Injection Pattern
```python
# Service dependencies
async def get_movie_service() -> MovieService:
    """Dependency to get movie service instance."""
    database = create_database_handler()
    repository = MovieRepository(database)
    return MovieService(repository)

# Route dependencies
@router.get("/movies/{movie_id}")
async def get_movie(
    movie_id: str,
    movie_service: MovieService = Depends(get_movie_service),
):
    return await movie_service.get_movie_by_id(movie_id)
```

## Architecture Patterns

### Clean Architecture Layers
1. **API Layer** (`app/api/`): FastAPI routes and HTTP handling
2. **Service Layer** (`app/services/`): Business logic and orchestration
3. **Repository Layer** (`app/repositories/`): Data access abstraction
4. **Core Layer** (`app/core/`): Database, configuration, exceptions, logging

### Repository Pattern
```python
class MovieRepository:
    """Data access layer for movies."""
    
    def __init__(self, database: DatabaseHandler) -> None:
        self.database = database
    
    async def find_by_id(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """Find movie by ID."""
        return await self.database.fetch_documents(
            "movies", {"_id": movie_id}, limit=1
        )
```

### Service Pattern
```python
class MovieService:
    """Business logic layer for movies."""
    
    def __init__(self, movie_repository: MovieRepository) -> None:
        self.movie_repository = movie_repository
    
    async def get_movie_by_id(self, movie_id: str) -> Dict[str, Any]:
        """Get movie by ID with validation."""
        movie = await self.movie_repository.find_by_id(movie_id)
        if not movie:
            raise NotFoundError(f"Movie with ID {movie_id} not found")
        return movie
```

## Testing Guidelines

### Test Structure
```python
class TestMovieService:
    """Test cases for MovieService."""
    
    @pytest.mark.asyncio
    async def test_get_movie_by_id_success(self, movie_service, sample_movie_data):
        """Test getting a movie by ID successfully."""
        # Setup
        movie_service.movie_repository.find_by_id = AsyncMock(
            return_value=sample_movie_data
        )
        
        # Execute
        result = await movie_service.get_movie_by_id("test_id")
        
        # Assert
        assert result == sample_movie_data
        movie_service.movie_repository.find_by_id.assert_called_once_with("test_id")
```

### Test Fixtures
- Use fixtures from `tests/conftest.py` and `tests/fixtures/`
- Mark async tests with `@pytest.mark.asyncio`
- Use `AsyncMock` for async dependencies
- Test both success and error cases

### Test Markers
- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.api`: API endpoint tests
- `@pytest.mark.backend`: Backend service tests
- `@pytest.mark.frontend`: Frontend component tests

## Database Patterns

### MongoDB Document Structure
```python
# Movie documents follow MongoDB sample_mflix schema
{
    "_id": "503f19d3767d81a2a1200003",
    "title": "Movie Title",
    "plot": "Movie plot...",
    "genres": ["Action", "Drama"],
    "cast": ["Actor 1", "Actor 2"],
    "directors": ["Director 1"],
    "year": 2023,
    "type": "movie",
    "imdb": {"rating": 7.5, "votes": 1000, "id": 12345},
    "tomatoes": {"viewer": {"rating": 4.0, "numReviews": 50}}
}
```

### Database Configuration
- Use environment variables for connection (DB_USER, DB_PASS, DB_HOST)
- Configure logging via LOG_LEVEL, LOG_TO_CONSOLE, LOG_TO_FILE
- Use Motor for async MongoDB operations
- Implement proper connection management with context managers

## Logging Guidelines

### Logger Usage
```python
from ..core.logging import get_logger

logger = get_logger(__name__)

async def some_function():
    logger.info("Starting operation")
    try:
        result = await operation()
        logger.info(f"Operation completed successfully: {result}")
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise
```

### Log Levels by Component
- **app.core.database**: DEBUG (query details)
- **app.repositories**: INFO
- **app.services**: INFO
- **app.api**: INFO
- **uvicorn.access**: WARNING

## Frontend Patterns (FastHTML)

### Component Structure
```python
def MovieComponent(movie_data):
    """Reusable movie component."""
    return Div(
        H3(movie_data["title"]),
        P(movie_data["plot"]),
        cls="movie-card"
    )
```

### Route Handlers
```python
@rt
def movie_details(movie_id: str):
    """Movie details page."""
    movie = fetch_movie(movie_id)
    return MovieDetails(movie)
```

## Important Notes

1. **Always use async/await** for database operations
2. **Validate inputs** in service layer before repository calls
3. **Use proper exception handling** with custom exceptions
4. **Write tests** for all service methods (success and error cases)
5. **Use relative imports** within the app package
6. **Follow the existing patterns** in the codebase
7. **Document public methods** with docstrings
8. **Use type hints** consistently throughout the codebase

## Environment Variables

Required in `.env` file:
```
DB_USER=your_mongodb_username
DB_PASS=your_mongodb_password  
DB_HOST=your_mongodb_host
MONGODB_TLS=true
```

Optional:
```
LOG_LEVEL=INFO
LOG_TO_CONSOLE=true
LOG_TO_FILE=true
LOG_FORMAT=detailed
```