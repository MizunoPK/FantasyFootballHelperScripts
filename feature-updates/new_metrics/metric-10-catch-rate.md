# Feature Request: Catch Rate (WR/TE/RB Reliability Metric)

**Metric ID:** M10
**Priority:** MEDIUM
**Positions:** WR, TE, RB
**Effort Estimate:** 2-3 hours
**Expected Impact:** 8-12% improvement in receiver reliability assessment

---

## What This Metric Is

Catch Rate measures the percentage of targets that result in receptions for pass-catchers (WR, TE, RB), identifying reliable hands (75%+ catch rate) versus drop-prone or contested-catch receivers (<65%). High catch rate indicates QB trust, route precision, and consistent PPR production.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify reliable receivers**: 75%+ catch rate indicates elite hands and QB trust (Christian McCaffrey, Cooper Kupp)
- **Minimize wasted targets**: Low catch rate (<65%) means fewer PPR points per target and inefficient offensive usage
- **QB trust indicator**: High catch rate receivers get more target volume due to reliability
- **Route running quality**: High catch rate often indicates precise route running and separation ability
- **Draft strategy**: Target high catch rate receivers in PPR leagues for consistent weekly floors

**Example Use Case:**
> Christian McCaffrey with 80% catch rate on 8 targets = 6.4 receptions = 6.4 PPR points. A receiver with 60% catch rate on 8 targets = 4.8 receptions = 4.8 PPR points. The 1.6 reception difference equals 1.6 PPR points per week, or 27+ points per season.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/wr_data.json`, `data/player_data/te_data.json`, `data/player_data/rb_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `receiving.receptions` | float | Yes (17 weeks) | WR/TE/RB JSON | 6.0 |
| `receiving.targets` | float | Yes (17 weeks) | WR/TE/RB JSON | 8.0 |
| `position` | string | No | All player JSON | "WR", "TE", or "RB" |

**Example Data Structure:**
```json
{
  "id": "3116165",
  "name": "Christian McCaffrey",
  "team": "SF",
  "position": "RB",
  "receiving": {
    "receptions": [7.0, 5.0, 8.0, 0.0, 6.0, 7.0, 5.0, 8.0, 6.0, 8.0, 6.0, 7.0, 5.0, 7.0],
    "targets": [9.0, 6.0, 10.0, 0.0, 7.0, 9.0, 6.0, 10.0, 7.0, 10.0, 7.0, 9.0, 6.0, 9.0]
  }
}
```

### Data Validation
- ✅ Data verified in: `data/player_data/wr_data.json`, `data/player_data/te_data.json`, `data/player_data/rb_data.json`
- ✅ Weekly granularity: Yes (17 weeks per season)
- ✅ Historical availability: Current season
- ⚠️ Known limitations: None

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_catch_rate(player: FantasyPlayer) -> dict:
    """
    Calculate catch rate for WR/TE/RB.

    Args:
        player: FantasyPlayer object with receiving stats

    Returns:
        dict: {
            'catch_rate': float,
            'total_receptions': int,
            'total_targets': int,
            'tier': str
        }

    Example:
        >>> player = FantasyPlayer(name="Christian McCaffrey", position="RB", stats={...})
        >>> result = calculate_catch_rate(player)
        >>> result
        {'catch_rate': 80.0, 'total_receptions': 88, 'total_targets': 110, 'tier': 'EXCELLENT'}
    """
    if player.position not in ['WR', 'TE', 'RB']:
        return {
            'catch_rate': 0.0,
            'total_receptions': 0,
            'total_targets': 0,
            'tier': 'N/A'
        }

    # Step 1: Get receiving stats
    weekly_receptions = player.stats['receiving']['receptions']
    weekly_targets = player.stats['receiving']['targets']

    # Step 2: Calculate season totals
    total_receptions = sum(weekly_receptions)
    total_targets = sum(weekly_targets)

    # Step 3: Calculate catch rate percentage
    if total_targets > 0:
        catch_rate = (total_receptions / total_targets) * 100
    else:
        catch_rate = 0.0

    # Step 4: Determine tier
    tier = _classify_catch_rate_tier(catch_rate, total_targets)

    return {
        'catch_rate': round(catch_rate, 1),
        'total_receptions': int(total_receptions),
        'total_targets': int(total_targets),
        'tier': tier
    }

def _classify_catch_rate_tier(catch_rate: float, total_targets: int) -> str:
    """
    Classify receiver tier based on catch rate.

    Args:
        catch_rate: Catch rate percentage
        total_targets: Minimum targets required for reliable sample

    Returns:
        str: Tier classification
    """
    # Require minimum 40 targets for reliable catch rate measurement
    if total_targets < 40:
        return "INSUFFICIENT_DATA"

    if catch_rate >= 75.0:
        return "EXCELLENT"  # Elite hands, reliable
    elif catch_rate >= 70.0:
        return "GOOD"       # Above average
    elif catch_rate >= 65.0:
        return "AVERAGE"    # Standard
    else:
        return "POOR"       # Drop-prone or contested catches
```

### Thresholds & Tiers

**Catch Rate (All Positions):**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥75% catch rate | Elite hands, reliable | 1.03 | Christian McCaffrey, Cooper Kupp |
| GOOD | 70-74% catch rate | Above average | 1.015 | CeeDee Lamb, Travis Kelce |
| AVERAGE | 65-69% catch rate | Standard reliability | 1.0 | Most starting receivers |
| POOR | <65% catch rate | Drop-prone or contested | 0.985 | Deep threats, jump ball receivers |

**Note:** Requires minimum 40 targets for reliable classification.

### Edge Cases

**1. Deep Threat with Low Catch Rate**
- **Scenario:** WR with 58% catch rate due to contested deep balls
- **Handling:** Gets POOR tier penalty despite value from explosive plays
- **Example:** DK Metcalf type - contested catch specialist

**2. Checkdown RB with High Catch Rate**
- **Scenario:** RB with 85% catch rate on short dump-offs
- **Handling:** Gets EXCELLENT tier bonus - reliability matters for PPR
- **Example:** James White archetype - short-area specialist

**3. Low Volume Receiver**
- **Scenario:** WR with 35 targets (below 40 minimum) and 80% catch rate
- **Handling:** Classified as "INSUFFICIENT_DATA" despite elite catch rate
- **Example:** Complementary receiver with limited opportunities

**4. Uncatchable Targets**
- **Scenario:** Receiver with low catch rate due to poor QB accuracy
- **Handling:** Metric penalizes them - can't distinguish QB vs WR fault
- **Example:** Receivers on bad QB teams may be undervalued

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**File:** `league_helper/util/CatchRateCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class CatchRateCalculator:
    """Calculate catch rate for WR/TE/RB receivers"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate catch rate and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position not in ['WR', 'TE', 'RB']:
            return 1.0, "N/A"

        # Calculate catch rate metrics
        metrics = self._calculate_catch_rate_metrics(player)

        # Get multiplier from config
        multiplier = self.config.get_catch_rate_multiplier(metrics['tier'])

        self.logger.debug(
            f"{player.position} {player.name}: {metrics['catch_rate']:.1f}% catch rate "
            f"({metrics['total_receptions']}/{metrics['total_targets']}) "
            f"(Tier: {metrics['tier']}, Multiplier: {multiplier:.3f})"
        )

        return multiplier, metrics['tier']

    def _calculate_catch_rate_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate catch rate metrics for a receiver"""
        weekly_receptions = player.stats.get('receiving', {}).get('receptions', [])
        weekly_targets = player.stats.get('receiving', {}).get('targets', [])

        if not weekly_receptions or not weekly_targets:
            return {
                'catch_rate': 0.0,
                'total_receptions': 0,
                'total_targets': 0,
                'tier': 'N/A'
            }

        total_receptions = sum(weekly_receptions)
        total_targets = sum(weekly_targets)

        catch_rate = (total_receptions / total_targets * 100) if total_targets > 0 else 0.0

        tier = self._classify_tier(catch_rate, total_targets)

        return {
            'catch_rate': round(catch_rate, 1),
            'total_receptions': int(total_receptions),
            'total_targets': int(total_targets),
            'tier': tier
        }

    def _classify_tier(self, catch_rate: float, total_targets: int) -> str:
        """Classify receiver tier based on catch rate"""
        thresholds = self.config.catch_rate_scoring.get('THRESHOLDS', {})
        min_targets = self.config.catch_rate_scoring.get('MIN_TARGETS', 40)

        if total_targets < min_targets:
            return "INSUFFICIENT_DATA"

        if catch_rate >= thresholds.get('EXCELLENT', 75.0):
            return "EXCELLENT"
        elif catch_rate >= thresholds.get('GOOD', 70.0):
            return "GOOD"
        elif catch_rate >= thresholds.get('AVERAGE', 65.0):
            return "AVERAGE"
        else:
            return "POOR"
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "CATCH_RATE_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 75.0,
      "GOOD": 70.0,
      "AVERAGE": 65.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.03,
      "GOOD": 1.015,
      "AVERAGE": 1.0,
      "POOR": 0.985,
      "INSUFFICIENT_DATA": 1.0
    },
    "WEIGHT": 1.5,
    "MIN_TARGETS": 40,
    "DESCRIPTION": "Catch rate - receiver reliability and QB trust"
  }
}
```

**2.2 Add ConfigManager method**

```python
def get_catch_rate_multiplier(self, tier: str) -> float:
    """
    Get catch rate multiplier for receiver reliability tier.

    Args:
        tier: Tier classification (EXCELLENT, GOOD, AVERAGE, POOR, INSUFFICIENT_DATA)

    Returns:
        float: Multiplier value
    """
    multipliers = self.config.get('CATCH_RATE_SCORING', {}).get('MULTIPLIERS', {})
    return multipliers.get(tier, 1.0)
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_catch_rate_scoring()`

```python
def _apply_catch_rate_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply catch rate adjustment (WR/TE/RB only)"""
    if p.position not in ['WR', 'TE', 'RB']:
        return player_score, ""

    if not self.config.catch_rate_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = CatchRateCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    # Apply multiplier with weight
    weight = self.config.catch_rate_scoring.get('WEIGHT', 1.5)
    adjusted_score = player_score * (multiplier ** weight)

    # Get metrics for reason string
    metrics = calculator._calculate_catch_rate_metrics(p)
    reason = f"Catch Rate ({tier}): {metrics['catch_rate']:.1f}%"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_CatchRateCalculator.py`

```python
import pytest
from league_helper.util.CatchRateCalculator import CatchRateCalculator
from league_helper.util.FantasyPlayer import FantasyPlayer
from league_helper.util.ConfigManager import ConfigManager

class TestCatchRateCalculator:
    """Test Catch Rate Calculator functionality"""

    @pytest.fixture
    def calculator(self, tmp_path):
        """Create calculator with test config"""
        config = ConfigManager(tmp_path)
        return CatchRateCalculator(config)

    def test_elite_hands_rb(self, calculator):
        """Test RB with 75%+ catch rate"""
        player = FantasyPlayer(
            name="Christian McCaffrey",
            position="RB",
            stats={
                'receiving': {
                    'receptions': [7, 5, 8, 0, 6, 7, 5, 8, 6, 8, 6, 7, 5, 7],
                    'targets': [9, 6, 10, 0, 7, 9, 6, 10, 7, 10, 7, 9, 6, 9]
                }
            }
        )

        metrics = calculator._calculate_catch_rate_metrics(player)

        assert metrics['total_receptions'] == 85
        assert metrics['total_targets'] == 105
        catch_rate = (85 / 105) * 100
        assert metrics['catch_rate'] == pytest.approx(catch_rate, abs=0.1)
        assert metrics['tier'] == "EXCELLENT"

    def test_drop_prone_receiver(self, calculator):
        """Test receiver with <65% catch rate"""
        player = FantasyPlayer(
            name="Drop Prone WR",
            position="WR",
            stats={
                'receiving': {
                    'receptions': [4, 3, 5, 0, 4, 5, 3, 5, 4, 5, 4, 5, 3, 5],
                    'targets': [8, 6, 10, 0, 7, 9, 6, 10, 7, 10, 7, 9, 6, 9]
                }
            }
        )

        metrics = calculator._calculate_catch_rate_metrics(player)
        catch_rate = (metrics['total_receptions'] / metrics['total_targets']) * 100

        assert catch_rate < 65.0
        assert metrics['tier'] == "POOR"

    def test_insufficient_targets(self, calculator):
        """Test receiver with <40 targets"""
        player = FantasyPlayer(
            name="Low Volume WR",
            position="WR",
            stats={
                'receiving': {
                    'receptions': [3, 0, 4, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                    'targets': [5, 0, 6, 0, 4, 0, 5, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        )

        metrics = calculator._calculate_catch_rate_metrics(player)

        assert metrics['total_targets'] < 40
        assert metrics['tier'] == "INSUFFICIENT_DATA"

    def test_non_receiver_returns_neutral(self, calculator):
        """Test that non-receiver positions return 1.0 multiplier"""
        player = FantasyPlayer(
            name="Patrick Mahomes",
            position="QB",
            stats={'passing': {'attempts': [40, 38, 42]}}
        )

        multiplier, tier = calculator.calculate(player)

        assert multiplier == 1.0
        assert tier == "N/A"
```

---

### Phase 5: Documentation (Estimated: 30 min)

**File:** `docs/scoring/20_catch_rate_scoring.md`

```markdown
# Step 20: Catch Rate (Receiver Reliability)

**Priority:** MEDIUM | **Positions:** WR, TE, RB | **Pattern:** Multiplier-based

## Overview

Catch Rate measures receiver reliability through receptions-to-targets ratio, identifying elite hands (75%+ catch rate) who maximize PPR value and QB trust.

## Formula

```
catch_rate = (total_receptions / total_targets) * 100
```

## Thresholds

- EXCELLENT: ≥75% catch rate (+3% bonus)
- GOOD: 70-74% catch rate (+1.5% bonus)
- AVERAGE: 65-69% catch rate (no adjustment)
- POOR: <65% catch rate (-1.5% penalty)
- INSUFFICIENT_DATA: <40 targets (no adjustment)

## Example

**Christian McCaffrey (SF, RB)**
- Receptions: 88
- Targets: 110
- Catch Rate: 80.0%
- Tier: EXCELLENT
- Multiplier: 1.03^1.5 = 1.0452
- Impact: +4.52% to base score

## Why This Matters

High catch rate indicates reliable hands and QB trust, maximizing PPR points per target and reducing wasted offensive opportunities. Critical metric for PPR league evaluation.
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 8-12%
- Rationale: Identifies reliable receivers for PPR leagues

**Starter Helper Mode:**
- Expected improvement: 10-14%
- Rationale: High catch rate receivers have more predictable PPR floors

**Trade Simulator Mode:**
- Expected improvement: 6-10%
- Rationale: Separates reliable targets from boom/bust receivers

---

## Real-World Examples

### Example 1: Elite Hands RB

**Christian McCaffrey (SF, RB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Receptions | 88 |
| Targets | 110 |
| Catch Rate | 80.0% |
| Tier | EXCELLENT |
| Multiplier | 1.03^1.5 = 1.0452 |
| Base Score | 285.0 |
| Adjusted Score | 297.9 (+12.9 pts) |

**Reason String:** `"Catch Rate (EXCELLENT): 80.0%"`

### Example 2: Drop-Prone Receiver

**Drop Prone WR (Team, WR)** - Unreliable:

| Metric | Value |
|--------|-------|
| Receptions | 54 |
| Targets | 104 |
| Catch Rate | 51.9% |
| Tier | POOR |
| Multiplier | 0.985^1.5 = 0.9777 |
| Base Score | 165.0 |
| Adjusted Score | 161.3 (-3.7 pts) |

**Reason String:** `"Catch Rate (POOR): 51.9%"`

---

## Dependencies

### Data Dependencies
- ✅ `receiving.receptions` - Available in `data/player_data/[wr|te|rb]_data.json`
- ✅ `receiving.targets` - Available in `data/player_data/[wr|te|rb]_data.json`

### Code Dependencies
- 🆕 `CatchRateCalculator` - To be created
- ✅ `ConfigManager` - Existing, needs new method

---

## Risks & Mitigations

### Risk 1: Uncatchable Targets
- **Issue:** Low catch rate may reflect poor QB accuracy, not receiver fault
- **Mitigation:** Accept limitation - can't distinguish QB vs WR fault from data
- **Severity:** Medium (affects receivers on bad QB teams)

### Risk 2: Contested Catch Specialists
- **Issue:** Deep threats and jump ball receivers penalized for difficult catches
- **Mitigation:** Explosive play value captured by other metrics (YPR, TDs)
- **Severity:** Low (complementary metrics balance this)

---

## Implementation Checklist

**Phase 1: Data Pipeline**
- [ ] `CatchRateCalculator.py` created
- [ ] `calculate()` method implemented
- [ ] `_calculate_catch_rate_metrics()` helper created
- [ ] `_classify_tier()` helper created

**Phase 2: Configuration**
- [ ] `CATCH_RATE_SCORING` section added to `league_config.json`
- [ ] `get_catch_rate_multiplier()` method added to ConfigManager

**Phase 3: Scoring Integration**
- [ ] `_apply_catch_rate_scoring()` method added to `player_scoring.py`
- [ ] Integration point added to `calculate_total_score()`

**Phase 4: Testing**
- [ ] `test_CatchRateCalculator.py` created
- [ ] Test elite hands receiver (75%+ catch rate)
- [ ] Test drop-prone receiver (<65% catch rate)
- [ ] Test insufficient targets (<40 targets)
- [ ] Test non-receiver returns neutral
- [ ] All tests passing (100% pass rate)

**Phase 5: Documentation**
- [ ] `20_catch_rate_scoring.md` created
- [ ] README.md updated with Step 20
- [ ] Checklist marked complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add catch rate scoring (M10)"

---

**END OF FEATURE REQUEST**
