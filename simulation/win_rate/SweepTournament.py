"""
Sweep Tournament

A per-draft-order-config convergent coordinate-ascent tournament over the 7 draft-side
params. For each (strategy_id, draft_order) config independently, it runs full
coordinate-ascent passes to convergence: each pass sweeps all 7 numerics (holding the
others at their current best), advancing a param to a candidate value only when that
candidate beats the config's current best win rate by more than the ε margin (a strict
ε-switch). Passes repeat until a full pass moves no parameter — convergence is the sole
stopping rule. The candidate grid is computed once per config from its baseline and
reused across passes (a fixed, finite search space).

Each combination is scored via an injected CombinationEvaluator (called sequentially)
and recorded into an injected SweepResultsManager. The authoritative ranked best is read
back from the accumulating store; the returned per-config map is a convenience handle
over the same recorded data. Re-running accumulates more evidence into the same store
records.

Author: Kai Mizuno
"""

# Standard library
from math import sqrt
from statistics import NormalDist
from typing import Callable, Dict, List, Optional, Tuple

# Local
from utils.LoggingManager import get_logger
from utils.error_handler import ConfigurationError
from simulation.win_rate.param_value_generation import generate_candidate_values, DRAFT_SWEEP_PARAMS

# Significance-gate parameters (D1/D2/D3/D5/D6). A trial param value is adopted only when its
# ACCUMULATED win rate (read back from the store) is both statistically significantly higher
# (one-sided pooled two-proportion z-test at DEFAULT_CONFIDENCE) AND higher by more than
# DEFAULT_MIN_EFFECT_SIZE than the running-best's accumulated rate; adoption is held until both
# combos have at least DEFAULT_MIN_GAMES accumulated games. Module-level so the driver's input
# fingerprint and the engine's gate share one source of truth (no drift -> no spurious resume
# mismatch).
DEFAULT_CONFIDENCE = 0.95
DEFAULT_MIN_EFFECT_SIZE = 0.01
DEFAULT_MIN_GAMES = 30


def _adopt_by_significance(
    w_trial: int,
    n_trial: int,
    w_best: int,
    n_best: int,
    confidence: float,
    min_effect_size: float,
    min_games: int,
) -> bool:
    """Decide whether a trial combination should be adopted over the running best.

    Applies the accumulated-evidence adoption gate (D1/D2/D5/D6): a one-sided pooled
    two-proportion z-test AND-ed with a minimum-effect-size guard, both over the
    accumulated wins/games of the two combinations, held below a minimum-games floor and
    on a degenerate (zero standard error) pool. Stdlib-only (``statistics.NormalDist``).

    Args:
        w_trial (int): Trial combination's accumulated wins.
        n_trial (int): Trial combination's accumulated games.
        w_best (int): Running-best combination's accumulated wins.
        n_best (int): Running-best combination's accumulated games.
        confidence (float): One-sided confidence level for the z critical value (0, 1).
        min_effect_size (float): Minimum accumulated-rate effect (p_trial - p_best) required.
        min_games (int): Minimum accumulated games required for BOTH combinations.

    Returns:
        bool: True iff (n_trial >= min_games and n_best >= min_games) and the pooled
            standard error is non-zero and z > z_crit and effect > min_effect_size.
    """
    if n_trial < min_games or n_best < min_games:
        return False  # D5: hold below the minimum-games floor (also guarantees n_* > 0)
    p_trial = w_trial / n_trial
    p_best = w_best / n_best
    effect = p_trial - p_best
    p_pool = (w_trial + w_best) / (n_trial + n_best)
    se = sqrt(p_pool * (1.0 - p_pool) * (1.0 / n_trial + 1.0 / n_best))
    if se == 0:
        return False  # D5: hold on a degenerate (all-wins / all-losses) pool — z undefined
    z = effect / se
    z_crit = NormalDist().inv_cdf(confidence)
    return z > z_crit and effect > min_effect_size  # D2/D6: AND-gate, both boundaries strict


class SweepTournament:
    """
    Per-config convergent coordinate-ascent tournament over the 7 draft-side params.

    Each (strategy_id, draft_order) config is tuned independently: full coordinate-ascent
    passes (all 7 numerics each pass, holding the others at their current best) repeat to
    convergence under a significance gate — a param adopts a candidate only when the
    candidate's ACCUMULATED win rate (read back from the store) is both significantly higher
    (one-sided pooled two-proportion z-test at the configured confidence) AND higher by more
    than the minimum effect size than the running-best's accumulated rate, with adoption held
    until both combos have at least min_games accumulated games. Convergence (a full pass that
    moves no parameter) is the sole stopping rule. The candidate grid is fixed per config
    (computed once from its baseline). Dependencies are injected so the tournament does no
    file/sim/config loading itself:

    Attributes:
        _evaluator: a CombinationEvaluator (evaluate(draft_order, param_values) ->
            (wins, games, win_rate)).
        _store: a SweepResultsManager (update(...) + get_combination(strategy_id, param_values)).
        _num_values: candidate count per numeric (passed to generate_candidate_values).
        _confidence: one-sided confidence level for the z critical value (0, 1).
        _min_effect_size: minimum accumulated-rate effect (p_trial - p_best) to adopt.
        _min_games: minimum accumulated games required of BOTH combos before a decision.
    """

    def __init__(
        self,
        evaluator,
        store,
        num_values: int = 5,
        confidence: float = DEFAULT_CONFIDENCE,
        min_effect_size: float = DEFAULT_MIN_EFFECT_SIZE,
        min_games: int = DEFAULT_MIN_GAMES,
    ) -> None:
        """
        Args:
            evaluator: CombinationEvaluator used to score each combination.
            store: SweepResultsManager used to record/accumulate every evaluation.
            num_values (int): Candidate values per numeric parameter (default 5).
            confidence (float): One-sided confidence level for the adoption z-test
                (default DEFAULT_CONFIDENCE = 0.95); must lie in the open interval (0, 1).
            min_effect_size (float): Minimum accumulated-rate effect (p_trial - p_best) a
                candidate must exceed to be adopted (default DEFAULT_MIN_EFFECT_SIZE = 0.01).
            min_games (int): Minimum accumulated games BOTH combos must reach before a
                candidate can be adopted (default DEFAULT_MIN_GAMES = 30).

        Raises:
            ConfigurationError: If confidence is not strictly within (0, 1).
            ConfigurationError: If min_games is less than 1.
            ConfigurationError: If min_effect_size is not in [0, 1).
        """
        if not 0 < confidence < 1:
            raise ConfigurationError(
                f"SweepTournament confidence must be in the open interval (0, 1); got {confidence!r}"
            )
        if min_games < 1:
            raise ConfigurationError(
                f"SweepTournament min_games must be a positive integer (>= 1); got {min_games!r}"
            )
        if not 0 <= min_effect_size < 1:
            raise ConfigurationError(
                f"SweepTournament min_effect_size must be in the interval [0, 1); got {min_effect_size!r}"
            )
        self._evaluator = evaluator
        self._store = store
        self._num_values = num_values
        self._confidence = confidence
        self._min_effect_size = min_effect_size
        self._min_games = min_games

    def _accumulated_rate(self, strategy_id: str, param_values: Dict[str, float]) -> float:
        """Return the store's accumulated win rate for one combination.

        Args:
            strategy_id (str): Strategy identifier keying the combination.
            param_values (Dict[str, float]): The 7 draft-side param values.

        Returns:
            float: total_wins / total_games for the combination, or 0.0 when the
                combination is unrecorded or has zero accumulated games.
        """
        entry = self._store.get_combination(strategy_id, param_values)
        if entry is None or entry["total_games"] == 0:
            return 0.0
        return entry["total_wins"] / entry["total_games"]

    def run(
        self,
        strategies: List[Tuple[str, list]],
        baseline_params: Dict[str, float],
        resume: bool = False,
        carry_over_seeds: Optional[Dict[str, Dict[str, float]]] = None,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> Dict[str, Dict]:
        """
        Run an independent convergent coordinate-ascent tournament for every draft-order
        config and return the per-config converged result map.

        Args:
            strategies: List of (strategy_id, draft_order) configs, each tuned independently.
            baseline_params: The 7 current draft-side param values (each config's anchor / start).
            resume: When True (D3), consult the injected store's per-config convergence to
                skip configs already marked "converged" and seed an "in_progress" config's
                start point from its checkpointed best values; configs with no convergence
                entry start from baseline. When False (default), every config starts from
                baseline (the pre-T9 behavior). Either way, per-config progress is written
                via the store's mark_config_progress so an interrupt leaves a resumable
                checkpoint.
            carry_over_seeds: When provided (T10/D1a — endless passes 2+ only), a per-config
                {strategy_id: best_param_values} map. A config with a seed starts its
                coordinate ascent from dict(seed) (not baseline), is evaluated ONCE to
                re-establish this pass's best_rate as the ε-gate baseline from fresh
                evidence (recorded via the existing store.update), is marked in_progress,
                and then tunes over the FULL grid — it is NOT skipped. Orthogonal to resume:
                the driver guarantees resume and carry_over_seeds are never both active in one
                pass (pass 1 -> resume=<decision>, carry_over_seeds=None; passes 2+ ->
                resume=False, carry_over_seeds=<map>), so conv is None whenever a seed fires.
                Configs with no seed fall back to the baseline start. Default None ->
                unchanged behavior.
            progress_callback: Optional callback invoked exactly once per config when that
                config reaches a terminal state — on BOTH the resume-skip ("already converged")
                path and the converged path — with the config's strategy_id. When None (the
                default), no progress signal is emitted and behavior is unchanged. The callback
                owns the per-config *progress* output (the TTY bar / non-TTY progress lines); the
                tournament itself does no console (stdout) I/O, though it still emits its own
                status lines (e.g. "Config ... converged") through the logger.

        Returns:
            Dict[str, Dict]: {strategy_id: {"param_values": <7-param dict>, "win_rate": float}}.

        Raises:
            ConfigurationError: If strategies is empty.
        """
        if not strategies:
            raise ConfigurationError("SweepTournament.run requires a non-empty strategies list")

        logger = get_logger()  # KDD-3: resolve at call time so --log-level governs this output

        candidates = generate_candidate_values(baseline_params, self._num_values)  # KDD-3: fixed grid
        results: Dict[str, Dict] = {}

        for strategy_id, draft_order in strategies:
            # D3: when resuming, consult the per-config convergence to skip / seed.
            conv = self._store.get_config_convergence(strategy_id) if resume else None
            if conv is not None and conv.get("status") == "converged":
                logger.info(f"Config {strategy_id} skipped (already converged)")
                results[strategy_id] = {
                    "param_values": dict(conv["best_param_values"]),
                    # D4: new key, else legacy best_win_rate (old-schema resume safety).
                    "win_rate": conv.get("best_combo_win_rate", conv.get("best_win_rate")),
                }
                if progress_callback is not None:  # KDD-2: fire on the resume-skip path
                    progress_callback(strategy_id)
                continue
            if conv is not None and conv.get("status") == "in_progress":
                # Resume the interrupted config from its checkpointed best point (NOT re-evaluated).
                # The seed combo already exists in the persisted store from the prior run, so we do
                # NOT re-record it — a 0-win/0-game update() would bump total_runs / last_run with
                # zero evidence and skew the per-combo metadata on every resume (PR #18).
                current = dict(conv["best_param_values"])
                # D4: new key, else legacy best_win_rate (old-schema resume safety).
                best_rate = conv.get("best_combo_win_rate", conv.get("best_win_rate"))
            elif carry_over_seeds is not None and strategy_id in carry_over_seeds:
                # T10/D1a: seed-and-tune from a prior pass's converged params (endless passes 2+).
                # Unlike the in_progress resume branch, the seed is evaluated ONCE here to
                # re-establish THIS pass's running-best baseline from fresh evidence (the
                # evaluator is non-deterministic and the store accumulates games), recording it
                # via the existing update(). best_rate (T31/F7) is the seed combo's ACCUMULATED
                # rate read back from the store. The config then falls through to the full
                # coordinate-ascent below — it is NOT skipped and the grid is unchanged.
                current = dict(carry_over_seeds[strategy_id])
                wins, games, win_rate = self._evaluator.evaluate(draft_order, current)
                self._store.update(strategy_id, current, win_rate, wins, games)
                best_rate = self._accumulated_rate(strategy_id, current)
            else:
                # Per-config baseline evaluation establishes the starting best (also recorded).
                # best_rate (T31/F7) is the baseline combo's ACCUMULATED rate from the store.
                current = dict(baseline_params)
                wins, games, win_rate = self._evaluator.evaluate(draft_order, current)
                self._store.update(strategy_id, current, win_rate, wins, games)
                best_rate = self._accumulated_rate(strategy_id, current)

            # Record in-progress so an interrupt at any point leaves a resumable checkpoint (D3).
            self._store.mark_config_progress(strategy_id, "in_progress", current, best_rate)

            # Loop full coordinate-ascent passes until a pass moves no parameter (convergence
            # is the sole stopping rule — no wall-time, no pass cap).
            moved = True
            while moved:
                moved = False
                for param in DRAFT_SWEEP_PARAMS:           # all 7 swept every pass
                    for value in candidates[param]:
                        if value == current[param]:
                            continue                       # current best already recorded
                        trial = dict(current)
                        trial[param] = value
                        wins, games, win_rate = self._evaluator.evaluate(draft_order, trial)
                        self._store.update(strategy_id, trial, win_rate, wins, games)
                        # T31: decide adoption on ACCUMULATED evidence read back from the store
                        # (D4) — the trial combo (just update()-ed) vs the running-best (current).
                        # best_entry is None only when the running-best combo has no accumulated
                        # evidence this run (e.g. a checkpoint-seeded resume whose seed combo was
                        # not re-recorded, per PR #18) — treat that as below the floor and hold.
                        trial_entry = self._store.get_combination(strategy_id, trial)
                        best_entry = self._store.get_combination(strategy_id, current)
                        if best_entry is not None and _adopt_by_significance(
                            trial_entry["total_wins"], trial_entry["total_games"],
                            best_entry["total_wins"], best_entry["total_games"],
                            self._confidence, self._min_effect_size, self._min_games,
                        ):
                            current[param] = value
                            # After adoption current == trial, so the new running-best's
                            # accumulated rate (F7) is the trial entry's rate; the floor in the
                            # gate guarantees total_games >= min_games > 0 (divide-safe).
                            best_rate = trial_entry["total_wins"] / trial_entry["total_games"]
                            moved = True
                            # Persist the new running best immediately, so an interrupt mid-ascent
                            # leaves the LATEST values on disk (not the stale seed) and a resume
                            # restarts from them rather than losing this run's progress (PR #18).
                            self._store.mark_config_progress(
                                strategy_id, "in_progress", current, best_rate
                            )

            self._store.mark_config_progress(strategy_id, "converged", current, best_rate)
            results[strategy_id] = {"param_values": dict(current), "win_rate": best_rate}
            logger.info(f"Config {strategy_id} converged | win_rate={best_rate:.3f}")
            if progress_callback is not None:  # KDD-2: fire on the converged path
                progress_callback(strategy_id)

        return results
