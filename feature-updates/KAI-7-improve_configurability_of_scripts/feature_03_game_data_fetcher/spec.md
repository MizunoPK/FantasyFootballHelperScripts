# Feature 03 Specification: Game Data Fetcher Enhancement

**Status:** INITIAL (S2.P1 Phase 0 complete, will be detailed in S2.P1 Phase 1)
**Created:** 2026-01-28
**Last Updated:** 2026-01-29

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Purpose:** Enhance existing argparse with debug/E2E modes for game data fetcher

**Scope:**
- Enhance existing argparse (add --debug, --e2e-test, --log-level)
- Add debug mode (DEBUG logging + limited weeks)
- Add E2E test mode (fetch single week, ≤3 min)
- Unit tests for new modes

**Size Estimate:** SMALL

**Discovery Basis:**
- Based on Finding: `run_game_data_fetcher.py` already has argparse with --season, --output, --weeks (Discovery Iteration 1, lines 50)
- Based on User Answer Q3: Real APIs with data limiting for E2E
- Based on User Answer Q4: Debug = behavioral changes + DEBUG logging

---

### Relevant Discovery Decisions

**Recommended Approach:** Comprehensive Script-Specific Argparse (Option 2 from DISCOVERY.md)

**Key Design Decisions:**
1. **Script-Specific Args:** Enhance existing argparse with universal flags (--debug, --e2e-test, --log-level)
2. **E2E Behavior:** Use real APIs with data limiting (fetch single week only, ≤3 min)
3. **Debug Behavior:** Enable DEBUG logging + behavioral changes (limit to single week, verbose output)
4. **Integration Test Validation:** Tests check exit code AND specific expected outcomes

**Scope Boundaries:**
- IN SCOPE: Enhance existing args, add debug/E2E modes, unit tests
- OUT OF SCOPE: Mocking APIs, new data sources, configuration files
- DEFERRED: Mock data support (future work)

---

### Relevant User Answers (from Discovery)

**Q3: What makes an E2E run "reasonable" (3 min max)?**
- Answer: "Fetchers: real APIs with data limiting args"
- Impact for Feature 03: E2E mode fetches single week only, uses existing --weeks arg

**Q4: Should debug mode be a separate log level or different behavior?**
- Answer: "Option C: Both logging AND behavioral changes"
- Impact for Feature 03: --debug flag enables DEBUG logs AND limits to single week fetch

**Q5: How should integration tests determine pass/fail?**
- Answer: "Check exit code AND verify expected outcomes (specific logs, result counts)"
- Impact for Feature 03: Test validates exit code 0, checks output file exists, verifies week count

---

## Dependencies

- **Depends on:** None
- **Blocks:** Feature 08 (integration_test_framework)

---

## Initial Purpose (from S1 Breakdown)

Enhance existing argparse arguments and add debug logging to game data fetcher.

---

## Initial Scope (from S1 Breakdown)

- Enhance argparse in `run_game_data_fetcher.py` (add --debug, --e2e-test, --log-level)
- Add debug mode (DEBUG logging + limited weeks)
- Create E2E test mode (fetch single week, ~3 min)
- Unit tests for new arguments and modes

---

---

## Components Affected

### File 1: run_game_data_fetcher.py

**Path:** `run_game_data_fetcher.py` (root directory)
**Current State:** Has argparse with 4 arguments (lines 56-84), hardcoded INFO logging (line 109)
**Modifications Required:**
1. Add --debug flag to argparse (enhancement to existing parser)
2. Add --e2e-test flag to argparse (enhancement to existing parser)
3. Add --log-level argument to argparse (enhancement to existing parser)
4. Replace hardcoded "INFO" with args.log_level in setup_logger() call (line 109)
5. Add conditional logic for debug mode behavior (after arg parsing)
6. Add conditional logic for E2E test mode behavior (after arg parsing)

**Source:** Derived requirement (necessary to implement user-requested --debug and --e2e-test flags from Discovery)

**Research Evidence:** Research document lines 29-94 (complete file analysis with line numbers)

---

### File 2: No New Files Created

**Source:** Derived requirement (existing code supports all functionality, no new modules needed)

**Rationale:**
- LoggingManager already supports DEBUG level (research: lines 96-120)
- fetch_game_data() already accepts weeks parameter (research: lines 122-152)
- No new classes or modules needed for this enhancement

---

## Requirements

### Requirement 1: Add --debug Flag

**Description:** Add --debug command-line flag that enables DEBUG logging and behavioral changes

**Source:** Epic Request (DISCOVERY.md line 206: "Universal --debug flag on all 7 runners (enables DEBUG logging + behavioral changes)")

**Traceability:** User Answer Q4 from Discovery: "Debug mode = behavioral changes + DEBUG logs"

**Implementation:**
- Add `parser.add_argument('--debug', action='store_true', help='Enable debug mode (DEBUG logging + single week fetch)')`
- When --debug is True: set log_level to "DEBUG" AND limit weeks to current_week only
- Behavioral change: Single week fetch for faster debugging cycles

**Edge Cases:** If both --debug and --e2e-test specified, --e2e-test takes precedence (see Requirement 6)

---

### Requirement 2: Add --e2e-test Flag

**Description:** Add --e2e-test command-line flag that runs fast end-to-end test mode (≤3 min)

**Source:** Epic Request (DISCOVERY.md line 206: "Universal --e2e-test flag on all 7 runners (triggers fast E2E mode ≤3 min)")

**Traceability:** User Answer Q3 from Discovery: "Fetchers: real APIs with data limiting args"

**Implementation:**
- Add `parser.add_argument('--e2e-test', action='store_true', help='Run E2E test mode (fetch week 1 only, ~3 min)')`
- When --e2e-test is True: Force weeks=[1] regardless of other arguments
- Use real ESPN and Open-Meteo APIs (no mocking)
- Single week fetch completes in <3 minutes

**Edge Cases:**
- If --weeks also specified: --e2e-test overrides (E2E mode always fetches week 1)
- If --season specified: E2E mode fetches week 1 of that season

---

### Requirement 3: Add --log-level Argument

**Description:** Add --log-level argument to control logging verbosity

**Source:** Derived requirement (necessary to provide flexible logging control as specified in Discovery approach)

**Traceability:** DISCOVERY.md line 37 (Comprehensive Script-Specific Argparse includes log-level control)

**Implementation:**
- Add `parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help='Set logging level')`
- Replace hardcoded "INFO" at line 109 with args.log_level
- LoggingManager already supports all 5 levels (research confirmed)

**Edge Cases:** If --debug flag also specified, --debug forces DEBUG level (see Requirement 6)

---

### Requirement 4: Debug Mode Behavioral Changes

**Description:** When --debug is enabled, limit data fetch to current week only (faster debugging)

**Source:** Epic Request (DISCOVERY.md line 209: "Debug mode behavioral changes (fewer iterations, smaller datasets, verbose output)")

**Traceability:** User Answer Q4: "Debug = behavioral changes + DEBUG logs"

**Implementation:**
```python
if args.debug:
    log_level = "DEBUG"
    if not args.e2e_test and not args.weeks:
        weeks = [current_week]  # Single week for debugging
    logger.debug("Debug mode enabled: single week fetch")
```

**Rationale:** Debugging with full season data (18 weeks) is slow; single week provides fast feedback loop

---

### Requirement 5: E2E Test Mode Behavioral Changes

**Description:** When --e2e-test is enabled, force fetch of week 1 only (≤3 min execution)

**Source:** Epic Request (DISCOVERY.md line 208: "E2E test modes with specific behaviors (simulations: 1 run/0-1 configs, fetchers: limited data)")

**Traceability:** User Answer Q3: "Fetchers use real APIs with data limiting"

**Implementation:**
```python
if args.e2e_test:
    weeks = [1]  # Force week 1 for E2E mode
    # E2E uses INFO logging unless overridden
    if not args.debug and args.log_level == 'INFO':  # Default case
        log_level = 'INFO'
    logger.info("E2E test mode: fetching week 1 only")
```

**E2E Logging Level:**
- **Default:** INFO level (cleaner output than DEBUG, more visible than WARNING)
- **Overridable:** Can be changed with --log-level DEBUG or --debug flag for verbose E2E testing
- **Consistency:** Pattern established in Feature 01, applied across all fetchers

**Rationale:** Week 1 data is always available (past week), provides consistent E2E test target, completes in <3 min

---

### Requirement 6: Flag Priority Logic

**Description:** Define clear priority when multiple flags conflict

**Source:** Derived requirement (necessary to prevent ambiguous behavior when conflicting flags specified)

**Implementation Priority (highest to lowest):**
1. --e2e-test (if present, forces weeks=[1])
2. --weeks (if present, uses specified weeks)
3. --debug (if present and no --weeks, uses current_week)
4. Default (fetches weeks 1 to current_week)

**Pseudocode:**
```python
if args.e2e_test:
    weeks = [1]
elif args.weeks:
    weeks = parse_weeks(args.weeks)
elif args.debug:
    weeks = [current_week]
else:
    weeks = None  # Default behavior
```

---

### Requirement 7: Unit Tests for New Arguments

**Description:** Create unit tests for argument parsing and mode behaviors

**Source:** Epic Request (DISCOVERY.md line 22: "Unit tests for new arguments and logging")

**Test Cases:**
1. Test --debug flag enables DEBUG logging
2. Test --e2e-test flag forces week 1
3. Test --log-level argument sets correct level
4. Test flag priority logic (--e2e-test > --weeks > --debug)
5. Test conflicting flags handled correctly

**Test File:** `tests/test_run_game_data_fetcher.py` (new file)

---

## Data Structures

### Input: Command-Line Arguments

**Existing Arguments (unchanged):**
- `--season` (int): NFL season year (default: current season from config)
- `--output` (str): Output file path (default: data/game_data.csv)
- `--weeks` (str): Weeks to fetch ("1-18" range or "1,3,5" list)
- `--current-week` (int): Override current NFL week

**New Arguments:**
- `--debug` (flag): Enable debug mode
- `--e2e-test` (flag): Enable E2E test mode
- `--log-level` (str): Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)

**Source:** Epic Request + Derived (existing args from research, new args from Discovery)

---

### Output: Game Data CSV

**Format:** CSV file with game data (format unchanged by this feature)

**Columns:** Defined in game_data_models.py GAME_DATA_CSV_COLUMNS

**Sample Output:** data/game_data.csv or user-specified path

**Changes:** None (this feature only affects HOW data is fetched, not WHAT is fetched)

**Source:** Research (lines 569 in fetch_game_data: returns Path to CSV)

---

### Internal: weeks Parameter

**Type:** Optional[List[int]]

**Purpose:** Controls which weeks to fetch

**Values:**
- None: Default behavior (fetches weeks 1 to current_week)
- [1]: E2E test mode (single week)
- [current_week]: Debug mode (single week)
- [1, 3, 5]: User-specified weeks (via --weeks arg)

**Source:** Research (fetch_game_data signature line 521 accepts weeks parameter)

---

## Algorithms

### Algorithm 1: Argument Processing and Mode Detection

**Pseudocode:**
```python
def main():
    # Parse arguments
    parser = argparse.ArgumentParser(...)
    parser.add_argument('--season', ...)  # Existing
    parser.add_argument('--output', ...)  # Existing
    parser.add_argument('--weeks', ...)   # Existing
    parser.add_argument('--current-week', ...)  # Existing
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode (DEBUG logging + single week)')
    parser.add_argument('--e2e-test', action='store_true',
                       help='Run E2E test (fetch week 1, ~3 min)')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                       default='INFO', help='Set logging level')

    args = parser.parse_args()

    # Determine logging level (--debug forces DEBUG)
    if args.debug:
        log_level = "DEBUG"
    else:
        log_level = args.log_level

    # Setup logger with determined level
    logger = setup_logger("game_data_fetcher", log_level, False, None, "standard")

    # Determine season and current_week (unchanged logic)
    season = args.season if args.season else NFL_SEASON
    current_week = args.current_week if args.current_week else CURRENT_NFL_WEEK
    if args.season and args.season < NFL_SEASON:
        current_week = 18

    # Determine weeks based on flag priority
    weeks = None
    if args.e2e_test:
        weeks = [1]
        logger.info("E2E test mode: fetching week 1 only")
    elif args.weeks:
        weeks = parse_weeks(args.weeks)
        logger.info(f"Fetching specific weeks: {weeks}")
    elif args.debug:
        weeks = [current_week]
        logger.debug(f"Debug mode: fetching current week {current_week} only")

    # Determine output path (unchanged logic)
    if args.output:
        output_path = script_dir / args.output
    else:
        output_path = script_dir / "data" / "game_data.csv"

    # Fetch game data (unchanged call)
    result_path = fetch_game_data(
        output_path=output_path,
        season=season,
        current_week=current_week,
        weeks=weeks
    )

    # Print summary (unchanged)
    ...
```

**Source:** Derived requirement (necessary logic to implement user-requested flags)

---

### Algorithm 2: Flag Priority Resolution

**Logic Flow:**
1. Check --e2e-test first (highest priority)
   - If True: weeks = [1], skip other week logic
2. Check --weeks second (user-specified weeks)
   - If present: weeks = parse_weeks(args.weeks)
3. Check --debug third (single week for debugging)
   - If True and no --weeks: weeks = [current_week]
4. Default behavior (if none of above)
   - weeks = None (fetch_game_data fetches 1 to current_week)

**Rationale:** E2E testing needs consistent behavior (always week 1), user-specified weeks should work unless overridden by E2E, debug mode provides convenience default

**Source:** Derived requirement (prevents ambiguous behavior with conflicting flags)

---

### Algorithm 3: Logging Level Determination

**Logic:**
```python
if args.debug:
    log_level = "DEBUG"  # --debug forces DEBUG level
else:
    log_level = args.log_level  # Use user-specified or default INFO
```

**Rationale:** --debug flag is convenience shortcut (enables DEBUG + behavioral changes), --log-level provides fine-grained control

**Source:** Derived requirement (implements Discovery design decision for debug mode)

---

## Dependencies

### Internal Dependencies

**Dependency 1: utils/LoggingManager.py**

**Status:** EXISTS (no changes needed)

**Interface Used:** `setup_logger(name, level, log_to_file, log_file_path, log_format)`

**Source:** Research (lines 45-53 show function signature)

**Usage:** Pass args.log_level or "DEBUG" as level parameter

---

**Dependency 2: player-data-fetcher/game_data_fetcher.py**

**Status:** EXISTS (no changes needed)

**Interface Used:** `fetch_game_data(output_path, season, current_week, weeks)`

**Source:** Research (lines 517-522 show function signature)

**Usage:** Pass weeks=[1] for E2E mode, weeks=[current_week] for debug mode

---

**Dependency 3: player-data-fetcher/config.py**

**Status:** EXISTS (⚠️ NOTE: After Feature 10, CLI constants will be removed)

**Constants Used (BEFORE Feature 10):** NFL_SEASON, CURRENT_NFL_WEEK

**⚠️ ARCHITECTURAL CHANGE (2026-02-01):**
- After Feature 10 implementation, NFL_SEASON and CURRENT_NFL_WEEK will be REMOVED from player-data-fetcher/config.py
- These are CLI-configurable constants (Feature 01 exposes them via --season, --week arguments)
- Epic architectural requirement: CLI constants must be removed from all config files

**Impact on Feature 03:**
- **BEFORE:** run_game_data_fetcher.py imports NFL_SEASON, CURRENT_NFL_WEEK from player-data-fetcher/config.py as fallback defaults
- **AFTER Feature 10:** These constants won't exist in config.py
- **SOLUTION:** Use Feature 03's own argparse defaults instead
  - `parser.add_argument('--season', type=int, default=2025, ...)` ← Hardcode default in argparse
  - `parser.add_argument('--current-week', type=int, default=17, ...)` ← Hardcode default in argparse
- **Result:** Single source of truth (argparse defaults), no dependency on player-data-fetcher/config.py

**Required Change:**
- Remove imports: `from config import NFL_SEASON, CURRENT_NFL_WEEK`
- Update argparse defaults to use hardcoded values (2025, 17) instead of importing from config.py
- Document: "Defaults previously imported from player-data-fetcher/config.py, now hardcoded per epic architectural pattern"

**Reference:** Feature 10 R8 (removes CLI constants from config.py)

---

### External Dependencies

**Dependency 4: Feature 08 (integration_test_framework)**

**Status:** BLOCKS Feature 08 (this feature must complete first)

**Reason:** Integration tests for this script require --debug and --e2e-test flags to exist

**Source:** DISCOVERY.md line 400 (Feature 08 depends on Features 01-07)

---

### Feature Dependencies

**This Feature Depends On:** None (independent enhancement)

**This Feature Blocks:** Feature 08 (integration_test_framework needs these flags)

**Parallel Features:** Features 01, 02, 04, 05, 06, 07 (all can proceed independently)

**Source:** DISCOVERY.md Feature Dependency Diagram (lines 435-445)

---

## Edge Cases and Error Handling

### Edge Case 1: Conflicting Flags

**Scenario:** User specifies `--debug --e2e-test --weeks 5-10`

**Behavior:** --e2e-test takes highest priority, fetches week 1 only

**Logging:** "E2E test mode: fetching week 1 only"

**Source:** Derived requirement (prevents ambiguous behavior)

---

### Edge Case 2: Invalid Log Level with --debug

**Scenario:** User specifies `--debug --log-level ERROR`

**Behavior:** --debug forces DEBUG level, --log-level ignored

**Logging:** "Debug mode enabled: DEBUG logging active"

**Source:** Derived requirement (--debug is convenience shortcut)

---

### Edge Case 3: E2E Mode with Historical Season

**Scenario:** User specifies `--season 2024 --e2e-test`

**Behavior:** Fetches week 1 of 2024 season (real historical data)

**Expected:** Week 1 games from 2024 season in CSV

**Source:** Derived requirement (E2E mode should work for any season)

---

### Edge Case 4: Debug Mode with No Current Week Data

**Scenario:** User runs --debug when current_week has no games yet

**Behavior:** fetch_game_data() returns empty games list, CSV has 0 rows

**Logging:** "Total games: 0" in summary

**Source:** Research (existing behavior, no changes needed)

---

## Acceptance Criteria (Gate 4 - User Approval Required)

**Purpose:** This section defines EXACTLY what will be implemented. User approval required before proceeding to S5 (Implementation Planning).

---

### 1. Behavior Changes

**New Functionality:**
- ✅ `--debug` flag enables DEBUG logging + limits fetch to current week only
- ✅ `--e2e-test` flag forces week 1 fetch for fast E2E testing (≤3 min)
- ✅ `--log-level` argument provides fine-grained logging control (5 levels)

**Modified Functionality:**
- ✅ Logging level now configurable (was hardcoded to INFO)
- ✅ Weeks parameter now controllable via multiple methods (flags, args, defaults)

**No Changes:**
- ✅ CSV output format unchanged
- ✅ Game data fetching logic unchanged
- ✅ API integrations unchanged

---

### 2. Files Modified

**Existing Files Modified:**
- `run_game_data_fetcher.py` (root directory)
  - Lines 56-84: Add 3 new argparse arguments (--debug, --e2e-test, --log-level)
  - Line 109: Replace hardcoded "INFO" with args.log_level
  - Lines 115-125: Add flag priority logic (determine weeks based on flags)
  - Total changes: ~15-20 lines modified/added

**New Files Created:**
- `tests/test_run_game_data_fetcher.py`
  - Unit tests for new argument parsing
  - Unit tests for flag priority logic
  - Unit tests for edge cases
  - Estimated: ~100-150 lines

**Files NOT Modified:**
- `player-data-fetcher/game_data_fetcher.py` (no changes needed)
- `utils/LoggingManager.py` (already supports all log levels)
- `data/game_data.csv` (output format unchanged)

---

### 3. Data Structures

**New Structures:**
- None (this is an argparse enhancement only)

**Modified Structures:**
- `args` namespace (argparse.Namespace)
  - Added fields: `args.debug` (bool), `args.e2e_test` (bool), `args.log_level` (str)

**Unchanged Structures:**
- CSV output format (GAME_DATA_CSV_COLUMNS)
- Game data models
- Configuration structures

---

### 4. API/Interface Changes

**New Command-Line Arguments:**
- `--debug` (flag): Enable debug mode (DEBUG logging + single week fetch)
- `--e2e-test` (flag): Run E2E test mode (fetch week 1 only, ~3 min)
- `--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}` (arg): Set logging level (default: INFO)

**Existing Arguments (Unchanged):**
- `--season YEAR`: NFL season year
- `--output PATH`: Output file path
- `--weeks RANGE`: Weeks to fetch
- `--current-week NUM`: Override current NFL week

**No Python API Changes:**
- This feature ONLY affects `run_game_data_fetcher.py` CLI interface
- No changes to `fetch_game_data()` function signature
- No changes to any library modules

---

### 5. Testing

**Unit Tests:**
- Test count: 8-10 new tests in `tests/test_run_game_data_fetcher.py`
- Coverage target: >90% for argument parsing logic
- Test categories:
  - Argument parsing (3 tests)
  - Flag priority logic (3 tests)
  - Edge cases (2-4 tests)

**Integration Tests (Feature 08):**
- This feature BLOCKS Feature 08 (integration test framework)
- Feature 08 will create integration tests that USE --debug and --e2e-test flags

**Edge Cases Tested:**
- Conflicting flags (--debug + --e2e-test + --weeks)
- Invalid log level (already handled by argparse choices)
- Debug mode with no current week data
- E2E mode with historical season

---

### 6. Dependencies

**Depends On:**
- None (this is independent enhancement)

**Blocks:**
- Feature 08 (integration_test_framework) - requires --debug and --e2e-test flags

**External Dependencies:**
- LoggingManager (existing, no changes)
- game_data_fetcher.fetch_game_data() (existing, no changes)
- config.py constants (existing, no changes)

---

### 7. Edge Cases & Error Handling

**Argument Validation Approach (Issue 7 Resolution):**
- **Weeks:** No validation (trust user input, invalid weeks return empty results from API)
- **Season:** No validation (API handles invalid seasons gracefully)
- **Log Level:** Validated by argparse choices only (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- **Philosophy:** Argparse choices for enums, no numeric range validation
- **Rationale:** Minimal validation reduces complexity, API provides error feedback

**Edge Case 1: Conflicting Flags**
- Scenario: `--debug --e2e-test --weeks 5-10`
- Behavior: --e2e-test takes highest priority, fetches week 1
- Logging: "E2E test mode: fetching week 1 only"

**Edge Case 2: Invalid Log Level with --debug**
- Scenario: `--debug --log-level ERROR`
- Behavior: --debug forces DEBUG level, --log-level ignored
- Logging: "Debug mode enabled: DEBUG logging active"

**Edge Case 3: E2E Mode with Historical Season**
- Scenario: `--season 2024 --e2e-test`
- Behavior: Fetches week 1 of 2024 season
- Expected: Week 1 games from 2024 in CSV

**Edge Case 4: Debug Mode with No Current Week Data**
- Scenario: --debug when current_week has no games
- Behavior: Empty games list, CSV with 0 rows
- Logging: "Total games: 0"

**Error Handling:**
- Invalid log level: argparse rejects with error (built-in)
- Invalid weeks format: existing error handling unchanged
- API errors: existing error handling unchanged

---

### 8. Documentation

**User-Facing Documentation:**
- Feature 09 (documentation) will update docs with new arguments
- README.md will show new flag examples
- Command-line help text (built into argparse --help)

**Developer Documentation:**
- Inline code comments for flag priority logic
- Docstrings unchanged (no new functions)
- This spec.md serves as implementation guide

---

### 9. User Approval

**Approval Required:** This is Gate 4 (MANDATORY) - Cannot proceed to S5 without user approval

- [x] **I approve these acceptance criteria**

**Approval Timestamp:** 2026-01-30

**Approval Notes:** User approved on 2026-01-30 with no modifications requested. All acceptance criteria confirmed as accurate.

---

## Cross-Feature Alignment

**Compared To:** Features 01-02, 04-07 (all Group 1 features)

**Alignment Status:** ✅ ALIGNED - No conflicts found

**Universal Flags Consistency:**
- ✅ --debug: Consistent implementation (DEBUG logging + single week fetch)
- ✅ --e2e-test: Consistent implementation (week 1 only, ≤3 min)
- ✅ --log-level: Consistent implementation (DEBUG/INFO/WARNING/ERROR/CRITICAL choices)

**Argument Naming - Backward Compatibility:**
- ⚠️ --output: Feature 03 uses (EXISTING argument, must preserve for backward compatibility)
- ✅ Pattern: New features use `--output-dir` or `--output-path`, Feature 03 keeps existing `--output`
- ✅ Documented rationale: Backward compatibility with existing run_game_data_fetcher.py argparse

**Flag Priority Logic:**
- ✅ Feature 03 documents clear precedence: --e2e-test > --weeks > --debug
- ✅ Consistent with other features' priority handling approaches

**No Conflicts Found:**
- No file overlap (run_game_data_fetcher.py unique to Feature 03)
- Backward compatibility preserved (existing --output argument kept)
- Follows universal flag patterns established across Group 1

**Verified By:** Primary Agent (S3 Final Consistency Loop)
**Date:** 2026-01-30

---

**Summary:**
- **Files Modified:** 1 existing file (~20 lines), 1 new test file (~120 lines)
- **Behavior:** 3 new flags, configurable logging, E2E mode ≤3 min, debug mode fast feedback
- **Testing:** 8-10 unit tests, >90% coverage
- **Dependencies:** Blocks Feature 08 only
- **Edge Cases:** 4 identified and handled
- **Scope:** Small, focused enhancement (2 checklist questions, 7 requirements)
