"""
Configuration manager for league-wide settings.

Manages general NFL settings and scoring parameters shared across all modes.
"""

from pathlib import Path
from typing import Dict, Any

from league_helper.util.ConfigManager import ConfigManager


class LeagueConfigManager(ConfigManager):
    """Manages league-wide configuration settings."""

    def __init__(self, config_folder):
        """Initialize the league config manager."""
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

        config_path = config_folder / 'league_config.json'

        super().__init__(config_path)

    def _post_load_validation(self) -> None:
        """Validate and extract league-specific parameters."""
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
            "CONSISTENCY_SCORING"
        ]

        missing_params = [p for p in required_params if p not in self.parameters]
        if missing_params:
            raise ValueError(
                f"League config missing required parameters: {', '.join(missing_params)}"
            )

        # Extract and store parameters
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

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"LeagueConfigManager("
            f"week={self.current_nfl_week}, "
            f"season={self.nfl_season}, "
            f"format='{self.nfl_scoring_format}')"
        )
