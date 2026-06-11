"""
Budget Sizing

Sizes a win-rate parameter sweep to fit an overnight wall-time budget. Measures a
per-sim cost on the host (timing one real evaluation), then computes the pass sizing —
sims-per-combination and test-values-per-param — that fits the budget by fixing
num_values and maximizing num_simulations (per-combination confidence).

The estimate uses combinations = num_strategies + 7 * num_values, each combination
costing num_simulations sims, at the measured wall-seconds per sim (parallel workers and
season count are baked into the measured cost). The estimate is a target, not a
guarantee — the sweep is interruptible and accumulating.

Author: Kai Mizuno
"""

# Standard library
import time
from typing import Dict

# Local
from utils.error_handler import ConfigurationError

DEFAULT_NUM_VALUES = 5
MIN_SIMULATIONS = 20  # matches DraftStrategyOrchestrator.LOW_SIM_THRESHOLD
DEFAULT_BUDGET_SECONDS = 8 * 3600  # overnight: 8 hours

# Number of draft-side numeric parameters swept (DRAFT_SWEEP_PARAMS).
_NUM_SWEEP_PARAMS = 7


def measure_unit_cost(evaluator, draft_order, param_values, sims_per_eval: int) -> float:
    """
    Measure wall-seconds per sim per combination by timing one real evaluation.

    The evaluator must be constructed with num_simulations == sims_per_eval; this times a
    single evaluate() (which runs sims_per_eval sims across all seasons with parallel
    workers) and divides by sims_per_eval, so worker parallelism and season count are
    baked into the returned figure.

    Args:
        evaluator: A CombinationEvaluator constructed with num_simulations = sims_per_eval.
        draft_order: A strategy DRAFT_ORDER to evaluate.
        param_values: The 7 draft-side param values.
        sims_per_eval (int): Sims the evaluator runs per evaluation (its num_simulations).

    Returns:
        float: Measured wall-seconds per sim per combination.

    Raises:
        ConfigurationError: If sims_per_eval <= 0.
    """
    if sims_per_eval <= 0:
        raise ConfigurationError(f"sims_per_eval must be positive, got {sims_per_eval}")
    start = time.monotonic()
    evaluator.evaluate(draft_order, param_values)
    elapsed = time.monotonic() - start
    return elapsed / sims_per_eval


def compute_sizing(
    unit_cost: float,
    num_strategies: int,
    num_values: int = DEFAULT_NUM_VALUES,
    budget_seconds: float = DEFAULT_BUDGET_SECONDS,
    min_simulations: int = MIN_SIMULATIONS,
) -> Dict:
    """
    Compute the pass sizing that fits the budget: fix num_values, maximize num_simulations.

    Args:
        unit_cost (float): Wall-seconds per sim per combination (from measure_unit_cost).
        num_strategies (int): Number of strategies the tournament locks over.
        num_values (int): Candidate values per numeric (fixed; default DEFAULT_NUM_VALUES).
        budget_seconds (float): Wall-time budget (default DEFAULT_BUDGET_SECONDS).
        min_simulations (int): Statistical floor for num_simulations (default MIN_SIMULATIONS).

    Returns:
        Dict: {"num_simulations", "num_values", "estimated_seconds", "feasible"}.
            feasible is False when even min_simulations exceeds the budget (num_simulations
            is then min_simulations and estimated_seconds exceeds budget_seconds).

    Raises:
        ConfigurationError: If unit_cost <= 0 or the combination count is non-positive.
    """
    combinations = num_strategies + _NUM_SWEEP_PARAMS * num_values
    if unit_cost <= 0:
        raise ConfigurationError(f"unit_cost must be positive, got {unit_cost}")
    if combinations <= 0:
        raise ConfigurationError(
            f"combination count must be positive (num_strategies={num_strategies}, "
            f"num_values={num_values})"
        )

    max_sims = int(budget_seconds / (combinations * unit_cost))
    feasible = max_sims >= min_simulations
    num_simulations = max_sims if feasible else min_simulations
    estimated_seconds = combinations * num_simulations * unit_cost

    return {
        "num_simulations": num_simulations,
        "num_values": num_values,
        "estimated_seconds": estimated_seconds,
        "feasible": feasible,
    }
