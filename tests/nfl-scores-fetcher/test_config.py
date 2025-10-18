"""
Unit Tests for NFL Scores Fetcher Configuration Module

Tests configuration constants and values.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "nfl-scores-fetcher"))

import config


# ============================================================================
# CONFIGURATION CONSTANTS TESTS
# ============================================================================

class TestConfigConstants:
    """Test configuration constant values"""

    def test_season_values_set(self):
        """Test that season and week values are set"""
        assert hasattr(config, 'NFL_SCORES_SEASON')
        assert hasattr(config, 'NFL_SCORES_CURRENT_WEEK')
        assert isinstance(config.NFL_SCORES_SEASON, int)
        assert isinstance(config.NFL_SCORES_CURRENT_WEEK, int)

    def test_season_type_set(self):
        """Test that season type is set"""
        assert hasattr(config, 'NFL_SCORES_SEASON_TYPE')
        assert isinstance(config.NFL_SCORES_SEASON_TYPE, int)
        # Season type should be 1 (preseason), 2 (regular), or 3 (postseason)
        assert config.NFL_SCORES_SEASON_TYPE in [1, 2, 3]

    def test_output_settings(self):
        """Test output configuration settings"""
        assert hasattr(config, 'OUTPUT_DIRECTORY')
        assert hasattr(config, 'CREATE_CSV')
        assert hasattr(config, 'CREATE_JSON')
        assert hasattr(config, 'CREATE_EXCEL')

        assert isinstance(config.CREATE_CSV, bool)
        assert isinstance(config.CREATE_JSON, bool)
        assert isinstance(config.CREATE_EXCEL, bool)

    def test_api_settings(self):
        """Test API configuration settings"""
        assert hasattr(config, 'REQUEST_TIMEOUT')
        assert hasattr(config, 'RATE_LIMIT_DELAY')

        assert isinstance(config.REQUEST_TIMEOUT, (int, float))
        assert isinstance(config.RATE_LIMIT_DELAY, (int, float))

        # Timeouts should be positive
        assert config.REQUEST_TIMEOUT > 0
        assert config.RATE_LIMIT_DELAY >= 0

    def test_logging_settings(self):
        """Test logging configuration settings"""
        assert hasattr(config, 'LOGGING_LEVEL')
        assert hasattr(config, 'LOGGING_TO_FILE')
        assert hasattr(config, 'LOG_NAME')
        assert hasattr(config, 'LOGGING_FILE')
        assert hasattr(config, 'LOGGING_FORMAT')

        assert isinstance(config.LOGGING_TO_FILE, bool)
        assert config.LOGGING_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        assert config.LOGGING_FORMAT in ['detailed', 'standard', 'simple']

    def test_file_caps_setting(self):
        """Test default file caps setting"""
        assert hasattr(config, 'DEFAULT_FILE_CAPS')
        assert isinstance(config.DEFAULT_FILE_CAPS, dict)

        # Should have caps for common file types
        expected_types = ['csv', 'json', 'xlsx', 'txt']
        for file_type in expected_types:
            assert file_type in config.DEFAULT_FILE_CAPS
            assert isinstance(config.DEFAULT_FILE_CAPS[file_type], int)
            assert config.DEFAULT_FILE_CAPS[file_type] > 0


class TestConfigValues:
    """Test that config values are sensible"""

    def test_season_is_reasonable(self):
        """Test that season year is within reasonable range"""
        current_year = 2025  # Approximate current year
        assert config.NFL_SCORES_SEASON >= current_year - 10
        assert config.NFL_SCORES_SEASON <= current_year + 5

    def test_week_is_valid_nfl_week(self):
        """Test that week number is valid for NFL"""
        # NFL regular season is weeks 1-18, preseason 0-4, postseason 19-22
        assert config.NFL_SCORES_CURRENT_WEEK >= 0
        assert config.NFL_SCORES_CURRENT_WEEK <= 22

    def test_timeout_is_reasonable(self):
        """Test that request timeout is reasonable"""
        # Should be at least 5 seconds, not more than 120 seconds
        assert config.REQUEST_TIMEOUT >= 5
        assert config.REQUEST_TIMEOUT <= 120

    def test_rate_limit_is_reasonable(self):
        """Test that rate limit delay is reasonable"""
        # Should be at least 0, not more than 5 seconds
        assert config.RATE_LIMIT_DELAY >= 0
        assert config.RATE_LIMIT_DELAY <= 5.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
