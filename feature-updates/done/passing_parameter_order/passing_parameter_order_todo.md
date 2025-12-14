# Passing Parameter Order - Implementation TODO

## Iteration Progress Tracker

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [x]1 [x]2 [x]3 [x]4 [x]5 [x]6 [x]7 | 7/7 |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 |
| Third (8) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]24 | 8/8 |

**Current Iteration:** COMPLETE (24/24)

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

- Iterations completed: 24/24
- Requirements from spec: 4 (Q1-Q3 decisions + implementation)
- Questions for user: 0 (all resolved in planning)
- Integration points identified: 4
- Test files to update: ~25 test instantiations across 2 test files

---

## Phase 1: ConfigGenerator Changes

### Task 1.1: Add `parameter_order` parameter to `__init__()`
- **File:** `simulation/ConfigGenerator.py`
- **Location:** Line 391 (`__init__` method)
- **Status:** [ ] Not started

**Current signature:**
```python
def __init__(self, baseline_config_path: Path, num_test_values: int = 5, num_parameters_to_test: int = 1) -> None:
```

**New signature:**
```python
def __init__(self, baseline_config_path: Path, parameter_order: List[str],
             num_test_values: int = 5, num_parameters_to_test: int = 1) -> None:
```

**Note:** Add `from typing import List` import if not present

### Task 1.2: Add validation for `parameter_order`
- **File:** `simulation/ConfigGenerator.py`
- **Location:** Inside `__init__`, before storing
- **Status:** [ ] Not started

**Implementation:**
```python
# Validate parameter_order
unknown_params = [p for p in parameter_order if p not in self.PARAM_DEFINITIONS]
if unknown_params:
    raise ValueError(f"Unknown parameters in parameter_order: {unknown_params}")

self.parameter_order = parameter_order
```

### Task 1.3: Remove `PARAMETER_ORDER` class constant
- **File:** `simulation/ConfigGenerator.py`
- **Location:** Lines 191-225
- **Status:** [ ] Not started

**Note:** Keep the list content - will be moved to runner scripts.

### Task 1.4: Update all `self.PARAMETER_ORDER` to `self.parameter_order`
- **File:** `simulation/ConfigGenerator.py`
- **Locations:**
  - Line 800: `if param_name not in self.PARAMETER_ORDER`
  - Line 809: `max_params = len(self.PARAMETER_ORDER)`
  - Line 831: `available_params = [p for p in self.PARAMETER_ORDER if p != param_name]`
- **Status:** [ ] Not started

---

## Phase 2: SimulationManager Changes

### Task 2.1: Add `parameter_order` parameter to `__init__()`
- **File:** `simulation/SimulationManager.py`
- **Location:** `__init__` method signature
- **Status:** [ ] Not started

### Task 2.2: Pass `parameter_order` to ConfigGenerator
- **File:** `simulation/SimulationManager.py`
- **Location:** Where ConfigGenerator is instantiated
- **Status:** [ ] Not started

### Task 2.3: Verify instance access pattern
- **File:** `simulation/SimulationManager.py`
- **Locations:**
  - Line 547: `param_order = self.config_generator.PARAMETER_ORDER` → `.parameter_order`
  - Line 649: `param_order = self.config_generator.PARAMETER_ORDER` → `.parameter_order`
- **Status:** [ ] Not started

---

## Phase 3: Runner Script Changes

### Task 3.1: Define PARAMETER_ORDER in run_simulation.py
- **File:** `run_simulation.py`
- **Location:** Near top of file, after imports
- **Status:** [ ] Not started

**Content:** Copy the 22-parameter list from ConfigGenerator

### Task 3.2: Pass PARAMETER_ORDER to SimulationManager in run_simulation.py
- **File:** `run_simulation.py`
- **Locations:** Lines 320-329 (single mode), 347-355 (full mode), 378-387 (iterative mode)
- **Status:** [ ] Not started

### Task 3.3: Define PARAMETER_ORDER in run_draft_order_loop.py
- **File:** `run_draft_order_loop.py`
- **Location:** Near top of file, after imports
- **Status:** [ ] Not started

### Task 3.4: Pass PARAMETER_ORDER to SimulationManager in run_draft_order_loop.py
- **File:** `run_draft_order_loop.py`
- **Location:** Line 484-494 (SimulationManager creation)
- **Status:** [ ] Not started

---

## Phase 4: Test Updates

### Task 4.1: Update test_config_generator.py tests
- **File:** `tests/simulation/test_config_generator.py`
- **Changes needed:**
  - ~25 instantiations of `ConfigGenerator()` need `parameter_order` arg
  - ~15 references to `ConfigGenerator.PARAMETER_ORDER` need to use instance
  - Create a test fixture with a standard PARAMETER_ORDER for tests
- **Status:** [ ] Not started

**Lines with ConfigGenerator.PARAMETER_ORDER access:**
- 726, 731, 743, 747, 748, 760, 764, 765, 778, 779, 781, 784, 791, 792, 801, 805, 806, 808, 819, 822, 835, 839, 840, 850, 854, 855, 888

### Task 4.2: Update test_simulation_manager.py tests
- **File:** `tests/simulation/test_simulation_manager.py`
- **Changes needed:**
  - Mock tests that set `PARAMETER_ORDER` need updating
  - Tests that create SimulationManager need to pass `parameter_order`
- **Status:** [ ] Not started

### Task 4.3: Add new test for validation
- **File:** `tests/simulation/test_config_generator.py`
- **Test:** Verify ValueError raised for unknown parameter names
- **Status:** [ ] Not started

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| `parameter_order` param in ConfigGenerator | ConfigGenerator.py | SimulationManager.__init__() | SimulationManager.py:~100 | Task 2.2 |
| `parameter_order` param in SimulationManager | SimulationManager.py | run_simulation.py main() | run_simulation.py:320,347,378 | Task 3.2 |
| `parameter_order` param in SimulationManager | SimulationManager.py | run_draft_order_loop.py main() | run_draft_order_loop.py:484 | Task 3.4 |
| `self.parameter_order` instance var | ConfigGenerator.py | generate_iterative_combinations() | ConfigGenerator.py:800,809,831 | Task 1.4 |

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm Description | Code Location | Conditional Logic |
|--------------|----------------------|---------------|-------------------|
| Q3 Resolution | Validate param names exist in PARAM_DEFINITIONS | ConfigGenerator.__init__() | if unknown_params: raise ValueError |

---

## Data Flow Traces

### Requirement: PARAMETER_ORDER passed from runner to ConfigGenerator

```
Entry: run_simulation.py main()
  → PARAMETER_ORDER defined at top of file
  → SimulationManager.__init__(parameter_order=PARAMETER_ORDER)
  → ConfigGenerator.__init__(parameter_order=parameter_order)
  → self.parameter_order = parameter_order (after validation)
  → Used in generate_iterative_combinations()
```

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:** All task file locations, method signatures
- **Corrections made:** None - initial analysis was accurate
- **Confidence level:** High

### Round 2 (Iteration 13)
- **Verified correct:** Integration points all identified
- **Corrections made:** None
- **Confidence level:** High

### Round 3 (Iteration 22)
- **Verified correct:** All callers identified, no orphan code risk
- **Corrections made:** None
- **Confidence level:** High

---

## Progress Notes

**Last Updated:** 2025-12-13
**Current Status:** All 24 iterations complete - READY TO IMPLEMENT
**Next Steps:** Execute Phase 1-4 implementation tasks
**Blockers:** None

## Iteration Notes

### Iterations 1-3: Standard Verification
- Verified file locations: ConfigGenerator.py:191-225 (PARAMETER_ORDER), :391 (__init__)
- Verified SimulationManager.py:62-73 (__init__), :112 (ConfigGenerator instantiation)
- Verified run_simulation.py:320,347,378 (SimulationManager creations)
- Verified run_draft_order_loop.py:484 (SimulationManager creation)

### Iteration 4: Algorithm Traceability
- Only algorithm: validation of parameter names against PARAM_DEFINITIONS
- Location: ConfigGenerator.__init__() - will add validation loop

### Iteration 5: End-to-End Data Flow
- Entry: run_simulation.py → SimulationManager → ConfigGenerator → self.parameter_order
- Used in: generate_iterative_combinations() for param validation and sampling

### Iteration 7: Integration Gap Check
- All new code has callers - no orphan code risk
- parameter_order flows: runner → SimulationManager → ConfigGenerator → usage

### Iterations 17-18: Fresh Eyes Review
- Spec is clear: required param, validation, no class constant
- No ambiguity in implementation approach

### Iteration 20: Edge Cases
- Empty list: Should raise ValueError (no params to optimize)
- Unknown params: Should raise ValueError (Q3 decision)
- Duplicates: Not explicitly handled - will document as user responsibility

### Iteration 21: Test Coverage
- Need test for validation (unknown param raises ValueError)
- Need test for empty list raises error
- Existing tests need parameter_order fixture

### Iteration 24: Implementation Readiness
- All tasks identified and verified
- No blocking questions
- Ready to implement
