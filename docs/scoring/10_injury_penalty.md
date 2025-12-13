# Step 10: Injury Penalty

Injury Penalty reduces score based on player injury status and associated risk level.

## Overview

| Attribute | Value |
|-----------|-------|
| Step Number | 10 |
| Type | Additive Penalty |
| Penalty Range | 0 to -100 points |
| Data Source | `players.csv` → `injury_status` |

## Purpose

Injury status affects availability and production:
- **ACTIVE**: No injury concerns → No penalty
- **QUESTIONABLE**: May not play → Small/no penalty
- **OUT/IR**: Cannot play → Large penalty

This reduces value of players with significant injury risk.

## Mode Usage

| Mode | Enabled | Reason |
|------|---------|--------|
| Add To Roster | ✅ | Injury risk affects draft value |
| Starter Helper | ❌ | Availability filtered separately |
| Trade Simulator | ❌ | Injury status visible, not penalized |

## Calculation

### Risk Level Mapping

```python
def get_risk_level(self) -> str:
    if self.injury_status == 'ACTIVE':
        return 'LOW'
    elif self.injury_status in ['QUESTIONABLE', 'OUT', 'DOUBTFUL']:
        return 'MEDIUM'
    elif self.injury_status in ['INJURY_RESERVE', 'SUSPENSION', 'UNKNOWN']:
        return 'HIGH'
    else:
        return 'MEDIUM'  # Catch-all for unrecognized statuses
```

### Penalty Lookup

```python
penalty = config.get_injury_penalty(risk_level)
adjusted_score = previous_score - penalty
```

### Penalty Values

| Risk Level | Typical Penalty | Injury Statuses |
|------------|-----------------|-----------------|
| LOW | 0 pts | ACTIVE |
| MEDIUM | 0 pts | QUESTIONABLE, OUT, DOUBTFUL |
| HIGH | 100 pts | INJURY_RESERVE, SUSPENSION, UNKNOWN |

Note: Default configuration applies 100 pts penalty only for HIGH risk (long-term injuries).

### Example Calculation

**Player with IR status (HIGH risk)**:
- Risk level: HIGH
- Penalty: 100 pts
- If previous score = 234: Final = 234 - 100 = 134

## Data Sources

### players.csv Column

| Column | Description | Example |
|--------|-------------|---------|
| `injury_status` | ESPN injury status | QUESTIONABLE |

### ESPN API Source

```json
{
  "player": {
    "id": 4241389,
    "injuryStatus": "QUESTIONABLE",
    "injured": true
  }
}
```

**Extraction in espn_client.py** (line 1847-1851):

```python
injury_status = player_info.get('injuryStatus', 'ACTIVE')
if injury_status:
    injury_status = injury_status.upper()
```

### Common ESPN Injury Statuses

| Status | Description |
|--------|-------------|
| ACTIVE | Healthy, expected to play |
| PROBABLE | Likely to play (75%+) |
| QUESTIONABLE | Uncertain (50%) |
| DOUBTFUL | Unlikely to play (25%) |
| OUT | Will not play this week |
| IR | Injured Reserve |
| SUSPENDED | League suspension |
| PUP | Physically Unable to Perform |

## Implementation Details

### Code Location

**File**: `league_helper/util/player_scoring.py`

**Method**: `_apply_injury_penalty()` (lines 653-665)

```python
def _apply_injury_penalty(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    penalty = self.config.get_injury_penalty(p.get_risk_level())

    reason = "" if p.injury_status == "ACTIVE" else f"Injury: {p.injury_status} ({-penalty:.1f} pts)"

    return player_score - penalty, reason
```

### FantasyPlayer Method

**File**: `utils/FantasyPlayer.py` (lines 322-343)

```python
def get_risk_level(self) -> str:
    if self.injury_status == 'ACTIVE':
        return "LOW"
    elif self.injury_status in ['QUESTIONABLE', 'OUT', 'DOUBTFUL']:
        return "MEDIUM"
    elif self.injury_status in ['INJURY_RESERVE', 'SUSPENSION', 'UNKNOWN']:
        return "HIGH"
    else:
        return "MEDIUM"
```

### ConfigManager Method

**File**: `league_helper/util/ConfigManager.py`

**Method**: `get_injury_penalty()` (lines 495-515)

```python
def get_injury_penalty(self, risk_level: str) -> float:
    penalties = self.config.get('INJURY_PENALTIES', {})

    if risk_level == 'LOW':
        return penalties.get('LOW', 0)
    elif risk_level == 'MEDIUM':
        return penalties.get('MEDIUM', 0)
    else:  # HIGH or unknown
        return penalties.get('HIGH', 100)  # Default to HIGH if unknown
```

## Configuration

**league_config.json**:
```json
{
  "INJURY_PENALTIES": {
    "LOW": 0,
    "MEDIUM": 0,
    "HIGH": 100
  }
}
```

## Real Player Example

**Christian McCaffrey (RB, SF)** - Status: INJURY_RESERVE:

| Metric | Value |
|--------|-------|
| Injury Status | INJURY_RESERVE |
| Risk Level | HIGH |
| Penalty | 100 pts |
| Previous Score | 234.74 |
| Adjusted Score | 134.74 |

**Reason String**: `"Injury: INJURY_RESERVE (-100.0 pts)"`

**Note**: Players with DOUBTFUL or OUT status get MEDIUM risk (0 penalty) since these are typically weekly designations. Only long-term injuries (IR, SUSPENSION) receive the HIGH penalty.

## Edge Cases

### Unknown Status

If injury status is an unrecognized value:
- The catch-all returns MEDIUM risk
- However, the explicit 'UNKNOWN' status is mapped to HIGH risk
- This provides conservative handling for truly unknown situations while allowing flexibility for new status types

### ACTIVE Players

For healthy players:
- Penalty = 0
- Empty reason string (no injury indicator)

### Status Changes

Injury status can change frequently:
- Data fetcher updates on each run
- Penalty adjusts automatically

## Relationship to Other Steps

- **Input**: Bye penalty-adjusted score from Step 9
- **Output**: Final player score
- **This is the last step**: Result is the complete player score

## Strategic Considerations

### Why Only HIGH Risk Gets Penalty

Default configuration:
- LOW: 0 pts - Healthy players
- MEDIUM: 0 pts - Weekly injury designations (often play or return soon)
- HIGH: 100 pts - Long-term absences (IR, suspended)

This encourages:
- Drafting players with weekly injury tags (often play)
- Avoiding players on IR or suspended (extended absences)

### Penalty Magnitude

100 points is very substantial:
- Often drops player out of top recommendations
- Reflects near-total loss of value when OUT/IR
- Encourages waiting on injured players

### Trade Simulator Exception

Trade Simulator disables injury penalty:
- Injury status already visible to user
- Trade value includes risk assessment
- Avoids double-counting injury concern

## Final Score Summary

After Step 10, the final score reflects:
1. Raw projection potential
2. Market/expert consensus
3. Team and environmental factors
4. Performance trends
5. Opportunity indicators
6. Draft strategy guidance
7. Roster fit considerations
8. Availability risk

This comprehensive score enables informed fantasy football decisions.
