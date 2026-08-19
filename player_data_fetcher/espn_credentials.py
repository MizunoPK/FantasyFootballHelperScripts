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
from typing import List, Tuple, Union
from pathlib import Path

from dotenv import load_dotenv

from utils.error_handler import ConfigurationError
from utils.credential_redaction import (
    REDACTION_MARKER,
    CredentialRedactionFilter,
    credential_redaction_filter as _credential_redaction_filter,
    redact,
)

__all__ = [
    "load_espn_env",
    "get_espn_credentials",
    "missing_espn_credentials",
    "redact",
    "REDACTION_MARKER",
    "CredentialRedactionFilter",
    "install_credential_redaction",
]


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

    missing = missing_espn_credentials()

    if missing:
        raise ConfigurationError(
            f"Missing required ESPN credential(s): {', '.join(missing)}. "
            "Set them in the process environment or in a local .env file."
        )

    return espn_s2, swid


def missing_espn_credentials() -> List[str]:
    """
    Report which ESPN credentials are absent or blank, WITHOUT raising.

    The non-raising half of this module's single-owner validation:
    `get_espn_credentials()` calls it and turns a non-empty result into its
    ConfigurationError, so the presence/blank rule lives in exactly one
    place. It exists for callers that must PRE-FLIGHT the credential state
    rather than consume it -- notably Draft Mode, which has to decide
    whether the live cockpit can be entered at all and must render a setup
    notice instead of letting a ConfigurationError escape mid-session
    (D18.5 polish, user test plan scenario 7).

    Reads the same `os.environ` keys, with the same `.strip()` blank rule,
    as `get_espn_credentials()`, so a pre-flight can never disagree with
    the read that follows it.

    Args:
        None.

    Returns:
        List[str]: The names of the missing/blank credentials, in the fixed
            order ('espn_s2', 'SWID'). Empty when both are usable. NAMES
            ONLY -- no credential VALUE is returned, logged or printed,
            here or by any caller.
    """
    return [
        name
        for name in ('espn_s2', 'SWID')
        if not os.environ.get(name, '').strip()
    ]


# `redact`, `CredentialRedactionFilter` and the shared filter singleton
# (imported above as `_credential_redaction_filter`) now live in
# `utils.credential_redaction` -- a dependency-free module `utils` can
# import directly at module top level, which is what makes
# `LoggingManager._attach_credential_redaction`'s attachment structurally
# incapable of failing (D17.3 review BLOCKING-6). They are re-exported here
# (see `__all__` above and the module docstring) for backward compatibility
# with any existing `from player_data_fetcher.espn_credentials import ...`
# caller; this module is no longer their defining owner.

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

    This narrower approach's residual obligation was originally recorded as
    "a *future second* project handler-creation site would need the same
    one-line call" -- which was incomplete (D17.3 review CONCERN-13): it
    implied the *existing* site was already fully covered, when in fact the
    `"default"` logger built by `LoggingManager.__init__` at
    `utils.LoggingManager` import time was silently missing the filter
    (BLOCKING-6), because the old deferred import from
    `_attach_credential_redaction` back into this module cycled and its
    `ImportError` was swallowed. That cycle is now removed structurally
    (`CredentialRedactionFilter` and the shared filter singleton live in
    `utils.credential_redaction`, which `utils` imports directly with no
    cycle possible), so the *first* handler-creation site's attachment can
    no longer silently fail. The residual obligation that remains is
    unchanged in kind: a *future second* project handler-creation site
    (an `addHandler(...)`/`StreamHandler(` call outside `tests/`) would
    still need the same call at its own creation site; see
    `addressed_feedback.md` D17.3 for the greppable check.

    D17.3 review CONCERN-20: this function's install additionally attaches
    the filter to `logging.lastResort` (chosen alternative (a) + the
    `lastResort` line from (b) -- see `addressed_feedback.md` D17.3 Pass 7).
    `logging.lastResort` is what stdlib falls back to for a WARNING+ record
    on a logger with no handler anywhere in its propagation chain (the
    exact situation of a bare `logging.getLogger(__name__)` module, e.g.
    `utils/csv_utils.py`, which has 0 own handlers and a root logger with 0
    handlers). Attaching there closes that gap for every present and future
    bare-logger module in one line, without a per-module opt-in.

    **Known residual, deliberately left open and recorded rather than
    silently assumed closed (CONCERN-20's "known residual"):** the two
    `for handler in ...logger.handlers:` loops below still enumerate root
    and project logger handlers point-in-time, at install call. A handler
    added to either logger *after* `install_credential_redaction()` runs
    would still miss the filter (the same species of ordering gap CONCERN-8
    closed at `LoggingManager`'s own creation site, but not re-derived
    here). This is NOT closed by the `lastResort` attachment above --
    `lastResort` only fires when a record reaches no handler at all, so a
    handler added post-install and never wired to `LoggingManager`'s
    creation-time attachment is a distinct gap. Closing it fully would mean
    either re-deriving the ordering-proof pattern here (previously rejected
    on this ticket, CONCERN-8's own history above, as a stdlib-mutating
    monkeypatch with a demonstrated `RecursionError` hazard) or restricting
    every project handler-creation path to go through `LoggingManager`
    (true today per the grep in `addressed_feedback.md`, but not structurally
    enforced). Accepted bound: the residual can only be exploited by new
    handler-creation code added *outside* `LoggingManager` *after* process
    start and *before* an explicit re-`install_credential_redaction()` call
    -- there is no such code today (verified by the same grep CONCERN-20
    cites), so the gap is latent, not live.

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

    # D17.3 review CONCERN-20: covers any bare `logging.getLogger(__name__)`
    # module with no handler anywhere in its propagation chain (e.g.
    # utils/csv_utils.py) -- stdlib routes such a WARNING+ record to
    # logging.lastResort, which had no filter before this line.
    if _credential_redaction_filter not in logging.lastResort.filters:
        logging.lastResort.addFilter(_credential_redaction_filter)

    _credential_redaction_installed = True
