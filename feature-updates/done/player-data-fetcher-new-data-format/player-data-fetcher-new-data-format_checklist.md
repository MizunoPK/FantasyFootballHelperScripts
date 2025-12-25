# Player Data Fetcher - New Data Format - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `player-data-fetcher-new-data-format_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

> **CODEBASE VERIFICATION STATUS**: Round 1 complete. Round 2 (Skeptical Re-verification) pending.
> Items marked with resolution log below are candidates for [x] after user review in Phase 4.

---

## General Decisions (ALL RESOLVED ✅)

### Configuration
- [x] **Decision 1 - Config toggle default value:** ✅ RESOLVED - **True (enabled by default)** (see USER_DECISIONS_SUMMARY.md)
- [x] **Config toggle naming:** ✅ RESOLVED - Use `CREATE_POSITION_JSON = True` following existing pattern
- [x] **Backward compatibility:** ✅ RESOLVED - Existing CSV generation remains unchanged, this is purely additive
- [x] **Output folder location:** ✅ RESOLVED - `/data/player_data/` (new folder)
- [x] **File naming convention:** ✅ RESOLVED - `new_{position}_data.json` (e.g., `new_qb_data.json`)

### Data Structure Decisions
- [x] **Decision 2 - Array length (17 vs 18):** ✅ RESOLVED - **17 elements** (Weeks 1-17, fantasy regular season only)
- [x] **Decision 3 - Typo fix - "recieving":** ✅ RESOLVED - **Fix to "receiving"** (correct spelling)
- [x] **Decision 4 - JSON key "2_pt":** ✅ RESOLVED - **Rename to "two_pt"** (conventional naming)
- [x] **Decision 5 - Empty vs zero-filled arrays:** ✅ RESOLVED - **Actual data for past weeks, zeros for future weeks** (missing past data = 0)

### ESPN API Data Decisions
- [x] **Decision 6 - Return yards source (ret_yds):** ✅ RESOLVED - **Remove ret_yds and ret_tds from non-DST positions entirely** (only in DST files)
- [x] **Decision 7 - Field goal distance granularity:** ✅ RESOLVED - **Simplify to just made/missed totals** (no distance breakdown)
- [x] **Decision 8 - Stat arrays for historical weeks:** ✅ RESOLVED - **Use actual stats (statSourceId=0)** for weeks already played
- [x] **Decision 9 - Stat arrays for future weeks:** ✅ RESOLVED - **Use zeros** for future weeks (not projections)
- [x] **Decision 11 - Missing stat handling:** ✅ RESOLVED - **Always use 0** (never null/None)

---

## API/Data Source Questions

### ESPN API Stats (✅ ALL FOUND - Round 2 Research Complete!)
- [x] **Passing stats mapping:** ✅ COMPLETE - stat_1 (completions), stat_0 (attempts), stat_3 (pass_yds), stat_4 (pass_tds), stat_20 (interceptions), stat_64 (sacks)
- [x] **Rushing stats mapping:** ✅ COMPLETE - stat_23 (attempts), stat_24 (rush_yds), stat_25 (rush_tds)
- [x] **Receiving stats mapping:** ✅ COMPLETE - stat_58 (targets), stat_42 (receiving_yds), stat_43 (receiving_tds), stat_53 (receptions)
- [x] **Kicking stats mapping:** ✅ COMPLETE - stat_86-88 (XP made/att/missed), stat_74-82 (FG by distance), stat_201-203 (60+ FGs)
- [x] **Defense stats mapping:** ✅ COMPLETE - stat_127 (yds_g), stat_120 (pts_g), stat_94 (def_td), stat_99 (sacks), stat_98 (safety), stat_95 (interceptions), stat_106 (forced_fumble), stat_96 (fumbles_recovered)
- [x] **Return stats mapping:** ✅ FOUND - stat_114 (kickoff return yds), stat_115 (punt return yds), stat_101 (KR TDs), stat_102 (PR TDs)
- [x] **Misc stats mapping:** ✅ COMPLETE - stat_68 (fumbles), stat_19/26/44/62 (2PT conversions)

### ESPN API Structure
- [x] **RESOLVED from codebase:** ESPN API provides stats array with `statSourceId` to distinguish actual (0) vs projected (1)
- [x] **RESOLVED from codebase:** ESPN API has individual stat IDs that map to specific stats (e.g., passing yards, rushing TDs)
- [x] **Decision 8 - Stat arrays for historical weeks:** ✅ RESOLVED - Extract actual stats from `statSourceId=0` for weeks already played
- [x] **Decision 9 - Stat arrays for future weeks:** ✅ RESOLVED - Use zeros (not projections)

### Data Availability Research Needed
- [x] **Missing documentation:** ✅ COMPLETE - Round 2 research found all missing stats via GitHub + live API queries
- [x] **Stat ID discovery:** ✅ COMPLETE - All 31 stat IDs identified and verified
- [x] **Documentation location:** ✅ RESOLVED - Documented in specs.md and FINAL_STAT_RESEARCH_COMPLETE.md (sufficient for implementation)

---

## Output Files / Data Structures

### Example JSON File Analysis (COMPLETED - Phase 2.1)

All 6 example files read and documented:

**Root Structure** (all positions):
```json
{
    "{position}_data": [array of player objects]
}
```

**Common Player Fields** (all positions):
- `id` (number) - player ID
- `name` (string) - player full name
- `team` (string) - team abbreviation
- `position` (string) - player position
- `injury_status` (string) - injury status
- `drafted_by` (string) - team name owning player (empty string for FA)
- `locked` (boolean) - locked status (true/false)
- `average_draft_position` (number) - ADP value
- `player_rating` (number) - player rating value
- `projected_points` (array[17]) - weekly projected points
- `actual_points` (array[18]) - weekly actual points **NOTE: Example shows 18 elements, not 17**

**Position-Specific Stat Structures:**

**QB, RB, WR, TE** (all have same 4 categories):
```json
"passing": {
    "completions": [],
    "attempts": [],
    "pass_yds": [],
    "pass_tds": [],
    "interceptions": [],
    "sacks": []
},
"rushing": {
    "attempts": [],
    "rush_yds": [],
    "rush_tds": []
},
"recieving": {  // NOTE: Typo in example files
    "targets": [],
    "recieving_yds": [],
    "recieving_tds": [],
    "receptions": []
},
"misc": {
    "fumbles": [],
    "2_pt": [],  // NOTE: JSON key starting with number
    "ret_yds": [],
    "ret_tds": []
}
```

**K (Kicker)**:
```json
"extra_points": {
    "made": [],
    "missed": []
},
"field_goals": {
    "under_19": { "made": [], "missed": [] },
    "under_29": { "made": [], "missed": [] },
    "under_39": { "made": [], "missed": [] },
    "under_49": { "made": [], "missed": [] },
    "over_50": { "made": [], "missed": [] }
}
```

**DST (Defense)**:
```json
"defense": {
    "yds_g": [],
    "pts_g": [],
    "def_td": [],
    "sacks": [],
    "safety": [],
    "interceptions": [],
    "forced_fumble": [],
    "fumbles_recovered": []
}
```

### Critical Discrepancies Found in Example Files (Moved to General Decisions)

All discrepancies moved to "General Decisions > Data Structure Decisions" section above for user resolution.

Additional notes:
- [ ] **Example position typo:** QB example shows `"position": "QA"` instead of "QB" - obvious typo to fix
- [ ] **Trailing zeros in actual_points:** Example shows [18.4, ..., 0, 0] suggesting Week 18 data

### Data Transformation Questions

**drafted_by Mapping:**
- [x] **RESOLVED from codebase:** `drafted_data.csv` format is `{player_name} {position} - {team},{owning_team_name}`
- [x] **RESOLVED from codebase:** `DraftedRosterManager` exists and handles this mapping
- [x] **RESOLVED from codebase (Round 3):** Free agents represented as empty string "" when `drafted=0`
- [x] **RESOLVED from codebase (Round 3):** Player names are normalized and use fuzzy matching (0.75 threshold) - handles case, punctuation, whitespace variations
- [x] **RESOLVED from codebase (Round 3):** MY_TEAM_NAME config determines user's team name for `drafted=2` → `drafted_by="Sea Sharp"`
- [x] **Decision 10 - Team name reverse lookup:** ✅ RESOLVED - Add `get_team_name_for_player()` method to DraftedRosterManager

**locked Transformation:**
- [x] **RESOLVED from codebase:** CSV has 0/1 values in `locked` column
- [x] **RESOLVED from transformation:** Simple mapping: 0→false, 1→true
- [x] **Locked value source:** ✅ RESOLVED - Already available in FantasyPlayer.locked from CSV

**projected_points Array:**
- [x] **RESOLVED from codebase:** Available as `player.week_1_points` through `player.week_17_points` in `ESPNPlayerData`
- [x] **Array population algorithm:** ✅ RESOLVED - Extract from individual week fields into array `[week_1_points, week_2_points, ..., week_17_points]`

**actual_points Array:**
- [x] **Decision 8 - Source of actual points:** ✅ RESOLVED - Use `statSourceId=0` from ESPN API for past weeks
- [x] **Current week detection:** ✅ RESOLVED - Use `CURRENT_NFL_WEEK` constant from config.py
- [x] **Decision 5 - Unplayed weeks:** ✅ RESOLVED - Use 0 for future weeks (week > CURRENT_NFL_WEEK)

**Stat Arrays (passing, rushing, etc.):**
- [x] **Decision 2 - Array length:** ✅ RESOLVED - All stat arrays are 17 elements
- [x] **Decision 9 - Unplayed weeks:** ✅ RESOLVED - Use 0 for future weeks
- [x] **Decision 8 - Past weeks:** ✅ RESOLVED - Extract from ESPN `statSourceId=0` (actual stats)

---

## Algorithm/Logic Questions

### Weekly Array Population

- [x] **RESOLVED from codebase:** ESPNPlayerData has individual week fields (`week_1_points` through `week_17_points`)
- [x] **Pattern identified:** Can extract as array: `[player.week_1_points or 0.0, player.week_2_points or 0.0, ...]`
- [x] **projected_points vs actual_points distinction:** ✅ RESOLVED
  - projected_points = Use week_N_points field (contains projections from ESPN API)
  - actual_points = Use statSourceId=0 for past weeks (week <= CURRENT_NFL_WEEK), 0 for future weeks

### Current Week Detection

- [x] **RESOLVED from config:** `CURRENT_NFL_WEEK` constant in config.py (currently set to 16)
- [x] **Decision 5 - Logic for actual_points:** ✅ RESOLVED - If week <= CURRENT_NFL_WEEK: use actual data, else: use 0
- [x] **Edge case:** ✅ RESOLVED - Assume CURRENT_NFL_WEEK is manually updated at season start, mid-week uses projection (week not yet counted as complete)

### drafted_by Lookup

- [x] **RESOLVED from codebase:** `DraftedRosterManager.apply_drafted_state_to_players()` exists
- [x] **Mapping confirmed:** Sets `player.drafted` field (0=FA, 1=opponent, 2=my_team)
- [x] **RESOLVED from codebase (Round 3):** Team name extraction algorithm documented:
  - drafted=0 → "" (free agent, not in drafted_data.csv)
  - drafted=1 → Opponent team name (need reverse lookup from DraftedRosterManager.drafted_players dict)
  - drafted=2 → MY_TEAM_NAME from config ("Sea Sharp")
- [x] **Decision 10 - Implementation decision:** ✅ RESOLVED - **Add `get_team_name_for_player(player)` method to DraftedRosterManager**

### Stat Extraction from ESPN API

- [x] **Stat ID to field mapping:** ✅ RESOLVED - All mappings documented in specs.md (31 stat IDs)
- [x] **Weekly stat extraction:** ✅ RESOLVED - Extract from ESPN API stats array filtered by week and statSourceId=0
- [x] **Decision 11 - Missing stats handling:** ✅ RESOLVED - Always use 0 (never null)

---

## Architecture Questions

### Code Location

- [x] **RESOLVED from codebase exploration:** Add new method to `DataExporter` class
- [x] **Method name pattern:** `export_position_json_files(data)` - exports all 6 position files
- [x] **Integration point:** Call from `export_all_formats_with_teams()` after existing exports

### Code Structure

- [x] **RESOLVED from patterns:** Create separate method for each position or single method with position parameter?
  - **Recommendation:** Single method `_export_position_json(data, position)` called 6 times (QB, RB, WR, TE, K, DST)
- [x] **File creation:** Use `DataFileManager.save_json_data()` following existing JSON export pattern
- [ ] **Stat extraction helper:** Create `_extract_player_stats(player_data, position)` helper method?

### Data Flow Integration

- [x] **RESOLVED from codebase:** Flow: `NFLProjectionsCollector.export_data()` → `DataExporter.export_all_formats_with_teams()`
- [ ] **Config integration:** Add `create_position_json` parameter to `export_all_formats_with_teams()`
- [ ] **Task orchestration:** Add position JSON exports to asyncio.gather() tasks list

---

## Error Handling Questions

### Missing Data Scenarios

- [ ] **Player has no ESPN data for stat:** Use 0 in stat array
- [ ] **Player missing from drafted_data.csv:** Set `drafted_by` to empty string (treat as FA)
- [ ] **Week has no projection data:** Use 0.0 in projected_points array
- [ ] **Week has no actual data (future week):** Use 0.0 in actual_points array

### Invalid Data Scenarios

- [ ] **Unknown position:** Should player be skipped entirely or logged as warning?
- [ ] **Team abbreviation not in ESPN_TEAM_MAPPINGS:** Use raw team value or skip player?
- [ ] **Invalid array lengths:** Validation error or pad with 0s?

### File System Errors

- [x] **RESOLVED from existing pattern:** DataExporter already handles PermissionError, OSError
- [x] **Error propagation:** Follow existing pattern - log and raise, don't silently fail

---

## Edge Cases

### Player Data Edge Cases

- [ ] **Mid-season trades:** Which team value to use in JSON? (Current team from ESPN API)
- [ ] **Multi-position eligibility:** Example has QB with position "QA" - is this a typo or real case?
- [ ] **Bye week representation:** Are bye weeks represented in actual_points as 0? Or explicitly marked?
- [ ] **Injured reserve weeks:** Should actual_points be 0 or is there a special handling?

### Stat Array Edge Cases

- [ ] **Defensive players at skill positions:** Do RBs ever have defensive stats? Ignore or include?
- [ ] **QBs with receiving stats:** Should receiving stats for QBs be included if they exist?
- [ ] **Missing stat categories for position:** If position typically doesn't have stat, leave category out or include with empty arrays?

### Season Edge Cases

- [ ] **Week 18 handling:** User notes mention 17 weeks, but NFL has 18-week season. Ignore Week 18?
- [ ] **Playoffs:** Are playoff weeks (18+) included or only regular season (1-17)?

---

## Testing & Validation

### Quality Control Requirements (from user notes)

**MANDATORY validation steps:**
1. [ ] **Array length validation:** All arrays must have exactly 17 elements (or 18 if that's confirmed)
2. [ ] **Null value check:** Arrays must NOT contain null values - use 0 for unplayed weeks
3. [ ] **Current week verification:** Cross-reference internet - Week 17 games have not yet started (as of 2025-12-24)
4. [ ] **Data accuracy spot checks:** Check multiple players from every position against internet sources

### Manual Verification Plan

- [ ] **Players per position to verify:** How many? (Suggest: 3-5 per position = 18-30 total)
- [ ] **Fields to verify:** All common fields + position-specific stats for at least one week
- [ ] **Weeks to spot-check:** Week 1 (actual), Week 16 (actual, current), Week 17 (should be 0)
- [ ] **Data sources for verification:** ESPN.com, NFL.com, Pro-Football-Reference.com

### Automated Validation

- [ ] **JSON schema validation:** Create JSON schema for each position file structure
- [ ] **Array length test:** `assert all(len(player['projected_points']) == 17 for player in qb_data)`
- [ ] **Null value test:** `assert all(p not in [None, null] for player in data for arr in arrays for p in arr)`
- [ ] **Data type test:** Verify all fields have correct types (number, string, boolean, array)

### Config Toggle Testing

- [ ] **CREATE_POSITION_JSON=True:** Verify 6 JSON files created in /data/player_data/
- [ ] **CREATE_POSITION_JSON=False:** Verify NO JSON files created in /data/player_data/
- [ ] **CSV generation unaffected:** Verify players.csv still created regardless of toggle

---

## Output Consumer Validation

**CRITICAL:** Verify output folder structure and file format

### Future Consumers (from user notes)

User notes state: "A different feature will involve updating the league helper and simulations to use the new files."

- [ ] **Output folder structure:** Confirm /data/player_data/ is accessible to league_helper and simulation
- [ ] **File naming:** Confirm `new_{position}_data.json` naming expected by future consumers
- [ ] **Field naming conventions:** Verify snake_case naming, typos ("recieving" vs "receiving"), keys starting with numbers

### Roundtrip Testing

- [ ] **Can files be loaded back?** Test: `json.load(open('data/player_data/new_qb_data.json'))`
- [ ] **Schema consistency:** All 6 files follow same pattern for common fields?
- [ ] **Array element types:** All array elements are numbers (float), not strings?

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player ID | ESPN API `player.id` | VERIFIED in codebase |
| Player name | ESPN API `player.name` | VERIFIED in codebase |
| Team | ESPN API `player.proTeam` → ESPN_TEAM_MAPPINGS | VERIFIED in codebase |
| Position | ESPN API `player.defaultPositionId` → ESPN_POSITION_MAPPINGS | VERIFIED in codebase |
| Injury status | ESPN API `player.injuryStatus` | VERIFIED in codebase |
| Drafted by | drafted_data.csv via DraftedRosterManager | VERIFIED in codebase - REVERSE LOOKUP METHOD NEEDED |
| Locked | CSV `locked` column (0/1 → false/true) | VERIFIED in codebase |
| ADP | ESPN API `player.draftRanksByRankType['PPR'].rank` | VERIFIED in codebase |
| Player rating | Calculated from draft rank (normalized 1-100) | VERIFIED in codebase |
| Projected points (array) | ESPNPlayerData.week_N_points fields | VERIFIED in codebase - EXTRACTION NEEDED |
| Actual points (array) | ESPN API statSourceId=0 for past weeks | NEEDS RESEARCH - extraction method TBD |
| Position-specific stats | ESPN API stats array with stat IDs | NEEDS RESEARCH - stat ID mappings TBD |

---

## Resolution Log (Codebase Verification Round 1)

### RESOLVED from Codebase

| Item | Resolution | Source | Category |
|------|------------|--------|----------|
| Config toggle pattern | Use `CREATE_POSITION_JSON = True` following existing pattern | config.py:27-29 | RESOLVED |
| Output folder location | Create `/data/player_data/` new folder | user notes | RESOLVED |
| Export method location | Add to `DataExporter` class | player_data_exporter.py:34 | RESOLVED |
| Integration point | Call from `export_all_formats_with_teams()` | player_data_exporter.py:523 | RESOLVED |
| File naming pattern | Use `new_{position}_data.json` from examples | example files | RESOLVED |
| DataFileManager usage | Use `save_json_data(prefix, data, create_latest)` | exploration report | RESOLVED |
| drafted_data.csv format | `{player_name} {pos} - {team},{owning_team}` | drafted_data.csv:1-20 | RESOLVED |
| DraftedRosterManager exists | Handles drafted state application | player_data_exporter.py:65 | RESOLVED |
| ESPN stat structure | stats array with statSourceId (0=actual, 1=proj) | fantasy_points_calculator.py:135-162 | RESOLVED |
| Weekly points fields | week_1_points through week_17_points in ESPNPlayerData | player_data_models.py:73-99 | RESOLVED |
| Current week detection | CURRENT_NFL_WEEK constant in config.py | config.py:13 | RESOLVED |
| Async export pattern | All exports are async, use asyncio.gather() | player_data_exporter.py:354 | RESOLVED |
| DraftedRosterManager details | 635 lines, fuzzy matching, progressive strategy | utils/DraftedRosterManager.py | ROUND 3 |
| Team name mapping cache | DraftedRosterManager.drafted_players dict (normalized_key → team_name) | utils/DraftedRosterManager.py:62,117 | ROUND 3 |
| MY_TEAM_NAME config | "Sea Sharp" - user's team for drafted=2 identification | config.py:23 | ROUND 3 |
| Position filtering | ESPN position IDs (1=QB, 2=RB, 3=WR, 4=TE, 5=K, 16=DST) | Existing codebase | ROUND 3 |

### USER DECISIONS SUMMARY

**Total decisions needed:** 11

**Configuration (1):**
- Config toggle default value

**Data Structure (4):**
- Array length (17 vs 18)
- Typo fix ("recieving" vs "receiving")
- JSON key naming ("2_pt" vs "two_pt")
- Empty vs zero-filled arrays

**ESPN API Data (4):**
- Return yards source
- Field goal distance granularity
- Stat arrays for historical weeks (actual vs projected)
- Stat arrays for future weeks (projected vs zeros)

**Additional (2):**
- Team name from drafted value mapping
- Missing stat handling (use 0 confirmed, but need to verify)

### ✅ RESEARCH COMPLETE

| Item | Status | Resolution |
|------|--------|------------|
| ESPN stat ID mappings | ✅ COMPLETE | All 31 stat IDs documented in FINAL_STAT_RESEARCH_COMPLETE.md |
| Actual stats extraction | ✅ COMPLETE | Use statSourceId=0 for actual, statSourceId=1 for projected |
| Return yards source | ✅ RESOLVED | Remove ret_yds/ret_tds from non-DST positions entirely |
| FG distance granularity | ✅ RESOLVED | Remove ret_yds/ret_tds from non-DST positions entirely |
| Team name from drafted value | ✅ RESOLVED | Add get_team_name_for_player() method to DraftedRosterManager |
| Missing stat handling | ✅ RESOLVED | Always use 0 (never null) for missing stats |
| Week 18 handling | ✅ RESOLVED | 17 elements only (weeks 1-17, fantasy regular season)

---

## Progress Tracking

**Phase 2 Status:**
- ✅ Step 2.1: Analyze notes thoroughly
- ✅ Step 2.2: Research codebase patterns (Comprehensive Explore agent report)
- ✅ Step 2.3: Populate checklist with questions (Iteration 1 complete)
- ✅ Step 2.3.1: THREE-ITERATION question generation (All iterations complete)
- ✅ Step 2.4: CODEBASE VERIFICATION Round 1 (12 items resolved)
- ✅ Step 2.4: ESPN STAT ID RESEARCH Round 1 & 2 (All 31 stats found)
- ✅ Step 2.4: CODEBASE VERIFICATION Round 3 (drafted_data.csv deep dive - COMPLETE)
- ⏳ Step 2.5-2.10: Remaining Phase 2 steps (dependency map, final spec updates)

**Next Steps:**
- Update README.md with Round 3 findings
- Create dependency map
- Prepare for Phase 3 (Present findings and pause for user decisions)
