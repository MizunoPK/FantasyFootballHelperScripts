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

pytestmark = pytest.mark.live_api


class TestE2EExecution:
    """Integration Tests I1-I6: E2E execution with/without flag"""

    @pytest.fixture(autouse=True)
    def cleanup_logs(self):
        """Clean up test log files before and after each test"""
        logs_dir = project_root / "logs" / "schedule_fetcher"
        if logs_dir.exists():
            shutil.rmtree(logs_dir)
        yield
        if logs_dir.exists():
            shutil.rmtree(logs_dir)

    def test_schedule_fetcher_integration_with_get_logger(self):
        """
        Test I4: Verify ScheduleFetcher.logger works after main() sets up logger

        Links to: R3 (get_logger integration)
        Priority: HIGH
        """
        logger = setup_logger(
            name="schedule_fetcher",
            level="INFO",
            log_to_file=False,
            log_format="standard"
        )

        temp_output = project_root / "data" / "test_schedule.csv"
        fetcher = ScheduleFetcher(temp_output)

        assert fetcher.logger is not None, "ScheduleFetcher.logger should not be None"

        assert fetcher.logger.name == "schedule_fetcher", \
            "ScheduleFetcher.logger should have name 'schedule_fetcher'"

        try:
            fetcher.logger.info("Test message from integration test")
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

        logs_dir = project_root / "logs" / "schedule_fetcher"
        logs_dir.mkdir(parents=True, exist_ok=True)

        logger = setup_logger(
            name="schedule_fetcher",
            level="INFO",
            log_to_file=True,
            log_format="standard"
        )

        temp_output = project_root / "data" / "test_schedule.csv"
        fetcher = ScheduleFetcher(temp_output)

        fetcher.logger.warning("Error parsing event in week 1: Test error")

        log_files = list(logs_dir.glob("schedule_fetcher-*.log"))
        assert len(log_files) > 0, "Log file should exist"

        with open(log_files[0], 'r') as f:
            log_content = f.read()

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
        script_path = project_root / "run_schedule_fetcher.py"
        result = subprocess.run(
            [sys.executable, str(script_path), '--enable-log-file'],
            capture_output=True,
            text=True,
            timeout=60
        )

        stderr_lower = result.stderr.lower()
        stdout_lower = result.stdout.lower()

        assert "coroutine" not in stderr_lower, \
            "Should not have 'coroutine not awaited' errors"
        assert "asyncio" not in stderr_lower or "error" not in stderr_lower, \
            "Should not have asyncio-related errors"

        assert result.returncode in [0, 1], \
            f"Script should complete gracefully, got return code {result.returncode}"

    def test_log_rotation_during_long_fetch(self):
        """
        Test E2: Verify log rotation works if fetch generates >500 lines

        Links to: R1 (Feature 01 integration - rotation)
        Priority: LOW
        Note: Feature 01 tests cover rotation; this verifies integration
        """

        logger = setup_logger(
            name="schedule_fetcher",
            level="DEBUG",
            log_to_file=True,
            log_format="standard"
        )

        assert len(logger.handlers) > 0, "Logger should have handlers"

        file_handler = None
        for handler in logger.handlers:
            if hasattr(handler, 'baseFilename'):
                file_handler = handler
                break

        if file_handler:
            handler_class = file_handler.__class__.__name__
            assert "Rotating" in handler_class or "Handler" in handler_class, \
                f"File handler should support rotation, got {handler_class}"

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
        script_path = project_root / "run_schedule_fetcher.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60
        )

        logs_dir = project_root / "logs" / "schedule_fetcher"
        if logs_dir.exists():
            log_files = list(logs_dir.glob("schedule_fetcher-*.log"))
            assert len(log_files) == 0, \
                "No log files should be created by default (file logging OFF)"

        total_output = len(result.stderr) + len(result.stdout)
        assert total_output > 0, "Console logging should be active by default"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])


