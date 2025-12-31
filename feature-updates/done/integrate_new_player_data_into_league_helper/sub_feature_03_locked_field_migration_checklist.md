# Sub-Feature 3: Locked Field Migration - Checklist

> **IMPORTANT**: When marking items as resolved, also update `sub_feature_03_locked_field_migration_spec.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** 21
**Completed:** 17 (3 analysis + 14 implementation verified)
**Remaining:** 4 (5 testing items - deferred to implementation)

---

## Analysis & Strategy (3 items - RESOLVED)

- [x] **NEW-49:** locked field migration strategy decision ✅ RESOLVED
  - **Decision:** Change to boolean AND standardize all comparisons to use is_locked()
  - **Rationale:** More Pythonic, matches JSON format, encapsulates logic
  - **Impact:** 14 comparisons + 2 assignments = 16 total locations
- [x] **NEW-50:** is_locked() method usage analysis ✅ RESOLVED
  - **Finding:** FantasyPlayer has is_locked() method (line 320)
  - **Decision:** Standardize ALL code to use is_locked() instead of direct field access
- [x] **NEW-51:** is_available() method usage analysis ✅ RESOLVED
  - **Finding:** FantasyPlayer has is_available() method (checks drafted AND locked, line 308)
  - **Usage:** FantasyTeam.py:166 uses it
  - **Action:** Will be updated to use boolean locked internally

---

## FantasyPlayer.py Core Changes (4 items)

- [x] **NEW-54:** Change locked field definition ✅ VERIFIED
  - **Current:** `locked: int = 0` at line 96
  - **Update to:** `locked: bool = False`
  - **File:** utils/FantasyPlayer.py:96
- [x] **NEW-55:** Update is_locked() method ✅ VERIFIED
  - **Current:** `return self.locked == 1` at line 320
  - **Update to:** `return self.locked`
  - **File:** utils/FantasyPlayer.py:320
- [x] **NEW-56:** Update is_available() method ✅ VERIFIED
  - **Current:** `self.locked == 0` at line 308
  - **Update to:** `not self.locked`
  - **File:** utils/FantasyPlayer.py:308
- [x] **NEW-57:** Update __str__ method ✅ VERIFIED
  - **Current:** `self.locked == 1` at line 397
  - **Update to:** `self.is_locked()` (use method, not direct field access)
  - **File:** utils/FantasyPlayer.py:397

---

## JSON Loading/Saving (2 items)

- [x] **NEW-58:** Update from_json() to load locked boolean directly ✅ VERIFIED
  - **Current:** from_json() will be created in Sub-feature 1 with temporary int conversion
  - **Required change:** Load as boolean directly: `locked = data.get('locked', False)`
  - **File:** utils/FantasyPlayer.py from_json() method (will be created in Sub-feature 1)
  - **Note:** No conversion needed - JSON already has boolean, just load directly
- [x] **NEW-59:** Update to_json() to save locked boolean directly ✅ DEFERRED
  - **Decision:** DEFER to Sub-feature 4 (File Update Strategy creates to_json())
  - **Action:** Sub-feature 4 will write locked as boolean directly
  - **Note:** No conversion needed

---

## Standardize Comparisons to use is_locked() (8 items)

- [x] **NEW-60:** league_helper/util/PlayerManager.py:552 ✅ VERIFIED
  - **Current:** `if p.score < lowest_scores[p.position] and p.locked == 0:`
  - **Update to:** `if p.score < lowest_scores[p.position] and not p.is_locked():`
- [x] **NEW-61:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:338 ✅ VERIFIED
  - **Current:** `locked_players = [p for p in self.player_manager.players if p.locked == 1]`
  - **Update to:** `locked_players = [p for p in self.player_manager.players if p.is_locked()]`
- [x] **NEW-62:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:394 ✅ VERIFIED
  - **Current:** `was_locked = selected_player.locked == 1`
  - **Update to:** `was_locked = selected_player.is_locked()`
- [x] **NEW-63:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:409 ✅ VERIFIED
  - **Current:** `if selected_player.locked == 1:`
  - **Update to:** `if selected_player.is_locked():`
- [x] **NEW-64:** league_helper/trade_simulator_mode/trade_analyzer.py:639 ✅ VERIFIED
  - **Current:** `my_locked_original = [p for p in my_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]`
  - **Update to:** `my_locked_original = [p for p in my_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]`
- [x] **NEW-65:** league_helper/trade_simulator_mode/trade_analyzer.py:643 ✅ VERIFIED
  - **Current:** `their_locked_original = [p for p in their_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]`
  - **Update to:** `their_locked_original = [p for p in their_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]`
- [x] **NEW-66:** league_helper/trade_simulator_mode/trade_analyzer.py:820 ✅ VERIFIED
  - **Current:** `my_locked = [p for p in my_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]`
  - **Update to:** `my_locked = [p for p in my_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]`
- [x] **NEW-67:** league_helper/trade_simulator_mode/trade_analyzer.py:824 ✅ VERIFIED
  - **Current:** `their_locked = [p for p in their_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]`
  - **Update to:** `their_locked = [p for p in their_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]`

---

## Assignment Updates to use True/False (2 items)

- [x] **NEW-68:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py:401 ✅ VERIFIED
  - **Current:** `selected_player.locked = 0 if was_locked else 1`
  - **Update to:** `selected_player.locked = False if was_locked else True`
  - **Note:** This toggles lock status (unlock if locked, lock if unlocked)
- [x] **NEW-69:** league_helper/trade_simulator_mode/trade_analyzer.py:181 ✅ VERIFIED
  - **Current:** `p_copy.locked = 0` (with comment: "Unlock for testing - we're just counting violations, not enforcing lock status")
  - **Update to:** `p_copy.locked = False`

---

## Testing (5 items)

**Note:** Testing items deferred to implementation phase - no verification needed during deep dive

- [ ] **NEW-70:** Test is_locked() method with boolean field **(Testing - defer to implementation)**
  - Test with locked = True (returns True)
  - Test with locked = False (returns False)
  - Verify no regressions
- [ ] **NEW-71:** Test is_available() method with boolean locked **(Testing - defer to implementation)**
  - Test various combinations of drafted and locked
  - Verify logic still correct with boolean
- [ ] **NEW-72:** Test from_json() loads locked boolean correctly **(Testing - defer to implementation)**
  - Test with locked: true in JSON
  - Test with locked: false in JSON
  - Test with missing locked field (defaults to False)
- [ ] **NEW-73:** Test to_json() saves locked boolean correctly **(Testing - defer to implementation)**
  - **Deferred to Sub-feature 4** (File Update Strategy)
  - Verify locked written as boolean, not int
- [ ] **NEW-74:** Test all modes using locked field **(Testing - defer to implementation)**
  - ModifyPlayerDataMode (lock/unlock players)
  - trade_analyzer (locked player handling)
  - PlayerManager (locked filtering)
  - Verify all work with boolean field

---

## Success Criteria

✅ **locked field changed to bool in FantasyPlayer**
✅ **All 14 comparisons updated to use is_locked()**
✅ **All 2 assignments updated to use True/False**
✅ **from_json() loads boolean directly**
✅ **is_locked() and is_available() methods updated**
✅ **All unit tests passing (100%)**
✅ **Integration tests with ModifyPlayerDataMode and trade_analyzer passing**

---

## Dependencies

**Prerequisites:**
- Sub-feature 1 complete (from_json() exists for updating)

**Blocks:**
- Sub-feature 4 (File Update Strategy - needs to save locked as boolean)

---

## Impact Analysis

**Files Modified:** 4
- utils/FantasyPlayer.py (core field and methods)
- league_helper/util/PlayerManager.py (1 comparison)
- league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py (4 comparisons + 1 assignment)
- league_helper/trade_simulator_mode/trade_analyzer.py (4 comparisons + 1 assignment)

**Total Changes:** 18
- 1 field definition change
- 3 method updates (is_locked, is_available, __str__)
- 2 JSON loading/saving updates
- 8 comparison standardizations
- 2 assignment updates
- 2 method tests (is_locked, is_available)

---

## Notes

- More Pythonic: `if player.is_locked()` instead of `if player.locked == 1`
- Encapsulation: Using method hides internal representation
- Consistency: Matches JSON format (already boolean there)
- Future-proof: Can add logic to is_locked() if needed
