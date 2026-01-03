# Feature 02 Checklist: Accuracy Sim JSON Verification

**Status:** STAGE_2c - Refinement Phase Complete
**Last Updated:** 2026-01-03
**Total Questions:** 4 (4 resolved, 0 open)

---

## Open Questions

### Question 1: Verification Methodology ✅ RESOLVED

- [x] How should we verify the existing PlayerManager integration is correct?
  - **ANSWER: Option D (All of the above - comprehensive verification)**

**User's Answer (2026-01-03):**
"D"

**Implementation approach:**
- **Part 1: Code Review** - Line-by-line analysis of _create_player_manager(), _load_season_data(), _evaluate_config_weekly()
- **Part 2: Manual Testing** - Run Accuracy Simulation, inspect loaded data for weeks 1, 10, 17
- **Part 3: Automated Tests** - Verify/add comprehensive tests for PlayerManager integration

**Impacts on spec:**
- Requirement 6 Part 1: Code review confirmed as mandatory
- Requirement 6 Part 2: Manual testing confirmed as mandatory
- Requirement 6 Part 3: Automated tests confirmed (add if missing - per Question 2 answer)

---

### Question 2: Test Coverage Requirements ✅ RESOLVED

- [x] If JSON loading tests are missing from test_accuracy_simulation_integration.py, should we add them?
  - **ANSWER: Option A (Yes, add comprehensive tests for PlayerManager integration)**

**User's Answer (2026-01-03):**
"A"

**Implementation approach:**
- Inspect tests/integration/test_accuracy_simulation_integration.py to identify coverage gaps
- Add comprehensive tests for PlayerManager integration if missing:
  - Test `_create_player_manager()` creates temp directory with player_data/ subfolder
  - Test JSON files copied from week folder to temp/player_data/
  - Test PlayerManager loads JSON correctly from temporary directory
  - Test handling of all 6 position files (QB, RB, WR, TE, K, DST)
  - Test error handling for missing files (log warning, continue)
  - Test PlayerManager.players array populated correctly
  - Test week_N+1 logic (_load_season_data returns correct folders)
  - Test two-manager pattern (projected_mgr + actual_mgr)
  - Test array extraction from player.actual_points[week_num - 1]
- Ensure tests provide regression protection for delegation pattern

**Impacts on spec:**
- Requirement 6 Part 3: Confirmed comprehensive test coverage required
- Testing Strategy Part 3: Expand to include all PlayerManager integration tests

---

### Question 3: Week 17 Specific Testing ✅ RESOLVED

- [x] Should we add specific tests for the Week 17 edge case?
  - **ANSWER: Option A (Yes, dedicated test verifying week_17 projected + week_18 actual)**

**User's Answer (2026-01-03):**
"A"

**Implementation approach:**
- Add dedicated test for Week 17 edge case verification:
  - Test `_load_season_data(season_path, week_num=17)` returns (week_17 folder, week_18 folder)
  - Test `_evaluate_config_weekly()` for week 17 creates two managers:
    - projected_mgr from week_17 folder
    - actual_mgr from week_18 folder
  - Test array extraction: actual_mgr.players[X].actual_points[16] (week 17 = index 16)
  - Test week_18 folder exists and has real week 17 data
  - Test with real data structure (17-element arrays)
- This is in addition to broader week_N+1 pattern tests
- Provides explicit regression protection for user's specific concern

**Impacts on spec:**
- Requirement 6 Part 3: Add specific Week 17 test case to automated tests
- Testing Strategy Part 3: Add Week 17 dedicated test requirement

---

### Question 4: Edge Case Consistency with Win Rate Sim ✅ RESOLVED

- [x] Should Accuracy Sim's edge case handling match Win Rate Sim's behavior?
  - **ANSWER: Option A (Yes, maintain consistency across both simulations)**

**User's Answer (2026-01-03):**
"A"

**Implementation approach:**
- Align Accuracy Sim edge case handling with Win Rate Sim behavior:

  **Edge Case 1: Missing JSON file**
  - Current (both): Log warning, continue
  - Action: ✅ No change needed (already consistent)

  **Edge Case 2: Missing week_N+1 folder**
  - Win Rate Sim: Fallback to projected data
  - Accuracy Sim (current): Return None, skip week
  - Action: ⚠️ CHANGE Accuracy Sim to match Win Rate Sim (fallback to projected data)
  - Rationale: Consistent behavior, allows MAE calculation even without actuals

  **Edge Case 3: Array index out of bounds**
  - Win Rate Sim: Default to 0.0
  - Accuracy Sim (current): Check length, silently skip if too short
  - Action: ⚠️ CHANGE Accuracy Sim to match Win Rate Sim (default to 0.0)
  - Rationale: Consistent behavior, prevents silent data loss

- Add tests to verify aligned edge case behavior
- Document alignment in verification report

**Impacts on spec:**
- Requirements: Add new requirements for edge case alignment
- Edge Cases section: Update with aligned behavior
- Testing Strategy Part 3: Add edge case consistency tests

---

## Resolved Questions

All 4 questions have been resolved and integrated into spec.md:

1. **Question 1: Verification Methodology** ✅
   - Answer: Option D (Comprehensive verification - all methods)
   - Integrated into: Requirement 6 (Three-part verification: code review, manual testing, automated tests)

2. **Question 2: Test Coverage Requirements** ✅
   - Answer: Option A (Add comprehensive tests for PlayerManager integration)
   - Integrated into: Requirement 6 Part 3 (detailed test requirements for delegation pattern)

3. **Question 3: Week 17 Specific Testing** ✅
   - Answer: Option A (Dedicated Week 17 test)
   - Integrated into: Requirement 6 Part 3 (Week 17 test case with week_17 projected, week_18 actual)

4. **Question 4: Edge Case Consistency with Win Rate Sim** ✅
   - Answer: Option A (Maintain consistency across both simulations)
   - Integrated into: **NEW Requirement 7** (Align edge case handling with Win Rate Sim)

---

## Additional Scope Discovered

{Will populate during implementation if new requirements emerge}

---

## Traceability Check

**Every requirement in spec.md must have a source:**
- ✅ Requirement 1: Epic Request (line 5) - PlayerManager JSON loading
- ✅ Requirement 2: Epic Request (line 8) - Week_N+1 logic
- ✅ Requirement 3: Epic Request (line 8) - Week 17 verification
- ✅ Requirement 4: Epic Request (line 8) - Two-manager pattern
- ✅ Requirement 5: Epic Request (line 6) - Array extraction
- ✅ Requirement 6: User Constraint (line 10) - Comprehensive verification

**No assumptions found - all requirements traced to sources.**

---

## Notes

**Key architectural difference from Feature 01:**
- Win Rate Sim: Direct JSON parsing (`_parse_players_json()`)
- Accuracy Sim: PlayerManager delegation (uses league_helper's JSON loading)

**Implications:**
- Accuracy Sim doesn't need to implement JSON parsing
- Just needs to verify temporary directory setup works
- Depends on PlayerManager being correct (already migrated by league_helper)
