"""
Configuration manager for all league settings.

Manages all NFL settings, scoring parameters, and mode-specific configurations.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger


class ConfigManager:
    """Manages all configuration settings from a single league_config.json file."""

    def __init__(self, data_folder: Path):
        """
        Initialize the config manager and load configuration.

        Args:
            project_root: Root directory of the project
        """
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
        """Load and validate configuration from JSON file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            data = json.load(f)

        # Validate required fields
        self._validate_config_structure(data)

        # Store configuration data
        self.config_name = data.get("config_name", "")
        self.description = data.get("description", "")
        self.parameters = data.get("parameters", {})

        self.logger.debug(f"Loaded config file: {self.config_path}")
        self.logger.info(f"Loaded config_name: {self.config_name}")
        self.logger.debug(f"Loaded description: {self.description}")
        self.logger.info(f"Loaded parameters: {self.parameters}")

        # Extract and validate all parameters
        self._extract_parameters()

    def _validate_config_structure(self, data: Dict[str, Any]) -> None:
        """
        Validate that the configuration has the required structure.

        Args:
            data: The loaded JSON data

        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ["config_name", "description", "parameters"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise ValueError(
                f"Configuration missing required fields: {', '.join(missing_fields)}"
            )

        if not isinstance(data["parameters"], dict):
            raise ValueError("'parameters' field must be a dictionary")

    def _extract_parameters(self) -> None:
        """Extract and validate all parameters from the config."""
        # Required parameters
        required_params = [
            "CURRENT_NFL_WEEK",
            "NFL_SEASON",
            "NFL_SCORING_FORMAT",
            "NORMALIZATION_MAX_SCALE",
            "BASE_BYE_PENALTY",
            "INJURY_PENALTIES",
            "ADP_SCORING",
            "PLAYER_RATING_SCORING",
            "TEAM_QUALITY_SCORING",
            "CONSISTENCY_SCORING",
            "MATCHUP_SCORING",
            "DRAFT_ORDER_BONUSES",
            "DRAFT_ORDER",
        ]

        missing_params = [p for p in required_params if p not in self.parameters]
        if missing_params:
            raise ValueError(
                f"Config missing required parameters: {', '.join(missing_params)}"
            )

        # Extract league-wide parameters
        self.current_nfl_week = self.parameters["CURRENT_NFL_WEEK"]
        self.nfl_season = self.parameters["NFL_SEASON"]
        self.nfl_scoring_format = self.parameters["NFL_SCORING_FORMAT"]
        self.normalization_max_scale = self.parameters["NORMALIZATION_MAX_SCALE"]
        self.base_bye_penalty = self.parameters["BASE_BYE_PENALTY"]
        self.injury_penalties = self.parameters["INJURY_PENALTIES"]
        self.adp_scoring = self.parameters["ADP_SCORING"]
        self.player_rating_scoring = self.parameters["PLAYER_RATING_SCORING"]
        self.team_quality_scoring = self.parameters["TEAM_QUALITY_SCORING"]
        self.consistency_scoring = self.parameters["CONSISTENCY_SCORING"]
        self.matchup_scoring = self.parameters["MATCHUP_SCORING"]

        # Extract Add to Roster mode parameters
        self.draft_order_bonuses = self.parameters["DRAFT_ORDER_BONUSES"]
        self.draft_order = self.parameters["DRAFT_ORDER"]

        # Extract Starter Helper mode parameters (optional - not in current config)
        # Note: matchup_multipliers are accessed directly from matchup_scoring["MULTIPLIERS"]

        # Validate injury penalties structure
        required_injury_levels = ["LOW", "MEDIUM", "HIGH"]
        missing_levels = [
            level for level in required_injury_levels
            if level not in self.injury_penalties
        ]
        if missing_levels:
            raise ValueError(
                f"INJURY_PENALTIES missing levels: {', '.join(missing_levels)}"
            )

        # Validate draft order bonuses structure
        required_bonus_types = ["PRIMARY", "SECONDARY"]
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

    def get_matchup_multiplier(self, matchup_level: str) -> float:
        """
        Get the multiplier for a specific matchup level.

        Args:
            matchup_level: The matchup quality level

        Returns:
            The multiplier value

        Raises:
            KeyError: If matchup level is not found
        """
        if "MULTIPLIERS" not in self.matchup_scoring:
            raise KeyError("MATCHUP_SCORING missing MULTIPLIERS")

        multipliers = self.matchup_scoring["MULTIPLIERS"]
        if matchup_level not in multipliers:
            raise KeyError(f"Unknown matchup level: {matchup_level}")

        return multipliers[matchup_level]

    def __repr__(self) -> str:
        """String representation of the config manager."""
        return (
            f"ConfigManager("
            f"week={self.current_nfl_week}, "
            f"season={self.nfl_season}, "
            f"format='{self.nfl_scoring_format}')"
        )
