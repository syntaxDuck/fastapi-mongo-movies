from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from backend.api.main import create_app
from backend.core.config import settings


@pytest.fixture
def client():
    # Mock DatabaseManager.get_client to avoid real connection attempts during lifespan
    with patch("backend.core.database.DatabaseManager.get_client", new_callable=AsyncMock):
        app = create_app()
        with TestClient(app) as c:
            yield c

def test_registration_weak_password_service_level(client):
    """Test that registration with a password of length 7 fails (passes Pydantic but fails Service)."""
    # We need to ensure _get_user_service returns a service that uses our mock repository
    with patch("backend.api.routes.users._get_user_service") as mock_get_service:
        from backend.services.user_service import UserService
        mock_repo = MagicMock()
        real_service = UserService(mock_repo)
        mock_get_service.return_value = real_service

        response = client.post(
            "/users/",
            json={
                "name": "Weak User",
                "email": "weak@example.com",
                "password": "abcdefg" # Length 7
            }
        )
        assert response.status_code == 422
        assert "at least 8 characters" in response.json()["detail"]

def test_registration_common_password(client):
    """Test that registration with a common password fails."""
    with patch("backend.api.routes.users._get_user_service") as mock_get_service:
        from backend.services.user_service import UserService
        mock_repo = MagicMock()
        real_service = UserService(mock_repo)
        mock_get_service.return_value = real_service

        response = client.post(
            "/users/",
            json={
                "name": "Common User",
                "email": "common@example.com",
                "password": "password"
            }
        )
        assert response.status_code == 422
        assert "too common and insecure" in response.json()["detail"]

def test_get_users_unauthorized(client):
    """Test that listing users without admin key returns 404."""
    response = client.get("/users/")
    assert response.status_code == 404

def test_get_users_authorized(client):
    """Test that listing users with valid admin key passes auth and functions correctly."""
    with patch("backend.api.routes.users._get_user_service") as mock_get_service:
        mock_service = MagicMock()
        # Mocking the async method to return a dummy user to ensure 200 OK
        mock_service.get_users = AsyncMock(
            return_value=[
                {
                    "_id": "507f1f77bcf86cd799439011",
                    "name": "Test User",
                    "email": "test@example.com",
                }
            ]
        )
        mock_get_service.return_value = mock_service

        response = client.get(
            "/users/", headers={"X-Admin-API-Key": settings.ADMIN_API_KEY}
        )
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Test User"
