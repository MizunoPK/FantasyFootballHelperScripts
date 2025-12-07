# Simulation Parameter Precision

## Objective

Modify the simulation's parameter value generation to produce values at discrete precision levels derived from the min/max values in `PARAM_DEFINITIONS`, rather than arbitrary floats from `random.uniform()`.

---

## High-Level Requirements

### 1. Explicit Precision in PARAM_DEFINITIONS

Change `PARAM_DEFINITIONS` from 2-tuples to 3-tuples with explicit precision:
```python
# Old format: (min, max)
PARAM_DEFINITIONS = {
    'NORMALIZATION_MAX_SCALE': (100, 175),
    'SAME_POS_BYE_WEIGHT': (0.0, 0.5),
}

# New format: (min, max, precision)
PARAM_DEFINITIONS = {
    'NORMALIZATION_MAX_SCALE': (100, 175, 0),      # Integer (precision 0)
    'SAME_POS_BYE_WEIGHT': (0.0, 0.5, 1),          # 1 decimal place
    'PERFORMANCE_SCORING_STEPS': (0.10, 0.40, 2),  # 2 decimal places
}
```

This eliminates ambiguity about intended precision (trailing zeros matter).

### 2. Discrete Value Generation

Replace `random.uniform(min_val, max_val)` with selection from discrete set:
```python
# Current (arbitrary floats):
rand_val = random.uniform(0.0, 0.5)  # e.g., 0.2847362

# New (precision-aware):
possible_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
rand_val = random.choice(possible_values)  # e.g., 0.3
```

### 3. Test Value Capping

If `num_test_values` exceeds the number of possible discrete values, cap at available values:
```python
# Example: SAME_POS_BYE_WEIGHT (0.0, 0.5) with precision 1 → 6 possible values
# If num_test_values=50, only return 6 values (all possible ones)
```

### 4. Output/Deliverables

Modified `ConfigGenerator` class with precision-aware value generation.

---

## Resolved Implementation Details

### Algorithm/Logic Decisions

1. **Precision specification:** Use explicit precision in PARAM_DEFINITIONS as 3-tuples
   - Format: `(min, max, precision)`
   - Example: `'SAME_POS_BYE_WEIGHT': (0.0, 0.5, 1)` for 1 decimal place
   - Eliminates all detection/inference complexity

2. **Integer parameter handling:** Use precision=0
   - Example: `'NORMALIZATION_MAX_SCALE': (100, 175, 0)` → generates integers
   - No special detection needed - explicitly specified

3. **Mixed precision:** Not applicable
   - With explicit precision, there's no ambiguity
   - User specifies the exact precision level

### Architecture Decisions

4. **Precision storage:** In PARAM_DEFINITIONS itself (3rd tuple element)
   - Helper function `_generate_discrete_range(min_val, max_val, precision)` generates values
   - No separate module needed

5. **Unify with existing discrete method:**
   - `generate_discrete_parameter_values()` will be merged into precision-aware approach
   - DRAFT_ORDER_FILE uses precision=0 like other integers
   - File-loading logic moves into the unified method

### Edge Case Handling

6. **Full enumeration behavior:** When `num_test_values >= len(possible_values)`
   - Return ALL possible values in order
   - Include optimal value first
   - Remaining values in ascending order
   - Deterministic ordering for reproducibility

7. **Optimal value handling:** When returning subset
   - Always include optimal value first
   - Then random sample from remaining possible values

8. **Floating-point precision errors:**
   - Use `round(value, precision)` after each step
   - Standard library `round()` sufficient for 0-2 decimal places

9. **Zero edge case:** Not applicable
   - Precision is explicit, not inferred from values

### Testing Requirements

10. **Test coverage:** Comprehensive
    - Unit tests for `_generate_discrete_range()` helper
    - Unit tests for `generate_parameter_values()` with precision levels 0, 1, 2
    - Edge case tests: full enumeration, optimal value inclusion
    - Tests verifying each PARAM_DEFINITIONS entry generates valid values
    - Integration tests confirming generated configs contain discrete values

---

## Implementation Notes

### Files to Modify

- `simulation/ConfigGenerator.py:449-482` - `generate_parameter_values()` method
- Possibly `simulation/ConfigGenerator.py:484-519` - `generate_discrete_parameter_values()` if unifying

### Current Code Reference

**`ConfigGenerator.generate_parameter_values()` (lines 449-482):**
```python
def generate_parameter_values(
    self,
    param_name: str,
    optimal_val: float,
    min_val: float,
    max_val: float
) -> List[float]:
    values = [optimal_val]
    for _ in range(self.num_test_values):
        rand_val = random.uniform(min_val, max_val)  # ← Change this
        values.append(rand_val)
    return values
```

### Final Algorithm

```python
# PARAM_DEFINITIONS with explicit precision (3-tuples)
PARAM_DEFINITIONS = {
    'NORMALIZATION_MAX_SCALE': (100, 175, 0),      # precision 0 = integers
    'SAME_POS_BYE_WEIGHT': (0.0, 0.5, 1),          # precision 1 = 0.1 steps
    'PERFORMANCE_SCORING_STEPS': (0.10, 0.40, 2),  # precision 2 = 0.01 steps
    # ... all other parameters
}

def _generate_discrete_range(min_val: float, max_val: float, precision: int) -> List[float]:
    """Generate all possible values at given precision."""
    step = 10 ** (-precision)
    values = []
    current = min_val
    while current <= max_val + step / 2:  # Account for floating-point
        values.append(round(current, precision) if precision > 0 else int(round(current)))
        current += step
    return values

def generate_parameter_values(
    self,
    param_name: str,
    optimal_val: float,
    min_val: float,
    max_val: float,
    precision: int  # New parameter
) -> List[float]:
    """Generate discrete parameter values at specified precision."""
    possible_values = _generate_discrete_range(min_val, max_val, precision)

    if self.num_test_values >= len(possible_values):
        # Return all values, with optimal first
        if optimal_val in possible_values:
            values = [optimal_val] + [v for v in possible_values if v != optimal_val]
        else:
            values = possible_values
        return values
    else:
        # Sample subset, optimal first
        values = [optimal_val]
        remaining = [v for v in possible_values if v != optimal_val]
        values.extend(random.sample(remaining, min(self.num_test_values - 1, len(remaining))))
        return values
```

### Testing Strategy

- Unit tests for precision detection with various inputs
- Unit tests for discrete range generation
- Integration tests verifying correct values are generated for each PARAM_DEFINITIONS entry
- Edge case tests for floating-point precision issues

---

## Status: READY FOR IMPLEMENTATION
