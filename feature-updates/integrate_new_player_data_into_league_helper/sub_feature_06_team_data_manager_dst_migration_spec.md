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
- [ ] _load_dst_player_data() reads from dst_data.json
- [ ] actual_points arrays extracted correctly
- [ ] D/ST fantasy rankings working
- [ ] Team quality multiplier calculations verified

See `research/` for analysis that discovered this critical dependency.
