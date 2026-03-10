# S3: Epic-Level Documentation, Testing Plans, and Approval — Quick Reference Card

**Purpose:** One-page summary for epic-level integration testing, documentation refinement, and approval gate
**Use Case:** Quick lookup when running S3 after all features complete S2
**Total Time:** 75-105 minutes (scales with feature count)

> **SCOPE:** Runs **once per epic**, after S2 is complete for ALL features. Not repeated per feature.

---

## Workflow Overview

```text
S3.P1: Epic Testing Strategy Development (45-60 min)
    ├─ Step 1: Review all feature test requirements (10-15 min)
    ├─ Step 2: Identify integration points between features (15-20 min)
    ├─ Step 3: Define epic success criteria — measurable (15-20 min)
    ├─ Step 4: Create specific test scenarios with commands (15-25 min)
    ├─ Step 5: Update epic_smoke_test_plan.md (10-15 min)
    └─ Step 6: Validation Loop — 3 consecutive clean rounds
    ↓
S3.P2: Epic Documentation Refinement (20-30 min)
    ├─ Step 1: Consolidate feature details from all spec.md files (10-15 min)
    ├─ Step 2: Update EPIC_README.md with feature summaries + arch decisions (10-15 min)
    └─ Step 3: Validation Loop — 3 consecutive clean rounds
    ↓
S3.P3: Epic Plan Approval (10-15 min) ← MANDATORY GATE
    ├─ Step 1: Create epic summary
    ├─ Step 2: Gate 4.5 — present to user, wait for explicit approval
    └─ If rejected: 3-tier rejection handling (S1.P3 / S1.P4 / exit)
```

---

## Phase Summary Table

| Phase | Duration | Key Activities | Outputs | Gate? |
|-------|----------|----------------|---------|-------|
| S3.P1 | 45-60 min | Integration point mapping, epic success criteria, smoke test scenarios | epic_smoke_test_plan.md | No |
| S3.P2 | 20-30 min | Feature detail consolidation, EPIC_README.md update | EPIC_README.md | No |
| S3.P3 | 10-15 min | Epic summary, user approval | User sign-off (Gate 4.5) | ✅ YES |

---

## Epic-Level vs Feature-Level Tests

| Scope | Where | What |
|-------|-------|------|
| **Epic-Level (S3)** | `epic_smoke_test_plan.md` | End-to-end workflows across ALL features; integration points; epic success criteria |
| **Feature-Level (S4)** | Per-feature test plan | Unit tests; component integration; edge cases within feature boundary |

> **Key Rule:** If you find yourself writing tests for a single feature's internal behavior — stop. That belongs in S4.

---

## Integration Point Map Template (S3.P1 Step 2)

```markdown
## Integration Points Identified

### Integration Point 1: {Name}
**Features Involved:** {list features}
**Type:** {Shared data structure | Computational dependency | File system | API}
**Flow:**
- Feature X: {what it does}
- Feature Y: {what it does}
**Test Need:** {What needs to be verified}
```

---

## Epic Success Criteria Template (S3.P1 Step 3)

```markdown
## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: {Name}
✅ **MEASURABLE:** {Specific, verifiable condition}
**Verification:** {Command or observation}
```

---

## Mandatory Gate: Gate 4.5 (S3.P3 Step 2)

**Location:** `stages/s3/s3_epic_planning_approval.md` — S3.P3
**What to present:**
- Epic summary (all features, 1-sentence each)
- epic_smoke_test_plan.md
- Estimated timeline (feature count × ~6-8 hours)

**Pass Criteria:** User explicitly approves epic plan and testing strategy
**If FAIL — 3 Tier Rejection Handling:**

| Tier | User Says | Action |
|------|-----------|--------|
| A | "Research was incomplete" | Loop back to S1.P3 (Discovery) |
| B | "Features defined incorrectly" | Loop back to S1.P4 (Feature Breakdown) |
| C | "Epic should not proceed" | Exit epic planning |

---

## Prerequisites Checklist

**Before starting S3:**
- [ ] S2 completed for ALL features in the epic
- [ ] All feature spec.md files have user-approved acceptance criteria
- [ ] S2.P2 (Cross-Feature Alignment) completed
- [ ] EPIC_README.md Feature Tracking shows all S2 checkboxes marked
- [ ] epic_smoke_test_plan.md exists (initial version from S1)

---

## Critical Rules Summary

- ✅ ALL features must complete S2 (including S2.P2) before S3
- ✅ S3 tests span MULTIPLE features — single-feature tests belong in S4
- ✅ Each phase (S3.P1, S3.P2) uses a 3-consecutive-clean Validation Loop
- ✅ Gate 4.5 user approval is MANDATORY — cannot skip
- ✅ Total rejection → 3-tier handling, NOT a simple loop-back to S3
- ✅ Update epic EPIC_README.md Agent Status when starting

---

## Common Pitfalls

### ❌ Pitfall 1: Writing Feature-Level Tests
**Problem:** "I'll add unit tests for Feature 3 while I'm here"
**Impact:** Duplicates S4 work; S4 may conflict
**Solution:** Epic tests only — cross-feature integration scenarios

### ❌ Pitfall 2: Skipping S2.P2 Prerequisite
**Problem:** "Features are done individually, that's enough"
**Impact:** Cross-feature conflicts surface at test time
**Solution:** Verify S2.P2 (Cross-Feature Alignment) is complete before S3

### ❌ Pitfall 3: Vague Success Criteria
**Problem:** "The features work correctly" is a success criterion
**Impact:** No way to verify epic is done; QA has no target
**Solution:** Measurable criteria with specific commands/observations

### ❌ Pitfall 4: Assuming User Approval
**Problem:** "The plan looks good, I'll skip Gate 4.5"
**Impact:** Implement wrong scope, rework in S7+ or user testing
**Solution:** ALWAYS get explicit user approval (Gate 4.5 is mandatory)

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting S3 | `stages/s3/s3_epic_planning_approval.md` |
| Parallel work pre-check needed | `stages/s3/s3_parallel_work_sync.md` (optional pre-check) |
| S3.P1 test strategy details | `stages/s3/s3_epic_planning_approval.md` — S3.P1 |
| S3.P3 rejection handling | `stages/s3/s3_epic_planning_approval.md` — S3.P3 |

---

## File Outputs

| Phase | Output |
|-------|--------|
| S3.P1 | `epic/epic_smoke_test_plan.md` (validated) |
| S3.P2 | `EPIC_README.md` (updated with feature details) |
| S3.P3 | `EPIC_SUMMARY.md` (optional); user sign-off documented |

---

## Exit Conditions

**S3 is complete when:**
- [ ] epic_smoke_test_plan.md has concrete integration scenarios (3 clean rounds)
- [ ] EPIC_README.md updated with feature details (3 clean rounds)
- [ ] Epic summary created
- [ ] User explicitly approved epic plan (Gate 4.5)
- [ ] EPIC_README.md shows S3 complete
- [ ] Ready to start S4 (first feature's Feature Testing Strategy)

**Next Stage:** S4 (Feature Testing Strategy) — run once per feature

---

**Last Updated:** 2026-03-08
