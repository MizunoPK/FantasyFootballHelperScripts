"""
Credential Redaction Primitives

Dependency-free home for the ESPN credential-redaction mechanism's core
pieces: the redaction marker, the `redact()` helper, and the
`CredentialRedactionFilter` logging.Filter itself (D17.3 review BLOCKING-6
remediation).

This module deliberately imports nothing from `utils` or
`player_data_fetcher` -- only the standard library (`logging`, `os`) -- so
that `utils.LoggingManager` can import it directly, at module top level,
with zero risk of a circular import. Before this module existed,
`LoggingManager._attach_credential_redaction` reached
`player_data_fetcher.espn_credentials` via a deferred import specifically to
avoid a cycle; that deferred import itself cycled back through
`utils.error_handler` into a still-initializing `utils.LoggingManager`,
which silently defeated the redaction filter's installation on the
`"default"` logger (BLOCKING-6). Relocating the filter here removes the
cycle -- and therefore the failure mode -- entirely, rather than reporting
it after the fact: there is no import to fail, so attachment is
structurally incapable of failing.

`player_data_fetcher.espn_credentials` re-exports `REDACTION_MARKER`,
`redact`, `CredentialRedactionFilter` and the shared filter singleton from
here for backward compatibility with any existing caller, and remains the
owner of `install_credential_redaction()` (which needs `utils.LoggingManager`
and is therefore still deferred-imported from that direction only).

Author: Kai Mizuno
"""

import logging
import os

REDACTION_MARKER = "***REDACTED***"


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

    `filter()` is wrapped in a broad `except Exception` (D17.3 review
    CONCERN-12): `record.getMessage()` performs `msg %% args` interpolation,
    which can raise on a mismatched placeholder or an argument whose
    `__str__` raises. In stock `logging`, that failure is caught inside
    `Handler.emit()` and routed to `Handler.handleError()` (a stderr notice,
    execution continues); performed inside a `Filter` it instead propagates
    out of `Logger.handle()` and raises at the log call site. This filter
    fails open on any such error -- a record that cannot be rendered cannot
    be scrubbed, and dropping or raising here is worse than deferring to the
    handler's own existing `handleError` path, which still runs because
    `filter()` returns True and lets the record reach the handler unredacted
    in that one edge case. This is the one place on the credential path
    where "fail open" is the loud-and-safe choice rather than a silent
    fallback: the alternative (crashing the caller's log statement) is worse
    for an application whose whole purpose is defensive, and the failure
    itself is neither swallowed nor hidden -- it still surfaces via the
    handler's `handleError()`, exactly as any other formatting defect would.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            espn_s2 = os.environ.get('espn_s2', '')
            swid = os.environ.get('SWID', '')
            if not espn_s2 and not swid:
                return True
            # Render args into the message first (record.getMessage() does
            # this), then redact the rendered text and clear args so
            # downstream formatters don't re-interpolate the original
            # (unredacted) args.
            message = record.getMessage()
            redacted = redact(message, espn_s2, swid)
            if redacted != message:
                record.msg = redacted
                record.args = None

            # D17.3 review CONCERN-9: the msg/args axis above does not cover
            # the exception axis. A Formatter appends the formatted
            # traceback from exc_info *after* filtering runs, so a
            # credential embedded anywhere in an exception chain (e.g. a raw
            # ESPN response body echoed by a third-party exception __str__)
            # would otherwise reach the log unredacted whenever a caller
            # logs with exc_info=True -- and this repo has two live
            # exc_info=True sinks on paths a fetcher failure reaches:
            # player_data_fetcher_main.py's top-level handler and
            # utils/error_handler.py's shared error handler. Pre-format
            # exc_info into record.exc_text (redacted) so the eventual
            # Formatter reuses it verbatim instead of re-formatting the
            # original.
            if record.exc_info:
                exc_text = record.exc_text or logging.Formatter().formatException(record.exc_info)
                redacted_exc_text = redact(exc_text, espn_s2, swid)
                if redacted_exc_text != exc_text:
                    record.exc_text = redacted_exc_text

            if record.stack_info:
                redacted_stack_info = redact(record.stack_info, espn_s2, swid)
                if redacted_stack_info != record.stack_info:
                    record.stack_info = redacted_stack_info
        except Exception:
            # Fail open on the filter itself, never on redaction: a record
            # this filter cannot even render cannot be scrubbed, and the
            # handler's own handleError() path (which this return lets run)
            # is the existing, correct place for that failure to surface.
            return True

        return True


# Module-level singleton, shared by `utils.LoggingManager` (attaches at
# handler-creation time) and `player_data_fetcher.espn_credentials`
# (attaches at install time via `install_credential_redaction()`) -- both
# import this same instance so `filter in handler.filters` membership checks
# agree regardless of which side attached it first.
credential_redaction_filter = CredentialRedactionFilter()
