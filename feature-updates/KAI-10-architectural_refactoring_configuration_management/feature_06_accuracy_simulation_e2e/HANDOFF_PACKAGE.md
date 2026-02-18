# Secondary Agent Handoff: Feature 06 — accuracy_simulation_e2e

## One-Line Startup (paste this to begin)

I'm joining as a secondary agent for the KAI-10 epic (architectural_refactoring_configuration_management). My assignment is Feature 06: accuracy_simulation_e2e. Please read my HANDOFF_PACKAGE.md at `feature-updates/KAI-10-architectural_refactoring_configuration_management/feature_06_accuracy_simulation_e2e/HANDOFF_PACKAGE.md` and begin S2.P1.

---

## Agent Configuration

**My Agent ID:** Secondary-E
**My Feature Assignment:** Feature 06: accuracy_simulation_e2e
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
  - E2E mode: data limits + ≤180s completion
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
- E2E test modes must complete in ≤180 seconds

---

## My Feature: Feature 06 — accuracy_simulation_e2e

**Scope (from Discovery):** Wave 2 — Add 2 missing universal args to `run_accuracy_simulation.py` (which already has 10 args including --log-level). Focus is on E2E and debug mode.

**Key scope items:**
- `run_accuracy_simulation.py` currently has 10 CLI args including --log-level
- Add 2 missing universal args: --debug, --e2e-test
- Note: --log-level ALREADY EXISTS with choices: debug/info/warning/error (may need normalization to uppercase choices to match universal standard)
- Implement --e2e-test mode completing in ≤180 seconds
- Implement --debug mode (DEBUG logging + reduced scope)
- Research any config/constants files in simulation/ module

**Key Discovery Finding (Finding 8):**
- `run_accuracy_simulation.py` ALREADY HAS `--log-level` (choices: debug/info/warning/error)
- Missing: `--debug`, `--e2e-test`
- Existing --log-level may use lowercase choices — investigate whether to normalize to uppercase (DEBUG/INFO/...) for consistency with universal arg standard

**IMPORTANT OPEN QUESTION to investigate:** Does the existing --log-level need to be updated for consistency with the universal `--log-level` standard (which uses uppercase choices: DEBUG, INFO, WARNING, ERROR, CRITICAL)? Research the current implementation first.

**Files to Research:**
- `run_accuracy_simulation.py` — full current argparse, what the 10 args do, --log-level current implementation
- `simulation/` directory — module structure, any constants, how simulation params are passed
- `tests/` directory — look for accuracy simulation tests

---

## My Task

**Execute S2.P1 for Feature 06:**

1. **Read guide FIRST:** `feature-updates/guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. **Execute 3 iterations:** I1 (Discovery + Validation Loop), I2 (Checklist Resolution), I3 (Refinement + Gate 3)
3. **STOP after S2.P1.I3** — Primary runs S2.P2

**Key files:**
- `feature_06_accuracy_simulation_e2e/README.md` — update Agent Status here
- `feature_06_accuracy_simulation_e2e/spec.md` — rewrite during I1
- `feature_06_accuracy_simulation_e2e/checklist.md` — populate with open questions
- `feature_06_accuracy_simulation_e2e/STATUS` — update at phase transitions
- Research notes: `research/F06_accuracy_simulation_e2e_research.md`

**Getting Started:**
1. Read `guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
2. Read `CLAUDE.md` for workflow rules
3. Update Agent Status in `feature_06_accuracy_simulation_e2e/README.md`
4. Read Feature 01 spec for design patterns
5. Begin S2.P1.I1 — research `run_accuracy_simulation.py` first (pay close attention to existing --log-level implementation)
