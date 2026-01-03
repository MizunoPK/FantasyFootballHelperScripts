# Codebase Investigation Findings

**Date:** 2026-01-01
**Purpose:** Answer checklist questions through codebase analysis

---

## Summary of Findings

All 7 checklist questions answered through codebase investigation. No user input required.

---

## Question 1: Week-Specific Array Index Mapping

**Answer:** Index 0 = Week 1, Index 1 = Week 2, ..., Index 16 = Week 17 (17 elements total)

**Evidence:**
- `historical_data_compiler/constants.py:88` - REGULAR_SEASON_WEEKS = 17
- `historical_data_compiler/json_exporter.py:305-312` - Loops `for week in range(1, REGULAR_SEASON_WEEKS + 1):` which is range(1, 18)
- `historical_data_compiler/json_exporter.py:328` - Bye week conversion: `bye_idx = player_data.bye_week - 1`
- Actual JSON file: `simulation/sim_data/2025/weeks/week_01/qb_data.json` has 17 elements in projected_points array

**Conclusion:** Standard 0-based indexing where index = week_num - 1

---

## Question 2: Data Extraction Timing

**Answer:** Extract week-specific values DURING parsing (Option A)

**Rationale:**
- JSON arrays already contain week-specific logic (past weeks = actuals, future weeks = projections/0.0)
- Current CSV approach: `_parse_players_csv()` returns single-value dict
- To maintain consistent interface, `_parse_players_json(week_num)` should extract the week-specific value and return same format as CSV version
- This keeps `_load_week_data()` unchanged

**Implementation:**
```python
def _parse_players_json(week_folder_path: Path, week_num: int) -> Dict[int, Dict[str, Any]]:
    """Parse JSON files and extract week-specific values."""
    # Load all 6 JSON files
    # For each player, extract projected_points[week_num - 1] and actual_points[week_num - 1]
    # Return dict with single values (matching CSV format)
```

---

## Question 3: Shared Directory Structure

**Answer:** Create `player_data/` subfolder in shared directories, copy all 6 JSON files per week (Option A modified)

**Evidence:**
- `league_helper/util/PlayerManager.py:327` - PlayerManager hardcodes: `player_data_dir = self.data_folder / 'player_data'`
- PlayerManager expects `data_folder/player_data/{position}_data.json` structure
- Cannot change PlayerManager (it's used by league helper)

**Implementation:**
```python
def _create_shared_data_dir(dir_name: str, week_folder_path: Path) -> Path:
    """Create shared directory with player_data/ subfolder and 6 JSON files."""
    shared_dir = Path(tempfile.mkdtemp(prefix=dir_name))
    player_data_dir = shared_dir / 'player_data'
    player_data_dir.mkdir()

    # Copy 6 JSON files from week folder to player_data/
    for position_file in ['qb_data.json', 'rb_data.json', ...]:
        src = week_folder_path / position_file
        dst = player_data_dir / position_file
        shutil.copy(src, dst)

    # Copy other required files (config, team_data, etc.)
    return shared_dir
```

---

## Question 4: PlayerManager Compatibility

**Answer:** PlayerManager DOES hardcode `player_data/` subfolder - we must create this structure (Option B)

**Evidence:**
- `league_helper/util/PlayerManager.py:327` - `player_data_dir = self.data_folder / 'player_data'`
- `league_helper/util/PlayerManager.py:342` - `filepath = player_data_dir / position_file`
- PlayerManager expects: `{data_folder}/player_data/{position}_data.json`
- Simulation will pass `shared_dir` as data_folder, so files must be at `shared_dir/player_data/`

**No PlayerManager modifications needed** - just structure shared directories correctly.

---

## Question 5: Error Handling - Missing JSON Files

**Answer:** Different behavior for validation vs runtime (Option C)

**Evidence:**
- `simulation/win_rate/SimulationManager.py:210-211` - Current CSV validation: `raise FileNotFoundError` if players.csv missing
- `league_helper/util/PlayerManager.py:346` - Runtime: `logger.warning` and skip if JSON file missing

**Implementation:**
- **Validation (_validate_season_structure):** Fail loud if ANY of 6 JSON files missing for ANY week
- **Runtime (_preload_week_data):** Log warning and skip week if files missing (current CSV behavior)

**Rationale:** Validation ensures data integrity before simulation starts. Runtime handles gracefully for partial data scenarios.

---

## Question 6: Field Type Conversion

**Answer:** NO conversion needed - FantasyPlayer.from_json() handles boolean/string correctly (Option A)

**Evidence:**
- `utils/FantasyPlayer.py:250` - `locked = data.get('locked', False)` - Loads boolean directly
- `utils/FantasyPlayer.py:240` - `drafted_by = data.get('drafted_by', '')` - Loads string directly
- `utils/FantasyPlayer.py:96-97` - Class fields: `drafted_by: str = ""`, `locked: bool = False`

**Conclusion:** from_json() already handles new JSON field types. No conversion needed in simulation code.

---

## Question 7: Array Length Validation

**Answer:** Arrays have 17 elements (weeks 1-17), pad/truncate if different (Option B)

**Evidence:**
- `historical_data_compiler/constants.py:88` - REGULAR_SEASON_WEEKS = 17
- `utils/FantasyPlayer.py:235-237` - from_json() already pads/truncates:
  ```python
  projected_points = (projected_points + [0.0] * 17)[:17]
  actual_points = (actual_points + [0.0] * 17)[:17]
  ```
- Actual JSON files contain 17 elements

**Implementation:** Rely on FantasyPlayer.from_json() to handle array validation. No additional validation needed in simulation code.

---

## Impact on Implementation

**Changes Confirmed:**
1. `_parse_players_json(week_folder, week_num)` - Extract week-specific values from arrays using index = week_num - 1
2. `_create_shared_data_dir(dir_name, week_folder)` - Create `player_data/` subfolder, copy 6 JSON files
3. `_validate_season_structure()` - Validate all 6 JSON files exist per week
4. `_preload_week_data()` - Call `_parse_players_json()` instead of `_parse_players_csv()`

**No Changes Needed:**
- PlayerManager - already handles JSON correctly
- DraftHelperTeam - uses PlayerManager API
- SimulatedOpponent - uses PlayerManager API
- `_load_week_data()` - receives same format from cache

---

**Conclusion:** All questions answered. Ready to update spec.md with concrete implementation details.
