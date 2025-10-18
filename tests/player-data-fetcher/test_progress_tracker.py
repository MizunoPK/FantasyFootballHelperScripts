#!/usr/bin/env python3
"""
Tests for Progress Tracker Module

Basic smoke tests for progress tracking functionality.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock
from pathlib import Path
import sys
import time

# Add project root and player-data-fetcher to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

from progress_tracker import ProgressTracker


class TestProgressTrackerInit:
    """Test ProgressTracker initialization"""

    def test_tracker_initialization(self):
        """Test ProgressTracker can be initialized"""
        mock_logger = Mock()
        tracker = ProgressTracker(total_players=100, logger=mock_logger)

        assert tracker.total_players == 100
        assert tracker.processed_players == 0
        assert tracker.logger == mock_logger

    def test_tracker_custom_update_frequency(self):
        """Test ProgressTracker with custom update frequency"""
        mock_logger = Mock()
        tracker = ProgressTracker(
            total_players=100,
            logger=mock_logger,
            update_frequency=5
        )

        assert tracker.update_frequency == 5

    def test_tracker_custom_eta_window(self):
        """Test ProgressTracker with custom ETA window size"""
        mock_logger = Mock()
        tracker = ProgressTracker(
            total_players=100,
            logger=mock_logger,
            eta_window_size=25
        )

        assert tracker.eta_window_size == 25

    def test_tracker_starts_at_zero_progress(self):
        """Test ProgressTracker starts with zero progress"""
        mock_logger = Mock()
        tracker = ProgressTracker(total_players=50, logger=mock_logger)

        assert tracker.processed_players == 0


class TestProgressTrackerUpdate:
    """Test progress tracking updates"""

    def test_update_increments_progress(self):
        """Test update() increments processed players"""
        mock_logger = Mock()
        tracker = ProgressTracker(total_players=100, logger=mock_logger, update_frequency=1)

        tracker.update()
        assert tracker.processed_players == 1

        tracker.update()
        assert tracker.processed_players == 2

    def test_update_with_custom_increment(self):
        """Test update() with custom increment value"""
        mock_logger = Mock()
        tracker = ProgressTracker(total_players=100, logger=mock_logger)

        tracker.update(increment=5)
        assert tracker.processed_players == 5

    def test_update_multiple_times(self):
        """Test updating progress multiple times"""
        mock_logger = Mock()
        tracker = ProgressTracker(total_players=100, logger=mock_logger)

        for i in range(10):
            tracker.update()

        assert tracker.processed_players == 10

    def test_update_returns_true_on_log_event(self):
        """Test update() returns True when progress is logged"""
        mock_logger = Mock()
        tracker = ProgressTracker(
            total_players=100,
            logger=mock_logger,
            update_frequency=10
        )

        # Update to the logging threshold
        for i in range(9):
            result = tracker.update()
            assert result == False  # Should not log yet

        result = tracker.update()  # 10th update
        assert result == True  # Should log now

    def test_update_returns_true_on_completion(self):
        """Test update() returns True when reaching total"""
        mock_logger = Mock()
        tracker = ProgressTracker(
            total_players=5,
            logger=mock_logger,
            update_frequency=100  # High frequency so only completion triggers
        )

        # Update to completion
        for i in range(4):
            tracker.update()

        result = tracker.update()  # Final update
        assert result == True  # Should log on completion


class TestProgressTrackerTiming:
    """Test progress tracking timing"""

    def test_tracker_records_start_time(self):
        """Test tracker records start time"""
        mock_logger = Mock()
        start = time.time()
        tracker = ProgressTracker(total_players=100, logger=mock_logger)

        # Start time should be close to current time
        assert tracker.start_time >= start
        assert tracker.start_time <= time.time()

    def test_tracker_updates_last_update_time(self):
        """Test tracker updates last update time"""
        mock_logger = Mock()
        tracker = ProgressTracker(
            total_players=100,
            logger=mock_logger,
            update_frequency=1
        )

        initial_time = tracker.last_update_time
        time.sleep(0.01)  # Small delay
        tracker.update()

        # Last update time should have changed
        assert tracker.last_update_time >= initial_time


class TestEdgeCases:
    """Test edge cases"""

    def test_tracker_with_zero_total(self):
        """Test tracker handles zero total players gracefully"""
        mock_logger = Mock()
        # Should not crash with zero total
        tracker = ProgressTracker(total_players=0, logger=mock_logger)

        assert tracker.total_players == 0

    def test_tracker_with_large_total(self):
        """Test tracker handles large player counts"""
        mock_logger = Mock()
        tracker = ProgressTracker(total_players=1000000, logger=mock_logger)

        assert tracker.total_players == 1000000
        tracker.update()
        assert tracker.processed_players == 1

    def test_multiple_updates_at_once(self):
        """Test updating with large increments"""
        mock_logger = Mock()
        tracker = ProgressTracker(total_players=100, logger=mock_logger)

        tracker.update(increment=50)
        assert tracker.processed_players == 50

        tracker.update(increment=50)
        assert tracker.processed_players == 100
