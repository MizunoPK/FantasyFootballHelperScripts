# Consistency Loop: Test Strategy Context

**Master Protocol:** See `consistency_loop_protocol.md`

**Context:** S3.P1 Epic Testing Strategy, S4 Feature Testing Strategy

---

## What's Being Validated

Test plans and coverage including:
- epic_smoke_test_plan.md (epic-level)
- test_strategy.md (feature-level)
- Test coverage for all requirements
- Edge case identification
- Integration test coverage
- End-to-end scenario coverage

---

## What Counts as "Issue"

An issue in test strategy context is any of:
- **Requirements without tests:** Requirement exists but no test coverage planned
- **Missing edge cases:** Edge cases not identified or tested
- **Integration gaps:** Integration points without integration tests
- **Coverage below threshold:** <90% coverage planned (feature-level)
- **Vague test descriptions:** "Test login" vs "Verify valid credentials succeed, invalid credentials fail with HTTP 401"
- **Missing end-to-end scenarios:** User workflows not tested (epic-level)
- **Duplicate tests:** Same test case planned multiple times
- **Impossible tests:** Test cases that can't be executed

---

## Fresh Eyes Patterns Per Round

### Round 1: Sequential Read + Requirement Coverage Check
**Pattern:**
1. Read test plan top to bottom
2. Read requirements document (spec.md or epic requirements)
3. For each requirement, verify test coverage exists
4. Check test descriptions are specific (not vague)
5. Document ALL gaps found

**Checklist:**
- [ ] Every requirement has at least one test
- [ ] All test descriptions are specific and measurable
- [ ] No vague language (concrete pass/fail criteria)
- [ ] Test plan references requirements explicitly
- [ ] Coverage threshold met (>90% for features)

### Round 2: Edge Case Enumeration + Gap Detection
**Pattern:**
1. Read test plan in different order (by requirement category, by test type, etc.)
2. For each requirement, enumerate edge cases
3. Verify edge cases have test coverage
4. Check for missing integration tests
5. Document ALL gaps found

**Checklist:**
- [ ] Edge cases identified for each requirement
- [ ] All edge cases have test coverage
- [ ] Integration points between features tested
- [ ] Error scenarios tested (not just happy path)
- [ ] Boundary conditions tested

### Round 3: Random Spot-Checks + Integration Verification
**Pattern:**
1. Random spot-check 5 requirements
2. Verify each has comprehensive test coverage (happy path + edge cases + errors)
3. Check end-to-end scenarios (epic-level) or integration tests (feature-level)
4. Verify no duplicate tests
5. Document ALL gaps found

**Checklist:**
- [ ] Random requirements all have complete coverage
- [ ] End-to-end scenarios complete (epic-level)
- [ ] Integration tests complete (feature-level)
- [ ] No duplicate test cases
- [ ] All tests are executable (not impossible)

---

## Specific Criteria

**All of these MUST pass for loop to exit:**

**Feature-Level (S4):**
- [ ] Every requirement in spec.md has test coverage
- [ ] All edge cases identified and tested
- [ ] All integration points have integration tests
- [ ] >90% test coverage planned
- [ ] All test descriptions specific (concrete pass/fail criteria)
- [ ] No vague language remains

**Epic-Level (S3.P1):**
- [ ] Every epic requirement has test coverage
- [ ] End-to-end user scenarios identified and tested
- [ ] Cross-feature integration tested
- [ ] Smoke test cases cover critical paths
- [ ] All test descriptions specific
- [ ] Test plan references epic requirements

**Both Levels:**
- [ ] Zero requirements without tests
- [ ] Zero missing edge cases
- [ ] Zero integration gaps
- [ ] Zero vague test descriptions
- [ ] Ready for implementation

---

## Example Round Sequence

```
Round 1: Sequential + requirement coverage
- Read test_strategy.md top to bottom
- Check: Requirement R3 has no test coverage, R7 test is vague ("test error handling")
- Fix: Add test for R3, make R7 specific ("Verify HTTP 400 on invalid input, HTTP 500 on server error")
- Continue to Round 2

Round 2: Edge case enumeration
- Read by requirement category
- Check: Requirement R5 missing edge case (null input), integration test for F1-F2 missing
- Fix: Add null input test for R5, add F1-F2 integration test
- Continue to Round 3

Round 3: Random spot-checks + integration
- Random spot-check 5 requirements
- Check: 0 issues found → Continue (count = 1 clean)

Round 4: Repeat validation
- Check: 0 issues found → Continue (count = 2 clean)

Round 5: Final sweep
- Check: 0 issues found → PASSED (count = 3 consecutive clean)
```

---

## Common Issues in Test Strategy Context

1. **Requirements without tests:** Requirement R9 exists but no test → Add test for R9
2. **Vague test descriptions:** "Test login works" → "Verify valid credentials return HTTP 200 and session token, invalid credentials return HTTP 401"
3. **Missing edge cases:** "Test data loading" but no null/empty/malformed tests → Add edge case tests
4. **Integration gaps:** Features F1 and F2 integrate but no integration test → Add F1-F2 integration test
5. **Coverage below threshold:** 85% coverage planned → Add tests to reach >90%
6. **Duplicate tests:** "Test login" appears 3 times → Consolidate into single comprehensive test

---

## Integration with Stages

**S3.P1 Epic Testing Strategy:**
- Use this protocol for epic_smoke_test_plan.md
- Validate end-to-end scenarios cover all epic requirements
- Must pass before S4 (feature testing strategies)

**S4 Feature Testing Strategy:**
- Use this protocol for each feature's test_strategy.md
- Validate >90% coverage planned for feature
- Must pass before Gate 4.5 (User Approval)

---

## Exit Criteria Specific to Test Strategy

**Can only exit when ALL true:**
- [ ] 3 consecutive rounds found zero issues
- [ ] All requirements have test coverage
- [ ] All edge cases identified and tested
- [ ] All integration points tested
- [ ] Coverage threshold met (>90% features, 100% critical epic paths)
- [ ] Zero vague test descriptions
- [ ] Ready for user approval (Gate 4.5) or implementation

---

**Remember:** Follow all 7 principles from master protocol. This guide only specifies HOW to apply them in test strategy context, not WHETHER to apply them.
