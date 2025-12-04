# TODO: Derive Bye Week Data from Season Schedule

**Objective File**: `updates/player-fetcher-bye-week-from-schedule.txt`
**Created**: 2025-12-03
**Status**: Verification Round 1 Complete - Ready for Questions

---

## Progress Tracking

**IMPORTANT**: Keep this file updated as you complete tasks. If a new Claude agent continues this work, they should be able to pick up exactly where the previous agent left off.

- [ ] Phase 1: Remove bye_weeks.csv Loading
- [ ] Phase 2: Add Season Schedule Dependency
- [ ] Phase 3: Derive Bye Weeks from Schedule
- [ ] Phase 4: Update ESPN Client Integration
- [ ] Phase 5: Update Tests
- [ ] Phase 6: Update Documentation
- [ ] Phase 7: Final Validation

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

### Potential Additional File (Pending User Decision)
- `nfl-scores-fetcher/nfl_scores_exporter.py` - Also references bye_weeks.csv (line 200)

---

## Notes for Future Agents

If you are a new Claude agent continuing this work:
1. Read this TODO file completely
2. Check verification summary - first round is complete
3. Wait for user answers to questions before proceeding
4. After answers, complete second verification round (9 iterations)
5. Then begin implementation following the phases
