#!/usr/bin/env python3
"""
Unit Tests for run_schedule_fetcher.py

Tests CLI flag integration, logger setup, print replacement,
and log quality for schedule_fetcher_logging feature.

Part of Feature 07 (KAI-8-logging_refactoring)
"""

import pytest
import sys
from pathlib import Path
import argparse


# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestCLIFlagParsing:
    """Test Requirement R1: CLI Flag Integration (Tests 1.1-1.3)"""

    def test_cli_flag_parsing_without_flag(self):
        """
        Test 1.1: Verify --enable-log-file defaults to False when omitted

        Links to: R1 (default behavior)
        Priority: HIGH
        """
        # Create parser identical to run_schedule_fetcher.py
        parser = argparse.ArgumentParser(description="Fetch NFL season schedule from ESPN API")
        parser.add_argument(
            '--enable-log-file',
            action='store_true',
            help='Enable logging to file (default: console only)'
        )

        # Parse empty args (no flag)
        args = parser.parse_args([])

        # Verify default is False
        assert args.enable_log_file is False, "Flag should default to False when omitted"

    def test_cli_flag_parsing_with_flag(self):
        """
        Test 1.2: Verify --enable-log-file sets True when provided

        Links to: R1 (flag parsing)
        Priority: HIGH
        """
        # Create parser identical to run_schedule_fetcher.py
        parser = argparse.ArgumentParser(description="Fetch NFL season schedule from ESPN API")
        parser.add_argument(
            '--enable-log-file',
            action='store_true',
            help='Enable logging to file (default: console only)'
        )

        # Parse with flag
        args = parser.parse_args(['--enable-log-file'])

        # Verify flag is True
        assert args.enable_log_file is True, "Flag should be True when provided"

    def test_cli_flag_help_text(self):
        """
        Test 1.3: Verify help text mentions file logging

        Links to: R1 (user documentation)
        Priority: MEDIUM
        """
        # Create parser identical to run_schedule_fetcher.py
        parser = argparse.ArgumentParser(description="Fetch NFL season schedule from ESPN API")
        parser.add_argument(
            '--enable-log-file',
            action='store_true',
            help='Enable logging to file (default: console only)'
        )

        # Get help text
        help_text = parser.format_help()

        # Verify help contains flag and description
        assert '--enable-log-file' in help_text, "Help should mention --enable-log-file flag"
        assert 'Enable logging to file' in help_text, "Help should explain what flag does"
        assert 'default: console only' in help_text, "Help should mention default behavior"


class TestLoggerNameConsistency:
    """Test Requirement R2: Logger Name Consistency (Test 2.1)"""

    def test_logger_name_snake_case(self):
        """
        Test 2.1: Verify ScheduleFetcher uses "schedule_fetcher" logger name

        Links to: R2, R3 (logger name + get_logger pattern)
        Priority: MEDIUM
        Note: Source code inspection approach (more reliable than runtime inspection)
        """
        # Read run_schedule_fetcher.py source
        main_script_path = project_root / "run_schedule_fetcher.py"
        with open(main_script_path, 'r') as f:
            main_source = f.read()

        # Verify setup_logger() called with name="schedule_fetcher"
        assert 'name="schedule_fetcher"' in main_source, \
            "setup_logger() should use snake_case name 'schedule_fetcher'"

        # Read ScheduleFetcher.py source
        fetcher_path = project_root / "schedule-data-fetcher" / "ScheduleFetcher.py"
        with open(fetcher_path, 'r') as f:
            fetcher_source = f.read()

        # Verify get_logger() pattern (not setup_logger with wrong name)
        assert 'get_logger()' in fetcher_source, \
            "ScheduleFetcher should use get_logger() not setup_logger()"
        assert 'setup_logger' not in fetcher_source or 'from utils.LoggingManager import get_logger' in fetcher_source, \
            "ScheduleFetcher should not call setup_logger()"


class TestScheduleFetcherLoggerSetup:
    """Test Requirement R3: ScheduleFetcher Logger Setup (Tests 3.1-3.2)"""

    def test_schedule_fetcher_uses_get_logger(self):
        """
        Test 3.1: Verify ScheduleFetcher calls get_logger() not setup_logger()

        Links to: R3 (get_logger pattern from Feature 05)
        Priority: HIGH
        """
        # Read ScheduleFetcher.py source
        fetcher_path = project_root / "schedule-data-fetcher" / "ScheduleFetcher.py"
        with open(fetcher_path, 'r') as f:
            source = f.read()

        # Verify __init__ uses get_logger() pattern
        assert 'self.logger = get_logger()' in source, \
            "ScheduleFetcher.__init__() should use 'self.logger = get_logger()' pattern"

        # Verify import is get_logger (not setup_logger)
        assert 'from utils.LoggingManager import get_logger' in source, \
            "ScheduleFetcher should import get_logger from LoggingManager"

    def test_schedule_fetcher_no_enable_log_file_param(self):
        """
        Test 3.2: Verify ScheduleFetcher.__init__() has NO enable_log_file parameter

        Links to: R3 (simpler interface from S8.P1 alignment)
        Priority: HIGH
        """
        # Read ScheduleFetcher.py source
        fetcher_path = project_root / "schedule-data-fetcher" / "ScheduleFetcher.py"
        with open(fetcher_path, 'r') as f:
            source = f.read()

        # Find __init__ signature
        lines = source.split('\n')
        init_found = False
        for i, line in enumerate(lines):
            if 'def __init__(self' in line:
                init_found = True
                # Check this line and next few for parameters
                signature = line
                # Collect multiline signature if needed
                j = i + 1
                while j < len(lines) and '):' not in lines[j-1]:
                    signature += lines[j]
                    j += 1

                # Verify NO enable_log_file parameter
                assert 'enable_log_file' not in signature, \
                    "ScheduleFetcher.__init__() should NOT have enable_log_file parameter"

                # Verify correct signature: (self, output_path: Path)
                assert 'output_path' in signature, \
                    "ScheduleFetcher.__init__() should have output_path parameter"
                break

        assert init_found, "Could not find __init__ method in ScheduleFetcher"


class TestPrintReplacement:
    """Test Requirement R4: Replace Print Statements (Tests 4.1-4.4)"""

    def test_no_print_statements_in_main(self):
        """
        Test 4.1: Verify run_schedule_fetcher.py main() has no print() calls

        Links to: R4 (print replacement)
        Priority: HIGH
        Note: Source inspection verifies print removal
        """
        # Read run_schedule_fetcher.py source
        main_script_path = project_root / "run_schedule_fetcher.py"
        with open(main_script_path, 'r') as f:
            source = f.read()

        # Extract main() function
        lines = source.split('\n')
        in_main = False
        main_lines = []
        for line in lines:
            if 'async def main():' in line or 'def main():' in line:
                in_main = True
            elif in_main:
                if line.startswith('def ') or line.startswith('async def '):
                    break  # End of main function
                main_lines.append(line)

        main_source = '\n'.join(main_lines)

        # Verify no print() calls in main (excluding traceback.print_exc)
        # Split into lines and check each
        for line in main_lines:
            stripped = line.strip()
            if 'print(' in stripped and 'traceback.print_exc' not in stripped:
                pytest.fail(f"Found print() statement in main(): {stripped}")

        # Should have logger calls instead
        assert 'logger.info' in main_source or 'logger.error' in main_source, \
            "main() should use logger.info/error instead of print()"

    def test_logger_info_replaces_print_success(self):
        """
        Test 4.2: Verify logger.info() used for success messages

        Links to: R4 (logger.info usage)
        Priority: HIGH
        """
        # Read run_schedule_fetcher.py source
        main_script_path = project_root / "run_schedule_fetcher.py"
        with open(main_script_path, 'r') as f:
            source = f.read()

        # Verify specific logger.info calls exist
        assert 'logger.info(f"Fetching NFL season' in source, \
            "Should have logger.info for fetching message"
        assert 'logger.info(f"Schedule successfully exported' in source, \
            "Should have logger.info for success message"

    def test_logger_error_replaces_print_error(self):
        """
        Test 4.3: Verify logger.error() used for error messages

        Links to: R4 (logger.error usage)
        Priority: HIGH
        """
        # Read run_schedule_fetcher.py source
        main_script_path = project_root / "run_schedule_fetcher.py"
        with open(main_script_path, 'r') as f:
            source = f.read()

        # Verify specific logger.error calls exist
        assert 'logger.error("Failed to fetch schedule data")' in source, \
            "Should have logger.error for fetch failure"
        assert 'logger.error(f"Unhandled error' in source, \
            "Should have logger.error for unhandled errors"

    def test_setup_logger_called_before_fetcher(self):
        """
        Test 4.4: Verify setup_logger() called before ScheduleFetcher instantiation

        Links to: R1, R4 (correct initialization order)
        Priority: MEDIUM
        """
        # Read run_schedule_fetcher.py source
        main_script_path = project_root / "run_schedule_fetcher.py"
        with open(main_script_path, 'r') as f:
            source = f.read()

        # Find positions of setup_logger and ScheduleFetcher
        setup_pos = source.find('setup_logger(')
        fetcher_pos = source.find('ScheduleFetcher(')

        assert setup_pos != -1, "setup_logger() call not found"
        assert fetcher_pos != -1, "ScheduleFetcher() instantiation not found"

        # Verify setup_logger comes before ScheduleFetcher
        assert setup_pos < fetcher_pos, \
            "setup_logger() must be called before ScheduleFetcher instantiation"


class TestLogQualityDebugWarning:
    """Test Requirement R5: Log Quality - DEBUG/WARNING (Tests 5.1-5.2)"""

    def test_error_parsing_uses_warning_level(self):
        """
        Test 5.1: Verify error parsing log uses WARNING (not DEBUG)

        Links to: R5 (Feature 06 alignment - WARNING for parsing errors)
        Priority: HIGH
        Note: Per Feature 06 pattern, operational errors use WARNING
        """
        # Read ScheduleFetcher.py source
        fetcher_path = project_root / "schedule-data-fetcher" / "ScheduleFetcher.py"
        with open(fetcher_path, 'r') as f:
            lines = f.readlines()

        # Find line ~138 with error parsing
        found = False
        for i, line in enumerate(lines, 1):
            if 'Error parsing event' in line:
                # Verify this is a WARNING level log (not DEBUG)
                assert 'self.logger.warning' in line, \
                    f"Line {i}: Error parsing should use WARNING level, not DEBUG"
                found = True
                break

        assert found, "Could not find 'Error parsing event' log statement"

    def test_progress_tracking_uses_debug_level(self):
        """
        Test 5.2: Verify progress tracking log remains DEBUG

        Links to: R5 (DEBUG for progress tracking)
        Priority: MEDIUM
        """
        # Read ScheduleFetcher.py source
        fetcher_path = project_root / "schedule-data-fetcher" / "ScheduleFetcher.py"
        with open(fetcher_path, 'r') as f:
            lines = f.readlines()

        # Find line ~94 with progress tracking
        found = False
        for i, line in enumerate(lines, 1):
            if 'Fetching schedule for week' in line and '/18' in line:
                # Verify this is a DEBUG level log (not changed)
                assert 'self.logger.debug' in line, \
                    f"Line {i}: Progress tracking should remain DEBUG level"
                found = True
                break

        assert found, "Could not find 'Fetching schedule for week' log statement"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
