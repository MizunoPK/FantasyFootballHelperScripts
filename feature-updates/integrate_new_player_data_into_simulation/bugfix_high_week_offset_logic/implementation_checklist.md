# Bug Fix: Week Offset Logic - Implementation Checklist

**Purpose:** Track spec requirements during implementation (check off AS YOU IMPLEMENT)

**Instructions:**
- [ ] = Not implemented yet
- [x] = Implemented and verified

**⚠️ CRITICAL:** Update this file IN REAL-TIME (not batched at end)

**Last Updated:** 2026-01-02 (Start of Stage 5b)

---

## Requirements from spec.md

### Code Change Requirements

#### REQ-1: _load_season_data() returns two folders (week_N and week_N+1)

**Spec Section:** Solution Design - Change 1
**TODO Task:** Task 1 (AccuracySimulationManager), Task 3 (ParallelAccuracyRunner)

**AccuracySimulationManager Implementation:**
- [x] **REQ-1a:** Creates projected_folder variable: `season_path / "weeks" / f"week_{week_num:02d}"`
- [x] **REQ-1b:** Creates actual_folder variable: `season_path / "weeks" / f"week_{week_num+1:02d}"`
- [x] **REQ-1c:** Checks projected_folder exists, logs warning if not
- [x] **REQ-1d:** Checks actual_folder exists, logs warning if not
- [x] **REQ-1e:** Returns (projected_folder, actual_folder) instead of (week_folder, week_folder)
- [x] **REQ-1f:** Returns (None, None) if either folder missing
- [x] **REQ-1g:** Docstring explains WHY two folders needed (point-in-time data model)
- [x] **Implementation:** simulation/accuracy/AccuracySimulationManager.py:293-337
- [x] **Verified:** 2026-01-02 (Task 1 complete - code matches spec exactly)

**ParallelAccuracyRunner Implementation:**
- [x] **REQ-1h:** Same changes as AccuracySimulationManager (consistency)
  - Lines 195-236: Modified _load_season_data() to return (projected_folder, actual_folder) ✓
  - Line 217: `projected_folder = season_path / "weeks" / f"week_{week_num:02d}"` ✓
  - Line 222: `actual_folder = season_path / "weeks" / f"week_{actual_week_num:02d}"` ✓
  - Lines 225-234: Checks both folders exist, logs warnings ✓
  - Line 236: Returns (projected_folder, actual_folder) ✓
- [x] **REQ-1i:** STANDALONE FUNCTION (no self parameter)
  - Function signature: `def _load_season_data(season_path: Path, week_num: int)` ✓
- [x] **Implementation:** simulation/accuracy/ParallelAccuracyRunner.py:195-236
- [x] **Verified:** 2026-01-02 (Task 3 complete - code matches spec exactly)

---

#### REQ-2: get_accuracy_for_week() creates TWO PlayerManager instances

**Spec Section:** Solution Design - Change 2
**TODO Task:** Task 2 (AccuracySimulationManager), Task 4 (ParallelAccuracyRunner)

**AccuracySimulationManager Implementation:**
- [x] **REQ-2a:** Checks both projected_path AND actual_path from _load_season_data()
  - Line 437: `if not projected_path or not actual_path: continue` ✓
- [x] **REQ-2b:** Creates projected_mgr: `self._create_player_manager(config_dict, projected_path, season_path)`
  - Line 444: `projected_mgr = self._create_player_manager(config_dict, projected_path, season_path)` ✓
- [x] **REQ-2c:** Creates actual_mgr: `self._create_player_manager(config_dict, actual_path, season_path)`
  - Line 445: `actual_mgr = self._create_player_manager(config_dict, actual_path, season_path)` ✓
- [x] **REQ-2d:** Wraps both managers in try/finally block
  - Lines 447-505: try/finally block wraps both managers ✓
- [x] **REQ-2e:** Calculates max_weekly from projected_mgr
  - Line 454: `max_weekly = projected_mgr.calculate_max_weekly_projection(week_num)` ✓
- [x] **REQ-2f:** Gets projections from projected_mgr.players loop
  - Lines 458-478: `for player in projected_mgr.players:` ✓
- [x] **REQ-2g:** Gets actuals from actual_mgr.players loop
  - Lines 482-497: `for player in actual_mgr.players:` ✓
- [x] **REQ-2h:** Matches players by ID: `if player.id in projections`
  - Line 491: `if player.id in projections:` ✓
- [x] **REQ-2i:** Extracts actual_points[week_num - 1] from actual_mgr players (week_N+1 folder)
  - Line 486: `actual = player.actual_points[week_num - 1]` from actual_mgr ✓
- [x] **REQ-2j:** Cleans up BOTH managers: projected_mgr and actual_mgr
  - Line 504: `self._cleanup_player_manager(projected_mgr)` ✓
  - Line 505: `self._cleanup_player_manager(actual_mgr)` ✓
- [x] **Implementation:** simulation/accuracy/AccuracySimulationManager.py:435-505
- [x] **Verified:** 2026-01-02 (Task 2 complete - code matches spec Solution Design - Change 2 exactly)

**ParallelAccuracyRunner Implementation:**
- [x] **REQ-2k:** Same changes as AccuracySimulationManager (consistency)
  - Line 115: `if not projected_path or not actual_path: continue` ✓
  - Line 122: Creates projected_mgr from projected_path ✓
  - Line 123: Creates actual_mgr from actual_path ✓
  - Lines 125-183: try/finally block wraps both managers ✓
  - Line 132: max_weekly from projected_mgr ✓
  - Lines 136-156: Get projections from projected_mgr.players ✓
  - Lines 160-175: Get actuals from actual_mgr.players ✓
  - Line 169: Match by ID `if player.id in projections` ✓
  - Lines 182-183: Cleanup both managers ✓
- [x] **Implementation:** simulation/accuracy/ParallelAccuracyRunner.py:113-183
- [x] **Verified:** 2026-01-02 (Task 4 complete - code matches spec exactly)

---

#### REQ-3: Docstrings explain WHY two folders needed

**Spec Section:** Solution Design - Change 1, Implementation Checklist
**TODO Task:** Task 5

- [ ] **REQ-3a:** _load_season_data() docstring explains point-in-time data model
- [ ] **REQ-3b:** Docstring mentions: week_N has actuals for weeks 1 to N-1 only
- [ ] **REQ-3c:** Docstring mentions: week N actuals appear in week_N+1 folder
- [ ] **REQ-3d:** get_accuracy_for_week() docstring mentions two PlayerManager instances
- [ ] **REQ-3e:** Code comments explain: "week_N+1 has actual_points[N-1] populated"
- [ ] **Implementation:** Both AccuracySimulationManager.py and ParallelAccuracyRunner.py
- [ ] **Verified:** {Date after implementing Task 5}

---

#### REQ-WIN-1: Win Rate Sim - Cache both projected and actual data

**Spec Section:** Win Rate Simulation Fix (NEW)
**TODO Task:** Task 23

- [x] **REQ-WIN-1a:** _preload_all_weeks() caches TWO datasets per week
  - Lines 296-334: Caches projected_data from week_N folder ✓
  - Lines 312-314: Caches actual_data from week_N+1 folder ✓
  - Lines 325-328: week_data_cache structure: {week_num: {'projected': {}, 'actual': {}}} ✓
- [x] **REQ-WIN-1b:** Handle week 17 limitation (no week_18 exists for 17 actuals)
  - Lines 315-322: Falls back to projected data if actual_folder doesn't exist ✓
  - Line 318-321: Logs warning about missing week_18 ✓
  - Documented in docstring (lines 273-286) ✓
- [x] **Implementation:** simulation/win_rate/SimulatedLeague.py:269-336
- [x] **Verified:** 2026-01-02 (Task 23 complete - code matches requirements)

---

#### REQ-WIN-2: Win Rate Sim - Parse separate folders for projected vs actual

**Spec Section:** Win Rate Simulation Fix (NEW)
**TODO Task:** Task 24

- [x] **REQ-WIN-2a:** _parse_players_json() accepts week_folder and week_num_for_actual
  - Lines 363-368: Signature: `_parse_players_json(week_folder, week_num, week_num_for_actual=None)` ✓
  - Line 391: `actual_week = week_num_for_actual if week_num_for_actual is not None else week_num` ✓
  - Backward compatible (defaults to week_num if not provided) ✓
- [x] **REQ-WIN-2b:** Extract projected_points from week_N using index (week_num - 1)
  - Lines 413-417: Uses week_num for projected_array indexing ✓
- [x] **REQ-WIN-2c:** Extract actual_points using index (actual_week - 1)
  - Lines 419-423: Uses actual_week for actual_array indexing ✓
  - Supports week_N+1 fix when week_num_for_actual provided ✓
- [x] **Implementation:** simulation/win_rate/SimulatedLeague.py:363-440
- [x] **Verified:** 2026-01-02 (Task 24 complete - code matches requirements)

---

#### REQ-WIN-3: Win Rate Sim - Load different data for projected_pm vs actual_pm

**Spec Section:** Win Rate Simulation Fix (NEW)
**TODO Task:** Task 25

- [x] **REQ-WIN-3a:** _load_week_data() sets different data for each PlayerManager
  - Lines 470-477: Extracts projected_data and actual_data from cache ✓
  - Line 482: projected_pm gets week_data_cache[week_num]['projected'] ✓
  - Line 484: actual_pm gets week_data_cache[week_num]['actual'] ✓
- [x] **REQ-WIN-3b:** Handle legacy format and fallback
  - Lines 470-477: Checks if new format with 'projected' and 'actual' keys ✓
  - Lines 475-477: Falls back to same data for both if legacy format ✓
  - Backward compatible with old cache structure ✓
- [x] **Implementation:** simulation/win_rate/SimulatedLeague.py:442-486
- [x] **Verified:** 2026-01-02 (Task 25 complete - code matches requirements)

---

### Testing Requirements

#### REQ-4: Unit tests for _load_season_data()

**Spec Section:** Testing Strategy
**TODO Task:** Task 6, Task 7

- [x] **REQ-4a:** test_load_season_data_returns_two_folders() created
  - Test file: tests/simulation/test_AccuracySimulationManager.py (lines 351-399)
  - Verifies: Returns (week_01_path, week_02_path) for week_num=1 ✓
  - Verifies: Returns (week_17_path, week_18_path) for week_num=17 ✓
  - Verifies: projected_folder != actual_folder (different folders) ✓
- [x] **REQ-4b:** test_load_season_data_handles_missing_actual_folder() created
  - Test file: tests/simulation/test_AccuracySimulationManager.py (lines 401-449)
  - Verifies: Returns (None, None) if week_N+1 folder missing ✓
  - Verifies: Warning logged ("Actual folder not found", "week_19") ✓
  - Verifies: No exception raised ✓
- [x] **REQ-4c:** test_load_season_data_handles_missing_projected_folder() created (BONUS)
  - Test file: tests/simulation/test_AccuracySimulationManager.py (lines 451-496)
  - Verifies: Returns (None, None) if week_N folder missing ✓
  - Verifies: Warning logged ("Projected folder not found") ✓
  - Verifies: No exception raised ✓
- [x] **Implementation:** tests/simulation/test_AccuracySimulationManager.py
- [x] **Verified:** 2026-01-02 (Tasks 6, 7 complete - tests created and match spec requirements)

---

#### REQ-5: Unit tests for get_accuracy_for_week()

**Spec Section:** Testing Strategy
**TODO Task:** Task 8

- [x] **REQ-5a:** test_evaluate_config_weekly_uses_two_player_managers() created
  - Test file: tests/simulation/test_AccuracySimulationManager.py (lines 487-558)
  - Mocks _create_player_manager() to track calls ✓
  - Verifies: Called twice (projected_path week_01, actual_path week_02) ✓
  - Verifies: Both managers cleaned up ✓
  - **Test Result: PASSED** ✓
- [x] **Implementation:** tests/simulation/test_AccuracySimulationManager.py
- [x] **Verified:** 2026-01-02 (Task 8 complete - test passes)

---

#### REQ-6: Integration test - Week 1 accuracy with real data

**Spec Section:** Testing Strategy
**TODO Task:** Task 9

- [ ] **REQ-6a:** test_week_1_accuracy_with_real_data() created
  - Uses REAL AccuracySimulationManager (no mocks)
  - Runs accuracy calculation for season 2021, week 1
  - Verifies: >50% of players have non-zero actuals
  - Verifies: MAE in realistic range (3-8 for QB)
  - Verifies: Variance > 0
- [ ] **Implementation:** tests/simulation/accuracy/integration/test_accuracy_end_to_end.py
- [ ] **Verified:** {Date after implementing Task 9}

---

#### REQ-7: Integration test - Week 17 uses week_18 folder

**Spec Section:** Testing Strategy + Epic Requirement
**TODO Task:** Task 10

- [ ] **REQ-7a:** test_week_17_uses_week_18_folder() created
  - Runs accuracy for season 2021, week 17
  - Verifies: _load_season_data returns (week_17_path, week_18_path)
  - Verifies: Week 17 actuals are non-zero
  - Explicitly verifies epic requirement (line 8)
- [ ] **Implementation:** tests/simulation/accuracy/integration/test_accuracy_end_to_end.py
- [ ] **Verified:** {Date after implementing Task 10}

---

#### REQ-8: Integration test - All weeks have realistic MAE

**Spec Section:** Testing Strategy
**TODO Task:** Task 11

- [ ] **REQ-8a:** test_all_weeks_have_realistic_mae() created
  - Runs accuracy for season 2021, weeks 1-17
  - For EACH week verifies:
    - >50% non-zero actuals
    - MAE in realistic range (2-10)
    - Variance > 0
    - Zero percentage <90%
  - Logs results per week
- [ ] **Implementation:** tests/simulation/accuracy/integration/test_accuracy_end_to_end.py
- [ ] **Verified:** {Date after implementing Task 11}

---

#### REQ-9: All existing tests pass (no regressions)

**Spec Section:** Acceptance Criteria
**TODO Task:** Task 12

- [ ] **REQ-9a:** Command run: `python tests/run_all_tests.py`
- [ ] **REQ-9b:** Result: 2463/2463 tests pass (100%)
- [ ] **REQ-9c:** Exit code: 0 (success)
- [ ] **REQ-9d:** No new failures introduced
- [ ] **Implementation:** Test suite execution
- [ ] **Verified:** {Date after implementing Task 12}

---

### Smoke Testing Requirements

#### REQ-10: Smoke test - Import verification

**Spec Section:** Acceptance Criteria - Smoke Testing
**TODO Task:** Task 13

- [ ] **REQ-10a:** AccuracySimulationManager imports without error
- [ ] **REQ-10b:** ParallelAccuracyRunner imports without error
- [ ] **Implementation:** Python import commands
- [ ] **Verified:** {Date after implementing Task 13}

---

#### REQ-11: Smoke test - E2E with statistical sanity checks

**Spec Section:** Acceptance Criteria - Smoke Testing + Lessons Learned Strategy 3
**TODO Task:** Task 14

**Data Source Verification:**
- [ ] **REQ-11a:** Load week_01/qb_data.json: actual_points[0] = 0.0 ✓
- [ ] **REQ-11b:** Load week_02/qb_data.json: actual_points[0] = 33.6 (non-zero) ✓
- [ ] **REQ-11c:** Confirms data model understanding

**Run Accuracy Calculation:**
- [ ] **REQ-11d:** Execute accuracy simulation for season 2021, week 1
- [ ] **REQ-11e:** No exceptions raised
- [ ] **REQ-11f:** Result object returned

**Statistical Sanity Check 1 - Zero Percentage:**
- [ ] **REQ-11g:** Calculate: zero_pct = (zero_count / total) * 100
- [ ] **REQ-11h:** If zero_pct > 90%: AUTOMATIC FAIL
- [ ] **REQ-11i:** Verify: zero_pct <= 90% PASS

**Statistical Sanity Check 2 - Variance:**
- [ ] **REQ-11j:** Calculate: stddev = statistics.stdev(actual_points)
- [ ] **REQ-11k:** If stddev == 0: FAIL
- [ ] **REQ-11l:** Verify: stddev > 0 PASS

**Statistical Sanity Check 3 - Realistic MAE:**
- [ ] **REQ-11m:** Extract: mae = result.overall_mae
- [ ] **REQ-11n:** Verify: 3.0 <= mae <= 8.0 (realistic NFL range)

**Statistical Sanity Check 4 - Non-Zero Count:**
- [ ] **REQ-11o:** Count: non_zero = total - zero_count
- [ ] **REQ-11p:** If non_zero == 0: FAIL
- [ ] **REQ-11q:** Verify: non_zero > 0 PASS

**Critical Question Checklist:**
- [ ] **REQ-11r:** "Are output values statistically realistic?" ✓
- [ ] **REQ-11s:** "If I saw '(0 have non-zero points)' would I mark PASS?" NO - AUTOMATIC FAIL ✓
- [ ] **REQ-11t:** "Does MAE fall in expected range?" ✓
- [ ] **REQ-11u:** "If this ran in production, would users trust results?" ✓

- [ ] **Implementation:** smoke_test_bug_fix_verification.py
- [ ] **Verified:** {Date after implementing Task 14}

---

### Cross-Epic Verification Requirements

#### REQ-12: Feature 01 tests still pass

**Spec Section:** Acceptance Criteria - Cross-Epic Verification
**TODO Task:** Task 15

- [ ] **REQ-12a:** Run Feature 01 tests: `python -m pytest tests/simulation/win_rate/ -v`
- [ ] **REQ-12b:** ALL Feature 01 tests pass
- [ ] **REQ-12c:** No unintended interactions
- [ ] **Implementation:** Test suite execution
- [ ] **Verified:** {Date after implementing Task 15}

---

#### REQ-13: Epic notes requirements verified

**Spec Section:** Acceptance Criteria - Cross-Epic Verification
**TODO Task:** Task 16

- [ ] **REQ-13a:** Epic notes line 1: Update to use JSON files ✓
- [ ] **REQ-13b:** Epic notes line 3-6: Load JSON from week folders ✓
- [ ] **REQ-13c:** Epic notes line 6: Handle new fields ✓
- [ ] **REQ-13d:** Epic notes line 8: Week_N + week_N+1 pattern ✓ (THIS BUG FIX)
- [ ] **REQ-13e:** ALL epic requirements verified as complete
- [ ] **Implementation:** Documentation verification
- [ ] **Verified:** {Date after implementing Task 16}

---

#### REQ-14: Original simulation code unchanged (algorithms)

**Spec Section:** Acceptance Criteria - Cross-Epic Verification
**TODO Task:** Task 17

- [ ] **REQ-14a:** Read pre-epic AccuracySimulationManager.py
- [ ] **REQ-14b:** Identify original MAE calculation algorithm
- [ ] **REQ-14c:** Verify: MAE calculation logic UNCHANGED
- [ ] **REQ-14d:** Verify: Ranking metrics calculation UNCHANGED
- [ ] **REQ-14e:** Document: "Algorithms unchanged, only data loading modified"
- [ ] **Implementation:** Git diff or file comparison
- [ ] **Verified:** {Date after implementing Task 17}

---

#### REQ-15: Week 17 specifically verified

**Spec Section:** Acceptance Criteria - Cross-Epic Verification + Epic Requirement
**TODO Task:** Task 18

- [ ] **REQ-15a:** Re-run Task 10 test: test_week_17_uses_week_18_folder() ✓
- [ ] **REQ-15b:** Manually verify: Run accuracy for week 17
- [ ] **REQ-15c:** Confirm: week_17 folder used for projections
- [ ] **REQ-15d:** Confirm: week_18 folder used for actuals
- [ ] **REQ-15e:** Epic requirement (line 8) explicitly verified
- [ ] **Implementation:** Verification test + manual check
- [ ] **Verified:** {Date after implementing Task 18}

---

### Documentation Requirements

#### REQ-16: code_changes.md updated

**Spec Section:** Acceptance Criteria - Documentation
**TODO Task:** Task 19

- [ ] **REQ-16a:** File created: bugfix_high_week_offset_logic/code_changes.md
- [ ] **REQ-16b:** Documents Task 1: _load_season_data() changes (before/after)
- [ ] **REQ-16c:** Documents Task 2: get_accuracy_for_week() changes (before/after)
- [ ] **REQ-16d:** Documents Tasks 3-4: ParallelAccuracyRunner changes
- [ ] **REQ-16e:** Documents Task 5: Docstring updates
- [ ] **REQ-16f:** Includes file paths and line numbers
- [ ] **REQ-16g:** Includes rationale for each change
- [ ] **Implementation:** code_changes.md
- [ ] **Verified:** {Date after implementing Task 19}

---

#### REQ-17: implementation_checklist.md complete

**Spec Section:** Acceptance Criteria - Documentation
**TODO Task:** Task 20

- [ ] **REQ-17a:** File created: bugfix_high_week_offset_logic/implementation_checklist.md
- [ ] **REQ-17b:** Maps each code change to spec requirement
- [ ] **REQ-17c:** Verifies all spec requirements implemented
- [ ] **REQ-17d:** No missing requirements
- [ ] **REQ-17e:** No extra scope
- [ ] **Implementation:** implementation_checklist.md (THIS FILE)
- [ ] **Verified:** {Date after all tasks complete}

---

#### REQ-18: lessons_learned.md updated

**Spec Section:** Acceptance Criteria - Documentation
**TODO Task:** Task 21

- [ ] **REQ-18a:** File updated: bugfix_high_week_offset_logic/lessons_learned.md
- [ ] **REQ-18b:** Documents what worked (evidence-based spec, hands-on inspection, statistical validation)
- [ ] **REQ-18c:** Documents any challenges during implementation
- [ ] **REQ-18d:** Documents prevention strategies applied successfully
- [ ] **REQ-18e:** Final summary: "All 6 prevention strategies verified in practice"
- [ ] **Implementation:** lessons_learned.md
- [ ] **Verified:** {Date after all tasks complete}

---

#### REQ-19: Integration test - Parallel matches serial (added Round 3)

**Spec Section:** Stage 5a Round 3 - Iteration 21
**TODO Task:** Task 22

- [ ] **REQ-19a:** test_parallel_matches_serial() created
- [ ] **REQ-19b:** Uses REAL AccuracySimulationManager
- [ ] **REQ-19c:** Uses REAL ParallelAccuracyRunner
- [ ] **REQ-19d:** Compares MAE values (must match within 0.01)
- [ ] **REQ-19e:** Compares rankings (must match exactly)
- [ ] **REQ-19f:** No mocks used
- [ ] **Implementation:** tests/simulation/accuracy/integration/test_accuracy_end_to_end.py
- [ ] **Verified:** {Date after implementing Task 22}

---

## Summary

**Total Requirements:** 19 (REQ-1 through REQ-19)
**Total Sub-Requirements:** 106 (all [x] checkboxes above)
**Implemented:** 0
**Remaining:** 106

**Phases:**
- Phase 1 (Core Data Loading): REQ-1a to REQ-1g (Task 1, 6, 7)
- Phase 2 (Main Calculation): REQ-2a to REQ-2j, REQ-4a to REQ-8a (Tasks 2, 8-11)
- Phase 3 (Parallel Implementation): REQ-1h to REQ-2k, REQ-19a to REQ-19f (Tasks 3, 4, 22)
- Phase 4 (Documentation & Full Testing): REQ-3a to REQ-9d (Tasks 5, 12)
- Phase 5 (Smoke Testing & Cross-Epic): REQ-10a to REQ-15e (Tasks 13-18)
- Phase 6 (Final Documentation): REQ-16a to REQ-18e (Tasks 19-21)

**Last Updated:** 2026-01-02 (Start of Stage 5b)

**Update Frequency:** REAL-TIME (check off AS YOU IMPLEMENT, not batched)

---

*Created during Stage 5b Step 2 - Create Implementation Checklist*
*Update this file continuously as you implement each requirement*
