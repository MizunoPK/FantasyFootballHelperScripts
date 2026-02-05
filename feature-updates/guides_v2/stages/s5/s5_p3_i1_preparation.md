# S5: Feature Implementation
## S5.P3: Planning Round 3
### S5.P3.I1: Preparation (Iterations 17-22) - Router

**Guide Version:** 2.0
**Last Updated:** 2026-02-05 (Restructured for improved navigation)
**Purpose:** Quick navigation to Iterations 17-22 preparation guides
**Prerequisites:** Round 2 complete (S5.P2)
**Main Guide:** `stages/s5/s5_p3_planning_round3.md`

---

## Purpose

This guide has been split into 6 iteration-specific files for easier navigation and focused reference during S5 Round 3 execution.

**How to Use This Router:**
1. Identify which iteration you're currently executing (17-22)
2. Click the link to the relevant iteration-specific file
3. Complete that iteration following the guide
4. Return here to navigate to the next iteration

**Execute iterations sequentially** - do not skip iterations.

---

## Iteration 17: Implementation Phasing

**File:** [s5_p3_i1_iter17_phasing.md](s5_p3_i1_iter17_phasing.md)

**File Size:** 115 lines

**What's Covered:**
- Break implementation into incremental phases for validation
- Typical phases: Data structures → Core algorithm → Integration → Error handling → Edge cases → Tests
- Document why each phase matters
- Plan testing after each phase

**When to Use:**
- After completing Round 2 (Iterations 8-16)
- When planning incremental implementation approach
- When setting up mini-milestones for validation

**Output:** Implementation phasing plan in implementation_plan.md

---

## Iteration 18: Rollback Strategy

**File:** [s5_p3_i1_iter18_rollback.md](s5_p3_i1_iter18_rollback.md)

**File Size:** 158 lines

**What's Covered:**
- Plan how to undo changes if implementation fails
- Document rollback steps for each phase
- Identify rollback risks
- Plan data migration reversal if needed

**When to Use:**
- After completing Iteration 17
- When planning how to safely back out changes
- When implementing features with data migrations

**Output:** Rollback strategy in implementation_plan.md

---

## Iteration 19: Algorithm Traceability Matrix (Final)

**File:** [s5_p3_i1_iter19_traceability.md](s5_p3_i1_iter19_traceability.md)

**File Size:** 120 lines

**What's Covered:**
- **FINAL** verification of algorithm traceability (first created in Iteration 2)
- Verify ALL algorithms from spec.md have implementation tasks
- Check for orphan algorithms (in spec but not in plan)
- Verify 100% coverage

**When to Use:**
- After completing Iteration 18
- When doing final verification of requirements coverage
- Before Gate 23a (Pre-Implementation Spec Audit)

**Output:** Updated algorithm traceability matrix in implementation_plan.md

---

## Iteration 20: Performance Considerations

**File:** [s5_p3_i1_iter20_performance.md](s5_p3_i1_iter20_performance.md)

**File Size:** 176 lines

**What's Covered:**
- Identify performance-critical sections
- Document expected performance baselines
- Plan performance testing approach
- Identify optimization opportunities

**When to Use:**
- After completing Iteration 19
- When planning performance testing
- When setting performance expectations

**Output:** Performance considerations section in implementation_plan.md

---

## Iteration 21: Mock Audit & Integration Test Plan

**File:** [s5_p3_i1_iter21_mockaudit.md](s5_p3_i1_iter21_mockaudit.md)

**File Size:** 316 lines

**What's Covered:**
- **CRITICAL:** Audit all mocks match REAL interfaces
- Verify mocks created from actual source code (hands-on data inspection)
- Plan integration tests that use real objects (not mocks)
- Document when to use mocks vs real objects

**When to Use:**
- After completing Iteration 20
- When verifying test mocks are accurate
- Before creating integration test plan

**Output:** Mock audit results + integration test plan in implementation_plan.md

**Key Insight:** This iteration prevents "tests pass but code fails" bugs caused by incorrect mocks.

---

## Iteration 22: Output Consumer Validation

**File:** [s5_p3_i1_iter22_consumers.md](s5_p3_i1_iter22_consumers.md)

**File Size:** 220 lines

**What's Covered:**
- Verify outputs match what consumers expect
- Check output format, structure, units
- Validate against consumer interfaces
- Document output contracts

**When to Use:**
- After completing Iteration 21
- When verifying feature outputs are consumable
- Before proceeding to Gate 23a

**Output:** Output validation in implementation_plan.md

---

## Quick Navigation

| Iteration | Focus | File | Lines |
|-----------|-------|------|-------|
| **Iteration 17** | Implementation Phasing | [s5_p3_i1_iter17_phasing.md](s5_p3_i1_iter17_phasing.md) | 115 |
| **Iteration 18** | Rollback Strategy | [s5_p3_i1_iter18_rollback.md](s5_p3_i1_iter18_rollback.md) | 158 |
| **Iteration 19** | Algorithm Traceability (Final) | [s5_p3_i1_iter19_traceability.md](s5_p3_i1_iter19_traceability.md) | 120 |
| **Iteration 20** | Performance Considerations | [s5_p3_i1_iter20_performance.md](s5_p3_i1_iter20_performance.md) | 176 |
| **Iteration 21** | Mock Audit & Integration Tests | [s5_p3_i1_iter21_mockaudit.md](s5_p3_i1_iter21_mockaudit.md) | 316 |
| **Iteration 22** | Output Consumer Validation | [s5_p3_i1_iter22_consumers.md](s5_p3_i1_iter22_consumers.md) | 220 |

**Total Content:** 1,105 lines across 6 iteration-specific files

---

## Completion Criteria

**Iterations 17-22 complete when:**

- [ ] Iteration 17: Implementation phased into incremental steps
- [ ] Iteration 18: Rollback strategy documented
- [ ] Iteration 19: Algorithm traceability matrix finalized (100% coverage)
- [ ] Iteration 20: Performance considerations documented
- [ ] Iteration 21: Mock audit complete, integration test plan created
- [ ] Iteration 22: Output consumer validation complete

**After completing all iterations:**

Proceed to S5.P3.I2 (Gate 23a - Pre-Implementation Spec Audit): `stages/s5/s5_p3_i2_gates_part1.md`

---

## Navigation Back to Main Guide

**Return to:** [stages/s5/s5_p3_planning_round3.md](s5_p3_planning_round3.md)

**See Also:**
- S5.P3.I2: [s5_p3_i2_gates_part1.md](s5_p3_i2_gates_part1.md) - Gate 23a (next)
- S5.P3.I3: [s5_p3_i3_gates_part2.md](s5_p3_i3_gates_part2.md) - Gates 24-25

---

*Preparation iteration guides restructured 2026-02-05 for improved navigation and focused reference.*
