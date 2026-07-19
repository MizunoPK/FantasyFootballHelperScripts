# Fantasy Football Helper Scripts

A comprehensive Python-based toolkit for optimizing fantasy football draft decisions, evaluating trades, and tuning the scoring algorithm by replaying historical NFL seasons.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Main Applications](#main-applications)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Testing](#testing)
- [Testing & Fixture Mode](#testing--fixture-mode)
- [Development Guidelines](#development-guidelines)
- [Data Files](#data-files)

## Overview

The Fantasy Football Helper Scripts provide a complete suite of tools for serious fantasy football managers:

1. **League Helper**: Interactive, menu-driven assistant for draft recommendations, weekly lineup optimization, and trade/waiver evaluation.
2. **Simulation engines**: Two offline parameter-optimization engines that replay historical NFL seasons to tune the scoring algorithm — a **win-rate** engine (`run_win_rate_simulation.py`) and a **pairwise-ranking-accuracy** engine (`run_accuracy_simulation.py`).
3. **Data fetchers / compilers**: Scripts that pull live data from public APIs (ESPN, Open-Meteo) and shape it into the CSV/JSON files the other tools consume.

The system uses projected and actual player statistics, team rankings, bye weeks, injury risk, consistency metrics, and configurable scoring parameters to provide data-driven recommendations. All state is plain files on disk (CSV + JSON); there is no database and no network service.

## Key Features

- **Draft Assistant**: Real-time player recommendations using a multi-step scoring pipeline
- **Trade Simulator**: Evaluate trades by simulating their impact on your roster strength
- **Roster Optimizer**: Optimize the starting lineup each week based on matchups and bye weeks
- **Player Data Editor**: Modify player stats, projections, and injury status
- **Two Simulation Engines**: Tune scoring parameters by win rate or by pairwise ranking accuracy across historical seasons
- **Parallel Processing**: Multi-worker simulation execution (`--workers` / `--max-workers`)
- **Comprehensive Testing**: Full offline suite run via `python tests/run_all_tests.py` (~3,000+ tests; 100% pass required)
- **Flexible Configuration**: Customizable scoring weights, penalties, and multipliers
- **Data Validation**: Type-safe operations with Pydantic runtime validation
- **Error Recovery**: Robust error handling with detailed logging

## Installation

### Requirements

- Python 3.13+ (developed/tested on 3.13–3.14)
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd FantasyFootballHelperScripts
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python tests/run_all_tests.py
```

The full offline suite (~3,000+ tests) should pass at 100% (a 100% pass rate is required before commits). The authoritative count is whatever `python tests/run_all_tests.py` reports.

## Quick Start

### 1. Fetch Player Data

```bash
# Download latest player projections
python run_player_fetcher.py

# With file logging enabled
python run_player_fetcher.py --enable-log-file
```

This fetches projections for all NFL players and writes the per-position pool under `data/player_data/` (`qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`).

**Historical data archiving**: the player data fetcher can save weekly snapshots of player/team data. This is controlled by the `enable_historical_save` field on the `Settings` dataclass in `player_data_fetcher/player_data_fetcher_main.py` (set it to `False` to disable).

### 2. Fetch the Season Schedule

```bash
python run_schedule_fetcher.py
```

This fetches the NFL season schedule (including bye weeks) from the ESPN API and writes `data/season_schedule.csv`.

### 3. Run League Helper (Interactive Mode)

```bash
# Start the interactive assistant
python run_league_helper.py
```

Follow the prompts to select a mode (e.g. Add to Roster, Starter Helper, Trade Simulator, Modify Player Data), get recommendations during your draft, optimize your weekly lineup, or evaluate trades.

### 4. (Optional) Tune Scoring Parameters

```bash
# Win-rate optimization (ranks draft strategies / parameter combinations by simulated win rate)
python run_win_rate_simulation.py --sweep

# Pairwise-ranking-accuracy optimization
python run_accuracy_simulation.py
```

See [Main Applications](#main-applications) for the full flag set.

## Main Applications

### League Helper (`run_league_helper.py`)

Interactive, menu-driven application. Its modes are implemented as the `league_helper/*_mode/` subpackages:

#### Add to Roster Mode (Draft Helper)
- Real-time player recommendations during a draft
- Considers roster needs, bye weeks, injury risk, and opponent strength
- Displays top-N recommendations with a detailed scoring breakdown
- Updates automatically after each pick

#### Starter Helper Mode (Roster Optimizer)
- Optimizes the starting lineup for each week
- Considers opponent matchups and bye weeks
- Shows expected points for each position

#### Trade Simulator Mode
Three trade-evaluation sub-modes:

##### 1. Waiver Optimizer
Find optimal waiver-wire pickups (drop/add combinations) with two scoring modes:
- **Rest of Season**: seasonal projections with standard scoring
- **Current Week**: weekly projections for streaming (matchup-aware; matches Starter Helper scoring)

##### 2. Trade Suggestor
Find mutually beneficial trades with league opponents based on roster needs.

##### 3. Manual Trade Visualizer
Evaluate specific trade proposals with a before/after comparison (exports to txt and Excel).

**Supported Trade Types:**
- **Equal Trades**: 1-for-1, 2-for-2, 3-for-3
- **Unequal Trades**: 2-for-1, 1-for-2, 3-for-1, 1-for-3, 3-for-2, 2-for-3

#### Modify Player Data Mode
- Update player statistics, projections, or draft status
- Persist changes to the `data/player_data/` files for future sessions

#### Save Calculated Projected Points Mode
- Computes and saves the calculated projected points for the current player pool for later use
- Implemented under `league_helper/save_calculated_points_mode/`

### Win-Rate Simulation Engine (`run_win_rate_simulation.py`)

Optimizes the draft/season scoring parameters by replaying historical seasons and ranking draft strategies (and, in `--sweep` mode, parameter combinations) by simulated league win rate.

- Reads simulation data from `simulation/sim_data/` (override with `--data`) and draft strategies from `simulation/sim_data/draft_order_possibilities/*.json`.
- Bare `--promote` **previews** the winning combination (dry-run, no write); `--promote --confirm` **writes** it into `data/configs/league_config.json`.
- `--seed N` makes an evaluation reproducible from a base seed (omit for OS entropy).

```bash
# Parameter sweep (coordinate-ascent optimization)
python run_win_rate_simulation.py --sweep

# Reproducible run with an explicit seed and more workers
python run_win_rate_simulation.py --sweep --seed 42 --workers 8

# Preview the winning config, then write it to data/configs/league_config.json
python run_win_rate_simulation.py --sweep --promote
python run_win_rate_simulation.py --sweep --promote --confirm
```

Key flags: `--sweep`, `--data`, `--seed N`, `--sims` (sample size per evaluation), `--num-values` (grid density per parameter), `--workers`, `--promote` / `--promote --confirm`.

### Accuracy Simulation Engine (`run_accuracy_simulation.py`)

Tunes scoring parameters to optimize per-player **pairwise ranking accuracy** across four weekly horizons (week1-5, week6-9, week10-13, week14-17). MAE is computed and reported as a **diagnostic**, never as the selection objective — the League Helper's decisions are ordinal, so correct ordering matters more than a calibrated point total.

- Reads `simulation/sim_data/` and writes optimal/intermediate config folders under `simulation/simulation_configs/`.
- `--promote [FOLDER]` copies an optimal folder into `data/configs/`.
- `--seed N` sets the candidate-generation seed; unlike the win-rate engine, the accuracy engine is **deterministic by default** (fixed `DEFAULT_ACCURACY_SEED`).

```bash
# Run the accuracy tournament
python run_accuracy_simulation.py

# Promote an optimal config folder into data/configs/
python run_accuracy_simulation.py --promote <optimal-folder>
```

Key flags: `--seed N`, `--promote [FOLDER]`, `--max-workers`.

### Player Data Fetcher (`run_player_fetcher.py`)

Downloads current player projections from the ESPN API and writes the per-position pool under `data/player_data/`.

**Features:**
- Async HTTP requests with retry logic (`httpx` + `tenacity`)
- Pydantic validation for data integrity
- Offline/fixture support via `ESPN_FIXTURE_DIR` (see [Testing & Fixture Mode](#testing--fixture-mode))

### Schedule Fetcher (`run_schedule_fetcher.py`)

Fetches the NFL season schedule (including bye weeks) from the ESPN API and writes `data/season_schedule.csv`.

```bash
python run_schedule_fetcher.py
```

### Historical Data Compiler (`compile_historical_data.py`)

Compiles historical NFL season data (players, games, weather, per-team stats) from the ESPN and Open-Meteo APIs into the `simulation/sim_data/{YEAR}/` trees the simulation engines replay.

```bash
# Compile a season
python compile_historical_data.py --year 2024

# With verbose logging
python compile_historical_data.py --year 2024 --verbose
```

**Output Structure:**
```
simulation/sim_data/{YEAR}/
├── season_schedule.csv       # Full season schedule with bye weeks
├── game_data.csv             # Game results with weather data
├── team_data/                # Per-team CSV files (defensive stats)
└── weeks/                    # Point-in-time weekly snapshots
    ├── week_01/
    │   ├── players.csv       # Actual + projected points
    │   └── players_projected.csv
    └── ...                    # ... through week_17/
```

Supports seasons 2021+ (weekly data available).

### Sim-Data Validator (`validate_sim_data.py`)

Sanity-checks a compiled `simulation/sim_data/{YEAR}/` tree for completeness and consistency before it is replayed by the simulation engines.

### Pre-Commit Validation (`run_pre_commit_validation.py`)

Wrapper that runs the full test suite (the same runner as `tests/run_all_tests.py`) as the gate before committing.

### NFL Fantasy Data Exporter (Chrome Extension)

Chrome extension (`nfl-fantasy-exporter-extension/`) that extracts league ownership ("All Taken Players") from fantasy.nfl.com and exports it to CSV.

**Installation:**
1. Open Chrome → `chrome://extensions/`
2. Enable Developer mode
3. Click "Load unpacked" → select the `nfl-fantasy-exporter-extension/` folder

**Usage:**
1. Navigate to fantasy.nfl.com → your league → Players → All Taken Players
2. Click the extension icon → "Extract All Pages"
3. Download the CSV → move it to `data/drafted_data.csv`

See `nfl-fantasy-exporter-extension/README.md` for details.

## Project Structure

```
FantasyFootballHelperScripts/
├── run_league_helper.py          # Interactive entry point (draft / lineup / trade / edit)
├── run_player_fetcher.py         # Fetch player projections from ESPN
├── run_schedule_fetcher.py       # Fetch season schedule from ESPN
├── run_win_rate_simulation.py    # Win-rate parameter optimization engine
├── run_accuracy_simulation.py    # Pairwise-ranking-accuracy optimization engine (MAE = diagnostic)
├── compile_historical_data.py    # Build simulation/sim_data/{YEAR}/ from ESPN/Open-Meteo
├── validate_sim_data.py          # Sanity-check a compiled sim_data/{YEAR}/ tree
├── run_pre_commit_validation.py  # Wrapper that runs the full test suite (pre-commit gate)
├── league_helper/                # Interactive application, its *_mode/ subpackages, and util/
├── simulation/                   # win_rate/ + accuracy/ engines, shared/, utils/, sim_data, configs
├── player_data_fetcher/          # Live ESPN player + game-data fetching package
├── schedule_data_fetcher/        # Live ESPN schedule fetching package
├── historical_data_compiler/     # Multi-season historical compiler package
├── utils/                        # Cross-cutting shared utilities (logging, errors, CSV, models)
├── tests/                        # pytest suite mirroring the source tree (+ fixtures, integration)
├── data/                         # Live working data (configs, player_data, team_data, schedule)
├── docs/                         # Scoring algorithm, ESPN API, simulation, and research docs
├── nfl-fantasy-exporter-extension/ # Chrome extension exporting league ownership to CSV
├── requirements.txt              # pip dependencies
├── pytest.ini                    # pytest markers (live_api, offline)
└── CLAUDE.md                     # Shamt framework rules (rendered template)
```

**Key directories:**
- `league_helper/` — the interactive tool. `LeagueHelperManager.py` is the menu controller; `util/` holds the core domain logic (`ConfigManager`, `PlayerManager`, scoring); the `*_mode/` subpackages implement each menu mode (`add_to_roster_mode`, `starter_helper_mode`, `trade_simulator_mode`, `modify_player_data_mode`, `save_calculated_points_mode`).
- `simulation/win_rate/` and `simulation/accuracy/` — the two optimization engines. `simulation/sim_data/{YEAR}/` — committed per-season snapshots the engines replay. `simulation/simulation_configs/` — sim output (intermediate/optimal config folders).
- `player_data_fetcher/`, `schedule_data_fetcher/`, `historical_data_compiler/` — the live-data acquisition layer (the only code that touches the network).
- `utils/` — shared helpers imported everywhere (`LoggingManager`, `error_handler`, `csv_utils`, and the data models).
- `data/` — the live working dataset. `tests/` — the pytest suite plus committed `fixtures/` for offline runs.

## Configuration

### League Configuration (`data/configs/league_config.json`)

The primary live scoring config is `data/configs/league_config.json`, with per-horizon week overrides `data/configs/week1-5.json`, `week6-9.json`, `week10-13.json`, and `week14-17.json`. `ConfigManager` merges the base config with the active week file. (A legacy top-level `league_config.json` fallback is consulted only when `data/configs/` is absent, and is kept for back-compat/tests.)

**Key Parameters** (under `parameters`):
- `MAX_POSITIONS`: roster position limits (QB, RB, WR, TE, FLEX, K, DST)
- `FLEX_ELIGIBLE_POSITIONS`: positions that can fill FLEX slots (default: `["RB", "WR"]`)
- `INJURY_PENALTIES`: penalties by injury-risk tier (`LOW` / `MEDIUM` / `HIGH`)
- `SAME_POS_BYE_WEIGHT` / `DIFF_POS_BYE_WEIGHT`: weights for the bye-week penalty
- `ADP_SCORING` / `PLAYER_RATING_SCORING`: `THRESHOLDS` / `MULTIPLIERS` / `WEIGHT` for the ADP and player-rating scoring components
- `DRAFT_ORDER_BONUSES` / `DRAFT_ORDER`: positional draft strategy (primary/secondary targets per round)
- `NFL_SCORING_FORMAT`: league scoring format (e.g. `ppr`)
- `MATCHUP_SCORING.IMPACT_SCALE` / `SCHEDULE_SCORING.IMPACT_SCALE`: magnitude of the matchup and schedule bonus/penalty

**Editing configuration:** edit `data/configs/league_config.json` directly, or use the simulation engines to find and `--promote` optimal values.

### Logging Configuration

Each entry-point script accepts `--enable-log-file` to write logs under `logs/<script>/` (console-only by default).

## Testing

### Running Tests

```bash
# Run all tests (REQUIRED before commits)
python tests/run_all_tests.py

# Show individual test names
python tests/run_all_tests.py --verbose

# Show full test output
python tests/run_all_tests.py --detailed
```

`python tests/run_all_tests.py` is the canonical full-suite gate: it discovers every `test_*.py` under `tests/`, runs each through `pytest -m "not live_api"`, and requires a 100% pass rate (exit `0` = success, `1` = failure). The default suite is fully offline (~3,000+ tests); the exact count is whatever the runner reports. The pre-commit wrapper `python run_pre_commit_validation.py` calls the same runner.

### Test Structure

Tests mirror the source tree under `tests/` (files named `test_<module>.py`, sometimes split as `test_<module>_<aspect>.py`). See `tests/README.md` for detailed guidelines.

### Testing & Fixture Mode

The ESPN API fetchers support two environment variables for offline testing and
fixture recording.

#### Offline Mode (`ESPN_FIXTURE_DIR`)

Set `ESPN_FIXTURE_DIR` to a directory containing pre-recorded JSON fixtures.
When set, all ESPN API requests read from local files instead of making HTTP calls.

```bash
# Run integration tests in offline mode using committed fixtures
ESPN_FIXTURE_DIR=tests/fixtures python run_pre_commit_validation.py

# Run a specific integration test offline
ESPN_FIXTURE_DIR=tests/fixtures pytest tests/integration/
```

**Fixture directory layout:**
```
tests/fixtures/
├── espn_api/       # ESPN scoreboard API responses (JSON)
├── historical/     # Historical season data
├── player_data/    # Player projection data
└── league/         # League configuration data
```

When a requested fixture file is not found, a `FileNotFoundError` is raised with
instructions to run the fixture recording mechanism to populate the directory.

#### Recording Mode (`ESPN_RECORD_FIXTURES_DIR`)

Set `ESPN_RECORD_FIXTURES_DIR` to a directory where live ESPN API responses should
be saved. When set, real HTTP requests are made and responses are written as JSON
files, creating fixtures for future offline use.

```bash
# Record live ESPN API responses into the fixture directory
ESPN_RECORD_FIXTURES_DIR=tests/fixtures python run_schedule_fetcher.py
```

Recorded files are written to `{ESPN_RECORD_FIXTURES_DIR}/espn_api/` with
filenames matching what offline mode expects (e.g.,
`scoreboard_week_1_2024.json`).

## Development Guidelines

### Pre-Commit Protocol

**MANDATORY before every commit:**

1. Run the full test suite:
```bash
python tests/run_all_tests.py
```

2. Verify a 100% pass rate (exit code 0). The wrapper `python run_pre_commit_validation.py` runs the same gate.

3. Update documentation if functionality changed.

4. Commit with a clear message.

### Code Standards

- **Type hints**: required for public methods
- **Docstrings**: Google-style format
- **Error handling**: use the context managers from `utils/error_handler.py`
- **Logging**: use `utils/LoggingManager.py` (DEBUG for details, INFO for progress)
- **CSV operations**: use the `utils/csv_utils.py` helpers
- **Path handling**: use `pathlib.Path` objects

The authoritative development workflow lives in `CLAUDE.md` (the Shamt framework rules); project coding conventions live in `.shamt-core/project-specific-files/CODING_STANDARDS.md`.

## Data Files

### Required Files

**Player pool** (`data/player_data/{qb,rb,wr,te,k,dst}_data.json`):
- Per-position projection/stat files
- Generated by `run_player_fetcher.py` (and edited by Modify Player Data mode)

**Team Data** (`data/team_data/*.csv`):
- Per-team CSV files (32 total, one per NFL team); weekly fantasy points allowed by position
- Generated/updated by the data-fetch pipeline

**Schedule / games** (`data/season_schedule.csv`, `data/game_data.csv`):
- Season schedule (including bye weeks) and game results (including weather)
- Generated by `run_schedule_fetcher.py` and the game-data fetch

**Configuration** (`data/configs/league_config.json` + `week{N}.json` overrides):
- League settings and scoring parameters
- Edit directly or `--promote` from a simulation run

### Simulation Data Files

**Historical replay corpus** (`simulation/sim_data/{YEAR}/`):
- Point-in-time weekly snapshots per season (2021+), committed to the repo
- Generated by `compile_historical_data.py`
- Draft strategies the win-rate engine ranks live under `simulation/sim_data/draft_order_possibilities/*.json`

**Simulation output** (`simulation/simulation_configs/`):
- `accuracy_intermediate_*` and `accuracy_optimal_*` config folders produced by the accuracy engine

## Common Issues

### Tests Failing

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check the Python version: `python --version` (3.13+)
3. Run with the verbose flag: `python tests/run_all_tests.py --verbose`

### No Player Data

Run the player data fetcher:
```bash
python run_player_fetcher.py

# With file logging (logs saved to logs/player_data_fetcher/)
python run_player_fetcher.py --enable-log-file
```

### Simulation Taking Too Long

Reduce the sample size or grid density, or add workers:
```bash
python run_win_rate_simulation.py --sweep --sims 50 --workers 8
```

### Import Errors

Run scripts from the project root directory:
```bash
cd /path/to/FantasyFootballHelperScripts
python run_league_helper.py
```

## Contributing

Before making changes:
1. Read `CLAUDE.md` for the development workflow (Shamt framework rules).
2. Follow the Engineer flow and maintain a 100% test pass rate.
3. Update documentation as needed.

## License

[License information to be added]

## Author

Kai Mizuno

## Additional Documentation

- `CLAUDE.md`: development workflow (Shamt framework rules)
- `.shamt-core/project-specific-files/ARCHITECTURE.md`: system architecture and design documentation
- `docs/scoring/`: comprehensive scoring-algorithm documentation (per-step metric reports)
- `tests/README.md`: testing guidelines and patterns
