# Feature 08: integration_test_framework

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery lines 389-408)

**Purpose:** Create integration test runners for all scripts

**What's In Scope:**
- Create 7 individual test runners (one per script from Features 01-07)
- Enhance 2 existing simulation integration tests
- Create master runner (run_all_integration_tests.py)
- Each test validates exit code AND specific expected outcomes
- Tests cover multiple argument combinations per script

**Estimated Size:** MEDIUM

### Relevant Discovery Decisions

**Recommended Approach:** Comprehensive Script-Specific Argparse (Option 2 from Discovery)
- Each script has script-specific arguments + universal flags
- Integration tests must validate all argument combinations
- Focus on CLI argument behavior (not internal logic)

**Implementation Constraints:**
- Cannot implement until Features 01-07 are implemented (S5-S7)
- Specs can be created in S2 based on Group 1 specs (available now)
- Actual test code written in S6 after dependencies complete

### Relevant User Answers (from Discovery)

**User Answer Q5 (lines 28, CRITICAL for this feature):**
"How should integration tests determine pass/fail? Exit code only or also check output?"
**Answer:** "Check exit code AND verify expected outcomes (specific logs, result counts)"

**Impact on Feature 08:**
- All integration tests must check exit code 0 (success)
- All integration tests must validate specific outcomes:
  - Expected log messages appear
  - Expected output files exist
  - Expected result counts match
  - Expected file formats are correct

**User Answer Q3 (lines 26, affects test execution):**
"What makes an E2E run reasonable (3 min max)? What can be reduced/mocked?"
**Answer:** "Simulations: single run with 0-1 random configs. Fetchers: real APIs with data limiting args"

**Impact on Feature 08:**
- All integration tests use --e2e-test flag
- Tests complete in ≤3 minutes per script
- No long-running tests (use E2E mode for speed)

### Dependencies from Discovery

**Blocker Dependencies (must complete before Feature 08 S6):**
- Feature 01-07 implementations (scripts with argparse must exist to test)

**Reference Dependencies (need specs only, available now):**
- Features 01-07 spec.md files (CLI argument lists, E2E behaviors, validation requirements)

## Feature Purpose

Create integration test framework with 7 individual test runners and 1 master test runner to validate CLI argument behavior across all runner scripts.

## Dependencies

**Blocker Dependencies:**
- Feature 01 (player_fetcher) - need run_player_fetcher.py with argparse implemented
- Feature 02 (schedule_fetcher) - need run_schedule_fetcher.py with argparse implemented
- Feature 03 (game_data_fetcher) - need run_game_data_fetcher.py with enhanced argparse
- Feature 04 (historical_compiler) - need compile_historical_data.py with enhanced argparse
- Feature 05 (win_rate_simulation) - need run_win_rate_simulation.py with --e2e-test flag
- Feature 06 (accuracy_simulation) - need run_accuracy_simulation.py with --e2e-test flag
- Feature 07 (league_helper) - need run_league_helper.py with argparse implemented

**Reference Dependencies (available now):**
- Features 01-07 spec.md files (for CLI argument lists and E2E behavior specs)

## Components Affected

**Files to Modify (2 total):**

1. **tests/integration/test_simulation_integration.py**
   - **Source:** Epic Request (DISCOVERY.md line 395 - "Enhance 2 existing simulation integration tests")
   - **Modification:** Add new test class TestWinRateSimulationCLI with CLI subprocess tests
   - **Purpose:** Validate run_win_rate_simulation.py CLI arguments and --e2e-test flag
   - **Pattern:** New test methods use subprocess.run() for CLI execution (research: run_all_tests.py lines 88-93)
   - **Preservation:** Existing Python API tests remain untouched

2. **tests/integration/test_accuracy_simulation_integration.py**
   - **Source:** Epic Request (DISCOVERY.md line 395 - "Enhance 2 existing simulation integration tests")
   - **Modification:** Add new test class TestAccuracySimulationCLI with CLI subprocess tests
   - **Purpose:** Validate run_accuracy_simulation.py CLI arguments and --e2e-test flag
   - **Pattern:** Same as test_simulation_integration.py CLI tests
   - **Preservation:** Existing Python API tests remain untouched

**New Files to Create (6 total):**

1. **tests/integration/test_player_fetcher_cli.py**
   - **Source:** Epic Request (DISCOVERY.md line 394)
   - **Purpose:** Validate run_player_fetcher.py CLI arguments and E2E mode
   - **Pattern:** pytest with subprocess.run() for CLI execution (research: run_all_tests.py lines 88-93)

2. **tests/integration/test_schedule_fetcher_cli.py**
   - **Source:** Epic Request (DISCOVERY.md line 394)
   - **Purpose:** Validate run_schedule_fetcher.py CLI arguments and E2E mode
   - **Pattern:** Same as test_player_fetcher_cli.py

3. **tests/integration/test_game_data_fetcher_cli.py**
   - **Source:** Epic Request (DISCOVERY.md line 394)
   - **Purpose:** Validate run_game_data_fetcher.py CLI arguments and E2E mode
   - **Pattern:** Same as test_player_fetcher_cli.py

4. **tests/integration/test_historical_compiler_cli.py**
   - **Source:** Epic Request (DISCOVERY.md line 394)
   - **Purpose:** Validate compile_historical_data.py CLI arguments and E2E mode
   - **Pattern:** Same as test_player_fetcher_cli.py

5. **tests/integration/test_league_helper_cli.py**
   - **Source:** Epic Request (DISCOVERY.md line 394)
   - **Purpose:** Validate run_league_helper.py CLI arguments, --mode selection, and E2E mode (all 5 modes)
   - **Pattern:** Same as test_player_fetcher_cli.py but with mode-specific tests

6. **tests/integration/run_all_integration_tests.py**
   - **Source:** Epic Request (DISCOVERY.md line 396 - "Create master runner")
   - **Purpose:** Master test runner that executes all 7 CLI test runners (5 new files + 2 enhanced files) and aggregates results
   - **Pattern:** Similar to tests/run_all_tests.py (research: 324 lines, TestRunner class with discover/execute/aggregate)

**Existing Files NOT Modified (Beyond the 2 Enhancements Above):**
- tests/integration/test_league_helper_integration.py (existing Python API tests, untouched)
- tests/integration/test_data_fetcher_integration.py (existing Python API tests, untouched)
- tests/integration/test_game_conditions_integration.py (existing, untouched)

## Requirements

### R1: Create CLI Test Runners for All 7 Scripts

**Source:** Epic Request (DISCOVERY.md lines 394-395) + User Answer Q7 (Option B)
**Traceability:** "Create 7 individual test runners" + "Enhance 2 existing simulation integration tests"

**Description:** Create or enhance integration test runners for all 7 scripts to validate CLI argument behavior.

**Implementation Approach:**
- **5 New CLI Test Files:** Create dedicated CLI test files for features 01-04, 07
  - test_player_fetcher_cli.py (Feature 01)
  - test_schedule_fetcher_cli.py (Feature 02)
  - test_game_data_fetcher_cli.py (Feature 03)
  - test_historical_compiler_cli.py (Feature 04)
  - test_league_helper_cli.py (Feature 07)
- **2 Enhanced Existing Files:** Add CLI test classes to existing integration test files for features 05-06
  - test_simulation_integration.py - add TestWinRateSimulationCLI class
  - test_accuracy_simulation_integration.py - add TestAccuracySimulationCLI class
  - Preservation: Existing Python API tests remain untouched

**Implementation Pattern:**
- Use pytest framework (pattern from test_simulation_integration.py)
- Use subprocess.run() to execute scripts with CLI arguments (pattern from run_all_tests.py lines 88-93)
- Test pattern: `result = subprocess.run([sys.executable, "run_script.py", "--arg"], capture_output=True, text=True, cwd=project_root)`
- Each test runner focuses on CLI argument validation (NOT internal logic testing)

**Test Coverage per Runner:**
- --help argument (displays help text)
- --debug argument (enables DEBUG logging)
- --e2e-test argument (runs fast E2E mode, ≤180 seconds)
- --log-level argument (accepts DEBUG/INFO/WARNING/ERROR/CRITICAL)
- **Precedence Rule:** When both --debug and --log-level provided, --debug FORCES DEBUG level (ignores --log-level)
  - **Cross-Feature Alignment Override:** Originally User Answer Q3 selected Option B (--log-level wins), but Features 01-07 all implement Option A (--debug forces DEBUG). Feature 08 tests must match actual implementation behavior.
- Script-specific arguments (from respective feature specs)
- Representative argument combinations (3-5 per script - see R5)

### R2: Validate Exit Codes AND Specific Outcomes

**Source:** User Answer Q5 (DISCOVERY.md line 404)
**Traceability:** "Tests check exit code AND expected outcomes (specific logs, result counts)"

**Description:** All integration tests must validate BOTH exit codes AND specific expected outcomes.

**Implementation:**
- Exit code validation: `assert result.returncode == 0, f"Script failed: {result.stderr}"`
- Specific outcome validation (all required):
  1. **Log validation:** Check for expected DEBUG messages when --debug used
  2. **File validation:** Verify expected output files exist (for fetchers, compiler)
  3. **Count validation:** Check expected result counts (recommendations, trades, etc. for league helper)
  4. **Format validation:** Verify CSV column headers / JSON structure keys (NOT full content validation)
     - User Answer Q1: Option B (Format Headers - Moderate)
     - Check structure (headers/keys) without brittleness of full content validation
     - Example: `assert csv_headers == expected_headers`

**Example (from research - User Answer Q5):**
```python
# Exit code check
assert result.returncode == 0

# Specific outcome checks
assert "DEBUG" in result.stderr  # Log validation
assert output_file.exists()  # File validation

# Format validation (Q1: Option B - headers only)
with open(output_file, 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    assert headers == expected_headers  # Structure check, not content
```

### R3: Use --e2e-test Mode for All Tests

**Source:** User Answer Q3 + Epic Requirement (DISCOVERY.md line 26, 408)
**Traceability:** "E2E modes ≤3 minutes" and "Tests cover multiple argument combinations per script"

**Description:** All integration tests use --e2e-test flag to ensure fast execution.

**Implementation:**
- All test scenarios include --e2e-test flag
- Total test suite execution ≤21 minutes (7 scripts × 3 min max)
- No long-running tests (no full simulations, no full data fetches)
- Verify E2E mode completes in ≤180 seconds: `assert execution_time <= 180`

### R4: Create Master Test Runner

**Source:** Epic Request (DISCOVERY.md line 403)
**Traceability:** "Create master runner (run_all_integration_tests.py)"

**Description:** Create master test runner that executes all 7 individual test runners and aggregates results.

**Implementation (pattern from run_all_tests.py):**
- Discover all 7 test files in tests/integration/:
  - 5 new CLI test files: test_*_cli.py
  - 2 enhanced files: test_simulation_integration.py, test_accuracy_simulation_integration.py
- Execute each test file via subprocess (pytest subprocess pattern from run_all_tests.py lines 88-93)
- Capture results: passed count, total count, exit code per test runner
- **Output Format (User Answer Q4: Option B - Moderate Per-File Summary):**
  - Display per-file summary during execution: `test_player_fetcher_cli.py: PASS (5/5 tests)`
  - Display aggregate summary at end: `Integration Tests: 7/7 test runners passed (45/45 tests)`
  - Shows progress, identifies failures, balances readability with debugging utility
- Exit codes:
  - Exit 0 if ALL 7 test runners pass (100% pass rate)
  - Exit 1 if ANY test runner fails

**Master Runner Class Structure (derived from run_all_tests.py):**
```python
class IntegrationTestRunner:
    def discover_test_files() -> List[Path]  # Find test_*.py files
    def run_pytest_on_file(test_file) -> Tuple[bool, int, int, str]  # Run single test
    def run_all_tests() -> bool  # Execute all, aggregate, exit 0/1
```

### R5: Test Argument Combinations

**Source:** Derived (necessary to validate argparse correctness)
**Traceability:** Comprehensive testing requires validating argument combinations, not just individual arguments

**Description:** Tests validate multiple argument combinations to ensure argparse handles all cases correctly.

**Implementation (User Answer Q2: Option B - Representative Samples):**
- Use pytest.mark.parametrize for argument combination testing (pattern from test_simulation_integration.py)
- Test **3-5 key combinations per script** (not exhaustive):
  1. --help (basic smoke test)
  2. --debug + --e2e-test (primary debug mode)
  3. --log-level with 2 different values (INFO, WARNING)
  4. Script-specific combinations (e.g., --mode + --e2e-test for league helper)
  5. --log-level + --debug (verify precedence rule)
- Balances coverage with test execution speed (avoids exponential growth)
- **Note:** Backward compatibility NOT tested in integration tests (User Answer Q6: Option C - trust implementation)

**Example parametrized test:**
```python
@pytest.mark.parametrize("args,expected_log_level", [
    (["--debug"], "DEBUG"),
    (["--log-level", "WARNING"], "WARNING"),
    (["--debug", "--log-level", "INFO"], "DEBUG"),  # debug forces DEBUG (Features 01-07 behavior)
    (["--debug", "--e2e-test"], "DEBUG"),
])
def test_argument_combinations(args, expected_log_level):
    result = subprocess.run([sys.executable, "run_script.py", *args],
                          capture_output=True, text=True)
    assert result.returncode == 0
```

### R6: Pytest Framework Consistency

**Source:** Derived (existing test infrastructure)
**Traceability:** Project uses pytest for all tests (research: test_simulation_integration.py lines 12-29)

**Description:** All integration test runners use pytest framework for consistency with existing tests.

**Implementation:**
- Use pytest.fixture for test data setup (pattern from test_simulation_integration.py lines 99-145)
- Use pytest.mark.parametrize for argument combinations
- Use pytest assertions for validation
- Follow existing test file naming: test_{script_name}.py
- Follow existing test class naming: class Test{ScriptName}CLI

### R7: Test Cleanup Strategy

**Source:** User Answer Q5 (Option B - Cleanup on Pass, Keep on Fail)
**Traceability:** Derived requirement for managing temporary files created during CLI test execution

**Description:** Integration tests should clean up temporary output files created by scripts, but preserve files when tests fail for debugging.

**Implementation:**
- Use pytest fixtures with conditional cleanup in teardown
- **Cleanup on Pass:** Delete temporary files when test succeeds (clean environment)
- **Keep on Fail:** Preserve files when test fails (allows debugging)
- Applies to fetcher scripts (CSV outputs) and compiler (compiled data files)

**Example Pattern:**
```python
@pytest.fixture
def temp_output_files(tmp_path):
    """Manage temporary output files with conditional cleanup"""
    output_files = []
    yield output_files

    # Conditional cleanup in teardown
    if not hasattr(pytest, 'last_test_failed') or not pytest.last_test_failed:
        # Test passed - cleanup
        for file in output_files:
            if file.exists():
                file.unlink()
    # Test failed - preserve files for debugging
```

**Benefits:**
- Balances clean test environment with debugging capability
- Failed tests leave files for manual inspection
- Successful tests don't accumulate disk usage

## Data Structures

### Test Execution Data

**Input:** CLI arguments as list of strings
```python
args = ["run_player_fetcher.py", "--debug", "--e2e-test"]
```

**Output:** subprocess.CompletedProcess
```python
result = subprocess.CompletedProcess(
    returncode=0,  # Exit code
    stdout="...",  # Standard output
    stderr="..."   # Standard error (includes logs)
)
```

### Validation Data

**Expected Outcomes Structure:**
```python
expected_outcomes = {
    "exit_code": 0,
    "output_files": ["data/player_stats_league1.csv"],
    "log_messages": ["DEBUG", "Fetching player data"],
    "result_counts": None  # For fetchers
}
```

**For League Helper:**
```python
expected_outcomes = {
    "exit_code": 0,
    "output_files": [],
    "log_messages": ["Running mode 1", "Running mode 5"],
    "result_counts": {
        "modes_executed": 5,
        "recommendations": 2,  # debug count
        "trades": 1  # debug count
    }
}
```

## Algorithms

### Individual Test Runner Algorithm

**Pseudocode:**
```
For each test case (argument combination):
    1. Build command: [sys.executable, "run_script.py", *args]
    2. Execute via subprocess.run(command, capture_output=True, text=True, cwd=project_root)
    3. Validate exit code: assert result.returncode == 0
    4. Validate specific outcomes:
       a. If --debug in args: assert "DEBUG" in result.stderr
       b. If script creates files: assert output_file.exists()
       c. If script shows results: assert expected count in output
       d. Verify execution time ≤ 180 seconds (E2E mode requirement)
    5. Return test pass/fail
```

### Master Test Runner Algorithm

**Pseudocode (pattern from run_all_tests.py):**
```
1. Discover test files:
   - Find all test_*.py files in tests/integration/
   - Filter to only Feature 08 test files (test_player_fetcher.py, etc.)
   - Exclude existing tests (test_simulation_integration.py, etc.)

2. For each test file:
   a. Run pytest via subprocess: subprocess.run([python, "-m", "pytest", test_file])
   b. Parse output for passed/total counts
   c. Collect result: (test_file, passed, total, success)

3. Aggregate results:
   - Total passed across all test files
   - Total tests across all test files
   - Test runners passed (7/7 if all passed)

4. Display summary:
   - Show per-file results
   - Show aggregate totals
   - Show pass rate

5. Exit:
   - Exit code 0 if 100% tests passed
   - Exit code 1 if any test failed
```

## Testing Strategy

### Unit Tests for Feature 08

**Source:** Derived (test the test framework itself)
**Scope:** QUESTION for checklist - how much unit testing for test infrastructure?

**Potential unit tests:**
- Test master runner discovery logic (finds correct 7 files)
- Test result parsing (correctly extracts passed/total from pytest output)
- Test aggregation logic (correctly sums results)

### Integration Testing for Feature 08

**Integration tests ARE the feature** - Feature 08 creates integration tests, not business logic.

**Validation:**
- All 7 individual test runners execute successfully
- Master runner executes all 7 test runners
- All tests use --e2e-test mode
- All tests validate exit codes + specific outcomes
- Total execution time ≤21 minutes (7 × 3 min)

## Cross-Feature Alignment

**Compared To:** Features 01-07 (all S2 Complete, S3 Complete)
**Alignment Date:** 2026-01-30
**Alignment Status:** ✅ Aligned with 1 precedence rule override

### Alignment Verification Summary

**Features Compared:**
- Feature 01: player_fetcher (run_player_fetcher.py)
- Feature 02: schedule_fetcher (run_schedule_fetcher.py)
- Feature 03: game_data_fetcher (run_game_data_fetcher.py)
- Feature 04: historical_compiler (compile_historical_data.py)
- Feature 05: win_rate_simulation (run_win_rate_simulation.py)
- Feature 06: accuracy_simulation (run_accuracy_simulation.py)
- Feature 07: league_helper (run_league_helper.py)

### Universal Arguments Alignment ✅

**All 7 scripts implement 3 universal arguments:**
- `--debug` (enables DEBUG logging)
- `--e2e-test` (fast E2E mode ≤180 seconds)
- `--log-level` (DEBUG/INFO/WARNING/ERROR/CRITICAL)

**Verification:** Feature 08 tests will validate all 3 universal arguments for all 7 scripts.

### Backward Compatibility Arguments ✅

**Identified backward-compatible arguments:**
- **Feature 04 only:** `--verbose` (alias for `--log-level DEBUG`)
  - Rationale: compile_historical_data.py had `--verbose` before epic
  - Precedence: `--verbose` forces DEBUG level (same as `--debug`)

**User Answer Q6:** Option C (Skip backward compat tests - trust implementation)
**Impact:** Feature 08 will NOT create dedicated tests for `--verbose` backward compatibility

### Precedence Rule Conflict ⚠️ RESOLVED

**Conflict Found:**
- **User Answer Q3:** Option B (--log-level takes precedence / last wins)
- **Features 01-07 specs:** All implement Option A (--debug forces DEBUG level)

**Resolution:**
- **Override Applied:** User Answer Q3 (Option B) overridden to Option A
- **Rationale:** Feature 08 tests must validate ACTUAL behavior from Features 01-07
- **Final Rule:** `--debug` FORCES DEBUG level (ignores `--log-level` if both provided)

**Updated spec sections:**
- R1: Test Coverage per Runner (precedence rule updated)
- R5: Example parametrized test (corrected to expect DEBUG when both flags present)
- Acceptance Criteria #5 (precedence rule corrected)

### Script-Specific Arguments ✅

**No conflicts found** - each script's unique arguments are appropriate for its functionality:
- Feature 01: 20+ arguments (most complex - player data fetcher)
- Feature 02: 2 arguments (simplest - schedule fetcher)
- Feature 03: 4 arguments (game data fetcher)
- Feature 04: 4 arguments (historical compiler)
- Feature 05: 8 arguments (win rate simulation)
- Feature 06: 3 arguments (accuracy simulation)
- Feature 07: 6 arguments + --silent flag (league helper)

**Verification:** Feature 08 tests will validate representative combinations (3-5 per script) including script-specific arguments.

### Output Argument Naming ✅

**Different patterns identified (intentional, not conflicts):**
- Features 01, 04, 07: Use `--output-dir` (directory output)
- Feature 02: Uses `--output-path` (single file output)
- Features 03, 05: Use `--output` (existing/new argument)

**Resolution:** No conflict - different scripts have different output patterns.

### Changes Made to Feature 08 Spec

**Due to cross-feature alignment:**
1. **R1 (Test Coverage):** Updated precedence rule from "log-level wins" to "debug forces DEBUG"
2. **R5 (Example):** Updated parametrized test example to expect DEBUG when both flags present
3. **Acceptance Criteria #5:** Updated precedence rule description
4. **checklist.md Q3:** Documented override with rationale

**No changes made to Features 01-07** - all alignment corrections applied to Feature 08 only.

### Alignment Conclusion

**Conflicts Resolved:** 1 (precedence rule)
**No Remaining Conflicts:** All Feature 08 requirements now align with Features 01-07 specifications
**Ready for Implementation:** Yes - Feature 08 spec correctly reflects Features 01-07 CLI behavior

**Verified By:** Agent (Primary - KAI-7)
**Date:** 2026-01-30

## Acceptance Criteria

**Feature 08 is complete when:**

1. ✅ All 7 CLI test runners created/enhanced and passing
   - **5 New CLI Test Files:**
     - test_player_fetcher_cli.py
     - test_schedule_fetcher_cli.py
     - test_game_data_fetcher_cli.py
     - test_historical_compiler_cli.py
     - test_league_helper_cli.py
   - **2 Enhanced Existing Files (CLI test classes added):**
     - test_simulation_integration.py (TestWinRateSimulationCLI class added)
     - test_accuracy_simulation_integration.py (TestAccuracySimulationCLI class added)

2. ✅ Master test runner created and passing
   - run_all_integration_tests.py executes all 7 test runners (5 new files + 2 enhanced files)
   - Aggregates results correctly with per-file summary output
   - Exits with code 0 if all pass, 1 if any fail

3. ✅ All tests validate exit codes AND specific outcomes (User Answer Q5)
   - Exit code 0 checked
   - Log messages validated (DEBUG when --debug used)
   - Output files verified (existence)
   - File format validated (CSV headers / JSON keys - User Answer Q1: Option B)

4. ✅ All tests use --e2e-test mode
   - Each script test uses --e2e-test flag
   - Tests complete in ≤180 seconds per script

5. ✅ Argument combination testing implemented (User Answer Q2: Option B)
   - 3-5 representative combinations per script
   - Precedence rule validated: --debug FORCES DEBUG level (overrides --log-level if both provided)
     - Note: User Answer Q3 (Option B) overridden during Phase 5 alignment to match Features 01-07 behavior

6. ✅ Test cleanup strategy implemented (User Answer Q5: Option B)
   - Cleanup on pass, keep files on failure for debugging

7. ✅ Test suite passes when run via pytest tests/integration/run_all_integration_tests.py

---

## User Approval

- [x] **I approve these acceptance criteria**

**Approval Timestamp:** 2026-01-30 20:30

**Approval Notes:**
User approved on 2026-01-30 with no modifications requested. One precedence rule override was applied during Phase 5 alignment (User Answer Q3: Option B → Option A to match Features 01-07 behavior).
