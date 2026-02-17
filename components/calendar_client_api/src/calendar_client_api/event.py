from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Optional


@dataclass
class Attendee:
    id: str
    email: str
    name: Optional[str] = None


class Event(ABC):
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
    def start_time(self) -> Optional[datetime]:
        """Returns the start datetime of the time-specific events, all-day events return None."""
        return None

    @property
    def end_time(self) -> Optional[datetime]:
        """Returns the end datetime of the time-specific events, all-day events return None."""
        return None

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
    def description(self) -> str:
        """Returns the description of the event."""
        raise NotImplementedError

    @property
    @abstractmethod
    def location(self) -> str:
        """Returns the location of the event."""
        raise NotImplementedError

    @property
    @abstractmethod
    def attachments(self) -> list[str]:
        """Returns the urls of the attachments of the event."""
        raise NotImplementedError

def get_event(calendar_id: str, event_id: str, raw_data: str) -> Event:
    """Return an instance of a Message.

    Args:
        calendar_id (str): The unique identifier for the calendar where the event belongs.
        event_id (str): The unique identifier for the event.
        raw_data (str): The calendar event raw data used to construct the event.

    Returns:
        Event: An instance conforming to the Event contract.

    Raises:
        NotImplementedError: If the function is not overridden by an implementation.

    """
    raise NotImplementedError