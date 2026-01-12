# Stage 5: Feature Implementation
## Phase 5.1: Implementation Planning
### Part 5.1.2: Round 2 (Iterations 8-16)

**File:** `part_5.1.2_round2.md`

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

## Quick Start

**What is this stage?**
Round 2 of Implementation Planning is the deep verification phase where you create comprehensive test strategy, identify edge cases, and re-verify critical matrices through 9 mandatory iterations (8-16) to catch bugs introduced during Round 1.

**When do you use this guide?**
- Round 1 complete (STAGE_5aa passed)
- Confidence level is MEDIUM or higher
- Ready for deep verification of implementation plan

**Key Outputs:**
- ✅ implementation_plan.md "Test Strategy" section added (>90% coverage required)
- ✅ implementation_plan.md "Edge Cases" section added
- ✅ Algorithm Traceability Matrix re-verified (Iteration 11)
- ✅ E2E Data Flow re-verified (Iteration 12)
- ✅ Integration Gap Check re-verified (Iteration 14)
- ✅ Test Coverage Depth Check passed (Iteration 15)
- ✅ implementation_plan.md updated to v2.0

**Time Estimate:**
45-60 minutes (9 iterations)

**Exit Condition:**
Round 2 is complete when all 9 iterations pass, test coverage exceeds 90%, confidence level is at least MEDIUM, and you're ready to proceed to Round 3

---

## Navigation - Iteration Guides

**This is a ROUTER guide.** Detailed iteration instructions are in separate files:

**Iterations 8-10: Test Strategy & Configuration**
📖 **READ:** `stages/stage_5/round2/iterations_8_10_test_strategy.md`
- Iteration 8: Test Strategy Development
- Iteration 9: Edge Case Enumeration
- Iteration 10: Configuration Change Impact

**Iterations 11-12: Re-verification**
📖 **READ:** `stages/stage_5/round2/iterations_11_12_reverification.md`
- Iteration 11: Algorithm Traceability Matrix (Re-verify)
- Iteration 12: End-to-End Data Flow (Re-verify)

**Iterations 13-16: Final Verification & Documentation**
📖 **READ:** `stages/stage_5/round2/iterations_13_16_final_checks.md`
- Iteration 13: Dependency Version Check
- Iteration 14: Integration Gap Check (Re-verify)
- Iteration 15: Test Coverage Depth Check
- Iteration 16: Documentation Requirements

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 9 iterations in Round 2 are MANDATORY (no skipping)
   - Iterations 8-16
   - Each iteration deepens verification

2. ⚠️ Execute iterations IN ORDER (not parallel, not random)
   - Later iterations depend on earlier findings

3. ⚠️ Re-verification iterations (11, 12, 14) are CRITICAL
   - Algorithm Traceability Matrix re-verify (Iteration 11)
   - E2E Data Flow re-verify (Iteration 12)
   - Integration Gap Check re-verify (Iteration 14)
   - These catch bugs introduced during Round 1 updates

4. ⚠️ Test Coverage Depth Check (Iteration 15)
   - Verify tests cover edge cases, not just happy path
   - Target: >90% coverage

5. ⚠️ STOP if confidence < Medium at Round 2 checkpoint
   - Update questions file
   - Wait for user answers
   - Do NOT proceed to Round 3

6. ⚠️ Update feature README.md Agent Status after Round 2 complete
   - Document confidence level
   - Document next action
```

---

## Critical Decisions Summary

**Round 2 has 1 major decision point:**

### Decision Point 1: Test Coverage Threshold (Iteration 15)
**Question:** Does test coverage meet the >90% requirement?
- **If NO (coverage < 90%):**
  - Identify uncovered edge cases
  - Add tests to cover gaps
  - Re-run Iteration 15 to verify >90% coverage
  - Do NOT proceed to Iteration 16 until threshold met
- **If YES (coverage >= 90%):**
  - ✅ Proceed to Iteration 16 (Confidence Checkpoint)
  - Complete Round 2
- **Impact:** Insufficient test coverage means bugs will escape to production

**At End of Round 2: Confidence Checkpoint (Iteration 16)**
**Question:** Is confidence level >= MEDIUM after deep verification?
- **If < MEDIUM:**
  - Update questions.md with remaining uncertainties
  - Wait for user answers
  - DO NOT proceed to Round 3
- **If >= MEDIUM:**
  - ✅ Proceed to Round 3 Part 1 (stages/stage_5/round3_part1_preparation.md)
  - Final verification and implementation readiness
- **Impact:** Low confidence after deep verification indicates fundamental gaps in understanding

**Note:** Round 2 has no MANDATORY GATES (like Iteration 4a in Round 1), but all 9 iterations are required and >90% test coverage is strongly recommended.

---

## Prerequisites Checklist

**Verify BEFORE starting Round 2:**

□ Round 1 (STAGE_5aa) complete
□ All 8 Round 1 iterations executed (1-7 + 4a)
□ Iteration 4a PASSED (TODO Specification Audit)
□ implementation_plan.md v1.0 created with:
  - Implementation Tasks section (all requirements covered)
  - All tasks have acceptance criteria
  - Component Dependencies section
  - Algorithm Traceability Matrix section
  - Integration Gap Check complete
□ Confidence level: >= MEDIUM (from Round 1 checkpoint)
□ No blockers in feature README.md Agent Status

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with Round 2
- Return to Round 1 to complete prerequisites
- Document blocker in Agent Status

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│              ROUND 2: Deep Verification                      │
│                    (9 Iterations)                             │
└──────────────────────────────────────────────────────────────┘

Iterations 8-10: Test Strategy & Configuration
   📖 READ: stages/stage_5/round2/iterations_8_10_test_strategy.md
   - Test Strategy Development (Iteration 8)
   - Edge Case Enumeration (Iteration 9)
   - Configuration Change Impact (Iteration 10)
   ↓
Iterations 11-12: Re-verification
   📖 READ: stages/stage_5/round2/iterations_11_12_reverification.md
   - Algorithm Traceability Matrix Re-verify (Iteration 11)
   - End-to-End Data Flow Re-verify (Iteration 12)
   ↓
Iterations 13-16: Final Verification & Documentation
   📖 READ: stages/stage_5/round2/iterations_13_16_final_checks.md
   - Dependency Version Check (Iteration 13)
   - Integration Gap Check Re-verify (Iteration 14)
   - Test Coverage Depth Check (Iteration 15)
   - Documentation Requirements (Iteration 16)
   ↓
ROUND 2 CHECKPOINT
   ↓
If confidence >= MEDIUM: Proceed to Round 3 (Part 5.1.3)
If confidence < MEDIUM: Update questions file, wait for user
```

---

## ROUND 2 CHECKPOINT

**After completing all 9 iterations (8-16):**

1. **Update implementation_plan.md to v2.0:**
   - Add version history entry documenting Round 2 completion
   - Include test coverage percentage (must be >90%)
   - List all sections added (Test Strategy, Edge Cases, etc.)

2. **Update feature README.md Agent Status:**
   - Current step: Round 2 complete (16/24 total iterations)
   - Confidence level: HIGH/MEDIUM/LOW
   - Next action: Based on confidence level (see below)

3. **Evaluate Confidence Level:**
   - **If confidence >= MEDIUM:**
     - ✅ Proceed to Round 3 Part 1
     - **Next Guide:** `stages/stage_5/round3_part1_preparation.md`
   - **If confidence < MEDIUM:**
     - ❌ STOP - Update questions.md with uncertainties
     - Wait for user answers before proceeding

**Decision Point:**
- Test coverage >90%: Required for Round 2 completion
- Confidence >= MEDIUM: Required to proceed to Round 3
- If either fails: Address gaps before continuing

---

## Completion Criteria

**Round 2 is complete when ALL of these are true:**

□ All 9 iterations executed (8-16) in order
□ implementation_plan.md updated to v2.0 with:
  - Test Strategy section (unit, integration, edge, regression)
  - Edge Cases section (all cases enumerated and handled)
  - Algorithm Traceability Matrix updated (re-verified)
  - E2E Data Flow updated (re-verified)
  - Integration Gap Check updated (re-verified)
  - Test coverage >90%
  - Documentation tasks added
□ Feature README.md updated:
  - Agent Status: "Round 2 complete"
  - Confidence level documented
  - Test coverage documented

**If any item unchecked:**
- ❌ Round 2 is NOT complete
- Complete missing items before proceeding

---

## Common Mistakes to Avoid

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll skip re-verification iterations (11, 12, 14)"
   ✅ STOP - Re-verification catches bugs from Round 1 updates

❌ "Test coverage is 85%, close enough"
   ✅ STOP - Iteration 15 requires >90% coverage

❌ "I enumerated most edge cases, that's sufficient"
   ✅ STOP - Iteration 9 requires ALL edge cases

❌ "Algorithm matrix looks the same as Round 1"
   ✅ STOP - Round 1 likely added algorithms (error handling, etc.)

❌ "My confidence is medium-low, but I'll proceed to Round 3"
   ✅ STOP - Create/update questions file, wait for answers

❌ "Documentation can wait until after implementation"
   ✅ STOP - Iteration 16 plans documentation NOW

❌ "I'll batch these 9 iterations efficiently"
   ✅ STOP - NEVER say "efficiently", "quickly", or "batch" iterations
   ✅ Execute ONE iteration at a time, follow EVERY step
   ✅ Batching iterations leads to skipped verification steps and bugs
```

---

## Prerequisites for Round 3

**Before transitioning to Round 3, verify:**

□ Round 2 completion criteria ALL met
□ All 9 iterations executed (8-16)
□ implementation_plan.md updated to v2.0
□ Test coverage: >90%
□ Confidence level: >= MEDIUM
□ Feature README.md Agent Status updated with next action

**If any prerequisite fails:**
- ❌ Do NOT transition to Round 3
- Complete Round 2 missing items

---

## Next Round

**After completing Round 2:**

📖 **READ:** `stages/stage_5/round3_part1_preparation.md`
🎯 **GOAL:** Preparation iterations (17-22) - implementation phasing, rollback strategy, algorithm traceability (final), performance, mock audit
⏱️ **ESTIMATE:** 60-90 minutes for Part 1, then 1.5-2.5 hours for Part 2

**Round 3 Overview:**
- **Part 1:** Preparation (Iterations 17-22)
- **Part 2:** Final Gates (Iterations 23, 23a, 25, 24) with MANDATORY audits

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Round 3.

---

## See Also

**Related Guides:**
- `stages/stage_5/round1_todo_creation.md` - Round 1 (Initial Analysis)
- `stages/stage_5/round3_part1_preparation.md` - Round 3 Part 1 (Preparation)
- `stages/stage_5/round3_part2_final_gates.md` - Round 3 Part 2 (Final Gates)

**Iteration Details (Round 2):**
- `stages/stage_5/round2/iterations_8_10_test_strategy.md` - Iterations 8-10
- `stages/stage_5/round2/iterations_11_12_reverification.md` - Iterations 11-12
- `stages/stage_5/round2/iterations_13_16_final_checks.md` - Iterations 13-16

**Reference:**
- `prompts_reference_v2.md` - Phase transition prompts (MANDATORY)
- `README.md` - Complete workflow overview

---

*End of stages/stage_5/round2_todo_creation.md*
