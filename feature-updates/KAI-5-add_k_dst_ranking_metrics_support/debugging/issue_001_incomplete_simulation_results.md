# Issue #001: Incomplete Simulation Results - Missing Ranking Metrics and Metadata

**Created:** 2026-01-09
**Status:** 🟡 INVESTIGATING
**Priority:** HIGH (Critical - breaks core epic functionality)
**Discovered During:** Stage 6c - User Testing
**Current Phase:** Investigation Round 1 - Code Tracing

---

## Issue Description

**Symptoms:**
1. metadata.json shows test_idx = -1 for all horizons
2. metadata.json only shows MAE (missing ranking_metrics)
3. No positional data in output files
4. Individual horizon files have minimal performance_metrics
5. Log shows "test_?" instead of test_idx values
6. WARNING in log: "No best config found for ros after parameter PERFORMANCE_MIN_WEEKS"

**Discovered During:**
Stage 6c - User Testing (running accuracy simulation)

**Reproduction:**
```bash
# Run accuracy simulation (tournament mode)
python run_simulation.py
# Check output files in simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/
```

**Impact:**
CRITICAL - Cannot verify K/DST are being evaluated with ranking metrics (epic fails)

**Log Evidence:**
```
2026-01-09 17:08:16 - accuracy_simulation - INFO - save_intermediate_results:685 - Saved metadata to metadata.json
2026-01-09 17:08:16 - accuracy_simulation - WARNING - run_both:855 - No best config found for ros after parameter PERFORMANCE_MIN_WEEKS
2026-01-09 17:08:16 - accuracy_simulation - INFO - _log_parameter_summary:897 -   week_1_5: MAE=3.3916 (test_?)
```

---

## Investigation Round 1: Code Tracing

**Date:** 2026-01-09
**Duration:** 30 minutes
**Objective:** Trace code flow to identify where ranking_metrics are lost

### Suspicious Areas Identified:

#### 1. Invalid 'ros' key in horizon_map (AccuracySimulationManager.py:844)
**File:** simulation/accuracy/AccuracySimulationManager.py
**Lines:** 843-849

```python
horizon_map = {
    'ros': 'ros',  # <-- BUG! This key doesn't exist in best_configs!
    'week_1_5': '1-5',
    'week_6_9': '6-9',
    'week_10_13': '10-13',
    'week_14_17': '14-17'
}
```

**Evidence:**
- best_configs only has keys: week_1_5, week_6_9, week_10_13, week_14_17 (line 260-265)
- 'ros' key lookup fails → triggers warning at line 855
- Explains: "No best config found for ros" warning

**Impact:** Minor bug (doesn't affect ranking_metrics issue, just spurious warning)

---

#### 2. Resume logic doesn't load ranking_metrics (AccuracyResultsManager.py:730-738)
**File:** simulation/accuracy/AccuracyResultsManager.py
**Lines:** 730-738

```python
perf_data = {
    'mae': metrics['mae'],
    'player_count': metrics['player_count'],
    'config_id': metrics.get('config_id', ''),
    'config': data['parameters']
    # MISSING: Does NOT load ranking_metrics from file!
}
self.best_configs[week_key] = AccuracyConfigPerformance.from_dict(perf_data)
```

**Evidence:**
- Old intermediate folders exist from Dec 23: accuracy_intermediate_00, 01, etc.
- These old files don't have ranking_metrics (created before epic implementation)
- When loading, only mae/player_count/config_id are extracted
- from_dict() is called WITHOUT ranking_metrics data

**Impact:** HIGH - Loaded configs have overall_metrics=None

---

#### 3. Comparison logic fails with mixed metrics (AccuracyResultsManager.py:142-146)
**File:** simulation/accuracy/AccuracyResultsManager.py
**Lines:** 142-146

```python
# Use ranking metrics if available (Q12: pairwise_accuracy is primary)
if self.overall_metrics and other.overall_metrics:  # BOTH must have metrics
    return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy

# Fallback to MAE for backward compatibility (Q25)
return self.mae < other.mae
```

**Evidence:**
- Loaded config: overall_metrics=None (from old files)
- New config: overall_metrics=RankingMetrics(pairwise=0.67, ...)
- Comparison requires BOTH to have metrics
- Falls back to MAE comparison
- If old MAE < new MAE → new config rejected (even if better pairwise!)

**Impact:** CRITICAL - New configs with ranking metrics rejected in favor of old configs without metrics

---

### Root Cause Hypothesis

**Primary Theory:**

The simulation is RESUMING from old intermediate files (Dec 23) that were created BEFORE the K/DST ranking metrics epic was implemented. These old files don't have ranking_metrics in their performance_metrics.

**Chain of events:**
1. Simulation loads old intermediate files (resume feature)
2. Load logic (line 730-738) doesn't extract ranking_metrics → creates configs with overall_metrics=None
3. These old configs become "best" configs in best_configs dict
4. New configs are evaluated WITH ranking_metrics
5. Comparison logic (line 142-146) requires BOTH configs to have metrics
6. Falls back to MAE comparison
7. If old MAE is better → new config rejected despite having ranking metrics
8. best_configs contains old configs WITHOUT ranking_metrics
9. save_intermediate_results() checks if overall_metrics exists (line 601)
10. overall_metrics is None → ranking_metrics NOT saved to output files

**Result:** Output files only show MAE, missing all ranking metrics

---

### Diagnostic Logging Plan

To verify this hypothesis, add logging to trace:

1. **Loading phase (load_intermediate_results):**
   - Log which files are being loaded
   - Log if ranking_metrics present in loaded files
   - Log overall_metrics status after from_dict()

2. **Evaluation phase (_evaluate_config_weekly):**
   - Log if overall_metrics calculated
   - Log overall_metrics values

3. **Comparison phase (is_better_than):**
   - Log both configs' overall_metrics status
   - Log which comparison path taken (metrics vs MAE)
   - Log comparison result

4. **Saving phase (save_intermediate_results):**
   - Log overall_metrics status for each best_config
   - Log whether ranking_metrics being saved

**Files to instrument:**
- simulation/accuracy/AccuracyResultsManager.py
- simulation/accuracy/AccuracySimulationManager.py

---

## Next Steps

1. Add diagnostic logging to verify hypothesis
2. Run simulation with logging enabled
3. Analyze logs to confirm root cause
4. If confirmed → Design fix (Investigation Round 2)
5. If not confirmed → Continue investigation (Investigation Round 2)

---

## Solution Implementation

**Date:** 2026-01-09
**Root Cause Confirmed:** Resume logic loads old performance metrics and pollutes best_configs

### Solution Design

**Three fixes required:**

1. **Fix `load_intermediate_results()` (AccuracyResultsManager.py:740-810)**
   - Current: Loads MAE/metrics and populates best_configs
   - Fix: Don't populate best_configs, only return True/False for resume detection
   - Rationale: Metrics are for user visibility only, not for comparison

2. **Fix `is_better_than()` (AccuracyResultsManager.py:115-167)**
   - Current: Falls back to MAE if either config missing ranking_metrics
   - Fix: ONLY use pairwise_accuracy, no fallback
   - Rationale: Pairwise accuracy is the primary metric, MAE is diagnostic only

3. **Fix invalid 'ros' key (AccuracySimulationManager.py:844)**
   - Current: `'ros': 'ros'` in horizon_map (invalid key)
   - Fix: Remove this entry
   - Rationale: best_configs only has week_1_5, week_6_9, week_10_13, week_14_17

### Implementation Plan

**Change 1: load_intermediate_results() - Remove best_configs population**

Before:
```python
self.best_configs[week_key] = loaded_config  # Populates with old metrics
loaded_count += 1
```

After:
```python
# Don't populate best_configs - metrics are for user visibility only
# Just count files to indicate successful load
loaded_count += 1
```

**Change 2: is_better_than() - Remove MAE fallback**

Before:
```python
# Use ranking metrics if available
if self.overall_metrics and other.overall_metrics:
    return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy
# Fallback to MAE
return self.mae < other.mae
```

After:
```python
# ALWAYS use pairwise accuracy (no MAE fallback)
# If either config missing ranking_metrics, it's invalid
if not self.overall_metrics:
    return False  # This config is invalid
if not other.overall_metrics:
    return True   # Other is invalid, replace it
return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy
```

**Change 3: Remove 'ros' from horizon_map**

Before:
```python
horizon_map = {
    'ros': 'ros',  # Invalid!
    'week_1_5': '1-5',
    ...
}
```

After:
```python
horizon_map = {
    'week_1_5': '1-5',
    'week_6_9': '6-9',
    'week_10_13': '10-13',
    'week_14_17': '14-17'
}
```

---

## User Verification

**User Verification:** ✅ CONFIRMED FIXED
**Verified By:** User
**Verified Date:** 2026-01-09
**User Feedback:** "yes" - All 6 symptoms confirmed resolved

**Verification Results:**

1. ✅ test_idx shows actual indices (2, 2, 0, 1) instead of -1
2. ✅ ranking_metrics present in metadata.json (all 5 metrics)
3. ✅ ranking_metrics present in individual week files
4. ✅ by_position breakdown included (K/DST present)
5. ✅ No "No best config found for ros" warning
6. ✅ config_value shows actual parameter values (e.g., LOCATION_AWAY = 3.9)

**Example Verified Output (accuracy_intermediate_14_LOCATION_AWAY/metadata.json):**
```json
"week_1_5": {
  "mae": 4.5988,
  "test_idx": 2,
  "ranking_metrics": {
    "pairwise_accuracy": 0.6147,
    "top_5_accuracy": 0.29,
    "top_10_accuracy": 0.4367,
    "top_20_accuracy": 0.6529,
    "spearman_correlation": 0.3408
  }
}
```

**Status:** COMPLETE ✅
