import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from backend.main import app
from backend.core.config import settings

client = TestClient(app)

@pytest.fixture
def admin_headers():
    return {"X-Admin-API-Key": settings.ADMIN_API_KEY}

class TestUserSecurity:
    """Test cases for user-related security."""

    @pytest.mark.asyncio
    async def test_get_users_unauthorized(self):
        """Verify that GET /users/ returns 404 without API key."""
        response = client.get("/users/")
        # Security through obscurity: returns 404 for unauthorized access
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_users_invalid_key(self):
        """Verify that GET /users/ returns 404 with invalid API key."""
        response = client.get("/users/", headers={"X-Admin-API-Key": "wrong-key"})
        assert response.status_code == 404

    @patch("backend.api.routes.users._get_user_service")
    def test_get_users_authorized(self, mock_get_service, admin_headers):
        """Verify that GET /users/ returns 200 with valid API key."""
        mock_service = AsyncMock()
        mock_service.get_users.return_value = []
        mock_get_service.return_value = mock_service

        response = client.get("/users/", headers=admin_headers)
        assert response.status_code == 200

    def test_create_user_public(self):
        """Verify that POST /users/ is public (but will fail validation for bad data)."""
        # Sending empty data to trigger validation, but not 404/401
        response = client.post("/users/", json={})
        # 422 Unprocessable Entity (validation error) is expected for empty body,
        # but 404 would mean it's protected by verify_admin_api_key.
        assert response.status_code == 422

    @patch("backend.api.routes.users._get_user_service")
    def test_create_user_password_validation(self, mock_get_service):
        """Verify new password requirements are enforced."""
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        # Test password too short (< 8)
        response = client.post("/users/", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "short"
        })
        # Should be 422 because of Pydantic min_length=8
        assert response.status_code == 422

        # Test common password (should be caught by UserService)
        from backend.core.exceptions import ValidationError
        mock_service.create_user.side_effect = ValidationError("Password is too common", field="password")

        response = client.post("/users/", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123" # This one is 11 chars so passes Pydantic but we'll mock it failing UserService
        })
        assert response.status_code == 422
        assert "Password is too common" in response.json()["detail"]
