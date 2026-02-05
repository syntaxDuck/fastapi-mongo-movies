# FastAPI Mongo Movies

A FastAPI application with MongoDB for movie data management, featuring a multi-service architecture with separate API, frontend, and backend components.

## Features

- **Movie Catalog**: Browse and search movies from MongoDB sample_mflix database
- **User Management**: Create and manage user accounts
- **Comments System**: View and manage movie comments
- **Multi-Service Architecture**: Separate API, frontend, and backend services
- **FastHTML Frontend**: Modern web interface using Python-FastHTML
- **Async Operations**: Full async/await support for database operations

## Architecture

```
fastapi-mongo-movies/
├── app/                 # Restructured clean architecture
│   ├── api/            # FastAPI REST API endpoints
│   ├── services/        # Business logic layer
│   ├── repositories/    # Data access abstraction
│   ├── models/          # Database entities
│   ├── schemas/         # API request/response models
│   ├── core/           # Configuration & database
│   └── main.py         # Application entry point
├── frontend/           # FastHTML web interface
├── legacy/             # Original code structure (archived)
└── main.py            # Service launcher
```

## Tech Stack

- **Backend**: FastAPI, Python 3.12+
- **Database**: MongoDB with Motor (async driver)
- **Frontend**: Python-FastHTML
- **Validation**: Pydantic with email support
- **Environment**: Python-dotenv for configuration
- **Server**: Uvicorn

## Prerequisites

- Python 3.12 or higher
- MongoDB database (uses sample_mflix dataset)
- uv package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-mongo-movies
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Install backend dependencies:
```bash
cd backend
uv sync
cd ..
```

## Configuration

Create a `.env` file in the root directory with your MongoDB configuration:

```env
DB_USER=your_mongodb_username
DB_PASS=your_mongodb_password
DB_HOST=your_mongodb_host
```

## Running the Application

### Option 1: Run all services together (Recommended)
```bash
uv run python main.py
```

This will start:
- API service on port 8000 (new clean architecture)
- Frontend service on port 8080

### Option 2: Run services individually

**New API Service (Restructured):**
```bash
uv run uvicorn app.main:app --reload --port 8000
```

**Legacy API Service (Deprecated):**
```bash
uv run uvicorn legacy.api.main:app --reload --port 8000
```

**Frontend Service:**
```bash
uv run uvicorn frontend.main:app --reload --port 8080
```

## API Endpoints

### Movies (New Architecture)
- `GET /movies/` - List movies with filtering and pagination
- `GET /movies/{movie_id}` - Get specific movie by ID
- `GET /movies/type/{type}` - Get movies by type
- `GET /movies/year/{year}` - Get movies by year
- `GET /movies/genre/{genre}` - Get movies by genre
- Query parameters: `id`, `title`, `type`, `limit`, `skip`

### Users
- `GET /users/` - List users with filtering
- `POST /users/` - Create new user
- `GET /users/{user_id}` - Get specific user by ID
- `GET /users/email/{email}` - Get users by email
- `GET /users/name/{name}` - Get users by name
- Query parameters: `_id`, `name`, `email`, `limit`, `skip`

### Comments
- `GET /comments/` - List comments with filtering
- `GET /comments/{comment_id}` - Get specific comment by ID
- `GET /comments/movie/{movie_id}` - Get comments by movie
- `GET /comments/email/{email}` - Get comments by email
- `GET /comments/name/{name}` - Get comments by name
- Query parameters: `movie_id`, `limit`, `skip`

### Legacy API (Deprecated)
- `GET /movies` - Old endpoint (still functional)

### Users
- `GET /users` - List users with filtering
- `POST /users/` - Create a new user
- Query parameters: `_id`, `name`, `email`, `limit`, `skip`

### Comments
- `GET /comments` - List comments with filtering
- Query parameters: `movie_id`, `limit`, `skip`

## Data Models

### Movie
```python
- id: str
- title: str
- plot: str
- genres: list[str]
- cast: list[str]
- directors: list[str]
- year: int
- runtime: int
- countries: list[str]
- released: datetime
- imdb: dict
- tomatoes: dict
- awards: dict
```

### User
```python
- id: str
- name: str
- email: EmailStr
- password: str
```

### Comment
```python
- id: str
- name: str
- email: str
- movie_id: str
- text: str
- date: datetime
```

## Development

### Adding Dependencies

To add a new dependency:
```bash
uv add <package-name>
```

### Logging

The application includes comprehensive logging:

#### Environment Variables
```bash
# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
export LOG_LEVEL=INFO

# Enable/disable console logging
export LOG_TO_CONSOLE=true

# Enable/disable file logging  
export LOG_TO_FILE=true

# Log format (simple, detailed)
export LOG_FORMAT=detailed
```

#### Log Files
- `logs/app.log` - All application logs
- `logs/errors.log` - Error and critical logs only

#### Log Levels by Component
- **app.core.database**: DEBUG (query details)
- **app.repositories**: INFO
- **app.services**: INFO  
- **app.api**: INFO
- **uvicorn.access**: WARNING

#### Testing Logging
```bash
# Test logging configuration
uv run python test_logging.py
```

### Running Tests

If you have tests configured:
```bash
uv run pytest
```

## Database Schema

The application uses the MongoDB sample_mflix dataset with the following collections:

- **movies**: Movie information and metadata
- **users**: User accounts and profiles
- **comments**: User comments on movies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **MongoDB Connection**: Ensure your MongoDB credentials are correct in the `.env` file
2. **Port Conflicts**: Make sure ports 8000 and 8080 are available
3. **Dependencies**: Run `uv sync` if you encounter missing package errors

### Getting Help

- Check the API documentation at `http://localhost:8000/docs`
- Verify MongoDB connection and credentials
- Ensure all dependencies are installed with `uv sync`

