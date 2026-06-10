"""
Tests for simulation.win_rate.CombinationEvaluator.

The evaluator's value-add is orchestration + aggregation; real simulation
correctness is covered by test_ParallelLeagueRunner / test_SimulatedLeague. These
tests patch ConfigManager / SimDataLoader / ParallelLeagueRunner at the usage site
and mock run_simulations_for_config to return canned (wins, losses, points) tuples.

Author: Kai Mizuno
"""

# Standard library
import copy
from pathlib import Path
from unittest.mock import Mock, patch

# Third-party
import pytest

# Local
from simulation.win_rate.CombinationEvaluator import CombinationEvaluator
from utils.error_handler import FileOperationError

MODULE = "simulation.win_rate.CombinationEvaluator"


def _fake_params():
    """A league_config-like parameters dict (the 7 params nested + other keys)."""
    return {
        "CURRENT_NFL_WEEK": 17,
        "NFL_SEASON": 2025,
        "SAME_POS_BYE_WEIGHT": 0.07,
        "DIFF_POS_BYE_WEIGHT": 0.01,
        "DRAFT_ORDER_BONUSES": {"PRIMARY": 67, "SECONDARY": 69},
        "DRAFT_ORDER": [{"QB": "P"}],
        "MAX_POSITIONS": {"QB": 2},
        "ADP_SCORING": {"THRESHOLDS": {"STEPS": 25}, "WEIGHT": 4.76},
        "PLAYER_RATING_SCORING": {"THRESHOLDS": {"STEPS": 20}, "WEIGHT": 3.52},
        "DRAFT_NORMALIZATION_MAX_SCALE": 150,
    }


def _valid_param_values():
    return {
        "DRAFT_NORMALIZATION_MAX_SCALE": 160,
        "SAME_POS_BYE_WEIGHT": 0.10,
        "DIFF_POS_BYE_WEIGHT": 0.05,
        "PRIMARY_BONUS": 80,
        "SECONDARY_BONUS": 60,
        "ADP_SCORING_WEIGHT": 5.0,
        "PLAYER_RATING_SCORING_WEIGHT": 3.0,
    }


def _make_evaluator(tmp_path, per_season_results, num_seasons=2, num_sims=10, valid=True):
    """Construct a CombinationEvaluator with patched deps; return (evaluator, mock_runner)."""
    for i in range(num_seasons):
        (tmp_path / f"202{i + 1}").mkdir()

    mock_runner = Mock()
    mock_runner.run_simulations_for_config.return_value = per_season_results

    with patch(f"{MODULE}.ConfigManager") as MockCM, \
         patch(f"{MODULE}.SimDataLoader") as MockLoader, \
         patch(f"{MODULE}.ParallelLeagueRunner", return_value=mock_runner):
        MockCM.return_value.config_name = "test"
        MockCM.return_value.description = "test"
        MockCM.return_value.parameters = _fake_params()
        MockLoader.return_value.is_valid = valid
        MockLoader.return_value.week_data_cache = {1: {}}
        ev = CombinationEvaluator(tmp_path, num_simulations=num_sims)

    return ev, mock_runner


class TestCombinationEvaluator:
    """Tests for CombinationEvaluator."""

    def test_evaluate_aggregates_wins_and_games_across_seasons(self, tmp_path):
        ev, _ = _make_evaluator(tmp_path, [(10, 7, 1.0), (12, 5, 2.0)], num_seasons=2)
        wins, games, win_rate = ev.evaluate([{"RB": "P"}], _valid_param_values())
        # per season: wins 22, losses 12; x2 seasons -> wins 44, losses 24
        assert wins == 44
        assert games == 68
        assert win_rate == pytest.approx(44 / 68)

    def test_evaluate_win_rate_math(self, tmp_path):
        ev, _ = _make_evaluator(tmp_path, [(3, 1, 0.0)], num_seasons=1)
        wins, games, win_rate = ev.evaluate([{"RB": "P"}], _valid_param_values())
        assert (wins, games) == (3, 4)
        assert win_rate == pytest.approx(0.75)

    def test_evaluate_win_rate_zero_when_no_games(self, tmp_path):
        ev, _ = _make_evaluator(tmp_path, [(0, 0, 0.0)], num_seasons=2)
        wins, games, win_rate = ev.evaluate([{"RB": "P"}], _valid_param_values())
        assert wins == 0
        assert games == 0
        assert win_rate == 0.0

    def test_evaluate_applies_overrides_to_config(self, tmp_path):
        ev, mock_runner = _make_evaluator(tmp_path, [(1, 1, 0.0)], num_seasons=1)
        draft_order = [{"RB": "P"}, {"WR": "S"}]
        ev.evaluate(draft_order, _valid_param_values())

        config = mock_runner.run_simulations_for_config.call_args.args[0]
        params = config["parameters"]
        assert params["DRAFT_ORDER"] == draft_order
        assert params["DRAFT_ORDER_BONUSES"]["PRIMARY"] == 80
        assert params["ADP_SCORING"]["WEIGHT"] == 5.0
        assert params["PLAYER_RATING_SCORING"]["WEIGHT"] == 3.0
        assert params["DRAFT_NORMALIZATION_MAX_SCALE"] == 160

    def test_evaluate_runs_all_seasons(self, tmp_path):
        ev, mock_runner = _make_evaluator(tmp_path, [(1, 1, 0.0)], num_seasons=3)
        ev.evaluate([{"RB": "P"}], _valid_param_values())
        assert mock_runner.set_data_folder.call_count == 3
        assert mock_runner.run_simulations_for_config.call_count == 3

    def test_evaluate_does_not_mutate_base_config(self, tmp_path):
        ev, _ = _make_evaluator(tmp_path, [(1, 1, 0.0)], num_seasons=1)
        before = copy.deepcopy(ev._base_config)
        ev.evaluate([{"RB": "P"}], _valid_param_values())
        assert ev._base_config == before

    def test_init_raises_when_no_seasons(self, tmp_path):
        mock_runner = Mock()
        with patch(f"{MODULE}.ConfigManager") as MockCM, \
             patch(f"{MODULE}.ParallelLeagueRunner", return_value=mock_runner):
            MockCM.return_value.config_name = "test"
            MockCM.return_value.description = "test"
            MockCM.return_value.parameters = _fake_params()
            with pytest.raises(FileNotFoundError):
                CombinationEvaluator(tmp_path, num_simulations=10)  # no 20XX/ dirs

    def test_init_warns_when_no_valid_seasons(self, tmp_path):
        (tmp_path / "2021").mkdir()
        mock_runner = Mock()
        with patch(f"{MODULE}.ConfigManager") as MockCM, \
             patch(f"{MODULE}.SimDataLoader") as MockLoader, \
             patch(f"{MODULE}.ParallelLeagueRunner", return_value=mock_runner), \
             patch(f"{MODULE}.logger") as mock_logger:
            MockCM.return_value.config_name = "test"
            MockCM.return_value.description = "test"
            MockCM.return_value.parameters = _fake_params()
            MockLoader.return_value.is_valid = False  # season exists but invalid
            MockLoader.return_value.week_data_cache = {}
            ev = CombinationEvaluator(tmp_path, num_simulations=10)

        assert ev._season_cache == {}
        assert mock_logger.warning.called

    def test_base_config_returns_independent_deepcopy(self, tmp_path):
        ev, _ = _make_evaluator(tmp_path, [(1, 1, 0.0)], num_seasons=1)
        cfg = ev.base_config
        assert cfg == ev._base_config
        cfg["parameters"]["SAME_POS_BYE_WEIGHT"] = 999  # mutate the returned copy
        assert ev._base_config["parameters"]["SAME_POS_BYE_WEIGHT"] != 999  # internal unaffected
