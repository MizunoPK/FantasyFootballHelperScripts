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

    Unconditionally installs the global credential-redaction logging filter
    (`install_credential_redaction()`) as its first statement (D17.3 review
    BLOCKING-5). This deliberately broadens this function's role beyond
    D17.1 UD3's original charter ("sole owner of the os.environ read and the
    missing/blank validation") to also be the sole gate no caller can bypass
    to obtain credentials without redaction active -- an intentional,
    recorded reversal of the earlier decision to keep .env *loading*
    (`load_espn_env()`) out of this function for ownership clarity (see
    `addressed_feedback.md` Pass 1 item 1 and Pass 4's BLOCKING-5 disposition
    for the full reasoning: a security guarantee must not be caller-optional,
    while an environment-loading convenience may be). `install_credential_redaction()`
    is idempotent, so calling it here on every invocation is cheap and safe.

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
    install_credential_redaction()

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

        # D17.3 review CONCERN-9: the msg/args axis above does not cover the
        # exception axis. A Formatter appends the formatted traceback from
        # exc_info *after* filtering runs, so a credential embedded anywhere
        # in an exception chain (e.g. a raw ESPN response body echoed by a
        # third-party exception __str__) would otherwise reach the log
        # unredacted whenever a caller logs with exc_info=True -- and this
        # repo has two live exc_info=True sinks on paths a fetcher failure
        # reaches: player_data_fetcher_main.py's top-level handler and
        # utils/error_handler.py's shared error handler. Pre-format exc_info
        # into record.exc_text (redacted) so the eventual Formatter reuses it
        # verbatim instead of re-formatting the original.
        if record.exc_info:
            exc_text = record.exc_text or logging.Formatter().formatException(record.exc_info)
            redacted_exc_text = redact(exc_text, espn_s2, swid)
            if redacted_exc_text != exc_text:
                record.exc_text = redacted_exc_text

        if record.stack_info:
            redacted_stack_info = redact(record.stack_info, espn_s2, swid)
            if redacted_stack_info != record.stack_info:
                record.stack_info = redacted_stack_info

        return True


_credential_redaction_filter = CredentialRedactionFilter()
_credential_redaction_installed = False


def install_credential_redaction() -> None:
    """Install the global credential-redaction filter (D17.3 BLOCKING-3/BLOCKING-5).

    Idempotent -- safe to call more than once (e.g. from multiple entry
    points) or with the filter already present. Called unconditionally from
    `get_espn_credentials()` (D17.3 review BLOCKING-5's architect-decided
    remediation) so no caller can obtain ESPN credentials without redaction
    already active -- this is a structural guarantee of the credential-read
    contract, not a caller obligation to remember.

    Installs at two levels, because a `logging.Filter` on a `Logger` object
    and a `logging.Filter` on a `Handler` object are consulted in different
    circumstances and neither alone is sufficient:

    1. Directly on this project's shared logger
       (`utils.LoggingManager.get_logger()`). `LoggingManager.setup_logger()`
       sets `logger.propagate = False` on the logger it configures, and a
       `logging.Filter` added to a `Logger` (as opposed to a `Handler`) is
       consulted only by that logger's own `Logger.handle()` -- never by a
       descendant/propagating logger's records, and never inherited from an
       ancestor irrespective of `propagate`. Installing here covers every
       record actually logged through the project's own logger, cheaply
       (before any handler runs).
    2. Directly on every *existing* handler of the root logger and the
       project logger, at install time -- covers propagated records from
       any child logger reaching those handlers today (a logger-level
       filter on an ancestor is never consulted for a propagated record;
       only a handler-level filter is, per `Handler.handle()`).

    The ordering problem CONCERN-8 raised -- a handler attached *after*
    this function runs would miss the above two -- is closed at its actual
    source instead of by patching `logging.Logger.addHandler` process-wide:
    `utils.LoggingManager.setup_logger()` (the project's one handler-
    creation site, both the console `StreamHandler` and the file
    `LineBasedRotatingHandler`) attaches this same filter itself, at
    creation time, to every handler it builds -- including on a
    `setup_logger()` re-run, which clears and re-adds handlers. See
    `LoggingManager._attach_credential_redaction()`. An earlier version of
    this function instead monkeypatched `logging.Logger.addHandler`
    globally to make the coverage ordering-proof for *any* handler added
    anywhere in the process; that was reverted (D17.3 review, driver-
    verified blast radius) because it mutated stdlib behaviour process-wide
    and permanently for a benefit -- coverage of one project site plus
    arbitrary third-party handlers -- that a one-line addition at the
    actual creation site achieves without the hazard (it produced a
    demonstrated `RecursionError` under repeat/duplicate-import install).
    The residual obligation this narrower approach accepts: a *future
    second* project handler-creation site would need the same one-line
    call; see `addressed_feedback.md` D17.3 Pass 5 for the greppable check.

    Must be called before any credential-touching code runs. As of
    BLOCKING-5's remediation this is enforced structurally:
    `get_espn_credentials()` calls this function unconditionally as its
    first statement, so "before any credential-touching code runs" now
    reduces to "before `get_espn_credentials()` is ever called," which the
    process's own import/call order already guarantees.
    """
    global _credential_redaction_installed
    if _credential_redaction_installed:
        return

    root_logger = logging.getLogger()
    if _credential_redaction_filter not in root_logger.filters:
        root_logger.addFilter(_credential_redaction_filter)
    for handler in root_logger.handlers:
        if _credential_redaction_filter not in handler.filters:
            handler.addFilter(_credential_redaction_filter)

    from utils.LoggingManager import get_logger
    project_logger = get_logger()
    if _credential_redaction_filter not in project_logger.filters:
        project_logger.addFilter(_credential_redaction_filter)
    for handler in project_logger.handlers:
        if _credential_redaction_filter not in handler.filters:
            handler.addFilter(_credential_redaction_filter)

    _credential_redaction_installed = True
