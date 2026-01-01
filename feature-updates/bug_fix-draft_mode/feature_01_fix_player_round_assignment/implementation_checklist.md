# Feature 01: Fix Player-to-Round Assignment - Implementation Checklist

**Purpose:** Track spec requirements during implementation (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified
- Update this file IN REAL-TIME (not batched at end)

**Last Updated:** 2025-12-31 18:00

---

## Requirements from spec.md

### Objective Requirements

- [x] **REQ-1:** Fix FLEX position matching logic in `_match_players_to_rounds()`
  - Spec: Feature Overview
  - TODO Task: Tasks 1-2
  - Implementation: Helper method + line 426 replacement
  - Verified: 2025-12-31 18:15 (Tasks 1-2 complete)

- [ ] **REQ-2:** All 15 rostered players correctly assigned to draft rounds
  - Spec: Expected Behavior After Fix
  - TODO Task: Tasks 1-2 (implementation), Task 7 (test validation)
  - Implementation: Fixed matching logic
  - Verified: {Check after Task 7 test passes}

- [ ] **REQ-3:** No [EMPTY SLOT] entries when roster is full
  - Spec: Expected Behavior After Fix
  - TODO Task: Task 7, Task 11 (smoke test)
  - Implementation: All players matched correctly
  - Verified: {Check after smoke test}

---

### Matching Logic Requirements

- [ ] **MATCH-1:** WR players match rounds where ideal is "WR" OR "FLEX"
  - Spec: Expected Behavior After Fix, line 48
  - TODO Task: Task 1 (helper method logic)
  - Implementation: `_position_matches_ideal()` helper method
  - Verified: {Check after Task 4 test passes}

- [ ] **MATCH-2:** RB players match rounds where ideal is "RB" OR "FLEX"
  - Spec: Expected Behavior After Fix, line 49
  - TODO Task: Task 1 (helper method logic)
  - Implementation: `_position_matches_ideal()` helper method
  - Verified: {Check after Task 3 test passes}

- [ ] **MATCH-3:** QB, TE, K, DST match only their exact position (no FLEX)
  - Spec: Expected Behavior After Fix, line 50
  - TODO Task: Task 1 (helper method logic)
  - Implementation: `_position_matches_ideal()` else branch
  - Verified: {Check after Task 6 test passes}

- [ ] **MATCH-4:** FLEX-ideal rounds accept any FLEX-eligible player (RB/WR per config)
  - Spec: Expected Behavior After Fix, line 51
  - TODO Task: Task 1 (helper method logic)
  - Implementation: `_position_matches_ideal()` if branch
  - Verified: {Check after Task 5 test passes}

---

### Technical Implementation Requirements

- [x] **IMPL-1:** Create helper method `_position_matches_ideal()`
  - Spec: Technical Approach - Option B, lines 173-204
  - TODO Task: Task 1
  - Implementation: AddToRosterModeManager.py line 442 (after _match_players_to_rounds)
  - Verified: 2025-12-31 18:15 (Task 1 complete)

- [x] **IMPL-2:** Helper method signature: `(self, player_position: str, ideal_position: str) -> bool`
  - Spec: Technical Approach - Option B, line 174
  - TODO Task: Task 1
  - Implementation: Method definition line 442
  - Verified: 2025-12-31 18:15 (matches spec exactly)

- [x] **IMPL-3:** Helper method checks if position in `config.flex_eligible_positions`
  - Spec: Technical Approach - Option B, line 198
  - TODO Task: Task 1
  - Implementation: If condition line 466
  - Verified: 2025-12-31 18:15 (uses config, not hardcoded)

- [x] **IMPL-4:** FLEX-eligible positions match native OR FLEX
  - Spec: Technical Approach - Option B, lines 199-200
  - TODO Task: Task 1
  - Implementation: Return statement line 468 with OR logic
  - Verified: 2025-12-31 18:15 (matches spec exactly)

- [x] **IMPL-5:** Non-FLEX positions match exactly
  - Spec: Technical Approach - Option B, lines 202-203
  - TODO Task: Task 1
  - Implementation: Else branch return statement line 471
  - Verified: 2025-12-31 18:15 (exact match only)

- [x] **IMPL-6:** Add comprehensive docstring to helper method
  - Spec: Technical Approach - Option B, lines 175-197
  - TODO Task: Task 1
  - Implementation: Docstring lines 443-465 with Args, Returns, Examples
  - Verified: 2025-12-31 18:15 (comprehensive docstring)

- [x] **IMPL-7:** Replace line 426 with helper method call
  - Spec: Technical Approach - Option B, lines 207-213
  - TODO Task: Task 2
  - Implementation: `if self._position_matches_ideal(player.position, ideal_position):` line 426
  - Verified: 2025-12-31 18:15 (Task 2 complete)

---

### Success Criteria Requirements

- [ ] **SUCCESS-1:** All 15 rostered players correctly assigned to draft rounds
  - Spec: Success Criteria, criterion 1
  - TODO Task: Task 7 (test), Task 9 (integration), Task 11 (smoke test)
  - Implementation: Complete fix (Tasks 1-2)
  - Verified: {Check after all tests pass}

- [ ] **SUCCESS-2:** WR players match both WR-ideal rounds AND FLEX-ideal rounds
  - Spec: Success Criteria, criterion 2
  - TODO Task: Task 4 (test)
  - Implementation: Helper method logic
  - Verified: {Check after Task 4 test passes}

- [ ] **SUCCESS-3:** RB players match both RB-ideal rounds AND FLEX-ideal rounds
  - Spec: Success Criteria, criterion 3
  - TODO Task: Task 3 (test)
  - Implementation: Helper method logic
  - Verified: {Check after Task 3 test passes}

- [ ] **SUCCESS-4:** QB, TE, K, DST only match their specific ideal rounds
  - Spec: Success Criteria, criterion 4
  - TODO Task: Task 6 (test)
  - Implementation: Helper method else branch
  - Verified: {Check after Task 6 test passes}

- [ ] **SUCCESS-5:** Existing unit tests pass (100% pass rate)
  - Spec: Success Criteria, criterion 5
  - TODO Task: Task 10
  - Implementation: No breaking changes
  - Verified: {Check after Task 10 complete}

- [ ] **SUCCESS-6:** User's actual roster data displays correctly with no [EMPTY SLOT] errors
  - Spec: Success Criteria, criterion 6
  - TODO Task: Task 9 (integration test), Task 11 (smoke test)
  - Implementation: Complete fix
  - Verified: {Check after smoke test passes}

---

### Edge Case Requirements

- [ ] **EDGE-1:** All FLEX rounds already filled scenario handled
  - Spec: Edge Cases, case 1
  - TODO Task: Implicitly handled by greedy algorithm (no specific test)
  - Implementation: No special handling needed
  - Verified: {Check greedy algorithm unchanged}

- [ ] **EDGE-2:** No FLEX rounds in DRAFT_ORDER scenario handled
  - Spec: Edge Cases, case 2
  - TODO Task: Task 3-4 tests validate this
  - Implementation: Helper method returns False for FLEX when no FLEX exists
  - Verified: {Check after Tasks 3-4 tests pass}

- [ ] **EDGE-3:** Partial roster (fewer players than rounds) handled
  - Spec: Edge Cases, case 3
  - TODO Task: Existing tests (no changes needed)
  - Implementation: Existing algorithm handles correctly
  - Verified: {Check existing tests still pass}

- [ ] **EDGE-4:** Mixed position roster handled correctly
  - Spec: Edge Cases, case 4
  - TODO Task: Task 7 (full roster test)
  - Implementation: Main fix scenario
  - Verified: {Check after Task 7 test passes}

- [ ] **EDGE-5:** FLEX_ELIGIBLE_POSITIONS with uncommon positions (e.g., TE) handled
  - Spec: Edge Cases, case 5
  - TODO Task: Helper method uses config (not hardcoded)
  - Implementation: Uses `self.config.flex_eligible_positions`
  - Verified: {Check after Task 8 test passes (all logic paths)}

---

### Testing Requirements

- [ ] **TEST-1:** Test RB matches RB-ideal round
  - Spec: Testing Strategy - Test 1
  - TODO Task: Task 3
  - Implementation: `test_rb_matches_native_rb_round()`
  - Verified: {Check after test created and passes}

- [ ] **TEST-2:** Test WR matches WR-ideal round
  - Spec: Testing Strategy - Test 2
  - TODO Task: Task 4
  - Implementation: `test_wr_matches_native_wr_round()`
  - Verified: {Check after test created and passes}

- [ ] **TEST-3:** Test RB/WR still match FLEX rounds
  - Spec: Testing Strategy - Test 3
  - TODO Task: Task 5
  - Implementation: `test_rb_wr_still_match_flex_rounds()`
  - Verified: {Check after test created and passes}

- [ ] **TEST-4:** Test QB/TE/K/DST exact match only
  - Spec: Testing Strategy - Test 4
  - TODO Task: Task 6
  - Implementation: `test_non_flex_positions_exact_match_only()`
  - Verified: {Check after test created and passes}

- [ ] **TEST-5:** Test full roster (15 players)
  - Spec: Testing Strategy - Test 5
  - TODO Task: Task 7
  - Implementation: `test_full_roster_all_positions_match_correctly()`
  - Verified: {Check after test created and passes}

- [ ] **TEST-6:** Test helper method directly
  - Spec: Testing Strategy - Test 6
  - TODO Task: Task 8
  - Implementation: `test_position_matches_ideal_all_paths()`
  - Verified: {Check after test created and passes}

- [ ] **TEST-7:** Integration test with actual user data
  - Spec: Testing Strategy - Test 7
  - TODO Task: Task 9
  - Implementation: `test_integration_with_actual_user_roster()`
  - Verified: {Check after test created and passes}

- [ ] **TEST-8:** All existing tests still pass
  - Spec: Testing Strategy - Regression Tests
  - TODO Task: Task 10
  - Implementation: Run pytest on test file
  - Verified: {Check after all tests pass}

---

### Validation Requirements

- [ ] **VALID-1:** Smoke test with user's actual roster data
  - Spec: Implementation Checklist - Validation
  - TODO Task: Task 11
  - Implementation: Manual test in Add to Roster mode
  - Verified: {Check after smoke test complete}

- [ ] **VALID-2:** Verify all 15 players display correctly
  - Spec: Implementation Checklist - Validation
  - TODO Task: Task 11
  - Implementation: Visual verification of display
  - Verified: {Check after smoke test complete}

- [ ] **VALID-3:** Verify _get_current_round() returns correct value
  - Spec: Implementation Checklist - Validation
  - TODO Task: Task 12
  - Implementation: Verify method behavior unchanged
  - Verified: {Check after Task 12 complete}

- [ ] **VALID-4:** Verify draft recommendations still work
  - Spec: Implementation Checklist - Validation
  - TODO Task: Task 15
  - Implementation: Manual test of recommendations
  - Verified: {Check after Task 15 complete}

- [ ] **VALID-5:** Verify no other callers of `get_position_with_flex()` affected
  - Spec: Implementation Checklist - Production Code Changes
  - TODO Task: Task 14
  - Implementation: Grep search and verification
  - Verified: {Check after Task 14 complete}

- [ ] **VALID-6:** Verify `_display_roster_by_draft_rounds()` still works
  - Spec: Files Likely Affected - Related Methods
  - TODO Task: Task 13
  - Implementation: Verify method behavior unchanged
  - Verified: {Check after Task 13 complete}

---

## Summary

**Total Requirements:** 42
**Implemented:** 8
**Remaining:** 34

**Categories:**
- Objective: 3
- Matching Logic: 4
- Technical Implementation: 7
- Success Criteria: 6
- Edge Cases: 5
- Testing: 8
- Validation: 6
- **Total:** 39 unique requirements

**Last Updated:** 2025-12-31 18:00

---

*End of implementation_checklist.md - Update in REAL-TIME as you implement*
