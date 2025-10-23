#!/usr/bin/env python3
"""
Tests for league_helper/constants.py

Tests all constants, position definitions, roster limits, and helper functions
to ensure correct configuration for the Fantasy Football League Helper.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from league_helper import constants


class TestLoggingConstants:
    """Test suite for logging configuration constants."""

    def test_logging_level_is_valid(self):
        """Test that LOGGING_LEVEL is a valid log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        assert constants.LOGGING_LEVEL in valid_levels

    def test_logging_to_file_is_boolean(self):
        """Test that LOGGING_TO_FILE is a boolean."""
        assert isinstance(constants.LOGGING_TO_FILE, bool)

    def test_log_name_is_non_empty(self):
        """Test that LOG_NAME is a non-empty string."""
        assert isinstance(constants.LOG_NAME, str)
        assert len(constants.LOG_NAME) > 0

    def test_logging_file_is_valid_path(self):
        """Test that LOGGING_FILE is a valid file path string."""
        assert isinstance(constants.LOGGING_FILE, str)
        assert len(constants.LOGGING_FILE) > 0

    def test_logging_format_is_valid(self):
        """Test that LOGGING_FORMAT is a valid format type."""
        valid_formats = ['detailed', 'standard', 'simple']
        assert constants.LOGGING_FORMAT in valid_formats


class TestGeneralSettings:
    """Test suite for general application settings."""

    def test_recommendation_count_is_positive(self):
        """Test that RECOMMENDATION_COUNT is a positive integer."""
        assert isinstance(constants.RECOMMENDATION_COUNT, int)
        assert constants.RECOMMENDATION_COUNT > 0

    def test_fantasy_team_name_exists(self):
        """Test that FANTASY_TEAM_NAME is defined."""
        assert hasattr(constants, 'FANTASY_TEAM_NAME')
        assert isinstance(constants.FANTASY_TEAM_NAME, str)
        assert len(constants.FANTASY_TEAM_NAME) > 0


class TestWaiverOptimizerConstants:
    """Test suite for waiver optimizer configuration."""

    def test_min_trade_improvement_is_non_negative(self):
        """Test that MIN_TRADE_IMPROVEMENT is non-negative."""
        assert isinstance(constants.MIN_TRADE_IMPROVEMENT, int)
        assert constants.MIN_TRADE_IMPROVEMENT >= 0

    def test_num_trade_runners_up_is_positive(self):
        """Test that NUM_TRADE_RUNNERS_UP is positive."""
        assert isinstance(constants.NUM_TRADE_RUNNERS_UP, int)
        assert constants.NUM_TRADE_RUNNERS_UP > 0


class TestPositionConstants:
    """Test suite for position constant definitions."""

    def test_position_constants_are_strings(self):
        """Test that all position constants are non-empty strings."""
        positions = [constants.RB, constants.WR, constants.QB,
                    constants.TE, constants.K, constants.DST, constants.FLEX]

        for pos in positions:
            assert isinstance(pos, str)
            assert len(pos) > 0

    def test_all_positions_contains_core_positions(self):
        """Test that ALL_POSITIONS contains all core positions except FLEX."""
        assert constants.QB in constants.ALL_POSITIONS
        assert constants.RB in constants.ALL_POSITIONS
        assert constants.WR in constants.ALL_POSITIONS
        assert constants.TE in constants.ALL_POSITIONS
        assert constants.K in constants.ALL_POSITIONS
        assert constants.DST in constants.ALL_POSITIONS

    def test_all_positions_does_not_contain_flex(self):
        """Test that ALL_POSITIONS does not contain FLEX."""
        assert constants.FLEX not in constants.ALL_POSITIONS

    def test_offense_positions_are_offensive(self):
        """Test that OFFENSE_POSITIONS contains only offensive positions."""
        expected_offense = ["QB", "RB", "WR", "TE", "K"]
        assert constants.OFFENSE_POSITIONS == expected_offense

    def test_defense_positions_are_defensive(self):
        """Test that DEFENSE_POSITIONS contains defensive position variations."""
        assert "DEF" in constants.DEFENSE_POSITIONS
        assert "DST" in constants.DEFENSE_POSITIONS
        assert "D/ST" in constants.DEFENSE_POSITIONS


class TestRosterConstruction:
    """Test suite for roster construction limits."""

    def test_flex_eligible_positions_are_correct(self):
        """Test that FLEX_ELIGIBLE_POSITIONS contains RB, WR, DST."""
        assert constants.RB in constants.FLEX_ELIGIBLE_POSITIONS
        assert constants.WR in constants.FLEX_ELIGIBLE_POSITIONS
        assert constants.DST in constants.FLEX_ELIGIBLE_POSITIONS

    def test_flex_eligible_does_not_contain_flex_itself(self):
        """Test that FLEX_ELIGIBLE_POSITIONS doesn't contain FLEX (circular reference)."""
        assert constants.FLEX not in constants.FLEX_ELIGIBLE_POSITIONS

    def test_flex_eligible_contains_only_valid_positions(self):
        """Test that all positions in FLEX_ELIGIBLE_POSITIONS are valid positions."""
        for pos in constants.FLEX_ELIGIBLE_POSITIONS:
            assert pos in constants.ALL_POSITIONS or pos == constants.DST


class TestByeWeeks:
    """Test suite for bye week configuration."""

    def test_possible_bye_weeks_are_valid_nfl_weeks(self):
        """Test that all bye weeks are valid NFL week numbers."""
        for week in constants.POSSIBLE_BYE_WEEKS:
            assert isinstance(week, int)
            assert 1 <= week <= 18  # NFL season is 18 weeks

    def test_possible_bye_weeks_are_sorted(self):
        """Test that POSSIBLE_BYE_WEEKS is sorted."""
        assert constants.POSSIBLE_BYE_WEEKS == sorted(constants.POSSIBLE_BYE_WEEKS)

    def test_possible_bye_weeks_has_no_duplicates(self):
        """Test that POSSIBLE_BYE_WEEKS has no duplicate weeks."""
        assert len(constants.POSSIBLE_BYE_WEEKS) == len(set(constants.POSSIBLE_BYE_WEEKS))


class TestScoringConfiguration:
    """Test suite for scoring configuration constants."""

    def test_matchup_enabled_positions_are_offensive(self):
        """Test that matchup multipliers apply only to offensive skill positions."""
        # K and DST should NOT have matchup multipliers
        assert constants.QB in constants.MATCHUP_ENABLED_POSITIONS
        assert constants.RB in constants.MATCHUP_ENABLED_POSITIONS
        assert constants.WR in constants.MATCHUP_ENABLED_POSITIONS
        assert constants.TE in constants.MATCHUP_ENABLED_POSITIONS

    def test_matchup_enabled_excludes_kicker_and_defense(self):
        """Test that kickers and defense don't use matchup scoring."""
        assert constants.K not in constants.MATCHUP_ENABLED_POSITIONS
        assert constants.DST not in constants.MATCHUP_ENABLED_POSITIONS


class TestGetPositionWithFlexFunction:
    """Test suite for get_position_with_flex() helper function."""

    def test_running_back_returns_flex(self):
        """Test that RB position returns FLEX."""
        result = constants.get_position_with_flex('RB')
        assert result == constants.FLEX

    def test_wide_receiver_returns_flex(self):
        """Test that WR position returns FLEX."""
        result = constants.get_position_with_flex('WR')
        assert result == constants.FLEX

    def test_defense_returns_flex(self):
        """Test that DST position returns FLEX."""
        result = constants.get_position_with_flex('DST')
        assert result == constants.FLEX

    def test_quarterback_returns_qb(self):
        """Test that QB position returns QB (not FLEX)."""
        result = constants.get_position_with_flex('QB')
        assert result == 'QB'

    def test_tight_end_returns_correct_value(self):
        """Test that TE position returns FLEX if flex-eligible, otherwise TE."""
        result = constants.get_position_with_flex('TE')
        if constants.TE in constants.FLEX_ELIGIBLE_POSITIONS:
            assert result == constants.FLEX
        else:
            assert result == 'TE'

    def test_kicker_returns_k(self):
        """Test that K position returns K (not FLEX)."""
        result = constants.get_position_with_flex('K')
        assert result == 'K'

    def test_flex_returns_flex(self):
        """Test that FLEX position returns FLEX."""
        result = constants.get_position_with_flex('FLEX')
        assert result == constants.FLEX

    def test_all_flex_eligible_positions_return_flex(self):
        """Test that all FLEX-eligible positions return FLEX."""
        for position in constants.FLEX_ELIGIBLE_POSITIONS:
            result = constants.get_position_with_flex(position)
            assert result == constants.FLEX
