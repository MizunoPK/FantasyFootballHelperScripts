# Code Changes: MIN_WEEKS Non-Zero Lookback Enhancement

## Overview
This document tracks all code modifications made during the implementation of the MIN_WEEKS non-zero lookback enhancement.

## Status: COMPLETE

---

## Changes Made

### 1. Dynamic Lookback for Performance Deviation
Changed `calculate_performance_deviation()` from fixed window to dynamic lookback algorithm that:
- Works backwards from `current_week - 1` to find MIN_WEEKS valid data points
- Skips bye weeks and injury weeks (where actual = 0 or projected = 0)
- Uses 2x MIN_WEEKS as maximum lookback limit for data freshness
- Maintains strict MIN_WEEKS requirement (returns None if not met)

---

## Files Modified

| File | Type | Description |
|------|------|-------------|
| `league_helper/util/player_scoring.py` | MODIFY | Updated `calculate_performance_deviation()` with dynamic lookback |
| `tests/league_helper/util/test_player_scoring.py` | MODIFY | Added 4 new tests for dynamic lookback scenarios |
| `docs/scoring_v2/05_performance_multiplier.md` | MODIFY | Updated documentation with dynamic lookback behavior |

---

## Detailed Changes

### league_helper/util/player_scoring.py

**Method**: `calculate_performance_deviation()` (lines 167-263)

**Before** (fixed window):
```python
start_week = max(1, self.config.current_nfl_week - min_weeks)
for week in range(start_week, self.config.current_nfl_week):
    # collect deviations, skip if actual == 0
if len(deviations) < min_weeks:
    return None  # Problem: bye week reduces count
```

**After** (dynamic lookback):
```python
# Calculate maximum lookback limit (2x MIN_WEEKS for data freshness)
max_lookback = min_weeks * 2
earliest_week = max(1, self.config.current_nfl_week - max_lookback)

# Dynamic lookback: work backwards from most recent week
deviations = []
week = self.config.current_nfl_week - 1

while len(deviations) < min_weeks and week >= earliest_week:
    # Get week data, skip if actual <= 0 or projected <= 0
    # Add valid deviations to list
    week -= 1

# Strict MIN_WEEKS requirement
if len(deviations) < min_weeks:
    return None
```

**Key Changes**:
- Replaced fixed `range(start_week, current_week)` with `while` loop working backwards
- Added `max_lookback = min_weeks * 2` limit
- Loop continues until MIN_WEEKS valid weeks found or earliest_week reached
- Uses most recent valid weeks first (preserves recency weighting)

---

## Configuration Changes

None required. The 2x MIN_WEEKS lookback limit is calculated from the existing MIN_WEEKS parameter.

---

## Test Modifications

### tests/league_helper/util/test_player_scoring.py

Added 4 new tests to `TestPerformanceDeviation` class:

1. **`test_calculate_performance_deviation_dynamic_lookback_with_bye_week`**
   - Verifies algorithm skips bye week (actual=0) and finds MIN_WEEKS valid data
   - Setup: weeks 1-3 valid, week 4 bye, week 5 valid; current_week=6
   - Expected: Uses weeks 5, 3, 2 (skipping bye week 4)

2. **`test_calculate_performance_deviation_dynamic_lookback_multiple_bye_weeks`**
   - Tests handling of multiple consecutive bye/injury weeks
   - Setup: Two bye weeks in sequence
   - Expected: Looks back further to find MIN_WEEKS valid weeks

3. **`test_calculate_performance_deviation_respects_max_lookback_limit`**
   - Verifies 2x MIN_WEEKS limit is enforced
   - Setup: Valid data only outside lookback limit
   - Expected: Returns None (not unlimited lookback)

4. **`test_calculate_performance_deviation_uses_most_recent_valid_weeks`**
   - Confirms algorithm prioritizes most recent valid weeks
   - Setup: Valid weeks throughout, verify order
   - Expected: Uses closest valid weeks to current week

---

## Verification

### Files Checked But Not Modified
- `league_helper/util/TeamDataManager.py` - Uses team-level data, already handles bye weeks
- `league_helper/util/ConfigManager.py` - No changes needed (MIN_WEEKS getters unchanged)
- `data/league_config.json` - No changes needed (existing MIN_WEEKS values sufficient)

### Requirements Verification
- [x] All requirements from original spec implemented
- [x] All question answers reflected in implementation:
  - Q1: 2x MIN_WEEKS lookback limit ✓
  - Q2: Strict MIN_WEEKS requirement (return None if not met) ✓
  - Q3: Skip weeks with actual=0 OR projected=0 ✓
- [x] All unit tests pass (100%) - 2023 tests passed

---

## Notes

### Why Only Performance Scoring Changed

Analysis during verification revealed that only PERFORMANCE_SCORING uses player-level weekly data that could be affected by bye weeks:

1. **TEAM_QUALITY_SCORING** - Uses team offensive/defensive rankings from `TeamDataManager`, which already handles team bye weeks at the team level
2. **MATCHUP_SCORING** - Uses opponent defense rankings, not player weekly data
3. **SCHEDULE_SCORING** - Uses future schedule data, not historical player performance

### Design Decisions

1. **2x Lookback Limit**: Chosen to balance data freshness with availability. Looking back too far (e.g., week 2 data in week 14) would use stale performance data. The 2x multiplier provides reasonable flexibility for players with 1-2 bye/injury weeks.

2. **Strict MIN_WEEKS**: Maintained as a hard requirement rather than a soft minimum. This preserves the statistical significance that MIN_WEEKS was designed to ensure.

3. **Recency Ordering**: The while loop naturally uses the most recent valid weeks first, which maintains the intent of capturing recent performance trends.
