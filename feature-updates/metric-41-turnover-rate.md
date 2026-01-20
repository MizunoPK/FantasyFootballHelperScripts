# Feature Request: Turnover Rate (DST)

**Metric ID:** M41
**Priority:** HIGH
**Positions:** DST
**Effort Estimate:** 2-3 hours
**Expected Impact:** 8-12% improvement in DST scoring predictions

---

## What This Metric Is

Turnover Rate measures a defense's ability to generate turnovers (interceptions + fumble recoveries) per game. Turnovers are high-value scoring events in fantasy (typically 2 points each) and directly correlate with defensive fantasy output. This metric identifies defenses with playmaking ability vs. those relying solely on points/yards allowed.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify playmaking defenses**: High turnover teams score bonus fantasy points
- **Predict fantasy floor/ceiling**: Turnovers are volatile but some defenses create more opportunities
- **Evaluate DST beyond points allowed**: A defense allowing 24 points but getting 3 turnovers can outscore one allowing 17 with 0 turnovers
- **Support streaming decisions**: Weekly DST selection benefits from turnover tendency
- **Historical consistency**: Some defenses consistently generate turnovers year over year

**Example Use Case:**
> A DST that generates 2.5 turnovers/game with average points allowed will typically outscore a DST with 0.8 turnovers/game but slightly better points allowed. Turnovers are worth 2+ fantasy points each, so 1.7 extra turnovers = 3.4+ extra points per game.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:** `data/player_data/dst_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `defense.interceptions` | float | Yes (17 weeks) | dst_data.json | 2.0 |
| `defense.fumbles_recovered` | float | Yes (17 weeks) | dst_data.json | 1.0 |

**Example Data Structure:**
```json
{
  "id": "100029",
  "name": "Cowboys D/ST",
  "team": "DAL",
  "position": "DST",
  "defense": {
    "interceptions": [1.0, 2.0, 0.0, 1.0, 3.0, 1.0, 0.0, 2.0, 1.0, 1.0, 0.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0],
    "fumbles_recovered": [0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0],
    "sacks": [3.0, 2.0, 4.0, 1.0, 3.0, 2.0, 5.0, 2.0, 3.0, 4.0, 2.0, 3.0, 2.0, 4.0, 3.0, 2.0, 3.0],
    "def_td": [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0],
    "pts_g": [17.0, 21.0, 28.0, 14.0, 24.0, 20.0, 31.0, 17.0, 21.0, 24.0, 17.0, 28.0, 21.0, 14.0, 24.0, 21.0, 17.0],
    "yds_g": [320.0, 350.0, 410.0, 280.0, 370.0, 340.0, 420.0, 310.0, 360.0, 380.0, 300.0, 400.0, 350.0, 290.0, 370.0, 340.0, 310.0]
  }
}
```

### Data Validation
- Data verified in: `data/player_data/dst_data.json`
- Weekly granularity: Yes (17 weeks per season)
- Historical availability: Current season
- Known limitations: None - all turnover data is directly available

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_turnover_rate(dst: FantasyPlayer) -> dict:
    """
    Calculate turnover rate for a defense.

    Args:
        dst: FantasyPlayer object (DST position)

    Returns:
        dict: {
            'turnovers_per_game': float,
            'total_interceptions': int,
            'total_fumbles_recovered': int,
            'total_turnovers': int,
            'games_played': int
        }

    Example:
        >>> dst = FantasyPlayer(name="Cowboys D/ST", stats={...})
        >>> result = calculate_turnover_rate(dst)
        >>> result
        {'turnovers_per_game': 1.8, 'total_interceptions': 19, 'total_fumbles_recovered': 10,
         'total_turnovers': 29, 'games_played': 16}
    """
    # Step 1: Get weekly turnovers
    weekly_ints = dst.stats['defense']['interceptions']
    weekly_fumbles = dst.stats['defense']['fumbles_recovered']

    # Step 2: Calculate totals
    total_ints = sum(weekly_ints)
    total_fumbles = sum(weekly_fumbles)
    total_turnovers = total_ints + total_fumbles

    # Step 3: Calculate games played (weeks with any defensive stats)
    games_played = len([i for i, (ints, fum) in enumerate(zip(weekly_ints, weekly_fumbles))
                        if ints > 0 or fum > 0 or dst.stats['defense']['sacks'][i] > 0])

    # Handle bye weeks - count weeks with actual game activity
    if games_played == 0:
        games_played = len([w for w in weekly_ints if w is not None])

    # Step 4: Calculate turnovers per game
    if games_played > 0:
        turnovers_per_game = total_turnovers / games_played
    else:
        turnovers_per_game = 0.0

    return {
        'turnovers_per_game': round(turnovers_per_game, 2),
        'total_interceptions': int(total_ints),
        'total_fumbles_recovered': int(total_fumbles),
        'total_turnovers': int(total_turnovers),
        'games_played': games_played
    }
```

### Thresholds & Tiers

**DST Turnover Rate:**

| Tier | Threshold (TO/game) | Description | Multiplier | Example Team |
|------|---------------------|-------------|------------|--------------|
| EXCELLENT | >= 2.0 | Elite playmakers | 1.06 | DAL, SF elite years |
| GOOD | 1.5 - 1.99 | Above average | 1.03 | Most top-10 DSTs |
| AVERAGE | 1.0 - 1.49 | League average | 1.0 | Average DST |
| POOR | 0.5 - 0.99 | Below average | 0.97 | Struggling defenses |
| VERY_POOR | < 0.5 | No playmaking | 0.94 | Worst DSTs |

### Edge Cases

**1. Bye Week Handling**
- **Scenario:** DST has 0 turnovers in bye week
- **Handling:** Exclude bye week from games_played count
- **Example:** DST with [2, 1, 0, 3] where week 3 is bye = 3 games played, 2.0 TO/game

**2. All Zeros Week (Active Game, No Turnovers)**
- **Scenario:** DST played but got 0 INT and 0 fumbles
- **Handling:** Still counts as game played (check sacks/pts_g for activity)
- **Example:** Week with 0 TO but 3 sacks = game played, just no turnovers

**3. Extreme Outlier Games**
- **Scenario:** 6+ turnovers in one game skews average
- **Handling:** Optional cap at 4 turnovers per game for averaging
- **Example:** 5 INT game counts as 4 for tier calculation

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**1.1 Verify Data Availability**
- [x] Confirm `defense.interceptions` exists in dst_data.json
- [x] Confirm `defense.fumbles_recovered` exists in dst_data.json
- [x] Test data extraction with sample DSTs
- [x] Validate data ranges (0-5 turnovers typical per game)

**1.2 Create Calculation Module**

**File:** `league_helper/util/TurnoverRateCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class TurnoverRateCalculator:
    """Calculate turnover rate for DST players"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate turnover rate and return multiplier.

        Args:
            player: DST player to calculate for

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'DST':
            return 1.0, "N/A"

        # Calculate turnover metrics
        metrics = self._calculate_turnover_metrics(player)

        # Get tier
        tier = self._get_tier(metrics['turnovers_per_game'])

        # Get multiplier from config
        multiplier = self._get_multiplier(tier)

        return multiplier, tier

    def _calculate_turnover_metrics(self, player: FantasyPlayer) -> Dict:
        """Calculate turnover rate metrics"""
        weekly_ints = player.stats.get('defense', {}).get('interceptions', [])
        weekly_fumbles = player.stats.get('defense', {}).get('fumbles_recovered', [])

        total_ints = sum(weekly_ints)
        total_fumbles = sum(weekly_fumbles)
        total_turnovers = total_ints + total_fumbles

        # Count games with defensive activity
        weekly_sacks = player.stats.get('defense', {}).get('sacks', [0] * len(weekly_ints))
        games_played = sum(1 for i in range(len(weekly_ints))
                          if weekly_ints[i] > 0 or weekly_fumbles[i] > 0 or weekly_sacks[i] > 0)

        if games_played == 0:
            games_played = max(1, len([w for w in weekly_ints if w is not None and w >= 0]))

        turnovers_per_game = total_turnovers / games_played if games_played > 0 else 0.0

        return {
            'turnovers_per_game': round(turnovers_per_game, 2),
            'total_interceptions': int(total_ints),
            'total_fumbles_recovered': int(total_fumbles),
            'total_turnovers': int(total_turnovers),
            'games_played': games_played
        }

    def _get_tier(self, to_per_game: float) -> str:
        """Determine tier based on turnovers per game"""
        thresholds = self.config.turnover_rate_scoring.get('THRESHOLDS', {})

        if to_per_game >= thresholds.get('EXCELLENT', 2.0):
            return "EXCELLENT"
        elif to_per_game >= thresholds.get('GOOD', 1.5):
            return "GOOD"
        elif to_per_game >= thresholds.get('AVERAGE', 1.0):
            return "AVERAGE"
        elif to_per_game >= thresholds.get('POOR', 0.5):
            return "POOR"
        else:
            return "VERY_POOR"

    def _get_multiplier(self, tier: str) -> float:
        """Get multiplier for tier"""
        multipliers = self.config.turnover_rate_scoring.get('MULTIPLIERS', {})
        base_mult = multipliers.get(tier, 1.0)
        weight = self.config.turnover_rate_scoring.get('WEIGHT', 1.5)
        return base_mult ** weight
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**2.1 Add to league_config.json**

```json
{
  "TURNOVER_RATE_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 2.0,
      "GOOD": 1.5,
      "AVERAGE": 1.0,
      "POOR": 0.5
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
    "TURNOVER_CAP_PER_GAME": 4,
    "DESCRIPTION": "DST turnover rate - interceptions plus fumble recoveries per game"
  }
}
```

---

### Phase 3: Scoring Integration (Estimated: 0.5 hours)

**3.1 Add Scoring Step**

**File:** `league_helper/util/player_scoring.py`

```python
def _apply_turnover_rate_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply turnover rate adjustment to DST score.

    Args:
        p: FantasyPlayer object (DST)
        player_score: Current player score

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    if p.position != 'DST':
        return player_score, ""

    if not self.config.turnover_rate_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = TurnoverRateCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    adjusted_score = player_score * multiplier

    metrics = calculator._calculate_turnover_metrics(p)
    reason = f"Turnover Rate ({tier}): {metrics['turnovers_per_game']:.2f} TO/g ({metrics['total_interceptions']} INT, {metrics['total_fumbles_recovered']} FR)"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**4.1 Unit Tests**

**File:** `tests/league_helper/util/test_TurnoverRateCalculator.py`

```python
import pytest
from league_helper.util.TurnoverRateCalculator import TurnoverRateCalculator

class TestTurnoverRateCalculator:
    """Test turnover rate calculation"""

    def test_excellent_tier_dst(self, calculator):
        """Test DST with 2.0+ turnovers per game"""
        dst = create_dst(
            name="Cowboys D/ST",
            interceptions=[2, 1, 3, 0, 2, 1, 2, 3, 1, 2, 2, 1, 3, 2, 1, 2, 1],  # 29 INT
            fumbles_recovered=[1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 10 FR
        )
        # Total: 39 TO in 17 games = 2.29 TO/game

        multiplier, tier = calculator.calculate(dst)

        assert tier == "EXCELLENT"
        assert multiplier > 1.0

    def test_poor_tier_dst(self, calculator):
        """Test DST with low turnover rate"""
        dst = create_dst(
            name="Bad D/ST",
            interceptions=[0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],  # 5 INT
            fumbles_recovered=[0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]  # 4 FR
        )
        # Total: 9 TO in 17 games = 0.53 TO/game

        multiplier, tier = calculator.calculate(dst)

        assert tier == "POOR"
        assert multiplier < 1.0

    def test_bye_week_exclusion(self, calculator):
        """Test bye week is excluded from games played"""
        dst = create_dst(
            name="Test D/ST",
            interceptions=[2, 2, 0, 2, 2],  # Week 3 is bye (0 activity)
            fumbles_recovered=[1, 1, 0, 1, 1],
            sacks=[3, 2, 0, 4, 3]  # Week 3 also 0 sacks = bye
        )
        # 12 TO in 4 games (excluding bye) = 3.0 TO/game

        metrics = calculator._calculate_turnover_metrics(dst)

        assert metrics['games_played'] == 4
        assert metrics['turnovers_per_game'] == 3.0
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 6-8%
- Rationale: Identifies defenses with playmaking upside during draft

**Starter Helper Mode:**
- Expected improvement: 8-12%
- Rationale: Turnover-prone defenses have higher weekly ceilings

**Trade Simulator Mode:**
- Expected improvement: 5-8%
- Rationale: Evaluates DST value beyond simple points allowed

---

## Real-World Examples

### Example 1: Elite Playmaking Defense

**Dallas Cowboys D/ST** - 2024 Season (Hypothetical Elite Year):

| Metric | Value |
|--------|-------|
| Total Interceptions | 22 |
| Total Fumbles Recovered | 12 |
| Total Turnovers | 34 |
| Games Played | 16 |
| Turnovers/Game | 2.13 |
| Tier | EXCELLENT |
| Multiplier | 1.06^1.5 = 1.0915 |
| Base Score | 120.0 |
| Adjusted Score | 131.0 (+11.0 pts) |

**Reason String:** `"Turnover Rate (EXCELLENT): 2.13 TO/g (22 INT, 12 FR)"`

### Example 2: Average Defense

**Generic Average D/ST** - 2024 Season:

| Metric | Value |
|--------|-------|
| Total Interceptions | 12 |
| Total Fumbles Recovered | 8 |
| Total Turnovers | 20 |
| Games Played | 16 |
| Turnovers/Game | 1.25 |
| Tier | AVERAGE |
| Multiplier | 1.0^1.5 = 1.0 |

**Reason String:** `"Turnover Rate (AVERAGE): 1.25 TO/g (12 INT, 8 FR)"`

### Example 3: Poor Playmaking Defense

**Struggling D/ST** - 2024 Season:

| Metric | Value |
|--------|-------|
| Total Interceptions | 6 |
| Total Fumbles Recovered | 5 |
| Total Turnovers | 11 |
| Games Played | 16 |
| Turnovers/Game | 0.69 |
| Tier | POOR |
| Multiplier | 0.97^1.5 = 0.9549 |
| Base Score | 100.0 |
| Adjusted Score | 95.5 (-4.5 pts) |

**Reason String:** `"Turnover Rate (POOR): 0.69 TO/g (6 INT, 5 FR)"`

---

## Dependencies

### Data Dependencies
- `defense.interceptions` - Available in `data/player_data/dst_data.json`
- `defense.fumbles_recovered` - Available in `data/player_data/dst_data.json`
- `defense.sacks` - Available (used for game activity detection)

### Code Dependencies
- `ConfigManager` - Existing
- `FantasyPlayer` - Existing
- `TurnoverRateCalculator` - To be created

---

## Risks & Mitigations

### Risk 1: Turnover Volatility
**Likelihood:** High | **Impact:** Medium

**Description:** Turnovers are inherently volatile week-to-week

**Mitigation:** Use season-long average, require MIN_GAMES (3), apply moderate WEIGHT

### Risk 2: Scheme vs. Opponent Quality
**Likelihood:** Medium | **Impact:** Low

**Description:** Some turnovers come from facing bad QBs, not defense skill

**Mitigation:** This is still predictive; defenses that force turnovers tend to continue doing so

---

## Open Questions

**Questions for User:**
1. Should turnover TDs (pick-6, fumble return TD) be weighted separately or included in this metric?
2. Cap individual game turnovers at 4 for averaging to reduce outlier impact?

---

## Related Metrics

**Complementary Metrics:**
- **M42 (Sack Rate)** - Another DST playmaking metric
- **M43 (Points Allowed Trend)** - Traditional DST scoring component
- **M44 (Opponent Offensive Strength)** - Context for DST matchups

---

## Implementation Checklist

**Pre-Implementation:**
- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed
- [ ] User questions answered

**Implementation:**
- [ ] TurnoverRateCalculator module created
- [ ] Scoring integration added
- [ ] Configuration file updated

**Testing:**
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Validation against real DST data

**Documentation:**
- [ ] Scoring step documentation created
- [ ] README updated

---

**END OF FEATURE REQUEST**
