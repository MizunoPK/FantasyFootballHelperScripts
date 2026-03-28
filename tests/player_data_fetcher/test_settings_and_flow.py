#!/usr/bin/env python3
"""
Tests for Settings dataclass and settings flow (KAI-10 — REQ-02, REQ-03, REQ-11, REQ-13, REQ-14)

Tests Settings construction, create_settings_from_dict(), main() signature,
E2E graceful skip, backward compatibility, and log level wiring.

Author: Kai Mizuno
"""

import inspect
import os
import pytest
from unittest.mock import patch, AsyncMock, Mock, MagicMock

from player_data_fetcher.player_data_fetcher_main import Settings, create_settings_from_dict, main
from player_data_fetcher.player_data_models import ProjectionData


# ============================================================================
# Helper: build minimal valid settings dict
# ============================================================================

def _make_settings_dict(**overrides):
    """Build a minimal valid settings dict, with all required keys."""
    base = {
        'e2e_test': False,
        'log_level': 'INFO',
        'logging_to_file': False,
        'current_nfl_week': 17,
        'season': 2025,
        'my_team_name': 'Sea Sharp',
        'load_drafted_data': False,       # Disable to avoid file checks
        'drafted_data_path': '../data/drafted_data.csv',
        'position_json_output': '../data/player_data',
        'team_data_folder': '../data/team_data',
        'game_data_csv': '../data/game_data.csv',
        'enable_historical_save': False,
        'enable_game_data': False,        # Disable to avoid network calls
        'espn_player_limit': 100,
        'request_timeout': 30,
        'rate_limit_delay': 0.2,
        'progress_frequency': 10,
    }
    base.update(overrides)
    return base


# ============================================================================
# Tests 3.1-3.5 + 2.3: Settings @dataclass and create_settings_from_dict
# ============================================================================

class TestSettingsDataclass:
    """Test Settings @dataclass construction and fields"""

    def test_settings_default_initialization(self):
        """3.1: Settings() works with no args; all defaults set correctly"""
        settings = Settings()
        assert settings.season == 2025
        assert settings.current_nfl_week == 17
        assert settings.log_level == 'INFO'
        assert settings.e2e_test is False

    def test_settings_keyword_construction(self):
        """3.2: Settings(season=2024) keyword construction works"""
        settings = Settings(season=2024)
        assert settings.season == 2024

    def test_settings_has_all_18_required_fields(self):
        """3.3: Settings has all 18 required fields"""
        settings = Settings()
        required_fields = [
            'scoring_format', 'season', 'current_nfl_week', 'request_timeout',
            'rate_limit_delay', 'espn_player_limit', 'position_json_output',
            'team_data_folder', 'game_data_csv',
            'enable_historical_save', 'enable_game_data', 'load_drafted_data',
            'drafted_data_path', 'my_team_name', 'progress_frequency',
            'log_level', 'logging_to_file', 'e2e_test',
        ]
        for field in required_fields:
            assert hasattr(settings, field), f"Missing field: {field}"

    def test_create_settings_from_dict_maps_current_nfl_week(self):
        """3.4: create_settings_from_dict maps dict 'current_nfl_week' to Settings field"""
        d = _make_settings_dict(current_nfl_week=10)
        settings = create_settings_from_dict(d)
        assert settings.current_nfl_week == 10

    def test_create_settings_from_dict_with_multiple_fields(self):
        """3.5: create_settings_from_dict correctly maps all provided fields"""
        d = _make_settings_dict(season=2023, current_nfl_week=5, log_level='DEBUG')
        settings = create_settings_from_dict(d)
        assert settings.season == 2023
        assert settings.current_nfl_week == 5
        assert settings.log_level == 'DEBUG'

    def test_main_signature_accepts_none_default(self):
        """2.3: main() has settings_dict=None default (backward compat signature)"""
        sig = inspect.signature(main)
        params = sig.parameters
        assert 'settings_dict' in params
        assert params['settings_dict'].default is None


# ============================================================================
# Tests I-4, I-5, I-13, I-14: main() integration
# ============================================================================

class TestMainSignature:
    """Test main() function signature and integration with settings"""

    @pytest.mark.asyncio
    async def test_main_accepts_settings_dict(self):
        """I-4: main(settings_dict) builds Settings from dict and runs"""
        settings_dict = _make_settings_dict()
        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'qb': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
                # Should not raise
                await main(settings_dict)

    def test_main_settings_dict_parameter_exists(self):
        """I-5: main() accepts settings_dict=None (backward compat for direct invocation)"""
        sig = inspect.signature(main)
        assert 'settings_dict' in sig.parameters

    def test_main_settings_dict_defaults_to_none(self):
        """I-13: main() has settings_dict=None default"""
        sig = inspect.signature(main)
        param = sig.parameters['settings_dict']
        assert param.default is None

    def test_log_level_passed_through_to_settings(self):
        """I-14: log_level from settings dict is stored in Settings"""
        d = _make_settings_dict(log_level='WARNING')
        settings = create_settings_from_dict(d)
        assert settings.log_level == 'WARNING'


# ============================================================================
# Tests E-8, E-9, E-19, C-9: edge cases for settings construction
# ============================================================================

class TestSettingsEdgeCases:
    """Edge case tests for Settings construction"""

    def test_extra_keys_in_dict_do_not_cause_error(self):
        """E-8: Extra keys in args_dict are ignored (not accessed by create_settings_from_dict)"""
        d = _make_settings_dict()
        d['completely_unknown_key'] = 'surprise_value'
        # create_settings_from_dict only reads known keys
        settings = create_settings_from_dict(d)
        assert settings.season == d['season']

    def test_env_var_no_longer_overrides_settings(self):
        """E-9: NFL_PROJ_* env vars no longer override settings (pydantic removed)"""
        with patch.dict(os.environ, {'NFL_PROJ_SEASON': '1999'}):
            settings = Settings()
            assert settings.season != 1999  # Env var is ignored

    def test_week_to_current_nfl_week_mapping(self):
        """E-19: Runner's --week arg maps to 'current_nfl_week' in dict → Settings.current_nfl_week"""
        # Simulate the runner's create_settings_dict storing --week as current_nfl_week
        d = _make_settings_dict(current_nfl_week=7)
        settings = create_settings_from_dict(d)
        assert settings.current_nfl_week == 7

    def test_settings_works_without_config_cli_constants(self):
        """C-9: Settings() can be constructed with explicit values (no config.py CLI constants)"""
        settings = Settings(
            season=2024,
            current_nfl_week=10,
            espn_player_limit=500,
        )
        assert settings.season == 2024
        assert settings.current_nfl_week == 10
        assert settings.espn_player_limit == 500


# ============================================================================
# Tests 11.2, 11.3, E-1, E-2: E2E graceful skip behavior
# ============================================================================

class TestE2EGracefulSkip:
    """Test E2E graceful skip for missing drafted data file"""

    @pytest.mark.asyncio
    async def test_e2e_missing_drafted_file_no_exception(self, tmp_path):
        """11.2 / E-1: E2E mode + missing drafted data file → no FileNotFoundError"""
        missing_path = str(tmp_path / 'nonexistent_drafted.csv')
        settings_dict = _make_settings_dict(
            e2e_test=True,
            load_drafted_data=True,
            drafted_data_path=missing_path,
        )
        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'qb': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
                # Should NOT raise FileNotFoundError
                await main(settings_dict)

    @pytest.mark.asyncio
    async def test_e2e_with_existing_drafted_file_loads_normally(self, tmp_path):
        """11.3: E2E mode + file present → runs without error"""
        drafted_csv = tmp_path / 'drafted.csv'
        drafted_csv.write_text('player_name,team_name\nTest Player,Sea Sharp\n')
        settings_dict = _make_settings_dict(
            e2e_test=True,
            load_drafted_data=True,
            drafted_data_path=str(drafted_csv),
        )
        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'qb': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
                await main(settings_dict)

    @pytest.mark.asyncio
    async def test_non_e2e_missing_drafted_file_raises(self, tmp_path):
        """E-2: Non-E2E mode + missing drafted data file → FileNotFoundError"""
        missing_path = str(tmp_path / 'nonexistent_drafted.csv')
        settings_dict = _make_settings_dict(
            e2e_test=False,
            load_drafted_data=True,
            drafted_data_path=missing_path,
        )
        with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
            with pytest.raises(FileNotFoundError):
                await main(settings_dict)

    def test_e2e_settings_flag_is_true(self, tmp_path):
        """E-1: e2e_test=True in settings_dict → Settings.e2e_test is True"""
        settings_dict = _make_settings_dict(
            e2e_test=True,
            drafted_data_path=str(tmp_path / 'nonexistent.csv'),
        )
        settings = create_settings_from_dict(settings_dict)
        assert settings.e2e_test is True


# ============================================================================
# Test 13.2: log level wiring
# ============================================================================

class TestLogLevelWiring:
    """Test that log_level flows correctly from settings dict through to Settings"""

    def test_log_level_from_dict_stored_in_settings(self):
        """13.2: log_level in settings dict is correctly stored in Settings"""
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            d = _make_settings_dict(log_level=level)
            settings = create_settings_from_dict(d)
            assert settings.log_level == level
