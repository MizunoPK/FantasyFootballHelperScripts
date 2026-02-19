# Feature Request: QB Quality (Passing Game Context)

**Metric ID:** M12
**Priority:** HIGH
**Positions:** WR, TE, RB
**Effort Estimate:** 3-4 hours
**Expected Impact:** 12-18% improvement in pass-catcher evaluation

---

## What This Metric Is

QB Quality measures the skill level of a player's team quarterback, applying bonuses to pass-catchers (WR, TE, RB) with elite QBs and penalties to those with poor QBs. Elite QBs like Patrick Mahomes and Josh Allen elevate their receivers' fantasy ceilings, while struggling QBs limit their pass-catchers' upside regardless of individual talent.

---

## What We're Trying to Accomplish

**Goals:**
- **Identify elevated pass-catchers**: WRs/TEs with elite QBs (Mahomes, Allen, Burrow) have significantly higher ceilings and more consistent production
- **Penalize QB-limited receivers**: Talented receivers with poor QBs (rookie QBs, backup situations) are capped regardless of skill
- **Improve accuracy of waiver pickups**: A WR2 with an elite QB often outproduces a WR1 with a poor QB
- **Account for QB changes**: Mid-season QB injuries or benchings dramatically affect pass-catcher value
- **Draft strategy**: Prioritize pass-catchers tied to proven elite QBs over those with uncertain QB situations

**Example Use Case:**
> Nico Collins with C.J. Stroud (top-10 QB) vs. a similarly talented WR with a bottom-5 QB. Collins benefits from accurate deep balls, consistent target quality, and an offense that stays on the field. The WR with the poor QB faces inaccurate throws, fewer red zone opportunities, and more three-and-outs limiting total targets.

---

## Data Requirements

### Available Data Sources

**Status:** ✅ FULLY AVAILABLE

**Data Location:** `data/player_data/qb_data.json` (for QB stats), all position files (for team linkage)

**Required Fields:**

| Field Name | Data Type | Weekly Array? | Source | Example Value |
|------------|-----------|---------------|--------|---------------|
| `passing.pass_yds` | float | Yes (17 weeks) | QB JSON | 285.0 |
| `passing.pass_td` | float | Yes (17 weeks) | QB JSON | 2.0 |
| `passing.interceptions` | float | Yes (17 weeks) | QB JSON | 1.0 |
| `passing.completions` | float | Yes (17 weeks) | QB JSON | 24.0 |
| `passing.attempts` | float | Yes (17 weeks) | QB JSON | 35.0 |
| `team` | string | No | All player JSON | "KC" |

**Example Data Structure:**
```json
{
  "id": "3139477",
  "name": "Patrick Mahomes",
  "team": "KC",
  "position": "QB",
  "passing": {
    "pass_yds": [272.0, 328.0, 291.0, 0.0, 315.0, 284.0, 302.0, 346.0, 268.0, 298.0, 324.0, 289.0, 312.0, 295.0],
    "pass_td": [2.0, 3.0, 2.0, 0.0, 3.0, 2.0, 4.0, 3.0, 2.0, 2.0, 3.0, 2.0, 3.0, 2.0],
    "interceptions": [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0],
    "completions": [23.0, 28.0, 25.0, 0.0, 27.0, 24.0, 29.0, 31.0, 22.0, 26.0, 28.0, 25.0, 27.0, 24.0],
    "attempts": [32.0, 38.0, 34.0, 0.0, 36.0, 33.0, 40.0, 42.0, 31.0, 35.0, 39.0, 34.0, 37.0, 33.0]
  }
}
```

### Data Validation
- ✅ Data verified in: `data/player_data/qb_data.json`
- ✅ Weekly granularity: Yes (17 weeks per season)
- ✅ Historical availability: Current season
- ⚠️ Known limitations: Need to identify starting QB per team (highest attempts)

---

## Calculation Formula

### Mathematical Definition

```python
def calculate_qb_quality_score(qb: FantasyPlayer) -> dict:
    """
    Calculate composite QB quality score.

    Args:
        qb: FantasyPlayer object with passing stats (QB position)

    Returns:
        dict: {
            'qb_quality_score': float,
            'fantasy_ppg': float,
            'completion_pct': float,
            'td_int_ratio': float,
            'yards_per_attempt': float,
            'tier': str
        }

    Example:
        >>> qb = FantasyPlayer(name="Patrick Mahomes", position="QB", stats={...})
        >>> result = calculate_qb_quality_score(qb)
        >>> result
        {'qb_quality_score': 92.5, 'fantasy_ppg': 22.4, 'tier': 'ELITE'}
    """
    # Step 1: Get passing stats
    weekly_yards = qb.stats['passing']['pass_yds']
    weekly_tds = qb.stats['passing']['pass_td']
    weekly_ints = qb.stats['passing']['interceptions']
    weekly_completions = qb.stats['passing']['completions']
    weekly_attempts = qb.stats['passing']['attempts']

    # Step 2: Calculate games played (games with attempts)
    games_played = len([a for a in weekly_attempts if a > 0])

    if games_played < 3:
        return {
            'qb_quality_score': 0.0,
            'fantasy_ppg': 0.0,
            'completion_pct': 0.0,
            'td_int_ratio': 0.0,
            'yards_per_attempt': 0.0,
            'tier': 'INSUFFICIENT_DATA'
        }

    # Step 3: Calculate season totals
    total_yards = sum(weekly_yards)
    total_tds = sum(weekly_tds)
    total_ints = sum(weekly_ints)
    total_completions = sum(weekly_completions)
    total_attempts = sum(weekly_attempts)

    # Step 4: Calculate component metrics
    completion_pct = (total_completions / total_attempts * 100) if total_attempts > 0 else 0.0
    td_int_ratio = (total_tds / total_ints) if total_ints > 0 else total_tds * 2  # Cap at 2x TDs if 0 INTs
    yards_per_attempt = (total_yards / total_attempts) if total_attempts > 0 else 0.0

    # Step 5: Calculate fantasy PPG (standard 4pt passing TD scoring)
    # 0.04 pts per yard, 4 pts per TD, -2 pts per INT
    total_fantasy_pts = (total_yards * 0.04) + (total_tds * 4) - (total_ints * 2)
    fantasy_ppg = total_fantasy_pts / games_played

    # Step 6: Calculate composite QB quality score (0-100 scale)
    # Weighted components: Fantasy PPG (40%), Completion % (20%), TD:INT (25%), YPA (15%)
    fantasy_ppg_normalized = min(fantasy_ppg / 25.0, 1.0) * 100  # 25 PPG = 100
    completion_normalized = min((completion_pct - 55) / 15, 1.0) * 100  # 55-70% range
    td_int_normalized = min(td_int_ratio / 4.0, 1.0) * 100  # 4.0 ratio = 100
    ypa_normalized = min((yards_per_attempt - 5.5) / 3.5, 1.0) * 100  # 5.5-9.0 range

    qb_quality_score = (
        fantasy_ppg_normalized * 0.40 +
        completion_normalized * 0.20 +
        td_int_normalized * 0.25 +
        ypa_normalized * 0.15
    )

    # Step 7: Determine tier
    tier = _classify_qb_quality_tier(qb_quality_score)

    return {
        'qb_quality_score': round(qb_quality_score, 1),
        'fantasy_ppg': round(fantasy_ppg, 1),
        'completion_pct': round(completion_pct, 1),
        'td_int_ratio': round(td_int_ratio, 2),
        'yards_per_attempt': round(yards_per_attempt, 1),
        'tier': tier
    }

def _classify_qb_quality_tier(qb_quality_score: float) -> str:
    """
    Classify QB tier based on composite quality score.

    Args:
        qb_quality_score: Composite score (0-100)

    Returns:
        str: Tier classification
    """
    if qb_quality_score >= 80:
        return "ELITE"       # Top 5 QBs (Mahomes, Allen, Burrow, etc.)
    elif qb_quality_score >= 65:
        return "GOOD"        # QB1 territory (Stroud, Hurts, etc.)
    elif qb_quality_score >= 50:
        return "AVERAGE"     # Serviceable starters
    elif qb_quality_score >= 35:
        return "POOR"        # Below average starters
    else:
        return "VERY_POOR"   # Backups, struggling rookies
```

### Thresholds & Tiers

**QB Quality Score:**

| Tier | Threshold | Description | Multiplier | Example QB |
|------|-----------|-------------|------------|------------|
| ELITE | ≥80 | Top-tier franchise QB | 1.06 | Patrick Mahomes, Josh Allen, Joe Burrow |
| GOOD | 65-79 | Quality starting QB | 1.03 | C.J. Stroud, Jalen Hurts, Dak Prescott |
| AVERAGE | 50-64 | Serviceable starter | 1.0 | Geno Smith, Kirk Cousins |
| POOR | 35-49 | Below average starter | 0.97 | Struggling veterans, some rookies |
| VERY_POOR | <35 | Backup or struggling QB | 0.94 | Backup QBs, injured starters replaced |

**Position-Specific Weights:**

| Position | Weight | Rationale |
|----------|--------|-----------|
| WR | 2.5 | Most dependent on QB quality for targets and accuracy |
| TE | 2.0 | Heavily dependent but often safety valve role mitigates |
| RB | 1.0 | Less dependent but affects passing game involvement |

**Note:** Requires minimum 3 games for QB to qualify for rating.

### Edge Cases

**1. Mid-Season QB Change**
- **Scenario:** Starting QB injured, backup takes over (e.g., Tua injured, backup starts)
- **Handling:** Recalculate based on current starter's stats; if new QB has <3 games, use team's combined QB stats
- **Example:** Dolphins WRs lose value when Tua is out

**2. QB Platoon/Committee**
- **Scenario:** Team uses two QBs regularly (rare but happens)
- **Handling:** Use QB with most attempts as "starter" for rating
- **Example:** Ravens occasionally used Lamar + backup in past

**3. Rookie QB Early Season**
- **Scenario:** Rookie QB with only 2-3 games of data
- **Handling:** If <3 games, use AVERAGE tier (1.0 multiplier) until more data
- **Example:** Week 4 rookie QB - wait for more sample

**4. Elite QB on Bye Week**
- **Scenario:** Calculating for a week when the QB is on bye
- **Handling:** Use season-long QB quality score, not week-specific
- **Example:** Mahomes on bye - Chiefs WRs still rated based on his season quality

**5. Team with No Clear Starter**
- **Scenario:** Multiple QBs with similar attempts (injury carousel)
- **Handling:** Use weighted average of all QBs or apply POOR/VERY_POOR default
- **Example:** Injury-plagued team cycling through QBs

---

## Implementation Plan

### Phase 1: Data Pipeline (Estimated: 1.5 hours)

**File:** `league_helper/util/QBQualityCalculator.py`

```python
from typing import Tuple, Dict, List, Optional
from league_helper.util.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class QBQualityCalculator:
    """Calculate QB quality scores and apply to pass-catchers"""

    def __init__(self, config_manager, player_manager):
        self.config = config_manager
        self.player_manager = player_manager
        self.logger = get_logger()
        self._qb_cache = {}  # Cache QB quality by team

    def get_team_qb_quality(self, team: str) -> Tuple[float, str, Dict]:
        """
        Get QB quality score for a team.

        Args:
            team: Team abbreviation (e.g., "KC")

        Returns:
            Tuple[float, str, Dict]: (multiplier, tier, qb_metrics)
        """
        # Check cache first
        if team in self._qb_cache:
            return self._qb_cache[team]

        # Find starting QB for team (highest attempts)
        starting_qb = self._find_starting_qb(team)

        if starting_qb is None:
            self._qb_cache[team] = (1.0, "UNKNOWN", {})
            return 1.0, "UNKNOWN", {}

        # Calculate QB quality
        qb_metrics = self._calculate_qb_quality(starting_qb)

        # Get multiplier from config
        multiplier = self.config.get_qb_quality_multiplier(qb_metrics['tier'])

        self._qb_cache[team] = (multiplier, qb_metrics['tier'], qb_metrics)

        self.logger.debug(
            f"Team {team} QB {starting_qb.name}: {qb_metrics['qb_quality_score']:.1f} score "
            f"({qb_metrics['fantasy_ppg']:.1f} PPG, {qb_metrics['completion_pct']:.1f}% CMP) "
            f"(Tier: {qb_metrics['tier']}, Multiplier: {multiplier:.3f})"
        )

        return multiplier, qb_metrics['tier'], qb_metrics

    def calculate_for_player(self, player: FantasyPlayer) -> Tuple[float, str]:
        """
        Calculate QB quality multiplier for a pass-catcher.

        Args:
            player: FantasyPlayer (WR, TE, or RB)

        Returns:
            Tuple[float, str]: (multiplier, tier)
        """
        if player.position not in ['WR', 'TE', 'RB']:
            return 1.0, "N/A"

        multiplier, tier, _ = self.get_team_qb_quality(player.team)
        return multiplier, tier

    def _find_starting_qb(self, team: str) -> Optional[FantasyPlayer]:
        """Find the starting QB for a team based on pass attempts"""
        qbs = self.player_manager.get_players_by_position_and_team('QB', team)

        if not qbs:
            return None

        # Find QB with most attempts
        starting_qb = max(qbs, key=lambda qb: sum(qb.stats.get('passing', {}).get('attempts', [0])))

        return starting_qb

    def _calculate_qb_quality(self, qb: FantasyPlayer) -> Dict:
        """Calculate QB quality metrics"""
        passing = qb.stats.get('passing', {})

        weekly_yards = passing.get('pass_yds', [])
        weekly_tds = passing.get('pass_td', [])
        weekly_ints = passing.get('interceptions', [])
        weekly_completions = passing.get('completions', [])
        weekly_attempts = passing.get('attempts', [])

        games_played = len([a for a in weekly_attempts if a > 0])

        if games_played < self.config.qb_quality_scoring.get('MIN_GAMES', 3):
            return {
                'qb_quality_score': 50.0,  # Default to AVERAGE
                'fantasy_ppg': 0.0,
                'completion_pct': 0.0,
                'td_int_ratio': 0.0,
                'yards_per_attempt': 0.0,
                'tier': 'INSUFFICIENT_DATA'
            }

        total_yards = sum(weekly_yards)
        total_tds = sum(weekly_tds)
        total_ints = sum(weekly_ints)
        total_completions = sum(weekly_completions)
        total_attempts = sum(weekly_attempts)

        completion_pct = (total_completions / total_attempts * 100) if total_attempts > 0 else 0.0
        td_int_ratio = (total_tds / total_ints) if total_ints > 0 else min(total_tds * 2, 10.0)
        yards_per_attempt = (total_yards / total_attempts) if total_attempts > 0 else 0.0

        total_fantasy_pts = (total_yards * 0.04) + (total_tds * 4) - (total_ints * 2)
        fantasy_ppg = total_fantasy_pts / games_played

        # Composite score calculation
        fantasy_ppg_normalized = min(fantasy_ppg / 25.0, 1.0) * 100
        completion_normalized = max(min((completion_pct - 55) / 15, 1.0), 0.0) * 100
        td_int_normalized = min(td_int_ratio / 4.0, 1.0) * 100
        ypa_normalized = max(min((yards_per_attempt - 5.5) / 3.5, 1.0), 0.0) * 100

        qb_quality_score = (
            fantasy_ppg_normalized * 0.40 +
            completion_normalized * 0.20 +
            td_int_normalized * 0.25 +
            ypa_normalized * 0.15
        )

        tier = self._classify_tier(qb_quality_score)

        return {
            'qb_quality_score': round(qb_quality_score, 1),
            'fantasy_ppg': round(fantasy_ppg, 1),
            'completion_pct': round(completion_pct, 1),
            'td_int_ratio': round(td_int_ratio, 2),
            'yards_per_attempt': round(yards_per_attempt, 1),
            'tier': tier
        }

    def _classify_tier(self, qb_quality_score: float) -> str:
        """Classify QB tier based on quality score"""
        thresholds = self.config.qb_quality_scoring.get('THRESHOLDS', {})

        if qb_quality_score >= thresholds.get('ELITE', 80):
            return "ELITE"
        elif qb_quality_score >= thresholds.get('GOOD', 65):
            return "GOOD"
        elif qb_quality_score >= thresholds.get('AVERAGE', 50):
            return "AVERAGE"
        elif qb_quality_score >= thresholds.get('POOR', 35):
            return "POOR"
        else:
            return "VERY_POOR"

    def clear_cache(self):
        """Clear the QB quality cache (call when data updates)"""
        self._qb_cache = {}
```

---

### Phase 2: Configuration (Estimated: 30 min)

**2.1 Add to league_config.json**

```json
{
  "QB_QUALITY_SCORING": {
    "ENABLED": true,
    "THRESHOLDS": {
      "ELITE": 80,
      "GOOD": 65,
      "AVERAGE": 50,
      "POOR": 35
    },
    "MULTIPLIERS": {
      "ELITE": 1.06,
      "GOOD": 1.03,
      "AVERAGE": 1.0,
      "POOR": 0.97,
      "VERY_POOR": 0.94,
      "INSUFFICIENT_DATA": 1.0,
      "UNKNOWN": 1.0
    },
    "POSITION_WEIGHTS": {
      "WR": 2.5,
      "TE": 2.0,
      "RB": 1.0
    },
    "MIN_GAMES": 3,
    "DESCRIPTION": "QB quality bonus/penalty for pass-catchers based on team QB performance"
  }
}
```

**2.2 Add ConfigManager method**

```python
def get_qb_quality_multiplier(self, tier: str) -> float:
    """
    Get QB quality multiplier for pass-catcher evaluation.

    Args:
        tier: QB tier classification (ELITE, GOOD, AVERAGE, POOR, VERY_POOR)

    Returns:
        float: Multiplier value
    """
    multipliers = self.config.get('QB_QUALITY_SCORING', {}).get('MULTIPLIERS', {})
    return multipliers.get(tier, 1.0)

def get_qb_quality_position_weight(self, position: str) -> float:
    """
    Get position-specific weight for QB quality scoring.

    Args:
        position: Player position (WR, TE, RB)

    Returns:
        float: Position weight
    """
    weights = self.config.get('QB_QUALITY_SCORING', {}).get('POSITION_WEIGHTS', {})
    return weights.get(position, 1.0)
```

---

### Phase 3: Scoring Integration (Estimated: 1 hour)

**File:** `league_helper/util/player_scoring.py`

**Method:** `_apply_qb_quality_scoring()`

```python
def _apply_qb_quality_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """Apply QB quality adjustment to pass-catchers (WR, TE, RB)"""
    if p.position not in ['WR', 'TE', 'RB']:
        return player_score, ""

    if not self.config.qb_quality_scoring.get('ENABLED', False):
        return player_score, ""

    calculator = QBQualityCalculator(self.config, self.player_manager)
    multiplier, tier, qb_metrics = calculator.get_team_qb_quality(p.team)

    if tier in ['N/A', 'UNKNOWN', 'INSUFFICIENT_DATA']:
        return player_score, ""

    # Apply multiplier with position-specific weight
    position_weight = self.config.get_qb_quality_position_weight(p.position)
    final_multiplier = multiplier ** position_weight
    adjusted_score = player_score * final_multiplier

    # Build reason string
    qb_name = qb_metrics.get('qb_name', p.team + ' QB')
    reason = f"QB Quality ({tier}): {qb_metrics['qb_quality_score']:.0f} score"

    return adjusted_score, reason
```

---

### Phase 4: Testing (Estimated: 1 hour)

**File:** `tests/league_helper/util/test_QBQualityCalculator.py`

```python
import pytest
from league_helper.util.QBQualityCalculator import QBQualityCalculator
from league_helper.util.FantasyPlayer import FantasyPlayer
from league_helper.util.ConfigManager import ConfigManager

class TestQBQualityCalculator:
    """Test QB Quality Calculator functionality"""

    @pytest.fixture
    def calculator(self, tmp_path, mock_player_manager):
        """Create calculator with test config"""
        config = ConfigManager(tmp_path)
        return QBQualityCalculator(config, mock_player_manager)

    def test_elite_qb(self, calculator):
        """Test QB with elite stats (Mahomes-level)"""
        qb = FantasyPlayer(
            name="Patrick Mahomes",
            position="QB",
            team="KC",
            stats={
                'passing': {
                    'pass_yds': [285, 320, 298, 0, 310, 275, 340, 295, 288, 315, 302, 290, 325, 280],
                    'pass_td': [2, 3, 2, 0, 3, 2, 4, 2, 2, 3, 3, 2, 3, 2],
                    'interceptions': [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
                    'completions': [24, 28, 25, 0, 27, 23, 30, 25, 24, 28, 26, 24, 29, 23],
                    'attempts': [33, 38, 35, 0, 36, 32, 42, 35, 34, 38, 37, 33, 40, 32]
                }
            }
        )

        metrics = calculator._calculate_qb_quality(qb)

        assert metrics['tier'] == "ELITE"
        assert metrics['qb_quality_score'] >= 80
        assert metrics['fantasy_ppg'] > 18

    def test_poor_qb(self, calculator):
        """Test QB with below average stats"""
        qb = FantasyPlayer(
            name="Struggling QB",
            position="QB",
            team="BAD",
            stats={
                'passing': {
                    'pass_yds': [185, 210, 175, 0, 195, 168, 202, 188, 172, 198, 185, 190, 178, 195],
                    'pass_td': [1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0],
                    'interceptions': [2, 1, 2, 0, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2],
                    'completions': [18, 20, 17, 0, 19, 16, 21, 18, 17, 19, 18, 19, 17, 18],
                    'attempts': [32, 35, 30, 0, 33, 29, 36, 32, 30, 34, 32, 33, 29, 31]
                }
            }
        )

        metrics = calculator._calculate_qb_quality(qb)

        assert metrics['tier'] in ["POOR", "VERY_POOR"]
        assert metrics['qb_quality_score'] < 50
        assert metrics['td_int_ratio'] < 1.0

    def test_insufficient_games(self, calculator):
        """Test QB with <3 games played"""
        qb = FantasyPlayer(
            name="Rookie QB",
            position="QB",
            team="NEW",
            stats={
                'passing': {
                    'pass_yds': [250, 275, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'pass_td': [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'interceptions': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'completions': [22, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    'attempts': [35, 38, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            }
        )

        metrics = calculator._calculate_qb_quality(qb)

        assert metrics['tier'] == "INSUFFICIENT_DATA"

    def test_wr_gets_qb_bonus(self, calculator):
        """Test that WR on elite QB team gets bonus"""
        wr = FantasyPlayer(
            name="Travis Kelce",
            position="TE",
            team="KC",
            stats={'receiving': {'targets': [8, 7, 9]}}
        )

        # Mock KC having an elite QB
        multiplier, tier = calculator.calculate_for_player(wr)

        # Should get positive multiplier for elite QB
        assert tier == "ELITE"
        assert multiplier > 1.0

    def test_non_pass_catcher_neutral(self, calculator):
        """Test that QB position returns neutral"""
        qb = FantasyPlayer(
            name="Patrick Mahomes",
            position="QB",
            team="KC",
            stats={'passing': {'attempts': [35, 38, 40]}}
        )

        multiplier, tier = calculator.calculate_for_player(qb)

        assert multiplier == 1.0
        assert tier == "N/A"
```

---

### Phase 5: Documentation (Estimated: 30 min)

**File:** `docs/scoring/22_qb_quality_scoring.md`

```markdown
# Step 22: QB Quality (Pass-Catcher Context)

**Priority:** HIGH | **Positions:** WR, TE, RB | **Pattern:** Multiplier-based

## Overview

QB Quality measures the skill level of a player's team quarterback, applying bonuses to pass-catchers with elite QBs and penalties to those with poor QBs. Elite QBs elevate their receivers through accurate throws, sustained drives, and red zone efficiency.

## Formula

```
qb_quality_score = (fantasy_ppg_norm * 0.40) + (completion_norm * 0.20) +
                   (td_int_norm * 0.25) + (ypa_norm * 0.15)
```

## Thresholds

- ELITE: ≥80 score (+6% bonus) - Mahomes, Allen, Burrow
- GOOD: 65-79 score (+3% bonus) - Stroud, Hurts, Prescott
- AVERAGE: 50-64 score (no adjustment) - Serviceable starters
- POOR: 35-49 score (-3% penalty) - Below average starters
- VERY_POOR: <35 score (-6% penalty) - Backups, struggling QBs

## Position Weights

- WR: 2.5 (most dependent on QB quality)
- TE: 2.0 (heavily dependent)
- RB: 1.0 (less dependent, but affects passing game)

## Example

**Tyreek Hill (MIA, WR)** with Tua Tagovailoa:
- QB Quality Score: 72
- Tier: GOOD
- Base Multiplier: 1.03
- Position Weight: 2.5
- Final Multiplier: 1.03^2.5 = 1.0765
- Impact: +7.65% to base score

## Why This Matters

Pass-catchers are heavily dependent on their QB's ability to deliver accurate passes, sustain drives, and create scoring opportunities. A WR2 with an elite QB often outproduces a WR1 with a struggling QB.
```

---

## Expected Impact

### Mode-Specific Impact

**Add To Roster Mode:**
- Expected improvement: 12-18%
- Rationale: Identifies undervalued WRs/TEs on elite QB teams vs overvalued ones on poor QB teams

**Starter Helper Mode:**
- Expected improvement: 10-15%
- Rationale: Weekly decisions account for QB quality when choosing between similar receivers

**Trade Simulator Mode:**
- Expected improvement: 15-20%
- Rationale: Trade values properly reflect QB situation - critical for dynasty/keeper leagues

---

## Real-World Examples

### Example 1: Elite QB Boost

**Nico Collins (HOU, WR)** with C.J. Stroud:

| Metric | Value |
|--------|-------|
| QB Quality Score | 74 |
| QB Fantasy PPG | 19.2 |
| QB Completion % | 66.5% |
| Tier | GOOD |
| Multiplier | 1.03^2.5 = 1.0765 |
| Base Score | 185.0 |
| Adjusted Score | 199.2 (+14.2 pts) |

**Reason String:** `"QB Quality (GOOD): 74 score"`

### Example 2: Poor QB Penalty

**WR on Struggling Team (TEAM, WR)** with Poor QB:

| Metric | Value |
|--------|-------|
| QB Quality Score | 38 |
| QB Fantasy PPG | 12.5 |
| QB Completion % | 58.2% |
| Tier | POOR |
| Multiplier | 0.97^2.5 = 0.9268 |
| Base Score | 165.0 |
| Adjusted Score | 152.9 (-12.1 pts) |

**Reason String:** `"QB Quality (POOR): 38 score"`

### Example 3: RB with Lower Weight

**Austin Ekeler (WAS, RB)** with Average QB:

| Metric | Value |
|--------|-------|
| QB Quality Score | 55 |
| Tier | AVERAGE |
| Multiplier | 1.0^1.0 = 1.0 |
| Base Score | 175.0 |
| Adjusted Score | 175.0 (no change) |

**Reason String:** `"QB Quality (AVERAGE): 55 score"`

---

## Dependencies

### Data Dependencies
- ✅ `passing.pass_yds` - Available in `data/player_data/qb_data.json`
- ✅ `passing.pass_td` - Available in `data/player_data/qb_data.json`
- ✅ `passing.interceptions` - Available in `data/player_data/qb_data.json`
- ✅ `passing.completions` - Available in `data/player_data/qb_data.json`
- ✅ `passing.attempts` - Available in `data/player_data/qb_data.json`
- ✅ `team` - Available in all player JSON files

### Code Dependencies
- 🆕 `QBQualityCalculator` - To be created
- ✅ `ConfigManager` - Existing, needs new methods
- ✅ `PlayerManager` - Existing, for finding team's QB

---

## Risks & Mitigations

### Risk 1: Mid-Season QB Changes
- **Issue:** QB injuries or benchings change team's QB quality mid-season
- **Mitigation:** Recalculate weekly; cache invalidation on data refresh
- **Severity:** Medium (affects several teams per season)

### Risk 2: Backup QB Small Sample
- **Issue:** Backup QB with 2-3 games may not have reliable quality score
- **Mitigation:** MIN_GAMES threshold; default to AVERAGE if insufficient data
- **Severity:** Low (handled by configuration)

### Risk 3: Overlapping with Other Metrics
- **Issue:** Some overlap with Team Quality (M04) which also considers offense
- **Mitigation:** QB Quality is specifically about passing game; weights tuned to complement
- **Severity:** Low (complementary metrics)

---

## Implementation Checklist

**Phase 1: Data Pipeline**
- [ ] `QBQualityCalculator.py` created
- [ ] `calculate_for_player()` method implemented
- [ ] `get_team_qb_quality()` method implemented
- [ ] `_find_starting_qb()` helper created
- [ ] `_calculate_qb_quality()` helper created
- [ ] QB quality caching implemented

**Phase 2: Configuration**
- [ ] `QB_QUALITY_SCORING` section added to `league_config.json`
- [ ] `get_qb_quality_multiplier()` method added to ConfigManager
- [ ] `get_qb_quality_position_weight()` method added to ConfigManager

**Phase 3: Scoring Integration**
- [ ] `_apply_qb_quality_scoring()` method added to `player_scoring.py`
- [ ] Integration point added to `calculate_total_score()`

**Phase 4: Testing**
- [ ] `test_QBQualityCalculator.py` created
- [ ] Test elite QB (80+ score)
- [ ] Test poor QB (<50 score)
- [ ] Test insufficient games (<3 games)
- [ ] Test WR gets proper bonus
- [ ] Test position weights (WR > TE > RB)
- [ ] Test non-pass-catcher returns neutral
- [ ] All tests passing (100% pass rate)

**Phase 5: Documentation**
- [ ] `22_qb_quality_scoring.md` created
- [ ] README.md updated with Step 22
- [ ] Checklist marked complete

**Completion:**
- [ ] Feature request moved to `done/`
- [ ] Committed: "Add QB quality scoring (M12)"

---

**END OF FEATURE REQUEST**
