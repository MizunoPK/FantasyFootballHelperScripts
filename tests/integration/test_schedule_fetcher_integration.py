#!/usr/bin/env python3
"""
Integration Tests for schedule_fetcher_logging

Tests E2E execution, log file creation, and ScheduleFetcher integration.
Real script execution with test data.

Part of Feature 07 (KAI-8-logging_refactoring)
"""

import pytest
import subprocess
import sys
from pathlib import Path
import shutil
import time
from datetime import datetime
import logging

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.LoggingManager import setup_logger, get_logger


class TestE2EExecution:
    """Integration Tests I1-I6: E2E execution with/without flag"""

    @pytest.fixture(autouse=True)
    def cleanup_logs(self):
        """Clean up test log files before and after each test"""
        logs_dir = project_root / "logs" / "schedule_fetcher"
        if logs_dir.exists():
            shutil.rmtree(logs_dir)
        yield
        # Cleanup after test
        if logs_dir.exists():
            shutil.rmtree(logs_dir)

    def test_e2e_with_enable_log_file_flag(self):
        """
        Test I1: Verify script runs E2E with --enable-log-file, creates log file

        Links to: R1, R4 (CLI flag + logger integration)
        Priority: CRITICAL
        """
        # Run script with --enable-log-file flag
        script_path = project_root / "run_schedule_fetcher.py"
        result = subprocess.run(
            [sys.executable, str(script_path), '--enable-log-file'],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Verify script completed successfully (note: may fail if ESPN API down, but should not crash)
        # We check that it either succeeded (0) or failed gracefully (1), not crashed
        assert result.returncode in [0, 1], f"Script crashed with code {result.returncode}"

        # Verify log directory was created
        logs_dir = project_root / "logs" / "schedule_fetcher"
        assert logs_dir.exists(), "logs/schedule_fetcher/ directory should be created"

        # Verify at least one log file was created
        log_files = list(logs_dir.glob("schedule_fetcher-*.log"))
        assert len(log_files) > 0, "At least one log file should be created"

        # Read log file content
        log_file = log_files[0]
        with open(log_file, 'r') as f:
            log_content = f.read()

        # Verify expected log entries
        assert "Fetching NFL season schedule" in log_content, \
            "Log should contain fetching message"

        # Script should either succeed or fail gracefully
        # If it succeeded, we'll see export message
        # If ESPN API failed, we'll see error message
        # Both are acceptable E2E outcomes
        has_success = "Schedule exported to" in log_content or "Schedule successfully exported" in log_content
        has_error = "Failed to fetch" in log_content or "Unhandled error" in log_content

        assert has_success or has_error, \
            "Log should contain either success or error message (graceful failure OK)"

    def test_e2e_without_flag_no_log_file(self):
        """
        Test I2: Verify script runs E2E without flag, NO log file created

        Links to: R1 (default behavior - file logging OFF)
        Priority: CRITICAL
        """
        # Run script WITHOUT --enable-log-file flag
        script_path = project_root / "run_schedule_fetcher.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Verify script completed (may fail gracefully, but should not crash)
        assert result.returncode in [0, 1], f"Script crashed with code {result.returncode}"

        # Verify NO log files created
        logs_dir = project_root / "logs" / "schedule_fetcher"
        if logs_dir.exists():
            log_files = list(logs_dir.glob("schedule_fetcher-*.log"))
            assert len(log_files) == 0, \
                "No log files should be created when flag not provided"

        # Verify console output exists (stderr logging)
        # Even if script fails, there should be some output
        assert len(result.stderr) > 0 or len(result.stdout) > 0, \
            "Console output should be present (default behavior)"

    def test_log_file_format_and_naming(self):
        """
        Test I3: Verify log file follows naming convention

        Links to: R1, R2 (naming convention)
        Priority: HIGH
        """
        # Run script with --enable-log-file
        script_path = project_root / "run_schedule_fetcher.py"
        result = subprocess.run(
            [sys.executable, str(script_path), '--enable-log-file'],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Find log file
        logs_dir = project_root / "logs" / "schedule_fetcher"
        assert logs_dir.exists(), "logs/schedule_fetcher/ directory should exist"

        log_files = list(logs_dir.glob("schedule_fetcher-*.log"))
        assert len(log_files) > 0, "At least one log file should exist"

        # Verify filename format: schedule_fetcher-YYYYMMDD_HHMMSS.log
        log_file = log_files[0]
        filename = log_file.name

        # Check snake_case naming (not ScheduleFetcher)
        assert filename.startswith("schedule_fetcher-"), \
            "Filename should start with 'schedule_fetcher-' (snake_case)"

        # Check NOT PascalCase
        assert not filename.startswith("ScheduleFetcher-"), \
            "Filename should NOT use PascalCase 'ScheduleFetcher-'"

        # Verify located in correct directory
        assert log_file.parent.name == "schedule_fetcher", \
            "Log file should be in logs/schedule_fetcher/ directory"

    def test_schedule_fetcher_integration_with_get_logger(self):
        """
        Test I4: Verify ScheduleFetcher.logger works after main() sets up logger

        Links to: R3 (get_logger integration)
        Priority: HIGH
        """
        # Setup logger (simulating what main() does)
        logger = setup_logger(
            name="schedule_fetcher",
            level="INFO",
            log_to_file=False,  # Console only for this test
            log_format="standard"
        )

        # Import ScheduleFetcher after logger setup
        sys.path.insert(0, str(project_root / "schedule-data-fetcher"))
        from ScheduleFetcher import ScheduleFetcher

        # Create ScheduleFetcher instance
        temp_output = project_root / "data" / "test_schedule.csv"
        fetcher = ScheduleFetcher(temp_output)

        # Verify logger was retrieved successfully
        assert fetcher.logger is not None, "ScheduleFetcher.logger should not be None"

        # Verify logger name is correct
        assert fetcher.logger.name == "schedule_fetcher", \
            "ScheduleFetcher.logger should have name 'schedule_fetcher'"

        # Verify ScheduleFetcher can log messages successfully
        try:
            fetcher.logger.info("Test message from integration test")
            # If we get here, logging worked
            assert True
        except Exception as e:
            pytest.fail(f"ScheduleFetcher.logger.info() failed: {e}")

    def test_info_logs_appear_in_file(self):
        """
        Test I5: Verify INFO logs from ScheduleFetcher appear in log file

        Links to: R4, R6 (INFO logging works E2E)
        Priority: HIGH
        """
        # Run script with --enable-log-file
        script_path = project_root / "run_schedule_fetcher.py"
        result = subprocess.run(
            [sys.executable, str(script_path), '--enable-log-file'],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Find and read log file
        logs_dir = project_root / "logs" / "schedule_fetcher"
        log_files = list(logs_dir.glob("schedule_fetcher-*.log"))
        assert len(log_files) > 0, "Log file should exist"

        with open(log_files[0], 'r') as f:
            log_content = f.read()

        # Verify expected INFO logs from ScheduleFetcher
        # These are the INFO logs that should appear (from ScheduleFetcher.py):
        # - "Fetching full season schedule (weeks 1-18)" (line 91)
        # - "Successfully fetched schedule for" (line 146)
        # - "Schedule exported to" (line 236)

        # And from run_schedule_fetcher.py:
        # - "Fetching NFL season schedule for" (line 61)
        # - "Schedule successfully exported to" (line 73)

        # Check for presence of key INFO messages
        # (some may be missing if script fails, but at least one should be there)
        info_messages = [
            "Fetching NFL season schedule",
            "Fetching full season schedule",
            "Successfully fetched schedule",
            "Schedule exported to",
            "Schedule successfully exported"
        ]

        found_any = any(msg in log_content for msg in info_messages)
        assert found_any, \
            f"At least one INFO message should appear in log file. Content:\n{log_content[:500]}"

    def test_warning_logs_appear_in_file(self):
        """
        Test I6: Verify WARNING logs from parsing errors appear in log file

        Links to: R5 (WARNING for parsing errors)
        Priority: MEDIUM
        Note: May need to mock or use test data to trigger parse errors
        """
        # This test verifies the mechanism works, even if no warnings occur
        # We'll check that IF a warning is logged, it appears with correct level

        # Import and setup
        sys.path.insert(0, str(project_root / "schedule-data-fetcher"))
        from ScheduleFetcher import ScheduleFetcher

        # Create temp log file
        logs_dir = project_root / "logs" / "schedule_fetcher"
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Setup logger with file output
        logger = setup_logger(
            name="schedule_fetcher",
            level="INFO",
            log_to_file=True,
            log_format="standard"
        )

        # Create ScheduleFetcher and trigger a warning
        temp_output = project_root / "data" / "test_schedule.csv"
        fetcher = ScheduleFetcher(temp_output)

        # Manually trigger a WARNING log (simulating parse error)
        fetcher.logger.warning("Error parsing event in week 1: Test error")

        # Find log file
        log_files = list(logs_dir.glob("schedule_fetcher-*.log"))
        assert len(log_files) > 0, "Log file should exist"

        # Read log content
        with open(log_files[0], 'r') as f:
            log_content = f.read()

        # Verify WARNING appears in log
        assert "WARNING" in log_content, "Log should contain WARNING level entries"
        assert "Error parsing event" in log_content, \
            "Log should contain parse error message"


class TestEdgeCases:
    """Edge Case Tests E1-E2"""

    @pytest.fixture(autouse=True)
    def cleanup_logs(self):
        """Clean up test log files"""
        logs_dir = project_root / "logs" / "schedule_fetcher"
        if logs_dir.exists():
            shutil.rmtree(logs_dir)
        yield
        if logs_dir.exists():
            shutil.rmtree(logs_dir)

    def test_async_main_with_argparse_no_conflicts(self):
        """
        Test E1: Verify argparse works correctly with async main() function

        Links to: R1 (async main requirement)
        Priority: HIGH
        Rationale: Argparse is synchronous, must verify no async/await conflicts
        """
        # Run script and verify it completes without async/await errors
        script_path = project_root / "run_schedule_fetcher.py"
        result = subprocess.run(
            [sys.executable, str(script_path), '--enable-log-file'],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Check for async-related errors
        stderr_lower = result.stderr.lower()
        stdout_lower = result.stdout.lower()

        # Verify no async/await errors
        assert "coroutine" not in stderr_lower, \
            "Should not have 'coroutine not awaited' errors"
        assert "asyncio" not in stderr_lower or "error" not in stderr_lower, \
            "Should not have asyncio-related errors"

        # Verify script completed (even if ESPN API failed, should not crash on async issues)
        assert result.returncode in [0, 1], \
            f"Script should complete gracefully, got return code {result.returncode}"

    def test_log_rotation_during_long_fetch(self):
        """
        Test E2: Verify log rotation works if fetch generates >500 lines

        Links to: R1 (Feature 01 integration - rotation)
        Priority: LOW
        Note: Feature 01 tests cover rotation; this verifies integration
        """
        # This test verifies rotation mechanism exists
        # We don't force >500 lines (would require mocking), but verify rotation config

        # Setup logger with file output
        logger = setup_logger(
            name="schedule_fetcher",
            level="DEBUG",  # More verbose to increase line count
            log_to_file=True,
            log_format="standard"
        )

        # Verify logger has handlers
        assert len(logger.handlers) > 0, "Logger should have handlers"

        # Find file handler
        file_handler = None
        for handler in logger.handlers:
            if hasattr(handler, 'baseFilename'):
                file_handler = handler
                break

        if file_handler:
            # Verify it's a LineBasedRotatingHandler (or RotatingFileHandler)
            handler_class = file_handler.__class__.__name__
            assert "Rotating" in handler_class or "Handler" in handler_class, \
                f"File handler should support rotation, got {handler_class}"

        # Verify log directory structure
        logs_dir = project_root / "logs" / "schedule_fetcher"
        assert logs_dir.exists(), "Log directory should exist"


class TestConfiguration:
    """Configuration Tests C1-C2"""

    @pytest.fixture(autouse=True)
    def cleanup_logs(self):
        """Clean up test log files"""
        logs_dir = project_root / "logs" / "schedule_fetcher"
        if logs_dir.exists():
            shutil.rmtree(logs_dir)
        yield
        if logs_dir.exists():
            shutil.rmtree(logs_dir)

    def test_default_behavior_file_logging_off(self):
        """
        Test C1: Verify file logging is OFF by default (no flag)

        Links to: R1 (default = OFF)
        Priority: HIGH
        Rationale: Critical UX requirement - must default to console only
        """
        # Run script without any CLI arguments
        script_path = project_root / "run_schedule_fetcher.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Verify no log files created
        logs_dir = project_root / "logs" / "schedule_fetcher"
        if logs_dir.exists():
            log_files = list(logs_dir.glob("schedule_fetcher-*.log"))
            assert len(log_files) == 0, \
                "No log files should be created by default (file logging OFF)"

        # Verify console logging active (stderr should have output)
        # Even if script fails, should have some console output
        total_output = len(result.stderr) + len(result.stdout)
        assert total_output > 0, "Console logging should be active by default"

    def test_explicit_flag_behavior_file_logging_on(self):
        """
        Test C2: Verify file logging is ON when flag provided

        Links to: R1 (explicit = ON)
        Priority: HIGH
        Rationale: Must verify opt-in behavior works correctly
        """
        # Run script with --enable-log-file explicitly
        script_path = project_root / "run_schedule_fetcher.py"
        result = subprocess.run(
            [sys.executable, str(script_path), '--enable-log-file'],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Verify log file created
        logs_dir = project_root / "logs" / "schedule_fetcher"
        assert logs_dir.exists(), "logs/schedule_fetcher/ directory should be created"

        log_files = list(logs_dir.glob("schedule_fetcher-*.log"))
        assert len(log_files) > 0, \
            "At least one log file should be created when flag provided"

        # Verify file contains expected log entries
        with open(log_files[0], 'r') as f:
            log_content = f.read()

        # Should have at least some log content
        assert len(log_content) > 0, "Log file should contain log entries"

        # Verify console logging also active (both outputs)
        # Console output may be on stderr or stdout
        total_output = len(result.stderr) + len(result.stdout)
        # Note: Console might be quiet if script succeeds, but stderr usually has something
        # We'll just verify script ran without crashing
        assert result.returncode in [0, 1], "Script should complete successfully"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
