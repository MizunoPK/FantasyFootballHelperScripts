"""
Configuration Generator

Generates parameter combinations for simulation optimization. Creates 7,776
different configurations (6^5) by varying 5 key parameters, with 6 values per
parameter (optimal + 5 random variations).

Parameters Varied:
- NORMALIZATION_MAX_SCALE: ±20 from optimal, bounded [60, 140]
- BASE_BYE_PENALTY: ±10 from optimal, bounded [0, 40]
- DRAFT_ORDER_BONUSES.PRIMARY: ±20 from optimal, bounded [25, 100]
- DRAFT_ORDER_BONUSES.SECONDARY: ±20 from optimal, bounded [25, 75]
- ADP_SCORING_WEIGHT, PLAYER_RATING_SCORING_WEIGHT, PERFORMANCE_SCORING_WEIGHT, MATCHUP_SCORING_WEIGHT

Author: Kai Mizuno
Date: 2024
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
        'NORMALIZATION_MAX_SCALE': (10.0, 50.0, 150.0),
        'BASE_BYE_PENALTY': (10.0, 0.0, 50.0),
        'PRIMARY_BONUS': (10.0, 0.0, 100.0),
        'SECONDARY_BONUS': (10.0, 0.0, 75.0),
        'ADP_SCORING_WEIGHT': (0.3, 0.0, 5.0),
        'PLAYER_RATING_SCORING_WEIGHT': (0.3, 0.0, 5.0),
        'PERFORMANCE_SCORING_WEIGHT': (0.3, 0.0, 5.0),
        'MATCHUP_SCORING_WEIGHT': (0.3, 0.0, 5.0),
    }

    # Scoring sections that need weights applied
    SCORING_SECTIONS = [
        'ADP_SCORING',
        'PLAYER_RATING_SCORING',
        'PERFORMANCE_SCORING',
        'MATCHUP_SCORING'
    ]

    # Parameter ordering for iterative optimization
    # Scalar parameters first, then weights by section
    PARAMETER_ORDER = [
        'PERFORMANCE_SCORING_WEIGHT',
        'NORMALIZATION_MAX_SCALE',
        'BASE_BYE_PENALTY',
        'PRIMARY_BONUS',
        'SECONDARY_BONUS',
        # Multiplier Weights
        'ADP_SCORING_WEIGHT',
        'PLAYER_RATING_SCORING_WEIGHT',
        'MATCHUP_SCORING_WEIGHT',
    ]

    def __init__(self, baseline_config_path: Path, num_test_values: int = 5):
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
        Generate value sets for all 8 parameters (4 scalar + 4 weights).

        Returns:
            Dict[str, List[float]]: {param_name: [N+1 values]} where N = num_test_values

        Example:
            >>> gen = ConfigGenerator(baseline_path, num_test_values=5)
            >>> value_sets = gen.generate_all_parameter_value_sets()
            >>> value_sets['NORMALIZATION_MAX_SCALE']
            [100.0, 94.3, 118.7, 83.2, 105.9, 112.1]  # 6 values
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
        elif param_name == 'PRIMARY_BONUS':
            current_val = params['DRAFT_ORDER_BONUSES']['PRIMARY']
            range_val, min_val, max_val = self.param_definitions['PRIMARY_BONUS']
        elif param_name == 'SECONDARY_BONUS':
            current_val = params['DRAFT_ORDER_BONUSES']['SECONDARY']
            range_val, min_val, max_val = self.param_definitions['SECONDARY_BONUS']
        elif '_WEIGHT' in param_name:
            # Extract section and multiplier type
            # Format: SECTION_SCORING_MULTIPLIERS_TYPE
            parts = param_name.split('_WEIGHT')
            section = parts[0]  # e.g., 'ADP_SCORING'

            current_val = params[section]['WEIGHT']
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
        combination['PRIMARY_BONUS'] = params['DRAFT_ORDER_BONUSES']['PRIMARY']
        combination['SECONDARY_BONUS'] = params['DRAFT_ORDER_BONUSES']['SECONDARY']

        # WEIGHTS for each section
        for section in ['ADP', 'PLAYER_RATING', 'PERFORMANCE', 'MATCHUP']:
            param_name = f'{section}_SCORING_WEIGHT'
            combination[param_name] = params[f'{section}_SCORING']['WEIGHT']

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
        params['DRAFT_ORDER_BONUSES']['PRIMARY'] = combination['PRIMARY_BONUS']
        params['DRAFT_ORDER_BONUSES']['SECONDARY'] = combination['SECONDARY_BONUS']
        for parameter in ['ADP', 'PLAYER_RATING', 'PERFORMANCE', 'MATCHUP']:
            params[f'{parameter}_SCORING']['WEIGHT'] = combination[f'{parameter}_SCORING_WEIGHT']
        return config

    def generate_all_configs(self) -> List[dict]:
        """
        Generate all complete configuration dictionaries.

        Returns:
            List[dict]: All configurations ready for simulation

        Note:
            Total configs = (num_test_values + 1)^8
            Each config is ~10KB
            Example: 6^8 = 1,679,616 configs = ~16GB memory
        """
        total_configs = (self.num_test_values + 1) ** 8
        self.logger.info(f"Generating all {total_configs:,} complete configurations")

        combinations = self.generate_all_combinations()
        configs = []

        for idx, combo in enumerate(combinations):
            config = self.create_config_dict(combo)
            configs.append(config)

        self.logger.info(f"All {len(configs)} configurations generated")
        return configs
