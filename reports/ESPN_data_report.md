# ESPN Fantasy Football API Data Structure Documentation

**Generated:** September 18, 2025
**Version:** 2.0
**Author:** Claude Code Research for Fantasy Football Helper Scripts

---

## Table of Contents

1. [Overview](#overview)
2. [API Endpoints](#api-endpoints)
3. [Fantasy Player Data Structure](#fantasy-player-data-structure)
4. [NFL Scores Data Structure](#nfl-scores-data-structure)
5. [Stats System](#stats-system)
6. [Position and Team Mappings](#position-and-team-mappings)
7. [Usage Examples](#usage-examples)
8. [Data Collection Best Practices](#data-collection-best-practices)

---

## Overview

ESPN provides free, public APIs for fantasy football and NFL data collection. This documentation details the complete data structures available from ESPN's Fantasy Football API and NFL Scores API, based on analysis of the existing codebase and live API testing.

### Key Features
- **No Authentication Required**: ESPN's APIs are publicly accessible
- **Real-time Data**: Live player projections, injury status, and game scores
- **Week-by-Week Projections**: Detailed weekly and season-long fantasy projections
- **Comprehensive Player Data**: ADP, ownership, injury status, team info
- **Complete Game Data**: Scores, stats, venue, weather, betting lines

### API Reliability
- Rate limiting: 0.2-0.5 second delays recommended between requests
- Retry logic: Implement exponential backoff for 429/500 errors
- Caching: ESPN data updates frequently during season but is stable for historical data

---

## API Endpoints

### Fantasy Football API

**Base URL:** `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/{scoring_format}`

#### Scoring Format IDs
- **Standard (Non-PPR):** `1`
- **Half-PPR:** `2`
- **PPR (Points Per Reception):** `3`

#### Primary Endpoints

**1. Season Projections**
```
GET /apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3
Parameters:
  - view: "kona_player_info"
  - scoringPeriodId: 0  # 0 = full season data
Headers:
  - User-Agent: [required]
  - X-Fantasy-Filter: {"players":{"limit":2000,"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}
```

**2. Weekly Projections**
```
GET /apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3
Parameters:
  - view: "kona_player_info"
  - scoringPeriodId: {week}  # 1-18 for regular season, 19-22 for playoffs
```

**3. Single Player Data**
```
GET /apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3
Parameters:
  - view: "kona_player_info"
  - scoringPeriodId: 0 or {week}
Headers:
  - X-Fantasy-Filter: {"players":{"filterIds":{"value":[{player_id}]}}}
```

### NFL Scores API

**Base URL:** `https://site.api.espn.com/apis/site/v2/sports/football/nfl`

#### Primary Endpoints

**1. Current Week Scores**
```
GET /scoreboard
```

**2. Specific Week Scores**
```
GET /scoreboard
Parameters:
  - seasontype: 2  # Regular season
  - week: {week_number}
  - dates: {season_year}
```

**3. Date Range Scores**
```
GET /scoreboard
Parameters:
  - dates: "YYYYMMDD-YYYYMMDD"
  - limit: 1000
```

---

## Fantasy Player Data Structure

### Root Response Format
```json
{
  "players": [
    {
      "draftAuctionValue": 0,
      "id": 4362628,
      "keeperValue": 0,
      "keeperValueFuture": 0,
      "lineupLocked": false,
      "onTeamId": 0,
      "player": { /* Player Object - See Below */ }
    }
  ]
}
```

### Player Object Structure

#### Core Player Information
```json
{
  "id": 4362628,                    // ESPN's unique player ID
  "firstName": "Ja'Marr",           // Player's first name
  "lastName": "Chase",              // Player's last name
  "fullName": "Ja'Marr Chase",      // Complete player name
  "jersey": "1",                    // Jersey number (string)
  "active": true,                   // Whether player is on active roster
  "defaultPositionId": 3,           // Position ID (see mappings below)
  "proTeamId": 4,                   // Team ID (see mappings below)
  "droppable": false,               // Whether player can be dropped in fantasy
  "injured": false,                 // Basic injury flag
  "injuryStatus": "ACTIVE"          // Detailed injury status
}
```

#### Position Eligibility
```json
{
  "eligibleSlots": [3, 4, 5, 23, 7, 20, 21]  // Array of position slot IDs player is eligible for
}
```

#### Draft Rankings
```json
{
  "draftRanksByRankType": {
    "STANDARD": {
      "auctionValue": 57,
      "published": false,
      "rank": 1,
      "rankSourceId": 0,
      "rankType": "STANDARD",
      "slotId": 0
    },
    "PPR": {
      "auctionValue": 57,
      "published": false,
      "rank": 1,
      "rankSourceId": 0,
      "rankType": "PPR",
      "slotId": 0
    }
  }
}
```

#### Ownership Data
```json
{
  "ownership": {
    "activityLevel": null,                    // Player add/drop activity
    "auctionValueAverage": 54.31,             // Average auction price
    "auctionValueAverageChange": -6.41,       // Change in auction value
    "averageDraftPosition": 2.74,             // ADP across all leagues
    "averageDraftPositionPercentChange": -1.07, // ADP movement percentage
    "date": 1758211517549,                    // Data timestamp
    "leagueType": 0,                          // League type identifier
    "percentChange": 0.005,                   // Ownership change percentage
    "percentOwned": 99.95,                    // Percentage of leagues owned in
    "percentStarted": 99.64                   // Percentage of leagues started in
  }
}
```

#### Player Rankings
```json
{
  "rankings": {
    "0": [  // Season rankings (use specific week numbers for weekly rankings)
      {
        "auctionValue": 0,
        "published": true,
        "rank": 1,
        "rankSourceId": 9,      // Ranking source (6=ESPN, 7=ESPN Fantasy, 9=ESPN Research, 11=ESPN Draft Guide)
        "rankType": "PPR",      // Scoring format
        "slotId": 4             // Position slot
      }
    ]
  }
}
```

#### Weekly Outlooks
```json
{
  "outlooks": {
    "outlooksByWeek": {
      "1": "Ja'Marr Chase's start to his career has been exceptional...",
      "2": "Ja'Marr Chase had arguably the most disappointing fantasy showing...",
      "3": "Ja'Marr Chase rebounded from a subpar Week 1 performance..."
    }
  },
  "seasonOutlook": "Season-long analysis text...",
  "lastNewsDate": 1757884281000  // Timestamp of last news update
}
```

### Defense/DST Players

Defense players have negative IDs and different structure:

```json
{
  "id": -16001,                    // Negative ID for defense teams
  "firstName": "Falcons",          // Team name as first name
  "lastName": "D/ST",              // Always "D/ST"
  "fullName": "Falcons D/ST",      // Team name + "D/ST"
  "defaultPositionId": 16,         // Always 16 for defense
  "proTeamId": 1,                  // Corresponding NFL team ID
  "droppable": true,               // Defenses are typically droppable
  "eligibleSlots": [16, 20, 21]    // Defense, bench, and IR slots
}
```

---

## Stats System

### Stats Array Structure
Each player has a `stats` array containing statistical data for different time periods:

```json
{
  "stats": [
    {
      "appliedTotal": 21.93,          // ESPN's calculated fantasy points
      "appliedAverage": 20.67,        // Average fantasy points per game
      "projectedTotal": 289.45,       // Projected fantasy points (future periods)
      "externalId": "202415",         // ESPN's internal period identifier
      "id": "11202415",              // Unique stat entry ID
      "proTeamId": 0,                // Team context (0 = league-wide)
      "scoringPeriodId": 15,         // Week number (0 = season, 1-18 = weeks)
      "seasonId": 2025,              // Season year
      "statSourceId": 0,             // Source: 0=actual, 1=projected
      "statSplitTypeId": 1,          // Split type (1=game, 0=season)
      "stats": {
        "23": 0.204,  // Receptions
        "24": 1.075,  // Receiving yards
        "25": 0.006,  // Receiving TDs
        "26": 0.0004, // Rushing attempts
        "35": 0.0003, // Rushing yards
        "41": 6.0,    // Actual receptions (integers for actual stats)
        "42": 86.0,   // Actual receiving yards
        "43": 1.0,    // Actual receiving TDs
        "47": 17.0,   // Fantasy points scored
        "48": 8.0,    // Additional stat
        "49": 2.0     // Additional stat
      }
    }
  ]
}
```

### Stat ID Mappings (Partial)

**Receiving Stats:**
- `23`: Receptions (or projected receptions)
- `24`: Receiving yards
- `25`: Receiving touchdowns
- `41`: Actual receptions (integer)
- `42`: Actual receiving yards (integer)
- `43`: Actual receiving TDs (integer)

**Rushing Stats:**
- `26`: Rushing attempts
- `35`: Rushing yards
- `27`: Rushing touchdowns

**Passing Stats:**
- Various IDs for completions, yards, TDs, interceptions

**Fantasy Points:**
- `47`: Total fantasy points for the period
- `48`: Additional scoring metric
- `49`: Additional scoring metric

### Data Types by Source
- **Projected data (`statSourceId: 1`)**: Decimal values representing averages/projections
- **Actual data (`statSourceId: 0`)**: Integer values for completed games
- **Season data (`scoringPeriodId: 0`)**: Aggregated totals or averages

---

## NFL Scores Data Structure

### Root Response Format
```json
{
  "events": [
    {
      "id": "401671740",
      "date": "2025-09-14T20:00Z",
      "season": {
        "year": 2025,
        "type": 2,
        "week": 2
      },
      "competitions": [
        { /* Competition Object - See Below */ }
      ]
    }
  ]
}
```

### Competition Object Structure

#### Game Status
```json
{
  "status": {
    "type": {
      "id": "3",
      "name": "STATUS_FINAL",
      "description": "Final",
      "detail": "Final",
      "shortDetail": "Final",
      "completed": true,
      "state": "post"
    }
  }
}
```

#### Team Data
```json
{
  "competitors": [
    {
      "id": "16",                          // ESPN team ID
      "homeAway": "home",                  // "home" or "away"
      "score": 24,                         // Final score
      "team": {
        "id": "16",
        "name": "Vikings",                 // Team name
        "displayName": "Minnesota Vikings", // Full display name
        "abbreviation": "MIN",             // 3-letter abbreviation
        "location": "Minnesota",           // Team location
        "color": "4f2683",                // Primary color (hex)
        "alternateColor": "ffc62f",       // Secondary color
        "logo": "https://...",            // Logo URL
        "record": {
          "displayValue": "1-1"           // Season record
        }
      },
      "statistics": [                      // Game statistics
        {
          "name": "totalYards",
          "displayValue": "312"
        },
        {
          "name": "turnovers",
          "displayValue": "1"
        }
      ],
      "linescores": [                      // Quarter scores
        {"value": 7},   // Q1
        {"value": 10},  // Q2
        {"value": 0},   // Q3
        {"value": 7}    // Q4
      ]
    }
  ]
}
```

#### Venue Information
```json
{
  "venue": {
    "id": "1992",
    "fullName": "U.S. Bank Stadium",
    "address": {
      "city": "Minneapolis",
      "state": "Minnesota"
    },
    "capacity": 66200,
    "indoor": true
  }
}
```

#### Weather and Broadcast
```json
{
  "weather": {
    "temperature": 72,
    "conditionId": "clear",
    "description": "Clear"
  },
  "broadcasts": [
    {
      "market": {
        "name": "ABC"
      }
    }
  ],
  "attendance": 66467
}
```

#### Betting Information
```json
{
  "odds": [
    {
      "provider": {
        "name": "ESPN BET"
      },
      "homeTeamOdds": {
        "moneyLine": -110
      },
      "awayTeamOdds": {
        "moneyLine": -110
      },
      "overUnder": 44.5
    }
  ]
}
```

---

## Position and Team Mappings

### ESPN Position IDs
```javascript
{
  1: 'QB',   // Quarterback
  2: 'RB',   // Running Back
  3: 'WR',   // Wide Receiver
  4: 'TE',   // Tight End
  5: 'K',    // Kicker
  16: 'DST'  // Defense/Special Teams
}
```

### ESPN Team IDs
```javascript
{
  1: 'ATL',  2: 'BUF',  3: 'CHI',  4: 'CIN',  5: 'CLE',  6: 'DAL',
  7: 'DEN',  8: 'DET',  9: 'GB',   10: 'TEN', 11: 'IND', 12: 'KC',
  13: 'LV',  14: 'LAR', 15: 'MIA', 16: 'MIN', 17: 'NE',  18: 'NO',
  19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
  25: 'SF',  26: 'SEA', 27: 'TB',  28: 'WSH', 29: 'CAR', 30: 'JAX',
  33: 'BAL', 34: 'HOU'
}
```

### Eligible Slot IDs (Fantasy Positions)
```javascript
{
  0: 'QB',     // Quarterback slot
  2: 'RB',     // Running back slot
  4: 'WR',     // Wide receiver slot
  6: 'TE',     // Tight end slot
  17: 'K',     // Kicker slot
  16: 'D/ST',  // Defense slot
  20: 'BE',    // Bench slot
  21: 'IR',    // Injured reserve
  23: 'FLEX'   // Flex position (RB/WR/TE)
}
```

### Injury Status Values
```javascript
{
  "ACTIVE": "Healthy and available",
  "QUESTIONABLE": "May play, game-time decision",
  "DOUBTFUL": "Unlikely to play",
  "OUT": "Will not play",
  "IR": "Injured reserve",
  "SUSPENDED": "League suspension",
  "PUP": "Physically unable to perform list"
}
```

---

## Usage Examples

### Example 1: Get Season Projections for Top 50 Players

```python
import asyncio
import httpx

async def get_season_projections():
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3"

    params = {
        "view": "kona_player_info",
        "scoringPeriodId": 0
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Fantasy-Filter': '{"players":{"limit":50,"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        data = response.json()

        for player_data in data['players']:
            player = player_data['player']

            # Extract basic info
            name = player['fullName']
            position_id = player['defaultPositionId']
            team_id = player['proTeamId']

            # Extract fantasy points from stats
            stats = player.get('stats', [])
            fantasy_points = 0
            for stat in stats:
                if stat.get('scoringPeriodId') == 0:  # Season data
                    fantasy_points = stat.get('appliedTotal', 0)
                    break

            print(f"{name}: {fantasy_points} projected points")

asyncio.run(get_season_projections())
```

### Example 2: Get Current Week Projections for Specific Player

```python
async def get_player_week_projection(player_id: str, week: int):
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3"

    params = {
        "view": "kona_player_info",
        "scoringPeriodId": week
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Fantasy-Filter': f'{{"players":{{"filterIds":{{"value":[{player_id}]}}}}}}'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        data = response.json()

        if data['players']:
            player = data['players'][0]['player']
            stats = player.get('stats', [])

            for stat in stats:
                if stat.get('scoringPeriodId') == week:
                    projected_points = stat.get('projectedTotal', 0)
                    print(f"Week {week} projection: {projected_points}")
                    return projected_points

        return 0

# Example: Get Lamar Jackson's Week 3 projection
projection = await get_player_week_projection("4431569", 3)
```

### Example 3: Get Current NFL Scores

```python
async def get_current_nfl_scores():
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

        for event in data['events']:
            game_id = event['id']
            date = event['date']

            competition = event['competitions'][0]
            competitors = competition['competitors']

            # Find home and away teams
            home_team = next(c for c in competitors if c['homeAway'] == 'home')
            away_team = next(c for c in competitors if c['homeAway'] == 'away')

            home_name = home_team['team']['displayName']
            away_name = away_team['team']['displayName']
            home_score = home_team['score']
            away_score = away_team['score']

            status = competition['status']['type']['description']

            print(f"{away_name} @ {home_name}: {away_score}-{home_score} ({status})")

await get_current_nfl_scores()
```

---

## Data Collection Best Practices

### Rate Limiting
- **Minimum delay**: 200ms between requests
- **Recommended delay**: 500ms for sustained scraping
- **Bulk operations**: 1-2 second delays between batches

### Error Handling
```python
from tenacity import retry, stop_after_attempt, wait_random_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(multiplier=1, max=10)
)
async def make_request(url, params, headers):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)

        if response.status_code == 429:
            # Rate limited - wait longer
            await asyncio.sleep(30)
            raise httpx.HTTPStatusError("Rate limited")

        response.raise_for_status()
        return response.json()
```

### Caching Strategy
- **Season projections**: Cache for 1-2 hours during season
- **Weekly projections**: Cache for 30-60 minutes
- **Live scores**: Cache for 5-10 minutes during games
- **Historical data**: Cache indefinitely

### Data Validation
```python
def validate_player_data(player_data):
    required_fields = ['id', 'fullName', 'defaultPositionId', 'proTeamId']
    player = player_data.get('player', {})

    for field in required_fields:
        if field not in player:
            raise ValueError(f"Missing required field: {field}")

    # Validate position ID
    if player['defaultPositionId'] not in [1, 2, 3, 4, 5, 16]:
        raise ValueError(f"Invalid position ID: {player['defaultPositionId']}")

    return True
```

### Performance Optimization
- **Concurrent requests**: Use asyncio for parallel API calls
- **Selective updates**: Only fetch data for players that need updating
- **Batch filtering**: Use X-Fantasy-Filter to limit response size
- **Compression**: Request gzip encoding for large responses

### API Limits and Considerations
- **No authentication required**: ESPN APIs are publicly accessible
- **Rate limiting**: ~100-200 requests per minute recommended maximum
- **Seasonal availability**: Fantasy data available during NFL season (Aug-Jan)
- **Data freshness**: Player projections update multiple times per week
- **Injury updates**: Real-time during season, check lastNewsDate field

---

## Conclusion

ESPN's Fantasy Football API provides comprehensive data for building fantasy football applications. The API structure is consistent and well-documented through practical usage. Key recommendations:

1. **Always implement rate limiting** to avoid 429 errors
2. **Use the stats array efficiently** - different scoringPeriodId values provide different time horizons
3. **Handle missing data gracefully** - not all players have complete stat histories
4. **Cache aggressively** - ESPN data doesn't change frequently except during games
5. **Monitor the lastNewsDate field** for injury and roster updates

For questions or issues with this documentation, refer to the existing codebase implementations in the `player-data-fetcher/`, `starter_helper/`, and `nfl-scores-fetcher/` directories.

---

*This documentation is based on analysis of ESPN's public APIs as of September 2025. API structures may change over time.*