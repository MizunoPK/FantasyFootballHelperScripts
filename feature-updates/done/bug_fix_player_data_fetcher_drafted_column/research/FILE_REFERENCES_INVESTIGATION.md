# File References Investigation - Feature 02

**Date:** 2025-12-30
**Purpose:** Investigate 14 files referencing players.csv and players_projected.csv

---

## Summary

**Total Files Investigated:** 14 (7 league_helper, 7 simulation)
**Real Dependencies Found:** 1 file needs code changes
**Dead Code / Comments:** 13 files (no changes needed)

---

## League Helper Files (7 total)

### 1. ModifyPlayerDataModeManager.py ✅ NO CHANGES NEEDED
**Lines:** 303, 382
**Type:** Comments/docstrings only
**Finding:** Comments mention "save to players.csv" but actual code uses `player_manager.update_players_file()` which already uses JSON
**Action:** None (comments are just explanatory, actual code uses JSON)

---

### 2. PlayerManager.py ✅ NO CHANGES NEEDED (already deprecated)
**Lines:** 10, 71, 102, 131, 148
**Type:** Comments + deprecated method
**Finding:**
- Lines 10, 71, 102: Comments/docstrings
- Line 131: `self.file_str = str(data_folder / 'players.csv')` - used by deprecated method only
- Lines 146-161: `load_players()` method marked DEPRECATED with warning
**Current Behavior:** Uses `load_players_from_json()` by default (line 139)
**Action:** None (deprecated method already warns users, not called by default)

---

### 3. ReserveAssessmentModeManager.py ✅ NO CHANGES NEEDED (different file)
**Lines:** 72, 227, 238
**Type:** Historical data reference
**Finding:** References `data/last_season/players.csv` (DIFFERENT FILE - historical comparison data, not current season data)
**Action:** None (this is a separate historical file, not the one being deprecated)

---

### 4. ProjectedPointsManager.py ✅ NO CHANGES NEEDED (class deprecated)
**Lines:** 59, 108
**Type:** Deprecated class
**Finding:**
- Entire class marked DEPRECATED in header (line 56: "ORIGINAL DOCUMENTATION (for historical reference)")
- Class consolidated into PlayerManager (per code comments)
- Line 108: `projected_file = self.data_folder / 'players_projected.csv'`
**Action:** None (class already deprecated and not used)

---

### 5. SaveCalculatedPointsManager.py ⚠️ **NEEDS UPDATE**
**Lines:** 11, 131, 132
**Type:** ACTUAL DEPENDENCY - copies files to historical snapshots
**Finding:**
```python
# Line 11 (comment):
# - Input data files (players.csv, configs/, team_data/, etc.)

# Lines 131-132 (actual code):
files_to_copy = [
    "players.csv",
    "players_projected.csv",
    "game_data.csv",
    "drafted_data.csv"
]
```
**Issue:** This code COPIES players.csv and players_projected.csv to historical_data folder
**Impact:** After deletion, this will fail when files don't exist
**Required Change:** Remove "players.csv" and "players_projected.csv" from files_to_copy list
**Action:** ✅ **UPDATE REQUIRED** - Remove from copy list

---

### 6. DraftedDataWriter.py ✅ NO CHANGES NEEDED
**Lines:** 167, 173
**Type:** Comments only
**Finding:** Comments explaining format differences between players.csv and drafted_data.csv for DST names
**Action:** None (just explanatory comments)

---

### 7. LeagueHelperManager.py ✅ NO CHANGES NEEDED
**Lines:** 62, 201
**Type:** Docstring comments
**Finding:** Docstrings listing expected files in data folder
**Action:** None (or optionally update docstring to remove players.csv from list)

---

## Simulation Files (7 total)

### 8. SimulatedOpponent.py ✅ NO CHANGES NEEDED
**Lines:** 77, 78
**Type:** Docstring comments
**Finding:** Comments describing PlayerManager parameters
**Action:** None

---

### 9. SimulationManager.py ✅ NO CHANGES NEEDED (uses historical sim_data)
**Lines:** 180, 210, 211, 228, 229, 231
**Type:** Historical sim_data validation
**Finding:** Validates and loads from `sim_data/{year}/weeks/week_NN/players.csv` (SEPARATE historical snapshot files)
**Example:** `sim_data/2024/weeks/week_01/players.csv` (NOT data/players.csv)
**Action:** None (simulation uses its own historical snapshot files in sim_data/, not live data/players.csv)

---

### 10. DraftHelperTeam.py ✅ NO CHANGES NEEDED
**Lines:** 72, 73
**Type:** Docstring comments
**Finding:** Comments describing PlayerManager parameters
**Action:** None

---

### 11. SimulatedLeague.py ✅ NO CHANGES NEEDED (uses historical sim_data)
**Lines:** 91, 164, 165, 169, 170, 221, 222, 231, 232, 286, 292, 296, 301
**Type:** Historical sim_data loading
**Finding:**
- Line 164: `players_projected_path = weeks_folder / "week_01" / "players_projected.csv"`
- Line 165: `players_actual_path = weeks_folder / "week_01" / "players.csv"`
- Line 169: Fallback to `data_folder / "players_projected.csv"` (legacy structure)
- Lines 231-232: Copies historical files for simulation
- Lines 286-292: Loads weekly historical data
**Important:** ALL paths are within sim_data/ folder structure (historical snapshots), NOT data/players.csv
**Action:** None (simulation has its own historical snapshot files)

---

### 12. ParallelAccuracyRunner.py ✅ NO CHANGES NEEDED (uses historical sim_data)
**Lines:** 202, 203, 217
**Type:** Historical sim_data loading
**Finding:** Loads from `week_folder / "players_projected.csv"` and `week_folder / "players.csv"` (within sim_data historical structure)
**Action:** None (uses historical snapshots)

---

### 13. AccuracySimulationManager.py ✅ NO CHANGES NEEDED (uses historical sim_data)
**Lines:** 313, 314, 332
**Type:** Historical sim_data loading
**Finding:** Same as ParallelAccuracyRunner - uses historical sim_data snapshots
**Action:** None (uses historical snapshots)

---

### 14. simulation/README.md ✅ NO CHANGES NEEDED (or optionally update docs)
**Lines:** 69, 70, 348, 353
**Type:** Documentation
**Finding:** Documentation describing sim_data folder structure and troubleshooting
**Action:** None (or optionally update docs to clarify historical vs live data)

---

## Investigation Summary

### Files Requiring Code Changes: 1

1. **SaveCalculatedPointsManager.py** (league_helper/save_calculated_points_mode/)
   - Remove "players.csv" from files_to_copy list (line 131)
   - Remove "players_projected.csv" from files_to_copy list (line 132)
   - Update comment on line 11 if desired

### Files with Dead Code (No Changes Needed): 2

1. **PlayerManager.py** - Has deprecated `load_players()` method (already warns users)
2. **ProjectedPointsManager.py** - Entire class deprecated

### Files with Comments Only (No Changes Needed): 11

All other files have only comments, docstrings, or reference DIFFERENT historical files (sim_data snapshots, not data/players.csv)

---

## Key Insights

### Simulation System is NOT Affected
- Simulation uses HISTORICAL snapshot files in `sim_data/{year}/weeks/week_NN/players.csv`
- These are SEPARATE from `data/players.csv` (live current data)
- Simulation will continue to work with historical snapshots

### SaveCalculatedPointsManager is the Only Issue
- This mode creates weekly snapshots of data files
- Currently tries to copy players.csv and players_projected.csv
- After deletion, these files won't exist → copy will fail
- **Fix:** Remove from files_to_copy list

---

## Recommended Actions for Feature 2 Implementation

### Required Changes:
1. **SaveCalculatedPointsManager.py** - Remove players.csv and players_projected.csv from files_to_copy list

### Optional Changes:
1. **LeagueHelperManager.py** - Update docstring to remove players.csv from expected files list
2. **simulation/README.md** - Update docs to clarify sim_data historical files vs data/ live files

### No Changes Needed:
- All other 12 files (comments, deprecated code, or historical sim_data references)

---

**Conclusion:** Only 1 file requires code changes (SaveCalculatedPointsManager.py). All other references are comments, deprecated code, or historical simulation data files.
