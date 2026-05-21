"""
E2E integration test for the player_data_fetcher pipeline in offline fixture mode.

Tests the full pipeline using ESPN fixture files and the drafted_data fixture,
exercising output validation, drafted state, and all 6 position JSON outputs.
"""
import asyncio
import json
from pathlib import Path

from player_data_fetcher.player_data_fetcher_main import main


FIXTURES_DIR = Path(__file__).parent.parent / 'fixtures'


class TestPlayerDataFetcherE2E:
    """E2E tests for the player_data_fetcher pipeline in offline fixture mode."""

    def _make_settings_dict(self, tmp_path: Path) -> dict:
        return {
            'e2e_test': True,
            'espn_player_limit': 100,
            'enable_game_data': False,
            'position_json_output': str(tmp_path / 'player_data'),
            'team_data_folder': str(tmp_path / 'team_data'),
            'game_data_csv': str(tmp_path / 'game_data.csv'),
            'enable_historical_save': False,
            'load_drafted_data': True,
            'drafted_data_path': str(FIXTURES_DIR / 'league' / 'drafted_data.csv'),
            'my_team_name': 'Sea Sharp',
            'season': 2025,
            'current_nfl_week': 1,
            'request_timeout': 30,
            'rate_limit_delay': 0.0,
            'progress_frequency': 50,
            'log_level': 'WARNING',
            'logging_to_file': False,
            'scoring_format': 'ppr',
        }

    def test_pipeline_runs_to_completion(self, tmp_path, monkeypatch):
        """R3: Pipeline completes without SystemExit when fixtures are present."""
        monkeypatch.setenv('ESPN_FIXTURE_DIR', str(FIXTURES_DIR))
        asyncio.run(main(self._make_settings_dict(tmp_path)))

    def test_all_position_json_files_valid(self, tmp_path, monkeypatch):
        """R4: All 6 position JSON files exist, are valid JSON, have root key, have >=1 player."""
        monkeypatch.setenv('ESPN_FIXTURE_DIR', str(FIXTURES_DIR))
        asyncio.run(main(self._make_settings_dict(tmp_path)))

        output_dir = tmp_path / 'player_data'
        for pos in ['qb', 'rb', 'wr', 'te', 'k', 'dst']:
            file_path = output_dir / f'{pos}_data.json'
            assert file_path.exists(), f"Expected {file_path} to exist"
            with open(file_path) as f:
                data = json.load(f)
            root_key = f'{pos}_data'
            assert root_key in data, f"Root key '{root_key}' not found in {file_path}"
            assert len(data[root_key]) >= 1, (
                f"Expected >=1 player in '{root_key}', got {len(data[root_key])}"
            )

    def test_drafted_by_populated(self, tmp_path, monkeypatch):
        """R5: At least one player has non-empty drafted_by when fixture drafted data loaded."""
        monkeypatch.setenv('ESPN_FIXTURE_DIR', str(FIXTURES_DIR))
        asyncio.run(main(self._make_settings_dict(tmp_path)))

        output_dir = tmp_path / 'player_data'
        all_players = []
        for pos in ['qb', 'rb', 'wr', 'te', 'k', 'dst']:
            file_path = output_dir / f'{pos}_data.json'
            with open(file_path) as f:
                data = json.load(f)
            all_players.extend(data.get(f'{pos}_data', []))

        assert any(p.get('drafted_by') for p in all_players), (
            "Expected at least one player with non-empty drafted_by"
        )

    def test_all_positions_represented(self, tmp_path, monkeypatch):
        """R6: All 6 position codes appear in output across all position JSON files."""
        monkeypatch.setenv('ESPN_FIXTURE_DIR', str(FIXTURES_DIR))
        asyncio.run(main(self._make_settings_dict(tmp_path)))

        output_dir = tmp_path / 'player_data'
        all_positions = set()
        for pos in ['qb', 'rb', 'wr', 'te', 'k', 'dst']:
            file_path = output_dir / f'{pos}_data.json'
            with open(file_path) as f:
                data = json.load(f)
            for player in data.get(f'{pos}_data', []):
                if player.get('position'):
                    all_positions.add(player['position'])

        assert {'QB', 'RB', 'WR', 'TE', 'K', 'DST'}.issubset(all_positions), (
            f"Expected all 6 positions but found: {all_positions}"
        )
