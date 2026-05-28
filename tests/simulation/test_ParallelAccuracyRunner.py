"""
Tests for ParallelAccuracyRunner module-level function _evaluate_config_tournament_process().

Implements spec.md R3: unit test for _evaluate_config_tournament_process() directly callable
without class instantiation. Implements spec.md R4: fixture helper duplicated in this file
(named create_mock_historical_season_f05() with _f05 suffix to avoid collision).

Author: Secondary-D for FF-5-accuracy_sim_improvements
"""

import json
import pytest
from pathlib import Path

from simulation.accuracy.ParallelAccuracyRunner import _evaluate_config_tournament_process
from simulation.accuracy.AccuracyCalculator import AccuracyResult

project_root = Path(__file__).parent.parent.parent


def create_mock_historical_season_f05(data_folder: Path, year: str = "2024") -> None:
    """Create a mock historical season folder structure for F05 unit testing.

    Implements spec.md R4: duplicated fixture helper pattern from
    tests/integration/test_accuracy_simulation_integration.py create_mock_historical_season().
    Named with _f05 suffix to avoid naming collision.

    Args:
        data_folder: Root folder for sim_data (season folder created inside).
        year: Season year string (e.g., "2024").
    """
    season_folder = data_folder / year
    season_folder.mkdir(parents=True, exist_ok=True)

    (season_folder / "season_schedule.csv").write_text(
        "week,team,opponent\n"
        "1,KC,DET\n"
        "1,DET,KC\n"
        "2,KC,JAX\n"
        "2,JAX,KC\n"
    )
    (season_folder / "game_data.csv").write_text(
        "week,home_team,away_team,temperature,wind_speed,location\n"
        "1,KC,DET,72,5,HOME\n"
        "2,KC,JAX,68,8,AWAY\n"
    )

    team_data_folder = season_folder / "team_data"
    team_data_folder.mkdir(exist_ok=True)
    (team_data_folder / "teams_week_1.csv").write_text(
        "team,offensive_rank,defensive_rank\n"
        "KC,1,5\n"
        "DET,3,10\n"
        "MIN,5,8\n"
    )

    weeks_folder = season_folder / "weeks"
    weeks_folder.mkdir(exist_ok=True)

    def _build_week_points(base_points: float, week_num: int, is_projected: bool = False) -> list:
        points = []
        for w in range(1, 18):
            week_points = base_points + (w * 0.5) - 5
            if is_projected:
                week_points -= 1.0
            points.append(round(week_points, 1))
        return points

    for week_num in range(1, 18):
        week_folder = weeks_folder / f"week_{week_num:02d}"
        week_folder.mkdir(exist_ok=True)

        qb_week = [{"id": "1", "name": "Patrick Mahomes", "position": "QB", "team": "KC",
                     "bye_week": 7, "fantasy_points": 350.5, "injury_status": "ACTIVE",
                     "average_draft_position": 1.2, "player_rating": 95,
                     "locked": False, "drafted_by": None,
                     "projected_points": _build_week_points(25.0, week_num, True),
                     "actual_points": _build_week_points(25.0, week_num, False)}]
        rb_week = [{"id": "3", "name": "Christian McCaffrey", "position": "RB", "team": "SF",
                     "bye_week": 9, "fantasy_points": 320.1, "injury_status": "ACTIVE",
                     "average_draft_position": 1.1, "player_rating": 94,
                     "locked": False, "drafted_by": None,
                     "projected_points": _build_week_points(22.0, week_num, True),
                     "actual_points": _build_week_points(22.0, week_num, False)}]
        wr_week = [{"id": "2", "name": "Justin Jefferson", "position": "WR", "team": "MIN",
                     "bye_week": 13, "fantasy_points": 310.8, "injury_status": "ACTIVE",
                     "average_draft_position": 2.1, "player_rating": 92,
                     "locked": False, "drafted_by": None,
                     "projected_points": _build_week_points(18.0, week_num, True),
                     "actual_points": _build_week_points(18.0, week_num, False)}]
        te_week = [{"id": "4", "name": "Travis Kelce", "position": "TE", "team": "KC",
                     "bye_week": 7, "fantasy_points": 220.4, "injury_status": "ACTIVE",
                     "average_draft_position": 4.5, "player_rating": 88,
                     "locked": False, "drafted_by": None,
                     "projected_points": _build_week_points(12.0, week_num, True),
                     "actual_points": _build_week_points(12.0, week_num, False)}]

        with open(week_folder / "qb_data.json", 'w') as f:
            json.dump({"qb_data": qb_week}, f, indent=2)
        with open(week_folder / "rb_data.json", 'w') as f:
            json.dump({"rb_data": rb_week}, f, indent=2)
        with open(week_folder / "wr_data.json", 'w') as f:
            json.dump({"wr_data": wr_week}, f, indent=2)
        with open(week_folder / "te_data.json", 'w') as f:
            json.dump({"te_data": te_week}, f, indent=2)
        with open(week_folder / "k_data.json", 'w') as f:
            json.dump({"k_data": []}, f, indent=2)
        with open(week_folder / "dst_data.json", 'w') as f:
            json.dump({"dst_data": []}, f, indent=2)


class TestEvaluateConfigTournamentProcess:
    """Unit tests for _evaluate_config_tournament_process() module-level function.

    Implements spec.md R3: directly callable without class instantiation.
    Uses mock season fixture constructed by create_mock_historical_season_f05().
    Config dict merged from accuracy_test_baseline/ league_config.json + week1-5.json.
    """

    @pytest.mark.offline
    def test_evaluate_config_tournament_process_returns_tuple_with_4_horizon_keys(self, tmp_path):
        """Test that _evaluate_config_tournament_process() returns (config_dict, results_dict)
        with all 4 horizon keys and valid AccuracyResult values.

        Asserts (spec.md R3):
        - Return value is a tuple: (config_dict, results_dict)
        - results_dict contains all 4 keys: week_1_5, week_6_9, week_10_13, week_14_17
        - Each AccuracyResult has mae >= 0.0 and player_count >= 0
        - If overall_metrics is not None: pairwise_accuracy in [0.0, 1.0]
        """
        data_path = tmp_path / "sim_data"
        data_path.mkdir()
        create_mock_historical_season_f05(data_path, "2024")

        fixtures_baseline = project_root / "tests" / "fixtures" / "accuracy_test_baseline"
        with open(fixtures_baseline / "league_config.json") as f:
            league_config = json.load(f)
        with open(fixtures_baseline / "week1-5.json") as f:
            week_config = json.load(f)

        config_dict = {
            "config_name": "test_f05_unit",
            "description": "F05 unit test config",
            "parameters": {
                **league_config.get("parameters", {}),
                **week_config.get("parameters", {}),
            },
            "_eval_metadata": {
                "param_name": "NORMALIZATION_MAX_SCALE",
                "param_value": 150,
                "horizon": "week_1_5",
                "test_idx": 0
            }
        }

        season_path = data_path / "2024"
        available_seasons = [season_path]

        result = _evaluate_config_tournament_process(config_dict, data_path, available_seasons)

        assert isinstance(result, tuple), (
            f"Expected tuple return value, got {type(result)}"
        )
        assert len(result) == 2, (
            f"Expected tuple of length 2, got length {len(result)}"
        )

        returned_config, results_dict = result

        assert isinstance(returned_config, dict), (
            f"First element of tuple should be dict (config_dict), got {type(returned_config)}"
        )
        assert isinstance(results_dict, dict), (
            f"Second element of tuple should be dict (results_dict), got {type(results_dict)}"
        )

        expected_keys = {"week_1_5", "week_6_9", "week_10_13", "week_14_17"}
        assert set(results_dict.keys()) == expected_keys, (
            f"Expected results_dict keys {expected_keys}, got {set(results_dict.keys())}"
        )

        for horizon_key, accuracy_result in results_dict.items():
            assert isinstance(accuracy_result, AccuracyResult), (
                f"results_dict['{horizon_key}'] should be AccuracyResult, "
                f"got {type(accuracy_result)}"
            )
            assert accuracy_result.mae >= 0.0, (
                f"results_dict['{horizon_key}'].mae should be >= 0.0, "
                f"got {accuracy_result.mae}"
            )
            assert accuracy_result.player_count >= 0, (
                f"results_dict['{horizon_key}'].player_count should be >= 0, "
                f"got {accuracy_result.player_count}"
            )
            if accuracy_result.overall_metrics is not None:
                pairwise = accuracy_result.overall_metrics.pairwise_accuracy
                assert 0.0 <= pairwise <= 1.0, (
                    f"results_dict['{horizon_key}'].overall_metrics.pairwise_accuracy "
                    f"should be in [0.0, 1.0], got {pairwise}"
                )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
