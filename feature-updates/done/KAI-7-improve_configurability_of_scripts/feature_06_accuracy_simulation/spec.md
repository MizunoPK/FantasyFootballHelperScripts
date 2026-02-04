# Feature 06 Specification: Accuracy Simulation Configurability

**Status:** APPROVED - S2 COMPLETE (User Approved 2026-01-30)
**Created:** 2026-01-28
**Last Updated:** 2026-01-30

---

## Discovery Context

**Discovery Document:** `../DISCOVERY.md`

### This Feature's Scope (from Discovery)

**Purpose:** Add E2E mode and debug enhancements to accuracy simulation

**Scope:**
- Enhance argparse (add --e2e-test flag)
- Add E2E test mode (single horizon, single run, 0-1 test values, ≤3 min)
- Enhance debug mode (already has --log-level arg, add behavioral changes)
- Unit tests

**Dependencies:** None (benefits from Feature 05 patterns)

**Estimated Size:** SMALL-MEDIUM

### Relevant Discovery Decisions

**Recommended Approach:** Option 2 - Comprehensive Script-Specific Argparse
- Script-specific args from constants.py/config.py files
- Universal --debug and --e2e-test flags on all runners
- Debug mode = behavioral changes + DEBUG logging
- E2E test mode with fast execution (≤3 min)

**Key Design Decisions:**
- run_accuracy_simulation.py already has extensive argparse (--baseline, --test-values, --log-level, etc.)
- E2E test mode: single horizon, single run, 0-1 test values (per User Answer Q3)
- Debug mode: behavioral changes (fewer iterations) + DEBUG logging (per User Answer Q4)

### Relevant User Answers (from Discovery)

**User Answer Q3:** "Simulations: single run with 0-1 random configs. Fetchers: real APIs with data limiting args"
- Impact on Feature 06: E2E mode runs single horizon, single run, 0-1 test values

**User Answer Q4:** "Option C: Both logging AND behavioral changes"
- Impact on Feature 06: Debug mode enables DEBUG logs AND reduces iterations/datasets

**User Answer Q5:** "Check exit code AND verify expected outcomes (specific logs, result counts)"
- Impact on Feature 06: Integration tests will validate exit code + specific accuracy simulation outputs

### Discovery Research Findings

**From DISCOVERY.md Iteration 1:**
- run_accuracy_simulation.py already HAS argparse (lines 1-80) with --baseline, --test-values, --log-level, etc.
- Logging infrastructure EXISTS (LoggingManager supports all levels including DEBUG)
- No E2E test mode exists (need to design)

**From DISCOVERY.md Iteration 2:**
- DEFAULT_LOG_LEVEL, DEFAULT_TEST_VALUES, DEFAULT_MAX_WORKERS already in script
- Already has extensive argparse configuration

---

## Initial Purpose (from S1 Breakdown)

Add E2E mode and debug enhancements to accuracy simulation.

---

## Initial Scope (from S1 Breakdown)

- Enhance argparse in `run_accuracy_simulation.py` (add --e2e-test, --debug flags)
- Add E2E test mode (single horizon, single run, 0-1 test values, ≤3 min)
- Enhance debug mode with behavioral changes (already has --log-level)
- Unit tests for E2E mode and debug behavioral changes

---

## Dependencies

- **Depends on:** None (benefits from Feature 05 win_rate_simulation patterns)
- **Blocks:** Feature 08 (integration_test_framework)

---

---

## Components Affected

### File 1: run_accuracy_simulation.py (Enhance Argparse + E2E/Debug Logic)

**Location:** `run_accuracy_simulation.py` (lines 1-319)
**Purpose:** Main runner script - add --e2e-test and --debug flags, implement E2E/debug behavioral changes
**Source:** Epic Request (DISCOVERY.md lines 349-354), User Answer Q3, User Answer Q4

**Modifications Required:**
1. **Argparse Enhancement** (lines 154-225):
   - Add `--e2e-test` flag (boolean, default: False)
   - Add `--debug` flag (boolean, default: False)
   - Source: Epic Request + User Answer Q3/Q4

2. **E2E Mode Logic** (after line 226):
   - If --e2e-test flag set:
     - Override test_values to 0 (baseline only, no parameter variations)
     - Pass single horizon ['week_1_5'] to AccuracySimulationManager
     - Break infinite while loop (lines 317-319) - run once
   - Source: User Answer Q3 ("single run with 0-1 random configs")

3. **Debug Mode Logic** (after line 226):
   - If --debug flag set:
     - Override log_level to 'debug'
     - Reduce test_values to 1 (for behavioral change)
     - Pass limited horizons ['week_1_5', 'week_6_9'] to AccuracySimulationManager
   - Source: User Answer Q4 ("both logging AND behavioral changes")

4. **While Loop Modification** (lines 317-319):
   - Check for --e2e-test flag BEFORE while True loop
   - If E2E mode: call main() once and exit
   - If normal mode: keep infinite while loop
   - Source: Derived (necessary for E2E ≤3 min constraint)

**Evidence:**
- Current argparse: lines 154-225 (8 existing arguments)
- Infinite loop: lines 317-319 (`while True: main()`)
- Research document: `research/accuracy_simulation_RESEARCH.md` Component 1

---

### File 2: simulation/accuracy/AccuracySimulationManager.py (Add Horizons Parameter)

**Location:** `simulation/accuracy/AccuracySimulationManager.py`
**Purpose:** Simulation manager - add optional horizons_to_run parameter to filter WEEK_RANGES
**Source:** Derived (necessary to support E2E/debug horizon limiting)

**Modifications Required:**
1. **__init__() Signature** (lines 74-97):
   - Add parameter: `horizons_to_run: Optional[List[str]] = None`
   - Store as instance variable: `self.horizons_to_run = horizons_to_run`
   - Source: Derived (required for E2E single horizon and debug limited horizons)

2. **run_both() Method** (line 709+):
   - Filter WEEK_RANGES based on horizons_to_run
   - If horizons_to_run is None: use all 4 horizons (backward compatible)
   - If horizons_to_run is list: filter WEEK_RANGES to only specified keys
   - Example: horizons_to_run=['week_1_5'] → only iterate week_1_5
   - Source: Derived (required to support E2E/debug modes)

3. **run_weekly_optimization() Method** (line 573+):
   - Apply same filtering logic as run_both()
   - Source: Derived (consistency across both methods)

**Evidence:**
- Current __init__: lines 74-97 (9 parameters)
- WEEK_RANGES usage: line 568 (`for week_key, week_range in WEEK_RANGES.items()`)
- Research document: `research/accuracy_simulation_RESEARCH.md` Component 2

---

### File 3: tests/accuracy_simulation/test_run_accuracy_simulation.py (New Unit Tests)

**Location:** `tests/accuracy_simulation/test_run_accuracy_simulation.py` (NEW FILE)
**Purpose:** Unit tests for argparse handling and E2E/debug mode logic
**Source:** Epic Request (DISCOVERY.md line 354 "Unit tests")

**Tests Required:**
1. **Test --e2e-test flag parsing**
   - Verify flag sets E2E mode
   - Verify test_values overridden to 0
   - Verify horizons limited to single horizon
   - Source: Epic + User Answer Q3

2. **Test --debug flag parsing**
   - Verify flag sets debug mode
   - Verify log_level set to 'debug'
   - Verify test_values reduced to 1
   - Verify horizons limited to 2
   - Source: Epic + User Answer Q4

3. **Test while loop breaking (E2E mode)**
   - Mock main() function
   - Verify main() called once in E2E mode
   - Verify main() called in loop for normal mode
   - Source: Derived (E2E mode requirement)

4. **Test AccuracySimulationManager initialization**
   - Mock AccuracySimulationManager
   - Verify horizons_to_run parameter passed correctly
   - Source: Derived (integration verification)

**Evidence:**
- No existing unit tests for run_accuracy_simulation.py (research found none)
- Integration tests exist but not unit tests
- Research document: `research/accuracy_simulation_RESEARCH.md` "Existing Test Patterns"

---

## Requirements (WITH SOURCES)

### R1: Add --e2e-test Flag

**Description:** Add --e2e-test boolean flag to run_accuracy_simulation.py argparse

**Source:** Epic Request (DISCOVERY.md line 350 "Enhance argparse (add --e2e-test flag)")

**Implementation:**
- Add argparse argument: `--e2e-test` (action='store_true', default=False)
- Help text: "Run in E2E test mode (fast, single horizon, ≤3 min)"
- Location: After existing --log-level argument (line 224)

**Traceability:** User explicitly requested E2E mode flag in Discovery

---

### R2: E2E Mode Runs Single Horizon

**Description:** When --e2e-test flag is set, limit simulation to single horizon (week_1_5 only)

**Source:** User Answer Q3 (DISCOVERY.md line 26: "Simulations: single run with 0-1 random configs")

**Implementation:**
- Pass `horizons_to_run=['week_1_5']` to AccuracySimulationManager when --e2e-test is True
- AccuracySimulationManager filters WEEK_RANGES to only week_1_5
- Reduces execution from 4 horizons to 1 horizon

**Traceability:** User specified "single run" for simulations in E2E mode

---

### R3: E2E Mode Uses 0 Test Values (Baseline Only)

**Description:** When --e2e-test flag is set, override test_values to 0 (test baseline config only, no variations)

**Source:** User Answer Q3 (DISCOVERY.md line 26: "0-1 random configs")

**Implementation:**
- If --e2e-test is True: set args.test_values = 0
- Total configs tested: (0+1)**6 = 1 config (baseline only)
- Minimizes execution time to meet ≤3 min constraint

**Traceability:** User specified "0-1 test values" for E2E mode

---

### R4: E2E Mode Runs Once (Breaks While Loop)

**Description:** When --e2e-test flag is set, run main() once and exit (do not loop infinitely)

**Source:** Derived from User Answer Q3 (≤3 min constraint requires single execution)

**Derivation:** Current code has `while True: main()` which runs forever. E2E mode must complete in ≤3 minutes, requiring single execution.

**Implementation:**
- Check --e2e-test flag before while loop
- If True: call main() once, then sys.exit(0)
- If False: execute `while True: main()` as before

**Traceability:** Logically required to meet E2E time constraint

---

### R5: Add --debug Flag

**Description:** Add --debug boolean flag to run_accuracy_simulation.py argparse

**Source:** Epic Request (DISCOVERY.md line 352 "Enhance debug mode")

**Implementation:**
- Add argparse argument: `--debug` (action='store_true', default=False)
- Help text: "Run in debug mode (DEBUG logging + behavioral changes)"
- Location: After --e2e-test argument

**Traceability:** User explicitly requested debug mode enhancements in Discovery

---

### R6: Debug Mode Enables DEBUG Logging

**Description:** When --debug flag is set, override log_level to 'debug'

**Source:** User Answer Q4 (DISCOVERY.md line 27: "Option C: Both logging AND behavioral changes")

**Implementation:**
- If --debug is True: set args.log_level = 'debug'
- Passed to setup_logger() which enables DEBUG level logging
- Shows all evaluations, parameter updates, worker activity

**Traceability:** User explicitly chose "both logging AND behavioral changes"

---

### R7: Debug Mode Reduces Iterations (Behavioral Change)

**Description:** When --debug flag is set, reduce test_values to 1 (fewer iterations for faster debugging)

**Source:** User Answer Q4 ("behavioral changes")

**Implementation:**
- If --debug is True: set args.test_values = 1
- Total configs: (1+1)**6 = 64 configs (vs default 729 configs)
- Faster execution for debugging purposes

**Traceability:** User specified debug mode should have "behavioral changes" not just logging

---

### R8: Debug Mode Limits Horizons (Behavioral Change)

**Description:** When --debug flag is set, limit simulation to 2 horizons (week_1_5, week_6_9)

**Source:** User Answer Q4 ("behavioral changes")

**Implementation:**
- If --debug is True: pass `horizons_to_run=['week_1_5', 'week_6_9']` to AccuracySimulationManager
- Reduces from 4 horizons to 2 horizons
- Faster execution while still testing multiple horizons

**Traceability:** User specified debug mode should reduce iterations/datasets

---

### R9: Add horizons_to_run Parameter to AccuracySimulationManager

**Description:** Add optional horizons_to_run parameter to AccuracySimulationManager.__init__() to support horizon filtering

**Source:** Derived (required to implement R2, R4, R8)

**Derivation:** E2E and debug modes require limiting horizons. AccuracySimulationManager currently processes all 4 horizons. Need parameter to filter horizons.

**Implementation:**
- Add parameter: `horizons_to_run: Optional[List[str]] = None`
- Default None = all 4 horizons (backward compatible)
- If list provided: filter WEEK_RANGES iteration to only specified keys
- Apply in run_both() and run_weekly_optimization() methods

**Traceability:** Logically necessary to support horizon limiting requirements

---

### R10: Create Unit Tests for Argparse Flags

**Description:** Create unit tests verifying --e2e-test and --debug flags work correctly

**Source:** Epic Request (DISCOVERY.md line 354 "Unit tests")

**Implementation:**
- Test file: `tests/accuracy_simulation/test_run_accuracy_simulation.py`
- Test flag parsing, parameter overrides, AccuracySimulationManager initialization
- Mock main() to test while loop breaking

**Traceability:** User explicitly requested unit tests in Discovery

---

### R11: Integration Tests Validate Exit Code and Outcomes

**Description:** Integration tests must check exit code AND verify specific accuracy simulation outputs

**Source:** User Answer Q5 (DISCOVERY.md line 28: "Check exit code AND verify expected outcomes")

**Implementation:**
- Check exit code (0 = success, 1 = failure)
- Verify expected outputs:
  - MAE values calculated
  - Optimal config files created
  - Results summary generated
  - Log file contains expected entries
- Source: User specified tests must validate specific outcomes, not just exit codes

**Traceability:** User explicitly specified integration test validation requirements

---

### R12: Combine E2E and Debug Modes When Both Flags Set

**Description:** When both --e2e-test and --debug flags are provided, combine E2E settings with DEBUG logging

**Source:** User Answer to Checklist Q1 (2026-01-30: "approve recommendation" for Option D - Combine Both Modes)

**Implementation:**
- If only --e2e-test: Use E2E settings (test_values=0, single horizon, run once)
- If only --debug: Use debug settings (log_level='debug', test_values=1, 2 horizons)
- **If both --e2e-test AND --debug:**
  - Use E2E settings (test_values=0, horizons=['week_1_5'], run once)
  - PLUS set log_level='debug' (DEBUG logging enabled)
  - Result: Fast E2E test with verbose DEBUG logging
- No mutual exclusion error
- No precedence warnings

**Rationale:** Maximizes user flexibility - allows combining fast testing with verbose logging for debugging E2E mode issues

**Traceability:** User explicitly approved Option D (Combine Both Modes) in checklist approval

---

## Data Structures

### Argument Flags

**--e2e-test Flag:**
- Type: Boolean (action='store_true')
- Default: False
- Impact: Triggers E2E mode (single horizon, test_values=0, run once)
- Source: Epic Request

**--debug Flag:**
- Type: Boolean (action='store_true')
- Default: False
- Impact: Triggers debug mode (log_level='debug', test_values=1, horizons=2)
- Source: Epic Request

### horizons_to_run Parameter

**Type:** `Optional[List[str]]`
**Values:** None OR list of horizon keys from WEEK_RANGES
**Valid horizon keys:** 'week_1_5', 'week_6_9', 'week_10_13', 'week_14_17'

**Examples:**
- None → all 4 horizons (default behavior)
- ['week_1_5'] → single horizon (E2E mode)
- ['week_1_5', 'week_6_9'] → 2 horizons (debug mode)

**Source:** Derived (required for horizon filtering)

---

## Algorithms

### E2E Mode Logic

**Pseudocode:**
```python
if args.e2e_test:
    # Override parameters for E2E
    args.test_values = 0  # Baseline only
    horizons_to_run = ['week_1_5']  # Single horizon

    # E2E logging level (unless overridden by --debug or --log-level)
    # Default: INFO level for clean E2E output
    # Consistency: Pattern from Features 01-05
    if not args.debug:
        log_level = args.log_level if hasattr(args, 'log_level') else 'INFO'
    else:
        log_level = 'DEBUG'  # Debug takes precedence

    # Run simulation once
    manager = AccuracySimulationManager(..., horizons_to_run=horizons_to_run)
    manager.run_both()
    sys.exit(0)  # Exit after single run (R4 - runs once and exits, not continuous loop)
else:
    # Normal mode: infinite loop
    while True:
        main()
```

**Source:** User Answer Q3 + Derived

---

### Debug Mode Logic

**Pseudocode:**
```python
if args.debug:
    # Override parameters for debug
    args.log_level = 'debug'  # Enable DEBUG logging
    args.test_values = 1  # Reduce iterations
    horizons_to_run = ['week_1_5', 'week_6_9']  # Limit to 2 horizons
else:
    horizons_to_run = None  # All 4 horizons
```

**Source:** User Answer Q4

---

### Horizon Filtering in AccuracySimulationManager

**Pseudocode:**
```python
def run_both(self):
    # Determine which horizons to process
    if self.horizons_to_run is None:
        horizons_to_process = WEEK_RANGES.items()  # All 4
    else:
        horizons_to_process = {k: v for k, v in WEEK_RANGES.items()
                               if k in self.horizons_to_run}.items()

    # Iterate only selected horizons
    for week_key, week_range in horizons_to_process:
        # Evaluate this horizon
        ...
```

**Source:** Derived

---

## Testing Requirements

### Unit Tests (New File)

**File:** `tests/accuracy_simulation/test_run_accuracy_simulation.py`

**Test Cases:**
1. test_e2e_flag_sets_parameters()
2. test_debug_flag_sets_parameters()
3. test_e2e_mode_breaks_while_loop()
4. test_horizons_parameter_passed_correctly()
5. test_normal_mode_preserves_defaults()

**Source:** Epic Request (unit tests required)

---

### Integration Tests (Enhance Existing)

**File:** `tests/integration/test_accuracy_simulation_integration.py` (likely exists)

**Enhancements:**
1. Test --e2e-test flag (verify ≤3 min execution)
2. Test --debug flag (verify DEBUG logs generated)
3. Validate exit codes (0 for success)
4. Validate outputs (MAE, optimal configs, results summary)

**Source:** User Answer Q5

---

## Edge Cases

### Edge Case 1: Both --e2e-test and --debug Flags Set

**Scenario:** User provides both `--e2e-test` and `--debug` flags

**Resolution:** ✅ RESOLVED (User Answer to Checklist Q1 - 2026-01-30)

**Behavior:** Combine both modes (Requirement R12)
- Use E2E settings (test_values=0, single horizon, run once)
- PLUS enable DEBUG logging (log_level='debug')
- Result: Fast E2E test with verbose DEBUG output

**Rationale:** User approved Option D (Combine Both Modes) - maximizes flexibility without mutual exclusion

---

### Edge Case 2: Invalid Horizon Key in horizons_to_run

**Scenario:** Code passes invalid horizon key (e.g., ['week_99_100'])

**Current Behavior:** Undefined (not specified)

**Handling:** Derived requirement - validate horizons_to_run
- Check all keys exist in WEEK_RANGES
- Raise ValueError if invalid key found
- Prevents silent failures

**Source:** Derived (robustness requirement)

---

## Acceptance Criteria

**Feature Summary:** Add E2E test mode and debug enhancements to accuracy simulation, enabling fast integration testing (≤3 min) and verbose debugging with behavioral changes.

---

### 1. Behavior Changes

**New Functionality:**
- **E2E Test Mode:** `--e2e-test` flag runs single horizon, baseline config only, exits after one run (≤3 min execution)
- **Debug Mode:** `--debug` flag enables DEBUG logging + reduces iterations/horizons for faster debugging
- **Combined Modes:** Both flags together = E2E speed with DEBUG verbosity

**Modified Functionality:**
- run_accuracy_simulation.py accepts new command-line flags
- AccuracySimulationManager supports horizon filtering via optional parameter

**No Changes To:**
- Existing simulation algorithms or scoring logic
- Default behavior (no flags = normal operation with infinite loop)
- Existing argparse flags (--baseline, --test-values, --log-level remain unchanged)

---

### 2. Files Modified

**New Files:**
- `tests/accuracy_simulation/test_run_accuracy_simulation.py` - Unit tests for argparse and mode logic (5 test cases)

**Existing Files Modified:**
- `run_accuracy_simulation.py` (lines 154-319 affected)
  - Argparse: Add --e2e-test and --debug flags
  - Mode logic: Override parameters based on flags
  - While loop: Break for E2E mode, maintain infinite loop for normal
- `simulation/accuracy/AccuracySimulationManager.py` (lines 74-97, 573+, 709+)
  - __init__: Add horizons_to_run parameter
  - run_both() and run_weekly_optimization(): Filter WEEK_RANGES based on parameter

**Data Files:**
- None (no config or data file changes)

---

### 3. Data Structures

**New Parameters:**
- `horizons_to_run: Optional[List[str]]` in AccuracySimulationManager.__init__()
  - Type: Optional[List[str]]
  - Values: None (all 4 horizons), OR list of keys from WEEK_RANGES
  - Valid keys: 'week_1_5', 'week_6_9', 'week_10_13', 'week_14_17'

**New Argument Flags:**
- `--e2e-test`: Boolean flag (action='store_true', default=False)
- `--debug`: Boolean flag (action='store_true', default=False)

**Modified Structures:**
- None (existing data structures unchanged)

---

### 4. API/Interface Changes

**New Methods:**
- None

**Modified Methods:**
- `AccuracySimulationManager.__init__()`:
  - **Before:** 9 parameters
  - **After:** 10 parameters (added horizons_to_run)
  - **Backward Compatible:** Yes (new parameter is optional with default None)
  - **Callers Affected:** run_accuracy_simulation.py (updated to pass parameter)

**Removed Methods:**
- None

---

### 5. Testing

**Unit Tests (New):**
- File: `tests/accuracy_simulation/test_run_accuracy_simulation.py`
- Test count: 5 tests
  1. test_e2e_flag_sets_parameters()
  2. test_debug_flag_sets_parameters()
  3. test_e2e_mode_breaks_while_loop()
  4. test_horizons_parameter_passed_correctly()
  5. test_normal_mode_preserves_defaults()
- Coverage target: 100% of new argparse logic and mode logic

**Integration Tests (Enhanced):**
- File: `tests/integration/test_accuracy_simulation_integration.py` (Feature 08 responsibility)
- Requirements from R11:
  - Test --e2e-test flag (verify ≤3 min execution time)
  - Test --debug flag (verify DEBUG logs generated)
  - Validate exit code (0 = success)
  - Validate outputs (MAE values, optimal configs, results summary, log entries)

**Edge Cases Tested:**
- Both flags set simultaneously (E2E + DEBUG logging)
- Invalid horizon keys (validation error)
- Normal mode still works (backward compatibility)

---

### 6. Dependencies

**Depends On:**
- None (Feature 06 is independent)
- Benefits from: Feature 05 (win_rate_simulation) patterns for similar implementation approach

**Blocks:**
- Feature 08 (integration_test_framework) - needs E2E mode working before creating integration test runners

**External Dependencies:**
- None (uses existing argparse, logging infrastructure)

---

### 7. Edge Cases & Error Handling

**Argument Validation Approach (Issue 7 Resolution):**
- **Test Values:** No validation (user-specified, no constraints)
- **Baseline Path:** File existence checked at runtime (not in argparse)
- **Log Level:** Validated by argparse choices (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- **Horizons (Internal):** Validated in AccuracySimulationManager (ValueError if invalid key)
- **Philosophy:** Minimal argparse validation, runtime checks for file operations
- **Rationale:** Trust user input, provide clear errors at usage time

**Edge Case 1: Both --e2e-test and --debug Flags (RESOLVED)**
- Behavior: Combine modes (E2E settings + DEBUG logging)
- Implementation: No mutual exclusion, no precedence warnings
- Source: R12, User Answer to Checklist Q1

**Edge Case 2: Invalid Horizon Key**
- Behavior: Validate horizons_to_run parameter
- Error Handling: Raise ValueError if invalid key provided
- Prevention: Only internal code uses this parameter (not user-facing)

**Edge Case 3: Backward Compatibility**
- Scenario: Existing code calling AccuracySimulationManager without horizons_to_run
- Behavior: Default None value = all 4 horizons (unchanged behavior)
- Verified By: Unit test test_normal_mode_preserves_defaults()

---

### 8. Documentation

**User-Facing Documentation:**
- None required (Feature 09 will document all arg flags across all scripts)

**Developer Documentation:**
- Docstrings for new parameter in AccuracySimulationManager.__init__()
- Comments explaining E2E/debug mode logic in run_accuracy_simulation.py
- Unit test docstrings explaining what each test validates

---

### 9. User Approval

**Status:** [x] APPROVED

**Approval Checklist:**
- [x] I understand the E2E mode behavior (single horizon, baseline only, ≤3 min, runs once)
- [x] I understand the debug mode behavior (DEBUG logs + reduced iterations/horizons)
- [x] I approve combining both modes when both flags provided (R12)
- [x] I approve the file modifications (2 files modified, 1 new test file)
- [x] I approve the backward-compatible API change (optional horizons_to_run parameter)
- [x] I approve proceeding to implementation planning (S5)

**Approval Timestamp:** 2026-01-30 22:29 UTC

**Approval Notes:** User approved acceptance criteria on 2026-01-30 with no modifications requested. All 12 requirements approved for implementation.

---

## Cross-Feature Alignment

**Compared To:** Features 01-05, 07 (all Group 1 features)

**Alignment Status:** ✅ ALIGNED - No conflicts found

**Universal Flags Consistency:**
- ✅ --debug: Consistent implementation (DEBUG logging + test_values=1 + 2 horizons)
- ✅ --e2e-test: Consistent implementation (single horizon, baseline only, runs once, ≤3 min)
- ✅ --log-level: Consistent implementation (DEBUG/INFO/WARNING/ERROR/CRITICAL choices)

**Simulation-Specific Patterns:**
- ✅ Feature 06: E2E = single horizon, 0 test values (baseline only)
- ✅ Feature 05: E2E = single run, 0 test values (baseline only)
- ✅ Consistent approach: Both simulations use "0-1 random configs" pattern per User Answer Q3

**Debug + E2E Combination:**
- ✅ Feature 06: Combines both modes (E2E settings + DEBUG logging) per R12
- ✅ Consistent with Features 01-05, 07 combination behaviors
- ✅ User approved Option D: Combine Both Modes (Checklist Q1)

**Backward Compatibility:**
- ✅ horizons_to_run parameter optional (default None = all 4 horizons)
- ✅ Existing code continues to work unchanged
- ✅ Pattern: All API changes backward compatible across Group 1

**No Conflicts Found:**
- No file overlap (run_accuracy_simulation.py and AccuracySimulationManager.py unique to Feature 06)
- No conflicting requirements with other features
- Simulation patterns consistent with Feature 05

**Verified By:** Primary Agent (S3 Final Consistency Loop)
**Date:** 2026-01-30

---

**Note:** Complete specification with 12 requirements. All requirements have full traceability to epic/user decisions. Checklist approved by user (Gate 2 PASSED - 2026-01-30). Ready for S2.P3 Refinement Phase.
