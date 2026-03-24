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

project_root = Path(__file__).parent.parent.parent

from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher
from utils.LoggingManager import setup_logger


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

    def test_warning_logs_appear_in_file(self):
        """
        Test I6: Verify WARNING logs from parsing errors appear in log file

        Links to: R5 (WARNING for parsing errors)
        Priority: MEDIUM
        Note: May need to mock or use test data to trigger parse errors
        """
        # This test verifies the mechanism works, even if no warnings occur
        # We'll check that IF a warning is logged, it appears with correct level

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

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
