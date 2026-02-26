"""Google Calendar implementation of the Event interface."""

from datetime import datetime
from zoneinfo import ZoneInfo

from calendar_client_api import Attendee, Event


class GoogleCalendarEvent(Event):
    """Concrete implementation of the Event abstraction for Google Calendar."""

    def __init__(self, event_id: str, raw_data: str, calendar_id: str = "primary") -> None:
        """Initialize an instance of an Event implementation."""
        self._calendar_id = calendar_id
        self._event_id = event_id
        self._raw_data = raw_data

    @property
    def calendar_id(self) -> str:
        """The calendar id of the event."""
        return self._calendar_id

    @property
    def id(self) -> str:
        """The id of the event."""
        return self._event_id

    @property
    def title(self) -> str:
        """The title of the event."""
        return ""

    @property
    def start_time(self) -> datetime:
        """Returns the start datetime of the time-specific events, all-day events return None."""
        return datetime.now(tz=ZoneInfo("America/New_York"))

    @property
    def end_time(self) -> datetime:
        """Returns the end datetime of the time-specific events, all-day events return None."""
        return datetime.now(tz=ZoneInfo("America/New_York"))

    @property
    def description(self) -> str | None:
        """The description of the event."""
        return None

    @property
    def location(self) -> str | None:
        """The location of the event."""
        return None

    @property
    def attendees(self) -> list[Attendee]:
        """Returns the attendees of the event."""
        return []

    @property
    def attachments(self) -> list[str]:
        """The attachments of the event."""
        return []
