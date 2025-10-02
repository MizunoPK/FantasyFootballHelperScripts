"""
Unit tests for starter_helper configuration validation.

Tests the new matchup multiplier configuration and validation system
added as part of the scoring overhaul.
"""

import sys
from pathlib import Path
import pytest

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared_files.configs.starter_helper_config import (
    MATCHUP_MULTIPLIERS,
    MATCHUP_ENABLED_POSITIONS,
    STARTER_HELPER_ACTIVE_STATUSES,
    QB, RB, WR, TE, K, DST,
    validate_config
)


class TestMatchupMultiplierConfiguration:
    """Tests for matchup multiplier configuration settings"""

    def test_matchup_multipliers_exist(self):
        """Test that MATCHUP_MULTIPLIERS is defined and not empty"""
        assert MATCHUP_MULTIPLIERS is not None
        assert len(MATCHUP_MULTIPLIERS) > 0

    def test_matchup_multipliers_structure(self):
        """Test that matchup multipliers have correct structure"""
        for key, value in MATCHUP_MULTIPLIERS.items():
            # Each key should be a tuple of (lower, upper) bounds
            assert isinstance(key, tuple)
            assert len(key) == 2
            lower, upper = key

            # Check that bounds are numeric or infinity
            assert isinstance(lower, (int, float))
            assert isinstance(upper, (int, float))

            # Check that multiplier value is numeric
            assert isinstance(value, (int, float))

    def test_matchup_multipliers_ranges(self):
        """Test that multiplier ranges are reasonable (0.5 to 2.0)"""
        for (lower, upper), multiplier in MATCHUP_MULTIPLIERS.items():
            assert 0.5 <= multiplier <= 2.0, f"Multiplier {multiplier} out of range"

    def test_matchup_multipliers_coverage(self):
        """Test that matchup multipliers cover expected scenarios"""
        # Should have 5 ranges: excellent, good, neutral, poor, very poor
        assert len(MATCHUP_MULTIPLIERS) == 5

        # Get all multiplier values
        multipliers = sorted(MATCHUP_MULTIPLIERS.values())

        # Should have decreasing multipliers for worse matchups
        assert multipliers[0] < 1.0  # Very poor
        assert multipliers[1] < 1.0  # Poor
        assert multipliers[2] == 1.0  # Neutral
        assert multipliers[3] > 1.0  # Good
        assert multipliers[4] > 1.0  # Excellent

    def test_matchup_enabled_positions(self):
        """Test that MATCHUP_ENABLED_POSITIONS contains correct positions"""
        assert MATCHUP_ENABLED_POSITIONS is not None
        assert len(MATCHUP_ENABLED_POSITIONS) > 0

        # Should only contain QB, RB, WR, TE (not K or DST)
        expected_positions = [QB, RB, WR, TE]
        assert set(MATCHUP_ENABLED_POSITIONS) == set(expected_positions)

    def test_matchup_enabled_positions_excludes_kicker_dst(self):
        """Test that K and DST are excluded from matchup adjustments"""
        assert K not in MATCHUP_ENABLED_POSITIONS
        assert DST not in MATCHUP_ENABLED_POSITIONS


class TestBinaryInjuryStatusConfiguration:
    """Tests for binary injury status configuration"""

    def test_active_statuses_exist(self):
        """Test that STARTER_HELPER_ACTIVE_STATUSES is defined"""
        assert STARTER_HELPER_ACTIVE_STATUSES is not None
        assert len(STARTER_HELPER_ACTIVE_STATUSES) > 0

    def test_active_statuses_content(self):
        """Test that active statuses contain ACTIVE and QUESTIONABLE"""
        assert 'ACTIVE' in STARTER_HELPER_ACTIVE_STATUSES
        assert 'QUESTIONABLE' in STARTER_HELPER_ACTIVE_STATUSES

    def test_active_statuses_are_strings(self):
        """Test that all active statuses are strings"""
        for status in STARTER_HELPER_ACTIVE_STATUSES:
            assert isinstance(status, str)

    def test_active_statuses_uppercase(self):
        """Test that all active statuses are uppercase"""
        for status in STARTER_HELPER_ACTIVE_STATUSES:
            assert status == status.upper()


class TestConfigValidation:
    """Tests for configuration validation function"""

    def test_validate_config_runs_without_error(self):
        """Test that validate_config runs without raising exceptions"""
        # Should not raise any exceptions with default config
        try:
            validate_config()
        except Exception as e:
            pytest.fail(f"validate_config() raised {type(e).__name__}: {e}")

    def test_validate_config_with_valid_settings(self):
        """Test validation with all valid settings"""
        # Validate should pass with current configuration
        validate_config()

    def test_invalid_matchup_multiplier_range(self):
        """Test that multiplier values are within valid range"""
        # All multipliers should be between 0.5 and 2.0
        for (lower, upper), multiplier in MATCHUP_MULTIPLIERS.items():
            assert 0.5 <= multiplier <= 2.0, f"Multiplier {multiplier} out of valid range [0.5, 2.0]"

    def test_matchup_enabled_positions_not_empty(self):
        """Test that MATCHUP_ENABLED_POSITIONS is not empty"""
        assert len(MATCHUP_ENABLED_POSITIONS) > 0, "MATCHUP_ENABLED_POSITIONS should not be empty"

    def test_active_statuses_not_empty(self):
        """Test that STARTER_HELPER_ACTIVE_STATUSES is not empty"""
        assert len(STARTER_HELPER_ACTIVE_STATUSES) > 0, "STARTER_HELPER_ACTIVE_STATUSES should not be empty"


class TestMatchupMultiplierRanges:
    """Tests for specific matchup multiplier range calculations"""

    def test_excellent_matchup_multiplier(self):
        """Test excellent matchup multiplier (rank difference >= 15)"""
        excellent_multiplier = MATCHUP_MULTIPLIERS[(15, float('inf'))]
        assert excellent_multiplier == 1.2

    def test_good_matchup_multiplier(self):
        """Test good matchup multiplier (rank difference 6-14)"""
        good_multiplier = MATCHUP_MULTIPLIERS[(6, 15)]
        assert good_multiplier == 1.1

    def test_neutral_matchup_multiplier(self):
        """Test neutral matchup multiplier (rank difference -5 to 5)"""
        neutral_multiplier = MATCHUP_MULTIPLIERS[(-5, 6)]
        assert neutral_multiplier == 1.0

    def test_poor_matchup_multiplier(self):
        """Test poor matchup multiplier (rank difference -14 to -6)"""
        poor_multiplier = MATCHUP_MULTIPLIERS[(-15, -5)]
        assert poor_multiplier == 0.9

    def test_very_poor_matchup_multiplier(self):
        """Test very poor matchup multiplier (rank difference <= -15)"""
        very_poor_multiplier = MATCHUP_MULTIPLIERS[(float('-inf'), -14)]
        assert very_poor_multiplier == 0.8


class TestConfigurationIntegration:
    """Integration tests for configuration system"""

    def test_all_positions_defined(self):
        """Test that all position constants are defined"""
        positions = [QB, RB, WR, TE, K, DST]
        for pos in positions:
            assert pos is not None
            assert isinstance(pos, str)

    def test_matchup_positions_subset_of_all_positions(self):
        """Test that matchup positions are a valid subset"""
        all_positions = {QB, RB, WR, TE, K, DST}
        matchup_positions = set(MATCHUP_ENABLED_POSITIONS)

        # All matchup positions should be valid positions
        assert matchup_positions.issubset(all_positions)

    def test_config_consistency(self):
        """Test overall configuration consistency"""
        # Matchup multipliers should cover all scenarios
        assert len(MATCHUP_MULTIPLIERS) >= 3  # At least good, neutral, poor

        # Active statuses should include standard statuses
        assert len(STARTER_HELPER_ACTIVE_STATUSES) >= 1

        # Matchup positions should be non-empty
        assert len(MATCHUP_ENABLED_POSITIONS) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])