#!/usr/bin/env python3
"""
Line-Based Rotating File Handler

Custom logging handler that rotates log files based on line count rather than file size.
Provides automatic cleanup to maintain a maximum number of log files per directory.

Author: Kai Mizuno
"""

import os
import re
import glob
from datetime import datetime
from logging import FileHandler
from pathlib import Path
from typing import Optional


class LineBasedRotatingHandler(FileHandler):
    """
    Custom log handler with line-based rotation and automated cleanup.

    Rotates log files when they reach a specified line count (default: 500 lines).
    Automatically cleans up old log files when folder exceeds max_files limit.
    Creates timestamped log filenames for easy chronological organization.

    Features:
    - Line-based rotation (not size-based)
    - In-memory line counter (resets on script restart)
    - Timestamped filenames: {script_name}-{YYYYMMDD_HHMMSS}.log
    - Automatic cleanup (max 50 files per folder)
    - Eager line counting (increments before writing)

    Example:
        >>> handler = LineBasedRotatingHandler(
        ...     filename='logs/my_app/my_app-20260207_160000.log',
        ...     max_lines=500,
        ...     max_files=50
        ... )
        >>> logger.addHandler(handler)

    Args:
        filename (str): Path to log file
        mode (str): File open mode (default: 'a' for append)
        max_lines (int): Maximum lines per file before rotation (default: 500)
        max_files (int): Maximum files per folder before cleanup (default: 50)
        encoding (str): File encoding (default: 'utf-8')
        delay (bool): Delay file opening until first emit (default: False)
    """

    def __init__(
        self,
        filename: str,
        mode: str = 'a',
        max_lines: int = 500,
        max_files: int = 50,
        encoding: Optional[str] = 'utf-8',
        delay: bool = False
    ):
        """
        Initialize the line-based rotating file handler.

        Args:
            filename (str): Path to log file
            mode (str): File open mode (default: 'a')
            max_lines (int): Max lines before rotation (default: 500)
            max_files (int): Max files before cleanup (default: 50)
            encoding (str): File encoding (default: 'utf-8')
            delay (bool): Delay file opening (default: False)

        Raises:
            ValueError: If max_lines < 1 or max_files < 1
        """
        # Validate parameters
        if max_lines < 1:
            raise ValueError(f"max_lines must be >= 1, got {max_lines}")
        if max_files < 1:
            raise ValueError(f"max_files must be >= 1, got {max_files}")

        self.max_lines = max_lines
        self.max_files = max_files
        self._line_counter = 0  # In-memory counter (NOT persistent)

        # Initialize parent FileHandler
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        """
        Emit a log record and increment line counter.

        Increments the line counter BEFORE emitting to ensure accurate
        rotation threshold detection (eager counting). Checks if rotation
        is needed after each emit.

        Args:
            record: LogRecord to emit

        Note:
            Line counter increments even if emit fails. This is intentional
            to maintain consistency and prevent infinite loops.
        """
        # Increment line counter BEFORE writing (eager counting)
        self._line_counter += 1

        # Call parent emit to write log record
        try:
            super().emit(record)
        except Exception:
            # Let parent class handle exceptions
            self.handleError(record)

        # Check if rotation needed after emit
        if self.shouldRollover(record):
            try:
                self.doRollover()
            except Exception:
                self.handleError(record)

    def shouldRollover(self, record) -> bool:
        """
        Determine if log file should rotate.

        Checks if line counter has reached or exceeded the max_lines threshold.
        Uses simple integer comparison for O(1) performance.

        Args:
            record: LogRecord (unused, for API compatibility)

        Returns:
            bool: True if rotation needed, False otherwise

        Note:
            The 'record' parameter is unused but required for compatibility
            with the logging.Handler API.
        """
        # Rotation needed if counter >= max_lines
        return self._line_counter >= self.max_lines

    def doRollover(self):
        """
        Perform log file rotation and cleanup.

        Rotation process:
        1. Close current log file
        2. Reset line counter to 0
        3. Generate new timestamped filename
        4. Open new log file
        5. Cleanup old files if folder exceeds max_files limit

        The new filename uses format: {base_name}-{YYYYMMDD_HHMMSS}.log
        where base_name is extracted from the current filename.

        Example:
            Current: logs/my_app/my_app-20260207_160000.log
            New:     logs/my_app/my_app-20260207_161530.log

        Raises:
            OSError: If file operations fail (logged but not propagated)
        """
        # Close current file
        if self.stream:
            self.stream.close()
            self.stream = None

        # Reset line counter to 0
        self._line_counter = 0

        # Generate new timestamped filename with collision avoidance
        base_filename = self._get_base_filename()
        log_dir = Path(self.baseFilename).parent

        # Add microsecond precision to avoid timestamp collisions
        # Format: YYYYMMDD_HHMMSS_microseconds (ensures uniqueness even within same second)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        new_filename = log_dir / f"{base_filename}-{timestamp}.log"

        # Update baseFilename to new file
        self.baseFilename = str(new_filename)

        # Open new log file
        self.stream = self._open()

        # Log rotation event (DEBUG level)
        # Note: This log line counts toward the new file's line counter
        self.stream.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                         f"DEBUG - Log rotation triggered at {self.max_lines} lines\n")
        self.stream.flush()

        # Cleanup old files if needed
        self._cleanup_old_files()

    def _get_base_filename(self) -> str:
        """
        Extract base filename from timestamped log file.

        Extracts the script name portion from filenames like:
        - my_app-20260207_160000.log → my_app
        - accuracy_simulation-20260206_143522.log → accuracy_simulation

        Uses regex to match pattern: {name}-{YYYYMMDD_HHMMSS}.log

        Returns:
            str: Base filename without timestamp and extension

        Example:
            >>> handler._get_base_filename()
            'my_app'  # from 'logs/my_app/my_app-20260207_160000.log'
        """
        filename = Path(self.baseFilename).name

        # Extract base name using regex
        # Supports both formats:
        #   - {name}-{YYYYMMDD_HHMMSS}.log (initial file from LoggingManager)
        #   - {name}-{YYYYMMDD_HHMMSS_microseconds}.log (rotated files)
        match = re.match(r'^(.+?)-\d{8}_\d{6}(?:_\d{6})?\.log$', filename)

        if match:
            return match.group(1)
        else:
            # Fallback: remove extension if regex doesn't match
            return Path(filename).stem

    def _cleanup_old_files(self):
        """
        Delete oldest log files when count exceeds max_files.

        Cleanup algorithm:
        1. List all .log files in same directory as current log
        2. Sort by modification time (oldest first)
        3. If count > max_files, delete oldest files
        4. Log cleanup actions at INFO level

        Only counts .log files (ignores other file types).
        Uses modification time (st_mtime) to determine age.
        Continues cleanup even if individual deletions fail.

        Example:
            Folder has 52 files, max_files=50
            → Deletes 2 oldest files
            → Logs: "Cleaned up 2 old log files"

        Note:
            File deletions that fail (PermissionError, etc.) are logged
            but don't halt the cleanup process for remaining files.
        """
        log_dir = Path(self.baseFilename).parent

        # List all .log files in directory
        log_files = list(log_dir.glob('*.log'))

        # Check if cleanup needed
        if len(log_files) <= self.max_files:
            return  # No cleanup needed

        # Sort by modification time (oldest first)
        log_files.sort(key=lambda f: f.stat().st_mtime)

        # Calculate how many files to delete
        files_to_delete = len(log_files) - self.max_files

        # Delete oldest files
        deleted_count = 0
        for old_file in log_files[:files_to_delete]:
            try:
                old_file.unlink()
                deleted_count += 1
            except OSError as e:
                # Log error but continue cleanup
                if self.stream:
                    self.stream.write(
                        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"WARNING - Failed to delete old log file {old_file}: {e}\n"
                    )
                    self.stream.flush()

        # Log cleanup summary (INFO level)
        if deleted_count > 0 and self.stream:
            self.stream.write(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"INFO - Cleaned up {deleted_count} old log files\n"
            )
            self.stream.flush()
