"""Unit tests for the calendar_client_api client module.

Contains unit tests for the CalendarClient class and the get_client function.
"""

from typing import Any
from unittest.mock import Mock

import pytest

import calendar_client_api
import calendar_client_api.client
from calendar_client_api.client import CalendarClient, get_client


class TestCalendarClientABC:
    """Test cases for the CalendarClient abstract base class."""

    def test_cannot_instantiate_abstract_class(self) -> None:
        with pytest.raises(TypeError):
            CalendarClient()

    def test_defines_expected_abstract_methods(self) -> None:
        
        expected_methods = {
            "create_event",
            "get_event",
            "list_events",
            "update_event",
            "delete_event",
        }

        abstract_methods = CalendarClient.__abstractmethods__

        assert expected_methods == abstract_methods


class TestGetClient:

    def test_raises_not_implemented_when_no_impl_registered(self) -> None:

        original = calendar_client_api.client.get_client
        calendar_client_api.client.get_client = get_client

        try:
            with pytest.raises(NotImplementedError):
                calendar_client_api.client.get_client()
        finally:
            calendar_client_api.client.get_client = original

    def test_can_be_replaced_via_dependency_injection(self) -> None:

        original = calendar_client_api.client.get_client
        mock_client = Mock(spec=CalendarClient)

        def fake_factory() -> Any:
            return mock_client

        calendar_client_api.client.get_client = fake_factory

        try:
            result = calendar_client_api.client.get_client()
            assert result is mock_client
        finally:
            calendar_client_api.client.get_client = original

    def test_module_level_reexport_raises_not_implemented(self) -> None:

        original = calendar_client_api.get_client
        calendar_client_api.get_client = get_client

        try:
            with pytest.raises(NotImplementedError):
                calendar_client_api.get_client()
        finally:
            calendar_client_api.get_client = original