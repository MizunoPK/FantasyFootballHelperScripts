#!/usr/bin/env python3
"""
Tests for the ESPN League Snapshot Seam (D18.4)

Covers the seam's own contract, one layer above `ESPNClient.get_league_snapshot()`'s
own tests in `test_espn_client.py`: synchronous delegation and offline corpus
resolution (AC), unmodified `ESPNAPIError` propagation (KD2), and the
`asyncio.run()` reentrance guard's two arms (KD4).

Author: Kai Mizuno
"""

import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from player_data_fetcher.espn_client import ESPNAPIError, ESPNClient
from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot
from player_data_fetcher.espn_league_snapshot_seam import get_league_snapshot_sync


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


class TestGetLeagueSnapshotSyncOfflineCorpus:
    """Offline, corpus-backed success path (AC: resolves from the committed corpus,
    no network access) -- this test also doubles as the KD4 normal-path (no
    running loop) regression check: it must keep passing unmodified once the
    reentrance guard is added.
    """

    def test_resolves_snapshot_from_committed_corpus_no_network(self, monkeypatch):
        # Arrange
        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(FIXTURES_DIR))
        monkeypatch.setenv("ESPN_DRAFT_FIXTURE_STEP", "0")
        monkeypatch.setenv("espn_s2", "offline-fixture-placeholder")
        monkeypatch.setenv("SWID", "{OFFLINE-FIXTURE-PLACEHOLDER}")

        # Act
        result = get_league_snapshot_sync(league_id=123, season=2026)

        # Assert
        assert isinstance(result, LeagueSnapshot)


class TestGetLeagueSnapshotSyncFailurePropagation:
    """KD2: a fixture-induced failure propagates as ESPNAPIError, unmodified,
    through the seam -- not caught, re-wrapped, or replaced. Mirrors the
    existing get_league_snapshot validation-failure test at
    tests/player_data_fetcher/test_espn_client.py:905
    (TestAuthenticatedLeagueSnapshot.test_get_league_snapshot_raises_on_invalid_payload).
    """

    def test_espnapi_error_propagates_unmodified_through_seam(self, monkeypatch):
        # Arrange -- same invalid-payload shape as the mirrored test:
        # draftDetail missing/wrong type fails LeagueSnapshot's pydantic
        # validation inside the real, unmocked get_league_snapshot().
        invalid_payload = {"draftDetail": None, "teams": []}
        monkeypatch.setattr(
            ESPNClient, "_get_raw_league_snapshot", AsyncMock(return_value=invalid_payload)
        )

        # Act / Assert -- ESPNAPIError specifically, not a bare Exception.
        with pytest.raises(ESPNAPIError, match="validation failed"):
            get_league_snapshot_sync(league_id=123, season=2026)


class TestGetLeagueSnapshotSyncReentranceGuard:
    """KD4 guard-path arm: called from a genuinely running event loop (not a
    mocked probe -- a mock would let a swallowed exception pass silently),
    the seam's own RuntimeError propagates out of the call uncaught.
    """

    @pytest.mark.asyncio
    async def test_guard_raises_when_called_from_running_event_loop(self):
        # Act / Assert -- called synchronously (not awaited) from inside this
        # already-running coroutine, so asyncio.get_running_loop() inside the
        # seam succeeds and the guard's `else` branch fires.
        with pytest.raises(RuntimeError, match="synchronous, non-async context"):
            get_league_snapshot_sync(league_id=123, season=2026)


class TestGetLeagueSnapshotSyncArgumentPassThrough:
    """CONCERN-2 guard: the seam delegates the caller's own `league_id` and
    `season` through unmodified. Without this assertion, dropping `season`,
    dropping `league_id`, or swapping the two would pass every other test in
    this file -- the offline-corpus test's fixture router keys on the URL shape
    and ESPN_DRAFT_FIXTURE_STEP, discarding the season's value, and the KD2 test
    asserts only on the raised exception. This is the test that makes
    `season`'s required-ness
    (spec_addendum1-required-season.md) load-bearing rather than decorative.
    """

    def test_delegates_league_id_and_season_unmodified(self, monkeypatch):
        # Arrange -- a real corpus payload so the call reaches a genuine
        # LeagueSnapshot instead of terminating on a validation error. The mock
        # sits one layer below the delegated ESPNClient.get_league_snapshot(),
        # so the assertion covers the whole
        # seam -> get_league_snapshot -> _get_raw_league_snapshot chain -- which
        # is exactly the chain whose tail resolves the stale Settings.season
        # fallback when `season` fails to arrive.
        raw_payload = json.loads(
            (FIXTURES_DIR / "espn_api" / "league_draft" / "step_000.json").read_text()
        )
        mock_raw = AsyncMock(return_value=raw_payload)
        monkeypatch.setattr(ESPNClient, "_get_raw_league_snapshot", mock_raw)

        # Act
        result = get_league_snapshot_sync(league_id=123, season=2026)

        # Assert -- both arguments arrive, in order, unmodified.
        mock_raw.assert_awaited_once_with(123, 2026)
        assert isinstance(result, LeagueSnapshot)
