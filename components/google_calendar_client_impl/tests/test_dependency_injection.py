"""Test verifies that the implementation successfully registers the get_client function by dependency injection."""

from calendar_client_api import get_client

from google_calendar_client_impl import GoogleCalendarClient
from google_calendar_client_impl.client_impl import register_google_calendar_client


def test_get_client() -> None:
    """Test that dependency injection works and get_client returns the correct client."""
    register_google_calendar_client()
    client = get_client()
    assert isinstance(client, GoogleCalendarClient)
