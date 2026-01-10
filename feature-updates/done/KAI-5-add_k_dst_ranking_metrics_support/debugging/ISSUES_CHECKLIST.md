# Epic Debugging Issues Checklist

**Epic:** KAI-5-add_k_dst_ranking_metrics_support
**Created:** 2026-01-09
**Discovery Stage:** Stage 6c - User Testing
**Total Issues:** 1

---

## Issue Tracking Legend

- 🔴 **OPEN** - Issue identified, investigation not started
- 🟡 **INVESTIGATING** - Root cause analysis in progress
- 🔵 **FIX_IN_PROGRESS** - Root cause known, implementing solution
- 🟢 **FIXED** - Solution implemented and user-confirmed
- ⚫ **WONTFIX** - User-approved to not fix (rare)

---

## Active Issues

### Issue 001: Incomplete Simulation Results - Missing Ranking Metrics and Metadata
**Status:** 🟢 FIXED - User Confirmed
**Priority:** HIGH (Breaks core epic functionality)
**Discovered:** 2026-01-09 (Stage 6c - User Testing)
**Discovered By:** User
**Resolved:** 2026-01-09
**File:** `debugging/issue_001_incomplete_simulation_results.md`

**Symptoms (All Fixed):**

1. **metadata.json shows test_idx = -1 for all horizons** ✅ FIXED - Shows actual indices
2. **metadata.json only shows MAE** ✅ FIXED - Includes all 5 ranking_metrics
3. **No positional data** ✅ FIXED - Includes by_position breakdown
4. **Individual horizon files have minimal performance_metrics** ✅ FIXED - Full metrics saved
5. **Log shows "test_?" instead of test_idx values** ✅ FIXED - Shows actual test_idx
6. **WARNING in log: "No best config found for ros"** ✅ FIXED - Invalid 'ros' key removed

**Example Output (Incorrect):**

metadata.json:
```json
"best_mae_per_horizon": {
  "week_1_5": {
    "mae": 3.3915545810723207,
    "test_idx": -1  // WRONG - should show actual test index
  }
}
```

week1-5.json:
```json
"performance_metrics": {
  "mae": 3.3915545810723207,
  "player_count": 6304,
  "config_id": "19e97887"
  // MISSING: ranking_metrics
  // MISSING: by_position
}
```

**Expected Output:**

metadata.json should include:
```json
"best_mae_per_horizon": {
  "week_1_5": {
    "mae": 3.3915545810723207,
    "test_idx": 12,  // Actual test index
    "ranking_metrics": {
      "pairwise_accuracy": 0.67,
      "top_5_accuracy": 0.45,
      "top_10_accuracy": 0.58,
      "top_20_accuracy": 0.72,
      "spearman_correlation": 0.543
    }
  }
}
```

**Log Evidence:**
```
2026-01-09 17:08:16 - accuracy_simulation - INFO - save_intermediate_results:685 - Saved metadata to metadata.json
2026-01-09 17:08:16 - accuracy_simulation - WARNING - run_both:855 - No best config found for ros after parameter PERFORMANCE_MIN_WEEKS
2026-01-09 17:08:16 - accuracy_simulation - INFO - _log_parameter_summary:877 - Parameter PERFORMANCE_MIN_WEEKS complete:
2026-01-09 17:08:16 - accuracy_simulation - INFO - _log_parameter_summary:897 -   week_1_5: MAE=3.3916 (test_?)
2026-01-09 17:08:16 - accuracy_simulation - INFO - _log_parameter_summary:897 -   week_6_9: MAE=3.2516 (test_?)
```

**Key Clues:**
- WARNING: "No best config found for ros" - What is "ros"? Typo? Specific parameter?
- test_idx = -1 suggests no "best" config was ever set
- "test_?" in logs confirms test_idx is missing/unknown
- Files save successfully but with incomplete data

**Impact:**
- **CRITICAL**: Epic goal is to add K/DST to ranking metrics - if metrics aren't saved, epic fails
- Users cannot see K/DST metrics in output files
- Cannot verify K and DST are being evaluated with ranking metrics
- Cannot see which test configuration performed best
- No positional breakdown to verify K/DST are included

**Affected Files:**
- simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/metadata.json
- simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/week1-5.json
- simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/week6-9.json
- simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/week10-13.json
- simulation/simulation_configs/accuracy_intermediate_05_PERFORMANCE_MIN_WEEKS/week14-17.json
- simulation/accuracy/AccuracyResultsManager.py (save logic)
- simulation/accuracy/AccuracySimulationManager.py (run_both method)

**Root Cause Hypothesis:** All symptoms may stem from single root cause:
- Ranking metrics ARE calculated (we verified in Stage 5/6 testing)
- But `best_configs` dictionary may not have valid data when saving
- "No best config found for ros" warning is KEY clue
- Need to investigate why best configs aren't being tracked properly

**Investigation Status:** ✅ Complete - Root cause confirmed in Round 1
**Root Cause:** Resume logic loads old metrics without ranking_metrics, pollutes best_configs

**Solution Implemented:**
1. **Change 1:** load_intermediate_results() - Don't populate best_configs with old metrics
2. **Change 2:** is_better_than() - Remove MAE fallback, only use pairwise_accuracy (check ordering fix)
3. **Change 3:** horizon_map - Remove invalid 'ros' key

**Tests:** ✅ All 2,486 tests passing (100%)

**Fix Status:** ✅ Solution implemented, tests passing
**User Confirmation:** ✅ CONFIRMED FIXED
**Verified By:** User
**Verified Date:** 2026-01-09

**User Feedback:** "yes" - All 6 symptoms confirmed resolved in simulation output files

---

## Resolved Issues

### Issue 001: Incomplete Simulation Results - Missing Ranking Metrics and Metadata
**Status:** ✅ RESOLVED
**Resolved Date:** 2026-01-09
**Root Cause:** Resume logic loaded old metrics without ranking_metrics, polluted best_configs
**Solution:** 3 code fixes + config_value feature
**User Verification:** ✅ Confirmed (2026-01-09)
**Details:** See debugging/issue_001_incomplete_simulation_results.md

---

---

## Active Issues

**None** - All issues resolved

---

## Resolved Issues

### Issue 002: config_value Showing null in Horizon Files
**Status:** ✅ RESOLVED
**Resolved Date:** 2026-01-09
**Root Cause:** param_name not passed to add_result() in run_weekly_optimization()
**Solution:** Pass param_name and test_idx to add_result() (1 line changed)
**User Verification:** ✅ Confirmed (2026-01-09)
**Details:** See debugging/issue_002_config_value_null.md

### Issue 003: Missing Position-Specific Metrics
**Status:** ✅ RESOLVED
**Resolved Date:** 2026-01-09
**Root Cause:** save_intermediate_results() doesn't serialize by_position to JSON
**Solution:** Add by_position to ranking_metrics dict in serialization (11 lines added)
**User Verification:** ✅ Confirmed (2026-01-09)
**Details:** See debugging/issue_003_missing_position_metrics.md

---

## Summary

**Total Issues:** 3
- 🔴 OPEN: 0
- 🟡 INVESTIGATING: 0
- 🔵 FIX_IN_PROGRESS: 0
- 🟢 FIXED: 3 (All user-confirmed)
- ⚫ WONTFIX: 0

**Status:** ✅ ALL ISSUES RESOLVED - Ready for Phase 5 (Loop Back to Testing)
**Loop Back Target:** Stage 6a - Epic Smoke Testing (restart epic testing from beginning)
