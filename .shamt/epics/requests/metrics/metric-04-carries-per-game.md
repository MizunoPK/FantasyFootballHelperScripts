# Feature Request: Carries Per Game (RB Volume Floor)

**Metric ID:** M04
**Priority:** HIGH
**Positions:** RB
**Effort Estimate:** 3-4 hours
**Expected Impact:** 10-15% improvement in RB weekly decisions

---

## What This Metric Is

Carries Per Game measures a running back's average rushing attempts per game, providing a volume floor indicator. This metric identifies workhorse backs (20+ carries), lead backs (15-19), committee backs (10-14), and backup RBs (<10 carries).

---

## What We're Trying to Accomplish

**Goals:**
- **Identify bell cow RBs**: Workhorses with 20+ carries/game have elite volume advantage and injury-protected value
- **Detect committee situations**: 10-14 carries means unpredictable week-to-week usage and lower floor
- **Value handcuffs properly**: Backup RBs with <10 carries but "next man up" potential provide injury insurance
- **Predict touchdown regression**: High TD rate + low carry volume = unsustainable (TDs will decline without volume)
- **Volume = opportunity**: More carries create more scoring chances, regardless of efficiency

**Example Use Case:**
> An RB with 65% carry share averaging 20 carries/game is far more valuable than an RB with 35% share averaging 11 carries/game, even with similar yards per carry. The 20-carry back gets ~18 more scoring opportunities per game (9 extra carries × 2 games = 18 touches), leading to more TDs and yards simply through volume.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/rb_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `rushing.attempts` | float | Yes (17 weeks) | RB JSON | 18.0 |
| `position` | string | No | All player JSON | "RB" |

**Example Data Structure:**
```json
{
  "id": "4241985",
  "name": "Saquon Barkley",
  "team": "PHI",
  "position": "RB",
  "rushing": {
    "attempts": [20.0, 18.0, 22.0, 0.0, 19.0, 21.0, ...],  // 17 weeks
    "rush_yds": [109.0, 87.0, 147.0, 0.0, 96.0, 118.0, ...],
    "rush_tds": [1.0, 0.0, 2.0, 0.0, 1.0, 1.0, ...]
  },
  "receiving": {
    "targets": [5.0, 4.0, 6.0, 0.0, 5.0, 4.0, ...]
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
def calculate_carries_per_game(player: FantasyPlayer) -> dict:
    """
    Calculate carries per game for an RB.

    Args:
        player: FantasyPlayer object with rushing stats

    Returns:
        dict: {
            'carries_per_game': float,
            'season_carries': int,
            'games_played': int,
            'tier': str
        }

    Example:
        >>> player = FantasyPlayer(name="Saquon Barkley", position="RB", stats={...})
        >>> result = calculate_carries_per_game(player)
        >>> result
        {'carries_per_game': 20.3, 'season_carries': 305, 'games_played': 15, 'tier': 'EXCELLENT'}
    """
    if player.position != 'RB':
        return {
            'carries_per_game': 0.0,
            'season_carries': 0,
            'games_played': 0,
            'tier': 'N/A'
        }

    # Step 1: Get weekly carries
    weekly_carries = player.stats['rushing']['attempts']

    # Step 2: Count games played (exclude bye weeks and injuries)
    games_played = len([c for c in weekly_carries if c > 0])

    # Step 3: Calculate season total
    season_carries = sum(weekly_carries)

    # Step 4: Calculate carries per game
    if games_played > 0:
        carries_per_game = season_carries / games_played
    else:
        carries_per_game = 0.0

    # Step 5: Determine tier
    tier = _classify_carries_tier(carries_per_game)

    return {
        'carries_per_game': round(carries_per_game, 1),
        'season_carries': season_carries,
        'games_played': games_played,
        'tier': tier
    }

def _classify_carries_tier(carries_per_game: float) -> str:
    """Classify RB tier based on carries per game"""
    if carries_per_game >= 20.0:
        return "EXCELLENT"  # Bell cow
    elif carries_per_game >= 15.0:
        return "GOOD"       # Lead back
    elif carries_per_game >= 10.0:
        return "AVERAGE"    # Committee
    elif carries_per_game >= 5.0:
        return "POOR"       # Limited role
    else:
        return "VERY_POOR"  # Backup
```

### Thresholds & Tiers

**RB Carries Per Game:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | ≥20 carries/game | Bell cow RB | 1.05 | Derrick Henry, Saquon Barkley |
| GOOD | 15-19 carries/game | Lead back | 1.025 | Josh Jacobs, Tony Pollard |
| AVERAGE | 10-14 carries/game | Committee back | 1.0 | RBBC situations |
| POOR | 5-9 carries/game | Limited role | 0.975 | Backup/3rd down back |
| VERY_POOR | <5 carries/game | Backup | 0.95 | Depth RB |

### Edge Cases

**1. Pass-Catching Specialist RB**
- **Scenario:** RB with low carries (8/game) but high targets (7/game) = 15 total touches
- **Handling:** This metric penalizes them, but M58 (Total Opportunity Share) captures full value
- **Example:** Austin Ekeler historically had 12 carries but 8 targets = 20 opportunities/game

**2. Timeshare/Committee Backfield**
- **Scenario:** Two RBs splitting 50/50 (each 12-13 carries/game)
- **Handling:** Both classified as AVERAGE tier, neither gets boost
- **Example:** Miami Dolphins RBBC with Mostert/Achane

**3. Goal-Line Specialist**
- **Scenario:** RB with 6 carries/game but 10 TDs (high TD rate, low volume)
- **Handling:** Penalized by carries metric, flagged for TD regression in M59 (TD Dependency)
- **Example:** Latavius Murray types - unsustainable scoring

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**File:** `league_helper/util/CarriesPerGameCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class CarriesPerGameCalculator:
    """Calculate carries per game for RBs"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate carries per game and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'RB':
            return 1.0, "N/A"

        # Calculate carries metrics
        metrics = self._calculate_carries_metrics(player)

        # Get multiplier
        multiplier = self.config.get_carries_per_game_multiplier(metrics['tier'])

        return multiplier, metrics['tier']
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "CARRIES_PER_GAME_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 20.0,
      "GOOD": 15.0,
      "AVERAGE": 10.0,
      "POOR": 5.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.05,
      "GOOD": 1.025,
      "AVERAGE": 1.0,
      "POOR": 0.975,
      "VERY_POOR": 0.95
    },
    "WEIGHT": 2.5,
    "MIN_WEEKS": 3,
    "DESCRIPTION": "RB carries per game - volume floor indicator"
  }
}
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_carries_per_game_scoring()`

```python
def _apply_carries_per_game_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply carries per game adjustment (RB only)"""
    if p.position != 'RB':
        return player_score, ""

    if not self.config.carries_per_game_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = CarriesPerGameCalculator(self.config)
    multiplier, tier = calculator.calculate(p)

    adjusted_score = player_score * multiplier

    metrics = calculator._calculate_carries_metrics(p)
    reason = f"Carries/Game ({tier}): {metrics['carries_per_game']:.1f}"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_CarriesPerGameCalculator.py`

```python
class TestCarriesPerGameCalculator:
    def test_bell_cow_rb(self, calculator):
        """Test RB with 20+ carries/game"""
        player = FantasyPlayer(
            name="Derrick Henry",
            position="RB",
            stats={
                'rushing': {
                    'attempts': [22, 20, 24, 0, 21, 23, 19, 22, 20, 21, 20, 23, 19, 22, 21, 20, 22]
                }
            }
        )

        multiplier, tier = calculator.calculate(player)

        assert tier == "EXCELLENT"
        assert multiplier > 1.04

    def test_committee_rb(self, calculator):
        """Test RB in committee (10-14 carries)"""
        player = FantasyPlayer(
            position="RB",
            stats={
                'rushing': {
                    'attempts': [12, 11, 13, 0, 12, 10, 14, 11, 13, 12]
                }
            }
        )

        multiplier, tier = calculator.calculate(player)

        assert tier == "AVERAGE"
        assert multiplier == pytest.approx(1.0, abs=0.01)
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 12-18%
- Rationale: Identifies workhorse RBs vs committee backs early in draft

**Starter Helper Mode:**
- Expected improvement: 10-15%
- Rationale: Volume = fantasy points; bell cows have highest floor/ceiling

**Trade Simulator Mode:**
- Expected improvement: 12-15%
- Rationale: Separates RB1s from RBBC backs for trade value

---

## Real-World Examples

### Example 1: Bell Cow RB

**Derrick Henry (BAL, RB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Season Carries | 327 |
| Games Played | 15 |
| Carries/Game | 21.8 |
| Tier | EXCELLENT |
| Multiplier | 1.05^2.5 = 1.1314 |
| Base Score | 185.0 |
| Adjusted Score | 209.3 (+24.3 pts) |

**Reason String:** `"Carries/Game (EXCELLENT): 21.8"`

### Example 2: Committee RB

**Committee RB (Team, RB)** - RBBC:

| Metric | Value |
|--------|-------|
| Season Carries | 156 |
| Games Played | 13 |
| Carries/Game | 12.0 |
| Tier | AVERAGE |
| Multiplier | 1.0^2.5 = 1.0 |
| Base Score | 120.0 |
| Adjusted Score | 120.0 (no change) |

**Reason String:** `"Carries/Game (AVERAGE): 12.0"`

---

## Dependencies

### Data Dependencies
- ✅ `rushing.attempts` - Available in `data/player_data/rb_data.json`

### Code Dependencies
- 🆕 `CarriesPerGameCalculator` - To be created

---

## Implementation Checklist

**Implementation:**
- [ ] CarriesPerGameCalculator module created
- [ ] Scoring integration added
- [ ] Configuration file updated

**Testing:**
- [ ] Unit tests written and passing
- [ ] Real data validation complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add carries per game scoring (Step 16)"

---

**END OF FEATURE REQUEST**
