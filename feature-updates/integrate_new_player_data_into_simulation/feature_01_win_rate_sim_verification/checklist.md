# Feature 01: Win Rate Simulation - Planning Checklist

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

---

## Open Questions

### Question 1: Verification Methodology ✅ RESOLVED

- [x] How should we verify the existing JSON loading implementation is correct?
  - **ANSWER: Option D (All of the above - comprehensive verification)**

**User's Answer (2026-01-02):**
"D - also note that we need to make sure the simulation has correctly adapted to the new ways of storing data, such as by using the new projected_points and actual_points arrays correctly"

**Verification approach includes:**
1. Code review (line-by-line implementation analysis)
2. Manual testing (run simulation, inspect loaded data)
3. Automated tests (verify coverage exists, add if missing)
4. Specific verification: Ensure simulation correctly uses projected_points and actual_points arrays

**Impacts on spec:**
- Requirement 6 expanded to include all verification methods
- Testing Strategy updated to reflect comprehensive approach
- Added explicit requirement to verify array usage correctness

---

### Question 2: Test Coverage Requirements ✅ RESOLVED

- [x] If JSON loading tests are missing from test_SimulatedLeague.py, should we add them?
  - **ANSWER: Option A (Yes, add comprehensive JSON loading tests)**

**User's Answer (2026-01-03):**
"A"

**Implementation approach:**
- Inspect tests/simulation/test_SimulatedLeague.py to identify coverage gaps
- Add comprehensive tests for JSON loading functionality:
  - Test `_parse_players_json()` method with valid JSON data
  - Test correct extraction of week-specific values from arrays
  - Test field conversions (locked boolean → string, arrays → single values)
  - Test handling of all 6 position files (QB, RB, WR, TE, K, DST)
  - Test error handling for missing files
  - Test error handling for malformed JSON
  - Test edge cases (empty arrays, missing fields)
- Ensure tests provide regression protection for JSON loading logic

**Impacts on spec:**
- Testing Strategy Part 3 confirmed: Add comprehensive JSON loading tests if missing
- Requirement 6 Part 3 scope expanded to include full test coverage

---

### Question 3: Week 17 Specific Testing ✅ RESOLVED

- [x] Should we add specific tests for Week 17 edge case?
  - **ANSWER: Option A (Yes, dedicated test verifying week_17 projected + week_18 actual)**

**User's Answer (2026-01-03):**
"A"

**Implementation approach:**
- Add dedicated test for Week 17 edge case verification:
  - Test that week 17 simulation loads projected_points from week_17 folder
  - Test that week 17 simulation loads actual_points from week_18 folder
  - Test array indexing: projected_points[16] from week_17, actual_points[16] from week_18
  - Verify week_num_for_actual=18 parameter used correctly for week 17
  - Test with real data structure (17-element arrays)
- This is in addition to broader week_N+1 pattern tests
- Provides explicit regression protection for user's specific concern

**Impacts on spec:**
- Testing Strategy Part 3: Confirmed need for dedicated Week 17 test
- Requirement 6 Part 3: Add specific Week 17 test case to automated tests section

---

### Question 4: Edge Case Handling Verification ✅ RESOLVED

- [x] Should we verify the edge case handlers are correct, or just that they exist?
  - **ANSWER: Option A (Verify behavior is correct - test missing files, invalid data, etc.)**

**User's Answer (2026-01-03):**
"A"

**Implementation approach:**
- Add tests to verify edge case handlers work correctly:
  - **Missing JSON file test:**
    - Create scenario where one position file is missing
    - Verify logger.warning is called
    - Verify simulation continues (doesn't crash)
    - Verify other position files still loaded correctly
  - **Missing week_18 folder test:**
    - Create scenario where week_18 folder doesn't exist
    - Verify fallback to projected data works
    - Verify logger.warning is called
    - Verify simulation uses projected values for actuals
  - **Array index out of bounds test:**
    - Create scenario with arrays shorter than 17 elements
    - Verify default value 0.0 is used
    - Verify no IndexError is raised
    - Test both projected_points and actual_points arrays
  - **Malformed JSON test:**
    - Test with invalid JSON syntax
    - Test with missing required fields
    - Verify appropriate error handling

**Impacts on spec:**
- Testing Strategy Part 3: Add edge case behavior tests
- Requirement 6 Part 3: Expand automated tests to include edge case verification

---

## Resolved Questions

All 4 questions have been resolved and integrated into spec.md:

1. **Question 1: Verification Methodology** ✅
   - Answer: Option D (Comprehensive verification - all methods)
   - User requirement: Verify projected_points and actual_points arrays used correctly
   - Integrated into: Requirement 6 (Three-part verification)

2. **Question 2: Test Coverage Requirements** ✅
   - Answer: Option A (Add comprehensive JSON loading tests)
   - Integrated into: Requirement 6 Part 3 (detailed test requirements)

3. **Question 3: Week 17 Specific Testing** ✅
   - Answer: Option A (Dedicated Week 17 test)
   - Integrated into: Requirement 6 Part 3 (Week 17 test case)

4. **Question 4: Edge Case Handling Verification** ✅
   - Answer: Option A (Verify behavior is correct)
   - Integrated into: Requirement 6 Part 3 (edge case behavior tests)

---

## Additional Scope Discovered

**None** - All work traces back to epic requests. No scope creep identified.

**User's explicit requests (all covered in spec.md):**
1. Remove CSV loading (line 4) → Requirement 1
2. Verify JSON loading (line 5) → Requirement 2
3. Verify field handling (line 6) → Requirement 3
4. Verify Week 17 logic (line 8) → Requirement 4
5. Update documentation (line 4) → Requirement 5
6. Verify correctness (line 10) → Requirement 6

All requirements traced to sources. No assumptions.
