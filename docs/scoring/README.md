# Fantasy Football Scoring Algorithm V2

This documentation provides a comprehensive analysis of the 13-step scoring algorithm used by the League Helper system.

## Table of Contents

1. [01_normalization.md](01_normalization.md) - Fantasy Points Normalization (Step 1)
2. [02_adp_multiplier.md](02_adp_multiplier.md) - Average Draft Position Multiplier (Step 2)
3. [03_player_rating_multiplier.md](03_player_rating_multiplier.md) - Expert Consensus Rating Multiplier (Step 3)
4. [04_team_quality_multiplier.md](04_team_quality_multiplier.md) - Team Offensive/Defensive Strength (Step 4)
5. [05_performance_multiplier.md](05_performance_multiplier.md) - Actual vs Projected Deviation (Step 5)
6. [06_matchup_multiplier.md](06_matchup_multiplier.md) - Current Opponent Strength (Step 6)
7. [07_schedule_multiplier.md](07_schedule_multiplier.md) - Future Opponents Strength (Step 7)
8. [08_draft_order_bonus.md](08_draft_order_bonus.md) - Position-Specific Draft Value (Step 8)
9. [09_bye_week_penalty.md](09_bye_week_penalty.md) - Roster Conflict Penalty (Step 9)
10. [10_injury_penalty.md](10_injury_penalty.md) - Injury Risk Assessment (Step 10)
11. [11_temperature_scoring.md](11_temperature_scoring.md) - Weather Temperature Adjustment (Step 11)
12. [12_wind_scoring.md](12_wind_scoring.md) - Wind Conditions Adjustment (Step 12)
13. [13_location_scoring.md](13_location_scoring.md) - Home/Away/International Adjustment (Step 13)

---

## Algorithm Overview

The scoring algorithm evaluates fantasy football players using a 13-step calculation that combines:
- **Multipliers** (Steps 2-5): Proportionally adjust base score
- **Additive Bonuses/Penalties** (Steps 6-13): Add or subtract fixed points
- **Game Conditions** (Steps 11-13): Weather and location adjustments

### Scoring Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     STEP 1: NORMALIZATION                           │
│  fantasy_points → normalized score (0 to ~135 scale)                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                   MULTIPLICATIVE ADJUSTMENTS                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Step 2    │  │   Step 3    │  │   Step 4    │  │   Step 5    │ │
│  │     ADP     │→ │   Player    │→ │    Team     │→ │ Performance │ │
│  │  Multiplier │  │   Rating    │  │   Quality   │  │  Multiplier │ │
│  │ (×0.87-1.15)│  │ (×0.96-1.04)│  │ (×0.91-1.09)│  │ (×0.87-1.14)│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                    ADDITIVE ADJUSTMENTS                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│  │   Step 6    │  │   Step 7    │  │   Step 8    │                  │
│  │   Matchup   │→ │  Schedule   │→ │ Draft Order │                  │
│  │   Bonus     │  │   Bonus     │  │   Bonus     │                  │
│  │ (±4.6 pts)  │  │ (±4.3 pts)  │  │ (+0-80 pts) │                  │
│  └─────────────┘  └─────────────┘  └─────────────┘                  │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐                                   │
│  │   Step 9    │  │   Step 10   │                                   │
│  │  Bye Week   │→ │   Injury    │                                   │
│  │   Penalty   │  │   Penalty   │                                   │
│  │  (-0-50 pts)│  │ (-0-100 pts)│                                   │
│  └─────────────┘  └─────────────┘                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                 GAME CONDITION ADJUSTMENTS (Weekly)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│  │   Step 11   │  │   Step 12   │  │   Step 13   │                  │
│  │ Temperature │→ │    Wind     │→ │  Location   │  → FINAL SCORE  │
│  │   Bonus     │  │   Bonus     │  │   Bonus     │                  │
│  │ (±2.5 pts)  │  │ (±3.0 pts)  │  │ (+2/-2/-5)  │                  │
│  └─────────────┘  └─────────────┘  └─────────────┘                  │
│  (All positions)  (QB/WR/K only)  (All positions)                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Score Formula

```python
final_score = (
    normalized_projection
    * adp_multiplier^ADP_WEIGHT
    * rating_multiplier^RATING_WEIGHT
    * team_quality_multiplier^TQ_WEIGHT
    * performance_multiplier^PERF_WEIGHT
    + matchup_bonus
    + schedule_bonus
    + draft_order_bonus
    - bye_week_penalty
    - injury_penalty
    + temperature_bonus      # Step 11 (game conditions)
    + wind_bonus             # Step 12 (game conditions, QB/WR/K only)
    + location_modifier      # Step 13 (game conditions)
)
```

---

## Mode Usage Comparison

Each League Helper mode uses different scoring flags based on its purpose:

| Step | Metric | Add To Roster | Starter Helper | Trade Sim (User) | Trade Sim (Opp) |
|------|--------|---------------|----------------|------------------|-----------------|
| 1 | Normalization | ROS | Weekly | ROS | ROS |
| 2 | ADP Multiplier | ✅ | ❌ | ❌ | ❌ |
| 3 | Player Rating | ✅ | ❌ | ✅ | ✅ |
| 4 | Team Quality | ✅ | ✅ | ✅ | ✅ |
| 5 | Performance | ❌ | ✅ | ✅ | ✅ |
| 6 | Matchup | ❌ | ✅ | ❌ | ❌ |
| 7 | Schedule | ❌ | ❌ | ✅ | ✅ |
| 8 | Draft Order | ✅ (round-based) | ❌ | ❌ | ❌ |
| 9 | Bye Week | ✅ | ❌ | ✅ | ❌ |
| 10 | Injury | ✅ | ❌ | ❌ | ❌ |
| 11 | Temperature | ❌ | ✅ | ❌ | ❌ |
| 12 | Wind | ❌ | ✅ | ❌ | ❌ |
| 13 | Location | ❌ | ✅ | ❌ | ❌ |

### Mode Descriptions

**Add To Roster Mode** (Draft Helper)
- Purpose: Evaluate available players for draft selection
- Focus: Season-long value with market positioning (ADP) and draft strategy
- Uses ROS projections with bye week conflicts considered

**Starter Helper Mode** (Roster Optimizer)
- Purpose: Optimize weekly starting lineup
- Focus: Current week performance and matchup
- Uses weekly projections with performance trends

**Trade Simulator Mode - User Team**
- Purpose: Evaluate pre/post-trade roster impact
- Focus: Season-long value with roster fit
- Uses ROS projections with bye penalties

**Trade Simulator Mode - Opponent**
- Purpose: Evaluate opponent's post-trade value
- Focus: Fair comparison without roster context
- Uses ROS projections without bye penalties

---

## Data Sources

### Primary Data Files

| File | Description | Used By |
|------|-------------|---------|
| `data/players.csv` | Player stats, projections, ADP, ratings | Steps 1-3, 8-10 |
| `data/players_projected.csv` | Pre-season projections | Step 5 (baseline) |
| `data/team_data/{TEAM}.csv` | Weekly team performance | Steps 4, 6, 7 |
| `data/season_schedule.csv` | NFL schedule | Steps 6, 7 |
| `data/game_data.csv` | Game conditions (temp, wind, location) | Steps 11-13 |
| `data/league_config.json` | Scoring configuration | All steps |

### Key Implementation Files

| File | Purpose |
|------|---------|
| `league_helper/util/player_scoring.py` | Main 13-step algorithm |
| `league_helper/util/ConfigManager.py` | Multiplier/penalty calculations |
| `league_helper/util/TeamDataManager.py` | Team rankings (rolling windows) |
| `league_helper/util/SeasonScheduleManager.py` | Schedule data |
| `league_helper/util/ProjectedPointsManager.py` | Pre-season projections |
| `league_helper/util/GameDataManager.py` | Game conditions (temp, wind, location) |
| `player-data-fetcher/espn_client.py` | ESPN API data extraction |
| `player-data-fetcher/game_data_fetcher.py` | Game conditions data fetcher |

---

## Configuration Structure

All scoring parameters are defined in `data/league_config.json` with a consistent threshold system:

```json
{
  "METRIC_SCORING": {
    "THRESHOLDS": {
      "BASE_POSITION": 0,      // Center point for ratings
      "DIRECTION": "INCREASING", // How values map to ratings
      "STEPS": 20              // Size of each rating band
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 1.0              // Exponent applied to multiplier
  }
}
```

### Rating Thresholds

Each metric maps input values to one of 5 ratings based on direction:

- **INCREASING**: Higher values = better (Player Rating: 80+ = EXCELLENT)
- **DECREASING**: Lower values = better (ADP: 1-30 = EXCELLENT)
- **BI_EXCELLENT_HI**: Middle is neutral, extremes vary (Schedule: 16 = neutral)

---

## ESPN API Integration

Player data is fetched from ESPN Fantasy API with key extraction points:

| Data Field | ESPN JSON Path | Notes |
|------------|----------------|-------|
| ADP | `ownership.averageDraftPosition` | Market consensus |
| Player Rating | `rankings[week].averageRank` (rankSourceId=0) | Expert consensus |
| Injury Status | `injuryStatus` | ACTIVE, QUESTIONABLE, OUT, etc. |
| Bye Week | Derived from team schedule | Team-specific |
| Weekly Projections | Via FantasyPointsExtractor | PPR scoring |

See individual metric reports for detailed JSON structure and extraction logic.

---

## Quick Reference: Multiplier Ranges

All multipliers use the same base range (0.95-1.05), with weights amplifying or dampening the effect:

| Step | Metric | Base Range | Typical Weight | Effective Range |
|------|--------|------------|----------------|-----------------|
| 2 | ADP | 0.95-1.05 | 2.846 | 0.87-1.15 |
| 3 | Player Rating | 0.95-1.05 | 0.784 | 0.96-1.04 |
| 4 | Team Quality | 0.95-1.05 | 1.777 | 0.91-1.09 |
| 5 | Performance | 0.95-1.05 | 2.681 | 0.87-1.14 |

| Step | Metric | Min Penalty/Bonus | Max Penalty/Bonus | Scale Factor |
|------|--------|-------------------|-------------------|--------------|
| 6 | Matchup | -4.6 pts | +4.6 pts | 115.44 |
| 7 | Schedule | -4.3 pts | +4.3 pts | 108.44 |
| 8 | Draft Order | 0 pts | +80 pts | N/A |
| 9 | Bye Week | 0 pts | -50+ pts | Linear |
| 10 | Injury | 0 pts | -100 pts | Fixed |
| 11 | Temperature | -2.5 pts | +2.5 pts | 50.0 |
| 12 | Wind | -3.0 pts | +3.0 pts | 60.0 |
| 13 | Location | -5.0 pts | +2.0 pts | Fixed |

---

## Version Information

- **Algorithm Version**: 13-step scoring system (v2.1)
- **Documentation Date**: 2025-11-26
- **Source Code Reference**: `league_helper/util/player_scoring.py`

### Recent Updates
- **v2.1 (2025-11-26)**: Added game conditions scoring (Steps 11-13)
  - Temperature scoring (all positions)
  - Wind scoring (QB, WR, K only)
  - Location scoring (home/away/international)
  - Data source: `data/game_data.csv` via GameDataManager
