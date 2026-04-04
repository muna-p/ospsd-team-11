"""Integration tests for DI wiring."""

import importlib
from collections.abc import Iterator
from unittest.mock import Mock, patch

import google_calendar_client_impl
import pytest
from calendar_client_api import CalendarClient
from calendar_client_api.event import Event
from calendar_client_api.registry import _ClientRegistry, get_client, register_client
from google_calendar_client_impl import GoogleCalendarClient, GoogleCalendarEvent
from google_calendar_client_impl.client_impl import get_google_calendar_client


@pytest.fixture(autouse=True)
def clear_client_registry() -> Iterator[None]:
    """Ensure registry state does not leak across tests."""
    _ClientRegistry.clear()
    yield
    _ClientRegistry.clear()


@pytest.mark.integration
def test_import_auto_registers_factory() -> None:
    """Importing google_calendar_client_impl auto-registers the factory."""
    assert _ClientRegistry._factory is None

    importlib.reload(google_calendar_client_impl)

    assert _ClientRegistry._factory is not None
    assert _ClientRegistry._factory is get_google_calendar_client


@pytest.mark.integration
@patch("google_calendar_client_impl.client_impl.build", return_value=Mock())
@patch(
    "google_calendar_client_impl.client_impl.GoogleCalendarClient._auth_from_env",
    return_value=Mock(valid=True, refresh_token=None),
)
def test_get_client_returns_google_calendar_client_instance(*_: Mock) -> None:
    """get_client() returns a GoogleCalendarClient that satisfies the CalendarClient ABC."""
    importlib.reload(google_calendar_client_impl)

    client = get_client()

    assert isinstance(client, GoogleCalendarClient)
    assert isinstance(client, CalendarClient)


@pytest.mark.integration
def test_get_client_raises_runtime_error_when_registry_empty() -> None:
    """get_client() raises RuntimeError when no implementation has been registered."""
    with pytest.raises(RuntimeError, match=r"No CalendarClient registered\."):
        get_client()


@pytest.mark.integration
def test_registered_factory_is_correct_function() -> None:
    """The registered factory is specifically get_google_calendar_client."""
    importlib.reload(google_calendar_client_impl)

    assert _ClientRegistry._factory is get_google_calendar_client


@pytest.mark.integration
def test_workspace_dependency_chain_resolves() -> None:
    """Workspace wiring allows impl to import from api, type hierarchies are correct."""
    assert issubclass(GoogleCalendarClient, CalendarClient)
    assert issubclass(GoogleCalendarEvent, Event)


@pytest.mark.integration
@patch("google_calendar_client_impl.client_impl.build", return_value=Mock())
@patch(
    "google_calendar_client_impl.client_impl.GoogleCalendarClient._auth_from_env",
    return_value=Mock(valid=True, refresh_token=None),
)
def test_multiple_imports_do_not_break_registration(*_: Mock) -> None:
    """Reimporting the impl module multiple times does not corrupt the registry."""
    importlib.reload(google_calendar_client_impl)
    importlib.reload(google_calendar_client_impl)

    client = get_client()

    assert isinstance(client, GoogleCalendarClient)
    assert isinstance(client, CalendarClient)


@pytest.mark.integration
@patch("google_calendar_client_impl.client_impl.build", return_value=Mock())
@patch(
    "google_calendar_client_impl.client_impl.GoogleCalendarClient._auth_from_env",
    return_value=Mock(valid=True, refresh_token=None),
)
def test_get_client_returns_new_instance_each_call(*_: Mock) -> None:
    """get_client() invokes the factory each time, returning different instances."""
    importlib.reload(google_calendar_client_impl)

    first = get_client()
    second = get_client()

    assert first is not second
    assert isinstance(first, GoogleCalendarClient)
    assert isinstance(second, GoogleCalendarClient)


@pytest.mark.integration
@patch("google_calendar_client_impl.client_impl.build", return_value=Mock())
@patch(
    "google_calendar_client_impl.client_impl.GoogleCalendarClient._auth_from_env",
    return_value=Mock(valid=True, refresh_token=None),
)
def test_register_client_replaces_previous_factory(*_: Mock) -> None:
    """Registering a new factory replaces the previous one."""
    fake_client = Mock(spec=CalendarClient)
    register_client(lambda: fake_client)

    assert get_client() is fake_client

    importlib.reload(google_calendar_client_impl)

    client = get_client()

    assert isinstance(client, GoogleCalendarClient)
    assert client is not fake_client


@pytest.mark.integration
@patch("google_calendar_client_impl.client_impl.GoogleCalendarClient._auth_from_interactive", return_value=None)
@patch("google_calendar_client_impl.client_impl.GoogleCalendarClient._auth_from_file", return_value=None)
@patch("google_calendar_client_impl.client_impl.GoogleCalendarClient._auth_from_env", return_value=None)
def test_get_client_propagates_factory_error(*_: Mock) -> None:
    """Factory auth failure propagates through get_client() as RuntimeError."""
    importlib.reload(google_calendar_client_impl)

    with pytest.raises(RuntimeError, match="Failed to authenticate with Google Calendar API"):
        get_client()
