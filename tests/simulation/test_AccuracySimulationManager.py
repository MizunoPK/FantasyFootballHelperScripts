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

from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager


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
        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0
        assert path is None

    def test_detect_resume_with_valid_folder(self, manager_with_output):
        """Test resume detection with valid intermediate folder."""
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_02_TEAM_QUALITY_SCORING_WEIGHT"
        intermediate.mkdir()
        (intermediate / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is True
        assert start_idx == 3
        assert path == intermediate

    def test_detect_resume_with_weekly_prefix(self, manager_with_output):
        """Test resume detection with weekly prefix in folder name."""
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_01_week1-5_TEAM_QUALITY_SCORING_WEIGHT"
        intermediate.mkdir()
        (intermediate / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is True
        assert start_idx == 2

    def test_detect_resume_incomplete_folder(self, manager_with_output):
        """Test resume detection skips folders without best.json files."""
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT"
        intermediate.mkdir()

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

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

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0

    def test_detect_resume_ros_mode(self, manager_with_output):
        """Test resume detection in ROS mode."""
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_03_TEAM_QUALITY_MIN_WEEKS"
        intermediate.mkdir()
        (intermediate / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('ros')

        assert should_resume is True
        assert start_idx == 4

    def test_detect_resume_invalid_folder_name(self, manager_with_output):
        """Test resume detection ignores folders with invalid names."""
        invalid = manager_with_output.output_dir / "accuracy_intermediate_invalid"
        invalid.mkdir()
        (invalid / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0

    def test_detect_resume_unknown_param(self, manager_with_output):
        """Test resume detection ignores folders with unknown parameter names."""
        unknown = manager_with_output.output_dir / "accuracy_intermediate_01_UNKNOWN_PARAM"
        unknown.mkdir()
        (unknown / "week1-5_best.json").write_text('{"mae": 10.5}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

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


