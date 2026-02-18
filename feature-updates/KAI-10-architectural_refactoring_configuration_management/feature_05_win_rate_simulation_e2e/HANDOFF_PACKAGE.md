# Secondary Agent Handoff: Feature 05 — win_rate_simulation_e2e

## One-Line Startup (paste this to begin)

I'm joining as a secondary agent for the KAI-10 epic (architectural_refactoring_configuration_management). My assignment is Feature 05: win_rate_simulation_e2e. Please read my HANDOFF_PACKAGE.md at `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_05_win_rate_simulation_e2e/HANDOFF_PACKAGE.md` and begin S2.P1.

---

## Agent Configuration

**My Agent ID:** Secondary-D
**My Feature Assignment:** Feature 05: win_rate_simulation_e2e
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
  - Runner direct import pattern; calls `asyncio.run(main(settings_dict))`
  - E2E mode: use file if present, skip gracefully if not
  - `--debug` flag: DEBUG logging + data limiting
  - `--log-level` universal arg (choices: DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - `--e2e-test` flag: data limits + ≤180s completion

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

## My Feature: Feature 05 — win_rate_simulation_e2e

**Scope (from Discovery):** Wave 2 — Add 3 universal CLI args to `run_win_rate_simulation.py` which already has 17 args. Focus is on E2E test mode implementation.

**Key scope items:**
- `run_win_rate_simulation.py` currently has 17 CLI args (comprehensive)
- Add 3 missing universal args: --debug, --e2e-test, --log-level
- Implement --e2e-test mode completing in ≤180 seconds (key challenge: simulation is compute-intensive)
- Implement --debug mode (DEBUG logging + reduced scope)
- Research any config/constants files in simulation/ module

**Key Discovery Finding (Finding 8):**
- `run_win_rate_simulation.py` does NOT have --log-level, --debug, or --e2e-test
- All 3 universal args are missing (contrast with Feature 06 accuracy_simulation which already has --log-level)
- The simulation is computationally intensive — E2E mode needs a data-limiting strategy

**IMPORTANT:** The E2E test mode for simulation is more complex than for data fetching scripts. Research how to limit the simulation to complete in ≤180 seconds (e.g., fewer iterations, smaller dataset).

**Files to Research:**
- `run_win_rate_simulation.py` — full current argparse, what the 17 args do, how it calls simulation/
- `simulation/` directory — module structure, any constants, how simulation params are passed
- `tests/` directory — look for simulation tests

---

## My Task

**Execute S2.P1 for Feature 05:**

1. **Read guide FIRST:** `feature-updates/guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. **Execute 3 iterations:** I1 (Discovery + Validation Loop), I2 (Checklist Resolution), I3 (Refinement + Gate 3)
3. **Reference Feature 01 spec** for design patterns
4. **Key open question to investigate:** How does E2E test mode limit the win rate simulation to ≤180 seconds? (Reduced iterations? Different dataset? User will answer.)
5. **STOP after S2.P1.I3** — Primary runs S2.P2

**Key files:**
- `feature_05_win_rate_simulation_e2e/README.md` — update Agent Status here
- `feature_05_win_rate_simulation_e2e/spec.md` — rewrite during I1
- `feature_05_win_rate_simulation_e2e/checklist.md` — populate with open questions
- `feature_05_win_rate_simulation_e2e/STATUS` — update at phase transitions
- Research notes: `research/F05_win_rate_simulation_e2e_research.md`

**Getting Started:**
1. Read `guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. Read `CLAUDE.md` for workflow rules
3. Update Agent Status in `feature_05_win_rate_simulation_e2e/README.md`
4. Read Feature 01 spec for design patterns
5. Begin S2.P1.I1 — research `run_win_rate_simulation.py` first
