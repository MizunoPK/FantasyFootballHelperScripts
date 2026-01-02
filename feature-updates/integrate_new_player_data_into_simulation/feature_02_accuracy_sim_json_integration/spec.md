# Feature 02: Accuracy Simulation JSON Integration - Technical Specification

**Version:** 2.0 (Stage 2 Deep Dive)
**Last Updated:** 2026-01-01
**Status:** Deep Dive in progress

---

## Objective

Update the Accuracy Simulation subsystem to load player data from position-specific JSON files instead of the legacy CSV format. Maintain same accuracy evaluation functionality with new JSON data structure.

---

## Scope

**What's included in THIS feature:**
- Update `AccuracySimulationManager.py` to copy JSON files instead of CSV files
- Update `ParallelAccuracyRunner.py` to copy JSON files instead of CSV files
- Create `player_data/` subfolder in temp directories for PlayerManager compatibility
- Handle new JSON file structure (6 position files per week)
- Maintain all existing accuracy calculation logic (no algorithm changes)

**What's NOT included:**
- Changes to accuracy calculation algorithms
- Changes to MAE computation logic
- Updates to Win Rate Sim (that's Feature 1)
- Adding new accuracy metrics
- Changes to AccuracyCalculator or AccuracyResultsManager

**Dependencies:**
- **Prerequisites:** None (parallel to Feature 1)
- **Blocks:** None
- **Alignment:** Uses same PlayerManager JSON loading as Feature 1

---

## Current Implementation (CSV-Based)

### Data Loading Flow

**See:** `research/ACCURACY_SIM_DISCOVERY.md` for complete discovery findings

**Current flow (per config evaluation):**
1. **_get_week_data_paths()** - Returns paths to players.csv and players_projected.csv
2. **_create_player_manager()** - Creates temp directory, copies CSV files
3. **PlayerManager** instantiation - Loads from temp directory
4. **AccuracyCalculator** - Calculates MAE using PlayerManager data

**Key difference from Win Rate Sim:**
- Accuracy Sim does NOT pre-load/cache week data
- Loads ONE week at a time per config evaluation
- Creates fresh temp directory for EACH evaluation

**Simpler than Win Rate Sim:**
- No caching logic needed
- No JSON parsing needed (just file copying)
- PlayerManager handles JSON loading

---

## Data Structure Changes

**Same as Feature 1 - see Feature 1 spec.md for details**

**CSV → JSON:**
- 2 CSV files → 6 JSON files per week
- drafted_by: int/empty → string
- locked: "0"/"1" → boolean
- projected_points: single value → array[17]
- actual_points: single value → array[17]

**Array indexing:**
- Index 0 = Week 1, Index 16 = Week 17
- Same as Feature 1 (see research/CODEBASE_INVESTIGATION_FINDINGS.md)

---

## Components Affected

### 1. AccuracySimulationManager.py

**Method:** `_get_week_data_paths(season_path, week_num)` (lines 298-319)
- **Current behavior:** Returns `(projected_csv_path, actual_csv_path)` tuple
- **Change needed:** Return `week_folder` path instead (all JSON files are in that folder)
- **OR:** Return (week_folder, week_folder) for compatibility with existing signature

**Method:** `_create_player_manager(config_dict, week_data_path, season_path)` (lines 327-380)
- **Current behavior:** Copies all `.csv` files from week folder (lines 343-346)
- **Change needed:** Create `player_data/` subfolder, copy 6 JSON files
- **Lines affected:** 343-346

### 2. ParallelAccuracyRunner.py

**Method:** `_get_week_data_paths_worker(season_path, week_num)` (lines 192-208)
- **Current behavior:** Same as AccuracySimulationManager version
- **Change needed:** Same as AccuracySimulationManager

**Method:** `_create_player_manager_worker(config_dict, week_data_path, season_path)` (lines 212-271)
- **Current behavior:** Copies all `.csv` files from week folder (lines 224-226)
- **Change needed:** Create `player_data/` subfolder, copy 6 JSON files
- **Lines affected:** 224-226

### 3. AccuracyCalculator.py

**No changes needed:**
- Receives player_data from PlayerManager
- Doesn't interact with files directly
- PlayerManager abstracts data format

### 4. AccuracyResultsManager.py

**No changes needed:**
- Only processes AccuracyResult objects
- Doesn't interact with player data files

---

## Implementation Details

**Status:** ✅ ALL QUESTIONS RESOLVED via Feature 1 investigation + codebase analysis

**See:**
- `research/ACCURACY_SIM_DISCOVERY.md` for Accuracy Sim specifics
- `research/CODEBASE_INVESTIGATION_FINDINGS.md` (Feature 1) for shared details

---

### Temp Directory Structure

**[UPDATED based on feature_01_win_rate_sim_json_integration implementation - 2026-01-02]**

**Required structure:** `temp_dir/player_data/{position}_data.json`

**Why:** PlayerManager hardcodes `player_data/` subfolder (same as Feature 1)

**Update from feature_01 implementation:**
- Error handling: Code should actively log warnings for missing JSON files (not assume PlayerManager will log)
- Logging pattern: `self.logger.warning(f"Missing {position_file} in {week_data_path}")`
- This matches the proactive logging approach established in feature_01 (SimulatedLeague.py:235)

**Implementation:**
```python
def _create_player_manager(config_dict, week_data_path, season_path):
    """Create PlayerManager with temporary directory containing JSON files."""
    import tempfile

    temp_dir = Path(tempfile.mkdtemp(prefix="accuracy_sim_"))

    # Create player_data/ subfolder (REQUIRED by PlayerManager)
    player_data_dir = temp_dir / 'player_data'
    player_data_dir.mkdir()

    # Copy 6 JSON files from week folder to player_data/
    position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                      'te_data.json', 'k_data.json', 'dst_data.json']
    for position_file in position_files:
        src = week_data_path / position_file
        dst = player_data_dir / position_file
        if src.exists():
            shutil.copy(src, dst)
        else:
            # Log warning and continue (following pattern from feature_01)
            self.logger.warning(f"Missing {position_file} in {week_data_path}")

    # Copy season-level files (unchanged from CSV version)
    season_schedule = season_path / "season_schedule.csv"
    if season_schedule.exists():
        shutil.copy(season_schedule, temp_dir / "season_schedule.csv")

    game_data = season_path / "game_data.csv"
    if game_data.exists():
        shutil.copy(game_data, temp_dir / "game_data.csv")

    team_data_source = season_path / "team_data"
    if team_data_source.exists():
        shutil.copytree(team_data_source, temp_dir / "team_data")

    # Create config file (unchanged)
    config_path = temp_dir / "league_config.json"
    with open(config_path, 'w') as f:
        json.dump(config_dict, f, indent=2)

    # Create PlayerManager (unchanged)
    config_mgr = ConfigManager(temp_dir)
    schedule_mgr = SeasonScheduleManager(temp_dir)
    team_data_mgr = TeamDataManager(temp_dir, config_mgr, schedule_mgr, config_mgr.current_nfl_week)
    pm = PlayerManager(temp_dir, config_mgr, team_data_mgr, schedule_mgr)

    return pm
```

---

### Week 17/18 Logic Clarification

**Epic request says:**
> "Use week_17 folders for projected_points, week_18 folders for actual_points in week 17"

**Investigation findings:**
- JSON arrays already handle this: `projected_points[16]` and `actual_points[16]` contain week 17 data
- Week 18 folder exists for data completeness (VALIDATION_WEEKS = 18)
- Current code loops weeks 1-17 (line 303 comment confirms)
- NO special handling needed - arrays contain all data

**Conclusion:**
- Epic request is asking to VERIFY this works correctly (validation task)
- JSON loading should use week_17 folder's JSON files
- Arrays contain week 17 projected (index 16) and actual (index 16)
- No code changes needed beyond standard JSON integration

---

### DEF/K Evaluation Clarification

**Epic request mentions:** "Verify if DEF and K positions are correctly assessed"

**Investigation findings:**
- DEF and K are two of the 6 position files: `dst_data.json` and `k_data.json`
- Same file loading as other positions
- No special handling in Accuracy Sim code
- PlayerManager loads all 6 positions equally

**Conclusion:**
- Epic request is asking to VERIFY they work correctly (validation task)
- No special code needed - DEF/K handled same as other positions
- Will be tested during Stage 5c (post-implementation QC)

---

### Field Type Handling

**No conversion needed** - Same as Feature 1

**Evidence:**
- FantasyPlayer.from_json() handles boolean `locked` and string `drafted_by` correctly
- See Feature 1 spec.md "Field Type Handling" section

---

### Error Handling

**Same pattern as CSV:**

**Current behavior:**
- `_get_week_data_paths()` returns (None, None) if CSV files don't exist
- Calling code checks for None and skips that week

**JSON behavior:**
- Return None if week_folder doesn't exist
- Let PlayerManager handle missing individual JSON files (it logs warnings)

---

## Implementation Estimate

**Based on codebase investigation:**
- **Files with code changes:** 2 (AccuracySimulationManager.py, ParallelAccuracyRunner.py)
- **Files needing NO changes:** 2 (AccuracyCalculator.py, AccuracyResultsManager.py)
- **New methods needed:** 0 (no parsing - just modify file copying)
- **Modified methods:** 4 methods (2 per file)
- **Lines of code (estimated):** ~40-50 LOC
- **Risk level:** LOW (simpler than Feature 1, no caching logic)

**Simpler than Feature 1 because:**
- No week data caching needed
- No JSON parsing method needed
- Just file copying logic changes
- PlayerManager handles all JSON loading

**No PlayerManager modifications required** - it already handles JSON correctly (proven by Feature 1)

---

## Key Differences from Feature 1

| Aspect | Feature 1 (Win Rate) | Feature 2 (Accuracy) |
|--------|---------------------|---------------------|
| **Data caching** | Pre-loads all 17 weeks | Loads 1 week per evaluation |
| **JSON parsing** | Needs `_parse_players_json()` | No parsing - PlayerManager handles it |
| **Temp directories** | One shared dir per simulation | One temp dir per config evaluation |
| **Complexity** | MEDIUM (caching + parsing) | LOW (file copying only) |
| **LOC estimate** | ~150 LOC | ~40-50 LOC |

---

## Phase 4: Scope Adjustment (COMPLETE)

**Scope Analysis:**
- Total changes: 2 files, 4 methods, ~40-50 LOC
- Estimated todo.md items: ~10-15 items
- Risk level: LOW

**Decision:** Scope is well within bounds. No feature split required.

---

## Phase 5: Cross-Feature Alignment (COMPLETE)

**Alignment with Feature 1:**

**Shared Patterns (reuse):**
- player_data/ subfolder requirement (PlayerManager.py:327)
- Array indexing: index 0 = Week 1, index N-1 = Week N
- Field type handling: rely on FantasyPlayer.from_json()
- Error handling: return None if week folder missing
- Same 6 position files per week

**Intentional Differences (by design):**
- Feature 1: Pre-loads/caches all 17 weeks (Win Rate Sim needs this for performance)
- Feature 2: Loads 1 week per evaluation (Accuracy Sim runs once per week, no caching needed)
- Feature 1: Needs _parse_players_json() to extract week-specific data
- Feature 2: No parsing needed - just file copying (PlayerManager handles loading)

**Why differences are intentional:**
- Win Rate Sim: Runs thousands of iterations → caching essential for performance
- Accuracy Sim: Runs once per config per week → caching adds unnecessary complexity

**Validation Tasks (not code changes):**
- Week 17/18 logic: JSON arrays already handle this (projected_points[16], actual_points[16])
- DEF/K evaluation: Handled same as other positions (dst_data.json, k_data.json)
- Both will be verified during Stage 5c QC testing

**No conflicts or inconsistencies identified.**

---

**Status:** ✅ Stage 2 COMPLETE - Ready for Stage 3 (Cross-Feature Sanity Check)
