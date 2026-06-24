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
from typing import Dict, List, Tuple

# Local
from utils.LoggingManager import get_logger
from utils.error_handler import ConfigurationError
from simulation.win_rate.param_value_generation import generate_candidate_values, DRAFT_SWEEP_PARAMS

logger = get_logger()

# Coordinate-ascent improvement margin (D5): a param adopts a candidate only when it beats
# the config's current best win rate by more than this. Module-level so the driver's input
# fingerprint and the engine's ε-gate share one source of truth (no drift -> no spurious
# resume mismatch).
DEFAULT_EPSILON = 0.005


class SweepTournament:
    """
    Per-config convergent coordinate-ascent tournament over the 7 draft-side params.

    Each (strategy_id, draft_order) config is tuned independently: full coordinate-ascent
    passes (all 7 numerics each pass, holding the others at their current best) repeat to
    convergence under a strict ε-switch — a param adopts a candidate only when it beats the
    config's current best by more than ε. Convergence (a full pass that moves no parameter)
    is the sole stopping rule. The candidate grid is fixed per config (computed once from
    its baseline). Dependencies are injected so the tournament does no file/sim/config
    loading itself:

    Attributes:
        _evaluator: a CombinationEvaluator (evaluate(draft_order, param_values) ->
            (wins, games, win_rate)).
        _store: a SweepResultsManager (update(strategy_id, param_values, win_rate, wins, games)).
        _num_values: candidate count per numeric (passed to generate_candidate_values).
        _epsilon: ε win-rate margin; a param moves only when a candidate beats the config's
            current best by more than this (strict ε-switch).
    """

    def __init__(self, evaluator, store, num_values: int = 5, epsilon: float = DEFAULT_EPSILON) -> None:
        """
        Args:
            evaluator: CombinationEvaluator used to score each combination.
            store: SweepResultsManager used to record/accumulate every evaluation.
            num_values (int): Candidate values per numeric parameter (default 5).
            epsilon (float): ε win-rate margin (default DEFAULT_EPSILON = 0.005); a param moves
                only when a candidate beats the config's current best by more than this margin.
        """
        self._evaluator = evaluator
        self._store = store
        self._num_values = num_values
        self._epsilon = epsilon

    def run(
        self,
        strategies: List[Tuple[str, list]],
        baseline_params: Dict[str, float],
        resume: bool = False,
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

        Returns:
            Dict[str, Dict]: {strategy_id: {"param_values": <7-param dict>, "win_rate": float}}.

        Raises:
            ConfigurationError: If strategies is empty.
        """
        if not strategies:
            raise ConfigurationError("SweepTournament.run requires a non-empty strategies list")

        candidates = generate_candidate_values(baseline_params, self._num_values)  # KDD-3: fixed grid
        results: Dict[str, Dict] = {}

        for strategy_id, draft_order in strategies:
            # D3: when resuming, consult the per-config convergence to skip / seed.
            conv = self._store.get_config_convergence(strategy_id) if resume else None
            if conv is not None and conv.get("status") == "converged":
                logger.info(f"Config {strategy_id} skipped (already converged)")
                results[strategy_id] = {
                    "param_values": dict(conv["best_param_values"]),
                    "win_rate": conv["best_win_rate"],
                }
                continue
            if conv is not None and conv.get("status") == "in_progress":
                # Resume the interrupted config from its checkpointed best point (NOT re-evaluated).
                current = dict(conv["best_param_values"])
                best_rate = conv["best_win_rate"]
                # Re-record the seeded combo so it is present in the accumulating store.
                self._store.update(strategy_id, current, best_rate, 0, 0)
            else:
                # Per-config baseline evaluation establishes the starting best (also recorded).
                current = dict(baseline_params)
                wins, games, best_rate = self._evaluator.evaluate(draft_order, current)
                self._store.update(strategy_id, current, best_rate, wins, games)

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
                        if win_rate > best_rate + self._epsilon:   # KDD-2: strict ε-gate
                            best_rate = win_rate
                            current[param] = value
                            moved = True

            self._store.mark_config_progress(strategy_id, "converged", current, best_rate)
            results[strategy_id] = {"param_values": dict(current), "win_rate": best_rate}
            logger.info(f"Config {strategy_id} converged | win_rate={best_rate:.3f}")

        return results
