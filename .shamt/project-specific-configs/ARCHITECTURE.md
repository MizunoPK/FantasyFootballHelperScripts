# FantasyFootballHelperScripts — Architecture

**Version:** 1.0
**Last Updated:** 2026-03-09
**Supplements:** Root-level `ARCHITECTURE.md` (1,673 lines — read for full detail)

---

## System Overview

A Python 3.14.2 fantasy football optimization system with four subsystems:

| Subsystem | Entry Point | Purpose |
|-----------|-------------|---------|
| **League Helper** | `run_league_helper.py` | Interactive draft/trade/lineup assistant (4 modes) |
| **Simulation** | `run_simulation.py` | Parameter optimization via league simulation |
| **Player Fetcher** | `run_player_fetcher.py` | ESPN API → CSV data collection |
| **Scores Fetcher** | `run_scores_fetcher.py` | NFL scores → team rankings update |

**Key stats:** ~15,000 LOC · 101 test files · 2,723 test functions · 100+ config parameters · 6 positions (QB/RB/WR/TE/K/DST)

---

## Top-Level Directory Structure

```
FantasyFootballHelperScriptsRefactored/
├── league_helper/              # Interactive application (4 modes)
├── simulation/                 # Parameter optimization engine
├── player-data-fetcher/        # ESPN data collection
├── nfl-scores-fetcher/         # NFL scores fetcher
├── schedule-data-fetcher/      # NFL schedule fetcher
├── historical_data_compiler/   # Historical data compilation
├── utils/                      # Shared utilities (ALL modules use this)
├── tests/                      # 2,723 unit tests (pytest)
├── data/                       # CSV/JSON data files + league config
├── docs/                       # Documentation
├── feature-updates/            # Epic development framework (legacy path)
├── .shamt/                     # Shamt epic development framework
├── logs/                       # Application logs
├── ARCHITECTURE.md             # Full architecture reference (1,673 lines)
├── CODING_STANDARDS.md         # Full coding standards (393 lines)
├── CLAUDE.md                   # Agent rules (this project's rules file)
├── README.md                   # User guide
└── requirements.txt            # Python dependencies
```

---

## Layer Architecture

```
User Interface Layer
  run_league_helper.py · run_simulation.py · run_player_fetcher.py · run_scores_fetcher.py
         │
Application Layer
  LeagueHelperManager · SimulationManager · PlayerDataFetcher
         │
Mode / Feature Layer (league_helper only)
  AddToRosterModeManager · StarterHelperModeManager · TradeSimulatorModeManager · ModifyPlayerDataModeManager
         │
Business Logic Layer
  PlayerManager · ConfigManager · TeamDataManager · SeasonScheduleManager · GameDataManager
         │
Data Access Layer
  csv_utils · error_handler · LoggingManager · ESPN API client
         │
Data Layer
  data/player_data/*.json · data/configs/league_config.json · data/team_data/ · data/season_schedule.csv
```

---

## Module Reference

### `league_helper/` — Interactive Application

**Entry class:** `LeagueHelperManager` (delegates to mode managers)

**Core utilities (`league_helper/util/`):**

| Class | File | Responsibility |
|-------|------|---------------|
| `PlayerManager` | `util/PlayerManager.py` | Loads player data (per-position JSON from `data/player_data/` or legacy CSV); runs 10-step scoring algorithm; manages draft state |
| `ConfigManager` | `util/ConfigManager.py` | Loads `league_config.json`; 100+ params; per-week overrides; caches values |
| `TeamDataManager` | `util/TeamDataManager.py` | NFL team rankings from `data/team_data/{TEAM}.csv`; matchup strength per position |
| `SeasonScheduleManager` | `util/SeasonScheduleManager.py` | NFL schedule; bye week lookup; opponent projections |
| `GameDataManager` | `util/GameDataManager.py` | Game conditions (weather, home/away) from `data/game_data.csv` |
| `ProjectedPointsManager` | `util/ProjectedPointsManager.py` | Weekly projection aggregation |
| `FantasyTeam` | `util/FantasyTeam.py` | Roster management (add/drop/trade) |
| `ScoredPlayer` | `util/ScoredPlayer.py` | Dataclass: player + computed score |
| `player_scoring` | `util/player_scoring.py` | 10-step scoring calculation (extracted from PlayerManager) |

**Mode managers:**

| Mode | Manager | Purpose |
|------|---------|---------|
| Draft Helper | `add_to_roster_mode/AddToRosterModeManager.py` | Real-time draft recommendations |
| Weekly Optimizer | `starter_helper_mode/StarterHelperModeManager.py` | Lineup optimization by matchup |
| Trade Evaluator | `trade_simulator_mode/TradeSimulatorModeManager.py` | Trade generation and quantitative evaluation |
| Data Editor | `modify_player_data_mode/ModifyPlayerDataModeManager.py` | CSV player data editor |

---

### `simulation/` — Parameter Optimization Engine

**Entry class:** `SimulationManager` (`simulation/win_rate/SimulationManager.py`)

**3 optimization modes:** Single (debug) · Iterative (default, fast) · Full (exhaustive)

**Key classes:**

| Class | File | Responsibility |
|-------|------|---------------|
| `SimulationManager` | `win_rate/SimulationManager.py` | Orchestrates 3 modes; manages 24 optimizable parameters; per-week tracking |
| `ParallelLeagueRunner` | `win_rate/ParallelLeagueRunner.py` | `ThreadPoolExecutor` (8 workers); 5-6x speedup |
| `SimulatedLeague` | `win_rate/SimulatedLeague.py` | 10-team league; 15-round snake draft; 17-week season |
| `DraftHelperTeam` | `win_rate/DraftHelperTeam.py` | Team using DraftHelper algorithm being tested |
| `SimulatedOpponent` | `win_rate/SimulatedOpponent.py` | 9 AI opponents (3 strategies: ADP, position-need, best-available) |
| `ConfigGenerator` | `shared/ConfigGenerator.py` | Parameter variation generation; coordinate descent + random exploration |
| `ResultsManager` | `shared/ResultsManager.py` | Results aggregation and storage |

**Simulation data** (separate from `data/`): `simulation/sim_data/players_projected.csv`, `players_actual.csv`, `season_schedule.csv`, `game_data.csv`, `team_data/`

**Active configs:** `data/configs/league_config.json`, `data/configs/week1-5.json`, `week6-9.json`, `week10-13.json`, `week14-17.json`
**Optimization results:** `simulation/simulation_configs/{result_name}/` — stored per optimization run

---

### `player-data-fetcher/` — Data Collection

**Entry:** `player_data_fetcher_main.py`

**Key classes:**

| Class | File | Responsibility |
|-------|------|---------------|
| ESPN client | `espn_client.py` | Async HTTP via `httpx`; Tenacity retries; Pydantic validation |
| `fantasy_points_calculator` | `fantasy_points_calculator.py` | Applies league scoring rules to raw ESPN stats |
| `player_data_exporter` | `player_data_exporter.py` | CSV/Excel export with backups; weekly snapshots |

**Output paths:**
- Current: `data/player_data/{position}.json` (per-position JSON: qb, rb, wr, te, k, dst)
- Historical: `data/historical_data/{year}/{week}/` (snapshots per week)

---

### `utils/` — Shared Utilities

**ALL modules import from here.** Never duplicate these patterns.

| Module | File | Responsibility |
|--------|------|---------------|
| `LoggingManager` | `utils/LoggingManager.py` | Centralized logging; 3 formats (detailed/standard/simple); file + console |
| `error_handler` | `utils/error_handler.py` | `error_context()` CM; retry decorator; custom exceptions |
| `csv_utils` | `utils/csv_utils.py` | `read_csv_with_validation()`, `write_csv_with_backup()`; validation + backups |
| `FantasyPlayer` | `utils/FantasyPlayer.py` | Player dataclass (shared across modules) |
| `TeamData` | `utils/TeamData.py` | Team data structures |
| `DraftedRosterManager` | `utils/DraftedRosterManager.py` | Roster CSV management (`data/drafted_data.csv`) |

---

## 10-Step Scoring Algorithm

Implemented in `league_helper/util/PlayerManager.py` (and `util/player_scoring.py`):

1. **Base Score** — Normalized projected points
2. **ADP Multiplier** — Market wisdom adjustment (1.0x–1.5x)
3. **Consistency Multiplier** — Position-based bonus (0.5x–1.2x)
4. **Team Quality Multiplier** — Offensive/defensive strength
5. **Matchup Bonus** — Current opponent strength (additive, ±37.5 pts)
6. **Schedule Bonus** — Future opponent strength (additive, ±20.0 pts)
7. **Draft Order Bonus** — Round-based positional value
8. **Bye Week Penalty** — Same/different-position conflicts (exponential)
9. **Injury Penalty** — Risk assessment (−100 to 0)
10. **NFL Team Penalty** — Team strength adjustment (optional)

Documented in detail at: `docs/scoring/`

---

## Configuration System

**Primary config:** `data/configs/league_config.json` (~100+ parameters)
- Scoring rules (pass/rush yards, TDs, receptions, PPR/standard)
- ADP curves and multiplier thresholds
- Consistency, injury, bye week penalty scales
- Roster settings (position slots, FLEX eligibility)
- Simulation-tuned matchup/schedule impact scales

**Per-week overrides (in `data/configs/`):**
- `week1-5.json` — early-season overrides
- `week6-9.json` — mid-season overrides
- `week10-13.json` — late-season overrides
- `week14-17.json` — playoff-push overrides

**Access pattern:** Always via `ConfigManager(data_folder)` — never read JSON directly.

**Environment:** `.env` for API keys (AccuWeather). Loaded via `python-dotenv`.

---

## Data File Reference

| File / Path | Format | Contents |
|-------------|--------|---------|
| `data/configs/league_config.json` | JSON | 100+ league parameters |
| `data/configs/week1-5.json` (+ week6-9, week10-13, week14-17) | JSON | Per-week parameter overrides |
| `data/player_data/{position}.json` | JSON | Current player projections per position (qb, rb, wr, te, k, dst) |
| `data/drafted_data.csv` | CSV | User's drafted players |
| `data/season_schedule.csv` | CSV | NFL schedule with bye weeks |
| `data/game_data.csv` | CSV | Game results with weather conditions |
| `data/team_data/{TEAM}.csv` | CSV | Per-team weekly fantasy pts allowed (QB/RB/WR/TE/K); 32 files (ARI–WAS) |
| `data/historical_data/{year}/{week}/` | mixed | Weekly snapshots: players.csv, players_projected.csv, teams.csv, configs/, team_data/ |

---

## Testing Architecture

**Framework:** pytest · **Runner:** `python tests/run_all_tests.py` · **Requirement:** 100% pass rate before commits

**Structure:** mirrors source code
```
tests/
├── league_helper/          # 1,000+ tests (mirrors league_helper/)
│   ├── util/              # 600+ tests (PlayerManager, ConfigManager, TeamData)
│   ├── add_to_roster_mode/
│   ├── starter_helper_mode/
│   ├── trade_simulator_mode/
│   └── modify_player_data_mode/
├── simulation/            # 600+ tests
├── player-data-fetcher/   # 100+ tests
├── utils/                 # 100+ tests
├── integration/           # 25 cross-module tests
├── root_scripts/          # 23 tests
├── fixtures/              # Shared test data
└── conftest.py            # Pytest fixtures
```

**Naming convention:**
- File: `test_{SourceFileName}.py` — casing mirrors the source file (e.g., `test_PlayerManager.py` for `PlayerManager.py`, `test_player_scoring.py` for `player_scoring.py`)
- Class: `Test{ClassName}`
- Method: `test_{method_name}_{scenario}`

---

## Key Libraries

| Library | Version | Use |
|---------|---------|-----|
| `httpx` | ≥0.24 | Async HTTP (ESPN API) |
| `pydantic` | ≥2.0 | Runtime validation models |
| `pandas` | ≥2.1 | Data manipulation, CSV/Excel |
| `tenacity` | ≥8.2 | Retry logic (API calls) |
| `pytest` | ≥8.0 | Test framework |
| `openpyxl` | ≥3.1 | Excel export |
| `python-dotenv` | ≥1.0 | Environment variables |
| `colorama` | ≥0.4.6 | Colored terminal output |

**Python version:** 3.14.2 (minimum: 3.13.6)

---

## Extension Points

- **New mode:** Add `{name}_mode/` under `league_helper/`, create `{Name}ModeManager.py`, register in `LeagueHelperManager.py`
- **New simulation parameter:** Add to `ConfigGenerator.py` parameter grid + `SimulationManager.py` tuning logic
- **New data source:** Add fetcher in `player-data-fetcher/` following `espn_client.py` pattern (async, Pydantic validation, Tenacity retry)

---

*For complete architectural detail, read the root-level `ARCHITECTURE.md`.*
