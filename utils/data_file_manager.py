#!/usr/bin/env python3
"""
Data File Manager - Automatic File Cap Enforcement

This module provides automatic cleanup of data files to maintain configurable limits
on the number of files of each type in data folders. When caps are exceeded, the
oldest files are automatically deleted to make room for new ones.

Usage:
    from utils.data_file_manager import DataFileManager
    from config import DEFAULT_FILE_CAPS

    manager = DataFileManager('path/to/data/folder', DEFAULT_FILE_CAPS)
    manager.enforce_file_caps('newly_created_file.csv')

Author: Kai Mizuno
"""

import asyncio
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from datetime import datetime
import pandas as pd
from utils.LoggingManager import get_logger


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

        # Set default caps if not provided
        if file_caps is None:
            file_caps = {'csv': 5, 'json': 5, 'xlsx': 5, 'txt': 5}

        self.file_caps = file_caps

        # Create data folder if it doesn't exist
        self.data_folder.mkdir(parents=True, exist_ok=True)

        self.logger = get_logger()
        self.logger.debug(f"DataFileManager initialized for {self.data_folder} with caps: {self.file_caps}")

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
            # Pattern is case-insensitive by using .lower()
            pattern = f"*.{file_extension.lower()}"
            files = list(self.data_folder.glob(pattern))

            # Sort by modification time (oldest first)
            # st_mtime is seconds since epoch, lower = older
            # This ensures we delete oldest files when enforcing caps
            files.sort(key=lambda f: f.stat().st_mtime)

            self.logger.debug(f"Found {len(files)} {file_extension} files in {self.data_folder}")
            return files

        except Exception as e:
            self.logger.error(f"Error getting {file_extension} files from {self.data_folder}: {e}")
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

        # Early return if nothing to delete
        if count_to_delete <= 0:
            return []

        # Get all files sorted by modification time (oldest first)
        files = self.get_files_by_type(file_extension)
        # Take first N files (oldest) for deletion
        files_to_delete = files[:count_to_delete]
        deleted_files = []

        for file_path in files_to_delete:
            try:
                file_path.unlink()
                self.logger.info(f"Deleted old file: {file_path.name}")
                deleted_files.append(file_path.name)

            except Exception as e:
                self.logger.error(f"Failed to delete {file_path.name}: {e}")

        return deleted_files

    def enforce_file_caps(self, new_file_path: str) -> Dict[str, List[str]]:
        """
        Enforce file caps after a new file has been created.

        Args:
            new_file_path: Path to the newly created file

        Returns:
            Dictionary mapping file extensions to lists of deleted files
        """

        # Extract file extension from the new file
        # .lstrip('.') removes leading dot from suffix (.csv -> csv)
        new_file = Path(new_file_path)
        file_extension = new_file.suffix.lstrip('.').lower()

        # Skip if no cap is configured for this file type
        if file_extension not in self.file_caps:
            self.logger.debug(f"No cap configured for .{file_extension} files")
            return {}

        # Cap of 0 or negative means unlimited files (no enforcement)
        cap = self.file_caps[file_extension]
        if cap <= 0:
            self.logger.debug(f"File cap disabled for .{file_extension} files (cap={cap})")
            return {}

        # Get current files of this type
        current_files = self.get_files_by_type(file_extension)
        current_count = len(current_files)

        self.logger.info(f"File cap check: {current_count} {file_extension} files, cap is {cap}")

        deleted_files = {}
        # Only delete if we exceed the cap
        # Example: cap=5, current=7 -> delete 2 oldest files
        if current_count > cap:
            files_to_delete = current_count - cap
            self.logger.info(f"Exceeds cap by {files_to_delete}, deleting oldest files")

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
        all_deleted = {}

        for file_extension, cap in self.file_caps.items():
            if cap <= 0:
                continue

            current_files = self.get_files_by_type(file_extension)
            current_count = len(current_files)

            if current_count > cap:
                files_to_delete = current_count - cap
                self.logger.info(f"Cleanup: {current_count} {file_extension} files, cap is {cap}, deleting {files_to_delete}")

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

    # === Enhanced File Pattern Methods ===

    def generate_timestamped_filename(self, prefix: str, extension: str, include_time: bool = True) -> str:
        """
        Generate timestamped filename with consistent format.

        Args:
            prefix: Filename prefix (e.g., 'players', 'scores')
            extension: File extension without dot (e.g., 'csv', 'json')
            include_time: Whether to include time in timestamp

        Returns:
            Timestamped filename string
        """
        # Generate timestamp in sortable format
        # With time: YYYYMMDD_HHMMSS (e.g., 20250117_143052)
        # Without time: YYYYMMDD (e.g., 20250117)
        if include_time:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        else:
            timestamp = datetime.now().strftime('%Y%m%d')

        # Format: prefix_timestamp.extension (e.g., players_20250117_143052.csv)
        return f"{prefix}_{timestamp}.{extension}"

    def get_timestamped_path(self, prefix: str, extension: str, include_time: bool = True) -> Path:
        """
        Get full path for timestamped file in managed data folder.

        Args:
            prefix: Filename prefix
            extension: File extension without dot
            include_time: Whether to include time in timestamp

        Returns:
            Full Path object for timestamped file
        """
        filename = self.generate_timestamped_filename(prefix, extension, include_time)
        return self.data_folder / filename

    def get_latest_path(self, prefix: str, extension: str) -> Path:
        """
        Get path for 'latest' version of a file.

        Args:
            prefix: Filename prefix
            extension: File extension without dot

        Returns:
            Full Path object for latest file
        """
        filename = f"{prefix}_latest.{extension}"
        return self.data_folder / filename

    async def save_dataframe_csv(self, df: pd.DataFrame, prefix: str,
                                create_latest: bool = True, **csv_kwargs) -> Tuple[Path, Optional[Path]]:
        """
        Save DataFrame to timestamped CSV with optional latest copy.

        Args:
            df: DataFrame to save
            prefix: Filename prefix
            create_latest: Whether to create latest copy
            **csv_kwargs: Additional arguments for to_csv()

        Returns:
            Tuple of (timestamped_path, latest_path)
        """
        # Set default CSV options (no index, UTF-8 encoding)
        # User can override with csv_kwargs
        csv_options = {'index': False, 'encoding': 'utf-8'}
        csv_options.update(csv_kwargs)

        timestamped_path = self.get_timestamped_path(prefix, 'csv')

        # Save timestamped version for historical record
        df.to_csv(timestamped_path, **csv_options)
        self.logger.info(f"Saved CSV: {timestamped_path}")

        # Optionally save a "latest" version for easy access
        # This gets overwritten each time, providing current snapshot
        latest_path = None
        if create_latest:
            latest_path = self.get_latest_path(prefix, 'csv')
            df.to_csv(latest_path, **csv_options)
            self.logger.info(f"Saved latest CSV: {latest_path}")

        # Enforce file caps after saving (deletes old timestamped files)
        # Latest files are not subject to caps
        self.enforce_file_caps(str(timestamped_path))

        return timestamped_path, latest_path

    async def save_dataframe_excel(self, df: pd.DataFrame, prefix: str,
                                  sheet_name: str = 'Sheet1', create_latest: bool = True,
                                  **excel_kwargs) -> Tuple[Path, Optional[Path]]:
        """
        Save DataFrame to timestamped Excel with optional latest copy.

        Args:
            df: DataFrame to save
            prefix: Filename prefix
            sheet_name: Excel sheet name
            create_latest: Whether to create latest copy
            **excel_kwargs: Additional arguments for to_excel()

        Returns:
            Tuple of (timestamped_path, latest_path)
        """
        # Set default Excel options
        excel_options = {'index': False, 'sheet_name': sheet_name}
        excel_options.update(excel_kwargs)

        timestamped_path = self.get_timestamped_path(prefix, 'xlsx')

        # Save timestamped version
        df.to_excel(timestamped_path, **excel_options)
        self.logger.info(f"Saved Excel: {timestamped_path}")

        latest_path = None
        if create_latest:
            latest_path = self.get_latest_path(prefix, 'xlsx')
            df.to_excel(latest_path, **excel_options)
            self.logger.info(f"Saved latest Excel: {latest_path}")

        # Enforce file caps
        self.enforce_file_caps(str(timestamped_path))

        return timestamped_path, latest_path

    def save_json_data(self, data: Any, prefix: str, create_latest: bool = True,
                       **json_kwargs) -> Tuple[Path, Optional[Path]]:
        """
        Save data to timestamped JSON with optional latest copy.

        Args:
            data: Data to save (must be JSON serializable)
            prefix: Filename prefix
            create_latest: Whether to create latest copy
            **json_kwargs: Additional arguments for json.dump()

        Returns:
            Tuple of (timestamped_path, latest_path)
        """
        # Set default JSON options with datetime serialization support
        json_options = {'indent': 2, 'ensure_ascii': False, 'default': str}
        json_options.update(json_kwargs)

        timestamped_path = self.get_timestamped_path(prefix, 'json')

        # Save timestamped version
        with open(timestamped_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, **json_options)
        self.logger.info(f"Saved JSON: {timestamped_path}")

        latest_path = None
        if create_latest:
            latest_path = self.get_latest_path(prefix, 'json')
            with open(latest_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, **json_options)
            self.logger.info(f"Saved latest JSON: {latest_path}")

        # Enforce file caps
        self.enforce_file_caps(str(timestamped_path))

        return timestamped_path, latest_path

    async def export_multi_format(self, df: pd.DataFrame, prefix: str,
                                 formats: List[str] = None, create_latest: bool = True,
                                 sheet_name: str = 'Sheet1') -> Dict[str, Tuple[Path, Optional[Path]]]:
        """
        Export DataFrame to multiple formats concurrently.

        Args:
            df: DataFrame to export
            prefix: Filename prefix for all formats
            formats: List of formats to export ('csv', 'xlsx', 'json'). Defaults to all.
            create_latest: Whether to create latest copies
            sheet_name: Excel sheet name

        Returns:
            Dictionary mapping format to (timestamped_path, latest_path) tuples
        """
        # Default to exporting all supported formats
        if formats is None:
            formats = ['csv', 'xlsx', 'json']

        # Build list of async tasks for concurrent execution
        tasks = []
        format_tasks = {}  # Maps format name to task index

        if 'csv' in formats:
            task = self.save_dataframe_csv(df, prefix, create_latest)
            tasks.append(task)
            format_tasks['csv'] = len(tasks) - 1

        if 'xlsx' in formats:
            task = self.save_dataframe_excel(df, prefix, sheet_name, create_latest)
            tasks.append(task)
            format_tasks['xlsx'] = len(tasks) - 1

        if 'json' in formats:
            # Convert DataFrame to JSON-serializable format (list of dicts)
            json_data = df.to_dict('records')
            # JSON save is synchronous, so wrap it in a coroutine for async execution
            async def save_json():
                return self.save_json_data(json_data, prefix, create_latest)
            task = save_json()
            tasks.append(task)
            format_tasks['json'] = len(tasks) - 1

        # Execute all exports concurrently for performance
        # asyncio.gather runs all tasks in parallel
        results = await asyncio.gather(*tasks)

        # Map results back to formats
        export_results = {}
        for format_name, task_index in format_tasks.items():
            export_results[format_name] = results[task_index]

        self.logger.info(f"Multi-format export completed for {prefix}: {list(export_results.keys())}")
        return export_results

    def create_backup_copy(self, source_path: Union[str, Path], backup_suffix: str = "_backup") -> Path:
        """
        Create backup copy of a file with timestamp.

        Args:
            source_path: Path to source file
            backup_suffix: Suffix to add before timestamp

        Returns:
            Path to backup file
        """
        source_path = Path(source_path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Build backup filename: original_stem + suffix + timestamp + extension
        # Example: players.csv -> players_backup_20250117_143052.csv
        backup_name = f"{source_path.stem}{backup_suffix}_{timestamp}{source_path.suffix}"
        backup_path = source_path.parent / backup_name

        if source_path.exists():
            # shutil.copy2 preserves metadata (timestamps, permissions)
            shutil.copy2(source_path, backup_path)
            self.logger.info(f"Created backup: {source_path} -> {backup_path}")
        else:
            self.logger.warning(f"Source file does not exist for backup: {source_path}")

        return backup_path

    def cleanup_old_backups(self, pattern: str, keep_count: int = 3) -> List[str]:
        """
        Clean up old backup files, keeping only the most recent ones.

        Args:
            pattern: Glob pattern to match backup files
            keep_count: Number of recent backups to keep

        Returns:
            List of deleted backup file names
        """
        # Find all backup files matching the glob pattern
        backup_files = list(self.data_folder.glob(pattern))
        # Sort by modification time (newest first) using reverse=True
        # This way we keep the most recent backups
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        deleted_files = []
        # Delete all backups beyond keep_count (oldest ones)
        # Example: keep_count=3, total=5 -> delete files at indices 3,4 (2 oldest)
        if len(backup_files) > keep_count:
            files_to_delete = backup_files[keep_count:]
            for file_path in files_to_delete:
                try:
                    file_path.unlink()
                    deleted_files.append(file_path.name)
                    self.logger.info(f"Deleted old backup: {file_path}")
                except Exception as e:
                    self.logger.error(f"Failed to delete backup {file_path}: {e}")

        return deleted_files


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
        self.logger.info(f"[{timestamp}] {operation}: {file_name} ({additional_info})")
    else:
        self.logger.info(f"[{timestamp}] {operation}: {file_name}")


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
