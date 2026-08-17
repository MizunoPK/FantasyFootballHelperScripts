"""
ESPN Credentials

Environment-only credential loading and redaction helpers for ESPN's
authenticated draft-night API (D17). Provides an explicit, non-import-time
.env loader plus a single-owner credential read/validate function and a
redaction helper reused by callers' own error paths (D17.3).

Nothing in this module runs at import time -- callers invoke
load_espn_env() and get_espn_credentials() explicitly.

Author: Kai Mizuno
"""

import logging
import os
from typing import Tuple, Union
from pathlib import Path

from dotenv import load_dotenv

from utils.error_handler import ConfigurationError

REDACTION_MARKER = "***REDACTED***"


def load_espn_env(override: bool = False, dotenv_path: Union[str, Path, None] = None) -> None:
    """
    Load environment variables from a local .env file.

    This is the repository's first load_dotenv call site. It is a plain
    function with no side effects at import time -- a caller (this unit's
    own tests today, D17.3's startup path later) must invoke it explicitly.

    Args:
        override: When True, values from .env replace already-set process
            environment variables. Defaults to False so an operator-supplied
            process environment variable always wins over .env.
        dotenv_path: Optional path to a specific .env file. When None (default),
            load_dotenv() searches from the calling module's directory upward.
            Tests may pass an explicit path for hermetic behavior.
    """
    load_dotenv(dotenv_path=dotenv_path, override=override)


def get_espn_credentials() -> Tuple[str, str]:
    """
    Read and validate the ESPN session credentials from the process environment.

    Reads espn_s2 and SWID only via os.environ -- never a direct
    python-dotenv accessor, a CLI flag, or JSON config -- and is the single
    owner of validating both are present and non-blank. It is a plain
    function; nothing calls it at import time.

    Returns:
        Tuple[str, str]: (espn_s2, swid), each stripped of surrounding
            whitespace. Validation checks the stripped form, so the
            returned form matches what was validated -- a .env line with
            a trailing space (e.g. from a stray editor autosave) never
            hands a whitespace-padded cookie value to a caller.

    Raises:
        ConfigurationError: If either credential is missing or blank. The
            message names which credential(s) are absent and contains no
            credential value.
    """
    espn_s2 = os.environ.get('espn_s2', '').strip()
    swid = os.environ.get('SWID', '').strip()

    missing = []
    if not espn_s2:
        missing.append('espn_s2')
    if not swid:
        missing.append('SWID')

    if missing:
        raise ConfigurationError(
            f"Missing required ESPN credential(s): {', '.join(missing)}. "
            "Set them in the process environment or in a local .env file."
        )

    return espn_s2, swid


def redact(text: str, *secrets: str) -> str:
    """
    Replace every occurrence of each secret value in text with a fixed marker.

    Args:
        text: Arbitrary text that may contain one or more secret values.
        *secrets: One or more known secret values to redact.

    Returns:
        str: text with every occurrence of each non-empty secret replaced by
            REDACTION_MARKER. Empty/falsy secrets are skipped so an unset
            credential does not turn every empty substring into a match.
    """
    redacted = text
    for secret in secrets:
        if secret:
            redacted = redacted.replace(secret, REDACTION_MARKER)
    return redacted


class CredentialRedactionFilter(logging.Filter):
    """Global, process-wide `logging.Filter` scrubbing ESPN session credential
    values from every `LogRecord` it sees (D17.3 BLOCKING-3 remediation).

    Reads `espn_s2` / `SWID` directly from `os.environ` on every record --
    never captured once at install time -- so it redacts correctly whether
    the filter is installed before or after `load_espn_env()` populates the
    process environment, and it keeps working if credentials are rotated
    mid-process. A record logged while neither credential is set is passed
    through unchanged (`redact()` no-ops on falsy secrets).
    """

    def filter(self, record: logging.LogRecord) -> bool:
        espn_s2 = os.environ.get('espn_s2', '')
        swid = os.environ.get('SWID', '')
        if not espn_s2 and not swid:
            return True
        # Render args into the message first (record.getMessage() does this),
        # then redact the rendered text and clear args so downstream
        # formatters don't re-interpolate the original (unredacted) args.
        message = record.getMessage()
        redacted = redact(message, espn_s2, swid)
        if redacted != message:
            record.msg = redacted
            record.args = None
        return True


_credential_redaction_filter = CredentialRedactionFilter()
_credential_redaction_installed = False


def install_credential_redaction() -> None:
    """Install the global credential-redaction filter (D17.3 BLOCKING-3/(a)).

    Idempotent -- safe to call more than once (e.g. from multiple entry
    points) or with the filter already present.

    Installs on **both** the root logger and this project's shared logger
    (`utils.LoggingManager.get_logger()`). Root alone is not sufficient:
    `LoggingManager.setup_logger()` sets `logger.propagate = False` on the
    logger it configures, and a `logging.Filter` added to a `Logger` object
    (as opposed to a `Handler`) is consulted only by that logger's own
    `Logger.handle()` -- never by a descendant/propagating logger's records,
    and never inherited from an ancestor irrespective of `propagate`. So a
    filter added only to the root logger would silently never run for any
    record logged through the project's actual (non-propagating) logger --
    exactly the "logger sits outside the hierarchy" failure mode this
    installer must rule out. Installing directly on the project logger
    closes that gap; installing on root too is defense-in-depth for any
    logger that *does* propagate.

    Must be called before any credential-touching code runs (obligation (a)
    of the D17.3 review's remediation).
    """
    global _credential_redaction_installed
    if _credential_redaction_installed:
        return

    root_logger = logging.getLogger()
    if _credential_redaction_filter not in root_logger.filters:
        root_logger.addFilter(_credential_redaction_filter)

    from utils.LoggingManager import get_logger
    project_logger = get_logger()
    if _credential_redaction_filter not in project_logger.filters:
        project_logger.addFilter(_credential_redaction_filter)

    _credential_redaction_installed = True
