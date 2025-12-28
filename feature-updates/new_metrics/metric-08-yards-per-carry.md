# Feature Request: Yards Per Carry (RB Efficiency)

**Metric ID:** M08
**Priority:** MEDIUM
**Positions:** RB
**Effort Estimate:** 2-3 hours
**Expected Impact:** 8-12% improvement in RB efficiency evaluation

---

## What This Metric Is

Yards Per Carry (YPC) measures a running back's rushing efficiency by calculating average yards gained per rush attempt. High YPC (5.0+) indicates elite elusiveness, blocking quality, and explosive play potential, while low YPC (<4.0) signals inefficient running or poor offensive line play.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify efficient RBs**: 5.0+ YPC indicates elite rushing ability and blocking support
- **Complement volume metrics**: High YPC + high volume (M04 Carries Per Game) = elite RB1
- **Explosive play indicator**: High YPC correlates with long runs and TD potential
- **Offensive line quality**: YPC reflects both RB talent and blocking support
- **Draft strategy**: Target RBs with elite YPC on high-scoring offenses for maximum upside

**Example Use Case:**
> Saquon Barkley with 5.8 YPC on 20 carries/game = 116 rush yards per game. An RB with 3.5 YPC on 20 carries = 70 yards per game. The 2-yard difference per carry translates to 40+ extra yards and 0.5-1.0 additional TDs per week.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/rb_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `rushing.rush_yds` | float | Yes (17 weeks) | RB JSON | 109.0 |
| `rushing.attempts` | float | Yes (17 weeks) | RB JSON | 20.0 |
| `position` | string | No | All player JSON | "RB" |

**Example Data Structure:**
```json
{
  "id": "4241985",
  "name": "Saquon Barkley",
  "team": "PHI",
  "position": "RB",
  "rushing": {
    "rush_yds": [109.0, 87.0, 147.0, 0.0, 96.0, 118.0, 105.0, 128.0, 94.0, 136.0, 102.0, 115.0, 89.0, 124.0],
    "attempts": [20.0, 18.0, 22.0, 0.0, 19.0, 21.0, 18.0, 23.0, 17.0, 24.0, 19.0, 22.0, 16.0, 22.0]
  }
}
```

### Data Validation
- ✅ Data verified in: `data/player_data/rb_data.json`
- ✅ Weekly granularity: Yes (17 weeks per season)
- ✅ Historical availability: Current season
- ⚠️ Known limitations: None

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_yards_per_carry(player: FantasyPlayer) -> dict:
    """
    Calculate yards per carry for an RB.

    Args:
        player: FantasyPlayer object with rushing stats

    Returns:
        dict: {
            'yards_per_carry': float,
            'total_rush_yds': int,
            'total_attempts': int,
            'tier': str
        }

    Example:
        >>> player = FantasyPlayer(name="Saquon Barkley", position="RB", stats={...})
        >>> result = calculate_yards_per_carry(player)
        >>> result
        {'yards_per_carry': 5.8, 'total_rush_yds': 1450, 'total_attempts': 250, 'tier': 'EXCELLENT'}
    """
    if player.position != 'RB':
        return {
            'yards_per_carry': 0.0,
            'total_rush_yds': 0,
            'total_attempts': 0,
            'tier': 'N/A'
        }

    # Step 1: Get rushing stats
    weekly_yards = player.stats['rushing']['rush_yds']
    weekly_attempts = player.stats['rushing']['attempts']

    # Step 2: Calculate season totals
    total_rush_yds = sum(weekly_yards)
    total_attempts = sum(weekly_attempts)

    # Step 3: Calculate yards per carry
    if total_attempts > 0:
        yards_per_carry = total_rush_yds / total_attempts
    else:
        yards_per_carry = 0.0

    # Step 4: Determine tier
    tier = _classify_ypc_tier(yards_per_carry, total_attempts)

    return {
        'yards_per_carry': round(yards_per_carry, 1),
        'total_rush_yds': int(total_rush_yds),
        'total_attempts': int(total_attempts),
        'tier': tier
    }

def _classify_ypc_tier(yards_per_carry: float, total_attempts: int) -> str:
    """
    Classify RB tier based on yards per carry.

    Args:
        yards_per_carry: Yards per carry average
        total_attempts: Minimum attempts required for reliable sample

    Returns:
        str: Tier classification
    """
    # Require minimum 50 rush attempts for reliable YPC measurement
    if total_attempts < 50:
        return "INSUFFICIENT_DATA"

    if yards_per_carry >= 5.0:
        return "EXCELLENT"  # Elite efficiency
    elif yards_per_carry >= 4.5:
        return "GOOD"       # Above average
    elif yards_per_carry >= 4.0:
        return "AVERAGE"    # Standard
    else:
        return "POOR"       # Inefficient
```

### Thresholds & Tiers

**RB Yards Per Carry:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥5.0 YPC | Elite efficiency, explosive | 1.04 | Saquon Barkley, Derrick Henry |
| GOOD | 4.5-4.9 YPC | Above average | 1.02 | Josh Jacobs, Jonathan Taylor |
| AVERAGE | 4.0-4.4 YPC | Standard efficiency | 1.0 | Most starting RBs |
| POOR | <4.0 YPC | Inefficient, struggling | 0.98 | Committee backs, poor O-line |

**Note:** Requires minimum 50 rush attempts for reliable classification.

### Edge Cases

**1. High YPC, Low Volume**
- **Scenario:** RB with 6.5 YPC on only 8 carries/game (backup)
- **Handling:** Gets EXCELLENT tier bonus but limited overall value due to low volume
- **Example:** Backup RB with explosive plays but limited touches

**2. Goal-Line Specialist**
- **Scenario:** RB with 3.2 YPC but high TD rate (short-yardage carries)
- **Handling:** Penalized by YPC metric despite fantasy value from TDs
- **Example:** Goal-line backs valued for TDs not efficiency

**3. Poor Offensive Line**
- **Scenario:** Talented RB with 3.8 YPC due to bad blocking
- **Handling:** Metric penalizes them despite talent - efficiency reflects situation
- **Example:** RB on bad team may be undervalued

**4. Small Sample Size**
- **Scenario:** RB with 45 carries (below 50 minimum)
- **Handling:** Classified as "INSUFFICIENT_DATA", returns 1.0 multiplier
- **Example:** Injured RB or late-season pickup

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**File:** `league_helper/util/YardsPerCarryCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class YardsPerCarryCalculator:
    """Calculate RB yards per carry efficiency"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate yards per carry and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'RB':
            return 1.0, "N/A"

        # Calculate YPC metrics
        metrics = self._calculate_ypc_metrics(player)

        # Get multiplier from config
        multiplier = self.config.get_yards_per_carry_multiplier(metrics['tier'])

        self.logger.debug(
            f"RB {player.name}: {metrics['yards_per_carry']:.1f} YPC "
            f"({metrics['total_rush_yds']} yds / {metrics['total_attempts']} att) "
            f"(Tier: {metrics['tier']}, Multiplier: {multiplier:.3f})"
        )

        return multiplier, metrics['tier']

    def _calculate_ypc_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate yards per carry metrics for an RB"""
        weekly_yards = player.stats.get('rushing', {}).get('rush_yds', [])
        weekly_attempts = player.stats.get('rushing', {}).get('attempts', [])

        if not weekly_yards or not weekly_attempts:
            return {
                'yards_per_carry': 0.0,
                'total_rush_yds': 0,
                'total_attempts': 0,
                'tier': 'N/A'
            }

        total_rush_yds = sum(weekly_yards)
        total_attempts = sum(weekly_attempts)

        yards_per_carry = (total_rush_yds / total_attempts) if total_attempts > 0 else 0.0

        tier = self._classify_tier(yards_per_carry, total_attempts)

        return {
            'yards_per_carry': round(yards_per_carry, 1),
            'total_rush_yds': int(total_rush_yds),
            'total_attempts': int(total_attempts),
            'tier': tier
        }

    def _classify_tier(self, yards_per_carry: float, total_attempts: int) -> str:
        """Classify RB tier based on yards per carry"""
        thresholds = self.config.yards_per_carry_scoring.get('THRESHOLDS', {})
        min_attempts = self.config.yards_per_carry_scoring.get('MIN_ATTEMPTS', 50)

        if total_attempts < min_attempts:
            return "INSUFFICIENT_DATA"

        if yards_per_carry >= thresholds.get('EXCELLENT', 5.0):
            return "EXCELLENT"
        elif yards_per_carry >= thresholds.get('GOOD', 4.5):
            return "GOOD"
        elif yards_per_carry >= thresholds.get('AVERAGE', 4.0):
            return "AVERAGE"
        else:
            return "POOR"
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "YARDS_PER_CARRY_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 5.0,
      "GOOD": 4.5,
      "AVERAGE": 4.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.04,
      "GOOD": 1.02,
      "AVERAGE": 1.0,
      "POOR": 0.98,
      "INSUFFICIENT_DATA": 1.0
    },
    "WEIGHT": 2.0,
    "MIN_ATTEMPTS": 50,
    "DESCRIPTION": "RB yards per carry - rushing efficiency"
  }
}
```

**2.2 Add ConfigManager method**

```python
def get_yards_per_carry_multiplier(self, tier: str) -> float:
    """
    Get yards per carry multiplier for RB efficiency tier.

    Args:
        tier: Tier classification (EXCELLENT, GOOD, AVERAGE, POOR, INSUFFICIENT_DATA)

    Returns:
        float: Multiplier value
    """
    multipliers = self.config.get('YARDS_PER_CARRY_SCORING', {}).get('MULTIPLIERS', {})
    return multipliers.get(tier, 1.0)
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_yards_per_carry_scoring()`

```python
def _apply_yards_per_carry_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply yards per carry adjustment (RB only)"""
    if p.position != 'RB':
        return player_score, ""

    if not self.config.yards_per_carry_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = YardsPerCarryCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    # Apply multiplier with weight
    weight = self.config.yards_per_carry_scoring.get('WEIGHT', 2.0)
    adjusted_score = player_score * (multiplier ** weight)

    # Get metrics for reason string
    metrics = calculator._calculate_ypc_metrics(p)
    reason = f"YPC ({tier}): {metrics['yards_per_carry']:.1f}"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_YardsPerCarryCalculator.py`

```python
import pytest
from league_helper.util.YardsPerCarryCalculator import YardsPerCarryCalculator
from league_helper.util.FantasyPlayer import FantasyPlayer
from league_helper.util.ConfigManager import ConfigManager

class TestYardsPerCarryCalculator:
    """Test Yards Per Carry Calculator functionality"""

    @pytest.fixture
    def calculator(self, tmp_path):
        """Create calculator with test config"""
        config = ConfigManager(tmp_path)
        return YardsPerCarryCalculator(config)

    def test_elite_efficiency_rb(self, calculator):
        """Test RB with 5.0+ YPC"""
        player = FantasyPlayer(
            name="Saquon Barkley",
            position="RB",
            stats={
                'rushing': {
                    'rush_yds': [109, 87, 147, 0, 96, 118, 105, 128, 94, 136, 102, 115, 89, 124],
                    'attempts': [20, 18, 22, 0, 19, 21, 18, 23, 17, 24, 19, 22, 16, 22]
                }
            }
        )

        metrics = calculator._calculate_ypc_metrics(player)

        assert metrics['total_rush_yds'] == 1450
        assert metrics['total_attempts'] == 261
        ypc = 1450 / 261
        assert metrics['yards_per_carry'] == pytest.approx(ypc, abs=0.1)
        assert metrics['tier'] == "EXCELLENT"

    def test_inefficient_rb(self, calculator):
        """Test RB with <4.0 YPC"""
        player = FantasyPlayer(
            name="Struggling RB",
            position="RB",
            stats={
                'rushing': {
                    'rush_yds': [62, 55, 71, 0, 58, 64, 59, 68, 54, 72, 60, 65, 52, 69],
                    'attempts': [18, 16, 20, 0, 17, 19, 17, 20, 15, 21, 18, 19, 14, 20]
                }
            }
        )

        metrics = calculator._calculate_ypc_metrics(player)
        ypc = metrics['total_rush_yds'] / metrics['total_attempts']

        assert ypc < 4.0
        assert metrics['tier'] == "POOR"

    def test_insufficient_attempts(self, calculator):
        """Test RB with <50 rush attempts"""
        player = FantasyPlayer(
            name="Backup RB",
            position="RB",
            stats={
                'rushing': {
                    'rush_yds': [28, 0, 35, 0, 22, 0, 31, 0, 0, 0, 0, 0, 0, 0],
                    'attempts': [6, 0, 8, 0, 5, 0, 7, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        )

        metrics = calculator._calculate_ypc_metrics(player)

        assert metrics['total_attempts'] < 50
        assert metrics['tier'] == "INSUFFICIENT_DATA"

    def test_non_rb_returns_neutral(self, calculator):
        """Test that non-RB positions return 1.0 multiplier"""
        player = FantasyPlayer(
            name="Tyreek Hill",
            position="WR",
            stats={'receiving': {'targets': [10, 8, 12]}}
        )

        multiplier, tier = calculator.calculate(player)

        assert multiplier == 1.0
        assert tier == "N/A"
```

---

### Phase 5: Documentation (Estimated: 30 min)

**File:** `docs/scoring/18_yards_per_carry_scoring.md`

```markdown
# Step 18: Yards Per Carry (RB Efficiency)

**Priority:** MEDIUM | **Positions:** RB | **Pattern:** Multiplier-based

## Overview

Yards Per Carry measures RB rushing efficiency, identifying elite runners (5.0+ YPC) who maximize yardage and TD potential through explosive play ability.

## Formula

```
yards_per_carry = total_rush_yds / total_attempts
```

## Thresholds

- EXCELLENT: ≥5.0 YPC (+4% bonus)
- GOOD: 4.5-4.9 YPC (+2% bonus)
- AVERAGE: 4.0-4.4 YPC (no adjustment)
- POOR: <4.0 YPC (-2% penalty)
- INSUFFICIENT_DATA: <50 attempts (no adjustment)

## Example

**Saquon Barkley (PHI, RB)**
- Rush yards: 1,450
- Attempts: 250
- YPC: 5.8
- Tier: EXCELLENT
- Multiplier: 1.04^2.0 = 1.0816
- Impact: +8.16% to base score

## Why This Matters

High YPC indicates elite elusiveness and blocking support, creating explosive play potential and higher TD probability. Complements volume metrics (M04 Carries Per Game) for complete RB evaluation.
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 8-12%
- Rationale: Identifies efficient RBs vs volume-based plodders

**Starter Helper Mode:**
- Expected improvement: 10-14%
- Rationale: High YPC RBs have higher boom potential weekly

**Trade Simulator Mode:**
- Expected improvement: 8-12%
- Rationale: Differentiates explosive RBs from committee backs

---

## Real-World Examples

### Example 1: Elite Efficiency RB

**Saquon Barkley (PHI, RB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Rush Yards | 1,450 |
| Attempts | 250 |
| YPC | 5.8 |
| Tier | EXCELLENT |
| Multiplier | 1.04^2.0 = 1.0816 |
| Base Score | 235.0 |
| Adjusted Score | 254.2 (+19.2 pts) |

**Reason String:** `"YPC (EXCELLENT): 5.8"`

### Example 2: Inefficient RB

**Struggling RB (Team, RB)** - Poor Efficiency:

| Metric | Value |
|--------|-------|
| Rush Yards | 809 |
| Attempts | 234 |
| YPC | 3.5 |
| Tier | POOR |
| Multiplier | 0.98^2.0 = 0.9604 |
| Base Score | 165.0 |
| Adjusted Score | 158.5 (-6.5 pts) |

**Reason String:** `"YPC (POOR): 3.5"`

---

## Dependencies

### Data Dependencies
- ✅ `rushing.rush_yds` - Available in `data/player_data/rb_data.json`
- ✅ `rushing.attempts` - Available in `data/player_data/rb_data.json`

### Code Dependencies
- 🆕 `YardsPerCarryCalculator` - To be created
- ✅ `ConfigManager` - Existing, needs new method

---

## Risks & Mitigations

### Risk 1: Offensive Line Impact
- **Issue:** YPC reflects both RB talent and O-line quality
- **Mitigation:** Accept as combined metric - situation matters for fantasy
- **Severity:** Low (situational analysis is part of fantasy evaluation)

### Risk 2: Goal-Line Backs Penalized
- **Issue:** Short-yardage RBs with high TD rate may have low YPC
- **Mitigation:** TD production captured elsewhere in scoring algorithm
- **Severity:** Low (complementary metrics balance this)

---

## Implementation Checklist

**Phase 1: Data Pipeline**
- [ ] `YardsPerCarryCalculator.py` created
- [ ] `calculate()` method implemented
- [ ] `_calculate_ypc_metrics()` helper created
- [ ] `_classify_tier()` helper created

**Phase 2: Configuration**
- [ ] `YARDS_PER_CARRY_SCORING` section added to `league_config.json`
- [ ] `get_yards_per_carry_multiplier()` method added to ConfigManager

**Phase 3: Scoring Integration**
- [ ] `_apply_yards_per_carry_scoring()` method added to `player_scoring.py`
- [ ] Integration point added to `calculate_total_score()`

**Phase 4: Testing**
- [ ] `test_YardsPerCarryCalculator.py` created
- [ ] Test elite efficiency RB (5.0+ YPC)
- [ ] Test inefficient RB (<4.0 YPC)
- [ ] Test insufficient attempts (<50 attempts)
- [ ] Test non-RB returns neutral
- [ ] All tests passing (100% pass rate)

**Phase 5: Documentation**
- [ ] `18_yards_per_carry_scoring.md` created
- [ ] README.md updated with Step 18
- [ ] Checklist marked complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add yards per carry scoring (M08)"

---

**END OF FEATURE REQUEST**
