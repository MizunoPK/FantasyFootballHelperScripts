"""
Tests for the CRN-paired A/B before/after comparator (T35: run_paired_ab_comparison).

These verify the helper's statistical contract on the REAL production seeding key
(_derive_task_seed, T29/T30) using a fast, deterministic Bernoulli win-model kernel — NOT the
multi-second full SimulatedLeague replay (which, in the default self-play regime, is ~0.50 by
symmetry and carries no constructible gap). The module's SimulatedLeague and SimDataLoader are
monkeypatched with fast fakes: SimDataLoader is always valid with an empty cache; the fake
league's get_draft_helper_results draws GAMES_PER_LEAGUE Bernoulli outcomes from
random.Random(seed), winning each when u < p, where p is the measured config's injected "_p".
Two arms sharing the per-task seed share every u (common random numbers).

Covers (mirrors the spec Test Strategy):
(a) Determinism — same fixed seed -> identical (current_rate, recommended_rate, delta, z, games).
(b) Identical-config -> zero delta (CRN: both arms see identical draws).
(c) Known-gap sign — a constructed skill gap yields a delta of the expected sign, both
    directions, with a finite pooled two-proportion z.
(d) Degenerate zero-SE guard — an all-wins pool yields z == 0.0.
(e) No live-config access — the helper never opens data/configs/league_config.json.

Author: Kai Mizuno
"""

# Standard library
import builtins
import random
from pathlib import Path

# Third-party
import pytest

# Local
import simulation.win_rate.paired_comparison as pac
from simulation.win_rate.paired_comparison import run_paired_ab_comparison


# FIXTURES

GAMES_PER_LEAGUE = 17  # a 17-week season -> 17 win/loss games per league (matches the engine)
SEED = 20260701


def _cfg(p: float) -> dict:
    """A minimal fake config carrying an injected win probability `_p` for the kernel."""
    return {"config_name": "fake", "description": "", "parameters": {}, "_p": p}


class _FakeLoader:
    """Stand-in for SimDataLoader: always valid, empty preloaded cache (no file I/O)."""

    def __init__(self, season_folder: Path) -> None:
        self.season_folder = season_folder
        self.is_valid = True
        self.week_data_cache = {}


class _FakeLeague:
    """Fast Bernoulli-kernel stand-in for SimulatedLeague (no draft/season replay, no I/O)."""

    def __init__(self, config_dict, data_folder, preloaded_week_data=None,
                 measured_config_dict=None, seed=None, naive_opponents=False):
        self._p = measured_config_dict["_p"]
        self._seed = seed

    def run_draft(self):
        pass

    def run_season(self):
        pass

    def get_draft_helper_results(self):
        rng = random.Random(self._seed)
        wins = sum(1 for _ in range(GAMES_PER_LEAGUE) if rng.random() < self._p)
        return wins, GAMES_PER_LEAGUE - wins, 0.0

    def cleanup(self):
        pass


@pytest.fixture
def fake_seasons(tmp_path, monkeypatch):
    """Create 3 empty season dirs (named 20XX for the real _derive_task_seed key) and patch
    the helper's SimulatedLeague + SimDataLoader with the fast fakes."""
    data_folder = tmp_path / "sim_data"
    for year in ("2021", "2022", "2023"):
        (data_folder / year).mkdir(parents=True)
    monkeypatch.setattr(pac, "SimulatedLeague", _FakeLeague)
    monkeypatch.setattr(pac, "SimDataLoader", _FakeLoader)
    return data_folder


class TestDeterminism:
    """(a) A fixed seed yields a byte-stable result across repeated calls."""

    def test_same_seed_gives_identical_result(self, fake_seasons):
        # Arrange / Act
        r1 = run_paired_ab_comparison(_cfg(0.50), _cfg(0.55), fake_seasons, seed=SEED)
        r2 = run_paired_ab_comparison(_cfg(0.50), _cfg(0.55), fake_seasons, seed=SEED)
        # Assert
        assert r1 == r2
        assert r1.seed == SEED
        assert r1.games == 3 * GAMES_PER_LEAGUE  # 3 seasons x 1 sim x 17 games


class TestIdenticalConfigZeroDelta:
    """(b) current == recommended -> exact zero delta under CRN (identical draws both arms)."""

    def test_identical_configs_yield_zero_delta(self, fake_seasons):
        result = run_paired_ab_comparison(_cfg(0.60), _cfg(0.60), fake_seasons, seed=SEED)
        assert result.current_rate == result.recommended_rate
        assert result.delta == 0.0


class TestKnownGapSign:
    """(c) A constructed gap yields a delta of the expected sign + a finite z, both directions."""

    def test_recommended_better_gives_positive_delta(self, fake_seasons):
        result = run_paired_ab_comparison(_cfg(0.40), _cfg(0.70), fake_seasons, seed=SEED)
        assert result.delta > 0.0
        assert result.z > 0.0
        import math
        assert math.isfinite(result.z)

    def test_recommended_worse_gives_negative_delta(self, fake_seasons):
        result = run_paired_ab_comparison(_cfg(0.70), _cfg(0.40), fake_seasons, seed=SEED)
        assert result.delta < 0.0
        assert result.z < 0.0


class TestDegenerateZeroSEGuard:
    """(d) An all-wins pool (p=1.0 both arms) -> pooled SE 0 -> z == 0.0 (no divide-by-zero)."""

    def test_all_wins_pool_yields_zero_z(self, fake_seasons):
        result = run_paired_ab_comparison(_cfg(1.0), _cfg(1.0), fake_seasons, seed=SEED)
        assert result.current_rate == 1.0
        assert result.recommended_rate == 1.0
        assert result.z == 0.0


class TestNoLiveConfigAccess:
    """(e) The helper never opens data/configs/league_config.json (D4 no-write / no-read-of-path)."""

    def test_helper_never_opens_live_config(self, fake_seasons, monkeypatch):
        # Arrange: record every path opened during the call.
        opened = []
        real_open = builtins.open

        def _tracking_open(file, *args, **kwargs):
            opened.append(str(file))
            return real_open(file, *args, **kwargs)

        monkeypatch.setattr(builtins, "open", _tracking_open)

        # Act
        run_paired_ab_comparison(_cfg(0.50), _cfg(0.55), fake_seasons, seed=SEED)

        # Assert: no opened path resolves to the live config.
        assert not any(
            p.replace("\\", "/").endswith("configs/league_config.json") for p in opened
        ), f"helper opened the live config path: {opened}"


class _FakeLoaderInvalid:
    """Stand-in for SimDataLoader: always INVALID — simulates a season that fails the player
    threshold check, so run_paired_ab_comparison skips it and accumulates zero games."""

    def __init__(self, season_folder: Path) -> None:
        self.season_folder = season_folder
        self.is_valid = False
        self.week_data_cache = {}


class TestZeroValidGames:
    """(f) When every season folder is invalid (all skipped), the helper raises ValueError
    instead of silently returning a degenerate zero-rate result."""

    def test_raises_when_all_seasons_invalid(self, tmp_path, monkeypatch):
        # Arrange: 3 season dirs, all invalid (FakeLoaderInvalid.is_valid = False).
        data_folder = tmp_path / "sim_data"
        for year in ("2021", "2022", "2023"):
            (data_folder / year).mkdir(parents=True)
        monkeypatch.setattr(pac, "SimulatedLeague", _FakeLeague)
        monkeypatch.setattr(pac, "SimDataLoader", _FakeLoaderInvalid)

        # Act / Assert: must raise ValueError, not return a zero-valued result.
        with pytest.raises(ValueError, match="no valid games evaluated"):
            run_paired_ab_comparison(_cfg(0.50), _cfg(0.55), data_folder, seed=SEED)
