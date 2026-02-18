# Secondary Agent Handoff: Feature 03 — game_data_fetcher_cli

## One-Line Startup (paste this to begin)

I'm joining as a secondary agent for the KAI-10 epic (architectural_refactoring_configuration_management). My assignment is Feature 03: game_data_fetcher_cli. Please read my HANDOFF_PACKAGE.md at `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_03_game_data_fetcher_cli/HANDOFF_PACKAGE.md` and begin S2.P1.

---

## ⚠️ DESIGN CORRECTION (2026-02-18): No Separate --debug Flag

**After Wave 1 (Feature 01) spec was approved, the user clarified a design change:**
- There is **NO separate `--debug` flag** in this epic
- Universal args are: **`--e2e-test`** and **`--log-level`** only (2 universal args, not 3)
- `--e2e-test` serves both purposes: fast E2E test mode AND debugging during development
- For verbose logging during debugging, developers use: `--e2e-test --log-level DEBUG`
- **Feature 01 spec has been updated** to reflect this — always treat it as the authoritative design reference

**Do NOT include a `--debug` flag in your spec.** Any mention of `--debug` below this notice is outdated and should be ignored.

---

## Agent Configuration

**My Agent ID:** Secondary-B
**My Feature Assignment:** Feature 03: game_data_fetcher_cli
**My Role:** Execute S2.P1 (3 iterations — I1 Discovery, I2 Checklist Resolution, I3 Refinement)
**Dependency Group:** Wave 2 (Group 2 — runs after Group 1 Feature 01 S2 is complete)
**Stop After:** S2.P1.I3 complete — Primary runs S2.P2 across all Wave 2 features

---

## Group Context

**Why I'm Starting Now:**
- Wave 1 (Feature 01: refactor_player_data_fetcher) has completed S2
- Feature 01's spec is available and defines the design precedents for all Wave 2 features

**Group 1 Spec Available (design reference):**
- `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_01_refactor_player_data_fetcher/spec.md`
- **Key patterns established:**
  - `@dataclass Settings` with `create_settings_from_dict(args_dict)` function
  - Runner uses direct import (not subprocess); calls `asyncio.run(main(settings_dict))`
  - E2E mode: use file if present, skip gracefully if not
  - `--debug` flag: DEBUG logging + data limiting
  - `--log-level` universal arg (choices: DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - `--e2e-test` flag: data limits + ≤180s completion

**Wave 2 Features Running in Parallel With Me:**
- Feature 02: schedule_fetcher_cli (Secondary-A)
- Feature 03: game_data_fetcher_cli (me — Secondary-B)
- Feature 04: historical_compiler_cli (Secondary-C)
- Feature 05: win_rate_simulation_e2e (Secondary-D)
- Feature 06: accuracy_simulation_e2e (Secondary-E)
- Feature 07: league_helper_cli (Secondary-F)

---

## Epic Context

**Epic:** KAI-10 — architectural_refactoring_configuration_management
**Epic Goal:** Refactor all 7 runner scripts to use CLI-based configuration with dependency injection. Zero CLI constants in config files. Each script gets E2E test mode (≤180s). Integration test framework (Feature 08) wraps all 7 scripts.
**Notes File:** `feature-updates/KAI-10-architectural_refactoring_configuration_management/architectural_refactoring_configuration_management_notes.txt`
**Discovery Doc:** `feature-updates/KAI-10-architectural_refactoring_configuration_management/DISCOVERY.md` (APPROVED)

**Key Constraints:**
- All 2,744+ existing unit tests must pass after any refactoring
- Behavioral equivalence preserved (no-args = same behavior as current)
- argparse defaults = single source of truth
- E2E test modes must complete in ≤180 seconds

---

## My Feature: Feature 03 — game_data_fetcher_cli

**Scope (from Discovery):** Wave 2 — Add universal CLI args to `run_game_data_fetcher.py` which already has 4 args.

**Key scope items:**
- `run_game_data_fetcher.py` currently has 4 args: --season, --output, --weeks, --current-week
- Add 3 universal args: --debug, --e2e-test, --log-level
- game_data_fetcher module imports from config as fallbacks — investigate and remove
- Implement --e2e-test mode completing in ≤180 seconds
- Implement --debug mode (DEBUG logging + reduced data scope)

**Key Discovery Finding (Finding 6):**
- `run_game_data_fetcher.py` already has: `--season`, `--output`, `--weeks`, `--current-week`
- Also imports `from config import NFL_SEASON, CURRENT_NFL_WEEK` as fallback defaults
- Missing: `--debug`, `--e2e-test`, `--log-level`

**IMPORTANT NOTE:** This is `run_game_data_fetcher.py` — the STANDALONE game data script.
This is DIFFERENT from `player-data-fetcher/game_data_fetcher.py` (internal module refactored in Feature 01).

**Files to Research:**
- `run_game_data_fetcher.py` — current argparse, config imports, structure
- The game data fetcher module it calls (likely `game-data-fetcher/` or similar — research the actual module location)
- Any config.py in the game data fetcher module
- `tests/` directory — look for game-data-fetcher tests

---

## My Task

**Execute S2.P1 for Feature 03:**

1. **Read guide FIRST:** `feature-updates/guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. **Execute 3 iterations:**
   - **I1:** Discovery (research files, write research notes to `research/F03_game_data_fetcher_cli_research.md`, draft spec.md and checklist.md — then Validation Loop: 3 consecutive clean rounds)
   - **I2:** Checklist resolution (present open questions to user ONE AT A TIME)
   - **I3:** Refinement + Gate 3 user approval
3. **Reference Feature 01 spec** for design pattern guidance
4. **STOP after S2.P1.I3** — Primary runs S2.P2

**Key files in my folder:**
- `feature_03_game_data_fetcher_cli/README.md` — update Agent Status here
- `feature_03_game_data_fetcher_cli/spec.md` — rewrite during I1
- `feature_03_game_data_fetcher_cli/checklist.md` — populate with open questions
- `feature_03_game_data_fetcher_cli/STATUS` — update at phase transitions
- Research notes: `research/F03_game_data_fetcher_cli_research.md`

**Getting Started:**
1. Read `guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. Read `CLAUDE.md` for workflow rules
3. Update Agent Status in `feature_03_game_data_fetcher_cli/README.md`
4. Read Feature 01 spec for design patterns
5. Begin S2.P1.I1 — research `run_game_data_fetcher.py` first
