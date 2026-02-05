# S3: Epic-Level Documentation, Testing Plans, and Approval

🚨 **MANDATORY READING PROTOCOL**

**Before starting this stage:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Verify prerequisites (S2 complete for ALL features)
3. Update epic EPIC_README.md Agent Status with guide name + timestamp

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
- S3.P1: Epic Testing Strategy Development (45-60 min) - Moved from old S4, expanded
- S3.P2: Epic Documentation Refinement (20-30 min)
- S3.P3: Epic Plan Approval (10-15 min) - Gate 4.5 with 3-tier rejection handling

**Time:** 75-105 minutes total
**Prerequisites:** S2 complete for ALL features (S2.P2 alignment done)

**Key Changes from Old S3:**
- **Pairwise comparison removed** (moved to S2.P2)
- **Epic testing strategy from old S4 moved here** (S3.P1)
- **Two Validation Loops** (testing strategy + documentation)
- **Gate 4.5 explicit with 3-tier rejection handling**

---

## S3.P1: Epic Testing Strategy Development (45-60 min)

### Purpose
Create epic_smoke_test_plan.md for end-to-end integration testing when all features complete

**Note:** This phase content was moved from old S4 (s4_epic_testing_strategy.md) and expanded with more detail

### What Epic-Level Tests Cover

**Epic-Level Tests (S3):**
- End-to-end workflows across ALL features
- Integration points between features
- Epic-level success criteria
- Data flow through complete system

**vs. Feature-Level Tests (S4):**
- Unit tests (function-level)
- Integration tests (component-level)
- Edge cases within feature boundary

**Key Distinction:** S3 tests ACROSS features, S4 tests WITHIN features

### Steps

**1. Review All Feature Test Requirements (10-15 min)**
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
```
{Actual command to run}
```json

[Continue for each test scenario...]
```

**5. Update epic_smoke_test_plan.md (10-15 min)**
- Replace S1 placeholder content with concrete scenarios
- Add all integration points
- Add all success criteria
- Add all test scenarios
- Mark as "S3 version - will update in S8.P2 (Epic Testing Update)"

**6. Validation Loop Validation (15-20 min)**

**Reference:** `reference/validation_loop_test_strategy.md`

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
Get user approval for complete epic plan before proceeding to S4 (Gate 4.5)

### Steps

**1. Create Epic Summary (5-10 min)**
- Consolidate all feature specs
- List all features with 1-sentence descriptions
- Summarize epic test plan approach
- Estimate total timeline (feature count × ~6-8 hours)

**2. Gate 4.5: User Approval of Epic Plan (5 min)**
- Present epic summary to user
- Present epic_smoke_test_plan.md
- Ask: "Approve this epic plan and testing strategy?"
- **MANDATORY GATE:** Cannot proceed to S4 without approval
- **Note:** Single Gate 4.5 (not split into 4.5a/4.5b per user direction)

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
- Ready to proceed to S4 (first feature)

---

## Exit Criteria

**S3 complete when ALL true:**

□ S3.P1 complete (epic_smoke_test_plan.md updated and validated)
□ S3.P2 complete (EPIC_README.md refined and validated)
□ S3.P3 complete (Gate 4.5 passed - user approved epic plan)
□ Epic EPIC_README.md updated with:
  - Epic Completion Checklist: S3 items checked
  - Agent Status: Phase = S4_READY
□ epic_smoke_test_plan.md shows "S3 version" (not "INITIAL")
□ epic_smoke_test_plan.md has specific test scenarios (not TBD)

---

## Next: S4 (Feature Testing Strategy)

**After S3 complete:**

📖 **READ:** `stages/s4/s4_feature_testing_strategy.md` (first feature)
🎯 **GOAL:** Plan feature-level tests BEFORE implementation (test-driven development)
⏱️ **ESTIMATE:** 45-60 minutes per feature

**S4 will:**
- Plan unit tests, integration tests, edge cases, config tests
- Create test_strategy.md with >90% coverage goal
- Validate with Validation Loop (4 iterations)

**Remember:** Use phase transition prompt from `prompts_reference_v2.md` when starting S4.

---

*End of s3_epic_planning_approval.md*
