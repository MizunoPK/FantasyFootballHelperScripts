#!/usr/bin/env python3
"""
Tests for tests/run_all_tests.py's pytest-summary result parsing

Regression coverage for a runner accounting defect found while building D1.1: the
parser searched the WHOLE captured output for '<n> failed', so a log record such as
"Simulation 0 failed: ..." matched before pytest's real summary line. A file with 6
failures was reported as "34/34 tests", and because the run-wide headline is derived
as (total discovered - total passed), those failures vanished from the failure count
entirely -- the suite gate read near-green while tests were failing.

The parser therefore reads counts from pytest's terminal summary line ONLY.

Author: Kai Mizuno
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root / 'tests') not in sys.path:
    sys.path.insert(0, str(project_root / 'tests'))

import run_all_tests  # noqa: E402


def _parse(output):
    """Drive the real parser without constructing a full TestRunner."""
    runner = run_all_tests.TestRunner.__new__(run_all_tests.TestRunner)
    return runner._parse_test_results(output)


class TestSummaryLineIsAuthoritative:
    """
    The parser must ignore count-shaped text anywhere except the summary line.
    """

    def test_incidental_log_text_does_not_mask_failures(self):
        """
        The exact defect: a captured ERROR record containing "Simulation 0 failed"
        precedes the summary. Parsing that instead of the summary yields (34, 34) --
        a file with 6 failures indistinguishable from a fully green one.
        """
        output = (
            "ERROR    test_runner:ParallelLeagueRunner.py:537 "
            "Simulation 0 failed: got an unexpected keyword argument\n"
            "=========================== short test summary info ===========================\n"
            "FAILED tests/simulation/test_ParallelLeagueRunner.py::TestRunSingleSimulation\n"
            "6 failed, 34 passed in 0.40s\n"
        )

        assert _parse(output) == (34, 40)

    def test_incidental_passed_text_does_not_inflate_total(self):
        """A log record mentioning a passed count must not be read as the summary."""
        output = (
            "INFO     seeding:harness.py:12 preflight: 99 passed in cache\n"
            "2 failed, 5 passed in 1.20s\n"
        )

        assert _parse(output) == (5, 7)

    def test_last_summary_wins_when_output_carries_several(self):
        """
        Nested/echoed pytest output can carry more than one summary-shaped line; the
        final one is the run being measured.
        """
        output = (
            "1 failed, 1 passed in 0.10s\n"
            "=========================== short test summary info ===========================\n"
            "3 failed, 7 passed in 2.00s\n"
        )

        assert _parse(output) == (7, 10)


class TestOrdinarySummaries:
    """The straightforward shapes must keep parsing exactly as before."""

    def test_all_passed(self):
        assert _parse("40 passed in 0.25s\n") == (40, 40)

    def test_errors_counted_in_total(self):
        assert _parse("2 errors in 0.03s\n") == (0, 2)

    def test_collection_error_with_partial_pass(self):
        assert _parse("1 failed, 2 errors, 3 passed in 0.50s\n") == (3, 6)

    def test_no_tests_ran_is_zero_zero(self):
        """
        Zero/zero is the signal run_pytest_on_file pairs with pytest's exit code 5
        to treat an empty file as a non-failure; it must not become a false green
        for a file that did run.
        """
        assert _parse("no tests ran in 0.01s\n") == (0, 0)

    def test_skipped_only_run_is_zero_zero(self):
        """
        A skipped-only summary carries no passed/failed/error token, so it reports
        (0, 0): skips are never counted as passes or failures. This assertion pins
        that reported value only -- it cannot (and does not) distinguish whether the
        line was recognised as a summary, because a recognised skipped-only line and
        an unrecognised one both yield (0, 0).
        """
        assert _parse("5 skipped in 0.05s\n") == (0, 0)

    def test_passed_alongside_skipped_and_warnings_is_counted(self):
        """The common real-world shape: counts come from the same line as the skips."""
        assert _parse("12 passed, 3 skipped, 2 warnings in 4.10s\n") == (12, 12)

    def test_failure_alongside_deselection_is_counted(self):
        assert _parse("1 failed, 9 passed, 4 deselected in 0.80s\n") == (9, 10)

    def test_trailing_warnings_line_does_not_displace_the_real_summary(self):
        """
        Regression pin for the vocabulary-width defect. The scan takes the LAST
        matching line, so if the outcome vocabulary admitted non-counted outcomes
        (warnings/skipped/deselected/...), a trailing "3 warnings in 0.50s" would be
        selected as the summary and every count would read 0 -- silently hiding 3
        failures. The narrow vocabulary skips that line and keeps the real summary.
        """
        output = (
            "3 failed, 7 passed in 2.00s\n"
            "3 warnings in 0.50s\n"
        )

        assert _parse(output) == (7, 10)

    def test_output_with_no_summary_line_is_zero_zero(self):
        """A crashed interpreter produces no summary; report nothing rather than guess."""
        assert _parse("Traceback (most recent call last):\n  ImportError: boom\n") == (0, 0)
