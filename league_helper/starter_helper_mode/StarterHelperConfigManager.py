"""
Configuration manager for Starter Helper mode.

Manages matchup multipliers for lineup optimization.
"""

from pathlib import Path
from typing import Dict
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from util.ConfigManager import ConfigManager


class StarterHelperConfigManager(ConfigManager):
    """Manages Starter Helper mode configuration settings."""

    def __init__(self, config_folder):
        """Initialize the starter helper config manager."""
        self.matchup_multipliers: Dict[str, float] = {}

        config_path = config_folder / 'starter_helper_mode_config.json'

        super().__init__(config_path)

    def _post_load_validation(self) -> None:
        """Validate and extract starter helper specific parameters."""
        # Required parameters
        required_params = ["MATCHUP_MULTIPLIERS"]

        missing_params = [p for p in required_params if p not in self.parameters]
        if missing_params:
            raise ValueError(
                f"Starter Helper config missing required parameters: {', '.join(missing_params)}"
            )

        # Extract and store parameters
        self.matchup_multipliers = self.parameters["MATCHUP_MULTIPLIERS"]

        # Validate matchup multipliers structure
        required_matchup_levels = ["VERY POOR", "POOR", "GOOD", "EXCELLENT"]
        missing_levels = [
            level for level in required_matchup_levels
            if level not in self.matchup_multipliers
        ]
        if missing_levels:
            raise ValueError(
                f"MATCHUP_MULTIPLIERS missing levels: {', '.join(missing_levels)}"
            )

        # Validate all multipliers are numeric
        for level, multiplier in self.matchup_multipliers.items():
            if not isinstance(multiplier, (int, float)):
                raise ValueError(
                    f"MATCHUP_MULTIPLIERS['{level}'] must be numeric, got {type(multiplier)}"
                )

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
        if matchup_level not in self.matchup_multipliers:
            raise KeyError(f"Unknown matchup level: {matchup_level}")

        return self.matchup_multipliers[matchup_level]

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"StarterHelperConfigManager("
            f"matchup_levels={len(self.matchup_multipliers)})"
        )
