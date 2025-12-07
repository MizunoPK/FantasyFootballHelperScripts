# Simulation Parameter Precision - Implementation TODO

## Iteration Progress Tracker

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 COMPLETE |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 COMPLETE |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 COMPLETE |

**ALL 24 ITERATIONS COMPLETE - READY TO IMPLEMENT**

---

## Protocol Execution Tracker

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [x]1 [x]2 [x]3 [x]8 [x]9 [x]10 [x]15 [x]16 |
| Algorithm Traceability | 4, 11, 19 | [x]4 [x]11 [x]19 |
| End-to-End Data Flow | 5, 12 | [x]5 [x]12 |
| Skeptical Re-verification | 6, 13, 22 | [x]6 [x]13 [x]22 |
| Integration Gap Check | 7, 14, 23 | [x]7 [x]14 [x]23 |
| Fresh Eyes Review | 17, 18 | [x]17 [x]18 |
| Edge Case Verification | 20 | [x]20 |
| Test Coverage Planning | 21 | [x]21 |
| Implementation Readiness | 24 | [x]24 |

---

## Verification Summary

- Iterations completed: 24/24 ✓
- Requirements from spec: 10
- Requirements in TODO: 10
- Questions for user: 0 (all resolved in planning)
- Integration points identified: 3
- Tests to update: 5 (4 existing + 1 to remove)
- New tests to add: 6 edge case tests
- **READY FOR IMPLEMENTATION**

---

## Phase 1: Update PARAM_DEFINITIONS Structure

### Task 1.1: Change PARAM_DEFINITIONS from 2-tuples to 3-tuples
- **File:** `simulation/ConfigGenerator.py`
- **Lines:** 84-133 (PARAM_DEFINITIONS dict)
- **Tests:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Implementation details:**
Change format from `(min, max)` to `(min, max, precision)`:
```python
PARAM_DEFINITIONS = {
    'NORMALIZATION_MAX_SCALE': (100, 175, 0),      # precision 0 = integers
    'SAME_POS_BYE_WEIGHT': (0.0, 0.5, 1),          # precision 1 = 0.1 steps
    'ADP_SCORING_WEIGHT': (1.00, 4.00, 2),         # precision 2 = 0.01 steps
    # ... all other parameters
}
```

**Precision assignments (from checklist analysis):**
- Integer params (precision=0): NORMALIZATION_MAX_SCALE, PRIMARY_BONUS, SECONDARY_BONUS, DRAFT_ORDER_FILE, ADP_SCORING_STEPS, TEAM_QUALITY_MIN_WEEKS, PERFORMANCE_MIN_WEEKS, MATCHUP_MIN_WEEKS, MATCHUP_IMPACT_SCALE
- 1 decimal (precision=1): SAME_POS_BYE_WEIGHT, DIFF_POS_BYE_WEIGHT
- 2 decimals (precision=2): ADP_SCORING_WEIGHT, PLAYER_RATING_SCORING_WEIGHT, TEAM_QUALITY_SCORING_WEIGHT, PERFORMANCE_SCORING_WEIGHT, PERFORMANCE_SCORING_STEPS, MATCHUP_SCORING_WEIGHT, TEMPERATURE_IMPACT_SCALE, TEMPERATURE_SCORING_WEIGHT, WIND_IMPACT_SCALE, WIND_SCORING_WEIGHT, LOCATION_HOME, LOCATION_AWAY, LOCATION_INTERNATIONAL

---

## Phase 2: Create Discrete Range Generator

### Task 2.1: Add `_generate_discrete_range()` helper method
- **File:** `simulation/ConfigGenerator.py`
- **Location:** Before `generate_parameter_values()` (around line 448)
- **Tests:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Implementation:**
```python
def _generate_discrete_range(self, min_val: float, max_val: float, precision: int) -> List[float]:
    """
    Generate all possible values at given precision.

    Args:
        min_val: Minimum value
        max_val: Maximum value
        precision: Number of decimal places (0 for integers)

    Returns:
        List of all discrete values from min to max at specified precision
    """
    step = 10 ** (-precision)
    values = []
    current = min_val
    while current <= max_val + step / 2:  # Account for floating-point
        if precision == 0:
            values.append(int(round(current)))
        else:
            values.append(round(current, precision))
        current += step
    return values
```

---

## Phase 3: Unify Value Generation Methods

### Task 3.1: Modify `generate_parameter_values()` to use precision-aware logic
- **File:** `simulation/ConfigGenerator.py`
- **Lines:** 449-482
- **Tests:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Implementation:**
```python
def generate_parameter_values(
    self,
    param_name: str,
    optimal_val: float,
    min_val: float,
    max_val: float,
    precision: int
) -> List[float]:
    """
    Generate discrete parameter values at specified precision.

    Args:
        param_name: Parameter name (for logging)
        optimal_val: Optimal/baseline value
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        precision: Decimal places (0 for integers)

    Returns:
        List of values: optimal first, then remaining values
    """
    possible_values = self._generate_discrete_range(min_val, max_val, precision)

    if self.num_test_values >= len(possible_values):
        # Full enumeration: return ALL values, optimal first
        if optimal_val in possible_values:
            values = [optimal_val] + [v for v in possible_values if v != optimal_val]
        else:
            values = possible_values
    else:
        # Subset: optimal first, then random samples
        values = [optimal_val]
        remaining = [v for v in possible_values if v != optimal_val]
        values.extend(random.sample(remaining, min(self.num_test_values, len(remaining))))

    self.logger.debug(f"{param_name}: {len(values)} values (precision={precision})")
    return values
```

### Task 3.2: Remove or deprecate `generate_discrete_parameter_values()`
- **File:** `simulation/ConfigGenerator.py`
- **Lines:** 484-518
- **Tests:** Update tests that call this method
- **Status:** [ ] Not started

**Implementation:**
- Method can be removed since DRAFT_ORDER_FILE will use precision=0
- Need to update `_load_draft_order_from_file()` integration

### Task 3.3: Update all callers to pass precision parameter
- **File:** `simulation/ConfigGenerator.py`
- **Status:** [ ] Not started

**Callers to update:**
- `create_config_dict()` - when generating parameter values
- Any other methods that call `generate_parameter_values()`

---

## Phase 4: Handle DRAFT_ORDER_FILE Special Case

### Task 4.1: Integrate DRAFT_ORDER loading with unified method
- **File:** `simulation/ConfigGenerator.py`
- **Status:** [ ] Not started

**Implementation:**
- DRAFT_ORDER_FILE uses precision=0 (integers 1-100)
- When generating configs, load DRAFT_ORDER array for each file number
- Keep `_load_draft_order_from_file()` helper

---

## Phase 5: Update Tests

### Task 5.1: Unit tests for `_generate_discrete_range()`
- **File:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Tests needed:**
- precision=0: generates integers
- precision=1: generates 0.1 steps
- precision=2: generates 0.01 steps
- Edge: min==max returns single value
- Edge: floating-point precision (0.1 + 0.1 + 0.1 = 0.3)

### Task 5.2: Unit tests for updated `generate_parameter_values()`
- **File:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Tests needed:**
- Full enumeration case (num_test_values >= possible_values)
- Subset case with optimal first
- precision=0, 1, 2 variations
- Optimal value is always first

### Task 5.3: Tests for each PARAM_DEFINITIONS entry
- **File:** `tests/simulation/test_config_generator.py`
- **Status:** [ ] Not started

**Tests needed:**
- Each parameter generates valid discrete values
- Values match expected precision
- Range is correct (min to max inclusive)

### Task 5.4: Integration tests for config generation
- **File:** `tests/simulation/test_config_generator.py` or `tests/integration/test_simulation_integration.py`
- **Status:** [ ] Not started

**Tests needed:**
- Generated configs contain discrete values (not arbitrary floats)
- End-to-end: run simulation manager with precision-aware generation

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| `_generate_discrete_range()` | ConfigGenerator.py | `generate_parameter_values()` | ConfigGenerator.py:~460 | Task 3.1 |
| Updated `generate_parameter_values()` | ConfigGenerator.py | `create_config_dict()` | ConfigGenerator.py | Task 3.3 |
| Updated `PARAM_DEFINITIONS` | ConfigGenerator.py | Multiple methods | ConfigGenerator.py | Task 1.1 |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Requirement 1 | Explicit precision in 3-tuples | PARAM_DEFINITIONS | N/A (data structure) |
| Requirement 6 | Full enumeration: all values, optimal first | generate_parameter_values() | if num_test >= possible |
| Requirement 7 | Subset: optimal first, random samples | generate_parameter_values() | else branch |
| Requirement 8 | Use round() for floating-point | _generate_discrete_range() | round(current, precision) |

---

## Data Flow Traces

### Requirement: Precision-aware value generation
```
Entry: run_simulation.py
  → SimulationManager.run_full_optimization()
  → ConfigGenerator.generate_configs_for_parameter()
  → ConfigGenerator.generate_parameter_values()  ← MODIFIED
  → ConfigGenerator._generate_discrete_range()   ← NEW
  → Output: List of discrete values
```

### Requirement: Config dict creation with precision
```
Entry: run_simulation.py
  → SimulationManager
  → ConfigGenerator.create_config_dict()
  → Uses PARAM_DEFINITIONS (min, max, precision)  ← MODIFIED
  → Output: Config dict with discrete parameter values
```

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:** (to be filled)
- **Corrections made:** (to be filled)
- **Confidence level:** (to be filled)

### Round 2 (Iteration 13)
- **Verified correct:** (to be filled)
- **Corrections made:** (to be filled)
- **Confidence level:** (to be filled)

### Round 3 (Iteration 22)
- **Verified correct:** (to be filled)
- **Corrections made:** (to be filled)
- **Confidence level:** (to be filled)

---

## Progress Notes

**Last Updated:** 2025-12-07
**Current Status:** Executing first verification round
**Next Steps:** Complete iterations 1-7, create questions file if needed
**Blockers:** None

---

## Iteration Notes

### Iteration 1: Files & Patterns
- **File to modify:** Only `simulation/ConfigGenerator.py`
- **Pattern discovered:** PARAM_DEFINITIONS is unpacked with `min_val, max_val = self.param_definitions[param_name]` in many places (lines 910, 913, 916, 937, 945, 953, 961, 968)
- **Impact:** With 3-tuples, need to update all unpacking sites to `min_val, max_val, precision = ...`
- **Callers of generate_parameter_values:** Lines 558, 583, 590, 597, 604, 611, 643, 656, 668, 684, 693, 706, 973
- **Callers using `*` unpacking:** These will automatically pass all 3 values if method signature changes

### Iteration 2: Error Handling
- Current `generate_parameter_values` has no error handling beyond logging
- New method should handle edge case: precision generates empty range (shouldn't happen with valid ranges)
- Logging already in place via `self.logger.debug()`
- No new error handling needed for this feature

### Iteration 3: Integration Points
- **Test file:** `tests/simulation/test_config_generator.py`
- **Integration:** `generate_configs_for_parameter()` is the main integration point called by SimulationManager
- **Mocking needed:** Tests should mock file system for DRAFT_ORDER files

### Iteration 4: Algorithm Traceability Matrix
| Spec Requirement | Algorithm | Code Location | Status |
|------------------|-----------|---------------|--------|
| Explicit 3-tuples | Change PARAM_DEFINITIONS structure | ConfigGenerator.py:84-133 | TODO |
| Generate discrete range | Increment by step, round each | `_generate_discrete_range()` (new) | TODO |
| Full enumeration: all values | If num_test >= possible, return all | `generate_parameter_values()` | TODO |
| Optimal first | Place optimal at index 0 | `generate_parameter_values()` | TODO |
| Subset: random sample | Sample from remaining after optimal | `generate_parameter_values()` | TODO |
| Use round() | `round(current, precision)` | `_generate_discrete_range()` | TODO |
| Unify methods | Merge discrete into precision-aware | Remove `generate_discrete_parameter_values()` | TODO |

### Iteration 5: End-to-End Data Flow
**Trace 1: Iterative optimization**
```
run_simulation.py (entry)
  → SimulationManager.run_iterative_optimization()
  → SimulationManager._run_single_iteration()
  → ConfigGenerator.generate_configs_for_parameter()  ← Calls generate_parameter_values() at line 973
  → ConfigGenerator.generate_parameter_values()  ← MODIFY: add precision param
  → ConfigGenerator._generate_discrete_range()  ← NEW method
  → Returns: discrete test values
```

**Trace 2: Full optimization**
```
run_simulation.py (entry)
  → SimulationManager.run_full_optimization()
  → ConfigGenerator.generate_all_parameter_value_sets()  ← Uses * unpacking
  → ConfigGenerator.generate_parameter_values()  ← MODIFY
  → Returns: value sets dict
```

All paths verified - no orphan code expected.

### Iteration 6: Skeptical Re-verification
**Assumptions challenged:**
1. ✓ PARAM_DEFINITIONS tuple unpacking works with 3-tuples (verified: `*tuple` unpacking passes all elements)
2. ✓ `round()` handles all precision levels 0-2 (verified: Python's round() works for all)
3. ⚠️ Need to verify: Does DRAFT_ORDER_FILE special case still work after removing `generate_discrete_parameter_values()`?
   - **Answer:** Yes, if DRAFT_ORDER_FILE uses precision=0, the unified method handles it
4. ⚠️ Need to verify: Are there any places that check tuple length?
   - **Answer:** No length checks found in code - safe to add 3rd element

**Corrections made:** None needed - all assumptions verified

### Iteration 7: Integration Gap Check
| New Method | Called By | Task Reference |
|------------|-----------|----------------|
| `_generate_discrete_range()` | `generate_parameter_values()` | Task 3.1 |
| Updated `generate_parameter_values()` | `generate_all_parameter_value_sets()`, `generate_configs_for_parameter()`, `generate_multiplier_parameter_values()` | Already integrated |

**Orphan code check:** No orphan code will be created - new method is immediately called by existing methods

### Iteration 8-10: Re-verification with Complete Spec
**Tests that need updating (existing tests call generate_parameter_values with 4 args, need 5):**
- `test_generate_parameter_values_correct_count` (line 311)
- `test_generate_parameter_values_includes_optimal` (line 320)
- `test_generate_parameter_values_respects_bounds` (line 329)
- `test_generate_parameter_values_random_variation` (line 338)

**Tests to remove/replace:**
- `test_generate_discrete_parameter_values` (line 786) - method being unified

**Dependency check:**
- No external dependencies added
- No new imports needed (uses standard library only)

### Iteration 11: Algorithm Traceability (Round 2)
Verified all spec requirements map to code:
| Requirement | Code Task | Verified |
|-------------|-----------|----------|
| 3-tuples | Task 1.1 | ✓ |
| _generate_discrete_range() | Task 2.1 | ✓ |
| Full enumeration | Task 3.1 | ✓ |
| Subset with optimal | Task 3.1 | ✓ |
| Unify methods | Tasks 3.2, 3.3 | ✓ |

### Iteration 12: End-to-End Data Flow (Round 2)
Re-traced with test updates:
```
run_simulation.py
  → SimulationManager
  → ConfigGenerator.generate_configs_for_parameter()
  → ConfigGenerator.generate_parameter_values(param, opt, min, max, precision)  ← 5 args
  → ConfigGenerator._generate_discrete_range(min, max, precision)
  → Returns: discrete values matching precision
```

### Iteration 13: Skeptical Re-verification (Round 2)
**Challenged assumptions:**
1. ✓ Test fixtures don't need precision - they DO need updating (4→5 args)
2. ✓ No tests check tuple length - verified, safe to extend
3. ✓ DRAFT_ORDER_FILE special case works - uses precision=0

**Corrections needed:**
- Add precision parameter to all test calls

### Iteration 14: Integration Gap Check (Round 2)
| Component | Caller | Status |
|-----------|--------|--------|
| Updated PARAM_DEFINITIONS | All methods using self.param_definitions | Verified |
| Updated generate_parameter_values | generate_all_parameter_value_sets, generate_single_parameter_configs | Verified |
| New _generate_discrete_range | generate_parameter_values | Verified |

### Iterations 15-16: Final Preparation
**Integration checklist created:**
- [ ] Update PARAM_DEFINITIONS to 3-tuples
- [ ] Add _generate_discrete_range() method
- [ ] Modify generate_parameter_values() signature and logic
- [ ] Update all tuple unpacking sites (8 locations)
- [ ] Remove generate_discrete_parameter_values()
- [ ] Update DRAFT_ORDER_FILE handling to use unified method
- [ ] Update existing tests for 5-arg signature
- [ ] Add new tests for precision levels 0, 1, 2
- [ ] Add tests for full enumeration case
- [ ] Add tests verifying each PARAM_DEFINITIONS entry

### Iterations 17-18: Fresh Eyes Review
**Re-read spec as if first time:**
- Spec is clear and complete
- All 10 requirements mapped to tasks
- Edge cases covered: full enumeration, optimal first, floating-point rounding
- No ambiguities found

### Iteration 19: Algorithm Deep Dive
**Exact spec quotes verified:**
1. "Format: `(min, max, precision)`" → Task 1.1 creates this format
2. "_generate_discrete_range(min_val, max_val, precision)" → Task 2.1 creates this method
3. "Return ALL possible values in order" → Task 3.1 implements this logic
4. "Always include optimal value first" → Task 3.1 ensures optimal is index 0
5. "Use `round(value, precision)` after each step" → Task 2.1 uses round()

### Iteration 20: Edge Case Verification
| Edge Case | Task | Test |
|-----------|------|------|
| precision=0 (integers) | Task 1.1, 2.1 | test_precision_zero_integers |
| precision=1 (0.1 steps) | Task 1.1, 2.1 | test_precision_one_decimals |
| precision=2 (0.01 steps) | Task 1.1, 2.1 | test_precision_two_decimals |
| Full enumeration | Task 3.1 | test_full_enumeration_returns_all |
| min == max | Task 2.1 | test_single_value_range |
| Floating-point 0.1+0.1+0.1=0.3 | Task 2.1 | test_floating_point_precision |

### Iteration 21: Test Coverage Planning
**Tests to write (avoiding anti-patterns):**
1. Unit tests for `_generate_discrete_range()` - test actual output values
2. Unit tests for `generate_parameter_values()` - test with real objects, not mocks
3. Tests that verify OUTPUT CONTENT, not just existence
4. Tests for parameter dependencies (DRAFT_ORDER_FILE → DRAFT_ORDER array)
5. Integration test that runs actual config generation

**Anti-patterns avoided:**
- ✓ No heavy mocking of internal classes
- ✓ Tests validate content, not just structure
- ✓ All edge cases have explicit tests

### Iteration 22: Skeptical Re-verification #3
**Final assumption check:**
1. ✓ All PARAM_DEFINITIONS can be assigned valid precision (reviewed each one)
2. ✓ No code paths skip the new precision parameter
3. ✓ Tests will catch regressions in existing behavior
4. ✓ DRAFT_ORDER_FILE integration still works with unified method

**Confidence: HIGH** - Implementation is straightforward

### Iteration 23: Integration Gap Check #3
**Final orphan code check:**
| New Code | Caller | Entry Point | Status |
|----------|--------|-------------|--------|
| _generate_discrete_range() | generate_parameter_values() | run_simulation.py | ✓ |
| Updated generate_parameter_values() | Multiple callers | run_simulation.py | ✓ |
| Updated PARAM_DEFINITIONS | self.param_definitions | run_simulation.py | ✓ |

**No orphan code** - all new code is integrated

### Iteration 24: Implementation Readiness Checklist
**READY TO IMPLEMENT**

- [x] All spec requirements have corresponding tasks
- [x] All tasks have specific file locations
- [x] All edge cases identified with tests
- [x] Integration matrix complete
- [x] No orphan code risk
- [x] Test anti-patterns avoided
- [x] Data flow verified end-to-end
- [x] Algorithm traceability complete
