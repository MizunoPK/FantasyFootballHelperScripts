# Feature Request: Touch Share (Total Opportunity)

**Metric ID:** M19
**Priority:** HIGH
**Positions:** RB, WR
**Effort Estimate:** 3-4 hours
**Expected Impact:** 10-14% improvement in RB/WR opportunity assessment

---

## What This Metric Is

Touch Share measures a player's total offensive involvement by combining rushing attempts and receiving targets as a percentage of the team's total touches. This provides a comprehensive view of a player's opportunity share regardless of how they're utilized (rushing vs receiving).

---

## What We're Trying to Accomplish

**Goals:**
- **Identify true workhorses**: Players with high touch share have guaranteed volume floor
- **Compare mixed-usage players**: RBs who catch passes vs pure rushers on same scale
- **Evaluate offensive role**: Distinguish bell cows (60%+ touches) from committee backs
- **Predict fantasy floor**: High touch share = more consistent weekly production
- **Account for game script flexibility**: Players who maintain touches in all situations

**Example Use Case:**
> An RB with 15 carries + 5 targets (20 touches) on a team with 60 total offensive touches has 33% touch share. Compare this to a WR with 0 carries + 10 targets (10 touches) on the same team with 16.7% touch share. The RB has twice the opportunity share, indicating a higher floor despite different usage patterns.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:** `data/player_data/[position]_data.json`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `rushing.attempts` | float | Yes (17 weeks) | RB/WR/QB JSON | 18.0 |
| `receiving.targets` | float | Yes (17 weeks) | RB/WR/TE JSON | 5.0 |
| `team` | string | No | All player JSON | "SF" |

**Example Data Structure:**
```json
{
  "id": "4241389",
  "name": "Christian McCaffrey",
  "team": "SF",
  "position": "RB",
  "rushing": {
    "attempts": [18.0, 20.0, 15.0, 0.0, 22.0, ...],  // 17 weeks
    "rush_yds": [95.0, 112.0, 78.0, 0.0, 130.0, ...],
    "rush_tds": [1.0, 2.0, 0.0, 0.0, 1.0, ...]
  },
  "receiving": {
    "targets": [6.0, 8.0, 5.0, 0.0, 7.0, ...],
    "receptions": [5.0, 6.0, 4.0, 0.0, 5.0, ...]
  }
}
```

### Data Validation
- Data verified in: `data/player_data/rb_data.json`, `data/player_data/wr_data.json`
- Weekly granularity: Yes (17 weeks per season)
- Historical availability: Current season
- Known limitations: Need to aggregate all team touches from all position files

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_touch_share(player: FantasyPlayer, team_players: List[FantasyPlayer]) -> dict:
    """
    Calculate touch share for a player.

    Args:
        player: FantasyPlayer object with rushing/receiving stats
        team_players: List of all players on the same team

    Returns:
        dict: {
            'touches_per_game': float,
            'touch_share': float,
            'season_touches': int,
            'team_total_touches': int
        }

    Example:
        >>> player = FantasyPlayer(name="Christian McCaffrey", stats={...})
        >>> result = calculate_touch_share(player, team_players)
        >>> result
        {'touches_per_game': 24.5, 'touch_share': 0.38, 'season_touches': 392, 'team_total_touches': 1032}
    """
    # Step 1: Get player touches (carries + targets)
    weekly_carries = player.stats.get('rushing', {}).get('attempts', [0] * 17)
    weekly_targets = player.stats.get('receiving', {}).get('targets', [0] * 17)
    weekly_touches = [c + t for c, t in zip(weekly_carries, weekly_targets)]

    games_played = len([t for t in weekly_touches if t > 0])
    season_touches = sum(weekly_touches)

    # Step 2: Calculate touches per game
    if games_played > 0:
        touches_per_game = season_touches / games_played
    else:
        touches_per_game = 0.0

    # Step 3: Calculate team total touches (all RB carries + all WR/TE/RB targets)
    team_total_touches = 0
    for teammate in team_players:
        # Add rushing attempts (QB, RB, WR)
        if 'rushing' in teammate.stats:
            team_total_touches += sum(teammate.stats['rushing'].get('attempts', []))
        # Add receiving targets (WR, TE, RB)
        if 'receiving' in teammate.stats:
            team_total_touches += sum(teammate.stats['receiving'].get('targets', []))

    # Step 4: Calculate touch share
    if team_total_touches > 0:
        touch_share = season_touches / team_total_touches
    else:
        touch_share = 0.0

    return {
        'touches_per_game': round(touches_per_game, 1),
        'touch_share': round(touch_share, 3),
        'season_touches': int(season_touches),
        'team_total_touches': int(team_total_touches)
    }
```

### Thresholds & Tiers

**RB Touch Share:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | >=30% | True bell cow | 1.05 | Derrick Henry, CMC |
| GOOD | 22-29% | Lead back | 1.025 | Bijan Robinson |
| AVERAGE | 15-21% | Committee lead | 1.0 | Most starting RBs |
| POOR | <15% | Committee/backup | 0.975 | Backup RBs |

**WR Touch Share:**

| Tier | Threshold | Description | Multiplier | Example Player |
|------|-----------|-------------|------------|----------------|
| EXCELLENT | >=18% | Alpha + rush work | 1.05 | Deebo Samuel |
| GOOD | 12-17% | Target hog | 1.025 | Tyreek Hill |
| AVERAGE | 8-11% | WR1/WR2 | 1.0 | Most starters |
| POOR | <8% | Limited role | 0.975 | WR3/depth |

### Edge Cases

**1. Bye Week Handling**
- **Scenario:** Player has 0 touches in bye week
- **Handling:** Exclude from games_played count
- **Example:** Player with [20, 0, 18, 22] touches has 3 games played, 60 season touches, 20.0 touches/game

**2. Injury/DNP**
- **Scenario:** Player didn't play but is not on bye
- **Handling:** If all rushing + receiving stats are 0.0 for that week, exclude from games_played

**3. Position Flexibility (Deebo Samuel type)**
- **Scenario:** WR with significant rushing work
- **Handling:** Include both rushing attempts and receiving targets in touch calculation
- **Example:** Deebo with 10 targets + 8 carries = 18 touches

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1.5 hours)

**1.1 Verify Data Availability**
- [x] Confirm `rushing.attempts` exists in RB/WR JSON files
- [x] Confirm `receiving.targets` exists in RB/WR/TE JSON files
- [x] Test data extraction with sample players
- [x] Validate data ranges (typical 10-30 touches/game for bell cows)

**1.2 Create Calculation Module**

**File:** `league_helper/util/TouchShareCalculator.py`

```python
from typing import Tuple, Dict, List
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class TouchShareCalculator:
    """Calculate total touch share for RB/WR players"""

    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = get_logger()

    def calculate(self, player: FantasyPlayer, team_players: List[FantasyPlayer]) -> Tuple[float, str]:
        """
        Calculate touch share and return multiplier.

        Args:
            player: Player to calculate for
            team_players: All players on same team

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position not in ['RB', 'WR']:
            return 1.0, "N/A"

        # Calculate touch metrics
        metrics = self._calculate_touch_metrics(player, team_players)

        # Get tier based on position
        tier = self._get_tier(metrics['touch_share'], player.position)

        # Get multiplier from config
        multiplier = self.config.get_touch_share_multiplier(tier, player.position)

        return multiplier, tier

    def _calculate_touch_metrics(self, player: FantasyPlayer, team_players: List[FantasyPlayer]) -> Dict:
        """Calculate touch share metrics"""
        # Implementation from formula above
        pass

    def _get_tier(self, touch_share: float, position: str) -> str:
        """Determine tier based on touch share"""
        thresholds = {
            'RB': {'EXCELLENT': 0.30, 'GOOD': 0.22, 'AVERAGE': 0.15},
            'WR': {'EXCELLENT': 0.18, 'GOOD': 0.12, 'AVERAGE': 0.08}
        }

        pos_thresholds = thresholds.get(position, thresholds['RB'])

        if touch_share >= pos_thresholds['EXCELLENT']:
            return "EXCELLENT"
        elif touch_share >= pos_thresholds['GOOD']:
            return "GOOD"
        elif touch_share >= pos_thresholds['AVERAGE']:
            return "AVERAGE"
        else:
            return "POOR"
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**2.1 Add to league_config.json**

```json
{
  "TOUCH_SHARE_SCORING": {
    "ENABLED": true,
    "POSITION_SPECIFIC": {
      "RB": {
        "THRESHOLDS": {
          "EXCELLENT": 0.30,
          "GOOD": 0.22,
          "AVERAGE": 0.15
        },
        "MULTIPLIERS": {
          "EXCELLENT": 1.05,
          "GOOD": 1.025,
          "AVERAGE": 1.0,
          "POOR": 0.975
        },
        "WEIGHT": 2.0
      },
      "WR": {
        "THRESHOLDS": {
          "EXCELLENT": 0.18,
          "GOOD": 0.12,
          "AVERAGE": 0.08
        },
        "MULTIPLIERS": {
          "EXCELLENT": 1.05,
          "GOOD": 1.025,
          "AVERAGE": 1.0,
          "POOR": 0.975
        },
        "WEIGHT": 1.5
      }
    },
    "MIN_WEEKS": 3,
    "DESCRIPTION": "Total touch share - combines carries and targets for opportunity assessment"
  }
}
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**3.1 Add Scoring Step**

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_touch_share_scoring()`

```python
def _apply_touch_share_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply touch share adjustment to player score.

    Args:
        p: FantasyPlayer object
        player_score: Current player score

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    if p.position not in ['RB', 'WR']:
        return player_score, ""

    if not self.config.touch_share_scoring.get('ENABLED', False):
        return player_score, ""

    team_players = self.player_manager.get_players_by_team(p.team)

    calculator = TouchShareCalculator(self.config)
    multiplier, tier = calculator.calculate(p, team_players)

    adjusted_score = player_score * multiplier

    metrics = calculator._calculate_touch_metrics(p, team_players)
    reason = f"Touch Share ({tier}): {metrics['touch_share']*100:.1f}% ({metrics['touches_per_game']:.1f} tch/g)"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**4.1 Unit Tests**

**File:** `tests/league_helper/util/test_TouchShareCalculator.py`

```python
import pytest
from league_helper.util.TouchShareCalculator import TouchShareCalculator

class TestTouchShareCalculator:
    """Test touch share calculation"""

    def test_rb_bell_cow_excellent_tier(self, calculator, mock_team_players):
        """Test RB with 30%+ touch share"""
        player = create_player(
            name="Derrick Henry",
            position="RB",
            rushing_attempts=[22, 25, 20, 0, 24, 23, 21, 20, 25, 22, 24, 20, 23, 21, 22, 24, 20],
            targets=[2, 3, 1, 0, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2]
        )

        multiplier, tier = calculator.calculate(player, mock_team_players)

        assert tier == "EXCELLENT"
        assert multiplier > 1.0

    def test_wr_with_rush_work(self, calculator, mock_team_players):
        """Test WR with rushing attempts (Deebo Samuel type)"""
        player = create_player(
            name="Deebo Samuel",
            position="WR",
            rushing_attempts=[5, 7, 4, 0, 6, 5, 8, 4, 6, 5, 7, 4, 5, 6, 5, 7, 4],
            targets=[8, 7, 9, 0, 8, 7, 6, 9, 8, 7, 8, 9, 7, 8, 7, 8, 9]
        )

        multiplier, tier = calculator.calculate(player, mock_team_players)

        assert tier == "EXCELLENT"  # High combined touch share
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 8-10%
- Rationale: Identifies bell cows and high-volume players early

**Starter Helper Mode:**
- Expected improvement: 10-14%
- Rationale: Touch share predicts weekly floor better than individual carry/target metrics

**Trade Simulator Mode:**
- Expected improvement: 8-12%
- Rationale: Reveals true opportunity share for RB/WR value assessment

---

## Real-World Examples

### Example 1: True Bell Cow RB

**Derrick Henry (TEN, RB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Season Carries | 345 |
| Season Targets | 32 |
| Season Touches | 377 |
| Games Played | 16 |
| Touches/Game | 23.6 |
| Team Total Touches | 980 |
| Touch Share | 38.5% |
| Tier | EXCELLENT |
| Multiplier | 1.05^2.0 = 1.1025 |

**Reason String:** `"Touch Share (EXCELLENT): 38.5% (23.6 tch/g)"`

### Example 2: Versatile WR (Deebo Type)

**Deebo Samuel (SF, WR)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Season Carries | 45 |
| Season Targets | 85 |
| Season Touches | 130 |
| Games Played | 15 |
| Touches/Game | 8.7 |
| Team Total Touches | 720 |
| Touch Share | 18.1% |
| Tier | EXCELLENT (for WR) |
| Multiplier | 1.05^1.5 = 1.0759 |

**Reason String:** `"Touch Share (EXCELLENT): 18.1% (8.7 tch/g)"`

---

## Dependencies

### Data Dependencies
- `rushing.attempts` - Available in `data/player_data/[rb|wr]_data.json`
- `receiving.targets` - Available in `data/player_data/[rb|wr|te]_data.json`
- `team` - Available in all player JSON files

### Code Dependencies
- `ConfigManager` - Existing
- `PlayerManager` - Existing (needs `get_players_by_team()`)
- `FantasyPlayer` - Existing
- `TouchShareCalculator` - To be created

---

## Risks & Mitigations

### Risk 1: Team Aggregation Performance
**Likelihood:** Medium | **Impact:** Medium

**Description:** Summing all team touches for every player evaluation

**Mitigation:** Cache team touch totals per calculation run

### Risk 2: Position Handling Complexity
**Likelihood:** Low | **Impact:** Low

**Description:** Some WRs have rushing work, some RBs have no targets

**Mitigation:** Include all available stats; position-specific thresholds handle different roles

---

## Open Questions

**Questions for User:**
1. Should touch share weight rushing attempts and targets equally, or weight targets higher for PPR?
2. Include QB rushing attempts in team total touches calculation?

---

## Related Metrics

**Complementary Metrics:**
- **M01 (Target Volume)** - Receiving-specific component of touch share
- **M04 (Carries Per Game)** - Rushing-specific component of touch share
- **M11 (RB Receiving Workload)** - Detailed RB receiving analysis

---

## Implementation Checklist

**Pre-Implementation:**
- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed
- [ ] User questions answered

**Implementation:**
- [ ] TouchShareCalculator module created
- [ ] Scoring integration added
- [ ] Configuration file updated

**Testing:**
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Validation against real player data

**Documentation:**
- [ ] Scoring step documentation created
- [ ] README updated

---

**END OF FEATURE REQUEST**
