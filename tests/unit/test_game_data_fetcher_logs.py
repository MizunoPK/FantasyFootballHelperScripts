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
        with open("historical_data_compiler/game_data_fetcher.py") as f:
            content = f.read()

        assert 'self.logger.debug(f"Fetching weather for {game_date} at' in content, \
            "Should have DEBUG log for weather fetch"
        assert "coords['lat']" in content and "coords['lon']" in content, \
            "DEBUG log should include coordinates"

    def test_no_coordinates_info_level(self):
        """T3.2: Verify "No coordinates" uses WARNING level

        Validates that game_data_fetcher.py uses WARNING level (not INFO or DEBUG)
        for "No coordinates" message since it is a recoverable data-quality anomaly.
        """
        with open("historical_data_compiler/game_data_fetcher.py") as f:
            lines = f.readlines()

        no_coords_lines = [line for line in lines if "No coordinates available" in line]

        assert len(no_coords_lines) > 0, "Should have 'No coordinates' log message"

        assert any("logger.warning" in line for line in no_coords_lines), \
            "Should use WARNING level for 'No coordinates' message"
        assert not any(("logger.debug" in line or "logger.info" in line) and "No coordinates" in line for line in lines), \
            "Should NOT use DEBUG or INFO level for 'No coordinates' message"


