"""
Configuration manager for Waiver Optimizer mode.

Manages trade simulation settings and thresholds.
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from util.ConfigManager import ConfigManager


class WaiverOptimizerConfigManager(ConfigManager):
    """Manages Waiver Optimizer mode configuration settings."""

    def __init__(self, config_folder : Path):
        """Initialize the waiver optimizer config manager."""
        self.min_trade_improvement: float = 0.0
        self.num_trade_runners_up: int = 0

        config_path = config_folder / 'waiver_optimizer_mode_config.json'

        super().__init__(config_path)

    def _post_load_validation(self) -> None:
        """Validate and extract waiver optimizer specific parameters."""
        # Required parameters
        required_params = [
            "MIN_TRADE_IMPROVEMENT",
            "NUM_TRADE_RUNNERS_UP"
        ]

        missing_params = [p for p in required_params if p not in self.parameters]
        if missing_params:
            raise ValueError(
                f"Waiver Optimizer config missing required parameters: {', '.join(missing_params)}"
            )

        # Extract and store parameters
        self.min_trade_improvement = self.parameters["MIN_TRADE_IMPROVEMENT"]
        self.num_trade_runners_up = self.parameters["NUM_TRADE_RUNNERS_UP"]

        # Validate types and values
        if not isinstance(self.min_trade_improvement, (int, float)):
            raise ValueError("MIN_TRADE_IMPROVEMENT must be numeric")

        if not isinstance(self.num_trade_runners_up, int):
            raise ValueError("NUM_TRADE_RUNNERS_UP must be an integer")

        if self.num_trade_runners_up < 0:
            raise ValueError("NUM_TRADE_RUNNERS_UP must be non-negative")

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"WaiverOptimizerConfigManager("
            f"min_improvement={self.min_trade_improvement}, "
            f"runners_up={self.num_trade_runners_up})"
        )
