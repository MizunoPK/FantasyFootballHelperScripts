# Secondary Agent Handoff: Feature 02 — schedule_fetcher_cli

## One-Line Startup (paste this to begin)

I'm joining as a secondary agent for the KAI-10 epic (architectural_refactoring_configuration_management). My assignment is Feature 02: schedule_fetcher_cli. Please read my HANDOFF_PACKAGE.md at `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_02_schedule_fetcher_cli/HANDOFF_PACKAGE.md` and begin S2.P1.

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

**My Agent ID:** Secondary-A
**My Feature Assignment:** Feature 02: schedule_fetcher_cli
**My Role:** Execute S2.P1 (3 iterations — I1 Discovery, I2 Checklist Resolution, I3 Refinement)
**Dependency Group:** Wave 2 (Group 2 — runs after Group 1 Feature 01 S2 is complete)
**Stop After:** S2.P1.I3 complete — Primary runs S2.P2 across all Wave 2 features

---

## Group Context

**Why I'm Starting Now:**
- Wave 1 (Feature 01: refactor_player_data_fetcher) has completed S2
- Feature 01's spec is available and defines the design precedents for all Wave 2 features
- I can now specify my feature with knowledge of the established patterns

**Group 1 Spec Available (design reference):**
- `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_01_refactor_player_data_fetcher/spec.md`
- **Key patterns established:**
  - `@dataclass Settings` with `create_settings_from_dict(args_dict)` function
  - Runner uses direct import (not subprocess); calls `asyncio.run(main(settings_dict))`
  - E2E mode: use file if present, skip gracefully if not (Option C)
  - `--debug` flag: DEBUG logging + data limiting
  - `--log-level` universal arg (choices: DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - `--e2e-test` flag: data limits + ≤180s completion

**Wave 2 Features Running in Parallel With Me:**
- Feature 02: schedule_fetcher_cli (me — Secondary-A)
- Feature 03: game_data_fetcher_cli (Secondary-B)
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
**EPIC_README:** `feature-updates/KAI-10-architectural_refactoring_configuration_management/EPIC_README.md`

**Key Constraints:**
- All 2,744+ existing unit tests must pass after any refactoring
- Behavioral equivalence preserved (no-args = same behavior as current)
- argparse defaults = single source of truth (no constants in config files)
- E2E test modes must complete in ≤180 seconds

---

## My Feature: Feature 02 — schedule_fetcher_cli

**Scope (from Discovery):** Wave 2 — Add CLI args to `run_schedule_fetcher.py` + debug/E2E modes.

**Key scope items (from Discovery):**
- Add argparse to `run_schedule_fetcher.py`: --season, --output-path, --data-folder, plus universal args
- Add universal args: --debug, --e2e-test, --log-level
- Remove `NFL_SEASON=2025` hardcoded directly in runner (replace with argparse default)
- schedule-data-fetcher/ has NO config.py — only `ScheduleFetcher.py`
- Implement --e2e-test mode completing in ≤180 seconds
- Implement --debug mode (DEBUG logging + reduced data scope)

**Key Discovery Finding (Finding 5):**
- `schedule-data-fetcher/` has only `ScheduleFetcher.py` (no config.py)
- NFL_SEASON=2025 is hardcoded directly in `run_schedule_fetcher.py` (not from a config import)
- Current CLI: only `--enable-log-file`

**Files to Research:**
- `run_schedule_fetcher.py` — current argparse, subprocess/import pattern, hardcoded values
- `schedule-data-fetcher/ScheduleFetcher.py` — constructor, parameters, any hardcoded constants
- `tests/` directory — look for schedule-related tests

---

## My Task

**Execute S2.P1 for Feature 02:**

1. **Read guide FIRST:** `feature-updates/guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. **Execute 3 iterations:**
   - **I1:** Discovery (research files, write research notes to `research/F02_schedule_fetcher_cli_research.md`, draft spec.md and checklist.md — then Validation Loop: 3 consecutive clean rounds)
   - **I2:** Checklist resolution (present open questions to user ONE AT A TIME, update spec per answers)
   - **I3:** Refinement + Alignment (finalize spec, Acceptance Criteria, Gate 2 + Gate 3 user approval)
3. **Reference Feature 01 spec** for design pattern guidance (not structural dependency)
4. **Update STATUS file** at phase transitions
5. **STOP after S2.P1.I3** — Primary runs S2.P2 across all Wave 2 features

**Important reminders:**
- NEVER mark checklist items RESOLVED autonomously — only user answers trigger resolution
- Gate 3 requires explicit user approval of spec.md + checklist.md
- Research notes go in the epic `research/` folder
- Update Agent Status in `feature_02_schedule_fetcher_cli/README.md` at each phase

---

## Key Files in My Feature Folder

- `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_02_schedule_fetcher_cli/README.md` — update Agent Status here
- `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_02_schedule_fetcher_cli/spec.md` — has stub content from S1, rewrite during I1
- `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_02_schedule_fetcher_cli/checklist.md` — populate with open questions during I1
- `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_02_schedule_fetcher_cli/STATUS` — update at phase transitions

**Research notes:** `feature-updates/KAI-10-architectural_refactoring_configuration_management/research/F02_schedule_fetcher_cli_research.md`

---

## Getting Started

**First 5 actions:**
1. Read `feature-updates/guides_v2/stages/s2/s2_p1_spec_creation_refinement.md` (full guide)
2. Read `CLAUDE.md` for workflow rules (critical anti-patterns to avoid)
3. Update Agent Status in `feature_02_schedule_fetcher_cli/README.md`
4. Read Feature 01 spec: `feature_01_refactor_player_data_fetcher/spec.md` (design patterns)
5. Begin S2.P1.I1 (Discovery — research run_schedule_fetcher.py and ScheduleFetcher.py)

**Remember:** You're in Wave 2, which started after Wave 1 (Feature 01) completed S2. Feature 01's established patterns (dataclass Settings, direct import, graceful E2E file handling) are the reference design for your feature too.
