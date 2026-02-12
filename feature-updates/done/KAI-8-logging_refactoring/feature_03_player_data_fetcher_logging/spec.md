# Feature Specification: player_data_fetcher_logging

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 03
**Created:** 2026-02-06
**Last Updated:** 2026-02-06 21:25

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 3: player_data_fetcher_logging**

**Purpose:** CLI integration and log quality improvements for player data fetcher script

**Scope:**
- Add --enable-log-file flag to run_player_fetcher.py (subprocess wrapper)
- Forward flag using sys.argv[1:] to player_data_fetcher.py
- Apply DEBUG/INFO quality criteria to player-data-fetcher/ modules
- Update affected test assertions

**Dependencies:** Feature 1 (core infrastructure)

### Relevant Discovery Decisions

- **Solution Approach:** Subprocess wrapper uses sys.argv[1:] forwarding (same as Feature 2)
- **Key Constraints:**
  - Must preserve existing script behavior when flag not provided
  - Subprocess wrapper must forward CLI arguments to target script
  - Log quality improvements must not break functionality
- **Implementation Order:** After Feature 1 (depends on LineBasedRotatingHandler)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q3: Log quality criteria | Agent to propose criteria | Must apply DEBUG (tracing) and INFO (user awareness) criteria from Iteration 3 |
| Q4: CLI flag default | File logging OFF by default | Flag must explicitly enable file logging, users opt-in |
| Q5: Script coverage | Just those 6 scripts for now | Confirms player-data-fetcher in scope |
| Q6: Log quality scope | System-wide (Option B) | Affects player-data-fetcher/ modules |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 1 identified run_player_fetcher.py as subprocess wrapper (similar pattern to league_helper)
- **Based on User Answer:** Q5 explicitly includes player-data-fetcher in scope
- **Based on Finding:** Iteration 3 proposed DEBUG/INFO criteria that guide log quality improvements

---

## Feature Overview

**What:** Add CLI flag control for file logging and improve log quality in player data fetcher modules

**Why:** Enables users to control file logging for player data fetching, improves debugging and runtime awareness

**Who:** Users running player data fetcher to collect API data

---

## Functional Requirements

**Source:** Epic requirement + Discovery Q3, Q4, Q5, Q6 + RESEARCH_NOTES.md

### Requirement 1: Subprocess Wrapper CLI Flag Integration

**Source:** Epic requirement "CLI argument to toggle file logging" + Discovery Iteration 5

**Description:**
Add `--enable-log-file` CLI flag to `run_player_fetcher.py` (subprocess wrapper) that forwards all command-line arguments to `player_data_fetcher_main.py` using `sys.argv[1:]` pattern. The wrapper script must preserve all arguments and pass them to the subprocess without modification.

**Acceptance Criteria:**
- ✅ run_player_fetcher.py accepts `--enable-log-file` flag (optional, boolean)
- ✅ Flag forwards to player_data_fetcher_main.py via subprocess
- ✅ Uses `sys.argv[1:]` to forward ALL arguments (not just --enable-log-file)
- ✅ Subprocess wrapper uses argparse to parse arguments (for help text consistency)
- ✅ Unknown arguments forwarded without error (allows future flag additions)
- ✅ Backward compatible: running without flag works identically to current behavior
- ✅ Help text available: `python run_player_fetcher.py --help`
- ✅ Help text is simple: "Enable file logging to logs/player_data_fetcher/" (User Answer Q2)

**Example:**
```bash
# Without flag (console logging only, existing behavior)
python run_player_fetcher.py

# With flag (file logging enabled)
python run_player_fetcher.py --enable-log-file

# Future flags forwarded correctly
python run_player_fetcher.py --enable-log-file --some-future-flag value
```

**Implementation:**
```python
# run_player_fetcher.py additions
import argparse

parser = argparse.ArgumentParser(description='Run player data fetcher')
parser.add_argument('--enable-log-file', action='store_true',
                    help='Enable file logging to logs/player_data_fetcher/')
# Parse known args, forward all args including unknown ones
args, unknown_args = parser.parse_known_args()

# Forward ALL arguments via sys.argv[1:]
result = subprocess.run([
    sys.executable,
    "player_data_fetcher_main.py"
] + sys.argv[1:], check=True)  # Forward sys.argv[1:] directly
```

**User Answer:** Q4 (file logging OFF by default, CLI flag enables)

---

### Requirement 2: Main Script CLI Flag Integration

**Source:** Epic requirement "CLI argument to toggle file logging" + Feature 01 integration contract

**Description:**
Add argparse support to `player_data_fetcher_main.py` to accept `--enable-log-file` flag. Wire flag value to `setup_logger()` call, replacing config.py constant `LOGGING_TO_FILE`. Follow Feature 01 integration contracts: logger name = "player_data_fetcher", log_file_path=None (auto-generated).

**Acceptance Criteria:**
- ✅ player_data_fetcher_main.py accepts `--enable-log-file` flag via argparse
- ✅ Flag wired to setup_logger() `log_to_file` parameter
- ✅ Logger name = "player_data_fetcher" (creates logs/player_data_fetcher/ folder)
- ✅ log_file_path=None (let LoggingManager auto-generate path)
- ✅ Config.py LOGGING_TO_FILE removed (flag is sole control)
- ✅ Help text documents flag: `python player_data_fetcher_main.py --help`
- ✅ Help text is simple: "Enable file logging to logs/player_data_fetcher/" (User Answer Q2)
- ✅ Default behavior: file logging OFF (aligns with Q4 decision)

**Example:**
```python
# player_data_fetcher_main.py modifications
import argparse

# Add after imports
parser = argparse.ArgumentParser(description='Collect NFL player projections from ESPN')
parser.add_argument('--enable-log-file', action='store_true',
                    help='Enable file logging to logs/player_data_fetcher/')
args = parser.parse_args()

# Modify setup_logger() call (line 540)
logger = setup_logger(
    name="player_data_fetcher",  # Logger name = folder name
    level=LOGGING_LEVEL,          # From config
    log_to_file=args.enable_log_file,  # From CLI flag (not config.py)
    log_file_path=None,           # Auto-generated (Feature 01 contract)
    log_format=LOGGING_FORMAT      # From config
)
# Result when flag used: logs/player_data_fetcher/player_data_fetcher-{timestamp}.log
```

**User Answer:** Q4 (file logging OFF by default, CLI flag enables)

---

### Requirement 3: Log Quality Improvements - DEBUG Level

**Source:** Discovery Iteration 3 (log quality criteria) + User Answer Q6 (system-wide improvements)

**Description:**
Improve DEBUG-level logs across all player-data-fetcher/ modules to follow quality criteria: function entry/exit for complex flows, data transformations with before/after values, conditional branch tracking. Remove excessive logging (variable assignments, tight loops).

**Acceptance Criteria:**
- ✅ Function entry/exit logs for complex flows only (API calls, data processing)
- ✅ Data transformation logs show before/after values (e.g., "ESPN data → FantasyPlayer")
- ✅ Conditional branch logs indicate which path taken (e.g., "Using cache", "Fetching fresh data")
- ❌ NO logging for every variable assignment
- ❌ NO logging inside tight loops without throttling (e.g., per-player iterations)
- ✅ DEBUG logs useful for troubleshooting API issues, data mismatches

**Modules to Review:**
1. espn_client.py - API calls, retries (User Answer Q5: remove rate limit delay logs)
2. player_data_exporter.py - Export transformations
3. player_data_fetcher_main.py - Main workflow
4. game_data_fetcher.py - Game data API calls
5. coordinates_manager.py - Coordinate lookups
6. fantasy_points_calculator.py - Points calculations
7. progress_tracker.py - Progress updates (User Answer Q4: keep existing frequency of every 10 players)

**Example Improvements:**
```python
# BEFORE (excessive):
logger.debug(f"player_name = {player.name}")  # Every variable assignment
logger.debug(f"Processing player {i}")  # Inside tight loop
logger.debug(f"Rate limiting: waiting {delay}s")  # Every API delay (300+ logs)

# AFTER (targeted):
logger.debug(f"Fetching projections for {len(players)} players from ESPN API")
logger.debug(f"Data transformation: ESPN format → FantasyPlayer (before: {espn_data}, after: {player})")
logger.debug(f"Cache hit for player {player_id}, using cached data")
# Rate limit logs removed (User Answer Q5: expected behavior, not useful for debugging)
```

**User Answer:** Q3 (agent proposes criteria), Q6 (system-wide improvements)

---

### Requirement 4: Log Quality Improvements - INFO Level

**Source:** Discovery Iteration 3 (log quality criteria) + User Answer Q6 (system-wide improvements)

**Description:**
Improve INFO-level logs to provide high-level user awareness: script start/complete, major phase transitions, significant outcomes. Remove implementation details (move to DEBUG).

**Acceptance Criteria:**
- ✅ Script start log includes configuration (season, scoring format, output settings)
- ✅ Major phase transitions logged (e.g., "Collecting season projections", "Exporting data")
- ✅ Significant outcomes logged (e.g., "Collected 150 players", "Exported to 3 formats")
- ❌ NO implementation details at INFO level (move to DEBUG)
- ❌ NO per-function call logs at INFO level
- ✅ INFO logs provide user with runtime awareness and progress

**Example Improvements:**
```python
# BEFORE (too detailed):
logger.info(f"Calling _get_api_client()")  # Implementation detail
logger.info(f"Setting self.exporter")  # Implementation detail

# AFTER (user-focused):
logger.info("Starting NFL projections collection with ESPN API")
logger.info(f"Collecting season projections for {settings.season} season")
logger.info(f"Collected {len(season_projections)} season projections")
logger.info(f"Exported projections to {len(output_files)} files")
logger.info("Data collection completed successfully")
```

**User Answer:** Q3 (agent proposes criteria), Q6 (system-wide improvements)

---

### Requirement 5: Config.py Constants Removal

**Source:** Feature 01 integration (replaces config.py LOGGING_FILE path) + User Answer Q1

**Description:**
Remove LOGGING_TO_FILE and LOGGING_FILE constants from config.py entirely. These are replaced by the --enable-log-file CLI flag and Feature 01's auto-generated paths. Update any tests that reference these constants to use the new CLI flag pattern.

**Acceptance Criteria:**
- ✅ LOGGING_TO_FILE constant removed from config.py (line 52)
- ✅ LOGGING_FILE constant removed from config.py (line 54)
- ✅ Tests updated to not reference removed constants
- ✅ CLI flag is the sole control for file logging behavior

**Example:**
```python
# config.py - BEFORE (lines 51-55):
LOGGING_LEVEL = 'INFO'
LOGGING_TO_FILE = False        # ← REMOVE
LOG_NAME = "player_data_fetcher"
LOGGING_FILE = './data/log.txt'  # ← REMOVE
LOGGING_FORMAT = 'standard'

# config.py - AFTER:
LOGGING_LEVEL = 'INFO'
LOG_NAME = "player_data_fetcher"
LOGGING_FORMAT = 'standard'
```

**User Decision (Q1):** Option B - Remove constants entirely (cleaner API, tests will be updated)

---

## Technical Requirements

**Source:** RESEARCH_NOTES.md (subprocess wrapper pattern, argparse usage)

### Subprocess Wrapper Argument Forwarding

**Pattern:** `sys.argv[1:]` forwarding (standard subprocess wrapper pattern)

**Rationale:** Subprocess wrappers should be transparent - all CLI arguments forwarded to target script without modification. This allows future flag additions without wrapper changes.

**Implementation:**
```python
# run_player_fetcher.py
import subprocess
import sys

# Parse wrapper-specific args (for help text), but forward ALL args
parser = argparse.ArgumentParser()
parser.add_argument('--enable-log-file', action='store_true')
args, unknown_args = parser.parse_known_args()

# Forward sys.argv[1:] directly (includes known + unknown args)
result = subprocess.run([
    sys.executable,
    "player_data_fetcher_main.py"
] + sys.argv[1:], check=True)
```

**Benefits:**
- Future-proof: New flags work without wrapper modification
- Transparent: Wrapper doesn't interpret/filter arguments
- Consistent: Same pattern as other subprocess wrappers (league_helper)

---

### Argparse Integration

**Module:** `player_data_fetcher_main.py`

**Flag Definition:**
```python
parser = argparse.ArgumentParser(description='Collect NFL player projections from ESPN')
parser.add_argument('--enable-log-file', action='store_true',
                    help='Enable file logging to logs/player_data_fetcher/')
args = parser.parse_args()
```

**Integration with setup_logger:**
```python
logger = setup_logger(
    name="player_data_fetcher",  # Constant (matches LOG_NAME from config)
    level=LOGGING_LEVEL,          # From config.py
    log_to_file=args.enable_log_file,  # From argparse (not config)
    log_file_path=None,           # Auto-generated (Feature 01 contract)
    log_format=LOGGING_FORMAT      # From config.py
)
```

**Key Decisions:**
- `log_to_file` parameter controlled by CLI flag (overrides config.py LOGGING_TO_FILE)
- `name` parameter = "player_data_fetcher" (consistent with config LOG_NAME)
- `log_file_path` = None (Feature 01 auto-generates path)

---

### Log Quality Review Approach

**Strategy:** Targeted review of existing logger calls (not comprehensive rewrite)

**Process:**
1. Search for all `logger.debug()` and `logger.info()` calls in player-data-fetcher/
2. Categorize each call against quality criteria
3. Improve/remove calls that violate criteria
4. Add missing logs for major phases (if gaps found)

**Modules to Review (7 total):**
- espn_client.py (API client, rate limiting, retries)
- player_data_exporter.py (data export, file creation)
- player_data_fetcher_main.py (main workflow, collectors)
- game_data_fetcher.py (game data API)
- coordinates_manager.py (coordinate lookups)
- fantasy_points_calculator.py (points calculations)
- progress_tracker.py (progress updates)

**Estimated Effort:** 20-30 lines of log improvements across 7 modules

---

### Feature 01 Integration Contracts

**Contract 1: Logger Name = Folder Name**
- Use "player_data_fetcher" as logger name
- Creates logs/player_data_fetcher/ folder
- Consistent with config LOG_NAME constant

**Contract 2: log_file_path=None**
- Do NOT specify custom log file path
- Let LoggingManager auto-generate path in logs/ folder
- Config LOGGING_FILE path deprecated (no longer used)

**Contract 3: log_to_file from CLI**
- Wire --enable-log-file flag to log_to_file parameter
- Default False (file logging OFF unless flag provided)
- Aligns with Q4 user decision

---

## Integration Points

### Integration with Feature 1 (Core Infrastructure)

**Direction:** This feature consumes FROM Feature 1

**Data Consumed:**
- **LineBasedRotatingHandler:** Custom logging handler (via LoggingManager)
- **Modified setup_logger():** Same signature, new behavior when log_to_file=True
- **logs/ folder structure:** Auto-created logs/player_data_fetcher/ folder

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

**Feature 03 Usage:**
```python
from utils.LoggingManager import setup_logger

logger = setup_logger(
    name="player_data_fetcher",       # Creates logs/player_data_fetcher/
    level="INFO",                      # Log level
    log_to_file=args.enable_log_file,  # From CLI flag
    log_file_path=None,                # Auto-generated by LoggingManager
    log_format="standard"               # Format style
    # enable_console=True (default, can omit)
    # max_file_size, backup_count (optional, can omit)
)
# Result:
#   Initial file: logs/player_data_fetcher/player_data_fetcher-{YYYYMMDD_HHMMSS}.log
#   Rotated files: logs/player_data_fetcher/player_data_fetcher-{YYYYMMDD_HHMMSS_microseconds}.log
```

**Note:** Updated based on feature_01 actual implementation. The enable_console, max_file_size, and backup_count parameters are optional. Rotated files include microsecond precision to prevent timestamp collisions.

**Dependency:**
- Feature 01 must be COMPLETE before Feature 03 implementation
- Feature 01 spec used as reference for integration contracts
- Group 2 features (including Feature 03) all depend on Feature 01

---

### Integration with Python subprocess Module

**Direction:** run_player_fetcher.py interacts WITH subprocess module

**Pattern:** Subprocess wrapper with argument forwarding

**Implementation:**
```python
import subprocess
import sys

# Forward all arguments to main script
result = subprocess.run([
    sys.executable,                # Current Python interpreter
    "player_data_fetcher_main.py"  # Main script
] + sys.argv[1:], check=True)      # Forward all CLI arguments
```

**Error Handling:**
- CalledProcessError raised if main script exits with non-zero code
- Wrapper exits with same return code (preserves exit status)
- Existing error handling preserved (no changes needed)

---

### Integration with Existing Tests

**Direction:** Feature modifications may affect test assertions

**Test Files (search needed):**
- tests/player-data-fetcher/ folder
- Likely files: test_player_data_fetcher_main.py, test_espn_client.py, etc.

**Potential Test Updates:**
- Log file path assertions (if tests check file paths)
- Handler type assertions (if tests check handler type)
- Most tests likely unaffected (don't assert on logger internals)

**Strategy:**
- Run existing tests FIRST to identify failures
- Update only failing tests (minimal changes) (User Answer Q6)
- No preemptive test modifications

---

## Error Handling

**Source:** Existing subprocess wrapper error handling + Feature 01 error handling (inherited)

### Scenario 1: Invalid CLI Flag Usage

**Trigger:** User provides invalid flag (e.g., `--invalid-flag`)

**Handling:**
- argparse raises error and displays usage message
- Script exits with non-zero code
- Standard argparse behavior (no custom handling needed)

**User Impact:** Clear error message explaining flag usage

**Example:**
```bash
$ python run_player_fetcher.py --invalid-flag
usage: run_player_fetcher.py [-h] [--enable-log-file]
run_player_fetcher.py: error: unrecognized arguments: --invalid-flag
```

---

### Scenario 2: Subprocess Failure (Main Script Error)

**Trigger:** player_data_fetcher_main.py exits with non-zero code

**Handling:**
- subprocess.run() with check=True raises CalledProcessError
- run_player_fetcher.py catches exception (existing code, line 41)
- Wrapper exits with same return code as main script

**User Impact:** Error message preserved from main script

**Existing Code:**
```python
except subprocess.CalledProcessError as e:
    print(f"Error running player data fetcher: {e}")
    sys.exit(e.returncode)  # Preserve exit code
```

**No changes needed** - existing error handling sufficient

---

### Scenario 3: File Logging Errors (Permission Denied, Disk Full)

**Trigger:** Cannot create logs/ folder or write log file

**Handling:**
- Inherited from Feature 01 (LineBasedRotatingHandler error handling)
- Error logged to stderr via FileHandler.handleError()
- Script continues with console logging only
- No crash (graceful degradation)

**User Impact:** Console logging unaffected, file logging fails silently

**Mitigation:** Document requirement for write permissions to project root

---

### Scenario 4: Missing Feature 01 (LineBasedRotatingHandler Not Found)

**Trigger:** Feature 03 implemented before Feature 01 complete

**Handling:**
- ImportError raised when importing LineBasedRotatingHandler
- Script crashes with clear error message
- **Prevention:** Feature dependencies enforced in S1 (Feature 03 after Feature 01)

**User Impact:** N/A (prevented by workflow)

**Mitigation:** S1 dependency tracking prevents this scenario

---

## Testing Strategy

{To be defined in S4 (Epic Testing Strategy stage)}

---

## Non-Functional Requirements

**Performance:**
- ✅ No performance impact when --enable-log-file flag NOT used (console logging unchanged)
- ✅ Minimal overhead when flag used (inherits LineBasedRotatingHandler performance from Feature 01)
- ✅ Log quality improvements must not add overhead in tight loops
- ✅ Argument parsing overhead negligible (<1ms)

**Backward Compatibility:**
- ✅ Running without --enable-log-file must work identically to current behavior
- ✅ No breaking changes to script interface
- ✅ Existing tests must pass (or require minimal updates)
- ✅ Config.py constants removed entirely per user decision Q1 (tests will be updated)

**Maintainability:**
- ✅ Must follow project coding standards (CODING_STANDARDS.md)
- ✅ Must preserve existing player-data-fetcher behavior (no functional changes)
- ✅ Must use type hints for new code (argparse args handling)
- ✅ Must include docstring updates for modified functions
- ✅ Log improvements must improve readability (not add noise)

**Usability:**
- ✅ CLI flag must be self-documenting via --help
- ✅ Flag name consistent across all scripts (--enable-log-file)
- ✅ Default behavior intuitive (file logging OFF by default)
- ✅ Log folder location discoverable (logs/ at project root)

**Testability:**
- ✅ CLI flag behavior testable via subprocess calls
- ✅ Log quality improvements testable via log assertions
- ✅ Existing test suite must pass (with minimal updates if needed)

**Compatibility:**
- ✅ Python 3.8+ compatibility (use argparse, subprocess from stdlib)
- ✅ Cross-platform compatibility (Windows, macOS, Linux)
- ✅ No new external dependencies

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Core infrastructure changes (Feature 1)
- Other scripts' CLI integration (Features 2, 4-7)
- Console logging changes (only file logging affected)

---

## Open Questions

{To be populated during S2 deep dive - questions tracked in checklist.md}

---

## Implementation Notes

**Source:** RESEARCH_NOTES.md + Discovery findings

### Design Decisions from Discovery

1. **Subprocess Wrapper Argument Forwarding:**
   - ✅ Use sys.argv[1:] pattern (not manual argument construction)
   - **Rationale:** Future-proof, transparent, consistent with league_helper pattern
   - **Alternative Rejected:** Manually constructing argument list (fragile, requires wrapper updates for new flags)

2. **CLI Flag Naming:**
   - ✅ Use `--enable-log-file` (consistent across all Features 2-7)
   - **Rationale:** Clear intent, aligns with user decision Q4 (opt-in behavior)
   - **Alternative Rejected:** `--disable-log-file` (inverted logic, confusing default)

3. **Config.py Constants Removal:**
   - ✅ Remove constants (LOGGING_TO_FILE, LOGGING_FILE) entirely
   - **Rationale:** Cleaner API, CLI flag is sole control, tests will be updated (User Answer Q1: Option B)
   - **Alternative Rejected:** Keep constants with deprecation comments (incomplete migration, confusing dual control)

4. **Log Quality Improvement Scope:**
   - ✅ Targeted review (improve existing logs, don't rewrite everything)
   - **Rationale:** Minimize risk, focus on high-value improvements
   - **Alternative Rejected:** Comprehensive logging rewrite (high risk, low benefit)

5. **Argparse vs Manual Parsing:**
   - ✅ Use argparse in both wrapper and main script
   - **Rationale:** Standard library, provides --help for free, extensible
   - **Alternative Rejected:** Manual sys.argv parsing (no --help, error-prone)

---

### Implementation Tips

**Subprocess Wrapper (run_player_fetcher.py):**
- Add argparse BEFORE subprocess.run() call
- Use `parse_known_args()` (allows unknown flags to forward)
- Forward `sys.argv[1:]` directly (don't reconstruct from parsed args)
- Preserve existing try/except error handling (User Answer Q3: no changes needed)

**Main Script (player_data_fetcher_main.py):**
- Add argparse at module level (before async main() function)
- Move to setup_logger() call (line 540) - replace LOGGING_TO_FILE with args.enable_log_file
- Use `log_file_path=None` (Feature 01 contract)
- Logger name = "player_data_fetcher" (consistent with LOG_NAME)

**Log Quality Review:**
- Search for `logger.debug(` and `logger.info(` in each module
- For each call, ask: Does this meet quality criteria?
- Improve/remove violations, add missing phase transition logs
- Test after changes (ensure no functional impact)

**Testing:**
- Run existing tests FIRST (identify baseline)
- Make feature changes
- Run tests again (identify failures)
- Update failing tests (minimal changes)
- Ensure 100% test pass rate before commit

---

### Code Organization

**Files to Modify:**
1. `run_player_fetcher.py` (lines 18-39: add argparse, forward sys.argv)
2. `player-data-fetcher/player_data_fetcher_main.py` (lines 540-541: add argparse, wire flag)
3. `player-data-fetcher/config.py` (lines 52-54: remove LOGGING_TO_FILE and LOGGING_FILE constants)
4. `player-data-fetcher/espn_client.py` (review logger calls)
5. `player-data-fetcher/player_data_exporter.py` (review logger calls)
6. `player-data-fetcher/game_data_fetcher.py` (review logger calls)
7. `player-data-fetcher/coordinates_manager.py` (review logger calls)
8. `player-data-fetcher/fantasy_points_calculator.py` (review logger calls)
9. `player-data-fetcher/progress_tracker.py` (review logger calls)
10. `tests/player-data-fetcher/*` (update if needed based on test failures)

**No New Files Created:** All modifications to existing files

---

### Gotchas

**Gotcha 1: Forgetting to Forward Unknown Args**
- **Issue:** wrapper only forwards --enable-log-file, drops other flags
- **Impact:** Future flags don't work (e.g., hypothetical --season flag)
- **Mitigation:** Use `sys.argv[1:]` directly, not reconstructed args

**Gotcha 2: Using config.py LOGGING_TO_FILE After Flag Added**
- **Issue:** CLI flag ignored if config constant still used in setup_logger()
- **Impact:** User provides --enable-log-file but file logging doesn't enable
- **Mitigation:** Replace LOGGING_TO_FILE with args.enable_log_file

**Gotcha 3: Specifying log_file_path in setup_logger()**
- **Issue:** Violates Feature 01 integration contract
- **Impact:** Logs written to wrong location (not logs/player_data_fetcher/)
- **Mitigation:** Use log_file_path=None (auto-generated)

**Gotcha 4: Inconsistent Logger Name**
- **Issue:** Using different logger name than "player_data_fetcher"
- **Impact:** Folder created with wrong name (e.g., logs/pdf/ instead of logs/player_data_fetcher/)
- **Mitigation:** Match LOG_NAME constant from config.py

**Gotcha 5: Adding Logs Inside Tight Loops**
- **Issue:** DEBUG logs inside per-player loop (1000+ iterations)
- **Impact:** Performance degradation, log spam
- **Mitigation:** Throttle logs (e.g., every 10 players) or move to outer scope

**Gotcha 6: Removing Existing Phase Transition Logs**
- **Issue:** Overzealous log cleanup removes valuable user awareness logs
- **Impact:** Users lose visibility into script progress
- **Mitigation:** Preserve existing INFO logs for major phases, improve clarity

---

### Acceptance Criteria Cross-Reference

All functional requirements map to acceptance criteria:

| Requirement | Test Coverage | Implementation Location |
|-------------|---------------|-------------------------|
| Req 1: Subprocess Wrapper CLI | Manual test: python run_player_fetcher.py --enable-log-file | run_player_fetcher.py lines 18-39 |
| Req 2: Main Script CLI | Manual test: python player_data_fetcher_main.py --enable-log-file | player_data_fetcher_main.py lines 537-545 |
| Req 3: DEBUG Level Quality | Code review + smoke test | player-data-fetcher/*.py (7 modules) |
| Req 4: INFO Level Quality | Code review + smoke test | player-data-fetcher/*.py (7 modules) |
| Req 5: Config Deprecation | Manual verification | config.py lines 52-54 |

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
| 2026-02-06 21:25 | Secondary-B | Complete spec draft with all requirements, acceptance criteria, technical details, integration points, error handling, and implementation notes | S2.P1.I1 (Feature-Level Discovery - research complete) |
| 2026-02-06 21:50 | Secondary-B | Spec finalized with all user answers incorporated (6 questions), Gate 3 approved | S2.P1.I3 (Refinement & Alignment - user approval complete) |
| 2026-02-08 12:05 | Agent | Updated setup_logger() signature, type hints, return type, filename formats based on Feature 01 actual implementation | S8.P1 (Cross-Feature Alignment - Feature 01 complete) |
