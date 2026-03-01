"""Unit tests for google_calendar_client_impl.event_impl."""

import inspect
from datetime import UTC, datetime

import pytest
from calendar_client_api import Attendee, EventCreate
from google_calendar_client_impl.event_impl import GoogleCalendarEvent


class TestGoogleCalendarEventInitialization:
    """Test constructor-level source constraints."""

    def test_requires_exactly_one_of_payload_or_event_create(self) -> None:
        """Reject missing or ambiguous initialization sources."""
        payload = {
            "id": "evt_123",
            "start": {"dateTime": "2026-02-27T10:00:00Z"},
            "end": {"dateTime": "2026-02-27T11:00:00Z"},
        }
        event_create = EventCreate(
            title="Design Review",
            start_time=datetime(2026, 3, 2, 9, 0, tzinfo=UTC),
            end_time=datetime(2026, 3, 2, 10, 0, tzinfo=UTC),
            attendees=[],
            attachments=[],
        )

        with pytest.raises(ValueError, match="Exactly one of 'payload' or 'event_create'"):
            GoogleCalendarEvent()

        with pytest.raises(ValueError, match="Exactly one of 'payload' or 'event_create'"):
            GoogleCalendarEvent(payload=payload, event_create=event_create)

    def test_init_signature_hides_normalized_internal_fields(self) -> None:
        """Expose only payload/event_create constructor inputs."""
        parameters = inspect.signature(GoogleCalendarEvent.__init__).parameters
        assert list(parameters) == ["self", "payload", "event_create", "calendar_id"]


class TestGoogleCalendarEventFromGooglePayload:
    """Test parsing Google API payloads into GoogleCalendarEvent."""

    def test_parses_timed_event_fields(self) -> None:
        """Parse a full timed payload into all event properties."""
        payload = {
            "id": "evt_123",
            "summary": "Team Sync",
            "description": "Weekly status meeting",
            "location": "Room 301",
            "start": {"dateTime": "2026-02-27T10:00:00-05:00"},
            "end": {"dateTime": "2026-02-27T11:00:00-05:00"},
            "attendees": [
                {"email": "alice@example.com", "displayName": "Alice"},
                {"email": "bob@example.com"},
            ],
            "attachments": [
                {"fileUrl": "https://drive.google.com/file/d/abc"},
                {"title": "ignored-without-url"},
            ],
        }

        event = GoogleCalendarEvent(payload=payload, calendar_id="work")

        assert event.id == "evt_123"
        assert event.calendar_id == "work"
        assert event.title == "Team Sync"
        assert event.start_time == datetime.fromisoformat("2026-02-27T10:00:00-05:00")
        assert event.end_time == datetime.fromisoformat("2026-02-27T11:00:00-05:00")
        assert event.description == "Weekly status meeting"
        assert event.location == "Room 301"
        assert event.attendees == [
            Attendee(email="alice@example.com", name="Alice"),
            Attendee(email="bob@example.com", name=None),
        ]
        assert event.attachments == ["https://drive.google.com/file/d/abc"]

    def test_parses_all_day_event_as_utc_midnight(self) -> None:
        """Convert all-day date fields to midnight UTC datetimes."""
        payload = {
            "id": "evt_all_day",
            "summary": "Holiday",
            "start": {"date": "2026-12-25"},
            "end": {"date": "2026-12-26"},
        }

        event = GoogleCalendarEvent(payload=payload)

        assert event.start_time == datetime(2026, 12, 25, 0, 0, tzinfo=UTC)
        assert event.end_time == datetime(2026, 12, 26, 0, 0, tzinfo=UTC)

    def test_defaults_optional_fields_when_absent(self) -> None:
        """Default optional event fields to empty/None values."""
        payload = {
            "id": "evt_min",
            "start": {"dateTime": "2026-02-27T10:00:00Z"},
            "end": {"dateTime": "2026-02-27T11:00:00Z"},
        }

        event = GoogleCalendarEvent(payload=payload)

        assert event.title == ""
        assert event.description is None
        assert event.location is None
        assert event.attendees == []
        assert event.attachments == []

    def test_raises_when_required_id_is_missing(self) -> None:
        """Reject payloads that do not provide an event id."""
        payload = {
            "summary": "No id",
            "start": {"dateTime": "2026-02-27T10:00:00Z"},
            "end": {"dateTime": "2026-02-27T11:00:00Z"},
        }

        with pytest.raises(ValueError, match="non-empty 'id'"):
            GoogleCalendarEvent(payload=payload)

    def test_raises_when_start_and_end_missing(self) -> None:
        """Reject payloads that do not include required time objects."""
        payload = {"id": "evt_456", "summary": "Broken payload"}

        with pytest.raises(ValueError, match="'start' object"):
            GoogleCalendarEvent(payload=payload)


class TestGoogleCalendarEventFromEventCreate:
    """Test constructing GoogleCalendarEvent from EventCreate."""

    def test_builds_event_from_event_create(self) -> None:
        """Copy normalized fields from EventCreate into the event."""
        event_create = EventCreate(
            title="Design Review",
            start_time=datetime(2026, 3, 2, 9, 0, tzinfo=UTC),
            end_time=datetime(2026, 3, 2, 10, 0, tzinfo=UTC),
            attendees=[Attendee(email="designer@example.com", name="Designer")],
            attachments=["https://example.com/spec"],
            description="Review v2 flows",
            location="Zoom",
        )

        event = GoogleCalendarEvent(event_create=event_create, calendar_id="primary")

        assert event.id == ""
        assert event.calendar_id == "primary"
        assert event.title == "Design Review"
        assert event.start_time == datetime(2026, 3, 2, 9, 0, tzinfo=UTC)
        assert event.end_time == datetime(2026, 3, 2, 10, 0, tzinfo=UTC)
        assert event.description == "Review v2 flows"
        assert event.location == "Zoom"
        assert event.attendees == [Attendee(email="designer@example.com", name="Designer")]
        assert event.attachments == ["https://example.com/spec"]
