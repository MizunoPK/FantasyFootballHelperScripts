"""
Configuration Generator

Generates parameter combinations for simulation optimization. Creates combinations
by varying 13 key parameters, with N+1 values per parameter (optimal + N random variations).

Total configurations = (N+1)^13 where N = num_test_values (default: 5)
Example: (5+1)^13 = ~13.1 billion configurations

Parameters Varied:
1. NORMALIZATION_MAX_SCALE: Random values in [50, 500]
2. SAME_POS_BYE_WEIGHT: Random values in [0, 3]
3. DIFF_POS_BYE_WEIGHT: Random values in [0, 3]
4. DRAFT_ORDER_BONUSES.PRIMARY: Random values in [0, 200]
5. DRAFT_ORDER_BONUSES.SECONDARY: Random values in [0, 200]
6. ADP_SCORING_WEIGHT: Random values in [0, 5]
7. ADP_SCORING_STEPS: Random values in [1, 60]
8. PLAYER_RATING_SCORING_WEIGHT: Random values in [0, 5]
9. TEAM_QUALITY_SCORING_WEIGHT: Random values in [0, 5]
10. PERFORMANCE_SCORING_WEIGHT: Random values in [0, 5]
11. PERFORMANCE_SCORING_STEPS: Random values in [0.05, 0.5]
12. MATCHUP_IMPACT_SCALE: Random values in [0, 300]
13. MATCHUP_SCORING_WEIGHT: Random values in [0, 5]

Note: PLAYER_RATING_SCORING_STEPS, TEAM_QUALITY_SCORING_STEPS, MATCHUP_SCORING_STEPS,
      and all SCHEDULE_SCORING parameters are disabled (not optimized)

Author: Kai Mizuno
"""

import json
import random
import copy
from pathlib import Path
from typing import List, Dict, Tuple
from itertools import product

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


class ConfigGenerator:
    """
    Generates configuration combinations for simulation optimization.

    Attributes:
        baseline_config (dict): Base configuration to vary from
        param_definitions (dict): Parameter ranges and bounds
        logger: Logger instance
    """

    # Parameter definitions ordered to match league_config.json structure
    # Format: (min_val, max_val)
    PARAM_DEFINITIONS = {
        # Normalization and Bye Penalties
        'NORMALIZATION_MAX_SCALE': (100.0, 150.0),
        'SAME_POS_BYE_WEIGHT': (0.1, 0.5),
        'DIFF_POS_BYE_WEIGHT': (0.0, 0.3),
        # Draft Order Bonuses
        'PRIMARY_BONUS': (60, 100.0),
        'SECONDARY_BONUS': (60, 100.0),
        # Draft Order File (discrete integer 1-10, draft order strategies)
        'DRAFT_ORDER_FILE': (1, 10),
        # ADP Scoring
        'ADP_SCORING_WEIGHT': (0.0, 3.0),
        'ADP_SCORING_STEPS': (10.0, 45.0),
        # Player Rating Scoring
        'PLAYER_RATING_SCORING_WEIGHT': (0.0, 3.0),
        # Team Quality Scoring
        'TEAM_QUALITY_SCORING_WEIGHT': (0.0, 3.0),
        'TEAM_QUALITY_MIN_WEEKS': (1, 17),
        # Performance Scoring
        'PERFORMANCE_SCORING_WEIGHT': (0.0, 4.0),
        'PERFORMANCE_SCORING_STEPS': (0.1, 0.4),
        'PERFORMANCE_MIN_WEEKS': (1, 17),
        # Matchup Scoring (additive)
        'MATCHUP_IMPACT_SCALE': (75.0, 175.0),
        'MATCHUP_SCORING_WEIGHT': (0.0, 3.0),
        'MATCHUP_MIN_WEEKS': (1, 17),
        # Temperature Scoring (game conditions)
        'TEMPERATURE_IMPACT_SCALE': (10.0, 100.0),
        'TEMPERATURE_SCORING_WEIGHT': (0.0, 3.0),
        # Wind Scoring (game conditions, QB/WR/K only)
        'WIND_IMPACT_SCALE': (10.0, 100.0),
        'WIND_SCORING_WEIGHT': (0.0, 3.0),
        # Location Modifiers
        'LOCATION_HOME': (0.0, 10.0),
        'LOCATION_AWAY': (-10.0, 0.0),
        'LOCATION_INTERNATIONAL': (-15.0, 0.0),
    }

    # Fixed threshold parameters (not varied during optimization)
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
            "DIRECTION": "INCREASING"  # Updated to match league_config.json (direct opponent rank 1-32)
        },
        # "SCHEDULE_SCORING": {
        #     "BASE_POSITION": 0,
        #     "DIRECTION": "INCREASING"
        # },
        "TEMPERATURE_SCORING": {
            "BASE_POSITION": 0,
            "DIRECTION": "DECREASING",  # Lower distance from ideal = better
            "STEPS": 10,
            "IDEAL_TEMPERATURE": 60
        },
        "WIND_SCORING": {
            "BASE_POSITION": 0,
            "DIRECTION": "DECREASING",  # Lower wind = better
            "STEPS": 8
        }
    }

    # Scoring sections that need weights applied
    SCORING_SECTIONS = [
        'ADP_SCORING',
        'PLAYER_RATING_SCORING',
        'PERFORMANCE_SCORING',
        'MATCHUP_SCORING',
        # 'SCHEDULE_SCORING',  # DISABLED
        'TEMPERATURE_SCORING',  # Game conditions
        'WIND_SCORING',  # Game conditions (QB/WR/K only)
    ]

    # Parameter ordering for iterative optimization
    # Ordered to match league_config.json structure
    PARAMETER_ORDER = [
        # Normalization and Bye Penalties
        'NORMALIZATION_MAX_SCALE',
        'SAME_POS_BYE_WEIGHT',
        'DIFF_POS_BYE_WEIGHT',
        # Draft Order Bonuses
        'PRIMARY_BONUS',
        'SECONDARY_BONUS',
        # Draft Order File
        'DRAFT_ORDER_FILE',
        # ADP Scoring
        'ADP_SCORING_WEIGHT',
        'ADP_SCORING_STEPS',
        # Player Rating Scoring
        'PLAYER_RATING_SCORING_WEIGHT',
        # Team Quality Scoring
        'TEAM_QUALITY_SCORING_WEIGHT',
        'TEAM_QUALITY_MIN_WEEKS',
        # Performance Scoring
        'PERFORMANCE_SCORING_WEIGHT',
        'PERFORMANCE_SCORING_STEPS',
        'PERFORMANCE_MIN_WEEKS',
        # Matchup Scoring (additive)
        'MATCHUP_IMPACT_SCALE',
        'MATCHUP_SCORING_WEIGHT',
        'MATCHUP_MIN_WEEKS',
        # Game Condition Scoring
        'TEMPERATURE_IMPACT_SCALE',
        'TEMPERATURE_SCORING_WEIGHT',
        'WIND_IMPACT_SCALE',
        'WIND_SCORING_WEIGHT',
        'LOCATION_HOME',
        'LOCATION_AWAY',
        'LOCATION_INTERNATIONAL',
    ]

    def __init__(self, baseline_config_path: Path, num_test_values: int = 5, num_parameters_to_test: int = 1) -> None:
        """
        Initialize ConfigGenerator with baseline configuration.

        Args:
            baseline_config_path (Path): Path to baseline config JSON file
            num_test_values (int): Number of random values to generate per parameter (default: 5)
                This creates (num_test_values + 1) total values per parameter (optimal + random)

        Raises:
            FileNotFoundError: If baseline config file doesn't exist
            ValueError: If baseline config is invalid
        """
        self.logger = get_logger()
        self.logger.info(f"Initializing ConfigGenerator with baseline: {baseline_config_path}")
        self.logger.info(f"Test values per parameter: {num_test_values} (total values: {num_test_values + 1})")

        self.baseline_config = self.load_baseline_config(baseline_config_path)
        self.param_definitions = self.PARAM_DEFINITIONS
        self.num_test_values = num_test_values
        self.num_parameters_to_test = num_parameters_to_test

        self.logger.info("ConfigGenerator initialized successfully")

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

        # Validate required structure
        if 'parameters' not in config:
            raise ValueError("Config missing 'parameters' section")

        self.logger.debug(f"Loaded config: {config.get('config_name', 'Unknown')}")
        return config

    def generate_parameter_values(
        self,
        param_name: str,
        optimal_val: float,
        min_val: float,
        max_val: float
    ) -> List[float]:
        """
        Generate N+1 values for a parameter: optimal + N random variations.

        Args:
            param_name (str): Parameter name (for logging)
            optimal_val (float): Optimal/baseline value
            min_val (float): Minimum allowed value
            max_val (float): Maximum allowed value

        Returns:
            List[float]: (N+1) values [optimal, rand1, rand2, ..., randN]
                where N = self.num_test_values

        Example:
            >>> gen = ConfigGenerator(baseline_path, num_test_values=5)
            >>> values = gen.generate_parameter_values('NORMALIZATION_MAX_SCALE', 100, 60, 140)
            >>> # Returns [100.0, 94.3, 118.7, 83.2, 105.9, 112.1] (6 values)
        """
        values = [optimal_val]

        # Generate N random values between min and max
        for _ in range(self.num_test_values):
            rand_val = random.uniform(min_val, max_val)
            values.append(rand_val)

        self.logger.debug(f"{param_name}: {len(values)} values generated (min={min(values):.2f}, max={max(values):.2f})")
        return values

    def generate_discrete_parameter_values(
        self,
        param_name: str,
        optimal_val: int,
        min_val: int,
        max_val: int
    ) -> List[int]:
        """
        Generate N+1 discrete integer values for a parameter: optimal + N random variations.

        Args:
            param_name (str): Parameter name (for logging)
            optimal_val (int): Optimal/baseline value
            min_val (int): Minimum allowed value
            max_val (int): Maximum allowed value

        Returns:
            List[int]: (N+1) values [optimal, rand1, rand2, ..., randN]
                where N = self.num_test_values

        Example:
            >>> gen = ConfigGenerator(baseline_path, num_test_values=5)
            >>> values = gen.generate_discrete_parameter_values('DRAFT_ORDER_FILE', 1, 1, 30)
            >>> # Returns [1, 15, 23, 7, 28, 12] (6 values)
        """
        values = [optimal_val]

        # Generate N random integers excluding optimal_val
        available = [i for i in range(min_val, max_val + 1) if i != optimal_val]
        num_to_sample = min(self.num_test_values, len(available))
        random_vals = random.sample(available, num_to_sample)
        values.extend(random_vals)

        self.logger.debug(f"{param_name}: {len(values)} discrete values generated")
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
        draft_order_dir = Path(__file__).parent / "sim_data" / "draft_order_possibilities"

        # Try pattern with suffix first (e.g., 2_zero_rb.json)
        matches = list(draft_order_dir.glob(f"{file_num}_*.json"))
        if not matches:
            # Try exact match (e.g., 1.json)
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
        min_val, max_val = self.param_definitions[full_name]
        value_sets[full_name] = self.generate_parameter_values(full_name, base_weight, min_val, max_val)

        return value_sets

    def generate_all_parameter_value_sets(self) -> Dict[str, List[float]]:
        """
        Generate value sets for all 13 parameters (5 scalar + 5 weights + 2 threshold STEPS + 1 IMPACT_SCALE).

        Returns:
            Dict[str, List[float]]: {param_name: [N+1 values]} where N = num_test_values

        Example:
            >>> gen = ConfigGenerator(baseline_path, num_test_values=5)
            >>> value_sets = gen.generate_all_parameter_value_sets()
            >>> value_sets['NORMALIZATION_MAX_SCALE']
            [100.0, 94.3, 118.7, 83.2, 105.9, 112.1]  # 6 values
            >>> value_sets['ADP_SCORING_STEPS']
            [37.5, 32.1, 42.8, 30.5, 45.2, 39.1]  # 6 values
        """
        self.logger.info("Generating value sets for all parameters")

        value_sets = {}
        params = self.baseline_config['parameters']

        # NORMALIZATION_MAX_SCALE
        value_sets['NORMALIZATION_MAX_SCALE'] = self.generate_parameter_values(
            'NORMALIZATION_MAX_SCALE',
            params['NORMALIZATION_MAX_SCALE'],
            *self.param_definitions['NORMALIZATION_MAX_SCALE']
        )

        # SAME_POS_BYE_WEIGHT
        value_sets['SAME_POS_BYE_WEIGHT'] = self.generate_parameter_values(
            'SAME_POS_BYE_WEIGHT',
            params['SAME_POS_BYE_WEIGHT'],
            *self.param_definitions['SAME_POS_BYE_WEIGHT']
        )

        # DIFF_POS_BYE_WEIGHT
        value_sets['DIFF_POS_BYE_WEIGHT'] = self.generate_parameter_values(
            'DIFF_POS_BYE_WEIGHT',
            params['DIFF_POS_BYE_WEIGHT'],
            *self.param_definitions['DIFF_POS_BYE_WEIGHT']
        )

        # PRIMARY_BONUS
        value_sets['PRIMARY_BONUS'] = self.generate_parameter_values(
            'PRIMARY_BONUS',
            params['DRAFT_ORDER_BONUSES']['PRIMARY'],
            *self.param_definitions['PRIMARY_BONUS']
        )

        # SECONDARY_BONUS
        value_sets['SECONDARY_BONUS'] = self.generate_parameter_values(
            'SECONDARY_BONUS',
            params['DRAFT_ORDER_BONUSES']['SECONDARY'],
            *self.param_definitions['SECONDARY_BONUS']
        )

        # ADP
        value_sets = self.generate_multiplier_parameter_values(value_sets, "ADP_SCORING")

        # PLAYER RATING
        value_sets = self.generate_multiplier_parameter_values(value_sets, "PLAYER_RATING_SCORING")

        # TEAM QUALITY
        value_sets = self.generate_multiplier_parameter_values(value_sets, "TEAM_QUALITY_SCORING")

        # PERFORMANCE
        value_sets = self.generate_multiplier_parameter_values(value_sets, "PERFORMANCE_SCORING")

        # MATCHUP
        value_sets = self.generate_multiplier_parameter_values(value_sets, "MATCHUP_SCORING")

        # SCHEDULE - DISABLED
        # value_sets = self.generate_multiplier_parameter_values(value_sets, "SCHEDULE_SCORING")

        # Threshold STEPS parameters - only for sections with STEPS in PARAM_DEFINITIONS
        # (PLAYER_RATING, TEAM_QUALITY, MATCHUP, SCHEDULE are disabled)
        for scoring_type in ["ADP_SCORING", "PERFORMANCE_SCORING"]:
            steps_param = f"{scoring_type}_STEPS"
            # Check if using parameterized format (has STEPS key)
            if 'STEPS' in params[scoring_type]['THRESHOLDS']:
                current_steps = params[scoring_type]['THRESHOLDS']['STEPS']
                min_val, max_val = self.param_definitions[steps_param]
                value_sets[steps_param] = self.generate_parameter_values(
                    steps_param,
                    current_steps,
                    min_val,
                    max_val
                )

        # IMPACT_SCALE parameters (additive scoring - NEW)
        # Only MATCHUP_SCORING - SCHEDULE_SCORING disabled
        for scoring_type in ["MATCHUP_SCORING"]:
            impact_param = scoring_type.replace('_SCORING', '_IMPACT_SCALE')
            current_impact = params[scoring_type]['IMPACT_SCALE']
            min_val, max_val = self.param_definitions[impact_param]
            value_sets[impact_param] = self.generate_parameter_values(
                impact_param,
                current_impact,
                min_val,
                max_val
            )

        # MIN_WEEKS parameters for rolling window calculations
        for scoring_type in ["TEAM_QUALITY_SCORING", "PERFORMANCE_SCORING", "MATCHUP_SCORING"]:
            min_weeks_param = scoring_type.replace('_SCORING', '_MIN_WEEKS')
            current_min_weeks = params[scoring_type].get('MIN_WEEKS', 5)
            min_val, max_val = self.param_definitions[min_weeks_param]
            value_sets[min_weeks_param] = self.generate_parameter_values(
                min_weeks_param,
                current_min_weeks,
                min_val,
                max_val
            )

        # Game conditions: Temperature and Wind scoring
        for section in ['TEMPERATURE', 'WIND']:
            scoring_key = f'{section}_SCORING'
            if scoring_key in params:
                # IMPACT_SCALE
                impact_param = f'{section}_IMPACT_SCALE'
                if impact_param in self.param_definitions:
                    current_impact = params[scoring_key].get('IMPACT_SCALE', 50.0)
                    min_val, max_val = self.param_definitions[impact_param]
                    value_sets[impact_param] = self.generate_parameter_values(
                        impact_param, current_impact, min_val, max_val
                    )

                # WEIGHT
                weight_param = f'{section}_SCORING_WEIGHT'
                if weight_param in self.param_definitions:
                    current_weight = params[scoring_key].get('WEIGHT', 1.0)
                    min_val, max_val = self.param_definitions[weight_param]
                    value_sets[weight_param] = self.generate_parameter_values(
                        weight_param, current_weight, min_val, max_val
                    )

        # Game conditions: Location modifiers
        location_modifiers = params.get('LOCATION_MODIFIERS', {})
        for loc_type in ['HOME', 'AWAY', 'INTERNATIONAL']:
            param_name = f'LOCATION_{loc_type}'
            if param_name in self.param_definitions:
                # Default values: HOME=2.0, AWAY=-2.0, INTERNATIONAL=-5.0
                defaults = {'HOME': 2.0, 'AWAY': -2.0, 'INTERNATIONAL': -5.0}
                current_val = location_modifiers.get(loc_type, defaults[loc_type])
                min_val, max_val = self.param_definitions[param_name]
                value_sets[param_name] = self.generate_parameter_values(
                    param_name, current_val, min_val, max_val
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

        # Generate value sets for all parameters
        value_sets = self.generate_all_parameter_value_sets()

        # Create all combinations using itertools.product
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
        # Task 2.0: Input Validation and Error Handling
        if param_name not in self.PARAMETER_ORDER:
            raise ValueError(f"Unknown parameter: {param_name}")

        # Validate and cap num_parameters_to_test
        num_params_to_test = self.num_parameters_to_test
        if num_params_to_test < 1:
            self.logger.warning(f"num_parameters_to_test={num_params_to_test} is invalid, defaulting to 1")
            num_params_to_test = 1

        max_params = len(self.PARAMETER_ORDER)
        if num_params_to_test > max_params:
            self.logger.info(f"num_parameters_to_test={num_params_to_test} exceeds available parameters ({max_params}), capping at {max_params}")
            num_params_to_test = max_params

        # Calculate and warn about performance
        num_values = self.num_test_values + 1
        expected_combinations = num_values ** num_params_to_test
        if expected_combinations > 1000:
            self.logger.warning(
                f"Cartesian product will generate {expected_combinations:,} combination configs. "
                f"This may impact performance. Consider reducing NUM_PARAMETERS_TO_TEST or num_test_values."
            )

        self.logger.info(f"Generating configs with cartesian product strategy for {num_params_to_test} parameters")

        # Task 2.1: Random Parameter Selection
        num_random = num_params_to_test - 1
        random_params = []

        if num_random > 0:
            # Create pool excluding base parameter
            available_params = [p for p in self.PARAMETER_ORDER if p != param_name]
            random_params = random.sample(available_params, num_random)
            self.logger.info(f"Selected {num_random} random parameters: {random_params}")
        else:
            self.logger.info("NUM_PARAMETERS_TO_TEST=1, testing only base parameter (no random selection)")

        # Task 2.2: Generate Individual Parameter Configs
        all_params = [param_name] + random_params
        param_configs = {}

        # Generate configs for base parameter
        base_configs = self.generate_single_parameter_configs(param_name, base_config)
        param_configs[param_name] = base_configs

        # Generate configs for each random parameter
        for random_param in random_params:
            configs = self.generate_single_parameter_configs(random_param, base_config)
            param_configs[random_param] = configs

        # Task 2.3: Generate Combination Configs (Cartesian Product)
        combination_configs = []

        if num_params_to_test > 1:
            # Extract parameter values from generated configs
            param_values = {}
            for param in all_params:
                param_values[param] = []
                for config in param_configs[param]:
                    combination = self._extract_combination_from_config(config)
                    param_values[param].append(combination[param])

            # Generate cartesian product of all values
            value_lists = [param_values[p] for p in all_params]

            for value_tuple in product(*value_lists):
                # Create combination with all params from base_config
                combination = self._extract_combination_from_config(base_config)

                # Update with values from this tuple
                for param, value in zip(all_params, value_tuple):
                    combination[param] = value

                # Create full config
                config = self.create_config_dict(combination)
                combination_configs.append(config)

        # Task 2.4: Merge All Configs and Add Logging
        all_configs = []

        # Add all individual parameter configs
        for param in all_params:
            all_configs.extend(param_configs[param])

        # Add combination configs
        all_configs.extend(combination_configs)

        # Log detailed breakdown
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

        # Extract current value from base_config
        params = base_config['parameters']

        # Determine range and bounds based on parameter type
        if param_name == 'NORMALIZATION_MAX_SCALE':
            current_val = params['NORMALIZATION_MAX_SCALE']
            min_val, max_val = self.param_definitions['NORMALIZATION_MAX_SCALE']
        elif param_name == 'SAME_POS_BYE_WEIGHT':
            current_val = params['SAME_POS_BYE_WEIGHT']
            min_val, max_val = self.param_definitions['SAME_POS_BYE_WEIGHT']
        elif param_name == 'DIFF_POS_BYE_WEIGHT':
            current_val = params['DIFF_POS_BYE_WEIGHT']
            min_val, max_val = self.param_definitions['DIFF_POS_BYE_WEIGHT']
        elif param_name == 'PRIMARY_BONUS':
            current_val = params['DRAFT_ORDER_BONUSES']['PRIMARY']
            min_val, max_val = self.param_definitions['PRIMARY_BONUS']
        elif param_name == 'SECONDARY_BONUS':
            current_val = params['DRAFT_ORDER_BONUSES']['SECONDARY']
            min_val, max_val = self.param_definitions['SECONDARY_BONUS']
        elif param_name == 'DRAFT_ORDER_FILE':
            current_val = params.get('DRAFT_ORDER_FILE', 1)
            min_val, max_val = self.param_definitions['DRAFT_ORDER_FILE']
            # Use discrete values for file selection
            test_values = self.generate_discrete_parameter_values(
                param_name, int(current_val), int(min_val), int(max_val)
            )
            # Create config for each test value
            configs = []
            for test_val in test_values:
                combination = self._extract_combination_from_config(base_config)
                combination[param_name] = test_val
                config = self.create_config_dict(combination)
                configs.append(config)
            self.logger.info(f"Generated {len(configs)} configs for {param_name}")
            return configs
        elif '_WEIGHT' in param_name:
            # Extract section and multiplier type
            # Format: SECTION_SCORING_WEIGHT
            parts = param_name.split('_WEIGHT')
            section = parts[0]  # e.g., 'ADP_SCORING'

            current_val = params[section]['WEIGHT']
            min_val, max_val = self.param_definitions[param_name]
        elif '_STEPS' in param_name:
            # Extract section for threshold STEPS
            # Format: SECTION_SCORING_STEPS
            parts = param_name.split('_STEPS')
            section = parts[0]  # e.g., 'ADP_SCORING'

            current_val = params[section]['THRESHOLDS']['STEPS']
            min_val, max_val = self.param_definitions[param_name]
        elif '_IMPACT_SCALE' in param_name:
            # Extract section for IMPACT_SCALE (additive scoring)
            # Format: SECTION_IMPACT_SCALE (e.g., 'MATCHUP_IMPACT_SCALE')
            parts = param_name.split('_IMPACT_SCALE')
            section = parts[0] + '_SCORING'  # e.g., 'MATCHUP_SCORING'

            current_val = params[section]['IMPACT_SCALE']
            min_val, max_val = self.param_definitions[param_name]
        elif '_MIN_WEEKS' in param_name:
            # Extract section for MIN_WEEKS
            # Format: SECTION_MIN_WEEKS (e.g., 'TEAM_QUALITY_MIN_WEEKS')
            parts = param_name.split('_MIN_WEEKS')
            section = parts[0] + '_SCORING'  # e.g., 'TEAM_QUALITY_SCORING'

            current_val = params[section].get('MIN_WEEKS', 5)
            min_val, max_val = self.param_definitions[param_name]
        elif param_name.startswith('LOCATION_'):
            # Location modifiers (HOME, AWAY, INTERNATIONAL)
            # Format: LOCATION_TYPE (e.g., 'LOCATION_HOME')
            location_type = param_name.replace('LOCATION_', '')  # e.g., 'HOME'
            location_modifiers = params.get('LOCATION_MODIFIERS', {})
            current_val = location_modifiers.get(location_type, 0.0)
            min_val, max_val = self.param_definitions[param_name]
        else:
            raise ValueError(f"Unknown parameter: {param_name}")

        # Generate test values
        test_values = self.generate_parameter_values(
            param_name,
            current_val,
            min_val,
            max_val
        )

        # Create config for each test value
        configs = []
        for test_val in test_values:
            # Create combination dict with all parameters from base_config
            combination = self._extract_combination_from_config(base_config)

            # Update only the parameter we're testing
            combination[param_name] = test_val

            # Create full config
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

        # Scalar parameters
        combination['NORMALIZATION_MAX_SCALE'] = params['NORMALIZATION_MAX_SCALE']
        combination['SAME_POS_BYE_WEIGHT'] = params['SAME_POS_BYE_WEIGHT']
        combination['DIFF_POS_BYE_WEIGHT'] = params['DIFF_POS_BYE_WEIGHT']
        combination['PRIMARY_BONUS'] = params['DRAFT_ORDER_BONUSES']['PRIMARY']
        combination['SECONDARY_BONUS'] = params['DRAFT_ORDER_BONUSES']['SECONDARY']
        combination['DRAFT_ORDER_FILE'] = params.get('DRAFT_ORDER_FILE', 1)

        # WEIGHTS for each section (SCHEDULE disabled)
        for section in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            param_name = f'{section}_SCORING_WEIGHT'
            combination[param_name] = params[f'{section}_SCORING']['WEIGHT']

        # MIN_WEEKS for relevant sections
        for section in ['TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            param_name = f'{section}_MIN_WEEKS'
            combination[param_name] = params[f'{section}_SCORING'].get('MIN_WEEKS', 5)

        # STEPS for each scoring type - extract all that are present in config
        # Only ADP and PERFORMANCE STEPS are actively optimized, but others may be in PARAMETER_ORDER
        for section in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            param_name = f'{section}_SCORING_STEPS'
            scoring_key = f'{section}_SCORING'
            if scoring_key in params and 'THRESHOLDS' in params[scoring_key]:
                thresholds = params[scoring_key]['THRESHOLDS']
                # Check if using parameterized format (has STEPS key)
                if 'STEPS' in thresholds:
                    combination[param_name] = thresholds['STEPS']
                else:
                    # Old format - use default value from baseline if it exists
                    # This handles backward compatibility with test fixtures
                    if scoring_key in self.baseline_config['parameters']:
                        if 'THRESHOLDS' in self.baseline_config['parameters'][scoring_key]:
                            baseline_thresholds = self.baseline_config['parameters'][scoring_key]['THRESHOLDS']
                            if 'STEPS' in baseline_thresholds:
                                combination[param_name] = baseline_thresholds['STEPS']

        # IMPACT_SCALE for additive scoring (NEW) - Only MATCHUP, SCHEDULE disabled
        for section in ['MATCHUP']:
            param_name = f'{section}_IMPACT_SCALE'
            combination[param_name] = params[f'{section}_SCORING']['IMPACT_SCALE']

        # Game conditions: Temperature and Wind scoring
        for section in ['TEMPERATURE', 'WIND']:
            scoring_key = f'{section}_SCORING'
            if scoring_key in params:
                # Extract IMPACT_SCALE
                impact_param = f'{section}_IMPACT_SCALE'
                combination[impact_param] = params[scoring_key].get('IMPACT_SCALE', 50.0)
                # Extract WEIGHT
                weight_param = f'{section}_SCORING_WEIGHT'
                combination[weight_param] = params[scoring_key].get('WEIGHT', 1.0)

        # Game conditions: Location modifiers
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
        # Deep copy baseline to avoid mutations
        config = copy.deepcopy(self.baseline_config)
        params = config['parameters']

        # Update scalar parameters
        params['NORMALIZATION_MAX_SCALE'] = combination['NORMALIZATION_MAX_SCALE']
        params['SAME_POS_BYE_WEIGHT'] = combination['SAME_POS_BYE_WEIGHT']
        params['DIFF_POS_BYE_WEIGHT'] = combination['DIFF_POS_BYE_WEIGHT']
        params['DRAFT_ORDER_BONUSES']['PRIMARY'] = combination['PRIMARY_BONUS']
        params['DRAFT_ORDER_BONUSES']['SECONDARY'] = combination['SECONDARY_BONUS']

        # Update DRAFT_ORDER_FILE and load corresponding DRAFT_ORDER
        draft_order_file = int(combination.get('DRAFT_ORDER_FILE', 1))
        params['DRAFT_ORDER_FILE'] = draft_order_file
        params['DRAFT_ORDER'] = self._load_draft_order_from_file(draft_order_file)

        # Update IMPACT_SCALE for additive scoring (NEW) - SCHEDULE disabled
        params['MATCHUP_SCORING']['IMPACT_SCALE'] = combination['MATCHUP_IMPACT_SCALE']
        # params['SCHEDULE_SCORING']['IMPACT_SCALE'] = combination['SCHEDULE_IMPACT_SCALE']

        # Update weights (SCHEDULE disabled)
        for parameter in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            params[f'{parameter}_SCORING']['WEIGHT'] = combination[f'{parameter}_SCORING_WEIGHT']

        # Update MIN_WEEKS for sections that use it
        for parameter in ['TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            min_weeks_param = f'{parameter}_MIN_WEEKS'
            if min_weeks_param in combination:
                params[f'{parameter}_SCORING']['MIN_WEEKS'] = int(combination[min_weeks_param])

        # Update threshold STEPS - only sections with STEPS in PARAM_DEFINITIONS
        # (PLAYER_RATING, TEAM_QUALITY, MATCHUP, SCHEDULE disabled)
        for parameter in ['ADP', 'PERFORMANCE']:
            steps_param = f'{parameter}_SCORING_STEPS'
            if steps_param in combination:
                fixed_params = self.THRESHOLD_FIXED_PARAMS[f'{parameter}_SCORING']
                params[f'{parameter}_SCORING']['THRESHOLDS'] = {
                    'BASE_POSITION': fixed_params['BASE_POSITION'],
                    'DIRECTION': fixed_params['DIRECTION'],
                    'STEPS': combination[steps_param]
                }

        # Update game conditions: Temperature and Wind scoring
        for section in ['TEMPERATURE', 'WIND']:
            scoring_key = f'{section}_SCORING'
            impact_param = f'{section}_IMPACT_SCALE'
            weight_param = f'{section}_SCORING_WEIGHT'

            # Ensure scoring section exists with default structure
            if scoring_key not in params:
                params[scoring_key] = {
                    'MULTIPLIERS': {
                        'EXCELLENT': 1.05,
                        'GOOD': 1.025,
                        'POOR': 0.975,
                        'VERY_POOR': 0.95
                    }
                }

            # Update IMPACT_SCALE if present in combination
            if impact_param in combination:
                params[scoring_key]['IMPACT_SCALE'] = combination[impact_param]

            # Update WEIGHT if present in combination
            if weight_param in combination:
                params[scoring_key]['WEIGHT'] = combination[weight_param]

            # Ensure threshold structure from fixed params
            if scoring_key in self.THRESHOLD_FIXED_PARAMS:
                fixed_params = self.THRESHOLD_FIXED_PARAMS[scoring_key]
                if 'THRESHOLDS' not in params[scoring_key]:
                    params[scoring_key]['THRESHOLDS'] = {}
                params[scoring_key]['THRESHOLDS']['BASE_POSITION'] = fixed_params['BASE_POSITION']
                params[scoring_key]['THRESHOLDS']['DIRECTION'] = fixed_params['DIRECTION']
                params[scoring_key]['THRESHOLDS']['STEPS'] = fixed_params['STEPS']
                # Preserve IDEAL_TEMPERATURE if present
                if 'IDEAL_TEMPERATURE' in fixed_params:
                    params[scoring_key]['IDEAL_TEMPERATURE'] = fixed_params['IDEAL_TEMPERATURE']

            # Ensure MULTIPLIERS exist (in case baseline config lacks them)
            if 'MULTIPLIERS' not in params[scoring_key]:
                params[scoring_key]['MULTIPLIERS'] = {
                    'EXCELLENT': 1.05,
                    'GOOD': 1.025,
                    'POOR': 0.975,
                    'VERY_POOR': 0.95
                }

        # Update game conditions: Location modifiers
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
