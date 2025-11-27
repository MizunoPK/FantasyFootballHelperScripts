# Game Data Scoring Parameters Research

This document analyzes the new `game_data.csv` data and proposes potential scoring parameters that could be integrated into the fantasy football scoring system.

## Data Summary

### Game Data Available

| Column | Description | 2024 Data Coverage |
|--------|-------------|-------------------|
| `week` | NFL week (1-18) | 272 games |
| `home_team` | Home team abbreviation | 100% |
| `away_team` | Away team abbreviation | 100% |
| `temperature` | Game-time temperature (°F) | 100% outdoor games |
| `gust` | Wind gusts (mph) | 100% outdoor games |
| `precipitation` | Hourly precipitation (inches) | 100% outdoor games |
| `home_team_score` | Final home score | 100% |
| `away_team_score` | Final away score | 100% |
| `indoor` | Stadium is indoor | 100% |
| `neutral_site` | Game at neutral site | 100% |
| `country` | Game country | 100% |
| `city` | Game city | 100% |
| `state` | Game state (USA only) | 100% |
| `date` | ISO 8601 game datetime | 100% |

### Stadium Distribution (2024)

- **Indoor games**: 94 (35%)
- **Outdoor games**: 178 (65%)
- **International games**: 5 (London: 3, Munich: 1, Sao Paulo: 1)

---

## Proposed New Scoring Parameters

### 1. Weather Multiplier (Outdoor Games Only)

**Concept**: Adjust player scores based on weather conditions that historically impact performance.

#### Temperature Impact

| Category | Range | Games (2024) | Avg Total Score | Proposed Effect |
|----------|-------|--------------|-----------------|-----------------|
| Freezing | < 32°F | 18 | 45.7 | Slight negative for passing, positive for rushing |
| Cold | 32-50°F | 34 | - | Slight negative |
| Moderate | 50-70°F | 76 | - | Neutral (baseline) |
| Warm | 70-90°F | 49 | - | Neutral |
| Hot | 90+°F | 1 | 37.4 | Negative (fatigue) |

**Key Observations**:
- Hot games (85°F+) averaged only 37.4 total points vs 45.8 overall
- Cold games show relatively normal scoring
- Temperature extremes affect passing efficiency more than rushing

**Position-Specific Recommendations**:
- **QB/WR/TE**: Slight penalty in extreme cold (<40°F) and extreme heat (85°F+)
- **RB**: Slight bonus in cold weather (game scripts favor running)
- **K**: Penalty in extreme cold (kicking mechanics affected)

#### Wind Impact

| Category | Gust Range | Games (2024) | Avg Total Score | Proposed Effect |
|----------|------------|--------------|-----------------|-----------------|
| Calm | 0-10 mph | 35 | - | Neutral |
| Moderate | 10-20 mph | 91 | - | Neutral |
| Windy | 20-30 mph | 42 | - | Negative for passing/kicking |
| Severe | 30+ mph | 10 | 44.1 | Strong negative for passing/kicking |

**Position-Specific Recommendations**:
- **QB/WR/TE**: Penalty in windy conditions (25+ mph gusts)
- **RB**: Bonus in windy conditions (game script adjustment)
- **K**: Strong penalty in windy conditions (field goal accuracy)
- **DST**: Slight bonus (turnovers increase in bad conditions)

#### Precipitation Impact

| Category | Amount | Games (2024) | Avg Total Score |
|----------|--------|--------------|-----------------|
| Dry | 0.0" | 164 | 45.0 |
| Light | 0.01-0.10" | 12 | - |
| Moderate | 0.10-0.25" | 2 | 48.0 |
| Heavy | 0.25+" | 0 | - |

**Note**: Only 14 games had precipitation in 2024. Sample size too small for definitive conclusions, but rain historically affects:
- Ball handling (fumble risk increases)
- Passing accuracy (grip issues)
- Kicking (wet ball)

---

### 2. Indoor/Outdoor Multiplier

**Concept**: Players in indoor stadiums have more consistent conditions.

| Environment | Games | Avg Total Score | Home Win % |
|-------------|-------|-----------------|------------|
| Indoor | 94 | 47.1 | 54.3% |
| Outdoor | 178 | 45.1 | 52.8% |

**Proposed Implementation**:
- **Indoor**: Slight bonus for passing-focused players (consistent conditions)
- **Outdoor**: No adjustment (baseline)

**Position-Specific Recommendations**:
- **QB/WR**: 1-2% boost for games in domed stadiums
- **K**: Slight boost for indoor games (no wind/weather)

---

### 3. Home Field Advantage Multiplier

**Concept**: Home teams have measurable advantages.

| Scenario | Games | Home Win % | Avg Home Point Diff |
|----------|-------|------------|---------------------|
| All Games | 272 | 53.3% | +1.9 |
| Indoor | 94 | 54.3% | - |
| Outdoor | 178 | 52.8% | - |
| Neutral Site | 5 | 100%* | - |

*Small sample size - international games in 2024 all went to designated home team.

**Proposed Implementation**:
- **Home players**: Slight scoring boost (1-3%)
- **Away players**: Slight scoring penalty (1-3%)

This could be integrated into the existing Team Quality or Matchup multipliers.

---

### 4. Travel/Timezone Penalty

**Concept**: Teams traveling across time zones may be disadvantaged.

**Data Available**:
- Game city/state/country
- Team home locations (from coordinates.json)
- Could calculate travel distance and timezone changes

**Proposed Implementation**:
- **0-1 timezone change**: No penalty
- **2 timezone change**: Slight penalty (e.g., East Coast to West Coast)
- **3+ timezone change** (international): Moderate penalty

**Affected Scenarios**:
- East coast team playing 4pm ET game on West coast
- West coast team playing 1pm ET game on East coast
- All teams playing international games

---

### 5. Neutral Site Penalty

**Concept**: Neutral site games remove home field advantage for both teams.

**2024 Data**: 5 neutral site games (all international)

**Proposed Implementation**:
- Both teams receive neutral treatment (no home/away bonus)
- Could combine with travel penalty for international games

---

### 6. Game Script Prediction

**Concept**: Use pre-game factors to predict game script, affecting position values.

**Available Data for Prediction**:
- Vegas spreads (would need to add)
- Team offensive/defensive rankings (already available)
- Historical team scoring (from game_data.csv)

**Game Script Impact**:
- **Blowout (team favored by 10+)**: RBs on favored team benefit (running out clock)
- **Close game**: Pass catchers more valuable (need to score quickly)
- **Heavy underdog**: WRs/TEs benefit (garbage time)

---

## Implementation Recommendations

### Phase 1: Weather Multiplier (Highest Impact)

Add new scoring step for weather conditions:

```json
{
  "WEATHER_SCORING": {
    "ENABLED": true,
    "TEMPERATURE": {
      "COLD_THRESHOLD": 40,
      "HOT_THRESHOLD": 85,
      "COLD_PENALTY": { "QB": 0.97, "WR": 0.98, "TE": 0.98, "K": 0.95 },
      "HOT_PENALTY": { "QB": 0.98, "WR": 0.98, "TE": 0.98, "RB": 0.99 },
      "COLD_BONUS": { "RB": 1.02 }
    },
    "WIND": {
      "MODERATE_THRESHOLD": 20,
      "SEVERE_THRESHOLD": 30,
      "MODERATE_PENALTY": { "QB": 0.98, "WR": 0.98, "K": 0.95 },
      "SEVERE_PENALTY": { "QB": 0.95, "WR": 0.95, "K": 0.90 },
      "WIND_BONUS": { "RB": 1.03, "DST": 1.02 }
    },
    "INDOOR_BONUS": { "QB": 1.02, "WR": 1.01, "K": 1.02 }
  }
}
```

### Phase 2: Travel/Timezone Penalty

Add travel calculations:

```json
{
  "TRAVEL_SCORING": {
    "ENABLED": true,
    "TIMEZONE_PENALTY": {
      "2_ZONES": 0.99,
      "3_PLUS_ZONES": 0.97
    },
    "INTERNATIONAL_PENALTY": 0.96
  }
}
```

### Phase 3: Home Field Advantage

Integrate into existing system:

```json
{
  "HOME_FIELD_SCORING": {
    "ENABLED": true,
    "HOME_BONUS": 1.02,
    "AWAY_PENALTY": 0.98,
    "NEUTRAL_SITE": 1.0
  }
}
```

---

## Data Requirements for Implementation

### Current Data (game_data.csv)
- Temperature, wind, precipitation
- Indoor/outdoor stadium
- Neutral site flag
- International location

### Additional Data Needed
- **Vegas spreads**: For game script prediction
- **Team travel schedules**: For precise travel calculations
- **Historical weather performance**: For validation of weather impacts

---

## Mode Usage Recommendations

| Parameter | Add To Roster | Starter Helper | Trade Simulator |
|-----------|---------------|----------------|-----------------|
| Weather | Seasonal avg | Current week | Seasonal avg |
| Indoor/Outdoor | Home stadium | Game venue | Home stadium |
| Home/Away | N/A (draft) | Current week | N/A (avg) |
| Travel | N/A | Current week | N/A |
| Game Script | N/A | Current week | N/A |

---

## Validation Approach

1. **Historical Analysis**: Apply proposed multipliers to 2024 data, validate against actual fantasy scoring
2. **Position-Specific Correlation**: Measure correlation between weather and fantasy output by position
3. **A/B Testing**: Run simulations with/without weather multipliers

---

## Priority Ranking

| Parameter | Priority | Complexity | Expected Impact |
|-----------|----------|------------|-----------------|
| Weather (Wind) | High | Low | High for K, moderate for pass game |
| Indoor Bonus | Medium | Low | Low-moderate |
| Weather (Temp) | Medium | Low | Low-moderate |
| Home Field | Low | Medium | Low |
| Travel/Timezone | Low | High | Unknown |
| Game Script | Future | High | Potentially high |

---

## Appendix: 2024 Weather Extremes

### Coldest Games
- Week 17-18: Multiple games below 20°F
- Min temperature: 10°F

### Windiest Games
- Max gusts: 41 mph (BUF vs ARI, Week 1)
- 10 games with 30+ mph gusts

### Hottest Games
- Week 1-3: Multiple 85°F+ games
- Max temperature: 103°F

### International Games
| Week | Teams | Location | Weather |
|------|-------|----------|---------|
| 1 | PHI vs GB | Sao Paulo, Brazil | 76°F, 8 mph |
| 5 | MIN vs NYJ | London, England | Available |
| 6 | CHI vs JAX | London, England | Available |
| 7 | JAX vs NE | London, England | Available |
| 10 | CAR vs NYG | Munich, Germany | Available |
