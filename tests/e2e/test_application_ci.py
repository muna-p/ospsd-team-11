"""CI-friendly E2E tests for service adapter using interface-only DI consumer flow.

These tests validate the highest abstraction level:
- consumer code depends only on `calendar_client_api.CalendarClient`
- service adapter implementation is injected via DI
- the consumer workflow never references concrete implementation types
"""

from __future__ import annotations

import importlib
import sys
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import TYPE_CHECKING, cast

import pytest
from calendar_client_api import CalendarClient, EventCreate, EventUpdate, get_client
from calendar_client_api.registry import _ClientRegistry
from google_calendar_service_adapter import register_service_calendar_client
from google_calendar_service_client.models.attendee_response import AttendeeResponse
from google_calendar_service_client.models.event_envelope import EventEnvelope
from google_calendar_service_client.models.event_response import EventResponse
from google_calendar_service_client.models.events_envelope import EventsEnvelope
from google_calendar_service_client.types import Unset

if TYPE_CHECKING:
    from collections.abc import Iterator

    from google_calendar_service_client.models.event_create_request import EventCreateRequest
    from google_calendar_service_client.models.event_update_request import EventUpdateRequest

pytestmark = [pytest.mark.e2e, pytest.mark.circleci]

_NOW = datetime(2026, 6, 1, 10, 0, tzinfo=UTC)
_END = _NOW + timedelta(hours=1)

<<<<<<< HEAD

def _fake_event_payload(
    *,
    event_id: str = "ci_evt_001",
    title: str = "CI Test Event",
    start: str = "2026-06-01T10:00:00+00:00",
    end: str = "2026-06-01T11:00:00+00:00",
    extras: dict[str, object] | None = None,
) -> dict[str, object]:
    """Return a realistic Google Calendar event JSON payload."""
    payload: dict[str, object] = {
        "id": event_id,
        "summary": title,
        "start": {"dateTime": start},
        "end": {"dateTime": end},
        "status": "confirmed",
        "description": "CI event description",
        "location": "CI Room",
    }
    if extras:
        payload.update(extras)
    return payload


def _fake_list_payload(events: list[dict[str, object]]) -> dict[str, object]:
    """Wrap a list of event payloads in a Google Calendar list response."""
    return {"kind": "calendar#events", "items": events}

=======
>>>>>>> upstream/main

@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    """Ensure DI registry state does not leak across tests."""
    _ClientRegistry.clear()
    yield
    _ClientRegistry.clear()


<<<<<<< HEAD
@pytest.fixture
def mock_service() -> MagicMock:
    """Return a MagicMock that mimics the Google Calendar service resource."""
    return MagicMock()


@pytest.fixture
def ci_client(mock_service: MagicMock) -> GoogleCalendarClient:
    """Return a GoogleCalendarClient wired to a mock service (no real credentials)."""
    return GoogleCalendarClient(service=mock_service)


def test_registry_wiring_with_mocked_auth() -> None:
    """DI registry resolves to a GoogleCalendarClient satisfying the CalendarClient ABC."""
    with (
        patch(
            "google_calendar_client_impl.client_impl.GoogleCalendarClient._auth_from_env",
            return_value=MagicMock(valid=True, refresh_token=None),
        ),
        patch("google_calendar_client_impl.client_impl.build", return_value=MagicMock()),
    ):
        assert _ClientRegistry._factory is None

        register_google_calendar_client()
        client = get_client()

    assert isinstance(client, GoogleCalendarClient)
    assert isinstance(client, CalendarClient)


def test_create_event_serializes_and_parses_response(ci_client: GoogleCalendarClient, mock_service: MagicMock) -> None:
    """create_event() serializes the request and parses the API response into an Event."""
    payload = _fake_event_payload(event_id="ci_create_001", title="CI Create Event")
    mock_service.events.return_value.insert.return_value.execute.return_value = payload

    event_data = EventCreate(
        title="CI Create Event",
        start_time=_NOW,
        end_time=_END,
        description="CI event description",
        location="CI Room",
        attendees=[],
=======
def _to_event_response(  # noqa: PLR0913
    *,
    event_id: str,
    title: str,
    start_time: datetime,
    end_time: datetime,
    description: str | None,
    location: str | None,
) -> EventResponse:
    """Build a generated EventResponse object."""
    return EventResponse(
        id=event_id,
        title=title,
        start_time=start_time,
        end_time=end_time,
        attendees=[AttendeeResponse(email="ci@example.com", name="CI User")],
>>>>>>> upstream/main
        attachments=[],
        description=description,
        location=location,
    )


def _install_service_adapter_mocks(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch generated endpoint calls used by the service adapter with in-memory handlers."""
    import google_calendar_service_adapter.client_adapter as adapter_module

    store: dict[str, EventResponse] = {}
    counter = {"value": 0}

    def create_sync(*, client: object, body: object) -> EventEnvelope:
        del client
        request = cast("EventCreateRequest", body)

        raw_description = request.description
        raw_location = request.location
        description = None if isinstance(raw_description, Unset) else raw_description
        location = None if isinstance(raw_location, Unset) else raw_location

        counter["value"] += 1
        event_id = f"ci_service_{counter['value']:03d}"

        created = _to_event_response(
            event_id=event_id,
            title=request.title,
            start_time=request.start_time,
            end_time=request.end_time,
            description=description,
            location=location,
        )
        store[event_id] = created
        return EventEnvelope(event=created)

    def get_sync(event_id: str, *, client: object) -> EventEnvelope:
        del client
        return EventEnvelope(event=store[event_id])

    def list_events_between_sync(*, client: object, start: datetime, end: datetime) -> EventsEnvelope:
        del client, start, end
        return EventsEnvelope(events=list(store.values()))

    def list_events_sync(*, client: object, max_results: int = 10) -> EventsEnvelope:
        del client
        return EventsEnvelope(events=list(store.values())[:max_results])

    def update_sync(event_id: str, *, client: object, body: object) -> EventEnvelope:
        del client
        request = cast("EventUpdateRequest", body)
        current = store[event_id]

        raw_title = request.title
        raw_start_time = request.start_time
        raw_end_time = request.end_time
        raw_description = request.description
        raw_location = request.location

        title = current.title if isinstance(raw_title, Unset) else raw_title
        start_time = current.start_time if isinstance(raw_start_time, Unset) else raw_start_time
        end_time = current.end_time if isinstance(raw_end_time, Unset) else raw_end_time
        description = current.description if isinstance(raw_description, Unset) else raw_description
        location = current.location if isinstance(raw_location, Unset) else raw_location

        updated = EventResponse(
            id=current.id,
            title=title if isinstance(title, str) else current.title,
            start_time=start_time if isinstance(start_time, datetime) else current.start_time,
            end_time=end_time if isinstance(end_time, datetime) else current.end_time,
            attendees=current.attendees,
            attachments=current.attachments,
            description=description,
            location=location,
        )
        store[event_id] = updated
        return EventEnvelope(event=updated)

    def delete_sync(event_id: str, *, client: object) -> None:
        del client
        store.pop(event_id, None)

    monkeypatch.setattr(adapter_module, "create_event_events_post", SimpleNamespace(sync=create_sync))
    monkeypatch.setattr(adapter_module, "get_event_events_event_id_get", SimpleNamespace(sync=get_sync))
    monkeypatch.setattr(adapter_module, "list_events_between_events_between_get", SimpleNamespace(sync=list_events_between_sync))
    monkeypatch.setattr(adapter_module, "list_events_events_get", SimpleNamespace(sync=list_events_sync))
    monkeypatch.setattr(adapter_module, "update_event_events_event_id_patch", SimpleNamespace(sync=update_sync))
    monkeypatch.setattr(adapter_module, "delete_event_events_event_id_delete", SimpleNamespace(sync=delete_sync))


def _consumer_flow(client: CalendarClient, *, title_prefix: str) -> None:
    """Consumer workflow that uses only the abstract CalendarClient interface."""
    created = client.create_event(
        EventCreate(
            title=f"{title_prefix} created",
            start_time=_NOW,
            end_time=_END,
            description="Created by CI e2e",
            location="CI Room",
            attendees=[],
            attachments=[],
        )
    )
    assert created.id
    assert title_prefix in created.title

<<<<<<< HEAD
    # Verify response handling
    assert event.id == "ci_create_001"
    assert event.title == "CI Create Event"
    assert event.description == "CI event description"
    assert event.location == "CI Room"
    assert event.start_time == _NOW
    assert event.end_time == _END


def test_get_event_returns_parsed_event(ci_client: GoogleCalendarClient, mock_service: MagicMock) -> None:
    """get_event() fetches by ID and returns a fully parsed Event."""
    payload = _fake_event_payload(event_id="ci_get_001", title="CI Get Event")
    mock_service.events.return_value.get.return_value.execute.return_value = payload

    event = ci_client.get_event("ci_get_001")

    mock_service.events.return_value.get.assert_called_once_with(
        calendarId="primary",
        eventId="ci_get_001",
    )
    assert event.id == "ci_get_001"
    assert event.title == "CI Get Event"


def test_list_events_returns_all_items(ci_client: GoogleCalendarClient, mock_service: MagicMock) -> None:
    """list_events_between() returns all items from the API list payload."""
    start = datetime(2026, 6, 1, 0, 0, tzinfo=UTC)
    end = datetime(2026, 6, 2, 0, 0, tzinfo=UTC)

    payloads = [
        _fake_event_payload(event_id="ci_list_001", title="Event A"),
        _fake_event_payload(event_id="ci_list_002", title="Event B"),
        _fake_event_payload(event_id="ci_list_003", title="Event C"),
    ]
    mock_service.events.return_value.list.return_value.execute.return_value = _fake_list_payload(payloads)

    events = list(ci_client.list_events_between(start, end))

    assert len(events) == len(payloads)
    assert [e.id for e in events] == ["ci_list_001", "ci_list_002", "ci_list_003"]
    assert [e.title for e in events] == ["Event A", "Event B", "Event C"]


def test_update_event_sends_patch_and_returns_updated_event(ci_client: GoogleCalendarClient, mock_service: MagicMock) -> None:
    """update_event() sends only the changed fields and parses the updated response."""
    updated_payload = _fake_event_payload(
        event_id="ci_upd_001",
        title="CI Updated Event",
        extras={"description": "Updated description", "location": "New Room"},
    )
    mock_service.events.return_value.patch.return_value.execute.return_value = updated_payload

    patch = EventUpdate(title="CI Updated Event", description="Updated description", location="New Room")
    event = ci_client.update_event("ci_upd_001", patch)

    mock_service.events.return_value.patch.assert_called_once_with(
        calendarId="primary",
        eventId="ci_upd_001",
        body={"summary": "CI Updated Event", "description": "Updated description", "location": "New Room"},
        supportsAttachments=True,
    )
    assert event.id == "ci_upd_001"
    assert event.title == "CI Updated Event"
    assert event.description == "Updated description"
    assert event.location == "New Room"


def test_delete_event_calls_api(ci_client: GoogleCalendarClient, mock_service: MagicMock) -> None:
    """delete_event() calls the Google Calendar delete API with the correct identifiers."""
    ci_client.delete_event("ci_del_001")

    mock_service.events.return_value.delete.assert_called_once_with(
        calendarId="primary",
        eventId="ci_del_001",
    )
    mock_service.events.return_value.delete.return_value.execute.assert_called_once_with()


def test_full_crud_lifecycle_ci(ci_client: GoogleCalendarClient, mock_service: MagicMock) -> None:
    """Full CRUD workflow against a mocked service: create -> get -> list -> update -> delete."""
    base_payload = _fake_event_payload(event_id="ci_crud_001", title="CI CRUD Event")

    # Create
    mock_service.events.return_value.insert.return_value.execute.return_value = base_payload
    event_data = EventCreate(
        title="CI CRUD Event",
        start_time=_NOW,
        end_time=_END,
        attendees=[],
        attachments=[],
    )
    created = ci_client.create_event(event_data)
    assert created.id == "ci_crud_001"
    assert created.title == "CI CRUD Event"

    # Get
    mock_service.events.return_value.get.return_value.execute.return_value = base_payload
    fetched = ci_client.get_event(created.id)
    assert fetched.id == created.id
    assert fetched.title == created.title

    # List
    mock_service.events.return_value.list.return_value.execute.return_value = _fake_list_payload([base_payload])
    start = _NOW - timedelta(minutes=5)
    end = _END + timedelta(minutes=5)
    events = list(ci_client.list_events_between(start, end))
    assert any(e.id == "ci_crud_001" for e in events)

    # Update
    updated_payload = _fake_event_payload(event_id="ci_crud_001", title="CI CRUD Updated", extras={"description": "Updated"})
    mock_service.events.return_value.patch.return_value.execute.return_value = updated_payload
    patch = EventUpdate(title="CI CRUD Updated", description="Updated")
    updated = ci_client.update_event(created.id, patch)
    assert updated.id == "ci_crud_001"
    assert updated.title == "CI CRUD Updated"
    assert updated.description == "Updated"
=======
    fetched = client.get_event(created.id)
    assert fetched.id == created.id
    assert fetched.title == created.title

    window_start = _NOW - timedelta(minutes=5)
    window_end = _END + timedelta(minutes=5)
    events = list(client.list_events_between(window_start, window_end))
    assert any(event.id == created.id for event in events)

    updated_title = f"{title_prefix} updated"
    updated = client.update_event(
        created.id,
        EventUpdate(
            title=updated_title,
            description="Updated by CI e2e",
            location="Updated Room",
        ),
    )
    assert updated.id == created.id
    assert updated.title == updated_title
    assert updated.description == "Updated by CI e2e"
    assert updated.location == "Updated Room"
>>>>>>> upstream/main

    client.delete_event(created.id)
    events_after_delete = list(client.list_events_between(window_start, window_end))
    assert all(event.id != created.id for event in events_after_delete)


def test_interface_consumer_flow_with_service_adapter_via_di(monkeypatch: pytest.MonkeyPatch) -> None:
    """Same interface-only consumer code works when service adapter is injected through DI."""
    _install_service_adapter_mocks(monkeypatch)
    register_service_calendar_client(base_url="http://ci-mocked-service:8000")

    client = get_client()
    assert isinstance(client, CalendarClient)

    _consumer_flow(client, title_prefix="[service-adapter]")


def test_import_side_effect_registers_service_adapter_factory() -> None:
    """Import side effect registers service adapter in DI registry."""
    assert _ClientRegistry._factory is None

    module = sys.modules["google_calendar_service_adapter"]
    importlib.reload(module)

    assert _ClientRegistry._factory is not None
    client = get_client()
    assert isinstance(client, CalendarClient)
    assert client.__class__.__name__ == "ServiceCalendarClient"
