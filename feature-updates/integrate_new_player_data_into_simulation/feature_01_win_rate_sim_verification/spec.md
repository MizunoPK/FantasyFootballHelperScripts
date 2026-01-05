# Feature 01: Win Rate Simulation JSON Verification and Cleanup

---

## Epic Intent (User's Original Request)

**⚠️ CRITICAL:** All requirements below MUST trace back to this section.

**Problem This Feature Solves:**

"A recent effort updated the league helper to no longer use players.csv and players_projected.csv to instead use a player_data folder with positional json files - this epic will be about updating the Simulation module to accomidate those changes"
(Source: Epic notes line 1)

"Both the Win Rate sim and Accuracy Sim should maintain the same functionality as before they were broken by the json file introduction, but now it will access data a bit differently"
(Source: Epic notes line 2)

---

**User's Explicit Requests (for Win Rate Sim specifically):**

1. "No longer try to load in players.csv or players_projected.csv"
   (Source: Epic notes line 4)

2. "Correctly load in the json files contained in the week_X folders"
   (Source: Epic notes line 5)

3. "Correctly update the simulations to accomidate the changes to the drafted_by, locked, projected_points, and actual_points fields compared to the original csv data"
   (Source: Epic notes line 6)

4. "I want to verify if Week 17 is being correctly assessed in both sims. When running score_player calculations, it should use the week_17 folders to determine a projected_points of the player, then it should look at the actual_points array in week_18 folders to determine what the player actually scored in week 17."
   (Source: Epic notes line 8)

---

**User's Constraints:**

- "Both the Win Rate sim and Accuracy Sim should maintain the same functionality as before they were broken by the json file introduction"
  (Source: Epic notes line 2 - functionality must remain equivalent)

- "ASSUME ALL PREVIOUS WORK IS INCORRECT OR INCOMPLETE AND VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS. REMOVE ANYTHING UNNECCESIARY, BUGGY, OR WRONG."
  (Source: Epic notes line 10 - must verify, not trust existing implementation)

---

**Out of Scope (User Explicitly Excluded):**

- Changes to league_helper module (already migrated to JSON)
  (Source: Epic notes line 1 - "recent effort updated the league helper" - implies league_helper is done)

- Changing JSON file structure or format
  (Source: Implicit - user says "accommodate" changes, not create new format)

- Accuracy Sim changes
  (Source: Feature 01 is scoped to Win Rate Sim only; Accuracy Sim is Feature 02)

---

**User's End Goal:**

"Both the Win Rate sim and Accuracy Sim should maintain the same functionality as before they were broken by the json file introduction, but now it will access data a bit differently"
(Source: Epic notes line 2)

User wants simulations to work correctly with JSON data, maintaining equivalent functionality to when they used CSV.

---

**Technical Components Mentioned by User:**

- **players.csv / players_projected.csv** (Epic notes line 4) - Must remove references
- **week_X folders** (Epic notes line 5) - JSON files location
- **JSON files** (Epic notes line 5) - New data source
- **drafted_by, locked, projected_points, actual_points fields** (Epic notes line 6) - Changed structure
- **week_17 folders** (Epic notes line 8) - For projected points
- **week_18 folders** (Epic notes line 8) - For week 17 actual points
- **Win Rate sim** (Epic notes line 2, 3) - This feature's target
- **Simulation module** (Epic notes line 1) - Code location

---

**Agent Verification:**

- [x] Re-read epic notes file: 2026-01-02
- [x] Re-read epic ticket: 2026-01-02
- [x] Extracted exact quotes (not paraphrases)
- [x] Cited line numbers for all quotes
- [x] Identified out-of-scope items
- [x] Understand user's goal (verify/fix existing JSON integration, not build from scratch)

---

---

## Components Affected

**Files to Modify:**

1. **SimulatedLeague.py** (`simulation/win_rate/SimulatedLeague.py`)
   - **Source:** Epic Request - User mentioned "Win Rate sim" (epic line 2, 3)
   - **Traceability:** Direct user request to update Win Rate Simulation
   - **Changes:**
     - DELETE `_parse_players_csv()` method (lines 338-361) - Remove deprecated code
     - UPDATE docstring (lines 91-92) - Remove CSV references, document JSON structure
     - VERIFY `_parse_players_json()` correctness (lines 363-440)
     - VERIFY `_preload_all_weeks()` week_N+1 logic (lines 269-336)

2. **SimulationManager.py** (`simulation/win_rate/SimulationManager.py`)
   - **Source:** Epic Request - Documentation references CSV (research finding)
   - **Traceability:** User requested "no longer try to load players.csv" (epic line 4)
   - **Changes:**
     - UPDATE docstring (line 180) - Remove "players.csv in each week folder" reference

3. **SimulatedOpponent.py** (`simulation/win_rate/SimulatedOpponent.py`)
   - **Source:** Epic Request - Documentation references CSV (research finding)
   - **Traceability:** User requested "no longer try to load players.csv" (epic line 4)
   - **Changes:**
     - UPDATE docstring (lines 77-78) - Remove "players_projected.csv" references

4. **DraftHelperTeam.py** (`simulation/win_rate/DraftHelperTeam.py`)
   - **Source:** Epic Request - Documentation references CSV (research finding)
   - **Traceability:** User requested "no longer try to load players.csv" (epic line 4)
   - **Changes:**
     - UPDATE docstring (lines 72-73) - Remove "players_projected.csv" references

**Test Files to Update/Create:**
- `tests/simulation/test_SimulatedLeague.py` - Verify JSON loading tests exist
  - **Source:** Derived requirement (need to verify correctness per user constraint)
  - **Traceability:** User said "ASSUME INCORRECT, VERIFY EVERYTHING" (epic line 10)

**No New Files to Create:**
- JSON data already exists in simulation/sim_data/2025/weeks/week_NN/
- _parse_players_json() method already exists (verification only)

---

## Requirements

### Requirement 1: Remove CSV File Loading

**Description:** Remove all attempts to load players.csv or players_projected.csv

**Source:** Epic Request
**Epic Citation:** Line 4: "No longer try to load in players.csv or players_projected.csv"
**Traceability:** Direct user request

**Implementation:**
- DELETE deprecated `_parse_players_csv()` method (SimulatedLeague.py lines 338-361)
- VERIFY no code calls `_parse_players_csv()` (research confirmed: no calls found)
- Status: Method exists but unused - safe to delete

---

### Requirement 2: Verify JSON Loading Correctness

**Description:** Verify JSON files from week_X folders are loaded correctly

**Source:** Epic Request
**Epic Citation:** Line 5: "Correctly load in the json files contained in the week_X folders"
**Traceability:** Direct user request

**Implementation:**
- VERIFY `_parse_players_json()` method (SimulatedLeague.py lines 363-440)
  - Verify reads 6 position files: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
  - Verify file paths: simulation/sim_data/{year}/weeks/week_{NN}/
  - Verify handles missing files gracefully (logs warning)
- Status: Method exists and appears correct - need verification testing

---

### Requirement 3: Verify Field Structure Handling

**Description:** Verify simulation correctly handles new JSON field structure (arrays vs single values)

**Source:** Epic Request
**Epic Citation:** Line 6: "Correctly update the simulations to accomidate the changes to the drafted_by, locked, projected_points, and actual_points fields compared to the original csv data"
**Traceability:** Direct user request

**Implementation:**
- VERIFY `_parse_players_json()` correctly handles:
  - `drafted_by`: String (no change from CSV) - line 430
  - `locked`: Boolean → String "0"/"1" conversion - line 431
  - `projected_points`: Array → Single value extraction via index [week_num - 1] - lines 413-417
  - `actual_points`: Array → Single value extraction via index [actual_week - 1] - lines 419-423
- Status: Code exists - need correctness verification

**Field Structure Details:**
- CSV format (OLD): Single values per column
- JSON format (NEW): Arrays with 17 values (weeks 1-17)
- Conversion: Extract week-specific value from array using zero-based index

---

### Requirement 4: Verify Week 17 Logic

**Description:** Verify Week 17 uses week_17 folder for projected points and week_18 folder for actual points

**Source:** Epic Request
**Epic Citation:** Line 8: "I want to verify if Week 17 is being correctly assessed in both sims. When running score_player calculations, it should use the week_17 folders to determine a projected_points of the player, then it should look at the actual_points array in week_18 folders to determine what the player actually scored in week 17."
**Traceability:** Direct user request

**Implementation:**
- VERIFY `_preload_all_weeks()` week_N+1 logic (lines 269-336):
  - For week 17: loads week_17 folder for projected data
  - For week 17: loads week_18 folder for actual data
  - Uses `week_num_for_actual` parameter to support this pattern
- VERIFY week_18 folder exists with real data (research confirmed: exists with actual_points[16] filled)
- Status: Code exists - need correctness verification

**Week_N+1 Pattern:**
```python
# For week 17 (example):
projected_folder = weeks_folder / "week_17"  # Projected points for week 17
actual_folder = weeks_folder / "week_18"      # Actual points for week 17
actual_data = self._parse_players_json(actual_folder, week_num=17, week_num_for_actual=18)
```

---

### Requirement 5: Update Documentation

**Description:** Update all docstrings referencing CSV files to reflect JSON-based data loading

**Source:** Epic Request
**Epic Citation:** Line 4: "No longer try to load in players.csv or players_projected.csv"
**Traceability:** Documentation must match implementation (derived from user constraint)

**Implementation:**
- UPDATE SimulationManager.py line 180: Change "players.csv in each week folder" to describe JSON structure
- UPDATE SimulatedLeague.py lines 91-92: Change "players_projected.csv, players_actual.csv" to describe week folders with JSON
- UPDATE SimulatedOpponent.py lines 77-78: Change "PlayerManager using players_projected.csv" to JSON description
- UPDATE DraftHelperTeam.py lines 72-73: Change "PlayerManager using players_projected.csv" to JSON description

---

### Requirement 6: Comprehensive Verification

**Description:** Comprehensively verify existing implementation is correct using code review, manual testing, and automated tests

**Source:** User Answer to Question 1 (checklist.md)
**Epic Citation:** Line 10: "ASSUME ALL PREVIOUS WORK IS INCORRECT OR INCOMPLETE AND VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
**Traceability:** User chose Option D (comprehensive verification) and added requirement to verify array usage

**User's Specific Requirement (2026-01-02):**
"we need to make sure the simulation has correctly adapted to the new ways of storing data, such as by using the new projected_points and actual_points arrays correctly"

**Implementation - Three-Part Verification:**

**Part 1: Code Review (line-by-line analysis)**
- Review `_parse_players_json()` implementation (lines 363-440)
- Review `_preload_week_data()` implementation (lines 296-336)
- Verify array indexing logic: projected_points[week_num - 1], actual_points[actual_week - 1]
- Verify field conversions: locked (boolean → string), arrays → single values
- Document findings in verification report

**Part 2: Manual Testing (runtime verification)**
- Run Win Rate Simulation with JSON data
- Inspect loaded player data for week 1, week 10, week 17
- Verify projected_points arrays correctly extracted
- Verify actual_points arrays correctly extracted
- Verify week 17 uses week_18 folder for actuals
- Confirm no FileNotFoundError for players.csv

**Part 3: Automated Tests (coverage verification)**
- Inspect tests/simulation/test_SimulatedLeague.py to identify coverage gaps
- **Add comprehensive JSON loading tests if missing (per Question 2 answer - Option A):**
  - Test `_parse_players_json()` method with valid JSON data
  - Test correct extraction of week-specific values from arrays
  - Test field conversions (locked boolean → string, arrays → single values)
  - Test handling of all 6 position files (QB, RB, WR, TE, K, DST)
  - Test error handling for missing files
  - Test error handling for malformed JSON
  - Test edge cases (empty arrays, missing fields)
- Verify tests cover week_N+1 logic (add if missing)
- **Add dedicated Week 17 edge case test (per Question 3 answer - Option A):**
  - Test week 17 loads projected_points from week_17 folder
  - Test week 17 loads actual_points from week_18 folder
  - Test array indexing: projected_points[16] from week_17, actual_points[16] from week_18
  - Verify week_num_for_actual=18 parameter used correctly
  - Test with real data structure (17-element arrays)
- Verify tests cover array extraction logic (add if missing)
- **Add edge case behavior tests (per Question 4 answer - Option A):**
  - Test missing JSON file: verify warning logged, simulation continues
  - Test missing week_18 folder: verify fallback to projected data works
  - Test array index out of bounds: verify default 0.0 used, no IndexError
  - Test malformed JSON: verify appropriate error handling
- Ensure 100% test pass rate

**Success Criteria:**
- Code review confirms logic correctness
- Manual testing shows correct data loaded
- Automated tests provide regression protection
- Specifically verified: projected_points and actual_points arrays used correctly

---

**Requirements Summary:**

Total Requirements: 6
- ✅ Requirement 1: Direct epic request (line 4)
- ✅ Requirement 2: Direct epic request (line 5)
- ✅ Requirement 3: Direct epic request (line 6)
- ✅ Requirement 4: Direct epic request (line 8)
- ✅ Requirement 5: Derived from epic request (documentation must match code)
- ✅ Requirement 6: Direct user constraint (line 10)

All requirements traced to sources.

---

## Data Structures

### JSON File Structure (Verified from Research)

**Location:** `simulation/sim_data/{year}/weeks/week_{NN}/`

**Files per week:** 6 position files
- qb_data.json
- rb_data.json
- wr_data.json
- te_data.json
- k_data.json
- dst_data.json

**Source:** Epic Request - "json files contained in the week_X folders" (line 5)

**Format (actual from research):**
```json
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
  "projected_points": [20.8, 20.8, ..., 20.8],  // Array of 17 values
  "actual_points": [0.0, 0.0, ..., 23.2]         // Array of 17 values
}
```

**Field Changes (CSV → JSON):**
- `drafted_by`: String (no change)
- `locked`: Boolean (was string "0"/"1" in CSV)
- `projected_points`: Array of 17 floats (was single float in CSV)
- `actual_points`: Array of 17 floats (was single float in CSV)

---

### Internal Representation

**Converted format (after _parse_players_json):**
```python
players[player_id] = {
    'id': str(player_id),
    'name': str,
    'position': str,
    'drafted_by': str,                    # Direct copy
    'locked': str,                        # Boolean → "0"/"1"
    'projected_points': str,              # Array[week_num-1] → single value
    'actual_points': str                  # Array[actual_week-1] → single value
}
```

**Source:** Research finding - _parse_players_json() implementation (lines 426-434)
**Traceability:** This conversion maintains CSV compatibility while using JSON source

---

## Algorithms

### Algorithm 1: JSON File Loading (_parse_players_json)

**Source:** Epic Request - "Correctly load in the json files" (line 5)

**Current Implementation (lines 363-440):**
```
1. Input: week_folder (Path), week_num (int), week_num_for_actual (Optional[int])
2. For each position file [qb, rb, wr, te, k, dst]:
   a. Check if json_file exists
   b. If missing: log warning, continue
   c. If exists: load JSON array of player dicts
   d. For each player in array:
      - Extract id
      - Extract projected_points array → get value at [week_num - 1]
      - Extract actual_points array → get value at [actual_week - 1]
      - Convert locked boolean → "0" or "1" string
      - Build dict with single values (matches CSV format)
      - Add to players dict keyed by id
3. Return players dict
```

**Verification Needed:**
- Confirm array indexing is correct (week 1 = index 0, week 17 = index 16)
- Confirm week_num_for_actual parameter works correctly
- Confirm handles missing files gracefully

---

### Algorithm 2: Week_N+1 Data Loading (_preload_week_data)

**Source:** Epic Request - "use the week_17 folders...look at...week_18 folders" (line 8)

**Current Implementation (lines 296-336):**
```
1. For each week 1-17:
   a. projected_folder = weeks_folder / f"week_{week_num:02d}"
   b. actual_week_num = week_num + 1
   c. actual_folder = weeks_folder / f"week_{actual_week_num:02d}"

   d. Parse projected data from week_N:
      projected_data = _parse_players_json(projected_folder, week_num)

   e. Parse actual data from week_N+1:
      if actual_folder exists:
          actual_data = _parse_players_json(actual_folder, week_num, week_num_for_actual=actual_week_num)
      else:
          actual_data = projected_data  // Fallback

   f. Cache both: week_data_cache[week_num] = {'projected': ..., 'actual': ...}
2. Return cached data
```

**Verification Needed:**
- Confirm week 17 loads from week_18 for actuals
- Confirm week_18 folder exists (research confirmed: YES)
- Confirm week_18 has real data for week 17 (research confirmed: actual_points[16] = 23.2)
- Confirm fallback only triggers when week_N+1 missing (should not happen for week 17)

---

## Dependencies

**This feature depends on:**

- **Existing JSON data files**
  - Source: Epic Request (user mentioned "json files")
  - Status: VERIFIED - Files exist in simulation/sim_data/2025/weeks/week_01 through week_18
  - Evidence: Research Phase verified structure

- **Existing _parse_players_json() method**
  - Source: Research finding
  - Status: EXISTS - SimulatedLeague.py lines 363-440
  - Action: VERIFY correctness (not implement from scratch)

- **Existing _preload_week_data() method**
  - Source: Research finding
  - Status: EXISTS - SimulatedLeague.py lines 296-336
  - Action: VERIFY correctness (not implement from scratch)

**This feature does NOT depend on:**

- PlayerManager changes (league_helper already migrated - epic line 1)
- JSON file format changes (format is established)
- New data collection (using existing sim_data)

**This feature blocks:**

- Feature 02 (Accuracy Sim) is independent (parallel work)
- Feature 03 (Cross-Simulation Testing) depends on this feature being complete

---

## Edge Cases

### Edge Case 1: Missing JSON File

**Scenario:** One of the 6 position files missing from week folder

**Current Handling:** Log warning, continue (lines 399-401)
```python
if not json_file.exists():
    self.logger.warning(f"Missing {position_file} in {week_folder}")
    continue
```

**Source:** Research finding - already implemented
**Verification Needed:** Confirm this is correct behavior (not error-causing)

---

### Edge Case 2: Missing week_18 Folder

**Scenario:** week_18 folder doesn't exist (can't get week 17 actuals)

**Current Handling:** Fallback to projected data, log warning (lines 312-322)
```python
if actual_folder.exists():
    actual_data = _parse_players_json(...)
else:
    self.logger.warning(...)
    actual_data = projected_data  # Fallback
```

**Source:** Research finding - already implemented
**Verification Needed:** Confirm week_18 exists (research confirmed: YES) so this shouldn't trigger for week 17

---

### Edge Case 3: Array Index Out of Bounds

**Scenario:** projected_points or actual_points array has <17 values

**Current Handling:** Check array length before indexing (lines 414-423)
```python
if len(projected_array) > week_num - 1:
    projected = projected_array[week_num - 1]
else:
    projected = 0.0
```

**Source:** Research finding - already implemented
**Verification Needed:** Confirm this is correct (using 0.0 as default)

---

## Testing Strategy

**Comprehensive verification approach (per user answer to Question 1):**

**Source:** User Answer 2026-01-02 - "we need to make sure the simulation has correctly adapted to the new ways of storing data, such as by using the new projected_points and actual_points arrays correctly"

**Three-Part Verification (aligned with Requirement 6):**

### Part 1: Code Review (line-by-line analysis)
- Review `_parse_players_json()` implementation (lines 363-440)
- Review `_preload_week_data()` implementation (lines 296-336)
- Verify array indexing logic: projected_points[week_num - 1], actual_points[actual_week - 1]
- Verify field conversions: locked (boolean → string), arrays → single values
- **Critical verification:** Ensure projected_points and actual_points arrays are used correctly
- Document findings in verification report

### Part 2: Manual Testing (runtime verification)
- Run Win Rate Simulation with JSON data
- Inspect loaded player data for week 1, week 10, week 17
- Verify projected_points arrays correctly extracted
- Verify actual_points arrays correctly extracted
- Verify week 17 uses week_18 folder for actuals
- Confirm no FileNotFoundError for players.csv

### Part 3: Automated Tests (coverage verification)
- Inspect tests/simulation/test_SimulatedLeague.py to identify coverage gaps
- **Add comprehensive JSON loading tests if missing (per Question 2 answer - Option A):**
  - Test `_parse_players_json()` method with valid JSON data
  - Test correct extraction of week-specific values from arrays
  - Test field conversions (locked boolean → string, arrays → single values)
  - Test handling of all 6 position files (QB, RB, WR, TE, K, DST)
  - Test error handling for missing files
  - Test error handling for malformed JSON
  - Test edge cases (empty arrays, missing fields)
- Verify tests cover week_N+1 logic (add if missing)
- **Add dedicated Week 17 edge case test (per Question 3 answer - Option A):**
  - Test week 17 loads projected_points from week_17 folder
  - Test week 17 loads actual_points from week_18 folder
  - Test array indexing: projected_points[16] from week_17, actual_points[16] from week_18
  - Verify week_num_for_actual=18 parameter used correctly
  - Test with real data structure (17-element arrays)
- Verify tests cover array extraction logic (add if missing)
- **Add edge case behavior tests (per Question 4 answer - Option A):**
  - Test missing JSON file: verify warning logged, simulation continues
  - Test missing week_18 folder: verify fallback to projected data works
  - Test array index out of bounds: verify default 0.0 used, no IndexError
  - Test malformed JSON: verify appropriate error handling
- Ensure 100% test pass rate

**Success Criteria:**
- Code review confirms logic correctness
- Manual testing shows correct data loaded
- Automated tests provide regression protection
- Specifically verified: projected_points and actual_points arrays used correctly

---

## Open Questions

(See checklist.md for details)

---

## Completion Criteria

**This feature is complete when:**

- [ ] Deprecated `_parse_players_csv()` method deleted
- [ ] All 4 CSV references in docstrings updated to JSON
- [ ] `_parse_players_json()` verified correct (code review + tests)
- [ ] Week_N+1 logic verified correct (code review + tests)
- [ ] Week 17 specifically verified (uses week_17 projected, week_18 actual)
- [ ] All tests passing (100% pass rate)
- [ ] No FileNotFoundError for players.csv (grep confirms)
- [ ] Documentation accurate (reflects JSON implementation)
