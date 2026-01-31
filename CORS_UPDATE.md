# CORS Configuration Update

The FastAPI backend has been updated to allow CORS requests from the React frontend running on port 3000.

## Changes Made:

1. **Updated CORS Origins**: Added `http://localhost:3000` to the allowed origins list
2. **Updated Frontend URL**: Changed default frontend URL from port 8080 to 3000
3. **Updated Frontend Port**: Changed default frontend port from 8080 to 3000

## How to Apply Changes:

Restart your FastAPI backend for the changes to take effect:

```bash
# Stop any running backend process
# Then restart
uv run python main.py
# or
uv run uvicorn app.main:app --reload --port 8000
```

## Alternative: Environment Variable Override

If you prefer to keep the original configuration and use environment variables, create a `.env` file in the project root:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:8000
FRONTEND_URL=http://localhost:3000
FRONTEND_PORT=3000
```

## Testing

After restarting the backend:
1. Start your React frontend: `cd frontend_react && npm start`
2. Navigate to `http://localhost:3000`
3. The CORS errors should be resolved

The backend will now properly handle requests from the React frontend.