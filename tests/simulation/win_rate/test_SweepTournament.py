"""
Tests for simulation.win_rate.SweepTournament.

Unit-only: a mocked CombinationEvaluator returns canned (wins, games, win_rate) keyed
on its inputs (controlling which strategy/value "wins"); a real SweepResultsManager on
tmp_path exercises the store; generate_candidate_values is the committed function.

Author: Kai Mizuno
"""

# Standard library
import json
import random
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

    def side_effect(draft_order, param_values, incumbent_param_values=None):
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

    def side_effect(draft_order, param_values, incumbent_param_values=None):
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
        # T58 step landscape: exactly ONE combination — baseline with PRIMARY_BONUS at the max
        # candidate — scores 0.70 head-to-head (700/1000): effect 0.20 over the 0.50 null and
        # z ~= 12.6, so it adopts. EVERY other combination sits exactly at the 0.50 null
        # (500/1000), effect 0.0, and is held by both gate conditions. Keying on the WHOLE param
        # dict (not PRIMARY_BONUS alone) is load-bearing: under a one-sample-vs-0.50 gate a fake
        # that kept returning >0.50 after the first adoption would make every later candidate
        # significant too, so `moved` would never go False and run() would never terminate.
        baseline = _baseline()
        target = _max_pb(baseline)
        winner = dict(baseline)
        winner["PRIMARY_BONUS"] = target

        def wg(do, pv):
            return (700, 1000) if pv == winner else (500, 1000)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == target

    def test_gate_blocks_trivial_effect_gain(self, tmp_path):
        # T58: the target's fresh rate is 0.505 -> effect 0.005 against the 0.50 null, which does
        # not exceed min_effect_size (0.01), while z ~= 3.16 DOES clear significance. This is the
        # genuine large-n demonstration that the AND-ed effect floor is live: it blocks a
        # statistically-detectable-but-trivial gain. Every other combo is exactly at 0.500.
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            # 0.505 vs 0.500 -> effect 0.005 (<= 0.01) over n=100000 each (clearly significant).
            return (50500, 100000) if pv["PRIMARY_BONUS"] == target else (50000, 100000)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline

    def test_converges_on_flat_landscape(self, tmp_path):
        # T58: a flat landscape sitting exactly AT the 0.50 null (500/1000). Every candidate's
        # effect is 0.0, so both gate conditions hold it, the first full pass moves nothing, and
        # the loop terminates at the baseline. The fake MUST sit at or below 0.50 — the old
        # 600/1000 constant is p = 0.60 with z ~= 6.3, which under the one-sample gate would
        # adopt EVERY candidate forever and hang run() rather than failing an assertion.
        ev = _wg_evaluator(lambda do, pv: (500, 1000))
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
        # (not the stale seed). T58 landscape: exactly ONE combination — baseline with
        # PRIMARY_BONUS at the max candidate — scores 0.90 (900/1000) head-to-head; every other
        # combination sits at the 0.50 null (500/1000) and is held. That single adoption writes an
        # in_progress checkpoint carrying best_rate 0.9 — which under T58/R4 is the trial's FRESH
        # win_rate, not a store-accumulated rate. Keying on the WHOLE param dict is load-bearing:
        # the old "any non-baseline PRIMARY_BONUS" fake would re-adopt on every later candidate
        # under the one-sample gate and run() would never terminate.
        store = _store(tmp_path)
        baseline = _baseline()
        winner = dict(baseline)
        winner["PRIMARY_BONUS"] = _max_pb(baseline)
        ev = _wg_evaluator(lambda do, pv: (900, 1000) if pv == winner else (500, 1000))
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

    def test_trials_pass_running_best_incumbent(self, tmp_path):
        """D2: trials pass incumbent_param_values=current, anchors remain 2-arg (T54/D2)."""
        baseline = _baseline()
        # T58: flat landscape AT the 0.50 null so nothing adopts and the ascent terminates after
        # one pass. This test pins the T54 CALL SHAPE (anchors 2-arg, trials pass an incumbent),
        # not any adoption outcome, so a null-centred fake is the correct fixture. The old
        # 600/1000 constant would adopt every candidate under the one-sample gate and hang.
        ev = _wg_evaluator(lambda do, pv: (500, 1000))
        t = SweepTournament(ev, _store(tmp_path))
        t.run([("s1", [{"s": "1"}])], baseline)

        # Inspect mock call history: at least one trial call has incumbent_param_values kwarg
        # (the trials at line 309 in the coordinate-ascent loop).
        # The baseline/seed/anchor evaluations (lines 284, 291) are called without incumbent_param_values.
        assert ev.evaluate.call_count > 1, "Should have multiple evaluate calls (baseline + trials)"

        call_args_list = ev.evaluate.call_args_list
        # First call should be the baseline/seed (2-arg, no incumbent_param_values)
        baseline_call = call_args_list[0]
        assert "incumbent_param_values" not in baseline_call.kwargs or baseline_call.kwargs.get("incumbent_param_values") is None

        # At least one trial call should have incumbent_param_values as a kwarg
        trial_calls_with_incumbent = [
            call for call in call_args_list[1:]
            if "incumbent_param_values" in call.kwargs and call.kwargs["incumbent_param_values"] is not None
        ]
        assert len(trial_calls_with_incumbent) > 0, "Should have at least one trial with incumbent_param_values"

    def test_accumulated_rate_reads_only_the_self_play_bucket(self, tmp_path):
        # T68/D4: _accumulated_rate returns the self_play bucket rate, never a blend with any
        # head-to-head games the same combo accrued as a trial.
        store = _store(tmp_path)
        baseline = _baseline()
        incumbent = dict(baseline, PRIMARY_BONUS=80)
        store.update("s1", baseline, 0.5, 50, 100)                                  # self_play
        store.update("s1", baseline, 0.9, 90, 100, incumbent_param_values=incumbent)  # head-to-head
        t = SweepTournament(_evaluator(lambda do, pv: 0.6), store)
        # self_play rate (0.50), NOT the blended 140/200 = 0.70.
        assert t._accumulated_rate("s1", baseline) == 0.5

    def test_accumulated_rate_zero_when_no_self_play_bucket(self, tmp_path):
        # A combo evaluated ONLY head-to-head has no self_play bucket -> 0.0 (defensive guard).
        store = _store(tmp_path)
        baseline = _baseline()
        incumbent = dict(baseline, PRIMARY_BONUS=80)
        store.update("s1", baseline, 0.9, 90, 100, incumbent_param_values=incumbent)
        t = SweepTournament(_evaluator(lambda do, pv: 0.6), store)
        assert t._accumulated_rate("s1", baseline) == 0.0
        # Unrecorded combo -> 0.0.
        assert t._accumulated_rate("s1", dict(baseline, PRIMARY_BONUS=999)) == 0.0


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
    """T31, revised by T58: end-to-end adoption decisions driven through run() with a real store,
    exercising the one-sample (vs the 0.50 null) significance + effect-size gate over each trial's
    FRESH head-to-head evaluation.

    HANG HAZARD — read before changing any fake in this class: run()'s only stopping rule is a
    full pass that moves no parameter. Under a one-sample-vs-0.50 gate, a fake returning a
    constant rate above 0.50 at large n makes EVERY candidate significant, so `moved` never goes
    False and run() never returns — the suite hangs rather than failing an assertion. Every
    non-adopting arm must therefore sit at or below 0.50, and any adopting arm must be keyed on
    the WHOLE param dict so it cannot re-fire after the adoption.
    """

    def test_adopts_significant_and_large_effect(self, tmp_path):
        # T58: the winning combination scores 0.70 head-to-head (700/1000) — effect 0.20 over the
        # 0.50 null and z ~= 12.6 (> z_crit), n = 1000 >= 30 -> ADOPT. Every other combination
        # sits at the 0.50 null (500/1000) and is held, which is also what makes the ascent
        # terminate under a one-sample gate (see the class-level hang note).
        baseline = _baseline()
        target = _max_pb(baseline)
        winner = dict(baseline)
        winner["PRIMARY_BONUS"] = target

        def wg(do, pv):
            return (700, 1000) if pv == winner else (500, 1000)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == target
        # T58/R4: returned win_rate is the winning trial's FRESH head-to-head rate (0.70).
        assert result["s1"]["win_rate"] == pytest.approx(0.70)

    def test_holds_when_not_significant(self, tmp_path):
        # T58: the target's fresh rate is 18/30 = 0.60 -> effect 0.10 (clears the 0.01 floor) but
        # n = 30 gives z = 0.10 / sqrt(0.25/30) ~= 1.10 < z_crit ~= 1.645 -> HOLD. Isolates the
        # one-sample significance condition. Every other combo is 12/30 = 0.40 (negative effect).
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            return (18, 30) if pv["PRIMARY_BONUS"] == target else (12, 30)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline

    def test_holds_on_trivial_effect_despite_significance(self, tmp_path):
        # T58: the target's fresh rate is 0.505 over n = 100000 -> z ~= 3.16 clears significance
        # but the effect against the 0.50 null is 0.005 (<= 0.01) -> the AND-ed effect floor
        # blocks the "large-n trivial-difference" bypass -> HOLD.
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            return (50500, 100000) if pv["PRIMARY_BONUS"] == target else (50000, 100000)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline

    def test_holds_below_min_games_floor(self, tmp_path):
        # T58: a maximal effect (the target's fresh rate is 20/20 = 1.0) but the evaluation yields
        # only n = 20 games (< min_games = 30) -> HOLD on the floor, now applied to the trial's
        # OWN fresh evaluation rather than to accumulated games.
        baseline = _baseline()
        target = _max_pb(baseline)

        def wg(do, pv):
            return (20, 20) if pv["PRIMARY_BONUS"] == target else (0, 20)

        t = SweepTournament(_wg_evaluator(wg), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline


class TestAdoptBySignificanceBoundaries:
    """T31/D6, revised by T58: the strict-boundary disposition of the pure gate helper under the
    one-sample-vs-0.50 statistic — strict '>' at the significance critical value and at the
    effect-size floor, inclusive '>=' at the games floor. All evidence is the trial's OWN
    (wins, games); there is no second arm."""

    def test_games_floor_is_inclusive(self):
        # Exactly min_games (30) passes the floor and (p = 1.0 -> effect 0.5, z ~= 5.48) adopts;
        # one game short (29) holds. Isolates the floor's inclusivity on the trial's own n.
        assert _adopt_by_significance(30, 30, 0.95, 0.01, 30) is True
        assert _adopt_by_significance(29, 29, 0.95, 0.01, 30) is False

    def test_effect_floor_is_strict(self):
        # Significant data (700/1000 -> effect 0.20 against the 0.50 null, z ~= 12.6). With
        # min_effect_size exactly == the effect the strict '>' holds; a hair below, it adopts.
        eff = 700 / 1000 - 0.5  # identical float to the helper's w_trial / n_trial - 0.5
        assert _adopt_by_significance(700, 1000, 0.95, eff, 30) is False
        assert _adopt_by_significance(700, 1000, 0.95, eff - 1e-9, 30) is True

    def test_significance_critical_value_is_strict(self):
        # Place z exactly at the critical value by setting confidence = cdf(z) (the same
        # round-trip identity as before, with the NULL standard error sqrt(0.25/n) substituted
        # for the old pooled SE) -> strict '>' holds; a slightly lower confidence adopts.
        # Effect (0.10) and games (100) clear their own gates, isolating the significance
        # boundary.
        from math import sqrt
        from statistics import NormalDist
        se = sqrt(0.25 / 100)
        z = (60 / 100 - 0.5) / se
        conf_at = NormalDist().cdf(z)
        assert _adopt_by_significance(60, 100, conf_at, 0.01, 30) is False
        assert _adopt_by_significance(60, 100, conf_at - 0.01, 0.01, 30) is True

    def test_holds_at_and_below_the_null(self):
        # T58 core semantics: a trial exactly AT the 0.50 null has effect 0.0 -> both conditions
        # hold it, at any n. A trial BELOW the null has a negative effect -> held at any n.
        assert _adopt_by_significance(500, 1000, 0.95, 0.01, 30) is False
        assert _adopt_by_significance(50000, 100000, 0.95, 0.01, 30) is False
        assert _adopt_by_significance(400, 1000, 0.95, 0.01, 30) is False
        assert _adopt_by_significance(1, 1000, 0.95, 0.01, 30) is False

    def test_adopts_on_a_significant_excess_over_the_null(self):
        # A genuine head-to-head excess at a realistic n: 0.60 over 1000 games -> effect 0.10,
        # z = 0.10 / sqrt(0.25/1000) ~= 6.32 > 1.645, effect > 0.01 -> ADOPT.
        assert _adopt_by_significance(600, 1000, 0.95, 0.01, 30) is True

    def test_no_zero_standard_error_case_exists(self):
        # T58/D3 replacement analysis for the deleted `if se == 0` guard: the NULL standard
        # error sqrt(0.25/n) is strictly positive for every n >= 1, so the degenerate pools that
        # zeroed the old POOLED SE (all-wins / all-losses) are ordinary inputs here — they
        # return a bool rather than raising ZeroDivisionError.
        assert _adopt_by_significance(60, 60, 0.95, 0.01, 30) is True    # p = 1.0
        assert _adopt_by_significance(0, 60, 0.95, 0.01, 30) is False    # p = 0.0
        # Smallest legal n: the point is that it RETURNS A BOOL rather than raising. It is
        # False, not True — at n = 1 even a maximal p = 1.0 gives z = 0.5 / sqrt(0.25/1) = 1.0,
        # which is below z_crit ~= 1.645. (Verified numerically, not assumed.)
        assert _adopt_by_significance(1, 1, 0.95, 0.01, 1) is False      # smallest legal n


class TestAdoptionGateIsStoreIndependent:
    """T58/D2 + AC1: the adoption gate reads ONLY the trial's fresh head-to-head evaluation.

    These are the decisive regressions for the store's demotion from gate input to
    record/report/promote surface. Each pre-seeds the store with accumulated totals that would
    have changed the OLD (pooled two-proportion, accumulated-evidence) decision, and asserts the
    new outcome is driven entirely by the fresh evaluation.
    """

    def test_pre_seeded_incumbent_totals_do_not_block_adoption(self, tmp_path):
        # Pre-seed the BASELINE (incumbent) combo with an overwhelming 0.95 accumulated rate over
        # 10000 games. Under the old pooled rule the trial's 0.70 would have had a NEGATIVE
        # effect against that incumbent and could never adopt. Under T58 the incumbent's totals
        # are not read at all, so the trial's fresh 0.70 (effect 0.20 over the 0.50 null) adopts.
        store = _store(tmp_path)
        baseline = _baseline()
        target = _max_pb(baseline)
        winner = dict(baseline)
        winner["PRIMARY_BONUS"] = target
        store.update("s1", baseline, 0.95, 9500, 10000)

        def wg(do, pv):
            return (700, 1000) if pv == winner else (500, 1000)

        t = SweepTournament(_wg_evaluator(wg), store)
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == target

    def test_best_rate_is_the_fresh_rate_not_the_accumulated_rate(self, tmp_path):
        # T58/R4 provenance. Pre-seed the WINNING combo with 0/1000 accumulated games, so after
        # this run's fresh 700/1000 evaluation its ACCUMULATED rate is 700/2000 = 0.35 while its
        # FRESH rate is 0.70. The reported win_rate must be the fresh 0.70 (the old code reported
        # the accumulated 0.35).
        store = _store(tmp_path)
        baseline = _baseline()
        target = _max_pb(baseline)
        winner = dict(baseline)
        winner["PRIMARY_BONUS"] = target
        store.update("s1", winner, 0.0, 0, 1000)

        def wg(do, pv):
            return (700, 1000) if pv == winner else (500, 1000)

        t = SweepTournament(_wg_evaluator(wg), store)
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == target
        assert result["s1"]["win_rate"] == pytest.approx(0.70)

    def test_store_still_records_every_evaluation(self, tmp_path):
        # T58/R3: the gate stops READING the store, but store.update(...) is retained — the
        # record / reporting / --promote surface is unchanged.
        store = _store(tmp_path)
        baseline = _baseline()
        t = SweepTournament(_wg_evaluator(lambda do, pv: (500, 1000)), store)
        t.run([("s1", [{"s": "1"}])], baseline)
        combos = store.get_all_combinations()
        assert len(combos) > 1  # the baseline anchor plus every swept candidate
        assert all(entry["total_games"] > 0 for entry in combos.values())


class TestAdoptionGateSampleSizeAndCost:
    """T58/AC2 + N1: the new gate fires at a SMALLER sample size than the old pooled rule, at
    unchanged simulation cost."""

    @staticmethod
    def _old_pooled_rule(w_trial, n_trial, w_best, n_best, confidence, min_effect_size,
                         min_games):
        """Frozen reference copy of the PRE-T58 pooled two-proportion gate.

        Deliberately duplicated here rather than imported: the production implementation is
        deleted by this story, and this copy exists only so the side-by-side AC2 comparison
        remains executable. It is never called by production code.
        """
        from math import sqrt
        from statistics import NormalDist
        if n_trial < min_games or n_best < min_games:
            return False
        effect = w_trial / n_trial - w_best / n_best
        p_pool = (w_trial + w_best) / (n_trial + n_best)
        se = sqrt(p_pool * (1.0 - p_pool) * (1.0 / n_trial + 1.0 / n_best))
        if se == 0:
            return False
        return effect / se > NormalDist().inv_cdf(confidence) and effect > min_effect_size

    def test_new_rule_fires_at_a_smaller_sample_size(self):
        # Fixed synthetic true effect: the trial wins 55% head-to-head against a 50% incumbent.
        # Sweep n upward and record the smallest n at which each rule first adopts. The new rule
        # needs only ONE arm's worth of variance, so it fires at roughly half the sample size.
        def smallest_n(fires):
            for n in range(DEFAULT_MIN_GAMES, 20001):
                if fires(n):
                    return n
            raise AssertionError("rule never fired below n = 20000")

        n_new = smallest_n(lambda n: _adopt_by_significance(
            round(0.55 * n), n, DEFAULT_CONFIDENCE, DEFAULT_MIN_EFFECT_SIZE, DEFAULT_MIN_GAMES
        ))
        n_old = smallest_n(lambda n: self._old_pooled_rule(
            round(0.55 * n), n, round(0.50 * n), n,
            DEFAULT_CONFIDENCE, DEFAULT_MIN_EFFECT_SIZE, DEFAULT_MIN_GAMES
        ))
        assert n_new < n_old
        # Recorded reference values at the committed constants: n_new = 261, n_old = 521.
        assert n_new == 261
        assert n_old == 521

    def test_evaluation_call_shape_is_unchanged(self, tmp_path):
        # T58/N1: exactly one evaluate() per trial plus the single baseline anchor — no second
        # arm, no extra evaluation. On a flat 0.50 landscape nothing adopts, so the ascent is a
        # single pass over every non-current candidate of every param.
        baseline = _baseline()
        ev = _wg_evaluator(lambda do, pv: (500, 1000))
        t = SweepTournament(ev, _store(tmp_path))
        t.run([("s1", [{"s": "1"}])], baseline)
        cands = generate_candidate_values(baseline, 5)
        expected = 1 + sum(
            len([v for v in cands[p] if v != baseline[p]]) for p in DRAFT_SWEEP_PARAMS
        )
        assert ev.evaluate.call_count == expected


class TestAdoptionGateFalseAdoptionRate:
    """T58/AC3: league-level synthetic-null false-adoption measurement for the one-sample gate.

    Pure-Python, fully seeded, offline — no simulation engine, no network. Each replication
    builds one evaluation's worth of evidence the way the real engine does: LEAGUES leagues,
    each contributing LEAGUE_GAMES correlated weekly outcomes drawn from that league's own
    latent quality, then aggregated to the game-level (wins, games) pair the gate actually
    receives. The trial is identically as strong as the incumbent, so every adoption is FALSE.

    Recorded results at SEED = 20260719, REPLICATIONS = 1200, LEAGUES = 60, LEAGUE_GAMES = 17
    (n = 1020 games per replication):
      - Arm (a), zero intra-league correlation: false-adoption rate = 4.83% against a nominal
        1 - DEFAULT_CONFIDENCE = 5% -> pass condition (a) satisfied.
      - Arm (b), positive intra-league correlation (per-league latent quality 0.5 +/- 0.10,
        intra-class correlation rho ~= 0.04, variance-inflation factor 1 + 16*rho ~= 1.64):
        false-adoption rate = 9.08% — roughly 2x nominal.

    Arm (b) is the QUANTIFIED anti-conservatism of the game-level sampling unit (spec D4). It is
    RECORDED, not a build failure: this is not a regression (the pre-T58 pooled z divided by the
    same inflated n), and the priced first correction is a league-level sampling unit, deferred
    to a follow-up story. Do NOT "fix" arm (b) by tightening the gate.
    """

    SEED = 20260719
    REPLICATIONS = 1200
    LEAGUES = 60
    LEAGUE_GAMES = 17

    def _false_adoption_rate(self, latent_delta):
        """Fraction of replications the gate falsely adopts under an exact 0.50 null.

        Args:
            latent_delta (float): Half-width of the per-league latent quality draw. 0.0 gives
                independent games (zero intra-league correlation); a positive value makes the
                LEAGUE_GAMES outcomes inside a league positively correlated while keeping the
                marginal win probability exactly 0.5.

        Returns:
            float: The observed false-adoption rate over REPLICATIONS replications.
        """
        rng = random.Random(self.SEED)
        games = self.LEAGUES * self.LEAGUE_GAMES
        adopted = 0
        for _ in range(self.REPLICATIONS):
            wins = 0
            for _ in range(self.LEAGUES):
                q = 0.5 + (latent_delta if rng.random() < 0.5 else -latent_delta)
                for _ in range(self.LEAGUE_GAMES):
                    if rng.random() < q:
                        wins += 1
            if _adopt_by_significance(
                wins, games, DEFAULT_CONFIDENCE, DEFAULT_MIN_EFFECT_SIZE, DEFAULT_MIN_GAMES
            ):
                adopted += 1
        return adopted / self.REPLICATIONS

    def test_pass_condition_a_uncorrelated_rate_at_or_below_nominal(self):
        # Zero intra-league correlation -> the game-level n is the true sample size, so the gate
        # should hold its nominal 1 - confidence = 5% false-adoption level. Monte-Carlo SE at
        # 1200 replications is ~0.0063; the bound below is nominal + ~4 SE.
        rate = self._false_adoption_rate(0.0)
        assert rate <= 0.075

    def test_pass_condition_b_correlated_rate_is_measured_and_inflated(self):
        # Positive intra-league correlation -> the game-level n overstates the true sample size,
        # so the gate is anti-conservative. This asserts only the DIRECTION and records the
        # magnitude in the class docstring and ARCHITECTURE Decision 6; it is not a nominal-level
        # gate, because exceeding 5% here is the documented D4 caveat, not a defect.
        rate_uncorrelated = self._false_adoption_rate(0.0)
        rate_correlated = self._false_adoption_rate(0.10)
        assert rate_correlated > rate_uncorrelated
        assert rate_correlated < 0.5  # sanity: still a null, not a broken generator


class TestSweepTerminatesUnderTheOneSampleGate:
    """T58/AC7: run() terminates under the one-sample gate — the explicit guard against the
    non-convergence hazard the statistic introduces.

    Convergence is run()'s ONLY stopping rule (a full pass that moves no parameter). Because the
    gate now compares against a FIXED 0.50 null rather than against the moving running-best, a
    landscape whose every combination sits above 0.50 would adopt forever. These tests pin the
    two shapes that must terminate: an at-the-null flat landscape, and a landscape with a single
    dominant winner.
    """

    def test_flat_null_landscape_terminates(self, tmp_path):
        baseline = _baseline()
        t = SweepTournament(_wg_evaluator(lambda do, pv: (500, 1000)), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline

    def test_single_winner_landscape_terminates_on_the_winner(self, tmp_path):
        baseline = _baseline()
        winner = dict(baseline)
        winner["PRIMARY_BONUS"] = _max_pb(baseline)
        t = SweepTournament(
            _wg_evaluator(lambda do, pv: (800, 1000) if pv == winner else (500, 1000)),
            _store(tmp_path),
        )
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == winner
        assert result["s1"]["win_rate"] == pytest.approx(0.80)

    def test_below_the_null_landscape_terminates_without_adopting(self, tmp_path):
        # Every combination is WORSE than the incumbent -> negative effect everywhere -> the gate
        # holds every candidate and the first pass converges on the baseline.
        baseline = _baseline()
        t = SweepTournament(_wg_evaluator(lambda do, pv: (300, 1000)), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline
