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
    # D/ST uses fantasy performance rank (NOT defensive rank)
    quality_rank = player.team_defensive_rank  # Contains dst_fantasy_rank for D/ST
else:
    quality_rank = player.team_offensive_rank

final_multiplier = base_multiplier ^ WEIGHT
adjusted_score = previous_score * final_multiplier
```

**Note**: For D/ST positions, `team_defensive_rank` contains the D/ST fantasy performance rank (see D/ST-Specific Behavior below).

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

## D/ST-Specific Behavior

### Why D/ST Uses Different Metric

D/ST positions use **D/ST fantasy points scored** instead of **points allowed to opponents** for team quality ranking.

**Problem with using defensive rank (points allowed)**:
- Measures opposing offense performance, NOT D/ST unit value
- Penalizes elite D/ST units that face high-powered offenses
- Creates backwards incentives (elite D/ST ranked poorly)

**Example - Houston Texans D/ST**:

| Metric | Points Allowed Rank | D/ST Fantasy Rank |
|--------|---------------------|-------------------|
| Season Avg | 116.6 fantasy points allowed | 9.34 fantasy points scored |
| Rank | 24th (VERY_POOR) ❌ | 4th (EXCELLENT) ✅ |
| Multiplier | 0.95x penalty | 1.05x boost |

### How D/ST Ranking Works

**Data Source**: `data/players.csv` - D/ST weekly fantasy scores (week_1_points...week_17_points)

**Ranking Logic**: Sort by D/ST fantasy points scored (descending)
- More sacks/INTs/TDs = higher fantasy points = better rank
- Uses same rolling window (MIN_WEEKS) as offensive/defensive ranks
- Skips bye weeks (None or 0 values)
- Includes negative scores in calculation

**Implementation**:
```python
# TeamDataManager calculates D/ST fantasy ranks
def _rank_dst_fantasy(self, totals: Dict[str, tuple]) -> None:
    """Rank teams by D/ST fantasy points scored (higher = better = rank 1)"""
    averages = [(team, total/games) for team, (total, games) in totals.items()]
    averages.sort(key=lambda x: x[1], reverse=True)  # Descending
    for rank, (team, _) in enumerate(averages, 1):
        self.dst_fantasy_ranks[team] = rank

# PlayerManager assigns rank to D/ST players
if player.position in Constants.DEFENSE_POSITIONS:
    player.team_defensive_rank = team_data_manager.get_team_dst_fantasy_rank(player.team)
else:
    player.team_defensive_rank = team_data_manager.get_team_defensive_rank(player.team)
```

**Semantic Note**: The attribute `team_defensive_rank` means different things by position:
- **For D/ST**: D/ST fantasy performance rank (points scored)
- **For others**: Team defensive rank (points allowed to opponents)

This reuse simplifies implementation without requiring data model changes.

### D/ST Team Quality Example

**Houston Texans D/ST** (Week 15):

| Metric | Value |
|--------|-------|
| D/ST Fantasy Rank | 4 (EXCELLENT) |
| Base Multiplier | 1.05 |
| Weight | 1.777 |
| Final Multiplier | 1.05^1.777 = 1.091 |
| Previous Score | 100.0 |
| Adjusted Score | 100.0 × 1.091 = 109.1 |

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
