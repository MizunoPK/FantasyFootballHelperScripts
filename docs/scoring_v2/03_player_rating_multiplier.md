# Step 3: Player Rating Multiplier

Player Rating reflects expert consensus rankings, normalizing position-specific rankings to a 0-100 scale.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 3 |
| Type | Multiplicative |
| Multiplier Range | 0.95 - 1.05 |
| Weight Exponent | 0.784 |
| Data Source | `players.csv` → `player_rating` |

## Purpose

Expert rankings capture professional analysis beyond raw projections:
- **High Rating (80+)**: Consensus top-tier player → Boost score
- **Low Rating (<40)**: Experts skeptical → Reduce score

This incorporates expert opinion on factors like coaching, opportunity, and talent.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ✅ | Expert consensus valuable for draft decisions |
| Starter Helper | ❌ | Weekly decisions based on matchups, not rankings |
| Trade Simulator | ✅ | Expert value assessment important for trades |

## Calculation

### Formula

```python
final_multiplier = base_multiplier ^ WEIGHT
adjusted_score = previous_score * final_multiplier
```

### Threshold System

Player Rating uses **INCREASING** direction (higher = better):

| Rating Range | Rating | Base Multiplier | With Weight (0.784) |
|--------------|--------|-----------------|---------------------|
| ≥80 | EXCELLENT | 1.05 | 1.039 |
| 60-79 | GOOD | 1.025 | 1.020 |
| 41-59 | AVERAGE | 1.0 | 1.000 |
| 21-40 | POOR | 0.975 | 0.981 |
| ≤20 | VERY_POOR | 0.95 | 0.961 |

### Example Calculation

**Player with Rating = 85 (EXCELLENT)**:
- Base multiplier: 1.05
- Weight: 0.784
- Final multiplier: 1.05^0.784 = 1.039
- If previous score = 115: Final = 115 × 1.039 = 119.49

## Data Sources

### players.csv Column

| Column | Description | Example |
|--------|-------------|---------|
| `player_rating` | Normalized 0-100 scale | 78.5 |

### ESPN API Source

The rating extraction is complex with different logic for pre-season vs in-season:

#### Pre-Season (Week 1)

Uses draft rankings:
```json
{
  "player": {
    "draftRanksByRankType": {
      "PPR": {
        "rank": 15,
        "averageRank": 14.8
      }
    }
  }
}
```

#### During Season (Week 2+)

Uses ROS consensus rankings:
```json
{
  "player": {
    "rankings": {
      "12": [  // Week 12
        {
          "rankSourceId": 0,  // 0 = consensus
          "averageRank": 8.5
        }
      ]
    }
  }
}
```

### Normalization to 0-100 Scale

Position-specific rank is converted to a 0-100 rating using inline logic in `player-data-fetcher/espn_client.py` (lines 1975-1981):

```python
# Inline normalization during data extraction
if draft_rank <= 50:
    player_rating = 100.0 - (draft_rank - 1) * 0.4      # 100 to 80.4
elif draft_rank <= 150:
    player_rating = 80.0 - (draft_rank - 50) * 0.25     # 80 to 55
elif draft_rank <= 300:
    player_rating = 55.0 - (draft_rank - 150) * 0.2     # 55 to 25
else:
    player_rating = max(15.0, 25.0 - (draft_rank - 300) * 0.01)  # 25 to 15
```

| Position Rank | Rating |
|---------------|--------|
| 1 | 100.0 |
| 10 | 96.4 |
| 25 | 90.4 |
| 50 | 80.4 |
| 100 | 67.5 |
| 150 | 55.0 |
| 300 | 25.0 |

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_player_rating_multiplier()` (lines 463-471)

```python
def _apply_player_rating_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    multiplier, rating = self.config.get_player_rating_multiplier(p.player_rating)
    reason = f"Player Rating: {rating} ({multiplier:.2f}x)"
    return player_score * multiplier, reason
```

### ConfigManager Method

**File**: `league_helper/util/ConfigManager.py`

**Method**: `get_player_rating_multiplier()` (line 270-271)

## Configuration

**league_config.json**:
```json
{
  "PLAYER_RATING_SCORING": {
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "INCREASING",
      "STEPS": 20
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 0.784
  }
}
```

## Real Player Example

**CeeDee Lamb (WR, DAL)**:

| Metric | Value |
|--------|-------|
| Position Rank (WR) | 3 |
| Player Rating | 99.2 (calculated) |
| Previous Score | 148.03 |
| Rating | EXCELLENT |
| Final Multiplier | 1.05^0.784 = 1.039 |
| Adjusted Score | 148.03 × 1.039 = 153.80 |

**Reason String**: `"Player Rating: EXCELLENT (1.04x)"`

## Edge Cases

### No Rankings Data
- Treated as AVERAGE (1.0x multiplier)
- Common for rookies early in season

### Rank Changes Mid-Season
- System fetches most recent week with valid consensus
- Falls back through weeks until finding valid data

### Position-Specific Rankings
- WR rank 3 is different from QB rank 3
- Normalization accounts for position depth

## Relationship to Other Steps

- **Input**: ADP-adjusted score from Step 2
- **Output**: Rating-adjusted score
- **Next Step**: Multiplied by Team Quality (Step 4)

Player Rating has lower weight (0.784) than ADP (2.846) because it's less differentiating at the extremes.
