# Feature Request: RB Receiving Workload (Pass-Catching Back Value)

**Metric ID:** M11
**Priority:** HIGH
**Positions:** RB
**Effort Estimate:** 3-4 hours
**Expected Impact:** 12-18% improvement in RB PPR evaluation

---

## What This Metric Is

RB Receiving Workload measures a running back's pass-catching role through targets per game, identifying pass-catching specialists (8+ targets/game) versus pure rushers (<3 targets/game). This metric is critical for PPR league evaluation, where receiving RBs have significantly higher fantasy value.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify pass-catching RB specialists**: 8+ targets/game RBs (Christian McCaffrey, Austin Ekeler) provide elite PPR floors
- **Quantify PPR advantage**: Each target = 0.5-0.7 PPR points, plus yardage and TD potential
- **Three-down back indicator**: High receiving workload indicates trust in all situations (rush, catch, block)
- **Game script protection**: Pass-catching RBs maintain value in negative game scripts when teams trail
- **Draft strategy**: Prioritize pass-catching RBs in PPR leagues - massive floor/ceiling advantage

**Example Use Case:**
> Christian McCaffrey with 7.6 targets/game = 129 targets per season. At 75% catch rate, that's 97 receptions = 97 PPR points + ~700 receiving yards + 3-4 receiving TDs = 140+ fantasy points from receiving alone. An RB with 2 targets/game = only 34 targets = ~25 receptions = 25 PPR points + ~150 yards = 40 fantasy points from receiving.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/rb_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `receiving.targets` | float | Yes (17 weeks) | RB JSON | 8.0 |
| `receiving.receptions` | float | Yes (17 weeks) | RB JSON | 6.0 |
| `receiving.receiving_yds` | float | Yes (17 weeks) | RB JSON | 45.0 |
| `position` | string | No | All player JSON | "RB" |

**Example Data Structure:**
```json
{
  "id": "3116165",
  "name": "Christian McCaffrey",
  "team": "SF",
  "position": "RB",
  "receiving": {
    "targets": [9.0, 6.0, 10.0, 0.0, 7.0, 9.0, 6.0, 10.0, 7.0, 10.0, 7.0, 9.0, 6.0, 9.0],
    "receptions": [7.0, 5.0, 8.0, 0.0, 6.0, 7.0, 5.0, 8.0, 6.0, 8.0, 6.0, 7.0, 5.0, 7.0],
    "receiving_yds": [62.0, 42.0, 75.0, 0.0, 54.0, 68.0, 38.0, 72.0, 51.0, 78.0, 48.0, 64.0, 39.0, 66.0]
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
def calculate_rb_receiving_workload(player: FantasyPlayer) -> dict:
    """
    Calculate RB receiving workload (targets per game).

    Args:
        player: FantasyPlayer object with receiving stats

    Returns:
        dict: {
            'targets_per_game': float,
            'season_targets': int,
            'season_receptions': int,
            'season_receiving_yds': int,
            'games_played': int,
            'tier': str
        }

    Example:
        >>> player = FantasyPlayer(name="Christian McCaffrey", position="RB", stats={...})
        >>> result = calculate_rb_receiving_workload(player)
        >>> result
        {'targets_per_game': 7.6, 'season_targets': 105, 'season_receptions': 85, 'tier': 'GOOD'}
    """
    if player.position != 'RB':
        return {
            'targets_per_game': 0.0,
            'season_targets': 0,
            'season_receptions': 0,
            'season_receiving_yds': 0,
            'games_played': 0,
            'tier': 'N/A'
        }

    # Step 1: Get receiving stats
    weekly_targets = player.stats['receiving']['targets']
    weekly_receptions = player.stats['receiving']['receptions']
    weekly_receiving_yds = player.stats['receiving']['receiving_yds']

    # Step 2: Count games played (games with at least 1 touch: rush or target)
    rush_attempts = player.stats.get('rushing', {}).get('attempts', [0] * len(weekly_targets))
    games_played = len([i for i, (t, r) in enumerate(zip(weekly_targets, rush_attempts)) if t > 0 or r > 0])

    # Step 3: Calculate season totals
    season_targets = sum(weekly_targets)
    season_receptions = sum(weekly_receptions)
    season_receiving_yds = sum(weekly_receiving_yds)

    # Step 4: Calculate targets per game
    if games_played > 0:
        targets_per_game = season_targets / games_played
    else:
        targets_per_game = 0.0

    # Step 5: Determine tier
    tier = _classify_rb_receiving_tier(targets_per_game, games_played)

    return {
        'targets_per_game': round(targets_per_game, 1),
        'season_targets': int(season_targets),
        'season_receptions': int(season_receptions),
        'season_receiving_yds': int(season_receiving_yds),
        'games_played': games_played,
        'tier': tier
    }

def _classify_rb_receiving_tier(targets_per_game: float, games_played: int) -> str:
    """
    Classify RB tier based on receiving workload (targets per game).

    Args:
        targets_per_game: Targets per game average
        games_played: Minimum games required for reliable sample

    Returns:
        str: Tier classification
    """
    # Require minimum 6 games for reliable targets/game measurement
    if games_played < 6:
        return "INSUFFICIENT_DATA"

    if targets_per_game >= 8.0:
        return "EXCELLENT"  # Pass-catching specialist
    elif targets_per_game >= 5.0:
        return "GOOD"       # Receiving back
    elif targets_per_game >= 3.0:
        return "AVERAGE"    # Occasional receiver
    else:
        return "POOR"       # Pure rusher
```

### Thresholds & Tiers

**RB Receiving Workload (Targets Per Game):**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥8 targets/game | Pass-catching specialist | 1.05 | Christian McCaffrey (historical), Austin Ekeler |
| GOOD | 5-7 targets/game | Three-down receiving back | 1.025 | Alvin Kamara, Bijan Robinson |
| AVERAGE | 3-4 targets/game | Occasional receiver | 1.0 | Most starting RBs |
| POOR | <3 targets/game | Pure rusher, limited pass game | 0.975 | Derrick Henry, rushing-only backs |

**Note:** Requires minimum 6 games played for reliable classification.

### Edge Cases

**1. Early Down + Third Down Specialist Combo**
- **Scenario:** RB rotates with pass-catching specialist, gets <3 targets despite being lead rusher
- **Handling:** Penalized by this metric, but M04 Carries Per Game captures rushing value
- **Example:** Derrick Henry type - elite rusher but limited receiving

**2. Pass-Catching Back on Run-First Team**
- **Scenario:** RB with receiving skills but team runs 65% of the time, limiting targets
- **Handling:** Targets still counted - metric measures actual usage not potential
- **Example:** Team offensive philosophy limits receiving opportunities

**3. Injury-Shortened Season**
- **Scenario:** RB with only 4 games played (below 6 minimum)
- **Handling:** Classified as "INSUFFICIENT_DATA", returns 1.0 multiplier
- **Example:** Early season injury limits sample size

**4. Goal-Line/Short-Yardage Specialist**
- **Scenario:** RB with high TD rate but only 2 targets/game
- **Handling:** Gets POOR tier penalty but TD value captured elsewhere
- **Example:** Vulture backs with limited all-around usage

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1.5 hours)

**File:** `league_helper/util/RBReceivingWorkloadCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class RBReceivingWorkloadCalculator:
    """Calculate RB receiving workload for pass-catching back evaluation"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate RB receiving workload and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'RB':
            return 1.0, "N/A"

        # Calculate receiving workload metrics
        metrics = self._calculate_receiving_workload_metrics(player)

        # Get multiplier from config
        multiplier = self.config.get_rb_receiving_workload_multiplier(metrics['tier'])

        self.logger.debug(
            f"RB {player.name}: {metrics['targets_per_game']:.1f} targets/game "
            f"({metrics['season_targets']} targets / {metrics['games_played']} games) "
            f"(Tier: {metrics['tier']}, Multiplier: {multiplier:.3f})"
        )

        return multiplier, metrics['tier']

    def _calculate_receiving_workload_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate receiving workload metrics for an RB"""
        weekly_targets = player.stats.get('receiving', {}).get('targets', [])
        weekly_receptions = player.stats.get('receiving', {}).get('receptions', [])
        weekly_receiving_yds = player.stats.get('receiving', {}).get('receiving_yds', [])

        if not weekly_targets:
            return {
                'targets_per_game': 0.0,
                'season_targets': 0,
                'season_receptions': 0,
                'season_receiving_yds': 0,
                'games_played': 0,
                'tier': 'N/A'
            }

        # Count games played (games with any touches)
        rush_attempts = player.stats.get('rushing', {}).get('attempts', [0] * len(weekly_targets))
        games_played = len([i for i, (t, r) in enumerate(zip(weekly_targets, rush_attempts)) if t > 0 or r > 0])

        season_targets = sum(weekly_targets)
        season_receptions = sum(weekly_receptions)
        season_receiving_yds = sum(weekly_receiving_yds)

        targets_per_game = (season_targets / games_played) if games_played > 0 else 0.0

        tier = self._classify_tier(targets_per_game, games_played)

        return {
            'targets_per_game': round(targets_per_game, 1),
            'season_targets': int(season_targets),
            'season_receptions': int(season_receptions),
            'season_receiving_yds': int(season_receiving_yds),
            'games_played': games_played,
            'tier': tier
        }

    def _classify_tier(self, targets_per_game: float, games_played: int) -> str:
        """Classify RB tier based on receiving workload"""
        thresholds = self.config.rb_receiving_workload_scoring.get('THRESHOLDS', {})
        min_games = self.config.rb_receiving_workload_scoring.get('MIN_GAMES', 6)

        if games_played < min_games:
            return "INSUFFICIENT_DATA"

        if targets_per_game >= thresholds.get('EXCELLENT', 8.0):
            return "EXCELLENT"
        elif targets_per_game >= thresholds.get('GOOD', 5.0):
            return "GOOD"
        elif targets_per_game >= thresholds.get('AVERAGE', 3.0):
            return "AVERAGE"
        else:
            return "POOR"
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "RB_RECEIVING_WORKLOAD_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 8.0,
      "GOOD": 5.0,
      "AVERAGE": 3.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.05,
      "GOOD": 1.025,
      "AVERAGE": 1.0,
      "POOR": 0.975,
      "INSUFFICIENT_DATA": 1.0
    },
    "WEIGHT": 2.5,
    "MIN_GAMES": 6,
    "DESCRIPTION": "RB receiving workload - pass-catching back value for PPR"
  }
}
```

**2.2 Add ConfigManager method**

```python
def get_rb_receiving_workload_multiplier(self, tier: str) -> float:
    """
    Get RB receiving workload multiplier for pass-catching role tier.

    Args:
        tier: Tier classification (EXCELLENT, GOOD, AVERAGE, POOR, INSUFFICIENT_DATA)

    Returns:
        float: Multiplier value
    """
    multipliers = self.config.get('RB_RECEIVING_WORKLOAD_SCORING', {}).get('MULTIPLIERS', {})
    return multipliers.get(tier, 1.0)
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_rb_receiving_workload_scoring()`

```python
def _apply_rb_receiving_workload_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply RB receiving workload adjustment (RB only)"""
    if p.position != 'RB':
        return player_score, ""

    if not self.config.rb_receiving_workload_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = RBReceivingWorkloadCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    # Apply multiplier with weight
    weight = self.config.rb_receiving_workload_scoring.get('WEIGHT', 2.5)
    adjusted_score = player_score * (multiplier ** weight)

    # Get metrics for reason string
    metrics = calculator._calculate_receiving_workload_metrics(p)
    reason = f"RB Receiving ({tier}): {metrics['targets_per_game']:.1f} tgt/game"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_RBReceivingWorkloadCalculator.py`

```python
import pytest
from league_helper.util.RBReceivingWorkloadCalculator import RBReceivingWorkloadCalculator
from league_helper.util.FantasyPlayer import FantasyPlayer
from league_helper.util.ConfigManager import ConfigManager

class TestRBReceivingWorkloadCalculator:
    """Test RB Receiving Workload Calculator functionality"""

    @pytest.fixture
    def calculator(self, tmp_path):
        """Create calculator with test config"""
        config = ConfigManager(tmp_path)
        return RBReceivingWorkloadCalculator(config)

    def test_pass_catching_specialist(self, calculator):
        """Test RB with 8+ targets/game"""
        player = FantasyPlayer(
            name="Christian McCaffrey",
            position="RB",
            stats={
                'receiving': {
                    'targets': [9, 6, 10, 0, 7, 9, 6, 10, 7, 10, 7, 9, 6, 9],
                    'receptions': [7, 5, 8, 0, 6, 7, 5, 8, 6, 8, 6, 7, 5, 7],
                    'receiving_yds': [62, 42, 75, 0, 54, 68, 38, 72, 51, 78, 48, 64, 39, 66]
                },
                'rushing': {
                    'attempts': [18, 15, 20, 0, 16, 19, 14, 21, 17, 20, 16, 19, 14, 18]
                }
            }
        )

        metrics = calculator._calculate_receiving_workload_metrics(player)

        assert metrics['season_targets'] == 105
        assert metrics['games_played'] == 13
        tpg = 105 / 13
        assert metrics['targets_per_game'] == pytest.approx(tpg, abs=0.1)
        assert metrics['tier'] == "EXCELLENT"

    def test_receiving_back(self, calculator):
        """Test RB with 5-7 targets/game"""
        player = FantasyPlayer(
            name="Alvin Kamara",
            position="RB",
            stats={
                'receiving': {
                    'targets': [6, 5, 7, 0, 6, 7, 5, 7, 6, 7, 6, 7, 5, 6],
                    'receptions': [5, 4, 6, 0, 5, 6, 4, 6, 5, 6, 5, 6, 4, 5],
                    'receiving_yds': [42, 35, 58, 0, 45, 62, 32, 54, 41, 68, 38, 56, 29, 48]
                },
                'rushing': {
                    'attempts': [15, 12, 18, 0, 14, 16, 11, 17, 13, 18, 14, 16, 10, 15]
                }
            }
        )

        metrics = calculator._calculate_receiving_workload_metrics(player)
        tpg = metrics['season_targets'] / metrics['games_played']

        assert 5.0 <= tpg < 8.0
        assert metrics['tier'] == "GOOD"

    def test_pure_rusher(self, calculator):
        """Test RB with <3 targets/game"""
        player = FantasyPlayer(
            name="Derrick Henry",
            position="RB",
            stats={
                'receiving': {
                    'targets': [2, 1, 3, 0, 2, 2, 1, 3, 2, 2, 1, 3, 1, 2],
                    'receptions': [1, 1, 2, 0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1],
                    'receiving_yds': [12, 8, 22, 0, 14, 18, 6, 24, 11, 19, 9, 21, 7, 15]
                },
                'rushing': {
                    'attempts': [22, 20, 24, 0, 21, 23, 19, 25, 20, 24, 21, 23, 18, 22]
                }
            }
        )

        metrics = calculator._calculate_receiving_workload_metrics(player)
        tpg = metrics['season_targets'] / metrics['games_played']

        assert tpg < 3.0
        assert metrics['tier'] == "POOR"

    def test_insufficient_games(self, calculator):
        """Test RB with <6 games played"""
        player = FantasyPlayer(
            name="Injured RB",
            position="RB",
            stats={
                'receiving': {
                    'targets': [8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'receptions': [6, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'receiving_yds': [52, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                },
                'rushing': {
                    'attempts': [15, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        )

        metrics = calculator._calculate_receiving_workload_metrics(player)

        assert metrics['games_played'] < 6
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

**File:** `docs/scoring/21_rb_receiving_workload_scoring.md`

```markdown
# Step 21: RB Receiving Workload (Pass-Catching Back Value)

**Priority:** HIGH | **Positions:** RB | **Pattern:** Multiplier-based

## Overview

RB Receiving Workload measures pass-catching role through targets per game, identifying three-down receiving backs (5+ targets/game) who provide elite PPR value.

## Formula

```
targets_per_game = season_targets / games_played
```

## Thresholds

- EXCELLENT: ≥8 targets/game (+5% bonus) - Pass-catching specialist
- GOOD: 5-7 targets/game (+2.5% bonus) - Three-down back
- AVERAGE: 3-4 targets/game (no adjustment)
- POOR: <3 targets/game (-2.5% penalty) - Pure rusher
- INSUFFICIENT_DATA: <6 games (no adjustment)

## Example

**Christian McCaffrey (SF, RB)**
- Season targets: 105
- Games played: 13
- Targets/game: 8.1
- Tier: EXCELLENT
- Multiplier: 1.05^2.5 = 1.1314
- Impact: +13.14% to base score

## Why This Matters

Pass-catching RBs provide massive PPR advantage through reception points, receiving yardage, and game script protection when teams trail. Elite receiving backs are top-5 fantasy assets in PPR formats.

## PPR Context

This metric is especially critical in PPR (Points Per Reception) leagues where each reception equals 1 point. An RB with 8 targets/game at 75% catch rate = 6 receptions = 6 PPR points per week beyond yardage and TDs.
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 12-18%
- Rationale: Identifies pass-catching RBs critical for PPR leagues

**Starter Helper Mode:**
- Expected improvement: 15-20%
- Rationale: Receiving RBs have higher weekly floors and game script protection

**Trade Simulator Mode:**
- Expected improvement: 15-22%
- Rationale: Massive value difference between pass-catching and pure rushing RBs in PPR

---

## Real-World Examples

### Example 1: Pass-Catching Specialist

**Christian McCaffrey (SF, RB)** - Historical (8+ targets/game):

| Metric | Value |
|--------|-------|
| Season Targets | 105 |
| Games Played | 13 |
| Targets/Game | 8.1 |
| Tier | EXCELLENT |
| Multiplier | 1.05^2.5 = 1.1314 |
| Base Score | 265.0 |
| Adjusted Score | 299.8 (+34.8 pts) |

**Reason String:** `"RB Receiving (EXCELLENT): 8.1 tgt/game"`

### Example 2: Receiving Back

**Alvin Kamara (NO, RB)** - Three-Down Back:

| Metric | Value |
|--------|-------|
| Season Targets | 78 |
| Games Played | 13 |
| Targets/Game | 6.0 |
| Tier | GOOD |
| Multiplier | 1.025^2.5 = 1.0641 |
| Base Score | 235.0 |
| Adjusted Score | 250.1 (+15.1 pts) |

**Reason String:** `"RB Receiving (GOOD): 6.0 tgt/game"`

### Example 3: Pure Rusher

**Derrick Henry (BAL, RB)** - Limited Receiving:

| Metric | Value |
|--------|-------|
| Season Targets | 25 |
| Games Played | 13 |
| Targets/Game | 1.9 |
| Tier | POOR |
| Multiplier | 0.975^2.5 = 0.9386 |
| Base Score | 205.0 |
| Adjusted Score | 192.4 (-12.6 pts) |

**Reason String:** `"RB Receiving (POOR): 1.9 tgt/game"`

---

## Dependencies

### Data Dependencies
- ✅ `receiving.targets` - Available in `data/player_data/rb_data.json`
- ✅ `receiving.receptions` - Available in `data/player_data/rb_data.json`
- ✅ `receiving.receiving_yds` - Available in `data/player_data/rb_data.json`
- ✅ `rushing.attempts` - Available in `data/player_data/rb_data.json` (for games played calculation)

### Code Dependencies
- 🆕 `RBReceivingWorkloadCalculator` - To be created
- ✅ `ConfigManager` - Existing, needs new method

---

## Risks & Mitigations

### Risk 1: Team Offensive Philosophy
- **Issue:** Pass-catching RBs on run-first teams undervalued despite skills
- **Mitigation:** Metric measures actual usage not potential - accept limitation
- **Severity:** Low (actual usage is what matters for fantasy)

### Risk 2: Complementary with M01 Target Volume
- **Issue:** This metric overlaps with M01 (Target Volume) for RB position
- **Mitigation:** Use RB-specific thresholds higher than WR/TE in M01
- **Severity:** Low (RB targets more valuable than WR targets in PPR)

---

## Implementation Checklist

**Phase 1: Data Pipeline**
- [ ] `RBReceivingWorkloadCalculator.py` created
- [ ] `calculate()` method implemented
- [ ] `_calculate_receiving_workload_metrics()` helper created
- [ ] `_classify_tier()` helper created

**Phase 2: Configuration**
- [ ] `RB_RECEIVING_WORKLOAD_SCORING` section added to `league_config.json`
- [ ] `get_rb_receiving_workload_multiplier()` method added to ConfigManager

**Phase 3: Scoring Integration**
- [ ] `_apply_rb_receiving_workload_scoring()` method added to `player_scoring.py`
- [ ] Integration point added to `calculate_total_score()`

**Phase 4: Testing**
- [ ] `test_RBReceivingWorkloadCalculator.py` created
- [ ] Test pass-catching specialist (8+ targets/game)
- [ ] Test receiving back (5-7 targets/game)
- [ ] Test pure rusher (<3 targets/game)
- [ ] Test insufficient games (<6 games)
- [ ] Test non-RB returns neutral
- [ ] All tests passing (100% pass rate)

**Phase 5: Documentation**
- [ ] `21_rb_receiving_workload_scoring.md` created
- [ ] README.md updated with Step 21
- [ ] Checklist marked complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add RB receiving workload scoring (M11)"

---

**END OF FEATURE REQUEST**
