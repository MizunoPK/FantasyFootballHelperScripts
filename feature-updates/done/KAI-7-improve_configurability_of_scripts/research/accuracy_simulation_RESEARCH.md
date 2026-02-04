# Feature 06: Accuracy Simulation Configurability - Research Findings

**Feature:** feature_06_accuracy_simulation
**Created:** 2026-01-29
**Last Updated:** 2026-01-29
**Status:** S2.P1 Phase 1 Complete

---

## Discovery Context Summary

**From DISCOVERY.md:**
- Purpose: Add E2E mode and debug enhancements to accuracy simulation
- Scope: Enhance argparse (add --e2e-test flag), add E2E test mode (single horizon, single run, 0-1 test values, ≤3 min), enhance debug mode (add behavioral changes)
- Dependencies: None (benefits from Feature 05 win_rate_simulation patterns)
- Estimated Size: SMALL-MEDIUM

**Relevant User Answers:**
- Q3: "Simulations: single run with 0-1 random configs" → E2E mode: single horizon, single run, 0-1 test values
- Q4: "Option C: Both logging AND behavioral changes" → Debug mode: DEBUG logs + behavioral changes (fewer iterations)
- Q5: "Check exit code AND verify expected outcomes" → Integration tests validate exit code + specific outputs

---

## Components Researched

### Component 1: run_accuracy_simulation.py (Main Runner Script)

**Discovery Scope Reference:** Main script to enhance

**Found in Codebase:**
- File: `run_accuracy_simulation.py` (lines 1-319)
- Current state: HAS extensive argparse already
- Line 27: imports argparse
- Lines 154-225: Argument parser setup with 8 existing arguments

**Actual Code Signatures:**
```python
# Line 154
parser = argparse.ArgumentParser(
    description="Run accuracy simulation to find optimal scoring parameters using tournament optimization"
)

# Lines 158-224 - Existing arguments:
--baseline (str, default: auto-detect most recent optimal config)
--output (str, default: simulation/simulation_configs)
--data (str, default: simulation/sim_data)
--test-values (int, default: 3)
--num-params (int, default: 1)
--max-workers (int, default: 8)
--use-processes / --no-use-processes (bool, default: True)
--log-level (choices: debug/info/warning/error, default: info)
```

**How It Works Today:**
- Lines 52-68: DEFAULT constants for logging and simulation configuration
- DEFAULT_LOG_LEVEL = 'info' (line 53)
- DEFAULT_TEST_VALUES = 3 (line 63)
- Line 229: setup_logger() called with args.log_level.upper()
- Line 268: Calculates total_configs = (args.test_values + 1) ** 6
- Lines 282-291: Initializes AccuracySimulationManager with args
- Line 298: Calls manager.run_both() - runs ALL 4 horizons
- Lines 317-319: Infinite while loop `while True: main()` - CRITICAL FOR E2E

**Implementation Approach for This Feature:**
- **E2E Flag:** Add --e2e-test flag (boolean)
- **Debug Flag:** Add --debug flag (boolean, sets log_level='debug' + behavioral changes)
- **E2E Behavior:**
  - Set test_values to 0 or 1
  - Limit horizons to 1 (need to modify AccuracySimulationManager or pass horizon list)
  - Set num_params to 1
  - BREAK infinite while loop (run main() once)
- **Debug Behavior:**
  - Set log_level to 'debug'
  - Reduce test_values (e.g., 1-2)
  - Set num_params to 1
  - Possibly limit horizons to 1-2

**Evidence:**
- File path: `run_accuracy_simulation.py:154-225` (argparse setup)
- Line numbers: 27 (argparse import), 229 (setup_logger), 298 (run_both), 317-319 (while loop)
- Code snippet: Infinite while loop (lines 317-319)

---

### Component 2: AccuracySimulationManager (Core Simulation Manager)

**Discovery Scope Reference:** Manager class that runs tournament optimization

**Found in Codebase:**
- File: `simulation/accuracy/AccuracySimulationManager.py`
- Class: AccuracySimulationManager (line 57)
- Method: run_both() (line 709) - runs tournament optimization across ALL 4 horizons

**Actual Code Signatures:**
```python
# Lines 74-97
def __init__(
    self,
    baseline_config_path: Path,
    output_dir: Path,
    data_folder: Path,
    parameter_order: List[str],
    num_test_values: int = 5,
    num_parameters_to_test: int = 1,
    max_workers: int = 8,
    use_processes: bool = True
) -> None:

# Line 709
def run_both(self) -> Path:
    """
    Run tournament optimization: each parameter optimizes across ALL 4 weekly horizons.
    """
```

**How It Works Today:**
- Line 568: `for week_key, week_range in WEEK_RANGES.items():`
- Line 619: Same loop pattern for run_weekly_optimization()
- Iterates through ALL 4 horizons (week_1_5, week_6_9, week_10_13, week_14_17)
- No current mechanism to limit horizons

**Implementation Approach for This Feature:**
- **Option A:** Add `horizons_to_run` parameter to __init__() (list of horizon keys)
  - Default: all 4 horizons
  - E2E: single horizon (e.g., ['week_1_5'])
  - Modify line 568 loop to filter WEEK_RANGES
- **Option B:** Add run_single_horizon() method (separate from run_both)
  - E2E calls run_single_horizon(horizon='week_1_5')
  - Cleaner separation, no conditional logic in existing methods
- **Recommendation:** Option A (cleaner, no new method needed)

**Evidence:**
- File path: `simulation/accuracy/AccuracySimulationManager.py:568, 619, 709`
- Code snippet: WEEK_RANGES iteration pattern

---

### Component 3: WEEK_RANGES (Horizon Configuration)

**Discovery Scope Reference:** 4 horizons (week1-5, week6-9, week10-13, week14-17)

**Found in Codebase:**
- File: `simulation/accuracy/AccuracyResultsManager.py` (lines 57-62)
- Exported from AccuracyResultsManager and used throughout

**Actual Code:**
```python
# Lines 57-62
WEEK_RANGES = {
    'week_1_5': (1, 5),
    'week_6_9': (6, 9),
    'week_10_13': (10, 13),
    'week_14_17': (14, 17),
}
```

**How It Works Today:**
- Global constant shared across AccuracySimulationManager, ParallelAccuracyRunner
- All code iterates through all 4 items
- Format: {week_key: (start_week, end_week)}

**Implementation Approach for This Feature:**
- No modification needed to WEEK_RANGES itself
- Filter at usage site (AccuracySimulationManager loops)
- E2E: Only use first horizon ('week_1_5')

**Evidence:**
- File path: `simulation/accuracy/AccuracyResultsManager.py:57-62`
- Usage: AccuracySimulationManager.py:568, 619; ParallelAccuracyRunner.py:71

---

## Existing Test Patterns

### Unit Tests for run_accuracy_simulation.py

**Search results:** No dedicated unit tests found for run_accuracy_simulation.py

**Expected location:** `tests/accuracy_simulation/` (does not exist)

**Integration tests:**
- File: `tests/integration/test_accuracy_simulation_integration.py` (likely exists based on Discovery findings)
- Need to verify existence and review patterns

**Test Structure to Follow:**
- Create: `tests/accuracy_simulation/test_run_accuracy_simulation.py`
- Test argparse argument handling
- Test E2E mode flag behavior
- Test debug mode flag behavior
- Mock AccuracySimulationManager to verify correct parameters passed

---

## Interface Dependencies

### LoggingManager (Logging Setup)

**Found in:**
- File: `utils/LoggingManager.py`
- Functions: setup_logger(), get_logger()

**Actual Signatures:**
```python
# Expected signature (from usage):
setup_logger(
    log_name: str,
    log_level: str,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    logging_to_file: bool,
    logging_file: str,
    logging_format: str
) -> None
```

**Usage in run_accuracy_simulation.py:**
- Line 229: `setup_logger(LOG_NAME, args.log_level.upper(), LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)`
- Converts log_level to uppercase before passing

**Implementation Approach:**
- Debug flag sets log_level='debug' → passed as 'DEBUG' to setup_logger
- No changes needed to LoggingManager interface

**Evidence:**
- File path: `run_accuracy_simulation.py:229`
- Interface: Already uses dynamic log_level from args

---

### AccuracySimulationManager.__init__() (Simulation Initialization)

**Found in:**
- File: `simulation/accuracy/AccuracySimulationManager.py:74-97`

**Actual Signature:**
```python
def __init__(
    self,
    baseline_config_path: Path,
    output_dir: Path,
    data_folder: Path,
    parameter_order: List[str],
    num_test_values: int = 5,
    num_parameters_to_test: int = 1,
    max_workers: int = 8,
    use_processes: bool = True
) -> None:
```

**Usage in run_accuracy_simulation.py:**
- Lines 282-291: Instantiates with args-based parameters

**Implementation Approach for E2E/Debug:**
- Need to add `horizons_to_run: Optional[List[str]] = None` parameter
- If None, use all 4 horizons (backward compatible)
- If list provided (e.g., ['week_1_5']), filter WEEK_RANGES
- Pass from run_accuracy_simulation.py based on --e2e-test or --debug flags

**Evidence:**
- File path: `simulation/accuracy/AccuracySimulationManager.py:74-97`
- Current usage: `run_accuracy_simulation.py:282-291`

---

## Edge Cases Identified

### Edge Case 1: Infinite While Loop (lines 317-319)

**Issue:** `while True: main()` runs forever

**Impact on E2E Mode:**
- E2E should run ONCE and exit
- Need to break loop when --e2e-test flag is set
- Solution: Check flag before while loop, run main() directly if E2E

**Code:**
```python
# Current (lines 317-319):
if __name__ == "__main__":
    while True:
        main()

# E2E fix:
if __name__ == "__main__":
    if args_have_e2e_test_flag:  # Check flag
        main()  # Run once
    else:
        while True:
            main()  # Infinite loop for normal mode
```

**Resolution:** Parse args before if __name__ block OR add flag check inside

---

### Edge Case 2: Test Values = 0 vs 1

**Issue:** Discovery says "0-1 test values" for E2E

**Interpretation:**
- 0 test values = only test baseline (no parameter variations)
- 1 test value = test baseline + 1 variation per parameter

**Impact on total configs:**
- Line 268: `total_configs = (args.test_values + 1) ** 6`
- test_values=0: (0+1)**6 = 1 config
- test_values=1: (1+1)**6 = 64 configs

**Recommendation:** Use test_values=0 for E2E (single config, fastest)

---

### Edge Case 3: Horizons Parameter Backward Compatibility

**Issue:** Adding horizons_to_run parameter to AccuracySimulationManager.__init__()

**Backward compatibility:**
- Default to None → use all 4 horizons (existing behavior)
- Existing callers (if any) won't break
- Only run_accuracy_simulation.py passes explicit horizons for E2E/debug

**Resolution:** Use Optional[List[str]] = None with default behavior

---

## Research Completeness

### Category 1: Component Knowledge
✅ Can list EXACT files to modify:
- run_accuracy_simulation.py (add --e2e-test, --debug flags, break while loop)
- simulation/accuracy/AccuracySimulationManager.py (add horizons_to_run parameter, filter WEEK_RANGES)

✅ Have READ source code for each component:
- run_accuracy_simulation.py (full file, 319 lines)
- AccuracySimulationManager.py (init and run_both methods)
- AccuracyResultsManager.py (WEEK_RANGES constant)

✅ Can cite actual method signatures:
- argparse.ArgumentParser() setup (lines 154-225)
- AccuracySimulationManager.__init__() (lines 74-97)
- manager.run_both() (line 298, 709)

---

### Category 2: Pattern Knowledge

✅ Searched for similar existing features:
- run_win_rate_simulation.py "single" mode (lines 8, 74, 133-137, 334-356)
- Single mode exists for debugging but NOT E2E mode
- Single mode pattern: mode subparser, run_single_config_test() method

✅ READ implementation of similar feature:
- run_win_rate_simulation.py single mode uses argparse subparsers
- Calls manager.run_single_config_test(season='2025')
- Accuracy simulation uses different pattern (no subparsers)

✅ Can describe existing pattern in detail:
- run_accuracy_simulation uses flat argument structure (no subparsers)
- All args are optional flags/values
- Manager instantiated once with all args
- manager.run_both() is main entry point

**Pattern to follow for Feature 06:**
- Add --e2e-test and --debug as boolean flags (not subparsers)
- Modify behavior based on flags (set test_values, horizons, etc.)
- No separate run_e2e() method - use run_both() with limited horizons

---

### Category 3: Data Structure Knowledge

✅ READ actual data files:
- WEEK_RANGES dictionary (AccuracyResultsManager.py:57-62)
- 4 horizon keys: week_1_5, week_6_9, week_10_13, week_14_17

✅ Can describe current format:
- Dictionary of {week_key: (start_week, end_week)}
- Tuple format: (int, int) for week ranges
- week_1_5 = weeks 1-5, week_6_9 = weeks 6-9, etc.

✅ Verified field names from source code:
- week_key: String with underscores (e.g., 'week_1_5')
- week_range: Tuple[int, int] (e.g., (1, 5))

---

### Category 4: Discovery Context Knowledge

✅ Reviewed DISCOVERY.md for this feature:
- Feature 06 scope: E2E mode + debug enhancements
- User Answer Q3: Single horizon, single run, 0-1 test values
- User Answer Q4: Debug = behavioral + logging

✅ Can list feature scope from Discovery:
- Enhance argparse (add --e2e-test, --debug)
- E2E: single horizon, single run, 0-1 test values, ≤3 min
- Debug: behavioral changes + DEBUG logging
- Unit tests

✅ Understand relevant user answers:
- Q3 → E2E: test_values=0-1, horizons=['week_1_5'], run once
- Q4 → Debug: log_level='debug' + test_values=1-2 + horizons=1-2
- Q5 → Integration tests: validate exit code + specific accuracy outputs

---

## Next Steps (for S2.P2 Specification Phase)

1. Create detailed requirements in spec.md based on research findings
2. Add traceability for each requirement (Epic/User Answer/Derived)
3. Create checklist.md with any remaining questions (if needed)
4. Run Phase 1.5 Research Completeness Audit

**Research is comprehensive - ready to proceed to Phase 1.5 Audit.**

---

**END OF RESEARCH DOCUMENT**
