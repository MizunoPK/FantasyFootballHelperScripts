# Feature 07 Specification: League Helper Configurability

**Status:** S2 COMPLETE
**Created:** 2026-01-28
**Last Updated:** 2026-01-30

---

## Discovery Context

**Epic-Level Findings (from DISCOVERY.md):**

### Approach Selected
Comprehensive Script-Specific Argparse - expose constants as CLI arguments

### League Helper Current State
- No argparse, subprocess runner
- 5 modes: Add to Roster, Starter Helper, Trade Simulator, Modify Player Data, Save Points
- 4 configurable constants: LOGGING_LEVEL, LOGGING_TO_FILE, RECOMMENDATION_COUNT, MIN improvements

### User Decisions
- Q2: Support ALL 5 modes OR specific mode via --mode
- Q3: E2E mode <=3 min (automated, skip prompts)
- Q4: Debug = behavioral changes + DEBUG logging
- Q5: Tests validate exit code AND outcomes

### Dependencies
- Size: MEDIUM-LARGE
- Depends: None
- Blocks: Feature 08

---

## Components Affected

### 1. run_league_helper.py (MODIFY)
**Source:** Epic Request + Derived

- Add argparse import
- Add 9+ arguments
- Pass args to LeagueHelperManager

### 2. LeagueHelperManager.py (MODIFY)
**Source:** Epic + User Q2, Q3

- Accept args in main()
- Override logging if needed
- Add run_single_mode(mode, e2e)
- Add run_all_modes_e2e()

### 3. Mode Managers (5 classes - MODIFY)
**Source:** User Q3

**Issue L3-3 Resolution: Detailed Method Signatures**

**All 5 mode managers require identical signature updates:**

**Classes to modify:**
1. `league_helper/AddToRosterManager.py`
2. `league_helper/StarterHelperManager.py`
3. `league_helper/TradeSimulatorManager.py`
4. `league_helper/ModifyPlayerDataManager.py`
5. `league_helper/SavePointsDataManager.py`

**Method signature changes:**

```python
# BEFORE (existing signature)
def main(self) -> None:
    # Interactive mode with user prompts
    pass

# AFTER (new signature)
def main(self, e2e_mode: bool = False) -> None:
    # Support both interactive and E2E modes
    if e2e_mode:
        # Skip user prompts, use automated selections
        pass
    else:
        # Original interactive behavior
        pass
```

**E2E Mode Behavior:**
- Skip all `show_list_selection()` calls (automated selection instead)
- Use hardcoded test data per R3 (highest-ranked QB, Week 1, etc.)
- Return immediately after action (no loops)
- Log actions taken for test verification

**Backward Compatibility:**
- `e2e_mode` parameter defaults to `False`
- Existing callers continue to work unchanged
- Only new E2E code passes `e2e_mode=True`

### 4. league_helper/constants.py (MODIFY - remove CLI constants)
**Source:** Epic Architectural Requirement (User 2026-02-01)

**Modifications:**
- **REMOVE:** CLI-configurable constants (LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, RECOMMENDATION_COUNT, MIN_WAIVER_IMPROVEMENT, MIN_TRADE_IMPROVEMENT)
- **KEEP:** Non-CLI constants (LOG_NAME, LOGGING_FORMAT, position constants, roster rules, etc.)
- **ADD:** Header comment explaining internal-only constants
- **Reasoning:** Single source of truth for CLI values (argparse defaults), not config files

**Reference:** See R7 for complete list of constants to remove/keep

---

## Requirements

### R1: Argparse Support
**Source:** Epic Request + User Q1

**Universal:**
- --debug
- --e2e-test
- --log-level
- --silent

**Specific:**
- --mode (1-5 or "all")
- --data-folder
- --recommendation-count
- --min-waiver-improvement
- --min-trade-improvement

**--silent Flag Behavior:**
**Source:** User Answer to Question 3 (checklist.md)
**Traceability:** User selected Option B on 2026-01-30

When --silent flag is enabled:
- Suppress: INFO and DEBUG level messages
- Show: WARNING and ERROR level messages
- Rationale: Safety over silence - users must see errors to troubleshoot issues

**Implementation:**
- Set logging level to WARNING when --silent is True
- Does not affect --log-to-file (file still gets full logs if enabled)
- Can be combined with --log-level (--log-level takes precedence)

**--log-to-file Location:**
**Source:** User Answer to Question 4 (checklist.md)
**Traceability:** User selected Option B on 2026-01-30

When --log-to-file is enabled:
- Create `logs/` directory at project root if it doesn't exist
- Log file naming: Include script name and timestamp for clarity
- Format: `logs/league_helper_YYYYMMDD_HHMMSS.log`
- Replaces old `./data/log.txt` approach

**Rationale:** User wants clear indication of where log came from and when it was created. Separates logs from data files for better organization.

### R2: Mode Selection
**Source:** User Q2

- --mode 1-5: Single mode
- --mode all: All 5 sequential
- No --mode: Interactive

**Invalid --mode Error Handling:**
**Source:** User Answer to Question 5 (checklist.md)
**Traceability:** User selected Option B on 2026-01-30

When user provides invalid --mode value:
- Print error message indicating invalid value
- Show focused usage for --mode argument only (not full help)
- Include valid options: 1, 2, 3, 4, 5, or "all"
- Exit with code 2 (argparse convention for usage errors)

**Implementation:**
- Custom error handler in argparse for --mode validation
- Format: "error: invalid mode: '99'. Valid modes: 1-5 or 'all'"
- Followed by: "--mode usage line only"

**Rationale:** Provides helpful guidance without overwhelming verbose output.

### R3: E2E Test Mode
**Source:** User Q3

Actions (<=3 min total):
- Mode 1: Draft 1 QB (<=30s)
- Mode 2: Starters Week 1 (<=30s)
- Mode 3: 1 trade (<=60s)
- Mode 4: Modify 1 player (<=20s)
- Mode 5: Save CSV (<=20s)

**E2E + --mode Interaction:**
**Source:** Loop 2 Issue L2-5 clarification

When both `--e2e-test` and `--mode <N>` are specified:
- **E2E takes precedence:** Runs ALL 5 modes sequentially (ignores --mode value)
- **User warned:** Print warning message: "Warning: --mode argument ignored when --e2e-test is set. Running all 5 modes for complete E2E validation."
- **Rationale:** E2E test requires validating complete workflow (all 5 modes), not just a single mode
- **Alternative:** User can run individual modes in E2E style by using --mode without --e2e-test flag

**Implementation:**
```python
if args.e2e_test and args.mode:
    print("Warning: --mode argument ignored when --e2e-test is set. Running all 5 modes for complete E2E validation.")
    # Proceed with all 5 modes
```

**E2E Test Data Strategy:**
**Source:** User Answer to Question 1 (checklist.md)
**Traceability:** User selected Option B on 2026-01-30

Use dynamic test data approach:
- Select highest-ranked available QB for Mode 1 (draft)
- Use Week 1 for Mode 2 (starters)
- Select any valid trade pair for Mode 3 (trade simulator)
- Modify first player in roster for Mode 4
- Use default output path for Mode 5

**Rationale:** Dynamic selection ensures tests remain valid across seasons when player rosters change. Focus is on validating workflow execution, not specific outputs.

**E2E Error Handling Strategy:**
**Source:** User Answer to Question 2 (checklist.md)
**Traceability:** User selected Option B on 2026-01-30

Continue through all 5 modes even if earlier modes fail:
- Each mode's result (pass/fail) tracked independently
- All 5 modes execute regardless of individual failures
- Final report lists all failures with details
- Exit code reflects overall result (0 = all pass, 1 = any failed)

**Rationale:** Maximizes test coverage per run - identifies all issues at once rather than requiring multiple runs to discover all failures.

### R4: Debug Mode
**Source:** User Q4

- Logging: DEBUG
- RECOMMENDATION_COUNT: 5 to 2
- Trades: 9 to 1
- Searches: Top 50 only

**Debug + E2E Combination:**
**Source:** Derived (consistency with Features 01-06)

When both `--debug` and `--e2e-test` flags are provided:
- **E2E behavior applies:** All 5 modes execute sequentially with automated selections
- **Debug logging enabled:** DEBUG level logging for verbose output
- **Debug behavioral changes apply:** Reduced counts (recommendations=2, trades=1, searches=top 50)
- **Result:** Fast E2E test (≤3 min) with verbose DEBUG logging and reduced iterations

**Rationale:** Combining both flags allows debugging E2E mode issues with detailed logging while maintaining fast execution via reduced data processing.

### R5: Backward Compatibility
**Source:** Epic Request

- No args: Interactive mode
- Existing usage unchanged

### R6: Unit Tests
**Source:** Epic Request

File: tests/integration/test_league_helper_arguments.py

Tests:
1. Argument parsing
2. Mode routing
3. E2E execution
4. Debug mode
5. Backward compat

---

### R7: Remove CLI-Configurable Constants from constants.py

**Description:** Remove CLI-configurable constants from league_helper/constants.py (now CLI-only), keep non-CLI constants

**Source:** Epic Architectural Requirement (User decision 2026-02-01: "ensure all scripts remove CLI arguments from config/constants files")

**Traceability:**
- Epic-wide architectural pattern established by Feature 10 (refactor_player_fetcher)
- User explicitly requires CLI constants removed from all config/constants files
- Single source of truth: argparse defaults in runner scripts, NOT config files

**Implementation:**
- **REMOVE from constants.py (CLI-configurable via arguments):**
  - LOGGING_LEVEL = 'INFO' (line 24) → Now in argparse default (--log-level default='INFO')
  - LOGGING_TO_FILE = False (line 25) → May become --log-to-file flag
  - LOGGING_FILE = './data/log.txt' (line 27) → Config for logging file path if needed
  - RECOMMENDATION_COUNT = 5 (line 33) → Now in argparse default (--recommendation-count default=5)
  - MIN_WAIVER_IMPROVEMENT = 0 (line 38) → Now in argparse default (--min-waiver-improvement default=0)
  - MIN_TRADE_IMPROVEMENT = 0 (line 56) → Now in argparse default (--min-trade-improvement default=0)

- **KEEP in constants.py (non-CLI, internal constants):**
  - FANTASY_TEAM_NAME = "Sea Sharp" (line 19) - may or may not be CLI-configurable, keep for now
  - LOG_NAME = "league_helper" (line 26) - internal logger name, not CLI-configurable
  - LOGGING_FORMAT = 'detailed' (line 28) - internal format, not CLI-configurable
  - NUM_TRADE_RUNNERS_UP = 9 (line 39) - internal constant
  - MIN_POSITIONS = {...} (lines 46-53) - internal roster validation rules
  - VALID_TEAMS = [...] (line 57) - internal team list
  - RB, WR, QB, TE, K, DST, FLEX (line 63) - position constants
  - ALL_POSITIONS, OFFENSE_POSITIONS, DEFENSE_POSITIONS (lines 66-68)
  - WIND_AFFECTED_POSITIONS (line 72)
  - POSSIBLE_BYE_WEEKS (line 88)
  - All other position/roster/bye constants

- **Update imports in run_league_helper.py:**
  - Remove imports of CLI-configurable constants
  - Keep imports of non-CLI constants (LOG_NAME, LOGGING_FORMAT, position constants, etc.)

- **Parameter passing:**
  - Mode managers may need to accept recommendation_count, min_waiver_improvement, min_trade_improvement as constructor params
  - Logging config passed to setup_logger() function directly from argparse values

**Acceptance Criteria:**
- constants.py contains only non-CLI constants (LOG_NAME, LOGGING_FORMAT, position constants, etc.)
- CLI-configurable constants removed from constants.py
- Clear header comment in constants.py: "Internal constants (not CLI-configurable)"
- All references updated to use parameter passing instead of constant imports
- No broken imports or undefined variable errors
- All 5 modes work correctly with new parameter passing

**Reference Implementation:** Feature 10 spec.md R8 (Handle Non-CLI Constants)

**⚠️ CRITICAL: Mode Manager Refactoring Required**

**Current Usage (WILL BREAK after removing constants):**
- AddToRosterModeManager.py: 3 references to `Constants.RECOMMENDATION_COUNT`
- TradeSimulatorModeManager.py: 2 references to `Constants.MIN_WAIVER_IMPROVEMENT`
- trade_analyzer.py: 40+ references to `Constants.MIN_WAIVER_IMPROVEMENT`, `Constants.MIN_TRADE_IMPROVEMENT`

**Total: 45+ code references** that will break if constants are removed without refactoring

**Required Refactoring:**

1. **Mode Manager Constructors:** Add parameters for CLI-configurable values
   ```python
   # AddToRosterModeManager.__init__
   def __init__(self, ..., recommendation_count: int = 5):
       self.recommendation_count = recommendation_count

   # TradeSimulatorModeManager.__init__
   def __init__(self, ..., min_waiver_improvement: int = 0, min_trade_improvement: int = 0):
       self.min_waiver_improvement = min_waiver_improvement
       self.min_trade_improvement = min_trade_improvement
   ```

2. **Replace all Constants.* references with self.* references:**
   ```python
   # BEFORE (will break):
   Constants.RECOMMENDATION_COUNT

   # AFTER (correct):
   self.recommendation_count
   ```

3. **Parameter Flow:** run_league_helper.py → LeagueHelperManager → Mode Managers
   - run_league_helper.py: Parse args (--recommendation-count, --min-waiver-improvement, --min-trade-improvement)
   - LeagueHelperManager: Pass args to mode manager constructors
   - Mode managers: Store and use instance variables instead of Constants

**Scope Impact:** This significantly increases Feature 07 complexity
- Originally: Add argparse + E2E mode (medium scope)
- Now: Add argparse + E2E mode + refactor 3 mode managers + update 45+ references (large scope)

**Alternative (if scope too large):** Keep these constants in constants.py with clear comment marking them as "INTERNAL DEFAULTS (overridden by CLI args)" - but this violates the epic architectural pattern

**Recommendation:** Proceed with refactoring to maintain architectural consistency across epic

---

## Dependencies

**Internal (EXISTS):**
- utils/LoggingManager.py
- league_helper/util/user_input.py
- All 5 mode managers
- league_helper/constants.py

**Blocks:** Feature 08

**External:** argparse, subprocess, sys, pathlib (stdlib)

---

## Data Structures

### Command-Line Arguments (Input)

**Format:** argparse.Namespace object

**Fields:**
- `mode` (str or None): Mode selection ("1", "2", "3", "4", "5", "all", or None for interactive)
- `debug` (bool): Enable debug mode (default: False)
- `e2e_test` (bool): Enable E2E test mode (default: False)
- `log_level` (str): Logging level (choices: DEBUG/INFO/WARNING/ERROR/CRITICAL, default: INFO)
- `silent` (bool): Suppress INFO/DEBUG logs (default: False)
- `log_to_file` (bool): Enable file logging (default: False)
- `data_folder` (str): Path to data folder (default: "./data")
- `recommendation_count` (int): Number of recommendations (default: 5)
- `min_waiver_improvement` (float): Minimum improvement for waiver recommendations (default: 0.5)
- `min_trade_improvement` (float): Minimum improvement for trade recommendations (default: 0.5)

**Source:** Derived from R1 (Argparse Support)

---

### Log File Naming

**Pattern:** `logs/league_helper_YYYYMMDD_HHMMSS.log`

**Components:**
- Directory: `logs/` (created at project root if doesn't exist)
- Prefix: `league_helper_` (identifies source script)
- Timestamp: `YYYYMMDD_HHMMSS` (creation time)
- Extension: `.log`

**Example:** `logs/league_helper_20260130_154530.log`

**Source:** User Answer to Question 4 (R1 - --log-to-file Location)

---

### E2E Test Results

**Format:** List of dictionaries (internal tracking structure)

**Structure:**
```python
e2e_results = [
    {"mode": 1, "name": "Draft", "status": "PASS/FAIL", "error": None or str},
    {"mode": 2, "name": "Starters", "status": "PASS/FAIL", "error": None or str},
    {"mode": 3, "name": "Trade", "status": "PASS/FAIL", "error": None or str},
    {"mode": 4, "name": "Modify", "status": "PASS/FAIL", "error": None or str},
    {"mode": 5, "name": "Save", "status": "PASS/FAIL", "error": None or str}
]
```

**Usage:** Track results when running E2E mode with continue-on-error behavior

**Source:** User Answer to Question 2 (R3 - E2E Error Handling Strategy)

---

## Algorithms

### Mode Selection Algorithm

**Pseudocode:**
```python
def determine_execution_path(args):
    # E2E mode overrides everything
    if args.e2e_test:
        if args.mode:
            print("Warning: --mode ignored when --e2e-test is set.")
        return run_all_modes_e2e()

    # Mode specified
    if args.mode:
        if args.mode == "all":
            return run_all_modes_sequential()
        else:
            mode_num = int(args.mode)
            return run_single_mode(mode_num, e2e=False)

    # No mode specified - interactive
    return run_interactive_mode()
```

**Source:** Derived from R2 (Mode Selection) and R3 (E2E Test Mode)

---

### E2E Mode Execution Algorithm

**E2E Logging Level:**
- **Default:** INFO level (clean output for automated testing)
- **Overridable:** Can use --log-level DEBUG or --debug flag for verbose E2E output
- **Consistency:** Pattern from Features 01-06, applied to league helper

**Pseudocode:**
```python
async def run_all_modes_e2e():
    # Set logging level (unless overridden)
    if not args.debug:
        log_level = args.log_level if hasattr(args, 'log_level') else 'INFO'
    else:
        log_level = 'DEBUG'  # Debug takes precedence

    results = []

    # Mode 1: Draft 1 QB (<=30s)
    try:
        await run_mode_1_e2e()  # Select highest-ranked available QB
        results.append({"mode": 1, "status": "PASS", "error": None})
    except Exception as e:
        results.append({"mode": 1, "status": "FAIL", "error": str(e)})

    # Mode 2: Starters Week 1 (<=30s)
    try:
        await run_mode_2_e2e()  # Use Week 1
        results.append({"mode": 2, "status": "PASS", "error": None})
    except Exception as e:
        results.append({"mode": 2, "status": "FAIL", "error": str(e)})

    # Mode 3: 1 trade (<=60s)
    try:
        await run_mode_3_e2e()  # Select any valid trade pair
        results.append({"mode": 3, "status": "PASS", "error": None})
    except Exception as e:
        results.append({"mode": 3, "status": "FAIL", "error": str(e)})

    # Mode 4: Modify 1 player (<=20s)
    try:
        await run_mode_4_e2e()  # Modify first player in roster
        results.append({"mode": 4, "status": "PASS", "error": None})
    except Exception as e:
        results.append({"mode": 4, "status": "FAIL", "error": str(e)})

    # Mode 5: Save CSV (<=20s)
    try:
        await run_mode_5_e2e()  # Use default output path
        results.append({"mode": 5, "status": "PASS", "error": None})
    except Exception as e:
        results.append({"mode": 5, "status": "FAIL", "error": str(e)})

    # Generate final report
    failures = [r for r in results if r["status"] == "FAIL"]
    if failures:
        print("E2E Test FAILED. Failures:")
        for f in failures:
            print(f"  Mode {f['mode']}: {f['error']}")
        return 1  # Exit code 1
    else:
        print("E2E Test PASSED. All 5 modes validated.")
        return 0  # Exit code 0
```

**Source:** User Answer to Question 2 (R3 - E2E Error Handling Strategy)

---

### Debug Mode Configuration Algorithm

**Pseudocode:**
```python
def apply_debug_mode(args):
    if args.debug:
        # Set logging to DEBUG
        log_level = "DEBUG"

        # Reduce behavioral parameters
        recommendation_count = 2  # 5 → 2
        max_trades_to_analyze = 1  # 9 → 1
        player_search_limit = 50  # Top 50 only

        print("DEBUG MODE ENABLED:")
        print(f"  Logging: {log_level}")
        print(f"  Recommendations: {recommendation_count}")
        print(f"  Trades analyzed: {max_trades_to_analyze}")
        print(f"  Player search limit: {player_search_limit}")

    # If both --debug and --e2e-test
    if args.debug and args.e2e_test:
        # Combine behaviors
        # E2E automated selections + DEBUG logging + reduced data
        print("  (Combined with E2E test mode)")
```

**Source:** R4 (Debug Mode) and R4 Debug + E2E Combination

---

### Logging Level Resolution Algorithm

**Pseudocode:**
```python
def resolve_logging_level(args):
    # Precedence order (highest to lowest)
    if args.silent:
        return "WARNING"  # Suppress INFO/DEBUG
    elif args.debug:
        return "DEBUG"  # Debug forces DEBUG
    elif args.log_level:
        return args.log_level  # User-specified
    else:
        return "INFO"  # Default
```

**Source:** R1 (--silent Flag Behavior) and R4 (Debug Mode)

---

## Acceptance Criteria

### 1. Behavior Changes

**New Functionality:**
- Command-line argument parsing via argparse (9+ arguments)
- E2E test mode that executes all 5 modes automatically in <=3 minutes
- Debug mode with reduced data processing for faster testing
- Silent mode for minimal console output
- Mode selection (specific mode 1-5, all modes, or interactive)
- Timestamped logging to `logs/` directory

**Modified Functionality:**
- LeagueHelperManager now accepts optional arguments (backward compatible)
- All 5 mode managers accept e2e_mode parameter to skip interactive prompts
- Logging configuration can be overridden via arguments

**No Changes:**
- Interactive mode remains default when no arguments provided
- All existing league helper functionality unchanged
- Existing data structures and business logic preserved

---

### 2. Files Modified

**Existing Files Modified:**
- `run_league_helper.py` - Add argparse, pass args to LeagueHelperManager
- `league_helper/LeagueHelperManager.py` - Add argument handling, mode routing
- `league_helper/AddToRosterManager.py` - Add e2e_mode parameter
- `league_helper/StarterHelperManager.py` - Add e2e_mode parameter
- `league_helper/TradeSimulatorManager.py` - Add e2e_mode parameter
- `league_helper/ModifyPlayerDataManager.py` - Add e2e_mode parameter
- `league_helper/SavePointsDataManager.py` - Add e2e_mode parameter
- `league_helper/util/user_input.py` (potentially) - E2E mode may need helper

**New Files Created:**
- `tests/integration/test_league_helper_arguments.py` - Integration tests
- `logs/` directory - Auto-created at project root

**Data Files:**
- No changes to existing data files
- New log files created in `logs/` directory with format: `league_helper_YYYYMMDD_HHMMSS.log`

---

### 3. Data Structures

**New Structures:**
- None - using argparse Namespace for arguments

**Modified Structures:**
- `LeagueHelperManager.main()` signature: Add optional args parameter
- All 5 mode manager `main()` signatures: Add optional e2e_mode parameter

**No Changes:**
- Player data structures
- League configuration structures
- Trade evaluation structures

---

### 4. API/Interface Changes

**New Methods:**
- `LeagueHelperManager.run_single_mode(mode, e2e)` - Execute specific mode
- `LeagueHelperManager.run_all_modes_e2e()` - Execute all 5 modes sequentially

**Modified Methods:**
- `LeagueHelperManager.main(args=None)` - Now accepts optional args
- Each mode manager's `main(e2e_mode=False)` - Add e2e_mode parameter
- `show_list_selection()` calls skip selection in E2E mode

**No Changes:**
- Trade evaluation methods
- Player scoring methods
- Data loading methods

---

### 5. Testing

**Test File:** `tests/integration/test_league_helper_arguments.py`

**Test Count:** 5 minimum tests
1. `test_argument_parsing` - Verify all 9 arguments parse correctly
2. `test_mode_routing` - Verify --mode 1-5 routes to correct mode
3. `test_e2e_execution` - Verify E2E mode completes all 5 modes in <=3 min
4. `test_debug_mode` - Verify debug mode reduces data processing
5. `test_backward_compatibility` - Verify no args = interactive mode

**Coverage Targets:**
- New argparse code: 100%
- Modified mode managers: 100%
- E2E test paths: 100%

**Edge Cases Tested:**
- Invalid --mode value (e.g., --mode 99)
- Combined flags (--debug --e2e-test)
- --silent with errors (ensures errors still shown)
- Missing data/ folder (graceful failure)
- Log directory creation (auto-create logs/)

---

### 6. Dependencies

**Depends On:**
- None (Feature 07 has no upstream dependencies)

**Blocks:**
- Feature 08 (Integration Test Framework) - depends on E2E modes being implemented

**External Dependencies:**
- argparse (stdlib)
- subprocess (stdlib)
- sys (stdlib)
- pathlib (stdlib)
- datetime (stdlib) - for timestamped logs

**Internal Dependencies:**
- utils/LoggingManager.py (existing)
- league_helper/util/user_input.py (existing)
- All 5 mode managers (existing)
- league_helper/constants.py (existing)

---

### 7. Edge Cases & Error Handling

**Edge Cases Handled:**
1. **Invalid --mode:** Custom error shows valid options (1-5, all)
2. **Missing data/ folder:** Graceful error message, exit code 1
3. **E2E mode failure:** Continue through all 5 modes, report all failures
4. **logs/ directory missing:** Auto-create on first use
5. **Conflicting flags:** --log-level takes precedence over --silent
6. **No players available:** E2E mode skips gracefully, reports issue

**Error Conditions:**
- Invalid argument values: Exit code 2 (usage error)
- Runtime errors: Exit code 1 (general error)
- E2E any mode failure: Exit code 1 (test failure)
- E2E all modes pass: Exit code 0 (success)

**Logging:**
- All errors logged to file if --log-to-file enabled
- Errors shown on console even with --silent
- DEBUG mode logs additional context

---

### 8. Documentation

**User-Facing Documentation:**
- --help output for all 9 arguments
- Usage examples in comments at top of run_league_helper.py
- Error messages for invalid arguments

**Developer Documentation:**
- Docstrings for new methods (run_single_mode, run_all_modes_e2e)
- Comments explaining E2E mode behavior in mode managers
- Comments explaining argument precedence (--log-level vs --silent)

**Testing Documentation:**
- Test file docstring explaining integration test approach
- Comments in E2E test explaining <=3 min time budget

---

### 9. User Approval

- [x] **I approve these acceptance criteria**

**Approval Timestamp:** 2026-01-30 23:16

**Approval Notes:**
User approved on 2026-01-30 with no modifications requested.

---

## Cross-Feature Alignment

**Compared To:** Features 01-06 (all Group 1 features)

**Alignment Status:** ✅ ALIGNED - No conflicts found

**Universal Flags Consistency:**
- ✅ --debug: Consistent implementation (DEBUG logging + reduced recommendations/trades/searches)
- ✅ --e2e-test: Consistent implementation (all 5 modes automated, ≤3 min total)
- ✅ --log-level: Consistent implementation (DEBUG/INFO/WARNING/ERROR/CRITICAL choices)
- ✅ --silent: Feature 07 specific (suppresses INFO/DEBUG, shows WARNING/ERROR)

**League Helper Specific Patterns:**
- ✅ --mode: Feature 07 specific (1-5 for specific mode, "all" for sequential, none for interactive)
- ✅ E2E + --mode interaction: Issue L2-5 identified (needs clarification)
- ✅ Pattern: Script-specific arguments for league helper's unique functionality

**Debug Mode Behavioral Changes:**
- ✅ Feature 07: RECOMMENDATION_COUNT 5→2, trades 9→1, searches top 50 only
- ✅ Consistent pattern: All features reduce iterations/datasets for debug mode

**E2E Mode Validation:**
- ✅ Feature 07: Continues through all 5 modes even if failures occur
- ✅ Unique approach: Most features stop on failure, Feature 07 collects all failures
- ✅ Rationale: Maximizes test coverage per run (User Answer Checklist Q2)

**Debug + E2E Combination:**
- ✅ Feature 07: Both flags combine (E2E behavior + DEBUG logging + reduced data)
- ✅ Consistent with Features 01-06 combination behaviors
- ✅ Added per Loop 1 Issue 2

**Logging Infrastructure:**
- ✅ Feature 07: Uses timestamped logs in logs/ directory
- ✅ Pattern: logs/league_helper_YYYYMMDD_HHMMSS.log
- ✅ Unique to Feature 07 (other features use standard logging)

**No Conflicts Found:**
- No file overlap (run_league_helper.py and LeagueHelperManager.py unique to Feature 07)
- No conflicting requirements with Features 01-06
- Script-specific args appropriate for league helper's 5-mode design

**Verified By:** Primary Agent (S3 Final Consistency Loop)
**Date:** 2026-01-30
