"""
Config Overrides

Pure helpers for the win-rate parameter sweep: apply a draft strategy plus
concrete values for the seven in-scope draft-side league_config parameters onto
a base config, producing a new config the simulation can evaluate. No I/O and no
simulation execution happen here.

Key responsibilities:
- Map each flat sweep-parameter name to its nested location under
  config["parameters"].
- Validate each value against the shared ConfigGenerator bounds and round it to
  the defined precision before writing.
- Return a deep copy so the caller's base config is never mutated.

Author: Kai Mizuno
"""

# Standard library
import copy
from typing import Dict, List

# Local
from simulation.shared.ConfigGenerator import ConfigGenerator
from utils.error_handler import ConfigurationError


# Maps each flat sweep-parameter name (matching ConfigGenerator.PARAM_DEFINITIONS)
# to its location under config["parameters"]: (section_key, leaf_key). A leaf of
# None means section_key is itself the top-level scalar to write.
DRAFT_PARAM_LOCATIONS = {
    'DRAFT_NORMALIZATION_MAX_SCALE': ('DRAFT_NORMALIZATION_MAX_SCALE', None),
    'SAME_POS_BYE_WEIGHT': ('SAME_POS_BYE_WEIGHT', None),
    'DIFF_POS_BYE_WEIGHT': ('DIFF_POS_BYE_WEIGHT', None),
    'PRIMARY_BONUS': ('DRAFT_ORDER_BONUSES', 'PRIMARY'),
    'SECONDARY_BONUS': ('DRAFT_ORDER_BONUSES', 'SECONDARY'),
    'ADP_SCORING_WEIGHT': ('ADP_SCORING', 'WEIGHT'),
    'PLAYER_RATING_SCORING_WEIGHT': ('PLAYER_RATING_SCORING', 'WEIGHT'),
}


def apply_draft_overrides(
    base_config: dict,
    draft_order: List[dict],
    param_values: Dict[str, float],
) -> dict:
    """
    Return a deep copy of base_config with DRAFT_ORDER and the seven draft-side
    parameters set to the supplied values.

    Each value is validated against ConfigGenerator.PARAM_DEFINITIONS bounds and
    rounded to the defined precision before being written to its nested location
    under config["parameters"]. The input base_config is never mutated.

    Args:
        base_config: Full config dict containing a "parameters" object, e.g. the
            contents of league_config.json.
        draft_order: The strategy's DRAFT_ORDER list, written verbatim. Structural
            validation of DRAFT_ORDER is the strategy loader's responsibility, not
            this function's.
        param_values: Exactly the seven keys in DRAFT_PARAM_LOCATIONS, each mapped
            to a numeric value.

    Returns:
        dict: A new config dict with the overrides applied.

    Raises:
        ConfigurationError: If param_values is missing a required key, contains an
            unknown key, or carries a value outside the parameter's [min, max]
            bounds.
    """
    expected = set(DRAFT_PARAM_LOCATIONS)
    provided = set(param_values)

    missing = expected - provided
    if missing:
        raise ConfigurationError(
            f"apply_draft_overrides missing required param(s): {sorted(missing)}"
        )
    unknown = provided - expected
    if unknown:
        raise ConfigurationError(
            f"apply_draft_overrides received unknown param(s): {sorted(unknown)}"
        )

    config = copy.deepcopy(base_config)
    params = config["parameters"]
    params["DRAFT_ORDER"] = copy.deepcopy(draft_order)

    for name, (section, leaf) in DRAFT_PARAM_LOCATIONS.items():
        min_val, max_val, precision = ConfigGenerator.PARAM_DEFINITIONS[name]
        value = param_values[name]

        if value < min_val or value > max_val:
            raise ConfigurationError(
                f"{name}={value} is outside bounds [{min_val}, {max_val}]"
            )

        rounded = int(round(value)) if precision == 0 else round(value, precision)

        if leaf is None:
            params[section] = rounded
        else:
            params[section][leaf] = rounded

    return config


def extract_draft_param_values(config: dict) -> Dict[str, float]:
    """
    Read the current value of each of the 7 draft-side params from a config.

    The inverse of apply_draft_overrides: for each flat param name in
    DRAFT_PARAM_LOCATIONS, read its value from config["parameters"] at the mapped
    (section, leaf) location.

    Args:
        config: Full config dict containing a "parameters" object.

    Returns:
        Dict[str, float]: Each of the 7 flat param names mapped to its current value.
    """
    params = config["parameters"]
    return {
        name: (params[section] if leaf is None else params[section][leaf])
        for name, (section, leaf) in DRAFT_PARAM_LOCATIONS.items()
    }
