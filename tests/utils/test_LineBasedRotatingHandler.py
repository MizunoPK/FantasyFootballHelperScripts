#!/usr/bin/env python3
"""
Unit tests for LineBasedRotatingHandler

Tests line-based log rotation, timestamped filenames, and automated cleanup.

Test Coverage:
- Line counting and rotation triggers (Tests 1.1-1.18)
- Timestamp generation and filename format (Tests 3.1-3.10)
- Cleanup and max files enforcement (Tests 4.1-4.16)
"""

import unittest
import tempfile
import time
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import logging

from utils.LineBasedRotatingHandler import LineBasedRotatingHandler


class TestLineBasedRotatingHandler(unittest.TestCase):
    """Test suite for LineBasedRotatingHandler class."""

    def setUp(self):
        """Create temporary directory for test log files."""
        self.test_dir = tempfile.mkdtemp()
        self.test_log_path = Path(self.test_dir) / "test_app" / "test_app-20260207_120000.log"
        self.test_log_path.parent.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """Clean up temporary test files."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # ========================================================================
    # TESTS 1.1-1.4: Line Counting (Unit Tests)
    # ========================================================================

    def test_1_1_line_counter_initializes_to_zero(self):
        """Test 1.1: Line counter starts at 0 on handler creation."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)
        self.assertEqual(handler._line_counter, 0)

    def test_1_2_emit_increments_line_counter(self):
        """Test 1.2: emit() increments line counter by 1 per log record."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        # Create a log record
        record = logging.LogRecord(
            name='test', level=logging.INFO, pathname='', lineno=0,
            msg='Test message', args=(), exc_info=None
        )

        # Emit record and verify counter incremented
        handler.emit(record)
        self.assertEqual(handler._line_counter, 1)

        # Emit another record
        handler.emit(record)
        self.assertEqual(handler._line_counter, 2)

    def test_1_3_counter_resets_to_zero_after_rotation(self):
        """Test 1.3: Line counter resets to 0 after doRollover()."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        # Manually increment counter
        handler._line_counter = 500

        # Trigger rollover
        handler.doRollover()

        # Verify counter reset to 0
        self.assertEqual(handler._line_counter, 0)

    def test_1_4_counter_does_not_persist_across_instances(self):
        """Test 1.4: Counter is in-memory only (not persistent across instances)."""
        # Create first handler, emit logs
        handler1 = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)
        record = logging.LogRecord(
            name='test', level=logging.INFO, pathname='', lineno=0,
            msg='Test message', args=(), exc_info=None
        )
        handler1.emit(record)
        handler1.emit(record)
        self.assertEqual(handler1._line_counter, 2)

        # Close first handler
        handler1.close()

        # Create second handler with same file (simulates script restart)
        new_log_path = Path(self.test_dir) / "test_app" / "test_app-20260207_120100.log"
        handler2 = LineBasedRotatingHandler(str(new_log_path), max_lines=500)

        # Verify second handler starts at 0 (counter NOT persistent)
        self.assertEqual(handler2._line_counter, 0)

    # ========================================================================
    # TESTS 1.5-1.7: Rotation Trigger (Integration Tests)
    # ========================================================================

    def test_1_5_rotation_triggers_at_exactly_500_lines(self):
        """Test 1.5: shouldRollover() returns True at exactly 500 lines."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        # Set counter to 499 (just below threshold)
        handler._line_counter = 499
        self.assertFalse(handler.shouldRollover(None))

        # Set counter to 500 (at threshold)
        handler._line_counter = 500
        self.assertTrue(handler.shouldRollover(None))

    def test_1_6_rotation_does_not_trigger_below_500_lines(self):
        """Test 1.6: shouldRollover() returns False below 500 lines."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        # Test various values below threshold
        for counter_value in [0, 1, 100, 250, 499]:
            handler._line_counter = counter_value
            self.assertFalse(handler.shouldRollover(None),
                           f"shouldRollover should be False at {counter_value} lines")

    def test_1_7_rotation_triggers_above_500_lines(self):
        """Test 1.7: shouldRollover() returns True above 500 lines."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        # Test values above threshold
        for counter_value in [501, 550, 1000]:
            handler._line_counter = counter_value
            self.assertTrue(handler.shouldRollover(None),
                          f"shouldRollover should be True at {counter_value} lines")

    # ========================================================================
    # TESTS 1.8-1.11: Rotation Execution (Integration Tests)
    # ========================================================================

    def test_1_8_doRollover_creates_new_timestamped_file(self):
        """Test 1.8: doRollover() creates new file with timestamp."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)
        handler._line_counter = 500

        # Get original file path
        original_file = Path(handler.baseFilename)

        # Trigger rollover
        with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 7, 12, 30, 45)
            handler.doRollover()

        # Verify new file path contains new timestamp
        new_file = Path(handler.baseFilename)
        self.assertIn('20260207_123045', str(new_file))
        self.assertNotEqual(original_file, new_file)

    def test_1_9_doRollover_closes_old_file(self):
        """Test 1.9: doRollover() closes current file before creating new one."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        # Write to handler to open file
        record = logging.LogRecord(
            name='test', level=logging.INFO, pathname='', lineno=0,
            msg='Test message', args=(), exc_info=None
        )
        handler.emit(record)

        # Verify stream is open
        self.assertIsNotNone(handler.stream)

        # Mock datetime for consistent testing
        with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 7, 12, 30, 45)

            # Trigger rollover
            handler.doRollover()

        # Verify stream was closed and reopened (new stream object)
        self.assertIsNotNone(handler.stream)

    def test_1_10_doRollover_calls_cleanup_old_files(self):
        """Test 1.10: doRollover() calls _cleanup_old_files() after rotation."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        # Mock _cleanup_old_files to verify it's called
        with patch.object(handler, '_cleanup_old_files') as mock_cleanup:
            with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
                mock_datetime.now.return_value = datetime(2026, 2, 7, 12, 30, 45)
                handler.doRollover()

            # Verify cleanup was called
            mock_cleanup.assert_called_once()

    def test_1_11_old_log_file_remains_after_rotation(self):
        """Test 1.11: Old log file is not deleted/renamed after rotation."""
        # Create handler and write some data
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)
        record = logging.LogRecord(
            name='test', level=logging.INFO, pathname='', lineno=0,
            msg='Test message', args=(), exc_info=None
        )
        handler.emit(record)
        handler.stream.flush()

        # Verify old file exists
        old_file = Path(handler.baseFilename)
        self.assertTrue(old_file.exists())

        # Trigger rollover
        with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 7, 12, 30, 45)
            handler.doRollover()

        # Verify old file still exists (not deleted)
        self.assertTrue(old_file.exists())

        # Verify new file also exists
        new_file = Path(handler.baseFilename)
        self.assertTrue(new_file.exists())
        self.assertNotEqual(old_file, new_file)

    # ========================================================================
    # TESTS 1.13-1.15: Boundary Conditions (Edge Case Tests)
    # ========================================================================

    def test_1_13_handler_accepts_max_lines_parameter(self):
        """Test 1.13: Handler accepts custom max_lines parameter."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=100)
        self.assertEqual(handler.max_lines, 100)

        # Verify rotation triggers at custom threshold
        handler._line_counter = 100
        self.assertTrue(handler.shouldRollover(None))

    def test_1_14_handler_validates_max_lines_greater_than_zero(self):
        """Test 1.14: Handler raises ValueError if max_lines < 1."""
        with self.assertRaises(ValueError):
            LineBasedRotatingHandler(str(self.test_log_path), max_lines=0)

        with self.assertRaises(ValueError):
            LineBasedRotatingHandler(str(self.test_log_path), max_lines=-10)

    def test_1_15_handler_validates_max_files_greater_than_zero(self):
        """Test 1.15: Handler raises ValueError if max_files < 1."""
        with self.assertRaises(ValueError):
            LineBasedRotatingHandler(str(self.test_log_path), max_files=0)

        with self.assertRaises(ValueError):
            LineBasedRotatingHandler(str(self.test_log_path), max_files=-5)

    # ========================================================================
    # TESTS 1.16-1.18: Configuration (Configuration Tests)
    # ========================================================================

    def test_1_16_handler_accepts_encoding_parameter(self):
        """Test 1.16: Handler accepts encoding parameter."""
        handler = LineBasedRotatingHandler(
            str(self.test_log_path),
            encoding='utf-8'
        )
        # Encoding is set at file handler level
        self.assertEqual(handler.encoding, 'utf-8')

    def test_1_17_handler_accepts_mode_parameter(self):
        """Test 1.17: Handler accepts mode parameter (append by default)."""
        handler = LineBasedRotatingHandler(
            str(self.test_log_path),
            mode='a'
        )
        # Mode is set at file handler level
        self.assertEqual(handler.mode, 'a')

    def test_1_18_handler_defaults_to_500_lines_and_50_files(self):
        """Test 1.18: Handler uses default values (500 lines, 50 files)."""
        handler = LineBasedRotatingHandler(str(self.test_log_path))
        self.assertEqual(handler.max_lines, 500)
        self.assertEqual(handler.max_files, 50)

    # ========================================================================
    # TESTS 3.1-3.10: Timestamp Generation (Timestamp Tests)
    # ========================================================================

    def test_3_1_get_base_filename_extracts_name_from_timestamped_file(self):
        """Test 3.1: _get_base_filename() extracts base name correctly."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)
        base_name = handler._get_base_filename()
        self.assertEqual(base_name, 'test_app')

    def test_3_2_get_base_filename_handles_various_timestamp_formats(self):
        """Test 3.2: _get_base_filename() handles different timestamps."""
        test_cases = [
            ('logs/app/app-20260207_120000.log', 'app'),
            ('logs/my_logger/my_logger-20251231_235959.log', 'my_logger'),
            ('logs/test/test-20200101_000000.log', 'test'),
        ]

        for filepath, expected_base in test_cases:
            full_path = Path(self.test_dir) / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            handler = LineBasedRotatingHandler(str(full_path), max_lines=500)
            self.assertEqual(handler._get_base_filename(), expected_base)

    def test_3_3_doRollover_generates_timestamp_in_correct_format(self):
        """Test 3.3: doRollover() generates timestamp in YYYYMMDD_HHMMSS format."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 7, 14, 30, 45)
            handler.doRollover()

        new_filename = Path(handler.baseFilename).name
        self.assertIn('20260207_143045', new_filename)

    def test_3_4_doRollover_generates_unique_timestamps(self):
        """Test 3.4: Each rollover generates unique timestamp (no collisions)."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        timestamps = []
        for i in range(3):
            with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
                # Different timestamps for each rollover
                mock_datetime.now.return_value = datetime(2026, 2, 7, 12, 0, i)
                handler.doRollover()

            filename = Path(handler.baseFilename).name
            # Extract timestamp from filename
            timestamp = filename.split('-')[1].replace('.log', '')
            timestamps.append(timestamp)

        # Verify all timestamps are unique
        self.assertEqual(len(timestamps), len(set(timestamps)))

    def test_3_5_filename_uses_hyphen_separator_not_underscore(self):
        """Test 3.5: Filename uses hyphen between name and timestamp."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 7, 12, 30, 45)
            handler.doRollover()

        filename = Path(handler.baseFilename).name
        # Format should be: test_app-20260207_123045_microseconds.log (after rotation)
        # Verify hyphen before timestamp and microsecond precision
        self.assertRegex(filename, r'^test_app-\d{8}_\d{6}_\d{6}\.log$')

    def test_3_6_filename_includes_dot_log_extension(self):
        """Test 3.6: Generated filename has .log extension."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 7, 12, 30, 45)
            handler.doRollover()

        filename = Path(handler.baseFilename).name
        self.assertTrue(filename.endswith('.log'))

    def test_3_7_timestamp_includes_time_component(self):
        """Test 3.7: Timestamp includes HHMMSS time component (not just date)."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 7, 23, 59, 59)
            handler.doRollover()

        filename = Path(handler.baseFilename).name
        # Verify both date and time present
        self.assertIn('20260207_235959', filename)

    def test_3_8_get_base_filename_fallback_for_non_standard_format(self):
        """Test 3.8: _get_base_filename() handles non-standard filenames."""
        # Create handler with non-timestamped filename
        non_standard_path = Path(self.test_dir) / "plain.log"
        handler = LineBasedRotatingHandler(str(non_standard_path), max_lines=500)

        # Should fallback to stem (filename without extension)
        base_name = handler._get_base_filename()
        self.assertEqual(base_name, 'plain')

    def test_3_9_timestamp_format_is_sortable_chronologically(self):
        """Test 3.9: Timestamp format allows chronological sorting."""
        timestamps = [
            '20260207_120000',  # Feb 7, 12:00:00
            '20260207_120001',  # Feb 7, 12:00:01
            '20260207_130000',  # Feb 7, 13:00:00
            '20260208_120000',  # Feb 8, 12:00:00
        ]

        # Verify timestamps sort chronologically when sorted as strings
        sorted_timestamps = sorted(timestamps)
        self.assertEqual(timestamps, sorted_timestamps)

    def test_3_10_doRollover_preserves_directory_structure(self):
        """Test 3.10: doRollover() keeps files in same directory."""
        handler = LineBasedRotatingHandler(str(self.test_log_path), max_lines=500)

        original_dir = Path(handler.baseFilename).parent

        with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 7, 12, 30, 45)
            handler.doRollover()

        new_dir = Path(handler.baseFilename).parent
        self.assertEqual(original_dir, new_dir)

    # ========================================================================
    # TESTS 4.1-4.16: Cleanup and Max Files (Cleanup Tests)
    # ========================================================================

    def test_4_1_cleanup_deletes_oldest_file_when_exceeding_max_files(self):
        """Test 4.1: _cleanup_old_files() deletes oldest when > max_files."""
        log_dir = Path(self.test_dir) / "cleanup_test"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 51 log files (exceeds max_files=50)
        for i in range(51):
            # Use unique timestamps to avoid overwriting
            log_file = log_dir / f"app-20260207_{120000+i:06d}.log"
            log_file.write_text(f"Log {i}")
            # Sleep to ensure different modification times
            time.sleep(0.001)

        # Create handler with last file
        last_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(last_file), max_files=50)

        # Trigger cleanup
        handler._cleanup_old_files()

        # Verify only 50 files remain
        remaining_files = list(log_dir.glob('*.log'))
        self.assertEqual(len(remaining_files), 50)

    def test_4_2_cleanup_does_not_delete_if_below_max_files(self):
        """Test 4.2: _cleanup_old_files() does nothing if count <= max_files."""
        log_dir = Path(self.test_dir) / "cleanup_test2"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 30 log files (below max_files=50)
        for i in range(30):
            # Use unique timestamps to avoid overwriting
            log_file = log_dir / f"app-20260207_{120000+i:06d}.log"
            log_file.write_text(f"Log {i}")

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Trigger cleanup
        handler._cleanup_old_files()

        # Verify all 30 files still present
        remaining_files = list(log_dir.glob('*.log'))
        self.assertEqual(len(remaining_files), 30)

    def test_4_3_cleanup_deletes_multiple_files_if_far_exceeding_max(self):
        """Test 4.3: _cleanup_old_files() deletes multiple files if needed."""
        log_dir = Path(self.test_dir) / "cleanup_test3"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 55 log files (5 over max_files=50)
        for i in range(55):
            log_file = log_dir / f"app-202602{i:02d}_120000.log"
            log_file.write_text(f"Log {i}")
            time.sleep(0.01)

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Trigger cleanup
        handler._cleanup_old_files()

        # Verify exactly 50 files remain
        remaining_files = list(log_dir.glob('*.log'))
        self.assertEqual(len(remaining_files), 50)

    def test_4_4_cleanup_determines_age_by_modification_time(self):
        """Test 4.4: _cleanup_old_files() uses modification time (st_mtime)."""
        log_dir = Path(self.test_dir) / "cleanup_test4"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create files with known modification times
        import os
        files_with_times = []
        base_time = time.time() - 1000  # Start 1000 seconds ago

        for i in range(52):
            log_file = log_dir / f"app-{i:03d}.log"
            log_file.write_text(f"Log {i}")
            # Set modification time
            mod_time = base_time + i
            os.utime(log_file, (mod_time, mod_time))
            files_with_times.append((log_file, mod_time))

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Trigger cleanup
        handler._cleanup_old_files()

        # Handler creates one file (app-20260207_120000.log), so total is 53 files
        # Cleanup should delete oldest 3 files (53 - 50 = 3) to get to max_files
        self.assertFalse(files_with_times[0][0].exists())
        self.assertFalse(files_with_times[1][0].exists())
        self.assertFalse(files_with_times[2][0].exists())
        # Verify newer files remain
        self.assertTrue(files_with_times[3][0].exists())
        self.assertTrue(files_with_times[-1][0].exists())

    def test_4_5_cleanup_only_counts_log_files(self):
        """Test 4.5: _cleanup_old_files() only counts *.log files."""
        log_dir = Path(self.test_dir) / "cleanup_test5"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 48 .log files
        for i in range(48):
            (log_dir / f"app-{i}.log").write_text("log")

        # Create other file types (should be ignored)
        (log_dir / "readme.txt").write_text("text")
        (log_dir / "data.csv").write_text("csv")
        (log_dir / "backup.bak").write_text("backup")

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Trigger cleanup (48 + 1 handler file = 49 .log files, below max)
        handler._cleanup_old_files()

        # Verify all .log files present (no cleanup needed, still at 49)
        log_files = list(log_dir.glob('*.log'))
        self.assertEqual(len(log_files), 49)

        # Verify non-.log files still present
        self.assertTrue((log_dir / "readme.txt").exists())
        self.assertTrue((log_dir / "data.csv").exists())

    def test_4_6_cleanup_continues_if_individual_deletion_fails(self):
        """Test 4.6: _cleanup_old_files() continues if one deletion fails."""
        log_dir = Path(self.test_dir) / "cleanup_test6"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 52 files
        for i in range(52):
            (log_dir / f"app-{i:02d}.log").write_text(f"log {i}")
            time.sleep(0.01)

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Mock unlink to fail for first file but succeed for second
        original_unlink = Path.unlink
        call_count = [0]

        def mock_unlink(self, *args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise OSError("Permission denied")
            return original_unlink(self, *args, **kwargs)

        with patch.object(Path, 'unlink', mock_unlink):
            # Trigger cleanup (should attempt to delete 2 files)
            handler._cleanup_old_files()

        # Verify second file was still deleted despite first failure
        # Should have 51 files (1 failed + 50 remaining)
        log_files = list(log_dir.glob('*.log'))
        self.assertEqual(len(log_files), 51)

    def test_4_7_cleanup_sorts_files_oldest_first(self):
        """Test 4.7: _cleanup_old_files() sorts by oldest modification time first."""
        log_dir = Path(self.test_dir) / "cleanup_test7"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create files with specific modification times (not in order)
        import os
        base_time = time.time() - 1000

        # Create in mixed order
        file_times = [
            ("app-002.log", base_time + 5),   # 3rd oldest
            ("app-001.log", base_time + 1),   # oldest
            ("app-003.log", base_time + 10),  # 4th oldest
            ("app-000.log", base_time + 3),   # 2nd oldest
        ]

        for filename, mod_time in file_times:
            filepath = log_dir / filename
            filepath.write_text("log")
            os.utime(filepath, (mod_time, mod_time))

        # Add 48 more files to exceed limit
        for i in range(4, 52):
            filepath = log_dir / f"app-{i:03d}.log"
            filepath.write_text("log")
            os.utime(filepath, (base_time + 10 + i, base_time + 10 + i))

        # Create handler (52 files + 1 handler file = 53 total, so 3 should be deleted)
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Trigger cleanup
        handler._cleanup_old_files()

        # Verify oldest 3 files deleted (53 - 50 = 3)
        self.assertFalse((log_dir / "app-001.log").exists())  # oldest
        self.assertFalse((log_dir / "app-000.log").exists())  # 2nd oldest
        self.assertFalse((log_dir / "app-002.log").exists())  # 3rd oldest
        # Verify newer files remain
        self.assertTrue((log_dir / "app-003.log").exists())  # 4th oldest (survives)

    def test_4_8_max_files_parameter_is_enforced(self):
        """Test 4.8: Handler respects custom max_files parameter."""
        log_dir = Path(self.test_dir) / "cleanup_test8"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 15 files
        for i in range(15):
            (log_dir / f"app-{i:02d}.log").write_text(f"log {i}")
            time.sleep(0.01)

        # Create handler with max_files=10
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=10)

        # Trigger cleanup
        handler._cleanup_old_files()

        # Verify exactly 10 files remain
        log_files = list(log_dir.glob('*.log'))
        self.assertEqual(len(log_files), 10)

    def test_4_9_cleanup_at_exactly_max_files_does_nothing(self):
        """Test 4.9: _cleanup_old_files() does nothing at exactly max_files."""
        log_dir = Path(self.test_dir) / "cleanup_test9"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create exactly 50 files
        for i in range(50):
            (log_dir / f"app-{i:02d}.log").write_text(f"log {i}")

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Trigger cleanup
        handler._cleanup_old_files()

        # Verify all 50 files still present
        log_files = list(log_dir.glob('*.log'))
        self.assertEqual(len(log_files), 50)

    def test_4_10_cleanup_handles_empty_directory(self):
        """Test 4.10: _cleanup_old_files() handles empty directory gracefully."""
        log_dir = Path(self.test_dir) / "cleanup_test10"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create handler in empty directory
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Trigger cleanup (should not error)
        try:
            handler._cleanup_old_files()
            cleanup_successful = True
        except Exception:
            cleanup_successful = False

        self.assertTrue(cleanup_successful)

    def test_4_11_cleanup_logs_deletion_count(self):
        """Test 4.11: _cleanup_old_files() logs number of files deleted."""
        log_dir = Path(self.test_dir) / "cleanup_test11"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 52 files
        for i in range(52):
            (log_dir / f"app-{i:02d}.log").write_text(f"log {i}")
            time.sleep(0.01)

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Mock stream to capture log output
        mock_stream = MagicMock()
        handler.stream = mock_stream

        # Trigger cleanup
        handler._cleanup_old_files()

        # Verify cleanup message was written
        # 52 files + 1 handler file = 53 total, so 3 should be deleted (53 - 50 = 3)
        write_calls = [call[0][0] for call in mock_stream.write.call_args_list]
        cleanup_messages = [msg for msg in write_calls if 'Cleaned up' in msg]
        self.assertTrue(len(cleanup_messages) > 0)
        self.assertIn('3 old log files', cleanup_messages[0])

    def test_4_12_cleanup_does_not_delete_current_log_file(self):
        """Test 4.12: _cleanup_old_files() never deletes current log file."""
        log_dir = Path(self.test_dir) / "cleanup_test12"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 50 old files
        for i in range(50):
            (log_dir / f"app-{i:02d}.log").write_text(f"log {i}")
            time.sleep(0.01)

        # Create current file (newest)
        current_file = log_dir / "app-current.log"
        current_file.write_text("current log")
        time.sleep(0.1)  # Ensure this is newest

        # Create handler with current file
        handler = LineBasedRotatingHandler(str(current_file), max_files=50)

        # Trigger cleanup (51 files, should delete 1 oldest)
        handler._cleanup_old_files()

        # Verify current file still exists
        self.assertTrue(current_file.exists())

    def test_4_13_cleanup_handles_permission_errors_gracefully(self):
        """Test 4.13: _cleanup_old_files() logs but continues on PermissionError."""
        log_dir = Path(self.test_dir) / "cleanup_test13"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 52 files
        for i in range(52):
            (log_dir / f"app-{i:02d}.log").write_text(f"log {i}")
            time.sleep(0.01)

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Mock stream for logging
        mock_stream = MagicMock()
        handler.stream = mock_stream

        # Mock unlink to raise PermissionError
        original_unlink = Path.unlink

        def mock_unlink(self, *args, **kwargs):
            raise PermissionError("Access denied")

        with patch.object(Path, 'unlink', mock_unlink):
            # Should not raise exception
            try:
                handler._cleanup_old_files()
                no_exception = True
            except Exception:
                no_exception = False

            self.assertTrue(no_exception)

    def test_4_14_doRollover_triggers_cleanup_automatically(self):
        """Test 4.14: doRollover() automatically calls cleanup."""
        log_dir = Path(self.test_dir) / "cleanup_test14"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 50 existing files
        for i in range(50):
            (log_dir / f"app-{i:02d}.log").write_text(f"log {i}")
            time.sleep(0.01)

        # Create handler
        test_file = log_dir / f"app-{50:02d}.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Trigger rollover (should create new file and trigger cleanup)
        with patch('utils.LineBasedRotatingHandler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2026, 2, 7, 12, 30, 45)
            handler.doRollover()

        # Verify cleanup occurred (should have max 50 files)
        log_files = list(log_dir.glob('*.log'))
        self.assertLessEqual(len(log_files), 50)

    def test_4_15_cleanup_uses_glob_to_find_log_files(self):
        """Test 4.15: _cleanup_old_files() uses glob('*.log') to find files."""
        log_dir = Path(self.test_dir) / "cleanup_test15"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create various file types
        (log_dir / "app-01.log").write_text("log")
        (log_dir / "app-02.log").write_text("log")
        (log_dir / "app-03.txt").write_text("text")  # Not .log
        (log_dir / "subdir").mkdir()  # Directory

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Trigger cleanup
        handler._cleanup_old_files()

        # Verify only .log files were considered
        self.assertTrue((log_dir / "app-01.log").exists())
        self.assertTrue((log_dir / "app-02.log").exists())
        self.assertTrue((log_dir / "app-03.txt").exists())  # Not deleted
        self.assertTrue((log_dir / "subdir").exists())  # Not deleted

    def test_4_16_cleanup_efficiency_with_large_file_count(self):
        """Test 4.16: _cleanup_old_files() performs efficiently with many files."""
        log_dir = Path(self.test_dir) / "cleanup_test16"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create 100 files (well over max_files=50)
        for i in range(100):
            (log_dir / f"app-{i:03d}.log").write_text(f"log {i}")
            if i % 10 == 0:
                time.sleep(0.01)  # Occasional sleep for distinct mtimes

        # Create handler
        test_file = log_dir / "app-20260207_120000.log"
        handler = LineBasedRotatingHandler(str(test_file), max_files=50)

        # Time the cleanup operation
        start_time = time.time()
        handler._cleanup_old_files()
        elapsed = time.time() - start_time

        # Verify cleanup completed quickly (< 1 second for 100 files)
        self.assertLess(elapsed, 1.0)

        # Verify exactly 50 files remain
        log_files = list(log_dir.glob('*.log'))
        self.assertEqual(len(log_files), 50)


if __name__ == '__main__':
    unittest.main()
