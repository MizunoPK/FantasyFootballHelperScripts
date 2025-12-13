# ESPN Fantasy Football API Documentation

**Last Updated**: 2025-12-13
**API Status**: Unofficial
**Purpose**: Comprehensive reference for ESPN's Fantasy Football API

---

## ⚠️ Important Disclaimers

ESPN Fantasy Football API is **unofficial**, **undocumented**, and **unsupported**:

- ❌ Not officially documented or supported by ESPN
- ❌ May change without notice
- ❌ No SLA or reliability guarantees
- ⚠️ Rate limiting enforced - use responsibly
- ✅ Free and no authentication required

**Use at your own risk. Not affiliated with ESPN.**

---

## Documentation Index

### Core References

| Document | Description | Pages |
|----------|-------------|-------|
| **[espn_api_endpoints.md](espn_api_endpoints.md)** | Complete endpoint reference (all 5 endpoints) | ~6 pages |
| **[espn_player_data.md](espn_player_data.md)** | Player data fields and structures | ~5 pages |
| **[espn_team_data.md](espn_team_data.md)** | Team data fields and structures | ~4 pages |
| **[espn_api_reference_tables.md](espn_api_reference_tables.md)** | ID mapping tables (positions, teams, formats) | ~3 pages |

### Additional Resources

| Resource | Description |
|----------|-------------|
| **[examples/](examples/)** | Real ESPN API response examples (5 JSON files) |
| **[examples/README.md](examples/README.md)** | Documentation for example responses |

---

## What's Available

ESPN's Fantasy Football API provides:

- **Player Projections**: Season and weekly fantasy point projections
- **Player Statistics**: Actual game results and historical data
- **Team Information**: NFL team IDs, names, and statistics
- **Schedule Data**: Weekly matchups and game information
- **Draft Rankings**: ESPN's rankings by scoring format (PPR, Standard, Half-PPR)

---

## Quick Start

### Requirements

```bash
pip install httpx  # Modern HTTP client with async support
```

### Example 1: Fetch Top Players (Simplest)

```python
import httpx

# Configuration
ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
SEASON = 2025
FORMAT_ID = 3  # 1=Standard, 3=PPR (Note: Format 2 returns 404)

# Build URL
url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leaguedefaults/{FORMAT_ID}"

# Headers (recommended for stability)
# Note: User-Agent is no longer strictly required as of 2025-12
headers = {"User-Agent": ESPN_USER_AGENT}

# IMPORTANT: Use sortPercOwned filter to get all players (default returns only 50)
headers["X-Fantasy-Filter"] = '{"players":{"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'

# Query parameters
params = {
    "view": "kona_player_info",
    "scoringPeriodId": 0  # 0 = season totals
}

# Make request
response = httpx.get(url, headers=headers, params=params, timeout=30.0)
response.raise_for_status()
data = response.json()

print(f"Fetched {len(data['players'])} players")  # Should be ~1081

# Parse and display
for player_obj in data['players'][:5]:
    player = player_obj['player']
    name = f"{player['firstName']} {player['lastName']}"

    # Get season projection (use appliedTotal, not projectedTotal)
    points = 0.0
    for stat in player.get('stats', []):
        if stat.get('scoringPeriodId') == 0 and stat.get('statSourceId') == 1:
            points = stat.get('appliedTotal', 0.0)  # appliedTotal for both actuals and projections
            break

    print(f"{name}: {points:.1f} projected points")
```

**Output**:
```
Fetched 1081 players
Jahmyr Gibbs: 324.9 projected points
Ja'Marr Chase: 285.5 projected points
Amon-Ra St. Brown: 268.2 projected points
...
```

> **Warning**: Without the `sortPercOwned` filter, the API returns only 50 players by default!

---

### Example 2: Get Player Weekly Data

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
    "scoringPeriodId": 0  # Fetches ALL weeks in one call (optimization!)
}

response = httpx.get(url, headers=headers, params=params, timeout=30.0)
data = response.json()

player = data['players'][0]['player']
print(f"{player['firstName']} {player['lastName']} - Week by Week:")

# Extract weekly points
for stat in player.get('stats', []):
    week = stat.get('scoringPeriodId')
    source = stat.get('statSourceId')

    # Only show actual results (not projections)
    if source == 0 and 1 <= week <= 18:
        points = stat.get('appliedTotal', 0.0)
        print(f"  Week {week}: {points:.1f} points")
```

---

### Example 3: Get All NFL Teams

```python
import httpx

url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

response = httpx.get(url, headers=headers, timeout=30.0)
data = response.json()

print("All NFL Teams:")
for sport in data.get('sports', []):
    for league in sport.get('leagues', []):
        for team_obj in league.get('teams', []):
            team = team_obj['team']
            print(f"  {team['abbreviation']}: {team['displayName']}")
```

---

### Example 4: Get Team Statistics

```python
import httpx

# Kansas City Chiefs (team_id=12)
team_id = 12

url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

response = httpx.get(url, headers=headers, timeout=30.0)
data = response.json()

# Extract key stats
team_name = data['team']['displayName']
print(f"{team_name} Statistics:")

for category in data['results']['stats']['categories']:
    for stat in category['stats']:
        if stat['name'] == 'totalPointsPerGame':
            print(f"  Points Per Game: {stat['displayValue']}")
        elif stat['name'] == 'totalYards':
            print(f"  Total Yards: {stat['displayValue']}")
        elif stat['name'] == 'totalTakeaways':
            print(f"  Takeaways: {stat['displayValue']}")
```

---

### Example 5: Get Weekly Schedule/Matchups

```python
import httpx

url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

params = {
    "seasontype": 2,  # Regular season
    "week": 1,
    "dates": 2025
}

response = httpx.get(url, headers=headers, params=params, timeout=30.0)
data = response.json()

print("Week 1 Matchups:")
for event in data.get('events', []):
    competitors = event['competitions'][0]['competitors']

    team1 = competitors[0]['team']['abbreviation']
    team2 = competitors[1]['team']['abbreviation']

    location1 = competitors[0]['homeAway']
    location2 = competitors[1]['homeAway']

    print(f"  {team1} ({location1}) vs {team2} ({location2})")
```

---

### Example 6: Error Handling and Rate Limiting

```python
import httpx
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, max=10)
)
async def fetch_with_retry(url, headers, params):
    """Fetch with automatic retry and rate limiting"""

    # Rate limiting: Wait 0.2s between requests
    await asyncio.sleep(0.2)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params, timeout=30.0)

        # Handle rate limiting
        if response.status_code == 429:
            print("Rate limited - waiting 60 seconds")
            await asyncio.sleep(60)
            raise Exception("Rate limited, retry")

        # Handle server errors
        if response.status_code >= 500:
            print(f"Server error: {response.status_code}")
            raise Exception("Server error, retry")

        response.raise_for_status()
        return response.json()

# Usage
async def main():
    url = "https://lm-api-reads.fantasy.espn.com/..."
    headers = {"User-Agent": "Mozilla/5.0..."}
    params = {"view": "kona_player_info", "scoringPeriodId": 0}

    try:
        data = await fetch_with_retry(url, headers, params)
        print(f"Success: {len(data.get('players', []))} players")
    except Exception as e:
        print(f"Failed after retries: {e}")

# Run
asyncio.run(main())
```

---

## Common Pitfalls

### 1. Default 50-Player Limit

```python
# ❌ Wrong - Returns only 50 players
response = httpx.get(url, headers=headers)
data = response.json()
print(len(data['players']))  # 50

# ✅ Correct - Use sortPercOwned filter
headers["X-Fantasy-Filter"] = '{"players":{"sortPercOwned":{"sortPriority":4,"sortAsc":false}}}'
response = httpx.get(url, headers=headers)
data = response.json()
print(len(data['players']))  # 1081+
```

### 2. No Rate Limiting

```python
# ❌ Wrong - Will get rate limited
for player_id in player_ids:
    data = fetch_player(player_id)

# ✅ Correct - Add delays
import time
for player_id in player_ids:
    data = fetch_player(player_id)
    time.sleep(0.2)  # 0.2s = 5 requests/sec
```

### 3. Not Handling Errors

```python
# ❌ Wrong - Crashes on error
response = httpx.get(url)
data = response.json()

# ✅ Correct - Handle errors
try:
    response = httpx.get(url, timeout=30.0)
    response.raise_for_status()
    data = response.json()
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e.response.status_code}")
except httpx.RequestError as e:
    print(f"Request error: {e}")
```

---

## ID Mappings Quick Reference

### Position IDs
- `1` = QB
- `2` = RB
- `3` = WR
- `4` = TE
- `5` = K
- `16` = DST

### Scoring Format IDs (in URL path)
- `1` = Standard
- `2` = ~~Half-PPR~~ (Returns 404 - not available)
- `3` = PPR (Full)

### Stat Source IDs
- `0` = Actual results (`appliedTotal` field)
- `1` = Projections (`appliedTotal` field - ⚠️ `projectedTotal` is deprecated)

> **2025 API Change**: Both stat sources now use `appliedTotal`. The `projectedTotal` field is deprecated and returns `null`.

**Full mappings**: See [espn_api_reference_tables.md](espn_api_reference_tables.md)

---

## Next Steps

### For Beginners
1. ✅ Run Example 1 to verify API access
2. ✅ Read [espn_api_endpoints.md](espn_api_endpoints.md) for all endpoints
3. ✅ Check [examples/](examples/) for real response structures

### For Integration
1. ✅ Read [espn_player_data.md](espn_player_data.md) for all player fields
2. ✅ Read [espn_team_data.md](espn_team_data.md) for all team fields
3. ✅ Implement error handling and rate limiting (Example 6)

### For Advanced Usage
1. ✅ Use async/await for concurrent requests
2. ✅ Implement response caching
3. ✅ Use `scoringPeriodId=0` for batch fetching
4. ✅ Read [espn_api_endpoints.md#performance-optimization](espn_api_endpoints.md#performance-optimization)

---

## Support and Issues

These docs are **community-maintained** and **unofficial**:

- **Not supported by ESPN** - No official help available
- **API may change** - Documentation may become outdated
- **Use responsibly** - Respect ESPN's servers with rate limiting

For questions about **this documentation project**:
- Check the main project [README.md](../README.md)
- Review [CLAUDE.md](../CLAUDE.md) for contribution guidelines

---

## License

This documentation is part of the Fantasy Football Helper Scripts project.

**Not affiliated with ESPN.**

---

*Documentation generated 2025-10-31, verified and updated 2025-12-13 against live ESPN API.*
