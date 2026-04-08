#!/usr/bin/env python3
"""
Tests for run_player_fetcher.py (KAI-10 — REQ-01, REQ-02, REQ-11–REQ-14)

Tests parse_args(), create_settings_dict(), and integration with the
player_data_fetcher_main.main() entry point.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
from unittest.mock import patch

import run_player_fetcher
from run_player_fetcher import parse_args, create_settings_dict



class TestParseArgs:
    """Test parse_args() produces correct argparse namespace"""

    def test_defaults_returned_with_no_args(self):
        """1.1: parse_args([]) returns expected defaults"""
        args = parse_args([])
        assert args.week == 17
        assert args.season == 2025
        assert args.log_level == 'INFO'
        assert args.e2e_test is False
        assert args.enable_log_file is False

    def test_log_level_debug(self):
        """1.2: --log-level DEBUG sets log_level correctly"""
        args = parse_args(['--log-level', 'DEBUG'])
        assert args.log_level == 'DEBUG'

    def test_e2e_test_flag(self):
        """1.3: --e2e-test sets e2e_test=True"""
        args = parse_args(['--e2e-test'])
        assert args.e2e_test is True

    def test_week_argument(self):
        """1.4: --week 5 sets week=5"""
        args = parse_args(['--week', '5'])
        assert args.week == 5

    def test_season_argument(self):
        """1.5: --season 2024 sets season=2024"""
        args = parse_args(['--season', '2024'])
        assert args.season == 2024

    def test_enable_historical_save_flag(self):
        """1.6: --enable-historical-save sets enable_historical_save=True"""
        args = parse_args(['--enable-historical-save'])
        assert args.enable_historical_save is True

    def test_boolean_optional_action_defaults_true(self):
        """1.7: load_drafted_data and enable_game_data default to True"""
        args = parse_args([])
        assert args.load_drafted_data is True
        assert args.enable_game_data is True

    def test_no_load_drafted_data_disables_flag(self):
        """1.8: --no-load-drafted-data sets load_drafted_data=False"""
        args = parse_args(['--no-load-drafted-data'])
        assert args.load_drafted_data is False



class TestCreateSettingsDict:
    """Test create_settings_dict() builds correct dict from argparse namespace"""

    def test_returns_dict_with_all_required_keys(self):
        """2.1: create_settings_dict(args) returns dict with all expected keys"""
        args = parse_args([])
        settings_dict = create_settings_dict(args)
        required_keys = [
            'e2e_test', 'log_level', 'logging_to_file', 'current_nfl_week',
            'season', 'my_team_name', 'load_drafted_data', 'drafted_data_path',
            'position_json_output', 'team_data_folder', 'game_data_csv',
            'enable_historical_save', 'enable_game_data', 'espn_player_limit',
            'request_timeout', 'rate_limit_delay', 'progress_frequency',
        ]
        for key in required_keys:
            assert key in settings_dict, f"Missing key: {key}"

    def test_espn_player_limit_uses_args_value_when_not_e2e(self):
        """2.2: espn_player_limit matches --espn-player-limit when not in e2e mode"""
        args = parse_args(['--espn-player-limit', '500'])
        settings_dict = create_settings_dict(args)
        assert settings_dict['espn_player_limit'] == 500



class TestRunnerIntegration:
    """Integration tests for parse_args and create_settings_dict working together"""

    def test_parse_args_and_create_settings_dict_roundtrip(self):
        """I-1: parse_args then create_settings_dict produces correct settings"""
        args = parse_args(['--week', '10', '--season', '2024'])
        settings_dict = create_settings_dict(args)
        assert settings_dict['current_nfl_week'] == 10
        assert settings_dict['season'] == 2024

    def test_debug_flag_not_present(self):
        """I-2: --debug flag is not a valid argument (SystemExit raised)"""
        with pytest.raises(SystemExit):
            parse_args(['--debug'])

    def test_all_17_args_accessible(self):
        """I-3: All 17 CLI args are accessible via parse_args"""
        args = parse_args([])
        arg_names = [
            'e2e_test', 'log_level', 'enable_log_file', 'week', 'season',
            'my_team_name', 'load_drafted_data', 'drafted_data_path',
            'position_json_output', 'team_data_folder', 'game_data_csv',
            'enable_historical_save', 'enable_game_data', 'espn_player_limit',
            'request_timeout', 'rate_limit_delay', 'progress_frequency',
        ]
        for name in arg_names:
            assert hasattr(args, name), f"Missing arg: {name}"

    def test_runner_imports_main_correctly(self):
        """I-6: run_player_fetcher module imports main from player_data_fetcher_main"""
        from run_player_fetcher import main  # noqa: F401
        assert callable(main)



class TestEdgeCases:
    """Edge case tests for parse_args and create_settings_dict"""

    def test_e2e_overrides_espn_player_limit_to_100(self):
        """E-3: --e2e-test overrides --espn-player-limit to 100 regardless of value"""
        args = parse_args(['--e2e-test', '--espn-player-limit', '500'])
        settings_dict = create_settings_dict(args)
        assert settings_dict['espn_player_limit'] == 100

    def test_negative_week_accepted(self):
        """E-4: Negative --week is accepted by argparse (no bounds check)"""
        args = parse_args(['--week', '-1'])
        assert args.week == -1

    def test_far_future_season_accepted(self):
        """E-5: Far-future --season is accepted by argparse"""
        args = parse_args(['--season', '2099'])
        assert args.season == 2099

    def test_empty_team_name_accepted(self):
        """E-6: Empty --my-team-name string is accepted"""
        args = parse_args(['--my-team-name', ''])
        assert args.my_team_name == ''

    def test_team_name_with_spaces_accepted(self):
        """E-7: Team name with spaces is accepted and stored as-is"""
        args = parse_args(['--my-team-name', 'My Fantasy Team'])
        assert args.my_team_name == 'My Fantasy Team'

    def test_rate_limit_delay_zero_accepted(self):
        """E-10: --rate-limit-delay 0 is accepted"""
        args = parse_args(['--rate-limit-delay', '0'])
        assert args.rate_limit_delay == 0.0

    def test_no_os_chdir_in_runner(self):
        """E-15: run_player_fetcher.py does not contain os.chdir"""
        runner_file = Path(__file__).parent.parent.parent / 'run_player_fetcher.py'
        content = runner_file.read_text()
        assert 'os.chdir' not in content

    def test_log_level_debug_accepted_in_args(self):
        """E-16: --log-level DEBUG is a valid choice"""
        args = parse_args(['--log-level', 'DEBUG'])
        assert args.log_level == 'DEBUG'



class TestDefaultValuesMatchOldConfig:
    """Verify default argument values match old config.py constants (backward compat)"""

    def test_default_week_matches_old_config(self):
        """C-1: Default --week == 17 (old CURRENT_NFL_WEEK)"""
        args = parse_args([])
        assert args.week == 17

    def test_default_season_matches_old_config(self):
        """C-2: Default --season == 2025 (old NFL_SEASON)"""
        args = parse_args([])
        assert args.season == 2025

    def test_default_espn_player_limit_matches_old_config(self):
        """C-3: Default --espn-player-limit == 2000 (old ESPN_PLAYER_LIMIT)"""
        args = parse_args([])
        assert args.espn_player_limit == 2000

    def test_default_request_timeout_matches_old_config(self):
        """C-4: Default --request-timeout == 30 (old REQUEST_TIMEOUT)"""
        args = parse_args([])
        assert args.request_timeout == 30

    def test_default_rate_limit_delay_matches_old_config(self):
        """C-5: Default --rate-limit-delay == 0.2 (old RATE_LIMIT_DELAY)"""
        args = parse_args([])
        assert args.rate_limit_delay == 0.2

    def test_default_progress_frequency_matches_old_config(self):
        """C-6: Default --progress-frequency == 10 (old PROGRESS_UPDATE_FREQUENCY)"""
        args = parse_args([])
        assert args.progress_frequency == 10



class TestE2EAndLogLevel:
    """Tests for E2E mode, absent debug flag, and log level handling"""

    def test_e2e_mode_sets_player_limit_to_100(self):
        """11.1: E2E mode always sets espn_player_limit to 100"""
        args = parse_args(['--e2e-test'])
        settings_dict = create_settings_dict(args)
        assert settings_dict['espn_player_limit'] == 100

    def test_no_debug_flag_raises_system_exit(self):
        """12.1: --debug flag is absent; attempting it causes SystemExit"""
        with pytest.raises(SystemExit):
            parse_args(['--debug'])

    def test_log_level_choices_are_valid(self):
        """13.1: --log-level accepts all valid choices; rejects invalid ones"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        for level in valid_levels:
            args = parse_args(['--log-level', level])
            assert args.log_level == level

        with pytest.raises(SystemExit):
            parse_args(['--log-level', 'VERBOSE'])


