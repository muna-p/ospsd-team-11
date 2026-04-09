"""Public exports and auto-registration for the service calendar adapter."""

import os

import calendar_client_api

from google_calendar_service_adapter.client_adapter import ServiceCalendarClient as ServiceCalendarClient
from google_calendar_service_adapter.event_adapter import ServiceCalendarEvent as ServiceCalendarEvent


def register_service_calendar_client(base_url: str = "http://localhost:8000") -> None:
    """Register the ServiceCalendarClient with the calendar_client_api registry."""
    base_url = os.getenv("CALENDAR_SERVICE_BASE_URL", base_url)
    cookie_id = os.getenv("CALENDAR_COOKIE_ID", None)
    cookie_value = os.getenv("CALENDAR_COOKIE_VALUE", None)
    cookie = None
    if cookie_id is not None and cookie_value is not None:
        cookie = {cookie_id: cookie_value}
    calendar_client_api.register_client(lambda: ServiceCalendarClient(base_url=base_url, cookie=cookie))


register_service_calendar_client()
