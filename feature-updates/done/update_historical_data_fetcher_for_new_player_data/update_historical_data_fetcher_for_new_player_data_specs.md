# Update Historical Data Fetcher for New Player Data

## Objective

Update the historical data compiler (`compile_historical_data.py` and `historical_data_compiler/` folder) to generate the new JSON-formatted player data files (6 position-specific JSON files) alongside the legacy CSV files (`players.csv` and `players_projected.csv`). Each week folder in the historical data should contain a snapshot of player data at that point in time, matching the structure used by the current player data fetcher.

**Primary Goal:** Generate historical JSON data files to prepare for future simulation system and league helper updates that will use enhanced player statistics.

**Backward Compatibility:** Maintain CSV generation via boolean toggles (simulation updates are out of scope).

---

## High-Level Requirements

### 1. Dual Output Format (Backward Compatible)
- **Legacy format (GENERATE_CSV toggle):** `players.csv` and `players_projected.csv` per week
- **New format (GENERATE_JSON toggle):** 6 JSON files per week (`qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`)
- **Configuration:** Boolean toggles at top of `compile_historical_data.py`
  - `GENERATE_CSV = True` (default: maintain backward compatibility)
  - `GENERATE_JSON = True` (default: enable new format)
- **Snapshot nature:** Each week's files represent data available at that point in time (historical actuals for past weeks, projections for future weeks)

### 2. JSON File Structure
- **Position-specific files:** Separate JSON file for each position (QB, RB, WR, TE, K, DST)
- **Content:** EXACT structure match to current player data fetcher output (data/player_data/*.json)
- **Required fields:** id, name, team, position, injury_status, drafted_by, locked, average_draft_position, player_rating, projected_points[], actual_points[], position-specific stat arrays
- **Stats inclusion:** All new stats and weekly breakdowns available in the new format
- **Point-in-time logic:** Arrays reflect data availability at that week
  - Weeks 1 to N-1: actual values
  - Weeks N to 17: zeros (for actual_points and stat arrays) or projections (for projected_points)
  - player_rating: Recalculated per week based on cumulative performance

### 3. Historical Data Generation
- **Per-week generation:** Each week folder (e.g., `week_01/`, `week_02/`) contains:
  - 2 CSV files (if GENERATE_CSV=True): players.csv, players_projected.csv
  - 6 JSON files (if GENERATE_JSON=True): qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
- **Time-accurate snapshots:** Data reflects what was known at that point in the season
- **Current consumer compatibility:** CSV files continue to work with existing simulation system
- **Future consumer preparation:** JSON files ready for future simulation system updates (out of scope)

---

## Resolved Implementation Details

### Decision 1: Backward Compatibility Strategy ✅

**User Decision:** Dual output with boolean toggles

**Implementation:**
- Add two boolean toggles at top of `compile_historical_data.py`:
  - `GENERATE_CSV = True` (default: maintain backward compatibility)
  - `GENERATE_JSON = True` (default: enable new format)
- Keep existing CSV generation implementation (no changes)
- Add new JSON generation implementation (new code)
- Both outputs can coexist in the same week folder

**Rationale:**
- Maintains backward compatibility with existing simulation system
- Allows gradual migration to JSON format
- Simulation updates are OUT OF SCOPE (future feature)
- Clean separation of concerns

### Decision 2: Point-in-Time Logic Application ✅

**User Decision:** Apply point-in-time logic to ALL JSON arrays

**Implementation:**
For week N snapshot:
- **actual_points array:**
  - Weeks 1 to N-1: Actual fantasy points from ESPN (statSourceId=0)
  - Weeks N to 17: 0.0 (data not yet available)
  - Bye weeks: Always 0.0

- **projected_points array:**
  - Weeks 1 to N-1: Historical projections from ESPN (statSourceId=1)
  - Weeks N to 17: Current week's projection repeated (best available estimate)
  - Bye weeks: 0.0

- **Stat arrays (passing.completions, rushing.attempts, etc.):**
  - Weeks 1 to N-1: Actual stat values from ESPN raw_stats
  - Weeks N to 17: 0.0 (no future data)
  - Bye weeks: 0.0

- **player_rating:**
  - Week 1: Original draft-based rating
  - Week 2+: Recalculated from cumulative actual points through week N-1
  - Formula: `rating = 100 - ((position_rank - 1) / (total_in_position - 1)) * 99`

**Rationale:**
- Consistency with existing CSV snapshot logic
- Realistic simulation (matches what system would know at that time)
- Clear semantics (zeros mean "not yet available", not "player didn't play")

### Decision 3: Code Reuse Strategy ✅

**User Decision:** Bridge Adapter Pattern

**Implementation:**
- Create new file: `historical_data_compiler/json_exporter.py`
- Import stat extraction methods from `player-data-fetcher/player_data_exporter.py`
- Adapter layer converts `PlayerData` → minimal `ESPNPlayerData`-like object
- Reuse existing stat extraction methods:
  - `_extract_passing_stats()`
  - `_extract_rushing_stats()`
  - `_extract_receiving_stats()`
  - `_extract_kicking_stats()`
  - `_extract_defense_stats()`
- Zero changes to current player data exporter

**Adapter Object Structure:**
```python
class PlayerDataAdapter:
    """Minimal ESPNPlayerData-like object for bridge pattern"""
    def __init__(self, player_data: PlayerData, current_week: int):
        self.id = player_data.id
        self.name = player_data.name
        self.team = player_data.team
        self.position = player_data.position
        self.stats = player_data.raw_stats  # ESPN stats array
        self.injury_status = player_data.injury_status
        # ... other fields needed by stat extractors
```

**Rationale:**
- Avoids code duplication (1000+ lines of stat extraction logic)
- Minimal coupling (adapter layer is small)
- Future-proof (changes to stat extraction benefit both systems)
- Clean separation (historical compiler doesn't modify current fetcher)

### Decision 4: Historical Projections Quality ✅

**User Decision:** Test historical projections first, verify with user before implementing fallback

**Implementation:**
🛑 **MANDATORY STOP POINT** in smoke testing protocol:

**5-Step Historical Projection Verification Process:**
1. **Generate historical data** for test season (e.g., 2023)
2. **Extract projection quality metrics:**
   - Compare statSourceId=1 (projected) vs statSourceId=0 (actual) for past weeks
   - Calculate average deviation, missing data percentage
   - Identify weeks with poor/missing projections
3. **🛑 STOP AND REPORT TO USER:**
   - Present projection quality findings
   - Show specific examples of good/poor projections
   - Recommendation: acceptable vs needs fallback
4. **WAIT FOR USER DECISION:**
   - If quality acceptable: Proceed with historical projections as-is
   - If quality poor: User approves fallback approach before implementation
5. **Document decision** in lessons learned

**Rationale:**
- Unknown quality of ESPN's historical projections (statSourceId=1)
- Data-driven decision making (test first, decide based on results)
- Avoid premature optimization (don't build fallback if not needed)
- User maintains control over critical design decisions

### Decision 5: Consumer Identification ✅

**User Decision:** Future Simulation System (no consumer yet)

**Context:**
JSON files will eventually be used by:
1. Updated simulation system (future feature)
2. Updated league helper classes with new stats for scoring (future feature)
3. Optimization of scoring weights for new metrics (future feature)

**In Scope for This Feature:**
- Generate JSON files with correct structure
- Structure validation against current player_data/*.json files
- Manual inspection of sample weeks

**Out of Scope:**
- Building the consumer (simulation updates)
- League helper updates
- Automated consumer roundtrip testing

**Testing Approach:**
- Structure validation: Load generated JSON and verify schema matches current format
- Field verification: All required fields present with correct types
- Point-in-time verification: Arrays follow correct logic
- Manual inspection: Review sample week_01, week_08, week_17 outputs

**Rationale:**
- Prepares infrastructure for future improvements
- Decouples historical data migration from simulation updates
- Allows parallel development of consumer later
- JSON structure is well-defined (matches existing format)

---

## Data Structure Specification

### JSON File Structure (Exact Match to Current Format)

Each position-specific JSON file follows this structure:

**File:** `{position}_data.json` (e.g., qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)

**Root object:**
```json
{
  "{position}_data": [
    {
      "id": "string",
      "name": "string",
      "team": "string (3-letter abbrev)",
      "position": "string (QB/RB/WR/TE/K/DST)",
      "injury_status": "string or null",
      "drafted_by": "string or null",
      "locked": "boolean",
      "average_draft_position": "float or null",
      "player_rating": "float (1-100)",
      "projected_points": [float, ...],  // 17 elements
      "actual_points": [float, ...],     // 17 elements
      "{position}_stats": {
        "stat_name": [float, ...],  // 17 elements per stat
        ...
      }
    },
    ...
  ]
}
```

**Position-Specific Stat Objects:**
- **QB:** `passing` (completions, attempts, yards, touchdowns, interceptions, sacks, rating), `rushing` (attempts, yards, touchdowns, long, fumbles)
- **RB/WR/TE:** `rushing` (attempts, yards, touchdowns, long, fumbles), `receiving` (receptions, targets, yards, touchdowns, long)
- **K:** `kicking` (field_goals_made, field_goals_attempted, extra_points_made, extra_points_attempted, long_field_goal)
- **DST:** `defense` (sacks, interceptions, fumbles_recovered, safeties, touchdowns, points_allowed, yards_allowed)

**Reference:** `data/player_data/qb_data.json`, `rb_data.json`, etc. (current player fetcher output)

---

## Data Source Mapping

### ESPN API Data Sources

**API Endpoint:**
```
https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leaguedefaults/3
```

**Parameters:**
- `scoringPeriodId={week}` - Specific week (1-17)
- `view=kona_player_info` - Player information and stats

**Field Mapping:**

| JSON Field | ESPN API Path | Notes |
|------------|---------------|-------|
| id | player.id | String conversion |
| name | player.fullName | Full player name |
| team | proTeamId → ESPN_TEAM_MAPPINGS | Convert ID to 3-letter abbrev |
| position | defaultPositionId → ESPN_POSITION_MAPPINGS | Convert ID to position string |
| injury_status | player.injuryStatus | "ACTIVE", "QUESTIONABLE", "OUT", etc. |
| average_draft_position | player.ownership.averageDraftPosition | Float value |
| drafted_by | null | Historical data doesn't have league context |
| locked | false | Historical data not locked |
| player_rating | CALCULATED | See player rating algorithm below |
| projected_points | stats[statSourceId=1] → fantasy points | Sum by week |
| actual_points | stats[statSourceId=0] → fantasy points | Sum by week |
| stat arrays | stats[statSourceId=0].stats[statId] → stat values | Extract per week |

**raw_stats Field:**
- **Source:** `player.stats` array from ESPN API response
- **Structure:** Array of stat objects, each containing:
  - `scoringPeriodId`: Week number (1-17)
  - `statSourceId`: 0 (actual) or 1 (projected)
  - `stats`: Dictionary mapping statId → value
- **NEW REQUIREMENT:** Add `raw_stats` field to `PlayerData` dataclass
- **Population:** Extract from `player_info.get('stats', [])` in player_data_fetcher.py

**Player Rating Algorithm:**
- **Week 1:** Use original draft-based rating from `average_draft_position`
- **Week 2+:** Calculate from cumulative actual points through week N-1
  1. Group players by position
  2. Calculate cumulative actual points for each player (weeks 1 to N-1)
  3. Rank players within position by cumulative points (descending)
  4. Apply formula: `rating = 100 - ((position_rank - 1) / (total_in_position - 1)) * 99`
  5. Clamp to range [1.0, 100.0]
- **Reference:** `historical_data_compiler/weekly_snapshot_generator.py:47-108`

---

## Implementation Approach

### Architecture Overview

**Current Historical Compiler Structure:**
```
historical_data_compiler/
├── constants.py              # Constants (ESPN API, team mappings, file names)
├── player_data_fetcher.py    # Fetch player data from ESPN API
├── team_rankings_fetcher.py  # Fetch team rankings
├── weekly_snapshot_generator.py  # Generate CSV snapshots (EXTEND THIS)
└── ... other modules
```

**New Files to Create:**
```
historical_data_compiler/
└── json_exporter.py          # NEW: JSON export with bridge adapter
```

**Modified Files:**
1. `compile_historical_data.py` - Add boolean toggles, call JSON generation
2. `historical_data_compiler/constants.py` - Add JSON file name constants
3. `historical_data_compiler/player_data_fetcher.py` - Add raw_stats field to PlayerData
4. `historical_data_compiler/weekly_snapshot_generator.py` - Call JSON exporter (or integrate into this file)

### Implementation Steps

**Step 1: Add Configuration Toggles**
- File: `compile_historical_data.py`
- Add at top of file:
  ```python
  # Output format toggles
  GENERATE_CSV = True   # Generate legacy CSV files (players.csv, players_projected.csv)
  GENERATE_JSON = True  # Generate new JSON files (qb_data.json, rb_data.json, etc.)
  ```
- Update main execution logic to check toggles before generating outputs

**Step 2: Update Constants**
- File: `historical_data_compiler/constants.py`
- Add after line 117 (after CSV file names):
  ```python
  # JSON file names
  QB_DATA_FILE = "qb_data.json"
  RB_DATA_FILE = "rb_data.json"
  WR_DATA_FILE = "wr_data.json"
  TE_DATA_FILE = "te_data.json"
  K_DATA_FILE = "k_data.json"
  DST_DATA_FILE = "dst_data.json"
  POSITION_JSON_FILES = {
      'QB': QB_DATA_FILE,
      'RB': RB_DATA_FILE,
      'WR': WR_DATA_FILE,
      'TE': TE_DATA_FILE,
      'K': K_DATA_FILE,
      'DST': DST_DATA_FILE
  }
  ```

**Step 3: Extend PlayerData Model**
- File: `historical_data_compiler/player_data_fetcher.py`
- Add `raw_stats` field to PlayerData dataclass:
  ```python
  @dataclass
  class PlayerData:
      # ... existing fields ...
      raw_stats: List[Dict[str, Any]] = field(default_factory=list)  # NEW
  ```
- In `_create_player_data()` method (around line 450), add:
  ```python
  player = PlayerData(
      # ... existing fields ...
      raw_stats=player_info.get('stats', [])  # NEW: Extract raw stats array
  )
  ```

**Step 4: Create JSON Exporter with Bridge Adapter**
- File: `historical_data_compiler/json_exporter.py` (NEW)
- Import stat extraction methods from player_data_exporter
- Create PlayerDataAdapter class to convert PlayerData → ESPNPlayerData-like object
- Implement JSON generation for each position
- Apply point-in-time logic to all arrays
- Export 6 JSON files per week

**Step 5: Integrate JSON Generation into Workflow**
- File: `historical_data_compiler/weekly_snapshot_generator.py`
- Add method `_generate_json_snapshots()` or call json_exporter
- Call from `_generate_week_snapshot()` if GENERATE_JSON=True
- Pass current_week for point-in-time logic

**Step 6: Update Main Runner**
- File: `compile_historical_data.py`
- Check GENERATE_CSV toggle before calling CSV generation
- Check GENERATE_JSON toggle before calling JSON generation
- Pass toggles to weekly snapshot generator

---

## Edge Cases and Special Handling

### Bye Weeks
- **Representation:** 0.0 in all arrays (actual_points, projected_points, all stat arrays)
- **Logic:** Always 0.0 regardless of current_week (bye is always known)
- **Detection:** player.bye_week field from ESPN API

### Injured Players
- **Inclusion:** YES - include all players regardless of injury status
- **Handling:** Set injury_status field from ESPN API ("ACTIVE", "QUESTIONABLE", "OUT", "DOUBTFUL", "IR", etc.)
- **Stats:** Use actual stats if player played (even if injured), 0.0 if didn't play
- **Rationale:** Simulation needs complete player pool to match real drafts

### Mid-Season Player Additions
- **Week appearance:** Player only appears in weeks they were active in ESPN data
- **Historical weeks:** No retroactive zeros (player didn't exist in those snapshots)
- **Example:** Rookie added week 5 → appears in week_05/ through week_17/ only
- **Rationale:** Matches point-in-time reality (player wasn't draftable earlier)

### Missing Data
- **Missing projections:** If statSourceId=1 data missing for a week, use 0.0
- **Missing actuals:** If statSourceId=0 data missing (shouldn't happen for past weeks), use 0.0
- **Missing raw_stats:** If stats array empty, all stat arrays will be zeros
- **Logging:** Log warnings for unexpected missing data

### Team Changes (Trades/Releases)
- **Team field:** Reflects current team at that week's snapshot
- **Historical accuracy:** Player's team may change across weeks
- **Example:** Week 5 snapshot shows team A, week 12 snapshot shows team B (after trade)

### Position Changes
- **Position field:** Use defaultPositionId from ESPN API
- **Eligibility:** Player appears in JSON file for their official position
- **Multi-position players:** ESPN assigns single primary position

---

## Testing Strategy

### Unit Tests
- **PlayerData model:** Test raw_stats field addition
- **Constants:** Verify JSON file name mappings
- **Bridge adapter:** Test PlayerData → ESPNPlayerData conversion
- **Point-in-time logic:** Test array generation for various current_week values
- **Player rating calculation:** Test recalculation algorithm

### Integration Tests
- **Full week generation:** Generate complete week folder (CSV + JSON if both toggles enabled)
- **Toggle behavior:** Test GENERATE_CSV=False, GENERATE_JSON=False, both True, both False
- **Structure validation:** Load generated JSON and verify schema matches current format
- **Field verification:** All required fields present with correct types

### Smoke Testing Protocol (MANDATORY)

**Part 1: Import Test**
```bash
python -c "from historical_data_compiler import json_exporter"
```
Expected: No import errors

**Part 2: Generation Test**
```bash
python compile_historical_data.py --year 2023 --weeks 1-3
```
Expected: Successfully generates 3 week folders with JSON files

**Part 3: Structure Validation**
```python
# Load generated JSON
with open('sim_data/2023/weeks/week_01/qb_data.json') as f:
    data = json.load(f)

# Verify structure matches current format
assert 'qb_data' in data
assert all(required_field in data['qb_data'][0] for required_field in [
    'id', 'name', 'team', 'position', 'projected_points', 'actual_points'
])
```

**Part 4: Point-in-Time Verification**
- Manual inspection of week_01, week_08, week_17
- Verify actual_points: weeks 1 to N-1 have values, weeks N+ are zeros
- Verify projected_points: all weeks have values (historical or repeated)
- Verify stat arrays: follow same point-in-time logic

**Part 5: Historical Projection Quality Check** 🛑 **MANDATORY STOP POINT**
1. Generate historical data for test season (e.g., 2023)
2. Extract projection quality metrics
3. **🛑 STOP AND REPORT TO USER** - Present findings
4. **WAIT FOR USER DECISION** - Proceed or implement fallback
5. Document decision in lessons learned

### Manual Testing
- **Sample weeks:** Review week_01, week_08, week_17 outputs
- **Player variety:** Check QB, RB, WR, TE, K, DST samples
- **Edge cases:** Verify bye weeks, injuries, mid-season additions
- **Comparison:** Compare CSV vs JSON data for consistency

---

## Out of Scope (Future Features)

### Simulation System Updates ❌
- Updating simulation to load JSON files instead of CSV
- Modifying SimulatedLeague, SimulationManager, etc.
- Consumer roundtrip testing with simulation

### League Helper Updates ❌
- Updating league helper classes to use new stat fields
- Incorporating new stats into player scoring algorithm
- UI changes to display new statistics

### Scoring Weight Optimization ❌
- Running simulations to optimize weights for new metrics
- Parameter tuning for new stat fields
- Accuracy analysis with enhanced data

### Historical Data Backfill ❌
- Generating JSON files for all past seasons (2021-2024)
- Bulk historical data compilation
- (Can be done manually after feature is complete)

---

## File Change Summary

### New Files
| File | Purpose | Lines (Est.) |
|------|---------|--------------|
| `historical_data_compiler/json_exporter.py` | JSON export with bridge adapter | ~500 |

### Modified Files
| File | Changes | Lines (Est.) |
|------|---------|--------------|
| `compile_historical_data.py` | Add toggles, call JSON generation | +20 |
| `historical_data_compiler/constants.py` | Add JSON file name constants | +15 |
| `historical_data_compiler/player_data_fetcher.py` | Add raw_stats field to PlayerData | +5 |
| `historical_data_compiler/weekly_snapshot_generator.py` | Integrate JSON generation | +30 |

**Total estimated changes:** ~570 lines (mostly new code, minimal modifications)

---

## Dependencies and Imports

### Required Imports for json_exporter.py
```python
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

# Import stat extraction methods
import sys
sys.path.append(str(Path(__file__).parent.parent))
from player-data-fetcher.player_data_exporter import PlayerDataExporter

# Local imports
from .constants import POSITION_JSON_FILES, REGULAR_SEASON_WEEKS
from .player_data_fetcher import PlayerData
from utils.LoggingManager import get_logger
```

### External Dependencies
- **Standard library:** json, pathlib, typing, dataclasses
- **Project modules:** player_data_exporter (stat extraction), constants, PlayerData model
- **No new external packages required**

---

## Success Criteria

### Feature Complete When:
- ✅ Boolean toggles added to compile_historical_data.py
- ✅ JSON file name constants added to constants.py
- ✅ raw_stats field added to PlayerData model
- ✅ json_exporter.py created with bridge adapter pattern
- ✅ JSON generation integrated into weekly_snapshot_generator.py
- ✅ All unit tests passing (100%)
- ✅ Integration tests passing (toggle behavior, structure validation)
- ✅ Smoke tests passing (import, generation, structure, point-in-time)
- ✅ Historical projection quality verified with user
- ✅ Manual inspection of sample weeks complete
- ✅ Code changes documented
- ✅ Lessons learned reviewed and guides updated

### Quality Gates
- **Code quality:** Follows project coding standards (Google docstrings, type hints, error handling)
- **Test coverage:** 100% pass rate on all tests
- **Structure validation:** Generated JSON matches current player_data format exactly
- **Point-in-time correctness:** Arrays follow specified logic for all weeks
- **Backward compatibility:** CSV generation still works when GENERATE_CSV=True
- **User verification:** Historical projection quality approved by user

---

## Status: PLANNING COMPLETE ✅

**All 5 critical decisions resolved**
**Ready for Phase 3: Report and Pause**
**Next step: User review, then proceed to TODO creation (feature_development_guide.md)**
