# ESPN Fantasy Football API - Player Data Reference

**Last Updated**: 2025-10-31
**API Status**: Unofficial
**Target Audience**: Python Developers (Intermediate)

---

## Table of Contents

1. [Overview](#overview)
2. [Player Object Structure](#player-object-structure)
3. [Basic Information Fields](#basic-information-fields)
4. [Team & Position Fields](#team--position-fields)
5. [Fantasy Scoring Fields](#fantasy-scoring-fields)
6. [Ownership & Draft Fields](#ownership--draft-fields)
7. [Statistics Array](#statistics-array)
8. [Injury Information](#injury-information)
9. [Optional Fields](#optional-fields)
10. [Data Validation](#data-validation)
11. [Complete Examples](#complete-examples)

---

## Overview

ESPN's player data structure contains comprehensive information for fantasy football analysis. This document details every field available in player responses.

### Response Container

```json
{
  "players": [
    {
      "player": { /* Player object documented here */ }
    }
  ]
}
```

Player data is wrapped in a `players` array, where each element contains a `player` object.

### Field Availability

- **Always Present**: id, firstName, lastName, defaultPositionId
- **Usually Present**: proTeamId, stats array
- **Often Present**: ownership, draftRanksByRankType
- **Sometimes Present**: injuryStatus, draftAuctionValue
- **Rarely Present**: Custom league-specific fields

---

## Player Object Structure

### High-Level Structure

```json
{
  "player": {
    // Basic Information
    "id": 3139477,
    "firstName": "Patrick",
    "lastName": "Mahomes",
    "fullName": "Patrick Mahomes",

    // Team & Position
    "defaultPositionId": 1,
    "proTeamId": 12,
    "eligibleSlots": [0, 16],

    // Injury
    "injuryStatus": "ACTIVE",

    // Ownership & Draft
    "ownership": { ... },
    "draftRanksByRankType": { ... },

    // Statistics
    "stats": [ ... ]
  }
}
```

---

## Basic Information Fields

### player.id

**Type**: `integer` or `string`
**Required**: Yes
**Description**: Unique ESPN player identifier

```json
"id": 3139477
```

**Notes**:
- Persistent across seasons
- Can be used to filter specific players via X-Fantasy-Filter
- Sometimes returned as string, sometimes as integer (handle both)

**Usage**:
```python
player_id = str(player['id'])  # Convert to string for consistency
```

### player.firstName

**Type**: `string`
**Required**: Yes
**Description**: Player's first name

```json
"firstName": "Patrick"
```

### player.lastName

**Type**: `string`
**Required**: Yes
**Description**: Player's last name

```json
"lastName": "Mahomes"
```

### player.fullName

**Type**: `string`
**Required**: Usually
**Description**: Complete player name (first + last)

```json
"fullName": "Patrick Mahomes"
```

**Notes**:
- Sometimes missing for obscure players
- Can be constructed from firstName + lastName if absent

**Usage**:
```python
full_name = player.get('fullName') or f"{player['firstName']} {player['lastName']}"
```

---

## Team & Position Fields

### player.defaultPositionId

**Type**: `integer`
**Required**: Yes
**Description**: Player's primary fantasy position

```json
"defaultPositionId": 1
```

**Mappings**:
| ID | Position |
|----|----------|
| 1  | QB       |
| 2  | RB       |
| 3  | WR       |
| 4  | TE       |
| 5  | K        |
| 16 | DST      |

**See**: [espn_api_reference_tables.md](espn_api_reference_tables.md#position-id-mappings) for complete mapping

**Usage**:
```python
POSITION_MAP = {1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'DST'}
position = POSITION_MAP.get(player['defaultPositionId'], 'UNKNOWN')
```

### player.proTeamId

**Type**: `integer`
**Required**: Yes
**Description**: NFL team the player belongs to

```json
"proTeamId": 12
```

**Mappings**: See [espn_api_reference_tables.md](espn_api_reference_tables.md#team-id-mappings)

**Special Values**:
- Valid IDs: 1-34 (gaps at 31-32)
- Free agents: Sometimes show invalid IDs or 0

**Usage**:
```python
TEAM_MAP = {12: 'KC', 17: 'NE', ...}  # See reference tables
team = TEAM_MAP.get(player['proTeamId'], 'UNK')
```

### player.eligibleSlots

**Type**: `array of integers`
**Required**: Usually
**Description**: Roster slots this player can fill

```json
"eligibleSlots": [0, 2, 16, 17]
```

**Common Slot IDs**:
| ID | Slot Type |
|----|-----------|
| 0  | QB        |
| 2  | RB        |
| 3  | RB/WR     |
| 4  | WR        |
| 6  | TE        |
| 16 | DST       |
| 17 | K         |
| 20 | BENCH     |
| 21 | IR        |
| 23 | FLEX      |

**Notes**:
- Multi-position eligibility shown (e.g., RB/WR for certain players)
- All players eligible for BENCH (20)

---

## Fantasy Scoring Fields

Fantasy scoring comes primarily from the `stats` array (see [Statistics Array](#statistics-array)), but some aggregate fields may appear at the player level.

### Derived from stats array

Most scoring data is in `player.stats[]`:

```json
"stats": [
  {
    "seasonId": 2025,
    "scoringPeriodId": 0,
    "statSourceId": 1,
    "appliedTotal": 285.6,
    "projectedTotal": 285.6
  }
]
```

See [Statistics Array](#statistics-array) section below for complete details.

---

## Ownership & Draft Fields

### player.ownership

**Type**: `object`
**Required**: Often (not always)
**Description**: Ownership and draft statistics

```json
"ownership": {
  "percentOwned": 99.8,
  "percentStarted": 95.2,
  "averageDraftPosition": 2.5,
  "auctionValueAverage": 65.0
}
```

#### ownership.percentOwned

**Type**: `float`
**Description**: Percentage of leagues where player is rostered

```json
"percentOwned": 99.8
```

**Range**: 0.0 - 100.0

#### ownership.percentStarted

**Type**: `float`
**Description**: Percentage of leagues where player is in starting lineup

```json
"percentStarted": 95.2
```

**Range**: 0.0 - 100.0

**Note**: Always ≤ percentOwned

#### ownership.averageDraftPosition

**Type**: `float`
**Description**: Average draft position across ESPN leagues (ADP)

```json
"averageDraftPosition": 2.5
```

**Range**: 1.0+ (lower = earlier draft pick)

**Special Values**:
- `null` or missing: Undrafted players (late-round/waiver wire)

**Usage**:
```python
adp = player.get('ownership', {}).get('averageDraftPosition')
if adp is None or adp > 200:
    print("Waiver wire candidate")
elif adp <= 24:  # 2 rounds in 12-team league
    print("Early-round pick")
```

#### ownership.auctionValueAverage

**Type**: `float`
**Description**: Average auction draft price

```json
"auctionValueAverage": 65.0
```

**Note**: Only relevant for auction leagues

### player.draftRanksByRankType

**Type**: `object`
**Required**: Often
**Description**: ESPN's draft rankings by scoring format

```json
"draftRanksByRankType": {
  "PPR": {
    "rank": 5,
    "rankSourceId": 1
  },
  "STANDARD": {
    "rank": 8,
    "rankSourceId": 1
  }
}
```

**Keys**: "PPR", "STANDARD", "HALF_PPR"

**Usage**:
```python
ppr_rank = player.get('draftRanksByRankType', {}).get('PPR', {}).get('rank')
if ppr_rank and ppr_rank <= 12:
    print("Top-12 player in PPR")
```

---

## Statistics Array

The `stats` array is the **most important part** of player data, containing all projections and actual results.

### Structure

```json
"stats": [
  {
    "seasonId": 2025,
    "scoringPeriodId": 1,
    "statSourceId": 0,
    "appliedTotal": 28.5,
    "appliedAverage": 28.5,
    "appliedStats": { ... }
  },
  {
    "seasonId": 2025,
    "scoringPeriodId": 1,
    "statSourceId": 1,
    "projectedTotal": 25.2,
    "projectedAverage": 25.2,
    "projectedStats": { ... }
  }
]
```

### stats[].seasonId

**Type**: `integer`
**Description**: NFL season year

```json
"seasonId": 2025
```

### stats[].scoringPeriodId

**Type**: `integer`
**Description**: Week number or season aggregate

```json
"scoringPeriodId": 1
```

**Values**:
- `0`: Season total or all-weeks aggregate
- `1-18`: Specific week number

**See**: [espn_api_reference_tables.md](espn_api_reference_tables.md#scoring-period-id-mappings)

### stats[].statSourceId

**Type**: `integer`
**Description**: Data type (actual vs projected)

```json
"statSourceId": 0
```

**Values**:
| ID | Type | Field with Points |
|----|------|------------------|
| 0  | Actual Results | `appliedTotal` |
| 1  | Projections    | `projectedTotal` |

**See**: [espn_api_reference_tables.md](espn_api_reference_tables.md#stat-source-id-mappings)

### stats[].appliedTotal

**Type**: `float`
**Description**: Actual fantasy points scored (when statSourceId=0)

```json
"appliedTotal": 28.5
```

**Notes**:
- Only present when statSourceId=0
- Reflects real game results
- Most reliable data source

### stats[].projectedTotal

**Type**: `float`
**Description**: Projected/estimated fantasy points (when statSourceId=1)

```json
"projectedTotal": 25.2
```

**Notes**:
- Present when statSourceId=1
- ESPN's forecast
- Less reliable than actual results

### Priority Logic

When both actual and projected exist for same week, prefer actual:

```python
def get_week_points(stats_array, week):
    actual = None
    projected = None

    for stat in stats_array:
        if stat.get('scoringPeriodId') != week:
            continue

        if stat.get('statSourceId') == 0:
            actual = stat.get('appliedTotal')
        elif stat.get('statSourceId') == 1:
            projected = stat.get('projectedTotal')

    return actual if actual is not None else projected
```

### stats[].appliedStats & projectedStats

**Type**: `object`
**Description**: Detailed stat breakdowns (passing yards, TDs, etc.)

```json
"appliedStats": {
  "3": 285.0,   // Passing yards
  "4": 2.0,     // Passing TDs
  "20": 15.0    // Rushing yards
}
```

**Notes**:
- Stat IDs are ESPN-internal codes
- Useful for custom scoring calculations
- Not all stats documented (ESPN internal)

---

## Injury Information

### player.injuryStatus

**Type**: `string`
**Required**: Sometimes
**Description**: Current injury status

```json
"injuryStatus": "QUESTIONABLE"
```

**Possible Values**:
- `"ACTIVE"`: Healthy, no injury
- `"QUESTIONABLE"`: Uncertain to play
- `"DOUBTFUL"`: Unlikely to play
- `"OUT"`: Confirmed out
- `"IR"`: Injured reserve (out for extended time)
- `"PUP"`: Physically unable to perform list
- `null` or missing: Assumed healthy

**Usage**:
```python
injury = player.get('injuryStatus', 'ACTIVE')
if injury not in ['ACTIVE', None]:
    print(f"WARNING: Player is {injury}")
```

---

## Optional Fields

### Fields that May Be Missing

**player.draftAuctionValue**
- Type: `float`
- Description: Player's auction value
- Present: Rarely

**player.ownership**
- Type: `object`
- Description: Ownership statistics
- Present: Often, but not guaranteed

**player.draftRanksByRankType**
- Type: `object`
- Description: Draft rankings
- Present: Often for drafted players only

**player.eligibleSlots**
- Type: `array`
- Description: Roster slot eligibility
- Present: Usually

### Handling Missing Fields

```python
# Safe access pattern
ownership = player.get('ownership', {})
adp = ownership.get('averageDraftPosition')

if adp is not None:
    print(f"ADP: {adp}")
else:
    print("No ADP data available")
```

---

## Data Validation

### Common Issues

**NaN Values**:
```python
import math

points = stat.get('projectedTotal')
if math.isnan(points):
    points = 0.0  # Or handle as missing data
```

**Type Inconsistencies**:
```python
# Player ID sometimes string, sometimes int
player_id = str(player['id'])

# ProTeamId sometimes missing
team_id = player.get('proTeamId', 0)
if team_id not in VALID_TEAM_IDS:
    team = 'UNK'
```

**Empty Stats Arrays**:
```python
stats = player.get('stats', [])
if not stats:
    print("No stats available for this player")
```

### Validation Function

```python
def validate_player_data(player):
    """Validate player data completeness"""
    required_fields = ['id', 'firstName', 'lastName', 'defaultPositionId']

    for field in required_fields:
        if field not in player:
            raise ValueError(f"Missing required field: {field}")

    # Validate position ID
    if player['defaultPositionId'] not in [1, 2, 3, 4, 5, 16]:
        raise ValueError(f"Invalid position ID: {player['defaultPositionId']}")

    # Validate stats array exists
    if 'stats' not in player or not isinstance(player['stats'], list):
        print(f"WARNING: Player {player['id']} has no stats array")

    return True
```

---

## Complete Examples

### Example 1: Full Player Object (QB)

```json
{
  "player": {
    "id": 3139477,
    "firstName": "Patrick",
    "lastName": "Mahomes",
    "fullName": "Patrick Mahomes",
    "defaultPositionId": 1,
    "proTeamId": 12,
    "eligibleSlots": [0, 16, 17],
    "injuryStatus": "ACTIVE",
    "ownership": {
      "percentOwned": 99.8,
      "percentStarted": 95.2,
      "averageDraftPosition": 2.5,
      "auctionValueAverage": 65.0
    },
    "draftRanksByRankType": {
      "PPR": {"rank": 5},
      "STANDARD": {"rank": 3}
    },
    "stats": [
      {
        "seasonId": 2025,
        "scoringPeriodId": 0,
        "statSourceId": 1,
        "projectedTotal": 285.6
      },
      {
        "seasonId": 2025,
        "scoringPeriodId": 1,
        "statSourceId": 0,
        "appliedTotal": 28.5
      },
      {
        "seasonId": 2025,
        "scoringPeriodId": 1,
        "statSourceId": 1,
        "projectedTotal": 25.2
      }
    ]
  }
}
```

### Example 2: Parsing Player Data

```python
def parse_player(player_obj):
    """Parse ESPN player object into simplified structure"""
    player = player_obj['player']

    # Basic info
    player_id = str(player['id'])
    name = player.get('fullName') or f"{player['firstName']} {player['lastName']}"

    # Position & Team
    position = POSITION_MAP.get(player['defaultPositionId'], 'UNKNOWN')
    team = TEAM_MAP.get(player.get('proTeamId', 0), 'UNK')

    # Injury
    injury = player.get('injuryStatus', 'ACTIVE')

    # Ownership
    ownership = player.get('ownership', {})
    adp = ownership.get('averageDraftPosition')
    pct_owned = ownership.get('percentOwned', 0.0)

    # Season projection
    season_points = None
    for stat in player.get('stats', []):
        if stat.get('scoringPeriodId') == 0 and stat.get('statSourceId') == 1:
            season_points = stat.get('projectedTotal')
            break

    return {
        'id': player_id,
        'name': name,
        'position': position,
        'team': team,
        'injury_status': injury,
        'adp': adp,
        'percent_owned': pct_owned,
        'projected_points': season_points
    }

# Usage
parsed = parse_player(player_obj)
print(f"{parsed['name']} ({parsed['position']}, {parsed['team']}): {parsed['projected_points']} pts")
```

### Example 3: Weekly Performance Tracking

```python
def extract_weekly_performance(player):
    """Extract all weekly actual results"""
    weekly_points = {}

    for stat in player.get('stats', []):
        week = stat.get('scoringPeriodId')
        source = stat.get('statSourceId')

        # Only track actual results (not projections)
        if source == 0 and week >= 1 and week <= 18:
            points = stat.get('appliedTotal', 0.0)
            weekly_points[week] = points

    return weekly_points

# Usage
weekly = extract_weekly_performance(player)
print(f"Week 1: {weekly.get(1, 'N/A')} pts")
print(f"Week 2: {weekly.get(2, 'N/A')} pts")
print(f"Total weeks played: {len(weekly)}")
print(f"Average: {sum(weekly.values()) / len(weekly) if weekly else 0:.1f} pts")
```

---

## Cross-References

- **Endpoints**: See [espn_api_endpoints.md](espn_api_endpoints.md) for API endpoint details
- **Team Data**: See [espn_team_data.md](espn_team_data.md) for NFL team field reference
- **ID Mappings**: See [espn_api_reference_tables.md](espn_api_reference_tables.md) for all mapping tables
- **Examples**: See [examples/player_projection_response.json](examples/player_projection_response.json) for real response

---

## Changelog

- **2025-10-31**: Initial version - All player fields documented with examples

---

## ⚠️ Disclaimer

ESPN Fantasy Football API is **unofficial** and **undocumented**. Field names and structures may change without notice. Use at your own risk.

**Not affiliated with ESPN.**
