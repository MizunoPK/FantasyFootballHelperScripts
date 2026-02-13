#!/usr/bin/env python3
"""
Tests for Config Module

Basic smoke tests for configuration constants and validation.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
import sys

# Add project root and player-data-fetcher to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

import config


class TestNFLConfiguration:
    """Test NFL season and week configuration"""

    def test_current_nfl_week_is_valid(self):
        """Test CURRENT_NFL_WEEK is within valid range"""
        assert isinstance(config.CURRENT_NFL_WEEK, int)
        assert 1 <= config.CURRENT_NFL_WEEK <= 18

    def test_nfl_season_is_valid(self):
        """Test NFL_SEASON is a reasonable year"""
        assert isinstance(config.NFL_SEASON, int)
        assert config.NFL_SEASON >= 2020  # Reasonable lower bound
        assert config.NFL_SEASON <= 2030  # Reasonable upper bound


class TestDataPreservationSettings:
    """Test data preservation configuration"""

    def test_load_drafted_data_from_file_is_boolean(self):
        """Test LOAD_DRAFTED_DATA_FROM_FILE is boolean"""
        assert isinstance(config.LOAD_DRAFTED_DATA_FROM_FILE, bool)

    def test_drafted_data_path_is_string(self):
        """Test DRAFTED_DATA is a string path"""
        assert isinstance(config.DRAFTED_DATA, str)
        assert len(config.DRAFTED_DATA) > 0

    def test_my_team_name_is_string(self):
        """Test MY_TEAM_NAME is a string"""
        assert isinstance(config.MY_TEAM_NAME, str)


class TestLoggingConfiguration:
    """Test logging configuration"""

    def test_logging_level_is_valid(self):
        """Test LOGGING_LEVEL is a valid log level string"""
        assert isinstance(config.LOGGING_LEVEL, str)
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        assert config.LOGGING_LEVEL in valid_levels

    # Note: LOGGING_TO_FILE constant removed - file logging now controlled via --enable-log-file CLI flag

    def test_log_name_is_string(self):
        """Test LOG_NAME is a string"""
        assert isinstance(config.LOG_NAME, str)
        assert len(config.LOG_NAME) > 0

    def test_logging_format_is_valid(self):
        """Test LOGGING_FORMAT is a valid format string"""
        assert isinstance(config.LOGGING_FORMAT, str)
        valid_formats = ['detailed', 'standard', 'simple']
        assert config.LOGGING_FORMAT in valid_formats


class TestProgressTrackingConfiguration:
    """Test progress tracking configuration"""

    def test_progress_update_frequency_is_positive(self):
        """Test PROGRESS_UPDATE_FREQUENCY is positive integer"""
        assert isinstance(config.PROGRESS_UPDATE_FREQUENCY, int)
        assert config.PROGRESS_UPDATE_FREQUENCY > 0

    def test_progress_eta_window_size_is_positive(self):
        """Test PROGRESS_ETA_WINDOW_SIZE is positive integer"""
        assert isinstance(config.PROGRESS_ETA_WINDOW_SIZE, int)
        assert config.PROGRESS_ETA_WINDOW_SIZE > 0


class TestESPNAPIConfiguration:
    """Test ESPN API configuration"""

    def test_espn_user_agent_is_string(self):
        """Test ESPN_USER_AGENT is a string"""
        assert isinstance(config.ESPN_USER_AGENT, str)
        assert len(config.ESPN_USER_AGENT) > 0

    def test_espn_player_limit_is_positive(self):
        """Test ESPN_PLAYER_LIMIT is positive integer"""
        assert isinstance(config.ESPN_PLAYER_LIMIT, int)
        assert config.ESPN_PLAYER_LIMIT > 0

    def test_request_timeout_is_positive(self):
        """Test REQUEST_TIMEOUT is positive number"""
        assert isinstance(config.REQUEST_TIMEOUT, (int, float))
        assert config.REQUEST_TIMEOUT > 0

    def test_rate_limit_delay_is_non_negative(self):
        """Test RATE_LIMIT_DELAY is non-negative number"""
        assert isinstance(config.RATE_LIMIT_DELAY, (int, float))
        assert config.RATE_LIMIT_DELAY >= 0


class TestTeamDataConfiguration:
    """Test team data configuration"""

    def test_team_data_folder_is_valid_path(self):
        """Test TEAM_DATA_FOLDER is a valid path string"""
        assert isinstance(config.TEAM_DATA_FOLDER, str)
        assert len(config.TEAM_DATA_FOLDER) > 0
        # Should be a relative path
        assert 'team_data' in config.TEAM_DATA_FOLDER
