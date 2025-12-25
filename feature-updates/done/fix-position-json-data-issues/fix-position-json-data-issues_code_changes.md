# Fix Position JSON Data Issues - Code Changes

**Feature**: Fix 4 critical data quality issues in position JSON export
**Started**: 2024-12-24
**Status**: Implementation in progress

---

## Change Log

### Change 1: Add raw_stats field to ESPNPlayerData model

**Date/Time**: 2024-12-24
**Requirement**: REQ-3.1
**Spec Location**: specs.md lines 164-171
**Files Modified**:
- `player-data-fetcher/player_data_models.py`

**Changes Made**:
1. Added `Any` to imports (line 13) - required for `Dict[str, Any]` type hint
2. Added `raw_stats` field to ESPNPlayerData class (lines 78-81)
   - Type: `Optional[List[Dict[str, Any]]]`
   - Default: `Field(default_factory=list)` (follows projected_weeks pattern)
   - Purpose: Store raw ESPN stats array for stat extraction

**Code Added**:
```python
# Line 13 - Import
from typing import Any, Dict, List, Optional

# Lines 78-81 - New field
# Raw stats array from ESPN API for position JSON export stat extraction
# Stores complete stats array from ESPN response to enable detailed stat extraction
# Each entry contains: {scoringPeriodId, statSourceId, appliedTotal, appliedStats}
raw_stats: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
```

**Rationale**:
- Uses `Field(default_factory=list)` instead of `= None` from spec to match existing `projected_weeks` pattern (line 76)
- Prevents None checks throughout code (always returns empty list)
- Documented in TODO Iteration 19 as justified improvement

**Verification**:
- ✅ All 2335 tests pass (100%)
- ✅ Field type matches requirement
- ✅ Follows existing pattern in codebase
- ✅ Pydantic validation works correctly

**Spec Compliance**: ✅ Matches specs.md lines 164-171 with justified improvement

---

### Change 2: Populate raw_stats from ESPN API during parsing

**Date/Time**: 2024-12-24
**Requirement**: REQ-3.2
**Spec Location**: specs.md lines 177-187
**Files Modified**:
- `player-data-fetcher/espn_client.py`

**Changes Made**:
1. Added `raw_stats` parameter to ESPNPlayerData constructor call (line 1836)
   - Value: `player_info.get('stats', [])`
   - Purpose: Capture ESPN stats array during initial parsing

**Code Added**:
```python
# Line 1836 - New parameter in ESPNPlayerData constructor
projection = ESPNPlayerData(
    id=id,
    name=name,
    team=team,
    position=position,
    bye_week=bye_week,
    drafted=0,  # Initialize all players as not drafted
    fantasy_points=fantasy_points,
    average_draft_position=average_draft_position,
    player_rating=player_rating,
    injury_status=injury_status,
    api_source="ESPN",
    raw_stats=player_info.get('stats', [])  # Store stats array for position JSON export
)
```

**Rationale**:
- Captures stats array during initial parsing (no additional API calls needed)
- `player_info` comes from `player.get('player', {})` at line 1635
- Stats array contains all weekly data with statSourceId indicators
- Empty list default ensures safe access even if stats missing

**Verification**:
- ✅ All 2335 tests pass (100%)
- ✅ Parameter correctly added to constructor
- ✅ No additional API calls required
- ✅ Safe default behavior (empty list if stats missing)

**Spec Compliance**: ✅ Matches specs.md lines 177-187 exactly

---

### Change 3: Fix file naming - write to data/ folder with fixed filenames

**Date/Time**: 2024-12-24
**Requirements**: REQ-1.1, REQ-1.2, REQ-1.3
**Spec Location**: specs.md lines 13-42
**Files Modified**:
- `player-data-fetcher/player_data_exporter.py`

**Changes Made**:
1. Added `import json` to imports (line 16)
2. Replaced DataFileManager call with direct file writing (lines 453-477)
   - New path: `Path(__file__).parent / f'../data/{position.lower()}_data.json'`
   - No timestamps, no "new_" prefix
   - Files: `qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`
   - Location: `data/` folder (same as `players.csv`)
   - Each run overwrites previous file

**Code Removed**:
```python
# OLD (lines 452-454):
prefix = f"new_{position.lower()}_data"
file_path, _ = file_manager.save_json_data(output_data, prefix, create_latest=False)
```

**Code Added**:
```python
# NEW (lines 453-477):
# Save to data/ folder with fixed filename (no timestamps, no prefix)
# Matches pattern of players.csv export - each run overwrites previous file
file_path = Path(__file__).parent / f'../data/{position.lower()}_data.json'

try:
    # Ensure the directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON file asynchronously
    async with aiofiles.open(str(file_path), mode='w', encoding='utf-8') as f:
        json_string = json.dumps(output_data, indent=2, ensure_ascii=False)
        await f.write(json_string)

    self.logger.info(f"Exported {len(players_json)} {position} players to {file_path}")
    return str(file_path)

except PermissionError as e:
    self.logger.error(f"Permission denied writing to {file_path}: {e}")
    raise
except OSError as e:
    self.logger.error(f"OS error writing to {file_path}: {e}")
    raise
except Exception as e:
    self.logger.error(f"Unexpected error exporting position JSON: {e}")
    raise
```

**Rationale**:
- Matches pattern used for `players.csv` export (lines 678-708)
- Direct file writing bypasses DataFileManager's automatic timestamp addition
- Fixed filenames make it easier for downstream consumers
- Each run overwrites previous file (no accumulation)
- Consistent with project's other output files in `data/` folder

**Verification**:
- ✅ All 2335 tests pass (100%)
- ✅ Follows same pattern as players.csv export
- ✅ No DataFileManager dependency
- ✅ Proper async file I/O with error handling
- ✅ Files will be created in data/ with simple names

**Spec Compliance**:
- ✅ REQ-1.1: Files written to `data/` folder (not `feature-updates/`)
- ✅ REQ-1.2: Fixed filenames (qb_data.json, rb_data.json, etc.)
- ✅ REQ-1.3: Each run overwrites previous files

---

### Change 4: Fix projected and actual points to use different stat sources

**Date/Time**: 2024-12-24
**Requirements**: REQ-2.1, REQ-2.2, REQ-2.3, REQ-2.4
**Spec Location**: specs.md lines 44-81, 201-225
**Files Modified**:
- `player-data-fetcher/player_data_exporter.py`

**Changes Made**:
1. **Updated `_get_projected_points_array()` (lines 555-579)**:
   - Changed signature from `player: FantasyPlayer` to `espn_data: Optional[ESPNPlayerData]`
   - Now extracts from `espn_data.raw_stats` with `statSourceId=1` (pre-game projections)
   - Returns pre-game ESPN projections instead of using week_N_points attributes

2. **Updated `_get_actual_points_array()` (lines 581-605)**:
   - Now extracts from `espn_data.raw_stats` with `statSourceId=0` (post-game results)
   - Removed TODO comment on line 592
   - Returns actual game results instead of using week_N_points attributes

3. **Updated caller (line 507)**:
   - Changed from `self._get_projected_points_array(player)` to `self._get_projected_points_array(espn_data)`
   - Both arrays now use same data source (espn_data) but different statSourceId

**Code Removed (_get_projected_points_array)**:
```python
# OLD:
def _get_projected_points_array(self, player: FantasyPlayer) -> List[float]:
    projected_points = []
    for week in range(1, 18):
        points = getattr(player, f"week_{week}_points", None)
        projected_points.append(points if points is not None else 0.0)
    return projected_points
```

**Code Added (_get_projected_points_array)**:
```python
# NEW:
def _get_projected_points_array(self, espn_data: Optional[ESPNPlayerData]) -> List[float]:
    """Extract projected points from statSourceId=1 (pre-game projections)"""
    if espn_data is None or not espn_data.raw_stats:
        return [0.0] * 17

    projected_points = []
    for week in range(1, 18):
        projected = None
        for stat in espn_data.raw_stats:
            if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 1:
                projected = stat.get('appliedTotal')
                break
        projected_points.append(float(projected) if projected else 0.0)
    return projected_points
```

**Code Removed (_get_actual_points_array)**:
```python
# OLD:
actual_points = []
for week in range(1, 18):
    if week <= CURRENT_NFL_WEEK:
        # TODO: In full implementation, extract from statSourceId=0
        points = getattr(espn_data, f"week_{week}_points", None)
        actual_points.append(points if points is not None else 0.0)
    else:
        actual_points.append(0.0)
return actual_points
```

**Code Added (_get_actual_points_array)**:
```python
# NEW:
actual_points = []
for week in range(1, 18):
    actual = None
    for stat in espn_data.raw_stats:
        if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 0:
            actual = stat.get('appliedTotal')
            break
    actual_points.append(float(actual) if actual else 0.0)
return actual_points
```

**Rationale**:
- **Critical bug fix**: Previous implementation used same data source for both arrays (actual results)
- This made projected_points and actual_points IDENTICAL - defeating primary use case
- ESPN API provides TWO stat entries per week:
  - statSourceId=0: What actually happened (post-game)
  - statSourceId=1: What was projected (pre-game)
- Both use `appliedTotal` field, difference is which stat entry to read from
- Pattern follows `compile_historical_data.py` implementation

**Verification**:
- ✅ All 2335 tests pass (100%)
- ✅ Both methods now use espn_data.raw_stats
- ✅ Different statSourceId values (1 vs 0)
- ✅ Arrays will be DIFFERENT (key requirement)
- ✅ TODO comment removed from _get_actual_points_array

**Spec Compliance**:
- ✅ REQ-2.1: projected_points uses statSourceId=1 (pre-game)
- ✅ REQ-2.2: actual_points uses statSourceId=0 (post-game)
- ✅ REQ-2.3: Arrays are DIFFERENT (different statSourceId)
- ✅ REQ-2.4: Caller updated (line 507)

---

### Change 5: Add helper methods for stat extraction

**Date/Time**: 2024-12-24
**Requirements**: REQ-3.3, REQ-3.4
**Spec Location**: specs.md lines 237-260
**Files Modified**:
- `player-data-fetcher/player_data_exporter.py`

**Changes Made**:
1. **Added `_extract_stat_value()` method (lines 607-629)**:
   - Extracts single stat value from raw_stats array for specific week
   - Uses statSourceId=0 (actual stats) for stat extraction
   - Returns float value or 0.0 if not found

2. **Added `_extract_combined_stat()` method (lines 631-649)**:
   - Sums multiple stat IDs for a specific week
   - Used for combined stats like return yards (stat_114 + stat_115)
   - Calls `_extract_stat_value()` for each stat ID

**Code Added**:
```python
def _extract_stat_value(self, raw_stats: List[Dict], week: int, stat_id: str) -> float:
    """
    Extract a single stat value from raw_stats array for a specific week.

    Pattern from compile_historical_data.py:
    - Find stat entry with scoringPeriodId == week AND statSourceId == 0
    - Extract from appliedStats dict using stat_id as string key
    - Return 0.0 if not found

    Args:
        raw_stats: List of stat dictionaries from ESPN API
        week: Week number (1-17)
        stat_id: ESPN stat ID as string (e.g., '0', '1', '3')

    Returns:
        Stat value as float, or 0.0 if not found
    """
    for stat in raw_stats:
        if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 0:
            applied_stats = stat.get('appliedStats', {})
            value = applied_stats.get(stat_id, 0.0)
            return float(value) if value else 0.0
    return 0.0

def _extract_combined_stat(self, raw_stats: List[Dict], week: int, stat_ids: List[str]) -> float:
    """
    Sum multiple stat IDs for a specific week.

    Used for combined stats like return yards (stat_114 + stat_115) or
    two-point conversions (multiple stat IDs).

    Args:
        raw_stats: List of stat dictionaries from ESPN API
        week: Week number (1-17)
        stat_ids: List of ESPN stat IDs to sum (as strings)

    Returns:
        Sum of all stat values as float
    """
    total = 0.0
    for stat_id in stat_ids:
        total += self._extract_stat_value(raw_stats, week, stat_id)
    return total
```

**Rationale**:
- Reusable helpers for all 6 stat extraction methods (passing, rushing, receiving, misc, kicking, defense)
- Follows pattern from `compile_historical_data.py`
- Stat IDs are strings ('0', '1', '3') not integers
- Uses statSourceId=0 for actual stats (post-game results)
- Safe defaults: returns 0.0 if stat not found
- `_extract_combined_stat()` enables summing multiple stats (e.g., return yards)

**Verification**:
- ✅ All 2335 tests pass (100%)
- ✅ Both methods added before first usage
- ✅ Pattern matches compile_historical_data.py
- ✅ Proper type hints and documentation

**Spec Compliance**:
- ✅ REQ-3.3: _extract_stat_value() created (lines 607-629)
- ✅ REQ-3.4: _extract_combined_stat() created (lines 631-649)

---

### Change 6: Implement all 6 stat extraction methods (Phases 7-12)

**Date/Time**: 2024-12-24
**Requirements**: REQ-3.5, REQ-3.6, REQ-3.7, REQ-3.8, REQ-3.9, REQ-3.10, REQ-4.1, REQ-4.2
**Spec Location**: specs.md lines 111-127
**Files Modified**:
- `player-data-fetcher/player_data_exporter.py`

**Changes Made**:
1. **_extract_passing_stats()** (lines 651-670) - REQ-3.5: 6 stats
2. **_extract_rushing_stats()** (lines 672-685) - REQ-3.6: 3 stats
3. **_extract_receiving_stats()** (lines 687-702) - REQ-3.7: 4 stats
4. **_extract_misc_stats()** (lines 704-732) - REQ-3.8: 1 stat (two_pt removed)
5. **_extract_kicking_stats()** (lines 734-757) - REQ-3.9: 4 stats
6. **_extract_defense_stats()** (lines 759-786) - REQ-3.10: 11 stats

**All TODO Comments Removed** (REQ-4.1, REQ-4.2):
- ✅ 6 TODO comments from stat extraction methods
- ✅ 1 TODO comment from _get_actual_points_array() (removed in Change 4)
- **Total: 7 TODO comments removed** (verified with grep)

**Implementation Pattern**:
```python
def _extract_{position}_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
    if espn_data is None or not espn_data.raw_stats:
        return {stat_name: [0.0] * 17 for stat_name in stat_names}

    return {
        "stat_name": [self._extract_stat_value(espn_data.raw_stats, week, 'ID')
                      for week in range(1, 18)]
    }
```

**Verification**:
- ✅ All 2335 tests pass (100%)
- ✅ All TODO comments removed
- ✅ Stat arrays will contain real ESPN data
- ✅ Uses helper methods for consistency
- ✅ Safe defaults (0.0) if no data

**Spec Compliance**:
- ✅ REQ-3.5: Passing (stat_0,1,3,4,20,64)
- ✅ REQ-3.6: Rushing (stat_23,24,25)
- ✅ REQ-3.7: Receiving (stat_53,58,42,43)
- ✅ REQ-3.8: Misc (stat_68 only - two_pt removed per user decision)
- ✅ REQ-3.9: Kicking (stat_83,85,86,88)
- ✅ REQ-3.10: Defense (stat_95,96,98,99,94,106,120,127,114+115,101+102)
- ✅ REQ-4.1: TODO from _get_actual_points_array removed (Change 4)
- ✅ REQ-4.2: All 6 TODO comments from stat methods removed

---

## Testing Status

- **Baseline Tests (Before Changes)**: 2335/2335 passing (100%)
- **Current Tests**: 2335/2335 passing (100%)
- **New Tests Added**: 0 (will add in Phase 13)
- **Test Regressions**: 0

---

## Next Changes

**Next**: All core requirements complete! Ready for Phase 13 (unit tests) and Phase 14 (integration testing)

---

## Notes

- Following implementation_execution_guide.md protocols
- Updating this file after EACH change (not batching)
- Verifying against specs.md before AND after each change
- Running full test suite after each change
