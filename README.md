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
├── api/                 # FastAPI REST API endpoints
├── backend/            # Database connection and business logic
├── frontend/           # FastHTML web interface
├── config/             # Configuration management
└── main.py            # Application entry point
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

### Option 1: Run all services together
```bash
uv run python main.py
```

This will start:
- API service on port 8000
- Frontend service on port 8080

### Option 2: Run services individually

**API Service:**
```bash
uv run uvicorn api.main:app --reload --port 8000
```

**Frontend Service:**
```bash
uv run uvicorn frontend.main:app --reload --port 8080
```

## API Endpoints

### Movies
- `GET /movies` - List movies with filtering and pagination
- Query parameters: `id`, `title`, `type`, `limit`, `skip`

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

For backend-specific dependencies:
```bash
cd backend
uv add <package-name>
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

