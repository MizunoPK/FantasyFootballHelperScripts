# STAGE 4: Feature Testing Strategy - Quick Reference Card

> **⚠️ DEPRECATED (SHAMT-6):** S4 has been deprecated. Test Scope Decision is now Step 0 of S5.
> See `stages/s4/s4_feature_testing_strategy.md` for the redirect stub.
> This file is preserved for reference only — do NOT follow for new epics.

**Purpose:** (Deprecated) One-page summary for creating feature-level test strategy before implementation
**Status:** DEPRECATED — Test Scope Decision moved to S5 Step 0
**Total Time:** N/A (deprecated)

---

## Workflow Overview

```text
STEP 1: Test Strategy Development (S4.I1 — 15-20 min)
    ├─ Read spec.md requirements
    ├─ For each requirement: identify testable behaviors, inputs/outputs, error conditions
    ├─ Create test coverage matrix (requirement → test mapping)
    ├─ Enumerate test cases (unit, integration, edge)
    └─ Link each test to requirement (traceability)
    ↓
STEP 2: Edge Case Enumeration (S4.I2 — 10-15 min)
    ├─ For each input: min/max, null/empty/zero, invalid types, special characters
    ├─ Enumerate error paths (invalid input, dependency failures, race conditions)
    ├─ Create edge case catalog
    └─ Update test coverage matrix
    ↓
STEP 3: Configuration Change Impact (S4.I3 — 10-15 min)
    ├─ Identify config files used by feature
    ├─ For each config value: default, custom, invalid, missing behavior
    ├─ Create configuration test matrix
    └─ Verify >90% coverage goal met
    ↓
STEP 4: Validation Loop (S4.I4 — 15-20 min)
    ├─ Reference: validation_loop_test_strategy.md
    ├─ Round 1: Sequential read + requirement coverage check
    ├─ Round 2: Edge case enumeration + gap detection
    ├─ Round 3: Random spot-checks + integration verification
    └─ Exit: 3 consecutive clean rounds
```

---

## Step Summary Table

| Step | Duration | Key Activities | Outputs | Gate? |
|------|----------|----------------|---------|-------|
| I1 | 15-20 min | Requirement analysis, test enumeration | Test coverage matrix, test case list | No |
| I2 | 10-15 min | Edge cases, error paths | Edge case catalog, updated matrix | No |
| I3 | 10-15 min | Config dependency analysis | Config test matrix, final coverage matrix | No |
| I4 | 15-20 min | Validation Loop (3 consecutive clean rounds) | test_strategy.md (validated) | No gates |

**Note:** S4 has ZERO formal gates. test_strategy.md is agent-validated only (via Validation Loop in I4). User approval is NOT required for test_strategy.md.

---

## Key Rules

- ✅ test-driven development (plan tests BEFORE coding)
- ✅ >90% coverage goal (feature-level, not epic-level)
- ✅ All 4 iterations MANDATORY (I1, I2, I3, I4)
- ✅ Validation Loop (I4) requires 3 consecutive clean rounds
- ✅ test_strategy.md created in S4, merged into implementation_plan.md in S5.P1.I1
- ✅ Update README Agent Status after EACH iteration
- ✅ Zero deferred issues (fix ALL issues immediately in I4 Validation Loop)
- ✅ 🚨 **Gate 4.5 was passed in S3.P3 (NOT in S4)** — S4 has no user approval gates

---

## Common Pitfalls

### ❌ Pitfall 1: Updating epic_smoke_test_plan.md in S4 (Wrong Stage)
**Problem:** Trying to update epic_smoke_test_plan.md in S4
**Impact:** Doing the wrong work; epic test plan was finalized in S3.P1
**Solution:** S4 creates FEATURE-level test_strategy.md (one per feature). Epic testing was done in S3.P1.

### ❌ Pitfall 2: Expecting Gate 4.5 to happen in S4
**Problem:** Waiting for user approval of test_strategy.md
**Impact:** Unnecessary delay; S4 is agent-validated only
**Solution:** Gate 4.5 was in S3.P3 (epic plan approval). Proceed to S5 after I4 Validation Loop passes.

### ❌ Pitfall 3: Vague Test Coverage
**Problem:** "I'll test requirement X" with no specifics
**Impact:** Can't verify coverage in S7 (testing)
**Solution:** Define SPECIFIC test scenarios (input → expected output → assertion)

### ❌ Pitfall 4: Skipping Config Tests
**Problem:** "This feature doesn't use config much"
**Impact:** Config bugs slip through to S7
**Solution:** I3 is MANDATORY - identify ALL config dependencies

### ❌ Pitfall 5: Merging test_strategy.md into implementation_plan.md in S4
**Problem:** Trying to merge test strategy early
**Impact:** S5.P1.I1 explicitly merges them; doing it in S4 causes confusion
**Solution:** Create test_strategy.md in S4. Let S5.P1.I1 perform the merge.

---

## Transition Checklist

**Prerequisites (before S4):**
- [ ] S3 complete (Gate 4.5 passed — epic plan user-approved in S3.P3)
- [ ] spec.md finalized and user-approved (Gate 3 passed from S2)
- [ ] Feature README.md has Agent Status section

**Iterations completion:**
- [ ] I1 → I2: Test coverage matrix created
- [ ] I2 → I3: Edge case catalog created
- [ ] I3 → I4: Config test matrix created, coverage >90%
- [ ] I4 → Create test_strategy.md: Validation Loop PASSED (3 consecutive clean rounds)

**Step 4 → S5:**
- [ ] test_strategy.md exists in feature folder
- [ ] test_strategy.md shows >90% coverage (not placeholder)
- [ ] All sections populated (unit, integration, edge, config tests)
- [ ] Traceability matrix complete (requirement → test mapping)
- [ ] README Agent Status shows S4_COMPLETE
- [ ] **NO Gate 4.5 here** — Gate 4.5 was passed in S3.P3 (proceed directly to S5)

---

## File Outputs

**I1 (Test Strategy Development):**
- Test coverage matrix (draft): unit, integration, edge test cases
- Traceability matrix: requirement → test mapping

**I2 (Edge Case Enumeration):**
- Edge case catalog: boundary conditions, error paths

**I3 (Configuration Change Impact):**
- Configuration test matrix: default, custom, invalid, missing scenarios
- Final test coverage matrix (>90%)

**I4 (Validation Loop):**
- test_strategy.md in `feature_{N}_{name}/` folder:
  - All test categories
  - Representative test cases
  - Coverage goal >90%
  - Traceability matrix
  - Edge case catalog
  - Configuration test matrix

---

## When to Use Which Guide

| Current Activity | Guide to Read |
|------------------|---------------|
| Starting S4 | stages/s4/archive/s4_feature_testing_strategy.md |
| Executing iterations (I1-I3) | stages/s4/archive/s4_test_strategy_development.md |
| Executing Validation Loop (I4) | stages/s4/archive/s4_validation_loop.md |
| Need test strategy validation dimensions | reference/archive/validation_loop_test_strategy.md |

---

## Exit Conditions

**S4 is complete when:**
- [ ] All 4 iterations complete (I1, I2, I3, I4)
- [ ] Validation Loop (I4) passed with 3 consecutive clean rounds
- [ ] test_strategy.md created in `feature_{N}_{name}/` folder
- [ ] test_strategy.md has all required sections
- [ ] Coverage goal >90% documented
- [ ] Traceability matrix complete
- [ ] README Agent Status shows S4_COMPLETE
- [ ] Ready to start S5 (NO user approval needed — S4 has zero formal gates)

**Next Stage:** S5 (Implementation Planning) — start by reading `stages/s5/s5_v2_validation_loop.md`

---

**Last Updated:** 2026-02-21
