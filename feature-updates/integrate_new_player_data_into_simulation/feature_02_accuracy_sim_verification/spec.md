# Feature 02: Accuracy Simulation JSON Verification and Cleanup

---

## Epic Intent (User's Original Request)

**⚠️ CRITICAL:** All requirements below MUST trace back to this section.

**Problem This Feature Solves:**

"A recent effort updated the league helper to no longer use players.csv and players_projected.csv to instead use a player_data folder with positional json files - this epic will be about updating the Simulation module to accomidate those changes"
(Source: Epic notes line 1)

"Both the Win Rate sim and Accuracy Sim should maintain the same functionality as before they were broken by the json file introduction, but now it will access data a bit differently"
(Source: Epic notes line 2)

---

**User's Explicit Requests (for Accuracy Sim specifically):**

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

- Win Rate Sim changes
  (Source: Feature 02 is scoped to Accuracy Sim only; Win Rate Sim is Feature 01)

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
- **Accuracy Sim** (Epic notes line 2, 3) - This feature's target
- **Simulation module** (Epic notes line 1) - Code location

---

**Agent Verification:**

- [x] Re-read epic notes file: 2026-01-03
- [x] Re-read epic ticket: (will read if needed)
- [x] Extracted exact quotes (not paraphrases)
- [x] Cited line numbers for all quotes
- [x] Identified out-of-scope items
- [x] Understand user's goal (verify/fix existing JSON integration, not build from scratch)

---

---

## Components Affected

**Files to Verify/Modify:**

1. **AccuracySimulationManager.py** (`simulation/accuracy/AccuracySimulationManager.py`)
   - **Source:** Epic Request - User mentioned "Accuracy Sim" (epic line 2, 3)
   - **Traceability:** Direct user request to update Accuracy Simulation
   - **Changes:**
     - VERIFY `_create_player_manager()` JSON file copying (lines 339-404)
     - VERIFY `_load_season_data()` week_N+1 logic (lines 293-337)
     - VERIFY `_evaluate_config_weekly()` two-manager pattern (lines 412-533)
     - UPDATE docstrings if CSV references found (research: none found)

2. **ParallelAccuracyRunner.py** (`simulation/accuracy/ParallelAccuracyRunner.py`)
   - **Source:** Research finding - Contains duplicated `_create_player_manager_for_worker()` method
   - **Traceability:** Same JSON loading logic as AccuracySimulationManager
   - **Changes:**
     - VERIFY worker process JSON file copying is correct
     - UPDATE docstrings if needed

**Test Files to Update/Create:**
- `tests/integration/test_accuracy_simulation_integration.py` - Verify JSON loading tests exist
  - **Source:** Derived requirement (need to verify correctness per user constraint)
  - **Traceability:** User said "ASSUME INCORRECT, VERIFY EVERYTHING" (epic line 10)

**No New Files to Create:**
- JSON data already exists in simulation/sim_data/2025/weeks/week_NN/
- PlayerManager already handles JSON loading (league_helper already migrated)

---

## Requirements

### Requirement 1: Verify PlayerManager JSON Loading in Simulation Context

**Description:** Verify PlayerManager correctly loads JSON files when used by Accuracy Sim through temporary directory pattern

**Source:** Epic Request
**Epic Citation:** Line 5: "Correctly load in the json files contained in the week_X folders"
**Traceability:** Direct user request

**Implementation:**
- VERIFY `_create_player_manager()` method (lines 339-404):
  - Creates temp directory with player_data/ subfolder (lines 359-363)
  - Copies 6 JSON files from week folder to player_data/ (lines 365-373)
    - qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
  - PlayerManager loads from player_data/ directory
- VERIFY no FileNotFoundError when PlayerManager loads JSON
- VERIFY PlayerManager.players array is populated correctly
- Status: Code exists - need verification testing

**Key Difference from Win Rate Sim:**
- Accuracy Sim uses **PlayerManager delegation** (not direct parsing)
- PlayerManager.load_players_from_json() handles JSON parsing
- Accuracy Sim only needs to copy files to correct location

---

### Requirement 2: Verify Week_N+1 Logic Correctness

**Description:** Verify Accuracy Sim correctly loads week_N folder for projected data and week_N+1 folder for actual data

**Source:** Epic Request
**Epic Citation:** Line 8: "use the week_17 folders to determine a projected_points...look at the actual_points array in week_18 folders"
**Traceability:** Direct user request

**Implementation:**
- VERIFY `_load_season_data()` method (lines 293-337):
  - For week N: returns (week_N folder, week_N+1 folder)
  - projected_folder = season_path / "weeks" / f"week_{week_num:02d}"
  - actual_folder = season_path / "weeks" / f"week_{actual_week_num:02d}" where actual_week_num = week_num + 1
  - Both folders must exist (returns None, None if either missing)
- VERIFY `_evaluate_config_weekly()` uses both folders correctly (lines 436-445):
  - Creates projected_mgr from projected_folder (week_N)
  - Creates actual_mgr from actual_folder (week_N+1)
- Status: Code exists - need correctness verification

---

### Requirement 3: Verify Week 17 Logic Specifically

**Description:** Verify Week 17 uses week_17 folder for projected points and week_18 folder for actual points

**Source:** Epic Request
**Epic Citation:** Line 8: "I want to verify if Week 17 is being correctly assessed...use the week_17 folders...look at the actual_points array in week_18 folders"
**Traceability:** Direct user request

**Implementation:**
- VERIFY week_N+1 logic applies to week 17:
  - week_num = 17 → projected_folder = week_17, actual_folder = week_18
  - Lines 318-323: actual_week_num = 17 + 1 = 18
- VERIFY week_18 folder exists with real data (research confirmed: exists)
- VERIFY two-manager pattern works for week 17:
  - projected_mgr from week_17 → score_player() calculations
  - actual_mgr from week_18 → extract actual_points[16] (line 486)
- Status: Code exists - need week 17 specific verification

**Week 17 Pattern:**
```python
# For week 17:
projected_folder = weeks_folder / "week_17"  # Projected points for week 17
actual_folder = weeks_folder / "week_18"      # Actual points for week 17
actual_data = player.actual_points[17 - 1]    # Extract from index 16
```

---

### Requirement 4: Verify Two-Manager Pattern Correctness

**Description:** Verify Accuracy Sim correctly creates two PlayerManagers per week and extracts correct data from each

**Source:** Epic Request + Research Finding
**Epic Citation:** Line 8: "This means we'll likely need two Player Managers - one for the N week and one for the N+1 week"
**Traceability:** User anticipated this pattern; research confirmed it exists

**Implementation:**
- VERIFY `_evaluate_config_weekly()` two-manager pattern (lines 441-505):
  - **projected_mgr** (from week_N folder):
    - Used for score_player() calculations
    - Returns projected_points (scored values)
  - **actual_mgr** (from week_N+1 folder):
    - Used for extracting actual_points array
    - Line 486: `actual = player.actual_points[week_num - 1]`
    - Array index: week 1 = index 0, week 17 = index 16
  - Matches projections to actuals by player.id
  - Cleanup both managers after use
- Status: Code exists - need correctness verification

---

### Requirement 5: Verify Array Extraction Correctness

**Description:** Verify Accuracy Sim correctly extracts week-specific values from projected_points and actual_points arrays

**Source:** Epic Request
**Epic Citation:** Line 6: "Correctly update the simulations to accomidate the changes to the drafted_by, locked, projected_points, and actual_points fields"
**Traceability:** Direct user request to handle array structure

**Implementation:**
- VERIFY array indexing (line 486):
  - `actual = player.actual_points[week_num - 1]`
  - Week 1 = index 0, Week 17 = index 16
  - Checks array length before indexing: `len(player.actual_points) >= week_num`
- VERIFY projected points come from score_player() (not direct array access):
  - Lines 458-478: projected_mgr.score_player() returns scored player
  - Uses scored.projected_points (calculated value, not raw array)
- VERIFY null/missing value handling:
  - Line 487: Checks `actual is not None and actual > 0`
  - Only includes valid actual points in MAE calculation
- Status: Code exists - need correctness verification

---

### Requirement 6: Comprehensive Verification

**Description:** Comprehensively verify existing implementation is correct using code review, manual testing, and automated tests

**Source:** User Constraint
**Epic Citation:** Line 10: "ASSUME ALL PREVIOUS WORK IS INCORRECT OR INCOMPLETE AND VERIFY EVERYTHING FOR CORRECTNESS AND COMPLETENESS"
**Traceability:** Direct user constraint (verify, don't trust)

**Implementation - Three-Part Verification:**

**Part 1: Code Review (line-by-line analysis)**
- Review `_create_player_manager()` implementation (lines 339-404)
- Review `_load_season_data()` implementation (lines 293-337)
- Review `_evaluate_config_weekly()` implementation (lines 412-533)
- Verify JSON file copying logic
- Verify PlayerManager integration
- Verify array extraction logic
- Document findings in verification report

**Part 2: Manual Testing (runtime verification)**
- Run Accuracy Simulation with JSON data
- Inspect loaded player data for week 1, week 10, week 17
- Verify PlayerManager loads JSON correctly
- Verify week_N+1 logic works (projected from N, actual from N+1)
- Verify week 17 uses week_18 for actuals
- Confirm no FileNotFoundError for players.csv

**Part 3: Automated Tests (coverage verification)**
- Inspect tests/integration/test_accuracy_simulation_integration.py to identify coverage gaps
- **Add comprehensive tests if missing (per Question 1 answer - Option D):**
  - Test `_create_player_manager()` creates temp directory correctly
  - Test JSON files copied to temp/player_data/ location
  - Test PlayerManager loads JSON from temporary directory
  - Test handling of all 6 position files (QB, RB, WR, TE, K, DST)
  - Test error handling for missing files
  - Test PlayerManager integration in simulation context
- Verify tests cover week_N+1 logic (add if missing)
- **Add dedicated Week 17 edge case test (per Question 3 answer - Option A):**
  - Test `_load_season_data(season_path, week_num=17)` returns (week_17, week_18)
  - Test `_evaluate_config_weekly()` for week 17 creates two managers correctly
  - Test projected_mgr from week_17 folder, actual_mgr from week_18 folder
  - Test array extraction: actual_points[16] from week_18 data
  - Test week_18 folder exists with real week 17 data
  - Test with real data structure (17-element arrays)
- Verify tests cover two-manager pattern (add if missing)
- Verify tests cover edge cases (add if missing - per Question 4 answer)
- Ensure 100% test pass rate

**Updated based on Feature 01 implementation (2026-01-03):**
- ✅ Array indexing pattern verified: `actual_points[week_num - 1]` is correct (matches Feature 01)
- ✅ Week 17 logic verified: Implementation correctly uses week_num (not actual_week_num) for indexing
- ✅ Malformed JSON handling: PlayerManager handles this internally (no changes needed to Accuracy Sim)
- ⚠️ Edge cases: Reference Feature 01's 25 edge cases for similar patterns applicable to PlayerManager integration
- ⚠️ Test coverage: If user answers "A" to test questions (like Feature 01), expect similar comprehensive test additions

**Success Criteria:**
- Code review confirms logic correctness
- Manual testing shows correct data loaded
- Automated tests provide regression protection
- PlayerManager correctly loads JSON in simulation context
- All three verification parts completed (code review, manual testing, automated tests)

---

### Requirement 7: Align Edge Case Handling with Win Rate Sim

**Description:** Update Accuracy Sim's edge case handling to match Win Rate Sim's behavior for consistency across both simulations

**Source:** Epic Request + User Answer
**Epic Citation:** Line 2: "Both the Win Rate sim and Accuracy Sim should maintain the same functionality"
**User Answer:** Question 4 (Option A) - "Maintain consistency across both simulations"
**Traceability:** Direct user request for "same functionality" + user decision for consistency

**Implementation:**

**Edge Case 1: Missing JSON File**
- Current behavior (both sims): Log warning, continue
- Action: ✅ No change needed (already consistent)

**Edge Case 2: Missing week_N+1 Folder**
- Win Rate Sim behavior: Fallback to projected data (use week_N for both projected and actual)
- Accuracy Sim current behavior: Return (None, None), skip week
- **Action: ⚠️ CHANGE Accuracy Sim to match Win Rate Sim**
- Update `_load_season_data()` lines 330-335:
  - If actual_folder missing: Log warning, return (projected_folder, projected_folder) instead of (None, None)
  - Allows MAE calculation using projected values as fallback actuals
- Update `_evaluate_config_weekly()` to handle fallback case (same folder for both managers)

**Edge Case 3: Array Index Out of Bounds**
- Win Rate Sim behavior: Default to 0.0 if array too short
- Accuracy Sim current behavior: Check array length, silently skip if too short
- **Action: ⚠️ CHANGE Accuracy Sim to match Win Rate Sim**
- Update `_evaluate_config_weekly()` line 485-487:
  - Remove length check: `if 1 <= week_num <= 17 and len(player.actual_points) >= week_num`
  - Add default fallback: `actual = player.actual_points[week_num - 1] if len(player.actual_points) > week_num - 1 else 0.0`
  - Include players with 0.0 actual in MAE calculation (consistent with Win Rate Sim)

**Testing:**
- Add tests for each aligned edge case
- Verify behavior matches Win Rate Sim exactly
- Document alignment in verification report

**Status:** New requirement - edge case alignment needed

---

**Requirements Summary:**

Total Requirements: 7
- ✅ Requirement 1: Epic request (line 5) - Verify PlayerManager JSON loading
- ✅ Requirement 2: Epic request (line 8) - Verify week_N+1 logic
- ✅ Requirement 3: Epic request (line 8) - Verify Week 17 specifically
- ✅ Requirement 4: Epic request (line 8) - Verify two-manager pattern
- ✅ Requirement 5: Epic request (line 6) - Verify array extraction
- ✅ Requirement 6: User constraint (line 10) - Comprehensive verification
- ✅ Requirement 7: Epic request (line 2) + User answer (Q4) - Edge case alignment

All requirements traced to sources.

---

## Data Structures

### JSON File Structure (Same as Feature 01)

**Location:** `simulation/sim_data/{year}/weeks/week_{NN}/`

**Files per week:** 6 position files
- qb_data.json
- rb_data.json
- wr_data.json
- te_data.json
- k_data.json
- dst_data.json

**Source:** Epic Request - "json files contained in the week_X folders" (line 5)

**Format (verified in Feature 01 research):**
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
- `locked`: Boolean (PlayerManager handles conversion)
- `projected_points`: Array of 17 floats (PlayerManager loads into player.projected_points array)
- `actual_points`: Array of 17 floats (PlayerManager loads into player.actual_points array)

---

### Internal Representation (After PlayerManager Loading)

**PlayerManager loads JSON into FantasyPlayer objects:**
```python
# PlayerManager.players is List[FantasyPlayer]
for player in player_mgr.players:
    player.id: str
    player.name: str
    player.position: str
    player.drafted_by: str
    player.locked: bool  # PlayerManager handles conversion from JSON boolean
    player.projected_points: List[float]  # 17-element array
    player.actual_points: List[float]     # 17-element array
```

**Source:** Research finding - PlayerManager from league_helper (already migrated to JSON)
**Traceability:** Accuracy Sim delegates JSON loading to PlayerManager

**Accuracy Sim extracts week-specific values:**
```python
# For week N:
actual = player.actual_points[week_num - 1]  # Extract single value from array
```

---

## Algorithms

### Algorithm 1: Temporary Directory Setup (_create_player_manager)

**Source:** Research finding - lines 339-404

**Current Implementation:**
```
1. Input: config_dict, week_data_path (week_N or week_N+1 folder), season_path
2. Create temporary directory: tempfile.mkdtemp(prefix="accuracy_sim_")
3. Create player_data/ subfolder in temp directory
4. For each position file [qb, rb, wr, te, k, dst]:
   a. source_file = week_data_path / "{position}_data.json"
   b. If source_file exists: copy to temp/player_data/{position}_data.json
   c. If missing: log warning, continue
5. Copy season_schedule.csv from season_path to temp/
6. Copy game_data.csv from season_path to temp/ (if exists)
7. Copy team_data/ folder from season_path to temp/team_data/
8. Write config_dict to temp/league_config.json
9. Create ConfigManager, SeasonScheduleManager, TeamDataManager, PlayerManager instances
10. PlayerManager.load_players_from_json() automatically loads from temp/player_data/
11. Return PlayerManager (with _temp_dir attribute for cleanup)
```

**Verification Needed:**
- Confirm all 6 JSON files are copied correctly
- Confirm PlayerManager loads from temp/player_data/ location
- Confirm no missing files cause errors (only warnings)

---

### Algorithm 2: Week_N+1 Data Loading (_load_season_data)

**Source:** Research finding - lines 293-337

**Current Implementation:**
```
1. Input: season_path, week_num (1-17)
2. projected_folder = season_path / "weeks" / f"week_{week_num:02d}"
3. actual_week_num = week_num + 1
4. actual_folder = season_path / "weeks" / f"week_{actual_week_num:02d}"
5. If projected_folder does NOT exist:
   - Log warning
   - Return (None, None)
6. If actual_folder does NOT exist:
   - Log warning
   - Return (None, None)
7. Return (projected_folder, actual_folder)
```

**Verification Needed:**
- Confirm week 17 correctly returns (week_17, week_18)
- Confirm week_18 folder exists (research confirmed: YES)
- Confirm fallback (None, None) is correct behavior when folder missing

---

### Algorithm 3: Two-Manager Pattern (_evaluate_config_weekly)

**Source:** Research finding - lines 412-533

**Current Implementation:**
```
1. Input: config_dict, week_range (start_week, end_week)
2. For each season in available_seasons:
   a. For each week_num in range(start_week, end_week + 1):
      i.  (projected_path, actual_path) = _load_season_data(season_path, week_num)
      ii. If either path is None: skip this week
      iii. projected_mgr = _create_player_manager(config_dict, projected_path, season_path)
      iv.  actual_mgr = _create_player_manager(config_dict, actual_path, season_path)
      v.   Try:
           - Calculate projections from projected_mgr (score_player for each player)
           - Extract actuals from actual_mgr (actual_points[week_num - 1] for each player)
           - Match by player.id
           - Store in week_projections[week_num], week_actuals[week_num]
           Finally:
           - Cleanup both managers (delete temp directories)
   b. Calculate MAE for this season: accuracy_calculator.calculate_weekly_mae(week_projections, week_actuals, week_range)
3. Aggregate MAE across all seasons
4. Return aggregated AccuracyResult
```

**Verification Needed:**
- Confirm two managers are created per week
- Confirm projected_mgr uses week_N folder, actual_mgr uses week_N+1 folder
- Confirm array indexing is correct (week_num - 1)
- Confirm cleanup happens even if errors occur (finally block)

---

## Dependencies

**This feature depends on:**

- **PlayerManager (league_helper)**
  - Source: Epic notes line 1 ("recent effort updated the league helper")
  - Status: VERIFIED - Already migrated to JSON
  - Evidence: AccuracySimulationManager imports and uses PlayerManager
  - Action: VERIFY PlayerManager works correctly in simulation context

- **Existing JSON data files**
  - Source: Epic Request (user mentioned "json files")
  - Status: VERIFIED - Files exist in simulation/sim_data/2025/weeks/week_01 through week_18
  - Evidence: Feature 01 research verified structure
  - Action: VERIFY Accuracy Sim copies files correctly

- **week_18 folder with week 17 actual data**
  - Source: Epic Request (week 17 verification)
  - Status: VERIFIED - week_18 folder exists (Feature 01 research confirmed)
  - Evidence: week_18/qb_data.json has actual_points[16] = 23.2
  - Action: VERIFY Accuracy Sim uses week_18 for week 17 actuals

**This feature does NOT depend on:**

- Win Rate Sim changes (Feature 01) - independent parallel work
- JSON file format changes (format is established)
- PlayerManager implementation changes (already migrated)

**This feature blocks:**

- Feature 03 (Cross-Simulation Testing) depends on this feature being complete

---

## Edge Cases

### Edge Case 1: Missing JSON File

**Scenario:** One of the 6 position files missing from week folder

**Current Handling:** Log warning, continue (lines 370-373)
```python
if source_file.exists():
    shutil.copy(source_file, player_data_dir / filename)
else:
    self.logger.warning(f"Missing position file: {filename} in {week_data_path}")
```

**Source:** Research finding - already implemented
**Verification Needed:** Confirm this is correct behavior (TBD - create checklist question)

---

### Edge Case 2: Missing week_N+1 Folder

**Scenario:** week_N+1 folder doesn't exist (can't get week N actuals)

**Current Handling:** Return (None, None), skip week (lines 330-335)
```python
if not actual_folder.exists():
    self.logger.warning(f"Actual folder not found: {actual_folder}")
    return None, None
```

**Source:** Research finding - already implemented

**⚠️ CHANGE REQUIRED (per Requirement 7 - User Answer to Question 4):**
- **New behavior:** Fallback to projected data (same as Win Rate Sim)
- Update to: `return (projected_folder, projected_folder)` instead of `(None, None)`
- Allows MAE calculation using projected values as fallback actuals
- Maintains consistency with Win Rate Sim behavior

---

### Edge Case 3: Array Index Bounds

**Scenario:** actual_points array has <17 values

**Current Handling:** Check array length before indexing (line 485)
```python
if 1 <= week_num <= 17 and len(player.actual_points) >= week_num:
    actual = player.actual_points[week_num - 1]
```

**Source:** Research finding - already implemented

**⚠️ CHANGE REQUIRED (per Requirement 7 - User Answer to Question 4):**
- **New behavior:** Default to 0.0 if array too short (same as Win Rate Sim)
- Update to: `actual = player.actual_points[week_num - 1] if len(player.actual_points) > week_num - 1 else 0.0`
- Include players with 0.0 actual in MAE calculation
- Maintains consistency with Win Rate Sim behavior
- Prevents silent data loss from skipping players

---

### Edge Case 4: Null or Zero Actual Points

**Scenario:** player.actual_points[week_num - 1] is None or 0

**Current Handling:** Only include if not None and > 0 (line 487)
```python
if actual is not None and actual > 0:
    actuals[player.id] = actual
```

**Source:** Research finding - already implemented
**Verification Needed:** Confirm this is correct (exclude zeros from MAE calculation)

---

## Testing Strategy

**Verification approach (per user constraint "VERIFY EVERYTHING"):**

### Part 1: Code Review
- Review `_create_player_manager()` implementation line-by-line
- Review `_load_season_data()` implementation line-by-line
- Review `_evaluate_config_weekly()` implementation line-by-line
- Verify JSON file copying is correct
- Verify PlayerManager integration is correct
- Verify array extraction logic is correct

### Part 2: Manual Verification
- Run Accuracy Simulation with JSON data
- Inspect loaded player data for week 1, week 10, week 17
- Verify PlayerManager loads JSON correctly in temp directory context
- Verify week_N+1 logic works correctly
- Confirm week 17 uses week_18 folder for actuals
- Confirm no FileNotFoundError for players.csv

### Part 3: Test Coverage Review
- Inspect tests/integration/test_accuracy_simulation_integration.py to identify coverage gaps
- **Add comprehensive tests for PlayerManager integration if missing (per Question 2 answer - Option A):**
  - Test `_create_player_manager()` creates temp directory with player_data/ subfolder
  - Test JSON files copied from week folder to temp/player_data/
  - Test PlayerManager loads JSON correctly from temporary directory
  - Test handling of all 6 position files (QB, RB, WR, TE, K, DST)
  - Test error handling for missing files (log warning, continue)
  - Test PlayerManager.players array populated correctly
- Verify tests cover week_N+1 logic (_load_season_data returns correct folders)
- **Add dedicated Week 17 edge case test (per Question 3 answer - Option A):**
  - Test `_load_season_data(season_path, week_num=17)` returns (week_17, week_18)
  - Test `_evaluate_config_weekly()` for week 17 creates two managers correctly
  - Test projected_mgr from week_17 folder, actual_mgr from week_18 folder
  - Test array extraction: actual_points[16] from week_18 data
  - Test week_18 folder exists with real week 17 data
- Verify tests cover two-manager pattern (projected_mgr + actual_mgr creation and usage)
- Verify tests cover array extraction (player.actual_points[week_num - 1])
- **Add edge case consistency tests (per Question 4 answer - Option A):**
  - Test missing JSON file: verify warning logged, simulation continues (consistent with Win Rate Sim)
  - Test missing week_N+1 folder: verify fallback to projected data (matches Win Rate Sim behavior)
  - Test array index out of bounds: verify default 0.0 used, player included in MAE (matches Win Rate Sim)
  - Verify all edge case behaviors match Win Rate Sim exactly

**Source:** User Constraint - "ASSUME INCORRECT, VERIFY EVERYTHING" (epic line 10)

---

## Open Questions

(See checklist.md for details)

---

## Completion Criteria

**This feature is complete when:**

- [ ] `_create_player_manager()` verified correct (JSON copying works)
- [ ] `_load_season_data()` verified correct (week_N+1 logic works)
- [ ] `_evaluate_config_weekly()` verified correct (two-manager pattern works)
- [ ] Week 17 specifically verified (uses week_17 projected, week_18 actual)
- [ ] Array extraction verified correct (week_num - 1 indexing)
- [ ] PlayerManager integration verified (loads JSON correctly in simulation context)
- [ ] Edge case handling aligned with Win Rate Sim (missing folders → fallback, array bounds → 0.0)
- [ ] All tests passing (100% pass rate)
- [ ] No FileNotFoundError for players.csv
- [ ] Edge cases tested (missing files, missing folders, array bounds) with consistent behavior
- [ ] Documentation accurate (reflects JSON implementation through PlayerManager)
