# ESPN API - NFL Game Data Research Report (v3)

**Research Date**: November 25, 2025
**Last Updated**: November 25, 2025 (Round 3 Verification - Weather Correction)
**Researcher**: Claude Code (Opus 4.5)
**Purpose**: Comprehensive investigation of available NFL game data through ESPN's unofficial API

---

## Executive Summary

This report documents the available data fields for NFL games through ESPN's unofficial API endpoints. The research covers game scores, timing, venue information, international game detection, **weather data availability**, broadcast information, and player statistics.

**Key Findings**:
1. **Final scores and quarter-by-quarter scores** are available (scores as STRING type)
2. **Overtime games** have 5 linescores (periods) instead of 4
3. **International games** can be reliably detected via venue country and game notes
4. **Weather data IS AVAILABLE for future games** (major correction from v2)
5. **Weather data NOT available for completed games** (verified)
6. **Game dates/times** are in ISO 8601 format with UTC timezone
7. **`indoor` field** is ONLY available in scoreboard endpoint, NOT in summary
8. **Venue capacity** is NOT available in the API
9. **Bye weeks** can be detected by missing teams in weekly scoreboard
10. **Predictor/Odds** are available for future games only

---

## Table of Contents

1. [API Endpoints](#api-endpoints)
2. [Available Data Fields](#available-data-fields)
3. [International Game Detection](#international-game-detection)
4. [Weather Data Availability](#weather-data-availability) **[MAJOR UPDATE]**
5. [Scores and Game Results](#scores-and-game-results)
6. [Overtime Games](#overtime-games)
7. [Scheduled vs Completed Games](#scheduled-vs-completed-games)
8. [Predictor and Odds](#predictor-and-odds) **[NEW SECTION]**
9. [Date and Time Information](#date-and-time-information)
10. [Venue Information](#venue-information)
11. [Bye Week Detection](#bye-week-detection)
12. [Broadcast Information](#broadcast-information)
13. [Game Leaders and Statistics](#game-leaders-and-statistics)
14. [Sample API Responses](#sample-api-responses)
15. [Implementation Recommendations](#implementation-recommendations)
16. [Limitations and Caveats](#limitations-and-caveats)

---

## API Endpoints

### Primary Endpoint: Scoreboard
```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
```

**Query Parameters**:
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `seasontype` | int | 1=preseason, 2=regular, 3=postseason | `2` |
| `week` | int | Week number (1-18 for regular season) | `12` |
| `dates` | int | Season year | `2025` |

**Top-Level Response Keys**:
- `leagues` - NFL league information and season calendar
- `season` - Current season info
- `week` - Current week info
- `events` - Array of games
- `provider` - Betting provider info (ESPN BET)

**Example Request**:
```python
import httpx

url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
params = {"seasontype": 2, "week": 12, "dates": 2025}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

response = httpx.get(url, headers=headers, params=params)
data = response.json()
```

### Secondary Endpoint: Game Summary
```
GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary
```

**Query Parameters**:
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `event` | str | ESPN game ID | `401772510` |

**Top-Level Response Keys**:
- `boxscore` - Team and player statistics
- `gameInfo` - Venue, attendance, officials, **weather** (future games only)
- `drives` - Drive summaries
- `leaders` - Game statistical leaders
- `injuries` - Player injuries
- `scoringPlays` - Scoring play details
- `winprobability` - Win probability timeline
- `againstTheSpread` - Betting results
- `predictor` - Win probability prediction (future games only)
- `odds` - Betting odds (empty for completed games)
- `news` - Related news articles
- `header` - Game header info
- `standings` - Team standings

---

## Available Data Fields

### From Scoreboard Endpoint (per game)

| Field Path | Type | Description | Always Available |
|------------|------|-------------|------------------|
| `id` | string | Unique game identifier | Yes |
| `name` | string | Full matchup name (e.g., "Buffalo Bills at Houston Texans") | Yes |
| `shortName` | string | Abbreviated (e.g., "BUF @ HOU") | Yes |
| `date` | string | ISO 8601 timestamp with UTC timezone | Yes |
| `season.year` | int | Season year | Yes |
| `season.type` | int | Season type (1/2/3) | Yes |
| `week.number` | int | Week number | Yes |
| `competitions[0].venue.id` | string | Venue identifier | Yes |
| `competitions[0].venue.fullName` | string | Venue name | Yes |
| `competitions[0].venue.address.city` | string | City | Yes |
| `competitions[0].venue.address.state` | string | State (if USA) | Conditional |
| `competitions[0].venue.address.country` | string | Country | Yes |
| `competitions[0].venue.indoor` | boolean | Indoor stadium flag | **Yes (ONLY in scoreboard)** |
| `competitions[0].neutralSite` | boolean | Neutral site flag | Yes |
| `competitions[0].attendance` | int | Game attendance | Yes (completed games) |
| `competitions[0].odds[]` | array | Betting odds | **Yes (future games only)** |
| `competitions[0].status.type.completed` | boolean | Game finished | Yes |
| `competitions[0].status.type.state` | string | "pre", "in", or "post" | Yes |
| `competitions[0].status.type.description` | string | "Scheduled", "In Progress", "Final" | Yes |
| `competitions[0].status.type.detail` | string | "Final", "Final/OT", "1st Quarter" | Yes |
| `competitions[0].notes[].headline` | string | Special game designation | Conditional |
| `competitions[0].broadcasts[].names` | array | Broadcast networks | Yes |
| `competitions[0].competitors[].team.abbreviation` | string | Team abbreviation | Yes |
| `competitions[0].competitors[].score` | **STRING** | Team score ("23", not 23) | Yes |
| `competitions[0].competitors[].winner` | boolean/null | Winner flag (null if scheduled) | Yes |
| `competitions[0].competitors[].homeAway` | string | "home" or "away" | Yes |
| `competitions[0].competitors[].linescores[]` | array/null | Quarter scores (null if scheduled) | Yes |
| `competitions[0].competitors[].records[]` | array | Team records (overall, home, road) | Yes |
| `competitions[0].leaders[]` | array | Game leaders (passing/rushing/receiving) | Yes (completed) |
| `competitions[0].headlines[]` | array | Game recap headlines | Yes (completed) |
| `weather` | object | Weather at game level | **Yes (future games only)** |
| `weather.displayValue` | string | Weather condition text | "Flurries", "Partly Cloudy" |
| `weather.temperature` | int | Temperature (°F) | 37 |

### From Game Summary Endpoint (additional)

| Field Path | Type | Description | Always Available |
|------------|------|-------------|------------------|
| `gameInfo.attendance` | int | Attendance | Yes |
| `gameInfo.venue.fullName` | string | Venue name | Yes |
| `gameInfo.venue.grass` | boolean | Natural grass flag | Yes |
| `gameInfo.venue.indoor` | - | **NOT AVAILABLE** | No |
| `gameInfo.weather` | object | Weather conditions | **YES (future games only)** |
| `gameInfo.officials[]` | array | Game officials | Yes |
| `boxscore.teams[].statistics[]` | array | Team statistics | Yes |
| `drives.previous[]` | array | Drive summaries | Yes |
| `scoringPlays[]` | array | Scoring play details | Yes |
| `winprobability[]` | array | Win probability data | Yes (completed) |
| `odds[]` | array | Betting odds | **Empty for completed games** |
| `predictor` | object | Win probability | **Yes (future games only)** |
| `againstTheSpread[]` | array | Betting results | Yes (completed) |

---

## International Game Detection

International games can be reliably detected using multiple indicators:

### Detection Method 1: Venue Country (Primary - Recommended)
```python
venue_country = game["competitions"][0]["venue"]["address"]["country"]
is_international = venue_country != "USA"
```

### Detection Method 2: Game Notes (Secondary)
```python
notes = game["competitions"][0].get("notes", [])
game_headlines = [n["headline"] for n in notes if n.get("headline")]
# Examples: "NFL São Paulo Game", "NFL London Games", "NFL Berlin Game"
```

### Detection Method 3: Neutral Site Flag (Supporting)
```python
is_neutral = game["competitions"][0]["neutralSite"]
# Usually True for international games
```

### 2025 International Games (Verified)

| Week | Game | City | Country | Venue | Note |
|------|------|------|---------|-------|------|
| 1 | KC VS LAC | Sao Paulo | Brazil | Corinthians Arena | NFL São Paulo Game |
| 4 | MIN VS PIT | Dublin | Ireland | Croke Park | NFL Dublin Game |
| 5 | MIN VS CLE | London | England | Tottenham Hotspur Stadium | NFL London Games |
| 6 | DEN VS NYJ | London | England | Tottenham Hotspur Stadium | NFL London Games |
| 7 | LAR VS JAX | London | England | Wembley Stadium | NFL London Games |
| 10 | ATL VS IND | Berlin | Germany | Olympic Stadium Berlin | NFL Berlin Game |
| 11 | WSH VS MIA | Madrid | Spain | Santiago Bernabéu | NFL Madrid Game |

---

## Weather Data Availability

### MAJOR CORRECTION: Weather IS Available for Future Games

**Previous incorrect claim**: Weather data is NOT available from the ESPN API.

**CORRECTED finding**: Weather data **IS AVAILABLE** for future/scheduled games, but **NOT for completed games**.

### How Weather Works

| Game State | Scoreboard (game.weather) | Summary (gameInfo.weather) |
|------------|---------------------------|----------------------------|
| Scheduled (state="pre") | **YES** | **YES** |
| Completed (state="post") | **NO** | **NO** |

### Weather Data Locations

Weather is available in **BOTH** endpoints for future games:

**Scoreboard** (game-level):
```python
weather = game.get("weather")  # At game level, not in competition
# Has: displayValue, temperature, highTemperature, conditionId
```

**Summary** (gameInfo):
```python
summary = await fetch_summary(game_id)
weather = summary.get("gameInfo", {}).get("weather")
# Has: temperature, highTemperature, lowTemperature, conditionId, gust, precipitation
```

**Key Difference**: Scoreboard weather includes `displayValue` (text like "Flurries"), while Summary weather includes `gust` and `precipitation`.

### Weather Field Structure

**Scoreboard** (game.weather):
```json
{
    "displayValue": "Flurries",  // str - Text description (scoreboard only)
    "temperature": 37,           // int - Temperature in Fahrenheit
    "highTemperature": 37,       // int - High temp prediction
    "conditionId": "19",         // str - AccuWeather condition code
    "link": {...}
}
```

**Summary** (gameInfo.weather):
```json
{
    "temperature": 37,           // int - Temperature in Fahrenheit
    "highTemperature": 37,       // int - High temp prediction
    "lowTemperature": 37,        // int - Low temp prediction (summary only)
    "conditionId": "19",         // str - AccuWeather condition code
    "gust": 39,                  // int - Wind gust speed mph (summary only)
    "precipitation": 56,         // int - Precipitation % (summary only)
    "link": {
        "href": "http://www.accuweather.com/...",
        "text": "Weather"
    }
}
```

### Weather Field Types

| Field | Type | Location | Description |
|-------|------|----------|-------------|
| `displayValue` | str | Scoreboard only | Text description ("Flurries", "Partly Cloudy") |
| `temperature` | int | Both | Current/predicted temperature (°F) |
| `highTemperature` | int | Both | High temperature prediction (°F) |
| `lowTemperature` | int | Summary only | Low temperature prediction (°F) |
| `conditionId` | str | Both | AccuWeather condition identifier |
| `gust` | int | Summary only | Wind gust speed (mph) |
| `precipitation` | int | Summary only | Precipitation probability (%) |
| `link` | dict | Both | Link to AccuWeather forecast |

### Weather Availability by Game Proximity

Weather data appears approximately 1 week before the game:

| Week Distance | Weather Available |
|---------------|-------------------|
| Current week games | YES - 100% have weather |
| Next week games | PARTIAL - ~25% have weather |
| 2+ weeks away | NO - Weather not yet available |

**Evidence (tested 2025-11-25)**:
- Week 13 (current week): All 16 games have weather
- Week 14 (next week): 4 of 16 games have weather
- Week 15+: No games have weather yet

### Example: Fetching Weather for Upcoming Games

```python
async def get_weather_for_game(game_id: str) -> dict | None:
    """Get weather for an upcoming game.

    Returns weather dict if available, None otherwise.
    Weather is typically available ~1 week before game.
    """
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary"
    params = {"event": game_id}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    game_info = data.get("gameInfo", {})
    return game_info.get("weather")  # Returns dict or None


# Example usage
weather = await get_weather_for_game("401772891")
if weather:
    temp = weather["temperature"]      # 37
    precip = weather["precipitation"]  # 56 (percent)
    gust = weather["gust"]             # 39 (mph)
```

### Weather Caveats

1. **Future games only**: Weather is never available for completed games
2. **Time-dependent**: Weather appears ~1 week before game time
3. **Indoor stadiums**: Weather is still provided (outdoor forecast at location)
4. **AccuWeather source**: Data comes from AccuWeather via ESPN

---

## Scores and Game Results

### Score Field Type

**IMPORTANT**: The `score` field is a **STRING**, not an integer.

```python
# Correct usage
score = competitor["score"]  # Returns "23" (string)
score_int = int(competitor["score"])  # Convert to integer

# Type verification
type(competitor["score"])  # <class 'str'>
```

### Extracting Scores
```python
for competitor in game["competitions"][0]["competitors"]:
    team = competitor["team"]["abbreviation"]
    score = int(competitor["score"])  # Convert from string
    is_home = competitor["homeAway"] == "home"
    is_winner = competitor["winner"]  # True, False, or None
```

### Quarter-by-Quarter Scores (Linescores)

```python
linescores = competitor["linescores"]
# Returns array for completed games, None for scheduled games

# Each linescore entry:
{
    "value": 7.0,           # Score as FLOAT
    "displayValue": "7",    # Score as STRING
    "period": 1             # Quarter number (1-4, or 5 for OT)
}

# Extract quarter scores
quarters = [int(q["value"]) for q in linescores]
# Example: [7, 14, 3, 0] for a 4-quarter game
# Example: [10, 7, 0, 10, 7] for an overtime game
```

---

## Overtime Games

Games that go to overtime have **5 linescores instead of 4**.

### Detection
```python
linescores = competitor.get("linescores", [])
is_overtime = linescores and len(linescores) > 4

if is_overtime:
    overtime_score = int(linescores[4]["value"])
```

### Status Field for Overtime
```python
status = comp["status"]["type"]
# For overtime games:
status["detail"]  # Returns "Final/OT"
status["description"]  # Returns "Final"
```

### 2025 Overtime Games (Through Week 12)

| Week | Game | Result |
|------|------|--------|
| 2 | NYG @ DAL | Final/OT |
| 4 | GB @ DAL | Final/OT |
| 5 | SF @ LAR | Final/OT |
| 9 | JAX @ LV | Final/OT |
| 10 | ATL VS IND | Final/OT |
| 11 | WSH VS MIA | Final/OT |
| 11 | CAR @ ATL | Final/OT |
| 12 | NYG @ DET | Final/OT |
| 12 | IND @ KC | Final/OT |
| 12 | JAX @ ARI | Final/OT |

---

## Scheduled vs Completed Games

### Field Differences

| Field | Completed Games | Scheduled Games |
|-------|-----------------|-----------------|
| `score` | Actual score ("23") | "0" |
| `winner` | `true` or `false` | `null` |
| `linescores` | Array of quarters | `null` |
| `status.type.state` | "post" | "pre" |
| `status.type.description` | "Final" | "Scheduled" |
| `status.type.completed` | `true` | `false` |
| `leaders` | Present | Empty or absent |
| `headlines` | Present | Empty |
| `gameInfo.weather` | `null` | **Available** |
| `predictor` | `null` | **Available** |
| `odds` | Empty | **Available** |

### Detection
```python
status = comp["status"]["type"]
is_completed = status["completed"]
is_scheduled = status["state"] == "pre"
is_in_progress = status["state"] == "in"
```

---

## Predictor and Odds

### Predictor (Future Games Only)

The `predictor` field is available in the summary endpoint for scheduled games:

```python
summary = await fetch_summary(game_id)
predictor = summary.get("predictor")
```

**Structure**:
```json
{
    "header": "Matchup Predictor",
    "homeTeam": {
        "id": "8",
        "gameProjection": "54",        // Win probability %
        "teamChanceLoss": "45.6"       // Loss probability %
    },
    "awayTeam": {
        "id": "9",
        "gameProjection": "45.6",
        "teamChanceLoss": "54"
    }
}
```

### Odds (Future Games Only)

Betting odds are available in the **scoreboard** endpoint for future games:

```python
odds = game["competitions"][0].get("odds", [])
```

**Structure**:
```json
{
    "provider": {
        "id": "58",
        "name": "ESPN BET"
    },
    "details": "DET -2.5",
    "overUnder": 48.5,
    "spread": -2.5,
    "awayTeamOdds": {
        "favorite": false,
        "underdog": true,
        "moneyLine": 120,
        "spreadOdds": -105.0
    },
    "homeTeamOdds": {
        "favorite": true,
        "underdog": false,
        "moneyLine": -140,
        "spreadOdds": -115.0
    }
}
```

### Availability Summary

| Data | Scoreboard | Summary | Future Games | Completed Games |
|------|------------|---------|--------------|-----------------|
| Odds | YES | YES | **Available** | Empty |
| Predictor | NO | YES | **Available** | null |
| Weather | NO | YES | **Available** | null |

---

## Date and Time Information

### Format
All dates are in **ISO 8601 format with UTC timezone** (Z suffix):
```
2025-11-21T01:15Z  (Thursday Night Football)
2025-09-07T17:00Z  (Sunday 1pm ET game)
```

### Parsing
```python
from datetime import datetime

date_str = game["date"]  # "2025-11-21T01:15Z"
dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
day_name = dt.strftime('%A')  # "Friday"
```

### Common Game Time Slots (UTC)

| Slot | UTC Time | Eastern Time | Typical Day |
|------|----------|--------------|-------------|
| Early Sunday | 18:00Z | 1:00 PM ET | Sunday |
| Late Sunday (Early) | 21:05Z | 4:05 PM ET | Sunday |
| Late Sunday (Late) | 21:25Z | 4:25 PM ET | Sunday |
| Sunday Night | 01:15Z+1 | 8:15 PM ET | Sunday |
| Thursday Night | 01:15Z | 8:15 PM ET | Thursday |
| Monday Night | 01:15Z | 8:15 PM ET | Monday |

---

## Venue Information

### Scoreboard Endpoint Fields
```python
venue = game["competitions"][0]["venue"]

{
    "id": "3891",
    "fullName": "NRG Stadium",
    "address": {
        "city": "Houston",
        "state": "TX",
        "country": "USA"
    },
    "indoor": true  # ONLY available in scoreboard
}
```

### Summary Endpoint Fields
```python
venue = summary["gameInfo"]["venue"]

{
    "id": "3891",
    "guid": "...",
    "fullName": "NRG Stadium",
    "address": {...},
    "grass": false,  # Natural grass flag
    "images": [...]  # Stadium images
    # NOTE: "indoor" is NOT present here
}
```

### Important Notes
- **`indoor`**: Only in scoreboard endpoint, NOT in summary
- **`grass`**: Only in summary endpoint, NOT in scoreboard
- **`capacity`**: NOT available in either endpoint

### Stadium Types (Examples)

| Stadium | Indoor | Grass |
|---------|--------|-------|
| NRG Stadium (Houston) | true | false |
| Soldier Field (Chicago) | false | true |
| SoFi Stadium (LA) | true | false |
| Lambeau Field (Green Bay) | false | true |
| Lucas Oil Stadium (Indy) | true | true |
| U.S. Bank Stadium (Minnesota) | true | false |

---

## Bye Week Detection

Teams on bye weeks do not appear in the scoreboard for that week.

### Detection Method
```python
ALL_NFL_TEAMS = {
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LAC", "LAR", "LV", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WSH"
}

def get_bye_teams(scoreboard_data):
    playing = set()
    for game in scoreboard_data["events"]:
        for comp in game["competitions"]:
            for competitor in comp["competitors"]:
                playing.add(competitor["team"]["abbreviation"])
    return ALL_NFL_TEAMS - playing
```

### 2025 Bye Week Schedule (Verified)

| Week | Teams on Bye |
|------|--------------|
| 5 | ATL, CHI, GB, PIT |
| 6 | HOU, MIN |
| 7 | BAL, BUF |
| 8 | ARI, DET, JAX, LAR, LV, SEA |
| 9 | CLE, NYJ, PHI, TB |
| 10 | CIN, DAL, KC, TEN |
| 11 | IND, NO |
| 12 | DEN, LAC, MIA, WSH |
| 14 | CAR, NE, NYG, SF |

---

## Broadcast Information

### Fields
```python
comp = game["competitions"][0]

# Primary broadcast string
broadcast = comp.get("broadcast")  # "Prime Video"

# Broadcast array with market info
broadcasts = comp.get("broadcasts", [])
# [{"market": "national", "names": ["Prime Video"]}]

# Detailed geo broadcasts
geo = comp.get("geoBroadcasts", [])
# [{"type": {...}, "market": {...}, "media": {"shortName": "Prime Video"}}]
```

### Common Networks (2025)
- **NBC / Peacock**: Sunday Night Football
- **Prime Video**: Thursday Night Football
- **FOX**: NFC games
- **CBS**: AFC games
- **ESPN / ESPN+**: Monday Night Football
- **YouTube**: Some international games
- **NFL Network**: Select games

---

## Game Leaders and Statistics

### From Scoreboard (3 categories)
```python
leaders = game["competitions"][0]["leaders"]

for leader in leaders:
    category = leader["name"]        # "passingYards", "rushingYards", "receivingYards"
    display = leader["displayName"]  # "Passing Leader"

    for player in leader["leaders"]:
        athlete = player["athlete"]
        name = athlete["fullName"]
        player_id = athlete["id"]
        position = athlete["position"]["abbreviation"]
        value = player["value"]           # Numeric (188.0)
        display_val = player["displayValue"]  # "24/34, 253 YDS, 2 INT"
```

### From Summary (Full Statistics)

The `boxscore.teams[].statistics[]` array contains 25 team statistics:
- firstDowns, firstDownsPassing, firstDownsRushing, firstDownsPenalty
- thirdDownEff, fourthDownEff
- totalOffensivePlays, totalYards, yardsPerPlay, totalDrives
- netPassingYards, completionAttempts, yardsPerPass, interceptions
- sacksYardsLost, rushingYards, rushingAttempts, yardsPerRushAttempt
- redZoneAttempts, totalPenaltiesYards, turnovers, fumblesLost
- defensiveTouchdowns, possessionTime

---

## Sample API Responses

### Future Game with Weather
```json
{
  "shortName": "GB @ DET",
  "date": "2025-11-27T17:30Z",
  "competitions": [{
    "status": {
      "type": {
        "state": "pre",
        "description": "Scheduled",
        "completed": false
      }
    },
    "competitors": [{
      "score": "0",
      "winner": null,
      "linescores": null
    }],
    "odds": [{
      "provider": {"name": "ESPN BET"},
      "details": "DET -2.5",
      "overUnder": 48.5
    }]
  }]
}
```

### Summary with Weather (Future Game)
```json
{
  "gameInfo": {
    "venue": {...},
    "weather": {
      "temperature": 37,
      "highTemperature": 37,
      "lowTemperature": 37,
      "conditionId": "19",
      "gust": 39,
      "precipitation": 56,
      "link": {
        "href": "http://www.accuweather.com/..."
      }
    }
  },
  "predictor": {
    "header": "Matchup Predictor",
    "homeTeam": {
      "id": "8",
      "gameProjection": "54"
    },
    "awayTeam": {
      "id": "9",
      "gameProjection": "45.6"
    }
  }
}
```

### Completed Game (No Weather)
```json
{
  "id": "401772946",
  "name": "Buffalo Bills at Houston Texans",
  "shortName": "BUF @ HOU",
  "date": "2025-11-21T01:15Z",
  "competitions": [{
    "venue": {
      "id": "3891",
      "fullName": "NRG Stadium",
      "address": {"city": "Houston", "state": "TX", "country": "USA"},
      "indoor": true
    },
    "status": {
      "type": {
        "completed": true,
        "description": "Final",
        "state": "post"
      }
    },
    "competitors": [{
      "team": {"abbreviation": "HOU"},
      "winner": true,
      "score": "23",
      "linescores": [
        {"value": 3.0, "period": 1},
        {"value": 17.0, "period": 2},
        {"value": 3.0, "period": 3},
        {"value": 0.0, "period": 4}
      ]
    }]
  }]
}
```

### Overtime Game Response
```json
{
  "shortName": "NYG @ DET",
  "competitions": [{
    "status": {
      "type": {
        "description": "Final",
        "detail": "Final/OT"
      }
    },
    "competitors": [{
      "score": "34",
      "linescores": [
        {"value": 0.0, "period": 1},
        {"value": 17.0, "period": 2},
        {"value": 0.0, "period": 3},
        {"value": 10.0, "period": 4},
        {"value": 7.0, "period": 5}
      ]
    }]
  }]
}
```

### International Game Response
```json
{
  "shortName": "KC VS LAC",
  "date": "2025-09-06T00:00Z",
  "competitions": [{
    "venue": {
      "fullName": "Corinthians Arena",
      "address": {"city": "Sao Paulo", "country": "Brazil"},
      "indoor": false
    },
    "neutralSite": true,
    "notes": [{"headline": "NFL São Paulo Game"}]
  }]
}
```

---

## Implementation Recommendations

### 1. Fetching All Games for a Week
```python
async def fetch_week_games(season: int, week: int) -> list:
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    params = {"seasontype": 2, "week": week, "dates": season}
    headers = {"User-Agent": "Mozilla/5.0..."}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()
        return data.get("events", [])
```

### 2. Fetching Weather for Upcoming Games
```python
async def get_upcoming_games_with_weather(week: int) -> list:
    """Get all upcoming games with weather data."""
    games = await fetch_week_games(2025, week)
    results = []

    for game in games:
        comp = game["competitions"][0]
        status = comp["status"]["type"]

        if status["state"] == "pre":  # Future game
            game_id = game["id"]
            summary = await fetch_summary(game_id)
            weather = summary.get("gameInfo", {}).get("weather")

            results.append({
                "game": game["shortName"],
                "date": game["date"],
                "weather": weather
            })

    return results
```

### 3. Complete Game Data Extraction
```python
def extract_game_data(game: dict, summary: dict = None) -> dict:
    comp = game["competitions"][0]
    venue = comp["venue"]
    status = comp["status"]["type"]

    teams = {}
    for competitor in comp["competitors"]:
        abbr = competitor["team"]["abbreviation"]
        linescores = competitor.get("linescores") or []

        teams[abbr] = {
            "score": int(competitor["score"]),
            "home_away": competitor["homeAway"],
            "winner": competitor["winner"],
            "quarters": [int(q["value"]) for q in linescores],
            "records": competitor.get("records", [])
        }

    is_international = venue.get("address", {}).get("country", "USA") != "USA"
    is_overtime = any(len(t["quarters"]) > 4 for t in teams.values())
    is_future = status.get("state") == "pre"

    result = {
        "game_id": game["id"],
        "date": game["date"],
        "venue": venue.get("fullName"),
        "city": venue.get("address", {}).get("city"),
        "country": venue.get("address", {}).get("country"),
        "indoor": venue.get("indoor"),
        "international": is_international,
        "overtime": is_overtime,
        "completed": status.get("completed", False),
        "status": status.get("detail"),
        "attendance": comp.get("attendance"),
        "teams": teams
    }

    # Add future game data
    if is_future and summary:
        result["weather"] = summary.get("gameInfo", {}).get("weather")
        result["predictor"] = summary.get("predictor")

    # Add odds from scoreboard
    odds = comp.get("odds", [])
    if odds:
        result["odds"] = odds[0]

    return result
```

---

## Limitations and Caveats

### 1. Weather Data
- **Available for future games only** (~1 week before game)
- **NOT available for completed games**
- Source is AccuWeather via ESPN

### 2. Venue Capacity
- **NOT available** in the API
- Must use external data source

### 3. Indoor Field
- **ONLY** in scoreboard endpoint
- NOT in summary endpoint (use `grass` field there instead)

### 4. Odds/Predictor
- Only populated for future/scheduled games
- Empty/null for completed games

### 5. Score Types
- `score` is a STRING ("23"), not integer
- `linescores[].value` is a FLOAT (7.0), not integer

### 6. API Stability
- ESPN API is **unofficial and undocumented**
- Response structures may change without notice
- Rate limiting exists (recommend 0.2-0.5s delays)

### 7. Historical Data
- Historical seasons are available
- Weather is NEVER available for historical games

---

## Verification

This report was verified through three rounds of comprehensive testing:

**Round 1**: Initial research
**Round 2**: Field-by-field verification, corrections documented
**Round 3**: Complete re-verification with weather for future games discovery

All test scripts are available in: `docs/research/`
- `comprehensive_verification_v3.py` - Round 3 verification suite
- `weather_deep_dive.py` - Weather availability testing
- `verification_test.py` - Round 2 verification suite
- `verification_deep_dive.py` - Edge case testing

---

## Changelog

- **v3 (2025-11-25)**: Major weather correction
  - **MAJOR**: Weather IS available for future games (not completed)
  - Added predictor field documentation for future games
  - Added odds availability for future games in scoreboard
  - Added weather field structure and types
  - Added weather availability by game proximity
  - Verified 43 claims from v2 remain accurate
  - Added implementation examples for weather fetching

- **v2 (2025-11-25)**: Complete re-verification with corrections
  - Corrected score field type (string, not int)
  - Added overtime game handling
  - Added scheduled game field differences
  - Corrected indoor field location (scoreboard only)
  - Added bye week detection
  - Added provider/leagues top-level fields
  - Confirmed venue capacity unavailability

- **v1 (2025-11-25)**: Initial research report
