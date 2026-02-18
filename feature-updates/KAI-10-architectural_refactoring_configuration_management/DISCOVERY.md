# DISCOVERY: architectural_refactoring_configuration_management

**Epic:** KAI-10
**Status:** COMPLETE — USER APPROVED 2026-02-18
**Discovery Started:** 2026-02-17
**Discovery Approved:** [pending]

---

## Epic Request Summary

The user wants to perform a comprehensive architectural refactoring of all 7 runner scripts to establish consistent, maintainable configuration management. This includes: migrating from hardcoded/scattered configuration to CLI-based configuration with dependency injection, adding fast E2E test modes (≤3 min each), consistent debug support, and an integration test framework that validates argument combinations. The post-KAI-9 scope is reduced by ~20% since 9 constants were already removed from player-data-fetcher.

**Notes file:** `architectural_refactoring_configuration_management_notes.txt`

---

## Key Findings

### Finding 1: Current CLI Arg Coverage Per Script

| Script | CLI Args | State |
|--------|----------|-------|
| run_player_fetcher.py | 1 (--enable-log-file) | Minimal |
| run_schedule_fetcher.py | 1 (--enable-log-file) | Minimal; NFL_SEASON=2025 hardcoded directly in runner |
| run_league_helper.py | 1 (--enable-log-file) | Minimal |
| run_game_data_fetcher.py | 4 | Partial |
| compile_historical_data.py | 4 | Partial |
| run_win_rate_simulation.py | 17 | Comprehensive |
| run_accuracy_simulation.py | 10 | Comprehensive |

### Finding 2: player-data-fetcher Config State (Post-KAI-9)

Current `player-data-fetcher/config.py` CLI-configurable constants (11 remain + LOGGING_LEVEL):
1. CURRENT_NFL_WEEK = 17 → --week
2. NFL_SEASON = 2025 → --season
3. LOAD_DRAFTED_DATA_FROM_FILE = True → --load-drafted-data
4. DRAFTED_DATA = "../data/drafted_data.csv" → --drafted-data-path
5. MY_TEAM_NAME = "Sea Sharp" → --my-team-name
6. POSITION_JSON_OUTPUT = "../data/player_data" → --position-json-output
7. TEAM_DATA_FOLDER = '../data/team_data' → --team-data-folder
8. GAME_DATA_CSV = '../data/game_data.csv' → --game-data-csv
9. ENABLE_HISTORICAL_DATA_SAVE = False → --enable-historical-save
10. ENABLE_GAME_DATA_FETCH = True → --enable-game-data
11. ESPN_PLAYER_LIMIT = 2000 → --espn-player-limit
12. LOGGING_LEVEL = 'INFO' → --log-level (universal arg)
- REQUEST_TIMEOUT = 30 → --request-timeout (optional)
- RATE_LIMIT_DELAY = 0.2 → --rate-limit-delay (optional)
- PROGRESS_UPDATE_FREQUENCY = 10 → --progress-frequency (optional)

**Non-CLI constants remaining in config.py (stay):** ESPN_USER_AGENT, LOG_NAME, LOGGING_FORMAT, PROGRESS_ETA_WINDOW_SIZE, COORDINATES_JSON

### Finding 3: league_helper Constants

`league_helper/constants.py` CLI-configurable constants (Q3 resolved — --my-team-name):
- FANTASY_TEAM_NAME → --my-team-name (consistent with player_fetcher)
- LOGGING_LEVEL → --log-level (universal)
- RECOMMENDATION_COUNT → --recommendation-count
- MIN_WAIVER_IMPROVEMENT → --min-waiver-improvement
- NUM_TRADE_RUNNERS_UP = 9 → --num-runners-up (number of trade alternatives shown)
- MIN_TRADE_IMPROVEMENT = 0 → --min-trade-improvement

Additional league_helper CLI args (not from constants.py, but needed):
- --mode: which of the 5 interactive modes to run
- --config-path: path to league_config.json
- --data-folder: path to player data folder
- --league-id: ESPN fantasy league ID
- --team-id: user's team number in the fantasy league
- --week: NFL week to analyze
- --season: NFL season year
- --logging-to-file: enable file logging
- --logging-file: log file path

**Note:** --league-id, --team-id, --week, --season are currently hardcoded or loaded from configs. Feature 07 S2 research will determine exact current source. Total: ~12 args + 3 universal (--debug, --e2e-test, --log-level).

### Finding 4: player-data-fetcher Internal Modules with Config Imports

5 internal modules use config imports and need refactoring:
1. `player_data_fetcher_main.py` — imports from config (multiple constants)
2. `espn_client.py` — imports ESPN_USER_AGENT, ESPN_PLAYER_LIMIT, CURRENT_NFL_WEEK (+ scattered inline imports)
3. `game_data_fetcher.py` — imports from config
4. `fantasy_points_calculator.py` — imports NFL_SEASON
5. `player_data_exporter.py` — imports POSITION_JSON_OUTPUT, CURRENT_NFL_WEEK, TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME

### Finding 5: schedule-data-fetcher Has No Config File

`schedule-data-fetcher/` has only `ScheduleFetcher.py` (no config.py). NFL_SEASON=2025 is hardcoded directly in `run_schedule_fetcher.py`. Feature 02 will add argparse to the runner (not strip from a config file).

### Finding 6: game_data_fetcher Existing CLI Args

`run_game_data_fetcher.py` currently has 4 args:
- --season (NFL season year)
- --output (output file path)
- --weeks (which weeks to fetch)
- --current-week (current NFL week)

Confirmed via code inspection. Missing: --debug, --e2e-test, --log-level. Also imports `from config import NFL_SEASON, CURRENT_NFL_WEEK` as fallback defaults.

### Finding 7: historical_compiler Existing CLI Args + Constants

`compile_historical_data.py` currently has 4 args:
- --year (NFL season year)
- --verbose (enable verbose logging)
- --enable-log-file (file logging)
- --output-dir (output directory)

Missing: --debug, --e2e-test, --log-level, --timeout, --rate-limit-delay

`historical_data_compiler/constants.py` CLI-configurable values:
- REQUEST_TIMEOUT = 30.0 → --timeout
- RATE_LIMIT_DELAY = 0.3 → --rate-limit-delay

### Finding 8: Simulation Scripts — Existing Log-Level Coverage

`run_accuracy_simulation.py` ALREADY HAS --log-level (choices: debug/info/warning/error). Feature 06 only needs --debug and --e2e-test.

`run_win_rate_simulation.py` does NOT have --log-level, --debug, or --e2e-test. Feature 05 needs all 3.

### Finding 9: Test Count

Current test count: **2,744** (as of 2026-02-17). Notes file says 2,754 — minor discrepancy from recent test changes.

### Finding 10: Notes File Feature 01/Feature 10 Overlap (Resolved)

The notes list two separate player_fetcher features:
- Feature 01: player_fetcher — "Add argparse (14 arguments), remove CLI constants, add debug mode + E2E test mode" — marked "PARTIALLY COMPLETE"
- Feature 10: refactor_player_fetcher — "Refactor from direct config imports to constructor pattern" — marked "MUST BE FIRST" and "ESTABLISHES ARCHITECTURAL PATTERN"

**Observation:** Feature 10 (internal refactoring) MUST precede Feature 01 (adding argparse) because you need the constructor parameters defined before you can wire CLI args through them. The previous epic attempt merged these into a single feature "refactor_player_data_fetcher". Whether to keep them merged or separate is an open question.

### Finding 11: Documentation Feature (Resolved)

Notes include Feature 09 "documentation" with explicit deliverables (README.md updates, ARCHITECTURE.md updates, INTEGRATION_TESTING_GUIDE.md, workflow guide updates). The S1 guide warns against creating documentation features as separate features (handled in S7.P3/S10), but the user explicitly requested it in the notes. User decision needed.

---

## Technical Analysis

### Architecture Pattern (Before → After)

**Before (direct import pattern — verified, NOT importlib):**
```python
# run_player_fetcher.py
# Only has --enable-log-file; no config wiring, calls main() with no params
asyncio.run(main())  # ← No settings passed

# player_data_fetcher_main.py
from config import (CURRENT_NFL_WEEK, NFL_SEASON, ...)  # ← Direct module imports
async def main():  # ← No parameters; reads from config at module level
    ...
```

**After (constructor parameter):**
```python
# run_player_fetcher.py
settings = create_settings_dict(args)
asyncio.run(main(settings))  # ← Pass as parameter

# player_data_fetcher_main.py
async def main(settings_dict: dict | None = None):
    settings = create_settings_from_dict(settings_dict)  # ← Use passed value
```

**Note:** player_data_fetcher_main.py uses DIRECT imports (from config import ...), NOT importlib override. This simplifies the refactor.

### Dependency Chain

```
Features 01-07 (all independent — parallel Wave 1)
    → Feature 08 (integration_test_framework — needs all feature specs)
```

**Deep Check Analysis (per KAI-10 lesson):** Features 02-07 are each for DIFFERENT scripts. They don't wire into Feature 01's constructors — each script has its own internal structure. The constructor parameter PATTERN is defined in the notes file with sufficient detail for any feature to write its own spec independently. **Result: Features 02-07 have NO spec-level dependencies on Feature 01.** Only Feature 08 has spec-level dependencies (needs to know CLI args of ALL 7 scripts to write test specifications). Documentation is NOT a separate feature.

---

## Solution Options (Resolved)

All options resolved via user Q&A:
- **Q1 → B:** Features 01+10 merged into single refactor_player_data_fetcher
- **Q2 → B:** Documentation integrated into per-feature S7.P3 + S10 + Feature 08 deliverable
- **Q3 → A:** --my-team-name for consistency

See Resolved Questions section.

---

## Resolved Questions

| # | Question | Answer | Impact |
|---|----------|--------|--------|
| 1 | Merge Feature 01 (argparse) and Feature 10 (internal refactoring)? | **B — Merge into single refactor_player_data_fetcher feature** | 8 features total (not 9/10); single feature covers internals + argparse |
| 2 | Documentation as formal feature vs integrated into workflow? | **B — Integrate into workflow** | README/ARCHITECTURE in each feature's S7.P3; INTEGRATION_TESTING_GUIDE.md part of Feature 08; S10 handles rest |
| 3 | league_helper team name arg: --team-name or --my-team-name? | **A — --my-team-name** (consistent with player_fetcher) | Both scripts use same arg name for user's fantasy team |

---

## Validation Loop Rounds

### Round 1 (2026-02-17) — Sequential Read + Completeness Check

**Reading Pattern:** Sequential top-to-bottom
**Issues Found:** 7
**Clean Round Counter:** 0 (reset after fixes)

**Issues and Fixes:**
1. Finding 3 showed unresolved Q3 wording → Fixed: --my-team-name confirmed, full constants list added
2. Dependency chain showed "Feature 09? documentation" → Fixed: documentation not a feature
3. Missing research: game_data_fetcher existing args → Fixed: Finding 6 added (--season, --output, --weeks, --current-week)
4. Missing research: historical_compiler existing args + constants → Fixed: Finding 7 added
5. Missing research: simulation scripts log-level coverage → Fixed: Finding 8 added (accuracy has --log-level, win_rate does not)
6. "Before" architecture showed importlib (wrong) → Fixed: Corrected to direct import pattern
7. Finding numbering collision after insertions → Fixed: Old Findings 7/8 renumbered to 10/11

### Round 2 (2026-02-17) — Different Order + Integration Verification

**Reading Pattern:** Bottom-to-top (scope/features → architecture → findings)
**Issues Found:** 4
**Clean Round Counter:** 0 (reset after fixes)

**Issues and Fixes:**
1. Dependency chain diagram still showed old "Feature 09?" text → Fixed: Updated to 2-wave diagram
2. Solution Options section was stale (Q1/Q2/Q3 resolved) → Fixed: Condensed to resolved summary
3. Critical: S2 wave grouping was wrong — Features 02-07 listed as "Wave 2, Spec Dep: Feature 01" → Fixed: Deep check confirms all independent; revised to Wave 1 parallel (01-07) + Wave 2 (08)
4. Scope section missing documentation deliverables note → Fixed: Added section explaining docs produced via S7.P3 + S10 + Feature 08

### Round 3 (2026-02-17) — Random Spot-Checks + Alignment

**Reading Pattern:** Random spot-checks (5 requirements)
**Issues Found:** 0
**Clean Round Counter:** 1

### Round 4 (2026-02-17) — Thematic Clustering (Integration + Data Flow)

**Reading Pattern:** By integration point (runner→main→modules, Feature 08 test scenarios)
**Issues Found:** 0
**Clean Round Counter:** 2

### Round 5 (2026-02-17) — Final Sweep

**Reading Pattern:** Full exit verification checklist
**Issues Found:** 0
**Clean Round Counter:** 3 ✅ — VALIDATION LOOP EXITS

**Exit Verification:**
- [x] 3 consecutive rounds found zero issues/gaps
- [x] All sections of DISCOVERY.md complete
- [x] All pending questions resolved (Q1, Q2, Q3)
- [x] Assumptions verified (deferred items explicitly flagged as S2 research)
- [x] Scope clearly defined (in/out/deferred + documentation deliverables)
- [x] Solution approach identified with rationale
- [x] Feature breakdown ready with Discovery basis for each feature

---

## Recommended Approach

**Recommendation:** 8-feature epic with group-based S2 parallelization (3 waves)

**Rationale:**
- Merge Feature 01 + Feature 10 (Q1 answer): Single refactor_player_data_fetcher feature covers both internals and argparse — cleaner, matches previous attempt structure
- No documentation feature (Q2 answer): Docs integrated per-feature in S7.P3 + S10 handles remaining; INTEGRATION_TESTING_GUIDE.md is Feature 08's deliverable
- --my-team-name for league_helper (Q3 answer): Consistent naming across player_fetcher and league_helper

**Key Design Decisions:**
- Single source of truth: argparse defaults ONLY, no CLI constants in config/constants files
- Constructor parameter pattern throughout all 7 scripts
- Universal args (--debug, --e2e-test, --log-level) on all 7 scripts
- E2E test modes ≤180 seconds per script
- 3-wave S2 parallelization: Wave 1 (Feature 01) → Wave 2 (Features 02-07) → Wave 3 (Feature 08)

**S2 Dependency Waves (3 waves — user decision):**
- Wave 1: Feature 01 alone — establishes concrete design precedents (Settings class shape, constructor parameter pattern, universal arg implementation) that Features 02-07 can reference when writing their own specs
- Wave 2: Features 02-07 (parallel) — each covers a different script; use Feature 01's completed spec as concrete reference to ensure consistent design decisions across all scripts
- Wave 3: Feature 08 — needs all 7 feature specs (CLI args per script, E2E mode behavior, test scenarios to assert)

**Rationale for Wave 1 solo:** Features 02-07 technically CAN write specs without Feature 01, but Feature 01's completed spec provides concrete examples (actual Settings class names, constructor signatures, universal arg conventions). This reduces design inconsistency risk across 7 independent teams.

---

## Scope Definition

### In Scope (confirmed from notes)
- All 7 runner scripts get CLI-based configuration
- Constructor parameter pattern (dependency injection) replaces config imports
- Zero CLI constants in config/constants files after epic
- Universal args: --debug, --e2e-test, --log-level on all 7 scripts
- E2E test mode ≤180 seconds per script
- Debug mode: reduced data scope + DEBUG logging
- Integration test framework (7 test runners + master runner)

### Out of Scope (confirmed from notes)
- Configuration file support (YAML/TOML)
- API mocking (real APIs with data limiting only)
- GUI or web interface
- CI/CD integration
- New features or algorithm changes
- Database support

### Deferred (confirmed from notes)
- Mock data support for fetchers
- Configuration file format
- Automated CI/CD smoke testing
- Performance benchmarking framework

### Documentation Deliverables (integrated, not a separate feature)
The following are produced during the normal workflow, not as a separate feature:
- README.md Quick Start section (per-script in S7.P3, compiled in S10)
- ARCHITECTURE.md Testing Architecture section (S10)
- INTEGRATION_TESTING_GUIDE.md (~300 lines) — Feature 08 deliverable (S7.P3)
- Workflow guide updates for integration tests (S10.P1 if needed)

---

## Proposed Feature Breakdown

**Total: 8 features** (merged player_fetcher internals + argparse; no documentation feature)

| Feature | Name | Scope | S2 Wave | Rationale |
|---------|------|-------|---------|-----------|
| 01 | refactor_player_data_fetcher | Internal DI refactoring (5 modules) + argparse (14 args) + debug/E2E modes | Wave 1 (solo) | Sets design precedents for all other scripts |
| 02 | schedule_fetcher_cli | argparse (5 args: --season, --output-path, --data-folder, --output-format) + debug/E2E modes | Wave 2 | References Feature 01 spec for design patterns |
| 03 | game_data_fetcher_cli | Enhance existing argparse (+--debug, --e2e-test, --log-level) + debug/E2E modes | Wave 2 | References Feature 01 spec for design patterns |
| 04 | historical_compiler_cli | Enhance existing argparse (+--debug, --e2e-test, --timeout, --rate-limit-delay, --log-level) + debug/E2E modes | Wave 2 | References Feature 01 spec for design patterns |
| 05 | win_rate_simulation_e2e | Add --e2e-test + --debug + --log-level to existing argparse + E2E mode | Wave 2 | References Feature 01 spec for design patterns |
| 06 | accuracy_simulation_e2e | Add --e2e-test + --debug to existing argparse (already has --log-level) + E2E mode | Wave 2 | References Feature 01 spec for design patterns |
| 07 | league_helper_cli | Add comprehensive argparse (12+ args), refactor mode managers, debug/E2E modes | Wave 2 | References Feature 01 spec for design patterns |
| 08 | integration_test_framework | 7 CLI test runners + master runner + INTEGRATION_TESTING_GUIDE.md | Wave 3 | Needs all 7 feature specs (CLI args, E2E behavior) |

**Parallelization:**
- Wave 1: Feature 01 completes S2 solo (Primary agent)
- Wave 2: Features 02-07 do S2 in parallel (6 secondary agents, after Feature 01 S2 complete)
- Wave 3: Feature 08 does S2 solo (Primary agent, after all Wave 2 complete)

---

## User Approval

**Discovery Approved:** YES
**Approved Date:** 2026-02-18
**Approval Notes:** Approach and feature breakdown approved. User revised S2 wave structure to 3 waves: Feature 01 solo (Wave 1) to set design precedents → Features 02-07 parallel (Wave 2) → Feature 08 (Wave 3).

---

## Discovery Log

| Timestamp | Activity | Outcome |
|-----------|----------|---------|
| 2026-02-17 | Initialized Discovery, read notes file + codebase | Confirmed 11 config constants, test count 2744, 5 internal modules to refactor |
| 2026-02-17 | Verified CLI arg coverage per script | Confirmed 3 minimal (player, schedule, league_helper), 4+ partial/comprehensive |
| 2026-02-17 | Identified Feature 01/10 overlap and documentation question | 3 pending questions for user |
| 2026-02-17 | User answered Q1/Q2/Q3 | 8-feature structure confirmed, docs integrated into workflow, --my-team-name for league_helper |
