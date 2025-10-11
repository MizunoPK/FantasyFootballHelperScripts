"""
Configuration Generator

Generates parameter combinations for simulation optimization. Creates 46,656
different configurations (6^6) by varying 6 key parameters, with 6 values per
parameter (optimal + 5 random variations).

Parameters Varied:
- NORMALIZATION_MAX_SCALE: ±20 from optimal, bounded [60, 140]
- BASE_BYE_PENALTY: ±10 from optimal, bounded [0, 40]
- DRAFT_ORDER_BONUSES.PRIMARY: ±20 from optimal, bounded [25, 100]
- DRAFT_ORDER_BONUSES.SECONDARY: ±20 from optimal, bounded [25, 75]
- POSITIVE_MULTIPLIER: ±0.1 from optimal, bounded [1.0, 1.3]
- NEGATIVE_MULTIPLIER: ±0.1 from optimal, bounded [0.7, 1.0]

Multiplier Application:
- POSITIVE_MULTIPLIER applies to GOOD and EXCELLENT ratings in all sections
- NEGATIVE_MULTIPLIER applies to POOR and VERY_POOR ratings in all sections
- For each config, generates unique multipliers per section (±0.05 variance)
- THRESHOLDS remain constant (only MULTIPLIERS vary)

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

    Creates 46,656 different configurations by varying 6 parameters with
    6 values each (optimal + 5 random variations). Applies multipliers
    to all scoring sections based on POSITIVE_MULTIPLIER and NEGATIVE_MULTIPLIER.

    Attributes:
        baseline_config (dict): Base configuration to vary from
        param_definitions (dict): Parameter ranges and bounds
        logger: Logger instance
    """

    # Parameter definitions: (range_val, min_val, max_val)
    PARAM_DEFINITIONS = {
        'NORMALIZATION_MAX_SCALE': (20.0, 60.0, 140.0),
        'BASE_BYE_PENALTY': (10.0, 0.0, 40.0),
        'PRIMARY_BONUS': (20.0, 25.0, 100.0),
        'SECONDARY_BONUS': (20.0, 25.0, 75.0),
        'POSITIVE_MULTIPLIER': (0.1, 1.0, 1.3),
        'NEGATIVE_MULTIPLIER': (0.1, 0.7, 1.0)
    }

    # Scoring sections that need multipliers applied
    SCORING_SECTIONS = [
        'ADP_SCORING',
        'PLAYER_RATING_SCORING',
        'TEAM_QUALITY_SCORING',
        'CONSISTENCY_SCORING',
        'MATCHUP_SCORING'
    ]

    def __init__(self, baseline_config_path: Path):
        """
        Initialize ConfigGenerator with baseline configuration.

        Args:
            baseline_config_path (Path): Path to baseline config JSON file

        Raises:
            FileNotFoundError: If baseline config file doesn't exist
            ValueError: If baseline config is invalid
        """
        self.logger = get_logger()
        self.logger.info(f"Initializing ConfigGenerator with baseline: {baseline_config_path}")

        self.baseline_config = self.load_baseline_config(baseline_config_path)
        self.param_definitions = self.PARAM_DEFINITIONS

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
        Generate 6 values for a parameter: optimal + 5 random variations.

        Args:
            param_name (str): Parameter name (for logging)
            optimal_val (float): Optimal/baseline value
            range_val (float): ± range for random values
            min_val (float): Minimum allowed value
            max_val (float): Maximum allowed value

        Returns:
            List[float]: 6 values [optimal, rand1, rand2, rand3, rand4, rand5]

        Example:
            >>> gen = ConfigGenerator(baseline_path)
            >>> values = gen.generate_parameter_values('NORMALIZATION_MAX_SCALE', 100, 20, 60, 140)
            >>> # Returns [100.0, 94.3, 118.7, 83.2, 105.9, 112.1]
        """
        values = [optimal_val]

        # Generate 5 random values within range, bounded by min/max
        for i in range(5):
            # Random value in [optimal - range, optimal + range]
            rand_val = optimal_val + random.uniform(-range_val, range_val)
            # Clamp to [min_val, max_val]
            rand_val = max(min_val, min(max_val, rand_val))
            values.append(rand_val)

        self.logger.debug(f"{param_name}: {len(values)} values generated (min={min(values):.2f}, max={max(values):.2f})")
        return values

    def generate_all_parameter_value_sets(self) -> Dict[str, List[float]]:
        """
        Generate value sets for all 6 parameters.

        Returns:
            Dict[str, List[float]]: {param_name: [6 values]}

        Example:
            >>> value_sets = gen.generate_all_parameter_value_sets()
            >>> value_sets['NORMALIZATION_MAX_SCALE']
            [100.0, 94.3, 118.7, 83.2, 105.9, 112.1]
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

        # POSITIVE_MULTIPLIER (extract from baseline's EXCELLENT multipliers - average across sections)
        pos_mult_baseline = self._extract_baseline_positive_multiplier(params)
        value_sets['POSITIVE_MULTIPLIER'] = self.generate_parameter_values(
            'POSITIVE_MULTIPLIER',
            pos_mult_baseline,
            *self.param_definitions['POSITIVE_MULTIPLIER']
        )

        # NEGATIVE_MULTIPLIER (extract from baseline's POOR multipliers - average across sections)
        neg_mult_baseline = self._extract_baseline_negative_multiplier(params)
        value_sets['NEGATIVE_MULTIPLIER'] = self.generate_parameter_values(
            'NEGATIVE_MULTIPLIER',
            neg_mult_baseline,
            *self.param_definitions['NEGATIVE_MULTIPLIER']
        )

        self.logger.info(f"Generated {len(value_sets)} parameter value sets")
        return value_sets

    def _extract_baseline_positive_multiplier(self, params: dict) -> float:
        """
        Extract average EXCELLENT multiplier from baseline config.

        Args:
            params (dict): Parameters section of config

        Returns:
            float: Average EXCELLENT multiplier across all sections
        """
        excellent_mults = []
        for section in self.SCORING_SECTIONS:
            if section in params and 'MULTIPLIERS' in params[section]:
                excellent_mults.append(params[section]['MULTIPLIERS']['EXCELLENT'])

        avg = sum(excellent_mults) / len(excellent_mults) if excellent_mults else 1.2
        self.logger.debug(f"Baseline POSITIVE_MULTIPLIER (avg EXCELLENT): {avg:.3f}")
        return avg

    def _extract_baseline_negative_multiplier(self, params: dict) -> float:
        """
        Extract average POOR multiplier from baseline config.

        Args:
            params (dict): Parameters section of config

        Returns:
            float: Average POOR multiplier across all sections
        """
        poor_mults = []
        for section in self.SCORING_SECTIONS:
            if section in params and 'MULTIPLIERS' in params[section]:
                poor_mults.append(params[section]['MULTIPLIERS']['POOR'])

        avg = sum(poor_mults) / len(poor_mults) if poor_mults else 0.85
        self.logger.debug(f"Baseline NEGATIVE_MULTIPLIER (avg POOR): {avg:.3f}")
        return avg

    def generate_all_combinations(self) -> List[Dict[str, float]]:
        """
        Generate all parameter combinations using itertools.product.

        Returns:
            List[Dict[str, float]]: 46,656 combinations, each a dict with 6 params

        Example:
            >>> combinations = gen.generate_all_combinations()
            >>> len(combinations)
            46656
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

        self.logger.info(f"Generated {len(combinations)} combinations (expected 46,656)")

        if len(combinations) != 46656:
            self.logger.warning(f"Expected 46,656 combinations, got {len(combinations)}")

        return combinations

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
            3. Apply multipliers to all scoring sections
        """
        # Deep copy baseline to avoid mutations
        config = copy.deepcopy(self.baseline_config)
        params = config['parameters']

        # Update scalar parameters
        params['NORMALIZATION_MAX_SCALE'] = combination['NORMALIZATION_MAX_SCALE']
        params['BASE_BYE_PENALTY'] = combination['BASE_BYE_PENALTY']
        params['DRAFT_ORDER_BONUSES']['PRIMARY'] = combination['PRIMARY_BONUS']
        params['DRAFT_ORDER_BONUSES']['SECONDARY'] = combination['SECONDARY_BONUS']

        # Apply multipliers to all scoring sections
        self.apply_multipliers(
            params,
            combination['POSITIVE_MULTIPLIER'],
            combination['NEGATIVE_MULTIPLIER']
        )

        return config

    def apply_multipliers(self, params: dict, pos_mult: float, neg_mult: float) -> None:
        """
        Apply POSITIVE and NEGATIVE multipliers to all scoring sections.

        Modifies params dict in-place by updating MULTIPLIERS in each section.

        Args:
            params (dict): Parameters section of config (modified in-place)
            pos_mult (float): Base positive multiplier (for GOOD/EXCELLENT)
            neg_mult (float): Base negative multiplier (for POOR/VERY_POOR)

        Process:
            For each section (ADP, Player Rating, Team Quality, Consistency, Matchup):
            - GOOD: random.uniform(pos_mult - 0.05, pos_mult + 0.05)
            - EXCELLENT: random.uniform(pos_mult - 0.05, pos_mult + 0.05) [different from GOOD]
            - POOR: random.uniform(neg_mult - 0.05, neg_mult + 0.05)
            - VERY_POOR: random.uniform(neg_mult - 0.05, neg_mult + 0.05) [different from POOR]
            - NEUTRAL: Always 1.0 (unchanged)
        """
        for section in self.SCORING_SECTIONS:
            if section not in params:
                self.logger.warning(f"Section {section} not found in config")
                continue

            if 'MULTIPLIERS' not in params[section]:
                self.logger.warning(f"MULTIPLIERS not found in {section}")
                continue

            mults = params[section]['MULTIPLIERS']

            # Generate unique multipliers for this section
            # EXCELLENT and GOOD both use pos_mult base but get different random values
            mults['EXCELLENT'] = random.uniform(pos_mult - 0.05, pos_mult + 0.05)
            mults['GOOD'] = random.uniform(pos_mult - 0.05, pos_mult + 0.05)

            # VERY_POOR and POOR both use neg_mult base but get different random values
            mults['VERY_POOR'] = random.uniform(neg_mult - 0.05, neg_mult + 0.05)
            mults['POOR'] = random.uniform(neg_mult - 0.05, neg_mult + 0.05)

            # NEUTRAL always 1.0
            if 'NEUTRAL' in mults:
                mults['NEUTRAL'] = 1.0

            # Clamp to reasonable bounds
            for key in ['EXCELLENT', 'GOOD', 'POOR', 'VERY_POOR']:
                if key in mults:
                    mults[key] = max(0.5, min(1.5, mults[key]))

    def generate_all_configs(self) -> List[dict]:
        """
        Generate all 46,656 complete configuration dictionaries.

        Returns:
            List[dict]: All configurations ready for simulation

        Note:
            This can take a few seconds and uses significant memory.
            Each config is ~10KB, total ~450MB for all configs.
        """
        self.logger.info("Generating all 46,656 complete configurations")

        combinations = self.generate_all_combinations()
        configs = []

        for idx, combo in enumerate(combinations):
            config = self.create_config_dict(combo)
            configs.append(config)

            if (idx + 1) % 5000 == 0:
                self.logger.info(f"Generated {idx + 1}/{len(combinations)} configs")

        self.logger.info(f"All {len(configs)} configurations generated")
        return configs
