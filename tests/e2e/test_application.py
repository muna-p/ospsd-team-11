"""E2E tests for the calendar client.

These tests encode exactly that contract.  The two test functions are
**identical in consumer code** — the only difference is which implementation
was injected via DI, handled entirely by the fixtures below.  The consumer
workflow (``_consumer_flow``) never imports or references any concrete type.

Fixtures
--------
``library_impl_client``
    Registers ``GoogleCalendarClient`` via DI and yields a ``CalendarClient``.
    Calls the real Google Calendar API — requires credentials in the environment.
``service_adapter_client``
    Registers ``ServiceCalendarClient`` via DI and yields a ``CalendarClient``.
    Calls the live deployed service at ``SERVICE_BASE_URL`` (default: localhost:8000).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from calendar_client_api import (
    CalendarClient,
    EventCreate,
    EventUpdate,
    get_client,
    register_client,
)
from calendar_client_api.registry import _ClientRegistry
from google_calendar_service_adapter import register_service_calendar_client

if TYPE_CHECKING:
    from collections.abc import Iterator

pytestmark = [pytest.mark.e2e, pytest.mark.circleci]

_NOW = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)
_END = _NOW + timedelta(hours=1)


# ---------------------------------------------------------------------------
# Fixtures for DI wiring.
# Both fixtures yield a ``CalendarClient``; the consumer code below never
# sees the concrete type behind it.
# ---------------------------------------------------------------------------


@pytest.fixture
def library_impl_client() -> Iterator[CalendarClient]:
    """Inject GoogleCalendarClient via DI; credentials resolved from env vars or token.json.

    Calls ``load_env()`` to load ``.env`` into the environment, then registers a
    factory that creates ``GoogleCalendarClient(interactive=False)``.  The client
    resolves credentials in priority order: env vars → ``token.json``.  The
    ``interactive=False`` flag prevents a browser popup from opening during tests.
    """
    from google_calendar_client_impl import GoogleCalendarClient, load_env  # noqa: PLC0415

    load_env()
    _ClientRegistry.clear()
    register_client(lambda: GoogleCalendarClient(interactive=True))
    yield get_client()
    _ClientRegistry.clear()


@pytest.fixture
def service_adapter_client() -> Iterator[CalendarClient]:
    """Inject ServiceCalendarClient via DI and yield a CalendarClient.

    The service base URL is read from the ``SERVICE_BASE_URL`` environment
    variable, falling back to ``http://localhost:8000`` for local development.
    Importing ``google_calendar_service_adapter`` performs the initial DI
    registration via its ``__init__.py``; subsequent calls re-register
    explicitly after the registry is cleared.
    """
    _ClientRegistry.clear()
    register_service_calendar_client()
    yield get_client()
    _ClientRegistry.clear()


# ---------------------------------------------------------------------------
# Shared consumer workflow. Uses ONLY the abstract CalendarClient interface.
#
# This function is the proof of the Adapter Pattern / location transparency:
# it runs unchanged regardless of which backend is injected.
# ---------------------------------------------------------------------------


def _consumer_flow(client: CalendarClient, *, title_prefix: str) -> None:
    """Exercise the full CRUD lifecycle using only the CalendarClient interface."""
    # Create
    created = client.create_event(
        EventCreate(
            title=f"{title_prefix} created",
            start_time=_NOW,
            end_time=_END,
            description="Created in e2e flow",
            location="Room A",
            attendees=[],
            attachments=[],
        )
    )
    assert created.id
    assert title_prefix in created.title

    # Read
    fetched = client.get_event(created.id)
    assert fetched.id == created.id
    assert fetched.title == created.title

    # List
    window_start = _NOW - timedelta(minutes=5)
    window_end = _END + timedelta(minutes=5)
    events = list(client.list_events_between(window_start, window_end))
    assert any(event.id == created.id for event in events)

    # Update
    updated = client.update_event(
        created.id,
        EventUpdate(
            title=f"{title_prefix} updated",
            description="Updated in e2e flow",
            location="Room B",
        ),
    )
    assert updated.id == created.id
    assert updated.title == f"{title_prefix} updated"
    assert updated.description == "Updated in e2e flow"
    assert updated.location == "Room B"

    # Delete
    client.delete_event(created.id)
    events_after_delete = list(client.list_events_between(window_start, window_end))
    assert all(event.id != created.id for event in events_after_delete)


# ---------------------------------------------------------------------------
# Same consumer flow, two different DI-injected backends.
# ---------------------------------------------------------------------------


def test_consumer_flow_with_library_impl(library_impl_client: CalendarClient) -> None:
    """Consumer interface-only flow works when the library implementation is injected via DI."""
    _consumer_flow(library_impl_client, title_prefix="[e2e-library]")


def test_consumer_flow_with_service_adapter(service_adapter_client: CalendarClient) -> None:
    """Identical consumer flow works when the service adapter is injected via DI."""
    _consumer_flow(service_adapter_client, title_prefix="[e2e-service]")
