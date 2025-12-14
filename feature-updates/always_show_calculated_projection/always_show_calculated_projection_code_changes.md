# Always Show Calculated Projection - Code Changes Documentation

## Overview

Added `projected_points` field to ScoredPlayer that shows the **calculated projection** - the final score converted back to fantasy points scale by reversing the normalization. This reflects what the player's adjusted fantasy points would be after all scoring multipliers, bonuses, and penalties.

---

## Files Modified

### 1. league_helper/util/ScoredPlayer.py

**Changes:**
- Added `projected_points` parameter to `__init__()` with default value `0.0` for backward compatibility
- Updated `__str__()` to show new format when `projected_points > 0`

**New format (when projected_points available):**
```
[QB] [KC] Patrick Mahomes - 320.50 pts (Score: 123.45) (Bye=7)
```

**Old format preserved (when projected_points = 0):**
```
[QB] [KC] Patrick Mahomes - 123.45 pts (Bye=7)
```

---

### 2. league_helper/util/player_scoring.py

**Changes:**
- Added calculation to reverse normalization after all scoring steps (line 455-464)
- Pass `calculated_projection` to ScoredPlayer via keyword argument

**Formula:**
```python
calculated_projection = (player_score / normalization_scale) * max_projection
```

Where:
- `player_score` = final score after all 13 scoring steps
- `normalization_scale` = config.normalization_max_scale
- `max_projection` = max_weekly_projection (for weekly) or max_projection (for ROS)

---

## Test Results

**All 2223 tests pass (100%)**

---

## Quality Control Rounds

### QC Round 1
- Reviewed: 2025-12-13
- Issues Found: None
- Status: PASSED

**Verified:**
- ScoredPlayer.__init__() has `projected_points` with default 0.0 (line 32)
- ScoredPlayer stores projected_points (line 59)
- ScoredPlayer.__str__() conditionally shows new format (lines 99-104)
- player_scoring.py calculates reverse normalization (lines 455-464)
- player_scoring.py passes calculated_projection to ScoredPlayer (line 466)

### QC Round 2
- Reviewed: 2025-12-13
- Issues Found: None
- Status: PASSED

**Verified:**
- Edge case: Division by zero protected (lines 461-464)
- Correct max is selected: weekly vs ROS based on use_weekly_projection (line 459)
- Formula matches StarterHelperModeManager approach
- Conditional display works (only shows new format when projected_points > 0)
- Backward compatible for callers not providing projected_points

### QC Round 3
- Reviewed: 2025-12-13
- Issues Found: None
- Status: PASSED

**Verified:**
- ReserveAssessmentModeManager.py uses keyword args and gets default 0.0 (correct)
- All production ScoredPlayer creations accounted for (2 places)
- All 2223 tests pass (100%)
- Backward compatibility confirmed working
