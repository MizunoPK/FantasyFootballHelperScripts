# Feature 02: Accuracy Simulation JSON Integration - Discovery Findings

**Research Date:** 2026-01-01
**Researcher:** Agent (Stage 2 Deep Dive)

---

## Current CSV-Based Implementation

### Data Loading Flow

**Two main files involved:**

1. **AccuracySimulationManager.py** - Main orchestration
2. **ParallelAccuracyRunner.py** - Parallel config evaluation

**Current flow:**
1. `_get_week_data_paths(season_path, week_num)` - Returns paths to CSV files
   - Lines 313-314: `projected_path = week_folder / "players_projected.csv"`, `actual_path = week_folder / "players.csv"`
2. `_create_player_manager(config_dict, week_data_path, season_path)` - Creates temp directory and copies CSV files
   - Lines 343-346: Copies all `.csv` files from week folder to temp dir
   - Lines 348-361: Copies season-level CSV files (season_schedule.csv, game_data.csv, team_data/)
3. PlayerManager instantiated with temp directory
4. Accuracy calculated by comparing projected vs actual points

---

## Key Differences from Win Rate Sim

**Win Rate Sim:**
- Pre-loads ALL 17 weeks of data into cache
- Uses `_parse_players_csv()` to parse CSV into dict
- Updates PlayerManager with week-specific data during simulation via `set_player_data()`

**Accuracy Sim:**
- Loads ONE week at a time (per config evaluation)
- Does NOT pre-load or cache week data
- Creates fresh temp directory for EACH config evaluation
- Copies files on-demand per evaluation

**Implementation approach will differ:**
- Win Rate Sim: Need `_parse_players_json()` to parse and cache
- Accuracy Sim: Need to copy JSON files instead of CSV files (simpler)

---

## Files to Modify

### 1. AccuracySimulationManager.py

**Method:** `_get_week_data_paths(season_path, week_num)` (lines 298-319)
- **Current:** Returns `(projected_path, actual_path)` to CSV files
- **Change needed:** Return week_folder path instead (JSON files are in the folder, not individual files)
- **OR:** Keep returning paths but change to JSON validation

**Method:** `_create_player_manager(config_dict, week_data_path, season_path)` (lines 327-380)
- **Current:** Copies all `.csv` files from week folder (lines 343-346)
- **Change needed:** Copy 6 JSON files OR create `player_data/` subfolder with JSON files
- **Lines affected:** 343-346

### 2. ParallelAccuracyRunner.py

**Method:** `_get_week_data_paths_worker(season_path, week_num)` (lines 192-208)
- **Current:** Returns `(projected_path, actual_path)` to CSV files
- **Change needed:** Same as AccuracySimulationManager - return week_folder or JSON paths

**Method:** `_create_player_manager_worker(config_dict, week_data_path, season_path)` (lines 212-271)
- **Current:** Copies all `.csv` files from week folder (lines 224-226)
- **Change needed:** Copy 6 JSON files OR create `player_data/` subfolder with JSON files
- **Lines affected:** 224-226

---

## PlayerManager Compatibility

**Same as Win Rate Sim:**
- PlayerManager expects `data_folder/player_data/{position}_data.json` structure (PlayerManager.py:327)
- Must create `player_data/` subfolder in temp directory
- Copy 6 JSON files to that subfolder

**Temp directory structure:**
```
temp_dir/
├── player_data/           # NEW - required by PlayerManager
│   ├── qb_data.json      # Copied from week folder
│   ├── rb_data.json
│   ├── wr_data.json
│   ├── te_data.json
│   ├── k_data.json
│   └── dst_data.json
├── league_config.json     # Created from config_dict
├── season_schedule.csv    # Copied from season folder
├── game_data.csv          # Copied from season folder
└── team_data/            # Copied from season folder
```

---

## Week 17/18 Logic Investigation

**Epic request says:**
> "When running score_player calculations, it should use the week_17 folders to determine a projected_points of the player, then it should look at the actual_points array in week_18 folders to determine what the player actually scored in week 17"

**Current implementation:**
- AccuracySimulationManager loops through weeks 1-17 (lines 302-303 comment: "Week number (1-17)")
- For each week, loads `week_{N:02d}/players.csv` and `players_projected.csv`
- No special handling for week 17 vs week 18

**JSON structure:**
- Week 17 folder: `week_17/` with JSON files containing projected_points array
- Week 18 folder: `week_18/` with JSON files containing actual_points array

**Question to investigate:**
- Does current CSV structure already use week_18 for week 17 actuals?
- Or is this a new requirement for JSON?

**From compile_historical_data.py investigation:**
- Week folders go up to week_18 (VALIDATION_WEEKS = 18, constants.py:91)
- Week 18 exists for capturing final week 17 stats
- JSON arrays: projected_points[16] = week 17 projected, actual_points[16] = week 17 actual

**Conclusion:**
- Epic request may be CHECKING if this is correct (validation task)
- JSON loading should use: week_17 folder for projected, same folder for actual (arrays handle this)
- No special week_18 logic needed - arrays contain all weeks

---

## Data Structure Changes

**Same as Win Rate Sim:**
- CSV → JSON (6 position files)
- drafted_by: int/empty → string
- locked: "0"/"1" → boolean
- projected_points: single value → array[17]
- actual_points: single value → array[17]

**Array indexing:**
- Same as Win Rate Sim: index 0 = Week 1, index 16 = Week 17

---

## Error Handling

**Current CSV approach:**
- `_get_week_data_paths()`: Returns (None, None) if files don't exist (lines 310-311, 316-317)
- Calling code checks for None and skips that week

**JSON approach:**
- Same pattern: Return None if any of 6 JSON files missing
- Or return week_folder and let file copy handle missing files gracefully

---

## Evaluation Scope

**Accuracy Sim evaluates 4 week ranges:**
- Week 1-5
- Week 6-9
- Week 10-13
- Week 14-17

**Per evaluation:**
- Loops through specified weeks in range
- Loads data for each week
- Calculates MAE across all weeks in range

**JSON impact:**
- Each week still loaded independently
- Same range evaluation logic
- Just different file format

---

## Components NOT Affected

**AccuracyCalculator.py** - NO CHANGES
- Receives player_data list (dicts with 'projected' and 'actual' keys)
- Doesn't care about file format
- PlayerManager provides the data in expected format

**AccuracyResultsManager.py** - NO CHANGES
- Tracks results and generates optimal configs
- Doesn't interact with data files
- Only processes AccuracyResult objects

---

## Key Implementation Differences from Feature 1

| Aspect | Feature 1 (Win Rate) | Feature 2 (Accuracy) |
|--------|---------------------|---------------------|
| **Data caching** | Pre-loads all 17 weeks | Loads 1 week per evaluation |
| **Parsing method** | Needs `_parse_players_json()` | No parsing - just copy files |
| **Temp directories** | One shared dir per sim | One temp dir per config |
| **Complexity** | Higher (caching logic) | Lower (file copying) |

---

## Estimated Changes

**Files to modify:** 2 (AccuracySimulationManager.py, ParallelAccuracyRunner.py)
**Methods to modify:** 4 methods (2 per file)
**New methods:** 0 (no parsing needed - just file copying)
**Lines of code:** ~40-50 LOC

**Lower complexity than Feature 1** because:
- No week data caching
- No JSON parsing needed
- Just file copying logic

---

## Open Questions

1. ~~Week 17/18 folder usage~~ - RESOLVED: JSON arrays handle this, use week_17 folder
2. ~~PlayerManager compatibility~~ - RESOLVED: Same as Feature 1 (needs player_data/ subfolder)
3. ~~Field type handling~~ - RESOLVED: Same as Feature 1 (FantasyPlayer handles it)
4. ~~Error handling for missing files~~ - Same pattern as CSV (return None, skip week)

**All questions likely answerable through Feature 1's findings**

---

**Next:** Update spec.md with confirmed details, leverage Feature 1's investigation results
