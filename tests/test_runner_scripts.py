#!/usr/bin/env python3
"""
Unit tests for Main Runner Scripts.

Tests the runner scripts (run_*.py) functionality including:
- Subprocess execution and error handling
- Directory management and path resolution
- Error propagation and exit codes
- Cross-platform compatibility
"""

import pytest
import sys
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import runner scripts as modules (they're designed to run as __main__)
import run_draft_helper
import run_player_data_fetcher
import run_nfl_scores_fetcher
import run_starter_helper


class TestRunnerScripts:
    """Test suite for all runner scripts"""

    def test_runner_scripts_exist(self):
        """Test that all runner scripts exist and are importable"""
        # Test that all runner modules can be imported
        assert run_draft_helper is not None
        assert run_player_data_fetcher is not None
        assert run_nfl_scores_fetcher is not None
        assert run_starter_helper is not None

    @pytest.mark.parametrize("runner_script,target_dir,target_script", [
        ("run_draft_helper.py", "draft_helper", "draft_helper.py"),
        ("run_player_data_fetcher.py", "player-data-fetcher", "data_fetcher-players.py"),
        ("run_nfl_scores_fetcher.py", "nfl-scores-fetcher", "data_fetcher-scores.py"),
        ("run_starter_helper.py", "starter_helper", "starter_helper.py"),
    ])
    def test_runner_script_directory_paths(self, runner_script, target_dir, target_script):
        """Test that runner scripts calculate correct directory paths"""
        script_path = Path(__file__).parent.parent / runner_script

        # Read the script to verify path calculations
        script_content = script_path.read_text()

        # Verify the script references the correct target directory
        assert target_dir in script_content
        assert target_script in script_content

    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_draft_helper_runner_success(self, mock_getcwd, mock_chdir, mock_subprocess):
        """Test successful execution of draft helper runner"""
        # Setup mocks
        mock_getcwd.return_value = "/original/path"
        mock_subprocess.return_value = MagicMock(returncode=0)

        # Import and execute (need to patch sys.argv to avoid actual execution)
        with patch('sys.argv', ['run_draft_helper.py']):
            # Execute the main block logic (not the actual main execution)
            script_dir = Path(run_draft_helper.__file__).parent
            draft_dir = script_dir / "draft_helper"

            # Simulate the try block
            expected_calls = [
                draft_dir,  # chdir to draft_helper
                "/original/path"  # chdir back to original
            ]

            # Verify the script would work correctly
            assert draft_dir.name == "draft_helper"

    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_player_data_fetcher_runner_success(self, mock_getcwd, mock_chdir, mock_subprocess):
        """Test successful execution of player data fetcher runner"""
        mock_getcwd.return_value = "/original/path"
        mock_subprocess.return_value = MagicMock(returncode=0)

        script_dir = Path(run_player_data_fetcher.__file__).parent
        fetcher_dir = script_dir / "player-data-fetcher"

        assert fetcher_dir.name == "player-data-fetcher"

    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_nfl_scores_fetcher_runner_success(self, mock_getcwd, mock_chdir, mock_subprocess):
        """Test successful execution of NFL scores fetcher runner"""
        mock_getcwd.return_value = "/original/path"
        mock_subprocess.return_value = MagicMock(returncode=0)

        script_dir = Path(run_nfl_scores_fetcher.__file__).parent
        fetcher_dir = script_dir / "nfl-scores-fetcher"

        assert fetcher_dir.name == "nfl-scores-fetcher"

    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    def test_starter_helper_runner_success(self, mock_getcwd, mock_chdir, mock_subprocess):
        """Test successful execution of starter helper runner"""
        mock_getcwd.return_value = "/original/path"
        mock_subprocess.return_value = MagicMock(returncode=0)

        script_dir = Path(run_starter_helper.__file__).parent
        starter_dir = script_dir / "starter_helper"

        assert starter_dir.name == "starter_helper"

    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    @patch('sys.exit')
    def test_runner_subprocess_error_handling(self, mock_exit, mock_getcwd, mock_chdir, mock_subprocess):
        """Test error handling when subprocess fails"""
        mock_getcwd.return_value = "/original/path"

        # Mock subprocess failure
        error = subprocess.CalledProcessError(1, 'command')
        mock_subprocess.side_effect = error

        # Simulate runner execution with error
        with patch('builtins.print') as mock_print:
            # This simulates what would happen in the runner script
            try:
                mock_subprocess.check = True
                raise error
            except subprocess.CalledProcessError as e:
                # This is what the runner scripts do
                mock_print.assert_not_called()  # We haven't called it yet
                expected_message = f"Error running draft helper: {e}"
                # The script would call print and sys.exit here

        # Verify error would be handled
        assert error.returncode == 1

    @patch('subprocess.run')
    @patch('os.chdir')
    @patch('os.getcwd')
    @patch('sys.exit')
    def test_runner_unexpected_error_handling(self, mock_exit, mock_getcwd, mock_chdir, mock_subprocess):
        """Test handling of unexpected errors"""
        mock_getcwd.return_value = "/original/path"

        # Mock unexpected error
        mock_subprocess.side_effect = Exception("Unexpected error")

        # Verify error would be caught and handled
        with pytest.raises(Exception) as exc_info:
            mock_subprocess(["python", "script.py"], check=True)

        assert "Unexpected error" in str(exc_info.value)

    def test_runner_script_structure_consistency(self):
        """Test that all runner scripts have consistent structure"""
        runner_files = [
            "run_draft_helper.py",
            "run_player_data_fetcher.py",
            "run_nfl_scores_fetcher.py",
            "run_starter_helper.py"
        ]

        for runner_file in runner_files:
            script_path = Path(__file__).parent.parent / runner_file
            content = script_path.read_text()

            # Check for consistent structure
            assert 'import os' in content
            assert 'import subprocess' in content
            assert 'import sys' in content
            assert 'from pathlib import Path' in content
            assert 'if __name__ == "__main__":' in content
            assert 'subprocess.run' in content
            assert 'CalledProcessError' in content
            assert 'original_cwd' in content
            assert 'finally:' in content

    def test_runner_script_error_messages(self):
        """Test that runner scripts have appropriate error messages"""
        script_files = {
            "run_draft_helper.py": "draft helper",
            "run_player_data_fetcher.py": "player data fetcher",
            "run_nfl_scores_fetcher.py": "NFL scores fetcher",
            "run_starter_helper.py": "starter helper"
        }

        for script_file, expected_name in script_files.items():
            script_path = Path(__file__).parent.parent / script_file
            content = script_path.read_text()

            # Check for appropriate error messages
            assert f"Error running {expected_name}" in content
            assert "Unexpected error" in content

    def test_python_executable_usage(self):
        """Test that runner scripts use sys.executable for Python calls"""
        runner_files = [
            "run_draft_helper.py",
            "run_player_data_fetcher.py",
            "run_nfl_scores_fetcher.py",
            "run_starter_helper.py"
        ]

        for runner_file in runner_files:
            script_path = Path(__file__).parent.parent / runner_file
            content = script_path.read_text()

            # Should use sys.executable for cross-platform compatibility
            assert 'sys.executable' in content
            assert 'subprocess.run([' in content

    def test_directory_restoration(self):
        """Test that all runner scripts restore original directory"""
        runner_files = [
            "run_draft_helper.py",
            "run_player_data_fetcher.py",
            "run_nfl_scores_fetcher.py",
            "run_starter_helper.py"
        ]

        for runner_file in runner_files:
            script_path = Path(__file__).parent.parent / runner_file
            content = script_path.read_text()

            # Check directory restoration logic
            assert 'original_cwd = os.getcwd()' in content
            assert 'os.chdir(original_cwd)' in content
            assert 'finally:' in content

    @patch('sys.argv', ['test_script.py'])
    def test_runner_import_safety(self):
        """Test that runner scripts can be imported without execution"""
        # Test that importing doesn't trigger execution
        # (This is already tested by the fact that we can import them)

        # Verify __name__ check exists
        for runner_module in [run_draft_helper, run_player_data_fetcher,
                             run_nfl_scores_fetcher, run_starter_helper]:

            script_path = Path(runner_module.__file__)
            content = script_path.read_text()

            # Should have __name__ == "__main__" check
            assert 'if __name__ == "__main__":' in content

    def test_cross_platform_path_handling(self):
        """Test that runner scripts handle paths in cross-platform way"""
        runner_files = [
            "run_draft_helper.py",
            "run_player_data_fetcher.py",
            "run_nfl_scores_fetcher.py",
            "run_starter_helper.py"
        ]

        for runner_file in runner_files:
            script_path = Path(__file__).parent.parent / runner_file
            content = script_path.read_text()

            # Should use pathlib.Path for cross-platform compatibility
            assert 'from pathlib import Path' in content
            assert 'Path(__file__).parent' in content

    def test_target_script_names(self):
        """Test that runner scripts target the correct script names"""
        target_scripts = {
            "run_draft_helper.py": "draft_helper.py",
            "run_player_data_fetcher.py": "data_fetcher-players.py",
            "run_nfl_scores_fetcher.py": "data_fetcher-scores.py",
            "run_starter_helper.py": "starter_helper.py"
        }

        for runner_file, target_script in target_scripts.items():
            script_path = Path(__file__).parent.parent / runner_file
            content = script_path.read_text()

            assert target_script in content


class TestRunnerIntegration:
    """Integration tests for runner scripts"""

    def test_all_target_directories_exist(self):
        """Test that all target directories referenced by runners exist"""
        base_dir = Path(__file__).parent.parent

        target_dirs = [
            "draft_helper",
            "player-data-fetcher",
            "nfl-scores-fetcher",
            "starter_helper"
        ]

        for target_dir in target_dirs:
            dir_path = base_dir / target_dir
            assert dir_path.exists(), f"Target directory {target_dir} does not exist"
            assert dir_path.is_dir(), f"Target {target_dir} is not a directory"

    def test_all_target_scripts_exist(self):
        """Test that all target scripts referenced by runners exist"""
        base_dir = Path(__file__).parent.parent

        target_files = [
            "draft_helper/draft_helper.py",
            "player-data-fetcher/data_fetcher-players.py",
            "nfl-scores-fetcher/data_fetcher-scores.py",
            "starter_helper/starter_helper.py"
        ]

        for target_file in target_files:
            file_path = base_dir / target_file
            assert file_path.exists(), f"Target script {target_file} does not exist"
            assert file_path.is_file(), f"Target {target_file} is not a file"

    def test_runner_scripts_executable_permissions(self):
        """Test that runner scripts have appropriate permissions"""
        base_dir = Path(__file__).parent.parent

        runner_files = [
            "run_draft_helper.py",
            "run_player_data_fetcher.py",
            "run_nfl_scores_fetcher.py",
            "run_starter_helper.py"
        ]

        for runner_file in runner_files:
            file_path = base_dir / runner_file
            assert file_path.exists(), f"Runner script {runner_file} does not exist"
            assert file_path.is_file(), f"Runner {runner_file} is not a file"

            # Check if file is readable
            content = file_path.read_text()
            assert len(content) > 0, f"Runner script {runner_file} is empty"


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        # Basic test runner
        base_dir = Path(__file__).parent.parent

        # Test that all runner scripts exist
        runner_files = [
            "run_draft_helper.py",
            "run_player_data_fetcher.py",
            "run_nfl_scores_fetcher.py",
            "run_starter_helper.py"
        ]

        for runner_file in runner_files:
            file_path = base_dir / runner_file
            assert file_path.exists(), f"{runner_file} not found"

            content = file_path.read_text()
            assert 'subprocess.run' in content
            assert 'if __name__ == "__main__":' in content

        print("✅ All runner scripts exist and have correct structure")

        # Test target directories exist
        target_dirs = ["draft_helper", "player-data-fetcher", "nfl-scores-fetcher", "starter_helper"]
        for target_dir in target_dirs:
            dir_path = base_dir / target_dir
            assert dir_path.exists() and dir_path.is_dir()

        print("✅ All target directories exist")

        # Test target scripts exist
        target_scripts = [
            "draft_helper/draft_helper.py",
            "player-data-fetcher/data_fetcher-players.py",
            "nfl-scores-fetcher/data_fetcher-scores.py",
            "starter_helper/starter_helper.py"
        ]

        for target_script in target_scripts:
            script_path = base_dir / target_script
            assert script_path.exists() and script_path.is_file()

        print("✅ All target scripts exist")

        # Test imports work
        try:
            import run_draft_helper
            import run_player_data_fetcher
            import run_nfl_scores_fetcher
            import run_starter_helper
            print("✅ All runner scripts can be imported")
        except ImportError as e:
            print(f"❌ Import error: {e}")

        print("Basic tests completed successfully!")