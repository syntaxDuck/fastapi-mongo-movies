# FastAPI MongoDB Movies - Restructured

A refactored FastAPI application with MongoDB for movie data management, featuring clean architecture with proper separation of concerns.

## 🏗️ Architecture

The application has been restructured to follow clean architecture principles:

```
app/
├── api/                    # API layer
│   ├── main.py            # FastAPI app factory and configuration
│   └── routes/           # API route handlers
│       ├── movies.py      # Movie endpoints
│       ├── users.py       # User endpoints
│       └── comments.py    # Comment endpoints
├── core/                   # Core functionality
│   ├── config.py          # Application settings
│   ├── database.py        # Database connection and operations
│   └── exceptions.py      # Custom exceptions
├── models/                 # Database entity models
│   └── movie.py          # Movie, User, Comment models
├── repositories/           # Data access layer
│   ├── base.py           # Base repository
│   └── movie_repository.py # Movie, User, Comment repositories
├── schemas/                # API request/response models
│   └── movie.py          # Pydantic schemas for API
├── services/               # Business logic layer
│   └── movie_service.py  # Movie, User, Comment services
└── main.py                 # Application entry point
```

## 🚀 Key Improvements

### Before
- **Monolithic structure**: All code mixed in `api/`, `backend/`, `config/`
- **Circular dependencies**: Frontend imported directly from API models
- **Mixed responsibilities**: Database logic mixed with API handlers
- **No separation of concerns**: Business logic scattered across controllers

### After
- **Clean separation of concerns**: Each layer has single responsibility
- **Dependency injection**: Proper DI with FastAPI's dependency system
- **Repository pattern**: Abstract data access layer
- **Service layer**: Centralized business logic
- **Type safety**: Separate models (database) from schemas (API)
- **Testable architecture**: Each layer can be tested independently

## 🎯 Layer Responsibilities

### API Layer (`app/api/`)
- HTTP request/response handling
- Input validation with Pydantic schemas
- Error handling and HTTP status codes
- API documentation with OpenAPI

### Service Layer (`app/services/`)
- Business logic and validation
- Coordination between repositories
- Complex operations and workflows
- Error handling with custom exceptions

### Repository Layer (`app/repositories/`)
- Data access abstraction
- MongoDB operations
- Query optimization
- Database-specific logic

### Core Layer (`app/core/`)
- Configuration management
- Database connection handling
- Custom exceptions
- Shared utilities

### Models (`app/models/`)
- Database entity definitions
- Data transformation helpers
- Internal data representation

### Schemas (`app/schemas/`)
- API request/response models
- Input validation rules
- Serialization/deserialization
- API documentation

## 🔧 Running the Application

### Development Mode
```bash
# Start all services together
uv run python main.py

# Or start individual services
uv run uvicorn app.main:app --reload --port 8000  # API
uv run uvicorn frontend.main:app --reload --port 8080  # Frontend
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test files
uv run pytest tests/test_basic_coverage.py
uv run pytest tests/test_services.py
```

## 📊 API Endpoints

### Movies
- `GET /movies/` - List movies with filtering and pagination
- `GET /movies/{movie_id}` - Get specific movie
- `GET /movies/type/{type}` - Get movies by type
- `GET /movies/year/{year}` - Get movies by year
- `GET /movies/genre/{genre}` - Get movies by genre

### Users
- `GET /users/` - List users with filtering
- `GET /users/{user_id}` - Get specific user
- `POST /users/` - Create new user
- `GET /users/email/{email}` - Get users by email
- `GET /users/name/{name}` - Get users by name

### Comments
- `GET /comments/` - List comments with filtering
- `GET /comments/{comment_id}` - Get specific comment
- `GET /comments/movie/{movie_id}` - Get comments by movie
- `GET /comments/email/{email}` - Get comments by email
- `GET /comments/name/{name}` - Get comments by name

## 🔗 Dependency Flow

```
API Routes → Services → Repositories → Database
     ↓           ↓            ↓
  Schemas → Models → Core Config
```

This unidirectional flow eliminates circular dependencies and creates a clear separation of concerns.

## 🎨 Benefits of New Architecture

1. **Maintainability**: Each layer has a single, well-defined responsibility
2. **Testability**: Components can be tested in isolation with proper mocking
3. **Scalability**: Easy to add new features or modify existing ones
4. **Reusability**: Services and repositories can be reused across different API endpoints
5. **Type Safety**: Clear separation between internal models and API contracts
6. **Error Handling**: Centralized exception handling with proper HTTP status codes
7. **Performance**: Optimized database queries and efficient data flow

## 📝 Migration Notes

- **Old API endpoints**: Still functional but deprecated
- **Frontend compatibility**: Updated to work with new API structure
- **Database**: No changes required - uses same MongoDB collections
- **Configuration**: Enhanced with more environment variables

## 🛠️ Development Guidelines

1. **Always use dependency injection** for services and repositories
2. **Keep business logic in services**, not in API routes
3. **Use repositories for all database operations**
4. **Validate input at the API layer** with Pydantic schemas
5. **Handle errors with custom exceptions** and proper HTTP status codes
6. **Write tests for each layer** independently

This restructured architecture provides a solid foundation for future development and maintenance.