# Step 5: Performance Multiplier

Performance Multiplier adjusts scores based on actual vs projected deviation, rewarding players who outperform expectations.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 5 |
| Type | Multiplicative |
| Multiplier Range | 0.95 - 1.05 |
| Weight Exponent | 2.681 |
| Data Source | `players.csv` (actual) + `players_projected.csv` (projected) |

## Purpose

Performance deviation captures momentum:
- **Positive deviation**: Player outperforming projections → Boost score
- **Negative deviation**: Player underperforming → Reduce score

This identifies players trending up or down relative to expectations.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ❌ | Projections already updated with recent performance |
| Starter Helper | ✅ | Recent trends critical for weekly decisions |
| Trade Simulator | ✅ | Performance trends affect trade value |

## Calculation

### Deviation Formula

```python
deviation = (actual_points - projected_points) / projected_points
```

For each week in the rolling window (last MIN_WEEKS completed weeks), calculate deviation then average across all valid weeks.

### Threshold System

Performance uses **BI_EXCELLENT_HI** direction (0 = neutral):

Calculated from BASE_POSITION=0, STEPS=0.215:

| Deviation Range | Rating | Base Multiplier | With Weight (2.681) |
|-----------------|--------|-----------------|---------------------|
| > +43% | EXCELLENT | 1.05 | 1.143 |
| +21.5% to +43% | GOOD | 1.025 | 1.069 |
| -21.5% to +21.5% | AVERAGE | 1.0 | 1.000 |
| -43% to -21.5% | POOR | 0.975 | 0.935 |
| < -43% | VERY_POOR | 0.95 | 0.873 |

Note: All multipliers use the same base range (0.95-1.05) as other scoring metrics.

### Example Calculation

**Player with +25% average deviation (GOOD)**:
- Base multiplier: 1.025
- Weight: 2.681
- Final multiplier: 1.025^2.681 = 1.069
- If previous score = 159: Final = 159 × 1.069 = 169.97

## Data Sources

### Actual Points

**Source**: `players.csv` weekly columns

| Column | Description |
|--------|-------------|
| `week_1_points` | Actual points scored in week 1 |
| `week_2_points` | Actual points scored in week 2 |
| ... | ... |

### Projected Points

**Source**: `players_projected.csv` (pre-season projections)

**Loaded by**: `ProjectedPointsManager`

```python
class ProjectedPointsManager:
    def get_projected_points(self, player: FantasyPlayer, week: int) -> Optional[float]:
        # Returns pre-season projection for comparison
        return self.projections.get(player.id, {}).get(week)
```

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `calculate_performance_deviation()` (lines 167-269)

```python
def calculate_performance_deviation(self, player: FantasyPlayer) -> Optional[float]:
    # Skip DST (insufficient projection data)
    if player.position == 'DST':
        return None

    # Get MIN_WEEKS for rolling window size
    min_weeks = self.config.performance_scoring[self.config.keys.MIN_WEEKS]

    # Calculate rolling window start (use last MIN_WEEKS completed weeks)
    start_week = max(1, self.config.current_nfl_week - min_weeks)

    deviations = []
    # Analyze only the rolling window (recent MIN_WEEKS weeks)
    for week in range(start_week, self.config.current_nfl_week):
        actual = getattr(player, f'week_{week}_points')
        projected = self.projected_points_manager.get_projected_points(player, week)

        # Skip invalid weeks
        if actual == 0 or projected == 0:
            continue

        deviation = (actual - projected) / projected
        deviations.append(deviation)

    # Require minimum weeks (MIN_WEEKS is both window size and minimum)
    if len(deviations) < min_weeks:
        return None

    return statistics.mean(deviations)
```

**Method**: `_apply_performance_multiplier()` (lines 489-523)

```python
def _apply_performance_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    deviation = self.calculate_performance_deviation(p)

    if deviation is None:
        return player_score, ""

    multiplier, rating = self.config.get_performance_multiplier(deviation)
    reason = f"Performance: {rating} ({deviation*100:+.1f}%, {multiplier:.2f}x)"
    return player_score * multiplier, reason
```

## Configuration

**league_config.json**:
```json
{
  "PERFORMANCE_SCORING": {
    "MIN_WEEKS": 3,
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "BI_EXCELLENT_HI",
      "STEPS": 0.215
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 2.681
  }
}
```

## Real Player Example

**Josh Allen (QB, BUF)** - Week 12:

| Week | Projected | Actual | Deviation |
|------|-----------|--------|-----------|
| 1 | 22.5 | 28.3 | +25.8% |
| 2 | 21.8 | 24.7 | +13.3% |
| 3 | 23.1 | 31.5 | +36.4% |
| ... | ... | ... | ... |

| Metric | Value |
|--------|-------|
| Average Deviation | +25.2% |
| Previous Score | 159.34 |
| Rating | GOOD (≥21.5%) |
| Base Multiplier | 1.025 |
| Final Multiplier | 1.025^2.681 = 1.069 |
| Adjusted Score | 159.34 × 1.069 = 170.33 |

**Reason String**: `"Performance: GOOD (+25.2%, 1.07x)"`

## Edge Cases

### DST Players

DST players are always skipped:
- Insufficient historical projection accuracy
- Returns `None` deviation, no multiplier applied

### Zero Projected Points

Weeks with projected = 0 are skipped:
- Prevents division by zero
- Often indicates missing data

### Zero Actual Points

Weeks with actual = 0 are skipped:
- Player likely didn't play (bye, injury)
- Not representative of performance ability

### Insufficient Data

Returns `None` if fewer than MIN_WEEKS valid weeks in the rolling window:
- Early season common (before MIN_WEEKS have been played)
- Players with many missed games in recent weeks

### Rolling Window

Performance now uses a rolling window of the most recent MIN_WEEKS:
- Example: current_week=10, MIN_WEEKS=3 → analyzes weeks 7, 8, 9
- This captures recent trends rather than season-long averages
- Matches how Matchup uses rolling windows for defense rankings

## Relationship to Other Steps

- **Input**: Team quality-adjusted score from Step 4
- **Output**: Performance-adjusted score
- **Next Step**: Matchup bonus applied (Step 6)

Performance uses the standard 0.95-1.05 base range with high weight (2.681), producing effective range 0.87-1.14. This creates significant impact for trending players.
