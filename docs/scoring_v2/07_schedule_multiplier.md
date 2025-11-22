# Step 7: Schedule Multiplier

Schedule Multiplier applies an additive bonus/penalty based on future opponent difficulty for rest of season.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 7 |
| Type | Additive Bonus/Penalty |
| Bonus Range | -4.3 to +4.3 points |
| Impact Scale | 108.44 |
| Data Source | `team_data/{TEAM}.csv` + `season_schedule.csv` |

## Purpose

Schedule strength captures opportunity over remaining games:
- **Easy schedule**: Many weak defenses ahead → Bonus points
- **Hard schedule**: Many strong defenses ahead → Penalty points

Like matchup, this is **additive** because it's environmental opportunity.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ❌ | Already factored into ROS projections |
| Starter Helper | ❌ | Current week only, future irrelevant |
| Trade Simulator | ✅ | Future strength affects trade value |

## Calculation

### Schedule Value Formula

```python
def _calculate_schedule_value(player: FantasyPlayer) -> Optional[float]:
    future_opponents = season_schedule.get_future_opponents(player.team, current_week)

    defense_ranks = []
    for opponent in future_opponents:
        rank = team_data.get_team_defense_vs_position_rank(opponent, player.position)
        defense_ranks.append(rank)

    # Require minimum 2 future games
    if len(defense_ranks) < 2:
        return None

    return sum(defense_ranks) / len(defense_ranks)
```

### Bonus Formula

```python
multiplier, rating = config.get_schedule_multiplier(schedule_value)
bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE
adjusted_score = previous_score + bonus
```

### Threshold System

Schedule uses **BI_EXCELLENT_HI** with base position 16, steps 2:
- **Higher rank = easier schedule** (facing worse defenses)
- **Lower rank = harder schedule** (facing better defenses)

| Avg Defense Rank | Rating | Base Multiplier | Weighted (^0.803) | Bonus (scale=108.44) |
|------------------|--------|-----------------|-------------------|----------------------|
| ≥20 | EXCELLENT | 1.05 | 1.040 | +4.34 pts |
| 18-19 | GOOD | 1.025 | 1.020 | +2.17 pts |
| 15-17 | AVERAGE | 1.0 | 1.000 | 0 pts |
| 13-14 | POOR | 0.975 | 0.980 | -2.17 pts |
| ≤12 | VERY_POOR | 0.95 | 0.961 | -4.34 pts |

### Example Calculation

**RB with avg future opponent rank 27.5 (EXCELLENT)**:
- Schedule value: 27.5
- Rating: EXCELLENT
- Weighted Multiplier: 1.05^0.803 = 1.040
- Bonus: (108.44 × 1.040) - 108.44 = +4.34
- If previous score = 163: Final = 163 + 4.34 = 167.34

## Data Sources

### Future Opponents

**Source**: `data/season_schedule.csv`

```python
def get_future_opponents(team: str, current_week: int) -> List[str]:
    opponents = []
    for week in range(current_week + 1, 18):  # Through week 17
        opponent = schedule.get_opponent(team, week)
        if opponent:  # Skip bye weeks
            opponents.append(opponent)
    return opponents
```

### Position-Specific Defense Ranks

Same as Matchup - uses rolling window rankings from `team_data/{OPPONENT}.csv`.

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_calculate_schedule_value()` (lines 271-322)

```python
def _calculate_schedule_value(self, player: FantasyPlayer) -> Optional[float]:
    future_opponents = self.season_schedule_manager.get_future_opponents(
        player.team, self.current_nfl_week
    )

    if not future_opponents:
        return None

    defense_ranks = []
    for opponent in future_opponents:
        rank = self.team_data_manager.get_team_defense_vs_position_rank(
            opponent, player.position
        )
        if rank is not None:
            defense_ranks.append(rank)

    if len(defense_ranks) < 2:
        return None

    return sum(defense_ranks) / len(defense_ranks)
```

**Method**: `_apply_schedule_multiplier()` (lines 539-575)

```python
def _apply_schedule_multiplier(self, player: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    schedule_value = self._calculate_schedule_value(player)

    if schedule_value is None:
        return player_score, ""

    multiplier, rating = self.config.get_schedule_multiplier(schedule_value)
    impact_scale = self.config.schedule_scoring['IMPACT_SCALE']
    bonus = (impact_scale * multiplier) - impact_scale

    reason = f"Schedule: {rating} (avg opp def rank: {schedule_value:.1f}, {bonus:+.1f} pts)"
    return player_score + bonus, reason
```

## Configuration

**league_config.json**:
```json
{
  "SCHEDULE_SCORING": {
    "MIN_WEEKS": 5,
    "THRESHOLDS": {
      "BASE_POSITION": 16,
      "DIRECTION": "BI_EXCELLENT_HI",
      "STEPS": 2
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 0.803,
    "IMPACT_SCALE": 108.44
  }
}
```

## Real Player Example

**A.J. Brown (WR, PHI)** - Week 12:

Future opponents (weeks 13-17): LAR, CAR, PIT, WSH, DAL

| Opponent | Defense vs WR Rank |
|----------|-------------------|
| LAR | 22 |
| CAR | 31 |
| PIT | 8 |
| WSH | 19 |
| DAL | 14 |

| Metric | Value |
|--------|-------|
| Avg Defense Rank | 18.8 |
| Previous Score | 163.26 |
| Rating | AVERAGE |
| Bonus | 0 pts |
| Adjusted Score | 163.26 |

**Reason String**: `"Schedule: AVERAGE (avg opp def rank: 18.8, +0.0 pts)"`

## Edge Cases

### End of Season

When fewer than 2 future games remain:
- Returns `None` schedule value
- No bonus applied
- Common in weeks 16-17

### Bye Weeks in Future

Bye weeks are excluded from future opponents:
- Only actual games count toward schedule

### Early Season

When insufficient weeks for defense rankings:
- All teams have neutral rank 16
- All schedules average to ~16 (neutral)

## Relationship to Other Steps

- **Input**: Matchup-adjusted score from Step 6
- **Output**: Schedule-adjusted score
- **Next Step**: Draft Order bonus applied (Step 8)

Schedule is additive like Matchup because both represent opportunity factors, not individual ability.

## Difference from Matchup

| Factor | Matchup (Step 6) | Schedule (Step 7) |
|--------|------------------|-------------------|
| Timeframe | Current week only | All future weeks |
| Use Case | Weekly decisions | Season/trade value |
| Calculation | Single opponent rank | Average of future ranks |
