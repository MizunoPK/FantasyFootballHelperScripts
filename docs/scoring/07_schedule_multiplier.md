# Schedule Multiplier (Step 7)

> **Note**: This documentation references the old `teams.csv` format. Team data is now stored in `data/team_data/` folder with per-team CSV files. Rankings are calculated on-the-fly using a configurable rolling window (MIN_WEEKS). See `TeamDataManager.py` for current implementation.

## Overview

**Type**: Additive bonus (point adjustment)
**Effect**: 0 pts (disabled, weight=0.0)
**Theoretical Effect**: ±4.0 pts if enabled (IMPACT_SCALE=80.0, base multiplier ±5%)
**When Applied**: Step 7 of 10-step scoring algorithm
**Purpose**: Reward players facing easier remaining schedules, penalize those facing tougher schedules

The Schedule Multiplier evaluates the strength of a player's remaining opponents for the rest of the season. Unlike matchup multiplier (which looks at the current week's opponent), schedule multiplier provides a longer-term view by analyzing all future games. Players facing weaker defenses receive a bonus, while those facing stronger defenses receive a penalty.

**Key Characteristics**:
- **Forward-looking**: Only analyzes weeks > CURRENT_NFL_WEEK (future games)
- **Position-specific**: Uses position-specific defense rankings (def_vs_qb_rank, def_vs_rb_rank, etc.)
- **Average-based**: Averages defense ranks across all remaining opponents
- **Minimum requirement**: Requires at least 2 future games for calculation
- **Additive scoring**: Bonus added to score, not multiplicative (represents opportunity, not ability)
- **Currently disabled**: Weight set to 0 in config, but logic fully documented

**Formula**:
```
Future opponents = [opponent_1, opponent_2, ..., opponent_N] for weeks > CURRENT_NFL_WEEK
Defense ranks = [rank(opp_1, position), rank(opp_2, position), ..., rank(opp_N, position)]
Schedule value = average(defense ranks)  # 1-32, higher = easier schedule
Multiplier = threshold_lookup(schedule_value) → apply weight exponent
Bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE
Adjusted score = player_score + bonus
```

**Implementation**: `league_helper/util/player_scoring.py:303-354, 571-607`

---

## Modes Using This Metric

### Add To Roster Mode (Draft Helper)
**Enabled**: No (`schedule=False`)
**Why**: Draft decisions prioritize expert consensus (player_rating) and team quality rather than granular schedule analysis. Schedule multiplier requires significant processing for all future weeks. ROS projections already incorporate expected performance across all matchups.

**Rationale**: While schedule analysis could help identify favorable matchups, the complexity-to-value ratio is low for draft decisions. Player rating and team quality multipliers provide sufficient differentiation. Schedule multiplier is more valuable for trade analysis where you're comparing specific players' remaining schedules in detail.

### Starter Helper Mode (Roster Optimizer)
**Enabled**: No (`schedule=False`)
**Why**: Weekly lineup decisions focus on immediate matchup (current week), not rest-of-season schedule. Matchup multiplier (step 6) handles current week opponent analysis.

**Rationale**:
- Schedule multiplier provides strategic value (who to roster for playoffs)
- Lineup optimizer needs tactical value (who to start this week)
- Using both schedule and matchup would double-count opponent strength
- Matchup multiplier alone is more appropriate for weekly decisions

### Trade Simulator Mode
**Enabled**: Varies by configuration
- **Manual Visualizer** (line 86): No (`schedule=False`)
- **Full Simulation** (line 89): Yes (`schedule=True`)

**Why Full Simulation enables it**: Trade evaluation in full simulation mode benefits from detailed ROS schedule analysis. Comparing two players' remaining matchups helps identify buy-low/sell-high opportunities where schedule strength differs significantly from ROS projections.

**Why Manual Visualizer disables it**: For quick trade comparisons, schedule adds complexity without much benefit. Manual mode relies on player_rating and team_quality for ROS valuation, which is faster and simpler.

**Example** (Full Simulation): Evaluating RB trade in week 10:
- Giving: RB with weeks 11-17 schedule avg rank 15 (neutral)
- Receiving: RB with weeks 11-17 schedule avg rank 28 (favorable)
- Schedule multiplier helps quantify the additional value from easier upcoming matchups

---

## How League Helper Gets the Value/Multiplier

### Step 1: Calculate Schedule Value

**Method**: `PlayerScoringCalculator._calculate_schedule_value()`
**File**: `league_helper/util/player_scoring.py:303-354`

```python
def _calculate_schedule_value(self, player: FantasyPlayer) -> Optional[float]:
    """
    Calculate schedule strength value based on future opponents.

    Minimum 2 future games required for calculation.
    End of season returns None.

    Args:
        player: Player to calculate schedule for

    Returns:
        Average defense rank of future opponents (1-32)
        Higher rank = easier schedule (facing worse defenses)
        None if insufficient future games (< 2)
    """
    # Get future opponents
    future_opponents = self.season_schedule_manager.get_future_opponents(
        player.team,
        self.current_nfl_week
    )

    if not future_opponents:
        self.logger.debug(f"{player.name}: No future games (end of season)")
        return None

    # Get position-specific defense ranks for each opponent
    defense_ranks = []
    for opponent in future_opponents:
        rank = self.team_data_manager.get_team_defense_vs_position_rank(
            opponent,
            player.position
        )
        if rank is not None:
            defense_ranks.append(rank)

    # Require minimum 2 future games
    if len(defense_ranks) < 2:
        self.logger.debug(
            f"{player.name}: Insufficient future games ({len(defense_ranks)}) "
            f"for schedule calculation (minimum 2 required)"
        )
        return None

    # Calculate average defense rank
    avg_rank = sum(defense_ranks) / len(defense_ranks)

    self.logger.debug(
        f"{player.name} schedule: {len(defense_ranks)} future games, "
        f"avg defense rank: {avg_rank:.1f}"
    )

    return avg_rank
```

**Key Logic**:
1. **Get future opponents**: Use SeasonScheduleManager to get opponents for weeks > CURRENT_NFL_WEEK
2. **Position-specific ranks**: Look up each opponent's defense rank against player's position
3. **Skip None values**: Exclude opponents with missing defense rank data
4. **Minimum requirement**: Need at least 2 future games with valid defense ranks
5. **Average calculation**: Simple mean of all future opponent defense ranks
6. **Return value**: 1-32 (lower = tougher schedule, higher = easier schedule)

### Step 2: Convert Schedule Value to Multiplier

**Method**: `ConfigManager.get_schedule_multiplier()`
**File**: `league_helper/util/ConfigManager.py:309-324`

```python
def get_schedule_multiplier(self, schedule_value) -> Tuple[float, str]:
    """
    Get schedule multiplier based on average future opponent defense rank.

    Args:
        schedule_value: Average defense rank of future opponents (1-32)
                       Higher rank = worse defenses = easier schedule = higher multiplier

    Returns:
        Tuple (multiplier, rating_label)
    """
    return self._get_multiplier(
        self.schedule_scoring,
        schedule_value,
        rising_thresholds=True  # Higher rank = better schedule
    )
```

Uses standard `_get_multiplier()` logic (same as other metrics):
1. Compare schedule_value to thresholds (EXCELLENT, GOOD, POOR, VERY_POOR)
2. Assign base multiplier based on threshold tier
3. Apply weight exponent: `final_multiplier = base_multiplier ^ weight`

**Threshold Direction**: `rising_thresholds=True`
- Higher average defense rank = easier schedule = EXCELLENT/GOOD multiplier
- Lower average defense rank = tougher schedule = POOR/VERY_POOR multiplier

### Step 3: Calculate Additive Bonus

**Method**: `PlayerScoringCalculator._apply_schedule_multiplier()`
**File**: `league_helper/util/player_scoring.py:571-607`

```python
def _apply_schedule_multiplier(self, player: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply schedule strength additive bonus based on future opponent difficulty.

    Schedule bonuses are additive (not multiplicative) because schedule represents
    environmental opportunity available equally to all players, not ability multipliers.

    Args:
        player: Player to score
        player_score: Current score before schedule adjustment

    Returns:
        Tuple (new_score, reason_string)
    """
    # Calculate schedule value
    schedule_value = self._calculate_schedule_value(player)

    if schedule_value is None:
        return player_score, ""

    # Get multiplier and rating
    multiplier, rating = self.config.get_schedule_multiplier(schedule_value)

    # Calculate additive bonus
    impact_scale = self.config.schedule_scoring['IMPACT_SCALE']
    bonus = (impact_scale * multiplier) - impact_scale

    # Apply bonus
    new_score = player_score + bonus
    reason = f"Schedule: {rating} (avg opp def rank: {schedule_value:.1f}, {bonus:+.1f} pts)"

    self.logger.debug(
        f"{player.name}: Schedule bonus {bonus:+.1f} pts "
        f"({schedule_value:.1f} avg rank) -> {player_score:.2f} to {new_score:.2f}"
    )

    return new_score, reason
```

**Key Points**:
- **Additive formula**: `bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE`
- **Why additive?**: Schedule represents external opportunity, not player ability
  - Matchup/schedule are environmental factors (same for all team players)
  - Player rating/performance are intrinsic factors (player-specific ability)
  - Additive approach prevents compounding environmental factors with ability factors
- **IMPACT_SCALE**: Determines magnitude of bonus (currently 80.0)
- **Bonus range**: With multipliers 0.95-1.05 and IMPACT_SCALE=80:
  - EXCELLENT (1.05): bonus = (80 * 1.05) - 80 = +4.0 pts
  - GOOD (1.025): bonus = (80 * 1.025) - 80 = +2.0 pts
  - NEUTRAL (1.0): bonus = (80 * 1.0) - 80 = 0 pts
  - POOR (0.975): bonus = (80 * 0.975) - 80 = -2.0 pts
  - VERY_POOR (0.95): bonus = (80 * 0.95) - 80 = -4.0 pts

**Complete Flow**:
```
Player: Saquon Barkley (RB, PHI)
Current week: 9
Future opponents (weeks 10-17): WAS, LAR, BAL, CAR, PIT, WSH, DAL, NYG
    ↓
_calculate_schedule_value() → gets defense ranks
    ↓
Defense vs RB ranks: [19, 1, 27, 26, 5, 19, 30, 31]
    ↓
Average rank = (19 + 1 + 27 + 26 + 5 + 19 + 30 + 31) / 8 = 19.75
    ↓
get_schedule_multiplier(19.75) → compare to thresholds
    ↓
Thresholds (INCREASING direction): VP=8, P=16, G=24, E=32
19.75 is between POOR (16) and GOOD (24) → NEUTRAL zone
Base multiplier = 1.0
    ↓
Apply weight: 1.0 ^ 0.0 = 1.0 (weight disabled)
    ↓
Calculate bonus: (80.0 * 1.0) - 80.0 = 0.0
    ↓
new_score = player_score + 0.0
```

---

## Calculations Involved

### Formula Breakdown

**Future Opponents Collection**:
```
For week W in [CURRENT_NFL_WEEK + 1, 17]:
    opponent = season_schedule.get_opponent(player.team, W)
    If opponent is not None (not bye week):
        future_opponents.append(opponent)
```

**Defense Rank Lookup** (per opponent):
```
For each opponent O in future_opponents:
    rank = team_data.get_defense_vs_position_rank(O, player.position)
    If rank is not None:
        defense_ranks.append(rank)
```

**Average Calculation**:
```
If len(defense_ranks) >= 2:
    schedule_value = sum(defense_ranks) / len(defense_ranks)
Else:
    schedule_value = None (insufficient data)
```

**Threshold Comparison** (INCREASING direction):
```
If schedule_value >= EXCELLENT_threshold:
    base_multiplier = EXCELLENT (1.05)
Elif schedule_value >= GOOD_threshold:
    base_multiplier = GOOD (1.025)
Elif schedule_value <= VERY_POOR_threshold:
    base_multiplier = VERY_POOR (0.95)
Elif schedule_value <= POOR_threshold:
    base_multiplier = POOR (0.975)
Else:
    base_multiplier = NEUTRAL (1.0)
```

**Weight Application**:
```
final_multiplier = base_multiplier ^ WEIGHT
```

**Additive Bonus**:
```
bonus = (IMPACT_SCALE * final_multiplier) - IMPACT_SCALE
adjusted_score = player_score + bonus
```

### Example Calculation

**Player**: Tyreek Hill (WR, MIA)
**Current Week**: 9
**Current Score**: 95.0 points (after steps 1-6)

**Step 1: Get future opponents** (weeks 10-17)

```python
future_opponents = season_schedule_manager.get_future_opponents('MIA', 9)
# Returns: ['LAR', 'LV', 'NE', 'GB', 'NYJ', 'HOU', 'SF', 'CLE']
```

**Step 2: Get defense ranks vs WR** (from data/teams.csv)

| Week | Opponent | Defense vs WR Rank |
|------|----------|-------------------|
| 10 | LAR | 1 (best vs WR) |
| 11 | LV | 22 |
| 12 | NE | 18 |
| 13 | GB | 4 |
| 14 | NYJ | 11 |
| 15 | HOU | 3 |
| 16 | SF | 25 |
| 17 | CLE | 16 |

**Step 3: Calculate average rank**
```
defense_ranks = [1, 22, 18, 4, 11, 3, 25, 16]
schedule_value = (1 + 22 + 18 + 4 + 11 + 3 + 25 + 16) / 8 = 100 / 8 = 12.5
```

**Step 4: Determine rating** (current thresholds)
```
Config thresholds (BASE=0, DIRECTION=INCREASING, STEPS=8):
VERY_POOR = 0 + 8 = 8
POOR = 0 + (2*8) = 16
GOOD = 0 + (3*8) = 24
EXCELLENT = 0 + (4*8) = 32

schedule_value = 12.5
12.5 is between VERY_POOR (8) and POOR (16) → POOR tier
base_multiplier = 0.975
```

**Step 5: Apply weight**
```
WEIGHT = 0.0
final_multiplier = 0.975 ^ 0.0 = 1.0 (weight disabled)
```

**Step 6: Calculate bonus**
```
IMPACT_SCALE = 80.0
bonus = (80.0 * 1.0) - 80.0 = 0.0
```

**Step 7: Apply to score**
```
adjusted_score = 95.0 + 0.0 = 95.0
reason = "Schedule: POOR (avg opp def rank: 12.5, +0.0 pts)"
```

**Result**: Tyreek Hill's schedule rated POOR (facing strong defenses), but weight=0 means no actual penalty applied. Score remains 95.0 points.

### Example with Enabled Weight (Hypothetical)

**Same player** (Tyreek Hill), but with weight enabled:

**Configuration**:
```json
{
  "SCHEDULE_SCORING": {
    "IMPACT_SCALE": 80.0,
    "WEIGHT": 0.5
  }
}
```

**Calculation** (steps 1-4 same as above):
```
schedule_value = 12.5 (POOR tier)
base_multiplier = 0.975
```

**Step 5: Apply weight**
```
WEIGHT = 0.5
final_multiplier = 0.975 ^ 0.5 = 0.9874
```

**Step 6: Calculate bonus**
```
bonus = (80.0 * 0.9874) - 80.0 = 78.99 - 80.0 = -1.01
```

**Step 7: Apply to score**
```
adjusted_score = 95.0 + (-1.01) = 93.99
penalty = -1.01 pts
reason = "Schedule: POOR (avg opp def rank: 12.5, -1.0 pts)"
```

**Result**: With weight enabled, Tyreek Hill receives -1.01 point penalty for tough remaining schedule (averaging 12.5 rank = strong defenses).

### Example: Favorable Schedule

**Player**: Garrett Wilson (WR, NYJ)
**Current Week**: 9
**Current Score**: 78.0 points

**Step 1: Future opponents**
```
Weeks 10-17: ['ARI', 'IND', 'SEA', 'MIA', 'JAX', 'LAR', 'BUF', 'MIA']
```

**Step 2: Defense vs WR ranks**

| Week | Opponent | Defense vs WR Rank |
|------|----------|-------------------|
| 10 | ARI | 6 |
| 11 | IND | 27 |
| 12 | SEA | 7 |
| 13 | MIA | 9 |
| 14 | JAX | 19 |
| 15 | LAR | 1 |
| 16 | BUF | 12 |
| 17 | MIA | 9 |

**Step 3: Calculate average**
```
defense_ranks = [6, 27, 7, 9, 19, 1, 12, 9]
schedule_value = (6 + 27 + 7 + 9 + 19 + 1 + 12 + 9) / 8 = 90 / 8 = 11.25
```

**Step 4: Rating** (current config)
```
Thresholds: VP=8, P=16, G=24, E=32
11.25 is between VERY_POOR (8) and POOR (16) → POOR tier
base_multiplier = 0.975
```

**Current config (weight=0)**:
```
bonus = 0.0
adjusted_score = 78.0
```

**If weight were 0.5**:
```
final_multiplier = 0.975 ^ 0.5 = 0.9874
bonus = (80.0 * 0.9874) - 80.0 = -1.01
adjusted_score = 78.0 - 1.01 = 76.99
```

**Note**: Even though ranks include some high values (27, 19), the average is pulled down by facing elite defenses (ranks 1, 6, 7), resulting in tough overall schedule.

### Example: End of Season (No Future Games)

**Player**: Any player
**Current Week**: 17 (final week)
**Future games**: 0 (season over)

**Calculation**:
```python
future_opponents = season_schedule_manager.get_future_opponents(player.team, 17)
# Returns: [] (empty list, no future games)

if not future_opponents:
    return None

_calculate_schedule_value() returns None
```

**Result**:
```
schedule_value = None
_apply_schedule_multiplier() returns (player_score, "")
No adjustment applied (expected at end of season)
```

---

## Data Sources

### Season Schedule (season_schedule.csv)

**File**: `data/season_schedule.csv`
**Purpose**: Maps each team's opponent for each week of the season

**Structure**:
```csv
week,team,opponent
1,KC,LAC
1,LAC,KC
1,PHI,DAL
2,KC,CIN
2,PHI,MIN
...
17,KC,DEN
17,PHI,NYG
```

**Field Specifications**:

| Field | Type | Description | Valid Range | Example |
|-------|------|-------------|-------------|---------|
| `week` | int | NFL week number | 1 - 17 | 1, 9, 17 |
| `team` | string | Team abbreviation | 32 NFL teams | KC, PHI, BAL |
| `opponent` | string (nullable) | Opponent abbreviation | 32 NFL teams or None | LAC, DAL, None (bye) |

**Special Cases**:
- **Bye weeks**: opponent field is None/empty (team has no game that week)
- **Bidirectional**: Each game appears twice (once for each team)
  - Example: KC vs LAC appears as both (KC, LAC) and (LAC, KC)

**Update Frequency**: Static (loaded at season start, does not change)

### Team Defense Rankings (teams.csv)

**File**: `data/teams.csv`
**Purpose**: Position-specific defense rankings for matchup analysis

**Structure**:
```csv
team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
KC,9,18,18,13,15,7,7
PHI,10,26,11,16,10,3,29
BAL,13,28,17,27,20,9,23
...
```

**Field Specifications**:

| Field | Type | Description | Valid Range | Used For |
|-------|------|-------------|-------------|----------|
| `team` | string | Team abbreviation | 32 NFL teams | Team lookup key |
| `offensive_rank` | int | Overall offensive rank | 1 - 32 | Team quality multiplier |
| `defensive_rank` | int | Overall defensive rank | 1 - 32 | DST position default |
| `def_vs_qb_rank` | int | Defense rank vs QB | 1 - 32 | QB schedule calculation |
| `def_vs_rb_rank` | int | Defense rank vs RB | 1 - 32 | RB schedule calculation |
| `def_vs_wr_rank` | int | Defense rank vs WR | 1 - 32 | WR schedule calculation |
| `def_vs_te_rank` | int | Defense rank vs TE | 1 - 32 | TE schedule calculation |
| `def_vs_k_rank` | int | Defense rank vs K | 1 - 32 | K schedule calculation |

**Rank Interpretation**:
- **1 = best defense** against that position (hardest matchup)
- **32 = worst defense** against that position (easiest matchup)
- **Lower rank = stronger defense = tougher schedule**
- **Higher rank = weaker defense = easier schedule**

**Update Frequency**: Weekly (updated by nfl-scores-fetcher after games complete)

### Player Team Field (players.csv)

**Field**: `team`
**Purpose**: Links player to their NFL team for schedule lookup

| Field | Type | Description | Valid Values | Example |
|-------|------|-------------|--------------|---------|
| `team` | string | Player's NFL team | 32 NFL teams | KC, PHI, MIA |

**Mapping Flow**:
```
Player (team="PHI")
    → SeasonScheduleManager.get_future_opponents("PHI", 9)
    → Returns: ["WAS", "LAR", "BAL", ...]
    → TeamDataManager.get_team_defense_vs_position_rank("WAS", "RB")
    → Returns: 19 (WSH ranked 19th vs RB)
```

---

## How player-data-fetcher Populates Data

### Season Schedule Data

**Source**: **NOT** provided by ESPN API
**Maintenance**: Manual or external data source

**Current Implementation**:
- `data/season_schedule.csv` is maintained separately
- Updated at beginning of NFL season when schedule is released
- Static for entire season (schedule doesn't change)

**File Format**:
```csv
week,team,opponent
1,KC,LAC
1,LAC,KC
...
```

**Future Enhancement**:
Could be automated by fetching from:
- NFL.com schedule API
- ESPN schedule endpoint
- External sports data provider

### Team Defense Rankings

**Script**: `nfl-scores-fetcher/NFLScoresFetcher.py`
**Method**: `update_team_rankings()`
**Frequency**: Weekly (after games complete)

**Data Sources**:
1. **Offensive/Defensive Ranks**: Calculated from NFL game data
2. **Position-Specific Ranks**: Derived from fantasy points allowed by position

**Process**:
```python
# File: nfl-scores-fetcher/NFLScoresFetcher.py
def update_team_rankings(self):
    """
    Update team rankings based on recent performance.

    Rankings include:
    - Overall offensive rank (total yards/points scored)
    - Overall defensive rank (total yards/points allowed)
    - Position-specific defense ranks (fantasy points allowed vs QB/RB/WR/TE/K)
    """

    # Fetch game results and team stats
    team_stats = self.fetch_team_stats()

    # Calculate offensive rankings (1-32)
    offensive_ranks = self.rank_teams_by_offense(team_stats)

    # Calculate defensive rankings (1-32)
    defensive_ranks = self.rank_teams_by_defense(team_stats)

    # Calculate position-specific defense rankings
    def_vs_qb_ranks = self.rank_teams_by_points_allowed('QB')
    def_vs_rb_ranks = self.rank_teams_by_points_allowed('RB')
    def_vs_wr_ranks = self.rank_teams_by_points_allowed('WR')
    def_vs_te_ranks = self.rank_teams_by_points_allowed('TE')
    def_vs_k_ranks = self.rank_teams_by_points_allowed('K')

    # Write to teams.csv
    self.write_team_rankings_csv(
        offensive_ranks,
        defensive_ranks,
        def_vs_qb_ranks,
        def_vs_rb_ranks,
        def_vs_wr_ranks,
        def_vs_te_ranks,
        def_vs_k_ranks
    )
```

**Ranking Methodology**:
```
For each position (QB, RB, WR, TE, K):
    1. Calculate total fantasy points allowed by each defense vs that position
    2. Sort teams by points allowed (ascending)
    3. Assign ranks 1-32:
       - Rank 1 = fewest points allowed (best defense vs position)
       - Rank 32 = most points allowed (worst defense vs position)
```

**Example Ranking Process** (RB defense):
```
Calculate points allowed to RBs:
PIT: 145.2 pts allowed → Rank 1 (best)
CLE: 158.7 pts allowed → Rank 2
...
CIN: 287.5 pts allowed → Rank 32 (worst)

Write to teams.csv:
PIT,12,2,25,5,30,26,21  (def_vs_rb_rank = 5)
CIN,16,17,29,32,29,32,25  (def_vs_rb_rank = 32)
```

### Player Team Assignment

**Script**: `player-data-fetcher/espn_client.py`
**Method**: `fetch_players()`

**ESPN API Extraction**:
```python
# File: player-data-fetcher/espn_client.py:1344-1345
async def fetch_players(self):
    """Fetch player data from ESPN API including team."""

    for player_info in players_data:
        # Extract team from proTeamId
        pro_team_id = player_info.get('proTeamId')
        team = ESPN_TEAM_MAPPINGS.get(pro_team_id, 'UNK')

        # Create player data object
        player_data = ESPNPlayerData(
            id=player_id,
            name=player_name,
            team=team,  # NFL team abbreviation (KC, PHI, etc.)
            position=position,
            # ... other fields
        )
```

**Team Mapping**:
```python
# ESPN team ID to abbreviation mapping
ESPN_TEAM_MAPPINGS = {
    1: "ATL", 2: "BUF", 3: "CHI", 4: "CIN", 5: "CLE",
    6: "DAL", 7: "DEN", 8: "DET", 9: "GB", 10: "TEN",
    11: "IND", 12: "KC", 13: "LV", 14: "LAR", 15: "MIA",
    16: "MIN", 17: "NE", 18: "NO", 19: "NYG", 20: "NYJ",
    21: "PHI", 22: "PIT", 23: "LAC", 24: "SF", 25: "SEA",
    26: "TB", 27: "WSH", 28: "CAR", 29: "JAX", 30: "BAL",
    33: "HOU", 34: "ARI"
}
```

---

## ESPN API JSON Analysis

### Player Team Data

**API Endpoint**: `https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{leagueId}`

**View Parameters**: `kona_player_info`

**Relevant JSON Path**: `player.proTeamId`

### JSON Structure

```json
{
  "id": 3929630,
  "fullName": "Saquon Barkley",
  "firstName": "Saquon",
  "lastName": "Barkley",
  "proTeamId": 21,
  "defaultPositionId": 2,
  "eligibleSlots": [2, 23, 16, 17],
  "stats": [...]
}
```

**Field Mapping**:

| JSON Field | Type | Description | Example Value | Maps To |
|------------|------|-------------|---------------|---------|
| `proTeamId` | int | ESPN team ID | 21 | PHI (via ESPN_TEAM_MAPPINGS) |
| `fullName` | string | Player full name | "Saquon Barkley" | name |
| `defaultPositionId` | int | ESPN position ID | 2 | RB (via ESPN_POSITION_MAPPINGS) |

**Team Extraction Logic**:
```python
# Input: ESPN JSON
player_json = {
    "id": 3929630,
    "fullName": "Saquon Barkley",
    "proTeamId": 21
}

# Extract team ID
pro_team_id = player_json.get('proTeamId')  # 21

# Map to abbreviation
team = ESPN_TEAM_MAPPINGS.get(21)  # "PHI"

# Written to players.csv
row = {
    'id': 3929630,
    'name': 'Saquon Barkley',
    'team': 'PHI',  # Used for schedule lookup
    'position': 'RB'
}
```

### Defense Rankings (Not in ESPN API)

Defense rankings are **NOT** provided by ESPN Fantasy API. They are calculated by `nfl-scores-fetcher` based on:

1. **Game Results**: Score data from NFL games
2. **Team Stats**: Offensive/defensive performance metrics
3. **Fantasy Points Allowed**: Position-specific scoring data

**Data Flow**:
```
NFL Game Results
    ↓
nfl-scores-fetcher (NFLScoresFetcher.py)
    ↓
Calculate rankings (offensive, defensive, position-specific)
    ↓
Write to data/teams.csv
    ↓
TeamDataManager loads rankings
    ↓
Used for schedule multiplier calculations
```

---

## Examples with Walkthroughs

### Example 1: Favorable Schedule (Weight Enabled)

**Scenario**: Week 9, drafting RB, hypothetical weight=0.5
**Config**: WEIGHT=0.5, IMPACT_SCALE=80.0

**Player**: Travis Etienne Jr. (RB, JAX)
**Team**: JAX
**Current Score**: 85.0 points (after steps 1-6)

**Step 1: Get future opponents**
```python
future_opponents = season_schedule_manager.get_future_opponents('JAX', 9)
# Returns: ['MIN', 'DET', None, 'HOU', 'TEN', 'NYJ', 'LV', 'TEN']
# Note: Week 12 is bye (None) - excluded from analysis
```

**Step 2: Get defense ranks vs RB**

| Week | Opponent | Defense vs RB Rank |
|------|----------|-------------------|
| 10 | MIN | 10 |
| 11 | DET | 3 |
| 12 | (BYE) | - (skipped) |
| 13 | HOU | 9 |
| 14 | TEN | 29 (easy) |
| 15 | NYJ | 20 |
| 16 | LV | 15 |
| 17 | TEN | 29 (easy) |

**Step 3: Calculate average**
```
defense_ranks = [10, 3, 9, 29, 20, 15, 29]
schedule_value = (10 + 3 + 9 + 29 + 20 + 15 + 29) / 7 = 115 / 7 = 16.43
```

**Step 4: Determine rating**
```
Thresholds (INCREASING): VP=8, P=16, G=24, E=32
16.43 is between POOR (16) and GOOD (24) → NEUTRAL zone
base_multiplier = 1.0
```

**Step 5: Apply weight**
```
WEIGHT = 0.5
final_multiplier = 1.0 ^ 0.5 = 1.0
```

**Step 6: Calculate bonus**
```
bonus = (80.0 * 1.0) - 80.0 = 0.0
```

**Step 7: Apply to score**
```
adjusted_score = 85.0 + 0.0 = 85.0
reason = "Schedule: NEUTRAL (avg opp def rank: 16.4, +0.0 pts)"
```

**Result**: Travis Etienne's schedule is neutral (average difficulty), so no bonus or penalty applied. Despite facing Tennessee twice (easy matchup), average is pulled down by Detroit (rank 3, very tough).

---

### Example 2: Difficult Schedule (Weight Enabled)

**Scenario**: Week 9, evaluating WR, weight=0.5
**Config**: WEIGHT=0.5, IMPACT_SCALE=80.0

**Player**: Davante Adams (WR, LV)
**Team**: LV
**Current Score**: 88.0 points

**Step 1: Future opponents (weeks 10-17)**
```
future_opponents = ['MIA', 'DEN', 'KC', 'TB', 'ATL', 'JAX', 'NO', 'LAC']
```

**Step 2: Defense ranks vs WR**

| Week | Opponent | Defense vs WR Rank |
|------|----------|-------------------|
| 10 | MIA | 9 |
| 11 | DEN | 8 |
| 12 | KC | 15 |
| 13 | TB | 13 |
| 14 | ATL | 2 (very tough) |
| 15 | JAX | 19 |
| 16 | NO | 24 |
| 17 | LAC | 14 |

**Step 3: Calculate average**
```
defense_ranks = [9, 8, 15, 13, 2, 19, 24, 14]
schedule_value = (9 + 8 + 15 + 13 + 2 + 19 + 24 + 14) / 8 = 104 / 8 = 13.0
```

**Step 4: Determine rating**
```
Thresholds: VP=8, P=16, G=24, E=32
13.0 is between VERY_POOR (8) and POOR (16) → POOR tier
base_multiplier = 0.975
```

**Step 5: Apply weight**
```
WEIGHT = 0.5
final_multiplier = 0.975 ^ 0.5 = 0.9874
```

**Step 6: Calculate bonus**
```
bonus = (80.0 * 0.9874) - 80.0 = 78.99 - 80.0 = -1.01
```

**Step 7: Apply to score**
```
adjusted_score = 88.0 + (-1.01) = 86.99
penalty = -1.01 pts
reason = "Schedule: POOR (avg opp def rank: 13.0, -1.0 pts)"
```

**Result**: Davante Adams receives -1.01 point penalty for tough remaining schedule (average rank 13.0 = strong defenses). Notable challenges include Atlanta (rank 2) and several mid-tier defenses.

---

### Example 3: Very Favorable Schedule (Weight Enabled)

**Scenario**: Week 9, drafting WR, weight=0.5
**Config**: WEIGHT=0.5, IMPACT_SCALE=80.0

**Player**: Terry McLaurin (WR, WSH)
**Team**: WSH
**Current Score**: 82.0 points

**Step 1: Future opponents**
```
future_opponents = ['PIT', 'PHI', 'DAL', 'TEN', 'NO', 'ATL', 'PHI', 'DAL']
```

**Step 2: Defense ranks vs WR**

| Week | Opponent | Defense vs WR Rank |
|------|----------|-------------------|
| 10 | PIT | 30 (easy) |
| 11 | PHI | 10 |
| 12 | DAL | 32 (easiest) |
| 13 | TEN | 28 (easy) |
| 14 | NO | 24 |
| 15 | ATL | 2 (tough) |
| 16 | PHI | 10 |
| 17 | DAL | 32 (easiest) |

**Step 3: Calculate average**
```
defense_ranks = [30, 10, 32, 28, 24, 2, 10, 32]
schedule_value = (30 + 10 + 32 + 28 + 24 + 2 + 10 + 32) / 8 = 168 / 8 = 21.0
```

**Step 4: Determine rating**
```
Thresholds: VP=8, P=16, G=24, E=32
21.0 is between POOR (16) and GOOD (24) → NEUTRAL zone (close to GOOD)
base_multiplier = 1.0
```

**Step 5: Apply weight**
```
WEIGHT = 0.5
final_multiplier = 1.0 ^ 0.5 = 1.0
```

**Step 6: Calculate bonus**
```
bonus = (80.0 * 1.0) - 80.0 = 0.0
```

**Step 7: Apply to score**
```
adjusted_score = 82.0 + 0.0 = 82.0
reason = "Schedule: NEUTRAL (avg opp def rank: 21.0, +0.0 pts)"
```

**Result**: Terry McLaurin's schedule is neutral (avg 21.0), just below GOOD threshold (24). Despite facing Dallas twice (rank 32, easiest) and Pittsburgh (rank 30), average is pulled down by Atlanta (rank 2, toughest) and two Philadelphia games (rank 10).

**Note**: If threshold for GOOD were lower (e.g., 20 instead of 24), this would be rated GOOD and receive a bonus.

---

### Example 4: Current Configuration (Weight = 0)

**Scenario**: Week 9, any draft pick with current production config
**Config**: WEIGHT=0.0 (disabled)

**Player**: CeeDee Lamb (WR, DAL)
**Team**: DAL
**Current Score**: 93.0 points

**Step 1: Future opponents**
```
future_opponents = ['PHI', 'HOU', 'WSH', 'NYG', 'CIN', 'CAR', 'TB', 'PHI']
```

**Step 2: Defense ranks vs WR**

| Week | Opponent | Defense vs WR Rank |
|------|----------|-------------------|
| 10 | PHI | 10 |
| 11 | HOU | 3 |
| 12 | WSH | 31 |
| 13 | NYG | 23 |
| 14 | CIN | 29 |
| 15 | CAR | 17 |
| 16 | TB | 13 |
| 17 | PHI | 10 |

**Step 3: Calculate average**
```
defense_ranks = [10, 3, 31, 23, 29, 17, 13, 10]
schedule_value = (10 + 3 + 31 + 23 + 29 + 17 + 13 + 10) / 8 = 136 / 8 = 17.0
```

**Step 4: Determine rating**
```
Thresholds: VP=8, P=16, G=24, E=32
17.0 is between POOR (16) and GOOD (24) → NEUTRAL zone
base_multiplier = 1.0
```

**Step 5: Apply weight (disabled)**
```
WEIGHT = 0.0
final_multiplier = 1.0 ^ 0.0 = 1.0
```

**Step 6: Calculate bonus**
```
bonus = (80.0 * 1.0) - 80.0 = 0.0
```

**Step 7: Apply to score**
```
adjusted_score = 93.0 + 0.0 = 93.0
reason = "Schedule: NEUTRAL (avg opp def rank: 17.0, +0.0 pts)"
```

**Result**: CeeDee Lamb's schedule rated NEUTRAL, but weight=0 means no adjustment regardless. Score remains 93.0 points. System tracks schedule strength for informational purposes but doesn't impact final score.

---

### Example 5: Insufficient Future Games

**Scenario**: Week 16, late season with limited remaining games
**Current Week**: 16
**Remaining weeks**: 17 (only 1 future game)

**Player**: Any player
**Current Score**: 80.0 points

**Calculation**:
```python
future_opponents = season_schedule_manager.get_future_opponents(player.team, 16)
# Returns: ['OPP'] (only week 17 opponent)

defense_ranks = [rank_for_OPP]  # Only 1 value

if len(defense_ranks) < 2:
    return None  # Insufficient data

_calculate_schedule_value() returns None
_apply_schedule_multiplier() returns (player_score, "")
```

**Result**:
```
schedule_value = None (< 2 future games)
adjusted_score = 80.0 (no adjustment)
reason = "" (empty, insufficient data)
```

**Rationale**: With only 1 future game, average schedule calculation is unreliable (single data point). Minimum 2 games required to assess schedule strength.

---

### Example 6: End of Season

**Scenario**: Week 17 (final week of regular season)
**Current Week**: 17

**Player**: Any player
**Future games**: 0 (season complete)

**Calculation**:
```python
future_opponents = season_schedule_manager.get_future_opponents(player.team, 17)
# Returns: [] (empty, no future games)

if not future_opponents:
    return None

_calculate_schedule_value() returns None
_apply_schedule_multiplier() returns (player_score, "")
```

**Result**:
```
No future opponents (season over)
adjusted_score = player_score (no change)
reason = "" (no schedule to evaluate)
```

---

## Configuration Reference

### Current Configuration (league_config.json)

```json
{
  "SCHEDULE_SCORING": {
    "IMPACT_SCALE": 80.0,
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "INCREASING",
      "STEPS": 8
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 0.0
  }
}
```

### Configuration Fields

| Field | Type | Description | Current Value | Effect |
|-------|------|-------------|---------------|--------|
| `IMPACT_SCALE` | float | Magnitude of schedule bonus | 80.0 | Determines point range of bonus/penalty |
| `THRESHOLDS.BASE_POSITION` | int | Center point for threshold calculation | 0 | Starting point for rank thresholds |
| `THRESHOLDS.DIRECTION` | string | Threshold direction logic | "INCREASING" | Higher rank = better |
| `THRESHOLDS.STEPS` | int | Step size between thresholds | 8 | Spacing between tiers |
| `MULTIPLIERS.VERY_POOR` | float | Base multiplier for very poor schedule | 0.95 | Tough schedule base |
| `MULTIPLIERS.POOR` | float | Base multiplier for poor schedule | 0.975 | Somewhat tough schedule |
| `MULTIPLIERS.GOOD` | float | Base multiplier for good schedule | 1.025 | Somewhat easy schedule |
| `MULTIPLIERS.EXCELLENT` | float | Base multiplier for excellent schedule | 1.05 | Easy schedule base |
| `WEIGHT` | float | Exponent for multiplier adjustment | 0.0 | Currently disabled |

### Threshold Calculation

**Direction**: `INCREASING` (higher rank = better schedule)

**Formula**:
```
BASE = 0 (neutral position)
STEP = 8

VERY_POOR = BASE + STEP = 0 + 8 = 8
POOR = BASE + (2 * STEP) = 0 + 16 = 16
GOOD = BASE + (3 * STEP) = 0 + 24 = 24
EXCELLENT = BASE + (4 * STEP) = 0 + 32 = 32
```

**Calculated Thresholds**:
- **VERY_POOR**: Avg rank ≤ 8 (facing elite defenses) → 0.95 multiplier
- **POOR**: Avg rank ≤ 16 (facing strong defenses) → 0.975 multiplier
- **NEUTRAL**: 16 < avg rank < 24 (mixed schedule) → 1.0 multiplier
- **GOOD**: Avg rank ≥ 24 (facing weak defenses) → 1.025 multiplier
- **EXCELLENT**: Avg rank ≥ 32 (facing worst defenses) → 1.05 multiplier

**Note**: EXCELLENT threshold (32) is theoretical maximum (no team can have avg > 32). Effectively, GOOD threshold (24+) represents best achievable schedules.

### Bonus Calculation Examples

**With IMPACT_SCALE = 80.0, WEIGHT = 0.5**:

| Rating | Base Mult | Final Mult | Bonus Calculation | Bonus |
|--------|-----------|------------|-------------------|-------|
| EXCELLENT | 1.05 | 1.05^0.5 = 1.0247 | (80 * 1.0247) - 80 | +1.98 pts |
| GOOD | 1.025 | 1.025^0.5 = 1.0124 | (80 * 1.0124) - 80 | +0.99 pts |
| NEUTRAL | 1.0 | 1.0^0.5 = 1.0 | (80 * 1.0) - 80 | 0 pts |
| POOR | 0.975 | 0.975^0.5 = 0.9874 | (80 * 0.9874) - 80 | -1.01 pts |
| VERY_POOR | 0.95 | 0.95^0.5 = 0.9747 | (80 * 0.9747) - 80 | -2.02 pts |

### Configuration Tuning Guide

**Increasing Effect**:
- **Increase WEIGHT** (e.g., 0.5, 1.0, 2.0) → amplifies schedule bonus/penalty
- **Increase IMPACT_SCALE** (e.g., 100.0, 120.0) → larger point adjustments
- **Adjust STEPS** (e.g., 6, 10) → changes threshold sensitivity

**Decreasing Effect**:
- **Decrease WEIGHT** (already at 0.0 = disabled)
- **Decrease IMPACT_SCALE** (e.g., 50.0, 40.0) → smaller point adjustments

**Changing Thresholds**:
```json
{
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "INCREASING",
    "STEPS": 6
  }
}
```
Results in:
- VERY_POOR = 6 (tighter threshold, easier to avoid)
- POOR = 12
- GOOD = 18 (easier to achieve)
- EXCELLENT = 24

**Why Currently Disabled**:
- Simulation optimization found no performance improvement with schedule scoring
- Projection-based scoring (current approach) works well without schedule adjustment
- Schedule strength already implicitly captured in player projections
- Can be re-enabled by setting WEIGHT > 0 if desired

---

## See Also

### Related Metrics
- **[06_matchup_multiplier.md](06_matchup_multiplier.md)** - Current week opponent analysis (complements schedule)
- **[04_team_quality_multiplier.md](04_team_quality_multiplier.md)** - Team offensive rank (uses same teams.csv data)
- **[01_normalization.md](01_normalization.md)** - Base score calculation (schedule adjusts this base)

### Implementation Files
- **`league_helper/util/player_scoring.py:303-354`** - Schedule value calculation
- **`league_helper/util/player_scoring.py:571-607`** - Schedule bonus application
- **`league_helper/util/ConfigManager.py:309-324`** - Schedule multiplier configuration
- **`league_helper/util/SeasonScheduleManager.py:117-141`** - Future opponents lookup
- **`league_helper/util/TeamDataManager.py:116-164`** - Position-specific defense ranks

### Data Files
- **`data/league_config.json`** - Schedule scoring configuration (SCHEDULE_SCORING section)
- **`data/season_schedule.csv`** - NFL season schedule (week, team, opponent)
- **`data/teams.csv`** - Team rankings (def_vs_qb_rank, def_vs_rb_rank, etc.)
- **`data/players.csv`** - Player team assignments (team field)

### Data Collection Scripts
- **`nfl-scores-fetcher/NFLScoresFetcher.py`** - Updates team defense rankings weekly

### Testing
- **`tests/league_helper/util/test_player_scoring.py`** - Schedule calculation and bonus tests
- **`tests/league_helper/util/test_SeasonScheduleManager.py`** - Future opponents lookup tests
- **`tests/league_helper/util/test_TeamDataManager.py`** - Defense rank retrieval tests

### Documentation
- **[README.md](../../README.md)** - Scoring algorithm overview
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture and data flow
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines

---

**Last Updated**: November 5, 2025
**Current NFL Week**: 9
**Documentation Version**: 1.0
**Schedule Scoring Status**: Disabled (weight = 0)
