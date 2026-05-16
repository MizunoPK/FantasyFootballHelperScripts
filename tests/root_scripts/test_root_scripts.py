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


