import pytest
from fastapi.testclient import TestClient
from backend.api.main import create_app
from backend.core.config import settings
from backend.services.poster_validation_service import ValidationStats
from datetime import datetime


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_admin_stats_unauthorized_no_key(client, mocker):
    """Test accessing admin endpoint without API key."""
    mocker.patch("backend.core.config.settings.ADMIN_API_KEY", "test-key")
    response = client.get("/admin/movies/validate-posters/statistics")
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin API Key is missing"


def test_admin_stats_unauthorized_wrong_key(client, mocker):
    """Test accessing admin endpoint with wrong API key."""
    mocker.patch("backend.core.config.settings.ADMIN_API_KEY", "test-key")
    response = client.get(
        "/admin/movies/validate-posters/statistics",
        headers={"X-Admin-API-Key": "wrong-key"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Admin API Key"


def test_admin_stats_locked(client, mocker):
    """Test accessing admin endpoint when API is locked."""
    mocker.patch("backend.core.config.settings.ADMIN_API_KEY", "")
    response = client.get(
        "/admin/movies/validate-posters/statistics",
        headers={"X-Admin-API-Key": "any-key"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin API is locked (no API key configured)"


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
