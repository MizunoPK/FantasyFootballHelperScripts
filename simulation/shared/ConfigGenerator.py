"""
Configuration Generator

Generates parameter candidate values for simulation optimization. Each parameter gets
N+1 values (the baseline optimal + N random variations), N = num_test_values (default: 5).

The accuracy tournament optimizes one parameter at a time: a horizon-specific parameter
yields an independent N+1 array per weekly horizon; a shared parameter yields a single array.

Parameters Varied (with ranges):

Base Config Parameters:
  1. NORMALIZATION_MAX_SCALE: [50, 200] - Point spread scaling
  2. SAME_POS_BYE_WEIGHT: [0.0, 1.0] - Same position bye penalty
  3. DIFF_POS_BYE_WEIGHT: [0.0, 0.5] - Different position bye penalty
  4. PRIMARY_BONUS: [25, 150] - Primary draft order bonus
  5. SECONDARY_BONUS: [25, 150] - Secondary draft order bonus
  6. DRAFT_ORDER_FILE: [1, 100] - Draft strategy file (discrete)
  7. ADP_SCORING_WEIGHT: [0.5, 7.0] - ADP influence weight
  8. ADP_SCORING_STEPS: [5, 50] - ADP picks per tier

Week-Specific Parameters:
  9. PLAYER_RATING_SCORING_WEIGHT: [0.5, 4.0] - Expert ranking weight
  10. TEAM_QUALITY_SCORING_WEIGHT: [0.0, 4.0] - Team strength weight
  11. TEAM_QUALITY_MIN_WEEKS: [1, 12] - Min weeks of team data
  12. PERFORMANCE_SCORING_WEIGHT: [0.0, 8.0] - Performance deviation weight
  13. PERFORMANCE_SCORING_STEPS: [0.01, 0.3] - Deviation % per tier
  14. PERFORMANCE_MIN_WEEKS: [1, 14] - Min weeks of performance data
  15. MATCHUP_IMPACT_SCALE: [25, 250] - Matchup additive impact max
  16. MATCHUP_SCORING_WEIGHT: [0.0, 4.0] - Matchup weight
  17. MATCHUP_MIN_WEEKS: [1, 14] - Min weeks of matchup data
  18. TEMPERATURE_IMPACT_SCALE: [0, 200] - Temperature impact max
  19. TEMPERATURE_SCORING_WEIGHT: [0.0, 3.0] - Temperature weight
  20. WIND_IMPACT_SCALE: [0, 150] - Wind impact max
  21. WIND_SCORING_WEIGHT: [0.0, 4.0] - Wind weight
  22. LOCATION_HOME: [-5, 15] - Home field modifier
  23. LOCATION_AWAY: [-15, 5] - Away game modifier
  24. LOCATION_INTERNATIONAL: [-25, 5] - International game modifier

Note: SCHEDULE_SCORING is disabled (not optimized)

Author: Kai Mizuno
"""

import json
import random
import copy
from pathlib import Path
from typing import List, Dict

from utils.LoggingManager import get_logger
from simulation.shared.config_constants import BASE_CONFIG_PARAMS, WEEK_SPECIFIC_PARAMS

# Default seed for the accuracy engine's private candidate-value RNG (T51). A fixed
# default makes the plain `run_accuracy_simulation.py` command reproducible run-to-run;
# the `--seed N` CLI flag overrides it. 42 matches the value the existing suite already
# uses for candidate generation. Mirrors the win-rate private-RNG pattern
# (simulation/win_rate/SimulatedLeague.py) but diverges (approved) on the default:
# win-rate defaults to None/OS-entropy for deliberate Monte-Carlo exploration, whereas
# the accuracy tournament requires default reproducibility.
DEFAULT_ACCURACY_SEED = 42


class ConfigGenerator:
    """
    Generates configuration combinations for simulation optimization.

    Attributes:
        baseline_configs (dict): Per-horizon baseline configurations, keyed by horizon
            ('1-5', '6-9', '10-13', '14-17')
        param_definitions (dict): Parameter ranges and bounds
        logger: Logger instance
    """

    PARAM_DEFINITIONS = {
        'NORMALIZATION_MAX_SCALE': (50, 200, 0),
        # Deliberately excluded from run_accuracy_simulation.py's PARAMETER_ORDER: it
        # scales draft scores, not the week-to-week projection accuracy the tournament
        # measures, so --params rejects it by design. No sweep tunes it (the win-rate
        # sweep excludes it as inert); the range stays because it is live in
        # league_helper/util/player_scoring.py as the is_draft_mode counterpart of
        # NORMALIZATION_MAX_SCALE.
        'DRAFT_NORMALIZATION_MAX_SCALE': (100, 200, 0),

        'SAME_POS_BYE_WEIGHT': (0.0, 1.0, 2),
        'DIFF_POS_BYE_WEIGHT': (0.0, 0.5, 2),

        'PRIMARY_BONUS': (25, 150, 0),
        'SECONDARY_BONUS': (25, 150, 0),

        'DRAFT_ORDER_FILE': (1, 100, 0),

        'ADP_SCORING_WEIGHT': (0.50, 7.00, 2),
        'ADP_SCORING_STEPS': (5, 50, 0),

        'PLAYER_RATING_SCORING_WEIGHT': (0.50, 4.00, 2),

        'TEAM_QUALITY_SCORING_WEIGHT': (0.00, 4.00, 2),
        'TEAM_QUALITY_MIN_WEEKS': (1, 12, 0),

        'PERFORMANCE_SCORING_WEIGHT': (0.00, 8.00, 2),
        'PERFORMANCE_SCORING_STEPS': (0.01, 0.30, 2),
        'PERFORMANCE_MIN_WEEKS': (1, 14, 0),

        'MATCHUP_IMPACT_SCALE': (25, 250, 0),
        'MATCHUP_SCORING_WEIGHT': (0.0, 4.0, 2),
        'MATCHUP_MIN_WEEKS': (1, 14, 0),

        'TEMPERATURE_IMPACT_SCALE': (0.0, 200.0, 0),
        'TEMPERATURE_SCORING_WEIGHT': (0.0, 3.0, 2),

        'WIND_IMPACT_SCALE': (0.0, 150.0, 0),
        'WIND_SCORING_WEIGHT': (0.0, 4.0, 2),

        'LOCATION_HOME': (-5.0, 15.0, 1),
        'LOCATION_AWAY': (-15.0, 5.0, 1),
        'LOCATION_INTERNATIONAL': (-25.0, 5.0, 1),
    }

    SCORING_SECTIONS = [
        'ADP_SCORING',
        'PLAYER_RATING_SCORING',
        'PERFORMANCE_SCORING',
        'MATCHUP_SCORING',
        'TEMPERATURE_SCORING',
        'WIND_SCORING',
    ]

    PARAM_TO_SECTION_MAP = {
        'NORMALIZATION_MAX_SCALE': 'NORMALIZATION_MAX_SCALE',
        'DRAFT_NORMALIZATION_MAX_SCALE': 'DRAFT_NORMALIZATION_MAX_SCALE',
        'SAME_POS_BYE_WEIGHT': 'SAME_POS_BYE_WEIGHT',
        'DIFF_POS_BYE_WEIGHT': 'DIFF_POS_BYE_WEIGHT',
        'PRIMARY_BONUS': 'DRAFT_ORDER_BONUSES',
        'SECONDARY_BONUS': 'DRAFT_ORDER_BONUSES',
        'DRAFT_ORDER_FILE': 'DRAFT_ORDER_FILE',
        'ADP_SCORING_WEIGHT': 'ADP_SCORING',
        'ADP_SCORING_STEPS': 'ADP_SCORING',
        'PLAYER_RATING_SCORING_WEIGHT': 'PLAYER_RATING_SCORING',
        'TEAM_QUALITY_SCORING_WEIGHT': 'TEAM_QUALITY_SCORING',
        'TEAM_QUALITY_MIN_WEEKS': 'TEAM_QUALITY_SCORING',
        'PERFORMANCE_SCORING_WEIGHT': 'PERFORMANCE_SCORING',
        'PERFORMANCE_SCORING_STEPS': 'PERFORMANCE_SCORING',
        'PERFORMANCE_MIN_WEEKS': 'PERFORMANCE_SCORING',
        'MATCHUP_IMPACT_SCALE': 'MATCHUP_SCORING',
        'MATCHUP_SCORING_WEIGHT': 'MATCHUP_SCORING',
        'MATCHUP_MIN_WEEKS': 'MATCHUP_SCORING',
        'TEMPERATURE_IMPACT_SCALE': 'TEMPERATURE_SCORING',
        'TEMPERATURE_SCORING_WEIGHT': 'TEMPERATURE_SCORING',
        'WIND_IMPACT_SCALE': 'WIND_SCORING',
        'WIND_SCORING_WEIGHT': 'WIND_SCORING',
        'LOCATION_HOME': 'LOCATION_MODIFIERS',
        'LOCATION_AWAY': 'LOCATION_MODIFIERS',
        'LOCATION_INTERNATIONAL': 'LOCATION_MODIFIERS',
    }

    def is_base_param(self, param_name: str) -> bool:
        """
        Check if a parameter belongs to the base config (not week-specific).

        Args:
            param_name (str): Parameter name from PARAMETER_ORDER

        Returns:
            bool: True if parameter belongs to base config, False otherwise

        Example:
            >>> gen.is_base_param('SAME_POS_BYE_WEIGHT')
            True
            >>> gen.is_base_param('NORMALIZATION_MAX_SCALE')
            False
        """
        if param_name not in self.PARAM_TO_SECTION_MAP:
            self.logger.warning(f"Unknown parameter: {param_name}")
            return False

        section = self.PARAM_TO_SECTION_MAP[param_name]
        return section in BASE_CONFIG_PARAMS

    @staticmethod
    def load_baseline_from_folder(folder_path: Path) -> Dict[str, dict]:
        """
        Load baseline configurations from a folder with 5-file structure.

        Loads all config files and creates 4 separate weekly horizon configs:
        - league_config.json (base parameters shared by all horizons)
        - week1-5.json, week6-9.json, week10-13.json, week14-17.json (week-specific params)

        Each horizon config = league_config.json + its horizon-specific file.
        NO merging across horizons - each horizon has independent baseline.

        Args:
            folder_path (Path): Path to folder containing config files

        Returns:
            Dict[str, dict]: 4 horizon configs with keys: '1-5', '6-9', '10-13', '14-17'

        Raises:
            ValueError: If folder doesn't exist or required files are missing

        Example:
            >>> configs = ConfigGenerator.load_baseline_from_folder(Path("data/configs"))
            >>> configs['1-5']['parameters']['PLAYER_RATING_SCORING']
            {'WEIGHT': 2.0}
        """
        logger = get_logger()
        folder_path = Path(folder_path)

        if not folder_path.exists():
            raise ValueError(f"Config folder does not exist: {folder_path}")

        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")

        required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']
        missing_files = []

        for filename in required_files:
            if not (folder_path / filename).exists():
                missing_files.append(filename)

        if missing_files:
            raise ValueError(
                f"Missing required config files in {folder_path}: {', '.join(missing_files)}"
            )

        base_config_path = folder_path / 'league_config.json'
        with open(base_config_path, 'r') as f:
            base_config = json.load(f)

        logger.debug(f"Loaded base config from {base_config_path}")

        horizon_files = {
            '1-5': 'week1-5.json',
            '6-9': 'week6-9.json',
            '10-13': 'week10-13.json',
            '14-17': 'week14-17.json'
        }

        horizon_configs = {}
        for horizon, filename in horizon_files.items():
            file_path = folder_path / filename
            with open(file_path, 'r') as f:
                horizon_specific = json.load(f)
            logger.debug(f"Loaded {filename} for horizon '{horizon}'")

            merged_config = copy.deepcopy(base_config)
            if 'parameters' not in merged_config:
                merged_config['parameters'] = {}

            horizon_params = horizon_specific.get('parameters', {})
            merged_config['parameters'].update(horizon_params)

            merged_config['config_name'] = horizon_specific.get('config_name', f'Horizon {horizon}')
            merged_config['description'] = horizon_specific.get('description', f'Config for horizon {horizon}')

            horizon_configs[horizon] = merged_config

        logger.info(f"Loaded 5 horizon configs from folder: {folder_path}")
        return horizon_configs

    def __init__(self, baseline_config_path: Path, num_test_values: int = 5, seed: int = DEFAULT_ACCURACY_SEED) -> None:
        """
        Initialize ConfigGenerator with baseline configuration from a folder.

        The baseline must be a folder containing the 5-file config structure:
        - league_config.json (base parameters shared by all horizons)
        - week1-5.json, week6-9.json, week10-13.json, week14-17.json (week-specific params)

        Args:
            baseline_config_path (Path): Path to config folder (NOT a single JSON file)
            num_test_values (int): Number of random values to generate per parameter (default: 5)
                This creates (num_test_values + 1) total values per parameter (optimal + random)
            seed (int): Seed for the private candidate-value RNG (default: DEFAULT_ACCURACY_SEED).
                A fixed default makes candidate generation reproducible run-to-run; pass a
                different value (e.g. via the accuracy sim's --seed flag) for a different
                reproducible candidate set.

        Raises:
            ValueError: If path is a file instead of folder, or folder is missing required files

        Note:
            parameter_order and num_parameters_to_test removed - now passed to
            generate_horizon_test_values() instead. Only single-parameter optimization supported.
        """
        self.logger = get_logger()
        baseline_config_path = Path(baseline_config_path)

        if baseline_config_path.is_file():
            raise ValueError(
                f"ConfigGenerator requires a folder path, not a file: {baseline_config_path}\n"
                f"Expected folder structure with: league_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json"
            )

        self.logger.info(f"Initializing ConfigGenerator with baseline folder: {baseline_config_path}")
        self.logger.info(f"Test values per parameter: {num_test_values} (total values: {num_test_values + 1})")

        self.baseline_configs = self.load_baseline_from_folder(baseline_config_path)
        self.param_definitions = self.PARAM_DEFINITIONS
        self.num_test_values = num_test_values
        self.baseline_folder = baseline_config_path
        # Private per-generator RNG (T51): isolates candidate draws from the process-global
        # `random` module so accuracy config selection is deterministic run-to-run. Mirrors
        # SimulatedLeague._rng (simulation/win_rate/SimulatedLeague.py:120).
        self._rng = random.Random(seed)

        self._cached_test_values = {}
        self._current_param = None

        self.logger.info("ConfigGenerator initialized successfully with 5 horizon configs")

    def generate_horizon_test_values(self, param_name: str) -> Dict[str, List[float]]:
        """
        Generate test values for a parameter across horizons.

        Auto-detects if parameter is shared (BASE_CONFIG_PARAMS) or horizon-specific
        (WEEK_SPECIFIC_PARAMS) and returns appropriate structure:

        - Shared params: {'shared': [baseline, test1, test2, ...]}
          → Single array tested across all 4 weekly horizons

        - Horizon params: {'1-5': [...], '6-9': [...], '10-13': [...], '14-17': [...]}
          → 4 independent arrays for tournament optimization

        Args:
            param_name (str): Parameter name from PARAM_DEFINITIONS

        Returns:
            Dict[str, List[float]]: Test values keyed by 'shared' or horizon names

        Example:
            >>> gen.generate_horizon_test_values('ADP_SCORING_WEIGHT')
            {'shared': [1.5, 2.3, 0.9, 3.1, ...]}  # Shared param

            >>> gen.generate_horizon_test_values('PLAYER_RATING_SCORING_WEIGHT')
            {'1-5': [2.0, 2.5, ...], '6-9': [2.0, 2.8, ...], ...}  # Horizon param
        """
        if param_name not in self.PARAM_DEFINITIONS:
            raise ValueError(f"Unknown parameter: {param_name}")

        if param_name != self._current_param:
            self._cached_test_values = {}
            self._current_param = param_name

        if param_name in self._cached_test_values:
            return self._cached_test_values[param_name]

        is_shared = self.is_base_param(param_name)

        min_val, max_val, precision = self.PARAM_DEFINITIONS[param_name]

        if is_shared:
            baseline_value = self._extract_param_value(self.baseline_configs['1-5'], param_name)
            test_values = self._generate_test_values_array(baseline_value, min_val, max_val, precision)
            result = {'shared': test_values}
        else:
            result = {}
            for horizon in ['1-5', '6-9', '10-13', '14-17']:
                baseline_value = self._extract_param_value(self.baseline_configs[horizon], param_name)
                test_values = self._generate_test_values_array(baseline_value, min_val, max_val, precision)
                result[horizon] = test_values

        self._cached_test_values[param_name] = result
        return result

    def get_config_for_horizon(self, horizon: str, param_name: str, test_index: int) -> dict:
        """
        Get complete config for a horizon with test value applied.

        Args:
            horizon (str): Horizon name ('1-5', '6-9', '10-13', '14-17')
            param_name (str): Parameter being tested
            test_index (int): Index into test values array

        Returns:
            dict: Complete configuration dictionary with test value applied

        Example:
            >>> config = gen.get_config_for_horizon('1-5', 'ADP_SCORING_WEIGHT', 2)
            >>> config['parameters']['ADP_SCORING']['WEIGHT']
            2.35  # Test value at index 2
        """
        if horizon not in self.baseline_configs:
            raise ValueError(f"Invalid horizon: {horizon}. Must be one of: {list(self.baseline_configs.keys())}")

        test_values = self.generate_horizon_test_values(param_name)

        is_shared = 'shared' in test_values
        if is_shared:
            value_array = test_values['shared']
        else:
            value_array = test_values[horizon]

        if test_index < 0 or test_index >= len(value_array):
            raise IndexError(f"test_index {test_index} out of range for {len(value_array)} values")

        test_value = value_array[test_index]

        config = copy.deepcopy(self.baseline_configs[horizon])
        self._apply_param_value(config, param_name, test_value)

        return config

    def update_baseline_for_horizon(self, horizon: str, new_config: dict) -> None:
        """
        Update baseline configuration after finding optimal value.

        Behavior depends on parameter type:
        - Shared params: Updates league_config portion in ALL 4 weekly horizons
        - Horizon params: Updates only the specified horizon

        Args:
            horizon (str): Horizon that found the optimal value
            new_config (dict): New configuration with optimal parameter value

        Example:
            >>> gen.update_baseline_for_horizon('1-5', optimal_config)
        """
        if horizon not in self.baseline_configs:
            raise ValueError(f"Invalid horizon: {horizon}")


        new_params = new_config.get('parameters', {})

        shared_params_changed = {}
        for param in BASE_CONFIG_PARAMS:
            if param in new_params:
                old_val = self.baseline_configs[horizon]['parameters'].get(param)
                new_val = new_params[param]
                if old_val != new_val:
                    shared_params_changed[param] = new_val

        if shared_params_changed:
            for h in ['1-5', '6-9', '10-13', '14-17']:
                for param, value in shared_params_changed.items():
                    self.baseline_configs[h]['parameters'][param] = copy.deepcopy(value)
            self.logger.debug(f"Updated shared params {list(shared_params_changed.keys())} in all horizons")

        horizon_params_changed = {}
        for param in WEEK_SPECIFIC_PARAMS:
            if param in new_params:
                old_val = self.baseline_configs[horizon]['parameters'].get(param)
                new_val = new_params[param]
                if old_val != new_val:
                    horizon_params_changed[param] = new_val

        if horizon_params_changed:
            for param, value in horizon_params_changed.items():
                self.baseline_configs[horizon]['parameters'][param] = copy.deepcopy(value)
            self.logger.debug(f"Updated horizon params {list(horizon_params_changed.keys())} in horizon '{horizon}'")

    def _extract_param_value(self, config: dict, param_name: str) -> float:
        """Extract parameter value from config, handling nested structures."""
        section = self.PARAM_TO_SECTION_MAP.get(param_name)
        if not section:
            raise ValueError(f"Unknown parameter: {param_name}")

        params = config.get('parameters', {})

        if section == param_name:
            return params.get(param_name, 0.0)

        section_data = params.get(section, {})
        if not isinstance(section_data, dict):
            raise ValueError(f"Section {section} is not a dict")

        if param_name.endswith('_WEIGHT'):
            return section_data.get('WEIGHT', 0.0)
        elif param_name.endswith('_STEPS'):
            return section_data.get('STEPS', 0)
        elif param_name.endswith('_MIN_WEEKS'):
            return section_data.get('MIN_WEEKS', 0)
        elif param_name.endswith('_IMPACT_SCALE'):
            return section_data.get('IMPACT_SCALE', 0.0)
        elif param_name == 'PRIMARY_BONUS':
            return section_data.get('PRIMARY', 0)
        elif param_name == 'SECONDARY_BONUS':
            return section_data.get('SECONDARY', 0)
        elif param_name.startswith('LOCATION_'):
            location_type = param_name.replace('LOCATION_', '')
            return section_data.get(location_type, 0.0)
        else:
            raise ValueError(f"Unknown param structure for {param_name}")

    def _apply_param_value(self, config: dict, param_name: str, value: float) -> None:
        """Apply parameter value to config, handling nested structures."""
        section = self.PARAM_TO_SECTION_MAP.get(param_name)
        if not section:
            raise ValueError(f"Unknown parameter: {param_name}")

        params = config.get('parameters', {})

        if section == param_name:
            params[param_name] = value
            return

        if section not in params:
            params[section] = {}

        section_data = params[section]

        if param_name.endswith('_WEIGHT'):
            section_data['WEIGHT'] = value
        elif param_name.endswith('_STEPS'):
            section_data['STEPS'] = int(value)
        elif param_name.endswith('_MIN_WEEKS'):
            section_data['MIN_WEEKS'] = int(value)
        elif param_name.endswith('_IMPACT_SCALE'):
            section_data['IMPACT_SCALE'] = value
        elif param_name == 'PRIMARY_BONUS':
            section_data['PRIMARY'] = value
        elif param_name == 'SECONDARY_BONUS':
            section_data['SECONDARY'] = value
        elif param_name.startswith('LOCATION_'):
            location_type = param_name.replace('LOCATION_', '')
            section_data[location_type] = value
        else:
            raise ValueError(f"Unknown param structure for {param_name}")

    def _generate_test_values_array(self, baseline: float, min_val: float, max_val: float, precision: int) -> List[float]:
        """Generate array of test values: [baseline, random1, random2, ...]"""
        values = [baseline]

        for _ in range(self.num_test_values):
            if precision == 0:
                val = self._rng.randint(int(min_val), int(max_val))
            else:
                val = self._rng.uniform(min_val, max_val)
                val = round(val, precision)
            values.append(val)

        return values


