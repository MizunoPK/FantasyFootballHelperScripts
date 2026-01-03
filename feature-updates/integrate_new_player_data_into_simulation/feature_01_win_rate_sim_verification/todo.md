# Feature 01: Win Rate Sim JSON Verification - TODO List

**Feature:** Win Rate Simulation JSON Verification and Cleanup
**Created:** 2026-01-03 (Stage 5a - Round 1)
**Status:** DRAFT (Round 1 - Iteration 1)

---

## Task 1: Delete Deprecated CSV Parsing Method

**Requirement:** Requirement 1 - Remove CSV File Loading (spec.md lines 137-149)
**Epic Citation:** Line 4: "No longer try to load in players.csv or players_projected.csv"

**Acceptance Criteria:**
- [ ] Method `_parse_players_csv()` deleted from SimulatedLeague.py (lines 338-361)
- [ ] Verified no calls to `_parse_players_csv()` exist in codebase
- [ ] Grep search confirms method no longer exists:
  ```bash
  grep -r "_parse_players_csv" simulation/
  # Should return 0 results
  ```

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Lines to DELETE: 338-361
- Method: _parse_players_csv()

**Dependencies:**
- None (safe to delete - research confirmed no calls exist)

**Tests:**
- Verify deletion: Search codebase for any references
- All existing tests still pass after deletion

---

## Task 2: Verify JSON Loading Implementation

**Requirement:** Requirement 2 - Verify JSON Loading Correctness (spec.md lines 152-166)
**Epic Citation:** Line 5: "Correctly load in the json files contained in the week_X folders"

**Acceptance Criteria:**
- [ ] Code review of `_parse_players_json()` method (SimulatedLeague.py lines 363-440)
- [ ] Verified reads 6 position files: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
- [ ] Verified file paths correct: simulation/sim_data/{year}/weeks/week_{NN}/
- [ ] Verified handles missing files gracefully (logs warning, continues)
- [ ] Manual test: Run simulation, inspect logs for JSON file loading
- [ ] Document findings in verification report

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Method: _parse_players_json() (EXISTING - lines 363-440)
- Action: VERIFY correctness (not modify)

**Dependencies:**
- Depends on: Task 3 (field structure verification)

**Tests:**
- Manual testing (Task 2 - Part 2 of Req 6)
- Code review (Task 2 - Part 1 of Req 6)

---

## Task 3: Verify Field Structure Handling

**Requirement:** Requirement 3 - Verify Field Structure Handling (spec.md lines 169-189)
**Epic Citation:** Line 6: "Correctly update the simulations to accomidate the changes to the drafted_by, locked, projected_points, and actual_points fields"

**Acceptance Criteria:**
- [ ] Verified `drafted_by` field handling (line 430): String (no change from CSV)
- [ ] Verified `locked` field handling (line 431): Boolean → String "0"/"1" conversion
- [ ] Verified `projected_points` array extraction (lines 413-417): Extract via [week_num - 1]
- [ ] Verified `actual_points` array extraction (lines 419-423): Extract via [actual_week - 1]
- [ ] Verified array indexing uses zero-based index correctly
- [ ] Manual test: Inspect loaded data for correct field values
- [ ] Document verification findings

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Method: _parse_players_json() (EXISTING - lines 363-440)
- Specific lines to verify: 413-417 (projected_points), 419-423 (actual_points), 430-431 (drafted_by, locked)

**Dependencies:**
- Part of: Task 2 (JSON loading verification)

**Tests:**
- Code review: Verify array indexing logic
- Manual testing: Verify extracted values correct

---

## Task 4: Verify Week 17 Logic

**Requirement:** Requirement 4 - Verify Week 17 Logic (spec.md lines 192-215)
**Epic Citation:** Line 8: "use the week_17 folders to determine a projected_points...look at the actual_points array in week_18 folders"
**⚠️ SPEC ERROR:** spec.md references `_preload_week_data()` but actual method is `_preload_all_weeks()`

**Acceptance Criteria:**
- [ ] Verified `_preload_all_weeks()` week_N+1 logic (lines 269-336)
- [ ] Verified week 17 loads week_17 folder for projected data (line 298)
- [ ] Verified week 17 loads week_18 folder for actual data (line 302)
- [ ] Verified `week_num_for_actual` parameter used correctly (value 18 for week 17, line 314)
- [ ] Verified week_18 folder exists with real data (actual_points[16] filled)
- [ ] Manual test: Run simulation for week 17, verify data sources
- [ ] Document verification findings
- [ ] **NOTE:** Update spec.md line 201 to reference correct method name (_preload_all_weeks)

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Method: _preload_all_weeks() (EXISTING - lines 269-336, NOT _preload_week_data as spec says)
- Action: VERIFY week_N+1 pattern for week 17

**Dependencies:**
- Depends on: Task 2 (JSON loading), Task 3 (field structure)

**Tests:**
- Code review: Verify week_num_for_actual parameter
- Manual testing: Week 17 specific test
- Automated test: Add dedicated Week 17 test (Task 9)

---

## Task 5: Update Documentation (Docstrings)

**Requirement:** Requirement 5 - Update Documentation (spec.md lines 218-231)
**Epic Citation:** Line 4: "No longer try to load in players.csv or players_projected.csv"

**Acceptance Criteria:**
- [ ] UPDATE SimulationManager.py line 180:
  - Old: "players.csv in each week folder"
  - New: "6 position JSON files (QB, RB, WR, TE, K, DST) in player_data/week_X folders"

- [ ] UPDATE SimulatedLeague.py lines 91-92:
  - Old: "players_projected.csv, players_actual.csv"
  - New: "week folders with JSON files for each position"

- [ ] UPDATE SimulatedOpponent.py lines 77-78:
  - Old: "PlayerManager using players_projected.csv"
  - New: "PlayerManager using JSON files from player_data/ folder"

- [ ] UPDATE DraftHelperTeam.py lines 72-73:
  - Old: "PlayerManager using players_projected.csv"
  - New: "PlayerManager using JSON files from player_data/ folder"

**Implementation Location:**
- File 1: simulation/win_rate/SimulationManager.py (line 180)
- File 2: simulation/win_rate/SimulatedLeague.py (lines 91-92)
- File 3: simulation/win_rate/SimulatedOpponent.py (lines 77-78)
- File 4: simulation/win_rate/DraftHelperTeam.py (lines 72-73)

**Dependencies:**
- Should be done AFTER verification (Tasks 2-4 confirm JSON structure)

**Tests:**
- Verify docstrings updated: Grep for CSV references
- All docstrings mention JSON structure

---

## Task 6: Code Review - JSON Parsing Logic

**Requirement:** Requirement 6 Part 1 - Comprehensive Verification (Code Review) (spec.md lines 247-252)
**Epic Citation:** Line 10: "VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
**User Requirement:** "make sure the simulation has correctly adapted to the new ways of storing data"

**Acceptance Criteria:**
- [ ] Line-by-line review of `_parse_players_json()` (lines 363-440)
- [ ] Line-by-line review of `_preload_all_weeks()` (lines 269-336)
- [ ] Verify array indexing: projected_points[week_num - 1], actual_points[actual_week - 1]
- [ ] Verify field conversions: locked (boolean → string), arrays → single values
- [ ] Verify error handling: missing files, malformed JSON
- [ ] Document all findings in verification report
- [ ] Confirm: projected_points and actual_points arrays used correctly
- [ ] **NOTE:** spec.md line 251 references wrong method name (_preload_week_data should be _preload_all_weeks)

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Methods to review:
  - _parse_players_json() (lines 363-440)
  - _preload_all_weeks() (lines 269-336, NOT _preload_week_data as spec says)

**Dependencies:**
- None (code review can be done first)

**Tests:**
- N/A (this IS the verification)

---

## Task 7: Manual Testing - Runtime Verification

**Requirement:** Requirement 6 Part 2 - Comprehensive Verification (Manual Testing) (spec.md lines 254-261)
**Epic Citation:** Line 10: "VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"

**Acceptance Criteria:**
- [ ] Run Win Rate Simulation with JSON data
- [ ] Inspect loaded player data for week 1
- [ ] Inspect loaded player data for week 10
- [ ] Inspect loaded player data for week 17
- [ ] Verify projected_points arrays correctly extracted (single values, not arrays)
- [ ] Verify actual_points arrays correctly extracted (single values, not arrays)
- [ ] Verify week 17 uses week_18 folder for actuals
- [ ] Confirm no FileNotFoundError for players.csv
- [ ] Document results in verification report

**Implementation Location:**
- Script: run_win_rate_simulation.py
- Command: `python run_win_rate_simulation.py`

**Dependencies:**
- Depends on: Tasks 2-4 (code review completed)

**Tests:**
- Manual execution and inspection

---

## Task 8: Add/Verify Comprehensive JSON Loading Tests

**Requirement:** Requirement 6 Part 3 - Comprehensive Verification (Automated Tests) (spec.md lines 263-279)
**Epic Citation:** Line 10: "VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
**User Answer:** Question 2 - Option A: "Add comprehensive tests for JSON loading"

**Acceptance Criteria:**
- [ ] Inspect tests/simulation/test_SimulatedLeague.py for existing JSON tests
- [ ] ADD test: `test_parse_players_json_valid_data()` - Test with valid JSON
- [ ] ADD test: `test_parse_players_json_array_extraction()` - Test week-specific value extraction
- [ ] ADD test: `test_parse_players_json_field_conversions()` - Test locked boolean → string
- [ ] ADD test: `test_parse_players_json_all_positions()` - Test all 6 position files
- [ ] ADD test: `test_parse_players_json_missing_file()` - Test error handling (warning logged)
- [ ] ADD test: `test_parse_players_json_malformed_json()` - Test malformed JSON handling
- [ ] ADD test: `test_parse_players_json_empty_arrays()` - Test edge case: empty arrays
- [ ] ADD test: `test_parse_players_json_week_num_for_actual()` - Test week_N+1 parameter
- [ ] ADD test: `test_preload_all_weeks_success()` - Test successful preloading of all weeks
- [ ] ADD test: `test_preload_week_data_week_n_plus_one()` - Test week_N+1 loading pattern
- [ ] ADD test: `test_json_loading_integration_with_simulation()` - Integration test (full simulation)
- [ ] Verify all tests pass (100% pass rate)
- [ ] **UPDATED (Iteration 8):** Added 3 additional tests (total 12 unit/integration tests)

**Implementation Location:**
- File: tests/simulation/test_SimulatedLeague.py
- Add new test methods to existing test class

**Dependencies:**
- Depends on: Task 6 (code review confirms what to test)

**Tests:**
- Run: `python -m pytest tests/simulation/test_SimulatedLeague.py -v`

---

## Task 9: Add Dedicated Week 17 Edge Case Test

**Requirement:** Requirement 6 Part 3 - Comprehensive Verification (Automated Tests - Week 17) (spec.md lines 273-279)
**Epic Citation:** Line 8: "verify if Week 17 is being correctly assessed"
**User Answer:** Question 3 - Option A: "Yes, dedicated test verifying week_17 projected + week_18 actual"

**Acceptance Criteria:**
- [ ] ADD test: `test_week_17_uses_week_18_for_actuals()`
- [ ] Test verifies: _preload_all_weeks() for week 17 loads week_17 and week_18 folders
- [ ] Test verifies: projected_points extracted from week_17 data
- [ ] Test verifies: actual_points extracted from week_18 data (actual_points[16])
- [ ] Test verifies: week_num_for_actual=18 parameter used
- [ ] Test uses real data structure (17-element arrays)
- [ ] Test passes (confirms Week 17 logic correct)
- [ ] **NOTE:** spec.md line 253 uses wrong method name

**Implementation Location:**
- File: tests/simulation/test_SimulatedLeague.py
- Add new test method: test_week_17_uses_week_18_for_actuals()

**Dependencies:**
- Depends on: Task 8 (comprehensive tests framework)

**Tests:**
- Run: `python -m pytest tests/simulation/test_SimulatedLeague.py::test_week_17_uses_week_18_for_actuals -v`

---

## Task 10: Add Edge Case Behavior Tests

**Requirement:** Requirement 6 Part 3 - Comprehensive Verification (Automated Tests - Edge Cases) (spec.md lines 280-284)
**User Answer:** Question 4 - Option A: "Align edge cases with Win Rate Sim behavior"

**Acceptance Criteria:**
- [ ] ADD test: `test_missing_json_file_handling()` - Verify warning logged, continues
- [ ] ADD test: `test_missing_week_n_plus_one_folder()` - Verify fallback to projected data
- [ ] ADD test: `test_array_index_out_of_bounds()` - Verify default 0.0, no IndexError
- [ ] ADD test: `test_malformed_json_handling()` - Verify appropriate error handling
- [ ] ADD test: `test_preload_all_weeks_missing_week_n_folder()` - Verify skip week, log warning
- [ ] ADD test: `test_preload_all_weeks_missing_week_n_plus_one_folder()` - Verify fallback logic
- [ ] ADD test: `test_parse_players_json_empty_json_array()` - Verify empty [] array returns empty dict
- [ ] ADD test: `test_parse_players_json_all_files_missing()` - Verify empty week folder (all 6 files missing)
- [ ] ADD test: `test_preload_all_weeks_legacy_mode()` - Verify fallback when weeks/ folder missing
- [ ] ADD test: `test_parse_players_json_null_values_in_array()` - Verify null handling in arrays
- [ ] Verify tests confirm Win Rate Sim edge case behavior:
  - Missing file: Log warning, continue (not crash)
  - Missing folder: Fallback to projected (not None)
  - Array bounds: Default to 0.0 (not crash)
  - Empty arrays: Default to 0.0 (not crash)
  - Null values: Handle gracefully (not crash)
- [ ] All edge case tests pass
- [ ] **UPDATED (Iteration 8):** Added 2 additional edge case tests (total 6 edge case tests)
- [ ] **UPDATED (Iteration 9):** Added 4 additional edge case tests (total 10 edge case tests)

**Implementation Location:**
- File: tests/simulation/test_SimulatedLeague.py
- Add 4 new edge case test methods

**Dependencies:**
- Depends on: Task 8 (comprehensive tests framework)

**Tests:**
- Run: `python -m pytest tests/simulation/test_SimulatedLeague.py -k "edge" -v`

---

## Task 11: Verify 100% Test Pass Rate

**Requirement:** Requirement 6 Part 3 - Comprehensive Verification (Test Coverage) (spec.md line 285)
**Epic Citation:** Line 10: "VERIFY EVERYTHING"

**Acceptance Criteria:**
- [ ] Run complete test suite: `python tests/run_all_tests.py`
- [ ] Verify exit code 0 (all tests pass)
- [ ] Verify 2,200+ tests passing (100% pass rate)
- [ ] No test failures related to JSON migration
- [ ] Simulation integration tests pass
- [ ] ADD test: `test_backward_compatibility_with_csv_deletion()` - Verify deletion doesn't break existing code
- [ ] **UPDATED (Iteration 8):** Added regression test for CSV deletion (total 1 regression test)

**Implementation Location:**
- Command: python tests/run_all_tests.py

**Dependencies:**
- Depends on: Tasks 8-10 (all new tests added)

**Tests:**
- This IS the test execution

---

## Summary

**Total Tasks:** 11
- Task 1: Delete deprecated method
- Task 2: Verify JSON loading
- Task 3: Verify field structure handling
- Task 4: Verify Week 17 logic
- Task 5: Update documentation (4 docstrings)
- Task 6: Code review
- Task 7: Manual testing
- Task 8: Add comprehensive JSON tests (9 tests)
- Task 9: Add Week 17 dedicated test (1 test)
- Task 10: Add edge case tests (4 tests)
- Task 11: Verify 100% test pass rate

**Requirements Coverage:**
- ✅ Requirement 1: Task 1
- ✅ Requirement 2: Tasks 2, 6, 7, 8
- ✅ Requirement 3: Tasks 3, 6, 7, 8
- ✅ Requirement 4: Tasks 4, 6, 7, 9
- ✅ Requirement 5: Task 5
- ✅ Requirement 6: Tasks 6, 7, 8, 9, 10, 11

**All requirements have corresponding TODO tasks.**
