# Feature Request: Completion Percentage (QB Efficiency)

**Metric ID:** M06
**Priority:** MEDIUM
**Positions:** QB
**Effort Estimate:** 2-3 hours
**Expected Impact:** 8-12% improvement in QB efficiency evaluation

---

## What This Metric Is

Completion Percentage measures a quarterback's passing efficiency by calculating the percentage of pass attempts that result in completions. High completion percentage (70%+) indicates QB accuracy, game control, and consistent offensive production.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify accurate QBs**: 70%+ completion rate indicates elite accuracy and game control
- **Predict consistency**: High completion % reduces boom/bust variance - more stable weekly floors
- **Offensive system indicator**: High completion % often indicates short passing game, high volume
- **Risk assessment**: Low completion % (<60%) indicates risky deep passing or struggling QB
- **Draft strategy**: Target high-completion QBs for PPR-style consistency

**Example Use Case:**
> Tua Tagovailoa with 69% completion percentage completes 28 of 40 passes per game, generating 280+ yards consistently. A QB with 58% completion only completes 23 of 40, leading to lower yardage floors despite similar attempt volume.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/qb_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `passing.completions` | float | Yes (17 weeks) | QB JSON | 28.0 |
| `passing.attempts` | float | Yes (17 weeks) | QB JSON | 42.0 |
| `position` | string | No | All player JSON | "QB" |

**Example Data Structure:**
```json
{
  "id": "4361741",
  "name": "Tua Tagovailoa",
  "team": "MIA",
  "position": "QB",
  "passing": {
    "completions": [28.0, 25.0, 31.0, 0.0, 26.0, 29.0, 27.0, 30.0, 28.0, 29.0, 27.0, 31.0, 26.0, 30.0],
    "attempts": [42.0, 37.0, 46.0, 0.0, 39.0, 44.0, 36.0, 41.0, 38.0, 40.0, 39.0, 42.0, 37.0, 43.0]
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
def calculate_completion_percentage(player: FantasyPlayer) -> dict:
    """
    Calculate QB completion percentage.

    Args:
        player: FantasyPlayer object with passing stats

    Returns:
        dict: {
            'completion_pct': float,
            'total_completions': int,
            'total_attempts': int,
            'tier': str
        }

    Example:
        >>> player = FantasyPlayer(name="Tua Tagovailoa", position="QB", stats={...})
        >>> result = calculate_completion_percentage(player)
        >>> result
        {'completion_pct': 69.3, 'total_completions': 388, 'total_attempts': 560, 'tier': 'GOOD'}
    """
    if player.position != 'QB':
        return {
            'completion_pct': 0.0,
            'total_completions': 0,
            'total_attempts': 0,
            'tier': 'N/A'
        }

    # Step 1: Get passing stats
    weekly_completions = player.stats['passing']['completions']
    weekly_attempts = player.stats['passing']['attempts']

    # Step 2: Calculate season totals
    total_completions = sum(weekly_completions)
    total_attempts = sum(weekly_attempts)

    # Step 3: Calculate completion percentage
    if total_attempts > 0:
        completion_pct = (total_completions / total_attempts) * 100
    else:
        completion_pct = 0.0

    # Step 4: Determine tier
    tier = _classify_completion_tier(completion_pct, total_attempts)

    return {
        'completion_pct': round(completion_pct, 1),
        'total_completions': int(total_completions),
        'total_attempts': int(total_attempts),
        'tier': tier
    }

def _classify_completion_tier(completion_pct: float, total_attempts: int) -> str:
    """
    Classify QB tier based on completion percentage.

    Args:
        completion_pct: Completion percentage
        total_attempts: Minimum attempts required for reliable sample

    Returns:
        str: Tier classification
    """
    # Require minimum 100 attempts for reliable completion % measurement
    if total_attempts < 100:
        return "INSUFFICIENT_DATA"

    if completion_pct >= 70.0:
        return "EXCELLENT"  # Elite accuracy
    elif completion_pct >= 65.0:
        return "GOOD"       # Above average
    elif completion_pct >= 60.0:
        return "AVERAGE"    # Standard
    else:
        return "POOR"       # Struggling accuracy
```

### Thresholds & Tiers

**QB Completion Percentage:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥70% completion | Elite accuracy, consistent | 1.03 | Tua Tagovailoa, Brock Purdy |
| GOOD | 65-69% completion | Above average accuracy | 1.015 | Patrick Mahomes, Jalen Hurts |
| AVERAGE | 60-64% completion | Standard accuracy | 1.0 | Most starting QBs |
| POOR | <60% completion | Struggling accuracy | 0.985 | Deep passing or struggling QBs |

**Note:** Requires minimum 100 pass attempts for reliable classification.

### Edge Cases

**1. Short Passing Game vs Deep Passing**
- **Scenario:** QB with 72% completion (short passes) vs QB with 58% completion (deep passes)
- **Handling:** Metric favors short passing game - deep passers penalized despite higher yards/attempt
- **Example:** Tua (short passes) rated higher than Justin Fields (deep passes)

**2. Checkdown Heavy QB**
- **Scenario:** QB with 75% completion but low yards/attempt (checkdowns)
- **Handling:** Metric rewards completion regardless of depth - yardage captured elsewhere
- **Example:** High completion % QB may still have low fantasy value if no TDs/yards

**3. Weather Conditions**
- **Scenario:** QB in cold/windy climate with lower completion % due to conditions
- **Handling:** No weather adjustment - season-long average smooths outliers
- **Example:** Buffalo QBs may have slightly lower completion % in December games

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**File:** `league_helper/util/CompletionPercentageCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class CompletionPercentageCalculator:
    """Calculate QB completion percentage efficiency"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate completion percentage and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'QB':
            return 1.0, "N/A"

        # Calculate completion metrics
        metrics = self._calculate_completion_metrics(player)

        # Get multiplier from config
        multiplier = self.config.get_completion_pct_multiplier(metrics['tier'])

        self.logger.debug(
            f"QB {player.name}: {metrics['completion_pct']:.1f}% completion "
            f"({metrics['total_completions']}/{metrics['total_attempts']}) "
            f"(Tier: {metrics['tier']}, Multiplier: {multiplier:.3f})"
        )

        return multiplier, metrics['tier']

    def _calculate_completion_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate completion percentage metrics for a QB"""
        weekly_completions = player.stats.get('passing', {}).get('completions', [])
        weekly_attempts = player.stats.get('passing', {}).get('attempts', [])

        if not weekly_completions or not weekly_attempts:
            return {
                'completion_pct': 0.0,
                'total_completions': 0,
                'total_attempts': 0,
                'tier': 'N/A'
            }

        total_completions = sum(weekly_completions)
        total_attempts = sum(weekly_attempts)

        completion_pct = (total_completions / total_attempts * 100) if total_attempts > 0 else 0.0

        tier = self._classify_tier(completion_pct, total_attempts)

        return {
            'completion_pct': round(completion_pct, 1),
            'total_completions': int(total_completions),
            'total_attempts': int(total_attempts),
            'tier': tier
        }

    def _classify_tier(self, completion_pct: float, total_attempts: int) -> str:
        """Classify QB tier based on completion percentage"""
        thresholds = self.config.completion_pct_scoring.get('THRESHOLDS', {})
        min_attempts = self.config.completion_pct_scoring.get('MIN_ATTEMPTS', 100)

        if total_attempts < min_attempts:
            return "INSUFFICIENT_DATA"

        if completion_pct >= thresholds.get('EXCELLENT', 70.0):
            return "EXCELLENT"
        elif completion_pct >= thresholds.get('GOOD', 65.0):
            return "GOOD"
        elif completion_pct >= thresholds.get('AVERAGE', 60.0):
            return "AVERAGE"
        else:
            return "POOR"
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "COMPLETION_PCT_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 70.0,
      "GOOD": 65.0,
      "AVERAGE": 60.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.03,
      "GOOD": 1.015,
      "AVERAGE": 1.0,
      "POOR": 0.985,
      "INSUFFICIENT_DATA": 1.0
    },
    "WEIGHT": 1.5,
    "MIN_ATTEMPTS": 100,
    "DESCRIPTION": "QB completion percentage - accuracy and consistency"
  }
}
```

**2.2 Add ConfigManager method**

```python
def get_completion_pct_multiplier(self, tier: str) -> float:
    """
    Get completion percentage multiplier for QB accuracy tier.

    Args:
        tier: Tier classification (EXCELLENT, GOOD, AVERAGE, POOR, INSUFFICIENT_DATA)

    Returns:
        float: Multiplier value
    """
    multipliers = self.config.get('COMPLETION_PCT_SCORING', {}).get('MULTIPLIERS', {})
    return multipliers.get(tier, 1.0)
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_completion_pct_scoring()`

```python
def _apply_completion_pct_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply completion percentage adjustment (QB only)"""
    if p.position != 'QB':
        return player_score, ""

    if not self.config.completion_pct_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = CompletionPercentageCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    # Apply multiplier with weight
    weight = self.config.completion_pct_scoring.get('WEIGHT', 1.5)
    adjusted_score = player_score * (multiplier ** weight)

    # Get metrics for reason string
    metrics = calculator._calculate_completion_metrics(p)
    reason = f"Completion% ({tier}): {metrics['completion_pct']:.1f}%"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_CompletionPercentageCalculator.py`

```python
import pytest
from league_helper.util.CompletionPercentageCalculator import CompletionPercentageCalculator
from league_helper.util.FantasyPlayer import FantasyPlayer
from league_helper.util.ConfigManager import ConfigManager

class TestCompletionPercentageCalculator:
    """Test Completion Percentage Calculator functionality"""

    @pytest.fixture
    def calculator(self, tmp_path):
        """Create calculator with test config"""
        config = ConfigManager(tmp_path)
        return CompletionPercentageCalculator(config)

    def test_elite_accuracy_qb(self, calculator):
        """Test QB with 70%+ completion percentage"""
        player = FantasyPlayer(
            name="Tua Tagovailoa",
            position="QB",
            stats={
                'passing': {
                    'completions': [28, 25, 31, 0, 26, 29, 27, 30, 28, 29, 27, 31, 26, 30],
                    'attempts': [42, 37, 46, 0, 39, 44, 36, 41, 38, 40, 39, 42, 37, 43]
                }
            }
        )

        metrics = calculator._calculate_completion_metrics(player)

        assert metrics['total_completions'] == 367
        assert metrics['total_attempts'] == 524
        comp_pct = (367 / 524) * 100
        assert metrics['completion_pct'] == pytest.approx(comp_pct, abs=0.1)
        assert metrics['tier'] == "EXCELLENT"

    def test_low_accuracy_qb(self, calculator):
        """Test QB with <60% completion percentage"""
        player = FantasyPlayer(
            name="Deep Ball QB",
            position="QB",
            stats={
                'passing': {
                    'completions': [18, 15, 20, 0, 17, 19, 16, 18, 17, 19, 16, 20, 15, 19],
                    'attempts': [35, 30, 38, 0, 32, 36, 30, 34, 32, 35, 31, 37, 29, 36]
                }
            }
        )

        metrics = calculator._calculate_completion_metrics(player)
        comp_pct = (metrics['total_completions'] / metrics['total_attempts']) * 100

        assert comp_pct < 60.0
        assert metrics['tier'] == "POOR"

    def test_insufficient_attempts(self, calculator):
        """Test QB with <100 pass attempts"""
        player = FantasyPlayer(
            name="Backup QB",
            position="QB",
            stats={
                'passing': {
                    'completions': [15, 12, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'attempts': [25, 20, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        )

        metrics = calculator._calculate_completion_metrics(player)

        assert metrics['total_attempts'] < 100
        assert metrics['tier'] == "INSUFFICIENT_DATA"

    def test_non_qb_returns_neutral(self, calculator):
        """Test that non-QB positions return 1.0 multiplier"""
        player = FantasyPlayer(
            name="Christian McCaffrey",
            position="RB",
            stats={'rushing': {'attempts': [20, 18, 22]}}
        )

        multiplier, tier = calculator.calculate(player)

        assert multiplier == 1.0
        assert tier == "N/A"
```

---

### Phase 5: Documentation (Estimated: 30 min)

**File:** `docs/scoring/16_completion_percentage_scoring.md`

```markdown
# Step 16: Completion Percentage (QB Efficiency)

**Priority:** MEDIUM | **Positions:** QB | **Pattern:** Multiplier-based

## Overview

Completion Percentage measures QB passing accuracy, identifying efficient passers (70%+) who provide consistent weekly production through high completion rates.

## Formula

```
completion_pct = (total_completions / total_attempts) * 100
```

## Thresholds

- EXCELLENT: ≥70% completion (+3% bonus)
- GOOD: 65-69% completion (+1.5% bonus)
- AVERAGE: 60-64% completion (no adjustment)
- POOR: <60% completion (-1.5% penalty)
- INSUFFICIENT_DATA: <100 attempts (no adjustment)

## Example

**Tua Tagovailoa (MIA, QB)**
- Completions: 388
- Attempts: 560
- Completion %: 69.3%
- Tier: GOOD
- Multiplier: 1.015^1.5 = 1.0226
- Impact: +2.26% to base score

## Why This Matters

High completion percentage indicates QB accuracy and game control, leading to more consistent yardage production and reduced boom/bust variance.

## Note

This metric favors short passing games over deep passing systems. Deep ball specialists may be penalized despite higher yards per attempt.
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 8-12%
- Rationale: Identifies accurate QBs for consistent weekly production

**Starter Helper Mode:**
- Expected improvement: 10-14%
- Rationale: High completion % QBs have more predictable weekly floors

**Trade Simulator Mode:**
- Expected improvement: 6-10%
- Rationale: Separates efficient passers from boom/bust deep ball QBs

---

## Real-World Examples

### Example 1: Elite Accuracy QB

**Tua Tagovailoa (MIA, QB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Total Completions | 388 |
| Total Attempts | 560 |
| Completion % | 69.3% |
| Tier | GOOD |
| Multiplier | 1.015^1.5 = 1.0226 |
| Base Score | 275.0 |
| Adjusted Score | 281.2 (+6.2 pts) |

**Reason String:** `"Completion% (GOOD): 69.3%"`

### Example 2: Low Accuracy QB

**Deep Ball QB (Team, QB)** - Struggling:

| Metric | Value |
|--------|-------|
| Total Completions | 229 |
| Total Attempts | 405 |
| Completion % | 56.5% |
| Tier | POOR |
| Multiplier | 0.985^1.5 = 0.9777 |
| Base Score | 245.0 |
| Adjusted Score | 239.5 (-5.5 pts) |

**Reason String:** `"Completion% (POOR): 56.5%"`

---

## Dependencies

### Data Dependencies
- ✅ `passing.completions` - Available in `data/player_data/qb_data.json`
- ✅ `passing.attempts` - Available in `data/player_data/qb_data.json`

### Code Dependencies
- 🆕 `CompletionPercentageCalculator` - To be created
- ✅ `ConfigManager` - Existing, needs new method

---

## Risks & Mitigations

### Risk 1: Favors Short Passing Over Deep Passing
- **Issue:** Short passing QBs rated higher than deep ball specialists
- **Mitigation:** Accept as design choice - completion % measures efficiency not style
- **Severity:** Low (complemented by yards/attempt metrics elsewhere)

### Risk 2: Checkdown Heavy QBs Overvalued
- **Issue:** QBs with high completion % but low depth may be overvalued
- **Mitigation:** Fantasy points come from volume - checkdowns still valuable
- **Severity:** Low

---

## Implementation Checklist

**Phase 1: Data Pipeline**
- [ ] `CompletionPercentageCalculator.py` created
- [ ] `calculate()` method implemented
- [ ] `_calculate_completion_metrics()` helper created
- [ ] `_classify_tier()` helper created

**Phase 2: Configuration**
- [ ] `COMPLETION_PCT_SCORING` section added to `league_config.json`
- [ ] `get_completion_pct_multiplier()` method added to ConfigManager

**Phase 3: Scoring Integration**
- [ ] `_apply_completion_pct_scoring()` method added to `player_scoring.py`
- [ ] Integration point added to `calculate_total_score()`

**Phase 4: Testing**
- [ ] `test_CompletionPercentageCalculator.py` created
- [ ] Test elite accuracy QB (70%+ completion)
- [ ] Test low accuracy QB (<60% completion)
- [ ] Test insufficient attempts (<100 attempts)
- [ ] Test non-QB returns neutral
- [ ] All tests passing (100% pass rate)

**Phase 5: Documentation**
- [ ] `16_completion_percentage_scoring.md` created
- [ ] README.md updated with Step 16
- [ ] Checklist marked complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add completion percentage scoring (M06)"

---

**END OF FEATURE REQUEST**
