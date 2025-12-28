# Feature Request: Pass Attempts Per Game (QB Volume)

**Metric ID:** M03
**Priority:** HIGH
**Positions:** QB
**Effort Estimate:** 2-3 hours
**Expected Impact:** 10-15% improvement in QB weekly projections

---

## What This Metric Is

Pass Attempts Per Game measures a quarterback's average passing attempts per game, providing a volume floor indicator for fantasy production. High-volume passing offenses (40+ attempts/game) create more opportunities for fantasy points through completions, yards, and touchdowns.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify high-volume passing offenses**: QBs with 40+ attempts/game have elite fantasy ceilings due to sheer opportunity volume
- **Quantify passing floor**: More attempts = more chances for completions, yards, and TDs
- **Game script indicator**: Teams that pass frequently (trailing, pass-first offenses) create consistent QB usage
- **Weather the variance**: High-volume passers are less affected by TD variance - even low TD games produce fantasy points through volume
- **Draft strategy**: Target QBs in pass-heavy offenses over talented QBs in run-first systems

**Example Use Case:**
> Joe Burrow averaging 42 attempts/game in a pass-heavy offense will outscore a QB with similar efficiency but only 30 attempts/game. The 12 extra attempts per game create ~8-10 additional completions, 80-100 extra yards, and 0.5-1.0 additional TDs per week, translating to 6-8 fantasy points.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/qb_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `passing.attempts` | float | Yes (17 weeks) | QB JSON | 38.0 |
| `position` | string | No | All player JSON | "QB" |

**Example Data Structure:**
```json
{
  "id": "3915511",
  "name": "Joe Burrow",
  "team": "CIN",
  "position": "QB",
  "passing": {
    "attempts": [42.0, 37.0, 46.0, 0.0, 39.0, 44.0, 36.0, 41.0, 38.0, 40.0, 39.0, 42.0, 37.0, 43.0],
    "completions": [28.0, 24.0, 31.0, 0.0, 26.0, 29.0, 23.0, 27.0, 25.0, 28.0, 26.0, 30.0, 24.0, 29.0],
    "pass_yds": [324.0, 278.0, 356.0, 0.0, 301.0, 342.0, 268.0, 318.0, 289.0, 327.0, 295.0, 348.0, 271.0, 335.0]
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
def calculate_pass_attempts_per_game(player: FantasyPlayer) -> dict:
    """
    Calculate pass attempts per game for a QB.

    Args:
        player: FantasyPlayer object with passing stats

    Returns:
        dict: {
            'attempts_per_game': float,
            'season_attempts': int,
            'games_played': int,
            'tier': str
        }

    Example:
        >>> player = FantasyPlayer(name="Joe Burrow", position="QB", stats={...})
        >>> result = calculate_pass_attempts_per_game(player)
        >>> result
        {'attempts_per_game': 40.3, 'season_attempts': 564, 'games_played': 14, 'tier': 'EXCELLENT'}
    """
    if player.position != 'QB':
        return {
            'attempts_per_game': 0.0,
            'season_attempts': 0,
            'games_played': 0,
            'tier': 'N/A'
        }

    # Step 1: Get weekly attempts
    weekly_attempts = player.stats['passing']['attempts']

    # Step 2: Count games played (exclude bye weeks and injuries)
    games_played = len([a for a in weekly_attempts if a > 0])

    # Step 3: Calculate season total
    season_attempts = sum(weekly_attempts)

    # Step 4: Calculate attempts per game
    if games_played > 0:
        attempts_per_game = season_attempts / games_played
    else:
        attempts_per_game = 0.0

    # Step 5: Determine tier
    tier = _classify_attempts_tier(attempts_per_game)

    return {
        'attempts_per_game': round(attempts_per_game, 1),
        'season_attempts': season_attempts,
        'games_played': games_played,
        'tier': tier
    }

def _classify_attempts_tier(attempts_per_game: float) -> str:
    """Classify QB tier based on pass attempts per game"""
    if attempts_per_game >= 40.0:
        return "EXCELLENT"  # Elite volume
    elif attempts_per_game >= 35.0:
        return "GOOD"       # High volume
    elif attempts_per_game >= 28.0:
        return "AVERAGE"    # Standard volume
    else:
        return "POOR"       # Low volume / run-first offense
```

### Thresholds & Tiers

**QB Pass Attempts Per Game:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥40 attempts/game | Elite volume, pass-first offense | 1.05 | Joe Burrow, Justin Herbert |
| GOOD | 35-39 attempts/game | High volume | 1.025 | Patrick Mahomes, Dak Prescott |
| AVERAGE | 28-34 attempts/game | Standard volume | 1.0 | Most starting QBs |
| POOR | <28 attempts/game | Low volume, run-first offense | 0.975 | Jalen Hurts (run-heavy), Justin Fields |

### Edge Cases

**1. Run-First Offense with Elite QB**
- **Scenario:** Talented QB (Josh Allen) in balanced offense with 32 attempts/game
- **Handling:** Classified as AVERAGE tier despite elite talent - volume matters more than skill
- **Example:** Josh Allen with 32 attempts/game scores lower than Joe Burrow with 42 attempts/game

**2. Garbage Time Inflation**
- **Scenario:** QB on bad team passes 45 times/game due to trailing (garbage time stats)
- **Handling:** Metric doesn't distinguish garbage time - volume is volume for fantasy
- **Example:** QB on 3-14 team still valuable in fantasy due to high attempt rate

**3. Blowout Games / Early Benching**
- **Scenario:** QB on dominant team gets benched in 4th quarter, lowering attempts
- **Handling:** Per-game average smooths out blowout games across full season
- **Example:** Patrick Mahomes may have lower attempts in wins but average stays high

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**File:** `league_helper/util/PassAttemptsPerGameCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class PassAttemptsPerGameCalculator:
    """Calculate pass attempts per game for QBs"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate pass attempts per game and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'QB':
            return 1.0, "N/A"

        # Calculate attempts metrics
        metrics = self._calculate_attempts_metrics(player)

        # Get multiplier from config
        multiplier = self.config.get_pass_attempts_multiplier(metrics['tier'])

        self.logger.debug(
            f"QB {player.name}: {metrics['attempts_per_game']:.1f} att/game "
            f"(Tier: {metrics['tier']}, Multiplier: {multiplier:.3f})"
        )

        return multiplier, metrics['tier']

    def _calculate_attempts_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate attempts metrics for a QB"""
        weekly_attempts = player.stats.get('passing', {}).get('attempts', [])

        if not weekly_attempts:
            return {
                'attempts_per_game': 0.0,
                'season_attempts': 0,
                'games_played': 0,
                'tier': 'N/A'
            }

        games_played = len([a for a in weekly_attempts if a > 0])
        season_attempts = sum(weekly_attempts)

        attempts_per_game = season_attempts / games_played if games_played > 0 else 0.0

        tier = self._classify_tier(attempts_per_game)

        return {
            'attempts_per_game': round(attempts_per_game, 1),
            'season_attempts': int(season_attempts),
            'games_played': games_played,
            'tier': tier
        }

    def _classify_tier(self, attempts_per_game: float) -> str:
        """Classify QB tier based on attempts per game"""
        thresholds = self.config.pass_attempts_scoring.get('THRESHOLDS', {})

        if attempts_per_game >= thresholds.get('EXCELLENT', 40.0):
            return "EXCELLENT"
        elif attempts_per_game >= thresholds.get('GOOD', 35.0):
            return "GOOD"
        elif attempts_per_game >= thresholds.get('AVERAGE', 28.0):
            return "AVERAGE"
        else:
            return "POOR"
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "PASS_ATTEMPTS_PER_GAME_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 40.0,
      "GOOD": 35.0,
      "AVERAGE": 28.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.05,
      "GOOD": 1.025,
      "AVERAGE": 1.0,
      "POOR": 0.975
    },
    "WEIGHT": 2.0,
    "MIN_WEEKS": 3,
    "DESCRIPTION": "QB pass attempts per game - volume indicator"
  }
}
```

**2.2 Add ConfigManager method**

```python
def get_pass_attempts_multiplier(self, tier: str) -> float:
    """
    Get pass attempts multiplier for QB volume tier.

    Args:
        tier: Tier classification (EXCELLENT, GOOD, AVERAGE, POOR)

    Returns:
        float: Multiplier value
    """
    multipliers = self.config.get('PASS_ATTEMPTS_PER_GAME_SCORING', {}).get('MULTIPLIERS', {})
    return multipliers.get(tier, 1.0)
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_pass_attempts_scoring()`

```python
def _apply_pass_attempts_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply pass attempts per game adjustment (QB only)"""
    if p.position != 'QB':
        return player_score, ""

    if not self.config.pass_attempts_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = PassAttemptsPerGameCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    # Apply multiplier with weight
    weight = self.config.pass_attempts_scoring.get('WEIGHT', 2.0)
    adjusted_score = player_score * (multiplier ** weight)

    # Get metrics for reason string
    metrics = calculator._calculate_attempts_metrics(p)
    reason = f"Pass Att/Game ({tier}): {metrics['attempts_per_game']:.1f}"

    return adjusted_score, reason
```

**Integration in `calculate_total_score()`:**

```python
# After existing scoring steps
player_score, reason = self._apply_pass_attempts_scoring(p, player_score)
if reason:
    score_reasons.append(reason)
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_PassAttemptsPerGameCalculator.py`

```python
import pytest
from league_helper.util.PassAttemptsPerGameCalculator import PassAttemptsPerGameCalculator
from league_helper.util.FantasyPlayer import FantasyPlayer
from league_helper.util.ConfigManager import ConfigManager

class TestPassAttemptsPerGameCalculator:
    """Test Pass Attempts Per Game Calculator functionality"""

    @pytest.fixture
    def calculator(self, tmp_path):
        """Create calculator with test config"""
        config = ConfigManager(tmp_path)
        return PassAttemptsPerGameCalculator(config)

    def test_elite_volume_qb(self, calculator):
        """Test QB with 40+ attempts/game"""
        player = FantasyPlayer(
            name="Joe Burrow",
            position="QB",
            stats={
                'passing': {
                    'attempts': [42, 37, 46, 0, 39, 44, 36, 41, 38, 40, 39, 42, 37, 43]
                }
            }
        )

        multiplier, tier = calculator.calculate(player)

        assert tier == "EXCELLENT"
        assert multiplier > 1.04

    def test_high_volume_qb(self, calculator):
        """Test QB with 35-39 attempts/game"""
        player = FantasyPlayer(
            name="Patrick Mahomes",
            position="QB",
            stats={
                'passing': {
                    'attempts': [37, 34, 38, 0, 36, 39, 35, 37, 36, 38, 37, 36, 35, 38]
                }
            }
        )

        multiplier, tier = calculator.calculate(player)

        assert tier == "GOOD"
        assert 1.02 < multiplier < 1.03

    def test_run_first_offense_qb(self, calculator):
        """Test QB in run-heavy offense (<28 attempts)"""
        player = FantasyPlayer(
            name="Jalen Hurts",
            position="QB",
            stats={
                'passing': {
                    'attempts': [25, 22, 27, 0, 24, 26, 23, 25, 24, 26, 25, 24, 23, 27]
                }
            }
        )

        multiplier, tier = calculator.calculate(player)

        assert tier == "POOR"
        assert multiplier < 1.0

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

    def test_insufficient_games_handled(self, calculator):
        """Test QB with very few games played"""
        player = FantasyPlayer(
            name="Injured QB",
            position="QB",
            stats={
                'passing': {
                    'attempts': [0, 0, 42, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        )

        metrics = calculator._calculate_attempts_metrics(player)

        assert metrics['games_played'] == 2
        assert metrics['attempts_per_game'] == 40.0
        assert metrics['tier'] == "EXCELLENT"
```

---

### Phase 5: Documentation (Estimated: 30 min)

**File:** `docs/scoring/14_pass_attempts_per_game_scoring.md`

```markdown
# Step 14: Pass Attempts Per Game (QB Volume Indicator)

**Priority:** HIGH | **Positions:** QB | **Pattern:** Multiplier-based

## Overview

Pass Attempts Per Game measures QB passing volume, identifying high-volume offenses (40+ attempts/game) that create more fantasy opportunities through sheer volume of throws.

## Formula

```
attempts_per_game = season_attempts / games_played
```

## Thresholds

- EXCELLENT: ≥40 attempts/game (+5% bonus)
- GOOD: 35-39 attempts/game (+2.5% bonus)
- AVERAGE: 28-34 attempts/game (no adjustment)
- POOR: <28 attempts/game (-2.5% penalty)

## Example

**Joe Burrow (CIN, QB)**
- Season attempts: 564
- Games played: 14
- Attempts/game: 40.3
- Tier: EXCELLENT
- Multiplier: 1.05^2.0 = 1.1025
- Impact: +10.25% to base score

## Why This Matters

More passing attempts create more opportunities for completions, yards, and touchdowns, providing a higher fantasy floor and ceiling regardless of efficiency metrics.
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 10-15%
- Rationale: Identifies QBs in pass-heavy offenses early in draft

**Starter Helper Mode:**
- Expected improvement: 12-18%
- Rationale: High-volume passers have more consistent weekly floors

**Trade Simulator Mode:**
- Expected improvement: 8-12%
- Rationale: Separates volume-based QB value from efficiency-based value

---

## Real-World Examples

### Example 1: Elite Volume QB

**Joe Burrow (CIN, QB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Season Attempts | 564 |
| Games Played | 14 |
| Attempts/Game | 40.3 |
| Tier | EXCELLENT |
| Multiplier | 1.05^2.0 = 1.1025 |
| Base Score | 285.0 |
| Adjusted Score | 314.2 (+29.2 pts) |

**Reason String:** `"Pass Att/Game (EXCELLENT): 40.3"`

### Example 2: Run-First Offense QB

**Jalen Hurts (PHI, QB)** - Run-Heavy Offense:

| Metric | Value |
|--------|-------|
| Season Attempts | 351 |
| Games Played | 14 |
| Attempts/Game | 25.1 |
| Tier | POOR |
| Multiplier | 0.975^2.0 = 0.9506 |
| Base Score | 265.0 |
| Adjusted Score | 251.9 (-13.1 pts) |

**Reason String:** `"Pass Att/Game (POOR): 25.1"`

---

## Dependencies

### Data Dependencies
- ✅ `passing.attempts` - Available in `data/player_data/qb_data.json`

### Code Dependencies
- 🆕 `PassAttemptsPerGameCalculator` - To be created
- ✅ `ConfigManager` - Existing, needs new method

---

## Risks & Mitigations

### Risk 1: Garbage Time Inflation
- **Issue:** QBs on bad teams may have inflated attempts from trailing frequently
- **Mitigation:** Garbage time volume still produces fantasy points - no adjustment needed
- **Severity:** Low

### Risk 2: Confusing Volume with Talent
- **Issue:** High-volume QB in bad offense may be overvalued vs talented QB in run-first system
- **Mitigation:** This metric intentionally values volume over talent - fantasy points come from opportunities
- **Severity:** Low (working as intended)

### Risk 3: Injury-Shortened Seasons
- **Issue:** QB with 2-3 games played may have skewed per-game average
- **Mitigation:** Add MIN_WEEKS threshold (3 games minimum) to config
- **Severity:** Medium

---

## Implementation Checklist

**Phase 1: Data Pipeline**
- [ ] `PassAttemptsPerGameCalculator.py` created
- [ ] `calculate()` method implemented
- [ ] `_calculate_attempts_metrics()` helper created
- [ ] `_classify_tier()` helper created

**Phase 2: Configuration**
- [ ] `PASS_ATTEMPTS_PER_GAME_SCORING` section added to `league_config.json`
- [ ] `get_pass_attempts_multiplier()` method added to ConfigManager

**Phase 3: Scoring Integration**
- [ ] `_apply_pass_attempts_scoring()` method added to `player_scoring.py`
- [ ] Integration point added to `calculate_total_score()`

**Phase 4: Testing**
- [ ] `test_PassAttemptsPerGameCalculator.py` created
- [ ] Test elite volume QB (40+ attempts)
- [ ] Test high volume QB (35-39 attempts)
- [ ] Test run-first offense QB (<28 attempts)
- [ ] Test non-QB returns neutral
- [ ] Test insufficient games handled
- [ ] All tests passing (100% pass rate)

**Phase 5: Documentation**
- [ ] `14_pass_attempts_per_game_scoring.md` created
- [ ] README.md updated with Step 14
- [ ] Checklist marked complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add pass attempts per game scoring (M03)"

---

**END OF FEATURE REQUEST**
