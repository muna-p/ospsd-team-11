"""Google Calendar implementation of the Event interface."""

from datetime import date, datetime
from zoneinfo import ZoneInfo

import calendar_client_api
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
    def start_date(self) -> date:
        """The start date of the event."""
        return datetime.now(tz=ZoneInfo("America/New_York")).date()

    @property
    def end_date(self) -> date:
        """The end date of the event."""
        return datetime.now(tz=ZoneInfo("America/New_York")).date()

    @property
    def is_all_day(self) -> bool:
        """Whether the event is all day or not."""
        return False

    @property
    def start_time(self) -> datetime | None:
        """Returns the start datetime of the time-specific events, all-day events return None."""
        return None

    @property
    def end_time(self) -> datetime | None:
        """Returns the end datetime of the time-specific events, all-day events return None."""
        return None

    @property
    def attendees(self) -> list[Attendee]:
        """Returns the attendees of the event."""
        return []

    @property
    def description(self) -> str | None:
        """The description of the event."""
        return None

    @property
    def location(self) -> str | None:
        """The location of the event."""
        return None

    @property
    def attachments(self) -> list[str]:
        """The attachments of the event."""
        return []


def get_google_calendar_event(event_id: str, raw_data: str, calendar_id: str = "primary") -> Event:
    """Return an instance of an Event implementation.

    Args:
        event_id (str): The unique identifier for the event.
        raw_data (str): The calendar event raw data used to construct the event.
        calendar_id (str): The unique identifier for the calendar where the event belongs.

    Returns:
        Event: An instance conforming to the Event contract.

    """
    return GoogleCalendarEvent(event_id, raw_data, calendar_id)


def register_google_calendar_event() -> None:
    """Register a Google Calendar event implementation with the event abstraction."""
    calendar_client_api.event.get_event = get_google_calendar_event
    calendar_client_api.get_event = get_google_calendar_event
