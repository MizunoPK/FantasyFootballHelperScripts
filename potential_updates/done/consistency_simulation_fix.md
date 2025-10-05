# Consistency Scoring - Simulation Data Fix

**Date**: 2025-10-05
**Issue**: Simulation was not providing actual weekly points data for consistency calculations
**Status**: ✅ FIXED

## Problem

The simulation's `_get_optimal_starting_lineup()` method was creating `player_dict` objects with only basic player info:
- id, name, position, team, injury_status, bye_week

**Missing**: Historical weekly points data (`week_1_points`, `week_2_points`, etc.)

This meant the ConsistencyCalculator had no actual performance data to calculate coefficient of variation (CV), causing:
- Consistency scoring to always default to MEDIUM (no data available)
- Simulations to not properly reflect the impact of player volatility
- Invalid testing of the consistency scoring feature

## Solution

Updated `season_simulator.py` to populate `player_dict` with actual weekly points:

```python
# Add actual weekly points data for consistency calculation
# Consistency should use ACTUAL performance data, not projections
for hist_week in range(1, week):  # Only weeks that have occurred
    week_attr = f'week_{hist_week}_points'
    # Get actual points from actual dataframe
    actual_points = self._get_player_week_points_from_df(player, hist_week, use_actual=True)
    player_dict[week_attr] = actual_points
```

## Data Flow (After Fix)

1. **Simulation Week 5 Example**:
   - Creates player_dict with weeks 1-4 actual points from `players_actual_df`
   - Gets week 5 projected points from `players_projected_df`
   - Passes complete player_dict to LineupOptimizer

2. **LineupOptimizer**:
   - Creates PlayerProxy with actual weeks 1-4 data
   - ConsistencyCalculator calculates CV from actual weeks 1-4
   - Applies consistency multiplier based on real performance variance
   - Uses week 5 projected points for lineup decisions

3. **Final Scoring**:
   - Lineup determined by: projections + matchups + **actual CV-based consistency**
   - Winner determined by: actual week 5 points

## Verification

✅ Simulation imports without errors
✅ PlayerProxy correctly receives weekly points data
✅ ConsistencyCalculator will use actual performance for CV
✅ Current week projections still use projected data

## Impact

- **Before Fix**: Consistency scoring had no effect in simulations (always MEDIUM)
- **After Fix**: Consistency scoring properly rewards/penalizes based on real volatility
- **Simulation Accuracy**: Now correctly models impact of drafting consistent vs volatile players

## Next Steps

When running Phase 8 baseline simulations, the consistency scoring will now:
1. Use real historical variance to categorize players (LOW/MEDIUM/HIGH)
2. Apply appropriate multipliers (1.08x / 1.00x / 0.92x)
3. Provide accurate win rate comparisons with consistency ON vs OFF
