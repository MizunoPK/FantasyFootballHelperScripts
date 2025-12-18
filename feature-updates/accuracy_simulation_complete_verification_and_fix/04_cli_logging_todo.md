# Accuracy Simulation - CLI & Logging - Implementation TODO

## Iteration Progress Tracker

### Compact View (Quick Status)

```
R1: □□□□□□□ (0/7)   R2: □□□□□□□□□ (0/9)   R3: □□□□□□□□ (0/8)
```
Legend: ■ = complete, □ = pending, ▣ = in progress

**Current:** Iteration ___ ({type} - Round {N})
**Confidence:** HIGH / MEDIUM / LOW
**Blockers:** None / {description}

### Detailed View

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [ ]1 [ ]2 [ ]3 [ ]4 [ ]5 [ ]6 [ ]7 | 0/7 |
| Second (9) | [ ]8 [ ]9 [ ]10 [ ]11 [ ]12 [ ]13 [ ]14 [ ]15 [ ]16 | 0/9 |
| Third (8) | [ ]17 [ ]18 [ ]19 [ ]20 [ ]21 [ ]22 [ ]23 [ ]24 | 0/8 |

**Current Iteration:** ___

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [ ]1 [ ]2 [ ]3 [ ]8 [ ]9 [ ]10 [ ]15 [ ]16 |
| Algorithm Traceability | 4, 11, 19 | [ ]4 [ ]11 [ ]19 |
| End-to-End Data Flow | 5, 12 | [ ]5 [ ]12 |
| Skeptical Re-verification | 6, 13, 22 | [ ]6 [ ]13 [ ]22 |
| Integration Gap Check | 7, 14, 23 | [ ]7 [ ]14 [ ]23 |
| Fresh Eyes Review | 17, 18 | [ ]17 [ ]18 |
| Edge Case Verification | 20 | [ ]20 |
| Test Coverage Planning + Mock Audit | 21 | [ ]21 |
| Implementation Readiness | 24 | [ ]24 |
| Interface Verification | Pre-impl | [ ] |

---

## Verification Summary

- Iterations completed: 0/24
- Requirements from spec: 2 (--log-level flag, systematic logging review)
- Requirements in TODO: 2
- Questions for user: 0
- Integration points identified: 1

---

## Sub-Feature Overview

**Name:** CLI & Logging (Phase 4 of 5)
**Priority:** Observability improvement
**Dependencies:** Phase 3 (Parallel Processing) must be complete
**Next Phase:** 05_testing_validation_todo.md

**What this sub-feature implements:**
1. Add --log-level CLI flag with choices (debug, info, warning, error) (Q44)
2. Systematic review of all logging statements in accuracy simulation (Q44)
3. Add debug-level logging for detailed visibility
4. Ensure info-level shows only new bests and summaries

**Why these are grouped:**
- All observability-related enhancements
- Logging control critical for continuous optimization loops
- Debug logging helps troubleshoot issues
- Info logging keeps output clean for normal operation
- Small scope - can be completed quickly

---

## Phase 1: Add --log-level CLI Flag

### Task 1.1: Add --log-level argument to run_accuracy_simulation.py

- **File:** `run_accuracy_simulation.py`
- **Location:** CLI argument parsing section
- **Status:** [ ] Not started

**Implementation details:**
1. Add constant for default log level
2. Add argparse argument with choices
3. Configure logging based on flag
4. Pass log level to AccuracySimulationManager

**Constant to add:**
```python
# Logging defaults
DEFAULT_LOG_LEVEL = 'info'
```

**Argument to add:**
```python
parser.add_argument(
    '--log-level',
    choices=['debug', 'info', 'warning', 'error'],
    default=DEFAULT_LOG_LEVEL,
    help=f'Logging level (default: {DEFAULT_LOG_LEVEL}). '
         'debug: all evaluations + parameter updates + worker activity. '
         'info: new bests + parameter completion + summaries. '
         'warning: warnings only. '
         'error: errors only.'
)
```

**Configure logging:**
```python
# Convert string to logging level
log_level_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
}

# Set log level
logging.getLogger().setLevel(log_level_map[args.log_level])
```

**Pass to manager (optional):**
```python
manager = AccuracySimulationManager(
    # ... existing args ...
    log_level=args.log_level  # Optional - manager can check current logger level
)
```

**Verification:**
- [ ] DEFAULT_LOG_LEVEL constant defined
- [ ] --log-level argument added with choices
- [ ] Help text clear and describes each level
- [ ] Logging configured based on flag
- [ ] Test: `--log-level debug` shows detailed output
- [ ] Test: `--log-level info` shows clean output
- [ ] Test: `--log-level warning` shows only warnings

---

## Phase 2: Systematic Logging Review

### Task 2.1: Audit all logging statements in AccuracySimulationManager.py

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Purpose:** Ensure appropriate log levels for all statements
- **Status:** [ ] Not started

**Implementation details:**
1. Read entire AccuracySimulationManager.py
2. For each logger statement, determine correct level:
   - **DEBUG**: Every config evaluation, parameter updates, worker activity
   - **INFO**: New bests, parameter completion, summaries, major milestones
   - **WARNING**: Unexpected but recoverable situations
   - **ERROR**: Serious problems, failures
3. Update log levels as needed
4. Add missing debug-level logging

**Logging guidelines:**

**DEBUG level should show:**
- Each config evaluation result:
  ```python
  self.logger.debug(f"Config test_{test_idx}: ros={result_ros.mae:.4f} MAE, 1-5={result_1_5.mae:.4f} MAE, ...")
  ```
- Parameter updates:
  ```python
  self.logger.debug(f"Updated baseline for {horizon}: {param_name} {old_value}→{new_value}")
  ```
- Parallel worker activity (if visible):
  ```python
  self.logger.debug(f"Worker {worker_id} completed config test_{test_idx}")
  ```
- Resume state detection:
  ```python
  self.logger.debug(f"Found intermediate folder: {folder_name}")
  ```

**INFO level should show:**
- Parameter optimization start:
  ```python
  self.logger.info(f"Optimizing parameter {param_idx + 1}/{total}: {param_name}")
  ```
- New best found:
  ```python
  self.logger.info(f"  New best for {horizon}: MAE={mae:.4f} (test_{test_idx})")
  ```
- Parameter completion summary:
  ```python
  self.logger.info(f"Parameter {param_name} complete:")
  self.logger.info(f"  {horizon}: MAE={mae:.4f} (test_{test_idx})")
  ```
- Optimization complete:
  ```python
  self.logger.info(f"Tournament optimization complete. Results saved to {folder}")
  ```
- Resume detected:
  ```python
  self.logger.info(f"Resuming from parameter {param_idx + 1}")
  ```

**Audit checklist:**
- [ ] Read all logger.debug() statements - verify appropriate
- [ ] Read all logger.info() statements - verify appropriate
- [ ] Read all logger.warning() statements - verify appropriate
- [ ] Read all logger.error() statements - verify appropriate
- [ ] Add missing debug statements for config evaluations
- [ ] Add missing debug statements for parameter updates
- [ ] Ensure info level shows only major milestones
- [ ] Ensure no verbose output at info level

---

### Task 2.2: Audit all logging statements in AccuracyResultsManager.py

- **File:** `simulation/accuracy/AccuracyResultsManager.py`
- **Purpose:** Ensure appropriate log levels for results tracking
- **Status:** [ ] Not started

**Implementation details:**
1. Read AccuracyResultsManager.py
2. Check logging in:
   - add_result() - should be debug or no logging (called frequently)
   - save_intermediate_results() - should be info (major milestone)
   - save_optimal_configs() - should be info (major milestone)
   - load_intermediate_results() - should be info (resume operation)
3. Update as needed

**Expected logging:**

**add_result():**
- No logging at info level (too frequent)
- Optional debug logging:
  ```python
  self.logger.debug(f"Added result for {horizon}: MAE={perf.mae:.4f}, player_count={perf.player_count}")
  ```

**save_intermediate_results():**
- Info level (major milestone):
  ```python
  self.logger.info(f"Saved intermediate results to {folder}")
  self.logger.info(f"Saved metadata to {metadata_path}")
  ```

**save_optimal_configs():**
- Info level (major milestone):
  ```python
  self.logger.info(f"Saved optimal configs to {folder}")
  ```

**load_intermediate_results():**
- Info level (resume operation):
  ```python
  self.logger.info(f"Loaded intermediate results from {folder}")
  ```

**Audit checklist:**
- [ ] add_result() uses debug level or no logging
- [ ] save_intermediate_results() uses info level
- [ ] save_optimal_configs() uses info level
- [ ] load_intermediate_results() uses info level
- [ ] No verbose output at info level

---

### Task 2.3: Audit all logging statements in AccuracyCalculator.py

- **File:** `simulation/accuracy/AccuracyCalculator.py`
- **Purpose:** Ensure appropriate log levels for MAE calculations
- **Status:** [ ] Not started

**Implementation details:**
1. Read AccuracyCalculator.py
2. Check logging in:
   - calculate_ros_mae() - should be debug (called frequently)
   - calculate_weekly_mae() - should be debug (called frequently)
   - Error handling - should be error level
3. Update as needed

**Expected logging:**

**calculate_ros_mae():**
- Debug level (called for every config):
  ```python
  self.logger.debug(f"Calculating ROS MAE: {player_count} players, total_error={total_error:.2f}")
  ```

**calculate_weekly_mae():**
- Debug level (called for every config):
  ```python
  self.logger.debug(f"Calculating weekly MAE for {week_range}: {player_count} players, total_error={total_error:.2f}")
  ```

**Error cases:**
- Error level:
  ```python
  self.logger.error(f"Failed to calculate MAE: {e}", exc_info=True)
  ```

**Audit checklist:**
- [ ] calculate_ros_mae() uses debug level
- [ ] calculate_weekly_mae() uses debug level
- [ ] Error handling uses error level
- [ ] No info-level logging (too frequent)

---

### Task 2.4: Audit all logging statements in ParallelAccuracyRunner.py

- **File:** `simulation/accuracy/ParallelAccuracyRunner.py`
- **Purpose:** Ensure appropriate log levels for parallel processing
- **Status:** [ ] Not started

**Implementation details:**
1. Read ParallelAccuracyRunner.py
2. Check logging in:
   - evaluate_configs_parallel() - info for start, debug for workers
   - Error handling - error level
3. Update as needed

**Expected logging:**

**evaluate_configs_parallel() start:**
- Info level (major operation):
  ```python
  self.logger.info(f"Starting parallel evaluation: {len(configs)} configs × 5 horizons = {len(configs) * 5} total evaluations")
  self.logger.info(f"Using {executor_name} with {self.max_workers} workers")
  ```

**Worker activity:**
- Debug level (too frequent for info):
  ```python
  self.logger.debug(f"Worker completed config {completed}/{total}")
  ```

**Error handling:**
- Error level:
  ```python
  self.logger.error(f"Config evaluation failed: {e}", exc_info=True)
  ```

**Audit checklist:**
- [ ] evaluate_configs_parallel() start uses info level
- [ ] Worker activity uses debug level
- [ ] Error handling uses error level
- [ ] No verbose output at info level

---

## Phase 3: Add Debug-Level Logging

### Task 3.1: Add debug logging for config evaluations in run_both()

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** `run_both()`
- **Status:** [ ] Not started

**Implementation details:**
1. After each config evaluation, add debug logging
2. Show MAE for all 5 horizons
3. Only logged at debug level (not info)

**Algorithm specification:**
```python
# In run_both(), after recording results:
for (config_dict, results_dict), (horizon, test_idx) in zip(evaluation_results, config_metadata):
    # Debug: Log all 5 MAE values
    mae_summary = ", ".join([f"{h}={r.mae:.4f}" for h, r in results_dict.items()])
    self.logger.debug(f"    Config test_{test_idx} (base={horizon}): {mae_summary}")

    # Record results for each horizon...
```

**Example output at debug level:**
```
Config test_05 (base=ros): ros=2.34, 1-5=2.41, 6-9=2.38, 10-13=2.45, 14-17=2.52
```

**Verification:**
- [ ] Debug logging added after config evaluation
- [ ] Shows all 5 MAE values
- [ ] Only at debug level (not info)
- [ ] Format clear and concise

---

### Task 3.2: Add debug logging for baseline updates

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** `run_both()`
- **Status:** [ ] Not started

**Implementation details:**
1. Before/after updating baselines, add debug logging
2. Show old and new values for parameter

**Algorithm specification:**
```python
# In run_both(), when updating baselines:
for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
    old_config = self.config_generator.baseline_configs[horizon]
    old_value = old_config.get(param_name, None)

    best_config = self.results_manager.best_configs[horizon].config
    new_value = best_config.get(param_name, None)

    self.config_generator.update_baseline_for_horizon(horizon, best_config)

    if old_value != new_value:
        self.logger.debug(f"  Updated baseline for {horizon}: {param_name} {old_value}→{new_value}")
```

**Example output at debug level:**
```
Updated baseline for ros: NORMALIZATION_MAX_SCALE 100→150
Updated baseline for 1-5: NORMALIZATION_MAX_SCALE 100→120
```

**Verification:**
- [ ] Debug logging added for baseline updates
- [ ] Shows old → new value
- [ ] Only logs if value changed
- [ ] Only at debug level (not info)

---

### QA CHECKPOINT 4: CLI & Logging Validation

- **Status:** [ ] Not started
- **Expected outcome:** Logging levels work correctly
- **Test commands:**
  - `python run_accuracy_simulation.py --test-values 2 --num-params 1 --log-level debug`
  - `python run_accuracy_simulation.py --test-values 2 --num-params 1 --log-level info`
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] --log-level flag accepted
  - [ ] Debug level shows detailed output:
    - [ ] Each config evaluation with all 5 MAE values
    - [ ] Baseline updates with old→new values
    - [ ] Worker activity (if visible)
  - [ ] Info level shows clean output:
    - [ ] Parameter optimization start
    - [ ] New bests only
    - [ ] Parameter completion summaries
    - [ ] Major milestones
    - [ ] NO config-level details
  - [ ] Warning level shows only warnings
  - [ ] Error level shows only errors
  - [ ] No inappropriate log levels found

**If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (Verified Pre-Implementation)

### --log-level CLI flag
- **Argument:** `--log-level {debug,info,warning,error}`
- **Source:** `run_accuracy_simulation.py`
- **Default:** 'info'
- **Verified:** [ ]

### Logging configuration
- **Function:** Configure logging based on CLI flag
- **Source:** `run_accuracy_simulation.py:main()`
- **Behavior:** Set logging.getLogger() level
- **Verified:** [ ]

### Quick E2E Validation Plan
- **Minimal test command:**
  ```bash
  # Debug level
  python run_accuracy_simulation.py --test-values 2 --num-params 1 --log-level debug | head -100

  # Info level
  python run_accuracy_simulation.py --test-values 2 --num-params 1 --log-level info | head -100
  ```
- **Expected result:**
  - Debug: Shows every config evaluation, baseline updates, worker activity
  - Info: Shows only new bests, parameter summaries, major milestones
  - Debug output significantly longer than info output
- **Run before:** Full implementation begins
- **Status:** [ ] Not run | [ ] Passed | [ ] Failed (fix before proceeding)

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| --log-level flag | run_accuracy_simulation.py | main() | run_accuracy_simulation.py:~70 | Task 1.1 (add arg) |
| Logging configuration | run_accuracy_simulation.py | main() | run_accuracy_simulation.py:~90 | Task 1.1 (configure) |
| Debug logging | AccuracySimulationManager.py | run_both() | AccuracySimulationManager.py:~820 | Task 3.1, 3.2 (add statements) |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Q44 Resolution | --log-level flag | run_accuracy_simulation.py:argparse | choices=['debug','info','warning','error'] |
| Q44 Resolution | Logging configuration | run_accuracy_simulation.py:main() | Set logger level based on flag |
| Q44 Resolution | Debug-level details | AccuracySimulationManager.py:run_both() | logger.debug() for each config |
| Q44 Resolution | Info-level summaries | AccuracySimulationManager.py:run_both() | logger.info() for new bests + summaries |
| Q44 Resolution | Systematic review | All accuracy files | Audit all logger statements |

---

## Data Flow Traces

### Requirement: Log level control
```
Entry: main()
  → argparse: --log-level {debug,info,warning,error}
  → log_level_map[args.log_level]
  → logging.getLogger().setLevel(level)
  → All loggers respect level:
      - logger.debug() only shown if level=DEBUG
      - logger.info() shown if level<=INFO
  → Result: User controls verbosity
```

### Requirement: Debug-level visibility
```
Entry: run_both() with --log-level debug
  → For each config:
      → logger.debug(f"Config test_{idx}: ros={mae1}, 1-5={mae2}, ...")
  → For each baseline update:
      → logger.debug(f"Updated baseline for {horizon}: {param} {old}→{new}")
  → Result: Full visibility into optimization process
```

### Requirement: Info-level cleanliness
```
Entry: run_both() with --log-level info
  → Only log:
      - Parameter start: logger.info(f"Optimizing parameter...")
      - New bests: logger.info(f"New best for {horizon}: MAE=...")
      - Parameter summary: logger.info(f"Parameter complete:")
      - Optimization complete: logger.info(f"Tournament optimization complete")
  → Result: Clean output for normal operation
```

---

## Verification Gaps

Document any gaps found during iterations here:

### Iteration {X} Gaps
(To be filled during verification iterations)

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:** (To be filled)
- **Corrections made:** (To be filled)
- **Confidence level:** (To be filled)

### Round 2 (Iteration 13)
- **Verified correct:** (To be filled)
- **Corrections made:** (To be filled)
- **Confidence level:** (To be filled)

### Round 3 (Iteration 22)
- **Verified correct:** (To be filled)
- **Corrections made:** (To be filled)
- **Confidence level:** (To be filled)

---

## Integration Gap Check Results

### Check 1 (Iteration 7)
**Every new method has a caller:**
- [ ] --log-level flag: Used by main() to configure logging
- [ ] Debug logging: Called during optimization loops

**Every caller modified:**
- [ ] Task 1.1: main() adds --log-level argument and configures logging
- [ ] Task 3.1: run_both() adds debug logging for config evaluations
- [ ] Task 3.2: run_both() adds debug logging for baseline updates

**Status:** (To be filled)

### Check 2 (Iteration 14)
(To be filled)

### Check 3 (Iteration 23)
(To be filled)

---

## Notes

- This is Phase 4 of 5 sub-features
- Observability improvement
- Small scope - should complete quickly
- Critical for debugging optimization issues
- Must complete all 24 verification iterations before implementing
- Dependencies: Phase 3 (Parallel Processing) must be complete
- Next phase: 05_testing_validation_todo.md
