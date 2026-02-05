# S5: Feature Implementation
## S5.P1: Implementation Planning
### S5.P3: Round 3
#### Step 5.1.3.3: Part 2b (Iterations 21, 22: Gates 25, 24)

**File:** `s5_p3_i3_gates_part2.md`

🚨 **MANDATORY READING PROTOCOL**

**Before starting this round:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update feature README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check feature README.md Agent Status for current iteration
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Overview

**What is this iteration?**
Iterations 21-22: Gate 24 (GO/NO-GO) and Gate 25 (Spec Validation) - Final gates before implementation

---

## Quick Start

**What is this guide?**
Part 2b of Round 3 is the final validation phase where you verify integration (Iteration 23), audit spec alignment (Gate 23a), validate against all user-approved sources (Iteration 21), and make the final GO/NO-GO decision (Iteration 22) through 4 mandatory iterations.

**When do you use this guide?**
- Part 2a (Round_3_Part_2a) complete
- Iterations 14-19 done
- Ready for final validation and GO/NO-GO decision

**Key Outputs:**
- ✅ Integration Gap Check complete (Iteration 23 - no orphan code)
- ✅ Gate 23a PASSED (Pre-Implementation Spec Audit - ALL 4 PARTS)
- ✅ Iteration 21 PASSED (Spec Validation - zero discrepancies with validated sources)
- ✅ Iteration 22 GO DECISION (Implementation Readiness)
- ✅ Gate 5 PASSED (User Approval of implementation_plan.md)

**Time Estimate:**
60-90 minutes (4 iterations + user approval)

**Exit Condition:**
Part 2b is complete when all 4 iterations pass (including Gates 23a and 25), user approves implementation_plan.md (Gate 5), confidence level is at least MEDIUM, and you're ready to proceed to S6

---

## Workflow Overview

```text
┌──────────────────────────────────────────────────────────────┐
│       PART 2b: Final Validation & GO/NO-GO                   │
│                  (4 Iterations)                               │
└──────────────────────────────────────────────────────────────┘

Prerequisites Met?
  ├─ Part 2a complete (Iterations 14-19)
  ├─ No blockers
  └─ Ready for final validation
         │
         ▼
Iteration 19: Integration Gap Check
   ↓
Gate 23a: Pre-Implementation Spec Audit (MANDATORY - 4 PARTS)
   ↓
Iteration 21: Spec Validation vs Validated Sources (CRITICAL)
   ↓
Iteration 22: Implementation Readiness (GO/NO-GO)
   ↓
Gate 5: User Approval of implementation_plan.md (MANDATORY)
   ↓
If ALL gates pass + user approval: Proceed to S6
If ANY gate fails: Fix issues, re-run
```markdown

---

## Critical Rules

```text
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 4 iterations in Part 2b are MANDATORY (no skipping)
   - Iterations 23, 23a (Gate 2), 25 (Gate 3 Part A), 24 (Gate 3 Part B)
   - Each iteration catches specific bug categories
   - Iteration 21 prevents Feature 02 catastrophic bug

2. ⚠️ Execute iterations IN ORDER (not parallel, not random)
   - Later iterations depend on earlier findings

3. ⚠️ Gate 23a (Pre-Implementation Spec Audit) is a MANDATORY GATE
   - ALL 4 PARTS must PASS to proceed
   - Cannot proceed to Iteration 21 without passing Gate 23a

4. ⚠️ Iteration 21 (Spec Validation) is CRITICAL - prevents wrong implementation
   - MUST validate spec.md against ALL validated sources
   - If discrepancies found → STOP and report to user
   - User decides: restart TODO OR fix and continue
   - CANNOT proceed to Iteration 22 without passing Iteration 21

5. ⚠️ Iteration 22 requires "GO" decision to proceed
   - Cannot proceed to S6 without GO
   - If NO-GO → Fix blockers, re-run Iteration 22
   - GO requires: confidence >= MEDIUM, all gates passed

6. ⚠️ Gate 5 (User Approval) is MANDATORY before S6
   - MUST present implementation_plan.md to user
   - WAIT for explicit user approval
   - Cannot proceed without approval

7. ⚠️ Close spec.md during Iteration 21 (avoid confirmation bias)
   - Re-read epic notes independently
   - Then compare spec to ALL validated sources
   - Ask critical questions (example vs special case)

8. ⚠️ Update feature README.md Agent Status after each iteration
   - Document gate results (PASSED/FAILED)
   - Document next action
```markdown

---

## Prerequisites Checklist

**Verify BEFORE starting Part 2b:**

□ Part 2a (Round_3_Part_2a) complete (Iterations 14-19)
□ implementation_plan.md v2.0 complete with all Round 1 and Round 2 outputs
□ spec.md is complete (no TBD sections)
□ Confidence level >= MEDIUM (from Round 2)
□ Test coverage >90%
□ Epic validated source files exist:
  - feature-updates/{epic}/{epic}_notes.txt
  - feature-updates/{epic}/EPIC_TICKET.md
  - feature-updates/{epic}/{feature}/SPEC_SUMMARY.md
□ No blockers in feature README.md Agent Status

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with Part 2b
- Return to previous stage to complete prerequisites
- Document blocker in Agent Status

---

## PART 2b: Iteration Details

### Iteration 19: Integration Gap Check

**📖 READ:** `stages/s5/s5_p3_i2_gates_part1.md`

**Covers:**
- Integration Gap Check - Verify ALL implementation tasks have integration points
- No orphan code (every method has caller)
- End-to-end integration flow verified

**Key Outputs:**
- Integration verification matrix (all methods have callers)
- No orphan code identified
- Complete execution flow traced

**🚨 CRITICAL:** Prevents implementing code that never gets called

---

### Gate 23a: Pre-Implementation Spec Audit (MANDATORY)

**📖 READ:** `stages/s5/s5_p3_i2_gates_part1.md`

**Covers:**
- **PART 1:** Completeness - Every spec requirement has implementation tasks
- **PART 2:** Specificity - All tasks are specific (what/where/how defined)
- **PART 3:** Interface Contracts - All dependencies verified from source code
- **PART 4:** Integration Evidence - All integration sections documented

**Key Outputs:**
- ALL 4 PARTS must PASS
- Requirement → Task mapping (100% coverage)
- Interface verification from actual source code
- Integration documentation complete

**🛑 MANDATORY GATE:** Cannot proceed to Iteration 21 without passing ALL 4 PARTS

---

### Iterations 25 & 24: Final Validation and GO/NO-GO

**📖 READ:** `stages/s5/s5_p3_i3_gates_part2.md`

**Covers:**
- **Iteration 21:** Spec Validation Against Validated Documents (CRITICAL)
  - Validates spec.md against epic notes, epic ticket, spec summary
  - Prevents Feature 02 catastrophic bug (implementing wrong solution)
  - If discrepancies found → Report to user, await decision
- **Iteration 22:** Implementation Readiness Protocol (FINAL GATE)
  - Final GO/NO-GO decision
  - Must achieve GO to proceed to S6
  - Readiness checklist + confidence assessment

**Key Outputs:**
- Iteration 21: PASSED (zero discrepancies) OR user decision on fixes
- Iteration 22: GO DECISION (ready for implementation)
- Final validation complete

**🛑 CRITICAL GATES:** Both iterations are MANDATORY - cannot skip

---

## Gate 5: User Approval of Implementation Plan (MANDATORY)

**After Iteration 22 returns GO decision:**

1. **Check questions.md status:**
   - If open questions exist → Present to user first → Update plan → Ask restart confirmation
   - If no questions (or after user answers) → Proceed to step 2

2. **Present implementation_plan.md to user for approval:**
   - Use prompt from `prompts/s5_s8_prompts.md`
   - Highlight key sections (tasks, dependencies, test strategy, phasing)
   - Request explicit approval

3. **Wait for user response:**
   - If approved → Document approval, proceed to completion criteria
   - If changes requested → Revise plan, re-run affected iterations, re-submit

4. **Document approval in implementation_plan.md and Agent Status**

**📖 DETAILED PROCESS:** See `stages/s5/s5_p3_i3_gates_part2.md` for complete Gate 5 workflow

---

## Completion Criteria

**Part 2b is complete when ALL of these are true:**

### All Iterations Complete
- [ ] Iteration 19: Integration Gap Check - PASSED (no orphan code)
- [ ] Gate 23a: Pre-Implementation Spec Audit - ALL 4 PARTS PASSED
- [ ] Iteration 21: Spec Validation - PASSED (zero discrepancies)
- [ ] Iteration 22: Implementation Readiness - GO DECISION

### Mandatory Gates Passed
- [ ] Gate 23a (Pre-Implementation Spec Audit): ALL 4 PARTS PASSED
- [ ] Gate 3 Part A (Iteration 21): Spec verified against all validated sources
- [ ] Gate 3 Part B (Iteration 22): GO decision
- [ ] Gate 5 (User Approval): User explicitly approved implementation_plan.md

### Documentation Updated
- [ ] implementation_plan.md v3.0 contains all Part 2b outputs
- [ ] User approval documented in implementation_plan.md
- [ ] feature README.md Agent Status shows:
  - All iterations complete (23, 23a, 25, 24)
  - All gates PASSED
  - Gate 5: User approval timestamp
  - Phase: IMPLEMENTATION
  - Next Action: Read S6 guide

### Quality Verified
- [ ] Confidence level >= MEDIUM
- [ ] No blockers
- [ ] All checklists 100% complete

**If ALL items checked:**
- Part 2b is COMPLETE
- Round 3 is COMPLETE
- S5 is COMPLETE
- Ready to proceed to S6 (Implementation)
- Read `stages/s6/s6_execution.md`

**If ANY item unchecked:**
- STOP - Do not proceed to S6
- Complete missing items
- Re-verify completion criteria

---

## Common Mistakes to Avoid

```text
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll skip iteration X, seems simple"
   ✅ STOP - ALL 4 iterations MANDATORY, no exceptions

❌ "I'll skip Iteration 21, spec looks fine"
   ✅ STOP - Iteration 21 prevents Feature 02 catastrophic bug

❌ "Spec has minor discrepancy, I'll ignore it"
   ✅ STOP - Report ALL discrepancies to user, wait for decision

❌ "Confidence is LOW but I'll mark GO anyway"
   ✅ STOP - GO requires confidence >= MEDIUM

❌ "I'll proceed to S6 without user approval"
   ✅ STOP - Gate 5 is MANDATORY, must wait for approval

❌ "Gate 23a failed but I'll proceed anyway"
   ✅ STOP - Gate 23a is MANDATORY GATE, must PASS ALL 4 PARTS

❌ "I'll look at spec.md while re-reading epic notes"
   ✅ STOP - Close spec.md during Iteration 21 to avoid confirmation bias

❌ "I'll complete all iterations efficiently to make progress"
   ✅ STOP - NEVER say "efficiently", "quickly", or "batch" iterations
   ✅ Execute ONE iteration at a time, follow EVERY step
```

---

## Prerequisites for S6 (Implementation Execution)

**Before transitioning to S6, verify:**

□ Part 2b completion criteria ALL met
□ All 4 iterations complete (23, 23a, 25, 24)
□ Gate 23a shows: ✅ ALL 4 PARTS PASSED
□ Iteration 21 shows: ✅ PASSED (zero discrepancies)
□ Iteration 22 shows: ✅ GO DECISION
□ Gate 5 shows: ✅ USER APPROVED (with timestamp)
□ Confidence level: >= MEDIUM
□ feature README.md shows:
  - Part 2b complete (4/4 iterations)
  - All gates: PASSED
  - User approval: PASSED
  - Next Action: Read S6 guide

**If any prerequisite fails:**
- ❌ Do NOT transition to S6
- Complete Part 2b missing items

---

## Next Stage

**After completing Part 2b (with user approval):**

📖 **READ:** `stages/s6/s6_execution.md`
🎯 **GOAL:** Implement tasks from implementation_plan.md with continuous verification
⏱️ **ESTIMATE:** Varies by feature complexity

**S6 will:**
- Create implementation_checklist.md from implementation_plan.md tasks
- Implement from implementation_plan.md (PRIMARY reference), spec.md (context/verification)
- Update checklist in real-time as tasks complete
- Run mini-QC checkpoints every 5-7 tasks
- Require 100% test pass after each step

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S6.

---

## See Also

**Iteration Guides:**
- `stages/s5/s5_p3_i2_gates_part1.md` - Integration Gap Check
- `stages/s5/s5_p3_i2_gates_part1.md` - Pre-Implementation Spec Audit (4 Parts)
- `stages/s5/s5_p3_i3_gates_part2.md` - Spec Validation + GO/NO-GO + Gate 5

**Supporting References:**
- `stages/s5/s5_p1_planning_round1.md` - Round 1 reference
- `stages/s5/s5_p2_planning_round2.md` - Round 2 reference
- `stages/s5/s5_p3_planning_round3.md` - Part 1 reference
- `stages/s5/s5_p3_i2_gates_part1.md` - Part 2a reference
- `prompts_reference_v2.md` - Phase transition prompts
- `mandatory_gates.md` - Gate requirements


## Exit Criteria

**Iterations 21-22 complete when ALL of these are true:**

- [ ] Gate 24 (GO/NO-GO) passed
- [ ] Gate 25 (Spec Validation) passed  
- [ ] Agent Status updated
- [ ] Ready to proceed to S6 (Implementation)

**If any criterion unchecked:** Complete missing items before proceeding

---
---

**END OF PART 2b GUIDE**
