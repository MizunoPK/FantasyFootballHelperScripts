# Player Data Fetcher - New Data Format

## Objective

Update the player-data-fetcher to generate position-based JSON files containing detailed player statistics and projections, while maintaining backward compatibility with existing CSV file generation.

---

## High-Level Requirements

### 1. Output Structure
- **Location:** `/data/player_data/` folder
- **Files:** 6 JSON files (one per position)
  - `new_qb_data.json`
  - `new_rb_data.json`
  - `new_wr_data.json`
  - `new_te_data.json`
  - `new_k_data.json`
  - `new_dst_data.json`
- **Format:** Each file contains an array of player objects for that position only

### 2. Data Fields

**Common Fields (all positions):**
- `id` (number) - player identifier
- `name` (string) - player full name
- `team` (string) - team abbreviation
- `position` (string) - player position
- `injury_status` (string) - injury status
- `drafted_by` (string) - owning team name or empty string for free agents
- `locked` (boolean) - locked status (true/false)
- `average_draft_position` (number or null) - ADP value
- `player_rating` (number or null) - player rating value
- `projected_points` (array[17]) - weekly projected points
- `actual_points` (array[17]) - weekly actual points

**Position-Specific Statistical Arrays:**
- QB: passing stats, rushing stats, receiving stats, misc stats
- RB: rushing stats, receiving stats, misc stats
- WR: receiving stats, rushing stats, misc stats
- TE: receiving stats, misc stats
- K: extra points stats, field goals stats
- DST: defense stats (includes ret_yds and ret_tds)

Each statistical array contains 17 elements (one per week), with 0 for unplayed weeks.

**Note:** All positions except DST do NOT include `ret_yds` or `ret_tds` fields (Decision 6).

### 3. Data Transformations from CSV

| CSV Field | New JSON Field | Transformation |
|-----------|----------------|----------------|
| `drafted` (0/1/2) | `drafted_by` (string) | 0→"", 1→Team1Name, 2→Team2Name (from drafted_data.csv) |
| `locked` (0/1) | `locked` (boolean) | 0→false, 1→true |
| `week_N_points` columns | `projected_points[N-1]` | Combine into array, 0-indexed |
| `week_N_points` columns | `actual_points[N-1]` | Combine into array, 0-indexed |

### 4. Configuration
- Add toggle to player-data-fetcher config: `CREATE_POSITION_JSON = True`
- Default: **True (enabled by default)** ✅
- Existing CSV generation remains unchanged
- Output folder: `POSITION_JSON_OUTPUT = "../data/player_data"`

### 5. Quality Control Requirements
- **Array length validation:** All arrays must have exactly 17 elements
- **Null handling:** Arrays must NOT contain null values - use 0 for unplayed weeks
- **Unplayed week detection:** Reference current NFL season (2025, Week 17 not yet started)
- **Data accuracy:** Manually verify multiple players from each position against internet sources

---

## User Decisions (ALL RESOLVED ✅)

**See `USER_DECISIONS_SUMMARY.md` for complete details**

### Data Structure Decisions

**✅ Decision 1 - Config Toggle Default:** `CREATE_POSITION_JSON = True` (enabled by default)
- Rationale: Feature needed immediately, minimal performance impact (async execution)
- Consistent with existing `CREATE_CSV = True` pattern

**✅ Decision 2 - Array Length:** 17 elements (weeks 1-17, fantasy regular season only)
- Rationale: Matches existing ESPNPlayerData model, fantasy leagues exclude Week 18
- All arrays (`projected_points`, `actual_points`, stat arrays) have exactly 17 elements
- Array index 0 = Week 1, index 16 = Week 17
- Example file's 18 elements was a typo

**✅ Decision 3 - Field Naming - "receiving":** Use correct spelling (not "recieving")
- Applies to: `"receiving"`, `"receiving_yds"`, `"receiving_tds"`
- Rationale: Professional code quality, correct English spelling
- Example files were templates with typos

**✅ Decision 4 - Field Naming - "two_pt":** Use conventional naming (not "2_pt")
- Change `"2_pt"` to `"two_pt"` (starts with letter, follows snake_case)
- Rationale: Consistent with other keys, prevents potential downstream issues

**✅ Decision 5 - Array Population:** Actual data for past weeks, zeros for future weeks
- For week <= CURRENT_NFL_WEEK: Extract actual stats (statSourceId=0)
- For week > CURRENT_NFL_WEEK: Use 0
- Missing stat data for past weeks: Use 0 (never null)
- Rationale: Clear semantics, consistent with user notes

**✅ Decision 6 - Return Yards/TDs:** Remove from non-DST positions entirely
- `ret_yds` and `ret_tds` only appear in DST `defense` section
- QB, RB, WR, TE, K files do NOT include these fields
- Rationale: ESPN only provides return data for D/ST players, avoids misleading zeros

**✅ Decision 7 - Field Goal Structure:** Simplified to totals only
- Remove all distance breakdowns (under_19, under_29, under_39, under_49, over_50)
- Keep only: `field_goals.made` and `field_goals.missed`
- Rationale: ESPN provides 3 distance ranges but example had 5, simplify to universally available totals

### ESPN API Data Decisions

**✅ Decision 8 - Stat Arrays for Past Weeks:** Use actual stats (statSourceId=0)
- Parallel to `actual_points` array logic
- Extract from ESPN API statSourceId=0 for weeks <= CURRENT_NFL_WEEK
- Rationale: More valuable data (actual performance vs old projections)

**✅ Decision 9 - Stat Arrays for Future Weeks:** Use zeros
- Clear indication: zero = game not yet played
- Separate concerns: projected_points has projections, stat arrays have actuals only
- Rationale: Clear semantic meaning, consistent with "use 0 for unplayed weeks"

**✅ Decision 11 - Missing Stat Handling:** Always use 0
- Never use null, None, or empty values
- Applies to: future weeks, missing API data, stats that didn't occur, bye weeks
- Rationale: Matches user notes, simplest implementation, correct semantics

### Implementation Decisions

**✅ Decision 10 - Team Name Reverse Lookup:** Add method to DraftedRosterManager
- Create `get_team_name_for_player(player)` method in `utils/DraftedRosterManager.py`
- Returns team name string for drafted players, empty string for free agents
- Keeps DraftedRosterManager as single source of truth
- Clean API for DataExporter to call during JSON export
- Rationale: Encapsulated logic, simple implementation

---

## Resolved Implementation Details

### Drafted Data Integration (RESEARCHED - Round 3)

**Source File:** `utils/DraftedRosterManager.py` (635 lines, comprehensive implementation)

**How It Works:**
The player-data-fetcher already has a complete system for loading drafted player data from `drafted_data.csv` and applying it to FantasyPlayer objects. This system can be reused for the new JSON format.

**CSV Format:**
```csv
player_info, team_name
Puka Nacua WR - LAR,Nixelodeon
Matthew Stafford QB - LAR,Nixelodeon
Kenneth Walker III RB - SEA,Pidgin
```

**Transformation Algorithm:**
```python
# Current System (CSV): drafted field (0/1/2)
# - 0: Free agent (not in drafted_data.csv)
# - 1: Drafted by another team
# - 2: On user's team (MY_TEAM_NAME from config)

# New System (JSON): drafted_by field (string)
# - "": Free agent
# - "Nixelodeon": Owned by team Nixelodeon
# - "Sea Sharp": Owned by user's team (MY_TEAM_NAME = "Sea Sharp")

# Reuse DraftedRosterManager.apply_drafted_state_to_players():
# 1. Load drafted_data.csv → Dict[normalized_player_key, team_name]
# 2. Match players using fuzzy matching (handles name variations)
# 3. Set drafted=1 for other teams, drafted=2 for MY_TEAM_NAME
# 4. For JSON export: map drafted value to team name string
```

**Team Name Mapping Logic:**
```python
# For each player in JSON export:
if player.drafted == 0:
    drafted_by = ""  # Free agent
elif player.drafted == 1:
    # Look up team name from drafted_data.csv
    drafted_by = drafted_roster_manager.get_team_for_player(player)
elif player.drafted == 2:
    drafted_by = MY_TEAM_NAME  # From config.py
```

**Key Implementation Details:**
- **DraftedRosterManager** handles fuzzy matching (handles "St. Brown" vs "St Brown", "Josh Allen" vs "Joshua Allen")
- **Position equivalency:** Handles DST/DEF/D/ST variations
- **Team abbreviation normalization:** Handles WSH/WAS, etc.
- **Similarity scoring:** 0.75 threshold for fuzzy matches
- **Progressive matching strategy:**
  1. Exact full name match (O(1))
  2. Defense-specific matching (handles name format variations)
  3. Exact last name + position/team validation
  4. Exact first name for unique names
  5. Fuzzy matching fallback (O(n) with similarity scoring)

**Config Settings (from config.py):**
```python
LOAD_DRAFTED_DATA_FROM_FILE = True  # Enable drafted_data.csv loading
DRAFTED_DATA = "../data/drafted_data.csv"  # Path to CSV
MY_TEAM_NAME = "Sea Sharp"  # User's team name for drafted=2 identification
```

**Existing Integration Point:**
In `player_data_exporter.py` line 328:
```python
fantasy_players = self.drafted_roster_manager.apply_drafted_state_to_players(fantasy_players)
```

This is called during `get_fantasy_players()` which converts ESPNPlayerData to FantasyPlayer objects. The new JSON export can call this same method, then map the `drafted` field to `drafted_by` string.

---

## Implementation Notes

### Files to Modify

**Core Implementation Files:**
1. **`player-data-fetcher/player_data_exporter.py`** (565 lines)
   - Add new method: `export_position_json_files()` (similar to `export_all_formats()`)
   - Add helper: `_prepare_position_json_data()` for transformations
   - Reuse: `get_fantasy_players()` for drafted state application
   - Location: Lines 336-365 (after `export_all_formats_with_teams()`)

2. **`player-data-fetcher/config.py`** (88 lines)
   - Add config toggle: `CREATE_POSITION_JSON = True`
   - Add output path constant: `POSITION_JSON_OUTPUT = "../data/player_data"`
   - Location: Lines 26-31 (with other output settings)

3. **`player-data-fetcher/player_data_fetcher_main.py`** (orchestration)
   - Add position JSON export to main workflow
   - Call `exporter.export_position_json_files()` if enabled
   - Location: After team data exports

**Data Model Files (READ-ONLY - for reference):**
- `player_data_models.py` - ESPNPlayerData structure
- `utils/FantasyPlayer.py` - FantasyPlayer model
- `utils/DraftedRosterManager.py` - Drafted state logic

### Dependencies
- **ESPN API** (existing integration via `data_sources/espn_client.py`)
- **drafted_data.csv** (existing file at `../data/drafted_data.csv`)
- **Player-data-fetcher config** (existing `config.py`)
- **Example JSON files** (reference format in `feature-updates/new_*.json`)
- **DraftedRosterManager** (existing `utils/DraftedRosterManager.py`)
- **ESPN Stat ID Mappings** (documented in `FINAL_STAT_RESEARCH_COMPLETE.md`)

### Reusable Code Patterns

**1. Async Export Pattern (from player_data_exporter.py):**
```python
async def export_position_json_files(self, data: ProjectionData) -> List[str]:
    """Export position-based JSON files concurrently"""
    tasks = []
    for position in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:
        tasks.append(self._export_single_position_json(data, position))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    # Filter exceptions, return successful paths
```

**2. Drafted State Application (REUSE EXISTING):**
```python
# In DataExporter.__init__() (lines 64-67):
self.drafted_roster_manager = DraftedRosterManager(DRAFTED_DATA, MY_TEAM_NAME)
if LOAD_DRAFTED_DATA_FROM_FILE:
    self.drafted_roster_manager.load_drafted_data()

# In get_fantasy_players() (line 328):
fantasy_players = self.drafted_roster_manager.apply_drafted_state_to_players(fantasy_players)
```

**3. File Manager Pattern (from player_data_exporter.py):**
```python
# Use DataFileManager for consistent file handling:
timestamped_path = self.file_manager.get_timestamped_path(prefix, 'json')
# No automatic caps enforcement for position JSON files (keep all versions)
```

**4. Team Name Reverse Lookup (NEW - needs implementation):**
```python
def _get_team_name_for_player(self, player: FantasyPlayer) -> str:
    """
    Get fantasy team name for a player based on drafted status.

    Returns:
        - "" if drafted=0 (free agent)
        - MY_TEAM_NAME if drafted=2 (user's team)
        - Actual team name from drafted_data.csv if drafted=1
    """
    if player.drafted == 0:
        return ""
    elif player.drafted == 2:
        return MY_TEAM_NAME
    else:
        # Need to reverse-lookup team name from DraftedRosterManager
        # Requires adding method to DraftedRosterManager or caching mapping
        return self._reverse_lookup_team_name(player)
```

**5. Data Transformation Pattern:**
```python
# Boolean transformation (locked):
json_player['locked'] = bool(fantasy_player.locked)  # 0/1 → false/true

# Array transformation (weekly points):
json_player['projected_points'] = [
    fantasy_player.get_week_points(week) or 0.0
    for week in range(1, 18)
]

# String transformation (drafted_by):
json_player['drafted_by'] = self._get_team_name_for_player(fantasy_player)
```

### Testing Strategy
- Unit tests for data transformation logic
- Unit tests for array population logic
- Integration test for full JSON file generation
- Manual validation against real player data
- Config toggle tests

---

---

## Complete Data Structures (All Decisions Applied)

### QB/RB/WR Structure:

```json
{
    "qb_data": [  // or "rb_data", "wr_data"
        {
            "id": 123,
            "name": "Trevor Lawrence",
            "team": "JAX",
            "position": "QB",
            "injury_status": "ACTIVE",
            "drafted_by": "Sea Sharp",
            "locked": true,
            "average_draft_position": 170,
            "player_rating": 97,
            "projected_points": [18.4, 18.1, ..., 22.6],  // 17 elements
            "actual_points": [97.5, 15.0, ..., 9.8, 0],   // 17 elements

            "passing": {
                "completions": [25, 18, ..., 0],           // stat_1
                "attempts": [39, 30, ..., 0],              // stat_0
                "pass_yds": [315, 280, ..., 0],            // stat_3
                "pass_tds": [2, 1, ..., 0],                // stat_4
                "interceptions": [1, 0, ..., 0],           // stat_20
                "sacks": [2, 3, ..., 0]                    // stat_64
            },
            "rushing": {
                "attempts": [3, 2, ..., 0],                // stat_23
                "rush_yds": [15, 8, ..., 0],               // stat_24
                "rush_tds": [0, 0, ..., 0]                 // stat_25
            },
            "receiving": {
                "targets": [0, 0, ..., 0],                 // stat_58
                "receiving_yds": [0, 0, ..., 0],           // stat_42
                "receiving_tds": [0, 0, ..., 0],           // stat_43
                "receptions": [0, 0, ..., 0]               // stat_53
            },
            "misc": {
                "fumbles": [0, 1, ..., 0],                 // stat_68
                "two_pt": [0, 0, ..., 0]                   // stat_19/26/44/62 combined
            }
        }
    ]
}
```

### TE Structure:

```json
{
    "te_data": [
        {
            "id": 234,
            "name": "Travis Kelce",
            "team": "KC",
            "position": "TE",
            "injury_status": "ACTIVE",
            "drafted_by": "Nixelodeon",
            "locked": false,
            "average_draft_position": 45,
            "player_rating": 98,
            "projected_points": [12.5, 11.8, ..., 13.2],
            "actual_points": [15.2, 8.4, ..., 0],

            "receiving": {
                "targets": [8, 6, ..., 0],
                "receiving_yds": [95, 72, ..., 0],
                "receiving_tds": [1, 0, ..., 0],
                "receptions": [6, 4, ..., 0]
            },
            "misc": {
                "fumbles": [0, 0, ..., 0],
                "two_pt": [0, 0, ..., 0]
            }
        }
    ]
}
```

### K (Kicker) Structure:

```json
{
    "k_data": [
        {
            "id": 456,
            "name": "Brandon Aubrey",
            "team": "DAL",
            "position": "K",
            "injury_status": "ACTIVE",
            "drafted_by": "",
            "locked": false,
            "average_draft_position": 200,
            "player_rating": 85,
            "projected_points": [8.5, 9.2, ..., 8.8],
            "actual_points": [12.0, 6.0, ..., 0],

            "extra_points": {
                "made": [3, 2, ..., 0],                    // stat_86
                "missed": [0, 0, ..., 0]                   // stat_88
            },
            "field_goals": {
                "made": [2, 1, ..., 0],                    // stat_83 (total)
                "missed": [0, 1, ..., 0]                   // stat_85 (total)
            }
        }
    ]
}
```

### DST Structure:

```json
{
    "dst_data": [
        {
            "id": 789,
            "name": "Eagles D/ST",
            "team": "PHI",
            "position": "DST",
            "injury_status": "ACTIVE",
            "drafted_by": "Pidgin",
            "locked": false,
            "average_draft_position": 150,
            "player_rating": 92,
            "projected_points": [10.5, 11.2, ..., 10.8],
            "actual_points": [15.0, 8.0, ..., 0],

            "defense": {
                "yds_g": [320, 280, ..., 0],               // stat_127
                "pts_g": [17, 21, ..., 0],                 // stat_120
                "def_td": [1, 0, ..., 0],                  // stat_94
                "sacks": [4, 3, ..., 0],                   // stat_99
                "safety": [0, 1, ..., 0],                  // stat_98
                "interceptions": [2, 1, ..., 0],           // stat_95
                "forced_fumble": [1, 2, ..., 0],           // stat_106
                "fumbles_recovered": [1, 1, ..., 0],       // stat_96
                "ret_yds": [29, 15, ..., 0],               // stat_114 + stat_115
                "ret_tds": [0, 0, ..., 0]                  // stat_101 + stat_102
            }
        }
    ]
}
```

---

## ESPN Stat ID Mappings (Complete)

**See `FINAL_STAT_RESEARCH_COMPLETE.md` for full research details**

### Passing Stats
- `stat_0`: Pass attempts
- `stat_1`: Pass completions
- `stat_3`: Passing yards
- `stat_4`: Passing TDs
- `stat_20`: Interceptions
- `stat_64`: Sacks taken

### Rushing Stats
- `stat_23`: Rush attempts
- `stat_24`: Rushing yards
- `stat_25`: Rushing TDs

### Receiving Stats
- `stat_42`: Receiving yards
- `stat_43`: Receiving TDs
- `stat_53`: Receptions
- `stat_58`: Targets

### Kicking Stats (Extra Points)
- `stat_86`: XP made
- `stat_87`: XP attempted
- `stat_88`: XP missed

### Kicking Stats (Field Goals - Simplified)
- `stat_83`: Total FG made
- `stat_85`: Total FG missed

### Defense Stats
- `stat_94`: Defensive TDs
- `stat_95`: Interceptions
- `stat_96`: Fumbles recovered
- `stat_98`: Safeties
- `stat_99`: Sacks
- `stat_106`: Forced fumbles
- `stat_120`: Points allowed per game
- `stat_127`: Yards allowed per game

### Return Stats (DST Only)
- `stat_114`: Kickoff return yards
- `stat_115`: Punt return yards
- `stat_101`: Kickoff return TDs
- `stat_102`: Punt return TDs

### Misc Stats
- `stat_68`: Fumbles (all positions)
- `stat_19`: 2-pt conversions (passing)
- `stat_26`: 2-pt conversions (rushing)
- `stat_44`: 2-pt conversions (receiving)
- `stat_62`: 2-pt conversions (return - DST only)

---

## Status: PLANNING COMPLETE - Ready for Implementation ✅
