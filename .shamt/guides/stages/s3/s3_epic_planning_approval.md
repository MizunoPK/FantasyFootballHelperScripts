# S3: Epic-Level Documentation, Testing Plans, and Approval

> **SCOPE:** This stage runs **once per epic**, after S2 is complete for ALL features. It is not
> repeated per feature. Working directory is the **epic folder root**, not a feature folder.

🚨 **MANDATORY READING PROTOCOL**

**Before starting this stage — including when resuming a prior session:**
1. **Quick entry point:** `reference/stage_3/stage_3_reference_card.md` — covers the happy path including Gate 4.5; S3 runs once per epic
2. **Full guide (this file):** Read entirely for detailed examples or when encountering edge cases
3. Verify prerequisites (S2 complete for ALL features)
4. Update epic EPIC_README.md Agent Status with guide name + timestamp

---

## 🚫 FORBIDDEN SHORTCUTS

You CANNOT:
- Skip S3.P1 (Testing Strategy) and proceed directly to P3 approval
- Draft the testing strategy from general knowledge rather than following S3.P1 Steps 1–5
- Skip S3.P2 (Epic Documentation Refinement) because docs appear complete
- Present the epic plan for approval (P3) before completing both P1 and P2

If you are about to do any of the above: STOP and re-read the relevant section.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Overview](#overview)
- [S3.P1: Epic Testing Strategy Development](#s3p1-epic-testing-strategy-development-45-60-min)
- [S3.P2: Epic Documentation Refinement](#s3p2-epic-documentation-refinement-20-30-min)
- [S3.P3: Epic Plan Approval](#s3p3-epic-plan-approval-10-15-min)
- [Exit Criteria](#exit-criteria)
- [Next: S5 (Implementation Planning)](#next-stage)

---

## Prerequisites

**Before starting S3:**

- [ ] S2 completed for ALL features in the epic
- [ ] All feature spec.md files have acceptance criteria (user-approved)
- [ ] S2.P2 (Cross-Feature Alignment) completed
- [ ] EPIC_README.md Feature Tracking shows all S2 checkboxes marked
- [ ] epic_smoke_test_plan.md exists (initial version from S1)
- [ ] Working directory: Epic folder root

**If any prerequisite fails:**
- Complete missing S2 work before proceeding
- Do NOT start S3 until all features have completed S2

---

## Overview

**Purpose:** Create epic-level testing strategy, refine epic documentation, get user approval (Gate 4.5)

**Structure:** 3 phases
- S3.P1: Epic Testing Strategy Development (45-60 min)
- S3.P2: Epic Documentation Refinement (20-30 min)
- S3.P3: Epic Plan Approval (10-15 min) - Gate 4.5 with 3-tier rejection handling

**Time:** 75-105 minutes total
**Prerequisites:** S2 complete for ALL features (S2.P2 alignment done)

---

## S3.P1: Epic Testing Strategy Development

⚠️ **Before starting P1, confirm:**
- [ ] S3.P2 (Epic Documentation Refinement) is mandatory after P1 — I will not skip it
- [ ] S3.P3 (Epic Plan Approval) is mandatory after P2 — I will not present for approval mid-phase
- [ ] I will complete all three phases before Gate 4.5

P1 produces the testing strategy. P2 refines documentation. P3 is the gate. All three are required.

---

### First: Read the Epic's Testing Approach

Before starting S3.P1, read `Testing Approach:` from EPIC_README. The approach was set at S1.

**If Option A or C (no integration scripts):** Run the full S3.P1 process (45-60 min) as described below.

**If Option B or D (integration scripts opted in):** Run the trimmed S3.P1 process (10-15 min) — jump to [S3.P1 Trimmed Process (Options B/D)](#s3p1-trimmed-process-options-bd) below.

---

### S3.P1 Full Process (Options A/C — 45-60 min)

**Purpose:** Create epic_smoke_test_plan.md for end-to-end integration testing when all features complete

> **This is NOT per-feature test planning.** Tests defined here span multiple features and verify
> end-to-end workflows across the whole epic. Per-feature tests are designed in S5 (Test Scope Decision).
> If you find yourself writing tests for a single feature's internal behavior, stop — that belongs in S5.

### What Epic-Level Tests Cover

**Epic-Level Tests (S3):**
- End-to-end workflows across ALL features
- Integration points between features
- Epic-level success criteria
- Data flow through complete system

**Key Distinction:** S3 tests ACROSS features, S5 designs WITHIN features

### Steps

**1. Review All Feature Specs for Integration Scenarios (10-15 min)**
- Read each feature's spec.md test section
- Identify epic-level integration scenarios
- Note dependencies between features
- Identify end-to-end workflows

**2. Identify Integration Points (15-20 min)**

Create integration point map with details:

```markdown
## Integration Points Identified

### Integration Point 1: {Name}
**Features Involved:** {list features}
**Type:** {Shared data structure | Computational dependency | File system | API}
**Flow:**
- Feature X: {what it does}
- Feature Y: {what it does}
- Feature Z: {what it depends on}

**Test Need:** {What needs to be verified}

[Continue for each integration point...]
```

**3. Define Epic Success Criteria (15-20 min)**

Convert vague goals to MEASURABLE criteria:

```markdown
## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: {Criterion Name}
✅ **MEASURABLE:** {Specific, measurable condition}

**Verification:** {How to verify (command, observation, test)}

[Continue for each criterion...]
```

**4. Create Specific Test Scenarios (15-25 min)**

Convert high-level categories to concrete tests with commands:

```markdown
## Specific Test Scenarios

### Test Scenario 1: {Name}

**Purpose:** {What this test verifies}

**Steps:**
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Expected Results:**
✅ {Expected result 1}
✅ {Expected result 2}
✅ {Expected result 3}

**Failure Indicators:**
❌ {What error means}
❌ {What failure means}

**Command to verify:**
~~~bash
{Actual command to run}
~~~

[Continue for each test scenario...]
```

**5. Update epic_smoke_test_plan.md (10-15 min)**
- Replace S1 placeholder content with concrete scenarios
- Add all integration points
- Add all success criteria
- Add all test scenarios
- Mark as "S3 version - will update in S8.P2 (Epic Testing Update)"

**6. Validation Loop Validation (15-20 min)**

**Reference:** `reference/validation_loop_master_protocol.md`

- **Round 1:** Check test plan completeness
  - All features integrated in tests?
  - All integration points tested?
  - End-to-end scenarios complete?
  - Edge cases across features included?
  - Exit criteria clear?
- **Round 2:** Fresh review, find gaps in coverage
- **Round 3:** Final validation, spot-check scenarios
- **Exit:** 3 consecutive clean rounds

**Outputs:**
- epic_smoke_test_plan.md (validated, epic-level integration tests with detailed scenarios)

---

### S3.P1 Trimmed Process (Options B/D — 10-15 min)

**Rationale:** When integration scripts are opted in, the scripts themselves (designed at S5, built at S6, run at S9) collectively constitute the epic-level test strategy. A 45-60 minute planning document produced before any features are implemented adds overhead without adding coverage — the same problem S4 had at the feature level. The scripts will cover integration behavior with far more precision than a plan written before any code exists.

**What to do:**

1. **Define epic success criteria only (3-5 measurable conditions):**
   These describe overall epic health — different from per-feature assertions.

   Examples: "All output files present with non-zero row counts", "cross-feature totals are consistent across all features", "all integration scripts pass with exit code 0"

2. **Create a minimal epic_smoke_test_plan.md with just the success criteria section:**
   - Header and purpose
   - Epic success criteria (3-5 conditions from step 1)
   - Note: "Integration test scripts (designed at S5, built at S6) are the feature-level test strategy. This document captures epic-level success criteria only."
   - Do NOT enumerate per-feature test scenarios or integration points — the scripts will cover these once implementation is known
   - Mark as "S3 version (B/D) - integration scripts are the test strategy; update in S8.P2"

3. **No validation loop on this document at S3.** The integration scripts themselves are validated through S7 execution and S9 epic-level run.

**Outputs:**
- epic_smoke_test_plan.md (minimal — success criteria only; scripts are the strategy)

---

## S3.P2: Epic Documentation Refinement (20-30 min)

### Purpose
Refine epic ticket with details from all developed feature specs

### Steps

**1. Consolidate Feature Details (10-15 min)**
- Read all feature spec.md files
- Extract key approaches, data structures, integration points
- Identify epic-level patterns

**2. Update Epic Ticket (10-15 min)**
- Enhance `EPIC_README.md` or epic ticket
- Add feature summary section (1-2 sentences per feature)
- Document epic-level architecture decisions
- Clarify scope boundaries

**3. Validation Loop Validation (15-20 min)**

**Reference:** `reference/validation_loop_spec_refinement.md`

- **Round 1:** Check epic documentation completeness
  - All features described?
  - Architecture decisions documented?
  - Scope boundaries clear?
  - Integration approach explained?
- **Round 2:** Fresh review, different reading patterns
- **Round 3:** Final validation
- **Exit:** 3 consecutive clean rounds

**Outputs:**
- EPIC_README.md (updated with feature details)

---

## S3.P3: Epic Plan Approval (10-15 min)

### Purpose
Get user approval for complete epic plan before proceeding to S5 (Gate 4.5 — S4 is deprecated)

### Steps

**1. Create Epic Summary (5-10 min)**
- Consolidate all feature specs
- List all features with 1-sentence descriptions
- Summarize epic test plan approach
- Estimate total timeline (feature count × ~6-8 hours)

**2. Gate 4.5: User Approval of Epic Plan (5 min)**
- Present epic summary to user
- Present epic_smoke_test_plan.md
- Ask: "Approve this epic plan and testing approach confirmed?"
- **MANDATORY GATE:** Cannot proceed without approval
- **Note:** Single Gate 4.5 (not split into 4.5a/4.5b per user direction)
- Gate 4.5 checklist includes: testing approach confirmed (A/B/C/D set in EPIC_README) + epic plan approved

### If User Requests Changes

**Option A: Update epic_smoke_test_plan.md or EPIC_README.md based on feedback**
- LOOP BACK to appropriate phase:
  - If testing strategy issues → S3.P1
  - If documentation issues → S3.P2
  - If fundamental approach wrong → S2 (cross-feature conflicts need re-resolution)
- Re-run updated phase with Validation Loop
- Re-present to user for approval (Gate 4.5 again)

### If User Rejects Entire Epic Approach

**User says:** "This epic scope/approach is fundamentally wrong"

**STOP - Do not loop back to S3**

**3-Tier Rejection Handling:**

Ask user for guidance:
1. **(A) Re-do Discovery Phase (S1.P3)** - research was incomplete
2. **(B) Revise feature breakdown (S1.P4)** - features defined incorrectly
3. **(C) Exit epic planning** - epic should not proceed

Await user decision before proceeding.

**Rationale:** Total rejection indicates problem earlier than S3, not refinement issue

**Outputs:**
- EPIC_SUMMARY.md (optional, for user reference)
- User approval obtained

**Exit Condition:**
- User explicitly approves epic plan
- Gate 4.5 passed
- Ready to proceed to S5 (first feature)

---

## Exit Criteria

**S3 complete when ALL true:**

- [ ] S3.P1 complete (epic_smoke_test_plan.md created/updated per testing approach)
- [ ] S3.P2 complete (EPIC_README.md refined and validated)
- [ ] S3.P3 complete (Gate 4.5 passed - user approved epic plan + testing approach confirmed)
- [ ] Epic EPIC_README.md updated with:
  - Epic Completion Checklist: S3 items checked
  - Agent Status: Phase = S5_READY
- [ ] epic_smoke_test_plan.md shows "S3 version" (not "INITIAL")
- [ ] For Options A/C: epic_smoke_test_plan.md has specific test scenarios (not TBD) and validation loop passed
- [ ] For Options B/D: epic_smoke_test_plan.md has epic success criteria section; scripts are the strategy

---

## Next Stage

**After S3 complete:**

📖 **READ:** `stages/s5/s5_v2_validation_loop.md` (first feature — test scope decision at S5 Step 0)
🎯 **GOAL:** Begin feature implementation planning
⏱️ **ESTIMATE:** 4.5-7 hours per feature (Phase 1 draft + Phase 2 validation)

**Note:** S4 is deprecated. Test scope decisions (Testing Approach A/B/C/D) are made at the start of S5 (Step 0 of Phase 1).

---

*End of s3_epic_planning_approval.md*
