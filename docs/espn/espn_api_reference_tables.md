# ESPN Fantasy Football API - Reference Tables

**Last Updated**: 2025-12-13
**API Status**: Unofficial
**Target Audience**: Python Developers (Intermediate)

---

## Table of Contents

1. [Overview](#overview)
2. [Position ID Mappings](#position-id-mappings)
3. [Team ID Mappings](#team-id-mappings)
4. [Stat Source ID Mappings](#stat-source-id-mappings)
5. [Scoring Period ID Mappings](#scoring-period-id-mappings)
6. [Stat Split Type ID Mappings](#stat-split-type-id-mappings)
7. [Scoring Format ID Mappings](#scoring-format-id-mappings)
8. [Usage Examples](#usage-examples)

---

## Overview

This document provides comprehensive mapping tables for ESPN Fantasy Football API constants. These mappings are essential for:

- **Translating numeric IDs to human-readable names** (teams, positions)
- **Understanding data sources** (actual vs projected stats)
- **Interpreting time periods** (season vs weekly data)
- **Selecting scoring formats** (PPR, Standard, Half-PPR)

### Why These Mappings Matter

ESPN API uses numeric IDs throughout its responses. Without these mappings, you'll see:
- `proTeamId: 12` instead of "Kansas City Chiefs"
- `defaultPositionId: 1` instead of "QB"
- `statSourceId: 0` instead of "actual results"

**All mappings are based on ESPN API behavior as of 2025-10-31 and may change.**

---

## Position ID Mappings

Maps `defaultPositionId` values to fantasy football positions.

### Standard Fantasy Positions

| Position ID | Position Name | Description | Roster Count (typical) |
|------------|--------------|-------------|----------------------|
| 1 | QB | Quarterback | 1-2 per team |
| 2 | RB | Running Back | 2-4 per team |
| 3 | WR | Wide Receiver | 2-4 per team |
| 4 | TE | Tight End | 1-2 per team |
| 5 | K | Kicker | 1 per team |
| 16 | DST | Defense/Special Teams | 1 per team |

### IDP Positions (Individual Defensive Players)

> **Note**: These positions appear in API responses but are only relevant for IDP leagues.

| Position ID | Position Name | Description |
|------------|--------------|-------------|
| 9 | DT | Defensive Tackle |
| 8 | DL | Defensive Line (generic) |
| 10 | DE | Defensive End |
| 11 | LB | Linebacker |
| 12 | CB | Cornerback |
| 13 | S | Safety |
| 14 | DB | Defensive Back (generic) |
| 15 | DP | IDP Flex |

### Notes

- **DST vs IDP**: Position 16 (DST) represents entire team defense. Positions 8-15 are individual defensive players for IDP leagues.
- **DST not in default response**: DST entries require using the `sortPercOwned` filter (see examples below)
- **Flex eligibility**: Most leagues allow RB (2), WR (3), and TE (4) in FLEX slots

### Usage in API Responses

```json
{
  "player": {
    "id": 3139477,
    "firstName": "Patrick",
    "lastName": "Mahomes",
    "defaultPositionId": 1  // ← Translates to "QB"
  }
}
```

### Python Example

```python
ESPN_POSITION_MAPPINGS = {
    1: 'QB',
    2: 'RB',
    3: 'WR',
    4: 'TE',
    5: 'K',
    16: 'DST'
}

position_id = 1
position_name = ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN')
print(position_name)  # Output: QB
```

---

## Team ID Mappings

Maps `proTeamId` values to NFL team abbreviations. All 32 NFL teams included.

### AFC Teams

| Team ID | Abbreviation | Full Name | Division |
|---------|-------------|-----------|----------|
| 2 | BUF | Buffalo Bills | AFC East |
| 15 | MIA | Miami Dolphins | AFC East |
| 17 | NE | New England Patriots | AFC East |
| 20 | NYJ | New York Jets | AFC East |
| 33 | BAL | Baltimore Ravens | AFC North |
| 4 | CIN | Cincinnati Bengals | AFC North |
| 5 | CLE | Cleveland Browns | AFC North |
| 23 | PIT | Pittsburgh Steelers | AFC North |
| 34 | HOU | Houston Texans | AFC South |
| 11 | IND | Indianapolis Colts | AFC South |
| 30 | JAX | Jacksonville Jaguars | AFC South |
| 10 | TEN | Tennessee Titans | AFC South |
| 7 | DEN | Denver Broncos | AFC West |
| 12 | KC | Kansas City Chiefs | AFC West |
| 13 | LV | Las Vegas Raiders | AFC West |
| 24 | LAC | Los Angeles Chargers | AFC West |

### NFC Teams

| Team ID | Abbreviation | Full Name | Division |
|---------|-------------|-----------|----------|
| 6 | DAL | Dallas Cowboys | NFC East |
| 19 | NYG | New York Giants | NFC East |
| 21 | PHI | Philadelphia Eagles | NFC East |
| 28 | WSH | Washington Commanders | NFC East |
| 3 | CHI | Chicago Bears | NFC North |
| 8 | DET | Detroit Lions | NFC North |
| 9 | GB | Green Bay Packers | NFC North |
| 16 | MIN | Minnesota Vikings | NFC North |
| 1 | ATL | Atlanta Falcons | NFC South |
| 29 | CAR | Carolina Panthers | NFC South |
| 18 | NO | New Orleans Saints | NFC South |
| 27 | TB | Tampa Bay Buccaneers | NFC South |
| 22 | ARI | Arizona Cardinals | NFC West |
| 14 | LAR | Los Angeles Rams | NFC West |
| 25 | SF | San Francisco 49ers | NFC West |
| 26 | SEA | Seattle Seahawks | NFC West |

### Notes

- **ID gaps exist**: IDs 31 and 32 are not assigned (no teams at those IDs)
- **Abbreviations are standard**: Match official NFL abbreviations
- **WSH not WAS**: Washington uses "WSH" in ESPN API (some endpoints may show "WAS")
- **LV not OAK**: Raiders moved from Oakland (OAK) to Las Vegas (LV) in 2020

### Usage in API Responses

```json
{
  "player": {
    "id": 3139477,
    "firstName": "Patrick",
    "lastName": "Mahomes",
    "proTeamId": 12  // ← Translates to "KC" (Kansas City Chiefs)
  }
}
```

### Python Example

```python
ESPN_TEAM_MAPPINGS = {
    1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL',
    7: 'DEN', 8: 'DET', 9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC',
    13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN', 17: 'NE', 18: 'NO',
    19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
    25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX',
    33: 'BAL', 34: 'HOU'
}

team_id = 12
team_abbr = ESPN_TEAM_MAPPINGS.get(team_id, 'UNK')
print(team_abbr)  # Output: KC
```

---

## Stat Source ID Mappings

Maps `statSourceId` values to data type classifications in player stats arrays.

| Stat Source ID | Data Type | Description | When Available |
|---------------|-----------|-------------|----------------|
| 0 | Actual Results | Real game statistics | After game completion |
| 1 | Projections | Estimated/predicted stats | Always (pre-game and post-game) |

### Understanding Stat Sources

ESPN provides **two types** of data for each week:

1. **Actual Results (statSourceId=0)**:
   - Real statistics from completed games
   - Most reliable for past weeks
   - Contains `appliedTotal` field (actual fantasy points scored)
   - Available after game completion

2. **Projections (statSourceId=1)**:
   - Estimated statistics (pre-game forecasts)
   - Available for all weeks (past, current, future)
   - Contains `appliedTotal` field (estimated fantasy points)
   - Less reliable than actuals but available sooner

> **⚠️ IMPORTANT (2025 API Change)**: Both stat sources now use `appliedTotal` for fantasy points. The `projectedTotal` field is **deprecated** and returns `null`.

### Priority Logic

When both exist for the same week, prefer actual results:

```python
def get_week_points(stats_array, week):
    """Extract fantasy points for a specific week, preferring actuals."""
    actual = None
    projected = None

    for stat in stats_array:
        if stat.get('scoringPeriodId') != week:
            continue

        source = stat.get('statSourceId')
        points = stat.get('appliedTotal')  # Both sources use appliedTotal now

        if source == 0:
            actual = points
        elif source == 1:
            projected = points

    return actual if actual is not None else projected
```

### Usage in API Responses

```json
{
  "player": {
    "stats": [
      {
        "seasonId": 2025,
        "scoringPeriodId": 1,
        "statSourceId": 0,      // ← Actual results
        "appliedTotal": 28.5    // ← Real points scored
      },
      {
        "seasonId": 2025,
        "scoringPeriodId": 1,
        "statSourceId": 1,      // ← Projection
        "appliedTotal": 25.2    // ← Both use appliedTotal now
        // Note: projectedTotal field no longer exists in response
      }
    ]
  }
}
```

### Notes

- **Both can exist**: Same week may have both actual and projected entries
- **Actuals are final**: Once a game is played, statSourceId=0 is authoritative
- **Projections update**: ESPN may revise projections throughout the week
- **DST can be negative**: Defense/special teams can have negative fantasy points

---

## Scoring Period ID Mappings

Maps `scoringPeriodId` values to time periods.

| Scoring Period ID | Time Period | Description |
|------------------|-------------|-------------|
| 0 | Season Total/All Weeks | Aggregate or all-weeks data |
| 1-17 | Week 1-17 | Regular season weeks |
| 18 | Week 18 | Final regular season week |

### Special Behaviors

**scoringPeriodId = 0 has two meanings**:

1. **In query parameter**: Fetches data for ALL weeks (optimization)
   ```
   ?scoringPeriodId=0  ← Returns weeks 1-18 in one response
   ```

2. **In response data**: Sometimes represents season-total statistics
   ```json
   {"scoringPeriodId": 0, "appliedTotal": 285.6}  // ← Season total
   ```

### Week Range

- **Weeks 1-17**: Standard fantasy regular season
- **Week 18**: Final NFL week (some leagues extend to week 18)
- **Playoffs**: Typically weeks 15-17 in fantasy leagues

### Usage in API Responses

```json
{
  "player": {
    "stats": [
      {"scoringPeriodId": 0, "appliedTotal": 285.6},   // Season total
      {"scoringPeriodId": 1, "appliedTotal": 28.5},    // Week 1
      {"scoringPeriodId": 2, "appliedTotal": 22.3}     // Week 2
    ]
  }
}
```

### Python Example

```python
def get_time_period_label(scoring_period_id):
    if scoring_period_id == 0:
        return "Season/All Weeks"
    elif 1 <= scoring_period_id <= 18:
        return f"Week {scoring_period_id}"
    else:
        return "Unknown Period"
```

---

## Stat Split Type ID Mappings

Maps `statSplitTypeId` values to data aggregation types in player stats arrays.

| Stat Split Type ID | Split Type | Description |
|-------------------|------------|-------------|
| 0 | Season Total | Aggregated stats for entire season |
| 1 | Weekly Split | Individual week statistics |
| 2 | Last N Games | Stats over a period (e.g., last 4 weeks) |

### Understanding Stat Splits

The `statSplitTypeId` field indicates how the statistics are aggregated:

1. **Season Total (statSplitTypeId=0)**:
   - Aggregated statistics across the entire season
   - Used with `scoringPeriodId=0` entries
   - Contains `appliedAverage` field for per-game average
   - Best for overall player evaluation

2. **Weekly Split (statSplitTypeId=1)**:
   - Individual week statistics
   - Used with `scoringPeriodId=1-18` entries
   - No `appliedAverage` field
   - Best for week-by-week analysis

3. **Last N Games (statSplitTypeId=2)**:
   - Rolling average over recent games
   - Used for hot/cold streak analysis
   - Contains `appliedAverage` field

### Usage in API Responses

```json
{
  "player": {
    "stats": [
      {
        "scoringPeriodId": 0,
        "statSplitTypeId": 0,    // ← Season total
        "appliedTotal": 324.92,
        "appliedAverage": 19.11   // ← Present in season totals
      },
      {
        "scoringPeriodId": 1,
        "statSplitTypeId": 1,    // ← Weekly split
        "appliedTotal": 26.02
        // No appliedAverage for weekly splits
      }
    ]
  }
}
```

### Python Example

```python
def get_season_average(stats_array, stat_source_id=1):
    """Get season average points from stats array."""
    for stat in stats_array:
        if (stat.get('scoringPeriodId') == 0 and
            stat.get('statSplitTypeId') == 0 and
            stat.get('statSourceId') == stat_source_id):
            return stat.get('appliedAverage')
    return None

# Usage
avg_projected = get_season_average(player['stats'], stat_source_id=1)
avg_actual = get_season_average(player['stats'], stat_source_id=0)
print(f"Projected PPG: {avg_projected:.1f}")
print(f"Actual PPG: {avg_actual:.1f}")
```

---

## Scoring Format ID Mappings

Maps scoring format IDs used in API URLs (specifically in the `leaguedefaults/{format_id}` path).

| Format ID | Scoring Format | Points Per Reception | Status |
|-----------|---------------|---------------------|--------|
| 1 | Standard | 0 | ✅ Works |
| 2 | ~~Half-PPR~~ | ~~0.5~~ | ❌ Returns 404 |
| 3 | PPR (Full) | 1.0 | ✅ Works |
| 5 | PPR (alternate) | 1.0 | ✅ Works |

> **⚠️ IMPORTANT (Verified 2025-12-13)**: Format ID 2 (previously documented as Half-PPR) returns HTTP 404. ESPN may have removed Half-PPR as a public format option. Only formats 1, 3, and 5 are confirmed working. Format 5 appears to return the same values as Format 3 (PPR).

### Usage in API URLs

The format ID appears in the endpoint path:

```
https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3
                                                                                            ↑
                                                                                         Format ID (3 = PPR)
```

### Choosing Format

```python
from enum import Enum

class ScoringFormat(str, Enum):
    STANDARD = "std"
    PPR = "ppr"
    HALF_PPR = "half"

def get_format_id(scoring_format: ScoringFormat) -> int:
    """Convert scoring format to ESPN API format ID"""
    format_map = {
        ScoringFormat.STANDARD: 1,
        ScoringFormat.HALF_PPR: 2,
        ScoringFormat.PPR: 3
    }
    return format_map.get(scoring_format, 3)  # Default to PPR

# Usage
format_id = get_format_id(ScoringFormat.PPR)  # Returns 3
url = f"https://lm-api-reads.fantasy.espn.com/.../leaguedefaults/{format_id}"
```

### Impact on Projections

- **Different projections**: Each format returns different point totals
- **WR/RB most affected**: Positions with many receptions see biggest differences
- **QB/K/DST less affected**: These positions get few/no reception points

### Notes

- **Format affects rankings**: Top players differ between Standard and PPR
- **Draft strategy changes**: PPR favors pass-catching RBs and slot WRs
- **Must match league**: Use the format ID that matches your league settings

---

## Usage Examples

### Complete Player Lookup

```python
import httpx

# Configuration
ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
SEASON = 2025
FORMAT_ID = 3  # PPR

# Mappings
POSITION_MAP = {1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'DST'}
TEAM_MAP = {12: 'KC', 17: 'NE', 25: 'SF'}  # ... full map in code

# Fetch player data
url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leaguedefaults/{FORMAT_ID}"
headers = {"User-Agent": ESPN_USER_AGENT}
params = {"view": "kona_player_info", "scoringPeriodId": 0}

response = httpx.get(url, headers=headers, params=params)
data = response.json()

# Parse with mappings
for player_obj in data.get('players', []):
    player = player_obj['player']

    # Translate IDs to names
    position = POSITION_MAP.get(player['defaultPositionId'], 'UNKNOWN')
    team = TEAM_MAP.get(player['proTeamId'], 'UNK')
    name = f"{player['firstName']} {player['lastName']}"

    print(f"{name} ({position}, {team})")
```

### Parsing Weekly Stats

```python
def get_week_points(stats_array, week, prefer_actual=True):
    """
    Extract fantasy points for a specific week.

    Args:
        stats_array: Player's stats array from API
        week: Week number (1-18)
        prefer_actual: If True, prefer statSourceId=0 over statSourceId=1

    Returns:
        Fantasy points for the week, or None if not found
    """
    actual_points = None
    projected_points = None

    for stat in stats_array:
        if stat.get('scoringPeriodId') != week:
            continue

        stat_source = stat.get('statSourceId')

        if stat_source == 0:  # Actual results
            actual_points = stat.get('appliedTotal')
        elif stat_source == 1:  # Projections (also uses appliedTotal now)
            projected_points = stat.get('appliedTotal')

    # Return actual if available and preferred, otherwise projected
    if prefer_actual and actual_points is not None:
        return actual_points
    elif projected_points is not None:
        return projected_points

    return None

# Usage
stats = player['stats']
week_1_points = get_week_points(stats, week=1)
print(f"Week 1: {week_1_points} points")
```

### Building Full Team Roster

```python
# Get all players
players = fetch_all_players()  # Your API call function

# Group by team
from collections import defaultdict
teams = defaultdict(list)

for player_obj in players:
    player = player_obj['player']
    team_id = player['proTeamId']
    team_abbr = ESPN_TEAM_MAPPINGS.get(team_id, 'UNK')

    if team_abbr != 'UNK':
        position = ESPN_POSITION_MAPPINGS.get(player['defaultPositionId'], 'UNKNOWN')
        teams[team_abbr].append({
            'name': f"{player['firstName']} {player['lastName']}",
            'position': position
        })

# Print KC Chiefs roster
print("Kansas City Chiefs Roster:")
for player in teams['KC']:
    print(f"  {player['position']}: {player['name']}")
```

---

## Cross-References

- **API Endpoints**: See [espn_api_endpoints.md](espn_api_endpoints.md) for complete endpoint documentation
- **Player Data**: See [espn_player_data.md](espn_player_data.md) for full player field reference
- **Team Data**: See [espn_team_data.md](espn_team_data.md) for full team field reference
- **Examples**: See [examples/](examples/) for real API response examples

---

## Changelog

- **2025-12-13**: Verified and expanded documentation
  - Added IDP position IDs (8-15) for individual defensive players
  - Added statSplitTypeId mappings section
  - Fixed projectedTotal deprecation (now appliedTotal for both sources)
  - Verified all 32 team IDs against live API
  - Confirmed format ID 2 returns 404
- **2025-10-31**: Initial version - all mappings documented
- Mappings sourced from `player-data-fetcher/player_data_constants.py`
- Verified against live ESPN API responses

---

## ⚠️ Disclaimer

ESPN Fantasy Football API is **unofficial** and **undocumented**. These mappings are based on observed behavior and may change without notice. Use at your own risk and implement proper error handling.

**Not affiliated with ESPN.**
