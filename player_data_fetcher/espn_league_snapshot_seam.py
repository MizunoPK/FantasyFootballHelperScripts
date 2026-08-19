#!/usr/bin/env python3
"""
ESPN League Snapshot Seam

The League Helper's single, `player_data_fetcher`-owned route to the ESPN league
read (ticket D18 `TD1`, Option B). Wraps the async->sync bridge (`TD2`) around the
already-validated `ESPNClient.get_league_snapshot()` (D17.3), following the
throwaway-client lifecycle `generate_espn_draft_corpus.py`'s
`_capture_raw_payload()` already establishes for a one-shot `ESPNClient` caller.

D18.5 wired this seam into the League Helper's draft cockpit
(league_helper/draft_mode/DraftModeManager.py), which is now its sole production
caller. It is no longer callerless.

THREE NAMES ARE RE-EXPORTED HERE DELIBERATELY, not incidentally. TD1 forbids
`league_helper/` from importing `espn_client` or `espn_credentials` at all, so
anything the League Helper legitimately needs from either module must reach it
through this one surface -- for the call, its failure mode, AND the setup
preconditions the call cannot succeed without:

- `ESPNAPIError` -- the ONE exception a caller must handle.
- `missing_espn_credentials` -- the non-raising presence check a caller runs as a
  PRE-FLIGHT, before the cockpit is entered, so a credential gap is a setup notice
  rather than a `ConfigurationError` traceback from inside the fetch.
- `load_espn_env` -- the explicit, non-import-time `.env` loader a caller invokes
  before that pre-flight reads the environment. Without it the pre-flight (and the
  credential read below the seam) sees only the process environment, so credentials
  supplied the way this repository documents them are invisible.

All three are RE-EXPORTS, never reimplementations: `espn_credentials` remains the
single owner of the `.env` load, the `os.environ` read and the blank rule, so this
seam cannot disagree with the read it fronts. All three are listed in `__all__` so
they are not mistaken for -- or linted as -- unused imports; do not remove them.

Author: Kai Mizuno
"""

__all__ = [
    "ESPNAPIError",
    "get_league_snapshot_sync",
    "load_espn_env",
    "missing_espn_credentials",
]

import asyncio

from player_data_fetcher.espn_client import ESPNAPIError, ESPNClient
from player_data_fetcher.espn_credentials import (
    load_espn_env,
    missing_espn_credentials,
)
from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot
from player_data_fetcher.player_data_fetcher_main import Settings


def get_league_snapshot_sync(league_id: int, season: int) -> LeagueSnapshot:
    """Get the authenticated private-league snapshot synchronously (TD1, TD2).

    The League Helper's sole synchronous entry point into the ESPN league read.
    Delegates to `ESPNClient.get_league_snapshot()` unmodified, bridging its
    `async` call with `asyncio.run()` internally so no caller needs `asyncio`.

    Must be called from a synchronous, non-async context: no event loop may
    already be running in the calling thread (see Raises).

    Args:
        league_id: ESPN league ID.
        season: Season year to read (required). There is deliberately no default:
            omitting it would fall through to `Settings.season` in
            `player_data_fetcher_main.py`, a hard-coded literal, and silently
            read the wrong year.

    Returns:
        A validated `player_data_fetcher.espn_league_snapshot_models.LeagueSnapshot`.

    Raises:
        RuntimeError: If called from a context that already has a running event
            loop (e.g. from inside an `async def` coroutine) -- this function
            wraps `asyncio.run()` internally and cannot be nested inside one.
        ESPNAPIError: On non-success HTTP response, network failure, or snapshot
            validation failure, propagated unmodified from the delegated
            `ESPNClient.get_league_snapshot()` call (credential-safe; see its own
            docstring).
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # No loop running -- the normal, correctly-contexted case. This
        # RuntimeError is the probe's own detection artifact, not the seam's
        # failure signal; it is fully contained here and never reaches the
        # caller.
        pass
    else:
        # A loop IS already running: raise the seam's OWN RuntimeError, in the
        # `else` clause -- outside the `except RuntimeError` handler above --
        # so it can never be caught by the same handler that contains the
        # probe's artifact. Do not merge this into a single try/except around
        # both the probe and this raise; that would swallow this error too.
        raise RuntimeError(
            "get_league_snapshot_sync() must be called from a synchronous, "
            "non-async context: no event loop may already be running. It wraps "
            "asyncio.run() internally and cannot be invoked from inside an "
            "async def coroutine or any other context with a running event loop."
        )

    return asyncio.run(_fetch_league_snapshot(league_id, season))


async def _fetch_league_snapshot(league_id: int, season: int) -> LeagueSnapshot:
    """Construct a throwaway `ESPNClient`, fetch the snapshot, and close it.

    Mirrors the throwaway-client lifecycle `generate_espn_draft_corpus.py`'s
    `_capture_raw_payload()` already establishes (KD3): construct
    `Settings`/`ESPNClient`, enter `client.session()`, call the target method,
    `client.close()` in a `finally` -- no client is cached or reused across calls.

    Args:
        league_id: ESPN league ID.
        season: Season year, passed through unmodified.

    Returns:
        The delegated call's validated `LeagueSnapshot`.
    """
    settings = Settings()
    client = ESPNClient(settings)
    try:
        async with client.session():
            return await client.get_league_snapshot(league_id, season)
    finally:
        await client.close()
