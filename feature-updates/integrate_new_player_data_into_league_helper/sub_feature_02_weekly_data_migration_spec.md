# Sub-Feature 2: Weekly Data Migration

## Objective

Replace the 17 individual `week_N_points` fields with two 17-element arrays (`projected_points` and `actual_points`). This provides clean separation between pre-season projections and actual game results.

## Dependencies

**Prerequisites:** Sub-feature 1 (Core Data Loading) - requires projected_points/actual_points arrays to be loaded from JSON

**Blocks:** Sub-features 5, 6 (ProjectedPointsManager, TeamDataManager)

## Scope

### Checklist Items (24 total)

**Field Removal (NEW-22a to NEW-22c):**
- NEW-22a: Remove all 17 week_N_points field definitions from FantasyPlayer.py:102-118
- NEW-22b: Remove all 17 week_N_points loading lines from from_dict() (FantasyPlayer.py:170-186)
- NEW-22c: Change get_weekly_projections() to return self.projected_points (actually hybrid - see below)

**Method Updates (NEW-22d, NEW-25a to NEW-25f):**
- NEW-22d: Verify get_single_weekly_projection() still works ✅ NO CHANGES NEEDED (delegates to get_weekly_projections)
- NEW-25a: ANALYZE get_weekly_projections() ✅ RESOLVED - Implement hybrid logic (actual for past, projected for future)
- NEW-25b: ANALYZE get_single_weekly_projection() ✅ RESOLVED - NO CHANGES (already delegates correctly)
- NEW-25c: ANALYZE get_rest_of_season_projection() ✅ RESOLVED - NO CHANGES (already delegates correctly)
- NEW-25d: DECIDE get_weekly_actuals() ✅ RESOLVED - DEFER to future features
- NEW-25e: DECIDE get_single_weekly_actual() ✅ RESOLVED - DEFER to future features
- NEW-25f: DECIDE get_rest_of_season_actual() ✅ RESOLVED - DEFER to future features

**Call Site Updates (NEW-22e to NEW-22l):**
- NEW-22e: VERIFY SaveCalculatedPointsManager.py:112 (uses method, no changes needed)
- NEW-22f: VERIFY StarterHelperModeManager.py:212 (uses method, no changes needed)
- NEW-22g: VERIFY player_scoring.py:123 (uses method, no changes needed)
- NEW-22h: VERIFY PlayerManager.py:307 (uses method, no changes needed)
- NEW-22i: UPDATE PlayerManager.py:375-379 - CSV fieldnames for save_players() (covered in Sub-feature 4)
- NEW-22j: UPDATE comment PlayerManager.py:633 about dict format
- NEW-22k: UPDATE/VERIFY TeamDataManager.py:83, 119 comments (covered in Sub-feature 6)
- NEW-22l: UPDATE/VERIFY ProjectedPointsManager.py:53, 108-109 (covered in Sub-feature 5)

**Additional Updates (NEW-23 to NEW-30):**
- NEW-23: Replace direct field access with method calls (NONE FOUND - already using methods!)
- NEW-24: Update any loops building weekly lists (handled by get_weekly_projections method)
- NEW-26: Unit test for get_weekly_projections() with arrays
- NEW-27: Unit test for get_single_weekly_projection(week) boundary cases
- NEW-28: Unit test for new get_weekly_actuals() methods (DEFERRED)
- NEW-29: Integration test for modes using weekly data
- NEW-30: Test from_json() loads both arrays correctly (covered in Sub-feature 1)

**Backward Compatibility (NEW-19):**
- NEW-19: RESOLVED - Immediate cutover, NO backward compatibility for week_N_points

## Verification Findings (From Deep Dive)

### Code Search Results

**NEW-1: Direct field access search (`.week_\d+_points`)**
- **Finding:** Only found in utils/FantasyPlayer.py (field definitions)
- **Action:** Covered by NEW-22a (remove field definitions)
- **Conclusion:** No direct field access in league_helper/ code - excellent encapsulation

**NEW-2: Dynamic attribute access (`getattr(player, f"week_{week}_points")`)**
- **CRITICAL FINDING:** league_helper/util/ConfigManager.py:598
- **Location:** Inside `calculate_player_median()` helper function within `calculate_bye_week_penalty()`
- **Code:** `if (points := getattr(player, f'week_{week}_points')) is not None`
- **Action:** NEW-22m created - must update to use `player.get_weekly_projections()[week-1]`
- **Impact:** This is the ONLY location using dynamic getattr - isolated fix

**NEW-3: Dictionary access (`player_dict['week_X_points']`)**
- **Finding:** None found
- **Conclusion:** No dictionary-based access to weekly points

**NEW-4: Modules accessing weekly data**
- **Finding:** 4 files use `get_single_weekly_projection()`:
  - SaveCalculatedPointsManager.py:112
  - player_scoring.py:123
  - PlayerManager.py:307
  - StarterHelperModeManager.py:212
- **Plus:** ConfigManager.py:598 uses dynamic getattr (see NEW-2)
- **All use method calls** (not direct field access) - confirms good design

### Verified Locations

**FantasyPlayer.py field definitions (NEW-22a, NEW-22b):**
- **Lines 102-118:** All 17 week_N_points field definitions
- **Lines 170-186:** All 17 week_N_points loading lines in from_dict()
- **Action:** Delete during implementation

**FantasyPlayer.py method updates (NEW-22c, NEW-22d):**
- **Lines 345-351:** get_weekly_projections() current implementation (returns list of week_N_points)
- **Line 353-354:** get_single_weekly_projection() delegates to get_weekly_projections()
- **Action:** Update get_weekly_projections() to implement HYBRID logic
- **No changes needed:** get_single_weekly_projection() will automatically use new logic

**Call sites verified (NEW-22e through NEW-22h):**
- All 4 locations use method calls, not direct field access
- **No changes needed** - methods will work automatically after implementation
- This confirms excellent encapsulation in the codebase

**PlayerManager.py updates (NEW-22i, NEW-22j):**
- **Lines 375-379:** CSV fieldnames include all 17 week_N_points
- **Line 633:** Docstring references week_N_points dict format
- **NEW-22i deferred:** Sub-feature 4 handles save_players() migration
- **NEW-22j:** Update docstring to reference arrays instead of individual fields

**TeamDataManager.py comments (NEW-22k):**
- **Lines 83, 119:** Comments mention week_N_points structure for D/ST data
- **Deferred:** Sub-feature 6 handles TeamDataManager D/ST migration

**ProjectedPointsManager.py comments (NEW-22l):**
- **Lines 53, 108-109:** Comments about CSV week_N_points columns
- **Deferred:** Sub-feature 5 consolidates ProjectedPointsManager

**ConfigManager.py dynamic getattr (NEW-22m - NEW DISCOVERY):**
- **Lines 595-600:** calculate_bye_week_penalty() uses dynamic getattr
- **Code:** `getattr(player, f'week_{week}_points')`
- **Update to:** `player.get_weekly_projections()[week-1]`
- **Impact:** Must be updated in this sub-feature (can't defer)

### Key Design Insight

**Excellent news:** ALL user-facing code uses METHODS, not direct field access!
- Only FantasyPlayer.py needs core changes
- Method calls will work automatically after implementation
- Only 1 dynamic getattr location to fix (ConfigManager.py)
- This confirms the codebase has good encapsulation

## Implementation Details

### Key Finding from Research

**CRITICAL:** Old week_N_points contained HYBRID data:
- For past weeks (week < current_week): ACTUAL results
- For future weeks (week >= current_week): PROJECTED points

**This behavior must be preserved** in get_weekly_projections() to maintain backward compatibility.

### get_weekly_projections() - HYBRID LOGIC (Only Method Requiring Changes)

```python
def get_weekly_projections(self, config) -> List[float]:
    """
    Return hybrid weekly points: actual results for past weeks,
    projected points for current/future weeks.

    This maintains backward compatibility with the old week_N_points
    behavior where player-data-fetcher updated past weeks with actual
    results after games were played.

    Args:
        config: ConfigManager instance (for current_nfl_week)

    Returns:
        List of 17 weekly points (actual for past, projected for future)

    Note:
        This replaces the old pattern:
        [self.week_1_points, ..., self.week_17_points]
    """
    current_week = config.current_nfl_week
    result = []

    for i in range(17):
        week_num = i + 1
        if week_num < current_week:  # Past weeks - use actual
            result.append(self.actual_points[i])
        else:  # Current/future weeks - use projected
            result.append(self.projected_points[i])

    return result
```

**CRITICAL DEPENDENCY:** FantasyPlayer now needs access to config to implement hybrid logic.

### get_single_weekly_projection() - NO CHANGES NEEDED

```python
def get_single_weekly_projection(self, week_num: int, config) -> float:
    """
    Get weekly points for a specific week.

    Returns actual result for past weeks, projected points for future weeks.
    Delegates to get_weekly_projections() for consistency.

    Args:
        week_num: Week number (1-17)
        config: ConfigManager instance

    Returns:
        Weekly points (actual for past, projected for future)
    """
    # Already delegates correctly - just needs config parameter added
    return self.get_weekly_projections(config)[week_num - 1]
```

### get_rest_of_season_projection() - NO CHANGES NEEDED

```python
def get_rest_of_season_projection(self, current_week, config) -> float:
    """
    Calculate total projected points from current week through week 17.

    Uses hybrid weekly points from get_weekly_projections(), so if
    current_week has already been played, it includes the actual result.

    Args:
        current_week: The current week number (1-17)
        config: ConfigManager instance

    Returns:
        Sum of projected points for remaining weeks
    """
    # Already delegates correctly - just needs config parameter
    weekly_projections = self.get_weekly_projections(config)
    total = 0.0
    for i in range(current_week, 18):
        week_projection = weekly_projections[i-1]
        if week_projection is not None:
            total += week_projection
    return total
```

### Field Removal

**Remove from FantasyPlayer.py:**
```python
# DELETE THESE 17 FIELDS (lines 102-118):
week_1_points: float = 0.0
week_2_points: float = 0.0
# ... all the way to ...
week_17_points: float = 0.0
```

**Remove from from_dict():**
```python
# DELETE THESE 17 LINES (lines 170-186):
week_1_points=safe_float_conversion(data.get('week_1_points'), 0.0),
week_2_points=safe_float_conversion(data.get('week_2_points'), 0.0),
# ... all the way to ...
week_17_points=safe_float_conversion(data.get('week_17_points'), 0.0),
```

## Testing Requirements

### Unit Tests

**Test get_weekly_projections() hybrid logic:**
- Mock config.current_nfl_week = 5
- Set actual_points = [10, 20, 30, 40, 50, ...]
- Set projected_points = [15, 25, 35, 45, 55, ...]
- Call get_weekly_projections(config)
- Verify result = [10, 20, 30, 40, projected[4], projected[5], ..., projected[16]]
- Weeks 1-4 should be actual (past weeks)
- Weeks 5-17 should be projected (current/future)

**Test get_single_weekly_projection():**
- Test week 1 (past) returns actual_points[0]
- Test week 10 (future) returns projected_points[9]
- Test week = current_week returns projected (not actual)
- Test invalid week (0, 18, -1) returns None or raises error

**Test get_rest_of_season_projection():**
- Mock current_week = 10
- Verify sums weeks 10-17 from hybrid array
- Verify includes actual result if week 10 already played

**Test array access patterns:**
- Verify no code accesses week_N_points fields
- Verify all code uses methods (get_weekly_projections, etc.)

### Integration Tests

**Test with StarterHelperMode:**
- Load players from JSON
- Run lineup optimization
- Verify uses correct weekly projections (hybrid)
- Verify no crashes or errors

**Test with AddToRosterMode:**
- Load players from JSON
- Get draft recommendations
- Verify uses correct projections
- Verify no crashes

**Test with player_scoring.py:**
- Run performance deviation calculations
- Verify gets correct actual vs projected comparisons
- Verify hybrid logic works correctly

## Success Criteria

✅ **Field Migration:**
- [ ] All 17 week_N_points fields removed from FantasyPlayer
- [ ] No code references week_N_points anywhere in league_helper/
- [ ] projected_points and actual_points arrays working

✅ **Method Updates:**
- [ ] get_weekly_projections() implements hybrid logic correctly
- [ ] get_single_weekly_projection() inherits hybrid behavior automatically
- [ ] get_rest_of_season_projection() inherits hybrid behavior automatically
- [ ] All 3 methods accept config parameter

✅ **Call Sites:**
- [ ] All 4 call sites verified working (SaveCalculated, StarterHelper, player_scoring, PlayerManager)
- [ ] No changes required to call sites (methods already used, not fields)

✅ **Testing:**
- [ ] All unit tests passing
- [ ] Integration tests with all 4 modes passing
- [ ] Hybrid logic verified with different current_week values

✅ **Code Quality:**
- [ ] Comprehensive docstrings on updated methods
- [ ] Comments updated to reference new arrays
- [ ] No dead code (all week_N_points removed)

## Notes

**Critical Design Decision:**
- get_weekly_projections() implements **HYBRID** logic (not pure projected)
- This maintains backward compatibility with old week_N_points behavior
- Past weeks return actual results, future weeks return projections

**Methods That Work Automatically:**
- get_single_weekly_projection() - delegates to get_weekly_projections()
- get_rest_of_season_projection() - delegates to get_weekly_projections()
- **NO CODE CHANGES** needed for these two methods (just add config parameter)

**Config Dependency:**
- FantasyPlayer methods now need access to ConfigManager
- Pass config as parameter to methods that need current_nfl_week
- Alternative: Store config reference in FantasyPlayer.__init__()

**Deferred Methods:**
- get_weekly_actuals() - not needed yet
- get_single_weekly_actual() - not needed yet
- get_rest_of_season_actual() - not needed yet
- Can add these in future features if needed

**Out of Scope:**
- PlayerManager.save_players() CSV fieldnames (Sub-feature 4)
- TeamDataManager D/ST comments (Sub-feature 6)
- ProjectedPointsManager updates (Sub-feature 5)
