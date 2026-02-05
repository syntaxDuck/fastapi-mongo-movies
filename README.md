# FastAPI Mongo Movies

A FastAPI application with MongoDB for movie data management, featuring a clean architecture with separate API and frontend components.

## Features

- **Movie Catalog**: Browse and search movies from MongoDB sample_mflix database
- **User Management**: Create and manage user accounts
- **Comments System**: View and manage movie comments
- **Genre Browsing**: Explore movies by genre with interactive cards
- **Search Functionality**: Full-text search across movie titles and descriptions
- **Responsive Design**: Mobile-first design with desktop optimizations
- **Clean Architecture**: Layered service-repository pattern with dependency injection
- **React Frontend**: Modern web interface using React with TypeScript
- **Async Operations**: Full async/await support for database operations

## Architecture

```
fastapi-mongo-movies/
├── app/                          # Backend clean architecture
│   ├── api/                       # FastAPI REST API endpoints
│   │   └── routes/               # Route definitions
│   ├── services/                   # Business logic layer
│   ├── repositories/               # Data access abstraction
│   │   └── protocol.py          # Repository interfaces
│   ├── schemas/                   # API request/response models
│   ├── core/                      # Configuration, database, exceptions
│   └── main.py                   # Backend application entry point
├── frontend/                      # React frontend application
│   ├── public/                    # Static assets
│   ├── src/                      # Source code
│   │   ├── components/           # React components
│   │   │   ├── genres/          # Genre-related components
│   │   │   ├── movies/          # Movie-related components
│   │   │   ├── util/            # Utility components
│   │   │   └── views/           # Page view components
│   │   ├── services/             # API service layer
│   │   ├── styles/               # CSS modules and styling
│   │   ├── types.ts              # TypeScript type definitions
│   │   └── App.tsx              # Main application component
│   ├── build/                    # Production build output
│   └── package.json              # Frontend dependencies
├── tests/                        # Test suites
│   ├── backend/                  # Backend tests
│   ├── frontend/                 # Frontend tests
│   └── fixtures/                # Test data fixtures
├── scripts/                      # Utility scripts
├── logs/                         # Application logs
└── main.py                      # Service launcher
```

## Tech Stack

### Backend
- **API Framework**: FastAPI with Python 3.12+
- **Database**: MongoDB with Motor (async driver)
- **Validation**: Pydantic with email support
- **Environment**: Python-dotenv for configuration
- **Server**: Uvicorn with hot reload

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: CSS Modules with custom design system
- **Routing**: React Router DOM
- **Build Tool**: Create React App
- **State Management**: React hooks and context
- **HTTP Client**: Fetch API with custom service layer

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

2. Install backend dependencies using uv:
```bash
uv sync
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
cd ..
```

4. Install test dependencies (optional):
```bash
uv sync --group test
```

## Configuration

Create a `.env` file in the root directory with your MongoDB configuration:

```env
DB_USER=your_mongodb_username
DB_PASS=your_mongodb_password
DB_HOST=your_mongodb_host
```

## Running the Application

### Option 1: Run both services together (Recommended)
```bash
# Terminal 1 - Start backend
uv run python main.py

# Terminal 2 - Start frontend  
cd frontend && npm start
```

### Option 2: Run services individually

**Backend API Service:**
```bash
uv run uvicorn app.main:app --reload --port 8000
```

**Frontend Development Server:**
```bash
cd frontend
npm start
```

**Production Build:**
```bash
cd frontend
npm run build
```

### Access Points
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend Application**: http://localhost:3000
- **Frontend Production Build**: Serve `frontend/build/` directory

## API Endpoints

### Movies
- `GET /movies/` - List movies with filtering, search, and pagination
- `GET /movies/{movie_id}` - Get specific movie by ID
- `GET /movies/type/{movie_type}` - Get movies by type
- `GET /movies/year/{year}` - Get movies by release year
- `GET /movies/genres` - Get all available movie genres
- `GET /movies/genres/{genre}` - Get movies by genre
- `GET /movies/types` - Get all available movie types
- Query parameters: `_id`, `title`, `search`, `type`, `limit`, `skip`, `include_invalid_posters`

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

**Backend Dependencies:**
```bash
uv add <package-name>
```

**Frontend Dependencies:**
```bash
cd frontend
npm install <package-name>
```

### Frontend Development

The React frontend uses a component-based architecture with:
- **Feature-based organization**: Components grouped by functionality
- **CSS Modules**: Scoped styling with design system variables
- **TypeScript**: Full type safety throughout the application
- **Responsive Design**: Mobile-first approach with desktop enhancements

**Component Structure:**
- `genres/`: Genre browsing and selection components
- `movies/`: Movie display, lists, and details components  
- `util/`: Reusable utility components
- `views/`: Page-level view components

**Styling:**
- Design system with CSS custom properties
- Component-scoped CSS modules
- Responsive breakpoints and utilities
- Dark theme with accessibility focus

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

**Backend Tests:**
```bash
# Run all backend tests
uv run pytest

# Run tests by category
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m api

# Run with coverage
uv run pytest --cov=app --cov-report=html
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

**Combined Tests:**
```bash
# Run both backend and frontend tests
uv run pytest && cd frontend && npm test
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

1. **MongoDB Connection**: Ensure your MongoDB credentials are correct in `.env` file
2. **Port Conflicts**: Make sure ports 8000 (API) and 3000 (frontend) are available
3. **Dependencies**: 
   - Backend: Run `uv sync` if you encounter missing package errors
   - Frontend: Run `npm install` in frontend directory
4. **TypeScript Errors**: Check `frontend/src/types.ts` for proper type definitions
5. **Build Failures**: Clear `node_modules` and `npm install` again

### Getting Help

- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **Frontend Dev Tools**: Use React Developer Tools for component inspection
- **Network Issues**: Check browser console for API connection errors
- **Database Issues**: Verify MongoDB connection strings and permissions

### Development Tips

- The backend runs on port 8000, frontend on port 3000
- CORS is configured to allow frontend-backend communication
- Use browser dev tools to inspect API requests and responses
- Check logs in `logs/` directory for backend debugging
- React hot reload provides instant frontend updates during development

