# Issue #002: config_value Showing null in Horizon Files

**Created:** 2026-01-09
**Status:** 🔴 OPEN
**Priority:** MEDIUM (Feature enhancement not working as expected)
**Discovered During:** Stage 6c - User Testing (Loop Back after Issue #001)
**Current Phase:** Investigation Round 1 - Code Tracing

---

## Issue Description

**Symptoms:**
1. config_value field shows null in all horizon files
2. Expected to show actual parameter value tested (e.g., 0.25, 3.9)
3. Affects all output files: week1-5.json, week6-9.json, etc.

**Discovered During:**
User testing after Issue #001 fix - checking simulation output files

**Reproduction:**
```bash
# Run accuracy simulation
python run_simulation.py

# Check output
cat simulation/simulation_configs/accuracy_intermediate_*/week1-5.json
# Shows: "config_value": null (should show actual value)
```

**Impact:**
MEDIUM - Feature enhancement not working, but doesn't block epic goal

**Example Output (Incorrect):**
```json
"performance_metrics": {
  "mae": 4.5988,
  "player_count": 6304,
  "config_value": null,  // WRONG - should show parameter value
  "ranking_metrics": {
    "pairwise_accuracy": 0.6147,
    ...
  }
}
```

**Expected Output:**
```json
"performance_metrics": {
  "mae": 4.5988,
  "player_count": 6304,
  "config_value": 3.9,  // Should show actual parameter value tested
  "ranking_metrics": {
    "pairwise_accuracy": 0.6147,
    ...
  }
}
```

---

## Investigation Round 1: Code Tracing

**Date:** 2026-01-09
**Objective:** Identify why config_value extraction is failing

### Hypothesis

**Primary Theory:**
The param_name is not being passed to AccuracyConfigPerformance when creating best_configs, so _extract_param_value() can't determine which parameter to extract.

**Chain of events:**
1. Simulation evaluates config with specific parameter
2. Creates AccuracyResult, converts to AccuracyConfigPerformance
3. AccuracyConfigPerformance.__init__() called WITHOUT param_name
4. _extract_param_value() gets None for param_name → returns None
5. config_value = None saved to JSON

### Areas to Investigate

1. **Where AccuracyConfigPerformance is created:**
   - AccuracyResultsManager._evaluate_config_weekly() (converts AccuracyResult)
   - AccuracySimulationManager.run_both() (gets best configs)

2. **Where param_name should come from:**
   - AccuracySimulationManager knows which parameter is being tested
   - Need to trace how parameter name gets to AccuracyConfigPerformance

3. **Check AccuracyResult to AccuracyConfigPerformance conversion:**
   - Does AccuracyResult have param_name field?
   - Is it passed during conversion?

---

## Next Steps

1. Read AccuracySimulationManager.py to see how parameter name is tracked
2. Read AccuracyResultsManager.py to see AccuracyResult → AccuracyConfigPerformance conversion
3. Identify where param_name needs to be added
4. Design fix
5. Implement and test

---

## Solution Implementation

**Date:** 2026-01-09
**Root Cause Confirmed:** param_name not passed to add_result() in weekly optimization

### Solution Design

**Single fix required:**

**Fix `run_weekly_optimization()` (AccuracySimulationManager.py:667)**
   - Current: `add_result(week_key, config_dict, result)` - NO param_name passed
   - Fix: Pass param_name and test_idx to enable config_value extraction
   - Rationale: _extract_param_value() needs param_name to find value in config

### Implementation

**Change: Pass param_name to add_result()**

Before (simulation/accuracy/AccuracySimulationManager.py:667):
```python
# Record result
is_new_best = self.results_manager.add_result(week_key, config_dict, result)
```

After:
```python
# Record result (pass param_name and test_idx for config_value extraction)
is_new_best = self.results_manager.add_result(
    week_key, config_dict, result,
    param_name=param_name,
    test_idx=test_idx
)
```

**Tests:** ✅ All 2,486 tests passing (100%)

**Files Modified:**
- simulation/accuracy/AccuracySimulationManager.py (line 667, 3 lines changed)

---

## User Verification

**User Verification:** ✅ CONFIRMED FIXED
**Verified By:** User
**Verified Date:** 2026-01-09
**User Feedback:** "they are both working"

**Verification Results:**

✅ config_value field now shows actual parameter values instead of null
✅ Output files (week1-5.json, etc.) contain meaningful config_value data

**Status:** RESOLVED ✅
