# Feature 02 Specification: Schedule Fetcher Configurability

**Status:** S2 COMPLETE (User approved acceptance criteria)
**Created:** 2026-01-28
**Last Updated:** 2026-01-30

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 02: schedule_fetcher**

Add argparse and debug/E2E modes to schedule fetcher.

From DISCOVERY.md Feature 02 section:
- Add argparse with arguments (--season, --output-path, --debug, --e2e-test, --log-level)
- Add debug mode (DEBUG logging)
- Add E2E test mode (fetch single week schedule, ≤3 min)
- Unit tests

**Dependencies:** None (benefits from Feature 01 patterns)

**Estimated Size:** SMALL

### Relevant Discovery Decisions

**Recommended Approach:** Comprehensive Script-Specific Argparse (Option 2)

Key design decisions from Discovery:
- **Script-Specific Args:** Each runner gets args matching its needs (schedule fetcher: season, output-path, log-level)
- **Universal Flags:** --debug and --e2e-test on all 7 runners
- **E2E Behavior:** Fetchers use real APIs with data limiting (single week fetch for schedule fetcher)
- **Debug Behavior:** DEBUG log level + behavioral changes (not specified for schedule fetcher yet, will research)

**Discovery Basis (from DISCOVERY.md):**
- Finding: schedule-data-fetcher has no config file (Iteration 2)
- User Answer Q1: Script-specific args from constants
- User Answer Q4: Debug mode with behavioral changes + logging

### Relevant User Answers (from Discovery)

**Question 1:** What specific arguments should each runner script accept beyond --debug and --e2e-test?
- **Answer:** Script-specific args focusing on constants.py settings for configurability
- **Impact:** Need to research schedule fetcher's code to identify configurable constants (Discovery found no config file)

**Question 3:** What makes an E2E run "reasonable" (3 min max)? What can be reduced/mocked?
- **Answer:** Fetchers: real APIs with data limiting args
- **Impact:** E2E test mode should fetch single week schedule using real API

**Question 4:** Should debug mode be a separate log level or different behavior entirely?
- **Answer:** Option C: Both logging AND behavioral changes
- **Impact:** Debug mode enables DEBUG logs + changes behavior (need to research what behavioral changes make sense)

**Question 5:** How should integration tests determine pass/fail?
- **Answer:** Check exit code AND verify expected outcomes (specific logs, result counts)
- **Impact:** Integration tests will validate exit code + expected schedule data outcomes

---

## Components Affected

### Files to Modify

**1. run_schedule_fetcher.py** (65 lines)
- **Current State:** No argparse, hardcoded NFL_SEASON = 2025 (line 25), hardcoded output path (line 32)
- **Modifications:**
  - Add argparse module import (line ~18)
  - Add parse_arguments() function (new, ~40 lines)
  - Modify main() to accept args parameter (line 28)
  - Pass args to ScheduleFetcher (line 35)
- **Source:** Epic Request - DISCOVERY.md line 263 "Add argparse with arguments"
- **Traceability:** Required to enable CLI argument support per epic intent

**2. schedule-data-fetcher/ScheduleFetcher.py** (241 lines)
- **Current State:** ScheduleFetcher.__init__ hardcodes log_level="INFO" (line 35)
- **Modifications:**
  - Modify `__init__(self, output_path: Path)` to accept `log_level: str = "INFO"` parameter (line 27)
  - Modify fetch_full_schedule() to accept optional weeks parameter for E2E mode (line 76)
- **Source:** Derived Requirement - Necessary to support --log-level and --e2e-test arguments
- **Traceability:** Cannot change log level without modifying ScheduleFetcher.__init__ signature

### Files to Create

**3. tests/root_scripts/test_run_schedule_fetcher.py** (new file)
- **Purpose:** Unit tests for argument parsing logic in run_schedule_fetcher.py
- **Pattern:** Follow existing test pattern from tests/root_scripts/test_root_scripts.py
- **Source:** Epic Request - DISCOVERY.md line 269 "Unit tests"
- **Traceability:** Required to verify argument handling works correctly

---

## Requirements

### R1: Add Argparse with 5 Arguments

**Description:** Add argparse module to run_schedule_fetcher.py with 5 command-line arguments

**Source:** Epic Request - DISCOVERY.md lines 265-266 "Add argparse with arguments (--season, --output-path, --debug, --e2e-test, --log-level)"

**Arguments:**
1. **--season** (type: int, default: 2025)
   - NFL season year to fetch
   - Source: Epic Request (explicit in DISCOVERY.md line 265)
   - Current hardcoded value: NFL_SEASON = 2025 (run_schedule_fetcher.py:25)

2. **--output-path** (type: str, default: "data/season_schedule.csv")
   - Output CSV file path
   - Source: Derived - Current hardcoded path needs to become configurable
   - Current value: Path(__file__).parent / "data" / "season_schedule.csv" (line 32)

3. **--log-level** (type: str, default: "INFO", choices: DEBUG/INFO/WARNING/ERROR/CRITICAL)
   - Logging level for ScheduleFetcher
   - Source: Epic Request (explicit in DISCOVERY.md line 265)
   - Will be passed to ScheduleFetcher.__init__

4. **--debug** (flag, default: False)
   - Enable debug mode (DEBUG logging + behavioral changes)
   - Source: Epic Request - DISCOVERY.md line 267 "Add debug mode"
   - Overrides --log-level when set

5. **--e2e-test** (flag, default: False)
   - Enable E2E test mode (single week fetch)
   - Source: Epic Request - DISCOVERY.md line 268 "Add E2E test mode (fetch single week schedule)"

**Implementation:**
- Create parse_arguments() function using argparse.ArgumentParser
- Pattern: Follow run_game_data_fetcher.py lines 56-80 for argparse setup
- Return parsed args object to main()

**Edge Cases:**
- If both --debug and --log-level provided → --debug takes precedence (DEBUG level)
- If both --debug and --e2e-test provided → both apply (DEBUG logging in E2E mode)

---

### R2: Debug Mode Behavior

**Description:** When --debug flag is set, enable DEBUG logging and reduce weeks fetched to 1-6

**Source:** User Answer Q4 from DISCOVERY.md: "Option C: Both logging AND behavioral changes" + User Answer to Checklist Q1

**Debug Behavioral Changes:**
1. **Set log level to DEBUG** (overrides --log-level argument)
   - Source: User Answer Q4 - "debug mode = behavioral changes + DEBUG logs"
   - Implementation: Pass level="DEBUG" to ScheduleFetcher.__init__

2. **Fetch weeks 1-6** (instead of full 1-18)
   - Source: User Answer to Checklist Q1 - "Have the debug mode be 6 weeks, so that we can include some bye weeks"
   - Justification: 6 weeks = ~1.5 seconds (vs 4-5 sec full season), includes bye weeks for testing
   - Current behavior: Fetches weeks 1-18 (ScheduleFetcher.py:93)
   - Modified behavior: Pass weeks=range(1, 7) to fetch_full_schedule()

**Implementation:**
- If args.debug is True:
  - Set log_level = "DEBUG"
  - Pass weeks=range(1, 7) to fetch_full_schedule()

---

### R3: E2E Test Mode Behavior

**Description:** When --e2e-test flag is set, fetch only week 1 schedule and validate all 32 NFL teams present

**Source:** User Answer Q3 from DISCOVERY.md: "Fetchers: real APIs with data limiting args" + User Answer to Checklist Q2

**E2E Behavioral Changes:**
1. **Fetch only week 1** (instead of weeks 1-18)
   - Source: Derived - User Answer Q3 specifies "data limiting" for fetchers
   - Justification: Single week = <1 minute (well under 3 min limit from DISCOVERY.md line 268)
   - Current: fetch_full_schedule loops weeks 1-18 (ScheduleFetcher.py:93)
   - Modified: Pass weeks=range(1, 2) to fetch_full_schedule()

2. **Use real ESPN API** (no mocking)
   - Source: User Answer Q3 - "Fetchers: real APIs with data limiting"
   - Implementation: No changes needed, already uses real API

3. **Use INFO logging** (unless overridden)
   - Source: Consistency with Feature 01 (E2E mode uses INFO level for clean output)
   - Default: INFO level logging (cleaner than DEBUG, more visible than WARNING)
   - Can be overridden: User can specify --log-level DEBUG or use --debug flag for verbose E2E
   - Implementation: Use default log_level unless --log-level or --debug specified

4. **Validate all 32 teams present**
   - Source: User Answer to Checklist Q2 - "Option C: Exit code + verify all 32 teams present in week 1"
   - Validation: Extract unique teams from week 1 schedule, verify count == 32
   - Fail if: Any team missing or duplicate team entries
   - Success message: "✓ E2E test passed: 32 teams validated in week 1"

**Implementation:**
- If args.e2e_test is True:
  - Pass weeks=range(1, 2) to fetch_full_schedule()
  - Extract all unique teams from schedule[1]
  - Verify len(unique_teams) == 32
  - Print "✓ E2E test passed: 32 teams validated" if successful
  - Return error code 1 if validation fails

---

### R4: Modify ScheduleFetcher.__init__ Signature

**Description:** Add log_level parameter to ScheduleFetcher class to support --log-level argument

**Source:** Derived Requirement - Necessary to fulfill R1 (--log-level argument)

**Derivation:** Current __init__ hardcodes level="INFO" (ScheduleFetcher.py:35). To support --log-level argument, must accept log_level parameter.

**Current Signature:**
```python
def __init__(self, output_path: Path):
    self.output_path = output_path
    self.logger = setup_logger(name="ScheduleFetcher", level="INFO")  # Hardcoded
```

**Modified Signature:**
```python
def __init__(self, output_path: Path, log_level: str = "INFO"):
    self.output_path = output_path
    self.logger = setup_logger(name="ScheduleFetcher", level=log_level)  # Use parameter
```

**Impact:**
- Backward compatible (default value preserves existing behavior)
- Enables log level configuration from CLI

---

### R5: Modify fetch_full_schedule() for E2E Mode

**Description:** Add optional weeks parameter to fetch_full_schedule() method to support E2E mode

**Source:** Derived Requirement - Necessary to fulfill R3 (E2E test mode)

**Derivation:** R3 requires fetching only week 1 for E2E mode. Current method hardcodes weeks 1-18 loop (line 93). Must accept weeks parameter.

**Current Signature:**
```python
async def fetch_full_schedule(self, season: int) -> Dict[int, Dict[str, str]]:
    for week in range(1, 19):  # Hardcoded 1-18
```

**Modified Signature:**
```python
async def fetch_full_schedule(self, season: int, weeks: range = range(1, 19)) -> Dict[int, Dict[str, str]]:
    for week in weeks:  # Use parameter
```

**Impact:**
- Backward compatible (default range preserves existing behavior)
- Enables single week fetch for E2E mode
- Supports debug mode week reduction (if user approves in checklist)

---

### R6: Unit Tests for Argument Handling

**Description:** Create unit tests for parse_arguments() function in run_schedule_fetcher.py

**Source:** Epic Request - DISCOVERY.md line 269 "Unit tests"

**Test Cases:**
1. Test default values (no arguments provided)
2. Test --season argument parsing
3. Test --output-path argument parsing
4. Test --log-level with valid choices
5. Test --log-level with invalid choice (should fail)
6. Test --debug flag (overrides --log-level)
7. Test --e2e-test flag
8. Test combination of --debug and --e2e-test

**Pattern:** Follow existing test structure from tests/root_scripts/test_root_scripts.py

---

## Data Structures

### Input Data

**ESPN API Response** (external, read-only)
- **URL:** https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
- **Parameters:** seasontype=2, week=N, dates=YYYY
- **Structure:**
  ```json
  {
    "events": [
      {
        "competitions": [
          {
            "competitors": [
              {"team": {"abbreviation": "KC"}},
              {"team": {"abbreviation": "BAL"}}
            ]
          }
        ]
      }
    ]
  }
  ```
- **Source:** Research - ScheduleFetcher.py lines 96-136
- **Normalization:** WAS → WSH (lines 130-131)

### Internal Representation

**schedule Dictionary** (in-memory)
- **Type:** `Dict[int, Dict[str, str]]`
- **Structure:** `{week_number: {team: opponent}}`
- **Example:** `{1: {'KC': 'BAL', 'BAL': 'KC'}, 2: {...}}`
- **Source:** Research - ScheduleFetcher.fetch_full_schedule return type (line 76)

**bye_weeks Dictionary** (computed)
- **Type:** `Dict[str, Set[int]]`
- **Structure:** `{team_abbrev: {bye_week_numbers}}`
- **Example:** `{'KC': {7}, 'BAL': {10}}`
- **Source:** Research - ScheduleFetcher._identify_bye_weeks (lines 158-188)

### Output Data

**season_schedule.csv** (file output)
- **Schema:** week, team, opponent
- **Example:**
  ```csv
  week,team,opponent
  1,KC,BAL
  1,BAL,KC
  7,KC,         # Bye week (empty opponent)
  ```
- **Source:** Research - ScheduleFetcher.export_to_csv (lines 212-234)
- **Weeks Exported:** 1-17 (not 18) per line 215

---

## Algorithms

### Algorithm 1: Argument Parsing

```
def parse_arguments():
    Create ArgumentParser with description

    Add argument --season:
        type = int
        default = 2025
        help = "NFL season year (default: 2025)"

    Add argument --output-path:
        type = str
        default = "data/season_schedule.csv"
        help = "Output CSV file path"

    Add argument --log-level:
        type = str
        default = "INFO"
        choices = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        help = "Logging level"

    Add argument --debug:
        action = "store_true"
        help = "Enable debug mode (DEBUG logging + reduced weeks)"

    Add argument --e2e-test:
        action = "store_true"
        help = "Enable E2E test mode (single week fetch)"

    Parse and return args
```

**Source:** Derived - Required to implement R1 (argparse)

---

### Algorithm 2: Main Execution Flow

```
async def main(args):
    # Determine log level
    if args.debug:
        log_level = "DEBUG"
    else:
        log_level = args.log_level

    # Determine output path
    output_path = Path(args.output_path)
    if not output_path.is_absolute():
        output_path = Path(__file__).parent / output_path

    # Create fetcher with log level
    fetcher = ScheduleFetcher(output_path, log_level)

    # Determine weeks to fetch
    if args.e2e_test:
        weeks = range(1, 2)  # Week 1 only
    elif args.debug:
        weeks = range(1, 7)  # Weeks 1-6 (User Answer Checklist Q1)
    else:
        weeks = range(1, 19)  # Full season

    # Fetch schedule
    schedule = await fetcher.fetch_full_schedule(args.season, weeks)

    if not schedule:
        print("ERROR: Failed to fetch schedule data")
        return 1

    # Validate E2E test (User Answer Checklist Q2)
    if args.e2e_test:
        if 1 not in schedule or len(schedule[1]) == 0:
            print("ERROR: E2E test failed - no games in week 1")
            return 1

        # Extract unique teams from week 1
        unique_teams = set()
        for team in schedule[1].keys():
            unique_teams.add(team)

        # Validate all 32 teams present
        if len(unique_teams) != 32:
            print(f"ERROR: E2E test failed - expected 32 teams, found {len(unique_teams)}")
            return 1

        print("✓ E2E test passed: 32 teams validated in week 1")

    # Export to CSV
    fetcher.export_to_csv(schedule)

    print(f"✓ Schedule successfully exported to {output_path}")
    return 0
```

**Source:** Derived - Orchestrates R1-R5 requirements

**Edge Cases:**
- Output path relative vs absolute (handle both)
- E2E test with missing teams (should fail with count message)
- Both --debug and --e2e-test (both apply, E2E overrides weeks)

---

## Dependencies

### Internal Dependencies

**1. utils/LoggingManager.py**
- **Status:** EXISTS (verified in research)
- **Used by:** ScheduleFetcher.__init__ (line 35)
- **Method:** setup_logger(name, level, ...)
- **Source:** Research - LoggingManager.py lines 45-50

**2. schedule-data-fetcher/ScheduleFetcher.py**
- **Status:** EXISTS (verified in research)
- **Used by:** run_schedule_fetcher.py (line 24)
- **Will modify:** __init__ signature, fetch_full_schedule signature
- **Source:** Research - ScheduleFetcher.py lines 19-241

### External Dependencies

**1. argparse** (Python stdlib)
- **Status:** Available in Python 3.x
- **Used by:** run_schedule_fetcher.py (new import)
- **Source:** Standard library

**2. ESPN API**
- **Status:** External dependency (real API, no mocking)
- **URL:** https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
- **Reliability:** Required for E2E mode per User Answer Q3
- **Source:** Research - ScheduleFetcher.py line 97

### Feature Dependencies

**Depends on:**
- None (independent feature)

**Blocks:**
- None (other features are independent)

**Benefits from:**
- Feature 01 (player_fetcher) - argparse patterns

**Source:** DISCOVERY.md line 271 "Dependencies: None (benefits from Feature 01 patterns)"

---

## Acceptance Criteria

**Will be defined in S2.P3 Phase 6 after checklist questions are resolved.**

---

## Acceptance Criteria (USER MUST APPROVE)

**Feature 02: Schedule Fetcher Configurability**

When this feature is complete, the following will be true:

### Behavior Changes

**New Functionality:**
1. Command-line argument support via argparse
   - `--season <year>`: NFL season year (default: 2025)
   - `--output-path <path>`: Output CSV file path (default: "data/season_schedule.csv")
   - `--log-level <level>`: Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL, default: INFO)
   - `--debug`: Enable debug mode (DEBUG logging + fetch weeks 1-6)
   - `--e2e-test`: Enable E2E test mode (fetch week 1 only, validate 32 teams)

2. Debug mode behavior
   - Sets log level to DEBUG (overrides --log-level)
   - Fetches only weeks 1-6 (instead of full 1-18)
   - Runtime: ~1.5 seconds (vs 4-5 seconds full season)
   - Includes bye weeks for testing

3. E2E test mode behavior
   - Fetches only week 1 schedule using real ESPN API
   - Validates all 32 NFL teams present in week 1
   - Exits with code 1 if validation fails (less than 32 teams)
   - Prints success message: "✓ E2E test passed: 32 teams validated in week 1"
   - Runtime: <1 minute (well under 3-minute target)

**Modified Functionality:**
1. `ScheduleFetcher.__init__` signature change
   - Before: `__init__(self, output_path: Path)`
   - After: `__init__(self, output_path: Path, log_level: str = "INFO")`
   - Backward compatible (default value preserves existing behavior)

2. `ScheduleFetcher.fetch_full_schedule` signature change
   - Before: `async def fetch_full_schedule(self, season: int)`
   - After: `async def fetch_full_schedule(self, season: int, weeks: range = range(1, 19))`
   - Backward compatible (default range preserves existing behavior)

**No Changes:**
- ESPN API integration unchanged (still uses real API)
- CSV export logic unchanged (schedule[1-17] export)
- Bye week detection logic unchanged
- Team abbreviation normalization unchanged (WAS → WSH)

---

### Files Modified

**Files Modified:**
1. `run_schedule_fetcher.py` (65 lines currently)
   - Add argparse module import
   - Add `parse_arguments()` function (~40 lines)
   - Modify `main()` to accept args parameter
   - Add weeks parameter calculation logic
   - Add E2E test validation logic
   - Estimated new length: ~140 lines (+75 lines)

2. `schedule-data-fetcher/ScheduleFetcher.py` (241 lines currently)
   - Modify `__init__` signature (line 27): Add log_level parameter
   - Modify `fetch_full_schedule` signature (line 76): Add weeks parameter
   - No new methods added
   - Estimated new length: ~242 lines (+1 line for parameter)

**Files Created:**
3. `tests/root_scripts/test_run_schedule_fetcher.py` (new file)
   - Purpose: Unit tests for argparse logic
   - Tests: 8 unit tests
     - Test default values (no arguments)
     - Test --season parsing
     - Test --output-path parsing
     - Test --log-level with valid/invalid choices
     - Test --debug flag behavior
     - Test --e2e-test flag behavior
     - Test --debug + --e2e-test combination
   - Estimated length: ~120 lines

**Files NOT Modified:**
- `data/season_schedule.csv` - Output file, not source code
- `utils/LoggingManager.py` - No changes needed, already supports log levels

---

### Data Structures

**No New Data Structures:**
- Uses existing `Dict[int, Dict[str, str]]` for schedule (weeks → team → opponent)
- Uses existing CSV format (week, team, opponent)

**Modified Function Signatures:**
1. `ScheduleFetcher.__init__`
   - New parameter: `log_level: str = "INFO"`

2. `ScheduleFetcher.fetch_full_schedule`
   - New parameter: `weeks: range = range(1, 19)`

---

### API/Interface Changes

**Modified Public Methods:**
1. `ScheduleFetcher.__init__(output_path: Path, log_level: str = "INFO")`
   - Added parameter: log_level (default "INFO" for backward compatibility)
   - Purpose: Allow CLI control of logging level

2. `ScheduleFetcher.fetch_full_schedule(season: int, weeks: range = range(1, 19))`
   - Added parameter: weeks (default range(1, 19) for backward compatibility)
   - Purpose: Enable week limiting for debug and E2E modes

**New Public Functions:**
1. `parse_arguments()` in run_schedule_fetcher.py
   - Returns: argparse.Namespace with parsed arguments
   - Purpose: Parse command-line arguments

**No API Changes:**
- All changes are backward compatible (default parameters preserve existing behavior)
- No existing method signatures broken
- Existing callers of ScheduleFetcher class will continue to work

---

### Testing

**New Tests:**
- Unit tests: 8 tests total
  - File: `tests/root_scripts/test_run_schedule_fetcher.py`
  - Coverage: Argument parsing, flag combinations, error conditions
- No integration tests needed (E2E test mode IS the integration test)

**Test Coverage:**
- Target: 100% coverage for new argparse logic
- Edge cases covered:
  - Missing arguments (defaults used)
  - Invalid --log-level choice (argparse error)
  - Both --debug and --e2e-test flags (E2E overrides weeks)
  - Relative vs absolute --output-path
  - E2E test with <32 teams (validation failure)

**Manual Testing (E2E Mode):**
- Run: `python run_schedule_fetcher.py --e2e-test`
- Expected: Fetches week 1, validates 32 teams, exits with code 0
- Time: <1 minute

---

### Dependencies

**This Feature Depends On:**
- NONE (independent feature)

**Features That Depend On This:**
- NONE (other features are independent)

**Benefits From:**
- Feature 01 (player_fetcher) - Argparse patterns to follow

**External Dependencies:**
- argparse (Python standard library, already available)
- ESPN API (already in use, no changes)

---

### Edge Cases & Error Handling

**Argument Validation Approach (Issue 7 Resolution):**
- **E2E Mode:** Validates 32 teams present in week 1 (outcome validation)
- **Weeks Argument:** No validation (trust user input + API response)
- **Log Level:** Validated by argparse choices (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- **Philosophy:** Minimal input validation, comprehensive outcome validation
- **Rationale:** ESPN API provides error feedback, E2E validates correctness

**Edge Cases Handled:**
1. Both --debug and --e2e-test flags provided
   - Behavior: --e2e-test overrides weeks (week 1 only)
   - Debug logging still applies
   - No conflict, both flags compatible

2. --debug overrides --log-level
   - If both provided: --debug wins (sets DEBUG level)
   - User sees DEBUG logs regardless of --log-level value

3. Relative --output-path
   - Behavior: Resolved relative to script directory
   - Example: "data/file.csv" → "{script_dir}/data/file.csv"

4. E2E test with <32 teams in week 1
   - Behavior: Print error message, exit code 1
   - Message: "ERROR: E2E test failed - expected 32 teams, found {N}"

5. E2E test with no games in week 1
   - Behavior: Print error message, exit code 1
   - Message: "ERROR: E2E test failed - no games in week 1"

**Error Conditions:**
1. Invalid --log-level choice
   - User sees: argparse error message with valid choices
   - System does: Exit with code 2 (argparse convention)

2. ESPN API failure (network error, API down)
   - User sees: "ERROR: Failed to fetch schedule data"
   - System does: Return exit code 1
   - Behavior: Same as before (existing error handling)

---

### Documentation

**User-Facing Documentation:**
- README.md will be updated in Feature 09 (documentation feature)
- This feature creates the infrastructure, Feature 09 documents it

**Developer Documentation:**
- Docstrings added to:
  - `parse_arguments()`: Argument descriptions and defaults
  - `main(args)`: Behavior with different argument combinations
- Inline comments added for:
  - Debug mode week range calculation
  - E2E test validation logic

---

## Cross-Feature Alignment

**Compared To:** Features 01, 03-07 (all Group 1 features)

**Alignment Status:** ✅ ALIGNED - No conflicts found

**Universal Flags Consistency:**
- ✅ --debug: Consistent implementation (DEBUG logging + 6 weeks instead of 18)
- ✅ --e2e-test: Consistent implementation (week 1 only, validate 32 teams, ≤3 min)
- ✅ --log-level: Consistent implementation (DEBUG/INFO/WARNING/ERROR/CRITICAL choices)

**Argument Naming Patterns:**
- ✅ --output-path: Feature 02 uses (single CSV file output)
- ✅ Consistent with pattern: `-path` for single files, `-dir` for directories
- ✅ No conflicts with other features (different scripts, different outputs)

**E2E Mode Validation:**
- ✅ Feature 02 validates 32 teams present (outcome verification)
- ✅ Consistent with User Answer Q5: Exit code + specific outcomes
- ✅ Other features have similar validation approaches

**Debug + E2E Combination:**
- ✅ Feature 02 allows both flags together (E2E precedence for weeks, debug for logging)
- ✅ Consistent with Features 01, 04-06 combination behaviors

**No Conflicts Found:**
- No file overlap (run_schedule_fetcher.py unique to Feature 02)
- No conflicting requirements
- Follows established patterns from Feature 01

**Verified By:** Primary Agent (S3 Final Consistency Loop)
**Date:** 2026-01-30

---

## User Approval

- [x] **I approve these acceptance criteria**

**Approval Timestamp:** 2026-01-30

**Approval Notes:**
User approved on 2026-01-30 with no modifications requested.

---

**Specification Status:** S2 COMPLETE (User approved acceptance criteria - 2026-01-30)
