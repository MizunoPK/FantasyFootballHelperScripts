---
Last Updated: 2026-06-10
Update History:
  - 2026-06-07: Initial creation (project initialization)
  - 2026-06-09: Added win_rate_sweep_results.json data store (story sweep-results-store)
  - 2026-06-10: Noted run_win_rate_simulation.py --sweep multi-parameter mode in the optimization data-flow (story sweep-mode-cli)
Update Triggers: |
  Update this document when:
  - New services, deployment units, or major components are added or removed
  - A data store is added, removed, or changes role (primary, replica, cache)
  - A boundary between components changes (new API contract, new event topic, new shared dependency)
  - An integration with an external system is added, removed, or changes auth/contract
  - A significant cross-cutting dependency is added (auth provider, message bus, observability backend)
  - An architectural decision affects how multiple features are built
How to Update: |
  Open a story (or a framework-update proposal if this is a shamt-core change), follow the
  Engineer flow, and amend the relevant sections of this file. Phase 6 (Review) will flag
  whether a story implies an update; Phase 7 (Polish) applies the update and re-validates.
  Run `/validate-artifact .shamt-core/project-specific-files/ARCHITECTURE.md` after substantive edits. Keep `Last Updated`
  current and add an entry to `Update History` with the triggering story or proposal slug.
---

# Project Architecture

**Purpose:** High-level system overview for context during discovery, planning, and code reviews. Threaded into Phase 2 (Spec) research, Phase 6 (Review) Documentation Impact Assessment, and Phase 7 (Polish) currency review per the Shamt rules.

---

## Overview

Fantasy Football Helper Scripts is a personal, single-operator command-line toolkit for optimizing fantasy football decisions in the author's own league (team name "Sea Sharp"). It is run locally by one person — there is no hosted service, no multi-user surface, and no shared deployment.

The system has three functional pillars:

1. **Data acquisition** — a set of fetchers that pull NFL player projections/actuals, the season schedule, and per-game conditions (venue, weather, scores) from free public APIs (ESPN and Open-Meteo) and write them to local CSV/JSON files under `data/`.
2. **Decision support** — an interactive `league_helper` application that loads the fetched data and a tunable scoring configuration, then runs a multi-step scoring algorithm to drive draft recommendations, weekly lineup optimization, trade evaluation, and player-data editing.
3. **Parameter optimization** — an offline `simulation` engine that replays historical seasons to tune the scoring configuration. It has two distinct objectives: **accuracy** (minimize prediction error, MAE) and **win rate** (maximize simulated-league wins across draft strategies).

A `historical_data_compiler` builds the per-season historical datasets the simulation consumes, and a small Chrome extension assists manual export of league roster ownership data.

---

## Tech Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| Language | Python 3.13+ (3.14 in the local dev environment) | `requirements.txt` targets 3.13.6+; type hints used throughout |
| Application style | Interactive CLI + standalone runner scripts | No web framework; `argparse`-driven runners at repo root |
| HTTP clients | `httpx` (primary, async), `requests` (minimal legacy) | All outbound calls are async via `httpx` |
| Data validation | `pydantic` v2, `pydantic-settings` | Used in `player_data_fetcher` and `game_data_models`; dataclasses elsewhere |
| Resilience | `tenacity` (retry/backoff), `aiofiles` (async file I/O) | Retries on ESPN/Open-Meteo calls; concurrent CSV/JSON export |
| Data processing | `pandas`, `openpyxl` (Excel export), `scipy` (Spearman correlation) | CSV manipulation, trade-output spreadsheets, accuracy metrics |
| Config / secrets | `python-dotenv` (`.env`, gitignored) | `.env` carries optional keys; environment overrides like `LEAGUE_DATA_DIR` |
| Testing | `pytest`, `pytest-asyncio`, `psutil` (perf tests) | 113 `test_*.py` files; custom `tests/run_all_tests.py` runner |
| Build / packaging | None (no `pyproject.toml`/`setup.py`) | Dependencies installed from `requirements.txt` into a local venv |
| Deployment | None — run locally from the repo via `python run_*.py` | Single-machine, single-user |

---

## Project Structure

```
FantasyFootballHelperScripts/
├── run_league_helper.py          — entry point: interactive league helper
├── run_player_fetcher.py         — entry point: fetch current player data (async)
├── run_schedule_fetcher.py       — entry point: fetch NFL season schedule (async)
├── run_accuracy_simulation.py    — entry point: tune scoring config for prediction accuracy
├── run_win_rate_simulation.py    — entry point: tune draft strategy for win rate
├── compile_historical_data.py    — entry point: build per-season historical datasets
├── validate_sim_data.py          — entry point: validate a compiled sim_data/{year}/ tree
├── run_pre_commit_validation.py  — wraps tests/run_all_tests.py (pre-commit gate)
├── league_helper/                — interactive decision-support application
│   ├── LeagueHelperManager.py    — top-level controller / menu dispatch
│   ├── <mode>/                   — one subpackage per interactive mode
│   └── util/                     — managers + scoring engine (PlayerManager, ConfigManager, ...)
├── player_data_fetcher/          — async ESPN + weather fetcher (current season)
├── schedule_data_fetcher/        — async ESPN season-schedule fetcher
├── historical_data_compiler/     — builds historical sim datasets from ESPN/Open-Meteo
├── simulation/                   — offline optimization engine (accuracy + win_rate)
│   ├── accuracy/                 — MAE-based scoring-config tuning
│   ├── win_rate/                 — draft-strategy simulated-league tuning
│   ├── shared/                   — config generation, progress, results helpers
│   └── sim_data/                 — per-season historical inputs (2021–2025) + draft strategies
├── utils/                        — cross-cutting shared utilities (logging, CSV, errors, models)
├── data/                         — runtime data store (configs + fetched player/team/game data)
├── docs/                         — research notes, scoring docs, ESPN API reference
├── nfl-fantasy-exporter-extension/ — Chrome extension for manual roster export
└── tests/                        — pytest suite mirroring the source packages
```

**Key directories:**
- `league_helper/util/` — the core domain managers and the scoring engine; the heart of the decision-support logic.
- `data/` — the local runtime data store; both the read source for `league_helper` and the write target for the fetchers.
- `simulation/sim_data/{year}/` — historical inputs the simulation replays; produced by `historical_data_compiler`.
- `utils/` — shared, package-agnostic helpers imported across all packages.
- `docs/` — narrative documentation of the scoring categories, ESPN API behavior, and research.

---

## Components and Boundaries

This is a single-process, local toolkit; "boundaries" here are primarily process entry points (CLI runners), the local filesystem (`data/`, `simulation/sim_data/`), and outbound calls to free public HTTP APIs. There is no network ingress and no inter-service messaging.

### Component 1: League Helper (`league_helper/`)

**Purpose:** Interactive CLI that loads fetched data + a scoring config and provides draft recommendations, weekly lineup optimization, trade evaluation, and player-data editing.

**Boundary:** CLI entry via `run_league_helper.py` → `league_helper.LeagueHelperManager.main()`. No caller authentication (single local operator). Reads its data directory from `$LEAGUE_DATA_DIR` if set, otherwise `data/`.

**Owns:** The runtime scoring algorithm and roster state during a session; in-place edits to player CSVs and trade-output files. It does **not** own the source data — that is produced by the fetchers.

**Key files:**
- `league_helper/LeagueHelperManager.py` — top-level controller; loads managers, renders the mode menu, dispatches to a mode each loop.
- `league_helper/util/ConfigManager.py` — loads `data/configs/league_config.json` and merges the active week range override (`week1-5`, `week6-9`, `week10-13`, `week14-17`); exposes scoring parameters and helper accessors.
- `league_helper/util/PlayerManager.py` — loads players, runs the 10-step scoring algorithm, manages roster operations and CSV persistence.
- `league_helper/util/player_scoring.py` — the scoring engine producing `ScoredPlayer` results with per-step reasons.
- `league_helper/util/TeamDataManager.py`, `GameDataManager.py`, `SeasonScheduleManager.py` — load team rankings, per-game conditions, and the schedule respectively.
- `league_helper/util/FantasyTeam.py` — roster model (position slots, FLEX eligibility, bye distribution).
- `league_helper/<mode>/...ModeManager.py` — one manager per mode (Add to Roster, Starter Helper, Trade Simulator, Modify Player Data, Save Calculated Points).

**Dependencies:**
- Internal: `utils/` (logging, CSV, error handling, `FantasyPlayer` model); the `data/` store.
- External: none at runtime — it consumes already-fetched local files (no live API calls).

### Component 2: Player Data Fetcher (`player_data_fetcher/`)

**Purpose:** Fetch current-season player projections/actuals and per-game conditions, then export them to the `data/` store for `league_helper` to consume.

**Boundary:** CLI entry via `run_player_fetcher.py` → `player_data_fetcher.player_data_fetcher_main.main(settings_dict)` (async). Outbound HTTP to ESPN (public, unauthenticated) and Open-Meteo (public, keyless).

**Owns:** The export shape under `data/player_data/{pos}_data.json`, `data/team_data/{TEAM}.csv`, `data/game_data.csv`, `data/coordinates.json`, and optional historical snapshots under `data/historical_data/{season}/{week:02d}/`.

**Key files:**
- `player_data_fetcher_main.py` — orchestrates fetch → export → optional historical save → game-data fetch.
- `espn_client.py` — `BaseAPIClient` (async session, retry, rate limiting) and `ESPNClient` (projections, rankings, schedule).
- `fantasy_points_calculator.py` — extracts week-by-week actual/projected points from ESPN stat arrays.
- `game_data_fetcher.py` + `coordinates_manager.py` — venue + weather enrichment via Open-Meteo (archive vs forecast by game age).
- `player_data_exporter.py` — async export to position JSON + team CSVs.
- `player_data_models.py`, `game_data_models.py` — Pydantic v2 models (`ESPNPlayerData`, `ProjectionData`, `GameData`, `ScoringFormat`).
- `config.py` — fetcher settings and constants.

**Dependencies:**
- Internal: `utils/`; the `data/` store.
- External: ESPN Fantasy/Scoreboard API; Open-Meteo Archive/Forecast/Geocoding APIs.

### Component 3: Schedule Data Fetcher (`schedule_data_fetcher/`)

**Purpose:** Fetch the full NFL season schedule (including bye weeks) and export `data/season_schedule.csv`.

**Boundary:** CLI entry via `run_schedule_fetcher.py` (async). Outbound HTTP to the ESPN Scoreboard API.

**Owns:** `data/season_schedule.csv` (`week, team, opponent`; empty opponent = bye).

**Key files:**
- `schedule_data_fetcher/ScheduleFetcher.py` — async fetch (18 weeks) with `tenacity` retry + rate limiting; CSV export.

**Dependencies:**
- Internal: `utils/csv_utils.py`, `utils/LoggingManager.py`.
- External: ESPN Scoreboard API.

### Component 4: Historical Data Compiler (`historical_data_compiler/`)

**Purpose:** Build the per-season historical datasets the simulation replays, capturing point-in-time weekly snapshots of what the system "would have seen."

**Boundary:** CLI entry via `compile_historical_data.py` (`--year` / `--all-years`). Outbound HTTP to ESPN + Open-Meteo.

**Owns:** `simulation/sim_data/{year}/` — `season_schedule.csv`, `game_data.csv`, `team_data/{TEAM}.csv` (32 teams), and `weeks/week_NN/{pos}_data.json` snapshots.

**Key files:**
- `compile_historical_data.py` — 5-phase orchestrator (schedule + game data in parallel, then players, team data, weekly snapshots).
- `http_client.py`, `schedule_fetcher.py`, `game_data_fetcher.py`, `player_data_fetcher.py`, `team_data_calculator.py`, `weekly_snapshot_generator.py`, `json_exporter.py`, `constants.py`.

**Dependencies:**
- Internal: `utils/`; writes into `simulation/sim_data/`.
- External: ESPN Fantasy/Scoreboard API; Open-Meteo Archive API.

### Component 5: Simulation Engine (`simulation/`)

**Purpose:** Offline optimization of the scoring configuration by replaying historical seasons. Two independent objectives:
- **Accuracy** (`simulation/accuracy/`) — tournament-style tuning of prediction parameters to minimize MAE; deterministic.
- **Win rate** (`simulation/win_rate/`) — replays a 10-team simulated league across the full draft-strategy set to maximize win rate; stochastic.

**Boundary:** CLI entry via `run_accuracy_simulation.py` and `run_win_rate_simulation.py`. No network — reads only local `simulation/sim_data/`.

**Owns:** Output configs under `simulation/simulation_configs/accuracy_optimal_*/` and `accuracy_intermediate_*/`; win-rate tracking in `simulation/sim_data/win_rate_meta_data.json`. Promotion can copy an optimal config into `data/configs/`.

**Key files:**
- `accuracy/AccuracySimulationManager.py`, `AccuracyCalculator.py`, `AccuracyResultsManager.py`, `ParallelAccuracyRunner.py`.
- `win_rate/DraftStrategyOrchestrator.py`, `SimulatedLeague.py`, `ParallelLeagueRunner.py`, `SimDataLoader.py`, `WinRateMetaDataManager.py`.
- `shared/ConfigGenerator.py`, `ProgressTracker.py`, `ResultsManager.py`, `config_cleanup.py`, `config_constants.py`.

**Dependencies:**
- Internal: reuses `league_helper` scoring logic against historical inputs; `utils/`.
- External: none at runtime.

### Component 6: NFL Fantasy Exporter (Chrome extension, `nfl-fantasy-exporter-extension/`)

**Purpose:** Browser-side helper that scrapes drafted/owned-player data from fantasy.nfl.com and exports CSV the operator manually places at `data/drafted_data.csv`.

**Boundary:** Runs in Chrome as an unpacked extension; entirely manual hand-off via downloaded CSV. No connection to the Python code.

**Owns:** Nothing in the repo at runtime; produces a CSV the operator imports by hand.

**Key files:** `manifest.json`, `content.js`, `popup.js`, `popup.html`.

**Dependencies:** External — the NFL Fantasy web UI.

---

## Data Stores

All "stores" are local files. There is no database. Two file trees matter: the live `data/` directory (consumed by `league_helper`) and the per-season `simulation/sim_data/{year}/` trees (consumed by the simulation).

| Store | Type | Role | Readers | Writers | Schema owner | Notes |
|-------|------|------|---------|---------|--------------|-------|
| `data/configs/league_config.json` | JSON | Base scoring config (primary) | League Helper, Simulation (baseline) | Operator; Accuracy sim `--promote`; Win-rate sim `--promote` | `ConfigManager` | UPPER_SNAKE_CASE params under `parameters` |
| `data/configs/week{range}.json` | JSON | Per-week-range scoring overrides | League Helper, Simulation | Operator; Accuracy sim `--promote` | `ConfigManager` | Ranges: 1-5, 6-9, 10-13, 14-17 |
| `data/player_data/{pos}_data.json` | JSON | Current-season player data (per position: qb/rb/wr/te/k/dst) | League Helper | Player Data Fetcher | `player_data_exporter` | Week-by-week projected + actual points |
| `data/team_data/{TEAM}.csv` | CSV | Per-team weekly defensive/quality stats (32 teams) | League Helper (`TeamDataManager`) | Player Data Fetcher | `player_data_exporter` | One file per NFL team |
| `data/game_data.csv` | CSV | Per-game venue/weather/scores | League Helper (`GameDataManager`) | Player Data Fetcher / Game Data Fetcher | `game_data_models.GameData` | `None` → empty string in CSV |
| `data/season_schedule.csv` | CSV | Full season schedule + byes | League Helper (`SeasonScheduleManager`), Player Data Fetcher | Schedule Data Fetcher | `ScheduleFetcher` | `week, team, opponent`; empty opponent = bye |
| `data/coordinates.json` | JSON | Cached stadium/venue coordinates | Player/Game Data Fetcher | Game Data Fetcher (geocode-on-miss) | `coordinates_manager` | Cache; grows as new venues are geocoded |
| `data/drafted_data.csv` | CSV | Drafted/owned roster snapshot | League Helper, Player Data Fetcher | Chrome extension (manual import) | Chrome extension | Optional; manually placed by operator |
| `data/historical_data/{season}/{week:02d}/` | CSV | Optional weekly archive snapshots | (archival) | Player Data Fetcher (`--enable-historical-save`) | Player Data Fetcher | Zero-padded week folders |
| `simulation/sim_data/{year}/...` | CSV + JSON | Historical replay inputs (2021–2025) | Simulation Engine | Historical Data Compiler | Historical Data Compiler | `season_schedule.csv`, `game_data.csv`, `team_data/`, `weeks/week_NN/{pos}_data.json` |
| `simulation/sim_data/draft_order_possibilities/` | JSON | Draft-strategy definitions (one per file; ~49 top-level) | Win-rate Simulation | Operator / authored | Win-rate Simulation | Engine globs `*.json` non-recursively, so the `archive/` subfolder is excluded |
| `simulation/sim_data/win_rate_meta_data.json` | JSON | Per-strategy win-rate tracking | Win-rate Simulation | Win-rate Simulation (atomic write) | `WinRateMetaDataManager` | Gitignored runtime metadata |
| `simulation/sim_data/win_rate_sweep_results.json` | JSON | Per-`(strategy + params)` combination win-rate tracking (multi-parameter sweep) | Win-rate Simulation (sweep) | Win-rate Simulation (sweep, atomic write) | `SweepResultsManager` | Gitignored runtime metadata |
| `simulation/simulation_configs/accuracy_optimal_*/` | JSON | Tuned accuracy configs + metrics | Operator (review/promote) | Accuracy Simulation | Accuracy `ResultsManager` | Timestamped output folders |

---

## Data Flow

The system runs in two passes: an acquisition pass (network → `data/`) and a consumption pass (`data/` → recommendations). Optimization is a separate offline loop over historical data.

**Acquisition (per week):**
```
ESPN / Open-Meteo APIs
   → run_player_fetcher.py / run_schedule_fetcher.py
   → data/player_data/*.json, data/team_data/*.csv,
     data/game_data.csv, data/season_schedule.csv
```

**Consumption (interactive):**
```
data/ (player + team + game + schedule + configs)
   → ConfigManager (merge base config + active week-range override)
   → PlayerManager / player_scoring (10-step scoring algorithm)
   → mode (Add to Roster / Starter Helper / Trade Simulator / ...)
   → recommendations on screen + CSV/Excel/txt outputs
```

**Optimization (offline):**
```
ESPN / Open-Meteo → compile_historical_data.py → simulation/sim_data/{year}/
simulation/sim_data/{year}/ + data/configs (baseline)
   → run_accuracy_simulation.py (minimize MAE)  → accuracy_optimal_*/  → (optional --promote) → data/configs/
   → run_win_rate_simulation.py (maximize wins)  → win_rate_meta_data.json
   → run_win_rate_simulation.py --sweep (multi-parameter tournament)  → win_rate_sweep_results.json
```

For boundary-crossing flows in active stories, prefer a Mermaid diagram per `reference/mermaid_diagram_standards.md` and link it from the relevant story's `context.md`.

---

## Integration Points

### External Services

- **ESPN Fantasy / Scoreboard API:** Public, unauthenticated JSON endpoints. Used by `player_data_fetcher`, `schedule_data_fetcher`, and `historical_data_compiler` for player projections/actuals, team rankings, the season schedule, and game scores. Calls are async (`httpx`) with `tenacity` retry/backoff and a configurable per-request rate-limit delay (default 0.2–0.3s). Failures degrade gracefully: fetch methods return empty containers and the caller checks truthiness. Endpoint reference lives in `docs/espn/`.
- **Open-Meteo API:** Public, keyless weather service. The Archive endpoint serves games older than ~5 days; the Forecast endpoint serves recent/upcoming games; the Geocoding endpoint resolves unknown venue coordinates (cached to `data/coordinates.json`). Used by `player_data_fetcher` and `historical_data_compiler` for per-game temperature, wind, and precipitation.

### APIs

- This project exposes **no inbound API**. All HTTP is outbound to the two public services above. There is no server, route table, or authorizer.

### Event / Message Contracts

- None. There is no message bus, queue, or event topic. Inter-component hand-off is exclusively via local files in `data/` and `simulation/sim_data/`, plus the manual CSV hand-off from the Chrome extension.

---

## Key Design Decisions

### Decision 1: Local files as the integration boundary (no database)

**Context:** Components must share NFL data (players, teams, schedule, game conditions) and tuned configs.

**Decision:** Use plain CSV/JSON files under `data/` and `simulation/sim_data/` as the sole integration surface; fetchers write, the helper and simulation read.

**Rationale:** Single-user, single-machine tool; files are trivially inspectable, diff-able, git-trackable (where appropriate), and require no server. Lets the simulation replay exactly the file shapes the live helper consumes.

**Alternatives considered:** A local SQLite/RDBMS — rejected as unnecessary ceremony for one operator and a fixed, small dataset.

### Decision 2: Two separate optimization objectives (accuracy vs win rate)

**Context:** "Better" can mean either more accurate weekly point predictions or more wins in a simulated league — these are not the same metric and can disagree.

**Decision:** Keep two distinct simulation entry points: `run_accuracy_simulation.py` (deterministic, minimize MAE) and `run_win_rate_simulation.py` (stochastic, maximize wins across the full draft-strategy set).

**Rationale:** The two objectives optimize different parameter sets and have different runtime characteristics (deterministic vs Monte-Carlo). Separating them keeps each loop simple and independently runnable.

**Alternatives considered:** A single combined objective — rejected because blending the metrics hides which lever moved a result and complicates the parallel-execution model.

### Decision 3: Process pool for accuracy, thread pool for win rate

**Context:** Both simulations fan out across many configurations/strategies and need parallelism.

**Decision:** Accuracy tuning defaults to a `ProcessPoolExecutor` (CPU-bound scoring evaluation, bypasses the GIL); win-rate simulation uses a `ThreadPoolExecutor` (dominated by local file I/O).

**Rationale:** Match the executor to the workload's bottleneck. CPU-bound scoring benefits from real parallelism across processes; I/O-bound league replay benefits from lightweight threads without process-spawn overhead.

**Alternatives considered:** A single executor type for both — rejected because it leaves one workload bottlenecked.

### Decision 4: Week-range config layering

**Context:** Optimal scoring weights differ across the season (early-season noise vs late-season signal).

**Decision:** A base `league_config.json` plus four week-range override files (`week1-5`, `week6-9`, `week10-13`, `week14-17`), merged by `ConfigManager` for the active week.

**Rationale:** Lets the scoring system adapt to the season phase without separate codepaths; the accuracy simulation tunes each range independently and can promote the result back into `data/configs/`.

**Alternatives considered:** A single static config — rejected because it underfits the early/late-season distribution shift.

---

## Security Posture

This is a **single-operator, local-only** tool; the security model reflects that scope rather than a hosted-service model.

- **Authentication / authorization:** None, by design. There is no server, no inbound surface, no users, and therefore no auth or tenant-isolation model. The sole trust boundary is the operator's own machine.
- **External API auth:** None required. ESPN's public endpoints and Open-Meteo are unauthenticated/keyless. No credentials are sent on outbound calls.
- **Secrets handling:** `.env` (gitignored, loaded via `python-dotenv`) holds optional configuration/keys; it is never committed. The currently present `ACCU_WEATHER_API_KEY` is not referenced by any code path (weather comes from keyless Open-Meteo) and can be treated as vestigial. Environment overrides such as `LEAGUE_DATA_DIR` are read with `os.getenv`.
- **Data classification:** No regulated, personal, or sensitive data. All data is public NFL statistics and the operator's own roster/config choices.
- **Input validation:** Outbound API responses are validated at the boundary via Pydantic models (`ESPNPlayerData`, `GameData`, ...) before use; malformed records degrade gracefully rather than crashing the run.
- **Standing obligation for reviewers:** Because there is no auth surface, review effort focuses on data-integrity correctness (parsing, scoring math, file I/O), not on access control. Do not introduce committed secrets, and keep new outbound integrations keyless or `.env`-sourced.

---

## Performance and Scaling Notes

- **Scaling axis:** Vertical only — one machine, parallelized across local CPU cores. There is no horizontal/distributed dimension and none is intended.
- **Hot paths:** The accuracy simulation evaluates many scoring configurations and is CPU-bound; it parallelizes with a process pool (default 8 workers, `--max-workers`). The win-rate simulation replays many leagues and is I/O-bound; it parallelizes with a thread pool (default 8, `--workers`).
- **Caching strategy:** Team rankings, schedule, and position-defense rankings are cached in-memory inside `ESPNClient` for the duration of a fetch run; venue coordinates are cached to `data/coordinates.json` across runs; a dated team-rankings cache file may be written under `data/`. The interactive helper reloads player data from disk between menu cycles to reflect edits.
- **Resilience targets:** No formal latency/throughput/RPO/RTO targets (interactive personal tool). Robustness goals are: never lose the live `data/` on a failed fetch (writes are validated and, for CSVs, backed up), and make long simulation runs resumable — accuracy optimization auto-resumes from `accuracy_intermediate_*` folders and cleans them up on completion.
- **Known cost driver:** ESPN/Open-Meteo rate limiting bounds fetch throughput; the configurable `rate_limit_delay` trades wall-clock time against politeness to the public APIs.

---

*Template for project `.shamt-core/project-specific-files/ARCHITECTURE.md` in Shamt. Header metadata block above is required — the framework-update audit reads it.*

---
Validated 2026-06-07 — 2 rounds, 1 adversarial sub-agent confirmed
Touched 2026-06-09 — added win_rate_sweep_results.json data-stores row (story sweep-results-store); additive single-row change re-read for accuracy, no re-validation loop required
Touched 2026-06-10 — added the `run_win_rate_simulation.py --sweep` line to the optimization data-flow (story sweep-mode-cli); additive single-line change re-read for accuracy
