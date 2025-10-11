# Simulation Implementation TODO

## 📋 Project Overview
Implement a comprehensive fantasy football draft and season simulation system to optimize configuration parameters through automated testing. The system will run 46,656 different parameter combinations (6^6), with 100 league simulations per configuration, to find the optimal settings that maximize DraftHelper win rate.

---

## 🗂️ Project Structure & File Locations

### Existing Files:
```
simulation/
├── SimulationManager.py          # Main orchestration (stub with config constants)
├── DraftHelperTeam.py            # Stub class with PlayerManager imports
├── SimulatedOpponent.py          # Stub class with PlayerManager imports
├── SIMULATION_QUESTIONS.md       # Answered Q&A document
├── SIMULATION_TODO.md            # This file
├── sim_data/                     # Real 2024 NFL season data
│   ├── players_projected.csv     # Projected fantasy points (what teams see)
│   ├── players_actual.csv        # Actual performance (ground truth)
│   ├── teams_week_0.csv          # Team rankings week 0
│   ├── teams_week_1.csv          # Team rankings week 1
│   ├── ...                       # (teams_week_2 through teams_week_17)
│   └── teams_week_18.csv         # Team rankings week 18
└── simulated_configs/
    └── optimal_2025-10-02_15-29-14.json.json  # Baseline config

league_helper/                    # Existing fantasy helper system (DO NOT MODIFY)
├── add_to_roster_mode/
│   └── AddToRosterModeManager.py # Draft assistant with intelligent recommendations
├── starter_helper_mode/
│   └── StarterHelperModeManager.py # Weekly lineup optimizer
└── util/
    ├── ConfigManager.py          # Configuration management
    ├── PlayerManager.py          # Player scoring and data management
    ├── TeamDataManager.py        # Team rankings and matchup data
    ├── FantasyTeam.py            # Roster management
    └── ScoredPlayer.py           # Wrapper for scored player data
```

### Files to Create:
```
simulation/
├── Week.py                       # Weekly matchup and scoring
├── SimulatedLeague.py            # Complete league simulation
├── ConfigGenerator.py            # Parameter combination generator
├── ConfigPerformance.py          # Performance tracking per config
├── ResultsManager.py             # Results aggregation and comparison
├── ParallelLeagueRunner.py       # Multi-threaded league execution
├── manual_simulation.py          # Single manual simulation for testing
├── run_simulation.py             # Main entry point
├── utils/
│   └── scheduler.py              # Round-robin scheduling
└── tests/                        # Unit tests for all components
    ├── test_DraftHelperTeam.py
    ├── test_SimulatedOpponent.py
    ├── test_Week.py
    ├── test_SimulatedLeague.py
    ├── test_RoundRobinScheduler.py
    ├── test_ConfigGenerator.py
    ├── test_ConfigPerformance.py
    ├── test_ResultsManager.py
    ├── test_ParallelLeagueRunner.py
    ├── test_ProgressTracker.py
    └── test_SimulationManager.py
```

---

## 📊 Data File Formats & Structures

### players_projected.csv & players_actual.csv
**Location:** `simulation/sim_data/`
**Structure:** (Both files have identical structure, different values)
```csv
id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,average_draft_position,player_rating,week_1_points,week_2_points,...,week_17_points
4374302,Amon-Ra St. Brown,DET,WR,8,219.69,ACTIVE,0,0,10.573511293634496,96.4,14.69,14.74,...,12.97
```

**Key Fields:**
- `id` (int): Unique player identifier
- `drafted` (int): 0=available, 1=drafted by opponent, 2=drafted by user (simulation uses 0 and 1)
- `fantasy_points` (float): Total seasonal projection
- `week_N_points` (float): Weekly projections (N=1 to 17)
- `bye_week` (int): Week number when team has bye (0 points that week)

### teams_week_N.csv
**Location:** `simulation/sim_data/teams_week_0.csv` through `teams_week_18.csv`
**Structure:**
```csv
team,offensive_rank,defensive_rank,opponent
ARI,21,18,NO
BAL,5,28,BUF
```

**Key Fields:**
- `team` (str): 3-letter team abbreviation
- `offensive_rank` (int): 1-32, lower is better
- `defensive_rank` (int): 1-32, lower is better
- `opponent` (str): Current opponent team abbreviation

**Usage:** Rankings change week-to-week (e.g., DET offense: #3 week 1 → #1 week 17)

---

## 🔌 Integration with Existing League Helper System

### Import Structure Pattern
```python
import sys
from pathlib import Path

# Add league_helper to path
sys.path.append(str(Path(__file__).parent.parent / "league_helper"))
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.add_to_roster_mode.AddToRosterModeManager import AddToRosterModeManager
from league_helper.starter_helper_mode.StarterHelperModeManager import StarterHelperModeManager

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.FantasyPlayer import FantasyPlayer
```

### PlayerManager API
**Constructor:**
```python
PlayerManager(data_folder: Path, config: ConfigManager, team_data_manager: TeamDataManager)
```

**Key Methods:**
```python
# Load player data from CSV
player_manager.load_players_from_csv()  # Automatically called in __init__

# Access player data
player_manager.players: List[FantasyPlayer]  # All players
player_manager.max_projection: float  # Used for normalization

# Scoring
scored_player: ScoredPlayer = player_manager.score_player(
    player: FantasyPlayer,
    use_weekly_projection=False,  # True for weekly lineup decisions
    adp=True,                      # Use ADP multiplier (draft only)
    player_rating=True,            # Use player rating multiplier (draft only)
    team_quality=True,             # Use team quality multiplier (draft only)
    consistency=True,              # Use consistency multiplier
    matchup=False,                 # Use matchup multiplier (weekly only)
    draft_round=-1,                # Round number (0-14) for draft order bonus, -1 to disable
    bye=True,                      # Apply bye week penalty
    injury=True                    # Apply injury penalty
)

# Weekly projections
original_points, weighted_points = player_manager.get_weekly_projection(player, week=5)

# Roster operations
player_manager.draft_player(player)  # Adds to roster, sets player.drafted = 2
player_manager.update_players_file() # Saves changes back to CSV
```

**CRITICAL:** Each PlayerManager loads from `data_folder / 'players.csv'`. For simulation:
- Use `sim_data/players_projected.csv` for one PlayerManager
- Use `sim_data/players_actual.csv` for another PlayerManager
- Must create **separate PlayerManager instances for each team** with fresh CSV data

### ConfigManager API
**Constructor:**
```python
ConfigManager(data_folder: Path)  # Loads from data_folder / 'league_config.json'
```

**Key Attributes:**
```python
config.current_nfl_week: int              # Current NFL week (1-17)
config.nfl_season: int                    # Season year (2024)
config.nfl_scoring_format: str            # 'ppr', 'std', or 'half'
config.normalization_max_scale: float     # Max scale for normalization
config.base_bye_penalty: float            # Base bye week penalty
config.draft_order: List[Dict[str, str]]  # Draft position priorities per round
config.draft_order_bonuses: Dict          # PRIMARY and SECONDARY bonuses
```

**Key Methods:**
```python
# Get multipliers (returns Tuple[float, str] = (multiplier, rating_label))
config.get_adp_multiplier(adp_val)
config.get_player_rating_multiplier(rating)
config.get_team_quality_multiplier(quality_rank)
config.get_consistency_multiplier(cv_value)
config.get_matchup_multiplier(matchup_score)

# Get bonuses
config.get_draft_order_bonus(position: str, draft_round: int) -> Tuple[float, str]
config.get_bye_week_penalty(num_matching_byes: int) -> float
config.get_injury_penalty(risk_level: str) -> float
```

**For Simulation:** Create ConfigManager by:
1. Generate new config JSON in memory (dict)
2. Save to temporary file in `sim_data/`
3. Initialize ConfigManager(Path("./sim_data"))
4. Each league simulation gets its own ConfigManager instance

### AddToRosterModeManager API
**Constructor:**
```python
AddToRosterModeManager(
    config: ConfigManager,
    player_manager: PlayerManager,
    team_data_manager: TeamDataManager
)
```

**Key Method for Draft Recommendations:**
```python
recommendations: List[ScoredPlayer] = add_to_roster_mgr.get_recommendations()
# Returns top N players (N = Constants.RECOMMENDATION_COUNT = 10)
# Automatically uses current round from roster size
# Applies draft order bonuses based on config.draft_order
```

**How DraftHelperTeam Uses It:**
```python
# In DraftHelperTeam.get_draft_recommendation():
self.add_to_roster_mgr = AddToRosterModeManager(self.config, self.projected_pm, self.team_data_mgr)
recommendations = self.add_to_roster_mgr.get_recommendations()
top_pick = recommendations[0]  # Always pick #1 recommendation (no human error)
return top_pick.player  # Returns FantasyPlayer object
```

### StarterHelperModeManager API
**Constructor:**
```python
StarterHelperModeManager(
    config: ConfigManager,
    player_manager: PlayerManager,
    team_data_manager: TeamDataManager
)
```

**Key Method for Weekly Lineups:**
```python
lineup: OptimalLineup = starter_helper_mgr.optimize_lineup()

# OptimalLineup has these attributes:
lineup.qb: Optional[ScoredPlayer]
lineup.rb1: Optional[ScoredPlayer]
lineup.rb2: Optional[ScoredPlayer]
lineup.wr1: Optional[ScoredPlayer]
lineup.wr2: Optional[ScoredPlayer]
lineup.te: Optional[ScoredPlayer]
lineup.flex: Optional[ScoredPlayer]  # Can be RB, WR, or TE
lineup.k: Optional[ScoredPlayer]
lineup.dst: Optional[ScoredPlayer]
lineup.bench: List[ScoredPlayer]
lineup.total_projected_points: float
```

**How DraftHelperTeam Uses It:**
```python
# In DraftHelperTeam.set_weekly_lineup(week):
# Update team data manager to current week's team rankings
self.team_data_mgr.load_team_data(week)  # Loads teams_week_N.csv

# Update config week
self.config.current_nfl_week = week

# Get optimal lineup using weekly projections
self.starter_helper_mgr = StarterHelperModeManager(self.config, self.projected_pm, self.team_data_mgr)
lineup = self.starter_helper_mgr.optimize_lineup()

# Calculate actual points using actual_pm
total_actual_points = 0.0
for starter in lineup.get_all_starters():
    if starter:
        actual_weekly_points, _ = self.actual_pm.get_weekly_projection(starter.player, week)
        total_actual_points += actual_weekly_points

return total_actual_points
```

### TeamDataManager API
**Constructor:**
```python
TeamDataManager(data_folder: Path)  # Loads from data_folder / 'teams.csv'
```

**Key Methods:**
```python
team_data_mgr.get_team_offensive_rank(team: str) -> int
team_data_mgr.get_team_defensive_rank(team: str) -> int
team_data_mgr.get_rank_difference(team: str, is_defense: bool) -> int  # Matchup score
```

**For Simulation:** Load different weeks by:
```python
# Option 1: Modify data_folder based on week
team_data_mgr = TeamDataManager(Path(f"./sim_data/week_{week}"))

# Option 2: Copy teams_week_N.csv to teams.csv before loading
import shutil
shutil.copy(f"./sim_data/teams_week_{week}.csv", "./sim_data/teams.csv")
team_data_mgr = TeamDataManager(Path("./sim_data"))
```

---

## 🎯 Critical Implementation Details from Q&A

### Draft Simulation Requirements
1. **Snake Draft Order:**
   - Standard: Round 1 (1→10), Round 2 (10→1), Round 3 (1→10), etc.
   - 15 rounds total (150 picks for 10 teams)
   - Randomize initial draft position order at league start

2. **Team Strategies:**
   - `'draft_helper'` (1 team): Uses AddToRosterModeManager, ALWAYS picks #1 recommendation (no human error)
   - `'adp_aggressive'` (2 teams): Pick lowest ADP available
   - `'projected_points_aggressive'` (2 teams): Pick highest projected points
   - `'adp_with_draft_order'` (2 teams): Use ADP but respect position priorities from config.draft_order
   - `'projected_points_with_draft_order'` (3 teams): Use projected points with position priorities

3. **Human Error for SimulatedOpponent Only:**
   - 20% chance to pick from top 5 options instead of #1
   - Apply using: `if random.random() < 0.2: pick from random.choice(recommendations[:5])`
   - DraftHelperTeam is PERFECT (no error)

4. **Draft Synchronization:**
   - When ANY team drafts a player: `player.drafted = 1` in ALL teams' PlayerManager instances
   - Must update both projected AND actual PlayerManagers for each team
   - Implementation: After each pick, broadcast to all teams to mark that player as drafted

### Season Simulation Requirements
1. **Matchup Scheduling:**
   - Double round-robin: Each team plays each opponent twice
   - 10 teams = 9 opponents × 2 = 18 games
   - Fit into 17 weeks (one team short 1 game, or handle overflow)

2. **Weekly Scoring:**
   - **DraftHelperTeam:** Use StarterHelperModeManager with weekly projections to set lineup
   - **SimulatedOpponent:** Select starters by highest weekly projected points per position
     - Same position counts as StarterHelper (1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX, 1 K, 1 DST)
     - NO optimization, just highest projected points
   - **Actual Scoring:** Both teams score based on `players_actual.csv` weekly points
   - **Winner:** Higher total actual points wins, ties = loss for both

3. **Win Rate Calculation:**
   - Track all weekly matchup results across ALL simulations
   - Win rate = total_wins / total_games (across all 100 simulations per config)
   - Also track: total_points_scored (used as tiebreaker)

### Configuration Parameter Testing
1. **Parameters to Vary (6 total):**
   - `NORMALIZATION_MAX_SCALE`: ±20 from optimal, bounded [60, 140]
   - `BASE_BYE_PENALTY`: ±10 from optimal, bounded [0, 40]
   - `DRAFT_ORDER_BONUSES.PRIMARY`: ±20 from optimal, bounded [25, 100]
   - `DRAFT_ORDER_BONUSES.SECONDARY`: ±20 from optimal, bounded [25, 75]
   - `POSITIVE_MULTIPLIER`: ±0.1 from optimal, bounded [1.0, 1.3]
   - `NEGATIVE_MULTIPLIER`: ±0.1 from optimal, bounded [0.7, 1.0]

2. **Value Generation:**
   - 6 values per parameter: optimal value + 5 random values within range
   - Total combinations: 6^6 = 46,656 configurations

3. **Multiplier Application (CRITICAL):**
   - `POSITIVE_MULTIPLIER` applies to GOOD and EXCELLENT in all sections
   - `NEGATIVE_MULTIPLIER` applies to POOR and VERY_POOR in all sections
   - **For each config's POSITIVE_MULTIPLIER value:**
     - ADP section: Generate GOOD multiplier (e.g., 1.12), Generate EXCELLENT multiplier (e.g., 1.18) - both within POSITIVE_MULTIPLIER constraints
     - Player Rating section: Re-generate new GOOD (e.g., 1.14), new EXCELLENT (e.g., 1.16)
     - Team Quality section: Re-generate new GOOD, new EXCELLENT
     - Consistency section: Re-generate new GOOD, new EXCELLENT
     - Matchup section: Re-generate new GOOD, new EXCELLENT
   - **Same for NEGATIVE_MULTIPLIER with POOR and VERY_POOR**
   - THRESHOLDS are NOT varied (only MULTIPLIERS)

4. **Optimization Flow:**
   - `NUMBER_OF_RUNS = 100`: Number of complete optimization cycles
   - `SIMULATIONS_PER_CONFIG = 100`: Number of league simulations per config
   - **One Optimization Cycle:**
     1. Load baseline config (or previous optimal config)
     2. Generate 46,656 parameter combinations
     3. For each combination: Run 100 league simulations
     4. Identify best config (highest win rate, points as tiebreaker)
     5. Save optimal config to `simulated_configs/optimal_YYYY-MM-DD_HH-MM-SS.json`
   - **Next Cycle:** Use previous optimal config as new baseline

---

## 🎯 Implementation Phases

### Phase 1: Core Data Structures & Models (Manual Testing Foundation)
Build the fundamental classes and data structures needed for a single manual simulation.

#### 1.1 Enhanced Team Classes
- [ ] **DraftHelperTeam class** (simulation/DraftHelperTeam.py)
  - [ ] Constructor: `__init__(self, projected_pm: PlayerManager, actual_pm: PlayerManager, config: ConfigManager, team_data_mgr: TeamDataManager)`
  - [ ] Store: `self.roster: List[FantasyPlayer]`, `self.projected_pm`, `self.actual_pm`, `self.config`, `self.team_data_mgr`
  - [ ] Initialize managers: `self.add_to_roster_mgr = None`, `self.starter_helper_mgr = None` (created on-demand)
  - [ ] Method: `draft_player(player: FantasyPlayer)` - adds to roster, marks as drafted in both PMs
  - [ ] Method: `get_draft_recommendation() -> FantasyPlayer` - uses AddToRosterModeManager.get_recommendations()[0]
  - [ ] Method: `set_weekly_lineup(week: int) -> float` - uses StarterHelperModeManager, returns actual points scored
  - [ ] Method: `mark_player_drafted(player_id: int)` - sets player.drafted = 1 in both PlayerManagers

- [ ] **SimulatedOpponent class** (simulation/SimulatedOpponent.py)
  - [ ] Constructor: `__init__(self, projected_pm: PlayerManager, actual_pm: PlayerManager, config: ConfigManager, team_data_mgr: TeamDataManager, strategy: str)`
  - [ ] Store: `self.roster: List[FantasyPlayer]`, `self.projected_pm`, `self.actual_pm`, `self.config`, `self.team_data_mgr`, `self.strategy`
  - [ ] Method: `draft_player(player: FantasyPlayer)` - adds to roster, marks as drafted in both PMs
  - [ ] Method: `get_draft_recommendation() -> FantasyPlayer` - implements strategy-based drafting:
    - [ ] `'adp_aggressive'`: Sort by ADP (ascending), pick lowest available
    - [ ] `'projected_points_aggressive'`: Sort by fantasy_points (descending), pick highest
    - [ ] `'adp_with_draft_order'`: Score by ADP + draft_order_bonus, pick best
    - [ ] `'projected_points_with_draft_order'`: Score by points + draft_order_bonus, pick best
  - [ ] Method: `apply_human_error(recommendations: List[FantasyPlayer]) -> FantasyPlayer`
    - [ ] 20% chance: return random.choice(recommendations[:5])
    - [ ] 80% chance: return recommendations[0]
  - [ ] Method: `set_weekly_lineup(week: int) -> float` - selects highest weekly projected points per position, returns actual points
  - [ ] Method: `mark_player_drafted(player_id: int)` - sets player.drafted = 1 in both PlayerManagers

#### 1.2 League Simulation Classes
- [ ] **Week class** (simulation/Week.py)
  - [ ] Constructor: `__init__(self, week_number: int, matchups: List[Tuple[Team, Team]])`
  - [ ] Method: `simulate_week() -> Dict[Team, Tuple[float, float, bool]]`
    - [ ] For each matchup: team1.set_weekly_lineup(week), team2.set_weekly_lineup(week)
    - [ ] Compare scores, determine winner (tie = both lose)
    - [ ] Return {team: (points_scored, points_against, won)}

- [ ] **SimulatedLeague class** (simulation/SimulatedLeague.py)
  - [ ] Constructor: `__init__(self, config_dict: dict, data_folder: Path = Path("./sim_data"))`
  - [ ] Method: `initialize_teams()` - creates 1 DraftHelperTeam + 9 SimulatedOpponent with strategy distribution
  - [ ] Method: `load_player_data()` - creates separate PlayerManager instances for each team
    - [ ] Each team gets: `PlayerManager(data_folder, config, team_data_mgr)` for projected
    - [ ] Each team gets: `PlayerManager(data_folder.parent / "sim_data_actual", config, team_data_mgr)` for actual
    - [ ] OR: Copy CSVs to separate temp folders per team
  - [ ] Method: `run_draft()` - executes snake draft:
    - [ ] Randomize initial draft order (list of 10 teams)
    - [ ] For round in range(15):
      - [ ] order = draft_order if round % 2 == 0 else reversed(draft_order)
      - [ ] For team in order:
        - [ ] player = team.get_draft_recommendation()
        - [ ] team.draft_player(player)
        - [ ] Broadcast: for other_team in all_teams: other_team.mark_player_drafted(player.id)
  - [ ] Method: `run_season()` - simulates 17 weeks using round-robin schedule
  - [ ] Method: `get_draft_helper_results() -> Tuple[int, int, float]` - returns (wins, losses, total_points)

#### 1.3 Round-Robin Scheduling
- [ ] **RoundRobinScheduler utility** (simulation/utils/scheduler.py)
  - [ ] Method: `generate_double_round_robin(teams: List) -> List[List[Tuple]]`
    - [ ] Circle method algorithm for 10 teams
    - [ ] Each team plays every other team twice over 17-18 weeks
    - [ ] Return: List[week_matchups] where week_matchups = List[(team1, team2)]

#### 1.4 Unit Tests for Core Components
- [ ] **test_DraftHelperTeam.py**
  - [ ] Test: Draft recommendation uses AddToRosterModeManager and picks #1
  - [ ] Test: Weekly lineup uses StarterHelperModeManager
  - [ ] Test: Drafted player synchronization across PlayerManagers

- [ ] **test_SimulatedOpponent.py**
  - [ ] Test: Each strategy type returns correct player
  - [ ] Test: Human error rate (mock random.random())
  - [ ] Test: Weekly lineup picks highest projected points

- [ ] **test_Week.py & test_SimulatedLeague.py & test_RoundRobinScheduler.py**
  - [ ] Test matchup generation, simulation, results
  - [ ] Test draft synchronization (no duplicate picks)
  - [ ] Test season flow (17 weeks, all matchups)

### Phase 2: Configuration Management & Parameter Generation
Build the system to generate and manage different configuration combinations.

#### 2.1 Parameter Generation System
- [ ] **ConfigGenerator class** (simulation/ConfigGenerator.py)
  - [ ] Method: `load_baseline_config(json_path: Path) -> dict`
  - [ ] Method: `generate_parameter_values(param_name: str, optimal_val: float, range_val: float, min_val: float, max_val: float) -> List[float]`
    - [ ] Return: [optimal_val] + [5 random values in [optimal±range] bounded by [min, max]]
  - [ ] Method: `generate_all_combinations() -> List[dict]`
    - [ ] Use itertools.product() to create 6^6 = 46,656 combinations
    - [ ] Each combination = dict with 6 parameter values
  - [ ] Method: `create_config_dict(combination: dict, baseline: dict) -> dict`
    - [ ] Copy baseline config
    - [ ] Update varied parameters
    - [ ] Apply multipliers to all scoring sections
  - [ ] Method: `apply_multipliers(config: dict, pos_mult: float, neg_mult: float) -> dict`
    - [ ] For each section (ADP, Player Rating, Team Quality, Consistency, Matchup):
      - [ ] Generate GOOD multiplier: random.uniform(pos_mult - 0.05, pos_mult + 0.05)
      - [ ] Generate EXCELLENT multiplier: random.uniform(pos_mult - 0.05, pos_mult + 0.05) (different from GOOD)
      - [ ] Generate POOR multiplier: random.uniform(neg_mult - 0.05, neg_mult + 0.05)
      - [ ] Generate VERY_POOR multiplier: random.uniform(neg_mult - 0.05, neg_mult + 0.05) (different from POOR)

#### 2.2 Configuration Testing
- [ ] **test_ConfigGenerator.py**
  - [ ] Test: 6 values per parameter (optimal + 5 random)
  - [ ] Test: Values within bounds
  - [ ] Test: Exactly 46,656 combinations generated
  - [ ] Test: Multipliers applied correctly (GOOD ≠ EXCELLENT, POOR ≠ VERY_POOR)

### Phase 3: Single Manual Simulation (Testing & Validation)
Run and validate a complete single league simulation before automation.

#### 3.1 Manual Simulation Script
- [ ] **manual_simulation.py** (simulation/manual_simulation.py)
  - [ ] Load baseline config: `simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json`
  - [ ] Create SimulatedLeague with config
  - [ ] Run draft and print: which team (strategy) got which players
  - [ ] Run season and print: weekly matchups, scores, winners
  - [ ] Print final standings: wins/losses/total_points for each team
  - [ ] Validate: DraftHelper team uses correct managers

#### 3.2 Manual Simulation Validation
- [ ] Run manual_simulation.py and verify:
  - [ ] Draft completes (150 picks, 15 per team)
  - [ ] Top ADP players go early
  - [ ] All 17 weeks simulate
  - [ ] Final results realistic

### Phase 4: Performance Metrics & Result Tracking
Build the system to track and compare configuration performance.

#### 4.1 Results Tracking Classes
- [ ] **ConfigPerformance class** (simulation/ConfigPerformance.py)
  - [ ] Store: config_dict, total_wins, total_games, total_points
  - [ ] Method: `add_league_result(wins: int, losses: int, points: float)`
  - [ ] Method: `get_win_rate() -> float`
  - [ ] Method: `get_avg_points_per_league() -> float`
  - [ ] Method: `compare_to(other: ConfigPerformance) -> int` (1 if self better, -1 if other better, 0 if tie)

- [ ] **ResultsManager class** (simulation/ResultsManager.py)
  - [ ] Store: Dict[str, ConfigPerformance]
  - [ ] Method: `record_result(config_id: str, wins: int, losses: int, points: float)`
  - [ ] Method: `get_best_config() -> ConfigPerformance` (highest win rate, points tiebreaker)
  - [ ] Method: `save_optimal_config(output_path: Path)` (save as JSON with timestamp)

### Phase 5: Parallel Execution & Progress Tracking
Implement parallelization and progress monitoring for large-scale simulations.

#### 5.1 Parallel League Runner
- [ ] **ParallelLeagueRunner class** (simulation/ParallelLeagueRunner.py)
  - [ ] Use: `concurrent.futures.ThreadPoolExecutor`
  - [ ] Method: `run_config_batch(config_dict: dict, num_simulations: int) -> Tuple[int, int, float]`
    - [ ] Each thread runs: SimulatedLeague(config_dict).run_draft().run_season().get_draft_helper_results()
    - [ ] Return: (total_wins, total_losses, total_points) aggregated across all simulations

#### 5.2 Progress Tracking
- [ ] **ProgressTracker class** (simulation/ProgressTracker.py)
  - [ ] Track: leagues_completed, total_leagues, start_time
  - [ ] Method: `update(count: int)` - increment progress
  - [ ] Method: `estimate_time_remaining() -> str` - calculate ETA
  - [ ] Method: `print_progress()` - display progress bar

### Phase 6: Full Simulation Manager (Automation)
Tie everything together into the main simulation orchestration system.

#### 6.1 SimulationManager Implementation
- [ ] **SimulationManager class** (simulation/SimulationManager.py)
  - [ ] Method: `run_optimization_cycle(baseline_config_path: Path) -> dict`
    - [ ] Load baseline config
    - [ ] Generate 46,656 combinations
    - [ ] For each config: run 100 simulations (parallelized)
    - [ ] Get best config, save to JSON
    - [ ] Return optimal config dict
  - [ ] Method: `run_n_cycles(n: int)`
    - [ ] Cycle 1: Use baseline config
    - [ ] Cycle 2-N: Use previous optimal config

#### 6.2 Main Entry Point
- [ ] **run_simulation.py** (simulation/run_simulation.py)
  - [ ] CLI args: --runs, --threads, --simulations-per-config
  - [ ] Initialize SimulationManager
  - [ ] Run cycles
  - [ ] Print results

### Phase 7: Optimization & Documentation
Final refinements, performance optimization, and documentation.

#### 7.1 Performance Optimization
- [ ] Profile simulation performance
- [ ] Optimize PlayerManager CSV loading
- [ ] Consider config reduction strategies

#### 7.2 Documentation
- [ ] Update simulation/README.md with architecture and usage
- [ ] Add docstrings to all classes
- [ ] Create example output files

---

## 📊 Implementation Summary

### Key Numbers:
- **Parameters varied**: 6 (NORMALIZATION_MAX_SCALE, BASE_BYE_PENALTY, PRIMARY_BONUS, SECONDARY_BONUS, POSITIVE_MULT, NEGATIVE_MULT)
- **Values per parameter**: 6 (baseline + 5 random)
- **Total configurations**: 6^6 = 46,656
- **Simulations per config**: 100 leagues
- **Total leagues per run**: 4,665,600
- **Weeks per league**: 17
- **Games per league**: ~170 (10 teams × 17 weeks / 2)

### Architecture:
- **DraftHelperTeam**: Uses AddToRosterMode + StarterHelper (our system under test)
- **SimulatedOpponent**: Uses strategy-based drafting + simple projected-points lineup setting
- **SimulatedLeague**: Manages 10 teams through draft + 17-week season
- **ConfigGenerator**: Creates all parameter combinations
- **ResultsManager**: Tracks performance, identifies optimal config
- **ParallelLeagueRunner**: Parallelizes league simulations
- **SimulationManager**: Orchestrates full optimization cycles

### Testing Strategy:
1. Unit test each component individually
2. Manual single-league validation
3. Small-scale integration test (9 configs, 5 sims each)
4. Full-scale production run (46,656 configs, 100 sims each)

---

## 🚀 Getting Started

**Current Status**: Phase 1 - Core Data Structures (Not Started)

**Next Steps**:
1. Implement DraftHelperTeam class with draft and lineup logic
2. Implement SimulatedOpponent with strategy-based drafting
3. Create unit tests for both team classes
4. Implement Week class and round-robin scheduler
5. Implement SimulatedLeague to tie it all together

**Estimated Timeline** (with testing):
- Phase 1: 2-3 days (core classes + tests)
- Phase 2: 1 day (config generation)
- Phase 3: 1 day (manual simulation validation)
- Phase 4: 1 day (performance tracking)
- Phase 5: 1-2 days (parallelization)
- Phase 6: 1 day (full automation)
- Phase 7: 1 day (optimization + docs)

**Total**: ~8-10 days of development + testing
