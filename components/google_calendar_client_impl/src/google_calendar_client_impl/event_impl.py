"""Google Calendar implementation of the Event interface."""

from collections.abc import Mapping
from datetime import UTC, date, datetime, time
from zoneinfo import ZoneInfo

from calendar_client_api import Attendee, Event, EventCreate


class GoogleCalendarEvent(Event):
    """Concrete implementation of the Event abstraction for Google Calendar."""

    def __init__(
        self,
        *,
        payload: Mapping[str, object] | None = None,
        event_create: EventCreate | None = None,
        calendar_id: str = "primary",
    ) -> None:
        """Initialize an event from exactly one source: payload or EventCreate."""
        if (payload is None) == (event_create is None):
            msg = "Exactly one of 'payload' or 'event_create' must be provided."
            raise ValueError(msg)

        self._calendar_id = calendar_id
        self._raw_payload: dict[str, object] | None = None

        if payload is not None:
            self._initialize_from_payload(payload)
            return

        if event_create is None:  # pragma: no cover - guarded by __init__ validation
            msg = "'event_create' must be provided."
            raise ValueError(msg)
        self._initialize_from_event_create(event_create)

    def _initialize_from_payload(self, payload: Mapping[str, object]) -> None:
        """Populate event fields from a Google Calendar event payload."""
        event_id = payload.get("id")
        if not isinstance(event_id, str) or not event_id:
            msg = "Google event payload must contain a non-empty 'id' string."
            raise ValueError(msg)

        title = payload.get("summary")
        description = payload.get("description")
        location = payload.get("location")

        start = payload.get("start")
        if start is None:
            msg = "Google event payload must contain a 'start' object."
            raise ValueError(msg)
        if not isinstance(start, Mapping):
            msg = "Google event payload 'start' must be an object."
            raise TypeError(msg)

        end = payload.get("end")
        if end is None:
            msg = "Google event payload must contain an 'end' object."
            raise ValueError(msg)
        if not isinstance(end, Mapping):
            msg = "Google event payload 'end' must be an object."
            raise TypeError(msg)

        self._event_id = event_id
        self._title = title if isinstance(title, str) else ""
        self._start_time = _parse_event_time(start, field_name="start")
        self._end_time = _parse_event_time(end, field_name="end")
        self._description = description if isinstance(description, str) else None
        self._location = location if isinstance(location, str) else None
        self._attendees = _parse_attendees(payload.get("attendees"))
        self._attachments = _parse_attachments(payload.get("attachments"))
        self._raw_payload = dict(payload)

    def _initialize_from_event_create(self, event_create: EventCreate) -> None:
        """Populate event fields from EventCreate data."""
        self._event_id = ""
        self._title = event_create.title
        self._start_time = event_create.start_time
        self._end_time = event_create.end_time
        self._description = event_create.description
        self._location = event_create.location
        self._attendees = list(event_create.attendees)
        self._attachments = list(event_create.attachments)
        self._raw_payload = None

    @property
    def calendar_id(self) -> str:
        """The calendar id of the event."""
        return self._calendar_id

    @property
    def id(self) -> str:
        """The id of the event."""
        return self._event_id

    @property
    def title(self) -> str:
        """The title of the event."""
        return self._title

    @property
    def start_time(self) -> datetime:
        """Returns the start datetime of the event."""
        return self._start_time

    @property
    def end_time(self) -> datetime:
        """Returns the end datetime of the event."""
        return self._end_time

    @property
    def description(self) -> str | None:
        """The description of the event."""
        return self._description

    @property
    def location(self) -> str | None:
        """The location of the event."""
        return self._location

    @property
    def attendees(self) -> list[Attendee]:
        """Returns the attendees of the event."""
        return list(self._attendees)

    @property
    def attachments(self) -> list[str]:
        """The attachments of the event."""
        return list(self._attachments)


def _parse_event_time(time_info: Mapping[str, object], field_name: str) -> datetime:
    """Parse Google event time objects with `dateTime` or all-day `date` fields."""
    date_time_value = time_info.get("dateTime")
    if isinstance(date_time_value, str):
        return _parse_datetime_value(date_time_value, time_info=time_info, field_name=field_name)

    date_value = time_info.get("date")
    if isinstance(date_value, str):
        try:
            all_day_date = date.fromisoformat(date_value)
        except ValueError as exc:
            msg = f"Invalid '{field_name}.date' value: {date_value!r}."
            raise ValueError(msg) from exc
        return datetime.combine(all_day_date, time.min, tzinfo=UTC)

    msg = f"Google event payload must contain '{field_name}.dateTime' or '{field_name}.date'."
    raise ValueError(msg)


def _parse_datetime_value(
    value: str,
    *,
    time_info: Mapping[str, object],
    field_name: str,
) -> datetime:
    """Parse a Google dateTime value and apply timezone defaults when needed."""
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        msg = f"Invalid '{field_name}.dateTime' value: {value!r}."
        raise ValueError(msg) from exc

    if parsed.tzinfo is not None:
        return parsed

    time_zone = time_info.get("timeZone")
    if isinstance(time_zone, str) and time_zone:
        return parsed.replace(tzinfo=ZoneInfo(time_zone))

    return parsed.replace(tzinfo=UTC)


def _parse_attendees(attendees_data: object) -> list[Attendee]:
    """Parse Google attendees into API attendees."""
    if not isinstance(attendees_data, list):
        return []

    attendees: list[Attendee] = []
    for attendee in attendees_data:
        if not isinstance(attendee, Mapping):
            continue

        email = attendee.get("email")
        if not isinstance(email, str) or not email:
            continue

        display_name = attendee.get("displayName")
        attendees.append(
            Attendee(
                email=email,
                name=display_name if isinstance(display_name, str) else None,
            )
        )
    return attendees


def _parse_attachments(attachments_data: object) -> list[str]:
    """Parse attachment URLs from Google attachments payload."""
    if not isinstance(attachments_data, list):
        return []

    attachments: list[str] = []
    for attachment in attachments_data:
        if not isinstance(attachment, Mapping):
            continue

        file_url = attachment.get("fileUrl")
        if isinstance(file_url, str) and file_url:
            attachments.append(file_url)
    return attachments
