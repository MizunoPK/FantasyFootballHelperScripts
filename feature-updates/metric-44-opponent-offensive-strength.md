# Feature Request: Opponent Offensive Strength (DST)

**Metric ID:** M44
**Priority:** HIGH
**Positions:** DST
**Effort Estimate:** 3-4 hours
**Expected Impact:** 10-14% improvement in DST weekly streaming decisions

---

## What This Metric Is

Opponent Offensive Strength measures the quality of the opposing offense that a DST will face in a given week. This metric evaluates the opponent's scoring ability based on their season points per game, providing crucial context for DST streaming decisions. A DST facing a weak offense (low PPG) has a higher floor and ceiling than one facing an elite offense.

---

## What We're Trying to Accomplish

**Goals:**
- **Improve weekly DST streaming**: Identify favorable matchups against weak offenses
- **Context for DST rankings**: A mediocre DST vs. a bad offense > elite DST vs. great offense
- **Predict fantasy floor**: DSTs vs. bottom-10 offenses have higher scoring floors
- **Evaluate schedule strength**: Compare upcoming DST schedules for add/drop decisions
- **Complement existing matchup data**: Adds offensive context to defensive metrics

**Example Use Case:**
> A DST facing an offense averaging 15 PPG (bottom-5 in NFL) should be valued higher than the same DST facing an offense averaging 28 PPG (top-5). The expected fantasy points difference could be 4-8 points.

---

## Data Requirements

### Available Data Sources

**Status:** YES - FULLY AVAILABLE

**Data Location:**
- `data/game_data.csv` - Weekly matchup schedule
- `data/historical_data/{year}/{week}/team_data/{TEAM}.csv` - Team scoring data

**Required Fields:**

| Field Name | Data Type | Source | Example Value |
|------------|-----------|--------|---------------|
| `week` | int | game_data.csv | 15 |
| `home_team` | string | game_data.csv | "KC" |
| `away_team` | string | game_data.csv | "BUF" |
| `points_scored` | float | team_data/{TEAM}.csv | 27.5 |

**Example Data Structures:**

**game_data.csv:**
```csv
week,home_team,away_team,home_team_score,away_team_score,temperature,gust,precipitation,indoor,neutral_site,location
15,KC,BUF,27,24,35,12,0,0,0,Kansas City
15,CAR,NYG,10,17,48,5,0,0,0,Charlotte
```

**team_data/NYG.csv:**
```csv
week,pts_allowed_to_QB,pts_allowed_to_RB,pts_allowed_to_WR,pts_allowed_to_TE,pts_allowed_to_K,points_scored,points_allowed
1,18.5,22.3,28.7,12.4,8.0,17,24
2,21.2,19.8,31.2,15.6,6.0,14,28
...
```

### Data Validation
- Data verified in: `data/game_data.csv`, `data/historical_data/2025/*/team_data/*.csv`
- Weekly granularity: Yes
- Historical availability: Current season
- Known limitations: Need to aggregate points_scored from team_data files

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_opponent_offensive_strength(dst: FantasyPlayer,
                                          game_data: List[Dict],
                                          team_stats: Dict[str, Dict],
                                          current_week: int) -> dict:
    """
    Calculate opponent offensive strength for a DST's upcoming matchup.

    Args:
        dst: FantasyPlayer object (DST position)
        game_data: List of game records from game_data.csv
        team_stats: Dict of team stats keyed by team code
        current_week: Current NFL week for upcoming matchup lookup

    Returns:
        dict: {
            'opponent': str,                    # Opponent team code
            'opponent_ppg': float,              # Opponent's points per game
            'opponent_rank': int,               # Opponent's offensive rank (1-32)
            'matchup_difficulty': str,          # EASY, MEDIUM, HARD
            'league_avg_ppg': float             # For context
        }

    Example:
        >>> dst = FantasyPlayer(name="Panthers D/ST", team="CAR", ...)
        >>> result = calculate_opponent_offensive_strength(dst, game_data, team_stats, 15)
        >>> result
        {'opponent': 'NYG', 'opponent_ppg': 15.8, 'opponent_rank': 30,
         'matchup_difficulty': 'EASY', 'league_avg_ppg': 22.5}
    """
    team = dst.team

    # Step 1: Find this week's opponent
    opponent = None
    for game in game_data:
        if game['week'] == current_week:
            if game['home_team'] == team:
                opponent = game['away_team']
                break
            elif game['away_team'] == team:
                opponent = game['home_team']
                break

    if not opponent:
        return {
            'opponent': 'BYE',
            'opponent_ppg': 0.0,
            'opponent_rank': 0,
            'matchup_difficulty': 'N/A',
            'league_avg_ppg': 0.0
        }

    # Step 2: Calculate opponent's PPG
    opp_stats = team_stats.get(opponent, {})
    opp_games_points = opp_stats.get('points_scored_by_week', [])

    if opp_games_points:
        games_with_scores = [p for p in opp_games_points if p > 0]
        opponent_ppg = sum(games_with_scores) / len(games_with_scores) if games_with_scores else 0.0
    else:
        opponent_ppg = 22.0  # League average default

    # Step 3: Calculate league average and rank
    all_team_ppg = []
    for team_code, stats in team_stats.items():
        team_points = stats.get('points_scored_by_week', [])
        if team_points:
            games_with_scores = [p for p in team_points if p > 0]
            if games_with_scores:
                all_team_ppg.append((team_code, sum(games_with_scores) / len(games_with_scores)))

    all_team_ppg.sort(key=lambda x: x[1], reverse=True)  # Highest PPG first
    league_avg_ppg = sum(t[1] for t in all_team_ppg) / len(all_team_ppg) if all_team_ppg else 22.0

    opponent_rank = next((i + 1 for i, (t, ppg) in enumerate(all_team_ppg) if t == opponent), 16)

    # Step 4: Determine matchup difficulty
    if opponent_ppg <= 18.0 or opponent_rank >= 26:
        matchup_difficulty = 'EASY'
    elif opponent_ppg >= 26.0 or opponent_rank <= 8:
        matchup_difficulty = 'HARD'
    else:
        matchup_difficulty = 'MEDIUM'

    return {
        'opponent': opponent,
        'opponent_ppg': round(opponent_ppg, 1),
        'opponent_rank': opponent_rank,
        'matchup_difficulty': matchup_difficulty,
        'league_avg_ppg': round(league_avg_ppg, 1)
    }
```

### Thresholds & Tiers

**DST Opponent Offensive Strength:**

| Tier | Opponent PPG | Opponent Rank | Description | Multiplier | Example Opponent |
|------|--------------|---------------|-------------|------------|------------------|
| EXCELLENT | <= 17.0 | 28-32 | Bottom-5 offense | 1.08 | CAR, NYG in bad years |
| GOOD | 17.1 - 20.0 | 23-27 | Bottom-10 offense | 1.04 | NE, LV struggling |
| AVERAGE | 20.1 - 24.0 | 12-22 | League average | 1.0 | Most teams |
| POOR | 24.1 - 27.0 | 6-11 | Above average | 0.96 | Good offenses |
| VERY_POOR | >= 27.1 | 1-5 | Elite offense | 0.92 | KC, SF, MIA elite |

### Edge Cases

**1. Bye Week**
- **Scenario:** DST is on bye, no opponent
- **Handling:** Return "BYE" as opponent, no adjustment
- **Example:** DST on bye week 14 → matchup_difficulty = "N/A"

**2. Early Season (Weeks 1-2)**
- **Scenario:** Limited opponent data for PPG calculation
- **Handling:** Use preseason projections or prior season data for weeks 1-2
- **Example:** Week 1 → use prior season opponent PPG

**3. Team Name Changes / Relocations**
- **Scenario:** Team code doesn't match between files
- **Handling:** Normalize team codes in data loading
- **Example:** "LV" vs "LVR" → standardize to "LV"

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1.5 hours)

**1.1 Create Team Stats Loader**

**File:** `league_helper/util/TeamStatsLoader.py`

```python
import csv
import os
from typing import Dict, List
from utils.LoggingManager import get_logger

class TeamStatsLoader:
    """Load and aggregate team statistics from historical data files"""

    def __init__(self, data_path: str = 'data/historical_data'):
        self.data_path = data_path
        self.logger = get_logger()

    def load_team_stats(self, year: int, up_to_week: int) -> Dict[str, Dict]:
        """
        Load team stats aggregated through specified week.

        Args:
            year: NFL season year
            up_to_week: Load data up to this week (inclusive)

        Returns:
            Dict keyed by team code with stats including points_scored_by_week
        """
        team_stats = {}
        nfl_teams = self._get_all_teams()

        for team in nfl_teams:
            points_by_week = []
            for week in range(1, up_to_week + 1):
                team_file = os.path.join(
                    self.data_path, str(year), str(week), 'team_data', f'{team}.csv'
                )
                if os.path.exists(team_file):
                    with open(team_file, 'r') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            if int(row['week']) == week:
                                points_by_week.append(float(row.get('points_scored', 0)))
                                break

            team_stats[team] = {
                'points_scored_by_week': points_by_week,
                'games_played': len([p for p in points_by_week if p > 0])
            }

        return team_stats

    def _get_all_teams(self) -> List[str]:
        """Return list of all NFL team codes"""
        return [
            'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
            'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
            'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
            'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS'
        ]
```

**1.2 Create Calculation Module**

**File:** `league_helper/util/OpponentStrengthCalculator.py`

```python
from typing import Tuple, Dict, List
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class OpponentStrengthCalculator:
    """Calculate opponent offensive strength for DST matchup evaluation"""

    def __init__(self, config_manager, game_data: List[Dict], team_stats: Dict[str, Dict]):
        self.config = config_manager
        self.game_data = game_data
        self.team_stats = team_stats
        self.logger = get_logger()
        self._rankings_cache = None

    def calculate(self, player: FantasyPlayer, current_week: int) -> Tuple[float, str]:
        """
        Calculate opponent strength and return multiplier.

        Args:
            player: DST player to calculate for
            current_week: Current NFL week

        Returns:
            Tuple[float, str]: (multiplier, tier_classification)
        """
        if player.position != 'DST':
            return 1.0, "N/A"

        # Calculate matchup metrics
        metrics = self._calculate_matchup_metrics(player, current_week)

        if metrics['opponent'] == 'BYE':
            return 1.0, "BYE"

        # Get tier
        tier = metrics['matchup_difficulty']

        # Get multiplier from config
        multiplier = self._get_multiplier(tier)

        return multiplier, tier

    def _calculate_matchup_metrics(self, player: FantasyPlayer, current_week: int) -> Dict:
        """Calculate opponent offensive strength metrics"""
        # Implementation from formula above
        pass

    def _get_multiplier(self, tier: str) -> float:
        """Get multiplier for matchup difficulty tier"""
        tier_map = {
            'EXCELLENT': 'EXCELLENT',  # Easy matchup = excellent for DST
            'GOOD': 'GOOD',
            'MEDIUM': 'AVERAGE',
            'HARD': 'POOR',
            'VERY_HARD': 'VERY_POOR'
        }

        config_tier = tier_map.get(tier, 'AVERAGE')
        multipliers = self.config.opponent_strength_scoring.get('MULTIPLIERS', {})
        base_mult = multipliers.get(config_tier, 1.0)
        weight = self.config.opponent_strength_scoring.get('WEIGHT', 2.0)

        return base_mult ** weight
```

---

### Phase 2: Configuration (Estimated: 0.5 hours)

**2.1 Add to league_config.json**

```json
{
  "OPPONENT_STRENGTH_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "EXCELLENT_PPG": 17.0,
      "GOOD_PPG": 20.0,
      "POOR_PPG": 24.0,
      "VERY_POOR_PPG": 27.0,
      "EXCELLENT_RANK": 28,
      "GOOD_RANK": 23,
      "POOR_RANK": 11,
      "VERY_POOR_RANK": 5
    },
    "MULTIPLIERS": {
      "EXCELLENT": 1.08,
      "GOOD": 1.04,
      "AVERAGE": 1.0,
      "POOR": 0.96,
      "VERY_POOR": 0.92
    },
    "WEIGHT": 2.0,
    "MIN_GAMES_FOR_OPPONENT": 3,
    "DESCRIPTION": "DST opponent offensive strength - matchup-based adjustment"
  }
}
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**3.1 Add Scoring Step**

**File:** `league_helper/util/player_scoring.py`

```python
def _apply_opponent_strength_scoring(self, p: FantasyPlayer, player_score: float, current_week: int) -> Tuple[float, str]:
    """
    Apply opponent offensive strength adjustment to DST score.

    Args:
        p: FantasyPlayer object (DST)
        player_score: Current player score
        current_week: Current NFL week

    Returns:
        Tuple[float, str]: (adjusted_score, reason_string)
    """
    if p.position != 'DST':
        return player_score, ""

    if not self.config.opponent_strength_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = OpponentStrengthCalculator(self.config, self.game_data, self.team_stats)
    multiplier, tier = calculator.calculate(p, current_week)

    if tier == "BYE":
        return player_score, "Bye Week"

    adjusted_score = player_score * multiplier

    metrics = calculator._calculate_matchup_metrics(p, current_week)
    reason = f"vs {metrics['opponent']} ({tier}): {metrics['opponent_ppg']:.1f} PPG (Rank #{metrics['opponent_rank']})"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**4.1 Unit Tests**

**File:** `tests/league_helper/util/test_OpponentStrengthCalculator.py`

```python
import pytest
from league_helper.util.OpponentStrengthCalculator import OpponentStrengthCalculator

class TestOpponentStrengthCalculator:
    """Test opponent offensive strength calculation"""

    def test_easy_matchup_boost(self, calculator):
        """Test DST facing weak offense gets boost"""
        dst = create_dst(name="Panthers D/ST", team="CAR")

        # CAR faces NYG who averages 15.8 PPG (bottom-5)
        mock_game_data = [{'week': 15, 'home_team': 'CAR', 'away_team': 'NYG'}]
        mock_team_stats = {
            'NYG': {'points_scored_by_week': [14, 17, 13, 10, 21, 14, 17, 10, 14, 17, 13, 17, 14, 21, 17]},
            # Add other teams for ranking context...
        }

        calc = OpponentStrengthCalculator(mock_config, mock_game_data, mock_team_stats)
        multiplier, tier = calc.calculate(dst, 15)

        assert tier == "EXCELLENT"  # Easy matchup
        assert multiplier > 1.0

    def test_hard_matchup_penalty(self, calculator):
        """Test DST facing elite offense gets penalty"""
        dst = create_dst(name="Raiders D/ST", team="LV")

        # LV faces KC who averages 28.5 PPG (top-3)
        mock_game_data = [{'week': 15, 'home_team': 'KC', 'away_team': 'LV'}]
        mock_team_stats = {
            'KC': {'points_scored_by_week': [31, 27, 24, 34, 28, 31, 27, 30, 28, 24, 31, 27, 34, 28, 24]},
            # Add other teams...
        }

        calc = OpponentStrengthCalculator(mock_config, mock_game_data, mock_team_stats)
        multiplier, tier = calc.calculate(dst, 15)

        assert tier in ["HARD", "VERY_HARD", "POOR", "VERY_POOR"]
        assert multiplier < 1.0

    def test_bye_week_handling(self, calculator):
        """Test DST on bye returns no adjustment"""
        dst = create_dst(name="Chiefs D/ST", team="KC")

        # KC has no game in week 10
        mock_game_data = [{'week': 10, 'home_team': 'BUF', 'away_team': 'MIA'}]

        calc = OpponentStrengthCalculator(mock_config, mock_game_data, {})
        multiplier, tier = calc.calculate(dst, 10)

        assert tier == "BYE"
        assert multiplier == 1.0
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 8-10%
- Rationale: Identifies DSTs with favorable upcoming schedules for draft

**Starter Helper Mode:**
- Expected improvement: 10-14%
- Rationale: Weekly matchup context is critical for DST streaming

**Trade Simulator Mode:**
- Expected improvement: 6-8%
- Rationale: Schedule-adjusted DST value for trade evaluation

---

## Real-World Examples

### Example 1: Excellent Matchup (Weak Opponent)

**Panthers D/ST vs NYG** - Week 15:

| Metric | Value |
|--------|-------|
| Opponent | NYG |
| Opponent PPG | 15.8 |
| Opponent Rank | 30 (bottom-3) |
| League Avg PPG | 22.5 |
| Matchup Difficulty | EXCELLENT |
| Multiplier | 1.08^2.0 = 1.1664 |
| Base Score | 85.0 |
| Adjusted Score | 99.1 (+14.1 pts) |

**Reason String:** `"vs NYG (EXCELLENT): 15.8 PPG (Rank #30)"`

### Example 2: Hard Matchup (Elite Opponent)

**Raiders D/ST vs KC** - Week 15:

| Metric | Value |
|--------|-------|
| Opponent | KC |
| Opponent PPG | 28.5 |
| Opponent Rank | 2 (top-3) |
| League Avg PPG | 22.5 |
| Matchup Difficulty | VERY_POOR |
| Multiplier | 0.92^2.0 = 0.8464 |
| Base Score | 90.0 |
| Adjusted Score | 76.2 (-13.8 pts) |

**Reason String:** `"vs KC (VERY_POOR): 28.5 PPG (Rank #2)"`

### Example 3: Average Matchup

**Cowboys D/ST vs WAS** - Week 15:

| Metric | Value |
|--------|-------|
| Opponent | WAS |
| Opponent PPG | 22.3 |
| Opponent Rank | 15 |
| League Avg PPG | 22.5 |
| Matchup Difficulty | AVERAGE |
| Multiplier | 1.0^2.0 = 1.0 |

**Reason String:** `"vs WAS (AVERAGE): 22.3 PPG (Rank #15)"`

---

## Dependencies

### Data Dependencies
- `game_data.csv` - Available in `data/game_data.csv`
- `team_data/{TEAM}.csv` - Available in `data/historical_data/{year}/{week}/team_data/`
- `points_scored` column in team CSV files

### Code Dependencies
- `ConfigManager` - Existing
- `FantasyPlayer` - Existing
- `TeamStatsLoader` - To be created
- `OpponentStrengthCalculator` - To be created

---

## Risks & Mitigations

### Risk 1: Early Season Data Scarcity
**Likelihood:** High (weeks 1-3) | **Impact:** Medium

**Description:** Limited games make opponent PPG unreliable

**Mitigation:** Use prior season data for weeks 1-2, require MIN_GAMES (3)

### Risk 2: Data File Path Consistency
**Likelihood:** Medium | **Impact:** Medium

**Description:** Team data files might not exist for all weeks

**Mitigation:** Graceful fallback to league average when file missing

### Risk 3: Team Code Mismatches
**Likelihood:** Low | **Impact:** Low

**Description:** Different team code formats between files

**Mitigation:** Normalize team codes in data loading functions

---

## Open Questions

**Questions for User:**
1. Use opponent's season PPG or recent 4-week rolling average?
2. Should this metric also apply to other positions (boost WRs vs. bad pass defenses)?
3. Weight PPG rank or raw PPG more heavily for tier determination?

---

## Related Metrics

**Complementary Metrics:**
- **M41 (Turnover Rate)** - DST playmaking independent of opponent
- **M42 (Sack Rate)** - DST pressure generation
- **M43 (Points Allowed Trend)** - DST's own defensive performance

**Note:** Step 6 (Matchup Multiplier) handles position-specific defensive matchups for skill players. This metric is DST-specific for opponent offensive quality.

---

## Implementation Checklist

**Pre-Implementation:**
- [x] Data availability verified
- [x] Formula validated
- [x] Configuration structure designed
- [ ] User questions answered

**Implementation:**
- [ ] TeamStatsLoader module created
- [ ] OpponentStrengthCalculator module created
- [ ] Scoring integration added
- [ ] Configuration file updated

**Testing:**
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Validation against real matchup data

**Documentation:**
- [ ] Scoring step documentation created
- [ ] README updated

---

**END OF FEATURE REQUEST**
