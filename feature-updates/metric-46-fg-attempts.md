# Feature Request: Field Goal Attempts Per Game (K)

**Metric ID:** M46
**Priority:** MEDIUM
**Positions:** K
**Effort Estimate:** 2-3 hours
**Expected Impact:** 8-12% improvement in kicker scoring predictions

---

## What This Metric Is

Field Goal Attempts Per Game measures a kicker's opportunity volume - how many FG attempts they get per game. This is the most predictive stat for kicker fantasy scoring since attempts directly translate to scoring chances. A kicker with 2.5 FGA/game has significantly more upside than one with 1.5 FGA/game.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify high-volume kickers**: More attempts = more scoring opportunities
- **Evaluate team context**: Good offense that stalls in red zone = more FG attempts
- **Predict kicker ceiling**: Volume is the primary driver of kicker fantasy points
- **Support streaming decisions**: Target kickers on high-attempt teams
- **Complement accuracy metric (M05)**: Volume + accuracy = complete kicker evaluation

**Example Use Case:**
> Kicker A: 2.8 FGA/game, 85% accuracy = ~7.1 FG points/game potential
> Kicker B: 1.6 FGA/game, 92% accuracy = ~4.4 FG points/game potential
> Despite lower accuracy, Kicker A has 60%+ higher ceiling due to volume.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:** `data/player_data/k_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `field_goals.made` | float | Yes (17 weeks) | k_data.json | 2.0 |
| `field_goals.missed` | float | Yes (17 weeks) | k_data.json | 1.0 |

**FG Attempts = FG Made + FG Missed**

**Example Data Structure:**
```json
{
  "id": "15683",
  "name": "Justin Tucker",
  "team": "BAL",
  "position": "K",
  "field_goals": {
    "made": [2.0, 3.0, 1.0, 0.0, 2.0, 2.0, 3.0, 1.0, 2.0, 2.0, 3.0, 2.0, 1.0, 2.0, 3.0, 2.0, 0.0],
    "missed": [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0]
  },
  "extra_points": {
    "made": [3.0, 2.0, 4.0, 0.0, 3.0, 2.0, 1.0, 4.0, 2.0, 3.0, 2.0, 4.0, 3.0, 2.0, 2.0, 3.0, 0.0],
    "missed": [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
  }
}
```

### Data Validation
- Data verified in: `data/player_data/k_data.json`
- Weekly granularity: Yes (17 weeks per season)
- Historical availability: Current season
- Known limitations: Bye weeks show as 0 made/missed

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_fg_attempts_per_game(kicker: FantasyPlayer) -> dict:
    """
    Calculate FG attempts per game for a kicker.

    Args:
        kicker: FantasyPlayer object (K position)

    Returns:
        dict: {
            'fg_attempts_per_game': float,
            'total_fg_attempts': int,
            'total_fg_made': int,
            'games_played': int,
            'volume_tier': str
        }

    Example:
        >>> kicker = FantasyPlayer(name="Justin Tucker", stats={...})
        >>> result = calculate_fg_attempts_per_game(kicker)
        >>> result
        {'fg_attempts_per_game': 2.6, 'total_fg_attempts': 39, 'total_fg_made': 34,
         'games_played': 15, 'volume_tier': 'EXCELLENT'}
    """
    fg_made = kicker.stats.get('field_goals', {}).get('made', [])
    fg_missed = kicker.stats.get('field_goals', {}).get('missed', [])

    # Calculate weekly attempts and filter bye weeks
    weekly_attempts = []
    total_made = 0
    total_missed = 0

    for made, missed in zip(fg_made, fg_missed):
        made = made or 0
        missed = missed or 0
        attempts = made + missed

        # Detect active games (any FG attempt or XP attempt indicates game played)
        xp_made = kicker.stats.get('extra_points', {}).get('made', [0] * len(fg_made))
        xp_missed = kicker.stats.get('extra_points', {}).get('missed', [0] * len(fg_made))
        idx = len(weekly_attempts)

        if idx < len(xp_made):
            xp_activity = (xp_made[idx] or 0) + (xp_missed[idx] or 0)
        else:
            xp_activity = 0

        # Game played if any kicking activity
        if attempts > 0 or xp_activity > 0:
            weekly_attempts.append(attempts)
            total_made += made
            total_missed += missed

    if len(weekly_attempts) < 3:
        return {
            'fg_attempts_per_game': 0.0,
            'total_fg_attempts': 0,
            'total_fg_made': 0,
            'games_played': len(weekly_attempts),
            'volume_tier': 'INSUFFICIENT_DATA'
        }

    total_attempts = total_made + total_missed
    games_played = len(weekly_attempts)
    fg_per_game = total_attempts / games_played

    # Determine tier
    if fg_per_game >= 2.5:
        volume_tier = 'EXCELLENT'
    elif fg_per_game >= 2.0:
        volume_tier = 'GOOD'
    elif fg_per_game >= 1.5:
        volume_tier = 'AVERAGE'
    elif fg_per_game >= 1.0:
        volume_tier = 'POOR'
    else:
        volume_tier = 'VERY_POOR'

    return {
        'fg_attempts_per_game': round(fg_per_game, 2),
        'total_fg_attempts': int(total_attempts),
        'total_fg_made': int(total_made),
        'games_played': games_played,
        'volume_tier': volume_tier
    }
```

### Thresholds & Tiers

**FG Attempts Per Game Thresholds:**

| Tier | FGA/Game | Description | Multiplier | Example Kicker |
|------|----------|-------------|------------|----------------|
| EXCELLENT | >= 2.5 | Elite volume | 1.06 | High-attempt team kicker |
| GOOD | 2.0 - 2.49 | Above average | 1.03 | Good offensive team |
| AVERAGE | 1.5 - 1.99 | League average | 1.0 | Most kickers |
| POOR | 1.0 - 1.49 | Below average | 0.97 | TD-heavy offense |
| VERY_POOR | < 1.0 | Very low volume | 0.94 | Bad offense |

### Edge Cases

**1. Bye Week Detection**
- **Scenario:** Week with 0 FG made/missed
- **Handling:** Check XP activity - if 0 XP too, it's a bye; if XP > 0, it's a real game with 0 FGA
- **Example:** 0 FG, 3 XP = real game (team scored TDs only)

**2. Games with Only XPs**
- **Scenario:** Team scores 4 TDs, 0 FGs
- **Handling:** Count as game played with 0 FG attempts
- **Example:** Week with 0 FGA but 4 XPA = games_played += 1, fg_attempts += 0

**3. Blowout Games**
- **Scenario:** 5 FG attempts in one game
- **Handling:** Include in calculation (reflects real opportunity)

---

## Implementation Plan

### Phase 1: Calculation Module (Estimated: 1 hour)

**File:** `league_helper/util/FGAttemptsCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class FGAttemptsCalculator:
    """Calculate FG attempts per game for kickers"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate FG attempts per game and return multiplier.

        Args:
            player: Kicker to calculate for

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'K':
            return 1.0, "N/A"

        metrics = self._calculate_fg_metrics(player)

        if metrics['volume_tier'] == 'INSUFFICIENT_DATA':
            return 1.0, "INSUFFICIENT_DATA"

        tier = metrics['volume_tier']
        multiplier = self._get_multiplier(tier)

        return multiplier, tier

    def _calculate_fg_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate FG attempt metrics"""
        # Implementation from formula above
        pass

    def _get_multiplier(self, tier: str) -> float:
        """Get multiplier for volume tier"""
        multipliers = self.config.fg_attempts_scoring.get('MULTIPLIERS', {})
        base_mult = multipliers.get(tier, 1.0)
        weight = self.config.fg_attempts_scoring.get('WEIGHT', 1.5)
        return base_mult ** weight
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**Add to league_config.json:**

```json
{
  "FG_ATTEMPTS_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 2.5,
      "GOOD": 2.0,
      "AVERAGE": 1.5,
      "POOR": 1.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.06,
      "GOOD": 1.03,
      "AVERAGE": 1.0,
      "POOR": 0.97,
      "VERY_POOR": 0.94
    },
    "WEIGHT": 1.5,
    "MIN_GAMES": 3,
    "DESCRIPTION": "Kicker FG attempts per game - opportunity volume metric"
  }
}
```

---

### Phase 3: Testing (Estimated: 0.5 hours)

**Unit Tests:**

```python
class TestFGAttemptsCalculator:

    def test_high_volume_kicker(self, calculator):
        """Test kicker with high FG attempts"""
        kicker = create_kicker(
            fg_made=[3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3],
            fg_missed=[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
            xp_made=[2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2]
        )
        # ~2.7 FGA/game

        multiplier, tier = calculator.calculate(kicker)

        assert tier == "EXCELLENT"
        assert multiplier > 1.0

    def test_low_volume_kicker(self, calculator):
        """Test kicker with low FG attempts"""
        kicker = create_kicker(
            fg_made=[1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            fg_missed=[0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            xp_made=[4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4]  # Lots of TDs
        )
        # ~1.0 FGA/game (team scores TDs instead of FGs)

        multiplier, tier = calculator.calculate(kicker)

        assert tier == "POOR"
        assert multiplier < 1.0

    def test_bye_week_detection(self, calculator):
        """Test bye week with 0 all kicking stats"""
        kicker = create_kicker(
            fg_made=[2, 3, 0, 2, 3],  # Week 3 could be bye
            fg_missed=[0, 0, 0, 1, 0],
            xp_made=[3, 2, 0, 3, 2],  # Week 3 also 0 XP = bye
            xp_missed=[0, 0, 0, 0, 0]
        )

        metrics = calculator._calculate_fg_metrics(kicker)

        assert metrics['games_played'] == 4  # Excludes bye week
```

---

## Real-World Examples

### Example 1: High-Volume Kicker

**High-Volume K (Offense Stalls Often):**

| Metric | Value |
|--------|-------|
| Weekly FG Attempts | 3, 2, 3, 4, 2, 3, 2, 3, 4, 2, 3, 2, 3, 3, 2 |
| Total FG Attempts | 41 |
| Total FG Made | 36 |
| Games Played | 15 |
| FGA/Game | 2.73 |
| Tier | EXCELLENT |
| Multiplier | 1.06^1.5 = 1.0915 |

**Reason String:** `"FG Attempts (EXCELLENT): 2.7 FGA/g (41 attempts, 36 made)"`

### Example 2: TD-Heavy Team Kicker

**Low-Volume K (Team Scores TDs):**

| Metric | Value |
|--------|-------|
| Weekly FG Attempts | 1, 0, 2, 1, 1, 0, 1, 2, 0, 1, 1, 0, 2, 1, 1 |
| Total FG Attempts | 14 |
| Total FG Made | 13 |
| Games Played | 15 |
| FGA/Game | 0.93 |
| Tier | VERY_POOR |
| Multiplier | 0.94^1.5 = 0.9117 |

**Reason String:** `"FG Attempts (VERY_POOR): 0.9 FGA/g (14 attempts, 13 made)"`

---

## Dependencies

### Data Dependencies
- `field_goals.made` - Available in `data/player_data/k_data.json`
- `field_goals.missed` - Available in `data/player_data/k_data.json`
- `extra_points.made/missed` - Available (used for bye detection)

### Code Dependencies
- `ConfigManager` - Existing
- `FantasyPlayer` - Existing
- `FGAttemptsCalculator` - To be created

---

## Related Metrics

**Complementary Metrics:**
- **M05 (Kicker Accuracy)** - Efficiency complement to volume
- **M48 (PAT Attempts)** - Total kicking opportunity
- **M28 (Game Script)** - Affects FG opportunity indirectly

---

## Implementation Checklist

- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed
- [ ] FGAttemptsCalculator module created
- [ ] Scoring integration added
- [ ] Unit tests written and passing

---

**END OF FEATURE REQUEST**
