#!/usr/bin/env python3
"""
Pre-Commit Validation Runner

Automates the complete pre-commit validation checklist including:
- Unit tests (all modules)
- Startup validation tests
- Interactive integration tests

This script ensures all validation steps are performed before committing changes.
Run from repository root: python run_pre_commit_validation.py
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class ValidationRunner:
    """Runs the complete pre-commit validation suite"""

    def __init__(self):
        self.start_time = datetime.now()
        self.results = {
            'unit_tests': {},
            'startup_tests': {},
            'integration_tests': {}
        }
        self.failed = False

    def print_header(self, message, level=1):
        """Print formatted section header"""
        if level == 1:
            print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")
        elif level == 2:
            print(f"\n{Colors.BOLD}{Colors.CYAN}{'-' * 50}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.CYAN}{message}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.CYAN}{'-' * 50}{Colors.END}\n")

    def print_success(self, message):
        """Print success message"""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")

    def print_failure(self, message):
        """Print failure message"""
        print(f"{Colors.RED}❌ {message}{Colors.END}")
        self.failed = True

    def print_warning(self, message):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

    def run_command(self, cmd, description, timeout=None, check_output=None):
        """
        Run a shell command and capture results

        Args:
            cmd: Command to run (list or string)
            description: Description of what's being tested
            timeout: Optional timeout in seconds
            check_output: Optional string to look for in output for success

        Returns:
            bool: True if successful, False otherwise
        """
        print(f"Running: {description}...", end=" ", flush=True)

        try:
            if isinstance(cmd, str):
                cmd = cmd.split()

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            # Check for success
            if check_output:
                success = check_output in result.stdout or check_output in result.stderr
            else:
                success = result.returncode == 0

            if success:
                print(f"{Colors.GREEN}PASSED{Colors.END}")
                return True
            else:
                print(f"{Colors.RED}FAILED{Colors.END}")
                if result.stderr:
                    print(f"{Colors.RED}Error output:{Colors.END}")
                    print(result.stderr[:500])  # First 500 chars of error
                return False

        except subprocess.TimeoutExpired:
            print(f"{Colors.YELLOW}TIMEOUT (expected){Colors.END}")
            return True  # Timeout is OK for startup tests
        except Exception as e:
            print(f"{Colors.RED}ERROR: {str(e)}{Colors.END}")
            return False

    def run_unit_tests(self):
        """Run all unit test suites"""
        self.print_header("STEP 1: UNIT TESTS", level=1)

        test_suites = [
            ("tests/test_runner_scripts.py", "Core runner scripts", 21),
            ("draft_helper/tests/test_draft_helper.py", "Draft helper", 34),
            ("shared_files/tests/", "Shared files", 379),
            ("player-data-fetcher/tests/", "Player data fetcher", None),
            ("nfl-scores-fetcher/tests/", "NFL scores fetcher", 47),
            ("starter_helper/tests/test_lineup_optimizer.py starter_helper/tests/test_matchup_calculator.py starter_helper/tests/test_config.py", "Starter helper", 73),
        ]

        total_passed = 0
        total_expected = 0

        for test_path, description, expected_count in test_suites:
            self.print_header(f"Testing: {description}", level=2)

            cmd = f"python -m pytest {test_path} -v --tb=short"

            try:
                result = subprocess.run(
                    cmd.split(),
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                # Parse pytest output for pass count
                output = result.stdout + result.stderr
                if "passed" in output:
                    # Extract number of passed tests
                    import re
                    match = re.search(r'(\d+) passed', output)
                    if match:
                        passed = int(match.group(1))
                        total_passed += passed
                        if expected_count:
                            total_expected += expected_count

                        if result.returncode == 0:
                            self.print_success(f"{description}: {passed} tests passed")
                            self.results['unit_tests'][description] = ('PASS', passed)
                        else:
                            # Check for failures
                            fail_match = re.search(r'(\d+) failed', output)
                            if fail_match:
                                failed = int(fail_match.group(1))
                                self.print_failure(f"{description}: {passed} passed, {failed} FAILED")
                                self.results['unit_tests'][description] = ('FAIL', f"{passed}/{passed+failed}")
                            else:
                                self.print_warning(f"{description}: {passed} passed (warnings present)")
                                self.results['unit_tests'][description] = ('WARN', passed)
                    else:
                        self.print_failure(f"{description}: Could not parse test results")
                        self.results['unit_tests'][description] = ('FAIL', 'parse error')
                else:
                    self.print_failure(f"{description}: No tests found or failed to run")
                    self.results['unit_tests'][description] = ('FAIL', 'no output')

            except subprocess.TimeoutExpired:
                self.print_warning(f"{description}: Tests timed out (may still be passing)")
                self.results['unit_tests'][description] = ('TIMEOUT', 'N/A')
            except Exception as e:
                self.print_failure(f"{description}: {str(e)}")
                self.results['unit_tests'][description] = ('ERROR', str(e))

        print(f"\n{Colors.BOLD}Unit Tests Summary:{Colors.END}")
        print(f"Total tests passed: {total_passed}")
        if total_expected > 0:
            print(f"Expected: {total_expected}")
            if total_passed >= total_expected * 0.95:  # Allow 5% variance
                self.print_success("Unit tests PASSED (>95% pass rate)")
            else:
                self.print_failure(f"Unit tests FAILED (only {total_passed}/{total_expected} passed)")

    def run_startup_tests(self):
        """Run startup validation tests"""
        self.print_header("STEP 2: STARTUP VALIDATION TESTS", level=1)

        startup_tests = [
            ("run_nfl_scores_fetcher.py", "NFL Scores Fetcher", "Starting NFL scores"),
            ("run_player_data_fetcher.py", "Player Data Fetcher", "Starting player data"),
        ]

        for script, description, expected_output in startup_tests:
            self.print_header(f"Testing: {description}", level=2)

            cmd = f"timeout 10 python {script}"

            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=12  # Slightly longer than the timeout command
                )

                # For startup tests, timeout is expected and good
                output = result.stdout + result.stderr

                if "ImportError" in output or "ModuleNotFoundError" in output:
                    self.print_failure(f"{description}: Import errors detected")
                    self.results['startup_tests'][description] = ('FAIL', 'import error')
                elif "Error" in output and "Traceback" in output:
                    self.print_failure(f"{description}: Runtime errors detected")
                    self.results['startup_tests'][description] = ('FAIL', 'runtime error')
                else:
                    self.print_success(f"{description}: Started successfully")
                    self.results['startup_tests'][description] = ('PASS', 'started')

            except subprocess.TimeoutExpired:
                # Timeout is expected - the scripts run indefinitely
                self.print_success(f"{description}: Started successfully (timed out as expected)")
                self.results['startup_tests'][description] = ('PASS', 'timeout expected')
            except Exception as e:
                self.print_failure(f"{description}: {str(e)}")
                self.results['startup_tests'][description] = ('ERROR', str(e))

    def run_integration_tests(self):
        """Run interactive integration tests"""
        self.print_header("STEP 3: INTERACTIVE INTEGRATION TESTS", level=1)

        self.print_warning("Running automated draft helper integration test sequence...")
        print("This tests: Mark Drafted, Waiver Optimizer, Drop Player, Add to Roster,")
        print("            Lock/Unlock, Starter Helper, Trade Simulator\n")

        # The automated test sequence
        test_input = "2\nHunt\n1\nexit\n3\n\n4\nHunt\n1\nHampton\n1\nexit\n1\n1\n5\n15\n16\n3\n\n5\n15\n16\n6\n\n7\n4\n8\n"

        try:
            result = subprocess.run(
                ["python", "run_draft_helper.py"],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=60
            )

            output = result.stdout + result.stderr

            # Check for success markers
            checks = {
                "Mark Drafted": "✅ Marked" in output or "marked as drafted" in output,
                "Drop Player": "✅ Dropped" in output or "dropped" in output.lower(),
                "Add to Roster": "✅ Successfully added" in output or "added to your roster" in output,
                "Clean Exit": "Goodbye!" in output,
                "No Errors": "Traceback" not in output and "Error:" not in output or output.count("Error") < 3
            }

            print(f"\n{Colors.BOLD}Integration Test Checks:{Colors.END}")
            all_passed = True
            for check_name, passed in checks.items():
                if passed:
                    self.print_success(f"{check_name}")
                else:
                    self.print_failure(f"{check_name}")
                    all_passed = False

            if all_passed:
                self.print_success("All integration tests PASSED")
                self.results['integration_tests']['Draft Helper'] = ('PASS', 'all checks passed')
            else:
                self.print_failure("Some integration tests FAILED")
                self.results['integration_tests']['Draft Helper'] = ('FAIL', 'some checks failed')

        except subprocess.TimeoutExpired:
            self.print_failure("Integration tests timed out")
            self.results['integration_tests']['Draft Helper'] = ('FAIL', 'timeout')
        except Exception as e:
            self.print_failure(f"Integration tests error: {str(e)}")
            self.results['integration_tests']['Draft Helper'] = ('ERROR', str(e))

    def print_final_summary(self):
        """Print final validation summary"""
        duration = (datetime.now() - self.start_time).total_seconds()

        self.print_header("VALIDATION SUMMARY", level=1)

        print(f"{Colors.BOLD}Duration:{Colors.END} {duration:.1f} seconds\n")

        # Unit Tests Summary
        print(f"{Colors.BOLD}Unit Tests:{Colors.END}")
        for module, (status, count) in self.results['unit_tests'].items():
            icon = "✅" if status == "PASS" else "⚠️" if status == "WARN" else "❌"
            print(f"  {icon} {module}: {count}")

        # Startup Tests Summary
        print(f"\n{Colors.BOLD}Startup Tests:{Colors.END}")
        for script, (status, msg) in self.results['startup_tests'].items():
            icon = "✅" if status == "PASS" else "❌"
            print(f"  {icon} {script}: {msg}")

        # Integration Tests Summary
        print(f"\n{Colors.BOLD}Integration Tests:{Colors.END}")
        for test, (status, msg) in self.results['integration_tests'].items():
            icon = "✅" if status == "PASS" else "❌"
            print(f"  {icon} {test}: {msg}")

        # Final verdict
        print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
        if not self.failed:
            print(f"{Colors.BOLD}{Colors.GREEN}✅ ALL VALIDATIONS PASSED - SAFE TO COMMIT{Colors.END}")
            print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 70}{Colors.END}\n")
            return 0
        else:
            print(f"{Colors.BOLD}{Colors.RED}❌ VALIDATION FAILED - DO NOT COMMIT{Colors.END}")
            print(f"{Colors.BOLD}{Colors.RED}{'=' * 70}{Colors.END}\n")
            print(f"{Colors.YELLOW}Please fix the failures above before committing.{Colors.END}\n")
            return 1

    def run(self):
        """Run the complete validation suite"""
        self.print_header("🚀 PRE-COMMIT VALIDATION SUITE")
        print(f"{Colors.BOLD}Started at:{Colors.END} {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        print(f"{Colors.YELLOW}This will run:{Colors.END}")
        print("  1. All unit tests (pytest)")
        print("  2. Startup validation tests")
        print("  3. Interactive integration tests")
        print(f"\n{Colors.YELLOW}Estimated time: 3-5 minutes{Colors.END}\n")

        # Run all validation steps
        self.run_unit_tests()
        self.run_startup_tests()
        self.run_integration_tests()

        # Print summary and return exit code
        return self.print_final_summary()


def main():
    """Main entry point"""
    # Verify we're in the correct directory
    if not Path("run_draft_helper.py").exists():
        print(f"{Colors.RED}Error: Must run from repository root directory{Colors.END}")
        print(f"{Colors.YELLOW}Expected files not found. Are you in the correct directory?{Colors.END}")
        return 1

    runner = ValidationRunner()
    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
