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
| `bye_week` | bye_week (int) | ??? | [ ] NEED TO FIND | Not visible in JSON sample - where is it? |
| `drafted_by` | drafted (0/1/2) | drafted_by (string) | Convert | "" -> 0, !="" && !="Sea Sharp" -> 1, "Sea Sharp" -> 2 |
| `locked` | locked (0/1) | locked (bool) | Convert | false -> 0, true -> 1 |
| `fantasy_points` | fantasy_points (float) | ??? | [ ] Calculated | ROS sum from week_N or projected_points array? |
| `average_draft_position` | average_draft_position | average_draft_position | Direct | Same field name |
| `player_rating` | player_rating | player_rating | Direct | Same field name |
| `week_1_points` through `week_17_points` | week_N_points (17 columns) | projected_points (array) | Map array to individual fields | projected_points[0] -> week_1_points, etc. |
| `injury_status` | injury_status | injury_status | Direct | Same format (ACTIVE, QUESTIONABLE, etc.) |
| (new stats) | N/A | passing, rushing, receiving, etc. | [ ] Store but don't use yet | Nested objects with arrays - need to document structure |

**Questions:**
- [ ] **bye_week source:** Where is bye_week in the JSON? Is it in a nested object or separate file?
- [ ] **projected vs actual:** JSON has both `projected_points` and `actual_points` arrays - which maps to week_N_points?
- [ ] **Additional stats storage:** Do we need to store passing/rushing/receiving/etc stats in FantasyPlayer, or just ignore them?
- [ ] **Empty drafted_by:** Confirm that `drafted_by: ""` (empty string) means not drafted?
- [ ] **Validation:** How to handle malformed JSON or missing required fields?

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

---

**Progress:** 9 items verified, 40+ items pending user decisions and investigation
