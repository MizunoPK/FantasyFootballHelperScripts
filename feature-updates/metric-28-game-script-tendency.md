# Feature Request: Game Script Tendency (Trailing Team Boost)

**Metric ID:** M28
**Priority:** HIGH
**Positions:** WR, TE, RB
**Effort Estimate:** 4-5 hours
**Expected Impact:** 8-12% improvement in weekly lineup decisions based on expected game flow

---

## What This Metric Is

Game Script Tendency measures how often a team plays from behind and the typical point differential, which directly impacts player usage patterns. Teams trailing tend to pass more (boosting WR/TE) while teams leading tend to run more (boosting RB). This metric adjusts player value based on their team's historical tendency to be in positive or negative game scripts.

---

## What We're Trying to Accomplish

**Goals:**
- **Predict pass-heavy game scripts**: Teams that frequently trail tend to abandon the run
- **Identify garbage time beneficiaries**: WR/TE on bad teams get volume when trailing
- **Penalize volume-dependent RBs on bad teams**: Negative game script = fewer carries
- **Adjust for team quality context**: Good teams maintain balanced scripts; bad teams go pass-heavy late
- **Support weekly projections**: Factor expected game script into lineup decisions

**Example Use Case:**
> A WR on a team that's been outscored by an average of 7 points in the 4th quarter will get more targets as the team passes to catch up. Meanwhile, an RB on a dominant team (average +10 point lead) gets more carries in positive game scripts to run out the clock.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:** `data/game_data.csv`

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `week` | int | Yes (rows per week) | game_data.csv | 15 |
| `home_team` | string | Yes | game_data.csv | "KC" |
| `away_team` | string | Yes | game_data.csv | "BUF" |
| `home_team_score` | int | Yes | game_data.csv | 27 |
| `away_team_score` | int | Yes | game_data.csv | 24 |

**Example Data Structure:**
```csv
week,home_team,away_team,home_team_score,away_team_score,temperature,gust,precipitation,indoor,neutral_site,location
15,KC,BUF,27,24,35,12,0,0,0,Kansas City
15,SF,SEA,31,17,52,5,0,0,0,San Francisco
15,NYJ,MIA,14,31,42,8,0,0,0,New York
```

### Data Validation
- Data verified in: `data/game_data.csv`
- Weekly granularity: Yes (one row per game per week)
- Historical availability: Current season
- Known limitations: Only final scores, not quarter-by-quarter (using final score as proxy)

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_game_script_tendency(player: FantasyPlayer, game_data: List[Dict]) -> dict:
    """
    Calculate game script tendency for a player's team.

    Args:
        player: FantasyPlayer object with team info
        game_data: List of game records from game_data.csv

    Returns:
        dict: {
            'avg_point_differential': float,  # Positive = winning, Negative = losing
            'games_trailing': int,            # Games where team lost
            'games_leading': int,             # Games where team won
            'trailing_percentage': float,     # % of games team trailed/lost
            'script_tendency': str            # PASS_HEAVY, BALANCED, RUN_HEAVY
        }

    Example:
        >>> player = FantasyPlayer(name="Garrett Wilson", team="NYJ", ...)
        >>> result = calculate_game_script_tendency(player, game_data)
        >>> result
        {'avg_point_differential': -7.2, 'games_trailing': 11, 'games_leading': 4,
         'trailing_percentage': 0.73, 'script_tendency': 'PASS_HEAVY'}
    """
    team = player.team
    games = []

    # Step 1: Get all games for this team
    for game in game_data:
        if game['home_team'] == team:
            point_diff = game['home_team_score'] - game['away_team_score']
            games.append({'week': game['week'], 'point_diff': point_diff})
        elif game['away_team'] == team:
            point_diff = game['away_team_score'] - game['home_team_score']
            games.append({'week': game['week'], 'point_diff': point_diff})

    if not games:
        return {
            'avg_point_differential': 0.0,
            'games_trailing': 0,
            'games_leading': 0,
            'trailing_percentage': 0.5,
            'script_tendency': 'BALANCED'
        }

    # Step 2: Calculate statistics
    total_diff = sum(g['point_diff'] for g in games)
    avg_point_differential = total_diff / len(games)

    games_trailing = len([g for g in games if g['point_diff'] < 0])
    games_leading = len([g for g in games if g['point_diff'] > 0])

    trailing_percentage = games_trailing / len(games)

    # Step 3: Determine script tendency
    if avg_point_differential <= -5.0 or trailing_percentage >= 0.60:
        script_tendency = 'PASS_HEAVY'
    elif avg_point_differential >= 5.0 or trailing_percentage <= 0.35:
        script_tendency = 'RUN_HEAVY'
    else:
        script_tendency = 'BALANCED'

    return {
        'avg_point_differential': round(avg_point_differential, 1),
        'games_trailing': games_trailing,
        'games_leading': games_leading,
        'trailing_percentage': round(trailing_percentage, 3),
        'script_tendency': script_tendency
    }
```

### Thresholds & Tiers

**WR/TE Adjustment (Benefit from trailing):**

| Script Tendency | Avg Point Diff | Trailing % | Multiplier | Description |
|-----------------|----------------|------------|------------|-------------|
| PASS_HEAVY | <= -5.0 | >= 60% | 1.04 | Garbage time volume boost |
| BALANCED | -4.9 to +4.9 | 35-59% | 1.0 | Neutral script |
| RUN_HEAVY | >= +5.0 | <= 35% | 0.98 | Less passing volume |

**RB Adjustment (Benefit from leading):**

| Script Tendency | Avg Point Diff | Trailing % | Multiplier | Description |
|-----------------|----------------|------------|------------|-------------|
| RUN_HEAVY | >= +5.0 | <= 35% | 1.04 | Clock-killing carries boost |
| BALANCED | -4.9 to +4.9 | 35-59% | 1.0 | Neutral script |
| PASS_HEAVY | <= -5.0 | >= 60% | 0.98 | Abandoned run game |

### Edge Cases

**1. Early Season (Weeks 1-3)**
- **Scenario:** Limited game data makes script tendency unreliable
- **Handling:** Use prior season data or reduce weight to 0.5 for weeks 1-3
- **Example:** Week 2 with only 1 game → blend with previous season tendency

**2. Blowout Games**
- **Scenario:** 40-point loss skews average dramatically
- **Handling:** Cap individual game point differential at +/- 21 points
- **Example:** 45-3 loss counts as -21, not -42

**3. Pass-Catching RBs**
- **Scenario:** Some RBs benefit from negative game script (CMC, Kamara)
- **Handling:** Position-specific sub-weights for receiving RBs
- **Example:** RB with 6+ targets/game uses WR formula instead of RB formula

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1.5 hours)

**1.1 Create Data Loader**

**File:** `league_helper/util/GameDataLoader.py` (if not existing)

```python
import csv
from typing import List, Dict

def load_game_data(filepath: str = 'data/game_data.csv') -> List[Dict]:
    """
    Load game data from CSV.

    Returns:
        List of game records with scores and team info
    """
    games = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            games.append({
                'week': int(row['week']),
                'home_team': row['home_team'],
                'away_team': row['away_team'],
                'home_team_score': int(row['home_team_score']),
                'away_team_score': int(row['away_team_score'])
            })
    return games
```

**1.2 Create Calculation Module**

**File:** `league_helper/util/GameScriptCalculator.py`

```python
from typing import Tuple, Dict, List
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class GameScriptCalculator:
    """Calculate game script tendency and apply position-specific adjustments"""

    def __init__(self, config_manager, game_data: List[Dict]):
        self.config = config_manager
        self.game_data = game_data
        self.logger = get_logger()
        self._team_cache = {}

    def calculate(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate game script adjustment for player.

        Args:
            player: Player to calculate for

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position not in ['WR', 'TE', 'RB']:
            return 1.0, "N/A"

        # Get or calculate team tendency
        if player.team not in self._team_cache:
            self._team_cache[player.team] = self._calculate_team_tendency(player.team)

        tendency = self._team_cache[player.team]

        # Apply position-specific adjustment
        multiplier = self._get_position_multiplier(player.position, tendency)
        tier = tendency['script_tendency']

        return multiplier, tier

    def _calculate_team_tendency(self, team: str) -> Dict:
        """Calculate game script tendency for team"""
        # Implementation from formula above
        pass

    def _get_position_multiplier(self, position: str, tendency: Dict) -> float:
        """Get multiplier based on position and script tendency"""
        script = tendency['script_tendency']

        if position in ['WR', 'TE']:
            # WR/TE benefit from trailing (more passing)
            multipliers = {'PASS_HEAVY': 1.04, 'BALANCED': 1.0, 'RUN_HEAVY': 0.98}
        else:  # RB
            # RB benefit from leading (more rushing)
            multipliers = {'RUN_HEAVY': 1.04, 'BALANCED': 1.0, 'PASS_HEAVY': 0.98}

        base_mult = multipliers.get(script, 1.0)
        weight = self.config.game_script_scoring.get('WEIGHT', 1.5)

        return base_mult ** weight
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**2.1 Add to league_config.json**

```json
{
  "GAME_SCRIPT_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "PASS_HEAVY_POINT_DIFF": -5.0,
      "RUN_HEAVY_POINT_DIFF": 5.0,
      "PASS_HEAVY_TRAILING_PCT": 0.60,
      "RUN_HEAVY_TRAILING_PCT": 0.35,
      "POINT_DIFF_CAP": 21
    },
    "MULTIPLIERS": {
      "WR_TE": {
        "PASS_HEAVY": 1.04,
        "BALANCED": 1.0,
        "RUN_HEAVY": 0.98
      },
      "RB": {
        "RUN_HEAVY": 1.04,
        "BALANCED": 1.0,
        "PASS_HEAVY": 0.98
      }
    },
    "WEIGHT": 1.5,
    "MIN_GAMES": 3,
    "DESCRIPTION": "Game script tendency - adjusts for team's typical game flow patterns"
  }
}
```

---

### Phase 3: Scoring Integration (Estimated: 1.5 hours)

**3.1 Add Scoring Step**

**File:** `league_helper/util/player_scoring.py`

```python
def _apply_game_script_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply game script tendency adjustment to player score.

    Args:
        p: FantasyPlayer object
        player_score: Current player score

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    if p.position not in ['WR', 'TE', 'RB']:
        return player_score, ""

    if not self.config.game_script_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = GameScriptCalculator(self.config, self.game_data)
    multiplier, tier = calculator.calculate(p)

    adjusted_score = player_score * multiplier

    tendency = calculator._team_cache.get(p.team, {})
    avg_diff = tendency.get('avg_point_differential', 0)
    trailing_pct = tendency.get('trailing_percentage', 0.5) * 100

    reason = f"Game Script ({tier}): Avg {avg_diff:+.1f} pts, {trailing_pct:.0f}% trailing"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1.5 hours)

**4.1 Unit Tests**

**File:** `tests/league_helper/util/test_GameScriptCalculator.py`

```python
import pytest
from league_helper.util.GameScriptCalculator import GameScriptCalculator

class TestGameScriptCalculator:
    """Test game script calculation"""

    def test_pass_heavy_team_wr_boost(self, calculator):
        """Test WR on trailing team gets boost"""
        player = create_player(name="Garrett Wilson", position="WR", team="NYJ")

        # NYJ loses most games by 7+ points
        mock_games = [
            {'week': w, 'home_team': 'NYJ', 'away_team': 'OPP',
             'home_team_score': 14, 'away_team_score': 24}
            for w in range(1, 12)
        ]

        calc = GameScriptCalculator(mock_config, mock_games)
        multiplier, tier = calc.calculate(player)

        assert tier == "PASS_HEAVY"
        assert multiplier > 1.0  # WR should get boost

    def test_pass_heavy_team_rb_penalty(self, calculator):
        """Test RB on trailing team gets penalty"""
        player = create_player(name="Breece Hall", position="RB", team="NYJ")

        # Same bad team
        mock_games = [
            {'week': w, 'home_team': 'NYJ', 'away_team': 'OPP',
             'home_team_score': 14, 'away_team_score': 24}
            for w in range(1, 12)
        ]

        calc = GameScriptCalculator(mock_config, mock_games)
        multiplier, tier = calc.calculate(player)

        assert tier == "PASS_HEAVY"
        assert multiplier < 1.0  # RB should get penalty

    def test_run_heavy_team_rb_boost(self, calculator):
        """Test RB on winning team gets boost"""
        player = create_player(name="Derrick Henry", position="RB", team="BAL")

        # BAL wins most games by 10+ points
        mock_games = [
            {'week': w, 'home_team': 'BAL', 'away_team': 'OPP',
             'home_team_score': 31, 'away_team_score': 17}
            for w in range(1, 12)
        ]

        calc = GameScriptCalculator(mock_config, mock_games)
        multiplier, tier = calc.calculate(player)

        assert tier == "RUN_HEAVY"
        assert multiplier > 1.0  # RB should get boost

    def test_point_diff_cap(self, calculator):
        """Test blowout games are capped at +/- 21"""
        mock_games = [
            {'week': 1, 'home_team': 'NYJ', 'away_team': 'OPP',
             'home_team_score': 3, 'away_team_score': 45}  # -42 raw
        ]

        calc = GameScriptCalculator(mock_config, mock_games)
        tendency = calc._calculate_team_tendency('NYJ')

        # Should be capped at -21, not -42
        assert tendency['avg_point_differential'] == -21.0
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 6-8%
- Rationale: Identifies WRs on bad teams who get garbage time volume

**Starter Helper Mode:**
- Expected improvement: 8-12%
- Rationale: Weekly game script prediction improves lineup decisions

**Trade Simulator Mode:**
- Expected improvement: 6-10%
- Rationale: Contextualizes player value based on team quality/script tendency

---

## Real-World Examples

### Example 1: WR on Bad Team (Garbage Time King)

**Garrett Wilson (NYJ, WR)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Team Record | 4-12 |
| Avg Point Differential | -8.3 |
| Games Trailing | 11 |
| Trailing Percentage | 73% |
| Script Tendency | PASS_HEAVY |
| Position | WR |
| Multiplier | 1.04^1.5 = 1.0606 |

**Reason String:** `"Game Script (PASS_HEAVY): Avg -8.3 pts, 73% trailing"`

### Example 2: RB on Dominant Team (Clock Killer)

**Derrick Henry (BAL, RB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Team Record | 12-4 |
| Avg Point Differential | +7.8 |
| Games Leading | 12 |
| Trailing Percentage | 25% |
| Script Tendency | RUN_HEAVY |
| Position | RB |
| Multiplier | 1.04^1.5 = 1.0606 |

**Reason String:** `"Game Script (RUN_HEAVY): Avg +7.8 pts, 25% trailing"`

### Example 3: RB on Bad Team (Script Victim)

**Breece Hall (NYJ, RB)** - 2024 Season:

| Metric | Value |
|--------|-------|
| Team Record | 4-12 |
| Avg Point Differential | -8.3 |
| Trailing Percentage | 73% |
| Script Tendency | PASS_HEAVY |
| Position | RB |
| Multiplier | 0.98^1.5 = 0.9701 |

**Reason String:** `"Game Script (PASS_HEAVY): Avg -8.3 pts, 73% trailing"`

---

## Dependencies

### Data Dependencies
- `game_data.csv` - Available in `data/game_data.csv` with scores
- `team` - Available in all player JSON files

### Code Dependencies
- `ConfigManager` - Existing
- `FantasyPlayer` - Existing
- `GameScriptCalculator` - To be created
- `GameDataLoader` - To be created (or extend existing)

---

## Risks & Mitigations

### Risk 1: Early Season Small Sample
**Likelihood:** High (weeks 1-4) | **Impact:** Medium

**Description:** Script tendency unreliable with few games

**Mitigation:** Require MIN_GAMES (3), use prior season data for weeks 1-2

### Risk 2: Pass-Catching RBs Mismatch
**Likelihood:** Medium | **Impact:** Medium

**Description:** RBs like CMC/Kamara benefit from passing game scripts

**Mitigation:** Add receiving RB detection (6+ tgt/game) to use WR formula

---

## Open Questions

**Questions for User:**
1. Should pass-catching RBs (6+ targets/game) use WR multipliers instead of RB?
2. Use season-long script tendency or rolling 4-week average?
3. Should we factor in Vegas lines for upcoming game script prediction?

---

## Related Metrics

**Complementary Metrics:**
- **M44 (Opponent Offensive Strength)** - DST context that affects game script
- **M27 (Pass-to-Run Ratio)** - Team tendency regardless of script

**Prerequisites:**
- None - foundational team context metric

---

## Implementation Checklist

**Pre-Implementation:**
- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed
- [ ] User questions answered

**Implementation:**
- [ ] GameScriptCalculator module created
- [ ] GameDataLoader created/extended
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
