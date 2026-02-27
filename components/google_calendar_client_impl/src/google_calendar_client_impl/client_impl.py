"""Google Calendar implementation of the CalendarClient interface."""

from collections.abc import Iterable
from datetime import datetime

import calendar_client_api
from calendar_client_api import CalendarClient, Event, EventCreate, EventUpdate


class GoogleCalendarClient(CalendarClient):
    """Concrete implementation of CalendarClient using Google Calendar."""

    def __init__(self) -> None:
        """Initialize the Google calendar client."""
        self._default_calendar_id = "primary"

    def create_event(self, event_create: EventCreate, calendar_id: str = "primary") -> Event:
        """Create a new calendar event and return its ID."""
        raise NotImplementedError

    def get_event(self, event_id: str, calendar_id: str = "primary") -> Event:
        """Retrieve a calendar event by its ID."""
        raise NotImplementedError

    def list_events(self, max_results: int = 10, calendar_id: str = "primary") -> Iterable[Event]:
        """Return an iterable of calendar events."""
        raise NotImplementedError

    def list_events_between(
        self, start: datetime, end: datetime, calendar_id: str = "primary"
    ) -> Iterable[Event]:
        """Return an iterable of calendar events between two dates."""
        raise NotImplementedError

    def update_event(
        self,
        event_id: str,
        event_patch: EventUpdate,
        calendar_id: str = "primary",
    ) -> Event:
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
    calendar_client_api.register_client(get_google_calendar_client)
