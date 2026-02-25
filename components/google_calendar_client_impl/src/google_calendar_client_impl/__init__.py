"""Public exports and dependency injections for the Google Calendar implementation package."""

from google_calendar_client_impl.client_impl import GoogleCalendarClient as GoogleCalendarClient
from google_calendar_client_impl.client_impl import (
    get_google_calendar_client as get_google_calendar_client,
)
from google_calendar_client_impl.client_impl import (
    register_google_calendar_client as _register_client,
)
from google_calendar_client_impl.event_impl import GoogleCalendarEvent as GoogleCalendarEvent
from google_calendar_client_impl.event_impl import (
    get_google_calendar_event as get_google_calendar_event,
)
from google_calendar_client_impl.event_impl import (
    register_google_calendar_event as _register_event,
)

_register_event()
_register_client()
