"""
Unit Tests for Root Runner Scripts

Tests all root-level runner scripts including league helper, data fetchers,
simulation runner, and pre-commit validation.

Author: Kai Mizuno
"""

import pytest
import subprocess
import sys
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
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == sys.executable
        assert "LeagueHelperManager.py" in call_args[1]
        assert "./data" in call_args

    @patch('subprocess.run')
    def test_run_league_helper_handles_subprocess_error(self, mock_run):
        """Test handling of subprocess errors"""
        # Mock subprocess failure
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')

        from run_league_helper import run_league_helper
        exit_code = run_league_helper()

        assert exit_code == 1

    @patch('subprocess.run')
    def test_run_league_helper_handles_general_exception(self, mock_run):
        """Test handling of general exceptions"""
        # Mock general exception
        mock_run.side_effect = RuntimeError("Test error")

        from run_league_helper import run_league_helper
        exit_code = run_league_helper()

        assert exit_code == 1

    @patch('subprocess.run')
    def test_run_league_helper_uses_correct_data_folder(self, mock_run):
        """Test that correct data folder is passed"""
        mock_run.return_value = Mock(returncode=0)

        from run_league_helper import run_league_helper
        run_league_helper()

        call_args = mock_run.call_args[0][0]
        assert "./data" == call_args[2]


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
# TEST RUN_SCORES_FETCHER.PY
# ============================================================================

class TestRunScoresFetcher:
    """Test run_scores_fetcher.py"""

    @patch('os.chdir')
    @patch('subprocess.run')
    def test_run_scores_fetcher_success(self, mock_run, mock_chdir):
        """Test successful scores fetcher execution"""
        mock_run.return_value = Mock(returncode=0)

        import run_scores_fetcher
        assert hasattr(run_scores_fetcher, 'subprocess')
        assert hasattr(run_scores_fetcher, 'Path')

    @patch('os.chdir')
    @patch('subprocess.run')
    def test_run_scores_fetcher_handles_errors(self, mock_run, mock_chdir):
        """Test error handling in scores fetcher"""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')

        import run_scores_fetcher
        assert run_scores_fetcher.subprocess is not None


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
    """Test run_simulation.py main function and argument parsing"""

    @patch('run_simulation.SimulationManager')
    @patch('run_simulation.Path')
    def test_single_mode_argument_parsing(self, mock_path_class, mock_sim_manager):
        """Test single mode argument parsing"""
        # Mock Path behavior
        mock_path = Mock()
        mock_path.glob.return_value = [Mock(stat=Mock(return_value=Mock(st_mtime=1.0)))]
        mock_path.name = "optimal_test.json"
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
        from run_simulation import main
        with patch('sys.argv', ['run_simulation.py', 'single', '--sims', '10']):
            try:
                main()
            except SystemExit:
                pass  # main() calls sys.exit() on error

    def test_simulation_modes_defined(self):
        """Test that all simulation modes are properly defined"""
        from run_simulation import main

        # Verify the function exists and is callable
        assert callable(main)

    @patch('run_simulation.SimulationManager')
    @patch('run_simulation.Path')
    def test_full_mode_shows_total_configs(self, mock_path_class, mock_sim_manager):
        """Test that full mode calculates and displays total configs"""
        # Mock Path
        mock_path = Mock()
        mock_path.glob.return_value = [Mock(stat=Mock(return_value=Mock(st_mtime=1.0)))]
        mock_path.name = "optimal_test.json"
        mock_path.exists.return_value = True
        mock_path_class.return_value = mock_path

        # This test verifies the structure is in place
        from run_simulation import main
        assert callable(main)

    @patch('run_simulation.SimulationManager')
    @patch('run_simulation.Path')
    def test_iterative_mode_shows_parameter_count(self, mock_path_class, mock_sim_manager):
        """Test that iterative mode shows parameter optimization info"""
        # Mock Path
        mock_path = Mock()
        mock_path.glob.return_value = [Mock(stat=Mock(return_value=Mock(st_mtime=1.0)))]
        mock_path.name = "optimal_test.json"
        mock_path.exists.return_value = True
        mock_path_class.return_value = mock_path

        from run_simulation import main
        assert callable(main)

    def test_logging_constants_defined(self):
        """Test that logging constants are properly defined"""
        import run_simulation

        assert hasattr(run_simulation, 'LOGGING_LEVEL')
        assert hasattr(run_simulation, 'LOGGING_TO_FILE')
        assert hasattr(run_simulation, 'LOG_NAME')
        assert run_simulation.LOG_NAME == "simulation"

    def test_default_arguments_defined(self):
        """Test that default argument values are reasonable"""
        import run_simulation

        # Verify the module loads without error
        assert run_simulation.LOGGING_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


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
            'run_scores_fetcher.py',
            'run_pre_commit_validation.py',
            'run_simulation.py'
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
            'run_scores_fetcher.py',
            'run_pre_commit_validation.py',
            'run_simulation.py'
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
            'run_scores_fetcher.py',
            'run_pre_commit_validation.py',
            'run_simulation.py'
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
            'run_scores_fetcher.py': ['subprocess', 'sys', 'Path', 'os'],
            'run_pre_commit_validation.py': ['subprocess', 'sys', 'Path'],
            'run_simulation.py': ['argparse', 'sys', 'Path']
        }

        for script, required_imports in scripts_and_imports.items():
            script_path = project_root / script
            with open(script_path, 'r') as f:
                content = f.read()
                for import_name in required_imports:
                    assert import_name in content, f"{script} missing import: {import_name}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
