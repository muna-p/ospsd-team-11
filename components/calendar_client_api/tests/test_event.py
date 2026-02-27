"""Unit tests for the calendar_client_api event module."""

from datetime import UTC, datetime
from unittest.mock import Mock

from calendar_client_api.event import (
    UNSET,
    Attendee,
    Event,
    EventCreate,
    EventUpdate,
)


def test_attendee_with_all_fields() -> None:
    """Test creating an Attendee with all fields."""
    attendee = Attendee(
        email="test@example.com",
        name="Test User",
    )

    assert attendee.email == "test@example.com"
    assert attendee.name == "Test User"


def test_attendee_without_optional_fields() -> None:
    """Test creating an Attendee without optional name field."""
    attendee = Attendee(email="another@example.com")

    assert attendee.email == "another@example.com"
    assert attendee.name is None


def test_event_abstract_properties() -> None:
    """Test that Event defines expected abstract properties."""
    expected_properties = {
        "id",
        "title",
        "start_time",
        "end_time",
        "description",
        "location",
        "attendees",
        "attachments",
    }
    assert Event.__abstractmethods__ == expected_properties


def test_event_comprehensive_mock() -> None:
    """Verifies all Event properties work together in a comprehensive test."""
    mock_event = Mock(spec=Event)
    mock_event.id = "event_123"
    mock_event.title = "Team Meeting"
    mock_event.start_time = datetime(2026, 1, 1, 10, 0, tzinfo=UTC)
    mock_event.end_time = datetime(2026, 1, 1, 11, 0, tzinfo=UTC)
    mock_event.description = "Quarterly planning meeting"
    mock_event.location = "Conference Room A"
    mock_event.attendees = [Attendee(email="alice@example.com")]
    mock_event.attachments = ["https://example.com/file.pdf"]

    properties = {
        "id": mock_event.id,
        "title": mock_event.title,
        "start_time": mock_event.start_time,
        "end_time": mock_event.end_time,
        "description": mock_event.description,
        "location": mock_event.location,
        "attendees": mock_event.attendees,
        "attachments": mock_event.attachments,
    }

    assert properties["id"] == "event_123"
    assert properties["title"] == "Team Meeting"
    assert properties["start_time"] == datetime(2026, 1, 1, 10, 0, tzinfo=UTC)
    assert properties["end_time"] == datetime(2026, 1, 1, 11, 0, tzinfo=UTC)
    assert properties["description"] == "Quarterly planning meeting"
    assert properties["location"] == "Conference Room A"
    assert len(properties["attendees"]) == 1
    assert properties["attendees"][0].email == "alice@example.com"
    assert len(properties["attachments"]) == 1


def test_event_create_with_all_fields() -> None:
    """Test creating an EventCreate with all fields."""
    start = datetime(2026, 1, 1, 10, 0, tzinfo=UTC)
    end = datetime(2026, 1, 1, 11, 0, tzinfo=UTC)
    attendees = [Attendee(email="test@example.com")]
    attachments = ["https://example.com/file.pdf"]

    event_create = EventCreate(
        title="Meeting",
        start_time=start,
        end_time=end,
        attendees=attendees,
        attachments=attachments,
        description="Important meeting",
        location="Conference Room A",
    )

    assert event_create.title == "Meeting"
    assert event_create.start_time == start
    assert event_create.end_time == end
    assert event_create.attendees == attendees
    assert event_create.attachments == attachments
    assert event_create.description == "Important meeting"
    assert event_create.location == "Conference Room A"


def test_event_create_without_optional_fields() -> None:
    """Test creating an EventCreate without optional fields."""
    start = datetime(2026, 1, 1, 10, 0, tzinfo=UTC)
    end = datetime(2026, 1, 1, 11, 0, tzinfo=UTC)

    event_create = EventCreate(
        title="Simple Meeting",
        start_time=start,
        end_time=end,
        attendees=[],
        attachments=[],
    )

    assert event_create.title == "Simple Meeting"
    assert event_create.description is None
    assert event_create.location is None


def test_unset_singleton_and_bool() -> None:
    """Test that UNSET evaluates to False."""
    assert not UNSET
    assert bool(UNSET) is False
    assert repr(UNSET) == "UNSET"


def test_event_update_with_all_fields() -> None:
    """Test creating an EventUpdate with all fields."""
    start = datetime(2026, 1, 1, 10, 0, tzinfo=UTC)
    end = datetime(2026, 1, 1, 11, 0, tzinfo=UTC)

    event_update = EventUpdate(
        title="Updated Meeting",
        start_time=start,
        end_time=end,
        description="Updated description",
        location="New Location",
    )

    assert event_update.title == "Updated Meeting"
    assert event_update.start_time == start
    assert event_update.end_time == end
    assert event_update.description == "Updated description"
    assert event_update.location == "New Location"


def test_event_update_with_no_fields() -> None:
    """Test creating an EventUpdate with no fields (all UNSET)."""
    event_update = EventUpdate()

    assert event_update.title is UNSET
    assert event_update.start_time is UNSET
    assert event_update.end_time is UNSET
    assert event_update.description is UNSET
    assert event_update.location is UNSET


def test_event_update_with_partial_fields() -> None:
    """Test creating an EventUpdate with only some fields set."""
    event_update = EventUpdate(
        title="New Title",
        description="New Description",
    )

    assert event_update.title == "New Title"
    assert event_update.description == "New Description"
    assert event_update.start_time is UNSET
    assert event_update.location is UNSET


def test_event_update_distinguishes_none_from_unset() -> None:
    """Test that EventUpdate can distinguish between None and UNSET."""
    event_update = EventUpdate(description=None)

    assert event_update.description is None
    assert event_update.description is not UNSET
    assert event_update.location is UNSET
    assert event_update.location is not None
    assert event_update.title is UNSET
    assert event_update.start_time is UNSET
    assert event_update.end_time is UNSET
