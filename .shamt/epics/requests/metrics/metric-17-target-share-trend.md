# Feature Request: Target Share Trend

**Metric ID:** M17
**Priority:** MEDIUM
**Positions:** WR, TE, RB
**Effort Estimate:** 2-3 hours
**Expected Impact:** 5-8% improvement in identifying emerging/fading players

---

## What This Metric Is

Target Share Trend tracks changes in a player's percentage of team targets over recent weeks, comparing the last 3 weeks to the previous 3 weeks to identify whether a player's role is expanding, stable, or shrinking within their offense.

---

## What We're Trying to Accomplish

**Goals:**
- **Detect breakout players early**: Rising target share (15% → 25%) indicates expanding role before it shows in fantasy points
- **Identify fading veterans**: Declining share (30% → 20%) signals reduced role, potential bench/sell candidate
- **Quantify role changes**: Injury to teammate, scheme changes, or coaching decisions show up in share trends before box scores
- **Improve draft strategy**: Target players with rising trends in late-season weeks (momentum into next year)
- **Buy-low/sell-high opportunities**: Trade for players with rising trends, trade away players with declining trends

**Example Use Case:**
> A WR going from 18% target share (weeks 5-7) to 28% target share (weeks 8-10) is showing a +55% role expansion. This player is likely breaking out as the WR1, making them a league-winner pickup even if TD production hasn't caught up yet. Conversely, a WR declining from 25% to 18% share is losing targets to a teammate and is a sell-high candidate.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE (Derived from M01 Target Volume)

**Data Location:** Calculated from `data/player_data/[position]_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `receiving.targets` | float | Yes (17 weeks) | WR/TE/RB JSON | 8.0 |
| `team` | string | No | All player JSON | "KC" |

**Example Data Structure:**
Same as M01 - uses existing target data to calculate rolling trends.

### Data Validation
- ✅ Data verified in: `data/player_data/wr_data.json`, `data/player_data/te_data.json`, `data/player_data/rb_data.json`
- ✅ Weekly granularity: Yes (17 weeks per season)
- ✅ Historical availability: Same as M01 Target Volume
- ⚠️ Known limitations: Requires minimum 6 weeks of data to calculate trend

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_target_share_trend(player: FantasyPlayer, team_players: List[FantasyPlayer], current_week: int) -> dict:
    """
    Calculate target share trend over recent weeks.

    Args:
        player: FantasyPlayer object with receiving stats
        team_players: List of all players on the same team
        current_week: Current NFL week (1-17)

    Returns:
        dict: {
            'trend_pct_change': float,  # Percentage change in target share
            'recent_share': float,       # Last 3 weeks average share
            'earlier_share': float,      # Weeks N-3 to N-5 average share
            'direction': str             # 'RISING', 'STABLE', 'DECLINING'
        }

    Example:
        >>> player = FantasyPlayer(name="Puka Nacua", stats={...})
        >>> result = calculate_target_share_trend(player, team_players, week=10)
        >>> result
        {'trend_pct_change': 25.0, 'recent_share': 0.25, 'earlier_share': 0.20, 'direction': 'RISING'}
    """
    # Step 1: Require minimum 6 weeks of data
    if current_week < 7:
        return {
            'trend_pct_change': 0.0,
            'recent_share': 0.0,
            'earlier_share': 0.0,
            'direction': 'INSUFFICIENT_DATA'
        }

    # Step 2: Calculate team target totals for each week
    weekly_team_targets = {}
    for week in range(1, current_week + 1):
        team_total = sum(
            p.stats['receiving']['targets'][week - 1]
            for p in team_players
            if p.position in ['WR', 'TE', 'RB']
        )
        weekly_team_targets[week] = team_total

    # Step 3: Calculate player's weekly target share
    player_weekly_shares = []
    for week in range(1, current_week + 1):
        player_targets = player.stats['receiving']['targets'][week - 1]
        team_targets = weekly_team_targets[week]

        if team_targets > 0:
            share = player_targets / team_targets
        else:
            share = 0.0

        player_weekly_shares.append(share)

    # Step 4: Calculate recent 3-week average (weeks N, N-1, N-2)
    recent_weeks = player_weekly_shares[-3:]
    recent_share = sum(recent_weeks) / len(recent_weeks)

    # Step 5: Calculate earlier 3-week average (weeks N-3, N-4, N-5)
    earlier_weeks = player_weekly_shares[-6:-3]
    earlier_share = sum(earlier_weeks) / len(earlier_weeks)

    # Step 6: Calculate percentage change
    if earlier_share > 0:
        trend_pct_change = ((recent_share - earlier_share) / earlier_share) * 100
    elif recent_share > 0:
        trend_pct_change = 100.0  # Went from 0 to something = +100%
    else:
        trend_pct_change = 0.0  # Both 0 = neutral

    # Step 7: Determine direction
    if trend_pct_change >= 15.0:
        direction = 'RISING'
    elif trend_pct_change <= -15.0:
        direction = 'DECLINING'
    else:
        direction = 'STABLE'

    return {
        'trend_pct_change': round(trend_pct_change, 1),
        'recent_share': round(recent_share, 3),
        'earlier_share': round(earlier_share, 3),
        'direction': direction
    }
```

### Thresholds & Tiers

**WR/TE/RB Target Share Trend:**

| Tier | Threshold | Description | Multiplier | Example Scenario |
|------|-----------|-------------|------------|------------------|
| EXCELLENT | +15% or more | Strong rising trend | 1.05 | 20% → 25% share (+25% trend) |
| GOOD | 0% to +15% | Slight rising trend | 1.025 | 22% → 24% share (+9% trend) |
| AVERAGE | -15% to 0% | Slight declining trend | 0.975 | 25% → 23% share (-8% trend) |
| POOR | < -15% | Strong declining trend | 0.95 | 28% → 22% share (-21% trend) |

### Edge Cases

**1. Early Season (Weeks 1-6)**
- **Scenario:** Not enough weeks to calculate 6-week trend
- **Handling:** Return 0.0% trend, tier = "INSUFFICIENT_DATA", multiplier = 1.0
- **Example:** Week 5 player should not have trend applied yet

**2. Bye Week in Trend Window**
- **Scenario:** Player has bye week in recent or earlier 3-week window
- **Handling:** Exclude bye week (0 targets) from share calculation, use available weeks
- **Example:** Weeks [0.20, 0, 0.25] → use [0.20, 0.25] for 2-week average

**3. Injury/DNP**
- **Scenario:** Player injured for 1-2 weeks in trend window
- **Handling:** Exclude injured weeks, calculate with remaining weeks (minimum 2 weeks per window)
- **Example:** If only 2 valid weeks in recent window, still calculate trend

**4. Extreme Volatility**
- **Scenario:** Target share swings wildly week-to-week (0.10, 0.30, 0.08)
- **Handling:** Use 3-week average to smooth volatility
- **Example:** Volatile shares still produce meaningful trend if directional

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1 hour)

**1.1 Verify Data Availability**
- [x] Confirm M01 (Target Volume) is implemented
- [x] Verify weekly target data available for rolling calculations
- [ ] Test trend calculation with sample players

**1.2 Create Calculation Module**

**File:** `league_helper/util/TargetShareTrendCalculator.py`

```python
from typing import Tuple, Dict, List
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class TargetShareTrendCalculator:
    """Calculate target share trends over rolling windows"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()
        self.min_weeks = config_manager.target_share_trend_scoring.get('MIN_WEEKS', 7)

    def calculate(self, player: FantasyPlayer, team_players: List[FantasyPlayer], current_week: int) -> Tuple[float, str]:
        """
        Calculate target share trend and return multiplier.

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position not in ['WR', 'TE', 'RB']:
            return 1.0, "N/A"

        if current_week < self.min_weeks:
            return 1.0, "INSUFFICIENT_DATA"

        # Calculate trend
        trend = self._calculate_trend(player, team_players, current_week)

        # Get tier
        tier = self._get_tier(trend['trend_pct_change'])

        # Get multiplier
        multiplier = self.config.get_target_share_trend_multiplier(tier)

        return multiplier, tier
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "TARGET_SHARE_TREND_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT": 15.0,
      "GOOD": 0.0,
      "POOR": -15.0
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.05,
      "GOOD": 1.025,
      "AVERAGE": 0.975,
      "POOR": 0.95
    },
    "WEIGHT": 1.7,
    "MIN_WEEKS": 7,
    "TREND_WINDOW_SIZE": 3,
    "DESCRIPTION": "Target share trend - identifies emerging/fading roles"
  }
}
```

**2.2 Configuration Parameters**

| Parameter | Default | Description | Typical Range |
|-----------|---------|-------------|---------------|
| `WEIGHT` | 1.7 | Multiplier exponent | 1.0 - 2.5 |
| `MIN_WEEKS` | 7 | Minimum weeks for trend | 6 - 10 |
| `TREND_WINDOW_SIZE` | 3 | Weeks per trend window | 2 - 4 |

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**3.1 Add Scoring Step**

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_target_share_trend_scoring()` (insert after Step 14 Target Volume)

```python
def _apply_target_share_trend_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply target share trend adjustment to player score.

    Args:
        p: FantasyPlayer object
        player_score: Current player score

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    # Skip if not applicable
    if p.position not in ['WR', 'TE', 'RB']:
        return player_score, ""

    # Skip if disabled
    if not self.config.target_share_trend_scoring.get('ENABLED', False):
        return player_score, ""

    # Skip if too early in season
    if self.config.current_nfl_week < 7:
        return player_score, ""

    # Get team players
    team_players = self.player_manager.get_players_by_team(p.team)

    # Calculate trend
    calculator = TargetShareTrendCalculator(self.config)
    multiplier, tier = calculator.calculate(p, team_players, self.config.current_nfl_week)

    # Apply multiplier
    adjusted_score = player_score * multiplier

    # Build reason string
    trend_data = calculator._calculate_trend(p, team_players, self.config.current_nfl_week)
    reason = f"Target Trend ({tier}): {trend_data['trend_pct_change']:+.1f}%"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**4.1 Unit Tests**

**File:** `tests/league_helper/util/test_TargetShareTrendCalculator.py`

```python
class TestTargetShareTrendCalculator:
    """Test target share trend calculation"""

    def test_rising_trend(self, calculator):
        """Test player with rising target share"""
        player = FantasyPlayer(
            position="WR",
            stats={
                'receiving': {
                    'targets': [8, 7, 9, 8, 9, 10, 11, 12, 13, 12]  # Clear rising trend
                }
            }
        )

        team_players = self._create_mock_team_with_stable_targets(500)

        multiplier, tier = calculator.calculate(player, team_players, current_week=10)

        assert tier == "EXCELLENT"
        assert multiplier > 1.0

    def test_declining_trend(self, calculator):
        """Test player with declining target share"""
        player = FantasyPlayer(
            position="WR",
            stats={
                'receiving': {
                    'targets': [12, 13, 12, 11, 10, 9, 8, 7, 6, 7]  # Clear declining trend
                }
            }
        )

        multiplier, tier = calculator.calculate(player, team_players, current_week=10)

        assert tier == "POOR"
        assert multiplier < 1.0
```

**4.2 Validation Test Cases**

```python
validation_cases = [
    {
        'player_name': 'Emerging WR',
        'position': 'WR',
        'target_share_progression': [0.15, 0.16, 0.17, 0.18, 0.20, 0.22, 0.24, 0.26],
        'expected_trend': 25.0,  # Rising from ~18% to ~24%
        'expected_tier': 'EXCELLENT',
        'rationale': 'Clear breakout pattern, expanding role'
    }
]
```

---

### Phase 5: Documentation (Estimated: 30 min)

**5.1 Create Scoring Documentation**

**File:** `docs/scoring/15_target_share_trend_scoring.md`

Include:
- Trend calculation methodology
- 3-week rolling window explanation
- Real examples of rising/declining trends
- When to trust trends vs statistical noise

**5.2 Update Checklist**

Mark M17 as implemented in `docs/research/metrics_implementation_checklist.md`.

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 3-5%
- Rationale: Late-season trends help identify breakout players for next season

**Starter Helper Mode:**
- Expected improvement: 5-8%
- Rationale: Rising trends indicate players to start confidently, declining trends suggest bench/trade

**Trade Simulator Mode:**
- Expected improvement: 8-12%
- Rationale: Trend analysis is critical for buy-low/sell-high decisions

### Accuracy Metrics

**Target Improvements:**
- Overall prediction accuracy: +5-8%
- Identify breakout players: 2-3 weeks earlier
- Reduce over-valuation of declining players: 10-15%

---

## Real-World Examples

### Example 1: Rising Trend (Breakout WR)

**Puka Nacua (LAR, WR)** - 2023 Season Weeks 5-10:

| Metric | Value |
|--------|-------|
| Earlier Share (Wks 5-7) | 18.2% |
| Recent Share (Wks 8-10) | 26.5% |
| Trend % Change | +45.6% |
| Tier | EXCELLENT |
| Multiplier | 1.05^1.7 = 1.0868 |
| Base Score | 140.0 |
| Adjusted Score | 152.2 (+12.2 pts) |

**Reason String:** `"Target Trend (EXCELLENT): +45.6%"`

### Example 2: Declining Trend (Fading Veteran)

**Aging WR (Team, WR)** - Mid-Season Decline:

| Metric | Value |
|--------|-------|
| Earlier Share (Wks 8-10) | 24.8% |
| Recent Share (Wks 11-13) | 18.3% |
| Trend % Change | -26.2% |
| Tier | POOR |
| Multiplier | 0.95^1.7 = 0.9163 |
| Base Score | 125.0 |
| Adjusted Score | 114.5 (-10.5 pts) |

**Reason String:** `"Target Trend (POOR): -26.2%"`

---

## Dependencies

### Data Dependencies
- ✅ M01 (Target Volume) - Must be implemented first
- ✅ `receiving.targets` - Available in player JSON files
- ✅ Weekly granularity - Required for trend calculation

### Code Dependencies
- ✅ `TargetVolumeCalculator` - For team aggregation logic
- ✅ `PlayerManager.get_players_by_team()` - For team context
- 🆕 `TargetShareTrendCalculator` - To be created

---

## Risks & Mitigations

### Risk 1: Noise vs Signal

**Likelihood:** High
**Impact:** Medium

**Description:** Short 3-week windows may capture noise rather than true role changes

**Mitigation:**
- Use 3-week windows (not 2-week) for smoother trends
- Set threshold at ±15% to filter small fluctuations
- Weight trend lower (1.7) than static volume (2.0)

### Risk 2: Mid-Season Injury Impact

**Likelihood:** Medium
**Impact:** Medium

**Description:** Teammate injury inflates target share temporarily

**Mitigation:**
- Track injury reports to contextualize trend changes
- Consider rolling 4-week average instead of 3-week for more stability
- Flag "caution" when trend is injury-driven

---

## Related Metrics

**Complementary Metrics:**
- **M01 (Target Volume)** - Foundation metric, trend builds on this
- **M58 (Total Opportunity Share)** - Similar trend logic applies to carries + targets

**Prerequisites:**
- **M01 (Target Volume)** - MUST be implemented first

---

## Implementation Checklist

**Pre-Implementation:**
- [x] Data availability verified (uses M01 data)
- [x] Formula validated with sample calculations
- [x] Configuration structure designed
- [ ] M01 (Target Volume) fully implemented

**Implementation:**
- [ ] TargetShareTrendCalculator module created
- [ ] Scoring integration added
- [ ] ConfigManager methods added
- [ ] Configuration file updated

**Testing:**
- [ ] Unit tests written and passing
- [ ] Trend calculation validated with real data
- [ ] Edge cases tested (bye weeks, injuries)

**Documentation:**
- [ ] Scoring step documentation created
- [ ] Checklist updated
- [ ] Real-world examples documented

**Completion:**
- [ ] All tests passing
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add target share trend scoring (Step 15)"

---

**END OF FEATURE REQUEST**
