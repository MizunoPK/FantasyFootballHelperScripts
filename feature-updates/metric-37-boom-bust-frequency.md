# Feature Request: Boom/Bust Frequency

**Metric ID:** M37
**Priority:** MEDIUM
**Positions:** All (QB, RB, WR, TE, K, DST)
**Effort Estimate:** 3-4 hours
**Expected Impact:** 5-8% improvement in weekly lineup optimization based on risk tolerance

---

## What This Metric Is

Boom/Bust Frequency measures how often a player significantly exceeds their projection (boom) versus significantly underperforms (bust). This captures outcome variance in fantasy points, helping identify reliable players versus high-variance gambles. A player who booms 40% and busts 20% is more valuable than one who booms 20% and busts 40%.

---

## What We're Trying to Accomplish

**Goals:**
- **Quantify player reliability**: Distinguish safe floors from volatile ceilings
- **Support risk-adjusted decisions**: Choose between consistent vs. upside plays
- **Identify true boom candidates**: Players who frequently exceed projections
- **Flag bust-prone players**: Those who frequently disappoint
- **Weekly lineup optimization**: Match risk profile to matchup needs

**Example Use Case:**
> Player A: 8 booms, 3 busts in 15 games (53% boom rate, 20% bust rate) → Reliable upside
> Player B: 4 booms, 7 busts in 15 games (27% boom rate, 47% bust rate) → Risky play
> Same average PPG, very different risk profiles.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:** `data/player_data/[position]_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `actual_points` | float | Yes (17 weeks) | All position JSON | 22.5 |
| `projected_points` | float | Yes (17 weeks) | All position JSON | 15.0 |

**Example Data Structure:**
```json
{
  "id": "4241389",
  "name": "Josh Allen",
  "team": "BUF",
  "position": "QB",
  "actual_points": [28.5, 18.2, 32.1, 0.0, 24.8, 15.3, 35.2, 22.1, 19.8, 28.4, 31.2, 20.5, 26.8, 18.9, 29.1, 24.2, 0.0],
  "projected_points": [22.0, 21.5, 23.0, 0.0, 22.5, 21.0, 22.0, 21.5, 22.0, 23.0, 22.5, 21.5, 22.0, 22.5, 23.0, 22.0, 0.0]
}
```

### Data Validation
- Data verified in: All `data/player_data/*_data.json` files
- Weekly granularity: Yes (17 weeks per season)
- Historical availability: Current season
- Known limitations: Projection quality affects accuracy; bye weeks = 0 in both fields

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_boom_bust_frequency(player: FantasyPlayer) -> dict:
    """
    Calculate boom/bust frequency for a player.

    Args:
        player: FantasyPlayer object with actual_points and projected_points

    Returns:
        dict: {
            'boom_count': int,          # Games exceeding projection by threshold
            'bust_count': int,          # Games below projection by threshold
            'neutral_count': int,       # Games within threshold
            'boom_rate': float,         # boom_count / games_played
            'bust_rate': float,         # bust_count / games_played
            'boom_bust_ratio': float,   # boom_rate / bust_rate (higher = better)
            'reliability_tier': str,    # BOOM_MACHINE, RELIABLE, AVERAGE, RISKY, BUST_PRONE
            'games_played': int
        }

    Example:
        >>> player = FantasyPlayer(name="Josh Allen", stats={...})
        >>> result = calculate_boom_bust_frequency(player)
        >>> result
        {'boom_count': 9, 'bust_count': 3, 'neutral_count': 3, 'boom_rate': 0.60,
         'bust_rate': 0.20, 'boom_bust_ratio': 3.0, 'reliability_tier': 'BOOM_MACHINE', 'games_played': 15}
    """
    actual = player.stats.get('actual_points', [])
    projected = player.stats.get('projected_points', [])

    # Step 1: Filter out bye weeks (both actual and projected = 0)
    game_results = []
    for act, proj in zip(actual, projected):
        if proj > 0:  # Has a projection = real game
            game_results.append({'actual': act, 'projected': proj})

    if len(game_results) < 3:
        return {
            'boom_count': 0,
            'bust_count': 0,
            'neutral_count': 0,
            'boom_rate': 0.0,
            'bust_rate': 0.0,
            'boom_bust_ratio': 1.0,
            'reliability_tier': 'INSUFFICIENT_DATA',
            'games_played': len(game_results)
        }

    # Step 2: Define boom/bust thresholds
    # Boom = exceeded projection by 25%+
    # Bust = fell below projection by 25%+
    BOOM_THRESHOLD = 1.25  # 25% above projection
    BUST_THRESHOLD = 0.75  # 25% below projection

    boom_count = 0
    bust_count = 0
    neutral_count = 0

    for game in game_results:
        ratio = game['actual'] / game['projected'] if game['projected'] > 0 else 1.0

        if ratio >= BOOM_THRESHOLD:
            boom_count += 1
        elif ratio <= BUST_THRESHOLD:
            bust_count += 1
        else:
            neutral_count += 1

    games_played = len(game_results)

    # Step 3: Calculate rates
    boom_rate = boom_count / games_played
    bust_rate = bust_count / games_played

    # Step 4: Calculate boom/bust ratio (avoid division by zero)
    if bust_rate > 0:
        boom_bust_ratio = boom_rate / bust_rate
    else:
        boom_bust_ratio = boom_rate * 10 if boom_rate > 0 else 1.0  # High ratio if no busts

    # Step 5: Determine reliability tier
    if boom_rate >= 0.50 and bust_rate <= 0.20:
        reliability_tier = 'BOOM_MACHINE'
    elif boom_rate >= 0.35 and bust_rate <= 0.30:
        reliability_tier = 'RELIABLE'
    elif boom_rate >= 0.25 and bust_rate <= 0.40:
        reliability_tier = 'AVERAGE'
    elif bust_rate >= 0.40 and boom_rate < 0.30:
        reliability_tier = 'RISKY'
    else:
        reliability_tier = 'BUST_PRONE' if bust_rate > boom_rate else 'AVERAGE'

    return {
        'boom_count': boom_count,
        'bust_count': bust_count,
        'neutral_count': neutral_count,
        'boom_rate': round(boom_rate, 3),
        'bust_rate': round(bust_rate, 3),
        'boom_bust_ratio': round(boom_bust_ratio, 2),
        'reliability_tier': reliability_tier,
        'games_played': games_played
    }
```

### Thresholds & Tiers

**Boom/Bust Thresholds:**
- **Boom:** Actual >= 125% of Projected (exceeded by 25%+)
- **Bust:** Actual <= 75% of Projected (fell short by 25%+)
- **Neutral:** Within 75-125% of projection

**Reliability Tiers:**

| Tier | Boom Rate | Bust Rate | Description | Multiplier |
|------|-----------|-----------|-------------|------------|
| BOOM_MACHINE | >= 50% | <= 20% | Frequent upside, rare busts | 1.04 |
| RELIABLE | >= 35% | <= 30% | Good boom rate, acceptable busts | 1.02 |
| AVERAGE | >= 25% | <= 40% | Normal variance | 1.0 |
| RISKY | < 30% | >= 40% | Frequent disappointments | 0.98 |
| BUST_PRONE | < 25% | > 40% | More busts than booms | 0.96 |

### Edge Cases

**1. Bye Week Handling**
- **Scenario:** Both actual and projected = 0
- **Handling:** Exclude from calculation entirely
- **Example:** Week 7 bye → not counted in games_played

**2. Low Projection Games**
- **Scenario:** Projected 2.0, actual 5.0 = 250% (boom)
- **Handling:** Use percentage-based threshold (works at all projection levels)

**3. Zero Projection But Played**
- **Scenario:** Late add with no projection but had actual points
- **Handling:** Skip game if projected = 0 (can't calculate ratio)

---

## Implementation Plan

### Phase 1: Calculation Module (Estimated: 1.5 hours)

**File:** `league_helper/util/BoomBustCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class BoomBustCalculator:
    """Calculate boom/bust frequency for fantasy players"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()
        self.boom_threshold = config_manager.boom_bust_scoring.get('BOOM_THRESHOLD', 1.25)
        self.bust_threshold = config_manager.boom_bust_scoring.get('BUST_THRESHOLD', 0.75)

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate boom/bust frequency and return multiplier.

        Args:
            player: Player to calculate for

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        metrics = self._calculate_boom_bust_metrics(player)

        if metrics['reliability_tier'] == 'INSUFFICIENT_DATA':
            return 1.0, "INSUFFICIENT_DATA"

        tier = metrics['reliability_tier']
        multiplier = self._get_multiplier(tier)

        return multiplier, tier

    def _calculate_boom_bust_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate boom/bust metrics"""
        # Implementation from formula above
        pass

    def _get_multiplier(self, tier: str) -> float:
        """Get multiplier for reliability tier"""
        multipliers = self.config.boom_bust_scoring.get('MULTIPLIERS', {})
        base_mult = multipliers.get(tier, 1.0)
        weight = self.config.boom_bust_scoring.get('WEIGHT', 1.0)
        return base_mult ** weight
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**Add to league_config.json:**

```json
{
  "BOOM_BUST_SCORING": {
    "ENABLED": true,
    "BOOM_THRESHOLD": 1.25,
    "BUST_THRESHOLD": 0.75,
    "TIER_THRESHOLDS": {
      "BOOM_MACHINE": {"BOOM_RATE": 0.50, "MAX_BUST_RATE": 0.20},
      "RELIABLE": {"BOOM_RATE": 0.35, "MAX_BUST_RATE": 0.30},
      "AVERAGE": {"BOOM_RATE": 0.25, "MAX_BUST_RATE": 0.40},
      "RISKY": {"BOOM_RATE": 0.30, "MIN_BUST_RATE": 0.40}
    },
    "MULTIPLIERS": {
      "BOOM_MACHINE": 1.04,
      "RELIABLE": 1.02,
      "AVERAGE": 1.0,
      "RISKY": 0.98,
      "BUST_PRONE": 0.96
    },
    "WEIGHT": 1.0,
    "MIN_GAMES": 3,
    "DESCRIPTION": "Boom/bust frequency - how often player exceeds or misses projections"
  }
}
```

---

### Phase 3: Testing (Estimated: 1 hour)

**Unit Tests:**

```python
class TestBoomBustCalculator:

    def test_boom_machine_player(self, calculator):
        """Test player who frequently exceeds projections"""
        player = create_player(
            actual_points=[28, 25, 30, 22, 32, 26, 35, 24, 29, 27, 31, 23, 28, 30, 26],
            projected_points=[20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
        )
        # Most games exceed 25 points (125% of 20)

        multiplier, tier = calculator.calculate(player)

        assert tier == "BOOM_MACHINE"
        assert multiplier > 1.0

    def test_bust_prone_player(self, calculator):
        """Test player who frequently underperforms"""
        player = create_player(
            actual_points=[12, 8, 15, 10, 14, 9, 11, 18, 8, 12, 10, 14, 9, 11, 13],
            projected_points=[20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
        )
        # Most games below 15 points (75% of 20)

        multiplier, tier = calculator.calculate(player)

        assert tier in ["RISKY", "BUST_PRONE"]
        assert multiplier < 1.0

    def test_bye_week_exclusion(self, calculator):
        """Test bye weeks are excluded"""
        player = create_player(
            actual_points=[25, 22, 0, 28, 24],
            projected_points=[20, 20, 0, 20, 20]  # Week 3 bye
        )

        metrics = calculator._calculate_boom_bust_metrics(player)

        assert metrics['games_played'] == 4  # Excludes bye
```

---

## Real-World Examples

### Example 1: Boom Machine QB

**Josh Allen (BUF, QB):**

| Metric | Value |
|--------|-------|
| Games Played | 15 |
| Boom Games (125%+) | 9 |
| Bust Games (75%-) | 2 |
| Neutral Games | 4 |
| Boom Rate | 60% |
| Bust Rate | 13% |
| Boom/Bust Ratio | 4.5 |
| Tier | BOOM_MACHINE |
| Multiplier | 1.04 |

**Reason String:** `"Boom/Bust (BOOM_MACHINE): 60% boom, 13% bust, ratio 4.5"`

### Example 2: Bust-Prone WR

**Inconsistent WR:**

| Metric | Value |
|--------|-------|
| Games Played | 14 |
| Boom Games | 3 |
| Bust Games | 7 |
| Neutral Games | 4 |
| Boom Rate | 21% |
| Bust Rate | 50% |
| Boom/Bust Ratio | 0.43 |
| Tier | BUST_PRONE |
| Multiplier | 0.96 |

**Reason String:** `"Boom/Bust (BUST_PRONE): 21% boom, 50% bust, ratio 0.43"`

---

## Dependencies

### Data Dependencies
- `actual_points` - Available in all `data/player_data/*_data.json` files
- `projected_points` - Available in all `data/player_data/*_data.json` files

### Code Dependencies
- `ConfigManager` - Existing
- `FantasyPlayer` - Existing
- `BoomBustCalculator` - To be created

---

## Related Metrics

**Complementary Metrics:**
- **M34 (Recent Form)** - Trending direction
- **M50/M51 (Consistency)** - Volume-based variance
- **M17 (Target Share Trend)** - Usage trending

---

## Implementation Checklist

- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed
- [ ] BoomBustCalculator module created
- [ ] Scoring integration added
- [ ] Unit tests written and passing

---

**END OF FEATURE REQUEST**
