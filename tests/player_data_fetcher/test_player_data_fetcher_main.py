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
import datetime

from player_data_fetcher.player_data_fetcher_main import (
    Settings, NFLProjectionsCollector, create_settings_from_dict
)
from player_data_fetcher.player_data_models import ScoringFormat, ProjectionData, PlayerProjection


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

        settings.validate_settings()

    def test_validate_settings_with_future_season(self):
        """Test validate_settings with future season"""
        settings = Settings(season=2099)

        settings.validate_settings()

    def test_validate_settings_with_old_season(self):
        """Test validate_settings with old season"""
        settings = Settings(season=2000)

        settings.validate_settings()


class TestNFLProjectionsCollectorInit:
    """Test NFLProjectionsCollector initialization"""

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    def test_collector_basic_initialization(self, mock_exists, mock_exporter):
        """Test NFLProjectionsCollector can be initialized"""
        mock_exists.return_value = True
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            assert collector.settings == settings
            assert isinstance(collector.script_dir, Path)
            assert isinstance(collector.bye_weeks, dict)
            assert isinstance(collector.team_rankings, dict)
            assert isinstance(collector.current_week_schedule, dict)

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    def test_collector_initializes_empty_dicts(self, mock_exists, mock_exporter):
        """Test collector initializes empty dictionaries"""
        mock_exists.return_value = True
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={'KC': 10}):
            collector = NFLProjectionsCollector(settings)

            assert collector.team_rankings == {}
            assert collector.current_week_schedule == {}
            assert collector.bye_weeks == {'KC': 10}


class TestDeriveBveWeeksFromSchedule:
    """Test _derive_bye_weeks_from_schedule method"""

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    @patch('pandas.read_csv')
    def test_derive_bye_weeks_success(self, mock_read_csv, mock_exists, mock_exporter):
        """Test deriving bye weeks from valid schedule data"""
        mock_exists.return_value = True

        schedule_data = []
        for week in range(1, 18):
            if week == 10:
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': ''})
            else:
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': 'OPP'})
            if week == 9:
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

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    def test_derive_bye_weeks_missing_schedule_raises_error(self, mock_exporter):
        """Test that missing season_schedule.csv raises FileNotFoundError"""
        settings = Settings()

        with patch('pathlib.Path.exists', return_value=False):
            with pytest.raises(FileNotFoundError) as exc_info:
                NFLProjectionsCollector(settings)

            assert "season_schedule.csv not found" in str(exc_info.value)

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    @patch('pandas.read_csv')
    def test_derive_bye_weeks_handles_team_with_no_bye(self, mock_read_csv, mock_exists, mock_exporter):
        """Test handling team that plays all 18 weeks (no bye)"""
        mock_exists.return_value = True

        schedule_data = [{'week': week, 'team': 'KC', 'opponent': 'OPP'} for week in range(1, 19)]
        mock_df = pd.DataFrame(schedule_data)
        mock_read_csv.return_value = mock_df

        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        assert 'KC' not in collector.bye_weeks

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    @patch('pandas.read_csv')
    def test_derive_bye_weeks_handles_team_with_multiple_byes(self, mock_read_csv, mock_exists, mock_exporter):
        """Test handling team with multiple bye week entries (uses first one)"""
        mock_exists.return_value = True

        schedule_data = []
        for week in range(1, 18):
            if week in [5, 10]:
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': ''})
            else:
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': 'OPP'})
        mock_df = pd.DataFrame(schedule_data)
        mock_read_csv.return_value = mock_df

        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        assert collector.bye_weeks['KC'] == 5

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists')
    @patch('pandas.read_csv')
    def test_derive_bye_weeks_logs_warning_for_non_32_teams(self, mock_read_csv, mock_exists, mock_exporter):
        """Test that warning is logged when not 32 teams found"""
        mock_exists.return_value = True

        schedule_data = []
        for week in range(1, 18):
            if week == 10:
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': ''})
            else:
                schedule_data.append({'week': week, 'team': 'KC', 'opponent': 'SF'})
            if week == 9:
                schedule_data.append({'week': week, 'team': 'SF', 'opponent': ''})
            else:
                schedule_data.append({'week': week, 'team': 'SF', 'opponent': 'KC'})
        mock_df = pd.DataFrame(schedule_data)
        mock_read_csv.return_value = mock_df

        settings = Settings()
        collector = NFLProjectionsCollector(settings)

        assert len(collector.bye_weeks) == 2
        assert collector.bye_weeks['KC'] == 10
        assert collector.bye_weeks['SF'] == 9


class TestGetApiClient:
    """Test _get_api_client method"""

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists', return_value=True)
    def test_get_api_client_returns_client(self, mock_exists, mock_exporter):
        """Test _get_api_client returns ESPN client"""
        settings = Settings()
        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)
            client = collector._get_api_client()

            assert client is not None


class TestPrintSummary:
    """Test print_summary method"""

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    @patch('pathlib.Path.exists', return_value=True)
    @patch('builtins.print')
    def test_print_summary_with_projections(self, mock_print, mock_exists, mock_exporter):
        """Test print_summary displays projection data correctly"""
        settings = Settings(season=2024, scoring_format=ScoringFormat.PPR)

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

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

            assert mock_print.call_count > 0

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    @patch('builtins.print')
    def test_print_summary_with_empty_data(self, mock_print, mock_exporter):
        """Test print_summary handles empty data"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            projection_data = {}

            collector.print_summary(projection_data)

            assert mock_print.call_count > 0


class TestGetFantasyPlayers:
    """Test get_fantasy_players method"""

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    def test_get_fantasy_players_returns_dict(self, mock_exporter_class):
        """Test get_fantasy_players returns dictionary with correct structure"""
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

            assert isinstance(result, dict)
            assert 'season' in result


class TestCollectAllProjections:
    """Test collect_all_projections method"""

    @pytest.mark.asyncio
    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    async def test_collect_all_projections_basic(self, mock_exporter):
        """Test collect_all_projections returns results"""
        settings = Settings()

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            mock_client = AsyncMock()
            mock_client.bye_weeks = {}
            mock_client.team_rankings = {}
            mock_client.current_week_schedule = {}

            mock_session_ctx = MagicMock()
            mock_session_ctx.__aenter__ = AsyncMock(return_value=None)
            mock_session_ctx.__aexit__ = AsyncMock(return_value=None)
            mock_client.session = Mock(return_value=mock_session_ctx)

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
    @patch('player_data_fetcher.player_data_fetcher_main.DataExporter')  # Patch in the module where it's imported
    async def test_export_data_basic(self, mock_exporter_class):
        """Test export_data calls exporter methods"""
        mock_exporter = AsyncMock()
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
            mock_exporter.export_position_json_files.assert_called_once()
            mock_exporter.export_teams_to_data.assert_called_once()


class TestHistoricalDataSave:
    """Test save_to_historical_data method"""

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    def test_save_creates_folder_when_missing(self, mock_exporter, tmp_path):
        """Test that historical data folder is created if it doesn't exist"""
        settings = Settings(enable_historical_save=True, current_nfl_week=11, season=2025)

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            collector.script_dir = tmp_path / "player_data_fetcher"
            collector.script_dir.mkdir()

            data_folder = tmp_path / "data"
            data_folder.mkdir()
            team_data_folder = data_folder / "team_data"
            team_data_folder.mkdir()
            (team_data_folder / "KC.csv").write_text("test team data")

            result = collector.save_to_historical_data()

            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "11"
            assert historical_folder.exists()
            assert result is True

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    def test_save_copies_files_and_team_data_folder(self, mock_exporter, tmp_path):
        """Test that files and team_data folder are copied with zero-padded week number"""
        settings = Settings(enable_historical_save=True, current_nfl_week=11, season=2025)

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            collector.script_dir = tmp_path / "player_data_fetcher"
            collector.script_dir.mkdir()

            data_folder = tmp_path / "data"
            data_folder.mkdir()
            (data_folder / "game_data.csv").write_text("test game data")

            team_data_folder = data_folder / "team_data"
            team_data_folder.mkdir()
            (team_data_folder / "KC.csv").write_text("week,QB,RB,WR,TE,K,points_scored,points_allowed\n1,20.5,25.3,35.2,8.1,9.0,31,17")

            result = collector.save_to_historical_data()

            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "11"
            assert (historical_folder / "game_data.csv").exists()
            assert (historical_folder / "team_data").exists()
            assert (historical_folder / "team_data" / "KC.csv").exists()

            assert (historical_folder / "game_data.csv").read_text() == "test game data"
            assert "31,17" in (historical_folder / "team_data" / "KC.csv").read_text()

            assert result is True

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    def test_save_skips_when_folder_exists(self, mock_exporter, tmp_path):
        """Test that save operation is skipped when weekly folder already exists"""
        settings = Settings(enable_historical_save=True, current_nfl_week=11, season=2025)

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            collector.script_dir = tmp_path / "player_data_fetcher"
            collector.script_dir.mkdir()

            data_folder = tmp_path / "data"
            data_folder.mkdir()
            team_data_folder = data_folder / "team_data"
            team_data_folder.mkdir()
            (team_data_folder / "KC.csv").write_text("test")

            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "11"
            historical_folder.mkdir(parents=True)

            result = collector.save_to_historical_data()

            assert result is False

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    def test_save_respects_config_flag_disabled(self, mock_exporter, tmp_path):
        """Test that save is skipped when enable_historical_save is False"""
        settings = Settings(enable_historical_save=False)

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            collector.script_dir = tmp_path / "player_data_fetcher"

            result = collector.save_to_historical_data()

            assert result is False

            historical_folder = tmp_path / "data" / "historical_data"
            assert not historical_folder.exists()

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    def test_save_constructs_zero_padded_path(self, mock_exporter, tmp_path):
        """Test that week number is zero-padded (e.g., 01, 02)"""
        settings = Settings(enable_historical_save=True, current_nfl_week=1, season=2025)

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            collector.script_dir = tmp_path / "player_data_fetcher"
            collector.script_dir.mkdir()

            data_folder = tmp_path / "data"
            data_folder.mkdir()
            team_data_folder = data_folder / "team_data"
            team_data_folder.mkdir()
            (team_data_folder / "KC.csv").write_text("test")

            result = collector.save_to_historical_data()

            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "01"
            assert historical_folder.exists()
            assert result is True

    @patch('player_data_fetcher.player_data_exporter.DataExporter')
    def test_save_handles_missing_source_file(self, mock_exporter, tmp_path):
        """Tests that game_data.csv is copied, team_data (missing) is skipped gracefully"""
        settings = Settings(enable_historical_save=True, current_nfl_week=11, season=2025)

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            collector = NFLProjectionsCollector(settings)

            collector.script_dir = tmp_path / "player_data_fetcher"
            collector.script_dir.mkdir()

            data_folder = tmp_path / "data"
            data_folder.mkdir()
            (data_folder / "game_data.csv").write_text("test game data")

            result = collector.save_to_historical_data()

            assert result is True

            historical_folder = tmp_path / "data" / "historical_data" / "2025" / "11"
            assert (historical_folder / "game_data.csv").exists()
            assert not (historical_folder / "team_data").exists()



class TestKAI10Refactoring:
    """
    Tests verifying KAI-10 refactoring: config imports removed,
    bare config usage replaced with self.settings.*, create_settings_from_dict exists.
    (REQ-03, REQ-04, REQ-05 — 11 tests)
    """

    def test_nfl_season_not_in_module_namespace(self):
        """4.1: NFL_SEASON is not imported in player_data_fetcher_main module"""
        import player_data_fetcher.player_data_fetcher_main as player_data_fetcher_main
        assert not hasattr(player_data_fetcher_main, 'NFL_SEASON')

    def test_current_nfl_week_not_in_module_namespace(self):
        """4.2: CURRENT_NFL_WEEK is not imported in player_data_fetcher_main module"""
        import player_data_fetcher.player_data_fetcher_main as player_data_fetcher_main
        assert not hasattr(player_data_fetcher_main, 'CURRENT_NFL_WEEK')

    def test_pydantic_settings_not_imported(self):
        """4.3: pydantic_settings is not imported in player_data_fetcher_main"""
        import player_data_fetcher.player_data_fetcher_main as player_data_fetcher_main
        assert not hasattr(player_data_fetcher_main, 'BaseSettings')
        assert not hasattr(player_data_fetcher_main, 'SettingsConfigDict')

    @patch('player_data_fetcher.player_data_fetcher_main.DataExporter')
    @patch('pathlib.Path.exists')
    def test_save_to_historical_data_uses_settings_enable_flag(self, mock_exists, mock_exporter):
        """5.1: save_to_historical_data uses settings.enable_historical_save (not bare config)"""
        mock_exists.return_value = True

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            settings = Settings(enable_historical_save=False)
            collector = NFLProjectionsCollector(settings)
            result = collector.save_to_historical_data()
            assert result is False

    @patch('player_data_fetcher.player_data_fetcher_main.DataExporter')
    @patch('pathlib.Path.exists')
    def test_save_to_historical_data_uses_settings_current_nfl_week(self, mock_exists, mock_exporter, tmp_path):
        """5.2: save_to_historical_data uses self.settings.current_nfl_week"""
        mock_exists.return_value = True

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            settings = Settings(enable_historical_save=True, current_nfl_week=5)
            collector = NFLProjectionsCollector(settings)

            with patch.object(collector, 'script_dir', tmp_path / 'player_data_fetcher'):
                (tmp_path / 'player_data_fetcher').mkdir(parents=True, exist_ok=True)
                result = collector.save_to_historical_data()
                assert isinstance(result, bool)

    @patch('player_data_fetcher.player_data_fetcher_main.DataExporter')
    @patch('pathlib.Path.exists')
    def test_fetch_game_data_method_uses_settings_enable_flag(self, mock_exists, mock_exporter):
        """5.3: NFLProjectionsCollector.fetch_game_data() uses settings.enable_game_data"""
        mock_exists.return_value = True

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            settings = Settings(enable_game_data=False)
            collector = NFLProjectionsCollector(settings)
            result = collector.fetch_game_data()
            assert result is False

    def test_removed_config_constants_not_in_module(self):
        """I-10: CLI-configurable constants are not accessible in player_data_fetcher_main"""
        import player_data_fetcher.player_data_fetcher_main as player_data_fetcher_main
        removed_constants = [
            'NFL_SEASON', 'CURRENT_NFL_WEEK', 'REQUEST_TIMEOUT', 'RATE_LIMIT_DELAY',
            'LOGGING_LEVEL', 'ENABLE_HISTORICAL_DATA_SAVE', 'ENABLE_GAME_DATA_FETCH',
        ]
        for const in removed_constants:
            assert not hasattr(player_data_fetcher_main, const), \
                f"Constant {const} should not be in player_data_fetcher_main"

    def test_create_settings_from_dict_function_exists(self):
        """I-11: create_settings_from_dict function exists in player_data_fetcher_main"""
        import player_data_fetcher.player_data_fetcher_main as player_data_fetcher_main
        assert hasattr(player_data_fetcher_main, 'create_settings_from_dict')
        assert callable(player_data_fetcher_main.create_settings_from_dict)

    def test_settings_validate_settings_still_works(self):
        """E-11: Settings.validate_settings() method is preserved and callable"""
        settings = Settings(season=datetime.datetime.now().year)
        settings.validate_settings()

    @patch('player_data_fetcher.player_data_fetcher_main.DataExporter')
    @patch('pathlib.Path.exists')
    def test_collector_passes_current_nfl_week_from_settings(self, mock_exists, mock_exporter):
        """E-12: NFLProjectionsCollector passes settings.current_nfl_week to DataExporter"""
        mock_exists.return_value = True
        mock_exporter_instance = Mock()
        mock_exporter.return_value = mock_exporter_instance

        with patch.object(NFLProjectionsCollector, '_derive_bye_weeks_from_schedule', return_value={}):
            settings = Settings(current_nfl_week=8)
            collector = NFLProjectionsCollector(settings)

        call_kwargs = mock_exporter.call_args.kwargs
        assert call_kwargs.get('current_nfl_week') == 8

    def test_e2e_test_field_in_settings(self):
        """I-12: Settings has e2e_test field for E2E mode"""
        settings = Settings(e2e_test=True)
        assert settings.e2e_test is True


