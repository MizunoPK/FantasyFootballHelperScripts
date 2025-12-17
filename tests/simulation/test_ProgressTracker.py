"""
Unit tests for ProgressTracker module

Tests progress tracking, time calculations, and display formatting.

Author: Kai Mizuno
"""

import pytest
import time
from unittest.mock import Mock, patch, call
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from simulation.shared.ProgressTracker import ProgressTracker, MultiLevelProgressTracker


class TestProgressTrackerInitialization:
    """Test ProgressTracker initialization"""

    def test_init_basic(self):
        """Test basic initialization"""
        tracker = ProgressTracker(total=100)

        assert tracker.total == 100
        assert tracker.completed == 0
        assert tracker.description == "Progress"
        assert tracker.start_time > 0
        assert tracker.last_update_time == tracker.start_time

    def test_init_with_description(self):
        """Test initialization with custom description"""
        tracker = ProgressTracker(total=50, description="Testing")

        assert tracker.total == 50
        assert tracker.description == "Testing"

    def test_init_zero_total(self):
        """Test initialization with zero total"""
        tracker = ProgressTracker(total=0)

        assert tracker.total == 0
        assert tracker.completed == 0

    def test_init_large_total(self):
        """Test initialization with large total"""
        tracker = ProgressTracker(total=1000000)

        assert tracker.total == 1000000


class TestProgressTrackerUpdate:
    """Test update method"""

    @patch.object(ProgressTracker, 'display')
    def test_update_default_increment(self, mock_display):
        """Test update with default increment of 1"""
        tracker = ProgressTracker(total=100)

        tracker.update()

        assert tracker.completed == 1
        mock_display.assert_called_once()

    @patch.object(ProgressTracker, 'display')
    def test_update_custom_increment(self, mock_display):
        """Test update with custom increment"""
        tracker = ProgressTracker(total=100)

        tracker.update(increment=5)

        assert tracker.completed == 5
        mock_display.assert_called_once()

    @patch.object(ProgressTracker, 'display')
    def test_update_multiple_times(self, mock_display):
        """Test multiple updates accumulate"""
        tracker = ProgressTracker(total=100)

        tracker.update(increment=10)
        tracker.update(increment=20)
        tracker.update(increment=15)

        assert tracker.completed == 45
        assert mock_display.call_count == 3

    @patch.object(ProgressTracker, 'display')
    def test_update_updates_last_update_time(self, mock_display):
        """Test that update refreshes last_update_time"""
        tracker = ProgressTracker(total=100)
        initial_time = tracker.last_update_time

        time.sleep(0.01)
        tracker.update()

        assert tracker.last_update_time > initial_time


class TestProgressTrackerSetCompleted:
    """Test set_completed method"""

    @patch.object(ProgressTracker, 'display')
    def test_set_completed_basic(self, mock_display):
        """Test setting absolute completion count"""
        tracker = ProgressTracker(total=100)

        tracker.set_completed(50)

        assert tracker.completed == 50
        mock_display.assert_called_once()

    @patch.object(ProgressTracker, 'display')
    def test_set_completed_overwrite(self, mock_display):
        """Test that set_completed overwrites previous value"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 30

        tracker.set_completed(50)

        assert tracker.completed == 50

    @patch.object(ProgressTracker, 'display')
    def test_set_completed_to_zero(self, mock_display):
        """Test setting completed to zero"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 50

        tracker.set_completed(0)

        assert tracker.completed == 0

    @patch.object(ProgressTracker, 'display')
    def test_set_completed_updates_last_update_time(self, mock_display):
        """Test that set_completed refreshes last_update_time"""
        tracker = ProgressTracker(total=100)
        initial_time = tracker.last_update_time

        time.sleep(0.01)
        tracker.set_completed(50)

        assert tracker.last_update_time > initial_time


class TestProgressTrackerGetElapsedTime:
    """Test get_elapsed_time method"""

    def test_get_elapsed_time_immediate(self):
        """Test elapsed time immediately after creation"""
        tracker = ProgressTracker(total=100)

        elapsed = tracker.get_elapsed_time()

        assert elapsed >= 0
        assert elapsed < 1  # Should be very small

    def test_get_elapsed_time_after_delay(self):
        """Test elapsed time after a delay"""
        tracker = ProgressTracker(total=100)

        time.sleep(0.1)
        elapsed = tracker.get_elapsed_time()

        assert elapsed >= 0.1
        assert elapsed < 0.5  # Reasonable upper bound

    def test_get_elapsed_time_increases(self):
        """Test that elapsed time increases"""
        tracker = ProgressTracker(total=100)

        elapsed1 = tracker.get_elapsed_time()
        time.sleep(0.05)
        elapsed2 = tracker.get_elapsed_time()

        assert elapsed2 > elapsed1


class TestProgressTrackerGetETA:
    """Test get_eta method"""

    def test_get_eta_no_progress(self):
        """Test ETA with no progress returns None"""
        tracker = ProgressTracker(total=100)

        eta = tracker.get_eta()

        assert eta is None

    def test_get_eta_with_progress(self):
        """Test ETA calculation with progress"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 50

        # Simulate some time elapsed
        tracker.start_time = time.time() - 10.0  # 10 seconds elapsed

        eta = tracker.get_eta()

        assert eta is not None
        # 50% done in 10 seconds -> ~10 seconds remaining
        assert 8 < eta < 12

    def test_get_eta_near_completion(self):
        """Test ETA near completion"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 99
        tracker.start_time = time.time() - 99.0

        eta = tracker.get_eta()

        assert eta is not None
        assert eta < 2  # Should be very small

    def test_get_eta_complete(self):
        """Test ETA when complete"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 100
        tracker.start_time = time.time() - 100.0

        eta = tracker.get_eta()

        assert eta == 0.0


class TestProgressTrackerGetPercentage:
    """Test get_percentage method"""

    def test_get_percentage_zero_progress(self):
        """Test percentage with no progress"""
        tracker = ProgressTracker(total=100)

        assert tracker.get_percentage() == 0.0

    def test_get_percentage_half_complete(self):
        """Test percentage at 50%"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 50

        assert tracker.get_percentage() == 50.0

    def test_get_percentage_complete(self):
        """Test percentage at 100%"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 100

        assert tracker.get_percentage() == 100.0

    def test_get_percentage_zero_total(self):
        """Test percentage with zero total returns 100%"""
        tracker = ProgressTracker(total=0)

        assert tracker.get_percentage() == 100.0

    def test_get_percentage_fractional(self):
        """Test percentage with fractional result"""
        tracker = ProgressTracker(total=3)
        tracker.completed = 1

        percentage = tracker.get_percentage()
        assert 33.0 < percentage < 34.0

    def test_get_percentage_over_total(self):
        """Test percentage when completed exceeds total"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 150

        assert tracker.get_percentage() == 150.0


class TestProgressTrackerFormatTime:
    """Test format_time method"""

    def test_format_time_seconds_only(self):
        """Test formatting seconds only"""
        tracker = ProgressTracker(total=100)

        assert tracker.format_time(30) == "30s"
        assert tracker.format_time(0) == "0s"
        assert tracker.format_time(59) == "59s"

    def test_format_time_minutes_and_seconds(self):
        """Test formatting minutes and seconds"""
        tracker = ProgressTracker(total=100)

        assert tracker.format_time(60) == "1m 0s"
        assert tracker.format_time(90) == "1m 30s"
        assert tracker.format_time(3599) == "59m 59s"

    def test_format_time_hours_and_minutes(self):
        """Test formatting hours and minutes"""
        tracker = ProgressTracker(total=100)

        assert tracker.format_time(3600) == "1h 0m"
        assert tracker.format_time(3660) == "1h 1m"
        assert tracker.format_time(7200) == "2h 0m"
        assert tracker.format_time(7380) == "2h 3m"

    def test_format_time_large_hours(self):
        """Test formatting large hour values"""
        tracker = ProgressTracker(total=100)

        result = tracker.format_time(36000)  # 10 hours
        assert "10h" in result


class TestProgressTrackerCreateProgressBar:
    """Test create_progress_bar method"""

    def test_create_progress_bar_empty(self):
        """Test progress bar at 0%"""
        tracker = ProgressTracker(total=100)

        bar = tracker.create_progress_bar(width=20)

        assert bar == "[                    ]"

    def test_create_progress_bar_half(self):
        """Test progress bar at 50%"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 50

        bar = tracker.create_progress_bar(width=20)

        assert bar.startswith("[")
        assert bar.endswith("]")
        assert ">" in bar  # Arrow indicator
        assert "=" in bar  # Filled portion

    def test_create_progress_bar_full(self):
        """Test progress bar at 100%"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 100

        bar = tracker.create_progress_bar(width=20)

        assert bar == "[====================]"

    def test_create_progress_bar_custom_width(self):
        """Test progress bar with custom width"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 50

        bar = tracker.create_progress_bar(width=10)

        assert len(bar) == 12  # width + 2 brackets

    def test_create_progress_bar_near_start(self):
        """Test progress bar with small progress"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 5

        bar = tracker.create_progress_bar(width=20)

        assert bar.startswith("[")
        assert ">" in bar


class TestProgressTrackerDisplay:
    """Test display method"""

    @patch('builtins.print')
    def test_display_basic(self, mock_print):
        """Test basic display output"""
        tracker = ProgressTracker(total=100, description="Test")
        tracker.completed = 50

        tracker.display()

        mock_print.assert_called()
        call_args = str(mock_print.call_args)
        assert "Test" in call_args
        assert "50" in call_args  # Percentage or count

    @patch('builtins.print')
    def test_display_shows_percentage(self, mock_print):
        """Test display shows percentage"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 75

        tracker.display()

        call_args = str(mock_print.call_args)
        assert "75" in call_args

    @patch('builtins.print')
    def test_display_at_completion(self, mock_print):
        """Test display at completion adds newline"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 100

        tracker.display()

        # Should have two print calls: main display and final newline
        assert mock_print.call_count == 2

    @patch('builtins.print')
    def test_display_before_completion(self, mock_print):
        """Test display before completion doesn't add newline"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 50

        tracker.display()

        # Should have only one print call (no final newline)
        assert mock_print.call_count == 1


class TestProgressTrackerFinish:
    """Test finish method"""

    @patch('builtins.print')
    def test_finish_sets_completed(self, mock_print):
        """Test finish sets completed to total"""
        tracker = ProgressTracker(total=100)
        tracker.completed = 50

        tracker.finish()

        assert tracker.completed == 100

    @patch('builtins.print')
    def test_finish_prints_message(self, mock_print):
        """Test finish prints completion message"""
        tracker = ProgressTracker(total=100, description="Test Task")

        tracker.finish()

        call_args = str(mock_print.call_args)
        assert "Complete" in call_args or "complete" in call_args
        assert "Test Task" in call_args


class TestMultiLevelProgressTrackerInitialization:
    """Test MultiLevelProgressTracker initialization"""

    def test_init_basic(self):
        """Test basic initialization"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        assert tracker.outer_total == 10
        assert tracker.inner_total == 100
        assert tracker.outer_completed == 0
        assert tracker.inner_completed == 0
        assert tracker.outer_desc == "Configs"
        assert tracker.inner_desc == "Simulations"

    def test_init_with_descriptions(self):
        """Test initialization with custom descriptions"""
        tracker = MultiLevelProgressTracker(
            outer_total=5,
            inner_total=20,
            outer_desc="Batches",
            inner_desc="Items"
        )

        assert tracker.outer_desc == "Batches"
        assert tracker.inner_desc == "Items"

    def test_init_zero_values(self):
        """Test initialization with zero values"""
        tracker = MultiLevelProgressTracker(outer_total=0, inner_total=0)

        assert tracker.outer_total == 0
        assert tracker.inner_total == 0


class TestMultiLevelProgressTrackerUpdateInner:
    """Test update_inner method"""

    @patch.object(MultiLevelProgressTracker, 'display')
    def test_update_inner_basic(self, mock_display):
        """Test updating inner progress"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        tracker.update_inner(50)

        assert tracker.inner_completed == 50
        mock_display.assert_called_once()

    @patch.object(MultiLevelProgressTracker, 'display')
    def test_update_inner_overwrite(self, mock_display):
        """Test that update_inner overwrites previous value"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)
        tracker.inner_completed = 30

        tracker.update_inner(70)

        assert tracker.inner_completed == 70

    @patch.object(MultiLevelProgressTracker, 'display')
    def test_update_inner_to_total(self, mock_display):
        """Test updating inner to total"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        tracker.update_inner(100)

        assert tracker.inner_completed == 100


class TestMultiLevelProgressTrackerNextOuter:
    """Test next_outer method"""

    @patch.object(MultiLevelProgressTracker, 'display')
    def test_next_outer_increments(self, mock_display):
        """Test next_outer increments outer count"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        tracker.next_outer()

        assert tracker.outer_completed == 1
        mock_display.assert_called_once()

    @patch.object(MultiLevelProgressTracker, 'display')
    def test_next_outer_resets_inner(self, mock_display):
        """Test next_outer resets inner progress"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)
        tracker.inner_completed = 75

        tracker.next_outer()

        assert tracker.inner_completed == 0

    @patch.object(MultiLevelProgressTracker, 'display')
    def test_next_outer_multiple_times(self, mock_display):
        """Test calling next_outer multiple times"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        tracker.next_outer()
        tracker.next_outer()
        tracker.next_outer()

        assert tracker.outer_completed == 3
        assert tracker.inner_completed == 0


class TestMultiLevelProgressTrackerGetOverallPercentage:
    """Test get_overall_percentage method"""

    def test_get_overall_percentage_no_progress(self):
        """Test overall percentage with no progress"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        assert tracker.get_overall_percentage() == 0.0

    def test_get_overall_percentage_one_outer_complete(self):
        """Test overall percentage with one outer item complete"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)
        tracker.outer_completed = 1

        # 1 out of 10 outer = 100 out of 1000 total = 10%
        assert tracker.get_overall_percentage() == 10.0

    def test_get_overall_percentage_partial_inner(self):
        """Test overall percentage with partial inner progress"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)
        tracker.outer_completed = 1
        tracker.inner_completed = 50

        # 1*100 + 50 = 150 out of 1000 = 15%
        assert tracker.get_overall_percentage() == 15.0

    def test_get_overall_percentage_complete(self):
        """Test overall percentage when complete"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)
        tracker.outer_completed = 10

        assert tracker.get_overall_percentage() == 100.0

    def test_get_overall_percentage_zero_total(self):
        """Test overall percentage with zero total returns 100%"""
        tracker = MultiLevelProgressTracker(outer_total=0, inner_total=0)

        assert tracker.get_overall_percentage() == 100.0


class TestMultiLevelProgressTrackerGetETA:
    """Test get_eta method for MultiLevelProgressTracker"""

    def test_get_eta_no_progress(self):
        """Test ETA with no progress returns None"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        eta = tracker.get_eta()

        assert eta is None

    def test_get_eta_with_progress(self):
        """Test ETA calculation with progress"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)
        tracker.outer_completed = 5
        tracker.inner_completed = 50
        tracker.start_time = time.time() - 100.0  # 100 seconds elapsed

        eta = tracker.get_eta()

        assert eta is not None
        # 550/1000 complete in 100s -> ~82s remaining
        assert 70 < eta < 95

    def test_get_eta_near_completion(self):
        """Test ETA near completion"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)
        tracker.outer_completed = 9
        tracker.inner_completed = 99
        tracker.start_time = time.time() - 999.0

        eta = tracker.get_eta()

        assert eta is not None
        assert eta < 2


class TestMultiLevelProgressTrackerFormatTime:
    """Test format_time method for MultiLevelProgressTracker"""

    def test_format_time_seconds(self):
        """Test formatting seconds"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        assert tracker.format_time(45) == "45s"

    def test_format_time_minutes(self):
        """Test formatting minutes"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        assert tracker.format_time(120) == "2m 0s"

    def test_format_time_hours(self):
        """Test formatting hours"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)

        assert tracker.format_time(3600) == "1h 0m"


class TestMultiLevelProgressTrackerDisplay:
    """Test display method for MultiLevelProgressTracker"""

    @patch('builtins.print')
    def test_display_basic(self, mock_print):
        """Test basic display output"""
        tracker = MultiLevelProgressTracker(
            outer_total=10,
            inner_total=100,
            outer_desc="Configs",
            inner_desc="Sims"
        )
        tracker.outer_completed = 5
        tracker.inner_completed = 50

        tracker.display()

        mock_print.assert_called()
        # Check all calls since display() calls print() multiple times
        all_calls = str(mock_print.call_args_list)
        assert "Configs" in all_calls
        assert "Sims" in all_calls

    @patch('builtins.print')
    def test_display_at_completion(self, mock_print):
        """Test display at completion adds newline"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)
        tracker.outer_completed = 10

        tracker.display()

        # Should call print at least twice (main display + newline)
        assert mock_print.call_count >= 2


class TestMultiLevelProgressTrackerFinish:
    """Test finish method for MultiLevelProgressTracker"""

    @patch('builtins.print')
    def test_finish_sets_completed(self, mock_print):
        """Test finish sets both levels to complete"""
        tracker = MultiLevelProgressTracker(outer_total=10, inner_total=100)
        tracker.outer_completed = 5
        tracker.inner_completed = 50

        tracker.finish()

        assert tracker.outer_completed == 10
        assert tracker.inner_completed == 100

    @patch('builtins.print')
    def test_finish_prints_message(self, mock_print):
        """Test finish prints completion message"""
        tracker = MultiLevelProgressTracker(
            outer_total=10,
            inner_total=100,
            outer_desc="Batches",
            inner_desc="Items"
        )

        tracker.finish()

        call_args = str(mock_print.call_args)
        assert "Complete" in call_args or "complete" in call_args


class TestProgressTrackerEdgeCases:
    """Test edge cases for ProgressTracker"""

    @patch.object(ProgressTracker, 'display')
    def test_progress_beyond_total(self, mock_display):
        """Test handling progress beyond total"""
        tracker = ProgressTracker(total=100)

        tracker.set_completed(150)

        assert tracker.completed == 150
        assert tracker.get_percentage() == 150.0

    def test_immediate_completion(self):
        """Test immediate completion without intermediate progress"""
        tracker = ProgressTracker(total=100)

        tracker.completed = 100

        assert tracker.get_percentage() == 100.0

    def test_very_large_total(self):
        """Test with very large total"""
        tracker = ProgressTracker(total=1000000)
        tracker.completed = 500000

        assert tracker.get_percentage() == 50.0


class TestMultiLevelProgressTrackerEdgeCases:
    """Test edge cases for MultiLevelProgressTracker"""

    def test_single_outer_single_inner(self):
        """Test with single item at each level"""
        tracker = MultiLevelProgressTracker(outer_total=1, inner_total=1)
        tracker.outer_completed = 1

        assert tracker.get_overall_percentage() == 100.0

    def test_asymmetric_totals(self):
        """Test with asymmetric totals"""
        tracker = MultiLevelProgressTracker(outer_total=3, inner_total=7)
        tracker.outer_completed = 1
        tracker.inner_completed = 3

        # 1*7 + 3 = 10 out of 21 total
        percentage = tracker.get_overall_percentage()
        assert 47 < percentage < 48  # ~47.6%


class TestProgressTrackerIntegration:
    """Test realistic integration scenarios"""

    @patch.object(ProgressTracker, 'display')
    def test_realistic_progress_sequence(self, mock_display):
        """Test realistic progress sequence"""
        tracker = ProgressTracker(total=100, description="Processing")

        # Simulate processing 10 items at a time
        for i in range(10):
            tracker.update(increment=10)

        assert tracker.completed == 100
        assert tracker.get_percentage() == 100.0
        assert mock_display.call_count == 10

    @patch.object(MultiLevelProgressTracker, 'display')
    def test_multilevel_realistic_sequence(self, mock_display):
        """Test realistic multi-level progress sequence"""
        tracker = MultiLevelProgressTracker(
            outer_total=5,
            inner_total=20,
            outer_desc="Configs",
            inner_desc="Simulations"
        )

        # Simulate processing 5 configs, each with 20 simulations
        for config_num in range(5):
            for sim_num in range(1, 21):
                tracker.update_inner(sim_num)
            tracker.next_outer()

        assert tracker.outer_completed == 5
        assert tracker.get_overall_percentage() == 100.0
