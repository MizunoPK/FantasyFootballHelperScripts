# Epic Smoke Test Plan: bug_fix-draft_mode

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: STAGE 5e (Updated after feature implementation)**
- Created: 2025-12-31 (Stage 1)
- Last Updated: 2025-12-31 (Stage 5e - after feature_01 implementation)
- Based on: ACTUAL implementation of feature_01_fix_player_round_assignment
- Quality: VERIFIED - Tests validated against actual code, not assumptions
- Next Update: Stage 6 (will execute this evolved plan during Epic Final QC)

**Update History:**
- Stage 1: Initial placeholder (assumptions only)
- Stage 4: **MAJOR UPDATE** - Added specific tests, integration points, measurable criteria
- Stage 5e: **IMPLEMENTATION VERIFICATION** - Confirmed Stage 4 plan matches actual implementation

---

## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: All Rostered Players Assigned to Rounds
✅ **MEASURABLE:** Run Add to Roster mode with 15-player roster (user's actual roster from bug report)
- **Verification:** Display roster by draft rounds
- **Expected:** All 15 players assigned to rounds (zero [EMPTY SLOT] entries that should have players)
- **Command:** `python run_league_helper.py` → mode 1 (Add to Roster) → display roster

### Criterion 2: RB Players Match RB-Ideal Rounds
✅ **MEASURABLE:** Verify RB players assigned to RB-ideal rounds (rounds 7, 9, 10, 12 per user config)
- **Verification:** Check round assignments for RB players
- **Expected:** RB players appear in RB-ideal rounds (not just FLEX rounds)
- **Test:** Unit test `test_rb_matches_rb_ideal_round()`

### Criterion 3: WR Players Match WR-Ideal Rounds
✅ **MEASURABLE:** Verify WR players assigned to WR-ideal rounds (rounds 1, 2, 4, 11 per user config)
- **Verification:** Check round assignments for WR players
- **Expected:** WR players appear in WR-ideal rounds (not just FLEX rounds)
- **Test:** Unit test `test_wr_matches_wr_ideal_round()`

### Criterion 4: RB/WR Still Match FLEX Rounds
✅ **MEASURABLE:** Verify RB/WR can still match FLEX-ideal rounds (rounds 5, 8, 15 per user config)
- **Verification:** RB/WR players assigned to FLEX rounds when appropriate
- **Expected:** FLEX rounds can still accept RB/WR players
- **Test:** Unit test `test_rb_wr_matches_flex_ideal_round()`

### Criterion 5: Non-FLEX Positions Unchanged
✅ **MEASURABLE:** Verify QB, TE, K, DST match only exact positions (behavior unchanged)
- **Verification:** QB only matches QB rounds, TE only matches TE rounds, etc.
- **Expected:** No regression in non-FLEX position matching
- **Test:** Unit test `test_non_flex_positions_exact_match_only()`

### Criterion 6: All Unit Tests Pass
✅ **MEASURABLE:** Run complete test suite for AddToRosterModeManager
- **Verification:** `python -m pytest tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py`
- **Expected:** 100% pass rate (existing + new tests)
- **Failure threshold:** Zero test failures allowed

### Criterion 7: Integration Test with User Data
✅ **MEASURABLE:** Integration test using user's actual 15-player roster from bug report
- **Verification:** Test fixture with user's exact roster data
- **Expected:** All 15 players correctly assigned to expected rounds
- **Test:** Unit test `test_integration_with_actual_user_roster()`

---

## Specific Test Scenarios

**These tests MUST be run for epic-level validation:**

### Test Scenario 1: Helper Method Logic Verification

**Purpose:** Verify `_position_matches_ideal()` helper method implements correct FLEX matching logic

**Steps:**
1. Run unit tests for helper method (Test 6 from spec.md)
2. Test all logic paths:
   - RB vs RB-ideal → True (native match)
   - RB vs FLEX-ideal → True (FLEX-eligible match)
   - RB vs WR-ideal → False (different positions)
   - WR vs WR-ideal → True (native match)
   - WR vs FLEX-ideal → True (FLEX-eligible match)
   - QB vs QB-ideal → True (exact match)
   - QB vs FLEX-ideal → False (QB not FLEX-eligible)

**Expected Results:**
✅ All helper method logic paths return correct values
✅ FLEX-eligible positions (RB, WR) match both native AND FLEX
✅ Non-FLEX positions (QB, TE, K, DST) match only exact position

**Failure Indicators:**
❌ RB/WR returns False for FLEX → FLEX matching broken
❌ QB returns True for FLEX → Non-FLEX positions incorrectly matching FLEX
❌ Any assertion failure → Logic error in helper method

**Command to verify:**
```bash
python -m pytest tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py::TestPositionMatchesIdeal -v
```

---

### Test Scenario 2: RB/WR Native Position Matching

**Purpose:** Verify RB and WR players can match their native position rounds (primary bug fix)

**Steps:**
1. Create test roster with RB and WR players
2. Create DRAFT_ORDER with RB-ideal and WR-ideal rounds (not just FLEX)
3. Run `_match_players_to_rounds()`
4. Verify RB players assigned to RB-ideal rounds
5. Verify WR players assigned to WR-ideal rounds

**Expected Results:**
✅ RB players match rounds where ideal_position = "RB"
✅ WR players match rounds where ideal_position = "WR"
✅ No [EMPTY SLOT] for rounds that should have RB/WR

**Failure Indicators:**
❌ RB only matches FLEX rounds → Bug NOT fixed
❌ WR only matches FLEX rounds → Bug NOT fixed
❌ RB/WR players unmatched → Regression in matching logic

**Command to verify:**
```bash
python -m pytest tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py::test_rb_matches_rb_ideal_round -v
python -m pytest tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py::test_wr_matches_wr_ideal_round -v
```

---

### Test Scenario 3: Full Roster Regression Test

**Purpose:** Verify complete 15-player roster is correctly assigned (no partial matches)

**Steps:**
1. Create test roster with 15 players (mix of all positions)
2. DRAFT_ORDER matches user's league config (15 rounds with varied positions)
3. Run `_match_players_to_rounds()`
4. Verify all 15 players assigned to appropriate rounds

**Expected Results:**
✅ All 15 players have round assignments
✅ Round assignments respect position matching rules
✅ No [EMPTY SLOT] errors for rounds that should have players
✅ Greedy algorithm assigns players to best-fit rounds

**Failure Indicators:**
❌ Fewer than 15 players matched → Some players not assigned
❌ [EMPTY SLOT] shown for round with available player → Matching logic failed
❌ Player in wrong round → Position matching error

**Command to verify:**
```bash
python -m pytest tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py::test_full_roster_15_players_all_assigned -v
```

---

### Test Scenario 4: Integration Test with Actual User Data

**Purpose:** Verify fix works with user's exact roster data from bug report

**Steps:**
1. Load test fixture with user's 15-player roster
2. Use user's league_config.json DRAFT_ORDER configuration
3. Run `_match_players_to_rounds()`
4. Verify assignments match expected rounds for each player

**Expected Results:**
✅ All 15 players from user's roster correctly assigned
✅ WR players in rounds 1, 2, 4, 11 (WR-ideal) or 5, 8, 15 (FLEX)
✅ RB players in rounds 7, 9, 10, 12 (RB-ideal) or 5, 8, 15 (FLEX)
✅ QB, TE, K, DST in their exact position rounds
✅ Zero [EMPTY SLOT] errors

**Failure Indicators:**
❌ Any player unmatched → Real-world scenario failed
❌ Player in unexpected round → Logic doesn't handle user's config
❌ [EMPTY SLOT] for user's data → Bug NOT fully fixed

**Command to verify:**
```bash
python -m pytest tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py::test_integration_with_actual_user_roster -v
```

---

### Test Scenario 5: End-to-End Workflow (Manual)

**Purpose:** Verify complete Add to Roster mode workflow with fix

**Steps:**
1. Start league helper: `python run_league_helper.py`
2. Select mode 1 (Add to Roster mode)
3. View roster display organized by draft rounds
4. Verify all players shown in correct rounds
5. Exit mode

**Expected Results:**
✅ Program starts without errors
✅ Add to Roster mode displays roster by rounds
✅ All 15 players visible in round assignments
✅ No [EMPTY SLOT] errors for rostered players
✅ Round display matches DRAFT_ORDER configuration
✅ Program exits cleanly

**Failure Indicators:**
❌ ImportError → Module integration issue
❌ [EMPTY SLOT] displayed → Fix not working in UI
❌ Crash during display → Runtime error
❌ Wrong round assignments → Logic error

**Command to verify:**
```bash
python run_league_helper.py
# Select: 1 (Add to Roster mode)
# View roster display
# Verify all players assigned
# Exit
```

---

### Test Scenario 6: Non-FLEX Position Regression Test

**Purpose:** Ensure QB, TE, K, DST matching unchanged (no regression)

**Steps:**
1. Create test roster with QB, TE, K, DST players
2. Create DRAFT_ORDER with exact position rounds (no FLEX)
3. Run `_match_players_to_rounds()`
4. Verify each position matches ONLY its exact round

**Expected Results:**
✅ QB matches only QB-ideal rounds
✅ TE matches only TE-ideal rounds
✅ K matches only K-ideal rounds
✅ DST matches only DST-ideal rounds
✅ None of these positions match FLEX rounds

**Failure Indicators:**
❌ QB matches FLEX round → Regression introduced
❌ TE matches non-TE round → Logic error
❌ Any non-FLEX position incorrectly matched → Broken logic

**Command to verify:**
```bash
python -m pytest tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py::test_non_flex_positions_exact_match_only -v
```

---

### Test Scenario 7: Existing Tests Still Pass

**Purpose:** Verify fix doesn't break existing functionality (regression prevention)

**Steps:**
1. Run all existing AddToRosterModeManager tests
2. Verify 100% pass rate on pre-existing tests
3. Confirm no tests were modified inappropriately

**Expected Results:**
✅ All existing tests pass (tests written before this epic)
✅ No test modifications needed (fix is additive, not breaking)
✅ 100% pass rate across entire test suite

**Failure Indicators:**
❌ Previously passing test now fails → Regression introduced
❌ Need to modify existing test → Breaking change (not allowed)

**Command to verify:**
```bash
python -m pytest tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py -v
```

---

## Integration Points Identified

**Single-feature epic, but internal integration points exist:**

### Integration Point 1: Helper Method → Main Method
**Components Involved:** `_position_matches_ideal()` (new) → `_match_players_to_rounds()` (existing, modified)
**Type:** Internal method call
**Flow:**
- `_match_players_to_rounds()` calls `_position_matches_ideal()` at line 426
- Helper method returns boolean (True/False for position match)
- Main method uses return value to assign player to round

**Test Need:** Verify helper method correctly called and return value properly handled

---

### Integration Point 2: ConfigManager Dependency
**Components Involved:** `_position_matches_ideal()` → `ConfigManager.flex_eligible_positions`
**Type:** Configuration read
**Flow:**
- Helper method reads `self.config.flex_eligible_positions`
- Configuration determines which positions are FLEX-eligible (typically ["RB", "WR"])
- Logic branches based on position being in this list

**Test Need:** Verify helper method uses correct config value (not hardcoded)

---

### Integration Point 3: Callers of _match_players_to_rounds()
**Components Involved:**
- `_get_current_round()` (line 442) → calls `_match_players_to_rounds()`
- `_display_roster_by_draft_rounds()` (line 314) → calls `_match_players_to_rounds()`

**Type:** Method dependency
**Flow:**
- Both methods depend on `_match_players_to_rounds()` return value
- Return value is Dict[int, FantasyPlayer] (round number → player)
- Callers use return value to find current round or display roster

**Test Need:** Verify callers work correctly with improved `_match_players_to_rounds()` (no changes to callers needed)

---

## High-Level Test Categories

**Agent will create additional scenarios for these categories during Stage 5e:**

### Category 1: Edge Case Testing
**What to test:** Unusual roster compositions and DRAFT_ORDER configurations
**Known edge cases:**
- All-RB roster (>5 RB players)
- All-WR roster (>5 WR players)
- No FLEX rounds in DRAFT_ORDER
- All FLEX rounds (no RB/WR-ideal rounds)
- Fewer players than rounds (partial roster)

**Stage 5e will add:** Specific edge case tests discovered during implementation

---

### Category 2: Error Handling
**What to test:** Graceful handling of invalid inputs
**Known error scenarios:**
- Empty roster (no players to match)
- Invalid DRAFT_ORDER (missing positions)
- Player with invalid position value
- FLEX_ELIGIBLE_POSITIONS empty or missing

**Stage 5e will add:** Error scenarios discovered during implementation

---

### Category 3: Performance
**What to test:** Algorithm efficiency with large rosters
**Known performance concerns:**
- 15-player roster (standard)
- Greedy algorithm O(n*m) complexity (n=players, m=rounds)

**Stage 5e will add:** Performance benchmarks after implementation (if needed)

---

### Category 4: Integration with Dependent Methods
**What to test:** `_get_current_round()` and `_display_roster_by_draft_rounds()` work correctly
**Known integration points:**
- `_get_current_round()` finds first empty round correctly
- `_display_roster_by_draft_rounds()` displays all players correctly

**Stage 5e will add:** Integration tests after implementation

---

## Update Log

| Date | Stage | What Changed | Why |
|------|-------|--------------|-----|
| 2025-12-31 | Stage 1 | Initial plan created | Epic planning - assumptions only |
| 2025-12-31 | Stage 4 | **MAJOR UPDATE** | Based on feature specs (Stages 2-3) |
| 2025-12-31 | Stage 5e (Feature 1) | **IMPLEMENTATION VERIFICATION** | Reviewed actual feature_01 implementation - confirmed Stage 4 plan matches reality |

**Stage 4 changes:**
- Added 7 specific test scenarios (was TBD):
  - Test 1: Helper method logic verification
  - Test 2: RB/WR native position matching
  - Test 3: Full roster regression test
  - Test 4: Integration test with user data
  - Test 5: E2E workflow (manual)
  - Test 6: Non-FLEX position regression
  - Test 7: Existing tests still pass
- Replaced vague success criteria with 7 measurable criteria:
  1. All rostered players assigned to rounds
  2. RB players match RB-ideal rounds
  3. WR players match WR-ideal rounds
  4. RB/WR still match FLEX rounds
  5. Non-FLEX positions unchanged
  6. All unit tests pass
  7. Integration test with user data passes
- Identified 3 integration points:
  - Helper method → main method call
  - ConfigManager dependency
  - Callers of _match_players_to_rounds()
- Added concrete commands and expected outputs for each test
- Documented failure indicators for each test scenario
- Expanded high-level categories with specific guidance

**Stage 5e changes (feature_01_fix_player_round_assignment):**
- **Reviewed ACTUAL implementation code:**
  - Verified `_position_matches_ideal()` helper at lines 442-471 (AddToRosterModeManager.py)
  - Confirmed helper uses `self.config.flex_eligible_positions` (ConfigManager integration)
  - Verified call at line 426 in `_match_players_to_rounds()`
  - Confirmed callers at lines 490 (_get_current_round) and 344 (_display_roster_by_draft_rounds)
  - Algorithm: Greedy optimal-fit, O(n*m) where n≤15 players, m=15 rounds
- **Findings:** Stage 4 assumptions were 100% accurate! No changes to test scenarios needed.
- **Smoke testing validation:** All 3 parts passed with ACTUAL DATA VALUES verified:
  - 15/15 players matched (not just "count > 0")
  - Real player names: Trevor Lawrence, C.J. Stroud, Ashton Jeanty, etc.
  - Valid positions and teams verified
  - Zero [EMPTY SLOT] errors confirmed
- **Integration test validation:** test_integration_with_actual_user_roster passed (15 players)
- **Unit test validation:** 46/46 tests passed (39 existing + 7 new comprehensive tests)
- **No new test scenarios needed:** Stage 4 plan already comprehensive and accurate
- **Quality confirmation:** Test plan ready for Stage 6 execution (no gaps identified)

**Current version is informed by:**
- Stage 1: Initial assumptions from epic request
- Stage 4: Feature spec and approved implementation plan
- **Stage 5e: ACTUAL implementation verification (feature_01 complete)** ← YOU ARE HERE

**Next update:** Stage 6 (Epic Final QC) - will execute this evolved plan

---

## Notes

**Single-Feature Epic:**
This is a focused bug fix epic with one feature. Test plan emphasizes:
- Comprehensive unit test coverage (7 tests per spec.md)
- Integration test with user's actual data
- Regression prevention (verify existing tests still pass)
- Manual E2E verification in Add to Roster mode

**User Emphasis:**
User specifically requested comprehensive testing (Option C) with rationale: "This is one of the most key parts of this project and deserves the time and energy to validate the behavior"

**Test Confidence:**
- 7 unit tests cover all scenarios from spec.md
- Integration test uses real-world data from bug report
- Manual E2E test confirms UI works correctly
- Existing tests verify no regressions

**Risk Mitigation:**
- Low-risk fix (single method + helper)
- Well-tested area (6 existing tests)
- Comprehensive new test coverage
- Clear success criteria

---

*End of epic_smoke_test_plan.md (Stage 4 version)*
