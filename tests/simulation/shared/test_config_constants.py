"""
Unit Tests for Base Config Parameter Shape

Guards the live raw base config against week-file-derived parameter leakage (T86):
- data/configs/league_config.json carries exactly BASE_CONFIG_PARAMS
- and no WEEK_SPECIFIC_PARAMS key ever re-enters it

Author: Kai Mizuno
"""

# Standard library
import json
from pathlib import Path

# Local
from simulation.shared.config_constants import BASE_CONFIG_PARAMS, WEEK_SPECIFIC_PARAMS


# FIXTURES

_LIVE_BASE_CONFIG = Path("data/configs/league_config.json")


class TestLiveBaseConfigParameterShape:
    """Data-shape guard over the live data/configs/league_config.json (T86 D5)."""

    def test_raw_base_config_carries_exactly_the_base_params(self):
        """The raw base config's key set equals BASE_CONFIG_PARAMS and excludes every week-owned key."""
        # Arrange
        expected = set(BASE_CONFIG_PARAMS)
        week_owned = set(WEEK_SPECIFIC_PARAMS)

        # Act
        with open(_LIVE_BASE_CONFIG) as handle:
            live = set(json.load(handle)["parameters"].keys())

        # Assert
        assert live == expected, (
            f"{_LIVE_BASE_CONFIG} parameters drifted from BASE_CONFIG_PARAMS - "
            f"unexpected={sorted(live - expected)} missing={sorted(expected - live)}"
        )
        assert live & week_owned == set(), (
            f"week-file-owned parameters leaked into {_LIVE_BASE_CONFIG}: "
            f"{sorted(live & week_owned)}"
        )
