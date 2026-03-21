"""FastAPI service endpoints for the Google Calendar service component."""

from datetime import datetime
from typing import Annotated

import google_calendar_client_impl  # noqa: F401 Registers the concrete client via Dependency Injection
from calendar_client_api import get_client
from calendar_client_api.event import UNSET, Attendee, Event, EventCreate, EventUpdate
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(
    title="Google Calendar Service",
    version="0.1.0",
)


class AttendeeResponse(BaseModel):
    """Response model for an event attendee."""

    email: str
    name: str | None = None


class EventResponse(BaseModel):
    """Response model for a calendar event."""

    id: str
    title: str
    start_time: datetime
    end_time: datetime
    description: str | None = None
    location: str | None = None
    attendees: list[AttendeeResponse]
    attachments: list[str]


class EventEnvelope(BaseModel):
    """Response envelope for a single event."""

    event: EventResponse


class EventsEnvelope(BaseModel):
    """Response envelope for multiple events."""

    events: list[EventResponse]


class StatusResponse(BaseModel):
    """Response model for status messages."""

    status: str


def _to_attendee_response(attendee: Attendee) -> AttendeeResponse:
    """Convert an attendee domain model to a response DTO."""
    return AttendeeResponse(
        email=attendee.email,
        name=attendee.name,
    )


def _to_event_response(event: Event) -> EventResponse:
    """Convert an event domain model to a response DTO."""
    return EventResponse(
        id=event.id,
        title=event.title,
        start_time=event.start_time,
        end_time=event.end_time,
        description=event.description,
        location=event.location,
        attendees=[_to_attendee_response(attendee) for attendee in event.attendees],
        attachments=event.attachments,
    )


# Convert FastAPI request models into EventCreate/EventUpdate for the client interface.
class AttendeeRequest(BaseModel):
    """Request model for an event attendee."""

    email: str
    name: str | None = None


class EventCreateRequest(BaseModel):
    """Request model for creating an event."""

    title: str
    start_time: datetime
    end_time: datetime
    attendees: list[AttendeeRequest]
    attachments: list[str]
    description: str | None = None
    location: str | None = None

    def to_event_create(self) -> EventCreate:
        """Convert request data to EventCreate."""
        return EventCreate(
            title=self.title,
            start_time=self.start_time,
            end_time=self.end_time,
            attendees=[Attendee(email=attendee.email, name=attendee.name) for attendee in self.attendees],
            attachments=self.attachments,
            description=self.description,
            location=self.location,
        )


class EventUpdateRequest(BaseModel):
    """Request model for updating an event."""

    title: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    description: str | None = None
    location: str | None = None

    def to_event_update(self) -> EventUpdate:
        """Convert request data to EventUpdate."""
        return EventUpdate(
            title=self.title if self.title is not None else UNSET,
            start_time=self.start_time if self.start_time is not None else UNSET,
            end_time=self.end_time if self.end_time is not None else UNSET,
            description=self.description if self.description is not None else UNSET,
            location=self.location if self.location is not None else UNSET,
        )


@app.get("/health")
def health() -> StatusResponse:
    """Return service health status."""
    return StatusResponse(status="ok")


@app.get("/auth/login")
def login() -> dict[str, str]:
    """Start the OAuth login flow."""
    return {"message": "OAuth login not implemented yet"}


@app.get("/auth/callback")
def callback(code: Annotated[str | None, Query()] = None) -> dict[str, str]:
    """Handle the OAuth callback from the provider."""
    if code is None:
        return {"message": "Missing authorization code"}
    return {"message": "OAuth callback not implemented yet"}


@app.get("/events")
def list_events(max_results: Annotated[int, Query(ge=1)] = 10) -> EventsEnvelope:
    """List calendar events."""
    client = get_client()
    events = client.list_events(max_results=max_results)
    return EventsEnvelope(events=[_to_event_response(event) for event in events])


@app.get("/events/{event_id}")
def get_event(event_id: str) -> EventEnvelope:
    """Get a single calendar event by ID."""
    client = get_client()
    event = client.get_event(event_id)
    return EventEnvelope(event=_to_event_response(event))


@app.post("/events")
def create_event(event: EventCreateRequest) -> EventEnvelope:
    """Create a calendar event."""
    client = get_client()
    created_event = client.create_event(event.to_event_create())
    return EventEnvelope(event=_to_event_response(created_event))


@app.patch("/events/{event_id}")
def update_event(event_id: str, event: EventUpdateRequest) -> EventEnvelope:
    """Update a calendar event."""
    client = get_client()
    updated_event = client.update_event(event_id, event.to_event_update())
    return EventEnvelope(event=_to_event_response(updated_event))


@app.delete("/events/{event_id}")
def delete_event(event_id: str) -> StatusResponse:
    """Delete a calendar event."""
    client = get_client()
    client.delete_event(event_id)
    return StatusResponse(status="deleted")
