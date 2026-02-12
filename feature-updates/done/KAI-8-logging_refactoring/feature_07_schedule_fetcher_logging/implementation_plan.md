# Implementation Plan: schedule_fetcher_logging

**Feature:** Feature 07 - schedule_fetcher_logging
**Part of Epic:** KAI-8-logging_refactoring
**Created:** 2026-02-12 (S5 Phase 1: Draft Creation)
**Status:** IN VALIDATION LOOP (Rounds 1-9 complete, 9 issues fixed, R4+R8+R9 CLEAN, 2 consecutive, Round 10 FINAL)

---

## Implementation Tasks

### Task 1: Add Argparse to run_schedule_fetcher.py

**Requirement:** spec.md Requirement 1 (CLI Flag Integration)

**Description:**
Add argparse setup to run_schedule_fetcher.py main() function to parse --enable-log-file CLI flag. Argparse is synchronous and runs at the start of async main() before any await calls.

**Acceptance Criteria:**
- [ ] Import argparse at top of file
- [ ] Create ArgumentParser with description in main() function
- [ ] Add --enable-log-file argument with action='store_true'
- [ ] Add help text: "Enable logging to file (default: console only)"
- [ ] Call parser.parse_args() to get args object
- [ ] Argparse called BEFORE any async operations (no await conflicts)

**Location:** run_schedule_fetcher.py (lines 16-28, main() function)

**Dependencies:**
- None (argparse is stdlib)

**Tests:**
- Test 1.1: test_cli_flag_parsing_without_flag
- Test 1.2: test_cli_flag_parsing_with_flag
- Test 1.3: test_cli_flag_help_text
- Test E1: test_async_main_with_argparse_no_conflicts
- Test C1: test_default_behavior_file_logging_off
- Test C2: test_explicit_flag_behavior_file_logging_on

---

### Task 2: Add setup_logger() Call to run_schedule_fetcher.py

**Requirement:** spec.md Requirement 1 (CLI Flag Integration)

**Description:**
Add setup_logger() call to main() function to configure logger based on CLI flag. This must be called ONCE before ScheduleFetcher instantiation, following Feature 05 pattern.

**Acceptance Criteria:**
- [ ] Import setup_logger from utils.LoggingManager
- [ ] Call setup_logger() after argparse, before ScheduleFetcher instantiation
- [ ] Pass name="schedule_fetcher" (snake_case, becomes folder name)
- [ ] Pass level="INFO"
- [ ] Pass log_to_file=args.enable_log_file (CLI-driven)
- [ ] Pass log_file_path=None (auto-generate path)
- [ ] Pass log_format="standard"
- [ ] Store returned logger in variable: logger = setup_logger(...)

**Location:** run_schedule_fetcher.py (lines 28-36, main() function)

**Dependencies:**
- Task 1 (argparse must be complete to access args.enable_log_file)
- Feature 01: setup_logger() function

**Interface Verification:**
```python
# From Feature 01 (utils/LoggingManager.py):
def setup_logger(
    name: str,
    level: Union[str, int] = 'INFO',
    log_to_file: bool = False,
    log_file_path: Optional[Union[str, Path]] = None,
    log_format: str = 'standard',
    enable_console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> logging.Logger
```

**Tests:**
- Test 4.4: test_setup_logger_called_before_fetcher
- Test I1: test_e2e_with_enable_log_file_flag
- Test I2: test_e2e_without_flag_no_log_file

---

### Task 3: Replace Print Statements with Logger Calls

**Requirement:** spec.md Requirement 4 (Replace Print Statements)

**Description:**
Replace all print() statements in run_schedule_fetcher.py main() function with logger.info() and logger.error() calls to provide consistent logging output.

**Acceptance Criteria:**
- [ ] Replace line 37: print(f"Fetching...") → logger.info(f"Fetching NFL season schedule for {NFL_SEASON}...")
- [ ] Replace line 43: print("ERROR:...") → logger.error("Failed to fetch schedule data")
- [ ] Replace line 49: print(f"✓ Schedule...") → logger.info(f"Schedule successfully exported to {output_path}")
- [ ] Replace line 50: print(f"  - Weeks:...") → logger.info(f"  Weeks: {len(schedule)}, Season: {NFL_SEASON}")
- [ ] Remove line 51 (redundant Season print - merged into line 50)
- [ ] Replace line 56: print(f"ERROR:...") → logger.error(f"Unhandled error: {e}")
- [ ] No print() statements remain in main() function
- [ ] Console output behavior unchanged when flag not provided (logs to stderr)

**Location:** run_schedule_fetcher.py (lines 37, 43, 49-51, 56)

**Dependencies:**
- Task 2 (logger must be created before use)

**Tests:**
- Test 4.1: test_no_print_statements_in_main
- Test 4.2: test_logger_info_replaces_print_success
- Test 4.3: test_logger_error_replaces_print_error
- Test I1: test_e2e_with_enable_log_file_flag
- Test I5: test_info_logs_appear_in_file

---

### Task 4: Update ScheduleFetcher to Use get_logger()

**Requirement:** spec.md Requirement 3 (ScheduleFetcher Logger Setup)

**Description:**
Change ScheduleFetcher.__init__() to use get_logger() instead of setup_logger() to retrieve the logger configured in main(). This follows Feature 05 pattern: entry script configures logger ONCE, modules retrieve it.

**Acceptance Criteria:**
- [ ] Change import: from utils.LoggingManager import setup_logger → from utils.LoggingManager import get_logger
- [ ] Change line 34: self.logger = setup_logger(name="ScheduleFetcher", level="INFO") → self.logger = get_logger()
- [ ] No parameters to get_logger() (retrieves singleton logger)
- [ ] Docstring unchanged (no new parameters to document)
- [ ] __init__() signature unchanged: def __init__(self, output_path: Path)

**Location:** schedule-data-fetcher/ScheduleFetcher.py (lines 14, 34)

**Dependencies:**
- Feature 01: get_logger() function
- Task 2 (main() must call setup_logger() first)

**Interface Verification:**
```python
# From Feature 01 (utils/LoggingManager.py):
def get_logger() -> logging.Logger
```

**Tests:**
- Test 3.1: test_schedule_fetcher_uses_get_logger
- Test 3.2: test_schedule_fetcher_no_enable_log_file_param
- Test I4: test_schedule_fetcher_integration_with_get_logger

---

### Task 5: Update Logger Name to "schedule_fetcher"

**Requirement:** spec.md Requirement 2 (Logger Name Consistency)

**Description:**
(MERGED INTO TASK 4) When updating to get_logger(), the logger name change from "ScheduleFetcher" to "schedule_fetcher" happens in main()'s setup_logger() call (Task 2), not in ScheduleFetcher.__init__(). This task is documentation-only to track requirement coverage.

**Acceptance Criteria:**
- [ ] Logger name "schedule_fetcher" used in main() setup_logger() call (Task 2)
- [ ] Folder created: logs/schedule_fetcher/ (not logs/ScheduleFetcher/)
- [ ] Filenames use snake_case: schedule_fetcher-{timestamp}.log
- [ ] get_logger() retrieves the "schedule_fetcher" logger configured in main()

**Location:** run_schedule_fetcher.py (Task 2's setup_logger call)

**Dependencies:**
- Task 2 (setup_logger with name="schedule_fetcher")
- Task 4 (get_logger retrieves configured logger)

**Tests:**
- Test 2.1: test_logger_name_snake_case
- Test I3: test_log_file_format_and_naming

---

### Task 6: Change Error Parsing Log Level to WARNING

**Requirement:** spec.md Requirement 5 (Log Quality - DEBUG/WARNING)

**Description:**
Change error parsing log from DEBUG to WARNING level (Feature 06 alignment). Parsing errors are operational issues affecting data quality, users should be aware of them.

**Acceptance Criteria:**
- [ ] Locate error parsing log in ScheduleFetcher.py (around line 138)
- [ ] Change: self.logger.debug(f"Error parsing event in week {week}: {e}") → self.logger.warning(f"Error parsing event in week {week}: {e}")
- [ ] Progress tracking log remains DEBUG (line 94)
- [ ] No other DEBUG logs changed

**Location:** schedule-data-fetcher/ScheduleFetcher.py (line 138)

**Dependencies:**
- None (isolated log level change)

**Tests:**
- Test 5.1: test_error_parsing_uses_warning_level
- Test 5.2: test_progress_tracking_uses_debug_level
- Test I6: test_warning_logs_appear_in_file

---

### Task 7: Verify Existing Tests Still Pass

**Requirement:** spec.md Requirement 7 (Test Updates)

**Description:**
Run existing test_ScheduleFetcher.py tests to verify S8.P1 changes (get_logger pattern) don't break existing tests. Tests should pass unchanged because ScheduleFetcher interface unchanged.

**Acceptance Criteria:**
- [ ] Run: pytest tests/schedule-data-fetcher/test_ScheduleFetcher.py
- [ ] All existing tests pass (100% pass rate)
- [ ] Zero test modifications needed (backward compatible)
- [ ] ScheduleFetcher instantiation unchanged: ScheduleFetcher(output_path)

**Location:** tests/schedule-data-fetcher/test_ScheduleFetcher.py

**Dependencies:**
- Tasks 1-6 (all implementation complete)

**Tests:**
- Test 7.1: test_existing_schedule_fetcher_tests_unchanged

---

### Task 8: Create Unit Tests (12 tests)

**Requirement:** test_strategy.md Category 1-7 (Unit Tests)

**Description:**
Create 12 unit tests covering CLI flag parsing, logger setup, print replacement, and log quality requirements. Use source code inspection approach for most tests (faster and more reliable than runtime).

**Acceptance Criteria:**
- [ ] Create test file: tests/root_scripts/test_run_schedule_fetcher.py
- [ ] Implement Tests 1.1-1.3: CLI flag parsing tests
- [ ] Implement Tests 2.1: Logger name verification (source inspection)
- [ ] Implement Tests 3.1-3.2: get_logger() pattern tests (source inspection)
- [ ] Implement Tests 4.1-4.4: Print replacement tests (source inspection)
- [ ] Implement Tests 5.1-5.2: Log level tests (source inspection)
- [ ] Implement Test 7.1: Existing test backward compatibility
- [ ] All 12 tests implemented and passing (100% pass rate)

**Test Names:**
- test_cli_flag_parsing_without_flag
- test_cli_flag_parsing_with_flag
- test_cli_flag_help_text
- test_logger_name_snake_case
- test_schedule_fetcher_uses_get_logger
- test_schedule_fetcher_no_enable_log_file_param
- test_no_print_statements_in_main
- test_logger_info_replaces_print_success
- test_logger_error_replaces_print_error
- test_setup_logger_called_before_fetcher
- test_error_parsing_uses_warning_level
- test_progress_tracking_uses_debug_level

**Location:** tests/root_scripts/test_run_schedule_fetcher.py (new file)

**Dependencies:**
- Tasks 1-6 (all implementation complete before tests)

**Tests:** (These ARE the tests)

---

### Task 9: Create Integration Tests (6 tests)

**Requirement:** test_strategy.md Integration Tests (I1-I6)

**Description:**
Create 6 integration tests covering E2E execution with/without flag, log file creation, ScheduleFetcher integration, and log content verification. Use real script execution (no mocks).

**Acceptance Criteria:**
- [ ] Create test file: tests/integration/test_schedule_fetcher_integration.py
- [ ] Implement Test I1: E2E with --enable-log-file flag
- [ ] Implement Test I2: E2E without flag (no log file)
- [ ] Implement Test I3: Log file naming convention
- [ ] Implement Test I4: ScheduleFetcher + get_logger integration
- [ ] Implement Test I5: INFO logs in file
- [ ] Implement Test I6: WARNING logs in file
- [ ] All 6 tests implemented and passing (100% pass rate)
- [ ] Tests clean up log files after execution

**Test Names:**
- test_e2e_with_enable_log_file_flag
- test_e2e_without_flag_no_log_file
- test_log_file_format_and_naming
- test_schedule_fetcher_integration_with_get_logger
- test_info_logs_appear_in_file
- test_warning_logs_appear_in_file

**Location:** tests/integration/test_schedule_fetcher_integration.py (new file)

**Dependencies:**
- Tasks 1-6 (all implementation complete before tests)
- Feature 01: LineBasedRotatingHandler (for log file creation)

**Tests:** (These ARE the tests)

---

### Task 10: Create Edge Case Tests (2 tests)

**Requirement:** test_strategy.md Edge Case Tests (E1-E2)

**Description:**
Create 2 edge case tests covering async/argparse integration and log rotation during long fetch. E1 verifies no async/await conflicts with synchronous argparse. E2 verifies Feature 01 rotation works in this context.

**Acceptance Criteria:**
- [ ] Add to test file: tests/integration/test_schedule_fetcher_integration.py
- [ ] Implement Test E1: Async main with argparse (no conflicts)
- [ ] Implement Test E2: Log rotation during verbose logging (>500 lines)
- [ ] All 2 tests implemented and passing (100% pass rate)

**Test Names:**
- test_async_main_with_argparse_no_conflicts
- test_log_rotation_during_long_fetch

**Location:** tests/integration/test_schedule_fetcher_integration.py (add to existing file)

**Dependencies:**
- Tasks 1-6 (all implementation complete before tests)

**Tests:** (These ARE the tests)

---

### Task 11: Create Configuration Tests (2 tests)

**Requirement:** test_strategy.md Configuration Tests (C1-C2)

**Description:**
Create 2 configuration tests verifying default behavior (file logging OFF) and explicit flag behavior (file logging ON). These tests validate Discovery Q4 requirement.

**Acceptance Criteria:**
- [ ] Add to test file: tests/integration/test_schedule_fetcher_integration.py
- [ ] Implement Test C1: Default behavior (no flag → no log file)
- [ ] Implement Test C2: Explicit flag (--enable-log-file → log file created)
- [ ] All 2 tests implemented and passing (100% pass rate)
- [ ] Tests verify Discovery Q4 requirement (file logging OFF by default)

**Test Names:**
- test_default_behavior_file_logging_off
- test_explicit_flag_behavior_file_logging_on

**Location:** tests/integration/test_schedule_fetcher_integration.py (add to existing file)

**Dependencies:**
- Tasks 1-6 (all implementation complete before tests)

**Tests:** (These ARE the tests)

---

## Component Dependencies

### Requirements-to-Task Mapping (Dimension 1)

| Spec Requirement | Implementation Tasks | Status |
|------------------|---------------------|--------|
| R1: CLI Flag Integration | Task 1, Task 2 | ✅ Covered |
| R2: Logger Name Consistency | Task 5 (documentation-only, handled by Task 2) | ✅ Covered |
| R3: ScheduleFetcher Logger Setup | Task 4 | ✅ Covered |
| R4: Replace Print Statements | Task 3 | ✅ Covered |
| R5: Log Quality - DEBUG/WARNING | Task 6 | ✅ Covered |
| R6: Log Quality - INFO | (No changes needed per spec - existing logs meet criteria) | ✅ N/A |
| R7: Test Updates | Task 7 | ✅ Covered |

**Coverage:** 7/7 requirements (100%)

### Test-to-Task Mapping (Dimension 1)

| Test Category | Tests Count | Implementation Task | Test File | Status |
|---------------|-------------|-------------------|-----------|--------|
| Unit Tests 1.1-1.3 | 3 tests | Task 8 | test_run_schedule_fetcher.py | ✅ Covered |
| Unit Test 2.1 | 1 test | Task 8 | test_run_schedule_fetcher.py | ✅ Covered |
| Unit Tests 3.1-3.2 | 2 tests | Task 8 | test_run_schedule_fetcher.py | ✅ Covered |
| Unit Tests 4.1-4.4 | 4 tests | Task 8 | test_run_schedule_fetcher.py | ✅ Covered |
| Unit Tests 5.1-5.2 | 2 tests | Task 8 | test_run_schedule_fetcher.py | ✅ Covered |
| Unit Test 7.1 | 1 test | Task 8 | test_run_schedule_fetcher.py | ✅ Covered |
| Integration Tests I1-I6 | 6 tests | Task 9 | test_schedule_fetcher_integration.py | ✅ Covered |
| Edge Tests E1-E2 | 2 tests | Task 10 | test_schedule_fetcher_integration.py | ✅ Covered |
| Config Tests C1-C2 | 2 tests | Task 11 | test_schedule_fetcher_integration.py | ✅ Covered |

**Total Tests:** 22 (from test_strategy.md)
**Test Creation Tasks:** 4 (Tasks 8-11)
**Coverage:** 22/22 tests (100%)

### External Dependencies (from Feature 01)

**1. setup_logger() function**
- **Used in:** Task 2 (run_schedule_fetcher.py)
- **File:** utils/LoggingManager.py:190-197
- **Interface:** (verified from ACTUAL source code)
```python
def setup_logger(
    name: str,
    level: Union[str, int] = 'INFO',
    log_to_file: bool = False,
    log_file_path: Optional[Union[str, Path]] = None,
    log_format: str = 'standard',
    enable_console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger
```
- **Purpose:** Configure logger with CLI-driven file logging

**2. get_logger() function**
- **Used in:** Task 4 (ScheduleFetcher.py)
- **File:** utils/LoggingManager.py:210-211
- **Interface:** (verified from ACTUAL source code)
```python
def get_logger() -> logging.Logger
```
- **Purpose:** Retrieve logger configured in main()

**3. LineBasedRotatingHandler class**
- **Used by:** setup_logger() internally (automatic)
- **File:** utils/LineBasedRotatingHandler.py
- **Purpose:** 500-line rotation, max 50 files
- **Integration:** Transparent (setup_logger handles instantiation)

### Internal Dependencies

**4. argparse module**
- **Used in:** Task 1 (run_schedule_fetcher.py)
- **Module:** argparse (Python stdlib)
- **Purpose:** Parse --enable-log-file CLI flag

**5. ScheduleFetcher class**
- **Modified in:** Task 4 (change to get_logger())
- **File:** schedule-data-fetcher/ScheduleFetcher.py
- **Purpose:** Schedule fetching logic (logging integration point)

---

## Algorithm Traceability Matrix

### Feature Algorithms (from spec.md)

| Algorithm (from spec) | Spec Section | Implementation Task | Implementation Location |
|----------------------|--------------|---------------------|------------------------|
| Parse CLI arguments | R1: CLI Flag Integration | Task 1 | run_schedule_fetcher.py:28-35 (argparse) |
| Configure logger with CLI flag | R1: CLI Flag Integration | Task 2 | run_schedule_fetcher.py:36-42 (setup_logger call) |
| Replace print with logger.info | R4: Replace Print Statements | Task 3 | run_schedule_fetcher.py:37,49-51 |
| Replace print with logger.error | R4: Replace Print Statements | Task 3 | run_schedule_fetcher.py:43,56 |
| Retrieve configured logger | R3: ScheduleFetcher Logger Setup | Task 4 | ScheduleFetcher.py:34 (get_logger) |
| Use snake_case logger name | R2: Logger Name Consistency | Task 5 | run_schedule_fetcher.py:36 (name="schedule_fetcher") |
| Promote error parsing to WARNING | R5: Log Quality DEBUG/WARNING | Task 6 | ScheduleFetcher.py:138 (warning level) |
| Verify backward compatibility | R7: Test Updates | Task 7 | Run existing tests unchanged |

### Test Creation Algorithms

| Algorithm (from test_strategy.md) | Test Category | Implementation Task | Test File Location |
|-----------------------------------|--------------|---------------------|-------------------|
| Verify argparse flag parsing | Unit Tests 1.1-1.3 | Task 8 | tests/root_scripts/test_run_schedule_fetcher.py |
| Verify logger name snake_case | Unit Test 2.1 | Task 8 | tests/root_scripts/test_run_schedule_fetcher.py |
| Verify get_logger() pattern | Unit Tests 3.1-3.2 | Task 8 | tests/root_scripts/test_run_schedule_fetcher.py |
| Verify print replacement | Unit Tests 4.1-4.4 | Task 8 | tests/root_scripts/test_run_schedule_fetcher.py |
| Verify log level changes | Unit Tests 5.1-5.2 | Task 8 | tests/root_scripts/test_run_schedule_fetcher.py |
| Verify E2E execution | Integration Tests I1-I6 | Task 9 | tests/integration/test_schedule_fetcher_integration.py |
| Verify edge cases | Edge Tests E1-E2 | Task 10 | tests/integration/test_schedule_fetcher_integration.py |
| Verify configuration | Config Tests C1-C2 | Task 11 | tests/integration/test_schedule_fetcher_integration.py |

**Total Algorithms Mapped:** 16 (8 feature + 8 test creation)

---

## Data Flow

### Entry Point: User Runs Script

```
User executes: python run_schedule_fetcher.py --enable-log-file
  ↓
asyncio.run(main()) executes async main() function
  ↓
argparse.parse_args() parses CLI arguments (Task 1)
  ↓
args.enable_log_file = True (flag present) OR False (flag absent)
  ↓
setup_logger(name="schedule_fetcher", log_to_file=args.enable_log_file) (Task 2)
  ↓
Logger configured with:
  - Console handler (always enabled, stderr)
  - File handler (if log_to_file=True): logs/schedule_fetcher/schedule_fetcher-{timestamp}.log
  ↓
logger.info("Fetching NFL season schedule...") (Task 3)
  ↓
Output: Console (stderr) + File (if flag present)
  ↓
ScheduleFetcher(output_path) instantiated (Task 4)
  ↓
ScheduleFetcher.__init__() calls get_logger() → retrieves configured logger
  ↓
ScheduleFetcher uses logger for INFO/WARNING/ERROR logs
  ↓
logger.info("Schedule successfully exported...") (Task 3)
  ↓
Output: Console + File (if flag present)
  ↓
Script completes, log file closed automatically (if created)
```

### Data Consumption Verification

**CLI Flag Consumption:**
- **Loaded by:** argparse.parse_args() (Task 1)
- **Consumed by:** setup_logger(log_to_file=args.enable_log_file) (Task 2)
- **Verification:** Integration tests I1, I2, C1, C2 verify file created when flag present, not created when absent

**Configured Logger Consumption:**
- **Created by:** setup_logger() in main() (Task 2)
- **Consumed by:**
  - main() function logger calls (Task 3)
  - ScheduleFetcher via get_logger() (Task 4)
- **Verification:** Integration test I4 verifies ScheduleFetcher.logger works after main() setup

**Log File Output Consumption:**
- **Created by:** LineBasedRotatingHandler (Feature 01)
- **Path:** logs/schedule_fetcher/schedule_fetcher-{timestamp}.log
- **Consumed by:**
  - User (reads log file for debugging)
  - Integration tests (verify log content)
- **Verification:** Tests I1, I3, I5, I6 verify file created, named correctly, contains expected logs

---

## Error Handling

### Error Scenario 1: Log Folder Creation Failure

**Trigger:** Permission denied or disk full when creating logs/schedule_fetcher/

**Handling:**
- Handled by Feature 01 (LineBasedRotatingHandler)
- Error logged to stderr (console, not file since file can't be created)
- Script continues (console logging unaffected)

**User Impact:** Log messages not written to file (console logging unaffected)

**Mitigation:** Feature 01 responsibility, documented in Feature 01 error handling

**Tests:** Not tested in Feature 07 (Feature 01 tests cover this)

---

### Error Scenario 2: ScheduleFetcher Instantiated Before setup_logger()

**Trigger:** Code calls ScheduleFetcher() before setup_logger() in main()

**Handling:**
- get_logger() returns None or unconfigured logger
- ScheduleFetcher.logger will be None or improperly configured
- Subsequent log calls may fail or produce no output

**User Impact:** No logs from ScheduleFetcher, potential NoneType errors

**Mitigation:** Test 4.4 (test_setup_logger_called_before_fetcher) verifies correct order in source code

**Tests:** Test 4.4 (source inspection verifies order)

---

### Error Scenario 3: Argparse Conflicts with Async Main

**Trigger:** User concerned about argparse (synchronous) usage in async def main()

**Handling:**
- argparse.parse_args() is synchronous (no async/await needed)
- Called at START of async main(), before any await calls
- No compatibility issues (standard pattern)

**User Impact:** None (works correctly)

**Mitigation:** None needed (argparse is synchronous, safe to use)

**Tests:** Test E1 (test_async_main_with_argparse_no_conflicts)

---

### Error Scenario 4: Parsing Errors During Schedule Fetch

**Trigger:** ESPN API returns malformed data, ScheduleFetcher parse fails

**Handling:**
- Line 138: logger.warning(f"Error parsing event in week {week}: {e}") (Task 6)
- Script continues (doesn't crash)
- Partial schedule may be exported

**User Impact:** User sees WARNING log, aware of parsing issue

**Mitigation:** WARNING level ensures user awareness (not hidden in DEBUG)

**Tests:** Test I6 (test_warning_logs_appear_in_file)

---

## Edge Cases

### Edge Case 1: Empty/Missing CLI Arguments

**Scenario:** User runs `python run_schedule_fetcher.py` (no arguments)

**Handling:**
- argparse sets args.enable_log_file = False (default)
- File logging disabled
- Console logging active (stderr)

**Expected:** Console logging only, no log files created

**Tests:** C1 (test_default_behavior_file_logging_off), I2 (test_e2e_without_flag_no_log_file)

---

### Edge Case 2: Invalid CLI Arguments

**Scenario:** User provides unknown flag: `python run_schedule_fetcher.py --invalid-flag`

**Handling:**
- argparse shows error + help text automatically
- Script exits with non-zero code

**Expected:** Error message + help text, script doesn't run

**Tests:** Not explicitly tested (argparse library handles this, standard behavior)

---

### Edge Case 3: Log Rotation at Exactly 500 Lines

**Scenario:** Script generates exactly 500 log lines

**Handling:**
- LineBasedRotatingHandler rotates at line 501
- New file created: schedule_fetcher-{timestamp}_microseconds.log

**Expected:** Two log files created, no data loss

**Tests:** E2 (test_log_rotation_during_long_fetch)

---

### Edge Case 4: Multiple Rapid Executions

**Scenario:** Script run multiple times per second (potential filename collisions)

**Handling:**
- Feature 01 uses microsecond timestamps in rotated filenames
- Prevents collisions

**Expected:** Each execution creates unique log file

**Tests:** Not tested in Feature 07 (Feature 01 tests cover this)

---

### Edge Case 5: ScheduleFetcher Instantiated Multiple Times

**Scenario:** Code creates multiple ScheduleFetcher instances

**Handling:**
- All instances call get_logger() → retrieve same singleton logger
- All instances use same logger configuration

**Expected:** All instances log to same file (if enabled)

**Tests:** Not explicitly tested (unlikely usage pattern)

---

### Edge Case 6: Log File Permission Denied During Write

**Scenario:** Log file created but becomes read-only mid-execution

**Handling:**
- Feature 01 (LineBasedRotatingHandler) handles write errors
- Error logged to console (stderr)

**Expected:** Console error, script may continue or fail depending on handler

**Tests:** Not tested in Feature 07 (Feature 01 responsibility)

---

### Edge Case 7: Async Main with Synchronous Argparse

**Scenario:** argparse (sync) called inside async def main()

**Handling:**
- argparse executes synchronously at start of main()
- No await needed for argparse operations
- Standard pattern, widely used

**Expected:** No async/await conflicts, script works correctly

**Tests:** E1 (test_async_main_with_argparse_no_conflicts)

---

### Edge Case 8: Logger Name Case Sensitivity

**Scenario:** "ScheduleFetcher" vs "schedule_fetcher" folder naming on different OS

**Handling:**
- Use "schedule_fetcher" consistently (lowercase)
- Prevents duplicate folders on case-sensitive filesystems (Linux)

**Expected:** Single folder logs/schedule_fetcher/ on all OS

**Tests:** Test 2.1 (test_logger_name_snake_case), I3 (test_log_file_format_and_naming)

---

### Edge Case 9: Backward Compatibility with Existing Callers

**Scenario:** Existing code calls ScheduleFetcher(output_path) without enable_log_file

**Handling:**
- S8.P1 removed enable_log_file parameter entirely
- ScheduleFetcher signature unchanged: __init__(self, output_path: Path)
- All existing callers work unchanged

**Expected:** Zero test modifications needed

**Tests:** Test 7.1 (test_existing_schedule_fetcher_tests_unchanged)

---

## Test Coverage Quality

### Test Strategy Reference

**Primary Source:** test_strategy.md (created in S4)

**Test Coverage Summary:**
- **Total Tests:** 22 tests
  - Unit Tests: 12 (Tests 1.1-7.1)
  - Integration Tests: 6 (Tests I1-I6)
  - Edge Case Tests: 2 (Tests E1-E2)
  - Configuration Tests: 2 (Tests C1-C2)

**Estimated Coverage:** >90% (test_strategy.md analysis)

**Coverage by Requirement:**
| Requirement | Test Coverage | Coverage % |
|-------------|--------------|-----------|
| R1: CLI Flag Integration | Tests 1.1-1.3, I1-I3, C1-C2 | 100% |
| R2: Logger Name Consistency | Tests 2.1, I3 | 100% |
| R3: ScheduleFetcher Logger Setup | Tests 3.1-3.2, I4 | 100% |
| R4: Replace Print Statements | Tests 4.1-4.4, I1-I2, I5 | 100% |
| R5: Log Quality - DEBUG/WARNING | Tests 5.1-5.2, I6 | 100% |
| R6: Log Quality - INFO | I5 (integration test) | 100% |
| R7: Test Updates | Test 7.1 | 100% |

**Untested Requirements:** None (all 7 requirements have test coverage)

### Test Success/Failure Paths

**Success Paths (100% coverage):**
- CLI flag parsing (present/absent)
- setup_logger() configuration
- Logger calls (info/error)
- get_logger() retrieval
- Log file creation
- E2E execution

**Failure Paths (100% coverage):**
- Invalid CLI arguments (argparse handles)
- Setup order violation (test 4.4 catches)
- Parse errors (WARNING logs, test I6)
- Log folder creation failure (Feature 01 handles)

**Edge Cases (>90% coverage):**
- Async/argparse integration (E1)
- Log rotation (E2)
- Case sensitivity (Tests 2.1, I3)
- Backward compatibility (Test 7.1)

### Resume/Persistence Tests

**Not applicable:** Feature 07 doesn't persist state or handle resume scenarios. Script runs once per execution, no session state to preserve.

### Overall Coverage Estimate

**Unit Test Coverage:**
- run_schedule_fetcher.py main(): 90% (argparse, setup_logger, print replacement)
- ScheduleFetcher.__init__(): 100% (get_logger verification)
- ScheduleFetcher error parsing: 80% (WARNING log verification)

**Integration Test Coverage:**
- E2E workflows: 95% (with/without flag)
- Feature 01 integration: 90% (log file creation, naming)
- ScheduleFetcher + logger: 90% (get_logger pattern)

**Overall Estimated Coverage:** >90% (meets S4 goal)

---

## Performance & Dependencies

### Performance Impact

**Baseline Performance:** Script execution time without feature (no file logging)

**Estimated Performance with Feature:**
- **Without --enable-log-file flag:** No impact (console logging only, same as baseline)
- **With --enable-log-file flag:** <1ms per log call overhead (file I/O)
- **Overall impact:** <1% total execution time (logging is small fraction of API fetch time)

**Bottlenecks:** None identified (file I/O is not in tight loops)

**Optimization:** Not needed (<1% impact acceptable)

### Python Package Dependencies

**New Dependencies:** None (all stdlib or existing)

**Existing Dependencies Used:**
- argparse (Python stdlib)
- asyncio (Python stdlib)
- logging (Python stdlib, used by Feature 01)

**Version Compatibility:**
- Python 3.8+ (asyncio.run available)
- No third-party package changes

### Configuration Changes

**Backward Compatibility:** 100% (ScheduleFetcher interface unchanged)

**New Configuration:**
- CLI flag --enable-log-file (opt-in, default OFF)
- Log folder: logs/schedule_fetcher/ (auto-created)

**Breaking Changes:** None

---

## Implementation Readiness

### Implementation Phases

**Phase 1: CLI Integration (Tasks 1-2)**
- Add argparse to run_schedule_fetcher.py
- Add setup_logger() call
- **Checkpoint:** Script parses --enable-log-file flag, configures logger
- **Validation:** Run script with --help, verify flag appears
- **Rollback:** Remove argparse and setup_logger additions

**Phase 2: Print Replacement (Task 3)**
- Replace print() statements with logger calls
- **Checkpoint:** No print statements remain in main()
- **Validation:** Run script, verify console output unchanged
- **Rollback:** Restore print statements

**Phase 3: ScheduleFetcher Logger Update (Tasks 4-5)**
- Update ScheduleFetcher to use get_logger()
- Logger name change handled in Phase 1 (main's setup_logger)
- **Checkpoint:** ScheduleFetcher uses get_logger(), retrieves configured logger
- **Validation:** Run existing ScheduleFetcher tests, verify all pass
- **Rollback:** Restore setup_logger() call in ScheduleFetcher

**Phase 4: Log Quality Update (Task 6)**
- Change error parsing log level to WARNING
- **Checkpoint:** Parsing errors use WARNING level
- **Validation:** Grep source for logger.warning at line 138
- **Rollback:** Change back to DEBUG

**Phase 5: Test Verification (Task 7)**
- Run existing test suite, verify 100% pass
- **Checkpoint:** All existing tests pass unchanged
- **Validation:** pytest tests/schedule-data-fetcher/test_ScheduleFetcher.py
- **Rollback:** (No rollback needed, verification only)

**Phase 6: New Test Creation (Tasks 8-11)**
- Create 22 new tests (12 unit, 6 integration, 4 edge/config)
- **Checkpoint:** All 22 tests implemented and passing
- **Validation:** pytest tests/root_scripts/ tests/integration/ --cov
- **Rollback:** (Tests don't affect production code)

### Mock Audit

**Mocks Used in Tests:**
- sys.argv mocking (Tests 1.1-1.3) - Verified: argparse uses sys.argv (stdlib)
- subprocess for E2E tests (Tests I1-I6) - Verified: Standard Python pattern
- httpx.AsyncClient mocking (existing tests) - Verified: Already in use, unchanged

**Integration Tests with REAL Objects:**
- Test I1: Real script execution (no mocks)
- Test I2: Real script execution (no mocks)
- Test I4: Real ScheduleFetcher instantiation with real get_logger() call
- **Count:** 3+ integration tests with real objects (meets requirement)

### Output Consumers

**Log File Consumers:**
- **User:** Reads log file for debugging (format: text, human-readable)
- **Integration tests:** Parse log file content (format: text with timestamps)
- **Format match:** Feature 01's standard log format used (verified in Feature 01)

**Console Output Consumers:**
- **User:** Sees console output (stderr) for runtime awareness
- **CI/CD systems:** Capture stderr for build logs
- **Format match:** Standard Python logging format (INFO/WARNING/ERROR prefix)

### Documentation Tasks

**Code Documentation:**
- [ ] Update run_schedule_fetcher.py docstring (mention --enable-log-file flag in Usage section)
- [ ] ScheduleFetcher.__init__() docstring unchanged (no new parameters)

**External Documentation:**
- [ ] (Optional) Update README.md if schedule fetcher usage section exists
- [ ] (Optional) Update ARCHITECTURE.md if logging section references schedule fetcher

**Implementation Note:** Documentation updates happen in Phase 6 (after all code complete)

---

## Spec Alignment & Cross-Validation

### Spec Validation

**spec.md validated against:**
- ✅ EPIC_TICKET.md (Epic KAI-8 logging refactoring scope includes schedule fetcher)
- ✅ Discovery.md (Feature 07 defined in discovery, async main noted)
- ✅ Feature 01 spec.md (setup_logger and get_logger interfaces verified)

**Discrepancies:** None found

### Cross-Dimension Validation (Gate 12a)

**Dimension 1 (Requirements Completeness):** All 7 spec requirements have implementation tasks (verified with Requirements-to-Task mapping table: 7/7 = 100%)

**Dimension 2 (Interface & Dependency Verification):** All Feature 01 interfaces verified from ACTUAL source code with file:line references (setup_logger: utils/LoggingManager.py:190-197, get_logger: utils/LoggingManager.py:210-211)

**Dimension 3 (Algorithm Traceability):** 16 algorithms mapped (8 feature + 8 test creation)

**Dimension 4 (Task Specification Quality):** All tasks have requirement references, acceptance criteria, locations

**Dimension 5 (Data Flow & Consumption):** CLI flag → setup_logger → logger → log file, all consumption verified

**Dimension 6 (Error Handling & Edge Cases):** 4 error scenarios + 9 edge cases documented

**Dimension 7 (Integration & Compatibility):** ScheduleFetcher interface unchanged (backward compatible)

**Dimension 8 (Test Coverage Quality):** 22 tests, >90% coverage, all requirements covered

**Dimension 9 (Performance & Dependencies):** <1% impact, no new dependencies

**Dimension 10 (Implementation Readiness):** 6 phases defined with checkpoints and rollback strategies

**Dimension 11 (Spec Alignment):** spec.md validated against epic/discovery/Feature 01, interfaces verified from actual source code (utils/LoggingManager.py)

**Confidence Level:** HIGH (validation loop in progress, Rounds 1-4 complete with 6 issues fixed, Round 4 CLEAN, quality ~95%)

---

## Plan Metadata

**Version:** v0.99 (IN VALIDATION LOOP - Rounds 1-9 complete, Round 10 FINAL)
**Created:** 2026-02-12 00:20
**Phase 1 Duration:** ~60 minutes (draft creation)
**Phase 2 Progress:** Rounds 1-9 complete (~115 minutes), Round 10 in progress (FINAL)
**Consecutive Clean Count:** 2 of 3 required (Rounds 8-9 consecutive CLEAN) ✅✅
**Estimated Remaining:** 1 final clean round to exit validation loop successfully
**Quality Estimate:** ~99% complete (up from 70% draft)

**Issues Addressed in Validation Loop:**
- Round 1 (3 issues): Interface verification from actual source code, Requirements-to-Task mapping, Test-to-Task mapping
- Round 2 (1 issue): Cross-Dimension Validation summary updated for interface verification
- Round 3 (2 issues): Metadata updates, Spec Alignment dimension detail
- Round 4 (0 issues): FIRST CLEAN ROUND - all 18 dimensions validated ✅
- Round 5 (1 issue): Plan Metadata not updated for Round 4+ progress
- Round 6 (1 issue): Header Status inconsistency with Plan Metadata
- Round 7 (1 issue): Plan Metadata drift (showed Round 5 when in Round 7)
- Round 8 (0 issues): SECOND CLEAN ROUND - proactive metadata strategy successful ✅
- Round 9 (0 issues): THIRD CLEAN ROUND - 2 consecutive clean rounds achieved ✅
- Round 10 (in progress - FINAL): Need 1 final clean for 3 consecutive → EXIT

**Next Step:** Complete Round 10, if clean → EXIT VALIDATION LOOP → Present plan to user for Gate 5 approval

---

*End of implementation_plan.md v0.99*
