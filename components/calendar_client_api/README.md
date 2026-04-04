# calendar_client_api

## Role

Defines the abstract interface and dependency injection registry for calendar operations. This package contains no concrete implementation and has zero external dependencies.

## Dependencies

None (Python stdlib only)

## Public API

| Export | Type | Description |
|--------|------|-------------|
| `CalendarClient` | ABC | Abstract base class with six methods: `create_event`, `get_event`, `list_events`, `list_events_between`, `update_event`, `delete_event` |
| `Event` | ABC | Abstract base class with properties: `id`, `title`, `start_time`, `end_time`, `description`, `location`, `attendees`, `attachments` |
| `EventCreate` | dataclass | DTO for creating events (title, start/end time, attendees, attachments, description, location) |
| `EventUpdate` | dataclass | DTO for partial updates using an `UNSET` sentinel to distinguish "not provided" from `None` |
| `Attendee` | dataclass | Value object representing an event attendee (email, optional name) |
| `register_client(factory)` | function | Registers a factory function `() -> CalendarClient` with the DI registry |
| `get_client()` | function | Returns a new `CalendarClient` instance from the registered factory. Raises `RuntimeError` if no factory is registered |
