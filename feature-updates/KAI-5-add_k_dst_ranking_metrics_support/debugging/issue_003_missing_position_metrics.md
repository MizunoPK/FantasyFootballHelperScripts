# Issue #003: Missing Position-Specific Metrics

**Created:** 2026-01-09
**Status:** 🔴 OPEN
**Priority:** HIGH (Breaks core epic functionality)
**Discovered During:** Stage 6c - User Testing (Loop Back after Issue #001)
**Current Phase:** Investigation Round 1 - Code Tracing

---

## Issue Description

**Symptoms:**
1. by_position field missing or empty in metric objects
2. No position-specific breakdown (QB, RB, WR, TE, K, DST)
3. Cannot verify K/DST are being evaluated separately
4. Output files only show overall ranking_metrics, not per-position

**Discovered During:**
User testing after Issue #001 fix - checking for K/DST metrics

**Reproduction:**
```bash
# Run accuracy simulation
python run_simulation.py

# Check output
cat simulation/simulation_configs/accuracy_intermediate_*/week1-5.json
# by_position field should exist with QB/RB/WR/TE/K/DST metrics
```

**Impact:**
HIGH - Cannot verify epic goal (adding K/DST to ranking metrics)
Without by_position breakdown, can't confirm K and DST are evaluated separately

**Example Output (Incorrect):**
```json
"ranking_metrics": {
  "pairwise_accuracy": 0.6147,
  "top_5_accuracy": 0.29,
  "top_10_accuracy": 0.4367,
  "top_20_accuracy": 0.6529,
  "spearman_correlation": 0.3408
  // MISSING: by_position breakdown
}
```

**Expected Output:**
```json
"ranking_metrics": {
  "pairwise_accuracy": 0.6147,
  "top_5_accuracy": 0.29,
  "top_10_accuracy": 0.4367,
  "top_20_accuracy": 0.6529,
  "spearman_correlation": 0.3408,
  "by_position": {
    "QB": {
      "pairwise_accuracy": 0.65,
      "top_5_accuracy": 0.35,
      ...
    },
    "RB": { ... },
    "WR": { ... },
    "TE": { ... },
    "K": { ... },    // MUST have K
    "DST": { ... }   // MUST have DST
  }
}
```

---

## Investigation Round 1: Code Tracing

**Date:** 2026-01-09
**Objective:** Identify why by_position is missing from output

### Hypothesis

**Primary Theory:**
The by_position field is being calculated but not saved to JSON files. Possible causes:
1. RankingMetrics.to_dict() doesn't include by_position
2. AccuracyConfigPerformance serialization excludes by_position
3. by_position is None (not calculated)

### Areas to Investigate

1. **Check RankingMetrics serialization:**
   - simulation/accuracy/RankingMetrics.py
   - Does to_dict() include by_position?

2. **Check AccuracyConfigPerformance serialization:**
   - AccuracyResultsManager.py: save_intermediate_results()
   - How is overall_metrics converted to dict?

3. **Check if by_position is calculated:**
   - AccuracyCalculator.calculate_ranking_metrics()
   - Returns RankingMetrics with by_position?

4. **Check AccuracyResult to AccuracyConfigPerformance conversion:**
   - Does by_position get passed through?

---

## Next Steps

1. Read RankingMetrics.py to check to_dict() implementation
2. Read AccuracyResultsManager.py to check serialization
3. Read AccuracyCalculator.py to verify by_position calculation
4. Identify where by_position is being lost
5. Design fix
6. Implement and test

---

## Solution Implementation

**Date:** 2026-01-09
**Root Cause Confirmed:** save_intermediate_results() doesn't include by_position in ranking_metrics serialization

### Solution Design

**Single fix required:**

**Fix `save_intermediate_results()` (AccuracyResultsManager.py:637-644)**
   - Current: Only saves 5 overall metrics to ranking_metrics dict
   - Fix: Add by_position breakdown if available
   - Rationale: by_position is calculated and stored in perf object, but not serialized to JSON

### Implementation

**Change: Add by_position to ranking_metrics serialization**

Before (simulation/accuracy/AccuracyResultsManager.py:637-644):
```python
# Include ranking metrics if available
if perf.overall_metrics:
    perf_metrics['ranking_metrics'] = {
        'pairwise_accuracy': perf.overall_metrics.pairwise_accuracy,
        'top_5_accuracy': perf.overall_metrics.top_5_accuracy,
        'top_10_accuracy': perf.overall_metrics.top_10_accuracy,
        'top_20_accuracy': perf.overall_metrics.top_20_accuracy,
        'spearman_correlation': perf.overall_metrics.spearman_correlation
    }
```

After:
```python
# Include ranking metrics if available
if perf.overall_metrics:
    perf_metrics['ranking_metrics'] = {
        'pairwise_accuracy': perf.overall_metrics.pairwise_accuracy,
        'top_5_accuracy': perf.overall_metrics.top_5_accuracy,
        'top_10_accuracy': perf.overall_metrics.top_10_accuracy,
        'top_20_accuracy': perf.overall_metrics.top_20_accuracy,
        'spearman_correlation': perf.overall_metrics.spearman_correlation
    }
    # Include per-position breakdown if available
    if perf.by_position:
        perf_metrics['ranking_metrics']['by_position'] = {
            pos: {
                'pairwise_accuracy': metrics.pairwise_accuracy,
                'top_5_accuracy': metrics.top_5_accuracy,
                'top_10_accuracy': metrics.top_10_accuracy,
                'top_20_accuracy': metrics.top_20_accuracy,
                'spearman_correlation': metrics.spearman_correlation
            }
            for pos, metrics in perf.by_position.items()
        }
```

**Tests:** ✅ All 2,486 tests passing (100%)

**Files Modified:**
- simulation/accuracy/AccuracyResultsManager.py (lines 645-656, 11 lines added)

---

## User Verification

**User Verification:** ✅ CONFIRMED FIXED
**Verified By:** User
**Verified Date:** 2026-01-09
**User Feedback:** "they are both working"

**Verification Results:**

✅ by_position field now present in ranking_metrics
✅ Position breakdown includes all 6 positions (QB, RB, WR, TE, K, DST)
✅ Can now verify K and DST are being evaluated with ranking metrics (epic goal achieved)

**Status:** RESOLVED ✅
