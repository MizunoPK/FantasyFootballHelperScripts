"""
Unit Tests for Config Cleanup Utilities

Tests the cleanup_old_optimal_folders function for:
- No cleanup when under limit
- Deletes oldest when at limit
- Handles deletion errors gracefully
- Only matches optimal_* pattern

Author: Kai Mizuno
"""

import pytest
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add simulation directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "simulation"))
from config_cleanup import cleanup_old_optimal_folders, MAX_OPTIMAL_FOLDERS


class TestCleanupOldOptimalFolders:
    """Tests for cleanup_old_optimal_folders function."""

    def test_no_cleanup_when_under_limit(self, tmp_path):
        """Should not delete any folders when count is under limit."""
        # Create 3 optimal folders (under default limit of 5)
        for i in range(3):
            (tmp_path / f"optimal_2025010{i}_120000").mkdir()

        deleted = cleanup_old_optimal_folders(tmp_path)

        assert deleted == 0
        assert len(list(tmp_path.glob("optimal_*"))) == 3

    def test_no_cleanup_when_at_limit_minus_one(self, tmp_path):
        """Should not delete when count is exactly limit - 1."""
        # Create 4 folders (one less than limit of 5)
        for i in range(4):
            (tmp_path / f"optimal_2025010{i}_120000").mkdir()

        deleted = cleanup_old_optimal_folders(tmp_path)

        assert deleted == 0
        assert len(list(tmp_path.glob("optimal_*"))) == 4

    def test_deletes_oldest_when_at_limit(self, tmp_path):
        """Should delete oldest folder when count equals limit."""
        # Create 5 folders (at limit)
        folders = []
        for i in range(5):
            folder = tmp_path / f"optimal_2025010{i}_120000"
            folder.mkdir()
            folders.append(folder)

        deleted = cleanup_old_optimal_folders(tmp_path)

        assert deleted == 1
        assert not folders[0].exists()  # Oldest deleted
        assert all(f.exists() for f in folders[1:])  # Rest remain
        assert len(list(tmp_path.glob("optimal_*"))) == 4

    def test_deletes_multiple_when_over_limit(self, tmp_path):
        """Should delete multiple folders when count exceeds limit."""
        # Create 7 folders (2 over limit)
        folders = []
        for i in range(7):
            folder = tmp_path / f"optimal_2025010{i}_120000"
            folder.mkdir()
            folders.append(folder)

        deleted = cleanup_old_optimal_folders(tmp_path)

        assert deleted == 3  # Need to delete 3 to get to 4 (room for new one)
        assert not folders[0].exists()
        assert not folders[1].exists()
        assert not folders[2].exists()
        assert all(f.exists() for f in folders[3:])
        assert len(list(tmp_path.glob("optimal_*"))) == 4

    def test_respects_custom_limit(self, tmp_path):
        """Should respect custom max_folders parameter."""
        # Create 4 folders
        for i in range(4):
            (tmp_path / f"optimal_2025010{i}_120000").mkdir()

        # With limit of 2, should delete 3 folders
        deleted = cleanup_old_optimal_folders(tmp_path, max_folders=2)

        assert deleted == 3
        assert len(list(tmp_path.glob("optimal_*"))) == 1

    def test_only_matches_optimal_pattern(self, tmp_path):
        """Should only count/delete folders matching optimal_* pattern."""
        # Create mix of folder types
        (tmp_path / "optimal_20250101_120000").mkdir()
        (tmp_path / "optimal_20250102_120000").mkdir()
        (tmp_path / "intermediate_01_TEST").mkdir()
        (tmp_path / "other_folder").mkdir()

        deleted = cleanup_old_optimal_folders(tmp_path, max_folders=2)

        assert deleted == 1
        # Only optimal folders should be affected
        assert not (tmp_path / "optimal_20250101_120000").exists()
        assert (tmp_path / "optimal_20250102_120000").exists()
        # Non-optimal folders should remain
        assert (tmp_path / "intermediate_01_TEST").exists()
        assert (tmp_path / "other_folder").exists()

    def test_sorts_by_name_for_oldest(self, tmp_path):
        """Should determine oldest by alphabetical sort of folder names."""
        # Create folders out of order
        (tmp_path / "optimal_20250103_120000").mkdir()
        (tmp_path / "optimal_20250101_120000").mkdir()  # Oldest
        (tmp_path / "optimal_20250102_120000").mkdir()
        (tmp_path / "optimal_20250105_120000").mkdir()
        (tmp_path / "optimal_20250104_120000").mkdir()

        deleted = cleanup_old_optimal_folders(tmp_path)

        assert deleted == 1
        # The alphabetically first (oldest) should be deleted
        assert not (tmp_path / "optimal_20250101_120000").exists()
        assert (tmp_path / "optimal_20250102_120000").exists()

    def test_handles_iterative_folder_names(self, tmp_path):
        """Should handle optimal_iterative_* folder naming pattern."""
        (tmp_path / "optimal_iterative_20250101_120000").mkdir()
        (tmp_path / "optimal_iterative_20250102_120000").mkdir()
        (tmp_path / "optimal_iterative_20250103_120000").mkdir()
        (tmp_path / "optimal_iterative_20250104_120000").mkdir()
        (tmp_path / "optimal_iterative_20250105_120000").mkdir()

        deleted = cleanup_old_optimal_folders(tmp_path)

        assert deleted == 1
        assert not (tmp_path / "optimal_iterative_20250101_120000").exists()

    def test_handles_nonexistent_directory(self, tmp_path):
        """Should return 0 when directory doesn't exist."""
        nonexistent = tmp_path / "does_not_exist"

        deleted = cleanup_old_optimal_folders(nonexistent)

        assert deleted == 0

    def test_handles_empty_directory(self, tmp_path):
        """Should return 0 when directory is empty."""
        deleted = cleanup_old_optimal_folders(tmp_path)

        assert deleted == 0

    @patch('shutil.rmtree')
    def test_continues_on_deletion_error(self, mock_rmtree, tmp_path):
        """Should log warning and continue if deletion fails."""
        # Create 6 folders
        for i in range(6):
            (tmp_path / f"optimal_2025010{i}_120000").mkdir()

        # Make rmtree fail for first call, succeed for second
        mock_rmtree.side_effect = [PermissionError("Access denied"), None]

        deleted = cleanup_old_optimal_folders(tmp_path)

        # Should have attempted to delete 2 folders
        assert mock_rmtree.call_count == 2
        # Only 1 successful deletion
        assert deleted == 1

    def test_ignores_files_matching_pattern(self, tmp_path):
        """Should only count directories, not files matching pattern."""
        # Create folders
        for i in range(4):
            (tmp_path / f"optimal_2025010{i}_120000").mkdir()

        # Create a file matching the pattern (should be ignored)
        (tmp_path / "optimal_20250105_120000.json").touch()

        deleted = cleanup_old_optimal_folders(tmp_path)

        assert deleted == 0  # 4 folders, under limit of 5
        assert (tmp_path / "optimal_20250105_120000.json").exists()


class TestMaxOptimalFoldersConstant:
    """Tests for MAX_OPTIMAL_FOLDERS constant."""

    def test_default_value_is_five(self):
        """Verify default constant is 5."""
        assert MAX_OPTIMAL_FOLDERS == 5
