#!/usr/bin/env python3
"""
Pre-Commit Validation Runner

Runs the full test suite before allowing commits.
This script is called by the pre-commit protocol as documented in CLAUDE.md

Usage:
    python run_pre_commit_validation.py

Exit Codes:
    0: All tests passed - safe to commit
    1: Tests failed - DO NOT commit

Author: Kai Mizuno
"""

import subprocess
import sys
from pathlib import Path


def run_validation():
    """
    Run full test suite for pre-commit validation.

    Returns:
        int: Exit code (0 = success, 1 = failure)
    """
    # Get the directory where this script is located (project root)
    script_dir = Path(__file__).parent

    # Construct path to the test runner script
    test_runner = script_dir / "tests" / "run_all_tests.py"

    # Verify test runner exists before attempting to run
    if not test_runner.exists():
        print(f"Error: Test runner not found: {test_runner}")
        return 1

    # Print header for validation process
    print("=" * 80)
    print("PRE-COMMIT VALIDATION - RUNNING FULL TEST SUITE")
    print("=" * 80)
    print()

    try:
        # Run the test suite using the same Python interpreter
        # check=False means we handle the return code ourselves instead of raising exception
        result = subprocess.run([
            sys.executable,        # Current Python interpreter path
            str(test_runner)       # Path to run_all_tests.py
        ], check=False)

        print()
        # Check if all tests passed (exit code 0)
        if result.returncode == 0:
            # All tests passed - safe to commit
            print("=" * 80)
            print(" PRE-COMMIT VALIDATION PASSED")
            print("=" * 80)
            print("All tests passed. Safe to commit.")
            return 0
        else:
            # Some tests failed - DO NOT commit
            print("=" * 80)
            print(" PRE-COMMIT VALIDATION FAILED")
            print("=" * 80)
            print("DO NOT COMMIT - Fix failing tests first.")
            return 1

    except Exception as e:
        # Unexpected error running tests (e.g., permission denied, Python not found)
        print(f"Error running tests: {e}")
        return 1


if __name__ == "__main__":
    # Execute validation and exit with its return code
    # This allows the script to be used in pre-commit hooks
    exit_code = run_validation()
    sys.exit(exit_code)
