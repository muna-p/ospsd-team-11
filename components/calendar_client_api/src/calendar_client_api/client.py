"""Core Calendar client contract definitions and factory placeholder."""

from abc import ABC, abstractmethod
from calendar_client_api.event import Event
from typing import Optional

class CalendarClient(ABC):
    """Abstract class defines the contract/methods for any calendar client."""

    @abstractmethod
    def create_event(self, title:str, start: str, end: str, calendar_id: Optional[str]) -> Event:
        """Create Calendar event."""
        raise NotImplementedError

    @abstractmethod
    def get_event(self, event_id: str, calendar_id: Optional[str]) -> Event:
        """Return an event and its details based on ID."""
        raise NotImplementedError

    @abstractmethod
    def list_events(self, calendar_id: Optional[str], max_results: int = 10) -> list[Event]:
        """List calendar events and their details."""
        raise NotImplementedError

    @abstractmethod
    def update_event(self, event_id: str, title: str, start: str, end: str, calendar_id: Optional[str]) -> None:
        """Updates a calendar event."""
        raise NotImplementedError

    @abstractmethod
    def delete_event(self, event_id: str, calendar_id: Optional[str]) -> None:
        """Delete an event by ID."""
        raise NotImplementedError

"""Stores the concrete CalendarClient class after registration.
    Used by get_client() to instantiate the active implementation."""

_client_factory: Optional[type[CalendarClient]] = None

def register_client(factory: type[CalendarClient]) -> None:
    """Called by the implementation package during import.
    Saves the concrete class so the interface can create instances."""
    global _client_factory
    _client_factory = factory

def get_client() -> CalendarClient:
    if _client_factory is None:
        """Return an instance of the registered CalendarClient via dependency injection. Raises error if no implementation has been registered."""
        raise NotImplementedError
    return _client_factory()


