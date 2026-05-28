import json
import pytest
from pathlib import Path
from unittest.mock import patch

from simulation.win_rate.SimDataLoader import SimDataLoader, MIN_VALID_PLAYERS
from simulation.win_rate.SimulatedLeague import SimulatedLeague, DRAFT_ROUNDS


def _make_season_folder(tmp_path, n_valid=150, add_weeks=True, add_week_01=True):
    """Create a mock season folder with n_valid undrafted players in week_01."""
    if not add_weeks:
        return tmp_path

    weeks = tmp_path / "weeks"
    weeks.mkdir()

    if not add_week_01:
        return tmp_path

    week_01 = weeks / "week_01"
    week_01.mkdir()

    players = [
        {
            "id": str(i + 1),
            "name": f"Player {i}",
            "position": "RB",
            "drafted_by": "",
            "locked": False,
            "projected_points": [10.0],
            "actual_points": [8.0],
        }
        for i in range(n_valid)
    ]
    (week_01 / "rb_data.json").write_text(json.dumps(players))
    for pos in ["qb_data.json", "wr_data.json", "te_data.json", "k_data.json", "dst_data.json"]:
        (week_01 / pos).write_text("[]")

    week_02 = weeks / "week_02"
    week_02.mkdir()
    (week_02 / "rb_data.json").write_text(json.dumps(players))
    for pos in ["qb_data.json", "wr_data.json", "te_data.json", "k_data.json", "dst_data.json"]:
        (week_02 / pos).write_text("[]")

    return tmp_path


class TestSimDataLoaderInit:
    def test_valid_season_sets_is_valid_true(self, tmp_path):
        season = _make_season_folder(tmp_path, n_valid=150)
        loader = SimDataLoader(season)
        assert loader.is_valid is True
        assert len(loader.week_data_cache) > 0

    def test_invalid_season_sets_is_valid_false(self, tmp_path):
        season = _make_season_folder(tmp_path, n_valid=10)
        loader = SimDataLoader(season)
        assert loader.is_valid is False

    def test_missing_week01_sets_is_valid_false(self, tmp_path):
        season = _make_season_folder(tmp_path, add_week_01=False)
        loader = SimDataLoader(season)
        assert loader.is_valid is False

    def test_no_weeks_folder_sets_is_valid_false(self, tmp_path):
        season = _make_season_folder(tmp_path, add_weeks=False)
        loader = SimDataLoader(season)
        assert loader.is_valid is False


class TestSimDataLoaderWeekDataCache:
    def test_week_data_cache_structure(self, tmp_path):
        season = _make_season_folder(tmp_path, n_valid=150)
        loader = SimDataLoader(season)
        assert 1 in loader.week_data_cache
        assert 'projected' in loader.week_data_cache[1]
        assert 'actual' in loader.week_data_cache[1]
        assert isinstance(loader.week_data_cache[1]['projected'], dict)
        assert isinstance(loader.week_data_cache[1]['actual'], dict)
        assert len(loader.week_data_cache[1]['projected']) > 0

    def test_preload_skipped_when_invalid(self, tmp_path):
        season = _make_season_folder(tmp_path, n_valid=5)
        loader = SimDataLoader(season)
        assert loader.is_valid is False
        assert loader.week_data_cache == {}

    def test_parse_players_json_malformed_json_skipped(self, tmp_path):
        season = _make_season_folder(tmp_path, n_valid=150)
        (season / "weeks" / "week_01" / "qb_data.json").write_text("INVALID JSON{{{")
        loader = SimDataLoader(season)
        assert loader.is_valid is True
        assert 1 in loader.week_data_cache
        projected = loader.week_data_cache[1]['projected']
        assert len(projected) == 150


class TestSimDataLoaderValidateSeasonData:
    def test_min_valid_players_threshold(self):
        expected = sum(SimulatedLeague.TEAM_STRATEGIES.values()) * DRAFT_ROUNDS
        assert MIN_VALID_PLAYERS == expected
        assert MIN_VALID_PLAYERS == 150

    def test_drafted_players_excluded_from_count(self, tmp_path):
        weeks = tmp_path / "weeks" / "week_01"
        weeks.mkdir(parents=True)
        players = [
            {"id": str(i), "name": f"P{i}", "position": "RB",
             "drafted_by": "team1", "locked": False,
             "projected_points": [10.0], "actual_points": [8.0]}
            for i in range(200)
        ]
        (weeks / "rb_data.json").write_text(json.dumps(players))
        for pos in ["qb_data.json", "wr_data.json", "te_data.json", "k_data.json", "dst_data.json"]:
            (weeks / pos).write_text("[]")
        loader = SimDataLoader(tmp_path)
        assert loader.is_valid is False

    def test_zero_projected_points_excluded(self, tmp_path):
        weeks = tmp_path / "weeks" / "week_01"
        weeks.mkdir(parents=True)
        players = [
            {"id": str(i), "name": f"P{i}", "position": "RB",
             "drafted_by": "", "locked": False,
             "projected_points": [0.0], "actual_points": [0.0]}
            for i in range(200)
        ]
        (weeks / "rb_data.json").write_text(json.dumps(players))
        for pos in ["qb_data.json", "wr_data.json", "te_data.json", "k_data.json", "dst_data.json"]:
            (weeks / pos).write_text("[]")
        loader = SimDataLoader(tmp_path)
        assert loader.is_valid is False


class TestSimulatedLeaguePreloadedWeekData:
    def test_preloaded_week_data_skips_file_reads(self, tmp_path):
        config_dict = {"config_name": "test", "description": "test", "parameters": {}}
        preloaded = {1: {'projected': {101: {'id': '101'}}, 'actual': {}}}
        with (
            patch.object(SimulatedLeague, '_initialize_teams'),
            patch.object(SimulatedLeague, '_generate_schedule'),
            patch.object(SimulatedLeague, '_parse_players_json') as mock_parse,
        ):
            league = SimulatedLeague(config_dict, tmp_path, preloaded_week_data=preloaded)
            mock_parse.assert_not_called()
        assert league.week_data_cache is preloaded

    def test_backward_compat_no_preloaded_data(self, tmp_path):
        config_dict = {"config_name": "test", "description": "test", "parameters": {}}
        with (
            patch.object(SimulatedLeague, '_initialize_teams'),
            patch.object(SimulatedLeague, '_generate_schedule'),
        ):
            league = SimulatedLeague(config_dict, tmp_path, preloaded_week_data=None)
        assert league.week_data_cache == {}
