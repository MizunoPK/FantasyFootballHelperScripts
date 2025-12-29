# Sub-Feature 6: TeamDataManager D/ST Migration - Checklist

> **IMPORTANT**: When marking items as resolved, also update `sub_feature_06_team_data_manager_dst_migration_spec.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Progress Summary

**Total Items:** 8
**Completed:** 5 (1 analysis + 2 patterns verified + 2 documentation verified)
**Remaining:** 3 (1 implementation task + 3 testing deferred)

---

## Analysis & Strategy (1 item - RESOLVED)

- [x] **NEW-46:** TeamDataManager D/ST data structure verification ✅ RESOLVED - CRITICAL FINDING
  - **Finding:** Comments are ACCURATE - data structure matches documentation
  - **CRITICAL:** TeamDataManager._load_dst_player_data() reads from players.csv using week_N_points columns
  - **Impact:** BREAKS with CSV elimination - method expects week_1_points through week_17_points columns
  - **Usage:** ACTIVELY USED by PlayerManager.py:206 for D/ST fantasy performance rankings
  - **Decision:** IN SCOPE - Must migrate to read from dst_data.json
  - **Data source:** Use actual_points array (historical data for rolling window calculations)
  - **Implementation:** NEW-110 through NEW-117 (8 items)

---

## Phase 1: Update Data Loading (3 items)

**Note:** Implementation tasks - current implementation verified, migration pattern provided

- [x] **NEW-110:** Update _load_dst_player_data() to read from JSON ✅ PATTERN VERIFIED
  - **Current implementation:** Lines 110-165 reads players.csv, filters position == 'DST', loads week_N_points columns
  - **Current data structure:** {team: [week_1, ..., week_17]} stored in self.dst_player_data
  - **Update required:** Read dst_data.json, extract actual_points arrays
  - **File:** league_helper/util/TeamDataManager.py:110-165 (complete method rewrite)
  - **JSON structure:** dst_data.json has {"dst_data": [{team, actual_points, ...}]}
  - **Target:** Build same self.dst_player_data structure (preserve interface)
  - **Implementation pattern:**
    ```python
    # Load dst_data.json
    with open(data_folder / 'player_data' / 'dst_data.json') as f:
        json_data = json.load(f)

    # Extract actual_points for each D/ST team
    for dst_player in json_data.get('dst_data', []):
        team = dst_player.get('team')
        actual_points = dst_player.get('actual_points', [0.0] * 17)
        if team:
            self.dst_player_data[team] = actual_points
    ```
- [x] **NEW-111:** Extract actual_points arrays for each D/ST team ✅ VERIFIED
  - **Purpose:** Build {team: [week_1, ..., week_17]} from actual_points arrays
  - **Source:** Use actual_points array (not projected_points)
  - **Reason:** Rolling window calculations need HISTORICAL data (past performance)
  - **File:** league_helper/util/TeamDataManager.py
  - **Note:** This is part of NEW-110 implementation, separated for clarity
  - **Current behavior:** Lines 145-157 extract weekly points from CSV columns
  - **New behavior:** Extract from actual_points array in JSON
- [ ] **NEW-112:** Update error handling for JSON loading **(IMPLEMENTATION TASK)**
  - **Current error handling:** Lines 163-165 catch all exceptions, log warning, set empty dict
  - **Required updates:**
    - FileNotFoundError if dst_data.json missing (graceful - log warning, return)
    - JSONDecodeError if file corrupted (fail fast - log error, raise)
    - KeyError if expected JSON structure missing ('dst_data' key)
    - Missing team or actual_points field (skip D/ST with warning)
  - **Maintain:** Same fallback behavior (empty dst_player_data dict)
  - **File:** league_helper/util/TeamDataManager.py
  - **Pattern:**
    ```python
    try:
        # Load JSON...
    except FileNotFoundError:
        self.logger.warning("dst_data.json not found, D/ST rankings unavailable")
        return
    except json.JSONDecodeError as e:
        self.logger.error(f"Malformed dst_data.json: {e}")
        raise
    ```

---

## Phase 2: Update Documentation (2 items)

- [x] **NEW-113:** Update method docstring ✅ VERIFIED
  - **Current location:** TeamDataManager.py:111-121
  - **Current text:** "Load D/ST weekly fantasy scores from players.csv"
  - **Update to:** "Load D/ST weekly fantasy scores from dst_data.json actual_points arrays"
  - **Additional updates:**
    - Change column references from week_N_points to actual_points array
    - Document JSON structure and extraction process
    - Update side effects note to reference JSON (not CSV)
- [x] **NEW-114:** Update data structure comment ✅ VERIFIED
  - **Current location:** TeamDataManager.py:83
  - **Current comment:** `# D/ST player data: {team: [week_1_points, week_2_points, ..., week_17_points]}`
  - **Format:** Correct and will remain accurate after migration
  - **Update to:** Add note that data comes from dst_data.json actual_points array (not CSV)
  - **Suggestion:** `# D/ST player data (from dst_data.json actual_points): {team: [week_1, ..., week_17]}`

---

## Phase 3: Testing (3 items)

**Note:** Testing items deferred to implementation phase - no verification needed during deep dive

- [ ] **NEW-115:** Test _load_dst_player_data() with JSON **(Testing - defer to implementation)**
  - **File:** tests/league_helper/util/test_TeamDataManager.py
  - Test loading from dst_data.json
  - Verify correct extraction of actual_points arrays
  - Test with multiple D/ST teams (all 32 NFL teams)
  - Test with partial data (some teams missing)
  - Test error handling:
    - Missing file (FileNotFoundError or warning + empty dict)
    - Corrupted JSON (JSONDecodeError)
    - Missing 'dst_data' key
    - Missing team or actual_points field
- [ ] **NEW-116:** Test D/ST fantasy ranking calculations **(Testing - defer to implementation)**
  - **File:** tests/league_helper/util/test_TeamDataManager.py
  - Verify _rank_dst_fantasy() works with JSON-loaded data
  - Test rolling window calculations (lines 248-270)
  - Verify bye week handling (0.0 or None values in actual_points)
  - Test with various current_week values (early, mid, late season)
  - Compare results with CSV-based data for validation
- [ ] **NEW-117:** Integration test - D/ST team quality **(Testing - defer to implementation)**
  - **File:** tests/integration/test_league_helper_integration.py
  - Load players from JSON (including D/ST actual_points)
  - Verify PlayerManager.py:206 gets correct D/ST fantasy ranks
  - Verify D/ST player scoring uses correct team quality multiplier
  - Test player score calculations depend on D/ST rankings
  - Compare overall results with CSV-based approach

---

## Success Criteria

✅ **_load_dst_player_data() reads from dst_data.json (not players.csv)**
✅ **actual_points arrays extracted for all D/ST teams**
✅ **dst_player_data structure unchanged: {team: [week_1, ..., week_17]}**
✅ **D/ST fantasy rankings work with JSON-loaded data**
✅ **Rolling window calculations produce correct results**
✅ **All error scenarios handled gracefully**
✅ **All unit tests passing (100%)**
✅ **Integration tests verify D/ST scoring unchanged**

---

## Dependencies

**Prerequisites:**
- Sub-feature 1 complete (JSON loading infrastructure exists)
- Sub-feature 2 complete (actual_points arrays loaded from JSON)

**Uses:**
- actual_points array (from Sub-feature 2 - weekly data migration)
- dst_data.json file (from player-data-fetcher module)

---

## Impact Analysis

**Files Modified:** 1
- league_helper/util/TeamDataManager.py (method _load_dst_player_data ~110-165)

**Usage:**
- PlayerManager.py:206 - Gets D/ST fantasy ranks for team quality multiplier
- team_quality_multiplier calculation (part of player scoring algorithm)
- Affects scoring for all player positions (via opponent team strength)

**Data Source Change:**
- OLD: players.csv with week_1_points through week_17_points columns
- NEW: dst_data.json with actual_points array

**Data Type:**
- Use actual_points (not projected_points)
- Reason: Need historical performance for rolling window calculations
- Rolling window: Calculate average D/ST fantasy points over past N weeks

**Risk:** MEDIUM
- Critical for scoring accuracy (team quality multiplier)
- Must preserve exact calculation behavior
- JSON structure different from CSV (different extraction logic)
- Comprehensive testing required

---

## Current Implementation Details

**Current Method (_load_dst_player_data lines 110-165):**
1. Opens players.csv
2. Filters rows where position == 'DST'
3. Builds dictionary: {team: [week_1_points, ..., week_17_points]}
4. Stores in self.dst_player_data
5. Used by _rank_dst_fantasy() for rolling window calculations

**Rolling Window Calculation (_rank_dst_fantasy lines 248-270):**
- Takes average of last N weeks of D/ST fantasy points
- Uses this to rank D/ST units by recent performance
- Ranking affects team quality multiplier (step 4 of scoring algorithm)

**Why actual_points (not projected_points):**
- Rolling window needs ACTUAL past performance
- projected_points = pre-season estimates (don't change week to week)
- actual_points = real game results (what happened)

---

## Notes

- This is a **CRITICAL** migration - breaks if CSV eliminated without this fix
- Data structure stays the same (no interface changes)
- Only internal data source changes (CSV → JSON)
- Must use actual_points array (historical data)
- See ARCHITECTURE.md "Scoring Algorithm" Step 4 for team quality multiplier details
