# Google Calendar Event Implementation

`google_calendar_client_impl` includes a concrete `GoogleCalendarEvent` type that wraps raw Google Calendar event payloads and exposes the implementation-independent `Event` interface defined in `calendar_client_api.event`.

## What this component contains:

- **Concrete Event implementation**: `GoogleCalendarEvent`, which implements `calendar_client_api.event.Event`
- **Provider to contract adaptation**: logic for converting Google event payload fields (description, location, attendees, etc.) into the event interface shape

## The Concrete Event

::: google_calendar_client_impl.event_impl.GoogleCalendarEvent
    options:
      show_root_heading: true
      show_source: true