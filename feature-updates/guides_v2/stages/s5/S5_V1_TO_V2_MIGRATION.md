# S5 v1 to v2 Migration Guide

**Version:** 1.0
**Created:** 2026-02-09
**Purpose:** Guide for agents transitioning from S5 v1 (22 iterations) to S5 v2 (Validation Loop)

---

## Table of Contents

1. [Overview](#overview)
2. [Key Differences](#key-differences)
3. [Side-by-Side Comparison](#side-by-side-comparison)
4. [Conceptual Shift](#conceptual-shift)
5. [How to Use S5 v2](#how-to-use-s5-v2)
6. [What Changed and Why](#what-changed-and-why)
7. [FAQ for Agents](#faq-for-agents)
8. [When to Use v1 vs v2](#when-to-use-v1-vs-v2)
9. [Troubleshooting](#troubleshooting)

---

## Overview

### What Changed?

S5 v2 replaces the 22-iteration sequential structure with a **2-phase Validation Loop approach**:

**Old (v1):** 22 iterations across 3 rounds → 9-11 hours
**New (v2):** Draft Creation + Validation Loop → 4.5-7 hours (35-50% time savings)

### Why Change?

**Problems with v1:**
- 3x redundant re-verifications (Algorithm Traceability, Integration Gap Check)
- No systematic validation (possible to skip checks)
- No mechanism to verify fixes didn't introduce new issues
- Subjective quality assessment (agent self-reports)

**How v2 fixes it:**
- Zero redundancy (all checks consolidated into 11 dimensions)
- Impossible to skip checks (validation loop requires checking all dimensions)
- Every fix re-verified in subsequent rounds
- Objective quality metric (3 consecutive clean rounds)

---

## Key Differences

### Structure

| Aspect | S5 v1 | S5 v2 |
|--------|-------|-------|
| **Approach** | 22 sequential iterations | 2-phase: Draft + Validation Loop |
| **Rounds** | 3 rounds (Round 1, 2, 3) | 6-8 validation rounds (typical) |
| **Time** | 9-11 hours | 4.5-7 hours |
| **Quality Guarantee** | Agent self-reports | 3 consecutive clean rounds |
| **Re-verification** | 3x separate iterations | Every round checks everything |
| **Exit Criteria** | Complete all 22 iterations | 3 consecutive rounds, zero issues |

### Process

| Aspect | S5 v1 | S5 v2 |
|--------|-------|-------|
| **Start** | Iteration 1 (Requirements) | Phase 1: Draft Creation (90 min) |
| **Planning** | Sequential iterations | Phase 2: Validation Loop |
| **Verification** | Checkpoints at iterations 4a, 7a, 20, 21, 22 | Every round validates all dimensions |
| **Issue Handling** | Continue to next iteration | Fix immediately, reset clean counter |
| **Documentation** | Update implementation_plan.md | Update implementation_plan.md + VALIDATION_LOOP_LOG.md |

### Gates

| Gate | S5 v1 Location | S5 v2 Location |
|------|----------------|----------------|
| **Gate 4a** (Task Spec Audit) | Iteration 4a (Round 1) | Embedded in Dimension 4 (every round) |
| **Gate 7a** (Backward Compat) | Iteration 7a (Round 1) | Embedded in Dimension 7 (every round) |
| **Gate 23a** (Pre-Impl Spec Audit) | Iteration 20 (Round 3) | Embedded in Dimension 11 (every round) |
| **Gate 24** (GO/NO-GO) | Iteration 22 (Round 3) | Embedded in Dimension 10 (every round) |
| **Gate 25** (Spec Validation) | Iteration 21 (Round 3) | Embedded in Dimension 11 (every round) |
| **Gate 5** (User Approval) | After iteration 22 | After validation loop completes |

---

## Side-by-Side Comparison

### S5 v1 Workflow

```text
Round 1 (3-4 hours):
├─ Iteration 1: Requirements Coverage
├─ Iteration 2: Component Dependencies
├─ Iteration 3: Interface Contracts
├─ Iteration 4: Algorithm Traceability Matrix
├─ Iteration 4a: Task Specification Audit (GATE)
├─ Iteration 5: E2E Data Flow
├─ Iteration 6: Edge Cases & Errors
├─ Iteration 7: Integration Gap Check
└─ Iteration 7a: Backward Compatibility (GATE)

Round 2 (3-4 hours):
├─ Iteration 8: Test Strategy Depth
├─ Iteration 9: Resume/Persistence Tests
├─ Iteration 10: Error Handler Audit
├─ Iteration 11: Algorithm Traceability (re-verify)
├─ Iteration 12: E2E Data Flow (re-verify)
├─ Iteration 13: Test Coverage Depth
└─ Iteration 14: Integration Gap Check (re-verify)

Round 3 (3-4 hours):
├─ Iteration 15: Implementation Phasing
├─ Iteration 16: Rollback Strategy
├─ Iteration 17: Output Consumer Validation
├─ Iteration 18: Documentation Tasks
├─ Iteration 19: Algorithm Traceability (final)
├─ Iteration 19: Integration Gap Check (final)
├─ Iteration 20: Pre-Implementation Spec Audit (GATE 23a)
├─ Iteration 21: Spec Validation (GATE 25)
└─ Iteration 22: GO/NO-GO Decision (GATE 24)

Gate 5: User Approval

Total: 22 iterations, 9-11 hours
```

### S5 v2 Workflow

```text
Phase 1: Draft Creation (60-90 minutes)
├─ Use template: implementation_plan_template.md
├─ Create all 11 dimension sections
├─ Target: ~70% completeness
└─ Time limit: 90 minutes

Phase 2: Validation Loop (3.5-6 hours, typically 6-8 rounds)
├─ Round 1: Sequential read, find issues → FIX ALL
├─ Round 2: Reverse read, find issues → FIX ALL
├─ Round 3: Spot-checks, find issues → FIX ALL
├─ Round 4: Full validation, zero issues ✓ (clean count = 1)
├─ Round 5: Fresh perspective, zero issues ✓ (clean count = 2)
└─ Round 6: Final validation, zero issues ✓ (clean count = 3) → EXIT

Gate 5: User Approval

Total: 6-8 rounds, 4.5-7 hours (35-50% time savings)

11 Validation Dimensions (checked EVERY round):
1. Requirements Completeness
2. Interface & Dependency Verification
3. Algorithm Traceability
4. Task Specification Quality (embeds Gate 4a)
5. Data Flow & Consumption
6. Error Handling & Edge Cases
7. Integration & Compatibility (embeds Gate 7a)
8. Test Coverage Quality
9. Performance & Dependencies
10. Implementation Readiness (embeds Gate 24)
11. Spec Alignment & Cross-Validation (embeds Gates 23a, 25)
```

---

## Conceptual Shift

### From Sequential Iterations to Validation Dimensions

**v1 Mindset:**
- "I need to complete 22 iterations in order"
- "Iteration 4 creates the Algorithm Traceability Matrix"
- "Iteration 11 re-verifies the matrix"
- "Iteration 19 does final verification"

**v2 Mindset:**
- "I need to validate implementation_plan.md against 11 dimensions"
- "Dimension 3 (Algorithm Traceability) is checked EVERY round"
- "I exit when 3 consecutive rounds find zero issues"
- "Every round is a complete validation of ALL dimensions"

### From Checkpoint Verification to Continuous Validation

**v1 Approach:**
- Complete iteration N
- Move to iteration N+1
- Maybe catch issues in later iterations (11, 12, 14, 19)

**v2 Approach:**
- Complete validation round N
- Fix ALL issues immediately
- Round N+1 validates fixes AND checks for new issues
- Every round is a fresh eyes review of ENTIRE plan

### From "Complete All Tasks" to "Achieve Quality"

**v1 Exit Criteria:**
- "Did I complete all 22 iterations?"
- "Did I pass iterations 4a, 7a, 20, 21, 22?"
- Agent self-reports: "Yes, all done"

**v2 Exit Criteria:**
- "Did 3 consecutive rounds find zero issues?"
- "Can I read implementation_plan.md with fresh eyes and find nothing wrong?"
- Objective proof: 3 independent validations found nothing

---

## How to Use S5 v2

### Step 1: Read the Guide

```bash
Read stages/s5/s5_v2_validation_loop.md
```

**Use the "Starting S5 v2" prompt** from `prompts_reference_v2.md`

### Step 2: Phase 1 - Draft Creation (60-90 minutes)

**Goal:** Create initial implementation_plan.md with all 11 dimension sections

**Process:**
1. Copy template: `cp templates/implementation_plan_template.md feature_XX/implementation_plan.md`
2. Create tasks for each spec.md requirement
3. Map dependencies (quick pass)
4. Create algorithm traceability matrix (initial, 70% coverage)
5. Document data flow (high-level)
6. List error/edge cases (initial)
7. Stop at 90 minutes even if only 70% complete

**Output:** Draft implementation_plan.md (~70% quality)

### Step 3: Phase 2 - Validation Loop (3.5-6 hours)

**Goal:** Iteratively refine until 3 consecutive clean rounds

**Process for EACH round:**

1. **Take 2-5 minute break** (clear mental model)

2. **Re-read ENTIRE implementation_plan.md** (use Read tool, no working from memory)

3. **Check ALL 11 dimensions systematically**:
   - Dimension 1: Requirements Completeness
   - Dimension 2: Interface & Dependency Verification
   - Dimension 3: Algorithm Traceability
   - Dimension 4: Task Specification Quality
   - Dimension 5: Data Flow & Consumption
   - Dimension 6: Error Handling & Edge Cases
   - Dimension 7: Integration & Compatibility
   - Dimension 8: Test Coverage Quality
   - Dimension 9: Performance & Dependencies
   - Dimension 10: Implementation Readiness
   - Dimension 11: Spec Alignment & Cross-Validation

4. **Document findings** in VALIDATION_LOOP_LOG.md

5. **If issues found (X > 0)**:
   - Fix ALL issues immediately
   - Update implementation_plan.md
   - RESET consecutive clean counter to 0
   - Proceed to next round

6. **If zero issues (X = 0)**:
   - Increment consecutive clean counter
   - If counter = 3: EXIT (PASSED)
   - If counter < 3: Proceed to next round

**Output:** Validated implementation_plan.md (99%+ quality)

### Step 4: Gate 5 - User Approval

Present implementation_plan.md to user for approval before S6.

---

## What Changed and Why

### Change 1: Eliminated Redundant Re-Verifications

**v1 Problem:**
- Algorithm Traceability verified 3 times (Iterations 4, 11, 19)
- Integration Gap Check verified 3 times (Iterations 7, 14, 19)
- E2E Data Flow verified 3 times (Iterations 5, 12, implied in 19)

**v2 Solution:**
- Each dimension checked EVERY round (automatic re-verification)
- No need for separate "re-verify" iterations
- Fixes from Round N validated in Round N+1

**Time Saved:** ~2-3 hours

---

### Change 2: Made Validation Systematic

**v1 Problem:**
- Possible to skip iterations (agent forgets or rushes)
- No enforcement mechanism
- Quality depends on agent discipline

**v2 Solution:**
- Validation Loop Protocol enforces checking all dimensions
- Cannot exit until 3 consecutive clean rounds
- Impossible to skip checks (must validate all 11 every round)

**Quality Improvement:** Objective verification (3 clean rounds) vs subjective (agent says "done")

---

### Change 3: Introduced Fresh Eyes Validation

**v1 Problem:**
- Complete iteration once, move on
- No mechanism to verify fixes are correct
- Agent works from memory of what was written

**v2 Solution:**
- Re-read ENTIRE document every round (fresh eyes)
- Take 2-5 minute breaks between rounds (clear mental model)
- Vary reading patterns (sequential, reverse, spot-checks)
- Every round validates fixes from previous rounds

**Quality Improvement:** Multiple independent validations vs single pass

---

### Change 4: Consolidated Gates into Dimensions

**v1 Problem:**
- Gates scattered across iterations (4a, 7a, 20, 21, 22)
- Easy to pass one gate but miss issues in others
- Gates checked once at specific iterations

**v2 Solution:**
- All gate requirements embedded in dimensions
- Gate 4a → Dimension 4 (Task Specification Quality)
- Gate 7a → Dimension 7 (Integration & Compatibility)
- Gates 23a, 24, 25 → Dimensions 10-11
- All dimensions checked EVERY round

**Quality Improvement:** Continuous verification vs point-in-time checks

---

### Change 5: Zero Tolerance for Deferred Issues

**v1 Possible Behavior:**
- "I'll fix this in Round 2"
- "This is minor, I'll note it and continue"
- "I'll address this later"

**v2 Required Behavior:**
- Fix ALL issues immediately (no exceptions)
- Cannot proceed to next round with known issues
- Zero deferred issues policy

**Quality Improvement:** No technical debt accumulation

---

## FAQ for Agents

### Q1: Why can't I just run the 22 iterations?

**A:** The 22-iteration structure (v1) is deprecated because:
- It contains redundant re-verifications (wasted time)
- It lacks systematic validation (quality gaps)
- It has no mechanism to verify fixes (potential for cascading errors)

S5 v2 achieves the same quality with 35-50% time savings through the Validation Loop approach.

### Q2: What if I'm more comfortable with v1?

**A:** Both approaches achieve the same 150+ checks and produce the same quality output. However:
- v2 is faster (4.5-7 hours vs 9-11 hours)
- v2 is more systematic (impossible to skip checks)
- v2 provides objective quality proof (3 clean rounds)
- v2 is the current standard going forward

If you're new to the workflow, learning v2 from the start is recommended.

### Q3: How do I know when my draft is "good enough"?

**A:** Use these thresholds:

**Minimum to start validation loop:**
- All 11 dimension sections exist in implementation_plan.md
- At least 70% of spec requirements have tasks
- At least 70% of algorithms mapped
- Time limit: 90 minutes (stop even if only 70%)

**Why low threshold?**
- Validation loop will catch everything systematically
- Better to have 70% draft and start validating than 95% draft with no validation
- Known gaps are fine (will be caught in Round 1-3)

### Q4: What if I find issues in Round 10?

**A:** Escalate to user per Validation Loop Protocol:
- Document pattern of issues found
- Ask user to assess: architecture issue? scope issue? misunderstanding?
- User decides: adjust scope, override validation, return to S2, etc.

Historical evidence: Most features exit by Round 6-8. Reaching Round 10 indicates deeper issue.

### Q5: Can I check dimensions in parallel within a round?

**A:** Yes, within a single round:
- Read implementation_plan.md once
- Find issues from ANY dimension as you read
- Document all issues found (across all dimensions)
- After round, fix all issues, then start next round

**No, across rounds:**
- Must fix ALL issues from Round N before starting Round N+1
- Cannot parallelize rounds (sequential validation required)

### Q6: What if I only find 1 issue in Round 4?

**A:** Fix it and reset clean counter:
- Round 4: 1 issue found → Fix → Reset clean count to 0
- Round 5: 0 issues → Clean count = 1
- Round 6: 0 issues → Clean count = 2
- Round 7: 0 issues → Clean count = 3 → PASSED ✅

**Critical:** Clean rounds must be CONSECUTIVE. Finding any issue resets the counter.

### Q7: How do reading patterns help?

**A:** Varying reading patterns prevents pattern blindness:

- **Sequential (Round 1):** Natural flow, catch structural issues
- **Reverse (Round 2):** See connections differently, catch flow issues
- **Spot-checks (Round 3):** Random sampling, catch consistency issues
- **Fresh eyes (Round 4+):** Assume everything is wrong, catch anything

Each pattern exposes different types of issues.

### Q8: Where does the evidence go?

**A:** All evidence goes IN implementation_plan.md:
- Algorithm Traceability Matrix → Section in implementation_plan.md
- Dependency Verification Table → Section in implementation_plan.md
- Data Flow Diagram → Section in implementation_plan.md
- All evidence artifacts → Sections within implementation_plan.md

**VALIDATION_LOOP_LOG.md tracks rounds/issues, NOT evidence artifacts.**

### Q9: What if user requests changes after Gate 5?

**A:** Depends on change scope:

**Minor changes (update 1-2 tasks, clarify acceptance criteria):**
- Fix implementation_plan.md
- Re-present to user (no re-validation needed)

**Major changes (add/remove requirements, change approach):**
- Update implementation_plan.md
- Re-run validation loop on affected dimensions
- Achieve 3 clean rounds again
- Re-present to user

### Q10: Can I use v1 for this feature and v2 for the next?

**A:** Not recommended:
- Mixing approaches creates confusion
- v2 is now the standard for all new features
- v1 guides remain available but are deprecated

**Exception:** If you're mid-feature using v1, complete that feature with v1, then switch to v2 for next feature.

---

## When to Use v1 vs v2

### Use S5 v2 (Validation Loop)

**Default for all new features:**
- ✅ Starting new feature implementation planning
- ✅ Prefer faster, more systematic approach
- ✅ Want objective quality guarantee (3 clean rounds)
- ✅ All features going forward (v2 is the standard)

**Guide:** `stages/s5/s5_v2_validation_loop.md`

### Use S5 v1 (22 Iterations) - DEPRECATED

**Only if:**
- ⚠️ Already mid-feature using v1 (complete with v1, switch to v2 next feature)
- ⚠️ Specifically requested by user for compatibility

**Guides:**
- `stages/s5/s5_v2_validation_loop.md` (Round 1)
- `stages/s5/s5_v2_validation_loop.md` (Round 2)
- `stages/s5/s5_p3_planning_round3.md` (Round 3)

**Note:** v1 guides remain available but are deprecated. v2 is the standard going forward.

---

## Troubleshooting

### Problem: "I'm stuck in validation loop, keep finding issues"

**Symptoms:**
- Reached Round 10+
- Finding 1-2 issues every round
- Cannot achieve 3 consecutive clean rounds

**Diagnosis:**
- Pattern 1: Spec ambiguity (keep interpreting requirements differently)
- Pattern 2: Architecture mismatch (plan doesn't fit codebase)
- Pattern 3: Scope creep (adding unrequested features)

**Solution:**
- Document issue pattern
- Escalate to user with analysis
- User decides: adjust scope, clarify spec, return to S2, override validation

---

### Problem: "My draft is only 50% complete after 90 minutes"

**Symptoms:**
- Missing sections in implementation_plan.md
- Algorithm matrix has <30 mappings
- Only 50-60% of requirements have tasks

**Diagnosis:**
- Normal for complex features
- Draft phase is time-boxed at 90 minutes

**Solution:**
- STOP at 90 minutes even if 50% complete
- Start validation loop with incomplete draft
- Rounds 1-3 will catch all missing content
- Validation loop will force completion to 100%

**Why this works:** Better to start validating 50% draft than delay validation for 95% draft. Validation loop systematically forces completion.

---

### Problem: "Round 1 found 20+ issues"

**Symptoms:**
- Round 1 found >20 issues
- Took 90+ minutes to fix all issues
- Concerned about time

**Diagnosis:**
- Normal for first round (draft was 70% complete)
- Rounds 2-3 will find fewer issues (typically 5-10, then 1-3)
- Total time still faster than v1

**Solution:**
- Fix ALL 20+ issues before Round 2
- Document fixes in VALIDATION_LOOP_LOG.md
- Continue to Round 2 (expect fewer issues)
- Trust the process (time savings happen over full loop)

**Historical data:** Round 1: 10-20 issues, Round 2: 5-10 issues, Round 3: 1-5 issues, Round 4+: 0-2 issues → Exit

---

### Problem: "I found spec discrepancy in Dimension 11"

**Symptoms:**
- Dimension 11 check revealed spec.md contradicts epic notes
- Not sure how to proceed

**Diagnosis:**
- CRITICAL issue (must resolve before continuing)
- Same as v1 Iteration 21 (Spec Validation Gate)

**Solution:**
1. **STOP validation loop immediately**
2. **Document all discrepancies found**
3. **Report to user with 3 options:**
   - Option A: Fix spec.md, restart validation loop from Round 1 (recommended)
   - Option B: Fix spec.md and implementation_plan.md, continue validation (faster but riskier)
   - Option C: Discuss discrepancies first
4. **Wait for user decision** (no autonomous resolution)
5. **After user decision:**
   - If spec.md changed → RESTART validation loop from Round 1
   - If implementation_plan.md changed → Continue validation from current round

---

### Problem: "Validation loop completed, but user rejected at Gate 5"

**Symptoms:**
- Achieved 3 consecutive clean rounds
- Presented to user for Gate 5 approval
- User requests changes or rejects approach

**Diagnosis:**
- User feedback on implementation strategy
- May require replanning

**Solution:**

**If minor changes:**
- Update implementation_plan.md per user feedback
- Re-present to user (no re-validation needed)

**If major changes:**
- Update implementation_plan.md
- Re-run validation loop on affected dimensions
- Achieve 3 clean rounds again
- Re-present to user

**If rejection:**
- User wants different approach
- May need to return to S2 to revise spec.md
- Follow user guidance

---

## Summary: v1 vs v2 Quick Reference

| Aspect | S5 v1 | S5 v2 |
|--------|-------|-------|
| **Guide** | 5 guides (Rounds 1, 2, 3) | 1 guide (s5_v2_validation_loop.md) |
| **Structure** | 22 iterations | 2 phases (Draft + Validation Loop) |
| **Time** | 9-11 hours | 4.5-7 hours |
| **Approach** | Sequential iterations | Iterative validation rounds |
| **Exit Criteria** | Complete all 22 | 3 consecutive clean rounds |
| **Quality Proof** | Agent self-reports | Objective (3 clean rounds) |
| **Re-verification** | 3x separate iterations | Every round checks all dimensions |
| **Redundancy** | High (3x checks) | Zero (consolidated dimensions) |
| **Gates** | 5 separate gates (4a, 7a, 23a, 24, 25) | Embedded in dimensions |
| **Issue Handling** | Continue to next iteration | Fix immediately, reset counter |
| **Reading Pattern** | Linear | Varied (sequential, reverse, spot-checks) |
| **Documentation** | implementation_plan.md | implementation_plan.md + VALIDATION_LOOP_LOG.md |
| **Status** | DEPRECATED | **CURRENT STANDARD** |

---

## Next Steps

**If you're starting a new feature:**
1. Read `stages/s5/s5_v2_validation_loop.md`
2. Use "Starting S5 v2" prompt from `prompts_reference_v2.md`
3. Follow the 2-phase approach (Draft + Validation Loop)

**If you have questions:**
- Check FAQ section above
- Review `S5_V2_DESIGN_PLAN.md` for architecture details
- Ask user for clarification on specific scenarios

**If you encounter issues:**
- Check Troubleshooting section above
- Escalate to user if stuck after 10 rounds
- Document lessons learned for future improvements

---

**Last Updated:** 2026-02-09
**Version:** 1.0
**Status:** Active (v2 is current standard, v1 is deprecated)
