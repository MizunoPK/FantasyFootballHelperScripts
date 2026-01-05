# Implementation Orchestration Guide - Feature Lifecycle (5b → 5e)

**Purpose:** Orchestrate the complete feature implementation lifecycle from code writing to epic test plan updates, ensuring smooth transitions between phases and proper EPIC_README tracking.

**Use Case:** Quick reference for navigating a single feature through Stages 5b, 5c, 5d, 5e with clear decision points.

**Total Time:** 2-5 hours per feature (varies by complexity)

---

## Feature Lifecycle Overview

```
Feature Workflow (Single Feature Journey)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stage 5a: TODO Creation COMPLETE
         ↓
         ✅ GO Decision from Iteration 24
         ↓
┌─────────────────────────────────────────┐
│ Stage 5b: Implementation Execution      │
│ (Write feature code)                    │
│ Time: 1-4 hours                         │
└─────────────────────────────────────────┘
         ↓
    [All tests pass?]
    ├─ NO → Fix tests, repeat
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────┐
│ Stage 5c: Post-Implementation           │
│ (Smoke testing, QC rounds, PR review)   │
│ Time: 45-90 minutes                     │
└─────────────────────────────────────────┘
         ↓
    [Stage 5c passed?]
    ├─ NO → Create bug fix → Restart 5c
    └─ YES → Feature complete!
         ↓
    [More features remaining?]
    ├─ YES → Stages 5d + 5e
    └─ NO → Skip to Stage 6
         ↓
┌─────────────────────────────────────────┐
│ Stage 5d: Post-Feature Alignment        │
│ (Update remaining feature specs)        │
│ Time: 15-30 minutes                     │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Stage 5e: Testing Plan Update           │
│ (Update epic_smoke_test_plan.md)        │
│ Time: 15-30 minutes                     │
└─────────────────────────────────────────┘
         ↓
    [More features remaining?]
    ├─ YES → Next Feature's Stage 5a
    └─ NO → Stage 6 (Epic Final QC)
```

---

## Stage 5b: Implementation Execution

### Purpose
Write the feature code following the TODO plan created in Stage 5a.

### Entry Conditions
- [ ] Stage 5a Round 3 complete (Iteration 24 = GO)
- [ ] TODO.md plan ready
- [ ] All mandatory gates passed (4a, 23a, 25, 24)

### Key Activities
1. **Interface Verification First** - Verify ALL external interfaces from source code before writing ANY code
2. **Implement Phase by Phase** - Follow TODO phasing plan (5-6 phases typical)
3. **Keep Spec Visible** - Literally open spec.md at all times
4. **Run Tests After Each Phase** - 100% pass required before next phase
5. **Mini-QC Checkpoints** - Lightweight validation after major components
6. **Update implementation_checklist.md in Real-Time** - Check off as you implement

### Exit Conditions
- [ ] All TODO tasks implemented
- [ ] 100% of tests passing
- [ ] Spec requirements verified complete (dual verification)
- [ ] code_changes.md fully documented
- [ ] implementation_checklist.md 100% complete

### EPIC_README Updates
**Update Epic Progress Tracker:**
- Mark feature Stage 5b column: ✅

**Update Agent Status:**
```markdown
Current Stage: Stage 5c - Post-Implementation
Current Phase: SMOKE_TESTING
Next Action: Read stages/stage_5/smoke_testing.md
```

### Time Estimate
1-4 hours (varies by complexity)

### Next Stage
Stage 5c (Post-Implementation)

---

## Stage 5c: Post-Implementation

### Purpose
Validate the implemented feature through smoke testing, QC rounds, and PR review.

### Entry Conditions
- [ ] Stage 5b complete (all code implemented)
- [ ] 100% of tests passing
- [ ] code_changes.md documented

### Key Activities (3 Phases)

**Phase 1: Smoke Testing (3 parts)**
1. Import Test - Feature imports successfully
2. Entry Point Test - Main entry points work
3. E2E Execution Test - End-to-end workflow succeeds (MANDATORY GATE)

**Phase 2: QC Rounds (3 rounds)**
1. Round 1: Algorithm Verification
2. Round 2: Consistency & Standards
3. Round 3: Integration & Edge Cases

**Phase 3: Final Review**
1. PR Review (7 categories)
2. Lessons Learned documentation
3. Zero tech debt tolerance

### Restart Protocol
**IF ANY ISSUES FOUND:**
- Create bug fix (Stage 2 → 5a → 5b → 5c for bug)
- RESTART Stage 5c from smoke testing
- Re-run all 3 phases

### Exit Conditions
- [ ] Smoke testing PASSED (all 3 parts)
- [ ] All 3 QC rounds PASSED
- [ ] PR review PASSED (all 7 categories)
- [ ] Lessons learned documented
- [ ] Feature is production-ready

### EPIC_README Updates
**Update Epic Progress Tracker:**
- Mark feature Stage 5c column: ✅

**Update Agent Status:**
```markdown
# If more features remaining:
Current Stage: Stage 5d - Post-Feature Alignment
Next Action: Read stages/stage_5/post_feature_alignment.md

# If NO more features:
Current Stage: Stage 6 - Epic Final QC
Next Action: Read stages/stage_6/epic_final_qc.md
```

### Decision Point: Skip 5d/5e?
**Question:** Are there more features to implement?

**If YES (features remaining):**
- Proceed to Stage 5d (Post-Feature Alignment)
- Update remaining feature specs
- Then Stage 5e (Testing Plan Update)
- Then next feature's Stage 5a

**If NO (this was last feature):**
- SKIP Stages 5d and 5e
- Proceed directly to Stage 6 (Epic Final QC)
- Reason: No remaining specs to update, no point updating test plan before final epic testing

### Time Estimate
45-90 minutes (3 phases)

### Next Stage
- Stage 5d (if features remaining)
- Stage 6 (if this was last feature)

---

## Stage 5d: Post-Feature Alignment

### Purpose
Update remaining (not-yet-implemented) feature specs based on ACTUAL implementation of just-completed feature.

### Entry Conditions
- [ ] Stage 5c complete (feature validated)
- [ ] At least 1 feature remaining to implement
- [ ] Feature implementation code accessible

### Key Activities
1. **Review Completed Feature** - Understand ACTUAL implementation (not plan)
2. **Identify Alignment Impacts** - Which remaining specs need updates?
3. **Update Remaining Feature Specs** - Proactively fix spec assumptions
4. **Document Integration Points** - Add implementation insights to specs
5. **Mark Features Needing Rework** - If >3 new tasks, return to Stage 5a

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
- Mark feature Stage 5d column: ✅

**Update Agent Status:**
```markdown
Current Stage: Stage 5e - Testing Plan Update
Current Phase: TESTING_PLAN_UPDATE
Next Action: Read stages/stage_5/post_feature_testing_update.md
```

### Time Estimate
15-30 minutes

### Next Stage
Stage 5e (Testing Plan Update)

---

## Stage 5e: Testing Plan Update

### Purpose
Update epic_smoke_test_plan.md to reflect ACTUAL implementation discoveries and integration points.

### Entry Conditions
- [ ] Stage 5d complete (specs aligned)
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
- Mark feature Stage 5e column: ✅

**Update Agent Status:**
```markdown
# If more features remaining:
Current Stage: Stage 5a - TODO Creation (Next Feature)
Next Feature: feature_0X_{name}
Next Action: Read stages/stage_5/round1_todo_creation.md for next feature

# If NO more features:
Current Stage: Stage 6 - Epic Final QC
Next Action: Read stages/stage_6/epic_final_qc.md
```

### Decision Point: Next Feature or Stage 6?
**Question:** Are there more features to implement?

**If YES (features remaining):**
- Proceed to next feature's Stage 5a (TODO Creation)
- Repeat cycle: 5a → 5b → 5c → 5d → 5e
- Each feature gets full Stage 5 treatment

**If NO (all features complete):**
- Proceed to Stage 6 (Epic Final QC)
- Test entire epic as cohesive system
- Epic-level smoke testing and QC rounds

### Time Estimate
15-30 minutes

### Next Stage
- Next feature's Stage 5a (if features remaining)
- Stage 6 (if all features complete)

---

## Epic Progress Tracker Management

### How the Tracker Works

The Epic Progress Tracker is a table in `EPIC_README.md` that tracks each feature through all stages:

```markdown
| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
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
| Stage 5b | Stage 5b | ✅ |
| Stage 5c | Stage 5c | ✅ |
| Stage 5d | Stage 5d | ✅ |
| Stage 5e | Stage 5e | ✅ |

**Before starting new stage:**
Mark next column as 🔄 (in progress)

---

## Common Decision Points

### Decision 1: After Stage 5c - Continue or Stop?

**Scenario:** Feature just completed Stage 5c (Post-Implementation)

**Question:** Do we continue to Stages 5d and 5e?

**Answer:**
- **YES** if features remaining to implement → Go to 5d
- **NO** if this was last feature → Skip to Stage 6

**Why:** No point updating specs (5d) or test plan (5e) if no more features to implement

---

### Decision 2: After Stage 5e - Next Feature or Epic QC?

**Scenario:** Feature just completed Stage 5e (Testing Plan Update)

**Question:** What's next?

**Answer:**
- **Next feature's Stage 5a** if features remaining
- **Stage 6 (Epic QC)** if all features complete

**How to check:** Look at Epic Progress Tracker - are all features showing ✅ through Stage 5e?

---

### Decision 3: Stage 5c Issues Found - Bug Fix or Continue?

**Scenario:** Issues found during Stage 5c QC rounds

**Question:** Do we continue or create bug fix?

**Answer:**
- **ANY issues** → Create bug fix
- Bug fix goes through: Stage 2 → 5a → 5b → 5c
- After bug fix complete → RESTART original feature's Stage 5c
- **Zero tolerance** for tech debt

---

## Quick Checklist: "Where Am I?"

**Use this to determine current position:**

**If you just completed:**
- [x] Stage 5a (Iteration 24 = GO) → **Next:** Stage 5b (Implementation)
- [x] Stage 5b (code written, tests pass) → **Next:** Stage 5c (Post-Implementation)
- [x] Stage 5c (all QC passed) → **Check:** Features remaining?
  - YES → **Next:** Stage 5d (Alignment)
  - NO → **Next:** Stage 6 (Epic QC)
- [x] Stage 5d (specs updated) → **Next:** Stage 5e (Test Plan Update)
- [x] Stage 5e (test plan updated) → **Check:** Features remaining?
  - YES → **Next:** Next feature's Stage 5a
  - NO → **Next:** Stage 6 (Epic QC)

**If ANY QC round failed:**
- Create bug fix
- RESTART that stage's QC from beginning

---

## Summary

**Feature Implementation Lifecycle:**

1. **Stage 5b (1-4 hours):** Write code, run tests after each phase
2. **Stage 5c (45-90 min):** Smoke test, QC rounds, PR review
3. **Stage 5d (15-30 min):** Update remaining feature specs (SKIP if last feature)
4. **Stage 5e (15-30 min):** Update epic test plan (SKIP if last feature)

**Total per feature:** 2-5 hours

**Key Decision Points:**
- After 5c: Skip 5d/5e if last feature
- After 5e: Next feature's 5a OR Stage 6 if all done
- During any stage: Issues found → Bug fix → Restart stage

**EPIC_README Updates:**
- Mark ✅ in Epic Progress Tracker after each stage
- Update Agent Status with next action
- Keep Quick Reference Card current

**Remember:** Stages 5d and 5e are ONLY for aligning future features. If you just completed the LAST feature, skip directly to Stage 6 for epic-level testing.

---

**Last Updated:** 2026-01-04
