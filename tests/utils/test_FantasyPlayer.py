"""
Tests for FantasyPlayer [LOCKED] indicator functionality.

Author: Kai Mizuno
"""

import pytest
from utils.FantasyPlayer import FantasyPlayer


class TestFantasyPlayerLockedIndicator:
    """Test suite for FantasyPlayer [LOCKED] indicator in __str__() method."""

    def test_str_shows_locked_indicator_when_locked_is_one(self):
        """Test that [LOCKED] appears at end of string when locked=1."""
        # Arrange
        player = FantasyPlayer(
            id=1,
            name="Test Player",
            team="KC",
            position="QB",
            bye_week=7,
            drafted=0,
            locked=1,  # Player is locked
            score=85.5,
            fantasy_points=250.0
        )

        # Act
        player_str = str(player)

        # Assert
        assert " [LOCKED]" in player_str, "Expected [LOCKED] indicator in player string"
        assert player_str.endswith("[LOCKED]"), "Expected [LOCKED] to be at the end of string"

    def test_str_no_locked_indicator_when_locked_is_zero(self):
        """Test that [LOCKED] does NOT appear when locked=0."""
        # Arrange
        player = FantasyPlayer(
            id=2,
            name="Available Player",
            team="KC",
            position="RB",
            bye_week=7,
            drafted=0,
            locked=0,  # Player is NOT locked
            score=75.0,
            fantasy_points=200.0
        )

        # Act
        player_str = str(player)

        # Assert
        assert " [LOCKED]" not in player_str, "Did not expect [LOCKED] indicator when locked=0"
        assert not player_str.endswith("[LOCKED]"), "[LOCKED] should not be at end when locked=0"

    def test_str_locked_indicator_with_drafted_status(self):
        """Test that [LOCKED] works correctly with different drafted statuses."""
        # Test with drafted=0 (AVAILABLE)
        player_available = FantasyPlayer(
            id=3,
            name="Available Locked",
            team="KC",
            position="WR",
            bye_week=7,
            drafted=0,
            locked=1,
            score=65.0,
            fantasy_points=180.0
        )
        assert "[AVAILABLE] [LOCKED]" in str(player_available)

        # Test with drafted=1 (DRAFTED)
        player_drafted = FantasyPlayer(
            id=4,
            name="Drafted Locked",
            team="KC",
            position="TE",
            bye_week=7,
            drafted=1,
            locked=1,
            score=55.0,
            fantasy_points=150.0
        )
        assert "[DRAFTED] [LOCKED]" in str(player_drafted)

        # Test with drafted=2 (ROSTERED)
        player_rostered = FantasyPlayer(
            id=5,
            name="Rostered Locked",
            team="KC",
            position="K",
            bye_week=7,
            drafted=2,
            locked=1,
            score=45.0,
            fantasy_points=120.0
        )
        assert "[ROSTERED] [LOCKED]" in str(player_rostered)

    def test_str_locked_indicator_format(self):
        """Test that the full format includes [LOCKED] in correct position."""
        # Arrange
        player = FantasyPlayer(
            id=6,
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            bye_week=10,
            drafted=2,
            locked=1,
            score=92.3,
            fantasy_points=310.5,
            injury_status="ACTIVE"
        )

        # Act
        player_str = str(player)

        # Assert
        # Expected format: "Name (Team Position) - Score pts [Bye=X] [STATUS] [LOCKED]"
        assert "Patrick Mahomes" in player_str
        assert "(KC QB)" in player_str
        assert "92.3 pts" in player_str
        assert "[Bye=10]" in player_str
        assert "[ROSTERED]" in player_str
        assert "[LOCKED]" in player_str
        # Ensure [LOCKED] comes after [ROSTERED]
        assert player_str.index("[ROSTERED]") < player_str.index("[LOCKED]")
