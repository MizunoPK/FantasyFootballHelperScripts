"""
Tests for simulation.win_rate.SweepTournament.

Unit-only: a mocked CombinationEvaluator returns canned (wins, games, win_rate) keyed
on its inputs (controlling which strategy/value "wins"); a real SweepResultsManager on
tmp_path exercises the store; generate_candidate_values is the committed function.

Author: Kai Mizuno
"""

# Standard library
import json
from unittest.mock import Mock

# Third-party
import pytest

# Local
from simulation.win_rate.SweepTournament import (
    SweepTournament,
    _adopt_by_significance,
    _read_convergence_best_rate,
    DEFAULT_CONFIDENCE,
    DEFAULT_MIN_EFFECT_SIZE,
    DEFAULT_MIN_GAMES,
)
from simulation.win_rate.SweepResultsManager import SweepResultsManager
from simulation.win_rate.param_value_generation import generate_candidate_values, DRAFT_SWEEP_PARAMS
from utils.error_handler import ConfigurationError


def _baseline():
    return {
        "SAME_POS_BYE_WEIGHT": 0.07,
        "DIFF_POS_BYE_WEIGHT": 0.01,
        "PRIMARY_BONUS": 67,
        "SECONDARY_BONUS": 69,
        "ADP_SCORING_WEIGHT": 4.76,
        "PLAYER_RATING_SCORING_WEIGHT": 3.52,
    }


def _evaluator(rate_fn):
    """Mock evaluator: rate_fn(draft_order, param_values) -> win_rate in [0,1]."""
    ev = Mock()

    def side_effect(draft_order, param_values):
        wr = rate_fn(draft_order, param_values)
        return (int(round(wr * 10)), 10, wr)

    ev.evaluate.side_effect = side_effect
    return ev


def _store(tmp_path, name="win_rate_sweep_results.json"):
    return SweepResultsManager(tmp_path / name)


def _wg_evaluator(wg_fn):
    """Mock evaluator: wg_fn(draft_order, param_values) -> (wins, games).

    Lets a test pin exact accumulated wins/games per combination so the significance gate's
    thresholds (effect size, sample size, significance) are hit deterministically. Each combo
    is evaluated once on a fresh store, so its accumulated counts equal the returned batch.
    """
    ev = Mock()

    def side_effect(draft_order, param_values):
        wins, games = wg_fn(draft_order, param_values)
        win_rate = wins / games if games else 0.0
        return (wins, games, win_rate)

    ev.evaluate.side_effect = side_effect
    return ev


def _max_pb(baseline):
    """The maximum PRIMARY_BONUS candidate for the committed grid (the ascent target)."""
    return max(generate_candidate_values(baseline, 5)["PRIMARY_BONUS"])


class TestSweepTournament:
    """Tests for SweepTournament.run (per-config convergent coordinate ascent)."""

    def test_tunes_every_config_independently(self, tmp_path):
        # Each config's win rate depends on its own draft_order; every config is tuned.
        ev = _evaluator(lambda do, pv: 0.9 if do == [{"s": "2"}] else 0.5)
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run(
            [("s1", [{"s": "1"}]), ("s2", [{"s": "2"}]), ("s3", [{"s": "3"}])],
            _baseline(),
        )
        assert set(result.keys()) == {"s1", "s2", "s3"}
        for entry in result.values():
            assert set(entry.keys()) == {"param_values", "win_rate"}
            assert set(entry["param_values"].keys()) == set(DRAFT_SWEEP_PARAMS)

    def test_sweeps_and_selects_best_value(self, tmp_path):
        # Step landscape: the max PRIMARY_BONUS candidate scores 0.70 (700/1000) with a large,
        # significant effect over the 0.60 baseline; every other value scores 0.60. Coordinate
        # ascent adopts the max candidate (significance + effect both clear) and converges there.
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            return (700, 1000) if pv["PRIMARY_BONUS"] == target else (600, 1000)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == target

    def test_gate_blocks_trivial_effect_gain(self, tmp_path):
        # Significance is satisfiable (huge n) but the accumulated-rate effect is only 0.005,
        # which does not exceed min_effect_size (0.01). The AND-ed effect floor blocks adoption
        # of this statistically-detectable-but-trivial gain — nothing is adopted (D2).
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            # 0.505 vs 0.500 -> effect 0.005 (<= 0.01) over n=100000 each (clearly significant).
            return (50500, 100000) if pv["PRIMARY_BONUS"] == target else (50000, 100000)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline

    def test_converges_on_flat_landscape(self, tmp_path):
        # Constant win rate -> every candidate's accumulated-rate effect over the running best is
        # 0 (< min_effect_size), so the gate adopts nothing, a full pass moves nothing, and the
        # loop terminates at the baseline.
        ev = _wg_evaluator(lambda do, pv: (600, 1000))
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}]), ("s2", [{"s": "2"}])], _baseline())
        for entry in result.values():
            assert entry["param_values"] == _baseline()

    def test_records_all_evaluations_to_store(self, tmp_path):
        ev = _evaluator(lambda do, pv: 0.6)
        store = _store(tmp_path)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}]), ("s2", [{"s": "2"}])], _baseline())
        combos = store.get_all_combinations()
        assert len(combos) > 0
        # Both configs were evaluated -> both strategy_ids appear in the store.
        strategy_ids = {entry["strategy_id"] for entry in combos.values()}
        assert {"s1", "s2"} <= strategy_ids

    def test_rerun_accumulates_in_store(self, tmp_path):
        ev = _evaluator(lambda do, pv: 0.6)
        store = _store(tmp_path)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}])], _baseline())
        t.run([("s1", [{"s": "1"}])], _baseline())
        # At least one combination was evaluated twice across the two runs.
        assert any(entry["total_runs"] >= 2 for entry in store.get_all_combinations().values())

    def test_num_values_controls_candidates(self, tmp_path):
        ev_small = _evaluator(lambda do, pv: 0.6)
        SweepTournament(ev_small, _store(tmp_path, "a.json"), num_values=3).run([("s1", [{"s": "1"}])], _baseline())
        ev_large = _evaluator(lambda do, pv: 0.6)
        SweepTournament(ev_large, _store(tmp_path, "b.json"), num_values=8).run([("s1", [{"s": "1"}])], _baseline())
        assert ev_large.evaluate.call_count > ev_small.evaluate.call_count

    def test_empty_strategies_raises(self, tmp_path):
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, _store(tmp_path))
        with pytest.raises(ConfigurationError):
            t.run([], _baseline())

    def test_gate_constants_match_init_defaults(self, tmp_path):
        # The module constants must be the constructor defaults, so the driver's fingerprint
        # (built from the constants) and the engine's gate never drift (a drift would spuriously
        # mismatch every resume).
        import inspect
        sig = inspect.signature(SweepTournament.__init__)
        assert sig.parameters["confidence"].default == DEFAULT_CONFIDENCE
        assert sig.parameters["min_effect_size"].default == DEFAULT_MIN_EFFECT_SIZE
        assert sig.parameters["min_games"].default == DEFAULT_MIN_GAMES
        assert DEFAULT_CONFIDENCE == 0.95
        assert DEFAULT_MIN_EFFECT_SIZE == 0.01
        assert DEFAULT_MIN_GAMES == 30

    def test_invalid_confidence_raises(self, tmp_path):
        # NF3: confidence outside the open interval (0, 1) is a configuration error.
        for bad in (0, 1, -0.1, 1.5):
            with pytest.raises(ConfigurationError):
                SweepTournament(_evaluator(lambda do, pv: 0.6), _store(tmp_path), confidence=bad)

    def test_invalid_min_games_raises(self, tmp_path):
        # min_games < 1 is a configuration error: a zero/negative value breaks the
        # '_adopt_by_significance' floor assumption (the "floor guarantees n>0" comment)
        # which would cause a divide-by-zero on 1/n_trial + 1/n_best.
        ev = _evaluator(lambda do, pv: 0.6)
        for bad in (0, -1, -10):
            with pytest.raises(ConfigurationError):
                SweepTournament(ev, _store(tmp_path), min_games=bad)

    def test_invalid_min_effect_size_raises(self, tmp_path):
        # min_effect_size outside [0, 1) is a configuration error: a negative value
        # inverts the effect guard, and >= 1 makes adoption mathematically impossible
        # (win rates are bounded to [0, 1]).
        ev = _evaluator(lambda do, pv: 0.6)
        for bad in (-0.1, -1.0, 1.0, 1.5):
            with pytest.raises(ConfigurationError):
                SweepTournament(ev, _store(tmp_path), min_effect_size=bad)

    def test_valid_defaults_construct_without_error(self, tmp_path):
        # The module defaults (confidence=0.95, min_effect_size=0.01, min_games=30) all
        # pass the new validation and construct a SweepTournament without error.
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, _store(tmp_path))  # must not raise
        assert t is not None

    def test_resume_in_progress_old_schema_convergence_no_keyerror(self, tmp_path):
        # D4: resuming an in_progress config written under the legacy "best_win_rate" key must
        # not KeyError — the line-246 baseline read falls back to the legacy key. Flat landscape
        # so ascent converges immediately on the checkpointed seed.
        path = tmp_path / "win_rate_sweep_results.json"
        baseline = _baseline()
        seeded = dict(baseline)
        seeded["PRIMARY_BONUS"] = 91
        old_schema = {
            "last_updated": "2026-06-01",
            "combinations": {},
            "convergence": {
                "s1": {
                    "status": "in_progress",
                    "best_param_values": seeded,
                    "best_win_rate": 0.7,
                    "updated": "2026-06-01",
                }
            },
        }
        path.write_text(json.dumps(old_schema))
        store = SweepResultsManager(path)
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        result = t.run([("s1", [{"s": "1"}])], baseline, resume=True)  # must not raise KeyError
        # Resumed from the checkpointed seed (not baseline 67); baseline best_rate read from the
        # legacy key (0.7) and carried through the flat-landscape (no-move) convergence.
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == 91
        assert result["s1"]["win_rate"] == 0.7

    def test_resume_converged_old_schema_convergence_no_keyerror(self, tmp_path):
        # D4: a converged config written under the legacy "best_win_rate" key must be skipped on
        # resume and surface its checkpointed rate via the line-235 fallback read (no KeyError).
        path = tmp_path / "win_rate_sweep_results.json"
        baseline = _baseline()
        old_schema = {
            "last_updated": "2026-06-01",
            "combinations": {},
            "convergence": {
                "s1": {
                    "status": "converged",
                    "best_param_values": baseline,
                    "best_win_rate": 0.8,
                    "updated": "2026-06-01",
                }
            },
        }
        path.write_text(json.dumps(old_schema))
        store = SweepResultsManager(path)
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        result = t.run([("s1", [{"s": "1"}])], baseline, resume=True)  # must not raise KeyError
        assert ev.evaluate.call_count == 0           # converged -> skipped
        assert result["s1"]["win_rate"] == 0.8        # read via legacy-key fallback

    def test_read_convergence_best_rate_new_key(self):
        # Helper returns best_combo_win_rate when present (D4 primary key).
        conv = {"best_combo_win_rate": 0.75, "best_win_rate": 0.60}
        assert _read_convergence_best_rate(conv) == 0.75

    def test_read_convergence_best_rate_legacy_key(self):
        # Helper falls back to legacy best_win_rate when new key is absent (D4 back-compat).
        conv = {"best_win_rate": 0.65}
        assert _read_convergence_best_rate(conv) == 0.65

    def test_read_convergence_best_rate_neither_key_raises(self):
        # Corrupt entry carrying neither key must raise KeyError — fail-fast, not silent None.
        conv = {"status": "converged", "best_param_values": {}}
        with pytest.raises(KeyError, match="missing both"):
            _read_convergence_best_rate(conv)

    def test_resume_skips_converged_config(self, tmp_path):
        # A pre-marked converged config is skipped (evaluator not called for it) when resume=True.
        store = _store(tmp_path)
        baseline = _baseline()
        store.mark_config_progress("s1", "converged", baseline, 0.8)
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        result = t.run([("s1", [{"s": "1"}])], baseline, resume=True)
        # Evaluator never called (the only config was skipped).
        assert ev.evaluate.call_count == 0
        # The skipped config's checkpointed best is surfaced in the result map.
        assert result["s1"]["win_rate"] == 0.8
        assert result["s1"]["param_values"] == baseline

    def test_resume_seeds_in_progress_config_from_checkpoint(self, tmp_path):
        # An in_progress config starts coordinate ascent from its checkpointed best_param_values,
        # not from baseline. Seed a non-baseline PRIMARY_BONUS and assert the first evaluated
        # trial carries the seeded value (proving the start point moved).
        store = _store(tmp_path)
        baseline = _baseline()
        seeded = dict(baseline)
        seeded["PRIMARY_BONUS"] = 91
        store.mark_config_progress("s1", "in_progress", seeded, 0.7)
        # Flat landscape so nothing moves -> coordinate ascent converges immediately on the seed.
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        result = t.run([("s1", [{"s": "1"}])], baseline, resume=True)
        # No baseline re-eval: every trial seen by the evaluator carries the seeded PRIMARY_BONUS
        # except where coordinate ascent varies PRIMARY_BONUS itself.
        first_pv = ev.evaluate.call_args_list[0].args[1]
        assert first_pv["PRIMARY_BONUS"] == 91  # seeded start, not baseline 67
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == 91

    def test_marks_in_progress_then_converged_per_config(self, tmp_path):
        # mark_config_progress is written in_progress then converged for each tuned config.
        store = _store(tmp_path)
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}])], _baseline())
        conv = store.get_config_convergence("s1")
        assert conv is not None
        assert conv["status"] == "converged"  # final mark is converged

    def test_in_progress_checkpoint_tracks_running_best_mid_ascent(self, tmp_path):
        # PR #18: an improvement found mid coordinate-ascent must be persisted immediately as an
        # in_progress checkpoint, so an interrupt before convergence resumes from the latest best
        # (not the stale seed). Landscape: any non-baseline PRIMARY_BONUS scores 0.90 (900/1000)
        # vs the 0.60 baseline (600/1000) — a large, significant effect — so the first such trial
        # adopts and must trigger an in_progress write carrying the new accumulated best (0.90).
        store = _store(tmp_path)
        baseline = _baseline()
        ev = _wg_evaluator(lambda do, pv: (900, 1000) if pv["PRIMARY_BONUS"] != 67 else (600, 1000))
        store.mark_config_progress = Mock(wraps=store.mark_config_progress)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}])], baseline)
        calls = store.mark_config_progress.call_args_list
        statuses = [c.args[1] for c in calls]  # args: (strategy_id, status, best_params, best_rate)
        improved = [
            i for i, c in enumerate(calls)
            if c.args[1] == "in_progress" and c.args[3] == 0.9
        ]
        assert improved, "no in_progress checkpoint captured the mid-ascent improvement"
        assert min(improved) < statuses.index("converged")  # running best persisted before converge

    def test_resume_false_reproduces_all_from_baseline(self, tmp_path):
        # Regression guard: with resume=False (default), a pre-marked converged config is NOT
        # skipped — every config is re-evaluated from baseline as in the pre-T9 behavior.
        store = _store(tmp_path)
        baseline = _baseline()
        store.mark_config_progress("s1", "converged", baseline, 0.8)
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}])], baseline, resume=False)
        # Evaluator WAS called (config not skipped) -> resume=False ignores convergence.
        assert ev.evaluate.call_count > 0

    def test_carry_over_seed_starts_from_seed_and_tunes_full_grid(self, tmp_path):
        # T10/D1a: a config with a carry_over_seeds entry starts its ascent from the seed
        # (not baseline) and is NOT skipped — it tunes over the full grid. Flat landscape so
        # nothing moves -> ascent converges immediately on the seed, and the FIRST evaluated
        # trial carries the seeded PRIMARY_BONUS (proving the start point is the seed).
        baseline = _baseline()
        seed = dict(baseline)
        seed["PRIMARY_BONUS"] = 91
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run(
            [("s1", [{"s": "1"}])], baseline, carry_over_seeds={"s1": seed}
        )
        # First evaluation is the seed combo (re-eval once to set best_rate) — carries the seed.
        first_pv = ev.evaluate.call_args_list[0].args[1]
        assert first_pv["PRIMARY_BONUS"] == 91  # seeded start, not baseline 67
        # Not skipped: the evaluator ran a full ascent (more than the single seed eval).
        assert ev.evaluate.call_count > 1
        # Converged on the seed (flat landscape), and the config is marked converged.
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == 91
        conv = _store(tmp_path).get_config_convergence("s1")
        assert conv is not None and conv["status"] == "converged"

    def test_carry_over_seeds_none_is_backward_compatible(self, tmp_path):
        # T10: carry_over_seeds defaults to None -> unchanged behavior (every config starts
        # from baseline). A config with NO seed entry also falls back to baseline.
        baseline = _baseline()
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, _store(tmp_path))
        # Default None.
        result_default = t.run([("s1", [{"s": "1"}])], baseline)
        assert result_default["s1"]["param_values"] == baseline
        # Empty seed map -> "s2" has no entry -> baseline start (first trial is baseline).
        ev2 = _evaluator(lambda do, pv: 0.6)
        t2 = SweepTournament(ev2, _store(tmp_path, "b.json"))
        t2.run([("s2", [{"s": "2"}])], baseline, carry_over_seeds={})
        first_pv = ev2.evaluate.call_args_list[0].args[1]
        assert first_pv["PRIMARY_BONUS"] == baseline["PRIMARY_BONUS"]  # baseline 67, no seed

    def test_holds_when_running_best_unrecorded(self, tmp_path):
        """None-running-best hold-guard regression (T31/PR #18 checkpoint-resume path).

        When an in_progress resume seeds `current` from convergence metadata but that
        combo was never update()-ed in this run (no accumulated evidence in the store),
        ``get_combination(strategy_id, current)`` returns None.  The inner-loop guard

            if best_entry is not None and _adopt_by_significance(...)

        must hold (short-circuit) so run() completes without raising.  Remove the guard
        and this test fails with TypeError (None["total_wins"]).
        """
        store = _store(tmp_path)
        baseline = _baseline()
        # Seed `current` to a non-baseline PRIMARY_BONUS that has NEVER been evaluated —
        # so get_combination("s1", seeded) returns None (no store combination entry exists).
        seeded = dict(baseline)
        seeded["PRIMARY_BONUS"] = 91
        store.mark_config_progress("s1", "in_progress", seeded, 0.7)
        # Evaluator returns a strongly adoptable result (900/1000) for every trial, so
        # the inner-loop adoption path is reached and best_entry is None is encountered.
        ev = _wg_evaluator(lambda do, pv: (900, 1000))
        t = SweepTournament(ev, store)
        # Must complete without raising (TypeError if the best_entry guard is removed).
        result = t.run([("s1", [{"s": "1"}])], baseline, resume=True)
        # Guard held -> run returned a result without crashing.
        assert "s1" in result
        # Guard held -> no adoption over a None running-best -> current stays at the seed.
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == 91


class TestSweepTournamentProgressCallback:
    """T16/KDD-2: the optional progress_callback fires exactly once per config (on both the
    converged and the resume-skip path), and defaults to a no-op when not supplied."""

    def test_callback_fires_once_per_converged_config(self, tmp_path):
        # Flat landscape: every config converges immediately on baseline. The callback must
        # fire exactly once per config, with that config's strategy_id.
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, _store(tmp_path))
        seen = []
        t.run(
            [("s1", [{"s": "1"}]), ("s2", [{"s": "2"}]), ("s3", [{"s": "3"}])],
            _baseline(),
            progress_callback=lambda sid: seen.append(sid),
        )
        assert seen == ["s1", "s2", "s3"]  # once per config, in order

    def test_callback_fires_on_resume_skip_path(self, tmp_path):
        # A pre-marked converged config is resume-skipped (evaluator not called) but the callback
        # must STILL fire once for it, or a resumed pass would never reach 100% on the bar.
        store = _store(tmp_path)
        baseline = _baseline()
        store.mark_config_progress("s1", "converged", baseline, 0.8)
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        seen = []
        t.run(
            [("s1", [{"s": "1"}])], baseline, resume=True,
            progress_callback=lambda sid: seen.append(sid),
        )
        assert ev.evaluate.call_count == 0  # skipped (no evaluation)
        assert seen == ["s1"]  # callback still fired once on the skip path

    def test_callback_default_none_is_noop(self, tmp_path):
        # No progress_callback -> unchanged behavior, no error. The result map is still produced.
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], _baseline())
        assert set(result.keys()) == {"s1"}


class TestSweepTournamentSignificanceGate:
    """T31: end-to-end adoption decisions driven through run() with a real store, exercising
    the accumulated-evidence significance + effect-size gate (D1/D2/D4/D5)."""

    def test_adopts_significant_and_large_effect(self, tmp_path):
        # Target PRIMARY_BONUS accumulates 700/1000 (0.70); baseline/others 600/1000 (0.60).
        # effect 0.10 (> 0.01) and z ~= 4.7 (> z_crit), both combos >= 30 games -> ADOPT.
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            return (700, 1000) if pv["PRIMARY_BONUS"] == target else (600, 1000)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == target
        # F7: returned win_rate is the running-best's ACCUMULATED rate (700/1000 = 0.70).
        assert result["s1"]["win_rate"] == pytest.approx(0.70)

    def test_holds_when_not_significant(self, tmp_path):
        # Large effect (0.60 vs 0.40) but tiny n=30 each -> z ~= 1.55 (< z_crit) -> HOLD.
        # Isolates the significance condition (the effect floor is satisfied).
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            return (18, 30) if pv["PRIMARY_BONUS"] == target else (12, 30)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline

    def test_holds_on_trivial_effect_despite_significance(self, tmp_path):
        # 0.505 vs 0.500 over n=100000 each -> clearly significant but effect 0.005 (<= 0.01)
        # -> the AND-ed effect floor blocks the "large-n trivial-difference" bypass -> HOLD.
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            return (50500, 100000) if pv["PRIMARY_BONUS"] == target else (50000, 100000)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline

    def test_holds_below_min_games_floor(self, tmp_path):
        # Huge effect (1.0 vs 0.0) but only 20 games per combo (< min_games=30) -> HOLD (D5 floor).
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            return (20, 20) if pv["PRIMARY_BONUS"] == target else (0, 20)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline

    def test_holds_on_zero_standard_error_without_crashing(self, tmp_path):
        # Degenerate all-wins pool above the floor (60/60 vs 30/30) -> p_pool == 1 -> se == 0
        # -> HOLD via the explicit se==0 guard (no ZeroDivisionError) (D5).
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            return (60, 60) if pv["PRIMARY_BONUS"] == target else (30, 30)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)  # must not raise
        assert result["s1"]["param_values"] == baseline


class TestAdoptBySignificanceBoundaries:
    """T31/D6: the strict-boundary disposition of the pure gate helper — strict '>' at the
    significance critical value and the effect-size floor, inclusive '>=' at the games floor."""

    def test_games_floor_is_inclusive(self):
        # Exactly min_games (30) passes the floor and (significant + large effect) adopts;
        # one game short (29) holds. Isolates the floor's inclusivity.
        assert _adopt_by_significance(30, 30, 0, 30, 0.95, 0.01, 30) is True
        assert _adopt_by_significance(29, 29, 0, 29, 0.95, 0.01, 30) is False

    def test_effect_floor_is_strict(self):
        # Significant data (700/1000 vs 600/1000); effect exactly == min_effect_size holds
        # (strict '>'), while a hair below the effect adopts.
        eff = 700 / 1000 - 600 / 1000  # identical float to the helper's p_trial - p_best
        assert _adopt_by_significance(700, 1000, 600, 1000, 0.95, eff, 30) is False
        assert _adopt_by_significance(700, 1000, 600, 1000, 0.95, eff - 1e-9, 30) is True

    def test_significance_critical_value_is_strict(self):
        # Place z exactly at the critical value by setting confidence = cdf(z) (round-trip
        # identity) -> strict '>' holds; a slightly lower confidence (lower z_crit) adopts.
        # Effect (0.20) and games (100) clear their gates, isolating the significance boundary.
        from math import sqrt
        from statistics import NormalDist
        p_pool = (60 + 40) / (100 + 100)
        se = sqrt(p_pool * (1.0 - p_pool) * (1.0 / 100 + 1.0 / 100))
        z = (60 / 100 - 40 / 100) / se
        conf_at = NormalDist().cdf(z)
        assert _adopt_by_significance(60, 100, 40, 100, conf_at, 0.01, 30) is False
        assert _adopt_by_significance(60, 100, 40, 100, conf_at - 0.01, 0.01, 30) is True
