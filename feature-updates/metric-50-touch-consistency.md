# Feature Request: Touch Consistency Index (RB)

**Metric ID:** M50
**Priority:** MEDIUM
**Positions:** RB
**Effort Estimate:** 2-3 hours
**Expected Impact:** 5-8% improvement in RB floor/ceiling assessment

---

## What This Metric Is

Touch Consistency Index measures the standard deviation of an RB's weekly touches (carries + targets), indicating how predictable their workload is week-to-week. Low variance = consistent floor; high variance = boom/bust potential. This helps distinguish reliable bell cows from volatile committee backs.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify reliable floors**: RBs with consistent touches have predictable weekly output
- **Flag volatile workloads**: Committee backs with high variance are riskier starts
- **Support risk-adjusted rankings**: Prefer consistency in close rankings
- **Complement volume metrics**: Adds stability dimension to touch share
- **Improve weekly decisions**: Favor consistent RBs in must-win situations

**Example Use Case:**
> RB-A averages 18 touches/game with std dev of 3.2 (consistent). RB-B averages 18 touches/game with std dev of 8.5 (volatile). Both have same average, but RB-A is safer for weekly floor while RB-B is boom/bust.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:** `data/player_data/rb_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `rushing.attempts` | float | Yes (17 weeks) | rb_data.json | 18.0 |
| `receiving.targets` | float | Yes (17 weeks) | rb_data.json | 4.0 |

**Example Data Structure:**
```json
{
  "id": "4241389",
  "name": "Derrick Henry",
  "team": "BAL",
  "position": "RB",
  "rushing": {
    "attempts": [22, 20, 18, 0, 24, 19, 21, 23, 20, 22, 18, 25, 21, 19, 22, 20, 0]
  },
  "receiving": {
    "targets": [2, 3, 1, 0, 2, 4, 2, 1, 3, 2, 3, 2, 1, 4, 2, 3, 0]
  }
}
```

### Data Validation
- Data verified in: `data/player_data/rb_data.json`
- Weekly granularity: Yes (17 weeks per season)
- Historical availability: Current season
- Known limitations: Bye weeks (0 touches) must be excluded from std dev calculation

---

## Calculation Formula

### Mathematical Definition

```python
import statistics

def calculate_touch_consistency(player: FantasyPlayer) -> dict:
    """
    Calculate touch consistency index for an RB.

    Args:
        player: FantasyPlayer object (RB position)

    Returns:
        dict: {
            'avg_touches': float,          # Mean touches per game
            'std_dev': float,              # Standard deviation of touches
            'coefficient_of_variation': float,  # CV = std_dev / avg (normalized)
            'consistency_tier': str,       # VERY_CONSISTENT, CONSISTENT, MODERATE, VOLATILE, VERY_VOLATILE
            'games_played': int
        }

    Example:
        >>> player = FantasyPlayer(name="Derrick Henry", stats={...})
        >>> result = calculate_touch_consistency(player)
        >>> result
        {'avg_touches': 23.2, 'std_dev': 2.8, 'coefficient_of_variation': 0.12,
         'consistency_tier': 'VERY_CONSISTENT', 'games_played': 15}
    """
    # Step 1: Get weekly touches (carries + targets)
    weekly_carries = player.stats.get('rushing', {}).get('attempts', [])
    weekly_targets = player.stats.get('receiving', {}).get('targets', [])

    weekly_touches = []
    for c, t in zip(weekly_carries, weekly_targets):
        total = (c or 0) + (t or 0)
        if total > 0:  # Exclude bye weeks
            weekly_touches.append(total)

    if len(weekly_touches) < 3:
        return {
            'avg_touches': 0.0,
            'std_dev': 0.0,
            'coefficient_of_variation': 0.0,
            'consistency_tier': 'INSUFFICIENT_DATA',
            'games_played': len(weekly_touches)
        }

    # Step 2: Calculate statistics
    avg_touches = statistics.mean(weekly_touches)
    std_dev = statistics.stdev(weekly_touches)

    # Step 3: Calculate Coefficient of Variation (CV)
    # CV normalizes std dev by the mean, making it comparable across different volume levels
    if avg_touches > 0:
        cv = std_dev / avg_touches
    else:
        cv = 0.0

    # Step 4: Determine consistency tier based on CV
    # Lower CV = more consistent
    if cv <= 0.15:
        consistency_tier = 'VERY_CONSISTENT'
    elif cv <= 0.25:
        consistency_tier = 'CONSISTENT'
    elif cv <= 0.35:
        consistency_tier = 'MODERATE'
    elif cv <= 0.50:
        consistency_tier = 'VOLATILE'
    else:
        consistency_tier = 'VERY_VOLATILE'

    return {
        'avg_touches': round(avg_touches, 1),
        'std_dev': round(std_dev, 2),
        'coefficient_of_variation': round(cv, 3),
        'consistency_tier': consistency_tier,
        'games_played': len(weekly_touches)
    }
```

### Thresholds & Tiers

**Coefficient of Variation (CV) Thresholds:**

| Tier | CV Range | Description | Multiplier | Example Player |
|------|----------|-------------|------------|----------------|
| VERY_CONSISTENT | <= 0.15 | Bell cow, predictable | 1.03 | Derrick Henry |
| CONSISTENT | 0.16 - 0.25 | Reliable starter | 1.015 | Most RB1s |
| MODERATE | 0.26 - 0.35 | Some variance | 1.0 | Committee lead |
| VOLATILE | 0.36 - 0.50 | Game-script dependent | 0.985 | Timeshare back |
| VERY_VOLATILE | > 0.50 | Highly unpredictable | 0.97 | Deep committee |

### Edge Cases

**1. Bye Week Handling**
- **Scenario:** Week with 0 carries and 0 targets
- **Handling:** Exclude from calculation entirely
- **Example:** [22, 20, 0, 24, 18] → use [22, 20, 24, 18] for std dev

**2. Early Season (Weeks 1-3)**
- **Scenario:** Less than 3 games of data
- **Handling:** Return INSUFFICIENT_DATA, no adjustment
- **Example:** Week 2 → skip metric until week 4+

**3. Injury Games**
- **Scenario:** Player left game early with 3 touches
- **Handling:** Include in calculation (reflects real variance in workload)
- **Example:** Injury game counts; this IS the variance we're measuring

---

## Implementation Plan

### Phase 1: Calculation Module (Estimated: 1 hour)

**File:** `league_helper/util/TouchConsistencyCalculator.py`

```python
import statistics
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class TouchConsistencyCalculator:
    """Calculate touch consistency index for RB players"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate touch consistency and return multiplier.

        Args:
            player: RB player to calculate for

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'RB':
            return 1.0, "N/A"

        metrics = self._calculate_consistency_metrics(player)

        if metrics['consistency_tier'] == 'INSUFFICIENT_DATA':
            return 1.0, "INSUFFICIENT_DATA"

        tier = metrics['consistency_tier']
        multiplier = self._get_multiplier(tier)

        return multiplier, tier

    def _calculate_consistency_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate touch consistency metrics"""
        # Implementation from formula above
        pass

    def _get_multiplier(self, tier: str) -> float:
        """Get multiplier for consistency tier"""
        multipliers = self.config.touch_consistency_scoring.get('MULTIPLIERS', {})
        base_mult = multipliers.get(tier, 1.0)
        weight = self.config.touch_consistency_scoring.get('WEIGHT', 1.0)
        return base_mult ** weight
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**Add to league_config.json:**

```json
{
  "TOUCH_CONSISTENCY_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "VERY_CONSISTENT": 0.15,
      "CONSISTENT": 0.25,
      "MODERATE": 0.35,
      "VOLATILE": 0.50
    },
    "MULTIPLIERS": {
      "VERY_CONSISTENT": 1.03,
      "CONSISTENT": 1.015,
      "MODERATE": 1.0,
      "VOLATILE": 0.985,
      "VERY_VOLATILE": 0.97
    },
    "WEIGHT": 1.0,
    "MIN_GAMES": 3,
    "DESCRIPTION": "RB touch consistency - standard deviation of weekly carries + targets"
  }
}
```

---

### Phase 3: Testing (Estimated: 1 hour)

**Unit Tests:**

```python
class TestTouchConsistencyCalculator:

    def test_bell_cow_very_consistent(self, calculator):
        """Test bell cow RB with low variance"""
        player = create_rb(
            carries=[22, 20, 21, 23, 20, 22, 21, 20, 23, 22, 21, 20, 22, 21, 20],
            targets=[2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2, 3]
        )
        # Touches: ~23-24/game with very low variance

        multiplier, tier = calculator.calculate(player)

        assert tier == "VERY_CONSISTENT"
        assert multiplier > 1.0

    def test_committee_back_volatile(self, calculator):
        """Test committee RB with high variance"""
        player = create_rb(
            carries=[18, 8, 22, 5, 20, 10, 15, 25, 8, 18, 12, 22, 6, 20, 10],
            targets=[4, 2, 3, 8, 2, 6, 4, 1, 7, 3, 5, 2, 6, 3, 5]
        )
        # Touches vary widely: 10-28/game

        multiplier, tier = calculator.calculate(player)

        assert tier in ["VOLATILE", "VERY_VOLATILE"]
        assert multiplier < 1.0
```

---

## Real-World Examples

### Example 1: Consistent Bell Cow

**Derrick Henry (BAL, RB):**

| Metric | Value |
|--------|-------|
| Weekly Touches | 24, 23, 22, 25, 23, 24, 22, 25, 23, 24, 22, 24, 23, 25, 22 |
| Average Touches | 23.4 |
| Std Dev | 1.06 |
| CV | 0.045 |
| Tier | VERY_CONSISTENT |
| Multiplier | 1.03 |

**Reason String:** `"Touch Consistency (VERY_CONSISTENT): 23.4 tch/g, CV=0.05"`

### Example 2: Volatile Committee Back

**Committee RB:**

| Metric | Value |
|--------|-------|
| Weekly Touches | 22, 8, 18, 5, 24, 10, 16, 28, 6, 20, 12, 22, 8, 18, 14 |
| Average Touches | 15.4 |
| Std Dev | 7.12 |
| CV | 0.46 |
| Tier | VOLATILE |
| Multiplier | 0.985 |

**Reason String:** `"Touch Consistency (VOLATILE): 15.4 tch/g, CV=0.46"`

---

## Dependencies

### Data Dependencies
- `rushing.attempts` - Available in `data/player_data/rb_data.json`
- `receiving.targets` - Available in `data/player_data/rb_data.json`

### Code Dependencies
- `ConfigManager` - Existing
- `FantasyPlayer` - Existing
- `TouchConsistencyCalculator` - To be created

---

## Related Metrics

**Complementary Metrics:**
- **M19 (Touch Share)** - Volume component, this adds stability
- **M04 (Carries Per Game)** - Average rushing volume
- **M37 (Boom/Bust Frequency)** - Points-based variance (this is touch-based)

---

## Implementation Checklist

- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed
- [ ] TouchConsistencyCalculator module created
- [ ] Scoring integration added
- [ ] Unit tests written and passing

---

**END OF FEATURE REQUEST**
