# Passing Parameter Order - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `passing_parameter_order_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Q1: Default Value Strategy:** Should PARAMETER_ORDER have a default if not passed?
  - ~~Option A: Use class constant as default (backward compatible)~~
  - **RESOLVED: Option B** - Require explicit passing (no default)

- [x] **Q2: Backward Compatibility for Tests:** How to handle tests accessing class constant?
  - ~~Option A: Keep class constant AND instance variable~~
  - **RESOLVED: Option B** - Deprecate class constant, update all tests

- [x] **Q3: Validation:** Should we validate parameter names exist in PARAM_DEFINITIONS?
  - **RESOLVED: Option A** - Yes, validate at init time
  - ~~Option B: No, trust caller~~

---

## Architecture Questions

- [ ] **Method Signature for ConfigGenerator.__init__:** Where in the parameter list should `parameter_order` go?
  - Current: `__init__(self, baseline_config_path: Path, num_test_values: int = 5, num_parameters_to_test: int = 1)`
  - Options: Before or after optional params, with default or without?

- [ ] **Method Signature for SimulationManager.__init__:** Where in the parameter list should `parameter_order` go?
  - Current signature has many parameters already

---

## Implementation Details

### ConfigGenerator Changes

| Task | Status | Notes |
|------|--------|-------|
| Add `parameter_order` parameter to `__init__()` | [ ] | |
| Store as instance variable `self.parameter_order` | [ ] | |
| Update `generate_iterative_combinations()` line 800 | [ ] | Uses for validation |
| Update `generate_iterative_combinations()` line 809 | [ ] | Uses `len()` for capping |
| Update `generate_iterative_combinations()` line 831 | [ ] | Uses for random sampling |
| Decide: Keep or remove class constant? | [ ] | Depends on Q2 |

### SimulationManager Changes

| Task | Status | Notes |
|------|--------|-------|
| Add `parameter_order` parameter to `__init__()` | [ ] | |
| Pass to `ConfigGenerator.__init__()` | [ ] | |
| Update `_detect_resume_state()` line 547 | [ ] | Already uses instance access |
| Update `run_iterative_optimization()` line 649 | [ ] | Already uses instance access |

### Runner Script Changes

| Task | Status | Notes |
|------|--------|-------|
| Define `PARAMETER_ORDER` in `run_simulation.py` | [ ] | At top of file |
| Pass to `SimulationManager` in `run_simulation.py` | [ ] | 3 places: single/full/iterative modes |
| Define `PARAMETER_ORDER` in `run_draft_order_loop.py` | [ ] | At top of file |
| Pass to `SimulationManager` in `run_draft_order_loop.py` | [ ] | 1 place |

### Test Updates

| Task | Status | Notes |
|------|--------|-------|
| Update `test_config_generator.py` tests | [ ] | Multiple tests access class constant |
| Update `test_simulation_manager.py` tests | [ ] | Mock tests set PARAMETER_ORDER |
| Add new test for custom parameter_order | [ ] | |
| Add new test for default behavior | [ ] | |

---

## Edge Cases

- [ ] **Empty parameter_order:** What happens if caller passes empty list?
- [ ] **Invalid parameter names:** What happens if caller passes unknown parameter?
- [ ] **Duplicate parameters:** What happens if same parameter appears twice?
- [ ] **Resume with different order:** What happens if PARAMETER_ORDER changes between runs?

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Current PARAMETER_ORDER | ConfigGenerator class constant | Verified (lines 191-225) |
| PARAM_DEFINITIONS | ConfigGenerator class constant | Verified (lines 88-137) |
| Usage in SimulationManager | Instance access pattern | Verified (lines 547, 649) |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Q1: Default Value Strategy | Option B - Require explicit passing | 2025-12-13 |
| Q2: Backward Compatibility | Option B - Deprecate class constant, update all tests | 2025-12-13 |
| Q3: Validation | Option A - Validate at init time | 2025-12-13 |
