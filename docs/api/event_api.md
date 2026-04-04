# Event API

This page documents the event contract used by the Calendar Client system.

The goal is to define implementation-independent types that represent calendar events and event-related inputs. Concrete providers (e.g., Google Calendar) must convert their provider-specific data into objects that satisfy the `Event` abstract base class and use the shared datamodels for create/update operations.

## What this component contains

- **The event contract**: `Event`, representation of an event.
- **Data models**: `Attendee`, `EventCreate`, and `EventUpdate` used by `CalendarClient`.
- **Patch sentinel**: `UNSET`, a sentinel used to distinguish “no change” from explicit `None`.


## Event Contract

::: calendar_client_api.event.Event
    options:
      show_root_heading: true
      show_source: true

## Data Models

::: calendar_client_api.event.Attendee
    options:
      show_root_heading: true
      show_source: true

::: calendar_client_api.event.EventCreate
    options:
      show_root_heading: true
      show_source: true

::: calendar_client_api.event.EventUpdate
    options:
      show_root_heading: true
      show_source: true

## Patch Sentinel

`EventUpdate` supports partial updates. To avoid ambiguity between “field omitted” and “field cleared,” the API uses a sentinel.

::: calendar_client_api.event.UNSET
    options:
      show_root_heading: true
      show_source: true