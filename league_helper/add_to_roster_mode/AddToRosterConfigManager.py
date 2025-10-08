"""
Configuration manager for Add to Roster mode.

Manages draft order, bonuses, and recommendation settings.
"""

from pathlib import Path
from typing import Dict, Any, List

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from util.ConfigManager import ConfigManager


class AddToRosterConfigManager(ConfigManager):
    """Manages Add to Roster mode configuration settings."""

    def __init__(self, config_folder : Path):
        """Initialize the add to roster config manager."""
        self.draft_order_bonuses: Dict[str, float] = {}
        self.draft_order: List[Dict[str, str]] = []
        self.recommendation_count: int = 0

        config_path = config_folder / 'add_to_roster_mode_config.json'

        super().__init__(config_path)

    def _post_load_validation(self) -> None:
        """Validate and extract add to roster specific parameters."""
        # Required parameters
        required_params = [
            "DRAFT_ORDER_BONUSES",
            "DRAFT_ORDER",
            "RECOMMENDATION_COUNT"
        ]

        missing_params = [p for p in required_params if p not in self.parameters]
        if missing_params:
            raise ValueError(
                f"Add to Roster config missing required parameters: {', '.join(missing_params)}"
            )

        # Extract and store parameters
        self.draft_order_bonuses = self.parameters["DRAFT_ORDER_BONUSES"]
        self.draft_order = self.parameters["DRAFT_ORDER"]
        self.recommendation_count = self.parameters["RECOMMENDATION_COUNT"]

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

        # Validate recommendation count is positive
        if self.recommendation_count <= 0:
            raise ValueError("RECOMMENDATION_COUNT must be positive")

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

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"AddToRosterConfigManager("
            f"draft_rounds={len(self.draft_order)}, "
            f"recommendation_count={self.recommendation_count})"
        )
