# Fantasy Football Helper Scripts - Architecture Documentation

**Author**: Kai Mizuno
**Version**: 2.0 (Post-Refactoring)
**Last Updated**: 2025

---

## Table of Contents

1. [System Overview](#system-overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Architecture](#component-architecture)
4. [Data Flow Architecture](#data-flow-architecture)
5. [Manager Hierarchy](#manager-hierarchy)
6. [Mode System Design](#mode-system-design)
7. [Configuration System](#configuration-system)
8. [Testing Architecture](#testing-architecture)
9. [Extension Points](#extension-points)
10. [Development Guidelines](#development-guidelines)

---

## System Overview

### Purpose

The Fantasy Football Helper Scripts is a comprehensive Python-based system designed to optimize fantasy football decision-making through:

1. **Data-Driven Draft Assistance** - Real-time player recommendations during drafts
2. **Trade Evaluation** - Quantitative analysis of trade impacts on roster strength
3. **Roster Optimization** - Weekly lineup optimization based on matchups and bye weeks
4. **Parameter Optimization** - Simulation-based tuning of scoring algorithms
5. **Data Collection** - Automated fetching of player projections and NFL scores

### Core Principles

1. **Modular Design** - Clear separation of concerns across manager classes
2. **Data-Driven** - All decisions based on statistical projections and historical data
3. **Configurable** - Extensive customization through JSON configuration
4. **Testable** - Comprehensive test coverage (1,811 tests) with 100% unit test pass rate
5. **Extensible** - Well-defined extension points for new features
6. **Error-Resilient** - Robust error handling with context managers and logging

### Key Statistics

- **Lines of Code**: ~15,000+ (excluding tests)
- **Test Coverage**: 1,811 tests (1,786 unit + 25 integration)
- **Modules**: 50+ Python modules
- **Configuration Parameters**: 100+ tunable settings
- **Supported Positions**: QB, RB, WR, TE, K, DST
- **League Simulation**: 10 teams, 17 weeks, 15 rounds per draft

---

## High-Level Architecture

### System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                   USER INTERFACE LAYER                       │
│  (run_league_helper.py, run_simulation.py, CLI scripts)     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  APPLICATION LAYER                           │
│  ┌──────────────────┐  ┌─────────────────────────────────┐ │
│  │ League Helper    │  │   Simulation System             │ │
│  │ Manager          │  │   Manager                       │ │
│  └──────────────────┘  └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   MODE LAYER                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │  Draft   │ │ Roster   │ │  Trade   │ │ Player Data  │  │
│  │  Helper  │ │Optimizer │ │Simulator │ │   Editor     │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │Player Manager│  │Config Manager│  │Team Data Manager│  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATA ACCESS LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ CSV Utils    │  │ Player Fetcher│ │ Scores Fetcher  │  │
│  │              │  │ (ESPN API)    │ │                 │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                                                              │
│  ESPN API Documentation: docs/espn_api_endpoints.md         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATA STORAGE LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ players.csv  │  │league_config │  │teams_week_N.csv │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Primary Components

1. **League Helper System** (`league_helper/`)
   - Interactive draft assistant
   - Roster optimization
   - Trade evaluation
   - Player data modification

2. **Simulation System** (`simulation/`)
   - Parameter optimization via league simulation
   - Parallel execution engine
   - Configuration generation and testing

3. **Data Collection** (`player-data-fetcher/`, `nfl-scores-fetcher/`)
   - Player projection fetching
   - NFL scores and team rankings
   - Automated data updates

4. **Shared Utilities** (`utils/`)
   - Logging infrastructure
   - Error handling
   - CSV I/O operations

---

## Component Architecture

### 1. League Helper Manager (`league_helper/LeagueHelperManager.py`)

**Purpose**: Main controller for the interactive league helper application.

**Responsibilities**:
- Initialize core managers (PlayerManager, ConfigManager, TeamDataManager)
- Present mode selection menu to user
- Route user to selected mode
- Manage data persistence across mode transitions

**Key Methods**:
```python
class LeagueHelperManager:
    def __init__(self, data_folder: Path)
    def run(self) -> None                              # Main loop
    def _initialize_managers(self) -> None             # Setup managers
    def _display_menu(self) -> int                     # Show mode options
    def _route_to_mode(self, selection: int) -> None   # Execute mode
```

**Dependencies**:
- `util/PlayerManager` - Player data and scoring
- `util/ConfigManager` - Configuration access
- `util/TeamDataManager` - NFL team data
- All 4 mode managers

**Data Flow**:
```
User Input → LeagueHelperManager → Mode Manager → Business Logic → Data Layer
```

---

### 2. Player Manager (`league_helper/util/PlayerManager.py`)

**Purpose**: Central hub for player data management and scoring calculations.

**Responsibilities**:
- Load and parse player CSV data
- Calculate player scores using configuration weights
- Apply ADP multipliers, injury penalties, bye week penalties
- Filter and sort players by position
- Track drafted vs available players

**Key Methods**:
```python
class PlayerManager:
    def load_players(self, filepath: Path) -> None
    def get_all_players(self) -> List[FantasyPlayer]
    def get_players_by_position(self, position: str) -> List[FantasyPlayer]
    def calculate_player_score(self, player: FantasyPlayer) -> float
    def mark_player_drafted(self, player_name: str) -> None
    def get_available_players(self) -> List[FantasyPlayer]
```

**Scoring Algorithm**:
```
Total Score = Base Score + Multiplicative Factors + Additive Bonuses/Penalties

Multiplicative Factors (applied to base score):
  - ADP Multiplier (e.g., ×1.20 for top picks)
  - Player Rating Multiplier (e.g., ×1.25 for elite players)
  - Team Quality Multiplier (e.g., ×1.30 for top offenses)

Additive Bonuses/Penalties (added to score):
  - Draft Order Bonus (e.g., +50 pts for primary position)
  - Matchup Bonus: (IMPACT_SCALE × multiplier) - IMPACT_SCALE (e.g., +37.5 pts)
  - Schedule Bonus: (IMPACT_SCALE × multiplier) - IMPACT_SCALE (e.g., +20.0 pts)
  - Bye Week Penalty (median-based exponential)
  - Injury Penalty

Where:
  Base Score = Projected Points (normalized)
  MATCHUP_SCORING.IMPACT_SCALE = 150.0 (default, range: 100-200)
  SCHEDULE_SCORING.IMPACT_SCALE = 80.0 (default, range: 40-120)

Matchup/Schedule Bonus Formula:
  bonus = (IMPACT_SCALE × weighted_multiplier) - IMPACT_SCALE

  Examples (MATCHUP_SCORING.IMPACT_SCALE = 150.0):
    - EXCELLENT (1.25): (150 × 1.25) - 150 = +37.5 pts
    - GOOD (1.10): (150 × 1.10) - 150 = +15.0 pts
    - NEUTRAL (1.0): (150 × 1.0) - 150 = 0.0 pts
    - POOR (0.90): (150 × 0.90) - 150 = -15.0 pts

Bye Week Penalty Calculation:
  1. Collect players with same bye week (same position and different position)
  2. Calculate median weekly points (weeks 1-17) for each player
  3. Sum medians for same-position and different-position groups
  4. Apply exponential scaling: (same_sum ** SAME_POS_BYE_WEIGHT) + (diff_sum ** DIFF_POS_BYE_WEIGHT)

Design Philosophy:
  - Multiplicative factors scale with player value (better for relative comparisons)
  - Additive bonuses provide consistent impact (prevents compounding effects)
  - Matchup/Schedule use additive system to avoid over-valuing elite players in good matchups
```

**Data Structures**:
```python
@dataclass
class FantasyPlayer:
    name: str
    position: str  # QB, RB, WR, TE, K, DST
    team: str
    projected_points: float
    adp: float
    consistency: float
    injury_status: str  # Healthy, Questionable, Doubtful, Out, IR
    bye_week: int
    total_score: float = 0.0
    is_drafted: bool = False
```

---

### 3. Configuration Manager (`league_helper/util/ConfigManager.py`)

**Purpose**: Single source of truth for all configuration parameters.

**Responsibilities**:
- Load league_config.json at initialization
- Provide accessor methods for all config values
- Calculate derived values (ADP multipliers, penalty amounts)
- Validate configuration integrity

**Configuration Schema**:
```json
{
  "config_name": "Configuration Name",
  "description": "Description of configuration purpose",
  "current_nfl_week": 1,

  "scoring": {
    "qb": {"pass_yards": 0.04, "pass_tds": 4, "interceptions": -2},
    "rb": {"rush_yards": 0.1, "rush_tds": 6, "receptions": 1},
    "wr": {"receptions": 1, "rec_yards": 0.1, "rec_tds": 6},
    "te": {"receptions": 1, "rec_yards": 0.1, "rec_tds": 6}
  },

  "thresholds": {
    "projected_points_multiplier": 1.0,
    "adp_multipliers": [[0, 1.5], [50, 1.2], [100, 1.0], [150, 0.8]],
    "consistency_multipliers": {
      "qb": 1.0, "rb": 1.2, "wr": 1.1, "te": 0.9, "k": 0.5, "dst": 0.5
    },
    "injury_penalties": {
      "Healthy": 0, "Questionable": -5, "Doubtful": -15, "Out": -100, "IR": -100
    },
    "bye_week_penalties": {
      "qb": -2, "rb": -3, "wr": -3, "te": -2, "k": -1, "dst": -1
    },
    "team_multipliers": {
      "offense_rank_weight": 0.3,
      "defense_rank_weight": 0.2
    }
  },

  "roster_settings": {
    "lineup_size": 15,
    "qb_slots": 2, "rb_slots": 4, "wr_slots": 4,
    "te_slots": 2, "flex_slots": 2, "k_slots": 1, "dst_slots": 1,
    "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"]
  }
}
```

**Key Methods**:
```python
class ConfigManager:
    def get_adp_multiplier(self, adp: float) -> Tuple[float, int]
    def get_injury_penalty(self, injury_status: str) -> float
    def get_bye_week_penalty(self, same_pos_players: List[FantasyPlayer], diff_pos_players: List[FantasyPlayer]) -> float
    def get_consistency_multiplier(self, position: str) -> float
    def get_team_multiplier(self, team: str, week: int) -> float
    def get_position_with_flex(self, position: str) -> str  # Returns 'FLEX' if eligible
```

---

### 4. Mode System Architecture

Each mode follows a consistent pattern:

```
Mode Manager
    │
    ├─── User Input Handling
    ├─── Business Logic Processing
    ├─── Data Retrieval (via PlayerManager/ConfigManager)
    ├─── Results Display
    └─── Loop Until Exit
```

#### Mode 1: Add to Roster Mode (`add_to_roster_mode/`)

**Purpose**: Provide real-time draft recommendations during fantasy draft.

**Workflow**:
```
1. Calculate scores for all available players
2. Sort by total score (descending)
3. Display top N recommendations with breakdown
4. User selects player to draft
5. Mark player as drafted
6. Update roster state
7. Repeat until draft complete
```

**Key Classes**:
- `AddToRosterModeManager` - Main controller
- `DraftRecommendation` - Recommendation data structure with score breakdown

**Output Format**:
```
TOP RECOMMENDATIONS:
  1. Patrick Mahomes (QB, KC) - Score: 385.2
     Base: 350.0 | ADP Bonus: +25.0 | Consistency: +10.2

  2. Christian McCaffrey (RB, SF) - Score: 380.1
     Base: 320.0 | ADP Bonus: +30.0 | Consistency: +15.1 | Injury: -5.0
```

---

#### Mode 2: Starter Helper Mode (`starter_helper_mode/`)

**Purpose**: Optimize starting lineup for a given week based on matchups.

**Workflow**:
```
1. Load current roster from CSV
2. Get current NFL week from config
3. Calculate weekly scores for each player
4. Apply opponent matchup adjustments
5. Optimize lineup considering position constraints
6. Display recommended starters vs bench
7. Validate lineup meets league rules
```

**Optimization Algorithm**:
```python
def optimize_lineup(roster: List[FantasyPlayer], week: int) -> Dict[str, List[FantasyPlayer]]:
    """
    Greedy optimization with position constraints.

    1. Sort all players by weekly projected points (descending)
    2. Fill required positions (QB, RB, WR, TE, K, DST) first
    3. Fill FLEX slots with highest remaining players
    4. Assign rest to bench
    5. Validate against roster rules
    """
```

**Output Format**:
```
WEEK 5 OPTIMAL LINEUP:
  QB:   Patrick Mahomes (KC) - 28.5 pts (vs DEN - #25 def)
  RB1:  Christian McCaffrey (SF) - 24.2 pts
  RB2:  Austin Ekeler (LAC) - 19.8 pts
  WR1:  Justin Jefferson (MIN) - 22.1 pts
  ...

BENCH:
  RB:   James Conner (ARI) - 14.5 pts (BYE WEEK)
  WR:   Chris Olave (NO) - 16.2 pts (Injury: Questionable)
```

---

#### Mode 3: Trade Simulator Mode (`trade_simulator_mode/`)

**Purpose**: Evaluate potential trades by simulating roster impact.

**Workflow**:
```
1. User selects trade type:
   a. Manual Trade Visualizer (single trade analysis)
   b. Search Trade Opportunities (find best trades)
   c. Full Trade Simulation (all possible trades)

2. For each trade:
   - Calculate current roster strength
   - Simulate trade (swap players)
   - Calculate new roster strength
   - Compute delta (improvement/decline)

3. Rank trades by roster improvement
4. Display top recommendations
```

**Trade Evaluation Metric**:
```
Roster Strength = Sum of (Starter Projected Points × Position Weight)

Trade Value = New Roster Strength - Old Roster Strength

Where:
  Position Weights: QB=1.0, RB=1.2, WR=1.1, TE=0.9, FLEX=1.0
```

**Key Classes**:
- `TradeSimulatorModeManager` - Main controller with 3 sub-modes
- `TradeSimTeam` - Team representation for trade simulation
- `TradeSnapshot` - Before/after comparison structure
- `TradeAnalyzer` - Core trade generation and evaluation engine
- `TradeDisplayHelper` - Display formatting for trade results
- `TradeFileWriter` - File output for trade analysis (txt and Excel formats)

**Output Format**:
```
TRADE ANALYSIS:
  Give: Christian McCaffrey (RB, SF) - 320.0 pts
  Get:  Justin Jefferson (WR, MIN) - 310.0 pts

ROSTER IMPACT:
  Before Trade: 1,425.5 total points
  After Trade:  1,410.3 total points
  Change: -15.2 points (DECLINE)

RECOMMENDATION: REJECT - Weakens overall roster strength
```

**Unequal Trade System Architecture**:

The system supports 9 trade types total: 3 equal (1:1, 2:2, 3:3) and 6 unequal (2:1, 1:2, 3:1, 1:3, 3:2, 2:3).

**Trade Type Selection**:
```python
# TradeAnalyzer.get_trade_combinations()
def get_trade_combinations(
    my_team: TradeSimTeam,
    their_team: TradeSimTeam,
    one_for_one: bool = True,
    two_for_two: bool = False,
    three_for_three: bool = False,
    two_for_one: bool = False,
    one_for_two: bool = False,
    three_for_one: bool = False,
    one_for_three: bool = False,
    three_for_two: bool = False,
    two_for_three: bool = False
) -> List[TradeSnapshot]:
    """
    Generate all valid trades based on selected trade types.

    Unequal trades create roster imbalances that require:
    1. Waiver recommendations (when giving > receiving)
    2. Drop recommendations (when receiving > giving violates MAX_PLAYERS)
    """
```

**Waiver Recommendation System**:

When a trade creates empty roster spots (giving away more players than receiving), the system automatically suggests waiver wire pickups:

```python
# TradeAnalyzer._generate_waiver_recommendations()
def _generate_waiver_recommendations(
    team: TradeSimTeam,
    num_spots: int
) -> List[ScoredPlayer]:
    """
    Generate waiver recommendations to fill empty roster spots.

    Algorithm:
    1. Get available players (drafted=0)
    2. Score each player in context of post-trade roster
    3. Sort by score (descending)
    4. Return top N players to fill spots

    Example: 2:1 trade loses 1 roster spot
             → Recommend best available player from waivers
    """
```

**Drop System for Roster Violations**:

When receiving more players than giving away would violate MAX_PLAYERS (15), the system identifies which players to drop:

```python
# TradeAnalyzer._generate_drop_recommendations()
def _generate_drop_recommendations(
    team: TradeSimTeam,
    num_to_drop: int
) -> List[ScoredPlayer]:
    """
    Identify lowest-value players to drop when roster limit exceeded.

    Algorithm:
    1. Score all players in post-trade roster context
    2. Sort by score (ascending - worst players first)
    3. Return N lowest-scored players to drop
    4. Ensures final roster size = MAX_PLAYERS (15)

    Example: Team has 14 players, 1:2 trade adds net 1 player
             → Final roster = 15 (no drop needed)

             Team has 15 players, 1:2 trade adds net 1 player
             → Final roster = 16 (VIOLATION)
             → Drop lowest-scored player to reach 15
    """
```

**Trade Snapshot Extended Fields**:

```python
@dataclass
class TradeSnapshot:
    # Existing fields (original feature)
    my_new_team: TradeSimTeam           # My team after trade
    their_new_team: TradeSimTeam        # Their team after trade
    my_original_players: List[ScoredPlayer]  # Players I'm giving
    my_new_players: List[ScoredPlayer]       # Players I'm receiving

    # New fields for unequal trades
    waiver_recommendations: List[ScoredPlayer] = None  # Waiver pickups for me
    their_waiver_recommendations: List[ScoredPlayer] = None  # Waiver pickups for opponent
    my_dropped_players: List[ScoredPlayer] = None  # Players I must drop
    their_dropped_players: List[ScoredPlayer] = None  # Players opponent must drop
```

**MIN_TRADE_IMPROVEMENT Enforcement**:

Trade suggestions enforce a 30-point minimum improvement threshold (vs 0 for waiver moves):

```python
# Constants in trade_simulator_mode/__init__.py
MIN_TRADE_IMPROVEMENT = 30.0  # Both teams must improve by ≥30 points
MIN_WAIVER_IMPROVEMENT = 0.0  # Waiver moves only need positive improvement

# Enforcement in TradeAnalyzer
def _filter_trades_by_improvement(
    trades: List[TradeSnapshot],
    my_original_score: float,
    their_original_score: float,
    is_waivers: bool
) -> List[TradeSnapshot]:
    """
    Filter trades to only include mutually beneficial trades above threshold.

    For regular trades: Both teams must improve by ≥ MIN_TRADE_IMPROVEMENT
    For waiver moves: Only my team needs any positive improvement
    """
    threshold = MIN_WAIVER_IMPROVEMENT if is_waivers else MIN_TRADE_IMPROVEMENT

    return [
        trade for trade in trades
        if (trade.my_new_team.team_score - my_original_score >= threshold and
            trade.their_new_team.team_score - their_original_score >= threshold)
    ]
```

**Display and File Output**:

Both `TradeDisplayHelper.display_trade_result()` and `TradeFileWriter` methods include sections for:
- Waiver recommendations (both teams)
- Drop requirements (both teams)
- Score improvements with proper sign handling (+/-)

Example output:
```
Trade with Team ABC
  My improvement: +45.50 pts (New score: 1045.50)
  Their improvement: +32.00 pts (New score: 998.00)
  I give:
    - Player A (RB) - 85.5 pts
    - Player B (WR) - 78.2 pts
  I receive:
    - Player C (QB) - 125.0 pts
  Recommended Waiver Adds (for me):
    - Waiver QB (QB) - 95.0 pts
  Players I Must Drop (to make room):
    - Bench Player (K) - 45.0 pts
```

---

#### Mode 4: Modify Player Data Mode (`modify_player_data_mode/`)

**Purpose**: Manually edit player statistics, projections, or status.

**Workflow**:
```
1. User selects operation:
   - Update existing player data
   - Add new custom player
   - Modify injury status
   - Adjust projections

2. Load current player data
3. Apply modifications
4. Validate changes (type checking, range validation)
5. Persist to CSV
6. Reload PlayerManager to reflect changes
```

**Supported Modifications**:
- Projected points
- ADP (Average Draft Position)
- Consistency rating
- Injury status
- Bye week
- Team assignment

---

### 5. Simulation System Architecture

**Purpose**: Optimize configuration parameters by simulating thousands of fantasy leagues.

**Simulation Flow**:
```
ConfigGenerator → ParallelLeagueRunner → SimulatedLeague → Week
                                              │
                                              ├─ DraftHelperTeam (1)
                                              └─ SimulatedOpponent (9)

Results → ResultsManager → Best Config
```

#### Simulation Manager (`simulation/SimulationManager.py`)

**Three Optimization Modes**:

1. **Single Config Test** (Debugging)
   ```
   - Load baseline config
   - Run N simulations
   - Display results
   - Fast validation
   ```

2. **Full Grid Search** (Exhaustive)
   ```
   - Generate all parameter combinations: (test_values + 1)^6
   - For each config:
       Run N simulations
       Track win rate
   - Return best config
   - SLOW: 7,776 configs @ 5 test values
   ```

3. **Iterative Optimization** (Coordinate Descent)
   ```
   - For each parameter (24 total):
       Generate test values (baseline ± offsets)
       Run N simulations per value
       Select best value
       Update baseline
   - Repeat until convergence
   - FAST: 144 configs @ 6 test values
   ```

**Key Parameters Optimized**:
- `projected_points_multiplier` - Base score weight
- `adp_multiplier_at_0/50/100/150/200` - ADP curve shape (5 params)
- `consistency_multiplier_qb/rb/wr/te/k/dst` - Position bonuses (6 params)
- `injury_penalty_questionable/doubtful/out/ir` - Injury penalties (4 params)
- `SAME_POS_BYE_WEIGHT` / `DIFF_POS_BYE_WEIGHT` - Bye penalty exponential weights (2 params)
- `team_offense_weight/team_defense_weight` - Team strength weights (2 params)

---

#### Parallel League Runner (`simulation/ParallelLeagueRunner.py`)

**Purpose**: Execute multiple league simulations in parallel using thread pool.

**Architecture**:
```python
class ParallelLeagueRunner:
    def __init__(self, max_workers: int = 8):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def run_simulations_for_config(
        self,
        config: Dict,
        num_simulations: int
    ) -> List[SimulationResult]:
        """
        1. Create thread pool with max_workers threads
        2. Submit num_simulations tasks to pool
        3. Each task runs SimulatedLeague.simulate()
        4. Aggregate results
        5. Return win rates and statistics
        """
```

**Performance**:
- Single-threaded: ~30 seconds per simulation
- 8-threaded: ~5-6 seconds per simulation (5-6x speedup)

---

#### Simulated League (`simulation/SimulatedLeague.py`)

**Purpose**: Simulate a complete fantasy league season.

**League Structure**:
```
10 Teams:
  - 1 DraftHelperTeam (uses optimized scoring algorithm)
  - 9 SimulatedOpponents (various strategies):
      * 3 ADP-based drafters
      * 3 Position-need drafters
      * 3 Best-available drafters

Draft: Snake draft, 15 rounds (150 total picks)

Season: 17 weeks, head-to-head matchups
  - Weeks 1-14: Regular season
  - Weeks 15-17: Playoffs (not yet implemented)
```

**Simulation Steps**:
```
1. Initialize 10 teams with empty rosters
2. Run snake draft (15 rounds)
   - Team 1 picks, Team 2 picks, ..., Team 10 picks
   - Team 10 picks, Team 9 picks, ..., Team 1 picks
   - Repeat for 15 rounds
3. For weeks 1-17:
   - Generate matchups (1v2, 3v4, 5v6, 7v8, 9v10)
   - Simulate each week:
       * Each team selects optimal lineup
       * Calculate actual points (from players_actual.csv)
       * Determine winner
   - Update team records
4. Return final record for DraftHelperTeam
```

**Week Simulation** (`simulation/Week.py`):
```python
class Week:
    def simulate(self, team1: FantasyTeam, team2: FantasyTeam) -> Tuple[float, float]:
        """
        1. Team 1 optimizes lineup → Calculate points
        2. Team 2 optimizes lineup → Calculate points
        3. Compare points → Determine winner
        4. Return (team1_points, team2_points)
        """
```

---

### 6. Data Collection Architecture

#### Player Data Fetcher (`player-data-fetcher/`)

**Purpose**: Fetch player projections from external APIs (ESPN, Yahoo, etc.).

**Architecture**:
```
PlayerFetcher
    │
    ├─── ESPN Data Source (primary)
    ├─── Yahoo Data Source (backup)
    └─── Manual CSV Override (user edits)
```

**Workflow**:
```
1. Async HTTP requests to ESPN API
2. Parse JSON responses → PlayerProjection objects
3. Validate data (Pydantic models)
4. Aggregate multiple sources
5. Export to players.csv
6. Backup previous CSV (rolling backups)
```

**Data Validation** (Pydantic):
```python
class PlayerProjection(BaseModel):
    name: str
    team: str
    position: str  # Must be: QB, RB, WR, TE, K, DST
    projected_points: float = Field(ge=0)  # >= 0
    adp: float = Field(ge=0)
    stats: Dict[str, float]
```

---

#### NFL Scores Fetcher (`nfl-scores-fetcher/`)

**Purpose**: Fetch weekly NFL game scores and update team rankings.

**Workflow**:
```
1. Fetch scores for each week (1-17)
2. Calculate team rankings based on:
   - Win/loss record
   - Points scored
   - Points allowed
3. Generate teams_week_N.csv files
4. Update offensive and defensive rankings
```

**Team Rankings Output** (`data/teams_week_N.csv`):
```csv
Team,Rank,Offense_Rank,Defense_Rank,Points_For,Points_Against
KC,1,3,5,28.5,18.2
SF,2,1,12,31.2,22.1
BUF,3,2,8,29.8,19.5
```

---

## Data Flow Architecture

### Draft Workflow Data Flow

```
User Input (draft pick)
    │
    ▼
LeagueHelperManager.run_add_to_roster_mode()
    │
    ▼
AddToRosterModeManager.run()
    │
    ├─── PlayerManager.get_available_players()
    │        │
    │        └─── Reads: data/players.csv
    │
    ├─── ConfigManager (loads config weights)
    │        │
    │        └─── Reads: data/league_config.json
    │
    ├─── Calculate scores for each player
    │        │
    │        └─── PlayerManager.calculate_player_score()
    │                 │
    │                 ├─── Apply ADP multiplier (from config)
    │                 ├─── Apply consistency bonus (from config)
    │                 ├─── Apply injury penalty (from config)
    │                 └─── Apply median-based bye week penalty (from config)
    │
    ├─── Sort by total_score (descending)
    │
    ├─── Display top N recommendations
    │
    ▼
User selects player to draft
    │
    ▼
PlayerManager.mark_player_drafted(player_name)
    │
    └─── Updates: data/drafted_players.csv
```

---

### Simulation Workflow Data Flow

```
User runs: python run_simulation.py iterative --sims 100

RunSimulation CLI
    │
    ▼
SimulationManager.__init__()
    │
    ├─── Loads baseline config from JSON
    ├─── Initializes ParallelLeagueRunner
    └─── Initializes ResultsManager
    │
    ▼
SimulationManager.run_iterative_optimization()
    │
    ├─── For each parameter (24 total):
    │       │
    │       ├─── ConfigGenerator.generate_variations(param, baseline)
    │       │        │
    │       │        └─── Returns: [baseline-2, baseline-1, baseline, baseline+1, baseline+2]
    │       │
    │       ├─── For each variation:
    │       │       │
    │       │       ├─── ParallelLeagueRunner.run_simulations_for_config(config, 100)
    │       │       │        │
    │       │       │        └─── ThreadPoolExecutor submits 100 tasks
    │       │       │                 │
    │       │       │                 ├─── Task 1: SimulatedLeague.simulate(config)
    │       │       │                 │       │
    │       │       │                 │       ├─── Load players from sim_data/players_projected.csv
    │       │       │                 │       ├─── Run snake draft (15 rounds)
    │       │       │                 │       ├─── Simulate 17 weeks
    │       │       │                 │       │      │
    │       │       │                 │       │      └─── Week.simulate(team1, team2)
    │       │       │                 │       │               │
    │       │       │                 │       │               └─── Load actual stats from players_actual.csv
    │       │       │                 │       │
    │       │       │                 │       └─── Return (wins, losses, points)
    │       │       │                 │
    │       │       │                 ├─── Task 2-100: (same as Task 1)
    │       │       │                 │
    │       │       │                 └─── Aggregate results
    │       │       │
    │       │       └─── ResultsManager.record_result(config_id, wins, losses, points)
    │       │
    │       ├─── Select variation with highest win rate
    │       └─── Update baseline for next parameter
    │
    └─── Save optimal config to simulation/simulation_configs/optimal_TIMESTAMP.json
```

---

### Trade Evaluation Data Flow

```
User selects: Trade Simulator Mode → Manual Trade Visualizer

TradeSimulatorModeManager.run_manual_trade()
    │
    ├─── Load user roster from data/teams.csv
    │
    ├─── User inputs:
    │       Give: [Christian McCaffrey]
    │       Get: [Justin Jefferson, Travis Kelce]
    │
    ├─── Create TradeSnapshot:
    │       │
    │       ├─── Current Roster:
    │       │       Calculate total roster strength
    │       │       Sum(starter_projected_points × position_weight)
    │       │
    │       ├─── Simulated Trade:
    │       │       Remove: Christian McCaffrey
    │       │       Add: Justin Jefferson, Travis Kelce
    │       │       Recalculate roster strength
    │       │
    │       └─── Trade Delta:
    │               New Strength - Old Strength
    │
    └─── Display comparison:
            - Before/After roster
            - Point delta
            - Recommendation (Accept/Reject)
```

---

## Manager Hierarchy

### Class Hierarchy

```
LeagueHelperManager
    │
    ├─── PlayerManager
    │       ├─── FantasyPlayer (data class)
    │       └─── Scoring logic
    │
    ├─── ConfigManager
    │       └─── Configuration access
    │
    ├─── TeamDataManager
    │       └─── NFL team rankings
    │
    └─── Mode Managers:
            ├─── AddToRosterModeManager
            │       └─── DraftRecommendation
            │
            ├─── StarterHelperModeManager
            │
            ├─── TradeSimulatorModeManager
            │       ├─── TradeSimTeam
            │       └─── TradeSnapshot
            │
            └─── ModifyPlayerDataModeManager
```

### Manager Initialization Order

```
1. LeagueHelperManager(data_folder)
   │
   ├── ConfigManager(data_folder / "league_config.json")  # Load first
   │
   ├── TeamDataManager(data_folder / "teams_week_*.csv")  # Load team data
   │
   └── PlayerManager(data_folder / "players.csv", config, team_data)
       │
       └── Load players → Calculate scores using config
```

**Rationale**: ConfigManager must load first because PlayerManager needs config values for scoring calculations.

---

### Shared State Management

**Problem**: Multiple modes need access to same player data, but modifications in one mode should be visible in others.

**Solution**: Reference passing - All modes receive same PlayerManager instance.

```python
class LeagueHelperManager:
    def __init__(self, data_folder: Path):
        self.player_manager = PlayerManager(...)  # Single instance
        self.config_manager = ConfigManager(...)

    def run_add_to_roster_mode(self):
        # Pass reference to shared player_manager
        mode = AddToRosterModeManager(
            self.player_manager,  # Same instance
            self.config_manager
        )
        mode.run()

    def run_trade_simulator_mode(self):
        # Same player_manager reference
        mode = TradeSimulatorModeManager(
            self.player_manager,  # Changes visible here
            self.config_manager
        )
        mode.run()
```

**Benefits**:
- Single source of truth for player data
- Modifications persist across modes
- No need for complex state synchronization

---

## Configuration System

### Configuration Loading Sequence

```
1. Application Start
   │
   ├── ConfigManager.__init__(config_path)
   │       │
   │       ├── Read JSON file
   │       ├── Validate schema (required keys present)
   │       ├── Parse nested structures
   │       └── Cache in memory
   │
   └── Provide accessor methods
```

### Configuration Hot-Reloading

**Current**: Configuration loaded once at startup, changes require restart.

**Future Enhancement**: Watch for file changes, reload automatically.

```python
# Potential implementation:
def watch_config_changes(self):
    last_modified = self.config_path.stat().st_mtime
    while True:
        current_modified = self.config_path.stat().st_mtime
        if current_modified > last_modified:
            self.reload_config()
            last_modified = current_modified
        time.sleep(5)
```

---

### Configuration Validation

**JSON Schema Validation** (Future Enhancement):

```python
from jsonschema import validate

CONFIG_SCHEMA = {
    "type": "object",
    "required": ["config_name", "scoring", "thresholds", "roster_settings"],
    "properties": {
        "thresholds": {
            "type": "object",
            "required": ["projected_points_multiplier"],
            "properties": {
                "projected_points_multiplier": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 5
                }
            }
        }
    }
}

def validate_config(config_dict: Dict) -> None:
    validate(instance=config_dict, schema=CONFIG_SCHEMA)
```

---

## Testing Architecture

### Test Organization

```
tests/
├── integration/                      # 25 integration tests
│   ├── test_league_helper_integration.py
│   ├── test_data_fetcher_integration.py
│   └── test_simulation_integration.py
│
├── league_helper/                    # 1,000+ unit tests
│   ├── add_to_roster_mode/
│   │   └── test_AddToRosterModeManager.py
│   ├── starter_helper_mode/
│   │   └── test_StarterHelperModeManager.py
│   ├── trade_simulator_mode/
│   │   ├── test_TradeSimulatorModeManager.py
│   │   ├── test_TradeSimTeam.py
│   │   └── test_TradeSnapshot.py
│   ├── modify_player_data_mode/
│   │   └── test_ModifyPlayerDataModeManager.py
│   └── util/
│       ├── test_PlayerManager.py          # 200+ tests
│       ├── test_ConfigManager.py          # 150+ tests
│       ├── test_FantasyTeam.py
│       ├── test_FantasyPlayer.py
│       └── test_TeamDataManager.py
│
├── simulation/                       # 500+ tests
│   ├── test_SimulationManager.py
│   ├── test_ParallelLeagueRunner.py
│   ├── test_ConfigGenerator.py
│   ├── test_ResultsManager.py
│   ├── test_SimulatedLeague.py
│   ├── test_DraftHelperTeam.py
│   ├── test_SimulatedOpponent.py
│   └── test_Week.py
│
├── player-data-fetcher/              # 100+ tests
├── nfl-scores-fetcher/               # 50+ tests
├── utils/                            # 100+ tests
└── root_scripts/                     # 23 tests
```

---

### Test Patterns

#### Unit Test Pattern (AAA)

```python
class TestPlayerManagerScoring:
    """Test PlayerManager scoring calculations"""

    @pytest.fixture
    def player_manager(self, tmp_path):
        """Create PlayerManager with test data"""
        # ARRANGE - Setup
        config = Mock()
        config.get_adp_multiplier.return_value = (1.5, 95)

        player_manager = PlayerManager(tmp_path, config, None)
        return player_manager

    def test_calculate_score_applies_adp_bonus(self, player_manager):
        """Test that ADP bonus is correctly applied to score"""
        # ARRANGE
        player = FantasyPlayer(
            name="Test Player",
            position="QB",
            projected_points=300.0,
            adp=10.0
        )
        expected_bonus = 1.5  # From config mock

        # ACT
        score = player_manager.calculate_player_score(player)

        # ASSERT
        assert score > 300.0  # Must be higher than base
        assert abs(score - (300.0 * expected_bonus)) < 0.1
```

---

#### Integration Test Pattern

```python
class TestLeagueHelperWorkflow:
    """Test complete workflows across multiple components"""

    @pytest.fixture
    def temp_data_folder(self, tmp_path):
        """Create realistic test data folder"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Create players.csv
        players_csv = data_folder / "players.csv"
        players_csv.write_text("Name,Position,Team,Projected Points,ADP\n"
                              "Patrick Mahomes,QB,KC,350.0,1.2\n")

        # Create league_config.json
        config_json = data_folder / "league_config.json"
        config_json.write_text('{"config_name": "Test"}')

        return data_folder

    def test_draft_player_then_optimize_lineup(self, temp_data_folder):
        """Test drafting a player then optimizing lineup"""
        # ARRANGE
        manager = LeagueHelperManager(temp_data_folder)

        # ACT - Draft player
        manager.player_manager.mark_player_drafted("Patrick Mahomes")

        # ACT - Optimize lineup
        lineup = manager.starter_helper.optimize_lineup(week=1)

        # ASSERT
        assert "Patrick Mahomes" in lineup['starters']
        assert len(lineup['starters']) <= manager.config.get_lineup_size()
```

---

### Test Execution Strategy

**Pre-Commit Testing**:
```bash
# REQUIRED before every commit
python tests/run_all_tests.py

# Exit code 0 = safe to commit
# Exit code 1 = DO NOT COMMIT
```

**Continuous Integration** (Future):
```yaml
# .github/workflows/tests.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: python tests/run_all_tests.py
      - name: Fail if tests fail
        if: failure()
        run: exit 1
```

---

## Extension Points

### Adding a New Mode

**Example**: Add "Waiver Wire Helper" mode

1. **Create mode directory**:
   ```
   league_helper/waiver_wire_mode/
   ├── WaiverWireModeManager.py
   └── WaiverRecommendation.py
   ```

2. **Implement mode manager**:
   ```python
   class WaiverWireModeManager:
       def __init__(
           self,
           player_manager: PlayerManager,
           config_manager: ConfigManager
       ):
           self.player_manager = player_manager
           self.config_manager = config_manager

       def run(self) -> None:
           """Main mode loop"""
           while True:
               self._display_available_players()
               choice = input("Select player to claim: ")
               if choice == 'q':
                   break
               self._claim_player(choice)
   ```

3. **Register in LeagueHelperManager**:
   ```python
   class LeagueHelperManager:
       def _display_menu(self) -> int:
           print("1. Add to Roster")
           print("2. Starter Helper")
           print("3. Trade Simulator")
           print("4. Modify Player Data")
           print("5. Waiver Wire Helper")  # NEW

       def _route_to_mode(self, selection: int):
           if selection == 5:
               self.run_waiver_wire_mode()

       def run_waiver_wire_mode(self):
           mode = WaiverWireModeManager(
               self.player_manager,
               self.config_manager
           )
           mode.run()
   ```

4. **Add tests**:
   ```
   tests/league_helper/waiver_wire_mode/
   └── test_WaiverWireModeManager.py
   ```

5. **Update documentation**:
   - README.md: Add mode description
   - CLAUDE.md: Add to mode list
   - ARCHITECTURE.md: Document mode architecture

---

### Adding a New Data Source

**Example**: Add "FantasyPros" API data source

1. **Create data source module**:
   ```
   player-data-fetcher/data_sources/
   └── fantasypros_client.py
   ```

2. **Implement client**:
   ```python
   class FantasyProsClient:
       def __init__(self, api_key: str):
           self.api_key = api_key
           self.base_url = "https://api.fantasypros.com"

       async def fetch_projections(self) -> List[PlayerProjection]:
           """Fetch player projections from FantasyPros API"""
           async with aiohttp.ClientSession() as session:
               url = f"{self.base_url}/projections"
               async with session.get(url, headers={"Authorization": f"Bearer {self.api_key}"}) as response:
                   data = await response.json()
                   return [self._parse_player(p) for p in data['players']]

       def _parse_player(self, raw: Dict) -> PlayerProjection:
           """Convert API response to PlayerProjection"""
           return PlayerProjection(
               name=raw['name'],
               team=raw['team'],
               position=raw['position'],
               projected_points=raw['points'],
               adp=raw.get('adp', 999),
               stats=raw.get('stats', {})
           )
   ```

3. **Integrate with PlayerFetcher**:
   ```python
   class PlayerFetcher:
       def __init__(self):
           self.espn_client = ESPNClient()
           self.fantasypros_client = FantasyProsClient(api_key=API_KEY)

       async def fetch_all_sources(self) -> List[PlayerProjection]:
           """Fetch from all sources and merge"""
           espn_data = await self.espn_client.fetch_projections()
           fp_data = await self.fantasypros_client.fetch_projections()

           # Merge and deduplicate
           return self._merge_sources([espn_data, fp_data])
   ```

---

### Adding New Configuration Parameters

**Example**: Add "playoff_bonus" for players on playoff teams

1. **Update league_config.json schema**:
   ```json
   {
     "thresholds": {
       "playoff_bonus": 5.0,
       "playoff_teams": ["KC", "SF", "BUF", "PHI"]
     }
   }
   ```

2. **Add accessor to ConfigManager**:
   ```python
   class ConfigManager:
       def get_playoff_bonus(self, team: str) -> float:
           """Get playoff bonus for team"""
           playoff_teams = self.config.get('thresholds', {}).get('playoff_teams', [])
           if team in playoff_teams:
               return self.config.get('thresholds', {}).get('playoff_bonus', 0)
           return 0
   ```

3. **Apply in PlayerManager scoring**:
   ```python
   def calculate_player_score(self, player: FantasyPlayer) -> float:
       score = player.projected_points
       score += self._apply_adp_bonus(player.adp)
       score += self._apply_consistency_bonus(player.consistency)
       score += self.config.get_playoff_bonus(player.team)  # NEW
       return score
   ```

4. **Add to simulation parameters**:
   ```python
   # simulation/ConfigGenerator.py
   OPTIMIZABLE_PARAMS = [
       'projected_points_multiplier',
       'adp_multiplier_at_0',
       'playoff_bonus',  # NEW
       ...
   ]
   ```

5. **Add tests**:
   ```python
   def test_playoff_bonus_applied(player_manager, config):
       config.get_playoff_bonus.return_value = 5.0
       player = FantasyPlayer(name="Test", team="KC", projected_points=300)

       score = player_manager.calculate_player_score(player)

       assert score == 305.0  # 300 + 5 bonus
   ```

---

## Development Guidelines

### Code Review Checklist

Before committing any code, ensure:

- [ ] All unit tests pass (100% pass rate)
- [ ] Integration tests pass where applicable
- [ ] Code follows naming conventions (PascalCase classes, snake_case functions)
- [ ] Type hints added for all public methods
- [ ] Google-style docstrings added
- [ ] No hardcoded paths or magic numbers
- [ ] Error handling with appropriate exceptions
- [ ] Logging at appropriate levels (DEBUG for details, INFO for progress)
- [ ] No duplicate code (DRY principle)
- [ ] No unused imports or dead code
- [ ] CSV operations use csv_utils helpers
- [ ] Path operations use pathlib.Path
- [ ] README.md updated if public API changed
- [ ] CLAUDE.md updated if development workflow changed

---

### Performance Optimization Guidelines

**Profiling**:
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
manager.run_single_config_test()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(20)  # Top 20 slowest functions
```

**Common Bottlenecks**:
1. **CSV I/O**: Use pandas for large files, cache in memory
2. **Player scoring**: Memoize scores if config unchanged
3. **Simulation**: Increase parallel workers (8-16 threads optimal)
4. **Draft recommendations**: Pre-compute scores, don't recalculate every time

**Optimization Patterns**:
```python
# BAD: Recalculate every time
def get_recommendations(self):
    for player in self.player_manager.get_all_players():
        score = self.player_manager.calculate_player_score(player)
        # Do something with score

# GOOD: Calculate once, cache
def get_recommendations(self):
    if not hasattr(self, '_cached_scores'):
        self._cached_scores = {
            player.name: self.player_manager.calculate_player_score(player)
            for player in self.player_manager.get_all_players()
        }

    # Use cached scores
    return sorted(self._cached_scores.items(), key=lambda x: x[1], reverse=True)
```

---

### Debugging Tips

**Enable Verbose Logging**:
```python
# In any run_*.py file
LOGGING_LEVEL = 'DEBUG'  # Change from 'INFO'
LOGGING_TO_FILE = True   # Save to file for analysis
```

**Use pdb for Interactive Debugging**:
```python
import pdb

def problematic_function(player):
    # Set breakpoint
    pdb.set_trace()

    score = calculate_score(player)
    return score

# When breakpoint hit:
#   (Pdb) player.name       # Inspect variables
#   (Pdb) n                 # Next line
#   (Pdb) c                 # Continue
```

**Test Individual Components**:
```bash
# Test just PlayerManager
python -m pytest tests/league_helper/util/test_PlayerManager.py -v

# Test just one test
python -m pytest tests/league_helper/util/test_PlayerManager.py::TestPlayerManagerScoring::test_adp_bonus -v
```

---

## Conclusion

This architecture document provides a comprehensive overview of the Fantasy Football Helper Scripts system. The modular design, clear separation of concerns, and extensive test coverage make the system maintainable, extensible, and reliable.

**Key Takeaways**:
1. **Modularity**: Each component has a single, well-defined responsibility
2. **Configuration-Driven**: Behavior controlled through league_config.json
3. **Data-Driven**: All decisions based on statistical projections
4. **Well-Tested**: 1,811 tests ensure reliability
5. **Extensible**: Clear extension points for new modes, data sources, and parameters

For additional information:
- **User Guide**: See README.md
- **Development Workflow**: See CLAUDE.md
- **Testing Guidelines**: See tests/README.md
- **Update Protocol**: See rules.txt

---

**Document Version**: 2.0
**Last Updated**: 2025
**Maintained By**: Kai Mizuno
