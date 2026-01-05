# Feature 02: Accuracy Sim JSON Verification - TODO List

**Feature:** Accuracy Simulation JSON Verification and Cleanup
**Created:** 2026-01-03 (Stage 5a - Round 1)
**Status:** DRAFT (Round 1 - Iteration 3)

---

## Task 1: Verify PlayerManager JSON Loading

**Requirement:** Requirement 1 - Verify PlayerManager JSON Loading in Simulation Context (spec.md lines 126-148)
**Epic Citation:** Line 5: "Correctly load in the json files contained in the week_X folders"

**Acceptance Criteria:**
- [ ] Code review of `_create_player_manager()` method (AccuracySimulationManager.py lines 339-404)
- [ ] Verified temp directory creation with player_data/ subfolder
- [ ] Verified 6 JSON files copied from week folder to temp/player_data/:
  - qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
- [ ] Verified PlayerManager.load_players_from_json() automatically loads from temp/player_data/
- [ ] Verified PlayerManager.players array is populated correctly
- [ ] Verified no FileNotFoundError when PlayerManager loads JSON
- [ ] Manual test: Run Accuracy Sim, verify PlayerManager loads JSON correctly
- [ ] Document findings in verification report

**Implementation Location:**
- File: simulation/accuracy/AccuracySimulationManager.py
- Method: _create_player_manager() (EXISTING - lines 339-404)
- Action: VERIFY correctness (not modify, unless bugs found)

**Dependencies:**
- Depends on: Task 2 (week_N+1 logic correct)

**Tests:**
- Manual testing (Task 1 - Part 2 of Req 6)
- Code review (Task 1 - Part 1 of Req 6)

---

## Task 2: Verify Week_N+1 Logic

**Requirement:** Requirement 2 - Verify Week_N+1 Logic Correctness (spec.md lines 151-169)
**Epic Citation:** Line 8: "use the week_17 folders to determine a projected_points...look at the actual_points array in week_18 folders"

**Acceptance Criteria:**
- [ ] Code review of `_load_season_data()` method (AccuracySimulationManager.py lines 293-337)
- [ ] Verified projected_folder = week_{week_num:02d}
- [ ] Verified actual_folder = week_{week_num+1:02d}
- [ ] Verified both folders must exist (returns None, None if either missing)
- [ ] Verified `_evaluate_config_weekly()` uses both folders correctly (lines 436-445):
  - projected_mgr from projected_folder (week_N)
  - actual_mgr from actual_folder (week_N+1)
- [ ] Manual test: Run Accuracy Sim for weeks 1, 10, verify week_N+1 pattern
- [ ] Document verification findings

**Implementation Location:**
- File: simulation/accuracy/AccuracySimulationManager.py
- Method: _load_season_data() (EXISTING - lines 293-337)
- Method: _evaluate_config_weekly() (EXISTING - lines 412-533)
- Action: VERIFY correctness (not modify, unless bugs found)

**Dependencies:**
- Depends on: Task 3 (Week 17 specific verification)

**Tests:**
- Code review: Verify week_N+1 pattern implementation
- Manual testing: Verify week_N+1 logic works correctly

---

## Task 3: Verify Week 17 Logic

**Requirement:** Requirement 3 - Verify Week 17 Logic Specifically (spec.md lines 172-196)
**Epic Citation:** Line 8: "I want to verify if Week 17 is being correctly assessed...use the week_17 folders...look at the actual_points array in week_18 folders"

**Acceptance Criteria:**
- [ ] Verified `_load_season_data()` week_N+1 logic applies to week 17:
  - week_num = 17 → projected_folder = week_17, actual_folder = week_18
  - Lines 318-323: actual_week_num = 17 + 1 = 18
- [ ] Verified week_18 folder exists with real data (research confirmed: exists)
- [ ] Verified two-manager pattern works for week 17:
  - projected_mgr from week_17 → score_player() calculations
  - actual_mgr from week_18 → extract actual_points[16] (line 486)
- [ ] Manual test: Run Accuracy Sim for week 17, verify data sources
- [ ] Document verification findings

**Implementation Location:**
- File: simulation/accuracy/AccuracySimulationManager.py
- Methods: _load_season_data(), _evaluate_config_weekly()
- Action: VERIFY week 17 specific behavior

**Dependencies:**
- Depends on: Task 2 (week_N+1 logic verification)

**Tests:**
- Code review: Verify week 17 uses week_18
- Manual testing: Week 17 specific test

---

## Task 4: Verify Two-Manager Pattern

**Requirement:** Requirement 4 - Verify Two-Manager Pattern Correctness (spec.md lines 199-219)
**Epic Citation:** Line 8: "This means we'll likely need two Player Managers - one for the N week and one for the N+1 week"

**Acceptance Criteria:**
- [ ] Code review of `_evaluate_config_weekly()` two-manager pattern (lines 441-505):
  - projected_mgr (from week_N folder): Used for score_player() calculations
  - actual_mgr (from week_N+1 folder): Used for extracting actual_points array
  - Line 486: `actual = player.actual_points[week_num - 1]`
  - Array index: week 1 = index 0, week 17 = index 16
  - Matches projections to actuals by player.id
  - Cleanup both managers after use (finally block)
- [ ] Verified both managers created per week
- [ ] Verified cleanup happens even if errors occur
- [ ] Manual test: Inspect two-manager creation during simulation run
- [ ] Document findings

**Implementation Location:**
- File: simulation/accuracy/AccuracySimulationManager.py
- Method: _evaluate_config_weekly() (EXISTING - lines 412-533)
- Action: VERIFY two-manager pattern correctness

**Dependencies:**
- Depends on: Task 1 (PlayerManager loading), Task 2 (week_N+1 logic)

**Tests:**
- Code review: Verify two-manager pattern implementation
- Manual testing: Verify both managers created correctly

---

## Task 5: Verify Array Extraction

**Requirement:** Requirement 5 - Verify Array Extraction Correctness (spec.md lines 222-242)
**Epic Citation:** Line 6: "Correctly update the simulations to accomidate the changes to the drafted_by, locked, projected_points, and actual_points fields"

**Acceptance Criteria:**
- [ ] Verified array indexing (line 486):
  - `actual = player.actual_points[week_num - 1]`
  - Week 1 = index 0, Week 17 = index 16
  - Checks array length before indexing: `len(player.actual_points) >= week_num`
- [ ] Verified projected points come from score_player() (not direct array access):
  - Lines 458-478: projected_mgr.score_player() returns scored player
  - Uses scored.projected_points (calculated value, not raw array)
- [ ] Verified null/missing value handling:
  - Line 487: Checks `actual is not None and actual > 0`
  - Only includes valid actual points in MAE calculation
- [ ] Manual test: Inspect extracted values for correctness
- [ ] Document verification findings

**Implementation Location:**
- File: simulation/accuracy/AccuracySimulationManager.py
- Method: _evaluate_config_weekly() (EXISTING - lines 482-497)
- Action: VERIFY array extraction correctness

**Dependencies:**
- Depends on: Task 4 (two-manager pattern)

**Tests:**
- Code review: Verify array indexing logic
- Manual testing: Verify extracted values correct

**Updated based on Feature 01 alignment (2026-01-03):**
- ✅ Array indexing pattern verified: `actual_points[week_num - 1]` matches Feature 01
- ✅ Week 17 logic verified: Uses week_num (not actual_week_num) for indexing

---

## Task 6: Code Review - PlayerManager Integration

**Requirement:** Requirement 6 Part 1 - Comprehensive Verification (Code Review) (spec.md lines 256-263)
**Epic Citation:** Line 10: "ASSUME ALL PREVIOUS WORK IS INCORRECT OR INCOMPLETE AND VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
**User Requirement:** "verify the simulation has correctly adapted to the new ways of storing data"

**Acceptance Criteria:**
- [ ] Line-by-line review of `_create_player_manager()` (lines 339-404)
- [ ] Line-by-line review of `_load_season_data()` (lines 293-337)
- [ ] Line-by-line review of `_evaluate_config_weekly()` (lines 412-533)
- [ ] Verify JSON file copying logic correct
- [ ] Verify PlayerManager integration correct
- [ ] Verify array extraction logic correct
- [ ] Verify temp directory cleanup logic correct
- [ ] Document all findings in verification report
- [ ] Confirm: PlayerManager correctly loads JSON in simulation context

**Implementation Location:**
- File: simulation/accuracy/AccuracySimulationManager.py
- Methods to review:
  - _create_player_manager() (lines 339-404)
  - _load_season_data() (lines 293-337)
  - _evaluate_config_weekly() (lines 412-533)

**Dependencies:**
- None (code review can be done first)

**Tests:**
- N/A (this IS the verification)

---

## Task 7: Manual Testing - Runtime Verification

**Requirement:** Requirement 6 Part 2 - Comprehensive Verification (Manual Testing) (spec.md lines 265-272)
**Epic Citation:** Line 10: "VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"

**Acceptance Criteria:**
- [ ] Run Accuracy Simulation with JSON data for weeks 1, 10, 17
- [ ] Inspect loaded player data for week 1
- [ ] Inspect loaded player data for week 10
- [ ] Inspect loaded player data for week 17
- [ ] Verify PlayerManager loads JSON correctly in temp directory context
- [ ] Verify week_N+1 logic works (projected from N, actual from N+1)
- [ ] Verify week 17 uses week_18 for actuals
- [ ] Confirm no FileNotFoundError for players.csv
- [ ] Document results in verification report

**Implementation Location:**
- Script: run_accuracy_simulation.py (or equivalent command)
- Command: `python run_accuracy_simulation.py` (or similar)

**Dependencies:**
- Depends on: Tasks 1-5 (code review completed)

**Tests:**
- Manual execution and inspection

---

## Task 8: Add/Verify Comprehensive JSON Loading Tests

**Requirement:** Requirement 6 Part 3 - Comprehensive Verification (Automated Tests) (spec.md lines 274-292)
**Epic Citation:** Line 10: "VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
**User Answer:** Question 2 - Option A: "Add comprehensive tests for JSON loading" (per checklist - assuming same answer as Feature 01)

**Acceptance Criteria:**
- [ ] Inspect tests/integration/test_accuracy_simulation_integration.py for existing tests
- [ ] ADD test: `test_create_player_manager_temp_directory()` - Test temp directory creation
- [ ] ADD test: `test_create_player_manager_json_file_copying()` - Test JSON files copied to temp/player_data/
- [ ] ADD test: `test_create_player_manager_player_manager_loads_json()` - Test PlayerManager loads from temp
- [ ] ADD test: `test_create_player_manager_all_positions()` - Test all 6 position files
- [ ] ADD test: `test_create_player_manager_missing_file()` - Test error handling (warning logged)
- [ ] ADD test: `test_create_player_manager_players_array_populated()` - Test PlayerManager.players populated
- [ ] ADD test: `test_load_season_data_week_n_plus_one()` - Test week_N+1 pattern
- [ ] ADD test: `test_evaluate_config_weekly_two_manager_pattern()` - Test two-manager creation
- [ ] ADD test: `test_evaluate_config_weekly_array_extraction()` - Test array indexing
- [ ] Verify all tests pass (100% pass rate)

**Implementation Location:**
- File: tests/integration/test_accuracy_simulation_integration.py
- Add new test methods to existing test class (or create new class if needed)

**Dependencies:**
- Depends on: Task 6 (code review confirms what to test)

**Tests:**
- Run: `python -m pytest tests/integration/test_accuracy_simulation_integration.py -v`

---

## Task 9: Add Dedicated Week 17 Edge Case Test

**Requirement:** Requirement 6 Part 3 - Comprehensive Verification (Automated Tests - Week 17) (spec.md lines 283-289)
**Epic Citation:** Line 8: "I want to verify if Week 17 is being correctly assessed"
**User Answer:** Question 3 - Option A: "Yes, dedicated test verifying week_17 projected + week_18 actual" (per checklist - assuming same answer as Feature 01)

**Acceptance Criteria:**
- [ ] ADD test: `test_week_17_uses_week_18_for_actuals()`
- [ ] Test verifies: _load_season_data(season_path, week_num=17) returns (week_17, week_18)
- [ ] Test verifies: _evaluate_config_weekly() for week 17 creates two managers correctly
- [ ] Test verifies: projected_mgr from week_17 folder
- [ ] Test verifies: actual_mgr from week_18 folder
- [ ] Test verifies: actual_points[16] extracted from week_18 data
- [ ] Test uses real data structure (17-element arrays)
- [ ] Test verifies week_18 folder exists with real week 17 data
- [ ] Test passes (confirms Week 17 logic correct)

**Implementation Location:**
- File: tests/integration/test_accuracy_simulation_integration.py
- Add new test method: test_week_17_uses_week_18_for_actuals()

**Dependencies:**
- Depends on: Task 8 (comprehensive tests framework)

**Tests:**
- Run: `python -m pytest tests/integration/test_accuracy_simulation_integration.py::test_week_17_uses_week_18_for_actuals -v`

---

## Task 10: Add Edge Case Alignment Tests

**Requirement:** Requirement 7 - Align Edge Case Handling with Win Rate Sim (spec.md lines 310-348)
**Epic Citation:** Line 2: "Both the Win Rate sim and Accuracy Sim should maintain the same functionality"
**User Answer:** Question 4 - Option A: "Maintain consistency across both simulations" (per checklist - assuming same answer as Feature 01)

**Acceptance Criteria:**
- [ ] ADD test: `test_missing_json_file_handling()` - Verify warning logged, continues
- [ ] ADD test: `test_missing_week_n_plus_one_folder()` - Verify fallback to projected data
- [ ] ADD test: `test_array_index_out_of_bounds()` - Verify default 0.0, no IndexError
- [ ] Verify tests confirm Accuracy Sim edge case behavior matches Win Rate Sim:
  - Missing file: Log warning, continue (not crash)
  - Missing week_N+1 folder: Fallback to projected (not skip week)
  - Array bounds: Default to 0.0 (not skip player)
- [ ] All edge case alignment tests pass

**Implementation Location:**
- File: tests/integration/test_accuracy_simulation_integration.py
- Add 3 new edge case test methods

**Dependencies:**
- Depends on: Task 8 (comprehensive tests framework)
- Depends on: Task 11 (edge case alignment code changes)

**Tests:**
- Run: `python -m pytest tests/integration/test_accuracy_simulation_integration.py -k "edge" -v`

---

## Task 11: Align Edge Case Handling with Win Rate Sim

**Requirement:** Requirement 7 - Align Edge Case Handling with Win Rate Sim (spec.md lines 310-348)
**Epic Citation:** Line 2: "Both the Win Rate sim and Accuracy Sim should maintain the same functionality"
**User Answer:** Question 4 - Option A: "Maintain consistency across both simulations"

**Acceptance Criteria:**
- [ ] UPDATE `_load_season_data()` lines 330-335 (Missing week_N+1 folder handling):
  - Old: `return None, None` (skip week)
  - New: `return (projected_folder, projected_folder)` (fallback to projected)
  - Log warning: "Actual folder not found...Using projected data as fallback"
  - Allows MAE calculation using projected values as fallback actuals
- [ ] UPDATE `_evaluate_config_weekly()` lines 485-487 (Array index bounds handling):
  - Remove length check: `if 1 <= week_num <= 17 and len(player.actual_points) >= week_num`
  - Add default fallback: `actual = player.actual_points[week_num - 1] if len(player.actual_points) > week_num - 1 else 0.0`
  - Include players with 0.0 actual in MAE calculation (consistent with Win Rate Sim)
  - Remove null check OR update to include 0.0 values
- [ ] Verify changes match Win Rate Sim behavior exactly
- [ ] Document alignment in code comments

**Implementation Location:**
- File: simulation/accuracy/AccuracySimulationManager.py
- Lines to UPDATE:
  - _load_season_data() lines 330-335 (fallback behavior)
  - _evaluate_config_weekly() lines 485-487 (array bounds handling)

**Dependencies:**
- Depends on: Task 6 (code review confirms current behavior)
- Blocks: Task 10 (edge case alignment tests depend on this)

**Tests:**
- Verify with Task 10 tests (edge case alignment tests)

---

## Task 12: Verify 100% Test Pass Rate

**Requirement:** Requirement 6 Part 3 - Comprehensive Verification (Test Coverage) (spec.md line 292)
**Epic Citation:** Line 10: "VERIFY EVERYTHING"

**Acceptance Criteria:**
- [ ] Run complete test suite: `python tests/run_all_tests.py`
- [ ] Verify exit code 0 (all tests pass)
- [ ] Verify 2,200+ tests passing (100% pass rate)
- [ ] No test failures related to JSON migration
- [ ] Accuracy Simulation integration tests pass

**Implementation Location:**
- Command: python tests/run_all_tests.py

**Dependencies:**
- Depends on: Tasks 8-11 (all new tests added, edge case changes made)

**Tests:**
- This IS the test execution

---

## Summary

**Total Tasks:** 12
- Task 1: Verify PlayerManager JSON loading
- Task 2: Verify week_N+1 logic
- Task 3: Verify Week 17 logic
- Task 4: Verify two-manager pattern
- Task 5: Verify array extraction
- Task 6: Code review - PlayerManager integration
- Task 7: Manual testing - runtime verification
- Task 8: Add comprehensive JSON loading tests (9 tests)
- Task 9: Add Week 17 dedicated test (1 test)
- Task 10: Add edge case alignment tests (3 tests)
- Task 11: Align edge case handling with Win Rate Sim (2 code changes)
- Task 12: Verify 100% test pass rate

**Requirements Coverage:**
- ✅ Requirement 1: Tasks 1, 6, 7, 8
- ✅ Requirement 2: Tasks 2, 6, 7, 8
- ✅ Requirement 3: Tasks 3, 6, 7, 9
- ✅ Requirement 4: Tasks 4, 6, 7, 8
- ✅ Requirement 5: Tasks 5, 6, 7, 8
- ✅ Requirement 6: Tasks 6, 7, 8, 9, 10, 12
- ✅ Requirement 7: Tasks 10, 11

**All requirements have corresponding TODO tasks.**
