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

        if platform.system() == "Windows":
            venv_candidates = [
                self.project_root / "venv" / "Scripts" / "python.exe",
                self.project_root / ".venv" / "Scripts" / "python.exe",
            ]
        else:
            venv_candidates = [
                self.project_root / "venv" / "bin" / "python",
                self.project_root / ".venv" / "bin" / "python",
            ]

        self.venv_python = None
        for candidate in venv_candidates:
            if candidate.exists():
                self.venv_python = candidate
                break

        if not self.venv_python:
            self.venv_python = sys.executable

    def discover_test_files(self) -> List[Path]:
        """Recursively find all test files in tests directory"""
        test_files = []

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
        cmd = [
            str(self.venv_python),
            "-m", "pytest",
            str(test_file),
            "-m", "not live_api",
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
                cwd=str(self.project_root),
                timeout=300
            )

            output = result.stdout + result.stderr

            passed_count, total_count = self._parse_test_results(output)

            success = (result.returncode in [0, 5] and passed_count == total_count)

            return success, passed_count, total_count, output

        except Exception as e:
            return False, 0, 0, f"Error running tests: {str(e)}"

    def _parse_test_results(self, output: str) -> Tuple[int, int]:
        """Parse pytest output to extract passed/total counts

        Counts are read from pytest's terminal summary line ONLY (the last line
        carrying an "in <duration>s" suffix, e.g. "6 failed, 34 passed in 0.40s").
        Searching the whole output is wrong: captured log records can contain
        incidental text such as "Simulation 0 failed: ...", and an unanchored
        search matched that first — reporting 0 failures for a file with 6, which
        then silently undercounted the run-wide failure headline.
        """
        import re

        summary = ""
        for line in reversed(output.splitlines()):
            candidate = line.strip().strip('=').strip()
            # The outcome vocabulary here identifies the summary LINE; only passed /
            # failed / error counts feed the totals below. It deliberately includes
            # outcomes this runner does not count (skipped, xfailed, ...) so that a
            # skipped-only or deselected-only run is recognised as a real summary
            # rather than falling through to the no-summary-at-all case.
            if re.search(r'\bin \d+(\.\d+)?s', candidate) and \
                    re.search(r'\b\d+ (passed|failed|error|errors|skipped|deselected'
                              r'|xfailed|xpassed|warning|warnings)\b', candidate):
                summary = candidate
                break

        def _count(word: str) -> int:
            match = re.search(rf'(\d+) {word}', summary)
            return int(match.group(1)) if match else 0

        passed_count = _count('passed')
        failed_count = _count('failed')
        error_count = _count('error')

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

            if success:
                print(f"[PASS] {passed}/{total} tests")
            else:
                print(f"[FAIL] {passed}/{total} tests")
                if self.verbose or self.detailed:
                    print("\nTest Output:")
                    print(output)

            print()

        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print()

        for rel_path, success, passed, total, _ in all_results:
            status = "[PASS]" if success else "[FAIL]"
            print(f"{status}: {rel_path} ({passed}/{total})")

        print()
        print("=" * 80)

        all_passed = all(success for _, success, _, _, _ in all_results)

        if all_passed and total_passed == total_tests and total_tests > 0:
            print(f"SUCCESS: ALL {total_tests} TESTS PASSED (100%)")
            print("=" * 80)
            return True
        else:
            failed_files = [(path, passed, total) for path, success, passed, total, _ in all_results if not success]

            if total_tests > 0:
                failed = total_tests - total_passed
                if failed > 0:
                    print(f"FAILURE: {failed} of {total_tests} TESTS DID NOT PASS ({total_passed} passed)")
                else:
                    print(f"FAILURE: {len(failed_files)} TEST FILE(S) FAILED TO RUN ({total_passed} tests passed)")
            else:
                print(f"FAILURE: NO TESTS DISCOVERED (0/0)")
            print()
            print("STRICT REQUIREMENT: 100% of tests must pass")
            print()

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
            "-m", "not live_api",
            "-v" if self.verbose else "",
            "--tb=short"
        ]

        cmd = [c for c in cmd if c]

        if self.detailed:
            cmd.append("-vv")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.project_root),
                timeout=900
            )

            output = result.stdout + result.stderr
            print(output)

            passed_count, total_count = self._parse_test_results(output)

            print()
            print("=" * 80)

            if result.returncode in [0, 5] and passed_count == total_count:
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


def _data_status_paths(project_root: Path):
    """Return the set of paths `git status --porcelain -- data/` reports.

    Returns None when git is unavailable, errors, or the runner is not inside a
    git work tree. The caller then prints a notice and SKIPS the check -- an
    infrastructure absence must never turn into a red suite (T91 AC10).
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--", "data/"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=60
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    return {line[3:] for line in result.stdout.splitlines() if len(line) > 3}


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

    # T91: baseline the data/ tree before the run so a test that writes into the
    # tracked data tree cannot pass silently. Baseline DIFF, not a clean-tree
    # assertion -- a developer with legitimate in-flight data/ edits must not get
    # a false red.
    before_paths = _data_status_paths(runner.project_root)
    if before_paths is None:
        print("NOTICE: git unavailable or not a git work tree "
              "- skipping the data/ cleanliness check")

    if args.single:
        success = runner.run_all_tests_single_command()
    else:
        success = runner.run_all_tests()

    if before_paths is not None:
        after_paths = _data_status_paths(runner.project_root)
        if after_paths is None:
            print("NOTICE: git status unavailable after the run "
                  "- skipping the data/ cleanliness check")
        else:
            newly_dirtied = sorted(after_paths - before_paths)
            if newly_dirtied:
                print()
                print("=" * 80)
                print("FAILURE: THIS TEST RUN DIRTIED PATHS UNDER data/")
                if success:
                    # The suite itself passed, so a green SUCCESS line was already
                    # printed above. Retract it explicitly: this run is a FAILURE,
                    # and output that still scans as green is the exact hazard the
                    # runner's reporting is meant to avoid.
                    print("*** The SUCCESS line printed above is SUPERSEDED. "
                          "This run FAILED. ***")
                for dirty_path in newly_dirtied:
                    print(f"  [NEWLY DIRTIED] {dirty_path}")
                print()
                print("Something wrote into the repository's data/ tree during "
                      "this run instead of a sandbox -- most likely a test, "
                      "though a concurrent process writing to data/ is "
                      "indistinguishable here.")
                print("Restore with:  git checkout -- data/")
                print("Then sandbox the writing test: point the fetcher's data "
                      "root at a temp dir via the PLAYER_DATA_DIR environment "
                      "variable, e.g.")
                print("    monkeypatch.setenv('PLAYER_DATA_DIR', str(tmp_path))")
                print("See tests/README.md.")
                print("=" * 80)
                success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()


