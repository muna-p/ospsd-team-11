"""Unit tests for GoogleCalendarClient authentication flow (latest implementation)."""

from __future__ import annotations

from unittest.mock import MagicMock, Mock, patch

import pytest
from google.auth.exceptions import GoogleAuthError, RefreshError
from google.oauth2.credentials import Credentials
from google_calendar_client_impl.client_impl import GoogleCalendarClient


def _creds(*, valid: bool, refresh_token: str | None = "rt") -> Mock:  # noqa: S107
    c = Mock(spec=Credentials)
    c.valid = valid
    c.refresh_token = refresh_token
    c.to_json.return_value = '{"token":"x"}'
    return c


class TestAuthFromEnv:
    """Tests for GoogleCalendarClient._auth_from_env."""

    def test_returns_none_when_required_vars_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Return None when all three required env vars are absent."""
        monkeypatch.delenv("GOOGLE_CALENDAR_CLIENT_ID", raising=False)
        monkeypatch.delenv("GOOGLE_CALENDAR_CLIENT_SECRET", raising=False)
        monkeypatch.delenv("GOOGLE_CALENDAR_REFRESH_TOKEN", raising=False)

        client = GoogleCalendarClient(service=MagicMock())
        assert client._auth_from_env() is None

    def test_success_refresh_returns_creds(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Return Credentials when all env vars are set and refresh succeeds."""
        monkeypatch.setenv("GOOGLE_CALENDAR_CLIENT_ID", "id")
        monkeypatch.setenv("GOOGLE_CALENDAR_CLIENT_SECRET", "secret")
        monkeypatch.setenv("GOOGLE_CALENDAR_REFRESH_TOKEN", "rt")

        creds = _creds(valid=True)
        with (
            patch("google_calendar_client_impl.client_impl.Credentials", return_value=creds) as cls,
            patch("google_calendar_client_impl.client_impl.Request"),
        ):
            client = GoogleCalendarClient(service=MagicMock())
            out = client._auth_from_env()

        assert out is creds
        cls.assert_called_once()
        creds.refresh.assert_called_once()

    @pytest.mark.parametrize(
        "exc",
        [
            GoogleAuthError("bad"),  # type: ignore[no-untyped-call] # google-auth exception constructors are untyped
            RefreshError("expired"),  # type: ignore[no-untyped-call] # google-auth exception constructors are untyped
            OSError("network"),
            ValueError("bad"),
        ],
    )
    def test_refresh_failure_returns_none(
        self, monkeypatch: pytest.MonkeyPatch, exc: Exception
    ) -> None:
        """Return None for each exception type raised during token refresh."""
        monkeypatch.setenv("GOOGLE_CALENDAR_CLIENT_ID", "id")
        monkeypatch.setenv("GOOGLE_CALENDAR_CLIENT_SECRET", "secret")
        monkeypatch.setenv("GOOGLE_CALENDAR_REFRESH_TOKEN", "rt")

        creds = _creds(valid=False)
        creds.refresh.side_effect = exc

        with (
            patch("google_calendar_client_impl.client_impl.Credentials", return_value=creds),
            patch("google_calendar_client_impl.client_impl.Request"),
        ):
            client = GoogleCalendarClient(service=MagicMock())
            out = client._auth_from_env()

        assert out is None

    def test_uses_custom_token_uri(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Pass GOOGLE_CALENDAR_TOKEN_URI to Credentials when set."""
        monkeypatch.setenv("GOOGLE_CALENDAR_CLIENT_ID", "id")
        monkeypatch.setenv("GOOGLE_CALENDAR_CLIENT_SECRET", "secret")
        monkeypatch.setenv("GOOGLE_CALENDAR_REFRESH_TOKEN", "rt")
        monkeypatch.setenv("GOOGLE_CALENDAR_TOKEN_URI", "https://custom.example/token")

        creds = _creds(valid=True)
        with (
            patch("google_calendar_client_impl.client_impl.Credentials", return_value=creds) as cls,
            patch("google_calendar_client_impl.client_impl.Request"),
        ):
            client = GoogleCalendarClient(service=MagicMock())
            client._auth_from_env()

        # Credentials(...) is called with keyword args in the impl
        _, kwargs = cls.call_args
        assert kwargs["token_uri"] == "https://custom.example/token"


class TestAuthFromFile:
    """Tests for GoogleCalendarClient._auth_from_file."""

    def test_returns_none_when_file_missing(self) -> None:
        """Return None when the token file does not exist."""
        client = GoogleCalendarClient(service=MagicMock())
        with patch("google_calendar_client_impl.client_impl.Path.exists", return_value=False):
            assert client._auth_from_file("token.json") is None

    def test_returns_creds_when_parse_ok(self) -> None:
        """Return Credentials when the token file is present and parses cleanly."""
        client = GoogleCalendarClient(service=MagicMock())
        creds = _creds(valid=True)

        with (
            patch("google_calendar_client_impl.client_impl.Path.exists", return_value=True),
            patch(
                "google_calendar_client_impl.client_impl.Credentials.from_authorized_user_file",
                return_value=creds,
            ) as f,
        ):
            out = client._auth_from_file("token.json")

        assert out is creds
        f.assert_called_once_with("token.json", GoogleCalendarClient.SCOPES)

    @pytest.mark.parametrize("exc", [OSError("perm"), ValueError("bad")])
    def test_returns_none_on_parse_error(self, exc: Exception) -> None:
        """Return None when parsing the token file raises OSError or ValueError."""
        client = GoogleCalendarClient(service=MagicMock())

        with (
            patch("google_calendar_client_impl.client_impl.Path.exists", return_value=True),
            patch(
                "google_calendar_client_impl.client_impl.Credentials.from_authorized_user_file",
                side_effect=exc,
            ),
        ):
            out = client._auth_from_file("token.json")

        assert out is None


class TestAuthFromInteractive:
    """Tests for GoogleCalendarClient._auth_from_interactive."""

    def test_raises_when_credentials_file_missing(self) -> None:
        """Raise FileNotFoundError when the credentials file does not exist."""
        client = GoogleCalendarClient(service=MagicMock())

        with (
            patch("google_calendar_client_impl.client_impl.Path.exists", return_value=False),
            pytest.raises(FileNotFoundError, match="not found"),
        ):
            client._auth_from_interactive("credentials.json")

    def test_runs_local_server_when_credentials_exist(self) -> None:
        """Return Credentials from InstalledAppFlow.run_local_server when file exists."""
        client = GoogleCalendarClient(service=MagicMock())

        creds = _creds(valid=True)
        flow = Mock()
        flow.run_local_server.return_value = creds

        with (
            patch("google_calendar_client_impl.client_impl.Path.exists", return_value=True),
            patch(
                "google_calendar_client_impl.client_impl.InstalledAppFlow.from_client_secrets_file",
                return_value=flow,
            ) as from_file,
        ):
            out = client._auth_from_interactive("credentials.json")

        assert out is creds
        from_file.assert_called_once_with("credentials.json", GoogleCalendarClient.SCOPES)
        flow.run_local_server.assert_called_once_with(port=0)


class TestRefreshTokenIfInvalid:
    """Tests for GoogleCalendarClient._auth_refresh_token_if_invalid."""

    def test_returns_none_when_creds_none(self) -> None:
        """Return None when None is passed in."""
        client = GoogleCalendarClient(service=MagicMock())
        assert client._auth_refresh_token_if_invalid(None) is None

    def test_does_not_refresh_when_already_valid(self) -> None:
        """Return creds unchanged without calling refresh when already valid."""
        client = GoogleCalendarClient(service=MagicMock())
        creds = _creds(valid=True)

        out = client._auth_refresh_token_if_invalid(creds)

        assert out is creds
        creds.refresh.assert_not_called()

    def test_does_not_refresh_when_no_refresh_token(self) -> None:
        """Return creds unchanged when there is no refresh token to use."""
        client = GoogleCalendarClient(service=MagicMock())
        creds = _creds(valid=False, refresh_token=None)

        out = client._auth_refresh_token_if_invalid(creds)

        assert out is creds
        creds.refresh.assert_not_called()

    def test_refreshes_when_invalid_and_has_refresh_token(self) -> None:
        """Call creds.refresh when creds are invalid but a refresh token exists."""
        client = GoogleCalendarClient(service=MagicMock())
        creds = _creds(valid=False, refresh_token="rt")

        with patch("google_calendar_client_impl.client_impl.Request"):
            out = client._auth_refresh_token_if_invalid(creds)

        assert out is creds
        creds.refresh.assert_called_once()

    @pytest.mark.parametrize(
        "exc",
        [
            GoogleAuthError("bad"),  # type: ignore[no-untyped-call] # google-auth exception constructors are untyped
            RefreshError("expired"),  # type: ignore[no-untyped-call] # google-auth exception constructors are untyped
            OSError("net"),
            ValueError("bad"),
        ],
    )
    def test_returns_none_on_refresh_exception(self, exc: Exception) -> None:
        """Return None for each exception type raised during creds.refresh()."""
        client = GoogleCalendarClient(service=MagicMock())
        creds = _creds(valid=False, refresh_token="rt")
        creds.refresh.side_effect = exc

        with patch("google_calendar_client_impl.client_impl.Request"):
            out = client._auth_refresh_token_if_invalid(creds)

        assert out is None


class TestInitAuthFlow:
    """Tests for the __init__ authentication orchestration of GoogleCalendarClient."""

    def test_injected_service_skips_auth_and_build(self) -> None:
        """Skip auth entirely and not call build() when a service is injected."""
        svc = MagicMock()
        with patch("google_calendar_client_impl.client_impl.build") as b:
            client = GoogleCalendarClient(service=svc)

        assert client.service is svc
        b.assert_not_called()

    def test_env_success_short_circuits_file_and_interactive(self) -> None:
        """Not call _auth_from_file or _auth_from_interactive when env auth succeeds."""
        env_creds = _creds(valid=True, refresh_token="rt")

        with (
            patch.object(GoogleCalendarClient, "_auth_from_env", return_value=env_creds) as aenv,
            patch.object(GoogleCalendarClient, "_auth_from_file") as afile,
            patch.object(GoogleCalendarClient, "_auth_from_interactive") as aint,
            patch.object(
                GoogleCalendarClient, "_auth_refresh_token_if_invalid", return_value=env_creds
            ) as aref,
            patch("google_calendar_client_impl.client_impl.build") as b,
            patch("google_calendar_client_impl.client_impl.Path") as p,
        ):
            p.return_value.open.return_value.__enter__.return_value.write = Mock()
            b.return_value = MagicMock()

            client = GoogleCalendarClient(interactive=True)

        aenv.assert_called_once()
        afile.assert_not_called()
        aint.assert_not_called()
        aref.assert_called_once_with(env_creds)
        b.assert_called_once_with("calendar", "v3", credentials=env_creds)
        assert client.service is b.return_value

    def test_falls_back_to_file_when_env_missing(self) -> None:
        """Fall back to _auth_from_file when _auth_from_env returns None."""
        file_creds = _creds(valid=True, refresh_token="rt")

        with (
            patch.object(GoogleCalendarClient, "_auth_from_env", return_value=None),
            patch.object(GoogleCalendarClient, "_auth_from_file", return_value=file_creds) as afile,
            patch.object(GoogleCalendarClient, "_auth_from_interactive") as aint,
            patch.object(
                GoogleCalendarClient, "_auth_refresh_token_if_invalid", return_value=file_creds
            ),
            patch("google_calendar_client_impl.client_impl.build") as b,
            patch("google_calendar_client_impl.client_impl.Path") as p,
        ):
            p.return_value.open.return_value.__enter__.return_value.write = Mock()
            b.return_value = MagicMock()

            GoogleCalendarClient(interactive=True)

        afile.assert_called_once_with(GoogleCalendarClient.TOKEN_PATH)
        aint.assert_not_called()
        b.assert_called_once_with("calendar", "v3", credentials=file_creds)

    def test_interactive_is_last_resort_only_when_enabled(self) -> None:
        """Call _auth_from_interactive only when env and file auth both fail."""
        int_creds = _creds(valid=True, refresh_token="rt")

        with (
            patch.object(GoogleCalendarClient, "_auth_from_env", return_value=None),
            patch.object(GoogleCalendarClient, "_auth_from_file", return_value=None),
            patch.object(
                GoogleCalendarClient, "_auth_from_interactive", return_value=int_creds
            ) as aint,
            patch.object(
                GoogleCalendarClient, "_auth_refresh_token_if_invalid", return_value=int_creds
            ),
            patch("google_calendar_client_impl.client_impl.build") as b,
            patch("google_calendar_client_impl.client_impl.Path") as p,
        ):
            p.return_value.open.return_value.__enter__.return_value.write = Mock()
            b.return_value = MagicMock()

            GoogleCalendarClient(interactive=True)

        aint.assert_called_once_with(GoogleCalendarClient.CREDENTIALS_PATH)
        b.assert_called_once_with("calendar", "v3", credentials=int_creds)

    def test_does_not_call_interactive_when_disabled_and_raises(self) -> None:
        """Never call _auth_from_interactive and raise RuntimeError when interactive=False."""
        with (
            patch.object(GoogleCalendarClient, "_auth_from_env", return_value=None),
            patch.object(GoogleCalendarClient, "_auth_from_file", return_value=None),
            patch.object(GoogleCalendarClient, "_auth_from_interactive") as aint,
            patch.object(GoogleCalendarClient, "_auth_refresh_token_if_invalid", return_value=None),
            pytest.raises(RuntimeError, match="Failed to authenticate"),
        ):
            GoogleCalendarClient(interactive=False)

        aint.assert_not_called()

    def test_saves_token_only_when_refresh_token_present(self) -> None:
        """Write token.json to disk when credentials include a refresh token."""
        creds = _creds(valid=True, refresh_token="rt")

        fake_file = Mock()
        fake_open_cm = Mock()
        fake_open_cm.__enter__ = Mock(return_value=fake_file)
        fake_open_cm.__exit__ = Mock(return_value=None)

        with (
            patch.object(GoogleCalendarClient, "_auth_from_env", return_value=creds),
            patch.object(
                GoogleCalendarClient, "_auth_refresh_token_if_invalid", return_value=creds
            ),
            patch("google_calendar_client_impl.client_impl.Path") as p,
            patch("google_calendar_client_impl.client_impl.build", return_value=MagicMock()),
        ):
            p.return_value.open.return_value = fake_open_cm

            GoogleCalendarClient(interactive=False)

        p.return_value.open.assert_called_once_with("w", encoding="utf-8")
        fake_file.write.assert_called_once()  # wrote creds.to_json()

    def test_does_not_save_token_when_no_refresh_token(self) -> None:
        """Skip writing token.json when credentials have no refresh token."""
        creds = _creds(valid=True, refresh_token=None)

        with (
            patch.object(GoogleCalendarClient, "_auth_from_env", return_value=creds),
            patch.object(
                GoogleCalendarClient, "_auth_refresh_token_if_invalid", return_value=creds
            ),
            patch("google_calendar_client_impl.client_impl.Path") as p,
            patch("google_calendar_client_impl.client_impl.build", return_value=MagicMock()),
        ):
            GoogleCalendarClient(interactive=False)

        # Path is only called for token-saving; skipped when refresh_token is absent
        p.assert_not_called()
