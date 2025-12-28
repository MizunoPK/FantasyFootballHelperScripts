# Feature Request: TD:INT Ratio (QB Ball Security)

**Metric ID:** M07
**Priority:** MEDIUM
**Positions:** QB
**Effort Estimate:** 2-3 hours
**Expected Impact:** 10-14% improvement in QB risk assessment

---

## What This Metric Is

TD:INT Ratio measures a quarterback's touchdown-to-interception ratio, quantifying ball security and decision-making. High ratio (4.0+) indicates elite ball security and efficient red zone scoring, while low ratio (<2.0) signals turnover risk and fantasy point volatility.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify elite decision-makers**: 4.0+ TD:INT ratio indicates elite ball security (Patrick Mahomes, Aaron Rodgers)
- **Quantify turnover risk**: Low ratio (<2.0) means more interceptions, leading to benching or reduced passing volume
- **Red zone efficiency**: High ratio often correlates with red zone TD efficiency
- **Predict sustainability**: QBs with low TD:INT ratios face coaching pressure to reduce risk, limiting fantasy upside
- **Draft strategy**: Target high-ratio QBs for consistent weekly floors without turnover volatility

**Example Use Case:**
> Patrick Mahomes with 4.2 TD:INT ratio (33 TDs, 8 INTs) provides stable weekly production. A QB with 1.8 ratio (24 TDs, 13 INTs) faces coaching pressure to reduce aggression, limiting fantasy upside and increasing benching risk.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/qb_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `passing.pass_tds` | float | Yes (17 weeks) | QB JSON | 2.0 |
| `passing.interceptions` | float | Yes (17 weeks) | QB JSON | 1.0 |
| `position` | string | No | All player JSON | "QB" |

**Example Data Structure:**
```json
{
  "id": "3139477",
  "name": "Patrick Mahomes",
  "team": "KC",
  "position": "QB",
  "passing": {
    "pass_tds": [3.0, 2.0, 4.0, 0.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 3.0, 2.0, 2.0],
    "interceptions": [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0]
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
def calculate_td_int_ratio(player: FantasyPlayer) -> dict:
    """
    Calculate QB TD:INT ratio.

    Args:
        player: FantasyPlayer object with passing stats

    Returns:
        dict: {
            'td_int_ratio': float,
            'total_tds': int,
            'total_ints': int,
            'tier': str
        }

    Example:
        >>> player = FantasyPlayer(name="Patrick Mahomes", position="QB", stats={...})
        >>> result = calculate_td_int_ratio(player)
        >>> result
        {'td_int_ratio': 4.2, 'total_tds': 33, 'total_ints': 8, 'tier': 'EXCELLENT'}
    """
    if player.position != 'QB':
        return {
            'td_int_ratio': 0.0,
            'total_tds': 0,
            'total_ints': 0,
            'tier': 'N/A'
        }

    # Step 1: Get passing stats
    weekly_tds = player.stats['passing']['pass_tds']
    weekly_ints = player.stats['passing']['interceptions']

    # Step 2: Calculate season totals
    total_tds = sum(weekly_tds)
    total_ints = sum(weekly_ints)

    # Step 3: Calculate TD:INT ratio
    if total_ints > 0:
        td_int_ratio = total_tds / total_ints
    else:
        # Perfect ball security (no INTs) - assign ratio equal to total TDs
        td_int_ratio = total_tds if total_tds > 0 else 0.0

    # Step 4: Determine tier
    tier = _classify_td_int_tier(td_int_ratio, total_tds)

    return {
        'td_int_ratio': round(td_int_ratio, 1),
        'total_tds': int(total_tds),
        'total_ints': int(total_ints),
        'tier': tier
    }

def _classify_td_int_tier(td_int_ratio: float, total_tds: int) -> str:
    """
    Classify QB tier based on TD:INT ratio.

    Args:
        td_int_ratio: Touchdown to interception ratio
        total_tds: Minimum TDs required for reliable sample

    Returns:
        str: Tier classification
    """
    # Require minimum 10 TDs for reliable ratio measurement
    if total_tds < 10:
        return "INSUFFICIENT_DATA"

    if td_int_ratio >= 4.0:
        return "EXCELLENT"  # Elite ball security
    elif td_int_ratio >= 3.0:
        return "GOOD"       # Above average
    elif td_int_ratio >= 2.0:
        return "AVERAGE"    # Standard
    else:
        return "POOR"       # Turnover prone
```

### Thresholds & Tiers

**QB TD:INT Ratio:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥4.0 ratio | Elite ball security | 1.04 | Patrick Mahomes, Aaron Rodgers |
| GOOD | 3.0-3.9 ratio | Above average | 1.02 | Dak Prescott, Kirk Cousins |
| AVERAGE | 2.0-2.9 ratio | Standard | 1.0 | Most starting QBs |
| POOR | <2.0 ratio | Turnover prone | 0.98 | Struggling QBs, rookies |

**Note:** Requires minimum 10 passing TDs for reliable classification.

### Edge Cases

**1. Perfect Ball Security (Zero INTs)**
- **Scenario:** QB with 25 TDs and 0 INTs (infinite ratio mathematically)
- **Handling:** Assign ratio = total TDs (caps at reasonable value)
- **Example:** QB with 0 INTs treated as having ratio equal to TD total

**2. Low Volume Passer**
- **Scenario:** QB with only 8 TDs and 2 INTs (4.0 ratio but low sample size)
- **Handling:** Classified as "INSUFFICIENT_DATA" if <10 TDs
- **Example:** Backup QB with limited action

**3. Garbage Time TDs**
- **Scenario:** QB on bad team with high TD total from garbage time but also high INTs
- **Handling:** No adjustment - ratio measures actual production regardless of context
- **Example:** QB on 3-14 team may have good volume but poor ratio

**4. Risk-Averse Game Manager**
- **Scenario:** QB with 3.5 ratio but low TD total (18 TDs, 5 INTs)
- **Handling:** Gets GOOD tier bonus but limited by overall TD production
- **Example:** Conservative QB valued for efficiency but limited ceiling

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**File:** `league_helper/util/TDINTRatioCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class TDINTRatioCalculator:
    """Calculate QB TD:INT ratio for ball security assessment"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate TD:INT ratio and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'QB':
            return 1.0, "N/A"

        # Calculate TD:INT metrics
        metrics = self._calculate_td_int_metrics(player)

        # Get multiplier from config
        multiplier = self.config.get_td_int_ratio_multiplier(metrics['tier'])

        self.logger.debug(
            f"QB {player.name}: {metrics['td_int_ratio']:.1f} TD:INT "
            f"({metrics['total_tds']} TDs / {metrics['total_ints']} INTs) "
            f"(Tier: {metrics['tier']}, Multiplier: {multiplier:.3f})"
        )

        return multiplier, metrics['tier']

    def _calculate_td_int_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate TD:INT ratio metrics for a QB"""
        weekly_tds = player.stats.get('passing', {}).get('pass_tds', [])
        weekly_ints = player.stats.get('passing', {}).get('interceptions', [])

        if not weekly_tds:
            return {
                'td_int_ratio': 0.0,
                'total_tds': 0,
                'total_ints': 0,
                'tier': 'N/A'
            }

        total_tds = sum(weekly_tds)
        total_ints = sum(weekly_ints)

        # Calculate ratio (handle zero INTs case)
        if total_ints > 0:
            td_int_ratio = total_tds / total_ints
        else:
            td_int_ratio = total_tds if total_tds > 0 else 0.0

        tier = self._classify_tier(td_int_ratio, total_tds)

        return {
            'td_int_ratio': round(td_int_ratio, 1),
            'total_tds': int(total_tds),
            'total_ints': int(total_ints),
            'tier': tier
        }

    def _classify_tier(self, td_int_ratio: float, total_tds: int) -> str:
        """Classify QB tier based on TD:INT ratio"""
        thresholds = self.config.td_int_ratio_scoring.get('THRESHOLDS', {})
        min_tds = self.config.td_int_ratio_scoring.get('MIN_TDS', 10)

        if total_tds < min_tds:
            return "INSUFFICIENT_DATA"

        if td_int_ratio >= thresholds.get('EXCELLENT', 4.0):
            return "EXCELLENT"
        elif td_int_ratio >= thresholds.get('GOOD', 3.0):
            return "GOOD"
        elif td_int_ratio >= thresholds.get('AVERAGE', 2.0):
            return "AVERAGE"
        else:
            return "POOR"
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "TD_INT_RATIO_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 4.0,
      "GOOD": 3.0,
      "AVERAGE": 2.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.04,
      "GOOD": 1.02,
      "AVERAGE": 1.0,
      "POOR": 0.98,
      "INSUFFICIENT_DATA": 1.0
    },
    "WEIGHT": 2.0,
    "MIN_TDS": 10,
    "DESCRIPTION": "QB TD:INT ratio - ball security and decision-making"
  }
}
```

**2.2 Add ConfigManager method**

```python
def get_td_int_ratio_multiplier(self, tier: str) -> float:
    """
    Get TD:INT ratio multiplier for QB ball security tier.

    Args:
        tier: Tier classification (EXCELLENT, GOOD, AVERAGE, POOR, INSUFFICIENT_DATA)

    Returns:
        float: Multiplier value
    """
    multipliers = self.config.get('TD_INT_RATIO_SCORING', {}).get('MULTIPLIERS', {})
    return multipliers.get(tier, 1.0)
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_td_int_ratio_scoring()`

```python
def _apply_td_int_ratio_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply TD:INT ratio adjustment (QB only)"""
    if p.position != 'QB':
        return player_score, ""

    if not self.config.td_int_ratio_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = TDINTRatioCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    # Apply multiplier with weight
    weight = self.config.td_int_ratio_scoring.get('WEIGHT', 2.0)
    adjusted_score = player_score * (multiplier ** weight)

    # Get metrics for reason string
    metrics = calculator._calculate_td_int_metrics(p)
    reason = f"TD:INT ({tier}): {metrics['td_int_ratio']:.1f} ({metrics['total_tds']}/{metrics['total_ints']})"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_TDINTRatioCalculator.py`

```python
import pytest
from league_helper.util.TDINTRatioCalculator import TDINTRatioCalculator
from league_helper.util.FantasyPlayer import FantasyPlayer
from league_helper.util.ConfigManager import ConfigManager

class TestTDINTRatioCalculator:
    """Test TD:INT Ratio Calculator functionality"""

    @pytest.fixture
    def calculator(self, tmp_path):
        """Create calculator with test config"""
        config = ConfigManager(tmp_path)
        return TDINTRatioCalculator(config)

    def test_elite_ball_security(self, calculator):
        """Test QB with 4.0+ TD:INT ratio"""
        player = FantasyPlayer(
            name="Patrick Mahomes",
            position="QB",
            stats={
                'passing': {
                    'pass_tds': [3, 2, 4, 0, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2],  # 33 TDs
                    'interceptions': [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0]  # 6 INTs
                }
            }
        )

        metrics = calculator._calculate_td_int_metrics(player)

        assert metrics['total_tds'] == 33
        assert metrics['total_ints'] == 6
        assert metrics['td_int_ratio'] == pytest.approx(5.5, abs=0.1)
        assert metrics['tier'] == "EXCELLENT"

    def test_turnover_prone_qb(self, calculator):
        """Test QB with <2.0 TD:INT ratio"""
        player = FantasyPlayer(
            name="Turnover Prone QB",
            position="QB",
            stats={
                'passing': {
                    'pass_tds': [2, 1, 2, 0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],  # 20 TDs
                    'interceptions': [2, 1, 2, 0, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1]  # 18 INTs
                }
            }
        )

        metrics = calculator._calculate_td_int_metrics(player)

        assert metrics['total_tds'] == 20
        assert metrics['total_ints'] == 18
        ratio = 20 / 18
        assert metrics['td_int_ratio'] == pytest.approx(ratio, abs=0.1)
        assert metrics['tier'] == "POOR"

    def test_perfect_ball_security_zero_ints(self, calculator):
        """Test QB with zero interceptions"""
        player = FantasyPlayer(
            name="Perfect QB",
            position="QB",
            stats={
                'passing': {
                    'pass_tds': [2, 2, 3, 0, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2],  # 30 TDs
                    'interceptions': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 0 INTs
                }
            }
        )

        metrics = calculator._calculate_td_int_metrics(player)

        assert metrics['total_tds'] == 30
        assert metrics['total_ints'] == 0
        # With 0 INTs, ratio should equal total TDs
        assert metrics['td_int_ratio'] == 30.0
        assert metrics['tier'] == "EXCELLENT"

    def test_insufficient_tds(self, calculator):
        """Test QB with <10 TDs"""
        player = FantasyPlayer(
            name="Backup QB",
            position="QB",
            stats={
                'passing': {
                    'pass_tds': [1, 0, 2, 0, 1, 0, 1, 0, 2, 0, 0, 0, 0, 0],  # 7 TDs
                    'interceptions': [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]  # 2 INTs
                }
            }
        )

        metrics = calculator._calculate_td_int_metrics(player)

        assert metrics['total_tds'] < 10
        assert metrics['tier'] == "INSUFFICIENT_DATA"

    def test_non_qb_returns_neutral(self, calculator):
        """Test that non-QB positions return 1.0 multiplier"""
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

**File:** `docs/scoring/17_td_int_ratio_scoring.md`

```markdown
# Step 17: TD:INT Ratio (QB Ball Security)

**Priority:** MEDIUM | **Positions:** QB | **Pattern:** Multiplier-based

## Overview

TD:INT Ratio measures quarterback ball security and decision-making, identifying elite QBs (4.0+ ratio) who maximize scoring while minimizing turnovers.

## Formula

```
td_int_ratio = total_tds / total_ints (if total_ints > 0)
td_int_ratio = total_tds (if total_ints = 0)
```

## Thresholds

- EXCELLENT: ≥4.0 ratio (+4% bonus)
- GOOD: 3.0-3.9 ratio (+2% bonus)
- AVERAGE: 2.0-2.9 ratio (no adjustment)
- POOR: <2.0 ratio (-2% penalty)
- INSUFFICIENT_DATA: <10 TDs (no adjustment)

## Example

**Patrick Mahomes (KC, QB)**
- Passing TDs: 33
- Interceptions: 8
- TD:INT Ratio: 4.1
- Tier: EXCELLENT
- Multiplier: 1.04^2.0 = 1.0816
- Impact: +8.16% to base score

## Why This Matters

High TD:INT ratio indicates elite ball security, reducing turnover risk and maintaining coaching trust for aggressive playcalling. Low ratio leads to conservative gameplans and benching risk.
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 10-14%
- Rationale: Identifies QBs with elite ball security vs turnover risk

**Starter Helper Mode:**
- Expected improvement: 12-16%
- Rationale: High-ratio QBs have lower weekly bust potential

**Trade Simulator Mode:**
- Expected improvement: 8-12%
- Rationale: Differentiates decision-making quality between QBs

---

## Real-World Examples

### Example 1: Elite Ball Security

**Patrick Mahomes (KC, QB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Passing TDs | 33 |
| Interceptions | 8 |
| TD:INT Ratio | 4.1 |
| Tier | EXCELLENT |
| Multiplier | 1.04^2.0 = 1.0816 |
| Base Score | 295.0 |
| Adjusted Score | 319.1 (+24.1 pts) |

**Reason String:** `"TD:INT (EXCELLENT): 4.1 (33/8)"`

### Example 2: Turnover Prone QB

**Struggling QB (Team, QB)** - High INTs:

| Metric | Value |
|--------|-------|
| Passing TDs | 20 |
| Interceptions | 18 |
| TD:INT Ratio | 1.1 |
| Tier | POOR |
| Multiplier | 0.98^2.0 = 0.9604 |
| Base Score | 215.0 |
| Adjusted Score | 206.5 (-8.5 pts) |

**Reason String:** `"TD:INT (POOR): 1.1 (20/18)"`

---

## Dependencies

### Data Dependencies
- ✅ `passing.pass_tds` - Available in `data/player_data/qb_data.json`
- ✅ `passing.interceptions` - Available in `data/player_data/qb_data.json`

### Code Dependencies
- 🆕 `TDINTRatioCalculator` - To be created
- ✅ `ConfigManager` - Existing, needs new method

---

## Risks & Mitigations

### Risk 1: Zero Interceptions Edge Case
- **Issue:** QBs with 0 INTs create infinite ratio mathematically
- **Mitigation:** Assign ratio = total TDs for perfect ball security
- **Severity:** Low (handled by formula)

### Risk 2: Low Sample Size
- **Issue:** Backup QBs with limited action may have skewed ratios
- **Mitigation:** Add MIN_TDS threshold (10 TDs minimum) to config
- **Severity:** Low (INSUFFICIENT_DATA tier)

---

## Implementation Checklist

**Phase 1: Data Pipeline**
- [ ] `TDINTRatioCalculator.py` created
- [ ] `calculate()` method implemented
- [ ] `_calculate_td_int_metrics()` helper created
- [ ] `_classify_tier()` helper created

**Phase 2: Configuration**
- [ ] `TD_INT_RATIO_SCORING` section added to `league_config.json`
- [ ] `get_td_int_ratio_multiplier()` method added to ConfigManager

**Phase 3: Scoring Integration**
- [ ] `_apply_td_int_ratio_scoring()` method added to `player_scoring.py`
- [ ] Integration point added to `calculate_total_score()`

**Phase 4: Testing**
- [ ] `test_TDINTRatioCalculator.py` created
- [ ] Test elite ball security (4.0+ ratio)
- [ ] Test turnover prone QB (<2.0 ratio)
- [ ] Test perfect ball security (zero INTs)
- [ ] Test insufficient TDs (<10 TDs)
- [ ] Test non-QB returns neutral
- [ ] All tests passing (100% pass rate)

**Phase 5: Documentation**
- [ ] `17_td_int_ratio_scoring.md` created
- [ ] README.md updated with Step 17
- [ ] Checklist marked complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add TD:INT ratio scoring (M07)"

---

**END OF FEATURE REQUEST**
