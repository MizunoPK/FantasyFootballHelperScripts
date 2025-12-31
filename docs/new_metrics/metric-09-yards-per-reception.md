# Feature Request: Yards Per Reception (WR/TE Deep Threat Metric)

**Metric ID:** M09
**Priority:** MEDIUM
**Positions:** WR, TE
**Effort Estimate:** 3-4 hours
**Expected Impact:** 10-14% improvement in WR/TE boom/bust assessment

---

## What This Metric Is

Yards Per Reception (YPR) measures the average yards gained per reception for wide receivers and tight ends, identifying deep threats (15+ YPR for WR) versus underneath possession receivers (9-12 YPR). High YPR indicates boom potential and explosive play ability, while low YPR signals volume-based consistency.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify deep threat WRs**: 15+ YPR WRs (Tyreek Hill, DK Metcalf) have elite boom potential and TD probability
- **Separate WR archetypes**: Deep threats vs possession receivers vs slot receivers
- **Predict boom/bust variance**: High YPR = higher ceiling but lower floor (big play dependent)
- **TE separation**: 12+ YPR TEs (George Kittle, Kyle Pitts) provide elite upside at position
- **Draft strategy**: Target deep threats in pass-heavy offenses for ceiling, possession receivers for floor

**Example Use Case:**
> Tyreek Hill with 16.2 YPR on 8 receptions = 130 yards per game. A possession receiver with 10.5 YPR on 8 receptions = 84 yards. The 5.7 yard difference per catch translates to 45+ extra yards and 0.5-1.0 additional TDs per week through explosive plays.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/wr_data.json`, `data/player_data/te_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `receiving.receiving_yds` | float | Yes (17 weeks) | WR/TE JSON | 124.0 |
| `receiving.receptions` | float | Yes (17 weeks) | WR/TE JSON | 8.0 |
| `position` | string | No | All player JSON | "WR" or "TE" |

**Example Data Structure (WR):**
```json
{
  "id": "3116406",
  "name": "Tyreek Hill",
  "team": "MIA",
  "position": "WR",
  "receiving": {
    "receiving_yds": [124.0, 103.0, 156.0, 0.0, 118.0, 142.0, 95.0, 138.0, 112.0, 148.0, 106.0, 134.0, 98.0, 128.0],
    "receptions": [8.0, 7.0, 10.0, 0.0, 7.0, 9.0, 6.0, 9.0, 7.0, 10.0, 7.0, 9.0, 6.0, 8.0]
  }
}
```

**Example Data Structure (TE):**
```json
{
  "id": "3116593",
  "name": "George Kittle",
  "team": "SF",
  "position": "TE",
  "receiving": {
    "receiving_yds": [88.0, 72.0, 105.0, 0.0, 85.0, 94.0, 68.0, 98.0, 76.0, 102.0, 82.0, 91.0, 70.0, 86.0],
    "receptions": [7.0, 6.0, 9.0, 0.0, 7.0, 8.0, 5.0, 8.0, 6.0, 9.0, 7.0, 8.0, 5.0, 7.0]
  }
}
```

### Data Validation
- ✅ Data verified in: `data/player_data/wr_data.json`, `data/player_data/te_data.json`
- ✅ Weekly granularity: Yes (17 weeks per season)
- ✅ Historical availability: Current season
- ⚠️ Known limitations: None

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_yards_per_reception(player: FantasyPlayer) -> dict:
    """
    Calculate yards per reception for WR/TE.

    Args:
        player: FantasyPlayer object with receiving stats

    Returns:
        dict: {
            'yards_per_reception': float,
            'total_receiving_yds': int,
            'total_receptions': int,
            'tier': str
        }

    Example:
        >>> player = FantasyPlayer(name="Tyreek Hill", position="WR", stats={...})
        >>> result = calculate_yards_per_reception(player)
        >>> result
        {'yards_per_reception': 16.2, 'total_receiving_yds': 1620, 'total_receptions': 100, 'tier': 'EXCELLENT'}
    """
    if player.position not in ['WR', 'TE']:
        return {
            'yards_per_reception': 0.0,
            'total_receiving_yds': 0,
            'total_receptions': 0,
            'tier': 'N/A'
        }

    # Step 1: Get receiving stats
    weekly_yards = player.stats['receiving']['receiving_yds']
    weekly_receptions = player.stats['receiving']['receptions']

    # Step 2: Calculate season totals
    total_receiving_yds = sum(weekly_yards)
    total_receptions = sum(weekly_receptions)

    # Step 3: Calculate yards per reception
    if total_receptions > 0:
        yards_per_reception = total_receiving_yds / total_receptions
    else:
        yards_per_reception = 0.0

    # Step 4: Determine tier (position-specific thresholds)
    tier = _classify_ypr_tier(yards_per_reception, total_receptions, player.position)

    return {
        'yards_per_reception': round(yards_per_reception, 1),
        'total_receiving_yds': int(total_receiving_yds),
        'total_receptions': int(total_receptions),
        'tier': tier
    }

def _classify_ypr_tier(yards_per_reception: float, total_receptions: int, position: str) -> str:
    """
    Classify WR/TE tier based on yards per reception.

    Args:
        yards_per_reception: YPR average
        total_receptions: Minimum receptions required for reliable sample
        position: WR or TE (different thresholds)

    Returns:
        str: Tier classification
    """
    # Require minimum 30 receptions for reliable YPR measurement
    if total_receptions < 30:
        return "INSUFFICIENT_DATA"

    # Position-specific thresholds
    if position == 'WR':
        if yards_per_reception >= 15.0:
            return "EXCELLENT"  # Deep threat
        elif yards_per_reception >= 12.0:
            return "GOOD"       # Above average
        elif yards_per_reception >= 9.0:
            return "AVERAGE"    # Possession receiver
        else:
            return "POOR"       # Underneath/screens
    else:  # TE
        if yards_per_reception >= 12.0:
            return "EXCELLENT"  # Elite YAC/seam threat
        elif yards_per_reception >= 9.0:
            return "GOOD"       # Above average
        elif yards_per_reception >= 7.0:
            return "AVERAGE"    # Standard TE
        else:
            return "POOR"       # Short-area target
```

### Thresholds & Tiers

**WR Yards Per Reception:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥15.0 YPR | Deep threat, boom potential | 1.03 | Tyreek Hill, DK Metcalf |
| GOOD | 12.0-14.9 YPR | Above average | 1.015 | CeeDee Lamb, Amon-Ra St. Brown |
| AVERAGE | 9.0-11.9 YPR | Possession receiver | 1.0 | Tyler Lockett, Juju Smith-Schuster |
| POOR | <9.0 YPR | Underneath/screen specialist | 0.985 | Deebo Samuel (rush-focused) |

**TE Yards Per Reception:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥12.0 YPR | Elite seam threat | 1.03 | George Kittle, Kyle Pitts |
| GOOD | 9.0-11.9 YPR | Above average | 1.015 | Travis Kelce, Mark Andrews |
| AVERAGE | 7.0-8.9 YPR | Standard TE | 1.0 | Most starting TEs |
| POOR | <7.0 YPR | Short-area target | 0.985 | Blocking-focused TEs |

**Note:** Requires minimum 30 receptions for reliable classification.

### Edge Cases

**1. Low Volume Deep Threat**
- **Scenario:** WR with 18 YPR but only 25 receptions (below 30 minimum)
- **Handling:** Classified as "INSUFFICIENT_DATA" despite elite YPR
- **Example:** Complementary deep threat WR with limited targets

**2. High Volume Underneath Receiver**
- **Scenario:** WR with 8.5 YPR but 120 receptions (high PPR value)
- **Handling:** Gets POOR tier penalty but high fantasy value from volume
- **Example:** Slot receivers like Jarvis Landry archetype

**3. YAC Specialist**
- **Scenario:** WR with 14 YPR from screens and YAC, not deep routes
- **Handling:** No distinction - all receiving yards count equally
- **Example:** Deebo Samuel-type versatile weapons

**4. Big Play Dependency**
- **Scenario:** WR with 16 YPR but most yards from 3 big plays
- **Handling:** Season average smooths outliers - boom/bust captured in variance
- **Example:** High YPR with inconsistent weekly production

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1.5 hours)

**File:** `league_helper/util/YardsPerReceptionCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class YardsPerReceptionCalculator:
    """Calculate WR/TE yards per reception efficiency"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate yards per reception and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position not in ['WR', 'TE']:
            return 1.0, "N/A"

        # Calculate YPR metrics
        metrics = self._calculate_ypr_metrics(player)

        # Get multiplier from config
        multiplier = self.config.get_yards_per_reception_multiplier(metrics['tier'])

        self.logger.debug(
            f"{player.position} {player.name}: {metrics['yards_per_reception']:.1f} YPR "
            f"({metrics['total_receiving_yds']} yds / {metrics['total_receptions']} rec) "
            f"(Tier: {metrics['tier']}, Multiplier: {multiplier:.3f})"
        )

        return multiplier, metrics['tier']

    def _calculate_ypr_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate yards per reception metrics for WR/TE"""
        weekly_yards = player.stats.get('receiving', {}).get('receiving_yds', [])
        weekly_receptions = player.stats.get('receiving', {}).get('receptions', [])

        if not weekly_yards or not weekly_receptions:
            return {
                'yards_per_reception': 0.0,
                'total_receiving_yds': 0,
                'total_receptions': 0,
                'tier': 'N/A'
            }

        total_receiving_yds = sum(weekly_yards)
        total_receptions = sum(weekly_receptions)

        yards_per_reception = (total_receiving_yds / total_receptions) if total_receptions > 0 else 0.0

        tier = self._classify_tier(yards_per_reception, total_receptions, player.position)

        return {
            'yards_per_reception': round(yards_per_reception, 1),
            'total_receiving_yds': int(total_receiving_yds),
            'total_receptions': int(total_receptions),
            'tier': tier
        }

    def _classify_tier(self, yards_per_reception: float, total_receptions: int, position: str) -> str:
        """Classify WR/TE tier based on yards per reception"""
        min_receptions = self.config.yards_per_reception_scoring.get('MIN_RECEPTIONS', 30)

        if total_receptions < min_receptions:
            return "INSUFFICIENT_DATA"

        # Position-specific thresholds
        if position == 'WR':
            thresholds = self.config.yards_per_reception_scoring.get('THRESHOLDS_WR', {})
        else:  # TE
            thresholds = self.config.yards_per_reception_scoring.get('THRESHOLDS_TE', {})

        if yards_per_reception >= thresholds.get('EXCELLENT', 15.0 if position == 'WR' else 12.0):
            return "EXCELLENT"
        elif yards_per_reception >= thresholds.get('GOOD', 12.0 if position == 'WR' else 9.0):
            return "GOOD"
        elif yards_per_reception >= thresholds.get('AVERAGE', 9.0 if position == 'WR' else 7.0):
            return "AVERAGE"
        else:
            return "POOR"
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "YARDS_PER_RECEPTION_SCORING": {
    "ENABLED": true,
    "THRESHOLDS_WR": {
      "EXCELLENT": 15.0,
      "GOOD": 12.0,
      "AVERAGE": 9.0
    },
    "THRESHOLDS_TE": {
      "EXCELLENT": 12.0,
      "GOOD": 9.0,
      "AVERAGE": 7.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.03,
      "GOOD": 1.015,
      "AVERAGE": 1.0,
      "POOR": 0.985,
      "INSUFFICIENT_DATA": 1.0
    },
    "WEIGHT": 1.5,
    "MIN_RECEPTIONS": 30,
    "DESCRIPTION": "WR/TE yards per reception - deep threat vs possession receiver"
  }
}
```

**2.2 Add ConfigManager method**

```python
def get_yards_per_reception_multiplier(self, tier: str) -> float:
    """
    Get yards per reception multiplier for WR/TE efficiency tier.

    Args:
        tier: Tier classification (EXCELLENT, GOOD, AVERAGE, POOR, INSUFFICIENT_DATA)

    Returns:
        float: Multiplier value
    """
    multipliers = self.config.get('YARDS_PER_RECEPTION_SCORING', {}).get('MULTIPLIERS', {})
    return multipliers.get(tier, 1.0)
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_yards_per_reception_scoring()`

```python
def _apply_yards_per_reception_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply yards per reception adjustment (WR/TE only)"""
    if p.position not in ['WR', 'TE']:
        return player_score, ""

    if not self.config.yards_per_reception_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = YardsPerReceptionCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    # Apply multiplier with weight
    weight = self.config.yards_per_reception_scoring.get('WEIGHT', 1.5)
    adjusted_score = player_score * (multiplier ** weight)

    # Get metrics for reason string
    metrics = calculator._calculate_ypr_metrics(p)
    reason = f"YPR ({tier}): {metrics['yards_per_reception']:.1f}"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_YardsPerReceptionCalculator.py`

```python
import pytest
from league_helper.util.YardsPerReceptionCalculator import YardsPerReceptionCalculator
from league_helper.util.FantasyPlayer import FantasyPlayer
from league_helper.util.ConfigManager import ConfigManager

class TestYardsPerReceptionCalculator:
    """Test Yards Per Reception Calculator functionality"""

    @pytest.fixture
    def calculator(self, tmp_path):
        """Create calculator with test config"""
        config = ConfigManager(tmp_path)
        return YardsPerReceptionCalculator(config)

    def test_deep_threat_wr(self, calculator):
        """Test WR with 15.0+ YPR"""
        player = FantasyPlayer(
            name="Tyreek Hill",
            position="WR",
            stats={
                'receiving': {
                    'receiving_yds': [124, 103, 156, 0, 118, 142, 95, 138, 112, 148, 106, 134, 98, 128],
                    'receptions': [8, 7, 10, 0, 7, 9, 6, 9, 7, 10, 7, 9, 6, 8]
                }
            }
        )

        metrics = calculator._calculate_ypr_metrics(player)

        assert metrics['total_receiving_yds'] == 1602
        assert metrics['total_receptions'] == 103
        ypr = 1602 / 103
        assert metrics['yards_per_reception'] == pytest.approx(ypr, abs=0.1)
        assert metrics['tier'] == "EXCELLENT"

    def test_possession_wr(self, calculator):
        """Test WR with 9.0-11.9 YPR"""
        player = FantasyPlayer(
            name="Possession WR",
            position="WR",
            stats={
                'receiving': {
                    'receiving_yds': [82, 68, 95, 0, 76, 88, 71, 92, 79, 96, 74, 86, 68, 84],
                    'receptions': [8, 7, 10, 0, 7, 9, 6, 9, 7, 10, 7, 9, 6, 8]
                }
            }
        )

        metrics = calculator._calculate_ypr_metrics(player)
        ypr = metrics['total_receiving_yds'] / metrics['total_receptions']

        assert 9.0 <= ypr < 12.0
        assert metrics['tier'] == "AVERAGE"

    def test_elite_te(self, calculator):
        """Test TE with 12.0+ YPR"""
        player = FantasyPlayer(
            name="George Kittle",
            position="TE",
            stats={
                'receiving': {
                    'receiving_yds': [88, 72, 105, 0, 85, 94, 68, 98, 76, 102, 82, 91, 70, 86],
                    'receptions': [7, 6, 9, 0, 7, 8, 5, 8, 6, 9, 7, 8, 5, 7]
                }
            }
        )

        metrics = calculator._calculate_ypr_metrics(player)

        assert metrics['total_receiving_yds'] == 1117
        assert metrics['total_receptions'] == 92
        ypr = 1117 / 92
        assert ypr >= 12.0
        assert metrics['tier'] == "EXCELLENT"

    def test_insufficient_receptions(self, calculator):
        """Test WR with <30 receptions"""
        player = FantasyPlayer(
            name="Low Volume WR",
            position="WR",
            stats={
                'receiving': {
                    'receiving_yds': [42, 0, 55, 0, 38, 0, 48, 0, 0, 0, 0, 0, 0, 0],
                    'receptions': [3, 0, 4, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        )

        metrics = calculator._calculate_ypr_metrics(player)

        assert metrics['total_receptions'] < 30
        assert metrics['tier'] == "INSUFFICIENT_DATA"

    def test_non_wr_te_returns_neutral(self, calculator):
        """Test that non-WR/TE positions return 1.0 multiplier"""
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

**File:** `docs/scoring/19_yards_per_reception_scoring.md`

```markdown
# Step 19: Yards Per Reception (WR/TE Deep Threat Metric)

**Priority:** MEDIUM | **Positions:** WR, TE | **Pattern:** Multiplier-based

## Overview

Yards Per Reception measures receiving efficiency for WR/TE, identifying deep threats (15+ YPR for WR, 12+ for TE) who provide elite boom potential through explosive plays.

## Formula

```
yards_per_reception = total_receiving_yds / total_receptions
```

## Thresholds

**WR:**
- EXCELLENT: ≥15.0 YPR (+3% bonus)
- GOOD: 12.0-14.9 YPR (+1.5% bonus)
- AVERAGE: 9.0-11.9 YPR (no adjustment)
- POOR: <9.0 YPR (-1.5% penalty)

**TE:**
- EXCELLENT: ≥12.0 YPR (+3% bonus)
- GOOD: 9.0-11.9 YPR (+1.5% bonus)
- AVERAGE: 7.0-8.9 YPR (no adjustment)
- POOR: <7.0 YPR (-1.5% penalty)

**MIN_RECEPTIONS:** 30 receptions required

## Example

**Tyreek Hill (MIA, WR)**
- Receiving yards: 1,620
- Receptions: 100
- YPR: 16.2
- Tier: EXCELLENT
- Multiplier: 1.03^1.5 = 1.0452
- Impact: +4.52% to base score

## Why This Matters

High YPR indicates deep threat ability and explosive play potential, leading to higher TD probability and boom weeks. Position-specific thresholds account for different TE roles.
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 10-14%
- Rationale: Identifies deep threats vs possession receivers for roster construction

**Starter Helper Mode:**
- Expected improvement: 12-16%
- Rationale: High YPR players have higher boom potential for ceiling plays

**Trade Simulator Mode:**
- Expected improvement: 8-12%
- Rationale: Differentiates receiver archetypes for trade value

---

## Real-World Examples

### Example 1: Deep Threat WR

**Tyreek Hill (MIA, WR)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Receiving Yards | 1,620 |
| Receptions | 100 |
| YPR | 16.2 |
| Tier | EXCELLENT |
| Multiplier | 1.03^1.5 = 1.0452 |
| Base Score | 255.0 |
| Adjusted Score | 266.5 (+11.5 pts) |

**Reason String:** `"YPR (EXCELLENT): 16.2"`

### Example 2: Possession WR

**Possession WR (Team, WR)** - Volume-Based:

| Metric | Value |
|--------|-------|
| Receiving Yards | 1,059 |
| Receptions | 103 |
| YPR | 10.3 |
| Tier | AVERAGE |
| Multiplier | 1.0^1.5 = 1.0 |
| Base Score | 195.0 |
| Adjusted Score | 195.0 (no change) |

**Reason String:** `"YPR (AVERAGE): 10.3"`

### Example 3: Elite TE

**George Kittle (SF, TE)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Receiving Yards | 1,117 |
| Receptions | 92 |
| YPR | 12.1 |
| Tier | EXCELLENT |
| Multiplier | 1.03^1.5 = 1.0452 |
| Base Score | 185.0 |
| Adjusted Score | 193.4 (+8.4 pts) |

**Reason String:** `"YPR (EXCELLENT): 12.1"`

---

## Dependencies

### Data Dependencies
- ✅ `receiving.receiving_yds` - Available in `data/player_data/wr_data.json`, `data/player_data/te_data.json`
- ✅ `receiving.receptions` - Available in `data/player_data/wr_data.json`, `data/player_data/te_data.json`

### Code Dependencies
- 🆕 `YardsPerReceptionCalculator` - To be created
- ✅ `ConfigManager` - Existing, needs new method

---

## Risks & Mitigations

### Risk 1: Position-Specific Thresholds
- **Issue:** WR and TE have different YPR expectations
- **Mitigation:** Separate threshold configs for each position
- **Severity:** Low (handled by configuration)

### Risk 2: Low Volume Deep Threats
- **Issue:** Low volume WRs may have high YPR but limited fantasy value
- **Mitigation:** MIN_RECEPTIONS threshold (30 minimum) filters out noise
- **Severity:** Low

---

## Implementation Checklist

**Phase 1: Data Pipeline**
- [ ] `YardsPerReceptionCalculator.py` created
- [ ] `calculate()` method implemented
- [ ] `_calculate_ypr_metrics()` helper created
- [ ] `_classify_tier()` helper created (position-specific)

**Phase 2: Configuration**
- [ ] `YARDS_PER_RECEPTION_SCORING` section added to `league_config.json`
- [ ] Separate thresholds for WR and TE configured
- [ ] `get_yards_per_reception_multiplier()` method added to ConfigManager

**Phase 3: Scoring Integration**
- [ ] `_apply_yards_per_reception_scoring()` method added to `player_scoring.py`
- [ ] Integration point added to `calculate_total_score()`

**Phase 4: Testing**
- [ ] `test_YardsPerReceptionCalculator.py` created
- [ ] Test deep threat WR (15.0+ YPR)
- [ ] Test possession WR (9.0-11.9 YPR)
- [ ] Test elite TE (12.0+ YPR)
- [ ] Test insufficient receptions (<30 receptions)
- [ ] Test non-WR/TE returns neutral
- [ ] All tests passing (100% pass rate)

**Phase 5: Documentation**
- [ ] `19_yards_per_reception_scoring.md` created
- [ ] README.md updated with Step 19
- [ ] Checklist marked complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add yards per reception scoring (M09)"

---

**END OF FEATURE REQUEST**
