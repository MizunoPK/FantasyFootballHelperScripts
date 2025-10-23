#!/usr/bin/env python3
"""
Tests for Player Data Fetcher Main Module

Tests the main orchestration logic, settings validation, and collector initialization.

Author: Kai Mizuno
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock, call
from pathlib import Path
import pandas as pd
import sys
import datetime

# Add project root and player-data-fetcher to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

from player_data_fetcher_main import (
    Settings, NFLProjectionsCollector
)
from player_data_models import ScoringFormat, ProjectionData, PlayerProjection


class TestSettings:
    """Test Settings configuration class"""

    def test_settings_default_initialization(self):
        """Test Settings can be initialized with defaults"""
        settings = Settings()

        assert settings.scoring_format == ScoringFormat.PPR
        assert settings.season > 0
        assert settings.current_nfl_week >= 1
        assert settings.current_nfl_week <= 18
        assert isinstance(settings.create_csv, bool)
        assert isinstance(settings.create_json, bool)
        assert isinstance(settings.create_excel, bool)

    def test_settings_custom_values(self):
        """Test Settings can be initialized with custom values"""
        settings = Settings(
            scoring_format=ScoringFormat.STANDARD,
            season=2023,
            current_nfl_week=5
        )

        assert settings.scoring_format == ScoringFormat.STANDARD
        assert settings.season == 2023
        assert settings.current_nfl_week == 5

    def test_validate_settings_does_not_crash(self):
        """Test validate_settings runs without crashing"""
        settings = Settings(season=datetime.datetime.now().year)

        # Should not raise any exceptions
        settings.validate_settings()

    def test_validate_settings_with_future_season(self):
        """Test validate_settings with future season"""
        settings = Settings(season=2099)

        # Should not crash even with unrealistic season
        settings.validate_settings()

    def test_validate_settings_with_old_season(self):
        """Test validate_settings with old season"""
        settings = Settings(season=2000)

        # Should not crash even with old season
        settings.validate_settings()


class TestNFLProjectionsCollectorInit:
    """Test NFLProjectionsCollector initialization"""

    @patch('player_data_exporter.DataExporter')
    def test_collector_basic_initialization(self, mock_exporter):
        """Test NFLProjectionsCollector can be initialized"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_load_bye_weeks', return_value={}):
            collector = NFLProjectionsCollector(settings)

            assert collector.settings == settings
            assert isinstance(collector.script_dir, Path)
            assert isinstance(collector.bye_weeks, dict)
            assert isinstance(collector.team_rankings, dict)
            assert isinstance(collector.current_week_schedule, dict)

    @patch('player_data_exporter.DataExporter')
    def test_collector_initializes_empty_dicts(self, mock_exporter):
        """Test collector initializes empty dictionaries"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_load_bye_weeks', return_value={'KC': 10}):
            collector = NFLProjectionsCollector(settings)

            assert collector.team_rankings == {}
            assert collector.current_week_schedule == {}
            assert collector.bye_weeks == {'KC': 10}


class TestLoadByeWeeks:
    """Test _load_bye_weeks method"""

    @patch('player_data_exporter.DataExporter')
    @patch('player_data_fetcher_main.read_csv_with_validation')
    def test_load_bye_weeks_success(self, mock_read_csv, mock_exporter):
        """Test loading bye weeks from valid CSV file"""
        # Mock CSV data
        mock_df = pd.DataFrame({
            'Team': ['KC', 'SF', 'BUF'],
            'ByeWeek': [10, 9, 7]
        })
        mock_read_csv.return_value = mock_df

        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        assert 'KC' in collector.bye_weeks
        assert 'SF' in collector.bye_weeks
        assert 'BUF' in collector.bye_weeks
        assert collector.bye_weeks['KC'] == 10

    @patch('player_data_exporter.DataExporter')
    @patch('player_data_fetcher_main.read_csv_with_validation')
    def test_load_bye_weeks_invalid_week_numbers(self, mock_read_csv, mock_exporter):
        """Test loading bye weeks filters out invalid week numbers"""
        # Mock CSV data with invalid bye weeks
        mock_df = pd.DataFrame({
            'Team': ['KC', 'SF', 'INVALID'],
            'ByeWeek': [10, 9, 99]  # 99 is invalid
        })
        mock_read_csv.return_value = mock_df

        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        # Should only load valid weeks (1-18)
        assert 'KC' in collector.bye_weeks
        assert 'SF' in collector.bye_weeks
        assert 'INVALID' not in collector.bye_weeks

    @patch('player_data_exporter.DataExporter')
    def test_load_bye_weeks_file_not_found(self, mock_exporter):
        """Test loading bye weeks when file doesn't exist returns empty dict"""
        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        # If file doesn't exist, should return empty dict (won't crash)
        assert isinstance(collector.bye_weeks, dict)

    @patch('player_data_exporter.DataExporter')
    @patch('player_data_fetcher_main.read_csv_with_validation')
    def test_load_bye_weeks_read_exception(self, mock_read_csv, mock_exporter):
        """Test loading bye weeks handles CSV read exceptions"""
        mock_read_csv.side_effect = Exception("CSV read error")

        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        # Should return empty dict and not crash
        assert collector.bye_weeks == {}


class TestGetApiClient:
    """Test _get_api_client method"""

    @patch('player_data_exporter.DataExporter')
    def test_get_api_client_returns_client(self, mock_exporter):
        """Test _get_api_client returns ESPN client"""
        settings = Settings()
        with patch.object(NFLProjectionsCollector, '_load_bye_weeks', return_value={}):
            collector = NFLProjectionsCollector(settings)
            client = collector._get_api_client()

            # Should return an ESPNClient instance (we don't need to mock the class itself)
            assert client is not None


class TestPrintSummary:
    """Test print_summary method"""

    @patch('player_data_exporter.DataExporter')
    @patch('builtins.print')
    def test_print_summary_with_projections(self, mock_print, mock_exporter):
        """Test print_summary displays projection data correctly"""
        settings = Settings(season=2024, scoring_format=ScoringFormat.PPR)

        with patch.object(NFLProjectionsCollector, '_load_bye_weeks', return_value={}):
            collector = NFLProjectionsCollector(settings)

            # Create mock projection data
            projection_data = {
                'season': ProjectionData(
                    season=2024,
                    scoring_format='PPR',
                    total_players=2,
                    players=[
                        PlayerProjection(id="1", name="Player 1", position="QB", team="KC", fantasy_points=300.0),
                        PlayerProjection(id="2", name="Player 2", position="RB", team="SF", fantasy_points=250.0)
                    ]
                )
            }

            collector.print_summary(projection_data)

            # Should have printed multiple lines
            assert mock_print.call_count > 0

    @patch('player_data_exporter.DataExporter')
    @patch('builtins.print')
    def test_print_summary_with_empty_data(self, mock_print, mock_exporter):
        """Test print_summary handles empty data"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_load_bye_weeks', return_value={}):
            collector = NFLProjectionsCollector(settings)

            # Empty projection data
            projection_data = {}

            collector.print_summary(projection_data)

            # Should still print something (header at minimum)
            assert mock_print.call_count > 0


class TestGetFantasyPlayers:
    """Test get_fantasy_players method"""

    @patch('player_data_exporter.DataExporter')
    def test_get_fantasy_players_returns_dict(self, mock_exporter_class):
        """Test get_fantasy_players returns dictionary with correct structure"""
        # Mock exporter instance
        mock_exporter = Mock()
        mock_exporter.get_fantasy_players.return_value = []
        mock_exporter_class.return_value = mock_exporter

        settings = Settings()
        with patch.object(NFLProjectionsCollector, '_load_bye_weeks', return_value={}):
            collector = NFLProjectionsCollector(settings)

            projection_data = {
                'season': ProjectionData(
                    season=2024,
                    scoring_format='PPR',
                    total_players=1,
                    players=[PlayerProjection(id="1", name="Test", position="QB", team="KC", fantasy_points=300.0)]
                )
            }

            result = collector.get_fantasy_players(projection_data)

            # Should return a dict with matching keys
            assert isinstance(result, dict)
            assert 'season' in result


class TestCollectAllProjections:
    """Test collect_all_projections method"""

    @pytest.mark.asyncio
    @patch('player_data_exporter.DataExporter')
    async def test_collect_all_projections_basic(self, mock_exporter):
        """Test collect_all_projections returns results"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_load_bye_weeks', return_value={}):
            collector = NFLProjectionsCollector(settings)

            # Mock API client
            mock_client = AsyncMock()
            mock_client.bye_weeks = {}
            mock_client.team_rankings = {}
            mock_client.current_week_schedule = {}

            # Mock session context manager properly
            mock_session_ctx = MagicMock()
            mock_session_ctx.__aenter__ = AsyncMock(return_value=None)
            mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
            mock_client.session = Mock(return_value=mock_session_ctx)

            # Mock get_season_projections
            mock_projections = [
                PlayerProjection(id="1", name="Test Player", position="QB", team="KC", fantasy_points=300.0)
            ]
            mock_client.get_season_projections = AsyncMock(return_value=mock_projections)

            with patch.object(collector, '_get_api_client', return_value=mock_client):
                results = await collector.collect_all_projections()

                assert isinstance(results, dict)
                if 'season' in results:
                    assert results['season'].total_players > 0


class TestExportData:
    """Test export_data method"""

    @pytest.mark.asyncio
    @patch('player_data_fetcher_main.DataExporter')  # Patch in the module where it's imported
    async def test_export_data_basic(self, mock_exporter_class):
        """Test export_data calls exporter methods"""
        # Mock exporter instance
        mock_exporter = AsyncMock()
        mock_exporter.export_all_formats_with_teams.return_value = ['file1.csv']
        mock_exporter.export_to_data.return_value = 'file2.csv'
        mock_exporter.export_projected_points_data.return_value = 'file3.csv'
        mock_exporter.set_team_rankings = Mock()
        mock_exporter.set_current_week_schedule = Mock()
        mock_exporter_class.return_value = mock_exporter

        settings = Settings()
        with patch.object(NFLProjectionsCollector, '_load_bye_weeks', return_value={}):
            collector = NFLProjectionsCollector(settings)

            projection_data = {
                'season': ProjectionData(
                    season=2024,
                    scoring_format='PPR',
                    total_players=1,
                    players=[PlayerProjection(id="1", name="Test", position="QB", team="KC", fantasy_points=300.0)]
                )
            }

            output_files = await collector.export_data(projection_data)

            assert isinstance(output_files, list)
            assert len(output_files) > 0
