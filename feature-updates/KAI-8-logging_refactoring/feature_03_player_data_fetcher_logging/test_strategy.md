# Test Strategy: player_data_fetcher_logging

**Feature:** Feature 03 - player_data_fetcher_logging
**Part of Epic:** KAI-8-logging_refactoring
**Created:** 2026-02-08
**Last Updated:** 2026-02-08 (S4.I4 COMPLETE - Validation Loop Passed)
**Status:** ✅ VALIDATED (Validation Loop passed with 3 consecutive clean rounds, ZERO issues found)

---

## Test Strategy Overview

**Testing Approach:** Test-driven development with >90% coverage goal

**Test Categories:**
1. **Unit Tests** - Function-level testing with mocked dependencies
2. **Integration Tests** - Component-level testing with real dependencies
3. **Edge Case Tests** - Boundary conditions and error paths
4. **Config Tests** - Configuration scenarios (default, custom, invalid, missing)

**Coverage Goal:** >90% code coverage across all modified/added code

---

## Requirements Coverage Analysis

### Requirement R1: Subprocess Wrapper CLI Flag Integration

**Testable Behaviors:**
- Accepts `--enable-log-file` flag via argparse
- Forwards all CLI arguments to player_data_fetcher_main.py using sys.argv[1:]
- Provides help text via --help
- Backward compatible (works without flag)
- Forwards unknown arguments without error

**Expected Inputs:**
- CLI arguments: --enable-log-file, --help, future flags

**Expected Outputs:**
- Subprocess call with sys.argv[1:] forwarded
- Exit code from subprocess
- Help text displayed

**Error Conditions:**
- Subprocess fails (non-zero exit code)
- Invalid arguments (handled by subprocess, not wrapper)

**Edge Cases:**
- No arguments provided
- Multiple flags provided
- Unknown flags provided

---

### Requirement R2: Main Script CLI Flag Integration

**Testable Behaviors:**
- Accepts `--enable-log-file` flag via argparse
- Wires flag to setup_logger() log_to_file parameter
- Creates logs/player_data_fetcher/ folder when flag used
- Uses logger name "player_data_fetcher"
- Removes LOGGING_TO_FILE config constant dependency

**Expected Inputs:**
- CLI flag: --enable-log-file (optional, boolean)

**Expected Outputs:**
- Logger configured with log_to_file=True when flag present
- Logger configured with log_to_file=False when flag absent
- Log file created in logs/player_data_fetcher/ when flag present

**Error Conditions:**
- Invalid flag value (argparse handles this)
- Log directory creation fails (handled by Feature 01)

**Edge Cases:**
- Script run without any flags
- Script run with --enable-log-file multiple times
- Script run with --help

---

### Requirement R3: Log Quality Improvements - DEBUG Level

**Testable Behaviors:**
- Function entry/exit for complex flows (API calls, data processing)
- Data transformation logs show before/after values
- Conditional branch logs indicate path taken
- No excessive logging (variable assignments, tight loops)

**Expected Inputs:**
- Various execution paths (cache hit, cache miss, API success, API failure)

**Expected Outputs:**
- DEBUG logs for function entry/exit
- DEBUG logs for data transformations
- DEBUG logs for conditional branches
- No DEBUG logs for variable assignments or tight loops

**Error Conditions:**
- N/A (log quality, not error handling)

**Edge Cases:**
- API rate limiting triggers
- Cache behavior changes
- Different data transformation paths

---

### Requirement R4: Log Quality Improvements - INFO Level

**Testable Behaviors:**
- Script start log includes configuration
- Major phase transitions logged
- Significant outcomes logged
- No implementation details at INFO level

**Expected Inputs:**
- Script execution phases (start, collect, export, complete)

**Expected Outputs:**
- INFO log for script start with config
- INFO logs for major phase transitions
- INFO logs for significant outcomes
- No INFO logs for implementation details

**Error Conditions:**
- N/A (log quality, not error handling)

**Edge Cases:**
- Different configuration settings
- Different output formats
- Different data volumes

---

### Requirement R5: Config.py Constants Removal

**Testable Behaviors:**
- LOGGING_TO_FILE constant not present in config.py
- LOGGING_FILE constant not present in config.py
- Tests don't reference removed constants
- CLI flag controls file logging behavior

**Expected Inputs:**
- Import of config.py

**Expected Outputs:**
- AttributeError when attempting to access removed constants
- CLI flag is sole control for file logging

**Error Conditions:**
- Code attempts to access removed constants (should fail)

**Edge Cases:**
- Legacy code references removed constants
- Tests reference removed constants

---

## Test Coverage Matrix (Draft)

| Requirement | Testable Behavior | Test Type | Priority | Estimated Tests |
|-------------|-------------------|-----------|----------|-----------------|
| R1: Subprocess Wrapper | Accept CLI flag | Unit | HIGH | 3 |
| R1: Subprocess Wrapper | Forward arguments | Integration | HIGH | 4 |
| R1: Subprocess Wrapper | Help text | Integration | MEDIUM | 2 |
| R2: Main Script CLI | Accept CLI flag | Unit | HIGH | 3 |
| R2: Main Script CLI | Wire to setup_logger | Integration | HIGH | 4 |
| R2: Main Script CLI | Logger configuration | Integration | HIGH | 3 |
| R3: DEBUG Log Quality | Function entry/exit | Integration | MEDIUM | 3 |
| R3: DEBUG Log Quality | Data transformations | Integration | MEDIUM | 2 |
| R3: DEBUG Log Quality | Conditional branches | Integration | MEDIUM | 2 |
| R4: INFO Log Quality | Script lifecycle | Integration | HIGH | 4 |
| R4: INFO Log Quality | Phase transitions | Integration | MEDIUM | 3 |
| R5: Config Constants | Constants removed | Unit | HIGH | 2 |

**Coverage Estimate:** 35 tests planned (before edge cases and config tests)
**Coverage Goal:** >90% code coverage

---

## Test Case List

### Requirement R1: Subprocess Wrapper CLI Flag Integration

#### Unit Tests

**Test 1.1: test_wrapper_accepts_enable_log_file_flag**
- **Purpose:** Verify wrapper accepts --enable-log-file flag
- **Setup:** Mock subprocess.run
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** argparse parses flag successfully, subprocess called
- **Links to:** R1 (CLI flag acceptance)

**Test 1.2: test_wrapper_help_text_available**
- **Purpose:** Verify --help displays flag documentation
- **Setup:** Mock subprocess.run
- **Input:** CLI args: ['--help']
- **Expected:** Help text displayed with --enable-log-file description
- **Links to:** R1 (Help text)

**Test 1.3: test_wrapper_backward_compatible**
- **Purpose:** Verify wrapper works without flag
- **Setup:** Mock subprocess.run
- **Input:** CLI args: [] (no arguments)
- **Expected:** Subprocess called with no extra arguments
- **Links to:** R1 (Backward compatibility)

#### Integration Tests

**Test 1.4: test_wrapper_forwards_sys_argv**
- **Purpose:** Verify sys.argv[1:] forwarded to subprocess
- **Setup:** Mock subprocess.run
- **Input:** CLI args: ['--enable-log-file', '--future-flag', 'value']
- **Expected:** subprocess.run called with all arguments forwarded
- **Links to:** R1 (Argument forwarding)

**Test 1.5: test_wrapper_subprocess_success**
- **Purpose:** Verify wrapper returns 0 on subprocess success
- **Setup:** Mock subprocess.run to return 0
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** Function returns 0 (success)
- **Links to:** R1 (Subprocess integration)

**Test 1.6: test_wrapper_subprocess_failure**
- **Purpose:** Verify wrapper propagates subprocess failure
- **Setup:** Mock subprocess.run to raise CalledProcessError
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** Exception propagated to caller
- **Links to:** R1 (Error handling)

**Test 1.7: test_wrapper_calls_correct_script**
- **Purpose:** Verify wrapper calls player_data_fetcher_main.py
- **Setup:** Mock subprocess.run
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** subprocess.run called with correct script path
- **Links to:** R1 (Script targeting)

---

### Requirement R2: Main Script CLI Flag Integration

#### Unit Tests

**Test 2.1: test_main_accepts_enable_log_file_flag**
- **Purpose:** Verify main script accepts --enable-log-file flag
- **Setup:** Mock setup_logger, mock all collectors
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** argparse parses flag, args.enable_log_file = True
- **Links to:** R2 (CLI flag acceptance)

**Test 2.2: test_main_flag_default_false**
- **Purpose:** Verify flag defaults to False when not provided
- **Setup:** Mock setup_logger, mock all collectors
- **Input:** CLI args: [] (no arguments)
- **Expected:** args.enable_log_file = False
- **Links to:** R2 (Default behavior)

**Test 2.3: test_main_help_text_available**
- **Purpose:** Verify --help displays flag documentation
- **Setup:** None (argparse built-in)
- **Input:** CLI args: ['--help']
- **Expected:** Help text displayed with --enable-log-file description
- **Links to:** R2 (Help text)

#### Integration Tests

**Test 2.4: test_main_wires_flag_to_setup_logger**
- **Purpose:** Verify flag value passed to setup_logger()
- **Setup:** Mock setup_logger, capture call arguments
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** setup_logger called with log_to_file=True
- **Links to:** R2 (setup_logger integration)

**Test 2.5: test_main_logger_name_correct**
- **Purpose:** Verify logger name is "player_data_fetcher"
- **Setup:** Mock setup_logger, capture call arguments
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** setup_logger called with name="player_data_fetcher"
- **Links to:** R2 (Logger name)

**Test 2.6: test_main_log_file_path_none**
- **Purpose:** Verify log_file_path=None (auto-generated)
- **Setup:** Mock setup_logger, capture call arguments
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** setup_logger called with log_file_path=None
- **Links to:** R2 (Auto-generated path)

**Test 2.7: test_main_creates_log_folder**
- **Purpose:** Verify logs/player_data_fetcher/ folder created
- **Setup:** Real setup_logger (no mock), filesystem check
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** logs/player_data_fetcher/ directory exists after execution
- **Links to:** R2 (Log folder creation)

---

### Requirement R3: DEBUG Log Quality Improvements

#### Integration Tests

**Test 3.1: test_debug_logs_function_entry_exit**
- **Purpose:** Verify complex functions log entry/exit
- **Setup:** Enable DEBUG logging, run API call flow
- **Input:** API call to fetch projections
- **Expected:** DEBUG logs for function entry/exit present
- **Links to:** R3 (Function tracing)

**Test 3.2: test_debug_logs_data_transformation**
- **Purpose:** Verify data transformations logged with before/after
- **Setup:** Enable DEBUG logging, run data export
- **Input:** Export player data to JSON
- **Expected:** DEBUG logs show before/after values
- **Links to:** R3 (Data transformations)

**Test 3.3: test_debug_logs_conditional_branches**
- **Purpose:** Verify conditional paths logged
- **Setup:** Enable DEBUG logging, trigger cache hit/miss
- **Input:** Cached vs uncached data requests
- **Expected:** DEBUG logs indicate which branch taken
- **Links to:** R3 (Conditional branches)

**Test 3.4: test_debug_no_variable_assignments**
- **Purpose:** Verify no excessive variable assignment logs
- **Setup:** Enable DEBUG logging, run full workflow
- **Input:** Complete data collection
- **Expected:** No logs like "player_name = X" for every variable
- **Links to:** R3 (Remove excessive logs)

**Test 3.5: test_debug_no_tight_loop_logs**
- **Purpose:** Verify no per-iteration logs in tight loops
- **Setup:** Enable DEBUG logging, process 100+ players
- **Input:** Player data for 100 players
- **Expected:** No DEBUG log per player iteration
- **Links to:** R3 (Remove excessive logs)

---

### Requirement R4: INFO Log Quality Improvements

#### Integration Tests

**Test 4.1: test_info_logs_script_start**
- **Purpose:** Verify script start logged with configuration
- **Setup:** Enable INFO logging, run script
- **Input:** Script execution with specific config
- **Expected:** INFO log shows script start with config details
- **Links to:** R4 (Script lifecycle)

**Test 4.2: test_info_logs_major_phases**
- **Purpose:** Verify major phase transitions logged
- **Setup:** Enable INFO logging, run full workflow
- **Input:** Complete data collection and export
- **Expected:** INFO logs for "Collecting season projections", "Exporting data"
- **Links to:** R4 (Phase transitions)

**Test 4.3: test_info_logs_significant_outcomes**
- **Purpose:** Verify significant outcomes logged
- **Setup:** Enable INFO logging, run data collection
- **Input:** Collect 150 players
- **Expected:** INFO log shows "Collected 150 players"
- **Links to:** R4 (Significant outcomes)

**Test 4.4: test_info_no_implementation_details**
- **Purpose:** Verify no implementation details at INFO level
- **Setup:** Enable INFO logging, run full workflow
- **Input:** Complete data collection
- **Expected:** No INFO logs like "Calling _get_api_client()"
- **Links to:** R4 (Remove implementation details)

---

### Requirement R5: Config.py Constants Removal

#### Unit Tests

**Test 5.1: test_config_logging_to_file_removed**
- **Purpose:** Verify LOGGING_TO_FILE constant doesn't exist
- **Setup:** Import config module
- **Input:** Attempt to access config.LOGGING_TO_FILE
- **Expected:** AttributeError raised
- **Links to:** R5 (Constants removal)

**Test 5.2: test_config_logging_file_removed**
- **Purpose:** Verify LOGGING_FILE constant doesn't exist
- **Setup:** Import config module
- **Input:** Attempt to access config.LOGGING_FILE
- **Expected:** AttributeError raised
- **Links to:** R5 (Constants removal)

---

## Traceability Matrix

| Requirement | Test Cases | Coverage |
|-------------|------------|----------|
| R1: Subprocess Wrapper | Tests 1.1-1.7 | 100% |
| R2: Main Script CLI | Tests 2.1-2.7 | 100% |
| R3: DEBUG Log Quality | Tests 3.1-3.5 | 100% |
| R4: INFO Log Quality | Tests 4.1-4.4 | 100% |
| R5: Config Constants | Tests 5.1-5.2 | 100% |

**Total Tests Planned:** 25 tests (before edge cases and config tests)
**Requirements with <90% Coverage:** 0 (target met)

---

## Test Summary (After S4.I1)

**Test Breakdown:**
- Unit tests: 8 (32%)
- Integration tests: 17 (68%)
- Edge case tests: 0 (to be added in S4.I2)
- Config tests: 0 (to be added in S4.I3)

**Total Tests:** 25
**Coverage:** Estimated >80% (will exceed 90% after edge cases and config tests)
**Next:** S4.I2 (Edge Case Enumeration)

---

---

## Edge Case Catalog (Added in S4.I2)

### Boundary Conditions Analysis

#### Input 1: CLI Arguments (strings)

**Boundary Values:**
- Empty arguments list: [] → Valid (default behavior)
- Single flag: ['--enable-log-file'] → Valid
- Multiple flags: ['--enable-log-file', '--future-flag'] → Valid (forwarded)
- Invalid flag format: ['--enable-log-file=true'] → May cause argparse error
- Very long flag: ['--' + 'x'*255] → Should handle gracefully

**Expected Behavior:**
- Empty → Default behavior (no file logging)
- Single flag → Enable file logging
- Multiple flags → Forward all arguments
- Invalid format → argparse error with helpful message

#### Input 2: Subprocess Exit Code (integer)

**Boundary Values:**
- Zero: 0 → Success
- Non-zero: 1-255 → Failure codes
- Negative: -N → Signal termination (Unix)

**Expected Behavior:**
- 0 → Wrapper returns 0 (success)
- Non-zero → Wrapper propagates error (CalledProcessError)
- Negative → Wrapper handles signal termination

#### Input 3: Log File Path (filesystem)

**Boundary Values:**
- Path doesn't exist: logs/player_data_fetcher/ not created yet → Feature 01 creates
- Path exists: logs/player_data_fetcher/ already exists → Reuse directory
- Insufficient permissions: Read-only filesystem → Error from Feature 01
- Disk full: No space for log file → Error from Feature 01

**Expected Behavior:**
- Not exist → Feature 01 creates directory
- Exists → Reuse directory
- No permissions → Feature 01 raises PermissionError
- Disk full → Feature 01 raises OSError

---

### Error Paths Identified

**Error Path 1: Subprocess Fails**
- **Trigger:** player_data_fetcher_main.py exits with non-zero code
- **Expected:** Wrapper propagates CalledProcessError
- **Recovery:** User fixes underlying issue, re-runs wrapper
- **Test:** test_wrapper_subprocess_failure (already planned)

**Error Path 2: Subprocess Not Found**
- **Trigger:** player_data_fetcher_main.py not found at expected path
- **Expected:** Wrapper raises FileNotFoundError
- **Recovery:** User verifies file location, fixes path
- **Test:** test_wrapper_script_not_found (new)

**Error Path 3: Invalid Argument Format**
- **Trigger:** User provides malformed argument (e.g., --enable-log-file=yes)
- **Expected:** Main script argparse raises error
- **Recovery:** User corrects argument format
- **Test:** test_main_invalid_arg_format (new)

**Error Path 4: Permission Denied for Log Directory**
- **Trigger:** logs/ directory has no write permissions
- **Expected:** Feature 01 raises PermissionError
- **Recovery:** User fixes permissions
- **Test:** test_main_log_directory_permission_denied (new)

**Error Path 5: Disk Full During Log Write**
- **Trigger:** Disk runs out of space during log file write
- **Expected:** Feature 01 raises OSError
- **Recovery:** User frees disk space
- **Test:** test_main_disk_full_during_logging (new)

**Error Path 6: Import Error (Missing Dependencies)**
- **Trigger:** Required module (e.g., espn_client) not found
- **Expected:** ImportError raised with clear message
- **Recovery:** User installs missing dependencies
- **Test:** test_main_import_error_handling (new)

**Error Path 7: Config File Malformed**
- **Trigger:** config.py has syntax errors
- **Expected:** SyntaxError raised during import
- **Recovery:** User fixes config.py syntax
- **Test:** test_main_malformed_config_handling (new)

**Error Path 8: API Timeout**
- **Trigger:** ESPN API doesn't respond within timeout
- **Expected:** TimeoutError raised, logged appropriately
- **Recovery:** User retries or increases timeout
- **Test:** test_api_timeout_handling (new)

**Error Path 9: API Rate Limit Exceeded**
- **Trigger:** ESPN API returns 429 (Too Many Requests)
- **Expected:** Retry with exponential backoff, log rate limit
- **Recovery:** Automatic retry after delay
- **Test:** test_api_rate_limit_handling (new)

**Error Path 10: API Invalid Response**
- **Trigger:** ESPN API returns non-JSON or malformed JSON
- **Expected:** ParsingError raised, logged with details
- **Recovery:** User retries or reports API issue
- **Test:** test_api_invalid_response_handling (new)

---

### Edge Case Tests (Added in S4.I2)

#### Subprocess Wrapper Edge Cases

**Test 1.8: test_wrapper_script_not_found**
- **Purpose:** Verify error when target script doesn't exist
- **Setup:** Rename or delete player_data_fetcher_main.py
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** FileNotFoundError raised with clear message
- **Links to:** R1 (Error handling)

**Test 1.9: test_wrapper_multiple_flags_forwarded**
- **Purpose:** Verify multiple unknown flags forwarded correctly
- **Setup:** Mock subprocess.run
- **Input:** CLI args: ['--enable-log-file', '--future-flag-1', '--future-flag-2']
- **Expected:** All flags forwarded to subprocess
- **Links to:** R1 (Argument forwarding)

**Test 1.10: test_wrapper_empty_arguments**
- **Purpose:** Verify wrapper works with no arguments
- **Setup:** Mock subprocess.run
- **Input:** CLI args: []
- **Expected:** Subprocess called with no extra arguments
- **Links to:** R1 (Default behavior)

#### Main Script Edge Cases

**Test 2.8: test_main_invalid_arg_format**
- **Purpose:** Verify error on malformed argument
- **Setup:** None (argparse built-in)
- **Input:** CLI args: ['--enable-log-file=true'] (invalid format)
- **Expected:** argparse error with helpful message
- **Links to:** R2 (Input validation)

**Test 2.9: test_main_log_directory_permission_denied**
- **Purpose:** Verify error when log directory has no write permissions
- **Setup:** Mock Feature 01 to raise PermissionError
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** PermissionError propagated with clear message
- **Links to:** R2 (Error handling)

**Test 2.10: test_main_disk_full_during_logging**
- **Purpose:** Verify error when disk runs out of space
- **Setup:** Mock Feature 01 to raise OSError (disk full)
- **Input:** CLI args: ['--enable-log-file']
- **Expected:** OSError propagated with clear message
- **Links to:** R2 (Error handling)

**Test 2.11: test_main_import_error_handling**
- **Purpose:** Verify graceful handling of missing dependencies
- **Setup:** Mock import to raise ImportError
- **Input:** Script execution
- **Expected:** ImportError with clear message indicating missing module
- **Links to:** R2 (Dependency validation)

**Test 2.12: test_main_malformed_config_handling**
- **Purpose:** Verify error on config.py syntax errors
- **Setup:** Create config.py with syntax error
- **Input:** Script execution
- **Expected:** SyntaxError raised during import
- **Links to:** R2 (Config validation)

#### API Integration Edge Cases

**Test 3.6: test_api_timeout_handling**
- **Purpose:** Verify timeout handling for API calls
- **Setup:** Mock espn_client to raise TimeoutError
- **Input:** API call to fetch projections
- **Expected:** TimeoutError raised, DEBUG log shows timeout details
- **Links to:** R3 (Error handling logging)

**Test 3.7: test_api_rate_limit_handling**
- **Purpose:** Verify rate limit handling (429 response)
- **Setup:** Mock espn_client to return 429 on first call, success on retry
- **Input:** API call to fetch projections
- **Expected:** Retry logic triggered, DEBUG log shows rate limit + retry
- **Links to:** R3 (Conditional branch logging)

**Test 3.8: test_api_invalid_response_handling**
- **Purpose:** Verify handling of malformed API responses
- **Setup:** Mock espn_client to return non-JSON response
- **Input:** API call to fetch projections
- **Expected:** ParsingError raised, DEBUG log shows response details
- **Links to:** R3 (Error handling logging)

#### Log Quality Edge Cases

**Test 3.9: test_debug_cache_hit_path**
- **Purpose:** Verify DEBUG log for cache hit path
- **Setup:** Enable DEBUG logging, trigger cache hit
- **Input:** Request cached player data
- **Expected:** DEBUG log shows "Using cached data"
- **Links to:** R3 (Conditional branch logging)

**Test 3.10: test_debug_cache_miss_path**
- **Purpose:** Verify DEBUG log for cache miss path
- **Setup:** Enable DEBUG logging, trigger cache miss
- **Input:** Request uncached player data
- **Expected:** DEBUG log shows "Cache miss, fetching fresh data"
- **Links to:** R3 (Conditional branch logging)

**Test 4.5: test_info_zero_players_collected**
- **Purpose:** Verify INFO log handles zero players case
- **Setup:** Enable INFO logging, mock API to return empty data
- **Input:** API returns no players
- **Expected:** INFO log shows "Collected 0 players" (not error)
- **Links to:** R4 (Edge case logging)

**Test 4.6: test_info_large_dataset**
- **Purpose:** Verify INFO log handles large datasets
- **Setup:** Enable INFO logging, mock API to return 1000+ players
- **Input:** API returns 1000 players
- **Expected:** INFO log shows "Collected 1000 players" (no performance issue)
- **Links to:** R4 (Edge case logging)

---

## Edge Case Catalog Summary

| Edge Case | Category | Expected Behavior | Test Coverage |
|-----------|----------|-------------------|---------------|
| No CLI arguments | Default behavior | Default behavior (no file logging) | Test 1.10 |
| Multiple unknown flags | Argument forwarding | All flags forwarded | Test 1.9 |
| Target script not found | File system | FileNotFoundError | Test 1.8 |
| Invalid argument format | Input validation | argparse error | Test 2.8 |
| Log directory no permissions | File system | PermissionError | Test 2.9 |
| Disk full | File system | OSError | Test 2.10 |
| Missing dependencies | Import | ImportError | Test 2.11 |
| Malformed config | Config validation | SyntaxError | Test 2.12 |
| API timeout | Network | TimeoutError + DEBUG log | Test 3.6 |
| API rate limit (429) | Network | Retry + DEBUG log | Test 3.7 |
| API invalid response | Data validation | ParsingError + DEBUG log | Test 3.8 |
| Cache hit | Conditional logic | DEBUG log "Using cached data" | Test 3.9 |
| Cache miss | Conditional logic | DEBUG log "Cache miss" | Test 3.10 |
| Zero players collected | Edge data | INFO log "0 players" | Test 4.5 |
| Large dataset (1000+) | Edge data | INFO log "1000 players" | Test 4.6 |

**Total Edge Cases Identified:** 15
**Edge Cases Without Tests:** 0

---

## Test Coverage Matrix (Updated After S4.I2)

| Requirement | Unit Tests | Integration Tests | Edge Case Tests | Total Tests |
|-------------|------------|-------------------|-----------------|-------------|
| R1: Subprocess Wrapper | 3 | 4 | 3 | 10 |
| R2: Main Script CLI | 3 | 4 | 5 | 12 |
| R3: DEBUG Log Quality | 0 | 5 | 5 | 10 |
| R4: INFO Log Quality | 0 | 4 | 2 | 6 |
| R5: Config Constants | 2 | 0 | 0 | 2 |

**Total Tests Planned:** 40 tests (was 25 after S4.I1)
**Edge Case Coverage:** 15 edge case tests added
**Coverage Estimate:** >90% (exceeds 90% goal ✅)

---

---

## Configuration Dependencies (Added in S4.I3)

### Config File: player-data-fetcher/config.py

**Values Used by This Feature:**

**1. LOGGING_LEVEL (string)**
- **Purpose:** Sets logger verbosity level (DEBUG, INFO, WARNING, ERROR)
- **Default:** 'INFO'
- **If missing:** setup_logger() may use default from Feature 01
- **If invalid (not valid level):** Raises ValueError from logging module
- **Impact:** Controls which logs are displayed/written

**2. LOG_NAME (string)**
- **Purpose:** Logger name (must match "player_data_fetcher" per Feature 01 contract)
- **Default:** "player_data_fetcher"
- **If missing:** Code uses hardcoded "player_data_fetcher"
- **If invalid (wrong name):** Logs go to wrong folder (logs/{wrong_name}/)
- **Impact:** Determines log folder location

**3. LOGGING_FORMAT (string)**
- **Purpose:** Log format style ('standard', 'detailed', 'simple')
- **Default:** 'standard'
- **If missing:** setup_logger() may use default from Feature 01
- **If invalid (unknown format):** setup_logger() may raise ValueError
- **Impact:** Controls log message formatting

**4. LOGGING_TO_FILE (REMOVED)**
- **Purpose:** DEPRECATED - Replaced by --enable-log-file CLI flag
- **Expected:** Constant should NOT exist (removed in R5)
- **Impact:** If present, indicates incomplete migration

**5. LOGGING_FILE (REMOVED)**
- **Purpose:** DEPRECATED - Replaced by Feature 01 auto-generated paths
- **Expected:** Constant should NOT exist (removed in R5)
- **Impact:** If present, indicates incomplete migration

---

## Configuration Test Cases (Added in S4.I3)

### Config Scenario 1: Default Configuration

**Test 6.1: test_config_default_logging_level**
- **Purpose:** Verify feature works with default LOGGING_LEVEL
- **Setup:** Use default config.py (LOGGING_LEVEL = 'INFO')
- **Input:** Run script with --enable-log-file
- **Expected:** INFO and higher logs written to file, DEBUG logs excluded
- **Links to:** R2 (Logger configuration)

**Test 6.2: test_config_default_log_name**
- **Purpose:** Verify feature uses correct default LOG_NAME
- **Setup:** Use default config.py (LOG_NAME = "player_data_fetcher")
- **Input:** Run script with --enable-log-file
- **Expected:** Logs written to logs/player_data_fetcher/ folder
- **Links to:** R2 (Logger configuration)

**Test 6.3: test_config_default_logging_format**
- **Purpose:** Verify feature works with default LOGGING_FORMAT
- **Setup:** Use default config.py (LOGGING_FORMAT = 'standard')
- **Input:** Run script with --enable-log-file
- **Expected:** Logs formatted with 'standard' format
- **Links to:** R2 (Logger configuration)

---

### Config Scenario 2: Custom Configuration

**Test 6.4: test_config_custom_logging_level_debug**
- **Purpose:** Verify DEBUG level logs all messages
- **Setup:** Set LOGGING_LEVEL = 'DEBUG' in config.py
- **Input:** Run script with --enable-log-file
- **Expected:** DEBUG, INFO, and higher logs written to file
- **Links to:** R2, R3 (DEBUG logging)

**Test 6.5: test_config_custom_logging_level_warning**
- **Purpose:** Verify WARNING level filters INFO/DEBUG
- **Setup:** Set LOGGING_LEVEL = 'WARNING' in config.py
- **Input:** Run script with --enable-log-file
- **Expected:** Only WARNING and higher logs written, INFO/DEBUG excluded
- **Links to:** R2 (Logger configuration)

**Test 6.6: test_config_custom_logging_format_detailed**
- **Purpose:** Verify 'detailed' format includes extra information
- **Setup:** Set LOGGING_FORMAT = 'detailed' in config.py
- **Input:** Run script with --enable-log-file
- **Expected:** Logs formatted with 'detailed' format (more verbose)
- **Links to:** R2 (Logger configuration)

**Test 6.7: test_config_custom_logging_format_simple**
- **Purpose:** Verify 'simple' format reduces verbosity
- **Setup:** Set LOGGING_FORMAT = 'simple' in config.py
- **Input:** Run script with --enable-log-file
- **Expected:** Logs formatted with 'simple' format (less verbose)
- **Links to:** R2 (Logger configuration)

---

### Config Scenario 3: Invalid Configuration

**Test 6.8: test_config_invalid_logging_level**
- **Purpose:** Verify invalid LOGGING_LEVEL raises error
- **Setup:** Set LOGGING_LEVEL = 'INVALID_LEVEL' in config.py
- **Input:** Run script
- **Expected:** ValueError raised with clear message about invalid level
- **Links to:** R2 (Config validation)

**Test 6.9: test_config_invalid_log_name_type**
- **Purpose:** Verify non-string LOG_NAME raises error
- **Setup:** Set LOG_NAME = 12345 (integer, not string) in config.py
- **Input:** Run script
- **Expected:** TypeError raised or logs fail to write
- **Links to:** R2 (Config validation)

**Test 6.10: test_config_invalid_logging_format**
- **Purpose:** Verify invalid LOGGING_FORMAT raises error
- **Setup:** Set LOGGING_FORMAT = 'unknown_format' in config.py
- **Input:** Run script with --enable-log-file
- **Expected:** ValueError raised or defaults to 'standard'
- **Links to:** R2 (Config validation)

---

### Config Scenario 4: Missing Configuration

**Test 6.11: test_config_missing_logging_level**
- **Purpose:** Verify missing LOGGING_LEVEL uses default
- **Setup:** Remove LOGGING_LEVEL from config.py
- **Input:** Run script with --enable-log-file
- **Expected:** Defaults to 'INFO' or Feature 01 default
- **Links to:** R2 (Config handling)

**Test 6.12: test_config_missing_log_name**
- **Purpose:** Verify missing LOG_NAME uses hardcoded value
- **Setup:** Remove LOG_NAME from config.py
- **Input:** Run script with --enable-log-file
- **Expected:** Uses hardcoded "player_data_fetcher" in code
- **Links to:** R2 (Config handling)

**Test 6.13: test_config_missing_logging_format**
- **Purpose:** Verify missing LOGGING_FORMAT uses default
- **Setup:** Remove LOGGING_FORMAT from config.py
- **Input:** Run script with --enable-log-file
- **Expected:** Defaults to 'standard' or Feature 01 default
- **Links to:** R2 (Config handling)

---

### Config Scenario 5: Deprecated Constants

**Test 6.14: test_config_logging_to_file_deprecated**
- **Purpose:** Verify LOGGING_TO_FILE constant doesn't exist
- **Setup:** Import config module
- **Input:** Attempt to access config.LOGGING_TO_FILE
- **Expected:** AttributeError raised (constant removed)
- **Links to:** R5 (Constants removal)

**Test 6.15: test_config_logging_file_deprecated**
- **Purpose:** Verify LOGGING_FILE constant doesn't exist
- **Setup:** Import config module
- **Input:** Attempt to access config.LOGGING_FILE
- **Expected:** AttributeError raised (constant removed)
- **Links to:** R5 (Constants removal)

**Test 6.16: test_cli_flag_overrides_any_legacy_config**
- **Purpose:** Verify CLI flag is sole control (not config)
- **Setup:** Ensure no LOGGING_TO_FILE in config.py
- **Input:** Run with/without --enable-log-file flag
- **Expected:** Flag controls behavior, no config constant used
- **Links to:** R2, R5 (CLI flag priority)

---

## Configuration Test Matrix

| Config Value | Default | Custom | Invalid | Missing | Deprecated | Total Tests |
|--------------|---------|--------|---------|---------|------------|-------------|
| LOGGING_LEVEL | Test 6.1 | Tests 6.4-6.5 | Test 6.8 | Test 6.11 | - | 5 |
| LOG_NAME | Test 6.2 | - | Test 6.9 | Test 6.12 | - | 3 |
| LOGGING_FORMAT | Test 6.3 | Tests 6.6-6.7 | Test 6.10 | Test 6.13 | - | 5 |
| LOGGING_TO_FILE | - | - | - | - | Test 6.14 | 1 |
| LOGGING_FILE | - | - | - | - | Test 6.15 | 1 |
| CLI Flag Priority | - | - | - | - | Test 6.16 | 1 |

**Total Config Tests Planned:** 16 tests
**Config Values Without Tests:** 0
**Scenarios Covered:** Default, Custom, Invalid, Missing, Deprecated

---

## Test Coverage Matrix (Final - After S4.I3)

| Requirement | Unit Tests | Integration Tests | Edge Case Tests | Config Tests | Total Tests |
|-------------|------------|-------------------|-----------------|--------------|-------------|
| R1: Subprocess Wrapper | 3 | 4 | 3 | 0 | 10 |
| R2: Main Script CLI | 3 | 4 | 5 | 13 | 25 |
| R3: DEBUG Log Quality | 0 | 5 | 5 | 2 | 12 |
| R4: INFO Log Quality | 0 | 4 | 2 | 0 | 6 |
| R5: Config Constants | 2 | 0 | 0 | 3 | 5 |

**Total Tests Planned:** 58 tests (was 40 after S4.I2)
**Coverage Estimate:** >95% (exceeds 90% goal ✅)
**Test Categories Complete:** Unit, Integration, Edge Case, Config

---

## Test Summary (After S4.I3)

**Test Breakdown:**
- Unit tests: 8 (14%)
- Integration tests: 17 (29%)
- Edge case tests: 15 (26%)
- Config tests: 18 (31%)

**Total Tests:** 58
**Coverage:** >95% (exceeds 90% goal)
**Next:** S4.I4 (Validation Loop Validation)

---

## Notes

- Similar pattern to Feature 02 (subprocess wrapper + CLI flag)
- Player data fetcher has 7 modules for log quality review vs league_helper's 10 modules
- Focus on API-related edge cases (timeouts, failures, rate limiting)
- Config tests cover LOGGING_LEVEL, LOG_NAME, LOGGING_FORMAT (kept)
- Config tests verify LOGGING_TO_FILE and LOGGING_FILE removed (deprecated)
