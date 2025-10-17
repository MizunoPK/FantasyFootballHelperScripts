"""
Configuration Manager

Centralized configuration management for Fantasy Football League Helper.
Loads and validates all league settings from league_config.json, providing
type-safe access to scoring parameters, thresholds, multipliers, and
mode-specific configurations.

This module handles:
- Loading and validating JSON configuration
- Extracting NFL settings (season, week, scoring format)
- Managing scoring thresholds and multipliers for all 9 scoring steps
- Providing draft order bonuses and strategy
- Calculating penalties for injuries and bye weeks

Author: Kai Mizuno
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import sys
sys.path.append(str(Path(__file__).parent.parent))
import constants as Constants

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer


class ConfigKeys:
    """
    Constants for JSON configuration keys.

    This class defines all valid keys used in league_config.json, providing
    a centralized reference for configuration structure. Using constants
    prevents typos and makes refactoring easier.

    The configuration follows a hierarchical structure:
    - Top level: config_name, description, parameters
    - Parameters: NFL settings, scoring configs, mode-specific settings
    - Nested: thresholds, multipliers, bonuses for each scoring category
    """

    # Top Level Keys
    CONFIG_NAME = "config_name"
    DESCRIPTION = "description"
    PARAMETERS = "parameters"

    # Parameter Keys
    CURRENT_NFL_WEEK = "CURRENT_NFL_WEEK"
    NFL_SEASON = "NFL_SEASON"
    NFL_SCORING_FORMAT = "NFL_SCORING_FORMAT"
    NORMALIZATION_MAX_SCALE = "NORMALIZATION_MAX_SCALE"
    BASE_BYE_PENALTY = "BASE_BYE_PENALTY"
    INJURY_PENALTIES = "INJURY_PENALTIES"
    ADP_SCORING = "ADP_SCORING"
    PLAYER_RATING_SCORING = "PLAYER_RATING_SCORING"
    TEAM_QUALITY_SCORING = "TEAM_QUALITY_SCORING"
    CONSISTENCY_SCORING = "CONSISTENCY_SCORING"  # Deprecated - kept for backwards compatibility
    PERFORMANCE_SCORING = "PERFORMANCE_SCORING"
    MATCHUP_SCORING = "MATCHUP_SCORING"
    DRAFT_ORDER_BONUSES = "DRAFT_ORDER_BONUSES"
    DRAFT_ORDER = "DRAFT_ORDER"

    # Draft Order scoring
    DRAFT_ORDER_PRIMARY_LABEL = "P"
    DRAFT_ORDER_SECONDARY_LABEL = "S"

    # Nested Structure Keys
    MULTIPLIERS = "MULTIPLIERS"
    THRESHOLDS = "THRESHOLDS"
    MIN_WEEKS = "MIN_WEEKS"
    WEIGHT = "WEIGHT"

    # Injury Level Keys
    INJURY_LOW = "LOW"
    INJURY_MEDIUM = "MEDIUM"
    INJURY_HIGH = "HIGH"

    # Bonus Type Keys
    BONUS_PRIMARY = "PRIMARY"
    BONUS_SECONDARY = "SECONDARY"

    # Threshold/Multiplier Level Keys
    VERY_POOR = "VERY_POOR"
    POOR = "POOR"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"
    NEUTRAL = "NEUTRAL"

    # Parameterized Threshold Keys (new system)
    BASE_POSITION = "BASE_POSITION"
    DIRECTION = "DIRECTION"
    STEPS = "STEPS"

    # Direction Values
    DIRECTION_INCREASING = "INCREASING"
    DIRECTION_DECREASING = "DECREASING"
    DIRECTION_BI_EXCELLENT_HI = "BI_EXCELLENT_HI"
    DIRECTION_BI_EXCELLENT_LOW = "BI_EXCELLENT_LOW"

    # Optional calculated field (for transparency in config files)
    CALCULATED = "_calculated"


class ConfigManager:
    """
    Manages all configuration settings from league_config.json.

    This class is the single source of truth for all league configuration,
    including scoring parameters, thresholds, multipliers, and mode-specific
    settings. It validates the JSON structure and provides type-safe access
    to all configuration values.

    Attributes:
        config_name (str): Name of the configuration (e.g., "Default", "Test High Normalization")
        description (str): Description of this configuration's purpose
        current_nfl_week (int): Current NFL week number
        nfl_season (int): Current NFL season year
        nfl_scoring_format (str): Scoring format ("ppr", "std", "half")
        normalization_max_scale (float): Maximum scale for normalized scores
        base_bye_penalty (float): Base penalty per bye week conflict
        injury_penalties (Dict[str, float]): Penalties by injury risk level (LOW/MEDIUM/HIGH)
        adp_scoring (Dict): ADP thresholds and multipliers
        player_rating_scoring (Dict): Player rating thresholds and multipliers
        team_quality_scoring (Dict): Team quality thresholds and multipliers
        consistency_scoring (Dict): Consistency thresholds and multipliers
        matchup_scoring (Dict): Matchup thresholds and multipliers
        draft_order_bonuses (Dict): PRIMARY and SECONDARY draft bonuses
        draft_order (List[Dict]): Draft strategy by round

    Example:
        >>> config = ConfigManager(Path("./data"))
        >>> adp_mult = config.get_adp_multiplier(15)  # ADP of 15 → returns multiplier
        >>> draft_bonus = config.get_draft_order_bonus("RB", 1)  # RB in round 1 → returns bonus
    """

    def __init__(self, data_folder: Path) -> None:
        """
        Initialize the config manager and load configuration.

        Args:
            data_folder (Path): Path to the data directory containing league_config.json

        Raises:
            FileNotFoundError: If league_config.json is not found
            ValueError: If configuration structure is invalid or missing required fields
        """
        self.keys = ConfigKeys()
        self.config_name: str = ""
        self.description: str = ""
        self.parameters: Dict[str, Any] = {}
        self.logger = get_logger()

        # Set config path to data/league_config.json
        self.config_path = data_folder / 'league_config.json'

        # League settings
        self.current_nfl_week: int = 0
        self.nfl_season: int = 0
        self.nfl_scoring_format: str = ""

        # Scoring parameters
        self.normalization_max_scale: float = 0.0
        self.base_bye_penalty: float = 0.0
        self.injury_penalties: Dict[str, float] = {}
        self.adp_scoring: Dict[str, Any] = {}
        self.player_rating_scoring: Dict[str, Any] = {}
        self.team_quality_scoring: Dict[str, Any] = {}
        self.consistency_scoring: Dict[str, Any] = {}  # Deprecated - kept for backwards compatibility
        self.performance_scoring: Dict[str, Any] = {}
        self.matchup_scoring: Dict[str, Any] = {}

        # Add to Roster mode settings
        self.draft_order_bonuses: Dict[str, float] = {}
        self.draft_order: List[Dict[str, str]] = []

        # Threshold calculation cache
        self._threshold_cache: Dict[Tuple[str, float, str, float], Dict[str, float]] = {}

        self._load_config()

    def validate_threshold_params(self, base_pos: float, direction: str, steps: float) -> bool:
        """
        Validate threshold parameters.

        Args:
            base_pos: Base position value (typically 0)
            direction: Direction type (INCREASING, DECREASING, BI_EXCELLENT_HI, BI_EXCELLENT_LOW)
            steps: Step size between thresholds (must be positive)

        Returns:
            True if parameters are valid

        Raises:
            ValueError: If parameters are invalid
        """
        import math

        # STEPS must be positive
        if steps <= 0:
            self.logger.error(f"STEPS must be positive, got {steps}")
            raise ValueError(f"STEPS must be positive, got {steps}")

        # Must be finite
        if not math.isfinite(base_pos) or not math.isfinite(steps):
            self.logger.error("BASE_POSITION and STEPS must be finite")
            raise ValueError("BASE_POSITION and STEPS must be finite")

        # DIRECTION must be valid
        valid_dirs = [
            self.keys.DIRECTION_INCREASING,
            self.keys.DIRECTION_DECREASING,
            self.keys.DIRECTION_BI_EXCELLENT_HI,
            self.keys.DIRECTION_BI_EXCELLENT_LOW
        ]
        if direction not in valid_dirs:
            self.logger.error(f"DIRECTION must be one of {valid_dirs}, got '{direction}'")
            raise ValueError(f"DIRECTION must be one of {valid_dirs}, got '{direction}'")

        return True

    def calculate_thresholds(self, base_pos: float, direction: str, steps: float,
                            scoring_type: str = "") -> Dict[str, float]:
        """
        Calculate threshold values from parameters.

        This method implements the parameterized threshold system, replacing
        hardcoded threshold values with calculated ones based on:
        - BASE_POSITION: Starting point (typically 0)
        - DIRECTION: How thresholds are arranged
        - STEPS: Spacing between threshold levels

        Args:
            base_pos: Base position (typically 0)
            direction: INCREASING, DECREASING, BI_EXCELLENT_HI, or BI_EXCELLENT_LOW
            steps: Step size between thresholds
            scoring_type: Optional scoring type for caching (e.g., "ADP_SCORING")

        Returns:
            Dict with VERY_POOR, POOR, GOOD, EXCELLENT threshold values

        Examples:
            >>> # INCREASING (player rating): VP=20, P=40, G=60, E=80
            >>> config.calculate_thresholds(0, "INCREASING", 20)
            {'VERY_POOR': 20, 'POOR': 40, 'GOOD': 60, 'EXCELLENT': 80}

            >>> # DECREASING (ADP): E=37.5, G=75, P=112.5, VP=150
            >>> config.calculate_thresholds(0, "DECREASING", 37.5)
            {'EXCELLENT': 37.5, 'GOOD': 75, 'POOR': 112.5, 'VERY_POOR': 150}

            >>> # BI_EXCELLENT_HI (performance): VP=-0.2, P=-0.1, G=0.1, E=0.2
            >>> config.calculate_thresholds(0, "BI_EXCELLENT_HI", 0.1)
            {'VERY_POOR': -0.2, 'POOR': -0.1, 'GOOD': 0.1, 'EXCELLENT': 0.2}
        """
        # Check cache first
        cache_key = (scoring_type, base_pos, direction, steps)
        if cache_key in self._threshold_cache:
            return self._threshold_cache[cache_key]

        # Validate parameters
        self.validate_threshold_params(base_pos, direction, steps)

        # Calculate thresholds based on direction
        if direction == self.keys.DIRECTION_INCREASING:
            # Higher values = better (e.g., player rating)
            # Formula: VP=base+1s, P=base+2s, G=base+3s, E=base+4s
            thresholds = {
                self.keys.VERY_POOR: base_pos + steps,
                self.keys.POOR: base_pos + (2 * steps),
                self.keys.GOOD: base_pos + (3 * steps),
                self.keys.EXCELLENT: base_pos + (4 * steps)
            }

        elif direction == self.keys.DIRECTION_DECREASING:
            # Lower values = better (e.g., ADP rank)
            # Formula: E=base+1s, G=base+2s, P=base+3s, VP=base+4s
            thresholds = {
                self.keys.EXCELLENT: base_pos + steps,
                self.keys.GOOD: base_pos + (2 * steps),
                self.keys.POOR: base_pos + (3 * steps),
                self.keys.VERY_POOR: base_pos + (4 * steps)
            }

        elif direction == self.keys.DIRECTION_BI_EXCELLENT_HI:
            # Bidirectional: positive deviation = excellent
            # Formula: VP=base-2s, P=base-1s, G=base+1s, E=base+2s (1x/2x multipliers per user Q4)
            thresholds = {
                self.keys.VERY_POOR: base_pos - (steps * 2),
                self.keys.POOR: base_pos - steps,
                self.keys.GOOD: base_pos + steps,
                self.keys.EXCELLENT: base_pos + (steps * 2)
            }

        elif direction == self.keys.DIRECTION_BI_EXCELLENT_LOW:
            # Bidirectional: negative deviation = excellent (rare case)
            # Formula: E=base-2s, G=base-1s, P=base+1s, VP=base+2s (1x/2x multipliers)
            thresholds = {
                self.keys.EXCELLENT: base_pos - (steps * 2),
                self.keys.GOOD: base_pos - steps,
                self.keys.POOR: base_pos + steps,
                self.keys.VERY_POOR: base_pos + (steps * 2)
            }

        else:
            # This should never happen due to validation, but included for safety
            raise ValueError(f"Invalid direction: {direction}")

        # Store in cache
        self._threshold_cache[cache_key] = thresholds
        return thresholds

    def _load_config(self) -> None:
        """
        Load and validate configuration from JSON file.

        Reads league_config.json, validates its structure, extracts all parameters,
        and stores them in instance variables for type-safe access.

        Raises:
            FileNotFoundError: If league_config.json does not exist
            json.JSONDecodeError: If the JSON is malformed
            ValueError: If required fields are missing or invalid
        """
        self.logger.debug(f"Loading configuration from: {self.config_path}")

        if not self.config_path.exists():
            self.logger.error(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
            self.logger.debug("Successfully loaded JSON configuration")
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            raise

        # Validate required fields
        self._validate_config_structure(data)

        # Store configuration data
        self.config_name = data.get(self.keys.CONFIG_NAME, "")
        self.description = data.get(self.keys.DESCRIPTION, "")
        self.parameters = data.get(self.keys.PARAMETERS, {})

        self.logger.debug(f"Loaded configuration: '{self.config_name}'")
        self.logger.debug(f"Description: {self.description}")
        self.logger.debug(f"Parameters count: {len(self.parameters)}")

        # Extract and validate all parameters
        self._extract_parameters()
        self.logger.debug("Configuration loaded and validated successfully")

    def _validate_config_structure(self, data: Dict[str, Any]) -> None:
        """
        Validate that the configuration has the required structure.

        Args:
            data: The loaded JSON data

        Raises:
            ValueError: If required fields are missing or have invalid types
        """
        required_fields = [self.keys.CONFIG_NAME, self.keys.DESCRIPTION, self.keys.PARAMETERS]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            error_msg = f"Configuration missing required fields: {', '.join(missing_fields)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        if not isinstance(data[self.keys.PARAMETERS], dict):
            error_msg = "'parameters' field must be a dictionary"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.logger.debug("Configuration structure validation passed")

    def _extract_parameters(self) -> None:
        """Extract and validate all parameters from the config."""
        # Required parameters
        required_params = [
            self.keys.CURRENT_NFL_WEEK,
            self.keys.NFL_SEASON,
            self.keys.NFL_SCORING_FORMAT,
            self.keys.NORMALIZATION_MAX_SCALE,
            self.keys.BASE_BYE_PENALTY,
            self.keys.INJURY_PENALTIES,
            self.keys.ADP_SCORING,
            self.keys.PLAYER_RATING_SCORING,
            self.keys.TEAM_QUALITY_SCORING,
            self.keys.PERFORMANCE_SCORING,
            self.keys.MATCHUP_SCORING,
            self.keys.DRAFT_ORDER_BONUSES,
            self.keys.DRAFT_ORDER,
        ]

        missing_params = [p for p in required_params if p not in self.parameters]
        if missing_params:
            raise ValueError(
                f"Config missing required parameters: {', '.join(missing_params)}"
            )

        # Extract league-wide parameters
        self.current_nfl_week = self.parameters[self.keys.CURRENT_NFL_WEEK]
        self.nfl_season = self.parameters[self.keys.NFL_SEASON]
        self.nfl_scoring_format = self.parameters[self.keys.NFL_SCORING_FORMAT]
        self.normalization_max_scale = self.parameters[self.keys.NORMALIZATION_MAX_SCALE]
        self.base_bye_penalty = self.parameters[self.keys.BASE_BYE_PENALTY]
        self.injury_penalties = self.parameters[self.keys.INJURY_PENALTIES]
        self.adp_scoring = self.parameters[self.keys.ADP_SCORING]
        self.player_rating_scoring = self.parameters[self.keys.PLAYER_RATING_SCORING]
        self.team_quality_scoring = self.parameters[self.keys.TEAM_QUALITY_SCORING]
        self.performance_scoring = self.parameters[self.keys.PERFORMANCE_SCORING]
        # Keep consistency_scoring as fallback for backwards compatibility
        self.consistency_scoring = self.parameters.get(self.keys.CONSISTENCY_SCORING, self.performance_scoring)
        self.matchup_scoring = self.parameters[self.keys.MATCHUP_SCORING]

        # Extract Add to Roster mode parameters
        self.draft_order_bonuses = self.parameters[self.keys.DRAFT_ORDER_BONUSES]
        self.draft_order = self.parameters[self.keys.DRAFT_ORDER]

        # Extract Starter Helper mode parameters (optional - not in current config)
        # Note: matchup_multipliers are accessed directly from matchup_scoring[self.keys.MULTIPLIERS]

        # Validate injury penalties structure
        required_injury_levels = [self.keys.INJURY_LOW, self.keys.INJURY_MEDIUM, self.keys.INJURY_HIGH]
        missing_levels = [
            level for level in required_injury_levels
            if level not in self.injury_penalties
        ]
        if missing_levels:
            raise ValueError(
                f"INJURY_PENALTIES missing levels: {', '.join(missing_levels)}"
            )

        # Validate draft order bonuses structure
        required_bonus_types = [self.keys.BONUS_PRIMARY, self.keys.BONUS_SECONDARY]
        missing_bonus_types = [
            bonus_type for bonus_type in required_bonus_types
            if bonus_type not in self.draft_order_bonuses
        ]
        if missing_bonus_types:
            raise ValueError(
                f"DRAFT_ORDER_BONUSES missing types: {', '.join(missing_bonus_types)}"
            )

        # Validate draft order is a list
        if not isinstance(self.draft_order, list):
            raise ValueError("DRAFT_ORDER must be a list")

        # Pre-calculate parameterized thresholds if needed (backward compatible)
        # Skip CONSISTENCY_SCORING as it's deprecated
        for scoring_type in [self.keys.ADP_SCORING, self.keys.PLAYER_RATING_SCORING,
                             self.keys.TEAM_QUALITY_SCORING, self.keys.PERFORMANCE_SCORING,
                             self.keys.MATCHUP_SCORING]:
            scoring_dict = self.parameters[scoring_type]
            thresholds_config = scoring_dict[self.keys.THRESHOLDS]

            # Check if parameterized (new format with BASE_POSITION, DIRECTION, STEPS)
            if self.keys.BASE_POSITION in thresholds_config:
                # Calculate thresholds from parameters
                calculated = self.calculate_thresholds(
                    thresholds_config[self.keys.BASE_POSITION],
                    thresholds_config[self.keys.DIRECTION],
                    thresholds_config[self.keys.STEPS],
                    scoring_type
                )

                # Add calculated values to thresholds dict for direct access
                # This maintains backward compatibility - existing code can continue
                # to access thresholds_config[VERY_POOR], etc.
                thresholds_config[self.keys.VERY_POOR] = calculated[self.keys.VERY_POOR]
                thresholds_config[self.keys.POOR] = calculated[self.keys.POOR]
                thresholds_config[self.keys.GOOD] = calculated[self.keys.GOOD]
                thresholds_config[self.keys.EXCELLENT] = calculated[self.keys.EXCELLENT]

                self.logger.debug(f"{scoring_type} thresholds calculated: E={calculated[self.keys.EXCELLENT]}, "
                                 f"G={calculated[self.keys.GOOD]}, P={calculated[self.keys.POOR]}, "
                                 f"VP={calculated[self.keys.VERY_POOR]}")

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """
        Get a parameter value by key.

        Args:
            key: The parameter key
            default: Default value if key not found

        Returns:
            The parameter value or default
        """
        return self.parameters.get(key, default)

    def has_parameter(self, key: str) -> bool:
        """
        Check if a parameter exists.

        Args:
            key: The parameter key

        Returns:
            True if parameter exists, False otherwise
        """
        return key in self.parameters
    
    def get_consistency_label(self, val: float) -> str:
        """
        Get a human-readable label for a consistency value.

        Consistency is measured using Coefficient of Variation (CV) where
        lower values indicate more consistent performance.

        Args:
            val (float): Coefficient of Variation (CV) value

        Returns:
            str: Label describing consistency level (EXCELLENT, GOOD, NEUTRAL, POOR, VERY_POOR)

        Example:
            >>> config.get_consistency_label(0.15)  # Very consistent
            'EXCELLENT'
            >>> config.get_consistency_label(0.9)   # Very inconsistent
            'VERY_POOR'
        """
        if val <= self.consistency_scoring[self.keys.THRESHOLDS][self.keys.EXCELLENT]:
            return self.keys.EXCELLENT
        elif val <= self.consistency_scoring[self.keys.THRESHOLDS][self.keys.GOOD]:
            return self.keys.GOOD
        elif val >= self.consistency_scoring[self.keys.THRESHOLDS][self.keys.POOR]:
            return self.keys.POOR
        elif val >= self.consistency_scoring[self.keys.THRESHOLDS][self.keys.VERY_POOR]:
            return self.keys.VERY_POOR
        else:
            return "NEUTRAL"

    
    def _get_multiplier(self, scoring_dict : Dict[str, Any], val, rising_thresholds=True) -> Tuple[float, str]:
        """
        Get multiplier based on threshold logic.

        Args:
            scoring_dict: Dictionary with THRESHOLDS and MULTIPLIERS
            val: Value to evaluate
            rising_thresholds: True if higher values are better (e.g., player rating)
                              False if lower values are better (e.g., ADP, team rank)

        Returns:
            float: Multiplier value

        Logic:
            rising_thresholds=True (higher is better):
                - val >= EXCELLENT threshold → EXCELLENT multiplier
                - val >= GOOD threshold → GOOD multiplier
                - GOOD > val > POOR → neutral (1.0)
                - val <= POOR threshold → POOR multiplier
                - val <= VERY_POOR threshold → VERY_POOR multiplier

            rising_thresholds=False (lower is better):
                - val <= EXCELLENT threshold → EXCELLENT multiplier
                - val <= GOOD threshold → GOOD multiplier
                - GOOD < val < POOR → neutral (1.0)
                - val >= POOR threshold → POOR multiplier
                - val >= VERY_POOR threshold → VERY_POOR multiplier
        """
        # Handle None values - return neutral multiplier (1.0) when data is unavailable
        if val == None:
            self.logger.debug(f"Multiplier calculation received None value, returning NEUTRAL (1.0)")
            multiplier, label = 1.0, self.keys.NEUTRAL

        elif rising_thresholds:
            # Higher values are better (e.g., player rating where 80+ is excellent)
            # Check from best to worst
            if val >= scoring_dict[self.keys.THRESHOLDS][self.keys.EXCELLENT]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.EXCELLENT], self.keys.EXCELLENT
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.GOOD]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.GOOD], self.keys.GOOD
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.VERY_POOR]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.VERY_POOR], self.keys.VERY_POOR
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.POOR]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.POOR], self.keys.POOR
            else:
                multiplier, label = 1.0, self.keys.NEUTRAL
        else:
            # Lower values are better (e.g., ADP where 20 or less is excellent)
            # Check from best to worst
            if val <= scoring_dict[self.keys.THRESHOLDS][self.keys.EXCELLENT]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.EXCELLENT], self.keys.EXCELLENT
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.GOOD]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.GOOD], self.keys.GOOD
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.VERY_POOR]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.VERY_POOR], self.keys.VERY_POOR
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.POOR]:
                multiplier, label = scoring_dict[self.keys.MULTIPLIERS][self.keys.POOR], self.keys.POOR
            else:
                multiplier, label = 1.0, self.keys.NEUTRAL
            
        multiplier = multiplier ** scoring_dict[self.keys.WEIGHT]
        return multiplier, label

    def get_adp_multiplier(self, adp_val) -> Tuple[float, str]:
        return self._get_multiplier(self.adp_scoring, adp_val, rising_thresholds=False)
    
    def get_player_rating_multiplier(self, rating) -> Tuple[float, str]:
        return self._get_multiplier(self.player_rating_scoring, rating)
    
    def get_team_quality_multiplier(self, quality_rank : int) -> Tuple[float, str]:
        return self._get_multiplier(self.team_quality_scoring, quality_rank, rising_thresholds=False)
    
    def get_matchup_multiplier(self, value) -> Tuple[float, str]:
        return self._get_multiplier(self.matchup_scoring, value)

    def get_performance_multiplier(self, deviation: float) -> Tuple[float, str]:
        return self._get_multiplier(self.performance_scoring, deviation)

    def get_draft_order_bonus(self, position : str, draft_round : int) -> Tuple[float, str]:
        position_with_flex = Constants.get_position_with_flex(position)
        ideal_positions = self.draft_order[draft_round]
        if position_with_flex in ideal_positions:
            if ideal_positions.get(position_with_flex) == self.keys.DRAFT_ORDER_PRIMARY_LABEL:
                return self.draft_order_bonuses[self.keys.BONUS_PRIMARY], self.keys.BONUS_PRIMARY
            else:
                return self.draft_order_bonuses[self.keys.BONUS_SECONDARY], self.keys.BONUS_SECONDARY
        else:
            return 0, ""
        
    def get_bye_week_penalty(self, num_same_position : int, num_different_position : int = 0) -> float:
        """
        Calculate bye week penalty based on roster conflicts.

        Args:
            num_same_position: Number of same-position bye week conflicts
            num_different_position: Number of different-position bye week conflicts (default: 0)

        Returns:
            float: Total bye week penalty
        """
        same_position_penalty = self.base_bye_penalty * num_same_position
        different_position_penalty = self.parameters.get('DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY', 0) * num_different_position
        return same_position_penalty + different_position_penalty
        
    def get_injury_penalty(self, risk_level : str) -> float:
        if risk_level in self.injury_penalties:
            return self.injury_penalties[risk_level]
        else:
            return self.injury_penalties[self.keys.INJURY_HIGH]

    def get_draft_position_for_round(self, round_number: int) -> Dict[str, str]:
        """
        Get the draft order entry for a specific round.

        Args:
            round_number: The draft round (1-indexed)

        Returns:
            Dictionary mapping positions to priority ('P' or 'S')

        Raises:
            IndexError: If round_number is out of range
        """
        if round_number < 1 or round_number > len(self.draft_order):
            raise IndexError(
                f"Round number {round_number} out of range (1-{len(self.draft_order)})"
            )

        return self.draft_order[round_number - 1]
    
    def get_ideal_draft_position(self, round_num: int) -> str:
        """Get the ideal position to draft in a given round (returns PRIMARY='P' position)"""
        if round_num < len(self.draft_order):
            # IMPORTANT: Use min() not max() because 'P' (PRIMARY) < 'S' (SECONDARY) in string comparison
            best_position = min(self.draft_order[round_num], key=self.draft_order[round_num].get)
            return best_position
        return 'FLEX'

    def __repr__(self) -> str:
        """String representation of the config manager."""
        return (
            f"ConfigManager("
            f"week={self.current_nfl_week}, "
            f"season={self.nfl_season}, "
            f"format='{self.nfl_scoring_format}')"
        )
