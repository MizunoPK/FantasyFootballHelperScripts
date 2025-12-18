# Fix 'both' Mode Behavior

## Objective

Change the accuracy simulation's 'both' mode from sequentially optimizing ROS then weekly parameters to simultaneously evaluating each config across all 5 time horizons (ROS + 4 weekly ranges), enabling parameter optimization that works well across all forecasting periods.

---

## High-Level Requirements

### 1. Core Behavior Change

**Current Behavior (Incorrect):**
- Run `run_ros_optimization()` completely (test all configs for ROS accuracy only)
- Then run `run_weekly_optimization()` completely (test all configs for weekly accuracy)
- Sequential approach: optimize one time horizon at a time

**New Behavior (Correct):**
- For each config:
  - Calculate ROS accuracy
  - Calculate week1-5 accuracy
  - Calculate week6-9 accuracy
  - Calculate week10-13 accuracy
  - Calculate week14-17 accuracy
  - Track which configs are best for each time horizon
- Per-config approach: test all time horizons before moving to next config

### 2. Iterative Base Config Behavior

Each parameter optimization uses 5 different base configs (tournament model):

**Parameter 1 (First):**
- Start from single baseline config for all 5 time horizons
- Test all configs, find best for each horizon
- Output: 6 files (draft_config.json, league_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json)

**Parameter 2+ (Subsequent):**
- Generate test configs from 5 different bases:
  1. draft_config.json (best for ROS from param 1) + new param value
  2. week1-5.json (best for week1-5 from param 1) + new param value
  3. week6-9.json (best for week6-9 from param 1) + new param value
  4. week10-13.json (best for week10-13 from param 1) + new param value
  5. week14-17.json (best for week14-17 from param 1) + new param value
- Each config evaluated across all 5 time horizons
- Track best config for each horizon independently

**"Tournament" Concept:** Each horizon's champion from parameter N competes to stay champion when parameter N+1 changes.

### 3. Parallel Processing

**Requirements:**
- Add `max_workers` parameter (default: 8)
- Add `use_processes` parameter (default: True)
- Use ProcessPoolExecutor when use_processes=True (bypasses GIL)
- Use ThreadPoolExecutor when use_processes=False (GIL-limited)
- Parallelize config evaluation
- Process results sequentially (add_result calls must be sequential)

**CLI Flags:**
- `--max-workers N` (default: 8)
- `--use-processes` / `--no-use-processes` (default: enabled)

### 4. Output Behavior

After testing all configs for a parameter, create intermediate/optimal folder with 6 files:
- `draft_config.json`: Config with best ROS accuracy (prediction params only)
- `league_config.json`: Config with best ROS accuracy (base params)
- `week1-5.json`: Config with best week1-5 accuracy
- `week6-9.json`: Config with best week6-9 accuracy
- `week10-13.json`: Config with best week10-13 accuracy
- `week14-17.json`: Config with best week14-17 accuracy

These 6 files may contain different parameter values (different configs won for different horizons).

---

## Technical Implementation

### Files to Modify

1. **simulation/accuracy/AccuracySimulationManager.py**
   - `__init__()`: Add max_workers, use_processes parameters
   - `run_both()`: Complete rewrite (see below)
   - New method: `_evaluate_config_both()`

2. **run_accuracy_simulation.py**
   - Add `--max-workers` CLI argument (default: 8)
   - Add `--use-processes` / `--no-use-processes` CLI arguments
   - Pass parameters to AccuracySimulationManager

### New Method: _evaluate_config_both()

```python
def _evaluate_config_both(self, config_dict: Dict[str, Any]) -> Dict[str, AccuracyConfigPerformance]:
    """
    Evaluate a single config across all 5 time horizons.

    Returns dict with keys: 'ros', 'week_1_5', 'week_6_9', 'week_10_13', 'week_14_17'
    """
    results = {}

    # Calculate ROS accuracy
    results['ros'] = self._evaluate_config_ros(config_dict)

    # Calculate weekly accuracies
    for week_range in WEEK_RANGES:  # ['week_1_5', 'week_6_9', 'week_10_13', 'week_14_17']
        results[week_range] = self._evaluate_config_weekly(config_dict, week_range)

    return results
```

### Rewritten run_both() Method

**Pseudocode:**
```python
def run_both(self) -> Path:
    # Initialize with ConfigGenerator's new interface
    # ConfigGenerator now stores 5 separate baseline configs + league_config
    config_generator = ConfigGenerator(
        baseline_config_path=self.baseline_config_path,
        parameter_order=self.parameter_order
    )

    for param_name in self.parameter_order:
        # ConfigGenerator generates test configs per horizon
        # Returns list of (horizon, test_idx, config_dict) tuples
        configs_to_test = []

        for horizon in HORIZONS:  # ['ros', '1-5', '6-9', '10-13', '14-17']
            test_values = config_generator.generate_horizon_test_values(
                param_name,
                horizon,
                num_values=self.num_test_values
            )

            for test_idx, test_value in enumerate(test_values):
                config_dict = config_generator.get_config_for_horizon(
                    param_name,
                    horizon,
                    test_idx
                )
                configs_to_test.append((horizon, test_idx, config_dict))

        # Parallel evaluation
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._evaluate_config_both, cfg): (horizon, test_idx)
                for horizon, test_idx, cfg in configs_to_test
            }

            for future in as_completed(futures):
                horizon, test_idx = futures[future]
                all_results = future.result()  # Dict with 5 results

                # Record all 5 results
                for result_horizon, perf in all_results.items():
                    self.results_manager.add_result(result_horizon, perf)

        # Save intermediate results (6 files with current bests)
        self.results_manager.save_intermediate_results(param_name)

        # Update baseline for next parameter
        config_generator.update_baseline_for_horizon(param_name, best_configs)

    # Save final optimal configs
    return self.results_manager.save_optimal_configs()
```

---

## Open Questions

*(To be populated during Phase 2 investigation)*

---

## Resolved Implementation Details

*(To be populated as checklist items are resolved)*

---

## Dependency Map

*(To be created during Phase 2.6)*

---

## Assumptions

### CRITICAL: Week-Specific Parameters (2025-12-17)

**Assumption:** Accuracy simulation optimizes WEEK_SPECIFIC_PARAMS, not BASE_CONFIG_PARAMS.

**Evidence:**
- run_accuracy_simulation.py PARAMETER_ORDER (lines 71-88): All 16 params are week-specific
- ResultsManager.WEEK_SPECIFIC_PARAMS includes all accuracy params
- ConfigGenerator returns per-horizon test values: `{'ros': [...], '1-5': [...], ...}`
- NOT `{'shared': [...]}`

**Implementation Impact:**
- Each parameter generates 5 sets of test configs (one per horizon's baseline)
- Total configs per parameter = 5 × (num_test_values + 1)
- Example with 3 test values: 5 × 4 = 20 configs (not 4)
- Each config still evaluated across all 5 horizons
- Tournament model: Each horizon maintains independent optimal config

**Win-rate simulation (for comparison):**
- Optimizes BASE_CONFIG_PARAMS (shared across all horizons)
- Generates 1 set of test configs per parameter
- Updates all 5 horizons simultaneously with same value
- Total configs per parameter = num_test_values + 1

*(Other assumptions to be populated during Phase 2.9 Assumptions Audit)*
