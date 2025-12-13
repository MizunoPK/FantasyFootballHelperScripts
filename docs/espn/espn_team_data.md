# ESPN Fantasy Football API - Team Data Reference

**Last Updated**: 2025-12-13
**API Status**: Unofficial
**Target Audience**: Python Developers (Intermediate)

---

## Table of Contents

1. [Overview](#overview)
2. [Team List Response](#team-list-response)
3. [Team Basic Information](#team-basic-information)
4. [Team Statistics Response](#team-statistics-response)
5. [Statistical Categories](#statistical-categories)
6. [Schedule/Matchup Data](#schedulematchup-data)
7. [Calculating Rankings](#calculating-rankings)
8. [Complete Examples](#complete-examples)

---

## Overview

ESPN provides NFL team data through two main endpoints:
1. **Team List**: Basic information for all 32 teams
2. **Team Statistics**: Detailed statistics for individual teams

### Use Cases

- **Matchup analysis**: Determine opponent strength
- **Strength of schedule**: Calculate difficulty of player schedules
- **Team rankings**: Rank offenses and defenses
- **Player evaluation**: Adjust player values based on team quality

---

## Team List Response

### Endpoint

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams
```

### Response Structure

> **Note**: Teams are nested under `sports[0].leagues[0].teams[]`, not at the root level.

```json
{
  "sports": [{
    "leagues": [{
      "teams": [
        {
          "team": {
            "id": 12,
            "guid": "...",
            "uid": "s:20~l:28~t:12",
            "abbreviation": "KC",
            "displayName": "Kansas City Chiefs",
            "shortDisplayName": "Chiefs",
            "location": "Kansas City",
            "name": "Chiefs",
            "nickname": "Chiefs",
            "slug": "kansas-city-chiefs",
            "color": "e31837",
            "alternateColor": "ffb81c",
            "isActive": true,
            "isAllStar": false,
            "logos": [
              {
                "href": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
                "width": 500,
                "height": 500,
                "alt": "Kansas City Chiefs Logo",
                "rel": ["full", "default"]
              }
            ],
            "links": [...]
          }
        }
      ]
    }]
  }]
}
```

### Parsing the Nested Structure

```python
import httpx

url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
headers = {"User-Agent": "Mozilla/5.0..."}

response = httpx.get(url, headers=headers)
data = response.json()

# Navigate nested structure (NOT data['teams'])
teams = data['sports'][0]['leagues'][0]['teams']

for team_obj in teams:
    team = team_obj['team']
    print(f"{team['abbreviation']}: {team['displayName']}")
```

---

## Team Basic Information

### team.id

**Type**: `integer`
**Description**: ESPN's unique team identifier

```json
"id": 12
```

**Range**: 1-34 (gaps at 31-32)

**See**: [espn_api_reference_tables.md](espn_api_reference_tables.md#team-id-mappings) for complete list

### team.abbreviation

**Type**: `string`
**Description**: Standard NFL team abbreviation

```json
"abbreviation": "KC"
```

**Examples**: "KC", "NE", "SF", "DAL"

**Note**: These match official NFL abbreviations

### team.displayName

**Type**: `string`
**Description**: Full team name

```json
"displayName": "Kansas City Chiefs"
```

### team.location

**Type**: `string`
**Description**: City/region

```json
"location": "Kansas City"
```

### team.name

**Type**: `string`
**Description**: Team nickname/mascot

```json
"name": "Chiefs"
```

### team.slug

**Type**: `string`
**Description**: URL-friendly team identifier

```json
"slug": "kansas-city-chiefs"
```

**Notes**:
- Used in ESPN URLs for team pages
- Lowercase with hyphens

### team.isAllStar

**Type**: `boolean`
**Description**: Whether this is an All-Star team entry

```json
"isAllStar": false
```

**Notes**:
- Always `false` for NFL teams (no All-Star games)
- Present in API response but not relevant for NFL

### team.color & alternateColor

**Type**: `string` (hex color code without #)
**Description**: Team colors

```json
"color": "e31837",
"alternateColor": "ffb81c"
```

**Usage**:
```python
primary_color = f"#{team['color']}"  # #e31837
secondary_color = f"#{team['alternateColor']}"  # #ffb81c
```

### team.logos

**Type**: `array`
**Description**: Team logo URLs and dimensions

```json
"logos": [
  {
    "href": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
    "width": 500,
    "height": 500,
    "alt": "Kansas City Chiefs Logo",
    "rel": ["full", "default"]
  }
]
```

**Usage**:
```python
logo_url = team['logos'][0]['href']
print(f"<img src='{logo_url}' alt='{team['displayName']}'>")
```

---

## Team Statistics Response

### Endpoint

```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics
```

### Response Structure

```json
{
  "status": "success",
  "team": {
    "id": "12",
    "abbreviation": "KC",
    "displayName": "Kansas City Chiefs",
    "recordSummary": "6-7",
    "standingSummary": "3rd in AFC West"
  },
  "season": {
    "year": 2025,
    "type": 2,
    "name": "Regular Season"
  },
  "results": {
    "stats": {
      "id": "0",
      "name": "All Splits",
      "abbreviation": "Any",
      "categories": [
        {
          "name": "passing",
          "displayName": "Passing",
          "abbreviation": "pass",
          "stats": [
            {
              "name": "completions",
              "displayName": "Completions",
              "shortDisplayName": "CMP",
              "description": "The times a player completes a pass...",
              "abbreviation": "CMP",
              "value": 285.0,
              "displayValue": "285",
              "perGameValue": 23.0,
              "perGameDisplayValue": "23"
            }
          ]
        }
      ]
    },
    "opponent": [
      {
        "name": "passing",
        "displayName": "Passing",
        "stats": [...]
      }
    ]
  }
}
```

> **Note**: The response includes both `stats` (team's offensive statistics) and `opponent` (stats allowed by defense). The `opponent` array has the same category structure as `stats`.

---

## Statistical Categories

Teams have statistics grouped into 11 categories:

### All Categories (as returned by API)

| Category Name | Display Name | Description | Stat Count |
|---------------|--------------|-------------|------------|
| `passing` | Passing | QB/passing offense stats | ~24 stats |
| `rushing` | Rushing | Running game stats | ~16 stats |
| `receiving` | Receiving | Pass-catching stats | ~17 stats |
| `miscellaneous` | Miscellaneous | Turnovers, first downs, etc. | ~24 stats |
| `defensive` | Defensive | Tackles, sacks, etc. | ~13 stats |
| `defensiveInterceptions` | Def. Interceptions | Interceptions, returns | ~4 stats |
| `general` | General | Points, yards totals | ~6 stats |
| `returning` | Returning | Kick/punt returns | ~15 stats |
| `kicking` | Kicking | FG, PAT stats | ~25 stats |
| `punting` | Punting | Punt stats | ~14 stats |
| `scoring` | Scoring | TDs, points breakdown | ~9 stats |

> **Note**: Category names are lowercase in API responses (e.g., `"passing"`, not `"Passing"`).

### Key Statistics for Fantasy

#### Offensive Quality Metrics

**totalPointsPerGame**
- **Description**: Average points scored per game
- **Use**: Primary offensive ranking metric
- **Higher is better** for player matchups

```json
{
  "name": "totalPointsPerGame",
  "value": 28.5,
  "displayValue": "28.5"
}
```

**totalYards**
- **Description**: Total offensive yardage
- **Use**: Secondary offensive metric
- **Higher is better**

```json
{
  "name": "totalYards",
  "value": 5432.0,
  "displayValue": "5,432"
}
```

#### Defensive Quality Metrics

**totalTakeaways**
- **Description**: Total turnovers forced (INTs + fumbles)
- **Use**: Primary defensive ranking metric
- **Higher is better** (better defense = worse for opposing players)

```json
{
  "name": "totalTakeaways",
  "value": 18.0,
  "displayValue": "18"
}
```

**pointsPerGameAllowed**
- **Description**: Average points allowed per game
- **Use**: Defensive ranking metric
- **Lower is better** (better defense)

```json
{
  "name": "pointsPerGameAllowed",
  "value": 19.2,
  "displayValue": "19.2"
}
```

### Extracting Statistics

```python
def extract_stat(stats_data, stat_name):
    """Extract specific stat value from team statistics"""
    for category in stats_data['categories']:
        for stat in category['stats']:
            if stat['name'] == stat_name:
                return {
                    'value': float(stat['value']),
                    'display': stat['displayValue'],
                    'description': stat.get('description', '')
                }
    return None

# Usage
stats = response['results']['stats']
ppg = extract_stat(stats, 'totalPointsPerGame')
print(f"Points Per Game: {ppg['display']}")
```

---

## Schedule/Matchup Data

### Scoreboard Response

Teams appear in weekly scoreboard/schedule data:

```json
{
  "events": [
    {
      "id": "401547417",
      "date": "2025-09-07T00:00Z",
      "competitions": [
        {
          "competitors": [
            {
              "id": "12",
              "homeAway": "home",
              "team": {
                "id": "12",
                "abbreviation": "KC",
                "displayName": "Kansas City Chiefs"
              },
              "score": "27"
            },
            {
              "id": "7",
              "homeAway": "away",
              "team": {
                "id": "7",
                "abbreviation": "DEN",
                "displayName": "Denver Broncos"
              },
              "score": "24"
            }
          ]
        }
      ]
    }
  ]
}
```

### competitors[] Array

**Type**: Array of 2 team objects
**Description**: Home and away teams for a game

#### competitor.homeAway

**Type**: `string`
**Values**: "home" or "away"
**Description**: Home/away designation

```json
"homeAway": "home"
```

**Usage**:
```python
for competitor in game['competitions'][0]['competitors']:
    team_abbr = competitor['team']['abbreviation']
    location = competitor['homeAway']
    print(f"{team_abbr} ({location})")
```

#### competitor.score

**Type**: `string` (numeric string)
**Description**: Final or current score

```json
"score": "27"
```

**Note**: Empty or "0" for games not yet played

### Building Matchup Map

```python
def build_weekly_matchups(scoreboard_data):
    """Create dict mapping team → opponent for a week"""
    matchups = {}

    for event in scoreboard_data.get('events', []):
        competitors = event['competitions'][0]['competitors']

        if len(competitors) == 2:
            team1 = competitors[0]['team']['abbreviation']
            team2 = competitors[1]['team']['abbreviation']

            matchups[team1] = {
                'opponent': team2,
                'location': competitors[0]['homeAway']
            }
            matchups[team2] = {
                'opponent': team1,
                'location': competitors[1]['homeAway']
            }

    return matchups

# Usage
matchups = build_weekly_matchups(scoreboard_data)
print(f"KC plays {matchups['KC']['opponent']} at {matchups['KC']['location']}")
# Output: "KC plays DEN at home"
```

---

## Calculating Rankings

### Offensive Rankings

```python
def rank_offenses(teams_stats):
    """Rank teams by offensive quality (points per game)"""
    rankings = []

    for team_id, stats in teams_stats.items():
        ppg = extract_stat(stats, 'totalPointsPerGame')
        if ppg:
            rankings.append({
                'team_id': team_id,
                'ppg': ppg['value']
            })

    # Sort by PPG (descending)
    rankings.sort(key=lambda x: x['ppg'], reverse=True)

    # Assign ranks
    for rank, team in enumerate(rankings, start=1):
        team['rank'] = rank

    return rankings

# Usage
offense_rankings = rank_offenses(all_teams_stats)
print("Top 5 Offenses:")
for team in offense_rankings[:5]:
    print(f"  {team['rank']}. Team {team['team_id']}: {team['ppg']} PPG")
```

### Defensive Rankings

```python
def rank_defenses(teams_stats):
    """Rank teams by defensive quality (takeaways)"""
    rankings = []

    for team_id, stats in teams_stats.items():
        takeaways = extract_stat(stats, 'totalTakeaways')
        if takeaways:
            rankings.append({
                'team_id': team_id,
                'takeaways': takeaways['value']
            })

    # Sort by takeaways (descending - more is better)
    rankings.sort(key=lambda x: x['takeaways'], reverse=True)

    # Assign ranks
    for rank, team in enumerate(rankings, start=1):
        team['rank'] = rank

    return rankings

# Usage
defense_rankings = rank_defenses(all_teams_stats)
print("Top 5 Defenses:")
for team in defense_rankings[:5]:
    print(f"  {team['rank']}. Team {team['team_id']}: {team['takeaways']} takeaways")
```

### Using Rankings for Player Evaluation

```python
def get_matchup_multiplier(player_team_id, opponent_id, team_rankings):
    """Calculate matchup difficulty multiplier for a player"""
    # Get opponent's defensive rank (1-32)
    opponent_defense_rank = team_rankings['defense'].get(opponent_id, 16)

    # Better defense (lower rank) = harder matchup
    if opponent_defense_rank <= 10:
        return 0.9  # Facing top-10 defense (10% penalty)
    elif opponent_defense_rank >= 23:
        return 1.1  # Facing bottom-10 defense (10% bonus)
    else:
        return 1.0  # Average matchup

# Usage
player_team = 12  # KC
opponent = 7      # DEN
multiplier = get_matchup_multiplier(player_team, opponent, rankings)
adjusted_projection = base_projection * multiplier
```

---

## Complete Examples

### Example 1: Full Team Statistics Object

See [examples/team_stats_response.json](examples/team_stats_response.json) for complete real response.

### Example 2: Fetch and Parse All Teams

```python
import httpx

async def fetch_all_teams():
    """Fetch basic info for all 32 NFL teams"""
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
    headers = {"User-Agent": "Mozilla/5.0..."}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json()

    teams = {}
    for sport in data.get('sports', []):
        for league in sport.get('leagues', []):
            for team_obj in league.get('teams', []):
                team = team_obj['team']
                teams[team['id']] = {
                    'id': team['id'],
                    'abbreviation': team['abbreviation'],
                    'name': team['displayName'],
                    'location': team['location']
                }

    return teams

# Usage
teams = await fetch_all_teams()
print(f"Fetched {len(teams)} teams")
for team_id, team in teams.items():
    print(f"  {team['abbreviation']}: {team['name']}")
```

### Example 3: Complete Team Quality Analysis

```python
import httpx
import asyncio

async def analyze_team_quality(team_id):
    """Complete team analysis: offense, defense, next matchup"""

    # Fetch team statistics
    stats_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics"
    headers = {"User-Agent": "Mozilla/5.0..."}

    async with httpx.AsyncClient() as client:
        response = await client.get(stats_url, headers=headers)
        data = response.json()

    stats = data['results']['stats']

    # Extract key metrics
    ppg = extract_stat(stats, 'totalPointsPerGame')
    yards = extract_stat(stats, 'totalYards')
    takeaways = extract_stat(stats, 'totalTakeaways')

    analysis = {
        'team_name': data['team']['displayName'],
        'offensive_ppg': ppg['value'] if ppg else None,
        'total_yards': yards['value'] if yards else None,
        'defensive_takeaways': takeaways['value'] if takeaways else None
    }

    # Categorize offense
    if analysis['offensive_ppg']:
        if analysis['offensive_ppg'] >= 27:
            analysis['offense_rank'] = "Elite"
        elif analysis['offensive_ppg'] >= 24:
            analysis['offense_rank'] = "Above Average"
        elif analysis['offensive_ppg'] >= 20:
            analysis['offense_rank'] = "Average"
        else:
            analysis['offense_rank'] = "Below Average"

    # Categorize defense
    if analysis['defensive_takeaways']:
        if analysis['defensive_takeaways'] >= 20:
            analysis['defense_rank'] = "Elite"
        elif analysis['defensive_takeaways'] >= 15:
            analysis['defense_rank'] = "Above Average"
        elif analysis['defensive_takeaways'] >= 10:
            analysis['defense_rank'] = "Average"
        else:
            analysis['defense_rank'] = "Below Average"

    return analysis

# Usage
team_analysis = await analyze_team_quality(12)  # Kansas City
print(f"{team_analysis['team_name']}:")
print(f"  Offense: {team_analysis['offensive_ppg']} PPG ({team_analysis['offense_rank']})")
print(f"  Defense: {team_analysis['defensive_takeaways']} takeaways ({team_analysis['defense_rank']})")
```

---

## Cross-References

- **Endpoints**: See [espn_api_endpoints.md](espn_api_endpoints.md) for endpoint details
- **Player Data**: See [espn_player_data.md](espn_player_data.md) for player field reference
- **ID Mappings**: See [espn_api_reference_tables.md](espn_api_reference_tables.md#team-id-mappings) for team ID list
- **Examples**: See [examples/team_stats_response.json](examples/team_stats_response.json) for real response

---

## Changelog

- **2025-12-13**: Verified and expanded documentation
  - Updated response structure with opponent stats array
  - Added status, recordSummary, standingSummary fields
  - Verified 11 stat categories against live API
  - Updated category names to lowercase (API returns lowercase)
- **2025-10-31**: Initial version - All team data fields documented with examples

---

## ⚠️ Disclaimer

ESPN Fantasy Football API is **unofficial** and **undocumented**. Field names and structures may change without notice. Use at your own risk.

**Not affiliated with ESPN.**
