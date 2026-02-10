# Feature Specification: league_helper_logging

**Part of Epic:** KAI-8-logging_refactoring
**Feature Number:** 02
**Created:** 2026-02-06
**Last Updated:** 2026-02-06 21:30

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 2: league_helper_logging**

**Purpose:** CLI integration and log quality improvements for league helper script

**Scope:**
- Add --enable-log-file flag to run_league_helper.py (subprocess wrapper)
- Add --enable-log-file flag to league_helper/LeagueHelperManager.py (main entry)
- Forward flag using sys.argv[1:] from wrapper to target script
- Apply DEBUG/INFO quality criteria to league_helper/ modules (316 calls across 17 files)
- Review and improve logs in all mode managers and utility managers
- Update affected test assertions (if any exist)

**Dependencies:** Feature 1 (core infrastructure) - ✅ COMPLETE (spec available)

### Relevant Discovery Decisions

- **Solution Approach:** Subprocess wrapper uses sys.argv[1:] forwarding (Option B from Iteration 5)
- **Key Constraints:**
  - Must preserve existing script behavior when flag not provided
  - Subprocess wrapper must forward CLI arguments to target script
  - Log quality improvements must not break functionality
  - File logging OFF by default (opt-in via --enable-log-file)
- **Implementation Order:** After Feature 1 (depends on LineBasedRotatingHandler)

### Relevant User Answers (from Discovery)

| Question | Answer | Impact on This Feature |
|----------|--------|----------------------|
| Q3: Log quality criteria | Agent proposed criteria (Iteration 3) | Must apply DEBUG (tracing) and INFO (user awareness) criteria to all 316 logger calls |
| Q4: CLI flag default | File logging OFF by default | --enable-log-file flag enables file logging, users must opt-in |
| Q6: Log quality scope | System-wide (Option B) | Affects league_helper/ modules AND shared utilities used by league_helper (all 17 files) |

### Discovery Basis for This Feature

- **Based on Finding:** Iteration 1 identified run_league_helper.py as subprocess wrapper requiring sys.argv[1:] forwarding
- **Based on Finding:** Iteration 2 confirmed 316 logger.debug/info calls across 17 league_helper files
- **Based on User Answer:** Q6 (system-wide scope) means all 17 files need log improvements, not just main managers
- **Based on Finding:** Iteration 3 proposed DEBUG/INFO criteria that guide log quality improvements
- **Based on Finding:** run_accuracy_simulation.py provides CLI precedent for argparse integration

---

## Feature Overview

**What:** Add --enable-log-file CLI flag to league helper scripts and improve log quality across all league_helper modules

**Why:** Enables users to control file logging for league helper, improves debugging experience (DEBUG logs) and runtime awareness (INFO logs)

**Who:** Users running league helper in draft, optimizer, trade, or data editor modes via run_league_helper.py or directly via LeagueHelperManager.py

---

## Functional Requirements

**Source:** RESEARCH_NOTES.md + Feature 01 spec.md + Discovery

### Requirement 1: CLI Flag Integration (Subprocess Wrapper)

**Source:** Discovery Iteration 5 (sys.argv[1:] forwarding) + RESEARCH_NOTES.md Section 1

**Description:**
Add --enable-log-file flag to run_league_helper.py and forward all CLI arguments to the target script (league_helper/LeagueHelperManager.py) via sys.argv[1:]. This allows users to control file logging when running league helper through the subprocess wrapper.

**Acceptance Criteria:**
- ✅ run_league_helper.py imports argparse
- ✅ ArgumentParser created with description "Fantasy Football League Helper"
- ✅ --enable-log-file flag added with action='store_true', default=False
- ✅ Help text explains flag enables file logging to logs/league_helper/
- ✅ All CLI arguments forwarded to target script using sys.argv[1:]
- ✅ subprocess.run() args updated: [sys.executable, script, DATA_FOLDER] + sys.argv[1:]
- ✅ Existing behavior preserved when flag not provided (file logging OFF)

**Example:**
```bash
# User runs wrapper with flag
python run_league_helper.py --enable-log-file

# Wrapper forwards to target
subprocess.run([sys.executable, "league_helper/LeagueHelperManager.py", "./data", "--enable-log-file"])
```

**User Decision Required:** See checklist.md Q1 (forward all args vs filter to known args)

---

### Requirement 2: CLI Flag Integration (Main Entry Point)

**Source:** RESEARCH_NOTES.md Section 2 + run_accuracy_simulation.py precedent

**Description:**
Add --enable-log-file flag to league_helper/LeagueHelperManager.py main() function and wire it to setup_logger()'s log_to_file parameter. This integrates with Feature 01's logging infrastructure to enable/disable file logging based on user preference.

**Acceptance Criteria:**
- ✅ LeagueHelperManager.py imports argparse
- ✅ ArgumentParser created in main() with description "Fantasy Football League Helper"
- ✅ --enable-log-file flag added with action='store_true', default=False
- ✅ Help text explains flag enables file logging to logs/league_helper/ with 500-line rotation, max 50 files
- ✅ Arguments parsed: args = parser.parse_args()
- ✅ setup_logger() call modified: log_to_file=args.enable_log_file (replaces constants.LOGGING_TO_FILE)
- ✅ setup_logger() call modified: log_file_path=None (let Feature 01 auto-generate)
- ✅ Existing behavior preserved when flag not provided (file logging OFF, default from arg default=False)

**Example:**
```python
# Before (LeagueHelperManager.py line 205):
setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL, constants.LOGGING_TO_FILE, constants.LOGGING_FILE, constants.LOGGING_FORMAT)

# After:
import argparse

def main():
    parser = argparse.ArgumentParser(description="Fantasy Football League Helper")
    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        default=False,
        help='Enable file logging (logs written to logs/league_helper/ with 500-line rotation, max 50 files)'
    )
    args = parser.parse_args()

    # Updated based on feature_01 actual implementation
    logger = setup_logger(
        constants.LOG_NAME,
        constants.LOGGING_LEVEL,
        log_to_file=args.enable_log_file,  # NEW: Use CLI flag
        log_file_path=None,  # NEW: Let Feature 01 generate path
        log_format=constants.LOGGING_FORMAT
        # enable_console=True (default, can omit)
        # max_file_size, backup_count (optional, can omit)
    )

    # Rest unchanged
    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"
    leagueHelper = LeagueHelperManager(data_path)
    leagueHelper.start_interactive_mode()
```

**Note:** setup_logger() now returns logging.Logger (not None). Feature 02 doesn't need to use the return value, but it's available if needed.

**User Decision Required:** See checklist.md Q2 (LOGGING_TO_FILE constant deprecation)

---

### Requirement 3: Log Quality - DEBUG Level

**Source:** Discovery Iteration 3 (DEBUG criteria) + RESEARCH_NOTES.md Section 5

**Description:**
Review all 316 logger.debug calls across 17 league_helper files and apply DEBUG level criteria: function entry/exit (only for complex flows), data transformations with before/after values, conditional branch taken. Remove excessive logging (every variable assignment, tight loops without throttling).

**Acceptance Criteria:**
- ✅ All 316 logger.debug/info calls audited using Discovery Iteration 3 criteria
- ✅ Each call marked KEEP/UPDATE/REMOVE based on criteria
- ✅ KEEP: Logs that meet DEBUG criteria (tracing data flow, function execution)
- ✅ UPDATE: Logs that need improvement (add context, fix format, adjust level)
- ✅ REMOVE: Excessive logs (redundant, every variable, tight loops)
- ✅ DEBUG logs provide value for developers tracing data flow
- ✅ No DEBUG logs inside tight loops without throttling
- ✅ No redundant DEBUG messages (e.g., "entering function" + "starting process" for same action)

**DEBUG Level Criteria (from Discovery Iteration 3):**
- ✅ Function entry/exit with parameters (not excessive - only for complex flows)
- ✅ Data transformations with before/after values
- ✅ Conditional branch taken (which if/else path executed)
- ❌ NOT every single variable assignment
- ❌ NOT logging inside tight loops without throttling
- ❌ NOT redundant messages

**Example KEEP (PlayerManager.py line 141):**
```python
# GOOD: Initialization with data values
self.logger.debug(f"Player Manager initialized with {len(self.players)} players, {len(self.team.roster)} on roster")
```

**Example UPDATE:**
```python
# BEFORE: Missing context
self.logger.debug("Loading data")

# AFTER: Added context and data values
self.logger.debug(f"Loading player data from {self.file_str} for week {week_num}")
```

**Example REMOVE:**
```python
# REMOVE: Every variable assignment (too verbose)
self.logger.debug(f"Setting player_id to {player_id}")
self.logger.debug(f"Setting name to {name}")
self.logger.debug(f"Setting position to {position}")
```

---

### Requirement 4: Log Quality - INFO Level

**Source:** Discovery Iteration 3 (INFO criteria) + RESEARCH_NOTES.md Section 5

**Description:**
Review all INFO-level logger.info calls and apply INFO level criteria: script start/complete with configuration, major phase transitions, significant outcomes. Remove implementation details (that's DEBUG) and every function call logging.

**Acceptance Criteria:**
- ✅ All logger.info calls (subset of 316 total) audited using Discovery Iteration 3 criteria
- ✅ INFO logs provide runtime awareness for users (not developers)
- ✅ Script start/complete messages include configuration summary
- ✅ Major phase transitions logged (e.g., "Starting draft mode", "Beginning trade analysis")
- ✅ Significant outcomes logged (e.g., "Processed 150 players", "Draft complete: 10 players selected")
- ✅ No implementation details at INFO level (moved to DEBUG)
- ✅ No technical jargon without context
- ✅ No logging every function call

**INFO Level Criteria (from Discovery Iteration 3):**
- ✅ Script start/complete with configuration
- ✅ Major phase transitions (e.g., "Starting draft mode")
- ✅ Significant outcomes (e.g., "Processed 15 players")
- ✅ User-relevant warnings (e.g., "Using cached data from yesterday")
- ❌ NOT implementation details (that's DEBUG)
- ❌ NOT every function call
- ❌ NOT technical jargon without context

**Example KEEP (LeagueHelperManager.py line 120):**
```python
# GOOD: Script start with configuration
self.logger.info(f"Interactive league helper started. Current roster size: {roster_size}/{self.config.max_players}")
```

**Example UPDATE:**
```python
# BEFORE: Implementation detail (DEBUG-level)
self.logger.info("Calling calculate_scores()")

# AFTER: Move to DEBUG or rewrite as user-facing outcome
self.logger.debug("Calculating scores for {len(players)} players")  # DEBUG version
# OR
self.logger.info(f"Scoring {len(players)} players for week {week}")  # INFO version (user-facing)
```

---

## Technical Requirements

**Source:** RESEARCH_NOTES.md + Feature 01 spec.md

### Algorithms

**No complex algorithms** - CLI flag integration is straightforward argument parsing and passing.

**Log Quality Algorithm (Manual Audit Process):**
1. Read file sequentially
2. For each logger.debug/info call:
   a. Apply DEBUG/INFO criteria checklist
   b. Mark KEEP/UPDATE/REMOVE
   c. If UPDATE, draft improved log message
   d. If REMOVE, verify no test assertions depend on it
3. Implement changes
4. Verify tests pass

---

### Data Structures

**CLI Arguments:**
- Type: argparse.Namespace
- Fields: enable_log_file (bool, default=False)

**No other data structures** - Feature primarily involves configuration changes and log message improvements.

---

### Interfaces

#### run_league_helper.py Command-Line Interface

```bash
python run_league_helper.py [--enable-log-file]

Arguments:
  --enable-log-file    Enable file logging (logs written to logs/league_helper/)

Example:
  python run_league_helper.py                    # File logging OFF (default)
  python run_league_helper.py --enable-log-file  # File logging ON
```

**Implementation Location:** run_league_helper.py lines 1-69 (add argparse before run_league_helper function)

---

#### LeagueHelperManager.py Command-Line Interface

```bash
python league_helper/LeagueHelperManager.py data_folder [--enable-log-file]

Positional Arguments:
  data_folder          Path to data directory (required, existing behavior)

Optional Arguments:
  --enable-log-file    Enable file logging (logs written to logs/league_helper/ with 500-line rotation, max 50 files)

Example:
  python league_helper/LeagueHelperManager.py ./data                    # File logging OFF
  python league_helper/LeagueHelperManager.py ./data --enable-log-file  # File logging ON
```

**Implementation Location:** league_helper/LeagueHelperManager.py main() function (lines 192-211, add argparse at beginning)

---

#### Integration with Feature 01: setup_logger()

**Call Site:** league_helper/LeagueHelperManager.py line 205

**Current Signature (unchanged):**
```python
def setup_logger(
    name: str,
    level: Union[str, int] = 'INFO',
    log_to_file: bool = False,
    log_file_path: Optional[Union[str, Path]] = None,
    log_format: str = 'standard',
    enable_console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB (kept for backward compatibility, not used)
    backup_count: int = 5  # (kept for backward compatibility, not used)
) -> logging.Logger
```

**Note:** Updated based on feature_01 actual implementation. The `enable_console`, `max_file_size`, and `backup_count` parameters were added in Feature 01 but not in the initial spec. All are optional with defaults.

**Current Call:**
```python
setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL, constants.LOGGING_TO_FILE, constants.LOGGING_FILE, constants.LOGGING_FORMAT)
```

**New Call:**
```python
setup_logger(
    constants.LOG_NAME,           # "league_helper" (matches folder name per Feature 01 contract)
    constants.LOGGING_LEVEL,       # "INFO" (unchanged)
    log_to_file=args.enable_log_file,  # From CLI flag (not constants.LOGGING_TO_FILE)
    log_file_path=None,            # Let Feature 01 auto-generate logs/league_helper/league_helper-{timestamp}.log
    log_format=constants.LOGGING_FORMAT,  # "detailed" (unchanged)
    enable_console=True,           # Keep console output (default, can omit)
    # max_file_size and backup_count kept for backward compatibility (not used by LineBasedRotatingHandler)
)
```

**Note:** Updated based on feature_01 actual implementation. The `enable_console`, `max_file_size`, and `backup_count` parameters are optional and can be omitted.

**Contract Compliance:**
- ✅ Logger name = "league_helper" (matches folder name logs/league_helper/)
- ✅ log_file_path=None (Feature 01 generates logs/league_helper/league_helper-{timestamp}.log)
- ✅ log_to_file from CLI (args.enable_log_file)

---

## Integration Points

### Integration with Feature 1 (Core Infrastructure)

**Direction:** This feature consumes FROM Feature 1

**Data Passed:**
- **Class:** LineBasedRotatingHandler (used internally by Feature 01's setup_logger())
- **API:** setup_logger() function (existing signature, new log_to_file source)
- **Folder Structure:** logs/league_helper/ (auto-created by Feature 01 handler)

**Interface:**

League helper calls setup_logger() with same signature as before:
```python
from utils.LoggingManager import setup_logger

setup_logger(
    name="league_helper",           # Script name (used for folder structure)
    level="INFO",                    # Log level
    log_to_file=args.enable_log_file,  # NEW: From CLI flag (not hardcoded constant)
    log_file_path=None,              # NEW: Auto-generated by Feature 01 (not constants.LOGGING_FILE)
    log_format="detailed"            # Format style
)
# Result: LineBasedRotatingHandler created by Feature 01, logs to logs/league_helper/league_helper-{timestamp}.log
```

**Example Flow:**
```
User runs: python run_league_helper.py --enable-log-file
  ↓
run_league_helper.py forwards flag to LeagueHelperManager.py
  ↓
LeagueHelperManager.main() parses --enable-log-file
  ↓
main() calls setup_logger(name="league_helper", log_to_file=True, log_file_path=None)
  ↓
Feature 01's setup_logger() creates LineBasedRotatingHandler
  ↓
Handler creates logs/league_helper/ folder
  ↓
Initial file: logs/league_helper/league_helper-20260206_143522.log
  ↓
After 500 lines, rotates to: league_helper-20260206_143525_123456.log (with microseconds)
  ↓
Max 50 files enforced (oldest deleted when 51st created)
```

**Note:** Updated based on feature_01 actual implementation. Rotated files include microsecond precision to prevent timestamp collisions during rapid rotation.

**Key Contracts (from Feature 01 actual implementation):**
1. **Logger name = folder name:** league helper uses "league_helper" (not "LeagueHelper" or variations)
2. **log_file_path=None:** Don't specify custom paths (let Feature 01 generate)
3. **log_to_file driven by CLI:** Wire --enable-log-file flag to log_to_file parameter
4. **Filename formats:**
   - Initial file: {logger_name}-{YYYYMMDD_HHMMSS}.log
   - Rotated files: {logger_name}-{YYYYMMDD_HHMMSS_microseconds}.log
5. **Optional parameters:** enable_console, max_file_size, backup_count available but optional (have defaults)

---

### Integration with Subprocess Wrapper

**Direction:** run_league_helper.py calls league_helper/LeagueHelperManager.py

**Data Passed:**
- **Positional arg:** DATA_FOLDER (existing, unchanged)
- **CLI args:** sys.argv[1:] (new, forwarded to target)

**Flow:**
```
run_league_helper.py receives: --enable-log-file
  ↓
Parses args (optional, pending Q1)
  ↓
Forwards to subprocess: subprocess.run([sys.executable, script, DATA_FOLDER] + sys.argv[1:])
  ↓
LeagueHelperManager.py receives: ["./data", "--enable-log-file"]
  ↓
Parses args, uses flag
```

**User Decision Required:** See checklist.md Q1 (forward all args vs parse and filter)

---

### Integration with Logging Constants

**Direction:** LeagueHelperManager.py reads FROM league_helper/constants.py

**Data Consumed:**
- constants.LOG_NAME = "league_helper" (still used)
- constants.LOGGING_LEVEL = "INFO" (still used)
- constants.LOGGING_FORMAT = "detailed" (still used)
- constants.LOGGING_TO_FILE = False (REMOVED - replaced by CLI flag)
- constants.LOGGING_FILE = './data/log.txt' (NO LONGER USED, Feature 01 auto-generates)

**User Decision (Q2):** Remove LOGGING_TO_FILE constant entirely

---

## Error Handling

**Source:** RESEARCH_NOTES.md + standard argparse behavior

### Error Scenario 1: Invalid CLI Arguments

**Trigger:** User provides unknown argument (e.g., --enable-log --verbose)

**Handling:**
- argparse automatically prints usage and exits with error
- Error message: "unrecognized arguments: --verbose"
- Exit code: 2

**User Impact:** Clear error message, script doesn't run

**Mitigation:** None needed (standard argparse behavior)

---

### Error Scenario 2: Flag Provided But Feature 01 Not Implemented

**Trigger:** User runs with --enable-log-file but Feature 01's LineBasedRotatingHandler doesn't exist

**Handling:**
- setup_logger() call fails with ImportError
- Error message: "No module named 'utils.LineBasedRotatingHandler'"
- Script exits

**User Impact:** Script fails to start

**Mitigation:** Feature 01 is prerequisite (must be implemented first)

---

### Error Scenario 3: Log File Creation Fails

**Trigger:** Permission denied when creating logs/league_helper/ folder

**Handling:**
- Feature 01's LineBasedRotatingHandler handles this
- Error logged to stderr (from logging.FileHandler.handleError)
- Script continues (console logging unaffected)

**User Impact:** No file logging, console logging works

**Mitigation:** Documented in Feature 01 (user needs write permissions to project root)

---

## Testing Strategy

{To be defined in S4 (Epic Testing Strategy stage)}

**Initial Test Plan:**
- Unit test: run_league_helper.py argument forwarding
- Unit test: LeagueHelperManager.main() argparse integration
- Integration test: End-to-end with --enable-log-file flag
- Manual test: Verify log quality improvements don't break functionality

---

## Non-Functional Requirements

**Performance:**
- ✅ Arg parsing overhead negligible (<1ms, standard argparse)
- ✅ Log quality improvements don't add performance overhead (removing logs if anything)
- ✅ No performance degradation for console-only logging (log_to_file=False)

**Maintainability:**
- ✅ Must follow project coding standards (CODING_STANDARDS.md)
- ✅ Must preserve existing league_helper behavior when flag not provided
- ✅ CLI flag consistent with run_accuracy_simulation.py precedent
- ✅ Log messages clear and actionable

**Usability:**
- ✅ --enable-log-file flag name self-explanatory
- ✅ Help text explains flag behavior (where logs go, rotation details)
- ✅ Default behavior unchanged (file logging OFF)

**Compatibility:**
- ✅ Backward compatible with existing usage (no breaking changes)
- ✅ Tests work without modification (if they don't use subprocess wrapper)

---

## Out of Scope

**Explicitly NOT included in this feature:**
- Core infrastructure changes (Feature 1 handles LineBasedRotatingHandler, folder structure, rotation, cleanup)
- Other scripts' CLI integration (Features 3-7 handle player_data_fetcher, accuracy_sim, win_rate_sim, historical_data_compiler, schedule_fetcher)
- Console logging changes (only file logging affected)
- Log level changes (keeping INFO default)
- New logging frameworks (staying with Python stdlib logging)
- Configurable line limits (hardcoded 500 in Feature 01)
- Log format changes (keeping existing DETAILED/STANDARD/SIMPLE formats)
- Log compression or archiving

---

## Open Questions

{Tracked in checklist.md - see checklist.md for all questions requiring user input}

**Summary of Open Questions:**
1. Subprocess wrapper argument forwarding strategy (all args vs filter)
2. LOGGING_TO_FILE constant deprecation approach (keep vs remove)
3. Integration test log assertions (add vs skip)
4. Log quality audit scope (all 6 mode managers vs 4 from Discovery)
5. LOG_NAME consistency verification

---

## Implementation Notes

**Source:** RESEARCH_NOTES.md Section 9-11

### Design Decisions from Discovery

1. **Subprocess wrapper forwarding:**
   - Discovery Iteration 5 recommended sys.argv[1:] (Option B)
   - Simpler, future-proof, handles any future flags automatically
   - Alternative: Filter to known args only (more explicit, prevents unexpected args)
   - User decision required (checklist.md Q1)

2. **CLI precedent:**
   - run_accuracy_simulation.py provides excellent pattern for argparse integration
   - Adapted for boolean flag (action='store_true') instead of choice argument
   - Help text style consistent with existing scripts

3. **Integration with Feature 01:**
   - setup_logger() signature unchanged (backward compatible)
   - log_file_path=None triggers Feature 01's auto-generation
   - log_to_file sourced from CLI flag (not hardcoded constant)

4. **Log quality scope:**
   - 316 calls across 17 files (comprehensive audit required)
   - Estimated 70% KEEP, 20% UPDATE, 10% REMOVE (to be verified)
   - All mode managers included (6 total, not just 4 from Discovery)
   - User decision required on scope (checklist.md Q4)

---

### Implementation Tips

**CLI Integration:**
- Add argparse import at top of both files (run_league_helper.py, LeagueHelperManager.py)
- Use action='store_true' for boolean flag (simpler than default=None + if args.enable_log_file)
- Help text should explain WHERE logs go, HOW rotation works (500 lines, 50 max files)

**Argument Forwarding:**
- sys.argv[1:] includes all args except script name
- Append to existing subprocess args: [sys.executable, script, DATA_FOLDER] + sys.argv[1:]
- Alternative: Filter args if user prefers explicit control (checklist.md Q1)

**setup_logger Call:**
- Use keyword arguments for clarity: log_to_file=args.enable_log_file
- Set log_file_path=None (not constants.LOGGING_FILE) to trigger Feature 01 auto-generation
- Verify constants.LOG_NAME = "league_helper" (not "LeagueHelper") for folder naming consistency

**Log Quality Audit:**
- Start with high-traffic files (PlayerManager, ConfigManager, LeagueHelperManager)
- Use systematic checklist for each log call (Discovery Iteration 3 criteria)
- Create temp branch for log changes, verify tests pass before committing
- Document any test assertion updates in implementation notes

---

### Gotchas

**Gotcha 1: LOGGING_TO_FILE Still Exists**
- **Issue:** constants.py still has LOGGING_TO_FILE = False
- **Impact:** Confusing to have unused constant
- **Mitigation:** Pending user decision (checklist.md Q2) - deprecate or remove

**Gotcha 2: Integration Test May Use Class Directly**
- **Issue:** Integration test may instantiate LeagueHelperManager class directly (not via main())
- **Impact:** CLI changes won't affect test, test still uses hardcoded constants
- **Mitigation:** Verify test doesn't fail after constant changes

**Gotcha 3: Mode Managers Not Mentioned in Discovery**
- **Issue:** 2 additional mode managers exist (ReserveAssessmentModeManager, SaveCalculatedPointsManager)
- **Impact:** Discovery scope incomplete, need user decision on whether to include
- **Mitigation:** Pending user decision (checklist.md Q4) - recommend including all 6

**Gotcha 4: Log Quality Changes May Affect Tests**
- **Issue:** If tests assert on log output, changes will break tests
- **Impact:** Need to update test assertions
- **Mitigation:** Check integration test for log-related assertions (preliminary check: none found)

**Gotcha 5: Subprocess Wrapper Positional Argument**
- **Issue:** DATA_FOLDER is positional, --enable-log-file is optional
- **Impact:** Order matters: subprocess.run([exe, script, DATA_FOLDER, "--enable-log-file"])
- **Mitigation:** DATA_FOLDER comes before sys.argv[1:] in args list

---

### Code Organization

**Files Modified:**

```
run_league_helper.py                    # Add argparse, forward CLI args
league_helper/
├── LeagueHelperManager.py              # Add argparse, wire flag to setup_logger
├── constants.py                        # Optional: deprecate LOGGING_TO_FILE (pending Q2)
├── util/
│   ├── PlayerManager.py                # Log quality improvements
│   ├── ConfigManager.py                # Log quality improvements
│   ├── TeamDataManager.py              # Log quality improvements
│   └── ... (6+ util files)
├── add_to_roster_mode/
│   └── AddToRosterModeManager.py       # Log quality improvements
├── starter_helper_mode/
│   └── StarterHelperModeManager.py     # Log quality improvements
├── trade_simulator_mode/
│   ├── TradeSimulatorModeManager.py    # Log quality improvements
│   ├── trade_analyzer.py               # Log quality improvements
│   └── trade_file_writer.py            # Log quality improvements
├── modify_player_data_mode/
│   └── ModifyPlayerDataModeManager.py  # Log quality improvements
└── ... (other mode managers)

tests/
└── integration/
    └── test_league_helper_integration.py  # Verify no test failures
```

**Import Dependencies (New):**
```python
# run_league_helper.py
import argparse  # NEW

# league_helper/LeagueHelperManager.py
import argparse  # NEW
```

**No new files created** - all changes to existing files.

---

## Acceptance Criteria Cross-Reference

All functional requirements map to test coverage:

| Requirement | Test Coverage | Implementation Location |
|-------------|---------------|-------------------------|
| Req 1: CLI Flag (Wrapper) | Manual test: run_league_helper.py --enable-log-file | run_league_helper.py lines 1-69 |
| Req 2: CLI Flag (Main Entry) | Unit test: argparse integration | LeagueHelperManager.py main() lines 192-211 |
| Req 3: Log Quality DEBUG | Manual audit: 316 calls, Discovery criteria | 17 league_helper files |
| Req 4: Log Quality INFO | Manual audit: subset of 316, Discovery criteria | 17 league_helper files |

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2026-02-06 | Agent | Initial spec created with Discovery Context | S1 Step 5 (Epic Structure Creation) |
| 2026-02-06 21:30 | Secondary-A | Complete spec draft with all requirements, technical details, algorithms, integration points, error handling, and implementation notes | S2.P1.I1 (Feature-Level Discovery - research complete, drafting spec) |
| 2026-02-06 21:45 | Secondary-A | Updated spec based on user Q2 answer (remove LOGGING_TO_FILE constant) | S2.P1.I2 (Checklist Resolution - user chose Option B) |
| 2026-02-06 21:50 | Secondary-A | Spec approved by user (Gate 3 passed) | S2.P1.I3 (Refinement & Alignment - user approval received) |
| 2026-02-08 11:55 | Agent | Updated setup_logger() signature, type hints, return type, filename formats based on Feature 01 actual implementation | S8.P1 (Cross-Feature Alignment - Feature 01 complete) |
