# Feature 01 Specification: Player Fetcher Configurability

**Status:** IN PROGRESS (S2.P1 - Research Phase)
**Created:** 2026-01-28
**Last Updated:** 2026-01-29 (Discovery Context added)

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature 01: player_fetcher**
- Add comprehensive argparse with 13+ arguments (--week, --output-dir, --create-csv, --create-json, --create-excel, --create-position-json, --enable-historical-save, --enable-game-data, --preserve-locked, --log-level, --progress-frequency, --debug, --e2e-test)
- Add debug mode (DEBUG logging + minimal data fetch)
- Add E2E test mode (fetch limited player set, ≤3 min)
- Unit tests for argument handling
- **Role:** Establishes patterns for other fetcher scripts
- **Estimated Size:** SMALL-MEDIUM

### Relevant Discovery Decisions

**Recommended Approach:** Comprehensive Script-Specific Argparse
- Each runner script gets full argparse implementation
- Script-specific arguments derived from constants.py/config.py files
- Universal --debug and --e2e-test flags across all 7 scripts
- Integration test framework to validate argument combinations

**Epic-Level Design Decisions:**
1. CLI arguments ONLY (no configuration files - out of scope)
2. Debug mode = behavioral changes + DEBUG logging (not just log level)
3. E2E test mode uses real APIs with data limiting (no mocking)
4. Integration tests validate exit codes AND expected outcomes

### Relevant User Answers (from Discovery)

**Q1: What specific arguments should each runner script accept?**
- Answer: Script-specific arguments focusing on constants.py settings
- Impact: Player fetcher gets 11+ arguments from player-data-fetcher/config.py constants

**Q3: What makes an E2E run "reasonable" (3 min max)?**
- Answer: Fetchers use real APIs with data-limiting arguments
- Impact: E2E mode for player_fetcher = fetch limited player set with real API

**Q4: Should debug mode be log level or different behavior?**
- Answer: Option C - Both logging AND behavioral changes
- Impact: Debug mode changes behavior (minimal data) + enables DEBUG logs

**Q5: How should integration tests determine pass/fail?**
- Answer: Check exit code AND verify expected outcomes
- Impact: Integration test runner must validate specific logs/result counts

### Discovery Basis for This Feature

**From Research Iteration 2:**
- player-data-fetcher/config.py has 11 frequently-modified constants identified
- These become the script-specific arguments for this feature

**From User Answers:**
- Q1: Script-specific args from constants
- Q3: Fetchers use real APIs with data limiting
- Q4: Debug = behavioral changes + DEBUG logs

---

## Feature Purpose

Add comprehensive argument support and debug/E2E modes to player data fetcher, establishing the pattern for other fetcher scripts in this epic.

---

## Dependencies

- **Depends on:** None (first feature, establishes patterns for Features 02-04)
- **Blocks:** None
- **Benefits:** Features 02-04 (other fetchers) will follow this feature's patterns

---

---

## Components Affected

### Files to Modify

**1. `run_player_fetcher.py` (52 lines)**
- **Location:** Project root
- **Modifications:** Add complete argparse implementation with main() function
- **Source:** Epic Request (DISCOVERY.md:243-244 - "Add argparse with 13+ arguments")
- **Pattern:** Follow run_game_data_fetcher.py:54-173 (argparse pattern)
- **Methods to Add:**
  - `main()` - New entry point with ArgumentParser
  - Argument parsing for 21+ CLI flags
  - Config override logic before subprocess call

**2. `player-data-fetcher/config.py` (90 lines)**
- **Location:** player-data-fetcher/
- **Modifications:** None (constants read as-is, overridden at runtime)
- **Source:** Derived (config provides defaults, CLI args override)
- **Note:** 21 constants identified (lines 13-58) become CLI arguments

**3. `player-data-fetcher/player_data_fetcher_main.py` (645 lines)**
- **Location:** player-data-fetcher/
- **Modifications:** None required (config overrides happen before import)
- **Source:** Derived (receives config via module-level constants)
- **Integration Point:** Settings class (line 42) reads from config

### Files to Create

**None** - All work done by modifying existing run_player_fetcher.py

### Dependencies on Existing Code

- **utils/LoggingManager:** Already exists (used in player_data_fetcher_main.py:26)
- **subprocess module:** Standard library
- **argparse module:** Standard library
- **pathlib.Path:** Standard library

---

## Requirements

### Requirement 1: CLI Argument Support (21 arguments)

**Description:** Add argparse to run_player_fetcher.py accepting 21 arguments from config.py constants

**Source:** Epic Request (DISCOVERY.md:243-244 - "Add argparse with 13+ arguments")

**Traceability:** User explicitly requested "comprehensive argparse" with script-specific arguments from constants.py

**Implementation:**
- Create ArgumentParser in main() function
- Add 21 arguments corresponding to config.py constants (lines 13-58)
- All arguments have `default=None` to distinguish "not provided" vs explicit value
- Override config.py constants before importing player_data_fetcher_main

**Argument Naming Convention:**
- **Source:** User Answer to Question 1 (checklist.md)
- **Decision:** Use concise naming (e.g., `--week` not `--current-week`)
- **Rationale:** Better usability, clearer mapping to config constants

**Arguments to Add:**

**Week/Season Arguments:**
1. `--week` → CURRENT_NFL_WEEK (int, default from config: 17)
2. `--season` → NFL_SEASON (int, default from config: 2025)

**Data Preservation Arguments:**
3. `--preserve-locked` → PRESERVE_LOCKED_VALUES (bool flag, default: False)
4. `--load-drafted-data` / `--no-load-drafted-data` → LOAD_DRAFTED_DATA_FROM_FILE (bool, default: True)
5. `--drafted-data-file` → DRAFTED_DATA (str path, default: "../data/drafted_data.csv")
6. `--my-team-name` → MY_TEAM_NAME (str, default: "Sea Sharp")

**Output Format Arguments:**
7. `--output-dir` → OUTPUT_DIRECTORY (str path, default: "./data")
8. `--create-csv` / `--no-csv` → CREATE_CSV (bool, default: True)
9. `--create-json` / `--no-json` → CREATE_JSON (bool, default: False)
10. `--create-excel` / `--no-excel` → CREATE_EXCEL (bool, default: False)
11. `--create-condensed-excel` / `--no-condensed-excel` → CREATE_CONDENSED_EXCEL (bool, default: False)
12. `--create-position-json` / `--no-position-json` → CREATE_POSITION_JSON (bool, default: True)
13. `--position-json-output` → POSITION_JSON_OUTPUT (str path, default: "../data/player_data")

**File Path Arguments:**
14. `--team-data-folder` → TEAM_DATA_FOLDER (str path, default: '../data/team_data')
15. `--game-data-csv` → GAME_DATA_CSV (str path, default: '../data/game_data.csv')

**Feature Toggle Arguments:**
16. `--enable-historical-save` / `--no-historical-save` → ENABLE_HISTORICAL_DATA_SAVE (bool, default: False)
17. `--enable-game-data` / `--no-game-data` → ENABLE_GAME_DATA_FETCH (bool, default: True)

**Logging Arguments:**
18. `--log-level` → LOGGING_LEVEL (str choice: DEBUG/INFO/WARNING/ERROR, default: 'INFO')
19. `--log-to-file` / `--no-log-file` → LOGGING_TO_FILE (bool, default: False)
20. `--log-file` → LOGGING_FILE (str path, default: './data/log.txt')
21. `--progress-frequency` → PROGRESS_UPDATE_FREQUENCY (int, default: 10)

**Special Mode Arguments:**
22. `--debug` → Trigger debug mode (see Requirement 2)
23. `--e2e-test` → Trigger E2E test mode (see Requirement 3)

---

### Requirement 2: Debug Mode

**Description:** Add --debug flag that enables DEBUG logging AND behavioral changes

**Source:** Epic Request (DISCOVERY.md:245 - "Add debug mode (DEBUG logging + minimal data fetch)") + User Answer Q4

**Traceability:** Discovery Q4 answer specified "Option C: Both logging AND behavioral changes"

**Debug Mode Behavior:**

**Logging Changes:**
- Set LOGGING_LEVEL = 'DEBUG'
- Enable verbose API response logging
- Show detailed progress tracking

**Behavioral Changes:**
- Set ESPN_PLAYER_LIMIT = 100 (vs 2000 default) - faster execution
- Set PROGRESS_UPDATE_FREQUENCY = 5 (vs 10 default) - more frequent updates
- Set ENABLE_GAME_DATA_FETCH = False - skip expensive game data operation
- Set ENABLE_HISTORICAL_DATA_SAVE = False - skip file I/O overhead

**Output Format Changes:**
- **Source:** User Answer to Question 4 (checklist.md)
- Set CREATE_CSV = True (keep - fast, essential data folder output)
- Set CREATE_JSON = False (disable - not essential)
- Set CREATE_EXCEL = False (disable - slow)
- Set CREATE_CONDENSED_EXCEL = False (disable - slow)
- Set CREATE_POSITION_JSON = True (keep - fast, goes to data/player_data folder)

**Mode Combination:**
- **Source:** User Answer to Question 3 (checklist.md)
- **If both --debug and --e2e-test specified:** E2E takes precedence for data limiting, debug adds DEBUG logging
- **Precedence rule:** E2E controls ESPN_PLAYER_LIMIT and feature flags, debug controls LOGGING_LEVEL

**Implementation:**
```python
# Apply debug mode first
if args.debug:
    config.LOGGING_LEVEL = 'DEBUG'
    config.ESPN_PLAYER_LIMIT = 100
    config.PROGRESS_UPDATE_FREQUENCY = 5
    config.ENABLE_GAME_DATA_FETCH = False
    config.ENABLE_HISTORICAL_DATA_SAVE = False
    # Force minimal output formats (User Answer Q4)
    config.CREATE_CSV = True
    config.CREATE_JSON = False
    config.CREATE_EXCEL = False
    config.CREATE_CONDENSED_EXCEL = False
    config.CREATE_POSITION_JSON = True

# Apply E2E mode second (overrides data limiting if both specified)
if args.e2e_test:
    config.ESPN_PLAYER_LIMIT = 100  # E2E precedence
    config.ENABLE_GAME_DATA_FETCH = False
    config.ENABLE_HISTORICAL_DATA_SAVE = False
    config.CREATE_EXCEL = False
    config.CREATE_JSON = False
    # Note: If debug was set, LOGGING_LEVEL stays 'DEBUG' (not overridden)
```

---

### Requirement 3: E2E Test Mode

**Description:** Add --e2e-test flag for fast end-to-end testing (≤3 minutes)

**Source:** Epic Request (DISCOVERY.md:246 - "Add E2E test mode (fetch limited player set, ≤3 min)") + User Answer Q3

**Traceability:** Discovery Q3 answer specified "Fetchers: real APIs with data-limiting args"

**E2E Mode Behavior:**

**API Limiting:**
- Set ESPN_PLAYER_LIMIT = 100 (vs 2000 default) - moderate data fetch
- **Source:** User Answer to Question 2 (checklist.md) - balances speed with coverage
- Use real ESPN API (no mocking per Q3 answer)

**Feature Disabling:**
- Set ENABLE_GAME_DATA_FETCH = False - skip game data
- Set ENABLE_HISTORICAL_DATA_SAVE = False - skip historical save
- Set CREATE_EXCEL = False - skip slow Excel generation
- Set CREATE_JSON = False - only CSV for speed
- Set CREATE_POSITION_JSON = True - keep position JSONs (fast)

**Logging:**
- **Source:** User Answer to Question 5 (checklist.md)
- Keep LOGGING_LEVEL = 'INFO' (not DEBUG) - cleaner output for workflow validation
- Note: Use `--debug --e2e-test` together for verbose E2E debugging

**Implementation:**
```python
if args.e2e_test:
    config.ESPN_PLAYER_LIMIT = 100  # User Answer Q2: Balance speed with coverage
    config.ENABLE_GAME_DATA_FETCH = False
    config.ENABLE_HISTORICAL_DATA_SAVE = False
    config.CREATE_EXCEL = False
    config.CREATE_JSON = False
```

**Open Questions:**
1. Should E2E mode enable DEBUG logging? → Question 5 in checklist

---

### Requirement 4: Config Override Pattern

**Description:** Override config.py constants from CLI arguments before importing main module

**Source:** Derived (necessary to pass arguments to underlying fetcher)

**Traceability:** Player fetcher uses config.py module-level constants (lines 13-58), Settings class reads from config (player_data_fetcher_main.py:42-69). Override pattern established in run_game_data_fetcher.py:105-124.

**Implementation Pattern:**
```python
# After parsing args
import sys
sys.path.insert(0, str(fetcher_dir))

# Import config module
from player-data-fetcher import config

# Override config constants with args
if args.week is not None:
    config.CURRENT_NFL_WEEK = args.week
if args.season is not None:
    config.NFL_SEASON = args.season
# ... etc for all 21 arguments

# Then import and run main (config overrides will be picked up)
from player-data-fetcher import player_data_fetcher_main
import asyncio
asyncio.run(player_data_fetcher_main.main())
```

---

### Requirement 5: Help Text and Documentation

**Description:** Each argument includes clear help text describing purpose and default

**Source:** Derived (standard argparse best practice for usability)

**Traceability:** Users need to understand what each argument does. Help text prevents incorrect usage.

**Implementation:**
```python
parser.add_argument(
    '--week',
    type=int,
    default=None,
    help='Current NFL week (1-18). Default: 17 from config'
)
```

**Help Text Pattern:**
- Describe what argument controls
- Specify valid range/values
- Show default value from config
- Indicate if optional or required

---

### Requirement 6: Error Handling

**Description:** Minimal validation - trust user input and let ESPN API validate

**Source:** User Answer to Question 6 (checklist.md) + Derived

**Traceability:** User chose no argument validation for simplicity - ESPN API will surface errors naturally

**Validation Approach:**
- **No range validation** for week, season, or numeric arguments
- **Argparse built-in validation only:**
  - Type checking (int for --week, str for paths)
  - Choices validation for --log-level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
  - Boolean flags (handled by argparse automatically)
- **Trust ESPN API** to reject invalid values with its own error messages
- **File path validation:** None (let Python I/O handle missing paths)

**Error Handling:**
- Argparse handles unknown arguments and type mismatches automatically
- ESPN API errors propagate naturally to user
- Python exceptions for file I/O handled by underlying fetcher code

---

### Requirement 7: Unit Tests

**Description:** Test argument parsing logic

**Source:** Epic Request (DISCOVERY.md:247 - "Unit tests for argument handling")

**Test Cases:**
- Test default values (no args provided)
- Test individual argument overrides
- Test debug mode config changes (including output format overrides)
- Test E2E mode config changes
- Test combined --debug --e2e-test mode (verify precedence rules)
- Test argparse type validation (invalid type for --week)
- Test argparse choices validation (invalid --log-level)
- Test boolean flag handling (--create-csv vs --no-csv)

---

## Data Structures

### Naming Convention: Logging Variables (Issue L2-3 Resolution)

**CRITICAL: Capitalization distinguishes scope**

- **`LOGGING_LEVEL`** (ALL_CAPS): Module-level constant defined in config.py
- **`log_level`** (lowercase): Local variable/parameter passed to functions

**Examples:**
```python
# Module constant (defined once)
LOGGING_LEVEL = 'INFO'  # Default config value

# Local override (used in functions)
if args.debug:
    log_level = 'DEBUG'  # Overrides constant
else:
    log_level = LOGGING_LEVEL  # Uses constant

setup_logger(LOG_NAME, log_level)  # Pass local variable
```

**Rationale:** Python convention - UPPER_CASE for constants, lower_case for variables

**Consistency:** This pattern applies across ALL features (01-07)

---

### Argument Specifications

**Command-Line Interface:**

```bash
# Basic usage (all defaults from config)
python run_player_fetcher.py

# Specify week and season
python run_player_fetcher.py --week 15 --season 2024

# Debug mode
python run_player_fetcher.py --debug

# E2E test mode
python run_player_fetcher.py --e2e-test

# Custom output
python run_player_fetcher.py --output-dir ./custom_data --no-csv --create-json

# Full example
python run_player_fetcher.py \
  --week 15 \
  --season 2024 \
  --output-dir ./data/week15 \
  --create-csv \
  --create-json \
  --no-excel \
  --log-level DEBUG \
  --progress-frequency 5
```

### Config Override Mapping

| CLI Argument | Config Constant | Type | Default |
|--------------|-----------------|------|---------|
| --week | CURRENT_NFL_WEEK | int | 17 |
| --season | NFL_SEASON | int | 2025 |
| --preserve-locked | PRESERVE_LOCKED_VALUES | bool | False |
| --output-dir | OUTPUT_DIRECTORY | str | "./data" |
| --create-csv | CREATE_CSV | bool | True |
| --log-level | LOGGING_LEVEL | str | 'INFO' |
| --debug | Multiple overrides | - | See Req 2 |
| --e2e-test | Multiple overrides | - | See Req 3 |

(Full mapping in research/player_fetcher_RESEARCH.md)

---

## Algorithms

### Main Execution Flow

**Pseudocode:**
```python
def main():
    # 1. Parse arguments
    parser = argparse.ArgumentParser(description="...")
    # Add 23 arguments (21 config + debug + e2e-test)
    args = parser.parse_args()

    # 2. Setup paths
    script_dir = Path(__file__).parent
    fetcher_dir = script_dir / "player-data-fetcher"

    # 3. Import config module
    sys.path.insert(0, str(fetcher_dir))
    from player-data-fetcher import config

    # 4. Apply debug mode overrides (if --debug)
    if args.debug:
        config.LOGGING_LEVEL = 'DEBUG'
        config.ESPN_PLAYER_LIMIT = 100
        # ... (see Requirement 2)

    # 5. Apply E2E mode overrides (if --e2e-test)
    if args.e2e_test:
        config.ESPN_PLAYER_LIMIT = 50
        # ... (see Requirement 3)

    # 6. Apply individual argument overrides
    if args.week is not None:
        config.CURRENT_NFL_WEEK = args.week
    # ... for all 21 arguments

    # 7. Validate overridden values (optional)
    if config.CURRENT_NFL_WEEK < 1 or config.CURRENT_NFL_WEEK > 18:
        print(f"Error: Week must be 1-18, got {config.CURRENT_NFL_WEEK}")
        sys.exit(1)

    # 8. Import and run main fetcher
    from player-data-fetcher import player_data_fetcher_main
    import asyncio
    asyncio.run(player_data_fetcher_main.main())
```

### Debug vs E2E Mode Precedence

**Decision:** User Answer to Question 3 (checklist.md)
- Allow both flags together
- E2E takes precedence for data limiting (ESPN_PLAYER_LIMIT, feature flags)
- Debug adds DEBUG logging (LOGGING_LEVEL)
- Result: Fast E2E execution with verbose debug output

---

## Testing Strategy

### Unit Tests (tests/test_run_player_fetcher.py)

**Test Cases:**
1. Test default argument parsing (no args)
2. Test individual arguments override config
3. Test debug mode config changes
4. Test E2E mode config changes
5. Test argument validation (invalid values)
6. Test help text generation
7. Test boolean flag handling (--create-csv vs --no-csv)

**Mock Strategy:**
- Mock subprocess.run to avoid actually running fetcher
- Mock config module to verify overrides
- Mock asyncio.run to verify main() called

### Integration Test (for Feature 08)

**Will be created in Feature 08: integration_test_framework**
- Test multiple argument combinations
- Validate exit codes (0 = success)
- Verify expected outputs (CSV file created, log messages present)

---

## Open Questions for checklist.md

Based on spec creation, these genuine unknowns need user input:

1. **Argument Naming:** Use `--week` or `--current-week`? (Game fetcher uses `--current-week`)

2. **E2E Player Limit:** Is 50 players adequate for E2E testing, or should it be higher/lower?

3. **Debug vs E2E Exclusivity:** Should `--debug` and `--e2e-test` be mutually exclusive, or can both be used together?

4. **Debug Output Formats:** Should debug mode force specific output formats (e.g., only CSV), or respect existing config?

5. **E2E Logging Level:** Should E2E mode enable DEBUG logging, or keep at INFO level?

6. **Argument Validation:** Should week/season validation be strict (error on invalid) or lenient (warn but continue)?

---

## Cross-Feature Alignment

**Compared To:** Features 02-07 (all Group 1 features)

**Alignment Status:** ✅ ALIGNED - No conflicts found

**Universal Flags Consistency:**
- ✅ --debug: All features implement (DEBUG logging + behavioral changes)
- ✅ --e2e-test: All features implement (≤3 min runtime, limited data)
- ✅ --log-level: All features implement (DEBUG/INFO/WARNING/ERROR/CRITICAL choices)

**Argument Naming Patterns:**
- ✅ --output-dir: Used by Feature 01, 04 (directory outputs)
- ✅ --output-path: Used by Feature 02 (file output)
- ✅ --output: Used by Feature 03 (existing arg, backward compatibility)
- Pattern: `-dir` for directories, `-path` for single files, consistent across new args

**Debug Mode Behavioral Changes:**
- ✅ All features: DEBUG logging enabled
- ✅ All features: Reduce dataset size (Feature 01: 100 players, Feature 02: 6 weeks, Feature 03: single week, etc.)
- ✅ Pattern established: Debug = faster iteration with verbose logging

**E2E Mode Specifications:**
- ✅ All features: ≤3 min execution time
- ✅ All features: Use real data/APIs (no mocking)
- ✅ All features: Limited scope (Feature 01: 100 players, Feature 02: week 1, etc.)
- ✅ Consistent validation approach: Exit code + specific outcome verification

**No Conflicts Found:**
- No file overlap (each feature modifies different runner script)
- No conflicting requirements across features
- All features follow established patterns from Feature 01

**Verified By:** Primary Agent (S3 Final Consistency Loop)
**Date:** 2026-01-30

---

## Acceptance Criteria

### 1. Behavior Changes

**New Functionality:**
- `run_player_fetcher.py` accepts 23 CLI arguments (21 config overrides + --debug + --e2e-test)
- `--debug` mode enables DEBUG logging + reduces dataset size (100 players, CSV+position JSON only)
- `--e2e-test` mode enables fast E2E testing (100 players, <3 min execution, INFO logging)
- Combined `--debug --e2e-test` mode allows verbose E2E debugging

**Modified Functionality:**
- `run_player_fetcher.py` no longer hardcoded - all config values overridable via CLI
- Script execution flow: parse args → override config → import+run fetcher

**No Changes:**
- `player-data-fetcher/` module logic unchanged (config override happens before import)
- ESPN API integration unchanged
- Data processing algorithms unchanged

### 2. Files Modified

**Existing Files Modified:**
- `run_player_fetcher.py` (52 lines → ~200 lines estimated)
  - Add argparse with 23 arguments
  - Add main() function with config override logic
  - Add debug/E2E mode precedence handling

**No New Files Created:**
- All work done by enhancing existing runner script

**Data Files:**
- No changes to data folder structure or formats

### 3. Data Structures

**No New Data Structures:**
- Uses existing config.py constants
- No new classes or data formats

**Modified Structures:**
- Config override pattern: CLI args → config module attributes → Settings class

### 4. API/Interface Changes

**New CLI Interface:**
```bash
python run_player_fetcher.py [OPTIONS]

Options:
  --week INT                 Current NFL week (1-18)
  --season INT              NFL season year
  --preserve-locked         Preserve locked player values
  --output-dir PATH         Output directory for data files
  --create-csv / --no-csv   Create CSV output (default: yes)
  --create-json / --no-json Create JSON output (default: no)
  --create-excel / --no-excel Create Excel output (default: no)
  --log-level LEVEL         Logging level (DEBUG/INFO/WARNING/ERROR)
  --debug                   Enable debug mode (fast iteration)
  --e2e-test                Enable E2E test mode (≤3 min)
  ... (21 total config args + 2 mode flags)
```

**No Python API Changes:**
- player-data-fetcher module interface unchanged
- No breaking changes to internal APIs

### 5. Testing

**Unit Tests:**
- Location: `tests/test_run_player_fetcher.py` (new file)
- Test count: 8 test cases minimum
  - Test default argument parsing
  - Test individual config overrides
  - Test debug mode overrides (data + output formats)
  - Test E2E mode overrides
  - Test combined --debug --e2e-test precedence
  - Test argparse type validation
  - Test argparse choices validation (--log-level)
  - Test boolean flag handling

**Integration Tests:**
- Created in Feature 08 (integration_test_framework)
- Will validate: Exit codes, output files created, log messages present

**Coverage Target:**
- 100% of new argparse code in run_player_fetcher.py
- Config override logic fully tested

**Edge Cases:**
- Combined debug+E2E mode (precedence rules)
- Invalid argument types (handled by argparse)
- Missing optional arguments (defaults from config)

### 6. Dependencies

**Depends On:**
- None (first feature, establishes patterns)

**Blocks:**
- None (Features 02-04 benefit from patterns but not blocked)

**External Dependencies:**
- argparse (stdlib)
- subprocess (stdlib)
- pathlib (stdlib)
- All existing player-data-fetcher dependencies unchanged

### 7. Edge Cases & Error Handling

**Edge Cases Handled:**
- Both --debug and --e2e-test specified (E2E precedence for data, debug for logging)
- No arguments provided (all defaults from config.py)
- Boolean flags in different orders (argparse handles)

**Error Conditions:**
- Invalid argument types: argparse raises clear error
- Invalid --log-level choice: argparse shows valid choices
- ESPN API errors: Propagate naturally (no validation)
- File I/O errors: Handled by underlying fetcher

**NOT Handled (by design):**
- Argument range validation (week, season) - trust user + ESPN API
- File path existence validation - let Python I/O handle

### 8. Documentation

**User-Facing Documentation:**
- CLI help text (--help flag) - argparse auto-generates from argument help strings
- Will be documented in Feature 09 (documentation)

**Developer Documentation:**
- Inline comments in run_player_fetcher.py for config override pattern
- Docstring for main() function

### 9. User Approval

**Approval Status:** ✅ APPROVED

**Approval Checklist:**
- [x] All 6 checklist questions resolved to user's satisfaction
- [x] Acceptance criteria accurately reflect feature scope
- [x] No concerns about implementation approach
- [x] Ready to proceed to S3 (Cross-Feature Sanity Check)

**Approval Timestamp:** 2026-01-30

**Notes:** User approved specification without changes

---

**Note:** All requirements documented with traceability. S2.P3 Refinement Phase complete pending user approval.
