from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from backend.api.main import create_app
from backend.services.poster_validation_service import ValidationStats


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_admin_stats_unauthorized_no_key(client, mocker):
    """Test accessing admin endpoint without API key."""
    mocker.patch("backend.core.config.settings.ADMIN_API_KEY", "test-key")
    response = client.get("/admin/movies/validate-posters/statistics")
    # Intentional 404 for security through obscurity
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_admin_stats_unauthorized_wrong_key(client, mocker):
    """Test accessing admin endpoint with wrong API key."""
    mocker.patch("backend.core.config.settings.ADMIN_API_KEY", "test-key")
    response = client.get(
        "/admin/movies/validate-posters/statistics",
        headers={"X-Admin-API-Key": "wrong-key"},
    )
    # Intentional 404 for security through obscurity
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_admin_stats_locked(client, mocker):
    """Test accessing admin endpoint when API is locked."""
    mocker.patch("backend.core.config.settings.ADMIN_API_KEY", "")
    response = client.get(
        "/admin/movies/validate-posters/statistics",
        headers={"X-Admin-API-Key": "any-key"},
    )
    # Intentional 404 for security through obscurity
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


@pytest.mark.asyncio
async def test_admin_stats_authorized(client, mocker):
    """Test accessing admin endpoint with correct API key."""
    mocker.patch("backend.core.config.settings.ADMIN_API_KEY", "test-key")
    # Mock the service to avoid actual DB/HTTP calls
    mock_stats = ValidationStats(
        total_movies=100,
        movies_with_posters=80,
        valid_posters=70,
        invalid_posters=10,
        validation_success_rate=87.5,
        last_validation_date=datetime.utcnow(),
    )

    mocker.patch(
        "backend.services.poster_validation_service.PosterValidationService.get_validation_statistics",
        return_value=mock_stats,
    )

    response = client.get(
        "/admin/movies/validate-posters/statistics",
        headers={"X-Admin-API-Key": "test-key"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_movies"] == 100
    assert data["validation_success_rate"] == 87.5


def test_users_list_unauthorized(client, mocker):
    """Test accessing users list without API key."""
    mocker.patch("backend.core.config.settings.ADMIN_API_KEY", "test-key-32-chars-long-security-key")
    response = client.get("/users")
    assert response.status_code == 404
