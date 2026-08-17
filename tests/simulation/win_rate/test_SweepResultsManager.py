"""
Tests for simulation.win_rate.SweepResultsManager.

Covers combo-key determinism, accumulate-on-update, best-win-rate tracking, record
contents, atomic write round-trip, absent/corrupt-file tolerance, and separation from
the single-axis store. Local-file persistence — exercised against tmp_path.

Author: Kai Mizuno
"""

# Standard library
import json
from unittest.mock import MagicMock, patch

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
        # T68/D1: both updates had no incumbent -> the self_play bucket; totals are the derived sum.
        assert entry["by_reference"]["self_play"] == {"wins": 11, "games": 20}
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
                    "by_reference": {"self_play": {"wins": 6, "games": 10}},
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
        assert entry["by_reference"] == {"self_play": {"wins": 6, "games": 10}}

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
                    "by_reference": {"self_play": {"wins": 6, "games": 10}},
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


class TestReferenceBucketing:
    """T68/D1 + AC6: evaluations against different references never merge into one rate."""

    def test_make_reference_key_self_play_and_value_tail(self, results_path):
        pv = _param_values()
        assert SweepResultsManager.make_reference_key(None) == "self_play"
        key = SweepResultsManager.make_reference_key(pv)
        # NAME=value tail over DRAFT_SWEEP_PARAMS order, no strategy_id prefix.
        assert key == "|".join(f"{p}={pv[p]}" for p in DRAFT_SWEEP_PARAMS)
        assert "self_play" != key

    def test_heterogeneous_references_are_not_merged(self, results_path):
        # AC6 (the load-bearing correctness test): three evals of ONE combo against three
        # references (self-play, incumbent A, incumbent B) land in three distinct buckets and are
        # NEVER pooled into a single rate. FAILS on pre-fix main (no by_reference); passes now.
        mgr = SweepResultsManager(results_path)
        trial = _param_values()
        incumbent_a = _param_values(PRIMARY_BONUS=80)
        incumbent_b = _param_values(PRIMARY_BONUS=90)
        mgr.update("1_zero_rb.json", trial, win_rate=0.5, wins=50, games=100)  # self_play (None)
        mgr.update("1_zero_rb.json", trial, win_rate=0.6, wins=60, games=100,
                   incumbent_param_values=incumbent_a)
        mgr.update("1_zero_rb.json", trial, win_rate=0.7, wins=70, games=100,
                   incumbent_param_values=incumbent_b)
        entry = mgr.get_combination("1_zero_rb.json", trial)
        by_ref = entry["by_reference"]
        key_a = SweepResultsManager.make_reference_key(incumbent_a)
        key_b = SweepResultsManager.make_reference_key(incumbent_b)
        assert set(by_ref) == {"self_play", key_a, key_b}
        assert by_ref["self_play"] == {"wins": 50, "games": 100}
        assert by_ref[key_a] == {"wins": 60, "games": 100}
        assert by_ref[key_b] == {"wins": 70, "games": 100}
        # Derived cross-bucket totals are the SUM, never a single merged rate.
        assert entry["total_wins"] == 180
        assert entry["total_games"] == 300

    def test_same_reference_accumulates_in_one_bucket(self, results_path):
        mgr = SweepResultsManager(results_path)
        trial = _param_values()
        incumbent = _param_values(PRIMARY_BONUS=80)
        mgr.update("1_zero_rb.json", trial, 0.6, 60, 100, incumbent_param_values=incumbent)
        mgr.update("1_zero_rb.json", trial, 0.5, 50, 100, incumbent_param_values=incumbent)
        by_ref = mgr.get_combination("1_zero_rb.json", trial)["by_reference"]
        assert by_ref[SweepResultsManager.make_reference_key(incumbent)] == {"wins": 110, "games": 200}
        assert "self_play" not in by_ref


class TestQuarantineAndRestart:
    """T68/D3 + AC5: a pre-fix store is quarantined (renamed, never destroyed) and restarts empty;
    an empty/fresh store is never quarantined."""

    def _prefix_store(self, results_path):
        pv = _param_values()
        key = SweepResultsManager(results_path).make_combo_key("1_zero_rb.json", pv)
        results_path.write_text(json.dumps({
            "last_updated": "2026-06-01",
            "combinations": {
                key: {  # NO by_reference -> pre-fix / reference-free mixture
                    "strategy_id": "1_zero_rb.json", "param_values": pv,
                    "best_single_run_win_rate": 0.6, "total_wins": 6, "total_games": 10,
                    "total_runs": 1, "last_run": "2026-06-01",
                }
            },
        }))

    def test_prefix_store_is_renamed_not_destroyed_and_restarts_empty(self, results_path):
        self._prefix_store(results_path)
        with patch("simulation.win_rate.SweepResultsManager.logger", MagicMock()) as mock_logger:
            mgr = SweepResultsManager(results_path)
        # Live store restarts empty.
        assert mgr.get_all_combinations() == {}
        # Old data preserved on disk under exactly one timestamped sibling (renamed, not deleted).
        siblings = list(results_path.parent.glob(results_path.name + ".quarantined-*"))
        assert len(siblings) == 1
        assert json.loads(siblings[0].read_text())["combinations"] != {}
        # Loud WARNING emitted.
        assert mock_logger.warning.called

    def test_empty_store_is_not_quarantined(self, results_path):
        mgr = SweepResultsManager(results_path)      # absent -> empty
        mgr.set_discriminating(True)                 # writes an empty-combinations store
        SweepResultsManager(results_path)            # reload must NOT quarantine
        assert not list(results_path.parent.glob(results_path.name + ".quarantined-*"))

    def test_post_fix_store_is_not_quarantined(self, results_path):
        mgr = SweepResultsManager(results_path)
        mgr.update("1_zero_rb.json", _param_values(), 0.6, 6, 10)  # writes by_reference
        reloaded = SweepResultsManager(results_path)
        assert len(reloaded.get_all_combinations()) == 1
        assert not list(results_path.parent.glob(results_path.name + ".quarantined-*"))


class TestNaiveOpponentsRegimeMarker:
    """T57/D8: the additive top-level opponent-regime marker round-trips, and reads as
    UNKNOWN (None) when the key is absent or null."""

    def test_set_get_naive_opponents_round_trip(self, results_path):
        mgr = SweepResultsManager(results_path)
        mgr.set_naive_opponents(True)
        assert mgr.get_naive_opponents() is True
        assert SweepResultsManager(results_path).get_naive_opponents() is True

    def test_set_naive_opponents_false_round_trips_as_false_not_none(self, results_path):
        # False is a REAL regime (self-play), not "unknown" — the deliberate divergence from
        # the discriminating pair, whose absent case correctly defaults to False.
        mgr = SweepResultsManager(results_path)
        mgr.set_naive_opponents(False)
        assert SweepResultsManager(results_path).get_naive_opponents() is False

    def test_get_naive_opponents_is_none_when_never_set(self, results_path):
        assert SweepResultsManager(results_path).get_naive_opponents() is None

    def test_get_naive_opponents_is_none_when_key_is_null(self, results_path):
        results_path.write_text(json.dumps({
            "last_updated": "2026-07-01", "combinations": {}, "naive_opponents": None,
        }))
        assert SweepResultsManager(results_path).get_naive_opponents() is None

    def test_empty_data_seeds_marker_none_not_false(self, results_path):
        # A quarantine-restarted / absent store must never ASSERT a regime it never ran under.
        assert SweepResultsManager._empty_data()["naive_opponents"] is None


class TestRegimeChangeQuarantine:
    """T57/D3/D4/D7 + AC1/AC3/AC5/AC8/AC9: an opponent-regime change quarantines through T68's
    shared primitive; NOTHING else does; and a repeat quarantine never clobbers an earlier one."""

    def _regime_store(self, results_path, stored_regime, wins=6, fingerprint="old-fp"):
        """Write a post-T68-shaped store (every record carries by_reference, so T68's
        structural trigger cannot fire) whose recorded regime is stored_regime. Pass the
        string "absent" to omit the marker key entirely (a pre-T57 store)."""
        pv = _param_values()
        data = {
            "last_updated": "2026-07-01",
            "input_fingerprint": fingerprint,
            "discriminating": True,
            "combinations": {
                SweepResultsManager.make_combo_key("1_zero_rb.json", pv): {
                    "strategy_id": "1_zero_rb.json", "param_values": pv,
                    "best_single_run_win_rate": 0.6,
                    "by_reference": {"self_play": {"wins": wins, "games": 10}},
                    "total_wins": wins, "total_games": 10, "total_runs": 1,
                    "last_run": "2026-07-01",
                }
            },
            "convergence": {},
        }
        if stored_regime != "absent":
            data["naive_opponents"] = stored_regime
        results_path.write_text(json.dumps(data))
        return data

    def test_regime_flip_false_to_true_quarantines_and_restarts_empty(self, results_path):
        """AC1/AC3: a self-play store re-run under --naive-opponents is archived and the live
        store restarts empty with an emptied fingerprint, so the driver cannot resume."""
        self._regime_store(results_path, stored_regime=False)
        with patch("simulation.win_rate.SweepResultsManager.logger", MagicMock()) as mock_logger:
            mgr = SweepResultsManager(results_path, expected_naive_opponents=True)
        assert mgr.get_all_combinations() == {}
        assert mgr.get_input_fingerprint() == ""
        assert mgr.get_naive_opponents() is None
        assert len(list(results_path.parent.glob(results_path.name + ".quarantined-*"))) == 1
        assert mock_logger.warning.called
        assert "opponent-regime change" in mock_logger.warning.call_args[0][0]

    def test_regime_flip_true_to_false_quarantines(self, results_path):
        self._regime_store(results_path, stored_regime=True)
        with patch("simulation.win_rate.SweepResultsManager.logger", MagicMock()):
            mgr = SweepResultsManager(results_path, expected_naive_opponents=False)
        assert mgr.get_all_combinations() == {}
        assert len(list(results_path.parent.glob(results_path.name + ".quarantined-*"))) == 1

    def test_archived_sibling_preserves_pre_toggle_combinations(self, results_path):
        """AC3: rename-never-delete — the archived sibling's combinations equal exactly what
        was written pre-toggle (T68 asserts only non-emptiness, which is weaker)."""
        written = self._regime_store(results_path, stored_regime=False)
        with patch("simulation.win_rate.SweepResultsManager.logger", MagicMock()):
            SweepResultsManager(results_path, expected_naive_opponents=True)
        siblings = list(results_path.parent.glob(results_path.name + ".quarantined-*"))
        assert len(siblings) == 1
        assert json.loads(siblings[0].read_text())["combinations"] == written["combinations"]

    def test_unseeded_rerun_fingerprint_mismatch_does_not_quarantine(self, results_path):
        """AC9 (spec OQ1's user decision): a NON-estimand input change — a fresh auto-seed on
        an unseeded re-run, an added strategy file, a different --num-values — all reach the
        store as a DIFFERING stored input_fingerprint at the SAME regime. That must set
        resume=False in the driver but must NOT archive: no sibling, store kept intact."""
        written = self._regime_store(results_path, stored_regime=False, fingerprint="stale-fp")
        mgr = SweepResultsManager(results_path, expected_naive_opponents=False)
        assert not list(results_path.parent.glob(results_path.name + ".quarantined-*"))
        assert results_path.exists()
        assert mgr.get_all_combinations() == written["combinations"]
        assert mgr.get_input_fingerprint() == "stale-fp"

    def test_absent_marker_never_quarantines_and_store_is_not_rewritten(self, results_path):
        """AC5 / D8: a pre-T57 store carries no regime marker — UNKNOWN, never guessed at.
        _load adds no setdefault for the key, so the file is left byte-identical on load."""
        self._regime_store(results_path, stored_regime="absent")
        raw_before = results_path.read_text()
        mgr = SweepResultsManager(results_path, expected_naive_opponents=True)
        assert not list(results_path.parent.glob(results_path.name + ".quarantined-*"))
        assert mgr.get_naive_opponents() is None
        assert results_path.read_text() == raw_before
        assert "naive_opponents" not in json.loads(raw_before)

    def test_null_marker_never_quarantines(self, results_path):
        self._regime_store(results_path, stored_regime=None)
        mgr = SweepResultsManager(results_path, expected_naive_opponents=True)
        assert not list(results_path.parent.glob(results_path.name + ".quarantined-*"))
        assert len(mgr.get_all_combinations()) == 1

    def test_no_expected_regime_never_quarantines(self, results_path):
        """AC7: --promote and every pre-existing test construct with ONE positional argument;
        the default None must leave the regime trigger completely inert."""
        self._regime_store(results_path, stored_regime=False)
        mgr = SweepResultsManager(results_path)
        assert not list(results_path.parent.glob(results_path.name + ".quarantined-*"))
        assert len(mgr.get_all_combinations()) == 1

    def test_matching_regime_never_quarantines(self, results_path):
        self._regime_store(results_path, stored_regime=True)
        mgr = SweepResultsManager(results_path, expected_naive_opponents=True)
        assert not list(results_path.parent.glob(results_path.name + ".quarantined-*"))
        assert len(mgr.get_all_combinations()) == 1

    def test_empty_combinations_never_quarantines_on_regime_change(self, results_path):
        """Mirrors T68's `if combinations` guard: nothing to preserve, so no operator-visible
        empty sibling is produced."""
        results_path.write_text(json.dumps({
            "last_updated": "2026-07-01", "combinations": {}, "naive_opponents": False,
        }))
        SweepResultsManager(results_path, expected_naive_opponents=True)
        assert not list(results_path.parent.glob(results_path.name + ".quarantined-*"))

    def test_repeat_quarantine_in_same_minute_does_not_clobber(self, results_path):
        """AC8 / D7: two quarantines of the same store at the SAME minute-resolution stamp
        leave BOTH archives on disk with distinct content. Pre-D7 the bare Path.rename would
        silently replace the first archive and only one file would survive."""
        fake_datetime = MagicMock()
        fake_datetime.datetime.now.return_value.strftime.return_value = "2026-07-21T1200"
        fake_datetime.date.today.return_value.isoformat.return_value = "2026-07-21"
        with patch("simulation.win_rate.SweepResultsManager.datetime", fake_datetime), \
             patch("simulation.win_rate.SweepResultsManager.logger", MagicMock()):
            first = self._regime_store(results_path, stored_regime=False, wins=6)
            SweepResultsManager(results_path, expected_naive_opponents=True)
            second = self._regime_store(results_path, stored_regime=False, wins=9)
            SweepResultsManager(results_path, expected_naive_opponents=True)
        siblings = sorted(results_path.parent.glob(results_path.name + ".quarantined-*"))
        assert len(siblings) == 2
        archived = [json.loads(s.read_text())["combinations"] for s in siblings]
        assert first["combinations"] in archived
        assert second["combinations"] in archived
