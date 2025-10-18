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

    def test_preserve_drafted_values_is_boolean(self):
        """Test PRESERVE_DRAFTED_VALUES is boolean"""
        assert isinstance(config.PRESERVE_DRAFTED_VALUES, bool)

    def test_preserve_locked_values_is_boolean(self):
        """Test PRESERVE_LOCKED_VALUES is boolean"""
        assert isinstance(config.PRESERVE_LOCKED_VALUES, bool)

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


class TestOptimizationSettings:
    """Test optimization configuration"""

    def test_skip_drafted_player_updates_is_boolean(self):
        """Test SKIP_DRAFTED_PLAYER_UPDATES is boolean"""
        assert isinstance(config.SKIP_DRAFTED_PLAYER_UPDATES, bool)

    def test_use_score_threshold_is_boolean(self):
        """Test USE_SCORE_THRESHOLD is boolean"""
        assert isinstance(config.USE_SCORE_THRESHOLD, bool)

    def test_player_score_threshold_is_numeric(self):
        """Test PLAYER_SCORE_THRESHOLD is a number"""
        assert isinstance(config.PLAYER_SCORE_THRESHOLD, (int, float))
        assert config.PLAYER_SCORE_THRESHOLD >= 0


class TestOutputSettings:
    """Test output configuration"""

    def test_output_directory_is_string(self):
        """Test OUTPUT_DIRECTORY is a string"""
        assert isinstance(config.OUTPUT_DIRECTORY, str)
        assert len(config.OUTPUT_DIRECTORY) > 0

    def test_create_csv_is_boolean(self):
        """Test CREATE_CSV is boolean"""
        assert isinstance(config.CREATE_CSV, bool)

    def test_create_json_is_boolean(self):
        """Test CREATE_JSON is boolean"""
        assert isinstance(config.CREATE_JSON, bool)

    def test_create_excel_is_boolean(self):
        """Test CREATE_EXCEL is boolean"""
        assert isinstance(config.CREATE_EXCEL, bool)

    def test_default_file_caps_is_dict(self):
        """Test DEFAULT_FILE_CAPS is a dictionary"""
        assert isinstance(config.DEFAULT_FILE_CAPS, dict)
        # Should have some file type entries
        assert len(config.DEFAULT_FILE_CAPS) > 0
        # All values should be integers
        for value in config.DEFAULT_FILE_CAPS.values():
            assert isinstance(value, int)


class TestLoggingConfiguration:
    """Test logging configuration"""

    def test_logging_level_is_valid(self):
        """Test LOGGING_LEVEL is a valid log level string"""
        assert isinstance(config.LOGGING_LEVEL, str)
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        assert config.LOGGING_LEVEL in valid_levels

    def test_logging_to_file_is_boolean(self):
        """Test LOGGING_TO_FILE is boolean"""
        assert isinstance(config.LOGGING_TO_FILE, bool)

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


class TestExportConfiguration:
    """Test export configuration"""

    def test_excel_position_sheets_is_list(self):
        """Test EXCEL_POSITION_SHEETS is a list"""
        assert isinstance(config.EXCEL_POSITION_SHEETS, list)
        assert len(config.EXCEL_POSITION_SHEETS) > 0

    def test_excel_position_sheets_contains_valid_positions(self):
        """Test EXCEL_POSITION_SHEETS contains valid position strings"""
        valid_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'D/ST', 'DEF']
        for position in config.EXCEL_POSITION_SHEETS:
            assert isinstance(position, str)
            assert position in valid_positions

    def test_export_columns_is_list(self):
        """Test EXPORT_COLUMNS is a list"""
        assert isinstance(config.EXPORT_COLUMNS, list)
        assert len(config.EXPORT_COLUMNS) > 0

    def test_export_columns_contains_required_fields(self):
        """Test EXPORT_COLUMNS contains required player fields"""
        required_fields = ['id', 'name', 'position', 'team']
        for field in required_fields:
            assert field in config.EXPORT_COLUMNS


class TestTeamRankingsConfiguration:
    """Test team rankings configuration"""

    def test_min_weeks_for_current_season_rankings_is_positive(self):
        """Test MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS is positive integer"""
        assert isinstance(config.MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS, int)
        assert config.MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS > 0
        # Should be a reasonable number of weeks
        assert config.MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS <= 18
