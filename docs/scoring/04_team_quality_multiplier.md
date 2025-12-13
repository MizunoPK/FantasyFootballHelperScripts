# Step 4: Team Quality Multiplier

Team Quality adjusts scores based on NFL team offensive/defensive strength using rolling window rankings.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 4 |
| Type | Multiplicative |
| Multiplier Range | 0.95 - 1.05 |
| Weight Exponent | 1.777 |
| Data Source | `data/team_data/{TEAM}.csv` |

## Purpose

Players on better teams have:
- More scoring opportunities (offense)
- Better defensive support (DST)
- Higher quality game scripts

Team Quality captures recent team performance trends using a rolling window.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ✅ | Team context affects season-long value |
| Starter Helper | ✅ | Team performance affects weekly upside |
| Trade Simulator | ✅ | Team quality impacts trade value |

## Calculation

### Formula

```python
# Determine which rank to use based on position
if player.position in ['DST']:
    quality_rank = player.team_defensive_rank
else:
    quality_rank = player.team_offensive_rank

final_multiplier = base_multiplier ^ WEIGHT
adjusted_score = previous_score * final_multiplier
```

### Threshold System

Team Quality uses **DECREASING** direction (lower rank = better):

Calculated from BASE_POSITION=0, STEPS=6:

| Rank Range | Rating | Base Multiplier | With Weight (1.777) |
|------------|--------|-----------------|---------------------|
| ≤6 | EXCELLENT | 1.05 | 1.091 |
| 7-12 | GOOD | 1.025 | 1.045 |
| 13-17 | AVERAGE | 1.0 | 1.000 |
| 18-23 | POOR | 0.975 | 0.956 |
| ≥24 | VERY_POOR | 0.95 | 0.914 |

Note: All multipliers use the same base range (0.95-1.05) as other scoring metrics.

### Example Calculation

**Player on rank 4 offense (EXCELLENT)**:
- Base multiplier: 1.05
- Weight: 1.777
- Final multiplier: 1.05^1.777 = 1.091
- If previous score = 153: Final = 153 × 1.091 = 166.92

## Data Sources

### Team Data Files

**Location**: `data/team_data/{TEAM}.csv` (one file per NFL team)

**Columns**:
| Column | Description |
|--------|-------------|
| `week` | NFL week (1-17) |
| `points_scored` | Team offensive output |
| `points_allowed` | Team defensive output |
| `pts_allowed_to_QB` | Points allowed to opposing QBs |
| `pts_allowed_to_RB` | Points allowed to opposing RBs |
| `pts_allowed_to_WR` | Points allowed to opposing WRs |
| `pts_allowed_to_TE` | Points allowed to opposing TEs |
| `pts_allowed_to_K` | Points allowed to opposing Ks |

### Rolling Window Calculation

Rankings use a configurable rolling window (typically 5 weeks):

```python
def _calculate_rankings(self):
    start_week = max(1, self.current_week - self.min_weeks + 1)
    end_week = self.current_week - 1  # Only completed weeks

    for team in all_teams:
        games_played = 0
        total_scored = 0
        total_allowed = 0

        for week in range(start_week, end_week + 1):
            data = load_team_week_data(team, week)
            # Skip bye weeks (both 0)
            if data.points_scored == 0 and data.points_allowed == 0:
                continue
            games_played += 1
            total_scored += data.points_scored
            total_allowed += data.points_allowed

        if games_played > 0:
            avg_scored = total_scored / games_played
            avg_allowed = total_allowed / games_played
```

### Ranking Logic

**Offensive Rank**: Teams sorted by avg points scored (highest = rank 1)
**Defensive Rank**: Teams sorted by avg points allowed (lowest = rank 1)

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_team_quality_multiplier()` (lines 473-487)

```python
def _apply_team_quality_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    quality_val = p.team_offensive_rank
    if p.position in Constants.DEFENSE_POSITIONS:
        quality_val = p.team_defensive_rank

    multiplier, rating = self.config.get_team_quality_multiplier(quality_val)
    reason = f"Team Quality: {rating} ({multiplier:.2f}x)"
    return player_score * multiplier, reason
```

### TeamDataManager

**File**: `league_helper/util/TeamDataManager.py`

Calculates and caches team rankings during initialization:

```python
class TeamDataManager:
    def __init__(self, data_folder, current_week, config):
        self.offensive_ranks = {}
        self.defensive_ranks = {}
        self._calculate_rankings()

    def get_team_offensive_rank(self, team: str) -> int:
        return self.offensive_ranks.get(team, 16)  # Default neutral

    def get_team_defensive_rank(self, team: str) -> int:
        return self.defensive_ranks.get(team, 16)
```

## Configuration

**league_config.json**:
```json
{
  "TEAM_QUALITY_SCORING": {
    "MIN_WEEKS": 5,
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "DECREASING",
      "STEPS": 6
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 1.777
  }
}
```

## Real Player Example

**Derrick Henry (RB, BAL)**:

| Metric | Value |
|--------|-------|
| Team | Baltimore Ravens |
| Offensive Rank | 3 |
| Previous Score | 153.80 |
| Rating | EXCELLENT |
| Final Multiplier | 1.05^1.777 = 1.091 |
| Adjusted Score | 153.80 × 1.091 = 167.80 |

**Reason String**: `"Team Quality: EXCELLENT (1.09x)"`

## Edge Cases

### Early Season (Week ≤ MIN_WEEKS)

When insufficient data exists:
- All teams get neutral rank 16
- Multiplier = 1.0 (AVERAGE)
- Prevents unreliable rankings from skewing scores

```python
def _set_neutral_rankings(self):
    for team in ALL_TEAMS:
        self.offensive_ranks[team] = 16
        self.defensive_ranks[team] = 16
```

### Bye Week Handling

Bye weeks are excluded from rolling window:
- Identified by points_scored = 0 AND points_allowed = 0
- games_played not incremented for bye weeks

### Unknown Teams

Teams not in data files get neutral rank 16.

## Relationship to Other Steps

- **Input**: Rating-adjusted score from Step 3
- **Output**: Team quality-adjusted score
- **Next Step**: Multiplied by Performance (Step 5)

Team Quality uses the standard 0.95-1.05 base range, with weight 1.777 producing effective range 0.91-1.09. The moderate weight reflects that it's an environmental factor, not individual skill.
