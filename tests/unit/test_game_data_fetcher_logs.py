"""
Unit Tests for Feature 06: game_data_fetcher.py Log Quality

Tests verify DEBUG log quality improvements:
- Added DEBUG log for weather fetch with coordinates
- Moved "No coordinates" log to INFO level

Test Category: R3 - DEBUG Log Quality (2 tests)

Created: 2026-02-11 (Feature 06 S6 Phase 6 Task 13)
"""

import pytest


class TestGameDataFetcherLogs:
    """R3: Unit tests for game_data_fetcher.py DEBUG log quality"""

    def test_weather_fetch_debug_log_added(self):
        """T3.1: Verify DEBUG log added before weather fetch

        Validates that game_data_fetcher.py line 349 contains DEBUG log
        with format: "Fetching weather for {game_date} at {coords['lat']},{coords['lon']}"

        This was implemented in Task 3.
        """
        # Read the actual source code to verify the log was added
        with open("historical_data_compiler/game_data_fetcher.py") as f:
            content = f.read()

        # Verify the DEBUG log exists in the code
        assert 'self.logger.debug(f"Fetching weather for {game_date} at' in content, \
            "Should have DEBUG log for weather fetch"
        assert "coords['lat']" in content and "coords['lon']" in content, \
            "DEBUG log should include coordinates"

    def test_no_coordinates_info_level(self):
        """T3.2: Verify "No coordinates" moved to INFO level

        Validates that game_data_fetcher.py line 346 uses INFO level (not DEBUG)
        for "No coordinates" message since it affects data quality.

        This was implemented in Task 4.
        """
        # Read the actual source code to verify the level change
        with open("historical_data_compiler/game_data_fetcher.py") as f:
            lines = f.readlines()

        # Find the line with "No coordinates" message
        no_coords_lines = [line for line in lines if "No coordinates available" in line]

        assert len(no_coords_lines) > 0, "Should have 'No coordinates' log message"

        # Verify it uses INFO level, not DEBUG
        assert any("logger.info" in line for line in no_coords_lines), \
            "Should use INFO level for 'No coordinates' message"
        assert not any("logger.debug" in line and "No coordinates" in line for line in lines), \
            "Should NOT use DEBUG level for 'No coordinates' message"
