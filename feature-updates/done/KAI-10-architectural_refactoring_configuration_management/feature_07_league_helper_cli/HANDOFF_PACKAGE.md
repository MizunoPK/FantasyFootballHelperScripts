# Secondary Agent Handoff: Feature 07 — league_helper_cli

## One-Line Startup (paste this to begin)

I'm joining as a secondary agent for the KAI-10 epic (architectural_refactoring_configuration_management). My assignment is Feature 07: league_helper_cli. Please read my HANDOFF_PACKAGE.md at `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_07_league_helper_cli/HANDOFF_PACKAGE.md` and begin S2.P1.

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

**My Agent ID:** Secondary-F
**My Feature Assignment:** Feature 07: league_helper_cli
**My Role:** Execute S2.P1 (3 iterations — I1 Discovery, I2 Checklist Resolution, I3 Refinement)
**Dependency Group:** Wave 2 (Group 2 — runs after Group 1 Feature 01 S2 is complete)
**Stop After:** S2.P1.I3 complete — Primary runs S2.P2 across all Wave 2 features

---

## Group Context

**Why I'm Starting Now:**
- Wave 1 (Feature 01: refactor_player_data_fetcher) has completed S2
- Feature 01's spec is available and defines the design precedents

**Group 1 Spec Available (design reference):**
- `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_01_refactor_player_data_fetcher/spec.md`
- **Key patterns established:**
  - `@dataclass Settings` with `create_settings_from_dict(args_dict)` function
  - Runner uses direct import; calls `asyncio.run(main(settings_dict))`
  - `--debug`, `--e2e-test`, `--log-level` universal args
  - `--my-team-name` arg (consistent between player_fetcher and league_helper per user decision)

**Wave 2 Features Running in Parallel With Me:**
- Feature 02-07 all running simultaneously (Secondary-A through Secondary-F)

---

## Epic Context

**Epic:** KAI-10 — architectural_refactoring_configuration_management
**Epic Goal:** Refactor all 7 runner scripts to CLI-based DI. Zero CLI constants in config files. E2E modes ≤180s each.
**Discovery Doc:** `feature-updates/KAI-10-architectural_refactoring_configuration_management/DISCOVERY.md` (APPROVED)

**Key Constraints:**
- All 2,744+ existing unit tests must pass
- Behavioral equivalence preserved (no-args = same behavior as current)
- E2E test modes must complete in ≤180 seconds

---

## My Feature: Feature 07 — league_helper_cli

**Scope (from Discovery):** Wave 2 — Add ~12 CLI args + 3 universal to `run_league_helper.py`. Largest scope in Wave 2. Must strip `league_helper/constants.py` CLI-configurable values.

**Key scope items:**
- `run_league_helper.py` currently has minimal CLI: only `--enable-log-file`
- Add ~12 script-specific args + 3 universal args (--debug, --e2e-test, --log-level)
- Strip `league_helper/constants.py` CLI-configurable constants → argparse defaults
- 5 interactive modes (draft, optimizer, trade, data editor, waiver) — consider `--mode` arg
- Implement --e2e-test mode completing in ≤180 seconds

**Key Discovery Finding (Finding 3 — league_helper constants):**
- `league_helper/constants.py` CLI-configurable constants:
  - `FANTASY_TEAM_NAME` → `--my-team-name` (same arg name as player_fetcher — per user decision Q3→A)
  - `LOGGING_LEVEL` → `--log-level` (universal)
  - `RECOMMENDATION_COUNT` → `--recommendation-count`
  - `MIN_WAIVER_IMPROVEMENT` → `--min-waiver-improvement`
  - `NUM_TRADE_RUNNERS_UP = 9` → `--num-runners-up`
  - `MIN_TRADE_IMPROVEMENT = 0` → `--min-trade-improvement`

**Additional league_helper args needed (not from constants.py):**
- `--mode` (which of the 5 interactive modes to run)
- `--config-path` (path to league_config.json)
- `--data-folder` (path to player data folder)
- `--league-id` (ESPN fantasy league ID)
- `--team-id` (user's team number)
- `--week` (NFL week to analyze)
- `--season` (NFL season year)
- `--logging-to-file` (enable file logging)
- `--logging-file` (log file path)

**NOTE:** Whether all these become CLI args depends on S2.P1.I1 research — some may be loaded from `league_config.json`. Research actual current behavior.

**Files to Research:**
- `run_league_helper.py` — current argparse, how it calls league_helper/, what's hardcoded
- `league_helper/constants.py` — all constants (CLI vs non-CLI)
- `league_helper/` directory — module structure (5 modes, how they're invoked)
- `league_helper/league_config.json` or similar — what's currently in config files
- `tests/` directory — look for league_helper tests

---

## My Task

**Execute S2.P1 for Feature 07:**

1. **Read guide FIRST:** `feature-updates/guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. **Execute 3 iterations:** I1 (Discovery + Validation Loop), I2 (Checklist Resolution), I3 (Refinement + Gate 3)
3. **Reference Feature 01 spec** for design patterns (especially --my-team-name naming)
4. **Key research focus:** Understand the 5 interactive modes and how --mode arg would work; understand what's in league_config.json vs. constants.py
5. **STOP after S2.P1.I3** — Primary runs S2.P2

**Key files:**
- `feature_07_league_helper_cli/README.md` — update Agent Status here
- `feature_07_league_helper_cli/spec.md` — rewrite during I1
- `feature_07_league_helper_cli/checklist.md` — populate with open questions (likely more Qs than other features due to complexity)
- `feature_07_league_helper_cli/STATUS` — update at phase transitions
- Research notes: `research/F07_league_helper_cli_research.md`

**Getting Started:**
1. Read `guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. Read `CLAUDE.md` for workflow rules
3. Update Agent Status in `feature_07_league_helper_cli/README.md`
4. Read Feature 01 spec for design patterns (especially the Settings dataclass approach)
5. Begin S2.P1.I1 — research `run_league_helper.py` and `league_helper/constants.py` first

**Note on complexity:** Feature 07 has the largest scope in Wave 2 (5 interactive modes, ~15 CLI args, config.json interaction). Expect more open questions in checklist.md. Take extra care to research the league_config.json role vs. argparse — this distinction will drive a key design decision.
