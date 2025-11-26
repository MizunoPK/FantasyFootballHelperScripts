# ESPN API - Predictive Fields for Player Performance

**Research Date**: November 25, 2025
**Purpose**: Identify all ESPN API fields useful for predicting fantasy football player performance

---

## Executive Summary

This report documents all fields available from the ESPN API that could be useful for predicting player performance in upcoming NFL games. Data is available for **future/scheduled games** (status.state = "pre") that is not available for completed games.

**Key Categories**:
1. Weather data (temperature, wind, precipitation)
2. Vegas/betting lines (spread, over/under, moneyline)
3. Win probability predictions
4. Team season statistics (offense and defense)
5. Last 5 games performance
6. Injury reports
7. Venue factors (indoor, grass, international)
8. Team leaders and recent form

---

## 1. Weather Data

### Availability
- **Scoreboard endpoint**: `game.weather` (game-level)
- **Summary endpoint**: `gameInfo.weather`
- **Timing**: Available ~1 week before game

### CORRECTION: Weather in Scoreboard
Weather is available at the **game level** in the scoreboard endpoint (not just summary):

```python
# Scoreboard endpoint - game.weather
weather = game.get("weather")
```

### Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `displayValue` | str | Text description of conditions | "Flurries", "Partly Cloudy" |
| `temperature` | int | Temperature in °F | 37 |
| `highTemperature` | int | Predicted high °F | 37 |
| `lowTemperature` | int | Predicted low °F (summary only) | 37 |
| `conditionId` | str | AccuWeather condition code | "19" |
| `gust` | int | Wind gust speed (mph) - summary only | 39 |
| `precipitation` | int | Precipitation chance (%) - summary only | 55 |
| `link.href` | str | AccuWeather forecast URL | "http://www.accuweather.com/..." |

### Predictive Use Cases

| Factor | Impact | Affected Positions |
|--------|--------|-------------------|
| Temperature < 32°F | Reduced grip, accuracy | QB, WR, K |
| Wind gust > 15 mph | Fewer deep passes, shorter FG range | QB, WR, K |
| Precipitation > 50% | Run-heavy game scripts | RB +, WR/QB - |
| Condition "Flurries/Rain" | Ball security issues | All skill positions |

### Example Code
```python
async def get_weather_factors(game: dict, summary: dict) -> dict:
    # Scoreboard has basic weather
    sb_weather = game.get("weather", {})

    # Summary has more details
    sum_weather = summary.get("gameInfo", {}).get("weather", {})

    return {
        "condition": sb_weather.get("displayValue"),  # "Flurries"
        "temperature": sb_weather.get("temperature"),  # 37
        "wind_gust": sum_weather.get("gust"),          # 39
        "precipitation_pct": sum_weather.get("precipitation"),  # 55
    }
```

---

## 2. Betting Lines / Vegas Odds

### Location
- **Scoreboard**: `competition.odds[0]`

### Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `details` | str | Spread summary | "DET -2.5" |
| `spread` | float | Point spread (negative = favorite) | -2.5 |
| `overUnder` | float | Total points line | 48.5 |
| `homeTeamOdds.favorite` | bool | Is home team favored | true |
| `homeTeamOdds.moneyLine` | int | Home team ML | -140 |
| `homeTeamOdds.spreadOdds` | float | Spread juice | -115.0 |
| `awayTeamOdds.favorite` | bool | Is away team favored | false |
| `awayTeamOdds.moneyLine` | int | Away team ML | 120 |
| `awayTeamOdds.spreadOdds` | float | Spread juice | -105.0 |

### Line Movement (Open vs Close)

```python
odds = competition["odds"][0]

# Point spread movement
spread_open = odds["pointSpread"]["home"]["open"]["line"]   # "-3"
spread_close = odds["pointSpread"]["home"]["close"]["line"] # "-2.5"

# Total movement
total_open = odds["total"]["over"]["open"]["line"]   # "o49.5"
total_close = odds["total"]["over"]["close"]["line"] # "o48.5"

# Moneyline movement
ml_open = odds["moneyline"]["home"]["open"]["odds"]   # "-150"
ml_close = odds["moneyline"]["home"]["close"]["odds"] # "-140"
```

### Predictive Use Cases

| Factor | Interpretation | Fantasy Impact |
|--------|----------------|----------------|
| High O/U (> 50) | Expected shootout | More fantasy points available |
| Low O/U (< 40) | Defensive battle | Lower ceilings for skill players |
| Large spread (> 7) | Potential blowout | Garbage time for losing team |
| Line moving toward team | Sharp money on that side | Confidence indicator |
| Heavy favorite at home | Likely to run out clock | RB boost late game |

### Example Code
```python
def get_game_script_indicators(odds: dict) -> dict:
    return {
        "spread": odds.get("spread"),
        "over_under": odds.get("overUnder"),
        "home_favorite": odds.get("homeTeamOdds", {}).get("favorite"),
        "implied_total_home": (odds.get("overUnder", 0) / 2) - (odds.get("spread", 0) / 2),
        "implied_total_away": (odds.get("overUnder", 0) / 2) + (odds.get("spread", 0) / 2),
    }
```

---

## 3. Win Probability (Predictor)

### Location
- **Summary**: `predictor`

### Fields

```json
{
    "header": "Matchup Predictor",
    "homeTeam": {
        "id": "8",
        "gameProjection": "54",      // Win probability %
        "teamChanceLoss": "45.6"     // Loss probability %
    },
    "awayTeam": {
        "id": "9",
        "gameProjection": "45.6",
        "teamChanceLoss": "54"
    }
}
```

### Predictive Use Cases

| Win Probability | Interpretation |
|-----------------|----------------|
| > 65% | Strong favorite, may rest starters if ahead |
| 45-55% | Toss-up game, full effort expected |
| < 35% | Underdog, may abandon run game if behind |

---

## 4. Team Season Statistics

### Location
- **Summary**: `boxscore.teams[].statistics[]`

### Available Statistics (Per Game Averages)

| Stat Name | Description | Fantasy Use |
|-----------|-------------|-------------|
| `totalPointsPerGame` | Points scored per game | Overall offense strength |
| `yardsPerGame` | Total yards per game | Volume indicator |
| `passingYardsPerGame` | Pass yards per game | Pass-heavy vs run-heavy |
| `rushingYardsPerGame` | Rush yards per game | Run game strength |
| `totalPointsPerGameAllowed` | Points allowed per game | Defense strength |
| `yardsPerGameAllowed` | Total yards allowed | Defense quality |
| `passingYardsPerGameAllowed` | Pass yards allowed | Pass defense (target WRs) |
| `rushingYardsPerGameAllowed` | Rush yards allowed | Run defense (target RBs) |

### Example Data
```json
{
    "team": {"abbreviation": "DET"},
    "statistics": [
        {"name": "totalPointsPerGame", "displayValue": "29.6"},
        {"name": "yardsPerGame", "displayValue": "391.8"},
        {"name": "passingYardsPerGame", "displayValue": "252.0"},
        {"name": "rushingYardsPerGame", "displayValue": "139.8"},
        {"name": "totalPointsPerGameAllowed", "displayValue": "22.1"},
        {"name": "yardsPerGameAllowed", "displayValue": "330.8"},
        {"name": "passingYardsPerGameAllowed", "displayValue": "229.1"},
        {"name": "rushingYardsPerGameAllowed", "displayValue": "101.7"}
    ]
}
```

### Predictive Use Cases

| Matchup | Indicator | Target |
|---------|-----------|--------|
| High pass yards allowed | Weak secondary | WRs, pass-catching RBs |
| High rush yards allowed | Weak front 7 | RBs |
| High points per game | Explosive offense | Stack with opposing pass catchers |
| Low points allowed | Strong defense | Fade offensive players |

---

## 5. Last 5 Games Performance

### Location
- **Summary**: `lastFiveGames[]`

### Fields

Each team entry contains an `events[]` array with recent games:

| Field | Type | Description |
|-------|------|-------------|
| `week` | int | NFL week number |
| `atVs` | str | "@" for away, "vs" for home |
| `score` | str | Final score (e.g., "34-27 OT") |
| `gameResult` | str | "W" or "L" |
| `homeTeamScore` | str | Home team points |
| `awayTeamScore` | str | Away team points |
| `opponent.abbreviation` | str | Opponent team |

### Predictive Use Cases

- **Recent form**: W-L record in last 5
- **Scoring trends**: Points scored/allowed trending up or down
- **Home/away splits**: Performance difference by venue
- **Strength of schedule**: Quality of recent opponents

---

## 6. Injury Reports

### Location
- **Summary**: `injuries[]`

### Fields

```json
{
    "team": {"abbreviation": "DET"},
    "injuries": [
        {
            "status": "Questionable",
            "date": "2025-11-25T13:16Z",
            "athlete": {
                "id": "4360383",
                "fullName": "Kerby Joseph",
                "displayName": "Kerby Joseph",
                "position": {
                    "name": "Safety",
                    "displayName": "Safety",
                    "abbreviation": "S"
                }
            },
            "type": {
                "id": "...",
                "name": "INJURY_STATUS_QUESTIONABLE",
                "description": "questionable",
                "abbreviation": "Q"
            }
        }
    ]
}
```

### Injury Statuses

| Status | Abbreviation | Fantasy Impact |
|--------|--------------|----------------|
| Out | O | Player will not play |
| Doubtful | D | Unlikely to play (~25%) |
| Questionable | Q | May or may not play (~50%) |
| Probable | P | Likely to play (~75%) |
| Active | A | Healthy, will play |
| Injured Reserve | IR | Out for extended period |

### Predictive Use Cases

- **Skill position injuries**: Opportunity for backups
- **O-line injuries**: Reduced protection, more sacks
- **Defensive injuries**: Exploit weak positions
- **Key player status**: QB, RB1, WR1 status critical

---

## 7. Venue Factors

### Location
- **Scoreboard**: `competition.venue`
- **Summary**: `gameInfo.venue`

### Fields

| Field | Location | Type | Description |
|-------|----------|------|-------------|
| `indoor` | Scoreboard only | bool | Dome/indoor stadium |
| `grass` | Summary only | bool | Natural grass vs turf |
| `address.country` | Both | str | Country (for international) |
| `address.city` | Both | str | City name |
| `address.state` | Both | str | State (USA only) |
| `fullName` | Both | str | Stadium name |

### Special Venue Fields

| Field | Location | Description |
|-------|----------|-------------|
| `neutralSite` | Scoreboard | True for international/Super Bowl |
| `notes[].headline` | Scoreboard | Special designation ("NFL London Games") |

### Predictive Use Cases

| Factor | Impact |
|--------|--------|
| Indoor | No weather impact, consistent conditions |
| Outdoor cold | Affects passing game |
| Grass vs turf | Speed players prefer turf |
| International | Travel fatigue, neutral crowd |
| High altitude (Denver) | Longer kicks, visitor fatigue |

---

## 8. Team Leaders

### Location
- **Scoreboard**: `competition.leaders[]` (game-level)
- **Scoreboard**: `competitor.leaders[]` (team-level)
- **Summary**: `leaders[]`

### Categories

| Category | Field Name | Description |
|----------|------------|-------------|
| Passing | `passingYards` / `passingLeader` | Season passing leader |
| Rushing | `rushingYards` / `rushingLeader` | Season rushing leader |
| Receiving | `receivingYards` / `receivingLeader` | Season receiving leader |

### Leader Data

```json
{
    "name": "passingLeader",
    "displayName": "Passing Leader",
    "leaders": [{
        "displayValue": "244/352, 2769 YDS, 23 TD, 5 INT",
        "value": 2769.0,
        "athlete": {
            "id": "3046779",
            "fullName": "Jared Goff",
            "position": {"abbreviation": "QB"},
            "injuries": {
                "status": "Active"
            }
        }
    }]
}
```

### Predictive Use Cases

- **Volume indicators**: YDS, ATT, TGT show usage
- **Efficiency**: TD/INT ratio, YPC, etc.
- **Injury status**: Leader's current health

---

## 9. Records and Standings

### Location
- **Scoreboard**: `competitor.records[]`

### Record Types

| Type | Name | Example |
|------|------|---------|
| `total` | Overall | "7-4" |
| `home` | Home | "4-1" |
| `road` | Road | "3-3" |

### Predictive Use Cases

- **Home/away splits**: Some teams much better at home
- **Win-loss momentum**: Winning teams play with confidence

---

## 10. Game Timing/Schedule

### Location
- **Scoreboard**: `game.date`, `status.type.detail`

### Fields

| Field | Type | Example |
|-------|------|---------|
| `date` | str (ISO 8601) | "2025-11-27T18:00Z" |
| `status.type.detail` | str | "Thu, November 27th at 1:00 PM EST" |
| `broadcast` | str | "FOX" |

### Predictive Use Cases

| Scenario | Impact |
|----------|--------|
| Thursday game | Short week (3 days rest) |
| Monday game | Extra rest for one team |
| Early Sunday (1pm) | Standard preparation |
| Late Sunday/SNF | More rest, national spotlight |
| International | Long travel, time zone issues |

---

## Complete Data Extraction Example

```python
async def get_all_predictive_factors(game_id: str, scoreboard_game: dict) -> dict:
    """Extract all predictive factors for a future game."""
    comp = scoreboard_game["competitions"][0]

    # Get summary for additional data
    summary = await fetch_summary(game_id)

    # Weather
    sb_weather = scoreboard_game.get("weather", {})
    sum_weather = summary.get("gameInfo", {}).get("weather", {})

    # Odds
    odds = comp.get("odds", [{}])[0] if comp.get("odds") else {}

    # Teams
    home_team = next(c for c in comp["competitors"] if c["homeAway"] == "home")
    away_team = next(c for c in comp["competitors"] if c["homeAway"] == "away")

    # Team stats from boxscore
    boxscore_teams = {
        t["team"]["abbreviation"]: t["statistics"]
        for t in summary.get("boxscore", {}).get("teams", [])
    }

    return {
        # Basic info
        "game_id": game_id,
        "date": scoreboard_game.get("date"),
        "home_team": home_team["team"]["abbreviation"],
        "away_team": away_team["team"]["abbreviation"],

        # Weather
        "weather": {
            "condition": sb_weather.get("displayValue"),
            "temperature": sb_weather.get("temperature"),
            "wind_gust": sum_weather.get("gust"),
            "precipitation_pct": sum_weather.get("precipitation"),
        },

        # Venue
        "venue": {
            "name": comp["venue"].get("fullName"),
            "indoor": comp["venue"].get("indoor"),
            "grass": summary.get("gameInfo", {}).get("venue", {}).get("grass"),
            "country": comp["venue"].get("address", {}).get("country"),
            "international": comp["venue"].get("address", {}).get("country") != "USA",
            "neutral_site": comp.get("neutralSite", False),
        },

        # Betting
        "betting": {
            "spread": odds.get("spread"),
            "over_under": odds.get("overUnder"),
            "home_moneyline": odds.get("homeTeamOdds", {}).get("moneyLine"),
            "away_moneyline": odds.get("awayTeamOdds", {}).get("moneyLine"),
            "home_favorite": odds.get("homeTeamOdds", {}).get("favorite"),
        },

        # Win probability
        "predictor": summary.get("predictor"),

        # Team stats
        "team_stats": boxscore_teams,

        # Records
        "home_record": home_team.get("records", [{}])[0].get("summary"),
        "away_record": away_team.get("records", [{}])[0].get("summary"),

        # Injuries
        "injuries": summary.get("injuries", []),

        # Last 5 games
        "last_five": summary.get("lastFiveGames", []),
    }
```

---

## Data Availability Summary

| Data | Scoreboard | Summary | Future Games | Completed |
|------|------------|---------|--------------|-----------|
| Weather | YES (game level) | YES | YES | NO |
| Odds | YES | NO | YES | Empty |
| Predictor | NO | YES | YES | null |
| Team Stats | NO | YES | YES | YES |
| Last 5 Games | NO | YES | YES | YES |
| Injuries | NO | YES | YES | YES |
| Indoor | YES | NO | YES | YES |
| Grass | NO | YES | YES | YES |
| Records | YES | NO | YES | YES |
| Leaders | YES | YES | YES | YES |

---

## Corrections from Previous Report

1. **Weather in Scoreboard**: Weather IS available at the game level in scoreboard (`game.weather`), not just in summary. It includes `displayValue` with text description.

2. **Weather fields differ**: Scoreboard weather has `displayValue`, summary has `gust`, `precipitation`, `lowTemperature`.

3. **Team Statistics**: Full team season statistics are available in `boxscore.teams[].statistics[]` for future games.

4. **Last Five Games**: Detailed recent game history is available in `lastFiveGames[]`.

5. **Line Movement**: Opening and closing lines are available for spread, total, and moneyline.

---

## Recommendations

### High-Value Predictive Factors

1. **Weather** (for outdoor games): Temperature, wind, precipitation
2. **Over/Under**: Best single predictor of total fantasy points available
3. **Spread**: Indicates likely game script
4. **Team defensive stats**: Identify weak defenses to target
5. **Injuries**: Critical for opportunity changes

### Implementation Priority

1. Fetch weather for all outdoor games ~1 week out
2. Track line movement (opening vs current)
3. Build matchup rankings from team stats
4. Monitor injury reports daily
5. Consider venue factors (dome, international, altitude)
