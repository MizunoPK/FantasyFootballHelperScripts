# Feature 08: integration_test_framework - Research Findings

Date: 2026-01-30
Epic: KAI-7 improve_configurability_of_scripts
Phase: S2.P1 (Research Phase)

## Discovery Context Summary

From DISCOVERY.md lines 389-408:
- Purpose: Create 7 individual test runners + 1 master runner
- User Answer Q5 (CRITICAL): Tests check exit code AND specific outcomes (logs, files, counts)
- Dependencies: Features 01-07 implementations (blocker), Features 01-07 specs (available now)
- Estimated Size: MEDIUM

## Components Researched

### Component 1: Existing Integration Test Infrastructure

File: tests/integration/test_simulation_integration.py
Lines Read: 1-150, 200-299 (total 450 lines read)
Evidence: Actual code patterns for pytest fixtures, mock data, test validation

Key Findings:
- Pytest fixture pattern (lines 99-145): create temp data, use fixtures for setup
- Mock data creation (lines 58-97): create_mock_historical_season() pattern
- Test class structure (line 248): class Test{Component}Integration
- Import pattern (lines 12-29): add paths, import modules
- Validation pattern: assert statements for expected values
- CRITICAL: Existing tests import modules directly (NOT subprocess)

### Component 2: Master Test Runner Pattern

File: tests/run_all_tests.py
Lines Read: Complete file (324 lines)
Evidence: Full master runner implementation with subprocess

Key Findings (with line numbers):
- TestRunner class (lines 25-228): discovery, execution, aggregation
- discover_test_files() (lines 57-66): find all test_*.py files
- run_pytest_on_file() (lines 68-106): subprocess.run() pattern
- Subprocess pattern (lines 88-93): capture_output=True, text=True, cwd=project_root
- Validation pattern (lines 100-101): result.returncode == 0 AND passed_count == total_count
- Result aggregation (lines 163-187): collect results from all test files
- 100% pass requirement (lines 203-227): strict requirement, exit code 0 if all pass

### Component 3: CLI Arguments from Group 1 Specs

Files Reviewed: All 7 Group 1 feature specs
Evidence: Requirement sections show --debug, --e2e-test, --log-level patterns

Key Findings:
- Universal arguments: --debug, --e2e-test, --log-level (all 7 scripts)
- Script-specific arguments: Vary per script (documented in each spec)
- Feature 02: R1 shows 5 arguments total
- Feature 05: R1, R2, R2a show --e2e-test, --debug, --log-level
- Feature 06: R1, R5, R10 show E2E and debug flag requirements
- Feature 07: R1-R4 show argparse, mode selection, E2E, debug

## Research Completeness Audit

Category 1: Component Knowledge - PASSED
- Can list EXACT files to create: 8 files (7 individual + 1 master)
- Read actual code: test_simulation_integration.py (450 lines), run_all_tests.py (324 lines)
- Can cite method signatures: subprocess.run(), TestRunner class, discover_test_files()

Category 2: Pattern Knowledge - PASSED
- Searched for similar features: Found master test runner (run_all_tests.py)
- Read implementation: Complete 324-line file
- Can describe pattern: TestRunner class, pytest subprocess execution, result aggregation

Category 3: Data Structure Knowledge - PASSED
- Read actual files: test_simulation_integration.py shows pytest patterns
- Current format: pytest fixtures, test classes, parametrized tests
- Verified from source: Lines 99-145 (fixtures), 248-299 (test methods)

Category 4: Discovery Context Knowledge - PASSED
- Reviewed DISCOVERY.md: Feature 08 section lines 389-408
- Feature scope: 7 individual + 1 master runner, User Answer Q5 validation
- User Answer Q5: Exit codes + specific outcomes (logs, files, counts)

OVERALL AUDIT RESULT: PASSED (all 4 categories)

## Implementation Approach

Pattern Established by Feature 08 (NEW):
- Existing tests: Import modules directly, test Python APIs
- Feature 08 tests: Use subprocess.run() to test CLI scripts
- Why different: Need to validate CLI argument behavior (argparse), not just Python APIs
- Reference pattern: run_all_tests.py (lines 88-93) for subprocess execution

Master Runner Pattern (from run_all_tests.py):
- TestRunner class with discover_test_files()
- Run each test file via subprocess
- Aggregate results (passed/total counts)
- Exit code 0 if ALL tests pass, 1 if ANY fail
- 100% pass requirement

Individual Test Pattern (derived from existing + subprocess):
- Test class per script: class TestPlayerFetcherCLI
- Parametrized tests: @pytest.mark.parametrize for argument combinations
- Subprocess execution: subprocess.run([sys.executable, "run_player_fetcher.py", "--debug", "--e2e-test"])
- Dual validation: assert result.returncode == 0 AND assert expected outcomes

Research Phase COMPLETE - Ready for S2.P2 Specification Phase
