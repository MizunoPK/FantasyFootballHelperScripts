"""
Tests for simulation.win_rate.SweepResultsManager.

Covers combo-key determinism, accumulate-on-update, best-win-rate tracking, record
contents, atomic write round-trip, absent/corrupt-file tolerance, and separation from
the single-axis store. Local-file persistence — exercised against tmp_path.

Author: Kai Mizuno
"""

# Standard library
import json

# Third-party
import pytest

# Local
from simulation.win_rate.SweepResultsManager import SweepResultsManager
from simulation.win_rate.param_value_generation import DRAFT_SWEEP_PARAMS


def _param_values(**overrides):
    base = {
        "SAME_POS_BYE_WEIGHT": 0.07,
        "DIFF_POS_BYE_WEIGHT": 0.01,
        "PRIMARY_BONUS": 67,
        "SECONDARY_BONUS": 69,
        "ADP_SCORING_WEIGHT": 4.76,
        "PLAYER_RATING_SCORING_WEIGHT": 3.52,
    }
    base.update(overrides)
    return base


@pytest.fixture
def results_path(tmp_path):
    return tmp_path / "win_rate_sweep_results.json"


class TestSweepResultsManager:
    """Tests for SweepResultsManager."""

    def test_make_combo_key_deterministic(self, results_path):
        mgr = SweepResultsManager(results_path)
        k1 = mgr.make_combo_key("1_zero_rb.json", _param_values())
        k2 = mgr.make_combo_key("1_zero_rb.json", _param_values())
        assert k1 == k2
        # All 6 params + strategy appear in the key.
        assert "1_zero_rb.json" in k1
        for p in DRAFT_SWEEP_PARAMS:
            assert p in k1

    def test_make_combo_key_differs_on_change(self, results_path):
        mgr = SweepResultsManager(results_path)
        base = mgr.make_combo_key("1_zero_rb.json", _param_values())
        assert mgr.make_combo_key("2_hero_rb.json", _param_values()) != base       # different strategy
        assert mgr.make_combo_key("1_zero_rb.json", _param_values(PRIMARY_BONUS=80)) != base  # different param

    def test_update_creates_and_accumulates(self, results_path):
        mgr = SweepResultsManager(results_path)
        pv = _param_values()
        mgr.update("1_zero_rb.json", pv, win_rate=0.6, wins=6, games=10)
        mgr.update("1_zero_rb.json", pv, win_rate=0.5, wins=5, games=10)
        key = mgr.make_combo_key("1_zero_rb.json", pv)
        entry = mgr.get_all_combinations()[key]
        assert entry["total_wins"] == 11
        assert entry["total_games"] == 20
        assert entry["total_runs"] == 2

    def test_update_tracks_best_single_run_win_rate(self, results_path):
        mgr = SweepResultsManager(results_path)
        pv = _param_values()
        mgr.update("1_zero_rb.json", pv, win_rate=0.6, wins=6, games=10)
        mgr.update("1_zero_rb.json", pv, win_rate=0.8, wins=8, games=10)
        mgr.update("1_zero_rb.json", pv, win_rate=0.7, wins=7, games=10)
        entry = mgr.get_all_combinations()[mgr.make_combo_key("1_zero_rb.json", pv)]
        assert entry["best_single_run_win_rate"] == 0.8

    def test_update_read_fallback_and_migrates_legacy_combination_key(self, results_path):
        # D4: an old-schema combination entry (legacy "best_win_rate", no new key) must be read
        # without KeyError and migrated on write — the legacy key is popped and the new
        # "best_single_run_win_rate" carries the (fallback-preserved) best.
        pv = _param_values()
        key = SweepResultsManager(results_path).make_combo_key("1_zero_rb.json", pv)
        old_schema = {
            "last_updated": "2026-06-01",
            "combinations": {
                key: {
                    "strategy_id": "1_zero_rb.json",
                    "param_values": pv,
                    "best_win_rate": 0.6,
                    "total_wins": 6,
                    "total_games": 10,
                    "total_runs": 1,
                    "last_run": "2026-06-01",
                }
            },
        }
        results_path.write_text(json.dumps(old_schema))
        mgr = SweepResultsManager(results_path)
        # A LOWER single-run rate must not lower the best; the fallback read of the legacy
        # key preserves 0.6, and the legacy key is popped (migrate-on-write).
        mgr.update("1_zero_rb.json", pv, win_rate=0.5, wins=5, games=10)
        entry = mgr.get_all_combinations()[key]
        assert entry["best_single_run_win_rate"] == 0.6
        assert "best_win_rate" not in entry
        # A HIGHER single-run rate raises the migrated best.
        mgr.update("1_zero_rb.json", pv, win_rate=0.9, wins=9, games=10)
        assert mgr.get_all_combinations()[key]["best_single_run_win_rate"] == 0.9

    def test_record_stores_strategy_and_params(self, results_path):
        mgr = SweepResultsManager(results_path)
        pv = _param_values()
        mgr.update("1_zero_rb.json", pv, win_rate=0.6, wins=6, games=10)
        entry = mgr.get_all_combinations()[mgr.make_combo_key("1_zero_rb.json", pv)]
        assert entry["strategy_id"] == "1_zero_rb.json"
        assert entry["param_values"] == pv

    def test_atomic_write_produces_valid_json(self, results_path):
        mgr = SweepResultsManager(results_path)
        pv = _param_values()
        mgr.update("1_zero_rb.json", pv, win_rate=0.6, wins=6, games=10)
        # File is valid JSON and reloads with the same record.
        with open(results_path) as f:
            data = json.load(f)
        assert "combinations" in data
        reloaded = SweepResultsManager(results_path)
        assert reloaded.get_all_combinations() == mgr.get_all_combinations()

    def test_load_absent_file_starts_fresh(self, results_path):
        mgr = SweepResultsManager(results_path)  # file does not exist yet
        assert mgr.get_all_combinations() == {}

    def test_get_combination_returns_recorded_entry(self, results_path):
        # get_combination returns the same entry get_all_combinations exposes for a key.
        mgr = SweepResultsManager(results_path)
        pv = _param_values()
        mgr.update("1_zero_rb.json", pv, win_rate=0.6, wins=6, games=10)
        entry = mgr.get_combination("1_zero_rb.json", pv)
        assert entry is not None
        assert entry["total_wins"] == 6
        assert entry["total_games"] == 10
        # Same object the full-map accessor returns for the combo key.
        key = mgr.make_combo_key("1_zero_rb.json", pv)
        assert entry is mgr.get_all_combinations()[key]

    def test_get_combination_absent_returns_none(self, results_path):
        # An unrecorded combination yields None (not a KeyError).
        mgr = SweepResultsManager(results_path)
        assert mgr.get_combination("1_zero_rb.json", _param_values()) is None

    def test_load_corrupt_file_starts_fresh(self, results_path):
        results_path.write_text("{ not valid json")
        mgr = SweepResultsManager(results_path)
        assert mgr.get_all_combinations() == {}

    def test_separate_from_single_axis_store(self, tmp_path):
        # The manager writes only its own results file, never win_rate_meta_data.json.
        results_path = tmp_path / "win_rate_sweep_results.json"
        meta_path = tmp_path / "win_rate_meta_data.json"
        mgr = SweepResultsManager(results_path)
        mgr.update("1_zero_rb.json", _param_values(), win_rate=0.6, wins=6, games=10)
        assert results_path.exists()
        assert not meta_path.exists()

    def test_set_get_discriminating_round_trip(self, results_path):
        """AC5: set_discriminating(True) -> get_discriminating() is True."""
        mgr = SweepResultsManager(results_path)
        mgr.set_discriminating(True)
        assert mgr.get_discriminating() is True

    def test_get_discriminating_defaults_false_when_absent(self, results_path):
        """AC3: fresh store (no set) returns False; legacy store without key also returns False."""
        mgr = SweepResultsManager(results_path)
        assert mgr.get_discriminating() is False

        # Also test a hand-written legacy store without the key.
        pv = _param_values()
        legacy_schema = {
            "last_updated": "2026-06-01",
            "combinations": {
                mgr.make_combo_key("1_zero_rb.json", pv): {
                    "strategy_id": "1_zero_rb.json",
                    "param_values": pv,
                    "best_single_run_win_rate": 0.6,
                    "total_wins": 6,
                    "total_games": 10,
                    "total_runs": 1,
                    "last_run": "2026-06-01",
                }
            },
        }
        results_path.write_text(json.dumps(legacy_schema))
        mgr2 = SweepResultsManager(results_path)
        assert mgr2.get_discriminating() is False

    def test_discriminating_persists_across_reload(self, results_path):
        """AC5: set_discriminating(True) -> reload -> get_discriminating() is True."""
        mgr = SweepResultsManager(results_path)
        mgr.set_discriminating(True)

        # Construct a new manager instance over the same path.
        mgr2 = SweepResultsManager(results_path)
        assert mgr2.get_discriminating() is True
