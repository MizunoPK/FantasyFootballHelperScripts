# ProjectedPointsManager Migration Analysis

**Date:** 2025-12-27
**Purpose:** Determine changes needed to migrate ProjectedPointsManager from players_projected.csv to JSON projected_points arrays

---

## Current Implementation

### File: `league_helper/util/ProjectedPointsManager.py`

**Purpose:**
- Manages access to ORIGINAL pre-season projected points
- Used for performance deviation calculations (comparing actual vs original projection)
- Separate from the hybrid week_N_points that gets updated weekly

**Data Source:**
- `data/players_projected.csv`
- Format: `id,name,week_1_points,week_2_points,...,week_17_points`
- Contains STATIC pre-season projections (never changes during season)

**Key Methods:**
1. `__init__(config, data_folder)` - Loads CSV on initialization
2. `_load_projected_data()` - Loads CSV into pandas DataFrame, creates name_lower column for matching
3. `get_projected_points(player, week_num)` - Returns float for specific player/week (or None)
4. `get_projected_points_array(player, start_week, end_week)` - Returns list of floats for week range
5. `get_historical_projected_points(player)` - Returns list for weeks 1 to current-1

**Player Lookup:**
- Uses **PLAYER NAME** (case-insensitive) for matching
- Creates normalized `name_lower` column for efficient lookups
- Does NOT use player ID

**Return Values:**
- `float` for valid data
- `None` for missing/unavailable data
- Handles pandas NaN gracefully

---

## Usage Analysis

### 1. PlayerManager (line 113)
```python
self.projected_points_manager = ProjectedPointsManager(config, data_folder)
```
**Usage:** Creates instance, passes to player_scoring

### 2. player_scoring.py (line 235)
```python
# Get projected points from ProjectedPointsManager
projected_points = self.projected_points_manager.get_projected_points(player, week)
```
**Usage:** Gets ORIGINAL projection for performance deviation calculation
**Context:** Comparing actual_points vs original projected_points to calculate performance multiplier

---

## New Data Source (JSON)

### Location: `data/player_data/*.json` (6 position files)

**Structure:**
```json
{
  "qb_data": [
    {
      "id": 4429795,
      "name": "Jahmyr Gibbs",
      "projected_points": [18.41926089, 18.07282489, ..., 20.78756694],
      ...
    }
  ]
}
```

**Key Points:**
- `projected_points` is a 17-element array (index 0 = week 1, index 16 = week 17)
- Contains SAME data as players_projected.csv (original pre-season projections)
- Already available in FantasyPlayer objects after from_json() loads them

---

## Migration Strategy

### ✅ REVISED APPROACH: Consolidate into PlayerManager (RECOMMENDED)

**Approach:** Add projection accessor methods to PlayerManager instead of maintaining separate class

**Why Consolidate:**
- PlayerManager already loads projected_points arrays from JSON
- ProjectedPointsManager would load same data from same files
- Eliminates duplicate data loading and storage
- Simpler architecture - PlayerManager is THE source for all player data
- Reduces code by ~200 lines

**Pros:**
- ✅ No duplicate data loading (PlayerManager already has projected_points)
- ✅ Simpler architecture (one less class to maintain)
- ✅ Single source of truth for all player data
- ✅ Less memory usage (no duplicate projection storage)
- ✅ Fewer implementation items (~9 vs 23)

**Cons:**
- ⚠️ Minor caller changes (player_scoring.py needs 1 line update)
- ⚠️ PlayerManager grows slightly (3 new methods)

### ~~Option A: Update ProjectedPointsManager to Read JSON~~ (SUPERSEDED)

**This option kept ProjectedPointsManager as separate class reading JSON.**

~~**Approach:** Update _load_projected_data() to read 6 JSON files instead of CSV~~

**Why Not Chosen:**
- Would duplicate data loading (PlayerManager already loads same JSON)
- More code to maintain for no benefit
- Creates unnecessary complexity

**Consolidation Implementation:**

```python
# Add to: league_helper/util/PlayerManager.py

def get_projected_points(self, player: FantasyPlayer, week_num: int) -> Optional[float]:
    """
    Get original projected points for specific player and week.

    Used for performance deviation calculations (actual vs original projection).

    Args:
        player: FantasyPlayer object
        week_num: Week number (1-17)

    Returns:
        Float projected points or None if unavailable

    Note:
        Replaces ProjectedPointsManager.get_projected_points().
        Uses projected_points array already loaded in FantasyPlayer objects.
    """
    # Validate week number
    if week_num < 1 or week_num > 17:
        return None

    # Check if player has projected_points array
    if not player.projected_points or len(player.projected_points) < week_num:
        return None

    # Get value from array (week_num=1 is index 0)
    projected_value = player.projected_points[week_num - 1]

    # Handle 0.0 as None (bye week or no projection available)
    if projected_value == 0.0:
        return None

    return float(projected_value)

def get_projected_points_array(self, player: FantasyPlayer, start_week: int, end_week: int) -> List[Optional[float]]:
    """
    Get projected points for a range of weeks.

    Args:
        player: FantasyPlayer object
        start_week: Starting week (1-17)
        end_week: Ending week (1-17)

    Returns:
        List of projected points (None for unavailable weeks)
    """
    result = []
    for week in range(start_week, end_week + 1):
        result.append(self.get_projected_points(player, week))
    return result

def get_historical_projected_points(self, player: FantasyPlayer, current_week: int) -> List[Optional[float]]:
    """
    Get projected points for weeks 1 to current_week-1.

    Args:
        player: FantasyPlayer object
        current_week: Current NFL week

    Returns:
        List of historical projected points
    """
    if current_week <= 1:
        return []
    return self.get_projected_points_array(player, 1, current_week - 1)
```

**Changes Required:**
1. Add 3 methods to PlayerManager (above)
2. Update PlayerManager.__init__() to remove ProjectedPointsManager instantiation
3. Update player_scoring.py to use `self.player_manager.get_projected_points()` instead of `self.projected_points_manager.get_projected_points()`
4. Mark ProjectedPointsManager.py as deprecated
5. Update tests to test PlayerManager methods instead

---

### Option B: Use PlayerManager's Loaded Players

**Approach:** Instead of loading data separately, use player objects from PlayerManager

**Pros:**
- No duplicate data loading
- Simpler implementation
- Automatic consistency with loaded players

**Cons:**
- Requires passing player list to ProjectedPointsManager
- Changes interface (constructor signature)
- Tighter coupling between PlayerManager and ProjectedPointsManager
- Circular dependency risk

**NOT RECOMMENDED** - Option A maintains better separation of concerns

---

## Comparison: CSV vs JSON Data

### Data Verification

**CSV (players_projected.csv):**
```
4429795,Jahmyr Gibbs,18.41926089,18.07282489,...,20.78756694
```

**JSON (rb_data.json):**
```json
{
  "id": 4429795,
  "name": "Jahmyr Gibbs",
  "projected_points": [18.41926089, 18.07282489, ..., 20.78756694]
}
```

**✅ DATA IS IDENTICAL** - Just different container format

---

## Implementation Checklist (REVISED for Consolidation)

**Phase 1: Add Methods to PlayerManager (3 items)**

- [ ] **NEW-100:** Add get_projected_points() method to PlayerManager
  - Returns Optional[float] for specific player/week
  - Validates week number (1-17)
  - Handles 0.0 as None (bye weeks)
  - **File:** league_helper/util/PlayerManager.py (~15 lines)

- [ ] **NEW-101:** Add get_projected_points_array() method to PlayerManager
  - Returns List[Optional[float]] for week range
  - Delegates to get_projected_points() for each week
  - **File:** league_helper/util/PlayerManager.py (~5 lines)

- [ ] **NEW-102:** Add get_historical_projected_points() method to PlayerManager
  - Returns historical projections (weeks 1 to current-1)
  - Delegates to get_projected_points_array()
  - **File:** league_helper/util/PlayerManager.py (~5 lines)

**Phase 2: Update Callers (2 items)**

- [ ] **NEW-103:** Remove ProjectedPointsManager from PlayerManager.__init__()
  - **Line:** league_helper/util/PlayerManager.py:113
  - **Remove:** self.projected_points_manager = ProjectedPointsManager(config, data_folder)
  - **Remove:** import statement for ProjectedPointsManager

- [ ] **NEW-104:** Update player_scoring.py to use PlayerManager methods
  - **Line:** league_helper/util/player_scoring.py:235
  - **OLD:** self.projected_points_manager.get_projected_points(player, week)
  - **NEW:** self.player_manager.get_projected_points(player, week)

**Phase 3: Deprecate Old Code (1 item)**

- [ ] **NEW-105:** Mark ProjectedPointsManager as deprecated
  - **File:** league_helper/util/ProjectedPointsManager.py (module docstring)
  - **Action:** Add DEPRECATED notice directing to PlayerManager methods
  - **Keep file:** For potential out-of-scope dependencies
  - **Future:** Remove in separate cleanup

**Phase 4: Testing (3 items)**

- [ ] **NEW-106:** Add tests for new PlayerManager projection methods
  - **File:** tests/league_helper/util/test_PlayerManager.py
  - Test get_projected_points() with valid/invalid weeks
  - Test get_projected_points_array() with ranges
  - Test get_historical_projected_points()
  - Test 0.0 handling (bye weeks)

- [ ] **NEW-107:** Update player_scoring tests
  - **File:** tests/league_helper/util/test_player_scoring.py
  - Verify performance multiplier calculations work
  - Verify calls to player_manager.get_projected_points()

- [ ] **NEW-108:** Integration test - scoring calculations
  - **File:** tests/integration/test_league_helper_integration.py
  - Verify performance deviation calculations
  - Verify no regressions in player scoring

**Phase 5: Cleanup (1 item)**

- [ ] **NEW-109:** Mark players_projected.csv as deprecated
  - **Action:** Rename to players_projected.csv.OLD or add deprecation comment
  - **Keep temporarily:** For validation during migration
  - **File:** data/players_projected.csv

**Total:** 10 new checklist items (NEW-100 through NEW-109)
**Reduction:** 23 items → 10 items (13 fewer items!)

---

## Key Design Decisions

### 1. Keep In-Memory Lookup?

**Current:** Pandas DataFrame with name_lower column
**Proposed:** Python dict with {name_lower: projected_points_array}

**DECISION:** ✅ YES - Keep in-memory lookup
- Maintains O(1) lookup performance
- Simpler than DataFrame (no pandas dependency)
- Efficient for repeated lookups during scoring

### 2. Handle 0.0 in Array?

**Question:** In JSON, 0.0 in projected_points array = no projection or valid 0.0 projection?

**Evidence:**
- Jahmyr Gibbs week 8: 0.0 in CSV, likely bye week
- Christian McCaffrey week 14: 0.0 in CSV, likely bye week

**DECISION:** ✅ Treat 0.0 as "no projection" (return None)
- Matches current CSV behavior (NaN → None)
- Bye weeks legitimately have 0.0 projection
- Consistent with existing logic

### 3. Remove players_projected.csv?

**DECISION:** ⏳ DEFER to cleanup phase
- Keep file during development for comparison/validation
- Mark as deprecated after migration complete
- Can remove in future cleanup

---

## Impact Assessment (REVISED for Consolidation)

### Files Requiring Changes: 2 files

1. **league_helper/util/PlayerManager.py** - Add 3 projection accessor methods, remove ProjectedPointsManager instantiation
2. **league_helper/util/player_scoring.py** - Update 1 line to call player_manager methods

### Files Being Deprecated: 1 file

1. **league_helper/util/ProjectedPointsManager.py** - Mark as deprecated (entire class ~200 lines becomes obsolete)

### Test Files Requiring Updates: 2 files

1. **tests/league_helper/util/test_PlayerManager.py** - Add tests for new projection methods
2. **tests/league_helper/util/test_player_scoring.py** - Verify calls to player_manager methods

---

## Migration Risks (REVISED for Consolidation)

**VERY LOW RISK:**
- Simple methods (delegate to existing projected_points arrays)
- Data already loaded by PlayerManager (no new loading logic)
- Only 1 caller to update (player_scoring.py)
- No dependencies on other migration work
- Reduces complexity (eliminates ~200 lines of code)

**TESTING CRITICAL:**
- Performance deviation calculations are complex
- Must verify exact same results as before
- Integration tests required for player_scoring

---

## Recommended Approach (REVISED)

✅ **CONSOLIDATE INTO PLAYERMANAGER**

1. **Add 3 methods to PlayerManager** (get_projected_points, get_projected_points_array, get_historical_projected_points)
2. **Update 1 caller** (player_scoring.py line 235)
3. **Deprecate ProjectedPointsManager** (mark as obsolete)
4. **Comprehensive testing** (unit + integration)
5. **Verify performance calculations** (same results as before)
6. **Keep players_projected.csv temporarily** (for validation)

**Why This Approach:**
- PlayerManager already has projected_points data
- No duplicate data loading
- Simpler architecture
- Fewer items to implement (10 vs 23)
- Reduces codebase by ~200 lines

---

## Next Steps

1. ✅ Update NEW-100 through NEW-109 in main checklist (consolidation approach)
2. Add 3 projection methods to PlayerManager
3. Remove ProjectedPointsManager instantiation from PlayerManager.__init__()
4. Update player_scoring.py caller
5. Add tests for new PlayerManager methods
6. Run integration tests to verify player_scoring
7. Mark ProjectedPointsManager and players_projected.csv as deprecated

---

## Summary (REVISED)

**Migration Scope:** VERY SMALL (2 files, 10 items)
**Complexity:** VERY LOW (simple delegation to existing arrays)
**Risk:** VERY LOW (no new data loading, minimal caller changes)
**Dependencies:** NONE (independent of other migration work)
**Priority:** MEDIUM (needed for complete CSV elimination)
**Impact:** Eliminates ~200 lines of code (entire ProjectedPointsManager class)

**Recommendation:** ✅ Consolidate into PlayerManager (approved by user 2025-12-27)
