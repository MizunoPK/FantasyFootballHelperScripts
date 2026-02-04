# Feature 05 Specification: Win Rate Simulation Configurability

**Status:** S2.P2 (Specification Phase - In Progress)
**Created:** 2026-01-28
**Last Updated:** 2026-01-29

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Purpose:** Add E2E mode and debug enhancements to win rate simulation

**From DISCOVERY.md Feature 05 Section (lines 323-343):**
- Enhance argparse (add --e2e-test flag)
- Add E2E test mode (single run, 0-1 random configs, ≤3 min)
- Enhance debug mode (already has --log-level, add behavioral changes for debug)
- Unit tests for E2E mode

**Estimated Size:** SMALL

### Relevant Discovery Decisions

**From Recommended Approach (lines 178-196):**
- **Script-Specific Args:** Each runner gets args matching its config.py/constants.py settings
- **Universal Flags:** --debug and --e2e-test on all 7 runners
- **E2E Behavior:** --e2e-test triggers simulations (single run, 0-1 configs)
- **Debug Behavior:** --debug triggers DEBUG log level + behavioral changes (fewer iterations, smaller datasets)

**From Research Findings - Iteration 1 (lines 48):**
- `run_win_rate_simulation.py` (lines 1-110): HAS argparse with mode, sims, baseline, workers, etc.

**From Research Findings - Iteration 2 (lines 77-78):**
- `run_win_rate_simulation.py` (lines 33-46): LOGGING_LEVEL, DEFAULT_SIMS, DEFAULT_WORKERS, DEFAULT_TEST_VALUES (already has extensive argparse)

### Relevant User Answers (from Discovery)

**User Answer Q3 (line 26):**
"Simulations: single run with 0-1 random configs. Fetchers: real APIs with data limiting args"
- **Impact:** E2E mode must use single simulation run with 0 or 1 random configuration (not multiple)
- **Implementation:** --e2e-test flag triggers single run mode with minimal random configs

**User Answer Q4 (line 27):**
"Option C: Both logging AND behavioral changes"
- **Impact:** Debug mode changes both logging level (to DEBUG) AND script behavior
- **Implementation:** --debug flag enables DEBUG logs + reduces iterations/configs for faster runs

**User Answer Q5 (line 28):**
"Check exit code AND verify expected outcomes (specific logs, result counts)"
- **Impact:** Integration tests must validate specific expected results, not just exit codes
- **Implementation:** Integration tests verify simulation results, log outputs, file creation

---

## Components Affected

### 1. run_win_rate_simulation.py (MODIFY)

**File:** `run_win_rate_simulation.py` (lines 1-421)
**Purpose:** Add --e2e-test and --debug flags, implement E2E and debug modes

**Source:** Epic Request (DISCOVERY.md lines 327-330)

**Modifications:**

1. **Add --e2e-test flag to argparse** (lines 94-214)
   - Source: Epic Request (DISCOVERY.md line 327 "add --e2e-test flag")
   - Add as global argument to main parser
   - Type: action='store_true' (boolean flag)
   - Help: "Run in E2E test mode (single run, minimal configs, ≤3 min)"

2. **Add --debug flag to argparse** (lines 94-214)
   - Source: Epic Request (DISCOVERY.md line 329 "add behavioral changes for debug") + User Answer Q4
   - Add as global argument to main parser
   - Type: action='store_true' (boolean flag)
   - Help: "Enable debug mode (DEBUG logging + reduced iterations/datasets)"

3. **Convert LOGGING_LEVEL constant to CLI-overridable variable** (line 33)
   - Source: Derived Requirement (necessary to support --debug flag)
   - Change from constant to variable that can be overridden by --debug flag
   - Default: 'INFO' (preserves current behavior)
   - Override: 'DEBUG' when --debug flag present

4. **Add E2E mode conditional logic** (after line 214, before mode execution)
   - Source: Epic Request (DISCOVERY.md line 328 "single run, 0-1 random configs, ≤3 min")
   - If --e2e-test flag: Force mode='single', args.sims=1, num_test_values=0
   - Override user-specified mode/sims/test-values when E2E enabled
   - Print E2E mode banner to stdout

5. **Add debug mode behavioral changes** (after line 214, before mode execution)
   - Source: User Answer Q4 "behavioral changes"
   - If --debug flag: Set LOGGING_LEVEL='DEBUG', reduce workers to 1, reduce sims
   - Override user-specified logging/workers when debug enabled
   - Print debug mode warning to stdout

### 2. tests/integration/test_simulation_integration.py (ENHANCE)

**File:** `tests/integration/test_simulation_integration.py` (lines 1-535)
**Purpose:** Add integration tests for E2E and debug modes

**Source:** Epic Request (DISCOVERY.md line 331 "Unit tests for E2E mode")

**Additions:**

1. **test_e2e_mode_completes_fast()** (new test method)
   - Source: Epic Request (DISCOVERY.md line 328 "≤3 min") + User Answer Q5
   - Verify: --e2e-test flag completes in ≤180 seconds
   - Verify: exit code 0
   - Verify: expected log message "RUNNING SINGLE CONFIG TEST"
   - Verify: results file created (optimal_* folder exists)

2. **test_debug_mode_behavioral_changes()** (new test method)
   - Source: User Answer Q4 "behavioral changes"
   - Verify: --debug flag enables DEBUG logging
   - Verify: workers reduced to 1
   - Verify: simulations reduced (fewer than default)
   - Verify: exit code 0

3. **test_e2e_and_debug_combined()** (new test method)
   - Source: Derived Requirement (ensure flags compatible)
   - Verify: Both --e2e-test and --debug work together
   - Verify: exit code 0

---

## Requirements

### R1: Add --e2e-test Flag

**Description:** Add --e2e-test boolean flag to run_win_rate_simulation.py argparse

**Source:** Epic Request (DISCOVERY.md Feature 05 line 327 "add --e2e-test flag")

**Traceability:** User explicitly requested E2E test mode flag in Discovery

**Implementation:**
- Add to main parser (not subparsers) so it works with all modes
- Type: `action='store_true'` (default: False)
- Help text: "Run in E2E test mode (single run, minimal configs, ≤3 min)"
- Position: After --use-processes argument
**Edge Cases:**
- When combined with mode subcommands (single/full/iterative): E2E overrides mode to 'single'
- When combined with --sims/--test-values: E2E overrides to minimal values
- When combined with --debug: Both apply (E2E behavior + DEBUG logging)

---

### R2: Add --debug Flag

**Description:** Add --debug boolean flag to enable debug mode (DEBUG logging + behavioral changes)

**Source:** User Answer Q4 (DISCOVERY.md line 27 "Both logging AND behavioral changes")

**Traceability:** User specified debug mode must include BOTH logging and behavioral changes (not just logging)

**Implementation:**
- Add to main parser (not subparsers) so it works with all modes
- Type: `action='store_true'` (default: False)
- Help text: "Enable debug mode (DEBUG logging + reduced iterations/datasets)"
- Triggers: LOGGING_LEVEL='DEBUG' + workers=1 + sims reduction

**Edge Cases:**
- When user also specifies --log-level: --debug takes precedence (sets to DEBUG)
- When combined with --e2e-test: Both apply independently
- When combined with --workers: Debug overrides to workers=1

---

### R2a: Add --log-level Argument

**Description:** Add --log-level argument to control logging verbosity

**Source:** Consistency with Features 01-04, 06-07 (universal argument pattern)

**Traceability:** All other features have --log-level for explicit logging control separate from --debug flag

**Implementation:**
- Add to main parser (not subparsers) so it works with all modes
- Type: `choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']`
- Default: 'INFO'
- Help text: "Set logging level (default: INFO)"
- Used to set LOGGING_LEVEL constant before setup_logger() call

**Edge Cases:**
- When --debug also specified: --debug takes precedence (forces DEBUG level)
- When neither specified: Use default INFO level

---

### R3: E2E Mode Triggers Single Run with Minimal Configs

**Description:** When --e2e-test flag present, force mode='single', sims=1, test_values=0

**Source:** User Answer Q3 (DISCOVERY.md line 26 "single run with 0-1 random configs")

**Traceability:** User specified E2E must use "single run with 0-1 random configs" (not multiple runs/configs)

**Variable Naming Clarification:**
**Source:** Loop 2 Issue L2-1 resolution
- **`args.test_values`**: Argparse argument (user-provided value or default)
- **Relationship**: E2E mode sets `args.test_values = 0` (overrides user value)
- **Consistency**: Use `args.test_values` throughout (not `num_test_values`)

**Implementation:**
- Check for --e2e-test flag after parsing args- If present:
  - Force `args.mode = 'single'` (use single mode, not iterative/full)
  - Force `args.sims = 1` (single simulation run)
  - Force `args.test_values = 0` (baseline config only, no test variations)
  - Force `season = '2025'` (use latest season for speed)
  - Print "E2E TEST MODE ENABLED" banner to stdout
- Preserve other user-specified args (--baseline, --output, --data)

**Rationale for test_values=0:**
- User Answer Q3: "0-1 random configs" interpreted as "zero OR one config variations"
- test_values=0 → baseline config only (1 total config) = FASTEST
- test_values=1 → baseline + 1 test value (2 configs) = SLOWER
- For ≤3 min requirement, use minimal (0) to ensure speed

**Edge Cases:**
- If user specified mode=full: E2E overrides to single (warn user)
- If user specified sims=100: E2E overrides to 1 (warn user)
- If user specified --test-values=5: E2E overrides to 0 (warn user)

---

### R4: Debug Mode Enables DEBUG Logging

**Description:** When --debug flag present, set LOGGING_LEVEL='DEBUG'

**Source:** User Answer Q4 (DISCOVERY.md line 27 "Both logging AND behavioral changes")

**Traceability:** User specified debug mode must enable DEBUG logging (part 1 of "both")

**Implementation:**
- Check for --debug flag after parsing args- If present:
  - Set `LOGGING_LEVEL = 'DEBUG'` (override hardcoded constant)
  - Call setup_logger() with DEBUG level (line 117)
  - Print "DEBUG MODE ENABLED" to stdout

**Edge Cases:**
- If LOGGING_LEVEL already defined: --debug overrides to DEBUG
- DEBUG logs include: parameter values, config paths, simulation progress

---

### R5: Debug Mode Reduces Workers and Simulations

**Description:** When --debug flag present, reduce workers to 1 and simulations to minimal

**Source:** User Answer Q4 (DISCOVERY.md line 27 "behavioral changes") + Discovery Approach line 31 "fewer iterations, smaller datasets"

**Traceability:** User specified debug mode must include "behavioral changes" (part 2 of "both"), and Recommended Approach specifies "fewer iterations, smaller datasets"

**Implementation:**
- Check for --debug flag after parsing args- If present:
  - Force `args.workers = 1` (single worker for deterministic execution)
  - Reduce `args.sims` if >5: set to 2 (minimal but still meaningful)
  - Reduce `args.test_values` if >1: set to 1 (minimal variations)
  - Print behavioral changes to stdout ("workers=1, sims reduced")

**Rationale:**
- workers=1: Ensures deterministic execution order (easier debugging)
- sims=2: Minimal but shows variation (1 sim = no statistical meaning)
- test_values=1: Minimal parameter variations (faster iteration)

**Edge Cases:**
- If user specified workers=8: Debug overrides to 1 (warn user)
- If user specified sims=1: Debug preserves 1 (don't reduce below 1)
- If combined with --e2e-test: E2E takes precedence for sims (E2E=1, debug ignored)

---

### R6: E2E Mode Completes in ≤3 Minutes

**Description:** E2E mode must complete entire run in ≤180 seconds

**Source:** Epic Request (DISCOVERY.md Feature 05 line 328 "≤3 min")

**Traceability:** User explicitly specified E2E mode must complete in ≤3 minutes maximum

**Implementation:**
- Use single mode with minimal params (mode='single', sims=1, num_test_values=0)
- Use single season data (season='2025', fastest)
- Rely on existing run_single_config_test() method (designed for "quick testing")
- **Runtime validated via integration test assertion (User Answer Q1 Checklist: Option C)**
- Integration test will fail if runtime >180 seconds, triggering optimization in S6

**Verification Approach (from User Answer Q1):**
- Runtime assertion added to test_e2e_mode_completes_fast() (see R7)
- If test fails: Optimize by reducing dataset size or simplifying baseline config
- No pre-measurement needed; TDD approach (write test, make it pass)

**Edge Cases:**
- If baseline config is very large: Integration test may fail, triggering optimization
- If data folder has >100K players: Integration test may fail, triggering optimization
- Optimization options: Reduce dataset size, simplify baseline config, use subset of seasons

---

### R7: Integration Tests Validate Exit Code AND Outcomes (Including Runtime Assertion)

**Description:** Integration tests must check exit code 0 AND verify specific expected outcomes, including ≤180 second runtime assertion for E2E mode

**Source:** User Answer Q5 (DISCOVERY.md line 28 "Check exit code AND verify expected outcomes") + User Answer Q1 Checklist (Option C: Add runtime assertion)

**Traceability:**
- User explicitly specified tests must validate BOTH exit code AND specific outcomes (not just exit code)
- User approved Option C: Add runtime assertion to integration test (fail if >3 min) for E2E verification

**Implementation:**
- test_e2e_mode_completes_fast():
  - Verify exit code 0
  - Verify stdout contains "RUNNING SINGLE CONFIG TEST"
  - Verify optimal_* folder created in output dir
  - **Verify completion time ≤180 seconds (ASSERTION - test fails if exceeds 3 min)**
  - **If assertion fails:** Optimization required during S6 (reduce dataset, simplify config)
- test_debug_mode_behavioral_changes():
  - Verify exit code 0
  - Verify log output contains DEBUG level messages
  - Verify workers=1 used (check log or result metadata)
  - Verify simulations reduced (check result count)

**Edge Cases:**
- If log output not accessible: Use alternative validation (file metadata, result counts)
- If stdout buffering issues: Flush stdout or use log file
- **If E2E runtime >180 seconds:** Test fails, optimization needed (reduce dataset size, simplify baseline config)

---

### R8: Remove CLI-Configurable Constants from Module

**Description:** Remove CLI-configurable logging constants from run_win_rate_simulation.py module-level definitions (use argparse defaults instead)

**Source:** Epic Architectural Requirement (User decision 2026-02-01: "ensure all scripts remove CLI arguments from config/constants files")

**Traceability:**
- Epic-wide architectural pattern established by Feature 10 (refactor_player_fetcher)
- User explicitly requires CLI constants removed from all config/constants files
- Single source of truth: argparse defaults in runner scripts, NOT module-level constants

**Current State (INCORRECT):**
```python
# run_win_rate_simulation.py lines 33-37
LOGGING_LEVEL = 'INFO'          # ← CLI-configurable, should NOT be module constant
LOGGING_TO_FILE = False         # ← Potentially CLI-configurable
LOGGING_FILE = './simulation/log.txt'  # ← Potentially CLI-configurable
LOGGING_FORMAT = 'standard'     # ← Non-CLI, can stay
```

**Implementation:**
- **REMOVE from module-level constants:**
  - LOGGING_LEVEL (line 33) → Use argparse default instead
  - LOGGING_TO_FILE (line 34) → If CLI-configurable, use argparse; if not, can stay
  - LOGGING_FILE (line 36) → If CLI-configurable, use argparse; if not, can stay

- **KEEP as module-level constants (non-CLI):**
  - LOGGING_FORMAT = 'standard' (line 37) - internal constant, not user-configurable via CLI

- **Architectural pattern:**
  ```python
  # CORRECT: Use argparse default
  parser.add_argument('--log-level', default='INFO', ...)  # Single source of truth

  # In main():
  setup_logger(args.log_level, ...)  # Use argparse value directly

  # NOT: LOGGING_LEVEL constant that gets overridden
  ```

**Acceptance Criteria:**
- No module-level LOGGING_LEVEL constant (use argparse default only)
- Logging configuration comes from argparse values, not module constants
- Non-CLI constants (if any) remain as module-level with clear comments
- All references updated to use args.log_level instead of LOGGING_LEVEL constant

**Reference Implementation:** Feature 10 spec.md R8 (Handle Non-CLI Constants)

**Note:** This aligns with Component Affected #1 line 81 ("Convert LOGGING_LEVEL constant to CLI-overridable variable"), but clarifies that "conversion" means REMOVAL of constant and use of argparse defaults

---

## Data Structures

### Command-Line Arguments (Input)

**Format:** argparse.Namespace object

**New fields:**
- `e2e_test` (bool): True if --e2e-test flag present, default False
- `debug` (bool): True if --debug flag present, default False

**Existing fields (unchanged):**
- `mode` (str): 'single', 'full', or 'iterative'
- `sims` (int): Number of simulations per config
- `baseline` (str): Path to baseline config folder
- `output` (str): Output directory path
- `workers` (int): Number of parallel workers
- `data` (str): Data folder path
- `test_values` (int): Number of test values per parameter
- `use_processes` (bool): Use ProcessPoolExecutor vs ThreadPoolExecutor

**Source:** Derived Requirement (argparse structure for new flags)

### Internal Representation

**No new data structures required.** Feature modifies existing argparse.Namespace and uses existing SimulationManager class.

**Source:** Derived from research (run_win_rate_simulation.py already has complete data flow)

### Output Format

**Output unchanged:** Existing output format (optimal_* folders with 5-file config structure)

**Source:** Research (SimulationManager.run_single_config_test outputs to optimal_* folders)

---

## Algorithms

### E2E Mode Algorithm

**Pseudocode:**
```python
# After parsing argsif args.e2e_test:
    print("=" * 80)
    print("E2E TEST MODE ENABLED")
    print("- Mode: single (overriding user-specified mode)")
    print("- Simulations: 1 (overriding user-specified sims)")
    print("- Test values: 0 (baseline config only)")
    print("- Season: 2025 (latest season for speed)")
    print("=" * 80)

    # Override args
    args.mode = 'single'
    args.sims = 1
    num_test_values = 0  # Baseline only
    season = '2025'  # Fast single-season test

    # E2E logging level (unless overridden by --debug or --log-level)
    # Default: INFO level for clean E2E output
    # Consistency: Pattern from Features 01-04
    if not args.debug:
        log_level = args.log_level if hasattr(args, 'log_level') else 'INFO'
    else:
        log_level = 'DEBUG'  # Debug takes precedence

# Continue with normal execution (mode-specific logic)
```

**Source:** Derived Requirement (implementation approach for User Answer Q3)

**Edge Cases:**
- If user specified conflicting args: Print override warnings
- If baseline config not found: Fail fast with clear error message

---

### Debug Mode Algorithm

**Pseudocode:**
```python
# After parsing argsif args.debug:
    print("=" * 80)
    print("DEBUG MODE ENABLED")
    print("- Logging level: DEBUG (verbose output)")
    print("- Workers: 1 (overriding user-specified workers)")
    print("- Simulations: reduced to 2 (if >5)")
    print("- Test values: reduced to 1 (if >1)")
    print("=" * 80)

    # Override logging
    LOGGING_LEVEL = 'DEBUG'

    # Override behavioral params
    args.workers = 1
    if args.sims > 5:
        args.sims = 2
    if args.test_values > 1:
        args.test_values = 1

# Call setup_logger with updated LOGGING_LEVEL (line 117)
setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
```

**Source:** Derived Requirement (implementation approach for User Answer Q4)

**Edge Cases:**
- If sims already ≤5: Don't reduce further (preserve user intent)
- If test_values already ≤1: Don't reduce (preserve minimum)
- If combined with --e2e-test: E2E sims override takes precedence

---

### Combined E2E + Debug Algorithm

**Precedence rules:**
1. E2E mode processes first (sets mode='single', sims=1, num_test_values=0)
2. Debug mode processes second (sets logging='DEBUG', workers=1, but sims already set by E2E)
3. Debug sims reduction skipped if --e2e-test present (E2E sims=1 takes precedence)

**Source:** Derived Requirement (ensure flags compose correctly)

**Pseudocode:**
```python
if args.e2e_test:
    # ... E2E logic ...
    args.sims = 1

if args.debug:
    LOGGING_LEVEL = 'DEBUG'
    args.workers = 1
    # Skip sims reduction if E2E already set it
    if not args.e2e_test and args.sims > 5:
        args.sims = 2
```

---

## Dependencies

### Dependencies (What This Feature Depends On)

**Existing Code:**
1. **LoggingManager** (`utils/LoggingManager.py`)
   - Status: EXISTS
   - Source: Research (run_win_rate_simulation.py line 117 uses setup_logger)
   - Used for: DEBUG logging setup when --debug flag present

2. **SimulationManager** (`simulation/win_rate/SimulationManager.py`)
   - Status: EXISTS
   - Source: Research (run_single_config_test method exists at line 1099)
   - Used for: E2E mode execution (run_single_config_test for fast testing)

3. **argparse** (Python standard library)
   - Status: EXISTS
   - Source: Research (run_win_rate_simulation.py lines 94-214 uses argparse)
   - Used for: Adding --e2e-test and --debug flags

**Other Features:**
- None (Feature 05 is independent, no dependencies on other features in this epic)

**Source:** Research (feature_05_win_rate_simulation_RESEARCH.md "Dependencies" section)

---

### Blocked By (What Blocks This Feature)

**Nothing blocks this feature.**

- Feature 05 can be implemented independently
- No dependencies on Features 01-04 or 06-09
- Benefits from Feature 01-04 patterns if working sequentially, but not required

**Source:** DISCOVERY.md Feature 05 line 334 "Dependencies: None"

---

### Blocks (What This Feature Blocks)

**Feature 08: integration_test_framework**
- Status: Feature 08 depends on ALL features 01-07 complete
- Source: DISCOVERY.md Feature 08 line 401 "Dependencies: Features 01-07"
- Impact: Feature 08 cannot start until Feature 05 complete (and Features 01-04, 06-07)

**Source:** DISCOVERY.md Feature 08 dependencies

---

## Acceptance Criteria

### 1. Behavior Changes

**New Functionality:**
- `run_win_rate_simulation.py` accepts two new flags: `--e2e-test` and `--debug`
- E2E test mode triggers single simulation run with minimal configs (≤3 min completion)
- Debug mode enables DEBUG logging AND reduces workers/simulations for faster iteration

**Modified Functionality:**
- LOGGING_LEVEL constant becomes CLI-overridable (--debug flag sets to DEBUG)
- Argument precedence: --e2e-test overrides mode/sims, --debug overrides logging/workers

**No Changes:**
- Existing simulation algorithms unchanged
- Existing argparse arguments preserved (backward compatible)
- Output format unchanged (optimal_* folders)

---

### 2. Files Modified

**New Files:** None

**Existing Files Modified:**
1. `run_win_rate_simulation.py` (lines 33, 94-214, post-214)
   - Add `--e2e-test` and `--debug` flags to argparse
   - Convert LOGGING_LEVEL to CLI-overridable variable
   - Add E2E mode conditional logic (force single mode, sims=1, num_test_values=0)
   - Add debug mode behavioral changes (DEBUG logging, workers=1, reduced sims)

2. `tests/integration/test_simulation_integration.py` (new test methods)
   - Add `test_e2e_mode_completes_fast()` (validates ≤180 sec runtime)
   - Add `test_debug_mode_behavioral_changes()` (validates DEBUG logging + behavioral changes)
   - Add `test_e2e_and_debug_combined()` (validates flag compatibility)

**Data Files:** None

---

### 3. Data Structures

**New Structures:** None

**Modified Structures:**
- `argparse.Namespace` (run_win_rate_simulation.py)
  - Add field: `e2e_test` (bool, default False)
  - Add field: `debug` (bool, default False)
  - Existing fields preserved unchanged

**No Changes:**
- SimulationManager data structures unchanged
- Output format unchanged (5-file config structure in optimal_* folders)

---

### 4. API/Interface Changes

**New Methods:** None

**Modified Methods:** None

**New CLI Arguments:**
- `--e2e-test` (boolean flag): Run in E2E test mode (single run, minimal configs, ≤3 min)
- `--debug` (boolean flag): Enable debug mode (DEBUG logging + reduced iterations/datasets)

**Backward Compatibility:**
- All existing arguments preserved
- New flags are optional (default: False)
- No breaking changes

---

### 5. Testing

**New Integration Tests:** 3
- `test_e2e_mode_completes_fast()` - Validates E2E completes in ≤180 seconds, exit code 0, expected outputs
- `test_debug_mode_behavioral_changes()` - Validates DEBUG logging enabled, workers=1, sims reduced
- `test_e2e_and_debug_combined()` - Validates both flags work together

**Coverage Target:** >90% (per S5 Round 2 requirement)

**Edge Cases Covered:**
- E2E mode with conflicting user args (mode/sims override)
- Debug mode with sims already ≤5 (no reduction)
- Combined --e2e-test + --debug (precedence rules)
- E2E runtime >180 seconds (test fails, triggers optimization)

---

### 6. Dependencies

**Depends On (Internal):**
- `utils/LoggingManager.py` (setup_logger method) - EXISTS
- `simulation/win_rate/SimulationManager.py` (run_single_config_test method) - EXISTS
- Python `argparse` standard library - EXISTS

**Blocks:**
- Feature 08 (integration_test_framework) - Cannot start until Features 01-07 complete

**External Dependencies:** None

---

## Cross-Feature Alignment

**Compared To:** Features 01-04, 06-07 (all Group 1 features)

**Alignment Status:** ✅ ALIGNED - No conflicts found

**Universal Flags Consistency:**
- ✅ --debug: Consistent implementation (DEBUG logging + workers=1 + reduced sims)
- ✅ --e2e-test: Consistent implementation (single run, baseline only, ≤3 min)
- ✅ --log-level: Consistent implementation (added via R2a per Loop 1 Issue 4)

**Simulation-Specific Patterns:**
- ✅ Feature 05: E2E = single run, 0 test values (baseline only)
- ✅ Feature 06: E2E = single horizon, 0 test values (baseline only)
- ✅ Consistent approach: Simulations use "0-1 random configs" pattern

**Debug Mode Behavioral Changes:**
- ✅ Feature 05: workers=1, sims=2 (if >5), test_values=1 (if >1)
- ✅ Feature 06: test_values=1, 2 horizons instead of 4
- ✅ Pattern: Reduce iterations/datasets for faster debugging

**Variable Naming:**
- ⚠️ Issue L2-1 identified: `num_test_values` vs `args.test_values` inconsistency
- Resolution pending: Clarify relationship in spec

**No Conflicts Found:**
- No file overlap (run_win_rate_simulation.py unique to Feature 05)
- No conflicting requirements with other features
- Simulation patterns consistent with Feature 06

**Verified By:** Primary Agent (S3 Final Consistency Loop)
**Date:** 2026-01-30

---

### 7. Edge Cases & Error Handling

**Edge Cases Handled:**
1. **E2E mode with user-specified conflicting args**
   - E2E overrides mode to 'single', sims to 1, test_values to 0
   - Print warning banner showing overrides

2. **Debug mode with small sims count**
   - If sims already ≤5, don't reduce (preserve user intent)
   - Skip reduction logic when --e2e-test present (E2E takes precedence)

3. **Combined --e2e-test + --debug flags**
   - E2E processes first (sets sims=1)
   - Debug processes second (sets logging/workers, skips sims reduction)
   - Both flags apply independently

4. **E2E runtime exceeds 3 minutes**
   - Integration test assertion fails
   - Triggers optimization during S6 (reduce dataset, simplify baseline config)

**Error Conditions:**
- Baseline config not found: Existing error handling preserved
- Invalid arguments: argparse validation (no changes needed)

---

### 8. Documentation

**User-Facing Documentation:**
- `--e2e-test` help text: "Run in E2E test mode (single run, minimal configs, ≤3 min)"
- `--debug` help text: "Enable debug mode (DEBUG logging + reduced iterations/datasets)"

**Developer Documentation:**
- Inline comments explaining E2E/debug logic (implementation plan details)
- spec.md documents all requirements with traceability

**README Updates:** None (handled by Feature 09 - documentation)

---

### 9. User Approval

**Status:** [x] APPROVED

**Approval Timestamp:** 2026-01-30 16:15

**Approval Notes:**
User approved acceptance criteria on 2026-01-30 with no modifications requested. All requirements validated and ready for implementation planning (S5).

---

## Open Questions

**See checklist.md for all open questions requiring user input.**

---

## Notes

**Implementation Strategy:**
- Start with --e2e-test flag (simpler, less behavioral changes)
- Then add --debug flag (more complex, multiple behavioral changes)
- Then add integration tests (validate both flags work correctly)
- Test combined --e2e-test + --debug to ensure no conflicts

**Testing Strategy:**
- Unit tests: Verify argparse adds flags correctly
- Integration tests: Verify E2E completes in ≤3 min, debug enables DEBUG logging
- Manual testing: Run with real data to measure actual E2E runtime

**Risk:** E2E mode may exceed 3 minutes with large baseline configs or datasets
- **Mitigation:** Measure runtime early, optimize if needed (reduce dataset, simplify config)

---

**Note:** This specification created during S2.P2. Complete specification with acceptance criteria will be finalized during S2.P3 (Refinement Phase) after user answers all checklist questions.
