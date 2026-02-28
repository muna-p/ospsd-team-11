"""Google Calendar implementation of the CalendarClient interface."""

import logging
import os
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import ClassVar

import calendar_client_api
from calendar_client_api import CalendarClient, Event, EventCreate, EventUpdate
from google.auth.exceptions import GoogleAuthError, RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore[import-untyped]
from googleapiclient.discovery import Resource, build


class GoogleCalendarClient(CalendarClient):
    """Concrete implementation of CalendarClient using Google Calendar."""

    TOKEN_PATH: ClassVar[str] = os.getenv("GOOGLE_TOKEN_PATH", "token.json")
    CREDENTIALS_PATH: ClassVar[str] = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    SCOPES: ClassVar[list[str]] = [
        "https://www.googleapis.com/auth/calendar",
    ]

    def __init__(self, service: Resource | None = None, *, interactive: bool = True) -> None:
        """Initialize the Google calendar client."""
        self._default_calendar_id = os.getenv("DEFAULT_CALENDAR_ID", "primary")
        self.logger = logging.getLogger(__name__)
        if service is not None:
            self.service = service
            return

        creds_path = self.CREDENTIALS_PATH
        token_path = self.TOKEN_PATH

        creds: Credentials | None = self._auth_from_env()

        if not creds:
            creds = self._auth_from_file(token_path)

        if not creds and interactive:
            creds = self._auth_from_interactive(creds_path)

        creds = self._auth_refresh_token_if_invalid(creds)

        if not (creds and creds.valid):
            err_msg = "Failed to authenticate with Google Calendar API"
            raise RuntimeError(err_msg)

        # Save the credentials for the next run
        if creds and creds.valid and creds.refresh_token:
            with Path(token_path).open("w", encoding="utf-8") as file:
                file.write(creds.to_json()) # type: ignore[no-untyped-call]

        self.service = build("calendar", "v3", credentials=creds)

    def _auth_from_env(self) -> Credentials | None:
        client_id = os.environ.get("GOOGLE_CALENDAR_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CALENDAR_CLIENT_SECRET")
        refresh_token = os.environ.get("GOOGLE_CALENDAR_REFRESH_TOKEN")
        token_uri = os.environ.get(
            "GOOGLE_CALENDAR_TOKEN_URI", "https://oauth2.googleapis.com/token"
        )

        if not (client_id and client_secret and refresh_token):
            return None

        try:
            creds = Credentials(  # type: ignore[no-untyped-call]
                None,
                refresh_token=refresh_token,
                token_uri=token_uri,
                client_id=client_id,
                client_secret=client_secret,
                scopes=self.SCOPES,
            )
            creds.refresh(Request())
        except (GoogleAuthError, RefreshError, OSError, ValueError):
            return None
        else:
            return creds

    def _auth_from_interactive(self, creds_path: str) -> Credentials:
        if not Path(creds_path).exists():
            err_msg = f"'{creds_path}' not found. Cannot run interactive auth."
            raise FileNotFoundError(err_msg)
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.SCOPES)
        return flow.run_local_server(port=0) # type: ignore[no-any-return]

    def _auth_from_file(self, token_path: str) -> Credentials | None:
        # get the token (access&refresh token) from token.json if the file exists
        if not Path(token_path).exists():
            return None
        try:
            return Credentials.from_authorized_user_file(token_path, self.SCOPES)  # type: ignore[no-untyped-call,no-any-return]
        except (OSError, ValueError):
            return None

    def _auth_refresh_token_if_invalid(self, creds: Credentials | None) -> Credentials | None:
        if creds and not creds.valid and creds.refresh_token:
            try:
                creds.refresh(Request())
            except (GoogleAuthError, RefreshError, OSError, ValueError):
                return None
        return creds

    def create_event(self, event_create: EventCreate, calendar_id: str = "primary") -> Event:
        """Create a new calendar event and return its ID."""
        raise NotImplementedError

    def get_event(self, event_id: str, calendar_id: str = "primary") -> Event:
        """Retrieve a calendar event by its ID."""
        raise NotImplementedError

    def list_events(self, max_results: int = 10, calendar_id: str = "primary") -> Iterable[Event]:
        """Return an iterable of calendar events."""
        raise NotImplementedError

    def list_events_between(
        self, start: datetime, end: datetime, calendar_id: str = "primary"
    ) -> Iterable[Event]:
        """Return an iterable of calendar events between two dates."""
        raise NotImplementedError

    def update_event(
        self,
        event_id: str,
        event_patch: EventUpdate,
        calendar_id: str = "primary",
    ) -> Event:
        """Update an existing calendar event."""
        raise NotImplementedError

    def delete_event(self, event_id: str, calendar_id: str = "primary") -> None:
        """Delete a calendar event by its ID."""
        raise NotImplementedError


def load_env() -> None:
    """Load environment variables."""
    try:
        from dotenv import load_dotenv  # noqa: PLC0415

        load_dotenv()
    except ImportError:
        env_path = Path(".env")
        if env_path.exists():
            with env_path.open() as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()


def get_google_calendar_client() -> GoogleCalendarClient:
    """Get a Google Calendar client."""
    load_env()
    return GoogleCalendarClient()


def register_google_calendar_client() -> None:
    """Register a Google Calendar client."""
    calendar_client_api.register_client(get_google_calendar_client)
