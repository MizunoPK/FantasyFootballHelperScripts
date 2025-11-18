# Team Quality Multiplier (Step 4)

## Overview

**Type**: Multiplicative (percentage adjustment)
**Effect**: ±1.8% (0.982x to 1.017x with default weight=0.36)
**Base Multipliers**: 0.95x to 1.05x (±5% before weight exponent)
**When Applied**: Step 4 of 10-step scoring algorithm
**Purpose**: Adjust scores based on the player's NFL team offensive or defensive strength

The Team Quality Multiplier evaluates how a player's NFL team performs overall, adjusting fantasy scores based on team-level offensive or defensive strength. Offensive players (QB, RB, WR, TE, K) benefit from playing on high-powered offenses, while defensive players (DST) benefit from strong defensive units. Team rankings (1-32, where 1=best) are calculated from ESPN API team statistics.

**Key Characteristics**:
- **Position-specific logic**: Offensive players use team_offensive_rank, DST uses team_defensive_rank
- **Data-driven rankings**: Calculated from aggregated ESPN team statistics
- **Rank-based (1-32)**: 1=best team, 32=worst team in league
- **Updated with player data**: Rankings fetched alongside player projections
- **Environmental factor**: Captures team context independent of individual player performance

**Formula**:
```
Team Rank (1-32) → Multiplier lookup → Apply weight exponent
```

**Implementation**:
- **Data Collection**: `player-data-fetcher/espn_client.py` (team rankings from ESPN API)
- **Multiplier Application**: `league_helper/util/player_scoring.py:505-519`
- **Data Storage**: `data/teams.csv` and `player-data-fetcher/data/teams_latest.csv`

---

## Modes Using This Metric

### Add To Roster Mode (Draft Helper)
**Enabled**: Yes (`team_quality=True`)
**Why**: Team context significantly impacts fantasy production. A talented RB on a strong offense (DET, SF) scores more than an equally-talented RB on a weak offense (CAR, NYG) due to more scoring opportunities, better game scripts, and higher volume.

**Example**: Two RBs with similar individual talent:
- RB1: Plays for DET (offensive_rank=2, top offense) → benefits from high-scoring games
- RB2: Plays for CAR (offensive_rank=27, bottom offense) → limited by poor offensive environment
- Team quality multiplier helps identify RB1 as the better fantasy option

### Starter Helper Mode (Roster Optimizer)
**Enabled**: Yes (`team_quality=True`)
**Why**: Team offensive/defensive strength provides important context for weekly scoring potential. Strong offenses create more opportunities and volume, while weak offenses limit scoring chances regardless of matchup.

**Rationale**: While team quality is a season-long factor, it directly affects weekly production by influencing game script, opportunity volume, and scoring potential. Combined with matchup (opponent strength) and performance (recent trends), team quality provides the environmental context needed for accurate weekly decisions. A RB on a high-powered offense (DET, SF) consistently receives more touches and red zone opportunities than an equivalent RB on a weak offense (CAR, NYG), making team quality relevant for weekly lineup optimization.

### Trade Simulator Mode
**Enabled**: Yes (`team_quality=True`)
**Why**: Team situation is a persistent environmental factor affecting player value throughout the season. Acquiring a player on a strong team provides more reliable production than projections alone suggest.

**Example**: Evaluating trade offer:
- Receiving: RB on IND (offensive_rank=1, best offense)
- Giving: RB on TEN (offensive_rank=32, worst offense)
- Team quality multiplier helps quantify the value of superior team context

---

## How League Helper Gets the Value/Multiplier

### Step 1: Determine Which Rank to Use (Position-Based Logic)

**Method**: `PlayerScoringCalculator._apply_team_quality_multiplier()`
**File**: `league_helper/util/player_scoring.py:505-519`

```python
def _apply_team_quality_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    """
    Apply team quality multiplier (Step 4).

    Offensive players (QB, RB, WR, TE, K) use team_offensive_rank
    Defensive players (DST) use team_defensive_rank
    """
    # Determine which team ranking to use based on player type
    quality_val = p.team_offensive_rank
    if p.position in Constants.DEFENSE_POSITIONS:
        quality_val = p.team_defensive_rank

    # Get multiplier based on team quality rank (1-32)
    # Better teams (rank 1-10) = higher multiplier
    # Worse teams (rank 23-32) = lower multiplier
    multiplier, rating = self.config.get_team_quality_multiplier(quality_val)
    reason = f"Team Quality: {rating} ({multiplier:.2f}x)"
    return player_score * multiplier, reason
```

**Position Logic**:
- **QB, RB, WR, TE, K**: Use `team_offensive_rank` (measures offensive firepower)
- **DST**: Use `team_defensive_rank` (measures defensive strength)

**Rationale**:
- Offensive players depend on their offense's ability to move the ball and score
- Defensive players depend on their defense's ability to stop opponents and create turnovers
- Each position group benefits from their respective unit's strength

### Step 2: Load Team Ranks from TeamDataManager

**Method**: `TeamDataManager.__init__()` and `_load_team_data()`
**File**: `league_helper/util/TeamDataManager.py:34-90`

```python
class TeamDataManager:
    """
    Loads and manages team ranking data from teams.csv file.

    Attributes:
        team_data_cache (Dict[str, TeamData]): Cached team data by team abbreviation
        teams_file (Path): Path to teams.csv data file
    """

    def __init__(self, data_folder: Path, season_schedule_manager=None, current_nfl_week=1):
        """Initialize TeamDataManager and load team data."""
        self.teams_file = data_folder / 'teams.csv'
        self.team_data_cache: Dict[str, TeamData] = {}
        self._load_team_data()

    def _load_team_data(self) -> None:
        """Load team data from teams.csv file."""
        try:
            if not self.teams_file.exists():
                self.logger.warning(f"Teams file not found: {self.teams_file}")
                return

            teams = load_teams_from_csv(str(self.teams_file))

            # Cache team data by abbreviation for fast lookup
            for team in teams:
                self.team_data_cache[team.abbreviation] = team

            self.logger.info(f"Loaded {len(self.team_data_cache)} teams from {self.teams_file}")

        except Exception as e:
            self.logger.error(f"Failed to load team data: {e}")
```

**Data Flow**:
```
teams.csv → load_teams_from_csv() → team_data_cache → player.team_offensive_rank
```

**Lookup Process**:
1. Player has `team` field (e.g., "DET", "SF", "NYG")
2. TeamDataManager finds team in cache: `team_data_cache["DET"]`
3. Returns TeamData object with offensive_rank and defensive_rank
4. Player object stores these values for scoring calculations

### Step 3: Convert Rank to Multiplier

**Method**: `ConfigManager.get_team_quality_multiplier()`
**File**: `league_helper/util/ConfigManager.py:305-310, 922-1008`

```python
def get_team_quality_multiplier(self, rank: int) -> Tuple[float, str]:
    """
    Convert team quality rank (1-32) to multiplier and rating label.

    Args:
        rank: Team rank where 1=best, 32=worst

    Returns:
        Tuple[float, str]: (multiplier, rating_label)
    """
    return self._get_multiplier(
        self.team_quality_scoring,
        rank,
        rising_thresholds=False  # Lower rank = better
    )

def _get_multiplier(self, scoring_dict, val, rising_thresholds=True):
    """
    Generic threshold-based multiplier calculation.

    For TEAM_QUALITY (rising_thresholds=False, lower rank = better):
    - val <= EXCELLENT threshold → EXCELLENT multiplier
    - val <= GOOD threshold → GOOD multiplier
    - GOOD < val < POOR → neutral (1.0)
    - val >= POOR threshold → POOR multiplier
    - val >= VERY_POOR threshold → VERY_POOR multiplier

    Then apply weight exponent: final_multiplier = base_multiplier ^ weight
    """
    thresholds = scoring_dict['THRESHOLDS']
    multipliers = scoring_dict['MULTIPLIERS']
    weight = scoring_dict['WEIGHT']

    # For team quality, lower rank = better (rising_thresholds=False)
    if not rising_thresholds:
        if val <= thresholds['EXCELLENT']:
            multiplier, label = multipliers['EXCELLENT'], 'EXCELLENT'
        elif val <= thresholds['GOOD']:
            multiplier, label = multipliers['GOOD'], 'GOOD'
        elif val >= thresholds['VERY_POOR']:
            multiplier, label = multipliers['VERY_POOR'], 'VERY_POOR'
        elif val >= thresholds['POOR']:
            multiplier, label = multipliers['POOR'], 'POOR'
        else:
            multiplier, label = 1.0, 'NEUTRAL'

    # Apply weight exponent
    multiplier = multiplier ** weight
    return multiplier, label
```

### Step 4: Apply to Player Score

**Complete Flow**:
```
Player (team="DET")
    ↓
TeamDataManager lookup: team_data_cache["DET"]
    ↓
Extract offensive_rank=2 (2nd best offense)
    ↓
get_team_quality_multiplier(2) → threshold check
    ↓
2 <= EXCELLENT threshold (3.15) → EXCELLENT
    ↓
Base multiplier: 1.05
    ↓
Apply weight: 1.05 ^ 0.357 = 1.0175
    ↓
Adjust score: player_score * 1.0175
```

---

## Calculations Involved

### Formula Breakdown

**1. Rank Extraction** (from teams.csv):
```
If player.position in ['QB', 'RB', 'WR', 'TE', 'K']:
    quality_val = player.team_offensive_rank
Elif player.position == 'DST':
    quality_val = player.team_defensive_rank
```

**2. Threshold Comparison** (falling thresholds logic - lower rank = better):
```
EXCELLENT = BASE + STEPS = 0 + 1.05 = 3.15 (ranks 1-3)
GOOD = BASE + (2 * STEPS) = 0 + 2.10 = 6.30 (ranks 4-6)
POOR = BASE + (30 * STEPS) = 0 + 31.43 = 25.73 (ranks 26+)
VERY_POOR = BASE + (32 * STEPS) = 0 + 33.53 = 29.68 (ranks 30+)

If rank <= 3.15:
    base_multiplier = EXCELLENT (1.05)
Elif rank <= 6.30:
    base_multiplier = GOOD (1.025)
Elif rank >= 29.68:
    base_multiplier = VERY_POOR (0.95)
Elif rank >= 25.73:
    base_multiplier = POOR (0.975)
Else:
    base_multiplier = NEUTRAL (1.0)
```

**3. Weight Exponent Application**:
```
final_multiplier = base_multiplier ^ WEIGHT

Example (WEIGHT=0.357):
- EXCELLENT: 1.05^0.357 = 1.0175 (+1.75%)
- GOOD: 1.025^0.357 = 1.0088 (+0.88%)
- NEUTRAL: 1.0^0.357 = 1.0 (0%)
- POOR: 0.975^0.357 = 0.9912 (-0.88%)
- VERY_POOR: 0.95^0.357 = 0.9826 (-1.74%)
```

**4. Final Score Adjustment**:
```
adjusted_score = player_score * final_multiplier
```

### Example Calculation

**Player**: Jahmyr Gibbs (RB, DET)
**Current Week**: 10
**Config**: WEIGHT=0.357, STEPS=1.05

**Step 1: Determine which rank to use**
```
Position: RB (offensive player)
Use: team_offensive_rank
```

**Step 2: Extract team rank**
```
Team: DET
teams.csv lookup: DET → offensive_rank = 2
quality_val = 2 (2nd best offense in NFL)
```

**Step 3: Determine rating threshold**
```
EXCELLENT threshold = 3.15
2 <= 3.15 → EXCELLENT
base_multiplier = 1.05
```

**Step 4: Apply weight exponent**
```
Config: WEIGHT = 0.357
final_multiplier = 1.05 ^ 0.357 = 1.0175
```

**Step 5: Apply to score**
```
If player_score = 80.0 (after steps 1-3):
adjusted_score = 80.0 * 1.0175 = 81.40
bonus = 81.40 - 80.0 = +1.40 points
reason = "Team Quality: EXCELLENT (1.02x)"
```

**Result**: Jahmyr Gibbs receives +1.40 point boost for playing on the 2nd best offense (DET).

---

## Data Sources (teams.csv and players.csv Fields)

### teams.csv Fields

| Field Name | Data Type | Description | Valid Range | Example Values |
|------------|-----------|-------------|-------------|----------------|
| `team` | string | NFL team abbreviation | 32 NFL teams | DET, SF, KC, CHI |
| `offensive_rank` | int | Team offensive strength rank | 1-32 (1=best) | 1, 2, 6, 22, 32 |
| `defensive_rank` | int | Team defensive strength rank | 1-32 (1=best) | 1, 2, 6, 28, 32 |

### teams.csv Field Specifications

**`team`**:
- **Type**: string (3-letter abbreviation)
- **Source**: ESPN NFL team abbreviations (normalized)
- **Values**: ARI, ATL, BAL, BUF, CAR, CHI, CIN, CLE, DAL, DEN, DET, GB, HOU, IND, JAX, KC, LAC, LAR, LV, MIA, MIN, NE, NO, NYG, NYJ, PHI, PIT, SEA, SF, TB, TEN, WSH
- **Special case**: "WSH" used instead of ESPN's "WAS" (normalized in fetcher)

**`offensive_rank`**:
- **Type**: int
- **Source**: Calculated by `player-data-fetcher/espn_client.py` from ESPN team statistics API
- **Range**: 1-32
  - 1-3: Elite offenses (EXCELLENT multiplier)
  - 4-6: Strong offenses (GOOD multiplier)
  - 7-25: Average offenses (NEUTRAL multiplier)
  - 26-29: Weak offenses (POOR multiplier)
  - 30-32: Bottom-tier offenses (VERY_POOR multiplier)
- **Update frequency**: Updated with player data fetcher runs (typically daily)
- **Calculation**: Based on ESPN team statistics (points scored, yards, efficiency)

**`defensive_rank`**:
- **Type**: int
- **Source**: Calculated by `player-data-fetcher/espn_client.py` from ESPN team statistics API
- **Range**: 1-32 (same tier structure as offensive_rank)
- **Update frequency**: Updated with player data fetcher runs (typically daily)
- **Calculation**: Based on ESPN team statistics (points allowed, yards allowed, turnovers)

### players.csv Fields (Inherited from teams.csv)

| Field Name | Data Type | Description | Valid Range | Example Values |
|------------|-----------|-------------|-------------|----------------|
| `team` | string | Player's NFL team | 32 NFL teams | DET, SF, KC, CHI |

**Note**: `team_offensive_rank` and `team_defensive_rank` are NOT stored in players.csv. They are looked up dynamically from teams.csv via TeamDataManager during scoring calculations.

### Sample teams.csv Data

```csv
team,offensive_rank,defensive_rank,def_vs_qb_rank,def_vs_rb_rank,def_vs_wr_rank,def_vs_te_rank,def_vs_k_rank
DET,2,6,16,3,21,11,4
IND,1,4,19,12,27,31,11
BUF,3,16,2,24,12,1,6
CHI,6,1,27,17,26,18,10
NYG,22,29,30,31,23,16,30
CAR,27,20,13,26,17,23,17
TEN,32,12,22,29,28,10,24
```

**Interpretation**:
- **DET**: Offense rank 2 (elite), Defense rank 6 (strong)
  - Detroit players benefit from high-powered offense (EXCELLENT multiplier)
- **IND**: Offense rank 1 (best), Defense rank 4 (elite)
  - Indianapolis offensive players get maximum boost (rank 1 = EXCELLENT)
- **CHI**: Offense rank 6 (strong), Defense rank 1 (best)
  - Chicago DST benefits from #1 defense (EXCELLENT multiplier)
- **NYG**: Offense rank 22 (below average), Defense rank 29 (poor)
  - New York offensive players receive penalty (NEUTRAL/POOR multiplier)
- **TEN**: Offense rank 32 (worst), Defense rank 12 (average)
  - Tennessee offensive players receive maximum penalty (VERY_POOR multiplier)

---

## How Player Data Fetcher Populates Team Rankings

### Data Collection Process

**Script**: `player-data-fetcher/player_data_fetcher_main.py`
**Data Source**: ESPN Fantasy Football API (team statistics endpoint)
**Method**: Fetch team statistics from ESPN API and calculate rankings
**Frequency**: Runs with player data fetcher (typically daily or on-demand)

### Team Ranking Calculation Logic

**Step 1: Calculate Rankings Using Rolling Window**

**File**: `player-data-fetcher/espn_client.py:739-1012`

**Main Method**: `_calculate_team_rankings_from_stats()` → `_calculate_rolling_window_rankings()`

The ESPN client uses a **rolling window approach** to calculate team rankings from recent game performance, providing more current team assessments compared to cumulative season statistics.

**Rolling Window Configuration**:
- **Window Size**: `MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS = 4` (previous 4 weeks)
- **Previous Weeks Only**: Excludes current week (uses only completed games)
- **Example (Week 10)**: Uses weeks 6, 7, 8, 9 (rolling 4-week window)
- **Early Season (Weeks 1-4)**: Uses neutral rankings (all teams = rank 16)

**Calculation Process**:

1. **Fetch Game Scores**: `_fetch_week_scores()` extracts scores from ESPN scoreboard API for each week in the rolling window
2. **Aggregate Performance**: Accumulates points scored/allowed per team across all games in window
3. **Calculate Averages**: Divides by actual games played (handles bye weeks correctly)
4. **Rank Teams**:
   - **Offensive Rank**: Based on points scored per game (higher = better)
   - **Defensive Rank**: Based on points allowed per game (lower = better)
5. **Position-Specific Rankings**: `_calculate_position_defense_rankings()` uses same rolling window for consistency

**Why Rolling Window?**
- **More Current**: Recent 4 weeks better reflects team's current form than full-season averages
- **Handles Improvement/Decline**: Teams that improve mid-season get better rankings faster
- **Fair Comparison**: Bye weeks handled by dividing by actual games played
- **Consistent**: All 7 rankings (offensive, defensive, 5× position-specific) use same window

**Early Season Behavior**:
- **Weeks 1-4**: Not enough previous weeks for 4-week window → neutral rankings (rank 16)
- **Week 5+**: Full rolling window available (4 previous weeks)
- This prevents volatile rankings from small sample sizes

**Step 2: Store Rankings**

**File**: `player-data-fetcher/player_data_fetcher_main.py:262-265`

```python
# Store team rankings for later use by exporter
self.team_rankings = team_rankings  # Format: {'KC': {'offensive_rank': 5, 'defensive_rank': 12}, ...}
self.current_week_schedule = current_week_schedule
self.position_defense_rankings = position_defense_rankings
```

**Step 3: Pass to Exporter**

**File**: `player-data-fetcher/player_data_fetcher_main.py:307-313`

```python
# Pass team data to exporter for teams.csv creation
self.exporter.set_team_rankings(self.team_rankings)
self.exporter.set_current_week_schedule(self.current_week_schedule)
self.exporter.set_position_defense_rankings(self.position_defense_rankings)
```

**Step 4: Export to CSV Files**

**File**: `player-data-fetcher/player_data_exporter.py:494-525, 452-492`

The exporter writes team rankings to TWO locations:

**A. Timestamped file** (`player-data-fetcher/data/teams_YYYYMMDD_HHMMSS.csv`):
- Created by `export_teams_csv()` method
- Provides historical record of rankings
- Also creates `teams_latest.csv` symlink

**B. Shared file** (`../data/teams.csv`):
- Created by `export_teams_to_data()` method
- This is the file consumed by league helper
- Path configured in `config.py:TEAMS_CSV = '../data/teams.csv'`

```python
async def export_teams_to_data(self, data: ProjectionData) -> str:
    """Export team data to data directory for consumption by other modules."""
    # Resolve path to teams.csv (configured in config.py)
    shared_teams_file = Path(__file__).parent / TEAMS_CSV  # ../data/teams.csv

    # Extract team data from players using team rankings
    fantasy_players = self.get_fantasy_players(data)
    teams = extract_teams_from_rankings(
        fantasy_players,
        self.team_rankings,  # Rankings from ESPN API
        self.current_week_schedule,
        self.position_defense_rankings
    )

    # Save to shared data/teams.csv
    save_teams_to_csv(teams, str(shared_teams_file))

    return str(shared_teams_file)
```

### Data Flow Summary

```
ESPN Team Stats API
    ↓
espn_client.py (_fetch_team_rankings, _calculate_team_rankings_from_stats)
    ↓
player_data_fetcher_main.py (stores rankings)
    ↓
player_data_exporter.py (set_team_rankings)
    ↓
utils/TeamData.py (extract_teams_from_rankings, save_teams_to_csv)
    ↓
TWO OUTPUTS:
    1. player-data-fetcher/data/teams_TIMESTAMP.csv (historical record)
    2. ../data/teams.csv (consumed by league helper)
    ↓
TeamDataManager.py (loads data/teams.csv)
    ↓
player_scoring.py (applies team quality multiplier)
```

### Ranking Methodology

**Offensive Rankings**:
- Based on ESPN team statistics (points scored, yards, efficiency)
- Higher offensive output = better rank (lower number)
- Ranks 1-32 (1 = best offense, 32 = worst offense)

**Defensive Rankings**:
- Based on ESPN team statistics (points allowed, yards allowed, turnovers)
- Better defensive performance = better rank (lower number)
- Ranks 1-32 (1 = best defense, 32 = worst defense)

**Position-Specific Defense Rankings**:
- Also extracted from ESPN API statistics
- Fields: `def_vs_qb_rank`, `def_vs_rb_rank`, `def_vs_wr_rank`, `def_vs_te_rank`, `def_vs_k_rank`
- Used for matchup scoring (Step 6) and schedule scoring (Step 7)

### Update Frequency

- **Player data fetcher runs**: Typically daily or on-demand
- **Minimum weeks check**: Requires MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS games (default: 3)
- **Early season**: Uses neutral rankings (all teams rank 16) if insufficient data
- **Mid-to-late season**: Uses current season statistics from ESPN API
- **Real-time**: Rankings reflect ESPN's latest team statistics

---

## Examples with Walkthroughs

### Example 1: Elite Offense Player (Jahmyr Gibbs - DET RB)

**Scenario**: Week 10, evaluating RB Jahmyr Gibbs for lineup
**Player Data**:
- Position: RB (offensive player)
- Team: DET
- Team Offensive Rank: 2 (2nd best offense)
- Current Score (after Steps 1-3): 80.0 points

**Step 1: Determine which rank to use**
```
Position: RB (offensive player, not DST)
Use: team_offensive_rank
```

**Step 2: Extract team rank**
```
Team: DET
teams.csv lookup: DET → offensive_rank = 2
quality_val = 2 (elite offense)
```

**Step 3: Determine rating threshold**
```
Config thresholds:
EXCELLENT = 3.15 (ranks 1-3)
GOOD = 6.30 (ranks 4-6)
NEUTRAL = 7-25
POOR = 26-29
VERY_POOR = 30-32

2 <= 3.15 → EXCELLENT tier
base_multiplier = 1.05
```

**Step 4: Apply weight exponent**
```
Config: WEIGHT = 0.357
final_multiplier = 1.05 ^ 0.357 = 1.0175
```

**Step 5: Apply to score**
```
adjusted_score = 80.0 * 1.0175 = 81.40
bonus = 81.40 - 80.0 = +1.40 points
reason = "Team Quality: EXCELLENT (1.02x)"
```

**Result**: Jahmyr Gibbs receives +1.40 point boost for playing on the 2nd best offense in the NFL (DET Lions).

---

### Example 2: Best Offense Player (Jonathan Taylor - IND RB)

**Scenario**: Week 10, evaluating RB Jonathan Taylor
**Player Data**:
- Position: RB
- Team: IND
- Team Offensive Rank: 1 (best offense)
- Current Score (after Steps 1-3): 85.0 points

**Step 1: Determine which rank to use**
```
Position: RB (offensive player)
Use: team_offensive_rank
```

**Step 2: Extract team rank**
```
Team: IND
teams.csv lookup: IND → offensive_rank = 1
quality_val = 1 (best offense in NFL)
```

**Step 3: Determine rating threshold**
```
1 <= 3.15 → EXCELLENT tier
base_multiplier = 1.05
```

**Step 4: Apply weight exponent**
```
final_multiplier = 1.05 ^ 0.357 = 1.0175
```

**Step 5: Apply to score**
```
adjusted_score = 85.0 * 1.0175 = 86.49
bonus = 86.49 - 85.0 = +1.49 points
reason = "Team Quality: EXCELLENT (1.02x)"
```

**Result**: Jonathan Taylor receives +1.49 point boost for playing on the #1 ranked offense (IND Colts).

---

### Example 3: Elite Defense Player (Bears D/ST - CHI)

**Scenario**: Week 10, evaluating Bears D/ST for lineup
**Player Data**:
- Position: DST (defensive player)
- Team: CHI
- Team Defensive Rank: 1 (best defense)
- Current Score (after Steps 1-3): 50.0 points

**Step 1: Determine which rank to use**
```
Position: DST (defensive player)
Use: team_defensive_rank (NOT offensive_rank)
```

**Step 2: Extract team rank**
```
Team: CHI
teams.csv lookup: CHI → defensive_rank = 1
quality_val = 1 (best defense in NFL)
```

**Step 3: Determine rating threshold**
```
1 <= 3.15 → EXCELLENT tier
base_multiplier = 1.05
```

**Step 4: Apply weight exponent**
```
final_multiplier = 1.05 ^ 0.357 = 1.0175
```

**Step 5: Apply to score**
```
adjusted_score = 50.0 * 1.0175 = 50.88
bonus = 50.88 - 50.0 = +0.88 points
reason = "Team Quality: EXCELLENT (1.02x)"
```

**Result**: Chicago Bears D/ST receives +0.88 point boost for being the #1 ranked defense in the NFL.

**Key Difference**: DST uses defensive_rank (1), not offensive_rank (6). This correctly rewards the Bears' elite defense.

---

### Example 4: Good Offense Player (Amon-Ra St. Brown - DET WR)

**Scenario**: Week 10, evaluating WR Amon-Ra St. Brown
**Player Data**:
- Position: WR
- Team: DET
- Team Offensive Rank: 2 (elite offense, same as Gibbs example)
- Current Score (after Steps 1-3): 95.0 points

**Step 1-5**: (Same logic as Gibbs example, both play for DET)
```
quality_val = 2
EXCELLENT tier
final_multiplier = 1.0175
adjusted_score = 95.0 * 1.0175 = 96.66
bonus = +1.66 points
```

**Result**: Amon-Ra St. Brown also benefits from DET's elite offense (+1.66 points). Both DET offensive players receive the same multiplier regardless of position.

---

### Example 5: Average Offense Player (Xavier Worthy - KC WR)

**Scenario**: Week 10, evaluating WR Xavier Worthy
**Player Data**:
- Position: WR
- Team: KC
- Team Offensive Rank: 9 (middle-of-pack offense)
- Current Score (after Steps 1-3): 70.0 points

**Step 1: Determine which rank to use**
```
Position: WR (offensive player)
Use: team_offensive_rank
```

**Step 2: Extract team rank**
```
Team: KC
teams.csv lookup: KC → offensive_rank = 9
quality_val = 9 (average offense)
```

**Step 3: Determine rating threshold**
```
9 > 6.30 (not GOOD)
9 < 25.73 (not POOR)
→ NEUTRAL tier
base_multiplier = 1.0
```

**Step 4: Apply weight exponent**
```
final_multiplier = 1.0 ^ 0.357 = 1.0
```

**Step 5: Apply to score**
```
adjusted_score = 70.0 * 1.0 = 70.0
bonus = 0.0 points
reason = "Team Quality: NEUTRAL (1.00x)"
```

**Result**: Xavier Worthy receives no adjustment for playing on an average offense (rank 9). No bonus or penalty applied.

---

### Example 6: Weak Offense Player (Malik Nabers - NYG WR)

**Scenario**: Week 10, evaluating WR Malik Nabers
**Player Data**:
- Position: WR
- Team: NYG
- Team Offensive Rank: 22 (below-average offense)
- Current Score (after Steps 1-3): 75.0 points

**Step 1: Determine which rank to use**
```
Position: WR (offensive player)
Use: team_offensive_rank
```

**Step 2: Extract team rank**
```
Team: NYG
teams.csv lookup: NYG → offensive_rank = 22
quality_val = 22 (below-average offense)
```

**Step 3: Determine rating threshold**
```
22 > 6.30 (not GOOD)
22 < 25.73 (not POOR)
→ NEUTRAL tier
base_multiplier = 1.0
```

**Step 4: Apply weight exponent**
```
final_multiplier = 1.0 ^ 0.357 = 1.0
```

**Step 5: Apply to score**
```
adjusted_score = 75.0 * 1.0 = 75.0
bonus = 0.0 points
reason = "Team Quality: NEUTRAL (1.00x)"
```

**Result**: Malik Nabers receives no adjustment (rank 22 still in neutral zone). Must reach rank 26+ for penalty.

---

### Example 7: Poor Offense Player (Chuba Hubbard - CAR RB)

**Scenario**: Week 10, evaluating RB Chuba Hubbard
**Player Data**:
- Position: RB
- Team: CAR
- Team Offensive Rank: 27 (poor offense)
- Current Score (after Steps 1-3): 68.0 points

**Step 1: Determine which rank to use**
```
Position: RB (offensive player)
Use: team_offensive_rank
```

**Step 2: Extract team rank**
```
Team: CAR
teams.csv lookup: CAR → offensive_rank = 27
quality_val = 27 (poor offense)
```

**Step 3: Determine rating threshold**
```
27 >= 25.73 (POOR threshold)
27 < 29.68 (not VERY_POOR)
→ POOR tier
base_multiplier = 0.975
```

**Step 4: Apply weight exponent**
```
final_multiplier = 0.975 ^ 0.357 = 0.9912
```

**Step 5: Apply to score**
```
adjusted_score = 68.0 * 0.9912 = 67.40
penalty = 68.0 - 67.40 = -0.60 points
reason = "Team Quality: POOR (0.99x)"
```

**Result**: Chuba Hubbard receives -0.60 point penalty for playing on a poor offense (CAR, rank 27).

---

### Example 8: Worst Offense Player (Tony Pollard - TEN RB)

**Scenario**: Week 10, evaluating RB Tony Pollard
**Player Data**:
- Position: RB
- Team: TEN
- Team Offensive Rank: 32 (worst offense)
- Current Score (after Steps 1-3): 65.0 points

**Step 1: Determine which rank to use**
```
Position: RB (offensive player)
Use: team_offensive_rank
```

**Step 2: Extract team rank**
```
Team: TEN
teams.csv lookup: TEN → offensive_rank = 32
quality_val = 32 (worst offense in NFL)
```

**Step 3: Determine rating threshold**
```
32 >= 29.68 (VERY_POOR threshold)
→ VERY_POOR tier
base_multiplier = 0.95
```

**Step 4: Apply weight exponent**
```
final_multiplier = 0.95 ^ 0.357 = 0.9826
```

**Step 5: Apply to score**
```
adjusted_score = 65.0 * 0.9826 = 63.87
penalty = 65.0 - 63.87 = -1.13 points
reason = "Team Quality: VERY_POOR (0.98x)"
```

**Result**: Tony Pollard receives -1.13 point penalty for playing on the worst offense in the NFL (TEN, rank 32).

---

## Configuration Reference

### Current Configuration (league_config.json)

```json
{
  "TEAM_QUALITY_SCORING": {
    "THRESHOLDS": {
      "BASE_POSITION": 0,
      "DIRECTION": "DECREASING",
      "STEPS": 1.0475899671798965
    },
    "MULTIPLIERS": {
      "VERY_POOR": 0.95,
      "POOR": 0.975,
      "GOOD": 1.025,
      "EXCELLENT": 1.05
    },
    "WEIGHT": 0.3573337942451747
  }
}
```

### Configuration Fields

| Field | Type | Description | Current Value |
|-------|------|-------------|---------------|
| `THRESHOLDS.BASE_POSITION` | int | Center point for threshold calculation | 0 |
| `THRESHOLDS.DIRECTION` | string | Threshold direction logic | "DECREASING" |
| `THRESHOLDS.STEPS` | float | Step size for threshold boundaries | 1.05 |
| `MULTIPLIERS.VERY_POOR` | float | Multiplier for very poor team | 0.95 |
| `MULTIPLIERS.POOR` | float | Multiplier for poor team | 0.975 |
| `MULTIPLIERS.GOOD` | float | Multiplier for good team | 1.025 |
| `MULTIPLIERS.EXCELLENT` | float | Multiplier for excellent team | 1.05 |
| `WEIGHT` | float | Exponent for multiplier adjustment | 0.357 |

### Threshold Calculation

**Direction**: `DECREASING` (lower rank = better, inverted thresholds)

**Formula**:
```
BASE = 0
STEP = 1.05

EXCELLENT = BASE + (3 * STEP) = 0 + 3.15 ≈ 3.15 (ranks 1-3)
GOOD = BASE + (6 * STEP) = 0 + 6.30 ≈ 6.30 (ranks 4-6)
POOR = BASE + (24.5 * STEP) = 0 + 25.73 ≈ 25.73 (ranks 26+)
VERY_POOR = BASE + (28.3 * STEP) = 0 + 29.68 ≈ 29.68 (ranks 30+)
```

**Calculated Thresholds**:
- EXCELLENT: Ranks 1-3 (elite teams)
- GOOD: Ranks 4-6 (strong teams)
- NEUTRAL: Ranks 7-25 (average teams)
- POOR: Ranks 26-29 (weak teams)
- VERY_POOR: Ranks 30-32 (bottom-tier teams)

### Weight Exponent Impact

**Current Weight**: 0.357

**Multiplier Transformations**:

| Rating | Base Multiplier | Weight Applied | Final Multiplier | Effect |
|--------|----------------|----------------|------------------|--------|
| EXCELLENT | 1.05 | 1.05^0.357 = 1.0175 | +1.75% | ~+1.8 pts on 100 pt player |
| GOOD | 1.025 | 1.025^0.357 = 1.0088 | +0.88% | ~+0.9 pts on 100 pt player |
| NEUTRAL | 1.0 | 1.0^0.357 = 1.0 | 0% | No change |
| POOR | 0.975 | 0.975^0.357 = 0.9912 | -0.88% | ~-0.9 pts on 100 pt player |
| VERY_POOR | 0.95 | 0.95^0.357 = 0.9826 | -1.74% | ~-1.7 pts on 100 pt player |

**Interpretation**: Low weight (0.357) dampens the multiplier effect, making team quality a moderate adjustment factor (±1-2% typical impact).

### Configuration Tuning Guide

**Increasing Effect**:
- Increase `WEIGHT` (e.g., 0.5, 1.0) → amplifies multiplier impact
- Increase `STEPS` (e.g., 2.0, 3.0) → makes thresholds harder to reach (fewer elite/poor teams)
- Increase base multipliers (e.g., EXCELLENT=1.10) → larger adjustments

**Decreasing Effect**:
- Decrease `WEIGHT` (e.g., 0.2, 0.1) → dampens multiplier impact further
- Decrease `STEPS` (e.g., 0.5) → makes thresholds easier to reach (more elite/poor teams)
- Decrease base multipliers (e.g., EXCELLENT=1.02) → smaller adjustments

**Changing Tier Boundaries**:
- Lower `STEPS` → More teams reach EXCELLENT/POOR tiers (e.g., top 5 vs top 3)
- Higher `STEPS` → Fewer teams reach extreme tiers (stricter requirements)

---

## See Also

### Related Metrics
- **[03_player_rating_multiplier.md](03_player_rating_multiplier.md)** - Player-level expert consensus
- **[06_matchup_multiplier.md](06_matchup_multiplier.md)** - Week-specific opponent strength (uses position-specific defense ranks)
- **[07_schedule_multiplier.md](07_schedule_multiplier.md)** - Future opponent difficulty

### Implementation Files
- **`league_helper/util/player_scoring.py:505-519`** - Team quality multiplier application
- **`league_helper/util/ConfigManager.py:305-310, 922-1008`** - Multiplier threshold logic
- **`league_helper/util/TeamDataManager.py`** - Team data loading and caching
- **`player-data-fetcher/espn_client.py:739-867`** - Team statistics fetching and ranking calculation
- **`player-data-fetcher/player_data_exporter.py:452-525`** - Team rankings export to CSV
- **`utils/TeamData.py`** - TeamData model and CSV loader

### Configuration
- **`data/league_config.json`** - Team quality scoring parameters (TEAM_QUALITY_SCORING section)
- **`data/teams.csv`** - Team rankings (offensive_rank, defensive_rank fields)

### Testing
- **`tests/league_helper/util/test_player_scoring.py`** - Team quality multiplier tests
- **`tests/league_helper/util/test_ConfigManager.py`** - Threshold and multiplier configuration tests
- **`tests/league_helper/util/test_TeamDataManager.py`** - Team data loading tests

### Documentation
- **[README.md](README.md)** - Scoring algorithm overview and metric summary
- **[ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture and data flow
- **[CLAUDE.md](../../CLAUDE.md)** - Development guidelines and coding standards

---

**Last Updated**: November 5, 2025
**Current NFL Week**: 10
**Documentation Version**: 1.0
**Code Version**: Week 10, 2025 NFL Season
