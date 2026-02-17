import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from backend.main import app
from backend.schemas import UserResponse

client = TestClient(app)

@pytest.fixture
def admin_headers():
    return {"X-Admin-API-Key": "12345678901234567890123456789012"}

def test_get_users_unauthorized():
    response = client.get("/users/")
    # verify_admin_api_key returns 404 for missing/invalid keys
    assert response.status_code == 404

def test_get_users_authorized():
    with patch("backend.api.routes.users._get_user_service") as mock_get_service:
        mock_service = AsyncMock()
        mock_service.get_users.return_value = [
            UserResponse(_id="507f1f77bcf86cd799439011", name="Test User", email="test@example.com")
        ]
        mock_get_service.return_value = mock_service

        headers = {"X-Admin-API-Key": "12345678901234567890123456789012"}
        response = client.get("/users/", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Test User"

def test_get_user_by_id_unauthorized():
    response = client.get("/users/507f1f77bcf86cd799439011")
    assert response.status_code == 404

def test_get_user_by_id_authorized():
    with patch("backend.api.routes.users._get_user_service") as mock_get_service:
        mock_service = AsyncMock()
        mock_service.get_user_by_id.return_value = UserResponse(
            _id="507f1f77bcf86cd799439011", name="Test User", email="test@example.com"
        )
        mock_get_service.return_value = mock_service

        headers = {"X-Admin-API-Key": "12345678901234567890123456789012"}
        response = client.get("/users/507f1f77bcf86cd799439011", headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Test User"

def test_create_user_still_public():
    """Verify that creating a user is still public (no API key required)."""
    with patch("backend.api.routes.users._get_user_service") as mock_get_service:
        mock_service = AsyncMock()
        mock_service.create_user.return_value = {"message": "User created successfully"}
        mock_get_service.return_value = mock_service

        user_data = {
            "name": "New User",
            "email": "new@example.com",
            "password": "securepassword123"
        }
        response = client.post("/users/", json=user_data)
        # Should be 200 (or whatever create_user returns), NOT 404
        assert response.status_code == 200
