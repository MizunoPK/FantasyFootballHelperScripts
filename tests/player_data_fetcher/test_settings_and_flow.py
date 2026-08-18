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



def _make_settings_dict(tmp_path, **overrides):
    """Build a minimal valid settings dict rooted at tmp_path, with all required keys."""
    base = {
        'e2e_test': False,
        'log_level': 'INFO',
        'logging_to_file': False,
        'current_nfl_week': 17,
        'season': 2025,
        'my_team_name': 'Sea Sharp',
        'load_drafted_data': False,
        'drafted_data_path': str(tmp_path / 'drafted_data.csv'),
        'position_json_output': str(tmp_path / 'player_data'),
        'team_data_folder': str(tmp_path / 'team_data'),
        'game_data_csv': str(tmp_path / 'game_data.csv'),
        'enable_historical_save': False,
        'enable_game_data': False,
        'espn_player_limit': 100,
        'request_timeout': 30,
        'rate_limit_delay': 0.2,
        'progress_frequency': 10,
        'scoring_format': 'ppr',
        'use_csv_ownership': True,
    }
    base.update(overrides)
    return base



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

    def test_create_settings_from_dict_maps_current_nfl_week(self, tmp_path):
        """3.4: create_settings_from_dict maps dict 'current_nfl_week' to Settings field"""
        d = _make_settings_dict(tmp_path, current_nfl_week=10)
        settings = create_settings_from_dict(d)
        assert settings.current_nfl_week == 10

    def test_create_settings_from_dict_with_multiple_fields(self, tmp_path):
        """3.5: create_settings_from_dict correctly maps all provided fields"""
        d = _make_settings_dict(tmp_path, season=2023, current_nfl_week=5, log_level='DEBUG')
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



class TestMainSignature:
    """Test main() function signature and integration with settings"""

    @pytest.mark.asyncio
    async def test_main_accepts_settings_dict(self, tmp_path):
        """I-4: main(settings_dict) builds Settings from dict and runs"""
        settings_dict = _make_settings_dict(tmp_path)
        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'season': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_collector.exporter.load_espn_attribution = AsyncMock(return_value=None)
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
                with patch('player_data_fetcher.player_data_fetcher_main.validate_output_files'):
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

    def test_log_level_passed_through_to_settings(self, tmp_path):
        """I-14: log_level from settings dict is stored in Settings"""
        d = _make_settings_dict(tmp_path, log_level='WARNING')
        settings = create_settings_from_dict(d)
        assert settings.log_level == 'WARNING'



class TestSettingsEdgeCases:
    """Edge case tests for Settings construction"""

    def test_extra_keys_in_dict_do_not_cause_error(self, tmp_path):
        """E-8: Extra keys in args_dict are ignored (not accessed by create_settings_from_dict)"""
        d = _make_settings_dict(tmp_path)
        d['completely_unknown_key'] = 'surprise_value'
        settings = create_settings_from_dict(d)
        assert settings.season == d['season']

    def test_env_var_no_longer_overrides_settings(self):
        """E-9: NFL_PROJ_* env vars no longer override settings (pydantic removed)"""
        with patch.dict(os.environ, {'NFL_PROJ_SEASON': '1999'}):
            settings = Settings()
            assert settings.season != 1999

    def test_week_to_current_nfl_week_mapping(self, tmp_path):
        """E-19: Runner's --week arg maps to 'current_nfl_week' in dict → Settings.current_nfl_week"""
        d = _make_settings_dict(tmp_path, current_nfl_week=7)
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



class TestE2EGracefulSkip:
    """Test E2E graceful skip for missing drafted data file"""

    @pytest.mark.asyncio
    async def test_e2e_missing_drafted_file_no_exception(self, tmp_path):
        """11.2 / E-1: E2E mode + missing drafted data file → no FileNotFoundError"""
        missing_path = str(tmp_path / 'nonexistent_drafted.csv')
        settings_dict = _make_settings_dict(
            tmp_path,
            e2e_test=True,
            load_drafted_data=True,
            drafted_data_path=missing_path,
        )
        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'season': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_collector.exporter.load_espn_attribution = AsyncMock(return_value=None)
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
                with patch('player_data_fetcher.player_data_fetcher_main.validate_output_files'):
                    await main(settings_dict)

    @pytest.mark.asyncio
    async def test_e2e_with_existing_drafted_file_loads_normally(self, tmp_path):
        """11.3: E2E mode + file present → runs without error"""
        drafted_csv = tmp_path / 'drafted.csv'
        drafted_csv.write_text('player_name,team_name\nTest Player,Sea Sharp\n')
        settings_dict = _make_settings_dict(
            tmp_path,
            e2e_test=True,
            load_drafted_data=True,
            drafted_data_path=str(drafted_csv),
        )
        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'season': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_collector.exporter.load_espn_attribution = AsyncMock(return_value=None)
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
                with patch('player_data_fetcher.player_data_fetcher_main.validate_output_files'):
                    await main(settings_dict)

    @pytest.mark.asyncio
    async def test_non_e2e_missing_drafted_file_raises(self, tmp_path):
        """E-2: Non-E2E mode + missing drafted data file → FileNotFoundError"""
        missing_path = str(tmp_path / 'nonexistent_drafted.csv')
        settings_dict = _make_settings_dict(
            tmp_path,
            e2e_test=False,
            load_drafted_data=True,
            drafted_data_path=missing_path,
        )
        with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
            with pytest.raises(FileNotFoundError):
                await main(settings_dict)

    @pytest.mark.asyncio
    async def test_default_espn_path_does_not_require_the_drafted_csv(self, tmp_path):
        """D17.5 review BLOCKING-2: on the DEFAULT (ESPN) path a missing
        drafted_data.csv must NOT abort the run.

        The whole-run precondition used to be gated on `load_drafted_data` alone.
        That was a correct proxy before the cutover -- the CSV was the only
        ownership source. After the flip the default path never opens the CSV, so
        gating on that flag alone made the shipped default
        (`python run_player_fetcher.py`, no flags) raise FileNotFoundError before
        any fetch, against a file it does not need. Reverting the `and
        settings.use_csv_ownership` clause turns this test red.
        """
        missing_path = str(tmp_path / 'nonexistent_drafted.csv')
        settings_dict = _make_settings_dict(
            tmp_path,
            e2e_test=False,
            load_drafted_data=True,       # the default
            use_csv_ownership=False,      # the NEW default -- CSV is not the supplier
            drafted_data_path=missing_path,
        )
        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'season': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_collector.exporter.load_espn_attribution = AsyncMock(return_value=None)
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
                with patch('player_data_fetcher.player_data_fetcher_main.validate_output_files'):
                    # Must reach the fetch, not raise on the absent CSV.
                    await main(settings_dict)
        mock_collector.collect_all_projections.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_e2e_skips_the_authenticated_league_read_without_a_fixture_dir(self, tmp_path, monkeypatch):
        """D17.5 review GAP-1: --e2e-test must not make a LIVE authenticated call.

        Before the cutover, e2e mode only had to excuse a missing drafted_data.csv.
        After the flip the flag inherits the ESPN supplier by default, so without the
        skip arm an e2e run performs a live authenticated league read -- turning the
        project's offline-graceful mode into one requiring credentials and network.
        Removing the `settings.e2e_test and not settings.use_csv_ownership and not
        ESPN_FIXTURE_DIR` arm turns this test red.
        """
        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        settings_dict = _make_settings_dict(
            tmp_path,
            e2e_test=True,
            load_drafted_data=True,
            use_csv_ownership=False,      # what --e2e-test actually yields post-cutover
            drafted_data_path=str(tmp_path / 'nonexistent_drafted.csv'),
        )
        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'season': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_collector.exporter.load_espn_attribution = AsyncMock(return_value=None)
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.setup_logger'):
                with patch('player_data_fetcher.player_data_fetcher_main.validate_output_files'):
                    await main(settings_dict)
        # The authenticated read must NOT have been attempted.
        mock_collector.exporter.load_espn_attribution.assert_not_awaited()
        mock_collector.collect_all_projections.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_absent_credentials_degrade_to_empty_attribution_with_one_warning(
        self, tmp_path, monkeypatch, caplog
    ):
        """D17.7 D1: no credentials -> public fetch succeeds, ownership degrades.

        Before this unit a credential-free checkout could not fetch player data at
        all: main() awaited load_espn_attribution unconditionally, which reached
        get_espn_credentials() and raised ConfigurationError before any export --
        even though the public projections endpoint needs no credentials and the
        run had not asked for ownership.

        Removing the `except ConfigurationError` arm turns this red.
        """
        import logging
        from player_data_fetcher.player_data_fetcher_main import LOG_NAME
        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)
        from player_data_fetcher.player_data_exporter import DataExporter
        from player_data_fetcher.player_data_models import ESPNPlayerData

        settings_dict = _make_settings_dict(tmp_path, e2e_test=False)
        # Mirror production construction: main() passes the Settings object itself
        # as espn_settings (player_data_fetcher_main.py:181). A bare DataExporter
        # trips the espn_settings guard before the credential read is ever reached.
        real_exporter = DataExporter(
            output_dir=str(tmp_path),
            espn_settings=create_settings_from_dict(settings_dict),
        )

        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'season': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_collector.exporter = real_exporter
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.validate_output_files'):
                # `setup_logger` CLEARS handlers on the logger it returns, so a
                # handler attached beforehand is wiped by main() itself; and
                # LoggingManager sets propagate=False, so caplog's root handler
                # never sees the record either. Hand main() a logger we control.
                captured = logging.getLogger("d17_7_degradation_capture")
                captured.handlers.clear()
                captured.addHandler(caplog.handler)
                captured.setLevel(logging.WARNING)
                captured.propagate = False
                with patch(
                    'player_data_fetcher.player_data_fetcher_main.setup_logger',
                    return_value=captured,
                ):
                    await main(settings_dict)

        # loaded-but-empty, NOT the never-loaded sentinel
        assert real_exporter._espn_attribution == {}
        assert real_exporter._espn_attribution is not None

        hits = [r for r in caplog.records if "LEAGUE OWNERSHIP UNAVAILABLE" in r.getMessage()]
        assert len(hits) == 1, f"expected exactly one degradation warning, got {len(hits)}"
        msg = hits[0].getMessage()
        assert "espn_s2" in msg and "SWID" in msg      # names what to set
        assert "REDACTED" not in msg                    # nothing to redact: no values present

        # and a real export path now works
        data = ProjectionData(season=2025, scoring_format="ppr", total_players=1, players=[
            ESPNPlayerData(id="101", name="Test Player", team="KC", position="WR"),
        ])
        players = real_exporter.get_fantasy_players(data)
        assert players[0].drafted_by == ""

    @pytest.mark.asyncio
    async def test_invalid_credentials_still_raise_and_do_not_degrade(self, tmp_path, monkeypatch):
        """D17.7 D3: ABSENT credentials degrade; INVALID ones must NOT.

        This is the guard against the degradation swallowing a real auth failure.
        Widening the catch to `except Exception` turns this red -- which is the
        whole point: a wrong or expired cookie must surface, not silently yield an
        unowned board.
        """
        from player_data_fetcher.espn_client import ESPNAPIError
        from player_data_fetcher.player_data_exporter import DataExporter

        monkeypatch.setenv("espn_s2", "present-but-rejected")
        monkeypatch.setenv("SWID", "{present-but-rejected}")

        real_exporter = DataExporter(output_dir=str(tmp_path))
        real_exporter.load_espn_attribution = AsyncMock(
            side_effect=ESPNAPIError("401 Unauthorized")
        )
        settings_dict = _make_settings_dict(tmp_path, e2e_test=False)

        with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
            mock_collector = MagicMock()
            mock_collector.collect_all_projections = AsyncMock(return_value={
                'season': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
            })
            mock_collector.export_data = AsyncMock(return_value=[])
            mock_collector.exporter = real_exporter
            mock_cls.return_value = mock_collector
            with patch('player_data_fetcher.player_data_fetcher_main.validate_output_files'):
                with pytest.raises(ESPNAPIError):
                    await main(settings_dict)

        # it must NOT have been degraded into an empty board
        assert real_exporter._espn_attribution is None

    @pytest.mark.asyncio
    async def test_degraded_path_makes_no_authenticated_call(self, tmp_path, monkeypatch):
        """D17.7: assert MECHANISM -- the league read is never attempted.

        Output-shaped assertions cannot tell 'we skipped the call' from 'we made
        the call and it returned nothing', which is this ticket's defining defect
        class. This pins the call itself.
        """
        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)
        from player_data_fetcher.player_data_exporter import DataExporter

        settings_dict = _make_settings_dict(tmp_path, e2e_test=False)
        real_exporter = DataExporter(
            output_dir=str(tmp_path),
            espn_settings=create_settings_from_dict(settings_dict),
        )

        # NOTE: `get_league_snapshot` IS entered on the degraded path -- the
        # credential read lives inside it (`_get_raw_league_snapshot`) and is what
        # raises. The meaningful mechanism assertion is therefore that no HTTP
        # request is ever issued: credentials are checked before the request is
        # built, so a credential-free run makes no authenticated call.
        with patch('player_data_fetcher.espn_client.ESPNClient._make_request') as mock_read:
            with patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector') as mock_cls:
                mock_collector = MagicMock()
                mock_collector.collect_all_projections = AsyncMock(return_value={
                    'season': ProjectionData(season=2025, scoring_format='ppr', total_players=200, players=[])
                })
                mock_collector.export_data = AsyncMock(return_value=[])
                mock_collector.exporter = real_exporter
                mock_cls.return_value = mock_collector
                with patch('player_data_fetcher.player_data_fetcher_main.validate_output_files'):
                    await main(settings_dict)

        mock_read.assert_not_called()

    def test_e2e_settings_flag_is_true(self, tmp_path):
        """E-1: e2e_test=True in settings_dict → Settings.e2e_test is True"""
        settings_dict = _make_settings_dict(
            tmp_path,
            e2e_test=True,
            drafted_data_path=str(tmp_path / 'nonexistent.csv'),
        )
        settings = create_settings_from_dict(settings_dict)
        assert settings.e2e_test is True



class TestLogLevelWiring:
    """Test that log_level flows correctly from settings dict through to Settings"""

    def test_log_level_from_dict_stored_in_settings(self, tmp_path):
        """13.2: log_level in settings dict is correctly stored in Settings"""
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            d = _make_settings_dict(tmp_path, log_level=level)
            settings = create_settings_from_dict(d)
            assert settings.log_level == level


class TestSettingsDataRootSeam:
    """T91: Settings' path defaults resolve PER INSTANCE, not at class-definition time"""

    def test_settings_defaults_redirect_under_player_data_dir(self, monkeypatch, tmp_path):
        """T91-10 (AC2): PLAYER_DATA_DIR redirects every Settings path default"""
        root = tmp_path / 'fetcher_root'
        monkeypatch.setenv('PLAYER_DATA_DIR', str(root))

        settings = Settings()

        assert settings.position_json_output == str(root / 'player_data')
        assert settings.team_data_folder == str(root / 'team_data')
        assert settings.game_data_csv == str(root / 'game_data.csv')
        assert settings.drafted_data_path == str(root / 'drafted_data.csv')

    def test_settings_defaults_are_repo_anchored_when_unset(self, monkeypatch):
        """T91-11 (AC3): unset, Settings' defaults are byte-identical to today's"""
        from pathlib import Path as _Path

        monkeypatch.delenv('PLAYER_DATA_DIR', raising=False)
        repo_data = _Path(__file__).parent.parent.parent / 'data'

        settings = Settings()

        assert settings.position_json_output == str(repo_data / 'player_data')
        assert settings.team_data_folder == str(repo_data / 'team_data')
        assert settings.game_data_csv == str(repo_data / 'game_data.csv')
        assert settings.drafted_data_path == str(repo_data / 'drafted_data.csv')

    def test_settings_resolves_per_instance_not_at_class_definition(self, monkeypatch, tmp_path):
        """T91-12 (AC4): two Settings() built under different PLAYER_DATA_DIR values differ.

        A dataclass field with a class-level `= str(...)` default is evaluated
        ONCE at class-definition time -- the same silent no-op as a def-time
        function default. field(default_factory=...) runs per instance, which is
        what this asserts. A regression to the class-level form fails here.
        """
        monkeypatch.setenv('PLAYER_DATA_DIR', str(tmp_path / 'first'))
        first = Settings()

        monkeypatch.setenv('PLAYER_DATA_DIR', str(tmp_path / 'second'))
        second = Settings()

        assert first.position_json_output == str(tmp_path / 'first' / 'player_data')
        assert second.position_json_output == str(tmp_path / 'second' / 'player_data')
        assert first.position_json_output != second.position_json_output

    def test_settings_explicit_paths_still_win(self, monkeypatch, tmp_path):
        """T91-13: an explicitly constructed Settings path beats the seam"""
        monkeypatch.setenv('PLAYER_DATA_DIR', str(tmp_path / 'fetcher_root'))
        explicit = str(tmp_path / 'explicit' / 'player_data')

        settings = Settings(position_json_output=explicit)

        assert settings.position_json_output == explicit


