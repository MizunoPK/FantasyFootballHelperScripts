# Shamt Epic Workflow — Comprehensive Usage Guide

This file provides a complete overview of the Shamt S1-S10 epic-driven development workflow.

**For stage-specific detail:** Read the full guide for each stage (listed below).
**For phase transition prompts:** See `prompts_reference_v2.md` or `prompts/`

---

## Prerequisites: Epic Request Files

**BEFORE starting S1,** epic requests must be created in `.shamt/epics/requests/`

### Creating an Epic Request

1. User describes the epic they want to build
2. Agent creates `.shamt/epics/requests/{name}.md` or `.txt`
3. Agent writes high-level request document:
   - Requirements, goals, constraints, research findings
   - Focus on WHAT needs to be done, not HOW to implement
   - Mention files/areas that MAY need changes (not specific code)
   - Reference coding practices to follow
   - **DO NOT** include code snippets or detailed implementation
4. File remains in `requests/` folder

**DO NOT create SHAMT-{N} folders at this stage. The S1-S10 flow will determine detailed design.**

### Starting S1

1. User says "Start S1 for [epic request name]"
2. Agent verifies request file exists in `.shamt/epics/requests/`
3. Agent reads `stages/s1/s1_epic_planning.md`
4. Agent creates git branch and SHAMT-{N} folder **during S1** (not before)

**SHAMT-{N} folders are ONLY created during S1 execution, never as part of request creation.**

---

## Workflow Overview

```text
S1: Epic Planning → S2: Feature Deep Dives → S3: Epic-Level Docs, Tests, and Approval →
S5-S8: Feature Loop (S4 deprecated — Test Scope Decision in S5 Step 0) → S9: Epic Final QC → S10: Epic Cleanup

Per-feature loop: S5 (Plan) → S6 (Execute) → S7 (Test) → S8 (Align) → repeat or S9
```

**Notation:**
- **S#** = Stage (e.g., S1, S5)
- **S#.P#** = Phase (e.g., S2.P1, S5.P1)
- **S#.P#.I#** = Iteration (e.g., S5.P1.I2)

---

## Stage-by-Stage Detailed Workflows

### S1: Epic Planning

**Guide:** `stages/s1/s1_epic_planning.md`

Key activities:
- Assign SHAMT number (ask user for next available or custom)
- Create epic folder and EPIC_README.md
- Create git branch: `{work_type}/{EPIC_TAG}-{N}`
- Run S1.P3 Discovery Phase (MANDATORY — research loop until 3 consecutive clean iterations)
- Break epic into features
- Get user approval on feature breakdown

**Outputs:** Epic folder, EPIC_README.md, feature folder structure, git branch

---

### S2: Feature Deep Dives

**Guide:** `stages/s2/s2_feature_deep_dive.md`

Key activities:
- For each feature: create `spec.md`, `checklist.md`, `RESEARCH_NOTES.md`
- Run S2.P1 Spec Creation Refinement Validation Loop (Gates 1, 2, 3)
- Gate 3: User approval of acceptance criteria (in S2.P1.I3, before S5)
- S2.P2: Cross-Feature Alignment — pairwise comparison of all feature specs to resolve conflicts (Primary agent only; runs after all features complete S2.P1)

**Parallelization option:** `parallel_work/s2_parallel_protocol.md` (3+ features)

**Outputs:** `spec.md`, `checklist.md`, `RESEARCH_NOTES.md` per feature; cross-feature conflict resolutions

---

### S3: Epic-Level Docs, Tests, and Approval

**Guide:** `stages/s3/s3_epic_planning_approval.md`

Key activities:
- S3.P1: Create epic smoke test plan (integration tests spanning ALL features)
- S3.P2: Refine EPIC_README.md with feature summaries and architecture decisions
- S3.P3: Gate 4.5 — present epic plan to user, mandatory approval before S5 (S4 deprecated)

**Outputs:** `epic_smoke_test_plan.md`, refined `EPIC_README.md`, Gate 4.5 approval

---

### S4: (Deprecated)

**Guide:** `stages/s4/s4_feature_testing_strategy.md` (redirect stub)

S4 has been deprecated. Test Scope Decision (what to test per feature) is now Step 0 of S5. The Testing Approach (A/B/C/D) is set at S1 Step 4.6.5.

**Next stage after S3:** S5 (skip S4 entirely)

---

### S5: Implementation Planning (Per Feature)

**Guide:** `stages/s5/s5_v2_validation_loop.md`

Two-phase approach:
1. **Draft Creation** (60-90 min): Write `implementation_plan.md`
2. **Validation Loop** (3.5-6 hours): 11 dimensions, 3 consecutive clean rounds required

Gate 5: User approval of implementation plan (3-tier rejection handling)

**Outputs:** `implementation_plan.md` (user-approved)

---

### S6: Execution (Per Feature)

**Guide:** `stages/s6/s6_execution.md`

Key activities:
- Create `implementation_checklist.md`
- Implement code following implementation plan
- Track progress in checklist

**Outputs:** Implemented code, `implementation_checklist.md`

---

### S7: Testing and Review (Per Feature)

**Guides:**
- `stages/s7/s7_p1_smoke_testing.md` — S7.P1 Smoke Testing
- `stages/s7/s7_p2_qc_rounds.md` — S7.P2 QC Rounds (3 rounds)
- `stages/s7/s7_p3_final_review.md` — S7.P3 Final Review

**Protocol:** S7.P2 uses fix-and-continue (fix issues immediately, reset clean counter, no restart). S7.P1 failure or S7.P3 critical issues → restart from S7.P1.

**Outputs:** Feature committed to git, `lessons_learned.md`

---

### S8: Cross-Feature Alignment (Per Feature)

**Guides:**
- `stages/s8/s8_p1_cross_feature_alignment.md` — Update remaining feature specs
- `stages/s8/s8_p2_epic_testing_update.md` — Update epic smoke test plan

**After S8:** Either start S5 for next feature (if more features) or proceed to S9

---

### S9: Epic Final QC

**Guide:** `stages/s9/s9_epic_final_qc.md`

**Guides:**
- `stages/s9/s9_p1_epic_smoke_testing.md` — Epic smoke test
- `stages/s9/s9_p2_epic_qc_rounds.md` — Epic QC Validation Loop (3 rounds)
- `stages/s9/s9_p3_user_testing.md` — User testing (ZERO bugs required)
- `stages/s9/s9_p4_epic_final_review.md` — Final review

**🚨 Restart Protocol:** If ANY issues found → restart from S9.P1

**Exit criteria:** User reports ZERO bugs, all tests pass

---

### S10: Epic Cleanup

**Guide:** `stages/s10/s10_epic_cleanup.md`

Key activities:
- Run unit tests (100% pass required)
- Verify all documentation
- S10.P1 Guide Updates (MANDATORY — analyze lessons, propose changes, get user approval, apply, update CHANGES.md and inform user of export opportunity if improvements are generic)
- Commit epic work
- Move epic to `done/` folder
- Update `EPIC_TRACKER.md`
- Create PR for user review

---

## Setup and First Use

1. Initialize Shamt in your project: run `init.sh` or `init.ps1` from `.shamt/scripts/initialization/`
2. Tell your AI agent: "Read `.shamt/project-specific-configs/init_config.md` and complete the Shamt initialization."
3. Start your first epic: tell your agent "Help me develop [epic description]"
4. Agent starts at S1 — reads `stages/s1/s1_epic_planning.md`

---

## Common Patterns

### Starting a New Epic
- Agent starts S1, assigns next SHAMT number, creates branch
- Runs Discovery Phase (S1.P3) — research loop
- Breaks epic into features, gets user approval

### Resuming In-Progress Work
- Check `.shamt/epics/` for active epic folders
- Read EPIC_README.md → Agent Status section
- Read the guide listed in Agent Status
- Continue from exact step listed

### Debugging Protocol
When issue root cause is unknown: `debugging/debugging_protocol.md`

### Missed Requirement Protocol
When new requirement discovered: `missed_requirement/missed_requirement_protocol.md`

---

## Quick Reference

**Phase transition prompts (MANDATORY):** `prompts_reference_v2.md` or `prompts/`

**Gate reference:** `reference/mandatory_gates.md`

**Common mistakes:** `reference/common_mistakes.md`

**Git conventions:** `reference/GIT_WORKFLOW.md`

**Decision tree:** `reference/PROTOCOL_DECISION_TREE.md`

**Audit system:** `audit/README.md`

**Sync system:** `sync/` — separation rule, export workflow, import workflow
