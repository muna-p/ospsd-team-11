"""Unit tests for the calendar_client_api registry module."""

from collections.abc import Iterator
from unittest.mock import Mock

import pytest

from calendar_client_api.client import CalendarClient
from calendar_client_api.registry import _ClientRegistry, get_client, register_client


@pytest.fixture(autouse=True)
def clear_client_registry() -> Iterator[None]:
    """Ensure registry state does not leak across tests."""
    _ClientRegistry.clear()
    yield
    _ClientRegistry.clear()


def test_get_client_raises_when_not_registered() -> None:
    """Test that get_client raises RuntimeError when no client is registered."""
    with pytest.raises(RuntimeError, match="No CalendarClient registered"):
        get_client()


def test_register_and_get_client() -> None:
    """Test that a client can be registered and retrieved."""
    mock_client = Mock(spec=CalendarClient)

    def factory() -> CalendarClient:
        return mock_client

    register_client(factory)
    result = get_client()

    assert result is mock_client


def test_get_client_calls_factory_each_time() -> None:
    """Test that get_client calls the factory function each time."""
    call_count = 0
    expected_calls = 10

    def factory() -> CalendarClient:
        nonlocal call_count
        call_count += 1
        return Mock(spec=CalendarClient)

    register_client(factory)

    for _ in range(expected_calls):
        get_client()

    assert call_count == expected_calls


def test_register_client_replaces_previous() -> None:
    """Test that registering a new client replaces the previous one."""
    mock_client_1 = Mock(spec=CalendarClient)
    mock_client_2 = Mock(spec=CalendarClient)

    register_client(lambda: mock_client_1)
    result_1 = get_client()

    register_client(lambda: mock_client_2)
    result_2 = get_client()

    assert result_1 is mock_client_1
    assert result_2 is mock_client_2


def test_registry_comprehensive() -> None:
    """Verifies the complete registry lifecycle."""
    # Initially should raise
    with pytest.raises(RuntimeError):
        get_client()

    # Register first client
    mock_client_1 = Mock(spec=CalendarClient)
    register_client(lambda: mock_client_1)
    assert get_client() is mock_client_1

    # Register second client (replaces first)
    mock_client_2 = Mock(spec=CalendarClient)
    register_client(lambda: mock_client_2)
    assert get_client() is mock_client_2

    # Clear and verify
    _ClientRegistry.clear()
    with pytest.raises(RuntimeError):
        get_client()

    # Can register again after clear
    mock_client_3 = Mock(spec=CalendarClient)
    register_client(lambda: mock_client_3)
    assert get_client() is mock_client_3
