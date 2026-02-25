"""Event contract - Core event representation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class Attendee:
    """An attendee for an event."""

    id: str
    email: str
    name: str | None = None


class Event(ABC):
    """An abstract class representing an Event."""

    @property
    @abstractmethod
    def calendar_id(self) -> str:
        """Returns the calendar ID where the event belongs to."""
        raise NotImplementedError

    @property
    @abstractmethod
    def id(self) -> str:
        """Returns the ID of the event."""
        raise NotImplementedError

    @property
    @abstractmethod
    def title(self) -> str:
        """Returns the event title."""
        raise NotImplementedError

    @property
    @abstractmethod
    def start_date(self) -> date:
        """Returns the start date of the event."""
        raise NotImplementedError

    @property
    @abstractmethod
    def end_date(self) -> date:
        """Returns the end date of the event."""
        raise NotImplementedError

    @property
    def start_time(self) -> datetime | None:
        """Returns the start datetime of the time-specific events, all-day events return None."""
        raise NotImplementedError

    @property
    def end_time(self) -> datetime | None:
        """Returns the end datetime of the time-specific events, all-day events return None."""
        raise NotImplementedError

    @property
    @abstractmethod
    def is_all_day(self) -> bool:
        """Returns True if this is an all-day event."""
        raise NotImplementedError

    @property
    @abstractmethod
    def attendees(self) -> list[Attendee]:
        """Returns the emails of the attendees."""
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str | None:
        """Returns the description of the event."""
        raise NotImplementedError

    @property
    @abstractmethod
    def location(self) -> str | None:
        """Returns the location of the event."""
        raise NotImplementedError

    @property
    @abstractmethod
    def attachments(self) -> list[str]:
        """Returns the urls of the attachments of the event."""
        raise NotImplementedError


def get_event(event_id: str, raw_data: str, calendar_id: str = "primary") -> Event:
    """Return an instance of a Event.

    Args:
        event_id (str): The unique identifier for the event.
        raw_data (str): The calendar event raw data used to construct the event.
        calendar_id (str): The unique identifier for the calendar where the event belongs.

    Returns:
        Event: An instance conforming to the Event contract.

    Raises:
        NotImplementedError: If the function is not overridden by an implementation.

    """
    raise NotImplementedError
