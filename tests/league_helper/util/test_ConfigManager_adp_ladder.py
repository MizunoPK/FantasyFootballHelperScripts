"""
Unit Tests for the Live ADP Threshold Ladder

Pins the five-tier ADP ladder produced from the LIVE config store
(`data/configs/league_config.json`) rather than from a temp-dir fixture, so that
flipping `parameters.ADP_SCORING.THRESHOLDS.DIRECTION` back to `INCREASING` in
the live file makes these tests fail (the mutation check, TD5/UD3).

NOTE (D10.3): the live ADP block now carries `SCALING: "LINEAR"`, so the ADP
factor emits only the FOUR anchor labels (EXCELLENT / GOOD / POOR / VERY_POOR)
for a valued input and never NEUTRAL (TD3 option C). The "five-tier" wording
above is retained verbatim because the sentence carrying it is the live-store
mutation check itself; read it as describing the BUCKETED ladder this file was
written against, not the label set the live LINEAR ADP factor now produces.

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
    """The live ADP ladder's label rule under TD3 option C (TD5, UD7)."""

    def test_adp_linear_tier_labels_follow_the_better_side_anchor(self, live_config):
        """Each probe sits half a step inside a band, derived from the live ladder.

        Both BASE_POSITION and STEPS are read, because `calculate_thresholds`
        computes every boundary as `base_pos + N * steps` — probing at
        `multiple * steps` alone would drift out of band the moment the
        hand-owned BASE_POSITION leaf moved (UD7).

        The live ADP block is `SCALING: "LINEAR"` (D10.3), so an interior probe
        takes the BETTER-side bracketing anchor's label (TD3 clause 3) and an
        out-of-window probe clamps to the nearest outer anchor (TD3 clause 2);
        NEUTRAL is unreachable for a valued ADP input.
        """
        # Arrange
        thresholds = live_config.adp_scoring["THRESHOLDS"]
        base, steps = thresholds["BASE_POSITION"], thresholds["STEPS"]
        expected = [
            (0.5, "EXCELLENT"),
            (1.5, "EXCELLENT"),
            (2.5, "GOOD"),
            (3.5, "POOR"),
            (4.5, "VERY_POOR"),
        ]

        # Act
        observed = [
            (multiple, live_config.get_adp_multiplier(base + multiple * steps)[1])
            for multiple, _ in expected
        ]

        # Assert
        assert observed == expected

    def test_adp_thresholds_are_base_plus_multiples_of_steps(self, live_config):
        """The computed boundaries themselves are pinned, not only the bands between them."""
        # Arrange
        thresholds = live_config.adp_scoring["THRESHOLDS"]
        base, steps = thresholds["BASE_POSITION"], thresholds["STEPS"]

        # Act
        observed = {
            tier: thresholds[tier]
            for tier in ("EXCELLENT", "GOOD", "POOR", "VERY_POOR")
        }

        # Assert
        assert observed == {
            "EXCELLENT": base + 1 * steps,
            "GOOD": base + 2 * steps,
            "POOR": base + 3 * steps,
            "VERY_POOR": base + 4 * steps,
        }

    def test_adp_tier_boundaries_are_closed_on_the_better_side(self, live_config):
        """An ADP landing exactly on a boundary takes that boundary's own tier.

        `_get_multiplier`'s rising_thresholds=False arm tests `val <= EXCELLENT`,
        `val <= GOOD`, `val >= VERY_POOR`, `val >= POOR` in that order, so every
        boundary is closed. The motivating regression includes a record at
        exactly the VERY_POOR boundary, so the equality case is pinned here
        rather than left to the half-step probes above.
        """
        # Arrange
        thresholds = live_config.adp_scoring["THRESHOLDS"]
        expected = [
            ("EXCELLENT", "EXCELLENT"),
            ("GOOD", "GOOD"),
            ("POOR", "POOR"),
            ("VERY_POOR", "VERY_POOR"),
        ]

        # Act
        observed = [
            (tier, live_config.get_adp_multiplier(thresholds[tier])[1])
            for tier, _ in expected
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
        thresholds = live_config.player_rating_scoring["THRESHOLDS"]
        base, steps = thresholds["BASE_POSITION"], thresholds["STEPS"]
        expected = [
            (0.5, "VERY_POOR"),
            (2.5, "NEUTRAL"),
            (4.5, "EXCELLENT"),
        ]

        # Act
        observed = [
            (multiple, live_config.get_player_rating_multiplier(base + multiple * steps)[1])
            for multiple, _ in expected
        ]

        # Assert
        assert observed == expected
