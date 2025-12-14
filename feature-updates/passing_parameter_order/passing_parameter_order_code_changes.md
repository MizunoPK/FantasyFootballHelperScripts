# Passing Parameter Order - Code Changes Documentation

## Overview

Moved `PARAMETER_ORDER` from a class constant in `ConfigGenerator` to a required parameter passed from runner scripts through `SimulationManager`. This allows different scripts to define their own optimization parameter ordering.

---

## Files Modified

### 1. simulation/ConfigGenerator.py

**Changes:**
- Removed `PARAMETER_ORDER` class constant (lines 191-225)
- Added `parameter_order` as a required parameter to `__init__()`
- Added validation: checks all parameter names exist in `PARAM_DEFINITIONS`
- Added validation: checks `parameter_order` is not empty
- Updated all `self.PARAMETER_ORDER` references to `self.parameter_order`

```diff
- PARAMETER_ORDER = [
-     'NORMALIZATION_MAX_SCALE',
-     'SAME_POS_BYE_WEIGHT',
-     # ... 20 more parameters
- ]

+ def __init__(self, baseline_config_path: Path, parameter_order: List[str],
+              num_test_values: int = 5, num_parameters_to_test: int = 1) -> None:
+     # Validate parameter_order
+     unknown_params = [p for p in parameter_order if p not in self.PARAM_DEFINITIONS]
+     if unknown_params:
+         raise ValueError(f"Unknown parameters in parameter_order: {unknown_params}")
+     if not parameter_order:
+         raise ValueError("parameter_order cannot be empty")
+     self.parameter_order = parameter_order
```

---

### 2. simulation/SimulationManager.py

**Changes:**
- Added `parameter_order` as a required parameter to `__init__()`
- Passes `parameter_order` to `ConfigGenerator.__init__()`
- Updated references from `self.config_generator.PARAMETER_ORDER` to `self.config_generator.parameter_order`

```diff
  def __init__(
      self,
      baseline_config_path: Path,
      output_dir: Path,
      num_simulations_per_config : int,
      max_workers : int,
      data_folder: Path,
+     parameter_order: List[str],
      num_test_values: int = 5,
      ...
  ):
      ...
-     self.config_generator = ConfigGenerator(baseline_config_path, num_test_values=num_test_values, ...)
+     self.config_generator = ConfigGenerator(
+         baseline_config_path,
+         parameter_order=parameter_order,
+         num_test_values=num_test_values,
+         ...
+     )
```

---

### 3. run_simulation.py

**Changes:**
- Added `PARAMETER_ORDER` list at top of file (22 parameters)
- Added `parameter_order=PARAMETER_ORDER` to all 3 SimulationManager calls (single/full/iterative modes)

---

### 4. run_draft_order_loop.py

**Changes:**
- Added `PARAMETER_ORDER` list at top of file (22 parameters)
- Added `parameter_order=PARAMETER_ORDER` to SimulationManager call

---

### 5. tests/simulation/test_config_generator.py

**Changes:**
- Added `TEST_PARAMETER_ORDER` constant at top of file
- Updated all ~25 `ConfigGenerator()` instantiations to include `TEST_PARAMETER_ORDER`
- Updated all `ConfigGenerator.PARAMETER_ORDER` references to `TEST_PARAMETER_ORDER` or `generator.parameter_order`
- Updated `test_parameter_order_exists` to check for instance variable

---

### 6. tests/simulation/test_simulation_manager.py

**Changes:**
- Added `TEST_PARAMETER_ORDER` constant at top of file
- Updated all ~8 `SimulationManager()` instantiations to include `parameter_order=TEST_PARAMETER_ORDER`
- Updated mock `config_gen.PARAMETER_ORDER` to `config_gen.parameter_order`

---

### 7. tests/integration/test_simulation_integration.py

**Changes:**
- Added `TEST_PARAMETER_ORDER` constant at top of file
- Updated all `ConfigGenerator()` and `SimulationManager()` instantiations to include parameter_order

---

## Test Results

**All 2223 tests pass (100%)**

---

## Quality Control Rounds

### QC Round 1
- Reviewed: 2025-12-13
- Issues Found: None
- Status: PASSED

**Verified:**
- ConfigGenerator.__init__() has parameter_order as required param (line 353)
- Validation for unknown params and empty list present (lines 385-390)
- self.parameter_order used at lines 392, 777, 786, 808
- PARAMETER_ORDER class constant fully removed
- SimulationManager.__init__() has parameter_order param (line 69)
- SimulationManager passes to ConfigGenerator (line 117)
- SimulationManager uses .parameter_order (lines 555, 657)
- run_simulation.py defines PARAMETER_ORDER and passes (3 places: 361, 389, 421)
- run_draft_order_loop.py defines PARAMETER_ORDER and passes (line 525)
- Test files use TEST_PARAMETER_ORDER constant

### QC Round 2
- Reviewed: 2025-12-13
- Issues Found: 1 (missing validation tests)
- Issues Fixed: 1 (added 2 tests for unknown params and empty list)
- Status: PASSED

**Verified:**
- Validation logic at ConfigGenerator.__init__() lines 385-390 is correct
- Unknown params check happens before empty check (correct order)
- Added test_unknown_parameter_in_parameter_order test
- Added test_empty_parameter_order test
- All 2223 tests pass (2 new tests added)

### QC Round 3
- Reviewed: 2025-12-13
- Issues Found: 1 (outdated docstring examples)
- Issues Fixed: 1 (updated 5 docstring examples with correct signatures)
- Status: PASSED

**Verified:**
- Both runner scripts have identical PARAMETER_ORDER lists (22 params)
- All ConfigGenerator callers pass parameter_order
- All SimulationManager callers pass parameter_order
- Fixed docstrings in ConfigGenerator.py (lines 492, 574)
- Fixed docstrings in SimulationManager.py (lines 386, 643, 1065)
- All 2223 tests pass (100%)
