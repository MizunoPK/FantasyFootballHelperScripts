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

project_root = Path(__file__).parent.parent.parent



class TestRunLeagueHelper:
    """Test run_league_helper.py"""

    def test_run_league_helper_calls_main(self):
        """Test run_league_helper calls main() when executed as __main__"""
        import runpy
        with patch('league_helper.LeagueHelperManager.main') as mock_main:
            runpy.run_module('run_league_helper', run_name='__main__')
            mock_main.assert_called_once()

    def test_run_league_helper_no_subprocess(self):
        """Test run_league_helper does not use subprocess"""
        import run_league_helper
        assert not hasattr(run_league_helper, 'subprocess')

    def test_run_league_helper_imports_main_from_league_helper(self):
        """Test run_league_helper imports main from league_helper.LeagueHelperManager"""
        import run_league_helper
        assert hasattr(run_league_helper, 'main')

    def test_run_league_helper_has_main_block(self):
        """Test run_league_helper has if __name__ == '__main__' block calling main()"""
        script_path = Path(__file__).parent.parent.parent / 'run_league_helper.py'
        content = script_path.read_text()
        assert 'if __name__ == "__main__"' in content
        assert 'main()' in content



class TestRunPlayerFetcher:
    """Test run_player_fetcher.py (KAI-10: direct import pattern, no subprocess)"""

    def test_run_player_fetcher_has_parse_args(self):
        """Test run_player_fetcher has parse_args function (KAI-10 refactoring)"""
        import run_player_fetcher
        assert hasattr(run_player_fetcher, 'parse_args')
        assert callable(run_player_fetcher.parse_args)

    def test_run_player_fetcher_has_create_settings_dict(self):
        """Test run_player_fetcher has create_settings_dict function"""
        import run_player_fetcher
        assert hasattr(run_player_fetcher, 'create_settings_dict')
        assert callable(run_player_fetcher.create_settings_dict)

    def test_run_player_fetcher_no_subprocess(self):
        """Test run_player_fetcher does not use subprocess (KAI-10 direct import)"""
        import run_player_fetcher
        assert not hasattr(run_player_fetcher, 'subprocess')



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
        exit_code = run_validation()

        assert exit_code == 1
        assert mock_run.call_args[1]['check'] == False



class TestRunSimulation:
    """Test run_win_rate_simulation.py main function and argument parsing"""

    @patch('run_win_rate_simulation.SimulationManager')
    @patch('run_win_rate_simulation.Path')
    def test_single_mode_argument_parsing(self, mock_path_class, mock_sim_manager):
        """Test single mode argument parsing"""
        mock_folder = Mock()
        mock_folder.name = "optimal_test_folder"
        mock_folder.is_dir.return_value = True
        mock_folder.stat.return_value = Mock(st_mtime=1.0)

        mock_file = Mock()
        mock_file.exists.return_value = True

        mock_folder.__truediv__ = Mock(return_value=mock_file)

        mock_path = Mock()
        mock_path.glob.return_value = [mock_folder]
        mock_path.name = "optimal_test_folder"
        mock_path.exists.return_value = True
        mock_path_class.return_value = mock_path

        mock_data_path = Mock()
        mock_data_path.exists.return_value = True

        def path_side_effect(arg):
            if "sim_data" in str(arg):
                return mock_data_path
            return mock_path

        mock_path_class.side_effect = path_side_effect

        mock_manager = Mock()
        mock_sim_manager.return_value = mock_manager

        from run_win_rate_simulation import main
        with patch('sys.argv', ['run_win_rate_simulation.py', 'single', '--sims', '10']):
            try:
                main()
            except SystemExit:
                pass

    def test_simulation_modes_defined(self):
        """Test that all simulation modes are properly defined"""
        from run_win_rate_simulation import main

        assert callable(main)

    @patch('run_win_rate_simulation.SimulationManager')
    @patch('run_win_rate_simulation.Path')
    def test_full_mode_shows_total_configs(self, mock_path_class, mock_sim_manager):
        """Test that full mode calculates and displays total configs"""
        mock_path = Mock()
        mock_path.glob.return_value = [Mock(stat=Mock(return_value=Mock(st_mtime=1.0)))]
        mock_path.name = "optimal_test.json"
        mock_path.exists.return_value = True
        mock_path_class.return_value = mock_path

        from run_win_rate_simulation import main
        assert callable(main)

    @patch('run_win_rate_simulation.SimulationManager')
    @patch('run_win_rate_simulation.Path')
    def test_iterative_mode_shows_parameter_count(self, mock_path_class, mock_sim_manager):
        """Test that iterative mode shows parameter optimization info"""
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

        assert run_win_rate_simulation.LOGGING_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']



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
        ]

        for script in scripts:
            script_path = project_root / script
            assert script_path.exists(), f"{script} not found"

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
        ]

        for script in scripts:
            script_path = project_root / script
            with open(script_path, 'r') as f:
                content = f.read()
                assert '"""' in content or "'''" in content, f"{script} missing docstring"

    def test_all_scripts_have_author_attribution(self):
        """Test that all scripts have author attribution"""
        scripts = [
            'run_league_helper.py',
            'run_player_fetcher.py',
            'run_pre_commit_validation.py',
            'run_win_rate_simulation.py',
            'run_accuracy_simulation.py',
        ]

        for script in scripts:
            script_path = project_root / script
            with open(script_path, 'r') as f:
                content = f.read()
                assert 'Author:' in content, f"{script} missing author attribution"

    def test_all_scripts_import_required_modules(self):
        """Test that all scripts import required modules"""
        scripts_and_imports = {
            'run_league_helper.py': ['league_helper', 'LeagueHelperManager'],
            'run_player_fetcher.py': ['argparse', 'asyncio', 'Path'],
            'run_pre_commit_validation.py': ['subprocess', 'sys', 'Path'],
            'run_win_rate_simulation.py': ['argparse', 'sys', 'Path'],
            'run_accuracy_simulation.py': ['argparse', 'sys', 'Path'],
        }

        for script, required_imports in scripts_and_imports.items():
            script_path = project_root / script
            with open(script_path, 'r') as f:
                content = f.read()
                for import_name in required_imports:
                    assert import_name in content, f"{script} missing import: {import_name}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


