"""FastAPI service endpoints for the Google Calendar service component."""

<<<<<<< HEAD
from typing import Annotated

import google_calendar_client_impl  # noqa: F401 Registers the concrete client via Dependency Injection
from calendar_client_api import get_client
from fastapi import FastAPI, Query

from google_calendar_service.models import (
    EventCreateRequest,
    EventEnvelope,
    EventsEnvelope,
    EventUpdateRequest,
    StatusResponse,
    to_event_response,
)
=======
from __future__ import annotations

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from google_calendar_service.routes.auth_routes import router as auth_router
from google_calendar_service.routes.event_routes import router as event_router
from google_calendar_service.routes.health_routes import router as health_router
>>>>>>> upstream/main

app = FastAPI(
    title="Google Calendar Service",
    version="0.1.0",
)


<<<<<<< HEAD
@app.get("/health")
def health() -> StatusResponse:
    """Return service health status."""
    return StatusResponse(status="ok")


@app.get("/auth/login")
async def login() -> dict[str, str]:
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
    return EventsEnvelope(events=[to_event_response(event) for event in events])


@app.get("/events/{event_id}")
def get_event(event_id: str) -> EventEnvelope:
    """Get a single calendar event by ID."""
    client = get_client()
    event = client.get_event(event_id)
    return EventEnvelope(event=to_event_response(event))


@app.post("/events")
def create_event(event: EventCreateRequest) -> EventEnvelope:
    """Create a calendar event."""
    client = get_client()
    created_event = client.create_event(event.to_event_create())
    return EventEnvelope(event=to_event_response(created_event))


@app.patch("/events/{event_id}")
def update_event(event_id: str, event: EventUpdateRequest) -> EventEnvelope:
    """Update a calendar event."""
    client = get_client()
    updated_event = client.update_event(event_id, event.to_event_update())
    return EventEnvelope(event=to_event_response(updated_event))


@app.delete("/events/{event_id}")
def delete_event(event_id: str) -> StatusResponse:
    """Delete a calendar event."""
    client = get_client()
    client.delete_event(event_id)
    return StatusResponse(status="deleted")
=======
@app.get("/")
def root() -> RedirectResponse:
    """Redirect root endpoint to /docs."""
    return RedirectResponse(url="/docs")


app.include_router(auth_router)
app.include_router(health_router)
app.include_router(event_router)
>>>>>>> upstream/main
