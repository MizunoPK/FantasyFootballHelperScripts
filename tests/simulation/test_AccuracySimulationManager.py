"""
Tests for AccuracySimulationManager

Tests the orchestration of accuracy simulation.

Author: Kai Mizuno
"""

import json
import os
import pytest
import shutil
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

project_root = Path(__file__).parent.parent.parent

from simulation.accuracy.AccuracyResultsManager import WEEK_RANGES
from simulation.accuracy.AccuracySimulationManager import (
    AccuracySimulationManager,
    MAX_ASCENT_PASSES,
)


TEST_PARAMETER_ORDER = [
    'NORMALIZATION_MAX_SCALE',
    'TEAM_QUALITY_SCORING_WEIGHT',
    'TEAM_QUALITY_MIN_WEEKS',
    'PERFORMANCE_SCORING_WEIGHT',
    'PERFORMANCE_SCORING_STEPS',
    'PERFORMANCE_MIN_WEEKS',
    'MATCHUP_IMPACT_SCALE',
    'MATCHUP_SCORING_WEIGHT',
    'MATCHUP_MIN_WEEKS',
    'TEMPERATURE_IMPACT_SCALE',
    'TEMPERATURE_SCORING_WEIGHT',
    'WIND_IMPACT_SCALE',
    'WIND_SCORING_WEIGHT',
    'LOCATION_HOME',
    'LOCATION_AWAY',
    'LOCATION_INTERNATIONAL',
]


class TestAccuracyParameterOrder:
    """Tests for accuracy parameter definitions."""

    def test_parameter_order_contains_expected_params(self):
        """Test that test parameter order contains expected prediction params."""
        expected = [
            'NORMALIZATION_MAX_SCALE',
            'TEAM_QUALITY_SCORING_WEIGHT',
            'MATCHUP_IMPACT_SCALE',
            'MATCHUP_SCORING_WEIGHT',
        ]
        for param in expected:
            assert param in TEST_PARAMETER_ORDER

    def test_parameter_order_excludes_strategy_params(self):
        """Test that test parameter order excludes win-rate strategy params."""
        strategy_params = [
            'SAME_POS_BYE_WEIGHT',
            'DIFF_POS_BYE_WEIGHT',
            'PRIMARY_BONUS',
            'SECONDARY_BONUS',
            'ADP_SCORING_WEIGHT',
            'DRAFT_ORDER_FILE',
        ]
        for param in strategy_params:
            assert param not in TEST_PARAMETER_ORDER

    def test_parameter_order_excludes_unused_params(self):
        """Test that params disabled in consuming mode are excluded."""
        unused_params = [
            'PLAYER_RATING_SCORING_WEIGHT',
        ]
        for param in unused_params:
            assert param not in TEST_PARAMETER_ORDER

    def test_parameter_order_count(self):
        """Test that we have 16 accuracy parameters."""
        assert len(TEST_PARAMETER_ORDER) == 16


class TestAccuracySimulationManagerInit:
    """Tests for AccuracySimulationManager initialization."""

    @pytest.fixture
    def mock_baseline_config(self, tmp_path):
        """Create a mock baseline config file."""
        config = {
            'config_name': 'test_config',
            'description': 'Test config',
            'parameters': {
                'NORMALIZATION_MAX_SCALE': 150,
                'DRAFT_NORMALIZATION_MAX_SCALE': 163,
                'PLAYER_RATING_SCORING': {'WEIGHT': 1.0},
            }
        }
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        return config_path

    @pytest.fixture
    def mock_data_folder(self, tmp_path):
        """Create a mock data folder with season structure."""
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()

        season_folder = data_folder / "2024"
        season_folder.mkdir()

        weeks_folder = season_folder / "weeks"
        weeks_folder.mkdir()

        for week in range(1, 18):
            week_folder = weeks_folder / f"week_{week:02d}"
            week_folder.mkdir()

            (week_folder / "players.csv").write_text("id,name\n1,Player1\n")
            (week_folder / "players_projected.csv").write_text("id,name\n1,Player1\n")

        return data_folder

    @patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager')
    def test_initialization(
        self,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        mock_data_folder,
        tmp_path
    ):
        """Test manager initialization."""
        output_dir = tmp_path / "output"

        manager = AccuracySimulationManager(
            baseline_config_path=mock_baseline_config,
            output_dir=output_dir,
            data_folder=mock_data_folder,
            parameter_order=TEST_PARAMETER_ORDER,
            num_test_values=5
        )

        assert manager.baseline_config_path == mock_baseline_config
        assert manager.output_dir == output_dir
        assert manager.data_folder == mock_data_folder
        assert manager.parameter_order == TEST_PARAMETER_ORDER
        assert manager.num_test_values == 5

    @patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager')
    def test_discover_seasons(
        self,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        mock_data_folder,
        tmp_path
    ):
        """Test season discovery."""
        output_dir = tmp_path / "output"

        manager = AccuracySimulationManager(
            baseline_config_path=mock_baseline_config,
            output_dir=output_dir,
            data_folder=mock_data_folder,
            parameter_order=TEST_PARAMETER_ORDER
        )

        assert len(manager.available_seasons) == 1
        assert manager.available_seasons[0].name == "2024"

    @patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager')
    def test_discover_seasons_multiple(
        self,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        mock_data_folder,
        tmp_path
    ):
        """Test discovery of multiple seasons."""
        season_2023 = mock_data_folder / "2023"
        season_2023.mkdir()
        (season_2023 / "weeks").mkdir()

        output_dir = tmp_path / "output"
        manager = AccuracySimulationManager(
            baseline_config_path=mock_baseline_config,
            output_dir=output_dir,
            data_folder=mock_data_folder,
            parameter_order=TEST_PARAMETER_ORDER
        )

        assert len(manager.available_seasons) == 2
        assert manager.available_seasons[0].name == "2023"
        assert manager.available_seasons[1].name == "2024"

    @patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager')
    def test_discover_seasons_no_valid_seasons_raises(
        self,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        tmp_path
    ):
        """Test that missing seasons raises error."""
        empty_data_folder = tmp_path / "empty_data"
        empty_data_folder.mkdir()

        output_dir = tmp_path / "output"

        with pytest.raises(ValueError) as exc_info:
            AccuracySimulationManager(
                baseline_config_path=mock_baseline_config,
                output_dir=output_dir,
                data_folder=empty_data_folder,
                parameter_order=TEST_PARAMETER_ORDER
            )

        assert "No valid season folders found" in str(exc_info.value)


class TestAccuracySimulationManagerSignalHandlers:
    """Tests for signal handling."""

    @pytest.fixture
    def mock_baseline_config(self, tmp_path):
        """Create a mock baseline config file."""
        config = {'config_name': 'test'}
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        return config_path

    @pytest.fixture
    def mock_data_folder(self, tmp_path):
        """Create minimal data folder."""
        data_folder = tmp_path / "sim_data" / "2024" / "weeks"
        data_folder.mkdir(parents=True)
        return tmp_path / "sim_data"

    @patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator')
    @patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager')
    @patch('signal.signal')
    def test_setup_signal_handlers(
        self,
        mock_signal,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        mock_data_folder,
        tmp_path
    ):
        """Test signal handler setup."""
        output_dir = tmp_path / "output"

        manager = AccuracySimulationManager(
            baseline_config_path=mock_baseline_config,
            output_dir=output_dir,
            data_folder=mock_data_folder,
            parameter_order=TEST_PARAMETER_ORDER
        )

        manager._setup_signal_handlers()

        assert mock_signal.call_count >= 2


class TestAccuracySimulationManagerResumeState:
    """Tests for resume state detection."""

    @pytest.fixture
    def manager_with_output(self, tmp_path):
        """Create manager with output directory for resume testing."""
        config = {'config_name': 'test'}
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)

        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()
        season = data_folder / "2024"
        season.mkdir()
        weeks = season / "weeks"
        weeks.mkdir()

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator'), \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator'), \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager'):
            manager = AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=TEST_PARAMETER_ORDER
            )
            return manager

    def test_detect_resume_no_folders(self, manager_with_output):
        """Test resume detection with no intermediate folders."""
        should_resume, start_idx, path, _pass_idx, _frozen = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0
        assert path is None

    def test_detect_resume_with_valid_folder(self, manager_with_output):
        """Test resume detection with valid intermediate folder."""
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_02_TEAM_QUALITY_SCORING_WEIGHT"
        intermediate.mkdir()
        (intermediate / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path, _pass_idx, _frozen = manager_with_output._detect_resume_state('weekly')

        assert should_resume is True
        assert start_idx == 3
        assert path == intermediate

    def test_detect_resume_with_weekly_prefix(self, manager_with_output):
        """Test resume detection with weekly prefix in folder name."""
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_01_week1-5_TEAM_QUALITY_SCORING_WEIGHT"
        intermediate.mkdir()
        (intermediate / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path, _pass_idx, _frozen = manager_with_output._detect_resume_state('weekly')

        assert should_resume is True
        assert start_idx == 2

    def test_detect_resume_incomplete_folder(self, manager_with_output):
        """Test resume detection skips folders without best.json files."""
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT"
        intermediate.mkdir()

        should_resume, start_idx, path, _pass_idx, _frozen = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0
        assert path is None

    def test_detect_resume_all_params_complete(self, manager_with_output):
        """Test resume detection when all parameters are complete."""
        last_param = TEST_PARAMETER_ORDER[-1]
        last_idx = len(TEST_PARAMETER_ORDER) - 1
        intermediate = manager_with_output.output_dir / f"accuracy_intermediate_{last_idx:02d}_{last_param}"
        intermediate.mkdir()
        (intermediate / "week1-5_best.json").write_text('{"mae": 10.5}')

        should_resume, start_idx, path, _pass_idx, _frozen = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0

    def test_detect_resume_ros_mode(self, manager_with_output):
        """Test resume detection in ROS mode."""
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_03_TEAM_QUALITY_MIN_WEEKS"
        intermediate.mkdir()
        (intermediate / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path, _pass_idx, _frozen = manager_with_output._detect_resume_state('ros')

        assert should_resume is True
        assert start_idx == 4

    def test_detect_resume_invalid_folder_name(self, manager_with_output):
        """Test resume detection ignores folders with invalid names."""
        invalid = manager_with_output.output_dir / "accuracy_intermediate_invalid"
        invalid.mkdir()
        (invalid / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path, _pass_idx, _frozen = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0

    def test_detect_resume_unknown_param(self, manager_with_output):
        """Test resume detection ignores folders with unknown parameter names."""
        unknown = manager_with_output.output_dir / "accuracy_intermediate_01_UNKNOWN_PARAM"
        unknown.mkdir()
        (unknown / "week1-5_best.json").write_text('{"mae": 10.5}')

        should_resume, start_idx, path, _pass_idx, _frozen = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0

    def test_resume_optimizes_first_incomplete_param(self, manager_with_output, tmp_path):
        """D1 regression: on resume, the first not-yet-optimized parameter
        (index resume_param_idx == highest_idx + 1) is optimized, and all
        strictly-earlier indices are skipped."""
        manager = manager_with_output

        # highest completed idx = 2 -> resume_param_idx = 3
        intermediate = manager.output_dir / "accuracy_intermediate_02_TEAM_QUALITY_MIN_WEEKS"
        intermediate.mkdir()
        league_config = {'config_name': 'League', 'parameters': {'BASE_PARAM': 1}}
        with open(intermediate / "league_config.json", 'w') as f:
            json.dump(league_config, f)
        for filename in ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            with open(intermediate / filename, 'w') as f:
                json.dump(
                    {'config_name': 'c', 'parameters': {'WEEK_PARAM': 1},
                     'performance_metrics': {'mae': 10.5, 'player_count': 10, 'config_value': 1.0}},
                    f
                )

        # Configure the mocked collaborators so run_both's loop body is survivable.
        manager.config_generator.generate_horizon_test_values.return_value = {
            '1-5': [0.1], '6-9': [0.1], '10-13': [0.1], '14-17': [0.1]
        }
        manager.config_generator.num_test_values = 5
        manager.results_manager.best_configs = {
            'week_1_5': None, 'week_6_9': None, 'week_10_13': None, 'week_14_17': None
        }
        manager.parallel_runner = Mock()
        manager.parallel_runner.evaluate_configs_parallel.return_value = []

        manager.run_both()

        called_params = [
            call.args[0]
            for call in manager.config_generator.generate_horizon_test_values.call_args_list
        ]

        # First param actually optimized is index 3 (resume_param_idx), not 4.
        assert called_params[0] == TEST_PARAMETER_ORDER[3]
        # Strictly-earlier indices (0,1,2) are skipped.
        for skipped in TEST_PARAMETER_ORDER[:3]:
            assert skipped not in called_params
        # The previously-buggy off-by-one would have skipped index 3 too.
        assert TEST_PARAMETER_ORDER[3] in called_params


class TestSweepOrphanedTempDirs:
    """Tests for AccuracySimulationManager._sweep_orphaned_temp_dirs()."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a minimal AccuracySimulationManager with mocked dependencies."""
        config = {
            'config_name': 'test',
            'description': 'test',
            'parameters': {'NORMALIZATION_MAX_SCALE': 150}
        }
        config_path = tmp_path / "baseline.json"
        config_path.write_text(json.dumps(config))

        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()
        season_folder = data_folder / "2024"
        season_folder.mkdir()
        (season_folder / "weeks").mkdir()

        output_dir = tmp_path / "output"

        with patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator'), \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator'), \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager'):
            mgr = AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=['NORMALIZATION_MAX_SCALE']
            )
        return mgr

    def test_sweep_deletes_stale_dirs(self, manager, tmp_path):
        """T1: Orphan sweep deletes dirs older than ORPHANED_DIR_MAX_AGE_HOURS."""
        mock_temp = tmp_path / "mock_temp"
        mock_temp.mkdir()

        stale1 = mock_temp / "accuracy_sim_abc123"
        stale1.mkdir()
        stale2 = mock_temp / "accuracy_sim_def456"
        stale2.mkdir()

        stale_mtime = time.time() - (25 * 3600)
        os.utime(stale1, (stale_mtime, stale_mtime))
        os.utime(stale2, (stale_mtime, stale_mtime))

        with patch('tempfile.gettempdir', return_value=str(mock_temp)):
            manager._sweep_orphaned_temp_dirs()

        assert not stale1.exists()
        assert not stale2.exists()

    def test_sweep_preserves_recent_dirs(self, manager, tmp_path):
        """T2: Orphan sweep does not delete dirs within ORPHANED_DIR_MAX_AGE_HOURS."""
        mock_temp = tmp_path / "mock_temp"
        mock_temp.mkdir()

        recent = mock_temp / "accuracy_sim_fresh123"
        recent.mkdir()

        with patch('tempfile.gettempdir', return_value=str(mock_temp)):
            manager._sweep_orphaned_temp_dirs()

        assert recent.exists()

    def test_sweep_continues_on_deletion_failure(self, manager, tmp_path):
        """T3: Orphan sweep logs warning and continues if rmtree raises OSError."""
        mock_temp = tmp_path / "mock_temp"
        mock_temp.mkdir()

        stale1 = mock_temp / "accuracy_sim_fail"
        stale1.mkdir()
        stale2 = mock_temp / "accuracy_sim_ok"
        stale2.mkdir()

        stale_mtime = time.time() - (25 * 3600)
        os.utime(stale1, (stale_mtime, stale_mtime))
        os.utime(stale2, (stale_mtime, stale_mtime))

        call_count = {'n': 0}
        original_rmtree = shutil.rmtree

        def rmtree_fail_first(path, **kwargs):
            call_count['n'] += 1
            if call_count['n'] == 1:
                raise OSError("Permission denied")
            original_rmtree(path, **kwargs)

        with patch('tempfile.gettempdir', return_value=str(mock_temp)), \
             patch('shutil.rmtree', side_effect=rmtree_fail_first):
            manager._sweep_orphaned_temp_dirs()

    def test_sweep_ignores_non_accuracy_sim_dirs(self, manager, tmp_path):
        """T4: Orphan sweep does not touch dirs without accuracy_sim_ prefix."""
        mock_temp = tmp_path / "mock_temp"
        mock_temp.mkdir()

        stale_accuracy = mock_temp / "accuracy_sim_old"
        stale_accuracy.mkdir()
        stale_other = mock_temp / "other_prefix_old"
        stale_other.mkdir()

        stale_mtime = time.time() - (25 * 3600)
        os.utime(stale_accuracy, (stale_mtime, stale_mtime))
        os.utime(stale_other, (stale_mtime, stale_mtime))

        with patch('tempfile.gettempdir', return_value=str(mock_temp)):
            manager._sweep_orphaned_temp_dirs()

        assert not stale_accuracy.exists()
        assert stale_other.exists()


def create_mock_historical_season_f05(data_folder: Path, year: str = "2024") -> None:
    """Create a mock historical season folder structure for F05 E2E accuracy testing.

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
            json.dump(qb_week, f, indent=2)
        with open(week_folder / "rb_data.json", 'w') as f:
            json.dump(rb_week, f, indent=2)
        with open(week_folder / "wr_data.json", 'w') as f:
            json.dump(wr_week, f, indent=2)
        with open(week_folder / "te_data.json", 'w') as f:
            json.dump(te_week, f, indent=2)
        with open(week_folder / "k_data.json", 'w') as f:
            json.dump([], f, indent=2)
        with open(week_folder / "dst_data.json", 'w') as f:
            json.dump([], f, indent=2)


class TestRunBothCliWiring:
    """Tests for run_accuracy_simulation.py main() CLI plumbing.

    Verifies CLI wiring (F02, F03 integration) without running the actual simulation.
    AccuracySimulationManager is mocked so tests run in milliseconds.
    """

    def test_main_shows_pairwise_in_output(self, tmp_path, capsys):
        """main() prints 'Pairwise' in stdout when get_summary() returns ranking metrics.

        Verifies F03 get_summary() upgrade is wired into the CLI output path.
        Optimal folder with all 4 horizon files must exist after run_both() completes.
        """
        fixtures_baseline = project_root / "tests" / "fixtures" / "accuracy_test_baseline"
        baseline_path = tmp_path / "baseline"
        baseline_path.mkdir()
        for fname in ["league_config.json", "week1-5.json", "week6-9.json",
                      "week10-13.json", "week14-17.json"]:
            shutil.copy(fixtures_baseline / fname, baseline_path / fname)

        data_path = tmp_path / "sim_data"
        data_path.mkdir()
        output_path = tmp_path / "output"
        output_path.mkdir()

        optimal_folder = output_path / "accuracy_optimal_test"
        optimal_folder.mkdir()
        for fname in ["week1-5.json", "week6-9.json", "week10-13.json", "week14-17.json"]:
            (optimal_folder / fname).write_text(json.dumps({}))

        mock_summary = "Pairwise=72.3% | Top-10=68.1% | Spearman=0.714 | MAE=3.2104 (diag)"

        import run_accuracy_simulation
        with patch('run_accuracy_simulation.AccuracySimulationManager') as MockMgr, \
             patch('sys.argv', ['run_accuracy_simulation.py',
                                '--baseline', str(baseline_path),
                                '--data', str(data_path),
                                '--output', str(output_path)]):
            mock_instance = MagicMock()
            mock_instance.run_both.return_value = optimal_folder
            mock_instance.results_manager.get_summary.return_value = mock_summary
            MockMgr.return_value = mock_instance
            try:
                run_accuracy_simulation.main()
            except SystemExit:
                pass

        captured = capsys.readouterr()
        assert "Pairwise" in captured.out, (
            f"Expected 'Pairwise' in stdout — verifies F03 get_summary() wiring. "
            f"stdout: {captured.out[:500]}"
        )
        for fname in ["week1-5.json", "week6-9.json", "week10-13.json", "week14-17.json"]:
            assert (optimal_folder / fname).exists(), f"Missing {fname} in optimal folder"


class TestRunBothBaselineSelection:
    """Tests for run_both non-resume baseline selection (D3: mtime, not lexical)."""

    @staticmethod
    def _write_complete_optimal_folder(folder):
        """Populate a folder with the 5 files find_baseline_config requires valid."""
        folder.mkdir(parents=True, exist_ok=True)
        for fname in ['league_config.json', 'week1-5.json', 'week6-9.json',
                      'week10-13.json', 'week14-17.json']:
            with open(folder / fname, 'w') as f:
                json.dump({'config_name': fname}, f)

    def test_run_both_picks_mtime_latest_baseline(self, tmp_path):
        """Given accuracy_optimal_* folders whose lexical and mtime orderings
        disagree, run_both's non-resume pick selects the mtime-latest *valid*
        folder (matching find_baseline_config), not the lexical-latest — and
        skips an even-newer folder that is missing required files (D3 + S1)."""
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump({'config_name': 'test'}, f)

        data_folder = tmp_path / "sim_data"
        (data_folder / "2024" / "weeks").mkdir(parents=True)

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Lexically-last but older by mtime (complete, valid).
        lexical_latest = output_dir / "accuracy_optimal_2020"
        self._write_complete_optimal_folder(lexical_latest)
        # Lexically-earlier but newer by mtime (complete, valid) — the expected pick.
        mtime_latest = output_dir / "accuracy_optimal_2019"
        self._write_complete_optimal_folder(mtime_latest)
        # Newest by mtime but INCOMPLETE (missing week files) — must be skipped (S1).
        incomplete_newest = output_dir / "accuracy_optimal_2099"
        incomplete_newest.mkdir()
        with open(incomplete_newest / "league_config.json", 'w') as f:
            json.dump({'config_name': 'partial'}, f)

        old_time = time.time() - 1000
        new_time = time.time() - 500
        newest_time = time.time()
        os.utime(lexical_latest, (old_time, old_time))
        os.utime(mtime_latest, (new_time, new_time))
        os.utime(incomplete_newest, (newest_time, newest_time))

        with patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator') as mock_cg, \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator'), \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager'):
            manager = AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=[]
            )
            # The promoted-config warner (T59) reads best_configs after
            # save_optimal_configs(); seed the four horizons so the mocked
            # results manager yields None rather than an uncomparable MagicMock.
            manager.results_manager.best_configs = {
                'week_1_5': None, 'week_6_9': None,
                'week_10_13': None, 'week_14_17': None
            }
            manager.run_both()

        # mtime-latest among the VALID folders (skips the newer incomplete one).
        mock_cg.load_baseline_from_folder.assert_called_once_with(mtime_latest)


class TestResetCandidateDumpWiring:
    """D2.2 Polish finding 1: run_both() resets the candidate-dump scratch file whenever
    _detect_resume_state() reports should_resume=False, and leaves it alone when resuming --
    so an abandoned run's records can never silently merge into a fresh ascent's promoted
    candidate_results.json. _detect_resume_state has three should_resume=False branches (no
    intermediate folders; a parameter-order mismatch; all parameters complete and all horizons
    frozen); this tests the caller-side wiring generically via the mocked return value rather
    than re-deriving each branch (already covered by TestAccuracySimulationManagerResumeState),
    since reset_candidate_dump() is called once per should_resume outcome regardless of which
    branch produced it.
    """

    def _manager(self, tmp_path):
        """A manager with the heavy collaborators stubbed out (mirrors TestT69ConvergenceLoop)."""
        mgr = AccuracySimulationManager.__new__(AccuracySimulationManager)
        mgr.logger = Mock()
        mgr.output_dir = tmp_path
        mgr.parameter_order = ['P1']
        mgr.results_manager = Mock()
        mgr.results_manager.save_optimal_configs.return_value = tmp_path / "accuracy_optimal_x"
        mgr.config_generator = Mock()
        mgr.config_generator.num_test_values = 2
        mgr._sweep_orphaned_temp_dirs = Mock()
        mgr._setup_signal_handlers = Mock()
        mgr._restore_signal_handlers = Mock()
        mgr._warn_low_accuracy_promoted = Mock()
        mgr._run_ascent_pass = Mock(return_value=set())
        return mgr

    def test_fresh_non_resumed_ascent_resets_the_scratch(self, tmp_path):
        """should_resume=False (any branch) -- reset_candidate_dump() is called exactly once,
        before the first candidate of the new ascent would be evaluated."""
        mgr = self._manager(tmp_path)
        mgr._detect_resume_state = Mock(return_value=(False, 0, None, 0, set()))

        with patch('simulation.accuracy.AccuracySimulationManager.cleanup_accuracy_intermediate_folders',
                   return_value=0):
            mgr.run_both()

        mgr.results_manager.reset_candidate_dump.assert_called_once()

    def test_resumed_ascent_does_not_touch_the_scratch(self, tmp_path):
        """should_resume=True -- reset_candidate_dump() must NOT be called, or a genuinely
        resumed process would discard its own predecessor's still-valid records."""
        mgr = self._manager(tmp_path)
        last_config_path = tmp_path / "accuracy_intermediate_0_P1"
        last_config_path.mkdir()
        mgr._detect_resume_state = Mock(return_value=(True, 1, last_config_path, 0, set()))

        with patch('simulation.accuracy.AccuracySimulationManager.cleanup_accuracy_intermediate_folders',
                   return_value=0), \
             patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator'):
            mgr.run_both()

        mgr.results_manager.reset_candidate_dump.assert_not_called()


def _perf(pairwise, top_10):
    """A best_configs entry stub carrying just the two metrics the warner reads."""
    return Mock(overall_metrics=Mock(pairwise_accuracy=pairwise, top_10_accuracy=top_10))


def _perf_without_metrics():
    """A best_configs entry whose overall_metrics is None (no valid weeks)."""
    return Mock(overall_metrics=None)


class TestLowAccuracyPromotedWarnings:
    """T59 R5/R6/R7: the low-accuracy threshold warnings fire in the PARENT,
    once per horizon, against the promoted config -- and stay wired to run_both.
    Silent detachment from run_both is exactly how the original (dead) warnings
    died, so the wiring is pinned by an explicit call-order assertion."""

    @staticmethod
    def _make_manager(tmp_path):
        """Build a manager with mocked collaborators and a MagicMock logger."""
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump({'config_name': 'test'}, f)

        data_folder = tmp_path / "sim_data"
        (data_folder / "2024" / "weeks").mkdir(parents=True)

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator'), \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator'), \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager'):
            manager = AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=[]
            )

        manager.logger = MagicMock()
        return manager

    @staticmethod
    def _warnings(manager):
        return [call.args[0] for call in manager.logger.warning.call_args_list]

    def test_threshold_constants_keep_their_values(self):
        """R5: both constants survive the deletion at their original values."""
        from simulation.accuracy import AccuracySimulationManager as module

        assert module.PAIRWISE_ACCURACY_WARN_THRESHOLD == 0.65
        assert module.TOP_10_ACCURACY_WARN_THRESHOLD == 0.70

    def test_below_threshold_warns_once_per_metric_per_horizon(self, tmp_path):
        """R6: every horizon below both bars emits exactly one warning per bar."""
        manager = self._make_manager(tmp_path)
        manager.results_manager.best_configs = {
            'week_1_5': _perf(0.50, 0.60),
            'week_6_9': _perf(0.50, 0.60),
            'week_10_13': _perf(0.50, 0.60),
            'week_14_17': _perf(0.50, 0.60),
        }

        manager._warn_low_accuracy_promoted()

        messages = self._warnings(manager)
        assert len(messages) == 8
        assert len([m for m in messages if 'Low pairwise accuracy' in m]) == 4
        assert len([m for m in messages if 'Low top-10 accuracy' in m]) == 4
        for week_key in ['week_1_5', 'week_6_9', 'week_10_13', 'week_14_17']:
            assert len([m for m in messages if f"[{week_key}]" in m]) == 2

    def test_exactly_at_threshold_does_not_warn(self, tmp_path):
        """R6 boundary: the comparison is strict `<`, so a value EQUAL to the
        threshold must stay silent."""
        manager = self._make_manager(tmp_path)
        manager.results_manager.best_configs = {
            'week_1_5': _perf(0.65, 0.70),
            'week_6_9': _perf(0.65, 0.70),
            'week_10_13': _perf(0.65, 0.70),
            'week_14_17': _perf(0.65, 0.70),
        }

        manager._warn_low_accuracy_promoted()

        assert self._warnings(manager) == []

    def test_above_threshold_does_not_warn(self, tmp_path):
        """R6: a healthy run emits zero warning lines."""
        manager = self._make_manager(tmp_path)
        manager.results_manager.best_configs = {
            'week_1_5': _perf(0.80, 0.90),
            'week_6_9': _perf(0.80, 0.90),
            'week_10_13': _perf(0.80, 0.90),
            'week_14_17': _perf(0.80, 0.90),
        }

        manager._warn_low_accuracy_promoted()

        assert self._warnings(manager) == []

    def test_none_metrics_are_skipped_without_raising(self, tmp_path):
        """None-guard parity with AccuracyResultsManager.is_better_than (T63):
        a None overall_metrics, a None pairwise_accuracy, and a None entry are
        all skipped rather than raising."""
        manager = self._make_manager(tmp_path)
        manager.results_manager.best_configs = {
            'week_1_5': _perf_without_metrics(),
            'week_6_9': _perf(None, 0.60),
            'week_10_13': None,
            'week_14_17': _perf(0.50, None),
        }

        manager._warn_low_accuracy_promoted()

        messages = self._warnings(manager)
        assert len(messages) == 2
        assert any('[week_6_9] Low top-10 accuracy' in m for m in messages)
        assert any('[week_14_17] Low pairwise accuracy' in m for m in messages)

    def test_missing_horizon_key_is_skipped(self, tmp_path):
        """An absent week_key is skipped via .get(), never a KeyError."""
        manager = self._make_manager(tmp_path)
        manager.results_manager.best_configs = {}

        manager._warn_low_accuracy_promoted()

        assert self._warnings(manager) == []

    def test_run_both_warns_immediately_after_save_optimal_configs(self, tmp_path):
        """R6 wiring: the helper runs right after save_optimal_configs(), so a
        future refactor cannot silently detach it (the original failure mode)."""
        manager = self._make_manager(tmp_path)

        call_order = []
        optimal_folder = manager.output_dir / "accuracy_optimal_test"
        manager.results_manager.save_optimal_configs.side_effect = (
            lambda: call_order.append('save_optimal_configs') or optimal_folder
        )

        with patch.object(manager, '_warn_low_accuracy_promoted',
                          side_effect=lambda: call_order.append('_warn_low_accuracy_promoted')):
            manager.run_both()

        assert call_order == ['save_optimal_configs', '_warn_low_accuracy_promoted']

    def test_no_threshold_warning_in_the_worker_module(self):
        """R7: neither constant is imported into, or evaluated inside, any accuracy
        module other than the manager that defines them.

        R7 is worded against 'any function executed in a worker process', so this
        scans every module under simulation/accuracy/ rather than only
        ParallelAccuracyRunner.py -- a threshold evaluation added to any helper the
        workers import would otherwise slip through.
        """
        accuracy_dir = project_root / "simulation" / "accuracy"
        owning_module = "AccuracySimulationManager.py"

        offenders = []
        for module_path in sorted(accuracy_dir.glob("*.py")):
            if module_path.name == owning_module:
                continue
            source = module_path.read_text()
            for constant in ('PAIRWISE_ACCURACY_WARN_THRESHOLD',
                             'TOP_10_ACCURACY_WARN_THRESHOLD'):
                if constant in source:
                    offenders.append(f"{module_path.name}: {constant}")

        assert offenders == [], (
            "Low-accuracy thresholds must be evaluated only in the parent process "
            f"({owning_module}), never in worker-executed code. Found: {offenders}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])




class TestT69ConvergenceLoop:
    """T69/D1: per-horizon convergent ascent, ported from SweepTournament's `while moved:`.

    These drive run_both's pass loop with _run_ascent_pass stubbed, so they exercise the
    freezing/termination logic without running a real optimization.
    """

    def _manager(self, tmp_path):
        """A manager with the heavy collaborators stubbed out."""
        mgr = AccuracySimulationManager.__new__(AccuracySimulationManager)
        mgr.logger = Mock()
        mgr.output_dir = tmp_path
        mgr.parameter_order = ['P1']
        mgr.results_manager = Mock()
        mgr.results_manager.save_optimal_configs.return_value = tmp_path / "accuracy_optimal_x"
        mgr.config_generator = Mock()
        mgr.config_generator.num_test_values = 2
        mgr._sweep_orphaned_temp_dirs = Mock()
        mgr._setup_signal_handlers = Mock()
        mgr._restore_signal_handlers = Mock()
        mgr._warn_low_accuracy_promoted = Mock()
        mgr._detect_resume_state = Mock(return_value=(False, 0, None, 0, set()))
        return mgr

    def test_all_horizons_converge_when_a_pass_adopts_nothing(self, tmp_path):
        """T69/AC2: a pass that adopts nothing freezes every remaining horizon and stops."""
        mgr = self._manager(tmp_path)
        mgr._run_ascent_pass = Mock(return_value=set())     # nothing ever adopts

        with patch('simulation.accuracy.AccuracySimulationManager.cleanup_accuracy_intermediate_folders', return_value=0):
            mgr.run_both()

        # One pass suffices: nothing adopted, so all four freeze immediately.
        assert mgr._run_ascent_pass.call_count == 1

    def test_frozen_horizons_are_passed_to_the_next_pass(self, tmp_path):
        """T69/AC2: a horizon that adopted nothing is frozen and handed to later passes.

        week_1_5 adopts on pass 1 only; the other three freeze after pass 1. Pass 2 must
        therefore receive those three as frozen.
        """
        mgr = self._manager(tmp_path)
        calls = []

        def fake_pass(pass_idx, frozen, should_resume, resume_idx, resume_pass_idx=0):
            calls.append(set(frozen))
            return {'week_1_5'} if pass_idx == 0 else set()

        mgr._run_ascent_pass = Mock(side_effect=fake_pass)
        with patch('simulation.accuracy.AccuracySimulationManager.cleanup_accuracy_intermediate_folders', return_value=0):
            mgr.run_both()

        assert calls[0] == set(), "pass 1 must start with nothing frozen"
        assert calls[1] == {'week_6_9', 'week_10_13', 'week_14_17'}, (
            "pass 2 must receive the three horizons that adopted nothing in pass 1"
        )
        assert mgr._run_ascent_pass.call_count == 2

    def test_bound_hit_stops_the_run_and_is_not_called_convergence(self, tmp_path):
        """T69/AC3: a never-converging horizon stops at the bound, reported distinctly.

        A bound hit means the run did NOT settle. Reporting it as convergence would hide
        exactly the non-convergence the bound exists to surface.
        """
        mgr = self._manager(tmp_path)
        mgr._run_ascent_pass = Mock(return_value=set(WEEK_RANGES.keys()))   # always adopts

        with patch('simulation.accuracy.AccuracySimulationManager.cleanup_accuracy_intermediate_folders', return_value=0):
            mgr.run_both()

        assert mgr._run_ascent_pass.call_count == MAX_ASCENT_PASSES

        warned = " ".join(str(c) for c in mgr.logger.warning.call_args_list)
        assert "BOUND" in warned.upper(), "a bound hit must be warned about"

        infos = " ".join(str(c) for c in mgr.logger.info.call_args_list)
        assert "BOUND-HIT" in infos, "the completion line must say BOUND-HIT"
        assert "CONVERGED after" not in infos, (
            "a bound-hit run must NOT be reported as converged"
        )

    def test_warn_low_accuracy_promoted_fires_exactly_once_per_run(self, tmp_path):
        """T69/AC7: T59's warning hook fires once per RUN, not once per pass.

        It is the only thing that makes the two low-accuracy thresholds reachable, and
        firing it per pass would turn it into noise.
        """
        mgr = self._manager(tmp_path)
        seq = [{'week_1_5'}, {'week_1_5'}, set()]
        mgr._run_ascent_pass = Mock(side_effect=lambda pi, fz, sr, ri, rpi=0: seq[min(pi, len(seq) - 1)])

        with patch('simulation.accuracy.AccuracySimulationManager.cleanup_accuracy_intermediate_folders', return_value=0):
            mgr.run_both()

        assert mgr._run_ascent_pass.call_count > 1, "this test is only meaningful multi-pass"
        assert mgr._warn_low_accuracy_promoted.call_count == 1
        assert mgr.results_manager.save_optimal_configs.call_count == 1


class TestT69PassAwareResume:
    """T69/D5: resume carries the pass index and frozen-horizon set, not just a param index."""

    def test_ascent_state_roundtrips_through_the_intermediate_folder(self, tmp_path):
        """The state is written into the folder it describes and read back."""
        mgr = AccuracySimulationManager.__new__(AccuracySimulationManager)
        mgr.logger = Mock()
        folder = tmp_path / "accuracy_intermediate_03_P1"
        folder.mkdir(parents=True)
        (folder / '_ascent_state.json').write_text(json.dumps({
            'pass_idx': 2,
            'frozen_horizons': ['week_1_5', 'week_6_9'],
        }))

        pass_idx, frozen = mgr._read_ascent_state(folder)
        assert pass_idx == 2
        assert frozen == {'week_1_5', 'week_6_9'}

    def test_legacy_folder_without_ascent_state_does_not_raise(self, tmp_path):
        """T69/AC8: a pre-T69 intermediate folder resumes as pass 0, nothing frozen.

        Losing the pass detail is far better than raising on it or discarding the run's
        completed work.
        """
        mgr = AccuracySimulationManager.__new__(AccuracySimulationManager)
        mgr.logger = Mock()
        folder = tmp_path / "accuracy_intermediate_01_P1"
        folder.mkdir(parents=True)

        assert mgr._read_ascent_state(folder) == (0, set())

    def test_corrupt_ascent_state_degrades_rather_than_raising(self, tmp_path):
        """A truncated/invalid state file must not take the whole resume down."""
        mgr = AccuracySimulationManager.__new__(AccuracySimulationManager)
        mgr.logger = Mock()
        folder = tmp_path / "accuracy_intermediate_02_P1"
        folder.mkdir(parents=True)
        (folder / '_ascent_state.json').write_text("{not valid json")

        assert mgr._read_ascent_state(folder) == (0, set())
        assert mgr.logger.warning.called, "a corrupt state file should be surfaced, not silent"

    def test_resume_seeds_the_loop_with_recorded_pass_and_frozen_set(self, tmp_path):
        """T69/AC8: run_both starts at the recorded pass with frozen horizons intact.

        Without this the run would restart at pass 1 and re-optimize horizons that had
        already converged.
        """
        mgr = AccuracySimulationManager.__new__(AccuracySimulationManager)
        mgr.logger = Mock()
        mgr.output_dir = tmp_path
        mgr.parameter_order = ['P1']
        mgr.results_manager = Mock()
        mgr.results_manager.save_optimal_configs.return_value = tmp_path / "opt"
        mgr.config_generator = Mock()
        mgr.config_generator.num_test_values = 2
        mgr.config_generator.baseline_configs = {}
        mgr._sweep_orphaned_temp_dirs = Mock()
        mgr._setup_signal_handlers = Mock()
        mgr._restore_signal_handlers = Mock()
        mgr._warn_low_accuracy_promoted = Mock()
        mgr._detect_resume_state = Mock(
            return_value=(True, 0, None, 2, {'week_1_5', 'week_6_9'})
        )

        seen = []

        def fake_pass(pass_idx, frozen, should_resume, resume_idx, resume_pass_idx=0):
            seen.append((pass_idx, set(frozen)))
            return set()

        mgr._run_ascent_pass = Mock(side_effect=fake_pass)
        with patch('simulation.accuracy.AccuracySimulationManager.cleanup_accuracy_intermediate_folders', return_value=0):
            mgr.run_both()

        assert seen[0][0] == 2, "must resume at the recorded pass, not restart at 0"
        assert seen[0][1] == {'week_1_5', 'week_6_9'}, "frozen horizons must survive the resume"


class TestT69ResumeAcrossPasses:
    """Polish: gaps found at review in how resume interacts with MULTIPLE passes.

    Pre-T69 there was only ever one pass, so "every parameter has an intermediate folder"
    correctly meant "the run is finished". That inference is wrong once passes exist.
    """

    def _mgr(self, tmp_path):
        mgr = AccuracySimulationManager.__new__(AccuracySimulationManager)
        mgr.logger = Mock()
        mgr.output_dir = tmp_path
        mgr.parameter_order = ['P1', 'P2']
        mgr.results_manager = Mock()
        mgr.results_manager.save_optimal_configs.return_value = tmp_path / "opt"
        mgr.config_generator = Mock()
        mgr.config_generator.num_test_values = 2
        mgr.config_generator.baseline_configs = {}
        mgr._sweep_orphaned_temp_dirs = Mock()
        mgr._setup_signal_handlers = Mock()
        mgr._restore_signal_handlers = Mock()
        mgr._warn_low_accuracy_promoted = Mock()
        return mgr

    def test_completed_pass_resumes_into_the_next_pass(self, tmp_path):
        """A pass that finished every parameter must resume at the NEXT pass, not refuse.

        Refusing here would discard a completed pass and restart the whole ascent.
        """
        mgr = self._mgr(tmp_path)
        mgr._detect_resume_state = Mock(return_value=(True, 0, None, 3, {'week_1_5'}))
        seen = []

        def fake_pass(pass_idx, frozen, should_resume, resume_idx, resume_pass_idx=0):
            seen.append(pass_idx)
            return set()

        mgr._run_ascent_pass = Mock(side_effect=fake_pass)
        with patch('simulation.accuracy.AccuracySimulationManager.cleanup_accuracy_intermediate_folders', return_value=0):
            mgr.run_both()

        assert seen and seen[0] == 3, "must continue at the recorded pass, not restart at 0"

    def test_fully_frozen_resume_runs_no_pass_at_all(self, tmp_path):
        """An already-converged resume must not run a no-op pass.

        Running one would do no work yet still write intermediate folders.
        """
        mgr = self._mgr(tmp_path)
        mgr._detect_resume_state = Mock(
            return_value=(True, 0, None, 2, set(WEEK_RANGES.keys()))
        )
        mgr._run_ascent_pass = Mock(return_value=set())

        with patch('simulation.accuracy.AccuracySimulationManager.cleanup_accuracy_intermediate_folders', return_value=0):
            mgr.run_both()

        assert mgr._run_ascent_pass.call_count == 0, "nothing left to optimize -- run no pass"
        assert mgr._warn_low_accuracy_promoted.call_count == 1, "the run still finalizes"

    def test_resume_skip_applies_only_to_the_resumed_pass(self, tmp_path):
        """The skip belongs to the pass being resumed INTO; later passes walk from the top.

        Guarding on `pass_idx == 0` instead would re-run already-completed parameters of a
        mid-pass-2 resume, and would wrongly skip them in every later pass.
        """
        mgr = self._mgr(tmp_path)
        mgr.parameter_order = ['P1', 'P2', 'P3']
        mgr.config_generator.generate_horizon_test_values = Mock(
            return_value={h: [1, 2] for h in WEEK_RANGES}
        )
        # must be a real dict -- the pass body assigns config_dict['_eval_metadata']
        mgr.config_generator.get_config_for_horizon = Mock(side_effect=lambda *a, **k: {})
        mgr.config_generator.update_baseline_for_horizon = Mock()
        mgr.parallel_runner = Mock()
        mgr.parallel_runner.evaluate_configs_parallel = Mock(return_value=[])
        mgr.progress_tracker = Mock()
        mgr._log_parameter_summary = Mock()

        with patch('simulation.accuracy.AccuracySimulationManager.ProgressTracker'):
            # resuming INTO pass 2 at param 2: P1 skipped
            mgr._run_ascent_pass(2, set(), should_resume=True, resume_param_idx=2, resume_pass_idx=2)
            first = mgr.config_generator.generate_horizon_test_values.call_args_list[:]
            assert [c.args[0] for c in first] == ['P3'], f"expected only P3, got {[c.args[0] for c in first]}"

            mgr.config_generator.generate_horizon_test_values.reset_mock()
            # a LATER pass must walk every parameter
            mgr._run_ascent_pass(3, set(), should_resume=True, resume_param_idx=2, resume_pass_idx=2)
            later = [c.args[0] for c in mgr.config_generator.generate_horizon_test_values.call_args_list]
            assert later == ['P1', 'P2', 'P3'], f"later pass must not skip: got {later}"


class TestD84ExcludeLowCoverageWeeksPrePass:
    """D8.4: the exclusion decision is a parent-side pre-pass, gated on the flag."""

    @pytest.fixture
    def baseline_config(self, tmp_path):
        """A minimal baseline config file."""
        config = {
            'config_name': 'test_config',
            'description': 'Test config',
            'parameters': {'NORMALIZATION_MAX_SCALE': 150},
        }
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        return config_path

    @pytest.fixture
    def data_folder(self, tmp_path):
        """A mock sim_data folder carrying one discoverable season."""
        data_folder = tmp_path / "sim_data"
        weeks_folder = data_folder / "2024" / "weeks"
        for week in range(1, 18):
            week_folder = weeks_folder / f"week_{week:02d}"
            week_folder.mkdir(parents=True)
            (week_folder / "players.csv").write_text("id,name\n1,Player1\n")
        return data_folder

    def _build(self, baseline_config, data_folder, tmp_path, **kwargs):
        with patch('simulation.accuracy.AccuracySimulationManager.ConfigGenerator'), \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyCalculator'), \
             patch('simulation.accuracy.AccuracySimulationManager.AccuracyResultsManager'), \
             patch('simulation.accuracy.AccuracySimulationManager.excluded_weeks_by_season') as mock_excluded:
            mock_excluded.return_value = {'2023': frozenset({1})}
            manager = AccuracySimulationManager(
                baseline_config_path=baseline_config,
                output_dir=tmp_path / "output",
                data_folder=data_folder,
                parameter_order=TEST_PARAMETER_ORDER,
                **kwargs
            )
        return manager, mock_excluded

    def test_the_pre_pass_does_not_run_by_default(
        self, baseline_config, data_folder, tmp_path
    ):
        # Act - no flag argument at all
        manager, mock_excluded = self._build(baseline_config, data_folder, tmp_path)

        # Assert - nothing computed, nothing logged, empty mapping.
        mock_excluded.assert_not_called()
        assert manager.excluded_season_weeks == {}

    def test_the_flag_off_explicitly_also_computes_nothing(
        self, baseline_config, data_folder, tmp_path
    ):
        # Act
        manager, mock_excluded = self._build(
            baseline_config, data_folder, tmp_path, exclude_low_coverage_weeks=False
        )

        # Assert
        mock_excluded.assert_not_called()
        assert manager.excluded_season_weeks == {}

    def test_the_flag_on_calls_the_shared_owner_once_with_the_discovered_seasons(
        self, baseline_config, data_folder, tmp_path
    ):
        # Act
        manager, mock_excluded = self._build(
            baseline_config, data_folder, tmp_path, exclude_low_coverage_weeks=True
        )

        # Assert - once per run, in the parent, over exactly the discovered
        # seasons (D8.4 HD1).
        mock_excluded.assert_called_once_with(manager.available_seasons)
        assert manager.excluded_season_weeks == {'2023': frozenset({1})}

    def test_the_pre_pass_mapping_is_the_one_handed_to_the_runner(
        self, baseline_config, data_folder, tmp_path
    ):
        """D8.4: the parent-side pre-pass result must REACH the workers.

        Asserting only `manager.excluded_season_weeks` (the three tests above)
        leaves the single link this unit exists to create untested: replacing
        the `excluded_season_weeks=self.excluded_season_weeks` argument at the
        `ParallelAccuracyRunner(...)` call site with a literal `{}` keeps every
        other test green while the pre-pass logs exclusions the workers never
        apply -- a silent, favourable-looking narrowing of nothing. This test
        drives the construction and asserts on the value actually passed.
        """
        # Arrange - flag on, so the pre-pass produces a non-empty mapping.
        manager, _ = self._build(
            baseline_config, data_folder, tmp_path, exclude_low_coverage_weeks=True
        )
        manager.parameter_order = ['P1']
        manager.config_generator.generate_horizon_test_values = Mock(
            return_value={h: [1] for h in WEEK_RANGES}
        )
        # must be a real dict -- the pass body assigns config_dict['_eval_metadata']
        manager.config_generator.get_config_for_horizon = Mock(side_effect=lambda *a, **k: {})
        manager.config_generator.update_baseline_for_horizon = Mock()
        manager.parallel_runner = None      # force the construction under test
        manager._log_parameter_summary = Mock()

        # Act - the runner is imported inside the method, so patch it at its home.
        with patch('simulation.accuracy.ParallelAccuracyRunner.ParallelAccuracyRunner') as mock_runner_cls, \
             patch('simulation.accuracy.AccuracySimulationManager.ProgressTracker'):
            mock_runner_cls.return_value.evaluate_configs_parallel.return_value = []
            manager._run_ascent_pass(
                0, set(), should_resume=False, resume_param_idx=0, resume_pass_idx=0
            )

        # Assert - the runner was handed the pre-pass's own mapping, by identity
        # and by value.
        mock_runner_cls.assert_called_once()
        passed = mock_runner_cls.call_args.kwargs['excluded_season_weeks']
        assert passed is manager.excluded_season_weeks, (
            "the runner must receive the pre-pass mapping itself, not a substitute"
        )
        assert passed == {'2023': frozenset({1})}, (
            f"the workers must see the excluded season-weeks, got {passed}"
        )
