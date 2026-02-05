# Implementation Orchestration Guide - Feature Lifecycle (S6 → S8)

**Purpose:** Orchestrate the complete feature implementation lifecycle from code writing to epic test plan updates, ensuring smooth transitions between phases and proper EPIC_README tracking.

**Use Case:** Quick reference for navigating a single feature through Stages 5b, 5c, 5d, 5e with clear decision points.

**Total Time:** 2-5 hours per feature (varies by complexity)

---

## Feature Lifecycle Overview

```text
Feature Workflow (Single Feature Journey)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

S5: TODO Creation COMPLETE
         ↓
         ✅ GO Decision from Iteration 22
         ↓
┌─────────────────────────────────────────┐
│ S6: Implementation Execution      │
│ (Write feature code)                    │
│ Time: 1-4 hours                         │
└─────────────────────────────────────────┘
         ↓
    [All tests pass?]
    ├─ NO → Fix tests, repeat
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────┐
│ S7: Post-Implementation           │
│ (Smoke testing, QC rounds, PR review)   │
│ Time: 45-90 minutes                     │
└─────────────────────────────────────────┘
         ↓
    [S7 passed?]
    ├─ NO → Create bug fix → Restart S7
    └─ YES → Feature complete!
         ↓
    [More features remaining?]
    ├─ YES → Stages 5d + 5e
    └─ NO → Skip to S9
         ↓
┌─────────────────────────────────────────┐
│ S8.P1: Post-Feature Alignment        │
│ (Update remaining feature specs)        │
│ Time: 15-30 minutes                     │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ S8.P2: Testing Plan Update           │
│ (Update epic_smoke_test_plan.md)        │
│ Time: 15-30 minutes                     │
└─────────────────────────────────────────┘
         ↓
    [More features remaining?]
    ├─ YES → Next Feature's S5
    └─ NO → S9 (Epic Final QC)
```markdown

---

## S6: Implementation Execution

### Purpose
Write the feature code following the implementation plan created in S5.

### Entry Conditions
- [ ] S5 Round 3 complete (Iteration 22 = GO)
- [ ] implementation_plan.md ready and user-approved
- [ ] All mandatory gates passed (4a, 23a, 25, 24)

### Key Activities
1. **Interface Verification First** - Verify ALL external interfaces from source code before writing ANY code
2. **Implement Phase by Phase** - Follow implementation_plan.md phasing (5-6 phases typical)
3. **Keep Spec Visible** - Literally open spec.md at all times
4. **Run Tests After Each Phase** - 100% pass required before next phase
5. **Mini-QC Checkpoints** - Lightweight validation after major components
6. **Update implementation_checklist.md in Real-Time** - Check off as you implement

### Exit Conditions
- [ ] All implementation_plan.md tasks implemented
- [ ] 100% of tests passing
- [ ] Spec requirements verified complete (dual verification)
- [ ] implementation_checklist.md 100% complete

### EPIC_README Updates
**Update Epic Progress Tracker:**
- Mark feature S6 column: ✅

**Update Agent Status:**
```markdown
Current Stage: S7 - Post-Implementation
Current Phase: SMOKE_TESTING
Next Action: Read stages/s7/s7_p1_smoke_testing.md
```markdown

### Time Estimate
1-4 hours (varies by complexity)

### Next Stage
S7 (Post-Implementation)

---

## S7: Post-Implementation

### Purpose
Validate the implemented feature through smoke testing, QC rounds, and PR review.

### Entry Conditions
- [ ] S6 complete (all code implemented)
- [ ] 100% of tests passing

### Key Activities (3 Phases)

**Step 1: Smoke Testing (3 parts)**
1. Import Test - Feature imports successfully
2. Entry Point Test - Main entry points work
3. E2E Execution Test - End-to-end workflow succeeds (MANDATORY GATE)

**Step 2: QC Rounds (3 rounds)**
1. Round 1: Algorithm Verification
2. Round 2: Consistency & Standards
3. Round 3: Integration & Edge Cases

**Step 3: Final Review**
1. PR Review (7 categories)
2. Lessons Learned documentation
3. Zero tech debt tolerance

### Restart Protocol
**IF ANY ISSUES FOUND:**
- Create bug fix (S2 → S5 → S6 → S7 for bug)
- RESTART S7 from smoke testing
- Re-run all 3 phases

### Exit Conditions
- [ ] Smoke testing PASSED (all 3 parts)
- [ ] All 3 QC rounds PASSED
- [ ] PR review PASSED (all 7 categories)
- [ ] Lessons learned documented
- [ ] Feature is production-ready

### EPIC_README Updates
**Update Epic Progress Tracker:**
- Mark feature S7 column: ✅

**Update Agent Status:**
```markdown
# If more features remaining:
Current Stage: S8.P1 - Post-Feature Alignment
Next Action: Read stages/s8/s8_p1_cross_feature_alignment.md

# If NO more features:
Current Stage: S9 - Epic Final QC
Next Action: Read stages/s9/s9_epic_final_qc.md
```markdown

### Decision Point: Skip S8?
**Question:** Are there more features to implement?

**If YES (features remaining):**
- Proceed to S8.P1 (Post-Feature Alignment)
- Update remaining feature specs
- Then S8.P2 (Testing Plan Update)
- Then next feature's S5

**If NO (this was last feature):**
- SKIP S8.P1 and S8.P2
- Proceed directly to S9 (Epic Final QC)
- Reason: No remaining specs to update, no point updating test plan before final epic testing

### Time Estimate
45-90 minutes (3 phases)

### Next Stage
- S8.P1 (if features remaining)
- S9 (if this was last feature)

---

## S8.P1: Post-Feature Alignment

### Purpose
Update remaining (not-yet-implemented) feature specs based on ACTUAL implementation of just-completed feature.

### Entry Conditions
- [ ] S7 complete (feature validated)
- [ ] At least 1 feature remaining to implement
- [ ] Feature implementation code accessible

### Key Activities
1. **Review Completed Feature** - Understand ACTUAL implementation (not plan)
2. **Identify Alignment Impacts** - Which remaining specs need updates?
3. **Update Remaining Feature Specs** - Proactively fix spec assumptions
4. **Document Integration Points** - Add implementation insights to specs
5. **Mark Features Needing Rework** - If >3 new tasks, return to S5

### Critical Rules
- Compare to ACTUAL implementation (not TODO or plan)
- Review ALL remaining features (not just "related" ones)
- Update specs proactively (don't defer to implementation time)
- Document WHY spec changed (reference actual code locations)
- Update checklist.md too (not just spec.md)

### Exit Conditions
- [ ] All remaining feature specs reviewed
- [ ] Specs updated with implementation insights
- [ ] Integration points documented
- [ ] Updates logged in each affected spec

### EPIC_README Updates
**Update Epic Progress Tracker:**
- Mark feature S8.P1 column: ✅

**Update Agent Status:**
```markdown
Current Stage: S8.P2 - Testing Plan Update
Current Phase: TESTING_PLAN_UPDATE
Next Action: Read stages/s8/s8_p2_epic_testing_update.md
```markdown

### Time Estimate
15-30 minutes

### Next Stage
S8.P2 (Testing Plan Update)

---

## S8.P2: Testing Plan Update

### Purpose
Update epic_smoke_test_plan.md to reflect ACTUAL implementation discoveries and integration points.

### Entry Conditions
- [ ] S8.P1 complete (specs aligned)
- [ ] Feature implementation code accessible
- [ ] epic_smoke_test_plan.md exists

### Key Activities
1. **Review epic_smoke_test_plan.md** - Current test scenarios
2. **Review Actual Implementation** - What was REALLY built (not specs)
3. **Identify New Integration Points** - Cross-feature interactions discovered
4. **Update Test Scenarios** - Add/modify/remove based on reality
5. **Document Update Rationale** - WHY tests added/changed

### Critical Rules
- Update based on ACTUAL implementation (not specs or TODO)
- Identify integration points DISCOVERED during implementation
- Add specific test scenarios (not vague categories)
- Update existing scenarios (don't just append)
- Focus on EPIC-LEVEL testing (cross-feature workflows)
- Document update rationale in update history

### Exit Conditions
- [ ] epic_smoke_test_plan.md reflects actual implementation
- [ ] New integration points added
- [ ] Test scenarios updated
- [ ] Changes documented in update history

### EPIC_README Updates
**Update Epic Progress Tracker:**
- Mark feature S8.P2 column: ✅

**Update Agent Status:**
```markdown
# If more features remaining:
Current Stage: S5 - TODO Creation (Next Feature)
Next Feature: feature_0X_{name}
Next Action: Read stages/s5/s5_p1_planning_round1.md for next feature

# If NO more features:
Current Stage: S9 - Epic Final QC
Next Action: Read stages/s9/s9_epic_final_qc.md
```markdown

### Decision Point: Next Feature or S9?
**Question:** Are there more features to implement?

**If YES (features remaining):**
- Proceed to next feature's S5 (TODO Creation)
- Repeat cycle: S5 → S6 → S7 → S8
- Each feature gets full S5 treatment

**If NO (all features complete):**
- Proceed to S9 (Epic Final QC)
- Test entire epic as cohesive system
- Epic-level smoke testing and QC rounds

### Time Estimate
15-30 minutes

### Next Stage
- Next feature's S5 (if features remaining)
- S9 (if all features complete)

---

## Epic Progress Tracker Management

### How the Tracker Works

The Epic Progress Tracker is a table in `EPIC_README.md` that tracks each feature through all stages:

```markdown
| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_name | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_02_name | ✅ | ✅ | ✅ | ✅ | ✅ | 🔄 | ◻️ | ◻️ | ◻️ |
| feature_03_name | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
```

**Legend:**
- ✅ = Complete
- 🔄 = In Progress (current stage)
- ◻️ = Not Started

### When to Update the Tracker

**After completing each stage:**

| Stage Complete | Mark Column | Update To |
|----------------|-------------|-----------|
| S6 | S6 | ✅ |
| S7 | S7 | ✅ |
| S8.P1 | S8.P1 | ✅ |
| S8.P2 | S8.P2 | ✅ |

**Before starting new stage:**
Mark next column as 🔄 (in progress)

---

## Common Decision Points

### Decision 1: After S7 - Continue or Stop?

**Scenario:** Feature just completed S7 (Post-Implementation)

**Question:** Do we continue to S8.P1 and S8.P2?

**Answer:**
- **YES** if features remaining to implement → Go to 5d
- **NO** if this was last feature → Skip to S9

**Why:** No point updating specs (5d) or test plan (5e) if no more features to implement

---

### Decision 2: After S8.P2 - Next Feature or Epic QC?

**Scenario:** Feature just completed S8.P2 (Testing Plan Update)

**Question:** What's next?

**Answer:**
- **Next feature's S5** if features remaining
- **S9 (Epic QC)** if all features complete

**How to check:** Look at Epic Progress Tracker - are all features showing ✅ through S8.P2?

---

### Decision 3: S7 Issues Found - Bug Fix or Continue?

**Scenario:** Issues found during S7 QC rounds

**Question:** Do we continue or create bug fix?

**Answer:**
- **ANY issues** → Create bug fix
- Bug fix goes through: S2 → S5 → S6 → S7
- After bug fix complete → RESTART original feature's S7
- **Zero tolerance** for tech debt

---

## Quick Checklist: "Where Am I?"

**Use this to determine current position:**

**If you just completed:**
- [x] S5 (Iteration 22 = GO) → **Next:** S6 (Implementation)
- [x] S6 (code written, tests pass) → **Next:** S7 (Post-Implementation)
- [x] S7 (all QC passed) → **Check:** Features remaining?
  - YES → **Next:** S8.P1 (Alignment)
  - NO → **Next:** S9 (Epic QC)
- [x] S8.P1 (specs updated) → **Next:** S8.P2 (Test Plan Update)
- [x] S8.P2 (test plan updated) → **Check:** Features remaining?
  - YES → **Next:** Next feature's S5
  - NO → **Next:** S9 (Epic QC)

**If ANY QC round failed:**
- Create bug fix
- RESTART that stage's QC from beginning

---

## Summary

**Feature Implementation Lifecycle:**

1. **S6 (1-4 hours):** Write code, run tests after each step
2. **S7 (45-90 min):** Smoke test, QC rounds, PR review
3. **S8.P1 (15-30 min):** Update remaining feature specs (SKIP if last feature)
4. **S8.P2 (15-30 min):** Update epic test plan (SKIP if last feature)

**Total per feature:** 2-5 hours

**Key Decision Points:**
- After 5c: Skip S8 if last feature
- After 5e: Next feature's 5a OR S9 if all done
- During any stage: Issues found → Bug fix → Restart stage

**EPIC_README Updates:**
- Mark ✅ in Epic Progress Tracker after each stage
- Update Agent Status with next action
- Keep Quick Reference Card current

**Remember:** S8.P1 and S8.P2 are ONLY for aligning future features. If you just completed the LAST feature, skip directly to S9 for epic-level testing.

---

**Last Updated:** 2026-01-04
