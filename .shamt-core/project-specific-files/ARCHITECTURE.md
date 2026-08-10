---
Last Updated: 2026-08-10
Update History:
  - 2026-08-10: D3.5 top-level-script-doc-registration-reconcile-three-surfaces — registered the D2.3 seed-sweep harness `run_accuracy_seed_sweep.py` in §"Project Structure", the last of the three project-structure surfaces (`README.md`'s tree, `QUICK_START_GUIDE.md`'s "All Scripts" table, this tree) it appeared in none of; the measured 10 × 3 registration matrix goes from 27/30 to 30/30. Also replaced the §Overview note on the root `README.md` / `QUICK_START_GUIDE.md`, whose two factual clauses (five named entry-point scripts said not to exist, and an out-of-date test count) were measured false this session, with a scoped note that preserves this document's source-of-truth precedence and records the reconciliation — applied under a user-approved amendment to the unit's diff manifest, since ARCHITECTURE prose beyond the tree entry sits outside it (the D3.2 entry below is the precedent). No component boundary changed — the harness orchestrates the existing `run_accuracy_simulation.py` CLI as a subprocess rather than importing `AccuracySimulationManager`, and makes no network call, so §"Data fetchers / compilers" and the network-boundary statement remain true as written (slug: D3.5-top-level-script-doc-registration-reconcile-three-surfaces)
  - 2026-08-10: D3.2 repair-live-pool-203-records-in-place — registered the new root utility `repair_bye_week_points.py` in §"Project Structure", beside its emulated peer `validate_sim_data.py`. Raised at `/du5-review` as a Documentation CONCERN: the unit's diff registered the script in `README.md` and `QUICK_START_GUIDE.md` but not here, hitting two of the three project-structure surfaces its declared peer occupies and leaving them inconsistent for this script. Applied at `/du6-polish` under a user-approved amendment to the unit's diff manifest, since this path sits outside it (the handling the `TESTING_STANDARDS.md` D8.2/D8.3/D8.4 entries record). No component boundary changed — the utility makes no network call, so §"Data fetchers / compilers" and the network-boundary statement remain true as written (slug: D3.2-repair-live-pool-203-records-in-place)
  - 2026-08-08: Mode C refresh after framework import — replaced retired ticket-stage references (`/dt7-review`, `/dt8-polish`) with the current six-stage delivery ownership model: `/dt5-review` performs the cross-unit Documentation Impact & Currency sweep, while `/du5-review` and `/du6-polish` retain per-unit review and application ownership; `/dt6-finalize` is archive-only and therefore is not described as a documentation-polish stage
  - 2026-06-16: Initial creation (project initialization)
  - 2026-06-16: Populated all sections from repository research (slug: populate-shamt-project-docs)
  - 2026-06-21: Win-rate sweep convergence stopping rule (slug: sweep-driver-rewire)
  - 2026-06-29: Win-rate `--seed N` per-task deterministic seeding (Component 2 boundary + Decision 5) (slug: deterministic-seeding)
  - 2026-06-29: T30 paired-comparison-in-ascent — Decision 5 rationale refined to note T30 realization: auto-seed policy + resume fingerprint includes base seed (slug: paired-comparison-in-ascent-shared-seeds)
  - 2026-06-29: T31 replace-epsilon-with-significance-gate-accumulated-games — win-rate adoption gate replaced with accumulated-evidence significance + effect-size test (Decision 6) (slug: replace-epsilon-with-significance-gate-accumulated-games)
  - 2026-07-01: T34 human-approved-promote-gate-no-auto-write — bare `--promote` now previews (dry-run); `--promote --confirm` performs the write (Component 2 boundary + Data Stores Writers column)
  - 2026-07-11: T45 accuracy-objective-pairwise-vs-mae — reconcile accuracy-engine objective docs to code (pairwise ranking accuracy, MAE = diagnostic) (slug: accuracy-objective-pairwise-vs-mae)
  - 2026-07-15: Align to master template after framework import — corrected stale Shamt phase numbers (Review→Phase 7, Polish→Phase 8) in How to Update + Purpose (slug: project-doc-master-alignment)
  - 2026-07-16: T51 accuracy-sim-nondeterministic-parallel-tiebreak — Component 3 boundary now documents the accuracy engine's `--seed N` flag + fixed-default-seed (`DEFAULT_ACCURACY_SEED`) deterministic-by-default generation, contrasted with Component 2's entropy default (slug: accuracy-sim-nondeterministic-parallel-tiebreak)
  - 2026-07-18: Doc-refresh drift fixes — re-attributed the multi-step scoring pipeline from `PlayerManager.py` to the extracted `player_scoring.py` (`PlayerScoringCalculator`; `score_player()` delegates) in Component 1 Key files, and added the 14th scoring step (NFL-team penalty) to the Data Flow pipeline list
  - 2026-07-19: T54 winrate-sweep-selfplay-nondiscriminating — the `--sweep` objective now measures the trial config **against the running-best incumbent** (measured-vs-incumbent, wiring the T27 measured-config path through `CombinationEvaluator`→`ParallelLeagueRunner`→`SimulatedLeague`), replacing the symmetric self-play field where every config scored ~0.50; `--promote` additionally fail-safe-blocks (raises `ConfigurationError`) unless the sweep store carries a `discriminating` flag (Component 2 boundary) (slug: winrate-sweep-selfplay-nondiscriminating)
  - 2026-07-20: T58 winrate-adoption-gate-unpaired-ztest — Decision 6 rewritten: the sweep's adoption gate is now a one-sided ONE-SAMPLE z of the trial's fresh head-to-head evaluation against the 0.50 null (the pooled two-proportion z over accumulated store totals is removed; the store is no longer a gate input, schema unchanged), with the game-level intra-league clustering caveat and its measured false-adoption rates recorded in the Rationale, the "Alternatives considered" line re-grounded on evaluation cost + per-league persistence + incumbent-arm redundancy, and a T58 back-reference added to Decision 5 (slug: T58-winrate-adoption-gate-unpaired-ztest)
  - 2026-07-20: T62 winrate-max-selection-optimistic-bias — Component 2 boundary now records that `--promote` runs fresh simulations (LCB shortlist → `paired_comparison.run_paired_ab_comparison` re-measurement), consumes `--seed`, carries `--promote-shortlist` / `--promote-sims`, and can refuse to write; Decision 6 extended in place with the T62 promote-path selection-vs-estimation split, K=3/B=20 parameterisation, the asymmetric SE×1.28 clustering correction (consuming the measured VIF ≈ 1.64), and the two named residual limitations (max-over-K bias ~3σ→~0.85σ, uncorrected K-fold multiplicity ~3× nominal); added three Data Stores rows for `win_rate_sweep_results.json`, `win_rate_sweep_report.{json,txt}`, and `win_rate_meta_data.json` (slug: winrate-max-selection-optimistic-bias)
  - 2026-07-20: T68 winrate-heterogeneous-reference-pooling — the `win_rate_sweep_results.json` Data Stores row now records the per-record **`by_reference` map** (per-incumbent `{wins, games}` buckets + a distinct `self_play` bucket), that `total_wins`/`total_games` are a derived NON-ranking cross-bucket sum, and the quarantine-and-restart of a pre-fix (reference-free) store on load (rename to a timestamped sibling, data preserved); the report row's `rate_semantics` parenthetical corrected off the stale `max_selected`/in-sample-maximum wording; Decision 6 gains a T68 paragraph recording that per-reference bookkeeping (D1) makes the store comparable and `rank_combinations` now ranks on the margin-over-reference LCB (D2) rather than the incommensurable blend, with the honest margin≠absolute-strength residual and the two cross-story contracts (T57 reuses the shared quarantine primitive; T61's shortlist floor operates on the cross-bucket non-self-play aggregate) (slug: winrate-heterogeneous-reference-pooling)
  - 2026-07-21: T61 winrate-min-games-silent-convergence — Decision 6 clause 1 corrected (the `DEFAULT_MIN_GAMES` floor is reachable by ordinary configuration — a single-season `--data` root at `--sims 1` gives 17 < 30 — not only by a pathological run; records T61's driver-side pre-flight ERROR and the `"starved"` disposition); the T68 paragraph's `DEFAULT_MIN_SHORTLIST_GAMES` credit re-attributed from T61 to T68 with the two-floor (promote-shortlist pooled vs. adoption-gate per-evaluation) distinction made explicit; the `win_rate_sweep_results.json` Data Stores row now enumerates the three legal `convergence[{id}].status` values `"converged" | "in_progress" | "starved"` and the resume/`is_all_converged` consequences (slug: winrate-min-games-silent-convergence)
  - 2026-07-21: T57 winrate-fingerprint-omits-regime-inputs — Decision 5's resume-fingerprint sentence now names the **opponent regime** (`--naive-opponents`) as a fingerprint input and separates the two predicates (a non-estimand fingerprint mismatch does not resume but **keeps** the store; only a regime change quarantines-and-restarts); the `win_rate_sweep_results.json` Data Stores row records the **second, semantic quarantine trigger** (regime change) plus the additive top-level `naive_opponents` marker (`true`/`false`/`null`-or-absent ⇒ unknown ⇒ never quarantine) and T57/D7's non-clobbering ascending-suffix sibling name; Decision 6's T68 paragraph corrected — T57 adds an **opponent-regime** trigger, not the rejected fingerprint-mismatch trigger (slug: T57-winrate-fingerprint-omits-regime-inputs)
  - 2026-07-27: Mode C refresh after framework import — no content drift found (all canonical references still resolve); added the missing falsified-clause Update Trigger from the current architecture template
  - 2026-08-03: T90 accuracy-promote-reinflates-league-config — Component 3's **Boundary** and **Owns** corrected: accuracy `--promote` rewrites `data/configs/league_config.json` via `propagate_to_configs` as well as the week files, the base-config write is `BASE_CONFIG_PARAMS`-filtered through the new shared `simulation/shared/config_filters.extract_base_params`, and the preserved user-maintained key list grew to six with `OPPONENT_TEAMS` (closing the symmetric drop direction) (slug: T90-accuracy-promote-reinflates-league-config)
  - 2026-08-04: Mode C refresh after framework import — no template drift (the section set still matches the current imported `architecture.template.md`) and all canonical references still resolve. One substantive correction: Component 3's **Purpose** described the accuracy engine as "single-pass per-parameter tournament optimization", which T69 (commit `32a00a54`) superseded with a convergent multi-pass coordinate ascent — per-horizon freezing on a no-adoption pass, termination once every horizon is frozen, and a `MAX_ASCENT_PASSES = 10` safety bound reported distinctly from convergence; **Owns** now records the `_ascent_state.json` mid-ascent resume record each intermediate folder carries (absent in a pre-T69 folder, read as pass 0 / nothing frozen). T69 shipped without an ARCHITECTURE update; this closes it
  - 2026-08-05: Mode C refresh after the project's conversion to `flow_track: delivery` — re-pointed the two flow-facing surfaces from the retired nine-phase Engineer flow to the delivery track: the frontmatter `How to Update` block (was "follow the Engineer flow / Phase 7 (Review) / Phase 8 (Polish)") and the Purpose's consumer list (was "Phase 2 (Spec) research, Phase 7 Documentation Impact Assessment, Phase 8 currency review"), now naming `/dt3-design` + `/du1-spec`, `/du5-review` + `/dt7-review`, and `/du6-polish` + `/dt8-polish`. No architectural content changed and no template drift — the section set still matches the current imported `architecture.template.md`. The `How to Update` staleness was systematic across all four standards-doc templates and is filed upstream as `proposals/standards-doc-templates-hardcode-engineer-flow-vocabulary.md`
Update Triggers: |
  Update this document when:
  - New services, deployment units, or major components are added or removed
  - A data store is added, removed, or changes role (primary, replica, cache)
  - A boundary between components changes (new API contract, new event topic, new shared dependency)
  - An integration with an external system is added, removed, or changes auth/contract
  - A significant cross-cutting dependency is added (auth provider, message bus, observability backend)
  - An architectural decision affects how multiple features are built
  - When adding an entry, re-read this document's own overview/status/summary prose and flag any clause the new entry falsifies; re-run until a clean pass.
How to Update: |
  Open a delivery ticket (or a framework-update proposal if this is a shamt-core change), follow the
  delivery track, and amend the relevant sections of this file. `/du5-review` (per unit) and
  `/dt5-review` (cross-unit) flag whether a change implies an update; `/du6-polish` applies
  per-unit documentation fixes and re-validates. `/update-project-doc` is the direct route for a doc-only edit.
  Run `/validate-artifact .shamt-core/project-specific-files/ARCHITECTURE.md` after substantive edits.
  Keep `Last Updated` current and add an `Update History` entry with the triggering ticket/unit or
  proposal slug.
---

# Project Architecture

**Purpose:** High-level system overview for context during discovery, planning, and code reviews. This project runs the **delivery track** (`flow_track: delivery`), so it is threaded into `/dt3-design`'s ticket-scope research and each unit's `/du1-spec`, into the Documentation Impact & Currency assessment run by `/du5-review` (per unit) and `/dt5-review` (cross-unit), and into per-unit documentation-fix application at `/du6-polish`.

---

## Overview

Fantasy Football Helper Scripts is a local, single-user Python toolkit for making data-driven NFL fantasy-football decisions. It is **not** a server or a hosted service — it is a collection of command-line scripts that a manager runs from a checkout on their own machine. The primary user is the repository owner (Kai Mizuno) running it for the "Start 7" league.

The toolkit has three functional pillars:

1. **League Helper** — an interactive menu-driven tool (`run_league_helper.py`) for draft recommendations, weekly lineup optimization, trade/waiver evaluation, and manual player-data edits.
2. **Simulation engines** — two offline parameter-optimization engines that replay historical NFL seasons to tune the scoring algorithm: a **win-rate** engine (`run_win_rate_simulation.py`, optimizes draft/season win percentage) and an **accuracy** engine (`run_accuracy_simulation.py`, optimizes per-player pairwise ranking accuracy; MAE reported as a diagnostic).
3. **Data fetchers / compilers** — scripts that pull live data from public APIs (ESPN, Open-Meteo) and shape it into the CSV/JSON files the other two pillars consume (`run_player_fetcher.py`, `run_schedule_fetcher.py`, `compile_historical_data.py`).

All state is plain files on disk (CSV + JSON). There is no database, no network service, and no authentication layer. The scoring algorithm itself — a multi-step multiplier pipeline — is the intellectual core of the project and is documented in depth under `docs/scoring/`.

> **Note on the root `README.md` / `QUICK_START_GUIDE.md`:** these are user-facing summaries; this document and the code remain the source of truth, and the actual entry points are enumerated under **Components and Boundaries** below. Their script registries — `README.md`'s project-structure tree and `QUICK_START_GUIDE.md`'s "All Scripts" table, alongside the tree under **Project Structure** below — were reconciled against the tracked top-level `*.py` scripts and verified consistent on 2026-08-10 (D3.5-top-level-script-doc-registration-reconcile-three-surfaces).

---

## Tech Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| Language | Python 3.13+ (developed/tested on 3.13–3.14) | Standard CPython; no compiled extensions of our own |
| Framework | None | Plain CLI scripts driven by `argparse`; interactive menus via `input()` |
| HTTP clients | `httpx` (async, primary), `requests` (legacy, minimal) | Used only by the fetcher/compiler scripts |
| Data validation | `pydantic` >= 2, `pydantic-settings` | Runtime type checking of fetched API payloads and config |
| Resilience | `tenacity` (retry w/ exponential backoff), `aiofiles` (async file I/O) | Used in the async fetch paths |
| Data processing | `pandas`, `openpyxl` (Excel export), `scipy` (Spearman correlation) | CSV/Excel I/O and statistics |
| Config / env | `python-dotenv` | Optional `.env` loading |
| Data stores | CSV + JSON files on the local filesystem | No database — see Data Stores |
| Testing | `pytest`, `pytest-asyncio`, `psutil` | Run via `tests/run_all_tests.py` or `pytest` directly |
| Build / package manager | `pip` + `requirements.txt`, virtualenv (`.venv/`) | No `pyproject.toml` / packaging; scripts run in place from the repo root |
| Deployment | None (run locally from a checkout) | No container, orchestrator, or CI pipeline checked in |

---

## Project Structure

```
FantasyFootballHelperScripts/
├── run_league_helper.py          — interactive entry point (draft / lineup / trade / edit)
├── run_player_fetcher.py         — fetch player projections from ESPN
├── run_schedule_fetcher.py       — fetch season schedule from ESPN
├── run_win_rate_simulation.py    — win-rate parameter optimization engine
├── run_accuracy_simulation.py    — pairwise-ranking-accuracy optimization engine (MAE = diagnostic)
├── run_accuracy_seed_sweep.py    — multi-seed accuracy-engine sweep (noise-floor measurement)
├── compile_historical_data.py    — build simulation/sim_data/{YEAR}/ from ESPN/Open-Meteo
├── validate_sim_data.py          — sanity-check a compiled sim_data/{YEAR}/ tree
├── repair_bye_week_points.py     — zero stale bye-week points in data/player_data/ (offline, idempotent)
├── run_pre_commit_validation.py  — wrapper that runs the full test suite (gate before commit)
├── league_helper/                — interactive application + its modes and shared util/
├── simulation/                   — win_rate/ + accuracy/ engines, shared/, utils/, data, configs
├── player_data_fetcher/          — live ESPN player + game-data fetching package
├── schedule_data_fetcher/        — live ESPN schedule fetching package
├── historical_data_compiler/     — multi-season historical compiler package
├── utils/                        — cross-cutting shared utilities (logging, errors, CSV, models)
├── tests/                        — pytest suite mirroring the source tree (+ fixtures, integration)
├── data/                         — live working data (configs, player_data, team_data, schedule)
├── docs/                         — scoring algorithm, ESPN API, simulation, and research docs
├── nfl-fantasy-exporter-extension/ — Chrome extension exporting league ownership to CSV
├── requirements.txt              — pip dependencies
├── pytest.ini                    — pytest markers (live_api, offline)
└── CLAUDE.md                     — Shamt framework rules (rendered template)
```

**Key directories:**
- `league_helper/` — the interactive tool. `LeagueHelperManager.py` is the menu controller; `util/` holds the core domain logic (`ConfigManager`, `PlayerManager`, scoring); `*_mode/` subpackages implement each menu mode (`add_to_roster_mode`, `starter_helper_mode`, `trade_simulator_mode`, `modify_player_data_mode`, `reserve_assessment_mode`, `save_calculated_points_mode`).
- `simulation/win_rate/` — the win-rate engine (draft-strategy tournament, parameter sweep, config promoter). `simulation/accuracy/` — the pairwise-ranking-accuracy tournament engine (MAE diagnostic). `simulation/sim_data/{YEAR}/` — committed per-season historical snapshots the engines replay. `simulation/simulation_configs/` — sim output (intermediate/optimal config folders).
- `player_data_fetcher/`, `schedule_data_fetcher/`, `historical_data_compiler/` — the live-data acquisition layer (the only code that touches the network).
- `utils/` — shared, dependency-free-ish helpers imported everywhere: `LoggingManager`, `error_handler`, `csv_utils`, `FantasyPlayer`, `TeamData`, `DraftedRosterManager`, `data_file_manager`.
- `data/` — the live working dataset the League Helper reads/writes. `tests/` — the pytest suite plus committed `fixtures/` enabling offline runs.

---

## Components and Boundaries

A "boundary" here is anywhere data, identity, or trust crosses. Because this project is a set of local scripts with no network service, the boundaries are: **CLI entry points** (where a human/agent supplies input), **the filesystem** (the shared store every component reads/writes), and **outbound calls to external HTTP APIs**.

### Component 1: League Helper (interactive)

**Purpose:** Interactive, menu-driven assistant for draft recommendations, weekly lineup optimization, trade/waiver evaluation, and manual data edits.

**Boundary:** CLI entry `run_league_helper.py` → `league_helper.LeagueHelperManager.main()`. Input arrives via stdin (numbered-menu prompts through `league_helper/util/user_input.py`). No network access at runtime — it reads only local files. Flags: `--enable-log-file`, `--week N` (override current NFL week in-memory).

**Owns:** The interactive session state and the in-session roster. It is a *reader* of the live data files and a *writer* of `data/player_data/*` (Modify Player Data mode) and of trade/visualizer export files (txt + Excel).

**Key files:**
- `league_helper/LeagueHelperManager.py` — menu controller; reloads player data before each menu display.
- `league_helper/util/ConfigManager.py` — loads and validates `league_config.json` (+ week overrides).
- `league_helper/util/PlayerManager.py` — player loading; its `score_player()` is the scoring entry point and delegates the actual math to `player_scoring.py`.
- `league_helper/util/player_scoring.py` — `PlayerScoringCalculator`, the multi-step scoring pipeline (14 steps) `score_player()` delegates to.
- `league_helper/util/user_input.py` — `show_list_selection()` and input helpers.
- `league_helper/*_mode/` — one subpackage per menu mode.

**Dependencies:**
- Internal: `utils/` (logging, CSV, models), `data/` files.
- External: none at runtime.

### Component 2: Win-Rate Simulation Engine

**Purpose:** Optimize the draft/season scoring parameters by replaying historical seasons and ranking draft strategies (and, in `--sweep` mode, parameter combinations) by simulated league win rate. In `--sweep` mode each trial config is evaluated **measured-vs-incumbent** — the measured team drafts the trial config while the other 9 draft the coordinate-ascent's running-best — so the win rate is a marginal "does this beat the best so far?" signal rather than a symmetric self-play field (where every config scored ~0.50). A sweep run stamps a `discriminating` flag into its results store; `--promote` fail-safe-blocks a store lacking it (T54).

**Boundary:** CLI entry `run_win_rate_simulation.py`. Reads simulation data from `simulation/sim_data/` (overridable via `--data`) and draft strategies from `simulation/sim_data/draft_order_possibilities/*.json`. Bare `--promote` **previews** the winning combination (dry-run, no write); `--promote --confirm` **writes** it into `data/configs/league_config.json`. Since T62 the promote path is **no longer a pure read-then-write of the store max**: it LCB-shortlists the top candidates and **runs fresh simulations** to re-measure each of them head-to-head against the live config (`config_promoter` → `paired_comparison.run_paired_ab_comparison`), promoting only the candidate that wins on that fresh evidence. It therefore **consumes `--seed`** (threaded through to the re-measurement for reproducibility) and carries two new flags, `--promote-shortlist N` (candidates re-measured, default 3) and `--promote-sims N` (simulations per candidate, default 20). A promote can now **refuse to write** — raising `ConfigurationError` with the live config byte-unchanged — when no re-measured candidate clears the clustering-adjusted significance threshold with a positive delta (see Decision 6). The optional `--seed N` flag makes an evaluation reproducible from a base seed (omitted → OS entropy, today's stochastic behavior); see Decision 5.

**Owns:** Sweep results under `simulation/win_rate/` outputs and (when promoting) authorship of the live base config.

**Key files:**
- `simulation/win_rate/DraftStrategyOrchestrator.py`, `CombinationEvaluator.py`, `SweepTournament.py`, `ParallelLeagueRunner.py` — the tournament + parallel execution.
- `simulation/win_rate/strategy_loader.py` — globs/validates `draft_order_possibilities/*.json`.
- `simulation/win_rate/config_promoter.py` — promotes the best combination into the live config.
- `simulation/win_rate/SimulatedLeague.py`, `SimulatedOpponent.py`, `DraftHelperTeam.py`, `Week.py` — the league/draft/season model.

**Dependencies:**
- Internal: `simulation/shared/`, `simulation/utils/`, `utils/`, the scoring pipeline.
- External: none at runtime (replays committed data).

### Component 3: Accuracy Simulation Engine

**Purpose:** Tune scoring parameters to optimize per-player **pairwise ranking accuracy** across four weekly horizons (week1-5, week6-9, week10-13, week14-17) via **convergent multi-pass coordinate ascent** over a per-parameter candidate tournament (T69). Each pass sweeps every parameter for every not-yet-converged horizon; a horizon that adopts nothing in a pass is **frozen** and skipped by later passes, and the run stops — exiting `0` — once every horizon has frozen. `MAX_ASCENT_PASSES = 10` (`simulation/accuracy/AccuracySimulationManager.py:61`) is a **safety bound, not the stopping rule**: hitting it is reported distinctly and is never described as convergence, because a run that ran out of passes has not settled. This supersedes the engine's former single-pass shape, in which multi-pass behavior was an emergent side effect of a `while True: main()` runner that never exited.

**Why pairwise ranking accuracy, not MAE?** The League Helper's decisions are all ordinal — draft the higher-ranked player, start the higher-projected lineup, pick the better waiver — so it needs correct ordering, never a calibrated point total. The scoring pipeline's tier multipliers intentionally distort absolute magnitudes to improve ordering; optimizing MAE would penalize exactly those order-preserving distortions, whereas pairwise ranking accuracy (and Spearman correlation) are scale-invariant and do not fight the normalization step. MAE is still computed and reported as a **diagnostic** for absolute-value fidelity (bye-week medians, trade/lineup differentials, user-facing "expected points"), but it is never the selection objective.

**Boundary:** CLI entry `run_accuracy_simulation.py`. Reads `simulation/sim_data/`, writes optimal/intermediate config folders under `simulation/simulation_configs/`. With `--promote [FOLDER]`, `propagate_to_configs` rewrites **all five** `data/configs/` files — the four `week*.json` files **and** `league_config.json`. The base-config write is not a verbatim copy: the source `parameters` block is filtered to `BASE_CONFIG_PARAMS` (`simulation/shared/config_filters.extract_base_params`) so week-file-owned keys can never ride in, and six user-maintained keys (`CURRENT_NFL_WEEK`, `NFL_SEASON`, `MAX_POSITIONS`, `FLEX_ELIGIBLE_POSITIONS`, `INJURY_PENALTIES`, `OPPONENT_TEAMS`) are preserved from the existing target so live-only keys can never ride out (T90). All five writes are atomic tmp→rename **replacements**, built in memory before any write. The optional `--seed N` flag sets the seed for candidate-config generation; **unlike the win-rate engine (Component 2 / Decision 5), the accuracy engine defaults to a fixed seed** (`DEFAULT_ACCURACY_SEED`), so a plain run is **deterministic by default** — the tournament exists to produce reproducible `--compare`/`--promote` tuning evidence, not stochastic exploration, so candidate generation uses a per-generator `random.Random(seed)` seeded from a fixed constant rather than OS entropy (T51).

**Owns:** Output config folders under `simulation/simulation_configs/` — including each intermediate folder's `_ascent_state.json`, the T69 resume record holding the completed pass index and the set of frozen (converged) horizons, which lets an interrupted run resume mid-ascent rather than restarting; a pre-T69 folder carries no such file and is read as "pass 0, nothing frozen" — and (when promoting) authorship of **both** the `data/configs/` week files **and** `data/configs/league_config.json` (base-params-filtered, with the six preserved user-maintained keys). The base-vs-week ownership split itself is defined by `simulation/shared/config_constants.py` (`BASE_CONFIG_PARAMS` / `WEEK_SPECIFIC_PARAMS`) and enforced on write by `simulation/shared/config_filters.extract_base_params`.

**Key files:** `simulation/accuracy/AccuracySimulationManager.py`, `AccuracyCalculator.py`, `AccuracyResultsManager.py`, `ParallelAccuracyRunner.py`.

**Dependencies:** Internal `simulation/`, `utils/`, scoring pipeline. External: none at runtime.

### Component 4: Data Fetchers / Historical Compiler

**Purpose:** Acquire live data and shape it into the CSV/JSON files the other components consume.

**Boundary:** CLI entries `run_player_fetcher.py`, `run_schedule_fetcher.py`, `compile_historical_data.py`. These are the **only** components that make outbound network calls (ESPN APIs; Open-Meteo for weather). Each **writes** files under `data/` or `simulation/sim_data/{YEAR}/`.

**Owns:** Authorship of `data/player_data/*.json`, `data/season_schedule.csv`, `data/game_data.csv`, and the `simulation/sim_data/{YEAR}/` trees.

**Key files:**
- `player_data_fetcher/player_data_fetcher_main.py`, `espn_client.py`, `game_data_fetcher.py`, `fantasy_points_calculator.py`, `player_data_models.py` (pydantic).
- `schedule_data_fetcher/ScheduleFetcher.py`.
- `historical_data_compiler/` — `schedule_fetcher.py`, `game_data_fetcher.py`, `player_data_fetcher.py`, `team_data_calculator.py`, `weekly_snapshot_generator.py`, `json_exporter.py`, `http_client.py`, `constants.py`.

**Dependencies:**
- Internal: `utils/`.
- External: **ESPN Fantasy / Scoreboard APIs**, **Open-Meteo weather API**. Offline behavior is controlled by `ESPN_FIXTURE_DIR` (read from fixtures) and `ESPN_RECORD_FIXTURES_DIR` (record live responses) — see Integration Points.

### Component 5: NFL Fantasy Exporter (Chrome extension)

**Purpose:** Browser extension that scrapes current league ownership ("All Taken Players") from fantasy.nfl.com and exports it to CSV for import as `data/drafted_data.csv`.

**Boundary:** Runs in the user's Chrome browser (loaded unpacked), entirely outside the Python process. Hand-off to the Python tools is a CSV file the user drops into `data/`.

**Key files:** `nfl-fantasy-exporter-extension/` (JS + `manifest`; see its own `README.md`).

**Dependencies:** External: the logged-in fantasy.nfl.com session in the user's browser. No coupling to the Python code beyond the CSV file format.

---

## Data Stores

There is no database. All persistent state is files on the local filesystem. The table below lists the logical stores by directory/role.

| Store | Type | Role | Readers | Writers | Schema owner | Notes |
|-------|------|------|---------|---------|--------------|-------|
| `data/configs/league_config.json` + `week{1-5,6-9,10-13,14-17}.json` | JSON | primary (live scoring config) | League Helper, both sim engines (as baseline) | user (manual edit), win-rate `--promote --confirm`, accuracy `--promote` | Base config + per-horizon week overrides; `ConfigManager` merges base + active week file |
| `data/league_config.json` | JSON | legacy primary (back-compat) | `ConfigManager` fallback, some tests | rarely | Used only when `data/configs/` is absent; kept for tests/back-compat |
| `data/player_data/{qb,rb,wr,te,k,dst}_data.json` | JSON | primary (live player pool) | League Helper (`PlayerManager`) | `run_player_fetcher.py`, Modify Player Data mode | Per-position projection/stat files |
| `data/team_data/*.csv` | CSV | primary (per-team rankings) | League Helper, scoring | fetchers | One file per NFL team (32 total); weekly fantasy points allowed by position |
| `data/season_schedule.csv`, `data/game_data.csv` | CSV | primary (schedule/results) | League Helper, scoring | `run_schedule_fetcher.py`, game-data fetch | Schedule incl. bye weeks; games incl. weather |
| `data/drafted_data.csv` | CSV | primary (ownership) | League Helper | Chrome extension export (manual drop-in) | Who is rostered across the league |
| `simulation/sim_data/{YEAR}/` | CSV/JSON | primary (historical replay corpus) | both sim engines | `compile_historical_data.py` | Point-in-time weekly snapshots per season (2021+); committed to the repo |
| `simulation/sim_data/draft_order_possibilities/*.json` | JSON | primary (draft strategies) | win-rate engine | hand-authored | ~50 named draft strategies the win-rate tournament ranks |
| `simulation/simulation_configs/` | JSON folders | output (sim results) | accuracy engine (`--baseline`), promotion | accuracy engine | `accuracy_intermediate_*` and `accuracy_optimal_*` config folders |
| `simulation/sim_data/win_rate_sweep_results.json` | JSON | output (sweep accumulation store; under `--data`) | `config_promoter` (promote shortlist), `sweep_summary.rank_combinations` (report path) | `SweepResultsManager` | `SweepResultsManager` | Per-combo `{strategy_id, param_values, best_single_run_win_rate, by_reference, total_wins, total_games, total_runs, last_run}`; since T68 each record carries a **`by_reference` map** — one `{wins, games}` bucket per incumbent identity an evaluation was measured against, plus a distinct `self_play` bucket for the symmetric baseline/carry-over evaluations — so no bucket ever pools evaluations taken against different references (Decision 6, T68). `total_wins`/`total_games` are **kept as a derived cross-bucket sum** (back-compat/inspection only) and are **no longer a ranking or report-display input**: `rank_combinations` and the promote shortlist now read a same-reference **margin-over-reference LCB** pooled across the non-self-play buckets. A **pre-fix (reference-free) store is quarantined-and-restarted on load** — structurally detected (any record lacking `by_reference`), renamed to a timestamped `<path>.quarantined-<datetime>` sibling with the old data preserved on disk, and the live store restarts empty (a shared primitive; never a silent re-pool). Since **T57** the same primitive has a **second, semantic trigger — an opponent-regime change**, backed by an additive top-level **`naive_opponents` marker** (`true` = accumulated under `--naive-opponents`, `false` = the self-play default, `null` **or absent ⇒ unknown**) written on **every** `--sweep` launch: a load whose run regime differs from a **non-null** recorded marker over a **non-empty** combinations map quarantines-and-restarts, while an **absent/`null`** marker is *unknown* and **never** quarantines (the marker is simply stamped that run — the driver logs a one-time notice when it stamps a store that already holds evidence, since the label is then an inference). A **non-estimand fingerprint mismatch never quarantines** (it only sets `resume = False`, store kept). The archived sibling name is **non-clobbering** (T57/D7): the stamp is minute-resolution and this trigger can recur for one store, so a colliding name gains an ascending `-2`, `-3`, … suffix and an existing archive is never overwritten (rename-never-delete). The file also carries a per-config `convergence[{id}]` map whose **`status` has exactly three legal values — `"converged" \| "in_progress" \| "starved"`** (since T61; `mark_config_progress` rejects anything else): `"in_progress"` is a mid-ascent resume checkpoint, `"converged"` is the normal terminal mark, and `"starved"` is a **terminal non-converged** mark meaning the run's games per evaluation could never clear the adoption gate's `min_games` (Decision 6 clause 1). The resume path must tolerate all three; `is_all_converged` tests `== "converged"` **only**, so a `"starved"` entry keeps it `False` and the config is re-tuned **from baseline** on the next run rather than skipped |
| `simulation/sim_data/win_rate_sweep_report.{json,txt}` | JSON + text | output (human-readable sweep report; under `--data`) | report-only (no non-test consumer) | `sweep_summary.write_sweep_report` | `sweep_summary.shape_report_json` | Regenerated every `--sweep`; per-config `rank/strategy_id/win_rate/lcb/games/wins/param_values` plus top-level `rate_semantics` (`win_rate` = the selected combo's non-self-play pooled rate, not an estimate — T68; `lcb` = the margin-over-reference lower bound) and a `pooling_caveat` string — the `lcb`/`wins`/`rate_semantics`/`pooling_caveat` fields added additively by T62 |
| `simulation/sim_data/win_rate_meta_data.json` | JSON | output (strategy-only tournament store; under `--data`) | `_print_summary` (`run_win_rate_simulation.py`) | `WinRateMetaDataManager` (via `DraftStrategyOrchestrator`, strategy-only mode) | `WinRateMetaDataManager` | Per-strategy `{name, best_win_rate, total_wins, total_games, ...}`; homogeneous totals (no moving incumbent), so the Decision 6 / T68 incommensurability caveat does **not** apply here |
| `logs/<script>/` | text | append (diagnostics) | humans | every script (when `--enable-log-file`) | Rotating logs; console-only by default |

---

## Data Flow

The system is a pipeline from public data sources to live working files to recommendations/optimized configs.

**Acquisition → live data:**
```
ESPN / Open-Meteo APIs → [Data Fetchers] → data/player_data/, data/*.csv
Chrome (fantasy.nfl.com) → [Exporter extension] → data/drafted_data.csv (manual drop-in)
```

**Live data → recommendations:**
```
data/configs/*.json + data/player_data/* + data/team_data/* + data/*.csv
   → [League Helper: ConfigManager + PlayerManager scoring pipeline]
   → on-screen recommendations / lineup / trade analysis (+ optional Excel/txt exports)
```

**Historical data → optimized config:**
```
ESPN / Open-Meteo → [compile_historical_data.py] → simulation/sim_data/{YEAR}/
simulation/sim_data/{YEAR}/ + baseline config
   → [Win-Rate engine | Accuracy engine] (parallel replay of seasons)
   → ranked results → (--promote) → data/configs/league_config.json (closes the loop back to the League Helper)
```

The scoring pipeline (14 steps: normalization → ADP → player rating → team quality → performance → matchup → schedule → draft-order bonus → bye-week penalty → injury penalty → temperature → wind → location → NFL-team penalty) is shared between the League Helper and the simulation engines, which is what makes simulation-tuned parameters meaningful in live use. Steps 11–13 (temperature, wind, location) are the game-condition group. See `docs/scoring/` (steps 01–13); the 14th step, the NFL-team penalty, lives in `league_helper/util/player_scoring.py` (`_apply_nfl_team_penalty`) and is not yet documented under `docs/scoring/`.

---

## Integration Points

### External Services

- **ESPN Fantasy / Scoreboard APIs:** Source of player projections/stats, the season schedule, and game scores. Reached over HTTPS via `httpx` from the fetcher/compiler packages. **No authentication** (public endpoints). Offline/test behavior is controlled by two environment variables:
  - `ESPN_FIXTURE_DIR` — when set, all ESPN requests read pre-recorded JSON from this directory instead of the network (a missing fixture raises `FileNotFoundError` with recording instructions).
  - `ESPN_RECORD_FIXTURES_DIR` — when set, live responses are made *and* saved as JSON fixtures under `{dir}/espn_api/` for future offline use.
  Committed fixtures live under `tests/fixtures/` (`espn_api/`, `historical/`, `player_data/`, `league/`).
- **Open-Meteo weather API:** Source of game-day weather (temperature, wind) for game-condition scoring. Reached over HTTPS from the game-data fetcher/compiler. No authentication.

### APIs

- This project exposes **no inbound API**. All API usage is **outbound** to the external services above. Endpoint and field documentation lives under `docs/espn/` and `docs/research/`.

### Event / Message Contracts

- None. There is no queue, topic, or event bus. Inter-component hand-off is exclusively via files on disk (see Data Stores).

---

## Key Design Decisions

### Decision 1: File-based stores, no database

**Context:** A single-user, locally run toolkit needs to persist player data, config, schedules, and historical seasons.

**Decision:** Use plain CSV + JSON files on disk as the only persistence layer; pass data between components via well-known file paths under `data/` and `simulation/sim_data/`.

**Rationale:** Zero operational overhead, trivially diffable/committable, and easy to inspect or hand-edit. Historical snapshots and configs are versioned in git alongside the code.

**Alternatives considered:** SQLite/Postgres — rejected as unnecessary complexity for one user and a workload dominated by full-file reads and batch replays.

### Decision 2: Shared scoring pipeline between live tool and simulators

**Context:** Simulation-derived parameters are only useful if they govern the same scoring math the live League Helper uses.

**Decision:** Implement one scoring pipeline (rooted in `league_helper/util` and mirrored in the simulation models) driven entirely by `league_config.json`, and let the simulators write their winning config back via `--promote`.

**Rationale:** Closes the optimization loop — `simulate → promote → use live` — without code divergence.

**Alternatives considered:** Separate "simulation scoring" vs "live scoring" — rejected because it would let the two drift and invalidate tuning.

### Decision 3: Offline fixture mode for all external calls

**Context:** Tests and reproducible runs must not depend on the live ESPN/Open-Meteo APIs.

**Decision:** Gate every ESPN request behind `ESPN_FIXTURE_DIR` (replay) / `ESPN_RECORD_FIXTURES_DIR` (record), with fixtures committed under `tests/fixtures/`, and mark network tests with the `live_api` pytest marker so the default suite is fully offline.

**Rationale:** Deterministic tests and demos; the network is only touched on an explicit live fetch.

**Alternatives considered:** Mocking at the HTTP-client level inside each test — rejected in favor of a single record/replay seam that also serves manual offline runs.

### Decision 4: Parallel replay for simulation throughput

**Context:** Optimization replays thousands of league-seasons per parameter sweep.

**Decision:** Use worker pools (`ParallelLeagueRunner` / `ParallelAccuracyRunner`, `--workers` / `--max-workers`; accuracy defaults to `ProcessPoolExecutor` to bypass the GIL).

**Rationale:** Keeps full sweeps tractable (hours, not days).

**Alternatives considered:** Single-threaded replay — too slow for the sweep sizes used.

---

### Decision 5: Per-task deterministic seeding for reproducible win-rate evaluation

**Context:** The win-rate engine's randomness (team-slot shuffle, snake-draft-order shuffle, naive-opponent human-error picks) flowed through the process-global `random` module while leagues run concurrently in `ParallelLeagueRunner`'s thread pool — so identical inputs produced different results each run, and seeding the global RNG once would not help (worker threads draw from one shared RNG in OS-scheduler-dependent order).

**Decision:** Plumb an opt-in base seed (CLI `--seed N`) through the evaluate/runner path. The **per-task-seeded per-league private RNG (D1)** is the core mechanism: each `SimulatedLeague` owns its own `random.Random(seed)` and every randomness site routes through that instance (the naive opponent receives the league's RNG). Each simulation task derives its seed from `(base_seed, season, sim_index)` — **config-independent (D2)** — at submission. Omitting `--seed` seeds from OS entropy (D3), preserving the prior stochastic behavior. *(D1, D2, and D3 here are design-property sub-labels for this per-task seeding design — D1 = the per-league private RNG mechanism, D2 = the config-independent seed key, D3 = the entropy default — referenced from code comments as `D1/T29` etc. that backreference this decision; they are not cross-references to Architecture Decisions 1/2/3.)*

**Rationale:** Same seed → identical `(wins, games)` regardless of worker count (resolves the thread + global-`random` interaction by construction — no shared mutable RNG across threads). The config-independent per-task key is the substrate the **common-random-numbers / paired-comparison** work (T30) depends on to share draws across the trial-vs-current comparison. T30 realizes this consumer: on every `--sweep` run the coordinator auto-assigns a base seed from OS entropy, logs it with a `--seed N` reproduce hint, and the sweep resume fingerprint now includes the base seed — so an unseeded resume produces a fingerprint mismatch and **does not resume** (every config is re-tuned from baseline, the accumulated store **retained**) rather than silently mixing seed pools; an explicit `--seed N` resume yields the same fingerprint and resumes correctly. **T57 update:** the fingerprint's inputs also include the **opponent regime** (`--naive-opponents`) — an eighth `compute_input_fingerprint` payload input, beside the base seed, the strategy set, the baseline param values, `--num-values` and the three significance-gate constants — because the regime changes the estimand (~0.84 vs ~0.50). Two predicates are deliberately **distinct**: a plain **non-estimand fingerprint mismatch** (fresh auto-seed, added strategy file, changed `--num-values`) sets `resume = False` but **keeps** the store — nothing is archived; whereas an **opponent-regime change** triggers a **regime-only quarantine-and-restart at load** — the store is renamed to a timestamped `<path>.quarantined-<datetime>` sibling (data preserved, never deleted) and the live store restarts empty. "Starts fresh" therefore means *re-tunes every config from baseline*, not *discards the store*. **T58 update:** since T54's measured-vs-incumbent design and T58's one-sample adoption gate, the CRN pairing this decision established is consumed *inside* each head-to-head evaluation (the measured team plays the trial config against nine incumbent-config opponents at a shared per-task seed) rather than reconstructed across two separately-run arms. The cross-arm CRN use survives only in `paired_comparison.py`'s before/after measurement — see Decision 6.

**Alternatives considered:** Single-threaded seeded replay (discards parallelism — violates Decision 4); `numpy.random.SeedSequence` per task (adds a non-stdlib dependency; `random.Random` independence is ample for this Monte-Carlo workload).

---

### Decision 6: One-sample head-to-head significance gate for win-rate parameter adoption (T31, revised by T58, promote path extended by T62, store made per-reference by T68, min-games starvation surfaced by T61)

**Context:** The win-rate sweep's prior adoption rule was a single-evaluation ε-switch (ε = 0.005): a candidate replaced the running best only if its single-run win rate exceeded the running best's single-run rate by more than ε. Single-run win rates are noisy (a typical evaluation uses a few hundred to a few thousand simulated seasons), so the switch was arbitrary and inconsistent across noise levels — a small-n evaluation could adopt a candidate on luck, while a large-n one might correctly suppress a true improvement.

**Decision (revised by T58):** Replace the ε-switch with a **one-sample significance + effect-size AND-gate** evaluated over the trial's **fresh head-to-head evaluation** against the running-best incumbent (the measured-vs-incumbent objective of Decision 4's engine path, established by T54). The gate adopts a trial only when:
1. That single fresh evaluation yields at least `DEFAULT_MIN_GAMES` (= 30) games — a degenerate-input floor (it also guarantees the divisor is non-zero). **This floor is reachable by ordinary configuration, not only by a pathological run** (T61): games per evaluation are `17 weeks × --sims × valid seasons`, so a single-season `--data` root at `--sims 1` yields `17 × 1 × 1 = 17 < 30` — and `--sweep --sims 1` is documented, intended practice (`docs/simulation/BASELINE_RETUNE_T35.md:64-75`). Before T61 such a run silently adopted nothing and was still marked `converged`, poisoning the resume store. T61 adds a driver-side **pre-flight check** that computes the nominal games per evaluation and logs one ERROR naming the shortfall and the two levers (`--sims`, the season content of the `--data` root) without aborting the run, plus a distinct terminal **`"starved"`** disposition for exactly this case (see the `win_rate_sweep_results.json` Data Stores row).
2. The one-sided **one-sample** z-test (stdlib `statistics.NormalDist`) of the trial's own rate against the **0.50 null** — `z = (p_trial − 0.5) / sqrt(0.25 / n)` — is satisfied at `DEFAULT_CONFIDENCE` (= 0.95). The 0.50 null is exact by construction: the measured team plays the trial config while all nine opponents hold the incumbent config, so "trial ≡ incumbent" implies an expected win rate of exactly 0.5.
3. The effect (p_trial − 0.5) exceeds `DEFAULT_MIN_EFFECT_SIZE` (= 0.01) — a large-n guard blocking economically irrelevant adoptions. At realistic single-evaluation sample sizes the z-test is strictly stricter (the two conditions cross at n ≈ 6,764), so this floor is effectively inert below that.

The **persistent store is no longer a gate input.** It retains its other three roles — durable record, reporting source, and `--promote` input — and its schema is unchanged. All three module-level constants remain shared between the sweep driver's input fingerprint and the `SweepTournament` engine's gate so resume-fingerprint drift cannot occur (their values are unchanged by T58, so no in-flight resume checkpoint is invalidated). The gate function (`_adopt_by_significance`) is a pure helper: stdlib-only, independently testable, and side-effect free.

**Rationale:** The head-to-head design gives the trial an exact 0.50 null, so its own rate *is* the comparison — a second arm is redundant. Reading the running-best's accumulated rate was worse than redundant: it is a **different estimand**, blending symmetric self-play games (recorded by the baseline and carry-over anchors, which are ~0.50 by construction and carry no information about strength) with head-to-head games recorded when that combo was itself a trial against an *older* incumbent. Pooling those with the trial's totals is not conservative, it is incommensurable. Using the fresh evaluation rather than accumulated totals also makes the evidence same-reference by construction, immune to the store's mixed-provenance bookkeeping and to the running-best moving mid-pass, and it deletes (rather than guards) the checkpoint-resume path on which the running-best had no store entry. The effect-size floor still prevents a very large sample from adopting a trivial difference. **Clustering caveat (honest limitation):** the sampling unit is the **game**, but the 17 weekly matchups inside a league share one drafted roster and one seed, so they are positively correlated; treating `n = 17 × sims × seasons` as independent understates variance and makes the gate **anti-conservative**. This is not a regression — the prior pooled z divided by exactly the same inflated `n` — and it is measured rather than asserted away: a seeded league-level synthetic-null harness in the test suite records a false-adoption rate of **≈ 4.8% at zero intra-league correlation** (against a 5% nominal level) rising to **≈ 9.1% under a positive intra-league correlation** (latent per-league quality 0.5 ± 0.10, ρ ≈ 0.04, variance-inflation factor ≈ 1.64) — roughly 2× nominal. That inflation is recorded, not treated as a build failure; the priced first correction is to move to a **league-level sampling unit** (using each league's win/loss as the Bernoulli unit), which costs no extra simulation and is deferred to a follow-up story.

**T62 promote-path extension (selection vs. estimation).** The gate above governs the sweep's *ascent* adoption; T62 fixes the separate **`--promote` selection bias** — promoting `rank_combinations(...)[0]` reported an in-sample maximum (a double max over ~10³ noisy stored rates, ≈ +3σ optimistic) as if it were an estimate. The fix splits selection from estimation: the **Wilson-LCB shortlist is a candidate *filter*** over the store's pooled totals — and, because those totals carry no reference dimension and are the same **incommensurable** mixture this decision names, the LCB is explicitly *not* an estimate; the **re-measured paired value is the only quantity promote reports as an estimate**, produced by re-running the top-K shortlisted candidates head-to-head against the live config on fresh data (`run_paired_ab_comparison`) and promoting whichever wins that fresh evidence. Parameterisation: **K = 3** candidates re-measured (`--promote-shortlist`), **B = 20** simulations per candidate (`--promote-sims`). The clustering correction is applied **asymmetrically**, and the asymmetry is deliberate: the shortlist LCB uses **raw game counts** (an internal heuristic filter that claims no precision), while the operator-facing re-measured interval **and** the promote/refuse decision `z` are both widened by **SE × 1.28** (= √VIF, consuming this decision's own measured **VIF ≈ 1.64**), because that headline is claimed as an estimate and drives the live-config write. **Two residual limitations, named not corrected** (recorded here in the same honest-limitation style as the clustering caveat above): (1) a **max-over-K bias** survives — the promoted config is the argmax of `delta` over K = 3 fresh measurements, so the ~+3σ store bias is **shrunk to ≈ +0.85σ of the re-measurement's SE, not eliminated**; and (2) the K significance tests are an **uncorrected multiplicity** — three candidates each tested at the same one-sided level push the gate's false-promote rate to up to **≈ 3× nominal at K = 3**, compounding (not cancelling) the clustering inflation. Both are surfaced to the operator (the headline is labelled the winner of a K-way re-measurement) rather than corrected in-story; the cheaper structural fix remains the **league-level sampling unit** this decision already prices as its next step.

**T68 store bookkeeping (closes the structural gap the T62 shortlist routed around).** The T62 paragraph above describes the shortlist LCB as taken "over the store's pooled totals … the same **incommensurable** mixture this decision names"; T68 removes that gap at the source. Each sweep-store record now carries a **`by_reference` map** (per-incumbent `{wins, games}` buckets plus a distinct `self_play` bucket) so per-reference bookkeeping (D1) makes the store's own numbers comparable — no bucket ever pools evaluations against different references. `rank_combinations` now ranks on a **margin-over-reference LCB** (D2) — `_wilson_lower_bound(W, G) − 0.50` over each combo's pooled **non-self-play** buckets, excluding the ~0.50 self-play baseline/carry-over bucket — rather than the incommensurable blend, so the LCB shortlist T62 consumes is **no longer built from a mixture** (the `total_wins`/`total_games` flat pair survives only as a NON-ranking derived cross-bucket sum). One honest residual remains: the margin is improvement-over-reference, **not absolute strength** — pooling a combo's *different* older incumbents treats their margins as roughly exchangeable — so the LCB stays a promising-ness *filter*, re-leveled by T62's fresh head-to-head re-measurement before any write. Two cross-story contracts are recorded in the T68 spec: **T57** reuses T68's shared **quarantine-and-restart primitive** (adding an **opponent-regime** trigger to the same mechanism — explicitly **not** a fingerprint-mismatch trigger, which was the design considered and **rejected**: a non-estimand fingerprint mismatch sets `resume = False` and **keeps** the store, archiving nothing — and owning the fingerprint inputs, which T57 extends with the regime; the **resume** predicate (the full fingerprint) and the **quarantine** predicate (the regime marker only) are deliberately distinct, because "cannot resume" and "the evidence is incompatible" are different severities), and **T68**'s own shortlist/promote games floor (`config_promoter`'s `DEFAULT_MIN_SHORTLIST_GAMES`) now operates on the **cross-bucket non-self-play aggregate** (the pooled head-to-head games the margin is computed over), not per individual reference bucket. **Two distinct floors — do not conflate them:** `DEFAULT_MIN_SHORTLIST_GAMES` is **T68's**, applied at *promote/ranking* time to a combo's pooled non-self-play buckets in the store, whereas `DEFAULT_MIN_GAMES` (clause 1 above) is the **adoption gate's per-evaluation** floor, checked during the sweep's *ascent* against a single fresh head-to-head evaluation and never against anything pooled — the floor **T61** owns the handling of (its pre-flight ERROR + the `"starved"` disposition). Different mechanism, different scope, different owning story; T61 does **not** touch `DEFAULT_MIN_SHORTLIST_GAMES` or `config_promoter`.

**Alternatives considered:** Per-run ε-switch with a larger ε — still arbitrary and noise-dependent. Full Bayesian update — adds a non-stdlib dependency and is substantially more complex to implement, test, and explain. **Retaining the pooled two-proportion z over accumulated totals** (the pre-T58 rule) — rejected because the incumbent arm is both redundant under the head-to-head design and a different estimand, so the test compared incommensurable quantities. **Paired-difference z on per-league outcomes** and **McNemar on discordant per-league pairs** — both rejected on two grounds beyond the storage question: each requires running a second (incumbent) arm at the same task seed, roughly **2× the evaluation cost** on the project's heaviest workload, *and* per-league or per-pairing persistence that the aggregate-only sweep store does not carry; neither addresses the estimand mismatch, they sidestep it. The paired-difference z is retained on record as the priced fallback should the 0.50 null prove structurally inexact, ranked **behind** the cheaper league-level sampling unit above.

---

## Security Posture

This is a local, single-user toolkit with **no authentication, authorization, tenancy, or network-exposed surface** — there is no server to attack and no multi-user trust boundary. The standing security obligations are therefore narrow:

- **No secrets required or stored.** All external APIs (ESPN, Open-Meteo) are public and unauthenticated. There are no API keys, tokens, or credentials in the codebase, and none should be added without a deliberate secret-handling design.
- **Untrusted input is external API payloads**, validated at the boundary with `pydantic` models before use. Treat fetched/scraped data as untrusted.
- **No regulated or personal data.** The data is public NFL stats and the user's own league rosters; nothing sensitive belongs in logs, exports, or fixtures.
- **The Chrome extension** runs in the user's authenticated browser session and only reads the page the user is viewing; it produces a CSV. It holds no credentials of its own.
- Because every component shares the filesystem, the relevant integrity concern is **which component is allowed to write which file** (see the Writers column in Data Stores) — notably that only `--promote` paths and Modify-Player-Data mode write the live config/player files.

---

## Performance and Scaling Notes

- **No latency/throughput SLOs** — this is a batch/interactive local tool, not a service. "Fast enough for a draft room" and "a full sweep finishes overnight" are the practical targets.
- **Simulation is the only heavy workload.** Win-rate full sweeps and accuracy tournaments are CPU-bound; they parallelize across workers (`--workers` / `--max-workers`) and the accuracy engine uses processes by default to bypass the GIL. The win-rate sweep runs per-config coordinate-ascent loops to convergence; the sample size per evaluation is set by `--sims` and the grid density per parameter is set by `--num-values`.
- **The League Helper is effectively instant** — it loads a few CSV/JSON files and runs the scoring pipeline over a few hundred players.
- **Scaling axis is vertical (more CPU cores → more workers).** There is no horizontal/sharded scaling; the historical corpus and player pool are small enough to hold in memory.
- **Known cost driver:** the number of simulations per strategy (`--sims`) trades statistical stability against wall time; the engine warns when `--sims` is low enough to be noisy.

---

*Template for project `.shamt-core/project-specific-files/ARCHITECTURE.md` in Shamt. Header metadata block above is required — the framework-update audit reads it.*

---
Validated 2026-08-08 — 2 rounds, 1 adversarial sub-agent confirmed (sha256:6baa56e52861f81d) (Mode C refresh: current delivery review/polish ownership)
