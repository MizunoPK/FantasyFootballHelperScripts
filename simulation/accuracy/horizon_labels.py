"""
Accuracy Horizon Labels

Single definition of the accuracy simulation's weekly horizon set, its
cardinality, and the operator-facing label strings that report it.

Consolidates the horizon-count claims that previously each restated their own
literal: the CLI banner (run_accuracy_simulation.main), the manager's startup
log (AccuracySimulationManager.__init__), and the parallel runner's evaluation
log (ParallelAccuracyRunner.evaluate_configs_parallel), whose count had drifted
to five after the ROS horizon was removed at c3a6c86b. WEEK_RANGES itself moved
here from AccuracyResultsManager, which now re-exports it, and replaces the
function-local copy the parallel runner's worker carried. Each consumer keeps
its own emission shape - two print() calls, one prefixed logger.info(), one
evaluation log line - so only the label text and the count are shared.

This module imports typing and nothing else on purpose:
ParallelAccuracyRunner._evaluate_config_tournament_process is a
ProcessPoolExecutor entry point, so every worker process pays these imports.

Author: Kai Mizuno
"""

from typing import Dict, Tuple

WEEK_RANGES: Dict[str, Tuple[int, int]] = {
    'week_1_5': (1, 5),
    'week_6_9': (6, 9),
    'week_10_13': (10, 13),
    'week_14_17': (14, 17),
}

HORIZON_COUNT = len(WEEK_RANGES)


def candidate_values_label(candidate_values: int) -> str:
    """Build the shared 'candidate values per parameter' banner label.

    Args:
        candidate_values: Number of candidate values tested per parameter per
            horizon (num_test_values + 1, including the baseline value).

    Returns:
        str: The label text, thousands-separated, carrying no leading prefix
            and no trailing punctuation so each consumer supplies its own
            line shape.
    """
    return f"Candidate values per parameter per horizon: {candidate_values:,}"


def configs_per_param_label(candidate_values: int, configs_per_param: int) -> str:
    """Build the shared 'configs per horizon-specific parameter' banner label.

    Args:
        candidate_values: Number of candidate values tested per parameter per
            horizon.
        configs_per_param: Total configs generated for one horizon-specific
            parameter (candidate_values * HORIZON_COUNT).

    Returns:
        str: The label text, thousands-separated, with the horizon count taken
            from HORIZON_COUNT so it can never disagree with WEEK_RANGES.
    """
    return (
        f"Configs per horizon-specific parameter: {candidate_values:,} "
        f"× {HORIZON_COUNT} horizons = {configs_per_param:,}"
    )
