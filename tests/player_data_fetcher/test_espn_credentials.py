"""
Tests for player_data_fetcher.espn_credentials (D17.1)

Covers load_espn_env's non-overriding precedence, get_espn_credentials'
single-owner presence/blank validation and credential-free failure text, and
redact()'s sentinel replacement -- all offline, no network, no real
credentials.

Author: Kai Mizuno
"""

import os

import pytest

from player_data_fetcher.espn_credentials import (
    get_espn_credentials,
    load_espn_env,
    redact,
)
from utils.error_handler import ConfigurationError


@pytest.fixture(autouse=True)
def _clean_espn_env(monkeypatch):
    """espn_s2/SWID start unset for every test AND do not leak out of it.

    monkeypatch alone is insufficient here: load_espn_env() (via
    python-dotenv's load_dotenv) writes directly into the real os.environ,
    and monkeypatch only remembers names it *itself* deleted/set -- it
    cannot undo a write made underneath it by other code during the test.
    Without an explicit snapshot/restore, a value loaded by one test's
    load_espn_env() call survives into every later test in the same pytest
    session (CONCERN, review_2026-08-17T0933.md).
    """
    saved = {k: os.environ.get(k) for k in ('espn_s2', 'SWID')}
    monkeypatch.delenv('espn_s2', raising=False)
    monkeypatch.delenv('SWID', raising=False)
    yield
    for key, value in saved.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


class TestLoadEspnEnv:
    """load_espn_env(override=False) precedence and import-safety."""

    def test_does_not_override_existing_process_env(self, tmp_path, monkeypatch):
        """An already-set process env var wins over a .env value."""
        monkeypatch.setenv('espn_s2', 'PROCESS_VALUE')
        env_file = tmp_path / '.env'
        env_file.write_text('espn_s2=DOTENV_VALUE\nSWID=DOTENV_SWID\n')

        load_espn_env(override=False, dotenv_path=env_file)

        assert os.environ['espn_s2'] == 'PROCESS_VALUE'
        assert os.environ['SWID'] == 'DOTENV_SWID'

    def test_loads_dotenv_values_when_unset(self, tmp_path, monkeypatch):
        """With no process env var set, .env values are loaded."""
        env_file = tmp_path / '.env'
        env_file.write_text('espn_s2=DOTENV_VALUE\nSWID=DOTENV_SWID\n')

        load_espn_env(override=False, dotenv_path=env_file)

        assert os.environ['espn_s2'] == 'DOTENV_VALUE'
        assert os.environ['SWID'] == 'DOTENV_SWID'

    def test_import_alone_does_not_populate_environment(self, tmp_path, monkeypatch):
        """Merely importing the module must never read .env (UD3)."""
        env_file = tmp_path / '.env'
        env_file.write_text('espn_s2=SHOULD_NOT_LOAD\nSWID=SHOULD_NOT_LOAD\n')
        monkeypatch.chdir(tmp_path)

        import importlib

        import player_data_fetcher.espn_credentials as module
        importlib.reload(module)

        assert 'espn_s2' not in os.environ


class TestGetEspnCredentials:
    """get_espn_credentials' single-owner read + presence/blank validation."""

    def test_returns_both_credentials_when_present(self, monkeypatch):
        monkeypatch.setenv('espn_s2', 'REAL_S2')
        monkeypatch.setenv('SWID', 'REAL_SWID')

        espn_s2, swid = get_espn_credentials()

        assert espn_s2 == 'REAL_S2'
        assert swid == 'REAL_SWID'

    def test_raises_when_both_missing(self):
        with pytest.raises(ConfigurationError) as exc_info:
            get_espn_credentials()

        message = str(exc_info.value)
        assert 'espn_s2' in message
        assert 'SWID' in message

    def test_raises_when_espn_s2_blank(self, monkeypatch):
        monkeypatch.setenv('espn_s2', '   ')
        monkeypatch.setenv('SWID', 'REAL_SWID')

        with pytest.raises(ConfigurationError) as exc_info:
            get_espn_credentials()

        assert 'espn_s2' in str(exc_info.value)

    def test_raises_when_swid_missing(self, monkeypatch):
        monkeypatch.setenv('espn_s2', 'REAL_S2')

        with pytest.raises(ConfigurationError) as exc_info:
            get_espn_credentials()

        assert 'SWID' in str(exc_info.value)

    def test_failure_message_contains_no_credential_value(self, monkeypatch):
        """Loud failure, but the message never leaks a partially-set value."""
        monkeypatch.setenv('espn_s2', 'SENTINEL_S2_LEAK_CHECK')

        with pytest.raises(ConfigurationError) as exc_info:
            get_espn_credentials()

        assert 'SENTINEL_S2_LEAK_CHECK' not in str(exc_info.value)


class TestRedact:
    """redact()'s sentinel replacement, reused by D17.3's error path."""

    def test_replaces_single_secret(self):
        result = redact('token=SECRET123 end', 'SECRET123')
        assert 'SECRET123' not in result
        assert '***REDACTED***' in result

    def test_replaces_multiple_secrets(self):
        result = redact('a=ONE b=TWO', 'ONE', 'TWO')
        assert 'ONE' not in result
        assert 'TWO' not in result
        assert result.count('***REDACTED***') == 2

    def test_no_secrets_passed_leaves_text_unchanged(self):
        text = 'nothing to redact here'
        assert redact(text) == text

    def test_empty_secret_values_are_skipped(self):
        """A blank/unset secret must not turn every empty substring into a hit."""
        result = redact('unchanged', '', '')
        assert result == 'unchanged'


class TestCredentialRedactionFilterAttachment:
    """D17.3 review BLOCKING-6 regression: the filter must be present on the
    `"default"` logger's handlers after an entry-point-shaped
    `setup_logger("<other-name>")` call -- the exact ordering the original
    defect failed on (a circular deferred import inside
    `LoggingManager._attach_credential_redaction`, silently swallowed by a
    bare `except ImportError: return`, left the `"default"` logger's
    handlers -- built at `utils.LoggingManager` import time -- without the
    filter). The fix relocated `CredentialRedactionFilter` and its shared
    singleton to `utils.credential_redaction`, a module with zero project
    dependencies that `utils` can import directly, making the attachment
    structurally incapable of failing rather than merely less likely to.
    """

    def test_default_logger_handlers_carry_filter_after_other_entry_point_setup(self):
        import logging as _logging

        from utils.LoggingManager import setup_logger
        from utils.credential_redaction import credential_redaction_filter

        # Mimic a real entry point: configure a *different* named logger,
        # exactly as player_data_fetcher_main.py does.
        setup_logger("some_other_entry_point")

        default_logger = _logging.getLogger("default")
        assert default_logger.handlers, "expected the default logger to have been configured at import time"
        for handler in default_logger.handlers:
            assert credential_redaction_filter in handler.filters, (
                f"credential redaction filter missing from default logger handler {handler!r} "
                "-- this is the exact BLOCKING-6 regression"
            )


class TestCredentialRedactionFilterFailsOpen:
    """D17.3 review CONCERN-12: `CredentialRedactionFilter.filter()` must not
    raise at the log call site when a record's `%`-formatting is broken --
    that failure belongs to the handler's own `handleError()` path (as it
    would for any other formatting defect), not to the filter.
    """

    def test_broken_percent_formatting_does_not_raise_through_filter_when_credentials_set(self, monkeypatch):
        import logging as _logging

        from utils.credential_redaction import CredentialRedactionFilter

        monkeypatch.setenv("espn_s2", "some_sentinel_value")
        monkeypatch.setenv("SWID", "some_other_sentinel")

        class _BadArg:
            def __str__(self):
                raise RuntimeError("boom")

        record = _logging.LogRecord(
            name="test", level=_logging.INFO, pathname=__file__, lineno=1,
            msg="%s", args=(_BadArg(),), exc_info=None,
        )

        result = CredentialRedactionFilter().filter(record)
        assert result is True
