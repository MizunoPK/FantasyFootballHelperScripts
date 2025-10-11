#!/usr/bin/env python3
"""
Run All Unit Tests

This script dynamically discovers and runs all unit tests in the tests/ folder.
Requires 100% of tests to pass - no exceptions.

Usage:
    python tests/run_all_tests.py
    python tests/run_all_tests.py --verbose
    python tests/run_all_tests.py --detailed

Author: Claude Code
Date: 2025-10-09
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple
import argparse
import platform


class TestRunner:
    """Discovers and runs all unit tests with strict 100% pass requirement"""

    def __init__(self, verbose: bool = False, detailed: bool = False):
        self.verbose = verbose
        self.detailed = detailed
        self.tests_dir = Path(__file__).parent
        self.project_root = self.tests_dir.parent

        # Detect platform and use appropriate venv path
        if platform.system() == "Windows":
            self.venv_python = self.project_root / ".venv" / "Scripts" / "python.exe"
        else:
            self.venv_python = self.project_root / ".venv" / "bin" / "python"

        # Use system python if venv doesn't exist
        if not self.venv_python.exists():
            self.venv_python = sys.executable

    def discover_test_files(self) -> List[Path]:
        """Recursively find all test files in tests directory"""
        test_files = []

        # Find all test_*.py files
        for test_file in self.tests_dir.rglob("test_*.py"):
            if test_file.is_file():
                test_files.append(test_file)

        return sorted(test_files)

    def run_pytest_on_file(self, test_file: Path) -> Tuple[bool, int, int, str]:
        """
        Run pytest on a single test file

        Returns:
            (success, passed_count, total_count, output)
        """
        # Build pytest command
        cmd = [
            str(self.venv_python),
            "-m", "pytest",
            str(test_file),
            "-v" if self.verbose else "-q",
            "--tb=short"
        ]

        if self.detailed:
            cmd.append("-vv")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.project_root)
            )

            output = result.stdout + result.stderr

            # Parse test results from output
            passed_count, total_count = self._parse_test_results(output)

            # Success if all tests passed and exit code is 0
            success = (result.returncode == 0 and passed_count == total_count)

            return success, passed_count, total_count, output

        except Exception as e:
            return False, 0, 0, f"Error running tests: {str(e)}"

    def _parse_test_results(self, output: str) -> Tuple[int, int]:
        """Parse pytest output to extract passed/total counts"""
        # Look for pattern like "60 passed in 0.30s" or "47 passed, 13 failed"
        import re

        # Pattern: "X passed"
        passed_match = re.search(r'(\d+) passed', output)
        passed_count = int(passed_match.group(1)) if passed_match else 0

        # Pattern: "X failed"
        failed_match = re.search(r'(\d+) failed', output)
        failed_count = int(failed_match.group(1)) if failed_match else 0

        # Pattern: "X error"
        error_match = re.search(r'(\d+) error', output)
        error_count = int(error_match.group(1)) if error_match else 0

        total_count = passed_count + failed_count + error_count

        return passed_count, total_count

    def run_all_tests(self) -> bool:
        """
        Discover and run all tests

        Returns:
            True if 100% of tests pass, False otherwise
        """
        print("=" * 80)
        print("FANTASY FOOTBALL HELPER - UNIT TEST RUNNER")
        print("=" * 80)
        print(f"Test Directory: {self.tests_dir}")
        print(f"Python: {self.venv_python}")
        print()

        # Discover test files
        test_files = self.discover_test_files()

        if not test_files:
            print("[ERROR] No test files found!")
            print(f"   Searched in: {self.tests_dir}")
            return False

        print(f"Discovered {len(test_files)} test file(s):")
        for test_file in test_files:
            rel_path = test_file.relative_to(self.project_root)
            print(f"  • {rel_path}")
        print()

        # Run tests
        print("=" * 80)
        print("RUNNING TESTS")
        print("=" * 80)
        print()

        all_results = []
        total_passed = 0
        total_tests = 0

        for test_file in test_files:
            rel_path = test_file.relative_to(self.project_root)
            print(f"Running: {rel_path}")
            print("-" * 80)

            success, passed, total, output = self.run_pytest_on_file(test_file)

            all_results.append((rel_path, success, passed, total, output))
            total_passed += passed
            total_tests += total

            # Show results for this file
            if success:
                print(f"[PASS] {passed}/{total} tests")
            else:
                print(f"[FAIL] {passed}/{total} tests")
                if self.verbose or self.detailed:
                    print("\nTest Output:")
                    print(output)

            print()

        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print()

        for rel_path, success, passed, total, _ in all_results:
            status = "[PASS]" if success else "[FAIL]"
            print(f"{status}: {rel_path} ({passed}/{total})")

        print()
        print("=" * 80)

        # Final verdict
        all_passed = all(success for _, success, _, _, _ in all_results)

        if all_passed and total_passed == total_tests:
            print(f"SUCCESS: ALL {total_tests} TESTS PASSED (100%)")
            print("=" * 80)
            return True
        else:
            print(f"FAILURE: {total_passed}/{total_tests} TESTS PASSED ({total_passed/total_tests*100:.1f}%)")
            print()
            print("STRICT REQUIREMENT: 100% of tests must pass")
            print()

            # Show which files failed
            failed_files = [(path, passed, total) for path, success, passed, total, _ in all_results if not success]
            if failed_files:
                print("Failed test files:")
                for path, passed, total in failed_files:
                    print(f"  - {path}: {passed}/{total} passed")

            print("=" * 80)
            return False

    def run_all_tests_single_command(self) -> bool:
        """
        Alternative: Run all tests in a single pytest command
        This is faster but less granular in reporting
        """
        print("=" * 80)
        print("FANTASY FOOTBALL HELPER - UNIT TEST RUNNER")
        print("(Single Command Mode)")
        print("=" * 80)
        print(f"Test Directory: {self.tests_dir}")
        print()

        cmd = [
            str(self.venv_python),
            "-m", "pytest",
            str(self.tests_dir),
            "-v" if self.verbose else "",
            "--tb=short"
        ]

        # Remove empty strings
        cmd = [c for c in cmd if c]

        if self.detailed:
            cmd.append("-vv")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.project_root)
            )

            output = result.stdout + result.stderr
            print(output)

            # Parse results
            passed_count, total_count = self._parse_test_results(output)

            print()
            print("=" * 80)

            if result.returncode == 0 and passed_count == total_count:
                print(f"SUCCESS: ALL {total_count} TESTS PASSED (100%)")
                print("=" * 80)
                return True
            else:
                print(f"FAILURE: {passed_count}/{total_count} TESTS PASSED")
                print()
                print("STRICT REQUIREMENT: 100% of tests must pass")
                print("=" * 80)
                return False

        except Exception as e:
            print(f"ERROR: {str(e)}")
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run all unit tests with 100% pass requirement"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output (show individual test names)"
    )
    parser.add_argument(
        "-d", "--detailed",
        action="store_true",
        help="Very detailed output (includes full test output)"
    )
    parser.add_argument(
        "-s", "--single",
        action="store_true",
        help="Run all tests in single pytest command (faster)"
    )

    args = parser.parse_args()

    runner = TestRunner(verbose=args.verbose, detailed=args.detailed)

    if args.single:
        success = runner.run_all_tests_single_command()
    else:
        success = runner.run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
