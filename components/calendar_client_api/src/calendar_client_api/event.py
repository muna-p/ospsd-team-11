"""Event contract - Core event representation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Attendee:
    """An attendee for an event."""

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
    @abstractmethod
    def start_time(self) -> datetime:
        """Returns the start datetime of the time-specific events."""
        raise NotImplementedError

    @property
    @abstractmethod
    def end_time(self) -> datetime:
        """Returns the end datetime of the time-specific events."""
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


@dataclass(frozen=True)
class EventCreate:
    """Information used to create an event."""

    title: str
    start_time: datetime
    end_time: datetime
    attendees: list[Attendee]
    attachments: list[str]
    description: str | None = None
    location: str | None = None


class _UnsetType:
    """Sentinel type used to represent an unset value."""

    __slots__ = ()

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "UNSET"


UNSET = _UnsetType()


@dataclass(frozen=True)
class EventUpdate:
    """Information used to update an event."""

    title: str | _UnsetType = UNSET
    start_time: datetime | _UnsetType = UNSET
    end_time: datetime | _UnsetType = UNSET
    description: str | None | _UnsetType = UNSET
    location: str | None | _UnsetType = UNSET
