# Feature Request: Kicker Accuracy (Overall FG%)

**Metric ID:** M05
**Priority:** HIGH
**Positions:** K
**Effort Estimate:** 2-3 hours
**Expected Impact:** 8-12% improvement in kicker valuations

---

## What This Metric Is

Kicker Accuracy measures a kicker's overall field goal percentage and extra point accuracy, providing a reliability metric for fantasy production. High-accuracy kickers (90%+ FG) provide a consistent weekly floor and minimize negative points from missed kicks.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify reliable kickers**: 90%+ accuracy kickers provide weekly consistency and minimize boom/bust variance
- **Penalize inconsistency**: Low-accuracy kickers (<80%) hurt fantasy teams with missed kicks and potential negative points
- **Volume + accuracy combination**: Best kickers combine high attempt volume with high accuracy (Justin Tucker, Harrison Butker)
- **Draft strategy**: Target accurate kickers on high-scoring offenses for optimal floor/ceiling combination
- **Weather reliability**: Accurate kickers perform better in adverse weather conditions

**Example Use Case:**
> Justin Tucker with 92% FG accuracy and 8 attempts per game scores more consistently than a kicker with 78% accuracy and 10 attempts. The high-volume but inaccurate kicker has more boom/bust weeks, while Tucker provides a stable weekly floor.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/k_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `field_goals.made` | float | Yes (17 weeks) | K JSON | 3.0 |
| `field_goals.missed` | float | Yes (17 weeks) | K JSON | 1.0 |
| `extra_points.made` | float | Yes (17 weeks) | K JSON | 5.0 |
| `extra_points.missed` | float | Yes (17 weeks) | K JSON | 0.0 |
| `position` | string | No | All player JSON | "K" |

**Example Data Structure:**
```json
{
  "id": "4046702",
  "name": "Justin Tucker",
  "team": "BAL",
  "position": "K",
  "field_goals": {
    "made": [3.0, 2.0, 4.0, 0.0, 2.0, 3.0, 2.0, 3.0, 2.0, 4.0, 3.0, 2.0, 3.0, 2.0],
    "missed": [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
  },
  "extra_points": {
    "made": [5.0, 4.0, 6.0, 0.0, 3.0, 5.0, 4.0, 6.0, 5.0, 7.0, 5.0, 4.0, 5.0, 3.0],
    "missed": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  }
}
```

### Data Validation
- ✅ Data verified in: `data/player_data/k_data.json`
- ✅ Weekly granularity: Yes (17 weeks per season)
- ✅ Historical availability: Current season
- ⚠️ Known limitations: No distance breakdown (0-39, 40-49, 50+ yards) - only overall accuracy

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_kicker_accuracy(player: FantasyPlayer) -> dict:
    """
    Calculate kicker field goal and extra point accuracy.

    Args:
        player: FantasyPlayer object with kicking stats

    Returns:
        dict: {
            'fg_percentage': float,
            'xp_percentage': float,
            'fg_made': int,
            'fg_attempted': int,
            'xp_made': int,
            'xp_attempted': int,
            'tier': str
        }

    Example:
        >>> player = FantasyPlayer(name="Justin Tucker", position="K", stats={...})
        >>> result = calculate_kicker_accuracy(player)
        >>> result
        {'fg_percentage': 92.3, 'xp_percentage': 100.0, 'fg_made': 36, 'fg_attempted': 39, 'tier': 'EXCELLENT'}
    """
    if player.position != 'K':
        return {
            'fg_percentage': 0.0,
            'xp_percentage': 0.0,
            'fg_made': 0,
            'fg_attempted': 0,
            'xp_made': 0,
            'xp_attempted': 0,
            'tier': 'N/A'
        }

    # Step 1: Get kicking stats
    fg_made_weekly = player.stats['field_goals']['made']
    fg_missed_weekly = player.stats['field_goals']['missed']
    xp_made_weekly = player.stats['extra_points']['made']
    xp_missed_weekly = player.stats['extra_points']['missed']

    # Step 2: Calculate season totals
    fg_made = sum(fg_made_weekly)
    fg_missed = sum(fg_missed_weekly)
    xp_made = sum(xp_made_weekly)
    xp_missed = sum(xp_missed_weekly)

    fg_attempted = fg_made + fg_missed
    xp_attempted = xp_made + xp_missed

    # Step 3: Calculate percentages
    if fg_attempted > 0:
        fg_percentage = (fg_made / fg_attempted) * 100
    else:
        fg_percentage = 0.0

    if xp_attempted > 0:
        xp_percentage = (xp_made / xp_attempted) * 100
    else:
        xp_percentage = 0.0

    # Step 4: Determine tier (based on FG%, XP% is expected to be near 100%)
    tier = _classify_kicker_tier(fg_percentage, fg_attempted)

    return {
        'fg_percentage': round(fg_percentage, 1),
        'xp_percentage': round(xp_percentage, 1),
        'fg_made': int(fg_made),
        'fg_attempted': int(fg_attempted),
        'xp_made': int(xp_made),
        'xp_attempted': int(xp_attempted),
        'tier': tier
    }

def _classify_kicker_tier(fg_percentage: float, fg_attempted: int) -> str:
    """
    Classify kicker tier based on FG accuracy.

    Args:
        fg_percentage: Field goal percentage
        fg_attempted: Minimum attempts required for reliable sample

    Returns:
        str: Tier classification
    """
    # Require minimum 10 attempts for reliable accuracy measurement
    if fg_attempted < 10:
        return "INSUFFICIENT_DATA"

    if fg_percentage >= 90.0:
        return "EXCELLENT"  # Elite accuracy
    elif fg_percentage >= 85.0:
        return "GOOD"       # Reliable
    elif fg_percentage >= 80.0:
        return "AVERAGE"    # Standard
    else:
        return "POOR"       # Unreliable
```

### Thresholds & Tiers

**Kicker FG Accuracy:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥90% FG accuracy | Elite accuracy, minimal misses | 1.03 | Justin Tucker, Harrison Butker |
| GOOD | 85-89% FG accuracy | Reliable accuracy | 1.015 | Jake Elliott, Tyler Bass |
| AVERAGE | 80-84% FG accuracy | Standard accuracy | 1.0 | Most starting kickers |
| POOR | <80% FG accuracy | Unreliable, frequent misses | 0.985 | Struggling kickers |

**Note:** Requires minimum 10 FG attempts for reliable classification.

### Edge Cases

**1. Low Volume Kicker**
- **Scenario:** Kicker with only 8 FG attempts (below 10 minimum threshold)
- **Handling:** Classified as "INSUFFICIENT_DATA" tier, returns 1.0 multiplier
- **Example:** Kicker on low-scoring offense with few opportunities

**2. Perfect Accuracy with Low Volume**
- **Scenario:** Kicker with 12/12 FG (100%) but only 12 attempts all season
- **Handling:** Classified as EXCELLENT despite low sample size
- **Example:** May not be sustainable but currently performing at elite level

**3. Extra Point Misses**
- **Scenario:** Kicker misses multiple extra points (unusual)
- **Handling:** Currently not factored into tier (FG% only), but captured in metrics
- **Example:** Could add XP% penalty in future if needed

**4. Long-Distance Specialist**
- **Scenario:** Kicker with lower FG% due to high percentage of 50+ yard attempts
- **Handling:** Metric doesn't account for distance - treats all FG equally
- **Example:** This is a limitation since we don't have distance data

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**File:** `league_helper/util/KickerAccuracyCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class KickerAccuracyCalculator:
    """Calculate kicker field goal and extra point accuracy"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate kicker accuracy and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'K':
            return 1.0, "N/A"

        # Calculate accuracy metrics
        metrics = self._calculate_accuracy_metrics(player)

        # Get multiplier from config
        multiplier = self.config.get_kicker_accuracy_multiplier(metrics['tier'])

        self.logger.debug(
            f"K {player.name}: {metrics['fg_percentage']:.1f}% FG "
            f"({metrics['fg_made']}/{metrics['fg_attempted']}) "
            f"(Tier: {metrics['tier']}, Multiplier: {multiplier:.3f})"
        )

        return multiplier, metrics['tier']

    def _calculate_accuracy_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate accuracy metrics for a kicker"""
        fg_made_weekly = player.stats.get('field_goals', {}).get('made', [])
        fg_missed_weekly = player.stats.get('field_goals', {}).get('missed', [])
        xp_made_weekly = player.stats.get('extra_points', {}).get('made', [])
        xp_missed_weekly = player.stats.get('extra_points', {}).get('missed', [])

        if not fg_made_weekly:
            return {
                'fg_percentage': 0.0,
                'xp_percentage': 0.0,
                'fg_made': 0,
                'fg_attempted': 0,
                'xp_made': 0,
                'xp_attempted': 0,
                'tier': 'N/A'
            }

        # Calculate season totals
        fg_made = sum(fg_made_weekly)
        fg_missed = sum(fg_missed_weekly)
        xp_made = sum(xp_made_weekly)
        xp_missed = sum(xp_missed_weekly)

        fg_attempted = fg_made + fg_missed
        xp_attempted = xp_made + xp_missed

        # Calculate percentages
        fg_percentage = (fg_made / fg_attempted * 100) if fg_attempted > 0 else 0.0
        xp_percentage = (xp_made / xp_attempted * 100) if xp_attempted > 0 else 0.0

        # Determine tier
        tier = self._classify_tier(fg_percentage, fg_attempted)

        return {
            'fg_percentage': round(fg_percentage, 1),
            'xp_percentage': round(xp_percentage, 1),
            'fg_made': int(fg_made),
            'fg_attempted': int(fg_attempted),
            'xp_made': int(xp_made),
            'xp_attempted': int(xp_attempted),
            'tier': tier
        }

    def _classify_tier(self, fg_percentage: float, fg_attempted: int) -> str:
        """Classify kicker tier based on FG accuracy"""
        thresholds = self.config.kicker_accuracy_scoring.get('THRESHOLDS', {})
        min_attempts = self.config.kicker_accuracy_scoring.get('MIN_ATTEMPTS', 10)

        if fg_attempted < min_attempts:
            return "INSUFFICIENT_DATA"

        if fg_percentage >= thresholds.get('EXCELLENT', 90.0):
            return "EXCELLENT"
        elif fg_percentage >= thresholds.get('GOOD', 85.0):
            return "GOOD"
        elif fg_percentage >= thresholds.get('AVERAGE', 80.0):
            return "AVERAGE"
        else:
            return "POOR"
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "KICKER_ACCURACY_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 90.0,
      "GOOD": 85.0,
      "AVERAGE": 80.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.03,
      "GOOD": 1.015,
      "AVERAGE": 1.0,
      "POOR": 0.985,
      "INSUFFICIENT_DATA": 1.0
    },
    "WEIGHT": 1.5,
    "MIN_ATTEMPTS": 10,
    "DESCRIPTION": "Kicker field goal accuracy - reliability metric"
  }
}
```

**2.2 Add ConfigManager method**

```python
def get_kicker_accuracy_multiplier(self, tier: str) -> float:
    """
    Get kicker accuracy multiplier for reliability tier.

    Args:
        tier: Tier classification (EXCELLENT, GOOD, AVERAGE, POOR, INSUFFICIENT_DATA)

    Returns:
        float: Multiplier value
    """
    multipliers = self.config.get('KICKER_ACCURACY_SCORING', {}).get('MULTIPLIERS', {})
    return multipliers.get(tier, 1.0)
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_kicker_accuracy_scoring()`

```python
def _apply_kicker_accuracy_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply kicker accuracy adjustment (K only)"""
    if p.position != 'K':
        return player_score, ""

    if not self.config.kicker_accuracy_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = KickerAccuracyCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    # Apply multiplier with weight
    weight = self.config.kicker_accuracy_scoring.get('WEIGHT', 1.5)
    adjusted_score = player_score * (multiplier ** weight)

    # Get metrics for reason string
    metrics = calculator._calculate_accuracy_metrics(p)
    reason = f"K Accuracy ({tier}): {metrics['fg_percentage']:.1f}% FG ({metrics['fg_made']}/{metrics['fg_attempted']})"

    return adjusted_score, reason
```

**Integration in `calculate_total_score()`:**

```python
# After existing scoring steps
player_score, reason = self._apply_kicker_accuracy_scoring(p, player_score)
if reason:
    score_reasons.append(reason)
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_KickerAccuracyCalculator.py`

```python
import pytest
from league_helper.util.KickerAccuracyCalculator import KickerAccuracyCalculator
from league_helper.util.FantasyPlayer import FantasyPlayer
from league_helper.util.ConfigManager import ConfigManager

class TestKickerAccuracyCalculator:
    """Test Kicker Accuracy Calculator functionality"""

    @pytest.fixture
    def calculator(self, tmp_path):
        """Create calculator with test config"""
        config = ConfigManager(tmp_path)
        return KickerAccuracyCalculator(config)

    def test_elite_accuracy_kicker(self, calculator):
        """Test kicker with 90%+ FG accuracy"""
        player = FantasyPlayer(
            name="Justin Tucker",
            position="K",
            stats={
                'field_goals': {
                    'made': [3, 2, 4, 0, 2, 3, 2, 3, 2, 4, 3, 2, 3, 2],  # 36 made
                    'missed': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]  # 3 missed
                },
                'extra_points': {
                    'made': [5, 4, 6, 0, 3, 5, 4, 6, 5, 7, 5, 4, 5, 3],
                    'missed': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        )

        metrics = calculator._calculate_accuracy_metrics(player)

        assert metrics['fg_made'] == 36
        assert metrics['fg_attempted'] == 39
        assert metrics['fg_percentage'] >= 90.0
        assert metrics['tier'] == "EXCELLENT"

    def test_unreliable_kicker(self, calculator):
        """Test kicker with <80% FG accuracy"""
        player = FantasyPlayer(
            name="Struggling Kicker",
            position="K",
            stats={
                'field_goals': {
                    'made': [2, 1, 1, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],  # 19 made
                    'missed': [1, 1, 2, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1]  # 10 missed
                },
                'extra_points': {
                    'made': [3, 2, 3, 0, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                    'missed': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                }
            }
        )

        metrics = calculator._calculate_accuracy_metrics(player)

        assert metrics['fg_attempted'] == 29
        fg_pct = (19 / 29) * 100
        assert metrics['fg_percentage'] == pytest.approx(fg_pct, abs=0.1)
        assert metrics['tier'] == "POOR"

    def test_insufficient_attempts(self, calculator):
        """Test kicker with <10 FG attempts"""
        player = FantasyPlayer(
            name="Low Volume Kicker",
            position="K",
            stats={
                'field_goals': {
                    'made': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],  # 5 made
                    'missed': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 0 missed
                },
                'extra_points': {
                    'made': [2, 1, 2, 0, 2, 1, 2, 1, 2, 1, 0, 0, 0, 0],
                    'missed': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        )

        metrics = calculator._calculate_accuracy_metrics(player)

        assert metrics['fg_attempted'] < 10
        assert metrics['tier'] == "INSUFFICIENT_DATA"

    def test_non_kicker_returns_neutral(self, calculator):
        """Test that non-K positions return 1.0 multiplier"""
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

**File:** `docs/scoring/15_kicker_accuracy_scoring.md`

```markdown
# Step 15: Kicker Accuracy (Reliability Metric)

**Priority:** HIGH | **Positions:** K | **Pattern:** Multiplier-based

## Overview

Kicker Accuracy measures field goal percentage to identify reliable kickers (90%+) who provide consistent weekly floors and minimize boom/bust variance.

## Formula

```
fg_percentage = (fg_made / (fg_made + fg_missed)) * 100
```

## Thresholds

- EXCELLENT: ≥90% FG accuracy (+3% bonus)
- GOOD: 85-89% FG accuracy (+1.5% bonus)
- AVERAGE: 80-84% FG accuracy (no adjustment)
- POOR: <80% FG accuracy (-1.5% penalty)
- INSUFFICIENT_DATA: <10 FG attempts (no adjustment)

## Example

**Justin Tucker (BAL, K)**
- FG made: 36
- FG attempted: 39
- FG percentage: 92.3%
- Tier: EXCELLENT
- Multiplier: 1.03^1.5 = 1.0452
- Impact: +4.52% to base score

## Why This Matters

High-accuracy kickers provide consistent weekly floors and avoid negative points from missed kicks. Combined with high attempt volume, accuracy creates elite fantasy kickers.

## Limitations

This metric uses overall FG percentage without distance breakdown (no data for 0-39, 40-49, 50+ yard ranges). Long-distance specialists may be undervalued.
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 8-12%
- Rationale: Identifies reliable kickers for late-round draft picks

**Starter Helper Mode:**
- Expected improvement: 6-10%
- Rationale: Consistent kickers provide stable weekly floors

**Trade Simulator Mode:**
- Expected improvement: 5-8%
- Rationale: Separates reliable kickers from boom/bust options

---

## Real-World Examples

### Example 1: Elite Accuracy Kicker

**Justin Tucker (BAL, K)** - 2024 Season:

| Metric | Value |
|--------|-------|
| FG Made | 36 |
| FG Attempted | 39 |
| FG Percentage | 92.3% |
| XP Made | 62 |
| XP Attempted | 62 |
| Tier | EXCELLENT |
| Multiplier | 1.03^1.5 = 1.0452 |
| Base Score | 155.0 |
| Adjusted Score | 162.0 (+7.0 pts) |

**Reason String:** `"K Accuracy (EXCELLENT): 92.3% FG (36/39)"`

### Example 2: Unreliable Kicker

**Struggling Kicker (Team, K)** - Low Accuracy:

| Metric | Value |
|--------|-------|
| FG Made | 19 |
| FG Attempted | 29 |
| FG Percentage | 65.5% |
| Tier | POOR |
| Multiplier | 0.985^1.5 = 0.9777 |
| Base Score | 120.0 |
| Adjusted Score | 117.3 (-2.7 pts) |

**Reason String:** `"K Accuracy (POOR): 65.5% FG (19/29)"`

---

## Dependencies

### Data Dependencies
- ✅ `field_goals.made` - Available in `data/player_data/k_data.json`
- ✅ `field_goals.missed` - Available in `data/player_data/k_data.json`
- ✅ `extra_points.made` - Available in `data/player_data/k_data.json`
- ✅ `extra_points.missed` - Available in `data/player_data/k_data.json`

### Code Dependencies
- 🆕 `KickerAccuracyCalculator` - To be created
- ✅ `ConfigManager` - Existing, needs new method

---

## Risks & Mitigations

### Risk 1: No Distance Breakdown
- **Issue:** Long-distance specialists penalized for lower FG% on harder kicks
- **Mitigation:** Accept limitation since distance data not available
- **Severity:** Medium (could undervalue elite long-distance kickers)

### Risk 2: Low Sample Size
- **Issue:** Kickers with <10 attempts may have unreliable accuracy percentages
- **Mitigation:** Add MIN_ATTEMPTS threshold (10 FG minimum) to config
- **Severity:** Low (handled by INSUFFICIENT_DATA tier)

### Risk 3: Extra Point Misses Not Factored
- **Issue:** Kicker with poor XP% but good FG% may be overvalued
- **Mitigation:** Could add XP% component in future if needed
- **Severity:** Low (XP misses are rare)

---

## Implementation Checklist

**Phase 1: Data Pipeline**
- [ ] `KickerAccuracyCalculator.py` created
- [ ] `calculate()` method implemented
- [ ] `_calculate_accuracy_metrics()` helper created
- [ ] `_classify_tier()` helper created

**Phase 2: Configuration**
- [ ] `KICKER_ACCURACY_SCORING` section added to `league_config.json`
- [ ] `get_kicker_accuracy_multiplier()` method added to ConfigManager

**Phase 3: Scoring Integration**
- [ ] `_apply_kicker_accuracy_scoring()` method added to `player_scoring.py`
- [ ] Integration point added to `calculate_total_score()`

**Phase 4: Testing**
- [ ] `test_KickerAccuracyCalculator.py` created
- [ ] Test elite accuracy kicker (90%+ FG)
- [ ] Test unreliable kicker (<80% FG)
- [ ] Test insufficient attempts (<10 FG)
- [ ] Test non-kicker returns neutral
- [ ] All tests passing (100% pass rate)

**Phase 5: Documentation**
- [ ] `15_kicker_accuracy_scoring.md` created
- [ ] README.md updated with Step 15
- [ ] Checklist marked complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add kicker accuracy scoring (M05)"

---

**END OF FEATURE REQUEST**
