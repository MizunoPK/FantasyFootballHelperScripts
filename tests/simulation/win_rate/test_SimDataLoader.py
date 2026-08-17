import json
import shutil

import pytest
from pathlib import Path
from unittest.mock import patch

from simulation.win_rate.SimDataLoader import SimDataLoader, MIN_VALID_PLAYERS, WEEKS_REQUIRED
from simulation.win_rate.SimulatedLeague import SimulatedLeague, DRAFT_ROUNDS


def _write_position_file(week_folder, position_file, players):
    """Write a position JSON file in dict-wrapper format."""
    key = position_file.removesuffix(".json")
    (week_folder / position_file).write_text(json.dumps({key: players}))


def _make_season_folder(tmp_path, n_valid=150, add_weeks=True, add_week_01=True):
    """
    Create a mock season folder with n_valid undrafted players in every week folder.

    T73/R12: builds the COMPLETE week_01..week_18 tree SimDataLoader now requires
    (week_N+1 supplies week N's actuals, so a partial tree is invalid input). Week_01's
    contents are unchanged from the pre-T73 fixture, so the MIN_VALID_PLAYERS assertions
    keyed on n_valid are unaffected.
    """
    if not add_weeks:
        return tmp_path

    weeks = tmp_path / "weeks"
    weeks.mkdir()

    if not add_week_01:
        return tmp_path

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

    for week_num in range(1, WEEKS_REQUIRED + 1):
        week_folder = weeks / f"week_{week_num:02d}"
        week_folder.mkdir()
        _write_position_file(week_folder, "rb_data.json", players)
        for pos in ["qb_data.json", "wr_data.json", "te_data.json", "k_data.json", "dst_data.json"]:
            _write_position_file(week_folder, pos, [])

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
        expected = sum(SimulatedLeague.SELF_PLAY_TEAM_STRATEGIES.values()) * DRAFT_ROUNDS
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
        _write_position_file(weeks, "rb_data.json", players)
        for pos in ["qb_data.json", "wr_data.json", "te_data.json", "k_data.json", "dst_data.json"]:
            _write_position_file(weeks, pos, [])
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
        _write_position_file(weeks, "rb_data.json", players)
        for pos in ["qb_data.json", "wr_data.json", "te_data.json", "k_data.json", "dst_data.json"]:
            _write_position_file(weeks, pos, [])
        loader = SimDataLoader(tmp_path)
        assert loader.is_valid is False


class TestSimDataLoaderWeekCompleteness:
    """T73/R2 + R8: an incomplete week_01..week_18 tree is refused, loudly."""

    def test_missing_week_18_sets_is_valid_false(self, tmp_path):
        season = _make_season_folder(tmp_path, n_valid=150)
        shutil.rmtree(season / "weeks" / "week_18")
        loader = SimDataLoader(season)
        assert loader.is_valid is False
        assert loader.week_data_cache == {}

    def test_missing_intermediate_week_sets_is_valid_false(self, tmp_path):
        season = _make_season_folder(tmp_path, n_valid=150)
        shutil.rmtree(season / "weeks" / "week_09")
        loader = SimDataLoader(season)
        assert loader.is_valid is False
        assert loader.week_data_cache == {}

    def test_incomplete_season_logs_error_naming_season_and_weeks(self, tmp_path):
        season = _make_season_folder(tmp_path, n_valid=150)
        shutil.rmtree(season / "weeks" / "week_09")
        shutil.rmtree(season / "weeks" / "week_18")
        with patch("simulation.win_rate.SimDataLoader.get_logger") as mock_get_logger:
            loader = SimDataLoader(season)
        assert loader.is_valid is False
        messages = " ".join(
            str(call.args[0]) for call in mock_get_logger.return_value.error.call_args_list
        )
        assert season.name in messages
        assert "week_09" in messages
        assert "week_18" in messages

    def test_complete_season_caches_all_17_weeks(self, tmp_path):
        season = _make_season_folder(tmp_path, n_valid=150)
        loader = SimDataLoader(season)
        assert loader.is_valid is True
        assert sorted(loader.week_data_cache) == list(range(1, 18))


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
