# Feature 01: Win Rate Simulation - Discovery Findings

**Research Date:** 2026-01-02
**Researcher:** Agent
**Grounded In:** Epic Intent (user's explicit requests)

---

## Epic Intent Summary

**User requested:**
- "No longer try to load in players.csv or players_projected.csv" (Epic notes line 4)
- "Correctly load in the json files contained in the week_X folders" (Epic notes line 5)
- "Correctly update the simulations to accomidate the changes to the drafted_by, locked, projected_points, and actual_points fields" (Epic notes line 6)
- "Verify if Week 17 is being correctly assessed...use the week_17 folders to determine a projected_points...look at the actual_points array in week_18 folders" (Epic notes line 8)
- "ASSUME ALL PREVIOUS WORK IS INCORRECT OR INCOMPLETE AND VERIFY EVERYTHING" (Epic notes line 10)

**Components user mentioned:**
- Win Rate sim
- players.csv / players_projected.csv (to remove)
- week_X folders
- JSON files
- Fields: drafted_by, locked, projected_points, actual_points (arrays)
- week_17 and week_18 folders

**This research focused on user-mentioned components ONLY.**

---

## Components Identified

### Component 1: SimulatedLeague._parse_players_json()

**User mentioned:** "Correctly load in the json files contained in the week_X folders"

**Found in codebase:**
- File: `simulation/win_rate/SimulatedLeague.py`
- Method definition: Line 363
- Method implementation: Lines 363-440

**Method signature (actual from source):**
```python
def _parse_players_json(
    self,
    week_folder: Path,
    week_num: int,
    week_num_for_actual: Optional[int] = None
) -> Dict[int, Dict[str, Any]]:
```

**How it works today:**
- Reads 6 position JSON files from week folder (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)
- Extracts week-specific values from arrays:
  - `projected_points[week_num - 1]` for projected
  - `actual_points[actual_week - 1]` for actual (supports week_N+1 logic)
- Handles field structure changes:
  - `drafted_by`: Directly copied as string (line 430)
  - `locked`: Converted from boolean to "0"/"1" string for compatibility (line 431)
  - `projected_points`: Extracted from array to single value string (line 432)
  - `actual_points`: Extracted from array to single value string (line 433)
- Returns dict keyed by player ID with single-value fields (matching CSV format)

**Relevance to this feature:**
- ✅ Already implements JSON loading (user requested)
- ✅ Already handles field structure changes (user requested)
- ✅ Already has week_num_for_actual parameter for week_N+1 logic (user requested)
- ⚠️ Need to VERIFY correctness (user: "assume incorrect")

---

### Component 2: Week_N+1 Logic Implementation

**User mentioned:** "use the week_17 folders to determine a projected_points...look at the actual_points array in week_18 folders"

**Found implementation:**
- File: `simulation/win_rate/SimulatedLeague.py`
- Method: `_preload_week_data()`
- Lines: 296-336

**Code structure (actual):**
```python
for week_num in range(1, 18):
    # Week N folder for projections
    projected_folder = weeks_folder / f"week_{week_num:02d}"

    # Week N+1 folder for actuals
    actual_week_num = week_num + 1
    actual_folder = weeks_folder / f"week_{actual_week_num:02d}"

    # Parse projected data from week_N
    projected_data = self._parse_players_json(projected_folder, week_num)

    # Parse actual data from week_N+1 (if exists)
    if actual_folder.exists():
        actual_data = self._parse_players_json(actual_folder, week_num, week_num_for_actual=actual_week_num)
    else:
        # Week 17 limitation: no week_18 exists for actual data
        self.logger.warning(...)
        actual_data = projected_data  # Fallback
```

**Pattern observed:**
- For week 17: tries to load week_18 folder for actuals
- week_18 folder DOES EXIST (verified: simulation/sim_data/2025/weeks/week_18/)
- week_18 has actual_points[16] filled with real data (e.g., 23.2, not 0.0)
- Fallback only triggers if week_18 missing (should not happen with current data)

**Verification Result:**
- ✅ Week_N+1 logic is implemented
- ✅ week_18 folder exists
- ✅ week_18 has actual week 17 data
- ⚠️ Need to verify logic is CORRECT (user: "assume incorrect")
- ⚠️ Fallback message says "Week 17 limitation: no week_18" but week_18 DOES exist - misleading comment?

---

### Component 3: Deprecated _parse_players_csv()

**User mentioned:** "No longer try to load in players.csv or players_projected.csv"

**Found deprecated method:**
- File: `simulation/win_rate/SimulatedLeague.py`
- Method definition: Line 338
- Lines: 338-361
- Status: **DEPRECATED** (docstring line 342)

**Current usage:**
- Searched for calls: `grep -r "_parse_players_csv\(" simulation/win_rate`
- Result: **NO CALLS FOUND** (only the definition exists)
- Method is defined but never invoked

**Conclusion:**
- ✅ CSV method not being called
- ❌ CSV method still exists in codebase (should be removed per user request)

---

### Component 4: CSV References in Documentation

**User mentioned:** "No longer try to load in players.csv or players_projected.csv"

**Found CSV references in docstrings:**

1. **SimulationManager.py:180**
   - Docstring mentions "players.csv in each week folder"
   - Context: Describing data folder structure
   - Status: **OUTDATED** (should reference JSON files)

2. **SimulatedLeague.py:91-92**
   - Docstring mentions "players_projected.csv, players_actual.csv"
   - Context: __init__ method data_folder parameter description
   - Status: **OUTDATED** (should reference week folders with JSON)

3. **SimulatedOpponent.py:77-78**
   - Docstring mentions "PlayerManager using players_projected.csv"
   - Context: Constructor parameter documentation
   - Status: **OUTDATED** (should reference JSON data)

4. **DraftHelperTeam.py:72-73**
   - Docstring mentions "PlayerManager using players_projected.csv"
   - Context: Constructor parameter documentation
   - Status: **OUTDATED** (should reference JSON data)

---

### Data Source: JSON Files in week_X Folders

**User mentioned:** "json files contained in the week_X folders"

**Found in codebase:**
- Location: `simulation/sim_data/2025/weeks/week_NN/`
- Files per week: 6 position files (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)
- Week range: week_01 through week_18 (18 folders total)

**Data format verified (qb_data.json example):**
```json
{
  "id": "3918298",
  "name": "Josh Allen",
  "team": "BUF",
  "position": "QB",
  "bye_week": 7,
  "injury_status": "QUESTIONABLE",
  "drafted_by": "",           // STRING (empty initially)
  "locked": false,            // BOOLEAN
  "average_draft_position": 20.2,
  "player_rating": 100.0,
  "projected_points": [       // ARRAY of 17 values (weeks 1-17)
    20.8, 20.8, 20.8, ...
  ],
  "actual_points": [          // ARRAY of 17 values (weeks 1-17)
    0.0, 0.0, 0.0, ...        // Zeros in week_01 (no games played yet)
  ]
}
```

**week_18 verified (has actual week 17 data):**
```json
"actual_points": [
  38.8, 11.8, 23.0, 24.9, 19.4, 15.4, 0.0,  // Weeks 1-7
  23.2, 28.8, 19.3, 42.7, 8.1, 16.7,        // Weeks 8-13
  37.8, 24.5, 6.9,                          // Weeks 14-16
  23.2                                       // Week 17 (index 16) - REAL DATA
]
```

**Field structure changes (CSV → JSON):**
- **CSV format (OLD):** Single columns - `drafted_by`, `locked`, `projected_points`, `actual_points`
- **JSON format (NEW):**
  - `drafted_by`: Still string (no change)
  - `locked`: Now boolean (was string "0"/"1")
  - `projected_points`: Now array of 17 values (was single value)
  - `actual_points`: Now array of 17 values (was single value)

---

## Existing Test Patterns

**Searched for tests:**
- `tests/simulation/test_SimulatedLeague.py` - Tests for SimulatedLeague class
- `tests/simulation/test_simulation_manager.py` - Tests for SimulationManager

**Test coverage to verify:**
- Need to check if tests cover JSON loading
- Need to check if tests cover week_N+1 logic
- Need to check if tests verify week 17 specifically

(Will research test files in more detail if needed for spec)

---

## Research Completeness

**Components researched:**
- ✅ SimulatedLeague._parse_players_json() (READ source code lines 363-440)
- ✅ Week_N+1 logic implementation (READ source code lines 296-336)
- ✅ Deprecated _parse_players_csv() (READ source code lines 338-361, verified not called)
- ✅ CSV references in docstrings (grep search, found 4 locations)
- ✅ JSON file structure (READ actual files: week_01/qb_data.json, week_18/qb_data.json)
- ✅ Data folder structure (verified weeks 1-18 exist)

**Evidence collected:**
- File paths: simulation/win_rate/SimulatedLeague.py, SimulationManager.py, SimulatedOpponent.py, DraftHelperTeam.py
- Line numbers: Cited for all code references
- Actual code snippets: Method signatures, key logic copied above
- Actual data files: JSON structure verified from source files

**Ready for Phase 1.5 audit.**

---

## Key Findings Summary

### ✅ Already Implemented (Verify Correctness)
1. JSON loading via `_parse_players_json()` method
2. Week_N+1 logic for loading week 17 actuals from week 18
3. Field structure handling (arrays → single values, boolean → string conversion)
4. week_18 folder exists with real week 17 actual data

### ❌ Needs Cleanup (User Requested)
1. Remove deprecated `_parse_players_csv()` method (lines 338-361)
2. Update 4 docstrings referencing CSV files:
   - SimulationManager.py:180
   - SimulatedLeague.py:91-92
   - SimulatedOpponent.py:77-78
   - DraftHelperTeam.py:72-73

### ⚠️ Needs Verification (User: "Assume Incorrect")
1. Verify `_parse_players_json()` correctness:
   - Array indexing logic (week_num - 1)
   - Field extraction logic
   - Boolean to string conversion
2. Verify week_N+1 logic correctness:
   - Loads week_17 for projected points ✓
   - Loads week_18 for actual points ✓
   - Handles week 17 edge case properly
3. Verify existing tests cover JSON loading
4. Verify no hidden CSV dependencies

---

**Next Steps:**
- Phase 1.5: Research Completeness Audit
- STAGE_2b: Update spec.md with detailed requirements based on findings
