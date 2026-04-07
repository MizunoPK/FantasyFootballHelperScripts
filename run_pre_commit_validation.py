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
    script_dir = Path(__file__).parent

    test_runner = script_dir / "tests" / "run_all_tests.py"

    if not test_runner.exists():
        print(f"Error: Test runner not found: {test_runner}")
        return 1

    print("=" * 80)
    print("PRE-COMMIT VALIDATION - RUNNING FULL TEST SUITE")
    print("=" * 80)
    print()

    try:
        result = subprocess.run([
            sys.executable,
            str(test_runner)
        ], check=False)

        print()
        if result.returncode == 0:
            print("=" * 80)
            print(" PRE-COMMIT VALIDATION PASSED")
            print("=" * 80)
            print("All tests passed. Safe to commit.")
            return 0
        else:
            print("=" * 80)
            print(" PRE-COMMIT VALIDATION FAILED")
            print("=" * 80)
            print("DO NOT COMMIT - Fix failing tests first.")
            return 1

    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


if __name__ == "__main__":
    exit_code = run_validation()
    sys.exit(exit_code)


