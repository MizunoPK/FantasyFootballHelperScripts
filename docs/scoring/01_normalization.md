# Step 1: Normalization

Normalization converts raw fantasy point projections to a standardized 0-N scale for fair comparison across all players.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 1 |
| Type | Base Score Calculation |
| Output Range | 0 to ~135 points |
| Data Source | `players.csv` weekly projections |

## Purpose

Fantasy point projections vary widely (0-400+ points for season). Normalization creates a comparable scale where:
- The highest projected player gets the maximum normalized score
- All other players are scored proportionally
- Different projection timeframes (ROS vs weekly) can be compared

## Mode Usage

| Mode | Projection Type | Description |
|------|-----------------|-------------|
| Add To Roster | Rest-of-Season (ROS) | Sum of weeks from current week to week 17 |
| Starter Helper | Weekly | Single week projection |
| Trade Simulator | Rest-of-Season (ROS) | Sum of remaining weeks |

## Calculation

### Formula

```python
normalized_score = (player_projection / max_projection) * NORMALIZATION_MAX_SCALE
```

Where:
- `player_projection`: Player's fantasy points (ROS or weekly)
- `max_projection`: Highest projection among all players
- `NORMALIZATION_MAX_SCALE`: Configured maximum score (typically ~135)

### Example Calculation

**Simplified Example:**

Given NORMALIZATION_MAX_SCALE = 134.79:

| Player | Projection | Calculation | Normalized Score |
|--------|------------|-------------|------------------|
| Player A | 350.0 pts | (350/350) × 134.79 | 134.79 |
| Player B | 280.0 pts | (280/350) × 134.79 | 107.83 |
| Player C | 175.0 pts | (175/350) × 134.79 | 67.40 |

### Rest-of-Season Projection

ROS projection sums weekly projections from current week through week 17:

```python
def get_rest_of_season_projection(self, current_week: int) -> float:
    total = 0.0
    for week in range(current_week, 18):  # Weeks current through 17
        week_pts = getattr(self, f'week_{week}_points', 0) or 0
        total += float(week_pts)
    return total
```

**Example**: If current week is 12, ROS = week_12 + week_13 + ... + week_17

### Weekly Projection

For Starter Helper mode, uses single week projection:

```python
def get_weekly_projection(self, player: FantasyPlayer, week: int) -> Tuple[float, float]:
    weekly_points = player.get_single_weekly_projection(week)
    weighted_projection = self.weight_projection(weekly_points, use_weekly_max=True)
    return weekly_points, weighted_projection
```

## Data Sources

### players.csv Columns

| Column | Description | Example |
|--------|-------------|---------|
| `fantasy_points` | Pre-calculated ROS projection | 285.5 |
| `week_1_points` | Week 1 projection | 18.5 |
| `week_2_points` | Week 2 projection | 17.2 |
| ... | ... | ... |
| `week_17_points` | Week 17 projection | 16.8 |

### ESPN API Source

Weekly projections come from ESPN Fantasy API:

```json
{
  "player": {
    "id": 4241389,
    "fullName": "Ja'Marr Chase",
    "stats": [
      {
        "seasonId": 2024,
        "scoringPeriodId": 1,  // Week number
        "statSourceId": 1,     // 1 = projected
        "appliedTotal": 18.5   // Fantasy points
      }
    ]
  }
}
```

**Extraction in espn_client.py**:
- Processes `stats` array for each player
- Filters by `statSourceId=1` (projections)
- Maps `scoringPeriodId` to week columns
- Uses PPR scoring format configuration

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_get_normalized_fantasy_points()` (lines 432-451)

```python
def _get_normalized_fantasy_points(self, p: FantasyPlayer, use_weekly_projection: bool) -> Tuple[float, str]:
    if use_weekly_projection:
        orig_pts, weighted_pts = self.get_weekly_projection(p)
    else:
        orig_pts = p.get_rest_of_season_projection(self.config.current_nfl_week)
        if self.max_projection > 0:
            weighted_pts = self.weight_projection(orig_pts)
        else:
            weighted_pts = 0.0

    reason = f"Projected: {orig_pts:.2f} pts, Weighted: {weighted_pts:.2f} pts"
    return weighted_pts, reason
```

### Max Projection Calculation

During player loading (`PlayerManager.load_players_from_csv()`):

```python
for player in players:
    player.fantasy_points = player.get_rest_of_season_projection(self.config.current_nfl_week)
    if player.fantasy_points > self.max_projection:
        self.max_projection = player.fantasy_points
```

## Real Player Example

**Patrick Mahomes (QB, KC)** - Week 12 of season:

| Metric | Value |
|--------|-------|
| Total Season Projection | 378.5 pts |
| Current Week | 12 |
| ROS Projection (weeks 12-17) | 127.3 pts |
| Max ROS Projection (all players) | 142.8 pts |
| NORMALIZATION_MAX_SCALE | 134.79 |

**Calculation**:
```
normalized_score = (127.3 / 142.8) × 134.79 = 120.12
```

## Edge Cases

### Zero Projections
- Players with 0 fantasy points get normalized score of 0
- Common for injured players or late-season additions

### Division by Zero Protection
```python
if self.max_projection > 0:
    weighted_pts = self.weight_projection(orig_pts)
else:
    weighted_pts = 0.0
```

### Bye Week Handling
- Bye weeks have 0 points in their week column
- ROS projection automatically excludes bye week (0 doesn't add to sum)
- Weekly projection for bye week returns 0

## Configuration

**league_config.json**:
```json
{
  "NORMALIZATION_MAX_SCALE": 134.79
}
```

This value determines the maximum possible normalized score. It's calibrated based on historical player data to produce meaningful score differentials.

## Relationship to Other Steps

- **Input**: Raw fantasy point projections from ESPN
- **Output**: Normalized score (0-135 range)
- **Next Step**: Multiplied by ADP Multiplier (Step 2)

The normalized score becomes the base that all subsequent multipliers and bonuses adjust.
