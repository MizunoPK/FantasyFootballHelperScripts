"""
Configuration Generator

Generates parameter combinations for simulation optimization. Creates combinations
by varying 23 key parameters, with N+1 values per parameter (optimal + N random variations).

Total configurations = (N+1)^23 where N = num_test_values (default: 5)
For practical use, iterative optimization tests one parameter at a time.

Parameters Varied (with ranges):

Base Config Parameters:
  1. NORMALIZATION_MAX_SCALE: [50, 200] - Point spread scaling
  2. SAME_POS_BYE_WEIGHT: [0.0, 0.5] - Same position bye penalty
  3. DIFF_POS_BYE_WEIGHT: [0.0, 0.3] - Different position bye penalty
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
from itertools import product

from utils.LoggingManager import get_logger
from simulation.shared.config_constants import BASE_CONFIG_PARAMS, WEEK_SPECIFIC_PARAMS


class ConfigGenerator:
    """
    Generates configuration combinations for simulation optimization.

    Attributes:
        baseline_config (dict): Base configuration to vary from
        param_definitions (dict): Parameter ranges and bounds
        logger: Logger instance
    """

    PARAM_DEFINITIONS = {
        'NORMALIZATION_MAX_SCALE': (50, 200, 0),
        # DRAFT_NORMALIZATION_MAX_SCALE controls draft-score scale, not week-to-week
        # accuracy — excluded from PARAMETER_ORDER but range defined for --params testing.
        'DRAFT_NORMALIZATION_MAX_SCALE': (100, 200, 0),

        'SAME_POS_BYE_WEIGHT': (0.0, 0.5, 2),
        'DIFF_POS_BYE_WEIGHT': (0.0, 0.3, 2),

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

    THRESHOLD_FIXED_PARAMS = {
        "ADP_SCORING": {
            "BASE_POSITION": 0,
            "DIRECTION": "DECREASING"
        },
        "PLAYER_RATING_SCORING": {
            "BASE_POSITION": 0,
            "DIRECTION": "INCREASING"
        },
        "TEAM_QUALITY_SCORING": {
            "BASE_POSITION": 0,
            "DIRECTION": "DECREASING"
        },
        "PERFORMANCE_SCORING": {
            "BASE_POSITION": 0.0,
            "DIRECTION": "BI_EXCELLENT_HI"
        },
        "MATCHUP_SCORING": {
            "BASE_POSITION": 0,
            "DIRECTION": "INCREASING"
        },
        "TEMPERATURE_SCORING": {
            "BASE_POSITION": 0,
            "DIRECTION": "DECREASING",
            "STEPS": 10,
            "IDEAL_TEMPERATURE": 60
        },
        "WIND_SCORING": {
            "BASE_POSITION": 0,
            "DIRECTION": "DECREASING",
            "STEPS": 8
        }
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

    def is_week_specific_param(self, param_name: str) -> bool:
        """
        Check if a parameter belongs to week-specific configs.

        Args:
            param_name (str): Parameter name from PARAMETER_ORDER

        Returns:
            bool: True if parameter is week-specific, False otherwise

        Example:
            >>> gen.is_week_specific_param('NORMALIZATION_MAX_SCALE')
            True
            >>> gen.is_week_specific_param('SAME_POS_BYE_WEIGHT')
            False
        """
        if param_name not in self.PARAM_TO_SECTION_MAP:
            self.logger.warning(f"Unknown parameter: {param_name}")
            return False

        section = self.PARAM_TO_SECTION_MAP[param_name]
        return section in WEEK_SPECIFIC_PARAMS

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

    def __init__(self, baseline_config_path: Path, num_test_values: int = 5) -> None:
        """
        Initialize ConfigGenerator with baseline configuration from a folder.

        The baseline must be a folder containing the 5-file config structure:
        - league_config.json (base parameters shared by all horizons)
        - week1-5.json, week6-9.json, week10-13.json, week14-17.json (week-specific params)

        Args:
            baseline_config_path (Path): Path to config folder (NOT a single JSON file)
            num_test_values (int): Number of random values to generate per parameter (default: 5)
                This creates (num_test_values + 1) total values per parameter (optimal + random)

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

        self._cached_test_values = {}
        self._current_param = None

        self.logger.info("ConfigGenerator initialized successfully with 5 horizon configs")

    @property
    def baseline_config(self) -> dict:
        """
        Backward compatibility property for old tests.
        Returns a unified config merged from all horizons (uses '1-5' as base).

        DEPRECATED: Use baseline_configs dict instead for horizon-specific access.
        """
        return self.baseline_configs.get('1-5', {})

    @property
    def parameter_order(self) -> List[str]:
        """
        Backward compatibility property for old tests.

        DEPRECATED: parameter_order is no longer stored in ConfigGenerator.
        Returns empty list.
        """
        return []

    def load_baseline_config(self, json_path: Path) -> dict:
        """
        Load baseline configuration from JSON file.

        Args:
            json_path (Path): Path to JSON config file

        Returns:
            dict: Full configuration dictionary

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If JSON is invalid
        """
        self.logger.debug(f"Loading baseline config from {json_path}")

        with open(json_path, 'r') as f:
            config = json.load(f)

        if 'parameters' not in config:
            raise ValueError("Config missing 'parameters' section")

        self.logger.debug(f"Loaded config: {config.get('config_name', 'Unknown')}")
        return config

    def _generate_discrete_range(
        self,
        min_val: float,
        max_val: float,
        precision: int
    ) -> List[float]:
        """
        Generate all possible discrete values at given precision.

        Args:
            min_val (float): Minimum value
            max_val (float): Maximum value
            precision (int): Decimal places (0=integers, 1=0.1 steps, 2=0.01 steps)

        Returns:
            List[float]: All possible values from min to max at given precision

        Example:
            >>> gen._generate_discrete_range(0.0, 0.5, 1)
            [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
            >>> gen._generate_discrete_range(100, 105, 0)
            [100, 101, 102, 103, 104, 105]
        """
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

    def generate_parameter_values(
        self,
        param_name: str,
        optimal_val: float,
        min_val: float,
        max_val: float,
        precision: int
    ) -> List[float]:
        """
        Generate discrete parameter values at specified precision level.

        Values are selected from discrete set derived from (min, max, precision).
        When num_test_values >= possible values, returns ALL values with optimal first.
        Otherwise returns optimal + random sample from remaining values.

        Args:
            param_name (str): Parameter name (for logging)
            optimal_val (float): Optimal/baseline value
            min_val (float): Minimum allowed value
            max_val (float): Maximum allowed value
            precision (int): Decimal places (0=integers, 1=0.1 steps, 2=0.01 steps)

        Returns:
            List[float]: Values with optimal first, then additional test values

        Example:
            >>> gen = ConfigGenerator(baseline_path, parameter_order, num_test_values=5)
            >>> # Precision 1 (0.1 steps) with 6 possible values [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
            >>> values = gen.generate_parameter_values('SAME_POS_BYE_WEIGHT', 0.3, 0.0, 0.5, 1)
            >>> # Returns [0.3, 0.0, 0.1, 0.2, 0.4, 0.5] (all 6 values, optimal first)
        """
        possible_values = self._generate_discrete_range(min_val, max_val, precision)

        if precision > 0:
            optimal_rounded = round(optimal_val, precision)
        else:
            optimal_rounded = int(round(optimal_val))

        if self.num_test_values >= len(possible_values):
            if optimal_rounded in possible_values:
                values = [optimal_rounded] + [v for v in possible_values if v != optimal_rounded]
            else:
                values = [optimal_rounded] + possible_values
            self.logger.debug(f"{param_name}: {len(values)} values (all discrete, optimal first)")
            return values
        else:
            values = [optimal_rounded]
            remaining = [v for v in possible_values if v != optimal_rounded]
            num_to_sample = min(self.num_test_values, len(remaining))
            if num_to_sample > 0:
                values.extend(random.sample(remaining, num_to_sample))
            self.logger.debug(f"{param_name}: {len(values)} values (subset of {len(possible_values)} possible)")
            return values

    def _load_draft_order_from_file(self, file_num: int) -> list:
        """
        Load DRAFT_ORDER array from numbered file.

        Args:
            file_num (int): File number (1-30)

        Returns:
            list: DRAFT_ORDER array from the file

        Raises:
            FileNotFoundError: If no matching file found
        """
        draft_order_dir = Path(__file__).parent.parent / "sim_data" / "draft_order_possibilities"

        matches = list(draft_order_dir.glob(f"{file_num}_*.json"))
        if not matches:
            matches = list(draft_order_dir.glob(f"{file_num}.json"))

        if not matches:
            raise FileNotFoundError(f"No draft order file found for number {file_num} in {draft_order_dir}")

        with open(matches[0], 'r') as f:
            data = json.load(f)

        self.logger.debug(f"Loaded DRAFT_ORDER from {matches[0].name}")
        return data['DRAFT_ORDER']

    def generate_multiplier_parameter_values(
        self,
        value_sets : Dict[str, List[float]],
        param_name: str
    ) -> Dict[str, List[float]]:
        base_weight = self.baseline_config['parameters'][param_name]["WEIGHT"]
        full_name = f"{param_name}_WEIGHT"
        min_val, max_val, precision = self.param_definitions[full_name]
        value_sets[full_name] = self.generate_parameter_values(full_name, base_weight, min_val, max_val, precision)

        return value_sets

    def generate_all_parameter_value_sets(self) -> Dict[str, List[float]]:
        """
        Generate value sets for all 13 parameters (5 scalar + 5 weights + 2 threshold STEPS + 1 IMPACT_SCALE).

        Returns:
            Dict[str, List[float]]: {param_name: [N+1 values]} where N = num_test_values

        Example:
            >>> gen = ConfigGenerator(baseline_path, parameter_order, num_test_values=5)
            >>> value_sets = gen.generate_all_parameter_value_sets()
            >>> value_sets['NORMALIZATION_MAX_SCALE']
            [100.0, 94.3, 118.7, 83.2, 105.9, 112.1]  # 6 values
            >>> value_sets['ADP_SCORING_STEPS']
            [37.5, 32.1, 42.8, 30.5, 45.2, 39.1]  # 6 values
        """
        self.logger.info("Generating value sets for all parameters")

        value_sets = {}
        params = self.baseline_config['parameters']

        value_sets['NORMALIZATION_MAX_SCALE'] = self.generate_parameter_values(
            'NORMALIZATION_MAX_SCALE',
            params['NORMALIZATION_MAX_SCALE'],
            *self.param_definitions['NORMALIZATION_MAX_SCALE']
        )

        value_sets['SAME_POS_BYE_WEIGHT'] = self.generate_parameter_values(
            'SAME_POS_BYE_WEIGHT',
            params['SAME_POS_BYE_WEIGHT'],
            *self.param_definitions['SAME_POS_BYE_WEIGHT']
        )

        value_sets['DIFF_POS_BYE_WEIGHT'] = self.generate_parameter_values(
            'DIFF_POS_BYE_WEIGHT',
            params['DIFF_POS_BYE_WEIGHT'],
            *self.param_definitions['DIFF_POS_BYE_WEIGHT']
        )

        value_sets['PRIMARY_BONUS'] = self.generate_parameter_values(
            'PRIMARY_BONUS',
            params['DRAFT_ORDER_BONUSES']['PRIMARY'],
            *self.param_definitions['PRIMARY_BONUS']
        )

        value_sets['SECONDARY_BONUS'] = self.generate_parameter_values(
            'SECONDARY_BONUS',
            params['DRAFT_ORDER_BONUSES']['SECONDARY'],
            *self.param_definitions['SECONDARY_BONUS']
        )

        value_sets = self.generate_multiplier_parameter_values(value_sets, "ADP_SCORING")

        value_sets = self.generate_multiplier_parameter_values(value_sets, "PLAYER_RATING_SCORING")

        value_sets = self.generate_multiplier_parameter_values(value_sets, "TEAM_QUALITY_SCORING")

        value_sets = self.generate_multiplier_parameter_values(value_sets, "PERFORMANCE_SCORING")

        value_sets = self.generate_multiplier_parameter_values(value_sets, "MATCHUP_SCORING")


        for scoring_type in ["ADP_SCORING", "PERFORMANCE_SCORING"]:
            steps_param = f"{scoring_type}_STEPS"
            if 'STEPS' in params[scoring_type]['THRESHOLDS']:
                current_steps = params[scoring_type]['THRESHOLDS']['STEPS']
                min_val, max_val, precision = self.param_definitions[steps_param]
                value_sets[steps_param] = self.generate_parameter_values(
                    steps_param,
                    current_steps,
                    min_val,
                    max_val,
                    precision
                )

        for scoring_type in ["MATCHUP_SCORING"]:
            impact_param = scoring_type.replace('_SCORING', '_IMPACT_SCALE')
            current_impact = params[scoring_type]['IMPACT_SCALE']
            min_val, max_val, precision = self.param_definitions[impact_param]
            value_sets[impact_param] = self.generate_parameter_values(
                impact_param,
                current_impact,
                min_val,
                max_val,
                precision
            )

        for scoring_type in ["TEAM_QUALITY_SCORING", "PERFORMANCE_SCORING", "MATCHUP_SCORING"]:
            min_weeks_param = scoring_type.replace('_SCORING', '_MIN_WEEKS')
            current_min_weeks = params[scoring_type].get('MIN_WEEKS', 5)
            min_val, max_val, precision = self.param_definitions[min_weeks_param]
            value_sets[min_weeks_param] = self.generate_parameter_values(
                min_weeks_param,
                current_min_weeks,
                min_val,
                max_val,
                precision
            )

        for section in ['TEMPERATURE', 'WIND']:
            scoring_key = f'{section}_SCORING'
            if scoring_key in params:
                impact_param = f'{section}_IMPACT_SCALE'
                if impact_param in self.param_definitions:
                    current_impact = params[scoring_key].get('IMPACT_SCALE', 50.0)
                    min_val, max_val, precision = self.param_definitions[impact_param]
                    value_sets[impact_param] = self.generate_parameter_values(
                        impact_param, current_impact, min_val, max_val, precision
                    )

                weight_param = f'{section}_SCORING_WEIGHT'
                if weight_param in self.param_definitions:
                    current_weight = params[scoring_key].get('WEIGHT', 1.0)
                    min_val, max_val, precision = self.param_definitions[weight_param]
                    value_sets[weight_param] = self.generate_parameter_values(
                        weight_param, current_weight, min_val, max_val, precision
                    )

        location_modifiers = params.get('LOCATION_MODIFIERS', {})
        for loc_type in ['HOME', 'AWAY', 'INTERNATIONAL']:
            param_name = f'LOCATION_{loc_type}'
            if param_name in self.param_definitions:
                defaults = {'HOME': 2.0, 'AWAY': -2.0, 'INTERNATIONAL': -5.0}
                current_val = location_modifiers.get(loc_type, defaults[loc_type])
                min_val, max_val, precision = self.param_definitions[param_name]
                value_sets[param_name] = self.generate_parameter_values(
                    param_name, current_val, min_val, max_val, precision
                )

        self.logger.info(f"Generated {len(value_sets)} parameter value sets")
        return value_sets

    def generate_all_combinations(self) -> List[Dict[str, float]]:
        """
        Generate all parameter combinations using itertools.product.

        Returns:
            List[Dict[str, float]]: All combinations, each a dict with 13 params

        Example:
            >>> combinations = gen.generate_all_combinations()
            >>> combinations[0]
            {'NORMALIZATION_MAX_SCALE': 100.0, 'ADP_SCORING_WEIGHT': 1.94, ...}
        """
        self.logger.info("Generating all parameter combinations")

        value_sets = self.generate_all_parameter_value_sets()

        param_names = list(value_sets.keys())
        param_value_lists = [value_sets[name] for name in param_names]

        combinations = []
        for combo_values in product(*param_value_lists):
            combo_dict = dict(zip(param_names, combo_values))
            combinations.append(combo_dict)

        self.logger.info(f"Generated {len(combinations)} combinations")

        return combinations
    
    def generate_iterative_combinations(self, param_name: str, base_config: dict) -> List[dict]:
        """
        Generate configs for iterative optimization with random parameter exploration.

        Creates configs for:
        1. Base parameter (provided param_name)
        2. NUM_PARAMETERS_TO_TEST - 1 randomly selected parameters
        3. Cartesian product of all parameter values (all combinations)

        Args:
            param_name (str): Base parameter to optimize
            base_config (dict): Current optimal configuration

        Returns:
            List[dict]: Complete configs ready for simulation

        Example:
            With NUM_PARAMETERS_TO_TEST=2, N=5:
            - Base param: 6 individual configs
            - 1 random param: 6 individual configs
            - Cartesian combinations: 6^2 = 36 combination configs
            - Total: 48 configs

        Raises:
            ValueError: If param_name not in PARAMETER_ORDER
        """
        if param_name not in self.parameter_order:
            raise ValueError(f"Unknown parameter: {param_name}")

        num_params_to_test = self.num_parameters_to_test
        if num_params_to_test < 1:
            self.logger.warning(f"num_parameters_to_test={num_params_to_test} is invalid, defaulting to 1")
            num_params_to_test = 1

        max_params = len(self.parameter_order)
        if num_params_to_test > max_params:
            self.logger.info(f"num_parameters_to_test={num_params_to_test} exceeds available parameters ({max_params}), capping at {max_params}")
            num_params_to_test = max_params

        num_values = self.num_test_values + 1
        expected_combinations = num_values ** num_params_to_test
        if expected_combinations > 1000:
            self.logger.warning(
                f"Cartesian product will generate {expected_combinations:,} combination configs. "
                f"This may impact performance. Consider reducing NUM_PARAMETERS_TO_TEST or num_test_values."
            )

        self.logger.info(f"Generating configs with cartesian product strategy for {num_params_to_test} parameters")

        num_random = num_params_to_test - 1
        random_params = []

        if num_random > 0:
            available_params = [p for p in self.parameter_order if p != param_name]
            random_params = random.sample(available_params, num_random)
            self.logger.info(f"Selected {num_random} random parameters: {random_params}")
        else:
            self.logger.info("NUM_PARAMETERS_TO_TEST=1, testing only base parameter (no random selection)")

        all_params = [param_name] + random_params
        param_configs = {}

        base_configs = self.generate_single_parameter_configs(param_name, base_config)
        param_configs[param_name] = base_configs

        for random_param in random_params:
            configs = self.generate_single_parameter_configs(random_param, base_config)
            param_configs[random_param] = configs

        combination_configs = []

        if num_params_to_test > 1:
            param_values = {}
            for param in all_params:
                param_values[param] = []
                for config in param_configs[param]:
                    combination = self._extract_combination_from_config(config)
                    param_values[param].append(combination[param])

            value_lists = [param_values[p] for p in all_params]

            for value_tuple in product(*value_lists):
                combination = self._extract_combination_from_config(base_config)

                for param, value in zip(all_params, value_tuple):
                    combination[param] = value

                config = self.create_config_dict(combination)
                combination_configs.append(config)

        all_configs = []

        for param in all_params:
            all_configs.extend(param_configs[param])

        all_configs.extend(combination_configs)

        random_param_str = ', '.join(random_params) if random_params else 'none'
        individual_count = sum(len(param_configs[p]) for p in all_params)

        self.logger.info(
            f"Generated {len(all_configs)} total configs:\n"
            f"  - Base parameter ({param_name}): {len(param_configs[param_name])} configs\n"
            f"  - Random parameters ({random_param_str}): {individual_count - len(param_configs[param_name])} configs\n"
            f"  - Combination configs: {len(combination_configs)} configs"
        )

        return all_configs

    def generate_single_parameter_configs(
        self,
        param_name: str,
        base_config: dict
    ) -> List[dict]:
        """
        Generate configs varying only a single parameter for iterative optimization.

        Args:
            param_name (str): Parameter name from PARAMETER_ORDER
            base_config (dict): Base configuration to vary from

        Returns:
            List[dict]: List of configs with only param_name varied

        Example:
            >>> configs = gen.generate_single_parameter_configs(
            ...     'NORMALIZATION_MAX_SCALE',
            ...     current_optimal_config
            ... )
            >>> len(configs)  # num_test_values + 1
            6
        """
        self.logger.info(f"Generating configs for parameter: {param_name}")

        params = base_config['parameters']

        if param_name == 'NORMALIZATION_MAX_SCALE':
            current_val = params['NORMALIZATION_MAX_SCALE']
            min_val, max_val, precision = self.param_definitions['NORMALIZATION_MAX_SCALE']
        elif param_name == 'SAME_POS_BYE_WEIGHT':
            current_val = params['SAME_POS_BYE_WEIGHT']
            min_val, max_val, precision = self.param_definitions['SAME_POS_BYE_WEIGHT']
        elif param_name == 'DIFF_POS_BYE_WEIGHT':
            current_val = params['DIFF_POS_BYE_WEIGHT']
            min_val, max_val, precision = self.param_definitions['DIFF_POS_BYE_WEIGHT']
        elif param_name == 'PRIMARY_BONUS':
            current_val = params['DRAFT_ORDER_BONUSES']['PRIMARY']
            min_val, max_val, precision = self.param_definitions['PRIMARY_BONUS']
        elif param_name == 'SECONDARY_BONUS':
            current_val = params['DRAFT_ORDER_BONUSES']['SECONDARY']
            min_val, max_val, precision = self.param_definitions['SECONDARY_BONUS']
        elif param_name == 'DRAFT_ORDER_FILE':
            current_val = params.get('DRAFT_ORDER_FILE', 1)
            min_val, max_val, precision = self.param_definitions['DRAFT_ORDER_FILE']
        elif '_WEIGHT' in param_name:
            parts = param_name.split('_WEIGHT')
            section = parts[0]

            current_val = params[section]['WEIGHT']
            min_val, max_val, precision = self.param_definitions[param_name]
        elif '_STEPS' in param_name:
            parts = param_name.split('_STEPS')
            section = parts[0]

            current_val = params[section]['THRESHOLDS']['STEPS']
            min_val, max_val, precision = self.param_definitions[param_name]
        elif '_IMPACT_SCALE' in param_name:
            parts = param_name.split('_IMPACT_SCALE')
            section = parts[0] + '_SCORING'

            current_val = params[section]['IMPACT_SCALE']
            min_val, max_val, precision = self.param_definitions[param_name]
        elif '_MIN_WEEKS' in param_name:
            parts = param_name.split('_MIN_WEEKS')
            section = parts[0] + '_SCORING'

            current_val = params[section].get('MIN_WEEKS', 5)
            min_val, max_val, precision = self.param_definitions[param_name]
        elif param_name.startswith('LOCATION_'):
            location_type = param_name.replace('LOCATION_', '')
            location_modifiers = params.get('LOCATION_MODIFIERS', {})
            current_val = location_modifiers.get(location_type, 0.0)
            min_val, max_val, precision = self.param_definitions[param_name]
        else:
            raise ValueError(f"Unknown parameter: {param_name}")

        test_values = self.generate_parameter_values(
            param_name,
            current_val,
            min_val,
            max_val,
            precision
        )

        configs = []
        for test_val in test_values:
            combination = self._extract_combination_from_config(base_config)

            combination[param_name] = test_val

            config = self.create_config_dict(combination)
            configs.append(config)

        self.logger.info(f"Generated {len(configs)} configs for {param_name}")
        return configs

    def _extract_combination_from_config(self, config: dict) -> Dict[str, float]:
        """
        Extract all parameter values from a config dict into a combination dict.

        Args:
            config (dict): Full configuration dictionary

        Returns:
            Dict[str, float]: Combination dict with all parameter values
        """
        params = config['parameters']
        combination = {}

        combination['NORMALIZATION_MAX_SCALE'] = params['NORMALIZATION_MAX_SCALE']
        combination['SAME_POS_BYE_WEIGHT'] = params['SAME_POS_BYE_WEIGHT']
        combination['DIFF_POS_BYE_WEIGHT'] = params['DIFF_POS_BYE_WEIGHT']
        combination['PRIMARY_BONUS'] = params['DRAFT_ORDER_BONUSES']['PRIMARY']
        combination['SECONDARY_BONUS'] = params['DRAFT_ORDER_BONUSES']['SECONDARY']
        combination['DRAFT_ORDER_FILE'] = params.get('DRAFT_ORDER_FILE', 1)

        for section in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            param_name = f'{section}_SCORING_WEIGHT'
            combination[param_name] = params[f'{section}_SCORING']['WEIGHT']

        for section in ['TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            param_name = f'{section}_MIN_WEEKS'
            combination[param_name] = params[f'{section}_SCORING'].get('MIN_WEEKS', 5)

        for section in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            param_name = f'{section}_SCORING_STEPS'
            scoring_key = f'{section}_SCORING'
            if scoring_key in params and 'THRESHOLDS' in params[scoring_key]:
                thresholds = params[scoring_key]['THRESHOLDS']
                if 'STEPS' in thresholds:
                    combination[param_name] = thresholds['STEPS']
                else:
                    if scoring_key in self.baseline_config['parameters']:
                        if 'THRESHOLDS' in self.baseline_config['parameters'][scoring_key]:
                            baseline_thresholds = self.baseline_config['parameters'][scoring_key]['THRESHOLDS']
                            if 'STEPS' in baseline_thresholds:
                                combination[param_name] = baseline_thresholds['STEPS']

        for section in ['MATCHUP']:
            param_name = f'{section}_IMPACT_SCALE'
            combination[param_name] = params[f'{section}_SCORING']['IMPACT_SCALE']

        for section in ['TEMPERATURE', 'WIND']:
            scoring_key = f'{section}_SCORING'
            if scoring_key in params:
                impact_param = f'{section}_IMPACT_SCALE'
                combination[impact_param] = params[scoring_key].get('IMPACT_SCALE', 50.0)
                weight_param = f'{section}_SCORING_WEIGHT'
                combination[weight_param] = params[scoring_key].get('WEIGHT', 1.0)

        location_modifiers = params.get('LOCATION_MODIFIERS', {})
        combination['LOCATION_HOME'] = location_modifiers.get('HOME', 2.0)
        combination['LOCATION_AWAY'] = location_modifiers.get('AWAY', -2.0)
        combination['LOCATION_INTERNATIONAL'] = location_modifiers.get('INTERNATIONAL', -5.0)

        return combination

    def create_config_dict(self, combination: Dict[str, float]) -> dict:
        """
        Create complete config dict from a parameter combination.

        Args:
            combination (Dict[str, float]): Parameter values for this config

        Returns:
            dict: Complete configuration dictionary ready for simulation

        Process:
            1. Deep copy baseline config
            2. Update varied parameters
            3. Apply weights to all scoring sections
        """
        config = copy.deepcopy(self.baseline_config)
        params = config['parameters']

        params['NORMALIZATION_MAX_SCALE'] = combination['NORMALIZATION_MAX_SCALE']
        params['SAME_POS_BYE_WEIGHT'] = combination['SAME_POS_BYE_WEIGHT']
        params['DIFF_POS_BYE_WEIGHT'] = combination['DIFF_POS_BYE_WEIGHT']
        params['DRAFT_ORDER_BONUSES']['PRIMARY'] = combination['PRIMARY_BONUS']
        params['DRAFT_ORDER_BONUSES']['SECONDARY'] = combination['SECONDARY_BONUS']

        draft_order_file = int(combination.get('DRAFT_ORDER_FILE', 1))
        params['DRAFT_ORDER_FILE'] = draft_order_file
        params['DRAFT_ORDER'] = self._load_draft_order_from_file(draft_order_file)

        params['MATCHUP_SCORING']['IMPACT_SCALE'] = combination['MATCHUP_IMPACT_SCALE']

        for parameter in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            params[f'{parameter}_SCORING']['WEIGHT'] = combination[f'{parameter}_SCORING_WEIGHT']

        for parameter in ['TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            min_weeks_param = f'{parameter}_MIN_WEEKS'
            if min_weeks_param in combination:
                params[f'{parameter}_SCORING']['MIN_WEEKS'] = int(combination[min_weeks_param])

        for parameter in ['ADP', 'PERFORMANCE']:
            steps_param = f'{parameter}_SCORING_STEPS'
            if steps_param in combination:
                fixed_params = self.THRESHOLD_FIXED_PARAMS[f'{parameter}_SCORING']
                params[f'{parameter}_SCORING']['THRESHOLDS'] = {
                    'BASE_POSITION': fixed_params['BASE_POSITION'],
                    'DIRECTION': fixed_params['DIRECTION'],
                    'STEPS': combination[steps_param]
                }

        for section in ['TEMPERATURE', 'WIND']:
            scoring_key = f'{section}_SCORING'
            impact_param = f'{section}_IMPACT_SCALE'
            weight_param = f'{section}_SCORING_WEIGHT'

            if scoring_key not in params:
                params[scoring_key] = {
                    'MULTIPLIERS': {
                        'EXCELLENT': 1.05,
                        'GOOD': 1.025,
                        'POOR': 0.975,
                        'VERY_POOR': 0.95
                    }
                }

            if impact_param in combination:
                params[scoring_key]['IMPACT_SCALE'] = combination[impact_param]

            if weight_param in combination:
                params[scoring_key]['WEIGHT'] = combination[weight_param]

            if scoring_key in self.THRESHOLD_FIXED_PARAMS:
                fixed_params = self.THRESHOLD_FIXED_PARAMS[scoring_key]
                if 'THRESHOLDS' not in params[scoring_key]:
                    params[scoring_key]['THRESHOLDS'] = {}
                params[scoring_key]['THRESHOLDS']['BASE_POSITION'] = fixed_params['BASE_POSITION']
                params[scoring_key]['THRESHOLDS']['DIRECTION'] = fixed_params['DIRECTION']
                params[scoring_key]['THRESHOLDS']['STEPS'] = fixed_params['STEPS']
                if 'IDEAL_TEMPERATURE' in fixed_params:
                    params[scoring_key]['IDEAL_TEMPERATURE'] = fixed_params['IDEAL_TEMPERATURE']

            if 'MULTIPLIERS' not in params[scoring_key]:
                params[scoring_key]['MULTIPLIERS'] = {
                    'EXCELLENT': 1.05,
                    'GOOD': 1.025,
                    'POOR': 0.975,
                    'VERY_POOR': 0.95
                }

        if 'LOCATION_MODIFIERS' not in params:
            params['LOCATION_MODIFIERS'] = {}

        if 'LOCATION_HOME' in combination:
            params['LOCATION_MODIFIERS']['HOME'] = combination['LOCATION_HOME']
        if 'LOCATION_AWAY' in combination:
            params['LOCATION_MODIFIERS']['AWAY'] = combination['LOCATION_AWAY']
        if 'LOCATION_INTERNATIONAL' in combination:
            params['LOCATION_MODIFIERS']['INTERNATIONAL'] = combination['LOCATION_INTERNATIONAL']

        return config

    def generate_all_configs(self) -> List[dict]:
        """
        Generate all complete configuration dictionaries.

        Returns:
            List[dict]: All configurations ready for simulation

        Note:
            Total configs = (num_test_values + 1)^13
            Each config is ~10KB
            Example: 6^13 = ~13.1 billion configs = impractical for full cartesian product
            For practical use, use iterative optimization instead
        """
        total_configs = (self.num_test_values + 1) ** 13
        self.logger.info(f"Generating all {total_configs:,} complete configurations")

        combinations = self.generate_all_combinations()
        configs = []

        for combo in combinations:
            config = self.create_config_dict(combo)
            configs.append(config)

        self.logger.info(f"All {len(configs)} configurations generated")
        return configs


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
                val = random.randint(int(min_val), int(max_val))
            else:
                val = random.uniform(min_val, max_val)
                val = round(val, precision)
            values.append(val)

        return values


