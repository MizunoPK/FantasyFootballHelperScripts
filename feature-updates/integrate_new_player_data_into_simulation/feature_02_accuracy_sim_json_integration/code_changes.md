# Feature 02: Accuracy Simulation JSON Integration - Code Changes

**Created:** 2026-01-02 (Stage 5b start)
**Status:** IN PROGRESS

---

## Interface Verification (Step 1 - Before Implementation)

**Verification Date:** 2026-01-02
**Method:** Read actual source code, copy-paste exact signatures

### Verified Interfaces

| Interface | File | Line | Signature | Verified |
|-----------|------|------|-----------|----------|
| _load_season_data (instance) | AccuracySimulationManager.py | 293-297 | `def _load_season_data(self, season_path: Path, week_num: int) -> Tuple[Optional[Path], Optional[Path]]` | ✅ |
| _create_player_manager (instance) | AccuracySimulationManager.py | 321-326 | `def _create_player_manager(self, config_dict: dict, week_data_path: Path, season_path: Path) -> PlayerManager` | ✅ |
| Caller location | AccuracySimulationManager.py | 414 | `player_mgr = self._create_player_manager(config_dict, projected_path.parent, season_path)` | ✅ |
| _load_season_data (module) | ParallelAccuracyRunner.py | 195 | `def _load_season_data(season_path: Path, week_num: int) -> Tuple[Path, Path]` | ✅ |
| _create_player_manager (module) | ParallelAccuracyRunner.py | 211 | `def _create_player_manager(config_dict: dict, week_data_path: Path, season_path: Path) -> PlayerManager` | ✅ |
| Caller location | ParallelAccuracyRunner.py | 119 | `player_mgr = _create_player_manager(config_dict, projected_path.parent, season_path)` | ✅ |

**All interfaces verified from source code** ✅

---

## Code Changes

### Phase 1: Core Path Modifications (AccuracySimulationManager.py)

**Completed:** 2026-01-02

#### Task 1: Update _load_season_data() method

**File:** `simulation/accuracy/AccuracySimulationManager.py`
**Lines Modified:** 293-313 (method body reduced from 27 lines to 21 lines)

**Changes:**
1. **Removed CSV file checking logic (lines 313-317 deleted):**
   - Removed: `projected_path = week_folder / "players_projected.csv"`
   - Removed: `actual_path = week_folder / "players.csv"`
   - Removed: `if not projected_path.exists() or not actual_path.exists(): return None, None`

2. **Changed return value (line 313):**
   - **Old:** `return projected_path, actual_path`
   - **New:** `return week_folder, week_folder`

3. **Updated docstring (line 306):**
   - **Old:** `Tuple of (projected_csv_path, actual_csv_path) or (None, None) if not found`
   - **New:** `Tuple of (week_folder, week_folder) or (None, None) if week folder not found`

**Why:** Method now returns the week folder path instead of specific CSV file paths, enabling JSON file loading by _create_player_manager()

**Impact:** Callers receive week_folder path which contains 6 JSON files instead of 2 CSV file paths

---

#### Task 1a: Update caller to pass week_folder (not .parent)

**File:** `simulation/accuracy/AccuracySimulationManager.py`
**Line Modified:** 408

**Changes:**
1. **Removed .parent accessor (line 408):**
   - **Old:** `player_mgr = self._create_player_manager(config_dict, projected_path.parent, season_path)`
   - **New:** `player_mgr = self._create_player_manager(config_dict, projected_path, season_path)`

**Why:** After Task 1, projected_path IS the week_folder (not a CSV file path), so .parent is no longer needed

**Impact:** _create_player_manager() now receives week_folder directly (critical integration fix)

---

#### Task 2: Update _create_player_manager() method

**File:** `simulation/accuracy/AccuracySimulationManager.py`
**Lines Modified:** 321-349 (CSV copying replaced with JSON subfolder pattern)

**Changes:**
1. **Updated docstring (line 326):**
   - **Old:** `week_data_path: Path to week folder containing players.csv, players_projected.csv`
   - **New:** `week_data_path: Path to week folder containing position JSON files`

2. **Created player_data/ subfolder (lines 337-339):**
   - **Added:** `player_data_dir = temp_dir / "player_data"`
   - **Added:** `player_data_dir.mkdir(exist_ok=True)`

3. **Replaced CSV iteration with explicit JSON copying (lines 341-349):**
   - **Old (lines 337-340):**
     ```python
     # Copy player data files from week folder
     for file in week_data_path.iterdir():
         if file.suffix == '.csv':
             shutil.copy(file, temp_dir / file.name)
     ```
   - **New (lines 341-349):**
     ```python
     # Copy 6 position JSON files from week folder to player_data/
     position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                       'te_data.json', 'k_data.json', 'dst_data.json']
     for filename in position_files:
         source_file = week_data_path / filename
         if source_file.exists():
             shutil.copy(source_file, player_data_dir / filename)
         else:
             self.logger.warning(f"Missing position file: {filename} in {week_data_path}")
     ```

**Why:** PlayerManager requires player_data/ subfolder with position-specific JSON files (6 files per week)

**Impact:** Temp directory now has correct structure for JSON-based PlayerManager initialization

---

### Phase 2: Player Data Loading (AccuracySimulationManager.py)

**Completed:** 2026-01-02

---

### Phase 3: Parallel Implementation (ParallelAccuracyRunner.py)

**Completed:** 2026-01-02

#### Task 3: Update _load_season_data() module function

**File:** `simulation/accuracy/ParallelAccuracyRunner.py`
**Lines Modified:** 195-206 (method body reduced from 14 lines to 7 lines)

**Changes:**
1. **Removed CSV file checking logic (lines 202-206 deleted):**
   - Removed: `projected_path = week_folder / "players_projected.csv"`
   - Removed: `actual_path = week_folder / "players.csv"`
   - Removed: `if not projected_path.exists() or not actual_path.exists(): return None, None`

2. **Changed return value (line 206):**
   - **Old:** `return projected_path, actual_path`
   - **New:** `return week_folder, week_folder`

3. **Updated docstring (lines 196-199):**
   - **Old:** `Load projected and actual data paths for a given week.`
   - **New:** `Load week folder path for a given week. Returns: Tuple of (week_folder, week_folder) or (None, None) if week folder not found`

**Why:** Module function mirrors AccuracySimulationManager._load_season_data() behavior for parallel processing

**Impact:** Parallel workers now return week folder paths containing JSON files

---

#### Task 3a: Update caller to pass week_folder (not .parent)

**File:** `simulation/accuracy/ParallelAccuracyRunner.py`
**Line Modified:** 119

**Changes:**
1. **Removed .parent accessor (line 119):**
   - **Old:** `player_mgr = _create_player_manager(config_dict, projected_path.parent, season_path)`
   - **New:** `player_mgr = _create_player_manager(config_dict, projected_path, season_path)`

**Why:** After Task 3, projected_path IS the week_folder (not a CSV file path), so .parent is no longer needed

**Impact:** _create_player_manager() now receives week_folder directly (critical integration fix for parallel workers)

---

#### Task 4: Update _create_player_manager() module function

**File:** `simulation/accuracy/ParallelAccuracyRunner.py`
**Lines Modified:** 210-235 (CSV copying replaced with JSON subfolder pattern)

**Changes:**
1. **Updated docstring (line 215):**
   - **Old:** `week_data_path: Path to week folder containing players.csv, players_projected.csv`
   - **New:** `week_data_path: Path to week folder containing position JSON files`

2. **Added logger initialization (line 218):**
   - **Added:** `logger = get_logger()`

3. **Created player_data/ subfolder (lines 223-225):**
   - **Added:** `player_data_dir = temp_dir / "player_data"`
   - **Added:** `player_data_dir.mkdir(exist_ok=True)`

4. **Replaced CSV iteration with explicit JSON copying (lines 227-235):**
   - **Old (lines 223-226):**
     ```python
     # Copy player data files from week folder
     for file in week_data_path.iterdir():
         if file.suffix == '.csv':
             shutil.copy(file, temp_dir / file.name)
     ```
   - **New (lines 227-235):**
     ```python
     # Copy 6 position JSON files from week folder to player_data/
     position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                       'te_data.json', 'k_data.json', 'dst_data.json']
     for filename in position_files:
         source_file = week_data_path / filename
         if source_file.exists():
             shutil.copy(source_file, player_data_dir / filename)
         else:
             logger.warning(f"Missing position file: {filename} in {week_data_path}")
     ```

**Why:** Module function mirrors AccuracySimulationManager._create_player_manager() behavior for parallel workers

**Impact:** Parallel workers create correct temp directory structure with player_data/ subfolder for JSON files

---

### Phase 4: Test Fixtures and Validation

**Completed:** 2026-01-02

#### Task 5: Update Integration Test Fixtures

**File:** `tests/integration/test_accuracy_simulation_integration.py`
**Lines Modified:** 91-246 (replaced CSV file creation with JSON file creation)

**Changes:**
1. **Removed CSV file creation (lines 95-125 deleted):**
   - Removed: `players.csv` creation with CSV format
   - Removed: `players_projected.csv` creation with CSV format

2. **Added JSON file creation (lines 91-246):**
   - **Added:** `player_data/` folder creation at season level (lines 91-198)
   - **Added:** Helper function `build_points_array()` for 17-element arrays (lines 96-108)
   - **Added:** Position-specific JSON data structures (QB, RB, WR, TE, K, DST) (lines 111-184)
   - **Added:** Week-specific JSON files (6 files per week, lines 200-246)

3. **JSON structure includes:**
   - All required fields: id, name, position, team, bye_week, fantasy_points, injury_status, average_draft_position, player_rating
   - New fields: locked, drafted_by
   - 17-element arrays: projected_points, actual_points

**Why:** Test fixtures must match new JSON-based player data format for integration tests

**Impact:** Integration tests now use correct JSON file structure, 12/12 tests pass

---

## Implementation Summary

**Stage 5b Status:** COMPLETE ✅
**Completion Date:** 2026-01-02

### Files Modified

1. **simulation/accuracy/AccuracySimulationManager.py** (2 methods + 1 caller line)
   - Lines 293-313: Modified _load_season_data() method (Task 1)
   - Line 408: Updated caller to remove .parent (Task 1a)
   - Lines 321-349: Modified _create_player_manager() method (Task 2)

2. **simulation/accuracy/ParallelAccuracyRunner.py** (2 functions + 1 caller line)
   - Lines 195-206: Modified _load_season_data() module function (Task 3)
   - Line 119: Updated caller to remove .parent (Task 3a)
   - Lines 210-235: Modified _create_player_manager() module function (Task 4)

3. **tests/integration/test_accuracy_simulation_integration.py** (test fixtures)
   - Lines 91-246: Replaced CSV fixtures with JSON fixtures (Task 5)

### Code Statistics

- **Total lines modified:** ~100 lines
- **Lines added:** ~80 lines (JSON handling, player_data/ creation, logging)
- **Lines removed:** ~50 lines (CSV file checking, iteration logic)
- **Net change:** +30 lines

### Test Results

- **Unit tests:** 2463/2463 passed (100%)
- **Integration tests:** 12/12 passed (100%)
- **Test coverage:** All modified code paths tested
- **Regression:** Zero test failures

### Implementation Notes

1. **Critical Integration Fix:** Tasks 1a and 3a (discovered in Stage 5a Iteration 7) were essential - without removing `.parent` calls, the implementation would have failed
2. **Parallel Consistency:** ParallelAccuracyRunner mirrors AccuracySimulationManager changes for multiprocessing compatibility
3. **Graceful Degradation:** Missing JSON files log warnings but don't crash (continues with available positions)
4. **Test Fixture Alignment:** Updated fixtures ensure future tests work with JSON format

### Validation Deferred to Stage 5c

- **Task 6:** Week 17/18 logic validation (smoke testing)
- **Task 7:** DEF/K position evaluation validation (smoke testing)

---

## 🚨 CRITICAL BUG FIX (Discovered During Stage 5cb QC Round 3)

**Discovered:** 2026-01-02 (Stage 5cb Round 3 - Skeptical Review)
**Severity:** CRITICAL - Feature would have been completely non-functional
**Status:** FIXED (QC restart required)

### Bug Description

**Problem:** Accuracy calculation code used deprecated `player.week_N_points` attributes instead of new `player.actual_points[N-1]` array API.

**Impact:** All players skipped during calculation (hasattr returns False) → MAE = NaN/empty → feature completely broken

**Root Cause:** Spec focused on data LOADING changes (CSV → JSON files) but missed data CONSUMPTION changes (how to access loaded player data)

### Files Modified (Bug Fix)

#### 1. simulation/accuracy/AccuracySimulationManager.py

**Lines Modified:** 451-456 (6 lines)

**OLD CODE (Broken):**
```python
# Get actual points for this specific week
week_points_attr = f'week_{week_num}_points'
if hasattr(player, week_points_attr):
    actual = getattr(player, week_points_attr)
    if actual is not None and actual > 0:
        actuals[player.id] = actual
```

**NEW CODE (Fixed):**
```python
# Get actual points for this specific week (from actual_points array)
# Array index: week 1 = index 0, week N = index N-1
if 1 <= week_num <= 17 and len(player.actual_points) >= week_num:
    actual = player.actual_points[week_num - 1]
    if actual is not None and actual > 0:
        actuals[player.id] = actual
```

**Changes:**
- Removed: `week_points_attr` string construction
- Removed: `hasattr()` and `getattr()` calls (always failed)
- Added: Array bounds check (`1 <= week_num <= 17` and `len() >= week_num`)
- Added: Direct array access (`player.actual_points[week_num - 1]`)
- Added: Comment explaining array indexing convention

#### 2. simulation/accuracy/ParallelAccuracyRunner.py

**Lines Modified:** 153-158 (6 lines)

**Changes:** Identical to AccuracySimulationManager.py fix (same pattern in parallel worker)

### Why This Bug Survived Multiple QC Stages

**Stages that missed it:**
- Stage 2 (Spec): Focused on file loading, not data consumption
- Stage 5a (24 iterations): No downstream consumption tracing
- Stage 5b (Implementation): Followed incomplete spec
- Stage 5ca (Smoke Testing): Verified data loading, not calculation output
- Stage 5cb Round 1 (Basic): Checked code structure, not runtime behavior
- Stage 5cb Round 2 (Deep): Checked edge cases, not API compatibility

**Stage that caught it:**
- **Stage 5cb Round 3 (Skeptical):** Asked "What could STILL be broken despite tests passing?"

### Test Results After Fix

- **Unit tests:** 2463/2463 passed (100%) ✅
- **Integration tests:** 12/12 passed (100%) ✅
- **Regression:** Zero test failures ✅

### Next Steps (QC Restart Protocol)

Per STAGE_5cb_qc_rounds_guide.md:
> **Round 3 QC Restart Rule:** If ANY critical issues found in Round 3 → RESTART from Smoke Testing (Stage 5ca)

**Required Actions:**
1. ✅ Bug fixed (completed)
2. ✅ Tests passing (verified above)
3. ⏳ RESTART from Stage 5ca with end-to-end MAE validation
4. ⏳ Re-execute QC Round 1 (Basic Validation)
5. ⏳ Re-execute QC Round 2 (Deep Verification)
6. ⏳ Re-execute QC Round 3 (Skeptical Review)

### Lessons Learned

See `lessons_learned.md` (lines 66-293) for complete analysis and prevention strategies.

**Key Takeaway:** Data format changes have TWO parts:
1. **Data Loading** (file paths, parsing) - what the spec caught ✅
2. **Data Consumption** (API changes, access patterns) - what the spec missed ❌

Both parts are mandatory. Future features must verify BOTH.

---

**Ready for Stage 5c RESTART:** Smoke Testing with end-to-end MAE validation → QC Rounds (all 3) → Final Review

