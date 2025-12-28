# Integrate New Player Data Into League Helper

## Objective

Replace CSV-based player data loading in the League Helper module with JSON-based data loading from the new position-specific JSON files in /data/player_data/, ensuring all existing functionality continues to work while making additional stats accessible for future features.

---

## High-Level Requirements

### 1. PlayerManager Data Loading

- **Current Behavior:** Loads from players.csv (single file, CSV format)
- **New Behavior:** Load from 6 position-specific JSON files (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json) in /data/player_data/
- **Requirement:** All fields and stats must be read and accessible (even if not currently used)

### 2. Field Mapping Changes

**Drafted Status:**
- OLD: `drafted` column (int: 0 = not drafted, 1 = drafted by opponent, 2 = drafted by user)
- NEW: `drafted_by` column (string: "" = not drafted, opponent team name = opponent drafted, "Sea Sharp" = user drafted)
- **Requirement:** Update logic to use drafted_by field with team name comparison
- **Decision needed:** Keep `drafted` int field and convert, or change FantasyPlayer to use `drafted_by` string?

**Locked Status:**
- OLD: `locked` column (int: 0 = unlocked, 1 = locked)
- NEW: `locked` field (boolean: false = unlocked, true = locked)
- **Requirement:** Update logic to use boolean value instead of integer
- **Decision needed:** Keep `locked` int field and convert, or change FantasyPlayer to use boolean?

**Weekly Points:**
- OLD: Individual columns `week_1_points` through `week_17_points` (17 separate fields)
- NEW: `projected_points` array with 17 elements (also `actual_points` array)
- **Requirement:** Map array to individual week fields
- **Decision needed:** Keep individual week_N_points fields and map from array, or change to array?

### 3. Data Access Consistency

- **Requirement:** League Helper functionality must work exactly as before
- **Requirement:** No changes to user-facing behavior
- **Requirement:** All modes (Add to Roster, Starter Helper, Trade Simulator, Modify Player Data) must continue to work

### 4. drafted_data.csv Elimination

- **Current:** Separate file tracking which team drafted which player
- **New:** Information now in `drafted_by` field within JSON
- **Requirement:** Eliminate dependency on drafted_data.csv
- **Decision needed:** Delete DraftedDataWriter class or update it?

---

## Dependency Map

### Module Dependencies

```
┌──────────────────────────────────────────────────────────────────────────┐
│ run_league_helper.py (entry point)                                      │
│     │                                                                    │
│     ▼                                                                    │
│ LeagueHelperManager                                                      │
│     │                                                                    │
│     ├──► PlayerManager (league_helper/util/)                            │
│     │     │                                                              │
│     │     ├──► ConfigManager (league_config.json)                        │
│     │     ├──► TeamDataManager (team rankings)                           │
│     │     ├──► SeasonScheduleManager (season_schedule.csv)               │
│     │     │                                                              │
│     │     ├──► CURRENT: load_players_from_csv()                          │
│     │     │     └──► data/players.csv                                    │
│     │     │                                                              │
│     │     ├──► NEW: load_players_from_json() ← TO BE IMPLEMENTED        │
│     │     │     ├──► data/player_data/qb_data.json                       │
│     │     │     ├──► data/player_data/rb_data.json                       │
│     │     │     ├──► data/player_data/wr_data.json                       │
│     │     │     ├──► data/player_data/te_data.json                       │
│     │     │     ├──► data/player_data/k_data.json                        │
│     │     │     └──► data/player_data/dst_data.json                      │
│     │     │                                                              │
│     │     ├──► FantasyPlayer (utils/)                                    │
│     │     │     ├──► from_dict() - converts dict to FantasyPlayer        │
│     │     │     ├──► get_weekly_projections() - returns week array       │
│     │     │     └──► get_single_weekly_projection(week) - accesses week  │
│     │     │                                                              │
│     │     ├──► FantasyTeam (roster management)                           │
│     │     │     └──► Sets player.drafted = 0 or 2 when adding/removing   │
│     │     │                                                              │
│     │     └──► update_players_file()                                     │
│     │           └──► CURRENT: writes to data/players.csv                 │
│     │                 NEW: ??? (decision needed - write to JSON or CSV?) │
│     │                                                                    │
│     ├──► AddToRosterModeManager (draft helper)                          │
│     │     └──► Filters players: [p for p in players if p.drafted == 0]  │
│     │                                                                    │
│     ├──► StarterHelperModeManager (roster optimizer)                    │
│     │     └──► Works with team.roster (drafted == 2 players)             │
│     │                                                                    │
│     ├──► TradeSimulatorModeManager (trade evaluator)                    │
│     │     ├──► CURRENT: Loads data/drafted_data.csv                      │
│     │     │     └──► Maps player names to team names                     │
│     │     └──► NEW: Use drafted_by field from PlayerManager             │
│     │                                                                    │
│     └──► ModifyPlayerDataModeManager (data editor)                      │
│           ├──► Sets player.drafted = 0/1/2                               │
│           ├──► CURRENT: Uses DraftedDataWriter                           │
│           │     └──► Writes to data/drafted_data.csv                     │
│           └──► NEW: ??? (decision needed - update drafted_by? write?)   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Input: data/player_data/*.json (6 position files)
   ▼
PlayerManager.load_players_from_json() ← NEW
   ├─ Parse each JSON file
   ├─ Access position key ("qb_data", "rb_data", etc.)
   ├─ Iterate over player array
   │
   ▼
FantasyPlayer.from_dict() or from_json() ← MAY NEED UPDATE
   ├─ Map JSON fields to FantasyPlayer attributes
   ├─ Convert drafted_by (string) → drafted (int) ??? OR keep string
   ├─ Convert locked (boolean) → locked (int) ??? OR keep boolean
   ├─ Convert projected_points[0-16] → week_1_points...week_17_points
   │
   ▼
PlayerManager.players (List[FantasyPlayer])
   ├─ Filter drafted == 2 → team.roster
   ├─ Filter drafted == 0 → available players
   │
   ▼
Four League Helper Modes use players list
   ├─ AddToRosterMode: Recommend from available (drafted == 0)
   ├─ StarterHelperMode: Optimize team roster (drafted == 2)
   ├─ TradeSimulatorMode: Build opponent rosters (drafted == 1, by team)
   └─ ModifyPlayerDataMode: Edit player data, update drafted status
```

### Key Integration Points

| Component | Depends On | Used By | Notes |
|-----------|------------|---------|-------|
| PlayerManager | JSON files, FantasyPlayer | All 4 modes | Core data loading - main focus of changes |
| FantasyPlayer | None | PlayerManager, all modes | May need field changes (drafted, locked, weeks) |
| DraftedDataWriter | drafted_data.csv | ModifyPlayerDataMode, TradeSimulator | May be eliminated |
| drafted_data.csv | None | DraftedDataWriter | To be eliminated |

---

## Codebase Investigation Findings

### JSON File Structure (Verified)

**Location:** `/data/player_data/` (6 files)
**Files:** qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json

**Structure Example (qb_data.json):**
```json
{
  "qb_data": [
    {
      "id": "3918298",
      "name": "Josh Allen",
      "team": "BUF",
      "position": "QB",
      "injury_status": "QUESTIONABLE",
      "drafted_by": "The Injury Report",
      "locked": false,
      "average_draft_position": 170.0,
      "player_rating": 92.92857142857143,
      "projected_points": [23.63, 21.06, ...],  // 17 elements
      "actual_points": [38.76, 11.82, ...],     // 17 elements
      "passing": {
        "completions": [33.0, 14.0, ...],
        "attempts": [46.0, 25.0, ...],
        "pass_yds": [394.0, 148.0, ...],
        "pass_tds": [2.0, 0.0, ...],
        "interceptions": [0.0, 0.0, ...],
        "sacks": [1.0, 1.0, ...]
      },
      "rushing": {
        "attempts": [14.0, 6.0, ...],
        "rush_yds": [30.0, 59.0, ...],
        "rush_tds": [2.0, 2.0, ...]
      }
    },
    // ... more QB players
  ]
}
```

**Key Observations:**
- Wrapped in position key (e.g., "qb_data")
- Players in array
- `id` is string, not int (need conversion)
- `drafted_by` is string with team name or empty ""
- `locked` is boolean (true/false)
- `projected_points` is array[17] (weeks 1-17)
- `actual_points` is also array[17]
- Additional nested stats (passing, rushing, receiving, etc.)

---

## Current CSV Structure (for comparison)

**File:** `/data/players.csv`

**Columns:**
- id (int), name, team, position, bye_week, fantasy_points
- drafted (int: 0/1), locked (int: 0/1)
- average_draft_position, player_rating, injury_status
- week_1_points, week_2_points, ..., week_17_points (17 separate columns)

**Separate File:** `/data/drafted_data.csv`
- Format: "Player Name POSITION - TEAM,Team Name"
- Maps players to teams for drafted == 1 (opponent drafted) tracking

---

## Files Affected (Verified via grep)

### Files Using `drafted` Field (8 files):
1. **PlayerManager.py** (line 329) - Filters `drafted == 2` for team roster
2. **FantasyTeam.py** (lines 192, 204, 247) - Sets `drafted = 0` or `2`
3. **player_search.py** (lines 51, 54, 57) - Filters by `drafted == 0/1/2`
4. **ModifyPlayerDataModeManager.py** (lines 231, 236, 290, 303, 357, 359) - Sets and checks drafted
5. **ReserveAssessmentModeManager.py** (line 170) - Checks `drafted == 0`
6. **AddToRosterModeManager.py** - Uses drafted field
7. **TradeSimulatorModeManager.py** - Loads drafted_data.csv for opponent rosters
8. **FantasyPlayer.py** (__str__ method, lines 389-394) - Display logic

### Files Using `locked` Field (2 files):
1. **FantasyPlayer.py** (line 96 definition, line 397 display) - Uses `locked == 1`
2. (Potentially others - need full grep)

### Files Using `drafted_data.csv` (4 files):
1. **DraftedDataWriter.py** - Entire class manages this file
2. **ModifyPlayerDataModeManager.py** - Uses DraftedDataWriter
3. **TradeSimulatorModeManager.py** (line 206) - Loads file for opponent rosters
4. **SaveCalculatedPointsManager.py** (line 134) - References file

---

## Open Questions (To Be Resolved)

### Critical Architecture Decisions

1. **FantasyPlayer field strategy:** ✅ RESOLVED
   - **DECISION: Hybrid Approach**
     - **Add NEW field:** `drafted_by: str = ""` to preserve team name information
     - **Keep existing field:** `drafted: int = 0` for backwards compatibility
     - **Synchronization:** Keep both fields in sync (when one changes, update the other)
     - **Loading:** Create new `FantasyPlayer.from_json()` method
     - **Writing:** Write `drafted_by` to JSON, ignore `drafted` (calculated on load)
     - **Weekly points:** Keep individual `week_N_points` fields, map from JSON array
     - **Locked field:** Keep as `locked: int`, convert from boolean during load

   **Implementation Details:**
   ```python
   # In FantasyPlayer class, add new field:
   drafted_by: str = ""

   # In from_json() method:
   drafted_by_value = json_data.get("drafted_by", "")
   player.drafted_by = drafted_by_value
   player.drafted = 0 if drafted_by_value == "" else (2 if drafted_by_value == FANTASY_TEAM_NAME else 1)

   # When setting drafted in code:
   player.drafted = 2
   player.drafted_by = FANTASY_TEAM_NAME  # Keep synchronized
   ```

   **Synchronization Strategy:** ✅ RESOLVED - Helper Method with Strict Validation
   ```python
   class FantasyPlayer:
       def set_drafted_status(self, drafted_value: int, team_name: str = "") -> None:
           """
           Set drafted status and team name synchronously.

           Args:
               drafted_value: 0 (not drafted), 1 (opponent), 2 (our team)
               team_name: Team name for drafted_by field (required for drafted_value=1)

           Raises:
               ValueError: If drafted_value not in [0,1,2]
               ValueError: If drafted_value=1 and team_name is empty

           Examples:
               player.set_drafted_status(0)  # Undraft
               player.set_drafted_status(2)  # Draft to our team
               player.set_drafted_status(1, "Fishoutawater")  # Draft to opponent
               player.set_drafted_status(1)  # ERROR - raises ValueError
           """
           # Validate inputs
           if drafted_value not in [0, 1, 2]:
               raise ValueError(f"drafted_value must be 0, 1, or 2, got {drafted_value}")
           if drafted_value == 1 and not team_name:
               raise ValueError("team_name required when drafted_value=1 (opponent drafted)")

           # Set fields synchronously
           self.drafted = drafted_value
           if drafted_value == 0:
               self.drafted_by = ""
           elif drafted_value == 2:
               self.drafted_by = Constants.FANTASY_TEAM_NAME
           else:  # drafted_value == 1
               self.drafted_by = team_name
   ```

   **Direct Assignment Policy:** ✅ RESOLVED - Option C (Read-Only Properties)

   Both `drafted` and `drafted_by` will be read-only properties:
   ```python
   @dataclass
   class FantasyPlayer:
       # Private backing fields
       _drafted: int = field(default=0, init=False, repr=False)
       _drafted_by: str = field(default="", init=False, repr=False)

       @property
       def drafted(self) -> int:
           """Read-only property. Use set_drafted_status() to modify."""
           return self._drafted

       @property
       def drafted_by(self) -> str:
           """Read-only property. Use set_drafted_status() to modify."""
           return self._drafted_by

       def set_drafted_status(self, drafted_value: int, team_name: str = "") -> None:
           """Only way to modify drafted/drafted_by fields."""
           # ... validation and setting logic
           self._drafted = drafted_value  # Set private field
           self._drafted_by = ...  # Set private field
   ```

   **CRITICAL IMPACT:**
   - All code using `player.drafted = X` will break with AttributeError
   - Must update ALL 7+ locations to use `set_drafted_status()` before code works
   - This is a BREAKING CHANGE that requires careful migration

   **Loading from JSON:** ✅ RESOLVED - Option B (Use Helper Method)

   The `from_json()` method will use the public helper to set fields:
   ```python
   @classmethod
   def from_json(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
       """Create FantasyPlayer from JSON dictionary."""
       # Create player with basic fields
       player = cls(
           id=safe_int_conversion(data.get('id'), 0),
           name=str(data.get('name', '')),
           team=str(data.get('team', '')),
           position=str(data.get('position', '')),
           # ... other fields
       )

       # Set drafted status using helper method
       drafted_by_value = data.get("drafted_by", "")
       if drafted_by_value == "":
           player.set_drafted_status(0)
       elif drafted_by_value == Constants.FANTASY_TEAM_NAME:
           player.set_drafted_status(2)
       else:
           player.set_drafted_status(1, drafted_by_value)

       # Set locked (convert boolean to int)
       player._locked = 1 if data.get("locked", False) else 0

       # Map projected_points array to individual week fields
       projected_points = data.get("projected_points", [])
       for i in range(17):
           week_num = i + 1
           setattr(player, f"week_{week_num}_points",
                   projected_points[i] if i < len(projected_points) else None)

       return player
   ```

   **Benefits:**
   - Consistent API (all changes go through helper)
   - Validation ensures data integrity
   - Clean, maintainable code
   - Performance impact negligible (happens once at load)

   **Remaining Questions:**
   - How to handle dataclass compatibility with private fields?
   - Need complete grep for ALL `.drafted = ` assignments (breaking changes)

2. **File update strategy:** ✅ RESOLVED - Option A (Write to JSON)

   **Implementation:**
   - `update_players_file()` will write to JSON files instead of CSV
   - Group players by position (QB, RB, WR, TE, K, DST)
   - Write each position to its respective JSON file
   - Maintain JSON structure with position key wrapper

   ```python
   def update_players_file(self) -> str:
       """Write all players back to position-specific JSON files."""
       # Group by position
       by_position = defaultdict(list)
       for player in self.players:
           by_position[player.position].append(player)

       # Write each position file
       for position, players in by_position.items():
           filename = f"{position.lower()}_data.json"
           filepath = self.data_folder / "player_data" / filename

           json_data = {
               f"{position.lower()}_data": [
                   player.to_json() for player in players
               ]
           }

           with open(filepath, 'w', encoding='utf-8') as f:
               json.dump(json_data, f, indent=2)

       return f"Wrote {len(self.players)} players to JSON files"
   ```

   **Critical Requirements:**
   - Must preserve ALL fields from original JSON (including stats we don't use)
   - Need `FantasyPlayer.to_json()` method that round-trips perfectly
   - Must handle fields that exist in JSON but not in FantasyPlayer class

   **New Questions from This Decision:**
   - How to preserve unknown/unused fields during round-trip?
   - to_json() implementation details
   - Error handling and atomicity (what if write fails partway?)

3. **drafted_data.csv fate:** ✅ RESOLVED
   - **DECISION:** Deprecate and stop writing to it
   - Update TradeSimulator to use `drafted_by` field from JSON
   - DraftedDataWriter class will be deprecated/removed

### Data Mapping Questions

4. **bye_week field:** ⏳ PENDING - Not visible in JSON sample - where is it? In nested object? Separate file?
5. **projected vs actual:** ⏳ PENDING - JSON has both `projected_points` and `actual_points` - which maps to `week_N_points`?
6. **Additional stats:** ⏳ PENDING - Must store passing/rushing/receiving stats to preserve during write (even if not used)
   - Need strategy to preserve these fields for round-trip
   - Options: Store raw JSON dict, add specific fields, or add generic `_extra_data` dict
7. **Empty drafted_by:** ⏳ PENDING - Confirm `drafted_by: ""` means not drafted (vs null or missing field)?

### Implementation Questions

8. **Method naming:** ✅ RESOLVED - Create new `load_players_from_json()` method (rename from load_players_from_csv)
9. **Error handling:** ⏳ PENDING - What if one JSON file is missing? Skip position or error out?
10. **Validation:** ⏳ PENDING - Validate JSON schema or just try/except?
11. **Performance:** ⏳ PENDING - Is loading 6 JSON files slower than 1 CSV? Acceptable?

### New Questions from Decision 1

12. **Synchronization strategy:** ✅ RESOLVED - Option C: Helper method `set_drafted_status(drafted_value, team_name="")`
13. **Helper method details:** ✅ RESOLVED - Strict validation: team_name required for drafted=1, validate drafted_value in [0,1,2]
14. **Direct assignment policy:** ✅ RESOLVED - Option C: Read-only properties, enforce helper method only
15. **Loading from JSON:** ✅ RESOLVED - Option B: Use public helper method `set_drafted_status()` during loading
16. **Consistency validation:** ✅ RESOLVED - Not needed! Read-only properties make inconsistency impossible via public API
19. **Dataclass compatibility:** ⏳ PENDING - How to handle private fields with @dataclass decorator? field(init=False, repr=False)?
17. **Conflict resolution:** ⏳ PENDING - If JSON has both drafted and drafted_by fields that conflict, which wins? (Assume drafted_by is source of truth?)
18. **Files that set drafted:** ⏳ PENDING - Need grep for complete list of `.drafted = ` assignments
    - Known: FantasyTeam.py (3 locations), ModifyPlayerDataMode (4 locations)
    - Need complete inventory
20. **to_json() implementation:** ⏳ PENDING - Now straightforward with all fields in class
    - Serialize all Optional fields (skip if None)
    - Convert week_N_points → projected_points array
    - Convert drafted int → omit (use drafted_by)
    - Convert locked int → boolean
24. **Field inventory:** ⏳ PENDING - Need complete list of all JSON fields across all positions
    - Examine QB, RB, WR, TE, K, DST JSON files
    - Document universal fields vs position-specific fields
25. **Nested dict structure:** ⏳ PENDING - Keep nested (passing.completions) or flatten (passing_completions)?
26. **Position-specific fields:** ⏳ PENDING - How to handle fields only some positions have? All Optional?
21. **Unknown fields preservation:** ✅ RESOLVED - Option C: Add all possible fields to FantasyPlayer

   **Implementation Approach:**
   Add all JSON fields as Optional attributes to FantasyPlayer class:
   ```python
   @dataclass
   class FantasyPlayer:
       # ... existing fields ...

       # Nested stat structures (position-specific)
       passing: Optional[Dict[str, List[float]]] = None      # QB stats
       rushing: Optional[Dict[str, List[float]]] = None      # RB, QB, WR stats
       receiving: Optional[Dict[str, List[float]]] = None    # WR, RB, TE stats
       kicking: Optional[Dict[str, List[float]]] = None      # K stats
       defense: Optional[Dict[str, List[float]]] = None      # DST stats

       # Any other fields discovered in JSON...
   ```

   **Benefits:**
   - Explicit and typed (better IDE support, type checking)
   - Future features can use these stats without refactoring
   - Clear documentation of what data is available
   - No "magic" hidden fields

   **Trade-offs:**
   - Larger class definition
   - Need to inventory all possible fields
   - Position-specific fields will be None for other positions (QB has passing, but RB doesn't)

   **New Questions:**
   - Complete field inventory needed (examine all 6 position JSON files)
   - How to structure nested dicts (keep nested or flatten)?
   - Position-specific field handling
22. **Write atomicity:** ⏳ PENDING - How to handle partial write failures?
    - Write to temp files first, then atomic rename?
    - Backup existing files before write?
23. **Directory creation:** ⏳ PENDING - What if player_data/ directory doesn't exist? Create or error?

---

## Resolved Implementation Details

### PlayerManager Current Loading (Line 137-142)
**Current flow:**
1. PlayerManager.__init__() calls `load_players_from_csv()`
2. load_players_from_csv() opens `self.file_str` (data/players.csv)
3. Uses csv.DictReader to read rows
4. Calls `FantasyPlayer.from_dict(row)` for each row
5. Validates and appends to `self.players` list
6. Calculates `self.max_projection` from fantasy_points
7. Then calls `load_team()` which filters `p.drafted == 2`

### Constants (Verified)
- **FANTASY_TEAM_NAME:** Defined in `league_helper/constants.py` line 19 as `"Sea Sharp"`
- Used to determine if player is on user's team vs opponent

### FantasyPlayer Structure (Verified)
- **Dataclass** with fields as class attributes
- **from_dict() method** (line 141) converts dictionary to FantasyPlayer
- **Weekly points access:**
  - `get_weekly_projections()` returns `[week_1_points, ..., week_17_points]`
  - `get_single_weekly_projection(week_num)` indexes into array
- **Drafted display logic:** Lines 389-394 shows "AVAILABLE" / "DRAFTED" / "ROSTERED"

---

## Implementation Notes (To Be Expanded During Development)

### Files to Modify (Confirmed)
- `league_helper/util/PlayerManager.py` - Main changes (load_players_from_csv → load_players_from_json)
- `utils/FantasyPlayer.py` - Possibly update from_dict or add from_json
- If Option B chosen:
  - All 8 files that use `drafted` field
  - All files that use `locked` field
  - All files that access `week_N_points`

### Files to Potentially Remove
- `league_helper/util/DraftedDataWriter.py` - If eliminating drafted_data.csv
- `data/drafted_data.csv` - If eliminating this file

### Dependencies
- JSON standard library (built-in)
- pathlib.Path (already used)
- Constants.FANTASY_TEAM_NAME (already used)

### Testing Strategy
- Run all unit tests after changes (100% pass required)
- Test all four League Helper modes manually
- Verify player counts match (JSON vs CSV should have same players)
- Verify team roster loads correctly
- Verify drafted/locked status conversions work
- Test error handling (missing files, malformed JSON)

---

## Status: PLANNING (Phase 2 Complete - Ready for Phase 3)

**Next Steps:**
1. Present findings to user
2. Get user decisions on:
   - FantasyPlayer field strategy (Option A or B)
   - File update strategy (A, B, or C)
   - drafted_data.csv fate
   - Answers to data mapping questions
3. Move to Phase 4: Resolve remaining checklist items
