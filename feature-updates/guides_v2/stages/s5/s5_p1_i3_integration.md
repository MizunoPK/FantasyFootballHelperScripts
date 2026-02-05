# S5: Feature Implementation
## S5.P1: Planning Round 1
### S5.P1.I3: Integration (Iterations 5-7) - Router

**Guide Version:** 2.0
**Last Updated:** 2026-02-05 (Restructured for improved navigation)
**Purpose:** Quick navigation to Iterations 5, 5a, 6, 6a, 7, 7a iteration guides
**Prerequisites:** Iterations 1-4 + Gate 4a complete (s5_p1_i2_algorithms.md)
**Main Guide:** `stages/s5/s5_p1_planning_round1.md`

---

## Purpose

This guide has been split into 6 iteration-specific files for easier navigation and focused reference during S5 Round 1 execution.

**How to Use This Router:**
1. Identify which iteration you're currently executing (5, 5a, 6, 6a, 7, or 7a)
2. Click the link to the relevant iteration-specific file
3. Complete that iteration following the guide
4. Return here to navigate to the next iteration

**Execute iterations sequentially** - do not skip iterations.

---

## Iteration 5: End-to-End Data Flow

**File:** [s5_p1_i3_iter5_dataflow.md](s5_p1_i3_iter5_dataflow.md)

**File Size:** 109 lines

**What's Covered:**
- Trace data from entry point through all transformations to output
- Identify entry points (load functions, API calls, user input)
- Document complete data flow step-by-step
- Verify no gaps in data flow
- Identify data transformations at each step

**When to Use:**
- After completing Iteration 4 + Gate 4a
- When verifying data flows correctly through system
- When documenting end-to-end data paths

**Output:** Data flow diagram in implementation_plan.md

---

## Iteration 5a: Downstream Data Consumption Tracing

**File:** [s5_p1_i3_iter5a_downstream.md](s5_p1_i3_iter5a_downstream.md)

**File Size:** 352 lines

**What's Covered:**
- **CRITICAL:** Verify how loaded data is CONSUMED (not just loaded)
- Prevents "data loads successfully but calculation fails" bugs
- Trace consumption paths for EVERY data loading operation
- Document where loaded data is used in calculations
- Identify missing consumption paths

**When to Use:**
- Immediately after Iteration 5
- When verifying data loading operations have consumers
- When preventing catastrophic "silent failure" bugs

**Output:** Consumption tracing table in implementation_plan.md

**Key Insight:** This iteration was added after KAI-1 revealed critical bug pattern - data loaded but never consumed in calculations.

---

## Iteration 6: Error Handling Scenarios

**File:** [s5_p1_i3_iter6_errorhandling.md](s5_p1_i3_iter6_errorhandling.md)

**File Size:** 132 lines

**What's Covered:**
- Enumerate ALL possible error cases for the feature
- Plan error handling strategy for each case
- Document graceful degradation paths
- Identify error messages and logging
- Verify no unhandled exceptions

**When to Use:**
- After completing Iteration 5a
- When planning error handling strategy
- When ensuring graceful degradation

**Output:** Error handling table in implementation_plan.md

---

## Iteration 6a: External Dependency Final Verification

**File:** [s5_p1_i3_iter6a_dependencies.md](s5_p1_i3_iter6a_dependencies.md)

**File Size:** 157 lines

**What's Covered:**
- **NEW:** Final verification of external dependencies before implementation
- Verify API availability, authentication, rate limits
- Document dependency failure modes
- Plan fallback strategies for unavailable dependencies
- Added from KAI-1 lessons learned

**When to Use:**
- After completing Iteration 6
- When feature depends on external APIs, services, or libraries
- When planning for dependency failures

**Output:** Dependency verification table in implementation_plan.md

---

## Iteration 7: Integration Gap Check

**File:** [s5_p1_i3_iter7_integration.md](s5_p1_i3_iter7_integration.md)

**File Size:** 122 lines

**What's Covered:**
- **CRITICAL:** Verify all new methods/functions have identified callers
- Prevents orphan code (code written but never called)
- Check integration points are documented
- Verify no missing integration tasks
- Final verification before Gate 7a

**When to Use:**
- After completing Iteration 6a
- When verifying all code has integration points
- Before executing Gate 7a (Backward Compatibility)

**Output:** Integration verification in implementation_plan.md

---

## Iteration 7a: Backward Compatibility Analysis (Gate 7a)

**File:** [s5_p1_i3_iter7a_compatibility.md](s5_p1_i3_iter7a_compatibility.md)

**File Size:** 323 lines

**What's Covered:**
- **MANDATORY GATE:** Backward compatibility check before Round 2
- Verify new code works with existing data formats
- Check configuration file compatibility
- Verify no breaking changes to existing workflows
- Document migration path if breaking changes required

**When to Use:**
- After completing Iteration 7
- Before proceeding to Round 2 (S5.P2)
- When verifying backward compatibility

**Output:** Compatibility analysis in implementation_plan.md

**This is Gate 7a** - Must pass before proceeding to Round 2.

---

## Quick Navigation

| Iteration | Focus | File | Lines |
|-----------|-------|------|-------|
| **Iteration 5** | End-to-End Data Flow | [s5_p1_i3_iter5_dataflow.md](s5_p1_i3_iter5_dataflow.md) | 109 |
| **Iteration 5a** | Downstream Consumption Tracing | [s5_p1_i3_iter5a_downstream.md](s5_p1_i3_iter5a_downstream.md) | 352 |
| **Iteration 6** | Error Handling Scenarios | [s5_p1_i3_iter6_errorhandling.md](s5_p1_i3_iter6_errorhandling.md) | 132 |
| **Iteration 6a** | External Dependency Verification | [s5_p1_i3_iter6a_dependencies.md](s5_p1_i3_iter6a_dependencies.md) | 157 |
| **Iteration 7** | Integration Gap Check | [s5_p1_i3_iter7_integration.md](s5_p1_i3_iter7_integration.md) | 122 |
| **Iteration 7a** | Backward Compatibility (Gate 7a) | [s5_p1_i3_iter7a_compatibility.md](s5_p1_i3_iter7a_compatibility.md) | 323 |

**Total Content:** 1,195 lines across 6 iteration-specific files

---

## Completion Criteria

**Iterations 5-7 complete when:**

- [ ] Iteration 5: End-to-end data flow documented
- [ ] Iteration 5a: Downstream consumption verified for ALL data loads
- [ ] Iteration 6: Error handling planned for all cases
- [ ] Iteration 6a: External dependencies verified
- [ ] Iteration 7: Integration gaps identified and documented
- [ ] Iteration 7a: Gate 7a PASSED (backward compatibility verified)

**After completing all iterations:**

Proceed to S5.P2 (Round 2): `stages/s5/s5_p2_planning_round2.md`

---

## Navigation Back to Main Guide

**Return to:** [stages/s5/s5_p1_planning_round1.md](s5_p1_planning_round1.md)

**See Also:**
- S5.P1.I1: [s5_p1_i1_requirements.md](s5_p1_i1_requirements.md) - Iterations 1-3
- S5.P1.I2: [s5_p1_i2_algorithms.md](s5_p1_i2_algorithms.md) - Iteration 4 + Gate 4a
- S5.P2: [s5_p2_planning_round2.md](s5_p2_planning_round2.md) - Round 2 (next)

---

*Integration iteration guides restructured 2026-02-05 for improved navigation and focused reference.*
