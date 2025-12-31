# Sub-Feature 5: ProjectedPointsManager Consolidation - Checklist

> **IMPORTANT**: When marking items as resolved, also update `sub_feature_05_projected_points_manager_consolidation_spec.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** 11 (REVISED from original 23, corrected count)
**Completed:** 4 (1 analysis + 1 pattern verified + 2 locations verified)
**Remaining:** 7 (2 implementation tasks + 2 deprecation/cleanup + 3 testing deferred)

---

## Analysis & Strategy (1 item - RESOLVED)

- [x] **NEW-47:** ProjectedPointsManager CSV format assumptions ✅ RESOLVED
  - **Finding:** ProjectedPointsManager reads from players_projected.csv (NOT players.csv)
  - **Discovery:** PlayerManager already loads projected_points arrays - no need for separate class!
  - **Migration:** Consolidate into PlayerManager (NEW-100 through NEW-109)
  - **Decision:** Eliminate entire ProjectedPointsManager class, add 3 methods to PlayerManager
  - **Impact:** Eliminates ~200 lines of code, much simpler architecture
  - **See:** PROJECTED_POINTS_MANAGER_ANALYSIS.md for complete details

---

## Phase 1: Add Methods to PlayerManager (3 items)

**Note:** Implementation tasks - patterns verified, full implementation during coding phase

- [x] **NEW-100:** Add get_projected_points() method to PlayerManager ✅ PATTERN VERIFIED
  - **Purpose:** Get original projected points for specific player/week
  - **Signature:** `def get_projected_points(self, player: FantasyPlayer, week: int) -> Optional[float]`
  - **Returns:** Original projected points for that week, or None for bye weeks (0.0 treated as None)
  - **Validates:** Week number (1-17, raise ValueError if out of range)
  - **Uses:** player.projected_points array already loaded from JSON (Sub-feature 1)
  - **File:** league_helper/util/PlayerManager.py (~15 lines)
  - **Verified:** Method does not exist yet in PlayerManager
  - **Implementation pattern provided:**
    ```python
    if week < 1 or week > 17:
        raise ValueError(f"Week must be 1-17, got {week}")
    projected = player.projected_points[week - 1]
    return None if projected == 0.0 else projected
    ```
- [ ] **NEW-101:** Add get_projected_points_array() method to PlayerManager **(IMPLEMENTATION TASK)**
  - **Purpose:** Get projected points for a range of weeks
  - **Signature:** `def get_projected_points_array(self, player: FantasyPlayer, start_week: int, end_week: int) -> List[Optional[float]]`
  - **Returns:** List of projected points (None for bye weeks)
  - **Delegates:** Calls get_projected_points() for each week in range
  - **File:** league_helper/util/PlayerManager.py (~5 lines)
- [ ] **NEW-102:** Add get_historical_projected_points() method to PlayerManager **(IMPLEMENTATION TASK)**
  - **Purpose:** Get historical projections (weeks 1 to current-1)
  - **Signature:** `def get_historical_projected_points(self, player: FantasyPlayer) -> List[Optional[float]]`
  - **Returns:** List of projected points for weeks 1 to current_week-1
  - **Uses:** self.config.current_nfl_week to determine range
  - **Delegates:** Calls get_projected_points_array(player, 1, current_week-1)
  - **File:** league_helper/util/PlayerManager.py (~5 lines)

---

## Phase 2: Update Callers (2 items)

- [x] **NEW-103:** Remove ProjectedPointsManager from PlayerManager.__init__() ✅ VERIFIED
  - **Current locations:**
    - Line 43: `from util.ProjectedPointsManager import ProjectedPointsManager` (import)
    - Line 113: `self.projected_points_manager = ProjectedPointsManager(config, data_folder)` (instantiation)
  - **Actions:**
    - Remove import statement at line 43
    - Remove instantiation at line 113
  - **File:** league_helper/util/PlayerManager.py
- [x] **NEW-104:** Update player_scoring.py to use PlayerManager methods ✅ VERIFIED
  - **Current location:** league_helper/util/player_scoring.py:235
  - **Current code:** `projected_points = self.projected_points_manager.get_projected_points(player, week)`
  - **Update to:** `projected_points = self.player_manager.get_projected_points(player, week)`
  - **Verified:** player_scoring.py already has self.player_manager (passed in __init__)
  - **Additional updates needed:**
    - Lines 53, 65, 77, 86: Update parameter type hints and docstrings (remove ProjectedPointsManager references)
  - **File:** league_helper/util/player_scoring.py

---

## Phase 3: Deprecate Old Code (1 item)

- [ ] **NEW-105:** Mark ProjectedPointsManager as deprecated **(IMPLEMENTATION TASK)**
  - **File:** league_helper/util/ProjectedPointsManager.py (module docstring at top)
  - **Action:** Add DEPRECATED notice directing to PlayerManager methods
  - **Format:**
    ```python
    """
    DEPRECATED: This module is deprecated as of [date].

    Use PlayerManager methods instead:
    - PlayerManager.get_projected_points(player, week)
    - PlayerManager.get_projected_points_array(player, start, end)
    - PlayerManager.get_historical_projected_points(player)

    Reason: PlayerManager already loads projected_points arrays from JSON,
    eliminating the need for a separate class and duplicate data loading.
    """
    ```
  - **Keep file:** For potential out-of-scope dependencies
  - **Future:** Remove in Sub-feature 8 (CSV Deprecation & Cleanup)

---

## Phase 4: Testing (3 items)

**Note:** Testing items deferred to implementation phase - no verification needed during deep dive

- [ ] **NEW-106:** Add tests for new PlayerManager projection methods **(Testing - defer to implementation)**
  - **File:** tests/league_helper/util/test_PlayerManager.py
  - Test get_projected_points() with valid weeks (1-17)
  - Test get_projected_points() with invalid weeks (0, 18) - should raise ValueError
  - Test 0.0 handling (bye weeks - should return None)
  - Test get_projected_points_array() with various week ranges
  - Test get_historical_projected_points() with different current_week values
  - Test with QB, RB, WR, TE, K, DST (all positions)
- [ ] **NEW-107:** Update player_scoring tests **(Testing - defer to implementation)**
  - **File:** tests/league_helper/util/test_player_scoring.py
  - Verify performance multiplier calculations still work
  - Verify calls to player_manager.get_projected_points() instead of projected_points_manager
  - Test performance deviation calculations (actual vs original projection)
  - Verify no regressions in scoring logic
- [ ] **NEW-108:** Integration test - scoring calculations **(Testing - defer to implementation)**
  - **File:** tests/integration/test_league_helper_integration.py
  - Load players from JSON (with projected_points arrays)
  - Calculate player scores using player_scoring module
  - Verify performance deviation calculations work
  - Compare results with old ProjectedPointsManager approach
  - Verify no regressions in player rankings

---

## Phase 5: Cleanup (1 item)

- [ ] **NEW-109:** Mark players_projected.csv as deprecated **(IMPLEMENTATION TASK)**
  - **File:** data/players_projected.csv
  - **Action:** Rename to players_projected.csv.OLD or add deprecation notice
  - **Keep temporarily:** For validation during migration (can compare results)
  - **Future:** Delete in Sub-feature 8 (CSV Deprecation & Cleanup)
  - **Note:** File currently exists, used by ProjectedPointsManager for loading

---

## Success Criteria

✅ **3 projection accessor methods added to PlayerManager**
✅ **player_scoring.py uses PlayerManager methods (not ProjectedPointsManager)**
✅ **ProjectedPointsManager marked as deprecated**
✅ **All unit tests passing (100%)**
✅ **Integration tests verify scoring calculations unchanged**
✅ **Performance deviation calculations working correctly**
✅ **~200 lines of code eliminated (ProjectedPointsManager obsolete)**

---

## Dependencies

**Prerequisites:**
- Sub-feature 1 complete (projected_points arrays loaded from JSON)
- Sub-feature 2 complete (weekly data migration, projected_points arrays available)

**Blocks:**
- None (self-contained consolidation)

---

## Impact Analysis

**Files Modified:** 2
- league_helper/util/PlayerManager.py (add 3 methods, remove ProjectedPointsManager instantiation)
- league_helper/util/player_scoring.py (update 1 method call)

**Files Deprecated:** 1
- league_helper/util/ProjectedPointsManager.py (~200 lines - mark deprecated, remove later)

**Data Files Deprecated:** 1
- data/players_projected.csv (rename to .OLD)

**Risk:** VERY LOW
- Simple delegation to existing projected_points arrays
- No new data loading logic
- Only 1 caller to update (player_scoring.py)
- Reduces complexity significantly

**Benefits:**
- Eliminates duplicate data loading (~200 lines)
- Simpler architecture (one less class to maintain)
- Single source of truth (PlayerManager has all player data)
- No CSV dependency for projections

---

## Key Decisions

✅ **Treat 0.0 in array as None** (represents bye weeks or unavailable data)
✅ **Keep players_projected.csv temporarily** for validation
✅ **Consolidate into PlayerManager** (don't create separate JSON loading in ProjectedPointsManager)
✅ **Verify week bounds** (1-17, raise ValueError if invalid)

---

## Notes

- **Original plan:** Update ProjectedPointsManager to read from JSON (23 items)
- **Discovery:** PlayerManager already has all the data! (projected_points arrays loaded)
- **REVISED plan:** Consolidate into PlayerManager (10 items)
- **Savings:** 13 items eliminated, ~200 lines of code removed
- **Simplicity:** Much simpler approach, natural location for methods
- See PROJECTED_POINTS_MANAGER_ANALYSIS.md for complete analysis
