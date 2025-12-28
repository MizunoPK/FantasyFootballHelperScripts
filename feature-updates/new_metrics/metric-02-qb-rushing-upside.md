# Feature Request: QB Rushing Upside (Dual-Threat QBs)

**Metric ID:** M02
**Priority:** HIGH
**Positions:** QB
**Effort Estimate:** 2-3 hours
**Expected Impact:** 12-18% improvement in QB weekly projections

---

## What This Metric Is

QB Rushing Upside measures a quarterback's rushing production (yards and touchdowns) to classify them into mobility tiers (Elite Rusher, Mobile, Pocket Passer). This metric quantifies the added fantasy value that dual-threat QBs provide through their legs.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify dual-threat QBs**: Elite rushers (Lamar Jackson, Jalen Hurts, Josh Allen) gain 40-60 rush yards/game, adding 4-6 fantasy points per week
- **Quantify rushing floor/ceiling**: Mobile QBs have higher fantasy floors since rushing yards are more consistent than passing TDs
- **Rushing TD value**: QB rushing TDs are worth 6 points vs 4 for passing TDs, making them 50% more valuable
- **Injury risk awareness**: Elite rushers have higher injury risk but also higher weekly ceiling
- **Draft strategy**: Dual-threat QBs (Tier 1) should be prioritized over pure passers even with similar passing stats

**Example Use Case:**
> Lamar Jackson averaging 250 pass yards + 1 pass TD + 60 rush yards + 0.5 rush TDs = ~23 fantasy points. Tom Brady with 300 pass yards + 2 pass TDs + 2 rush yards = ~20 points. The rushing adds 3+ points per week consistently, making Lamar a top-5 QB despite lower passing volume.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/qb_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `rushing.attempts` | float | Yes (17 weeks) | QB JSON | 8.0 |
| `rushing.rush_yds` | float | Yes (17 weeks) | QB JSON | 45.0 |
| `rushing.rush_tds` | float | Yes (17 weeks) | QB JSON | 1.0 |

**Example Data Structure:**
```json
{
  "id": "3916387",
  "name": "Lamar Jackson",
  "team": "BAL",
  "position": "QB",
  "rushing": {
    "attempts": [9.0, 7.0, 10.0, 0.0, 8.0, 9.0, ...],
    "rush_yds": [45.0, 38.0, 62.0, 0.0, 41.0, 54.0, ...],
    "rush_tds": [1.0, 0.0, 1.0, 0.0, 0.0, 1.0, ...]
  }
}
```

### Data Validation
- ✅ Data verified in: `data/player_data/qb_data.json`
- ✅ Weekly granularity: Yes (17 weeks per season)
- ✅ Historical availability: Current season
- ⚠️ Known limitations: None

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_qb_rushing_upside(player: FantasyPlayer) -> dict:
    """
    Calculate QB rushing upside metrics.

    Args:
        player: FantasyPlayer object (QB only)

    Returns:
        dict: {
            'rush_yds_per_game': float,
            'rush_tds_season': int,
            'rush_attempts_per_game': float,
            'tier': str
        }
    """
    if player.position != 'QB':
        return {'rush_yds_per_game': 0.0, 'tier': 'N/A'}

    # Step 1: Get rushing stats
    weekly_attempts = player.stats['rushing']['attempts']
    weekly_yards = player.stats['rushing']['rush_yds']
    weekly_tds = player.stats['rushing']['rush_tds']

    # Step 2: Count games played
    games_played = len([a for a in weekly_attempts if a > 0])

    # Step 3: Calculate totals
    total_rush_yds = sum(weekly_yards)
    total_rush_tds = sum(weekly_tds)
    total_attempts = sum(weekly_attempts)

    # Step 4: Calculate per-game averages
    if games_played > 0:
        rush_yds_per_game = total_rush_yds / games_played
        rush_attempts_per_game = total_attempts / games_played
    else:
        rush_yds_per_game = 0.0
        rush_attempts_per_game = 0.0

    # Step 5: Classify tier
    tier = _classify_qb_rushing_tier(rush_yds_per_game, total_rush_tds)

    return {
        'rush_yds_per_game': round(rush_yds_per_game, 1),
        'rush_tds_season': total_rush_tds,
        'rush_attempts_per_game': round(rush_attempts_per_game, 1),
        'tier': tier
    }

def _classify_qb_rushing_tier(rush_yds_pg: float, season_rush_tds: int) -> str:
    """Classify QB rushing tier"""
    # Elite mobile QBs: 50+ rush yds/game OR 6+ rush TDs
    if rush_yds_pg >= 50.0 or season_rush_tds >= 6:
        return "EXCELLENT"  # Elite dual-threat
    # Mobile QBs: 30-49 rush yds/game OR 3-5 rush TDs
    elif rush_yds_pg >= 30.0 or season_rush_tds >= 3:
        return "GOOD"       # Mobile QB
    # Occasionally mobile: 15-29 rush yds/game
    elif rush_yds_pg >= 15.0:
        return "AVERAGE"    # Occasionally mobile
    # Pocket passers: <15 rush yds/game
    else:
        return "POOR"       # Pocket passer
```

### Thresholds & Tiers

**QB Rushing Upside:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥50 yds/game OR 6+ TDs | Elite dual-threat | 1.05 | Lamar Jackson, Jalen Hurts |
| GOOD | 30-49 yds/game OR 3-5 TDs | Mobile QB | 1.025 | Josh Allen, Kyler Murray |
| AVERAGE | 15-29 yds/game | Occasionally mobile | 1.0 | Patrick Mahomes |
| POOR | <15 yds/game | Pocket passer | 0.975 | Joe Burrow, Tua Tagovailoa |

### Edge Cases

**1. Designed Runs vs Scrambles**
- **Scenario:** Some QBs have designed runs (RPO), others scramble when pressured
- **Handling:** Metric doesn't distinguish - all rushing yards count equally
- **Example:** Lamar's designed runs and Josh Allen's scrambles both contribute to rushing yards

**2. Short-Yardage QB Sneaks**
- **Scenario:** QB with low rush yards but multiple short TD sneaks
- **Handling:** Season rush TDs >= 6 qualifies as EXCELLENT even with low yards/game
- **Example:** QB with 12 rush yards/game but 8 TDs from goal line = EXCELLENT tier

**3. Injury-Related Rushing Decline**
- **Scenario:** QB with history of rushing becomes pocket passer after injury
- **Handling:** Uses current season data only, not historical patterns
- **Example:** Cam Newton post-injury had different rushing profile

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**File:** `league_helper/util/QBRushingUpsideCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer

class QBRushingUpsideCalculator:
    """Calculate QB rushing upside for dual-threat QBs"""

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """Calculate rushing upside and return multiplier"""
        if player.position != 'QB':
            return 1.0, "N/A"

        metrics = self._calculate_rushing_metrics(player)
        multiplier = self.config.get_qb_rushing_upside_multiplier(metrics['tier'])

        return multiplier, metrics['tier']
```

---

### Phase 2: Configuration (Estimated: 30 min)

```json
{
  "QB_RUSHING_UPSIDE_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT_YDS": 50.0,
      "EXCELLENT_TDS": 6,
      "GOOD_YDS": 30.0,
      "GOOD_TDS": 3,
      "AVERAGE_YDS": 15.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.05,
      "GOOD": 1.025,
      "AVERAGE": 1.0,
      "POOR": 0.975
    },
    "WEIGHT": 1.8,
    "DESCRIPTION": "QB rushing upside - dual-threat value"
  }
}
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 10-15%
- Rationale: Identifies dual-threat QBs early in draft, separates elite rushers from pocket passers

**Starter Helper Mode:**
- Expected improvement: 12-18%
- Rationale: Rushing floor is more predictable than passing TDs, helps weekly QB decisions

**Trade Simulator Mode:**
- Expected improvement: 8-12%
- Rationale: Differentiates QB value beyond just passing stats

---

## Real-World Examples

### Example 1: Elite Dual-Threat QB

**Lamar Jackson (BAL, QB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Rush Yards | 764 |
| Games Played | 15 |
| Rush Yds/Game | 50.9 |
| Rush TDs | 4 |
| Tier | EXCELLENT |
| Multiplier | 1.05^1.8 = 1.0922 |
| Base Score | 265.0 |
| Adjusted Score | 289.4 (+24.4 pts) |

**Reason String:** `"QB Rushing (EXCELLENT): 50.9 yds/game, 4 TDs"`

### Example 2: Pocket Passer

**Joe Burrow (CIN, QB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Rush Yards | 45 |
| Games Played | 14 |
| Rush Yds/Game | 3.2 |
| Rush TDs | 0 |
| Tier | POOR |
| Multiplier | 0.975^1.8 = 0.9554 |
| Base Score | 245.0 |
| Adjusted Score | 234.1 (-10.9 pts) |

**Reason String:** `"QB Rushing (POOR): 3.2 yds/game, 0 TDs"`

---

## Dependencies

### Data Dependencies
- ✅ `rushing.attempts`, `rushing.rush_yds`, `rushing.rush_tds` - Available in QB JSON

### Code Dependencies
- 🆕 `QBRushingUpsideCalculator` - To be created

---

## Implementation Checklist

**Implementation:**
- [ ] QBRushingUpsideCalculator module created
- [ ] Scoring integration added
- [ ] Configuration updated

**Testing:**
- [ ] Unit tests passing
- [ ] Validated with Lamar Jackson, Josh Allen, Joe Burrow

**Completion:**
- [ ] Committed: "Add QB rushing upside scoring"

---

**END OF FEATURE REQUEST**
