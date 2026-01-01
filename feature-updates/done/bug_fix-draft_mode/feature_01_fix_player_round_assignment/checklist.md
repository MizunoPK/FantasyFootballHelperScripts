# Feature 01: Fix Player-to-Round Assignment - Planning Checklist

**Purpose:** Track open questions and decisions for this feature

**Instructions:**
- [ ] = Open question (needs user answer)
- [x] = Resolved (answer documented below)

---

## Open Questions

### Question 1: Implementation Approach

- [x] **RESOLVED:** Option B (Helper Method)

**Option A: Inline Logic (simpler)**
- Pros: Simple, no new methods, fewer lines of code
- Cons: Slightly verbose inline conditional logic
- Code: ~10 lines replacing line 426

**Option B: Helper Method (cleaner)**
- Pros: Clean, testable in isolation, self-documenting, reusable
- Cons: Adds one new method (~20 lines total)
- Code: New `_position_matches_ideal()` method + 1-line call at line 426

**Context:** Both achieve the same result. Option B is slightly more code but cleaner architecture.

**My recommendation:** Option B (helper method) - More maintainable, easier to test, clearer intent.

**What do you prefer?**

---

### Question 2: Test Coverage Level

- [x] **RESOLVED:** Option C (Comprehensive)

**Option A: Minimal (regression test only)**
- Add 1 test: Full roster (15 players) matches correctly
- Pros: Fastest to implement, proves bug is fixed
- Cons: Less coverage of edge cases

**Option B: Moderate (core scenarios)**
- Add 3 tests:
  1. RB matches RB-ideal round
  2. WR matches WR-ideal round
  3. Full roster (15 players) matches correctly
- Pros: Good coverage, reasonable effort
- Cons: Doesn't test all edge cases

**Option C: Comprehensive (all scenarios)**
- Add 6-7 tests covering all scenarios in spec.md
- Pros: Maximum coverage, prevents future regressions
- Cons: More time to implement

**Context:** Existing tests cover some scenarios. New tests would add specific coverage for the bug fix.

**My recommendation:** Option B (Moderate) - Balances coverage with effort. Can add more tests later if needed.

**What level of test coverage do you want?**

---

### Question 3: Integration Test with Actual Data

- [x] **RESOLVED:** Option A (Yes, create integration test)

**Option A: Yes, create integration test**
- Use your 15-player roster as test fixture
- Verify exact round assignments match expected
- Pros: Tests real-world scenario, prevents regression
- Cons: Test data maintenance (if roster changes)

**Option B: No, unit tests are sufficient**
- Rely on unit tests with synthetic data
- Manual smoke testing during Stage 5c
- Pros: Simpler, less maintenance
- Cons: Less confidence in real-world scenario

**Context:** Your bug report included specific roster data showing the issue. We could use that as a test fixture.

**My recommendation:** Option A (Yes) - High value for minimal effort, ensures real scenario works.

**Do you want an integration test with your actual roster data?**

---

### Question 4: FLEX-Eligible Positions Verification

- [x] **RESOLVED:** Standard configuration (RB, WR only)

**Standard configuration:**
```json
"FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"]
```

**Non-standard examples:**
```json
"FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "TE"]  // TE also FLEX-eligible
"FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "DST"]  // DST also FLEX-eligible
```

**Context:** The fix automatically handles any positions in `FLEX_ELIGIBLE_POSITIONS`, but I want to confirm your configuration so tests use the right setup.

**What positions are FLEX-eligible in your league?** (check your `league_config.json`)

---

### Question 5: Documentation Updates

- [x] **RESOLVED:** Option A (Minimal comments - docstring only)

**Option A: Minimal comments (code is self-explanatory)**
- Only add docstring for helper method (if Option B)
- Rely on method names and structure for clarity

**Option B: Detailed comments**
- Add comments explaining why FLEX matching works this way
- Document the bug that was fixed
- Add examples in comments

**Context:** Code will be clear from method names and docstrings. Additional comments could help future developers understand the FLEX logic.

**My recommendation:** Option A (Minimal) - If we use helper method (Option B from Question 1), the docstring + method name make intent very clear.

**How much inline documentation do you want?**

---

## Resolved Questions

### Question 1: Implementation Approach
- [x] **RESOLVED:** Option B (Helper Method)

**User's Answer:** "B" (2025-12-31)

**Implementation Impact:**
- Create new `_position_matches_ideal()` helper method (~20 lines)
- Add comprehensive docstring with examples
- Replace line 426 with single method call
- Method will be testable in isolation (Test 6 in spec.md)
- Total code addition: ~21 lines

---

### Question 2: Test Coverage Level
- [x] **RESOLVED:** Option C (Comprehensive)

**User's Answer:** "C" (2025-12-31)
**User's Rationale:** "This is one of the most key parts of this project and deserves the time and energy to validate the behavior"

**Implementation Impact:**
- Add 6-7 comprehensive tests (Tests 1-6 mandatory, Test 7 pending Question 3)
- Test 1: RB matches RB-ideal round
- Test 2: WR matches WR-ideal round
- Test 3: RB/WR still match FLEX rounds
- Test 4: QB/TE/K/DST exact match only (unchanged behavior)
- Test 5: Full roster (15 players) regression test
- Test 6: Helper method `_position_matches_ideal()` unit tests (all logic paths)
- Test 7: Integration test with actual user data (TBD)
- Estimated test code: ~150-200 lines
- Maximum confidence in fix correctness

---

### Question 3: Integration Test with Actual Data
- [x] **RESOLVED:** Option A (Yes, create integration test)

**User's Answer:** "Yes" (2025-12-31)

**Implementation Impact:**
- Create Test 7: Integration test with actual 15-player roster from bug report
- Test fixture: User's exact roster data showing the bug
- Verification: All 15 players correctly assigned to expected rounds
- **Value:** Tests the real-world scenario that exposed the bug
- Prevents regression on user's specific league configuration
- Estimated additional test code: ~50-80 lines (including fixture setup)
- **Total test code estimate:** ~200-280 lines (Tests 1-7)

---

### Question 4: FLEX-Eligible Positions Verification
- [x] **RESOLVED:** Standard configuration (RB, WR only)

**User's Answer:** "Standard RB and WR" (2025-12-31)

**Configuration Confirmed:**
```json
"FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"]
```

**Implementation Impact:**
- Tests will use standard RB/WR as FLEX-eligible positions
- No special handling needed for TE or DST in FLEX
- Helper method `_position_matches_ideal()` will check against `["RB", "WR"]`
- Test fixtures will use RB/WR for FLEX scenarios
- Edge case tests (Test 3) will verify RB/WR can match FLEX rounds

---

### Question 5: Documentation Updates
- [x] **RESOLVED:** Option A (Minimal comments - docstring only)

**User's Answer:** "A" (2025-12-31)

**Implementation Impact:**
- Comprehensive docstring for `_position_matches_ideal()` helper method
- Docstring includes: description, FLEX-eligible vs non-FLEX logic explanation, Args, Returns, 5 examples
- No additional inline comments beyond docstring
- Code is self-documenting through clear method names and structure
- **Rationale:** Helper method name + docstring provide sufficient context

---

## Additional Scope Discovered

**None** - Scope matches initial epic request. No new work discovered during deep dive.

---

## Checklist Summary

**Total Questions:** 5
**Resolved:** 5 ✅ **ALL COMPLETE**
**Pending:** 0

**Status:** ✅ All questions resolved - Ready for Phase 4 (Scope Adjustment)

---

## Notes

**Critical Decision:** Question 1 (implementation approach) blocks implementation. Must be resolved first.

**Testing Decisions:** Questions 2-3 affect test implementation but don't block spec completion.

**Configuration Verification:** Question 4 is informational - fix works regardless, but answer helps with test setup.

**Documentation:** Question 5 is low priority - can decide during implementation if needed.

---

**Last Updated:** 2025-12-31 16:15
**Phase:** 2 (Spec & Checklist) - Questions created, waiting for Phase 3
