# Feature 05 Research: Win Rate Simulation Configurability

**Feature:** feature_05_win_rate_simulation
**Researcher:** Secondary-D
**Date:** 2026-01-29
**Phase:** S2.P1 (Research Phase)

---

## Discovery Context Summary

**From DISCOVERY.md Feature 05 Section (lines 323-343):**

**Purpose:** Add E2E mode and debug enhancements to win rate simulation

**Scope:**
- Enhance argparse (add --e2e-test flag)
- Add E2E test mode (single run, 0-1 random configs, ≤3 min)
- Enhance debug mode (already has --log-level, add behavioral changes for debug)
- Unit tests for E2E mode

**Key User Answers:**
- Q3: "Simulations: single run with 0-1 random configs"
- Q4: "Both logging AND behavioral changes" (DEBUG logs + fewer iterations/smaller datasets)
- Q5: "Check exit code AND verify expected outcomes (specific logs, result counts)"

**Estimated Size:** SMALL

---

## Components Researched

### 1. run_win_rate_simulation.py (Main Runner)

**File:** `run_win_rate_simulation.py` (lines 1-421)
**Purpose:** CLI entry point for win rate simulations

**Existing argparse (lines 94-214):**
- **Mode selection:** single, full, iterative (default: iterative)
  - single: Test baseline config (fast for debugging) - uses 2025 season (line 355)
  - full: Grid search all parameter combinations (very slow)
  - iterative: Coordinate descent optimization (one param at a time)
- **Arguments:** --sims, --baseline, --output, --workers, --data, --test-values, --use-processes
- **NO --debug flag:** Not implemented yet
- **NO --e2e-test flag:** Not implemented yet
- **NO --log-level flag:** LOGGING_LEVEL is hardcoded constant (line 33)

**Logging configuration (lines 32-37):**
```python
LOGGING_LEVEL = 'INFO'          # Hardcoded constant
LOGGING_TO_FILE = False
LOG_NAME = "simulation"
LOGGING_FILE = './simulation/log.txt'
LOGGING_FORMAT = 'standard'
```

**Entry point (line 117):**
```python
setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
```

**Implementation needed:**
- Add --e2e-test flag to argparse
- Add --debug flag (or use --log-level and interpret 'DEBUG' as debug mode)
- Modify LOGGING_LEVEL constant to accept CLI override
- Add E2E mode logic (trigger single mode with specific params)
- Add debug mode behavioral changes (reduce sims, test-values, workers)

---

### 2. SimulationManager (Core Simulation Engine)

**File:** `simulation/win_rate/SimulationManager.py` (lines 1-1129+)
**Purpose:** Orchestrates configuration optimization process

**Class:** SimulationManager (lines 47-1129+)

**Constructor parameters (lines 65-76):**
- baseline_config_path: Path to config folder (5-file structure)
- output_dir: Results directory
- num_simulations_per_config: Simulations per config (default from runner: 5)
- max_workers: Parallel workers (default from runner: 8)
- data_folder: Historical season data
- parameter_order: List of parameter names for optimization
- num_test_values: Number of test values per parameter (default: 5)
- num_parameters_to_test: Number of parameters to optimize in iterative mode (default: 1)
- use_processes: True = ProcessPoolExecutor, False = ThreadPoolExecutor

**Key method: run_single_config_test (lines 1099-1129):**
```python
def run_single_config_test(self, config_id: str = "test", season: str = "2025") -> None:
    """
    Run simulations for a single configuration (for debugging).

    .. deprecated::
        This method uses single-season data only. Use `run_iterative_optimization()`
        instead for multi-season validation across all historical data.
    """
```
- Uses baseline config directly (line 1129)
- Uses single season (default "2025") for speed
- Deprecated in favor of multi-season validation
- **This could be the basis for E2E mode!**

**Implementation notes:**
- E2E mode can leverage single mode + run_single_config_test
- Reduce num_simulations_per_config for E2E (e.g., 1-2 instead of default 5)
- Single season ("2025") already used by single mode for speed
- Debug mode: reduce workers, sims, test-values

---

### 3. ConfigGenerator (Parameter Combinations)

**File:** `simulation/shared/ConfigGenerator.py` (lines 1-99+)
**Purpose:** Generates parameter combinations for optimization

**Key concept (lines 4-6):**
"Generates parameter combinations by varying 23 key parameters, with N+1 values per parameter (optimal + N random variations). Total configurations = (N+1)^23 where N = num_test_values (default: 5)"

**"Random configs" clarification:**
- NOT truly random
- Systematic test values: optimal + N variations (min, max, and steps in between)
- For iterative mode: tests one parameter at a time
- For full mode: grid search all combinations (very slow)

**PARAM_DEFINITIONS (lines 88+):**
24 parameters with ranges (min, max, precision)
- Examples: NORMALIZATION_MAX_SCALE (50, 200), SAME_POS_BYE_WEIGHT (0.0, 0.5), etc.

**For E2E mode:**
- User Answer Q3: "0-1 random configs" means:
  - Option A: 0 configs (just baseline, no variations)
  - Option B: 1 config (baseline + 1 random variation)
- Likely interpretation: num_test_values=0 (baseline only) OR num_test_values=1 (baseline + 1 test value)

---

## Existing Test Patterns

### Integration Test File

**File:** `tests/integration/test_simulation_integration.py` (lines 1-535)
**Purpose:** Integration tests for win rate simulation workflow

**Test structure:**
- Uses pytest with fixtures: `baseline_config`, `temp_simulation_data`
- Creates mock historical season folders (lines 59-98)
- Creates minimal player/team CSV data (lines 109-145)
- Creates test config folders with 5-file structure (lines 149-239)

**Test classes:**
1. TestConfigGeneratorIntegration (lines 248-287)
2. TestSimulationManagerIntegration (lines 289-331)
3. TestParallelLeagueRunnerIntegration (lines 333-369)
4. TestResultsManagerIntegration (lines 371-413)
5. TestConfigPerformanceIntegration (lines 415-459)
6. TestEndToEndSimulationWorkflow (lines 461-496) - SKIPPED
7. TestErrorHandling (lines 498-531) - SKIPPED

**Key finding (line 310-327):**
```python
@pytest.mark.skip(reason="Requires full simulation environment. Single config test functionality verified by smoke tests.")
def test_simulation_manager_single_config_test(self, baseline_config, temp_simulation_data, tmp_path):
    """Test simulation manager can run single config test"""
    manager = SimulationManager(...)
    manager.run_single_config_test()  # This is what E2E mode should use!
```

**Pattern to follow for E2E integration tests:**
- Create minimal test data (not full historical data)
- Use small values: num_simulations_per_config=1, max_workers=1
- Validate exit code AND specific outcomes (wins, losses, output files)
- Check for expected log messages (DEBUG logs in debug mode)

---

## Interface Dependencies

### Classes this feature will call:

1. **LoggingManager** (`utils/LoggingManager.py`)
   - `setup_logger(name, level, to_file, file_path, format)` (called in runner line 117)
   - Supports log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
   - get_logger() to retrieve logger instance

2. **SimulationManager** (`simulation/win_rate/SimulationManager.py`)
   - Constructor: accepts num_simulations_per_config, max_workers, num_test_values
   - run_single_config_test(config_id, season): runs single config test
   - run_iterative_optimization(): runs full iterative optimization
   - run_full_optimization(): runs exhaustive grid search

3. **ConfigGenerator** (`simulation/shared/ConfigGenerator.py`)
   - Constructor: accepts baseline_config_path, num_test_values
   - generate_horizon_test_values(param_name): generates test values for parameter
   - get_config_for_horizon(horizon, param_name, value_index): gets specific config

### Files this feature will modify:

1. **run_win_rate_simulation.py** (MAJOR CHANGES)
   - Add --e2e-test flag to argparse
   - Add --debug flag (or use --log-level with 'DEBUG')
   - Convert LOGGING_LEVEL constant to CLI-overridable variable
   - Add E2E mode logic (conditional execution path)
   - Add debug mode behavioral changes

2. **simulation/ module logging** (MINOR CHANGES)
   - May need to add DEBUG logging statements in simulation/ module
   - Verify existing logging infrastructure (LoggingManager already used)

3. **tests/integration/test_simulation_integration.py** (ENHANCEMENTS)
   - Add test for --e2e-test flag
   - Add test for --debug flag
   - Add test validating E2E completes in ≤3 min
   - Add test validating debug mode behavioral changes

---

## Edge Cases Identified

### 1. E2E Mode Speed Requirements
- **Requirement:** ≤3 minutes total runtime
- **Challenge:** How to ensure speed? Need to measure current single mode speed
- **Solution approach:**
  - Use single mode as baseline
  - Reduce num_simulations_per_config to 1
  - Use single season (2025) not multi-season
  - Consider reducing max_workers to 1 for consistency
  - May need num_test_values=0 (baseline only, no variations)

### 2. Debug vs Log-Level Distinction
- **Current:** LOGGING_LEVEL constant (line 33) defaults to 'INFO'
- **User Answer Q4:** Debug mode = "both logging AND behavioral changes"
- **Options:**
  - Option A: --debug flag (separate from --log-level) triggers both DEBUG logging + behavioral changes
  - Option B: --log-level DEBUG triggers behavioral changes automatically
  - **Recommendation:** Option A (explicit --debug flag) for clarity

### 3. Backward Compatibility
- **Current:** No --debug or --e2e-test flags exist
- **Risk:** Minimal (adding new optional flags doesn't break existing usage)
- **Consideration:** Ensure defaults preserve current behavior
  - Default mode: iterative (unchanged)
  - Default logging: INFO (unchanged)
  - Default simulations: 5 (unchanged unless --e2e-test specified)

### 4. Integration Test Validation
- **User Answer Q5:** "Check exit code AND verify expected outcomes"
- **Need to validate:**
  - Exit code 0 for success
  - Specific log messages (e.g., "RUNNING SINGLE CONFIG TEST" for E2E)
  - Result files created (optimal_* folders)
  - Result counts (num_simulations matches expected)

### 5. "0-1 Random Configs" Interpretation
- **User Answer Q3:** "single run with 0-1 random configs"
- **Ambiguity:** What does "0-1" mean?
  - Interpretation 1: Zero OR one (either baseline only, or baseline + 1 variation)
  - Interpretation 2: Zero to one (a range, meaning "minimal configs")
- **Research finding:** ConfigGenerator uses num_test_values
  - num_test_values=0 → baseline only (1 config total)
  - num_test_values=1 → baseline + 1 test value (2 configs per parameter)
- **Recommendation:** Use num_test_values=0 for E2E (baseline only, fastest)

---

## Research Completeness

**Components identified:**
- [x] Main runner script (run_win_rate_simulation.py)
- [x] Core simulation engine (SimulationManager)
- [x] Config generator (ConfigGenerator)
- [x] Existing integration tests
- [x] Logging infrastructure (LoggingManager)

**Code read (with line numbers):**
- [x] run_win_rate_simulation.py (lines 1-421)
- [x] SimulationManager.py __init__ (lines 47-99)
- [x] SimulationManager.run_single_config_test (lines 1099-1129)
- [x] ConfigGenerator.py header (lines 1-99)
- [x] test_simulation_integration.py (lines 1-535)

**Interfaces documented:**
- [x] LoggingManager.setup_logger
- [x] SimulationManager constructor
- [x] SimulationManager.run_single_config_test
- [x] ConfigGenerator constructor

**Questions answered:**
1. Does run_win_rate_simulation.py have existing argparse? **YES** (extensive, lines 94-214)
2. Does it have --debug or --log-level? **NO** (LOGGING_LEVEL is hardcoded constant)
3. What is the simulation entry point? **SimulationManager.run_single_config_test** (line 1099)
4. What are "random configs"? **Systematic test values** (num_test_values parameter)
5. How long does single mode take? **Unknown** (need to measure, but designed for "fast debugging")
6. Where to add E2E logic? **In run_win_rate_simulation.py main()** (conditional based on --e2e-test flag)
7. Where is logging? **LoggingManager** (already integrated at line 117)
8. Where are tests? **tests/integration/test_simulation_integration.py** (535 lines)

**Ready for Phase 1.5 audit:** YES

---

## Next Steps

1. **Phase 1.5:** Research Completeness Audit (verify all 4 categories)
2. **S2.P2:** Create detailed specification with:
   - Exact argparse design (--e2e-test, --debug flags)
   - E2E mode implementation (single mode + minimal params)
   - Debug mode behavioral changes (reduce workers, sims, test-values)
   - Integration test requirements (exit code + outcome validation)
3. **Clarification needed:** Measure actual single mode runtime (to ensure ≤3 min)
