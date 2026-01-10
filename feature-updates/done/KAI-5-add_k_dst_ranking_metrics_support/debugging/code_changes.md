# Debugging Code Changes: Issues #001, #002, #003

**Issues:**
- Issue #001: Missing ranking metrics and metadata in simulation output files
- Issue #002: config_value showing null in horizon files
- Issue #003: Missing position-specific metrics (by_position)

**Date:** 2026-01-09

---

## Change 1: Fix load_intermediate_results() - Don't populate best_configs

**File:** `simulation/accuracy/AccuracyResultsManager.py`
**Lines:** 782-793
**Date:** 2026-01-09

**Before:**
```python
if 'mae' in metrics and metrics['mae'] is not None:
    perf_data = {
        'mae': metrics['mae'],
        'player_count': metrics['player_count'],
        'config_id': metrics.get('config_id', ''),
        'config': data['parameters']
    }
    loaded_config = AccuracyConfigPerformance.from_dict(perf_data)
    self.best_configs[week_key] = loaded_config  # ← BUG: Populates with old metrics
    loaded_count += 1
```

**After:**
```python
if 'mae' in metrics and metrics['mae'] is not None:
    # NOTE: We load intermediate files for resume detection only
    # Do NOT populate best_configs with old metrics
    # Metrics are for user visibility, not for comparison
    # Each run evaluates configs fresh with current ranking metrics
    loaded_count += 1
    self.logger.debug(
        f"Found intermediate config {standard_filename} for {week_key} "
        f"(parameters only, not loading metrics)"
    )
```

**Reason:**
- Intermediate files contain metrics for user visibility only
- Should NOT load old metrics into best_configs for comparison
- Each run should evaluate configs fresh with current ranking metrics
- Fixes bug where old configs without ranking_metrics blocked new configs with ranking_metrics

---

## Change 2: Fix is_better_than() - Remove MAE fallback, only use pairwise accuracy

**File:** `simulation/accuracy/AccuracyResultsManager.py`
**Lines:** 115-152
**Date:** 2026-01-09

**Before:**
```python
def is_better_than(self, other: 'AccuracyConfigPerformance') -> bool:
    """Uses pairwise_accuracy when available. Falls back to MAE for backward compatibility."""
    if self.player_count == 0:
        return False
    if other is None:
        return True
    if other.player_count == 0:
        return False

    # Use ranking metrics if available
    if self.overall_metrics and other.overall_metrics:
        return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy

    # Fallback to MAE for backward compatibility
    return self.mae < other.mae
```

**After:**
```python
def is_better_than(self, other: 'AccuracyConfigPerformance') -> bool:
    """ALWAYS uses pairwise_accuracy. MAE is for diagnostics/user visibility only."""
    # Reject invalid configs FIRST (before checking if other is None)
    # This prevents invalid configs from becoming "best" when no previous best exists
    if self.player_count == 0:
        return False

    # Check if this config has ranking metrics (required for all configs)
    if not self.overall_metrics:
        return False  # This config is invalid/incomplete, cannot be "best"

    # Now safe to check if other is None (we know self is valid)
    if other is None:
        return True

    # Don't replace valid config with invalid one
    if other.player_count == 0:
        return False

    # If other config missing ranking_metrics, replace it with this valid one
    if not other.overall_metrics:
        return True   # Other config is invalid, replace it with this one

    # Both have ranking metrics - compare pairwise accuracy
    return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy
```

**Reason:**
- Pairwise accuracy is the primary metric for accuracy simulation
- MAE is diagnostic/user visibility only, not for comparison
- Configs without ranking_metrics are invalid and should be replaced
- Prevents mixed comparisons (new with metrics vs old without metrics)
- **CRITICAL:** Check if self has ranking_metrics BEFORE checking if other is None
  - This prevents invalid configs (without ranking_metrics) from becoming the first "best" config

---

## Change 3: Fix invalid 'ros' key in horizon_map

**File:** `simulation/accuracy/AccuracySimulationManager.py`
**Lines:** 841-848
**Date:** 2026-01-09

**Before:**
```python
# Update baselines for all 5 horizons
horizon_map = {
    'ros': 'ros',  # ← BUG: Invalid key, doesn't exist in best_configs
    'week_1_5': '1-5',
    'week_6_9': '6-9',
    'week_10_13': '10-13',
    'week_14_17': '14-17'
}
```

**After:**
```python
# Update baselines for all 4 weekly horizons
horizon_map = {
    'week_1_5': '1-5',
    'week_6_9': '6-9',
    'week_10_13': '10-13',
    'week_14_17': '14-17'
}
```

**Reason:**
- best_configs only has 4 keys: week_1_5, week_6_9, week_10_13, week_14_17
- 'ros' key doesn't exist, caused warning: "No best config found for ros"
- Removed invalid entry to eliminate spurious warning

---

## Summary

**Total Files Modified:** 2
- simulation/accuracy/AccuracyResultsManager.py (2 changes)
- simulation/accuracy/AccuracySimulationManager.py (1 change)

**Total Lines Changed:** ~55 lines
- Change 1: ~15 lines (load_intermediate_results)
- Change 2: ~30 lines (is_better_than - includes check ordering fix)
- Change 3: ~2 lines (horizon_map)
- Test updates: ~100 lines across 13 test files (added ranking_metrics to test fixtures)

**Bug Fixes:**
1. Resume logic no longer pollutes best_configs with old metrics
2. Comparison logic always uses pairwise accuracy (no MAE fallback)
3. Removed invalid 'ros' key that caused spurious warnings

**Expected Result:**
- All new configs have ranking_metrics (calculated fresh each run)
- Comparison uses pairwise_accuracy exclusively
- Output files include ranking_metrics in performance_metrics
- Output files include by_position breakdown with K/DST
- metadata.json includes ranking_metrics for each horizon
- No "No best config found for ros" warning

---

## Change 4: Fix config_value extraction - Pass param_name to add_result()

**Issue:** Issue #002 - config_value Showing null in Horizon Files
**File:** `simulation/accuracy/AccuracySimulationManager.py`
**Lines:** 667-671
**Date:** 2026-01-09

**Before:**
```python
# Evaluate configuration for this week range
result = self._evaluate_config_weekly(config_dict, week_range)

# Record result
is_new_best = self.results_manager.add_result(week_key, config_dict, result)
```

**After:**
```python
# Evaluate configuration for this week range
result = self._evaluate_config_weekly(config_dict, week_range)

# Record result (pass param_name and test_idx for config_value extraction)
is_new_best = self.results_manager.add_result(
    week_key, config_dict, result,
    param_name=param_name,
    test_idx=test_idx
)
```

**Reason:**
- AccuracyConfigPerformance._extract_param_value() requires param_name to extract parameter value
- Without param_name, config_value defaults to None
- Passing param_name enables automatic extraction of tested parameter value
- Users can now see which parameter value was optimal (e.g., 3.9, 0.25) instead of null

---

## Change 5: Fix by_position serialization - Add to ranking_metrics output

**Issue:** Issue #003 - Missing Position-Specific Metrics
**File:** `simulation/accuracy/AccuracyResultsManager.py`
**Lines:** 645-656
**Date:** 2026-01-09

**Before:**
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

**After:**
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

**Reason:**
- by_position is calculated by AccuracyCalculator and stored in AccuracyConfigPerformance
- save_intermediate_results() serializes overall_metrics but was missing by_position
- Without by_position, cannot verify K/DST are being evaluated (epic goal)
- Adding by_position enables users to see per-position accuracy metrics (QB, RB, WR, TE, K, DST)

---

## Updated Summary

**Total Files Modified:** 2
- simulation/accuracy/AccuracyResultsManager.py (3 changes: load, is_better_than, by_position serialization)
- simulation/accuracy/AccuracySimulationManager.py (2 changes: horizon_map, param_name passing)

**Total Lines Changed:** ~70 lines
- Change 1: ~15 lines (load_intermediate_results - Issue #001)
- Change 2: ~30 lines (is_better_than - Issue #001)
- Change 3: ~2 lines (horizon_map - Issue #001)
- Change 4: ~3 lines (param_name passing - Issue #002)
- Change 5: ~11 lines (by_position serialization - Issue #003)
- Test updates: ~100 lines across 13 test files (added ranking_metrics to test fixtures)

**Bug Fixes:**
1. Resume logic no longer pollutes best_configs with old metrics (Issue #001)
2. Comparison logic always uses pairwise accuracy (Issue #001)
3. Removed invalid 'ros' key that caused spurious warnings (Issue #001)
4. config_value now shows actual parameter values instead of null (Issue #002)
5. by_position breakdown now included in output files (Issue #003)

**Expected Result:**
- All new configs have ranking_metrics (calculated fresh each run)
- Comparison uses pairwise_accuracy exclusively
- Output files include ranking_metrics in performance_metrics
- Output files include by_position breakdown with K/DST (epic goal verified)
- Output files show config_value with actual parameter values
- metadata.json includes ranking_metrics for each horizon
- No "No best config found for ros" warning

**User Verification:** ✅ All 3 issues confirmed fixed (2026-01-09)
