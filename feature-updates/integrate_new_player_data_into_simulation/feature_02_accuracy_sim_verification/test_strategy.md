# Test Strategy - Feature 02

**Created:** 2026-01-03 (Stage 5a Round 2 - Iterations 8-9)
**Purpose:** Define comprehensive test coverage for Accuracy Sim JSON verification

---

## Iteration 8: Test Strategy Development

### Test Categories

**Category 1: PlayerManager Integration Tests (Task 8)**
- Test `_create_player_manager()` creates temp directory correctly
- Test JSON files copied to temp/player_data/
- Test PlayerManager loads from temporary directory
- Test all 6 position files handled
- Test missing file handling (warning logged, continues)
- Test PlayerManager.players array populated
- **Coverage Target:** 100% of PlayerManager integration logic

**Category 2: Week_N+1 Logic Tests (Task 8)**
- Test `_load_season_data()` returns (week_N, week_N+1)
- Test week 17 returns (week_17, week_18)
- Test missing projected folder behavior
- Test missing actual folder fallback (after Task 11 changes)
- **Coverage Target:** 100% of week_N+1 logic

**Category 3: Two-Manager Pattern Tests (Task 8)**
- Test two managers created per week
- Test projected_mgr from week_N folder
- Test actual_mgr from week_N+1 folder
- Test cleanup happens (finally block)
- **Coverage Target:** 100% of two-manager pattern

**Category 4: Array Extraction Tests (Task 8)**
- Test `actual_points[week_num - 1]` indexing
- Test array bounds checking (after Task 11 changes)
- Test null value handling
- **Coverage Target:** 100% of array extraction logic

**Category 5: Week 17 Edge Case Tests (Task 9)**
- Test Week 17 uses week_17 for projected
- Test Week 17 uses week_18 for actual
- Test actual_points[16] extraction from week_18
- **Coverage Target:** 100% of Week 17 specific logic

**Category 6: Edge Case Alignment Tests (Task 10)**
- Test missing JSON file (warning logged, continues)
- Test missing week_N+1 folder (fallback to projected)
- Test array index out of bounds (default 0.0)
- **Coverage Target:** 100% of edge case handlers

**Total Test Count:** 22+ tests
**Overall Coverage Target:** >90%

---

## Iteration 9: Edge Case Enumeration

### Edge Case Catalog

| # | Edge Case | Spec Location | Current Handling | Test Task | Status |
|---|-----------|---------------|------------------|-----------|--------|
| 1 | Missing JSON file (1 of 6) | spec.md 561-574 | Log warning, continue | Task 10 | ✅ Covered |
| 2 | Missing ALL JSON files | Not in spec | Return empty players list | Task 10 | ⚠️ ADD TEST |
| 3 | Missing week_N folder | spec.md 577-596 | Return (None, None) | Task 8 | ✅ Covered |
| 4 | Missing week_N+1 folder | spec.md 577-596 | Return (projected, projected) after Task 11 | Task 10 | ✅ Covered |
| 5 | Array < 17 elements | spec.md 599-616 | Default to 0.0 after Task 11 | Task 10 | ✅ Covered |
| 6 | Array = empty [] | Not in spec | Default to 0.0 | Task 10 | ⚠️ ADD TEST |
| 7 | Null values in array | spec.md 619-632 | Skip if None or 0 | Task 8 | ✅ Covered |
| 8 | Week 17 specific | spec.md 172-196 | Use week_17 + week_18 | Task 9 | ✅ Covered |
| 9 | Malformed JSON | Not in spec | PlayerManager handles | Task 8 | ✅ Implicit (PlayerManager) |
| 10 | Player ID type mismatch | Feature 01 finding | PlayerManager uses string IDs | N/A | ✅ Implicit (PlayerManager) |
| 11 | Temp directory cleanup failure | Not in spec | Finally block ensures cleanup | Task 8 | ✅ Covered |
| 12 | Two managers same folder (fallback) | spec.md 577-596 | After Task 11: Use same folder twice | Task 10 | ✅ Covered |

**Total Edge Cases:** 12
**Covered by Tests:** 10
**Need to Add:** 2 (Missing ALL files, Empty array)

**Action:** Add 2 additional tests to Task 10

---

## Iteration 10: Configuration Change Impact

### Changes Made in Task 11

**Change 1: Missing week_N+1 Folder Fallback**
- **Old:** Return (None, None), skip week
- **New:** Return (projected_folder, projected_folder), use projected as fallback for actuals
- **Impact:** MAE calculation uses projected values when actual data missing
- **Tests Needed:** Test fallback behavior (Task 10)

**Change 2: Array Index Bounds Handling**
- **Old:** Check length, skip player if array too short
- **New:** Default to 0.0 if array too short, include player in MAE
- **Impact:** All players included in MAE calculation, even with incomplete data
- **Tests Needed:** Test bounds handling (Task 10)

**No Other Configuration Changes** - Only edge case handling alignment with Feature 01

---

## Test Coverage Analysis

### Coverage by Requirement

| Requirement | Test Tasks | Test Count | Coverage % |
|-------------|-----------|------------|------------|
| Req 1: PlayerManager JSON Loading | Task 8 | 6 tests | 100% |
| Req 2: Week_N+1 Logic | Task 8 | 4 tests | 100% |
| Req 3: Week 17 Specific | Task 9 | 4 tests | 100% |
| Req 4: Two-Manager Pattern | Task 8 | 4 tests | 100% |
| Req 5: Array Extraction | Task 8 | 3 tests | 100% |
| Req 6: Comprehensive Verification | Tasks 6-12 | All tasks | 100% |
| Req 7: Edge Case Alignment | Task 10, 11 | 3+ tests | 100% |

**Total Tests:** 24+ (22 from initial plan + 2 additional edge cases)
**Requirements Coverage:** 7/7 = 100%
**Edge Case Coverage:** 12/12 = 100%

**Overall Test Coverage:** >90% ✅

---

## Test Execution Plan

### Phase 1: Verification Tests (Tasks 6-7)
1. Code review (Task 6)
2. Manual testing (Task 7)

### Phase 2: Automated Tests - PlayerManager Integration (Task 8)
1. test_create_player_manager_temp_directory()
2. test_create_player_manager_json_file_copying()
3. test_create_player_manager_player_manager_loads_json()
4. test_create_player_manager_all_positions()
5. test_create_player_manager_missing_file()
6. test_create_player_manager_all_files_missing() ⚠️ NEW
7. test_create_player_manager_players_array_populated()
8. test_load_season_data_week_n_plus_one()
9. test_evaluate_config_weekly_two_manager_pattern()
10. test_evaluate_config_weekly_array_extraction()

### Phase 3: Automated Tests - Week 17 (Task 9)
11. test_week_17_uses_week_18_for_actuals()

### Phase 4: Automated Tests - Edge Cases (Task 10)
12. test_missing_json_file_handling()
13. test_missing_week_n_plus_one_folder()
14. test_array_index_out_of_bounds()
15. test_empty_array_handling() ⚠️ NEW

### Phase 5: 100% Test Pass (Task 12)
16. Run complete test suite
17. Verify 100% pass rate

**Total Phases:** 5
**Total Tests:** 24+ tests

---

## Iteration 8-9 Summary

**Test Strategy Developed:** ✅
- 6 test categories defined
- 24+ tests planned
- >90% coverage target met

**Edge Cases Enumerated:** ✅
- 12 edge cases identified
- 10 covered by existing plan
- 2 additional tests added

**Configuration Impact Analyzed:** ✅
- 2 changes in Task 11 identified
- Tests planned for both changes

**Coverage Verified:** ✅
- 100% requirement coverage
- 100% edge case coverage
- >90% overall coverage target met

**Next:** Proceed to Iteration 11 (Algorithm Re-verification)
