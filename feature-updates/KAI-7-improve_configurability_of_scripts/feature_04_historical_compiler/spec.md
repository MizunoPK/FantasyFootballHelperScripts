# Feature 04 Specification: Historical Compiler Configurability

**Status:** RESEARCH_PHASE (S2.P1 - Discovery Context Review)
**Created:** 2026-01-28
**Last Updated:** 2026-01-29

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Feature:** Feature 04 - historical_compiler (lines 303-322 in DISCOVERY.md)

**Purpose:** Enhance historical compiler with debug/E2E modes and additional args

**Initial Scope:**
- Enhance argparse (add --debug, --e2e-test, --timeout, --rate-limit-delay, --log-level)
- Add debug mode (DEBUG logging + single week compilation)
- Add E2E test mode (compile minimal dataset, ≤3 min)
- Unit tests for argument handling

**Estimated Size:** SMALL-MEDIUM

**Dependencies:** None

---

### Relevant Discovery Decisions

**Recommended Approach:** Option 2 - Comprehensive Script-Specific Argparse (DISCOVERY.md lines 179-196)

**Key Design Decisions:**
1. **Script-Specific Args:** Each runner gets args matching its config.py/constants.py settings
2. **Universal Flags:** --debug and --e2e-test on all 7 runners
3. **E2E Behavior:** --e2e-test triggers limited data compilation (≤3 min)
4. **Debug Behavior:** --debug triggers DEBUG log level + behavioral changes (single week, verbose output)
5. **Integration Test Validation:** Each test checks exit code AND specific expected outcomes

---

### Relevant User Answers (from Discovery)

**Question 1 (Script-specific arguments):**
- **Answer:** "Script specific... research to determine what arguments should be added... focus on constants.py settings"
- **Impact for Feature 04:** Research historical_data_compiler/constants.py for configurable settings

**Question 3 (E2E mode specifications):**
- **Answer:** "Simulations: single run with 0-1 random configs. Fetchers: real APIs with data limiting args"
- **Impact for Feature 04:** E2E mode should compile minimal dataset (single week, limited year range)

**Question 4 (Debug mode behavior):**
- **Answer:** "Option C: Both logging AND behavioral changes"
- **Impact for Feature 04:** --debug enables DEBUG logs + changes behavior (single week compilation, verbose output)

**Question 5 (Integration test validation):**
- **Answer:** "Check exit code AND verify expected outcomes (specific logs, result counts)"
- **Impact for Feature 04:** Integration tests must validate exit code + specific outcomes (files created, data integrity)

---

### Relevant Research Findings (from Discovery)

**Iteration 1 - Current State:**
- `compile_historical_data.py` (lines 1-60): **HAS argparse** with year, weeks, validate, clean
- Already has some argument support (ahead of player/schedule/league_helper)
- Uses argparse module

**Iteration 2 - Constants Research:**
- `historical_data_compiler/constants.py` (lines 1-157): **4 configurable constants**
  - REQUEST_TIMEOUT
  - RATE_LIMIT_DELAY
  - MIN_SUPPORTED_YEAR
  - REGULAR_SEASON_WEEKS
- These constants should become CLI arguments per User Answer Q1

---

## Initial Purpose (from S1 Breakdown)

Enhance historical data compiler with debug logging and E2E mode.

---

## Initial Scope (from S1 Breakdown)

- Enhance `compile_historical_data.py` with argument support
- Add debug logging throughout compilation process
- Create E2E test mode (fast compilation with minimal data, ~3 min)
- Unit tests for new arguments and logging

---

## Dependencies

- **Depends on:** None
- **Blocks:** None

---

## Components Affected

### Files to Modify

**1. `compile_historical_data.py` (lines 59-96, 249-307)**
- **Modify:** `parse_args()` function - add 5 new arguments
- **Modify:** `main()` function - add debug/E2E mode logic
- **Modify:** `compile_season_data()` function - accept timeout/rate-limit parameters
- **Source:** Derived (necessary to expose constants as CLI args per User Answer Q1)
- **Line numbers:** parse_args (59-96), main (249-307), compile_season_data (165-220)

**2. `historical_data_compiler/constants.py` (MODIFY - remove CLI-configurable constants)**
- **REMOVE:** REQUEST_TIMEOUT (line 98), RATE_LIMIT_DELAY (line 101) - these are now CLI-only
- **KEEP:** MIN_SUPPORTED_YEAR (line 85), REGULAR_SEASON_WEEKS (line 88) - non-CLI constants
- **Reasoning:** Epic architectural requirement - CLI arguments must be removed from config/constants files (single source of truth: argparse defaults)
- **Source:** Epic architectural pattern (Feature 10 reference) + User requirement (2026-02-01)
- **Reference:** See Feature 10 R8 for pattern

**3. `historical_data_compiler/http_client.py` (MODIFY - update default parameter values)**
- **Change needed** - BaseHTTPClient constructor uses REQUEST_TIMEOUT, RATE_LIMIT_DELAY as default values
- **Current signature (WILL BREAK after R8):** `__init__(self, timeout: float = REQUEST_TIMEOUT, rate_limit_delay: float = RATE_LIMIT_DELAY, user_agent: str = ESPN_USER_AGENT)` (lines 62-67)
- **New signature (after R8):** `__init__(self, timeout: float = 30.0, rate_limit_delay: float = 0.3, user_agent: str = ESPN_USER_AGENT)`
- **Reasoning:** R8 removes REQUEST_TIMEOUT, RATE_LIMIT_DELAY from constants.py, so hardcode defaults in constructor
- **Impact:** Backward compatible - same default values (30.0, 0.3), just hardcoded instead of from constants
- **Source:** Consistency verification - detected during S3 Step 3.2 (verify resolutions don't create new conflicts)

### Files to Create

**4. `tests/test_compile_historical_data_args.py` (NEW)**
- **Purpose:** Unit tests for argument parsing and mode behaviors
- **Pattern to follow:** Existing test files in tests/historical_data_compiler/ (pytest framework)
- **Test cases:** 6+ tests for argparse, debug mode, E2E mode, timeout/rate-limit
- **Source:** Discovery Q5 (integration tests validate exit code + outcomes) + Derived (unit tests required for new functionality)

**5. `tests/integration/test_compile_historical_data_integration.py` (NEW)**
- **Purpose:** Integration test for compile_historical_data.py main script
- **Pattern to follow:** Existing integration tests for simulations (mentioned in Discovery Iteration 1)
- **Test coverage:** Multiple argument combinations, debug mode, E2E mode
- **Source:** Epic Request (DISCOVERY.md line 393: "Create 7 individual test runners") + User Answer Q5 (validate exit code + outcomes)

---

## Requirements

### Requirement 1: Add --debug Flag

**Description:** Add universal --debug flag that enables debug mode

**Source:** Epic Request (DISCOVERY.md line 20: "add --debug...to compile_historical_data.py")

**Traceability:** User explicitly requested --debug as a universal flag across all 7 runners (DISCOVERY.md lines 206, 308)

**Implementation:**
- Add `--debug` flag to parse_args() (action="store_true")
- In main(), if args.debug: enable debug behavioral changes
- Debug behavioral changes (User Answer Q4):
  - Set log_level = "DEBUG"
  - Limit compilation to single week (week 1 only)
  - Use single year (first year in array or --year arg)
  - Skip cleanup on error (preserve partial output for debugging)

**Interaction with --e2e-test:**
- Source: User Answer to Checklist Q1 (Option D: Merge behaviors)
- If both --debug and --e2e-test are set:
  - Use DEBUG log level (from --debug)
  - Use E2E scope: weeks 1-2, fixed year 2024, fast timeouts (from --e2e-test)
  - Skip cleanup on error (from --debug)
  - This allows debugging the E2E mode itself

---

### Requirement 2: Add --e2e-test Flag

**Description:** Add universal --e2e-test flag that triggers fast E2E test mode (≤3 min)

**Source:** Epic Request (DISCOVERY.md line 20: "add --e2e-test...to compile_historical_data.py")

**Traceability:** User explicitly requested --e2e-test as universal flag (DISCOVERY.md lines 207, 309) + User Answer Q3 (compile minimal dataset with data limiting)

**Implementation:**
- Add `--e2e-test` flag to parse_args() (action="store_true")
- In main(), if args.e2e_test: trigger E2E mode
- E2E mode specifications (User Answer Q3):
  - Fixed year: 2024 (most recent complete season)
  - Limited weeks: weeks 1-2 only (instead of 1-17)
  - Faster HTTP settings: timeout=10s, rate_limit_delay=0.1s
  - JSON only: GENERATE_JSON=True, GENERATE_CSV=False
  - Target runtime: ≤3 minutes (estimated 1.8 minutes based on research)

**Interaction with --debug:**
- Source: User Answer to Checklist Q1 (Option D: Merge behaviors)
- If both --debug and --e2e-test are set:
  - Use DEBUG log level (from --debug)
  - Use E2E scope: weeks 1-2, fixed year 2024, fast timeouts (from --e2e-test)
  - Skip cleanup on error (from --debug)
  - This allows debugging the E2E mode itself

**Output Directory Handling:**
- Source: User Answer to Checklist Q2 (Option A: Append "_e2e" suffix)
- When --e2e-test is set:
  - Append "_e2e" suffix to year directory
  - Output path: `simulation/sim_data/2024_e2e/` (instead of `simulation/sim_data/2024/`)
  - This prevents overwriting production compilation data
  - Simple, safe approach that maintains existing directory structure patterns

**Interaction with --year argument:**
- Source: User Answer to Checklist Q6 (Option D: Warn and use E2E)
- When both --e2e-test and --year are set:
  - Print warning: "Warning: --year argument ignored when --e2e-test is set. Using fixed year 2024 for E2E reproducibility."
  - Use E2E fixed year (2024), ignore --year value
  - Maintains E2E reproducibility while providing user feedback
  - User is informed their --year argument was ignored

---

### Requirement 3: Add --timeout Argument

**Description:** Add --timeout argument to configure HTTP request timeout

**Source:** Derived from User Answer Q1 (script-specific args from constants.py) + Research finding (REQUEST_TIMEOUT constant at constants.py:98)

**Traceability:**
- User Answer Q1: "focus on constants.py settings"
- Discovery Iteration 2: Identified REQUEST_TIMEOUT as 1 of 4 configurable constants
- Research: BaseHTTPClient accepts timeout as constructor param (http_client.py:64)

**Implementation:**
- Add `--timeout` argument to parse_args() (type=float, default=30.0)
- Pass args.timeout to BaseHTTPClient constructor in compile_season_data()
- Modify compile_season_data() signature to accept timeout parameter

**Validation:**
- Source: User Answer to Checklist Q3 (Option A: Strict validation)
- Require: timeout > 0 and timeout <= 300 (5 minutes max)
- Validation happens in parse_args() or early in main()
- Error message if validation fails: "Timeout must be between 0 and 300 seconds"
- Prevents unreasonable timeout values while allowing flexibility within safe range

---

### Requirement 4: Add --rate-limit-delay Argument

**Description:** Add --rate-limit-delay argument to configure delay between API requests

**Source:** Derived from User Answer Q1 (script-specific args from constants.py) + Research finding (RATE_LIMIT_DELAY constant at constants.py:101)

**Traceability:**
- User Answer Q1: "focus on constants.py settings"
- Discovery Iteration 2: Identified RATE_LIMIT_DELAY as 1 of 4 configurable constants
- Research: BaseHTTPClient accepts rate_limit_delay as constructor param (http_client.py:65)

**Implementation:**
- Add `--rate-limit-delay` argument to parse_args() (type=float, default=0.3)
- Pass args.rate_limit_delay to BaseHTTPClient constructor in compile_season_data()
- Modify compile_season_data() signature to accept rate_limit_delay parameter

**Validation:**
- Source: User Answer to Checklist Q4 (Option B: Require minimum)
- Require: rate_limit_delay >= 0.05 (50ms minimum)
- Validation happens in parse_args() or early in main()
- Error message if validation fails: "Rate limit delay must be at least 0.05 seconds"
- Prevents API abuse by enforcing minimum delay, while allowing fast testing

---

### Requirement 5: Add --log-level Argument

**Description:** Add --log-level argument to configure logging verbosity

**Source:** Derived from Discovery Key Design Decision #4 (debug triggers DEBUG log level) + Common pattern from research (existing --verbose flag at compile_historical_data.py:85-87)

**Traceability:**
- Discovery Key Design Decision: "Debug Behavior: --debug triggers DEBUG log level + behavioral changes"
- Research finding: Existing --verbose flag controls log level (line 259: `log_level = "DEBUG" if args.verbose else "INFO"`)
- Derived: Need explicit log level control separate from --debug flag for flexibility

**Implementation:**
- Add `--log-level` argument to parse_args() (type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")
- In main(), use args.log_level for setup_logger() call

**Backward Compatibility with --verbose:**
- Source: User Answer to Checklist Q5 (Option B: Keep --verbose as alias)
- Keep existing --verbose/-v flag for backward compatibility
- When --verbose is set, treat it as shorthand for --log-level DEBUG
- Implementation logic:
  ```python
  if args.verbose:
      log_level = "DEBUG"
  elif args.debug:
      log_level = "DEBUG"
  else:
      log_level = args.log_level
  ```
- Maintains backward compatibility with existing scripts/workflows
- User-friendly approach (simpler --verbose vs --log-level DEBUG)

---

### Requirement 6: Unit Tests for Argument Handling

**Description:** Create unit tests for all new arguments and mode behaviors

**Source:** Epic Request (DISCOVERY.md line 23: "Unit tests for new arguments and logging")

**Traceability:** User explicitly requested unit tests for argument handling

**Implementation:**
- Create tests/test_compile_historical_data_args.py
- Test cases:
  - test_argparse_debug_flag()
  - test_argparse_e2e_test_flag()
  - test_argparse_timeout()
  - test_argparse_rate_limit_delay()
  - test_argparse_log_level()
  - test_debug_mode_limits_to_single_week()
  - test_e2e_mode_uses_fast_timeouts()
  - test_backward_compatibility_verbose_flag() (if --verbose kept)

---

### Requirement 7: Integration Tests

**Description:** Create integration test runner for compile_historical_data.py

**Source:** Epic Request (DISCOVERY.md lines 393-398: "Create 7 individual test runners... Each test validates exit code AND specific expected outcomes")

**Traceability:**
- Epic explicitly requests integration test runner for each script
- User Answer Q5: Tests check exit code AND verify expected outcomes (log counts, file existence, output validation)

**Implementation:**
- Create tests/integration/test_compile_historical_data_integration.py
- Test scenarios:
  - Test E2E mode completes in ≤3 minutes
  - Test debug mode creates partial output
  - Test various timeout/rate-limit combinations
  - Validate exit codes (0 for success, 1 for failure)
  - Validate expected outcomes (files created, data integrity)

---

### Requirement 8: Remove CLI-Configurable Constants from constants.py

**Description:** Remove REQUEST_TIMEOUT and RATE_LIMIT_DELAY from historical_data_compiler/constants.py (now CLI-only), keep non-CLI constants

**Source:** Epic Architectural Requirement (User decision 2026-02-01: "ensure all scripts remove CLI arguments from config/constants files")

**Traceability:**
- Epic-wide architectural pattern established by Feature 10 (refactor_player_fetcher)
- User explicitly requires CLI constants removed from all config/constants files
- Single source of truth: argparse defaults in runner scripts, NOT config files

**Implementation:**
- **REMOVE from constants.py:**
  - REQUEST_TIMEOUT = 30 (line 98) → Now in argparse default (--timeout default=30.0)
  - RATE_LIMIT_DELAY = 0.3 (line 101) → Now in argparse default (--rate-limit-delay default=0.3)

- **KEEP in constants.py (non-CLI):**
  - MIN_SUPPORTED_YEAR = 2009 (line 85) - internal constant, not user-configurable
  - REGULAR_SEASON_WEEKS = 18 (line 88) - internal constant, not user-configurable
  - ESPN_USER_AGENT (if exists) - internal constant
  - Any other non-CLI constants

- **Update imports in compile_historical_data.py:**
  - Remove: `from historical_data_compiler.constants import REQUEST_TIMEOUT, RATE_LIMIT_DELAY`
  - Keep: `from historical_data_compiler.constants import MIN_SUPPORTED_YEAR, REGULAR_SEASON_WEEKS`

- **Parameter passing:**
  - http_client.py already accepts timeout/rate_limit_delay as constructor params (lines 62-67)
  - Values flow: argparse → main() → compile_season_data() → BaseHTTPClient constructor

**Acceptance Criteria:**
- constants.py contains only non-CLI constants (MIN_SUPPORTED_YEAR, REGULAR_SEASON_WEEKS, etc.)
- REQUEST_TIMEOUT and RATE_LIMIT_DELAY removed from constants.py
- Clear header comment in constants.py: "Internal constants (not CLI-configurable)"
- All references updated to use parameter passing instead of constant imports
- No broken imports or undefined variable errors

**Reference Implementation:** Feature 10 spec.md R8 (Handle Non-CLI Constants)

---

## Data Structures

### Argument Namespace (argparse.Namespace)

**Structure:**
```python
args = argparse.Namespace(
    year: int | None = None,
    verbose: bool = False,  # Existing
    output_dir: Path | None = None,  # Existing
    debug: bool = False,  # NEW
    e2e_test: bool = False,  # NEW
    timeout: float = 30.0,  # NEW
    rate_limit_delay: float = 0.3,  # NEW
    log_level: str = "INFO"  # NEW
)
```

**Source:** Derived from requirements (combination of existing args + new args)

**No input/output data format changes** - this feature only enhances CLI arguments, doesn't modify compilation data structures

---

## Algorithms

### Debug Mode Algorithm

**Pseudocode:**
```python
if args.debug and args.e2e_test:
    # MERGE BEHAVIORS (User Answer to Checklist Q1: Option D)
    log_level = "DEBUG"  # From --debug
    year_array = [2024]  # From --e2e-test
    weeks_to_compile = [1, 2]  # From --e2e-test
    http_timeout = 10.0  # From --e2e-test
    http_rate_limit = 0.1  # From --e2e-test
    cleanup_enabled = False  # From --debug
    # Result: Debug logging + E2E scope + no cleanup

elif args.debug:
    # DEBUG MODE ONLY
    log_level = "DEBUG"

    # Limit compilation scope
    if args.year:
        year_array = [args.year]
    else:
        year_array = [YEARS[0]]  # First year only

    # Override week compilation (in compile_season_data)
    weeks_to_compile = [1]  # Week 1 only

    # Skip cleanup on error
    cleanup_enabled = False

else:
    # Normal mode
    log_level = args.log_level
    year_array = [args.year] if args.year else YEARS
    weeks_to_compile = range(1, REGULAR_SEASON_WEEKS + 1)
    cleanup_enabled = True
```

**Source:** Derived from User Answer Q4 (debug = behavioral changes + DEBUG logging) + User Answer to Checklist Q1 (merge behaviors when both flags set)

---

### E2E Test Mode Algorithm

**Note:** When both --debug and --e2e-test are set, see Debug Mode Algorithm above for merge behavior.

**Pseudocode:**
```python
if args.e2e_test and not args.debug:
    # E2E MODE ONLY (without debug)

    # Warn if --year argument provided (User Answer to Checklist Q6: Option D)
    if args.year:
        print("Warning: --year argument ignored when --e2e-test is set. Using fixed year 2024 for E2E reproducibility.")

    # Fixed compilation scope
    year_array = [2024]  # Fixed year for E2E (ignore args.year)
    weeks_to_compile = [1, 2]  # Weeks 1-2 only

    # Faster HTTP settings
    http_timeout = 10.0
    http_rate_limit = 0.1

    # JSON only
    GENERATE_JSON = True
    GENERATE_CSV = False

    # Output directory with "_e2e" suffix (User Answer to Checklist Q2: Option A)
    output_dir = Path("simulation/sim_data/2024_e2e")

    # E2E logging level
    # Default: INFO level (unless overridden by --log-level or --debug)
    # Consistency: Pattern from Feature 01, applied across all features
    if not args.debug:
        log_level = args.log_level if hasattr(args, 'log_level') else 'INFO'
else:
    # Use args values
    http_timeout = args.timeout
    http_rate_limit = args.rate_limit_delay
    # Use global GENERATE_JSON/CSV settings
```

**Source:** Derived from User Answer Q3 (E2E = limited data with faster settings) + User Answer to Checklist Q6 (warn and use E2E year)

---

### HTTP Client Initialization

**Pseudocode:**
```python
# Modified compile_season_data signature
async def compile_season_data(
    year: int,
    output_dir: Path,
    timeout: float = REQUEST_TIMEOUT,
    rate_limit_delay: float = RATE_LIMIT_DELAY
) -> None:
    # Create HTTP client with provided settings
    http_client = BaseHTTPClient(
        timeout=timeout,
        rate_limit_delay=rate_limit_delay
    )

    # ... rest of compilation ...
```

**Source:** Derived from research (http_client.py already accepts these params)

---

## Dependencies

**This feature depends on:**
- ✅ **argparse module** (already in use, compile_historical_data.py:23)
- ✅ **LoggingManager.setup_logger** (already imported, compile_historical_data.py:32)
- ✅ **BaseHTTPClient** (already imported, compile_historical_data.py:40)
- ✅ **Constants module** (already imported, compile_historical_data.py:33-39)

**No new dependencies required** - all necessary modules already exist

**What depends on this feature:**
- Feature 08: integration_test_framework (will use these new arguments for testing)

**Independent features (can be developed in parallel):**
- Features 01-03, 05-07 (other runner script enhancements)

**Source:** Research findings + DISCOVERY.md Feature Dependency Diagram (lines 434-444)

---

## Cross-Feature Alignment

**Compared To:**
- Feature 01: player_fetcher (S2 Complete)
- Feature 03: game_data_fetcher (S2 Complete)
- Feature 06: accuracy_simulation (S2 Complete)
- Feature 07: league_helper (S2 Complete)

**Alignment Status:** ✅ No conflicts - Fully aligned

**Components Affected:**
- ✅ No file overlap - Feature 04 modifies `compile_historical_data.py` only
- ✅ Other features modify different runner scripts (run_player_fetcher.py, run_game_data_fetcher.py, run_accuracy_simulation.py, run_league_helper.py)

**Universal Flags Consistency:**
- ✅ --debug: All features implement with DEBUG logging + behavioral changes (consistent)
- ✅ --e2e-test: All features implement with ≤3 min runtime, limited data (consistent)

**Argument Patterns:**
- ✅ All features expose constants.py/config.py settings as CLI arguments (consistent)
- ✅ Feature 04 exposes REQUEST_TIMEOUT, RATE_LIMIT_DELAY from historical_data_compiler/constants.py

**Feature-Specific: --verbose Flag (Issue 6 Resolution)**
- ⚠️ **ONLY Feature 04 has --verbose flag** (existing in compile_historical_data.py)
- **Reason:** Backward compatibility - script already has --verbose, must preserve
- **Other Features:** Use --log-level only (new argparse, no existing --verbose)
- **Behavior:** --verbose acts as alias for --log-level DEBUG (R5)
- **Precedence (Issue L2-4):** If both --verbose and --log-level specified, --verbose takes precedence

**Testing Approach:**
- ✅ All features add unit tests for argument parsing (consistent)
- ✅ All features add integration tests for E2E mode validation (consistent)

**Dependencies:**
- Feature 04 is independent of Features 01, 03, 06, 07
- Feature 08 (integration_test_framework) will depend on Feature 04's new arguments

**Changes Made:** None - zero conflicts found

**Verified By:** Secondary-C Agent
**Date:** 2026-01-30

---

## Acceptance Criteria

**Feature:** Feature 04 - Historical Compiler Configurability

**Created:** 2026-01-30
**Status:** Pending User Approval

---

### 1. Behavior Changes

**New Functionality:**
- ✅ CLI argument parsing for 5 new arguments (--debug, --e2e-test, --timeout, --rate-limit-delay, --log-level)
- ✅ Debug mode: Enables DEBUG logging + compiles single week + single year + preserves output on error
- ✅ E2E test mode: Compiles minimal dataset (year 2024, weeks 1-2, ≤3 minutes runtime)
- ✅ Configurable HTTP timeout via --timeout argument (validated: 0 < timeout <= 300 seconds)
- ✅ Configurable rate-limit delay via --rate-limit-delay argument (validated: >= 0.05 seconds)
- ✅ Explicit log level control via --log-level argument (DEBUG|INFO|WARNING|ERROR|CRITICAL)

**Modified Functionality:**
- ✅ --verbose flag kept for backward compatibility (acts as alias for --log-level DEBUG)
- ✅ E2E mode outputs to separate directory (2024_e2e) to avoid overwriting production data
- ✅ E2E mode warns and ignores --year argument to maintain reproducibility

**No Changes:**
- Compilation algorithm remains unchanged
- Data output formats remain unchanged (JSON/CSV)
- BaseHTTPClient interface unchanged (already accepts timeout/rate_limit_delay params)

---

### 2. Files Modified

**Existing Files Modified (1):**
- `compile_historical_data.py` (root directory)
  - Modify `parse_args()` function: Add 5 new arguments
  - Modify `main()` function: Add debug/E2E mode logic, argument validation
  - Modify `compile_season_data()` function: Accept timeout/rate_limit_delay parameters

**New Files Created (2):**
- `tests/test_compile_historical_data_args.py` (new unit test file)
  - 8+ unit tests for argument parsing and mode behaviors
- `tests/integration/test_compile_historical_data_integration.py` (new integration test file)
  - Integration tests for multiple argument combinations, E2E mode, debug mode

**No Changes:**
- `historical_data_compiler/constants.py` - No modifications (constants used as-is)
- `historical_data_compiler/http_client.py` - No modifications (already supports params)

---

### 3. Data Structures

**Modified Structures:**
- `argparse.Namespace` (argument structure)
  ```python
  args = argparse.Namespace(
      # Existing args (unchanged)
      year: int | None,
      verbose: bool,
      output_dir: Path | None,

      # New args
      debug: bool = False,
      e2e_test: bool = False,
      timeout: float = 30.0,
      rate_limit_delay: float = 0.3,
      log_level: str = "INFO"
  )
  ```

**No New Data Structures:**
- Compilation output format unchanged
- HTTP request/response structures unchanged
- Configuration data structures unchanged

---

### 4. API/Interface Changes

**Modified Function Signatures (1):**
- `compile_season_data()` signature updated:
  ```python
  # Before
  async def compile_season_data(year: int, output_dir: Path) -> None

  # After
  async def compile_season_data(
      year: int,
      output_dir: Path,
      timeout: float = REQUEST_TIMEOUT,
      rate_limit_delay: float = RATE_LIMIT_DELAY
  ) -> None
  ```

**New CLI Interface:**
- 5 new command-line arguments available to users
- Backward compatible (--verbose still works)

**No Changes:**
- BaseHTTPClient constructor interface unchanged
- LoggingManager.setup_logger interface unchanged
- Public module APIs unchanged

---

### 5. Testing

**Unit Tests:**
- Minimum 8 unit tests in `test_compile_historical_data_args.py`:
  - test_argparse_debug_flag()
  - test_argparse_e2e_test_flag()
  - test_argparse_timeout()
  - test_argparse_rate_limit_delay()
  - test_argparse_log_level()
  - test_debug_mode_limits_to_single_week()
  - test_e2e_mode_uses_fast_timeouts()
  - test_verbose_backward_compatibility()
  - test_debug_and_e2e_both_set()
  - test_timeout_validation()
  - test_rate_limit_delay_validation()
  - test_e2e_with_year_argument()

**Integration Tests:**
- Integration test file: `test_compile_historical_data_integration.py`
  - Test E2E mode completes in ≤3 minutes
  - Test debug mode creates partial output
  - Test various timeout/rate-limit combinations
  - Validate exit codes (0 for success, 1 for failure)
  - Validate expected outcomes (files created, data integrity)

**Coverage Target:**
- 100% coverage for new argument parsing logic
- 100% coverage for debug/E2E mode logic
- All edge cases tested (validation failures, flag conflicts)

**Edge Cases Tested:**
- Both --debug and --e2e-test set (merge behaviors)
- Both --e2e-test and --year set (warn and use E2E year)
- Invalid timeout values (< 0 or > 300)
- Invalid rate-limit-delay values (< 0.05)
- --verbose with --log-level (--verbose takes precedence)

---

### 6. Dependencies

**Feature Dependencies:**
- **Depends on:** None (independent feature)
- **Blocks:** None
- **Used by:** Feature 08 (integration_test_framework) will use new arguments for testing

**External Dependencies:**
- ✅ argparse (standard library - already in use)
- ✅ LoggingManager.setup_logger (already imported)
- ✅ BaseHTTPClient (already imported)
- ✅ Constants module (already imported)

**No New Dependencies Required**

---

### 7. Edge Cases & Error Handling

**Edge Cases Handled:**
1. **Debug + E2E conflict:** Merge behaviors (DEBUG logs + E2E scope)
2. **E2E + --year conflict:** Warn user, use E2E year (2024) for reproducibility
3. **Invalid timeout:** Validate 0 < timeout <= 300, error message if fails
4. **Invalid rate-limit-delay:** Validate >= 0.05, error message if fails
5. **E2E output directory:** Append "_e2e" suffix to prevent overwriting production data
6. **Backward compatibility:** --verbose flag kept as alias for --log-level DEBUG

**Error Conditions:**
- Timeout validation failure: "Timeout must be between 0 and 300 seconds"
- Rate-limit-delay validation failure: "Rate limit delay must be at least 0.05 seconds"
- E2E + --year warning: "Warning: --year argument ignored when --e2e-test is set. Using fixed year 2024 for E2E reproducibility."

---

### 8. Documentation

**User-Facing Documentation:**
- Update compile_historical_data.py --help output with new arguments
- Document debug mode behavior (DEBUG logs + single week + single year)
- Document E2E mode behavior (≤3 min, weeks 1-2, year 2024, separate output directory)
- Document argument validation rules (timeout, rate-limit-delay)

**Developer Documentation:**
- Code comments in parse_args() explaining new arguments
- Code comments in main() explaining debug/E2E mode logic
- Test documentation in test files explaining edge cases
- DISCOVERY.md already documents epic-level design decisions

---

### 9. User Approval

**Status:** ✅ APPROVED

**Approval Checkbox:**
- [x] I approve these acceptance criteria for Feature 04 (historical_compiler)

**Timestamp:** 2026-01-30

**Notes:** User approved acceptance criteria - Feature 04 S2 phase complete

---

**End of Detailed Specification**
