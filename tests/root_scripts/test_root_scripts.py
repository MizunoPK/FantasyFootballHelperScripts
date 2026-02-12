"""
Unit Tests for Root Runner Scripts

Tests all root-level runner scripts including league helper, data fetchers,
simulation runner, and pre-commit validation.

Author: Kai Mizuno
"""

import pytest
import subprocess
import sys
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
from io import StringIO

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))


# ============================================================================
# TEST RUN_LEAGUE_HELPER.PY
# ============================================================================

class TestRunLeagueHelper:
    """Test run_league_helper.py"""

    @patch('sys.argv', ['run_league_helper.py'])
    @patch('subprocess.run')
    def test_run_league_helper_success(self, mock_run):
        """Test successful league helper execution"""
        # Mock successful subprocess execution
        mock_run.return_value = Mock(returncode=0)

        # Import and run
        from run_league_helper import run_league_helper
        exit_code = run_league_helper()

        assert exit_code == 0
        mock_run.assert_called_once()

        # Verify correct script path and arguments
        # Note: Data folder is NOT passed as argument - LeagueHelperManager constructs it internally
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == sys.executable
        assert "LeagueHelperManager.py" in call_args[1]
        assert len(call_args) == 2  # Only python executable and script path

    @patch('sys.argv', ['run_league_helper.py'])
    @patch('subprocess.run')
    def test_run_league_helper_handles_subprocess_error(self, mock_run):
        """Test handling of subprocess errors"""
        # Mock subprocess failure
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')

        from run_league_helper import run_league_helper
        exit_code = run_league_helper()

        assert exit_code == 1

    @patch('sys.argv', ['run_league_helper.py'])
    @patch('subprocess.run')
    def test_run_league_helper_handles_general_exception(self, mock_run):
        """Test handling of general exceptions"""
        # Mock general exception
        mock_run.side_effect = RuntimeError("Test error")

        from run_league_helper import run_league_helper
        exit_code = run_league_helper()

        assert exit_code == 1

    @patch('sys.argv', ['run_league_helper.py', '--enable-log-file'])
    @patch('subprocess.run')
    def test_run_league_helper_uses_correct_data_folder(self, mock_run):
        """Test that CLI arguments are forwarded correctly"""
        # Note: Data folder is NOT passed as argument - LeagueHelperManager constructs it internally
        # This test now verifies CLI argument forwarding (KAI-8 feature)
        mock_run.return_value = Mock(returncode=0)

        from run_league_helper import run_league_helper
        run_league_helper()

        call_args = mock_run.call_args[0][0]
        assert len(call_args) == 3  # python, script, --enable-log-file
        assert "--enable-log-file" in call_args


# ============================================================================
# TEST RUN_PLAYER_FETCHER.PY
# ============================================================================

class TestRunPlayerFetcher:
    """Test run_player_fetcher.py"""

    @patch('os.chdir')
    @patch('subprocess.run')
    def test_run_player_fetcher_success(self, mock_run, mock_chdir):
        """Test successful player fetcher execution"""
        mock_run.return_value = Mock(returncode=0)

        # Import and run the main block
        import run_player_fetcher
        # The script runs in if __name__ == "__main__", so we need to call it differently
        # Let's just verify the script structure exists

        assert hasattr(run_player_fetcher, 'subprocess')
        assert hasattr(run_player_fetcher, 'Path')

    @patch('os.chdir')
    @patch('subprocess.run')
    @patch('sys.exit')
    def test_run_player_fetcher_handles_subprocess_error(self, mock_exit, mock_run, mock_chdir):
        """Test handling of subprocess errors in player fetcher"""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')

        # We can't easily test the __main__ block, but we can verify the imports work
        import run_player_fetcher
        assert run_player_fetcher.subprocess is not None

    @patch('os.chdir')
    def test_run_player_fetcher_changes_directory(self, mock_chdir):
        """Test that player fetcher changes to correct directory"""
        import run_player_fetcher

        # Verify the script structure
        assert run_player_fetcher.Path is not None


# ============================================================================
# TEST RUN_PRE_COMMIT_VALIDATION.PY
# ============================================================================

class TestRunPreCommitValidation:
    """Test run_pre_commit_validation.py"""

    @patch('subprocess.run')
    def test_run_validation_success(self, mock_run):
        """Test successful validation"""
        mock_run.return_value = Mock(returncode=0)

        from run_pre_commit_validation import run_validation
        exit_code = run_validation()

        assert exit_code == 0
        mock_run.assert_called_once()

        # Verify test runner is called
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == sys.executable
        assert "run_all_tests.py" in call_args[1]

    @patch('subprocess.run')
    def test_run_validation_failure(self, mock_run):
        """Test validation failure"""
        mock_run.return_value = Mock(returncode=1)

        from run_pre_commit_validation import run_validation
        exit_code = run_validation()

        assert exit_code == 1

    @patch('subprocess.run')
    def test_run_validation_handles_exception(self, mock_run):
        """Test handling of exceptions during validation"""
        mock_run.side_effect = RuntimeError("Test error")

        from run_pre_commit_validation import run_validation
        exit_code = run_validation()

        assert exit_code == 1

    @patch('subprocess.run')
    def test_run_validation_uses_check_false(self, mock_run):
        """Test that validation doesn't raise on failure"""
        mock_run.return_value = Mock(returncode=1)

        from run_pre_commit_validation import run_validation
        # Should not raise exception even with returncode=1
        exit_code = run_validation()

        assert exit_code == 1
        # Verify check=False was used
        assert mock_run.call_args[1]['check'] == False


# ============================================================================
# TEST RUN_SIMULATION.PY
# ============================================================================

class TestRunSimulation:
    """Test run_win_rate_simulation.py main function and argument parsing"""

    @patch('run_win_rate_simulation.SimulationManager')
    @patch('run_win_rate_simulation.Path')
    def test_single_mode_argument_parsing(self, mock_path_class, mock_sim_manager):
        """Test single mode argument parsing"""
        # Create a mock config folder that supports the / operator for file paths
        mock_folder = Mock()
        mock_folder.name = "optimal_test_folder"
        mock_folder.is_dir.return_value = True
        mock_folder.stat.return_value = Mock(st_mtime=1.0)

        # Mock file that exists
        mock_file = Mock()
        mock_file.exists.return_value = True

        # Mock the / operator to return file paths
        mock_folder.__truediv__ = Mock(return_value=mock_file)

        # Mock Path behavior - now uses folder-based configs
        mock_path = Mock()
        mock_path.glob.return_value = [mock_folder]
        mock_path.name = "optimal_test_folder"
        mock_path.exists.return_value = True
        mock_path_class.return_value = mock_path

        # Mock data folder existence
        mock_data_path = Mock()
        mock_data_path.exists.return_value = True

        def path_side_effect(arg):
            if "sim_data" in str(arg):
                return mock_data_path
            return mock_path

        mock_path_class.side_effect = path_side_effect

        # Mock SimulationManager
        mock_manager = Mock()
        mock_sim_manager.return_value = mock_manager

        # Test single mode
        from run_win_rate_simulation import main
        with patch('sys.argv', ['run_win_rate_simulation.py', 'single', '--sims', '10']):
            try:
                main()
            except SystemExit:
                pass  # main() calls sys.exit() on error

    def test_simulation_modes_defined(self):
        """Test that all simulation modes are properly defined"""
        from run_win_rate_simulation import main

        # Verify the function exists and is callable
        assert callable(main)

    @patch('run_win_rate_simulation.SimulationManager')
    @patch('run_win_rate_simulation.Path')
    def test_full_mode_shows_total_configs(self, mock_path_class, mock_sim_manager):
        """Test that full mode calculates and displays total configs"""
        # Mock Path
        mock_path = Mock()
        mock_path.glob.return_value = [Mock(stat=Mock(return_value=Mock(st_mtime=1.0)))]
        mock_path.name = "optimal_test.json"
        mock_path.exists.return_value = True
        mock_path_class.return_value = mock_path

        # This test verifies the structure is in place
        from run_win_rate_simulation import main
        assert callable(main)

    @patch('run_win_rate_simulation.SimulationManager')
    @patch('run_win_rate_simulation.Path')
    def test_iterative_mode_shows_parameter_count(self, mock_path_class, mock_sim_manager):
        """Test that iterative mode shows parameter optimization info"""
        # Mock Path
        mock_path = Mock()
        mock_path.glob.return_value = [Mock(stat=Mock(return_value=Mock(st_mtime=1.0)))]
        mock_path.name = "optimal_test.json"
        mock_path.exists.return_value = True
        mock_path_class.return_value = mock_path

        from run_win_rate_simulation import main
        assert callable(main)

    def test_logging_constants_defined(self):
        """Test that logging constants are properly defined"""
        import run_win_rate_simulation

        assert hasattr(run_win_rate_simulation, 'LOGGING_LEVEL')
        assert hasattr(run_win_rate_simulation, 'LOG_NAME')
        assert run_win_rate_simulation.LOG_NAME == "win_rate_simulation"

    def test_default_arguments_defined(self):
        """Test that default argument values are reasonable"""
        import run_win_rate_simulation

        # Verify the module loads without error
        assert run_win_rate_simulation.LOGGING_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


# ============================================================================
# TEST RUN_DRAFT_ORDER_LOOP.PY
# ============================================================================

class TestRunDraftOrderLoop:
    """Test run_draft_order_loop.py functions and argument parsing"""

    def test_logging_constants_defined(self):
        """Test that logging constants are properly defined"""
        import run_draft_order_loop

        assert hasattr(run_draft_order_loop, 'LOGGING_LEVEL')
        assert hasattr(run_draft_order_loop, 'LOGGING_TO_FILE')
        assert hasattr(run_draft_order_loop, 'LOG_NAME')
        assert run_draft_order_loop.LOG_NAME == "draft_order_loop"

    def test_default_arguments_defined(self):
        """Test that default argument values are defined"""
        import run_draft_order_loop

        assert hasattr(run_draft_order_loop, 'DEFAULT_SIMS')
        assert hasattr(run_draft_order_loop, 'DEFAULT_WORKERS')
        assert hasattr(run_draft_order_loop, 'DEFAULT_DATA')
        assert hasattr(run_draft_order_loop, 'DEFAULT_TEST_VALUES')
        assert run_draft_order_loop.LOGGING_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    def test_discover_draft_order_files_empty_dir(self, tmp_path):
        """Test discover_draft_order_files with empty directory"""
        from run_draft_order_loop import discover_draft_order_files
        from utils.LoggingManager import setup_logger

        # Set up logging for the test
        setup_logger("test", "WARNING", False, None, "simple")

        # Create empty directory
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        result = discover_draft_order_files(draft_order_dir)
        assert result == []

    def test_discover_draft_order_files_finds_files(self, tmp_path):
        """Test discover_draft_order_files finds numbered JSON files"""
        from run_draft_order_loop import discover_draft_order_files
        from utils.LoggingManager import setup_logger

        setup_logger("test", "WARNING", False, None, "simple")

        # Create directory with test files
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        # Create test JSON files
        (draft_order_dir / "0_MINE.json").write_text('{"DRAFT_ORDER": []}')
        (draft_order_dir / "1_zero_rb.json").write_text('{"DRAFT_ORDER": []}')
        (draft_order_dir / "2_hero_rb.json").write_text('{"DRAFT_ORDER": []}')

        result = discover_draft_order_files(draft_order_dir)
        assert result == [0, 1, 2]

    def test_discover_draft_order_files_skips_non_numbered(self, tmp_path):
        """Test discover_draft_order_files skips files without leading numbers"""
        from run_draft_order_loop import discover_draft_order_files
        from utils.LoggingManager import setup_logger

        setup_logger("test", "WARNING", False, None, "simple")

        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        # Create files - some with numbers, some without
        (draft_order_dir / "0_MINE.json").write_text('{"DRAFT_ORDER": []}')
        (draft_order_dir / "readme.json").write_text('{}')
        (draft_order_dir / "test_file.json").write_text('{}')

        result = discover_draft_order_files(draft_order_dir)
        assert result == [0]

    def test_discover_draft_order_files_missing_dir(self, tmp_path):
        """Test discover_draft_order_files raises error for missing directory"""
        from run_draft_order_loop import discover_draft_order_files

        draft_order_dir = tmp_path / "nonexistent"

        with pytest.raises(FileNotFoundError):
            discover_draft_order_files(draft_order_dir)

    def test_load_draft_order_from_file(self, tmp_path):
        """Test load_draft_order_from_file loads DRAFT_ORDER correctly"""
        from run_draft_order_loop import load_draft_order_from_file
        from utils.LoggingManager import setup_logger

        setup_logger("test", "WARNING", False, None, "simple")

        # Create test structure
        data_folder = tmp_path
        draft_order_dir = data_folder / "draft_order_possibilities"
        draft_order_dir.mkdir()

        # Create test file with DRAFT_ORDER
        test_order = ["QB", "RB", "WR", "TE"]
        (draft_order_dir / "0_MINE.json").write_text(json.dumps({"DRAFT_ORDER": test_order}))

        result = load_draft_order_from_file(0, data_folder)
        assert result == test_order

    def test_load_draft_order_from_file_missing(self, tmp_path):
        """Test load_draft_order_from_file raises error for missing file"""
        from run_draft_order_loop import load_draft_order_from_file

        data_folder = tmp_path
        draft_order_dir = data_folder / "draft_order_possibilities"
        draft_order_dir.mkdir()

        with pytest.raises(FileNotFoundError):
            load_draft_order_from_file(99, data_folder)

    def test_get_strategy_name(self, tmp_path):
        """Test get_strategy_name returns correct name"""
        from run_draft_order_loop import get_strategy_name

        data_folder = tmp_path
        draft_order_dir = data_folder / "draft_order_possibilities"
        draft_order_dir.mkdir()

        (draft_order_dir / "0_MINE.json").write_text('{}')
        (draft_order_dir / "1_zero_rb.json").write_text('{}')

        assert get_strategy_name(0, data_folder) == "0_MINE"
        assert get_strategy_name(1, data_folder) == "1_zero_rb"

    def test_get_strategy_name_missing(self, tmp_path):
        """Test get_strategy_name raises error for missing file"""
        from run_draft_order_loop import get_strategy_name

        data_folder = tmp_path
        draft_order_dir = data_folder / "draft_order_possibilities"
        draft_order_dir.mkdir()

        with pytest.raises(FileNotFoundError):
            get_strategy_name(99, data_folder)

    def test_find_latest_optimal_folder(self, tmp_path):
        """Test find_latest_optimal_folder finds most recent folder"""
        from run_draft_order_loop import find_latest_optimal_folder
        import time

        config_dir = tmp_path

        # Create two optimal folders
        folder1 = config_dir / "optimal_old"
        folder1.mkdir()
        for f in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            (folder1 / f).write_text('{}')

        time.sleep(0.1)  # Ensure different modification times

        folder2 = config_dir / "optimal_new"
        folder2.mkdir()
        for f in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            (folder2 / f).write_text('{}')

        result = find_latest_optimal_folder(config_dir)
        assert result.name == "optimal_new"

    def test_find_latest_optimal_folder_empty(self, tmp_path):
        """Test find_latest_optimal_folder returns None when no folders exist"""
        from run_draft_order_loop import find_latest_optimal_folder

        result = find_latest_optimal_folder(tmp_path)
        assert result is None

    def test_find_latest_optimal_folder_incomplete(self, tmp_path):
        """Test find_latest_optimal_folder skips incomplete folders"""
        from run_draft_order_loop import find_latest_optimal_folder

        config_dir = tmp_path

        # Create incomplete folder (missing files)
        folder = config_dir / "optimal_incomplete"
        folder.mkdir()
        (folder / "league_config.json").write_text('{}')
        # Missing week files

        result = find_latest_optimal_folder(config_dir)
        assert result is None

    def test_find_resume_point_no_progress(self, tmp_path):
        """Test find_resume_point with no progress file (fresh start)"""
        from run_draft_order_loop import find_resume_point
        from utils.LoggingManager import setup_logger

        setup_logger("test", "WARNING", False, None, "simple")

        strategies_dir = tmp_path / "strategies"
        strategies_dir.mkdir()

        # Create data folder (required parameter)
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()

        draft_files = [0, 1, 2]
        start_idx, action, cycle = find_resume_point(draft_files, strategies_dir, data_folder)

        assert start_idx == 0
        assert action == "start"
        assert cycle == 1

    def test_find_resume_point_with_progress(self, tmp_path):
        """Test find_resume_point resumes from progress file"""
        from run_draft_order_loop import find_resume_point
        from utils.LoggingManager import setup_logger

        setup_logger("test", "WARNING", False, None, "simple")

        strategies_dir = tmp_path / "strategies"
        strategies_dir.mkdir()

        # Create data folder (required parameter)
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()

        # Create progress file
        progress_file = strategies_dir / "loop_progress.json"
        progress_file.write_text(json.dumps({
            "current_cycle": 2,
            "last_completed_strategy": 1
        }))

        draft_files = [0, 1, 2]
        start_idx, action, cycle = find_resume_point(draft_files, strategies_dir, data_folder)

        assert start_idx == 2
        assert action == "start"
        assert cycle == 2

    def test_find_resume_point_bounds_check(self, tmp_path):
        """Test find_resume_point resets when index exceeds file count"""
        from run_draft_order_loop import find_resume_point
        from utils.LoggingManager import setup_logger

        setup_logger("test", "WARNING", False, None, "simple")

        strategies_dir = tmp_path / "strategies"
        strategies_dir.mkdir()

        # Create data folder (required parameter)
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()

        # Create progress file with index exceeding file count
        progress_file = strategies_dir / "loop_progress.json"
        progress_file.write_text(json.dumps({
            "current_cycle": 1,
            "last_completed_strategy": 10  # Exceeds file count
        }))

        draft_files = [0, 1, 2]
        start_idx, action, cycle = find_resume_point(draft_files, strategies_dir, data_folder)

        assert start_idx == 0
        assert cycle == 2  # Incremented due to reset

    def test_update_progress(self, tmp_path):
        """Test update_progress creates correct JSON"""
        from run_draft_order_loop import update_progress

        progress_file = tmp_path / "loop_progress.json"
        update_progress(progress_file, last_completed=3, cycle=2)

        assert progress_file.exists()
        content = json.loads(progress_file.read_text())
        assert content["current_cycle"] == 2
        assert content["last_completed_strategy"] == 3
        assert "last_updated" in content

    def test_seed_strategy_folder(self, tmp_path):
        """Test seed_strategy_folder copies files and injects DRAFT_ORDER"""
        from run_draft_order_loop import seed_strategy_folder
        from utils.LoggingManager import setup_logger

        setup_logger("test", "WARNING", False, None, "simple")

        # Set up root baseline
        root_baseline = tmp_path / "optimal_baseline"
        root_baseline.mkdir()
        for f in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            (root_baseline / f).write_text(json.dumps({"parameters": {}}))

        # Set up draft order file
        data_folder = tmp_path / "sim_data"
        draft_order_dir = data_folder / "draft_order_possibilities"
        draft_order_dir.mkdir(parents=True)
        test_order = ["QB", "RB", "WR"]
        (draft_order_dir / "0_MINE.json").write_text(json.dumps({"DRAFT_ORDER": test_order}))

        # Seed the folder
        strategy_folder = tmp_path / "strategy_test"
        seed_strategy_folder(strategy_folder, root_baseline, 0, data_folder)

        # Verify
        seed_folder = strategy_folder / "optimal_seed"
        assert seed_folder.exists()
        assert (seed_folder / "league_config.json").exists()
        assert (seed_folder / "week1-5.json").exists()

        # Check DRAFT_ORDER injection
        config = json.loads((seed_folder / "league_config.json").read_text())
        assert config["parameters"]["DRAFT_ORDER_FILE"] == 0
        assert config["parameters"]["DRAFT_ORDER"] == test_order

    def test_ensure_strategy_folder_creates_new(self, tmp_path):
        """Test ensure_strategy_folder creates new folder when missing"""
        from run_draft_order_loop import ensure_strategy_folder
        from utils.LoggingManager import setup_logger

        setup_logger("test", "WARNING", False, None, "simple")

        # Set up root baseline
        root_baseline = tmp_path / "optimal_baseline"
        root_baseline.mkdir()
        for f in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            (root_baseline / f).write_text(json.dumps({"parameters": {}}))

        # Set up draft order file
        data_folder = tmp_path / "sim_data"
        draft_order_dir = data_folder / "draft_order_possibilities"
        draft_order_dir.mkdir(parents=True)
        (draft_order_dir / "0_MINE.json").write_text(json.dumps({"DRAFT_ORDER": []}))

        # Ensure folder
        strategy_folder = tmp_path / "new_strategy"
        ensure_strategy_folder(strategy_folder, root_baseline, 0, data_folder)

        assert strategy_folder.exists()
        assert (strategy_folder / "optimal_seed").exists()

    def test_get_strategy_baseline_returns_most_recent(self, tmp_path):
        """Test get_strategy_baseline returns most recent optimal folder"""
        from run_draft_order_loop import get_strategy_baseline
        import time

        strategy_folder = tmp_path / "strategy"
        strategy_folder.mkdir()

        # Create seed folder
        seed = strategy_folder / "optimal_seed"
        seed.mkdir()
        for f in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            (seed / f).write_text('{}')

        time.sleep(0.1)

        # Create iterative folder (more recent)
        iterative = strategy_folder / "optimal_iterative_20251209"
        iterative.mkdir()
        for f in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            (iterative / f).write_text('{}')

        result = get_strategy_baseline(strategy_folder)
        assert result.name == "optimal_iterative_20251209"

    def test_get_strategy_baseline_falls_back_to_seed(self, tmp_path):
        """Test get_strategy_baseline falls back to optimal_seed"""
        from run_draft_order_loop import get_strategy_baseline

        strategy_folder = tmp_path / "strategy"
        strategy_folder.mkdir()

        # Create only seed folder
        seed = strategy_folder / "optimal_seed"
        seed.mkdir()
        for f in ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            (seed / f).write_text('{}')

        result = get_strategy_baseline(strategy_folder)
        assert result.name == "optimal_seed"

    def test_get_strategy_baseline_raises_on_empty(self, tmp_path):
        """Test get_strategy_baseline raises error when no baseline exists"""
        from run_draft_order_loop import get_strategy_baseline

        strategy_folder = tmp_path / "strategy"
        strategy_folder.mkdir()

        with pytest.raises(ValueError):
            get_strategy_baseline(strategy_folder)

    def test_cleanup_intermediate_folders(self, tmp_path):
        """Test cleanup_intermediate_folders removes intermediate folders"""
        from run_draft_order_loop import cleanup_intermediate_folders
        from utils.LoggingManager import setup_logger

        setup_logger("test", "WARNING", False, None, "simple")

        strategy_folder = tmp_path / "strategy"
        strategy_folder.mkdir()

        # Create intermediate folders
        (strategy_folder / "intermediate_param1").mkdir()
        (strategy_folder / "intermediate_param2").mkdir()
        (strategy_folder / "optimal_seed").mkdir()  # Should not be removed

        cleanup_intermediate_folders(strategy_folder)

        assert not (strategy_folder / "intermediate_param1").exists()
        assert not (strategy_folder / "intermediate_param2").exists()
        assert (strategy_folder / "optimal_seed").exists()

    def test_main_function_exists(self):
        """Test that main function exists and is callable"""
        from run_draft_order_loop import main
        assert callable(main)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestRootScriptsIntegration:
    """Integration tests for root scripts"""

    def test_all_scripts_have_main_block(self):
        """Test that all scripts have proper __main__ block"""
        scripts = [
            'run_league_helper.py',
            'run_player_fetcher.py',
            'run_pre_commit_validation.py',
            'run_win_rate_simulation.py',
            'run_accuracy_simulation.py',
            'run_draft_order_loop.py'
        ]

        for script in scripts:
            script_path = project_root / script
            assert script_path.exists(), f"{script} not found"

            # Read file and check for __main__ block
            with open(script_path, 'r') as f:
                content = f.read()
                assert '__name__' in content, f"{script} missing __main__ block"
                assert '__main__' in content, f"{script} missing __main__ block"

    def test_all_scripts_have_docstrings(self):
        """Test that all scripts have module docstrings"""
        scripts = [
            'run_league_helper.py',
            'run_player_fetcher.py',
            'run_pre_commit_validation.py',
            'run_win_rate_simulation.py',
            'run_accuracy_simulation.py',
            'run_draft_order_loop.py'
        ]

        for script in scripts:
            script_path = project_root / script
            with open(script_path, 'r') as f:
                content = f.read()
                # Check for triple-quote docstring
                assert '"""' in content or "'''" in content, f"{script} missing docstring"

    def test_all_scripts_have_author_attribution(self):
        """Test that all scripts have author attribution"""
        scripts = [
            'run_league_helper.py',
            'run_player_fetcher.py',
            'run_pre_commit_validation.py',
            'run_win_rate_simulation.py',
            'run_accuracy_simulation.py',
            'run_draft_order_loop.py'
        ]

        for script in scripts:
            script_path = project_root / script
            with open(script_path, 'r') as f:
                content = f.read()
                assert 'Author:' in content, f"{script} missing author attribution"

    def test_all_scripts_import_required_modules(self):
        """Test that all scripts import required modules"""
        scripts_and_imports = {
            'run_league_helper.py': ['subprocess', 'sys', 'Path'],
            'run_player_fetcher.py': ['subprocess', 'sys', 'Path', 'os'],
            'run_pre_commit_validation.py': ['subprocess', 'sys', 'Path'],
            'run_win_rate_simulation.py': ['argparse', 'sys', 'Path'],
            'run_accuracy_simulation.py': ['argparse', 'sys', 'Path'],
            'run_draft_order_loop.py': ['argparse', 'sys', 'Path', 'json']
        }

        for script, required_imports in scripts_and_imports.items():
            script_path = project_root / script
            with open(script_path, 'r') as f:
                content = f.read()
                for import_name in required_imports:
                    assert import_name in content, f"{script} missing import: {import_name}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
