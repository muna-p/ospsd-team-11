<<<<<<< HEAD
"""Tests for the Google Calendar FastAPI service."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime

import google_calendar_service.main as main_module
=======
# ruff: noqa: D101, D102, D103, D107
"""Tests for the Google Calendar FastAPI service."""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime

>>>>>>> upstream/main
import pytest
from calendar_client_api.event import Attendee, Event, EventCreate, EventUpdate
from fastapi.testclient import TestClient
from google_calendar_service.main import app
<<<<<<< HEAD
=======
from google_calendar_service.routes import event_routes
>>>>>>> upstream/main

HTTP_OK = 200
DEFAULT_MAX_RESULTS = 10

client = TestClient(app)


<<<<<<< HEAD
=======
@pytest.fixture(autouse=True)
def override_get_client_dependency() -> Iterator[None]:
    """Override the events router _get_client dependency with a fake client."""
    app.dependency_overrides[event_routes._get_client] = fake_get_client
    yield
    app.dependency_overrides.pop(event_routes._get_client, None)


>>>>>>> upstream/main
@dataclass(frozen=True)
class FakeEventData:
    """Concrete event data used to back a fake Event implementation."""

    event_id: str
    title: str
    start_time: datetime
    end_time: datetime
    description: str | None = None
    location: str | None = None
    attendees: list[Attendee] | None = None
    attachments: list[str] | None = None


class FakeEvent(Event):
    """Fake event used for service tests."""

    def __init__(self, data: FakeEventData) -> None:
<<<<<<< HEAD
        """Initialize a fake event from test data."""
=======
>>>>>>> upstream/main
        self._data = data

    @property
    def id(self) -> str:
<<<<<<< HEAD
        """Return the event ID."""
=======
>>>>>>> upstream/main
        return self._data.event_id

    @property
    def title(self) -> str:
<<<<<<< HEAD
        """Return the event title."""
=======
>>>>>>> upstream/main
        return self._data.title

    @property
    def start_time(self) -> datetime:
<<<<<<< HEAD
        """Return the start time."""
=======
>>>>>>> upstream/main
        return self._data.start_time

    @property
    def end_time(self) -> datetime:
<<<<<<< HEAD
        """Return the end time."""
=======
>>>>>>> upstream/main
        return self._data.end_time

    @property
    def description(self) -> str | None:
<<<<<<< HEAD
        """Return the description."""
=======
>>>>>>> upstream/main
        return self._data.description

    @property
    def location(self) -> str | None:
<<<<<<< HEAD
        """Return the location."""
=======
>>>>>>> upstream/main
        return self._data.location

    @property
    def attendees(self) -> list[Attendee]:
<<<<<<< HEAD
        """Return the attendees."""
=======
>>>>>>> upstream/main
        return self._data.attendees or []

    @property
    def attachments(self) -> list[str]:
<<<<<<< HEAD
        """Return the attachments."""
=======
>>>>>>> upstream/main
        return self._data.attachments or []


class FakeCalendarClient:
    """Fake calendar client used for service tests."""

    def list_events(self, max_results: int = DEFAULT_MAX_RESULTS) -> Iterable[Event]:
<<<<<<< HEAD
        """Return fake events."""
=======
>>>>>>> upstream/main
        assert max_results == DEFAULT_MAX_RESULTS
        return [
            FakeEvent(
                FakeEventData(
                    event_id="test_123",
                    title="Networking Event",
                    start_time=datetime(2026, 3, 18, 10, 0, tzinfo=UTC),
                    end_time=datetime(2026, 3, 18, 11, 0, tzinfo=UTC),
                    description="NYU event",
                    location="2 MetroTech",
                    attendees=[Attendee(email="test@example.com", name="Joe")],
                    attachments=["https://example.com/doc"],
                )
            ),
        ]

    def get_event(self, event_id: str) -> Event:
<<<<<<< HEAD
        """Return one fake event by ID."""
=======
>>>>>>> upstream/main
        assert event_id == "test_123"
        return FakeEvent(
            FakeEventData(
                event_id="test_123",
                title="Networking Event",
                start_time=datetime(2026, 3, 18, 10, 0, tzinfo=UTC),
                end_time=datetime(2026, 3, 18, 11, 0, tzinfo=UTC),
                description="NYU event",
                location="2 MetroTech",
                attendees=[Attendee(email="test@example.com", name="Joe")],
                attachments=["https://example.com/doc"],
            )
        )

    def create_event(self, event_create: EventCreate) -> Event:
<<<<<<< HEAD
        """Return a created fake event."""
=======
>>>>>>> upstream/main
        assert event_create.title == "Java Exam"
        assert event_create.description == "Java Midterm"
        assert event_create.location == "2 MetroTech"
        assert len(event_create.attendees) == 1
        assert event_create.attendees[0] == Attendee(email="designer@example.com", name="Designer")
        assert event_create.attachments == ["https://example.com/spec"]

        return FakeEvent(
            FakeEventData(
                event_id="evt_created",
                title=event_create.title,
                start_time=event_create.start_time,
                end_time=event_create.end_time,
                description=event_create.description,
                location=event_create.location,
                attendees=event_create.attendees,
                attachments=event_create.attachments,
            )
        )

    def update_event(self, event_id: str, event_update: EventUpdate) -> Event:
<<<<<<< HEAD
        """Return an updated fake event."""
=======
>>>>>>> upstream/main
        assert event_id == "test_123"
        assert event_update.title == "Updated Java Midterm"
        assert event_update.location == "New 2 MetroTech Room"

        return FakeEvent(
            FakeEventData(
                event_id="test_123",
                title="Updated Java Midterm",
                start_time=datetime(2026, 3, 18, 10, 0, tzinfo=UTC),
                end_time=datetime(2026, 3, 18, 11, 0, tzinfo=UTC),
                description=None,
                location="2 MetroTech Room",
                attendees=[Attendee(email="test@example.com", name="Joe")],
                attachments=["https://example.com/doc"],
            )
        )

    def delete_event(self, event_id: str) -> None:
<<<<<<< HEAD
        """Delete a fake event."""
=======
>>>>>>> upstream/main
        assert event_id == "test_123"


def fake_get_client() -> FakeCalendarClient:
<<<<<<< HEAD
    """Return a fake calendar client."""
=======
>>>>>>> upstream/main
    return FakeCalendarClient()


class TestHealthEndpoint:
<<<<<<< HEAD
    """Tests for the health endpoint."""

    def test_returns_ok_status(self) -> None:
        """Return a successful health response."""
=======
    def test_returns_ok_status(self) -> None:
>>>>>>> upstream/main
        response = client.get("/health")

        assert response.status_code == HTTP_OK
        assert response.json() == {"status": "ok"}


class TestListEventsEndpoint:
<<<<<<< HEAD
    """Tests for the list events endpoint."""

    def test_returns_serialized_events(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Return serialized event data from the client."""
        monkeypatch.setattr(main_module, "get_client", fake_get_client)

        response = client.get("/events")
=======
    def test_returns_serialized_events(self) -> None:
        response = client.get("/events/")
>>>>>>> upstream/main

        assert response.status_code == HTTP_OK
        assert response.json() == {
            "events": [
                {
                    "id": "test_123",
                    "title": "Networking Event",
                    "start_time": "2026-03-18T10:00:00Z",
                    "end_time": "2026-03-18T11:00:00Z",
                    "description": "NYU event",
                    "location": "2 MetroTech",
                    "attendees": [
                        {
                            "email": "test@example.com",
                            "name": "Joe",
                        },
                    ],
                    "attachments": ["https://example.com/doc"],
                },
            ],
        }


class TestGetEventEndpoint:
<<<<<<< HEAD
    """Tests for the get event endpoint."""

    def test_returns_serialized_event(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Return one serialized event by ID."""
        monkeypatch.setattr(main_module, "get_client", fake_get_client)

=======
    def test_returns_serialized_event(self) -> None:
>>>>>>> upstream/main
        response = client.get("/events/test_123")

        assert response.status_code == HTTP_OK
        assert response.json() == {
            "event": {
                "id": "test_123",
                "title": "Networking Event",
                "start_time": "2026-03-18T10:00:00Z",
                "end_time": "2026-03-18T11:00:00Z",
                "description": "NYU event",
                "location": "2 MetroTech",
                "attendees": [
                    {
                        "email": "test@example.com",
                        "name": "Joe",
                    },
                ],
                "attachments": ["https://example.com/doc"],
            },
        }


class TestCreateEventEndpoint:
<<<<<<< HEAD
    """Tests for the create event endpoint."""

    def test_creates_and_returns_serialized_event(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Create an event and return serialized event data."""
        monkeypatch.setattr(main_module, "get_client", fake_get_client)

        response = client.post(
            "/events",
=======
    def test_creates_and_returns_serialized_event(self) -> None:
        response = client.post(
            "/events/",
>>>>>>> upstream/main
            json={
                "title": "Java Exam",
                "start_time": "2026-03-20T14:00:00+00:00",
                "end_time": "2026-03-20T15:00:00+00:00",
                "attendees": [
                    {
                        "email": "designer@example.com",
                        "name": "Designer",
                    },
                ],
                "attachments": ["https://example.com/spec"],
                "description": "Java Midterm",
                "location": "2 MetroTech",
            },
        )

        assert response.status_code == HTTP_OK
        assert response.json() == {
            "event": {
                "id": "evt_created",
                "title": "Java Exam",
                "start_time": "2026-03-20T14:00:00Z",
                "end_time": "2026-03-20T15:00:00Z",
                "description": "Java Midterm",
                "location": "2 MetroTech",
                "attendees": [
                    {
                        "email": "designer@example.com",
                        "name": "Designer",
                    },
                ],
                "attachments": ["https://example.com/spec"],
            },
        }


class TestUpdateEventEndpoint:
<<<<<<< HEAD
    """Tests for the update event endpoint."""

    def test_updates_and_returns_serialized_event(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Update an event and return serialized event data."""
        monkeypatch.setattr(main_module, "get_client", fake_get_client)

=======
    def test_updates_and_returns_serialized_event(self) -> None:
>>>>>>> upstream/main
        response = client.patch(
            "/events/test_123",
            json={
                "title": "Updated Java Midterm",
                "location": "New 2 MetroTech Room",
            },
        )

        assert response.status_code == HTTP_OK
        assert response.json() == {
            "event": {
                "id": "test_123",
                "title": "Updated Java Midterm",
                "start_time": "2026-03-18T10:00:00Z",
                "end_time": "2026-03-18T11:00:00Z",
                "description": None,
                "location": "2 MetroTech Room",
                "attendees": [
                    {
                        "email": "test@example.com",
                        "name": "Joe",
                    },
                ],
                "attachments": ["https://example.com/doc"],
            },
        }


class TestDeleteEventEndpoint:
<<<<<<< HEAD
    """Tests for the delete event endpoint."""

    def test_deletes_event(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Delete an event and return confirmation."""
        monkeypatch.setattr(main_module, "get_client", fake_get_client)

=======
    def test_deletes_event(self) -> None:
>>>>>>> upstream/main
        response = client.delete("/events/test_123")

        assert response.status_code == HTTP_OK
        assert response.json() == {"status": "deleted"}
