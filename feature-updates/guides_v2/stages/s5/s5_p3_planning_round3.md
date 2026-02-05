# S5: Feature Implementation
## S5.P1: Implementation Planning
### S5.P3: Planning Round 3 (Router)

**File:** `s5_p3_planning_round3.md`

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

**What is this guide?**
Planning Round 3 Part 1 (Preparation) is the first half of Planning Round 3, where you prepare for implementation by defining phasing, rollback strategies, final algorithm traceability, performance optimizations, mock audits, and output validation through 6 systematic iterations (14-19).

**When do you use this guide?**
- Planning Round 2 (STAGE_5ab) complete
- Confidence level >= MEDIUM
- Test coverage >90%
- Ready to prepare for implementation

**Key Outputs:**
- ✅ Implementation phasing plan (4-6 phases with checkpoints)
- ✅ Rollback strategy documented (3 options)
- ✅ Final Algorithm Traceability Matrix (40+ mappings, 100% coverage)
- ✅ Performance analysis and optimizations (if regression >20%)
- ✅ Mock audit complete (all mocks verified against real interfaces)
- ✅ Integration test plan (at least 3 real-object tests)
- ✅ Output consumer validation (roundtrip tests planned)

**Time Estimate:**
45-60 minutes (6 iterations)

**Exit Condition:**
Part 1 is complete when all 6 iterations pass, all preparation outputs added to implementation_plan.md, and you're ready to proceed to Part 2 (Final Gates)

---

## Quick Navigation

**Planning Round 3 is split into 3 parts:**

| Part | Guide to Read | Iterations | Time Estimate |
|------|---------------|------------|---------------|
| S5.P3.1: Preparation | `stages/s5/s5_p3_i1_preparation.md` | 14-19 | 45-60 min |
| S5.P3.2: Gate 23a | `stages/s5/s5_p3_i2_gates_part1.md` | 20 (Gate 23a) | 30-45 min |
| S5.P3.3: Gates 24, 25 | `stages/s5/s5_p3_i3_gates_part2.md` | 21, 22 (Gates 25, 24) | 15-30 min |

**Total Time:** 90-135 minutes (9 iterations + 3 gates)


## Navigation - Iteration Guides

**This is a ROUTER guide.** Detailed iteration instructions are in separate files:

**Iterations 17-18: Phasing & Rollback**
📖 **READ:** `stages/s5/s5_p3_i1_preparation.md`
- Iteration 17: Implementation Phasing
- Iteration 18: Rollback Strategy

**Iterations 19-20: Algorithm Traceability & Performance**
📖 **READ:** `stages/s5/s5_p3_i1_preparation.md`
- Iteration 19: Final Algorithm Traceability Matrix
- Iteration 20: Performance Analysis

**Iterations 21-22: Mock Audit & Output Validation**
📖 **READ:** `stages/s5/s5_p3_i1_preparation.md`
- Iteration 21: Mock Audit
- Iteration 22: Output Consumer Validation

---

## Workflow Overview

```text
┌──────────────────────────────────────────────────────────────┐
│       ROUND 3 PART 1: Preparation (Iterations 14-19)         │
│                    (6 Iterations)                             │
└──────────────────────────────────────────────────────────────┘

Iterations 17-18: Phasing & Rollback
   ↓
Iterations 19-20: Algorithm Traceability & Performance
   ↓
Iterations 21-22: Mock Audit & Output Validation
   ↓
PART 1 COMPLETE
   ↓
Transition to Part 2 (Read stages/s5/s5_p3_i3_gates_part2.md)
```

---

## Critical Rules for Part 1

```text
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - Part 1 (Preparation Iterations)            │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 6 iterations in Part 1 are MANDATORY (no skipping)
   - Iterations 14-19 prepare for implementation
   - Skipping iterations causes implementation failures

2. ⚠️ Implementation Phasing (Iteration 17) prevents "big bang" failures
   - Must define phases with clear checkpoints
   - Cannot implement everything at once
   - Each phase must have test validation

3. ⚠️ Algorithm Traceability (Iteration 19) is FINAL verification
   - Last chance to catch missing algorithm mappings
   - Typical: 40+ mappings (spec + error handling + edge cases)
   - ALL spec algorithms must be traced to implementation_plan.md tasks

4. ⚠️ Mock Audit (Iteration 21) prevents interface mismatch bugs
   - MUST verify EACH mock matches real interface
   - Read actual source code (don't assume)
   - Plan at least 3 integration tests with REAL objects

5. ⚠️ Performance considerations (Iteration 20) identify bottlenecks early
   - Estimate performance impact
   - Identify O(n²) algorithms
   - Add optimization tasks if >20% regression expected

6. ⚠️ Update feature README.md Agent Status after each iteration
   - Document progress: "Iteration X/24 (Planning Round 3) complete"
   - Document next action: "Iteration Y - {Name}"

7. ⚠️ Do NOT proceed to Part 2 without completing ALL 6 iterations
   - Part 2 requires these preparation outputs
   - Missing preparation causes gate failures
```

---

## Prerequisites

**Before starting Part 1, verify ALL of these are true:**

### From Planning Round 2 (STAGE_5ab)
- [ ] Planning Round 2 complete (all 9 iterations 8-13)
- [ ] Test strategy comprehensive and complete
- [ ] Edge cases enumerated and handled
- [ ] Algorithm Traceability Matrix updated (Planning Round 2)
- [ ] E2E Data Flow updated (Planning Round 2)
- [ ] Integration Gap Check updated (Planning Round 2)
- [ ] Test coverage: >90%
- [ ] Documentation plan created

### Confidence & Blockers
- [ ] Confidence level: >= MEDIUM (from Planning Round 2 checkpoint)
- [ ] No blockers in feature README.md Agent Status
- [ ] No unresolved questions in questions.md

### File Access
- [ ] implementation_plan.md v2.0 exists and accessible
- [ ] spec.md complete and validated (Planning Round 2)
- [ ] tests/ folder accessible

**If ANY prerequisite not met:**
- STOP - Do not proceed with Part 1
- Return to Planning Round 2 (STAGE_5ab) to complete prerequisites
- Document blocker in Agent Status

---

## ROUND 3 PART 1: Iteration Details

### Iterations 17-18: Implementation Phasing & Rollback

**📖 READ:** `stages/s5/s5_p3_i1_preparation.md`

**Covers:**
- **Iteration 17:** Implementation Phasing - Break implementation into phases with checkpoints
- **Iteration 18:** Rollback Strategy - Define how to rollback if critical issues found

**Key Outputs:**
- Implementation phasing plan with 4-6 phases added to implementation_plan.md
- Rollback strategy documented (3 options: config toggle, git revert, code disable)
- Rollback test task added

**Why this matters:** "Big bang" integration causes failures. Phasing enables incremental validation.

---

### Iterations 19-20: Algorithm Traceability & Performance

**📖 READ:** `stages/s5/s5_p3_i1_preparation.md`

**Covers:**
- **Iteration 19:** Algorithm Traceability Matrix (Final) - LAST chance to catch missing mappings
- **Iteration 20:** Performance Considerations - Assess impact and identify optimizations

**Key Outputs:**
- Final Algorithm Traceability Matrix section added (40+ mappings, 100% coverage)
- Performance analysis complete
- Optimization tasks added if regression >20%

**⚠️ CRITICAL:** Iteration 19 is final algorithm verification before implementation begins.

---

### Iterations 21-22: Mock Audit & Output Validation

**📖 READ:** `stages/s5/s5_p3_i1_preparation.md`

**Covers:**
- **Iteration 21:** Mock Audit & Integration Test Plan (CRITICAL) - Verify mocks match real interfaces
- **Iteration 22:** Output Consumer Validation - Verify outputs consumable downstream

**Key Outputs:**
- Mock audit report (all mocks verified against real source code)
- Integration test plan (at least 3 real-object tests, NO mocks)
- Output consumer validation plan (roundtrip tests for 3+ consumers)

**⚠️ CRITICAL:** Unit tests with wrong mocks can pass while hiding interface mismatch bugs.

---

## Part 1 Completion Criteria

**Part 1 is COMPLETE when ALL of these are true:**

### All 6 Iterations Complete
- [ ] Iteration 17: Implementation Phasing plan created
- [ ] Iteration 18: Rollback Strategy documented
- [ ] Iteration 19: Algorithm Traceability Matrix final (40+ mappings)
- [ ] Iteration 20: Performance assessment complete, optimizations planned
- [ ] Iteration 21: Mock audit complete, integration tests planned
- [ ] Iteration 22: Output consumer validation planned

### Documentation Updated
- [ ] implementation_plan.md contains "Implementation Phasing" section
- [ ] implementation_plan.md contains "Rollback Strategy" section (or separate section)
- [ ] implementation_plan.md "Algorithm Traceability Matrix" section updated (final)
- [ ] implementation_plan.md contains "Performance Considerations" section
- [ ] implementation_plan.md contains "Mock Audit" section
- [ ] implementation_plan.md "Implementation Tasks" includes integration tests (at least 3)
- [ ] implementation_plan.md "Implementation Tasks" includes consumer validation tasks

### Agent Status Updated
- [ ] feature README.md Agent Status shows: "Part 1 complete, ready for Part 2"
- [ ] Progress documented: "Iteration 22/24 (Planning Round 3 Part 1) complete"
- [ ] Next action set: "Read stages/s5/s5_p3_i3_gates_part2.md"

**If ALL items checked:**
- Part 1 is COMPLETE
- Proceed to Part 2 (Final Gates)
- Read stages/s5/s5_p3_i3_gates_part2.md

**If ANY item unchecked:**
- STOP - Do not proceed to Part 2
- Complete missing iterations
- Re-verify completion criteria

---

## Common Mistakes to Avoid

### ❌ MISTAKE 1: "Skipping Implementation Phasing (Iteration 17)"

**Why this is wrong:**
- "Big bang" integration (all at once) causes failures
- No incremental validation checkpoints
- Hard to debug when everything fails

**What to do instead:**
- ✅ Define 4-6 logical phases
- ✅ Add checkpoint validation after each step
- ✅ Document phasing in implementation_plan.md

---

### ❌ MISTAKE 2: "Not verifying mocks against real interfaces (Iteration 21)"

**Why this is wrong:**
- Mocks that don't match real interfaces → Tests pass but code fails
- Interface changes not caught by tests
- False sense of security

**What to do instead:**
- ✅ Read ACTUAL source code for each mocked dependency
- ✅ Verify parameter types match
- ✅ Verify return types match
- ✅ Fix mock mismatches immediately

**Example:**
```text
BAD: Assume mock is correct
GOOD: Read utils/csv_utils.py:45, verify signature matches mock
```

---

### ❌ MISTAKE 3: "Skipping integration tests with real objects"

**Why this is wrong:**
- Only unit tests with mocks → Don't prove feature works
- Interface mismatches not caught
- Integration failures discovered late

**What to do instead:**
- ✅ Plan at least 3 integration tests with REAL objects
- ✅ NO MOCKS in integration tests
- ✅ Test proves feature works in real environment

---

### ❌ MISTAKE 4: "Not optimizing performance bottlenecks (Iteration 20)"

**Why this is wrong:**
- Performance regression >20% → User complaints
- Optimization post-implementation harder
- May require architectural changes

**What to do instead:**
- ✅ Estimate performance impact
- ✅ Identify O(n²) algorithms
- ✅ Plan optimizations if regression >20%
- ✅ Add optimization tasks to implementation_plan.md

**Example:**
```text
O(n²) player matching → 5.0s (unacceptable)
O(n) dict lookup → 0.01s (acceptable)
```

---

## Prerequisites for Next Stage

**Before proceeding to Part 2 (stages/s5/s5_p3_i3_gates_part2.md), verify:**

### Part 1 Completion
- [ ] ALL 6 iterations complete (14-19)
- [ ] Implementation phasing defined
- [ ] Rollback strategy documented
- [ ] Algorithm traceability 100%
- [ ] Performance optimized (if needed)
- [ ] Mocks audited and fixed
- [ ] Integration tests planned
- [ ] Output consumers validated

### Documentation
- [ ] implementation_plan.md updated with all Part 1 outputs
- [ ] feature README.md Agent Status shows Part 1 complete

### Readiness
- [ ] No blockers
- [ ] Confidence level still >= MEDIUM
- [ ] Ready for mandatory gates (Part 2)

**Only proceed to Part 2 when ALL items checked.**

**Next stage:** stages/s5/s5_p3_i3_gates_part2.md

---

## Summary

**Planning Round 3 Part 1 - Preparation prepares all prerequisites for implementation:**

**Key Activities:**
1. **Implementation Phasing (Iteration 17):** Break into phases with checkpoints
2. **Rollback Strategy (Iteration 18):** Define how to rollback if needed
3. **Algorithm Traceability (Iteration 19):** Final verification (40+ mappings)
4. **Performance Assessment (Iteration 20):** Identify bottlenecks, optimize
5. **Mock Audit (Iteration 21):** Verify mocks match real interfaces, plan integration tests
6. **Output Consumer Validation (Iteration 22):** Verify outputs consumable downstream

**Critical Outputs:**
- Implementation phasing plan (prevents "big bang" failures)
- Final algorithm traceability (100% coverage)
- Mock audit report (interface mismatches fixed)
- Integration test plan (at least 3 real-object tests)
- Performance optimization plan (if regression >20%)

**Success Criteria:**
- All 6 iterations complete
- No missing algorithm mappings
- All mocks verified
- Integration tests planned
- Ready for mandatory gates (Part 2)

**Next Stage:** stages/s5/s5_p3_i3_gates_part2.md - Final validation and GO/NO-GO decision

**Remember:** Part 1 preparation prevents implementation failures. Thoroughness here saves massive rework later.

---

## See Also

**Iteration Detail Guides:**
- `stages/s5/s5_p3_i1_preparation.md` - Iterations 17-18: Phasing & Rollback
- `stages/s5/s5_p3_i1_preparation.md` - Iterations 19-20: Algorithm Traceability & Performance
- `stages/s5/s5_p3_i1_preparation.md` - Iterations 21-22: Mock Audit & Output Validation

**Related Guides:**
- `stages/s5/s5_p2_planning_round2.md` - Planning Round 2 (prerequisite for Part 1)
- `stages/s5/s5_p3_i3_gates_part2.md` - Part 2: Final Gates (next stage)
- `prompts_reference_v2.md` - Phase transition prompts (MANDATORY)

---

**END OF S5.P3 PART 1 GUIDE**
