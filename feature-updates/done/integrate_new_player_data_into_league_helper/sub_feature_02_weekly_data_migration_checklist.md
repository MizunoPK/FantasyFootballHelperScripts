# Sub-Feature 2: Weekly Data Migration - Checklist

> **IMPORTANT**: When marking items as resolved, also update `sub_feature_02_weekly_data_migration_spec.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** 25 (1 new item discovered during verification)
**Completed:** 23 (6 method analysis + 4 code search + 13 codebase sweep verified)
**Remaining:** 2 (implementation tasks - NEW-5 awaiting Sub-feature 1)

---

## Code Search & Analysis (4 items)

- [x] **NEW-1:** Grep for all direct weekly field access (`.week_\d+_points`) ✅ VERIFIED
  - **Finding:** Only utils/FantasyPlayer.py (expected - field definitions)
  - **Action:** Covered by NEW-22a (remove field definitions)
- [x] **NEW-2:** Grep for dynamic attribute access (`getattr(player, f"week_{week}_points")`) ✅ VERIFIED
  - **Finding:** league_helper/util/ConfigManager.py:598 - FOUND ONE!
  - **Location:** `calculate_bye_week_penalty()` method uses dynamic getattr
  - **Action:** NEW ITEM - Must update ConfigManager.py:595-600 to use get_weekly_projections()
  - **Pattern:** Replace `getattr(player, f'week_{week}_points')` with `player.get_weekly_projections()[week-1]`
- [x] **NEW-3:** Grep for dictionary access (`player_dict['week_X_points']`) ✅ VERIFIED
  - **Finding:** None found - no dictionary access to week_N_points
  - **Action:** No changes needed
- [x] **NEW-4:** Identify all modules accessing weekly data ✅ VERIFIED
  - **Finding:** 4 files use get_single_weekly_projection():
    - SaveCalculatedPointsManager.py
    - player_scoring.py
    - PlayerManager.py
    - StarterHelperModeManager.py
  - **All use method calls** (not direct field access) - covered by NEW-22e through NEW-22h
  - **Plus:** ConfigManager.py uses dynamic getattr (see NEW-2)

---

## FantasyPlayer Field Removal (1 item)

- [ ] **NEW-5:** Remove 17 `week_N_points` fields from FantasyPlayer dataclass **(AWAITING SUB-FEATURE 1)**
  - Delete week_1_points through week_17_points field definitions
  - This is a **BREAKING CHANGE** - causes compilation errors in any code still using fields
  - **Rationale:** Clean break approach (Decision 10) - errors guide fixes
  - **Verified:** utils/FantasyPlayer.py:102-118 contains all 17 field definitions
  - **Dependency:** Sub-feature 1 must add projected_points/actual_points fields FIRST

---

## Codebase Sweep - Update All Usage (12 items)

**IN SCOPE - League Helper locations:**

- [x] **NEW-22a:** utils/FantasyPlayer.py:102-118 - Remove all 17 week_N_points field definitions ✅ VERIFIED
  - **Verified:** Lines 102-118 contain all 17 field definitions (week_1_points through week_17_points)
  - **Action:** Delete these 17 lines during implementation
  - **Same as:** NEW-5 (field removal)
- [x] **NEW-22b:** utils/FantasyPlayer.py:170-186 - Remove all 17 week_N_points loading lines from from_dict() ✅ VERIFIED
  - **Verified:** Lines 170-186 in from_dict() load all 17 week_N_points with safe_float_conversion
  - **Action:** Delete these 17 lines during implementation
  - **Note:** from_dict() is OLD CSV loading - will be replaced by from_json() in Sub-feature 1
- [x] **NEW-22c:** utils/FantasyPlayer.py:345-351 - Update get_weekly_projections() to implement HYBRID logic ✅ VERIFIED
  - **Current implementation:** Returns list of 17 week_N_points fields
  - **Required change:** Return HYBRID (actual_points for past, projected_points for future)
  - **Pattern:** Use config.current_nfl_week to determine cutoff
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 1" for complete implementation
- [x] **NEW-22d:** utils/FantasyPlayer.py:353-354 - Verify get_single_weekly_projection() still works ✅ VERIFIED
  - **Current implementation:** `return self.get_weekly_projections()[week_num - 1]`
  - **Verification:** Already delegates to get_weekly_projections() - perfect encapsulation
  - **Action:** NO CHANGES needed - will automatically use HYBRID logic after NEW-22c
- [x] **NEW-22e:** league_helper/save_calculated_points_mode/SaveCalculatedPointsManager.py:112 ✅ VERIFIED
  - **Verified:** Uses `player.get_single_weekly_projection(week)` (method call, not field access)
  - **Action:** NO CHANGES needed - method call will continue working
- [x] **NEW-22f:** league_helper/starter_helper_mode/StarterHelperModeManager.py:212 ✅ VERIFIED
  - **Verified:** Uses `recommendation.player.get_single_weekly_projection(current_week)` (method call)
  - **Action:** NO CHANGES needed - method call will continue working
- [x] **NEW-22g:** league_helper/util/player_scoring.py:123 ✅ VERIFIED
  - **Verified:** Uses `player.get_single_weekly_projection(week)` (method call)
  - **Action:** NO CHANGES needed - method call will continue working
- [x] **NEW-22h:** league_helper/util/PlayerManager.py:307 ✅ VERIFIED
  - **Verified:** Uses `player.get_single_weekly_projection(week_num)` (method call)
  - **Action:** NO CHANGES needed - method call will continue working
- [x] **NEW-22i:** league_helper/util/PlayerManager.py:375-379 - CSV fieldnames in save_players() ✅ VERIFIED
  - **Verified:** Lines 375-379 define fieldnames array with all 17 week_N_points
  - **Decision:** DEFER to Sub-feature 4 (File Update Strategy handles save_players() migration)
  - **Action:** Sub-feature 4 will update this method to write JSON instead of CSV
- [x] **NEW-22j:** league_helper/util/PlayerManager.py:633 - Update comment about dict format ✅ VERIFIED
  - **Verified:** Line 633 docstring mentions 'week_1_points', etc. in player_data dict format
  - **Action:** Update comment during implementation to reference projected_points/actual_points arrays
- [x] **NEW-22k:** league_helper/util/TeamDataManager.py:83, 119 - Update comments about D/ST data ✅ VERIFIED
  - **Verified:** Lines 83 and 119 have comments mentioning week_N_points structure for D/ST
  - **Decision:** DEFER to Sub-feature 6 (TeamDataManager D/ST Migration handles these)
  - **Action:** Sub-feature 6 will update both code and comments together
- [x] **NEW-22l:** league_helper/util/ProjectedPointsManager.py:53, 108-109 - CSV format expectations ✅ VERIFIED
  - **Verified:** Lines 53 and 108-109 have comments about CSV columns (week_N_points)
  - **Decision:** DEFER to Sub-feature 5 (ProjectedPointsManager Consolidation)
  - **Action:** Sub-feature 5 consolidates this entire manager into PlayerManager
- [x] **NEW-22m:** league_helper/util/ConfigManager.py:595-600 - Update calculate_bye_week_penalty() ✅ VERIFIED
  - **CRITICAL FINDING:** Line 598 uses `getattr(player, f'week_{week}_points')`
  - **Location:** Inside calculate_player_median() helper function
  - **Update required:** Replace with `player.get_weekly_projections()[week-1]`
  - **Discovered during:** Verification grep (NEW-2)

---

## Method Updates (3 items)

- [x] **NEW-25a:** ANALYZE get_weekly_projections() ✅ RESOLVED
  - **Decision:** Returns HYBRID (actual for past, projected for future)
  - **Implementation:** Add hybrid logic using config.current_nfl_week
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 1"
- [x] **NEW-25b:** ANALYZE get_single_weekly_projection() ✅ RESOLVED
  - **Decision:** NO CHANGES - already delegates correctly
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 2"
- [x] **NEW-25c:** ANALYZE get_rest_of_season_projection() ✅ RESOLVED
  - **Decision:** NO CHANGES - already delegates correctly
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 3"

---

## New Methods (Deferred - 3 items)

- [x] **NEW-25d:** DECIDE if we need get_weekly_actuals() ✅ RESOLVED
  - **Decision:** DEFER to future features (not needed for minimum viable migration)
- [x] **NEW-25e:** DECIDE if we need get_single_weekly_actual() ✅ RESOLVED
  - **Decision:** DEFER to future features (not needed for minimum viable migration)
- [x] **NEW-25f:** DECIDE if we need get_rest_of_season_actual() ✅ RESOLVED
  - **Decision:** DEFER to future features (not needed for minimum viable migration)

---

## Call Site Updates (2 items)

- [x] **NEW-23:** Replace direct field access with method calls or array indexing ✅ VERIFIED
  - **Finding:** No direct field access found in league_helper/! (Verified via grep)
  - **Exception:** ConfigManager.py uses dynamic getattr (covered by NEW-22m)
  - **Rationale:** All user-facing code uses methods - confirms design is good
- [x] **NEW-24:** Update any loops building weekly lists ✅ VERIFIED
  - **Finding:** get_weekly_projections() returns full list (FantasyPlayer.py:347-351)
  - **Verified:** No other code builds weekly lists manually
  - **Rationale:** Centralized in one method - good encapsulation

---

## Testing (5 items)

**Note:** Testing items deferred to implementation phase - no verification needed during deep dive

- [ ] **NEW-26:** Unit test for `get_weekly_projections()` with hybrid logic **(Testing - defer to implementation)**
  - Test with current_week = 1 (all projected)
  - Test with current_week = 10 (mix of actual and projected)
  - Test with current_week = 18 (all actual)
  - Verify correct cutoff point
- [ ] **NEW-27:** Unit test for `get_single_weekly_projection(week)` boundary cases **(Testing - defer to implementation)**
  - Week 1 (first week)
  - Week 17 (last week)
  - Week 0 (invalid - should error)
  - Week 18 (invalid - should error)
  - Verify hybrid behavior based on current_week
- [ ] **NEW-28:** Unit test for array loading **(Testing - defer to implementation)**
  - Test projected_points and actual_points arrays load correctly
  - Test from_json() loads both arrays
  - Test arrays have correct length (17 elements)
- [ ] **NEW-29:** Integration test for modes using weekly data **(Testing - defer to implementation)**
  - StarterHelperMode (lineup recommendations)
  - SaveCalculatedPointsMode (saving weekly points)
  - PlayerManager (max weekly projection)
  - Verify all work with new array-based methods
- [ ] **NEW-30:** Test from_json() and to_json() with arrays **(Testing - defer to implementation)**
  - Load projected_points and actual_points from JSON
  - Verify arrays stored correctly in FantasyPlayer
  - Save back to JSON (Sub-feature 4)
  - Verify arrays preserved

---

## Success Criteria

✅ **All week_N_points fields removed from FantasyPlayer**
✅ **All 12 identified locations updated**
✅ **get_weekly_projections() implements hybrid logic**
✅ **All method calls still work (no direct field access)**
✅ **All unit tests passing (100%)**
✅ **Integration tests with StarterHelper and other modes passing**

---

## Dependencies

**Prerequisites:**
- Sub-feature 1 complete (projected_points/actual_points fields exist and load from JSON)

**Blocks:**
- Sub-feature 4 (File Update Strategy - may need to handle week_N_points in writes)
- Sub-feature 5 (ProjectedPointsManager - uses projected_points arrays)
- Sub-feature 6 (TeamDataManager - uses actual_points arrays for D/ST)

---

## Key Findings

**✅ GOOD NEWS:**
- All user-facing code uses METHODS, not direct field access!
- Only FantasyPlayer needs core changes
- Method calls should work automatically after implementation
- Only 4 call sites to verify (not modify)

**⚠️ BREAKING CHANGES:**
- Removing week_N_points fields causes compilation errors (intentional per Decision 10)
- Errors will guide any missed spots during testing
- Clean break approach - no backward compatibility

---

## Notes

- See `WEEKLY_DATA_ANALYSIS.md` for complete method-by-method implementation details
- Hybrid logic matches OLD week_N_points behavior (actual for past, projected for future)
- No new methods added - deferred actual_points accessors to future features
- Sub-feature 5 and 6 depend on these arrays being available
