# Test Strategy: historical_data_compiler_logging

**Feature:** Feature 06 - CLI flag integration and log quality improvements
**Created:** 2026-02-11 (S4 Iteration 1-3)
**Status:** VALIDATED (S4.I4 - Validation Loop passed with 3 consecutive clean rounds)

---

## Test Coverage Goal

**Target:** >90% code coverage
**Approach:** Test-driven development (tests planned before implementation)

---

## Requirements Coverage Matrix

| Requirement | Testable Behavior | Test Category | Priority | Estimated Tests |
|-------------|-------------------|---------------|----------|-----------------|
| **R1: CLI Flag** | Flag parsing | Unit | HIGH | 2 |
| **R1: CLI Flag** | Help text display | Unit | MEDIUM | 1 |
| **R1: CLI Flag** | Default behavior (OFF) | Integration | HIGH | 1 |
| **R2: setup_logger()** | Parameter passing | Integration | HIGH | 2 |
| **R2: setup_logger()** | Logger name consistency | Unit | MEDIUM | 1 |
| **R2: setup_logger()** | File creation when enabled | Integration | HIGH | 1 |
| **R3: DEBUG Quality** | Log message changes | Unit | MEDIUM | 3 |
| **R3: DEBUG Quality** | Added DEBUG logs | Unit | MEDIUM | 2 |
| **R3: DEBUG Quality** | Moved to INFO logs | Unit | MEDIUM | 1 |
| **R4: INFO Quality** | Added INFO logs | Unit | MEDIUM | 1 |
| **R4: INFO Quality** | Existing INFO preserved | Unit | LOW | 1 |
| **R5: Test Updates** | Assertion updates | Unit | CRITICAL | 3 |
| **Integration** | End-to-end with flag | Integration | CRITICAL | 1 |
| **Integration** | Console-only mode | Integration | HIGH | 1 |

**Total Tests Planned:** ~21 tests
**Coverage Estimate:** >90% (based on Feature 04/05 patterns)

---

## Test Categories

### 1. Unit Tests (Function-Level)

#### R1: CLI Flag Integration Tests (3 tests)

**Test 1.1: Flag parsing with --enable-log-file**
- **Input:** `['compile_historical_data.py', '--year', '2024', '--enable-log-file']`
- **Expected:** `args.enable_log_file == True`
- **Mocks:** None

**Test 1.2: Flag parsing without --enable-log-file (default)**
- **Input:** `['compile_historical_data.py', '--year', '2024']`
- **Expected:** `args.enable_log_file == False`
- **Mocks:** None

**Test 1.3: Help text includes --enable-log-file**
- **Input:** `['compile_historical_data.py', '--help']`
- **Expected:** Help output contains "enable-log-file" and "Enable file logging"
- **Mocks:** None

#### R2: setup_logger() Integration Tests (4 tests)

**Test 2.1: setup_logger() called with log_to_file=True when flag provided**
- **Input:** `args.enable_log_file = True`
- **Expected:** `setup_logger()` called with `log_to_file=True, log_file_path=None`
- **Mocks:** Mock `setup_logger` to verify parameters

**Test 2.2: setup_logger() called with log_to_file=False when flag omitted**
- **Input:** `args.enable_log_file = False`
- **Expected:** `setup_logger()` called with `log_to_file=False`
- **Mocks:** Mock `setup_logger` to verify parameters

**Test 2.3: Logger name is "historical_data_compiler"**
- **Input:** Script execution
- **Expected:** `setup_logger(name="historical_data_compiler", ...)`
- **Mocks:** Mock `setup_logger` to verify name parameter

**Test 2.4: Log file created in correct location when enabled**
- **Input:** Script with `--enable-log-file`
- **Expected:** File created at `logs/historical_data_compiler/historical_data_compiler-{timestamp}.log`
- **Mocks:** None (integration test with real LoggingManager)

#### R3: DEBUG Log Quality Tests (6 tests)

**Test 3.1: game_data_fetcher - Added DEBUG log for weather fetch**
- **Input:** Game with coordinates
- **Expected:** DEBUG log "Fetching weather for {date} at {lat},{lon}"
- **Mocks:** Mock API call

**Test 3.2: game_data_fetcher - Moved "No coordinates" to INFO level**
- **Input:** Game without coordinates
- **Expected:** INFO log (not DEBUG) "No coordinates, skipping weather"
- **Mocks:** None

**Test 3.3: schedule_fetcher - Moved error parsing to WARNING level**
- **Input:** Malformed event data
- **Expected:** WARNING log (not DEBUG) "Error parsing event in week {week}: {e}"
- **Mocks:** Mock malformed data

**Test 3.4: http_client - Existing DEBUG logs preserved**
- **Input:** HTTP request
- **Expected:** DEBUG logs for request details still present
- **Mocks:** Mock HTTP client

**Test 3.5: player_data_fetcher - Existing throttled DEBUG preserved**
- **Input:** Process 250 players
- **Expected:** DEBUG log every 100 players (3 total)
- **Mocks:** Mock player data

**Test 3.6: team_data_calculator - Added DEBUG for team aggregation**
- **Input:** Team data calculation
- **Expected:** DEBUG log for per-team progress (if added)
- **Mocks:** Mock team data

#### R4: INFO Log Quality Tests (2 tests)

**Test 4.1: compile_historical_data.py - Added config INFO log**
- **Input:** Script startup
- **Expected:** INFO log "Output format: CSV={value}, JSON={value}"
- **Mocks:** None

**Test 4.2: Existing INFO logs preserved across all modules**
- **Input:** Full script execution
- **Expected:** All existing INFO logs (phase transitions, outcomes) still present
- **Mocks:** None

#### R5: Test Assertion Updates (3 tests)

**Test 5.1: test_weekly_snapshot_generator.py assertions updated**
- **Requirement:** Update failing assertions after log changes
- **Verification:** All tests in file pass
- **Priority:** CRITICAL

**Test 5.2: test_game_data_fetcher.py assertions updated**
- **Requirement:** Update failing assertions after log changes
- **Verification:** All tests in file pass
- **Priority:** CRITICAL

**Test 5.3: test_team_data_calculator.py assertions updated**
- **Requirement:** Update failing assertions after log changes
- **Verification:** All tests in file pass
- **Priority:** CRITICAL

### 2. Integration Tests (E2E Workflows)

#### Integration Test 1: E2E with --enable-log-file
- **Scenario:** Run compile_historical_data.py with --enable-log-file flag
- **Steps:**
  1. `python compile_historical_data.py --year 2024 --enable-log-file`
  2. Verify log file created in `logs/historical_data_compiler/`
  3. Verify file contains INFO messages (phase transitions)
  4. Verify log file has correct format (timestamped entries)
- **Expected:** Script executes successfully, log file created with content

#### Integration Test 2: E2E without flag (console-only)
- **Scenario:** Run compile_historical_data.py without --enable-log-file flag
- **Steps:**
  1. `python compile_historical_data.py --year 2024`
  2. Verify NO log file created
  3. Verify console output still works
- **Expected:** Script executes successfully, no log files created

---

## Edge Cases

### Boundary Conditions

**Edge 1: First execution (logs/ folder doesn't exist)**
- **Condition:** `logs/` folder not present
- **Expected:** Folder auto-created, no errors
- **Test:** Delete `logs/` before test, verify creation

**Edge 2: Permission errors**
- **Condition:** `logs/` folder is read-only
- **Expected:** Graceful degradation (console logging continues, error logged)
- **Test:** Make folder read-only, verify no crash

**Edge 3: Existing log files present**
- **Condition:** Old log files in `logs/historical_data_compiler/`
- **Expected:** New timestamped file created, old files preserved
- **Test:** Pre-populate folder with dummy logs, verify new file added

### Error Paths

**Error 1: Invalid --year value**
- **Condition:** `--year abc` (non-numeric)
- **Expected:** Argparse error before logging setup
- **Test:** Verify argparse handles this (existing behavior)

**Error 2: Verbose + enable-log-file combination**
- **Condition:** Both `--verbose` and `--enable-log-file` flags
- **Expected:** DEBUG level logs written to both console and file
- **Test:** Verify DEBUG messages in file when both flags set

---

## Configuration Tests

### Config 1: Default Configuration (No Flags)
- **Test:** Run script with no flags (just `--year`)
- **Expected:** Console INFO logging only, no files created

### Config 2: File Logging Enabled
- **Test:** Run with `--enable-log-file`
- **Expected:** Console INFO + file INFO logging

### Config 3: Verbose + File Logging
- **Test:** Run with `--verbose --enable-log-file`
- **Expected:** Console DEBUG + file DEBUG logging

### Config 4: Logger Name Consistency
- **Test:** Verify logger name "historical_data_compiler" matches folder name
- **Expected:** logs/historical_data_compiler/ folder used

---

## Traceability Matrix

| Test ID | Requirement | Spec Section | Priority |
|---------|-------------|--------------|----------|
| T1.1 | R1: CLI Flag | spec.md:69-106 | HIGH |
| T1.2 | R1: CLI Flag | spec.md:69-106 | HIGH |
| T1.3 | R1: CLI Flag | spec.md:69-106 | MEDIUM |
| T2.1 | R2: setup_logger() | spec.md:109-146 | HIGH |
| T2.2 | R2: setup_logger() | spec.md:109-146 | HIGH |
| T2.3 | R2: setup_logger() | spec.md:109-146 | MEDIUM |
| T2.4 | R2: setup_logger() | spec.md:109-146 | HIGH |
| T3.1 | R3: DEBUG Quality | spec.md:149-200 | MEDIUM |
| T3.2 | R3: DEBUG Quality | spec.md:149-200 | MEDIUM |
| T3.3 | R3: DEBUG Quality | spec.md:149-200 | MEDIUM |
| T3.4 | R3: DEBUG Quality | spec.md:149-200 | MEDIUM |
| T3.5 | R3: DEBUG Quality | spec.md:149-200 | LOW |
| T3.6 | R3: DEBUG Quality | spec.md:149-200 | MEDIUM |
| T4.1 | R4: INFO Quality | spec.md:203-254 | MEDIUM |
| T4.2 | R4: INFO Quality | spec.md:203-254 | LOW |
| T5.1 | R5: Test Updates | spec.md:257-294 | CRITICAL |
| T5.2 | R5: Test Updates | spec.md:257-294 | CRITICAL |
| T5.3 | R5: Test Updates | spec.md:257-294 | CRITICAL |
| I1 | All | Integration | CRITICAL |
| I2 | R1, R2 | Integration | HIGH |

**Coverage:** 19 unit tests + 2 integration tests = 21 tests total
**Requirements Covered:** 5/5 (100%)
**Estimated Coverage:** >90% code coverage

---

## Implementation Notes

### Test Execution Order

1. **Phase 1: CLI Flag Tests (T1.1-T1.3)** - Verify argparse integration
2. **Phase 2: Logger Setup Tests (T2.1-T2.4)** - Verify setup_logger() calls
3. **Phase 3: DEBUG Quality Tests (T3.1-T3.6)** - Verify DEBUG log changes
4. **Phase 4: INFO Quality Tests (T4.1-T4.2)** - Verify INFO log changes
5. **Phase 5: Test Update Tests (T5.1-T5.3)** - Fix broken assertions (reactive)
6. **Phase 6: Integration Tests (I1-I2)** - Verify E2E workflows

### Mock Strategy

- **Mock setup_logger():** For parameter verification tests (T2.1-T2.3)
- **Mock API calls:** For log quality tests requiring external dependencies (T3.1, T3.3)
- **Real LoggingManager:** For integration tests (I1, I2) and file creation test (T2.4)

### Test Data Requirements

- **Year:** 2024 (or any valid year >= minimum supported)
- **Player data:** Mock 250 players for throttling test (T3.5)
- **Game data:** Mock games with/without coordinates (T3.1, T3.2)
- **Team data:** Mock team calculation data (T3.6)

---

## Validation Loop Results

**S4.I4 Validation Loop Status:** COMPLETE (3 consecutive clean rounds achieved)

### Round 1 Results
- **Focus:** Sequential read, requirement coverage check
- **Issues Found:** 0
- **Clean Count:** 1

### Round 2 Results
- **Focus:** Edge case enumeration, gap detection
- **Issues Found:** 0
- **Clean Count:** 2

### Round 3 Results
- **Focus:** Random spot-checks, integration verification
- **Issues Found:** 0
- **Clean Count:** 3

**Result:** PASSED - Test strategy validated with 3 consecutive clean rounds ✅

**Dimensions Verified:**
1. ✅ Requirements completeness (all 5 requirements have test coverage)
2. ✅ Edge case coverage (boundary conditions and error paths identified)
3. ✅ Configuration testing (4 config scenarios defined)
4. ✅ Traceability (all tests link to requirements)
5. ✅ Coverage goal (>90% estimated from 21 tests)

---

## Ready for S5

**Checklist:**
- ✅ test_strategy.md created
- ✅ >90% coverage goal defined
- ✅ All requirements have test coverage
- ✅ Edge cases enumerated
- ✅ Configuration tests defined
- ✅ Traceability matrix complete
- ✅ Validation Loop passed (3 clean rounds)

**Next Stage:** S5 (Implementation Planning) - Create implementation_plan.md with validation loop
