# Feature Request: Sack Rate (DST)

**Metric ID:** M42
**Priority:** MEDIUM
**Positions:** DST
**Effort Estimate:** 2-3 hours
**Expected Impact:** 6-8% improvement in DST floor prediction

---

## What This Metric Is

Sack Rate measures a defense's ability to generate sacks per game. Sacks are reliable fantasy scoring events (typically 1 point each) with less variance than turnovers. A defense with high sack production has a more predictable fantasy floor, while pass rush ability also correlates with forcing turnovers.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify pass rush strength**: Sack-heavy defenses have consistent fantasy floors
- **Predict DST reliability**: Sacks are more consistent than turnovers week-to-week
- **Complement turnover metrics**: Adds another DST evaluation dimension
- **Support streaming decisions**: High sack teams are safer plays
- **Evaluate defensive pressure**: Sacks indicate overall defensive effectiveness

**Example Use Case:**
> A DST averaging 3.5 sacks/game will reliably score 3-4 points from sacks alone, providing a floor. A DST averaging 1.5 sacks/game has less predictable scoring.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:** `data/player_data/dst_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `defense.sacks` | float | Yes (17 weeks) | dst_data.json | 4.0 |

**Example Data Structure:**
```json
{
  "id": "100029",
  "name": "Cowboys D/ST",
  "team": "DAL",
  "position": "DST",
  "defense": {
    "sacks": [4.0, 3.0, 5.0, 0.0, 3.0, 4.0, 2.0, 5.0, 3.0, 4.0, 3.0, 5.0, 4.0, 2.0, 4.0, 3.0, 0.0],
    "interceptions": [1.0, 2.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 1.0, 2.0, 1.0, 0.0, 1.0, 2.0, 1.0, 0.0, 0.0],
    "pts_g": [17.0, 21.0, 28.0, 0.0, 24.0, 20.0, 31.0, 17.0, 21.0, 24.0, 17.0, 28.0, 21.0, 14.0, 24.0, 21.0, 0.0]
  }
}
```

### Data Validation
- Data verified in: `data/player_data/dst_data.json`
- Weekly granularity: Yes (17 weeks per season)
- Historical availability: Current season
- Known limitations: Bye weeks show as 0.0 (need to exclude)

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_sack_rate(dst: FantasyPlayer) -> dict:
    """
    Calculate sack rate for a defense.

    Args:
        dst: FantasyPlayer object (DST position)

    Returns:
        dict: {
            'sacks_per_game': float,
            'total_sacks': int,
            'games_played': int,
            'sack_tier': str
        }

    Example:
        >>> dst = FantasyPlayer(name="Cowboys D/ST", stats={...})
        >>> result = calculate_sack_rate(dst)
        >>> result
        {'sacks_per_game': 3.6, 'total_sacks': 54, 'games_played': 15, 'sack_tier': 'EXCELLENT'}
    """
    weekly_sacks = dst.stats.get('defense', {}).get('sacks', [])

    # Filter out bye weeks (0 sacks with no other activity)
    # Use pts_g or interceptions to detect actual games vs byes
    pts_g = dst.stats.get('defense', {}).get('pts_g', [0] * len(weekly_sacks))

    active_sacks = []
    for sacks, pts in zip(weekly_sacks, pts_g):
        if pts > 0 or sacks > 0:  # Real game (even if 0 sacks)
            active_sacks.append(sacks)

    if len(active_sacks) < 3:
        return {
            'sacks_per_game': 0.0,
            'total_sacks': 0,
            'games_played': len(active_sacks),
            'sack_tier': 'INSUFFICIENT_DATA'
        }

    total_sacks = sum(active_sacks)
    games_played = len(active_sacks)
    sacks_per_game = total_sacks / games_played

    # Determine tier
    if sacks_per_game >= 3.5:
        sack_tier = 'EXCELLENT'
    elif sacks_per_game >= 2.8:
        sack_tier = 'GOOD'
    elif sacks_per_game >= 2.0:
        sack_tier = 'AVERAGE'
    elif sacks_per_game >= 1.5:
        sack_tier = 'POOR'
    else:
        sack_tier = 'VERY_POOR'

    return {
        'sacks_per_game': round(sacks_per_game, 2),
        'total_sacks': int(total_sacks),
        'games_played': games_played,
        'sack_tier': sack_tier
    }
```

### Thresholds & Tiers

**Sacks Per Game Thresholds:**

| Tier | Sacks/Game | Description | Multiplier | Example Team |
|------|------------|-------------|------------|--------------|
| EXCELLENT | >= 3.5 | Elite pass rush | 1.04 | Top-5 sack teams |
| GOOD | 2.8 - 3.49 | Above average | 1.02 | Top-10 sack teams |
| AVERAGE | 2.0 - 2.79 | League average | 1.0 | Most DSTs |
| POOR | 1.5 - 1.99 | Below average | 0.98 | Weak pass rush |
| VERY_POOR | < 1.5 | No pass rush | 0.96 | Bottom-5 teams |

### Edge Cases

**1. Bye Week Detection**
- **Scenario:** Week with 0 sacks - bye or actual game?
- **Handling:** Check pts_g - if also 0, it's a bye; if pts_g > 0, it's a real game with 0 sacks
- **Example:** 0 sacks, 0 pts_g = bye; 0 sacks, 24 pts_g = real game

**2. Outlier Sack Games**
- **Scenario:** 8+ sack game skews average
- **Handling:** Include in calculation (reflects real defensive ability)

---

## Implementation Plan

### Phase 1: Calculation Module (Estimated: 1 hour)

**File:** `league_helper/util/SackRateCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class SackRateCalculator:
    """Calculate sack rate for DST players"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate sack rate and return multiplier.

        Args:
            player: DST player to calculate for

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'DST':
            return 1.0, "N/A"

        metrics = self._calculate_sack_metrics(player)

        if metrics['sack_tier'] == 'INSUFFICIENT_DATA':
            return 1.0, "INSUFFICIENT_DATA"

        tier = metrics['sack_tier']
        multiplier = self._get_multiplier(tier)

        return multiplier, tier

    def _calculate_sack_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate sack rate metrics"""
        # Implementation from formula above
        pass

    def _get_multiplier(self, tier: str) -> float:
        """Get multiplier for sack tier"""
        multipliers = self.config.sack_rate_scoring.get('MULTIPLIERS', {})
        base_mult = multipliers.get(tier, 1.0)
        weight = self.config.sack_rate_scoring.get('WEIGHT', 1.0)
        return base_mult ** weight
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**Add to league_config.json:**

```json
{
  "SACK_RATE_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 3.5,
      "GOOD": 2.8,
      "AVERAGE": 2.0,
      "POOR": 1.5
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.04,
      "GOOD": 1.02,
      "AVERAGE": 1.0,
      "POOR": 0.98,
      "VERY_POOR": 0.96
    },
    "WEIGHT": 1.0,
    "MIN_GAMES": 3,
    "DESCRIPTION": "DST sack rate - sacks per game as floor indicator"
  }
}
```

---

### Phase 3: Testing (Estimated: 0.5 hours)

**Unit Tests:**

```python
class TestSackRateCalculator:

    def test_elite_pass_rush(self, calculator):
        """Test DST with elite sack production"""
        dst = create_dst(
            sacks=[4, 5, 3, 4, 5, 3, 4, 4, 5, 3, 4, 5, 3, 4, 4],
            pts_g=[17, 21, 28, 24, 20, 31, 17, 21, 24, 17, 28, 21, 14, 24, 21]
        )
        # ~4.0 sacks/game

        multiplier, tier = calculator.calculate(dst)

        assert tier == "EXCELLENT"
        assert multiplier > 1.0

    def test_weak_pass_rush(self, calculator):
        """Test DST with poor sack production"""
        dst = create_dst(
            sacks=[1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1],
            pts_g=[24, 28, 31, 27, 24, 28, 21, 28, 24, 31, 27, 24, 28, 21, 27]
        )
        # ~1.3 sacks/game

        multiplier, tier = calculator.calculate(dst)

        assert tier == "VERY_POOR"
        assert multiplier < 1.0

    def test_bye_week_detection(self, calculator):
        """Test bye week is excluded"""
        dst = create_dst(
            sacks=[4, 3, 0, 4, 3],  # Week 3 could be bye or 0-sack game
            pts_g=[17, 21, 0, 24, 20]  # Week 3 pts_g=0 confirms bye
        )

        metrics = calculator._calculate_sack_metrics(dst)

        assert metrics['games_played'] == 4  # Excludes bye
```

---

## Real-World Examples

### Example 1: Elite Pass Rush

**Dallas Cowboys D/ST:**

| Metric | Value |
|--------|-------|
| Weekly Sacks | 4, 5, 3, 4, 5, 3, 4, 4, 5, 3, 4, 5, 3, 4, 4 |
| Total Sacks | 60 |
| Games Played | 15 |
| Sacks/Game | 4.0 |
| Tier | EXCELLENT |
| Multiplier | 1.04 |

**Reason String:** `"Sack Rate (EXCELLENT): 4.0 sacks/g (60 total)"`

### Example 2: Weak Pass Rush

**Struggling D/ST:**

| Metric | Value |
|--------|-------|
| Weekly Sacks | 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1 |
| Total Sacks | 20 |
| Games Played | 15 |
| Sacks/Game | 1.33 |
| Tier | VERY_POOR |
| Multiplier | 0.96 |

**Reason String:** `"Sack Rate (VERY_POOR): 1.3 sacks/g (20 total)"`

---

## Dependencies

### Data Dependencies
- `defense.sacks` - Available in `data/player_data/dst_data.json`
- `defense.pts_g` - Available (used for bye detection)

### Code Dependencies
- `ConfigManager` - Existing
- `FantasyPlayer` - Existing
- `SackRateCalculator` - To be created

---

## Related Metrics

**Complementary Metrics:**
- **M41 (Turnover Rate)** - Another DST playmaking metric
- **M43 (Points Allowed Trend)** - Defensive performance
- **M44 (Opponent Strength)** - Matchup context

---

## Implementation Checklist

- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed
- [ ] SackRateCalculator module created
- [ ] Scoring integration added
- [ ] Unit tests written and passing

---

**END OF FEATURE REQUEST**
