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
