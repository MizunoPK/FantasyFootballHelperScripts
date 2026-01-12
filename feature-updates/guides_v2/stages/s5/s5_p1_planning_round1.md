# S5: Feature Implementation
## S5.P1: Implementation Planning
### S5.P1: Planning Round 1 (Iterations 1-7 + Gates 4a, 7a)

**File:** `part_5.1.1_round1.md`

🚨 **MANDATORY READING PROTOCOL**

**Before starting this guide:**
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
Planning Round 1 of Implementation Planning is the initial analysis phase where you verify requirements coverage, map dependencies, trace algorithms to code locations, and analyze downstream consumption through 9 mandatory iterations (1-7 + 4a + 7a).

**When do you use this guide?**
- S4 complete (Epic Testing Strategy updated + Gate 4.5 user approval passed)
- Feature spec.md is finalized
- Ready to create implementation plan

**Key Outputs:**
- ✅ implementation_plan.md v1.0 created with initial sections
- ✅ Implementation Tasks section added (with file/line/code details)
- ✅ Interface Verification complete (exact method signatures verified)
- ✅ Dependencies mapped and verified
- ✅ Algorithm Traceability Matrix section added (40+ mappings typical)
- ✅ Gate 4a PASSED (Implementation Plan Specification Audit - MANDATORY GATE)
- ✅ Component Dependencies section added
- ✅ Downstream consumption verified (Iteration 5a)
- ✅ Integration verified (no orphan code - Iteration 7)
- ✅ Backward compatibility analyzed (Iteration 7a)

**Time Estimate:**
45-60 minutes (9 iterations)

**Exit Condition:**
Planning Round 1 is complete when all 9 iterations pass (including Gate 4a mandatory gate), confidence level is at least MEDIUM, and you're ready to proceed to Planning Round 2

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 9 iterations in Planning Round 1 are MANDATORY (no skipping)
   - Iterations 1-7 + Iteration 4a + Iteration 7a
   - Each iteration catches specific bug categories
   - Iteration 5a prevents "data loads but calculation fails" bugs
   - Iteration 7a prevents backward compatibility bugs

2. ⚠️ Execute iterations IN ORDER (not parallel, not random)
   - Later iterations depend on earlier findings

3. ⚠️ Gate 4a (TODO Specification Audit) is a MANDATORY GATE
   - CANNOT proceed to Iteration 5 without PASSING Gate 4a
   - Every implementation task MUST have acceptance criteria

4. ⚠️ NEVER ASSUME - IMPLEMENTATION TASKS MUST TRACE TO SPEC REQUIREMENTS
   - Every implementation task must map to explicit spec.md requirement
   - Do NOT add tasks based on "best practices" or assumptions
   - Do NOT add tasks the user didn't ask for
   - If uncertain about a task → create question in questions.md
   - Only create implementation tasks for confirmed, documented requirements

5. ⚠️ Interface Verification Protocol: READ actual source code
   - Never assume interface - always verify (Iteration 2)
   - Copy-paste exact method signatures

6. ⚠️ Algorithm Traceability Matrix (Iteration 4)
   - Map EVERY algorithm in spec to exact code location
   - Typical matrix has 40+ mappings

7. ⚠️ Integration Gap Check (Iteration 7)
   - For EVERY new method: identify caller
   - No orphan code allowed

8. ⚠️ STOP if confidence < Medium at Planning Round 1 checkpoint
   - Create questions file
   - Wait for user answers
   - Do NOT proceed to Planning Round 2

9. ⚠️ Update feature README.md Agent Status after Planning Round 1 complete
   - Document confidence level
   - Document next action
```

---

## Prerequisites Checklist

**Verify BEFORE starting Planning Round 1:**

□ S4 (Epic Testing Strategy) complete + Gate 4.5 passed (user approved test plan)
□ This feature's spec.md is complete:
  - All sections filled (Components, Data Structures, Algorithms, Dependencies)
  - No "TBD" or placeholder content
  - All algorithms documented with pseudocode
□ This feature's checklist.md shows all items resolved
□ epic_smoke_test_plan.md updated (S4 version)
□ No blockers in feature README.md Agent Status

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with Planning Round 1
- Return to previous stage to complete prerequisites
- Document blocker in Agent Status

---

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│          ROUND 1: Initial Analysis & Planning                │
│                    (9 Iterations)                             │
└──────────────────────────────────────────────────────────────┘

Iterations 1-3: Requirements & Dependencies
   ↓
Iteration 4: Algorithm Traceability Matrix
   ↓
Gate 4a: TODO Specification Audit (MANDATORY GATE)
   ↓
Iterations 5-6: Data Flow & Error Handling
   ↓
Iteration 7: Integration & Compatibility
   ↓
ROUND 1 CHECKPOINT
   ↓
If confidence >= MEDIUM: Proceed to Planning Round 2
If confidence < MEDIUM: Create questions file, wait for user
```

---

## ROUND 1: Iteration Details

### Iterations 1-3: Requirements Analysis & Dependencies

**📖 READ:** `stages/s5/round1/iterations_1_3_requirements.md`

**Covers:**
- **Iteration 1:** Requirements Coverage Check - Verify every spec requirement has implementation tasks
- **Iteration 2:** Component Dependency Mapping - Read actual source code, verify interfaces
- **Iteration 3:** Data Structure Verification - Verify data structures from source code

**Key Outputs:**
- implementation_plan.md created with Implementation Tasks section
- All tasks trace to spec.md requirements (no assumptions)
- All interfaces verified from actual source code (no guessing)

**Critical Rule:** Tasks ONLY for explicit spec requirements - if uncertain → questions.md

---

### Iteration 4 + Gate 4a: Algorithm Tracing & Audit

**📖 READ:** `stages/s5/round1/iteration_4_algorithms.md`

**Covers:**
- **Iteration 4:** Algorithm Traceability Matrix - Map EVERY spec algorithm to exact code location
- **Gate 4a:** TODO Specification Audit (MANDATORY) - Verify EVERY task has acceptance criteria

**Key Outputs:**
- Algorithm Traceability Matrix section added to implementation_plan.md (40+ mappings typical)
- Gate 4a: PASSED (all tasks have acceptance criteria)

**🛑 MANDATORY GATE:** Cannot proceed to Iteration 5 without PASSING Gate 4a

---

### Iterations 5-6: Data Flow & Error Handling

**📖 READ:** `stages/s5/round1/iterations_5_6_dependencies.md`

**Covers:**
- **Iteration 5:** End-to-End Data Flow - Document complete data flow from entry to output
- **Iteration 5a:** Downstream Consumption Tracing (CRITICAL) - Verify how loaded data is CONSUMED
- **Iteration 6:** Error Handling Scenarios - Document failure modes and recovery

**Key Outputs:**
- Data flow section added to implementation_plan.md
- Downstream consumption verified (prevents "data loads but calculation fails" bugs)
- Error handling scenarios documented

**🚨 CRITICAL:** Iteration 5a prevents catastrophic bugs where data loads successfully but calculations fail

---

### Iteration 7 + 7a: Integration & Compatibility

**📖 READ:** `stages/s5/round1/iteration_7_integration.md`

**Covers:**
- **Iteration 7:** Integration Gap Check - Verify EVERY new method has an identified caller
- **Iteration 7a:** Backward Compatibility Analysis - Handle old data formats gracefully
- **ROUND 1 CHECKPOINT:** Evaluate confidence, decide Planning Round 2 vs questions.md

**Key Outputs:**
- Integration matrix (no orphan code)
- Backward compatibility strategy documented
- Confidence level evaluated (HIGH/MEDIUM/LOW)

**Decision Point:**
- If confidence >= MEDIUM: Proceed to Planning Round 2
- If confidence < MEDIUM: Create questions.md, wait for user answers

---

## Completion Criteria

**Planning Round 1 is complete when ALL of these are true:**

□ All 9 iterations executed (1-7 + 4a + 7a) in order
□ Gate 4a PASSED (TODO Specification Audit)
□ implementation_plan.md v1.0 created with:
  - All requirements covered by tasks
  - All tasks have acceptance criteria
  - Dependencies verified from source code
  - Algorithm Traceability Matrix created (40+ mappings)
  - Integration Gap Check complete (no orphan code)
  - Downstream consumption verified
  - Backward compatibility analyzed
  - E2E data flow documented
□ Feature README.md updated:
  - Agent Status: "Planning Round 1 complete (9/9 iterations)"
  - Confidence level documented
  - Next action documented

**If any item unchecked:**
- ❌ Planning Round 1 is NOT complete
- Complete missing items before proceeding

---

## Common Mistakes to Avoid

```
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll skip iteration X, seems simple"
   ✅ STOP - ALL 9 iterations MANDATORY, no exceptions

❌ "I'll assume ConfigManager.get_adp_multiplier interface"
   ✅ STOP - READ actual source code, verify interface (Iteration 2)

❌ "My confidence is low but I'll proceed to Planning Round 2"
   ✅ STOP - Create questions file, wait for answers

❌ "Implementation tasks can be vague, I'll figure it out later"
   ✅ STOP - Gate 4a requires acceptance criteria for EVERY task

❌ "I mapped most algorithms, that's good enough"
   ✅ STOP - Algorithm Traceability Matrix must map ALL algorithms

❌ "This new method seems obvious, don't need caller"
   ✅ STOP - Integration Gap Check requires caller for EVERY new method

❌ "Gate 4a failed but I'll proceed anyway"
   ✅ STOP - Gate 4a is MANDATORY GATE, must PASS

❌ "I'll skip Iteration 5a, data loading is verified"
   ✅ STOP - Iteration 5a checks CONSUMPTION not LOADING

❌ "I'll complete all iterations efficiently to make progress"
   ✅ STOP - NEVER say "efficiently", "quickly", or "batch" iterations
   ✅ Execute ONE iteration at a time, follow EVERY step
   ✅ Saying "efficiently" is a RED FLAG indicating cutting corners
   ✅ The guides exist to prevent mistakes - skipping ANY step WILL lead to bugs
```

---

## Prerequisites for Planning Round 2 (STAGE_5ab)

**Before transitioning to Planning Round 2, verify:**

□ Planning Round 1 completion criteria ALL met
□ Gate 4a shows: ✅ PASS
□ Confidence level: >= MEDIUM
□ Feature README.md shows:
  - Planning Round 1 complete (9/9)
  - Gate 4a: PASSED
  - Confidence: HIGH or MEDIUM
  - Next Action: Read Planning Round 2 guide (stages/s5/round2_todo_creation.md)

**If any prerequisite fails:**
- ❌ Do NOT transition to Planning Round 2
- Complete Planning Round 1 missing items

---

## Next Round

**After completing Planning Round 1:**

📖 **READ:** `stages/s5/round2_todo_creation.md`
🎯 **GOAL:** Deep verification - test strategy, edge cases, re-verification
⏱️ **ESTIMATE:** 45-60 minutes

**Planning Round 2 will:**
- Develop comprehensive test strategy (Iteration 8)
- Enumerate all edge cases (Iteration 9)
- Re-verify algorithms, data flow, integration (Iterations 11, 12, 14)
- Check test coverage depth (Iteration 15)
- Plan documentation (Iteration 16)

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Planning Round 2.

---

**END OF ROUND 1 GUIDE**
