# Secondary Agent Handoff: Feature 04 — historical_compiler_cli

## One-Line Startup (paste this to begin)

I'm joining as a secondary agent for the KAI-10 epic (architectural_refactoring_configuration_management). My assignment is Feature 04: historical_compiler_cli. Please read my HANDOFF_PACKAGE.md at `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_04_historical_compiler_cli/HANDOFF_PACKAGE.md` and begin S2.P1.

---

## Agent Configuration

**My Agent ID:** Secondary-C
**My Feature Assignment:** Feature 04: historical_compiler_cli
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
  - E2E mode: use file if present, skip gracefully if not
  - `--debug` flag: DEBUG logging + data limiting
  - `--log-level` universal arg (choices: DEBUG, INFO, WARNING, ERROR, CRITICAL)

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

## My Feature: Feature 04 — historical_compiler_cli

**Scope (from Discovery):** Wave 2 — Extend CLI args in `compile_historical_data.py` + strip constants.py.

**Key scope items:**
- `compile_historical_data.py` currently has 4 args: --year, --verbose, --enable-log-file, --output-dir
- Add universal args: --debug, --e2e-test, --log-level
- Strip `historical_data_compiler/constants.py` CLI-configurable constants → argparse defaults
- Implement --e2e-test mode completing in ≤180 seconds
- Implement --debug mode

**Key Discovery Finding (Finding 7):**
- Current args: `--year` (NFL season), `--verbose`, `--enable-log-file`, `--output-dir`
- Missing: `--debug`, `--e2e-test`, `--log-level`, `--timeout`, `--rate-limit-delay`
- `historical_data_compiler/constants.py` CLI-configurable values:
  - `REQUEST_TIMEOUT = 30.0` → `--timeout`
  - `RATE_LIMIT_DELAY = 0.3` → `--rate-limit-delay`

**Files to Research:**
- `compile_historical_data.py` — current argparse, structure, how it calls the module
- `historical_data_compiler/` directory — module structure, constants.py, any config
- `tests/` directory — look for historical-compiler tests

---

## My Task

**Execute S2.P1 for Feature 04:**

1. **Read guide FIRST:** `feature-updates/guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. **Execute 3 iterations:** I1 (Discovery + Validation Loop), I2 (Checklist Resolution), I3 (Refinement + Gate 3)
3. **Reference Feature 01 spec** for design patterns
4. **STOP after S2.P1.I3** — Primary runs S2.P2

**Key files:**
- `feature_04_historical_compiler_cli/README.md` — update Agent Status here
- `feature_04_historical_compiler_cli/spec.md` — rewrite during I1
- `feature_04_historical_compiler_cli/checklist.md` — populate with open questions
- `feature_04_historical_compiler_cli/STATUS` — update at phase transitions
- Research notes: `research/F04_historical_compiler_cli_research.md`

**Getting Started:**
1. Read `guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. Read `CLAUDE.md` for workflow rules
3. Update Agent Status in `feature_04_historical_compiler_cli/README.md`
4. Read Feature 01 spec for design patterns
5. Begin S2.P1.I1 — research `compile_historical_data.py` and `historical_data_compiler/constants.py`
