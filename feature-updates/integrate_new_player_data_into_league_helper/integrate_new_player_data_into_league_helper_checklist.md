# Integrate New Player Data Into League Helper - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `integrate_new_player_data_into_league_helper_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## THREE-ITERATION Question Generation Progress

- [x] Iteration 1: Edge cases, error conditions, configuration options
- [x] Iteration 2: Logging, performance, testing, integration workflows
- [x] Iteration 3: Relationships to similar features, cross-cutting concerns

---

## General Decisions

- [x] **FantasyPlayer field changes:** RESOLVED - Add NEW `drafted_by: str` field, KEEP existing `drafted: int` field, keep synchronized
- [ ] **FantasyPlayer locked field:** Should FantasyPlayer class change `locked` int to boolean, or keep int and convert?
- [x] **Weekly points storage:** RESOLVED - Keep individual `week_N_points` fields, map from `projected_points` array during loading
- [x] **drafted_data.csv elimination:** RESOLVED - Yes, deprecate and stop writing to it
- [x] **DraftedDataWriter fate:** RESOLVED - Will be deprecated/removed (details TBD)
- [x] **players.csv updates:** RESOLVED - Deprecate, do not update or write to it
- [x] **Loading method:** RESOLVED - Create separate `FantasyPlayer.from_json()` method

### NEW Decisions from Research Phase (2025-12-27)

- [x] **DECISION 1 - Weekly data storage:** RESOLVED - Deprecate week_N_points, use projected_points and actual_points arrays
- [x] **DECISION 2 - Conflict resolution:** RESOLVED - drafted_by is source of truth (ignore drafted field if it exists)
- [x] **DECISION 3 - Error handling:** RESOLVED - Comprehensive error handling policy
  - **Missing JSON file:** Fail fast (raise FileNotFoundError)
  - **Malformed JSON:** Fail fast (raise JSONDecodeError)
  - **Missing required fields:** Skip player with warning
  - **Missing optional fields:** Use defaults (no error)
  - **Type mismatches:** Attempt conversion, warn if fails
  - **Wrong array length:** Pad/truncate to 17, log warning
- [x] **DECISION 4 - Write atomicity:** RESOLVED - Three-step atomic write pattern (as specified in Decision 4)
  - **Step 1:** Backup existing file to .bak
  - **Step 2:** Write new data to .tmp file
  - **Step 3:** Atomic rename using os.replace()
  - **Applies to:** All write operations (currently only update_players_file)
  - **Rationale:** Ensures data integrity, prevents corruption, allows recovery
- [x] **DECISION 5 - Directory creation:** RESOLVED - Fail fast if directory missing
  - **Policy:** Raise FileNotFoundError if /data/player_data/ doesn't exist
  - **Rationale:** Consistent with fail-fast error handling (Decision 7)
  - **Error message:** Guides user to run player-data-fetcher
  - **Additional check:** Verify it's a directory (not a file)

---

## Data Source & Structure Questions

### JSON File Structure

**File-level decisions:**
- [x] Location: Confirmed in /data/player_data/
- [x] Naming: Confirmed filenames (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)
- [ ] Format: Each JSON has wrapper key like "qb_data" containing array of players - document exact structure

**Fields Mapping:**

| Field Name | CSV Field | JSON Field | Mapping Strategy | Notes |
|------------|-----------|------------|------------------|-------|
| `id` | id (int) | id (string) | Convert string to int | JSON has string "3918298", need int 3918298 |
| `name` | name | name | Direct | Same format |
| `position` | position | position | Direct | Same format (QB, RB, WR, TE, K, DST) |
| `team` | team | team | Direct | Same format (BUF, DET, etc.) |
| `bye_week` | bye_week (int) | bye_week (int) | [x] Direct | Top-level field in JSON, no conversion needed |
| `drafted_by` | drafted (0/1/2) | drafted_by (string) | [x] Convert via helper | Use set_drafted_status() helper method |
| `locked` | locked (0/1) | locked (bool) | Convert | false -> 0, true -> 1 |
| `fantasy_points` | fantasy_points (float) | N/A (not in JSON) | [x] Calculate | Sum of projected_points array: `sum(data['projected_points'])` |
| `average_draft_position` | average_draft_position | average_draft_position | Direct | Same field name |
| `player_rating` | player_rating | player_rating | Direct | Same field name |
| `week_1_points` through `week_17_points` | week_N_points (17 cols) | **DEPRECATED** | [x] REMOVE FIELDS | Replace with projected_points and actual_points arrays |
| `projected_points` (NEW) | N/A | projected_points (array) | [x] Direct | Store as List[float] with 17 elements |
| `actual_points` (NEW) | N/A | actual_points (array) | [x] Direct | Store as List[float] with 17 elements |
| `injury_status` | injury_status | injury_status | Direct | Same format (ACTIVE, QUESTIONABLE, etc.) |
| (nested stats) | N/A | passing, rushing, receiving, misc, etc. | [x] Store as Optional | See field inventory below |

**Questions:**
- [x] **bye_week source:** ✅ FOUND - Top-level integer field in all JSON files
- [x] **projected vs actual:** ✅ RESOLVED - Deprecate week_N_points, use BOTH arrays (projected_points and actual_points)
- [x] **Additional stats storage:** ✅ RESOLVED - Store all nested stats as Optional[Dict[str, List[float]]] fields
- [x] **Empty drafted_by:** ✅ CONFIRMED - "" means not drafted (verified in actual data)
- [ ] **Validation:** How to handle malformed JSON or missing required fields? → DECISION NEEDED

---

## Weekly Data Migration (NEW from Decision 1)

**DECISION:** Deprecate individual `week_N_points` fields, use arrays instead

**Impact:** This is a **breaking API change** affecting any code that accesses weekly data

**Tasks Required:**
- [ ] **Grep for weekly field access:** Find all code accessing `week_1_points`, `week_2_points`, etc.
  - [ ] Pattern: `.week_\d+_points`
  - [ ] Pattern: `getattr(player, f"week_{week}_points")`
  - [ ] Pattern: `player['week_X_points']` (dict access)
- [ ] **Update FantasyPlayer methods:**
  - [ ] `get_weekly_projections()` - Return `self.projected_points` instead of field list
  - [ ] `get_single_weekly_projection(week)` - Return `self.projected_points[week-1]`
  - [ ] Add new method: `get_weekly_actuals()` - Return `self.actual_points`
  - [ ] Add new method: `get_single_weekly_actual(week)` - Return `self.actual_points[week-1]`
- [ ] **Update all call sites:**
  - [ ] League Helper modes that access weekly data
  - [ ] Any loops iterating over weeks (need to use array indexing)
  - [ ] Any code building weekly projections list
- [ ] **Update from_dict() method:**
  - [ ] Remove loading of week_N_points from CSV (for backward compat during transition)
  - [ ] Or handle both old CSV format and new JSON format
- [ ] **Update to_json() method:**
  - [ ] Write projected_points array
  - [ ] Write actual_points array
  - [ ] Do NOT write week_N_points fields
- [ ] **Testing:**
  - [ ] Unit tests for new array-based methods
  - [ ] Integration tests for modes using weekly data
  - [ ] Verify no code still accessing old week_N_points fields

**Affected Modules (estimated):**
- FantasyPlayer class (method updates)
- AddToRosterMode (if it uses weekly projections)
- StarterHelperMode (definitely uses weekly projections)
- Any scoring/ranking logic using weekly data

**Backward Compatibility:**
- CSV files (if still used anywhere) still have week_N_points columns
- May need transition period where from_dict() supports both formats
- Decide: immediate cutover or gradual migration?

---

## NEW Checklist Items from Decision 1 (Weekly Arrays Migration)

### Code Search & Analysis
- [ ] **NEW-1:** Grep for all direct weekly field access (`.week_\d+_points`)
- [ ] **NEW-2:** Grep for dynamic attribute access (`getattr(player, f"week_{week}_points")`)
- [ ] **NEW-3:** Grep for dictionary access (`player_dict['week_X_points']`)
- [ ] **NEW-4:** Identify all modules accessing weekly data (AddToRoster, StarterHelper, etc.)

### FantasyPlayer Class Updates
- [ ] **NEW-5:** Remove 17 `week_N_points` fields from FantasyPlayer dataclass
- [ ] **NEW-6:** Add `projected_points: List[float]` field (default: [0.0] * 17)
- [ ] **NEW-7:** Add `actual_points: List[float]` field (default: [0.0] * 17)
- [ ] **NEW-8:** Update `get_weekly_projections()` to return `self.projected_points`
- [ ] **NEW-9:** Update `get_single_weekly_projection(week)` to index into array
- [ ] **NEW-10:** Add new method `get_weekly_actuals()` returning `self.actual_points`
- [ ] **NEW-11:** Add new method `get_single_weekly_actual(week)` with array indexing

### from_json() Implementation
- [ ] **NEW-12:** Load `projected_points` array from JSON
- [ ] **NEW-13:** Load `actual_points` array from JSON
- [ ] **NEW-14:** Validate arrays have exactly 17 elements (pad if needed)
- [ ] **NEW-15:** Handle missing arrays (default to [0.0] * 17)

### to_json() Implementation
- [ ] **NEW-16:** Write `projected_points` array to JSON
- [ ] **NEW-17:** Write `actual_points` array to JSON
- [ ] **NEW-18:** Ensure week_N_points fields are NOT written

### Backward Compatibility (from_dict for CSV)
- [x] **NEW-19:** RESOLVED - Immediate cutover, NO backward compatibility
  - **Decision:** Remove week_N_points fields entirely, clean break
  - **Rationale:** User explicitly stated "instead of" old CSV files, wants errors to guide fixes
  - **Action:** Remove ALL week_N_points fields, let compilation errors identify missed spots
- [ ] **NEW-20:** REMOVED - Not needed (immediate cutover)
- [ ] **NEW-21:** REMOVED - Not needed (immediate cutover)

### Codebase Sweep Results (2025-12-27 - DECISION 10)

**✅ COMPREHENSIVE SWEEP COMPLETE** - All week_N_points usage identified

**IN SCOPE - League Helper (12 locations):**

1. **utils/FantasyPlayer.py:102-118** - FIELD DEFINITIONS (17 fields)
   - [ ] **NEW-22a:** Remove all 17 week_N_points field definitions

2. **utils/FantasyPlayer.py:170-186** - from_dict() LOADS week_N_points (17 lines)
   - [ ] **NEW-22b:** Remove all 17 week_N_points loading lines from from_dict()

3. **utils/FantasyPlayer.py:345-351** - get_weekly_projections() METHOD
   - [ ] **NEW-22c:** Change to return `self.projected_points` instead of field list

4. **utils/FantasyPlayer.py:353** - get_single_weekly_projection() METHOD
   - [ ] **NEW-22d:** Change to return `self.projected_points[week_num - 1]` (already correct!)

5. **league_helper/save_calculated_points_mode/SaveCalculatedPointsManager.py:112**
   - USES: `player.get_single_weekly_projection(week)`
   - [ ] **NEW-22e:** VERIFY METHOD STILL WORKS (should be fine - uses method, not fields)

6. **league_helper/starter_helper_mode/StarterHelperModeManager.py:212**
   - USES: `recommendation.player.get_single_weekly_projection(current_week)`
   - [ ] **NEW-22f:** VERIFY METHOD STILL WORKS (should be fine - uses method, not fields)

7. **league_helper/util/player_scoring.py:123**
   - USES: `player.get_single_weekly_projection(week)`
   - [ ] **NEW-22g:** VERIFY METHOD STILL WORKS (should be fine - uses method, not fields)

8. **league_helper/util/PlayerManager.py:307**
   - USES: `player.get_single_weekly_projection(week_num)`
   - [ ] **NEW-22h:** VERIFY METHOD STILL WORKS (should be fine - uses method, not fields)

9. **league_helper/util/PlayerManager.py:375-379** - CSV FIELDNAMES for save_players()
   - LISTS: All 17 week_N_points as CSV columns
   - [ ] **NEW-22i:** CRITICAL - Decide: deprecate save_players() or adapt to JSON?
   - NOTE: Already flagged as NEW-45 in verification report

10. **league_helper/util/PlayerManager.py:633** - COMMENT about dict format
    - [ ] **NEW-22j:** Update comment to reference projected_points/actual_points arrays

11. **league_helper/util/TeamDataManager.py:83, 119** - COMMENTS about D/ST data
    - MENTIONS: "D/ST data: {team: [week_1_points, ..., week_17_points]}"
    - [ ] **NEW-22k:** UPDATE comments to reference new array structure OR verify out of scope
    - NOTE: Already flagged as NEW-46 in verification report

12. **league_helper/util/ProjectedPointsManager.py:53, 108-109** - CSV FORMAT expectations
    - EXPECTS: CSV with week_N_points columns
    - [ ] **NEW-22l:** CRITICAL - Verify if this reads from players.csv or separate source
    - NOTE: Already flagged as NEW-47 in verification report

**OUT OF SCOPE - Separate Modules (not to be modified):**
- player-data-fetcher/ (3 files, ~40 references)
- historical_data_compiler/ (1 file, 5 references)
- All test files (will need updating AFTER implementation)

**ANALYSIS:**
- **Direct field access:** 0 locations (all usage is via methods!)
- **Method calls:** 4 locations (SaveCalculatedPointsManager, StarterHelperModeManager, player_scoring, PlayerManager)
- **Field definitions:** 2 locations (dataclass fields + from_dict loading)
- **Method implementations:** 2 locations (get_weekly_projections, get_single_weekly_projection)
- **CSV/format references:** 6 locations (comments, fieldnames, format expectations)

**GOOD NEWS:** All user-facing code uses methods (`get_single_weekly_projection`), NOT direct field access!
This means only FantasyPlayer needs changes, and the rest should work automatically!

---

### Call Site Updates
- [ ] **NEW-22:** PARENT TASK - Update all identified locations (see NEW-22a through NEW-22l above)
- [ ] **NEW-23:** Replace direct field access with method calls or array indexing (NONE FOUND - already using methods!)
- [ ] **NEW-24:** Update any loops building weekly lists (handled by NEW-22c - get_weekly_projections method)

### Weekly Data Method Analysis (CRITICAL - Decision 10.1)

**⚠️ STOP AND ANALYZE:** Before implementation, we must understand WHEN to use projected vs actual

**Context:**
- OLD: Single `week_N_points` field per week (hybrid: actual for past weeks, projected for future)
- NEW: TWO separate arrays - `projected_points` (pre-game ESPN estimates) and `actual_points` (post-game results)
- QUESTION: Which array should each method return? When should code use which?

**Existing Methods to Update (3 methods):**

- [x] **NEW-25a: ANALYZE get_weekly_projections()** ✅ RESOLVED
  - **Current:** Returns list of all 17 week_N_points fields
  - **Decision:** Returns HYBRID (actual for past weeks, projected for future weeks)
  - **Implementation:** Use config.current_nfl_week to determine cutoff point
  - **Rationale:** Matches OLD week_N_points behavior (verified via codebase analysis)
  - **Code change:** Add hybrid logic to method implementation
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 1" section for full implementation

- [x] **NEW-25b: ANALYZE get_single_weekly_projection(week_num)** ✅ RESOLVED
  - **Current:** Returns week_N_points for specific week via array indexing
  - **Decision:** Returns HYBRID (delegates to get_weekly_projections(), NO CHANGES NEEDED)
  - **Implementation:** Already correct! Method delegates via get_weekly_projections()[week_num-1]
  - **Rationale:** Automatically inherits hybrid behavior from get_weekly_projections()
  - **Code change:** NONE (only needs config dependency)
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 2" section

- [x] **NEW-25c: ANALYZE get_rest_of_season_projection(current_week)** ✅ RESOLVED
  - **Current:** Sums week_N_points from current_week to week 17
  - **Decision:** Returns HYBRID (delegates to get_weekly_projections(), NO CHANGES NEEDED)
  - **Implementation:** Already correct! Method calls get_weekly_projections() and sums
  - **Rationale:** Automatically inherits hybrid behavior from get_weekly_projections()
  - **Code change:** NONE (only needs config dependency)
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 3" section

**New Methods to Add (3+ methods):**

- [x] **NEW-25d: DECIDE if we need get_weekly_actuals()** ✅ RESOLVED
  - **Purpose:** Return all 17 actual_points results
  - **Decision:** DEFER to future features
  - **Rationale:** Not needed for minimum viable migration, no current usage
  - **Future use case:** Historical analysis, performance tracking
  - **Implementation:** Add when needed: `return self.actual_points`
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 4" section

- [x] **NEW-25e: DECIDE if we need get_single_weekly_actual(week_num)** ✅ RESOLVED
  - **Purpose:** Return actual_points[week_num-1] for specific week
  - **Decision:** DEFER to future features
  - **Rationale:** Not needed for minimum viable migration, no current usage
  - **Future use case:** Comparing actual vs projected for individual weeks
  - **Implementation:** Add when needed: `return self.actual_points[week_num - 1]`
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 5" section

- [x] **NEW-25f: DECIDE if we need get_rest_of_season_actual(current_week)** ✅ RESOLVED
  - **Purpose:** Sum actual_points from week 1 to current_week (season-to-date performance)
  - **Decision:** DEFER to future features
  - **Rationale:** Not needed for minimum viable migration, no current usage
  - **Future use case:** Season-to-date performance tracking
  - **Implementation:** Add when needed: `return sum(self.actual_points[:current_week-1])`
  - **See:** WEEKLY_DATA_ANALYSIS.md "Method 6" section

**Critical Usage Analysis:**

**Current Usages of get_single_weekly_projection():**
1. SaveCalculatedPointsManager.py:112 - Getting weekly projection for a specific week
2. StarterHelperModeManager.py:212 - Getting projection for current week (lineup recommendations)
3. player_scoring.py:123 - Getting weekly points for scoring calculations
4. PlayerManager.py:307 - Finding max weekly projection across all players

**All 4 usages appear to want PROJECTED (pre-game estimates) for planning purposes**

**Current Usages of get_rest_of_season_projection():**
1. PlayerManager.py:197 - Sets player.fantasy_points based on rest of season
2. player_scoring.py:487 - Gets original rest of season projection

**Both usages appear to want PROJECTED (future value for planning)**

**Key Questions for User:**
1. Should get_weekly_projections() return ONLY projected_points?
2. Should get_single_weekly_projection() return ONLY projected_points[week-1]?
3. Should get_rest_of_season_projection() return SUM of projected_points[current_week:17]?
4. Do we need actual_points accessor methods NOW, or defer to future feature?
5. For weeks that haven't been played yet, actual_points[i] = 0.0 - is this correct?

---

### Testing
- [ ] **NEW-26:** Unit test for `get_weekly_projections()` with arrays
- [ ] **NEW-27:** Unit test for `get_single_weekly_projection(week)` boundary cases
- [ ] **NEW-28:** Unit test for new `get_weekly_actuals()` methods (if added)
- [ ] **NEW-29:** Integration test for modes using weekly data (StarterHelper, etc.)
- [ ] **NEW-30:** Test from_json() loads both arrays correctly
- [ ] **NEW-31:** Test to_json() writes both arrays correctly

---

## NEW Checklist Items from Research Discoveries

### Position-Specific Stats Fields
- [ ] **NEW-31:** Add `passing: Optional[Dict[str, List[float]]]` to FantasyPlayer
- [ ] **NEW-32:** Add `rushing: Optional[Dict[str, List[float]]]` to FantasyPlayer
- [ ] **NEW-33:** Add `receiving: Optional[Dict[str, List[float]]]` to FantasyPlayer
- [ ] **NEW-34:** Add `misc: Optional[Dict[str, List[float]]]` to FantasyPlayer (QB/RB/WR/TE only)
- [ ] **NEW-35:** Add `extra_points: Optional[Dict[str, List[float]]]` to FantasyPlayer (K only)
- [ ] **NEW-36:** Add `field_goals: Optional[Dict[str, List[float]]]` to FantasyPlayer (K only)
- [ ] **NEW-37:** Add `defense: Optional[Dict[str, List[float]]]` to FantasyPlayer (DST only)
- [ ] **NEW-38:** Load nested stats in from_json() (direct dict copy)
- [ ] **NEW-39:** Write nested stats in to_json() (preserve during round-trip)
- [ ] **NEW-40:** Test round-trip preservation: load → modify → save → reload → verify stats intact

### Scope Clarifications
- [x] **NEW-41:** Confirm simulation module is OUT OF SCOPE (8 .drafted assignments won't be updated) ✅ RESOLVED
  - **Decision:** OUT OF SCOPE - Simulation will be migrated in separate future features
  - **Impact:** 9 locations to update (League Helper + utils only, not 17)
  - **Implication:** Simulation continues using CSV data from simulation/sim_data/ temporarily
  - **Note:** Avoid read-only properties for drafted field (use regular fields + helper methods)
- [x] **NEW-42:** Confirm utils/DraftedRosterManager.py is IN SCOPE (1 .drafted assignment needs update) ✅ RESOLVED
  - **Decision:** IN SCOPE - DraftedRosterManager will be deprecated and replaced
  - **Approach:** Add 3 roster organization methods to PlayerManager instead of DraftedRosterManager
  - **Impact:** 90% of DraftedRosterManager code (680+ lines of fuzzy matching) becomes obsolete
  - **Implementation:** NEW-124 through NEW-135 (12 items)
  - **Analysis:** See DRAFTED_ROSTER_MANAGER_ANALYSIS.md for complete details
- [ ] **NEW-43:** Document simulation incompatibility if read-only properties implemented

### Validation & Error Handling
- [x] **NEW-44:** Position-specific field policy - all Optional (no validation) or validate position matches stats? ✅ RESOLVED
  - **Decision:** NO VALIDATION - All position-specific fields are Optional, no checks
  - **Rationale:** Simple, fast, flexible, appropriate (League Helper doesn't use these stats yet)
  - **Fields:** passing, rushing, receiving, misc, extra_points, field_goals, defense (all Optional[Dict[str, List[float]]])
  - **Loading:** Direct .get() from JSON (returns None if absent)
  - **Validation:** Deferred to future features that actually use these stats (validate at usage time, not load time)
  - **Trust boundary:** player-data-fetcher owns data quality, League Helper trusts source

---

## NEW Checklist Items from Verification Phase (2025-12-27)

### Breaking Change 1: projected_points/actual_points
- [x] **NEW-45:** PlayerManager.update_players_file() migration strategy (HIGH PRIORITY) - RESOLVED
  - **DECISION:** Modified Option A - Write to JSON with selective field updates
  - **Implementation:** Update ONLY drafted_by and locked fields in JSON files
  - **Rationale:** Preserves all stats/projections from player-data-fetcher, maintains single source of truth
  - **Current:** Writes to CSV at PlayerManager.py:349-391
  - **Used by:** AddToRosterMode (1 call), ModifyPlayerDataMode (3 calls)
- [ ] **NEW-46:** TeamDataManager D/ST data structure verification
  - Current: Comments reference [week_1_points, ..., week_17_points] format
  - Action: Verify actual implementation vs documentation
  - Files: TeamDataManager.py:83, 119
- [x] **NEW-47:** ProjectedPointsManager CSV format assumptions ✅ RESOLVED
  - **Finding:** ProjectedPointsManager reads from players_projected.csv (NOT players.csv)
  - **Migration:** Consolidate into PlayerManager (NEW-100 through NEW-109)
  - **Decision:** Eliminate entire ProjectedPointsManager class, add 3 methods to PlayerManager
  - **Covered by:** ProjectedPointsManager consolidation analysis (approved 2025-12-27)

### Breaking Change 3: TeamDataManager D/ST Data

- [x] **NEW-46:** TeamDataManager D/ST data structure verification ✅ RESOLVED - CRITICAL FINDING
  - **Finding:** Comments are ACCURATE - data structure matches documentation
  - **CRITICAL:** TeamDataManager._load_dst_player_data() reads from players.csv using week_N_points columns
  - **Impact:** BREAKS with CSV elimination - method expects week_1_points through week_17_points columns
  - **Usage:** ACTIVELY USED by PlayerManager.py:206 for D/ST fantasy performance rankings
  - **Decision:** IN SCOPE - Must migrate to read from dst_data.json
  - **Data source:** Use actual_points array (historical data for rolling window calculations)
  - **Implementation:** NEW-110 through NEW-117 (8 items)

### Breaking Change 2: drafted_by Field
- [x] **NEW-48:** Document drafted_by team name policy (HIGH PRIORITY) - RESOLVED
  - **DECISION:** Option C - Only track FANTASY_TEAM_NAME, treat all others as opponents
  - **Rationale:** Team names change frequently throughout season, no static list needed
  - **Implementation:**
    - drafted_by == "" → drafted = 0 (not drafted)
    - drafted_by == FANTASY_TEAM_NAME → drafted = 2 (user's team)
    - drafted_by == <any other string> → drafted = 1 (opponent)
  - **No validation needed** - Accept any non-empty string as valid opponent team name

### Breaking Change 3: locked Field
- [x] **NEW-49:** locked field migration strategy decision (HIGH PRIORITY) - RESOLVED
  - **DECISION:** Option A - Change to boolean AND standardize all comparisons to use is_locked()
  - Rationale: More Pythonic, matches JSON format, encapsulates logic
  - Implementation: Change field to bool, update is_locked() method, standardize all usages
  - Locations: 14 comparisons + 2 assignments = 16 total
- [x] **NEW-50:** is_locked() method usage analysis - RESOLVED
  - FantasyPlayer has is_locked() method (line 320)
  - Found: Only tests use it currently
  - **DECISION:** Standardize ALL code to use is_locked() instead of direct field access
- [x] **NEW-51:** is_available() method usage analysis - RESOLVED
  - FantasyPlayer has is_available() method (checks drafted AND locked, line 308)
  - Found: FantasyTeam.py:166 uses it
  - Will be updated to use boolean locked internally

### Cross-Cutting Concerns
- [x] **NEW-52:** update_players_file() usage analysis and migration strategy (HIGH PRIORITY) - RESOLVED
  - **Analysis Complete:** Found 4 calls (AddToRoster: 1, ModifyPlayerData: 3)
  - **Decision:** Same as NEW-45 - migrate to selective JSON updates
  - **Note:** Method is actually `update_players_file()`, not `save_players()`
- [x] **NEW-53:** Verify to_dict() method matches new field structure (HIGH PRIORITY) - RESOLVED
  - **DECISION:** Keep to_dict() using asdict() - no changes needed
  - **Current Implementation:** `return asdict(self)` - outputs ALL dataclass fields
  - **After field updates:** Will automatically output new structure (projected_points, actual_points, drafted_by, locked boolean)
  - **to_json() method:** NOT creating - Decision 4 doesn't need it (can add later if needed)
  - **Rationale:** Simple, automatic, stays in sync with dataclass fields

---

## NEW Checklist Items from Decision 3 (Locked Boolean Migration)

**DECISION:** Change locked to boolean AND standardize all code to use is_locked() method

### FantasyPlayer.py Core Changes (4 items)
- [ ] **NEW-54:** Change locked field definition: `locked: int = 0` → `locked: bool = False`
- [ ] **NEW-55:** Update is_locked() method: `return self.locked == 1` → `return self.locked`
- [ ] **NEW-56:** Update is_available() method: `self.locked == 0` → `not self.locked`
- [ ] **NEW-57:** Update __str__ method line 397: Use `self.is_locked()` instead of `self.locked == 1`

### JSON Loading/Saving (2 items)
- [ ] **NEW-58:** Update from_json(): Load locked boolean directly (no conversion needed)
- [ ] **NEW-59:** Update to_json(): Save locked boolean directly (no conversion needed)

### Standardize Comparisons to use is_locked() (8 items)
- [ ] **NEW-60:** PlayerManager.py:552 - Change `p.locked == 0` → `not p.is_locked()`
- [ ] **NEW-61:** ModifyPlayerDataModeManager.py:338 - Change `p.locked == 1` → `p.is_locked()`
- [ ] **NEW-62:** ModifyPlayerDataModeManager.py:394 - Change `selected_player.locked == 1` → `selected_player.is_locked()`
- [ ] **NEW-63:** ModifyPlayerDataModeManager.py:409 - Change `selected_player.locked == 1` → `selected_player.is_locked()`
- [ ] **NEW-64:** trade_analyzer.py:639 - Change `p.locked == 1` → `p.is_locked()`
- [ ] **NEW-65:** trade_analyzer.py:643 - Change `p.locked == 1` → `p.is_locked()`
- [ ] **NEW-66:** trade_analyzer.py:820 - Change `p.locked == 1` → `p.is_locked()`
- [ ] **NEW-67:** trade_analyzer.py:824 - Change `p.locked == 1` → `p.is_locked()`

### Assignment Updates to use True/False (2 items)
- [ ] **NEW-68:** ModifyPlayerDataModeManager.py:401 - Change `selected_player.locked = 0 if was_locked else 1` → `False if was_locked else True`
- [ ] **NEW-69:** trade_analyzer.py:181 - Change `p_copy.locked = 0` → `p_copy.locked = False`

### Testing (5 items)
- [ ] **NEW-70:** Test is_locked() method with boolean field
- [ ] **NEW-71:** Test is_available() method with boolean locked
- [ ] **NEW-72:** Test from_json() loads locked boolean correctly
- [ ] **NEW-73:** Test to_json() saves locked boolean correctly
- [ ] **NEW-74:** Test all modes using locked field (ModifyPlayerData, trade_analyzer)

---

## NEW Checklist Items from Decision 4 (update_players_file Migration)

**DECISION:** Migrate update_players_file() to selective JSON updates (only drafted_by and locked fields)

### Core Implementation (8 items)
- [ ] **NEW-75:** Implement selective JSON update algorithm
  - Read existing JSON file for each position
  - Parse JSON structure (position key wrapper + array)
  - Match players by ID between self.players and JSON data
  - Update ONLY drafted_by and locked fields for matched players
  - Preserve all other fields exactly as-is
- [ ] **NEW-76:** Implement backup strategy before writes
  - Create .bak file before overwriting JSON
  - Handle backup rotation (keep N backups?)
  - Log backup creation
- [ ] **NEW-77:** Handle player not found in JSON
  - Player in self.players but not in JSON file
  - Should we add the player? Or skip with warning?
  - Log warning for unmatched players
- [ ] **NEW-78:** Handle position file missing
  - What if qb_data.json doesn't exist?
  - Create new file? Or error?
  - Consistent with directory creation policy (Decision 5)
- [ ] **NEW-79:** Implement atomic writes with temp files
  - Write to .tmp file first
  - Rename to actual filename only if write succeeds
  - Prevents corruption if write fails mid-operation
- [ ] **NEW-80:** Preserve JSON formatting and structure
  - Maintain same indentation (indent=2)
  - Preserve field order in JSON
  - Maintain position key wrapper format
- [ ] **NEW-81:** Update method signature and docstring
  - Update docstring to reflect JSON writing (not CSV)
  - Update return message ("Updated 6 JSON files" vs "Updated players.csv")
  - Update logging messages
- [ ] **NEW-82:** Performance optimization considerations
  - Should we only write files for positions that changed?
  - Track dirty flags per position?
  - Or just write all 6 files every time (simpler)?

### Field Conversion Logic (3 items)
- [ ] **NEW-83:** Convert drafted → drafted_by for JSON write
  - Use reverse mapping: drafted=0 → "", drafted=2 → "Sea Sharp", drafted=1 → (need team name)
  - **PROBLEM:** For drafted=1, we need the actual team name - where do we get it?
  - **SOLUTION:** Use player.drafted_by field (should already be set if using hybrid approach)
- [ ] **NEW-84:** Convert locked int → boolean for JSON write
  - After Decision 3, locked is already boolean in FantasyPlayer
  - Direct write, no conversion needed
  - Verify this assumption holds
- [ ] **NEW-85:** Verify no week_N_points written to JSON
  - JSON should have projected_points and actual_points arrays
  - Do NOT write individual week_N_points fields
  - Verify to_json() outputs correct format

### Error Handling (4 items)
- [ ] **NEW-86:** Handle JSON parsing errors
  - Malformed JSON file
  - Should we error or skip file with warning?
  - Log error with filename
- [ ] **NEW-87:** Handle file write permission errors
  - JSON file is read-only
  - Directory is read-only
  - Disk full scenarios
- [ ] **NEW-88:** Handle concurrent access issues
  - What if another process is reading/writing JSON?
  - File locking needed?
  - Or just accept race condition risk?
- [ ] **NEW-89:** Rollback strategy on failure
  - If writing 3rd file fails, should we rollback first 2?
  - Or leave partial update?
  - Restore from .bak files?

### Testing (5 items)
- [ ] **NEW-90:** Unit test update_players_file() with mock JSON files
  - Create test JSON with known data
  - Update drafted_by and locked for some players
  - Verify other fields unchanged
- [ ] **NEW-91:** Test round-trip preservation
  - Load JSON → Modify drafted/locked → Save → Reload
  - Verify all stats (passing, rushing, etc.) unchanged
  - Verify only drafted_by and locked changed
- [ ] **NEW-92:** Test error scenarios
  - Missing JSON file
  - Malformed JSON
  - Write permission errors
  - Player not found in JSON
- [ ] **NEW-93:** Integration test with AddToRosterMode
  - Draft a player
  - Verify update_players_file() writes to JSON
  - Reload League Helper
  - Verify drafted status persists
- [ ] **NEW-94:** Integration test with ModifyPlayerDataMode
  - Lock/unlock players
  - Add/drop players
  - Verify all changes persist to JSON
  - Verify no data loss

### Dependency Updates (2 items)
- [x] **NEW-95:** Update to_json() method in FantasyPlayer - RESOLVED
  - **DECISION:** Do NOT create to_json() method
  - **Rationale:** Decision 4 (update_players_file) doesn't need it - accesses fields directly
  - **Alternative:** Can add later if future features need it
  - **Related:** NEW-53 (to_dict verification)
- [ ] **NEW-96:** Verify from_json() round-trip compatibility
  - from_json() should load all fields that update_players_file() writes (drafted_by, locked)
  - All other fields preserved from original JSON (stats, projections, etc.)
  - No fields lost in round-trip

---

## PlayerManager Integration

### Current CSV Loading (load_players_from_csv method - line 142)

- [x] **Method identification:** `PlayerManager.load_players_from_csv()` at line 142
- [x] **File path:** `self.file_str = str(data_folder / 'players.csv')` at line 129
- [x] **Current flow:** Reads CSV → calls `FantasyPlayer.from_dict(row)` → validates → appends to `self.players`
- [x] **Max projection calculation:** Calculates `self.max_projection` from fantasy_points
- [x] **Team loading:** After loading players, calls `load_team()` which filters `p.drafted == 2`

### New JSON Loading Strategy

- [ ] **Method name:** Should we rename `load_players_from_csv()` to `load_players_from_json()` or keep name?
- [ ] **File paths:** Need to load all 6 JSON files (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)
- [ ] **JSON parsing:** Use `json.load()` to read each file, access position key ("qb_data"), iterate array
- [ ] **Combining positions:** How to combine all 6 position files into single `self.players` list?
- [ ] **Error handling:** What if one position file is missing? Skip position or error?
- [ ] **Performance:** Loading 6 files vs 1 CSV - is this acceptable?
- [ ] **Validation:** Should we validate JSON schema or just try/except?

---

## FantasyPlayer Class Changes

### Current Structure (utils/FantasyPlayer.py)
- [x] **Constructor:** Uses `@dataclass` with fields defined as class attributes
- [x] **from_dict method:** Line 141 - creates FantasyPlayer from dictionary (used for CSV rows)
- [x] **Drafted field:** Line 95 - `drafted: int = 0` (0=not drafted, 1=drafted by opponent, 2=on our roster)
- [x] **Locked field:** Line 96 - `locked: int = 0` (0=unlocked, 1=locked)
- [x] **Weekly points:** Lines 102-118 - individual fields `week_1_points` through `week_17_points`
- [x] **get_weekly_projections:** Line 347 - returns array `[self.week_1_points, ..., self.week_17_points]`
- [x] **get_single_weekly_projection:** Line 353 - accesses via `get_weekly_projections()[week_num - 1]`

### Modification Strategy - RESOLVED

**DECISION: Hybrid Approach (Best of Both Worlds)**
- [x] **Add NEW field:** `drafted_by: str = ""` to store team name
- [x] **Keep existing field:** `drafted: int = 0` for backwards compatibility
- [x] **Synchronization:** Keep both fields synchronized - when one changes, update the other
- [x] **Keep existing:** `locked: int` and individual `week_N_points` fields (convert from JSON)
- [x] **New method:** Create `FantasyPlayer.from_json()` method (keep `from_dict()` for CSV)
- [x] **File writes:** Write `drafted_by` string to JSON files only
- [x] **CSV deprecation:** Stop updating players.csv entirely

**NEW QUESTIONS FROM THIS DECISION:**
- [x] **Synchronization logic location:** RESOLVED - Option C: Helper method in FantasyPlayer
  - Method name: `set_drafted_status(drafted_value, team_name="")`
  - Centralizes sync logic
  - All call sites (7+ locations) will use helper instead of direct assignment
- [x] **Helper method signature:** RESOLVED - Strict validation approach
  - team_name REQUIRED for drafted=1 (raise ValueError if missing)
  - Validate drafted_value in [0,1,2] (raise ValueError if not)
  - Final signature with validation:
    ```python
    def set_drafted_status(self, drafted_value: int, team_name: str = "") -> None:
        if drafted_value not in [0, 1, 2]:
            raise ValueError(f"drafted_value must be 0, 1, or 2, got {drafted_value}")
        if drafted_value == 1 and not team_name:
            raise ValueError("team_name required when drafted_value=1")
        # ... set fields
    ```
- [x] **Direct assignment:** RESOLVED - Option C: Make drafted read-only property
  - `drafted` becomes read-only (property with no setter)
  - `drafted_by` also becomes read-only (for consistency)
  - ONLY way to change: `set_drafted_status()` helper method
  - Implementation approach:
    ```python
    @dataclass
    class FantasyPlayer:
        # Private fields
        _drafted: int = field(default=0, init=False, repr=False)
        _drafted_by: str = field(default="", init=False, repr=False)

        @property
        def drafted(self) -> int:
            return self._drafted

        @property
        def drafted_by(self) -> str:
            return self._drafted_by

        # No setters - read-only!
    ```
  - **CONSEQUENCE:** ALL 7+ locations that assign `player.drafted = X` must be updated
- [x] **Loading behavior:** RESOLVED - Option B: Use public helper method
  - `from_json()` will call `set_drafted_status()` to set fields
  - Validation runs during loading (ensures data integrity)
  - Consistent API usage throughout codebase
  - Implementation in from_json():
    ```python
    drafted_by_value = data.get("drafted_by", "")
    if drafted_by_value == "":
        player.set_drafted_status(0)
    elif drafted_by_value == Constants.FANTASY_TEAM_NAME:
        player.set_drafted_status(2)
    else:
        player.set_drafted_status(1, drafted_by_value)
    ```
- [x] **Validation:** RESOLVED - No longer needed! Read-only properties enforce consistency
  - Fields can only be changed via helper method
  - Helper method enforces synchronization
  - Impossible to create inconsistent state through public API
- [ ] **Conflict resolution:** If JSON has both fields and they conflict, which is source of truth?
  - Assume drafted_by is source of truth (calculate drafted from it)
  - During loading, only load drafted_by from JSON, calculate drafted
- [ ] **Dataclass compatibility:** How to use properties with @dataclass decorator?
  - Properties work with dataclass, but need field(init=False, repr=False) for private fields
  - May need to adjust from_dict() and from_json() to handle private fields
- [ ] **Files to update:** CRITICAL - Which files currently SET drafted and need to use helper?
  - Identified so far: FantasyTeam.py (3 locations), ModifyPlayerDataMode (4 locations)
  - **MUST grep for complete list:** `.drafted = ` and `.drafted=` patterns
  - All must be changed to `set_drafted_status()` before code will work
  - This is a BREAKING CHANGE - all assignments will fail with AttributeError

---

## Drafted Status Logic Changes

### Current Usage Patterns (found via grep)

**Files using drafted field:**
1. `util/PlayerManager.py` line 329: `drafted_players = [p for p in self.players if p.drafted == 2]`
2. `util/FantasyTeam.py` lines 192, 204, 247: Sets `player.drafted = 0` or `2`
3. `util/player_search.py` lines 51, 54, 57: Filters by `drafted == 0/1/2`
4. `modify_player_data_mode/ModifyPlayerDataModeManager.py` lines 231, 236, 290, 303, 357, 359: Sets and checks drafted
5. `reserve_assessment_mode/ReserveAssessmentModeManager.py` line 170: Checks `drafted == 0`
6. `add_to_roster_mode/AddToRosterModeManager.py`: (found in grep output)
7. `trade_simulator_mode/TradeSimulatorModeManager.py`: Uses drafted_data.csv
8. `utils/FantasyPlayer.py` __str__ method lines 389-394: Display logic for drafted status

### New Logic Mapping - RESOLVED

**DECISION: Hybrid approach with both fields**

**Loading from JSON (in from_json() method):**
```python
drafted_by_value = json_data.get("drafted_by", "")
player.drafted_by = drafted_by_value  # Store team name

# Calculate drafted int from drafted_by
if drafted_by_value == "":
    player.drafted = 0
elif drafted_by_value == Constants.FANTASY_TEAM_NAME:
    player.drafted = 2
else:
    player.drafted = 1
```

**When setting drafted in code:**
```python
# Example: User drafts a player
player.drafted = 2
player.drafted_by = Constants.FANTASY_TEAM_NAME

# Example: Opponent drafts
player.drafted = 1
player.drafted_by = "Fishoutawater"  # Actual team name

# Example: Undrafting
player.drafted = 0
player.drafted_by = ""
```

**Writing to JSON (in update_players_file()):**
- Write `drafted_by` field (string with team name)
- Do NOT write `drafted` field (calculated from drafted_by on load)

**Questions - RESOLVED:**
- [x] **Opponent team tracking:** YES - `drafted_by` field stores actual team name
- [x] **Round-trip problem:** SOLVED - `drafted_by` preserved, `drafted` calculated on load
- [x] **DraftedDataWriter dependency:** RESOLVED - Deprecated, will not write to drafted_data.csv

---

## Locked Status Logic Changes

### Current Usage Patterns

**Files using locked field:**
- `utils/FantasyPlayer.py` line 96: Field definition `locked: int = 0`
- `utils/FantasyPlayer.py` line 397: Display logic `if self.locked == 1`
- (Need to grep more thoroughly for other usage)

### New Logic Mapping

**If keeping `locked` as int:**
- When loading from JSON: `locked (boolean)` → `locked = 1 if json_value else 0`
- When saving to JSON: `locked (int)` → `locked = bool(locked)`

**If changing to boolean:**
- Change field to `locked: bool = False`
- Update any code that checks `locked == 1` to `locked == True` or just `if locked:`
- Update any code that checks `locked == 0` to `locked == False` or `if not locked:`

**Questions:**
- [ ] **Usage frequency:** How often is locked used? Is it worth migrating to boolean?
- [ ] **Default value:** JSON has `locked: false` - confirm this means not locked?

---

## File Update Strategy

### Current: update_players_file() method
- [x] **Location:** PlayerManager.py line 349
- [x] **Current behavior:** Writes `self.players` back to CSV file
- [x] **Usage:** Called after drafting players or modifying data

### New Strategy - RESOLVED

**DECISION: Option A - Write back to JSON files**

- Split players by position when writing
- Write each position's players to respective JSON file (qb_data.json, etc.)
- Maintain JSON structure with position key wrapper
- Single source of truth (JSON only, no CSV)

**Implementation approach:**
```python
def update_players_file(self) -> str:
    """Write all players back to position-specific JSON files."""
    # Group players by position
    by_position = {'QB': [], 'RB': [], 'WR': [], 'TE': [], 'K': [], 'DST': []}
    for player in self.players:
        by_position[player.position].append(player)

    # Write each position file
    for position, players in by_position.items():
        filepath = self.data_folder / "player_data" / f"{position.lower()}_data.json"
        json_data = {
            f"{position.lower()}_data": [player.to_json() for player in players]
        }
        with open(filepath, 'w') as f:
            json.dump(json_data, f, indent=2)
```

**NEW QUESTIONS FROM THIS DECISION:**
- [x] **Unknown fields preservation:** RESOLVED - Option C: Add all possible fields to FantasyPlayer
  - Explicit, typed approach
  - All stats will be Optional fields in FantasyPlayer class
  - Makes future feature development easier
- [ ] **Field inventory:** What are ALL possible fields in JSON?
  - Need to examine QB, RB, WR, TE, K, DST JSON files
  - Document complete list of fields for each position
  - Determine which are position-specific vs universal
- [ ] **Nested structure:** How to handle nested dicts (passing, rushing, receiving)?
  - Keep as nested dicts: `passing: Optional[Dict[str, List[float]]]`?
  - Or flatten: `passing_completions: Optional[List[float]]`?
  - Nested is cleaner and matches JSON structure
- [ ] **Position-specific fields:** How to handle fields only certain positions have?
  - QB has passing, RB/WR have rushing+receiving, K has kicking, DST has defensive
  - Make all Optional and set to None for positions that don't use them?
  - Or use typing.Union with position-specific subclasses?
- [ ] **to_json() implementation:** Now straightforward - serialize all fields
  - Convert week_N_points back to projected_points array
  - Convert drafted → drafted_by (already have drafted_by)
  - Convert locked int → boolean
  - Include all nested stat dicts
- [ ] **Write atomicity:** What if write fails partway through (wrote 3 files, failed on 4th)?
  - Should we write to temp files first, then rename?
  - Should we backup existing files before writing?
- [ ] **Error handling:** What if position file directory doesn't exist?
  - Create it automatically?
  - Raise error?
- [ ] **Performance:** Is writing 6 JSON files acceptable?
  - Each file ~100KB with rich stats
  - Probably fine, but should measure

**Questions:**
- [x] **Write strategy:** RESOLVED - Option A: Write to JSON files
- [x] **Backwards compatibility:** No - players.csv is deprecated
- [ ] **Additional stats preservation:** How to preserve passing/rushing stats we don't use during round-trip?

---

## drafted_data.csv Elimination

### Current Usage (found via grep)

**Files using drafted_data.csv:**
1. `util/DraftedDataWriter.py` - Entire class manages this file
2. `modify_player_data_mode/ModifyPlayerDataModeManager.py` - Uses DraftedDataWriter to add/remove players
3. `trade_simulator_mode/TradeSimulatorModeManager.py` line 206-209 - Loads drafted_data.csv for trade simulation
4. `save_calculated_points_mode/SaveCalculatedPointsManager.py` line 134 - References file

### Elimination Strategy

**What drafted_data.csv provides:**
- Maps player names to team names (which team drafted which player)
- Format: "Player Name POSITION - TEAM,Team Name"
- Used by Trade Simulator to know opponent rosters

**Replacement Strategy:**
- JSON `drafted_by` field contains team name directly
- Can filter `[p for p in players if p.drafted_by == "Fishoutawater"]` to get opponent roster
- No longer need separate file

**Questions:**
- [ ] **Trade Simulator impact:** Does Trade Simulator need drafted_data.csv or can it use drafted_by from JSON?
- [ ] **DraftedDataWriter removal:** Should we delete DraftedDataWriter class entirely?
- [ ] **Modify Player Data mode:** How should this mode update drafted_by? Write back to JSON or keep in memory?
- [ ] **File cleanup:** Should we delete drafted_data.csv from /data/ folder?

---

## Integration Points

### LeagueHelperManager
- [ ] **Impact:** Main entry point - does it interact with player loading? Need to verify

### AddToRosterMode (Draft Helper)
- [x] **Uses:** Filters players by `drafted == 0` (available players)
- [ ] **Change needed:** Update filter logic if changing to drafted_by

### StarterHelperMode (Roster Optimizer)
- [x] **Uses:** Works with team roster (drafted == 2 players)
- [ ] **Change needed:** Verify no direct drafted access

### TradeSimulatorMode
- [x] **Uses:** Loads drafted_data.csv to build opponent rosters
- [ ] **Change needed:** Load from drafted_by field instead of CSV file
- [ ] **File location:** TradeSimulatorModeManager.py line 206

### ModifyPlayerDataMode
- [x] **Uses:** Allows marking players as drafted/undrafted, uses DraftedDataWriter
- [ ] **Change needed:** Update to modify drafted_by field and optionally write back to JSON

### ReserveAssessmentMode
- [x] **Uses:** Filters available players (drafted == 0)
- [ ] **Change needed:** Update filter logic if changing to drafted_by

---

## Error Handling & Edge Cases

### Missing Files
- [ ] **What if JSON file missing:** Should we error or skip that position?
- [ ] **What if all JSON files missing:** Error with clear message?
- [ ] **Fallback to CSV:** Should we fallback to loading players.csv if JSON missing?

### Malformed Data
- [ ] **Invalid JSON:** How to handle JSON parsing errors?
- [ ] **Missing required fields:** What if id, name, or position is missing?
- [ ] **Type mismatches:** What if drafted_by is not a string, or locked is not a boolean?
- [ ] **Empty arrays:** What if projected_points array is empty or wrong length?

### Data Validation
- [ ] **Position validation:** Should we validate position is in [QB, RB, WR, TE, K, DST]?
- [ ] **Team name validation:** Should we validate team names against VALID_TEAMS constant?
- [ ] **ID uniqueness:** Should we check for duplicate player IDs?

---

## Testing & Validation

### Unit Tests
- [ ] **Test files location:** tests/league_helper/util/test_PlayerManager.py - needs updates
- [ ] **Test data:** Will need to create test JSON files for unit tests
- [ ] **Test coverage:** Need tests for JSON loading, field mapping, error handling

### Integration Tests
- [ ] **End-to-end:** Test all four modes work with JSON data
- [ ] **Drafted status:** Test drafted_by conversion logic
- [ ] **Weekly points:** Test that get_single_weekly_projection still works

### Manual Testing
- [ ] **Smoke test plan:** Load league_helper, verify all modes work
- [ ] **Data verification:** Compare player list from JSON vs old CSV to ensure same players
- [ ] **Drafted players:** Verify team roster loads correctly (drafted == 2 / drafted_by == "Sea Sharp")

---

## Performance Considerations

### Load Time
- [ ] **6 files vs 1 file:** Is loading 6 JSON files slower than 1 CSV?
- [ ] **JSON parsing:** Is json.load() performance acceptable for file sizes?
- [ ] **Memory usage:** Are we loading unnecessary stats (passing, rushing) that waste memory?

### Optimization Options
- [ ] **Lazy loading:** Load position files on demand vs all upfront?
- [ ] **Caching:** Cache parsed JSON in memory?
- [ ] **Selective loading:** Only load fields we need, ignore detailed stats?

---

## Configuration & Paths

- [ ] **Data folder path:** Is /data/player_data/ path hardcoded or should it be configurable?
- [ ] **Constants access:** Where is FANTASY_TEAM_NAME accessed from? (Found: league_helper/constants.py line 19)
- [ ] **Config manager:** Does ConfigManager need any updates for JSON paths?

---

## Logging & Debugging

- [ ] **Log messages:** What should we log during JSON loading?
- [ ] **Success messages:** "Loaded N players from position_data.json"?
- [ ] **Error messages:** Clear messages for missing files, parsing errors?
- [ ] **Debug output:** Should we log field mapping conversions?

---

## Additional Stats Handling

**JSON has rich stats not in CSV:**
- `passing`: {completions[], attempts[], pass_yds[], pass_tds[], interceptions[], sacks[]}
- `rushing`: {attempts[], rush_yds[], rush_tds[], fumbles[]}
- `receiving`: {receptions[], targets[], rec_yds[], rec_tds[]}
- (other position-specific stats)

**Questions:**
- [ ] **Storage:** Should FantasyPlayer store these stats for future use?
- [ ] **Ignore:** Should we just ignore them during loading?
- [ ] **Future features:** Will future features need these stats?
- [ ] **Memory impact:** How much memory would storing all stats use?

---

## Execution Path Coverage

### Core Operation: Player Data Loading

**All execution paths that load player data:**

1. **PlayerManager.__init__()** → `load_players_from_csv()` → loads all players
   - **Needs update:** YES - change to load from JSON
   - **Location:** league_helper/util/PlayerManager.py line 137

2. **ModifyPlayerDataMode** - May reload or modify players
   - **Needs update:** MAYBE - verify if it reloads or just modifies in memory
   - **Location:** league_helper/modify_player_data_mode/ModifyPlayerDataModeManager.py

### Core Operation: Drafted Status Checking

**All execution paths that check drafted status:**

1. **AddToRosterMode** - Filters available players (drafted == 0)
2. **ReserveAssessmentMode** - Filters available players (drafted == 0)
3. **ModifyPlayerDataMode** - Sets and checks drafted
4. **player_search.py** - Filters by drafted status
5. **PlayerManager.load_team()** - Filters drafted == 2
6. **FantasyTeam** - Sets drafted when adding/removing players

**All need update if changing to drafted_by string**

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player list | /data/player_data/*.json (6 files) | ✓ Verified |
| Drafted status | drafted_by field in JSON | ✓ Verified (string with team name) |
| Locked status | locked field in JSON | ✓ Verified (boolean) |
| Weekly projections | projected_points array in JSON | ✓ Verified (17-element array) |
| Bye week | ??? | ⏳ Need to locate in JSON |
| Additional stats | passing, rushing, receiving objects in JSON | ✓ Verified (nested objects with arrays) |
| Fantasy points (ROS) | Calculated from projected_points array | [ ] Need to confirm calculation |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| JSON file locations | Confirmed in /data/player_data/ with 6 position files | 2025-12-26 |
| JSON structure | Each file has position key wrapper (e.g., "qb_data") with array of players | 2025-12-26 |
| drafted_by format | String field with team name or empty string | 2025-12-26 |
| locked format | Boolean field (true/false) | 2025-12-26 |
| weekly_points format | Array called projected_points with 17 elements | 2025-12-26 |
| Current CSV loading | PlayerManager.load_players_from_csv() at line 142 | 2025-12-26 |
| drafted field usage | Used in 8 files with patterns: drafted == 0/1/2 | 2025-12-26 |
| FANTASY_TEAM_NAME | Defined in constants.py as "Sea Sharp" | 2025-12-26 |
| drafted_data.csv usage | Used by Trade Simulator and ModifyPlayerDataMode | 2025-12-26 |
| **bye_week field** | **FOUND - Top-level integer in all JSON files** | **2025-12-27** |
| **empty drafted_by** | **CONFIRMED - "" means not drafted (verified in actual data)** | **2025-12-27** |
| **fantasy_points** | **NOT in JSON - must calculate as sum(projected_points)** | **2025-12-27** |
| **Complete field inventory** | **Documented 12 universal + position-specific nested stats** | **2025-12-27** |
| **misc field** | **NEW DISCOVERY - Contains fumbles array (QB/RB/WR/TE only)** | **2025-12-27** |
| **Nested structure** | **Keep as-is (don't flatten), matches JSON, easier round-trip** | **2025-12-27** |
| **Dataclass compatibility** | **Properties work with @dataclass (existing code proves it)** | **2025-12-27** |
| **All .drafted assignments** | **17 total: 9 in scope (league_helper+utils), 8 out of scope (simulation)** | **2025-12-27** |
| **DECISION 1: weekly data** | **Deprecate week_N_points, use projected_points and actual_points arrays** | **2025-12-27** |
| **DECISION 2: conflict resolution** | **drafted_by is source of truth (ignore drafted field if present)** | **2025-12-27** |
| **DECISION 3: locked field** | **Migrate to boolean AND standardize to use is_locked() method** | **2025-12-27** |
| **DECISION 4: update_players_file()** | **Migrate to selective JSON updates (only drafted_by/locked fields)** | **2025-12-27** |
| **DECISION 5: Team name policy** | **Only track FANTASY_TEAM_NAME, treat all others as opponents** | **2025-12-27** |
| **DECISION 6: Serialization** | **Keep to_dict() using asdict(), don't create to_json()** | **2025-12-27** |
| **DECISION 7: Error handling** | **Fail fast for critical, graceful for recoverable** | **2025-12-27** |
| **DECISION 8: Write atomicity** | **Formalize three-step pattern (backup, temp write, atomic rename)** | **2025-12-27** |
| **DECISION 9: Directory creation** | **Fail fast if /data/player_data/ missing (raise FileNotFoundError)** | **2025-12-27** |
| **DECISION 10: Backward compatibility** | **NO support for old CSV week_N_points (immediate cutover, clean break)** | **2025-12-27** |
| **Weekly data method analysis** | **All 6 method decisions resolved (3 hybrid, 3 deferred) - NEW-25a through NEW-25f** | **2025-12-27** |
| **ProjectedPointsManager scope** | **IN SCOPE - Include CSV to JSON migration (NEW-100 through NEW-122, 23 items)** | **2025-12-27** |
| **NEW-41: Simulation module scope** | **OUT OF SCOPE - Separate future features (9 League Helper locations only, not 17)** | **2025-12-27** |
| **NEW-42: DraftedRosterManager scope** | **IN SCOPE - Deprecate 711-line class, add 3 methods to PlayerManager (NEW-124 through NEW-135, 12 items)** | **2025-12-27** |
| **NEW-44: Position-specific field policy** | **NO VALIDATION - All Optional fields, no position checks (trust data source, validate at usage time)** | **2025-12-27** |
| **NEW-46: TeamDataManager D/ST verification** | **IN SCOPE - CRITICAL FINDING - Reads week_N_points from players.csv, must migrate to dst_data.json actual_points (NEW-110 through NEW-117, 8 items)** | **2025-12-27** |
| **NEW-47: ProjectedPointsManager migration** | **CONSOLIDATE into PlayerManager - Eliminates ~200 line class, adds 3 methods (NEW-100 through NEW-109, 10 items)** | **2025-12-27** |

---

**Progress:**
- ✅ 47 items resolved:
  - 17 research findings
  - 10 major policy decisions (DECISION 1-10)
  - 5 verification items (NEW-49, NEW-50, NEW-51, NEW-45, NEW-52)
  - 4 additional policy items (NEW-48, NEW-53, NEW-95, NEW-47)
  - 6 weekly data method analysis items (NEW-25a through NEW-25f)
  - 4 scope decisions (ProjectedPointsManager, Simulation, DraftedRosterManager, TeamDataManager)
  - 1 validation policy (NEW-44: Position-specific fields - no validation)
- ✅ **ALL DECISIONS RESOLVED!** Planning phase complete, ready for Phase 3 (Report and Pause)
- 🆕 132 NEW checklist items added (REVISED):
  - From Decision 1 (44 items):
    - NEW-1 to NEW-30: Weekly array migration tasks (30 items)
    - NEW-31 to NEW-40: Position-specific stats fields (10 items)
    - NEW-41 to NEW-44: Scope and validation decisions (4 items)
  - From Verification Phase (9 items):
    - NEW-45 to NEW-47: Breaking Change 1 verification (3 items)
    - NEW-48: Breaking Change 2 verification (1 item)
    - NEW-49 to NEW-51: Breaking Change 3 verification (3 items)
    - NEW-52 to NEW-53: Cross-cutting concerns (2 items)
  - From Decision 3 (21 items): NEW-54 to NEW-74 (locked field migration)
  - From Decision 4 (22 items): NEW-75 to NEW-96 (update_players_file migration)
  - From Codebase Sweep (12 items): NEW-22a to NEW-22l (week_N_points usage)
  - From Weekly Data Analysis (6 items): NEW-25a to NEW-25f (method analysis) - ✅ ALL RESOLVED
  - From ProjectedPointsManager Migration (10 items): NEW-100 to NEW-109 (consolidate into PlayerManager) - ✅ REVISED
  - From TeamDataManager Migration (8 items): NEW-110 to NEW-117 (D/ST data from CSV to JSON) - 🆕 ADDED
  - From DraftedRosterManager Migration (12 items): NEW-124 to NEW-135 (deprecate fuzzy matching, add PlayerManager methods)
- 📊 Total pending items: ~126 implementation tasks (132 NEW minus 6 resolved weekly data items), ALL DECISIONS RESOLVED
- ✅ **ALL HIGH PRIORITY decisions RESOLVED** (10 major policy decisions complete)
- ✅ **ALL weekly data method analysis RESOLVED** (6 items: NEW-25a through NEW-25f)
- ✅ **ProjectedPointsManager scope decision RESOLVED** (IN SCOPE)

---

## ProjectedPointsManager Migration Analysis (NEW-100 to NEW-109) - REVISED FOR CONSOLIDATION

**Status:** ✅ REVISED - Consolidating into PlayerManager instead of keeping separate class

**See:** PROJECTED_POINTS_MANAGER_ANALYSIS.md for complete details

**Summary:**
- **Current:** ProjectedPointsManager loads players_projected.csv for ORIGINAL pre-season projections
- **Used by:** player_scoring.py for performance deviation calculations (actual vs original projection)
- **Discovery:** PlayerManager already loads projected_points arrays from JSON - no need for separate class!
- **Migration scope:** 2 files (PlayerManager.py, player_scoring.py), 10 items, VERY LOW RISK
- **Strategy:** ✅ Add 3 projection accessor methods to PlayerManager, deprecate ProjectedPointsManager entirely
- **Interface:** Minor change (player_scoring.py uses player_manager methods instead)
- **Impact:** Eliminates ~200 lines of code (entire ProjectedPointsManager class becomes obsolete)

**Implementation Phases:**
1. **Add Methods to PlayerManager (3 items: NEW-100 to NEW-102)** - Add projection accessors
2. **Update Callers (2 items: NEW-103 to NEW-104)** - Remove ProjectedPointsManager, update player_scoring
3. **Deprecate Old Code (1 item: NEW-105)** - Mark ProjectedPointsManager as deprecated
4. **Testing (3 items: NEW-106 to NEW-108)** - Test new methods, verify scoring
5. **Cleanup (1 item: NEW-109)** - Deprecate players_projected.csv

**Key Decisions:**
- ✅ **CONSOLIDATE** into PlayerManager (eliminates duplicate data loading)
- ✅ PlayerManager already has all projected_points data (no new loading needed)
- ✅ Treat 0.0 in array as None (bye weeks)
- ✅ Keep players_projected.csv temporarily for validation

**Risk Assessment:** VERY LOW
- Simple delegation to existing projected_points arrays
- No new data loading logic
- Only 1 caller to update
- Reduces complexity significantly
- Comprehensive testing plan

---

### Phase 1: Add Methods to PlayerManager (3 items)

- [ ] **NEW-100: Add get_projected_points() method to PlayerManager**
  - **Purpose:** Get original projected points for specific player/week
  - **Returns:** Optional[float] (None for unavailable/bye weeks)
  - **Validates:** Week number (1-17)
  - **Handles:** 0.0 as None (bye weeks)
  - **Uses:** player.projected_points array already loaded from JSON
  - **File:** league_helper/util/PlayerManager.py (~15 lines)

- [ ] **NEW-101: Add get_projected_points_array() method to PlayerManager**
  - **Purpose:** Get projected points for a range of weeks
  - **Returns:** List[Optional[float]] for week range
  - **Delegates:** to get_projected_points() for each week
  - **File:** league_helper/util/PlayerManager.py (~5 lines)

- [ ] **NEW-102: Add get_historical_projected_points() method to PlayerManager**
  - **Purpose:** Get historical projections (weeks 1 to current-1)
  - **Returns:** List[Optional[float]] for past weeks
  - **Delegates:** to get_projected_points_array()
  - **File:** league_helper/util/PlayerManager.py (~5 lines)

### Phase 2: Update Callers (2 items)

- [ ] **NEW-103: Remove ProjectedPointsManager from PlayerManager.__init__()**
  - **Line:** league_helper/util/PlayerManager.py:113
  - **Remove:** `self.projected_points_manager = ProjectedPointsManager(config, data_folder)`
  - **Remove:** Import statement for ProjectedPointsManager
  - **File:** league_helper/util/PlayerManager.py

- [ ] **NEW-104: Update player_scoring.py to use PlayerManager methods**
  - **Line:** league_helper/util/player_scoring.py:235
  - **OLD:** `self.projected_points_manager.get_projected_points(player, week)`
  - **NEW:** `self.player_manager.get_projected_points(player, week)`
  - **File:** league_helper/util/player_scoring.py

### Phase 3: Deprecate Old Code (1 item)

- [ ] **NEW-105: Mark ProjectedPointsManager as deprecated**
  - **File:** league_helper/util/ProjectedPointsManager.py (module docstring)
  - **Action:** Add DEPRECATED notice directing to PlayerManager methods
  - **Keep file:** For potential out-of-scope dependencies
  - **Future:** Remove in separate cleanup

### Phase 4: Testing (3 items)

- [ ] **NEW-106: Add tests for new PlayerManager projection methods**
  - **File:** tests/league_helper/util/test_PlayerManager.py
  - Test get_projected_points() with valid/invalid weeks
  - Test get_projected_points_array() with ranges
  - Test get_historical_projected_points()
  - Test 0.0 handling (bye weeks)

- [ ] **NEW-107: Update player_scoring tests**
  - **File:** tests/league_helper/util/test_player_scoring.py
  - Verify performance multiplier calculations work
  - Verify calls to player_manager.get_projected_points()

- [ ] **NEW-108: Integration test - scoring calculations**
  - **File:** tests/integration/test_league_helper_integration.py
  - Verify performance deviation calculations
  - Verify no regressions in player scoring

### Phase 5: Cleanup (1 item)

- [ ] **NEW-109: Mark players_projected.csv as deprecated**
  - **Action:** Rename to players_projected.csv.OLD or add deprecation comment
  - **Keep temporarily:** For validation during migration
  - **File:** data/players_projected.csv

---

## TeamDataManager D/ST Data Migration (NEW-110 to NEW-117)

**Status:** Analysis complete (NEW-46 RESOLVED), implementation pending

**Summary:**
- **Current:** TeamDataManager._load_dst_player_data() reads from players.csv using week_N_points columns
- **Used by:** PlayerManager.py:206 for D/ST fantasy performance rankings (team quality multiplier)
- **Discovery:** CRITICAL - This method breaks with CSV elimination
- **Migration scope:** 1 file (TeamDataManager.py), 8 items, MEDIUM RISK
- **Strategy:** Update to read D/ST actual_points arrays from dst_data.json
- **Data source:** Use actual_points array (historical data for rolling window calculations)

**Migration Strategy:**
- Read dst_data.json instead of players.csv
- Extract actual_points arrays for each D/ST team
- Maintain existing data structure: {team: [week_1, ..., week_17]}
- No interface changes (self.dst_player_data structure stays the same)

### Phase 1: Update Data Loading (3 items)

- [ ] **NEW-110: Update _load_dst_player_data() to read from JSON**
  - **Current:** Reads players.csv, filters position == 'DST'
  - **Update:** Read dst_data.json, extract actual_points arrays
  - **File:** league_helper/util/TeamDataManager.py:110-165
  - **Data structure:** dst_data.json has {"dst_data": [{team, actual_points, ...}]}

- [ ] **NEW-111: Extract actual_points arrays for each D/ST team**
  - **Purpose:** Build {team: [week_1, ..., week_17]} from actual_points arrays
  - **Source:** Use actual_points array (not projected_points)
  - **Reason:** Rolling window calculations need HISTORICAL data
  - **File:** league_helper/util/TeamDataManager.py

- [ ] **NEW-112: Update error handling for JSON loading**
  - **Handle:** FileNotFoundError if dst_data.json missing
  - **Handle:** JSONDecodeError if file corrupted
  - **Handle:** KeyError if expected structure missing
  - **Maintain:** Same fallback behavior (empty dst_player_data dict)
  - **File:** league_helper/util/TeamDataManager.py

### Phase 2: Update Documentation (2 items)

- [ ] **NEW-113: Update method docstring**
  - **Line:** TeamDataManager.py:111-121
  - **OLD:** "Load D/ST weekly fantasy scores from players.csv"
  - **NEW:** "Load D/ST weekly fantasy scores from dst_data.json"
  - **Update:** Change column references from week_N_points to actual_points array

- [ ] **NEW-114: Update data structure comment**
  - **Line:** TeamDataManager.py:83
  - **Current:** Correct format, just ensure it remains accurate
  - **Verify:** {team: [week_1_points, ..., week_17_points]} still accurate

### Phase 3: Testing (3 items)

- [ ] **NEW-115: Test _load_dst_player_data() with JSON**
  - **File:** tests/league_helper/util/test_TeamDataManager.py
  - Test loading from dst_data.json
  - Verify correct extraction of actual_points arrays
  - Test with multiple D/ST teams
  - Test error handling (missing file, corrupted JSON)

- [ ] **NEW-116: Test D/ST fantasy ranking calculations**
  - **File:** tests/league_helper/util/test_TeamDataManager.py
  - Verify _rank_dst_fantasy() works with JSON-loaded data
  - Test rolling window calculations (lines 248-270)
  - Verify bye week handling (None or 0 values)

- [ ] **NEW-117: Integration test - D/ST team quality**
  - **File:** tests/integration/test_league_helper_integration.py
  - Verify PlayerManager.py:206 gets correct D/ST fantasy ranks
  - Verify D/ST scoring uses correct team quality multiplier
  - Compare results with CSV-based data for validation

**Total:** 8 new checklist items (NEW-110 through NEW-117)

---

## DraftedRosterManager Migration (NEW-124 to NEW-135)

**Status:** Analysis complete (NEW-42 RESOLVED), implementation pending

**See:** DRAFTED_ROSTER_MANAGER_ANALYSIS.md for complete details

**Summary:**
- **Current:** 711-line class with complex fuzzy matching for drafted_data.csv
- **Discovery:** 90% of code (680+ lines) becomes obsolete with JSON drafted_by field
- **Decision:** Add 3 roster organization methods to PlayerManager (instead of new file)
- **Impact:** TradeSimulatorModeManager needs update, DraftedRosterManager deprecated
- **Benefit:** Much simpler code, natural location, no CSV dependency

**Migration Strategy:**
- Add get_players_by_team(), get_all_team_names(), get_team_stats() to PlayerManager
- Update TradeSimulatorModeManager to use PlayerManager methods
- Mark DraftedRosterManager as deprecated (keep for out-of-scope player-data-fetcher)

### Phase 1: Add Methods to PlayerManager (3 items)

- [ ] **NEW-124: Add get_players_by_team() method to PlayerManager**
  - Returns Dict[team_name, List[FantasyPlayer]]
  - Filters players by non-empty drafted_by field
  - Groups players by their fantasy team
  - **File:** league_helper/util/PlayerManager.py (~10 lines)

- [ ] **NEW-125: Add comprehensive docstrings to new PlayerManager methods**
  - Document that this replaces DraftedRosterManager functionality
  - Explain drafted_by field usage
  - Provide usage examples
  - **File:** league_helper/util/PlayerManager.py

- [ ] **NEW-126: Add error handling to new PlayerManager methods**
  - Handle empty player lists
  - Handle None values in drafted_by
  - Log warnings for unexpected states
  - **File:** league_helper/util/PlayerManager.py

### Phase 2: Update Trade Simulator (3 items)

- [ ] **NEW-127: Remove DraftedRosterManager import from TradeSimulatorModeManager**
  - **Line:** trade_simulator_mode/TradeSimulatorModeManager.py:45
  - **OLD:** from utils.DraftedRosterManager import DraftedRosterManager
  - **NEW:** No new import needed (already has PlayerManager)

- [ ] **NEW-128: Simplify _initialize_team_data() method**
  - **Lines:** trade_simulator_mode/TradeSimulatorModeManager.py:209-219
  - **OLD:** Create DraftedRosterManager, load CSV, call get_players_by_team()
  - **NEW:** Call self.player_manager.get_players_by_team() directly
  - **Remove:** Lines about loading drafted_data.csv and DraftedRosterManager instantiation

- [ ] **NEW-129: Update docstrings in TradeSimulatorModeManager**
  - **Lines:** trade_simulator_mode/TradeSimulatorModeManager.py:178-190
  - **OLD:** References loading drafted_data.csv and fuzzy matching
  - **NEW:** Explain using drafted_by field from JSON data via PlayerManager

### Phase 3: Deprecate Old Code (2 items)

- [ ] **NEW-130: Add deprecation warning to DraftedRosterManager**
  - **File:** utils/DraftedRosterManager.py:1-20 (module docstring)
  - **Action:** Add DEPRECATED notice with migration instructions
  - **Keep file:** For player-data-fetcher compatibility (out of scope)
  - **Future:** Remove in separate cleanup feature

- [ ] **NEW-131: Add deprecation warnings to DraftedRosterManager methods**
  - **Methods:** __init__, load_drafted_data, apply_drafted_state_to_players
  - **Action:** Log warnings directing users to PlayerManager methods
  - **File:** utils/DraftedRosterManager.py

### Phase 4: Testing (4 items)

- [ ] **NEW-132: Add tests for new PlayerManager roster methods**
  - **File:** tests/league_helper/util/test_PlayerManager.py
  - Test get_players_by_team() with various scenarios
  - Test handling of empty drafted_by values
  - Test with multiple teams and edge cases
  - Verify correct grouping and filtering

- [ ] **NEW-133: Test TradeSimulatorModeManager with new PlayerManager methods**
  - **File:** tests/league_helper/trade_simulator_mode/test_TradeSimulatorModeManager.py
  - Verify _initialize_team_data() works with PlayerManager methods
  - Verify team_rosters populated correctly
  - Verify all team names captured

- [ ] **NEW-134: Integration test - Trade Simulator workflow**
  - **File:** tests/integration/test_league_helper_integration.py
  - Load players from JSON (with drafted_by values)
  - Initialize Trade Simulator
  - Verify team rosters organized correctly via PlayerManager
  - Verify trade analysis works with new approach

- [ ] **NEW-135: Mark DraftedRosterManager tests as deprecated**
  - **File:** tests/utils/test_DraftedRosterManager.py
  - Add deprecation notices
  - Keep tests passing for backward compatibility
  - Document that PlayerManager methods should be used instead
