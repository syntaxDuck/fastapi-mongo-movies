# React Frontend for FastAPI Movies

This is the React frontend for the FastAPI MongoDB Movies application.

## Features

- Browse movies with pagination
- View detailed movie information
- Filter movies by genre, director, year, and rating
- Responsive design with dark theme
- Clean component architecture

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend_react directory:
   ```bash
   cd frontend_react
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The app will be available at `http://localhost:3000`

### Configuration

The React app is configured to proxy API requests to the FastAPI backend running on `http://localhost:8000`. 

You can override this by setting the `REACT_APP_API_URL` environment variable:

```bash
REACT_APP_API_URL=http://your-api-url:8000 npm start
```

## Project Structure

```
src/
├── components/          # React components
│   ├── MovieList.tsx   # Movie list component
│   ├── MovieDetails.tsx # Movie details component
│   ├── NavBar.tsx      # Navigation bar
│   └── Rating.tsx      # Rating display components
├── services/           # API services
│   └── api.ts         # API client functions
├── types.ts           # TypeScript type definitions
├── App.tsx            # Main app component with routing
└── index.tsx          # App entry point
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm run build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm run eject` - Ejects from Create React App (one-way operation)

## Styling

The app uses CSS modules with a dark theme that matches the original FastHTML design. All styles are located alongside their components.

## API Integration

The frontend communicates with the FastAPI backend through the services in `src/services/api.ts`. The API client handles:

- Fetching movies with pagination and filtering
- Retrieving individual movie details
- Error handling and loading states

## Development

The React app was created to replace the FastHTML frontend while maintaining the same visual design and functionality. It provides a more modern development experience with:

- TypeScript for type safety
- Component-based architecture
- React Router for navigation
- Modern React patterns with hooks
- Better maintainability and scalability