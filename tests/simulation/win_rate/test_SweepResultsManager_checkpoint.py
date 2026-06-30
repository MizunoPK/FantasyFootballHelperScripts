"""
Tests for the checkpoint / convergence surface of simulation.win_rate.SweepResultsManager.

Covers the input-fingerprint determinism + sensitivity (compute_input_fingerprint),
the per-config convergence upsert + status transition (mark_config_progress) and its
invalid-status rejection, the read accessors (get_config_convergence /
get_all_convergence / get_input_fingerprint), the derived all-complete state
(is_all_converged), atomic save/reload round-trips, and _load() tolerance of absent,
corrupt, and old-schema (combinations-only) files defaulting the two new keys.
Local-file persistence — exercised against tmp_path.

Author: Kai Mizuno
"""

# Standard library
import json

# Third-party
import pytest

# Local
from simulation.win_rate.SweepResultsManager import SweepResultsManager
from utils.error_handler import ConfigurationError


def _param_values(**overrides):
    base = {
        "DRAFT_NORMALIZATION_MAX_SCALE": 150,
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


class TestSweepResultsManagerCheckpoint:
    """Tests for the convergence / fingerprint checkpoint surface."""

    # --- compute_input_fingerprint: determinism + sensitivity ---
    # Signature (T31): (strategy_ids, baseline_params, num_values,
    #                   confidence, min_effect_size, min_games, base_seed).

    def test_fingerprint_deterministic_same_inputs(self):
        a = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json", "2_hero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        b = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json", "2_hero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        assert a == b

    def test_fingerprint_independent_of_strategy_id_order(self):
        a = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json", "2_hero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        b = SweepResultsManager.compute_input_fingerprint(
            ["2_hero_rb.json", "1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        assert a == b

    def test_fingerprint_sensitive_to_strategy_ids(self):
        base = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        changed = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json", "2_hero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        assert changed != base

    def test_fingerprint_sensitive_to_baseline_params(self):
        base = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        changed = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(PRIMARY_BONUS=80), 5, 0.95, 0.01, 30, 0
        )
        assert changed != base

    def test_fingerprint_sensitive_to_num_values(self):
        base = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        changed = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 7, 0.95, 0.01, 30, 0
        )
        assert changed != base

    def test_fingerprint_sensitive_to_confidence(self):
        base = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        changed = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.99, 0.01, 30, 0
        )
        assert changed != base

    def test_fingerprint_sensitive_to_min_effect_size(self):
        base = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        changed = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.02, 30, 0
        )
        assert changed != base

    def test_fingerprint_sensitive_to_min_games(self):
        base = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        changed = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 50, 0
        )
        assert changed != base

    def test_fingerprint_sensitive_to_base_seed(self):
        base = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        changed = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 99
        )
        assert changed != base

    # --- set/get input fingerprint round-trip ---

    def test_get_input_fingerprint_defaults_empty(self, results_path):
        mgr = SweepResultsManager(results_path)
        assert mgr.get_input_fingerprint() == ""

    def test_set_and_get_input_fingerprint_round_trip(self, results_path):
        mgr = SweepResultsManager(results_path)
        fp = SweepResultsManager.compute_input_fingerprint(
            ["1_zero_rb.json"], _param_values(), 5, 0.95, 0.01, 30, 0
        )
        mgr.set_input_fingerprint(fp)
        reloaded = SweepResultsManager(results_path)
        assert reloaded.get_input_fingerprint() == fp

    # --- mark_config_progress: upsert, transition, round-trip ---

    def test_mark_config_progress_creates_entry(self, results_path):
        mgr = SweepResultsManager(results_path)
        pv = _param_values()
        mgr.mark_config_progress("1_zero_rb.json", "in_progress", pv, 0.55)
        entry = mgr.get_config_convergence("1_zero_rb.json")
        assert entry is not None
        assert entry["status"] == "in_progress"
        assert entry["best_param_values"] == pv
        assert entry["best_win_rate"] == 0.55
        assert entry["updated"] != ""

    def test_mark_config_progress_upserts_status_transition(self, results_path):
        mgr = SweepResultsManager(results_path)
        mgr.mark_config_progress("1_zero_rb.json", "in_progress", _param_values(), 0.55)
        mgr.mark_config_progress(
            "1_zero_rb.json", "converged", _param_values(PRIMARY_BONUS=80), 0.61
        )
        entry = mgr.get_config_convergence("1_zero_rb.json")
        assert entry["status"] == "converged"
        assert entry["best_param_values"] == _param_values(PRIMARY_BONUS=80)
        assert entry["best_win_rate"] == 0.61
        # Upsert, not append: still exactly one entry for this id.
        assert list(mgr.get_all_convergence().keys()) == ["1_zero_rb.json"]

    def test_mark_config_progress_round_trip_through_reload(self, results_path):
        mgr = SweepResultsManager(results_path)
        pv = _param_values()
        mgr.mark_config_progress("1_zero_rb.json", "converged", pv, 0.6)
        mgr.mark_config_progress("2_hero_rb.json", "in_progress", pv, 0.5)
        reloaded = SweepResultsManager(results_path)
        assert reloaded.get_all_convergence() == mgr.get_all_convergence()
        assert reloaded.get_config_convergence("1_zero_rb.json")["status"] == "converged"

    def test_mark_config_progress_rejects_invalid_status(self, results_path):
        mgr = SweepResultsManager(results_path)
        with pytest.raises(ConfigurationError):
            mgr.mark_config_progress("1_zero_rb.json", "done", _param_values(), 0.6)
        # Nothing was written for the rejected call.
        assert mgr.get_config_convergence("1_zero_rb.json") is None

    def test_get_config_convergence_missing_returns_none(self, results_path):
        mgr = SweepResultsManager(results_path)
        assert mgr.get_config_convergence("nope.json") is None

    # --- is_all_converged: derived all-complete ---

    def test_is_all_converged_true_when_all_converged(self, results_path):
        mgr = SweepResultsManager(results_path)
        mgr.mark_config_progress("1_zero_rb.json", "converged", _param_values(), 0.6)
        mgr.mark_config_progress("2_hero_rb.json", "converged", _param_values(), 0.5)
        assert mgr.is_all_converged(["1_zero_rb.json", "2_hero_rb.json"]) is True

    def test_is_all_converged_false_when_one_in_progress(self, results_path):
        mgr = SweepResultsManager(results_path)
        mgr.mark_config_progress("1_zero_rb.json", "converged", _param_values(), 0.6)
        mgr.mark_config_progress("2_hero_rb.json", "in_progress", _param_values(), 0.5)
        assert mgr.is_all_converged(["1_zero_rb.json", "2_hero_rb.json"]) is False

    def test_is_all_converged_false_when_id_missing(self, results_path):
        mgr = SweepResultsManager(results_path)
        mgr.mark_config_progress("1_zero_rb.json", "converged", _param_values(), 0.6)
        assert mgr.is_all_converged(["1_zero_rb.json", "2_hero_rb.json"]) is False

    # --- _load() tolerance: absent, corrupt, old-schema ---

    def test_load_absent_file_defaults_new_keys(self, results_path):
        mgr = SweepResultsManager(results_path)  # file does not exist yet
        assert mgr.get_input_fingerprint() == ""
        assert mgr.get_all_convergence() == {}

    def test_load_corrupt_file_defaults_new_keys(self, results_path):
        results_path.write_text("{ not valid json")
        mgr = SweepResultsManager(results_path)
        assert mgr.get_input_fingerprint() == ""
        assert mgr.get_all_convergence() == {}

    def test_load_old_schema_file_defaults_new_keys_and_preserves_combinations(self, results_path):
        # An old-schema (combinations-only) file: no input_fingerprint, no convergence.
        old_schema = {
            "last_updated": "2026-06-01",
            "combinations": {
                "1_zero_rb.json|PRIMARY_BONUS=67": {
                    "strategy_id": "1_zero_rb.json",
                    "param_values": _param_values(),
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
        # New keys default cleanly.
        assert mgr.get_input_fingerprint() == ""
        assert mgr.get_all_convergence() == {}
        # Existing combinations survive untouched.
        assert mgr.get_all_combinations() == old_schema["combinations"]

    # --- last_updated metadata consistency (PR #17 review) ---

    def test_set_input_fingerprint_bumps_last_updated(self, results_path):
        SweepResultsManager(results_path).set_input_fingerprint("deadbeef")
        on_disk = json.loads(results_path.read_text())
        # A fingerprint-only write must refresh the file metadata, like update() does,
        # so the store never looks stale after a checkpoint-only persist.
        assert on_disk["last_updated"] != ""

    def test_mark_config_progress_bumps_last_updated(self, results_path):
        SweepResultsManager(results_path).mark_config_progress(
            "1_zero_rb.json", "in_progress", _param_values(), 0.55
        )
        on_disk = json.loads(results_path.read_text())
        assert on_disk["last_updated"] != ""

