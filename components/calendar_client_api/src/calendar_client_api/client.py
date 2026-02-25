"""Core Calendar client contract definitions and factory placeholder."""

from abc import ABC, abstractmethod
from datetime import datetime

from calendar_client_api.event import Event


class CalendarClient(ABC):
    """Abstract class defines the contract/methods for any calendar client."""

    @abstractmethod
    def create_event(
        self, title: str, start: datetime, end: datetime, calendar_id: str = "primary"
    ) -> Event:
        """Create Calendar event."""
        raise NotImplementedError

    @abstractmethod
    def get_event(self, event_id: str, calendar_id: str = "primary") -> Event:
        """Return an event and its details based on ID."""
        raise NotImplementedError

    @abstractmethod
    def list_events(self, calendar_id: str = "primary", max_results: int = 10) -> list[Event]:
        """List calendar events and their details."""
        raise NotImplementedError

    @abstractmethod
    def update_event(
        self,
        event_id: str,
        title: str,
        start: datetime,
        end: datetime,
        calendar_id: str = "primary",
    ) -> None:
        """Update a calendar event."""
        raise NotImplementedError

    @abstractmethod
    def delete_event(self, event_id: str, calendar_id: str = "primary") -> None:
        """Delete an event by ID."""
        raise NotImplementedError


def get_client() -> CalendarClient:
    """Return an instance of the registered CalendarClient via dependency injection.

    Raises error if no implementation has been registered.
    """
    raise NotImplementedError
