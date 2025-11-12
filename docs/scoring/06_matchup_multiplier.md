# Matchup Multiplier (Step 6)

## Overview

**Type**: Additive (flat point bonus/penalty, not percentage)
**Effect**: ±3.6 pts (IMPACT_SCALE=108.38, base multiplier ±5%, weight=0.68)
**Base Multipliers**: 0.95x to 1.05x (adjusted by weight exponent before bonus calculation)
**When Applied**: Step 6 of 10-step scoring algorithm
**Purpose**: Adjust scores based on current week's opponent defensive strength (for offensive players) or offensive strength (for DST)

The Matchup Multiplier evaluates this week's specific opponent matchup, rewarding players facing weak defenses and penalizing those facing strong defenses. Unlike other multipliers, this is an **additive bonus** (flat points added/subtracted) rather than a multiplicative percentage adjustment, treating matchup as an environmental opportunity available equally to all players.

**Key Characteristics**:
- **Position-specific opponent defense**: Uses def_vs_qb_rank for QBs, def_vs_rb_rank for RBs, etc.
- **Weekly updates**: Matchup changes each week based on current opponent
- **Additive formula**: Adds/subtracts flat points, not percentage multiplier
- **Environmental factor**: Same matchup quality gives same absolute bonus regardless of player ability
- **Direct opponent ranking**: Uses opponent's defensive ranking directly

**Formula**:
```
matchup_score = (Opponent DEF vs Position Rank)  [for offensive players]
matchup_score = (Opponent Offensive Rank)         [for DST]
Multiplier lookup → Convert to additive bonus
bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE
adjusted_score = player_score + bonus
```

**Implementation**:
- **Matchup Calculation**: `league_helper/util/TeamDataManager.py:217-294`
- **Bonus Application**: `league_helper/util/player_scoring.py:557-569`
- **Data Sources**: `data/teams.csv` (position-specific defense ranks)

---

## Modes Using This Metric

### Add To Roster Mode (Draft Helper)
**Enabled**: No (`matchup=False`)
**Why**: Draft decisions focus on season-long value, not current week matchups. A player's value doesn't change based on this week's opponent - that's only relevant for immediate lineup decisions. Schedule multiplier (step 7) handles future opponent strength for ROS analysis.

**Example**: Two WRs with similar projections:
- WR1: Projected 15 pts, facing def_vs_wr_rank #28 (terrible pass defense)
- WR2: Projected 15 pts, facing def_vs_wr_rank #3 (elite pass defense)
- Matchup bonus helps identify WR1 as the better start this week

### Starter Helper Mode (Roster Optimizer)
**Enabled**: Yes (`matchup=True`)
**Why**: Matchup is THE most important factor for weekly lineup decisions. Same player can have wildly different outcomes based on opponent.

**Example**: Choosing between two RBs for FLEX:
- RB1: vs opponent def_vs_rb_rank #25 (matchup_score = 25, favorable - weak run defense)
- RB2: vs opponent def_vs_rb_rank #2 (matchup_score = 2, tough - elite run defense)
- Matchup bonus heavily favors RB1 facing weaker run defense

### Trade Simulator Mode
**Enabled**: No (`matchup=False`)
**Why**: Trade evaluation focuses on ROS value, not current week matchups. Schedule multiplier (step 7) provides better analysis of future opponent strength across multiple weeks rather than just this week.

**Rationale**: Matchup is a single-week factor (this week's opponent). For trade analysis, it's more important to evaluate the player's schedule over the remaining weeks (schedule multiplier) than just the immediate matchup. Trade Simulator uses schedule=True (in full simulation mode) for multi-week opponent analysis.

---

## How League Helper Gets the Value/Multiplier

### Step 1: Calculate Matchup Score (Rank Differential)

**Method**: `TeamDataManager.get_rank_difference()`
**File**: `league_helper/util/TeamDataManager.py:217-294`

```python
def get_rank_difference(self, player_team: str, position: str) -> int:
    """
    Calculate matchup quality using position-specific defense rankings.

    Formula for Offensive positions:
        matchup_score = (Opponent Position-Specific DEF Rank)

    Formula for Defensive positions:
        matchup_score = (Opponent OFF Rank)

    Args:
        player_team: Team abbreviation (e.g., 'KC', 'BUF')
        position: Player position (QB, RB, WR, TE, K, DST, DEF, D/ST)

    Returns:
        Opponent defense rank integer, or 0 if data unavailable
        Higher rank = weaker defense = favorable matchup
        Lower rank = stronger defense = tough matchup

    Example:
        KC QB vs BUF (DEF vs QB rank #25):
        matchup_score = 25 (favorable - BUF weak vs QB)

        KC RB vs BUF (DEF vs RB rank #5):
        matchup_score = 5 (tough - BUF strong vs RB)

        MIA DST vs NYJ (OFF rank #28):
        matchup_score = 28 (favorable - NYJ weak offense)
    """
    # Check if team data is loaded
    if not self.is_matchup_available():
        return 0

    # Get the opponent team abbreviation
    opponent_abbr = self.get_team_opponent(player_team)
    if opponent_abbr is None:
        return 0

    # Check if player is on defense
    is_defense = position in DEFENSE_POSITIONS

    # Get opponent's relevant rank
    if is_defense:
        # DST wants to face weak offenses (high offensive_rank)
        opponent_rank = self.get_team_offensive_rank(opponent_abbr)
    else:
        # Offensive players want to face weak position-specific defenses
        opponent_rank = self.get_team_defense_vs_position_rank(opponent_abbr, position)

    if opponent_rank is None:
        return 0

    # Return opponent defense rank directly
    # Higher rank = weaker defense = favorable matchup
    # Lower rank = stronger defense = tough matchup
    matchup_score = int(opponent_rank)
    return matchup_score
```

**Key Logic**:
1. **Get opponent**: Lookup current week opponent from schedule
2. **Determine player type**: Offensive (QB/RB/WR/TE/K) vs Defensive (DST)
3. **Get opponent rank**: Use position-specific defense rank (e.g., def_vs_rb_rank) for skill players, offensive_rank for DST
4. **Return rank directly**: Higher rank = weaker defense = favorable matchup (e.g., rank 32 = worst defense)

**Position-Specific Defense Ranks**:
- **QB**: Uses opponent's `def_vs_qb_rank` (how well they defend QBs)
- **RB**: Uses opponent's `def_vs_rb_rank` (how well they defend RBs)
- **WR**: Uses opponent's `def_vs_wr_rank` (how well they defend WRs)
- **TE**: Uses opponent's `def_vs_te_rank` (how well they defend TEs)
- **K**: Uses opponent's `def_vs_k_rank` (how well they defend kickers)
- **DST**: Uses opponent's `offensive_rank` (overall offensive strength)

### Step 2: Convert Matchup Score to Multiplier

**Method**: `ConfigManager.get_matchup_multiplier()`
**File**: `league_helper/util/ConfigManager.py:311-316, 922-1008`

```python
def get_matchup_multiplier(self, matchup_score: int) -> Tuple[float, str]:
    """
    Convert matchup score (opponent defense rank) to multiplier and rating label.

    Args:
        matchup_score: Opponent defense rank (higher rank = weaker defense = better matchup)

    Returns:
        Tuple[float, str]: (multiplier, rating_label)
    """
    return self._get_multiplier(
        self.matchup_scoring,
        matchup_score,
        rising_thresholds=True  # Higher rank = better matchup
    )

def _get_multiplier(self, scoring_dict, val, rising_thresholds=True):
    """
    Generic threshold-based multiplier calculation.

    For MATCHUP (rising_thresholds=True, higher score = better):
    - val >= EXCELLENT threshold → EXCELLENT multiplier
    - val >= GOOD threshold → GOOD multiplier
    - GOOD > val > POOR → neutral (1.0)
    - val <= POOR threshold → POOR multiplier
    - val <= VERY_POOR threshold → VERY_POOR multiplier

    Note: For matchup, multiplier is converted to additive bonus, not applied directly
    """
    thresholds = scoring_dict['THRESHOLDS']
    multipliers = scoring_dict['MULTIPLIERS']
    weight = scoring_dict['WEIGHT']

    # Determine rating level based on thresholds
    if val >= thresholds['EXCELLENT']:
        multiplier, label = multipliers['EXCELLENT'], 'EXCELLENT'
    elif val >= thresholds['GOOD']:
        multiplier, label = multipliers['GOOD'], 'GOOD'
    elif val <= thresholds['VERY_POOR']:
        multiplier, label = multipliers['VERY_POOR'], 'VERY_POOR'
    elif val <= thresholds['POOR']:
        multiplier, label = multipliers['POOR'], 'POOR'
    else:
        multiplier, label = 1.0, 'NEUTRAL'

    # Apply weight exponent
    multiplier = multiplier ** weight
    return multiplier, label
```

### Step 3: Convert Multiplier to Additive Bonus

**Method**: `PlayerScoringCalculator._apply_matchup_multiplier()`
**File**: `league_helper/util/player_scoring.py:557-569`

```python
def _apply_matchup_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply matchup additive bonus (Step 6).

    Matchup is treated as an additive bonus (not multiplicative) because it represents
    environmental opportunity available equally to all players, not ability multipliers.

    Args:
        p: Player to score
        player_score: Current score before matchup adjustment

    Returns:
        Tuple (new_score, reason_string)
    """
    # Apply matchup adjustments to all positions as additive bonuses
    # Matchup score represents opponent defense rank
    # Higher rank = weaker defense = favorable matchup → positive bonus
    # Lower rank = stronger defense = tough matchup → negative penalty
    # All players get same absolute bonus for same matchup (environmental factor)
    multiplier, rating = self.config.get_matchup_multiplier(p.matchup_score)
    impact_scale = self.config.matchup_scoring['IMPACT_SCALE']
    bonus = (impact_scale * multiplier) - impact_scale

    reason = f"Matchup: {rating} ({bonus:+.1f} pts)"
    return player_score + bonus, reason
```

**Additive Bonus Formula**:
```
bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE

Example (IMPACT_SCALE = 108.38):
- EXCELLENT (multiplier 1.05): (108.38 * 1.05) - 108.38 = +5.42 pts
- GOOD (multiplier 1.025): (108.38 * 1.025) - 108.38 = +2.71 pts
- NEUTRAL (multiplier 1.0): (108.38 * 1.0) - 108.38 = 0 pts
- POOR (multiplier 0.975): (108.38 * 0.975) - 108.38 = -2.71 pts
- VERY_POOR (multiplier 0.95): (108.38 * 0.95) - 108.38 = -5.42 pts
```

**Complete Flow**:
```
Player (team="KC", position="QB")
    ↓
Get opponent: BUF (from schedule)
    ↓
Get opponent_def_vs_qb_rank: BUF = 2 (elite pass defense)
    ↓
matchup_score = 2 (tough matchup - low rank = strong defense)
    ↓
get_matchup_multiplier(2) → threshold check
    ↓
2 <= POOR threshold → POOR or VERY_POOR (depending on thresholds)
    ↓
Base multiplier: 0.975 ^ 0.678 = 0.9831 (example)
    ↓
Calculate bonus: (108.38 * 0.9831) - 108.38 = -1.83 pts
    ↓
Adjust score: player_score - 1.83 pts
```

---

## Calculations Involved

### Formula Breakdown

**1. Matchup Score Calculation** (direct opponent defense rank):
```
If position in ['QB', 'RB', 'WR', 'TE', 'K']:
    opponent_rank = opponent.def_vs_{position}_rank
    matchup_score = opponent_rank

Elif position == 'DST':
    opponent_rank = opponent.offensive_rank
    matchup_score = opponent_rank

Interpretation:
- Higher matchup_score = weaker opponent defense = favorable matchup
- Lower matchup_score = stronger opponent defense = tough matchup
- matchup_score ranges from 1 (elite defense) to 32 (weakest defense)
```

**2. Threshold Comparison** (INCREASING direction - higher rank = better matchup):
```
VERY_POOR  = BASE + (1 × STEPS) = 0 + 6 = 6   (ranks 1-6: elite defenses)
POOR       = BASE + (2 × STEPS) = 0 + 12 = 12 (ranks 7-12: above-average defenses)
GOOD       = BASE + (3 × STEPS) = 0 + 18 = 18 (ranks 13-18: below-average defenses)
EXCELLENT  = BASE + (4 × STEPS) = 0 + 24 = 24 (ranks 19-32: weak defenses)

If matchup_score >= 24:
    base_multiplier = EXCELLENT (1.05)  # Facing weak defense
Elif matchup_score >= 18:
    base_multiplier = GOOD (1.025)       # Facing below-average defense
Elif matchup_score <= 6:
    base_multiplier = VERY_POOR (0.95)   # Facing elite defense
Elif matchup_score <= 12:
    base_multiplier = POOR (0.975)       # Facing above-average defense
Else:
    base_multiplier = NEUTRAL (1.0)
```

**3. Weight Exponent Application**:
```
final_multiplier = base_multiplier ^ WEIGHT

Example (WEIGHT=0.678):
- EXCELLENT: 1.05^0.678 = 1.0337
- GOOD: 1.025^0.678 = 1.0168
- NEUTRAL: 1.0^0.678 = 1.0
- POOR: 0.975^0.678 = 0.9831
- VERY_POOR: 0.95^0.678 = 0.9658
```

**4. Convert Multiplier to Additive Bonus**:
```
bonus = (IMPACT_SCALE * final_multiplier) - IMPACT_SCALE

Example (IMPACT_SCALE=108.38):
- EXCELLENT: (108.38 * 1.0337) - 108.38 = +3.65 pts
- GOOD: (108.38 * 1.0168) - 108.38 = +1.82 pts
- NEUTRAL: (108.38 * 1.0) - 108.38 = 0 pts
- POOR: (108.38 * 0.9831) - 108.38 = -1.83 pts
- VERY_POOR: (108.38 * 0.9658) - 108.38 = -3.71 pts
```

**5. Final Score Adjustment**:
```
adjusted_score = player_score + bonus
```

### Example Calculation

**Player**: Patrick Mahomes (QB, KC)
**Current Week**: 10
**Opponent**: BUF
**Config**: WEIGHT=0.678, STEPS=6, IMPACT_SCALE=108.38

**Step 1: Get opponent defense rank**
```
Team: KC QB
Opponent: BUF
  - def_vs_qb_rank = 2 (elite pass defense)
```

**Step 2: Calculate matchup score**
```
matchup_score = opponent_def_vs_qb_rank
matchup_score = 2 (tough matchup - facing elite defense)
```

**Step 3: Determine rating threshold**
```
Config thresholds:
EXCELLENT = >= 24 (ranks 19-32: weak defenses)
GOOD = >= 18 (ranks 13-18: below-average defenses)
NEUTRAL = 7-17 (mid-tier defenses)
POOR = <= 12 (ranks 7-12: above-average defenses)
VERY_POOR = <= 6 (ranks 1-6: elite defenses)

matchup_score = 2 <= 6 → VERY_POOR tier
base_multiplier = 0.95
```

**Step 4: Apply weight exponent**
```
Config: WEIGHT = 0.678
final_multiplier = 0.95 ^ 0.678 = 0.9658
```

**Step 5: Convert to additive bonus**
```
IMPACT_SCALE = 108.38
bonus = (108.38 * 0.9658) - 108.38
bonus = 104.67 - 108.38 = -3.71 pts
```

**Step 6: Apply to score**
```
If player_score = 90.0 (after steps 1-5):
adjusted_score = 90.0 + (-3.71) = 86.29
penalty = -3.71 points
reason = "Matchup: VERY_POOR (-3.7 pts)"
```

**Result**: Patrick Mahomes receives -3.71 point penalty for facing BUF's elite pass defense (rank #2 vs QB).

---

## Data Sources (teams.csv Fields)

### Required Fields

| Field Name | Data Type | Description | Valid Range | Example Values |
|------------|-----------|-------------|-------------|----------------|
| `team` | string | NFL team abbreviation | 32 NFL teams | KC, BUF, PHI, CHI |
| `offensive_rank` | int | Team offensive strength rank | 1-32 (1=best) | 1, 9, 16, 32 |
| `def_vs_qb_rank` | int | Defense vs QB position rank | 1-32 (1=best) | 2, 18, 29 |
| `def_vs_rb_rank` | int | Defense vs RB position rank | 1-32 (1=best) | 5, 13, 27 |
| `def_vs_wr_rank` | int | Defense vs WR position rank | 1-32 (1=best) | 1, 15, 32 |
| `def_vs_te_rank` | int | Defense vs TE position rank | 1-32 (1=best) | 3, 16, 28 |
| `def_vs_k_rank` | int | Defense vs K position rank | 1-32 (1=best) | 7, 14, 23 |

### Field Specifications

**Position-Specific Defense Ranks** (`def_vs_{position}_rank`):
- **Type**: int
- **Source**: Calculated by `player-data-fetcher/espn_client.py` from weekly player performance vs each team
- **Range**: 1-32
  - 1-5: Elite defense vs position (tough matchup)
  - 6-12: Strong defense vs position (difficult matchup)
  - 13-20: Average defense vs position (neutral matchup)
  - 21-27: Weak defense vs position (favorable matchup)
  - 28-32: Terrible defense vs position (excellent matchup)
- **Update frequency**: Updated weekly as player-data-fetcher runs
- **Calculation**: Sum of fantasy points allowed to position across all games, ranked 1-32

**Calculation Method**:
```python
# File: player-data-fetcher/espn_client.py:1029-1120

def _calculate_position_defense_rankings(
    self,
    players: List[ESPNPlayerData],
    schedule: Dict[int, Dict[str, str]],
    current_week: int
) -> Dict[str, Dict[str, int]]:
    """
    Calculate position-specific defense rankings for all teams.

    For each team, calculate how many fantasy points they've allowed
    to each offensive position (QB, RB, WR, TE, K) across all games.

    Args:
        players: List of all players with weekly stats
        schedule: Mapping of {week: {team: opponent}}
        current_week: Current NFL week

    Returns:
        Dict[team, {'def_vs_qb_rank': int, 'def_vs_rb_rank': int, ...}]
    """
    # Track points allowed by each defense to each position
    defense_stats = defaultdict(lambda: defaultdict(float))

    # For each player, accumulate points scored against their opponents
    for player in players:
        if player.position not in ['QB', 'RB', 'WR', 'TE', 'K']:
            continue

        # Get all opponents this team has faced (weeks 1 to current_week-1)
        for week in range(1, current_week):
            if week not in schedule:
                continue

            opponent = schedule[week].get(player.team)
            if opponent is None:
                continue

            # Get player's actual points scored that week
            week_points = getattr(player, f'week_{week}_points', 0.0)
            if week_points is None or week_points == 0.0:
                continue

            # Add to opponent defense's points allowed vs this position
            defense_stats[opponent][player.position] += week_points

    # Rank defenses for each position (lower points allowed = better rank)
    position_rankings = {}
    for position in ['QB', 'RB', 'WR', 'TE', 'K']:
        # Get all teams and their points allowed to this position
        team_points_allowed = [
            (team, stats.get(position, 0.0))
            for team, stats in defense_stats.items()
        ]

        # Sort by points allowed (ascending: fewer points = better defense)
        sorted_teams = sorted(team_points_allowed, key=lambda x: x[1])

        # Assign ranks (1 = best defense vs position)
        position_rankings[position] = {
            team: rank + 1
            for rank, (team, _) in enumerate(sorted_teams)
        }

    # Compile final rankings by team
    team_rankings = {}
    for team in defense_stats.keys():
        team_rankings[team] = {
            'def_vs_qb_rank': position_rankings['QB'].get(team, 16),
            'def_vs_rb_rank': position_rankings['RB'].get(team, 16),
            'def_vs_wr_rank': position_rankings['WR'].get(team, 16),
            'def_vs_te_rank': position_rankings['TE'].get(team, 16),
            'def_vs_k_rank': position_rankings['K'].get(team, 16),
        }

    return team_rankings
```

### Sample teams.csv Data

```csv
team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
KC,9,18,18,13,15,7,7
BUF,3,16,2,24,12,1,6
PHI,10,26,11,16,10,3,29
CHI,6,1,27,17,26,18,10
LAR,8,7,8,1,1,6,22
CIN,16,17,29,32,29,32,25
```

**Interpretation**:
- **BUF**: Elite pass defense (def_vs_qb_rank = 2), but weak vs TEs (def_vs_te_rank = 1) and RBs (def_vs_rb_rank = 24)
  - QBs face tough matchup vs BUF
  - TEs and RBs face favorable matchup vs BUF
- **LAR**: Elite defense vs RBs (def_vs_rb_rank = 1) and WRs (def_vs_wr_rank = 1)
  - Skill position players face tough matchup vs LAR
- **CIN**: Terrible defense vs all positions (ranks 29-32)
  - All offensive players face excellent matchup vs CIN

---

## Examples with Walkthroughs

### Example 1: Excellent Matchup (Jalen Hurts vs CIN)

**Scenario**: Week 10, evaluating QB Jalen Hurts for lineup
**Player Data**:
- Position: QB
- Team: PHI
- Opponent: CIN
- PHI offensive_rank: 10
- CIN def_vs_qb_rank: 29 (terrible pass defense)
- Current Score (after Steps 1-5): 85.0 points

**Step 1: Calculate matchup score**
```
matchup_score = opponent_def_vs_qb_rank
matchup_score = 29 (excellent matchup - facing weak defense)
```

**Step 2: Determine rating threshold**
```
Config thresholds:
EXCELLENT = >= 24 (ranks 19-32: weak defenses)
GOOD = >= 18 (ranks 13-18: below-average defenses)

matchup_score = 29 >= 24 → EXCELLENT tier
base_multiplier = 1.05
```

**Step 3: Apply weight exponent**
```
Config: WEIGHT = 0.678
final_multiplier = 1.05 ^ 0.678 = 1.0337
```

**Step 4: Convert to additive bonus**
```
IMPACT_SCALE = 108.38
bonus = (108.38 * 1.0337) - 108.38
bonus = 112.03 - 108.38 = +3.65 pts
```

**Step 5: Apply to score**
```
adjusted_score = 85.0 + 3.65 = 88.65
bonus = +3.65 points
reason = "Matchup: EXCELLENT (+3.7 pts)"
```

**Result**: Jalen Hurts receives +3.65 point bonus for facing CIN's terrible pass defense (rank #29 vs QB). Huge matchup advantage.

---

### Example 2: Good Matchup (Jahmyr Gibbs vs CHI)

**Scenario**: Week 10, evaluating RB Jahmyr Gibbs
**Player Data**:
- Position: RB
- Team: DET
- Opponent: CHI
- DET offensive_rank: 2
- CHI def_vs_rb_rank: 17 (below average vs RBs)
- Current Score (after Steps 1-5): 80.0 points

**Step 1: Calculate matchup score**
```
matchup_score = opponent_def_vs_rb_rank
matchup_score = 17 (below-average defense - neutral matchup)
```

**Step 2: Determine rating threshold**
```
matchup_score = 17 falls in NEUTRAL range (7-17)
base_multiplier = 1.0
```

**Step 3: Apply weight exponent**
```
final_multiplier = 1.0 ^ 0.678 = 1.0 (neutral)
```

**Step 4: Convert to additive bonus**
```
bonus = (108.38 * 1.0) - 108.38 = 0 pts
```

**Step 5: Apply to score**
```
adjusted_score = 80.0 + 0 = 80.0
bonus = 0 points
reason = "Matchup: NEUTRAL (0 pts)"
```

**Result**: Jahmyr Gibbs receives no matchup bonus or penalty. Facing mid-tier defense (rank 17) results in neutral matchup.

---

### Example 3: Neutral Matchup (DeVonta Smith @ DAL)

**Scenario**: Week 10, evaluating WR DeVonta Smith
**Player Data**:
- Position: WR
- Team: PHI
- Opponent: DAL
- PHI offensive_rank: 10
- DAL def_vs_wr_rank: 32 (worst pass defense)
- Current Score (after Steps 1-5): 72.0 points

**Step 1: Calculate matchup score**
```
matchup_score = opponent_def_vs_wr_rank
matchup_score = 32 (excellent matchup - worst defense in league)
```

**Step 2: Determine rating threshold**
```
matchup_score = 32 >= 24 → EXCELLENT tier
base_multiplier = 1.05
```

**Step 3: Apply weight exponent**
```
final_multiplier = 1.05 ^ 0.678 = 1.0337
```

**Step 4: Convert to additive bonus**
```
bonus = (108.38 * 1.0337) - 108.38 = +3.65 pts
```

**Step 5: Apply to score**
```
adjusted_score = 72.0 + 3.65 = 75.65
bonus = +3.65 points
reason = "Matchup: EXCELLENT (+3.7 pts)"
```

**Result**: DeVonta Smith receives +3.65 point bonus for facing DAL's worst-in-league WR defense (rank #32). Despite PHI's mediocre offense (#10), the matchup is still excellent.

---

### Example 4: Tough Matchup (Patrick Mahomes vs BUF)

**Scenario**: Week 10, evaluating QB Patrick Mahomes
**Player Data**:
- Position: QB
- Team: KC
- Opponent: BUF
- KC offensive_rank: 9
- BUF def_vs_qb_rank: 2 (elite pass defense)
- Current Score (after Steps 1-5): 90.0 points

**Step 1: Calculate matchup score**
```
matchup_score = opponent_def_vs_qb_rank - team_offensive_rank
matchup_score = 2 - 9 = -7 (very tough matchup)
```

**Step 2: Determine rating threshold**
```
Config thresholds:
VERY_POOR = -6.89

-7 <= -6.89 → VERY_POOR tier
base_multiplier = 0.95
```

**Step 3: Apply weight exponent**
```
Config: WEIGHT = 0.678
final_multiplier = 0.95 ^ 0.678 = 0.9658
```

**Step 4: Convert to additive bonus**
```
IMPACT_SCALE = 108.38
bonus = (108.38 * 0.9658) - 108.38
bonus = 104.67 - 108.38 = -3.71 pts
```

**Step 5: Apply to score**
```
adjusted_score = 90.0 + (-3.71) = 86.29
penalty = -3.71 points
reason = "Matchup: VERY_POOR (-3.7 pts)"
```

**Result**: Patrick Mahomes receives -3.71 point penalty for facing BUF's elite pass defense (rank #2 vs QB). Tough divisional matchup.

---

### Example 5: DST Player (CHI DST vs TEN)

**Scenario**: Week 10, evaluating Chicago Bears D/ST
**Player Data**:
- Position: DST (defensive player)
- Team: CHI
- Opponent: TEN
- CHI defensive_rank: 1 (best defense)
- TEN offensive_rank: 32 (worst offense)
- Current Score (after Steps 1-5): 50.0 points

**Step 1: Calculate matchup score**
```
Position: DST (uses opponent offensive rank directly)
matchup_score = opponent_offensive_rank
matchup_score = 32 (dream matchup - worst offense in league)
```

**Step 2: Determine rating threshold**
```
matchup_score = 32 >= 24 → EXCELLENT tier
base_multiplier = 1.05
```

**Step 3: Apply weight exponent**
```
final_multiplier = 1.05 ^ 0.678 = 1.0337
```

**Step 4: Convert to additive bonus**
```
bonus = (108.38 * 1.0337) - 108.38 = +3.65 pts
```

**Step 5: Apply to score**
```
adjusted_score = 50.0 + 3.65 = 53.65
bonus = +3.65 points
reason = "Matchup: EXCELLENT (+3.7 pts)"
```

**Result**: CHI D/ST receives +3.65 point bonus. Elite defense (#1) facing worst offense (#32) = maximum matchup advantage for DST.

---

### Example 6: Running Back vs Elite Run Defense

**Scenario**: Week 10, evaluating RB facing LAR
**Player Data**:
- Position: RB
- Team: SF
- Opponent: LAR
- SF offensive_rank: 23
- LAR def_vs_rb_rank: 1 (best run defense)
- Current Score (after Steps 1-5): 70.0 points

**Step 1: Calculate matchup score**
```
matchup_score = opponent_def_vs_rb_rank
matchup_score = 1 (nightmare matchup - elite defense #1)
```

**Step 2: Determine rating threshold**
```
matchup_score = 1 <= 6 → VERY_POOR tier
base_multiplier = 0.95
```

**Step 3: Apply weight exponent**
```
final_multiplier = 0.95 ^ 0.678 = 0.9658
```

**Step 4: Convert to additive bonus**
```
bonus = (108.38 * 0.9658) - 108.38 = -3.71 pts
```

**Step 5: Apply to score**
```
adjusted_score = 70.0 + (-3.71) = 66.29
penalty = -3.71 points
reason = "Matchup: VERY_POOR (-3.7 pts)"
```

**Result**: SF RB receives -3.71 point penalty. Weak offense (#23) facing elite run defense (#1 vs RB) = worst possible matchup for RB.

---

## Configuration Reference

### Current Configuration (league_config.json)

```json
{
  "MATCHUP_SCORING": {
    "IMPACT_SCALE": 108.37629512182852,
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "INCREASING",
      "STEPS": 6
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 0.6778481670093686
  }
}
```

### Configuration Fields

| Field | Type | Description | Current Value |
|-------|------|-------------|---------------|
| `IMPACT_SCALE` | float | Scaling factor for additive bonus calculation | 108.38 |
| `THRESHOLDS.BASE_POSITION` | int | Starting point for threshold calculation | 0 |
| `THRESHOLDS.DIRECTION` | string | Threshold direction logic | "INCREASING" |
| `THRESHOLDS.STEPS` | int | Step size for threshold boundaries | 6 |
| `MULTIPLIERS.VERY_POOR` | float | Multiplier for very poor matchup | 0.95 |
| `MULTIPLIERS.POOR` | float | Multiplier for poor matchup | 0.975 |
| `MULTIPLIERS.GOOD` | float | Multiplier for good matchup | 1.025 |
| `MULTIPLIERS.EXCELLENT` | float | Multiplier for excellent matchup | 1.05 |
| `WEIGHT` | float | Exponent for multiplier adjustment | 0.678 |

### Threshold Calculation

**Direction**: `INCREASING` (higher opponent defense rank = better matchup)

**Formula**:
```
BASE = 0 (starting position)
STEP = 6 (tier size ~6 teams per tier)

VERY_POOR = BASE + (1 × STEP) = 0 + 6 = 6  (ranks <= 6)
POOR = BASE + (2 × STEP) = 0 + 12 = 12      (ranks 7-12)
GOOD = BASE + (3 × STEP) = 0 + 18 = 18      (ranks 13-18)
EXCELLENT = BASE + (4 × STEP) = 0 + 24 = 24 (ranks >= 19)
```

**Calculated Thresholds**:
- EXCELLENT: Rank 19-32 (facing bottom-tier defenses - favorable matchup)
- GOOD: Rank 13-18 (facing below-average defenses)
- NEUTRAL: Rank 7-12 (facing average defenses)
- POOR: Rank 7 or below (facing above-average defenses)
- VERY_POOR: Rank 1-6 (facing elite defenses - tough matchup)

### Weight Exponent Impact

**Current Weight**: 0.678

**Multiplier Transformations**:

| Rating | Base Multiplier | Weight Applied | Final Multiplier | Additive Bonus (IMPACT_SCALE=108.38) |
|--------|----------------|----------------|------------------|--------------------------------------|
| EXCELLENT | 1.05 | 1.05^0.678 = 1.0337 | +3.37% | +3.65 pts |
| GOOD | 1.025 | 1.025^0.678 = 1.0168 | +1.68% | +1.82 pts |
| NEUTRAL | 1.0 | 1.0^0.678 = 1.0 | 0% | 0 pts |
| POOR | 0.975 | 0.975^0.678 = 0.9831 | -1.69% | -1.83 pts |
| VERY_POOR | 0.95 | 0.95^0.678 = 0.9658 | -3.42% | -3.71 pts |

**Interpretation**: Moderate weight (0.678) provides meaningful but not extreme matchup adjustments (±1-4 points typical range).

### Impact Scale Effect

**Current IMPACT_SCALE**: 108.38

**Purpose**: Converts percentage-based multipliers to flat point bonuses

**Formula**: `bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE`

**Effect on Point Ranges**:
- Higher IMPACT_SCALE = larger absolute point bonuses/penalties
- Lower IMPACT_SCALE = smaller absolute point bonuses/penalties

**Examples**:
- IMPACT_SCALE = 200: EXCELLENT = +6.74 pts, VERY_POOR = -6.84 pts (larger swings)
- IMPACT_SCALE = 50: EXCELLENT = +1.69 pts, VERY_POOR = -1.71 pts (smaller swings)

### Configuration Tuning Guide

**Increasing Matchup Impact**:
- Increase `IMPACT_SCALE` (e.g., 150, 200) → larger absolute point bonuses
- Increase `WEIGHT` (e.g., 1.0, 1.5) → amplifies multiplier differences
- Increase base multipliers (e.g., EXCELLENT=1.10) → larger percentage swings
- Decrease `STEPS` (e.g., 5.0, 4.0) → easier to reach extreme tiers

**Decreasing Matchup Impact**:
- Decrease `IMPACT_SCALE` (e.g., 75, 50) → smaller absolute point bonuses
- Decrease `WEIGHT` (e.g., 0.3, 0.1) → dampens multiplier differences
- Decrease base multipliers (e.g., EXCELLENT=1.02) → smaller percentage swings
- Increase `STEPS` (e.g., 10.0, 15.0) → harder to reach extreme tiers

**Changing Tier Boundaries**:
- Lower `STEPS` → More matchups reach EXCELLENT/POOR (e.g., diff ≥ ±5)
- Higher `STEPS` → Fewer matchups reach extremes (stricter requirements)

---

## See Also

### Related Metrics
- **[04_team_quality_multiplier.md](04_team_quality_multiplier.md)** - Overall team strength (season-long context)
- **[07_schedule_multiplier.md](07_schedule_multiplier.md)** - Future opponent difficulty (ROS matchups)
- **[03_player_rating_multiplier.md](03_player_rating_multiplier.md)** - Player-level expert consensus

### Implementation Files
- **`league_helper/util/player_scoring.py:557-569`** - Matchup bonus application
- **`league_helper/util/ConfigManager.py:311-316, 922-1008`** - Multiplier threshold logic
- **`league_helper/util/TeamDataManager.py:217-294`** - Matchup score calculation (rank differential)
- **`league_helper/util/PlayerManager.py:219-222`** - Matchup score assignment to players
- **`player-data-fetcher/espn_client.py:1029-1120`** - Position-specific defense rankings calculation

### Configuration
- **`data/league_config.json`** - Matchup scoring parameters (MATCHUP_SCORING section)
- **`data/teams.csv`** - Position-specific defense ranks (def_vs_qb_rank, def_vs_rb_rank, etc.)

### Testing
- **`tests/league_helper/util/test_player_scoring.py`** - Matchup multiplier tests
- **`tests/league_helper/util/test_ConfigManager.py`** - Threshold and multiplier configuration tests
- **`tests/league_helper/util/test_TeamDataManager.py`** - Opponent defense rank calculation tests

### Documentation
- **[README.md](README.md)** - Scoring algorithm overview and metric summary
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture and data flow
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines and coding standards

---

**Last Updated**: November 5, 2025
**Current NFL Week**: 10
**Documentation Version**: 1.0
**Code Version**: Week 10, 2025 NFL Season
