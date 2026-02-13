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
    @patch('pathlib.Path.exists')
    def test_collector_basic_initialization(self, mock_exists, mock_exporter):
        """Test NFLProjectionsCollector can be initialized"""
        mock_exists.return_value = True  # season_schedule.csv exists
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            assert collector.settings == settings
            assert isinstance(collector.script_dir, Path)
            assert isinstance(collector.bye_weeks, dict)
            assert isinstance(collector.team_rankings, dict)
            assert isinstance(collector.current_week_schedule, dict)

    @patch('player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    def test_collector_initializes_empty_dicts(self, mock_exists, mock_exporter):
        """Test collector initializes empty dictionaries"""
        mock_exists.return_value = True  # season_schedule.csv exists
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={'KC': 10}):
            collector = NFLProjectionsCollector(settings)

            assert collector.team_rankings == {}
            assert collector.current_week_schedule == {}
            assert collector.bye_weeks == {'KC': 10}


class TestDeriveBveWeeksFromSchedule:
    """Test _derive_bye_weeks_from_schedule method"""

    @patch('player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    @patch('pandas.read_csv')
    def test_derive_bye_weeks_success(self, mock_read_csv, mock_exists, mock_exporter):
        """Test deriving bye weeks from valid schedule data"""
        mock_exists.return_value = True  # season_schedule.csv exists

        # Create mock schedule data with bye week entries (empty opponent)
        # New logic: bye weeks are identified by empty opponent field
        schedule_data = []
        for week in range(1, 18):  # Weeks 1-17
            if week == 10:  # KC has bye week 10
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': ''})
            else:
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': 'OPP'})
            if week == 9:  # SF has bye week 9
                schedule_data.append({'week': week, 'team': 'SF', 'opponent': ''})
            else:
                schedule_data.append({'week': week, 'team': 'SF', 'opponent': 'OPP'})

        mock_df = pd.DataFrame(schedule_data)
        mock_read_csv.return_value = mock_df

        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        assert 'KC' in collector.bye_weeks
        assert 'SF' in collector.bye_weeks
        assert collector.bye_weeks['KC'] == 10
        assert collector.bye_weeks['SF'] == 9

    @patch('player_data_exporter.DataExporter')
    def test_derive_bye_weeks_missing_schedule_raises_error(self, mock_exporter):
        """Test that missing season_schedule.csv raises FileNotFoundError"""
        settings = Settings()

        # Don't mock Path.exists - let it check the actual file system
        # Since the test runs from a different directory, the file won't exist
        with patch('pathlib.Path.exists', return_value=False):
            with pytest.raises(FileNotFoundError) as exc_info:
                NFLProjectionsCollector(settings)

            assert "season_schedule.csv not found" in str(exc_info.value)

    @patch('player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    @patch('pandas.read_csv')
    def test_derive_bye_weeks_handles_team_with_no_bye(self, mock_read_csv, mock_exists, mock_exporter):
        """Test handling team that plays all 18 weeks (no bye)"""
        mock_exists.return_value = True

        # Create schedule where team plays all 18 weeks
        schedule_data = [{'week': week, 'team': 'KC', 'opponent': 'OPP'} for week in range(1, 19)]
        mock_df = pd.DataFrame(schedule_data)
        mock_read_csv.return_value = mock_df

        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        # Team with no bye should not be in bye_weeks dict
        assert 'KC' not in collector.bye_weeks

    @patch('player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    @patch('pandas.read_csv')
    def test_derive_bye_weeks_handles_team_with_multiple_byes(self, mock_read_csv, mock_exists, mock_exporter):
        """Test handling team with multiple bye week entries (uses first one)"""
        mock_exists.return_value = True

        # Create schedule where team has multiple bye week entries (empty opponent)
        schedule_data = []
        for week in range(1, 18):
            if week in [5, 10]:
                # Multiple bye week entries with empty opponent
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': ''})
            else:
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': 'OPP'})
        mock_df = pd.DataFrame(schedule_data)
        mock_read_csv.return_value = mock_df

        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        # Should use first bye week (5)
        assert collector.bye_weeks['KC'] == 5

    @patch('player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    @patch('pandas.read_csv')
    def test_derive_bye_weeks_logs_warning_for_non_32_teams(self, mock_read_csv, mock_exists, mock_exporter):
        """Test that warning is logged when not 32 teams found"""
        mock_exists.return_value = True

        # Create schedule with only 2 teams (with proper bye week entries)
        schedule_data = []
        for week in range(1, 18):  # Weeks 1-17
            if week == 10:  # KC bye week
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': ''})
            else:
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': 'SF'})
            if week == 9:  # SF bye week
                schedule_data.append({'week': week, 'team': 'SF', 'opponent': ''})
            else:
                schedule_data.append({'week': week, 'team': 'SF', 'opponent': 'KC'})
        mock_df = pd.DataFrame(schedule_data)
        mock_read_csv.return_value = mock_df

        settings = Settings()
        # Should not crash, just log warning about non-32 teams
        collector = NFLProjectionsCollector(settings)

        assert len(collector.bye_weeks) == 2
        assert collector.bye_weeks['KC'] == 10
        assert collector.bye_weeks['SF'] == 9


class TestGetApiClient:
    """Test _get_api_client method"""

    @patch('player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists', return_value=True)
    def test_get_api_client_returns_client(self, mock_exists, mock_exporter):
        """Test _get_api_client returns ESPN client"""
        settings = Settings()
        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)
            client = collector._get_api_client()

            # Should return an ESPNClient instance (we don't need to mock the class itself)
            assert client is not None


class TestPrintSummary:
    """Test print_summary method"""

    @patch('player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists', return_value=True)
    @patch('builtins.print')
    def test_print_summary_with_projections(self, mock_print, mock_exists, mock_exporter):
        """Test print_summary displays projection data correctly"""
        settings = Settings(season=2024, scoring_format=ScoringFormat.PPR)

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
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

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
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
        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
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

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
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
        # Mock the preserved export methods (legacy formats removed in KAI-9)
        mock_exporter.export_position_json_files.return_value = ['qb_data.json', 'rb_data.json']
        mock_exporter.export_teams_to_data.return_value = '../data/team_data'
        mock_exporter.set_team_rankings = Mock()
        mock_exporter.set_current_week_schedule = Mock()
        mock_exporter.set_position_defense_rankings = Mock()
        mock_exporter.set_team_weekly_data = Mock()
        mock_exporter_class.return_value = mock_exporter

        settings = Settings()
        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
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
            # Verify the new export methods were called
            mock_exporter.export_position_json_files.assert_called_once()
            mock_exporter.export_teams_to_data.assert_called_once()


class TestHistoricalDataSave:
    """Test save_to_historical_data method"""

    @patch('player_data_exporter.DataExporter')
    @patch('player_data_fetcher_main.ENABLE_HISTORICAL_DATA_SAVE', True)
    @patch('player_data_fetcher_main.CURRENT_NFL_WEEK', 11)
    @patch('player_data_fetcher_main.NFL_SEASON', 2025)
    def test_save_creates_folder_when_missing(self, mock_exporter, tmp_path):
        """Test that historical data folder is created if it doesn't exist"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            # Override script_dir to use tmp_path
            collector.script_dir = tmp_path / "player-data-fetcher"
            collector.script_dir.mkdir()

            # Create data folder with test files
            data_folder = tmp_path / "data"
            data_folder.mkdir()
            (data_folder / "players.csv").write_text("test players")
            (data_folder / "players_projected.csv").write_text("test projected")
            # Create team_data folder
            team_data_folder = data_folder / "team_data"
            team_data_folder.mkdir()
            (team_data_folder / "KC.csv").write_text("test team data")

            # Call save method
            result = collector.save_to_historical_data()

            # Verify folder was created with zero-padded week number
            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "11"
            assert historical_folder.exists()
            assert result is True

    @patch('player_data_exporter.DataExporter')
    @patch('player_data_fetcher_main.ENABLE_HISTORICAL_DATA_SAVE', True)
    @patch('player_data_fetcher_main.CURRENT_NFL_WEEK', 11)
    @patch('player_data_fetcher_main.NFL_SEASON', 2025)
    def test_save_copies_files_and_team_data_folder(self, mock_exporter, tmp_path):
        """Test that files and team_data folder are copied with zero-padded week number"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            # Override script_dir
            collector.script_dir = tmp_path / "player-data-fetcher"
            collector.script_dir.mkdir()

            # Create data folder with test files
            data_folder = tmp_path / "data"
            data_folder.mkdir()
            (data_folder / "players.csv").write_text("test players data")
            (data_folder / "players_projected.csv").write_text("test projected data")

            # Create team_data folder with test team files
            team_data_folder = data_folder / "team_data"
            team_data_folder.mkdir()
            (team_data_folder / "KC.csv").write_text("week,QB,RB,WR,TE,K,points_scored,points_allowed\n1,20.5,25.3,35.2,8.1,9.0,31,17")

            # Call save method
            result = collector.save_to_historical_data()

            # Verify files and team_data folder were copied
            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "11"
            assert (historical_folder / "players.csv").exists()
            assert (historical_folder / "players_projected.csv").exists()
            assert (historical_folder / "team_data").exists()
            assert (historical_folder / "team_data" / "KC.csv").exists()

            # Verify file contents
            assert (historical_folder / "players.csv").read_text() == "test players data"
            assert (historical_folder / "players_projected.csv").read_text() == "test projected data"
            assert "31,17" in (historical_folder / "team_data" / "KC.csv").read_text()

            assert result is True

    @patch('player_data_exporter.DataExporter')
    @patch('player_data_fetcher_main.ENABLE_HISTORICAL_DATA_SAVE', True)
    @patch('player_data_fetcher_main.CURRENT_NFL_WEEK', 11)
    @patch('player_data_fetcher_main.NFL_SEASON', 2025)
    def test_save_skips_when_folder_exists(self, mock_exporter, tmp_path):
        """Test that save operation is skipped when weekly folder already exists"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            # Override script_dir
            collector.script_dir = tmp_path / "player-data-fetcher"
            collector.script_dir.mkdir()

            # Create data folder with test files
            data_folder = tmp_path / "data"
            data_folder.mkdir()
            (data_folder / "players.csv").write_text("test")
            (data_folder / "players_projected.csv").write_text("test")
            # Create team_data folder
            team_data_folder = data_folder / "team_data"
            team_data_folder.mkdir()
            (team_data_folder / "KC.csv").write_text("test")

            # Create historical folder (already exists)
            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "11"
            historical_folder.mkdir(parents=True)

            # Call save method
            result = collector.save_to_historical_data()

            # Should return False (already exists, skip)
            assert result is False

    @patch('player_data_exporter.DataExporter')
    @patch('player_data_fetcher_main.ENABLE_HISTORICAL_DATA_SAVE', False)
    def test_save_respects_config_flag_disabled(self, mock_exporter, tmp_path):
        """Test that save is skipped when ENABLE_HISTORICAL_DATA_SAVE is False"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            # Override script_dir
            collector.script_dir = tmp_path / "player-data-fetcher"

            # Call save method
            result = collector.save_to_historical_data()

            # Should return False (disabled)
            assert result is False

            # Verify no folder was created
            historical_folder = tmp_path / "data" / "historical_data"
            assert not historical_folder.exists()

    @patch('player_data_exporter.DataExporter')
    @patch('player_data_fetcher_main.ENABLE_HISTORICAL_DATA_SAVE', True)
    @patch('player_data_fetcher_main.CURRENT_NFL_WEEK', 1)
    @patch('player_data_fetcher_main.NFL_SEASON', 2025)
    def test_save_constructs_zero_padded_path(self, mock_exporter, tmp_path):
        """Test that week number is zero-padded (e.g., 01, 02)"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            # Override script_dir
            collector.script_dir = tmp_path / "player-data-fetcher"
            collector.script_dir.mkdir()

            # Create data folder with test files
            data_folder = tmp_path / "data"
            data_folder.mkdir()
            (data_folder / "players.csv").write_text("test")
            (data_folder / "players_projected.csv").write_text("test")
            # Create team_data folder
            team_data_folder = data_folder / "team_data"
            team_data_folder.mkdir()
            (team_data_folder / "KC.csv").write_text("test")

            # Call save method with week 1
            result = collector.save_to_historical_data()

            # Verify folder created with zero-padded number "01" (not "1")
            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "01"
            assert historical_folder.exists()
            assert result is True

    @patch('player_data_exporter.DataExporter')
    @patch('player_data_fetcher_main.ENABLE_HISTORICAL_DATA_SAVE', True)
    @patch('player_data_fetcher_main.CURRENT_NFL_WEEK', 11)
    @patch('player_data_fetcher_main.NFL_SEASON', 2025)
    def test_save_handles_missing_source_file(self, mock_exporter, tmp_path):
        """Test graceful handling when source file is missing"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            # Override script_dir
            collector.script_dir = tmp_path / "player-data-fetcher"
            collector.script_dir.mkdir()

            # Create data folder but with only 2 files (missing team_data folder)
            data_folder = tmp_path / "data"
            data_folder.mkdir()
            (data_folder / "players.csv").write_text("test")
            (data_folder / "players_projected.csv").write_text("test")
            # Intentionally not creating team_data folder

            # Call save method - should still succeed for existing files
            result = collector.save_to_historical_data()

            # Should still return True (partial success)
            assert result is True

            # Verify 2 files were copied
            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "11"
            assert (historical_folder / "players.csv").exists()
            assert (historical_folder / "players_projected.csv").exists()
            # team_data folder should not exist
            assert not (historical_folder / "team_data").exists()
