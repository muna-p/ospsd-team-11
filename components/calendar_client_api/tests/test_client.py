"""Unit tests for the calendar_client_api client module.

Contains unit tests for the CalendarClient class and the get_client function.
"""

from typing import Any
from unittest.mock import Mock

import pytest

import calendar_client_api
import calendar_client_api.client
from calendar_client_api.client import CalendarClient
from calendar_client_api.registry import get_client


class TestCalendarClientABC:
    """Test cases for the CalendarClient abstract base class."""

    def test_cannot_instantiate_abstract_class(self) -> None:
        """Test that CalendarClient cannot be instantiated directly."""
        with pytest.raises(TypeError):
            CalendarClient()  # type: ignore[abstract]

    def test_defines_expected_abstract_methods(self) -> None:
        """Test that CalendarClient declares exactly the expected abstract methods."""
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
    """Test cases for the get_client dependency injection factory."""

    def test_raises_not_implemented_when_no_impl_registered(self) -> None:
        """Test that get_client raises NotImplementedError before any impl is injected."""
        original = calendar_client_api.registry.get_client
        calendar_client_api.registry.get_client = get_client

        try:
            with pytest.raises(NotImplementedError):
                calendar_client_api.registry.get_client()
        finally:
            calendar_client_api.registry.get_client = original

    def test_can_be_replaced_via_dependency_injection(self) -> None:
        """Test that get_client can be replaced by an implementation's factory."""
        original = calendar_client_api.registry.get_client
        mock_client = Mock(spec=CalendarClient)

        def fake_factory() -> Any:
            return mock_client

        calendar_client_api.registry.get_client = fake_factory  # type: ignore[assignment]

        try:
            result = calendar_client_api.registry.get_client()
            assert result is mock_client
        finally:
            calendar_client_api.registry.get_client = original

    def test_module_level_reexport_raises_not_implemented(self) -> None:
        """Test that the module-level re-export also raises NotImplementedError."""
        original = calendar_client_api.get_client
        calendar_client_api.get_client = get_client

        try:
            with pytest.raises(NotImplementedError):
                calendar_client_api.get_client()
        finally:
            calendar_client_api.get_client = original
