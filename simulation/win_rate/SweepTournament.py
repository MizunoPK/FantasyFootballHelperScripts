"""
Sweep Tournament

The per-parameter tournament that searches the (strategy + 7 draft-side params) space
for a single global-best combination, within budget. It locks the best strategy at
baseline param values, then sweeps each of the 7 numerics once (greedy coordinate
descent, holding the others at their current best), evaluating each combination via an
injected CombinationEvaluator and recording every result into an injected
SweepResultsManager.

Single-pass design (mirrors the accuracy sim's run_both). The tournament explores and
records; the authoritative ranked best is read back from the accumulating store via
sweep_summary. Re-running accumulates more evidence into the same store records.

Author: Kai Mizuno
"""

# Standard library
from typing import Dict, List, Tuple

# Local
from utils.LoggingManager import get_logger
from utils.error_handler import ConfigurationError
from simulation.win_rate.param_value_generation import generate_candidate_values, DRAFT_SWEEP_PARAMS

logger = get_logger()


class SweepTournament:
    """
    Single-pass per-parameter tournament over the (strategy + 7 params) space.

    Dependencies are injected so the tournament does no file/sim/config loading itself:

    Attributes:
        _evaluator: a CombinationEvaluator (evaluate(draft_order, param_values) ->
            (wins, games, win_rate)).
        _store: a SweepResultsManager (update(strategy_id, param_values, win_rate, wins, games)).
        _num_values: candidate count per numeric (passed to generate_candidate_values).
    """

    def __init__(self, evaluator, store, num_values: int = 5) -> None:
        """
        Args:
            evaluator: CombinationEvaluator used to score each combination.
            store: SweepResultsManager used to record/accumulate every evaluation.
            num_values (int): Candidate values per numeric parameter (default 5).
        """
        self._evaluator = evaluator
        self._store = store
        self._num_values = num_values

    def run(
        self,
        strategies: List[Tuple[str, list]],
        baseline_params: Dict[str, float],
    ) -> Dict:
        """
        Run the single-pass tournament and return the greedy-converged best combination.

        Args:
            strategies: List of (strategy_id, draft_order) to consider for the strategy lock.
            baseline_params: The 7 current draft-side param values (the anchor / starting point).

        Returns:
            Dict: {"strategy_id", "param_values", "win_rate"} for the converged best.

        Raises:
            ConfigurationError: If strategies is empty.
        """
        if not strategies:
            raise ConfigurationError("SweepTournament.run requires a non-empty strategies list")

        # Phase 1 — lock the best strategy at baseline params.
        best_strategy_id = None
        best_draft_order = None
        current_rate = -1.0
        for strategy_id, draft_order in strategies:
            wins, games, win_rate = self._evaluator.evaluate(draft_order, baseline_params)
            self._store.update(strategy_id, baseline_params, win_rate, wins, games)
            if win_rate > current_rate:
                current_rate = win_rate
                best_strategy_id = strategy_id
                best_draft_order = draft_order

        logger.info(f"Locked best strategy: {best_strategy_id} (baseline win_rate={current_rate:.3f})")

        # Phase 2 — single greedy sweep of the 7 numerics, holding others at current best.
        candidates = generate_candidate_values(baseline_params, self._num_values)
        current = dict(baseline_params)
        for param in DRAFT_SWEEP_PARAMS:
            for value in candidates[param]:
                trial = dict(current)
                trial[param] = value
                wins, games, win_rate = self._evaluator.evaluate(best_draft_order, trial)
                self._store.update(best_strategy_id, trial, win_rate, wins, games)
                if win_rate > current_rate:
                    current_rate = win_rate
                    current[param] = value

        logger.info(f"Tournament best: {best_strategy_id} | win_rate={current_rate:.3f}")
        return {
            "strategy_id": best_strategy_id,
            "param_values": current,
            "win_rate": current_rate,
        }
