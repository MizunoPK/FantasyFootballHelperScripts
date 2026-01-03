# Feature 01: Win Rate Simulation JSON Integration - Discovery Findings

**Research Date:** 2026-01-01
**Researcher:** Agent (Stage 2 Deep Dive)

---

## Current CSV-Based Implementation

### Data Loading Flow

1. **SimulatedLeague._create_shared_data_dir()** (line 211-236)
   - Creates shared directories to reduce file I/O
   - Copies `players.csv` and `players_projected.csv` from week folders to shared directories
   - Current paths:
     - Historical: `data_folder/weeks/week_01/players.csv` and `players_projected.csv`
     - Legacy: `data_folder/players.csv` and `players_projected.csv`

2. **PlayerManager instantiation** (lines 195-196)
   - `projected_pm = PlayerManager(shared_projected_dir, ...)`
   - `actual_pm = PlayerManager(shared_actual_dir, ...)`
   - PlayerManager loads data from CSV files in its __init__

3. **Week Data Caching** (_preload_week_data, line 269-294)
   - Pre-loads all 17 weeks of player data into `week_data_cache` dictionary
   - Calls `_parse_players_csv()` for each week
   - Format: `week_data_cache[week_num] = Dict[player_id, Dict[field, value]]`

4. **Week Data Loading** (_load_week_data, line 318-344)
   - Called at start of each simulated week
   - Updates PlayerManager instances with week-specific data via `set_player_data()`
   - Uses pre-loaded cache (no disk I/O during simulation)

### Current CSV Structure

**players.csv format (actual points):**
- Columns: id, name, team, position, bye_week, injury_status, drafted_by, locked, projected_points, actual_points, ...
- drafted_by: Integer or empty string (represents team number)
- locked: "0" or "1" (string representation of boolean)
- projected_points: Single float value
- actual_points: Single float value

**players_projected.csv format (projected points):**
- Same structure as players.csv
- Contains projected stats instead of actual

---

## New JSON Structure

**6 position-specific JSON files per week:**
- `qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`

**JSON structure per file:**
```json
{
  "qb_data": [
    {
      "id": "3918298",
      "name": "Josh Allen",
      "team": "BUF",
      "position": "QB",
      "bye_week": 7,
      "injury_status": "QUESTIONABLE",
      "drafted_by": "",
      "locked": false,
      "average_draft_position": 20.2,
      "player_rating": 100.0,
      "projected_points": [20.8, 20.8, ...],  // Array of 18 values (one per week)
      "actual_points": [0, 0, ...]             // Array of 18 values
    }
  ]
}
```

**Field changes:**
- `drafted_by`: String (empty string instead of empty value)
- `locked`: Boolean (true/false instead of "0"/"1")
- `projected_points`: Array of 18 floats (one per week)
- `actual_points`: Array of 18 floats (one per week)

---

## Components to Modify

### 1. SimulationManager.py

**Method:** `_validate_season_structure(folder)` (lines 166-211)
- **Current:** Validates `players.csv` exists in each week folder
- **Change needed:** Validate 6 JSON files exist instead
- **Lines affected:** 210-211

**Method:** `_validate_season_data(season_folder)` (lines 213-252)
- **Current:** Checks `players_projected.csv` or `players.csv` in week_01
- **Change needed:** Check for JSON files instead
- **Lines affected:** 228-231

### 2. SimulatedLeague.py

**Method:** `__init__()` - Data path determination (lines 159-170)
- **Current:** Determines `players_projected.csv` and `players.csv` paths
- **Change needed:** Determine path to week folder containing JSON files
- **Lines affected:** 164-170

**Method:** `_create_shared_data_dir()` (lines 211-236)
- **Current:** Copies 2 CSV files to shared directory
- **Change needed:** Copy 6 JSON files to shared directory
- **Signature change:** May need to accept week folder path instead of individual CSV paths
- **Lines affected:** 231-232

**Method:** `_preload_week_data()` (lines 269-294)
- **Current:** Calls `_parse_players_csv()` for each week
- **Change needed:** Call new `_parse_players_json()` method instead
- **Lines affected:** 286, 289

**New method needed:** `_parse_players_json(week_folder_path)`
- **Purpose:** Load 6 JSON files and merge into single player dictionary
- **Returns:** Dict[player_id, Dict[field, value]]
- **Logic:**
  1. Load all 6 position JSON files
  2. Extract arrays from each (e.g., qb_data.json → qb_data array)
  3. Merge all players into single dict keyed by player ID
  4. Convert projected_points/actual_points arrays to week-specific values

**Method:** `_load_week_data()` (lines 318-344)
- **Current:** Passes pre-loaded week data to PlayerManager
- **Change needed:** Ensure week-specific data extraction from arrays works correctly
- **Potential issue:** Need to verify PlayerManager.set_player_data() can handle new field structure

### 3. DraftHelperTeam.py

**No direct changes needed:**
- Uses PlayerManager which will handle JSON loading internally
- As long as PlayerManager interface stays the same, DraftHelperTeam should work unchanged

**Verification needed:**
- Confirm PlayerManager.load_players_from_json() already exists (saw this in league_helper earlier)
- Verify it handles JSON correctly for simulation use case

### 4. SimulatedOpponent.py

**No direct changes needed:**
- Uses PlayerManager like DraftHelperTeam
- Should work unchanged as long as PlayerManager interface is stable

**Verification needed:**
- Same as DraftHelperTeam - confirm PlayerManager compatibility

---

## Key Questions for Checklist

1. **PlayerManager compatibility:**
   - Does PlayerManager.load_players_from_json() work correctly with simulation data folder structure?
   - Does set_player_data() handle the new field types (boolean locked, string drafted_by)?
   - How should we pass week-specific projected_points/actual_points values to PlayerManager?

2. **Week-specific data extraction:**
   - projected_points and actual_points are now arrays - which index represents which week?
   - Do we extract week-specific values during _parse_players_json() or during _load_week_data()?
   - Should we convert arrays to single values before passing to PlayerManager?

3. **Shared directory structure:**
   - Should we copy all 6 JSON files to shared directories for each week?
   - Or should we copy once and extract week-specific data dynamically?
   - Performance implications?

4. **Error handling:**
   - What if JSON files are missing for a week?
   - What if a player exists in some position files but not others?
   - What if projected_points/actual_points arrays don't have 18 elements?

---

## Existing Patterns to Leverage

### PlayerManager JSON Loading (league_helper/util/PlayerManager.py)

**Method:** `load_players_from_json()` (lines 304-422)
- Already implemented for league helper module
- Loads 6 position files from `data_folder/player_data/`
- Handles field name mapping
- Can potentially reuse this logic

**Key difference:**
- League helper uses: `data/player_data/{position}_data.json`
- Simulation uses: `simulation/sim_data/YYYY/weeks/week_NN/{position}_data.json`

### Similar Week Data Loading

**Accuracy Sim** also needs JSON integration (Feature 2)
- Likely shares similar patterns
- Should coordinate approaches for consistency

---

## Next Steps

1. Create checklist.md with open questions
2. Update spec.md with technical details once questions resolved
3. Verify PlayerManager compatibility with simulation requirements
4. Design week-specific data extraction approach

---

**Files to Modify Summary:**
- `simulation/win_rate/SimulationManager.py` - Validation logic (2 methods)
- `simulation/win_rate/SimulatedLeague.py` - Data loading logic (3 methods + 1 new method)
- `simulation/win_rate/DraftHelperTeam.py` - Likely no changes (uses PlayerManager)
- `simulation/win_rate/SimulatedOpponent.py` - Likely no changes (uses PlayerManager)

**Total:** 2 files with significant changes, 2 files needing verification only
