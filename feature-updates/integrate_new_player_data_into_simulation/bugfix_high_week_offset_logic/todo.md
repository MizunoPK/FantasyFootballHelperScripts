# Bug Fix TODO: Week Offset Logic

**Created:** 2026-01-02
**Status:** Stage 5a Round 1 (Iteration 1 complete)

---

## Phase 1: Code Changes

### Task 1: Update _load_season_data() in AccuracySimulationManager

**Requirement:** Return two week folders (week_N for projections, week_N+1 for actuals) (spec.md "Code Changes Required" - Change 1)

**Acceptance Criteria:**
- [ ] Method signature unchanged: `_load_season_data(self, season_path: Path, week_num: int) -> Tuple[Optional[Path], Optional[Path]]`
- [ ] Creates `projected_folder` variable: `season_path / "weeks" / f"week_{week_num:02d}"`
- [ ] Creates `actual_folder` variable: `season_path / "weeks" / f"week_{week_num+1:02d}"`
- [ ] Checks both folders exist (both must exist to proceed)
- [ ] Logs warning if projected_folder missing: "Projected folder not found: {path}"
- [ ] Logs warning if actual_folder missing: "Actual folder not found: {path} (needed for week {week_num} actuals)"
- [ ] Returns (projected_folder, actual_folder) instead of (week_folder, week_folder)
- [ ] Returns (None, None) if either folder missing
- [ ] Docstring updated to explain WHY two folders needed (point-in-time data model)

**Implementation Location:**
- File: `simulation/accuracy/AccuracySimulationManager.py`
- Method: `_load_season_data()`
- Lines: 293-313 (current BROKEN code)

**Dependencies:**
- None (foundational change)

**Tests:**
- Unit test: `test_load_season_data_returns_two_folders()` (Task 6)
- Unit test: `test_load_season_data_handles_missing_actual_folder()` (Task 7)

---

### Task 2: Update get_accuracy_for_week() in AccuracySimulationManager

**Requirement:** Create two PlayerManager instances (one for projections, one for actuals) (spec.md "Code Changes Required" - Change 2)

**Acceptance Criteria:**
- [ ] Checks both projected_path AND actual_path: `if not projected_path or not actual_path: continue`
- [ ] Creates `projected_mgr`: `self._create_player_manager(config_dict, projected_path, season_path)`
- [ ] Creates `actual_mgr`: `self._create_player_manager(config_dict, actual_path, season_path)`
- [ ] Wraps both managers in try/finally block
- [ ] Calculates max_weekly from projected_mgr: `projected_mgr.calculate_max_weekly_projection(week_num)`
- [ ] Gets projections from `projected_mgr.players` loop
- [ ] Gets actuals from `actual_mgr.players` loop
- [ ] Matches players by ID: `if player.id in projections`
- [ ] Gets actual points: `player.actual_points[week_num - 1]` from actual_mgr (week_N+1 folder)
- [ ] Cleans up BOTH managers in finally: `self._cleanup_player_manager(projected_mgr)` and `self._cleanup_player_manager(actual_mgr)`

**Implementation Location:**
- File: `simulation/accuracy/AccuracySimulationManager.py`
- Method: `get_accuracy_for_week()`
- Lines: 411-472 (current BROKEN code)

**Dependencies:**
- Requires: Task 1 complete (_load_season_data returns two folders)

**Tests:**
- Unit test: `test_get_accuracy_uses_correct_folders()` (Task 8)
- Integration test: `test_week_1_accuracy_with_real_data()` (Task 9)
- Integration test: `test_all_weeks_have_realistic_mae()` (Task 11)

---

### Task 3: Update _load_season_data() in ParallelAccuracyRunner

**Requirement:** Apply identical fix to parallel implementation (spec.md "Code Changes Required" - Change 3)

**Acceptance Criteria:**
- [ ] IDENTICAL changes to Task 1 (consistency between serial and parallel)
- [ ] Method signature unchanged
- [ ] Creates projected_folder and actual_folder variables
- [ ] Checks both folders exist
- [ ] Logs warnings if folders missing
- [ ] Returns (projected_folder, actual_folder)
- [ ] Returns (None, None) if either folder missing
- [ ] Docstring updated with same explanation

**Implementation Location:**
- File: `simulation/accuracy/ParallelAccuracyRunner.py`
- Method: `_load_season_data()`
- Lines: Find method location (similar structure to AccuracySimulationManager)

**Dependencies:**
- Conceptually after Task 1 (use same pattern)

**Tests:**
- Unit test: test in ParallelAccuracyRunner test file (same pattern as Task 1)

---

### Task 4: Update week calculation in ParallelAccuracyRunner

**Requirement:** Apply identical fix to parallel week calculation loop (spec.md "Code Changes Required" - Change 3)

**Acceptance Criteria:**
- [ ] IDENTICAL changes to Task 2 (consistency between serial and parallel)
- [ ] Creates projected_mgr and actual_mgr
- [ ] Checks both paths exist
- [ ] Gets projections from projected_mgr.players
- [ ] Gets actuals from actual_mgr.players
- [ ] Matches by player ID
- [ ] Cleans up both managers

**Implementation Location:**
- File: `simulation/accuracy/ParallelAccuracyRunner.py`
- Method: Week calculation method (find equivalent to get_accuracy_for_week)
- Lines: Find method location

**Dependencies:**
- Requires: Task 3 complete (_load_season_data in ParallelAccuracyRunner)

**Tests:**
- Integration test: Verify parallel and serial produce same results

---

### Task 5: Update Docstrings

**Requirement:** Explain WHY two folders needed (spec.md Implementation Checklist Phase 1)

**Acceptance Criteria:**
- [ ] _load_season_data() docstring explains point-in-time data model
- [ ] Docstring mentions: week_N has actuals for weeks 1 to N-1 only
- [ ] Docstring mentions: week N actuals appear in week_N+1 folder
- [ ] get_accuracy_for_week() docstring mentions two PlayerManager instances
- [ ] Code comments explain: "week_N+1 has actual_points[N-1] populated (week N complete)"

**Implementation Location:**
- Files: AccuracySimulationManager.py and ParallelAccuracyRunner.py
- Methods: _load_season_data(), get_accuracy_for_week() (or equivalent)

**Dependencies:**
- After Tasks 1-4 (update docstrings after code changes)

**Tests:**
- N/A (documentation only)

---

## Phase 2: Testing

### Task 6: Unit Test - _load_season_data Returns Two Folders

**Requirement:** Verify method returns correct folder paths (spec.md Implementation Checklist Phase 2)

**Acceptance Criteria:**
- [ ] Test name: `test_load_season_data_returns_two_folders()`
- [ ] Test file: `tests/simulation/accuracy/test_accuracy_simulation_manager.py`
- [ ] Creates mock season_path with week_01 and week_02 folders
- [ ] Calls `_load_season_data(season_path, 1)`
- [ ] Asserts returns tuple: (week_01_path, week_02_path)
- [ ] Verifies projected_folder points to week_01
- [ ] Verifies actual_folder points to week_02
- [ ] Tests week 17: Returns (week_17_path, week_18_path)
- [ ] Test passes with new implementation

**Implementation Location:**
- File: `tests/simulation/accuracy/test_accuracy_simulation_manager.py`
- Test: `test_load_season_data_returns_two_folders()`

**Dependencies:**
- Requires: Task 1 complete

**Verifies:** Task 1

---

### Task 7: Unit Test - _load_season_data Handles Missing Folder

**Requirement:** Verify graceful handling when week_N+1 folder missing (spec.md Implementation Checklist Phase 2)

**Acceptance Criteria:**
- [ ] Test name: `test_load_season_data_handles_missing_actual_folder()`
- [ ] Creates mock season_path with week_18 but NO week_19
- [ ] Calls `_load_season_data(season_path, 18)`
- [ ] Asserts returns (None, None)
- [ ] Verifies warning logged: "Actual folder not found"
- [ ] Verifies no exception raised
- [ ] Tests projected_folder missing: also returns (None, None)

**Implementation Location:**
- File: `tests/simulation/accuracy/test_accuracy_simulation_manager.py`
- Test: `test_load_season_data_handles_missing_actual_folder()`

**Dependencies:**
- Requires: Task 1 complete

**Verifies:** Task 1 error handling

---

### Task 8: Unit Test - get_accuracy Uses Correct Folders

**Requirement:** Verify two PlayerManagers created from correct folders (spec.md Implementation Checklist Phase 2)

**Acceptance Criteria:**
- [ ] Test name: `test_get_accuracy_uses_correct_folders()`
- [ ] Mocks `_create_player_manager()` to track calls
- [ ] Calls `get_accuracy_for_week()` for week 1
- [ ] Asserts `_create_player_manager` called twice:
  - First call with week_01_path (projected_mgr)
  - Second call with week_02_path (actual_mgr)
- [ ] Verifies both managers cleaned up (cleanup called twice)
- [ ] Test passes with new implementation

**Implementation Location:**
- File: `tests/simulation/accuracy/test_accuracy_simulation_manager.py`
- Test: `test_get_accuracy_uses_correct_folders()`

**Dependencies:**
- Requires: Task 2 complete

**Verifies:** Task 2

---

### Task 9: Integration Test - Week 1 Accuracy with Real Data

**Requirement:** Verify week 1 accuracy uses real actuals (not 0.0) (spec.md Implementation Checklist Phase 2)

**Acceptance Criteria:**
- [ ] Test name: `test_week_1_accuracy_with_real_data()`
- [ ] Test file: `tests/simulation/accuracy/integration/test_accuracy_end_to_end.py`
- [ ] Runs accuracy calculation for season 2021, week 1
- [ ] Verifies actual_points are NON-ZERO (not all 0.0)
- [ ] Counts non-zero actuals: >50% of players have non-zero
- [ ] Verifies MAE is realistic: 3-8 range for QB position
- [ ] Verifies variance > 0 (not all identical)
- [ ] Test FAILS with old code (would get all 0.0)
- [ ] Test PASSES with new code (gets real values from week_02)

**Implementation Location:**
- File: `tests/simulation/accuracy/integration/test_accuracy_end_to_end.py`
- Test: `test_week_1_accuracy_with_real_data()`

**Dependencies:**
- Requires: Tasks 1-2 complete

**Verifies:** Tasks 1-2 end-to-end

---

### Task 10: Integration Test - Week 17 Uses Week 18 Folder

**Requirement:** Verify week 17 specifically uses week_18 for actuals (spec.md Implementation Checklist Phase 2 + Epic requirement)

**Acceptance Criteria:**
- [ ] Test name: `test_week_17_uses_week_18_folder()`
- [ ] Runs accuracy calculation for season 2021, week 17
- [ ] Mocks `_load_season_data()` to verify it's called with week_num=17
- [ ] Verifies method returns (week_17_path, week_18_path)
- [ ] Verifies actual_points come from week_18 folder
- [ ] Verifies week 17 actuals are non-zero (not 0.0)
- [ ] Test explicitly verifies epic requirement (line 8)

**Implementation Location:**
- File: `tests/simulation/accuracy/integration/test_accuracy_end_to_end.py`
- Test: `test_week_17_uses_week_18_folder()`

**Dependencies:**
- Requires: Tasks 1-2 complete

**Verifies:** Epic requirement (week 17/18 pattern)

---

### Task 11: Integration Test - All Weeks Have Realistic MAE

**Requirement:** Verify ALL weeks 1-17 produce realistic accuracy results (spec.md Implementation Checklist Phase 2)

**Acceptance Criteria:**
- [ ] Test name: `test_all_weeks_have_realistic_mae()`
- [ ] Runs accuracy calculation for season 2021, weeks 1-17
- [ ] For EACH week, verifies:
  - >50% of players have non-zero actuals (not all 0.0)
  - MAE is in realistic range (2-10 for NFL data)
  - Variance > 0 (not all identical values)
  - Zero percentage <90% (AUTOMATIC FAIL if >=90%)
- [ ] Logs results per week for debugging
- [ ] Test FAILS with old code (all weeks would have 0.0)
- [ ] Test PASSES with new code (all weeks have real actuals)

**Implementation Location:**
- File: `tests/simulation/accuracy/integration/test_accuracy_end_to_end.py`
- Test: `test_all_weeks_have_realistic_mae()`

**Dependencies:**
- Requires: Tasks 1-2 complete

**Verifies:** Solution works for ALL weeks (not just week 1 or 17)

---

### Task 12: Run All Existing Tests

**Requirement:** Verify no regressions (spec.md Implementation Checklist Phase 2)

**Acceptance Criteria:**
- [ ] Command run: `python tests/run_all_tests.py`
- [ ] ALL tests pass: 2463/2463 (100% pass rate)
- [ ] No new failures introduced
- [ ] Exit code: 0 (success)
- [ ] If any failures: Fix before proceeding

**Implementation Location:**
- Command line: `python tests/run_all_tests.py`

**Dependencies:**
- Requires: Tasks 1-11 complete (all code changes and new tests)

**Verifies:** No regressions introduced

---

## Phase 3: Smoke Testing (Enhanced with Statistical Sanity Checks)

### Task 13: Smoke Test Part 1 - Import Test

**Requirement:** Verify modules import without errors (spec.md Implementation Checklist Phase 3)

**Acceptance Criteria:**
- [ ] Command run: `python -c "from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager"`
- [ ] No ImportError raised
- [ ] Command run: `python -c "from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner"`
- [ ] No ImportError raised
- [ ] Both imports succeed

**Implementation Location:**
- Command line imports

**Dependencies:**
- Requires: Tasks 1-5 complete (code changes)

**Verifies:** No syntax errors, imports work

---

### Task 14: Smoke Test Part 3 - E2E with Statistical Sanity Checks

**Requirement:** Verify end-to-end execution with enhanced statistical validation (spec.md Implementation Checklist Phase 3 + Lessons Learned Strategy 3)

**Acceptance Criteria:**
- [ ] **Data Source Verification:**
  - Load week_01/qb_data.json: actual_points[0] = 0.0 ✓
  - Load week_02/qb_data.json: actual_points[0] = 33.6 (non-zero) ✓
  - Confirms data model understanding
- [ ] **Run Accuracy Calculation:**
  - Execute: `run_accuracy_simulation(season=2021, start_week=1, end_week=1)`
  - No exceptions raised
  - Result object returned
- [ ] **Statistical Sanity Check 1 - Zero Percentage:**
  - Count zero values in actual_points used
  - Calculate: `zero_pct = (zero_count / total) * 100`
  - If zero_pct > 90%: AUTOMATIC FAIL (bug not fixed)
  - If zero_pct <= 90%: PASS
- [ ] **Statistical Sanity Check 2 - Variance:**
  - Calculate: `stddev = statistics.stdev(actual_points)`
  - If stddev == 0: FAIL (all values identical - bug)
  - If stddev > 0: PASS
- [ ] **Statistical Sanity Check 3 - Realistic MAE:**
  - Extract: `mae = result.overall_mae`
  - If mae < 1.0: WARNING (too low - investigate)
  - If mae > 15.0: WARNING (too high - investigate)
  - If 3.0 <= mae <= 8.0: PASS (realistic NFL range)
- [ ] **Statistical Sanity Check 4 - Non-Zero Count:**
  - Count: `non_zero = total - zero_count`
  - If non_zero == 0: FAIL (ZERO players have non-zero - bug)
  - If non_zero > 0: PASS
- [ ] **Critical Question Checklist:**
  - "Are output values statistically realistic?" ✓
  - "If I saw '(0 have non-zero points)' would I mark PASS?" NO - AUTOMATIC FAIL ✓
  - "Does MAE fall in expected range?" ✓
  - "If this ran in production, would users trust results?" ✓

**Implementation Location:**
- Script: `smoke_test_bug_fix_verification.py` (new file)
- Based on template in spec.md "Smoke Testing" section

**Dependencies:**
- Requires: Tasks 1-12 complete (all tests passing)

**Verifies:**
- End-to-end functionality
- Statistical sanity (prevents "0.0 acceptance" failure)
- Lessons Learned Strategy 3 applied

---

## Phase 4: Cross-Epic Verification

### Task 15: Verify Feature 01 Tests Still Pass

**Requirement:** Ensure bug fix doesn't affect WinRateSimulationManager (spec.md Implementation Checklist Phase 4 + User requirement)

**Acceptance Criteria:**
- [ ] Run Feature 01 tests: `python -m pytest tests/simulation/win_rate/ -v`
- [ ] ALL Feature 01 tests pass (no regressions)
- [ ] WinRateSimulationManager unchanged (different files)
- [ ] No unintended interactions between features

**Implementation Location:**
- Command line: pytest for win_rate tests

**Dependencies:**
- Requires: Task 12 complete (all tests passing)

**Verifies:** Bug fix isolated to accuracy sim (doesn't break feature 01)

---

### Task 16: Compare with Epic Notes

**Requirement:** Verify ALL epic requirements met (spec.md Implementation Checklist Phase 4 + User requirement: "verify ALL changes against notes")

**Acceptance Criteria:**
- [ ] Epic notes line 1: Update to use JSON files ✓ (feature_01 + feature_02 + bugfix)
- [ ] Epic notes line 3-6: Load JSON from week folders ✓
- [ ] Epic notes line 6: Handle new fields (drafted_by, locked, projected_points, actual_points) ✓
- [ ] Epic notes line 8: Week_N + week_N+1 pattern ✓ (THIS BUG FIX)
- [ ] ALL epic requirements verified as complete
- [ ] Documented in checklist: "Epic requirements ALL met ✓"

**Implementation Location:**
- Document verification in `feature_02/README.md` or `bugfix_high_week_offset_logic/lessons_learned.md`

**Dependencies:**
- Requires: Task 14 complete (smoke testing passed)

**Verifies:** Epic requirements complete

---

### Task 17: Compare with Original Simulation Code

**Requirement:** Verify only data loading changed (not algorithms) (spec.md Implementation Checklist Phase 4 + User requirement)

**Acceptance Criteria:**
- [ ] Read pre-epic AccuracySimulationManager.py (before JSON changes)
- [ ] Identify original MAE calculation algorithm
- [ ] Verify: MAE calculation logic UNCHANGED (same algorithm)
- [ ] Verify: Ranking metrics calculation UNCHANGED
- [ ] Only changes: Data loading (CSV → JSON, single folder → two folders)
- [ ] Document: "Algorithms unchanged, only data loading modified ✓"

**Implementation Location:**
- Git diff or file comparison
- Document findings in lessons_learned.md

**Dependencies:**
- Requires: Tasks 1-5 complete (code changes)

**Verifies:** Calculation logic preserved (only data source changed)

---

### Task 18: Verify Week 17 Specifically

**Requirement:** Verify week 17 uses week_18 folder (epic requirement + spec.md Implementation Checklist Phase 4)

**Acceptance Criteria:**
- [ ] Re-run Task 10 test: `test_week_17_uses_week_18_folder()` ✓
- [ ] Manually verify: Run accuracy for week 17, check actual_points source
- [ ] Confirm: week_17 folder used for projections
- [ ] Confirm: week_18 folder used for actuals
- [ ] Epic requirement (line 8) explicitly verified
- [ ] Document: "Week 17/18 pattern verified ✓"

**Implementation Location:**
- Verification test + manual check

**Dependencies:**
- Requires: Task 10 complete

**Verifies:** Epic line 8 requirement

---

## Phase 5: Documentation

### Task 19: Update code_changes.md

**Requirement:** Document all code modifications (spec.md Implementation Checklist Phase 5)

**Acceptance Criteria:**
- [ ] File created: `bugfix_high_week_offset_logic/code_changes.md`
- [ ] Documents Task 1: _load_season_data() changes (before/after code)
- [ ] Documents Task 2: get_accuracy_for_week() changes (before/after code)
- [ ] Documents Tasks 3-4: ParallelAccuracyRunner changes
- [ ] Documents Task 5: Docstring updates
- [ ] Includes file paths and line numbers
- [ ] Includes rationale for each change

**Implementation Location:**
- File: `bugfix_high_week_offset_logic/code_changes.md`

**Dependencies:**
- Requires: Tasks 1-5 complete

**Verifies:** Code changes documented

---

### Task 20: Update implementation_checklist.md

**Requirement:** Track continuous spec verification (spec.md Implementation Checklist Phase 5)

**Acceptance Criteria:**
- [ ] File created: `bugfix_high_week_offset_logic/implementation_checklist.md`
- [ ] Maps each code change to spec requirement
- [ ] Verifies all spec requirements implemented
- [ ] No missing requirements
- [ ] No extra scope (only what spec says)

**Implementation Location:**
- File: `bugfix_high_week_offset_logic/implementation_checklist.md`

**Dependencies:**
- Requires: Tasks 1-18 complete

**Verifies:** Spec requirements complete

---

### Task 21: Update lessons_learned.md

**Requirement:** Document final insights (spec.md Implementation Checklist Phase 5)

**Acceptance Criteria:**
- [ ] File updated: `bugfix_high_week_offset_logic/lessons_learned.md`
- [ ] Documents what worked: Evidence-based spec, hands-on data inspection, statistical validation
- [ ] Documents any challenges during implementation
- [ ] Documents prevention strategies applied successfully
- [ ] Final summary: "All 6 prevention strategies verified in practice"

**Implementation Location:**
- File: `bugfix_high_week_offset_logic/lessons_learned.md`

**Dependencies:**
- Requires: All tasks complete

**Verifies:** Lessons learned captured

---

## Task Summary

**Total Tasks:** 21

**Phase 1 (Code Changes):** 5 tasks (Tasks 1-5)
**Phase 2 (Testing):** 7 tasks (Tasks 6-12)
**Phase 3 (Smoke Testing):** 2 tasks (Tasks 13-14)
**Phase 4 (Cross-Epic Verification):** 4 tasks (Tasks 15-18)
**Phase 5 (Documentation):** 3 tasks (Tasks 19-21)

**All tasks traced to spec.md requirements ✓**

---

## Dependencies Graph

```
Task 1 (Update _load_season_data AccuracySimulationManager)
  ├─> Task 2 (Update get_accuracy_for_week)
  ├─> Task 6 (Unit test: returns two folders)
  └─> Task 7 (Unit test: handles missing folder)

Task 2 (Update get_accuracy_for_week)
  ├─> Task 8 (Unit test: uses correct folders)
  ├─> Task 9 (Integration test: week 1 real data)
  ├─> Task 10 (Integration test: week 17 uses week_18)
  └─> Task 11 (Integration test: all weeks realistic)

Task 3 (Update _load_season_data ParallelAccuracyRunner)
  └─> Task 4 (Update week calculation ParallelAccuracyRunner)

Tasks 1-4 (Code changes)
  └─> Task 5 (Update docstrings)

Tasks 1-11 (Code + Tests)
  └─> Task 12 (Run all tests)

Task 12 (All tests pass)
  └─> Task 13 (Smoke test part 1: imports)
  └─> Task 14 (Smoke test part 3: E2E with statistical checks)

Task 14 (Smoke testing passed)
  └─> Task 15 (Verify Feature 01 tests)
  └─> Task 16 (Compare with epic notes)
  └─> Task 17 (Compare with original code)
  └─> Task 18 (Verify week 17)

Tasks 1-5 (Code changes)
  └─> Task 19 (Update code_changes.md)

Tasks 1-18 (All implementation complete)
  └─> Task 20 (Update implementation_checklist.md)
  └─> Task 21 (Update lessons_learned.md)
```

---

## Implementation Phasing (Stage 5a Round 3 - Iteration 17)

**Purpose:** Break implementation into phases for incremental validation

**Phase 1: Core Data Loading (Foundation)**
- **Tasks:** 1, 6, 7
- **Focus:** Update _load_season_data() in AccuracySimulationManager + unit tests
- **Tests:** test_load_season_data_returns_two_folders(), test_load_season_data_handles_missing_actual_folder()
- **Checkpoint:** Both unit tests pass
- **Why:** Foundation must be solid before building get_accuracy_for_week()

**Phase 2: Main Calculation Update**
- **Tasks:** 2, 8, 9, 10, 11
- **Focus:** Update get_accuracy_for_week() in AccuracySimulationManager + integration tests
- **Tests:** test_get_accuracy_uses_correct_folders(), test_week_1_accuracy_with_real_data(), test_week_17_uses_week_18_folder(), test_all_weeks_have_realistic_mae()
- **Checkpoint:** All AccuracySimulationManager tests pass, statistical validation shows realistic MAE
- **Why:** Core fix for serial implementation, must work before parallel

**Phase 3: Parallel Implementation**
- **Tasks:** 3, 4
- **Focus:** Update ParallelAccuracyRunner (identical changes to Phase 1-2)
- **Tests:** Parallel-specific unit/integration tests (mirror Phase 1-2 tests)
- **Checkpoint:** Parallel tests pass, serial and parallel produce identical results
- **Why:** Maintain consistency between serial/parallel implementations

**Phase 4: Documentation & Full Testing**
- **Tasks:** 5, 12
- **Focus:** Update docstrings + run full test suite
- **Tests:** ALL 2463 tests (100% pass required)
- **Checkpoint:** python tests/run_all_tests.py exits with code 0
- **Why:** Verify no regressions before smoke testing

**Phase 5: Smoke Testing & Cross-Epic Verification**
- **Tasks:** 13, 14, 15, 16, 17, 18
- **Focus:** End-to-end validation + statistical sanity checks + cross-epic verification
- **Tests:** Smoke tests (imports, E2E), Feature 01 tests, epic requirements verification
- **Checkpoint:** All smoke tests pass, zero_pct <90%, variance >0, MAE realistic (3-8)
- **Why:** Statistical validation prevents "0.0 acceptance" failure, cross-epic verification meets user requirement

**Phase 6: Final Documentation**
- **Tasks:** 19, 20, 21
- **Focus:** Document code changes, implementation checklist, lessons learned update
- **Tests:** N/A (documentation only)
- **Checkpoint:** All documentation files complete and accurate
- **Why:** Capture knowledge, support future maintenance

**Critical Rules:**
- ✅ Must complete Phase N before starting Phase N+1
- ✅ All tests must pass before proceeding to next phase
- ✅ If any test fails: Fix immediately, re-run phase checkpoint
- ✅ Phase 5 statistical checks are MANDATORY GATES (cannot skip)

**Phase Boundaries (Mini-QC Checkpoints):**
- After Phase 1: Verify _load_season_data() unit tests pass
- After Phase 2: Verify get_accuracy_for_week() integration tests show realistic MAE
- After Phase 3: Verify parallel implementation matches serial results
- After Phase 4: Verify 100% test pass rate (2463/2463)
- After Phase 5: Verify statistical sanity (zero_pct <90%, MAE 3-8)
- After Phase 6: Verify all documentation complete

---

## Rollback Strategy (Stage 5a Round 3 - Iteration 18)

**Purpose:** Define how to rollback if bug fix introduces critical issues

**Rollback Approach: Git Revert**

**If critical bug discovered after commit:**

**Option 1: Immediate Git Revert (Recommended)**
1. Identify commit hash: `git log --oneline | grep "fix/KAI-3"`
2. Revert commit: `git revert <commit_hash>`
3. Verify accuracy simulation: Run Task 14 smoke test (should fail with old bug)
4. Push revert: `git push origin epic/KAI-3`
5. **Result:** Code reverted to pre-bugfix state (week_N used for both projected and actual)
6. **Downtime:** ~2 minutes (one git command)

**Option 2: Manual Code Restore (If git revert has conflicts)**
1. Restore AccuracySimulationManager.py:
   - Revert `_load_season_data()` to return `(week_folder, week_folder)`
   - Revert `get_accuracy_for_week()` to use single PlayerManager
2. Restore ParallelAccuracyRunner.py:
   - Revert `_load_season_data()` to return single folder
   - Revert week calculation to use single PlayerManager
3. Run tests: `python tests/run_all_tests.py`
4. Commit: `fix/KAI-3: Rollback week offset bug fix due to {issue}`
5. **Result:** Manual restoration to pre-bugfix state
6. **Downtime:** ~10 minutes (manual editing, testing)

**Verification After Rollback:**
1. **Confirm rollback worked:**
   - Run smoke test: Should see "(0 have non-zero points)" (old bug behavior)
   - MAE should be near 0 (projections vs 0.0 actuals)
   - This confirms we're back to pre-bugfix state

2. **Verify no new issues introduced by rollback:**
   - Run full test suite: `python tests/run_all_tests.py`
   - All tests should pass (pre-bugfix state was tested)
   - Feature 01 tests should still pass (no interaction)

3. **Document rollback:**
   - Update README.md: Status = ROLLED BACK
   - Document reason: What critical issue triggered rollback
   - Document investigation plan: How to fix the issue

**Rollback Decision Criteria:**

| Issue Severity | Rollback Action | Timeline |
|----------------|-----------------|----------|
| Critical bug (crashes, data corruption) | Immediate git revert | < 5 minutes |
| Incorrect calculations (MAE wrong) | Investigate first, revert if unfixable quickly | < 30 minutes |
| Performance issue (10x slowdown) | Investigate first, may not need rollback | < 1 hour |
| Edge case issue (week 18 missing) | Fix forward (no rollback needed) | As needed |

**Testing Rollback Procedure (Pre-Implementation Verification):**

Before implementing bug fix, verify rollback works:
1. **Test git revert simulation:**
   - Create test commit on branch
   - Practice: `git revert HEAD`
   - Verify: Code restored correctly
   - Undo revert: `git revert HEAD` (revert the revert)
   - **Result:** Confident we can rollback if needed

2. **Document rollback contact:**
   - User should be notified if rollback needed
   - Document in lessons_learned.md: What to do if rollback necessary

**No Feature Toggle Needed:**
- This is a bug fix (not a new feature)
- Code either has bug (week_N for both) or doesn't (week_N + week_N+1)
- No intermediate state makes sense
- Git revert is simplest and safest

**Rollback Success Criteria:**
- ✅ Code reverted to pre-bugfix state
- ✅ Old bug reproduced (confirms rollback worked)
- ✅ All tests pass
- ✅ No new issues introduced
- ✅ User notified and rollback documented

---

## Algorithm Traceability Matrix (FINAL - Stage 5a Round 3 - Iteration 19)

**Purpose:** Final verification that all algorithms from spec are traced to implementation

**Total Algorithms Traced:** 15 (unchanged from Rounds 1-2)

**Breakdown:**
- Core algorithms (from spec): 5
- Error handling algorithms: 5
- Edge case algorithms: 5

**Verification:**
- ✅ All algorithms from spec.md mapped to TODO tasks
- ✅ All TODO tasks reference spec algorithms
- ✅ No implementation without spec algorithm
- ✅ All error handling algorithms included
- ✅ All edge case algorithms included
- ✅ Coverage: 100% of spec + comprehensive error handling

**Final Algorithm Traceability Matrix:**

| # | Algorithm (from spec.md) | Spec Section | Implementation Location | TODO Task | Verified |
|---|--------------------------|--------------|-------------------------|-----------|----------|
| 1 | Load two week folders (week_N, week_N+1) | Code Changes - Change 1 | AccuracySimulationManager._load_season_data():293-313 | Task 1 | ✅ |
| 2 | Check both folders exist | Code Changes - Change 1 | AccuracySimulationManager._load_season_data():300-305 | Task 1 | ✅ |
| 3 | Create two PlayerManager instances | Code Changes - Change 2 | AccuracySimulationManager.get_accuracy_for_week():420-425 | Task 2 | ✅ |
| 4 | Get projections from week_N PlayerManager | Code Changes - Change 2 | AccuracySimulationManager.get_accuracy_for_week():430-435 | Task 2 | ✅ |
| 5 | Get actuals from week_N+1 PlayerManager | Code Changes - Change 2 | AccuracySimulationManager.get_accuracy_for_week():440-450 | Task 2 | ✅ |
| 6 | Match players by ID between folders | Code Changes - Change 2 | AccuracySimulationManager.get_accuracy_for_week():445 | Task 2 | ✅ |
| 7 | Cleanup both PlayerManagers | Code Changes - Change 2 | AccuracySimulationManager.get_accuracy_for_week():460-465 | Task 2 | ✅ |
| 8 | Apply identical fix to ParallelAccuracyRunner | Code Changes - Change 3 | ParallelAccuracyRunner._load_season_data():195 | Task 3 | ✅ |
| 9 | Apply identical fix to parallel week calc | Code Changes - Change 3 | ParallelAccuracyRunner week calculation | Task 4 | ✅ |
| 10 | Handle missing week_N+1 folder | Edge Cases | AccuracySimulationManager._load_season_data():310 | Task 1 | ✅ |
| 11 | Log warning if folder missing | Edge Cases | AccuracySimulationManager._load_season_data():308-312 | Task 1 | ✅ |
| 12 | Return (None, None) if folder missing | Edge Cases | AccuracySimulationManager._load_season_data():313 | Task 1 | ✅ |
| 13 | Skip week if both folders not available | Edge Cases | AccuracySimulationManager.get_accuracy_for_week():417 | Task 2 | ✅ |
| 14 | Extract actual_points[week_num - 1] from week_N+1 | Data Model | AccuracySimulationManager.get_accuracy_for_week():448 | Task 2 | ✅ |
| 15 | Document WHY two folders needed (point-in-time model) | Documentation | Docstrings in _load_season_data(), get_accuracy_for_week() | Task 5 | ✅ |

**Changes from Previous Rounds:**
- Round 1 (Iteration 4): Created matrix with 15 algorithms
- Round 2 (Iteration 11): Re-verified all 15 algorithms, no changes
- Round 3 (Iteration 19): **FINAL verification** - all 15 algorithms still correctly traced

**Verification Results:**
- ✅ All 15 algorithms from spec.md traced to exact code locations
- ✅ Every algorithm has corresponding TODO task
- ✅ Every TODO task references at least one algorithm
- ✅ No orphan algorithms (spec mentions but not implemented)
- ✅ No orphan implementations (code without spec algorithm)
- ✅ Error handling complete (missing folders, player ID mismatches)
- ✅ Edge cases complete (week 18 → week 19 missing, etc.)

**Cross-Reference Validation:**
- Spec.md "Code Changes Required" section: 3 changes → Algorithms 1-9 ✅
- Spec.md "Edge Cases" section: 10 edge cases → Algorithms 10-13 + Task 1,2 error handling ✅
- Spec.md "Data Model Investigation" section: Point-in-time model → Algorithm 14, 15 ✅

**✅ FINAL VERIFICATION: ALL 15 ALGORITHMS TRACED**

**Last chance issues check:**
- ❌ No unmapped algorithms found
- ❌ No orphan implementations found
- ❌ No missing error handling found
- ❌ No undefined edge cases found

**Confidence Level:** HIGH - All algorithms comprehensively traced

---

## Performance Considerations (Stage 5a Round 3 - Iteration 20)

**Purpose:** Assess performance impact and optimization needs

**Baseline Performance (current BROKEN code):**
- PlayerManagers per week: 1
- JSON loading per week: 5 files (qb, rb, wr, te, k) × 1 folder = 5 loads
- Player object creation: ~500 players × 1 = 500 objects
- Memory footprint: ~500 player objects
- Typical accuracy simulation: 17 weeks
- Total PlayerManagers: 17 (one per week)

**Estimated Performance (with bug fix):**
- PlayerManagers per week: 2 (projected_mgr + actual_mgr)
- JSON loading per week: 5 files × 2 folders = 10 loads
- Player object creation: ~500 players × 2 = 1000 objects per week
- Memory footprint: ~1000 player objects (500 from week_N, 500 from week_N+1)
- Typical accuracy simulation: 17 weeks
- Total PlayerManagers: 34 (two per week)

**Performance Impact:**
- JSON file reads: 2x increase (5 → 10 per week)
- PlayerManager creation: 2x increase (1 → 2 per week)
- Player object creation: 2x increase (500 → 1000 per week)
- Memory usage: 2x increase (500 → 1000 objects in memory per week)
- **Overall impact: ~2x slower per week**

**Estimated Timing:**
- Current (BROKEN): ~2s per week × 17 weeks = 34s total
- With fix: ~4s per week × 17 weeks = 68s total
- **Additional time: +34s (100% increase)**

**Is This Acceptable?**

✅ **YES - Performance impact is acceptable because:**

1. **Accuracy simulation runs infrequently:**
   - Not part of interactive workflows (draft mode, optimizer)
   - Typically run once per season for validation
   - +34s for a validation tool is negligible

2. **Correctness > Performance:**
   - Current code produces GARBAGE output (all actuals = 0.0)
   - 2x slower but CORRECT is better than fast but WRONG
   - This is a bug fix (not optional optimization)

3. **Small absolute time increase:**
   - +34s for 17-week simulation
   - ~+2s per week
   - Still completes in ~1 minute (acceptable for batch job)

4. **No user-facing impact:**
   - Accuracy simulation is internal validation tool
   - Not used during live draft or roster management
   - Users won't notice the delay

**Bottleneck Analysis:**

Primary bottleneck: **JSON file I/O**
- Reading 10 files per week instead of 5
- Each file: ~50-200 KB (small)
- Total I/O: ~5 MB per week × 17 = 85 MB
- SSD read time: ~100ms total (negligible)

Secondary bottleneck: **Player object creation**
- Creating 1000 objects per week instead of 500
- Python object creation: ~1µs per object
- Total: 1000 × 1µs = 1ms (negligible)

**Actual bottleneck: PlayerManager initialization**
- Parsing JSON: ~50ms per file × 5 files = 250ms
- Creating Player objects: ~50ms
- Total per PlayerManager: ~300ms
- Two PlayerManagers: ~600ms per week
- **This is the real cost: 2x PlayerManager initialization**

**Optimization Opportunities:**

**Option 1: Cache PlayerManager instances**
- Pro: Reuse week_N+1 as week_N in next iteration
- Con: Complex state management, potential bugs
- Impact: Could save ~50% (reuse half the managers)
- **Decision: NOT WORTH IT** - Complexity outweighs benefit

**Option 2: Lazy load player data**
- Pro: Only load players we actually need (QB only, not all positions)
- Con: Requires refactoring PlayerManager
- Impact: Could save ~80% (if only loading 1 position)
- **Decision: OUT OF SCOPE** - This is a bug fix, not a refactor

**Option 3: Parallel folder loading**
- Pro: Load week_N and week_N+1 simultaneously
- Con: Requires threading/async
- Impact: Could save ~40% (parallel I/O)
- **Decision: NOT WORTH IT** - Adds complexity for minimal gain

**Optimization Decision:**

❌ **NO optimizations needed**

**Rationale:**
1. Performance impact is acceptable (2x on infrequent validation tool)
2. All optimization options add complexity
3. Bug fix should be simple and correct (not complex and optimized)
4. Premature optimization is root of all evil
5. If performance becomes issue later, can optimize then

**Performance Testing Plan:**

Include in integration tests (Task 11):
- **Task 11 includes:** `test_all_weeks_have_realistic_mae()`
- Runs accuracy for weeks 1-17 (full simulation)
- Measure total execution time
- **Acceptance criteria:**
  - Total time: <120 seconds (2 minutes)
  - If exceeds: Investigate bottleneck
  - If within: Performance is acceptable

**Monitoring Strategy:**

During smoke testing (Task 14):
- Measure execution time for 1 week
- Extrapolate to 17 weeks
- Log timing: "Week 1 accuracy: {time}s"
- **Red flag:** If >10s per week (investigate)
- **Green flag:** If <5s per week (acceptable)

**Performance Impact Summary:**

| Metric | Current (BROKEN) | With Fix | Change | Acceptable? |
|--------|------------------|----------|--------|-------------|
| PlayerManagers/week | 1 | 2 | +100% | ✅ Yes |
| JSON reads/week | 5 | 10 | +100% | ✅ Yes |
| Time/week | ~2s | ~4s | +100% | ✅ Yes |
| Total time (17 weeks) | ~34s | ~68s | +34s | ✅ Yes |
| Memory usage | ~500 objects | ~1000 objects | +100% | ✅ Yes |

**✅ CONCLUSION: 2x performance impact is ACCEPTABLE for this bug fix**

---

## Mock Audit & Integration Test Plan (Stage 5a Round 3 - Iteration 21)

**Purpose:** Verify mocks match real interfaces, plan integration tests with real objects

**⚠️ CRITICAL:** Unit tests with wrong mocks can pass while hiding bugs

---

### Mock Audit

**Mock 1: AccuracySimulationManager._create_player_manager()**

**Used in tests:** Task 8 (`test_get_accuracy_uses_correct_folders()`)

**Mock definition (planned):**
```python
mock_projected_mgr = MagicMock()
mock_actual_mgr = MagicMock()
mock_create = MagicMock(side_effect=[mock_projected_mgr, mock_actual_mgr])
```

**Real interface (VERIFIED from source):**
```python
# simulation/accuracy/AccuracySimulationManager.py:315
def _create_player_manager(
    self,
    config_dict: Dict[str, Any],
    week_folder: Path,
    season_path: Path
) -> PlayerManager:
    """Create and return a PlayerManager instance."""
```

**Parameters:**
- Mock accepts: config_dict, week_folder, season_path (via side_effect tracking) ✅
- Real accepts: config_dict, week_folder, season_path ✅
- ✅ MATCH

**Return value:**
- Mock returns: MagicMock (simulates PlayerManager) ✅
- Real returns: PlayerManager instance ✅
- ✅ ACCEPTABLE for unit test

**Verification:** ✅ PASSED - Mock signature matches real interface

---

**Mock 2: AccuracySimulationManager._cleanup_player_manager()**

**Used in tests:** Task 8 (`test_get_accuracy_uses_correct_folders()`)

**Mock definition (planned):**
```python
mock_cleanup = MagicMock()
```

**Real interface (VERIFIED from source):**
```python
# simulation/accuracy/AccuracySimulationManager.py:382
def _cleanup_player_manager(self, manager: PlayerManager) -> None:
    """Cleanup PlayerManager resources."""
```

**Parameters:**
- Mock accepts: ANY (MagicMock default) ⚠️
- Real accepts: manager (PlayerManager) ⚠️
- ⚠️ LOOSE MATCH - Mock should validate parameter type

**Return value:**
- Mock returns: None ✅
- Real returns: None ✅
- ✅ MATCH

**Fix:** Add parameter validation to mock
```python
def mock_cleanup(manager):
    assert hasattr(manager, 'players'), "manager must be PlayerManager-like"
mock_cleanup_player_manager.side_effect = mock_cleanup
```

**Verification:** ✅ FIXED - Mock now validates parameter

---

**Mock 3: Path.exists()**

**Used in tests:** Task 7 (`test_load_season_data_handles_missing_actual_folder()`)

**Mock definition (planned):**
```python
with patch('pathlib.Path.exists') as mock_exists:
    mock_exists.side_effect = [True, False]  # projected exists, actual missing
```

**Real interface (VERIFIED from Python stdlib):**
```python
# pathlib.Path.exists() -> bool
```

**Parameters:**
- Mock accepts: self (Path object)
- Real accepts: self (Path object)
- ✅ MATCH

**Return value:**
- Mock returns: bool (via side_effect)
- Real returns: bool
- ✅ MATCH

**Verification:** ✅ PASSED - Mock signature matches real interface

---

### Mock Summary

**Total Mocks:** 3
**Mocks Verified:** 3/3
**Issues Found:** 1 (Mock 2 - fixed with parameter validation)
**Issues Fixed:** 1/1

**✅ All mocks match real interfaces (after fixes)**

---

### Integration Test Plan (No Mocks)

**Philosophy:** Integration tests use REAL objects to catch interface mismatches

**Integration Test 1: test_week_1_accuracy_with_real_data() (Task 9)**

**Purpose:** Verify week 1 accuracy uses REAL data (not mocked)

**Setup:**
- Use REAL AccuracySimulationManager (not mock)
- Use REAL season data (simulation/sim_data/2021/)
- Use REAL PlayerManager instances
- Use REAL JSON files

**Steps:**
1. Initialize real AccuracySimulationManager
2. Run get_accuracy_for_week(season_path="simulation/sim_data/2021", week_num=1)
3. Verify actual_points are NON-ZERO (>50% have non-zero values)
4. Verify MAE is realistic (3-8 range for QB)

**Why no mocks:** Proves bug fix works with REAL PlayerManager interface

**Expected Duration:** ~500ms (acceptable for integration test)

---

**Integration Test 2: test_week_17_uses_week_18_folder() (Task 10)**

**Purpose:** Verify week 17 specifically uses week_18 for actuals

**Setup:**
- Use REAL AccuracySimulationManager
- Use REAL season data (simulation/sim_data/2021/)
- **Instrument _load_season_data()** to verify folder paths

**Steps:**
1. Spy on _load_season_data() calls (not mock, just track)
2. Run get_accuracy_for_week(week_num=17)
3. Verify _load_season_data returned (week_17_path, week_18_path)
4. Verify actual_points came from week_18

**Why no mocks:** Verifies epic requirement (line 8) with real data

---

**Integration Test 3: test_all_weeks_have_realistic_mae() (Task 11)**

**Purpose:** Full E2E test for weeks 1-17 with REAL objects

**Setup:**
- REAL AccuracySimulationManager
- REAL season data
- REAL PlayerManager instances (34 total: 2 per week × 17 weeks)

**Steps:**
1. Run accuracy simulation for weeks 1-17
2. For EACH week:
   - Verify >50% non-zero actuals
   - Verify MAE in realistic range (2-10)
   - Verify variance > 0
3. Log results per week

**Why no mocks:** Proves entire feature works end-to-end in real environment

**Expected Duration:** ~68s (17 weeks × 4s per week)

---

**Integration Test 4: test_parallel_matches_serial() (NEW - added in Iteration 21)**

**Purpose:** Verify ParallelAccuracyRunner produces same results as AccuracySimulationManager

**Setup:**
- REAL AccuracySimulationManager
- REAL ParallelAccuracyRunner
- Same season data

**Steps:**
1. Run serial accuracy: results_serial = AccuracySimulationManager.get_accuracy_for_week(week=1)
2. Run parallel accuracy: results_parallel = ParallelAccuracyRunner.run_week(week=1)
3. Compare MAE values: assert abs(results_serial.mae - results_parallel.mae) < 0.01
4. Compare rankings: assert results_serial.rankings == results_parallel.rankings

**Why no mocks:** Catches divergence between serial and parallel implementations

**Expected Duration:** ~8s (2 implementations × 4s each)

---

### Integration Test Tasks (add to TODO)

**NEW Task 22: Integration Test - Parallel Matches Serial**

**Requirement:** Verify ParallelAccuracyRunner produces same results as serial

**Acceptance Criteria:**
- [ ] Test name: `test_parallel_matches_serial()`
- [ ] Test file: `tests/simulation/accuracy/integration/test_accuracy_end_to_end.py`
- [ ] Uses REAL AccuracySimulationManager
- [ ] Uses REAL ParallelAccuracyRunner
- [ ] Compares MAE values (must match within 0.01)
- [ ] Compares rankings (must match exactly)
- [ ] No mocks used
- [ ] Test proves parallel implementation correct

**Implementation Location:**
- File: `tests/simulation/accuracy/integration/test_accuracy_end_to_end.py`
- Test: `test_parallel_matches_serial()`

**Dependencies:**
- Requires: Tasks 1-4 complete (both serial and parallel fixed)

**Verifies:** ParallelAccuracyRunner consistency with serial implementation

---

### Summary

**Mocks Audited:** 3
**Mocks Verified:** 3/3
**Mock Issues Fixed:** 1

**Integration Tests Planned:** 4 (Tasks 9, 10, 11, 22)
- Task 9: Week 1 real data (E2E with real PlayerManager)
- Task 10: Week 17 uses week_18 (epic requirement verification)
- Task 11: All weeks realistic (full 17-week E2E)
- Task 22: Parallel matches serial (consistency check)

**Real Object Usage:**
- ✅ All integration tests use REAL AccuracySimulationManager
- ✅ All integration tests use REAL PlayerManager
- ✅ All integration tests use REAL season data
- ✅ No mocks in integration tests (only in unit tests)

**✅ Mock audit complete, integration test plan comprehensive**

---

## Output Consumer Validation (Stage 5a Round 3 - Iteration 22)

**Purpose:** Verify outputs are consumable by downstream code

**Output from this bug fix:**
- AccuracySimulationManager.get_accuracy_for_week() returns accurate MAE values
- ParallelAccuracyRunner produces correct accuracy metrics
- Results now have realistic MAE (3-8 range) instead of near-zero (bug)

**Consumer Analysis:**

### Consumer 1: User/Human (Primary Consumer)

**Purpose:** Accuracy simulation is a validation tool for humans

**Usage:**
- User runs: `python run_simulation.py --mode accuracy`
- Views output: MAE metrics, ranking accuracy, projection vs actual comparison
- Uses output: Validate that league simulation parameters are realistic

**Impact of bug fix:**
- ✅ Users now see REALISTIC MAE values (3-8) instead of garbage (near 0)
- ✅ Users can trust accuracy metrics for parameter tuning
- ✅ Validation tool is now functional

**Validation:**
- Smoke test (Task 14) verifies human-readable output shows realistic values
- No code changes needed (output format unchanged)

---

### Consumer 2: Logging/Results Storage (Secondary Consumer)

**Purpose:** Results may be logged or saved for historical comparison

**Potential usage:**
- Accuracy results logged to file
- Historical tracking of projection accuracy over seasons

**Impact of bug fix:**
- ✅ Logged values will now be meaningful
- ✅ Historical comparisons will be valid
- ⚠️ Pre-bugfix logs have garbage data (MAE near 0)

**Validation:**
- Verify log output format unchanged (only values change)
- Document: "Pre-bugfix logs (before 2026-01-02) contain incorrect MAE values"

---

### Consumer 3: None - Standalone Tool

**Finding:** Accuracy simulation is a STANDALONE VALIDATION TOOL
- Not consumed by other code modules
- Not integrated into league helper workflow
- Not used by draft mode, optimizer, trade analyzer, etc.
- Output is for HUMAN validation only

**Evidence:**
- run_simulation.py is separate entry point (not imported elsewhere)
- AccuracySimulationManager is not imported by league_helper modules
- Results are displayed/logged, not passed to other code

**Implication:**
- ✅ Bug fix has NO IMPACT on other modules
- ✅ No consumer validation tests needed
- ✅ Only need to verify output format unchanged

---

### Output Format Validation

**Current output format (unchanged):**
```
Accuracy Simulation Results:
  Week 1: MAE = 5.23
  Week 2: MAE = 4.87
  ...
  Overall MAE: 5.12
```

**After bug fix (values change, format unchanged):**
```
Accuracy Simulation Results:
  Week 1: MAE = 5.23  (realistic value from week_02 actuals)
  Week 2: MAE = 4.87  (realistic value from week_03 actuals)
  ...
  Overall MAE: 5.12  (realistic overall)
```

**Validation plan:**
- ✅ Task 14 (smoke test) verifies output format
- ✅ Integration tests (Tasks 9-11) verify output values realistic
- ✅ No additional consumer validation tests needed

---

### Breaking Changes Analysis

**Question:** Does bug fix introduce breaking changes?

**Answer:** ❌ NO - No breaking changes

**Rationale:**
1. **API unchanged:**
   - Method signatures unchanged
   - Return types unchanged
   - Parameters unchanged

2. **Output format unchanged:**
   - Log format unchanged
   - Result object structure unchanged
   - Only VALUES change (not structure)

3. **No code consumers:**
   - Accuracy simulation is standalone tool
   - No other modules depend on it
   - No imports to break

**Validation:**
- ✅ Smoke test verifies no import errors
- ✅ Integration tests verify API still works
- ✅ No consumer-specific tests needed

---

### Consumer Validation Summary

**Total Consumers Identified:** 1 (Human/User)
**Code Consumers:** 0
**Breaking Changes:** 0
**Consumer Validation Tests Needed:** 0 (already covered by existing smoke/integration tests)

**Conclusion:**
✅ Bug fix has NO downstream code consumers
✅ Output format unchanged (only values corrected)
✅ Existing tests (Tasks 9-14) provide sufficient validation
✅ No additional consumer validation tests required

**Cross-reference with existing tests:**
- Task 9: Verifies realistic output values
- Task 10: Verifies epic requirement met
- Task 11: Verifies all weeks produce valid output
- Task 14: Verifies E2E execution and output format
- Task 22: Verifies parallel/serial consistency

**✅ Output consumer validation complete - no additional tests needed**

---

## Integration Gap Check (FINAL - Stage 5a Round 3 - Iteration 23)

**Purpose:** Final verification - no orphan code

**⚠️ CRITICAL:** This is the LAST chance to catch orphan methods before implementation

**Review Summary:**
- Round 1 (Iteration 7): Identified 4 modified methods, all have callers
- Round 2 (Iteration 14): Re-verified 4 methods, all still integrated
- Round 3 (Iteration 23): **FINAL verification** - all methods still integrated

---

### Final Integration Matrix

**Total Modified Methods:** 4

| # | Modified Method | File | Caller | Call Location | Round Added | Verified |
|---|----------------|------|--------|---------------|-------------|----------|
| 1 | AccuracySimulationManager._load_season_data() | AccuracySimulationManager.py:293 | get_accuracy_for_week() | Line 415 | Round 1 | ✅ |
| 2 | AccuracySimulationManager.get_accuracy_for_week() | AccuracySimulationManager.py:411 | run() | Line 250 (main loop) | Round 1 | ✅ |
| 3 | ParallelAccuracyRunner._load_season_data() | ParallelAccuracyRunner.py:195 | _run_week() | Line 225 | Round 1 | ✅ |
| 4 | ParallelAccuracyRunner._run_week() | ParallelAccuracyRunner.py:220 | run() | Line 180 (parallel execution) | Round 1 | ✅ |

**New Methods Added:** 0 (bug fix only modifies existing methods)

**Methods Deleted:** 0

---

### Integration Verification Results

**Method 1: AccuracySimulationManager._load_season_data()**
- ✅ Caller identified: AccuracySimulationManager.get_accuracy_for_week()
- ✅ Call location: Line 415 (verified from source)
- ✅ Execution path: run() → get_accuracy_for_week() → _load_season_data()
- ✅ Integration confirmed

**Method 2: AccuracySimulationManager.get_accuracy_for_week()**
- ✅ Caller identified: AccuracySimulationManager.run()
- ✅ Call location: Line 250 (main accuracy simulation loop)
- ✅ Execution path: run_simulation.py → AccuracySimulationManager.run() → get_accuracy_for_week()
- ✅ Integration confirmed

**Method 3: ParallelAccuracyRunner._load_season_data()**
- ✅ Caller identified: ParallelAccuracyRunner._run_week()
- ✅ Call location: Line 225 (STANDALONE FUNCTION, called from _run_week)
- ✅ Execution path: run() → _run_week() → _load_season_data()
- ✅ Integration confirmed

**Method 4: ParallelAccuracyRunner._run_week()**
- ✅ Caller identified: ParallelAccuracyRunner.run()
- ✅ Call location: Line 180 (parallel map execution)
- ✅ Execution path: run_simulation.py → ParallelAccuracyRunner.run() → parallel map → _run_week()
- ✅ Integration confirmed

---

### Orphan Code Check

**Question:** Are there any methods/functions without callers?

**Answer:** ❌ NO - All 4 modified methods have identified callers

**Verification:**
- Modified methods: 4
- Methods with callers: 4
- **Coverage: 4/4 (100%)**

**Orphan methods found:** 0

---

### New Code Check

**Question:** Were any NEW methods added during Rounds 1-3?

**Answer:** ❌ NO - This is a bug fix (only modifies existing methods)

**Verification:**
- Task 1: Modifies existing _load_season_data() (not new)
- Task 2: Modifies existing get_accuracy_for_week() (not new)
- Task 3: Modifies existing _load_season_data() (not new)
- Task 4: Modifies existing _run_week() (not new)
- Task 5: Updates docstrings (not new methods)

**New methods added:** 0

**Implication:** No risk of orphan new methods (nothing new to orphan)

---

### Deleted Code Check

**Question:** Were any methods deleted during this bug fix?

**Answer:** ❌ NO - Bug fix only modifies method internals

**Verification:**
- No methods removed
- No functions deleted
- No classes removed

**Impact:** No risk of breaking existing callers

---

### Integration Changes from Previous Rounds

**Round 1 to Round 2:**
- No changes (4/4 methods still integrated)

**Round 2 to Round 3:**
- No changes (4/4 methods still integrated)
- Task 22 added (new integration test), but no new code methods

**Stability:** ✅ Integration matrix stable across all 3 rounds

---

### Execution Path Verification

**Path 1: Serial Accuracy Simulation**
```
run_simulation.py (entry point)
  → AccuracySimulationManager.run()
    → get_accuracy_for_week() (MODIFIED - Task 2)
      → _load_season_data() (MODIFIED - Task 1)
        → _create_player_manager() (existing, unchanged)
      → _cleanup_player_manager() (existing, unchanged)
```

**Execution path verified:** ✅ Complete, no gaps

---

**Path 2: Parallel Accuracy Simulation**
```
run_simulation.py (entry point)
  → ParallelAccuracyRunner.run()
    → parallel map: _run_week() (MODIFIED - Task 4)
      → _load_season_data() (MODIFIED - Task 3)
        → _create_player_manager() (existing, unchanged)
      → _cleanup_player_manager() (existing, unchanged)
```

**Execution path verified:** ✅ Complete, no gaps

---

### Final Integration Gap Check Summary

**Total Modified Methods:** 4
**Methods with Callers:** 4
**Coverage:** 100%

**New Methods Added:** 0
**Orphan New Methods:** 0

**Methods Deleted:** 0
**Broken Callers:** 0

**Execution Paths Verified:** 2 (serial, parallel)
**Execution Path Gaps:** 0

**✅ FINAL VERIFICATION: NO ORPHAN CODE - ALL 4 METHODS INTEGRATED**

---

### Last Chance Issues Check

**Question:** Any integration issues discovered in Round 3?

**Answer:** ❌ NO - No new issues found

**Checks performed:**
- ❌ No unmapped methods found
- ❌ No orphan implementations found
- ❌ No broken call chains found
- ❌ No deleted methods with remaining callers
- ❌ No circular dependencies introduced

**Confidence Level:** HIGH - All methods comprehensively integrated

---

## ✅ Iteration 23a: Pre-Implementation Spec Audit (MANDATORY GATE - 4 PARTS)

**Audit Date:** 2026-01-02
**Purpose:** Final comprehensive audit before implementation
**⚠️ MANDATORY:** ALL 4 PARTS must PASS before proceeding to Iteration 24

---

### PART 1: Completeness Audit

**Question:** Does every requirement from spec.md have corresponding TODO tasks?

**Requirements from spec.md:**

1. **Code Changes - Change 1:** Update _load_season_data() to return two folders
   - → Task 1 (AccuracySimulationManager) ✅
   - → Task 3 (ParallelAccuracyRunner) ✅

2. **Code Changes - Change 2:** Create two PlayerManager instances per week
   - → Task 2 (AccuracySimulationManager) ✅
   - → Task 4 (ParallelAccuracyRunner) ✅

3. **Code Changes - Change 3:** Update docstrings explaining WHY
   - → Task 5 (Docstring updates) ✅

4. **Testing:** Unit tests for _load_season_data()
   - → Task 6 (returns two folders) ✅
   - → Task 7 (handles missing folder) ✅

5. **Testing:** Unit tests for get_accuracy_for_week()
   - → Task 8 (uses correct folders) ✅

6. **Testing:** Integration test week 1 real data
   - → Task 9 (week 1 accuracy with real data) ✅

7. **Testing:** Integration test week 17 uses week_18
   - → Task 10 (week 17 uses week_18 folder) ✅

8. **Testing:** Integration test all weeks realistic
   - → Task 11 (all weeks have realistic MAE) ✅

9. **Testing:** Run all existing tests (no regressions)
   - → Task 12 (run all tests) ✅

10. **Smoke Testing:** Import tests
    - → Task 13 (smoke test imports) ✅

11. **Smoke Testing:** E2E with statistical sanity checks
    - → Task 14 (smoke test E2E with statistical validation) ✅

12. **Cross-Epic Verification:** Feature 01 tests pass
    - → Task 15 (verify Feature 01 tests) ✅

13. **Cross-Epic Verification:** Compare with epic notes
    - → Task 16 (compare with epic notes) ✅

14. **Cross-Epic Verification:** Compare with original simulation code
    - → Task 17 (compare with original code) ✅

15. **Cross-Epic Verification:** Verify week 17 specifically
    - → Task 18 (verify week 17) ✅

16. **Documentation:** code_changes.md
    - → Task 19 (update code_changes.md) ✅

17. **Documentation:** implementation_checklist.md
    - → Task 20 (update implementation_checklist.md) ✅

18. **Documentation:** lessons_learned.md update
    - → Task 21 (update lessons_learned.md) ✅

19. **Testing (Round 3):** Integration test parallel/serial consistency
    - → Task 22 (test parallel matches serial) ✅

**Result:**
- Requirements in spec: 19
- Requirements with TODO tasks: 19
- Coverage: 100% ✅

**✅ PART 1: PASSED** - All requirements have TODO tasks

---

### PART 2: Specificity Audit

**Question:** Does every TODO task have concrete acceptance criteria?

**Reviewing all TODO tasks:**

**Task 1:** Update _load_season_data() in AccuracySimulationManager
- ✅ Has 9 acceptance criteria (specific)
- ✅ Has implementation location (AccuracySimulationManager.py:293-313)
- ✅ Has test coverage (Tasks 6, 7)
- ✅ SPECIFIC

**Task 2:** Update get_accuracy_for_week() in AccuracySimulationManager
- ✅ Has 10 acceptance criteria (specific)
- ✅ Has implementation location (AccuracySimulationManager.py:411-472)
- ✅ Has test coverage (Tasks 8, 9, 11)
- ✅ SPECIFIC

**Task 3:** Update _load_season_data() in ParallelAccuracyRunner
- ✅ Has 8 acceptance criteria (specific, references Task 1 for consistency)
- ✅ Has implementation location (ParallelAccuracyRunner.py:195)
- ✅ Has test coverage (ParallelAccuracyRunner tests)
- ✅ SPECIFIC

**Task 4:** Update week calculation in ParallelAccuracyRunner
- ✅ Has 8 acceptance criteria (specific, references Task 2 for consistency)
- ✅ Has implementation location (ParallelAccuracyRunner.py)
- ✅ Has test coverage (Integration test for consistency)
- ✅ SPECIFIC

**Task 5:** Update Docstrings
- ✅ Has 5 acceptance criteria (specific)
- ✅ Has implementation location (both files, specific methods)
- ✅ N/A test coverage (documentation only)
- ✅ SPECIFIC

**Tasks 6-12:** Testing tasks
- ✅ All have test names
- ✅ All have specific assertions
- ✅ All have expected outcomes
- ✅ All SPECIFIC

**Tasks 13-14:** Smoke testing tasks
- ✅ Have specific commands/scripts
- ✅ Have acceptance criteria (statistical checks)
- ✅ SPECIFIC

**Tasks 15-18:** Cross-epic verification tasks
- ✅ Have specific verification steps
- ✅ Have acceptance criteria
- ✅ SPECIFIC

**Tasks 19-21:** Documentation tasks
- ✅ Have specific deliverables
- ✅ Have content requirements
- ✅ SPECIFIC

**Task 22:** Integration test parallel/serial (added Round 3)
- ✅ Has test name
- ✅ Has 8 acceptance criteria
- ✅ Has implementation location
- ✅ SPECIFIC

**Result:**
- Total tasks: 22 (21 original + 1 added in Round 3)
- Tasks with acceptance criteria: 22
- Tasks with implementation location: 22
- Tasks with test coverage: 22 (or N/A for docs)
- Specificity: 100% ✅

**✅ PART 2: PASSED** - All tasks have acceptance criteria

---

### PART 3: Interface Contracts Audit

**Question:** Are all external interfaces verified against source code?

**External Dependencies:**

**Dependency 1: AccuracySimulationManager._create_player_manager()**
- ✅ Verified from source: AccuracySimulationManager.py:315
- ✅ Signature: `def _create_player_manager(self, config_dict: Dict, week_folder: Path, season_path: Path) -> PlayerManager`
- ✅ Return type matches: PlayerManager
- ✅ Used in: Task 2
- ✅ VERIFIED

**Dependency 2: AccuracySimulationManager._cleanup_player_manager()**
- ✅ Verified from source: AccuracySimulationManager.py:382
- ✅ Signature: `def _cleanup_player_manager(self, manager: PlayerManager) -> None`
- ✅ Return type matches: None
- ✅ Used in: Task 2
- ✅ VERIFIED

**Dependency 3: ParallelAccuracyRunner._create_player_manager()**
- ✅ Verified from source: ParallelAccuracyRunner.py:209
- ✅ Signature: `def _create_player_manager(config_dict: Dict, week_folder: Path, season_path: Path) -> PlayerManager`
- ✅ **STANDALONE FUNCTION (no self parameter)**
- ✅ Return type matches: PlayerManager
- ✅ Used in: Task 4
- ✅ VERIFIED

**Dependency 4: FantasyPlayer class**
- ✅ Verified from source: FantasyPlayer.py:105
- ✅ Fields: actual_points: List[float], projected_points: List[float]
- ✅ Both fields exist (added in Feature 01/02)
- ✅ Used in: Tasks 2, 4 (accessing actual_points array)
- ✅ VERIFIED

**Dependency 5: Path.exists()**
- ✅ Verified from source: Python stdlib pathlib.Path
- ✅ Signature: `def exists(self) -> bool`
- ✅ Return type matches: bool
- ✅ Used in: Task 1 error handling
- ✅ VERIFIED

**Result:**
- Total external dependencies: 5
- Dependencies verified from source: 5
- Verification: 100% ✅

**✅ PART 3: PASSED** - All dependencies verified from source

---

### PART 4: Integration Evidence Audit

**Question:** Does every new/modified method have identified caller?

**Modified Methods:**

**Method 1: AccuracySimulationManager._load_season_data()**
- ✅ Caller: AccuracySimulationManager.get_accuracy_for_week()
- ✅ Call location: Line 415
- ✅ Execution path: run() → get_accuracy_for_week() → _load_season_data()
- ✅ CALLER IDENTIFIED

**Method 2: AccuracySimulationManager.get_accuracy_for_week()**
- ✅ Caller: AccuracySimulationManager.run()
- ✅ Call location: Line 250
- ✅ Execution path: run_simulation.py → run() → get_accuracy_for_week()
- ✅ CALLER IDENTIFIED

**Method 3: ParallelAccuracyRunner._load_season_data()**
- ✅ Caller: ParallelAccuracyRunner._run_week()
- ✅ Call location: Line 225
- ✅ Execution path: run() → _run_week() → _load_season_data()
- ✅ CALLER IDENTIFIED

**Method 4: ParallelAccuracyRunner._run_week()**
- ✅ Caller: ParallelAccuracyRunner.run()
- ✅ Call location: Line 180 (parallel map)
- ✅ Execution path: run_simulation.py → run() → _run_week()
- ✅ CALLER IDENTIFIED

**New Methods:** 0 (bug fix only modifies existing methods)

**Result:**
- Modified methods: 4
- Methods with callers: 4
- Integration: 100% ✅

**✅ PART 4: PASSED** - All methods have callers

---

## ✅ FINAL RESULTS: Iteration 23a

**Audit Date:** 2026-01-02

**PART 1 - Completeness:** ✅ PASSED
- Requirements: 19
- With TODO tasks: 19
- Coverage: 100%

**PART 2 - Specificity:** ✅ PASSED
- TODO tasks: 22
- With acceptance criteria: 22
- Specificity: 100%

**PART 3 - Interface Contracts:** ✅ PASSED
- External dependencies: 5
- Verified from source: 5
- Verification: 100%

**PART 4 - Integration Evidence:** ✅ PASSED
- Modified methods: 4
- With callers: 4
- Integration: 100%

**OVERALL RESULT: ✅ ALL 4 PARTS PASSED**

**Ready to proceed to Iteration 24 (Implementation Readiness Protocol - FINAL GATE).**

---

## ✅ Iteration 24: Implementation Readiness Protocol (FINAL GATE)

**Date:** 2026-01-02
**Purpose:** Final go/no-go decision before implementation
**⚠️ FINAL GATE:** Cannot proceed to Stage 5b without "GO" decision

---

### Implementation Readiness Checklist

**Spec Verification:**
- [x] spec.md complete (no TBD sections)
- [x] All algorithms documented (15 algorithms traced)
- [x] All edge cases defined (10 edge cases handled)
- [x] All dependencies identified (5 dependencies verified from source)
- [x] Manual data inspection completed (week_01 vs week_02 verified)
- [x] Assumption Validation Table complete (5 assumptions, all verified)

**TODO Verification:**
- [x] TODO file created: `bugfix_high_week_offset_logic/todo.md`
- [x] All requirements have tasks (19 requirements → 22 tasks including Round 3 additions)
- [x] All tasks have acceptance criteria (22/22 tasks specific)
- [x] Implementation locations specified (22/22 tasks have locations)
- [x] Test coverage defined (17 tests planned)
- [x] Implementation phasing defined (6 phases with checkpoints)

**Iteration Completion:**
- [x] All 24 iterations complete (Rounds 1, 2, 3)
- [x] Round 1: Iterations 1-7 + 4a (MANDATORY GATE) - COMPLETE
- [x] Round 2: Iterations 8-16 - COMPLETE
- [x] Round 3: Iterations 17-24 + 23a (MANDATORY GATE) - COMPLETE
- [x] Iteration 4a PASSED (TODO Specification Audit)
- [x] Iteration 23a PASSED (ALL 4 PARTS - Completeness, Specificity, Interface Contracts, Integration Evidence)
- [x] No iterations skipped

**Confidence Assessment:**
- [x] Confidence level: **HIGH**
- [x] All questions resolved (0 open questions)
- [x] No critical unknowns
- [x] Spec re-validated against epic notes (Stage 2.5 principles applied)

**Integration Verification:**
- [x] Algorithm Traceability Matrix complete (15 algorithms traced to code locations)
- [x] Integration Gap Check complete (4/4 modified methods have callers, no orphan code)
- [x] Interface Verification complete (5 dependencies verified from source code)
- [x] Mock Audit complete (3 mocks audited, 1 issue fixed, all match real interfaces)

**Quality Gates:**
- [x] Test coverage: ~92% (exceeds >90% target)
- [x] Performance impact: Acceptable (2x increase for infrequent validation tool)
- [x] Rollback strategy: Defined (git revert approach)
- [x] Documentation plan: Complete (3 docs: code_changes, implementation_checklist, lessons_learned update)
- [x] All mandatory audits PASSED (Iterations 4a, 23a)
- [x] No blockers

**Prevention Strategies Applied (User Requirement):**
- [x] Strategy 1: Stage 2.5 principles (re-read epic notes, validate independently) - APPLIED
- [x] Strategy 2: Stage 5a.5 principles (hands-on data inspection before implementing) - PLAN READY
- [x] Strategy 3: Statistical sanity checks (smoke testing) - DOCUMENTED
- [x] Strategy 4: Output validation (QC Round 2) - PLAN READY
- [x] Strategy 5: Spec re-validation (epic notes as source of truth) - APPLIED
- [x] Strategy 6: Critical questions checklists - IMPLEMENTED

**Cross-Epic Verification (User Requirement):**
- [x] Epic notes verification plan (Tasks 16, 18)
- [x] Original simulation code comparison plan (Task 17)
- [x] Feature 01 consistency check plan (Task 15)
- [x] CSV vs JSON comparison plan (checklist item 25)

---

### GO/NO-GO Decision

**Decision Criteria:**

✅ **GO if:**
- All checklist items checked ✅
- Confidence >= MEDIUM ✅ (actual: HIGH)
- All mandatory audits PASSED (iterations 4a, 23a) ✅
- Iteration 23a: ALL 4 PARTS PASSED ✅
- No critical blockers ✅

❌ **NO-GO if:**
- Any checklist item unchecked
- Confidence < MEDIUM
- Any mandatory audit FAILED
- Any critical blocker

**Evaluation:**
- ✅ ALL checklist items checked (44/44)
- ✅ Confidence: HIGH
- ✅ Iteration 4a: PASSED
- ✅ Iteration 23a: ALL 4 PARTS PASSED
- ✅ Critical blockers: NONE

---

## ✅ DECISION: GO

**Date:** 2026-01-02
**Confidence:** HIGH
**Iterations Complete:** 24/24 (all rounds complete)
**Mandatory Audits:** ALL PASSED
- Iteration 4a: PASSED (TODO Specification Audit)
- Iteration 23a: ALL 4 PARTS PASSED (Pre-Implementation Spec Audit)

**Quality Metrics:**
- Algorithm mappings: 15/15 (100%)
- Integration verification: 4/4 methods (100%)
- Interface verification: 5/5 dependencies (100%)
- Test coverage: ~92% (exceeds >90% target)
- Performance impact: 2x (acceptable for infrequent validation tool)
- Requirements coverage: 19/19 (100%)
- TODO specificity: 22/22 tasks (100%)

**Prevention Strategies:**
- ALL 6 lessons learned strategies applied/planned ✅
- Cross-epic verification requirements integrated ✅
- Statistical sanity checks mandated in smoke testing ✅

**DECISION: ✅ READY FOR IMPLEMENTATION**

**Next Stage:** Stage 5b (Implementation Execution)

**Proceed to Stage 5b using:** `feature-updates/guides_v2/STAGE_5b_implementation_execution_guide.md`

**Critical Notes for Stage 5b:**
1. Execute implementation in 6 phases (not "big bang")
2. Run tests after EACH phase (100% pass required)
3. Apply Stage 5a.5 principles BEFORE coding (hands-on data inspection)
4. Keep spec.md visible during implementation
5. Update implementation_checklist.md continuously
6. Statistical sanity checks in Task 14 are MANDATORY GATE

---

*Created during Stage 5a Round 1 - Iteration 1: Requirements Coverage Check*
*Updated during Stage 5a Round 3 - Iteration 17: Implementation Phasing*
*Updated during Stage 5a Round 3 - Iteration 18: Rollback Strategy*
*Updated during Stage 5a Round 3 - Iteration 19: Algorithm Traceability Matrix (FINAL)*
*Updated during Stage 5a Round 3 - Iteration 20: Performance Considerations*
*Updated during Stage 5a Round 3 - Iteration 21: Mock Audit & Integration Test Plan*
*Updated during Stage 5a Round 3 - Iteration 22: Output Consumer Validation*
*Updated during Stage 5a Round 3 - Iteration 23: Integration Gap Check (FINAL)*
*Updated during Stage 5a Round 3 - Iteration 23a: Pre-Implementation Spec Audit (ALL 4 PARTS PASSED)*
*Updated during Stage 5a Round 3 - Iteration 24: Implementation Readiness Protocol (DECISION: GO)*
