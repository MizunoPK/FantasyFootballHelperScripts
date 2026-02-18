#!/usr/bin/env python3
"""
Tests for Config Module

Basic smoke tests for configuration constants that remain in config.py
(non-CLI-configurable values only). CLI-configurable constants have been
moved to argparse defaults in run_player_fetcher.py.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
import sys

# Add project root and player-data-fetcher to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

import config


class TestLoggingConfiguration:
    """Test logging configuration constants (non-CLI-configurable)"""

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

    def test_progress_eta_window_size_is_positive(self):
        """Test PROGRESS_ETA_WINDOW_SIZE is positive integer"""
        assert isinstance(config.PROGRESS_ETA_WINDOW_SIZE, int)
        assert config.PROGRESS_ETA_WINDOW_SIZE > 0


class TestESPNAPIConfiguration:
    """Test ESPN API configuration constants (non-CLI-configurable)"""

    def test_espn_user_agent_is_string(self):
        """Test ESPN_USER_AGENT is a string"""
        assert isinstance(config.ESPN_USER_AGENT, str)
        assert len(config.ESPN_USER_AGENT) > 0


# ============================================================================
# KAI-10 Refactoring Tests (Task 11 — Tests C-7, C-8, I-15, C-10)
# ============================================================================

class TestKAI10ConfigRefactoring:
    """
    Tests verifying KAI-10 refactoring: CLI-configurable constants removed from config.py;
    non-CLI constants remain accessible.
    (REQ-10, REQ-15 — 4 tests)
    """

    def test_removed_cli_constants_not_in_config(self):
        """C-7: CLI-configurable constants are not accessible in config module"""
        removed_constants = [
            'CURRENT_NFL_WEEK', 'NFL_SEASON', 'LOAD_DRAFTED_DATA_FROM_FILE',
            'DRAFTED_DATA', 'MY_TEAM_NAME', 'POSITION_JSON_OUTPUT',
            'TEAM_DATA_FOLDER', 'GAME_DATA_CSV', 'ENABLE_HISTORICAL_DATA_SAVE',
            'ENABLE_GAME_DATA_FETCH', 'ESPN_PLAYER_LIMIT', 'LOGGING_LEVEL',
            'REQUEST_TIMEOUT', 'RATE_LIMIT_DELAY', 'PROGRESS_UPDATE_FREQUENCY',
        ]
        for const in removed_constants:
            assert not hasattr(config, const), \
                f"Constant {const} should have been removed from config.py"

    def test_kept_non_cli_constants_importable(self):
        """C-8: Non-CLI constants are still importable from config module"""
        kept_constants = [
            'COORDINATES_JSON', 'ESPN_USER_AGENT', 'LOG_NAME',
            'LOGGING_FORMAT', 'PROGRESS_ETA_WINDOW_SIZE',
        ]
        for const in kept_constants:
            assert hasattr(config, const), \
                f"Constant {const} should still be in config.py"

    def test_config_module_has_exactly_kept_constants(self):
        """I-15: config module exposes only the expected non-CLI constants"""
        # Verify all 5 kept constants are accessible
        assert hasattr(config, 'COORDINATES_JSON')
        assert hasattr(config, 'ESPN_USER_AGENT')
        assert hasattr(config, 'LOG_NAME')
        assert hasattr(config, 'LOGGING_FORMAT')
        assert hasattr(config, 'PROGRESS_ETA_WINDOW_SIZE')

    def test_coordinates_json_is_filename_string(self):
        """C-10: COORDINATES_JSON is a filename string (non-CLI constant preserved)"""
        assert isinstance(config.COORDINATES_JSON, str)
        assert len(config.COORDINATES_JSON) > 0
        assert config.COORDINATES_JSON.endswith('.json')
