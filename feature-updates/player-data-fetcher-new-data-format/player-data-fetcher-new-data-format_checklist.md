# Player Data Fetcher - New Data Format - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `player-data-fetcher-new-data-format_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [ ] **Config parameter name and location:** Where should the enable/disable toggle be defined?
  - **Pattern exists:** config.py has CREATE_CSV, CREATE_JSON, CREATE_EXCEL flags
  - **Suggested name:** CREATE_JSON_PLAYER_DATA (follows existing naming convention)
  - **Location:** Add to config.py (line 28-30 area)
- [ ] **Default config value:** Should new JSON generation be enabled or disabled by default?
  - **Consideration:** Existing CREATE_JSON defaults to False
  - **Question:** Match that pattern (False) or enable by default (True)?
- [x] **Code organization:** Where should JSON generation logic live?
  - **RESOLVED:** Extend DataExporter class (player_data_exporter.py)
  - **Pattern:** Add new method `async def export_json_player_data(data: ProjectionData)`
  - **Similar to:** `export_json()` (lines 93-124), `export_csv()` (lines 126-151)

---

## API/Data Source Questions

- [x] **ESPN API endpoints for weekly stats:** Which API endpoints provide position-specific weekly stats?
  - **RESOLVED:** Bulk endpoint with scoringPeriodId=0 returns all weeks
  - **URL:** `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/{ppr_id}`
  - **Stats Structure:** `stats` array with entries for each week, stat IDs map to specific stats
  - **Documentation:** /docs/espn/reference/stat_ids.md (44 stat IDs confirmed)
- [x] **ESPN API documentation:** Is there existing documentation?
  - **RESOLVED:** Yes - comprehensive stat_ids.md with 44 confirmed stat IDs
  - **Passing:** stat_0 (attempts), stat_1 (completions), stat_3 (yards), stat_4 (TDs), stat_14 (INTs)
  - **Rushing:** stat_23 (attempts), stat_24 (yards), stat_25 (TDs)
  - **Receiving:** stat_53 (receptions), stat_42 (yards), stat_43 (TDs), stat_58 (targets)
  - **Kicking:** stat_80 (XP made), stat_81 (XP attempted), stat_83 (FG made), stat_84 (FG attempted)
  - **Defense:** stat_95 (INTs), stat_99 (fumbles recovered), stat_106 (forced fumbles), stat_112 (sacks), stat_120 (pts allowed), stat_127 (yds allowed)
- [x] **drafted_data.csv format:** What is the exact format?
  - **RESOLVED:** CSV with format "Player Name POSITION - TEAM,Team Name"
  - **Example:** "Puka Nacua WR - LAR,Nixelodeon"
  - **No header row**
  - **Integration:** DraftedRosterManager handles loading and normalization
- [x] **Player ID source:** Confirm ESPN player ID is used consistently
  - **RESOLVED:** Yes - ESPNPlayerData.id field is string type, sourced from ESPN API
  - **Consistent across:** API fetch, data models, CSV export, team data
- [ ] **Data availability timing:** When does ESPN API make weekly stats available?
  - **Question:** Real-time during games or delayed? (May not matter for our use case)

---

## Output Files Structure

### Common Fields (All Positions)

| Field | Source Known? | Notes |
|-------|---------------|-------|
| `id` | [x] | ESPN API - field is `id` (string) in ESPNPlayerData model |
| `name` | [x] | ESPN API - field is `fullName`, stored as `name` in model |
| `team` | [x] | ESPN API - 3-letter team abbreviation (verified consistent) |
| `position` | [x] | ESPN API - position codes: QB, RB, WR, TE, K, D/ST (DST in our code) |
| `injury_status` | [x] | ESPN API - stored in ESPNPlayerData, default "ACTIVE" |
| `drafted_by` | [x] | Derived from drafted_data.csv via DraftedRosterManager |
| `locked` | [x] | ESPN API - currently stored as 0/1, need to convert to boolean |
| `average_draft_position` | [x] | ESPN API - field exists in ESPNPlayerData as Optional[float] |
| `player_rating` | [x] | ESPN API - 0-100 scale, field exists in ESPNPlayerData |
| `projected_points` | [x] | Array from ESPNPlayerData.projected_weeks dict (statSourceId=1) |
| `actual_points` | [x] | Array from ESPNPlayerData week_N_points fields (uses actuals when available) |

**Resolved Questions:**
- [x] All fields exist in current ESPN API integration
- [x] Some fields are derived: drafted_by (from CSV), locked (boolean conversion needed)

---

### Position-Specific Stats

#### QB/RB/WR/TE Stats

**Passing Stats:**
| Stat | ESPN API Field | Notes |
|------|----------------|-------|
| `completions` | [x] stat_1 | Weekly array - fetch per week from stats object |
| `attempts` | [x] stat_0 | Weekly array |
| `pass_yds` | [x] stat_3 | Weekly array |
| `pass_tds` | [x] stat_4 | Weekly array |
| `interceptions` | [x] stat_14 | Weekly array |
| `sacks` | [x] stat_64 | QB sacks taken (passingTimesSacked) - 580 players ✅ RESEARCH VERIFIED |

**Rushing Stats:**
| Stat | ESPN API Field | Notes |
|------|----------------|-------|
| `attempts` | [x] stat_23 | Weekly array |
| `rush_yds` | [x] stat_24 | Weekly array |
| `rush_tds` | [x] stat_25 | Weekly array |

**Receiving Stats:**
| Stat | ESPN API Field | Notes |
|------|----------------|-------|
| `targets` | [x] stat_58 | Weekly array |
| `recieving_yds` | [x] stat_42 | Weekly array (note: typo in example JSON - keep for compatibility) |
| `recieving_tds` | [x] stat_43 | Weekly array |
| `receptions` | [x] stat_53 | Weekly array |

**Misc Stats:**
| Stat | ESPN API Field | Notes |
|------|----------------|-------|
| `fumbles` | [x] stat_72 | 409 players, values 1-2 ✅ VERIFIED |
| `2_pt` | [x] stat_175 | 338 players, appropriate rarity ✅ VERIFIED |
| `ret_yds` | [x] stat_114 + stat_115 | Kickoff (stat_114: 1,043 players) + Punt (stat_115: 869 players) ✅ VERIFIED |
| `ret_tds` | [x] stat_101 + stat_102 | Kickoff (stat_101: 24 D/ST) + Punt (stat_102: 22 D/ST) ✅ VERIFIED |

#### K (Kicker) Stats

**Extra Points:**
| Stat | ESPN API Field | Notes |
|------|----------------|-------|
| `made` | [x] stat_86 | Weekly array - VERIFIED ✅ |
| `missed` | [x] CALCULATED | stat_87 (attempted) - stat_86 (made) = missed ✅ |

**Field Goals (Simplified Schema):**
| Stat | ESPN API Field | Notes |
|------|----------------|-------|
| `made` | [x] stat_83 | Total FG made (weekly) - VERIFIED ✅ |
| `missed` | [x] stat_85 | Total FG missed (weekly) - VERIFIED ✅ |

**RESOLVED:** User decision to use simplified FG tracking (total made/missed) rather than distance breakdowns. ESPN provides distance stats (stat_74-82 for 50+, 40-49, 0-39) but simplified schema is cleaner.

#### DST (Defense) Stats

| Stat | ESPN API Field | Notes |
|------|----------------|-------|
| `yds_g` | [x] stat_127 | Total yards allowed (weekly array) ✅ |
| `pts_g` | [x] stat_120 | Points allowed (weekly array) ✅ |
| `def_td` | [x] stat_93 | 14 players (all D/ST), very rare ✅ VERIFIED |
| `sacks` | [x] stat_112 | Sacks (weekly array) ✅ VERIFIED |
| `safety` | [x] stat_98 | 26 players (all D/ST) ✅ VERIFIED |
| `interceptions` | [x] stat_95 | Interceptions (weekly array) ✅ VERIFIED |
| `forced_fumble` | [x] stat_106 | Forced fumbles (weekly array) ✅ VERIFIED |
| `fumbles_recovered` | [x] stat_99 | Fumbles recovered (weekly array) ✅ VERIFIED |
| `kickoff_return_td` | [x] stat_101 | 24 players (all D/ST) ✅ VERIFIED |
| `punt_return_td` | [x] stat_102 | 22 players (all D/ST) ✅ VERIFIED |

**Research Complete:**
- [x] **All 10 defensive stats identified!**
  - stat_93 (defensive TDs): 14 players
  - stat_98 (safeties): 26 players - CORRECTED from stat_102!
  - stat_101 (kickoff return TDs): 24 players
  - stat_102 (punt return TDs): 22 players - Previously misidentified as safeties!

---

## Algorithm/Logic Questions

- [x] **Player filtering criteria:** Include all players or only those meeting certain criteria?
  - **CURRENT BEHAVIOR:** player-data-fetcher fetches 2000 players (ESPN_PLAYER_LIMIT)
  - **DECISION:** Match current CSV behavior - include all fetched players
- [x] **Array length for stats:** Fixed 17-week arrays or dynamic based on current week?
  - **CURRENT BEHAVIOR:** ESPNPlayerData has week_1_points through week_17_points (17 weeks)
  - **DECISION:** Fixed 17-element arrays (index 0 = Week 1, index 16 = Week 17)
- [x] **Null vs 0 for unplayed weeks:** Confirm all stat arrays use null for weeks not yet played
  - **CONFIRMED:** Example JSON files show null for unplayed weeks
  - **PATTERN:** actual_points uses null, projected_points uses values for all weeks
- [ ] **Bye week handling:** How should bye weeks be represented in all arrays?
  - **LIKELY:** null (same as unplayed weeks)
  - **NEEDS CONFIRMATION:** Does ESPN API return stats for bye weeks or skip them?
- [x] **Mid-season player additions:** How to handle players added to ESPN mid-season?
  - **PATTERN:** Use null for weeks before player was added (consistent with unplayed weeks)
- [x] **Team name lookup:** Exact logic for mapping drafted_data.csv to team names
  - **RESOLVED:** DraftedRosterManager.apply_drafted_state_to_players() handles this
  - **Returns:** Team name string from CSV, or empty string "" for free agents
  - **Mapping:** Draft status 0→"", 1→"Team Name", 2→MY_TEAM_NAME
- [x] **Free agent detection:** How to detect if player is free agent vs owned?
  - **RESOLVED:** DraftedRosterManager returns empty string "" for free agents
  - **Logic:** If player not found in drafted_data.csv → drafted_by = ""

---

## Architecture Questions

- [x] **Module structure:** New dedicated module, extend existing, or separate formatter class?
  - **RESOLVED:** Extend DataExporter class with new method
  - **Method:** `async def export_json_player_data(data: ProjectionData) -> List[str]`
  - **Returns:** List of created file paths (6 files for 6 positions)
- [x] **Code reuse:** Which existing ESPN API fetching code can be reused?
  - **REUSE:** All ESPN API fetching (no new endpoints needed)
  - **REUSE:** DraftedRosterManager for drafted_by field
  - **REUSE:** ESPNPlayerData model already has all needed data
  - **NEW:** Stat extraction from ESPN stats array (need to fetch raw stats per week)
- [ ] **File writing:** Atomic writes (temp + rename) or direct writes?
  - **CURRENT PATTERN:** DataFileManager uses direct async writes with aiofiles
  - **QUESTION:** Match existing pattern (direct write) or use atomic writes for safety?
- [x] **Folder creation:** Should code create `/data/player_data/` if it doesn't exist?
  - **RESOLVED:** Yes - DataExporter.__init__ uses `output_dir.mkdir(exist_ok=True, parents=True)`
  - **Pattern:** Create folder if missing, no error if exists
- [x] **Error handling:** How to handle API failures, missing data, or incomplete stats?
  - **CURRENT PATTERN:** Log errors, skip invalid data, continue processing
  - **APPROACH:** Match existing error handling in _populate_weekly_projections()
  - **Specifics:** Use None/null for missing stats, log warnings for unexpected data
- [x] **Logging:** What should be logged during JSON generation?
  - **PATTERN:** Match existing exports (info for start/complete, debug for details)
  - **LOG:** Start message, player counts per position, file paths created, errors/warnings
- [x] **Performance:** Memory usage concerns for large player sets?
  - **ANALYSIS:** 2000 players * 6 files = ~12k player objects in memory (negligible)
  - **NO CONCERN:** Current code handles this size easily

---

## Error Handling Questions

- [x] **Missing API data:** If ESPN API is missing a stat for a week, use null or 0?
  - **DECISION:** Use null (consistent with unplayed weeks)
  - **PATTERN:** actual_points array uses null for missing data
- [x] **Missing stat category:** If entire stat category unavailable, skip it or include empty arrays?
  - **DECISION:** Include structure with empty arrays [] (preserves JSON schema consistency)
  - **EXAMPLE:** If no passing stats for RB, include `"passing": {"completions": [], ...}`
- [x] **File write failures:** How to handle disk write errors?
  - **PATTERN:** Match existing export_csv() error handling
  - **APPROACH:** Log error with self.logger.error(), raise exception to caller
  - **Existing exceptions:** PermissionError, OSError handled specifically
- [x] **Invalid data:** How to handle unexpected data types or values from API?
  - **PATTERN:** Match _populate_weekly_projections() validation
  - **APPROACH:** Skip invalid values, use null, log warning
- [x] **Partial failures:** If one position file fails, should others still be generated?
  - **DECISION:** Yes - wrap each position file write in try/except
  - **PATTERN:** Similar to export_all_formats_with_teams() continuing on errors
  - **LOG:** Error for failed file, continue with remaining positions

---

## Edge Cases

- [x] **Bye weeks:** Representation in stat arrays
  - **DECISION:** null (same as unplayed weeks)
- [x] **Injured players:** Special handling for injury status affecting stats?
  - **NO SPECIAL HANDLING:** injury_status field shows status, stats use null if player didn't play
- [x] **Traded players:** If player changes teams mid-season, which team code?
  - **CURRENT BEHAVIOR:** ESPN API returns current team
  - **DECISION:** Use current team (matches CSV behavior)
- [x] **Players with no projections:** Should they be included in output?
  - **DECISION:** Yes - include all players fetched from ESPN API (matches CSV)
- [x] **Duplicate player IDs:** How to handle if ESPN has duplicate IDs?
  - **UNLIKELY:** ESPN player IDs are unique
  - **IF OCCURS:** Take first occurrence, log warning
- [x] **Empty stat arrays:** Is it valid to have all nulls/zeros?
  - **YES:** Valid for players who haven't played or positions without certain stats
  - **EXAMPLE:** Kicker with all null receiving stats is valid
- [x] **Player position changes:** What if ESPN changes a player's position mid-season?
  - **DECISION:** Use current position from ESPN API (determines which file)
  - **EDGE CASE:** Player might move from one JSON file to another in future fetches

---

## Testing & Validation

- [x] **Test data source:** Use historical ESPN API responses, mocked data, or live API?
  - **APPROACH:** Use mocked ESPNPlayerData objects for unit tests
  - **INTEGRATION:** Use real ESPN API for integration tests (if ENABLE flag set)
  - **PATTERN:** Match existing test structure in tests/player-data-fetcher/
- [x] **Output validation approach:** JSON schema validation, spot-checks, or comparison?
  - **MULTI-LEVEL:**
    1. JSON schema validation (structure)
    2. Spot-check against example files
    3. Verify common fields match CSV export
- [ ] **Consistency checks:** How to verify JSON data matches CSV for common fields?
  - **APPROACH:** Create validation test that loads both CSV and JSON, compares:
    - Player counts per position
    - Sample of player IDs, names, teams
    - Weekly projected/actual points arrays
- [x] **Integration testing:** Test with real player-data-fetcher or isolated unit tests?
  - **BOTH:**
    - Unit tests for JSON generation logic (isolated)
    - Integration test with full DataExporter flow
- [ ] **Example files:** Should example JSON files be version controlled?
  - **QUESTION FOR USER:** Keep examples in feature-updates/ or move to tests/fixtures/?
- [x] **Error scenarios:** What failure scenarios need test coverage?
  - **SCENARIOS:**
    - Missing stat data (null handling)
    - Invalid ESPN API response
    - File write permission errors
    - Partial ESPN stats (some weeks missing)
- [x] **Performance testing:** Any benchmarks for generation time?
  - **NO SPECIFIC BENCHMARK:** Expect <5 seconds for 2000 players (similar to CSV)
  - **LOG TIMING:** Add start/end timestamps in logs for monitoring

---

## Configuration Questions

- [ ] **Config parameter name:** Final decision on name
  - **OPTIONS:**
    - `CREATE_JSON_PLAYER_DATA` (explicit, follows naming pattern)
    - `ENABLE_JSON_PLAYER_DATA` (matches ENABLE_* pattern)
    - `CREATE_POSITION_JSON_FILES` (descriptive)
  - **RECOMMENDATION:** `CREATE_JSON_PLAYER_DATA` (consistent with CREATE_CSV, CREATE_JSON, CREATE_EXCEL)
- [x] **Config location:** player-data-fetcher config file or league_config.json?
  - **RESOLVED:** player-data-fetcher/config.py (lines 27-30 area)
  - **REASON:** Output format configuration belongs with other export flags
- [x] **Config validation:** Should invalid config value log warning or raise error?
  - **PATTERN:** Current config uses boolean flags (True/False only)
  - **NO VALIDATION NEEDED:** Python type system ensures boolean
- [ ] **Default value:** Enabled or disabled by default?
  - **OPTIONS:**
    - False (matches CREATE_JSON default, conservative)
    - True (new format is primary goal)
  - **RECOMMENDATION:** False initially for gradual rollout, True after testing
  - **USER DECISION NEEDED**

---

## Integration Questions

- [x] **Execution timing:** When in the player-data-fetcher flow should JSON be generated?
  - **RESOLVED:** In export_data() after ESPN data is collected
  - **LOCATION:** Call from NFLProjectionsCollector.export_data() (lines 302-370)
  - **ORDER:** After CSV/JSON/Excel export, before historical data save
- [x] **Dependency on CSV:** Must CSV files be generated first?
  - **NO:** JSON generation can be independent (uses same ProjectionData)
  - **PARALLEL:** Can run concurrently with CSV export using asyncio tasks
- [x] **drafted_data.csv read:** When/how is drafted_data.csv loaded?
  - **RESOLVED:** DraftedRosterManager loads in DataExporter.__init__ (lines 65-67)
  - **TIMING:** At initialization if LOAD_DRAFTED_DATA_FROM_FILE=True
- [x] **ESPN API calls:** Reuse existing API calls or need additional endpoints?
  - **REUSE:** All data comes from existing get_season_projections() call
  - **NEED TO ADD:** Extract raw stats from player_info['stats'] array (not currently exposed)
- [ ] **Output cleanup:** Should old JSON files be deleted before writing new ones?
  - **CURRENT PATTERN:** DataFileManager keeps N versions, auto-deletes oldest
  - **QUESTION:** Apply same pattern (keep last 5) or always replace 6 position files?
  - **CONSIDERATION:** Position files are static names (qb_data.json), not timestamped

---

## Documentation Questions

- [ ] **User-facing docs:** Does README.md need updates?
  - **YES:** Document new /data/player_data/ folder output
  - **YES:** Explain CREATE_JSON_PLAYER_DATA config flag
  - **YES:** Describe JSON file structure (6 position files)
- [ ] **Developer docs:** Need documentation for JSON schema?
  - **YES:** Create docs/player_data_json_schema.md
  - **INCLUDE:** Field definitions, position-specific stats, example structures
- [ ] **Config documentation:** Where to document the new parameter?
  - **UPDATE:** player-data-fetcher/config.py inline comments
  - **UPDATE:** README.md configuration section
- [ ] **Migration guide:** Need guide for transitioning consumers from CSV to JSON?
  - **OUT OF SCOPE:** This feature only generates files
  - **FUTURE:** Consumer integration features will need migration guides

---

## NEW QUESTIONS: Raw Stats Extraction

- [ ] **How to access raw ESPN stats:** Current code only extracts fantasy points, not individual stats
  - **CURRENT:** ESPNClient._extract_raw_espn_week_points() only gets appliedTotal (fantasy points)
  - **NEEDED:** Extract stats dict from player_info['stats'][week]['stats']
  - **CONTAINS:** stat_0, stat_1, stat_3, ... stat_127 (per ESPN stat_ids.md)
  - **ARCHITECTURE:** Add method to extract and organize stats by week
- [ ] **Stats storage in ESPNPlayerData:** Where to store weekly raw stats?
  - **CURRENT:** ESPNPlayerData only has week_N_points fields (fantasy points)
  - **OPTIONS:**
    1. Add weekly_stats: Dict[int, Dict[str, float]] field
    2. Add position-specific stat fields directly to model
    3. Extract on-demand during JSON generation
  - **CONSIDERATION:** Option 3 keeps model unchanged, processes during export
- [ ] **Missing stats handling:** How to handle when ESPN API doesn't return a stat ID for a week?
  - **OPTIONS:**
    1. Omit from dict (sparse data)
    2. Set to null (explicit missing)
    3. Set to 0 (assume zero)
  - **RECOMMENDATION:** null for consistency with unplayed weeks
- [ ] **Position-specific stat filtering:** Only extract relevant stats per position
  - **EXAMPLE:** Don't extract passing stats for kickers
  - **BENEFIT:** Reduces data size, clearer JSON structure
  - **QUESTION:** Apply filtering or include all stats (even if empty)?

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Player basic info | ESPN API (player_info) | ✅ VERIFIED |
| Weekly fantasy points (actual) | ESPN API (stats array, statSourceId=0) | ✅ VERIFIED |
| Weekly fantasy points (projected) | ESPN API (stats array, statSourceId=1) | ✅ VERIFIED |
| Passing stats (weekly) | ESPN API (stats.stats dict, stat_0, 1, 3, 4, 14, 64) | ✅ VERIFIED (6 of 6) |
| Rushing stats (weekly) | ESPN API (stats.stats dict, stat_23-25) | ✅ VERIFIED (3 of 3) |
| Receiving stats (weekly) | ESPN API (stats.stats dict, stat_42, 43, 53, 58) | ✅ VERIFIED (4 of 4) |
| Kicking stats (weekly) | ESPN API (stats.stats dict, stat_83, 85, 86, 87, 88) | ✅ VERIFIED (5 of 5, simplified schema) |
| Defense stats (weekly) | ESPN API (stats.stats dict, stat_93, 95, 98, 99, 101, 102, 106, 112, 120, 127) | ✅ VERIFIED (10 of 10) |
| Misc stats (weekly) | ESPN API (stat_72, 114, 115, 175, 101, 102) | ✅ VERIFIED (fumbles, 2pt, returns) |
| Team ownership | drafted_data.csv via DraftedRosterManager | ✅ VERIFIED |
| Config toggle | config.py | ✅ LOCATION CONFIRMED |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| ESPN API endpoint for weekly stats | Bulk endpoint with scoringPeriodId=0 | 2025-12-23 |
| ESPN stat IDs documentation | /docs/espn/reference/stat_ids.md exists with 44 confirmed IDs | 2025-12-23 |
| drafted_data.csv format | "Player Name POS - TEAM,Team Name" format confirmed | 2025-12-23 |
| Code organization | Extend DataExporter class with new method | 2025-12-23 |
| File path patterns | Use /data/player_data/{position}_data.json | 2025-12-23 |
| Null vs 0 for unplayed weeks | Use null (confirmed from example files) | 2025-12-23 |
| Array length | Fixed 17-element arrays (weeks 1-17) | 2025-12-23 |
| Free agent detection | drafted_by = "" for free agents | 2025-12-23 |
| Kicker distance FG stats | NOT AVAILABLE per week (cumulative only) - use empty arrays | 2025-12-23 |
| stat_64 (QB sacks taken) | FOUND via cwendt94/espn-api library - passingTimesSacked, 580 players | 2025-12-23 |
| stat_72 (fumbles) | FOUND via ESPN API research - 409 players | 2025-12-23 |
| stat_175 (2-pt conversions) | FOUND via ESPN API research - 338 players | 2025-12-23 |
| stat_93 (defensive TDs) | FOUND via ESPN API research - 14 D/ST players | 2025-12-23 |
| stat_98 (safeties) | FOUND via cwendt94/espn-api library - 26 D/ST players | 2025-12-23 |
| stat_101 (kickoff return TDs) | FOUND via cwendt94/espn-api library - 24 D/ST players | 2025-12-23 |
| stat_102 (punt return TDs) | FOUND via cwendt94/espn-api library - 22 D/ST players (was misidentified as safeties) | 2025-12-23 |
| stat_114 (kickoff return yards) | FOUND via cwendt94/espn-api library - 1,043 players | 2025-12-23 |
| stat_115 (punt return yards) | FOUND via cwendt94/espn-api library - 869 players | 2025-12-23 |
| stat_83/85 (FG made/missed) | FOUND via cwendt94/espn-api library - weekly totals | 2025-12-23 |
| stat_86/87/88 (XP stats) | FOUND via cwendt94/espn-api library - corrected from stat_80/81 | 2025-12-23 |
| Kicker schema simplification | USER DECISION - Use total FG tracking instead of distance breakdown | 2025-12-23 |
| Default config value | USER DECISION - CREATE_JSON_PLAYER_DATA = True (enable by default) | 2025-12-23 |
| Output file management | USER DECISION - Always replace (no timestamping) | 2025-12-23 |
| Raw stats storage | Add weekly_raw_stats dict to ESPNPlayerData model | 2025-12-23 |
| Bye week representation | Use null in all arrays (consistent with unplayed weeks) | 2025-12-23 |

---

## CRITICAL DECISIONS NEEDED FROM USER

### ✅ COMPLETELY RESOLVED VIA ESPN RESEARCH (2025-12-23)

1. **~~Missing Defense Stats~~** - FULLY RESOLVED
   - ✅ Found stat_93 (defensive TDs) - 14 D/ST players
   - ✅ Found stat_98 (safeties) - 26 D/ST players
   - ✅ Found stat_101 (kickoff return TDs) - 24 D/ST players
   - ✅ Found stat_102 (punt return TDs) - 22 D/ST players
   - **DECISION:** All defense stats identified and verified

2. **~~Missing Misc Stats~~** - FULLY RESOLVED
   - ✅ Found stat_64 (QB sacks taken) - 580 players
   - ✅ Found stat_72 (fumbles) - 409 players
   - ✅ Found stat_175 (2-pt conversions) - 338 players
   - ✅ Found stat_114 (kickoff return yards) - 1,043 players
   - ✅ Found stat_115 (punt return yards) - 869 players
   - ✅ Found stat_101/102 (return TDs) - verified
   - **DECISION:** ALL misc stats found and verified!

3. **~~Kicker Field Goal Stats~~** - RESOLVED
   - **USER DECISION:** Use simplified schema with total FG made/missed
   - ✅ stat_83 (FG made), stat_85 (FG missed) - weekly data available
   - ✅ stat_86 (XP made), stat_87 (XP attempted), stat_88 (XP missed)
   - **DECISION:** Simplified kicker schema implemented

### ✅ ALL DECISIONS RESOLVED (2025-12-23)

4. **Default Config Value:** ✅ RESOLVED
   - **USER DECISION:** `CREATE_JSON_PLAYER_DATA = True` (enable by default)

5. **Output File Cleanup:** ✅ RESOLVED
   - **USER DECISION:** Always replace (no timestamping, static filenames)

6. **Raw Stats Storage:** ✅ RESOLVED
   - **DECISION:** Add `weekly_raw_stats: Dict[int, Dict[str, float]]` to ESPNPlayerData model

7. **Bye Week Representation:** ✅ RESOLVED
   - **DECISION:** Use `null` in all arrays (consistent with unplayed weeks)
