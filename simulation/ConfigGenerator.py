"""
Configuration Generator

Generates parameter combinations for simulation optimization. Creates combinations
by varying 14 key parameters, with N+1 values per parameter (optimal + N random variations).

Total configurations = (N+1)^14 where N = num_test_values (default: 5)
Example: (5+1)^14 = ~78 billion configurations

Parameters Varied:
1. NORMALIZATION_MAX_SCALE: ±10 from optimal, bounded [50, 150]
2. BASE_BYE_PENALTY: ±10 from optimal, bounded [0, 50]
3. DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY: ±10 from optimal, bounded [0, 50]
4. DRAFT_ORDER_BONUSES.PRIMARY: ±10 from optimal, bounded [0, 100]
5. DRAFT_ORDER_BONUSES.SECONDARY: ±10 from optimal, bounded [0, 75]
6. ADP_SCORING_WEIGHT: ±0.3 from optimal, bounded [0, 5]
7. PLAYER_RATING_SCORING_WEIGHT: ±0.3 from optimal, bounded [0, 5]
8. PERFORMANCE_SCORING_WEIGHT: ±0.3 from optimal, bounded [0, 5]
9. MATCHUP_SCORING_WEIGHT: ±0.3 from optimal, bounded [0, 5]
10. ADP_SCORING_STEPS: ±5 from optimal, bounded [25, 50]
11. PLAYER_RATING_SCORING_STEPS: ±4 from optimal, bounded [12, 28]
12. TEAM_QUALITY_SCORING_STEPS: ±2 from optimal, bounded [4, 10]
13. PERFORMANCE_SCORING_STEPS: ±0.05 from optimal, bounded [0.05, 0.20]
14. MATCHUP_SCORING_STEPS: ±3 from optimal, bounded [4, 12]

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

    # Parameter definitions: (range_val, min_val, max_val)
    PARAM_DEFINITIONS = {
        'NORMALIZATION_MAX_SCALE': (10.0, 50.0, 500.0),
        'BASE_BYE_PENALTY': (10.0, 0.0, 200.0),
        'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY': (10.0, 0.0, 200.0),
        'PRIMARY_BONUS': (10.0, 0.0, 200.0),
        'SECONDARY_BONUS': (10.0, 0.0, 200.0),
        'ADP_SCORING_WEIGHT': (0.3, 0.0, 5.0),
        'PLAYER_RATING_SCORING_WEIGHT': (0.3, 0.0, 5.0),
        'PERFORMANCE_SCORING_WEIGHT': (0.3, 0.0, 5.0),
        'MATCHUP_SCORING_WEIGHT': (0.3, 0.0, 5.0),
        # Threshold STEPS parameters (NEW)
        'ADP_SCORING_STEPS': (5.0, 1.0, 60.0),
        'PLAYER_RATING_SCORING_STEPS': (4.0, 1.0, 50.0),
        'TEAM_QUALITY_SCORING_STEPS': (2.0, 1.0, 20.0),
        'PERFORMANCE_SCORING_STEPS': (0.05, 0.05, 0.5),
        'MATCHUP_SCORING_STEPS': (3.0, 1.0, 20.0),
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
            "DIRECTION": "BI_EXCELLENT_HI"
        }
    }

    # Scoring sections that need weights applied
    SCORING_SECTIONS = [
        'ADP_SCORING',
        'PLAYER_RATING_SCORING',
        'PERFORMANCE_SCORING',
        'MATCHUP_SCORING'
    ]

    # Parameter ordering for iterative optimization
    # Scalar parameters first, then weights, then threshold STEPS
    PARAMETER_ORDER = [
        'NORMALIZATION_MAX_SCALE',
        'BASE_BYE_PENALTY',
        'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY',
        'PRIMARY_BONUS',
        'SECONDARY_BONUS',
        # Multiplier Weights
        'ADP_SCORING_WEIGHT',
        'PLAYER_RATING_SCORING_WEIGHT',
        'PERFORMANCE_SCORING_WEIGHT',
        'MATCHUP_SCORING_WEIGHT',
        # Threshold STEPS (NEW)
        'ADP_SCORING_STEPS',
        'PLAYER_RATING_SCORING_STEPS',
        'TEAM_QUALITY_SCORING_STEPS',
        'PERFORMANCE_SCORING_STEPS',
        'MATCHUP_SCORING_STEPS',
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
        range_val: float,
        min_val: float,
        max_val: float
    ) -> List[float]:
        """
        Generate N+1 values for a parameter: optimal + N random variations.

        Args:
            param_name (str): Parameter name (for logging)
            optimal_val (float): Optimal/baseline value
            range_val (float): ± range for random values
            min_val (float): Minimum allowed value
            max_val (float): Maximum allowed value

        Returns:
            List[float]: (N+1) values [optimal, rand1, rand2, ..., randN]
                where N = self.num_test_values

        Example:
            >>> gen = ConfigGenerator(baseline_path, num_test_values=5)
            >>> values = gen.generate_parameter_values('NORMALIZATION_MAX_SCALE', 100, 20, 60, 140)
            >>> # Returns [100.0, 94.3, 118.7, 83.2, 105.9, 112.1] (6 values)
        """
        values = [optimal_val]

        # Generate N random values within range, bounded by min/max
        for i in range(self.num_test_values):
            # Random value in [optimal - range, optimal + range]
            rand_val = optimal_val + random.uniform(-range_val, range_val)
            # Clamp to [min_val, max_val]
            rand_val = max(min_val, min(max_val, rand_val))
            values.append(rand_val)

        self.logger.debug(f"{param_name}: {len(values)} values generated (min={min(values):.2f}, max={max(values):.2f})")
        return values

    def generate_multiplier_parameter_values(
        self,
        value_sets : Dict[str, List[float]],
        param_name: str
    ) -> Dict[str, List[float]]:
        base_weight = self.baseline_config['parameters'][param_name]["WEIGHT"]
        full_name = f"{param_name}_WEIGHT"
        range, min, max = self.param_definitions[full_name]
        value_sets[full_name] = self.generate_parameter_values(full_name, base_weight, range, min, max )

        return value_sets

    def generate_all_parameter_value_sets(self) -> Dict[str, List[float]]:
        """
        Generate value sets for all 14 parameters (5 scalar + 4 weights + 5 threshold STEPS).

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

        # BASE_BYE_PENALTY
        value_sets['BASE_BYE_PENALTY'] = self.generate_parameter_values(
            'BASE_BYE_PENALTY',
            params['BASE_BYE_PENALTY'],
            *self.param_definitions['BASE_BYE_PENALTY']
        )

        # DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY
        value_sets['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY'] = self.generate_parameter_values(
            'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY',
            params['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY'],
            *self.param_definitions['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY']
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

        # PERFORMANCE
        value_sets = self.generate_multiplier_parameter_values(value_sets, "PERFORMANCE_SCORING")

        # MATCHUP
        value_sets = self.generate_multiplier_parameter_values(value_sets, "MATCHUP_SCORING")

        # Threshold STEPS parameters (NEW) - Note: TEAM_QUALITY doesn't have a WEIGHT
        for scoring_type in ["ADP_SCORING", "PLAYER_RATING_SCORING", "TEAM_QUALITY_SCORING",
                             "PERFORMANCE_SCORING", "MATCHUP_SCORING"]:
            steps_param = f"{scoring_type}_STEPS"
            current_steps = params[scoring_type]['THRESHOLDS']['STEPS']
            range_val, min_val, max_val = self.param_definitions[steps_param]
            value_sets[steps_param] = self.generate_parameter_values(
                steps_param,
                current_steps,
                range_val,
                min_val,
                max_val
            )

        self.logger.info(f"Generated {len(value_sets)} parameter value sets")
        return value_sets

    def generate_all_combinations(self) -> List[Dict[str, float]]:
        """
        Generate all parameter combinations using itertools.product.

        Returns:
            List[Dict[str, float]]: All combinations, each a dict with 8 params

        Example:
            >>> combinations = gen.generate_all_combinations()
            >>> combinations[0]
            {'NORMALIZATION_MAX_SCALE': 100.0, 'BASE_BYE_PENALTY': 25.0, ...}
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
            range_val, min_val, max_val = self.param_definitions['NORMALIZATION_MAX_SCALE']
        elif param_name == 'BASE_BYE_PENALTY':
            current_val = params['BASE_BYE_PENALTY']
            range_val, min_val, max_val = self.param_definitions['BASE_BYE_PENALTY']
        elif param_name == 'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY':
            current_val = params['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY']
            range_val, min_val, max_val = self.param_definitions['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY']
        elif param_name == 'PRIMARY_BONUS':
            current_val = params['DRAFT_ORDER_BONUSES']['PRIMARY']
            range_val, min_val, max_val = self.param_definitions['PRIMARY_BONUS']
        elif param_name == 'SECONDARY_BONUS':
            current_val = params['DRAFT_ORDER_BONUSES']['SECONDARY']
            range_val, min_val, max_val = self.param_definitions['SECONDARY_BONUS']
        elif '_WEIGHT' in param_name:
            # Extract section and multiplier type
            # Format: SECTION_SCORING_WEIGHT
            parts = param_name.split('_WEIGHT')
            section = parts[0]  # e.g., 'ADP_SCORING'

            current_val = params[section]['WEIGHT']
            range_val, min_val, max_val = self.param_definitions[param_name]
        elif '_STEPS' in param_name:
            # Extract section for threshold STEPS
            # Format: SECTION_SCORING_STEPS
            parts = param_name.split('_STEPS')
            section = parts[0]  # e.g., 'ADP_SCORING'

            current_val = params[section]['THRESHOLDS']['STEPS']
            range_val, min_val, max_val = self.param_definitions[param_name]
        else:
            raise ValueError(f"Unknown parameter: {param_name}")

        # Generate test values
        test_values = self.generate_parameter_values(
            param_name,
            current_val,
            range_val,
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
        combination['BASE_BYE_PENALTY'] = params['BASE_BYE_PENALTY']
        combination['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY'] = params['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY']
        combination['PRIMARY_BONUS'] = params['DRAFT_ORDER_BONUSES']['PRIMARY']
        combination['SECONDARY_BONUS'] = params['DRAFT_ORDER_BONUSES']['SECONDARY']

        # WEIGHTS for each section
        for section in ['ADP', 'PLAYER_RATING', 'PERFORMANCE', 'MATCHUP']:
            param_name = f'{section}_SCORING_WEIGHT'
            combination[param_name] = params[f'{section}_SCORING']['WEIGHT']

        # STEPS for each scoring type (NEW) - only if parameterized format
        for section in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            param_name = f'{section}_SCORING_STEPS'
            thresholds = params[f'{section}_SCORING']['THRESHOLDS']
            # Check if using parameterized format (has STEPS key)
            if 'STEPS' in thresholds:
                combination[param_name] = thresholds['STEPS']
            else:
                # Old format - use default value from baseline if it exists
                # This handles backward compatibility with test fixtures
                if 'THRESHOLDS' in self.baseline_config['parameters'][f'{section}_SCORING']:
                    baseline_thresholds = self.baseline_config['parameters'][f'{section}_SCORING']['THRESHOLDS']
                    if 'STEPS' in baseline_thresholds:
                        combination[param_name] = baseline_thresholds['STEPS']

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
        params['BASE_BYE_PENALTY'] = combination['BASE_BYE_PENALTY']
        params['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY'] = combination['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY']
        params['DRAFT_ORDER_BONUSES']['PRIMARY'] = combination['PRIMARY_BONUS']
        params['DRAFT_ORDER_BONUSES']['SECONDARY'] = combination['SECONDARY_BONUS']

        # Update weights
        for parameter in ['ADP', 'PLAYER_RATING', 'PERFORMANCE', 'MATCHUP']:
            params[f'{parameter}_SCORING']['WEIGHT'] = combination[f'{parameter}_SCORING_WEIGHT']

        # Update threshold STEPS (NEW)
        for parameter in ['ADP', 'PLAYER_RATING', 'TEAM_QUALITY', 'PERFORMANCE', 'MATCHUP']:
            steps_param = f'{parameter}_SCORING_STEPS'
            if steps_param in combination:
                fixed_params = self.THRESHOLD_FIXED_PARAMS[f'{parameter}_SCORING']
                params[f'{parameter}_SCORING']['THRESHOLDS'] = {
                    'BASE_POSITION': fixed_params['BASE_POSITION'],
                    'DIRECTION': fixed_params['DIRECTION'],
                    'STEPS': combination[steps_param]
                }

        return config

    def generate_all_configs(self) -> List[dict]:
        """
        Generate all complete configuration dictionaries.

        Returns:
            List[dict]: All configurations ready for simulation

        Note:
            Total configs = (num_test_values + 1)^14
            Each config is ~10KB
            Example: 6^14 = ~78 billion configs = impractical for full cartesian product
            For practical use, use iterative optimization instead
        """
        total_configs = (self.num_test_values + 1) ** 14
        self.logger.info(f"Generating all {total_configs:,} complete configurations")

        combinations = self.generate_all_combinations()
        configs = []

        for idx, combo in enumerate(combinations):
            config = self.create_config_dict(combo)
            configs.append(config)

        self.logger.info(f"All {len(configs)} configurations generated")
        return configs
