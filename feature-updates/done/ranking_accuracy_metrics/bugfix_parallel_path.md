# Bug Fix: Add Ranking Metrics to Parallel Execution Path

**Date:** 2025-12-21
**Issue:** Ranking metrics not calculated in ParallelAccuracyRunner worker path
**Severity:** CRITICAL - Feature completely non-functional in default (parallel) mode

---

## Problem Summary

The ranking metrics feature was only implemented in the serial execution path (`AccuracySimulationManager._evaluate_config_weekly()`) but NOT in the parallel execution path (`ParallelAccuracyRunner._evaluate_config_weekly_worker()`).

Since parallel execution is the default, the feature doesn't work in production.

---

## Root Cause Analysis

### Two Execution Paths

1. **Serial Path (WORKS):**
   - `AccuracySimulationManager._evaluate_config_weekly()`
   - Lines 592-594: Calls `_calculate_ranking_metrics()` and attaches to result
   - ✅ Ranking metrics calculated

2. **Parallel Path (BROKEN):**
   - `ParallelAccuracyRunner._evaluate_config_weekly_worker()`
   - Module-level function, no access to AccuracySimulationManager instance
   - ❌ Never calls ranking metrics calculation
   - ❌ Returns AccuracyResult without ranking metrics

### Architectural Issue

`_calculate_ranking_metrics()` is a method of `AccuracySimulationManager`, but the parallel worker is a module-level function that can't access it.

**Solution:** Move the method to `AccuracyCalculator` where it belongs architecturally.

---

## Fix Implementation Plan

### Step 1: Move `_calculate_ranking_metrics()` to AccuracyCalculator

**File:** `simulation/accuracy/AccuracyCalculator.py`

**Action:** Add new method `calculate_ranking_metrics_for_season()`

```python
def calculate_ranking_metrics_for_season(
    self,
    player_data_by_week: Dict[int, List[Dict[str, Any]]]
) -> Tuple[RankingMetrics, Dict[str, RankingMetrics]]:
    """
    Calculate ranking metrics across weeks and positions for a season.

    [Copy implementation from AccuracySimulationManager._calculate_ranking_metrics]
    """
```

**Changes needed:**
- Copy lines 385-498 from AccuracySimulationManager.py
- Change `self.accuracy_calculator.calculate_*` to `self.calculate_*`
- Change `self.logger` to use calculator's logger
- Import numpy at top of file (already imported)

### Step 2: Update Serial Path to Use New Method

**File:** `simulation/accuracy/AccuracySimulationManager.py`

**Line 592:** Change from:
```python
overall_metrics, by_position = self._calculate_ranking_metrics(player_data_by_week)
```

To:
```python
overall_metrics, by_position = self.accuracy_calculator.calculate_ranking_metrics_for_season(player_data_by_week)
```

**Lines 385-498:** Delete `_calculate_ranking_metrics()` method (now in AccuracyCalculator)

### Step 3: Update Parallel Worker Path

**File:** `simulation/accuracy/ParallelAccuracyRunner.py`

**Changes to `_evaluate_config_weekly_worker()` function:**

1. **Line 106:** Add player_data_by_week initialization:
```python
start_week, end_week = week_range
season_results = []
player_data_by_week = {}  # ADD THIS LINE
```

2. **Line 119:** Add player_data initialization inside week loop:
```python
for week_num in range(start_week, end_week + 1):
    projected_path, actual_path = _load_season_data(season_path, week_num)
    if not projected_path:
        continue

    # Create player manager with this config
    player_mgr = _create_player_manager(config_dict, projected_path.parent, season_path)

    try:
        projections = {}
        actuals = {}
        player_data = []  # ADD THIS LINE
```

3. **Lines 154-157:** Collect player metadata when storing actuals:

Change from:
```python
# Get actual points for this specific week
week_points_attr = f'week_{week_num}_points'
if hasattr(player, week_points_attr):
    actual = getattr(player, week_points_attr)
    if actual is not None and actual > 0:
        actuals[player.id] = actual
```

To:
```python
# Get actual points for this specific week
week_points_attr = f'week_{week_num}_points'
if hasattr(player, week_points_attr):
    actual = getattr(player, week_points_attr)
    if actual is not None and actual > 0:
        actuals[player.id] = actual

        # Collect player metadata for ranking metrics
        if scored:
            player_data.append({
                'name': player.name,
                'position': player.position,
                'projected': scored.projected_points,
                'actual': actual
            })
```

4. **Line 159:** Store player_data after week processing:

Change from:
```python
week_projections[week_num] = projections
week_actuals[week_num] = actuals
```

To:
```python
week_projections[week_num] = projections
week_actuals[week_num] = actuals
player_data_by_week[week_num] = player_data  # ADD THIS LINE
```

5. **Lines 165-168:** Add ranking metrics calculation after season loop:

Change from:
```python
# Calculate MAE for this season's week range
result = calculator.calculate_weekly_mae(
    week_projections, week_actuals, week_range
)
season_results.append((season_path.name, result))
```

To:
```python
# Calculate MAE for this season's week range
result = calculator.calculate_weekly_mae(
    week_projections, week_actuals, week_range
)

# Calculate ranking metrics for this season
overall_metrics, by_position = calculator.calculate_ranking_metrics_for_season(
    player_data_by_week
)
result.overall_metrics = overall_metrics
result.by_position = by_position

season_results.append((season_path.name, result))
```

### Step 4: Update Tests

**Verify existing tests still pass:**
```bash
python -m pytest tests/simulation/ -q
```

**Expected:** All 608 tests should still pass (they test serial path mostly)

**Add new test for parallel path with ranking metrics:**

**File:** `tests/simulation/test_ParallelAccuracyRunner.py` (if exists) or `tests/integration/test_accuracy_simulation_integration.py`

```python
def test_parallel_worker_calculates_ranking_metrics():
    """Test that parallel worker calculates ranking metrics."""
    # Setup test data
    # Call _evaluate_config_tournament_process
    # Assert result has overall_metrics
    # Assert overall_metrics.pairwise_accuracy is not None
```

---

## Verification Checklist

Before marking complete:

- [ ] AccuracyCalculator has calculate_ranking_metrics_for_season() method
- [ ] Serial path uses new calculator method
- [ ] Old _calculate_ranking_metrics() removed from AccuracySimulationManager
- [ ] Parallel worker collects player_data_by_week
- [ ] Parallel worker calls calculator.calculate_ranking_metrics_for_season()
- [ ] Parallel worker attaches metrics to result
- [ ] All 608 existing tests pass
- [ ] New test added for parallel path
- [ ] **SMOKE TEST:** Run actual script and verify ranking metrics appear in output
- [ ] **SMOKE TEST:** Verify metadata.json contains ranking metrics fields

---

## Testing Strategy

1. **Unit tests:** Should pass (test individual functions)
2. **Integration tests:** Should pass (may test serial path only)
3. **Smoke test (REQUIRED):** Run actual accuracy simulation:
   ```bash
   python run_accuracy_simulation.py --test-values 1 --num-params 1
   ```

   **Verify:**
   - Console output shows: `Pairwise=XX.X% | Top-10=XX.X% | Spearman=X.XXX`
   - JSON output contains all ranking metric fields
   - No fallback to MAE-only display

---

## Files Modified

1. `simulation/accuracy/AccuracyCalculator.py` - Add calculate_ranking_metrics_for_season()
2. `simulation/accuracy/AccuracySimulationManager.py` - Use calculator method, remove old method
3. `simulation/accuracy/ParallelAccuracyRunner.py` - Collect player data, calculate metrics
4. `tests/simulation/test_ParallelAccuracyRunner.py` - Add test for parallel path (if needed)

---

## Risk Assessment

**Risk Level:** LOW

**Rationale:**
- Moving method to AccuracyCalculator is low-risk refactoring
- Serial path update is one-line change
- Parallel worker changes mirror existing serial path code
- All existing tests should pass
- Smoke testing will catch any issues

**Mitigation:**
- Run all tests after each step
- Smoke test after completion
- Code review parallel worker changes carefully
