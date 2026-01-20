# Feature Request: Recent Form (Rolling 4-Week Average)

**Metric ID:** M34
**Priority:** MEDIUM
**Positions:** All (QB, RB, WR, TE, K, DST)
**Effort Estimate:** 2-3 hours
**Expected Impact:** 5-8% improvement in weekly lineup decisions based on recent performance trends

---

## What This Metric Is

Recent Form measures a player's average fantasy production over the last 4 games, providing a momentum-based view of current performance. This captures hot streaks, cold spells, and recent usage changes that season-long averages miss. Players trending up get boosted; those trending down get penalized.

---

## What We're Trying to Accomplish

**Goals:**
- **Capture momentum**: Identify players on hot/cold streaks
- **React to usage changes**: New starter, increased role, or reduced snaps
- **Improve weekly decisions**: Recent performance is more predictive than season average
- **Complement season-long metrics**: Adds recency weighting to existing calculations
- **Support streaming positions**: K and DST benefit significantly from form analysis

**Example Use Case:**
> A WR averaging 12 PPG on the season but scoring 18, 22, 16, 20 over the last 4 weeks (19 PPG recent) is performing above baseline. Conversely, a WR averaging 15 PPG but scoring 8, 6, 10, 9 recently (8.25 PPG) is trending down.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:** `data/player_data/[position]_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `actual_points` | float | Yes (17 weeks) | All position JSON | 18.5 |

**Example Data Structure:**
```json
{
  "id": "4241389",
  "name": "CeeDee Lamb",
  "team": "DAL",
  "position": "WR",
  "actual_points": [22.5, 15.3, 8.2, 0.0, 28.7, 12.4, 18.9, 24.1, 16.5, 21.3, 14.8, 19.2, 25.6, 11.4, 17.8, 22.1, 0.0]
}
```

### Data Validation
- Data verified in: All `data/player_data/*_data.json` files
- Weekly granularity: Yes (17 weeks per season)
- Historical availability: Current season
- Known limitations: Bye weeks show as 0.0 (need to exclude from average)

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_recent_form(player: FantasyPlayer, current_week: int, window_size: int = 4) -> dict:
    """
    Calculate recent form based on rolling average.

    Args:
        player: FantasyPlayer object with actual_points
        current_week: Current NFL week (1-indexed)
        window_size: Number of recent games to average (default 4)

    Returns:
        dict: {
            'recent_avg': float,           # Average of last N games
            'season_avg': float,           # Season-long average
            'form_ratio': float,           # recent_avg / season_avg
            'form_trend': str,             # HOT, WARM, NEUTRAL, COLD, ICE_COLD
            'games_in_window': int         # Actual games used (excluding byes)
        }

    Example:
        >>> player = FantasyPlayer(name="CeeDee Lamb", stats={'actual_points': [...]})
        >>> result = calculate_recent_form(player, current_week=15)
        >>> result
        {'recent_avg': 19.2, 'season_avg': 16.8, 'form_ratio': 1.14,
         'form_trend': 'HOT', 'games_in_window': 4}
    """
    actual_points = player.stats.get('actual_points', [])

    # Step 1: Get games played up to current week (exclude future weeks)
    games_played = actual_points[:current_week]

    # Step 2: Filter out bye weeks (0.0 points)
    active_games = [(i, pts) for i, pts in enumerate(games_played) if pts > 0]

    if len(active_games) < 2:
        return {
            'recent_avg': 0.0,
            'season_avg': 0.0,
            'form_ratio': 1.0,
            'form_trend': 'NEUTRAL',
            'games_in_window': 0
        }

    # Step 3: Calculate season average
    season_points = [pts for _, pts in active_games]
    season_avg = sum(season_points) / len(season_points)

    # Step 4: Get last N active games for recent average
    recent_games = active_games[-window_size:]
    recent_points = [pts for _, pts in recent_games]
    recent_avg = sum(recent_points) / len(recent_points)

    # Step 5: Calculate form ratio
    if season_avg > 0:
        form_ratio = recent_avg / season_avg
    else:
        form_ratio = 1.0

    # Step 6: Determine form trend
    if form_ratio >= 1.20:
        form_trend = 'HOT'
    elif form_ratio >= 1.08:
        form_trend = 'WARM'
    elif form_ratio >= 0.92:
        form_trend = 'NEUTRAL'
    elif form_ratio >= 0.80:
        form_trend = 'COLD'
    else:
        form_trend = 'ICE_COLD'

    return {
        'recent_avg': round(recent_avg, 1),
        'season_avg': round(season_avg, 1),
        'form_ratio': round(form_ratio, 3),
        'form_trend': form_trend,
        'games_in_window': len(recent_games)
    }
```

### Thresholds & Tiers

**Form Ratio Thresholds (Recent Avg / Season Avg):**

| Tier | Form Ratio | Description | Multiplier | Example |
|------|------------|-------------|------------|---------|
| HOT | >= 1.20 | 20%+ above season avg | 1.04 | Breakout player |
| WARM | 1.08 - 1.19 | 8-19% above average | 1.02 | Trending up |
| NEUTRAL | 0.92 - 1.07 | Within 8% of average | 1.0 | Consistent |
| COLD | 0.80 - 0.91 | 9-20% below average | 0.98 | Slumping |
| ICE_COLD | < 0.80 | 20%+ below average | 0.96 | Major decline |

### Edge Cases

**1. Bye Week in Window**
- **Scenario:** One of the last 4 weeks was a bye (0.0 points)
- **Handling:** Exclude bye from window, use next most recent game
- **Example:** Weeks 11-14 with bye in week 12 → use weeks 10, 11, 13, 14

**2. Early Season (Weeks 1-4)**
- **Scenario:** Less than 4 games played
- **Handling:** Use all available games, reduce weight for small samples
- **Example:** Week 3 → use 2-3 games with WEIGHT reduced to 0.5

**3. Injury Return**
- **Scenario:** Player returns from multi-week absence
- **Handling:** Only count games actually played (filter 0.0 weeks)
- **Example:** Missed weeks 8-11, returned week 12 → recent form starts week 12

**4. Zero Season Average**
- **Scenario:** New player with no games yet
- **Handling:** Return form_ratio = 1.0 (neutral), no adjustment
- **Example:** Week 1 → no historical data, skip metric

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**1.1 Create Calculation Module**

**File:** `league_helper/util/RecentFormCalculator.py`

```python
from typing import Tuple, Dict
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class RecentFormCalculator:
    """Calculate recent form based on rolling performance average"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()
        self.window_size = config_manager.recent_form_scoring.get('WINDOW_SIZE', 4)

    def calculate(self, player: FantasyPlayer, current_week: int) -> Tuple[float, str]:
        """
        Calculate recent form and return multiplier.

        Args:
            player: Player to calculate for
            current_week: Current NFL week

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        # Calculate form metrics
        metrics = self._calculate_form_metrics(player, current_week)

        if metrics['games_in_window'] < self.config.recent_form_scoring.get('MIN_GAMES', 2):
            return 1.0, "INSUFFICIENT_DATA"

        # Get tier and multiplier
        tier = metrics['form_trend']
        multiplier = self._get_multiplier(tier)

        return multiplier, tier

    def _calculate_form_metrics(self, player: FantasyPlayer, current_week: int) -> Dict:
        """Calculate recent form metrics"""
        # Implementation from formula above
        pass

    def _get_multiplier(self, tier: str) -> float:
        """Get multiplier for form tier"""
        multipliers = self.config.recent_form_scoring.get('MULTIPLIERS', {})
        base_mult = multipliers.get(tier, 1.0)
        weight = self.config.recent_form_scoring.get('WEIGHT', 1.0)
        return base_mult ** weight
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**2.1 Add to league_config.json**

```json
{
  "RECENT_FORM_SCORING": {
    "ENABLED": true,
    "WINDOW_SIZE": 4,
    "THRESHOLDS": {
      "HOT": 1.20,
      "WARM": 1.08,
      "COLD": 0.92,
      "ICE_COLD": 0.80
    },
    "MULTIPLIERS": {
      "HOT": 1.04,
      "WARM": 1.02,
      "NEUTRAL": 1.0,
      "COLD": 0.98,
      "ICE_COLD": 0.96
    },
    "WEIGHT": 1.0,
    "MIN_GAMES": 2,
    "EARLY_SEASON_WEIGHT": 0.5,
    "DESCRIPTION": "Recent form - rolling 4-week performance average vs season average"
  }
}
```

---

### Phase 3: Scoring Integration (Estimated: 0.5 hours)

**3.1 Add Scoring Step**

**File:** `league_helper/util/player_scoring.py`

```python
def _apply_recent_form_scoring(self, p: FantasyPlayer, player_score: float, current_week: int) -> Tuple[float, str]:
    """
    Apply recent form adjustment to player score.

    Args:
        p: FantasyPlayer object
        player_score: Current player score
        current_week: Current NFL week

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    if not self.config.recent_form_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = RecentFormCalculator(self.config)
    multiplier, tier = calculator.calculate(p, current_week)

    if tier == "INSUFFICIENT_DATA":
        return player_score, ""

    adjusted_score = player_score * multiplier

    metrics = calculator._calculate_form_metrics(p, current_week)
    reason = f"Recent Form ({tier}): {metrics['recent_avg']:.1f} PPG last {metrics['games_in_window']}g vs {metrics['season_avg']:.1f} season"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**4.1 Unit Tests**

**File:** `tests/league_helper/util/test_RecentFormCalculator.py`

```python
import pytest
from league_helper.util.RecentFormCalculator import RecentFormCalculator

class TestRecentFormCalculator:
    """Test recent form calculation"""

    def test_hot_streak_player(self, calculator):
        """Test player on hot streak gets boost"""
        player = create_player(
            name="Breakout WR",
            position="WR",
            actual_points=[10, 12, 11, 10, 12, 11, 10, 22, 25, 20, 24]  # Recent surge
        )
        # Season avg: ~15.2, Recent 4: ~22.75, Ratio: ~1.50

        multiplier, tier = calculator.calculate(player, current_week=11)

        assert tier == "HOT"
        assert multiplier > 1.0

    def test_cold_streak_player(self, calculator):
        """Test player on cold streak gets penalty"""
        player = create_player(
            name="Slumping RB",
            position="RB",
            actual_points=[20, 22, 18, 24, 20, 22, 18, 8, 6, 10, 9]  # Recent decline
        )
        # Season avg: ~16.1, Recent 4: ~8.25, Ratio: ~0.51

        multiplier, tier = calculator.calculate(player, current_week=11)

        assert tier == "ICE_COLD"
        assert multiplier < 1.0

    def test_bye_week_exclusion(self, calculator):
        """Test bye week is excluded from window"""
        player = create_player(
            name="Test Player",
            actual_points=[15, 15, 15, 15, 0, 20, 20, 20, 20]  # Week 5 bye
        )

        metrics = calculator._calculate_form_metrics(player, current_week=9)

        assert metrics['games_in_window'] == 4  # Should skip bye week
        assert metrics['recent_avg'] == 20.0  # Last 4 active games
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 4-6%
- Rationale: Identifies breakout players during draft

**Starter Helper Mode:**
- Expected improvement: 5-8%
- Rationale: Recent form is highly predictive for weekly decisions

**Trade Simulator Mode:**
- Expected improvement: 4-6%
- Rationale: Captures buy-low/sell-high opportunities

---

## Real-World Examples

### Example 1: Hot Streak (Breakout Player)

**Puka Nacua (LAR, WR)** - Mid-Season Breakout:

| Metric | Value |
|--------|-------|
| Season Average | 14.2 PPG |
| Last 4 Games | 22, 18, 25, 21 |
| Recent Average | 21.5 PPG |
| Form Ratio | 1.51 |
| Form Trend | HOT |
| Multiplier | 1.04^1.0 = 1.04 |
| Base Score | 140.0 |
| Adjusted Score | 145.6 (+5.6 pts) |

**Reason String:** `"Recent Form (HOT): 21.5 PPG last 4g vs 14.2 season"`

### Example 2: Cold Streak (Slumping Star)

**Slumping WR** - Late Season Decline:

| Metric | Value |
|--------|-------|
| Season Average | 18.5 PPG |
| Last 4 Games | 8, 10, 12, 9 |
| Recent Average | 9.75 PPG |
| Form Ratio | 0.53 |
| Form Trend | ICE_COLD |
| Multiplier | 0.96^1.0 = 0.96 |
| Base Score | 155.0 |
| Adjusted Score | 148.8 (-6.2 pts) |

**Reason String:** `"Recent Form (ICE_COLD): 9.8 PPG last 4g vs 18.5 season"`

---

## Dependencies

### Data Dependencies
- `actual_points` - Available in all `data/player_data/*_data.json` files

### Code Dependencies
- `ConfigManager` - Existing
- `FantasyPlayer` - Existing
- `RecentFormCalculator` - To be created

---

## Related Metrics

**Complementary Metrics:**
- **M17 (Target Share Trend)** - Volume-specific trending for receivers
- **M36 (Volume Spike Indicator)** - Detects sharp volume increases
- **M37 (Boom/Bust Frequency)** - Consistency complement to form

---

## Implementation Checklist

**Pre-Implementation:**
- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed

**Implementation:**
- [ ] RecentFormCalculator module created
- [ ] Scoring integration added
- [ ] Configuration file updated

**Testing:**
- [ ] Unit tests written and passing
- [ ] Validation against real player data

---

**END OF FEATURE REQUEST**
