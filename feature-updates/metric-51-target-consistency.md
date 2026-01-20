# Feature Request: Target Consistency Index (WR/TE)

**Metric ID:** M51
**Priority:** MEDIUM
**Positions:** WR, TE
**Effort Estimate:** 2-3 hours
**Expected Impact:** 5-8% improvement in WR/TE floor assessment

---

## What This Metric Is

Target Consistency Index measures the standard deviation of a WR or TE's weekly targets, indicating workload predictability. Low variance means reliable target volume; high variance indicates boom/bust potential. In PPR leagues, consistent targets = consistent floor.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify reliable PPR floors**: WRs/TEs with consistent targets have predictable output
- **Flag volatile target distribution**: Big play dependent receivers are riskier
- **Risk-adjusted rankings**: Prefer consistency in close decisions
- **Complement target share**: Adds stability dimension to volume metrics
- **Weekly decision support**: Favor consistent players in must-win weeks

**Example Use Case:**
> WR-A averages 8 targets/game with std dev of 1.5 (consistent). WR-B averages 8 targets/game with std dev of 4.2 (volatile). Same average, but WR-A has a higher floor while WR-B is boom/bust.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:** `data/player_data/[wr|te]_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `receiving.targets` | float | Yes (17 weeks) | wr/te_data.json | 9.0 |

**Example Data Structure:**
```json
{
  "id": "4262921",
  "name": "CeeDee Lamb",
  "team": "DAL",
  "position": "WR",
  "receiving": {
    "targets": [12, 10, 9, 0, 11, 8, 10, 12, 9, 11, 10, 8, 12, 9, 10, 11, 0]
  }
}
```

### Data Validation
- Data verified in: `data/player_data/wr_data.json`, `data/player_data/te_data.json`
- Weekly granularity: Yes (17 weeks per season)
- Historical availability: Current season
- Known limitations: Bye weeks (0 targets) must be excluded

---

## Calculation Formula

### Mathematical Definition

```python
import statistics

def calculate_target_consistency(player: FantasyPlayer) -> dict:
    """
    Calculate target consistency index for a WR or TE.

    Args:
        player: FantasyPlayer object (WR or TE position)

    Returns:
        dict: {
            'avg_targets': float,
            'std_dev': float,
            'coefficient_of_variation': float,
            'consistency_tier': str,
            'games_played': int
        }

    Example:
        >>> player = FantasyPlayer(name="CeeDee Lamb", stats={...})
        >>> result = calculate_target_consistency(player)
        >>> result
        {'avg_targets': 10.2, 'std_dev': 1.4, 'coefficient_of_variation': 0.14,
         'consistency_tier': 'VERY_CONSISTENT', 'games_played': 15}
    """
    weekly_targets = player.stats.get('receiving', {}).get('targets', [])

    # Filter out bye weeks (0 targets)
    active_targets = [t for t in weekly_targets if t > 0]

    if len(active_targets) < 3:
        return {
            'avg_targets': 0.0,
            'std_dev': 0.0,
            'coefficient_of_variation': 0.0,
            'consistency_tier': 'INSUFFICIENT_DATA',
            'games_played': len(active_targets)
        }

    avg_targets = statistics.mean(active_targets)
    std_dev = statistics.stdev(active_targets)

    # Coefficient of Variation (normalized)
    cv = std_dev / avg_targets if avg_targets > 0 else 0.0

    # Determine tier
    if cv <= 0.18:
        consistency_tier = 'VERY_CONSISTENT'
    elif cv <= 0.28:
        consistency_tier = 'CONSISTENT'
    elif cv <= 0.40:
        consistency_tier = 'MODERATE'
    elif cv <= 0.55:
        consistency_tier = 'VOLATILE'
    else:
        consistency_tier = 'VERY_VOLATILE'

    return {
        'avg_targets': round(avg_targets, 1),
        'std_dev': round(std_dev, 2),
        'coefficient_of_variation': round(cv, 3),
        'consistency_tier': consistency_tier,
        'games_played': len(active_targets)
    }
```

### Thresholds & Tiers

**Coefficient of Variation (CV) Thresholds for WR/TE:**

| Tier | CV Range | Description | Multiplier | Example |
|------|----------|-------------|------------|---------|
| VERY_CONSISTENT | <= 0.18 | Elite target hog | 1.03 | Alpha WR1 |
| CONSISTENT | 0.19 - 0.28 | Reliable WR1/TE1 | 1.015 | Most WR1s |
| MODERATE | 0.29 - 0.40 | Some variance | 1.0 | WR2/TE1 |
| VOLATILE | 0.41 - 0.55 | Game-script dependent | 0.985 | Deep threat |
| VERY_VOLATILE | > 0.55 | Highly variable | 0.97 | Boom/bust |

**Note:** WR/TE thresholds are slightly higher than RB (M50) because target distribution is naturally more variable than carry distribution.

### Edge Cases

**1. Bye Week Handling**
- **Scenario:** Week with 0 targets (bye or DNP)
- **Handling:** Exclude from calculation
- **Example:** [10, 8, 0, 12, 9] → use [10, 8, 12, 9]

**2. Blowout Game with Limited Targets**
- **Scenario:** Team up big, stopped passing early
- **Handling:** Include in calculation (reflects real-world variance)

**3. Injury Return**
- **Scenario:** Player returns with limited snap count
- **Handling:** Include all active games

---

## Implementation Plan

### Phase 1: Calculation Module (Estimated: 1 hour)

**File:** `league_helper/util/TargetConsistencyCalculator.py`

```python
import statistics
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class TargetConsistencyCalculator:
    """Calculate target consistency index for WR/TE players"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate target consistency and return multiplier.

        Args:
            player: WR or TE player to calculate for

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position not in ['WR', 'TE']:
            return 1.0, "N/A"

        metrics = self._calculate_consistency_metrics(player)

        if metrics['consistency_tier'] == 'INSUFFICIENT_DATA':
            return 1.0, "INSUFFICIENT_DATA"

        tier = metrics['consistency_tier']
        multiplier = self._get_multiplier(tier)

        return multiplier, tier

    def _calculate_consistency_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate target consistency metrics"""
        # Implementation from formula above
        pass

    def _get_multiplier(self, tier: str) -> float:
        """Get multiplier for consistency tier"""
        multipliers = self.config.target_consistency_scoring.get('MULTIPLIERS', {})
        base_mult = multipliers.get(tier, 1.0)
        weight = self.config.target_consistency_scoring.get('WEIGHT', 1.0)
        return base_mult ** weight
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**Add to league_config.json:**

```json
{
  "TARGET_CONSISTENCY_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "VERY_CONSISTENT": 0.18,
      "CONSISTENT": 0.28,
      "MODERATE": 0.40,
      "VOLATILE": 0.55
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
    "DESCRIPTION": "WR/TE target consistency - standard deviation of weekly targets"
  }
}
```

---

### Phase 3: Testing (Estimated: 1 hour)

**Unit Tests:**

```python
class TestTargetConsistencyCalculator:

    def test_alpha_wr_very_consistent(self, calculator):
        """Test alpha WR with consistent targets"""
        player = create_wr(
            targets=[12, 11, 10, 12, 11, 10, 12, 11, 10, 12, 11, 10, 12, 11, 10]
        )
        # ~11 targets/game with std dev ~0.8, CV ~0.07

        multiplier, tier = calculator.calculate(player)

        assert tier == "VERY_CONSISTENT"
        assert multiplier > 1.0

    def test_deep_threat_volatile(self, calculator):
        """Test deep threat WR with volatile targets"""
        player = create_wr(
            targets=[4, 12, 3, 15, 5, 2, 14, 6, 3, 11, 4, 13, 5, 2, 12]
        )
        # High variance in targets

        multiplier, tier = calculator.calculate(player)

        assert tier in ["VOLATILE", "VERY_VOLATILE"]
        assert multiplier < 1.0
```

---

## Real-World Examples

### Example 1: Consistent Alpha WR

**CeeDee Lamb (DAL, WR):**

| Metric | Value |
|--------|-------|
| Weekly Targets | 12, 10, 11, 10, 12, 9, 11, 10, 12, 10, 11, 10, 12, 11, 10 |
| Average Targets | 10.7 |
| Std Dev | 0.98 |
| CV | 0.09 |
| Tier | VERY_CONSISTENT |
| Multiplier | 1.03 |

**Reason String:** `"Target Consistency (VERY_CONSISTENT): 10.7 tgt/g, CV=0.09"`

### Example 2: Volatile Deep Threat

**Deep Threat WR:**

| Metric | Value |
|--------|-------|
| Weekly Targets | 4, 12, 3, 8, 15, 5, 2, 11, 6, 14, 4, 9, 3, 12, 5 |
| Average Targets | 7.5 |
| Std Dev | 4.21 |
| CV | 0.56 |
| Tier | VERY_VOLATILE |
| Multiplier | 0.97 |

**Reason String:** `"Target Consistency (VERY_VOLATILE): 7.5 tgt/g, CV=0.56"`

---

## Dependencies

### Data Dependencies
- `receiving.targets` - Available in `data/player_data/[wr|te]_data.json`

### Code Dependencies
- `ConfigManager` - Existing
- `FantasyPlayer` - Existing
- `TargetConsistencyCalculator` - To be created

---

## Related Metrics

**Complementary Metrics:**
- **M01 (Target Volume)** - Volume component, this adds stability
- **M17 (Target Share Trend)** - Trending direction
- **M37 (Boom/Bust Frequency)** - Points-based variance

---

## Implementation Checklist

- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed
- [ ] TargetConsistencyCalculator module created
- [ ] Scoring integration added
- [ ] Unit tests written and passing

---

**END OF FEATURE REQUEST**
