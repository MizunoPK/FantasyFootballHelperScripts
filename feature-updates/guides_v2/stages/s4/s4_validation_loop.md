# S4.I4: Validation Loop (Test Strategy Validation)

🚨 **MANDATORY READING PROTOCOL**

**Before starting this iteration:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Verify Iterations 1-3 complete (test strategy, edge cases, config tests planned)
3. Read reference guide: `reference/validation_loop_test_strategy.md`
4. Update feature README.md Agent Status with guide name + timestamp

---

## Quick Start

**What is this iteration?**
S4.I4 validates test strategy completeness using Validation Loop protocol with 3 consecutive clean rounds.

**When do you use this iteration?**
After completing S4.I1, I2, I3 (test coverage matrix, edge cases, config tests all planned)

**Key Outputs:**
- ✅ Test strategy validated (3 consecutive clean rounds)
- ✅ test_strategy.md created in feature folder
- ✅ Ready for S5 (Implementation Planning)

**Time Estimate:**
15-20 minutes

---

## Purpose

Validate test strategy completeness using systematic Validation Loop validation from `validation_loop_test_strategy.md`.

**Reference:** `feature-updates/guides_v2/reference/validation_loop_test_strategy.md`

---

## Prerequisites

□ S4.I1 complete (test coverage matrix created)
□ S4.I2 complete (edge case catalog created)
□ S4.I3 complete (config test matrix created)
□ Test coverage >90% (from I1-I3)
□ Traceability matrix shows 100% requirement coverage

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed to I4
- Complete missing iterations first

---

## Validation Loop Process

**Follow master protocol:** `validation_loop_protocol.md`
**Context-specific guide:** `validation_loop_test_strategy.md`

**Exit Criteria:** 3 consecutive rounds with ZERO issues found

---

## Round 1: Sequential Read + Requirement Coverage Check (5-10 min)

**Pattern:** Read test plan top to bottom, check requirement coverage

**Process:**

1. **Re-read test coverage matrix** (from I1-I3)
2. **Re-read feature spec.md requirements section** with fresh eyes
3. **Check each requirement:**
   - Does this requirement have test coverage?
   - Are tests sufficient (happy path + edge cases + errors)?
   - Is coverage >90% for this requirement?
4. **Check test descriptions:**
   - Are they specific? (not vague like "test login works")
   - Do they have concrete pass/fail criteria?
   - Do they link to requirements?
5. **Document ALL issues found**

**Round 1 Checklist:**

- [ ] Every requirement in spec.md has test coverage
- [ ] All test descriptions are specific and measurable
- [ ] No vague language (concrete pass/fail criteria present)
- [ ] Test plan references requirements explicitly
- [ ] Coverage threshold met (>90% for feature)
- [ ] All edge cases have tests
- [ ] All config scenarios have tests
- [ ] Error paths have tests
- [ ] Integration points have tests
- [ ] Traceability: Each test links to requirement

**If N > 0 issues:**
- Fix ALL issues immediately
- Continue to Round 2

**If N = 0 issues:**
- Proceed to Round 2 anyway (need 3 consecutive clean)
- Increment clean counter: count = 1

---

## Round 2: Edge Case Enumeration + Gap Detection (5-10 min)

**Pattern:** Re-read in different order, focus on gaps and edge cases

**Process:**

1. **Take 2-5 minute break** (clear mental model from Round 1)
2. **Re-read test case list** in different order (by test type, by requirement category, reverse)
3. **Re-read spec.md** with fresh perspective
4. **Ask "what else?":**
   - Are there edge cases I missed?
   - Are there integration points not tested?
   - Are there assumptions that need validation?
   - Are there boundary conditions I didn't consider?
5. **Document ALL issues found**

**Round 2 Checklist:**

- [ ] Re-read spec.md with fresh eyes
- [ ] Any new edge cases discovered?
- [ ] Any new integration points found?
- [ ] Any assumptions needing validation?
- [ ] Coverage gaps identified?
- [ ] Error handling tests comprehensive?
- [ ] Boundary conditions all tested?
- [ ] Config scenarios complete (default, custom, invalid, missing)?

**If N > 0 issues:**
- Fix ALL issues immediately
- Reset counter to 0
- Continue to Round 3

**If N = 0 issues:**
- Proceed to Round 3
- Increment clean counter: count = 2

---

## Round 3: Random Spot-Checks + Integration Verification (5-10 min)

**Pattern:** Random sampling, integration focus, final sweep

**Process:**

1. **Take 2-5 minute break** (fresh perspective)
2. **Random spot-check 5 requirements:**
   - Pick 5 requirements randomly (use: first, middle, last, 2 random)
   - For each: verify test coverage is comprehensive (happy + edge + error)
3. **Integration test verification:**
   - Check all integration points between features have tests
   - Check end-to-end workflow tests present
4. **Final coverage check:**
   - Re-calculate coverage estimate
   - Verify >90% goal met
5. **Document ALL issues found**

**Round 3 Checklist:**

- [ ] Random requirements all have complete coverage (happy + edge + error)
- [ ] Integration tests cover all feature interactions
- [ ] End-to-end workflow tests present
- [ ] Error handling tests comprehensive
- [ ] Final coverage estimate >90%
- [ ] No vague test descriptions remain
- [ ] All tests executable (not impossible scenarios)
- [ ] No duplicate test cases

**If N > 0 issues:**
- Fix ALL issues immediately
- Reset counter to 0
- Continue to Round 4

**If N = 0 issues:**
- Increment clean counter: count = 3
- **Check if count >= 3:** YES → PASSED, proceed to create test_strategy.md

---

## Rounds 4+ (If Issues Found in Round 3)

**If issues found in any round:**
- Fix ALL issues immediately
- Reset clean counter to 0
- Continue with next round
- Repeat until 3 consecutive rounds with ZERO issues

**Maximum rounds:** 10 (see `validation_loop_protocol.md` for escalation if exceeded)

---

## Exit Criteria

**Can only exit when:**
- [ ] 3 consecutive rounds found ZERO issues each
- [ ] All requirements have test coverage
- [ ] All edge cases tested
- [ ] All integration points tested
- [ ] Coverage >90%
- [ ] All test descriptions specific (not vague)
- [ ] Zero deferred issues

---

## Create test_strategy.md File

**After Validation Loop passes (3 consecutive clean rounds):**

Create `feature_{N}_{name}/test_strategy.md` with:

```markdown
# Test Strategy: {Feature Name}

**Purpose:** Define testing approach for {feature name} feature

**Created:** {YYYY-MM-DD} (S4.I4)
**Last Updated:** {YYYY-MM-DD}
**Status:** VALIDATED (Validation Loop passed with 3 consecutive clean rounds)

---

## Test Coverage Summary

**Total Tests Planned:** {N} tests
**Coverage Goal:** >90%
**Coverage Estimate:** {X}%

**Test Distribution:**
- Unit Tests: {N1} tests
- Integration Tests: {N2} tests
- Edge Case Tests: {N3} tests
- Configuration Tests: {N4} tests

---

## Test Coverage Matrix

{Paste matrix from I3}

---

## Traceability Matrix

{Paste matrix from I1}

---

## Unit Tests

{Paste unit test cases from I1}

---

## Integration Tests

{Paste integration test cases from I1}

---

## Edge Case Tests

{Paste edge case tests from I2}

**Edge Case Catalog:**
{Paste catalog from I2}

---

## Configuration Tests

{Paste config test cases from I3}

**Configuration Test Matrix:**
{Paste matrix from I3}

---

## Validation Loop Validation

**Validation Date:** {YYYY-MM-DD}
**Rounds Executed:** {N} rounds
**Issues Found:** 0 (after {N-3} rounds of fixes)
**Exit:** 3 consecutive clean rounds achieved ✅

**Round Summary:**
- Round {N-2}: 0 issues found (count = 1 clean)
- Round {N-1}: 0 issues found (count = 2 clean)
- Round {N}: 0 issues found (count = 3 clean) → PASSED

---

## Next Steps

**This file will be merged into implementation_plan.md during S5.P1.I1:**
- S5.P1.I1 will verify this file exists
- S5.P1.I1 will merge test strategy into "Test Strategy" section of implementation_plan.md
- Implementation tasks will reference these tests

---

*End of test_strategy.md*
```

**Verify file created:**
```bash
ls feature_{N}_{name}/test_strategy.md
```

---

## Update Feature README.md

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** S4_COMPLETE
**Current Step:** Completed S4.I4 (Validation Loop passed with 3 consecutive clean rounds)
**Current Guide:** stages/s4/s4_validation_loop.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** S4 complete - test_strategy.md created and validated
**Next Action:** Transition to S5 (Implementation Planning)
**Blockers:** None

**Test Summary:**
- Total tests: {N}
- Coverage: {X}% (>90% goal met ✅)
- Validation Loop: PASSED (3 consecutive clean rounds)
```

---

## Completion Criteria

**S4.I4 is complete when ALL of these are true:**

□ Validation Loop executed with master protocol
□ 3 consecutive rounds found ZERO issues
□ ALL issues fixed (no deferred issues)
□ test_strategy.md created in `feature_{N}_{name}/` folder
□ test_strategy.md has all required sections (not empty)
□ test_strategy.md shows >90% coverage
□ Feature README.md updated with S4_COMPLETE status

**If any item unchecked:**
- ❌ S4.I4 is NOT complete
- ❌ Do NOT proceed to S5
- Complete missing items first

---

## Next: S5 (Implementation Planning)

**After completing S4.I4:**

📖 **READ:** `stages/s5/s5_p1_planning_round1.md` (Round 1)
🎯 **GOAL:** Create implementation plan (22 verification iterations across 3 rounds)
⏱️ **ESTIMATE:** 2-3 hours per feature (split across 3 rounds)

**S5.P1.I1 will:**
- Verify test_strategy.md exists (MANDATORY check)
- Merge test strategy into implementation_plan.md
- Continue with 22 verification iterations

**Remember:** Use phase transition prompt from `prompts_reference_v2.md` when starting S5.

---

*End of stages/s4/s4_validation_loop.md*
