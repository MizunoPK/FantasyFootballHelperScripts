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
  - CSV format was hybrid: actual points for played weeks, projected for future weeks
- NEW: TWO separate arrays with 17 elements each
  - `projected_points`: Pre-game ESPN projections for all 17 weeks
  - `actual_points`: Post-game actual results for all 17 weeks
- **✅ DECISION (2025-12-27):** DEPRECATE individual week_N_points fields
  - **Remove:** All 17 `week_N_points` fields from FantasyPlayer
  - **Add:** `projected_points: List[float]` (17 elements, 0-indexed)
  - **Add:** `actual_points: List[float]` (17 elements, 0-indexed)
  - **Rationale:** Clean architecture - separate concerns (projections vs actuals), avoid hybrid data
  - **Impact:** Breaking API change - all code accessing week_N_points must be updated

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
- Additional nested stats (passing, rushing, receiving, misc, etc.)
- **NEW DISCOVERY (2025-12-27):** `bye_week` exists as top-level integer field
- **NEW DISCOVERY (2025-12-27):** `misc` field with nested `fumbles` array (QB/RB/WR/TE only)

### Complete Field Inventory (Research 2025-12-27)

**Universal Fields (All 6 Positions):**
```python
{
    "id": str,                          # Needs conversion to int
    "name": str,
    "team": str,                        # 3-letter abbrev (BUF, KC, etc.)
    "position": str,                    # QB/RB/WR/TE/K/DST
    "bye_week": int,                    # Week number 1-18
    "injury_status": str,               # ACTIVE, QUESTIONABLE, OUT, etc.
    "drafted_by": str,                  # Team name or ""
    "locked": bool,                     # true/false
    "average_draft_position": float,
    "player_rating": float,             # 0-100 scale
    "projected_points": [float] * 17,   # Pre-game projections
    "actual_points": [float] * 17       # Post-game results
}
```

**Position-Specific Nested Stats:**

**QB, RB, WR, TE:**
```python
{
    "passing": {
        "completions": [float] * 17,
        "attempts": [float] * 17,
        "pass_yds": [float] * 17,
        "pass_tds": [float] * 17,
        "interceptions": [float] * 17,
        "sacks": [float] * 17
    },
    "rushing": {
        "attempts": [float] * 17,
        "rush_yds": [float] * 17,
        "rush_tds": [float] * 17
    },
    "receiving": {
        "targets": [float] * 17,
        "receiving_yds": [float] * 17,
        "receiving_tds": [float] * 17,
        "receptions": [float] * 17
    },
    "misc": {
        "fumbles": [float] * 17
    }
}
```

**K (Kicker) Only:**
```python
{
    "extra_points": {
        "made": [float] * 17,
        "missed": [float] * 17
    },
    "field_goals": {
        "made": [float] * 17,
        "missed": [float] * 17
    }
    // No passing/rushing/receiving/misc
}
```

**DST (Defense) Only:**
```python
{
    "defense": {
        "yds_g": [float] * 17,
        "pts_g": [float] * 17,
        "def_td": [float] * 17,
        "sacks": [float] * 17,
        "safety": [float] * 17,
        "interceptions": [float] * 17
    }
    // No passing/rushing/receiving/misc
}
```

**FantasyPlayer Fields to Add:**
```python
@dataclass
class FantasyPlayer:
    # ... existing universal fields ...

    # NEW: Replace week_N_points with arrays
    projected_points: List[float] = field(default_factory=lambda: [0.0] * 17)
    actual_points: List[float] = field(default_factory=lambda: [0.0] * 17)

    # NEW: Position-specific nested stats (all Optional)
    passing: Optional[Dict[str, List[float]]] = None
    rushing: Optional[Dict[str, List[float]]] = None
    receiving: Optional[Dict[str, List[float]]] = None
    misc: Optional[Dict[str, List[float]]] = None
    extra_points: Optional[Dict[str, List[float]]] = None
    field_goals: Optional[Dict[str, List[float]]] = None
    defense: Optional[Dict[str, List[float]]] = None
```

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

## Weekly Data Migration Requirements (Decision 1 - 2025-12-27)

### Overview
User decision: Deprecate individual `week_N_points` fields and use arrays instead. This provides cleaner separation between projected and actual points.

### Breaking Changes

**Fields to Remove from FantasyPlayer:**
- `week_1_points` through `week_17_points` (17 fields)

**Fields to Add to FantasyPlayer:**
- `projected_points: List[float]` - 17-element array (0-indexed, week 1 = index 0)
- `actual_points: List[float]` - 17-element array (0-indexed, week 1 = index 0)

### Methods to Update

**Existing Methods (modify):**
```python
def get_weekly_projections(self) -> List[float]:
    """OLD: return [self.week_1_points, ..., self.week_17_points]"""
    """NEW: return self.projected_points"""
    return self.projected_points

def get_single_weekly_projection(self, week: int) -> Optional[float]:
    """
    Get projected points for specific week (1-indexed).

    Args:
        week: Week number (1-17)

    Returns:
        Projected points for that week, or None if invalid week
    """
    if 1 <= week <= 17:
        return self.projected_points[week - 1]  # Convert to 0-indexed
    return None
```

**New Methods (add):**
```python
def get_weekly_actuals(self) -> List[float]:
    """Return actual points for all 17 weeks."""
    return self.actual_points

def get_single_weekly_actual(self, week: int) -> Optional[float]:
    """
    Get actual points for specific week (1-indexed).

    Args:
        week: Week number (1-17)

    Returns:
        Actual points for that week, or None if invalid week
    """
    if 1 <= week <= 17:
        return self.actual_points[week - 1]
    return None
```

### Code Search Required

**Must find and update all:**
1. Direct field access: `player.week_5_points`
2. Dynamic attribute access: `getattr(player, f"week_{week}_points")`
3. Dictionary access: `player_dict['week_7_points']`
4. Loops building weekly lists: `[player.week_1_points, player.week_2_points, ...]`

**Estimated affected modules:**
- `league_helper/add_to_roster_mode/` - May use weekly projections for ranking
- `league_helper/starter_helper_mode/` - **Definitely** uses weekly projections for optimization
- Any scoring calculation using weekly data

### Loading Logic (from_json)

**Load both arrays directly from JSON:**
```python
@classmethod
def from_json(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
    # ... other fields ...

    # Load arrays directly
    projected_points = data.get('projected_points', [0.0] * 17)
    actual_points = data.get('actual_points', [0.0] * 17)

    # Ensure exactly 17 elements
    if len(projected_points) != 17:
        projected_points = projected_points + [0.0] * (17 - len(projected_points))
    if len(actual_points) != 17:
        actual_points = actual_points + [0.0] * (17 - len(actual_points))

    return cls(
        # ... other fields ...
        projected_points=projected_points,
        actual_points=actual_points
    )
```

### Writing Logic (to_json)

**Write both arrays back to JSON:**
```python
def to_json(self) -> Dict[str, Any]:
    return {
        # ... other fields ...
        "projected_points": self.projected_points,
        "actual_points": self.actual_points
        # Do NOT include week_N_points fields
    }
```

### Backward Compatibility Considerations

**Issue:** Old CSV files still have `week_N_points` columns

**Options:**
1. **Immediate cutover** - from_dict() throws error or returns zeros for week_N_points
2. **Support both** - from_dict() checks for week_N_points OR projected_points
3. **Migration period** - Load week_N_points into projected_points if JSON arrays not present

**Decision needed:** How to handle old CSV format during transition?

---

## Conflict Resolution Policy (Decision 2 - 2025-12-27)

### Overview
If JSON contains BOTH `drafted` (old int) and `drafted_by` (new string) fields with conflicting values, we need a clear policy.

### Decision: drafted_by is Source of Truth

**Policy:** Always use `drafted_by` field, completely ignore `drafted` field if it exists.

**Rationale:**
1. JSON files are generated by player-data-fetcher - new canonical source
2. Current JSON files already only use `drafted_by` (no old `drafted` field)
3. Simplest implementation with fewest edge cases
4. New format should win in migration scenarios
5. If old `drafted` field appears, it's likely stale/incorrect

**Implementation:**
```python
@classmethod
def from_json(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
    # Always use drafted_by, ignore drafted field completely
    drafted_by = data.get('drafted_by', '')

    # Calculate drafted int from drafted_by string
    if drafted_by == "":
        drafted = 0  # Not drafted
    elif drafted_by == FANTASY_TEAM_NAME:  # "Sea Sharp"
        drafted = 2  # On our team
    else:
        drafted = 1  # Drafted by opponent

    # Do NOT check or use data.get('drafted') at all

    return cls(
        # ...
        _drafted=drafted,
        _drafted_by=drafted_by,
        # ...
    )
```

**Edge Cases:**
- If `drafted_by` is missing → Default to "" (not drafted)
- If `drafted_by` has unexpected value → Treat as opponent (drafted=1)
- If old `drafted` field exists → Ignore completely, use only `drafted_by`

**No Validation:** We do NOT validate consistency between fields. New format wins unconditionally.

---

## Team Name Policy - drafted_by Field (Decision 5 - 2025-12-27)

### Overview
The `drafted_by` field contains team names to track which fantasy team drafted each player. Team names change frequently throughout the season.

### Decision: Flexible Team Name Handling (Option C)

**Policy:** Only explicitly track user's team name (FANTASY_TEAM_NAME). Treat any other non-empty string as opponent team.

**Rationale:**
1. **Team names change frequently** - No static list can be maintained
2. **Simplicity** - No validation overhead, no maintenance burden
3. **Flexibility** - Automatically handles team renames, new teams, typos
4. **Sufficient granularity** - We only need to distinguish: not drafted, user's team, opponent's team
5. **Already designed** - This matches the original feature specification

**Implementation:**

```python
# In constants.py (already exists)
FANTASY_TEAM_NAME = "Sea Sharp"

# In from_json() conversion
drafted_by = data.get('drafted_by', '')

if drafted_by == "":
    drafted = 0  # Not drafted
elif drafted_by == FANTASY_TEAM_NAME:  # Exact string match
    drafted = 2  # On our team
else:
    drafted = 1  # Drafted by ANY opponent (any other string)
```

**Key Points:**

1. **No Team Name List:** We do NOT maintain a list of opponent team names
2. **No Validation:** Accept any non-empty string as valid opponent name
3. **Exact Match:** Use exact string comparison for FANTASY_TEAM_NAME
4. **Case Sensitive:** "Sea Sharp" ≠ "sea sharp" ≠ "SEA SHARP"
5. **Whitespace Matters:** "Sea Sharp" ≠ "Sea Sharp " (trailing space)

**Edge Cases:**

| drafted_by Value | Result | drafted Value | Notes |
|-----------------|--------|---------------|-------|
| `""` | Not drafted | 0 | Empty string = available |
| `"Sea Sharp"` | User's team | 2 | Exact match to constant |
| `"The Injury Report"` | Opponent | 1 | Any other string |
| `"Fishoutawater"` | Opponent | 1 | Different opponent |
| `"NEW TEAM NAME 2025"` | Opponent | 1 | Works automatically |
| `"sea sharp"` | Opponent | 1 | ⚠️ Case mismatch = opponent! |
| `"Sea Sharp "` | Opponent | 1 | ⚠️ Trailing space = opponent! |
| `null` (JSON null) | Not drafted | 0 | Treated as empty string |

**Important Warnings:**

⚠️ **Case Sensitivity:** If player-data-fetcher writes "sea sharp" (lowercase), it will be treated as opponent, NOT user's team. Ensure FANTASY_TEAM_NAME matches exactly.

⚠️ **Whitespace:** Extra spaces will cause mismatch. Player-data-fetcher should write exact string.

**Future Considerations:**

- If you need to track WHICH specific opponent drafted a player, the information is preserved in `drafted_by` field
- Can implement opponent-specific features later without code changes
- Can add validation later if data quality becomes an issue

**No Additional Work Required:** This is already the intended behavior. No code changes needed beyond what's already specified.

---

## Locked Field Migration (Decision 3 - 2025-12-27)

### Overview
The `locked` field indicates whether a player is locked in the lineup (cannot be moved/traded). JSON uses boolean, FantasyPlayer currently uses int.

### Decision: Migrate to Boolean AND Standardize Access Pattern

**Policy:** Change `locked` field to boolean AND standardize all code to use `is_locked()` method instead of direct field access.

**Rationale:**
1. **Type consistency:** Matches JSON format exactly (no conversion overhead)
2. **Pythonic:** Booleans are proper type for true/false state
3. **Encapsulation:** Using `is_locked()` method provides better abstraction
4. **Clearer intent:** `if player.is_locked():` vs `if player.locked == 1:`
5. **Maintainability:** Centralizes logic, easier to modify if needed

**Implementation Details:**

**1. FantasyPlayer Field Change:**
```python
@dataclass
class FantasyPlayer:
    # OLD: locked: int = 0
    # NEW:
    locked: bool = False
```

**2. Method Updates:**
```python
def is_locked(self) -> bool:
    # OLD: return self.locked == 1
    # NEW:
    return self.locked

def is_available(self) -> bool:
    # OLD: return self.drafted == 0 and self.locked == 0
    # NEW:
    return self.drafted == 0 and not self.locked

def __str__(self) -> str:
    # OLD: locked_indicator = " [LOCKED]" if self.locked == 1 else ""
    # NEW:
    locked_indicator = " [LOCKED]" if self.is_locked() else ""
```

**3. Loading from JSON:**
```python
@classmethod
def from_json(cls, data: Dict[str, Any]) -> 'FantasyPlayer':
    # Direct assignment - no conversion needed
    locked = data.get('locked', False)

    return cls(
        # ...
        locked=locked,
        # ...
    )
```

**4. Saving to JSON:**
```python
def to_json(self) -> Dict[str, Any]:
    return {
        # ...
        "locked": self.locked,  # No conversion needed
        # ...
    }
```

**5. Code Standardization Pattern:**

All comparisons should use the helper method:
```python
# OLD PATTERN:
if player.locked == 1:
    # ...
if player.locked == 0:
    # ...

# NEW PATTERN:
if player.is_locked():
    # ...
if not player.is_locked():
    # ...
```

All assignments should use boolean values:
```python
# OLD PATTERN:
player.locked = 1
player.locked = 0

# NEW PATTERN:
player.locked = True
player.locked = False
```

**Affected Locations (16 total):**
- **FantasyPlayer.py:** 3 method updates (is_locked, is_available, __str__)
- **PlayerManager.py:** 1 comparison
- **ModifyPlayerDataModeManager.py:** 3 comparisons + 1 assignment
- **trade_analyzer.py:** 4 comparisons + 1 assignment

**Benefits:**
- Simpler JSON loading/saving (no conversion)
- More maintainable (method encapsulation)
- Type-safe (boolean operations)
- Self-documenting code

---

## File Update Strategy - update_players_file() Migration (Decision 4 - 2025-12-27)

### Overview
The `update_players_file()` method persists changes to drafted/locked status back to disk. Currently writes to CSV, needs migration to JSON format.

### Decision: Selective JSON Updates (Modified Option A)

**Policy:** Migrate to JSON with selective field updates - update ONLY `drafted_by` and `locked` fields while preserving all other data.

**Rationale:**
1. **Single source of truth:** JSON files are canonical (generated by player-data-fetcher)
2. **Separation of concerns:** League Helper manages only drafted/locked, player-data-fetcher manages stats/projections
3. **Data safety:** Selective updates prevent accidental data loss
4. **Clean architecture:** No dual sources of truth (CSV vs JSON)

**Current Usage (4 calls):**
- AddToRosterModeManager.py:194 - After drafting a player
- ModifyPlayerDataModeManager.py:250 - After adding player to roster
- ModifyPlayerDataModeManager.py:307 - After dropping player from roster
- ModifyPlayerDataModeManager.py:405 - After toggling locked status

**Purpose:** Immediate persistence (comments say "ensures data saved even if program crashes")

---

### Implementation Approach

**Algorithm:**
```python
def update_players_file(self) -> str:
    """
    Update drafted_by and locked fields in JSON files.

    Reads existing JSON files, updates only drafted_by and locked fields
    for players that exist in self.players, preserves all other data
    (stats, projections, etc.), then writes back to JSON files.

    Returns:
        str: Success message with count of updated files

    Raises:
        FileNotFoundError: If player_data directory doesn't exist
        JSONDecodeError: If JSON file is malformed
        PermissionError: If JSON files are read-only
    """

    # Group players by position
    by_position = {'QB': [], 'RB': [], 'WR': [], 'TE': [], 'K': [], 'DST': []}
    for player in self.players:
        by_position[player.position].append(player)

    updated_count = 0

    for position, position_players in by_position.items():
        if not position_players:
            continue  # Skip positions with no players

        filepath = self.data_folder / "player_data" / f"{position.lower()}_data.json"

        # Read existing JSON
        if not filepath.exists():
            self.logger.warning(f"JSON file not found: {filepath}")
            continue

        # Create backup
        backup_path = str(filepath) + ".bak"
        shutil.copy(filepath, backup_path)

        # Load and parse JSON
        with open(filepath, 'r') as f:
            json_data = json.load(f)

        # Get player array from position key wrapper
        position_key = f"{position.lower()}_data"
        players_array = json_data.get(position_key, [])

        # Build lookup by ID for fast matching
        player_updates = {str(p.id): p for p in position_players}

        # Update only drafted_by and locked fields
        for player_dict in players_array:
            player_id = str(player_dict.get('id', ''))
            if player_id in player_updates:
                updated_player = player_updates[player_id]
                # Update ONLY these two fields
                player_dict['drafted_by'] = updated_player.drafted_by
                player_dict['locked'] = updated_player.locked

        # Write to temp file first (atomic write)
        temp_path = str(filepath) + ".tmp"
        with open(temp_path, 'w') as f:
            json.dump(json_data, f, indent=2)

        # Rename temp to actual (atomic operation)
        os.replace(temp_path, filepath)

        updated_count += 1
        self.logger.info(f"Updated {position} data in {filepath.name}")

    return f"Updated {updated_count} position files"
```

**Key Design Decisions:**

1. **Selective Updates:**
   - Read entire JSON file
   - Update ONLY `drafted_by` and `locked` fields
   - Preserve ALL other fields (projected_points, actual_points, passing, rushing, etc.)

2. **Safety Measures:**
   - Create `.bak` backup before writing
   - Use temp file + atomic rename to prevent corruption
   - Log warnings for missing files

3. **Matching Strategy:**
   - Match players by ID (converted to string for comparison)
   - Skip players not found in JSON (log warning)
   - Don't add new players to JSON (only update existing)

4. **Error Handling:**
   - Continue processing other files if one fails
   - Log errors but don't halt entire operation
   - Backup files allow manual recovery

5. **Performance:**
   - Write all 6 files every time (simpler, more reliable)
   - Could optimize with dirty flags later if needed

---

### Field Mapping for Updates

**drafted → drafted_by conversion:**
```python
# Reading from JSON (in from_json):
drafted_by = data.get('drafted_by', '')
if drafted_by == "":
    drafted = 0
elif drafted_by == FANTASY_TEAM_NAME:
    drafted = 2
else:
    drafted = 1

# Writing to JSON (in update_players_file):
# Use player.drafted_by directly (already set via hybrid approach)
player_dict['drafted_by'] = updated_player.drafted_by
```

**locked conversion:**
```python
# After Decision 3, locked is already boolean in FantasyPlayer
# Direct assignment, no conversion needed
player_dict['locked'] = updated_player.locked  # Already boolean
```

---

### Edge Cases and Handling

| Scenario | Handling |
|----------|----------|
| JSON file missing | Log warning, skip file, continue with others |
| Player not in JSON | Skip player, log warning (don't add to JSON) |
| Malformed JSON | Raise JSONDecodeError, halt operation |
| Write permission denied | Raise PermissionError, halt operation |
| Partial write failure | Backup allows manual recovery |
| player_data/ directory missing | Raise FileNotFoundError (consistent with Decision 5) |

---

### Testing Requirements

**Round-trip Preservation Test:**
```python
# Load JSON
players = load_players_from_json()

# Modify drafted/locked
players[0].drafted_by = "Sea Sharp"
players[0].locked = True

# Save
update_players_file()

# Reload
new_players = load_players_from_json()

# Verify
assert new_players[0].drafted_by == "Sea Sharp"
assert new_players[0].locked == True
assert new_players[0].projected_points == players[0].projected_points  # Unchanged
assert new_players[0].passing == players[0].passing  # Unchanged
# ... verify all stats preserved
```

**Critical:** Must verify NO data loss of stats/projections during round-trip.

---

## Serialization Methods - to_dict() and to_json() (Decision 6 - 2025-12-27)

### Overview
FantasyPlayer needs methods to convert instances to dictionaries for CSV export, JSON writing, and testing.

### Decision: Keep to_dict() Simple, Don't Create to_json()

**Policy:** Use existing `to_dict()` method with `asdict()`, do not create separate `to_json()` method.

**Rationale:**
1. **Decision 4 doesn't need serialization** - update_players_file() reads existing JSON and updates fields directly
2. **Automatic synchronization** - asdict() outputs whatever is in the dataclass, stays in sync automatically
3. **Simple maintenance** - no custom serialization logic to maintain
4. **Sufficient for current uses** - CSV export (player-data-fetcher), tests, debugging
5. **Can add later** - if future features need custom JSON serialization, can add then

**Current Implementation (FantasyPlayer.py:292):**

```python
def to_dict(self) -> Dict[str, Any]:
    """
    Convert FantasyPlayer to dictionary.

    Returns:
        Dictionary representation of the player
    """
    return asdict(self)  # Returns ALL dataclass fields
```

**No Changes Needed** - This method stays exactly as-is.

**Behavior After Field Updates:**

After implementing our field changes, `to_dict()` will automatically output:

```python
{
    'id': 3918298,
    'name': 'Josh Allen',
    'team': 'BUF',
    'position': 'QB',
    'bye_week': 7,
    'drafted': 2,  # Converted from drafted_by during loading
    'drafted_by': 'Sea Sharp',  # NEW field
    'locked': True,  # Changed to boolean
    'fantasy_points': 347.64,  # Calculated from sum(projected_points)
    'average_draft_position': 1.2,
    'player_rating': 95.0,
    # OLD fields REMOVED - no longer in dataclass:
    # 'week_1_points', 'week_2_points', ..., 'week_17_points'
    # NEW fields ADDED:
    'projected_points': [23.63, 21.06, ...],  # 17 elements
    'actual_points': [38.76, 11.82, ...],  # 17 elements
    'injury_status': 'ACTIVE',
    # Nested stats:
    'passing': {'completions': [...], 'attempts': [...], ...},
    'rushing': {'attempts': [...], 'rush_yds': [...], ...},
    'receiving': None,  # QB doesn't have receiving stats
    'misc': {'fumbles': [...]},
    'extra_points': None,  # QB doesn't have kicking stats
    'field_goals': None,
    'defense': None,  # QB doesn't have defensive stats
    # Computed fields (still included):
    'score': 315.5,
    'weighted_projection': 0.92,
    'consistency': 0.85,
    'matchup_score': 8,
    'team_offensive_rank': 1,
    'team_defensive_rank': 5,
}
```

**Usage:**

1. **CSV Export (player-data-fetcher):**
   ```python
   df = pd.DataFrame([player.to_dict() for player in fantasy_players])
   df.to_csv('players.csv')
   ```
   - Will include ALL fields (including computed ones)
   - CSV columns will change after field updates
   - This is acceptable - player-data-fetcher controls CSV format

2. **Testing:**
   ```python
   player_dict = player.to_dict()
   assert player_dict['name'] == 'Josh Allen'
   assert player_dict['projected_points'] == [23.63, 21.06, ...]
   ```

3. **Debugging:**
   ```python
   print(player.to_dict())  # See all fields
   ```

**Why NOT Create to_json():**

The original plan (NEW-95) was to create a `to_json()` method for JSON file writing. However:

1. **Decision 4's implementation doesn't use it:**
   ```python
   # update_players_file() accesses fields directly:
   player_dict['drafted_by'] = updated_player.drafted_by
   player_dict['locked'] = updated_player.locked
   # Does NOT call: player_json = updated_player.to_json()
   ```

2. **No other need identified:**
   - League Helper reads JSON, doesn't create new player entries
   - player-data-fetcher creates the JSON files (separate codebase)
   - Migration scenarios can access fields directly if needed

3. **Can add later if needed:**
   - Not a breaking change to add new method
   - Can implement when actual need arises
   - Avoid premature optimization

**If to_json() is Needed in Future:**

If a future feature needs to create new player JSON entries, implement like this:

```python
def to_json(self) -> Dict[str, Any]:
    """
    Convert to JSON-compatible dictionary for file writing.

    Excludes computed fields that shouldn't be persisted.
    """
    return {
        'id': str(self.id),  # JSON uses string IDs
        'name': self.name,
        'team': self.team,
        'position': self.position,
        'bye_week': self.bye_week,
        'drafted_by': self.drafted_by,
        'locked': self.locked,
        'average_draft_position': self.average_draft_position,
        'player_rating': self.player_rating,
        'projected_points': self.projected_points,
        'actual_points': self.actual_points,
        'injury_status': self.injury_status,
        'passing': self.passing,
        'rushing': self.rushing,
        'receiving': self.receiving,
        'misc': self.misc,
        'extra_points': self.extra_points,
        'field_goals': self.field_goals,
        'defense': self.defense,
        # Note: Excludes score, weighted_projection, consistency, etc.
    }
```

But this is **not needed now** and is **not part of this feature's scope**.

**Summary:**
- ✅ Keep to_dict() as-is (uses asdict)
- ✅ Do NOT create to_json()
- ✅ to_dict() behavior automatically updates when dataclass fields change
- ✅ No code changes required for this decision

---

## Error Handling Policy (Decision 7 - 2025-12-27)

### Overview
Comprehensive error handling strategy for loading player data from JSON files and handling various failure scenarios.

### Decision: Layered Error Handling - Fail Fast for Critical, Graceful for Recoverable

**Philosophy:**
- **Critical errors** (missing files, corrupted data) → Fail fast, alert user immediately
- **Recoverable errors** (missing optional fields, bad individual players) → Continue with warnings
- **Type mismatches** → Attempt conversion, warn on failure

---

### Scenario 1: Missing JSON File

**Policy:** **Fail Fast** - Raise FileNotFoundError

**Implementation:**
```python
def load_players_from_json(self) -> List[FantasyPlayer]:
    """Load players from JSON files."""
    for position in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:
        filepath = self.data_folder / "player_data" / f"{position.lower()}_data.json"

        if not filepath.exists():
            self.logger.error(f"Required JSON file not found: {filepath}")
            raise FileNotFoundError(
                f"Missing required player data file: {filepath}. "
                f"Please run player-data-fetcher to generate data files."
            )

        # Continue loading...
```

**Rationale:**
- Missing files indicate setup problem (player-data-fetcher not run)
- Better to fail clearly than run with incomplete data
- All 6 position files should exist in properly configured system
- Clear error message guides user to solution

**User Experience:**
- League Helper refuses to start
- Error message: "Missing required player data file: qb_data.json. Please run player-data-fetcher..."
- User must fix data source before continuing

---

### Scenario 2: Malformed JSON

**Policy:** **Fail Fast** - Raise JSONDecodeError

**Implementation:**
```python
try:
    with open(filepath, 'r') as f:
        json_data = json.load(f)
except json.JSONDecodeError as e:
    self.logger.error(f"Malformed JSON in {filepath}: {e}")
    raise  # Re-raise original exception
```

**Rationale:**
- Malformed JSON indicates data corruption or system error
- Not a normal condition - should be investigated and fixed
- Continuing with corrupted data is risky
- Original exception provides detailed error location

**User Experience:**
- League Helper refuses to start
- Error shows line/column of JSON syntax error
- User must fix or regenerate corrupted file

---

### Scenario 3: Missing Required Fields

**Policy:** **Skip Player with Warning** - Continue loading other players

**Required Fields:** `id`, `name`, `position`

**Implementation:**
```python
for player_dict in players_array:
    # Validate required fields
    player_id = player_dict.get('id')
    name = player_dict.get('name')
    position = player_dict.get('position')

    if not player_id:
        self.logger.warning(
            f"Player missing required field 'id', skipping: {name or 'Unknown'}"
        )
        continue

    if not name:
        self.logger.warning(
            f"Player missing required field 'name', skipping player ID: {player_id}"
        )
        continue

    if not position:
        self.logger.warning(
            f"Player missing required field 'position', skipping: {name} (ID: {player_id})"
        )
        continue

    # Player has all required fields - create FantasyPlayer
    player = FantasyPlayer.from_json(player_dict)
    players.append(player)
```

**Rationale:**
- Individual player corruption shouldn't break entire load
- Other players are likely valid
- User can still use League Helper with most players
- Warning log allows investigation
- Balance between strictness and usability

**User Experience:**
- League Helper starts successfully
- Most players loaded
- Warning in logs: "Player missing required field 'id', skipping: Josh Allen"
- User can investigate logs if player counts seem low

---

### Scenario 4: Missing Optional Fields

**Policy:** **Use Defaults** - No error, no warning

**Optional Fields:** `bye_week`, `average_draft_position`, `player_rating`, `injury_status`, nested stats, etc.

**Implementation:**
```python
# In FantasyPlayer.from_json()
bye_week = data.get('bye_week', None)  # None is acceptable
average_draft_position = data.get('average_draft_position', None)
player_rating = data.get('player_rating', None)
injury_status = data.get('injury_status', 'UNKNOWN')
projected_points = data.get('projected_points', [0.0] * 17)
actual_points = data.get('actual_points', [0.0] * 17)
passing = data.get('passing', None)
rushing = data.get('rushing', None)
# ... etc
```

**Rationale:**
- Optional fields are expected to sometimes be missing
- Defaults are safe and reasonable
- No need to alert user - normal condition
- from_json() handles gracefully

**No logging or errors** - silent fallback to defaults

---

### Scenario 5: Type Mismatches

**Policy:** **Attempt Conversion** - Convert if possible, warn and use default if not

**Implementation:**
```python
# For locked field (expecting boolean)
locked = data.get('locked', False)
if isinstance(locked, int):
    # Convert int to bool (for backward compatibility)
    locked = bool(locked)
    self.logger.debug(f"Converted locked from int to bool for player {name}")
elif not isinstance(locked, bool):
    self.logger.warning(
        f"Invalid type for 'locked' field: expected bool, got {type(locked).__name__} "
        f"for player {name}. Using default: False"
    )
    locked = False

# For id field (expecting int, might be string in JSON)
player_id = data.get('id', 0)
try:
    player_id = int(player_id)  # Convert string to int if needed
except (ValueError, TypeError):
    self.logger.warning(
        f"Could not convert 'id' to int: {player_id} for player {name}. Skipping player."
    )
    continue  # Skip this player

# For float fields
fantasy_points = safe_float_conversion(data.get('fantasy_points'), default=0.0)
```

**Rationale:**
- JSON format might evolve over time
- player-data-fetcher might have bugs or format variations
- Defensive programming - handle reasonable variations
- Use existing safe_int_conversion and safe_float_conversion helpers
- Log warnings for unexpected types (helps debugging)

**User Experience:**
- System tolerates minor type mismatches
- Debug/warning logs for investigation
- Fallback to safe defaults

---

### Scenario 6: Wrong Array Length

**Policy:** **Pad or Truncate to 17** - Adjust array, log warning

**Arrays:** `projected_points`, `actual_points`

**Implementation:**
```python
projected_points = data.get('projected_points', [])

if len(projected_points) == 0:
    # Empty array - use zeros
    projected_points = [0.0] * 17
    self.logger.warning(f"Empty projected_points array for {name}, using zeros")
elif len(projected_points) < 17:
    # Pad with zeros
    original_length = len(projected_points)
    projected_points.extend([0.0] * (17 - len(projected_points)))
    self.logger.warning(
        f"projected_points array too short for {name}: {original_length} weeks, "
        f"padded to 17 with zeros"
    )
elif len(projected_points) > 17:
    # Truncate to 17
    original_length = len(projected_points)
    projected_points = projected_points[:17]
    self.logger.warning(
        f"projected_points array too long for {name}: {original_length} weeks, "
        f"truncated to 17"
    )

# Same logic for actual_points
```

**Rationale:**
- Code expects exactly 17 weeks (fantasy regular season)
- Padding with zeros is safe default
- Allows system to work even with incomplete/incorrect data
- Warning alerts user to data quality issue
- Better than crashing on length mismatch

**User Experience:**
- System continues to work
- Warning in logs if arrays adjusted
- Can investigate if projections seem off

---

### Scenario 7: Nested Stats Missing or Malformed

**Policy:** **Use None** - Optional fields, safe default

**Implementation:**
```python
# Nested stats are all Optional
passing = data.get('passing', None)
if passing is not None and not isinstance(passing, dict):
    self.logger.warning(f"Invalid type for 'passing': expected dict, got {type(passing)} for {name}")
    passing = None

# No validation of nested structure - just store as-is
# If dict is malformed, future access will handle it gracefully
```

**Rationale:**
- Nested stats are optional (position-specific)
- Not currently used by League Helper
- Preserve for future features
- No need for strict validation

---

### Summary Table

| Error Scenario | Policy | Action | Logging |
|----------------|--------|--------|---------|
| Missing JSON file | **Fail Fast** | Raise FileNotFoundError | Error |
| Malformed JSON | **Fail Fast** | Raise JSONDecodeError | Error |
| Missing required field | **Skip Player** | Continue, skip player | Warning |
| Missing optional field | **Use Default** | Silent fallback | None |
| Type mismatch | **Attempt Conversion** | Convert or default | Warning |
| Wrong array length | **Pad/Truncate** | Adjust to 17 | Warning |
| Malformed nested stats | **Use None** | Set to None | Warning |

---

### Testing Requirements

**Error handling tests needed:**
```python
def test_missing_json_file():
    """Verify FileNotFoundError raised when JSON file missing."""
    # Remove qb_data.json
    # Attempt to load
    # Assert FileNotFoundError raised

def test_malformed_json():
    """Verify JSONDecodeError raised when JSON syntax invalid."""
    # Create file with invalid JSON
    # Attempt to load
    # Assert JSONDecodeError raised

def test_missing_required_field():
    """Verify player skipped when required field missing."""
    # JSON with player missing 'id'
    # Load players
    # Assert player not in list
    # Assert warning logged

def test_type_mismatch_conversion():
    """Verify type conversion works for common mismatches."""
    # locked as int (0/1) instead of bool
    # Load player
    # Assert locked is boolean
    # Assert warning logged

def test_array_padding():
    """Verify short arrays padded to 17."""
    # projected_points with 10 elements
    # Load player
    # Assert projected_points has 17 elements
    # Assert last 7 are 0.0
    # Assert warning logged

def test_array_truncation():
    """Verify long arrays truncated to 17."""
    # projected_points with 20 elements
    # Load player
    # Assert projected_points has 17 elements
    # Assert warning logged
```

---

## Write Atomicity Policy (Decision 8 - 2025-12-27)

### Overview
Standard approach for all write operations to ensure data integrity and prevent corruption from failed writes.

### Decision: Three-Step Atomic Write Pattern (Formalize Decision 4 Approach)

**Policy:** All write operations in League Helper follow the three-step atomic write pattern originally specified in Decision 4 for update_players_file().

**The Three Steps:**

**Step 1: Backup Existing File**
```python
# Create backup before any modifications
if filepath.exists():
    backup_path = str(filepath) + ".bak"
    shutil.copy(filepath, backup_path)
    logger.debug(f"Created backup: {backup_path}")
```

**Step 2: Write to Temporary File**
```python
# Write new data to temporary file
temp_path = str(filepath) + ".tmp"
with open(temp_path, 'w') as f:
    json.dump(json_data, f, indent=2)
logger.debug(f"Wrote data to temp file: {temp_path}")
```

**Step 3: Atomic Rename**
```python
# Atomically replace original with temp file
os.replace(temp_path, filepath)
logger.info(f"Successfully updated: {filepath}")
```

---

### Why This Approach?

**Backup (.bak file):**
- Allows recovery if write succeeds but data is wrong
- User can manually restore from backup if needed
- Useful for debugging data issues

**Temporary File (.tmp):**
- Prevents partial writes corrupting the original
- If write fails midway, original file is untouched
- Clear indication when write is in progress

**Atomic Rename (os.replace()):**
- OS-level atomic operation (all-or-nothing)
- No window where file doesn't exist or is partially written
- Works across platforms (Windows, Linux, macOS)

**Together:** Provides maximum safety against corruption and data loss.

---

### Current Application

**update_players_file()** (Decision 4)
- Updates drafted_by and locked fields in 6 position JSON files
- Uses three-step pattern for each file write
- Already fully specified and documented

---

### Future Application

**Any new write operations** added to League Helper should follow this pattern:

```python
def write_data_to_file(self, filepath: Path, data: Any) -> None:
    """
    Write data to file using atomic write pattern.

    Args:
        filepath: Target file path
        data: Data to write

    Raises:
        IOError: If backup, write, or rename fails
    """
    # Step 1: Backup
    if filepath.exists():
        backup_path = filepath.with_suffix(filepath.suffix + '.bak')
        shutil.copy(filepath, backup_path)

    # Step 2: Temp write
    temp_path = filepath.with_suffix(filepath.suffix + '.tmp')
    with open(temp_path, 'w') as f:
        json.dump(data, f, indent=2)

    # Step 3: Atomic rename
    os.replace(temp_path, filepath)
```

---

### Error Handling During Writes

**If backup fails:**
- Raise IOError - don't proceed with write
- Original file should not be modified

**If temp write fails:**
- Exception raised, temp file may be incomplete
- Original file and backup untouched
- User can retry operation

**If atomic rename fails:**
- Unlikely (OS-level operation)
- If it fails, original and backup still intact
- Temp file remains (can be manually inspected)

**Cleanup:**
- Keep .bak files (user might need them)
- Remove .tmp files on success
- Log all operations for debugging

---

### Backup File Management

**Rotation Policy:**
- Each write creates new .bak file
- Overwrites previous .bak (only keep most recent)
- Alternative: Could implement numbered backups (.bak.1, .bak.2) if needed

**Current Policy:** Single .bak file (simple, sufficient for current needs)

---

### Platform Considerations

**os.replace() behavior:**
- **Windows:** Replaces file atomically (requires Python 3.3+)
- **Linux/macOS:** Atomic rename (standard POSIX behavior)
- **All platforms:** Overwrites destination if it exists

**shutil.copy() behavior:**
- Preserves file permissions and metadata
- Creates exact copy of original
- Cross-platform compatible

---

### Testing Requirements

**Atomic write pattern tests:**
```python
def test_atomic_write_creates_backup():
    """Verify backup file created before write."""
    # Create original file
    # Perform write
    # Assert .bak exists
    # Assert .bak contents match original

def test_atomic_write_uses_temp_file():
    """Verify temp file used during write."""
    # Mock file write to pause mid-operation
    # Assert .tmp file exists during write
    # Assert .tmp removed after success

def test_atomic_write_preserves_original_on_failure():
    """Verify original unchanged if write fails."""
    # Create original file
    # Force write failure (disk full, permissions, etc.)
    # Assert original file unchanged
    # Assert backup exists

def test_atomic_rename_is_atomic():
    """Verify no window where file doesn't exist."""
    # Monitor file existence during write
    # Assert file always exists (original or new)
    # No gap in availability
```

---

### Summary

**Standard Pattern:**
1. Backup → .bak file
2. Write → .tmp file
3. Rename → atomic replacement

**Applies To:**
- update_players_file() (current)
- Any future write operations (standardized)

**Benefits:**
- Data integrity guaranteed
- Recovery possible if issues discovered
- No corruption from interrupted writes

---

## Directory Creation Policy (Decision 9 - 2025-12-27)

### Overview
Policy for handling missing `/data/player_data/` directory when loading player data.

### Decision: Fail Fast If Directory Missing

**Policy:** Raise FileNotFoundError if `/data/player_data/` directory doesn't exist when attempting to load player data.

**Rationale:**
1. **Consistent with fail-fast approach** - Aligns with Decision 7's error handling philosophy (fail fast for critical errors)
2. **Indicates setup problem** - Missing directory means player-data-fetcher hasn't been run
3. **Clear error message** - Guides user to correct action (run player-data-fetcher)
4. **No false hope** - Creating empty directory won't help since files will still be missing
5. **Prevents cascading failures** - Better to fail immediately than proceed with empty/incorrect data

### Implementation

**Directory Validation (in PlayerManager.load_players_from_json()):**

```python
def load_players_from_json(self) -> List[FantasyPlayer]:
    """
    Load players from position-specific JSON files.

    Raises:
        FileNotFoundError: If player_data directory doesn't exist
        NotADirectoryError: If player_data exists but is not a directory
    """
    player_data_dir = self.data_folder / "player_data"

    # Check 1: Directory must exist
    if not player_data_dir.exists():
        self.logger.error(f"Player data directory not found: {player_data_dir}")
        raise FileNotFoundError(
            f"Player data directory not found: {player_data_dir}. "
            f"Please run player-data-fetcher to generate data files."
        )

    # Check 2: Path must be a directory (not a file)
    if not player_data_dir.is_dir():
        self.logger.error(f"Expected directory but found file: {player_data_dir}")
        raise NotADirectoryError(
            f"player_data exists but is not a directory: {player_data_dir}. "
            f"Please check your data folder structure."
        )

    # Directory exists and is valid - proceed with loading
    self.logger.info(f"Loading player data from: {player_data_dir}")
    players = []

    # Load each position file...
    for position_file in POSITION_FILES:
        filepath = player_data_dir / position_file
        # ... (continue with file loading, per Decision 7 error handling)
```

**Constants (at top of PlayerManager.py):**

```python
POSITION_FILES = [
    'qb_data.json',
    'rb_data.json',
    'wr_data.json',
    'te_data.json',
    'k_data.json',
    'dst_data.json'
]
```

### Error Messages

**Missing Directory:**
```
FileNotFoundError: Player data directory not found: /path/to/data/player_data.
Please run player-data-fetcher to generate data files.
```

**Not a Directory:**
```
NotADirectoryError: player_data exists but is not a directory: /path/to/data/player_data.
Please check your data folder structure.
```

### User Experience

**Expected Flow:**
1. User runs `run_league_helper.py` without running player-data-fetcher first
2. PlayerManager attempts to load players
3. Directory check fails immediately
4. Clear error message tells user exactly what to do
5. User runs `python run_player_fetcher.py`
6. Directory and files created
7. User re-runs league helper successfully

**Error Handling:**
- **Fast failure** - No time wasted attempting to load non-existent files
- **Clear guidance** - Error message tells user the solution
- **Safe state** - No partial data loaded, no corrupt state

### Alternative Approaches NOT Chosen

**Option B: Auto-create directory**
- ❌ Rejected because: Would still fail when files missing
- ❌ Creates false hope (directory exists but empty)
- ❌ Hides the real problem (player-data-fetcher not run)

**Option C: Create during write, error during load**
- ❌ Rejected because: Inconsistent behavior (different for read vs write)
- ❌ Write operations also need directory to exist (can't create files without it)
- ❌ Adds complexity without benefit

### Testing Requirements

**Directory validation tests:**

```python
def test_load_fails_if_directory_missing():
    """Verify FileNotFoundError raised when player_data directory missing."""
    # Remove player_data directory
    player_data_dir = data_folder / "player_data"
    if player_data_dir.exists():
        shutil.rmtree(player_data_dir)

    # Attempt to load players
    manager = PlayerManager(data_folder)

    # Assert FileNotFoundError raised
    with pytest.raises(FileNotFoundError) as exc_info:
        manager.load_players_from_json()

    # Assert error message includes guidance
    assert "run player-data-fetcher" in str(exc_info.value).lower()

def test_load_fails_if_path_is_file_not_directory():
    """Verify NotADirectoryError raised when player_data is a file."""
    # Create file named "player_data" instead of directory
    player_data_path = data_folder / "player_data"
    player_data_path.write_text("invalid")

    # Attempt to load players
    manager = PlayerManager(data_folder)

    # Assert NotADirectoryError raised
    with pytest.raises(NotADirectoryError) as exc_info:
        manager.load_players_from_json()

    # Assert error message explains the problem
    assert "not a directory" in str(exc_info.value).lower()

def test_load_succeeds_when_directory_exists():
    """Verify loading works when directory exists (even if files missing)."""
    # Create player_data directory
    player_data_dir = data_folder / "player_data"
    player_data_dir.mkdir(exist_ok=True)

    # Attempt to load (may fail on missing files per Decision 7, but NOT on directory check)
    manager = PlayerManager(data_folder)

    # This should pass directory validation
    # (File-level errors tested separately per Decision 7)
```

### Integration with Decision 7 (Error Handling)

**Execution Order:**
1. **Decision 9 check (directory)** - Fail fast if directory missing/invalid
2. **Decision 7 Scenario 1 (missing file)** - Fail fast if position file missing
3. **Decision 7 Scenario 2 (malformed JSON)** - Fail fast if file corrupted
4. **Decision 7 Scenarios 3-7** - Graceful handling of individual player issues

**Layered Validation:**
- Level 1: Directory structure (Decision 9)
- Level 2: File existence (Decision 7 Scenario 1)
- Level 3: File format (Decision 7 Scenario 2)
- Level 4: Player data quality (Decision 7 Scenarios 3-7)

---

### Summary

**Policy:** Raise FileNotFoundError if `/data/player_data/` doesn't exist

**Checks:**
1. Directory exists (`player_data_dir.exists()`)
2. Path is a directory (`player_data_dir.is_dir()`)

**Error Messages:**
- Clear guidance to run player-data-fetcher
- Explain the problem and solution

**Benefits:**
- Consistent with fail-fast philosophy
- Prevents wasted time on missing files
- Guides user to correct action
**Benefits:**
- Data integrity guaranteed
- Recovery possible from backups
- Cross-platform compatible
- Industry best practice

**No Additional Work Required:** Already implemented in Decision 4, now formalized as standard.

---

## Backward Compatibility for CSV week_N_points (Decision 10 - 2025-12-27)

### Overview
Policy for handling old CSV format with individual week_N_points fields vs new JSON format with projected_points/actual_points arrays.

### Decision: Immediate Cutover - NO Backward Compatibility

**Policy:** Remove ALL week_N_points fields from FantasyPlayer. No support for old CSV format. Clean break, errors will guide fixes.

**Rationale:**
1. **User intent explicit:** User notes say "instead of" old CSV files (not "in addition to")
2. **Clean architecture:** Single data representation (arrays), no dual code paths
3. **Simpler implementation:** No conditional logic for format detection
4. **Error-driven discovery:** Missing fields will cause compilation errors, ensuring nothing is missed
5. **player-data-fetcher unchanged:** Still generates CSV for other uses, but League Helper won't use it

**Implementation:**

```python
# OLD - REMOVE THESE
class FantasyPlayer:
    week_1_points: Optional[float] = None
    week_2_points: Optional[float] = None
    # ... week_3 through week_17 ...

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            # ...
            week_1_points=data.get('week_1_points'),
            week_2_points=data.get('week_2_points'),
            # ... etc ...
        )

    def get_weekly_projections(self) -> List[float]:
        return [
            self.week_1_points, self.week_2_points, self.week_3_points,
            # ... etc ...
        ]

# NEW - REPLACE WITH THESE
class FantasyPlayer:
    projected_points: List[float] = field(default_factory=lambda: [0.0] * 17)
    actual_points: List[float] = field(default_factory=lambda: [0.0] * 17)

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        return cls(
            # ...
            projected_points=data.get('projected_points', [0.0] * 17),
            actual_points=data.get('actual_points', [0.0] * 17),
        )

    def get_weekly_projections(self) -> List[float]:
        return self.projected_points

    def get_single_weekly_projection(self, week_num: int) -> float:
        return self.projected_points[week_num - 1]  # Already correct!
```

### Comprehensive Sweep Results

**Total files scanned:** 223 files (20 Python source files)

**IN SCOPE - League Helper (12 locations identified):**

1. **utils/FantasyPlayer.py:102-118** - Field definitions (17 week_N_points fields)
   - **Action:** Remove all 17 field definitions
   - **Replace with:** `projected_points` and `actual_points` List[float] fields

2. **utils/FantasyPlayer.py:170-186** - from_dict() loading (17 lines)
   - **Action:** Remove all 17 week_N_points loading lines
   - **Note:** from_dict() is OUT OF SCOPE (used by player-data-fetcher only)

3. **utils/FantasyPlayer.py:345-351** - get_weekly_projections() method
   - **Action:** Change to `return self.projected_points`
   - **Current:** Returns list of 17 individual fields

4. **utils/FantasyPlayer.py:353** - get_single_weekly_projection() method
   - **Action:** Change to `return self.projected_points[week_num - 1]`
   - **Current:** Already uses array indexing! Just needs array to exist

5. **league_helper/save_calculated_points_mode/SaveCalculatedPointsManager.py:112**
   - **Uses:** `player.get_single_weekly_projection(week)`
   - **Action:** NONE - uses method, will work automatically!

6. **league_helper/starter_helper_mode/StarterHelperModeManager.py:212**
   - **Uses:** `recommendation.player.get_single_weekly_projection(current_week)`
   - **Action:** NONE - uses method, will work automatically!

7. **league_helper/util/player_scoring.py:123**
   - **Uses:** `player.get_single_weekly_projection(week)`
   - **Action:** NONE - uses method, will work automatically!

8. **league_helper/util/PlayerManager.py:307**
   - **Uses:** `player.get_single_weekly_projection(week_num)`
   - **Action:** NONE - uses method, will work automatically!

9. **league_helper/util/PlayerManager.py:375-379** - CSV fieldnames for save_players()
   - **Lists:** All 17 week_N_points as CSV columns
   - **Action:** See Decision 4 - migrate to JSON-based update_players_file()
   - **Note:** save_players() likely deprecated (writes to CSV)

10. **league_helper/util/PlayerManager.py:633** - Comment about dict format
    - **Action:** Update comment to reference projected_points/actual_points arrays

11. **league_helper/util/TeamDataManager.py:83, 119** - Comments about D/ST data
    - **Mentions:** "D/ST data: {team: [week_1_points, ..., week_17_points]}"
    - **Action:** Investigate - is this IN SCOPE or separate? (see NEW-46)

12. **league_helper/util/ProjectedPointsManager.py:53, 108-109** - CSV format expectations
    - **Expects:** CSV with week_N_points columns
    - **Action:** Verify if this reads from players.csv or separate source (see NEW-47)

**OUT OF SCOPE - Separate Modules:**
- **player-data-fetcher/** - 3 files, ~40 references (separate module, generates CSV/JSON)
- **historical_data_compiler/** - 1 file, 5 references (separate module)
- **All test files** - Will need updating AFTER implementation

### Key Finding: All User Code Uses Methods!

**CRITICAL DISCOVERY:** All League Helper code accesses weekly data via methods:
- `player.get_single_weekly_projection(week)` - 4 locations
- `player.get_weekly_projections()` - via internal method

**NO direct field access found** (no `.week_1_points`, no `player['week_1_points']`)

**Implication:** Only FantasyPlayer class needs changes. All calling code will work automatically once methods are updated!

### Migration Strategy

**Step 1: Update FantasyPlayer**
1. Remove 17 week_N_points field definitions
2. Add projected_points and actual_points List[float] fields
3. Update get_weekly_projections() to return self.projected_points
4. Update get_single_weekly_projection() to index into self.projected_points
5. Add get_weekly_actuals() and get_single_weekly_actual() methods

**Step 2: Update from_json()**
1. Load projected_points array from JSON
2. Load actual_points array from JSON
3. Validate arrays have exactly 17 elements (pad/truncate per Decision 7)

**Step 3: Verify Call Sites**
1. Run unit tests - should work automatically (methods unchanged)
2. Fix any compilation errors (will guide to missed locations)
3. Update comments referencing old field names

**Step 4: Handle Edge Cases**
1. PlayerManager.save_players() - likely deprecated (see Decision 4)
2. TeamDataManager D/ST data - verify scope
3. ProjectedPointsManager - verify data source

### Testing Requirements

```python
def test_projected_points_array():
    """Verify projected_points array loaded from JSON."""
    player = FantasyPlayer.from_json({
        'projected_points': [10.0, 15.0, 20.0, ...]  # 17 elements
    })
    assert len(player.projected_points) == 17
    assert player.projected_points[0] == 10.0

def test_get_weekly_projections_returns_array():
    """Verify get_weekly_projections() returns projected_points array."""
    player = FantasyPlayer(projected_points=[10.0] * 17)
    weekly = player.get_weekly_projections()
    assert weekly == player.projected_points
    assert len(weekly) == 17

def test_get_single_weekly_projection_indexes_array():
    """Verify get_single_weekly_projection() indexes into array."""
    player = FantasyPlayer(projected_points=[10.0, 20.0, 30.0, ...])
    assert player.get_single_weekly_projection(1) == 10.0
    assert player.get_single_weekly_projection(2) == 20.0
    assert player.get_single_weekly_projection(17) == player.projected_points[16]

def test_week_N_points_fields_removed():
    """Verify week_N_points fields no longer exist."""
    player = FantasyPlayer()
    assert not hasattr(player, 'week_1_points')
    assert not hasattr(player, 'week_17_points')
```

### Summary

**Decision:** Immediate cutover, no CSV backward compatibility

**Benefits:**
- Clean architecture (single data representation)
- Simpler implementation (no dual code paths)
- Error-driven (missing fields cause compilation errors)
- All user code already uses methods (automatic compatibility!)

**Scope:**
- IN SCOPE: League Helper (12 locations, mostly comments + FantasyPlayer)
- OUT OF SCOPE: player-data-fetcher, historical_data_compiler, tests

**Implementation Complexity:** LOW - Only FantasyPlayer needs changes, rest works automatically

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

## ProjectedPointsManager Migration (2025-12-27)

### Scope Decision

**✅ IN SCOPE (Decision made 2025-12-27)**

**Question:** Should ProjectedPointsManager migration be included in this feature?

**Decision:** YES - Include NEW-100 through NEW-122 (23 items)

**Rationale:**
- Low risk (1 file, interface unchanged, data identical)
- Small addition (23 items is manageable)
- Completes CSV elimination (removes players_projected.csv dependency)
- Natural companion to PlayerManager migration (both load player projection data)
- Independent work (can be implemented in parallel, no blocking dependencies)

### Overview

**Purpose:** ProjectedPointsManager manages access to ORIGINAL pre-season projected points for performance deviation calculations. Currently loads from `players_projected.csv`, needs migration to read from JSON `projected_points` arrays.

**Current Implementation:**
- **File:** `league_helper/util/ProjectedPointsManager.py`
- **Data Source:** `data/players_projected.csv`
- **Format:** CSV with columns: `id,name,week_1_points,week_2_points,...,week_17_points`
- **Purpose:** Holds STATIC pre-season projections (never changes during season)
- **Usage:** Used by `player_scoring.py` for performance deviation calculations

**Key Distinction:**
- **players_projected.csv** = ORIGINAL pre-season projections (static)
- **players.csv week_N_points** = HYBRID data (actual for past, projected for future, updated weekly)
- These are TWO DIFFERENT data sources with different purposes

### Current Usage

**Instantiation (PlayerManager.py:113):**
```python
self.projected_points_manager = ProjectedPointsManager(config, data_folder)
```

**Usage (player_scoring.py:235):**
```python
# Get ORIGINAL projection for performance deviation calculation
projected_points = self.projected_points_manager.get_projected_points(player, week)

# Compare actual vs original to calculate performance multiplier
if actual_points > 0 and projected_points is not None and projected_points > 0:
    deviation = (actual_points - projected_points) / projected_points
```

**Methods:**
1. `__init__(config, data_folder)` - Loads CSV on initialization
2. `_load_projected_data()` - Loads CSV into pandas DataFrame
3. `get_projected_points(player, week_num)` - Returns float for specific player/week (or None)
4. `get_projected_points_array(player, start_week, end_week)` - Returns list of floats
5. `get_historical_projected_points(player)` - Returns list for weeks 1 to current-1

**Player Lookup:** Uses PLAYER NAME (case-insensitive), not ID

### New Data Source (JSON)

**Location:** `data/player_data/*.json` (6 position files)

**Structure:**
```json
{
  "qb_data": [
    {
      "id": 4429795,
      "name": "Jahmyr Gibbs",
      "projected_points": [18.41926089, 18.07282489, ..., 20.78756694],
      ...
    }
  ]
}
```

**Data Verification:**
- ✅ CSV and JSON contain IDENTICAL values (verified 2025-12-27)
- CSV: `4429795,Jahmyr Gibbs,18.41926089,18.07282489,...,20.78756694`
- JSON: `"projected_points": [18.41926089, 18.07282489, ..., 20.78756694]`

### Migration Strategy

**✅ DECISION: Option A - Update ProjectedPointsManager to Read JSON**

**Approach:**
- Update `_load_projected_data()` to read 6 JSON position files instead of CSV
- Build in-memory lookup: `{name_lower: projected_points_array}`
- Replace pandas DataFrame with native Python dict
- Maintain existing interface (no changes to callers)

**Implementation:**
```python
def _load_projected_data(self):
    """Load projected points from JSON position files."""
    position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                      'te_data.json', 'k_data.json', 'dst_data.json']

    # Build in-memory lookup
    self.projected_lookup = {}

    for position_file in position_files:
        filepath = self.data_folder / 'player_data' / position_file

        if not filepath.exists():
            raise FileNotFoundError(f"Position file not found: {filepath}")

        with open(filepath, 'r') as f:
            data = json.load(f)

        # Extract position key (e.g., "qb_data" from qb_data.json)
        position_key = position_file.replace('.json', '')
        players = data.get(position_key, [])

        for player in players:
            name_lower = player['name'].lower().strip()
            projected_points = player.get('projected_points', [0.0] * 17)
            self.projected_lookup[name_lower] = projected_points

def get_projected_points(self, player, week_num):
    """Get projected points for specific player and week."""
    # Normalize player name
    player_name_lower = player.name.lower().strip()

    # Look up player in in-memory structure
    projected_array = self.projected_lookup.get(player_name_lower)

    if projected_array is None:
        return None

    # Validate week number
    if week_num < 1 or week_num > 17:
        return None

    # Get value from array (week_num=1 is index 0)
    projected_value = projected_array[week_num - 1]

    # Handle 0.0 as None (no projection available, matches CSV behavior)
    if projected_value == 0.0:
        return None

    return float(projected_value)
```

### Key Design Decisions

**1. In-Memory Lookup Structure**

**Decision:** ✅ Use Python dict `{name_lower: projected_points_array}`

**Rationale:**
- Simpler than pandas DataFrame
- No pandas dependency needed
- O(1) lookup performance maintained
- Native Python types only

**2. Handle 0.0 in Array**

**Decision:** ✅ Treat 0.0 as "no projection" (return None)

**Rationale:**
- Matches current CSV behavior (NaN → None)
- Bye weeks legitimately have 0.0 projection
- Consistent with existing logic in player_scoring

**3. Remove players_projected.csv**

**Decision:** ⏳ DEFER to cleanup phase

**Rationale:**
- Keep file during development for validation
- Mark as deprecated after migration complete
- Can remove in future cleanup

### Breaking Changes

**None** - Interface unchanged:
- Constructor signature: `ProjectedPointsManager(config, data_folder)` ✅ Same
- Method signatures: `get_projected_points(player, week_num)` ✅ Same
- Return types: `float` or `None` ✅ Same

**No caller modifications required:**
- `PlayerManager.py` continues to instantiate the same way
- `player_scoring.py` continues to call methods the same way

### Files Affected

**Files Requiring Changes: 1 file**
- `league_helper/util/ProjectedPointsManager.py` - Core migration (all methods)

**Files NOT Requiring Changes: 2 files**
- `league_helper/util/PlayerManager.py` - Instantiation unchanged
- `league_helper/util/player_scoring.py` - Method calls unchanged

**Test Files Requiring Updates: 1 file**
- `tests/league_helper/util/test_ProjectedPointsManager.py` - Update to use JSON fixtures

### Implementation Checklist

**See:** PROJECTED_POINTS_MANAGER_ANALYSIS.md for complete implementation details

**Summary (23 items: NEW-100 through NEW-122):**

1. **Core Implementation (7 items)** - Remove pandas, add json, update _load_projected_data(), build dict, update get_projected_points()
2. **Edge Cases (5 items)** - Handle 0.0 vs None, missing players, invalid weeks, corrupted JSON, empty arrays
3. **Testing (6 items)** - Update test fixtures, test all methods, test error handling
4. **Integration (3 items)** - Verify player_scoring, performance multiplier, no regressions
5. **Cleanup (2 items)** - Deprecate CSV, update documentation

### Risk Assessment

**Risk Level:** LOW

**Why Low Risk:**
- Interface unchanged (same method signatures)
- Data identical (verified CSV vs JSON match)
- Single file to modify
- No dependencies on other migration work
- Comprehensive testing plan

**Testing Critical:**
- Performance deviation calculations are complex
- Must verify exact same results with JSON vs CSV
- Integration tests required for player_scoring

### Dependencies

**None** - Independent of other migration work

**Can be implemented:**
- Before or after FantasyPlayer migration
- Before or after PlayerManager migration
- Independently of all other changes

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
