# S4: Feature Testing Strategy (Router)

🚨 **MANDATORY READING PROTOCOL**

**Before starting this guide:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update feature README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check feature README.md Agent Status for current phase
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Overview

**What is this stage?**
S4 is Feature-Level Test Strategy Development - planning tests BEFORE implementation (test-driven development approach). You will plan unit tests, integration tests, edge cases, and config scenarios with >90% coverage goal.

**When do you use this stage?**
- S3 complete (epic test plan approved - Gate 4.5 passed)
- Feature spec.md finalized and user-approved (Gate 3 passed from S2)
- Ready to plan feature-level tests before implementation

**Key Outputs:**
- ✅ test_strategy.md created with all test categories
- ✅ >90% coverage planned (unit + integration + edge + config tests)
- ✅ Traceability matrix (each test links to requirement)
- ✅ Edge case catalog complete
- ✅ Configuration test matrix complete
- ✅ Ready for S5 (Implementation Planning)

**Time Estimate:**
45-60 minutes per feature

**Exit Condition:**
S4 is complete when test_strategy.md exists with >90% coverage planned, all edge cases identified, config tests defined, and Validation Loop validation passed with 3 consecutive clean rounds

---

## Critical Rules

```text
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ S3 (epic test plan approval) MUST be complete before S4
   - Gate 4.5 must have passed
   - Cannot plan feature tests without epic context

2. ⚠️ test-driven development approach
   - Plan tests BEFORE writing implementation
   - Tests guide implementation structure
   - >90% coverage goal required

3. ⚠️ test_strategy.md created in S4, merged in S5.P1.I1
   - S4 creates separate file (implementation_plan.md doesn't exist yet)
   - S5.P1 Iteration 1 merges test strategy into implementation plan
   - Validate test_strategy.md exists before starting S5

4. ⚠️ 4 Iterations structure (S4.I1, S4.I2, S4.I3, S4.I4)
   - Iteration 1: Test Strategy Development (15-20 min)
   - Iteration 2: Edge Case Enumeration (10-15 min)
   - Iteration 3: Configuration Change Impact (10-15 min)
   - Iteration 4: Validation Loop (15-20 min)

5. ⚠️ Traceability required
   - Each test must link to requirement in spec.md
   - Coverage matrix shows requirement → test mapping
   - No untested requirements allowed

6. ⚠️ Validation Loop validation mandatory (Iteration 4)
   - Reference: validation_loop_test_strategy.md
   - 3 consecutive clean rounds required
   - Exit only when ZERO issues remain

7. ⚠️ Update feature README.md Agent Status at each iteration
   - After Iteration 1, 2, 3, 4 completion
   - Proves progress, enables resumption after compaction
```

---

## Prerequisites Checklist

**Verify BEFORE starting S4:**

- [ ] S3 (Cross-Feature Sanity Check) complete
- [ ] Epic test plan approved by user (Gate 4.5 passed)
- [ ] Feature spec.md finalized and user-approved (Gate 3 passed from S2)
- [ ] Have read feature spec.md to understand:
  - All requirements and acceptance criteria
  - Expected inputs and outputs
  - Integration points with other features
  - Configuration dependencies

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with S4
- Complete missing prerequisites
- Document blocker in Agent Status

---

## Stage Structure

**S4 has 4 iterations (NO PHASES):**

```text
S4: Feature Testing Strategy
├── S4.I1 - Test Strategy Development (s4_test_strategy_development.md)
├── S4.I2 - Edge Case Enumeration (s4_test_strategy_development.md)
├── S4.I3 - Configuration Change Impact (s4_test_strategy_development.md)
└── S4.I4 - Validation Loop Validation (s4_validation_loop.md)
```

**Router Logic:**

**Execute S4.I1, I2, I3 sequentially:**
- READ: `stages/s4/s4_test_strategy_development.md`
- Follow iterations 1, 2, 3 in order
- Output: Test coverage matrix (draft), test case list, edge case catalog, config test matrix

**Execute S4.I4:**
- READ: `stages/s4/s4_validation_loop.md`
- Validate test strategy with Validation Loop
- Reference: `reference/validation_loop_test_strategy.md`
- Exit when 3 consecutive clean rounds achieved

**After S4.I4 completes:**
- Create `feature_{N}_{name}/test_strategy.md` with all outputs
- Mark S4 complete in feature README.md
- Transition to S5 (Implementation Planning)

---

## Workflow Overview

```text
┌──────────────────────────────────────────────────────────────┐
│                    STAGE 4 WORKFLOW                          │
└──────────────────────────────────────────────────────────────┘

Iteration 1: Test Strategy Development (15-20 min)
   ├─ Requirement coverage analysis
   ├─ Test case enumeration (unit, integration, edge)
   └─ Create test coverage matrix (draft)

Iteration 2: Edge Case Enumeration (10-15 min)
   ├─ Boundary conditions identification
   ├─ Error path enumeration
   └─ Update test coverage matrix

Iteration 3: Configuration Change Impact (10-15 min)
   ├─ Configuration dependency analysis
   ├─ Configuration test cases
   └─ Configuration test matrix

Iteration 4: Validation Loop (15-20 min)
   ├─ Reference: validation_loop_test_strategy.md
   ├─ Round 1: Sequential read + requirement coverage check
   ├─ Round 2: Edge case enumeration + gap detection
   ├─ Round 3: Random spot-checks + integration verification
   └─ Exit: 3 consecutive clean rounds

Output: Create test_strategy.md
   ├─ All test categories (unit, integration, edge, config)
   ├─ Representative test cases
   ├─ Coverage goal (>90%)
   ├─ Traceability matrix
   ├─ Edge case catalog
   └─ Configuration test matrix
```

---

## Navigation

**Current Guide:** `stages/s4/s4_feature_testing_strategy.md` (router)

**Next Actions:**
1. READ: `stages/s4/s4_test_strategy_development.md` (Iterations 1-3)
2. Execute Iterations 1, 2, 3 sequentially
3. READ: `stages/s4/s4_validation_loop.md` (Iteration 4)
4. Execute Iteration 4 (Validation Loop)
5. Create test_strategy.md file
6. Mark S4 complete
7. Transition to S5

**Quick Reference:**
- See: `stages/s4/s4_feature_testing_card.md` for condensed checklist

---

## Exit Criteria

**S4 is complete when ALL of these are true:**

- [ ] Iterations 1, 2, 3 complete (test strategy developed)
- [ ] Iteration 4 complete (Validation Loop passed with 3 consecutive clean rounds)
- [ ] test_strategy.md created in `feature_{N}_{name}/` folder with:
  - All test categories (unit, integration, edge, config)
  - Representative test cases for each requirement
  - Coverage goal >90%
  - Traceability matrix (requirement → test mapping)
  - Edge case catalog (boundary conditions, error paths)
  - Configuration test matrix (default, custom, invalid, missing)
- [ ] Feature README.md updated:
  - Agent Status: Current Phase = S5_READY
  - S4 completion marked with timestamp

**If any item unchecked:**
- ❌ S4 is NOT complete
- ❌ Do NOT proceed to S5
- Complete missing items first

---

## Common Mistakes to Avoid

```text
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "I'll plan tests during implementation"
   ✅ STOP - S4 is test-DRIVEN development (tests guide implementation)

❌ "I'll just list test names, no details needed"
   ✅ STOP - Must link each test to requirement (traceability)

❌ "80% coverage is good enough"
   ✅ STOP - Feature-level goal is >90% coverage

❌ "Edge cases can wait until S7 (testing)"
   ✅ STOP - Edge cases MUST be identified in S4 (plan ALL tests upfront)

❌ "Config tests aren't needed for this feature"
   ✅ STOP - Iteration 3 is MANDATORY (identify config dependencies)

❌ "One pass through test strategy is enough"
   ✅ STOP - Validation Loop (I4) requires 3 consecutive clean rounds

❌ "I'll merge test strategy into implementation_plan.md now"
   ✅ STOP - Create separate test_strategy.md (S5.P1.I1 merges it)

❌ "Let me skip to implementation"
   ✅ STOP - S5 (Implementation Planning) comes next (not S6 execution)
```

---

## README Agent Status Update Requirements

**Update feature README.md Agent Status at these points:**

1. ⚡ After starting S4 (before Iteration 1)
2. ⚡ After Iteration 1 complete (test strategy drafted)
3. ⚡ After Iteration 2 complete (edge cases identified)
4. ⚡ After Iteration 3 complete (config tests defined)
5. ⚡ After Iteration 4 complete (Validation Loop passed)
6. ⚡ After test_strategy.md created
7. ⚡ After marking S4 complete

---

## Prerequisites for S5

**Before transitioning to S5, verify:**

- [ ] S4 completion criteria ALL met
- [ ] test_strategy.md exists in `feature_{N}_{name}/` folder
- [ ] test_strategy.md has all required sections (not empty/placeholder)
- [ ] test_strategy.md shows >90% coverage goal
- [ ] Validation Loop passed (documented in test_strategy.md)
- [ ] Feature README.md shows:
  - Agent Status: Current Phase = S5_READY
  - S4 completion timestamp

**If any prerequisite fails:**
- ❌ Do NOT transition to S5
- Complete missing prerequisites
- S5 will verify test_strategy.md exists and escalate if missing

---

## Next Stage

**After completing S4:**

**READ:** `stages/s5/s5_v2_validation_loop.md`
**GOAL:** Create comprehensive implementation plan using 2-phase validation loop approach
**ESTIMATE:** 4.5-7 hours per feature (Phase 1: 60-90 min draft + Phase 2: 3.5-6 hours validation)

**S5 v2 will:**
- Verify test_strategy.md exists (from S4)
- Create draft implementation_plan.md with all 11 dimension sections
- Run validation loop until 3 consecutive clean rounds achieved
- Reference test strategy for test coverage requirements

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S5.

---

*End of stages/s4/s4_feature_testing_strategy.md*
