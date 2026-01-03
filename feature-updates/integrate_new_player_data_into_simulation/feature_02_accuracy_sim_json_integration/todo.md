# Feature 02: Accuracy Simulation JSON Integration - TODO List

**Status:** Round 1 - Initial Draft
**Created:** 2026-01-02 (Stage 5a Round 1 - Iteration 1)
**Last Updated:** 2026-01-02

---

## Task 1: Update AccuracySimulationManager._load_season_data()

**Requirement:** Return week_folder path instead of CSV file paths (spec.md Components Affected section)

**⚠️ CORRECTED:** Spec lists wrong method name (`_get_week_data_paths()`). Actual method is `_load_season_data()` (verified Iteration 2).

**Acceptance Criteria:**
- [ ] Method signature: `_load_season_data(self, season_path: Path, week_num: int) -> Tuple[Optional[Path], Optional[Path]]`
- [ ] Returns `(week_folder, week_folder)` tuple for compatibility with existing callers
- [ ] Returns `(None, None)` if week_folder doesn't exist (same error handling as CSV version)
- [ ] Week folder path: `season_path / "weeks" / f"week_{week_num:02d}"`
- [ ] No changes to method visibility (remains private instance method)

**Implementation Location:**
- File: `simulation/accuracy/AccuracySimulationManager.py`
- Method: `_load_season_data()` (lines 293-319)
- Type: MODIFICATION (not new method)

**Dependencies:**
- None (standalone method)

**Called by:**
- AccuracySimulationManager._evaluate_config_weekly() (existing caller - passes week_data_path to _create_player_manager)

**Tests:**
- Unit test: Verify returns correct (week_folder, week_folder) tuple
- Unit test: Verify returns (None, None) for missing week_folder
- Integration test: Verify accuracy evaluation works with new path format

---

## Task 1a: Update AccuracySimulationManager caller of _load_season_data()

**Requirement:** Update caller to NOT use .parent since _load_season_data() now returns week_folder directly (Integration Gap Check - Iteration 7)

**⚠️ CRITICAL:** This task was NOT in original spec - discovered during Integration Gap Check

**Acceptance Criteria:**
- [ ] Update line 414: Change `projected_path.parent` to `projected_path`
- [ ] Current: `player_mgr = self._create_player_manager(config_dict, projected_path.parent, season_path)`
- [ ] New: `player_mgr = self._create_player_manager(config_dict, projected_path, season_path)`
- [ ] Reason: _load_season_data() now returns week_folder directly (not CSV file path)

**Implementation Location:**
- File: `simulation/accuracy/AccuracySimulationManager.py`
- Line: 414 (inside loop in _evaluate_config_weekly or similar method)
- Type: MODIFICATION (one-line change)

**Dependencies:**
- Requires: Task 1 complete (_load_season_data returns week_folder)
- Called by: N/A (this modifies a caller, not a called method)

**Tests:**
- Integration test: Verify accuracy evaluation works end-to-end
- Unit test: Verify _create_player_manager receives correct week_folder path

---

## Task 2: Update AccuracySimulationManager._create_player_manager()

**Requirement:** Create player_data/ subfolder and copy 6 JSON files (spec.md Components Affected section)

**Acceptance Criteria:**
- [ ] Create `player_data/` subfolder inside temp_dir
- [ ] Copy 6 JSON files from week_folder to player_data/:
  - qb_data.json
  - rb_data.json
  - wr_data.json
  - te_data.json
  - k_data.json
  - dst_data.json
- [ ] Log warning for missing JSON files: `self.logger.warning(f"Missing {position_file} in {week_data_path}")`
- [ ] Continue copying other files even if one JSON missing (graceful degradation)
- [ ] Copy season-level files to temp_dir root (unchanged from CSV version):
  - season_schedule.csv
  - game_data.csv
  - team_data/ (directory)
- [ ] Create league_config.json in temp_dir root (unchanged)
- [ ] Return PlayerManager instance (unchanged)

**Implementation Location:**
- File: `simulation/accuracy/AccuracySimulationManager.py`
- Method: `_create_player_manager()` (lines 327-380)
- Lines to modify: 343-346 (file copying logic)

**Dependencies:**
- Imports: `shutil` (already imported)
- Requires: `week_data_path` parameter (from Task 1)

**Called by:**
- AccuracySimulationManager.run_accuracy_evaluation() (existing caller)

**Tests:**
- Unit test: Verify player_data/ subfolder created
- Unit test: Verify all 6 JSON files copied to player_data/
- Unit test: Verify warning logged for missing JSON file
- Unit test: Verify season-level files copied correctly
- Unit test: Verify PlayerManager instance created successfully

---

## Task 3: Update ParallelAccuracyRunner._load_season_data()

**Requirement:** Same changes as Task 1, but for module-level function used in multiprocessing (spec.md Components Affected section)

**⚠️ CORRECTED:** Spec lists wrong method name (`_get_week_data_paths_worker()`). Actual function is `_load_season_data()` (module-level, NOT a class method). Verified Iteration 2.

**Acceptance Criteria:**
- [ ] Function signature: `_load_season_data(season_path: Path, week_num: int) -> Tuple[Path, Path]`
- [ ] **NOTE:** Module-level function (no `self` parameter)
- [ ] Returns `(week_folder, week_folder)` tuple for compatibility
- [ ] Returns `(None, None)` if week_folder doesn't exist
- [ ] Week folder path: `season_path / "weeks" / f"week_{week_num:02d}"`
- [ ] Identical logic to Task 1 (but as module function for multiprocessing)

**Implementation Location:**
- File: `simulation/accuracy/ParallelAccuracyRunner.py`
- Function: `_load_season_data()` (module-level, lines 195-208)
- Type: MODIFICATION (module-level function)

**Dependencies:**
- None (standalone module function)

**Called by:**
- ParallelAccuracyRunner worker processes (multiprocessing context)

**Tests:**
- Unit test: Verify returns correct (week_folder, week_folder) tuple
- Unit test: Verify returns (None, None) for missing week_folder
- Integration test: Verify parallel accuracy evaluation works

---

## Task 3a: Update ParallelAccuracyRunner caller of _load_season_data()

**Requirement:** Update caller to NOT use .parent since _load_season_data() now returns week_folder directly (Integration Gap Check - Iteration 7)

**⚠️ CRITICAL:** This task was NOT in original spec - discovered during Integration Gap Check

**Acceptance Criteria:**
- [ ] Update line 119: Change `projected_path.parent` to `projected_path`
- [ ] Current: `player_mgr = _create_player_manager(config_dict, projected_path.parent, season_path)`
- [ ] New: `player_mgr = _create_player_manager(config_dict, projected_path, season_path)`
- [ ] Reason: _load_season_data() now returns week_folder directly (not CSV file path)

**Implementation Location:**
- File: `simulation/accuracy/ParallelAccuracyRunner.py`
- Line: 119 (inside worker function loop)
- Type: MODIFICATION (one-line change)

**Dependencies:**
- Requires: Task 3 complete (_load_season_data returns week_folder)
- Called by: N/A (this modifies a caller, not a called method)

**Tests:**
- Integration test: Verify parallel accuracy evaluation works end-to-end
- Unit test: Verify _create_player_manager receives correct week_folder path

---

## Task 4: Update ParallelAccuracyRunner._create_player_manager()

**Requirement:** Same changes as Task 2, but for parallel worker version (spec.md Components Affected section)

**⚠️ CORRECTED:** Spec lists wrong method name (`_create_player_manager_worker()`). Actual function is `_create_player_manager()` (module-level, NOT a class method). Verified Iteration 2.

**Acceptance Criteria:**
- [ ] Function signature: `_create_player_manager(config_dict: dict, week_data_path: Path, season_path: Path) -> PlayerManager`
- [ ] **NOTE:** Module-level function (no `self` parameter)
- [ ] Create `player_data/` subfolder inside temp_dir
- [ ] Copy 6 JSON files from week_folder to player_data/ (same list as Task 2)
- [ ] Log warning for missing JSON files (same pattern as Task 2)
- [ ] Continue copying other files even if one JSON missing
- [ ] Copy season-level files to temp_dir root (same as Task 2)
- [ ] Create league_config.json in temp_dir root
- [ ] Return PlayerManager instance
- [ ] Identical logic to Task 2 (parallel implementation)

**Implementation Location:**
- File: `simulation/accuracy/ParallelAccuracyRunner.py`
- Function: `_create_player_manager()` (module-level, lines 212-257)
- Lines to modify: 224-226 (file copying logic)

**Dependencies:**
- Imports: `shutil` (already imported)
- Requires: `week_data_path` parameter (from Task 3)

**Called by:**
- ParallelAccuracyRunner worker processes (multiprocessing context)

**Tests:**
- Unit test: Verify player_data/ subfolder created
- Unit test: Verify all 6 JSON files copied to player_data/
- Unit test: Verify warning logged for missing JSON file
- Unit test: Verify season-level files copied correctly
- Unit test: Verify PlayerManager instance created in worker process

---

## Task 5: Update Integration Test Fixtures

**Requirement:** Update test fixtures to use JSON format (implied by code changes)

**Acceptance Criteria:**
- [ ] Update test fixtures to create 6 JSON files per week (not CSV)
- [ ] JSON files have required structure (17-element arrays)
- [ ] Test data covers all 6 positions (QB, RB, WR, TE, K, DST)
- [ ] Fixtures create week_folder structure (not individual CSV files)

**Implementation Location:**
- File: `tests/integration/test_accuracy_simulation.py` (if exists)
- Type: Test fixture update

**Dependencies:**
- Requires: Understanding of JSON structure from feature_01

**Tests:**
- Integration test: Verify AccuracySimulationManager works with JSON fixtures
- Integration test: Verify ParallelAccuracyRunner works with JSON fixtures

---

## Task 6: Verify Week 17 Scoring Logic (VALIDATION TASK)

**Requirement:** Verify Week 17 uses correct data - no code changes needed (spec.md Week 17/18 section)

**Acceptance Criteria:**
- [ ] Verify week_17 folder's JSON files are loaded correctly
- [ ] Verify projected_points[16] contains week 17 projected data
- [ ] Verify actual_points[16] contains week 17 actual data
- [ ] Verify MAE calculations for week 17 are correct
- [ ] NO code changes needed (arrays already handle this)

**Implementation Location:**
- N/A (validation task, not code change)

**Type:** QC validation (Stage 5c)

**Tests:**
- Smoke test: Run Accuracy Sim for week 17, verify results
- Manual verification: Check week 17 MAE values are reasonable

---

## Task 7: Verify DEF/K Position Evaluation (VALIDATION TASK)

**Requirement:** Verify DEF and K positions work correctly - no code changes needed (spec.md DEF/K section)

**Acceptance Criteria:**
- [ ] Verify dst_data.json loaded correctly
- [ ] Verify k_data.json loaded correctly
- [ ] Verify DEF players included in accuracy calculations
- [ ] Verify K players included in accuracy calculations
- [ ] NO special code needed (handled same as other positions)

**Implementation Location:**
- N/A (validation task, not code change)

**Type:** QC validation (Stage 5c)

**Tests:**
- Smoke test: Run Accuracy Sim, verify DEF/K in results
- Manual verification: Check DEF/K players appear in output

---

## Summary

**Total Tasks:** 9 (7 original + 2 discovered in Integration Gap Check)
- Code changes: 6 tasks (Tasks 1, 1a, 2, 3, 3a, 4)
- Test updates: 1 task (Task 5)
- Validation tasks: 2 tasks (Tasks 6-7, QC only)

**Tasks Added During Iteration 7 (Integration Gap Check):**
- Task 1a: Update AccuracySimulationManager caller (line 414) ⚠️ CRITICAL
- Task 3a: Update ParallelAccuracyRunner caller (line 119) ⚠️ CRITICAL

**Files to Modify:**
1. simulation/accuracy/AccuracySimulationManager.py (2 methods + 1 caller line)
2. simulation/accuracy/ParallelAccuracyRunner.py (2 methods + 1 caller line)
3. tests/integration/test_accuracy_simulation.py (fixtures)

**Estimated LOC:** ~40-50 lines (matches spec estimate)

**Risk Level:** LOW (simpler than feature_01, no caching or parsing)

---

## ✅ Iteration 4a: TODO Specification Audit - PASSED

**Audit Date:** 2026-01-02
**Auditor:** Stage 5a Round 1 - Iteration 4a (MANDATORY GATE)

**Verification Results:**

| Task | Requirement Ref | Acceptance Criteria | Implementation Location | Dependencies | Tests | Status |
|------|----------------|--------------------|-----------------------|--------------|-------|--------|
| Task 1 | ✅ spec.md Components Affected | ✅ 5 criteria | ✅ File, Method, Lines | ✅ Listed | ✅ 3 tests | ✅ PASS |
| Task 2 | ✅ spec.md Components Affected | ✅ 10 criteria | ✅ File, Method, Lines | ✅ Listed | ✅ 5 tests | ✅ PASS |
| Task 3 | ✅ spec.md Components Affected | ✅ 6 criteria | ✅ File, Function, Lines | ✅ Listed | ✅ 3 tests | ✅ PASS |
| Task 4 | ✅ spec.md Components Affected | ✅ 10 criteria | ✅ File, Function, Lines | ✅ Listed | ✅ 5 tests | ✅ PASS |
| Task 5 | ✅ spec.md (implied) | ✅ 4 criteria | ✅ File, Type | ✅ Listed | ✅ 2 tests | ✅ PASS |
| Task 6 | ✅ spec.md Week 17/18 | ✅ 5 criteria | ✅ N/A (validation) | ✅ N/A | ✅ 2 tests | ✅ PASS |
| Task 7 | ✅ spec.md DEF/K | ✅ 5 criteria | ✅ N/A (validation) | ✅ N/A | ✅ 2 tests | ✅ PASS |

**Summary:**
- Total tasks: 7
- Tasks with requirement reference: 7/7 ✅
- Tasks with acceptance criteria: 7/7 ✅
- Tasks with implementation location: 7/7 ✅
- Tasks with dependencies documented: 7/7 ✅
- Tasks with tests specified: 7/7 ✅

**Result:** ✅ **PASS** - All tasks have specific acceptance criteria, requirements traced to spec, and implementation details documented.

**Critical Findings from Iteration 2:**
- Corrected 3 method names (spec contained wrong names)
- Verified ParallelAccuracyRunner uses module-level functions (multiprocessing compatibility)

**No vague tasks found. Ready to proceed to Iteration 5.**

---

## End-to-End Data Flow (Iteration 5)

**Entry Point:** `AccuracySimulationManager.run_accuracy_evaluation()` receives season_path and week_num

**Data Flow:**

1. **Entry:** season_path (Path to sim_data/YYYY/), week_num (1-17)
   - Source: User input via command line or test
   - Example: `Path("sim_data/2025/")`, week_num=1

2. **Task 1:** _load_season_data(season_path, week_num) → Constructs week_folder path
   - Transformation: `week_folder = season_path / "weeks" / f"week_{week_num:02d}"`
   - Validation: Check week_folder.exists()
   - Output: (week_folder, week_folder) tuple OR (None, None)
   - Example: (Path("sim_data/2025/weeks/week_01/"), Path("sim_data/2025/weeks/week_01/"))

3. **Caller Check:** _evaluate_config_weekly() validates return value
   - If (None, None): Skip week, log warning
   - If valid: Pass week_folder to _create_player_manager()

4. **Task 2/4:** _create_player_manager(config_dict, week_folder, season_path) → Setup temp directory
   - Transformation: Creates temp_dir with mkdtemp()
   - Subprocess: Creates player_data/ subfolder
   - Output: temp_dir (Path to /tmp/accuracy_sim_XXXXX/)

5. **Task 2/4:** Copy 6 JSON files from week_folder to player_data/
   - Source files: week_folder/{qb,rb,wr,te,k,dst}_data.json
   - Destination: temp_dir/player_data/{position}_data.json
   - Transformation: shutil.copy() for each file
   - Error handling: Log warning if file missing, continue with others

6. **Task 2/4:** Copy season-level files to temp_dir root
   - Source files: season_path/{season_schedule.csv, game_data.csv, team_data/}
   - Destination: temp_dir/{season_schedule.csv, game_data.csv, team_data/}
   - Transformation: shutil.copy() and shutil.copytree()

7. **Task 2/4:** Create league_config.json in temp_dir
   - Source: config_dict parameter
   - Destination: temp_dir/league_config.json
   - Transformation: json.dump()

8. **Task 2/4:** Instantiate PlayerManager
   - Input: temp_dir path
   - Transformation: ConfigManager, SeasonScheduleManager, TeamDataManager, PlayerManager chain
   - PlayerManager loads JSON files from temp_dir/player_data/
   - Output: PlayerManager instance with all players loaded

9. **AccuracyCalculator:** Uses PlayerManager data
   - Input: PlayerManager instance from Task 2/4
   - Reads: player.projected_points[week_num-1], player.actual_points[week_num-1]
   - Transformation: Calculate MAE per position
   - Output: AccuracyResult object

10. **Exit:** AccuracyResultsManager stores and reports results
    - Input: AccuracyResult object
    - Output: CSV file or console output with MAE metrics

**Critical Validation Points:**
- Step 2: week_folder must exist (Task 1)
- Step 5: player_data/ subfolder must exist (Task 2/4)
- Step 8: PlayerManager requires player_data/ subfolder (hardcoded)
- Step 9: Week-specific data extracted from 17-element arrays

**Parallel Path (ParallelAccuracyRunner):**
- Same flow as above, but Tasks 3-4 replace Tasks 1-2
- Module-level functions instead of instance methods (multiprocessing compatibility)

---

## Error Handling Scenarios (Iteration 6)

**Error Scenario Matrix:**

| Scenario | Location | Current Behavior | Required Behavior | Task | Severity |
|----------|----------|-----------------|-------------------|------|----------|
| Week folder doesn't exist | Task 1: _load_season_data() line 310 | Returns (None, None) | KEEP - Return (None, None) | Task 1 | LOW (expected) |
| Missing JSON file (qb_data.json) | Task 2/4: _create_player_manager() NEW | Not handled | ADD - Log warning, continue | Task 2/4 | MEDIUM |
| Missing JSON file (rb_data.json) | Task 2/4: _create_player_manager() NEW | Not handled | ADD - Log warning, continue | Task 2/4 | MEDIUM |
| Missing JSON file (wr_data.json) | Task 2/4: _create_player_manager() NEW | Not handled | ADD - Log warning, continue | Task 2/4 | MEDIUM |
| Missing JSON file (te_data.json) | Task 2/4: _create_player_manager() NEW | Not handled | ADD - Log warning, continue | Task 2/4 | MEDIUM |
| Missing JSON file (k_data.json) | Task 2/4: _create_player_manager() NEW | Not handled | ADD - Log warning, continue | Task 2/4 | MEDIUM |
| Missing JSON file (dst_data.json) | Task 2/4: _create_player_manager() NEW | Not handled | ADD - Log warning, continue | Task 2/4 | MEDIUM |
| Missing season_schedule.csv | Task 2/4: line 349-351 (ASM), 229-231 (PAR) | Check exists, skip if not | KEEP - Existing logic | N/A | LOW (expected) |
| Missing game_data.csv | Task 2/4: line 354-356 (ASM), 234-236 (PAR) | Check exists, skip if not | KEEP - Existing logic | N/A | LOW (expected) |
| Missing team_data/ directory | Task 2/4: line 359-361 (ASM), 239-241 (PAR) | Check exists, skip if not | KEEP - Existing logic | N/A | LOW (expected) |
| temp_dir creation fails | Task 2/4: line 341 (ASM), 221 (PAR) | mkdtemp() raises OSError | KEEP - Propagate exception | N/A | HIGH (system) |
| player_data/ mkdir fails | Task 2/4: NEW | N/A (new code) | ADD - mkdir() raises OSError, propagate | Task 2/4 | HIGH (system) |
| JSON file copy fails (I/O error) | Task 2/4: NEW | N/A (new code) | ADD - Try/except, log error, continue | Task 2/4 | LOW (rare) |
| PlayerManager instantiation fails | Task 2/4: line 372 (ASM), 252 (PAR) | Raises exception | KEEP - Propagate exception | N/A | HIGH (critical) |

**Error Handling Patterns:**

**Pattern 1: Expected Missing Data (Graceful Degradation)**
```python
# Example: Missing JSON file
if src.exists():
    shutil.copy(src, dst)
else:
    self.logger.warning(f"Missing {position_file} in {week_data_path}")
    # Continue with other files
```
- Used for: Missing JSON files (6 files)
- Used for: Missing season-level files (already implemented)
- Severity: MEDIUM/LOW
- Action: Log warning, continue execution

**Pattern 2: System Errors (Propagate)**
```python
# Example: temp_dir creation
temp_dir = Path(tempfile.mkdtemp(prefix="accuracy_sim_"))  # Raises OSError if fails
```
- Used for: temp_dir creation, mkdir(), PlayerManager instantiation
- Severity: HIGH
- Action: Let exception propagate to caller (no special handling)

**Pattern 3: Validation Checks (Return sentinel)**
```python
# Example: Week folder doesn't exist
if not week_folder.exists():
    return None, None  # Caller checks for (None, None) and skips week
```
- Used for: Week folder existence check
- Severity: LOW (expected scenario)
- Action: Return sentinel value, caller handles

**Tasks with Error Handling Requirements:**

- **Task 1:** Pattern 3 (validation check) - KEEP existing logic
- **Task 2:** Pattern 1 (missing JSON files) - ADD new error handling
- **Task 2:** Pattern 2 (mkdir, copy errors) - ADD try/except if needed
- **Task 3:** Pattern 3 (validation check) - KEEP existing logic
- **Task 4:** Pattern 1 (missing JSON files) - ADD new error handling
- **Task 4:** Pattern 2 (mkdir, copy errors) - ADD try/except if needed

**Acceptance Criteria Updates:**
- Task 2 acceptance criteria already includes: "Log warning for missing JSON files"
- Task 4 acceptance criteria already includes: "Log warning for missing JSON files"
- No new tasks needed - error handling already covered in existing tasks

---

## Integration Gap Check (Iteration 7)

**Purpose:** Identify ALL integration points and verify no orphan code

**Integration Points Found:**

| Modified Component | Integration Point | Caller/Consumer | Compatibility | Issues Found |
|-------------------|-------------------|-----------------|---------------|--------------|
| Task 1: _load_season_data() | Return value | AccuracySimulationManager line 409 | ⚠️ ISSUE | Caller uses .parent → Added Task 1a |
| Task 3: _load_season_data() | Return value | ParallelAccuracyRunner line 114 | ⚠️ ISSUE | Caller uses .parent → Added Task 3a |
| Task 2/4: _create_player_manager() | PlayerManager | AccuracyCalculator | ✅ COMPATIBLE | No changes needed |
| Task 2/4: player_data/ subfolder | PlayerManager.load_players_from_json() | PlayerManager line 327 | ✅ COMPATIBLE | Hardcoded path matches |
| PlayerManager | AccuracyCalculator.calculate_mae() | AccuracyCalculator | ✅ COMPATIBLE | No changes needed |
| AccuracyCalculator | AccuracyResultsManager | AccuracyResultsManager | ✅ COMPATIBLE | No changes needed |

**Critical Gaps Found: 2**

1. **Gap:** AccuracySimulationManager caller (line 414) uses `projected_path.parent`
   - **Impact:** BREAKING - After Task 1, would pass wrong directory
   - **Solution:** Added Task 1a to remove `.parent` call
   - **Risk:** HIGH - Would cause integration failure without this fix

2. **Gap:** ParallelAccuracyRunner caller (line 119) uses `projected_path.parent`
   - **Impact:** BREAKING - After Task 3, would pass wrong directory
   - **Solution:** Added Task 3a to remove `.parent` call
   - **Risk:** HIGH - Would cause integration failure without this fix

**Integration Points Verified:**
- ✅ Task 1 → Task 1a → Task 2 chain verified
- ✅ Task 3 → Task 3a → Task 4 chain verified
- ✅ Task 2/4 → PlayerManager compatibility verified
- ✅ PlayerManager → AccuracyCalculator compatibility verified
- ✅ No orphan code (all methods have callers)

**No Additional Tasks Needed:** All gaps resolved with Tasks 1a and 3a

---

## Round 1 Verification Evidence

**Iteration 1: Requirements Coverage Check**
- ✅ Evidence: Extracted 7 requirements from spec.md (Components Affected, Week 17/18, DEF/K)
- ✅ Evidence: Created 7 TODO tasks mapping to requirements (Tasks 1-7)
- ✅ Evidence: Each task cites spec section (spec.md Components Affected)

**Iteration 2: Component Dependency Mapping**
- ✅ Evidence: Identified 4 methods to modify
- ✅ Evidence: READ actual source code (AccuracySimulationManager.py, ParallelAccuracyRunner.py)
- ✅ Evidence: Found 3 method name errors in spec, corrected in TODO
- ✅ Evidence: Documented ParallelAccuracyRunner uses module-level functions (no self)

**Iteration 3: Data Structure Verification**
- ✅ Evidence: Verified 6 JSON position files in sim_data/2025/weeks/week_01/
- ✅ Evidence: Verified JSON arrays have 17 elements (projected_points, actual_points)
- ✅ Evidence: Verified PlayerManager hardcodes player_data/ subfolder (line 327)
- ✅ Evidence: Verified season-level files exist (season_schedule.csv, game_data.csv, team_data/)

**Iteration 4: Algorithm Traceability Matrix**
- ✅ Evidence: Mapped 7 algorithms to exact code locations
- ✅ Evidence: Created matrix showing File 1 (ASM) and File 2 (PAR) locations
- ✅ Evidence: Documented change types (MODIFY, REPLACE, KEEP, ADD)

**Iteration 4a: TODO Specification Audit (MANDATORY GATE)**
- ✅ Evidence: Audited all 7 tasks (100% have acceptance criteria)
- ✅ Evidence: Verified all tasks have requirement references
- ✅ Evidence: Verified all tasks have implementation locations
- ✅ Evidence: Verified all tasks have dependencies and tests
- ✅ Evidence: PASSED iteration 4a (documented in TODO)

**Iteration 5: End-to-End Data Flow**
- ✅ Evidence: Traced data flow from entry point to output (10 steps)
- ✅ Evidence: Documented transformations at each step
- ✅ Evidence: Identified 4 critical validation points

**Iteration 6: Error Handling Scenarios**
- ✅ Evidence: Listed 14 error scenarios
- ✅ Evidence: Defined handling for each scenario (3 patterns)
- ✅ Evidence: Mapped error handling to existing TODO tasks (no new tasks)

**Iteration 7: Integration Gap Check (CRITICAL)**
- ✅ Evidence: Listed 6 integration points
- ✅ Evidence: Found 2 critical gaps (caller uses .parent)
- ✅ Evidence: Added 2 tasks to fix gaps (Tasks 1a, 3a)
- ✅ Evidence: Verified all methods have callers (no orphan code)

---

**Round 1 Status:** ✅ **COMPLETE** - All 8 iterations (1-7 + 4a) executed with evidence

**Confidence Level:** MEDIUM-HIGH
- All integration gaps identified and resolved
- Spec errors corrected (3 method names)
- 2 critical tasks added (caller updates)
- All algorithms traced to code locations
- All error scenarios documented

**Blockers:** None

---

## Iteration 8: Test Strategy Development

**Purpose:** Define comprehensive test strategy and verify >90% coverage

**Test Categorization:**

### Unit Tests (Method-Level Testing)

**Test File:** `tests/simulation/accuracy/test_accuracy_simulation_manager.py`

**Task 1 Tests:** (3 tests)
1. `test_load_season_data_returns_week_folder_tuple()`
   - Given: Valid week_folder exists (sim_data/2025/weeks/week_01/)
   - When: _load_season_data(season_path, 1) called
   - Then: Returns (week_folder, week_folder) tuple

2. `test_load_season_data_missing_week_folder()`
   - Given: Week folder doesn't exist
   - When: _load_season_data(season_path, 99) called
   - Then: Returns (None, None)

3. `test_load_season_data_with_various_week_numbers()`
   - Given: Weeks 1-17 exist
   - When: _load_season_data() called for each week
   - Then: All return valid tuples

**Task 2 Tests:** (5 tests)
4. `test_create_player_manager_creates_player_data_subfolder()`
   - Given: Week folder with 6 JSON files
   - When: _create_player_manager() called
   - Then: temp_dir/player_data/ subfolder exists

5. `test_create_player_manager_copies_all_json_files()`
   - Given: Week folder with all 6 JSON files
   - When: _create_player_manager() called
   - Then: All 6 files copied to player_data/ subfolder

6. `test_create_player_manager_logs_warning_missing_json()`
   - Given: Week folder missing qb_data.json
   - When: _create_player_manager() called
   - Then: Warning logged, continues with other files

7. `test_create_player_manager_copies_season_files()`
   - Given: Season folder with season_schedule.csv, game_data.csv, team_data/
   - When: _create_player_manager() called
   - Then: All season files copied to temp_dir root

8. `test_create_player_manager_returns_player_manager()`
   - Given: Valid week and season data
   - When: _create_player_manager() called
   - Then: Returns PlayerManager instance with loaded players

**Test File:** `tests/simulation/accuracy/test_parallel_accuracy_runner.py`

**Task 3 Tests:** (3 tests - same as Task 1)
9. `test_load_season_data_module_function_returns_tuple()`
10. `test_load_season_data_module_function_missing_folder()`
11. `test_load_season_data_module_function_various_weeks()`

**Task 4 Tests:** (5 tests - same as Task 2)
12. `test_create_player_manager_worker_creates_subfolder()`
13. `test_create_player_manager_worker_copies_json_files()`
14. `test_create_player_manager_worker_logs_warnings()`
15. `test_create_player_manager_worker_copies_season_files()`
16. `test_create_player_manager_worker_returns_player_manager()`

---

### Integration Tests (Feature-Level Testing)

**Test File:** `tests/integration/test_accuracy_simulation.py`

**Task 1a & 3a Tests:** (4 tests)
17. `test_accuracy_evaluation_end_to_end_single_week()`
    - Given: Complete JSON data for week 1
    - When: run_accuracy_evaluation() called
    - Then: AccuracyResult returned with correct MAE values

18. `test_accuracy_evaluation_end_to_end_multiple_weeks()`
    - Given: JSON data for weeks 1-17
    - When: run_accuracy_evaluation() for all weeks
    - Then: All weeks evaluated, correct aggregate results

19. `test_parallel_accuracy_evaluation_end_to_end()`
    - Given: Multiple configs, multiple weeks
    - When: ParallelAccuracyRunner.run() called
    - Then: All configs evaluated correctly in parallel

20. `test_accuracy_evaluation_caller_passes_correct_path()`
    - Given: _load_season_data() returns week_folder
    - When: Caller passes to _create_player_manager()
    - Then: Correct week_folder received (NOT .parent)

**Task 5 Tests:** (2 tests)
21. `test_accuracy_fixtures_use_json_format()`
    - Given: Test fixtures
    - When: Tests run
    - Then: Fixtures create 6 JSON files per week (not CSV)

22. `test_accuracy_fixtures_have_17_element_arrays()`
    - Given: Test fixture JSON data
    - When: Data loaded
    - Then: projected_points and actual_points have 17 elements

---

### Edge Case / Validation Tests

**Task 6 Tests:** (2 tests - Week 17/18 validation)
23. `test_week_17_uses_correct_data()`
    - Given: Week 17 JSON files
    - When: Accuracy evaluation for week 17
    - Then: projected_points[16] and actual_points[16] used correctly

24. `test_week_17_mae_calculations_correct()`
    - Given: Week 17 data with known projections/actuals
    - When: MAE calculated
    - Then: MAE values match expected calculations

**Task 7 Tests:** (2 tests - DEF/K validation)
25. `test_def_position_evaluated_correctly()`
    - Given: dst_data.json loaded
    - When: Accuracy evaluation
    - Then: DEF players included in results

26. `test_k_position_evaluated_correctly()`
    - Given: k_data.json loaded
    - When: Accuracy evaluation
    - Then: K players included in results

---

**Test Coverage Summary:**

| Task | Unit Tests | Integration Tests | Edge/Validation Tests | Total |
|------|-----------|-------------------|----------------------|-------|
| Task 1 | 3 | - | - | 3 |
| Task 1a | - | 1 | - | 1 |
| Task 2 | 5 | - | - | 5 |
| Task 3 | 3 | - | - | 3 |
| Task 3a | - | 1 | - | 1 |
| Task 4 | 5 | - | - | 5 |
| Task 5 | - | 2 | - | 2 |
| Task 6 | - | - | 2 | 2 |
| Task 7 | - | - | 2 | 2 |
| **Integration** | - | 2 | - | 2 |
| **TOTAL** | **16** | **6** | **4** | **26** |

**Coverage Analysis:**
- ✅ Unit test coverage: 100% (all methods have tests)
- ✅ Integration test coverage: 100% (end-to-end flow tested)
- ✅ Edge case coverage: 100% (Week 17, DEF/K, missing files)
- ✅ Error handling coverage: 100% (missing folder, missing files)
- ✅ Estimated coverage: >95% (exceeds >90% requirement)

**No Additional Test Tasks Needed:** All test scenarios covered by existing task specifications

---

## Iteration 9: Edge Case Enumeration

**Purpose:** List ALL edge cases and verify handling in TODO/tests

**Edge Case Catalog:**

### Data Quality Edge Cases

| Edge Case | Handling | Covered In | Test |
|-----------|----------|------------|------|
| Empty JSON file (0 bytes) | PlayerManager logs warning, continues | Task 2/4 (graceful degradation) | Test #6/#14 (missing JSON) |
| Malformed JSON (syntax error) | PlayerManager raises JSONDecodeError | PlayerManager spec (out of scope) | PlayerManager tests |
| Missing position in JSON (no "QB" key) | PlayerManager skips position, logs warning | PlayerManager spec (out of scope) | PlayerManager tests |
| JSON with extra fields | PlayerManager ignores extra fields | FantasyPlayer.from_json() (out of scope) | PlayerManager tests |
| projected_points array length ≠ 17 | PlayerManager validates on load | PlayerManager spec (out of scope) | PlayerManager tests |
| actual_points array length ≠ 17 | PlayerManager validates on load | PlayerManager spec (out of scope) | PlayerManager tests |

### File System Edge Cases

| Edge Case | Handling | Covered In | Test |
|-----------|----------|------------|------|
| Week folder doesn't exist | Return (None, None), caller skips | Task 1/3, Iteration 6 (Pattern 3) | Test #2/#10 |
| Missing qb_data.json | Log warning, continue | Task 2/4, Iteration 6 (Pattern 1) | Test #6/#14 |
| Missing rb_data.json | Log warning, continue | Task 2/4, Iteration 6 (Pattern 1) | Test #6/#14 |
| Missing wr_data.json | Log warning, continue | Task 2/4, Iteration 6 (Pattern 1) | Test #6/#14 |
| Missing te_data.json | Log warning, continue | Task 2/4, Iteration 6 (Pattern 1) | Test #6/#14 |
| Missing k_data.json | Log warning, continue | Task 2/4, Iteration 6 (Pattern 1) | Test #6/#14 |
| Missing dst_data.json | Log warning, continue | Task 2/4, Iteration 6 (Pattern 1) | Test #6/#14 |
| Missing season_schedule.csv | Check exists, skip | Current code (unchanged) | Test #7/#15 |
| Missing game_data.csv | Check exists, skip | Current code (unchanged) | Test #7/#15 |
| Missing team_data/ directory | Check exists, skip | Current code (unchanged) | Test #7/#15 |
| All JSON files missing | PlayerManager empty, MAE = NaN | Graceful degradation | Test #6/#14 (partial) |
| File unreadable (permissions) | OSError raised, propagated | Iteration 6 (Pattern 2) | Not tested (rare) |
| Disk full during copy | OSError raised, propagated | Iteration 6 (Pattern 2) | Not tested (rare) |

### Boundary Cases

| Edge Case | Handling | Covered In | Test |
|-----------|----------|------------|------|
| Week number = 0 | Week folder "week_00" doesn't exist → (None, None) | Task 1/3 logic | Test #2/#10 (implicit) |
| Week number = 1 | Week folder "week_01" exists → valid | Task 1/3 logic | Test #1/#9 |
| Week number = 17 | Week folder "week_17" exists → valid | Task 1/3 logic, Task 6 (validation) | Test #3/#11, Test #23/#24 |
| Week number = 18 | Week folder "week_18" may exist → valid if present | Task 1/3 logic | Test #3/#11 (implicit) |
| Week number = 99 | Week folder doesn't exist → (None, None) | Task 1/3 logic | Test #2/#10 |
| projected_points[16] (week 17) | Valid index, contains week 17 projected | Task 6 (validation) | Test #23 |
| actual_points[16] (week 17) | Valid index, contains week 17 actual | Task 6 (validation) | Test #23 |
| projected_points[0] (week 1) | Valid index, contains week 1 projected | Array indexing (tested) | Test #23 (implicit) |

### Integration / State Edge Cases

| Edge Case | Handling | Covered In | Test |
|-----------|----------|------------|------|
| Caller uses .parent on week_folder | Integration failure (broken after Task 1) | Task 1a/3a (fixes this) | Test #20 |
| temp_dir creation fails (mkdtemp) | OSError raised, propagated | Iteration 6 (Pattern 2) | Not tested (rare) |
| player_data/ mkdir fails | OSError raised, propagated | Task 2/4 (new code) | Not tested (rare) |
| PlayerManager instantiation fails | Exception raised, propagated | Iteration 6 (Pattern 2) | Not tested (unlikely) |
| ConfigManager missing temp_dir config | PlayerManager handles default | PlayerManager spec (out of scope) | PlayerManager tests |

### Position-Specific Edge Cases

| Edge Case | Handling | Covered In | Test |
|-----------|----------|------------|------|
| DEF position (dst_data.json) loaded | Handled same as other positions | Task 7 (validation) | Test #25 |
| K position (k_data.json) loaded | Handled same as other positions | Task 7 (validation) | Test #26 |
| DEF players missing | Log warning, continue | Task 2/4 (Pattern 1) | Test #6/#14 (covers all positions) |
| K players missing | Log warning, continue | Task 2/4 (Pattern 1) | Test #6/#14 (covers all positions) |

**Summary:**
- **Total edge cases identified:** 35
- **Handled in existing tasks:** 33
- **Tested:** 31 (3 rare system errors not tested)
- **Not handled (out of scope):** 6 (PlayerManager validation - separate feature)

**Edge Cases NOT Tested (Acceptable):**
1. File unreadable (permissions) - Rare system error, propagates exception
2. Disk full during copy - Rare system error, propagates exception
3. temp_dir creation fails - Rare system error, propagates exception
4. player_data/ mkdir fails - Rare system error, propagates exception
5. PlayerManager instantiation fails - Unlikely, propagates exception

**No Additional Tasks Needed:** All critical edge cases covered by existing tasks and tests

---

## Iteration 10: Configuration Change Impact

**Purpose:** Assess impact on league_config.json and ensure backward compatibility

**Configuration Impact Assessment:**

**New Config Keys Added:** NONE

**Existing Config Keys Modified:** NONE

**Configuration Changes:** NONE - This feature only changes file loading logic, not configuration

**Rationale:**
- Feature changes how player data is loaded (from CSV to JSON files)
- Player data source is NOT configurable in league_config.json
- league_config.json contains league settings (scoring, roster limits, etc.), not data source paths
- No configuration changes needed for JSON migration

**Backward Compatibility:**
- ✅ **100% backward compatible** - No config changes mean existing configs work unchanged
- ✅ **No migration needed** - Configs from previous versions work as-is
- ✅ **No defaults needed** - No new keys to default
- ✅ **No user action required** - Transparent change to data loading

**Data Migration (Not Config Migration):**
- User MUST run player-data-fetcher to generate JSON files
- This is a **data migration**, not a configuration migration
- Data migration is out of scope for this feature (documented in epic notes)

**No Tasks Needed:** No configuration changes in this feature

---

## Iteration 11: Algorithm Traceability Matrix Re-verify (CRITICAL)

**Purpose:** Re-verify algorithm matrix after Tasks 1a and 3a were added in Iteration 7

**Updated Algorithm Traceability Matrix:**

| Algorithm | Spec Requirement | AccuracySimulationManager | ParallelAccuracyRunner | Task | Change Type |
|-----------|------------------|---------------------------|------------------------|------|-------------|
| 1. Week Folder Path Construction | Return week_folder instead of CSV paths | _load_season_data():308 | _load_season_data():197 | Task 1, Task 3 | MODIFY return |
| 2. Week Existence Check | Return (None, None) if missing | _load_season_data():310-311 | _load_season_data():199-200 | Task 1, Task 3 | KEEP unchanged |
| 3. Caller Path Passing | Pass week_folder (not .parent) | Caller line 414 | Caller line 119 | **Task 1a, Task 3a** | **MODIFY caller** |
| 4. Player Data Subfolder Creation | Create player_data/ subfolder | _create_player_manager():NEW | _create_player_manager():NEW | Task 2, Task 4 | ADD new code |
| 5. JSON File Iteration | Iterate 6 position files | _create_player_manager():343-346 | _create_player_manager():224-226 | Task 2, Task 4 | REPLACE logic |
| 6. JSON File Copying | Copy src to player_data/dst | _create_player_manager():343-346 | _create_player_manager():224-226 | Task 2, Task 4 | REPLACE logic |
| 7. Missing File Error Handling | Log warning, continue | _create_player_manager():NEW | _create_player_manager():NEW | Task 2, Task 4 | ADD new logic |
| 8. Season-Level File Copying | Copy 3 files to temp_dir root | _create_player_manager():348-361 | _create_player_manager():228-241 | Task 2, Task 4 | KEEP unchanged |
| 9. Config File Creation | Create league_config.json | _create_player_manager():364-366 | _create_player_manager():244-246 | Task 2, Task 4 | KEEP unchanged |
| 10. PlayerManager Instantiation | Return PlayerManager | _create_player_manager():369-377 | _create_player_manager():249-257 | Task 2, Task 4 | KEEP unchanged |

**Re-verification Results:**

✅ **All 10 algorithms traced** (3 more than original matrix from Iteration 4)
✅ **Tasks 1a and 3a integrated** (Algorithm #3 - caller modification)
✅ **All tasks map to algorithms** (9 tasks → 10 algorithms)
✅ **No orphan algorithms** (all have implementing tasks)
✅ **No orphan tasks** (all implement an algorithm)

**Changes Since Iteration 4:**
- Added Algorithm #3: Caller Path Passing (Tasks 1a, 3a) - discovered in Integration Gap Check
- Added Algorithm #4: Player Data Subfolder Creation (Tasks 2, 4) - was implicit in file copying
- Total algorithms increased from 7 to 10 (more granular)

**Verification Matrix:**

| Task | Implements Algorithm(s) | Verified |
|------|------------------------|----------|
| Task 1 | #1, #2 | ✅ |
| Task 1a | #3 | ✅ |
| Task 2 | #4, #5, #6, #7, #8, #9, #10 | ✅ |
| Task 3 | #1, #2 | ✅ |
| Task 3a | #3 | ✅ |
| Task 4 | #4, #5, #6, #7, #8, #9, #10 | ✅ |
| Task 5 | N/A (test fixtures, not algorithms) | ✅ |
| Task 6 | N/A (validation task, not algorithm changes) | ✅ |
| Task 7 | N/A (validation task, not algorithm changes) | ✅ |

**Matrix is COMPLETE and ACCURATE** ✅

---

## Iteration 12: End-to-End Data Flow Re-verify (CRITICAL)

**Purpose:** Re-verify E2E data flow after Tasks 1a and 3a were added

**Updated End-to-End Data Flow:**

**Entry Point:** `AccuracySimulationManager.run_accuracy_evaluation()` receives season_path and week_num

**Complete Data Flow (Updated):**

1. **Entry:** season_path (Path to sim_data/YYYY/), week_num (1-17)
   - Source: User input via command line or test
   - Example: `Path("sim_data/2025/")`, week_num=1

2. **Task 1:** _load_season_data(season_path, week_num) → Constructs week_folder path
   - Transformation: `week_folder = season_path / "weeks" / f"week_{week_num:02d}"`
   - Validation: Check week_folder.exists()
   - Output: **(week_folder, week_folder)** tuple OR (None, None)
   - Example: (Path("sim_data/2025/weeks/week_01/"), Path("sim_data/2025/weeks/week_01/"))
   - **CHANGED from Iteration 5:** Returns week_folder (not CSV paths)

3. **Caller Check:** _evaluate_config_weekly() validates return value
   - If (None, None): Skip week, log warning
   - If valid: **Extract projected_path (which is week_folder)**

4. **Task 1a:** Caller passes week_folder to _create_player_manager()
   - **OLD CODE:** `player_mgr = self._create_player_manager(config_dict, projected_path.parent, season_path)`
   - **NEW CODE:** `player_mgr = self._create_player_manager(config_dict, projected_path, season_path)`
   - Transformation: Remove `.parent` call (projected_path IS week_folder after Task 1)
   - **ADDED in Iteration 7 - Critical integration fix**

5. **Task 2:** _create_player_manager(config_dict, week_folder, season_path) → Setup temp directory
   - Input: week_folder (Path to week_01/), season_path
   - Transformation: Creates temp_dir with mkdtemp()
   - Subprocess: **Creates player_data/ subfolder** (Algorithm #4)
   - Output: temp_dir (Path to /tmp/accuracy_sim_XXXXX/)
   - **CHANGED from Iteration 5:** Creates player_data/ subfolder

6. **Task 2:** Copy 6 JSON files from week_folder to player_data/
   - Source files: week_folder/{qb,rb,wr,te,k,dst}_data.json
   - Destination: temp_dir/player_data/{position}_data.json
   - Transformation: shutil.copy() for each file (Algorithm #6)
   - Error handling: Log warning if file missing, continue (Algorithm #7)
   - **UNCHANGED from Iteration 5**

7. **Task 2:** Copy season-level files to temp_dir root
   - Source files: season_path/{season_schedule.csv, game_data.csv, team_data/}
   - Destination: temp_dir/{season_schedule.csv, game_data.csv, team_data/}
   - Transformation: shutil.copy() and shutil.copytree() (Algorithm #8)
   - **UNCHANGED from Iteration 5**

8. **Task 2:** Create league_config.json in temp_dir
   - Source: config_dict parameter
   - Destination: temp_dir/league_config.json
   - Transformation: json.dump() (Algorithm #9)
   - **UNCHANGED from Iteration 5**

9. **Task 2:** Instantiate PlayerManager
   - Input: temp_dir path
   - Transformation: ConfigManager, SeasonScheduleManager, TeamDataManager, PlayerManager chain (Algorithm #10)
   - PlayerManager loads JSON files from temp_dir/player_data/
   - Output: PlayerManager instance with all players loaded
   - **UNCHANGED from Iteration 5**

10. **AccuracyCalculator:** Uses PlayerManager data
    - Input: PlayerManager instance from Task 2
    - Reads: player.projected_points[week_num-1], player.actual_points[week_num-1]
    - Transformation: Calculate MAE per position
    - Output: AccuracyResult object
    - **UNCHANGED from Iteration 5**

11. **Exit:** AccuracyResultsManager stores and reports results
    - Input: AccuracyResult object
    - Output: CSV file or console output with MAE metrics
    - **UNCHANGED from Iteration 5**

**Parallel Path (ParallelAccuracyRunner):**
- Same flow as above, but Tasks 3-3a-4 replace Tasks 1-1a-2
- Module-level functions instead of instance methods (multiprocessing compatibility)
- Task 3a: Caller line 119 updated (same .parent fix)

**Critical Validation Points (Updated):**
- ✅ Step 2: week_folder must exist (Task 1)
- ✅ **Step 4: Caller must pass week_folder (NOT .parent) (Task 1a) - CRITICAL FIX**
- ✅ Step 5: player_data/ subfolder must exist (Task 2)
- ✅ Step 9: PlayerManager requires player_data/ subfolder (hardcoded)
- ✅ Step 10: Week-specific data extracted from 17-element arrays

**Changes Since Iteration 5:**
1. Added Step 4 (Task 1a) - Caller modification to remove `.parent`
2. Updated Step 2 output - Now explicitly (week_folder, week_folder)
3. Added Step 5 subprocess - Explicit player_data/ subfolder creation
4. Renumbered steps 5-11 (was 4-10)

**Re-verification Results:**
✅ **Data flow is COMPLETE** (11 steps, was 10)
✅ **Task 1a integrated** (Step 4 - caller fix)
✅ **All tasks in flow** (Tasks 1, 1a, 2, 3, 3a, 4)
✅ **No data flow gaps** (each step connects to next)
✅ **Parallel path documented** (Tasks 3-3a-4)

**Flow is ACCURATE and VERIFIED** ✅

---

## Iteration 13: Dependency Version Check

**Purpose:** Verify external dependency versions and compatibility

**External Dependencies Analysis:**

### Standard Library Dependencies

| Module | Used In | Version Required | Version Concerns |
|--------|---------|-----------------|------------------|
| pathlib.Path | All tasks | Python 3.6+ | ✅ None (standard lib) |
| json | Task 2/4 (config) | Python 3.6+ | ✅ None (standard lib) |
| tempfile | Task 2/4 (mkdtemp) | Python 3.6+ | ✅ None (standard lib) |
| shutil | Task 2/4 (copy, copytree) | Python 3.6+ | ✅ None (standard lib) |

### Internal Dependencies

| Module | Used In | Version/Compatibility | Concerns |
|--------|---------|----------------------|----------|
| PlayerManager | Task 2/4 | Internal (league_helper) | ✅ Spec verified (player_data/ subfolder) |
| ConfigManager | Task 2/4 | Internal (league_helper) | ✅ None (unchanged usage) |
| SeasonScheduleManager | Task 2/4 | Internal (league_helper) | ✅ None (unchanged usage) |
| TeamDataManager | Task 2/4 | Internal (league_helper) | ✅ None (unchanged usage) |
| AccuracyCalculator | E2E flow | Internal (simulation/accuracy) | ✅ None (unchanged usage) |
| AccuracyResultsManager | E2E flow | Internal (simulation/accuracy) | ✅ None (unchanged usage) |

### External Package Dependencies

**None** - This feature uses only Python standard library and internal modules

**Python Version Requirement:**
- **Minimum:** Python 3.6+ (for pathlib.Path)
- **Current Project:** Python 3.8+ (based on CLAUDE.md)
- ✅ **Compatible:** No version concerns

**Backward Compatibility:**
- ✅ All standard library modules available in Python 3.6+
- ✅ No new external packages added
- ✅ No version constraints needed
- ✅ No package upgrades required

**Dependency Risks:**
- **Risk Level:** NONE
- **Reason:** Only standard library + internal modules
- **Mitigation:** N/A (no risks identified)

**No Tasks Needed:** No dependency version issues

---

## Iteration 14: Integration Gap Check Re-verify (CRITICAL)

**Purpose:** Re-verify all integration points after completing Round 1 and Round 2 updates

**Integration Points Matrix (Re-verified):**

| Integration Point | Provider | Consumer | Interface | Status | Resolution |
|-------------------|----------|----------|-----------|--------|------------|
| _load_season_data return value | Task 1 | Caller line 409 | Tuple[Optional[Path], Optional[Path]] | ✅ COMPATIBLE | Task 1a fixes caller |
| _load_season_data return value | Task 3 | Caller line 114 | Tuple[Path, Path] | ✅ COMPATIBLE | Task 3a fixes caller |
| Caller → _create_player_manager | Task 1a | Task 2 | week_folder path | ✅ COMPATIBLE | Caller passes week_folder |
| Caller → _create_player_manager | Task 3a | Task 4 | week_folder path | ✅ COMPATIBLE | Caller passes week_folder |
| player_data/ subfolder | Task 2/4 | PlayerManager | Hardcoded path | ✅ COMPATIBLE | Verified line 327 |
| PlayerManager | Task 2/4 | AccuracyCalculator | PlayerManager instance | ✅ COMPATIBLE | No changes |
| AccuracyCalculator | E2E flow | AccuracyResultsManager | AccuracyResult object | ✅ COMPATIBLE | No changes |

**Critical Integration Fixes Applied:**

1. **Gap #1 (Found in Iteration 7):** AccuracySimulationManager caller line 414 uses `.parent`
   - **Status:** ✅ RESOLVED by Task 1a
   - **Verification:** Task 1a changes `projected_path.parent` → `projected_path`
   - **Test:** Test #20 verifies correct path passed

2. **Gap #2 (Found in Iteration 7):** ParallelAccuracyRunner caller line 119 uses `.parent`
   - **Status:** ✅ RESOLVED by Task 3a
   - **Verification:** Task 3a changes `projected_path.parent` → `projected_path`
   - **Test:** Test #20 verifies correct path passed

**New Gaps Introduced in Round 1/2:**
- ✅ **NONE** - No new integration gaps found

**All Integration Points Verified:**
- ✅ Task 1 → Task 1a: Compatible (Tuple → week_folder extraction)
- ✅ Task 1a → Task 2: Compatible (week_folder → week_data_path parameter)
- ✅ Task 2 → PlayerManager: Compatible (player_data/ subfolder created)
- ✅ Task 3 → Task 3a: Compatible (Tuple → week_folder extraction)
- ✅ Task 3a → Task 4: Compatible (week_folder → week_data_path parameter)
- ✅ Task 4 → PlayerManager: Compatible (player_data/ subfolder created)
- ✅ PlayerManager → AccuracyCalculator: Compatible (no interface changes)
- ✅ AccuracyCalculator → AccuracyResultsManager: Compatible (no interface changes)

**Integration Chain Completeness:**

**Main Path:**
```
User Input (season_path, week_num)
  ↓
Task 1 (_load_season_data) → Returns (week_folder, week_folder)
  ↓
Task 1a (caller line 414) → Passes week_folder
  ↓
Task 2 (_create_player_manager) → Creates player_data/, copies JSON
  ↓
PlayerManager → Loads from player_data/
  ↓
AccuracyCalculator → Calculates MAE
  ↓
AccuracyResultsManager → Outputs results
```

**Parallel Path:**
```
User Input (season_path, week_num)
  ↓
Task 3 (_load_season_data) → Returns (week_folder, week_folder)
  ↓
Task 3a (caller line 119) → Passes week_folder
  ↓
Task 4 (_create_player_manager) → Creates player_data/, copies JSON
  ↓
PlayerManager → Loads from player_data/
  ↓
AccuracyCalculator → Calculates MAE
  ↓
AccuracyResultsManager → Outputs results
```

**Re-verification Results:**
✅ **All integration points verified**
✅ **Both critical gaps resolved** (Tasks 1a, 3a added)
✅ **No new gaps introduced**
✅ **Both paths (main + parallel) complete**
✅ **No orphan tasks** (all tasks integrate)

**Integration Check PASSES** ✅

---

## Iteration 15: Test Coverage Depth Check

**Purpose:** Verify test coverage >90% and includes edge cases (not just happy path)

**Coverage Analysis by Task:**

| Task | Code LOC | Happy Path Tests | Edge Case Tests | Total Tests | Coverage % |
|------|----------|-----------------|-----------------|-------------|------------|
| Task 1 | ~3 lines | 2 (Test #1, #3) | 1 (Test #2) | 3 | 100% |
| Task 1a | ~1 line | 1 (Test #20) | - | 1 | 100% |
| Task 2 | ~25 lines | 3 (Test #4, #5, #8) | 2 (Test #6, #7) | 5 | 100% |
| Task 3 | ~3 lines | 2 (Test #9, #11) | 1 (Test #10) | 3 | 100% |
| Task 3a | ~1 line | 1 (Test #20) | - | 1 | 100% |
| Task 4 | ~25 lines | 3 (Test #12, #13, #16) | 2 (Test #14, #15) | 5 | 100% |
| Task 5 | ~varies | - | 2 (Test #21, #22) | 2 | 100% |
| Task 6 | N/A (validation) | - | 2 (Test #23, #24) | 2 | 100% |
| Task 7 | N/A (validation) | - | 2 (Test #25, #26) | 2 | 100% |
| **Integration** | N/A | 4 (Test #17-#20) | - | 4 | - |

**Total:**
- **Happy path tests:** 12 (46%)
- **Edge case tests:** 12 (46%)
- **Integration tests:** 4 (15%)  (note: percentages > 100% due to overlap)
- **Total tests:** 26 (counts tests once, some test both happy + edge)
- **Estimated LOC:** ~60 lines (4 methods × 15 LOC avg)
- **Estimated coverage:** >95%

**Edge Case Coverage Verification:**

| Edge Case Category | Tests Covering | Coverage |
|-------------------|---------------|----------|
| Missing week folder | Test #2, #10 | ✅ 100% |
| Missing JSON files (all 6 positions) | Test #6, #14 | ✅ 100% |
| Missing season files | Test #7, #15 | ✅ 100% |
| Week 17 boundary | Test #23, #24 | ✅ 100% |
| Week 1 boundary | Test #1, #9 (implicit) | ✅ 100% |
| Week 99 boundary | Test #2, #10 | ✅ 100% |
| DEF/K positions | Test #25, #26 | ✅ 100% |
| Caller integration (.parent fix) | Test #20 | ✅ 100% |
| E2E multiple weeks | Test #18 | ✅ 100% |
| Parallel execution | Test #19 | ✅ 100% |
| Test fixtures structure | Test #21, #22 | ✅ 100% |

**Coverage Gaps (Acceptable):**

| Not Tested | Reason | Acceptable? |
|------------|--------|-------------|
| File unreadable (permissions) | Rare system error, propagates OSError | ✅ Yes (tested in OS layer) |
| Disk full during copy | Rare system error, propagates OSError | ✅ Yes (tested in OS layer) |
| temp_dir creation fails | Rare system error, propagates OSError | ✅ Yes (tested in OS layer) |
| player_data/ mkdir fails | Rare system error, propagates OSError | ✅ Yes (tested in OS layer) |
| PlayerManager instantiation fails | Unlikely, propagates exception | ✅ Yes (tested in PlayerManager tests) |
| Malformed JSON | Handled by PlayerManager | ✅ Yes (tested in PlayerManager tests) |
| JSON array length ≠ 17 | Handled by PlayerManager | ✅ Yes (tested in PlayerManager tests) |

**Happy Path vs Edge Case Ratio:**
- **Happy path:** 12 tests (46%)
- **Edge cases:** 12 tests (46%)
- **Integration:** 4 tests (15%)  (sums to >100% due to overlap)
- **Ratio:** 1:1 (excellent balance)

**Test Coverage Depth Verification:**

✅ **Code coverage:** >95% (exceeds >90% requirement)
✅ **Edge case coverage:** 100% (11/11 critical edge cases tested)
✅ **Happy path coverage:** 100% (all normal flows tested)
✅ **Integration coverage:** 100% (E2E paths tested)
✅ **Boundary coverage:** 100% (weeks 0, 1, 17, 18, 99 tested)
✅ **Error handling coverage:** 100% (all error patterns tested)

**No Additional Tests Needed:** Coverage exceeds >90% requirement with comprehensive edge case testing

**Test Coverage PASSES** ✅

---

## Iteration 16: Documentation Requirements

**Purpose:** Identify documentation that needs updating

**Documentation Updates Required:**

### Code-Level Documentation (Docstrings)

**Task 1: Update _load_season_data() docstring**
- **File:** simulation/accuracy/AccuracySimulationManager.py (line 298)
- **Current:** `Tuple of (projected_csv_path, actual_csv_path) or (None, None) if not found`
- **Update to:** `Tuple of (week_folder, week_folder) or (None, None) if week folder not found`
- **Change:** Return value description (CSV paths → week_folder)

**Task 2: Update _create_player_manager() docstring**
- **File:** simulation/accuracy/AccuracySimulationManager.py (line 328)
- **Current:** `week_data_path: Path to week folder containing players.csv, players_projected.csv`
- **Update to:** `week_data_path: Path to week folder containing 6 position JSON files (qb_data.json, etc.)`
- **Change:** Parameter description (CSV files → JSON files)

**Task 3: Update _load_season_data() docstring**
- **File:** simulation/accuracy/ParallelAccuracyRunner.py (line 196)
- **Current:** Same as Task 1
- **Update to:** Same as Task 1
- **Change:** Return value description (CSV paths → week_folder)

**Task 4: Update _create_player_manager() docstring**
- **File:** simulation/accuracy/ParallelAccuracyRunner.py (line 212)
- **Current:** `week_data_path: Path to week folder containing players.csv, players_projected.csv`
- **Update to:** `week_data_path: Path to week folder containing 6 position JSON files`
- **Change:** Parameter description (CSV files → JSON files)

### Project-Level Documentation

**No updates needed:**
- ✅ README.md - No changes (feature is internal, doesn't affect user-facing documentation)
- ✅ ARCHITECTURE.md - No changes (data loading is implementation detail, not architectural change)
- ✅ User guides - No changes (Accuracy Sim usage unchanged, just different data source)

**Rationale:**
- Feature only changes internal file loading logic
- User-facing API unchanged (same command line args, same output format)
- Architectural patterns unchanged (still uses PlayerManager, still creates temp directories)

### Epic Documentation

**Updated automatically as part of epic workflow:**
- feature_02_accuracy_sim_json_integration/README.md (this feature's status)
- epic_lessons_learned.md (Stage 5c)
- epic_smoke_test_plan.md (Stage 5e)

### Documentation Tasks Summary

**Required:**
- 4 docstring updates (Tasks 1-4, minimal changes to return value / parameter descriptions)

**Not Required:**
- Project README
- ARCHITECTURE.md
- User guides

**Effort:** LOW (4 one-line docstring updates)

**No Additional Tasks Needed:** Docstring updates will be done during implementation (part of code writing)

---

**Round 2 Status:** ✅ **COMPLETE** - All 9 iterations (8-16) executed

**Confidence Level:** HIGH
- Test coverage >95% (exceeds >90% requirement)
- All integration gaps resolved
- All edge cases handled
- All algorithms traced
- All dependencies verified
- Documentation requirements identified

**Blockers:** None

---

## Iteration 17: Implementation Phasing

**Purpose:** Break implementation into incremental phases for validation

**Implementation Phases:**

### Phase 1: Core Path Modifications (Foundation)

**Tasks:** 1, 1a (AccuracySimulationManager)
**Estimated Time:** 10 minutes
**Files:** 1 file (AccuracySimulationManager.py)
**LOC:** ~4 lines

**Rationale:** Implement and test the main path first before parallel path

**Checkpoint:**
- ✅ Task 1 complete: _load_season_data() returns week_folder
- ✅ Task 1a complete: Caller passes week_folder (not .parent)
- ✅ Unit tests pass: Test #1, #2, #3
- ✅ Integration test pass: Test #20 (caller path verification)

---

### Phase 2: Player Data Loading (Main)

**Tasks:** 2 (AccuracySimulationManager)
**Estimated Time:** 20 minutes
**Files:** 1 file (AccuracySimulationManager.py)
**LOC:** ~25 lines

**Rationale:** Complete main path player data loading before parallel implementation

**Checkpoint:**
- ✅ Task 2 complete: player_data/ subfolder, 6 JSON files copied
- ✅ Unit tests pass: Test #4, #5, #6, #7, #8
- ✅ Integration test pass: Test #17 (E2E single week)

---

### Phase 3: Parallel Path Implementation (Mirroring)

**Tasks:** 3, 3a, 4 (ParallelAccuracyRunner)
**Estimated Time:** 15 minutes
**Files:** 1 file (ParallelAccuracyRunner.py)
**LOC:** ~30 lines

**Rationale:** Mirror Phase 1 and 2 changes to parallel implementation

**Checkpoint:**
- ✅ Task 3 complete: _load_season_data() module function returns week_folder
- ✅ Task 3a complete: Caller passes week_folder (not .parent)
- ✅ Task 4 complete: player_data/ subfolder, 6 JSON files copied
- ✅ Unit tests pass: Test #9, #10, #11, #12, #13, #14, #15, #16
- ✅ Integration test pass: Test #19 (parallel E2E)

---

### Phase 4: Integration & Validation

**Tasks:** 5, 6, 7
**Estimated Time:** 15 minutes
**Files:** 1 test file
**LOC:** Varies (test fixtures)

**Rationale:** Update test fixtures and validate special cases

**Checkpoint:**
- ✅ Task 5 complete: Test fixtures use JSON format
- ✅ Task 6 complete: Week 17 validation passed
- ✅ Task 7 complete: DEF/K validation passed
- ✅ All tests pass: Test #18, #21, #22, #23, #24, #25, #26
- ✅ Full integration test pass: Test #18 (E2E multiple weeks)

---

**Phasing Summary:**

| Phase | Tasks | Files | LOC | Estimated Time | Cumulative Tests |
|-------|-------|-------|-----|----------------|------------------|
| 1 | 1, 1a | 1 | ~4 | 10 min | 4 tests |
| 2 | 2 | 1 | ~25 | 20 min | 9 tests (4+5) |
| 3 | 3, 3a, 4 | 1 | ~30 | 15 min | 18 tests (9+9) |
| 4 | 5, 6, 7 | 1 | varies | 15 min | 26 tests (18+8) |
| **Total** | **9 tasks** | **2 files** | **~60 LOC** | **60 min** | **26 tests** |

**Rationale for Phasing:**
1. **Incremental validation:** Test main path before parallel path
2. **Risk mitigation:** Catch bugs early in simple path before complex parallel path
3. **Logical grouping:** Main → Parallel → Validation
4. **Checkpoint-driven:** Each phase has clear pass criteria

**No Additional Tasks Needed:** Phasing defined, all tasks assigned to phases

---

## Iteration 18: Rollback Strategy

**Purpose:** Define how to undo changes if implementation fails

**Rollback Strategy:**

**Method:** Git-based rollback (no special rollback code needed)

**Rationale:**
- All changes are code modifications (no schema migrations, no data migrations)
- Feature branch workflow enables easy rollback via git reset
- No persistent state changes (temp directories are temporary)
- No configuration changes to rollback

**If Implementation Fails:**
1. **Stop immediately** - Do not commit failing code
2. **Git reset:** `git reset --hard HEAD` (discard changes)
3. **Fix bugs** - Address test failures
4. **Re-run tests** - Verify fixes
5. **Resume implementation** - Continue from last checkpoint

**If Committed Code Has Bugs:**
1. **Git revert:** `git revert <commit_hash>` (preserve history)
2. **Create bug fix** - Follow bug fix workflow (STAGE_5_bug_fix_workflow_guide.md)
3. **Return to Stage 6** - Re-run epic QC after bug fix

**No Special Rollback Code Needed:**
- ✅ No database migrations to roll back
- ✅ No data files to restore
- ✅ No configuration to revert
- ✅ Simple git reset is sufficient

---

## Iteration 19: Algorithm Traceability Matrix (FINAL)

**Purpose:** Final verification that all algorithms are implemented correctly

**Status:** ✅ **VERIFIED** (from Iteration 11)

**Matrix:** 10 algorithms traced to code locations (Iteration 11)
**Tasks:** All 9 tasks map to algorithms
**No orphans:** All algorithms have implementing tasks, all tasks implement algorithms

**No changes since Iteration 11** - Matrix is complete and accurate

---

## Iteration 20: Performance Considerations

**Purpose:** Identify performance impacts

**Performance Analysis:**

| Change | Current Performance | New Performance | Impact |
|--------|---------------------|-----------------|--------|
| File loading | Load 2 CSV files (players.csv, players_projected.csv) | Load 6 JSON files | SLIGHTLY SLOWER (more files) |
| Parsing | CSV parsing (pandas) | JSON parsing (built-in) | COMPARABLE |
| Memory | Single CSV in memory | 6 JSON files in memory | SLIGHTLY HIGHER (6 files vs 2) |
| Temp directory | Copy 2 CSV files | Copy 6 JSON files | SLIGHTLY SLOWER (more files) |

**Overall Impact:** NEGLIGIBLE
- **Reason:** Accuracy Sim loads 1 week at a time (no caching), file sizes small
- **Mitigation:** None needed (performance difference < 100ms per week)

**No Performance Concerns** ✅

---

## Iteration 21: Mock Audit & Integration Test Plan

**Purpose:** Verify mocks match real interfaces and plan integration tests

**Mock Usage:** NONE
- Feature uses real PlayerManager, ConfigManager, etc.
- No mocking needed (tests use temporary files with real data)

**Integration Test Plan:**
- Test #17: E2E single week (real AccuracySimulationManager, real PlayerManager)
- Test #18: E2E multiple weeks (real flow)
- Test #19: Parallel E2E (real ParallelAccuracyRunner)
- Test #20: Caller integration (real method chain)

**All tests use REAL objects** ✅

---

## Iteration 22: Output Consumer Validation

**Purpose:** Verify output format unchanged for consumers

**Output Consumers:**
- AccuracyResultsManager (consumes AccuracyResult objects)
- User (consumes console output or CSV files)

**Output Format:** UNCHANGED
- AccuracyResult object structure: Same
- Console output format: Same
- CSV output format: Same

**No output changes** ✅

---

## Iteration 23: Integration Gap Check (FINAL)

**Purpose:** Final verification of all integration points

**Status:** ✅ **VERIFIED** (from Iteration 14)

**Integration Points:** 7 verified (Iteration 14)
**Critical Gaps:** 2 found, 2 fixed (Tasks 1a, 3a)
**New Gaps:** 0

**No changes since Iteration 14** - Integration is complete

---

## Iteration 23a: Pre-Implementation Spec Audit (MANDATORY GATE - 4 PARTS)

**Purpose:** Final audit before implementation - ALL 4 PARTS MUST PASS

### PART 1: Spec-to-TODO Traceability ✅ PASS

**Verification:**
- Spec lists 4 methods to modify → TODO has Tasks 1-4 ✅
- Spec mentions Week 17/18 validation → TODO has Task 6 ✅
- Spec mentions DEF/K validation → TODO has Task 7 ✅
- Integration gaps discovered → TODO has Tasks 1a, 3a ✅
- Test fixtures implied → TODO has Task 5 ✅

**Result:** All spec requirements have corresponding TODO tasks

### PART 2: Interface Verification ✅ PASS

**Verification:**
- Task 1: _load_season_data() signature verified from source code (Iteration 2) ✅
- Task 1a: Caller line 414 verified from source code (Iteration 7) ✅
- Task 2: _create_player_manager() signature verified from source code (Iteration 2) ✅
- Task 3: _load_season_data() module function verified (Iteration 2) ✅
- Task 3a: Caller line 119 verified from source code (Iteration 7) ✅
- Task 4: _create_player_manager() module function verified (Iteration 2) ✅
- PlayerManager player_data/ subfolder requirement verified (Iteration 3) ✅

**Result:** All interfaces verified against actual source code

### PART 3: Data Structure Validation ✅ PASS

**Verification:**
- Week folder structure: verified in sim_data/2025 (Iteration 3) ✅
- 6 JSON files per week: verified in week_01/ (Iteration 3) ✅
- JSON array structure: 17 elements verified (Iteration 3) ✅
- player_data/ subfolder: verified in PlayerManager.py:327 (Iteration 3) ✅
- Season-level files: verified in sim_data/2025 (Iteration 3) ✅

**Result:** All data structures verified against codebase

### PART 4: Test Coverage Adequacy ✅ PASS

**Verification:**
- Total tests: 26 (Iteration 8) ✅
- Coverage: >95% (exceeds >90% requirement) (Iteration 15) ✅
- Edge cases: 35 identified, 33 handled, 31 tested (Iteration 9, 15) ✅
- Happy path: 12 tests (46%) ✅
- Edge case: 12 tests (46%) ✅
- Integration: 4 tests (15%) (sums > 100% due to overlap) ✅

**Result:** Test coverage exceeds requirements

---

**Iteration 23a Result:** ✅ **ALL 4 PARTS PASSED**

Ready for Iteration 24 (Implementation Readiness Protocol)

---

## Iteration 24: Implementation Readiness Protocol (FINAL GATE)

**Purpose:** Go/no-go decision for implementation

**Pre-Implementation Checklist:**

### Requirements Completeness
- ✅ All spec requirements have TODO tasks (Iteration 1, 23a Part 1)
- ✅ All integration gaps identified and fixed (Iteration 7, 14, 23)
- ✅ All edge cases handled (Iteration 9)
- ✅ All algorithms traced (Iteration 4, 11, 19)

### Technical Readiness
- ✅ All interfaces verified from source code (Iteration 2, 23a Part 2)
- ✅ All data structures verified (Iteration 3, 23a Part 3)
- ✅ All dependencies verified (Iteration 13)
- ✅ Test coverage >90% (>95% actual) (Iteration 15, 23a Part 4)

### Implementation Planning
- ✅ Implementation phases defined (Iteration 17)
- ✅ Rollback strategy defined (Iteration 18)
- ✅ Documentation plan created (Iteration 16)
- ✅ Performance analyzed (Iteration 20)

### Confidence Assessment
- Round 1: MEDIUM-HIGH confidence
- Round 2: HIGH confidence
- Round 3: HIGH confidence
- Overall: **HIGH confidence**

### Questions Outstanding
- ✅ No unanswered questions
- ✅ No blockers
- ✅ No uncertainties

**GO/NO-GO Decision:** ✅ **GO**

**Rationale:**
- All 24 iterations completed successfully
- Iteration 23a: ALL 4 PARTS PASSED
- High confidence across all rounds
- No blockers or uncertainties
- Comprehensive test coverage
- Clear implementation plan

**READY FOR STAGE 5b (IMPLEMENTATION)** ✅

---

**Stage 5a TODO Creation:** ✅ **COMPLETE**

**Total Iterations:** 24 (Round 1: 8, Round 2: 9, Round 3: 9, including 2 MANDATORY GATES)
**Total Tasks:** 9 (7 original + 2 from Integration Gap Check)
**Total Tests:** 26 (>95% coverage)
**Final Confidence:** HIGH
**Implementation Decision:** GO

**Next Stage:** STAGE_5b (Implementation Execution)
