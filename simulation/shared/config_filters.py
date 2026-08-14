"""
Config Parameter Filters

Cross-simulation primitive: filter a full configuration dict down to the base
(non-week-specific) parameters enumerated in BASE_CONFIG_PARAMS, so the base
config file and the week config files each carry only the keys they own.

Consolidates the single "filter a config dict to base params" body that
previously lived inline in simulation/shared/ResultsManager._extract_base_params
(win-rate promote path). Its callers are that method, which still returns the
whole dict, and the accuracy promote path
(simulation/accuracy/AccuracyResultsManager.save_optimal_configs, which writes
the whole dict, and propagate_to_configs, which consumes only the returned
'parameters' block so the live file keeps the source's own metadata).

Author: Kai Mizuno
"""

from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.config_constants import BASE_CONFIG_PARAMS


def extract_base_params(config_dict: dict) -> dict:
    """Extract base (non-week-specific) parameters from a config.

    Args:
        config_dict: Full configuration dictionary. A missing 'parameters' key
            is treated as an empty parameter block.

    Returns:
        dict: Config dict carrying 'config_name', 'description', and a
            'parameters' block restricted to the BASE_CONFIG_PARAMS members
            present in the input (input order of BASE_CONFIG_PARAMS preserved).
    """
    params = config_dict.get('parameters', {})
    base_params = {
        key: params[key]
        for key in BASE_CONFIG_PARAMS
        if key in params
    }

    return {
        'config_name': config_dict.get('config_name', 'Optimal Base Config'),
        'description': 'Base configuration (non-week-specific parameters)',
        'parameters': base_params
    }
