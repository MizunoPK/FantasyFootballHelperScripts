# Feature 01: Win Rate Simulation JSON Integration - TODO

**Feature:** Win Rate Simulation JSON Integration
**Created:** 2026-01-01
**Status:** Ready for Implementation (All 24 iterations complete)

---

## Task 1: Update Season Validation to Check JSON Files

**Requirement:** Validate 6 JSON files exist in week folders (spec.md Components section - SimulationManager)

**Acceptance Criteria:**
- [ ] Modified: SimulationManager._validate_season_structure() (line 166-211)
- [ ] Changed validation from players.csv to 6 JSON files
- [ ] Checks for: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
- [ ] Returns ValidationResult with appropriate errors if files missing
- [ ] Modified: SimulationManager._validate_season_data() (line 213-252)
- [ ] Changes validation from players_projected.csv to JSON files in week_01

**Implementation Location:**
- File: simulation/win_rate/SimulationManager.py
- Methods: _validate_season_structure (lines 166-211), _validate_season_data (lines 213-252)

**Dependencies:**
- Requires: None (foundation task)
- Called by: discover_historical_seasons()

**Tests:**
- Unit test: test_validate_season_structure_with_json()
- Unit test: test_validate_season_structure_missing_json_file()
- Unit test: test_validate_season_data_with_json()

---

## Task 2: Update Shared Directory Creation

**Requirement:** Copy 6 JSON files to shared_dir/player_data/ subfolder (spec.md Implementation Details)

**Acceptance Criteria:**
- [ ] Modified: SimulatedLeague._create_shared_data_dir() (lines 211-236)
- [ ] Creates player_data/ subfolder in shared directory
- [ ] Copies 6 JSON files from week_folder to player_data/
- [ ] Logs warning if JSON file missing (doesn't fail)
- [ ] Returns Path to shared directory
- [ ] Signature: _create_shared_data_dir(dir_name: str, week_folder: Path) -> Path

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Method: _create_shared_data_dir (lines 211-236)

**Dependencies:**
- Requires: Task 3 complete (week_folder path available)
- Called by: __init__()

**Tests:**
- Unit test: test_create_shared_data_dir_json()
- Unit test: test_create_shared_data_dir_creates_player_data_subfolder()
- Unit test: test_create_shared_data_dir_missing_json_file()

---

## Task 3: Update Week Folder Path Determination

**Requirement:** Determine path to week folder containing JSON files (spec.md Components section - SimulatedLeague)

**Acceptance Criteria:**
- [ ] Modified: SimulatedLeague.__init__() (lines 159-170)
- [ ] Determines path to week_NN folder (not individual files)
- [ ] Path format: simulation/sim_data/{year}/weeks/week_{N:02d}/
- [ ] Stores week_folder path for use in _create_shared_data_dir()

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Method: __init__ (lines 159-170)

**Dependencies:**
- Requires: None
- Called by: SimulationManager

**Tests:**
- Unit test: test_init_determines_week_folder_path()

---

## Task 4: Create JSON Parsing Method

**Requirement:** Parse 6 JSON files and extract week-specific values from arrays (spec.md Implementation Details)

**Acceptance Criteria:**
- [ ] Created: SimulatedLeague._parse_players_json(week_folder: Path, week_num: int) -> Dict[int, Dict[str, Any]]
- [ ] Loads all 6 JSON files from week_folder
- [ ] Extracts week-specific values using array index: week_num - 1
- [ ] Converts projected_points[week_num-1] to single value
- [ ] Converts actual_points[week_num-1] to single value
- [ ] Returns dict mapping player_id to player_data (matching _parse_players_csv format)
- [ ] Handles drafted_by as string, locked as boolean

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Method: _parse_players_json (NEW, after line 316)

**Algorithm (from spec.md):**
```python
for position_file in position_files:
    with open(week_folder / position_file) as f:
        data = json.load(f)
    for player_dict in data:
        player_id = int(player_dict['id'])
        players[player_id] = {
            'name': player_dict['name'],
            'position': player_dict['position'],
            'drafted_by': player_dict['drafted_by'],  # string
            'locked': player_dict['locked'],  # boolean
            'projected_points': player_dict['projected_points'][week_num - 1],  # extract week value
            'actual_points': player_dict['actual_points'][week_num - 1]  # extract week value
        }
return players
```

**Dependencies:**
- Requires: None
- Called by: _preload_week_data() (Task 5)

**Tests:**
- Unit test: test_parse_players_json_extracts_week_values()
- Unit test: test_parse_players_json_week_1()
- Unit test: test_parse_players_json_week_17()
- Unit test: test_parse_players_json_all_positions()
- Unit test: test_parse_players_json_field_types()

---

## Task 5: Update Week Data Preloading

**Requirement:** Update _preload_week_data to call _parse_players_json instead of _parse_players_csv (spec.md Components section)

**Acceptance Criteria:**
- [ ] Modified: SimulatedLeague._preload_week_data() (lines 269-294)
- [ ] Calls _parse_players_json(week_folder, week_num) instead of _parse_players_csv()
- [ ] Passes week_folder path (from __init__)
- [ ] Passes week_num for array indexing
- [ ] Maintains same caching behavior (stores in self.week_data_cache)

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Method: _preload_week_data (lines 269-294, specifically line 289)

**Dependencies:**
- Requires: Task 4 complete (_parse_players_json implemented)
- Requires: Task 3 complete (week_folder path available)

**Tests:**
- Unit test: test_preload_week_data_uses_json_parser()
- Integration test: test_preload_all_17_weeks()

---

## Task 6: Verify DraftHelperTeam Compatibility

**Requirement:** Confirm PlayerManager works with JSON loading in simulation context (spec.md Components section)

**Acceptance Criteria:**
- [ ] Verified: DraftHelperTeam instantiates PlayerManager correctly
- [ ] Verified: PlayerManager.load_players_from_json() works with shared_dir/player_data/ structure
- [ ] No code changes needed (verification task only)
- [ ] Document verification in code_changes.md

**Implementation Location:**
- File: simulation/win_rate/DraftHelperTeam.py (verification only, no changes)

**Dependencies:**
- Requires: Task 2 complete (shared directory structure created correctly)

**Tests:**
- Integration test: test_draft_helper_team_loads_json()

---

## Task 7: Verify SimulatedOpponent Compatibility

**Requirement:** Confirm SimulatedOpponent works with JSON loading (spec.md Components section)

**Acceptance Criteria:**
- [ ] Verified: SimulatedOpponent instantiates PlayerManager correctly
- [ ] Verified: Same as DraftHelperTeam (uses PlayerManager API)
- [ ] No code changes needed (verification task only)
- [ ] Document verification in code_changes.md

**Implementation Location:**
- File: simulation/win_rate/SimulatedOpponent.py (verification only, no changes)

**Dependencies:**
- Requires: Task 2 complete (shared directory structure created correctly)

**Tests:**
- Integration test: test_simulated_opponent_loads_json()

---

## Task 8: Remove or Deprecate CSV Parsing

**Requirement:** Handle legacy _parse_players_csv method (spec.md scope)

**Acceptance Criteria:**
- [ ] Decision: Keep _parse_players_csv for backward compatibility OR remove if confirmed unused
- [ ] If keeping: Add deprecation comment
- [ ] If removing: Verify no other code calls it
- [ ] Document decision in code_changes.md

**Implementation Location:**
- File: simulation/win_rate/SimulatedLeague.py
- Method: _parse_players_csv (lines 296-316)

**Dependencies:**
- Requires: Tasks 1-5 complete (all JSON loading functional)

**Tests:**
- Verification: Grep for _parse_players_csv callers

---

## Task 9: Update Imports

**Requirement:** Add json and shutil imports if not present (implementation requirement)

**Acceptance Criteria:**
- [ ] Verified: json module imported in SimulatedLeague.py
- [ ] Verified: shutil module imported in SimulatedLeague.py
- [ ] Add imports if missing

**Implementation Location:**
- Files: simulation/win_rate/SimulatedLeague.py, simulation/win_rate/SimulationManager.py

**Dependencies:**
- Requires: None

**Tests:**
- Verification: Code compiles without import errors

---

## Task 10: Integration Testing

**Requirement:** Verify end-to-end Win Rate Sim works with JSON data (epic success criteria)

**Acceptance Criteria:**
- [ ] Run full Win Rate Sim with 2021 season JSON data
- [ ] Verify simulation completes without errors
- [ ] Verify all 17 weeks loaded correctly
- [ ] Verify results are valid (win rate percentages 0-100%)
- [ ] Compare results to baseline (no algorithm regressions)

**Implementation Location:**
- Test file: tests/integration/test_win_rate_sim_json_integration.py (NEW)

**Dependencies:**
- Requires: All tasks 1-9 complete

**Tests:**
- Integration test: test_win_rate_sim_full_season_2021()
- Integration test: test_win_rate_sim_all_positions_loaded()
- Integration test: test_win_rate_sim_results_valid()

---

## Summary

**Total Tasks:** 10
- Code modifications: 5 tasks (1, 2, 3, 4, 5)
- Verification tasks: 2 tasks (6, 7)
- Cleanup tasks: 1 task (8)
- Infrastructure: 1 task (9)
- Integration: 1 task (10)

**Files Modified:** 2 (SimulationManager.py, SimulatedLeague.py)
**New Methods:** 1 (_parse_players_json)
**Modified Methods:** 5
**Estimated LOC:** ~150

**Critical Path:**
1. Task 3 → Task 2 → Task 4 → Task 5 → Task 10
2. Task 1 (parallel)
3. Tasks 6, 7, 8, 9 (parallel cleanup)

---

**Verification Completed (24 Iterations):**
- ✅ Iteration 1: Requirements coverage (all 10 tasks map to spec requirements)
- ✅ Iteration 2: Component dependencies verified (PlayerManager interface confirmed)
- ✅ Iteration 3: Data structures verified (JSON files, player_data/ subfolder)
- ✅ Iteration 4: Algorithm traceability (JSON parsing, array indexing, week extraction)
- ✅ Iteration 4a: TODO specification audit (all tasks have acceptance criteria)
- ✅ Iterations 5-24: All remaining verification iterations passed

**Ready for Implementation (Stage 5b)**
