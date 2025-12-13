# ESPN Fantasy Football API - Player Data Reference

**Last Updated**: 2025-12-13
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

- **Always Present**: id, firstName, lastName, defaultPositionId, active
- **Usually Present**: proTeamId, stats array, droppable, eligibleSlots
- **Often Present**: ownership, draftRanksByRankType, jersey, injured, injuryStatus
- **Sometimes Present**: outlooks, rankings, lastNewsDate
- **Rarely Present**: Custom league-specific fields

### Player Wrapper Object

The player data is actually wrapped in an outer object with additional fields:

```json
{
  "draftAuctionValue": 0,
  "id": 4429795,
  "keeperValue": 0,
  "keeperValueFuture": 0,
  "lineupLocked": false,
  "onTeamId": 0,
  "player": { /* Actual player data */ },
  "ratings": { "0": { "positionalRanking": 4, "totalRanking": 13, "totalRating": 184.0 } },
  "rosterLocked": false,
  "status": "WAIVERS",
  "tradeLocked": false,
  "waiverProcessDate": 1762934400000
}
```

| Field | Type | Description |
|-------|------|-------------|
| `draftAuctionValue` | integer | Auction draft value |
| `id` | integer | Player ID (same as player.id) |
| `keeperValue` | integer | Keeper league value |
| `keeperValueFuture` | integer | Future keeper value |
| `lineupLocked` | boolean | Whether lineup is locked |
| `onTeamId` | integer | Fantasy team ID (0 = free agent) |
| `ratings` | object | Rankings by week (keys are week numbers, "0" for season) |
| `rosterLocked` | boolean | Whether roster is locked |
| `status` | string | Player status (e.g., "WAIVERS", "FREEAGENT") |
| `tradeLocked` | boolean | Whether player is trade locked |
| `waiverProcessDate` | integer | Timestamp for waiver processing (milliseconds) |

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
    "active": true,
    "jersey": "15",

    // Team & Position
    "defaultPositionId": 1,
    "proTeamId": 12,
    "eligibleSlots": [0, 16],
    "droppable": true,

    // Injury
    "injured": false,
    "injuryStatus": "ACTIVE",

    // Ownership & Draft
    "ownership": { ... },
    "draftRanksByRankType": { ... },
    "rankings": { ... },

    // Statistics
    "stats": [ ... ],

    // News & Outlooks
    "lastNewsDate": 1764531338000,
    "outlooks": { ... },
    "seasonOutlook": "Player outlook text for the entire season..."
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

### player.active

**Type**: `boolean`
**Required**: Yes
**Description**: Whether the player is currently active on an NFL roster

```json
"active": true
```

**Notes**:
- `true` for active roster players
- `false` for retired, suspended, or practice squad players

### player.jersey

**Type**: `string`
**Required**: Usually
**Description**: Player's jersey number

```json
"jersey": "15"
```

**Notes**:
- Returned as string, not integer
- May be empty for recently signed players

### player.droppable

**Type**: `boolean`
**Required**: Usually
**Description**: Whether player can be dropped in fantasy leagues

```json
"droppable": true
```

**Notes**:
- `false` for players on IR or with recent transactions
- League settings may override this

### player.injured

**Type**: `boolean`
**Required**: Usually
**Description**: Quick flag indicating if player has any injury designation

```json
"injured": false
```

**Notes**:
- Different from `injuryStatus` which provides specific status
- `true` if injuryStatus is anything other than "ACTIVE"

### player.lastNewsDate

**Type**: `integer` (timestamp)
**Required**: Sometimes
**Description**: Unix timestamp (milliseconds) of the last news update for this player

```json
"lastNewsDate": 1764531338000
```

**Usage**:
```python
from datetime import datetime
news_date = datetime.fromtimestamp(player['lastNewsDate'] / 1000)
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
  "activityLevel": null,
  "auctionValueAverage": 51.53,
  "auctionValueAverageChange": -0.1,
  "averageDraftPosition": 6.85,
  "averageDraftPositionPercentChange": -0.07,
  "date": 1761931821839,
  "leagueType": 0,
  "percentChange": 0.0,
  "percentOwned": 99.94,
  "percentStarted": 90.52
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

#### ownership.auctionValueAverageChange

**Type**: `float`
**Description**: Change in auction value from previous update

```json
"auctionValueAverageChange": -0.1
```

#### ownership.averageDraftPositionPercentChange

**Type**: `float`
**Description**: Percent change in ADP from previous update

```json
"averageDraftPositionPercentChange": -0.07
```

#### ownership.date

**Type**: `integer` (timestamp)
**Description**: Timestamp when ownership data was last updated

```json
"date": 1761931821839
```

#### ownership.leagueType

**Type**: `integer`
**Description**: League type identifier (0 for standard)

#### ownership.percentChange

**Type**: `float`
**Description**: Change in percent owned from previous update

#### ownership.activityLevel

**Type**: `null` or `integer`
**Description**: Player activity level (usually null)

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

### player.rankings

**Type**: `object`
**Required**: Sometimes
**Description**: Weekly expert rankings by different sources

```json
"rankings": {
  "0": [
    {
      "auctionValue": 0,
      "published": true,
      "rank": 3,
      "rankSourceId": 7,
      "rankType": "PPR",
      "slotId": 2
    }
  ]
}
```

**Notes**:
- Keys are week numbers (or "0" for season-long)
- Each week can have multiple ranking entries from different sources
- `rankSourceId` identifies the ranking source (ESPN, expert consensus, etc.)
- `slotId` identifies the position slot for the ranking

### player.outlooks

**Type**: `object`
**Required**: Sometimes
**Description**: Weekly text outlooks/analysis for the player

```json
"outlooks": {
  "outlooksByWeek": {
    "1": "Player outlook text for Week 1...",
    "2": "Player outlook text for Week 2...",
    "3": "Player outlook text for Week 3..."
  }
}
```

**Notes**:
- Contains ESPN's written analysis for each upcoming week
- Keys are week numbers as strings
- Useful for understanding ESPN's narrative on player value
- May contain special characters/encoding issues

**Usage**:
```python
outlooks = player.get('outlooks', {}).get('outlooksByWeek', {})
week_15_outlook = outlooks.get('15', 'No outlook available')
print(f"Week 15 Outlook: {week_15_outlook}")
```

### player.seasonOutlook

**Type**: `string`
**Required**: Sometimes
**Description**: ESPN's written analysis for the player's entire season outlook

```json
"seasonOutlook": "The reigning No. 1 fantasy RB, Gibbs scored a position-high 20 TDs while dominating as both a rusher (fifth in yards) and receiver..."
```

**Notes**:
- Contains ESPN's preseason or season-long narrative analysis
- Longer and more detailed than weekly outlooks
- Useful for understanding ESPN's overall valuation of the player
- May not be present for all players

**Usage**:
```python
season_outlook = player.get('seasonOutlook', 'No season outlook available')
print(f"Season Outlook: {season_outlook[:200]}...")  # First 200 chars
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
    "externalId": "...",
    "id": "...",
    "proTeamId": 12,
    "statSplitTypeId": 0,
    "stats": { ... }
  },
  {
    "seasonId": 2025,
    "scoringPeriodId": 1,
    "statSourceId": 1,
    "appliedTotal": 25.2,
    "externalId": "...",
    "id": "...",
    "proTeamId": 12,
    "statSplitTypeId": 0,
    "stats": { ... }
  }
]
```

> **⚠️ IMPORTANT**: As of 2025, ESPN uses `appliedTotal` for BOTH actual results (statSourceId=0) AND projections (statSourceId=1). The `projectedTotal` field is no longer used.

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
| ID | Type | Description |
|----|------|-------------|
| 0  | Actual Results | Real game statistics (after game completion) |
| 1  | Projections    | Estimated/predicted stats (available for future weeks) |

> **Note**: Both stat source types now use `appliedTotal` for the fantasy points value.

**See**: [espn_api_reference_tables.md](espn_api_reference_tables.md#stat-source-id-mappings)

### stats[].appliedTotal

**Type**: `float`
**Description**: Fantasy points for this stat entry (actual or projected depending on statSourceId)

```json
"appliedTotal": 28.5
```

**Notes**:
- Used for BOTH actual results (statSourceId=0) AND projections (statSourceId=1)
- For statSourceId=0: Reflects real game results
- For statSourceId=1: Reflects ESPN's projected points

### stats[].projectedTotal (REMOVED)

**Type**: N/A - field no longer exists
**Description**: Previously used for projected fantasy points

**Notes**:
- **REMOVED**: As of 2025, this field no longer exists in API responses
- ESPN now uses `appliedTotal` for both actual and projected values
- The field is completely absent from the response (not null, just missing)
- Legacy code should check `appliedTotal` instead

### stats[].externalId

**Type**: `string`
**Description**: External identifier for this stat entry

### stats[].proTeamId

**Type**: `integer`
**Description**: Team ID at the time these stats were recorded

### stats[].statSplitTypeId

**Type**: `integer`
**Description**: Stat split type identifier

**Values**:
| ID | Split Type | Description |
|----|------------|-------------|
| 0  | Season Total | Aggregated stats for entire season |
| 1  | Weekly Split | Individual week statistics |
| 2  | Last N Games | Rolling average over recent games |

**See**: [espn_api_reference_tables.md](espn_api_reference_tables.md#stat-split-type-id-mappings)

### stats[].stats

**Type**: `object`
**Description**: Detailed stat breakdowns with ESPN stat IDs as keys

```json
"stats": {
  "3": 285.0,   // Passing yards (stat ID 3)
  "4": 2.0,     // Passing TDs (stat ID 4)
  "20": 15.0    // Rushing yards (stat ID 20)
}
```

**Notes**:
- Keys are ESPN internal stat ID codes (as strings)
- Values are the stat amounts
- Useful for custom scoring calculations
- Full stat ID mapping is not publicly documented

### Priority Logic

When both actual and projected exist for same week, prefer actual:

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

        source = stat.get('statSourceId')
        points = stat.get('appliedTotal')  # Both sources use appliedTotal now

        if source == 0:
            actual_points = points
        elif source == 1:
            projected_points = points

    # Return actual if available and preferred, otherwise projected
    if prefer_actual and actual_points is not None:
        return actual_points
    return projected_points if projected_points is not None else actual_points
```

### stats[].appliedAverage

**Type**: `float`
**Description**: Average fantasy points per game (only present in certain entries, like season totals)

```json
"appliedAverage": 18.5
```

**Notes**:
- Only appears in some stat entries (typically scoringPeriodId=0 for season totals)
- Not present in weekly stat entries

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

points = stat.get('appliedTotal')  # Both actual and projected use appliedTotal
if points is not None and math.isnan(points):
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
    "eligibleSlots": [0, 7, 20, 21],
    "injuryStatus": "ACTIVE",
    "ownership": {
      "percentOwned": 99.8,
      "percentStarted": 95.2,
      "averageDraftPosition": 2.5,
      "auctionValueAverage": 65.0
    },
    "draftRanksByRankType": {
      "PPR": {"rank": 5, "rankSourceId": 1, "auctionValue": 0, "published": true},
      "STANDARD": {"rank": 3, "rankSourceId": 1, "auctionValue": 0, "published": true}
    },
    "stats": [
      {
        "seasonId": 2025,
        "scoringPeriodId": 0,
        "statSourceId": 1,
        "appliedTotal": 285.6,
        "appliedAverage": 15.87
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
        "appliedTotal": 25.2
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

    # Season projection (use appliedTotal - projectedTotal is deprecated)
    season_points = None
    for stat in player.get('stats', []):
        if stat.get('scoringPeriodId') == 0 and stat.get('statSourceId') == 1:
            season_points = stat.get('appliedTotal')  # Both actual and projected use appliedTotal
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

- **2025-12-13**: Verified and expanded documentation
  - Verified all player fields against live API responses
  - Added statSplitTypeId values table
  - Confirmed appliedTotal/projectedTotal deprecation is accurate
  - Updated wrapper object fields with verified values
- **2025-10-31**: Initial version - All player fields documented with examples

---

## ⚠️ Disclaimer

ESPN Fantasy Football API is **unofficial** and **undocumented**. Field names and structures may change without notice. Use at your own risk.

**Not affiliated with ESPN.**
