"""
Config Cleanup Utilities

Provides automatic cleanup of old optimal configuration folders to prevent
unbounded growth of saved configurations.

Supports both win-rate simulation (optimal_*) and accuracy simulation
(accuracy_optimal_*) folder patterns.

Author: Kai Mizuno
"""

import shutil
from pathlib import Path
from typing import List

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger

# Maximum number of optimal folders to keep per type
MAX_OPTIMAL_FOLDERS = 5


def cleanup_old_optimal_folders(config_dir: Path, max_folders: int = MAX_OPTIMAL_FOLDERS) -> int:
    """
    Delete oldest optimal_* folders when count exceeds limit.

    Checks the config directory for folders matching 'optimal_*' pattern
    (but NOT 'accuracy_optimal_*' which is handled separately).
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

    # Find all optimal_* folders (excluding accuracy_optimal_*)
    optimal_folders: List[Path] = sorted([
        p for p in config_dir.iterdir()
        if p.is_dir() and p.name.startswith("optimal_") and not p.name.startswith("accuracy_optimal_")
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


def cleanup_old_accuracy_optimal_folders(config_dir: Path, max_folders: int = MAX_OPTIMAL_FOLDERS) -> int:
    """
    Delete oldest accuracy_optimal_* folders when count exceeds limit.

    Checks the config directory for folders matching 'accuracy_optimal_*' pattern.
    If the count is >= max_folders, deletes the oldest folders (by name,
    which contains sortable timestamps) until count < max_folders.

    Args:
        config_dir: Directory containing accuracy_optimal_* folders
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

    # Find all accuracy_optimal_* folders
    accuracy_folders: List[Path] = sorted([
        p for p in config_dir.iterdir()
        if p.is_dir() and p.name.startswith("accuracy_optimal_")
    ])

    deleted_count = 0

    # Delete oldest folders until we're under the limit
    # We need to delete enough to make room for the new folder
    while len(accuracy_folders) >= max_folders:
        oldest = accuracy_folders.pop(0)  # Remove from sorted list (oldest first)
        try:
            shutil.rmtree(oldest)
            logger.info(f"Deleted old accuracy optimal folder: {oldest.name}")
            deleted_count += 1
        except Exception as e:
            logger.warning(f"Failed to delete {oldest.name}: {e}")
            # Continue anyway - don't block new folder creation

    return deleted_count
