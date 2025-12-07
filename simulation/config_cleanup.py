"""
Config Cleanup Utilities

Provides automatic cleanup of old optimal configuration folders to prevent
unbounded growth of saved configurations.

Author: Kai Mizuno
"""

import shutil
from pathlib import Path
from typing import List

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger

# Maximum number of optimal_* folders to keep
MAX_OPTIMAL_FOLDERS = 5


def cleanup_old_optimal_folders(config_dir: Path, max_folders: int = MAX_OPTIMAL_FOLDERS) -> int:
    """
    Delete oldest optimal_* folders when count exceeds limit.

    Checks the config directory for folders matching 'optimal_*' pattern.
    If the count is >= max_folders, deletes the oldest folders (by name,
    which contains sortable timestamps) until count < max_folders.

    Args:
        config_dir: Directory containing optimal_* folders
        max_folders: Maximum folders to keep (default: 5)

    Returns:
        Number of folders deleted

    Note:
        Deletion failures are logged as warnings but don't raise exceptions.
        This ensures folder creation can proceed even if cleanup fails.
    """
    logger = get_logger()

    if not config_dir.exists():
        return 0

    # Find all optimal_* folders
    optimal_folders: List[Path] = sorted([
        p for p in config_dir.iterdir()
        if p.is_dir() and p.name.startswith("optimal_")
    ])

    deleted_count = 0

    # Delete oldest folders until we're under the limit
    # We need to delete enough to make room for the new folder
    while len(optimal_folders) >= max_folders:
        oldest = optimal_folders.pop(0)  # Remove from sorted list (oldest first)
        try:
            shutil.rmtree(oldest)
            logger.info(f"Deleted old optimal folder: {oldest.name}")
            deleted_count += 1
        except Exception as e:
            logger.warning(f"Failed to delete {oldest.name}: {e}")
            # Continue anyway - don't block new folder creation

    return deleted_count
