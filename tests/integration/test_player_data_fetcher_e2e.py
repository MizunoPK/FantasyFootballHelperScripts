"""
E2E integration test for the player_data_fetcher pipeline in offline fixture mode.

Tests the full pipeline using ESPN fixture files -- including the manifest-backed
`league_draft` replay corpus as the ownership supplier -- exercising output
validation, drafted state, and all 6 position JSON outputs.

D17.6: the CSV ownership supplier this fixture used to drive was deleted. The run
now drives the ESPN supplier the same way every other offline test does: dummy
credentials in the process environment (`_get_raw_league_snapshot` reads them
before `_make_request` reaches its fixture branch, so they are required even
though no request leaves the machine) plus an explicit `ESPN_DRAFT_FIXTURE_STEP`.
"""
import asyncio
import json
import os
from pathlib import Path

import pytest

from player_data_fetcher.player_data_fetcher_main import main, POSITION_CODES


FIXTURES_DIR = Path(__file__).parent.parent / 'fixtures'
# Last step of the league_draft replay corpus -- the only step with completed picks
# for more than one team, so ownership is provably applied to several teams.
DRAFT_FIXTURE_STEP = 7


class TestPlayerDataFetcherE2E:
    """E2E tests for the player_data_fetcher pipeline in offline fixture mode."""

    @pytest.fixture(scope="class")
    def pipeline_output(self, tmp_path_factory):
        output_root = tmp_path_factory.mktemp("e2e_output")
        settings = {
            'e2e_test': True,
            'espn_player_limit': 100,
            'enable_game_data': False,
            'position_json_output': str(output_root / 'player_data'),
            'team_data_folder': str(output_root / 'team_data'),
            'game_data_csv': str(output_root / 'game_data.csv'),
            'enable_historical_save': False,
            'season': 2025,
            'current_nfl_week': 1,
            'request_timeout': 30,
            'rate_limit_delay': 0.0,
            'progress_frequency': 50,
            'log_level': 'WARNING',
            'logging_to_file': False,
            'scoring_format': 'ppr',
        }
        env = {
            'ESPN_FIXTURE_DIR': str(FIXTURES_DIR),
            'ESPN_DRAFT_FIXTURE_STEP': str(DRAFT_FIXTURE_STEP),
            'espn_s2': 'offline-fixture-placeholder',
            'SWID': '{OFFLINE-FIXTURE-PLACEHOLDER}',
        }
        prev = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        try:
            asyncio.run(main(settings))
        finally:
            for k, v in prev.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        return output_root / 'player_data'

    def test_pipeline_runs_to_completion(self, pipeline_output):
        """Pipeline completes without SystemExit when fixtures are present."""
        assert pipeline_output.exists()

    def test_all_position_json_files_valid(self, pipeline_output):
        """All 6 position JSON files exist, are valid JSON, have root key, have >=1 player."""
        for pos in POSITION_CODES:
            file_path = pipeline_output / f'{pos}_data.json'
            assert file_path.exists(), f"Expected {file_path} to exist"
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
            root_key = f'{pos}_data'
            assert root_key in data, f"Root key '{root_key}' not found in {file_path}"
            assert isinstance(data[root_key], list), (
                f"Expected list for '{root_key}', got {type(data[root_key])}"
            )
            assert len(data[root_key]) >= 1, (
                f"Expected >=1 player in '{root_key}', got {len(data[root_key])}"
            )

    def test_drafted_by_populated(self, pipeline_output):
        """D17.6 AC3: ownership APPLICATION survives the CSV supplier's deletion --
        the exported JSON still carries drafted_by for the replay corpus's
        completed picks."""
        all_players = []
        for pos in POSITION_CODES:
            file_path = pipeline_output / f'{pos}_data.json'
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
            all_players.extend(data.get(f'{pos}_data', []))
        assert any(p.get('drafted_by') for p in all_players), (
            "Expected at least one player with non-empty drafted_by"
        )

    def test_all_positions_represented(self, pipeline_output):
        """All 6 position codes appear in output across all position JSON files."""
        all_positions = set()
        for pos in POSITION_CODES:
            file_path = pipeline_output / f'{pos}_data.json'
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
            for player in data.get(f'{pos}_data', []):
                if player.get('position'):
                    all_positions.add(player['position'])
        assert {'QB', 'RB', 'WR', 'TE', 'K', 'DST'}.issubset(all_positions), (
            f"Expected all 6 positions but found: {all_positions}"
        )
