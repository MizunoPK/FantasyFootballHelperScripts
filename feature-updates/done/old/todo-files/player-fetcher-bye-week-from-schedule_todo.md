# TODO: Derive Bye Week Data from Season Schedule

**Objective File**: `updates/player-fetcher-bye-week-from-schedule.txt`
**Created**: 2025-12-03
**Status**: Verification Round 2 In Progress (User Answers Received)

---

## User Answers (Received 2025-12-04)

**Q1: NFL Scores Exporter** → **Option A: Leave as-is**
- Do not update nfl-scores-fetcher
- It will silently fail if bye_weeks.csv missing (acceptable)

**Q2: Error Handling Strictness** → **Option A: Fatal error**
- Raise `FileNotFoundError` if season_schedule.csv missing
- User must run schedule-data-fetcher first

---

## Progress Tracking

**STATUS: COMPLETE** ✅

- [x] Phase 1: Remove bye_weeks.csv Loading
- [x] Phase 2: Add Season Schedule Dependency
- [x] Phase 3: Derive Bye Weeks from Schedule
- [x] Phase 4: Update ESPN Client Integration (no changes needed - interface unchanged)
- [x] Phase 5: Update Tests (24 tests pass)
- [x] Phase 6: Update Documentation
- [x] Phase 7: Final Validation (2249/2249 tests pass - 100%)

---

## Phase 1: Remove bye_weeks.csv Loading

### Task 1.1: Remove `_load_bye_weeks()` method
- **File**: `player-data-fetcher/player_data_fetcher_main.py`
- **Action**: Delete the `_load_bye_weeks()` method entirely
- **Lines**: 144-202 (verified via skeptical re-verification)
- **Method signature**: `def _load_bye_weeks(self) -> Dict[str, int]:`

### Task 1.2: Remove `self.bye_weeks` initialization that loads from CSV
- **File**: `player-data-fetcher/player_data_fetcher_main.py`
- **Action**: Remove/replace `self.bye_weeks = self._load_bye_weeks()` line
- **Line**: 127 (verified)
- **Note**: This will be replaced in Phase 3, not just removed

### Task 1.3: Remove failing tests for `_load_bye_weeks()`
- **File**: `tests/player-data-fetcher/test_player_data_fetcher_main.py`
- **Action**: Remove entire `TestLoadByeWeeks` class
- **Class location**: Lines 107-167 (verified)
- **Tests to remove** (4 tests):
  - `test_load_bye_weeks_success` (line 112)
  - `test_load_bye_weeks_invalid_week_numbers` (line 131)
  - `test_load_bye_weeks_file_not_found` (line 149)
  - `test_load_bye_weeks_read_exception` (line 159)

---

## Phase 2: Add Season Schedule Dependency

### Task 2.1: Add schedule file path check on initialization
- **File**: `player-data-fetcher/player_data_fetcher_main.py`
- **Action**: Check if `data/season_schedule.csv` exists in `__init__`
- **Location**: After line 124 (after `self.script_dir` is set)
- **Path to check**: `self.script_dir.parent / "data" / "season_schedule.csv"`
- **Verified**: File exists at `data/season_schedule.csv` (5933 bytes)

### Task 2.2: Implement error with clear message
- **File**: `player-data-fetcher/player_data_fetcher_main.py`
- **Action**: Raise `FileNotFoundError` if season_schedule.csv missing
- **Error message**:
  ```
  Error: season_schedule.csv not found at {path}
  Please run the schedule-data-fetcher first to generate this file:
    python run_scores_fetcher.py
  ```
- **Note**: This is a FATAL error - unlike bye_weeks.csv which was optional

---

## Phase 3: Derive Bye Weeks from Schedule

### Task 3.1: Implement `_derive_bye_weeks_from_schedule()` method
- **File**: `player-data-fetcher/player_data_fetcher_main.py`
- **Action**: Create new method to derive bye weeks from schedule
- **Location**: Replace lines 144-202 (where `_load_bye_weeks` was)
- **Schedule file format** (verified):
  ```csv
  week,team,opponent
  1,ARI,NO
  1,ATL,TB
  ...
  ```
- **Logic**:
  1. Load season_schedule.csv using pandas
  2. Get unique teams from 'team' column
  3. For each team, get set of weeks they play (weeks where team appears)
  4. NFL regular season is weeks 1-18
  5. Bye week = the week in 1-18 that is NOT in team's weeks
  6. Return dict: `{team_abbrev: bye_week_number}`

### Task 3.2: Update `self.bye_weeks` initialization
- **File**: `player-data-fetcher/player_data_fetcher_main.py`
- **Action**: Change line 127 to call new method
- **Before**: `self.bye_weeks = self._load_bye_weeks()`
- **After**: `self.bye_weeks = self._derive_bye_weeks_from_schedule(schedule_path)`

### Task 3.3: Add validation for derived bye weeks
- **File**: `player-data-fetcher/player_data_fetcher_main.py`
- **Action**: Add validation within `_derive_bye_weeks_from_schedule()`
- **Validations**:
  - Verify exactly 32 teams found
  - Log warning if team has no bye week (plays all 18 weeks - shouldn't happen)
  - Log warning if team has multiple bye weeks (missing games - data issue)
  - Log info showing bye week distribution

---

## Phase 4: Update ESPN Client Integration

### Task 4.1: Verify ESPN client interface remains unchanged
- **File**: `player-data-fetcher/espn_client.py`
- **Action**: Verify line 228 `client.bye_weeks = self.bye_weeks` still works
- **Expected**: No code changes needed - interface unchanged
- **Verification**: The bye_weeks dict format `{team: week}` is identical

### Task 4.2: Update ESPN client docstrings
- **File**: `player-data-fetcher/espn_client.py`
- **Action**: Update docstring at line 202 that mentions bye weeks source
- **Line 202**: "- Bye week mappings for NFL teams" - update to mention season schedule source

---

## Phase 5: Update Tests

### Task 5.1: Remove old bye_weeks.csv loading tests
- **File**: `tests/player-data-fetcher/test_player_data_fetcher_main.py`
- **Action**: Delete entire `TestLoadByeWeeks` class (lines 107-167)
- **Tests being removed** (4 tests):
  - `test_load_bye_weeks_success`
  - `test_load_bye_weeks_invalid_week_numbers`
  - `test_load_bye_weeks_file_not_found`
  - `test_load_bye_weeks_read_exception`

### Task 5.2: Update tests that mock `_load_bye_weeks`
- **File**: `tests/player-data-fetcher/test_player_data_fetcher_main.py`
- **Action**: Update `TestNFLProjectionsCollectorInit` to mock new method
- **Lines**: 85, 99, 177 - patch `_load_bye_weeks` → patch `_derive_bye_weeks_from_schedule`

### Task 5.3: Add tests for `_derive_bye_weeks_from_schedule()`
- **File**: `tests/player-data-fetcher/test_player_data_fetcher_main.py`
- **Action**: Create new `TestDeriveBveWeeksFromSchedule` class
- **New tests to create**:
  - `test_derive_bye_weeks_from_schedule_success` - Valid schedule returns correct bye weeks
  - `test_derive_bye_weeks_missing_schedule_file_error` - Missing file raises FileNotFoundError
  - `test_derive_bye_weeks_validates_32_teams` - Logs warning if not 32 teams
  - `test_derive_bye_weeks_handles_team_with_no_bye` - Handles edge case
  - `test_derive_bye_weeks_handles_team_with_multiple_byes` - Handles data issues

### Task 5.4: Run all tests and ensure 100% pass rate
- **Command**: `python tests/run_all_tests.py`
- **Requirement**: All 2248+ tests must pass

---

## Phase 6: Update Documentation

### Task 6.1: Update LeagueHelperManager docstring
- **File**: `league_helper/LeagueHelperManager.py`
- **Lines to update**: 63 and 195
- **Action**: Remove "bye_weeks.csv: Bye week schedule" from data file lists

### Task 6.2: Update CLAUDE.md if needed
- **File**: `CLAUDE.md`
- **Action**: Search for bye_weeks.csv references
- **Status**: Checked - NOT mentioned in CLAUDE.md (no changes needed)

### Task 6.3: Update player_data_fetcher_main.py docstrings
- **File**: `player-data-fetcher/player_data_fetcher_main.py`
- **Action**: Update module docstring and method docstrings to reference season_schedule.csv

---

## Phase 7: Final Validation

### Task 7.1: Run full test suite
- **Command**: `python tests/run_all_tests.py`
- **Requirement**: 100% pass rate (all 2248+ tests)

### Task 7.2: Manual integration test
- **Action**: Run player fetcher and verify bye weeks are derived correctly
- **Command**: `python run_player_fetcher.py`
- **Verification**: Check logs for "Derived bye weeks for 32 teams" message

### Task 7.3: Verify no active references to bye_weeks.csv remain
- **Action**: Search codebase for "bye_weeks.csv"
- **Expected references** (acceptable):
  - Git history (unavoidable)
  - TODO/update files (documentation)
- **Unexpected references** (must fix):
  - Source code files (except nfl_scores_exporter.py if decided not to change)

---

## Verification Summary

**First Verification Round: COMPLETE (7/7 iterations)**

### Iteration 1: Initial Research
- Located `_load_bye_weeks()` method: lines 144-202
- Located initialization: line 127
- Located test class: lines 107-167
- Verified schedule file format: `week,team,opponent`

### Iteration 2: Deep Dive
- Error handling pattern: `FileNotFoundError` used in codebase
- Logging pattern: `self.logger.info/warning/error()`
- CSV reading: `read_csv_with_validation` or `pd.read_csv`

### Iteration 3 & 4: Integration Points & Technical Details
- Entry point: `run_player_fetcher.py` → `player_data_fetcher_main.py`
- Data flow: `__init__` → `self.bye_weeks` → `collect_all_projections` → `client.bye_weeks`
- ESPN client usage: line 1867 `bye_week = self.bye_weeks.get(team)`

### Iteration 5: End-to-End Data Flow
```
Entry: run_player_fetcher.py
  → subprocess.run(player_data_fetcher_main.py)
  → main() at line 532
    → NFLProjectionsCollector(settings) at line 545
      → __init__() at line 107
        → self.bye_weeks = self._load_bye_weeks() at line 127  ← CHANGE HERE
    → collector.collect_all_projections() at line 546
      → client.bye_weeks = self.bye_weeks at line 228
      → ESPN client uses bye_weeks at line 1867
Output: players.csv with bye_week column
```

### Iteration 6: Skeptical Re-Verification
- ✅ Line 144: `def _load_bye_weeks(self) -> Dict[str, int]:` (verified)
- ✅ Line 127: `self.bye_weeks = self._load_bye_weeks()` (verified)
- ✅ Line 107: `class TestLoadByeWeeks:` (verified)
- ✅ File exists: `data/season_schedule.csv` (5933 bytes)
- ✅ Format verified: `week,team,opponent`

### Iteration 7: Integration Gap Check
| New Component | File | Called By | Modification Task |
|---------------|------|-----------|-------------------|
| `_derive_bye_weeks_from_schedule()` | player_data_fetcher_main.py | `__init__()` line 127 | Task 3.2 |
| Schedule file check | player_data_fetcher_main.py | `__init__()` ~line 125 | Task 2.1 |

**No orphan code** - new method replaces old method in same location.

---

## Questions Identified for User

1. **nfl-scores-fetcher/nfl_scores_exporter.py**: This file also looks for `bye_weeks.csv` at `shared_files/bye_weeks.csv` (line 200). Should we also update this to derive from season_schedule.csv, or leave it as is (it's optional - silently fails if missing)?

---

## Integration Matrix

| New Component | File | Called By | Caller Modification |
|---------------|------|-----------|---------------------|
| `_derive_bye_weeks_from_schedule()` | player_data_fetcher_main.py:144 | `__init__()` | Line 127: replace `_load_bye_weeks()` |
| Schedule file validation | player_data_fetcher_main.py:~125 | `__init__()` | New code before line 127 |

---

## Files to Modify (Final List)

1. `player-data-fetcher/player_data_fetcher_main.py` - Main implementation
2. `tests/player-data-fetcher/test_player_data_fetcher_main.py` - Test updates
3. `league_helper/LeagueHelperManager.py` - Docstring cleanup (lines 63, 195)
4. `player-data-fetcher/espn_client.py` - Docstring update (line 202)

### Out of Scope (Per User Answer Q1)
- `nfl-scores-fetcher/nfl_scores_exporter.py` - Leave as-is, will silently fail without bye_weeks.csv

---

## Second Verification Round: COMPLETE (9/9 iterations)

### Iterations 8-11: Standard Verification with User Answers (POST-IMPLEMENTATION)

**User Answers Applied**:
- Q1 (nfl-scores-fetcher): Leave as-is - no changes needed ✅
- Q2 (Error handling): Fatal error if season_schedule.csv missing ✅

**Requirements Cross-Reference (All 12 requirements verified)**:
| # | Requirement | Implementation | Status |
|---|-------------|----------------|--------|
| 1 | Remove `_load_bye_weeks()` method | Replaced with `_derive_bye_weeks_from_schedule()` | ✅ |
| 2 | Remove CSV file loading references | No `bye_weeks.csv` in player-data-fetcher | ✅ |
| 3 | Check if `season_schedule.csv` exists | Line 128: `if not schedule_path.exists()` | ✅ |
| 4 | Raise error with specific message | Lines 129-135: `FileNotFoundError` | ✅ |
| 5 | Error includes path + instructions | "python run_scores_fetcher.py" | ✅ |
| 6 | Load season_schedule.csv | Line 183: `pd.read_csv(schedule_path)` | ✅ |
| 7 | For each team, find missing week | Lines 192-208: loop + set difference | ✅ |
| 8 | Build bye_weeks dict | Line 201: `bye_weeks[team] = ...` | ✅ |
| 9 | Validate 32 teams | Lines 188-189: warning logged | ✅ |
| 10 | Log warning for no bye | Line 203: warning | ✅ |
| 11 | Log warning for multiple byes | Line 206: warning | ✅ |
| 12 | ESPN client interface unchanged | Line 243: `client.bye_weeks = self.bye_weeks` | ✅ |

### Iteration 12: End-to-End Data Flow Re-verification (POST-IMPLEMENTATION)

```
Entry: run_player_fetcher.py (line 36)
  → subprocess.run(player_data_fetcher_main.py)
  → main() at line 547
    → NFLProjectionsCollector(settings) at line 560
      → __init__() at line 113
        → Check schedule_path.exists() (line 128) ✅
        → _derive_bye_weeks_from_schedule(schedule_path) (line 138) ✅
          → pd.read_csv(schedule_path) (line 183)
          → For each team, find missing week (lines 192-208)
          → Returns bye_weeks dict ✅
    → collector.collect_all_projections() at line 561
      → client.bye_weeks = self.bye_weeks at line 243 ✅
      → ESPN client uses bye_weeks.get(team) at line 1867 ✅
Output: players.csv with bye_week column populated ✅
```

### Iteration 13: Skeptical Re-verification (POST-IMPLEMENTATION)

**Fresh codebase searches (assume nothing is correct)**:
| Search | Expected | Actual | Status |
|--------|----------|--------|--------|
| `_load_bye_weeks` in player-data-fetcher | None | None | ✅ |
| `bye_weeks.csv` in player-data-fetcher | None | None | ✅ |
| `_derive_bye_weeks_from_schedule` exists | Yes | Lines 138, 155 | ✅ |
| `_load_bye_weeks` in tests | None | None | ✅ |
| `TestLoadByeWeeks` class | None | None | ✅ |
| `season_schedule.csv` exists | Yes | 545 lines | ✅ |
| Format correct | `week,team,opponent` | `week,team,opponent` | ✅ |
| 32 teams × 17 games | 544 rows | 544 rows | ✅ |

### Iteration 14: Integration Gap Check (POST-IMPLEMENTATION)

| Component | File | Integration | Status |
|-----------|------|-------------|--------|
| Source method | `_derive_bye_weeks_from_schedule` (main:155) | Created | ✅ |
| Instance storage | `self.bye_weeks` (main:138) | Connected | ✅ |
| ESPN client pass | `client.bye_weeks = self.bye_weeks` (main:243) | Connected | ✅ |
| ESPN client store | `self.bye_weeks` (espn_client:215) | Receives | ✅ |
| ESPN client use | `bye_weeks.get(team)` (espn_client:1867) | Uses | ✅ |
| Schedule generator | `ScheduleFetcher._identify_bye_weeks` | Separate (generates CSV) | ✅ |
| NFL scores exporter | `nfl_scores_exporter.py` | Left as-is per Q1 | ✅ |

**No orphan code. No broken integrations.**

### Iterations 15-16: Final Verification (POST-IMPLEMENTATION)

**Implementation Verification Checklist (ALL COMPLETE)**:
- [x] Delete `_load_bye_weeks()` method (lines 144-202)
- [x] Add schedule file existence check (line 128)
- [x] Create `_derive_bye_weeks_from_schedule()` method (line 155)
- [x] Update initialization to call new method (line 138)
- [x] Delete `TestLoadByeWeeks` class
- [x] Update patches to new method name
- [x] Create new `TestDeriveBveWeeksFromSchedule` class (5 tests)
- [x] Update LeagueHelperManager docstrings (lines 63, 195)
- [x] Run full test suite: **2249/2249 tests pass (100%)**
- [x] Verify no orphan `bye_weeks.csv` references in source code

---

## Notes for Future Agents

If you are a new Claude agent continuing this work:
1. Read this TODO file completely
2. Both verification rounds are complete (16 total iterations)
3. User answers received and integrated
4. Ready for implementation - follow phases in order
5. Run tests after each phase
