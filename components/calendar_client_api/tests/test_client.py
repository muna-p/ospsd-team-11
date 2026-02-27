"""Unit tests for the calendar_client_api client module.

Contains unit tests for the CalendarClient class and the get_client function.
"""

import inspect
from collections.abc import Iterator
from datetime import datetime
from unittest.mock import Mock

import pytest

import calendar_client_api
import calendar_client_api.client
from calendar_client_api.client import CalendarClient
from calendar_client_api.event import Event, EventCreate, EventUpdate
from calendar_client_api.registry import _ClientRegistry, get_client, register_client


@pytest.fixture(autouse=True)
def clear_client_registry() -> Iterator[None]:
    """Ensure registry state does not leak across tests."""
    _ClientRegistry.clear()
    yield
    _ClientRegistry.clear()


class TestCalendarClientABC:
    """Test cases for the CalendarClient abstract base class."""

    def test_cannot_instantiate_abstract_class(self) -> None:
        """Test that CalendarClient cannot be instantiated directly."""
        with pytest.raises(TypeError):
            CalendarClient()  # type: ignore[abstract]

    def test_defines_expected_abstract_methods(self) -> None:
        """Test that CalendarClient declares exactly the expected abstract methods."""
        expected_methods = {
            "create_event",
            "get_event",
            "list_events",
            "list_events_between",
            "update_event",
            "delete_event",
        }

        abstract_methods = CalendarClient.__abstractmethods__

        assert expected_methods == abstract_methods

    def test_abstract_methods_are_decorated(self) -> None:
        """Test that all contract methods are explicitly abstract."""
        method_names = {
            "create_event",
            "get_event",
            "list_events",
            "list_events_between",
            "update_event",
            "delete_event",
        }

        for method_name in method_names:
            assert getattr(CalendarClient, method_name).__isabstractmethod__

    def test_minimal_concrete_subclass_can_be_instantiated(self) -> None:
        """Test that implementing all abstract methods allows instantiation."""

        class MinimalClient(CalendarClient):
            def create_event(self, event_create: EventCreate) -> Event:
                raise NotImplementedError

            def get_event(self, event_id: str) -> Event:
                raise NotImplementedError

            def list_events(self, max_results: int = 10) -> list[Event]:
                raise NotImplementedError

            def list_events_between(self, start: datetime, end: datetime) -> list[Event]:
                raise NotImplementedError

            def update_event(self, event_id: str, event_patch: EventUpdate) -> Event:
                raise NotImplementedError

            def delete_event(self, event_id: str) -> None:
                raise NotImplementedError

        client = MinimalClient()
        assert isinstance(client, CalendarClient)

    def test_list_events_default_max_results_is_10(self) -> None:
        """Test that list_events keeps backward-compatible default max_results."""
        signature = inspect.signature(CalendarClient.list_events)
        assert signature.parameters["max_results"].default == 10


class TestGetClient:
    """Test cases for the get_client dependency injection factory."""

    def test_raises_runtime_error_when_no_impl_registered(self) -> None:
        """Test that get_client raises RuntimeError before any impl is injected."""
        original = calendar_client_api.registry.get_client
        calendar_client_api.registry.get_client = get_client

        try:
            with pytest.raises(RuntimeError, match=r"No CalendarClient registered\."):
                calendar_client_api.registry.get_client()
        finally:
            calendar_client_api.registry.get_client = original

    def test_can_be_replaced_via_dependency_injection(self) -> None:
        """Test that get_client can be replaced by an implementation's factory."""
        original = calendar_client_api.registry.get_client
        mock_client = Mock(spec=CalendarClient)

        def fake_factory() -> CalendarClient:
            return mock_client

        calendar_client_api.registry.get_client = fake_factory  # type: ignore[assignment]

        try:
            result = calendar_client_api.registry.get_client()
            assert result is mock_client
        finally:
            calendar_client_api.registry.get_client = original

    def test_module_level_monkeypatched_reexport_raises_runtime_error(self) -> None:
        """Test that a monkeypatched module-level re-export raises RuntimeError."""
        original = calendar_client_api.get_client
        calendar_client_api.get_client = get_client

        try:
            with pytest.raises(RuntimeError, match=r"No CalendarClient registered\."):
                calendar_client_api.get_client()
        finally:
            calendar_client_api.get_client = original

    def test_get_client_uses_factory_each_call(self) -> None:
        """Test that get_client invokes the factory on every call."""
        created_clients: list[CalendarClient] = []

        def fake_factory() -> CalendarClient:
            client = Mock(spec=CalendarClient)
            created_clients.append(client)
            return client

        register_client(fake_factory)
        first = get_client()
        second = get_client()

        assert len(created_clients) == 2
        assert first is created_clients[0]
        assert second is created_clients[1]
        assert first is not second

    def test_get_client_propagates_factory_error(self) -> None:
        """Test that factory exceptions are not swallowed by get_client."""

        def fake_factory() -> CalendarClient:
            error_str = "factory failed"
            raise ValueError(error_str)

        register_client(fake_factory)
        with pytest.raises(ValueError, match="factory failed"):
            get_client()

    def test_clear_registry_then_get_raises_runtime_error(self) -> None:
        """Test that clearing registry resets get_client to unregistered state."""
        register_client(lambda: Mock(spec=CalendarClient))
        get_client()

        _ClientRegistry.clear()
        with pytest.raises(RuntimeError, match=r"No CalendarClient registered\."):
            get_client()

    def test_module_level_reexport_raises_runtime_error(self) -> None:
        """Test that package-level get_client mirrors registry behavior."""
        with pytest.raises(RuntimeError, match=r"No CalendarClient registered\."):
            calendar_client_api.get_client()
