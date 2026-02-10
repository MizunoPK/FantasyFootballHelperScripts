# Validation Loop: QC and PR Review

**Extends:** Master Validation Loop Protocol
**See:** `reference/validation_loop_master_protocol.md`

**Applicable Stages:**
- S7.P2: Feature QC Rounds (3 rounds post-smoke testing)
- S7.P3: Feature PR Review (final review before commit)
- S9.P2: Epic QC Rounds (3 rounds post-epic smoke testing)
- S10.P2: Final PR Review (epic-level)

**Version:** 2.0 (Updated to extend master protocol)
**Last Updated:** 2026-02-10

---

## What's Being Validated

Code, tests, and implementation correctness including:
- Source code matches implementation plan
- All tests pass (100% pass rate)
- No bugs found during review
- All requirements implemented
- Integration points work correctly
- Code quality and maintainability

---

## What Counts as "Issue"

An issue in QC/PR context is any of:
- **Test failures:** Any test fails (unit, integration, or end-to-end)
- **Code not matching plan:** Implementation deviates from implementation_plan.md without justification
- **Bugs found during review:** Logic errors, edge cases not handled, incorrect behavior
- **Missing requirements:** Requirement in spec.md not implemented
- **Integration problems:** Integration points don't work as specified
- **Code quality issues:** Hard-coded values, missing error handling, poor naming
- **Performance issues:** Code performs poorly on expected data volumes
- **Security issues:** Vulnerabilities introduced (SQL injection, XSS, etc.)

---

## Fresh Eyes Patterns Per Round

### Round 1: Automated Tests + Sequential Code Review
**Pattern:**
1. Run ALL tests (unit, integration, end-to-end)
2. Verify 100% pass rate
3. Read code files sequentially (alphabetical or logical order)
4. Check code matches implementation plan
5. Check for obvious bugs (null checks, error handling, etc.)
6. Document ALL issues found

**Checklist:**
- [ ] All tests pass (100% pass rate)
- [ ] Code matches implementation_plan.md
- [ ] All requirements from spec.md implemented
- [ ] Error handling present for all failure scenarios
- [ ] No hard-coded values (use config/constants)

### Round 2: Different File Order + Manual Verification
**Pattern:**
1. Re-run ALL tests (verify still 100% pass)
2. Read code files in different order (reverse, by module, by dependency, etc.)
3. Manual verification of critical logic paths
4. Check integration points work correctly
5. Check for edge cases not covered by tests
6. Document ALL issues found

**Checklist:**
- [ ] Tests still pass after code review
- [ ] Critical logic verified manually
- [ ] Integration points work as specified
- [ ] Edge cases handled correctly
- [ ] No code quality issues (naming, structure, etc.)

### Round 3: Random Spot-Checks + Integration Verification
**Pattern:**
1. Re-run ALL tests (final verification)
2. Random spot-check 5 files or functions
3. End-to-end integration verification (call stack traced)
4. Performance check (expected data volumes)
5. Security check (common vulnerabilities)
6. Document ALL issues found

**Checklist:**
- [ ] Random spot-checks reveal no issues
- [ ] End-to-end integration works correctly
- [ ] Performance acceptable on expected data
- [ ] No security vulnerabilities found
- [ ] Ready for commit/PR

---

## Specific Criteria

**All of these MUST pass for loop to exit:**

**Code Correctness:**
- [ ] All tests pass (100% pass rate)
- [ ] Code matches implementation_plan.md (or justified deviations documented)
- [ ] All requirements from spec.md implemented
- [ ] No bugs found during review
- [ ] Integration points work correctly

**Code Quality:**
- [ ] Error handling present for all failure scenarios
- [ ] No hard-coded values (use config/constants)
- [ ] Clear variable/function naming
- [ ] No code duplication (DRY principle)
- [ ] Logging present for debugging

**Performance & Security:**
- [ ] Performance acceptable on expected data volumes
- [ ] No security vulnerabilities (SQL injection, XSS, etc.)
- [ ] Resource cleanup (file handles, connections, etc.)

**Documentation:**
- [ ] Code comments for complex logic
- [ ] Docstrings for public functions
- [ ] README updated if needed

---

## Example Round Sequence

```text
Round 1: Automated tests + sequential review
- Run tests: 2 tests fail (test_player_fetch, test_trade_validation)
- Fix: Debug and fix both test failures
- Sequential review: Found hard-coded API key in fetcher.py
- Fix: Move API key to config file
- Continue to Round 2

Round 2: Different order + manual verification
- Run tests: All pass (100% pass rate)
- Review in reverse order: Found missing error handling in optimizer.py
- Fix: Add try/except with proper error logging
- Manual verification: Integration point F1→F2 returns wrong data type
- Fix: Add type conversion in F1's output
- Continue to Round 3

Round 3: Random spot-checks + integration
- Run tests: All pass (100% pass rate)
- Random spot-check 5 functions: 0 issues found
- Integration verification: End-to-end call stack works correctly
- Check: 0 issues found → Continue (count = 1 clean)

Round 4: Repeat validation
- Run tests: All pass
- Check: 0 issues found → Continue (count = 2 clean)

Round 5: Final sweep
- Run tests: All pass
- Check: 0 issues found → PASSED (count = 3 consecutive clean)
```

---

## Common Issues in QC/PR Context

1. **Test failures:** Tests fail → Debug and fix code or test
2. **Code not matching plan:** Implementation uses approach X, plan specified approach Y → Align with plan or document justification
3. **Missing error handling:** Function doesn't handle null input → Add error handling
4. **Hard-coded values:** API URL hard-coded → Move to config
5. **Integration problems:** F1 calls F2 but F2 expects different parameters → Fix interface
6. **Performance issues:** Code loads entire 10GB file into memory → Use streaming
7. **Security issues:** User input not sanitized → Add input validation

---

## Integration with Stages

**S7.P2 QC Rounds (Feature-Level):**
- Use this protocol after implementation complete
- 3 QC rounds required (embedded Validation Loop)
- Must pass before S7.P3 (PR Review)

**S7.P3 PR Review (Feature-Level):**
- Use this protocol for final pre-commit review
- Verify ALL issues from S7.P2 fixed
- Must pass before feature commit

**S9.P2 Epic QC Rounds (Epic-Level):**
- Use this protocol after all features complete
- 3 QC rounds across entire epic codebase
- Must pass before S9.P3 (User Testing)

---

## Exit Criteria Specific to QC/PR

**Can only exit when ALL true:**
- [ ] 3 consecutive rounds found zero issues
- [ ] All tests pass (100% pass rate)
- [ ] Code matches implementation plan
- [ ] All requirements implemented
- [ ] Integration points work
- [ ] No bugs found during review
- [ ] Code quality acceptable
- [ ] Ready for commit (S7.P3) or user testing (S9.P3)

---

## Special Handling: Restart Protocol

**CRITICAL:** If ANY issues found in ANY round:

1. **Fix ALL issues immediately** (no deferring)
2. **Re-run ALL tests** to verify fixes didn't break anything
3. **Restart from Round 1** (not mid-QC)
   - Fixes can introduce new issues
   - Fresh perspective required after fixes
   - Reset counter to 0
4. **Continue until 3 consecutive clean rounds**

**Why restart from Round 1:**
- Fixing Issue A can introduce Issue B
- Fresh eyes needed to catch fix-induced issues
- Cannot guarantee quality by spot-checking only fixed areas
- Historical evidence: 40% of fixes introduce new issues

**Example:**
```bash
Round 1: 5 issues → Fix ALL → Restart
Round 1 (again): 2 issues (1 original missed, 1 introduced by fix) → Fix ALL → Restart
Round 1 (again): 0 issues → Round 2 (count = 1 clean)
Round 2: 0 issues → Round 3 (count = 2 clean)
Round 3: 0 issues → PASSED (count = 3 consecutive clean)
```

---

**Remember:** Follow all 7 principles from master protocol. This guide only specifies HOW to apply them in QC/PR context, not WHETHER to apply them.
