# ESPN Fantasy Football API - Endpoints Reference

**Last Updated**: 2025-12-23
**API Status**: Unofficial
**Target Audience**: Python Developers (Intermediate)

---

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Authentication & Headers](#authentication--headers)
4. [Endpoints](#endpoints)
   - [Player Projections](#player-projections-endpoint)
   - [Player Weekly Data](#player-weekly-data-endpoint)
   - [Team Stats List](#team-stats-list-endpoint)
   - [Individual Team Statistics](#individual-team-statistics-endpoint)
   - [Scoreboard/Schedule](#scoreboardschedule-endpoint)
5. [Rate Limiting](#rate-limiting)
6. [Error Handling](#error-handling)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

The ESPN Fantasy Football API is an **unofficial, undocumented API** that powers ESPN's fantasy football platform. While freely accessible without authentication, it comes with important caveats:

### ⚠️ Important Warnings

- **No official support**: ESPN does not officially document or support this API
- **May change without notice**: Endpoints, parameters, or response structures can change
- **No SLA or guarantees**: No uptime or reliability guarantees
- **Rate limiting exists**: Excessive requests may result in temporary blocks
- **Use responsibly**: Respect ESPN's infrastructure with proper rate limiting

### What This API Provides

- **Player projections**: Season and weekly fantasy point projections
- **Player statistics**: Actual game results and historical data
- **Team information**: NFL team IDs, names, and statistics
- **Schedule data**: Weekly matchups and game information
- **Draft rankings**: ESPN's draft rankings by scoring format

### Who Should Use This

This API is suitable for:
- Personal fantasy football tools and analysis
- Educational projects and learning
- Small-scale data collection for research
- Prototyping fantasy sports applications

**Not suitable for**:
- Commercial products without ESPN permission
- High-volume/production applications
- Real-time live scoring (use official NFL API)

---

## Quick Start

Minimal example to fetch player projections:

```python
import httpx

# Configuration
ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
SEASON = 2025
FORMAT_ID = 3  # 1=Standard, 3=PPR (Note: Format 2 returns 404)

# Endpoint URL
url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leaguedefaults/{FORMAT_ID}"

# Headers (recommended for stability)
headers = {"User-Agent": ESPN_USER_AGENT}

# Use sortPercOwned filter to get more players (default returns only 50)
headers["X-Fantasy-Filter"] = '{"players":{"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'

# Query parameters
params = {
    "view": "kona_player_info",
    "scoringPeriodId": 0  # 0 = season totals
}

# Make request
response = httpx.get(url, headers=headers, params=params, timeout=30.0)
response.raise_for_status()

# Parse response
data = response.json()
players = data.get('players', [])

print(f"Fetched {len(players)} players")
for player_obj in players[:5]:
    player = player_obj['player']
    name = f"{player['firstName']} {player['lastName']}"
    print(f"  - {name}")
```

**Output:**
```
Fetched 1081 players
  - Jahmyr Gibbs
  - Ja'Marr Chase
  - Amon-Ra St. Brown
  - ...
```

> **⚠️ IMPORTANT**: Without the `sortPercOwned` filter, the API returns only **50 players** by default. Always use a filter to get the full player list.

---

## Authentication & Headers

### No Authentication Required

ESPN Fantasy API **does not require authentication**:
- ✅ No API keys needed
- ✅ No OAuth tokens required
- ✅ No account registration necessary
- ✅ Publicly accessible endpoints

### Recommended Headers

**User-Agent** (Recommended):
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
```

> **Note (Verified 2025-12)**: User-Agent is no longer strictly required. API requests work without it, but including a browser-like User-Agent is recommended for stability and to avoid potential future restrictions.

### Optional Headers

**X-Fantasy-Filter** (Optional but useful):

```python
headers = {
    "User-Agent": "Mozilla/5.0...",
    "X-Fantasy-Filter": '{"players":{"limit":50,"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'
}
```

Used for filtering and sorting players. See [Player Projections Endpoint](#player-projections-endpoint) for details.

---

## Endpoints

### Player Projections Endpoint

Fetches fantasy football projections for all players.

#### Endpoint Details

- **URL**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/{format_id}`
- **Method**: GET
- **Response Format**: JSON

#### Path Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `season` | integer | NFL season year | `2025` |
| `format_id` | integer | Scoring format (1=Standard, 3=PPR). Note: Format 2 returns 404 | `3` |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `view` | string | Yes | View type (use `"kona_player_info"`) |
| `scoringPeriodId` | integer | Yes | `0` for season, `1-18` for weekly |

#### Request Example

```python
import httpx

url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Fantasy-Filter": '{"players":{"limit":100,"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'
}

params = {
    "view": "kona_player_info",
    "scoringPeriodId": 0
}

async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=headers, params=params, timeout=30.0)
    data = response.json()

players_count = len(data.get('players', []))
print(f"Fetched {players_count} players")
```

#### Response Structure

```json
{
  "players": [
    {
      "draftAuctionValue": 0,
      "id": 3139477,
      "keeperValue": 0,
      "onTeamId": 0,
      "status": "FREEAGENT",
      "player": {
        "id": 3139477,
        "firstName": "Patrick",
        "lastName": "Mahomes",
        "fullName": "Patrick Mahomes",
        "defaultPositionId": 1,
        "proTeamId": 12,
        "injuryStatus": "ACTIVE",
        "active": true,
        "ownership": {
          "averageDraftPosition": 2.5,
          "percentOwned": 99.8,
          "percentStarted": 85.2
        },
        "draftRanksByRankType": {
          "PPR": {"rank": 5, "rankSourceId": 1},
          "STANDARD": {"rank": 3, "rankSourceId": 1}
        },
        "stats": [
          {
            "seasonId": 2025,
            "scoringPeriodId": 0,
            "statSourceId": 1,
            "appliedTotal": 285.6
          }
        ]
      }
    }
  ]
}
```

> **⚠️ IMPORTANT**: ESPN now uses `appliedTotal` for BOTH actual results (statSourceId=0) AND projections (statSourceId=1). The `projectedTotal` field is deprecated and returns null.

#### X-Fantasy-Filter JSON Syntax

The `X-Fantasy-Filter` header accepts JSON to filter/sort players:

**Limit players returned:**
```json
{"players":{"limit":50}}
```

**Sort by ownership:**
```json
{"players":{"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}
```

**Filter by specific IDs:**
```json
{"players":{"filterIds":{"value":[3139477,4040715]}}}
```

**Combined:**
```json
{
  "players": {
    "limit": 100,
    "sortPercOwned": {
      "sortPriority": 4,
      "sortAsc": false
    }
  }
}
```

#### Use Cases

- Get top players by ownership for draft prep
- Fetch season-long projections for all positions
- Compare projections across scoring formats
- Build player database for analysis

#### See Also

- [espn_player_data.md](espn_player_data.md) - Complete player field reference
- [espn_api_reference_tables.md](espn_api_reference_tables.md#position-id-mappings) - Position/Team ID mappings
- [examples/player_projection_response.json](examples/player_projection_response.json) - Real response example

---

### Player Weekly Data Endpoint

Fetches week-by-week statistics and projections for a specific player.

#### Endpoint Details

**Same URL as Player Projections**, but with different parameters:

- **URL**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/{format_id}`
- **Method**: GET
- **Response Format**: JSON

#### Key Difference

Use `scoringPeriodId=0` with a player filter to get **all weeks at once** (optimization).

#### Request Example

```python
import httpx

# Patrick Mahomes (ID: 3139477)
player_id = 3139477

url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leaguedefaults/3"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Fantasy-Filter": f'{{"players":{{"filterIds":{{"value":[{player_id}]}}}}}}'
}

params = {
    "view": "kona_player_info",
    "scoringPeriodId": 0  # Get ALL weeks in one call
}

response = httpx.get(url, headers=headers, params=params, timeout=30.0)
data = response.json()

player = data['players'][0]['player']
stats = player['stats']
print(f"Fetched {len(stats)} stat entries for {player['firstName']} {player['lastName']}")
```

#### Response Structure

Each player has multiple `stats` entries - one per week, often with both actual and projected data:

```json
{
  "players": [{
    "player": {
      "id": 3139477,
      "firstName": "Patrick",
      "lastName": "Mahomes",
      "stats": [
        {
          "seasonId": 2025,
          "scoringPeriodId": 1,
          "statSourceId": 0,       // Actual results
          "appliedTotal": 28.5     // Both actual and projected use appliedTotal
        },
        {
          "seasonId": 2025,
          "scoringPeriodId": 1,
          "statSourceId": 1,       // Projection
          "appliedTotal": 25.2     // Note: projectedTotal is deprecated
        },
        {
          "seasonId": 2025,
          "scoringPeriodId": 2,
          "statSourceId": 1,
          "appliedTotal": 26.8
        }
        // ... weeks 3-18
      ]
    }
  }]
}
```

#### Parsing Weekly Stats

```python
def get_week_points(stats_array, week_num):
    """Extract points for a specific week, prefer actuals"""
    actual_points = None
    projected_points = None

    for stat in stats_array:
        if stat.get('scoringPeriodId') != week_num:
            continue

        # Both actual (0) and projected (1) now use appliedTotal
        points = stat.get('appliedTotal')

        if stat.get('statSourceId') == 0:
            actual_points = points
        elif stat.get('statSourceId') == 1:
            projected_points = points

    # Return actual if available, otherwise projected
    return actual_points if actual_points is not None else projected_points

# Usage
week_1 = get_week_points(stats, 1)
week_2 = get_week_points(stats, 2)
```

#### Performance Note

**⚡ Optimization**: Using `scoringPeriodId=0` fetches all weeks in **one API call** instead of 18 separate calls. This is dramatically faster and reduces load on ESPN's servers.

#### Use Cases

- Week-by-week performance tracking
- Identifying player trends (hot/cold streaks)
- Comparing projections vs actual results
- Building player consistency metrics

#### See Also

- [espn_api_reference_tables.md](espn_api_reference_tables.md#stat-source-id-mappings) - Understanding statSourceId
- [espn_api_reference_tables.md](espn_api_reference_tables.md#scoring-period-id-mappings) - Understanding scoringPeriodId
- [examples/player_weekly_data_response.json](examples/player_weekly_data_response.json) - Real response example

---

### Team Stats List Endpoint

Fetches basic information for all 32 NFL teams.

#### Endpoint Details

- **URL**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams`
- **Method**: GET
- **Response Format**: JSON
- **Path Parameters**: None
- **Query Parameters**: None (optionally can filter, but not needed)

#### Request Example

```python
import httpx

url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

response = httpx.get(url, headers=headers, timeout=30.0)
data = response.json()

teams = data.get('teams', [])
print(f"Fetched {len(teams)} teams")

for team_obj in teams[:5]:
    team = team_obj['team']
    print(f"  {team['abbreviation']}: {team['displayName']}")
```

#### Response Structure

```json
{
  "sports": [
    {
      "leagues": [
        {
          "teams": [
            {
              "team": {
                "id": 12,
                "abbreviation": "KC",
                "displayName": "Kansas City Chiefs",
                "shortDisplayName": "Chiefs",
                "location": "Kansas City",
                "name": "Chiefs",
                "nickname": "Chiefs",
                "color": "e31837",
                "alternateColor": "ffb81c",
                "isActive": true,
                "logos": [
                  {"href": "https://...", "width": 500, "height": 500}
                ],
                "links": [...]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

> **Note**: Teams are nested under `sports[0].leagues[0].teams[]`, not at the root level.

#### Parsing Example

```python
import httpx

url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
headers = {"User-Agent": "Mozilla/5.0..."}

response = httpx.get(url, headers=headers)
data = response.json()

# Navigate the nested structure
teams = data['sports'][0]['leagues'][0]['teams']
print(f"Fetched {len(teams)} teams")

for team_obj in teams:
    team = team_obj['team']
    print(f"  {team['abbreviation']}: {team['displayName']}")
```

#### Use Cases

- Building team ID → abbreviation mappings
- Getting team names and logos
- Enumerating all NFL teams for UI dropdowns
- Validating team IDs before other API calls

#### See Also

- [espn_api_reference_tables.md](espn_api_reference_tables.md#team-id-mappings) - Complete team ID mappings
- [examples/team_stats_list_response.json](examples/team_stats_list_response.json) - Real response example

---

### Individual Team Statistics Endpoint

Fetches detailed statistics for a specific NFL team.

#### Endpoint Details

- **URL**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics`
- **Method**: GET
- **Response Format**: JSON

#### Path Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `team_id` | integer | ESPN team ID (1-34, see mapping) | `12` (KC) |

#### Request Example

```python
import httpx

# Kansas City Chiefs (team_id=12)
team_id = 12
url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

response = httpx.get(url, headers=headers, timeout=30.0)
data = response.json()

# Extract key stats
stats = data['results']['stats']
for category in stats['categories']:
    for stat in category['stats']:
        if stat['name'] == 'totalPointsPerGame':
            print(f"Points Per Game: {stat['displayValue']}")
```

#### Response Structure

```json
{
  "status": "success",
  "team": {
    "id": 12,
    "abbreviation": "KC",
    "displayName": "Kansas City Chiefs",
    "color": "e31837",
    "logo": "https://...",
    "recordSummary": "..."
  },
  "season": {
    "year": 2025,
    "type": 2,
    "name": "Regular Season",
    "displayName": "2025"
  },
  "results": {
    "stats": {
      "id": "...",
      "name": "...",
      "abbreviation": "...",
      "categories": [
        {
          "name": "passing",
          "displayName": "Passing",
          "shortDisplayName": "PASS",
          "abbreviation": "PASS",
          "stats": [
            {
              "name": "completions",
              "displayName": "Completions",
              "shortDisplayName": "COMP",
              "description": "Total Completions",
              "abbreviation": "C",
              "value": 285.0,
              "displayValue": "285",
              "perGameValue": 20.4,
              "perGameDisplayValue": "20.4"
            }
          ]
        }
      ]
    },
    "opponent": [...]  // Opponent stats categories
  }
}
```

> **Note**: The response includes 11 stat categories: passing, rushing, receiving, miscellaneous, defensive, defensiveInterceptions, general, returning, kicking, punting, scoring.

#### Key Statistics

| Stat Name | Description | Use Case |
|-----------|-------------|----------|
| `totalPointsPerGame` | Offensive scoring rate | Ranking offensive quality |
| `totalYards` | Total offensive yardage | Measuring offensive output |
| `totalTakeaways` | Defensive takeaways | Ranking defensive quality |

#### Extracting Stats

```python
def extract_stat(stats_data, stat_name):
    """Extract specific stat value from team statistics"""
    for category in stats_data['categories']:
        for stat in category['stats']:
            if stat['name'] == stat_name:
                return float(stat['value'])
    return None

# Usage
stats = data['results']['stats']
ppg = extract_stat(stats, 'totalPointsPerGame')
yards = extract_stat(stats, 'totalYards')
takeaways = extract_stat(stats, 'totalTakeaways')

print(f"Offensive Rating: {ppg} PPG, {yards} yards")
print(f"Defensive Rating: {takeaways} takeaways")
```

#### Use Cases

- Calculating team offensive/defensive rankings
- Evaluating matchup difficulty for players
- Building strength of schedule metrics
- Analyzing team performance trends

#### See Also

- [espn_team_data.md](espn_team_data.md) - Complete team field reference
- [espn_api_reference_tables.md](espn_api_reference_tables.md#team-id-mappings) - Team ID list
- [examples/team_stats_response.json](examples/team_stats_response.json) - Real response example

---

### Scoreboard/Schedule Endpoint

Fetches game schedule and results for a specific week.

#### Endpoint Details

- **URL**: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
- **Method**: GET
- **Response Format**: JSON

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `seasontype` | integer | Yes | `2` for regular season, `3` for playoffs |
| `week` | integer | Yes | Week number (1-18) |
| `dates` | integer | Yes | Season year (e.g., `2025`) |

#### Request Example

```python
import httpx

url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

params = {
    "seasontype": 2,  # Regular season
    "week": 1,
    "dates": 2025
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

response = httpx.get(url, headers=headers, params=params, timeout=30.0)
data = response.json()

events = data.get('events', [])
print(f"Week 1 has {len(events)} games")

for event in events:
    competitors = event['competitions'][0]['competitors']
    team1 = competitors[0]['team']['abbreviation']
    team2 = competitors[1]['team']['abbreviation']
    print(f"  {team1} vs {team2}")
```

#### Response Structure

```json
{
  "leagues": [...],
  "season": {"type": 2, "year": 2025},
  "week": {"number": 15},
  "events": [
    {
      "id": "401547417",
      "uid": "...",
      "date": "2025-09-07T00:00Z",
      "name": "Denver Broncos at Kansas City Chiefs",
      "shortName": "DEN @ KC",
      "season": {...},
      "week": {...},
      "competitions": [
        {
          "id": "...",
          "date": "2025-09-07T00:00Z",
          "attendance": 76416,
          "type": {...},
          "neutralSite": false,
          "venue": {
            "id": "3622",
            "fullName": "GEHA Field at Arrowhead Stadium",
            "address": {"city": "Kansas City", "state": "MO"}
          },
          "competitors": [
            {
              "id": "12",
              "uid": "...",
              "homeAway": "home",
              "winner": true,
              "team": {
                "id": "12",
                "abbreviation": "KC",
                "displayName": "Kansas City Chiefs",
                "logo": "https://..."
              },
              "score": "27",
              "linescores": [...],
              "statistics": [...],
              "records": [...]
            },
            {
              "id": "7",
              "uid": "...",
              "homeAway": "away",
              "winner": false,
              "team": {
                "id": "7",
                "abbreviation": "DEN",
                "displayName": "Denver Broncos"
              },
              "score": "24"
            }
          ],
          "notes": [...],
          "status": {
            "clock": 0.0,
            "displayClock": "0:00",
            "period": 4,
            "type": {
              "id": "3",
              "name": "STATUS_FINAL",
              "completed": true
            }
          },
          "broadcasts": [...],
          "leaders": [...],
          "headlines": [...]
        }
      ],
      "links": [...],
      "status": {...}
    }
  ],
  "provider": {...}
}
```

#### Building Matchup Map

```python
def build_matchup_map(schedule_data):
    """Build dict mapping team → opponent for the week"""
    matchups = {}

    for event in schedule_data.get('events', []):
        competitors = event['competitions'][0]['competitors']

        if len(competitors) == 2:
            team1 = competitors[0]['team']['abbreviation']
            team2 = competitors[1]['team']['abbreviation']

            # Each team's opponent is the other team
            matchups[team1] = team2
            matchups[team2] = team1

    return matchups

# Usage
matchups = build_matchup_map(data)
print(f"KC plays: {matchups['KC']}")
print(f"DEN plays: {matchups['DEN']}")
```

#### Use Cases

- Determining weekly matchups for lineup decisions
- Finding home/away designation
- Building strength of schedule analysis
- Tracking game timing and status

#### See Also

- [examples/schedule_response.json](examples/schedule_response.json) - Real response example

---

## Rate Limiting

### ESPN's Rate Limits

ESPN does not publicly document rate limits, but observed behavior suggests:

- **Requests per second**: ~5 requests/second appears safe
- **Burst tolerance**: Small bursts (10-20 requests) seem acceptable
- **429 responses**: Excessive requests trigger HTTP 429 (Too Many Requests)

### Recommended Strategy

**Add delays between requests**:

```python
import asyncio

async def fetch_with_rate_limit(url, headers, delay=0.2):
    """Fetch with rate limiting delay"""
    await asyncio.sleep(delay)  # 0.2s = 5 req/sec
    async with httpx.AsyncClient() as client:
        return await client.get(url, headers=headers)

# Usage
for player_id in player_ids:
    response = await fetch_with_rate_limit(url, headers, delay=0.2)
```

**Recommended delays**:
- **Casual use**: 0.2 seconds (5 req/sec)
- **Bulk fetching**: 0.5 seconds (2 req/sec)
- **Production**: 1.0 second (1 req/sec) + exponential backoff

### Retry Logic

Implement exponential backoff for failed requests:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, max=10)
)
async def fetch_with_retry(url, headers):
    """Fetch with automatic retry and exponential backoff"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=30.0)

        if response.status_code == 429:
            raise Exception("Rate limited")

        response.raise_for_status()
        return response.json()
```

### Best Practices

1. ✅ **Add delays**: Always add 0.2s minimum between requests
2. ✅ **Implement retries**: Use exponential backoff for failures
3. ✅ **Cache responses**: Store results to avoid repeated calls
4. ✅ **Batch requests**: Use `scoringPeriodId=0` for all-weeks data
5. ✅ **Respect 429s**: If rate limited, increase delays significantly

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Cause | Solution |
|------|---------|-------|----------|
| 200 | Success | Request succeeded | Parse response |
| 400 | Bad Request | Invalid parameters | Check query params |
| 429 | Too Many Requests | Rate limit exceeded | Add delays, retry later |
| 500 | Server Error | ESPN server issue | Retry with backoff |
| 503 | Service Unavailable | ESPN maintenance | Wait and retry |

### Common Error Scenarios

**Empty Response (Default Limit):**
```python
# ❌ Wrong - Returns only 50 players
response = httpx.get(url, headers=headers)
data = response.json()
print(len(data['players']))  # 50

# ✅ Correct - Use sortPercOwned filter for full list
headers["X-Fantasy-Filter"] = '{"players":{"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'
response = httpx.get(url, headers=headers)
data = response.json()
print(len(data['players']))  # 1081+
```

**Invalid Scoring Format:**
```python
# ❌ Wrong - Invalid format_id
url = f".../leaguedefaults/999"  # No such format

# ✅ Correct - Use 1, 2, or 3
url = f".../leaguedefaults/3"  # PPR
```

**Invalid Team ID:**
```python
# ❌ Wrong - No team with ID 999
url = f"https://.../teams/999/statistics"

# ✅ Correct - Use valid team IDs (1-34)
url = f"https://.../teams/12/statistics"  # KC
```

### Error Handling Pattern

```python
import httpx

async def safe_fetch(url, headers):
    """Fetch with comprehensive error handling"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=30.0)

            # Check for rate limiting
            if response.status_code == 429:
                print("Rate limited - waiting 60 seconds")
                await asyncio.sleep(60)
                raise Exception("Rate limited, retry")

            # Check for server errors
            if response.status_code >= 500:
                print(f"Server error: {response.status_code}")
                raise Exception("Server error, retry")

            # Check for client errors
            if response.status_code >= 400:
                print(f"Client error: {response.status_code}")
                return None

            response.raise_for_status()
            return response.json()

    except httpx.TimeoutException:
        print("Request timed out")
        return None
    except httpx.RequestError as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## Performance Optimization

### 1. Use Async/Await for Concurrent Requests

**Serial (Slow)**:
```python
# ❌ Slow - One request at a time
results = []
for player_id in player_ids:
    data = fetch_player(player_id)
    results.append(data)
# Total time: 50 players × 0.3s = 15 seconds
```

**Concurrent (Fast)**:
```python
# ✅ Fast - Multiple requests simultaneously
import asyncio

async def fetch_all_players(player_ids):
    tasks = [fetch_player(pid) for pid in player_ids]
    return await asyncio.gather(*tasks)

results = await fetch_all_players(player_ids)
# Total time: ~1-2 seconds (with rate limiting)
```

### 2. Batch Fetching with scoringPeriodId=0

**Multiple Calls (Slow)**:
```python
# ❌ Slow - 18 separate API calls
for week in range(1, 19):
    data = fetch_player_week(player_id, week)
# Total time: 18 × 0.3s = 5.4 seconds per player
```

**Single Call (Fast)**:
```python
# ✅ Fast - 1 API call for all weeks
data = fetch_player_all_weeks(player_id, scoring_period=0)
# Total time: 0.3 seconds per player
```

### 3. Response Caching

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def fetch_team_stats_cached(team_id):
    """Cache team stats for 1 hour"""
    cache_key = f"team_{team_id}_{int(time.time() / 3600)}"
    return fetch_team_stats(team_id)

# First call: Hits API
stats1 = fetch_team_stats_cached(12)

# Second call: Returns cached result
stats2 = fetch_team_stats_cached(12)  # Instant!
```

### 4. Session Reuse

```python
# ❌ Slow - Creates new connection every time
def fetch_player(player_id):
    async with httpx.AsyncClient() as client:
        return await client.get(url)

# ✅ Fast - Reuses connection
async def fetch_many_players(player_ids):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for pid in player_ids]
        return await asyncio.gather(*tasks)
```

### Performance Benchmarks

| Method | Time for 100 players | Speedup |
|--------|---------------------|---------|
| Serial + individual weeks | ~90 seconds | 1x |
| Serial + batch weeks | ~30 seconds | 3x |
| Async + individual weeks | ~10 seconds | 9x |
| Async + batch weeks | ~3 seconds | **30x** |

---

## Troubleshooting

### Issue: Empty Response

**Symptoms**:
```python
data = response.json()
players = data.get('players', [])
print(len(players))  # Output: 0
```

**Causes & Solutions**:
1. **Missing X-Fantasy-Filter**: Add player limit filter
2. **Invalid scoringPeriodId**: Use 0 for season data
3. **Wrong format_id**: Use 1 or 3 only (Format 2 returns 404 - not available)

### Issue: 429 Rate Limit Error

**Symptoms**:
```
httpx.HTTPStatusError: 429 Too Many Requests
```

**Solutions**:
1. **Increase delay**: Change from 0.2s to 0.5s or 1.0s
2. **Implement backoff**: Wait 60+ seconds before retrying
3. **Reduce concurrency**: Limit to 3-5 concurrent requests

### Issue: Invalid JSON Response

**Symptoms**:
```python
json.decoder.JSONDecodeError: Expecting value
```

**Causes & Solutions**:
1. **Server error**: Check status code first
2. **Invalid endpoint**: Verify URL is correct
3. **Missing User-Agent**: Add header

### Issue: Missing Player Data

**Symptoms**:
```python
stats = player.get('stats', [])
print(len(stats))  # Output: 0
```

**Causes & Solutions**:
1. **Rookie/new player**: May not have projection data yet
2. **Practice squad**: Only active roster players have projections
3. **Wrong season**: Ensure season year is correct

### Getting Help

For ESP issues:
- Check [examples/](examples/) for working response examples
- Verify request matches examples exactly
- Test with curl first to isolate Python issues
- Check ESPN Fantasy website to confirm data availability

---

## Cross-References

- **Player Data**: See [espn_player_data.md](espn_player_data.md) for complete player field reference
- **Team Data**: See [espn_team_data.md](espn_team_data.md) for complete team field reference
- **ID Mappings**: See [espn_api_reference_tables.md](espn_api_reference_tables.md) for all mapping tables
- **Examples**: See [examples/](examples/) for real API response examples

---

## Changelog

- **2025-12-13**: Verified and corrected documentation
  - Corrected User-Agent requirement: Now recommended, not required
  - Added warning about default 50-player limit
  - Updated quick start example with sortPercOwned filter
  - Verified all endpoints return 200 OK
  - Confirmed format ID 2 returns 404 (Half-PPR unavailable)
- **2025-10-31**: Initial version - All 5 endpoints documented with real examples

---

## ⚠️ Final Disclaimer

ESPN Fantasy Football API is **unofficial**, **undocumented**, and **unsupported**. Use at your own risk:

- ⚠️ May change without notice
- ⚠️ No SLA or guarantees
- ⚠️ Rate limiting enforced
- ⚠️ Use responsibly

**Not affiliated with ESPN.**
