"""
Param Value Generation

Pure, deterministic candidate-value generation for the win-rate parameter sweep.
For each of the seven in-scope draft-side parameters, produces a list of discrete
values to test, evenly spaced across the parameter's [min, max] range at its
defined precision and always including the parameter's current value (the anchor).

No simulation, no file I/O, no randomness — identical inputs always yield identical
output, so sweeps using these domains are reproducible and resumable. Bounds and
precision come from ConfigGenerator.PARAM_DEFINITIONS; current values are supplied
by the caller (this module does not read league_config.json).

Author: Kai Mizuno
"""

# Standard library
from typing import Dict, List

# Local
from simulation.shared.ConfigGenerator import ConfigGenerator
from utils.error_handler import ConfigurationError


# The seven draft-side parameters this sweep optimizes (flat names matching
# ConfigGenerator.PARAM_DEFINITIONS).
DRAFT_SWEEP_PARAMS = (
    'DRAFT_NORMALIZATION_MAX_SCALE',
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    'PRIMARY_BONUS',
    'SECONDARY_BONUS',
    'ADP_SCORING_WEIGHT',
    'PLAYER_RATING_SCORING_WEIGHT',
)


def _discrete_grid(min_val: float, max_val: float, precision: int) -> List[float]:
    """Return every discrete value from min_val to max_val at the given precision."""
    step = 10 ** (-precision)
    values = []
    current = min_val
    while current <= max_val + step / 2:
        if precision > 0:
            values.append(round(current, precision))
        else:
            values.append(int(round(current)))
        current += step
    return values


def generate_candidate_values(
    current_values: Dict[str, float],
    num_values: int = 5,
) -> Dict[str, List[float]]:
    """
    Generate per-parameter candidate value lists for the sweep tournament.

    For each of the seven DRAFT_SWEEP_PARAMS, returns a sorted list of candidate
    values: num_values evenly spaced across the parameter's [min, max] range at its
    precision, plus the parameter's current value (anchor). When num_values is at
    least the number of discrete values in range, the full discrete set is returned;
    when num_values <= 1, only the anchor is returned.

    Args:
        current_values: Mapping of each of the seven flat param names to its current
            value (the anchor). Exactly the seven keys are required.
        num_values: Target number of evenly-spaced candidates per parameter
            (the anchor is added on top if not already among them).

    Returns:
        Dict[str, List[float]]: Each of the seven param names mapped to a sorted list
            of candidate values.

    Raises:
        ConfigurationError: If current_values is missing a required key, contains an
            unknown key, or carries a value outside the parameter's [min, max] bounds.
    """
    expected = set(DRAFT_SWEEP_PARAMS)
    provided = set(current_values)

    missing = expected - provided
    if missing:
        raise ConfigurationError(
            f"generate_candidate_values missing required param(s): {sorted(missing)}"
        )
    unknown = provided - expected
    if unknown:
        raise ConfigurationError(
            f"generate_candidate_values received unknown param(s): {sorted(unknown)}"
        )

    result: Dict[str, List[float]] = {}
    for name in DRAFT_SWEEP_PARAMS:
        min_val, max_val, precision = ConfigGenerator.PARAM_DEFINITIONS[name]
        raw = current_values[name]
        anchor = int(round(raw)) if precision == 0 else round(raw, precision)
        if anchor < min_val or anchor > max_val:
            raise ConfigurationError(
                f"{name}={raw} is outside bounds [{min_val}, {max_val}]"
            )

        grid = _discrete_grid(min_val, max_val, precision)
        if num_values >= len(grid):
            candidates = set(grid)
        elif num_values <= 1:
            candidates = {anchor}
        else:
            candidates = set()
            for i in range(num_values):
                idx = round(i * (len(grid) - 1) / (num_values - 1))
                candidates.add(grid[idx])

        candidates.add(anchor)
        result[name] = sorted(candidates)

    return result
