# Passing Parameter Order - Specification

## Objective

Enable runner scripts (`run_simulation.py`, `run_draft_order_loop.py`) to define their own `PARAMETER_ORDER` list and pass it to the simulation system, allowing different optimization orderings per script without modifying core simulation code.

---

## High-Level Requirements

### 1. Runner Script Changes

- Define `PARAMETER_ORDER` at the top of each runner script
- Pass `PARAMETER_ORDER` to `SimulationManager.__init__()`
- Example:
```python
# run_simulation.py
PARAMETER_ORDER = [
    'NORMALIZATION_MAX_SCALE',
    'SAME_POS_BYE_WEIGHT',
    # ... etc
]

# Later in main():
manager = SimulationManager(
    baseline_config_path=baseline_path,
    # ... other args ...
    parameter_order=PARAMETER_ORDER  # NEW
)
```

### 2. SimulationManager Changes

- Accept `parameter_order` in `__init__()`
- Pass it to `ConfigGenerator.__init__()`
- Use it in `_detect_resume_state()` and `run_iterative_optimization()`

### 3. ConfigGenerator Changes

- Accept `parameter_order` in `__init__()`
- Store as instance variable instead of using class constant
- Continue to provide class constant as default for backward compatibility

### 4. Test Updates

- Update tests that rely on `ConfigGenerator.PARAMETER_ORDER` class constant
- May need to pass explicit parameter_order or use instance

---

## Current Architecture

### PARAMETER_ORDER Definition

```python
# simulation/ConfigGenerator.py lines 191-225
class ConfigGenerator:
    PARAMETER_ORDER = [
        # 'DRAFT_ORDER_FILE',  # commented out
        'NORMALIZATION_MAX_SCALE',
        'SAME_POS_BYE_WEIGHT',
        'DIFF_POS_BYE_WEIGHT',
        'PRIMARY_BONUS',
        'SECONDARY_BONUS',
        'ADP_SCORING_WEIGHT',
        # 'ADP_SCORING_STEPS',  # commented out
        'PLAYER_RATING_SCORING_WEIGHT',
        'TEAM_QUALITY_SCORING_WEIGHT',
        'TEAM_QUALITY_MIN_WEEKS',
        'PERFORMANCE_SCORING_WEIGHT',
        'PERFORMANCE_SCORING_STEPS',
        'PERFORMANCE_MIN_WEEKS',
        'MATCHUP_IMPACT_SCALE',
        'MATCHUP_SCORING_WEIGHT',
        'MATCHUP_MIN_WEEKS',
        'TEMPERATURE_IMPACT_SCALE',
        'TEMPERATURE_SCORING_WEIGHT',
        'WIND_IMPACT_SCALE',
        'WIND_SCORING_WEIGHT',
        'LOCATION_HOME',
        'LOCATION_AWAY',
        'LOCATION_INTERNATIONAL',
    ]
```

### Where PARAMETER_ORDER is Used

1. **ConfigGenerator.generate_iterative_combinations()** (line 800):
   - Validates `param_name in self.PARAMETER_ORDER`
   - Uses `len(self.PARAMETER_ORDER)` for capping
   - Uses `self.PARAMETER_ORDER` for random sampling

2. **SimulationManager._detect_resume_state()** (line 547):
   - `param_order = self.config_generator.PARAMETER_ORDER`
   - Uses for resume validation

3. **SimulationManager.run_iterative_optimization()** (line 649):
   - `param_order = self.config_generator.PARAMETER_ORDER`
   - Uses to iterate through parameters

---

## Resolved Implementation Details

### Q1: Default Value Strategy - RESOLVED

**Decision:** Option B - Require explicit passing (no default)
- `parameter_order` is a **required** parameter in `ConfigGenerator.__init__()` and `SimulationManager.__init__()`
- No default value - callers must explicitly provide the list
- The class constant `PARAMETER_ORDER` will be **removed** from ConfigGenerator

### Q2: Backward Compatibility - RESOLVED

**Decision:** Option B - Deprecate class constant, update all tests
- Remove `PARAMETER_ORDER` class constant from ConfigGenerator
- Only instance variable `self.parameter_order` exists
- Update all tests to pass `parameter_order` explicitly or access via instance

### Q3: Validation - RESOLVED

**Decision:** Option A - Validate at init time
- In `ConfigGenerator.__init__()`, validate each parameter name in `parameter_order`
- Check that each name exists in `PARAM_DEFINITIONS`
- Raise `ValueError` with clear message if unknown parameter found

**Implementation:**
```python
def __init__(self, baseline_config_path: Path, parameter_order: List[str],
             num_test_values: int = 5, num_parameters_to_test: int = 1) -> None:
    # Validate parameter_order
    unknown_params = [p for p in parameter_order if p not in self.PARAM_DEFINITIONS]
    if unknown_params:
        raise ValueError(f"Unknown parameters in parameter_order: {unknown_params}")

    self.parameter_order = parameter_order
    # ... rest of init
```

---

## Implementation Notes

### Files to Modify

1. **`simulation/ConfigGenerator.py`**
   - Add `parameter_order` param to `__init__()`
   - Store as `self.parameter_order` instance variable
   - Update all uses of `self.PARAMETER_ORDER` to `self.parameter_order`

2. **`simulation/SimulationManager.py`**
   - Add `parameter_order` param to `__init__()`
   - Pass to `ConfigGenerator.__init__()`

3. **`run_simulation.py`**
   - Define `PARAMETER_ORDER` at top of file
   - Pass to `SimulationManager.__init__()`

4. **`run_draft_order_loop.py`**
   - Define `PARAMETER_ORDER` at top of file
   - Pass to `SimulationManager.__init__()`

5. **`tests/simulation/test_config_generator.py`**
   - Update tests that reference `ConfigGenerator.PARAMETER_ORDER`

6. **`tests/simulation/test_simulation_manager.py`**
   - Update tests that mock `PARAMETER_ORDER`

### Dependencies

- No new external dependencies
- Internal changes only

### Reusable Code

- Current `PARAMETER_ORDER` definition can be copied to runner scripts

### Testing Strategy

- Verify all 2200+ tests pass after changes
- Add tests for passing custom parameter order
- Add tests for default behavior when not passed

---

## Status: READY FOR IMPLEMENTATION
