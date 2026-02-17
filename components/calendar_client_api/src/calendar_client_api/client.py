# Core Calendar client contract definitions and factory placeholder

from abc import ABC, abstractmethod
from typing import Optional, Type

class CalendarClient(ABC):
    # This abstract class defines the contract/methods for any calendar client

    @abstractmethod
    def create_event(self, title:str, start: str, end: str) -> str:
        # Create Calndar event
        raise NotImplementedError

    @abstractmethod
    def get_event(self, event_id: str) -> dict:
        # Return an event and its details based on ID
        raise NotImplementedError

    @abstractmethod
    def list_events(self) -> list[dict]:
        # List calndar events and their details
        raise NotImplementedError

    @abstractmethod
    def update_event(self, event_id: str, title: str, start: str, end: str) -> None:
        # Updates a calendar event
        raise NotImplementedError

    @abstractmethod
    def delete_event(self, event_id: str) -> None:
        # Delete an event by ID
        raise NotImplementedError

# Stores the concrete CalendarClient class after registration.
# Used by get_client() to instantiate the active implementation.
_client_factory: Optional[type[CalendarClient]] = None

def register_client(factory: type[CalendarClient]) -> None:
    # Called by the implementation package during import.
    # Saves the concrete class so the interface can create instances.
    global _client_factory
    _client_factory = factory

def get_client() -> CalendarClient:
    if _client_factory is None:
    # Return an instance of the registered CalendarClient via dependency injection
    # Raises error if no implementation has been registered
        raise NotImplementedError
    return _client_factory()


