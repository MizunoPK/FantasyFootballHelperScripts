# Fantasy Football Helper Scripts

A comprehensive Python-based system for optimizing fantasy football draft decisions, evaluating trades, and simulating league outcomes through advanced statistical modeling and parallel simulation.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Main Applications](#main-applications)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Testing](#testing)
- [Development Guidelines](#development-guidelines)
- [Data Files](#data-files)

## Overview

The Fantasy Football Helper Scripts provide a complete suite of tools for serious fantasy football managers:

1. **League Helper**: Interactive draft assistant with real-time player recommendations and trade evaluation
2. **Simulation System**: Parallel league simulation engine for parameter optimization (tests thousands of configurations)
3. **Data Fetchers**: Automated collection of player projections and NFL scores

The system uses projected and actual player statistics, team rankings, bye weeks, injury risk, consistency metrics, and configurable scoring parameters to provide data-driven recommendations.

## Key Features

- **Draft Assistant**: Real-time player recommendations using advanced scoring algorithms
- **Trade Simulator**: Evaluate trades by simulating their impact on your roster strength
- **Roster Optimizer**: Optimize starting lineup each week based on matchups and bye weeks
- **Player Data Editor**: Modify player stats, projections, and injury status
- **Multi-Mode Simulation**: Test parameter configurations through full grid search or iterative optimization
- **Parallel Processing**: Efficient multi-threaded simulation execution (8+ workers supported)
- **Comprehensive Testing**: 2,255 tests across 70 test files ensuring system reliability
- **Flexible Configuration**: Customizable scoring weights, penalties, and multipliers
- **Data Validation**: Type-safe operations with Pydantic runtime validation
- **Error Recovery**: Robust error handling with detailed logging

## Installation

### Requirements

- Python 3.13.6+ (recommended)
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd FantasyFootballHelperScriptsRefactored
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python tests/run_all_tests.py
```

All 2,255 tests should pass (100% pass rate required).

## Quick Start

### 1. Fetch Player Data

```bash
# Download latest player projections
python run_player_fetcher.py
```

This fetches projected statistics for all NFL players and saves them to `data/players.csv`.

**Automatic Historical Data Archiving**: The player data fetcher automatically saves weekly snapshots of player and team data to `data/historical_data/{Season}/{WeekNumber}/` (e.g., `data/historical_data/2025/11/`). This feature:
- Preserves historical data for each week (players.csv, players_projected.csv, teams.csv)
- Skips saving if data for the current week has already been archived
- Uses zero-padded week numbers (01, 02, ..., 17) for consistent folder naming
- Can be disabled by setting `ENABLE_HISTORICAL_DATA_SAVE = False` in `player-data-fetcher/config.py`

### 2. Run League Helper (Interactive Mode)

```bash
# Start the interactive draft assistant
python run_league_helper.py
```

Follow the prompts to:
- Select your mode (Draft Helper, Trade Simulator, or Modify Player Data)
- Get player recommendations during draft
- Evaluate potential trades
- Optimize your roster

### 3. Run Simulations (Optional - for Advanced Users)

```bash
# Test a single configuration (fast)
python run_simulation.py single --sims 5

# Run iterative parameter optimization (recommended)
python run_simulation.py iterative --sims 100 --workers 8

# Run full grid search (exhaustive but slow)
python run_simulation.py full --sims 100 --workers 8
```

## Main Applications

### League Helper (`run_league_helper.py`)

Interactive application with **four main modes**:

#### 1. Add to Roster Mode (Draft Helper)
- Real-time player recommendations during draft
- Considers roster needs, bye weeks, injury risk, and opponent strength
- Displays top N recommendations with detailed scoring breakdown
- Updates automatically after each pick
- Tracks drafted players and roster composition

#### 2. Starter Helper Mode (Roster Optimizer)
- Optimizes starting lineup for each week
- Considers opponent matchups and bye weeks
- Displays best starters vs bench recommendations
- Shows expected points for each position
- Validates lineup against league rules

#### 3. Trade Simulator Mode
Three trade evaluation sub-modes:

##### 1. Waiver Optimizer
Find optimal waiver wire pickups (drop/add combinations) with two scoring modes:

**Mode Selection**:
- **Rest of Season**: Seasonal projections with standard scoring (player rating, schedule strength)
- **Current Week**: Weekly projections for streaming (matches Starter Helper scoring with matchup multipliers)

**Use Cases**:
- **Rest of Season**: Target long-term value, season-long pickups
- **Current Week**: Stream positions (QB, TE, K, DST) based on weekly matchups

##### 2. Trade Suggestor
Find mutually beneficial trades with league opponents based on roster needs.

##### 3. Manual Trade Visualizer
Evaluate specific trade proposals with before/after comparison (exports to txt and Excel files).

**Supported Trade Types:**
- **Equal Trades**: 1-for-1, 2-for-2, 3-for-3 (balanced player exchanges)
- **Unequal Trades**: 2-for-1, 1-for-2, 3-for-1, 1-for-3, 3-for-2, 2-for-3 (asymmetric exchanges)

**Advanced Features:**
- **Waiver Recommendations**: Automatically suggests waiver wire pickups when trading away more players than receiving
- **Drop System**: Identifies lowest-value players to drop when receiving more players than giving away
- **Trade Threshold**: Enforces minimum 30-point improvement for trade suggestions (0-point minimum for waiver moves)

#### 4. Modify Player Data Mode
- Update player statistics, projections, or draft status
- Add custom players or modify existing data
- Adjust injury status, bye weeks, or team assignments
- Persist changes to CSV files for future sessions

### Simulation System (`run_simulation.py`)

Parameter optimization engine that runs thousands of simulated leagues to identify optimal configuration settings.

**Three Optimization Modes:**

1. **Single Config Test** (debugging):
```bash
python run_simulation.py single --sims 5
```
- Tests one configuration quickly
- Useful for validating changes

2. **Iterative Optimization** (recommended):
```bash
python run_simulation.py iterative --sims 100 --workers 8
```
- Coordinate descent approach with random parameter exploration
- For each parameter: tests individual values + cartesian product of NUM_PARAMETERS_TO_TEST parameters
- Default: NUM_PARAMETERS_TO_TEST=1 (single parameter at a time)
- With NUM_PARAMETERS_TO_TEST=2: tests base parameter + 1 random parameter + all value combinations
- Example (NUM_PARAMETERS_TO_TEST=2, N=5): 48 configs per parameter (12 individual + 36 combinations)
- Total configs: 14 parameters x configs per parameter
- Much faster than full grid search (~2-3 hours vs days)
- **Configuration**: Edit NUM_PARAMETERS_TO_TEST in `simulation/ConfigGenerator.py` to explore multiple parameters simultaneously
- **Auto-resume**: If interrupted mid-optimization, automatically resumes from last completed parameter
  - Detects existing intermediate_*.json files and continues where it left off
  - Validates parameter order consistency before resuming
  - Cleans up intermediate files when full optimization completes

3. **Full Grid Search** (exhaustive):
```bash
python run_simulation.py full --sims 100 --workers 8
```
- Tests all parameter combinations
- (test_values + 1)^6 total configs (default: 7,776 configs)
- Finds global optimum but very slow

**How Simulation Works:**
1. Creates 10-team fantasy league (1 DraftHelper team + 9 opponents with various strategies)
2. Runs snake draft (15 rounds, 150 total picks)
3. Simulates 17-week regular season
4. Tracks wins, losses, and total points
5. Repeats N times per configuration
6. Identifies configuration with best win rate

### Draft Order Strategy Analyzer (`run_draft_order_simulation.py`)

Tests all 75 draft order strategies to identify which strategies perform best in league simulations. Produces a JSON report mapping each strategy to its win percentage.

**Usage:**
```bash
# Default: 15 simulations per strategy (~10-15 minutes)
python run_draft_order_simulation.py

# More accurate: 50 simulations per strategy (~30-45 minutes)
python run_draft_order_simulation.py --sims 50

# Quick test: 5 simulations per strategy (~3-5 minutes)
python run_draft_order_simulation.py --sims 5
```

**Output:**
Generates `simulation/draft_order_results/draft_order_win_rates_YYYYMMDD_HHMMSS.json`:
```json
{
  "metadata": {
    "timestamp": "2025-11-24 12:34:56",
    "num_simulations_per_file": 15,
    "total_files_tested": 75,
    "successful_files": 75,
    "failed_files": [],
    "baseline_config": "auto-detected",
    "runtime_minutes": 12.5
  },
  "results": {
    "1": 70.2,
    "2": 80.1,
    "3": 65.8,
    ...
  }
}
```

**Draft Strategies Tested:**
- Zero RB, Hero RB, Robust RB strategies
- WR-first, TE-premium strategies
- QB early vs late strategies
- Balanced, contrarian, and value-based approaches
- 75 unique strategies total

### Player Data Fetcher (`run_player_fetcher.py`)

Downloads current player projections from data sources and saves to `data/players.csv`.

**Features:**
- Async HTTP requests with retry logic
- Pydantic validation for data integrity
- Automatic backup of previous data

### Scores Fetcher (`run_scores_fetcher.py`)

Downloads NFL game scores and updates team rankings.

### Schedule Fetcher (`run_schedule_fetcher.py`)

Fetches NFL season schedule from ESPN API and saves to `data/season_schedule.csv`.

```bash
python run_schedule_fetcher.py
```

### Game Data Fetcher (`run_game_data_fetcher.py`)

Fetches game data including venue, weather, and scores from ESPN and Open-Meteo APIs.

```bash
# Fetch current season data
python run_game_data_fetcher.py

# Fetch specific season for simulation
python run_game_data_fetcher.py --season 2024 --output simulation/sim_data/game_data.csv

# Fetch specific weeks
python run_game_data_fetcher.py --weeks 1-5
```

### Draft Order Loop (`run_draft_order_loop.py`)

Advanced simulation tool that loops through all draft order strategies, running iterative optimization for each one with dedicated per-strategy config folders.

```bash
# Run with default settings
python run_draft_order_loop.py

# More simulations per config
python run_draft_order_loop.py --sims 100

# Use ProcessPoolExecutor for true parallelism
python run_draft_order_loop.py --use-processes
```

### NFL Fantasy Data Exporter (Chrome Extension)

Chrome extension (`nfl-fantasy-exporter-extension/`) that extracts player ownership data from NFL Fantasy and exports to CSV format.

**Installation:**
1. Open Chrome → `chrome://extensions/`
2. Enable Developer mode
3. Click "Load unpacked" → Select `nfl-fantasy-exporter-extension/` folder

**Usage:**
1. Navigate to fantasy.nfl.com → Your league → Players → All Taken Players
2. Click extension icon → "Extract All Pages"
3. Download CSV → Move to `data/drafted_data.csv`

See `nfl-fantasy-exporter-extension/README.md` for detailed instructions.

### Historical Data Compiler (`compile_historical_data.py`)

Standalone script that compiles historical NFL season data from ESPN APIs for simulation testing.

**Usage:**
```bash
# Compile 2024 season data
python compile_historical_data.py --year 2024

# With verbose logging
python compile_historical_data.py --year 2024 --verbose

# Custom output directory
python compile_historical_data.py --year 2024 --output-dir /path/to/output
```

**Output Structure:**
```
simulation/sim_data/{YEAR}/
├── season_schedule.csv       # Full season schedule with bye weeks
├── game_data.csv             # Game results with weather data
├── team_data/                # 32 team CSV files (defensive stats)
│   ├── KC.csv
│   └── ... (all 32 teams)
└── weeks/                    # Point-in-time weekly snapshots
    ├── week_01/
    │   ├── players.csv       # Actual + projected points
    │   └── players_projected.csv
    └── ... week_17/
```

**Features:**
- Fetches player data from ESPN Fantasy API (actual and projected points)
- Fetches game data from ESPN Scoreboard API with weather from Open-Meteo
- Creates point-in-time snapshots for each week (what the system would "see" at that point)
- Supports seasons 2021+ (weekly data available)

## Project Structure

```
FantasyFootballHelperScriptsRefactored/

   run_league_helper.py          # Main league helper application
   run_simulation.py              # Simulation system CLI
   run_player_fetcher.py          # Player data downloader
   run_scores_fetcher.py          # NFL scores fetcher
   run_pre_commit_validation.py   # Pre-commit test runner

   league_helper/                 # Main application logic
      LeagueHelperManager.py     # Main controller for league helper modes
      modes/                     # Application modes
         DraftHelperMode.py     # Draft recommendation engine
         ModifyPlayerDataMode.py # Player data modification
      trade_simulator_mode/      # Trade evaluation system
         TradeSimulatorModeManager.py
         TradeSimTeam.py
         TradeSnapshot.py
      util/                      # Core utilities
          PlayerManager.py       # Player data management
          ConfigManager.py       # Configuration loader
          FantasyTeam.py         # Roster management
          FantasyPlayer.py       # Player model
          TeamDataManager.py     # Team rankings data

   simulation/                    # Simulation system
      SimulationManager.py       # Main simulation controller
      ParallelLeagueRunner.py    # Multi-threaded execution
      ConfigGenerator.py         # Parameter combination generator
      ResultsManager.py          # Results aggregation
      SimulatedLeague.py         # Single league simulation
      DraftHelperTeam.py         # Team using DraftHelper system
      SimulatedOpponent.py       # AI opponent teams
      Week.py                    # Weekly matchup simulation
      sim_data/                  # Simulation data files

   player-data-fetcher/           # Data collection system
      PlayerFetcher.py           # Main fetcher
      data_sources/              # API integrations

   utils/                         # Shared utilities
      LoggingManager.py          # Centralized logging
      error_handler.py           # Error handling utilities
      csv_utils.py               # CSV I/O helpers

   tests/                         # Tests (2,255 tests across 70 files)
      run_all_tests.py           # Test runner
      [mirrors source structure]

   data/                          # Data files
      league_config.json         # League configuration
      players.csv                # Player statistics
      team_data/                 # Per-team rankings (32 CSV files)

   requirements.txt               # Python dependencies
   README.md                      # This file
   CLAUDE.md                      # Development guidelines
   rules.txt                      # Development workflow rules
```

## Configuration

### League Configuration (`data/league_config.json`)

Controls scoring weights, penalties, and roster settings:

**Key Parameters:**
- `num_recommendations`: Number of draft recommendations to display
- `lineup_size`: Total roster size (e.g., 15)
- `[position]_slots`: Position limits (QB: 2, RB: 4, WR: 4, TE: 2, FLEX: 2, K: 1)
- `FLEX_ELIGIBLE_POSITIONS`: Positions that can fill FLEX slots (default: ["RB", "WR"])
- `consistency_multipliers`: Bonuses for consistent performers
- `injury_penalties`: Penalties based on injury risk (Out/Doubtful/Questionable)
- `SAME_POS_BYE_WEIGHT` / `DIFF_POS_BYE_WEIGHT`: Weights for median-based bye week penalty calculation
- `team_multipliers`: Bonuses/penalties based on team strength
- `draft_order_adp_weight`: How much to favor earlier picks
- **`MATCHUP_SCORING.IMPACT_SCALE`**: Controls magnitude of matchup bonus/penalty (default: 150.0, range: 100-200)
- **`SCHEDULE_SCORING.IMPACT_SCALE`**: Controls magnitude of schedule bonus/penalty (default: 80.0, range: 40-120)

**Editing Configuration:**
You can modify `league_config.json` directly or use the simulation system to find optimal values.

### Logging Configuration

Each main script has logging settings at the top:

```python
LOGGING_LEVEL = 'INFO'        # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING_TO_FILE = False       # Console vs file output
LOGGING_FORMAT = 'standard'   # detailed / standard / simple
```

## Testing

### Running Tests

```bash
# Run all tests (REQUIRED before commits)
python tests/run_all_tests.py

# Show individual test names
python tests/run_all_tests.py --verbose

# Show full test output
python tests/run_all_tests.py --detailed

# Faster single-command mode
python tests/run_all_tests.py --single
```

**Test Requirements:**
- 100% pass rate required before commits
- Exit code 0 = success, 1 = failure
- All tests located in `tests/` directory

### Test Structure

Tests mirror source code structure:
```
tests/
   league_helper/
      util/
         test_PlayerManager.py
      modes/
          test_DraftHelperMode.py
   simulation/
       test_SimulatedLeague.py
```

**Writing Tests:**
- Use pytest framework
- Mock external dependencies
- Follow Arrange-Act-Assert pattern
- See `tests/README.md` for detailed guidelines

## Development Guidelines

### Pre-Commit Protocol

**MANDATORY before every commit:**

1. Run all unit tests:
```bash
python tests/run_all_tests.py
```

2. Verify 100% pass rate (exit code 0)

3. Update documentation if functionality changed

4. Commit with clear message (no emojis, under 50 chars)

### Code Standards

- **Type hints**: Required for all public methods
- **Docstrings**: Google-style format required
- **Error handling**: Use context managers from `utils/error_handler.py`
- **Logging**: Use `utils/LoggingManager.py` (DEBUG for details, INFO for progress)
- **CSV operations**: Use `utils/csv_utils.py` helpers
- **Path handling**: Always use `pathlib.Path` objects

**Example:**
```python
from typing import List, Optional
from pathlib import Path

def load_players(filepath: Path, position: Optional[str] = None) -> List[FantasyPlayer]:
    """
    Load players from CSV file.

    Args:
        filepath (Path): Path to players CSV file
        position (Optional[str]): Filter by position (QB, RB, WR, TE, K)

    Returns:
        List[FantasyPlayer]: Loaded player objects

    Raises:
        FileNotFoundError: If CSV file doesn't exist
    """
    pass
```

### Development Workflow

See `CLAUDE.md` for complete development guidelines including:
- Update workflow (using `updates/` folder)
- TODO file creation and tracking
- Test requirements
- Commit standards
- Documentation requirements

See `rules.txt` for detailed protocols including:
- TODO file verification (3+ iteration requirement)
- Requirement verification before completion
- Pre-commit validation steps
- Integration testing requirements

## Data Files

### Required Files

**Player Data** (`data/players.csv`):
- Columns: id, name, position, team, projected_points, adp, consistency, injury_risk, bye_week, etc.
- Generated by: `run_player_fetcher.py`

**Team Data** (`data/team_data/*.csv`):
- Per-team CSV files (32 total, one per NFL team)
- Contains weekly fantasy points allowed by position
- Generated by: `run_scores_fetcher.py`

**Configuration** (`data/league_config.json`):
- League settings and scoring parameters
- Edit directly or use simulation to optimize

### Simulation Data Files

**Simulation data** (`simulation/sim_data/`):
- `players_projected.csv`: Projected stats for simulation
- `players_actual.csv`: Actual stats for simulation
- `teams_week_N.csv`: Weekly team rankings

These files are separate from main data files to allow simulation testing without affecting live league helper data.

## Common Issues

### Tests Failing

1. Ensure all dependencies installed: `pip install -r requirements.txt`
2. Check Python version: `python --version` (3.13.6+ recommended)
3. Run with verbose flag: `python tests/run_all_tests.py --verbose`

### No Player Data

Run the player data fetcher:
```bash
python run_player_fetcher.py
```

### Simulation Taking Too Long

Use iterative mode instead of full grid search:
```bash
python run_simulation.py iterative --sims 50 --workers 8
```

### Import Errors

Ensure you're running scripts from the project root directory:
```bash
cd /path/to/FantasyFootballHelperScriptsRefactored
python run_league_helper.py
```

## Contributing

Before making changes:
1. Read `CLAUDE.md` for development guidelines
2. Read `rules.txt` for workflow protocols
3. Create update specification in `updates/` folder
4. Follow TODO file creation and verification process
5. Maintain 100% test pass rate
6. Update documentation as needed

## License

[License information to be added]

## Author

Kai Mizuno

## Additional Documentation

- `CLAUDE.md`: Complete development guidelines and coding standards
- `ARCHITECTURE.md`: System architecture and design documentation
- `docs/scoring_v2/`: **Comprehensive scoring algorithm documentation** (10 metrics, 10,000+ lines)
  - `docs/scoring_v2/README.md`: Scoring algorithm overview and dependency diagram
  - Individual metric reports (01-10): Detailed analysis of each scoring step
- `rules.txt`: Development workflow protocols and requirements
- `tests/README.md`: Testing guidelines and patterns
- `updates/`: Pending and completed update specifications
