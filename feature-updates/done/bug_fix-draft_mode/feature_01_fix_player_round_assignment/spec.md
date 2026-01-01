# Feature Specification: Fix Player-to-Round Assignment Logic

**Part of Epic:** bug_fix-draft_mode
**Feature Number:** 1
**Created:** 2025-12-31
**Last Updated:** 2025-12-31

---

## Feature Overview

**What:** Fix the FLEX position matching logic in `AddToRosterModeManager._match_players_to_rounds()` so all rostered players (especially RB/WR) are correctly assigned to their appropriate draft rounds.

**Why:** Currently, the bug causes RB/WR players to only match FLEX-ideal rounds and not RB-ideal or WR-ideal rounds. This leaves many rounds incorrectly displayed as [EMPTY SLOT] even when the roster is full, making the draft assistant unusable.

**Who:** Users of the Add to Roster (draft assistant) mode who need to see their current roster organized by draft rounds to make informed drafting decisions.

---

## Problem Statement

**Current Buggy Behavior:**
- RB/WR players are converted to "FLEX" position before matching (line 426)
- RB/WR players can ONLY match rounds where ideal position is "FLEX"
- RB/WR players CANNOT match rounds where ideal position is "RB" or "WR"
- Result: Many rounds show [EMPTY SLOT] even though players exist

**Example from User's Data:**
```
Round  1 (Ideal: WR  ): [EMPTY SLOT]  ← Should have a WR here
Round  2 (Ideal: WR  ): [EMPTY SLOT]  ← Should have a WR here
Round  4 (Ideal: WR  ): [EMPTY SLOT]  ← Should have a WR here
Round  7 (Ideal: RB  ): [EMPTY SLOT]  ← Should have an RB here
Round  9 (Ideal: RB  ): [EMPTY SLOT]  ← Should have an RB here
Round 10 (Ideal: RB  ): [EMPTY SLOT]  ← Should have an RB here
Round 11 (Ideal: WR  ): [EMPTY SLOT]  ← Should have a WR here
Round 12 (Ideal: RB  ): [EMPTY SLOT]  ← Should have an RB here
Round 15 (Ideal: FLEX): Ashton Jeanty (RB) - 259.8 pts  ← RB assigned correctly
```

User has 15 players rostered, but only a few show up because most RB/WR can't match their ideal rounds.

---

## Expected Behavior After Fix

**Correct Matching Logic:**
- WR players should match rounds where ideal is "WR" OR "FLEX"
- RB players should match rounds where ideal is "RB" OR "FLEX"
- QB, TE, K, DST should only match their exact position (no FLEX)
- FLEX-ideal rounds should accept any FLEX-eligible player (RB/WR per config)

**Result:**
- All 15 rostered players correctly assigned to their optimal rounds
- No [EMPTY SLOT] entries when roster is full
- Clear visibility of draft strategy and roster composition

---

## Files Likely Affected

**Primary Fix:**
- `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
  - Method: `_match_players_to_rounds()` (lines 372-440)
  - Specific line: 426 (buggy conditional)

**Test Validation:**
- `tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py`
  - Validate existing tests still pass
  - Add regression tests if needed

**Related Methods (likely unchanged):**
- `ConfigManager.get_position_with_flex()` (league_helper/util/ConfigManager.py:313)
- `ConfigManager.get_ideal_draft_position()` (league_helper/util/ConfigManager.py:683)
- `AddToRosterModeManager._get_current_round()` (depends on _match_players_to_rounds)

---

## Initial Scope (High-Level)

**In Scope:**
- Fix the position matching conditional logic (line 426)
- Allow RB/WR to match both their native position AND FLEX
- Maintain existing behavior for non-FLEX positions (QB, TE, K, DST)
- Validate fix with existing unit tests
- Test with real roster data from bug report

**Out of Scope:**
- Changing FLEX_ELIGIBLE_POSITIONS configuration
- Modifying DRAFT_ORDER structure
- Changing ConfigManager helper methods
- UI/display changes beyond fixing the assignment logic
- Changes to other modes (this is Add to Roster mode only)

---

## Dependencies

**Prerequisites:** None (standalone fix)

**Blocks:** None

**Related Config:**
- `DRAFT_ORDER` - Defines ideal position for each round (15 rounds)
- `FLEX_ELIGIBLE_POSITIONS` - Defines which positions can fill FLEX slots (currently: RB, WR)
- `MAX_POSITIONS` - Roster limits per position

---

## Technical Approach

**Current Buggy Code (line 426 in AddToRosterModeManager.py):**
```python
if self.config.get_position_with_flex(player.position) == ideal_position:
    # BUG: get_position_with_flex() converts RB→"FLEX" and WR→"FLEX"
    # So RB/WR can ONLY match "FLEX" ideal, not "RB" or "WR" ideal
```

**Why This is Wrong:**

`ConfigManager.get_position_with_flex()` (line 313) converts:
- RB → "FLEX"
- WR → "FLEX"
- QB → "QB" (unchanged)
- TE → "TE" (unchanged)
- K → "K" (unchanged)
- DST → "DST" (unchanged)

When matching round 1 (ideal = "WR"):
- Player position: "WR"
- `get_position_with_flex("WR")` returns "FLEX"
- Comparison: "FLEX" == "WR" → **False** (no match!)

When matching round 5 (ideal = "FLEX"):
- Player position: "WR"
- `get_position_with_flex("WR")` returns "FLEX"
- Comparison: "FLEX" == "FLEX" → **True** (match!)

**Result:** WR can only match FLEX-ideal rounds, not WR-ideal rounds.

---

### Proposed Fix - Two Options

**Option A: Inline Logic (simpler)**

Replace line 426 with:
```python
# Check if player position matches ideal for this round
if player.position in self.config.flex_eligible_positions:
    # FLEX-eligible positions (RB/WR) can match both native AND FLEX
    position_matches = (player.position == ideal_position or
                       ideal_position == "FLEX")
else:
    # Non-FLEX positions (QB/TE/K/DST) must match exactly
    position_matches = (player.position == ideal_position)

if position_matches:
    # Found a match! Assign player to this round
    round_assignments[round_num] = player
    available_players.remove(player)
    break
```

**Pros:** Simple, no new methods
**Cons:** Slightly verbose inline logic

---

**Option B: Helper Method (cleaner)**

Add new method (after `_match_players_to_rounds()` around line 441):
```python
def _position_matches_ideal(self, player_position: str, ideal_position: str) -> bool:
    """
    Check if a player's position can fill a round with the given ideal position.

    For FLEX-eligible positions (defined in config.flex_eligible_positions,
    typically RB and WR), players can match both their native position rounds
    AND FLEX-ideal rounds.

    For non-FLEX positions (QB, TE, K, DST), players must match exactly.

    Args:
        player_position: Player's actual position ("RB", "WR", "QB", etc.)
        ideal_position: Ideal position for the round from DRAFT_ORDER

    Returns:
        True if player can fill this round, False otherwise

    Examples:
        >>> self._position_matches_ideal("RB", "RB")     # True (native match)
        >>> self._position_matches_ideal("RB", "FLEX")   # True (FLEX-eligible)
        >>> self._position_matches_ideal("RB", "WR")     # False (different position)
        >>> self._position_matches_ideal("QB", "QB")     # True (exact match)
        >>> self._position_matches_ideal("QB", "FLEX")   # False (QB not FLEX-eligible)
    """
    if player_position in self.config.flex_eligible_positions:
        # FLEX-eligible: match native position OR FLEX
        return player_position == ideal_position or ideal_position == "FLEX"
    else:
        # Non-FLEX: exact match only
        return player_position == ideal_position
```

Replace line 426 with:
```python
if self._position_matches_ideal(player.position, ideal_position):
    # Found a match! Assign player to this round
    round_assignments[round_num] = player
    available_players.remove(player)
    break
```

**Pros:** Clean, testable in isolation, self-documenting
**Cons:** Adds one method (~20 lines)

---

**DECISION:** ✅ **Option B (Helper Method)** - User approved 2025-12-31

**Implementation:**
- Add new `_position_matches_ideal()` helper method after line 440
- Replace line 426 with call to helper method
- Total changes: ~21 lines (20 new method + 1 line replacement)

---

## Success Criteria

**Feature is successful when:**
1. All 15 rostered players are correctly assigned to draft rounds
2. WR players match both WR-ideal rounds AND FLEX-ideal rounds
3. RB players match both RB-ideal rounds AND FLEX-ideal rounds
4. QB, TE, K, DST only match their specific ideal rounds
5. Existing unit tests pass (100% pass rate)
6. User's actual roster data (from bug report) displays correctly with no [EMPTY SLOT] errors

---

## Edge Cases

**Edge Case 1: All FLEX Rounds Already Filled**
- **Scenario:** Roster has 10 RBs + 5 WRs, but DRAFT_ORDER only has 3 FLEX-ideal rounds
- **Current Bug:** Only 3 players match (to FLEX rounds), rest show [EMPTY SLOT]
- **Expected After Fix:** First N players match to RB/WR-ideal rounds, next 3 to FLEX rounds
- **Handling:** Greedy algorithm assigns sequentially, remainder can't match (expected)

**Edge Case 2: No FLEX Rounds in DRAFT_ORDER**
- **Scenario:** DRAFT_ORDER has specific positions only (no "FLEX" ideal rounds)
- **Current Bug:** RB/WR can't match ANY rounds
- **Expected After Fix:** RB/WR match to their native position rounds only
- **Handling:** Match logic handles both native and FLEX, works correctly

**Edge Case 3: Roster Fewer Players Than Rounds (Partial Roster)**
- **Scenario:** 5 players rostered, 15 rounds in DRAFT_ORDER
- **Current Bug:** Some players don't match (RB/WR to native rounds)
- **Expected After Fix:** All 5 players matched, 10 rounds empty
- **Handling:** Should work correctly (more rounds than players)

**Edge Case 4: Mixed Position Roster (All Position Types)**
- **Scenario:** 2 QB, 4 RB, 4 WR, 2 TE, 1 K, 1 DST, 1 unmatched
- **Current Bug:** QB/TE/K/DST match correctly, but RB/WR only match FLEX rounds
- **Expected After Fix:** All positions match to their ideal rounds
- **Handling:** This is the main fix scenario

**Edge Case 5: FLEX_ELIGIBLE_POSITIONS Includes Uncommon Positions**
- **Scenario:** League allows TE or DST in FLEX (config: `["RB", "WR", "TE"]`)
- **Current Bug:** TE might also fail to match native rounds
- **Expected After Fix:** All FLEX-eligible positions match both native + FLEX
- **Handling:** Fix uses `config.flex_eligible_positions`, handles any positions

---

## Testing Strategy

### Unit Tests (New Tests Needed)

**Test 1: RB Matches RB-Ideal Round**
```python
def test_rb_matches_native_rb_round(add_to_roster_manager, mock_player_manager):
    """Test RB player can match to RB-ideal round (not just FLEX)"""
    # Setup: RB player, DRAFT_ORDER has round with RB as PRIMARY
    rb_player = FantasyPlayer(position="RB", ...)
    mock_player_manager.team.roster = [rb_player]

    result = add_to_roster_manager._match_players_to_rounds()

    # Assert: RB matched to an RB-ideal round (e.g., round 7)
    assert 7 in result  # Round 7 is RB-ideal in user's DRAFT_ORDER
    assert result[7] == rb_player
```

**Test 2: WR Matches WR-Ideal Round**
```python
def test_wr_matches_native_wr_round(add_to_roster_manager, mock_player_manager):
    """Test WR player can match to WR-ideal round (not just FLEX)"""
    # Similar to Test 1, but with WR
    wr_player = FantasyPlayer(position="WR", ...)
    mock_player_manager.team.roster = [wr_player]

    result = add_to_roster_manager._match_players_to_rounds()

    # Assert: WR matched to a WR-ideal round (e.g., round 1)
    assert 1 in result
    assert result[1] == wr_player
```

**Test 3: RB/WR Still Match FLEX Rounds**
```python
def test_rb_wr_still_match_flex_rounds(add_to_roster_manager, mock_player_manager):
    """Test RB/WR can still match to FLEX-ideal rounds"""
    # Setup: Multiple RBs, some native rounds filled, should use FLEX
    # Assert: RB matched to FLEX-ideal round when native rounds full
```

**Test 4: QB/TE/K/DST Still Exact Match Only**
```python
def test_non_flex_positions_exact_match_only(add_to_roster_manager, mock_player_manager):
    """Test QB/TE/K/DST unchanged (exact match only)"""
    # Setup: QB player, DRAFT_ORDER has QB and FLEX rounds
    qb_player = FantasyPlayer(position="QB", ...)

    result = add_to_roster_manager._match_players_to_rounds()

    # Assert: QB matched to QB-ideal round, NOT FLEX round
    # (even if FLEX round comes first)
```

**Test 5: Full Roster (15 Players) Regression Test**
```python
def test_full_roster_all_positions_match_correctly(add_to_roster_manager, mock_player_manager):
    """Test with 15 players (mix of all positions) - regression test for bug"""
    # Use actual roster data from bug report
    # 2 QB, 4 RB, 4 WR, 2 TE, 1 K, 1 DST, 1 FLEX
    roster = [...]  # 15 players

    result = add_to_roster_manager._match_players_to_rounds()

    # Assert: All 15 players matched (no [EMPTY SLOT])
    assert len(result) == 15
    # Assert: Specific players in specific rounds based on DRAFT_ORDER
```

**Test 6: Helper Method (if Option B chosen)**
```python
def test_position_matches_ideal_logic(add_to_roster_manager):
    """Test _position_matches_ideal() helper method directly"""
    # RB native match
    assert add_to_roster_manager._position_matches_ideal("RB", "RB") == True
    # RB FLEX match
    assert add_to_roster_manager._position_matches_ideal("RB", "FLEX") == True
    # RB vs WR (different positions)
    assert add_to_roster_manager._position_matches_ideal("RB", "WR") == False
    # QB exact match only
    assert add_to_roster_manager._position_matches_ideal("QB", "QB") == True
    assert add_to_roster_manager._position_matches_ideal("QB", "FLEX") == False
```

### Integration Tests

**Test 7: End-to-End with Actual League Data**
```python
def test_add_to_roster_mode_with_actual_user_data():
    """Integration test using actual roster data from bug report"""
    # Load user's league_config.json
    # Load user's roster (15 players from bug report)
    # Run Add to Roster mode
    # Verify display shows all 15 players in correct rounds
    # Verify _get_current_round() returns None (roster full)
```

### Regression Tests

**Existing Tests:** All 6 existing `_match_players_to_rounds()` tests should still pass
- `test_match_players_empty_roster()`
- `test_match_players_perfect_match()`
- `test_match_players_partial_match()`
- `test_match_players_multiple_same_position()`
- `test_match_players_uses_optimal_fit()`
- `test_match_players_to_rounds_with_duplicate_positions()`

---

## Implementation Checklist

**Production Code Changes:**
- [ ] Choose Option A (inline) or Option B (helper method) - See checklist.md Question 1
- [ ] Implement chosen option in AddToRosterModeManager.py
- [ ] Update line 426 with correct matching logic
- [ ] Add docstring (if Option B helper method)
- [ ] Verify no other callers of `get_position_with_flex()` affected

**Test Code Changes:**
- [ ] Add Test 1: RB matches RB-ideal round ✅ **REQUIRED (Comprehensive)**
- [ ] Add Test 2: WR matches WR-ideal round ✅ **REQUIRED (Comprehensive)**
- [ ] Add Test 3: RB/WR still match FLEX rounds ✅ **REQUIRED (Comprehensive)**
- [ ] Add Test 4: QB/TE/K/DST exact match only ✅ **REQUIRED (Comprehensive)**
- [ ] Add Test 5: Full roster (15 players) regression test ✅ **REQUIRED (Comprehensive)**
- [ ] Add Test 6: Helper method `_position_matches_ideal()` tests ✅ **REQUIRED (Option B chosen)**
- [ ] Add Test 7: Integration test with actual user data ✅ **REQUIRED (User approved)**
- [ ] Run all existing tests (verify 100% pass) ✅ **REQUIRED**

**Decision:** ✅ **Option C (Comprehensive)** - User approved 2025-12-31
**Rationale:** "This is one of the most key parts of this project and deserves the time and energy to validate the behavior"

**Validation:**
- [ ] Smoke test with user's actual roster data
- [ ] Verify all 15 players display correctly
- [ ] Verify _get_current_round() returns correct value
- [ ] Verify draft recommendations still work

---

## Open Questions

{To be resolved in checklist.md during Phase 3}

---

## Status

**Created:** Stage 1 (Epic Planning) - INITIAL VERSION
**Next:** Stage 2 (Feature Deep Dive) will flesh out this spec with:
- Detailed algorithm specification
- Specific test cases
- Edge case analysis
- Complete acceptance criteria
- Resolved open questions

---

## Notes

**Root Cause Analysis:**
The bug was introduced because `get_position_with_flex()` was designed to help with FLEX slot validation, but its use in the matching algorithm inadvertently prevented RB/WR from matching their native position rounds.

**Historical Context:**
- `get_position_with_flex()` returns "FLEX" for RB/WR, unchanged for QB/TE/K/DST
- This is correct for roster validation (checking if a player can fill a FLEX slot)
- But INCORRECT for round assignment (where we need to match both native AND FLEX)

**Fix Philosophy:**
The fix should be minimal and surgical - change only the matching logic, not the helper methods which may be used correctly elsewhere in the codebase.
