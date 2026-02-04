# S4: Feature Testing Strategy - Quick Reference Card

**📚 Full Guides:** `s4_feature_testing_strategy.md`, `s4_test_strategy_development.md`, `s4_validation_loop.md`

---

## Stage Overview

**Purpose:** Test-driven development - plan ALL tests BEFORE implementation
**Structure:** 4 iterations (S4.I1, I2, I3, I4)
**Time:** 45-60 minutes per feature
**Output:** test_strategy.md with >90% coverage
**Prerequisites:** S3 complete (Gate 4.5 passed), spec.md finalized (Gate 3 passed)

---

## Iteration Checklist

### S4.I1: Test Strategy Development (15-20 min)

**Goal:** Create test coverage matrix with unit, integration, edge tests

□ Read spec.md requirements completely
□ For each requirement, identify:
  - Testable behaviors
  - Expected inputs/outputs
  - Error conditions
  - Initial edge cases
□ Create test coverage matrix (requirement → test mapping)
□ Enumerate test cases (unit, integration, edge)
□ Link each test to requirement (traceability)
□ Update README Agent Status

**Output:** Test coverage matrix, test case list, traceability matrix

---

### S4.I2: Edge Case Enumeration (10-15 min)

**Goal:** Systematically identify ALL edge cases

□ For each input, identify boundary values:
  - Min/max values
  - Null/empty/zero
  - Invalid types
  - Special characters
□ Enumerate error paths:
  - Invalid input scenarios
  - Dependency failures
  - Race conditions
  - State conflicts
□ Add boundary tests to test case list
□ Add error path tests to test case list
□ Create edge case catalog
□ Update test coverage matrix
□ Update README Agent Status

**Output:** Edge case catalog, updated test coverage matrix

---

### S4.I3: Configuration Change Impact (10-15 min)

**Goal:** Plan config tests (default, custom, invalid, missing)

□ Identify config files used by feature
□ For each config value, identify:
  - Default behavior
  - Custom value behavior
  - Invalid value behavior (error handling)
  - Missing value behavior (fallback/default)
□ Create config test cases for all scenarios
□ Create configuration test matrix
□ Update test coverage matrix (final)
□ Verify >90% coverage goal met
□ Update README Agent Status

**Output:** Config test matrix, final test coverage matrix

---

### S4.I4: Validation Loop (15-20 min)

**Goal:** Validate test strategy with 3 consecutive clean rounds

**Reference:** `reference/validation_loop_test_strategy.md`

□ **Round 1:** Sequential read + requirement coverage check
  - Every requirement has test coverage?
  - Test descriptions specific (not vague)?
  - Coverage >90%?
  - Edge cases tested?
  - Config scenarios tested?
  - Fix issues → Round 2

□ **Round 2:** Edge case enumeration + gap detection
  - Re-read with fresh eyes (different order)
  - New edge cases discovered?
  - New integration points?
  - Coverage gaps?
  - Fix issues (reset counter) → Round 3

□ **Round 3:** Random spot-checks + integration verification
  - Random spot-check 5 requirements
  - Integration tests comprehensive?
  - Final coverage >90%?
  - If 0 issues → count = 3 → PASSED

□ **Rounds 4+:** If issues found, fix and repeat
  - Continue until 3 consecutive clean rounds
  - Maximum 10 rounds (escalate if exceeded)

□ Create `feature_{N}_{name}/test_strategy.md`
□ Update README Agent Status (S4_COMPLETE)

**Output:** test_strategy.md (validated, >90% coverage)

---

## Exit Criteria

**S4 complete when ALL true:**

□ I1 complete (test coverage matrix created)
□ I2 complete (edge case catalog created)
□ I3 complete (config test matrix created)
□ I4 complete (Validation Loop passed - 3 consecutive clean rounds)
□ test_strategy.md exists in `feature_{N}_{name}/` folder
□ test_strategy.md has all sections (not empty)
□ test_strategy.md shows >90% coverage
□ README Agent Status = S4_COMPLETE

---

## Common Issues

❌ **"I'll plan tests during implementation"**
→ ✅ STOP - S4 is test-DRIVEN (tests guide implementation)

❌ **"80% coverage is good enough"**
→ ✅ STOP - Feature-level goal is >90%

❌ **"One pass is enough"**
→ ✅ STOP - Validation Loop requires 3 consecutive clean rounds

❌ **"Skip edge case/config iterations"**
→ ✅ STOP - All 4 iterations are MANDATORY

---

## Navigation

**Current Stage:** S4 (Feature Testing Strategy)
**Previous:** S3 (Cross-Feature Sanity Check + Gate 4.5)
**Next:** S5 (Implementation Planning - 22 iterations across 3 rounds)

**Start S5:**
1. Use phase transition prompt from `prompts_reference_v2.md`
2. Read `stages/s5/s5_p1_planning_round1.md`
3. S5.P1.I1 will verify test_strategy.md exists (MANDATORY)

---

## Key Rules

1. ⚠️ test-driven development (plan tests BEFORE coding)
2. ⚠️ >90% coverage goal (feature-level)
3. ⚠️ 4 iterations structure (I1, I2, I3, I4 - all MANDATORY)
4. ⚠️ Validation Loop (I4) - 3 consecutive clean rounds required
5. ⚠️ test_strategy.md created in S4, merged in S5.P1.I1
6. ⚠️ Update README Agent Status after EACH iteration
7. ⚠️ Zero deferred issues (fix ALL issues immediately)

---

**📖 For detailed instructions, read the full guides.**

*End of S4 quick reference card*
