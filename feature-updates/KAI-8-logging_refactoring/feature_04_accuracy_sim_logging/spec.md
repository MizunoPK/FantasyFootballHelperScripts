# Feature Specification: accuracy_sim_logging

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 04
**Created:** 2026-02-06
**Last Updated:** 2026-02-06 21:40 UTC

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 4: accuracy_sim_logging**

**Purpose:** CLI integration and log quality improvements for accuracy simulation script

**Scope:**
- Add --enable-log-file flag to run_accuracy_simulation.py (direct entry, already has --log-level precedent)
- Apply DEBUG/INFO quality criteria to simulation/accuracy/ modules
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure) - ✅ COMPLETE

### Relevant Discovery Decisions

- **Solution Approach:** Direct entry script with existing argparse setup (--log-level precedent)
- **Key Constraints:**
  - Must integrate with existing --log-level CLI argument
  - Must preserve existing script behavior when flag not provided
  - Log quality improvements must not break functionality
- **Implementation Order:** After Feature 1 (depends on LineBasedRotatingHandler)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q1: Timestamp format | Full timestamp YYYYMMDD_HHMMSS | Log filenames use precise timestamps |
| Q2: Line-based rotation approach | Eager - maintain counter in memory | Handler tracks line count for 500-line rotation |
| Q3: Log quality criteria | Agent to propose criteria | Must apply DEBUG (tracing) and INFO (user awareness) criteria |
| Q4: CLI flag default | File logging OFF by default | --enable-log-file flag must explicitly enable |
| Q6: Log quality scope | System-wide (Option B) | Affects all simulation/accuracy/ modules |
| Q7: Counter persistence | Counter resets on restart | New timestamped file each script run |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 1 identified run_accuracy_simulation.py has --log-level precedent (smooth argparse integration)
- **Based on User Answer:** Q4 (file logging OFF by default) requires --enable-log-file flag to enable
- **Based on Finding:** Iteration 3 proposed DEBUG/INFO criteria that guide log quality improvements

---

## Feature Overview

**What:** Add CLI flag control for file logging and improve log quality in accuracy simulation modules

**Why:** Enables users to control file logging for simulations, improves debugging and runtime awareness

**Who:** Users running accuracy simulation to optimize scoring algorithm parameters

---

## Functional Requirements

**Source:** RESEARCH_NOTES.md + Feature 01 spec integration contracts + Discovery

### Requirement 1: CLI Flag Integration (--enable-log-file)

**Source:** Epic requirement "CLI toggle for file logging" + Discovery Q4

**Description:**
Add `--enable-log-file` flag to `run_accuracy_simulation.py` argparse configuration. When flag is provided, file logging is enabled using Feature 01's LineBasedRotatingHandler. When flag is omitted, only console logging is active (file logging disabled). This follows the precedent of existing `--log-level` flag.

**Acceptance Criteria:**
- ✅ Add --enable-log-file argument to argparse (after line 224 in run_accuracy_simulation.py)
- ✅ Flag type: action='store_true' (boolean flag, no value needed)
- ✅ Flag default: False (file logging OFF by default per Discovery Q4)
- ✅ Flag help text: Clear description of what flag does
- ✅ Change LOGGING_TO_FILE constant from True → False (line 54)
- ✅ Wire flag to setup_logger() call: pass args.enable_log_file (line 229)
- ✅ Existing --log-level flag behavior unchanged
- ✅ Script runs without errors when flag omitted (console-only logging)
- ✅ Script runs without errors when flag provided (file + console logging)

**Example:**
```bash
# File logging disabled (default):
python run_accuracy_simulation.py

# File logging enabled:
python run_accuracy_simulation.py --enable-log-file

# Combined with --log-level:
python run_accuracy_simulation.py --enable-log-file --log-level debug
```

**Integration with Feature 01:**
- When `--enable-log-file` provided → setup_logger() creates LineBasedRotatingHandler
- Logs written to `logs/accuracy_simulation/accuracy_simulation-{YYYYMMDD_HHMMSS}.log`
- 500-line rotation automatic (per Feature 01)
- Max 50 files enforced (per Feature 01)

**User Answer:** Discovery Q4 (file logging OFF by default, --enable-log-file flag to enable)

---

### Requirement 2: setup_logger() Integration with Feature 01

**Source:** Feature 01 spec integration contracts + RESEARCH_NOTES.md

**Description:**
Update `setup_logger()` call in `run_accuracy_simulation.py` to follow Feature 01's integration contracts. Pass `None` for `log_file_path` parameter (let LoggingManager auto-generate path), pass CLI-driven `enable_log_file` parameter, use consistent logger name "accuracy_simulation" (becomes folder name).

**Acceptance Criteria:**
- ✅ Remove hardcoded log path constant LOGGING_FILE (line 56) - no longer needed
- ✅ Update setup_logger() call (line 229) to:
  ```python
  setup_logger(LOG_NAME, args.log_level.upper(), args.enable_log_file, None, LOGGING_FORMAT)
  ```
  - Parameter 1: LOG_NAME = "accuracy_simulation" (unchanged)
  - Parameter 2: args.log_level.upper() (unchanged)
  - Parameter 3: args.enable_log_file (NEW - CLI-driven)
  - Parameter 4: None (CHANGED from LOGGING_FILE - let LoggingManager generate path)
  - Parameter 5: LOGGING_FORMAT (unchanged)
- ✅ Logger name "accuracy_simulation" creates folder logs/accuracy_simulation/
- ✅ No hardcoded paths in run_accuracy_simulation.py (all paths auto-generated)
- ✅ Integration contract 1 satisfied: Logger name = folder name
- ✅ Integration contract 2 satisfied: log_file_path = None
- ✅ Integration contract 3 satisfied: log_to_file CLI-driven

**Example:**
```python
# OLD (current):
setup_logger(LOG_NAME, args.log_level.upper(), LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
# - LOGGING_TO_FILE = True (hardcoded)
# - LOGGING_FILE = "./simulation/accuracy_log.txt" (hardcoded path)

# NEW (required):
setup_logger(LOG_NAME, args.log_level.upper(), args.enable_log_file, None, LOGGING_FORMAT)
# - args.enable_log_file = CLI-driven (default False)
# - None = let LoggingManager generate path (logs/accuracy_simulation/accuracy_simulation-{timestamp}.log)
```

**Integration Contracts (from Feature 01):**
1. **Logger name = folder name:** "accuracy_simulation" → logs/accuracy_simulation/
2. **log_file_path = None:** Let LoggingManager generate path (no hardcoded paths)
3. **log_to_file CLI-driven:** args.enable_log_file controls file logging on/off

**User Answer:** Feature 01 integration contracts (documented in Feature 01 spec)

---

### Requirement 3: Log Quality - DEBUG Level Improvements

**Source:** Discovery Iteration 3 (DEBUG criteria) + RESEARCH_NOTES.md log quality assessment

**Description:**
Improve DEBUG-level logging across accuracy simulation modules to follow quality criteria: function entry/exit for complex flows, data transformations with before/after values, conditional branches taken. Apply comprehensive quality improvements to ALL 111 logger calls (system-wide coverage per Discovery Q6).

**Acceptance Criteria:**

**DEBUG Criteria (from Discovery):**
- ✅ Function entry/exit with parameters (not excessive - only for complex flows)
- ✅ Data transformations with before/after values
- ✅ Conditional branch taken (which if/else path executed)
- ❌ NOT every variable assignment
- ❌ NOT logging inside tight loops without throttling

**High-Priority Improvements (from RESEARCH_NOTES.md):**

**AccuracySimulationManager.py:**
- ✅ Add DEBUG entry/exit for `_find_resume_point()` method (complex resume logic with 9 steps)
- ✅ Add DEBUG entry/exit for `_load_projected_data()` method (multi-week data loading)
- ✅ Add DEBUG parameter value logging in `run_single_mode()` for each test iteration
  - Example: "Testing parameter X: value=Y (test_idx=Z)"
- ✅ Review existing 13 DEBUG calls for quality (keep if criteria-compliant, improve if not)

**ParallelAccuracyRunner.py:**
- ✅ Add DEBUG worker activity tracing in `evaluate_configs_parallel()`
  - Example: "Worker N starting config X (queue depth: Y)"
  - Throttle: Log every 10th config (not every single config - too verbose with 100+ configs)
  - **User Decision (Q2):** Confirmed - add with every 10th throttling
- ✅ Add DEBUG completion rate in `evaluate_configs_parallel()`
  - Example: "Progress: X/Y configs evaluated (Z% complete)"
  - Log every 10 configs completed
  - **User Decision (Q2):** Confirmed - valuable for debugging parallel execution

**AccuracyCalculator.py:**
- ✅ Review existing 12 DEBUG calls for loop verbosity
- ✅ Add throttling if DEBUG calls inside loops exceed 100 iterations
- ✅ Add DEBUG data transformation tracing in `calculate_mae()` before/after projected points calculation
  - Example: "calculate_mae: before_agg=X_players, after_agg=Y_players"

**AccuracyResultsManager.py:**
- ✅ Add DEBUG entry/exit for `get_summary()` method (generates multi-line summary string)
- ✅ Review existing 4 DEBUG calls for quality

**Total Estimated Changes:** Review and improve ALL 111 logger calls (comprehensive system-wide coverage)

**User Decision (Q1):** Update ALL 111 calls for comprehensive quality improvement (not just high-priority subset)

**Out of Scope:**
- Adding DEBUG for every method (only improve existing calls, don't add unnecessary ones)
- Standardizing message decoration - **User Decision (Q3):** Keep existing styles (cosmetic, no functional impact)

**User Answer:** Discovery Q3 (agent-proposed DEBUG criteria), Q6 (system-wide improvements)

---

### Requirement 4: Log Quality - INFO Level Improvements

**Source:** Discovery Iteration 3 (INFO criteria) + RESEARCH_NOTES.md log quality assessment

**Description:**
Improve INFO-level logging across accuracy simulation modules to follow quality criteria: script start/complete with configuration, major phase transitions, significant outcomes. Focus on high-priority improvements that provide user awareness without implementation details.

**Acceptance Criteria:**

**INFO Criteria (from Discovery):**
- ✅ Script start/complete with configuration
- ✅ Major phase transitions (e.g., "Starting accuracy simulation")
- ✅ Significant outcomes (e.g., "Simulation complete: 10 parameters optimized")
- ❌ NOT implementation details (that's DEBUG)
- ❌ NOT every function call

**High-Priority Improvements (from RESEARCH_NOTES.md):**

**AccuracySimulationManager.py:**
- ✅ Add INFO configuration summary at initialization (after line 99):
  - Baseline config path
  - Number of parameters to test
  - Test values per parameter
  - Total configs to evaluate
  - Parallel workers count
  - Example: "Configuration: baseline=X, params=16, test_values=3, total_configs=Y, workers=8"
- ✅ Review existing 29 INFO calls for quality (currently good coverage)

**AccuracyResultsManager.py:**
- ✅ Add INFO summary stats at initialization (line 306):
  - Baseline config count (number of week horizon configs)
  - Output directory
  - Example: "AccuracyResultsManager: baseline_configs=4, output=simulation/simulation_configs"
- ✅ Review existing 16 INFO calls (currently good coverage of save/load operations)

**AccuracyCalculator.py:**
- ✅ Review existing 2 INFO calls (season-level summaries - currently appropriate)
- ✅ Consider adding INFO MAE threshold messages (optional):
  - Example: "MAE below target threshold: 2.5 < 3.0"
  - Only if meaningful to user (may be too detailed)

**ParallelAccuracyRunner.py:**
- ✅ Review existing 7 INFO calls (currently good parallel execution tracking)
- ✅ Consider adding INFO completion rate statistics (covered by Requirement 3 DEBUG improvements)

**Total Estimated Changes:** Review and improve ALL INFO calls as part of comprehensive 111-call review

**User Decision (Q1):** Update ALL 111 calls for comprehensive quality improvement

**Out of Scope:**
- Adding INFO for every method (excessive, violates "not every function call" criteria)
- Detailed algorithm implementation logging (that's DEBUG)

**User Answer:** Discovery Q3 (agent-proposed INFO criteria), Q6 (system-wide improvements)

---

### Requirement 5: ERROR-Level Logging for Critical Failures

**Source:** User Answer to Question 4 + RESEARCH_NOTES.md gap analysis

**Description:**
Add ERROR-level logging for critical failures to improve error diagnosability. Currently only 1 ERROR call exists (ParallelAccuracyRunner). Add ERROR logging for unrecoverable failures during initialization and execution.

**Acceptance Criteria:**

**ERROR Criteria:**
- ✅ Add ERROR for unrecoverable failures (failures that cause script to exit)
- ✅ Include exception info with exc_info=True for traceability
- ✅ Clear error messages indicating what failed and why

**Critical Failures to Add ERROR For:**

**run_accuracy_simulation.py:**
- ✅ Baseline config folder not found (line ~256: FileNotFoundError)
- ✅ Baseline config folder missing required files (line ~251)
- ✅ sim_data/ folder not found (line ~264)
- ✅ AccuracySimulationManager initialization failure (line ~293)

**AccuracySimulationManager.py:**
- ✅ Projected data load failure (lines ~327, 331: folder not found, missing files)
- ✅ Configuration validation failure (if any)
- ✅ Critical resume point detection failure (if data corruption)

**AccuracyCalculator.py:**
- ✅ Season data load failure (line ~159: week data missing - upgrade WARNING to ERROR if unrecoverable)

**AccuracyResultsManager.py:**
- ✅ Baseline config load failure (line ~468: missing league_config.json - upgrade WARNING to ERROR)
- ✅ Optimal config save failure (if folder creation fails)

**Total Estimated Changes:** 5-10 new ERROR calls (critical failure paths)

**User Decision (Q4):** Add ERROR for critical failures - improves error visibility and diagnosability

---

## Technical Requirements

**Source:** RESEARCH_NOTES.md code locations + Feature 01 spec

### Files to Modify

**1. run_accuracy_simulation.py**

**Changes:**
- Line 54: Change `LOGGING_TO_FILE = True` → `LOGGING_TO_FILE = False`
- Line 56: Remove or comment out `LOGGING_FILE = "./simulation/accuracy_log.txt"` (no longer needed)
- After line 224: Add --enable-log-file flag to argparse
- Line 229: Update setup_logger() call to use args.enable_log_file and None for path

**Implementation:**
```python
# Line 54 (CHANGE):
LOGGING_TO_FILE = False  # Default OFF - use --enable-log-file to enable

# Line 56 (REMOVE or COMMENT):
# LOGGING_FILE = "./simulation/accuracy_log.txt"  # No longer needed - LoggingManager auto-generates path

# After line 224 (ADD):
parser.add_argument(
    '--enable-log-file',
    action='store_true',
    default=False,
    help='Enable file logging to logs/accuracy_simulation/ folder (default: console only). '
         'Logs rotate at 500 lines, max 50 files per folder.'
)

# Line 229 (UPDATE):
setup_logger(LOG_NAME, args.log_level.upper(), args.enable_log_file, None, LOGGING_FORMAT)
```

**2. simulation/accuracy/AccuracySimulationManager.py**

**Changes:**
- Add DEBUG entry/exit for `_find_resume_point()` (lines ~180-290)
- Add DEBUG entry/exit for `_load_projected_data()` (lines ~300-380)
- Add INFO configuration summary at initialization (after line 99)
- Add DEBUG parameter value logging in `run_single_mode()` test iterations (lines ~770-900)
- Review existing 58 logger calls for quality

**3. simulation/accuracy/ParallelAccuracyRunner.py**

**Changes:**
- Add DEBUG worker activity tracing in `evaluate_configs_parallel()` (lines ~370-420)
- Add DEBUG completion rate tracking (log every 10 configs)
- Add throttling for DEBUG logs (every 10th config, not every single one)
- Review existing 11 logger calls for quality

**4. simulation/accuracy/AccuracyCalculator.py**

**Changes:**
- Add DEBUG data transformation tracing in `calculate_mae()` (lines ~110-130)
- Review existing 12 DEBUG calls for loop verbosity
- Add throttling if loops exceed 100 iterations
- Review existing 19 logger calls for quality

**5. simulation/accuracy/AccuracyResultsManager.py**

**Changes:**
- Add INFO summary stats at initialization (line 306)
- Add DEBUG entry/exit for `get_summary()` (lines ~640-730)
- Add ERROR for baseline config load failure (line 468: upgrade WARNING to ERROR)
- Add ERROR for optimal config save failure
- Review existing 23 logger calls for quality

**6. run_accuracy_simulation.py**

**Changes:**
- Add ERROR for baseline config not found (line ~256)
- Add ERROR for baseline config missing required files (line ~251)
- Add ERROR for sim_data/ folder not found (line ~264)
- Add ERROR for AccuracySimulationManager initialization failure (line ~293)

---

## Integration Points

### Integration with Feature 01 (Core Infrastructure)

**Direction:** This feature CONSUMES FROM Feature 01

**Data Consumed:**
- **LineBasedRotatingHandler:** Custom handler class (500-line rotation, 50-file cleanup, timestamped filenames)
- **Modified setup_logger():** Accepts log_to_file parameter, instantiates LineBasedRotatingHandler when True
- **Folder Structure:** logs/{script_name}/ auto-created by handler

**Interface:**

**Complete setup_logger() Signature (from Feature 01 actual implementation):**
```python
def setup_logger(
    name: str,
    level: Union[str, int] = 'INFO',
    log_to_file: bool = False,
    log_file_path: Optional[Union[str, Path]] = None,
    log_format: str = 'standard',
    enable_console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # Backward compatibility (not used)
    backup_count: int = 5  # Backward compatibility (not used)
) -> logging.Logger
```

**Feature 04 Usage:**
```python
from utils.LoggingManager import setup_logger, get_logger

# Entry point (run_accuracy_simulation.py):
setup_logger(
    name="accuracy_simulation",       # Logger name (becomes folder name)
    level="INFO",                      # Log level (from --log-level flag)
    log_to_file=args.enable_log_file, # CLI-driven (from --enable-log-file flag)
    log_file_path=None,               # Let LoggingManager auto-generate path
    log_format="detailed"             # Format style
    # enable_console=True (default, can omit)
    # max_file_size, backup_count (optional, can omit)
)
# Result:
#   Initial file: logs/accuracy_simulation/accuracy_simulation-{YYYYMMDD_HHMMSS}.log
#   Rotated files: logs/accuracy_simulation/accuracy_simulation-{YYYYMMDD_HHMMSS_microseconds}.log

# Modules (AccuracySimulationManager, AccuracyCalculator, etc.):
logger = get_logger()  # Gets logger configured by entry point
logger.info("Starting accuracy simulation")
logger.debug("Testing parameter X: value=Y")
```

**Note:** Updated based on feature_01 actual implementation. Rotated files include microsecond precision to prevent timestamp collisions.

**Integration Contracts (must follow):**
1. **Logger name = folder name:** Use "accuracy_simulation" (not variations) → creates logs/accuracy_simulation/
2. **log_file_path = None:** Don't specify custom paths (let LoggingManager generate)
3. **log_to_file CLI-driven:** Wire --enable-log-file flag to log_to_file parameter

**Example Flow:**
```
User runs: python run_accuracy_simulation.py --enable-log-file --log-level debug

→ run_accuracy_simulation.py:
  - Parses args: enable_log_file=True, log_level='debug'
  - Calls setup_logger('accuracy_simulation', 'DEBUG', True, None, 'detailed')

→ LoggingManager (Feature 01):
  - Creates logs/accuracy_simulation/ folder (if not exists)
  - Generates filename: accuracy_simulation-20260206_214530.log
  - Instantiates LineBasedRotatingHandler(max_lines=500, max_files=50)
  - Configures logger with DEBUG level

→ AccuracySimulationManager:
  - Calls get_logger() - receives configured logger
  - logger.info("Initializing AccuracySimulationManager") → written to file
  - logger.debug("Testing parameter X: value=Y") → written to file

→ After 500 log lines:
  - LineBasedRotatingHandler rotates to new file
  - Old file: accuracy_simulation-20260206_214530.log (500 lines)
  - New file: accuracy_simulation-20260206_215045.log (continuing)
```

---

## Error Handling

**Source:** Feature 01 error handling + RESEARCH_NOTES.md

### Error Scenario 1: Missing logs/ Folder (Permission Denied)

**Trigger:** User doesn't have write permissions to project root when --enable-log-file provided

**Handling:**
- LineBasedRotatingHandler (Feature 01) attempts to create logs/accuracy_simulation/
- Permission denied → OSError raised
- Caught by logging.FileHandler.handleError()
- Error logged to stderr (not file, since file can't be created)
- Script continues with console-only logging

**User Impact:** File logging disabled, console logging continues

**Mitigation:** Document requirement that user needs write permissions to project root

---

### Error Scenario 2: Invalid --log-level Value

**Trigger:** User provides invalid log level: `python run_accuracy_simulation.py --log-level invalid`

**Handling:**
- argparse validates choices=['debug', 'info', 'warning', 'error'] (line 218)
- Invalid value → argparse error message
- Script exits with error code 2

**User Impact:** Script doesn't run, user sees helpful error message

**Mitigation:** None needed (argparse handles validation)

---

### Error Scenario 3: Disk Full During Simulation

**Trigger:** Disk space exhausted during log file write

**Handling:**
- LineBasedRotatingHandler write operation raises OSError
- Caught by logging.FileHandler.handleError()
- Error logged to stderr
- Simulation continues (logs to console if enabled)

**User Impact:** Some log messages may be lost from file

**Mitigation:** User responsible for disk space management (standard logging behavior)

---

## Testing Strategy

{To be defined in S4 (Epic Testing Strategy stage)}

**Expected Test Coverage:**

**Unit Tests:**
- CLI flag parsing (--enable-log-file default, provided)
- setup_logger() integration (args.enable_log_file wiring)
- Logger mock assertions for new/modified log statements

**Integration Tests:**
- File logging enabled: Verify logs/ folder created, timestamped files generated
- File logging disabled: Verify no file created, console-only
- 500-line rotation: Verify new file created after 500 lines
- Max 50 files: Verify oldest files deleted when limit exceeded

**Test Files to Update:**
- `tests/simulation/accuracy/test_accuracy_cli_logging.py` (NEW - CLI flag tests)
- `tests/simulation/accuracy/test_AccuracySimulationManager.py` (UPDATE - logger mock assertions)
- `tests/simulation/accuracy/test_AccuracyCalculator.py` (UPDATE - logger mock assertions)
- `tests/simulation/accuracy/test_ParallelAccuracyRunner.py` (UPDATE - logger mock assertions)
- `tests/simulation/accuracy/test_AccuracyResultsManager.py` (UPDATE - logger mock assertions)

---

## Non-Functional Requirements

**Maintainability:**
- ✅ Must follow project coding standards (CODING_STANDARDS.md)
- ✅ Must preserve existing accuracy simulation behavior (no functional changes)
- ✅ Must maintain backward compatibility (script runs without --enable-log-file)
- ✅ Logger improvements must not break existing tests (update assertions as needed)

**Performance:**
- ✅ No performance degradation when file logging disabled (default)
- ✅ Minimal overhead when file logging enabled (<1ms per log call)
- ✅ Throttled DEBUG logging (every 10th config) to prevent excessive volume
- ✅ No tight-loop logging without throttling (per DEBUG criteria)

**Usability:**
- ✅ Clear help text for --enable-log-file flag
- ✅ Consistent with existing --log-level flag pattern
- ✅ Error messages helpful when invalid arguments provided

**Testability:**
- ✅ All code changes covered by unit tests
- ✅ Integration tests verify Feature 01 integration
- ✅ Logger mock assertions validate new log statements

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Core infrastructure changes (Feature 01 handles LineBasedRotatingHandler)
- Other scripts' CLI integration (Features 2-3, 5-7 handle their scripts)
- Console logging format changes (only file logging affected)
- Log compression or archiving (not required)
- Configurable rotation limits (hardcoded 500 lines, 50 files per Feature 01)

---

## Open Questions

{To be populated during S2 deep dive - questions tracked in checklist.md}

---

## Implementation Notes

**Source:** RESEARCH_NOTES.md + Feature 01 spec

### Design Decisions

**1. CLI Flag Pattern:**
- ✅ Follow existing --log-level precedent (argparse, choices validation)
- ✅ Use action='store_true' for boolean flag (no value needed)
- ✅ Default False (file logging OFF per Discovery Q4)
- **Rationale:** Consistent with existing CLI patterns, easy to use

**2. Log Quality Scope:**
- ✅ Comprehensive improvements (ALL 111 logger calls)
- ✅ System-wide coverage per Discovery Q6
- ✅ Focus on complex methods, data transformations, parallel execution, plus review all existing calls
- **Rationale:** User Decision Q1 - comprehensive approach ensures consistent quality across all modules
- **User Decision (Q1):** Update ALL 111 calls (not just high-priority subset)

**3. DEBUG Throttling:**
- ✅ Log every 10th config in parallel execution (not every single config)
- ✅ Add throttling for tight loops (if >100 iterations)
- **Rationale:** Prevents log volume explosion with 100+ configs × 8 workers

**4. Logger Name:**
- ✅ Use "accuracy_simulation" (matches script purpose)
- ✅ Creates folder logs/accuracy_simulation/
- **Rationale:** Clear, descriptive, follows Feature 01 contract

**5. Backward Compatibility:**
- ✅ Keep existing --log-level behavior unchanged
- ✅ Script runs without --enable-log-file (console-only)
- ✅ Update tests but don't break existing test suite
- **Rationale:** No breaking changes for existing users

### Implementation Tips

**CLI Flag:**
- Add --enable-log-file immediately after --log-level (line 224) for logical grouping
- Use clear help text explaining what flag does and default behavior

**setup_logger() Integration:**
- Use args.enable_log_file directly (no intermediate variable needed)
- Pass None for log_file_path (let LoggingManager handle path generation)
- Test both flag=True and flag=False cases

**Log Quality:**
- Add new DEBUG/INFO statements incrementally (not all at once)
- Test after each batch of changes (verify tests still pass)
- Use consistent message formats (e.g., "Testing parameter X: value=Y" not "Testing param X: Y")

**Testing:**
- Create new test file for CLI flag tests (test_accuracy_cli_logging.py)
- Update existing tests' logger mock assertions (grep for logger.info/debug assertions)
- Use tmp_path fixture for integration tests (clean log folder per test)

---

## Acceptance Criteria Cross-Reference

| Requirement | Test Coverage | Implementation Location |
|-------------|---------------|-------------------------|
| Req 1: CLI Flag Integration | test_accuracy_cli_logging.py: test_enable_log_file_flag | run_accuracy_simulation.py lines 54, 224, 229 |
| Req 2: setup_logger() Integration | test_accuracy_cli_logging.py: test_setup_logger_integration | run_accuracy_simulation.py line 229 |
| Req 3: DEBUG Improvements | test_AccuracySimulationManager.py: test_logger_debug_calls | AccuracySimulationManager, ParallelAccuracyRunner, AccuracyCalculator |
| Req 4: INFO Improvements | test_AccuracySimulationManager.py: test_logger_info_calls | AccuracySimulationManager, AccuracyResultsManager |
| Req 5: ERROR Critical Failures | test_accuracy_cli_logging.py: test_error_logging | run_accuracy_simulation.py, AccuracySimulationManager, AccuracyResultsManager |

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
| 2026-02-06 21:40 UTC | Secondary-C | Complete spec draft with 4 requirements, technical details, integration points, error handling | S2.P1.I1 (Discovery - research complete) |
| 2026-02-06 22:00 UTC | Secondary-C | Added Requirement 5 (ERROR-level logging), updated all user decisions from checklist Q1-Q4 | S2.P1.I2 (Checklist Resolution - complete) |
| 2026-02-08 12:10 | Agent | Updated setup_logger() signature, type hints, return type, filename formats based on Feature 01 actual implementation | S8.P1 (Cross-Feature Alignment - Feature 01 complete) |

---

**End of Feature Specification**
