# Sub-Feature 6: TeamDataManager D/ST Migration

## Objective
Migrate TeamDataManager._load_dst_player_data() from reading week_N_points columns in players.csv to reading actual_points arrays from dst_data.json.

## Dependencies
**Prerequisites:** Sub-feature 2 (Weekly Data Migration)
**Blocks:** None

## Scope (8 items)
- NEW-110 to NEW-117: TeamDataManager D/ST migration

**From checklist:**
- NEW-110: Update _load_dst_player_data() to read from JSON
- NEW-111: Extract actual_points arrays for each D/ST team
- NEW-112: Update error handling for JSON loading
- NEW-113: Update method docstring
- NEW-114: Update data structure comment
- NEW-115 to NEW-117: Testing

## Verification Findings (From Deep Dive)

### Current Implementation Verified

**_load_dst_player_data() location:** league_helper/util/TeamDataManager.py:110-165

**Current behavior (lines 123-158):**
- Opens players.csv
- Filters for rows where position == 'DST'
- Extracts week_1_points through week_17_points columns (lines 146-156)
- Builds dictionary: `{team: [week_1, ..., week_17]}`
- Stores in `self.dst_player_data` (line 158)

**Data structure comment (line 83):**
```python
# D/ST player data: {team: [week_1_points, week_2_points, ..., week_17_points]}
```
**Format is correct and will remain unchanged**

**Method docstring (lines 111-120):**
- **Current:** "Load D/ST weekly fantasy scores from players.csv"
- **Update to:** "Load D/ST weekly fantasy scores from dst_data.json actual_points arrays"

### Usage Verified

**Used by:** PlayerManager.py:206 for D/ST fantasy performance rankings
- Feeds into team quality multiplier calculation (scoring algorithm step 4)
- **Critical for scoring accuracy** - affects all player positions

**Rolling window calculations (_rank_dst_fantasy lines 248-270):**
- Takes average of last N weeks of D/ST fantasy points
- Uses this to rank D/ST units by recent performance
- **Requires ACTUAL historical data** (not projections)

### Data Source Decision

**Use actual_points array (not projected_points):**
- **Reason:** Rolling window needs ACTUAL past performance
- projected_points = pre-season estimates (don't change week to week)
- actual_points = real game results (what actually happened)

**Verified in:** data/player_data/dst_data.json structure

## Key Implementation

**CRITICAL FINDING:**
TeamDataManager._load_dst_player_data() currently reads from players.csv using week_N_points columns. This breaks with CSV elimination.

**Current (lines 123-158):**
```python
# Reads from players.csv looking for position='DST'
# Extracts week_1_points through week_17_points columns
```

**New implementation:**
```python
def _load_dst_player_data(self) -> None:
    """Load D/ST weekly fantasy scores from dst_data.json."""
    dst_json_path = self.data_folder / 'player_data' / 'dst_data.json'

    with open(dst_json_path, 'r') as f:
        data = json.load(f)

    dst_players = data.get('dst_data', [])

    for dst_player in dst_players:
        team = dst_player.get('team', '').upper()
        actual_points = dst_player.get('actual_points', [0.0] * 17)

        # Store in same format: {team: [week_1, ..., week_17]}
        self.dst_player_data[team] = actual_points
```

**Data structure preserved:** {team: [week_1_points, ..., week_17_points]}
**No interface changes** - callers still use get_team_dst_fantasy_rank() the same way

## Success Criteria
- [x] _load_dst_player_data() reads from dst_data.json ✅
- [x] actual_points arrays extracted correctly ✅
- [x] D/ST fantasy rankings working ✅ (17/17 integration tests passing)
- [x] Team quality multiplier calculations verified ✅ (no regressions)

See `research/` for analysis that discovered this critical dependency.
