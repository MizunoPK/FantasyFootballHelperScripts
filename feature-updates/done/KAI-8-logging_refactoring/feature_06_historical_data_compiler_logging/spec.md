# Feature Specification: historical_data_compiler_logging

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 06
**Created:** 2026-02-06
**Last Updated:** 2026-02-06 (Gate 3 approved)

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 6: historical_data_compiler_logging**

**Purpose:** CLI integration and log quality improvements for historical data compiler script

**Scope:**
- Add --enable-log-file flag to compile_historical_data.py
- Apply DEBUG/INFO criteria to historical_data_compiler/ modules logs
- Review and improve logs in: json_exporter, player_data_fetcher, weekly_snapshot_generator, game_data_fetcher, http_client, schedule_fetcher
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

### Relevant Discovery Decisions

- **Solution Approach:** Direct entry script (compile_historical_data.py)
- **Key Constraints:**
  - Must preserve existing script behavior when flag not provided
  - Log quality improvements must not break functionality
  - Multiple submodules need log quality attention
- **Implementation Order:** After Feature 1 (depends on LineBasedRotatingHandler)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q2: Rotation approach | Eager counter | Handler integration from Feature 1 |
| Q3: Log quality criteria | Agent to propose criteria | Must apply DEBUG (tracing) and INFO (user awareness) criteria |
| Q4: CLI flag default | File logging OFF by default | Flag must explicitly enable file logging |
| Q5: Script coverage | Just those 6 scripts | Confirms historical_data_compiler in scope (compile_historical_data.py) |
| Q6: Log quality scope | System-wide (Option B) | Affects historical_data_compiler/ submodules |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 2 confirmed compile_historical_data.py is the historical_data_compiler script
- **Based on Finding:** Iteration 2 identified 17 debug/info calls in historical_data_compiler/
- **Based on Finding:** Iteration 3 proposed DEBUG/INFO criteria that guide log quality improvements

---

## Feature Overview

**What:** Add CLI flag control for file logging and improve log quality in historical data compiler modules

**Why:** Enables users to control file logging for historical data compilation, improves debugging and runtime awareness

**Who:** Users running compile_historical_data.py to build historical datasets

---

## Functional Requirements

**Source:** RESEARCH_NOTES.md + Discovery Q3, Q4, Q6

### Requirement 1: CLI Flag Integration

**Source:** Epic requirement + Discovery Q4 (file logging OFF by default)

**Description:**
Add `--enable-log-file` flag to `compile_historical_data.py` argument parser to control file logging. When enabled, logs are written to `logs/historical_data_compiler/` using Feature 01's LineBasedRotatingHandler. When disabled (default), only console logging occurs.

**Acceptance Criteria:**
- ✅ Flag `--enable-log-file` added to argument parser (after `--verbose` flag at line 87)
- ✅ Flag is action="store_true" (boolean, no value required)
- ✅ Help text: "Enable file logging to logs/historical_data_compiler/"
- ✅ Flag passed to setup_logger() via `log_to_file=args.enable_log_file` parameter
- ✅ `log_file_path=None` passed to setup_logger() (let LoggingManager auto-generate path)
- ✅ Default behavior unchanged (file logging OFF when flag not provided)
- ✅ Existing behavior preserved (console logging always works)

**Example:**
```bash
# File logging disabled (default):
python compile_historical_data.py --year 2024
# Result: Console logs only, no files created

# File logging enabled:
python compile_historical_data.py --year 2024 --enable-log-file
# Result: Console logs + logs/historical_data_compiler/historical_data_compiler-20260206_143522.log

# Combined with verbose:
python compile_historical_data.py --year 2024 --verbose --enable-log-file
# Result: Console DEBUG logs + file DEBUG logs
```

**Implementation Location:**
- File: `compile_historical_data.py`
- Argument parser: Lines 66-96 (add flag after line 87)
- setup_logger call: Line 260 (modify to add log_to_file and log_file_path parameters)

**User Answer:** Q4 (file logging OFF by default, --enable-log-file flag to enable)

---

### Requirement 2: setup_logger() Integration

**Source:** Feature 01 integration contract + RESEARCH_NOTES.md

**Description:**
Modify `setup_logger()` call in `compile_historical_data.py` to pass `log_to_file` and `log_file_path` parameters, integrating with Feature 01's LineBasedRotatingHandler.

**Acceptance Criteria:**
- ✅ Pass `log_to_file=args.enable_log_file` to setup_logger() (ties flag to file logging)
- ✅ Pass `log_file_path=None` to setup_logger() (use auto-generated path from LoggingManager)
- ✅ Logger name remains `"historical_data_compiler"` (matches folder name requirement)
- ✅ Log level logic unchanged (`log_level = "DEBUG" if args.verbose else "INFO"`)
- ✅ Integration follows Feature 01 contracts: consistent logger name, no custom paths, CLI-driven log_to_file

**Example:**
```python
# Current code (line 258-260):
log_level = "DEBUG" if args.verbose else "INFO"
setup_logger(name="historical_data_compiler", level=log_level)
logger = get_logger()

# Modified code:
log_level = "DEBUG" if args.verbose else "INFO"
setup_logger(
    name="historical_data_compiler",
    level=log_level,
    log_to_file=args.enable_log_file,  # NEW
    log_file_path=None                  # NEW (auto-generate)
)
logger = get_logger()
```

**Implementation Location:**
- File: `compile_historical_data.py`
- Lines: 258-261

**User Answer:** Feature 01 integration contract (log_file_path=None, log_to_file from CLI)

---

### Requirement 3: Log Quality - DEBUG Level

**Source:** Discovery Q3 (DEBUG criteria) + RESEARCH_NOTES.md

**Description:**
Review and improve DEBUG-level logging across historical_data_compiler modules to follow Discovery criteria: function entry/exit with parameters, data transformations with before/after values, conditional branches taken. Remove excessive debugging (variable assignments, tight loops without throttling).

**Acceptance Criteria:**
- ✅ http_client.py: DEBUG logs for lifecycle (session create/close), request details (URL, method), outcomes (success)
  - CURRENT: 5 DEBUG calls ✅ (already good - line 98, 111, 146, 176)
  - NO CHANGES needed
- ✅ game_data_fetcher.py: DEBUG logs for fetching progress per week, data loading outcomes
  - CURRENT: 3 DEBUG calls (lines 143, 189, 346)
  - ADD: DEBUG log for weather fetch attempts before API call (approved - helps trace API calls with coordinates)
  - CHANGE: Move line 346 "No coordinates, skipping weather" to INFO (affects output data quality - user should be aware)
- ✅ schedule_fetcher.py: DEBUG logs for fetching progress per week
  - CURRENT: 2 DEBUG calls (lines 68, 124)
  - CHANGE: Move line 124 "Error parsing event" to WARNING (non-fatal error with data quality impact)
- ✅ json_exporter.py: DEBUG logs for JSON generation per position
  - CURRENT: 2 DEBUG calls (lines 409, 436) ✅ (already good)
  - NO CHANGES needed
- ✅ weekly_snapshot_generator.py: DEBUG logs for snapshot generation per week
  - CURRENT: 1 DEBUG call (line 178) ✅ (already good)
  - NO CHANGES needed
- ✅ player_data_fetcher.py: DEBUG logs for player processing progress
  - CURRENT: 1 DEBUG call (line 257 - throttled every 100 players) ✅
  - SKIP: No additional DEBUG log for parsing transformations (user decision - existing throttled log sufficient)
- ✅ team_data_calculator.py: DEBUG logs for team data calculation
  - CURRENT: 0 DEBUG calls
  - ADD: DEBUG log for team aggregation calculations (per-team progress if needed)
- ❌ NO tight loop logging without throttling
- ❌ NO variable assignment logging

**Example:**
```python
# GOOD (existing - http_client.py line 146):
self.logger.debug(f"Making {method} request to: {url}")

# GOOD (existing - player_data_fetcher.py line 257 - throttled):
if processed % 100 == 0:
    self.logger.debug(f"Processed {processed} players")

# ADD (game_data_fetcher.py - before weather fetch):
self.logger.debug(f"Fetching weather for {game_date} at {lat},{lon}")

# CONSIDER MOVING (schedule_fetcher.py line 124):
# FROM: self.logger.debug(f"Error parsing event in week {week}: {e}")
# TO: self.logger.warning(f"Error parsing event in week {week}: {e}")
```

**User Answer:** Q3 (agent proposes criteria), Q6 (system-wide log quality)

---

### Requirement 4: Log Quality - INFO Level

**Source:** Discovery Q3 (INFO criteria) + RESEARCH_NOTES.md

**Description:**
Review and improve INFO-level logging across compile_historical_data.py and modules to follow Discovery criteria: script start/complete with configuration, major phase transitions, significant outcomes. Remove implementation details (those belong in DEBUG).

**Acceptance Criteria:**
- ✅ compile_historical_data.py: INFO logs for compilation workflow phases
  - CURRENT: ~22 INFO calls (already good - phase transitions, outcomes, configuration)
  - ADD: Log GENERATE_CSV/GENERATE_JSON toggle values at startup (approved - improves configuration visibility and debugging)
- ✅ player_data_fetcher.py: INFO logs for player fetching phases
  - CURRENT: 6 INFO calls (lines 167, 188, 212, 481, 492, 506, 517) ✅ (already good)
  - NO CHANGES needed
- ✅ team_data_calculator.py: INFO logs for team calculation phases
  - CURRENT: 4 INFO calls (lines 76, 116, 250, 260) ✅ (already good)
  - NO CHANGES needed
- ✅ game_data_fetcher.py: INFO logs for game fetching phases
  - CURRENT: 4 INFO calls (lines 184, 205, 412, 424) ✅ (already good)
  - NO CHANGES needed
- ✅ schedule_fetcher.py: INFO logs for schedule fetching phases
  - CURRENT: 4 INFO calls (lines 63, 82, 168, 193) ✅ (already good)
  - NO CHANGES needed
- ✅ json_exporter.py: INFO logs for JSON export phases
  - CURRENT: 1 INFO call (line 428) ✅ (already good)
  - NO CHANGES needed
- ✅ weekly_snapshot_generator.py: INFO logs for snapshot generation phases
  - CURRENT: 2 INFO calls (lines 132, 139) ✅ (already good)
  - NO CHANGES needed
- ✅ http_client.py: INFO logs for configuration at initialization
  - CURRENT: 0 INFO calls
  - SKIP: No INFO log for HTTP client configuration (user decision - not important enough)
- ❌ NO implementation details (function calls, variable values)
- ❌ NO excessive INFO logs (only major phase transitions)

**Example:**
```python
# GOOD (existing - compile_historical_data.py line 187):
logger.info("[1/5] Fetching schedule data...")

# GOOD (existing - compile_historical_data.py line 189):
logger.info(f"  - Schedule fetched for {len(schedule)} weeks")

# ADD (compile_historical_data.py - after logger setup):
logger.info(f"Output format: CSV={GENERATE_CSV}, JSON={GENERATE_JSON}")

# ADD (http_client.py __init__):
self.logger.info(f"HTTP client initialized (timeout={timeout}s, rate_limit={rate_limit_delay}s)")
```

**User Answer:** Q3 (agent proposes criteria), Q6 (system-wide log quality)

---

### Requirement 5: Test Assertion Updates

**Source:** RESEARCH_NOTES.md (Test Impact Analysis)

**Description:**
Update test assertions in 3 test files to reflect modified/added log messages from Requirement 3 and 4. Ensure 100% test pass rate after log quality changes.

**Acceptance Criteria:**
- ✅ Reactive approach: Run tests first, update only failing assertions (user decision - more efficient)
- ✅ tests/historical_data_compiler/test_weekly_snapshot_generator.py: Update assertions that fail
- ✅ tests/historical_data_compiler/test_game_data_fetcher.py: Update assertions that fail
- ✅ tests/historical_data_compiler/test_team_data_calculator.py: Update assertions that fail
- ✅ All test assertions match new log messages (wording, level, count)
- ✅ 100% test pass rate after changes (mandatory per workflow)
- ✅ No skipped tests, no xfail tests

**Example:**
```python
# Before (test expects specific log message):
assert "Fetching game data for week" in caplog.text

# After (updated to match new message):
assert "Fetching game data for week 1/17" in caplog.text

# Before (test expects 5 log calls):
assert len(caplog.records) == 5

# After (updated to match new count with added DEBUG log):
assert len(caplog.records) == 6
```

**Implementation Location:**
- tests/historical_data_compiler/test_weekly_snapshot_generator.py
- tests/historical_data_compiler/test_game_data_fetcher.py
- tests/historical_data_compiler/test_team_data_calculator.py

**User Answer:** Workflow requirement (100% test pass rate mandatory)

---

## Technical Requirements

**Source:** RESEARCH_NOTES.md (Code Locations)

### Modified Files

| File | Lines Modified | Type | Description |
|------|----------------|------|-------------|
| compile_historical_data.py | 87-94 (add), 260-264 (modify) | PRIMARY | Add --enable-log-file flag, modify setup_logger() call, add config INFO log |
| historical_data_compiler/http_client.py | 79-83 (add) | SECONDARY | Add INFO log for configuration at __init__ |
| historical_data_compiler/game_data_fetcher.py | ~350 (add/modify) | SECONDARY | Add DEBUG log for weather fetch, consider moving line 346 to INFO |
| historical_data_compiler/player_data_fetcher.py | ~260 (add) | SECONDARY | Add DEBUG log for player parsing |
| historical_data_compiler/schedule_fetcher.py | 124 (modify) | SECONDARY | Consider moving error log from DEBUG to WARNING |
| tests/historical_data_compiler/test_*.py | Various | TEST | Update 3 test files for new log assertions |

### Argument Parser Changes

**Location:** compile_historical_data.py lines 66-96

**Add new argument** (after line 87):
```python
parser.add_argument(
    "--enable-log-file",
    action="store_true",
    help="Enable file logging to logs/historical_data_compiler/"
)
```

**Key Details:**
- Position: After `--verbose` flag
- Type: Boolean flag (action="store_true")
- Default: False (file logging disabled)
- No value required (presence of flag = True)

### setup_logger() Call Changes

**Location:** compile_historical_data.py lines 258-261

**Current code:**
```python
log_level = "DEBUG" if args.verbose else "INFO"
setup_logger(name="historical_data_compiler", level=log_level)
logger = get_logger()
```

**Modified code:**
```python
log_level = "DEBUG" if args.verbose else "INFO"
setup_logger(
    name="historical_data_compiler",
    level=log_level,
    log_to_file=args.enable_log_file,  # NEW
    log_file_path=None                  # NEW
)
logger = get_logger()

# ADD after get_logger():
logger.info(f"Output format: CSV={GENERATE_CSV}, JSON={GENERATE_JSON}")
```

### Log Quality Modifications

**Summary of Changes:**

1. **http_client.py** (~line 80, __init__ method):
   - ADD: `self.logger.info(f"HTTP client initialized (timeout={self.timeout}s, rate_limit={self.rate_limit_delay}s)")`

2. **game_data_fetcher.py** (~line 350):
   - ADD: DEBUG log before weather API call
   - CONSIDER: Move line 346 "No coordinates" from DEBUG to INFO

3. **player_data_fetcher.py** (~line 260):
   - ADD: DEBUG log for player parsing transformations

4. **schedule_fetcher.py** (line 124):
   - CONSIDER: Change `logger.debug(f"Error parsing event...")` to `logger.warning(...)`

5. **compile_historical_data.py** (~line 263):
   - ADD: INFO log for GENERATE_CSV/GENERATE_JSON configuration

---

## Integration Points

### Integration with Feature 1 (Core Infrastructure)

**Direction:** This feature consumes FROM Feature 1

**What Feature 01 Provides:**
- `LineBasedRotatingHandler` class (500-line rotation, 50-file cleanup)
- Modified `setup_logger()` API accepting `log_to_file` parameter
- Centralized `logs/{script_name}/` folder structure
- Timestamped filenames: `historical_data_compiler-{YYYYMMDD_HHMMSS}.log`
- Automatic rotation at 500 lines
- Automatic cleanup (max 50 files, delete oldest)

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

**Feature 06 Usage:**
```python
from utils.LoggingManager import setup_logger, get_logger

# Feature 06 calls setup_logger() with new parameters:
setup_logger(
    name="historical_data_compiler",  # Logger name = folder name
    level=log_level,                   # "DEBUG" or "INFO"
    log_to_file=args.enable_log_file, # CLI flag controls file logging
    log_file_path=None                 # Auto-generate path
    # enable_console=True (default, can omit)
    # max_file_size, backup_count (optional, can omit)
)

# Result when --enable-log-file flag provided:
# - logs/historical_data_compiler/ folder created
# - Initial file: historical_data_compiler-{YYYYMMDD_HHMMSS}.log
# - Rotated files: historical_data_compiler-{YYYYMMDD_HHMMSS_microseconds}.log
# - LineBasedRotatingHandler attached to logger
# - Rotation at 500 lines, max 50 files enforced
```

**Note:** Updated based on feature_01 actual implementation. Rotated files include microsecond precision.

**Integration Contracts (from Feature 01 spec):**
1. **Logger name = folder name:** Use consistent name `"historical_data_compiler"` ✅
   - VERIFIED: compile_historical_data.py line 260 already uses this name
2. **log_file_path=None:** Don't specify custom paths ✅
   - PLAN: Pass `log_file_path=None` in modified setup_logger() call
3. **log_to_file driven by CLI:** Wire `--enable-log-file` flag to `log_to_file` parameter ✅
   - PLAN: Pass `log_to_file=args.enable_log_file` in modified setup_logger() call

**Call Flow:**
```
User runs: python compile_historical_data.py --year 2024 --enable-log-file
  ↓
compile_historical_data.py parse_args() → args.enable_log_file = True
  ↓
setup_logger(name="historical_data_compiler", log_to_file=True, log_file_path=None)
  ↓
LoggingManager._generate_log_file_path() → logs/historical_data_compiler/historical_data_compiler-{timestamp}.log
  ↓
LoggingManager.setup_logger() → Instantiates LineBasedRotatingHandler
  ↓
All logger.info/debug/warning/error calls → Written to console AND file
  ↓
At 500 lines → LineBasedRotatingHandler.doRollover() → New timestamped file created
  ↓
After rotation → _cleanup_old_files() → Delete oldest files if > 50
```

### Integration with Python Logging Framework

**Direction:** Uses standard Python logging module

**Logger Acquisition:**
- All modules use `get_logger()` from `utils.LoggingManager`
- Logger name set in compile_historical_data.py: `"historical_data_compiler"`
- Submodules inherit logger from main script (shared logger instance)

**Logger Hierarchy:**
```
compile_historical_data.py:
  setup_logger(name="historical_data_compiler") → Creates root logger

historical_data_compiler/http_client.py:
  self.logger = get_logger() → Gets "historical_data_compiler" logger

historical_data_compiler/player_data_fetcher.py:
  self.logger = get_logger() → Gets "historical_data_compiler" logger

... (all other modules get same logger)
```

**Result:** All modules log to same file (logs/historical_data_compiler/*.log)

---

## Error Handling

**Source:** Feature 01 integration + Python logging behavior

### Error Scenario 1: File Logging Setup Failure

**Trigger:** Permission denied when creating logs/historical_data_compiler/ folder

**Handling:**
- Feature 01's LineBasedRotatingHandler catches `OSError` during folder creation
- Error logged to stderr (console)
- Script continues with console-only logging
- No crash, graceful degradation

**User Impact:** No file logs created, console logs still work

**Mitigation:** Document requirement for write permissions to project root

---

### Error Scenario 2: Disk Full During Logging

**Trigger:** Disk space exhausted while writing log records

**Handling:**
- logging.FileHandler catches write failures
- Error logged to stderr (console)
- Script continues execution
- Logging resumes if space freed

**User Impact:** Some log records may be lost

**Mitigation:** User responsible for disk space management (standard logging behavior)

---

### Error Scenario 3: Missing --enable-log-file Flag

**Trigger:** User runs script without --enable-log-file flag

**Handling:**
- args.enable_log_file = False (default)
- setup_logger() called with log_to_file=False
- Feature 01's LineBasedRotatingHandler NOT instantiated
- Only console logging occurs (existing behavior)

**User Impact:** No file logs created (expected behavior)

**Mitigation:** None needed (by design per Discovery Q4)

---

### Error Scenario 4: Test Failures After Log Changes

**Trigger:** Modified log messages break test assertions

**Handling:**
- pytest fails with assertion errors
- Identify failing tests
- Update test assertions to match new log messages
- Re-run tests until 100% pass rate

**User Impact:** Implementation blocked until tests fixed

**Mitigation:** Update test assertions as part of implementation (Requirement 5)

---

## Testing Strategy

{To be defined in S4 (Epic Testing Strategy stage)}

---

## Non-Functional Requirements

**Maintainability:**
- ✅ Must follow project coding standards (CODING_STANDARDS.md)
- ✅ Must preserve existing historical_data_compiler behavior when flag not provided
- ✅ Must use clear, descriptive log messages
- ✅ Must maintain consistent logging patterns across modules
- ✅ Must keep imports organized per CODING_STANDARDS.md

**Testability:**
- ✅ All logging changes must maintain 100% test pass rate
- ✅ Test assertions must be updated to match new log messages
- ✅ Log quality changes must not break functional tests

**Performance:**
- ✅ No performance degradation from log quality improvements
- ✅ Throttled DEBUG logging in loops (every 100 iterations, not every iteration)
- ✅ No excessive string formatting in log calls (use f-strings efficiently)
- ✅ File logging disabled by default (zero overhead when flag not provided)

**Compatibility:**
- ✅ Backward compatible (existing script behavior preserved)
- ✅ New flag is optional (script works without it)
- ✅ Feature 01 integration via existing LoggingManager API

**Usability:**
- ✅ Clear help text for --enable-log-file flag
- ✅ Logs provide meaningful information for debugging
- ✅ INFO logs provide user awareness of compilation progress
- ✅ Log file location clearly communicated (help text)

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Core infrastructure changes (Feature 1)
- Other scripts' CLI integration (Features 2-5, 7)
- Console logging changes (only file logging affected)

---

## Open Questions

{To be populated during S2 deep dive - questions tracked in checklist.md}

---

## Implementation Notes

**Source:** RESEARCH_NOTES.md + Feature 01 integration contract

### Design Decisions from Discovery

1. **Direct Entry Script:**
   - compile_historical_data.py is the entry point (not a wrapper)
   - Single setup_logger() call controls all module logging
   - All modules use get_logger() to inherit logger configuration

2. **Log Quality Scope:**
   - System-wide improvements (Discovery Q6)
   - 7 modules need review: http_client, player_data_fetcher, json_exporter, weekly_snapshot_generator, team_data_calculator, game_data_fetcher, schedule_fetcher
   - Focus on DEBUG (tracing) and INFO (user awareness) levels

3. **CLI Flag Default:**
   - File logging OFF by default (Discovery Q4)
   - --enable-log-file flag explicitly enables file logging
   - Preserves existing behavior (console-only by default)

4. **Feature 01 Integration:**
   - Follow integration contracts (logger name = folder name, log_file_path=None, CLI-driven log_to_file)
   - No custom log file paths
   - Rely on Feature 01 for rotation and cleanup

### Implementation Tips

**Argument Parser:**
- Add --enable-log-file after --verbose for logical grouping
- Use action="store_true" (boolean flag, no value required)
- Clear help text mentioning log folder location

**setup_logger() Call:**
- Add log_to_file and log_file_path parameters
- Keep existing parameters unchanged (name, level)
- Preserve log_level logic (DEBUG if verbose, else INFO)

**Log Quality Changes:**
- Review modules systematically (one at a time)
- Test after each change to ensure no breakage
- Update test assertions immediately after modifying logs
- Follow throttling pattern for loop logging (every 100 iterations)

**Testing:**
- Run pytest for each module after log changes
- Fix failing test assertions before moving to next module
- Final test run must show 100% pass rate

### Code Organization

**File Structure:**
```
compile_historical_data.py              # MODIFY: Add flag, modify setup_logger call
historical_data_compiler/
├── http_client.py                      # MODIFY: Add INFO log for config
├── player_data_fetcher.py              # MODIFY: Add DEBUG log for parsing
├── game_data_fetcher.py                # MODIFY: Add DEBUG log, consider level change
├── schedule_fetcher.py                 # MODIFY: Consider level change
├── json_exporter.py                    # NO CHANGES (already good)
├── weekly_snapshot_generator.py        # NO CHANGES (already good)
├── team_data_calculator.py             # NO CHANGES (already good)
└── ...

tests/historical_data_compiler/
├── test_weekly_snapshot_generator.py   # MODIFY: Update assertions
├── test_game_data_fetcher.py           # MODIFY: Update assertions
└── test_team_data_calculator.py        # MODIFY: Update assertions
```

**Import Dependencies:**
```python
# compile_historical_data.py (existing imports):
from utils.LoggingManager import setup_logger, get_logger

# No new imports needed (all from Feature 01)
```

### Acceptance Criteria Cross-Reference

All functional requirements map to acceptance criteria:

| Requirement | Test Coverage | Implementation Location |
|-------------|---------------|-------------------------|
| Req 1: CLI Flag Integration | Manual testing | compile_historical_data.py lines 87-94, 260-264 |
| Req 2: setup_logger() Integration | Manual testing | compile_historical_data.py lines 260-264 |
| Req 3: Log Quality - DEBUG | test_*.py assertions | historical_data_compiler/*.py (various locations) |
| Req 4: Log Quality - INFO | test_*.py assertions | historical_data_compiler/*.py (various locations) |
| Req 5: Test Assertion Updates | pytest 100% pass | tests/historical_data_compiler/test_*.py |

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
| 2026-02-06 | Secondary Agent E | Complete spec draft with all requirements, technical details, integration points, error handling, and implementation notes | S2.P1.I1 (Feature-Level Discovery - research complete) |
| 2026-02-06 | Secondary Agent E | Incorporated all 7 user answers from checklist, passed Gate 2 (Spec-to-Epic Alignment), passed Gate 3 (User Approval) | S2.P1.I3 (Refinement & Alignment - complete) |
| 2026-02-08 12:20 | Agent | Updated setup_logger() signature, type hints, return type, filename formats based on Feature 01 actual implementation | S8.P1 (Cross-Feature Alignment - Feature 01 complete) |
