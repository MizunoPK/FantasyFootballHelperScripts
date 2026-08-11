"""
Unit Tests for the Live ADP Threshold Ladder

Pins the five-tier ADP ladder produced from the LIVE config store
(`data/configs/league_config.json`) rather than from a temp-dir fixture, so that
flipping `parameters.ADP_SCORING.THRESHOLDS.DIRECTION` back to `INCREASING` in
the live file makes these tests fail (the mutation check, TD5/UD3).

Also pins the neighbouring `PLAYER_RATING_SCORING` block, which is `INCREASING`
*correctly* — `get_player_rating_multiplier` resolves to `rising_thresholds=True`
via the default in `ConfigManager._get_multiplier`'s signature — so a symmetric
"fix both `INCREASING` blocks" edit would invert that factor (TD2/UD2).

Author: Claude Code
Date: 2026-08-10
"""

from pathlib import Path

import pytest

from league_helper.util.ConfigManager import ConfigManager


# FIXTURES

@pytest.fixture
def live_config():
    """ConfigManager over the LIVE data store — deliberately not a temp fixture."""
    return ConfigManager(Path("data"))


class TestAdpLadderReachability:
    """All five ADP tiers are reachable under the live config (TD5, UD7)."""

    def test_all_five_adp_tiers_reachable(self, live_config):
        """Each tier is probed half a step inside its band, derived from the live STEPS."""
        # Arrange
        steps = live_config.adp_scoring["THRESHOLDS"]["STEPS"]
        expected = [
            (0.5, "EXCELLENT"),
            (1.5, "GOOD"),
            (2.5, "NEUTRAL"),
            (3.5, "POOR"),
            (4.5, "VERY_POOR"),
        ]

        # Act
        observed = [
            (multiple, live_config.get_adp_multiplier(multiple * steps)[1])
            for multiple, _ in expected
        ]

        # Assert
        assert observed == expected

    def test_adp_direction_is_decreasing(self, live_config):
        """The live ADP ladder is built descending, pairing with rising_thresholds=False."""
        # Arrange / Act
        direction = live_config.adp_scoring["THRESHOLDS"]["DIRECTION"]

        # Assert
        assert direction == "DECREASING"


class TestPlayerRatingLadderUnchanged:
    """`PLAYER_RATING_SCORING` stays ascending and still discriminates (TD2, UD2)."""

    def test_player_rating_direction_is_increasing(self, live_config):
        """The neighbouring INCREASING block is correct and must not be flipped."""
        # Arrange / Act
        direction = live_config.player_rating_scoring["THRESHOLDS"]["DIRECTION"]

        # Assert
        assert direction == "INCREASING"

    def test_player_rating_ascending_pairing_discriminates(self, live_config):
        """Three distinct labels prove the assertion above is not a tautology."""
        # Arrange
        steps = live_config.player_rating_scoring["THRESHOLDS"]["STEPS"]
        expected = [
            (0.5, "VERY_POOR"),
            (2.5, "NEUTRAL"),
            (4.5, "EXCELLENT"),
        ]

        # Act
        observed = [
            (multiple, live_config.get_player_rating_multiplier(multiple * steps)[1])
            for multiple, _ in expected
        ]

        # Assert
        assert observed == expected
