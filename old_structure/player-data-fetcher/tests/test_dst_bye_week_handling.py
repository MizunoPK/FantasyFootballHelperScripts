#!/usr/bin/env python3
"""
Unit tests for DST bye week handling in player data fetcher.

Tests that DST teams correctly default to 0 points when week data
cannot be found (likely bye weeks).

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import pytest
from unittest.mock import MagicMock, patch
import math

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from espn_client import ESPNClient
from player_data_models import ESPNPlayerData


class TestDSTByeWeekHandling:
    """Test DST bye week handling in ESPN client."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create mock settings
        mock_settings = MagicMock()
        mock_settings.season = 2025

        self.client = ESPNClient(mock_settings)
        self.client.logger = MagicMock()

    @pytest.mark.asyncio
    async def test_dst_bye_week_defaults_to_zero(self):
        """Test that DST teams get 0 points for weeks with no data (bye weeks)."""
        # Create mock DST player data
        dst_player = ESPNPlayerData(
            id='dst_test',
            name='Buffalo Defense',
            team='BUF',
            position='DST',
            fantasy_points=120.0
        )

        # Mock player data with no week 7 data (simulating bye week)
        mock_player_stats = {
            'stats': [
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 6,  # Week 6 has data
                    'appliedTotal': 8.5
                },
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 8,  # Week 8 has data
                    'appliedTotal': 12.0
                }
                # Week 7 is missing (bye week)
            ]
        }

        # Mock _get_all_weeks_data to return our test data
        with patch.object(self.client, '_get_all_weeks_data', return_value=mock_player_stats):
            # Test the weekly projections population
            await self.client._populate_weekly_projections(
                dst_player, 'dst_test', 'Buffalo Defense', 'DST'
            )

        # Verify week 6 and 8 have actual data
        assert dst_player.get_week_points(6) == 8.5
        assert dst_player.get_week_points(8) == 12.0

        # Verify week 7 (bye week) defaults to 0.0
        assert dst_player.get_week_points(7) == 0.0

    @pytest.mark.asyncio
    async def test_dst_negative_points_preserved(self):
        """Test that DST teams can have negative points (bad defensive performance)."""
        dst_player = ESPNPlayerData(
            id='dst_test2',
            name='Poor Defense',
            team='CHI',
            position='DST',
            fantasy_points=50.0
        )

        # Mock player data with negative points
        mock_player_stats = {
            'stats': [
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 5,
                    'appliedTotal': -3.5  # Bad defensive game
                },
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 6,
                    'projectedTotal': -1.2  # Projected negative points
                }
            ]
        }

        # Mock _get_all_weeks_data to return our test data
        with patch.object(self.client, '_get_all_weeks_data', return_value=mock_player_stats):
            await self.client._populate_weekly_projections(
                dst_player, 'dst_test2', 'Poor Defense', 'DST'
            )

        # Verify negative points are preserved for DST
        assert dst_player.get_week_points(5) == -3.5
        assert dst_player.get_week_points(6) == -1.2

    @pytest.mark.asyncio
    async def test_non_dst_zero_points_filtered(self):
        """Test that non-DST players with 0 or negative points are filtered out."""
        qb_player = ESPNPlayerData(
            id='qb_test',
            name='Test QB',
            team='KC',
            position='QB',
            fantasy_points=250.0
        )

        # Mock player data with 0 and negative points
        mock_player_stats = {
            'stats': [
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 5,
                    'appliedTotal': 0.0  # Zero points
                },
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 6,
                    'projectedTotal': -2.0  # Negative points
                },
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 7,
                    'appliedTotal': 25.5  # Positive points
                }
            ]
        }

        # Mock _get_all_weeks_data to return our test data
        with patch.object(self.client, '_get_all_weeks_data', return_value=mock_player_stats):
            await self.client._populate_weekly_projections(
                qb_player, 'qb_test', 'Test QB', 'QB'
            )

        # Zero and negative points should be filtered for non-DST players
        assert qb_player.get_week_points(5) == 0.0  # Filtered to default
        assert qb_player.get_week_points(6) == 0.0  # Filtered to default
        assert qb_player.get_week_points(7) == 25.5  # Positive points preserved

    def test_extract_raw_espn_week_points_dst_handling(self):
        """Test the raw ESPN week points extraction for DST specifically."""
        mock_player_data = {
            'stats': [
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 7,
                    'appliedTotal': -4.0  # Negative DST points
                },
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 8,
                    'projectedTotal': 0.0  # Zero DST points
                }
            ]
        }

        # Mock the settings
        self.client.settings = MagicMock()
        self.client.settings.season = 2025

        # Test DST with negative points - should be allowed
        points = self.client._extract_raw_espn_week_points(mock_player_data, 7, 'DST')
        assert points == -4.0

        # Test DST with zero points - should be allowed
        points = self.client._extract_raw_espn_week_points(mock_player_data, 8, 'DST')
        assert points == 0.0

        # Test non-DST with negative points - should be filtered
        points = self.client._extract_raw_espn_week_points(mock_player_data, 7, 'QB')
        assert points is None

        # Test non-DST with zero points - should be filtered
        points = self.client._extract_raw_espn_week_points(mock_player_data, 8, 'RB')
        assert points is None

    def test_extract_raw_espn_week_points_nan_handling(self):
        """Test that NaN values are properly handled."""
        mock_player_data = {
            'stats': [
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 7,
                    'appliedTotal': float('nan')  # NaN value
                },
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 8,
                    'projectedTotal': float('nan')  # NaN value
                }
            ]
        }

        self.client.settings = MagicMock()
        self.client.settings.season = 2025

        # NaN values should be treated as None (no data)
        points = self.client._extract_raw_espn_week_points(mock_player_data, 7, 'DST')
        assert points is None

        points = self.client._extract_raw_espn_week_points(mock_player_data, 8, 'QB')
        assert points is None

    @pytest.mark.asyncio
    async def test_dst_bye_week_logging(self):
        """Test that DST bye weeks are logged appropriately."""
        dst_player = ESPNPlayerData(
            id='dst_logging_test',
            name='Test Defense',
            team='DAL',
            position='DST',
            fantasy_points=100.0
        )

        # Mock player data with missing week (bye week)
        mock_player_stats = {'stats': []}  # No stats = bye week

        with patch.object(self.client, '_get_all_weeks_data', return_value=mock_player_stats):
            await self.client._populate_weekly_projections(
                dst_player, 'dst_logging_test', 'Test Defense', 'DST'
            )

        # Verify logging was called for bye week
        self.client.logger.debug.assert_called()

        # Check that some debug calls mention bye week
        debug_calls = [call.args[0] for call in self.client.logger.debug.call_args_list]
        bye_week_logs = [call for call in debug_calls if 'likely bye week' in call]
        assert len(bye_week_logs) > 0

    @pytest.mark.asyncio
    async def test_dst_multiple_missing_weeks(self):
        """Test DST handling when multiple weeks are missing."""
        dst_player = ESPNPlayerData(
            id='dst_multi_test',
            name='Multi Bye Defense',
            team='SF',
            position='DST',
            fantasy_points=80.0
        )

        # Mock player data with only week 1 and 17 (missing weeks 2-16)
        mock_player_stats = {
            'stats': [
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 1,
                    'appliedTotal': 15.0
                },
                {
                    'seasonId': 2025,
                    'scoringPeriodId': 17,
                    'appliedTotal': 10.0
                }
            ]
        }

        with patch.object(self.client, '_get_all_weeks_data', return_value=mock_player_stats):
            await self.client._populate_weekly_projections(
                dst_player, 'dst_multi_test', 'Multi Bye Defense', 'DST'
            )

        # Verify actual data is preserved
        assert dst_player.get_week_points(1) == 15.0
        assert dst_player.get_week_points(17) == 10.0

        # Verify all missing weeks default to 0.0
        for week in range(2, 17):
            assert dst_player.get_week_points(week) == 0.0


if __name__ == '__main__':
    pytest.main([__file__])