"""
Progress Tracker

Displays real-time progress updates for long-running simulations.
Shows progress bars, ETA estimates, and completion statistics.

Uses simple text-based progress indicators that work in any terminal.
Provides both simple progress bars and detailed multi-level tracking.

Author: Kai Mizuno
Date: 2024
"""

import time
from datetime import datetime, timedelta
from typing import Optional


class ProgressTracker:
    """
    Tracks and displays simulation progress.

    Provides real-time updates with progress bars, completion percentages,
    elapsed time, and estimated time remaining. Designed for terminal output.

    Attributes:
        total (int): Total number of items to process
        completed (int): Number of completed items
        start_time (float): Start timestamp
        last_update_time (float): Last progress update timestamp
        description (str): Description of the task being tracked
    """

    def __init__(self, total: int, description: str = "Progress") -> None:
        """
        Initialize ProgressTracker.

        Args:
            total (int): Total number of items to process
            description (str): Description of the task (default: "Progress")
        """
        self.total = total
        self.completed = 0
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.description = description

    def update(self, increment: int = 1) -> None:
        """
        Update progress by increment and display.

        Args:
            increment (int): Number of items completed (default: 1)
        """
        self.completed += increment
        self.last_update_time = time.time()
        self.display()

    def set_completed(self, completed: int) -> None:
        """
        Set absolute completion count and display.

        Args:
            completed (int): Total number of completed items
        """
        self.completed = completed
        self.last_update_time = time.time()
        self.display()

    def get_elapsed_time(self) -> float:
        """
        Get elapsed time in seconds.

        Returns:
            float: Seconds elapsed since start
        """
        return time.time() - self.start_time

    def get_eta(self) -> Optional[float]:
        """
        Get estimated time remaining in seconds.

        Returns:
            Optional[float]: Estimated seconds remaining, or None if can't calculate
        """
        if self.completed == 0:
            return None

        elapsed = self.get_elapsed_time()
        rate = self.completed / elapsed  # items per second
        remaining = self.total - self.completed

        if rate > 0:
            return remaining / rate
        return None

    def get_percentage(self) -> float:
        """
        Get completion percentage.

        Returns:
            float: Percentage complete (0.0 to 100.0)
        """
        if self.total == 0:
            return 100.0
        return (self.completed / self.total) * 100.0

    def format_time(self, seconds: float) -> str:
        """
        Format seconds as human-readable time string.

        Args:
            seconds (float): Time in seconds

        Returns:
            str: Formatted time string (e.g., "1h 23m 45s", "2m 30s", "45s")
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"

    def create_progress_bar(self, width: int = 40) -> str:
        """
        Create ASCII progress bar.

        Args:
            width (int): Width of progress bar in characters (default: 40)

        Returns:
            str: Progress bar string like "[=========>          ] 45%"
        """
        percentage = self.get_percentage()
        filled_width = int((percentage / 100.0) * width)

        # Create bar with filled and empty sections
        if filled_width >= width:
            bar = "=" * width
        elif filled_width > 0:
            bar = "=" * (filled_width - 1) + ">" + " " * (width - filled_width)
        else:
            bar = " " * width

        return f"[{bar}]"

    def display(self) -> None:
        """
        Display current progress to console.

        Prints a single-line progress update with bar, percentage, count,
        elapsed time, and ETA.
        """
        bar = self.create_progress_bar(width=40)
        percentage = self.get_percentage()
        elapsed = self.get_elapsed_time()
        eta = self.get_eta()

        # Build progress line
        line = (
            f"\r{self.description}: {bar} "
            f"{percentage:5.1f}% "
            f"({self.completed}/{self.total}) | "
            f"Elapsed: {self.format_time(elapsed)}"
        )

        if eta is not None:
            line += f" | ETA: {self.format_time(eta)}"

        # Print without newline (overwrite previous line)
        print(line, end="", flush=True)

        # Add newline when complete
        if self.completed >= self.total:
            print()  # Final newline

    def finish(self) -> None:
        """
        Mark progress as complete and display final stats.

        Prints final completion message with total elapsed time.
        """
        self.completed = self.total
        elapsed = self.get_elapsed_time()
        print(
            f"\n{self.description}: Complete! "
            f"({self.total} items in {self.format_time(elapsed)})"
        )


class MultiLevelProgressTracker:
    """
    Tracks progress at multiple levels (e.g., configs and simulations per config).

    Provides hierarchical progress tracking for nested operations like:
    - Testing 100 configs (outer level)
    - Each config runs 100 simulations (inner level)

    Attributes:
        outer_total (int): Total outer items (e.g., number of configs)
        inner_total (int): Total inner items per outer item (e.g., sims per config)
        outer_completed (int): Completed outer items
        inner_completed (int): Completed inner items for current outer item
        start_time (float): Start timestamp
        outer_desc (str): Description of outer level
        inner_desc (str): Description of inner level
    """

    def __init__(
        self,
        outer_total: int,
        inner_total: int,
        outer_desc: str = "Configs",
        inner_desc: str = "Simulations"
    ) -> None:
        """
        Initialize MultiLevelProgressTracker.

        Args:
            outer_total (int): Total number of outer items
            inner_total (int): Total number of inner items per outer item
            outer_desc (str): Description of outer level (default: "Configs")
            inner_desc (str): Description of inner level (default: "Simulations")
        """
        self.outer_total = outer_total
        self.inner_total = inner_total
        self.outer_completed = 0
        self.inner_completed = 0
        self.start_time = time.time()
        self.outer_desc = outer_desc
        self.inner_desc = inner_desc

    def update_inner(self, completed: int) -> None:
        """
        Update inner level progress.

        Args:
            completed (int): Number of inner items completed for current outer item
        """
        self.inner_completed = completed
        self.display()

    def next_outer(self) -> None:
        """
        Move to next outer item and reset inner progress.
        """
        self.outer_completed += 1
        self.inner_completed = 0
        self.display()

    def get_overall_percentage(self) -> float:
        """
        Get overall completion percentage across all levels.

        Returns:
            float: Overall percentage (0.0 to 100.0)
        """
        total_items = self.outer_total * self.inner_total
        completed_items = (self.outer_completed * self.inner_total) + self.inner_completed

        if total_items == 0:
            return 100.0
        return (completed_items / total_items) * 100.0

    def get_eta(self) -> Optional[float]:
        """
        Get estimated time remaining in seconds.

        Returns:
            Optional[float]: Estimated seconds remaining, or None if can't calculate
        """
        total_items = self.outer_total * self.inner_total
        completed_items = (self.outer_completed * self.inner_total) + self.inner_completed

        if completed_items == 0:
            return None

        elapsed = time.time() - self.start_time
        rate = completed_items / elapsed
        remaining = total_items - completed_items

        if rate > 0:
            return remaining / rate
        return None

    def format_time(self, seconds: float) -> str:
        """Format seconds as human-readable time string."""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"

    def display(self) -> None:
        """
        Display current progress for both levels.

        Prints multi-line progress update showing outer progress, inner progress,
        and overall completion percentage with ETA.
        """
        overall_pct = self.get_overall_percentage()
        eta = self.get_eta()
        elapsed = time.time() - self.start_time

        # Outer progress
        outer_pct = (self.outer_completed / self.outer_total * 100.0) if self.outer_total > 0 else 0.0

        # Inner progress
        inner_pct = (self.inner_completed / self.inner_total * 100.0) if self.inner_total > 0 else 0.0

        print(f"\r{self.outer_desc}: {self.outer_completed}/{self.outer_total} ({outer_pct:.1f}%) | "
              f"{self.inner_desc}: {self.inner_completed}/{self.inner_total} ({inner_pct:.1f}%) | "
              f"Overall: {overall_pct:.1f}% | "
              f"Elapsed: {self.format_time(elapsed)}", end="")

        if eta is not None:
            print(f" | ETA: {self.format_time(eta)}", end="")

        print("    ", end="", flush=True)  # Extra spaces to clear previous text

        # Add newline when complete
        if self.outer_completed >= self.outer_total:
            print()

    def finish(self) -> None:
        """
        Mark progress as complete and display final stats.
        """
        self.outer_completed = self.outer_total
        self.inner_completed = self.inner_total
        elapsed = time.time() - self.start_time
        total_items = self.outer_total * self.inner_total

        print(
            f"\nComplete! Processed {total_items} total items "
            f"({self.outer_total} {self.outer_desc.lower()} × "
            f"{self.inner_total} {self.inner_desc.lower()}) "
            f"in {self.format_time(elapsed)}"
        )
