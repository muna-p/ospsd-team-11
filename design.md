# Design

## Overview

The project is split into two components:

- **`calendar_client_api`** — Abstract interface defining the contract for calendar operations.
- **`google_calendar_client_impl`** — Concrete implementation backed by the Google Calendar API.

## Why Two Components

The interface package has zero dependencies on Google libraries which mean that it will never depend on a specific provider. Swapping to a different calendar provider only requires a new implementation package.

## Dependency Injection

The DI pattern uses a simple registry in `calendar_client_api`:

- `register_client(factory)` stores a `Callable[[], CalendarClient]`.
- `get_client()` invokes and returns a new instance.

The implementation package auto registers itself at import time. When `google_calendar_client_impl` is imported, its `__init__.py` calls `register_client(get_google_calendar_client)`. After that, any call to `get_client()` returns a `GoogleCalendarClient`.

## Authentication

`GoogleCalendarClient` authenticates through a three-step chain, stopping at the first success:

1. **Environment variables** — `GOOGLE_CALENDAR_CLIENT_ID`, `GOOGLE_CALENDAR_CLIENT_SECRET`, `GOOGLE_CALENDAR_REFRESH_TOKEN`.
2. **Token file** — A previously saved `token.json` with OAuth credentials.
3. **Interactive OAuth** — Browser-based login using `credentials.json` (only when `interactive=True`).

No credentials are hardcoded. All secrets come from environment variables or files excluded from version control.

## Event Model

- `Event` (ABC) — Read only properties (`id`, `title`, `start_time`, `end_time`, `description`, `location`, `attendees`, `attachments`).
- `EventCreate` (dataclass) — DTO for creating events with all required fields.
- `EventUpdate` (dataclass) — DTO for partial updates.
- `GoogleCalendarEvent` — Concrete implementation that parses Google Calendar API payloads into the `Event` interface.
