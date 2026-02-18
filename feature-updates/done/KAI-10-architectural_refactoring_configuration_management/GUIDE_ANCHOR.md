## Guide Anchor: KAI-10 — architectural_refactoring_configuration_management

**Purpose:** Resumption instructions for new agents joining this epic mid-workflow.

**Created:** 2026-02-18 (S1)
**Last Updated:** 2026-02-18

---

## How to Resume This Epic

If you are a new agent resuming this epic after a session interruption:

### Step 1: Read EPIC_README.md FIRST

```
Read: feature-updates/KAI-10-architectural_refactoring_configuration_management/EPIC_README.md
```

The EPIC_README.md contains the **Agent Status** section with:
- Current Stage (S#.P# notation)
- Current Step (exactly where work stopped)
- Next Action (exactly what to do next)
- Current Guide (which guide file to read)
- Debugging Active field (check for active debugging sessions)

### Step 2: Check for Active Debugging

Look for a `debugging/` folder in the epic or any feature folder:
```
Glob: feature-updates/KAI-10-*/debugging/
```

If found, read `debugging/ISSUES_CHECKLIST.md` before anything else. Active debugging takes priority over Agent Status.

### Step 3: Read the Current Guide

Use the guide path listed in Agent Status:
```
Read: feature-updates/guides_v2/stages/[guide_path]
```

Do NOT skip this. Reading the guide ensures you don't miss mandatory steps.

### Step 4: Continue From Where Work Stopped

Follow the guide step-by-step from the step listed in "Current Step" in Agent Status.

---

## Epic Overview

**KAI Number:** KAI-10
**Epic:** architectural_refactoring_configuration_management
**Branch:** epic/KAI-10
**Status:** IN PROGRESS

**Goal:** Refactor all 7 runner scripts from scattered hardcoded configuration to CLI-based configuration with dependency injection. Zero CLI constants in config files, constructor parameter pattern throughout, E2E test modes ≤180s each, integration test framework, 2,744+ unit tests passing.

**8 Features:**
- Feature 01: refactor_player_data_fetcher (Wave 1 — solo, sets design precedents)
- Features 02-07: schedule_fetcher_cli, game_data_fetcher_cli, historical_compiler_cli, win_rate_simulation_e2e, accuracy_simulation_e2e, league_helper_cli (Wave 2 — parallel, reference F01 spec)
- Feature 08: integration_test_framework (Wave 3 — after all features)

**Key Documents:**
- `DISCOVERY.md` — Research findings and feature breakdown (user-approved)
- `EPIC_TICKET.md` — Acceptance criteria and success indicators (user-approved)
- `epic_smoke_test_plan.md` — How to validate the complete epic
- `epic_lessons_learned.md` — Cross-feature insights (filled throughout)

---

## S2 Wave Structure

**This epic uses group-based S2 parallelization (3 waves):**

| Wave | Features | Parallelization | Start Condition |
|------|----------|-----------------|-----------------|
| Wave 1 | Feature 01 | Solo | Start immediately |
| Wave 2 | Features 02-07 | All parallel | Feature 01 S2 complete |
| Wave 3 | Feature 08 | Solo | Features 01-07 S2 all complete + S3 + S4 done |

**Relevant guides:**
- Primary agent: `feature-updates/guides_v2/parallel_work/s2_primary_agent_group_wave_guide.md`
- Secondary agents: `feature-updates/guides_v2/parallel_work/s2_secondary_agent_guide.md`

---

## Stage Workflow (CLAUDE.md Reference)

| Stage | Guide |
|-------|-------|
| S1 (current) | `stages/s1/s1_epic_planning.md` |
| S2 | `stages/s2/s2_feature_deep_dive.md` |
| S3 | `stages/s3/s3_epic_planning_approval.md` |
| S4 | `stages/s4/s4_feature_testing_strategy.md` |
| S5 | `stages/s5/s5_v2_validation_loop.md` |
| S6 | `stages/s6/s6_execution.md` |
| S7 | `stages/s7/s7_p1_smoke_testing.md` |
| S8 | `stages/s8/s8_p1_cross_feature_alignment.md` |
| S9 | `stages/s9/s9_epic_final_qc.md` |
| S10 | `stages/s10/s10_epic_cleanup.md` |

All paths relative to: `feature-updates/guides_v2/`
