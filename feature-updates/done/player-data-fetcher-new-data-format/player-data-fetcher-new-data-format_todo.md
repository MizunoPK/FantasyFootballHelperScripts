# Player Data Fetcher - New Data Format - Implementation TODO

## Iteration Progress Tracker

### Compact View (Quick Status)

```
R1: ■■■■■■■■ (8/8)   R2: ■■■■■■■■■ (9/9)   R3: ■■■■■■■■■ (9/9)  ✅ ALL COMPLETE
```
Legend: ■ = complete, □ = pending, ▣ = in progress

**Current:** ALL 24 + 1 ITERATIONS COMPLETE ✅
**Confidence:** HIGH (passed 4-part spec audit, ready after interface verification)
**Blockers:** Interface Verification Protocol (must run before coding)

### Detailed View

| Round | Iterations | Status |
|-------|------------|--------|
| First (7+1) | [x]1 [x]2 [x]3 [x]4 [x]4a [x]5 [x]6 [x]7 | 8/8 ✅ |
| Second (9) | [x]8 [x]9 [x]10 [x]11 [x]12 [x]13 [x]14 [x]15 [x]16 | 9/9 ✅ |
| Third (8+1) | [x]17 [x]18 [x]19 [x]20 [x]21 [x]22 [x]23 [x]23a [x]24 | 9/9 ✅ |

**Total Progress:** 24 iterations + iteration 23a = **25/25 COMPLETE** ✅

---

## Protocol Execution Tracker

Track which protocols have been executed (protocols must be run at specified iterations):

| Protocol | Required Iterations | Completed |
|----------|---------------------|-----------|
| Standard Verification | 1, 2, 3, 8, 9, 10, 15, 16 | [x]1 [x]2 [x]3 [x]8 [x]9 [x]10 [x]15 [x]16 ✅ |
| Algorithm Traceability | 4, 11, 19 | [x]4 [x]11 [x]19 ✅ |
| TODO Specification Audit | 4a | [x]4a ✅ |
| End-to-End Data Flow | 5, 12 | [x]5 [x]12 ✅ |
| Skeptical Re-verification | 6, 13, 22 | [x]6 [x]13 [x]22 ✅ |
| Integration Gap Check | 7, 14, 23 | [x]7 [x]14 [x]23 ✅ |
| Fresh Eyes Review | 17, 18 | [x]17 [x]18 ✅ |
| Edge Case Verification | 20 | [x]20 ✅ |
| Test Coverage Planning + Mock Audit | 21 | [x]21 ✅ |
| Pre-Implementation Spec Audit | 23a | [x]23a ✅ |
| Implementation Readiness | 24 | [x]24 ✅ |
| Interface Verification | Pre-impl | [x] ✅ COMPLETE |

---

## Interface Verification Results

**Status:** ✅ ALL 3 INTERFACES VERIFIED

Verified the following interfaces against actual source code before implementation:

### Interface 1: FantasyPlayer ✅ VERIFIED
**File:** `utils/FantasyPlayer.py` (lines 77-121)

**Verified Attributes:**
- `id: int` (line 87) - Integer ID from ESPN API
- `name: str` (line 88) - Player name
- `team: str` (line 89) - NFL team abbreviation
- `position: str` (line 90) - Position code (QB, RB, WR, TE, K, DST)
- `drafted: int = 0` (line 94) - 0=FA, 1=opponent, 2=my_team
- `locked: int = 0` (line 95) - 0/1 boolean as int
- `average_draft_position: Optional[float] = None` (line 97)
- `player_rating: Optional[float] = None` (line 98)
- `week_1_points` through `week_17_points: Optional[float]` (lines 102-118)
- `injury_status: str = "UNKNOWN"` (line 121)

**Status:** All assumptions VERIFIED ✅

### Interface 2: ESPNPlayerData ✅ VERIFIED
**File:** `player-data-fetcher/player_data_models.py` (lines 24-66)

**Verified Attributes:**
- `id: str` (line 33) - **IMPORTANT: This is str, not int!**
- `name: str` (line 34)
- `team: str` (line 35)
- `position: str` (line 36)
- `drafted: int = 0` (line 40)
- `locked: int = 0` (line 41)
- `average_draft_position: Optional[float] = None` (line 43)
- `player_rating: Optional[float] = None` (line 44)
- `week_1_points` through `week_17_points: Optional[float]` (lines 47-63)
- `injury_status: str = "ACTIVE"` (line 66)

**Important Finding:** ESPNPlayerData.id is **str**, FantasyPlayer.id is **int**
- This difference is handled by existing conversion in `get_fantasy_players()` method
- No changes needed to TODO tasks (conversion already exists)

**Status:** All attributes VERIFIED ✅

### Interface 3: DraftedRosterManager ✅ VERIFIED
**File:** `utils/DraftedRosterManager.py`

**Verified Attributes & Methods:**
- `drafted_players: Dict[str, str]` (line 62) - Normalized player key → team name mapping
  - Structure confirmed: `{"normalized_player_key": "fantasy_team_name"}`
  - Populated in `load_drafted_data()` method (lines 65-124)
- `_normalize_player_info(self, player_info: str) -> str` (lines 269-301)
  - Signature matches expected usage in Task 1.2
  - Handles name normalization (removes Jr./Sr., punctuation, injury tags, etc.)
  - Returns normalized lowercase string for consistent matching

**New Method Design (Task 1.2):**
```python
def get_team_name_for_player(self, player: FantasyPlayer) -> str:
    """
    Get fantasy team name for a player.

    Args:
        player: FantasyPlayer object

    Returns:
        Team name string if player is drafted, empty string otherwise
    """
    # Build normalized player key (same format as apply_drafted_state_to_players)
    player_info = f"{player.name} {player.position} - {player.team}"
    player_key = self._normalize_player_info(player_info)

    # Look up in drafted_players dict
    return self.drafted_players.get(player_key, "")
```

**Status:** All assumptions VERIFIED ✅ - Ready to implement

---

## Verification Summary

- Iterations completed: 16/24 (Rounds 1-2 complete ✅)
- Requirements from spec: 22 algorithms + 11 decisions = 33 total
- Requirements in TODO: 37 acceptance criteria
- Questions for user: 0 (all 11 decisions already made during planning)
- Integration points identified: 12 components, all with callers verified
- Cross-feature impact: ZERO (DraftedRosterManager change is additive only)
- Dependencies verified: 9/9 (all available)
- File paths verified: All corrected (1 test path fixed in iteration 15)
- Integration Checklist: COMPLETE (iteration 16)

---

## Phase 1: Infrastructure Setup

### Task 1.1: Add config settings to config.py
- **File:** `player-data-fetcher/config.py`
- **Location:** Lines 26-31 (with other output settings)
- **Tests:** `tests/player-data-fetcher/test_config.py` (verify new settings exist)
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ REQUIREMENT 1: Add CREATE_POSITION_JSON toggle
  - Spec: specs.md Decision 1
  - Value: `CREATE_POSITION_JSON = True` (enabled by default)
  - Location: After CREATE_CONDENSED_EXCEL setting
  - NOT: False by default ❌

✓ REQUIREMENT 2: Add POSITION_JSON_OUTPUT path constant
  - Spec: specs.md lines 60-61
  - Value: `POSITION_JSON_OUTPUT = "../data/player_data"`
  - Type: String path to output folder
  - NOT: Absolute path or different folder ❌

**Implementation details:**
```python
# In config.py around line 29:
CREATE_POSITION_JSON = True  # NEW: Generate position-based JSON files
DEFAULT_FILE_CAPS = {'csv': 5, 'json': 5, 'xlsx': 5, 'txt': 5}

# Position JSON Output Settings
POSITION_JSON_OUTPUT = "../data/player_data"  # NEW: Output folder for position JSON files
```

**IMPORTANT - Dependencies:**
After adding these constants to config.py, update player_data_exporter.py imports:
```python
# Update line 31 in player_data_exporter.py to include new constants:
from config import DEFAULT_FILE_CAPS, CREATE_POSITION_JSON, POSITION_JSON_OUTPUT, \
    EXCEL_POSITION_SHEETS, EXPORT_COLUMNS, PRESERVE_DRAFTED_VALUES, PRESERVE_LOCKED_VALUES, \
    PLAYERS_CSV, TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME
```

### Task 1.2: Add get_team_name_for_player() method to DraftedRosterManager
- **File:** `utils/DraftedRosterManager.py`
- **Similar to:** Existing `_normalize_player_info()` method (lines vary)
- **Tests:** `tests/utils/test_DraftedRosterManager.py`
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ REQUIREMENT 1: Method signature matches USER_DECISIONS_SUMMARY.md
  - Spec: Decision 10, lines 156-172
  - Signature: `def get_team_name_for_player(self, player: FantasyPlayer) -> str:`
  - Returns: Team name string or empty string
  - NOT: Returns None or raises exception ❌

✓ REQUIREMENT 2: Uses drafted_players dict for lookup
  - Spec: Decision 10
  - Logic: Build normalized key, look up in self.drafted_players
  - Returns: self.drafted_players.get(player_key, "")
  - NOT: Iterates through all players ❌

✓ REQUIREMENT 3: Normalizes player key same as apply_drafted_state_to_players()
  - Spec: specs.md Round 3 research
  - Uses: self._normalize_player_info(player_info)
  - Format: "{player.name} {player.position} - {player.team}"
  - NOT: Different normalization algorithm ❌

**Implementation details:**
```python
def get_team_name_for_player(self, player: FantasyPlayer) -> str:
    """
    Get fantasy team name for a player.

    Args:
        player: FantasyPlayer object

    Returns:
        Team name string if player is drafted, empty string otherwise
    """
    # Build normalized player key (same format as apply_drafted_state_to_players)
    player_info = f"{player.name} {player.position} - {player.team}"
    player_key = self._normalize_player_info(player_info)

    # Look up in drafted_players dict
    return self.drafted_players.get(player_key, "")
```

### QA CHECKPOINT 1: Infrastructure Ready
- **Status:** [ ] Not started
- **Expected outcome:** Config settings exist, DraftedRosterManager method works
- **Test command:** `python -m pytest tests/player-data-fetcher/utils/test_DraftedRosterManager.py -v -k get_team_name`
- **Verify:**
  - [ ] Unit tests pass
  - [ ] Method returns correct team name for drafted players
  - [ ] Method returns empty string for free agents
  - [ ] Config settings accessible from config.py
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 2: Core Export Logic

### Task 2.1: Create export_position_json_files() method in DataExporter
- **File:** `player-data-fetcher/player_data_exporter.py`
- **Location:** After export_all_formats_with_teams() (around line 365)
- **Similar to:** export_all_formats() method (lines 336-365)
- **Tests:** `tests/player-data-fetcher/test_player_data_exporter.py`
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ REQUIREMENT 1: Async method that exports all 6 position files
  - Spec: specs.md lines 14-19, reusable patterns
  - Signature: `async def export_position_json_files(self, data: ProjectionData) -> List[str]`
  - Exports: QB, RB, WR, TE, K, DST files
  - Returns: List of file paths created
  - NOT: Synchronous method ❌

✓ REQUIREMENT 2: Uses asyncio.gather() for parallel export
  - Spec: specs.md Reusable Pattern 1
  - Pattern: Create tasks list, await asyncio.gather(*tasks)
  - Uses: _export_single_position_json(data, position) helper
  - NOT: Sequential exports ❌

✓ REQUIREMENT 3: Checks CREATE_POSITION_JSON config before running
  - Spec: Decision 1 (enabled by default but should be checkable)
  - Logic: if not CREATE_POSITION_JSON: return []
  - Returns: Empty list if disabled
  - NOT: Always runs regardless of config ❌

✓ REQUIREMENT 4: Creates output folder if doesn't exist
  - Spec: specs.md output location
  - Folder: POSITION_JSON_OUTPUT path
  - Uses: Path.mkdir(parents=True, exist_ok=True)
  - NOT: Crashes if folder doesn't exist ❌

**Implementation details:**
```python
async def export_position_json_files(self, data: ProjectionData) -> List[str]:
    """
    Export position-based JSON files concurrently.

    Creates 6 JSON files (one per position) in POSITION_JSON_OUTPUT folder.

    Args:
        data: ProjectionData containing player data

    Returns:
        List of file paths created (empty if CREATE_POSITION_JSON=False)
    """
    if not CREATE_POSITION_JSON:
        self.logger.info("Position JSON export disabled (CREATE_POSITION_JSON=False)")
        return []

    # Ensure output folder exists
    output_path = Path(POSITION_JSON_OUTPUT)
    output_path.mkdir(parents=True, exist_ok=True)

    # Create tasks for parallel export
    tasks = []
    for position in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:
        tasks.append(self._export_single_position_json(data, position))

    # Execute concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions, log them, return successful paths
    file_paths = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            position = ['QB', 'RB', 'WR', 'TE', 'K', 'DST'][i]
            self.logger.error(f"Failed to export {position} data: {result}", exc_info=result)
        else:
            file_paths.append(result)

    return file_paths
```

### Task 2.2: Create _export_single_position_json() helper method
- **File:** `player-data-fetcher/player_data_exporter.py`
- **Tests:** `tests/player-data-fetcher/test_player_data_exporter.py`
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ REQUIREMENT 1: Filters players by position
  - Spec: specs.md lines 14-19
  - Filter: position_players = [p for p in all_players if p.position == position]
  - Uses: FantasyPlayer.position attribute
  - NOT: Includes players from other positions ❌

✓ REQUIREMENT 2: Transforms each player to JSON structure
  - Spec: specs.md Complete Data Structures section
  - Calls: _prepare_position_json_data(player, position) for each player
  - Structure: Different per position (QB vs K vs DST)
  - NOT: All positions have same structure ❌

✓ REQUIREMENT 3: Wraps in position-specific root key
  - Spec: specs.md example files analysis
  - Format: {"qb_data": [players]} or {"rb_data": [players]}
  - Key: f"{position.lower()}_data"
  - NOT: Just array without root key ❌

✓ REQUIREMENT 4: Saves to timestamped file using DataFileManager
  - Spec: specs.md Reusable Pattern 3
  - File: self.file_manager.save_json_data(prefix, data)
  - Prefix: f"new_{position.lower()}_data"
  - NOT: Overwrites same file without timestamp ❌

**Implementation details:**
```python
async def _export_single_position_json(self, data: ProjectionData, position: str) -> str:
    """Export JSON file for a single position."""
    # Get all fantasy players with drafted state applied
    fantasy_players = self.get_fantasy_players(data)

    # Filter to position
    position_players = [p for p in fantasy_players if p.position == position]

    # Transform to JSON structure
    players_json = []
    for player in position_players:
        player_json = self._prepare_position_json_data(player, position)
        players_json.append(player_json)

    # Wrap in position-specific root key
    root_key = f"{position.lower()}_data"
    output_data = {root_key: players_json}

    # Save using DataFileManager
    prefix = f"new_{position.lower()}_data"
    file_path = self.file_manager.save_json_data(prefix, output_data, create_latest=False)

    self.logger.info(f"Exported {len(players_json)} {position} players to {file_path}")
    return file_path
```

### Task 2.3: Create _prepare_position_json_data() transformation method
- **File:** `player-data-fetcher/player_data_exporter.py`
- **Tests:** `tests/player-data-fetcher/test_player_data_exporter.py`
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ REQUIREMENT 1: All common fields populated correctly
  - Spec: specs.md lines 24-35
  - Fields: id, name, team, position, injury_status, drafted_by, locked, average_draft_position, player_rating
  - Types: Correct (number, string, boolean)
  - NOT: Missing any common fields ❌

✓ REQUIREMENT 2: drafted_by uses get_team_name_for_player()
  - Spec: Decision 10
  - Logic: self.drafted_roster_manager.get_team_name_for_player(player)
  - Returns: Empty string for FA, team name for drafted
  - NOT: Uses player.drafted integer value ❌

✓ REQUIREMENT 3: locked is boolean (not 0/1)
  - Spec: Decision from transformation table
  - Transform: bool(player.locked)
  - Type: true/false boolean
  - NOT: 0/1 integer ❌

✓ REQUIREMENT 4: projected_points array has exactly 17 elements
  - Spec: Decision 2 (17 elements)
  - Source: player.week_1_points through player.week_17_points
  - Format: [week_1, week_2, ..., week_17]
  - NOT: 18 elements or variable length ❌

✓ REQUIREMENT 5: actual_points uses statSourceId=0 for past weeks, 0 for future
  - Spec: Decision 5, Decision 8
  - Logic: if week <= CURRENT_NFL_WEEK: use actual, else: 0
  - Source: ESPN API statSourceId=0
  - NOT: All zeros or all projections ❌

✓ REQUIREMENT 6: Position-specific stat arrays included
  - Spec: specs.md Complete Data Structures
  - QB: passing, rushing, receiving, misc
  - RB: rushing, receiving, misc
  - WR: receiving, rushing, misc
  - TE: receiving, misc
  - K: extra_points, field_goals
  - DST: defense
  - NOT: All positions have same stats ❌

✓ REQUIREMENT 7: Stat arrays use correct stat IDs
  - Spec: specs.md ESPN Stat ID Mappings
  - Source: FINAL_STAT_RESEARCH_COMPLETE.md
  - Example: stat_1 (completions), stat_0 (attempts)
  - NOT: Wrong stat IDs ❌

✓ REQUIREMENT 8: Non-DST positions do NOT include ret_yds/ret_tds
  - Spec: Decision 6
  - Applies to: QB, RB, WR, TE, K
  - misc section: Only fumbles and two_pt
  - NOT: Has ret_yds/ret_tds in misc ❌

✓ REQUIREMENT 9: Field goal structure simplified to made/missed only
  - Spec: Decision 7
  - Structure: {"made": [], "missed": []}
  - Stat IDs: stat_83 (made), stat_85 (missed)
  - NOT: Distance breakdowns ❌

✓ REQUIREMENT 10: All field names use correct spelling
  - Spec: Decision 3, Decision 4
  - Correct: "receiving" (not "recieving")
  - Correct: "two_pt" (not "2_pt")
  - NOT: Has typos from example files ❌

**Implementation details:**
(This is a large method - will create helper methods for stat extraction)

### Task 2.4: Create stat extraction helper methods
- **File:** `player-data-fetcher/player_data_exporter.py`
- **Tests:** `tests/player-data-fetcher/test_player_data_exporter.py`
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ REQUIREMENT 1: _extract_weekly_stat_array(player_data, stat_id, weeks=17)
  - Purpose: Extract single stat for all weeks
  - Logic: For each week 1-17, get stat from ESPN API
  - Returns: List[float] with exactly 17 elements
  - Uses: statSourceId=0 for weeks <= CURRENT_NFL_WEEK, 0 for future
  - NOT: Returns variable length arrays ❌

✓ REQUIREMENT 2: _extract_passing_stats(player_data) -> dict
  - Returns: {"completions": [], "attempts": [], "pass_yds": [], "pass_tds": [], "interceptions": [], "sacks": []}
  - Stat IDs: stat_1, stat_0, stat_3, stat_4, stat_20, stat_64
  - NOT: Missing any passing stats ❌

✓ REQUIREMENT 3: _extract_rushing_stats(player_data) -> dict
  - Returns: {"attempts": [], "rush_yds": [], "rush_tds": []}
  - Stat IDs: stat_23, stat_24, stat_25
  - NOT: Missing any rushing stats ❌

✓ REQUIREMENT 4: _extract_receiving_stats(player_data) -> dict
  - Returns: {"targets": [], "receiving_yds": [], "receiving_tds": [], "receptions": []}
  - Stat IDs: stat_58, stat_42, stat_43, stat_53
  - Spelling: "receiving" (not "recieving")
  - NOT: Has typo in field names ❌

✓ REQUIREMENT 5: _extract_misc_stats(player_data, include_return_stats=False) -> dict
  - Returns: {"fumbles": [], "two_pt": []} for non-DST
  - Returns: {"fumbles": [], "two_pt": [], "ret_yds": [], "ret_tds": []} for DST (when include_return_stats=True)
  - Stat IDs: stat_68 (fumbles), stat_19/26/44/62 (two_pt), stat_114+115 (ret_yds), stat_101+102 (ret_tds)
  - NOT: Always includes return stats ❌

✓ REQUIREMENT 6: _extract_kicking_stats(player_data) -> dict
  - Returns: {"extra_points": {"made": [], "missed": []}, "field_goals": {"made": [], "missed": []}}
  - Stat IDs: stat_86 (XP made), stat_88 (XP missed), stat_83 (FG made), stat_85 (FG missed)
  - NOT: Includes distance breakdowns ❌

✓ REQUIREMENT 7: _extract_defense_stats(player_data) -> dict
  - Returns: {"yds_g": [], "pts_g": [], "def_td": [], "sacks": [], "safety": [], "interceptions": [], "forced_fumble": [], "fumbles_recovered": [], "ret_yds": [], "ret_tds": []}
  - Stat IDs: stat_127, stat_120, stat_94, stat_99, stat_98, stat_95, stat_106, stat_96, stat_114+115, stat_101+102
  - NOT: Missing any defense stats ❌

✓ REQUIREMENT 8: All helpers use Decision 11 (missing stats = 0)
  - Logic: .get(stat_id, 0.0) or similar
  - Never: null, None, or raise exception
  - NOT: Has null values in arrays ❌

**Implementation details:**
(Helper methods to extract stats from ESPN API data structure)

### Task 2.5: Create _get_actual_points_array() method
- **File:** `player-data-fetcher/player_data_exporter.py`
- **Tests:** `tests/player-data-fetcher/test_player_data_exporter.py`
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ REQUIREMENT 1: Returns array with exactly 17 elements
  - Spec: Decision 2
  - Length: 17 (weeks 1-17)
  - NOT: 18 elements or variable ❌

✓ REQUIREMENT 2: Uses actual stats for past weeks
  - Spec: Decision 5, Decision 8
  - Logic: if week <= CURRENT_NFL_WEEK: extract from statSourceId=0
  - Source: ESPN API actual stats
  - NOT: Uses projections for past weeks ❌

✓ REQUIREMENT 3: Uses 0 for future weeks
  - Spec: Decision 9
  - Logic: if week > CURRENT_NFL_WEEK: 0.0
  - NOT: Uses projections or null ❌

✓ REQUIREMENT 4: Never includes null values
  - Spec: Decision 11
  - Missing data: 0.0
  - NOT: null, None, or empty ❌

**Implementation details:**
```python
def _get_actual_points_array(self, player_data) -> List[float]:
    """
    Get actual points array with 17 elements.

    Uses actual stats (statSourceId=0) for weeks <= CURRENT_NFL_WEEK,
    zeros for future weeks.
    """
    actual_points = []
    for week in range(1, 18):  # Weeks 1-17
        if week <= CURRENT_NFL_WEEK:
            # Extract from ESPN API statSourceId=0
            points = self._extract_actual_points_for_week(player_data, week)
        else:
            # Future week
            points = 0.0
        actual_points.append(points)
    return actual_points
```

### QA CHECKPOINT 2: Export Logic Complete
- **Status:** [ ] Not started
- **Expected outcome:** Can generate position JSON files with correct structure
- **Test command:** `python -m pytest tests/player-data-fetcher/test_player_data_exporter.py -v -k position_json`
- **Verify:**
  - [ ] Unit tests pass
  - [ ] All 6 position files created
  - [ ] JSON structure matches specs
  - [ ] All arrays have 17 elements
  - [ ] No null values in arrays
  - [ ] Non-DST files don't have ret_yds/ret_tds
  - [ ] Field goal structure simplified
  - [ ] Correct spelling ("receiving", "two_pt")
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Phase 3: Integration

### Task 3.1: Integrate into main workflow
- **File:** `player-data-fetcher/player_data_fetcher_main.py`
- **Location:** After team data exports in main()
- **Tests:** Integration test
- **Status:** [ ] Not started

**ACCEPTANCE CRITERIA (from specs.md):**

✓ REQUIREMENT 1: Call export_position_json_files() if enabled
  - Logic: if CREATE_POSITION_JSON: await exporter.export_position_json_files(data)
  - Location: After existing exports
  - NOT: Always calls or never calls ❌

✓ REQUIREMENT 2: Log file paths created
  - Logs: File paths returned from export method
  - Level: INFO
  - NOT: Silent export ❌

**Implementation details:**
Add to main() after team data exports, conditional on config toggle.

---

## Phase 4: Testing

### Task 4.1: Unit tests for DraftedRosterManager.get_team_name_for_player()
- **File:** `tests/player-data-fetcher/utils/test_DraftedRosterManager.py`
- **Status:** [ ] Not started

**Test cases:**
- Player drafted by team 1: returns team name
- Player drafted by MY_TEAM_NAME: returns MY_TEAM_NAME
- Free agent (drafted=0): returns empty string
- Player not in drafted_data.csv: returns empty string
- Player with special characters in name: normalizes and finds match

### Task 4.2: Unit tests for position JSON export methods
- **File:** `tests/player-data-fetcher/test_player_data_exporter.py`
- **Status:** [ ] Not started

**Test cases:**
- export_position_json_files() creates all 6 files
- CREATE_POSITION_JSON=False: no files created
- Each position has correct structure
- Arrays all have 17 elements
- No null values in arrays
- Non-DST positions don't have ret_yds/ret_tds
- Field goals simplified (no distance breakdown)
- Correct spelling ("receiving", "two_pt")
- drafted_by field correct (empty string for FA, team name for drafted)
- locked is boolean (not 0/1)

### Task 4.3: Integration test for full workflow
- **File:** `tests/player-data-fetcher/integration/test_position_json_export.py`
- **Status:** [ ] Not started

**Test case:**
- Run full player-data-fetcher with CREATE_POSITION_JSON=True
- Verify all 6 position files created
- Verify files can be loaded as JSON
- Verify structure matches specs
- Spot-check player data accuracy

### Task 4.4: Manual QC validation
- **File:** Manual testing notes in lessons_learned.md
- **Status:** [ ] Not started

**QC Requirements (from specs.md):**
- [ ] All arrays have exactly 17 elements
- [ ] Unplayed weeks (Week 17) have 0 values
- [ ] Check 3-5 players per position against internet sources:
  - [ ] QB: Trevor Lawrence (if available)
  - [ ] RB: Check multiple RBs
  - [ ] WR: Check multiple WRs
  - [ ] TE: Travis Kelce (if available)
  - [ ] K: Brandon Aubrey (if available)
  - [ ] DST: Eagles D/ST (if available)
- [ ] Verify fields match for at least Week 1 and Week 16 (actual data)
- [ ] Verify Week 17 is all zeros (not yet played as of 2025-12-24)

### QA CHECKPOINT 3: All Tests Pass
- **Status:** [ ] Not started
- **Expected outcome:** 100% test pass rate
- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] All unit tests pass (100%)
  - [ ] Integration tests pass
  - [ ] Manual QC validation complete
  - [ ] No null values found
  - [ ] Array lengths correct
  - [ ] Data accuracy verified
- **If checkpoint fails:** STOP, fix issue, document in lessons learned, then re-run

---

## Interface Contracts (Verified Pre-Implementation)

### DraftedRosterManager
- **Method:** `apply_drafted_state_to_players(players: List[FantasyPlayer]) -> List[FantasyPlayer]`
- **Source:** `player-data-fetcher/utils/DraftedRosterManager.py` (existing)
- **Existing usage:** `player_data_exporter.py:328`
- **Verified:** [ ] (will verify during Interface Verification Protocol)

### DraftedRosterManager.drafted_players
- **Attribute:** `drafted_players` - Dict[str, str] mapping normalized player key to team name
- **Type:** dict
- **Source:** `player-data-fetcher/utils/DraftedRosterManager.py`
- **Note:** Populated by load_drafted_data(), keys are normalized player info strings
- **Verified:** [ ]

### FantasyPlayer
- **Attributes:**
  - `name` (str)
  - `position` (str)
  - `team` (str)
  - `drafted` (int) - 0=FA, 1=opponent, 2=my_team
  - `locked` (int) - 0/1
  - `week_1_points` through `week_17_points` (float or None)
- **Source:** `utils/FantasyPlayer.py`
- **Note:** projected points, NOT actual
- **Verified:** [ ]

### ESPNPlayerData
- **Attributes:**
  - `week_1_points` through `week_17_points` - weekly projections
  - `stats` - array with statSourceId (0=actual, 1=projected)
- **Source:** `player-data-fetcher/player_data_models.py`
- **Verified:** [ ]

### DataFileManager
- **Method:** `save_json_data(prefix: str, data: dict, create_latest: bool = True) -> str`
- **Source:** `player-data-fetcher/data_file_manager.py`
- **Returns:** File path created
- **Verified:** [ ]

### Quick E2E Validation Plan
- **Minimal test command:** `python -m pytest tests/player-data-fetcher/test_player_data_exporter.py::test_export_position_json_files -v`
- **Expected result:** Test passes, creates 6 JSON files in /data/player_data/
- **Run before:** Full implementation begins
- **Status:** [ ] Not run

---

## Integration Matrix

| New Component | File | Called By | Caller File:Line | Caller Modification Task |
|---------------|------|-----------|------------------|--------------------------|
| get_team_name_for_player() | DraftedRosterManager.py | _prepare_position_json_data() | player_data_exporter.py:TBD | Task 2.3 |
| export_position_json_files() | player_data_exporter.py | main() | player_data_fetcher_main.py:TBD | Task 3.1 |
| _export_single_position_json() | player_data_exporter.py | export_position_json_files() | player_data_exporter.py:TBD | Task 2.1 |
| _prepare_position_json_data() | player_data_exporter.py | _export_single_position_json() | player_data_exporter.py:TBD | Task 2.2 |
| _extract_weekly_stat_array() | player_data_exporter.py | stat extraction methods | player_data_exporter.py:TBD | Task 2.4 |
| _extract_passing_stats() | player_data_exporter.py | _prepare_position_json_data() | player_data_exporter.py:TBD | Task 2.4 |
| _extract_rushing_stats() | player_data_exporter.py | _prepare_position_json_data() | player_data_exporter.py:TBD | Task 2.4 |
| _extract_receiving_stats() | player_data_exporter.py | _prepare_position_json_data() | player_data_exporter.py:TBD | Task 2.4 |
| _extract_misc_stats() | player_data_exporter.py | _prepare_position_json_data() | player_data_exporter.py:TBD | Task 2.4 |
| _extract_kicking_stats() | player_data_exporter.py | _prepare_position_json_data() | player_data_exporter.py:TBD | Task 2.4 |
| _extract_defense_stats() | player_data_exporter.py | _prepare_position_json_data() | player_data_exporter.py:TBD | Task 2.4 |
| _get_actual_points_array() | player_data_exporter.py | _prepare_position_json_data() | player_data_exporter.py:TBD | Task 2.5 |

---

## Algorithm Traceability Matrix

**Purpose:** Map every algorithm in specs to exact TODO task and implementation location

| Spec Section | Algorithm Description | TODO Task | Code Location | Conditional Logic | Acceptance Criteria |
|--------------|----------------------|-----------|---------------|-------------------|---------------------|
| Decision 2 | Array length = 17 elements | ALL tasks | All array creation | len(array) == 17 | Task 2.3 REQ-4, Task 2.4 REQ-1, Task 2.5 REQ-1 |
| Decision 5 | Array population: actual for past, zeros for future | Task 2.5 | _get_actual_points_array() | if week <= CURRENT_NFL_WEEK: use actual else: 0 | Task 2.5 REQ-2, REQ-3 |
| Decision 8 | Stat arrays use statSourceId=0 for past weeks | Task 2.4 | _extract_weekly_stat_array() | if week <= CURRENT_NFL_WEEK: extract statSourceId=0 | Task 2.4 REQ-1, REQ-8 |
| Decision 9 | Stat arrays use 0 for future weeks | Task 2.4 | _extract_weekly_stat_array() | if week > CURRENT_NFL_WEEK: 0.0 | Task 2.4 REQ-1, REQ-5 |
| Decision 10 | drafted_by mapping algorithm | Task 1.2, Task 2.3 | get_team_name_for_player() | if drafted==0: "", elif drafted==2: MY_TEAM_NAME, else: lookup | Task 1.2 REQ-1, REQ-2, REQ-3 |
| Decision 11 | Missing stats always use 0 | Task 2.4, Task 2.5 | All stat extraction | stat.get(id, 0.0) | Task 2.4 REQ-8, Task 2.5 REQ-4 |
| Transformation table | locked: 0/1 → false/true | Task 2.3 | _prepare_position_json_data() | bool(player.locked) | Task 2.3 REQ-3 |
| Transformation table | drafted: 0/1/2 → drafted_by string | Task 2.3 | _prepare_position_json_data() | Call get_team_name_for_player() | Task 2.3 REQ-2 |
| Transformation table | week columns → projected_points array | Task 2.3 | _prepare_position_json_data() | [week_1_points, ..., week_17_points] | Task 2.3 REQ-4 |
| Transformation table | week columns → actual_points array | Task 2.5 | _get_actual_points_array() | Extract from statSourceId=0 | Task 2.3 REQ-5, Task 2.5 REQ-2 |
| Decision 3 | Spelling: "receiving" not "recieving" | Task 2.4 | _extract_receiving_stats() | Field names in dict | Task 2.3 REQ-10, Task 2.4 REQ-4 |
| Decision 4 | Key naming: "two_pt" not "2_pt" | Task 2.4 | _extract_misc_stats() | Field name in dict | Task 2.3 REQ-10 |
| Decision 6 | Remove ret_yds/ret_tds from non-DST | Task 2.4 | _extract_misc_stats() | if include_return_stats==False: omit fields | Task 2.3 REQ-8, Task 2.4 REQ-5 |
| Decision 7 | Field goals simplified to made/missed | Task 2.4 | _extract_kicking_stats() | {"made": [], "missed": []} only | Task 2.3 REQ-9, Task 2.4 REQ-6 |
| Position filtering | Filter players by position | Task 2.2 | _export_single_position_json() | [p for p in players if p.position == position] | Task 2.2 REQ-1 |
| Root key wrapping | Wrap in position-specific root key | Task 2.2 | _export_single_position_json() | {f"{position.lower()}_data": players} | Task 2.2 REQ-3 |
| Async export pattern | Parallel export of 6 positions | Task 2.1 | export_position_json_files() | asyncio.gather(*tasks) | Task 2.1 REQ-2 |
| Config toggle | Check CREATE_POSITION_JSON before export | Task 2.1 | export_position_json_files() | if not CREATE_POSITION_JSON: return [] | Task 2.1 REQ-3 |
| Folder creation | Create output folder if missing | Task 2.1 | export_position_json_files() | Path.mkdir(parents=True, exist_ok=True) | Task 2.1 REQ-4 |
| ESPN Stat IDs | Map stat IDs to field names | Task 2.4 | All _extract_*_stats() | stat_0=attempts, stat_1=completions, etc. | Task 2.3 REQ-7, Task 2.4 all REQs |
| Normalization | Normalize player key for lookup | Task 1.2 | get_team_name_for_player() | self._normalize_player_info(player_info) | Task 1.2 REQ-3 |
| Position-specific stats | Different stats per position | Task 2.3 | _prepare_position_json_data() | if position == "QB": passing+rushing+receiving+misc, elif position == "K": kicking, etc. | Task 2.3 REQ-6 |

**Coverage Verification:**
- ✅ All 11 user decisions mapped to tasks
- ✅ All transformation rules mapped
- ✅ All conditional logic documented
- ✅ All acceptance criteria cross-referenced

### Iteration 4a - TODO Specification Audit (4-Part Audit)

**Part 1: Acceptance Criteria Completeness**

Audit each task's acceptance criteria against specs.md:

| Task | Acceptance Criteria Count | Spec Requirements | Complete? | Gaps Found |
|------|---------------------------|-------------------|-----------|------------|
| 1.1 (config settings) | 2 REQs | 2 from Decision 1, specs lines 60-61 | ✅ YES | None |
| 1.2 (get_team_name_for_player) | 3 REQs | 3 from Decision 10 | ✅ YES | None |
| 2.1 (export_position_json_files) | 4 REQs | 4 from specs Reusable Pattern 1 + Decision 1 | ✅ YES | None |
| 2.2 (_export_single_position_json) | 4 REQs | 4 from specs lines 14-19 + patterns | ✅ YES | None |
| 2.3 (_prepare_position_json_data) | 10 REQs | 10 from specs Complete Data Structures | ✅ YES | None |
| 2.4 (stat extraction helpers) | 8 REQs (7 methods + 1 general) | 31 stat IDs + all decisions | ✅ YES | None |
| 2.5 (_get_actual_points_array) | 4 REQs | 4 from Decision 5, 8, 9, 11 | ✅ YES | None |
| 3.1 (main integration) | 2 REQs | 2 from specs integration notes | ✅ YES | None |

**Total:** 37 acceptance criteria covering all spec requirements ✅

**Part 2: Ambiguity Detection**

Review each acceptance criterion for ambiguous language:

| Task | Criterion | Ambiguity Check | Resolution |
|------|-----------|-----------------|------------|
| 2.3 REQ-5 | "actual_points uses statSourceId=0 for past weeks" | ❓ What is "past weeks"? | ✅ RESOLVED: week <= CURRENT_NFL_WEEK (Decision 5) |
| 2.3 REQ-6 | "Position-specific stat arrays included" | ❓ Which stats for which position? | ✅ RESOLVED: specs.md Complete Data Structures documents exact stats |
| 2.4 REQ-1 | "_extract_weekly_stat_array returns exactly 17 elements" | ✅ CLEAR | No ambiguity |
| 2.4 REQ-5 | "include_return_stats parameter" | ✅ CLEAR | Boolean, default False |
| All criteria | Use of "0" vs "0.0" | ❓ Type consistency | ✅ RESOLVED: Use 0.0 (float) for arrays |

**No blocking ambiguities found.** Minor clarifications added above.

**Part 3: Contradiction Check**

Cross-check acceptance criteria for contradictions:

| Criterion A | Criterion B | Potential Conflict | Resolution |
|-------------|-------------|-------------------|------------|
| Task 2.3 REQ-4: "projected_points array has exactly 17 elements" | Task 2.3 REQ-5: "actual_points uses statSourceId=0" | ✅ NO CONFLICT | Different arrays, both 17 elements |
| Task 2.4 REQ-8: "Always use 0" | Task 2.3 REQ-7: "Stat arrays use correct stat IDs" | ✅ NO CONFLICT | Use stat IDs when present, 0 when missing |
| Task 2.1 REQ-2: "Uses asyncio.gather()" | Task 2.1 REQ-3: "Checks CREATE_POSITION_JSON config" | ✅ NO CONFLICT | Check config first, then gather if enabled |
| Decision 6: "Remove ret_yds from non-DST" | Task 2.4 REQ-5: "include_return_stats parameter" | ✅ NO CONFLICT | Parameter controls inclusion (True for DST only) |

**No contradictions found.** All criteria are consistent.

**Part 4: Spec Coverage Verification**

Verify every requirement in specs.md is covered by TODO acceptance criteria:

| Spec Requirement | Spec Location | TODO Task | Acceptance Criteria | Covered? |
|------------------|---------------|-----------|---------------------|----------|
| 6 position files (QB, RB, WR, TE, K, DST) | specs.md lines 14-19 | Task 2.1 | REQ-1 | ✅ |
| Output location: /data/player_data/ | specs.md lines 12-13 | Task 2.1 | REQ-4 | ✅ |
| Config toggle CREATE_POSITION_JSON = True | Decision 1 | Task 1.1 | REQ-1 | ✅ |
| Config default: True | Decision 1 | Task 1.1 | REQ-1 | ✅ |
| All common fields (9 fields) | specs.md lines 24-35 | Task 2.3 | REQ-1 | ✅ |
| drafted_by transformation | Transformation table | Task 2.3 | REQ-2 | ✅ |
| locked boolean transformation | Transformation table | Task 2.3 | REQ-3 | ✅ |
| projected_points array (17 elements) | Decision 2 | Task 2.3 | REQ-4 | ✅ |
| actual_points array (17 elements) | Decision 2 | Task 2.3, 2.5 | REQ-5, Task 2.5 REQ-1 | ✅ |
| Position-specific stats | specs.md Complete Data Structures | Task 2.3 | REQ-6 | ✅ |
| Stat IDs correct (31 stats) | specs.md ESPN Stat ID Mappings | Task 2.3, 2.4 | REQ-7, Task 2.4 all | ✅ |
| Non-DST no ret_yds/ret_tds | Decision 6 | Task 2.3, 2.4 | REQ-8, Task 2.4 REQ-5 | ✅ |
| Field goals simplified | Decision 7 | Task 2.3, 2.4 | REQ-9, Task 2.4 REQ-6 | ✅ |
| Correct spelling ("receiving", "two_pt") | Decision 3, 4 | Task 2.3, 2.4 | REQ-10, Task 2.4 REQ-4 | ✅ |
| Array population logic | Decision 5, 8, 9 | Task 2.4, 2.5 | Multiple REQs | ✅ |
| Missing stats = 0 | Decision 11 | Task 2.4, 2.5 | REQ-8 (Task 2.4), REQ-4 (Task 2.5) | ✅ |
| get_team_name_for_player() method | Decision 10 | Task 1.2 | All 3 REQs | ✅ |
| Async export pattern | specs Reusable Pattern 1 | Task 2.1 | REQ-2 | ✅ |
| Position filtering | specs lines 14-19 | Task 2.2 | REQ-1 | ✅ |
| Root key wrapping | specs example files | Task 2.2 | REQ-3 | ✅ |
| Integration into main workflow | Implementation Notes | Task 3.1 | Both REQs | ✅ |
| QC: 17 elements | specs.md QC Requirements | Task 4.2 | Test case | ✅ |
| QC: No null values | specs.md QC Requirements | Task 4.2 | Test case | ✅ |
| QC: Manual validation | specs.md QC Requirements | Task 4.4 | All checkboxes | ✅ |

**Spec Coverage:** 100% ✅ All requirements from specs.md covered by TODO acceptance criteria.

**Audit Summary:**
- ✅ Part 1: All tasks have complete acceptance criteria
- ✅ Part 2: No blocking ambiguities (minor clarifications added)
- ✅ Part 3: No contradictions found
- ✅ Part 4: 100% spec coverage verified

**Confidence Level:** HIGH - TODO is ready for implementation

---

## Data Flow Traces

### Iteration 5 - End-to-End Data Flow (COMPLETE ✅)

**Complete Data Flow: Entry Point → Position JSON Files**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ENTRY POINT: run_player_fetcher.py                                          │
│   └─► Imports and calls: player_data_fetcher_main.py                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ player_data_fetcher_main.py:main()                                          │
│   1. Create NFLProjectionsCollector                                         │
│   2. await collector.collect_all_projections()                              │
│      └─► ESPN API calls → ProjectionData (List[ESPNPlayerData])            │
│   3. await collector.export_data()                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ player_data_fetcher_main.py:export_data()                                   │
│   └─► Line 343: await exporter.export_all_formats_with_teams(data, ...)    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ player_data_exporter.py:export_all_formats_with_teams()                     │
│   1. Create tasks list                                                      │
│   2. if create_json: tasks.append(self.export_json(data))                  │
│   3. if create_csv: tasks.append(self.export_csv(data))                    │
│   4. tasks.append(self.export_to_data(data))  # Always                     │
│   5. tasks.append(self.export_teams_csv(data))                             │
│   6. tasks.append(self.export_teams_to_data(data))                         │
│   7. **NEW**: if CREATE_POSITION_JSON:                                     │
│      tasks.append(self.export_position_json_files(data))  ← TASK 3.1       │
│   8. results = await asyncio.gather(*tasks)                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK 2.1: export_position_json_files(data: ProjectionData) → List[str]     │
│   1. if not CREATE_POSITION_JSON: return []                                │
│   2. output_path = Path(POSITION_JSON_OUTPUT)                              │
│   3. output_path.mkdir(parents=True, exist_ok=True)                        │
│   4. tasks = []                                                             │
│   5. for position in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']:                │
│      tasks.append(self._export_single_position_json(data, position))       │
│   6. results = await asyncio.gather(*tasks, return_exceptions=True)        │
│   7. Log exceptions, return successful paths                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ (6 parallel tasks)
┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK 2.2: _export_single_position_json(data, position) → str               │
│   1. fantasy_players = self.get_fantasy_players(data)                      │
│      └─► player_data_exporter.py:323 (existing method)                    │
│          ├─► Convert ESPNPlayerData to FantasyPlayer                       │
│          └─► Apply drafted state via DraftedRosterManager                  │
│   2. position_players = [p for p in fantasy_players if p.position == pos] │
│   3. players_json = []                                                      │
│   4. for player in position_players:                                        │
│      player_json = self._prepare_position_json_data(player, position)      │
│      players_json.append(player_json)                                       │
│   5. output_data = {f"{position.lower()}_data": players_json}              │
│   6. file_path = self.file_manager.save_json_data(data, prefix, False)    │
│   7. return str(timestamped_path)                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ (for each player)
┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK 2.3: _prepare_position_json_data(player, position) → dict             │
│   1. Common fields:                                                         │
│      ├─► id: player.id                                                     │
│      ├─► name: player.name                                                 │
│      ├─► team: player.team                                                 │
│      ├─► position: player.position                                         │
│      ├─► injury_status: player.injury_status                               │
│      ├─► drafted_by: self.drafted_roster_manager.                         │
│      │                get_team_name_for_player(player) ← TASK 1.2          │
│      ├─► locked: bool(player.locked)                                       │
│      ├─► average_draft_position: player.adp                                │
│      └─► player_rating: player.rating                                      │
│   2. projected_points: [player.week_1_points, ..., week_17_points]        │
│   3. actual_points: self._get_actual_points_array(player) ← TASK 2.5      │
│   4. Position-specific stats:                                               │
│      if position == "QB":                                                   │
│         ├─► passing: self._extract_passing_stats(player) ← TASK 2.4       │
│         ├─► rushing: self._extract_rushing_stats(player)                   │
│         ├─► receiving: self._extract_receiving_stats(player)               │
│         └─► misc: self._extract_misc_stats(player, False)                  │
│      elif position == "K":                                                  │
│         └─► kicking: self._extract_kicking_stats(player)                   │
│      elif position == "DST":                                                │
│         └─► defense: self._extract_defense_stats(player)                   │
│      ...                                                                    │
│   5. return player_json dict                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
          ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
          │ TASK 1.2:    │ │ TASK 2.5:   │ │ TASK 2.4:    │
          │ get_team_    │ │ _get_actual_│ │ _extract_*   │
          │ name_for_    │ │ points_     │ │ _stats()     │
          │ player()     │ │ array()     │ │ methods      │
          └──────────────┘ └─────────────┘ └──────────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                            All data combined
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ DataFileManager.save_json_data(data, prefix, create_latest=False)          │
│   └─► Write to: /data/player_data/new_{position}_data_TIMESTAMP.json      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ OUTPUT: 6 JSON files in /data/player_data/                                 │
│   ├─► new_qb_data_20251224_HHMMSS.json                                    │
│   ├─► new_rb_data_20251224_HHMMSS.json                                    │
│   ├─► new_wr_data_20251224_HHMMSS.json                                    │
│   ├─► new_te_data_20251224_HHMMSS.json                                    │
│   ├─► new_k_data_20251224_HHMMSS.json                                     │
│   └─► new_dst_data_20251224_HHMMSS.json                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Data Transformations at Each Stage:**

| Stage | Input | Transformation | Output |
|-------|-------|----------------|--------|
| ESPN API | Raw API response | Parse JSON | ESPNPlayerData objects |
| get_fantasy_players() | List[ESPNPlayerData] | Convert to FantasyPlayer, apply drafted state | List[FantasyPlayer] |
| _export_single_position_json() | List[FantasyPlayer] | Filter by position | List[FantasyPlayer] (single position) |
| _prepare_position_json_data() | FantasyPlayer | Transform to JSON dict structure | dict (player JSON) |
| get_team_name_for_player() | FantasyPlayer | drafted (0/1/2) → drafted_by (string) | str |
| _get_actual_points_array() | FantasyPlayer + ESPN data | Week-by-week stats → 17-element array | List[float] |
| _extract_*_stats() | FantasyPlayer + ESPN data | Stat IDs → named fields in arrays | dict with arrays |
| save_json_data() | dict | Serialize to JSON | JSON file on disk |

**Critical Dependencies:**

1. **CURRENT_NFL_WEEK** (from config.py) - determines which weeks get actual vs 0 values
2. **drafted_data.csv** - source of drafted_by team names
3. **ESPN API statSourceId** - 0=actual, 1=projected
4. **ESPN Stat IDs** - 31 stat IDs map to field names
5. **DraftedRosterManager.drafted_players** - Dict[str, str] for team lookups

**Data Flow Verification:**
- ✅ Entry point identified: run_player_fetcher.py
- ✅ All transformation steps documented
- ✅ Output location confirmed: /data/player_data/
- ✅ All dependencies identified
- ✅ No circular dependencies
- ✅ No data loss in transformations

### Requirement: Position JSON Export
```
Entry: TBD
  → TBD
  → Output: TBD
```

---

## Verification Gaps

### Iteration 1 - Files & Patterns (COMPLETE ✅)

**Files Verified:**
- ✅ config.py - Lines 25-31 correct location for new settings
- ✅ DraftedRosterManager.py - Located at utils/DraftedRosterManager.py (ROOT utils, not player-data-fetcher/utils)
- ✅ player_data_exporter.py - Line 365 end of export_all_formats(), good insertion point
- ✅ player_data_fetcher_main.py - Line 343 calls export_all_formats_with_teams()
- ✅ tests/player-data-fetcher/test_player_data_exporter.py exists

**Patterns Found:**
1. **Async Export Pattern** (lines 336-365 in player_data_exporter.py):
   ```python
   async def export_method(self, data: ProjectionData) -> List[str]:
       tasks = []
       if condition:
           tasks.append(self.helper_method(data))
       results = await asyncio.gather(*tasks, return_exceptions=True)
       # Filter exceptions, log them
       return [path for path in results if isinstance(path, str)]
   ```

2. **Config Toggle Pattern** (lines 27-30 in config.py):
   ```python
   CREATE_CSV = True
   CREATE_JSON = False
   CREATE_EXCEL = False
   ```

3. **DraftedRosterManager Already Imported** (line 29 in player_data_exporter.py):
   - Already have: `from utils.DraftedRosterManager import DraftedRosterManager`
   - Already initialized: Lines 65-67 in __init__

4. **DataFileManager Pattern** (line 48 in player_data_exporter.py):
   - self.file_manager = DataFileManager(str(self.output_dir), DEFAULT_FILE_CAPS)
   - Usage: self.file_manager instance variable available

**Corrections Made:**
- [CORRECTION-1] DraftedRosterManager path: utils/DraftedRosterManager.py (NOT player-data-fetcher/utils/)
- [NOTE-1] DraftedRosterManager already imported - no need to add import
- [NOTE-2] Integration point: export_all_formats_with_teams() at line 523 is the right place to add position JSON export call

### Iteration 2 - Error Handling (COMPLETE ✅)

**Error Handling Pattern Identified (from existing exports):**
```python
try:
    # Operation
    result = do_something()
except PermissionError as e:
    self.logger.error(f"Permission denied writing file: {e}")
    raise
except OSError as e:
    self.logger.error(f"OS error writing file: {e}")
    raise
except (TypeError, ValueError) as e:
    self.logger.error(f"Serialization error: {e}")
    raise
except Exception as e:
    self.logger.error(f"Unexpected error: {e}")
    raise
```

**Required Error Handling for New Code:**

1. **Task 1.2 (get_team_name_for_player):**
   - No try-except needed (uses .get() with default "")
   - Returns empty string on lookup failure (graceful degradation)

2. **Task 2.1 (export_position_json_files):**
   - ✅ Already handled: asyncio.gather(*tasks, return_exceptions=True)
   - Log exceptions from failed position exports
   - Return empty list if CREATE_POSITION_JSON=False (no error)
   - Folder creation: Path.mkdir(parents=True, exist_ok=True) - no try needed

3. **Task 2.2 (_export_single_position_json):**
   - No explicit try-except (let caller handle via gather)
   - Log info on successful export

4. **Task 2.3 (_prepare_position_json_data):**
   - No try-except needed (data transformation, no I/O)
   - Use .get(stat_id, 0.0) pattern for missing stats (no exception)

5. **Task 2.4 (stat extraction helpers):**
   - Use .get() with default 0.0 for missing stats
   - No exceptions raised

6. **Task 2.5 (_get_actual_points_array):**
   - Use .get() pattern for missing data
   - Return 0.0 for missing weeks (no exception)

7. **Task 3.1 (main workflow integration):**
   - Wrapped in export_all_formats_with_teams() try-except already
   - No additional handling needed

**Logging Requirements:**

| Method | Log Level | What to Log |
|--------|-----------|-------------|
| export_position_json_files() | INFO | "Position JSON export disabled" (if CREATE_POSITION_JSON=False) |
| export_position_json_files() | INFO | "Creating position JSON output folder: {path}" |
| export_position_json_files() | ERROR | "{position} export failed: {exception}" (for each failure) |
| _export_single_position_json() | INFO | "Exported {count} {position} players to {file_path}" |
| _prepare_position_json_data() | None | (data transformation, no logging) |
| get_team_name_for_player() | None | (simple lookup, no logging) |

**Missing Data Handling (Decision 11 - always use 0):**
- Missing stat from ESPN API: 0.0
- Future week data: 0.0
- Player not in drafted_data.csv: "" (empty string)
- Stat array element missing: 0.0
- NEVER: null, None, raise exception

### Iteration 3 - Integration Points (COMPLETE ✅)

**Identified Integration Points:**

| New Code | Calls Existing | Location | Verified |
|----------|---------------|----------|----------|
| export_position_json_files() | self.file_manager.save_json_data() | player_data_exporter.py:TBD | ✅ |
| export_position_json_files() | Path.mkdir(parents=True, exist_ok=True) | Built-in | ✅ |
| _export_single_position_json() | self.get_fantasy_players(data) | player_data_exporter.py:323 | ✅ |
| _export_single_position_json() | self.file_manager.save_json_data() | utils/data_file_manager.py:365 | ✅ |
| _prepare_position_json_data() | self.drafted_roster_manager.get_team_name_for_player() | NEW METHOD | ⏳ |
| get_team_name_for_player() | self._normalize_player_info() | DraftedRosterManager.py:existing | ✅ |
| get_team_name_for_player() | self.drafted_players.get() | DraftedRosterManager attribute | ✅ |

| Existing Code | Calls New Code | Location | Task |
|---------------|----------------|----------|------|
| export_all_formats_with_teams() | export_position_json_files() | player_data_exporter.py:540 (after line 556) | 3.1 |
| main() | (calls export_all_formats_with_teams) | player_data_fetcher_main.py:343 | (no change) |

**Interface Signature Corrections:**

[CORRECTION-2] DataFileManager.save_json_data() signature:
```python
def save_json_data(self, data: Any, prefix: str, create_latest: bool = True,
                   **json_kwargs) -> Tuple[Path, Optional[Path]]:
```
**NOT:** `-> str` as assumed in TODO Task 2.2

**Returns:** Tuple[Path, Optional[Path]] (timestamped_path, latest_path)
**Usage:** `timestamped_path, latest_path = self.file_manager.save_json_data(data, prefix, create_latest=False)`

**Test Mocking Requirements:**

| Test | What to Mock | Why |
|------|--------------|-----|
| test_export_position_json_files() | CREATE_POSITION_JSON config | Test enabled/disabled |
| test_export_position_json_files() | self.file_manager.save_json_data | Avoid actual file I/O |
| test_export_position_json_files() | Path.mkdir | Verify folder creation called |
| test_export_single_position_json() | self.get_fantasy_players | Control test data |
| test_export_single_position_json() | self.file_manager.save_json_data | Avoid file I/O |
| test_prepare_position_json_data() | self.drafted_roster_manager.get_team_name_for_player | Control return value |
| test_prepare_position_json_data() | player.week_N_points fields | Control player data |
| test_get_team_name_for_player() | self.drafted_players dict | Control drafted state |
| test_get_team_name_for_player() | self._normalize_player_info | Verify normalization called |

**Reusable Existing Methods (NO changes needed):**
- get_fantasy_players(data): Already converts ProjectionData to List[FantasyPlayer] with drafted state applied
- DraftedRosterManager.__init__(): Already initialized in DataExporter.__init__()
- DraftedRosterManager.apply_drafted_state_to_players(): Already called in get_fantasy_players()

**Key Discovery:**
- Position JSON export should be added to export_all_formats_with_teams() AFTER line 556 (tasks.append(self.export_teams_to_data(data)))
- Use same pattern: `tasks.append(self.export_position_json_files(data))` if CREATE_POSITION_JSON is true

---

## Skeptical Re-verification Results

### Round 1 (Iteration 6)
- **Verified correct:** 9 assumptions verified as correct
- **Items requiring interface verification:** 4 (FantasyPlayer attributes, ESPNPlayerData field names, position strings, ProjectionData structure)
- **Confidence level:** MEDIUM (acceptable to proceed, will verify interfaces before implementation)

### Round 2 (Iteration 13)
- **Verified correct:** All 9 assumptions from Round 1 still valid
- **Updates:** Iteration 9 import fix incorporated
- **Confidence level:** MEDIUM (acceptable to proceed)

### Round 3 (Iteration 22)
- **Verified correct:** All assumptions from Rounds 1-2 confirmed
- **Confidence level:** HIGH (upgraded from MEDIUM)
- **Rationale:** Fresh Eyes (iterations 17-18) confirmed 100% spec coverage, Edge Case audit (iteration 20) found 16 cases all covered, 4-part Spec Audit (iteration 23a) PASSED

---

## Integration Gap Check Results

### Round 1 (Iteration 7) - COMPLETE ✅

**1. Integration Matrix Verification:**
- ✅ All 12 new components have callers identified
- ✅ Integration Matrix exists in TODO (lines 626-642)
- ✅ Entry point: `run_player_fetcher.py` → `main()` → `export_position_json_files()`
- ✅ Call chain verified: main() → export_position_json_files() → _export_single_position_json() → _prepare_position_json_data() → [all helpers]

**2. Caller Modification Tasks:**
- ✅ Task 3.1 modifies `player_data_fetcher_main.py:main()` to call `export_position_json_files()`
- ✅ All internal method calls are within new methods (no additional caller modifications needed)

**3. Orphan Code Check:**
- ✅ **NO ORPHAN CODE FOUND**
- Every new method has a caller or is called from the entry point
- Complete execution path verified from entry to output

**4. Entry Point Coverage:**
- ✅ Verified trace from `run_player_fetcher.py` through to 6 position JSON output files
- ✅ Data Flow section (lines 769-867) documents complete execution path
- ✅ All new code is in execution path when CREATE_POSITION_JSON=True

**5. Entry Script File Discovery:**
- ✅ N/A - Not changing output file format discovery
- New files go to separate folder (/data/player_data/), not main data folder
- No glob pattern updates needed in run_*.py scripts

**6. Cross-Feature Impact Check:**

**Files Modified:**
| File | Other Features Using It | Impact Assessment | Mitigation |
|------|------------------------|-------------------|------------|
| `player-data-fetcher/config.py` | None (isolated to player-data-fetcher) | None - adding new settings | N/A |
| `player-data-fetcher/player_data_exporter.py` | None (isolated module) | None - adding new methods | N/A |
| `player-data-fetcher/player_data_fetcher_main.py` | None (entry point) | None - adding new export call | N/A |
| `utils/DraftedRosterManager.py` | ✅ **TradeSimulatorModeManager** | ✅ **ZERO IMPACT** - adding NEW method only | Existing methods unchanged |

**Verification:**
- Checked `league_helper/trade_simulator_mode/TradeSimulatorModeManager.py`
- Uses `DraftedRosterManager` constructor and `load_drafted_data()` method
- Our change: adding NEW method `get_team_name_for_player()`
- **Impact:** NONE - we're not modifying any existing methods
- **Risk:** ZERO - additive change only

**7. Unresolved Alternatives Check:**
- ✅ Searched for "Alternative:" - **NONE FOUND**
- ✅ Searched for "May need to..." - **NONE FOUND**
- ✅ All decisions resolved during planning phase

**Summary:**
- ✅ All new methods have callers
- ✅ No orphan code
- ✅ Entry point coverage verified
- ✅ Zero cross-feature impact
- ✅ No unresolved alternatives
- ✅ Integration Matrix complete and accurate

**Status:** PASS ✅ - Ready to proceed to Round 2 verification

### Round 2 (Iteration 14)
- **Integration Matrix:** Re-verified - all 12 components have callers
- **Orphan Code:** Zero found
- **Cross-feature impact:** ZERO (DraftedRosterManager change still additive only)
- **Unresolved items:** Zero ("Alternative:" and "May need to..." searches = 0 results)

### Round 3 (Iteration 23) - COMPLETE ✅
- **Integration Matrix:** Final verification - all 12 components traced from entry point
- **Call chain:** run_player_fetcher.py → main() → export_position_json_files() → all helpers
- **Orphan Code:** ZERO confirmed (verified 3 times across all rounds)
- **Cross-feature impact:** ZERO (TradeSimulatorModeManager unaffected)
- **Entry point coverage:** 100% - all new code reachable when CREATE_POSITION_JSON=True
- **Status:** PASS ✅

---

## Step 3: Questions File Decision - SKIPPED ✅

**Decision:** No questions file needed

**Rationale:**
- All 11 user decisions already made during planning phase (documented in USER_DECISIONS_SUMMARY.md)
- Iteration 6 (Skeptical Re-verification) identified 4 items needing interface verification, NOT user decisions
- Interface items will be verified during pre-implementation Interface Verification Protocol
- Iteration 7 (Integration Gap Check) found zero unresolved alternatives ("Alternative:" search = 0 results)
- Spec is clear and complete - no ambiguities requiring user input

**Verification:**
- ✅ USER_DECISIONS_SUMMARY.md documents all 11 decisions with rationale
- ✅ No "Alternative:" notes in TODO (verified via grep)
- ✅ No "May need to..." phrases in TODO (verified via grep)
- ✅ Algorithm Traceability Matrix complete (22 algorithms mapped)
- ✅ Acceptance criteria complete (37 criteria covering 100% of spec)

**Next Step:** Skip Step 4 (no answers to integrate) → Proceed to Step 5 (Round 2 verification)

---

## Integration Checklist (Iteration 16)

**Purpose:** Final verification before Round 3 that all integration points are documented.

### Code Integration Points

| # | Integration Point | From Component | To Component | Status |
|---|-------------------|----------------|--------------|---------|
| 1 | Config imports | config.py | player_data_exporter.py | ✅ Documented (Task 1.1) |
| 2 | DraftedRosterManager import | DraftedRosterManager.py | player_data_exporter.py | ✅ Already imported (line 29) |
| 3 | New method call | get_team_name_for_player() | _prepare_position_json_data() | ✅ Task 2.3 REQ-2 |
| 4 | Main workflow call | export_position_json_files() | main() | ✅ Task 3.1 |
| 5 | Async gather pattern | export_position_json_files() | _export_single_position_json() | ✅ Task 2.1 REQ-2 |
| 6 | File manager call | _export_single_position_json() | self.file_manager.save_json_data() | ✅ Existing pattern |
| 7 | Player transformation | get_fantasy_players() | _export_single_position_json() | ✅ Existing method |
| 8 | Stat extraction | All stat helpers | _prepare_position_json_data() | ✅ Task 2.4 |
| 9 | Actual points | _get_actual_points_array() | _prepare_position_json_data() | ✅ Task 2.5 |
| 10 | ESPN API data | ESPNPlayerData | stat extraction helpers | ✅ Via player_data param |
| 11 | CURRENT_NFL_WEEK | config.py | _get_actual_points_array() | ✅ Already imported |
| 12 | MY_TEAM_NAME | config.py | _prepare_position_json_data() | ✅ Already imported |

**Total Integration Points:** 12/12 documented ✅

### File Modification Checklist

| File | Modifications | Lines Affected (est.) | Status |
|------|---------------|----------------------|---------|
| `player-data-fetcher/config.py` | Add 2 constants | ~5 lines | ✅ Task 1.1 |
| `player-data-fetcher/player_data_exporter.py` | Update imports | 1 line | ✅ Task 1.1 |
| `player-data-fetcher/player_data_exporter.py` | Add 9 new methods | ~300 lines | ✅ Tasks 2.1-2.5 |
| `player-data-fetcher/player_data_fetcher_main.py` | Add export call | ~5 lines | ✅ Task 3.1 |
| `utils/DraftedRosterManager.py` | Add 1 method | ~10 lines | ✅ Task 1.2 |
| `tests/player-data-fetcher/test_config.py` | Add config tests | ~20 lines | ✅ Task 4.1 |
| `tests/utils/test_DraftedRosterManager.py` | Add method tests | ~50 lines | ✅ Task 4.1 |
| `tests/player-data-fetcher/test_player_data_exporter.py` | Add export tests | ~150 lines | ✅ Task 4.2 |
| `tests/player-data-fetcher/integration/` | Create integration test | ~100 lines | ✅ Task 4.3 |

**Total Files:** 5 modified, 1 created (integration test) ✅

### Dependency Verification

| Dependency | Type | Source | Status |
|------------|------|--------|---------|
| asyncio | Standard library | Python | ✅ Available |
| pathlib.Path | Standard library | Python | ✅ Available |
| typing.List | Standard library | Python | ✅ Available |
| FantasyPlayer | Internal class | utils/FantasyPlayer.py | ✅ Exists |
| ESPNPlayerData | Internal class | player_data_models.py | ✅ Exists |
| DraftedRosterManager | Internal class | utils/DraftedRosterManager.py | ✅ Exists |
| DataFileManager | Internal class | utils/data_file_manager.py | ✅ Exists |
| Logger | Internal utility | utils/LoggingManager.py | ✅ Available |
| Config constants | Internal | config.py | ✅ Accessible |

**Total Dependencies:** 9/9 verified ✅

### Test Coverage Plan

| Component | Test Type | Test File | Coverage |
|-----------|-----------|-----------|----------|
| Config settings | Unit | test_config.py | Settings exist & correct values |
| get_team_name_for_player() | Unit | test_DraftedRosterManager.py | 5 test cases (Task 4.1) |
| export_position_json_files() | Unit | test_player_data_exporter.py | File creation, config check |
| Position JSON structure | Unit | test_player_data_exporter.py | 10 test cases (Task 4.2) |
| Full workflow | Integration | test_position_json_export.py | End-to-end validation |
| Manual QC | Manual | Documented in lessons_learned.md | Data accuracy spot-checks |

**Total Test Coverage:** 6 test scenarios planned ✅

### Pre-Implementation Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| All 11 user decisions made | ✅ COMPLETE | USER_DECISIONS_SUMMARY.md |
| Specs finalized | ✅ COMPLETE | player-data-fetcher-new-data-format_specs.md |
| Algorithm Traceability Matrix | ✅ COMPLETE | 22 algorithms mapped |
| Integration Matrix | ✅ COMPLETE | 12 components, all with callers |
| File paths verified | ✅ COMPLETE | Iteration 15 |
| Dependencies identified | ✅ COMPLETE | All 9 dependencies verified |
| Test plan created | ✅ COMPLETE | Tasks 4.1-4.4 |
| Interface verification pending | ⚠️ PENDING | Pre-implementation protocol |

**Readiness Status:** ✅ 7/8 complete (Interface verification before coding)

---

## Round 3 Verification Summary

**Iterations 17-18: Fresh Eyes Review**
- Read specs.md with fresh perspective
- Created fresh requirements list (33 items)
- Compared to TODO: 100% match, zero missing requirements
- Verified "similar to" pattern (export_all_formats) was actually read
- Result: ✅ PASS - All requirements covered

**Iteration 19: Algorithm Traceability #3**
- Re-verified Algorithm Traceability Matrix
- Confirmed 22 algorithms mapped to code locations
- Cross-checked with fresh requirements list
- Result: ✅ PASS - Matrix complete and accurate

**Iteration 20: Edge Case Verification**
- Identified 16 edge cases from specs
- Verified all 16 have TODO tasks
- Verified all 16 have test coverage
- Created edge case matrix with expected behaviors
- Result: ✅ PASS - All edge cases covered

**Iteration 21: Test Coverage Planning + Mock Audit**
- Identified 14 algorithm tests needed
- Audited 5 mock objects vs real interfaces
- Found 2/5 interfaces verified, 3/5 require pre-implementation check
- Result: ✅ PASS - Comprehensive test plan, interfaces flagged

**Iteration 22: Skeptical Re-verification #3**
- Re-challenged all assumptions from Rounds 1-2
- Verified all 10 assumptions still valid
- Upgraded confidence from MEDIUM → HIGH
- Result: ✅ PASS - High confidence, ready for implementation

**Iteration 23: Integration Gap Check #3**
- Final verification of Integration Matrix (3rd time)
- Traced all 12 components from entry point
- Confirmed zero orphan code, zero cross-feature impact
- Result: ✅ PASS - Integration complete

**Iteration 23a: Pre-Implementation Spec Audit** ⭐
- **Part 1:** Spec Coverage Audit → ✅ PASS (100% coverage)
- **Part 2:** TODO Clarity Audit → ✅ PASS (all actionable)
- **Part 3:** Data Structure Audit → ✅ PASS (exact match)
- **Part 4:** Spec-to-TODO Mapping → ✅ PASS (100% traceability)
- Result: ✅ **PASS** - TODO is implementation-ready

**Iteration 24: Implementation Readiness**
- Verified all 15 pre-implementation requirements
- 14/15 complete, 1 pending (Interface Verification)
- Confidence level: HIGH
- Result: ⚠️ **ALMOST READY** - Interface Verification required

---

## Progress Notes

**Last Updated:** 2025-12-24 12:10 (ALL ROUNDS COMPLETE)
**Current Status:** ✅ ALL 25 VERIFICATION ITERATIONS COMPLETE
**Next Steps:** Execute Interface Verification Protocol (MANDATORY before coding)
**Blockers:** Interface Verification Protocol (3 interfaces to verify)
**Notes:**
- ✅ Round 1 complete (iterations 1-7 + 4a) - 8/8
- ✅ Round 2 complete (iterations 8-16) - 9/9
- ✅ Round 3 complete (iterations 17-24 + 23a) - 9/9
- ✅ **TOTAL: 25/25 iterations complete**
- ✅ 4-part Pre-Implementation Spec Audit PASSED (iteration 23a)
- ✅ Confidence level upgraded to HIGH
- ✅ Edge cases: 16 identified, all covered
- ✅ Test coverage: 14 algorithm tests + 16 edge case tests planned
- ⚠️ **NEXT REQUIRED:** Interface Verification Protocol (verify FantasyPlayer, ESPNPlayerData, DraftedRosterManager)
- 📋 After interfaces verified: Ready to begin implementation following implementation_execution_guide.md
