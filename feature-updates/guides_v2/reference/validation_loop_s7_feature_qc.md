# Validation Loop: S7 Feature QC

**Extends:** Master Validation Loop Protocol
**See:** `reference/validation_loop_master_protocol.md`

**Applicable Stages:**
- S7.P2: Feature QC Rounds (post-implementation quality validation)

**Version:** 2.0 (Created to extend master protocol)
**Last Updated:** 2026-02-10

---

## Table of Contents

1. [Overview](#overview)
2. [Master Dimensions (7) - Always Checked](#master-dimensions-7---always-checked)
3. [S7 Feature QC Dimensions (5) - Context-Specific](#s7-feature-qc-dimensions-5---context-specific)
4. [Total Dimensions: 12](#total-dimensions-12)
5. [What's Being Validated](#whats-being-validated)
6. [Fresh Eyes Patterns Per Round](#fresh-eyes-patterns-per-round)
7. [Common Issues in S7 QC Context](#common-issues-in-s7-qc-context)
8. [Exit Criteria](#exit-criteria)
9. [Integration with S7](#integration-with-s7)

---

## Overview

**Purpose:** Validate implemented feature quality before final review and commit

**What this validates:**
- Completed feature implementation (post-S6 execution)
- Feature meets all spec requirements
- Integration with existing features works
- Code quality and consistency
- End-to-end functionality

**Quality Standard:**
- 100% requirements implemented
- All integration points work correctly
- Zero critical bugs
- Code follows project standards
- Ready for S7.P3 (Final Review)

**Uses:** All 7 master dimensions + 5 S7 QC-specific dimensions = 12 total

---

## Master Dimensions (7) - Always Checked

**See `reference/validation_loop_master_protocol.md` for complete checklists.**

These universal dimensions apply to S7 Feature QC validation:

### Dimension 1: Empirical Verification
- [ ] All interface contracts verified from actual source code
- [ ] All integration points verified to exist (file:line references)
- [ ] All test commands verified to work (100% pass rate confirmed)
- [ ] All spec requirements traced to actual implementation (file:line)

### Dimension 2: Completeness
- [ ] All spec.md requirements implemented (100% coverage)
- [ ] All implementation_plan.md tasks completed
- [ ] All integration points implemented
- [ ] All error handling implemented
- [ ] All edge cases handled

### Dimension 3: Internal Consistency
- [ ] No contradictions between implementation and spec
- [ ] No contradictions between implementation and implementation_plan
- [ ] Naming conventions consistent throughout feature
- [ ] Error handling approach consistent throughout
- [ ] Coding patterns consistent with project standards

### Dimension 4: Traceability
- [ ] Every implemented function traces to spec requirement
- [ ] Every test traces to requirement or acceptance criteria
- [ ] All integration points documented with source/destination
- [ ] No orphan code (code without requirement justification)

### Dimension 5: Clarity & Specificity
- [ ] No vague error messages ("Error occurred" → "FileNotFoundError: adp.csv not found in data/rankings/")
- [ ] Specific logging (includes context, not just "Processing item")
- [ ] Clear function names (behavior obvious from name)
- [ ] Specific acceptance criteria verification (not "works well")

### Dimension 6: Upstream Alignment
- [ ] Implementation matches spec.md exactly (no deviations without justification)
- [ ] Implementation matches implementation_plan.md approach
- [ ] All original goals from spec achieved
- [ ] All acceptance criteria met
- [ ] No scope creep (no unrequested functionality)

### Dimension 7: Standards Compliance
- [ ] Follows project coding standards (CODING_STANDARDS.md)
- [ ] Follows project structure/organization
- [ ] Uses project utilities (LoggingManager, csv_utils, etc.)
- [ ] Import organization correct (standard, third-party, local)
- [ ] Error handling follows project patterns

---

## S7 Feature QC Dimensions (5) - Context-Specific

These 5 dimensions are specific to S7.P2 Feature QC validation:

### Dimension 8: Cross-Feature Integration

**Question:** Does this feature integrate correctly with existing features?

**Checklist:**

**Integration Point Verification:**
- [ ] All integration points identified (which features this feature calls/is called by)
- [ ] All interface contracts verified (method signatures match expectations)
- [ ] Data flow verified (data passed between features has correct format/structure)
- [ ] Error propagation tested (errors from downstream features handled correctly)

**Data Exchange:**
- [ ] Data structures compatible (no format mismatches)
- [ ] Data validation present at boundaries (input from other features validated)
- [ ] Data transformation correct (if needed between features)
- [ ] Shared resources accessed correctly (config, data files, etc.)

**Timing/Sequencing:**
- [ ] Call order correct (dependencies called before dependent code)
- [ ] No race conditions (if async operations present)
- [ ] State management correct (shared state updated consistently)

**Common Violations:**

❌ **WRONG - Integration not verified:**
```python
# Feature 1 calls Feature 2's method
result = feature2.process_data(player_data)
# Assumed feature2.process_data() returns dict
# Actually returns tuple → TypeError at runtime
```

✅ **CORRECT - Integration verified:**
```python
# Verified from feature2/processor.py:45
# def process_data(self, data: dict) -> Tuple[int, str]:
#     return (score, status)

result = feature2.process_data(player_data)
score, status = result  # Correctly unpacks tuple
```

---

### Dimension 9: Error Handling Completeness

**Question:** Are all error scenarios handled gracefully?

**Checklist:**

**File/Resource Errors:**
- [ ] FileNotFoundError handled (all file operations)
- [ ] PermissionError handled (file/directory access)
- [ ] IOError handled (read/write failures)
- [ ] Resource cleanup in finally blocks (file handles, connections)

**Data Quality Errors:**
- [ ] ValueError handled (invalid data types, out-of-range values)
- [ ] KeyError handled (missing dictionary keys, config values)
- [ ] TypeError handled (wrong types passed to functions)
- [ ] Empty data handled (empty list, empty string, None)

**Integration Errors:**
- [ ] Downstream feature errors caught and handled
- [ ] API errors handled (if external APIs used)
- [ ] Timeout errors handled (if async operations)
- [ ] Partial failure handled (some operations succeed, some fail)

**Error Response:**
- [ ] All errors logged with context (what was being attempted, what failed)
- [ ] User-facing errors have clear messages (not stack traces)
- [ ] Error recovery attempted where possible (fallback values, retry logic)
- [ ] Critical errors escalated appropriately (not silently swallowed)

**Common Violations:**

❌ **WRONG - Error not handled:**
```python
def load_player_data():
    with open('data/players.csv', 'r') as f:
        return csv.reader(f)
# FileNotFoundError crashes entire program
```

✅ **CORRECT - Error handled gracefully:**
```python
def load_player_data():
    try:
        with open('data/players.csv', 'r') as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        logger.error("players.csv not found in data/ directory")
        return []  # Return empty list, allow program to continue
    except PermissionError:
        logger.error("Permission denied reading players.csv")
        raise  # Re-raise critical error
```

---

### Dimension 10: End-to-End Functionality

**Question:** Does the complete user flow work correctly?

**Checklist:**

**User Flow Completeness:**
- [ ] Entry point works (CLI flag, menu option, API endpoint)
- [ ] Main flow completes successfully (happy path end-to-end)
- [ ] Exit point works (results displayed, files written, state saved)
- [ ] User feedback provided (progress indicators, completion messages)

**Edge Case Coverage:**
- [ ] Minimum input works (empty list, single item)
- [ ] Maximum input works (large datasets, boundary values)
- [ ] Invalid input handled (wrong format, missing required fields)
- [ ] Duplicate input handled (repeated operations, re-running)

**Data Persistence:**
- [ ] State saved correctly (if feature maintains state)
- [ ] State loaded correctly (if resuming from saved state)
- [ ] Old data format still works (backward compatibility)
- [ ] New data format documented (if changed)

**Performance:**
- [ ] Reasonable performance on expected data volumes
- [ ] No obvious bottlenecks (O(n²) algorithms on large data)
- [ ] Memory usage acceptable (no loading entire dataset unnecessarily)
- [ ] Timeout handling (if long-running operations)

**Common Violations:**

❌ **WRONG - Incomplete flow:**
```python
# User runs command → code executes → no output
# User doesn't know if it succeeded or failed
```

✅ **CORRECT - Complete flow:**
```python
print("Loading player data...")
players = load_players()
print(f"Loaded {len(players)} players")

print("Processing trades...")
results = process_trades(players)
print(f"Processed {len(results)} trades")

save_results(results)
print(f"Results saved to {output_path}")
```

---

### Dimension 11: Test Coverage Quality

**Question:** Do tests adequately cover the implementation?

**Checklist:**

**Test Pass Rate:**
- [ ] All tests pass (100% pass rate - run `python tests/run_all_tests.py`)
- [ ] No skipped tests (all tests enabled and passing)
- [ ] No flaky tests (tests pass consistently, not intermittently)

**Coverage Adequacy:**
- [ ] All requirements have tests (from test_strategy.md)
- [ ] All edge cases have tests (boundary values, empty input, etc.)
- [ ] All error paths have tests (FileNotFoundError, ValueError, etc.)
- [ ] All integration points have tests (feature interactions tested)

**Test Quality:**
- [ ] Tests verify behavior (not just code coverage)
- [ ] Tests have clear pass/fail criteria (no subjective checks)
- [ ] Tests are isolated (no dependencies between tests)
- [ ] Test names describe what's being tested

**Integration Testing:**
- [ ] At least 3 integration tests with real objects (no mocks)
- [ ] End-to-end tests cover main user flow
- [ ] Cross-feature integration tested (if applicable)

**Common Violations:**

❌ **WRONG - Test failure ignored:**
```bash
$ python tests/run_all_tests.py
...
FAILED tests/test_trade.py::test_calculate_value
...
97 passed, 1 failed

# Agent proceeds to S7.P3 anyway ❌
```

✅ **CORRECT - All tests pass:**
```bash
$ python tests/run_all_tests.py
...
98 passed

# All tests passing, ready to proceed ✅
```

---

### Dimension 12: Requirements Completion

**Question:** Are ALL spec requirements fully implemented (zero tech debt)?

**Checklist:**

**Requirement Coverage:**
- [ ] Every spec.md requirement has implementation (100% coverage)
- [ ] Every implementation_checklist.md item verified
- [ ] No "TODO" comments in code
- [ ] No "temporary" solutions or workarounds
- [ ] No deferred features ("we'll add this later")

**Acceptance Criteria:**
- [ ] All acceptance criteria met (from spec.md and implementation_plan.md)
- [ ] All success criteria verified (can demonstrate feature works)
- [ ] All validation criteria pass (data validation, input validation)

**Completeness Verification:**
- [ ] Feature is production-ready (would ship to users)
- [ ] No partial implementations ("90% done" = not done)
- [ ] No scope cuts without user approval
- [ ] Zero tech debt introduced

**Documentation:**
- [ ] All public functions have docstrings
- [ ] Complex logic has explanatory comments
- [ ] ARCHITECTURE.md updated (if architecture changed)
- [ ] README.md updated (if user-facing changes)

**Common Violations:**

❌ **WRONG - Incomplete requirement:**
```markdown
Spec requirement: "Support CSV and JSON input formats"

Implementation: Only CSV supported, JSON TODO
❌ Incomplete - must implement both or get user approval to remove JSON
```

✅ **CORRECT - Complete requirement:**
```markdown
Spec requirement: "Support CSV and JSON input formats"

Implementation:
- CSV: load_from_csv() implemented and tested ✅
- JSON: load_from_json() implemented and tested ✅
- Both formats have integration tests ✅
```

---

## Total Dimensions: 12

**Every validation round checks ALL 12 dimensions:**
- 7 Master dimensions (universal)
- 5 S7 Feature QC dimensions (context-specific)

**Process:** See master protocol for 3 consecutive clean rounds requirement

---

## What's Being Validated

### S7.P2: Feature QC Rounds

**Artifact:** Implemented feature code (post-S6 execution)

**Validates:**
- Feature implementation completeness
- Integration with existing features
- Error handling robustness
- End-to-end functionality
- Test coverage adequacy
- Requirements fulfillment

**Success Criteria:**
- 100% requirements implemented
- 100% tests passing
- All integration points work
- Zero critical bugs
- Ready for S7.P3 (Final Review)

---

## Fresh Eyes Patterns Per Round

**See master protocol for general fresh eyes principles.**

S7 Feature QC-specific reading patterns:

### Round 1: Sequential Code Review + Test Verification

**Pattern:**
1. Run ALL tests first (`python tests/run_all_tests.py`)
2. Verify 100% pass rate (exit code 0)
3. Read implementation code sequentially (top to bottom, file by file)
4. Read spec.md in parallel (verify requirements covered)
5. Check all 12 dimensions systematically
6. Document ALL issues found

**Checklist:**
- [ ] All 12 dimensions checked (7 master + 5 S7 QC)
- [ ] All tests passing (100% pass rate)
- [ ] All spec requirements implemented
- [ ] Integration points verified
- [ ] Error handling present

**Document findings in VALIDATION_LOOP_LOG.md**

---

### Round 2: Reverse Code Review + Integration Focus

**Pattern:**
1. Re-run ALL tests (verify still passing)
2. Read implementation code in reverse order (bottom to top, last file to first)
3. Focus on integration points (feature boundaries)
4. Trace data flow across features
5. Verify error propagation
6. Check all 12 dimensions systematically

**Focus Areas:**
- Dimension 8 (Cross-Feature Integration) - primary focus
- Dimension 9 (Error Handling) - verify error paths
- All master dimensions - continue checking

**Checklist:**
- [ ] All 12 dimensions checked
- [ ] Integration verified (data flow correct, interfaces match)
- [ ] Error handling comprehensive
- [ ] No new issues from fixes

---

### Round 3: Random Spot-Checks + E2E Verification

**Pattern:**
1. Re-run ALL tests (final verification)
2. Random spot-check 5-7 functions/classes
3. End-to-end flow verification (trace from CLI to output)
4. Performance check (acceptable on expected data volumes)
5. Check all 12 dimensions systematically

**Focus Areas:**
- Dimension 10 (End-to-End Functionality) - primary focus
- Dimension 11 (Test Coverage Quality) - verify comprehensive
- Dimension 12 (Requirements Completion) - final check

**Checklist:**
- [ ] All 12 dimensions checked
- [ ] E2E flow works correctly
- [ ] Performance acceptable
- [ ] All requirements 100% complete

---

## Common Issues in S7 QC Context

### Issue 1: Integration Point Mismatch

**Problem:** Feature calls another feature's method with wrong parameters

❌ **WRONG:**
```python
# Feature A calls Feature B
result = feature_b.calculate_score(player_name)
# But Feature B expects: calculate_score(player_id: int)
# TypeError at runtime
```

✅ **CORRECT:**
```python
# Verified from feature_b/scorer.py:123
# def calculate_score(self, player_id: int) -> float:

player_id = self.get_player_id(player_name)
result = feature_b.calculate_score(player_id)  # Correct type
```

---

### Issue 2: Missing Error Handling

**Problem:** Error case not handled, causing crash

❌ **WRONG:**
```python
data = json.load(open('config.json'))
# If config.json doesn't exist → FileNotFoundError → crash
```

✅ **CORRECT:**
```python
try:
    with open('config.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    logger.error("config.json not found, using defaults")
    data = get_default_config()
except json.JSONDecodeError:
    logger.error("config.json is malformed")
    raise
```

---

### Issue 3: Incomplete E2E Flow

**Problem:** Feature works but user has no feedback

❌ **WRONG:**
```python
def run_analysis():
    results = analyze_players()
    save_results(results)
    # User sees nothing, doesn't know if it worked
```

✅ **CORRECT:**
```python
def run_analysis():
    print("Starting player analysis...")
    results = analyze_players()
    print(f"Analyzed {len(results)} players")

    save_results(results)
    print(f"Results saved to {RESULTS_FILE}")
    print("Analysis complete!")
```

---

### Issue 4: Test Failure Not Blocking

**Problem:** Agent proceeds despite failing tests

❌ **WRONG:**
```bash
$ python tests/run_all_tests.py
...
45 passed, 2 failed

# Agent: "Most tests pass, proceeding to S7.P3" ❌
```

✅ **CORRECT:**
```bash
$ python tests/run_all_tests.py
...
45 passed, 2 failed

# Agent: "2 tests failing, must fix before proceeding"
# Fix both test failures
# Re-run tests → 47 passed ✅
# Now ready to proceed
```

---

### Issue 5: Partial Implementation

**Problem:** Requirement only partially implemented

❌ **WRONG:**
```markdown
Spec: "Support filtering by position (QB, RB, WR, TE)"

Implementation: Only QB and RB implemented
"Will add WR and TE later" ← NOT ACCEPTABLE
```

✅ **CORRECT:**
```markdown
Spec: "Support filtering by position (QB, RB, WR, TE)"

Implementation:
- QB filtering: ✅ Implemented and tested
- RB filtering: ✅ Implemented and tested
- WR filtering: ✅ Implemented and tested
- TE filtering: ✅ Implemented and tested
All positions supported ✅
```

---

## Exit Criteria

**S7 Feature QC validation is COMPLETE when ALL of the following are true:**

**From Master Protocol:**
- [ ] 3 consecutive rounds with ZERO issues found
- [ ] All 7 master dimensions checked every round
- [ ] All 5 S7 QC dimensions checked every round
- [ ] Validation log complete with all rounds documented

**S7 QC Specific:**
- [ ] All tests passing (100% pass rate, verified every round)
- [ ] All spec requirements implemented (100% coverage)
- [ ] All integration points verified and working
- [ ] All error scenarios handled gracefully
- [ ] End-to-end flow works correctly
- [ ] Test coverage adequate (>90% line coverage)
- [ ] Zero tech debt (no TODOs, no partial implementations)
- [ ] Ready for S7.P3 (Final Review)

**Cannot exit if:**
- ❌ Any tests failing
- ❌ Any spec requirement not implemented
- ❌ Any integration point broken
- ❌ Any critical errors not handled
- ❌ Any incomplete implementations

---

## Integration with S7

### S7.P2: Feature QC Rounds

**When:** After S7.P1 (Smoke Testing) passes, after S6 (Execution) complete

**Validates:** Implemented feature code

**Process:**
1. Use this validation loop protocol
2. Check all 12 dimensions (7 master + 5 S7 QC)
3. Exit when 3 consecutive clean rounds
4. Proceed to S7.P3 (Final Review)

**Replaces:** Old sequential 3-round QC with restart protocol

**Key Difference:**
- **Old:** Round 1 (Integration) → Round 2 (Consistency) → Round 3 (Success) → Any issue → RESTART from beginning
- **New:** Check ALL concerns EVERY round → Fix issues immediately → Continue validation until 3 consecutive clean

---

## Example Validation Round Sequence

```text
Round 1: Sequential + Test Verification
- Run tests: 2 failures (test_trade_validation, test_edge_case)
- Fix: Debug and fix both test failures
- Re-run tests: All pass ✅
- Sequential code review: Found integration point mismatch (Feature B interface)
- Fix: Update call to feature_b.calculate_score() with correct parameter type
- Check all 12 dimensions
- Issues found: 3 total
- Clean counter: 0

Round 2: Reverse + Integration Focus
- Run tests: All pass ✅
- Reverse code review: Found missing error handling (FileNotFoundError)
- Fix: Add try/except with fallback
- Integration focus: Traced data flow F1→F2→F3, all correct
- Check all 12 dimensions
- Issues found: 1 total
- Clean counter: 0

Round 3: Spot-Checks + E2E
- Run tests: All pass ✅
- Random spot-checks: 6 functions checked, all correct
- E2E verification: Traced from CLI to output, complete flow works
- Check all 12 dimensions
- Issues found: 0 ✅
- Clean counter: 1

Round 4: Repeat Validation
- Run tests: All pass ✅
- Fresh eyes, different reading pattern
- Check all 12 dimensions
- Issues found: 0 ✅
- Clean counter: 2

Round 5: Final Sweep
- Run tests: All pass ✅
- Complete re-read of implementation
- Check all 12 dimensions
- Issues found: 0 ✅
- Clean counter: 3 → VALIDATION COMPLETE ✅

Total: 5 rounds, 4 issues fixed, 3 consecutive clean rounds achieved
Ready for S7.P3 (Final Review)
```

---

## Summary

**S7 Feature QC Validation Loop:**
- **Extends:** Master Validation Loop Protocol (7 universal dimensions)
- **Adds:** 5 S7 QC-specific dimensions
- **Total:** 12 dimensions checked every round
- **Process:** 3 consecutive clean rounds required
- **Exit:** 100% tests passing, 100% requirements implemented, all integration verified
- **Quality:** Zero tech debt, ready for production

**Key Principle:**
> "Every implemented feature must pass comprehensive quality validation (functionality, integration, error handling, testing, completeness) through 3 consecutive clean validation rounds before proceeding to final review."

**Key Difference from Old Approach:**
- **Old:** Sequential rounds checking different concerns → Any issue → Restart from beginning
- **New:** All concerns checked every round → Fix immediately → Continue until 3 consecutive clean

**Time Savings:** 60-180 minutes per bug (eliminates restart overhead)

---

*End of S7 Feature QC Validation Loop v2.0*
