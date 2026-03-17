"""Tests for the Google Calendar FastAPI service."""
from fastapi.testclient import TestClient
from google_calendar_service.main import app

HTTP_OK = 200

client = TestClient(app)


def test_health_endpoint() -> None:
    """Tests if the health endpoint returns a successful status response."""
    response = client.get("/health")

    assert response.status_code == HTTP_OK
    assert response.json() == {"status": "ok"}
