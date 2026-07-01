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
import logging
from pathlib import Path
from unittest.mock import Mock, patch

# Third-party
import pytest

# Local
from simulation.win_rate.CombinationEvaluator import CombinationEvaluator
from utils.error_handler import FileOperationError

MODULE = "simulation.win_rate.CombinationEvaluator"


def _fake_params():
    """A league_config-like parameters dict (the 6 params nested + other keys)."""
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
    # Initialize counter attributes (KDD-1) for compatibility with evaluate()'s counter-reading
    mock_runner.last_dropped_count = 0
    mock_runner.last_requested_count = num_sims

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

    def test_naive_opponents_threads_to_runner(self, tmp_path):
        """naive_opponents passed to the evaluator reaches ParallelLeagueRunner (D2)."""
        (tmp_path / "2021").mkdir()
        with patch(f"{MODULE}.ConfigManager") as MockCM, \
             patch(f"{MODULE}.SimDataLoader") as MockLoader, \
             patch(f"{MODULE}.ParallelLeagueRunner") as MockRunner:
            MockCM.return_value.config_name = "test"
            MockCM.return_value.description = "test"
            MockCM.return_value.parameters = _fake_params()
            MockLoader.return_value.is_valid = True
            MockLoader.return_value.week_data_cache = {1: {}}
            CombinationEvaluator(tmp_path, num_simulations=10, naive_opponents=True)

        assert MockRunner.call_args.kwargs["naive_opponents"] is True

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
             patch(f"{MODULE}.get_logger") as mock_get_logger:
            mock_logger = mock_get_logger.return_value
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

    def test_evaluate_surfaces_dropped_leagues_across_seasons(self, tmp_path, caplog):
        """A dropped league per season is aggregated, logged at ERROR, and total_games is reduced."""
        with patch(f"{MODULE}.get_logger") as mock_get_logger:
            test_logger = logging.getLogger('test_evaluator')
            mock_get_logger.return_value = test_logger

            # One drop per season with one survivor: requested=2, completed=1, dropped=1
            # (survivor-results length + dropped == requested, matching the real runner
            # contract where dropped = requested - len(results)).
            ev, mock_runner = _make_evaluator(tmp_path, [(10, 7, 1.0)], num_seasons=2, num_sims=2)
            mock_runner.last_dropped_count = 1
            mock_runner.last_requested_count = 2

            with caplog.at_level(logging.ERROR, logger='test_evaluator'):
                wins, games, win_rate = ev.evaluate([{"RB": "P"}], _valid_param_values())

            # Survivor results are unchanged ([(10, 7, 1.0)] per season x 2 seasons).
            assert wins == 20
            assert games == 34
            # Aggregated drop ERROR surfaced once (2 seasons x 1 drop = 2 of 4 requested).
            assert any(
                record.levelno == logging.ERROR
                and "evaluate dropped 2/4 leagues" in record.getMessage()
                for record in caplog.records
            )

    def test_evaluate_no_drop_error_when_all_complete(self, tmp_path, caplog):
        """Zero drops -> no evaluate-level ERROR is logged."""
        with patch(f"{MODULE}.get_logger") as mock_get_logger:
            test_logger = logging.getLogger('test_evaluator')
            mock_get_logger.return_value = test_logger

            # All complete: one survivor, requested=1, dropped=0 (survivor-results length
            # == requested, matching the real runner contract).
            ev, mock_runner = _make_evaluator(tmp_path, [(10, 7, 1.0)], num_seasons=2, num_sims=1)
            mock_runner.last_dropped_count = 0
            mock_runner.last_requested_count = 1

            with caplog.at_level(logging.ERROR, logger='test_evaluator'):
                ev.evaluate([{"RB": "P"}], _valid_param_values())

            assert not any(
                "evaluate dropped" in record.getMessage() for record in caplog.records
            )
