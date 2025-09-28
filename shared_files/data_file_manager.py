#!/usr/bin/env python3
"""
Data File Manager - Automatic File Cap Enforcement

This module provides automatic cleanup of data files to maintain configurable limits
on the number of files of each type in data folders. When caps are exceeded, the
oldest files are automatically deleted to make room for new ones.

Usage:
    from shared_files.data_file_manager import DataFileManager
    from shared_config import DEFAULT_FILE_CAPS

    manager = DataFileManager('path/to/data/folder', DEFAULT_FILE_CAPS)
    manager.enforce_file_caps('newly_created_file.csv')

Author: Generated for Fantasy Football Helper Scripts
Last Updated: September 2025
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from shared_files.logging_utils import setup_module_logging

# Set up logging
logger = setup_module_logging(__name__)


class DataFileManager:
    """
    Manages file caps in data directories to prevent unlimited accumulation of files.

    Features:
    - Configurable caps per file type (csv, json, xlsx, txt)
    - Automatic deletion of oldest files when caps are exceeded
    - Safe operation with comprehensive logging
    - Dry-run mode for testing
    - Module-specific cap overrides
    """

    def __init__(self, data_folder_path: str, file_caps: Optional[Dict[str, int]] = None):
        """
        Initialize DataFileManager for a specific data folder.

        Args:
            data_folder_path: Path to the data folder to manage
            file_caps: Dictionary of file type caps (e.g., {'csv': 5, 'json': 5})
                      If None, will try to import from shared_config
        """
        self.data_folder = Path(data_folder_path)

        # Import default caps if not provided
        if file_caps is None:
            try:
                from shared_config import DEFAULT_FILE_CAPS
                file_caps = DEFAULT_FILE_CAPS
            except ImportError:
                logger.warning("Could not import DEFAULT_FILE_CAPS, using built-in defaults")
                file_caps = {'csv': 5, 'json': 5, 'xlsx': 5, 'txt': 5}

        self.file_caps = file_caps

        # Create data folder if it doesn't exist
        self.data_folder.mkdir(parents=True, exist_ok=True)

        logger.info(f"DataFileManager initialized for {self.data_folder} with caps: {self.file_caps}")

    def get_files_by_type(self, file_extension: str) -> List[Path]:
        """
        Get all files of a specific type, sorted by modification time (oldest first).

        Args:
            file_extension: File extension without dot (e.g., 'csv', 'json')

        Returns:
            List of Path objects sorted by modification time (oldest first)
        """
        try:
            # Get all files with the specified extension
            pattern = f"*.{file_extension.lower()}"
            files = list(self.data_folder.glob(pattern))

            # Sort by modification time (oldest first)
            files.sort(key=lambda f: f.stat().st_mtime)

            logger.debug(f"Found {len(files)} {file_extension} files in {self.data_folder}")
            return files

        except Exception as e:
            logger.error(f"Error getting {file_extension} files from {self.data_folder}: {e}")
            return []

    def delete_oldest_files(self, file_extension: str, count_to_delete: int) -> List[str]:
        """
        Delete the oldest files of a specific type.

        Args:
            file_extension: File extension without dot (e.g., 'csv', 'json')
            count_to_delete: Number of files to delete

        Returns:
            List of deleted file names (for logging)
        """
        # Check if file caps are enabled
        try:
            from shared_config import ENABLE_FILE_CAPS, DRY_RUN_MODE
        except ImportError:
            ENABLE_FILE_CAPS = True
            DRY_RUN_MODE = False

        if not ENABLE_FILE_CAPS:
            logger.info("File caps disabled, skipping deletion")
            return []

        if count_to_delete <= 0:
            return []

        files = self.get_files_by_type(file_extension)
        files_to_delete = files[:count_to_delete]
        deleted_files = []

        for file_path in files_to_delete:
            try:
                if DRY_RUN_MODE:
                    logger.info(f"DRY RUN: Would delete {file_path.name}")
                    deleted_files.append(f"[DRY RUN] {file_path.name}")
                else:
                    file_path.unlink()
                    logger.info(f"Deleted old file: {file_path.name}")
                    deleted_files.append(file_path.name)

            except Exception as e:
                logger.error(f"Failed to delete {file_path.name}: {e}")

        return deleted_files

    def enforce_file_caps(self, new_file_path: str) -> Dict[str, List[str]]:
        """
        Enforce file caps after a new file has been created.

        Args:
            new_file_path: Path to the newly created file

        Returns:
            Dictionary mapping file extensions to lists of deleted files
        """
        # Check if file caps are enabled
        try:
            from shared_config import ENABLE_FILE_CAPS
        except ImportError:
            ENABLE_FILE_CAPS = True

        if not ENABLE_FILE_CAPS:
            logger.info("File caps disabled globally")
            return {}

        # Get file extension
        new_file = Path(new_file_path)
        file_extension = new_file.suffix.lstrip('.').lower()

        if file_extension not in self.file_caps:
            logger.debug(f"No cap configured for .{file_extension} files")
            return {}

        cap = self.file_caps[file_extension]
        if cap <= 0:
            logger.debug(f"File cap disabled for .{file_extension} files (cap={cap})")
            return {}

        # Get current files of this type
        current_files = self.get_files_by_type(file_extension)
        current_count = len(current_files)

        logger.info(f"File cap check: {current_count} {file_extension} files, cap is {cap}")

        deleted_files = {}
        if current_count > cap:
            files_to_delete = current_count - cap
            logger.info(f"Exceeds cap by {files_to_delete}, deleting oldest files")

            deleted = self.delete_oldest_files(file_extension, files_to_delete)
            if deleted:
                deleted_files[file_extension] = deleted

        return deleted_files

    def cleanup_all_file_types(self) -> Dict[str, List[str]]:
        """
        Enforce caps for all configured file types in the data folder.

        Returns:
            Dictionary mapping file extensions to lists of deleted files
        """
        # Check if file caps are enabled
        try:
            from shared_config import ENABLE_FILE_CAPS
        except ImportError:
            ENABLE_FILE_CAPS = True

        if not ENABLE_FILE_CAPS:
            logger.info("File caps disabled globally")
            return {}

        all_deleted = {}

        for file_extension, cap in self.file_caps.items():
            if cap <= 0:
                continue

            current_files = self.get_files_by_type(file_extension)
            current_count = len(current_files)

            if current_count > cap:
                files_to_delete = current_count - cap
                logger.info(f"Cleanup: {current_count} {file_extension} files, cap is {cap}, deleting {files_to_delete}")

                deleted = self.delete_oldest_files(file_extension, files_to_delete)
                if deleted:
                    all_deleted[file_extension] = deleted

        return all_deleted

    def get_file_counts(self) -> Dict[str, int]:
        """
        Get current file counts for all configured file types.

        Returns:
            Dictionary mapping file extensions to current file counts
        """
        counts = {}
        for file_extension in self.file_caps.keys():
            files = self.get_files_by_type(file_extension)
            counts[file_extension] = len(files)

        return counts

    def validate_caps(self) -> List[str]:
        """
        Validate file cap configuration.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        if not isinstance(self.file_caps, dict):
            errors.append("file_caps must be a dictionary")
            return errors

        for file_type, cap in self.file_caps.items():
            if not isinstance(file_type, str):
                errors.append(f"File type must be string, got {type(file_type)}: {file_type}")

            if not isinstance(cap, int):
                errors.append(f"Cap for {file_type} must be integer, got {type(cap)}: {cap}")
            elif cap < 0:
                errors.append(f"Cap for {file_type} must be non-negative, got {cap}")

        return errors


def log_file_operation(operation: str, file_path: str, additional_info: str = ""):
    """
    Centralized logging for file operations with timestamp.

    Args:
        operation: Type of operation (e.g., "CREATED", "DELETED", "CAP_ENFORCED")
        file_path: Path to the file involved
        additional_info: Additional context information
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = Path(file_path).name

    if additional_info:
        logger.info(f"[{timestamp}] {operation}: {file_name} ({additional_info})")
    else:
        logger.info(f"[{timestamp}] {operation}: {file_name}")


# Convenience function for common usage pattern
def enforce_caps_for_new_file(new_file_path: str, data_folder: str = None) -> Dict[str, List[str]]:
    """
    Convenience function to enforce file caps for a newly created file.

    Args:
        new_file_path: Path to the newly created file
        data_folder: Data folder path (auto-detected from file path if None)

    Returns:
        Dictionary of deleted files by extension
    """
    if data_folder is None:
        data_folder = Path(new_file_path).parent

    manager = DataFileManager(data_folder)
    deleted = manager.enforce_file_caps(new_file_path)

    if deleted:
        log_file_operation("CAP_ENFORCED", new_file_path, f"Deleted: {deleted}")

    return deleted


if __name__ == "__main__":
    # Example usage and testing
    from shared_files.logging_utils import setup_basic_logging
    setup_basic_logging(level='INFO', format_style='simple')

    # Test with current configuration
    try:
        from shared_config import DEFAULT_FILE_CAPS
        print(f"Default file caps: {DEFAULT_FILE_CAPS}")

        # Test validation
        manager = DataFileManager("test_data", DEFAULT_FILE_CAPS)
        errors = manager.validate_caps()
        if errors:
            print(f"Configuration errors: {errors}")
        else:
            print("Configuration is valid")

        # Show current counts for existing data folders
        data_folders = [
            "player-data-fetcher/data",
            "nfl-scores-fetcher/data",
            "starter_helper/data",
            "draft_helper/data"
        ]

        for folder in data_folders:
            if Path(folder).exists():
                folder_manager = DataFileManager(folder, DEFAULT_FILE_CAPS)
                counts = folder_manager.get_file_counts()
                print(f"\n{folder}: {counts}")

    except ImportError as e:
        print(f"Could not import configuration: {e}")