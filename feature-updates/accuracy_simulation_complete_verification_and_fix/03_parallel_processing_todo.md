# Accuracy Simulation - Parallel Processing - Implementation TODO

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
- Requirements from spec: 3 (parallel evaluation, progress tracking, CLI flags)
- Requirements in TODO: 3
- Questions for user: 0
- Integration points identified: 2

---

## Sub-Feature Overview

**Name:** Parallel Processing (Phase 3 of 5)
**Priority:** Performance enhancement
**Dependencies:** Phase 2 (Tournament Rewrite) must be complete
**Next Phase:** 04_cli_logging_todo.md

**What this sub-feature implements:**
1. Create ParallelAccuracyRunner.py with module-level evaluation function (Q15)
2. Implement parallel config evaluation with ProcessPoolExecutor (Q13)
3. Add MultiLevelProgressTracker integration (Q17, Q22)
4. Add --max-workers and --use-processes CLI flags (Q13, Q18)
5. Pass explicit parameters to parallel workers (Q16)

**Why these are grouped:**
- All performance-related enhancements
- Parallel processing significantly speeds up tournament optimization
- ProcessPoolExecutor bypasses GIL for true parallelism
- Proper progress tracking essential for long-running optimizations
- 525 evaluations per parameter warrants parallelization

---

## Phase 1: Create ParallelAccuracyRunner Module

### Task 1.1: Create new file ParallelAccuracyRunner.py

- **File:** `simulation/accuracy/ParallelAccuracyRunner.py` (NEW FILE)
- **Purpose:** Module-level evaluation function for ProcessPoolExecutor pickling
- **Pattern:** Follow win-rate simulation's ParallelLeagueRunner.py
- **Status:** [ ] Not started

**Implementation details:**
1. Review win-rate simulation's `simulation/win_rate/ParallelLeagueRunner.py` as reference
2. Create new file `simulation/accuracy/ParallelAccuracyRunner.py`
3. Implement module-level evaluation function
4. Implement ParallelAccuracyRunner class

**File structure:**
```python
"""
Parallel processing support for accuracy simulation using ProcessPoolExecutor.

This module provides parallel evaluation of configs across multiple horizons
to speed up tournament optimization. Each config is evaluated across all 5
horizons (ROS, week 1-5, 6-9, 10-13, 14-17) to calculate MAE.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

from simulation.accuracy.AccuracyCalculator import AccuracyCalculator, AccuracyResult
from utils.LoggingManager import get_logger


def _evaluate_config_tournament_process(
    config_dict: Dict[str, Any],
    data_folder: Path,
    available_seasons: List[str]
) -> Tuple[Dict[str, Any], Dict[str, AccuracyResult]]:
    """
    Module-level function to evaluate single config across all 5 horizons.

    Must be module-level for ProcessPoolExecutor pickling.

    Args:
        config_dict: Configuration to evaluate
        data_folder: Path to simulation data folder (sim_data/)
        available_seasons: List of season folders to use

    Returns:
        Tuple of (config_dict, results_dict) where results_dict maps horizon to AccuracyResult:
        {'ros': result_ros, '1-5': result_1_5, '6-9': result_6_9, '10-13': result_10_13, '14-17': result_14_17}
    """
    # Create calculator (stateless except logger - safe for parallel)
    calculator = AccuracyCalculator(data_folder, available_seasons)

    results = {}

    # Evaluate ROS horizon
    results['ros'] = calculator.calculate_ros_mae(data_folder, config_dict)

    # Evaluate all 4 weekly horizons
    for week_horizon in ['1-5', '6-9', '10-13', '14-17']:
        results[week_horizon] = calculator.calculate_weekly_mae(data_folder, config_dict, week_horizon)

    return (config_dict, results)


class ParallelAccuracyRunner:
    """
    Manages parallel evaluation of accuracy configs using ProcessPoolExecutor.

    Evaluates multiple configs in parallel across all 5 horizons to speed up
    tournament optimization. Each config gets 5 MAE calculations (one per horizon).
    """

    def __init__(
        self,
        data_folder: Path,
        available_seasons: List[str],
        max_workers: int = 8,
        use_processes: bool = True
    ):
        """
        Initialize parallel runner.

        Args:
            data_folder: Path to simulation data folder
            available_seasons: List of season folders to use
            max_workers: Number of parallel workers (default: 8)
            use_processes: Use ProcessPoolExecutor (True) or ThreadPoolExecutor (False)
        """
        self.data_folder = data_folder
        self.available_seasons = available_seasons
        self.max_workers = max_workers
        self.use_processes = use_processes
        self.logger = get_logger()

    def evaluate_configs_parallel(
        self,
        configs: List[Dict[str, Any]],
        progress_callback = None
    ) -> List[Tuple[Dict[str, Any], Dict[str, AccuracyResult]]]:
        """
        Evaluate multiple configs in parallel across all 5 horizons.

        Args:
            configs: List of config dicts to evaluate
            progress_callback: Optional callback(completed_count) to track progress

        Returns:
            List of (config_dict, results_dict) tuples in same order as input
        """
        if len(configs) == 0:
            return []

        # Choose executor type
        executor_class = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor
        executor_name = "ProcessPoolExecutor" if self.use_processes else "ThreadPoolExecutor"

        self.logger.info(f"Starting parallel evaluation: {len(configs)} configs × 5 horizons = {len(configs) * 5} total evaluations")
        self.logger.info(f"Using {executor_name} with {self.max_workers} workers")

        results = []
        completed = 0

        with executor_class(max_workers=self.max_workers) as executor:
            # Submit all configs
            future_to_config = {
                executor.submit(
                    _evaluate_config_tournament_process,
                    config,
                    self.data_folder,
                    self.available_seasons
                ): config
                for config in configs
            }

            # Collect results as they complete
            for future in as_completed(future_to_config):
                config = future_to_config[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1

                    # Progress callback
                    if progress_callback is not None:
                        progress_callback(completed)

                except Exception as e:
                    self.logger.error(f"Config evaluation failed: {e}", exc_info=True)
                    raise  # Fail-fast (Q10 decision)

        # Sort results to match input order (futures complete in arbitrary order)
        config_to_result = {str(cfg): res for cfg, res in results}
        ordered_results = [(cfg, config_to_result[str(cfg)][1]) for cfg in configs]

        return ordered_results
```

**Verification:**
- [ ] File created in correct location
- [ ] Module-level function defined
- [ ] Module-level function returns correct tuple format
- [ ] ParallelAccuracyRunner class defined
- [ ] __init__ accepts correct parameters
- [ ] evaluate_configs_parallel() submits jobs to executor
- [ ] Results collected as they complete
- [ ] Progress callback supported
- [ ] Fail-fast on exceptions (Q10 decision)
- [ ] Results ordered to match input

---

## Phase 2: Integrate Parallel Processing into Tournament Optimization

### Task 2.1: Modify run_both() to use parallel evaluation

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** `run_both()` (modified in Phase 2)
- **Status:** [ ] Not started

**Implementation details:**
1. Read run_both() from Phase 2 (tournament rewrite)
2. Add parallel_runner as instance variable in __init__
3. Modify run_both() to batch configs and evaluate in parallel
4. Keep rest of logic unchanged

**Changes to __init__:**
```python
def __init__(
    self,
    # ... existing params ...
    max_workers: int = 8,
    use_processes: bool = True
):
    # ... existing initialization ...

    # Parallel processing
    self.max_workers = max_workers
    self.use_processes = use_processes
    self.parallel_runner = None  # Lazy initialization
```

**Changes to run_both():**
```python
# Replace this pattern:
for horizon, test_values in test_values_dict.items():
    for test_idx, test_value in enumerate(test_values):
        config_dict = self.config_generator.get_config_for_horizon(horizon, param_name, test_idx)
        all_results = self._evaluate_config_tournament(config_dict, horizon)
        # ... record results ...

# With parallel pattern:
# 1. Collect all configs to evaluate
configs_to_evaluate = []
config_metadata = []  # Track (horizon, test_idx) for each config

for horizon, test_values in test_values_dict.items():
    for test_idx, test_value in enumerate(test_values):
        config_dict = self.config_generator.get_config_for_horizon(horizon, param_name, test_idx)
        configs_to_evaluate.append(config_dict)
        config_metadata.append((horizon, test_idx))

# 2. Initialize parallel runner (lazy)
if self.parallel_runner is None:
    from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner
    self.parallel_runner = ParallelAccuracyRunner(
        self.data_folder,
        self.available_seasons,
        max_workers=self.max_workers,
        use_processes=self.use_processes
    )

# 3. Evaluate all configs in parallel with progress tracking
self.logger.info(f"  Evaluating {len(configs_to_evaluate)} configs in parallel...")

# Progress callback (will implement in Task 3.1)
def progress_update(completed):
    if hasattr(self, 'progress_tracker') and self.progress_tracker:
        self.progress_tracker.next_outer()  # Increment outer level

evaluation_results = self.parallel_runner.evaluate_configs_parallel(
    configs_to_evaluate,
    progress_callback=progress_update
)

# 4. Record all results
for (config_dict, results_dict), (horizon, test_idx) in zip(evaluation_results, config_metadata):
    # Record results for each horizon
    for result_horizon, result in results_dict.items():
        is_new_best = self.results_manager.add_result(
            result_horizon,
            config_dict,
            result,
            config_id=f"{param_name}_{test_idx}_horizon_{result_horizon}",
            param_name=param_name,
            test_idx=test_idx,
            base_horizon=horizon
        )

        # Log new bests
        if is_new_best:
            self.logger.info(f"    New best for {result_horizon}: MAE={result.mae:.4f} (test_{test_idx})")
```

**Verification:**
- [ ] __init__ accepts max_workers and use_processes parameters
- [ ] parallel_runner initialized lazily
- [ ] All configs collected before parallel evaluation
- [ ] config_metadata tracks horizon and test_idx
- [ ] evaluate_configs_parallel() called with all configs
- [ ] Progress callback provided
- [ ] Results processed and recorded correctly
- [ ] New bests still logged
- [ ] Existing behavior preserved (just parallelized)

---

## Phase 3: Add MultiLevelProgressTracker Integration

### Task 3.1: Add MultiLevelProgressTracker to run_both()

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** `run_both()`
- **Pattern:** Match win-rate simulation's progress tracking
- **Status:** [ ] Not started

**Implementation details:**
1. Import MultiLevelProgressTracker from simulation/shared/ProgressTracker.py
2. Calculate total configs per parameter
3. Create progress tracker with outer=configs, inner=horizons
4. Update progress after each config completes

**Algorithm specification:**
```python
from simulation.shared.ProgressTracker import MultiLevelProgressTracker

# In run_both(), before parameter loop:
for param_idx, param_name in enumerate(self.parameter_order):
    # ... existing code ...

    # Calculate total configs for this parameter
    test_values_dict = self.config_generator.generate_horizon_test_values(param_name)
    total_configs = sum(len(vals) for vals in test_values_dict.values())
    total_evaluations = total_configs * 5  # Each config × 5 horizons

    # Create progress tracker
    self.progress_tracker = MultiLevelProgressTracker(
        outer_total=total_configs,
        inner_total=5,
        outer_desc="Configs",
        inner_desc="Horizons"
    )

    self.logger.info(f"Optimizing parameter {param_idx + 1}/{len(self.parameter_order)}: {param_name}")
    self.logger.info(f"  Evaluating {total_configs} configs × 5 horizons = {total_evaluations} total evaluations")

    # ... collect configs ...

    # Evaluate with progress tracking
    def progress_update(completed):
        self.progress_tracker.next_outer()  # Increment outer (completed config)
        # Note: Inner level auto-increments in MultiLevelProgressTracker

    evaluation_results = self.parallel_runner.evaluate_configs_parallel(
        configs_to_evaluate,
        progress_callback=progress_update
    )

    # Close progress tracker after parameter completes
    self.progress_tracker.close()
```

**Progress display format (from Q22 research):**
```
Configs: 42/105 (40.0%) | Horizons: 3/5 (60.0%) | Overall: 40.6% | Elapsed: 2m 15s | ETA: 3m 18s
```

**Verification:**
- [ ] MultiLevelProgressTracker imported
- [ ] Total configs calculated correctly
- [ ] Progress tracker created with outer=configs, inner=5
- [ ] Progress callback increments outer level
- [ ] Progress tracker closed after parameter completes
- [ ] Display shows config progress, horizon progress, overall, ETA

---

### Task 3.2: Verify MultiLevelProgressTracker exists and works

- **File:** `simulation/shared/ProgressTracker.py`
- **Class:** `MultiLevelProgressTracker`
- **Status:** [ ] Not started

**Implementation details:**
1. Read simulation/shared/ProgressTracker.py
2. Verify MultiLevelProgressTracker class exists
3. Verify interface matches win-rate simulation usage
4. NO CHANGES NEEDED (just verification)

**Expected interface:**
```python
class MultiLevelProgressTracker:
    def __init__(
        self,
        outer_total: int,
        inner_total: int,
        outer_desc: str = "Outer",
        inner_desc: str = "Inner"
    ):
        ...

    def next_outer(self) -> None:
        """Increment outer level counter."""
        ...

    def update_inner(self, n: int = 1) -> None:
        """Increment inner level counter."""
        ...

    def close(self) -> None:
        """Close progress tracker."""
        ...
```

**Verification:**
- [ ] MultiLevelProgressTracker class exists
- [ ] __init__ accepts outer_total, inner_total, descriptions
- [ ] next_outer() method exists
- [ ] update_inner() method exists
- [ ] close() method exists
- [ ] NO CODE CHANGES NEEDED

---

## Phase 4: Add CLI Flags for Parallel Processing

### Task 4.1: Add --max-workers and --use-processes flags

- **File:** `run_accuracy_simulation.py`
- **Location:** CLI argument parsing section
- **Status:** [ ] Not started

**Implementation details:**
1. Add constants at top of file (Q18 decision)
2. Add argparse arguments for parallel processing
3. Pass to AccuracySimulationManager

**Constants to add:**
```python
# Parallel processing defaults
DEFAULT_MAX_WORKERS = 8
DEFAULT_USE_PROCESSES = True
```

**Arguments to add:**
```python
parser.add_argument(
    '--max-workers',
    type=int,
    default=DEFAULT_MAX_WORKERS,
    help=f'Number of parallel workers for config evaluation (default: {DEFAULT_MAX_WORKERS})'
)

parser.add_argument(
    '--use-processes',
    dest='use_processes',
    action='store_true',
    default=DEFAULT_USE_PROCESSES,
    help='Use ProcessPoolExecutor for true parallelism (default, bypasses GIL)'
)

parser.add_argument(
    '--no-use-processes',
    dest='use_processes',
    action='store_false',
    help='Use ThreadPoolExecutor instead of processes (slower, for debugging)'
)
```

**Pass to manager:**
```python
manager = AccuracySimulationManager(
    # ... existing args ...
    max_workers=args.max_workers,
    use_processes=args.use_processes
)
```

**Verification:**
- [ ] Constants defined at top of file
- [ ] --max-workers argument added
- [ ] --use-processes / --no-use-processes arguments added
- [ ] Arguments passed to AccuracySimulationManager
- [ ] Help text clear and accurate
- [ ] Defaults match constants

---

### QA CHECKPOINT 3: Parallel Processing Validation

- **Status:** [ ] Not started
- **Expected outcome:** Parallel processing significantly speeds up optimization
- **Test command:** `python run_accuracy_simulation.py --test-values 2 --num-params 1 --max-workers 8`
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] CLI accepts --max-workers and --use-processes flags
  - [ ] Tournament optimization uses parallel processing
  - [ ] ProcessPoolExecutor initialized with correct worker count
  - [ ] All configs evaluated in parallel
  - [ ] Progress tracker shows config progress, horizon progress, ETA
  - [ ] Results same as sequential (correctness)
  - [ ] Performance improvement observed (faster than sequential)
  - [ ] No race conditions or parallel execution errors
  - [ ] Test with --no-use-processes (ThreadPoolExecutor fallback)
  - [ ] No errors in output

**Performance benchmark:**
- Sequential (Phase 2): ~X minutes for 105 configs × 5 horizons
- Parallel with 8 workers: Should be ~8x faster (estimate: X/8 minutes)
- Document actual speedup in QC report

**If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (Verified Pre-Implementation)

### _evaluate_config_tournament_process()
- **Function:** Module-level function for ProcessPoolExecutor
- **Source:** `simulation/accuracy/ParallelAccuracyRunner.py` (NEW)
- **Signature:** `(config_dict, data_folder, available_seasons) -> (config_dict, results_dict)`
- **Must be:** Module-level (not method) for pickling
- **Verified:** [ ]

### ParallelAccuracyRunner.evaluate_configs_parallel()
- **Method:** `evaluate_configs_parallel(configs, progress_callback) -> List[Tuple]`
- **Source:** `simulation/accuracy/ParallelAccuracyRunner.py` (NEW)
- **Returns:** List of (config_dict, results_dict) tuples
- **Verified:** [ ]

### AccuracySimulationManager.__init__
- **Method:** Modified to accept max_workers and use_processes
- **Source:** `simulation/accuracy/AccuracySimulationManager.py`
- **New params:** max_workers (int), use_processes (bool)
- **Verified:** [ ]

### MultiLevelProgressTracker
- **Class:** Existing progress tracker for two-level progress
- **Source:** `simulation/shared/ProgressTracker.py`
- **Methods:** __init__, next_outer(), update_inner(), close()
- **Verified:** [ ]

### Quick E2E Validation Plan
- **Minimal test command:**
  ```bash
  python run_accuracy_simulation.py --test-values 2 --num-params 1 --max-workers 4
  ```
- **Expected result:**
  - Parallel processing starts
  - 4 workers used
  - Progress tracker shows configs, horizons, ETA
  - Results correct (match sequential)
  - Faster than sequential execution
- **Run before:** Full implementation begins
- **Status:** [ ] Not run | [ ] Passed | [ ] Failed (fix before proceeding)

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| ParallelAccuracyRunner | ParallelAccuracyRunner.py | run_both() | AccuracySimulationManager.py:~800 | Task 2.1 (initialize + call) |
| _evaluate_config_tournament_process() | ParallelAccuracyRunner.py | evaluate_configs_parallel() | ParallelAccuracyRunner.py:~100 | Task 1.1 (submit to executor) |
| MultiLevelProgressTracker | ProgressTracker.py | run_both() | AccuracySimulationManager.py:~790 | Task 3.1 (create tracker) |
| --max-workers flag | run_accuracy_simulation.py | main() | run_accuracy_simulation.py:~60 | Task 4.1 (add arg) |
| --use-processes flag | run_accuracy_simulation.py | main() | run_accuracy_simulation.py:~65 | Task 4.1 (add arg) |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Q13 Resolution | Parallel config evaluation | ParallelAccuracyRunner.py:evaluate_configs_parallel() | ProcessPoolExecutor for 8 workers |
| Q15 Resolution | Module-level evaluation function | ParallelAccuracyRunner.py:_evaluate_config_tournament_process() | Module-level for pickling |
| Q16 Resolution | Explicit worker parameters | ParallelAccuracyRunner.py:_evaluate_config_tournament_process() | (config, data_folder, seasons) |
| Q17 Resolution | Progress tracking integration | AccuracySimulationManager.py:run_both() | MultiLevelProgressTracker with callbacks |
| Q22 Resolution | Multi-level progress with ETA | AccuracySimulationManager.py:run_both() | Outer: configs, Inner: horizons, Overall: ETA |
| Q18 Resolution | CLI flag defaults | run_accuracy_simulation.py | DEFAULT_MAX_WORKERS = 8 |

---

## Data Flow Traces

### Requirement: Parallel config evaluation
```
Entry: run_both()
  → Collect all configs for parameter
  → Initialize ParallelAccuracyRunner (lazy)
  → parallel_runner.evaluate_configs_parallel(configs)
      → ProcessPoolExecutor with 8 workers
      → Submit all configs to executor
      → Each worker:
          → _evaluate_config_tournament_process(config)
              → AccuracyCalculator.calculate_ros_mae()
              → AccuracyCalculator.calculate_weekly_mae() × 4
              → Return (config, {5 results})
      → Collect results as they complete
      → Progress callback after each completion
  → Record all results
  → Result: All configs evaluated in parallel, ~8x speedup
```

### Requirement: Multi-level progress tracking
```
Entry: run_both()
  → Create MultiLevelProgressTracker(outer=105, inner=5)
  → For each config evaluation completion:
      → progress_callback(completed)
          → progress_tracker.next_outer()  # Increment config counter
  → Display: "Configs: 42/105 (40.0%) | Horizons: 3/5 (60.0%) | Overall: 40.6% | ETA: 3m 18s"
  → Result: Real-time progress visibility with ETA
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
- [ ] ParallelAccuracyRunner: Initialized and called by run_both()
- [ ] _evaluate_config_tournament_process(): Called by evaluate_configs_parallel()
- [ ] MultiLevelProgressTracker: Created in run_both()
- [ ] --max-workers / --use-processes: Passed to AccuracySimulationManager

**Every caller modified:**
- [ ] Task 2.1: run_both() creates and calls ParallelAccuracyRunner
- [ ] Task 3.1: run_both() creates MultiLevelProgressTracker
- [ ] Task 4.1: main() passes CLI flags to manager

**Status:** (To be filled)

### Check 2 (Iteration 14)
(To be filled)

### Check 3 (Iteration 23)
(To be filled)

---

## Notes

- This is Phase 3 of 5 sub-features
- Performance-critical enhancement
- ProcessPoolExecutor bypasses GIL for true parallelism
- Expected ~8x speedup with 8 workers
- Must complete all 24 verification iterations before implementing
- Dependencies: Phase 2 (Tournament Rewrite) must be complete
- Next phase: 04_cli_logging_todo.md
