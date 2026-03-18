#!/usr/bin/env python3
"""
Tests for Schedule Data Fetcher

Tests for ScheduleFetcher class including API fetching, CSV export,
and bye week handling.

Author: Kai Mizuno
"""

import pytest
import csv
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import sys

# Add project root and schedule-data-fetcher to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "schedule-data-fetcher"))

from ScheduleFetcher import ScheduleFetcher


class TestScheduleFetcherInit:
    """Test ScheduleFetcher initialization"""

    def test_schedule_fetcher_initialization(self, tmp_path):
        """Test ScheduleFetcher can be initialized"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        assert fetcher.output_path == output_path
        assert fetcher.logger is not None
        assert fetcher.client is None

    def test_schedule_fetcher_stores_output_path(self, tmp_path):
        """Test ScheduleFetcher stores output path correctly"""
        output_path = tmp_path / "test" / "schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        assert fetcher.output_path == output_path


class TestClientManagement:
    """Test HTTP client creation and cleanup"""

    @pytest.mark.asyncio
    async def test_create_client(self, tmp_path):
        """Test _create_client creates httpx async client"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        await fetcher._create_client()

        assert fetcher.client is not None

        # Cleanup
        await fetcher._close_client()

    @pytest.mark.asyncio
    async def test_close_client(self, tmp_path):
        """Test _close_client closes httpx async client"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        await fetcher._create_client()
        assert fetcher.client is not None

        await fetcher._close_client()
        assert fetcher.client is None

    @pytest.mark.asyncio
    async def test_close_client_without_open_client(self, tmp_path):
        """Test _close_client doesn't crash when no client exists"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Should not raise any exception
        await fetcher._close_client()


class TestFetchFullSchedule:
    """Test fetch_full_schedule method"""

    @pytest.mark.asyncio
    async def test_fetch_full_schedule_basic(self, tmp_path):
        """Test fetch_full_schedule with mocked API response"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Mock API response for a single week
        mock_response = {
            'events': [
                {
                    'competitions': [
                        {
                            'competitors': [
                                {'team': {'abbreviation': 'KC'}},
                                {'team': {'abbreviation': 'BAL'}}
                            ]
                        }
                    ]
                }
            ]
        }

        # Mock _make_request to return mock response
        with patch.object(fetcher, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            # Fetch schedule for weeks 1-18
            result = await fetcher.fetch_full_schedule(2025)

            assert isinstance(result, dict)
            assert len(result) == 18  # Weeks 1-18
            assert 1 in result
            assert 'KC' in result[1]
            assert result[1]['KC'] == 'BAL'
            assert result[1]['BAL'] == 'KC'

    @pytest.mark.asyncio
    async def test_fetch_full_schedule_normalizes_team_names(self, tmp_path):
        """Test fetch_full_schedule normalizes WAS to WSH"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Mock API response with WAS (should be converted to WSH)
        mock_response = {
            'events': [
                {
                    'competitions': [
                        {
                            'competitors': [
                                {'team': {'abbreviation': 'WAS'}},
                                {'team': {'abbreviation': 'PHI'}}
                            ]
                        }
                    ]
                }
            ]
        }

        with patch.object(fetcher, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await fetcher.fetch_full_schedule(2025)

            # WAS should be converted to WSH
            assert 'WSH' in result[1]
            assert 'WAS' not in result[1]
            assert result[1]['WSH'] == 'PHI'

    @pytest.mark.asyncio
    async def test_fetch_full_schedule_handles_errors(self, tmp_path):
        """Test fetch_full_schedule handles API errors gracefully"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Mock _make_request to raise an exception
        with patch.object(fetcher, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = Exception("API error")

            result = await fetcher.fetch_full_schedule(2025)

            # Should return empty dict on error
            assert result == {}


class TestIdentifyByeWeeks:
    """Test _identify_bye_weeks method"""

    def test_identify_bye_weeks_with_full_schedule(self, tmp_path):
        """Test _identify_bye_weeks identifies teams without games"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Create schedule where KC has bye in week 5
        schedule = {
            1: {'KC': 'BAL', 'BAL': 'KC', 'PHI': 'DAL', 'DAL': 'PHI'},
            5: {'BAL': 'CIN', 'CIN': 'BAL', 'PHI': 'DAL', 'DAL': 'PHI'}  # KC missing
        }

        bye_weeks = fetcher._identify_bye_weeks(schedule)

        # KC should have bye week 5
        assert 5 in bye_weeks['KC']

    def test_identify_bye_weeks_no_byes(self, tmp_path):
        """Test _identify_bye_weeks when all teams play every week"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Schedule with all 32 teams playing in week 1
        all_teams = [
            'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
            'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
            'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
            'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH'
        ]

        schedule = {1: {}}
        for i in range(0, len(all_teams), 2):
            team1 = all_teams[i]
            team2 = all_teams[i + 1]
            schedule[1][team1] = team2
            schedule[1][team2] = team1

        bye_weeks = fetcher._identify_bye_weeks(schedule)

        # No team should have bye week 1
        for team in all_teams:
            assert 1 not in bye_weeks[team]


class TestExportToCsv:
    """Test export_to_csv method"""

    def test_export_to_csv_basic(self, tmp_path):
        """Test export_to_csv creates CSV file with correct schema"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Create simple schedule
        schedule = {
            1: {'KC': 'BAL', 'BAL': 'KC'},
            2: {'KC': 'PHI', 'PHI': 'KC'}
        }

        fetcher.export_to_csv(schedule)

        # Verify file was created
        assert output_path.exists()

        # Read and verify CSV contents
        with open(output_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            # Should have header: week,team,opponent
            assert 'week' in rows[0]
            assert 'team' in rows[0]
            assert 'opponent' in rows[0]

    def test_export_to_csv_with_bye_weeks(self, tmp_path):
        """Test export_to_csv handles bye weeks (empty opponent)"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Schedule where KC has bye in week 5 (missing from week 5)
        schedule = {
            1: {'KC': 'BAL', 'BAL': 'KC', 'PHI': 'DAL', 'DAL': 'PHI'},
            5: {'BAL': 'CIN', 'CIN': 'BAL', 'PHI': 'DAL', 'DAL': 'PHI'}
        }

        fetcher.export_to_csv(schedule)

        # Read CSV and verify KC has empty opponent in week 5
        with open(output_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            # Find KC's week 5 entry
            kc_week_5 = [r for r in rows if r['team'] == 'KC' and r['week'] == '5']
            assert len(kc_week_5) > 0
            assert kc_week_5[0]['opponent'] == ''  # Empty opponent = bye week

    def test_export_to_csv_creates_directory(self, tmp_path):
        """Test export_to_csv creates output directory if needed"""
        output_path = tmp_path / "new_dir" / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Directory doesn't exist yet
        assert not output_path.parent.exists()

        schedule = {1: {'KC': 'BAL', 'BAL': 'KC'}}
        fetcher.export_to_csv(schedule)

        # Directory should be created
        assert output_path.parent.exists()
        assert output_path.exists()

    def test_export_to_csv_sorted_output(self, tmp_path):
        """Test export_to_csv outputs sorted by week and team"""
        output_path = tmp_path / "season_schedule.csv"
        fetcher = ScheduleFetcher(output_path)

        # Create schedule out of order
        schedule = {
            2: {'PHI': 'KC', 'KC': 'PHI'},
            1: {'BAL': 'KC', 'KC': 'BAL'}
        }

        fetcher.export_to_csv(schedule)

        with open(output_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            # Should be sorted by week
            weeks = [int(r['week']) for r in rows]
            assert weeks == sorted(weeks)


class TestModuleImports:
    """Test that all expected classes can be imported"""

    def test_import_schedule_fetcher(self):
        """Test ScheduleFetcher can be imported"""
        from ScheduleFetcher import ScheduleFetcher

        assert ScheduleFetcher is not None
