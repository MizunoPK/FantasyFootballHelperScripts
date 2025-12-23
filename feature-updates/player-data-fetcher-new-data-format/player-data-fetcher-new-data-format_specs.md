# Player Data Fetcher - New Data Format Specification

## Objective

Update the player-data-fetcher to save player data in a new JSON-based format organized by position (QB, RB, WR, TE, K, DST) with enhanced data structures including weekly stat arrays and detailed performance metrics from ESPN API, while maintaining all existing CSV-based functionality.

---

## High-Level Requirements

### 1. File Structure

**Output Location:** `/data/player_data/`

**Files to Generate:**
- `qb_data.json` - All quarterbacks
- `rb_data.json` - All running backs
- `wr_data.json` - All wide receivers
- `te_data.json` - All tight ends
- `k_data.json` - All kickers
- `dst_data.json` - All defense/special teams

**Root Structure:**
Each file contains a single object with a position-keyed array:
```json
{
  "{position}_data": [
    {player1},
    {player2},
    ...
  ]
}
```

**File Management:**
- Files will have static names (not timestamped like CSV exports)
- Each run replaces the previous files (no versioning)
- Folder `/data/player_data/` created automatically if it doesn't exist

### 2. Common Player Fields (All Positions)

Fields present in every player object regardless of position:

| Field | Type | Description | Source | Notes |
|-------|------|-------------|--------|-------|
| `id` | number | ESPN player ID | ESPN API `player.id` | String in model, number in JSON |
| `name` | string | Player full name | ESPN API `fullName` | |
| `team` | string | 3-letter team abbreviation | ESPN API | KC, SF, BUF, etc. |
| `position` | string | Position code | ESPN API | QB, RB, WR, TE, K, DST |
| `injury_status` | string | Current injury status | ESPN API | ACTIVE, QUESTIONABLE, OUT, etc. |
| `drafted_by` | string | Team name or empty string | drafted_data.csv | Via DraftedRosterManager |
| `locked` | boolean | Roster lock status | ESPN API | Convert from 0/1 to false/true |
| `average_draft_position` | number | ADP value | ESPN API | Optional[float] in model |
| `player_rating` | number | 0-100 scale rating | ESPN API | Position-specific normalized ranking |
| `projected_points` | array[number] | Weekly projections | ESPN API statSourceId=1 | 17 elements, index 0 = Week 1 |
| `actual_points` | array[number or null] | Weekly actuals | ESPN API statSourceId=0 | null for unplayed weeks |

**Array Indexing Convention:**
- Index 0 = Week 1
- Index 1 = Week 2
- ...
- Index 16 = Week 17
- All arrays are exactly 17 elements long
- Unplayed/future weeks use `null`
- Bye weeks use `null`

### 3. Position-Specific Stat Fields

All position-specific stats are weekly arrays following the same 17-element convention.

#### QB, RB, WR, TE Stats

**Passing Stats (primarily QB, occasionally RB/WR):**
```json
"passing": {
  "completions": [],    // ESPN stat_1 (weekly)
  "attempts": [],       // ESPN stat_0 (weekly)
  "pass_yds": [],       // ESPN stat_3 (weekly)
  "pass_tds": [],       // ESPN stat_4 (weekly)
  "interceptions": [],  // ESPN stat_14 (weekly)
  "sacks": []           // ESPN stat_64 (passingTimesSacked) - weekly QB sacks taken ✅
}
```

**Rushing Stats (primarily RB, also QB/WR):**
```json
"rushing": {
  "attempts": [],  // ESPN stat_23 (weekly)
  "rush_yds": [],  // ESPN stat_24 (weekly)
  "rush_tds": []   // ESPN stat_25 (weekly)
}
```

**Receiving Stats (WR, TE, RB):**
```json
"recieving": {           // NOTE: Typo preserved from example JSON for compatibility
  "targets": [],         // ESPN stat_58 (weekly)
  "recieving_yds": [],   // ESPN stat_42 (weekly)
  "recieving_tds": [],   // ESPN stat_43 (weekly)
  "receptions": []       // ESPN stat_53 (weekly)
}
```

**Misc Stats:**
```json
"misc": {
  "fumbles": [],   // ESPN stat_72 (70% confidence) - RESEARCH VERIFIED
  "2_pt": [],      // ESPN stat_175 (60% confidence) - RESEARCH VERIFIED
  "ret_yds": [],   // ESPN stat_114 (kickoff) + stat_115 (punt) - VERIFIED ✅
  "ret_tds": []    // ESPN stat_101 (kickoff) + stat_102 (punt) - VERIFIED ✅
}
```

**Research Notes:**
- stat_72 (fumbles): 409 players, typical values 1-2
- stat_175 (2-pt conversions): 338 players, appropriate rarity
- stat_114 (kickoff return yards): 1,043 players, includes RBs/WRs who return kicks
- stat_115 (punt return yards): 869 players, includes WRs like Amon-Ra St. Brown
- stat_101 (kickoff return TDs): 24 players (all D/ST)
- stat_102 (punt return TDs): 22 players (all D/ST)
- **Note:** Return stats combine kickoff + punt returns for total values

#### K (Kicker) Stats

**Extra Points:**
```json
"extra_points": {
  "made": [],    // ESPN stat_86 (weekly) - VERIFIED ✅
  "missed": []   // CALCULATED: stat_87 (attempted) - stat_86 (made)
}
```

**Field Goals:**
```json
"field_goals": {
  "made": [],    // ESPN stat_83 (total FG made, weekly) - VERIFIED ✅
  "missed": []   // ESPN stat_85 (total FG missed, weekly) - VERIFIED ✅
}
```

**Note:** ESPN provides distance-based FG stats (0-39, 40-49, 50+, 60+) but we're using simplified total tracking. Distance breakdowns available as: stat_74-76 (50+), stat_77-79 (40-49), stat_80-82 (0-39), stat_201-203 (60+).

#### DST (Defense/Special Teams) Stats

```json
"defense": {
  "yds_g": [],              // ESPN stat_127 (total yards allowed) - VERIFIED ✅
  "pts_g": [],              // ESPN stat_120 (points allowed) - VERIFIED ✅
  "def_td": [],             // ESPN stat_93 (85% confidence) - RESEARCH VERIFIED
  "sacks": [],              // ESPN stat_112 (weekly) - VERIFIED ✅
  "safety": [],             // ESPN stat_98 (100% confidence) - VERIFIED ✅
  "interceptions": [],      // ESPN stat_95 (weekly) - VERIFIED ✅
  "forced_fumble": [],      // ESPN stat_106 (weekly) - VERIFIED ✅
  "fumbles_recovered": [],  // ESPN stat_99 (weekly) - VERIFIED ✅
  "kickoff_return_td": [],  // ESPN stat_101 (weekly) - VERIFIED ✅
  "punt_return_td": []      // ESPN stat_102 (weekly) - VERIFIED ✅
}
```

**Research Notes:**
- stat_93 (defensive TDs): 14 players (all D/ST), very rare
- stat_98 (safeties): 26 players (all D/ST), appropriate rarity
- stat_101 (kickoff return TDs): 24 players (all D/ST)
- stat_102 (punt return TDs): 22 players (all D/ST) - Previously misidentified as safeties!
- **ALL 10 defense stats now identified!**

### 4. Data Transformations from Current Format

| Current Source | New JSON Format | Transformation Logic |
|---------------|-----------------|---------------------|
| ESPNPlayerData.drafted (0/1/2) | drafted_by (string) | Via DraftedRosterManager: 0→"", 1→"Team Name", 2→MY_TEAM_NAME |
| ESPNPlayerData.locked (0/1) | locked (boolean) | 0 → false, 1 → true |
| ESPNPlayerData.week_N_points | actual_points array | Collect weeks 1-17, use null for unplayed |
| ESPNPlayerData.projected_weeks dict | projected_points array | Collect projection-only values (statSourceId=1) |
| player_info['stats'][week]['stats'] | Position-specific stat arrays | Extract stat_0, stat_1, etc. per week (NEW!) |

**Key Transformation:**
- Current code does NOT extract raw stats (stat_0, stat_23, etc.)
- Only extracts `appliedTotal` (fantasy points)
- **NEED TO ADD:** Raw stats extraction from ESPN API response

### 5. Configuration Toggle

**Config Parameter:**
- **Name:** `CREATE_JSON_PLAYER_DATA` (follows CREATE_CSV, CREATE_JSON pattern)
- **Location:** `player-data-fetcher/config.py` (line 28-30 area)
- **Type:** `bool`
- **Default:** `True` ✅ **USER DECISION: Enable by default for immediate use**

**Usage Pattern:**
```python
# In config.py
CREATE_JSON_PLAYER_DATA = True  # Enable/disable JSON player data generation

# In player_data_fetcher_main.py (NFLProjectionsCollector.export_data)
if CREATE_JSON_PLAYER_DATA:
    player_data_files = await self.exporter.export_json_player_data(data)
    output_files.extend(player_data_files)
```

### 6. Backward Compatibility

**Critical:** All existing player-data-fetcher functionality MUST remain unchanged:
- ✅ Continue generating `players.csv`
- ✅ Continue generating `players_projected.csv`
- ✅ Continue using `drafted_data.csv` as input
- ✅ New JSON files are additive, not replacements
- ✅ Existing CSV exports unaffected by new feature

---

## Dependency Map

### Module Dependencies

```
┌─────────────────────────────────────────────────────────────────────┐
│ run_player_fetcher.py (entry point)                                 │
│     │                                                                │
│     ▼                                                                │
│ NFLProjectionsCollector (player_data_fetcher_main.py)               │
│     │                                                                │
│     ├──► ESPNClient (espn_client.py)                                │
│     │         ├──► HTTP requests to ESPN API                        │
│     │         └──► Returns: List[ESPNPlayerData]                    │
│     │                   ├─► player.id, name, team, position         │
│     │                   ├─► player.week_N_points (fantasy points)   │
│     │                   ├─► player.projected_weeks dict             │
│     │                   └─► player_info['stats'] (RAW - NEW!)       │
│     │                                                                │
│     ├──► DataExporter (player_data_exporter.py)                     │
│     │         │                                                      │
│     │         ├──► DraftedRosterManager (utils/)                    │
│     │         │         └──► drafted_data.csv (input)               │
│     │         │                   └──► Maps player → team name      │
│     │         │                                                      │
│     │         ├──► export_csv() [EXISTING]                          │
│     │         ├──► export_json() [EXISTING]                         │
│     │         │                                                      │
│     │         └──► export_json_player_data() [NEW]                  │
│     │                   │                                            │
│     │                   ├──► _extract_weekly_stats() [NEW]          │
│     │                   │         └──► Parses player_info['stats']  │
│     │                   │                   └──► Returns weekly     │
│     │                   │                         stat arrays       │
│     │                   │                                            │
│     │                   ├──► _build_position_json() [NEW]           │
│     │                   │         └──► Formats player data          │
│     │                   │               for JSON structure          │
│     │                   │                                            │
│     │                   └──► aiofiles (async file write)            │
│     │                             └──► /data/player_data/           │
│     │                                   ├─► qb_data.json            │
│     │                                   ├─► rb_data.json            │
│     │                                   ├─► wr_data.json            │
│     │                                   ├─► te_data.json            │
│     │                                   ├─► k_data.json             │
│     │                                   └─► dst_data.json           │
│     │                                                                │
│     └──► config.py                                                  │
│               └──► CREATE_JSON_PLAYER_DATA [NEW FLAG]               │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
ESPN API Request (scoringPeriodId=0)
   │
   ▼
ESPNClient.get_season_projections()
   │
   ├─► Fetches player_info dict from ESPN for all 2000 players
   │     └─► Contains: player metadata + stats array (all weeks)
   │
   ▼
List[ESPNPlayerData] created (1 per player)
   │
   ├─► Populated with: id, name, team, position, injury_status,
   │                   fantasy points (week_1_points...week_17_points),
   │                   projected_weeks dict, ADP, rating
   │
   └─► CRITICAL GAP: Raw stats (stat_0, stat_23, etc.) NOT currently stored
       └─► Need to preserve player_info['stats'] for later extraction

   ▼
NFLProjectionsCollector.export_data()
   │
   ├─► [EXISTING] export_csv(), export_json(), export_excel()
   │
   └─► [NEW] if CREATE_JSON_PLAYER_DATA:
           │
           ▼
       DataExporter.export_json_player_data(ProjectionData)
           │
           ├─► Step 1: Group players by position
           │     └─► {QB: [...], RB: [...], WR: [...], TE: [...], K: [...], DST: [...]}
           │
           ├─► Step 2: For each player, extract weekly stats
           │     └─► _extract_weekly_stats(player)
           │           └─► REQUIRES: Access to player_info['stats'] from ESPN
           │                 ├─► For each week (1-17):
           │                 │     └─► Extract stats dict where statSourceId=0
           │                 │           └─► {0: attempts, 1: completions, ...}
           │                 └─► Returns: {week_num: {stat_id: value}}
           │
           ├─► Step 3: Apply drafted status
           │     └─► DraftedRosterManager.apply_drafted_state_to_players()
           │           └─► Reads: drafted_data.csv
           │                 └─► Returns: drafted_by field (team name or "")
           │
           ├─► Step 4: Build JSON structure per position
           │     └─► _build_position_json(players, position)
           │           └─► Transforms to complete JSON structure with:
           │                 ├─► Common fields (id, name, team, ...)
           │                 ├─► Weekly arrays (projected_points, actual_points)
           │                 └─► Position-specific stat arrays
           │
           └─► Step 5: Write 6 JSON files concurrently
                 └─► asyncio.gather() for parallel writes (1-2 sec total)
                       └─► Output: /data/player_data/{position}_data.json
```

### Key Integration Points

| Component | Depends On | Used By | Critical Notes |
|-----------|------------|---------|----------------|
| **export_json_player_data()** | ProjectionData, player_info['stats'] | NFLProjectionsCollector | New method in DataExporter |
| **_extract_weekly_stats()** | player_info['stats'] array | export_json_player_data() | **REQUIRES raw ESPN stats access (not currently available)** |
| **DraftedRosterManager** | drafted_data.csv | DataExporter (existing) | Already integrated, reuse |
| **CREATE_JSON_PLAYER_DATA** | None | NFLProjectionsCollector.export_data() | New config flag |
| **/data/player_data/ folder** | None | export_json_player_data() | Auto-created if missing |

### CRITICAL DISCOVERY: Raw Stats Access Gap

**Current State:**
- ESPNClient fetches `player_info` dict from ESPN API
- `_extract_raw_espn_week_points()` only extracts `appliedTotal` (fantasy points)
- Raw stats dict (`player_info['stats'][week]['stats']`) containing stat_0, stat_1, etc. is **NOT currently stored or exposed**

**Problem:**
- To populate position-specific stat arrays, we need access to raw stat IDs (stat_0, stat_23, stat_42, etc.)
- Current architecture discards this data after extracting fantasy points

**Solutions:**

| Option | Description | Pros | Cons | Recommendation |
|--------|-------------|------|------|----------------|
| **A** | Store raw stats in ESPNPlayerData | Clean, reusable | Increases model size (+12MB for 2000 players) | ❌ Heavyweight |
| **B** | Return player_info alongside ESPNPlayerData | Parallel data structures | Both structures in memory | ⚠️ Workable but inelegant |
| **C** | Cache player_info in ESPNClient | Access when needed | Tight coupling | ❌ Poor separation |
| **D** | Store weekly stats dict in ESPNPlayerData | Only what's needed | Clean API | ✅ **RECOMMENDED** |

**Recommended Implementation (Option D):**

Add to ESPNPlayerData model:
```python
weekly_raw_stats: Dict[int, Dict[str, float]] = Field(default_factory=dict)
# Structure: {week_num: {stat_id: value}}
# Example: {1: {"0": 34.0, "1": 24.0, "3": 283.0, ...}, 2: {...}, ...}
```

Populate in ESPNClient:
```python
# After extracting fantasy points per week
for week_entry in stats_array:
    week = week_entry['scoringPeriodId']
    if week_entry['statSourceId'] == 0:  # Actual stats only
        player_data.weekly_raw_stats[week] = week_entry.get('stats', {})
```

**Impact:**
- +8MB memory for 2000 players (acceptable)
- Clean API for stat extraction
- No architectural changes needed
- Reusable for future features

---

## Resolved Implementation Details

### Architecture

**Module Organization:**
- **Location:** Extend `DataExporter` class in `player_data_exporter.py`
- **New Methods:**
  - `async def export_json_player_data(data: ProjectionData) -> List[str]`
  - `def _extract_weekly_stats(player: ESPNPlayerData) -> Dict[int, Dict[str, Any]]`
  - `def _build_position_json(players: List[ESPNPlayerData], position: str) -> dict`
  - `async def _write_position_file(position: str, data: dict, output_path: Path) -> str`

**Pattern:** Similar to existing `export_csv()` and `export_json()` methods (lines 93-151)

### File Writing Strategy

**Approach:** Atomic writes (temp file + rename)
- Write to `{position}_data.json.tmp`
- Validate JSON structure
- Rename to `{position}_data.json`
- **Tradeoff:** +300ms overhead vs data integrity (acceptable)

**Parallelization:** Use `asyncio.gather()` to write all 6 files concurrently
- Expected time: ~1-2 seconds for 2000 players

### Data Transformations

**locked field (0/1 → boolean):**
```python
"locked": bool(player.locked)  # 0 → False, 1 → True
```

**drafted_by field (0/1/2 → team name):**
```python
# Via existing DraftedRosterManager
drafted_by = drafted_roster_manager.get_team_for_player(player) or ""
# Returns: "Team Name" or "" (empty string for free agents)
```

**Weekly arrays (week_N_points → array):**
```python
actual_points = [
    player.get_week_points(week) for week in range(1, 18)
]
# Returns: [week1_val, week2_val, ..., null, null] for unplayed weeks
```

**Stat arrays (stat_ID → named arrays):**
```python
# Extract from weekly_raw_stats dict
passing_attempts = [
    player.weekly_raw_stats.get(week, {}).get("0", None)
    for week in range(1, 18)
]
# Returns: [34.0, 25.0, ..., None, None] for weeks with no data
```

### Error Handling

**Missing Stats:**
- Use `None`/`null` for missing weekly stats
- Log warning for unexpected missing data
- Continue processing (don't fail entire export)

**File Write Errors:**
- Catch `PermissionError`, `OSError` specifically
- Log error with full context
- Raise exception to caller (let NFLProjectionsCollector handle)

**Partial Failures:**
- Wrap each position file write in try/except
- If one position fails, continue with others
- Log all failures, return list of successful files

### Performance Considerations

**Memory:**
- Weekly raw stats: +8MB for 2000 players
- JSON generation working set: +10MB
- Total overhead: ~20MB (negligible)

**Time:**
- Stat extraction: ~500ms
- JSON formatting: ~300ms
- File writing (parallel): ~800ms
- **Total: ~1.6 seconds**

**Optimization:**
- Use asyncio for parallel file writes
- Reuse existing DraftedRosterManager instance
- Group players by position first (single pass)

---

## Open Questions (To Be Resolved)

### RESOLVED VIA ESPN API RESEARCH (2025-12-23)

1. ✅ **Kicker Field Goal Distance Stats:** CONFIRMED NOT AVAILABLE
   - ESPN provides only cumulative season totals (stat_85-88, 214-234)
   - **RESOLUTION:** Include structure with empty arrays

2. ✅ **Defense Defensive TDs and Safeties:** FOUND
   - stat_93 (defensive TDs) - 85% confidence, 14 players (all D/ST)
   - stat_102 (safeties) - 75% confidence, 22 players (all D/ST)
   - **RESOLUTION:** Include both stats, fallback to empty arrays if verification fails

3. ✅ **Misc Stats:** PARTIALLY FOUND
   - stat_72 (fumbles) - 70% confidence, 409 players ✅
   - stat_175 (2-pt conversions) - 60% confidence, 338 players ✅
   - stat_64 (QB sacks taken) - 100% confidence via cwendt94/espn-api library, 580 players ✅
   - Return yards/TDs - NOT AVAILABLE (stat_114/118 are likely yardage breakdowns) ❌
   - **RESOLUTION:** Include fumbles, 2-pt, and QB sacks; empty arrays for returns

### ✅ ALL CRITICAL DECISIONS RESOLVED

4. **Default Config Value:** ✅ RESOLVED
   - **USER DECISION:** `CREATE_JSON_PLAYER_DATA = True` (enable by default)

5. **Output File Management:** ✅ RESOLVED
   - **USER DECISION:** Always replace (no timestamping, static filenames)

6. **Raw Stats Storage:** ✅ RESOLVED
   - **DECISION:** Add `weekly_raw_stats: Dict[int, Dict[str, float]]` to ESPNPlayerData model

7. **Bye Week Representation:** ✅ RESOLVED
   - **DECISION:** Use `null` in all arrays (consistent with unplayed weeks)

8. **Example Files:** ✅ RESOLVED
   - **DECISION:** Move to `tests/fixtures/` after development starts

---

## Implementation Notes

### Files to Modify

1. **player-data-fetcher/player_data_models.py** (lines 25-120)
   - Add `weekly_raw_stats: Dict[int, Dict[str, float]]` field to ESPNPlayerData

2. **player-data-fetcher/espn_client.py** (lines 429-556)
   - Modify `_extract_raw_espn_week_points()` to also populate weekly_raw_stats
   - Store stats dict alongside fantasy points extraction

3. **player-data-fetcher/player_data_exporter.py** (lines 34-151)
   - Add `export_json_player_data()` method
   - Add helper methods for stat extraction and JSON building

4. **player-data-fetcher/player_data_fetcher_main.py** (lines 302-370)
   - Call `export_json_player_data()` in `export_data()` when flag enabled

5. **player-data-fetcher/config.py** (lines 27-30)
   - Add `CREATE_JSON_PLAYER_DATA = True` flag

### Files to Create

- **New methods in existing files** (no new files needed)

### Testing Strategy

**Unit Tests:**
- `test_extract_weekly_stats()` - Stat extraction logic
- `test_build_position_json()` - JSON structure formatting
- `test_data_transformations()` - locked/drafted_by conversions
- `test_missing_data_handling()` - null values for missing stats

**Integration Tests:**
- `test_export_json_player_data()` - Full export flow
- `test_parallel_file_writes()` - Concurrent writes
- `test_with_real_espn_data()` - Real API integration

**Validation Tests:**
- `test_json_schema_validation()` - Structure correctness
- `test_consistency_with_csv()` - Compare common fields
- `test_output_file_structure()` - Verify 6 files created

### ESPN API Stat ID Reference

**Passing:** stat_0 (attempts), stat_1 (completions), stat_3 (yards), stat_4 (TDs), stat_14 (INTs), stat_64 (QB sacks taken)
**Rushing:** stat_23 (attempts), stat_24 (yards), stat_25 (TDs)
**Receiving:** stat_53 (receptions), stat_42 (yards), stat_43 (TDs), stat_58 (targets)
**Kicking:** stat_83 (FG made), stat_85 (FG missed), stat_86 (XP made), stat_87 (XP att), stat_88 (XP missed)
**Defense:** stat_93 (def TDs), stat_95 (INTs), stat_98 (safeties), stat_99 (fumbles rec), stat_101 (KR TDs), stat_102 (PR TDs), stat_106 (forced fumbles), stat_112 (sacks), stat_120 (pts allowed), stat_127 (yds allowed)
**Misc:** stat_72 (fumbles), stat_175 (2-pt conversions), stat_114 (KR yards), stat_115 (PR yards), stat_101 (KR TDs), stat_102 (PR TDs)

**Total NEW Stats Found:** 11 stat IDs (stat_64, 72, 93, 98, 101, 102, 114, 115, 175, plus corrected XP stats 86/87/88)

**Documentation:** `/docs/espn/reference/stat_ids.md` (44 previously confirmed)
**Research:** `feature-updates/player-data-fetcher-new-data-format/ESPN_STAT_RESEARCH_FINDINGS.md` (4 new stat IDs identified)

---

## Status: PLANNING - Ready for Phase 3 (User Review)

**Planning Completion:** All codebase research complete, dependency map created, critical decisions identified.

**Next Step:** Present findings to user and get decisions on critical questions before proceeding to development.
