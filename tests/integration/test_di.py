"""Integration test for cross-package DI wiring."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock

if TYPE_CHECKING:
    from collections.abc import Iterator

import pytest
from calendar_client_api import CalendarClient
from calendar_client_api.registry import _ClientRegistry, get_client, register_client
from google_calendar_client_impl import GoogleCalendarClient


@pytest.fixture(autouse=True)
def _clean_registry() -> Iterator[None]:
    """Reset the DI registry before and after every test."""
    _ClientRegistry.clear()
    yield
    _ClientRegistry.clear()


@pytest.mark.integration
def test_google_calendar_client_satisfies_di_contract() -> None:
    """GoogleCalendarClient registered as a factory is resolved as a CalendarClient."""
    service = MagicMock()
    register_client(lambda: GoogleCalendarClient(service=service))

    client = get_client()

    assert isinstance(client, CalendarClient)
    assert isinstance(client, GoogleCalendarClient)
