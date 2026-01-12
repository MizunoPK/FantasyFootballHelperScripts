# Workflow Diagrams - Visual Quick Reference

**Purpose:** Visual diagrams for all major workflows in the Epic-Driven Development v2 process

**Last Updated:** 2026-01-04

---

## Table of Contents

1. [Complete Epic Workflow (Stages 1-7)](#complete-epic-workflow-stages-1-7)
2. [Stage 5: Feature Implementation Lifecycle](#stage-5-feature-implementation-lifecycle)
3. [Stage 5a: TODO Creation (3 Rounds)](#stage-5a-todo-creation-3-rounds)
4. [Stage 5c: Post-Implementation (3 Phases)](#stage-5c-post-implementation-3-phases)
5. [Stage 9: Epic-Level Final QC](#stage-6-epic-level-final-qc)
6. [Debugging Loop-Back Flow](#debugging-loop-back-flow)
7. [Missed Requirement Workflow](#missed-requirement-workflow)
8. [Decision Point: Skip 5d/5e?](#decision-point-skip-5d5e)
9. [Restart Protocols](#restart-protocols)

---

## Complete Epic Workflow (Stages 1-7)

```
Epic-Driven Development v2 - Complete Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User creates {epic_name}.txt
         ↓
┌─────────────────────────────────────────────┐
│ STAGE 1: Epic Planning                     │
│ - Analyze epic                              │
│ - Propose feature breakdown (user approves) │
│ - Create folder structure                   │
│ - Create epic files (README, test plan)     │
│ Time: 30-45 minutes                         │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ STAGE 2: Feature Deep Dives                 │
│ - Loop through ALL features                 │
│ - Flesh out spec.md for each                │
│ - Interactive question resolution           │
│ - Compare to completed features             │
│ Time: 1-3 hours per feature                 │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ STAGE 3: Cross-Feature Sanity Check         │
│ - Pairwise comparison of all specs          │
│ - Resolve conflicts/inconsistencies         │
│ - User sign-off on aligned specs            │
│ Time: 30-60 minutes                         │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ STAGE 4: Epic Testing Strategy              │
│ - Update epic_smoke_test_plan.md            │
│ - Identify integration points               │
│ - Define epic success criteria              │
│ Time: 30-45 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [🚨 GATE 4.5: User approves test plan?]
    ├─ NO → Revise test plan → Re-present
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ STAGE 5: Feature Implementation             │
│ - Loop PER FEATURE (5a→5b→5c→5d→5e)        │
│ - 28 verification iterations in 5a          │
│ - Smoke testing + 3 QC rounds in 5c         │
│ - Update specs/test plan after each feature │
│ Time: 2-5 hours per feature                 │
└─────────────────────────────────────────────┘
         ↓
    [All features complete?]
    ├─ NO → Next feature's Stage 5a
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ STAGE 6: Epic-Level Final QC                │
│ - Execute epic_smoke_test_plan.md           │
│ - 3 epic-level QC rounds                    │
│ - Validate against epic request             │
│ Time: 1-2 hours                             │
└─────────────────────────────────────────────┘
         ↓
    [Stage 9 passed?]
    ├─ NO → Debugging → RESTART Stage 9
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ STAGE 7: Epic Cleanup                       │
│ - Run unit tests (100% pass required)       │
│ - User testing (MANDATORY GATE)             │
│ - Commit changes                            │
│ - Push branch and create Pull Request      │
│ - User reviews and merges PR                │
│ - Update EPIC_TRACKER.md                    │
│ - Move to done/ folder                      │
│ Time: 30-60 minutes (+ user review time)    │
└─────────────────────────────────────────────┘
         ↓
    [User testing passed?]
    ├─ NO → Debugging → RESTART Stage 9
    └─ YES → Proceed to PR creation
         ↓
    [User approved and merged PR?]
    ├─ NO → Address feedback → Push updates
    └─ YES → Epic Complete! ✅
```

---

## Stage 5: Feature Implementation Lifecycle

```
Single Feature Journey (5a → 5b → 5c → 5d → 5e)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Prerequisites: Stage 4 complete (Gate 4.5 passed), feature spec ready
         ↓
┌─────────────────────────────────────────────┐
│ Stage 5a: TODO Creation                     │
│ - Round 1: Initial TODO (7 iterations + 4a) │
│ - Round 2: Integration (9 iterations)       │
│ - Round 3: Preparation + Gates (10 iters)   │
│ - 3 MANDATORY GATES (4a, 23a, 25)           │
│ - GO/NO-GO decision (Iteration 24)          │
│ Time: 2.5-4 hours                           │
└─────────────────────────────────────────────┘
         ↓
    [Iteration 24 = GO?]
    ├─ NO → Fix issues, return to Round 3
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ Stage 5b: Implementation Execution          │
│ - Interface verification FIRST              │
│ - Implement phase-by-phase (5-6 phases)     │
│ - Run tests after EACH phase               │
│ - Keep spec.md visible at all times        │
│ - Mini-QC checkpoints                       │
│ Time: 1-4 hours                             │
└─────────────────────────────────────────────┘
         ↓
    [All tests pass?]
    ├─ NO → Fix tests, repeat
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ Stage 5c: Post-Implementation               │
│ - Step 1: Smoke Testing (3 parts)         │
│ - Step 2: QC Rounds (3 rounds)             │
│ - Step 3: Final Review (PR + Lessons)      │
│ Time: 45-90 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [Stage 5c passed?]
    ├─ NO → Create bug fix → RESTART 5c
    └─ YES → Feature complete!
         ↓
    [More features remaining?]
    ├─ NO → SKIP to Stage 9
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ Stage 5d: Post-Feature Alignment            │
│ - Review ACTUAL implementation              │
│ - Update remaining feature specs            │
│ - Document integration points               │
│ Time: 15-30 minutes                         │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ Stage 5e: Testing Plan Update               │
│ - Update epic_smoke_test_plan.md            │
│ - Add integration points discovered         │
│ - Update test scenarios                     │
│ Time: 15-30 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [More features remaining?]
    ├─ YES → Next feature's Stage 5a
    └─ NO → Stage 9 (Epic Final QC)
```

---

## Stage 5a: TODO Creation (3 Rounds)

```
TODO Creation - 24 Verification Iterations Across 3 Rounds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entry: Stage 4 complete (Gate 4.5 passed), feature spec.md ready
         ↓
┌─────────────────────────────────────────────┐
│ ROUND 1: Initial TODO Creation              │
│ (Iterations 1-7 + GATE 4a)                  │
│                                             │
│ Iteration 1: Core Structure                │
│ Iteration 2: Traceability Matrix            │
│ Iteration 3: Test Coverage Planning         │
│ Iteration 4: Dependency Mapping             │
│ Iteration 5: Edge Case Analysis             │
│ Iteration 6: Error Handling Planning        │
│ Iteration 7: Data Validation Planning       │
│ ──────────────────────────────────────────  │
│ GATE 4a: TODO Specification Audit (MANDATORY)│
│ Time: 30-45 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [Gate 4a PASSED?]
    ├─ NO → Fix issues, re-run Gate 4a
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ ROUND 2: Integration Verification           │
│ (Iterations 8-16)                           │
│                                             │
│ Iteration 8: Interface Contracts            │
│ Iteration 9: Integration Points             │
│ Iteration 10: Mock Strategy                 │
│ Iteration 11: Real Object Testing           │
│ Iteration 12: Component Interaction         │
│ Iteration 13: Configuration Requirements    │
│ Iteration 14: External Dependencies         │
│ Iteration 15: Backwards Compatibility       │
│ Iteration 16: API Surface Audit             │
│ Time: 45-60 minutes                         │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ ROUND 3 Part 1: Preparation                 │
│ (Iterations 17-22)                          │
│                                             │
│ Iteration 17: Implementation Phasing        │
│ Iteration 18: Rollback Strategy             │
│ Iteration 19: Algorithm Traceability (Final)│
│ Iteration 20: Performance Considerations    │
│ Iteration 21: Mock Audit & Integration Test │
│ Iteration 22: Output Consumer Validation    │
│ Time: 60-90 minutes                         │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ ROUND 3 Part 2a: Gates 1-2                  │
│ (Iterations 23, 23a)                        │
│                                             │
│ Iteration 23: Integration Gap Check (Final) │
│ ──────────────────────────────────────────  │
│ GATE 23a: Pre-Implementation Spec Audit     │
│   - Part 1: Completeness (Coverage=100%)   │
│   - Part 2: Specificity (Specificity=100%)  │
│   - Part 3: Interface Contracts (Verify=100%)│
│   - Part 4: Integration Evidence (Int=100%) │
│ Time: 30-40 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [Gate 23a PASSED (all 4 parts)?]
    ├─ NO → Fix issues, re-run Gate 23a
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ ROUND 3 Part 2b: Gate 3                     │
│ (Iterations 25, 24)                         │
│                                             │
│ GATE 25: Spec Validation (CRITICAL)         │
│   - Close spec.md (avoid bias)              │
│   - Re-read validated docs independently    │
│   - Three-way comparison                    │
│   - IF discrepancies → STOP, report to user│
│ ──────────────────────────────────────────  │
│ GATE 24: Implementation Readiness (GO/NO-GO)│
│   - All checklist items verified            │
│   - Confidence >= MEDIUM                    │
│   - All gates passed (4a, 23a, 25)          │
│ Time: 30-50 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [Iteration 24 = GO?]
    ├─ NO → Fix issues, return to appropriate round
    └─ YES → Stage 5b (Implementation)
```

---

## Stage 5c: Post-Implementation (3 Phases)

```
Post-Implementation Validation - 3 Phases
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entry: Stage 5b complete, all tests passing
         ↓
┌─────────────────────────────────────────────┐
│ PHASE 1: Smoke Testing (3 Parts)            │
│                                             │
│ Part 1: Import Test                         │
│   - Feature imports successfully            │
│   - No import errors                        │
│                                             │
│ Part 2: Entry Point Test                    │
│   - Main entry points work                  │
│   - Basic functionality confirmed           │
│                                             │
│ Part 3: E2E Execution Test (MANDATORY GATE) │
│   - End-to-end workflow succeeds            │
│   - Real data, real objects                 │
│   - Verify outputs match expectations       │
│ Time: 15-30 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [Smoke testing PASSED?]
    ├─ NO → Debugging → RESTART from Part 1
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ PHASE 2: QC Rounds (3 Rounds)                │
│                                             │
│ Round 1: Algorithm Verification             │
│   - Spec.md vs actual code (line-by-line)  │
│   - Algorithm traceability check            │
│   - Edge case handling verified             │
│                                             │
│ Round 2: Consistency & Standards            │
│   - Coding standards compliance             │
│   - Error handling patterns                 │
│   - Documentation completeness              │
│                                             │
│ Round 3: Integration & Edge Cases           │
│   - Integration point verification          │
│   - Edge case testing                       │
│   - Cross-feature interactions              │
│ Time: 30-45 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [All 3 QC rounds PASSED?]
    ├─ NO → Debugging → RESTART from Smoke Part 1
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ PHASE 3: Final Review                       │
│                                             │
│ PR Review (7 categories):                   │
│   1. Code quality                           │
│   2. Test coverage                          │
│   3. Documentation                          │
│   4. Error handling                         │
│   5. Performance                            │
│   6. Security                               │
│   7. Maintainability                        │
│                                             │
│ Lessons Learned:                            │
│   - Update lessons_learned.md               │
│   - Document what worked/didn't             │
│                                             │
│ Zero Tech Debt Tolerance:                   │
│   - Fix ALL issues immediately              │
│   - No deferrals allowed                    │
│ Time: 15-30 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [Final review PASSED?]
    ├─ NO → Fix issues → RESTART from Smoke Part 1
    └─ YES → Stage 5c complete!
         ↓
    [More features remaining?]
    ├─ YES → Stage 5d (Alignment)
    └─ NO → Stage 9 (Epic QC)
```

---

## Stage 9: Epic-Level Final QC

```
Epic-Level Final QC - Testing Entire Epic
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entry: ALL features complete (Stage 5c passed for all)
         ↓
┌─────────────────────────────────────────────┐
│ S9.P1: Epic Smoke Testing                │
│                                             │
│ Part 1: Import Test (all features)          │
│ Part 2: Entry Point Test (cross-feature)    │
│ Part 3: E2E Epic Workflow (MANDATORY GATE)  │
│ Part 4: Cross-Feature Integration           │
│   - Feature interactions verified           │
│   - Integration points tested               │
│   - Epic-level workflows work               │
│ Time: 30-45 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [Epic smoke testing PASSED?]
    ├─ NO → Debugging → RESTART S9.P1
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ S9.P2: Epic QC Rounds                    │
│                                             │
│ Round 1: Epic Algorithm Verification        │
│   - Epic requirements vs implementation     │
│   - Cross-feature cohesion                  │
│                                             │
│ Round 2: Epic Consistency & Standards       │
│   - Consistent patterns across features     │
│   - Architectural consistency               │
│                                             │
│ Round 3: Epic Integration & Success Criteria│
│   - Epic success criteria met               │
│   - Integration points verified             │
│   - Validate against epic request           │
│ Time: 45-60 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [All 3 epic QC rounds PASSED?]
    ├─ NO → Debugging → RESTART S9.P1
    └─ YES → Proceed
         ↓
┌─────────────────────────────────────────────┐
│ S9.P3: Epic Final Review                 │
│                                             │
│ Epic PR Review:                             │
│   - Review all feature changes together     │
│   - Architectural consistency               │
│   - Integration point quality               │
│                                             │
│ Epic Lessons Learned:                       │
│   - Update epic_lessons_learned.md          │
│   - Cross-feature insights                  │
│                                             │
│ Validate Against Epic Request:              │
│   - Re-read original epic notes             │
│   - Verify ALL outcomes delivered           │
│ Time: 30-45 minutes                         │
└─────────────────────────────────────────────┘
         ↓
    [Epic final review PASSED?]
    ├─ NO → Debugging → RESTART S9.P1
    └─ YES → Stage 10 (Epic Cleanup)
```

---

## Debugging Loop-Back Flow

```
Debugging Protocol - Integrated Loop-Back Mechanism
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issues discovered during Testing (Stage 5c or 6)
         ↓
┌─────────────────────────────────────────────┐
│ PHASE 1: Issue Discovery & Checklist Update │
│                                             │
│ - Create/update debugging/ISSUES_CHECKLIST.md│
│ - Add ALL discovered issues                 │
│ - Categorize: 🔴 CRITICAL, 🟡 MAJOR, 🟢 MINOR│
│ - Create issue_{number}_{name}.md per issue │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ PHASE 2: Investigation Rounds (per issue)   │
│                                             │
│ Round 1: Code Tracing                       │
│   - Identify suspicious areas               │
│   - Map data flow                           │
│                                             │
│ Round 2: Hypothesis Formation               │
│   - Max 3 testable hypotheses               │
│   - Rank by likelihood                      │
│                                             │
│ Round 3: Diagnostic Testing                 │
│   - Confirm root cause                      │
│   - Reproduce bug reliably                  │
│                                             │
│ [Max 5 rounds before user escalation]       │
│ [Max 2 hours per round]                     │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ PHASE 3: Root Cause Analysis                │
│                                             │
│ - Document confirmed root cause             │
│ - Identify why issue wasn't caught earlier  │
│ - Plan fix approach                         │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ PHASE 4: Fix Implementation                 │
│                                             │
│ - Implement fix                             │
│ - Update tests (prevent regression)         │
│ - Document in debugging/code_changes.md     │
│ - Run ALL tests (100% pass required)        │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ PHASE 5: User Verification                  │
│                                             │
│ - Present before/after state                │
│ - User confirms issue resolved              │
│ - Update ISSUES_CHECKLIST.md (mark 🟢 FIXED)│
└─────────────────────────────────────────────┘
         ↓
    [All issues in checklist resolved?]
    ├─ NO → PHASE 2 for next issue
    └─ YES → LOOP BACK to testing stage
         ↓
    [Feature debugging?]
    ├─ YES → RESTART S7.P1
    └─ NO → RESTART S9.P1 (Epic Smoke Testing)
         ↓
    [Testing passes with ZERO new issues?]
    ├─ NO → New issues found → PHASE 1 (restart debugging)
    └─ YES → Proceed to next stage
```

---

## Missed Requirement Workflow

```
Missed Requirement - Known Solution Path
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QC/Smoke finds missing requirement (solution known)
         ↓
    [Is root cause unknown?]
    ├─ YES → Use Debugging Protocol instead
    └─ NO → Proceed with Missed Requirement Workflow
         ↓
┌─────────────────────────────────────────────┐
│ STEP 1: Requirement Analysis                │
│                                             │
│ - Read spec.md completely                   │
│ - Identify what's missing                   │
│ - Determine if it SHOULD have been in spec  │
└─────────────────────────────────────────────┘
         ↓
    [Was requirement in spec?]
    ├─ YES → Implementation bug (use debugging)
    └─ NO → True missed requirement
         ↓
┌─────────────────────────────────────────────┐
│ STEP 2: Impact Assessment                   │
│                                             │
│ Impact on spec.md:                          │
│   - Document what needs to be added         │
│   - Estimate complexity (trivial/minor/major)│
│                                             │
│ Impact on implementation_plan.md:           │
│   - Count tasks that need adding            │
│   - Estimate effort                         │
│                                             │
│ Decision threshold:                         │
│   - ≤3 tasks → Add directly, proceed        │
│   - >3 tasks → Return to Stage 5a Round 3   │
└─────────────────────────────────────────────┘
         ↓
    [Task count threshold]
    ├─ ≤3 tasks → Simple addition
    └─ >3 tasks → Return to Stage 5a Round 3
         ↓
┌─────────────────────────────────────────────┐
│ STEP 3a: Simple Addition (≤3 tasks)         │
│                                             │
│ - Update spec.md with requirement           │
│ - Add tasks to implementation_plan.md       │
│ - Update implementation_checklist.md        │
│ - Implement immediately                     │
│ - Update code_changes.md                    │
└─────────────────────────────────────────────┘
         ↓
         │ RESTART S7.P1
         │ or RESTART S9.P1 (Epic Smoke Testing)
         ↓
┌─────────────────────────────────────────────┐
│ STEP 3b: Major Addition (>3 tasks)          │
│                                             │
│ - Return to Stage 5a Round 3 Part 1         │
│ - Re-run preparation iterations (17-22)     │
│ - Re-run gates (23a, 25, 24)                │
│ - Get new GO decision                       │
│ - Then proceed to Stage 5b                  │
└─────────────────────────────────────────────┘
         ↓
         │ Complete full implementation cycle
         │ (5b → 5c → [5d] → [5e])
         ↓
    [Feature level?]
    ├─ YES → Continue with Stage 5d/5e if needed
    └─ NO → Stage 9 (Epic testing)
```

---

## Decision Point: Skip 5d/5e?

```
After Stage 5c Complete - Decision Tree
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stage 5c complete (feature validated)
         ↓
    ┌──────────────────────────────────┐
    │ Are there more features          │
    │ remaining to implement?          │
    └──────────────────────────────────┘
         ↓
    ├─ YES ─────────────────────────────┐
    │                                   │
    │   Proceed to Stage 5d             │
    │   (Post-Feature Alignment)        │
    │         ↓                         │
    │   Update remaining feature specs  │
    │   based on ACTUAL implementation  │
    │         ↓                         │
    │   Proceed to Stage 5e             │
    │   (Testing Plan Update)           │
    │         ↓                         │
    │   Update epic_smoke_test_plan.md  │
    │   with integration points         │
    │         ↓                         │
    │   Next feature's Stage 5a         │
    │   (TODO Creation)                 │
    │                                   │
    └───────────────────────────────────┘
         ↓
    └─ NO ──────────────────────────────┐
    │                                   │
    │   SKIP Stages 5d and 5e           │
    │         ↓                         │
    │   Why skip?                       │
    │   - No remaining specs to update  │
    │   - Test plan will be validated   │
    │     in Stage 9 anyway             │
    │   - No point in intermediate      │
    │     updates                       │
    │         ↓                         │
    │   Proceed directly to Stage 9     │
    │   (Epic-Level Final QC)           │
    │                                   │
    └───────────────────────────────────┘
```

---

## Restart Protocols

```
When to Restart - Complete Decision Matrix
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌────────────────────────────────────────────────────────┐
│ SCENARIO 1: Issues During Smoke Testing (Stage 5c)    │
├────────────────────────────────────────────────────────┤
│ Issue found in:                                        │
│   - Part 1 (Import Test)                               │
│   - Part 2 (Entry Point Test)                          │
│   - Part 3 (E2E Test)                                  │
│                                                        │
│ Action:                                                │
│   1. Enter Debugging Protocol                          │
│   2. Resolve ALL issues in checklist                   │
│   3. RESTART from S10.P1 Step 1 (Import Test)       │
│   4. Re-run ALL 3 parts of smoke testing               │
│   5. Only proceed to QC rounds if smoke passes         │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ SCENARIO 2: Issues During QC Rounds (Stage 5c)        │
├────────────────────────────────────────────────────────┤
│ Issue found in:                                        │
│   - Round 1 (Algorithm Verification)                   │
│   - Round 2 (Consistency & Standards)                  │
│   - Round 3 (Integration & Edge Cases)                 │
│                                                        │
│ Action:                                                │
│   1. Enter Debugging Protocol                          │
│   2. Resolve ALL issues                                │
│   3. RESTART from S10.P1 Step 1 (NOT from QC Round 1)│
│   4. Complete smoke testing → QC rounds again          │
│   5. Zero tolerance for deferring issues               │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ SCENARIO 3: Issues During Epic Testing (Stage 9)      │
├────────────────────────────────────────────────────────┤
│ Issue found in:                                        │
│   - Epic smoke testing (6a)                            │
│   - Epic QC rounds (6b)                                │
│   - Epic final review (6c)                             │
│                                                        │
│ Action:                                                │
│   1. Add to epic-level debugging/ISSUES_CHECKLIST.md   │
│   2. Enter Debugging Protocol                          │
│   3. Resolve ALL issues                                │
│   4. RESTART from S9.P1 Part 1 (Epic Import Test)   │
│   5. Re-run entire Stage 9 (6a → 6b → 6c)              │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ SCENARIO 4: User Testing Failures (Stage 10)           │
├────────────────────────────────────────────────────────┤
│ User finds bugs during testing                         │
│                                                        │
│ Action:                                                │
│   1. Document bugs in epic-level ISSUES_CHECKLIST.md   │
│   2. Enter Debugging Protocol                          │
│   3. Resolve ALL issues with user confirmation         │
│   4. RESTART from S9.P1 (not Stage 10)               │
│   5. Complete full Stage 9 validation again            │
│   6. Return to Stage 10 user testing                    │
│   7. ZERO bugs required to proceed                     │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ SCENARIO 5: Iteration 24 = NO-GO (Stage 5a)           │
├────────────────────────────────────────────────────────┤
│ GO/NO-GO decision fails                                │
│                                                        │
│ Action:                                                │
│   1. Review failure reasons                            │
│   2. Determine which iteration to return to:           │
│      - Gate 4a failed → Return to Round 1              │
│      - Gate 23a failed → Return to Round 3 Part 2a     │
│      - Gate 25 failed → Fix spec, return to Gate 25    │
│      - Readiness check failed → Return to Round 3 Part 1│
│   3. Complete remaining iterations                     │
│   4. Re-run ALL gates                                  │
│   5. Make GO decision again                            │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ SCENARIO 6: Missed Requirement >3 Tasks                │
├────────────────────────────────────────────────────────┤
│ Significant requirement missed (>3 tasks needed)       │
│                                                        │
│ Action:                                                │
│   1. Update spec.md with missed requirement            │
│   2. Return to Stage 5a Round 3 Part 1 (Iteration 17)  │
│   3. Complete preparation iterations (17-22)           │
│   4. Re-run ALL gates (23a, 25, 24)                    │
│   5. Get new GO decision                               │
│   6. Proceed to Stage 5b with updated plan             │
│   7. Complete full cycle (5b → 5c → [5d] → [5e])      │
└────────────────────────────────────────────────────────┘
```

---

## Quick Reference Legend

**Symbols Used:**
- `┌─┐ │ └─┘` - Box drawing characters for stages/phases
- `→ ↓` - Flow direction
- `├─ └─` - Decision tree branches
- `[Question?]` - Decision points
- `✅` - Completion marker
- `🔴 🟡 🟢` - Issue severity (Critical, Major, Minor)

**Time Estimates:**
- Listed in stage boxes as "Time: X-Y minutes/hours"
- Estimates are per feature for Stage 5 workflows
- Epic-level times assume 3-5 features

**Mandatory Gates:**
- Iteration 4a: TODO Specification Audit (Stage 5a Round 1)
- Iteration 23a: Pre-Implementation Spec Audit - 4 PARTS (Stage 5a Round 3)
- Iteration 25: Spec Validation Against Validated Documents (Stage 5a Round 3)
- Iteration 24: Implementation Readiness Protocol - GO/NO-GO (Stage 5a Round 3)
- Smoke Testing Part 3: E2E Execution Test (Stage 5c, S9.P1)
- User Testing: Zero bugs required (Stage 10)

**Key Principles:**
- **Loop-back on issues:** Never proceed with unresolved issues
- **Zero tech debt tolerance:** Fix all issues immediately
- **100% test pass required:** Before stage transitions
- **User approval required:** For specs (Stage 3), testing (Stage 10)
- **Restart from beginning:** When issues found in QC/smoke testing

---

**Last Updated:** 2026-01-04
**See Also:**
- EPIC_WORKFLOW_USAGE.md - Comprehensive usage guide
- README.md - Complete guide index
- prompts_reference_v2.md - Phase transition prompts
