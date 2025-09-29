#!/usr/bin/env python3
"""
Progress Tracking System for Player Data Fetcher
==============================================

Provides progress tracking with percentage completion and ETA calculation
based on recent performance for improved accuracy.

Author: Kai Mizuno
Last Updated: September 2025
"""

import logging
import time
from collections import deque
from typing import Optional, Tuple


# Custom PROGRESS log level (set to highest level to always display, above CRITICAL)
PROGRESS_LEVEL = 60

class ProgressTracker:
    """
    Tracks progress of player data fetching with ETA calculation.

    Features:
    - Percentage completion tracking
    - ETA based on recent performance (configurable window size)
    - Automatic detection of total player count
    - Progress updates every N players (configurable)
    """

    def __init__(
        self,
        total_players: int,
        update_frequency: int = 10,
        eta_window_size: int = 50,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize progress tracker.

        Args:
            total_players: Total number of players to process
            update_frequency: Update progress every N players (default: 10)
            eta_window_size: Number of recent players to use for ETA calculation (default: 50)
            logger: Logger instance to use for progress messages
        """
        self.total_players = total_players
        self.update_frequency = update_frequency
        self.eta_window_size = eta_window_size
        self.logger = logger or logging.getLogger(__name__)

        # Progress tracking
        self.processed_players = 0
        self.start_time = time.time()

        # Recent performance tracking for ETA calculation
        self.recent_times = deque(maxlen=eta_window_size)
        self.last_update_time = self.start_time
        self.last_update_count = 0

        # Add custom PROGRESS log level if not already added
        self._setup_progress_logging()

    def _setup_progress_logging(self):
        """Set up custom PROGRESS log level."""
        if not hasattr(logging, 'PROGRESS'):
            logging.addLevelName(PROGRESS_LEVEL, 'PROGRESS')

            def progress(self, message, *args, **kwargs):
                if self.isEnabledFor(PROGRESS_LEVEL):
                    self._log(PROGRESS_LEVEL, message, args, **kwargs)

            logging.Logger.progress = progress

    def update(self, increment: int = 1) -> bool:
        """
        Update progress tracker.

        Args:
            increment: Number of players processed since last update (default: 1)

        Returns:
            bool: True if progress message was logged, False otherwise
        """
        self.processed_players += increment
        current_time = time.time()

        # Track timing for recent players
        if self.processed_players > self.last_update_count:
            players_since_last = self.processed_players - self.last_update_count
            time_since_last = current_time - self.last_update_time

            if players_since_last > 0:
                avg_time_per_player = time_since_last / players_since_last
                self.recent_times.append(avg_time_per_player)

        # Check if we should log progress
        should_log = (
            self.processed_players % self.update_frequency == 0 or
            self.processed_players >= self.total_players
        )

        if should_log:
            self._log_progress()
            self.last_update_time = current_time
            self.last_update_count = self.processed_players
            return True

        return False

    def _log_progress(self):
        """Log current progress with ETA."""
        percentage = (self.processed_players / self.total_players) * 100
        eta_str = self._calculate_eta()

        message = f"Fetched {self.processed_players}/{self.total_players} players ({percentage:.1f}%)"
        if eta_str:
            message += f" - ETA: {eta_str}"

        # Use PROGRESS level if available, otherwise INFO
        if hasattr(self.logger, 'progress'):
            self.logger.progress(message)
        else:
            self.logger.info(f"[PROGRESS] {message}")

    def _calculate_eta(self) -> str:
        """
        Calculate ETA based on recent performance.

        Returns:
            str: Formatted ETA string (e.g., "5m 32s") or empty string if can't calculate
        """
        if self.processed_players >= self.total_players:
            return "Complete"

        remaining_players = self.total_players - self.processed_players

        if not self.recent_times:
            # Fall back to overall average if no recent data
            elapsed_time = time.time() - self.start_time
            if self.processed_players > 0:
                avg_time_per_player = elapsed_time / self.processed_players
                estimated_remaining_time = remaining_players * avg_time_per_player
            else:
                return ""
        else:
            # Use recent performance for more accurate ETA
            recent_avg_time = sum(self.recent_times) / len(self.recent_times)
            estimated_remaining_time = remaining_players * recent_avg_time

        return self._format_duration(estimated_remaining_time)

    def _format_duration(self, seconds: float) -> str:
        """
        Format duration in seconds to human-readable string.

        Args:
            seconds: Duration in seconds

        Returns:
            str: Formatted duration (e.g., "5m 32s", "1h 15m", "45s")
        """
        if seconds < 0:
            return ""

        seconds = int(seconds)

        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:  # Less than 1 hour
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes}m"
            else:
                return f"{minutes}m {remaining_seconds}s"
        else:  # 1 hour or more
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            if remaining_minutes == 0:
                return f"{hours}h"
            else:
                return f"{hours}h {remaining_minutes}m"

    def get_stats(self) -> dict:
        """
        Get current progress statistics.

        Returns:
            dict: Progress statistics including completion percentage, ETA, etc.
        """
        elapsed_time = time.time() - self.start_time
        percentage = (self.processed_players / self.total_players) * 100

        return {
            'processed': self.processed_players,
            'total': self.total_players,
            'percentage': percentage,
            'elapsed_time': elapsed_time,
            'eta_seconds': self._calculate_eta_seconds(),
            'eta_formatted': self._calculate_eta(),
            'players_per_second': self.processed_players / elapsed_time if elapsed_time > 0 else 0
        }

    def _calculate_eta_seconds(self) -> Optional[float]:
        """Calculate ETA in seconds."""
        if self.processed_players >= self.total_players:
            return 0.0

        remaining_players = self.total_players - self.processed_players

        if not self.recent_times:
            elapsed_time = time.time() - self.start_time
            if self.processed_players > 0:
                avg_time_per_player = elapsed_time / self.processed_players
                return remaining_players * avg_time_per_player
        else:
            recent_avg_time = sum(self.recent_times) / len(self.recent_times)
            return remaining_players * recent_avg_time

        return None

    def complete(self):
        """Mark progress as complete and log final message."""
        self.processed_players = self.total_players
        elapsed_time = time.time() - self.start_time

        message = f"Completed processing {self.total_players} players in {self._format_duration(elapsed_time)}"

        if hasattr(self.logger, 'progress'):
            self.logger.progress(message)
        else:
            self.logger.info(f"[PROGRESS] {message}")