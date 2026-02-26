"""Event contract - Core event representation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


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
    def id(self) -> str:
        """Returns the ID of the event."""
        raise NotImplementedError

    @property
    @abstractmethod
    def title(self) -> str:
        """Returns the event title."""
        raise NotImplementedError

    @property
    def start_time(self) -> datetime:
        """Returns the start datetime of the time-specific events, all-day events return None."""
        raise NotImplementedError

    @property
    def end_time(self) -> datetime:
        """Returns the end datetime of the time-specific events, all-day events return None."""
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
    def attendees(self) -> list[Attendee]:
        """Returns the emails of the attendees."""
        raise NotImplementedError

    @property
    @abstractmethod
    def attachments(self) -> list[str]:
        """Returns the urls of the attachments of the event."""
        raise NotImplementedError
