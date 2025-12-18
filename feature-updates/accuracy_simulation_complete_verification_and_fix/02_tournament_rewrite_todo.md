# Accuracy Simulation - Tournament Rewrite - Implementation TODO

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
- Requirements from spec: 5 (tournament model, metadata, auto-resume, folder naming, evaluation wrapper)
- Requirements in TODO: 5
- Questions for user: 0
- Integration points identified: 3

---

## Sub-Feature Overview

**Name:** Tournament Rewrite (Phase 2 of 5)
**Priority:** Core feature - complete rewrite of run_both()
**Dependencies:** Phase 1 (Core Fixes) must be complete
**Next Phase:** 03_parallel_processing_todo.md

**What this sub-feature implements:**
1. Rewrite run_both() → run_tournament_optimization() for per-parameter tournament model (Q7, Q9)
2. Implement metadata tracking (Q28-Q30)
3. Implement auto-resume for tournament mode (Q8)
4. Implement simple folder naming with metadata.json (Q24)
5. Create _evaluate_config_tournament() wrapper method (Q9)

**Why these are grouped:**
- All core tournament optimization logic
- Foundation for parallel processing (Phase 3)
- Must work correctly before adding performance optimizations
- Natural flow: evaluation → optimization → results tracking

---

## Phase 1: Create _evaluate_config_tournament() Wrapper

### Task 1.1: Create instance method to evaluate single config across all 5 horizons

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** `_evaluate_config_tournament(config_dict: dict, horizon: str) -> Dict[str, AccuracyResult]`
- **Location:** Add after `_evaluate_config_weekly()` (after line 527)
- **Status:** [ ] Not started

**Implementation details:**
1. Read existing `_evaluate_config_ros()` (lines 374-445) and `_evaluate_config_weekly()` (lines 447-527)
2. Create new instance method that wraps both
3. Method signature:
   ```python
   def _evaluate_config_tournament(
       self,
       config_dict: dict,
       horizon: str
   ) -> Dict[str, AccuracyResult]:
       """
       Evaluate single config across all 5 horizons for tournament optimization.

       Args:
           config_dict: Configuration to evaluate
           horizon: Base horizon this config was generated from ('ros', '1-5', etc.)

       Returns:
           Dict mapping each horizon to its AccuracyResult:
           {'ros': result_ros, '1-5': result_1_5, '6-9': result_6_9, '10-13': result_10_13, '14-17': result_14_17}
       """
   ```
4. Implementation:
   ```python
   results = {}

   # Evaluate ROS horizon
   results['ros'] = self._evaluate_config_ros(config_dict)

   # Evaluate all 4 weekly horizons
   for week_horizon in ['1-5', '6-9', '10-13', '14-17']:
       results[week_horizon] = self._evaluate_config_weekly(config_dict, week_horizon)

   return results
   ```
5. This wrapper delegates to existing evaluation methods (no duplication)

**Algorithm specification:**
```python
def _evaluate_config_tournament(self, config_dict: dict, horizon: str) -> Dict[str, AccuracyResult]:
    """Evaluate config across all 5 horizons."""
    results = {}

    # ROS evaluation
    results['ros'] = self._evaluate_config_ros(config_dict)

    # Weekly evaluations
    for week_horizon in ['1-5', '6-9', '10-13', '14-17']:
        results[week_horizon] = self._evaluate_config_weekly(config_dict, week_horizon)

    return results
```

**Verification:**
- [ ] Code matches algorithm specification exactly
- [ ] Returns dict with 5 keys (all horizons)
- [ ] Each value is AccuracyResult
- [ ] Delegates to existing evaluation methods (no code duplication)
- [ ] Docstring complete and accurate

---

## Phase 2: Rewrite run_both() → run_tournament_optimization()

### Task 2.1: Replace run_both() with tournament optimization logic

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** `run_both()` (lines 774-792)
- **Current:** Sequential execution (ROS then weekly)
- **New:** Per-parameter tournament optimization
- **Status:** [ ] Not started

**Implementation details:**
1. Read current run_both() (lines 774-792) - only 19 lines, trivial to replace
2. Delete entire method body
3. Implement tournament model:

**Algorithm specification:**
```python
def run_both(self) -> None:
    """
    Run tournament optimization: each parameter optimizes across ALL 5 horizons.

    For each parameter:
    - Generate test configs from 5 baseline configs (one per horizon)
    - Evaluate each config across all 5 horizons
    - Track best config for each horizon independently
    - Save intermediate results (all 5 best configs)
    - Update baselines for next parameter
    """
    # Setup signal handlers (existing pattern)
    self._setup_signal_handlers()

    # Auto-resume detection
    resume_param_idx = self._detect_resume_state()
    if resume_param_idx is not None:
        self.logger.info(f"Resuming from parameter {resume_param_idx + 1}")
        self.results_manager.load_intermediate_results(
            self.intermediate_folder / f"accuracy_intermediate_{resume_param_idx:02d}_{self.parameter_order[resume_param_idx]}"
        )

    # Main optimization loop
    for param_idx, param_name in enumerate(self.parameter_order):
        # Skip if resuming and before resume point
        if resume_param_idx is not None and param_idx <= resume_param_idx:
            continue

        self.logger.info(f"Optimizing parameter {param_idx + 1}/{len(self.parameter_order)}: {param_name}")

        # Generate test values for all 5 horizons
        test_values_dict = self.config_generator.generate_horizon_test_values(param_name)
        # Returns: {'ros': [...], '1-5': [...], '6-9': [...], '10-13': [...], '14-17': [...]}

        # Check for empty test values (fail fast)
        for horizon, test_values in test_values_dict.items():
            if len(test_values) == 0:
                raise ValueError(f"No test values generated for parameter {param_name}, horizon {horizon}")

        # Evaluate all configs across all horizons
        config_count = sum(len(vals) for vals in test_values_dict.values())

        for horizon, test_values in test_values_dict.items():
            self.logger.info(f"  Testing {len(test_values)} values for horizon {horizon}")

            for test_idx, test_value in enumerate(test_values):
                # Get config for this horizon and test value
                config_dict = self.config_generator.get_config_for_horizon(horizon, param_name, test_idx)

                # Evaluate across all 5 horizons
                all_results = self._evaluate_config_tournament(config_dict, horizon)

                # Record results for each horizon
                for result_horizon, result in all_results.items():
                    is_new_best = self.results_manager.add_result(
                        result_horizon,
                        config_dict,
                        result,
                        config_id=f"{param_name}_{test_idx}_horizon_{result_horizon}",
                        param_name=param_name,
                        test_idx=test_idx,
                        base_horizon=horizon
                    )

                    # Log new bests (Q25 decision)
                    if is_new_best:
                        self.logger.info(f"    New best for {result_horizon}: MAE={result.mae:.4f} (test_{test_idx})")

        # After all configs tested, save intermediate results
        intermediate_folder = self.intermediate_folder / f"accuracy_intermediate_{param_idx:02d}_{param_name}"
        self.results_manager.save_intermediate_results(
            intermediate_folder,
            param_idx,
            param_name
        )

        # Update baselines for all 5 horizons
        for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
            best_config = self.results_manager.best_configs[horizon].config
            self.config_generator.update_baseline_for_horizon(horizon, best_config)

        # Log parameter summary (Q25, Q44 decisions)
        self._log_parameter_summary(param_name)

    # Save optimal configs
    self.results_manager.save_optimal_configs(self.optimal_folder)
    self.logger.info(f"Tournament optimization complete. Results saved to {self.optimal_folder}")
```

**Key behaviors:**
- Per-parameter optimization (not sequential ROS → weekly)
- Each config evaluated across all 5 horizons
- Each horizon maintains independent best config
- Save once per parameter (not per new best)
- Auto-resume from interrupted optimization
- Fail-fast on empty test values or errors

**Verification:**
- [ ] Code matches algorithm specification exactly
- [ ] Auto-resume detection works
- [ ] Signal handlers set up
- [ ] Empty test values raises ValueError
- [ ] Each config evaluated across all 5 horizons
- [ ] Results tracked per horizon independently
- [ ] New bests logged during optimization
- [ ] Intermediate saved once per parameter
- [ ] Baselines updated for all 5 horizons
- [ ] Parameter summary logged after completion

---

### Task 2.2: Create _log_parameter_summary() helper method

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** `_log_parameter_summary(param_name: str) -> None`
- **Location:** Add as private helper method after run_both()
- **Status:** [ ] Not started

**Implementation details:**
1. Log summary of parameter optimization results across all 5 horizons
2. Format from Q25 decision:
   ```
   Parameter NORMALIZATION_MAX_SCALE complete:
     ros: MAE=2.34 (test_05)
     1-5: MAE=2.41 (test_03)
     6-9: MAE=2.38 (test_05)
     10-13: MAE=2.45 (test_01)
     14-17: MAE=2.52 (test_02)
   ```

**Algorithm specification:**
```python
def _log_parameter_summary(self, param_name: str) -> None:
    """Log summary of best results for all horizons after parameter completes."""
    self.logger.info(f"Parameter {param_name} complete:")

    for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
        best = self.results_manager.best_configs[horizon]
        # Extract test_idx from config_id (format: "PARAM_idx_horizon_HORIZON")
        # Example: "NORMALIZATION_MAX_SCALE_5_horizon_ros" → test_05
        test_idx = best.config_id.split('_')[1] if '_' in best.config_id else '?'
        self.logger.info(f"  {horizon}: MAE={best.mae:.4f} (test_{test_idx})")
```

**Verification:**
- [ ] Code matches algorithm specification
- [ ] Logs all 5 horizons
- [ ] Format matches Q25 specification
- [ ] Extracts test_idx from config_id correctly
- [ ] Uses info log level (Q44 decision)

---

## Phase 3: Add Metadata Tracking

### Task 3.1: Add metadata fields to AccuracyConfigPerformance

- **File:** `simulation/accuracy/AccuracyResultsManager.py`
- **Class:** `AccuracyConfigPerformance` (lines 42-83)
- **Status:** [ ] Not started

**Implementation details:**
1. Read current AccuracyConfigPerformance (lines 42-83)
2. Add optional metadata fields to __init__:
   ```python
   param_name: Optional[str] = None
   test_idx: Optional[int] = None
   base_horizon: Optional[str] = None
   ```
3. Store as instance variables
4. Update to_dict() to include metadata

**Algorithm specification:**
```python
@dataclass
class AccuracyConfigPerformance:
    """Performance metrics for accuracy config with tournament metadata."""
    config_id: str
    config: Dict[str, Any]
    mae: float
    player_count: int
    total_error: float
    param_name: Optional[str] = None      # NEW
    test_idx: Optional[int] = None        # NEW
    base_horizon: Optional[str] = None    # NEW

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        d = {
            'config_id': self.config_id,
            'config': self.config,
            'mae': self.mae,
            'player_count': self.player_count,
            'total_error': self.total_error
        }
        # Add metadata if present
        if self.param_name is not None:
            d['param_name'] = self.param_name
        if self.test_idx is not None:
            d['test_idx'] = self.test_idx
        if self.base_horizon is not None:
            d['base_horizon'] = self.base_horizon
        return d
```

**Verification:**
- [ ] Code matches specification
- [ ] Fields optional (don't break existing code)
- [ ] to_dict() includes metadata when present
- [ ] to_dict() omits metadata when None

---

### Task 3.2: Update add_result() to accept metadata parameters

- **File:** `simulation/accuracy/AccuracyResultsManager.py`
- **Method:** `add_result()` (lines ~190-210)
- **Status:** [ ] Not started

**Implementation details:**
1. Read current add_result() signature
2. Add optional metadata parameters:
   ```python
   param_name: Optional[str] = None,
   test_idx: Optional[int] = None,
   base_horizon: Optional[str] = None
   ```
3. Pass to AccuracyConfigPerformance constructor

**Algorithm specification:**
```python
def add_result(
    self,
    horizon: str,
    config: Dict[str, Any],
    result: AccuracyResult,
    config_id: str = "",
    param_name: Optional[str] = None,     # NEW
    test_idx: Optional[int] = None,       # NEW
    base_horizon: Optional[str] = None    # NEW
) -> bool:
    """Add result and return True if new best."""
    perf = AccuracyConfigPerformance(
        config_id=config_id,
        config=config,
        mae=result.mae,
        player_count=result.player_count,
        total_error=result.total_error,
        param_name=param_name,    # NEW
        test_idx=test_idx,        # NEW
        base_horizon=base_horizon # NEW
    )

    # Rest of method unchanged...
```

**Verification:**
- [ ] Parameters optional (backward compatible)
- [ ] Passed to AccuracyConfigPerformance correctly
- [ ] Existing tests still pass

---

### Task 3.3: Add metadata.json creation to save_intermediate_results()

- **File:** `simulation/accuracy/AccuracyResultsManager.py`
- **Method:** `save_intermediate_results()` (lines 353-456)
- **Status:** [ ] Not started

**Implementation details:**
1. Read current save_intermediate_results()
2. After saving all 6 config files, create metadata.json
3. Metadata structure from Q28-Q30:
   ```json
   {
     "param_idx": 5,
     "param_name": "MATCHUP_SCORING_WEIGHT",
     "horizons_evaluated": ["ros", "1-5", "6-9", "10-13", "14-17"],
     "best_mae_per_horizon": {
       "ros": {"mae": 2.34, "test_idx": 5},
       "1-5": {"mae": 2.41, "test_idx": 3},
       "6-9": {"mae": 2.38, "test_idx": 5},
       "10-13": {"mae": 2.45, "test_idx": 1},
       "14-17": {"mae": 2.52, "test_idx": 2}
     },
     "timestamp": "2025-12-17_20:30:15"
   }
   ```

**Algorithm specification:**
```python
# At end of save_intermediate_results(), after all config files saved:

# Create metadata.json
metadata = {
    "param_idx": param_idx,
    "param_name": param_name,
    "horizons_evaluated": ["ros", "1-5", "6-9", "10-13", "14-17"],
    "best_mae_per_horizon": {},
    "timestamp": datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
}

for horizon in ["ros", "1-5", "6-9", "10-13", "14-17"]:
    best = self.best_configs[horizon]
    metadata["best_mae_per_horizon"][horizon] = {
        "mae": best.mae,
        "test_idx": best.test_idx if best.test_idx is not None else -1
    }

metadata_path = intermediate_folder / "metadata.json"
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)

self.logger.info(f"Saved metadata to {metadata_path}")
```

**Verification:**
- [ ] Code matches specification
- [ ] metadata.json created in intermediate folder
- [ ] All 5 horizons included
- [ ] Timestamp present
- [ ] test_idx handled if None

---

## Phase 4: Implement Auto-Resume for Tournament Mode

### Task 4.1: Verify _detect_resume_state() works for tournament folders

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** `_detect_resume_state()` (lines 176-280)
- **Status:** [ ] Not started

**Implementation details:**
1. Read current _detect_resume_state() implementation
2. Verify regex pattern matches tournament folder naming: `accuracy_intermediate_{idx:02d}_{param_name}`
3. Pattern already supports this format
4. NO CHANGES NEEDED (just verification)

**Expected folder format:**
- `accuracy_intermediate_00_NORMALIZATION_MAX_SCALE`
- `accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT`
- `accuracy_intermediate_05_MATCHUP_SCORING_WEIGHT`

**Verification:**
- [ ] Read _detect_resume_state() code
- [ ] Confirm regex pattern: `r'accuracy_intermediate_(\d+)_'`
- [ ] Confirm pattern matches tournament folder naming
- [ ] Confirm highest index detection works
- [ ] NO CODE CHANGES NEEDED

---

### Task 4.2: Verify load_intermediate_results() loads all 5 horizons

- **File:** `simulation/accuracy/AccuracyResultsManager.py`
- **Method:** `load_intermediate_results()` (lines ~300-350)
- **Status:** [ ] Not started

**Implementation details:**
1. Read current load_intermediate_results()
2. Verify it loads all 6 config files (league_config + 5 horizons)
3. Verify it restores best_configs for all 5 horizons
4. Expected to already work correctly (from verification in checklist)
5. NO CHANGES NEEDED (just verification)

**Verification:**
- [ ] Read load_intermediate_results() code
- [ ] Confirm loads draft_config.json (ros)
- [ ] Confirm loads week1-5.json, week6-9.json, week10-13.json, week14-17.json
- [ ] Confirm restores best_configs dict with 5 entries
- [ ] NO CODE CHANGES NEEDED

---

## Phase 5: Update CLI to Remove Mode Argument

### Task 5.1: Remove mode positional argument from run_accuracy_simulation.py

- **File:** `run_accuracy_simulation.py`
- **Lines:** CLI argument parsing section
- **Status:** [ ] Not started

**Implementation details:**
1. Read current argparse configuration
2. Remove mode positional argument (was: 'ros', 'weekly', 'both')
3. Update help text to indicate tournament mode only
4. Remove mode branching logic in main()
5. Call manager.run_both() unconditionally (tournament mode)

**Changes:**
```python
# BEFORE:
parser.add_argument('mode', choices=['ros', 'weekly', 'both'], help='Optimization mode')

if args.mode == 'ros':
    manager.run_ros_optimization()
elif args.mode == 'weekly':
    manager.run_weekly_optimization()
elif args.mode == 'both':
    manager.run_both()

# AFTER:
# (no mode argument)

# Main execution
manager.run_both()  # Tournament optimization (only mode)
```

**Verification:**
- [ ] Mode argument removed from argparse
- [ ] Help text updated
- [ ] No mode branching in main()
- [ ] Always calls run_both() (tournament mode)
- [ ] --help shows correct usage

---

### QA CHECKPOINT 2: Tournament Rewrite Validation

- **Status:** [ ] Not started
- **Expected outcome:** Tournament optimization works correctly
- **Test command:** `python run_accuracy_simulation.py --test-values 2 --num-params 2`
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] CLI accepts no mode argument
  - [ ] Tournament optimization starts
  - [ ] Each config evaluated across all 5 horizons
  - [ ] Results tracked independently per horizon
  - [ ] New bests logged during optimization
  - [ ] Parameter summary logged after completion
  - [ ] Intermediate folder created after parameter 1
  - [ ] metadata.json present in intermediate folder
  - [ ] All 6 config files saved
  - [ ] Parameter 2 uses parameter 1's best configs as baselines
  - [ ] Auto-resume works if interrupted
  - [ ] No errors in output

**If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (Verified Pre-Implementation)

### _evaluate_config_tournament()
- **Method:** `_evaluate_config_tournament(config_dict: dict, horizon: str) -> Dict[str, AccuracyResult]`
- **Source:** `simulation/accuracy/AccuracySimulationManager.py` (NEW)
- **Returns:** Dict with 5 keys (all horizons), each value is AccuracyResult
- **Verified:** [ ]

### run_both()
- **Method:** `run_both() -> None`
- **Source:** `simulation/accuracy/AccuracySimulationManager.py:774-792`
- **Current:** Sequential (ROS → weekly)
- **New:** Per-parameter tournament optimization
- **Verified:** [ ]

### AccuracyConfigPerformance
- **Class:** Modified to include metadata fields
- **Source:** `simulation/accuracy/AccuracyResultsManager.py:42-83`
- **New fields:** param_name, test_idx, base_horizon (all optional)
- **Verified:** [ ]

### add_result()
- **Method:** Modified to accept metadata parameters
- **Source:** `simulation/accuracy/AccuracyResultsManager.py:~190-210`
- **New params:** param_name, test_idx, base_horizon (all optional)
- **Verified:** [ ]

### save_intermediate_results()
- **Method:** Modified to create metadata.json
- **Source:** `simulation/accuracy/AccuracyResultsManager.py:353-456`
- **New file:** metadata.json in intermediate folder
- **Verified:** [ ]

### Quick E2E Validation Plan
- **Minimal test command:**
  ```bash
  python run_accuracy_simulation.py --test-values 2 --num-params 1
  ```
- **Expected result:**
  - Tournament optimization runs
  - 105 configs tested (5 horizons × 21 configs)
  - 525 MAE calculations (105 configs × 5 horizons)
  - Intermediate folder created
  - metadata.json present
  - All 6 config files saved
- **Run before:** Full implementation begins
- **Status:** [ ] Not run | [ ] Passed | [ ] Failed (fix before proceeding)

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| _evaluate_config_tournament() | AccuracySimulationManager.py | run_both() | AccuracySimulationManager.py:~800 | Task 2.1 (new caller) |
| run_both() rewrite | AccuracySimulationManager.py | main() | run_accuracy_simulation.py:~100 | Task 5.1 (update CLI) |
| _log_parameter_summary() | AccuracySimulationManager.py | run_both() | AccuracySimulationManager.py:~850 | Task 2.1 (new caller) |
| metadata fields | AccuracyResultsManager.py | add_result() | AccuracySimulationManager.py:~820 | Task 2.1 (pass metadata) |
| metadata.json | AccuracyResultsManager.py | save_intermediate_results() | AccuracySimulationManager.py:~840 | Task 3.3 (create file) |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Q7 Resolution | Per-parameter tournament optimization | AccuracySimulationManager.py:run_both() | for param in parameter_order: evaluate all configs |
| Q9 Resolution | Instance method wrapper for evaluation | AccuracySimulationManager.py:_evaluate_config_tournament() | Call ros + 4 weekly methods |
| Q8 Resolution | Auto-resume for tournament | AccuracySimulationManager.py:run_both() | if resume_param_idx: skip completed params |
| Q24 Resolution | Simple folder naming | AccuracySimulationManager.py:run_both() | f"accuracy_intermediate_{idx:02d}_{param}" |
| Q28-Q30 Resolution | Metadata tracking | AccuracyResultsManager.py:save_intermediate_results() | Create metadata.json with param info |
| Q25 Resolution | Logging strategy | AccuracySimulationManager.py:run_both() + _log_parameter_summary() | Log new bests + parameter summary |

---

## Data Flow Traces

### Requirement: Per-parameter tournament optimization
```
Entry: run_both()
  → for param_name in parameter_order:
      → generate_horizon_test_values(param_name)  # Returns 5 arrays
      → for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
          → for test_idx in test_values[horizon]:
              → get_config_for_horizon(horizon, param_name, test_idx)
              → _evaluate_config_tournament(config, horizon)  ← Evaluates across all 5
                  → _evaluate_config_ros(config)
                  → _evaluate_config_weekly(config, '1-5')
                  → _evaluate_config_weekly(config, '6-9')
                  → _evaluate_config_weekly(config, '10-13')
                  → _evaluate_config_weekly(config, '14-17')
              → add_result() for each of 5 horizons
      → save_intermediate_results()  ← Once per parameter
      → update_baseline_for_horizon() for all 5 horizons
  → Result: Each parameter optimizes all 5 horizons before moving to next
```

### Requirement: Metadata tracking
```
Entry: run_both() calls save_intermediate_results()
  → save_intermediate_results(folder, param_idx, param_name)
      → Save all 6 config files
      → Create metadata dict with:
          - param_idx, param_name
          - best_mae_per_horizon (5 horizons)
          - timestamp
      → Write metadata.json
  → Result: metadata.json in each intermediate folder
```

### Requirement: Auto-resume
```
Entry: run_both()
  → resume_param_idx = _detect_resume_state()
      → Find highest intermediate folder index
      → Extract parameter index from folder name
  → if resume_param_idx is not None:
      → load_intermediate_results(folder)
          → Load all 6 config files
          → Restore best_configs for all 5 horizons
      → Skip completed parameters in loop
  → Result: Resume from last completed parameter
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
- [ ] _evaluate_config_tournament(): Called by run_both()
- [ ] run_both() rewrite: Called by main() in run_accuracy_simulation.py
- [ ] _log_parameter_summary(): Called by run_both()
- [ ] metadata fields: Used by add_result() and save_intermediate_results()

**Every caller modified:**
- [ ] Task 2.1: run_both() calls _evaluate_config_tournament()
- [ ] Task 2.1: run_both() calls _log_parameter_summary()
- [ ] Task 2.1: run_both() passes metadata to add_result()
- [ ] Task 5.1: main() calls run_both() unconditionally

**Status:** (To be filled)

### Check 2 (Iteration 14)
(To be filled)

### Check 3 (Iteration 23)
(To be filled)

---

## Notes

- This is Phase 2 of 5 sub-features
- Core tournament optimization logic
- Foundation for parallel processing (Phase 3)
- Must complete all 24 verification iterations before implementing
- Dependencies: Phase 1 (Core Fixes) must be complete
- Next phase: 03_parallel_processing_todo.md
