"""Google Calendar implementation of the CalendarClient interface."""

from calendar_client_api.client import CalendarClient
from typing import Optional, type

class GoogleCalendarClient(CalendarClient):
    """Concrete implementation of CalendarClient using Google Calendar."""

    def __init__(self) -> None:
        """Initialize the Google calendar client."""
        self._default_calendar_id = "primary"

    def _resolve_calendar_id(self, calendar_id: Optional[str]) -> str:
        """Return provider calendar identifier, defaulting to the user's primary calendar."""
        return calendar_id or self._default_calendar_id

    def create_event(self, title: str, start: str, end: str, calendar_id: Optional[str]) -> str:
        """Create a new calendar event and return its ID."""
        raise NotImplementedError

    def get_event(self, event_id: str, calendar_id: Optional[str]) -> Event:
        """Retrieve a calendar event by its ID."""
        raise NotImplementedError

    def list_events(self, calendar_id: Optional[str] | None, max_results: int = 10) -> list[Event]:
        """Return a list of calendar events."""
        raise NotImplementedError

    def update_event(self, event_id: str, title: str, start: str, end: str, calendar_id: Optional[str]) -> None:
        """Update an existing calendar event."""
        raise NotImplementedError

    def delete_event(self, event_id: str, calendar_id: Optional[str]) -> None:
        """Delete a calendar event by its ID."""
        raise NotImplementedError

