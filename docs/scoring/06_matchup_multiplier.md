# Step 6: Matchup Multiplier

Matchup Multiplier applies an additive bonus/penalty based on current week opponent defensive strength.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 6 |
| Type | Additive Bonus/Penalty |
| Bonus Range | -4.6 to +4.6 points |
| Impact Scale | 115.44 |
| Data Source | `team_data/{TEAM}.csv` + `season_schedule.csv` |

## Purpose

Matchup captures opportunity:
- **Favorable matchup**: Facing weak defense → Bonus points
- **Unfavorable matchup**: Facing strong defense → Penalty points

This is **additive** (not multiplicative) because matchup is an environmental factor available equally to all players.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ❌ | Season-long value, not single-week matchup |
| Starter Helper | ✅ | Critical for weekly lineup decisions |
| Trade Simulator | ❌ | Current week not relevant to trade value |

## Calculation

### Matchup Score Formula

```python
matchup_score = opponent_position_defense_rank
```

Where opponent rank is position-specific (e.g., defense vs WR):
- Rank 32 (worst defense) → score = 32 (favorable - EXCELLENT)
- Rank 16 (average defense) → score = 16 (AVERAGE)
- Rank 1 (best defense) → score = 1 (unfavorable - VERY_POOR)

Higher matchup score = facing weaker defense = better matchup.

### Bonus Formula

```python
multiplier, rating = config.get_matchup_multiplier(matchup_score)
bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE
adjusted_score = previous_score + bonus
```

### Threshold System

Calculated from BASE_POSITION=0, STEPS=6, DIRECTION=INCREASING:

Note: Higher matchup_score = better matchup (facing weaker defense)

| Matchup Score | Rating | Base Multiplier | Weighted (^0.803) | Bonus (scale=115.44) |
|---------------|--------|-----------------|-------------------|----------------------|
| ≥24 | EXCELLENT | 1.05 | 1.040 | +4.57 pts |
| 18-23 | GOOD | 1.025 | 1.020 | +2.29 pts |
| 13-17 | AVERAGE | 1.0 | 1.000 | 0 pts |
| 7-12 | POOR | 0.975 | 0.980 | -2.29 pts |
| ≤6 | VERY_POOR | 0.95 | 0.961 | -4.57 pts |

### Example Calculation

**WR facing rank 28 defense (EXCELLENT)**:
- Matchup score: 28 (opponent's defense rank vs WR)
- Rating: EXCELLENT (score ≥ 24)
- Base Multiplier: 1.05
- Weighted Multiplier: 1.05^0.803 = 1.040
- Bonus: (115.44 × 1.040) - 115.44 = +4.62
- If previous score = 161: Final = 161 + 4.62 = 165.62

## Data Sources

### Position-Specific Defense Ranks

**Source**: `data/team_data/{OPPONENT}.csv`

Each team file contains weekly position-specific points allowed:

| Column | Description |
|--------|-------------|
| `pts_allowed_to_QB` | Points allowed to opposing QBs |
| `pts_allowed_to_RB` | Points allowed to opposing RBs |
| `pts_allowed_to_WR` | Points allowed to opposing WRs |
| `pts_allowed_to_TE` | Points allowed to opposing TEs |
| `pts_allowed_to_K` | Points allowed to opposing Ks |

### Rolling Window Ranking

Same as Team Quality, uses MIN_WEEKS rolling window:

```python
def get_team_defense_vs_position_rank(team: str, position: str) -> int:
    # Calculate average points allowed to position
    # Rank all teams (lowest allowed = rank 1 = best)
    return self.position_ranks[team][position]
```

### Current Week Opponent

**Source**: `data/season_schedule.csv`

```csv
week,team,opponent
12,KC,LV
12,BUF,SF
```

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_matchup_multiplier()` (lines 525-537)

```python
def _apply_matchup_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    multiplier, rating = self.config.get_matchup_multiplier(p.matchup_score)
    impact_scale = self.config.matchup_scoring['IMPACT_SCALE']
    bonus = (impact_scale * multiplier) - impact_scale

    reason = f"Matchup: {rating} ({bonus:+.1f} pts)"
    return player_score + bonus, reason
```

### Matchup Score Assignment

During player loading in `PlayerManager.load_players_from_csv()`:

```python
matchup_score = self.team_data_manager.get_rank_difference(player.team, player.position)
player.matchup_score = matchup_score
```

## Configuration

**league_config.json**:
```json
{
  "MATCHUP_SCORING": {
    "MIN_WEEKS": 5,
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "INCREASING",
      "STEPS": 6
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 0.803,
    "IMPACT_SCALE": 115.44
  }
}
```

## Real Player Example

**Davante Adams (WR, NYJ)** vs TEN (Week 12):

| Metric | Value |
|--------|-------|
| Opponent | Tennessee Titans |
| TEN defense vs WR rank | 25 |
| Matchup Score | 25 |
| Previous Score | 161.41 |
| Rating | EXCELLENT (≥24) |
| Bonus | +4.57 pts |
| Adjusted Score | 161.41 + 4.57 = 165.98 |

**Reason String**: `"Matchup: EXCELLENT (+4.6 pts)"`

## Edge Cases

### Bye Week

Players on bye have no opponent:
- No matchup score assigned
- Matchup multiplier skipped or returns neutral

### Early Season

When insufficient weeks for position defense rankings:
- All teams get neutral rank 16
- Matchup scores all become 0 (neutral)

### Unknown Opponent

If opponent not found in schedule:
- Returns neutral matchup score

## Relationship to Other Steps

- **Input**: Performance-adjusted score from Step 5
- **Output**: Matchup-adjusted score
- **Next Step**: Schedule bonus applied (Step 7)

Matchup is additive because it's an opportunity factor, not a skill multiplier. All players benefit equally from good matchups.
