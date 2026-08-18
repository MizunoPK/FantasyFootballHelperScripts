# Step 2: ADP Multiplier

Average Draft Position (ADP) reflects market consensus on player value, incorporating wisdom from thousands of fantasy drafters.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 2 |
| Type | Multiplicative |
| Scaling Mode | LINEAR (continuous interpolation) |
| Multiplier Range | 0.8970 - 1.1090 (after the weight exponent) |
| Weight Exponent | 2.12 |
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

ADP uses **DECREASING** direction (lower ADP = better) and, since D10.3,
**`SCALING: "LINEAR"`** — the ladder is no longer a set of stepped bands.

Four anchors are calculated from BASE_POSITION=0, STEPS=25:

| Anchor ADP | Rating | Base Multiplier | With Weight (2.12) |
|-----------|--------|-----------------|---------------------|
| 25 | EXCELLENT | 1.05 | 1.1090 |
| 50 | GOOD | 1.025 | 1.0537 |
| 75 | POOR | 0.975 | 0.9477 |
| 100 | VERY_POOR | 0.95 | 0.8970 |

The label and multiplier are resolved as follows:

1. **Exactly on an anchor** → that anchor's own multiplier and label.
2. **Outside the outermost anchors** (ADP < 25 or > 100) → clamp to the nearest
   outer anchor's multiplier and label. The curve never extrapolates.
3. **Strictly between two anchors** → **linearly interpolate** the *base*
   multiplier between them, then apply the weight exponent; the label is taken
   from the bracketing anchor with the **higher** multiplier (the better side).

There is no middle band and **no `AVERAGE` rating** — that label does not exist
in the codebase's tier vocabulary. `NEUTRAL` is reachable only for a **missing**
ADP (`None`), never for an ordered valued one.

### Example Calculation

**Player with ADP = 37.5 (interpolated, between the 25 and 50 anchors)**:
- Interpolated base multiplier: 1.05 + (1.025 - 1.05) × (37.5 - 25) / (50 - 25) = 1.0375
- Weight: 2.12
- Final multiplier: 1.0375^2.12 = 1.0812
- Label: EXCELLENT (the better-side bracketing anchor)
- If normalized score = 100: Final = 100 × 1.0812 = 108.12

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
    reason = f"ADP: {rating} ({multiplier:.4f}x)"
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
    "SCALING": "LINEAR",
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "DECREASING",
      "STEPS": 25
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 2.12
  }
}
```

## Real Player Example

**Ja'Marr Chase (WR, CIN)**:

| Metric | Value |
|--------|-------|
| ADP | 8.3 (below the 25 anchor → clamped) |
| Normalized Score | 128.5 |
| Rating | EXCELLENT |
| Base Multiplier | 1.05 |
| Final Multiplier | 1.05^2.12 = 1.1090 |
| Adjusted Score | 128.5 × 1.1090 = 142.50 |

**Reason String**: `"ADP: EXCELLENT (1.1090x)"`

## Edge Cases

### No ADP Data
- Players without ownership data get `None` ADP
- Treated as NEUTRAL (multiplier 1.0) — the step neither boosts nor penalises
- This is the only way the ADP factor emits NEUTRAL under LINEAR scaling

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
