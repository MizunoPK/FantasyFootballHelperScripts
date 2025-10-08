#!/usr/bin/env python3
"""
Unit tests for ProgressTracker class
"""

import logging
import time
import unittest
from unittest.mock import MagicMock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from progress_tracker import ProgressTracker, PROGRESS_LEVEL


class TestProgressTracker(unittest.TestCase):
    """Test cases for ProgressTracker class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_logger = MagicMock(spec=logging.Logger)
        self.tracker = ProgressTracker(
            total_players=100,
            update_frequency=10,
            eta_window_size=20,
            logger=self.mock_logger
        )

    def test_initialization(self):
        """Test ProgressTracker initialization"""
        self.assertEqual(self.tracker.total_players, 100)
        self.assertEqual(self.tracker.update_frequency, 10)
        self.assertEqual(self.tracker.eta_window_size, 20)
        self.assertEqual(self.tracker.processed_players, 0)
        self.assertEqual(len(self.tracker.recent_times), 0)
        self.assertIsNotNone(self.tracker.start_time)

    def test_custom_log_level_setup(self):
        """Test that custom PROGRESS log level is set up correctly"""
        self.assertEqual(PROGRESS_LEVEL, 25)
        self.assertTrue(hasattr(logging.Logger, 'progress'))

    def test_update_basic(self):
        """Test basic progress update functionality"""
        # First 9 updates shouldn't trigger logging
        for i in range(9):
            result = self.tracker.update()
            self.assertFalse(result)
            self.assertEqual(self.tracker.processed_players, i + 1)

        # 10th update should trigger logging
        result = self.tracker.update()
        self.assertTrue(result)
        self.assertEqual(self.tracker.processed_players, 10)

    def test_update_with_increment(self):
        """Test progress update with custom increment"""
        result = self.tracker.update(increment=10)
        self.assertTrue(result)  # Should trigger because it's exactly update_frequency
        self.assertEqual(self.tracker.processed_players, 10)

        result = self.tracker.update(increment=5)
        self.assertFalse(result)
        self.assertEqual(self.tracker.processed_players, 15)

        result = self.tracker.update(increment=5)
        self.assertTrue(result)  # Should trigger at 20
        self.assertEqual(self.tracker.processed_players, 20)

    def test_progress_logging(self):
        """Test that progress messages are logged correctly"""
        # Mock the logger to have progress method
        self.mock_logger.progress = MagicMock()
        self.tracker.logger = self.mock_logger

        # Trigger progress update
        self.tracker.update(increment=10)

        # Verify progress method was called
        self.mock_logger.progress.assert_called_once()
        call_args = self.mock_logger.progress.call_args[0][0]
        self.assertIn("Fetched 10/100 players (10.0%)", call_args)

    def test_progress_logging_fallback(self):
        """Test fallback to INFO logging when progress method not available"""
        # Remove progress method from mock logger
        if hasattr(self.mock_logger, 'progress'):
            del self.mock_logger.progress

        # Trigger progress update
        self.tracker.update(increment=10)

        # Verify info method was called with [PROGRESS] prefix
        self.mock_logger.info.assert_called_once()
        call_args = self.mock_logger.info.call_args[0][0]
        self.assertIn("[PROGRESS]", call_args)
        self.assertIn("Fetched 10/100 players (10.0%)", call_args)

    def test_eta_calculation_no_data(self):
        """Test ETA calculation when no timing data available"""
        # Mock time to control elapsed time
        with patch('time.time', return_value=100.0):
            self.tracker.start_time = 90.0  # 10 seconds elapsed
            self.tracker.processed_players = 25  # 25% complete

            eta_str = self.tracker._calculate_eta()

            # Should fall back to overall average
            # 75 remaining players * (10 seconds / 25 players) = 30 seconds
            self.assertEqual(eta_str, "30s")

    def test_eta_calculation_with_recent_data(self):
        """Test ETA calculation using recent performance data"""
        # Add some recent timing data (2 seconds per player average)
        for _ in range(10):
            self.tracker.recent_times.append(2.0)

        self.tracker.processed_players = 20
        eta_str = self.tracker._calculate_eta()

        # 80 remaining players * 2 seconds each = 160 seconds = 2m 40s
        self.assertEqual(eta_str, "2m 40s")

    def test_format_duration(self):
        """Test duration formatting"""
        test_cases = [
            (30, "30s"),
            (60, "1m"),
            (65, "1m 5s"),
            (120, "2m"),
            (3600, "1h"),
            (3665, "1h 1m"),
            (7200, "2h"),
            (7260, "2h 1m")
        ]

        for seconds, expected in test_cases:
            with self.subTest(seconds=seconds):
                result = self.tracker._format_duration(seconds)
                self.assertEqual(result, expected)

    def test_get_stats(self):
        """Test getting progress statistics"""
        # Set up some test state
        with patch('time.time', return_value=110.0):
            self.tracker.start_time = 100.0  # 10 seconds elapsed
            self.tracker.processed_players = 25

            # Add some recent timing data
            self.tracker.recent_times.extend([1.0, 1.5, 2.0])

            stats = self.tracker.get_stats()

            self.assertEqual(stats['processed'], 25)
            self.assertEqual(stats['total'], 100)
            self.assertEqual(stats['percentage'], 25.0)
            self.assertEqual(stats['elapsed_time'], 10.0)
            self.assertEqual(stats['players_per_second'], 2.5)
            self.assertIsNotNone(stats['eta_formatted'])
            self.assertIsNotNone(stats['eta_seconds'])

    def test_complete(self):
        """Test completion functionality"""
        # Mock the logger to have progress method
        self.mock_logger.progress = MagicMock()
        self.tracker.logger = self.mock_logger

        # Mock time for predictable duration
        with patch('time.time', return_value=160.0):
            self.tracker.start_time = 100.0  # 60 seconds total

            self.tracker.complete()

            # Verify completion state
            self.assertEqual(self.tracker.processed_players, self.tracker.total_players)

            # Verify completion message was logged
            self.mock_logger.progress.assert_called_once()
            call_args = self.mock_logger.progress.call_args[0][0]
            self.assertIn("Completed processing 100 players in 1m", call_args)

    def test_completion_triggers_logging(self):
        """Test that reaching total players always triggers logging"""
        self.tracker.processed_players = 95

        # This should trigger logging even though it's not a multiple of update_frequency
        result = self.tracker.update(increment=5)
        self.assertTrue(result)
        self.assertEqual(self.tracker.processed_players, 100)

    def test_automatic_detection_small_total(self):
        """Test progress tracking works with small total player counts"""
        small_tracker = ProgressTracker(
            total_players=15,
            update_frequency=10,
            logger=self.mock_logger
        )

        # Should work fine with small numbers
        small_tracker.update(increment=15)
        self.assertEqual(small_tracker.processed_players, 15)

    def test_eta_edge_cases(self):
        """Test ETA calculation edge cases"""
        # Test when complete
        self.tracker.processed_players = self.tracker.total_players
        eta = self.tracker._calculate_eta()
        self.assertEqual(eta, "Complete")

        # Test with zero processed players
        self.tracker.processed_players = 0
        eta = self.tracker._calculate_eta()
        self.assertEqual(eta, "")

    def test_recent_performance_window(self):
        """Test that recent performance window is properly maintained"""
        # Fill up the recent times beyond capacity
        for i in range(30):  # More than eta_window_size (20)
            self.tracker.recent_times.append(float(i))

        # Should only keep the most recent 20 values
        self.assertEqual(len(self.tracker.recent_times), 20)
        self.assertEqual(list(self.tracker.recent_times)[-1], 29.0)


class TestProgressTrackerIntegration(unittest.TestCase):
    """Integration tests for ProgressTracker"""

    def test_realistic_usage_pattern(self):
        """Test realistic usage pattern with varying processing times"""
        mock_logger = MagicMock()
        mock_logger.progress = MagicMock()

        tracker = ProgressTracker(
            total_players=50,
            update_frequency=5,
            eta_window_size=10,
            logger=mock_logger
        )

        # Simulate processing players with varying times
        start_time = time.time()
        tracker.start_time = start_time

        processed = 0
        for batch in [3, 2, 5, 7, 3, 5, 10, 15]:  # Total: 50
            # Simulate some processing time
            time.sleep(0.01)  # Small delay to generate realistic timing

            result = tracker.update(increment=batch)
            processed += batch

            # Check logging behavior
            if processed % 5 == 0 or processed >= 50:
                self.assertTrue(result, f"Should log at processed={processed}")
            else:
                self.assertFalse(result, f"Should not log at processed={processed}")

        # Verify final state
        self.assertEqual(tracker.processed_players, 50)
        self.assertTrue(len(tracker.recent_times) > 0)


if __name__ == '__main__':
    unittest.main()