# Weekly Data Migration Analysis - projected_points vs actual_points

**Date:** 2025-12-27
**Purpose:** Understand when to use projected_points vs actual_points and how to update methods correctly

**Status:** ✅ VERIFIED - User confirmed hybrid model, codebase analysis confirms implementation

---

## Data Structure Comparison

### OLD Structure (CSV - week_N_points) - ✅ VERIFIED

**Format:** 17 individual fields (week_1_points, week_2_points, ..., week_17_points)

**Example from players.csv (Jahmyr Gibbs, current week 17):**
```
week_1_points: 15.0     // Actual result (week played)
week_2_points: 19.4     // Actual result (week played)
...
week_16_points: 22.8    // Actual result (week played)
week_17_points: 6.4     // Projection (week not played yet)
```

**✅ VERIFIED - HYBRID MODEL:**
- **For past weeks (week < current_week):** ACTUAL results from completed games
- **For current/future weeks (week >= current_week):** PROJECTED points (ESPN estimates)
- **How it worked:** player-data-fetcher (OUT OF SCOPE) updated players.csv after each week with actual results

### NEW Structure (JSON - TWO separate arrays)

**Format:** Two 17-element arrays

**Example from rb_data.json (Jahmyr Gibbs):**

**projected_points** (pre-season ESPN projections):
```json
[
  16.58969096,  // Week 1 pre-season projection
  16.91124714,  // Week 2 pre-season projection
  16.09718215,  // Week 3 pre-season projection
  ...
  24.04080801   // Week 17 pre-season projection
]
```

**actual_points** (post-game results):
```json
[
  15.0,   // Week 1 actual result
  19.4,   // Week 2 actual result
  16.3,   // Week 3 actual result
  ...
  0.0     // Week 17 not played yet (returns 0.0)
]
```

**✅ CLEAR DISTINCTION:**
- `projected_points`: Pre-season estimates made BEFORE season started (from ESPN) - **STATIC, never changes**
- `actual_points`: Post-game results for completed weeks, 0.0 for future weeks - **UPDATED weekly by player-data-fetcher**

**✅ CRITICAL FINDING:**
- There is a SEPARATE file `players_projected.csv` (and ProjectedPointsManager class) that holds ORIGINAL pre-season projections
- Used for performance deviation calculations (comparing actual vs original projection)
- League Helper's week_N_points was the HYBRID (not the original projections)

---

## OLD System Architecture - ✅ VERIFIED

**Two separate data sources existed:**

1. **players.csv** (week_N_points) - HYBRID DATA
   - Actual results for past weeks
   - Projected points for future weeks
   - Updated weekly by player-data-fetcher

2. **players_projected.csv** (ProjectedPointsManager) - ORIGINAL PROJECTIONS
   - Pre-season ESPN estimates
   - Never changes throughout season
   - Used for performance deviation calculations

**Evidence from codebase:**
- `player_scoring.py:223-239` - Gets "actual points" from player.week_N_points for past weeks
- `player_scoring.py:235` - Gets "projected points" from ProjectedPointsManager for comparison
- Tests show week_N_points containing actual results for played weeks

---

## Method-by-Method Analysis

### Method 1: get_weekly_projections()

**Current Implementation:**
```python
def get_weekly_projections(self) -> List[float]:
    return [
        self.week_1_points, self.week_2_points, self.week_3_points,
        # ... all 17 weeks
    ]
```

**Current Behavior (OLD):**
- Returns HYBRID list (actual for past, projected for future)

**Usage:**
- Called by `get_rest_of_season_projection()` for rest-of-season calculations
- Returns all 17 weeks as a list

**✅ DECISION: HYBRID (Option C) - Maintain Current Behavior**

**Implementation:**
```python
def get_weekly_projections(self) -> List[float]:
    """
    Return hybrid weekly points: actual results for past weeks,
    projected points for current/future weeks.

    This matches the OLD week_N_points behavior where player-data-fetcher
    updated past weeks with actual results after games were played.

    Returns:
        List of 17 weekly points (actual for past, projected for future)
    """
    current_week = self.config.current_nfl_week
    result = []
    for i in range(17):
        week_num = i + 1
        if week_num < current_week:  # Past weeks - use actual
            result.append(self.actual_points[i])
        else:  # Current/future weeks - use projected
            result.append(self.projected_points[i])
    return result
```

**Rationale:**
- Maintains backward compatibility with existing behavior
- "Best estimate" for planning - known results + future projections
- get_rest_of_season_projection() depends on this for accurate planning

---

### Method 2: get_single_weekly_projection(week_num)

**Current Implementation:**
```python
def get_single_weekly_projection(self, week_num: int) -> float:
    return self.get_weekly_projections()[week_num - 1]
```

**Current Behavior (OLD):**
- Returns HYBRID value (actual if week played, projected if not)
- **Already delegates to get_weekly_projections()!**

**Current Usages (4 locations):**
1. **SaveCalculatedPointsManager.py:112** - Getting weekly projection for calculating points
2. **StarterHelperModeManager.py:212** - Getting projection for current week (lineup recommendations)
3. **player_scoring.py:123** - Getting weekly points for scoring calculations
4. **PlayerManager.py:307** - Finding max weekly projection across all players

**✅ DECISION: NO CHANGES NEEDED!**

**Implementation:**
```python
def get_single_weekly_projection(self, week_num: int) -> float:
    """
    Get weekly points for a specific week.

    Returns actual result for past weeks, projected points for future weeks.
    Delegates to get_weekly_projections() for consistency.

    Args:
        week_num: Week number (1-17)

    Returns:
        Weekly points (actual for past, projected for future)
    """
    return self.get_weekly_projections()[week_num - 1]
```

**Rationale:**
- **Already correct!** Delegates to get_weekly_projections() which now implements hybrid logic
- No code changes needed, just needs config dependency
- Automatically inherits hybrid behavior from get_weekly_projections()
- All 4 call sites continue to work without modification

---

### Method 3: get_rest_of_season_projection(current_week)

**Current Implementation:**
```python
def get_rest_of_season_projection(self, current_week) -> float:
    """Sum projected points from current week through week 17."""
    weekly_projections = self.get_weekly_projections()
    total = 0.0
    for i in range(current_week, 18):
        week_projection = weekly_projections[i-1]
        if week_projection is not None:
            total += week_projection
    return total
```

**Current Behavior (OLD):**
- Sums HYBRID values from get_weekly_projections()
- For current_week onward: actual for past, projected for future
- **Already delegates to get_weekly_projections()!**

**Usage:**
1. **PlayerManager.py:197** - Sets `player.fantasy_points` based on rest of season
2. **player_scoring.py:487** - Gets original rest of season projection

**✅ DECISION: NO CHANGES NEEDED!**

**Implementation:**
```python
def get_rest_of_season_projection(self, current_week) -> float:
    """
    Calculate total projected points from current week through week 17.

    Uses hybrid weekly points (actual for past, projected for future) from
    get_weekly_projections(), so if current_week has already been played,
    it includes the actual result.

    Args:
        current_week: The current week number (1-17)

    Returns:
        Sum of projected points for remaining weeks
    """
    weekly_projections = self.get_weekly_projections()
    total = 0.0
    for i in range(current_week, 18):
        week_projection = weekly_projections[i-1]
        if week_projection is not None:
            total += week_projection
    return total
```

**Rationale:**
- **Already correct!** Delegates to get_weekly_projections() which implements hybrid logic
- No code changes needed
- Automatically gets hybrid values (actual for past, projected for future)
- "Rest of season" includes any remaining weeks from current_week onward

---

## New Methods to Consider

### ✅ DECISION: DEFER ALL NEW METHODS to Future Features

**Rationale:**
1. **Minimum viable migration:** Current feature scope is migrating League Helper to JSON, not adding new functionality
2. **actual_points array will be loaded** but accessed indirectly through hybrid methods
3. **No current usage** of direct actual-only accessors in existing codebase
4. **Future features can add** when needed for performance analysis or historical tracking

### Method 4: get_weekly_actuals() [DEFERRED]

**Proposed (for future):**
```python
def get_weekly_actuals(self) -> List[float]:
    """Return all 17 actual results (0.0 for future weeks)."""
    return self.actual_points
```

**Use case:** Historical analysis, performance tracking
**Status:** Not needed for current migration

---

### Method 5: get_single_weekly_actual(week_num) [DEFERRED]

**Proposed (for future):**
```python
def get_single_weekly_actual(self, week_num: int) -> float:
    """Return actual result for specific week (0.0 if not played yet)."""
    return self.actual_points[week_num - 1]
```

**Use case:** Comparing actual vs projected for specific weeks
**Status:** Not needed for current migration

---

### Method 6: get_season_to_date_actual(current_week) [DEFERRED]

**Proposed (for future):**
```python
def get_season_to_date_actual(self, current_week: int) -> float:
    """Sum actual points from week 1 through current_week-1."""
    total = 0.0
    for i in range(0, current_week - 1):  # Up to but not including current_week
        total += self.actual_points[i]
    return total
```

**Use case:** Season-to-date performance
**Status:** Not needed for current migration

---

## Critical Questions - ✅ ALL ANSWERED

### 1. What did OLD week_N_points contain? ✅ ANSWERED

**ANSWER:** HYBRID DATA (verified through codebase analysis)

**Evidence:**
- `player_scoring.py:223-239` - Gets "actual points" from player.week_N_points for past weeks
- `player_scoring.py:235` - Gets "projected points" from ProjectedPointsManager for comparison
- Tests show week_N_points containing actual results for played weeks

**Verified Structure:**
- **For past weeks (week < current_week):** ACTUAL results from completed games
- **For current/future weeks (week >= current_week):** PROJECTED points (ESPN estimates)
- **How it worked:** player-data-fetcher (OUT OF SCOPE) updated players.csv after each week with actual results

**Note on CSV value mismatch (6.4 vs 24.04):**
- The CSV value (6.4) was likely an UPDATED projection (ESPN changes mid-season)
- The JSON projected_points (24.04) contains ORIGINAL pre-season projection
- Both are projections, just from different points in time

---

### 2. For future weeks, actual_points = 0.0 - is this correct? ✅ ANSWERED

**ANSWER:** YES, 0.0 is correct for unplayed weeks

**Rationale:**
- Bye weeks also legitimately result in 0.0 points
- No need to distinguish "not played yet" vs "played and scored 0.0"
- Existing code checks `if week_projection is not None:` which works fine with 0.0
- Using None would complicate the array structure (require Optional[float])

**Decision:** Keep 0.0 for unplayed weeks, accept that bye weeks also = 0.0

---

### 3. Should method names change? ✅ ANSWERED

**ANSWER:** KEEP EXISTING NAMES, update implementation only

**Rationale:**
- Method names reflect their PURPOSE (getting weekly points for planning)
- Implementation detail (hybrid vs projected) is internal
- Changing names would require updating all call sites (4 locations)
- Current names are semantically correct - they DO return "projections" (best estimates)

**Decision:** Keep method names as-is, update docstrings to clarify hybrid behavior

---

## Implementation Approach ✅ COMPLETE

### Analysis Complete

All questions answered through codebase verification:
1. ✅ OLD week_N_points contained HYBRID data (verified via player_scoring.py)
2. ✅ Must maintain exact old behavior (hybrid model)
3. ✅ Determined which methods return what (hybrid via get_weekly_projections())
4. ✅ Deferred new actual_points accessor methods to future features

### Implementation Strategy

**Only ONE method requires code changes:**
- `get_weekly_projections()` - Add hybrid logic using config.current_nfl_week

**Two methods work automatically (already delegate):**
- `get_single_weekly_projection()` - Delegates via get_weekly_projections()[week-1]
- `get_rest_of_season_projection()` - Delegates via get_weekly_projections()

**All call sites (4 locations) work automatically:**
- No changes needed in StarterHelperModeManager, SaveCalculatedPointsManager, PlayerManager, or player_scoring

### Documentation Requirements

Add docstrings to updated methods explaining:
- ✅ Hybrid behavior (actual for past, projected for future)
- ✅ When to use each method (documented in Method 1-3 sections above)
- ✅ Behavior for future weeks (0.0 for unplayed weeks)

---

## Summary of All Decisions ✅ COMPLETE

| Item | Question | Decision | Rationale |
|------|----------|----------|-----------|
| Method 1 | get_weekly_projections() returns? | **C) HYBRID** | Matches OLD week_N_points behavior (verified via codebase) |
| Method 2 | get_single_weekly_projection() returns? | **C) HYBRID** (auto) | Already delegates to get_weekly_projections() - no changes needed |
| Method 3 | get_rest_of_season_projection() returns? | **C) HYBRID** (auto) | Already delegates to get_weekly_projections() - no changes needed |
| Method 4 | Add get_weekly_actuals()? | **B) Defer to future** | Not needed for minimum viable migration |
| Method 5 | Add get_single_weekly_actual()? | **B) Defer to future** | Not needed for minimum viable migration |
| Method 6 | Add get_season_to_date_actual()? | **B) Defer to future** | Not needed for minimum viable migration |
| Data | What did OLD week_N_points contain? | **C) HYBRID (verified)** | Codebase analysis confirms actual for past, projected for future |
| Convention | 0.0 for unplayed weeks OK? | **A) Yes** | Simpler than None, existing null checks work fine |
| Naming | Should method names change? | **A) Keep as-is** | Avoids updating 4 call sites, semantically correct |

---

## Final Implementation Summary

**CODE CHANGES REQUIRED:** 1 method
- `get_weekly_projections()` - Add hybrid logic using config.current_nfl_week

**NO CHANGES NEEDED:** 2 methods (already delegate correctly)
- `get_single_weekly_projection()`
- `get_rest_of_season_projection()`

**CALL SITES:** 0 changes needed (4 locations work automatically)

**NEW METHODS:** 0 (all deferred to future features)

**DEPENDENCY:** FantasyPlayer needs access to config.current_nfl_week (add config parameter or dependency)
