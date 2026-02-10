# Validation Loop: Test Strategy

**Extends:** Master Validation Loop Protocol
**See:** `reference/validation_loop_master_protocol.md`

**Applicable Stages:**
- S3.P1: Epic Testing Strategy Development
- S4: Feature Testing Strategy

**Version:** 2.0 (Updated to extend master protocol)
**Last Updated:** 2026-02-10

---

## Table of Contents

1. [Overview](#overview)
2. [Master Dimensions (7) - Always Checked](#master-dimensions-7---always-checked)
3. [Test Strategy Dimensions (3) - Context-Specific](#test-strategy-dimensions-3---context-specific)
4. [Total Dimensions: 10](#total-dimensions-10)
5. [What's Being Validated](#whats-being-validated)
6. [Fresh Eyes Patterns Per Round](#fresh-eyes-patterns-per-round)
7. [Common Issues in Test Strategy Context](#common-issues-in-test-strategy-context)
8. [Exit Criteria](#exit-criteria)
9. [Integration with Stages](#integration-with-stages)

---

## Overview

**Purpose:** Validate test plans and coverage to ensure comprehensive testing before implementation

**What this validates:**
- epic_smoke_test_plan.md (epic-level in S3.P1)
- test_strategy.md (feature-level in S4)

**Quality Standard:**
- >90% coverage planned (feature-level)
- 100% critical epic paths (epic-level)
- All edge cases identified
- All integration points tested

**Uses:** All 7 master dimensions + 3 test strategy-specific dimensions = 10 total

---

## Master Dimensions (7) - Always Checked

**See `reference/validation_loop_master_protocol.md` for complete checklists.**

These universal dimensions apply to test strategy validation:

### Dimension 1: Empirical Verification
- [ ] All referenced test commands verified to work
- [ ] All test file paths verified to exist (if tests already exist)
- [ ] All referenced requirements traced to actual spec.md sections
- [ ] All tool versions verified (pytest, coverage, etc.)

### Dimension 2: Completeness
- [ ] All test categories present (unit, integration, edge, config)
- [ ] All requirements have test coverage
- [ ] All edge cases enumerated
- [ ] All test scenarios have expected results

### Dimension 3: Internal Consistency
- [ ] No contradictory test expectations
- [ ] Test naming consistent throughout
- [ ] Test organization follows consistent pattern
- [ ] Coverage percentages add up correctly

### Dimension 4: Traceability
- [ ] Every test traces to a requirement
- [ ] Every requirement has at least one test
- [ ] Test-to-requirement mapping complete
- [ ] No orphan tests (no requirement)

### Dimension 5: Clarity & Specificity
- [ ] No vague test descriptions ("test login works")
- [ ] Specific pass/fail criteria ("return HTTP 200 with session token")
- [ ] Expected values concrete (not "appropriate response")
- [ ] Test steps actionable (can be implemented)

### Dimension 6: Upstream Alignment
- [ ] Test coverage matches spec requirements (no missing)
- [ ] No test for unrequested functionality (no scope creep)
- [ ] Epic test plan reflects epic goals
- [ ] Feature test plan reflects feature spec

### Dimension 7: Standards Compliance
- [ ] Follows test strategy template
- [ ] Test file naming follows project conventions
- [ ] Test organization follows project structure
- [ ] Uses project testing frameworks (pytest)

---

## Test Strategy Dimensions (3) - Context-Specific

These 3 dimensions are specific to test strategy validation:

### Dimension 8: Test Coverage Threshold

**Question:** Does test coverage meet minimum thresholds?

**Checklist:**

**Feature-Level (S4):**
- [ ] >90% requirement coverage planned
- [ ] All critical path requirements have tests
- [ ] All error paths have tests
- [ ] All edge cases have tests

**Epic-Level (S3.P1):**
- [ ] 100% critical epic paths covered
- [ ] All end-to-end scenarios covered
- [ ] All cross-feature integration points covered
- [ ] All smoke test scenarios defined

**Coverage Calculation:**
```
Coverage = (Requirements with tests) / (Total requirements) × 100%

Feature-level minimum: >90%
Epic-level critical paths: 100%
```

**Common Violations:**

❌ **WRONG - Below threshold:**
```markdown
Test Coverage:
- Requirements with tests: 27/32
- Coverage: 84% ← BELOW 90% threshold
```

✅ **CORRECT - Meets threshold:**
```markdown
Test Coverage:
- Requirements with tests: 30/32
- Coverage: 94% ✅
- Missing requirements: R15, R28 (optional features - excluded from coverage)
```

---

### Dimension 9: Edge Case Completeness

**Question:** Are ALL edge cases identified and tested?

**Checklist:**

**Boundary Conditions:**
- [ ] Min/max value tests (e.g., adp = 1, adp = 500)
- [ ] Empty input tests (empty list, empty string)
- [ ] Null/None input tests
- [ ] Zero value tests

**Error Conditions:**
- [ ] File not found tests
- [ ] Invalid format tests (malformed CSV, invalid JSON)
- [ ] Network errors (timeout, connection failed)
- [ ] Permission errors (access denied)

**Data Quality:**
- [ ] Missing required fields tests
- [ ] Duplicate data tests
- [ ] Inconsistent data tests
- [ ] Out-of-range value tests

**Integration Edge Cases:**
- [ ] Upstream dependency failure tests
- [ ] Partial data from integration tests
- [ ] Timing/race condition tests (if async)

**Common Violations:**

❌ **WRONG - Generic edge case:**
```markdown
Edge Cases:
- Test error handling
- Test invalid input
```

✅ **CORRECT - Specific edge cases:**
```markdown
Edge Cases:
1. File not found: Verify returns empty list, logs error
2. Invalid ADP value (0): Verify raises ValueError with message "ADP must be 1-500"
3. Invalid ADP value (501): Verify raises ValueError
4. Missing required column: Verify raises KeyError with column name
5. Empty CSV file: Verify returns empty list, logs warning
6. Duplicate player names: Verify uses first occurrence, logs warning
```

---

### Dimension 10: Test Execution Feasibility

**Question:** Can all planned tests actually be executed?

**Checklist:**

**Executable Tests:**
- [ ] All test scenarios have clear steps
- [ ] All test data sources are real (files exist or can be created)
- [ ] All test commands are valid (syntax checked)
- [ ] No circular dependencies in test order

**Test Environment:**
- [ ] Required test fixtures identified
- [ ] Required test data identified
- [ ] Required mock objects identified
- [ ] Test isolation ensured (no shared state)

**Measurement:**
- [ ] Pass/fail criteria are measurable
- [ ] Expected results are observable
- [ ] Test assertions are concrete
- [ ] No subjective criteria ("looks good")

**Common Violations:**

❌ **WRONG - Impossible test:**
```markdown
Test Scenario 5:
- Verify system handles all possible inputs correctly
- Expected: All inputs work
```

✅ **CORRECT - Executable test:**
```markdown
Test Scenario 5:
- Input: adp = -1 (invalid)
- Command: player_manager.get_adp_multiplier(-1)
- Expected: Raises ValueError("ADP must be 1-500")
- Verification: Use pytest.raises(ValueError, match="ADP must be 1-500")
```

---

## Total Dimensions: 10

**Every validation round checks ALL 10 dimensions:**
- 7 Master dimensions (universal)
- 3 Test Strategy dimensions (context-specific)

**Process:** See master protocol for 3 consecutive clean rounds requirement

---

## What's Being Validated

### S3.P1: Epic Testing Strategy

**Artifact:** epic_smoke_test_plan.md

**Validates:**
- End-to-end user scenarios
- Cross-feature integration tests
- Critical epic path coverage
- Smoke test scenarios
- Integration point testing

**Success Criteria:**
- 100% critical epic paths covered
- All end-to-end scenarios defined
- All cross-feature integration tested

---

### S4: Feature Testing Strategy

**Artifact:** test_strategy.md

**Validates:**
- Unit test coverage
- Integration test coverage
- Edge case coverage
- Configuration test coverage
- >90% requirement coverage

**Success Criteria:**
- >90% coverage planned
- All edge cases identified
- All integration points tested
- Test strategy detailed enough to implement

---

## Fresh Eyes Patterns Per Round

**See master protocol for general fresh eyes principles.**

Test strategy-specific reading patterns:

### Round 1: Sequential Read + Coverage Matrix

**Pattern:**
1. Read test plan sequentially (top to bottom)
2. Read spec.md/epic requirements
3. Create coverage matrix (requirement → tests)
4. Check for missing coverage

**Checklist:**
- [ ] All 10 dimensions checked (7 master + 3 test strategy)
- [ ] Coverage matrix shows >90% (feature) or 100% critical paths (epic)
- [ ] Every requirement has at least one test
- [ ] All tests trace to requirements

**Document findings in validation log**

---

### Round 2: Edge Case Audit + Integration Review

**Pattern:**
1. Read test plan by requirement category
2. For each requirement, enumerate edge cases
3. Verify edge cases have test coverage
4. Check integration point coverage

**Focus Areas:**
- Dimension 9 (Edge Case Completeness) - primary focus
- Dimension 8 (Test Coverage) - verify edge cases counted
- Dimension 2 (Completeness) - no missing edge cases

**Checklist:**
- [ ] All 10 dimensions checked
- [ ] All edge cases identified (boundary, error, data quality, integration)
- [ ] Integration points have integration tests
- [ ] Error scenarios tested (not just happy path)

---

### Round 3: Random Spot-Checks + Feasibility

**Pattern:**
1. Random spot-check 5 requirements
2. Verify each has comprehensive test coverage
3. Check test execution feasibility
4. Verify no impossible/subjective tests

**Focus Areas:**
- Dimension 10 (Test Execution Feasibility) - primary focus
- Dimension 5 (Clarity & Specificity) - concrete pass/fail
- All master dimensions - final sweep

**Checklist:**
- [ ] All 10 dimensions checked
- [ ] Spot-checked requirements have complete coverage
- [ ] All tests are executable (not impossible)
- [ ] No subjective pass/fail criteria

---

## Common Issues in Test Strategy Context

### Issue 1: Requirements Without Tests

**Problem:** Requirement exists but no test coverage planned

❌ **WRONG:**
```markdown
spec.md Requirements:
- R1: Load ADP data
- R2: Validate player names
- R3: Calculate multipliers
- R4: Handle errors

test_strategy.md:
- Test 1: Load ADP data ✓
- Test 2: Calculate multipliers ✓
← Missing: R2 (Validate player names), R4 (Handle errors)
```

✅ **CORRECT:**
```markdown
test_strategy.md:
- Test 1: Load ADP data (covers R1)
- Test 2: Validate player names - valid format (covers R2)
- Test 3: Validate player names - invalid format (covers R2)
- Test 4: Calculate multipliers (covers R3)
- Test 5: Handle FileNotFoundError (covers R4)
- Test 6: Handle ValueError (covers R4)

Coverage: 100% (all requirements covered)
```

---

### Issue 2: Vague Test Descriptions

**Problem:** Test description doesn't specify pass/fail criteria

❌ **WRONG:**
```markdown
Test 3: Test login functionality
- Verify login works correctly
```

✅ **CORRECT:**
```markdown
Test 3: Login with valid credentials
- Input: username="user1", password="valid_pass"
- Expected: HTTP 200, session token in response body
- Verification: assert response.status_code == 200
                 assert "session_token" in response.json()
```

---

### Issue 3: Missing Edge Cases

**Problem:** Only happy path tested, edge cases missing

❌ **WRONG:**
```markdown
Test 1: Load ADP data
- Load from data/rankings/adp.csv
- Expected: List of 200 players
```

✅ **CORRECT:**
```markdown
Test 1a: Load ADP data - happy path
- Load from data/rankings/adp.csv
- Expected: List of 200 players

Test 1b: Load ADP data - file not found
- Load from non_existent.csv
- Expected: FileNotFoundError OR empty list with logged error

Test 1c: Load ADP data - empty file
- Load from empty.csv
- Expected: Empty list, warning logged

Test 1d: Load ADP data - missing required column
- Load from invalid_columns.csv
- Expected: KeyError with column name
```

---

### Issue 4: Coverage Below Threshold

**Problem:** <90% requirement coverage (feature-level)

❌ **WRONG:**
```markdown
Coverage Analysis:
- Total requirements: 35
- Requirements with tests: 28
- Coverage: 80% ← BELOW threshold
```

✅ **CORRECT:**
```markdown
Coverage Analysis:
- Total requirements: 35
- Requirements with tests: 32
- Coverage: 91.4% ✅

Missing requirements (3):
- R14: Optional enhancement (excluded from coverage)
- R22: Future iteration (excluded from coverage)
- R30: Optional feature (excluded from coverage)

Covered requirements: 32/32 required = 100% ✅
```

---

### Issue 5: Duplicate Tests

**Problem:** Same test case planned multiple times

❌ **WRONG:**
```markdown
Test 3: Validate player names
Test 7: Check player name format
Test 12: Player name validation
← All testing the same thing (duplicates)
```

✅ **CORRECT:**
```markdown
Test 3: Validate player names
- Valid format: Letters, spaces, hyphens
- Invalid format: Numbers, special chars
- Edge cases: Empty string, null

(Tests 7 and 12 removed - duplicates of Test 3)
```

---

### Issue 6: Impossible Tests

**Problem:** Test cannot be executed or measured

❌ **WRONG:**
```markdown
Test 10: Verify system performance is good
- Expected: System performs well
```

✅ **CORRECT:**
```markdown
Test 10: Verify data loading performance
- Input: data/players_2024.csv (1000 rows)
- Expected: Load completes in < 2 seconds
- Measurement: Use time.time() to measure load_players() duration
- Verification: assert duration < 2.0
```

---

## Exit Criteria

**Test strategy validation is COMPLETE when ALL of the following are true:**

**From Master Protocol:**
- [ ] 3 consecutive rounds with ZERO issues found
- [ ] All 7 master dimensions checked every round
- [ ] All 3 test strategy dimensions checked every round
- [ ] Validation log complete with all rounds documented

**Test Strategy Specific:**
- [ ] Coverage threshold met:
  - Feature-level: >90% requirement coverage
  - Epic-level: 100% critical path coverage
- [ ] All edge cases identified and tested
- [ ] All integration points have integration tests
- [ ] Zero requirements without tests
- [ ] Zero vague test descriptions
- [ ] All tests are executable (feasibility verified)
- [ ] Ready for implementation (feature) or approval (epic)

**Cannot exit if:**
- ❌ Coverage below threshold
- ❌ Any requirement without test
- ❌ Any missing edge cases
- ❌ Any vague test descriptions
- ❌ Any impossible/unexecutable tests

---

## Integration with Stages

### S3.P1: Epic Testing Strategy Development

**When:** After all feature specs complete (S2 done for all features)

**Validates:** epic_smoke_test_plan.md

**Process:**
1. Use this validation loop protocol
2. Check all 10 dimensions (7 master + 3 test strategy)
3. Exit when 3 consecutive clean rounds
4. Proceed to S3.P2 (Epic Documentation Refinement)

**Threshold:** 100% critical epic path coverage

---

### S4: Feature Testing Strategy

**When:** After S3 complete, before S5 (Implementation Planning)

**Validates:** test_strategy.md (per feature)

**Process:**
1. Use this validation loop protocol
2. Check all 10 dimensions (7 master + 3 test strategy)
3. Exit when 3 consecutive clean rounds
4. Proceed to S5 (Implementation Planning)

**Threshold:** >90% requirement coverage

---

## Example Validation Round Sequence

```text
Round 1: Sequential + Coverage Matrix
- Read test_strategy.md top to bottom
- Read spec.md requirements
- Create coverage matrix
- Check all 10 dimensions
- Issues found: 5
  - D2 (Completeness): Missing edge case tests for R3, R7
  - D4 (Traceability): Test T5 doesn't reference requirement
  - D8 (Coverage): Coverage 87% (below 90%)
  - D9 (Edge Cases): R3 missing boundary condition tests
- Fix all 5 issues
- Clean counter: 0

Round 2: Edge Case Audit
- Read by requirement category
- Enumerate edge cases per requirement
- Check all 10 dimensions
- Issues found: 2
  - D9 (Edge Cases): R12 missing error path test
  - D10 (Feasibility): Test T8 has subjective pass criteria
- Fix all 2 issues
- Clean counter: 0

Round 3: Random Spot-Checks
- Spot-check 5 requirements
- Verify test coverage comprehensive
- Check all 10 dimensions
- Issues found: 0 ✅
- Clean counter: 1

Round 4: Repeat Validation
- Fresh eyes, different pattern
- Check all 10 dimensions
- Issues found: 0 ✅
- Clean counter: 2

Round 5: Final Sweep
- Complete re-read
- Check all 10 dimensions
- Issues found: 0 ✅
- Clean counter: 3 → VALIDATION COMPLETE ✅
```

---

## Summary

**Test Strategy Validation Loop:**
- **Extends:** Master Validation Loop Protocol (7 universal dimensions)
- **Adds:** 3 test strategy-specific dimensions
- **Total:** 10 dimensions checked every round
- **Process:** 3 consecutive clean rounds required
- **Coverage:** >90% (feature) or 100% critical paths (epic)
- **Quality:** All edge cases, integration points, and requirements tested

**Key Principle:**
> "Every requirement must have comprehensive test coverage (happy path + edge cases + errors) before implementation begins."

---

*End of Test Strategy Validation Loop v2.0*
