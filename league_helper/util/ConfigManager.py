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
from typing import Any, Dict, List

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
    CONSISTENCY_SCORING = "CONSISTENCY_SCORING"
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

    def __init__(self, data_folder: Path):
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
        self.consistency_scoring: Dict[str, Any] = {}
        self.matchup_scoring: Dict[str, Any] = {}

        # Add to Roster mode settings
        self.draft_order_bonuses: Dict[str, float] = {}
        self.draft_order: List[Dict[str, str]] = []

        self._load_config()

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

        self.logger.info(f"Loaded configuration: '{self.config_name}'")
        self.logger.debug(f"Description: {self.description}")
        self.logger.debug(f"Parameters count: {len(self.parameters)}")

        # Extract and validate all parameters
        self._extract_parameters()
        self.logger.info("Configuration loaded and validated successfully")

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
            self.keys.CONSISTENCY_SCORING,
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
        self.consistency_scoring = self.parameters[self.keys.CONSISTENCY_SCORING]
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
    
    def get_consistency_label(self, val):
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

    
    def _get_multiplier(self, scoring_dict : Dict[str, Any], val, rising_thresholds=True):
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
        if val is None:
            return 1.0

        if rising_thresholds:
            # Higher values are better (e.g., player rating where 80+ is excellent)
            # Check from best to worst
            if val >= scoring_dict[self.keys.THRESHOLDS][self.keys.EXCELLENT]:
                return scoring_dict[self.keys.MULTIPLIERS][self.keys.EXCELLENT]
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.GOOD]:
                return scoring_dict[self.keys.MULTIPLIERS][self.keys.GOOD]
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.VERY_POOR]:
                return scoring_dict[self.keys.MULTIPLIERS][self.keys.VERY_POOR]
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.POOR]:
                return scoring_dict[self.keys.MULTIPLIERS][self.keys.POOR]
            else:
                return 1.0
        else:
            # Lower values are better (e.g., ADP where 20 or less is excellent)
            # Check from best to worst
            if val <= scoring_dict[self.keys.THRESHOLDS][self.keys.EXCELLENT]:
                return scoring_dict[self.keys.MULTIPLIERS][self.keys.EXCELLENT]
            elif val <= scoring_dict[self.keys.THRESHOLDS][self.keys.GOOD]:
                return scoring_dict[self.keys.MULTIPLIERS][self.keys.GOOD]
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.VERY_POOR]:
                return scoring_dict[self.keys.MULTIPLIERS][self.keys.VERY_POOR]
            elif val >= scoring_dict[self.keys.THRESHOLDS][self.keys.POOR]:
                return scoring_dict[self.keys.MULTIPLIERS][self.keys.POOR]
            else:
                return 1.0

    def get_adp_multiplier(self, adp_val):
        return self._get_multiplier(self.adp_scoring, adp_val, rising_thresholds=False)
    
    def get_player_rating_multiplier(self, rating):
        return self._get_multiplier(self.player_rating_scoring, rating)
    
    def get_team_quality_multiplier(self, quality_rank : int):
        return self._get_multiplier(self.team_quality_scoring, quality_rank, rising_thresholds=False)
    
    def get_consistency_multiplier(self, value):
        # BUG FIX: Consistency uses CV (coefficient of variation) where lower is better
        # So we need rising_thresholds=False (like ADP and team quality)
        # Special case: if value == 0.5 (insufficient data default), return neutral 1.0
        if value == 0.5:
            return 1.0
        return self._get_multiplier(self.consistency_scoring, value, rising_thresholds=False)
    
    def get_matchup_multiplier(self, value):
        return self._get_multiplier(self.matchup_scoring, value)
    
    def get_draft_order_bonus(self, position : str, draft_round : int):
        position_with_flex = Constants.get_position_with_flex(position)
        ideal_positions = self.draft_order[draft_round]
        if position_with_flex in ideal_positions:
            if ideal_positions.get(position_with_flex) == self.keys.DRAFT_ORDER_PRIMARY_LABEL:
                return self.draft_order_bonuses[self.keys.BONUS_PRIMARY]
            else:
                return self.draft_order_bonuses[self.keys.BONUS_SECONDARY]
        else:
            return 0
        
    def get_bye_week_penalty(self, num_matching_byes : int):
        return self.base_bye_penalty * num_matching_byes
        
    def get_injury_penalty(self, risk_level : str):
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
