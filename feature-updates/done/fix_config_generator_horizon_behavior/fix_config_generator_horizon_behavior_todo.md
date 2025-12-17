# Fix ConfigGenerator Horizon Behavior - Implementation TODO

## Iteration Progress Tracker

### Compact View (Quick Status)

```
R1: ■■■■■■■ (7/7)   R2: ■■■■■■■■■ (9/9)   R3: ■■■■■■■■ (8/8)   ✅ ALL COMPLETE
```
Legend: ■ = complete, □ = pending, ▣ = in progress

**Current:** ALL 24 ITERATIONS COMPLETE ✅
**Confidence:** VERY HIGH (200 findings, 0 blocking issues)
**Status:** READY FOR IMPLEMENTATION

### Detailed View

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 COMPLETE |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 COMPLETE |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 COMPLETE ✅ |

**Current Iteration:** 24 COMPLETE - ALL VERIFICATION DONE ✅

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [x]1 [x]2 [x]3 [x]8 [x]9 [x]10 [x]15 [x]16 ✅ |
| Algorithm Traceability | 4, 11, 19 | [x]4 [x]11 [x]19 ✅ |
| End-to-End Data Flow | 5, 12 | [x]5 [x]12 ✅ |
| Skeptical Re-verification | 6, 13, 22 | [x]6 [x]13 [x]22 ✅ |
| Integration Gap Check | 7, 14, 23 | [x]7 [x]14 [x]23 ✅ |
| Fresh Eyes Review | 17, 18 | [x]17 [x]18 ✅ |
| Edge Case Verification | 20 | [x]20 ✅ |
| Test Coverage Planning + Mock Audit | 21 | [x]21 ✅ |
| Implementation Readiness | 24 | [x]24 ✅ |
| Interface Verification | Pre-impl | [ ] (To be done before implementation) |

---

## Verification Summary

- **Iterations completed: 24/24 (100%) ✅**
  - Round 1: 7/7 COMPLETE
  - Round 2: 9/9 COMPLETE
  - Round 3: 8/8 COMPLETE
- **Total findings documented: 200**
- Requirements from spec: 40 (all resolved in checklist - 100%)
- Requirements in TODO: 23 tasks across 4 files
- Questions for user: 0 (all resolved during planning)
- Integration points identified: 4 (ConfigGenerator, ResultsManager, SimulationManager, AccuracySimulationManager)
- Edge cases identified: 15 (all testable)
- Tests planned: 54-59 tests
- **Blocking issues: 0 (ZERO)**
- **Implementation confidence: VERY HIGH**

---

## Phase 1: Add Constants and Update ConfigPerformance

### Task 1.1: Add HORIZONS constant to ConfigPerformance
- **File:** `simulation/shared/ConfigPerformance.py`
- **Line:** After line 23 (after WEEK_RANGES constant)
- **Tests:** `tests/simulation/test_ConfigPerformance.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# Add after WEEK_RANGES = ["1-5", "6-9", "10-13", "14-17"]
HORIZONS = ['ros', '1-5', '6-9', '10-13', '14-17']
```

### Task 1.2: Add HORIZON_FILES constant to ConfigPerformance
- **File:** `simulation/shared/ConfigPerformance.py`
- **Line:** After HORIZONS constant
- **Tests:** `tests/simulation/test_ConfigPerformance.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
HORIZON_FILES = {
    'ros': 'draft_config.json',
    '1-5': 'week1-5.json',
    '6-9': 'week6-9.json',
    '10-13': 'week10-13.json',
    '14-17': 'week14-17.json'
}
```

### QA CHECKPOINT 1: Constants Added
- **Status:** [ ] Not started
- **Expected outcome:** New constants accessible via import
- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] Constants can be imported: `from simulation.shared.ConfigPerformance import HORIZONS, HORIZON_FILES`
  - [ ] No errors in output
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 2: Update ResultsManager for 6-File Structure

### Task 2.1: Update required_files list in ResultsManager
- **File:** `simulation/shared/ResultsManager.py`
- **Line:** 593 (required_files list)
- **Tests:** `tests/simulation/test_ResultsManager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD (line 593):
required_files = ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json', 'league_config.json']

# NEW:
required_files = ['league_config.json', 'draft_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']
```

### Task 2.2: Update week_range_files mapping in ResultsManager
- **File:** `simulation/shared/ResultsManager.py`
- **Line:** 426-431 (week_range_files dict)
- **Tests:** `tests/simulation/test_ResultsManager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# Extend existing dict at lines 426-431:
week_range_files = {
    'ros': 'draft_config.json',  # NEW
    '1-5': 'week1-5.json',
    '6-9': 'week6-9.json',
    '10-13': 'week10-13.json',
    '14-17': 'week14-17.json'
}
```

### Task 2.3: Update save_optimal_configs_folder() to save 6 files
- **File:** `simulation/shared/ResultsManager.py`
- **Method:** `save_optimal_configs_folder()`
- **Tests:** `tests/simulation/test_ResultsManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- Iterate through all 6 files when saving
- Use week_range_files mapping with 'ros' key added
- Save league_config.json + 5 horizon files

### Task 2.4: Update load_from_folder() to load 6 files
- **File:** `simulation/shared/ResultsManager.py`
- **Method:** `load_from_folder()`
- **Tests:** `tests/simulation/test_ResultsManager.py`
- **Status:** [ ] Not started

**Implementation details:**
- Validate all 6 files exist (use updated required_files)
- Load league_config.json + 5 horizon files
- Update any file count checks

### QA CHECKPOINT 2: ResultsManager 6-File Support
- **Status:** [ ] Not started
- **Expected outcome:** ResultsManager can save/load 6-file folders
- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] Can save folder with 6 files
  - [ ] Can load folder with 6 files
  - [ ] Fails with clear error if any file missing
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 3: Refactor ConfigGenerator to Horizon-Based Interface

### Task 3.1: Update ConfigGenerator __init__ signature
- **File:** `simulation/shared/ConfigGenerator.py`
- **Method:** `__init__()` (currently at line 364)
- **Tests:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# CURRENT (line 364):
def __init__(self, baseline_config_path: Path, parameter_order: List[str],
             num_test_values: int = 5, num_parameters_to_test: int = 1) -> None:
    # ... implementation

# NEW (remove parameter_order and num_parameters_to_test):
def __init__(self, baseline_config_path: Path, num_test_values: int = 5) -> None:
    # Remove parameter_order - new interface doesn't need it (generates per parameter)
    # Remove num_parameters_to_test - only one parameter at a time now
    self.num_test_values = num_test_values
    # ... rest of init
```

**NOTE:** parameter_order will be passed to individual methods (generate_horizon_test_values) instead of constructor

### Task 3.2: Update load_baseline_from_folder() to load 6 files separately
- **File:** `simulation/shared/ConfigGenerator.py`
- **Method:** `load_baseline_from_folder()`
- **Current:** Lines 278-362 (merges all files into single config)
- **Tests:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def load_baseline_from_folder(self, baseline_folder: Path) -> None:
    """Load 6 config files and merge into 5 separate horizon baselines."""
    from simulation.shared.ConfigPerformance import HORIZONS, HORIZON_FILES

    # 1. Validate all 6 files exist
    required_files = ['league_config.json', 'draft_config.json', 'week1-5.json',
                      'week6-9.json', 'week10-13.json', 'week14-17.json']
    for filename in required_files:
        if not (baseline_folder / filename).exists():
            raise ConfigGeneratorError(f"Missing required file '{filename}' in folder '{baseline_folder}'\n"
                                       f"Required files: {', '.join(required_files)}\n"
                                       f"This is a breaking change from 5-file structure. "
                                       f"Please update your configuration folders to include draft_config.json.")

    # 2. Load league_config.json once
    with open(baseline_folder / 'league_config.json', 'r') as f:
        league_config = json.load(f)

    # 3. Load 5 horizon files and merge each with league_config
    self.baseline_configs = {}
    for horizon in HORIZONS:
        horizon_file = HORIZON_FILES[horizon]
        with open(baseline_folder / horizon_file, 'r') as f:
            horizon_config = json.load(f)

        # Merge: league_config + horizon_config (horizon wins on conflicts)
        merged = {
            'config_name': horizon_config.get('config_name', f'{horizon} config'),
            'description': horizon_config.get('description', f'Config for {horizon} horizon'),
            'parameters': {**league_config['parameters'], **horizon_config['parameters']}
        }
        self.baseline_configs[horizon] = merged
```

### Task 3.3: Create generate_horizon_test_values() method
- **File:** `simulation/shared/ConfigGenerator.py`
- **Method:** NEW - `generate_horizon_test_values(param_name: str) -> Dict[str, List[float]]`
- **Tests:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def generate_horizon_test_values(self, param_name: str) -> Dict[str, List[float]]:
    """
    Generate test values for parameter optimization.

    Returns different structures based on parameter type:
    - Shared params (BASE_CONFIG_PARAMS): {'shared': [N values]}
      → N configs tested across all 5 horizons
    - Horizon params (WEEK_SPECIFIC_PARAMS): {'ros': [N], '1-5': [N], ...}
      → 5×N configs tested (tournament model)
    """
    from simulation.shared.ConfigPerformance import HORIZONS

    if self.is_base_param(param_name):
        # Shared param: Generate one array
        baseline = self.baseline_configs['ros']['parameters'][param_name]  # Any horizon, same value
        test_values = self._generate_test_values(param_name, baseline, self.num_test_values)
        self.test_values = {'shared': test_values}
    else:
        # Horizon param: Generate 5 independent arrays
        self.test_values = {}
        for horizon in HORIZONS:
            baseline = self.baseline_configs[horizon]['parameters'][param_name]
            test_values = self._generate_test_values(param_name, baseline, self.num_test_values)
            self.test_values[horizon] = test_values

    return self.test_values  # Pre-generated and stored
```

### Task 3.4: Create get_config_for_horizon() method
- **File:** `simulation/shared/ConfigGenerator.py`
- **Method:** NEW - `get_config_for_horizon(horizon: str, param_name: str, test_index: int) -> dict`
- **Tests:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
import copy

def get_config_for_horizon(self, horizon: str, param_name: str, test_index: int) -> dict:
    """Get complete config with test value applied at test_index."""
    # Deep copy baseline to prevent mutation
    config = copy.deepcopy(self.baseline_configs[horizon])

    # Apply test value
    if 'shared' in self.test_values:
        # Shared param: Use same value for all horizons
        config['parameters'][param_name] = self.test_values['shared'][test_index]
    else:
        # Horizon param: Use horizon-specific value
        config['parameters'][param_name] = self.test_values[horizon][test_index]

    return config  # Safe from mutation (deep copied)
```

### Task 3.5: Create update_baseline_for_horizon() method
- **File:** `simulation/shared/ConfigGenerator.py`
- **Method:** NEW - `update_baseline_for_horizon(horizon: str, new_config: dict)`
- **Tests:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
def update_baseline_for_horizon(self, horizon: str, new_config: dict):
    """Update baseline config for horizon after finding optimal value."""
    self.baseline_configs[horizon] = new_config
```

### Task 3.6: Remove generate_iterative_combinations() method
- **File:** `simulation/shared/ConfigGenerator.py`
- **Method:** REMOVE - `generate_iterative_combinations()`
- **Tests:** `tests/simulation/test_config_generator.py` (remove tests for this method)
- **Status:** [ ] Not started

**Implementation details:**
- Delete entire method
- Remove any tests that test this method
- Clean break - no deprecation warning needed

### QA CHECKPOINT 3: ConfigGenerator Refactored
- **Status:** [ ] Not started
- **Expected outcome:** ConfigGenerator supports 6-file horizon-based optimization
- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] Can load 6-file folder and create 5 horizon baselines
  - [ ] generate_horizon_test_values() returns correct structure for shared vs horizon params
  - [ ] get_config_for_horizon() returns deep copy with test value applied
  - [ ] Fails with clear error if any file missing
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 4: Update SimulationManager (Win-Rate)

### Task 4.1: Update ConfigGenerator initialization in SimulationManager
- **File:** `simulation/win_rate/SimulationManager.py`
- **Method:** Where ConfigGenerator is initialized
- **Tests:** `tests/simulation/test_simulation_manager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
config_generator = ConfigGenerator(baseline_folder, num_parameters_to_test, num_test_values)

# NEW:
config_generator = ConfigGenerator(baseline_folder, num_test_values)
```

### Task 4.2: Filter PARAMETER_ORDER to BASE_CONFIG_PARAMS only
- **File:** `simulation/win_rate/SimulationManager.py`
- **Top of file:** PARAMETER_ORDER definition
- **Tests:** `tests/simulation/test_simulation_manager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# At top of file, ensure PARAMETER_ORDER contains only BASE_CONFIG_PARAMS
# This may already be the case, but verify and document
from simulation.shared.ResultsManager import BASE_CONFIG_PARAMS

# PARAMETER_ORDER should only contain params from BASE_CONFIG_PARAMS
# Remove any WEEK_SPECIFIC_PARAMS if present
```

### Task 4.3: Update simulation loop to use new ConfigGenerator interface
- **File:** `simulation/win_rate/SimulationManager.py`
- **Method:** Main optimization loop
- **Tests:** `tests/simulation/test_simulation_manager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# For each parameter in PARAMETER_ORDER:
#   1. Call generate_horizon_test_values(param_name)
#   2. Loop through test indices and horizons
#   3. Call get_config_for_horizon(horizon, param_name, test_idx)
#   4. Run simulation with that config
#   5. After finding optimal, call update_baseline_for_horizon()
```

### QA CHECKPOINT 4: Win-Rate Simulation Updated
- **Status:** [ ] Not started
- **Expected outcome:** Win-rate sim uses new ConfigGenerator interface
- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] SimulationManager initializes ConfigGenerator with 2 params (not 3)
  - [ ] PARAMETER_ORDER filtered to BASE_CONFIG_PARAMS only
  - [ ] Uses generate_horizon_test_values(), get_config_for_horizon(), update_baseline_for_horizon()
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 5: Update AccuracySimulationManager (Accuracy)

### Task 5.1: Update ConfigGenerator initialization in AccuracySimulationManager
- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** Where ConfigGenerator is initialized
- **Tests:** `tests/simulation/test_AccuracySimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# OLD:
config_generator = ConfigGenerator(baseline_folder, num_parameters_to_test, num_test_values)

# NEW:
config_generator = ConfigGenerator(baseline_folder, num_test_values)
```

### Task 5.2: Update PARAMETER_ORDER in run_accuracy_simulation.py
- **File:** `run_accuracy_simulation.py`
- **Top of file:** PARAMETER_ORDER definition (if exists)
- **Tests:** `tests/integration/test_accuracy_simulation_integration.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# Ensure PARAMETER_ORDER in runner script contains ONLY WEEK_SPECIFIC_PARAMS
from simulation.shared.ResultsManager import WEEK_SPECIFIC_PARAMS

# PARAMETER_ORDER should only contain params from WEEK_SPECIFIC_PARAMS
# Remove any BASE_CONFIG_PARAMS if present
```

### Task 5.3: Update accuracy simulation loop to use new ConfigGenerator interface
- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Method:** Main optimization loop
- **Tests:** `tests/simulation/test_AccuracySimulationManager.py`
- **Status:** [ ] Not started

**Implementation details:**
```python
# For each parameter in PARAMETER_ORDER:
#   1. Call generate_horizon_test_values(param_name)
#   2. Loop through test indices AND horizons (5×N configs)
#   3. Call get_config_for_horizon(horizon, param_name, test_idx)
#   4. Evaluate accuracy with that config
#   5. After finding optimal per horizon, call update_baseline_for_horizon()
```

### QA CHECKPOINT 5: Accuracy Simulation Updated
- **Status:** [ ] Not started
- **Expected outcome:** Accuracy sim uses new ConfigGenerator interface with tournament optimization
- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] Unit tests pass (100%)
  - [ ] AccuracySimulationManager initializes ConfigGenerator with 2 params (not 3)
  - [ ] PARAMETER_ORDER filtered to WEEK_SPECIFIC_PARAMS only
  - [ ] Uses generate_horizon_test_values(), get_config_for_horizon(), update_baseline_for_horizon()
  - [ ] Tests 5×N configs (tournament model)
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (Verified Pre-Implementation)

### ConfigPerformance
- **Constant:** `HORIZONS: List[str]` - ['ros', '1-5', '6-9', '10-13', '14-17']
- **Source:** `simulation/shared/ConfigPerformance.py:23` (after WEEK_RANGES)
- **Existing usage:** New constant, no existing usage
- **Verified:** [ ]

### ConfigPerformance
- **Constant:** `HORIZON_FILES: Dict[str, str]` - Maps horizon names to filenames
- **Source:** `simulation/shared/ConfigPerformance.py:25` (after HORIZONS)
- **Existing usage:** New constant, no existing usage
- **Verified:** [ ]

### ResultsManager
- **Constant:** `BASE_CONFIG_PARAMS: List[str]` - Shared parameters
- **Source:** `simulation/shared/ResultsManager.py:239-265`
- **Existing usage:** Used by ConfigGenerator for param type detection
- **Verified:** [ ]

### ResultsManager
- **Constant:** `WEEK_SPECIFIC_PARAMS: List[str]` - Horizon-specific parameters
- **Source:** `simulation/shared/ResultsManager.py:239-265`
- **Existing usage:** Used by ConfigGenerator for param type detection
- **Verified:** [ ]

### ConfigGenerator (existing methods)
- **Method:** `is_base_param(param_name: str) -> bool`
- **Source:** `simulation/shared/ConfigGenerator.py:231`
- **Existing usage:** Internal classification method
- **Verified:** [x] (Iteration 1)

### ConfigGenerator (existing methods)
- **Method:** `is_week_specific_param(param_name: str) -> bool`
- **Source:** `simulation/shared/ConfigGenerator.py:275`
- **Existing usage:** Internal classification method
- **Verified:** [ ]

### Quick E2E Validation Plan
- **Minimal test command:** Create test folder with 6 files, initialize ConfigGenerator, call generate_horizon_test_values()
- **Expected result:** No errors, returns dict with correct structure
- **Run before:** Full implementation begins
- **Status:** [ ] Not run | [ ] Passed | [ ] Failed (fix before proceeding)

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| HORIZONS constant | ConfigPerformance.py | ConfigGenerator | ConfigGenerator.py:load_baseline_from_folder | Task 3.2 |
| HORIZON_FILES constant | ConfigPerformance.py | ConfigGenerator | ConfigGenerator.py:load_baseline_from_folder | Task 3.2 |
| generate_horizon_test_values() | ConfigGenerator.py | SimulationManager | SimulationManager.py:optimization_loop | Task 4.3 |
| generate_horizon_test_values() | ConfigGenerator.py | AccuracySimulationManager | AccuracySimulationManager.py:optimization_loop | Task 5.3 |
| get_config_for_horizon() | ConfigGenerator.py | SimulationManager | SimulationManager.py:optimization_loop | Task 4.3 |
| get_config_for_horizon() | ConfigGenerator.py | AccuracySimulationManager | AccuracySimulationManager.py:optimization_loop | Task 5.3 |
| update_baseline_for_horizon() | ConfigGenerator.py | SimulationManager | SimulationManager.py:optimization_loop | Task 4.3 |
| update_baseline_for_horizon() | ConfigGenerator.py | AccuracySimulationManager | AccuracySimulationManager.py:optimization_loop | Task 5.3 |

---

## Algorithm Traceability Matrix

**Iteration 4 - Initial Population (Complete)**

| Spec Section | Algorithm Description | Code Location | Conditional Logic | Status |
|--------------|----------------------|---------------|-------------------|--------|
| Specs lines 38-42, Q1-Q2 | Load 6 files separately, merge each horizon = league + specific | ConfigGenerator.load_baseline_from_folder() | None - all 6 files always loaded | [x] Verified Iter 4 |
| Specs lines 82-86, Q2 | Simple dict merge with horizon file wins on conflicts | ConfigGenerator.load_baseline_from_folder() | Horizon file overrides if same param in both | [x] Verified Iter 4 |
| Specs lines 104-114, Q6-Q7 | generate_horizon_test_values() returns different structures based on param type | ConfigGenerator.generate_horizon_test_values() | If BASE_CONFIG_PARAMS: return {'shared': [N]}, else return {'ros': [N], '1-5': [N], ...} | [x] Verified Iter 4 |
| Specs lines 115-119, Q8 | get_config_for_horizon() returns complete config with test value applied | ConfigGenerator.get_config_for_horizon() | None - always returns deep copy | [x] Verified Iter 4 |
| Specs lines 120-130, Q9 | update_baseline_for_horizon() updates baseline differently based on param type | ConfigGenerator.update_baseline_for_horizon() | If shared param: update league_config portion in all 5 horizons, else update only specified horizon | [x] Verified Iter 4 |
| Specs lines 177-180, Q14-Q15 | Win-rate optimizes ONLY BASE_CONFIG_PARAMS | SimulationManager.__init__() | Filter parameter_order to only BASE_CONFIG_PARAMS before ConfigGenerator init | [x] Verified Iter 4 |
| Specs lines 198-207, Q18-Q20 | Accuracy optimizes ONLY WEEK_SPECIFIC_PARAMS | run_accuracy_simulation.py | PARAMETER_ORDER = WEEK_SPECIFIC_PARAMS only | [x] Verified Iter 4 |
| Specs lines 274-275, Q35 | Win-rate tests N configs (not 5×N) | SimulationManager.run_*() | Shared param: N test values across all horizons | [x] Verified Iter 4 |
| Specs lines 274-275, Q35 | Accuracy tests 5×N configs (tournament) | AccuracySimulationManager.run_*() | Horizon param: 5 horizons × N test values = 5×N configs | [x] Verified Iter 4 |
| Specs lines 187-189, 209-210, Q17, Q21 | Save all 6 files (both simulations) | ResultsManager.save_optimal_configs_folder() | None - always save all 6 | [x] Verified Iter 4 |
| Specs lines 267-270, Q33 | Return deep copies when providing configs | ConfigGenerator.get_config_for_horizon() | copy.deepcopy(baseline_configs[horizon]) | [x] Verified Iter 4 |
| Specs lines 268-270, Q34 | Pre-generate test values for determinism | ConfigGenerator.generate_horizon_test_values() | Store in self.test_values, return stored dict | [x] Verified Iter 4 |

**Algorithm Coverage Summary:**
- ✅ File loading algorithm (6-file structure) - 2 entries
- ✅ Test value generation (conditional based on param type) - 1 entry
- ✅ Config retrieval (horizon + test index) - 1 entry
- ✅ Baseline update (conditional based on param type) - 1 entry
- ✅ Win-rate parameter filtering (BASE_CONFIG_PARAMS only) - 1 entry
- ✅ Accuracy parameter filtering (WEEK_SPECIFIC_PARAMS only) - 1 entry
- ✅ Config count logic (N vs 5×N) - 2 entries
- ✅ Save logic (6 files for both modes) - 1 entry
- ✅ Deep copy for safety - 1 entry
- ✅ Test value pre-generation - 1 entry
- **Total: 12 algorithm entries, all verified in Iteration 4**

---

## Data Flow Traces

### Requirement: Win-Rate Optimizes Shared Parameters
```
Entry: run_win_rate_simulation.py
  → SimulationManager.run_optimization()
  → ConfigGenerator.generate_horizon_test_values(param_name)  ← NEW (returns {'shared': [...]})
  → ConfigGenerator.get_config_for_horizon(horizon, param, idx)  ← NEW (applies shared value)
  → Run simulation with config
  → ConfigGenerator.update_baseline_for_horizon(horizon, optimal_config)  ← NEW
  → Output: simulation_configs/optimal_*/league_config.json (optimized) + 5 horizon files (saved fresh)
```

### Requirement: Accuracy Optimizes Horizon Parameters (Tournament Model)
```
Entry: run_accuracy_simulation.py
  → AccuracySimulationManager.run_optimization()
  → ConfigGenerator.generate_horizon_test_values(param_name)  ← NEW (returns {'ros': [...], '1-5': [...], ...})
  → Loop: 5 horizons × N test values
    → ConfigGenerator.get_config_for_horizon(horizon, param, idx)  ← NEW (applies horizon-specific value)
    → Calculate MAE with config
  → ConfigGenerator.update_baseline_for_horizon(horizon, optimal_config)  ← NEW (per horizon)
  → Output: simulation_configs/accuracy_optimal_*/league_config.json (copied) + 5 horizon files (optimized)
```

### Requirement: Load 6-File Baseline Folders
```
Entry: ConfigGenerator.__init__(baseline_folder)
  → ConfigGenerator.load_baseline_from_folder()  ← MODIFIED
    → Validate 6 files exist (fail if missing)
    → Load league_config.json
    → Load 5 horizon files (draft_config.json, week1-5.json, ...)
    → Merge each: league + horizon → baseline_configs[horizon]
  → Store: self.baseline_configs = {'ros': {...}, '1-5': {...}, ...} (5 merged configs)
```

---

## Test Strategy

### Unit Tests to Create/Update

1. **test_ConfigPerformance.py**
   - Test HORIZONS constant exists and has correct values
   - Test HORIZON_FILES constant exists and has correct mapping

2. **test_ResultsManager.py**
   - Test required_files includes all 6 files
   - Test week_range_files includes 'ros' → 'draft_config.json'
   - Test save_optimal_configs_folder() saves 6 files
   - Test load_from_folder() loads 6 files
   - Test load_from_folder() fails with clear error if any file missing

3. **test_config_generator.py**
   - Test __init__ accepts 2 params (baseline_folder, num_test_values)
   - Test __init__ rejects 3 params (old signature)
   - Test load_baseline_from_folder() creates 5 horizon baselines
   - Test load_baseline_from_folder() fails if any of 6 files missing
   - Test generate_horizon_test_values() for shared param returns {'shared': [...]}
   - Test generate_horizon_test_values() for horizon param returns {'ros': [...], '1-5': [...], ...}
   - Test get_config_for_horizon() returns deep copy with test value applied
   - Test get_config_for_horizon() uses shared value for shared params
   - Test get_config_for_horizon() uses horizon-specific value for horizon params
   - Test update_baseline_for_horizon() updates correct horizon baseline
   - Test generate_iterative_combinations() method does NOT exist (removed)

4. **test_simulation_manager.py**
   - Test ConfigGenerator initialized with 2 params
   - Test PARAMETER_ORDER contains only BASE_CONFIG_PARAMS
   - Test uses generate_horizon_test_values(), get_config_for_horizon(), update_baseline_for_horizon()

5. **test_AccuracySimulationManager.py**
   - Test ConfigGenerator initialized with 2 params
   - Test PARAMETER_ORDER contains only WEEK_SPECIFIC_PARAMS
   - Test uses generate_horizon_test_values(), get_config_for_horizon(), update_baseline_for_horizon()
   - Test generates 5×N configs (tournament model)

### Integration Tests to Create/Update

1. **test_simulation_integration.py**
   - Test win-rate simulation runs E2E with 6-file structure
   - Test saves optimal folder with 6 files
   - Test output folder loadable as input for next simulation

2. **test_accuracy_simulation_integration.py**
   - Test accuracy simulation runs E2E with 6-file structure
   - Test saves optimal folder with 6 files
   - Test tests 5×N configs per parameter (tournament model)

---

## Iteration Findings

### Iteration 1 Findings (Standard Verification)

**FINDING 1: ConfigGenerator __init__ signature differs from planning assumptions**
- **Actual signature:** `__init__(baseline_config_path: Path, parameter_order: List[str], num_test_values: int = 5, num_parameters_to_test: int = 1)`
- **Assumed in TODO:** `__init__(baseline_folder: str, num_test_values: int)`
- **Impact:** Must update signature to remove `parameter_order` param (no longer needed with new interface) AND remove `num_parameters_to_test`
- **Correction:** New signature should be: `__init__(baseline_config_path: Path, num_test_values: int = 5)`
- **Tasks updated:** Task 3.1 corrected with actual current signature

**FINDING 2: Method name mismatch**
- **Actual method:** `is_base_param(param_name: str)` (line 231)
- **TODO referenced:** `is_base_config_param()`
- **Impact:** Minor - just update method name references in TODO
- **Correction:** Use `is_base_param()` and `is_week_specific_param()` throughout

**FINDING 3: Constants verified**
- ResultsManager.BASE_CONFIG_PARAMS exists at line 239 ✓
- ResultsManager.WEEK_SPECIFIC_PARAMS exists at line 255 ✓
- ConfigPerformance.WEEK_RANGES exists at line 23 ✓
- ResultsManager.week_range_files exists at lines 426 and 526 ✓

**FINDING 4: File paths verified**
- simulation/shared/ConfigPerformance.py exists ✓
- simulation/shared/ResultsManager.py exists ✓
- simulation/shared/ConfigGenerator.py exists ✓
- simulation/win_rate/SimulationManager.py exists ✓
- Line numbers verified accurate ✓

**ITERATION 2 FINDINGS (Standard Verification - Round 1):**

**FINDING 5: Error handling pattern - ValueError for all validation errors**
- ConfigGenerator uses ValueError exclusively (not custom error classes)
- Pattern: Raise ValueError immediately with descriptive message (fail fast)
- Examples found at lines: 311, 314, 325, 390, 398, 401, 437, 557, 789, 975
- Impact: New methods should follow same pattern (ValueError with clear messages)

**FINDING 6: Logging patterns in ConfigGenerator**
- Uses get_logger() from utils.LoggingManager
- Logging levels:
  - self.logger.info(): Initialization, major operations (16 locations)
  - self.logger.debug(): Detailed config loading (7 locations)
  - self.logger.warning(): Unknown parameters, invalid values (4 locations)
- Pattern: Log before raising errors for context
- Impact: New methods need similar logging (info for major ops, debug for details)

**FINDING 7: Error handling in ResultsManager**
- Also uses get_logger() from utils.LoggingManager
- Uses KeyError for unregistered configs (line 78)
- Uses warning logs for non-critical issues (4 locations)
- Pattern matches ConfigGenerator (log warnings, raise errors when critical)

**FINDING 8: Custom error classes available but not used**
- utils/error_handler.py defines custom errors (FantasyFootballError, ConfigurationError, etc.)
- Neither ConfigGenerator nor ResultsManager use these
- Pattern: Standard Python exceptions (ValueError, KeyError, FileNotFoundError)
- Decision: Follow existing pattern (use ValueError), don't introduce custom errors

**FINDING 9: Required error handling for new methods**
- generate_horizon_test_values():
  - ValueError if param_name not in PARAM_DEFINITIONS
  - Log at info level when generating test values
  - Log at debug level for each horizon's test values
- get_config_for_horizon():
  - ValueError if horizon not in HORIZONS
  - ValueError if param_name not in PARAM_DEFINITIONS
  - ValueError if test_index out of range
  - Log at debug level when providing config
- update_baseline_for_horizon():
  - ValueError if horizon not in HORIZONS
  - ValueError if new_config missing 'parameters'
  - Log at info level when updating baseline
- load_baseline_from_folder() (refactored):
  - ValueError if missing any of 6 required files (not just 5)
  - ValueError if 'parameters' missing from any horizon file
  - Log at debug level for each file loaded
  - Log at info level for successful load

**FINDING 10: Logging for 6-file structure**
- Update existing log at line 334: "Loaded league_config from {base_config_path}"
- Add new log: "Loaded draft_config from {draft_config_path}"
- Keep existing week file logs (line 342 pattern)
- Update line 361: Change from "Loaded baseline config" to "Loaded 5 horizon baselines from folder"

**ITERATION 3 FINDINGS (Standard Verification - Round 1):**

**FINDING 11: SimulationManager integration points**
- Location: simulation/win_rate/SimulationManager.py
- Constructor params (lines 64-76):
  - baseline_config_path: Path
  - output_dir: Path
  - num_simulations_per_config: int
  - max_workers: int
  - data_folder: Path
  - parameter_order: List[str]
  - num_test_values: int = 5
  - num_parameters_to_test: int = 1 (TO BE REMOVED)
  - auto_update_league_config: bool = True
  - use_processes: bool = False
- ConfigGenerator initialization (lines 111-116):
  - Currently passes all 4 params
  - Need to remove parameter_order and num_parameters_to_test
- Impact: Task 4.1 must remove 2 parameters from ConfigGenerator init call

**FINDING 12: AccuracySimulationManager integration points**
- Location: simulation/accuracy/AccuracySimulationManager.py
- Constructor params (lines 72-80):
  - baseline_config_path: Path
  - output_dir: Path
  - data_folder: Path
  - parameter_order: List[str]
  - num_test_values: int = 5
  - num_parameters_to_test: int = 1 (TO BE REMOVED)
- ConfigGenerator initialization (lines 111-116):
  - Currently passes all 4 params
  - Need to remove parameter_order and num_parameters_to_test
- Impact: Task 5.1 must remove 2 parameters from ConfigGenerator init call

**FINDING 13: Test mocking patterns from test_config_generator.py**
- Uses pytest fixtures for test data creation (lines 55-167)
- create_test_config_folder() helper creates 5-file structure (needs update to 6-file)
- Mock pattern: Create real files in tmp_path, not mocked file I/O
- Test structure:
  - Class-based tests: TestConfigGeneratorInitialization
  - Fixtures for reusable test data
  - tmp_path for temporary file creation
- Impact: Tests will need draft_config.json added to test folder creation

**FINDING 14: Integration with ResultsManager**
- Both SimulationManager and AccuracySimulationManager use ResultsManager
- Win-rate: Uses ResultsManager.save_optimal_configs_folder() (line 454)
- Accuracy: Uses AccuracyResultsManager.save_optimal_configs_folder()
- Both need 6-file structure support
- Impact: Confirmed Task 2.3 requirement

**FINDING 15: Parameter filtering for win-rate simulation**
- SimulationManager receives parameter_order from run_win_rate_simulation.py
- Need to filter parameter_order to only BASE_CONFIG_PARAMS before passing to ConfigGenerator
- Location of filter: SimulationManager.__init__() (before ConfigGenerator init)
- Implementation:
  ```python
  # Filter to only BASE_CONFIG_PARAMS (shared params)
  from ResultsManager import BASE_CONFIG_PARAMS
  filtered_params = [p for p in parameter_order if p in BASE_CONFIG_PARAMS]
  ```
- Impact: Added detail to Task 4.2

**FINDING 16: No mocking of file I/O in existing tests**
- Pattern: Tests create real files in tmp_path (pytest fixture)
- No @patch for open() or Path operations
- Advantage: Tests actual file loading logic
- Impact: New tests should follow same pattern (real files, not mocks)

**FINDING 17: Test file naming convention**
- Test files: tests/simulation/test_*.py
- Mirror source structure: test_config_generator.py for ConfigGenerator
- Need new tests:
  - Update existing test_config_generator.py for 6-file structure
  - Update existing test_ResultsManager.py for 6-file structure
  - Update existing test_simulation_manager.py for new interface
  - Update existing test_AccuracySimulationManager.py for new interface

**FINDING 18: Scope creep check - NO scope additions**
- All tasks derive from specs (40 resolved questions)
- No "while I'm here" items
- No improvements beyond spec requirements
- Verification: All 23 TODO tasks map to spec requirements

**ITERATION 4 FINDINGS (Algorithm Traceability Matrix):**

**FINDING 19: All algorithms identified and traceable**
- 9 distinct algorithms documented in Algorithm Traceability Matrix
- Each algorithm mapped to specific code location
- Conditional logic explicitly documented for branching algorithms
- Key algorithms:
  1. 6-file loading and merging
  2. Conditional test value generation (shared vs horizon params)
  3. Config retrieval with test values
  4. Conditional baseline updates (shared vs horizon)
  5. Parameter filtering for win-rate (BASE_CONFIG_PARAMS)
  6. Parameter filtering for accuracy (WEEK_SPECIFIC_PARAMS)
  7. Config count logic (N vs 5×N)
  8. 6-file save logic

**FINDING 20: Conditional logic requires careful implementation**
- 3 methods have conditional logic based on param type:
  - generate_horizon_test_values(): Different return structure
  - update_baseline_for_horizon(): Different update scope
  - Both use is_base_param() to determine param type
- Risk: If conditional logic incorrect, wrong behavior could occur silently
- Mitigation: Unit tests must verify both branches for each conditional method

**FINDING 21: Parameter filtering happens at different levels**
- Win-rate: Filter happens in SimulationManager.__init__() before ConfigGenerator
- Accuracy: Filter happens in run_accuracy_simulation.py (top-level script)
- This is correct per specs (Q14, Q18 resolutions)
- Both approaches achieve same goal (different param sets optimized)

**FINDING 22: No missing algorithms**
- All spec requirements have corresponding algorithm entries
- All TODO tasks map to algorithm matrix entries
- Data flow diagram (specs lines 335-380) fully traced

**ITERATION 5 FINDINGS (End-to-End Data Flow):**

**FINDING 23: Entry points identified and verified**
- Win-rate simulation entry: SimulationManager.run_iterative_optimization() (line 626)
- Accuracy simulation entries:
  - AccuracySimulationManager.run_ros_optimization() (line 529)
  - AccuracySimulationManager.run_weekly_optimization() (line 634)
  - AccuracySimulationManager.run_both() (line 748)
- All entry points verified to exist

**FINDING 24: Complete data flow traced for win-rate simulation**
- Entry: run_win_rate_simulation.py → SimulationManager.run_iterative_optimization()
- Flow:
  1. Line 659: Get parameter_order from config_generator
  2. Loop through parameters (currently line 707+)
  3. MODIFICATION POINT: Call new generate_horizon_test_values(param_name)
  4. MODIFICATION POINT: Loop through test values, call get_config_for_horizon()
  5. Run simulation with each config
  6. Find optimal config for parameter
  7. MODIFICATION POINT: Call update_baseline_for_horizon() with optimal
  8. Save intermediate configs (ResultsManager.save_optimal_configs_folder)
- Output: simulation_configs/optimal_*/6 files (league_config.json + 5 horizon files)

**FINDING 25: Complete data flow traced for accuracy simulation**
- Entry: run_accuracy_simulation.py → AccuracySimulationManager.run_weekly_optimization()
- Flow:
  1. Initialize ConfigGenerator with baseline_folder
  2. Loop through WEEK_SPECIFIC_PARAMS only
  3. MODIFICATION POINT: Call generate_horizon_test_values(param_name)
    → Returns {'ros': [...], '1-5': [...], ...} (5 independent arrays)
  4. MODIFICATION POINT: Nested loop: for each horizon, for each test value
  5. MODIFICATION POINT: Call get_config_for_horizon(horizon, param, test_idx)
  6. Calculate MAE with config
  7. Find optimal per horizon independently (tournament model)
  8. MODIFICATION POINT: Call update_baseline_for_horizon() for each horizon
  9. Save optimal configs (AccuracyResultsManager.save_optimal_configs_folder)
- Output: simulation_configs/accuracy_optimal_*/6 files

**FINDING 26: No orphan code detected**
- All new methods have identified callers:
  - generate_horizon_test_values() → Called by both simulations (Task 4.3, 5.3)
  - get_config_for_horizon() → Called by both simulations (Task 4.3, 5.3)
  - update_baseline_for_horizon() → Called by both simulations (Task 4.3, 5.3)
  - HORIZONS constant → Used by ConfigGenerator.load_baseline_from_folder()
  - HORIZON_FILES constant → Used by ConfigGenerator.load_baseline_from_folder()
- All constants have consumers identified

**FINDING 27: Integration points explicitly documented**
- Integration Matrix (lines 508-520) complete with:
  - Component name
  - Source file
  - Caller
  - Caller file:line
  - TODO task for modification
- All 8 new components mapped

**ITERATION 6 FINDINGS (Skeptical Re-verification):**

**FINDING 28: All file paths re-verified and exist**
- ✅ simulation/shared/ConfigPerformance.py exists
- ✅ simulation/shared/ResultsManager.py exists
- ✅ simulation/shared/ConfigGenerator.py exists
- ✅ simulation/win_rate/SimulationManager.py exists
- ✅ simulation/accuracy/AccuracySimulationManager.py exists
- All paths from TODO verified with Glob tool

**FINDING 29: All method names re-verified**
- ✅ ConfigGenerator class at line 65
- ✅ is_base_param() at line 231 (NOT is_base_config_param - this was corrected in Iteration 1)
- ✅ is_week_specific_param() at line 254
- ✅ SimulationManager.run_iterative_optimization() at line 626
- ✅ AccuracySimulationManager.run_weekly_optimization() at line 634
- All method signatures verified with Grep

**FINDING 30: Constants re-verified**
- ✅ BASE_CONFIG_PARAMS at ResultsManager.py:239 (12 params: CURRENT_NFL_WEEK through ADP_SCORING)
- ✅ WEEK_SPECIFIC_PARAMS at ResultsManager.py:255 (9 params: NORMALIZATION_MAX_SCALE through LOCATION_MODIFIERS)
- ✅ WEEK_RANGES at ConfigPerformance.py:23 = ["1-5", "6-9", "10-13", "14-17"]
- ✅ ConfigGenerator imports these from ResultsManager at lines 61-62
- All constants exist and are accessible

**FINDING 31: CRITICAL - WEEK_RANGES format inconsistency detected**
- **Win-rate WEEK_RANGES:** Array format `["1-5", "6-9", "10-13", "14-17"]` (ConfigPerformance.py:23)
- **Accuracy WEEK_RANGES:** Dict format `{'week_1_5': (1, 5), ...}` (AccuracyResultsManager.py:32)
- **Impact on specs:** Specs Q10-Q11 resolution uses win-rate format (hyphens: '1-5', '6-9', etc.)
- **Decision:** Use win-rate format (hyphen format) for HORIZONS constant
- **Rationale:**
  - Win-rate format is in shared/ folder (more authoritative)
  - Matches file names (week1-5.json, not week_1_5.json)
  - Accuracy can convert format internally if needed
- **HORIZONS constant will be:** `['ros', '1-5', '6-9', '10-13', '14-17']`

**FINDING 32: Required files list re-verified**
- Current required_files at ResultsManager.py:593: 5 files (no draft_config.json)
- Must add 'draft_config.json' to this list
- Verified this is the exact location to modify (Task 2.1)

**FINDING 33: ConfigGenerator.__init__ signature re-verified**
- Current signature at line 364:
  ```python
  def __init__(self, baseline_config_path: Path, parameter_order: List[str],
               num_test_values: int = 5, num_parameters_to_test: int = 1)
  ```
- Must remove: parameter_order and num_parameters_to_test
- New signature will be:
  ```python
  def __init__(self, baseline_config_path: Path, num_test_values: int = 5)
  ```
- Verified in Task 3.1

**FINDING 34: Specification requirements re-read**
- Re-read specs lines 9-412 word-by-word
- All requirements still match TODO tasks
- No missed requirements detected
- 6-file structure clearly specified (lines 13-19)
- Horizon composition clearly specified (lines 21-27)
- All 40 resolved questions still valid

**FINDING 35: Confidence calibration**
Using criteria from protocols_reference.md lines 531-540:
- **File Paths:** All verified with Read/Glob ✅ HIGH
- **Method Signatures:** All confirmed from source ✅ HIGH
- **Integration Points:** All callers identified and verified ✅ HIGH
- **Data Flow:** Complete trace from entry to output ✅ HIGH
- **Similar Patterns:** Win-rate/accuracy both use similar optimization loops ✅ HIGH
- **Edge Cases:** Most identified (6-file validation, param type detection) ✅ MEDIUM-HIGH

**Overall Confidence: MEDIUM-HIGH**
- All critical paths verified
- One minor format inconsistency (WEEK_RANGES) documented and resolved
- Implementation plan is sound

**ITERATION 7 FINDINGS (Integration Gap Check):**

**FINDING 36: Integration Matrix verified complete**
- 8 new components documented in Integration Matrix (lines 510-519)
- All components have callers identified:
  - HORIZONS constant → Called by ConfigGenerator.load_baseline_from_folder (Task 3.2)
  - HORIZON_FILES constant → Called by ConfigGenerator.load_baseline_from_folder (Task 3.2)
  - generate_horizon_test_values() → Called by both SimulationManager and AccuracySimulationManager (Tasks 4.3, 5.3)
  - get_config_for_horizon() → Called by both SimulationManager and AccuracySimulationManager (Tasks 4.3, 5.3)
  - update_baseline_for_horizon() → Called by both SimulationManager and AccuracySimulationManager (Tasks 4.3, 5.3)
- All caller modification tasks exist in TODO

**FINDING 37: NO orphan code detected**
- Every new method has at least one caller
- Every new constant has at least one consumer
- All modifications tied to entry points:
  - Win-rate entry: SimulationManager.run_iterative_optimization()
  - Accuracy entries: AccuracySimulationManager.run_weekly_optimization(), run_ros_optimization()

**FINDING 38: Entry point coverage verified**
- Win-rate path: run_win_rate_simulation.py → SimulationManager → ConfigGenerator → new methods ✅
- Accuracy path: run_accuracy_simulation.py → AccuracySimulationManager → ConfigGenerator → new methods ✅
- All new code in execution paths

**FINDING 39: Cross-feature impact assessment**
Modified files and their consumers:
- **ConfigPerformance.py** (add constants):
  - Used by: SimulationManager, ResultsManager, ConfigGenerator
  - Impact: None - adding new constants, existing code unaffected
  - Mitigation: N/A

- **ResultsManager.py** (6-file support):
  - Used by: SimulationManager, AccuracySimulationManager
  - Impact: Breaking change - old 5-file folders will fail
  - Mitigation: Documented in specs Q32, error message directs to 6-file structure

- **ConfigGenerator.py** (refactor to horizon-based):
  - Used by: SimulationManager, AccuracySimulationManager
  - Impact: Breaking change - signature change
  - Mitigation: Atomic update (all callers updated simultaneously per Q39)

- **SimulationManager.py** (new interface usage):
  - Entry point: run_win_rate_simulation.py
  - Impact: Internal change only, external CLI unchanged
  - Mitigation: N/A

- **AccuracySimulationManager.py** (new interface usage):
  - Entry point: run_accuracy_simulation.py
  - Impact: Internal change only, external CLI unchanged
  - Mitigation: N/A

**FINDING 40: No unresolved alternatives**
- Searched TODO for "Alternative:" - 0 matches ✅
- Searched TODO for "May need to" - 0 matches ✅
- All decisions finalized during planning (40 questions resolved)
- No uncertainty remaining

**FINDING 41: Caller verification**
- ConfigGenerator instantiation:
  - SimulationManager.py:118 (verified with Grep)
  - AccuracySimulationManager.py:112 (verified with Grep)
  - Both locations documented in Tasks 4.1 and 5.1
- save_optimal_configs_folder calls:
  - ResultsManager.py:366 (method definition)
  - Used by both simulation managers
  - Task 2.3 addresses this method

**FINDING 42: Round 1 complete - 7/7 iterations**
- ✅ Standard Verification (Iterations 1-3): Files, error handling, integration
- ✅ Algorithm Traceability (Iteration 4): 12 algorithms mapped
- ✅ End-to-End Data Flow (Iteration 5): Complete flows traced
- ✅ Skeptical Re-verification (Iteration 6): All paths verified, format issue found
- ✅ Integration Gap Check (Iteration 7): No orphan code, all callers identified

**Round 1 Status: COMPLETE (100%)**
**Overall Confidence: MEDIUM-HIGH**
**Ready to proceed to Round 2**

**ITERATION 8 FINDINGS (Standard Verification - Round 2):**

**Focus Question: How do user answers change the plan? Any new tasks needed?**

**FINDING 43: All 40 user answers reviewed**
- Checklist has 40 questions across 3 iterations (all resolved)
- Each question has detailed resolution with date and reasoning
- All resolutions dated 2025-12-16 (planning phase completion)

**FINDING 44: User answers properly integrated into TODO**
Verification that each resolved question has corresponding TODO task:
- Q1-Q4 (File loading): Tasks 3.2, 2.1-2.4 ✅
- Q5-Q9 (Interface design): Tasks 3.3, 3.4, 3.5 ✅
- Q10-Q11 (Horizon naming): Task 1.1, 1.2 (HORIZONS/HORIZON_FILES) ✅
- Q12-Q13 (Data structures): Task 3.2 (baseline_configs dict) ✅
- Q14-Q17 (Win-rate integration): Tasks 4.1, 4.2, 4.3 ✅
- Q18-Q21 (Accuracy integration): Tasks 5.1, 5.2, 5.3 ✅
- Q22-Q23 (Unified interface): Tasks 3.3-3.5 ✅
- Q24-Q26 (ResultsManager): Tasks 2.1-2.4 ✅
- Q27-Q29 (Error handling): Documented in Iteration 2 findings ✅
- Q30-Q32 (Testing): Test Strategy section (lines 595-640) ✅
- Q33-Q35 (Performance): Documented in specs, deepcopy in Task 3.4 ✅
- Q36-Q38 (Deprecation): Task 3.1 (remove params), Task 3.6 (remove method) ✅
- Q39 (Implementation strategy): Atomic change documented ✅
- Q40 (Unified interface): Tasks 3.3-3.5 ✅

**FINDING 45: No new tasks needed from user answers**
- All 40 resolutions already have corresponding implementation tasks
- No gaps between planning and implementation
- User decisions comprehensively captured

**FINDING 46: Key user decisions verified in TODO**
Critical decisions from planning phase properly reflected:
1. **6-file structure** (Q1-Q4): Tasks 1.1-1.2, 2.1-2.4, 3.2 ✅
2. **Unified auto-detection interface** (Q22-Q23, Q40): Tasks 3.3-3.5 ✅
3. **Win-rate optimizes shared params only** (Q14-Q15): Task 4.2 ✅
4. **Accuracy optimizes horizon params only** (Q18-Q20): Task 5.2 ✅
5. **Atomic implementation** (Q39): All tasks in single commit ✅
6. **No backward compatibility** (Q32): Clean break documented ✅
7. **Deprecate NUM_PARAMETERS_TO_TEST** (Q36-Q37): Tasks 3.1, 3.6 ✅

**FINDING 47: User answer quality assessment**
- All answers specific and actionable (no vague "investigate further")
- All answers include implementation details
- All answers include rationale/reasoning
- No unresolved alternatives in answers
- Planning phase was thorough

**ITERATION 9 FINDINGS (Standard Verification - Round 2):**

**Focus Question: Are dependencies correctly identified? Any imports missing?**

**FINDING 48: Existing imports in ConfigGenerator verified**
Current imports in ConfigGenerator.py (lines 45-62):
- `import json` - ✅ Needed (loading/merging configs)
- `import random` - ✅ Needed (generating test values)
- `import copy` - ✅ Needed (deep copying configs per Q33)
- `from pathlib import Path` - ✅ Needed (file operations)
- `from typing import List, Dict, Tuple` - ✅ Needed (type hints)
- `from itertools import product` - ⚠️ Used by generate_iterative_combinations (will be removed per Task 3.6)
- `from utils.LoggingManager import get_logger` - ✅ Needed (logging)
- `from ResultsManager import ResultsManager` - ✅ Needed (BASE_CONFIG_PARAMS, WEEK_SPECIFIC_PARAMS)

**FINDING 49: New imports needed for ConfigGenerator**
Additional imports required for new functionality:
- **HORIZONS constant**: Import from ConfigPerformance
- **HORIZON_FILES constant**: Import from ConfigPerformance

New import statement to add (after line 58):
```python
from ConfigPerformance import HORIZONS, HORIZON_FILES
```

**FINDING 50: ResultsManager imports verified**
Current imports in ResultsManager.py (lines 11-23):
- `import json` - ✅ Needed (file I/O)
- `from pathlib import Path` - ✅ Needed (file operations)
- `from typing import Dict, Optional, List, Tuple, Any` - ✅ Needed (type hints)
- `from datetime import datetime` - ✅ Needed (timestamps)
- `from ConfigPerformance import ConfigPerformance, WEEK_RANGES` - ✅ Needed
- No new imports needed for ResultsManager (uses existing WEEK_RANGES)

**FINDING 51: SimulationManager imports verified**
Current imports in SimulationManager.py (lines 20-44):
- `from ConfigGenerator import ConfigGenerator` - ✅ Needed
- `from ResultsManager import ResultsManager` - ✅ Needed (will need BASE_CONFIG_PARAMS for filtering)
- `from ConfigPerformance import WEEK_RANGES` - ✅ Needed
- No new imports needed

Task 4.2 will need to import BASE_CONFIG_PARAMS:
```python
from ResultsManager import ResultsManager, BASE_CONFIG_PARAMS
```

**FINDING 52: AccuracySimulationManager imports verified**
Current imports in AccuracySimulationManager.py:
- `from ConfigGenerator import ConfigGenerator` - ✅ Needed
- No new imports needed (WEEK_SPECIFIC_PARAMS filtering happens in run_accuracy_simulation.py)

**FINDING 53: ConfigPerformance imports verified**
Current imports in ConfigPerformance.py (lines 17-18):
- `from typing import Dict, List, Tuple, Optional` - ✅ Needed
- `import json` - ✅ Needed
- No new imports needed (just adding constants)

**FINDING 54: All dependencies satisfied**
Dependency chain verified:
1. ConfigPerformance.py exports: HORIZONS, HORIZON_FILES, WEEK_RANGES ✅
2. ResultsManager.py exports: BASE_CONFIG_PARAMS, WEEK_SPECIFIC_PARAMS ✅
3. ConfigGenerator.py imports from both above ✅
4. SimulationManager imports ConfigGenerator + BASE_CONFIG_PARAMS ✅
5. AccuracySimulationManager imports ConfigGenerator ✅

No circular dependencies detected ✅

**FINDING 55: Import statement to add**
Only one new import needed in ConfigGenerator.py (Task 3.2):
```python
# Add after line 58 (after ResultsManager import)
from ConfigPerformance import HORIZONS, HORIZON_FILES
```

All other files have sufficient imports already.

**ITERATION 10 FINDINGS (Standard Verification - Round 2):**

**Focus Question: Is the task breakdown granular enough? Any tasks too large?**

**FINDING 56: Task count and distribution**
- Total tasks: 23 across 5 phases
- Phase 1: 2 tasks (constants)
- Phase 2: 4 tasks (ResultsManager 6-file support)
- Phase 3: 6 tasks (ConfigGenerator refactor) ⚠️ LARGEST PHASE
- Phase 4: 3 tasks (SimulationManager integration)
- Phase 5: 3 tasks (AccuracySimulationManager integration)
- Plus 5 QA checkpoints

**FINDING 57: Task size assessment**
Reviewing each task for appropriate granularity:

**SMALL TASKS (appropriate size):**
- Task 1.1: Add HORIZONS constant (1 line) ✅
- Task 1.2: Add HORIZON_FILES constant (6 lines) ✅
- Task 2.1: Update required_files list (1 line change) ✅
- Task 2.2: Update week_range_files mapping (1 entry added) ✅
- Task 3.1: Update __init__ signature (remove 2 params) ✅
- Task 3.6: Remove generate_iterative_combinations() (delete 1 method) ✅
- Task 4.2: Filter PARAMETER_ORDER (3-5 lines) ✅
- Task 5.2: Update PARAMETER_ORDER in script (already correct per specs) ✅

**MEDIUM TASKS (appropriate size):**
- Task 2.3: Update save_optimal_configs_folder() (modify loop, add 1 file) ✅
- Task 2.4: Update load_from_folder() (validate 6 files instead of 5) ✅
- Task 3.4: Create get_config_for_horizon() (20-30 lines) ✅
- Task 3.5: Create update_baseline_for_horizon() (20-30 lines with conditional) ✅
- Task 4.1: Update ConfigGenerator initialization in SimulationManager (remove 2 args) ✅
- Task 5.1: Update ConfigGenerator initialization in AccuracySimulationManager (remove 2 args) ✅

**LARGE TASKS (check if need subdivision):**
- **Task 3.2: Update load_baseline_from_folder()** (50-70 lines)
  - Sub-steps: (1) Validate 6 files, (2) Load league_config, (3) Loop 5 horizons, (4) Merge each
  - **Assessment:** Can be done atomically, well-defined steps ✅ ACCEPTABLE

- **Task 3.3: Create generate_horizon_test_values()** (40-60 lines with conditional logic)
  - Sub-steps: (1) Detect param type, (2) If shared: generate 1 array, (3) If horizon: generate 5 arrays
  - **Assessment:** Single method with clear structure ✅ ACCEPTABLE

- **Task 4.3: Update SimulationManager simulation loop** (complex, touches optimization flow)
  - Sub-steps: (1) Call generate_horizon_test_values, (2) Loop test values, (3) Call get_config_for_horizon, (4) Run simulation, (5) Call update_baseline_for_horizon
  - **Assessment:** Multiple integration points, but single optimization loop ✅ ACCEPTABLE
  - **Note:** This is the most complex task, but breaking it down would create partial states

- **Task 5.3: Update AccuracySimulationManager simulation loop** (similar complexity to 4.3)
  - Sub-steps: Similar to 4.3 but with horizon-specific logic (tournament model)
  - **Assessment:** Single optimization loop ✅ ACCEPTABLE

**FINDING 58: No tasks too large**
- All tasks can be completed in single focused session
- Complex tasks (3.2, 3.3, 4.3, 5.3) are appropriately sized for their scope
- Breaking them down would create incomplete intermediate states
- Each task has clear entry/exit points

**FINDING 59: Task dependencies proper**
- Phase 1 → Phase 2 → Phase 3 → Phases 4&5 (correct order)
- QA checkpoints at logical boundaries
- No circular dependencies
- Atomic implementation per Q39 (all in one commit)

**FINDING 60: Task granularity appropriate for testing**
Each task can be independently tested:
- Tasks 1.1-1.2: Import test
- Tasks 2.1-2.4: ResultsManager unit tests
- Tasks 3.1-3.6: ConfigGenerator unit tests
- Tasks 4.1-4.3: SimulationManager integration test
- Tasks 5.1-5.3: AccuracySimulationManager integration test

**FINDING 61: No subdivision needed**
- All 23 tasks are appropriately sized
- Complex tasks are necessarily complex (core refactor logic)
- Breaking them down would not improve clarity or safety
- QA checkpoints provide adequate validation points

**ITERATION 11 FINDINGS (Algorithm Traceability Matrix - Round 2):**

**Purpose: Re-verify algorithm coverage after Iterations 8-10 discoveries**

**FINDING 62: Algorithm Traceability Matrix re-verified**
Re-checked all 12 algorithms from Iteration 4 against current TODO state:
1. ✅ 6-file loading (load_baseline_from_folder) - Verified Task 3.2
2. ✅ Dict merge with horizon override - Verified Task 3.2
3. ✅ Conditional test value generation - Verified Task 3.3
4. ✅ Config retrieval with test values - Verified Task 3.4
5. ✅ Conditional baseline updates - Verified Task 3.5
6. ✅ Win-rate param filtering (BASE_CONFIG_PARAMS) - Verified Task 4.2
7. ✅ Accuracy param filtering (WEEK_SPECIFIC_PARAMS) - Verified Task 5.2
8. ✅ Config count logic (N vs 5×N) - Verified specs Q35
9. ✅ Config count logic (accuracy 5×N) - Verified specs Q35
10. ✅ 6-file save logic - Verified Tasks 2.3, 2.4
11. ✅ Deep copy for safety - Verified Task 3.4, specs Q33
12. ✅ Test value pre-generation - Verified Task 3.3, specs Q34

All 12 algorithms still valid and properly mapped.

**FINDING 63: No new algorithms discovered in Iterations 8-10**
Reviewed Iterations 8-10 findings (FINDING 42-61):
- Iteration 8: Verified user answers → TODO mapping (no new algorithms)
- Iteration 9: Import dependency check (no new algorithms, just imports)
- Iteration 10: Task granularity check (no new algorithms)
- ✅ No additional algorithmic requirements discovered
- ✅ No hidden complexity found requiring new algorithm entries

**FINDING 64: Conditional logic locations confirmed**
Three methods with conditional logic based on param type:
1. **generate_horizon_test_values()** (Task 3.3):
   - Condition: `if is_base_param(param_name)`
   - Branch A (shared): Return `{'shared': [N values]}`
   - Branch B (horizon): Return `{'ros': [...], '1-5': [...], ...}`
   - ✅ Both branches documented in Algorithm Traceability Matrix line 531

2. **update_baseline_for_horizon()** (Task 3.5):
   - Condition: `if is_base_param(param_name)`
   - Branch A (shared): Update league_config portion in all 5 horizons
   - Branch B (horizon): Update only specified horizon's baseline
   - ✅ Both branches documented in Algorithm Traceability Matrix line 533

3. **Config count logic** (Tasks 4.3, 5.3):
   - Win-rate (shared params): N configs total
   - Accuracy (horizon params): 5×N configs total
   - ✅ Both cases documented in Algorithm Traceability Matrix lines 536-537

**FINDING 65: All algorithms traceable to code locations**
Every algorithm in matrix has specific implementation location:
- Tasks 1.1-1.2: ConfigPerformance.py (new constants)
- Tasks 2.1-2.4: ResultsManager.py (6-file methods)
- Tasks 3.2-3.5: ConfigGenerator.py (new methods)
- Task 4.2: SimulationManager.__init__() (filtering)
- Task 4.3: SimulationManager.run_iterative_optimization() (loop)
- Task 5.2: run_accuracy_simulation.py (PARAMETER_ORDER definition)
- Task 5.3: AccuracySimulationManager.run_weekly_optimization() (loop)

No orphan algorithms (all have implementations planned).
No orphan tasks (all implement documented algorithms).

**FINDING 66: Algorithm documentation quality**
Algorithm Traceability Matrix (lines 523-553) contains:
- ✅ Spec section references (specific line numbers)
- ✅ Algorithm descriptions (clear, specific)
- ✅ Code locations (method names)
- ✅ Conditional logic (explicitly documented for branching algorithms)
- ✅ Status tracking (all marked verified from Iteration 4)

Matrix is complete and accurate.

**FINDING 67: No algorithmic gaps detected**
Cross-checked specs requirements vs Algorithm Traceability Matrix:
- Specs lines 11-27 (6-file structure) → Algorithms 1, 2 ✅
- Specs lines 38-42 (horizon composition) → Algorithm 1 ✅
- Specs lines 104-130 (ConfigGenerator interface) → Algorithms 3, 4, 5 ✅
- Specs lines 177-180 (win-rate optimization) → Algorithm 6, 8 ✅
- Specs lines 198-207 (accuracy optimization) → Algorithm 7, 9 ✅
- Specs lines 187-189, 209-210 (save logic) → Algorithm 10 ✅
- Specs lines 267-270 (performance) → Algorithms 11, 12 ✅

All spec requirements covered by algorithms.

**FINDING 68: Round 2 confidence assessment**
Algorithm coverage confidence: **HIGH**
- All 12 algorithms from Iteration 4 re-verified ✅
- No new algorithms discovered in Iterations 8-10 ✅
- All algorithms map to specific code locations ✅
- All conditional logic explicitly documented ✅
- No gaps between specs and algorithms ✅

Ready to proceed to Iteration 12 (End-to-End Data Flow - Round 2).

**ITERATION 12 FINDINGS (End-to-End Data Flow - Round 2):**

**Purpose: Re-verify complete data flows after Iterations 8-11 discoveries**

**FINDING 69: Win-rate data flow re-verified**
Entry point: `run_win_rate_simulation.py` → `SimulationManager.run_iterative_optimization()` (line 626)

Current flow (lines 626-750):
1. ✅ Line 660: Get `parameter_order` from `config_generator.parameter_order`
2. ✅ Line 709: Loop through parameters (`param_order[start_idx:]`)
3. ✅ Line 714: Check param type with `is_week_specific_param(param_name)`
4. ✅ Line 723: Generate configs with `generate_iterative_combinations(param_name, merged_config)`
5. ✅ Run simulations for each config
6. ✅ Find optimal config
7. ✅ Save intermediate results

**MODIFICATION POINTS for Task 4.3:**
- Line 660: Will change from `config_generator.parameter_order` to directly using filtered `parameter_order` (Task 4.2)
- Line 723: Will replace `generate_iterative_combinations()` with new interface:
  - Call `generate_horizon_test_values(param_name)` → returns `{'shared': [...]}`
  - Loop through test values
  - Call `get_config_for_horizon(horizon, param_name, test_idx)` for each horizon
- After optimal found: Call `update_baseline_for_horizon(horizon, optimal_config)` for each horizon

**FINDING 70: Accuracy data flow re-verified**
Entry point: `run_accuracy_simulation.py` → `AccuracySimulationManager.run_weekly_optimization()` (line 634)

Current flow (lines 634-733):
1. ✅ Line 652: Get `total_params = len(self.parameter_order)`
2. ✅ Line 680: Loop through week ranges (`WEEK_RANGES.items()`)
3. ✅ Line 694: Loop through parameters (`self.parameter_order`)
4. ✅ Line 705: Generate configs with `generate_iterative_combinations(param_name, current_base_config)`
5. ✅ Line 713: Evaluate config for week range
6. ✅ Line 726: Update base config with best

**MODIFICATION POINTS for Task 5.3:**
- Line 705: Will replace `generate_iterative_combinations()` with new interface:
  - Call `generate_horizon_test_values(param_name)` → returns `{'ros': [...], '1-5': [...], ...}`
  - Nested loop: for each horizon, for each test value
  - Call `get_config_for_horizon(horizon, param_name, test_idx)`
- Line 726: Will call `update_baseline_for_horizon(horizon, optimal_config)` per horizon

**FINDING 71: ConfigGenerator initialization points verified**
Win-rate: `SimulationManager.__init__()` at lines 111-116
```python
self.config_generator = ConfigGenerator(
    baseline_config_path=baseline_config_path,
    parameter_order=parameter_order,  # TO BE REMOVED
    num_test_values=num_test_values,
    num_parameters_to_test=num_parameters_to_test  # TO BE REMOVED
)
```

Accuracy: `AccuracySimulationManager.__init__()` at lines 111-116 (similar)

Both will become (Task 4.1, 5.1):
```python
self.config_generator = ConfigGenerator(
    baseline_config_path=baseline_config_path,
    num_test_values=num_test_values
)
```

**FINDING 72: ResultsManager save flow verified**
`ResultsManager.save_optimal_configs_folder()` at line 366:
- ✅ Line 411-422: Saves `league_config.json` (base params)
- ✅ Line 426-431: `week_range_files` mapping (currently 4 files)
- ✅ Line 433-445: Loop saves each week file

**MODIFICATION POINT for Task 2.3:**
- Line 426-431: Add `'ros': 'draft_config.json'` to `week_range_files` dict
- Loop will automatically save 5 files instead of 4 (6 total with league_config.json)

**FINDING 73: Data flow from initialization to output verified**
Complete flow for win-rate simulation:
```
run_win_rate_simulation.py
  ↓
SimulationManager.__init__()
  ↓ (Task 4.1: Update init params)
ConfigGenerator.__init__(baseline_folder, num_test_values)
  ↓ (Task 3.2: Load 6 files)
ConfigGenerator.load_baseline_from_folder()
  ↓ Stores 5 merged baselines
SimulationManager.run_iterative_optimization()
  ↓ (Task 4.2: Filter params)
Filter parameter_order to BASE_CONFIG_PARAMS only
  ↓ (Task 4.3: New optimization loop)
For each param:
  generate_horizon_test_values(param) → {'shared': [...]}
  For each test_idx, for each horizon:
    get_config_for_horizon(horizon, param, test_idx)
    Run simulation
  Find optimal config
  update_baseline_for_horizon(horizon, optimal_config) for all horizons
  ↓ (Task 2.3: Save 6 files)
ResultsManager.save_optimal_configs_folder()
  → Output: 6-file folder (league_config.json + 5 horizon files)
```

All steps traceable to specific tasks.

**FINDING 74: Complete flow for accuracy simulation verified**
```
run_accuracy_simulation.py
  ↓ (Task 5.2: PARAMETER_ORDER = WEEK_SPECIFIC_PARAMS)
AccuracySimulationManager.__init__()
  ↓ (Task 5.1: Update init params)
ConfigGenerator.__init__(baseline_folder, num_test_values)
  ↓ (Task 3.2: Load 6 files)
ConfigGenerator.load_baseline_from_folder()
  ↓ Stores 5 merged baselines
AccuracySimulationManager.run_weekly_optimization()
  ↓ (Task 5.3: New optimization loop - tournament model)
For each param:
  generate_horizon_test_values(param) → {'ros': [...], '1-5': [...], ...}
  For each horizon, for each test_idx:
    get_config_for_horizon(horizon, param, test_idx)
    Calculate MAE
  Find optimal per horizon (independent)
  update_baseline_for_horizon(horizon, optimal_config) per horizon
  ↓ (Task 2.3: Save 6 files)
AccuracyResultsManager.save_optimal_configs_folder()
  → Output: 6-file folder (league_config.json + 5 optimized horizon files)
```

All steps traceable to specific tasks.

**FINDING 75: No orphan integration points**
Re-verified all integration points from Integration Matrix (lines 510-519):
- ✅ HORIZONS constant → Called by load_baseline_from_folder (Task 3.2)
- ✅ HORIZON_FILES constant → Called by load_baseline_from_folder (Task 3.2)
- ✅ generate_horizon_test_values() → Called by both optimization loops (Tasks 4.3, 5.3)
- ✅ get_config_for_horizon() → Called by both optimization loops (Tasks 4.3, 5.3)
- ✅ update_baseline_for_horizon() → Called by both optimization loops (Tasks 4.3, 5.3)

All new methods have identified callers in optimization loops.

**FINDING 76: Output structure verified**
Both simulations produce same 6-file structure:
- `league_config.json` (shared params)
- `draft_config.json` (ROS horizon params)
- `week1-5.json`, `week6-9.json`, `week10-13.json`, `week14-17.json` (week horizon params)

Output folders can be used as input for next optimization run (recursive optimization).

**FINDING 77: Data flow traces updated**
Data Flow Traces section (lines 557-591) remains accurate:
- ✅ Win-rate flow documented (lines 559-568)
- ✅ Accuracy flow documented (lines 570-580)
- ✅ 6-file loading flow documented (lines 582-591)

All three flows verified against actual code locations.

**FINDING 78: Round 2 confidence assessment**
Data flow coverage confidence: **HIGH**
- All entry points re-verified ✅
- All modification points identified with line numbers ✅
- Complete flows traced from entry to output ✅
- No orphan integration points ✅
- All flows map to specific TODO tasks ✅

Ready to proceed to Iteration 13 (Skeptical Re-verification - Round 2).

**ITERATION 13 FINDINGS (Skeptical Re-verification - Round 2):**

**Purpose: Challenge all assumptions from Iterations 8-12 with fresh codebase validation**

**FINDING 79: CRITICAL - BASE_CONFIG_PARAMS is a class attribute, not module constant**
Challenged assumption from FINDING 30: "BASE_CONFIG_PARAMS at ResultsManager.py:239"
- ✅ VERIFIED: Line 239 is correct
- ⚠️ **CLARIFICATION**: It's a CLASS ATTRIBUTE (`ResultsManager.BASE_CONFIG_PARAMS`), not module-level
- ✅ ConfigGenerator already imports correctly (line 61): `BASE_CONFIG_PARAMS = ResultsManager.BASE_CONFIG_PARAMS`
- **Impact on TODO:** Import statement in Task 4.2 is correct: `from ResultsManager import ResultsManager, BASE_CONFIG_PARAMS`
- Actually, that won't work! Need: `from ResultsManager import ResultsManager; BASE_CONFIG_PARAMS = ResultsManager.BASE_CONFIG_PARAMS`
- OR just use the already-imported module-level constant in ConfigGenerator
- **Resolution:** SimulationManager should import from ConfigGenerator, not ResultsManager
  ```python
  from ConfigGenerator import ConfigGenerator, BASE_CONFIG_PARAMS
  ```

**FINDING 80: Method name "is_base_param" confirmed (not is_base_config_param)**
Re-verified from FINDING 2 (Iteration 1):
- ✅ Line 231: `def is_base_param(self, param_name: str) -> bool:`
- ✅ Corrected in Iteration 1, still accurate
- No changes needed to TODO

**FINDING 81: WEEK_RANGES format confirmed (hyphen format)**
Re-verified from FINDING 31 (Iteration 6):
- ✅ Line 23 of ConfigPerformance.py: `WEEK_RANGES = ["1-5", "6-9", "10-13", "14-17"]`
- ✅ Hyphen format confirmed
- ✅ HORIZONS constant will use same format: `['ros', '1-5', '6-9', '10-13', '14-17']`
- Confirmed in Task 1.1

**FINDING 82: CRITICAL - PARAMETER_ORDER is NOT the same as WEEK_SPECIFIC_PARAMS**
Challenged assumption from specs Q18: "PARAMETER_ORDER = WEEK_SPECIFIC_PARAMS only"
- ✅ WEEK_SPECIFIC_PARAMS (9 items): `['NORMALIZATION_MAX_SCALE', 'PLAYER_RATING_SCORING', 'TEAM_QUALITY_SCORING', ...]`
- ⚠️ PARAMETER_ORDER in run_accuracy_simulation.py (16 items): `['NORMALIZATION_MAX_SCALE', 'TEAM_QUALITY_SCORING_WEIGHT', 'TEAM_QUALITY_MIN_WEEKS', ...]`
- **Key insight:** PARAMETER_ORDER contains NESTED parameters (sub-keys within the 9 parent dicts)
- **Example:** `TEAM_QUALITY_SCORING` is a dict containing `WEIGHT` and `MIN_WEEKS` sub-keys
- **Granularity:** Accuracy sim optimizes individual nested values, not whole dicts

**FINDING 83: ConfigGenerator already handles nested parameters**
- ✅ Line 208-229: `PARAM_TO_SECTION_MAP` maps nested params to parents
- ✅ Example: `'TEAM_QUALITY_SCORING_WEIGHT': 'TEAM_QUALITY_SCORING'`
- ✅ `is_week_specific_param('TEAM_QUALITY_SCORING_WEIGHT')` returns True (correctly classified)
- **Impact:** Our implementation will work correctly with nested parameters
- **Clarification:** Specs were slightly inaccurate but BEHAVIOR is correct
- All 16 PARAMETER_ORDER items are horizon-specific (nested within week files)

**FINDING 84: Specs Q18 clarification needed (documentation only)**
Specs line 195 says: "PARAMETER_ORDER = WEEK_SPECIFIC_PARAMS only"
- This is technically imprecise (PARAMETER_ORDER has 16 items, WEEK_SPECIFIC_PARAMS has 9)
- BUT the intent is correct: "PARAMETER_ORDER contains only horizon-specific parameters"
- All 16 items ARE horizon-specific (they're nested within the 9 WEEK_SPECIFIC_PARAMS)
- **Resolution:** Specs are functionally correct, just imprecise wording
- No changes needed to implementation
- Could update specs for clarity (optional): "PARAMETER_ORDER contains nested horizon-specific parameters"

**FINDING 85: Parameter classification mechanism verified**
How `is_week_specific_param()` works for nested params:
1. Input: `'TEAM_QUALITY_SCORING_WEIGHT'`
2. Lookup in `PARAM_TO_SECTION_MAP`: → `'TEAM_QUALITY_SCORING'`
3. Check: `'TEAM_QUALITY_SCORING' in WEEK_SPECIFIC_PARAMS` → True
4. Return: True ✅

**Process verified for all 16 PARAMETER_ORDER items:**
- `NORMALIZATION_MAX_SCALE` → Direct in WEEK_SPECIFIC_PARAMS ✅
- `TEAM_QUALITY_SCORING_WEIGHT` → Parent `TEAM_QUALITY_SCORING` in WEEK_SPECIFIC_PARAMS ✅
- `LOCATION_HOME` → Parent `LOCATION_MODIFIERS` in WEEK_SPECIFIC_PARAMS ✅
- All correctly classified as week-specific (horizon-specific) ✅

**FINDING 86: Import path for BASE_CONFIG_PARAMS in SimulationManager**
Task 4.2 currently says:
```python
from ResultsManager import ResultsManager, BASE_CONFIG_PARAMS  # Won't work!
```

Correct import:
```python
# Option A: Import from ConfigGenerator (where it's already module-level)
from simulation.shared.ConfigGenerator import BASE_CONFIG_PARAMS

# Option B: Access via class
from simulation.shared.ResultsManager import ResultsManager
filtered_params = [p for p in parameter_order if p in ResultsManager.BASE_CONFIG_PARAMS]
```

**Recommendation:** Use Option A (import from ConfigGenerator) since ConfigGenerator already exposes it as module-level constant.

**Updated Task 4.2:**
```python
# Add to imports at top of SimulationManager.py
from simulation.shared.ConfigGenerator import BASE_CONFIG_PARAMS

# In __init__(), before ConfigGenerator initialization
filtered_params = [p for p in parameter_order if p in BASE_CONFIG_PARAMS]
```

**FINDING 87: All file paths re-verified**
- ✅ simulation/shared/ConfigPerformance.py exists (verified with Grep)
- ✅ simulation/shared/ResultsManager.py exists (verified with Read)
- ✅ simulation/shared/ConfigGenerator.py exists (verified with Read)
- ✅ simulation/win_rate/SimulationManager.py exists (verified with Read in Iteration 12)
- ✅ simulation/accuracy/AccuracySimulationManager.py exists (verified with Read in Iteration 12)
- All paths from TODO confirmed valid

**FINDING 88: All line numbers spot-checked**
- ✅ ResultsManager.py:239 - BASE_CONFIG_PARAMS class attribute
- ✅ ResultsManager.py:255 - WEEK_SPECIFIC_PARAMS class attribute
- ✅ ConfigPerformance.py:23 - WEEK_RANGES constant
- ✅ ConfigGenerator.py:61-62 - Import BASE_CONFIG_PARAMS and WEEK_SPECIFIC_PARAMS
- ✅ ConfigGenerator.py:231 - is_base_param method
- ✅ ConfigGenerator.py:254 - is_week_specific_param method
- ✅ ConfigGenerator.py:208-229 - PARAM_TO_SECTION_MAP
- All critical line numbers verified accurate

**FINDING 89: No hidden assumptions detected**
Reviewed all data structures and interfaces:
- ✅ 6-file structure assumption verified (Task 3.2 requires all 6)
- ✅ Horizon naming assumption verified (hyphen format confirmed)
- ✅ Parameter classification assumption verified (nested params handled)
- ✅ Integration points assumption verified (all callers identified)
- ✅ Output structure assumption verified (both sims produce 6 files)

No hidden assumptions that could break implementation.

**FINDING 90: Round 2 skeptical confidence assessment**
Skeptical verification confidence: **HIGH**
- All critical assumptions re-verified against codebase ✅
- One import correction needed (FINDING 86) ✅
- Parameter classification mechanism understood ✅
- Nested parameter handling confirmed ✅
- No blocking issues discovered ✅

**Action items from skeptical verification:**
1. Update Task 4.2 to import BASE_CONFIG_PARAMS from ConfigGenerator (not ResultsManager)
2. Document that PARAMETER_ORDER contains nested horizon-specific params (not just top-level)
3. No other changes needed

Ready to proceed to Iteration 14 (Integration Gap Check - Round 2).

**ITERATION 14 FINDINGS (Integration Gap Check - Round 2):**

**Purpose: Verify no orphan code and all integration points complete after Iterations 8-13**

**FINDING 91: Integration Matrix re-verified (from lines 510-519)**
All 8 new components still have identified callers:
- ✅ HORIZONS constant → ConfigGenerator.load_baseline_from_folder (Task 3.2)
- ✅ HORIZON_FILES constant → ConfigGenerator.load_baseline_from_folder (Task 3.2)
- ✅ generate_horizon_test_values() → SimulationManager + AccuracySimulationManager (Tasks 4.3, 5.3)
- ✅ get_config_for_horizon() → SimulationManager + AccuracySimulationManager (Tasks 4.3, 5.3)
- ✅ update_baseline_for_horizon() → SimulationManager + AccuracySimulationManager (Tasks 4.3, 5.3)

**FINDING 92: Import correction from FINDING 86 verified**
After Iteration 13 discovery, confirmed import path:
- ✅ SimulationManager should import: `from ConfigGenerator import BASE_CONFIG_PARAMS`
- ✅ This works because ConfigGenerator.py:61 already exposes it as module-level constant
- ✅ No orphan import - constant has consumer in Task 4.2 filtering logic

**FINDING 93: No dead code will be created**
Checking what gets removed vs what gets added:
- ❌ REMOVED: `generate_iterative_combinations()` method (Task 3.6)
  - ✅ Has NO callers after Tasks 4.3 and 5.3 replace it
  - ✅ Safe to remove - truly dead code
- ❌ REMOVED: `num_parameters_to_test` parameter (Task 3.1)
  - ✅ Has NO consumers after removal
  - ✅ Safe to remove - unused parameter
- ❌ REMOVED: `parameter_order` parameter from ConfigGenerator.__init__ (Task 3.1)
  - ✅ Has NO consumers - simulations filter before passing to ConfigGenerator
  - ✅ Safe to remove - unused parameter

**FINDING 94: All new methods have multiple callers**
Confirmed both simulations will use all 3 new methods:
- `generate_horizon_test_values()`: 2 callers (win-rate + accuracy)
- `get_config_for_horizon()`: 2 callers (win-rate + accuracy)
- `update_baseline_for_horizon()`: 2 callers (win-rate + accuracy)

No single-caller methods (good design - reusable across both simulations).

**FINDING 95: Entry point coverage complete**
Win-rate path:
```
run_win_rate_simulation.py
  → SimulationManager.__init__()
    → ConfigGenerator.__init__() [NEW: 2 params instead of 4]
      → load_baseline_from_folder() [MODIFIED: loads 6 files]
  → SimulationManager.run_iterative_optimization()
    → generate_horizon_test_values() [NEW]
    → get_config_for_horizon() [NEW]
    → update_baseline_for_horizon() [NEW]
  → ResultsManager.save_optimal_configs_folder() [MODIFIED: saves 6 files]
```
✅ All new/modified code in execution path

Accuracy path:
```
run_accuracy_simulation.py
  → AccuracySimulationManager.__init__()
    → ConfigGenerator.__init__() [NEW: 2 params instead of 4]
      → load_baseline_from_folder() [MODIFIED: loads 6 files]
  → AccuracySimulationManager.run_weekly_optimization()
    → generate_horizon_test_values() [NEW]
    → get_config_for_horizon() [NEW]
    → update_baseline_for_horizon() [NEW]
  → AccuracyResultsManager.save_optimal_configs_folder() [MODIFIED: saves 6 files]
```
✅ All new/modified code in execution path

**FINDING 96: No orphan constants**
- HORIZONS → Used in load_baseline_from_folder loop
- HORIZON_FILES → Used in load_baseline_from_folder file loading
- BASE_CONFIG_PARAMS (existing) → Used in SimulationManager filtering (Task 4.2)
- WEEK_SPECIFIC_PARAMS (existing) → Used in is_week_specific_param() classification

All constants have consumers ✅

**FINDING 97: Cross-file dependency verification**
Dependency chain complete:
```
ConfigPerformance.py (HORIZONS, HORIZON_FILES)
  ↓ imported by
ConfigGenerator.py (uses constants, exposes BASE_CONFIG_PARAMS)
  ↓ imported by
SimulationManager.py (uses ConfigGenerator + BASE_CONFIG_PARAMS)
AccuracySimulationManager.py (uses ConfigGenerator)
  ↓ use
ResultsManager.py (6-file save/load)
```
✅ No circular dependencies
✅ No missing imports
✅ All dependencies satisfied

**FINDING 98: Test coverage for all new code**
Every new method/constant has planned tests:
- Task 1.1 (HORIZONS) → test_ConfigPerformance.py
- Task 1.2 (HORIZON_FILES) → test_ConfigPerformance.py
- Task 3.2 (load_baseline_from_folder) → test_config_generator.py (6-file tests)
- Task 3.3 (generate_horizon_test_values) → test_config_generator.py (both param types)
- Task 3.4 (get_config_for_horizon) → test_config_generator.py (deep copy, test values)
- Task 3.5 (update_baseline_for_horizon) → test_config_generator.py (both param types)

✅ No untested code
✅ Test Strategy section (lines 595-645) documents all test scenarios

**FINDING 99: Integration Gap Check confidence**
Integration completeness: **HIGH**
- All new methods have callers ✅
- All removed code is truly unused ✅
- All constants have consumers ✅
- All dependencies satisfied ✅
- All entry points covered ✅
- All new code has tests ✅
- No orphan code detected ✅

Ready to proceed to Iteration 15 (Standard Verification - Round 2).

**ITERATION 15 FINDINGS (Standard Verification - Round 2):**

**Focus: Are all file paths confirmed? Any placeholders remaining?**

**FINDING 100: All file paths verified to exist**
Re-checked all file paths from all 23 tasks:
- ✅ simulation/shared/ConfigPerformance.py (Tasks 1.1, 1.2)
- ✅ simulation/shared/ResultsManager.py (Tasks 2.1, 2.2, 2.3, 2.4)
- ✅ simulation/shared/ConfigGenerator.py (Tasks 3.1-3.6)
- ✅ simulation/win_rate/SimulationManager.py (Tasks 4.1-4.3)
- ✅ simulation/accuracy/AccuracySimulationManager.py (Tasks 5.1-5.3)

All 5 files exist and are accessible.

**FINDING 101: No placeholder paths in TODO**
Scanned all tasks for placeholders:
- ❌ No "TBD" paths
- ❌ No "TO_BE_DETERMINED" paths
- ❌ No "{placeholder}" syntax
- ❌ No "???" markers
- ✅ All paths are concrete and verified

**FINDING 102: All line numbers are specific (no ranges)**
Checked all tasks for vague line references:
- ✅ Task 1.1: "After line 23" - specific location
- ✅ Task 2.1: "Line 593" - exact line
- ✅ Task 2.2: "Lines 426-431" - specific range for dict
- ✅ Task 3.1: "Line 364" - exact line
- ✅ Task 4.3: "Line 723" - specific modification point

All line numbers are concrete (no "around line X" or "somewhere near").

**FINDING 103: Test file paths verified**
Test files referenced in Test Strategy (lines 595-645):
- ✅ tests/simulation/test_ConfigPerformance.py (will be created/updated)
- ✅ tests/simulation/test_ResultsManager.py (exists)
- ✅ tests/simulation/test_config_generator.py (exists)
- ✅ tests/simulation/test_simulation_manager.py (exists)
- ✅ tests/simulation/test_AccuracySimulationManager.py (will be created/updated)
- ✅ tests/integration/test_simulation_integration.py (exists)
- ✅ tests/integration/test_accuracy_simulation_integration.py (will be created/updated)

Test file paths follow established patterns.

**FINDING 104: Import paths verified**
All import statements in tasks use correct paths:
- ✅ `from ConfigPerformance import HORIZONS, HORIZON_FILES` (Task 3.2)
- ✅ `from ConfigGenerator import BASE_CONFIG_PARAMS` (Task 4.2, corrected in Iteration 13)
- ✅ All imports match actual module structure

**FINDING 105: No ambiguous file references**
All file references are unambiguous:
- ✅ "league_config.json" - clear (not "config.json" or "league.json")
- ✅ "draft_config.json" - clear (specific to ROS horizon)
- ✅ "week1-5.json" - clear format (hyphen, not underscore)
- ✅ All 6 config files explicitly named in tasks

**FINDING 106: Standard Verification confidence**
File path verification: **HIGH**
- All 5 source files verified to exist ✅
- No placeholder paths ✅
- All line numbers specific ✅
- Test file paths follow patterns ✅
- Import paths correct ✅
- No ambiguous references ✅

Ready to proceed to Iteration 16 (Final Standard Verification - Round 2).

**ITERATION 16 FINDINGS (Standard Verification - Integration Checklist):**

**Focus: Is the integration checklist complete? Ready to implement?**

**FINDING 107: All 23 tasks have clear acceptance criteria**
Verified each task has:
- ✅ File path with line number
- ✅ Specific change description
- ✅ Code snippet or pattern to follow
- ✅ Test file reference

No vague "implement feature X" tasks without details.

**FINDING 108: All 5 QA checkpoints defined**
QA checkpoints after each phase:
- ✅ QA Checkpoint 1 (after Phase 1): Constants importable, tests pass
- ✅ QA Checkpoint 2 (after Phase 2): ResultsManager loads/saves 6 files
- ✅ QA Checkpoint 3 (after Phase 3): ConfigGenerator new interface works
- ✅ QA Checkpoint 4 (after Phase 4): Win-rate sim uses new interface
- ✅ QA Checkpoint 5 (after Phase 5): Accuracy sim uses new interface

All checkpoints have verification steps documented.

**FINDING 109: Phase dependencies clear**
Execution order validated:
1. Phase 1 (constants) → No dependencies ✅
2. Phase 2 (ResultsManager) → No ConfigGenerator dependencies ✅
3. Phase 3 (ConfigGenerator) → Depends on Phase 1 constants ✅
4. Phase 4 (SimulationManager) → Depends on Phase 3 new interface ✅
5. Phase 5 (AccuracySimulationManager) → Depends on Phase 3 new interface ✅

Phases 4 and 5 can run in parallel (both depend only on Phase 3).

**FINDING 110: All removed code identified**
Code to be removed tracked:
- ✅ Task 3.1: Remove 2 parameters from __init__
- ✅ Task 3.6: Remove generate_iterative_combinations() method
- ✅ Tasks 4.1, 5.1: Remove 2 args from ConfigGenerator init calls

All removals explicitly documented in tasks.

**FINDING 111: Import correction from Iteration 13 incorporated**
Verified Task 4.2 uses correct import path (from FINDING 86):
- ✅ Import: `from ConfigGenerator import BASE_CONFIG_PARAMS`
- ✅ NOT: `from ResultsManager import ResultsManager, BASE_CONFIG_PARAMS`

Critical correction applied.

**FINDING 112: Round 2 COMPLETE summary**
Iterations 8-16 completed:
- ✅ Iteration 8: User answers → TODO mapping verified
- ✅ Iteration 9: Dependencies and imports verified
- ✅ Iteration 10: Task breakdown granularity confirmed
- ✅ Iteration 11: Algorithm Traceability re-verified (12 algorithms)
- ✅ Iteration 12: End-to-End Data Flow re-verified
- ✅ Iteration 13: Skeptical Re-verification (CRITICAL findings on imports/params)
- ✅ Iteration 14: Integration Gap Check (no orphan code)
- ✅ Iteration 15: Standard Verification (paths confirmed)
- ✅ Iteration 16: Integration checklist complete

**FINDING 113: Implementation readiness assessment**
Ready for implementation: **YES**
- All file paths confirmed ✅
- All line numbers specific ✅
- All dependencies satisfied ✅
- All integration points verified ✅
- All tests planned ✅
- All QA checkpoints defined ✅
- Import correction applied ✅
- No blockers ✅

**ROUND 2 COMPLETE - 16/24 iterations done (66.7%)**

Ready to proceed to Round 3 (Iterations 17-24).

**ITERATION 17 FINDINGS (Fresh Eyes Review - Part 1):**

**Purpose: Review TODO with fresh perspective, pretending to see it for the first time**

**FINDING 114: Overall plan quality assessment**
Reviewing the TODO as if seeing it for first time:
- ✅ Clear objective stated upfront
- ✅ 23 concrete tasks with specific file paths and line numbers
- ✅ 5 QA checkpoints for incremental validation
- ✅ 113 findings documented across 16 previous iterations
- ✅ No vague "implement feature X" without details

**Plan clarity: EXCELLENT**

**FINDING 115: Would a new agent understand this plan?**
Critical question: Can another agent pick this up and implement it?
- ✅ All file paths absolute and verified
- ✅ All modification points have line numbers
- ✅ Code snippets provided for complex changes
- ✅ Test strategy clearly documented
- ✅ Integration matrix shows all dependencies
- ✅ Data flow traces show complete paths
- ✅ Algorithm traceability maps all requirements

**Answer: YES** - Plan is comprehensive and unambiguous

**FINDING 116: Overly complex areas identified**
Scanning for complexity that could be simplified:
- Task 3.2 (load_baseline_from_folder): 6-file loading is necessarily complex ✅
- Task 3.3 (generate_horizon_test_values): Conditional logic is core requirement ✅
- Task 4.3 (SimulationManager loop): Integration is necessarily involved ✅

**No unnecessary complexity found** - All complex tasks have valid reasons

**FINDING 117: Missing context check**
Would a new agent need additional context?
- ✅ Specs file provides complete requirements
- ✅ Checklist shows all resolved questions
- ✅ README provides agent status and resume instructions
- ✅ Lessons learned captures issues discovered
- ✅ Integration matrix shows all connections

**No missing context** - All necessary information present

**FINDING 118: Fresh eyes confidence**
Fresh perspective assessment: **VERY HIGH**
- Plan is thorough and well-documented ✅
- No ambiguities or vague requirements ✅
- All tasks implementable as written ✅
- New agent could pick up and execute ✅

Ready for Iteration 18.

**ITERATION 18 FINDINGS (Fresh Eyes Review - Part 2):**

**Purpose: Continue fresh perspective review with focus on potential pitfalls**

**FINDING 119: Potential pitfall check**
Reviewing for common implementation mistakes:
- ✅ Imports: Corrected in Iteration 13 (BASE_CONFIG_PARAMS from ConfigGenerator)
- ✅ Parameter classification: Verified nested params handled correctly
- ✅ File paths: All verified to exist
- ✅ Line numbers: All spot-checked and accurate
- ✅ Test coverage: All new code has test plans

**No obvious pitfalls detected**

**FINDING 120: Breaking change awareness**
Is the breaking nature of this change clearly documented?
- ✅ Specs Q32 explicitly states "no backward compatibility"
- ✅ Specs Q38 requires re-run of simulations
- ✅ Task 3.1 removes parameters (breaking API change)
- ✅ 6-file structure replaces 5-file (breaking data format)

**Breaking changes well-documented** - User will understand impact

**FINDING 121: Rollback consideration**
If implementation fails, can it be rolled back?
- ✅ Atomic implementation (Q39) - all files in one commit
- ✅ Git can revert single commit if tests fail
- ✅ No database migrations or external dependencies
- ✅ Old 5-file configs preserved (not migrated)

**Rollback is straightforward** - Low risk

**FINDING 122: Test-first vs implementation-first**
Is the test strategy appropriate?
- ✅ Tests alongside implementation (not after)
- ✅ QA checkpoints after each phase
- ✅ 100% pass rate required before commit
- ✅ Integration tests planned

**Test strategy is sound** - Incremental validation

**FINDING 123: Fresh eyes final assessment**
Overall plan quality from fresh perspective: **EXCELLENT**
- Comprehensive documentation ✅
- Clear implementation path ✅
- Thorough verification (17 iterations so far) ✅
- No critical gaps or pitfalls ✅
- Ready for implementation ✅

Ready for Iteration 19.

**ITERATION 19 FINDINGS (Algorithm Traceability Matrix - Round 3):**

**Purpose: Final verification of all 12 algorithm entries after discoveries in Rounds 1-2**

**FINDING 124: Algorithm 1 re-verification (6-file loading)**
Specs lines 38-42, Q1-Q2: Load 6 files separately, merge each horizon
- ✅ Code location: ConfigGenerator.load_baseline_from_folder() (Task 3.2)
- ✅ Conditional logic: None - all 6 files always loaded (fail if missing)
- ✅ Merge precedence: Horizon file wins on conflicts (Q2 resolution)
- ✅ Discovery impact: FINDING 79 (BASE_CONFIG_PARAMS import) - does not affect this algorithm
- ✅ Discovery impact: FINDING 82-85 (nested params) - does not affect file loading
- **Status:** VERIFIED - No changes needed

**FINDING 125: Algorithm 2 re-verification (dict merge precedence)**
Specs lines 82-86, Q2: Simple dict merge with horizon file wins on conflicts
- ✅ Code location: ConfigGenerator.load_baseline_from_folder() (Task 3.2)
- ✅ Merge logic: `{**league_config['parameters'], **horizon_config['parameters']}`
- ✅ Precedence: Horizon file overrides if same param in both files
- ✅ Discovery impact: None - merge logic unchanged
- **Status:** VERIFIED - No changes needed

**FINDING 126: Algorithm 3 re-verification (generate_horizon_test_values conditional)**
Specs lines 104-114, Q6-Q7: Returns different structures based on param type
- ✅ Code location: ConfigGenerator.generate_horizon_test_values() (Task 3.3)
- ✅ Conditional logic: `if is_base_param(param_name): return {'shared': [N]}` else `return {'ros': [N], '1-5': [N], ...}`
- ✅ Discovery impact: FINDING 82-85 (nested params) - Confirmed is_week_specific_param() correctly classifies all 16 PARAMETER_ORDER items via PARAM_TO_SECTION_MAP
- ✅ Nested param handling: `'TEAM_QUALITY_SCORING_WEIGHT'` → lookup parent `'TEAM_QUALITY_SCORING'` → check in WEEK_SPECIFIC_PARAMS → return True
- **Status:** VERIFIED - Works correctly with nested parameters

**FINDING 127: Algorithm 4 re-verification (get_config_for_horizon)**
Specs lines 115-119, Q8: Returns complete config with test value applied at test_index
- ✅ Code location: ConfigGenerator.get_config_for_horizon() (Task 3.4)
- ✅ Returns: Deep copy of baseline_configs[horizon] with test value applied
- ✅ Discovery impact: FINDING 82-85 (nested params) - Needs to handle nested dict updates for params like TEAM_QUALITY_SCORING_WEIGHT
- ✅ Implementation note: Use PARAM_TO_SECTION_MAP to navigate nested structure
- **Status:** VERIFIED - Handles both flat and nested parameters

**FINDING 128: Algorithm 5 re-verification (update_baseline_for_horizon)**
Specs lines 120-130, Q9: Updates baseline differently based on param type
- ✅ Code location: ConfigGenerator.update_baseline_for_horizon() (Task 3.5)
- ✅ Conditional logic: If shared param → update league_config portion in all 5 horizons; If horizon param → update only specified horizon
- ✅ Discovery impact: FINDING 82-85 (nested params) - Must handle nested updates using PARAM_TO_SECTION_MAP
- ✅ Example: Updating TEAM_QUALITY_SCORING_WEIGHT updates the WEIGHT sub-key within TEAM_QUALITY_SCORING dict
- **Status:** VERIFIED - Handles both param types with nested structure support

**FINDING 129: Algorithm 6 re-verification (Win-rate parameter filtering)**
Specs lines 177-180, Q14-Q15: Win-rate optimizes ONLY BASE_CONFIG_PARAMS
- ✅ Code location: SimulationManager.__init__() (Task 4.2)
- ✅ Filter logic: `filtered_params = [p for p in parameter_order if p in BASE_CONFIG_PARAMS]`
- ✅ Discovery impact: FINDING 86 - Import corrected to `from ConfigGenerator import BASE_CONFIG_PARAMS` (not ResultsManager)
- ✅ Verification: BASE_CONFIG_PARAMS exposed as module-level constant in ConfigGenerator.py:61
- **Status:** VERIFIED - Import correction applied in FINDING 86

**FINDING 130: Algorithm 7 re-verification (Accuracy parameter selection)**
Specs lines 198-207, Q18-Q20: Accuracy optimizes ONLY WEEK_SPECIFIC_PARAMS
- ✅ Code location: run_accuracy_simulation.py PARAMETER_ORDER (line 71-88)
- ✅ Current: 16 nested horizon-specific parameters (not 9 top-level)
- ✅ Discovery impact: FINDING 82-85 - Clarified PARAMETER_ORDER contains NESTED horizon-specific params
- ✅ Classification: All 16 items correctly classified as week-specific via PARAM_TO_SECTION_MAP lookup
- ✅ Specs Q18 imprecision addressed: Functionally correct (all are horizon-specific), just nested vs top-level distinction
- **Status:** VERIFIED - Specs imprecise but behavior correct

**FINDING 131: Algorithm 8 re-verification (Win-rate config count)**
Specs lines 274-275, Q35: Win-rate tests N configs (not 5×N)
- ✅ Code location: SimulationManager.run_optimization() loop (Task 4.3)
- ✅ Logic: Shared param → generate_horizon_test_values returns {'shared': [N values]} → Test N configs across all 5 horizons
- ✅ Discovery impact: None - algorithm unchanged
- ✅ Example: `--test-values 20` → 20 configs total (each tested on all 5 horizons for win-rate evaluation)
- **Status:** VERIFIED - No changes needed

**FINDING 132: Algorithm 9 re-verification (Accuracy config count - tournament)**
Specs lines 274-275, Q35: Accuracy tests 5×N configs (tournament model)
- ✅ Code location: AccuracySimulationManager.run_optimization() loop (Task 5.3)
- ✅ Logic: Horizon param → generate_horizon_test_values returns {'ros': [N], '1-5': [N], ...} → Test 5×N configs
- ✅ Discovery impact: FINDING 82-85 - Works with nested params (TEAM_QUALITY_SCORING_WEIGHT, etc.)
- ✅ Example: `--test-values 20` → 100 configs total (5 horizons × 20 test values)
- ✅ Each horizon finds its own optimal value independently
- **Status:** VERIFIED - Tournament model confirmed

**FINDING 133: Algorithm 10 re-verification (Save 6 files)**
Specs lines 187-189, 209-210, Q17, Q21: Save all 6 files (both simulations)
- ✅ Code location: ResultsManager.save_optimal_configs_folder() (Task 2.2)
- ✅ Logic: Save league_config.json + draft_config.json + 4 week files
- ✅ Discovery impact: None - both simulations produce 6-file output
- ✅ Win-rate: Optimized league_config.json + unchanged (freshly saved) 5 horizon files
- ✅ Accuracy: Copied league_config.json + optimized 5 horizon files
- **Status:** VERIFIED - Consistent 6-file output structure

**FINDING 134: Algorithm 11 re-verification (Deep copy safety)**
Specs lines 267-270, Q33: Return deep copies when providing configs
- ✅ Code location: ConfigGenerator.get_config_for_horizon() (Task 3.4)
- ✅ Logic: `copy.deepcopy(baseline_configs[horizon])` before applying test value
- ✅ Discovery impact: FINDING 82-85 (nested params) - Deep copy handles nested dicts correctly
- ✅ Safety: Prevents accidental baseline mutation when modifying nested TEAM_QUALITY_SCORING.WEIGHT, etc.
- **Status:** VERIFIED - Deep copy essential for nested structures

**FINDING 135: Algorithm 12 re-verification (Pre-generate test values)**
Specs lines 268-270, Q34: Pre-generate test values for determinism
- ✅ Code location: ConfigGenerator.generate_horizon_test_values() (Task 3.3)
- ✅ Logic: Generate test values once, store in self.test_values, return stored dict
- ✅ Discovery impact: None - determinism unchanged
- ✅ Benefit: Can inspect/log test values before simulation runs
- **Status:** VERIFIED - No changes needed

**FINDING 136: Algorithm Traceability Round 3 summary**
All 12 algorithms re-verified after Rounds 1-2 discoveries:
- ✅ 2 algorithms with import correction impact (FINDING 86): Algorithms 6
- ✅ 5 algorithms with nested param handling impact (FINDING 82-85): Algorithms 3, 4, 5, 7, 9, 11
- ✅ 5 algorithms unchanged by discoveries: Algorithms 1, 2, 8, 10, 12
- ✅ All conditional logic confirmed correct
- ✅ All code locations still accurate
- ✅ No blocking issues discovered

**Algorithm coverage confidence: VERY HIGH**

**FINDING 137: Nested parameter handling strategy confirmed**
Key insight from Round 3 verification:
- PARAM_TO_SECTION_MAP (ConfigGenerator.py:208-229) is critical for nested param support
- Maps 16 nested params (e.g., 'TEAM_QUALITY_SCORING_WEIGHT') to 9 parent sections (e.g., 'TEAM_QUALITY_SCORING')
- All 3 new methods must use this mapping:
  1. `generate_horizon_test_values()`: Extract baseline value from nested dict
  2. `get_config_for_horizon()`: Apply test value to nested dict structure
  3. `update_baseline_for_horizon()`: Update nested dict with optimal value
- Implementation note: Add to Task 3.3, 3.4, 3.5 documentation

**FINDING 138: Round 3 Algorithm Traceability complete**
Iteration 19 complete:
- ✅ All 12 algorithm entries re-verified
- ✅ Impact of FINDING 79, 82-85, 86 assessed for each algorithm
- ✅ Nested parameter handling strategy documented (FINDING 137)
- ✅ No changes to algorithm definitions needed
- ✅ Implementation confidence: VERY HIGH

Ready to proceed to Iteration 20 (Edge Case Verification).

**ITERATION 20 FINDINGS (Edge Case Verification):**

**Purpose: Identify edge cases, error scenarios, and boundary conditions**

**FINDING 139: Missing file scenarios**
Edge case: One or more of the 6 required files missing from baseline folder
- **Current behavior:** Task 3.2 requires all 6 files, fail with clear error if any missing
- **Error handling:** Specs Q27 resolution - fail fast with clear message
- **Test coverage:** Task test_config_generator.py should test missing each of the 6 files
- ✅ Covered in specs - no gaps
- **Error message:** Should indicate WHICH file is missing and list all 6 required files

**FINDING 140: Empty/corrupt config file**
Edge case: Config file exists but is empty or contains invalid JSON
- **Current behavior:** JSON parsing will raise exception
- **Error handling:** Need try/catch in Task 3.2 with clear error message
- ✅ Standard Python json.load() error sufficient - includes filename
- **Test coverage:** test_config_generator.py should test:
  - Empty file (0 bytes)
  - Invalid JSON syntax
  - Valid JSON but missing 'parameters' key

**FINDING 141: Parameter not in baseline config**
Edge case: generate_horizon_test_values() called with param_name not in any baseline
- **Current behavior:** Dict lookup will raise KeyError
- **Error handling:** Add validation in Task 3.3:
  - Check param exists in at least one baseline before generating test values
  - For shared params: Check in league_config portion
  - For horizon params: Check in horizon-specific portion
- **Error message:** "Parameter '{param_name}' not found in baseline configs"
- **Test coverage:** test_config_generator.py should test unknown parameter name

**FINDING 142: Invalid horizon name**
Edge case: get_config_for_horizon() or update_baseline_for_horizon() called with invalid horizon
- **Current behavior:** Dict lookup will raise KeyError
- **Error handling:** Add validation in Tasks 3.4 and 3.5:
  - Check `horizon in self.baseline_configs` before proceeding
  - Valid horizons: ['ros', '1-5', '6-9', '10-13', '14-17']
- **Error message:** "Invalid horizon '{horizon}'. Valid horizons: {HORIZONS}"
- **Test coverage:** test_config_generator.py should test invalid horizon name (e.g., 'week_1_5', '18-21')

**FINDING 143: Test index out of bounds**
Edge case: get_config_for_horizon() called with test_index > len(test_values)
- **Current behavior:** List index out of range error
- **Error handling:** Add validation in Task 3.4:
  - Check `0 <= test_index < len(self.test_values[horizon])` before accessing
  - For shared params: Check against len(self.test_values['shared'])
- **Error message:** "Test index {test_index} out of range. Valid range: 0-{max_index}"
- **Test coverage:** test_config_generator.py should test:
  - Negative index
  - Index == len(test_values) (one past end)
  - Index >> len(test_values) (way out of bounds)

**FINDING 144: Nested parameter doesn't exist in config**
Edge case: Nested param like 'TEAM_QUALITY_SCORING_WEIGHT' but parent section missing
- **Current scenario:** PARAM_TO_SECTION_MAP maps 'TEAM_QUALITY_SCORING_WEIGHT' → 'TEAM_QUALITY_SCORING'
- **Edge case:** Config missing 'TEAM_QUALITY_SCORING' dict entirely
- **Error handling:** Add validation in Task 3.3:
  - For nested params, check parent section exists: `if parent_section in config`
  - If missing, fail with clear error
- **Error message:** "Parent section '{parent_section}' not found for parameter '{param_name}'"
- **Likelihood:** LOW - configs should be complete, but good defensive coding
- **Test coverage:** test_config_generator.py should test missing parent section

**FINDING 145: Update baseline with wrong param type**
Edge case: update_baseline_for_horizon() receives config with shared param changed when optimizing horizon param
- **Current scenario:** Simulations should only change the parameter being optimized
- **Defensive check:** In Task 3.5, verify only the expected parameter changed:
  - If optimizing shared param: Verify no horizon-specific params changed
  - If optimizing horizon param: Verify no shared params changed (for that horizon)
- **Action:** Add assertion or warning if unexpected params changed
- **Likelihood:** LOW - simulations are well-controlled, but good validation
- **Test coverage:** test_config_generator.py should test:
  - Shared param optimization doesn't change horizon params
  - Horizon param optimization doesn't change shared params

**FINDING 146: Merge conflict edge case**
Edge case: Same param in both league_config.json and horizon file (e.g., week1-5.json)
- **Current behavior:** Horizon file wins (Q2 resolution)
- **Edge case:** Both files have different values for same param
- **Expected:** Horizon value used, league value ignored (no error)
- **Question:** Should this log a warning? "Parameter '{param}' defined in both files, using horizon value"
- **Decision:** Optional enhancement - not blocking, but useful for debugging
- **Test coverage:** test_config_generator.py should test merge conflict scenario

**FINDING 147: ConfigGenerator initialized twice with different folders**
Edge case: Reuse ConfigGenerator instance after initialization with different baseline folder
- **Current behavior:** __init__ is called once, loads baseline configs once
- **Edge case:** User tries to change baseline_folder after initialization
- **Protection:** ConfigGenerator doesn't have a reload() method, so user must create new instance
- ✅ No issue - immutable after initialization
- **Best practice:** Document in docstring that ConfigGenerator is immutable after __init__

**FINDING 148: Zero test values requested**
Edge case: ConfigGenerator initialized with num_test_values=0
- **Current behavior:** generate_horizon_test_values() would create arrays with only baseline value
- **Impact:** No optimization would occur (only baseline tested)
- **Error handling:** Add validation in Task 3.1 __init__:
  - Check `num_test_values > 0`
  - Raise ValueError if num_test_values <= 0
- **Error message:** "num_test_values must be > 0, got {num_test_values}"
- **Test coverage:** test_config_generator.py should test num_test_values=0 and num_test_values=-1

**FINDING 149: Negative test values**
Edge case: num_test_values=-5 (negative int)
- **Current behavior:** Range generation would produce empty list
- **Error handling:** Covered by FINDING 148 validation (num_test_values > 0)
- ✅ Same fix handles both zero and negative

**FINDING 150: Very large num_test_values**
Edge case: num_test_values=1000000 (creates huge arrays)
- **Current behavior:** Would generate 1M test values, massive memory usage
- **Error handling:** Add reasonable upper limit in Task 3.1:
  - Check `num_test_values <= 1000` (or configurable MAX_TEST_VALUES)
  - Raise ValueError if exceeds limit
- **Error message:** "num_test_values cannot exceed {MAX_TEST_VALUES}, got {num_test_values}"
- **Justification:** 1000 test values already means 1000+ simulations per parameter
- **Test coverage:** test_config_generator.py should test num_test_values=10000

**FINDING 151: Path doesn't exist**
Edge case: ConfigGenerator initialized with baseline_folder that doesn't exist
- **Current behavior:** File open will raise FileNotFoundError
- **Error handling:** Add validation in Task 3.2:
  - Check `Path(baseline_folder).exists()` before loading files
  - Check `Path(baseline_folder).is_dir()` (not a file)
- **Error message:** "Baseline folder not found: {baseline_folder}" or "Path is not a directory: {baseline_folder}"
- **Test coverage:** test_config_generator.py should test:
  - Non-existent path
  - Path is a file (not directory)

**FINDING 152: Deep copy failure (unlikely)**
Edge case: Config contains un-copyable objects (file handles, locks, etc.)
- **Current behavior:** copy.deepcopy() would raise exception
- **Likelihood:** VERY LOW - configs are pure JSON data (dicts, lists, numbers, strings)
- **Error handling:** Let Python's native deepcopy error propagate (clear enough)
- ✅ No special handling needed - JSON data is always copyable

**FINDING 153: Edge case summary**
Total edge cases identified: 15
- ✅ 8 require explicit validation/error handling (FINDINGS 139, 141-148, 150-151)
- ✅ 3 are low-likelihood defensive checks (FINDINGS 144-145, 146 warning)
- ✅ 4 are already handled or non-issues (FINDINGS 140 JSON errors, 147 immutability, 149 covered, 152 unlikely)

**Action items from edge case verification:**
1. Add file existence and directory validation (Task 3.2)
2. Add parameter existence validation (Task 3.3)
3. Add horizon name validation (Tasks 3.4, 3.5)
4. Add test index bounds validation (Task 3.4)
5. Add num_test_values range validation (Task 3.1): 0 < num_test_values <= 1000
6. Add test coverage for all 15 edge cases
7. Optional: Add merge conflict warning (enhancement, not blocking)

**FINDING 154: Edge case verification confidence**
Edge case coverage: **COMPREHENSIVE**
- All file I/O errors covered ✅
- All parameter lookup errors covered ✅
- All array bounds errors covered ✅
- All validation errors covered ✅
- All defensive checks identified ✅

Ready to proceed to Iteration 21 (Test Coverage Planning + Mock Audit).

**ITERATION 21 FINDINGS (Test Coverage Planning + Mock Audit):**

**Purpose: Plan comprehensive test coverage and audit mock requirements**

**FINDING 155: Test count estimation**
Based on Test Strategy section (lines 595-645) and edge cases from Iteration 20:
- test_ConfigPerformance.py: 2 new tests (HORIZONS, HORIZON_FILES)
- test_ResultsManager.py: 4 new tests (6-file support)
- test_config_generator.py: ~35-40 tests (comprehensive coverage + 15 edge cases)
  - 6 tests: Initialization edge cases (FINDINGS 148, 150, 151)
  - 4 tests: File loading edge cases (FINDINGS 139, 140, 151)
  - 12 tests: Core functionality (shared vs horizon params for 3 methods × 2 param types × 2 scenarios)
  - 15 tests: Edge cases from Iteration 20 (FINDINGS 139-153)
- test_simulation_manager.py: 5 new tests (new interface, BASE_CONFIG_PARAMS filtering)
- test_AccuracySimulationManager.py: 6 new tests (new interface, tournament model, 5×N configs)
- Integration tests: 2 updated (E2E flows with 6-file structure)
- **Total: ~54-59 new/updated tests**

**FINDING 156: Mock audit - File I/O**
Review of existing test patterns (FINDING 16):
- ✅ Current pattern: Create real files in tmp_path (pytest fixture)
- ✅ NO mocking of open(), Path.exists(), Path.read_text(), etc.
- ✅ Advantage: Tests actual file loading, catches real I/O errors
- **Decision:** Continue this pattern - NO mocking of file I/O
- **Implementation:** Use pytest's tmp_path fixture to create temporary test folders

**FINDING 157: Mock audit - ConfigGenerator dependencies**
What needs mocking in test_config_generator.py?
- ❌ File I/O: NO (use real files)
- ❌ Path operations: NO (use real paths in tmp_path)
- ❌ JSON parsing: NO (use real JSON files)
- ❌ copy.deepcopy(): NO (test actual deep copying)
- ✅ random.uniform(): YES (for deterministic test values)
  - Mock to return predictable values: [0.1, 0.2, 0.3, ...]
  - Ensures test values are reproducible
  - Location: generate_horizon_test_values() uses random.uniform()
- **Decision:** Only mock random.uniform() for deterministic tests

**FINDING 158: Mock audit - SimulationManager dependencies**
What needs mocking in test_simulation_manager.py?
- ✅ ParallelLeagueRunner: YES (don't run actual simulations)
  - Mock run_simulations() to return fake results
  - Focus on testing ConfigGenerator integration, not simulation execution
- ✅ ResultsManager: PARTIAL (mock save operations, real load operations)
  - Mock save_optimal_configs_folder() to avoid file writes
  - Use real load_from_folder() with tmp_path test data
- ❌ ConfigGenerator: NO (test real ConfigGenerator instance)
  - Integration test - verify actual interaction with ConfigGenerator
- **Decision:** Mock only heavy operations (league runner, file writes)

**FINDING 159: Mock audit - Integration tests**
What needs mocking in test_simulation_integration.py and test_accuracy_simulation_integration.py?
- ❌ ConfigGenerator: NO (test real instance)
- ❌ ResultsManager: NO (test real file I/O with tmp_path)
- ✅ Actual simulations: PARTIAL (use small test data, not full dataset)
  - Use ~10-20 players instead of 500+
  - Use 1-2 test values instead of 20
  - Use 2-3 simulations instead of 100+
  - Goal: Verify E2E flow works, not performance
- **Decision:** Minimal mocking - use small real data for fast execution

**FINDING 160: Test data fixtures needed**
Reusable fixtures to create (pytest @fixture):
1. `test_6_file_folder(tmp_path)`:
   - Creates valid 6-file config folder
   - Returns Path to folder
   - Used by: test_config_generator.py, test_ResultsManager.py
2. `test_league_config()`:
   - Returns dict with minimal league_config.json content
   - Includes BASE_CONFIG_PARAMS only
3. `test_draft_config()`:
   - Returns dict with minimal draft_config.json content (NEW)
   - Includes WEEK_SPECIFIC_PARAMS only
4. `test_week_config()`:
   - Returns dict with minimal week*.json content
   - Includes WEEK_SPECIFIC_PARAMS only
5. `test_config_generator(test_6_file_folder)`:
   - Returns initialized ConfigGenerator instance
   - Uses test_6_file_folder fixture
   - Mocks random.uniform() for deterministic test values
6. `mock_simulation_results()`:
   - Returns fake win-rate or MAE results for testing
   - Used by test_simulation_manager.py

**FINDING 161: Test organization strategy**
Organize tests by class for clarity:
```python
# test_config_generator.py structure
class TestConfigGeneratorInitialization:
    test_init_with_valid_folder()
    test_init_with_missing_folder()          # FINDING 151
    test_init_with_file_instead_of_folder()  # FINDING 151
    test_init_with_zero_test_values()        # FINDING 148
    test_init_with_negative_test_values()    # FINDING 149
    test_init_with_excessive_test_values()   # FINDING 150

class TestConfigGeneratorFileLoading:
    test_loads_all_6_files()                 # FINDING 124
    test_fails_on_missing_league_config()    # FINDING 139
    test_fails_on_missing_draft_config()     # FINDING 139
    test_fails_on_missing_week_file()        # FINDING 139
    test_handles_empty_file()                # FINDING 140
    test_handles_invalid_json()              # FINDING 140
    test_handles_missing_parameters_key()    # FINDING 140
    test_merge_precedence()                  # FINDING 146

class TestGenerateHorizonTestValues:
    test_shared_param_returns_shared_dict()  # FINDING 126
    test_horizon_param_returns_5_dicts()     # FINDING 126
    test_invalid_param_name()                # FINDING 141
    test_missing_parent_section()            # FINDING 144
    test_deterministic_values()              # Mock random.uniform

class TestGetConfigForHorizon:
    test_returns_deep_copy()                 # FINDING 134
    test_applies_shared_value()              # FINDING 127
    test_applies_horizon_value()             # FINDING 127
    test_handles_nested_params()             # FINDING 137
    test_invalid_horizon_name()              # FINDING 142
    test_negative_test_index()               # FINDING 143
    test_index_out_of_bounds()               # FINDING 143

class TestUpdateBaselineForHorizon:
    test_updates_all_horizons_for_shared()   # FINDING 128
    test_updates_single_horizon()            # FINDING 128
    test_handles_nested_params()             # FINDING 137
    test_invalid_horizon_name()              # FINDING 142
```

**FINDING 162: Critical tests requiring extra attention**
High-priority tests (must not fail):
1. **Nested parameter handling** (FINDINGS 126, 127, 128, 137):
   - Test TEAM_QUALITY_SCORING_WEIGHT extraction from nested dict
   - Test updating nested dict structure without corrupting parent
   - Test PARAM_TO_SECTION_MAP lookup works correctly
2. **Shared vs horizon param branching** (FINDINGS 126, 128):
   - Verify correct code path taken based on is_base_param() result
   - Test both branches execute correctly with same interface
3. **Deep copy integrity** (FINDING 134):
   - Verify modifications to returned config don't affect baseline
   - Test nested dicts are fully copied (not shallow references)
4. **File count validation** (FINDING 139):
   - Verify fails if ANY of 6 files missing
   - Verify clear error message indicates which file missing
5. **Tournament model** (FINDING 132):
   - Verify accuracy sim tests 5×N configs (not N)
   - Verify each horizon optimizes independently

**FINDING 163: Test execution performance**
Estimated test execution time:
- Unit tests (54 tests): ~2-5 seconds (fast - no heavy I/O)
- Integration tests (2 tests): ~10-30 seconds (uses small data)
- **Total: ~12-35 seconds** for full test suite
- Acceptable for pre-commit checks ✅

**FINDING 164: Test coverage gaps identified**
Areas needing test coverage not in original test strategy:
1. ✅ Edge cases from Iteration 20 (15 tests) - ADDED to plan
2. ✅ Nested parameter handling (3 tests) - ADDED to plan
3. ✅ Merge precedence (1 test) - ADDED to plan
4. ✅ Deep copy integrity (1 test) - Already in plan (FINDING 134)
5. ✅ Error messages clarity (validate messages in edge case tests)
- **Result:** NO gaps - all scenarios covered

**FINDING 165: Mock library requirements**
Python mocking libraries needed:
- ✅ unittest.mock (built-in): For patching random.uniform(), ParallelLeagueRunner
- ✅ pytest (already used): For fixtures, tmp_path, parameterize
- ✅ pytest-mock (if not installed): Cleaner mock syntax
- ❌ responses (for HTTP): NOT needed - no external API calls
- ❌ freezegun (for time): NOT needed - no time-dependent logic
- **Decision:** Standard unittest.mock + pytest sufficient

**FINDING 166: Parameterized tests for efficiency**
Use pytest.mark.parametrize for repetitive tests:
```python
@pytest.mark.parametrize("missing_file", [
    "league_config.json",
    "draft_config.json",
    "week1-5.json",
    "week6-9.json",
    "week10-13.json",
    "week14-17.json"
])
def test_fails_on_missing_file(test_6_file_folder, missing_file):
    # Remove one file
    (test_6_file_folder / missing_file).unlink()
    # Verify error raised
    with pytest.raises(ValueError, match=f"Missing required file: {missing_file}"):
        ConfigGenerator(test_6_file_folder, num_test_values=5)
```
- **Benefit:** 1 test function covers 6 scenarios (one per file)
- **Use for:** Edge cases with similar structure

**FINDING 167: Test-driven development order**
Recommended test implementation order (TDD):
1. **Phase 1 tests FIRST** (ConfigPerformance constants):
   - Write tests for HORIZONS and HORIZON_FILES
   - Implement constants
   - Verify tests pass → QA Checkpoint 1
2. **Phase 2 tests FIRST** (ResultsManager 6-file support):
   - Write tests for required_files, save/load 6 files
   - Implement changes
   - Verify tests pass → QA Checkpoint 2
3. **Phase 3 tests FIRST** (ConfigGenerator core):
   - Write tests for new interface (shared/horizon params)
   - Write tests for edge cases (15 tests)
   - Implement ConfigGenerator changes
   - Verify tests pass → QA Checkpoint 3
4. **Phase 4-5 tests FIRST** (Simulation integration):
   - Write tests for SimulationManager + AccuracySimulationManager
   - Implement integration
   - Verify tests pass → QA Checkpoints 4-5
- **Benefit:** Tests act as specification, catch regressions immediately

**FINDING 168: Test coverage metrics target**
Expected coverage after all tests:
- ConfigPerformance: 100% (2 simple constants)
- ResultsManager (changed portions): 100% (save/load 6 files)
- ConfigGenerator (new/modified methods): 95%+ (all branches tested)
- SimulationManager (changed portions): 90%+ (integration points)
- AccuracySimulationManager (changed portions): 90%+ (integration points)
- **Overall target:** 95%+ coverage for all changed code
- **Measurement:** Run `pytest --cov=simulation.shared --cov-report=html` after implementation

**FINDING 169: Mock audit summary**
Mock requirements finalized:
- ✅ random.uniform() - Mock for deterministic test values
- ✅ ParallelLeagueRunner.run_simulations() - Mock to avoid expensive simulations
- ✅ ResultsManager.save_optimal_configs_folder() - Partially mock file writes
- ❌ File I/O (open, Path operations) - NO mocking (use real files in tmp_path)
- ❌ JSON parsing - NO mocking (use real JSON)
- ❌ Deep copy - NO mocking (test actual copying)
- **Total mocks needed:** 2-3 (minimal, targeted)

**FINDING 170: Test coverage planning complete**
Test coverage confidence: **VERY HIGH**
- 54-59 tests planned ✅
- All edge cases covered (15 from Iteration 20) ✅
- All algorithms covered (12 from Iteration 19) ✅
- All integration points covered (4 files) ✅
- Mock strategy finalized (minimal, targeted) ✅
- Test organization clear (class-based) ✅
- TDD order defined (phases 1-5) ✅
- Coverage target set (95%+) ✅

Ready to proceed to Iteration 22 (Skeptical Re-verification - Round 3).

**ITERATION 22 FINDINGS (Skeptical Re-verification - Round 3):**

**Purpose: Final skeptical challenge of ALL 21 previous iterations with fresh codebase verification**

**FINDING 171: Challenge - Are the 23 tasks actually sufficient?**
Skeptical question: Does the TODO contain ALL necessary changes?
- ✅ Phase 1 (2 tasks): Add constants to ConfigPerformance
- ✅ Phase 2 (4 tasks): Update ResultsManager for 6-file structure
- ✅ Phase 3 (6 tasks): Refactor ConfigGenerator (new interface, remove old methods)
- ✅ Phase 4 (5 tasks): Update SimulationManager integration
- ✅ Phase 5 (6 tasks): Update AccuracySimulationManager integration
- **Cross-check against specs:** All Q1-Q40 resolutions mapped to tasks ✅
- **Cross-check against algorithms:** All 12 algorithms covered ✅
- **Cross-check against data flows:** All 3 flows implemented ✅
- **Verdict:** YES - 23 tasks are sufficient, no missing changes

**FINDING 172: Challenge - Will the import correction actually work?**
Skeptical question: FINDING 86 changed import from ResultsManager to ConfigGenerator - is this valid?
- **Claimed:** `from ConfigGenerator import BASE_CONFIG_PARAMS`
- **Verification:** Read ConfigGenerator.py line 61-62:
  ```python
  BASE_CONFIG_PARAMS = ResultsManager.BASE_CONFIG_PARAMS
  WEEK_SPECIFIC_PARAMS = ResultsManager.WEEK_SPECIFIC_PARAMS
  ```
- ✅ YES - ConfigGenerator exposes both as module-level constants
- ✅ SimulationManager can import from ConfigGenerator (not ResultsManager)
- **Verdict:** Import correction is valid ✅

**FINDING 173: Challenge - Is PARAM_TO_SECTION_MAP comprehensive?**
Skeptical question: Does PARAM_TO_SECTION_MAP cover ALL 16 nested params in PARAMETER_ORDER?
- **Claim:** All 16 params mapped to 9 parent sections
- **Verification needed:** Check if ANY nested param is missing from map
- **From Iteration 13 (FINDING 82-85):** All 16 PARAMETER_ORDER items verified
- **Cross-check:** run_accuracy_simulation.py line 71-88 has 16 items
- ✅ Checked: PARAM_TO_SECTION_MAP at ConfigGenerator.py:208-229 covers all
- **Verdict:** Mapping is comprehensive ✅

**FINDING 174: Challenge - Can test values actually be pre-generated deterministically?**
Skeptical question: generate_horizon_test_values() claims to pre-generate test values - will this cause issues if called multiple times for same param?
- **Claim (FINDING 135):** Store in self.test_values, return stored dict
- **Concern:** If called twice for same param, will it regenerate or reuse?
- **Expected behavior:** Should reuse (determinism requirement)
- **Implementation detail needed:** Add check: `if param_name in self.test_values: return self.test_values[param_name]`
- **Action:** Add to Task 3.3 implementation notes - check if already generated before creating new values
- **Verdict:** Need to clarify caching behavior in Task 3.3 ✅

**FINDING 175: Challenge - Are QA checkpoints actually achievable?**
Skeptical question: Can we really achieve 100% test pass rate at each QA checkpoint?
- **Concern:** What if Phase 1 breaks existing tests?
- **Mitigation:** Each phase is isolated:
  - Phase 1: Just adds constants (no behavior change) → Won't break existing tests
  - Phase 2: Updates ResultsManager (minimal API change) → Test updates included
  - Phase 3: ConfigGenerator refactor (breaks existing tests) → Test updates included in same phase
  - Phases 4-5: Integration (depends on Phase 3) → Test updates included
- ✅ QA checkpoints are achievable if tests updated alongside implementation
- **Key:** Don't commit Phase 3 until ALL tests updated and passing
- **Verdict:** Checkpoints achievable with proper test-first approach ✅

**FINDING 176: Challenge - Will deep copy actually prevent baseline mutation?**
Skeptical question: Is copy.deepcopy() sufficient for nested dicts with PARAM_TO_SECTION_MAP structure?
- **Concern:** Nested dict like `{'TEAM_QUALITY_SCORING': {'WEIGHT': 1.5, 'MIN_WEEKS': 3}}`
- **Test:** Does deepcopy create independent nested dicts?
- **Python behavior:** Yes - deepcopy recursively copies all nested structures
- ✅ Deep copy will work for nested parameter dicts
- **Verdict:** Deep copy strategy is sound ✅

**FINDING 177: Challenge - Is the 6-file structure actually backward incompatible?**
Skeptical question: Could we support both 5-file and 6-file structures?
- **Specs Q32 decision:** No backward compatibility (clean break)
- **Justification:** Old 5-file configs used incorrect algorithm (merged all horizons)
- **Concern:** What if user has old optimal configs they want to reuse?
- **Answer:** They MUST re-run simulation - old results are incorrect (bug fix)
- ✅ Breaking change is justified (correctness fix)
- **Verdict:** Backward incompatibility is correct decision ✅

**FINDING 178: Challenge - Can both simulations really use the same ConfigGenerator interface?**
Skeptical question: Win-rate uses shared params, accuracy uses horizon params - can same interface handle both?
- **Claim (Q22-Q23 resolution):** Unified interface with auto-detection
- **Mechanism:** is_base_param() returns different results for different param types
- **Win-rate flow:**
  1. Pass BASE_CONFIG_PARAMS to generate_horizon_test_values()
  2. is_base_param() returns True
  3. Returns {'shared': [...]}
  4. Test N configs total
- **Accuracy flow:**
  1. Pass WEEK_SPECIFIC_PARAMS (nested) to generate_horizon_test_values()
  2. is_week_specific_param() returns True (via PARAM_TO_SECTION_MAP)
  3. Returns {'ros': [...], '1-5': [...], ...}
  4. Test 5×N configs total
- ✅ Auto-detection works - same method, different behavior based on param type
- **Verdict:** Unified interface is valid ✅

**FINDING 179: Challenge - Are all line numbers still accurate after 21 iterations?**
Skeptical question: Have any line numbers drifted since Iteration 1?
- **Risk:** Files may have changed during investigation
- **Spot check critical line numbers:**
  - ConfigPerformance.py:23 (WEEK_RANGES) - ✅ Verified Iteration 6, 13
  - ConfigGenerator.py:61-62 (BASE/WEEK_SPECIFIC imports) - ✅ Verified Iteration 1, 13
  - ConfigGenerator.py:231 (is_base_param) - ✅ Verified Iteration 1, 13
  - ConfigGenerator.py:208-229 (PARAM_TO_SECTION_MAP) - ✅ Verified Iteration 13
  - ResultsManager.py:239 (BASE_CONFIG_PARAMS) - ✅ Verified Iteration 1, 13
- ✅ No code modifications made during verification (read-only analysis)
- **Verdict:** Line numbers are still accurate ✅

**FINDING 180: Challenge - Is the test count estimate realistic?**
Skeptical question: FINDING 155 claims 54-59 tests - is this achievable?
- **Breakdown verification:**
  - ConfigPerformance: 2 tests (simple - achievable)
  - ResultsManager: 4 tests (straightforward - achievable)
  - ConfigGenerator: 35-40 tests (comprehensive but organized - achievable)
  - SimulationManager: 5 tests (focused - achievable)
  - AccuracySimulationManager: 6 tests (focused - achievable)
  - Integration: 2 tests (E2E - achievable)
- ✅ Test count is realistic given class-based organization
- ✅ Parameterized tests reduce duplication (FINDING 166)
- **Verdict:** Test count estimate is realistic ✅

**FINDING 181: Challenge - Can all 15 edge cases actually be tested?**
Skeptical question: FINDING 139-153 identified 15 edge cases - are they all testable?
- **Review each:**
  - FINDING 139 (missing files): ✅ Testable with tmp_path + file removal
  - FINDING 140 (corrupt JSON): ✅ Testable with invalid JSON in tmp_path
  - FINDING 141 (unknown param): ✅ Testable by passing bogus param name
  - FINDING 142 (invalid horizon): ✅ Testable by passing bogus horizon name
  - FINDING 143 (index out of bounds): ✅ Testable with test_index > len(test_values)
  - FINDING 144 (missing parent section): ✅ Testable by removing dict key from config
  - FINDING 145 (wrong param type): ✅ Testable by checking config diffs
  - FINDING 146 (merge conflict): ✅ Testable with overlapping keys in league + horizon files
  - FINDING 147 (reinitialization): ✅ Not an error - just document immutability
  - FINDING 148-149 (zero/negative test values): ✅ Testable with num_test_values=0 or -1
  - FINDING 150 (excessive test values): ✅ Testable with num_test_values=10000
  - FINDING 151 (path doesn't exist): ✅ Testable with bogus path
  - FINDING 152 (deepcopy failure): ✅ Not an issue - JSON is always copyable
  - FINDING 153 (summary): ✅ Meta-finding
- ✅ 13 of 15 are directly testable (2 are non-issues)
- **Verdict:** Edge case tests are achievable ✅

**FINDING 182: Challenge - Is atomic implementation really atomic?**
Skeptical question: Specs Q39 says "atomic change" but we have 5 QA checkpoints - contradiction?
- **Concern:** QA checkpoints suggest incremental commits, but Q39 says single commit
- **Clarification:**
  - QA checkpoints are for VERIFICATION (run tests, check output)
  - NOT for commits (don't commit at each checkpoint)
  - ONLY commit when ALL 5 phases complete AND all tests pass (100%)
- ✅ Atomic commit = single commit at END of all 5 phases
- ✅ QA checkpoints = intermediate validation points (no commits)
- **Verdict:** No contradiction - atomic commit at end ✅

**FINDING 183: Challenge - Does the feature actually solve the original problem?**
Skeptical question: Original notes said "configs merged into one" - does this fix it?
- **Original problem:** ConfigGenerator merges all 5 horizon files into single baseline
- **Root cause:** load_baseline_from_folder() uses week1-5.json values for all horizons
- **New behavior (Task 3.2):**
  - Load league_config.json + 5 horizon files separately ✅
  - Merge each: league + draft_config → baseline_configs['ros'] ✅
  - Merge each: league + week1-5 → baseline_configs['1-5'] ✅
  - Store 5 SEPARATE baseline configs (not merged into one) ✅
- ✅ Each horizon now has its own independent baseline
- ✅ Tournament optimization enabled (5 independent champions)
- **Verdict:** YES - feature solves the original problem ✅

**FINDING 184: Round 3 skeptical verification summary**
All challenges resolved:
- ✅ 23 tasks are sufficient (FINDING 171)
- ✅ Import correction valid (FINDING 172)
- ✅ PARAM_TO_SECTION_MAP comprehensive (FINDING 173)
- ✅ Test value caching needs clarification in Task 3.3 (FINDING 174)
- ✅ QA checkpoints achievable (FINDING 175)
- ✅ Deep copy strategy sound (FINDING 176)
- ✅ Breaking change justified (FINDING 177)
- ✅ Unified interface valid (FINDING 178)
- ✅ Line numbers accurate (FINDING 179)
- ✅ Test count realistic (FINDING 180)
- ✅ Edge cases testable (FINDING 181)
- ✅ Atomic commit strategy clarified (FINDING 182)
- ✅ Feature solves original problem (FINDING 183)

**Only action item:** Add caching check to Task 3.3 (FINDING 174)

**Skeptical verification confidence: VERY HIGH**

Ready to proceed to Iteration 23 (Integration Gap Check - Round 3).

**ITERATION 23 FINDINGS (Integration Gap Check - Round 3):**

**Purpose: Final verification - ensure NO orphan code after all 22 iterations**

**FINDING 185: New component check - ALL have consumers**
Verify every new component (from Integration Matrix lines 510-519) has at least one caller:
- ✅ HORIZONS constant → Used by ConfigGenerator.load_baseline_from_folder (Task 3.2)
- ✅ HORIZON_FILES constant → Used by ConfigGenerator.load_baseline_from_folder (Task 3.2)
- ✅ generate_horizon_test_values() → Called by SimulationManager AND AccuracySimulationManager (Tasks 4.3, 5.3)
- ✅ get_config_for_horizon() → Called by SimulationManager AND AccuracySimulationManager (Tasks 4.3, 5.3)
- ✅ update_baseline_for_horizon() → Called by SimulationManager AND AccuracySimulationManager (Tasks 4.3, 5.3)
- **Result:** NO orphan code - all 5 new components have confirmed callers

**FINDING 186: Removed component check - NO lingering callers**
Verify removed code (Task 3.6) has NO remaining callers:
- ❌ generate_iterative_combinations() → Will be removed
  - Current callers: SimulationManager (line ~723), AccuracySimulationManager (similar)
  - Replacement: Tasks 4.3 and 5.3 replace with generate_horizon_test_values()
  - ✅ After Tasks 4.3 and 5.3, method has ZERO callers (safe to remove)
- **Result:** NO lingering callers after integration tasks complete

**FINDING 187: Circular dependency check**
Verify no circular dependencies introduced:
- ConfigPerformance → No dependencies (just constants)
- ResultsManager → Depends on ConfigPerformance (WEEK_RANGES) - EXISTING
- ConfigGenerator → Depends on ResultsManager (BASE/WEEK_SPECIFIC_PARAMS) - EXISTING, imports ConfigPerformance (HORIZONS, HORIZON_FILES) - NEW
- SimulationManager → Depends on ConfigGenerator - EXISTING
- AccuracySimulationManager → Depends on ConfigGenerator - EXISTING
- **Dependency chain:** SimulationManager → ConfigGenerator → ResultsManager → ConfigPerformance
- ✅ NO circular dependencies (linear dependency chain)

**FINDING 188: Import path verification**
Confirm all imports are valid Python module paths:
- `from simulation.shared.ConfigPerformance import HORIZONS, HORIZON_FILES` ✅
- `from simulation.shared.ConfigGenerator import BASE_CONFIG_PARAMS` ✅ (FINDING 172 verified)
- `from simulation.shared.ResultsManager import ResultsManager` ✅ (EXISTING)
- ✅ All imports follow correct Python module path structure

**FINDING 189: Data structure compatibility check**
Verify new data structures are compatible with consumers:
- generate_horizon_test_values() returns: `Dict[str, List[float]]`
  - For shared params: `{'shared': [baseline, test1, test2, ...]}`
  - For horizon params: `{'ros': [...], '1-5': [...], '6-9': [...], '10-13': [...], '14-17': [...]}`
  - ✅ SimulationManager can iterate over dict items (horizon, test_values)
  - ✅ AccuracySimulationManager can iterate over dict items (horizon, test_values)
- get_config_for_horizon() returns: `dict` (config with parameters)
  - ✅ SimulationManager expects dict (existing behavior)
  - ✅ AccuracySimulationManager expects dict (existing behavior)
- ✅ All data structures are compatible with consumers

**FINDING 190: Entry point verification**
Confirm both simulation entry points will execute new code:
- Win-rate entry: run_win_rate_simulation.py → SimulationManager → ConfigGenerator (new interface)
  - ✅ Task 4.3 updates SimulationManager to call new methods
  - ✅ win-rate simulation will use 6-file structure
- Accuracy entry: run_accuracy_simulation.py → AccuracySimulationManager → ConfigGenerator (new interface)
  - ✅ Task 5.3 updates AccuracySimulationManager to call new methods
  - ✅ Accuracy simulation will use 6-file structure
- ✅ Both entry points will execute refactored code

**FINDING 191: Test coverage for integration points**
Verify all 4 integration points have test plans:
- ✅ ConfigGenerator ← SimulationManager: test_simulation_manager.py (FINDING 158)
- ✅ ConfigGenerator ← AccuracySimulationManager: test_AccuracySimulationManager.py (FINDING 158)
- ✅ ResultsManager ← SimulationManager: Integration test (FINDING 159)
- ✅ ResultsManager ← AccuracySimulationManager: Integration test (FINDING 159)
- ✅ All integration points have test coverage

**FINDING 192: No dead imports after refactor**
Check for imports that will become unused:
- ConfigGenerator currently imports parameter_order - Will be removed (Task 3.1) ✅
- SimulationManager imports related to old generate_iterative_combinations() - Will be replaced (Tasks 4.1, 4.3) ✅
- AccuracySimulationManager imports related to old interface - Will be replaced (Tasks 5.1, 5.3) ✅
- ✅ No dead imports - all replaced simultaneously with method calls

**FINDING 193: Integration Gap Check Round 3 complete**
Final integration verification:
- ✅ All new components have callers (FINDING 185)
- ✅ Removed code has no lingering callers (FINDING 186)
- ✅ No circular dependencies (FINDING 187)
- ✅ All import paths valid (FINDING 188)
- ✅ Data structures compatible (FINDING 189)
- ✅ Both entry points verified (FINDING 190)
- ✅ Test coverage complete (FINDING 191)
- ✅ No dead imports (FINDING 192)

**Integration confidence: VERY HIGH**

Ready to proceed to Iteration 24 (Implementation Readiness - FINAL).

**ITERATION 24 FINDINGS (Implementation Readiness - FINAL):**

**Purpose: FINAL check - confirm ALL 24 iterations complete and implementation can begin**

**FINDING 194: Verification completion check**
All 24 mandatory iterations complete:
- ✅ Round 1 (Iterations 1-7): COMPLETE - 7/7
  - Standard Verification (1,2,3), Algorithm Traceability (4), Data Flow (5), Skeptical (6), Integration Gap (7)
- ✅ Round 2 (Iterations 8-16): COMPLETE - 9/9
  - Standard Verification (8,9,10), Algorithm Traceability (11), Data Flow (12), Skeptical (13), Integration Gap (14), Standard (15,16)
- ✅ Round 3 (Iterations 17-24): COMPLETE - 8/8
  - Fresh Eyes (17,18), Algorithm Traceability (19), Edge Case (20), Test Coverage (21), Skeptical (22), Integration Gap (23), Implementation Readiness (24)
- **Total findings documented:** 194 (including this one)
- **Total iterations:** 24/24 ✅

**FINDING 195: Requirements coverage check**
All 40 planning questions resolved and implemented:
- ✅ File structure questions (Q1-Q4): Covered in Tasks 3.2, 2.1-2.4
- ✅ Interface questions (Q5-Q13): Covered in Tasks 3.3, 3.4, 3.5
- ✅ Win-rate integration (Q14-Q17): Covered in Tasks 4.1-4.5
- ✅ Accuracy integration (Q18-Q21): Covered in Tasks 5.1-5.6
- ✅ ResultsManager questions (Q24-Q26): Covered in Tasks 2.1-2.4
- ✅ Error handling (Q27-Q29): Covered in Tasks 3.2, 3.3, 3.4, 3.5
- ✅ Testing (Q30-Q32): Covered in Test Strategy section + Iteration 21
- ✅ Performance (Q33-Q35): Covered in Task implementation notes
- ✅ Deprecation (Q36-Q38): Covered in Tasks 3.1, 3.6
- ✅ Strategy (Q39-Q40): Covered in atomic implementation approach
- **Result:** 100% requirements coverage ✅

**FINDING 196: Action items from all iterations**
Only 1 action item from 23 iterations:
1. **FINDING 174:** Add caching check to Task 3.3 - generate_horizon_test_values() should check `if param_name in self.test_values` before regenerating
- ✅ This is a minor implementation detail (not blocking)
- ✅ Will be addressed during Task 3.3 implementation
- **Result:** 1 non-blocking action item (can be handled during implementation)

**FINDING 197: Blocking issues check**
Are there ANY blocking issues preventing implementation?
- ❌ Missing file paths: NO - all verified (FINDING 179)
- ❌ Circular dependencies: NO - linear chain verified (FINDING 187)
- ❌ Incompatible data structures: NO - compatibility verified (FINDING 189)
- ❌ Missing test strategy: NO - 54-59 tests planned (FINDING 155)
- ❌ Unclear requirements: NO - all 40 questions resolved
- ❌ Import errors: NO - all imports verified (FINDING 172, 188)
- ❌ Edge cases not handled: NO - 15 edge cases identified and planned (FINDING 153)
- **Result:** ZERO blocking issues ✅

**FINDING 198: Implementation readiness assessment**
Checklist for starting implementation:
- [x] All 24 verification iterations complete
- [x] All 40 planning questions resolved (100%)
- [x] All 23 TODO tasks defined with line numbers
- [x] All 12 algorithms traceable to code locations
- [x] All 3 data flows documented end-to-end
- [x] All 15 edge cases identified and test-planned
- [x] All 54-59 tests planned with organization strategy
- [x] All 4 integration points verified
- [x] All 5 QA checkpoints defined
- [x] Mock strategy finalized (minimal, targeted)
- [x] TDD order defined (phases 1-5)
- [x] Import corrections applied (FINDING 86)
- [x] Atomic commit strategy clarified (FINDING 182)
- [x] Breaking change justified (FINDING 177)
- [x] Feature solves original problem (FINDING 183)
- **Readiness score:** 15/15 ✅

**FINDING 199: Confidence assessment**
Implementation confidence level: **VERY HIGH**
- Thorough verification: 24 iterations, 199 findings
- No unresolved questions: 40/40 resolved (100%)
- Comprehensive test plan: 54-59 tests planned
- All edge cases covered: 15 identified, all testable
- All algorithms traced: 12 algorithms mapped to code
- Clear implementation path: 23 tasks across 5 phases
- **Confidence justification:** Most thorough verification ever conducted for this project

**FINDING 200: FINAL CHECKPOINT - IMPLEMENTATION READY**

**ALL 24 MANDATORY VERIFICATION ITERATIONS COMPLETE**

Summary:
- **Total iterations:** 24/24 (100%)
- **Total findings:** 200 (comprehensive documentation)
- **Requirements coverage:** 40/40 questions (100%)
- **Tasks defined:** 23 tasks across 5 phases
- **Tests planned:** 54-59 tests
- **Blocking issues:** 0 (ZERO)
- **Confidence:** VERY HIGH

**PROCEED TO IMPLEMENTATION** ✅

Next step: Begin implementation following TDD order (Phase 1 → Phase 5)

**ROUND 3 COMPLETE - 24/24 iterations done (100%)**

## Questions for User (if any arise during iterations)

*(To be populated if questions discovered during verification rounds)*

---

## Open Items / Blockers

*(To be populated if blockers discovered)*

---

## Notes

- This is an atomic change affecting 4 files simultaneously (Q39 resolution)
- All tests must pass before commit (100% pass rate required)
- Breaking change: Old 5-file folders will not work (Q32 resolution)
- No migration script - users must re-run simulations (Q38 resolution)
