"""Google Calendar implementation of the CalendarClient interface."""

from datetime import datetime

import calendar_client_api
from calendar_client_api import CalendarClient, Event


class GoogleCalendarClient(CalendarClient):
    """Concrete implementation of CalendarClient using Google Calendar."""

    def __init__(self) -> None:
        """Initialize the Google calendar client."""
        self._default_calendar_id = "primary"

    def create_event(
        self, title: str, start: datetime, end: datetime, calendar_id: str = "primary"
    ) -> Event:
        """Create a new calendar event and return its ID."""
        raise NotImplementedError

    def get_event(self, event_id: str, calendar_id: str = "primary") -> Event:
        """Retrieve a calendar event by its ID."""
        raise NotImplementedError

    def list_events(self, calendar_id: str = "primary", max_results: int = 10) -> list[Event]:
        """Return a list of calendar events."""
        raise NotImplementedError

    def update_event(
        self,
        event_id: str,
        title: str,
        start: datetime,
        end: datetime,
        calendar_id: str = "primary",
    ) -> None:
        """Update an existing calendar event."""
        raise NotImplementedError

    def delete_event(self, event_id: str, calendar_id: str = "primary") -> None:
        """Delete a calendar event by its ID."""
        raise NotImplementedError


def get_google_calendar_client() -> GoogleCalendarClient:
    """Get a Google Calendar client."""
    return GoogleCalendarClient()


def register_google_calendar_client() -> None:
    """Register a Google Calendar client."""
    calendar_client_api.get_client = get_google_calendar_client
    calendar_client_api.client.get_client = get_google_calendar_client
