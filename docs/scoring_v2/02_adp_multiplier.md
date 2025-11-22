# Step 2: ADP Multiplier

Average Draft Position (ADP) reflects market consensus on player value, incorporating wisdom from thousands of fantasy drafters.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 2 |
| Type | Multiplicative |
| Multiplier Range | 0.95 - 1.05 |
| Weight Exponent | 2.846 |
| Data Source | `players.csv` → `average_draft_position` |

## Purpose

ADP captures collective market intelligence:
- **Low ADP** (early picks): High demand, proven performers → Boost score
- **High ADP** (late picks): Lower demand, higher risk → Reduce score

This adjusts projections based on how the broader fantasy community values players.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ✅ | Market positioning critical for draft decisions |
| Starter Helper | ❌ | Already drafted, ADP irrelevant |
| Trade Simulator | ❌ | Post-draft, value determined by performance |

## Calculation

### Formula

```python
final_multiplier = base_multiplier ^ WEIGHT
adjusted_score = normalized_score * final_multiplier
```

### Threshold System

ADP uses **DECREASING** direction (lower ADP = better):

Calculated from BASE_POSITION=0, STEPS=31.63:

| ADP Range | Rating | Base Multiplier | With Weight (2.846) |
|-----------|--------|-----------------|---------------------|
| ≤31.6 | EXCELLENT | 1.05 | 1.152 |
| 31.7-63.3 | GOOD | 1.025 | 1.073 |
| 63.4-94.9 | AVERAGE | 1.0 | 1.000 |
| 95.0-126.5 | POOR | 0.975 | 0.931 |
| >126.5 | VERY_POOR | 0.95 | 0.866 |

### Example Calculation

**Player with ADP = 25 (EXCELLENT)**:
- Base multiplier: 1.05
- Weight: 2.846
- Final multiplier: 1.05^2.846 = 1.152
- If normalized score = 100: Final = 100 × 1.152 = 115.2

## Data Sources

### players.csv Column

| Column | Description | Example |
|--------|-------------|---------|
| `average_draft_position` | ESPN ADP value | 42.5 |

### ESPN API Source

```json
{
  "player": {
    "id": 4241389,
    "ownership": {
      "averageDraftPosition": 42.5,
      "percentOwned": 98.2,
      "percentStarted": 85.1
    }
  }
}
```

**Extraction in espn_client.py** (line 1853-1857):
```python
if 'ownership' in player_info:
    ownership_data = player_info['ownership']
    if 'averageDraftPosition' in ownership_data:
        adp = float(ownership_data['averageDraftPosition'])
```

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_adp_multiplier()` (lines 453-461)

```python
def _apply_adp_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    multiplier, rating = self.config.get_adp_multiplier(p.adp)
    reason = f"ADP: {rating} ({multiplier:.2f}x)"
    return player_score * multiplier, reason
```

### ConfigManager Method

**File**: `league_helper/util/ConfigManager.py`

**Method**: `get_adp_multiplier()` (line 267-268)

```python
def get_adp_multiplier(self, adp_val) -> Tuple[float, str]:
    return self._get_multiplier(self.adp_scoring, adp_val, rising_thresholds=False)
```

## Configuration

**league_config.json**:
```json
{
  "ADP_SCORING": {
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "DECREASING",
      "STEPS": 31.63
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 2.846
  }
}
```

## Real Player Example

**Ja'Marr Chase (WR, CIN)**:

| Metric | Value |
|--------|-------|
| ADP | 8.3 |
| Normalized Score | 128.5 |
| Rating | EXCELLENT |
| Base Multiplier | 1.05 |
| Final Multiplier | 1.05^2.846 = 1.152 |
| Adjusted Score | 128.5 × 1.152 = 148.03 |

**Reason String**: `"ADP: EXCELLENT (1.15x)"`

## Edge Cases

### No ADP Data
- Players without ownership data get `None` ADP
- Treated as VERY_POOR (conservative estimate)

### Very High ADP
- Players with ADP > 300 treated as undrafted/low value
- Receive VERY_POOR rating

### Rookies/New Players
- May have inflated ADP due to hype
- System trusts market consensus even for unknowns

## Relationship to Other Steps

- **Input**: Normalized score from Step 1
- **Output**: ADP-adjusted score
- **Next Step**: Multiplied by Player Rating (Step 3)

ADP and Player Rating both capture market/expert consensus but from different sources (drafters vs analysts).
