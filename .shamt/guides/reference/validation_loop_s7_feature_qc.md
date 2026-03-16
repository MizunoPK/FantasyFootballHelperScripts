# Validation Loop: S7 Feature QC

**Extends:** Master Validation Loop Protocol
**See:** `reference/validation_loop_master_protocol.md`

**Applicable Stages:**
- S7.P2: Feature Validation Loop (post-implementation quality validation)

**Version:** 2.1
**Last Updated:** 2026-03-07

---

🚨 **BEFORE STARTING: Read the Hard Stop section at the top of `reference/validation_loop_master_protocol.md`** 🚨

---

## Table of Contents

1. [Overview](#overview)
2. [Master Dimensions (7) - Always Checked](#master-dimensions-7---always-checked)
3. [S7 Feature QC Dimensions (9) - Context-Specific](#s7-feature-qc-dimensions-9---context-specific)
4. [Total Dimensions: 16](#total-dimensions-16)
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

**Uses:** All 7 master dimensions + 9 S7 QC-specific dimensions = 16 total

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
- [ ] No vague error messages ("Error occurred" → "FileNotFoundError: priority.csv not found in data/rankings/")
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

## S7 Feature QC Dimensions (9) - Context-Specific

These 9 dimensions are specific to S7.P2 Feature QC validation:

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
## Feature 1 calls Feature 2's method
result = feature2.process_data(record_data)
## Assumed feature2.process_data() returns dict
## Actually returns tuple → TypeError at runtime
```

✅ **CORRECT - Integration verified:**
```python
## Verified from feature2/processor.py:45
## def process_data(self, data: dict) -> Tuple[int, str]:
##     return (score, status)

result = feature2.process_data(record_data)
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
def load_record_data():
    with open('data/items.csv', 'r') as f:
        return csv.reader(f)
## FileNotFoundError crashes entire program
```

✅ **CORRECT - Error handled gracefully:**
```python
def load_record_data():
    try:
        with open('data/items.csv', 'r') as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        logger.error("items.csv not found in data/ directory")
        return []  # Return empty list, allow program to continue
    except PermissionError:
        logger.error("Permission denied reading items.csv")
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
## User runs command → code executes → no output
## User doesn't know if it succeeded or failed
```

✅ **CORRECT - Complete flow:**
```python
print("Loading record data...")
items = load_players()
print(f"Loaded {len(items)} items")

print("Processing trades...")
results = process_trades(items)
print(f"Processed {len(results)} trades")

save_results(results)
print(f"Results saved to {output_path}")
```

---

### Dimension 11: Test Coverage Quality

**Question:** Do tests adequately cover the implementation?

**Checklist:**

**Test Pass Rate:**
- [ ] All tests pass (100% pass rate - run `{TEST_COMMAND}`)
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
$ {TEST_COMMAND}
...
FAILED tests/test_trade.py::test_calculate_value
...
97 passed, 1 failed

## Agent proceeds to S7.P3 anyway ❌
```

✅ **CORRECT - All tests pass:**
```bash
$ {TEST_COMMAND}
...
98 passed

## All tests passing, ready to proceed ✅
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

### Dimension 13: Import & Dependency Hygiene

**Question:** Are imports clean and dependencies correctly categorized?

**Checklist:**

- [ ] No unused imports in ANY changed file (grep for each import, verify it's referenced)
- [ ] Every new dependency in `pyproject.toml`/`package.json` is actually imported somewhere in `src/`
- [ ] Test-only deps (e.g., pytest, pytest-asyncio) are in `dev`/`optional` group, not main `[dependencies]`
- [ ] No stale imports left after refactoring (removed function → removed import)

**Quick check:** `ruff check --select F401 {changed_files}` or `npx tsc --noEmit --noUnusedLocals`

**Common Violations:**

❌ **WRONG — Stale import after refactoring:**
```python
from utils import process_image, resize_image  # resize_image was removed in refactor
```

✅ **CORRECT — Import matches usage:**
```python
from utils import process_image  # only import what's used
```

---

### Dimension 14: Cross-Layer & Type Consistency

**Question:** Do types and constants stay consistent across the full stack?

**Checklist:**

- [ ] Frontend TypeScript types mirror backend Pydantic model constraints exactly
  - Backend `Literal["jpeg", "png"]` → Frontend `"jpeg" | "png"` (NOT `string`)
  - Backend `int` with `Field(ge=0)` → Frontend with matching runtime validation
- [ ] Data flows through the FULL pipeline with consistent metadata (provider → route → response → storage → display)
- [ ] Frontend timeouts >= backend worst-case execution time (with buffer)
- [ ] Constants used in multiple modules are shared (single source of truth), not independently constructed
- [ ] UI copy uses consistent terminology per page (do not mix e.g. "Assets" and "Images")

**Common Violations:**

❌ **WRONG — Type widened in frontend:**
```typescript
interface GenerationRequest {
  format: string;  // should be "jpeg" | "png"
}
```

✅ **CORRECT — Type mirrors backend exactly:**
```typescript
interface GenerationRequest {
  format: "jpeg" | "png";
}
```

---

### Dimension 15: Input Validation & Path Safety

**Question:** Is all user-supplied input validated and are file paths safe?

**Checklist:**

- [ ] All user-addressable endpoints validate/allowlist inputs (no implicit `else: default`)
- [ ] Data integrity operations use strict mode (e.g., `base64.b64decode(data, validate=True)`)
- [ ] External data load functions (localStorage, API responses) validate individual entry shapes before use
- [ ] File paths are absolute or derived from `__file__` — NEVER relative to CWD
- [ ] `exc_info=True` in logging is only used inside `except` blocks
- [ ] Module-level side effects (`logging.basicConfig`, `load_dotenv`) are in entrypoints, not library modules

**Common Violations:**

❌ **WRONG — Path relative to CWD:**
```python
output_dir = Path("backend/temp_images")  # breaks if CWD changes
```

✅ **CORRECT — Path anchored to file location:**
```python
output_dir = Path(__file__).parent / "temp_images"
```

---

### Dimension 16: Test Stub Consistency

**Question:** Are mock/stub return values internally consistent with mock state?

**Checklist:**

- [ ] Mock return values match the state configured on the mock object
  - e.g., if `mock_output.output_format = "jpeg"`, then the save stub should return a `.jpeg` URL
- [ ] Assertions match what the real code would produce given the mock state (not hardcoded against an arbitrary value)

**Common Violations:**

❌ **WRONG — Stub returns value inconsistent with mock state:**
```python
mock_output.output_format = "jpeg"
mock_storage.save.return_value = "https://example.com/image.png"  # wrong extension
assert result.url.endswith(".png")  # passes but is wrong
```

✅ **CORRECT — Stub consistent with mock state:**
```python
mock_output.output_format = "jpeg"
mock_storage.save.return_value = "https://example.com/image.jpeg"
assert result.url.endswith(".jpeg")
```

---

## Total Dimensions: 16

**Every validation round checks ALL 16 dimensions:**
- 7 Master dimensions (universal)
- 9 S7 Feature QC dimensions (context-specific)

**Process:** See master protocol for 3 consecutive clean rounds requirement

---

## What's Being Validated

### S7.P2: Feature Validation Loop

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
1. Run ALL tests first (`{TEST_COMMAND}`)
2. Verify 100% pass rate (exit code 0)
3. Read implementation code sequentially (top to bottom, file by file)
4. Read spec.md in parallel (verify requirements covered)
5. Check all 16 dimensions systematically
6. Document ALL issues found

**Checklist:**
- [ ] All 16 dimensions checked (7 master + 9 S7 QC)
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
6. Check all 16 dimensions systematically

**Focus Areas:**
- Dimension 8 (Cross-Feature Integration) - primary focus
- Dimension 9 (Error Handling) - verify error paths
- All master dimensions - continue checking

**Checklist:**
- [ ] All 16 dimensions checked
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
5. Check all 16 dimensions systematically

**Focus Areas:**
- Dimension 10 (End-to-End Functionality) - primary focus
- Dimension 11 (Test Coverage Quality) - verify comprehensive
- Dimension 12 (Requirements Completion) - final check

**Checklist:**
- [ ] All 16 dimensions checked
- [ ] E2E flow works correctly
- [ ] Performance acceptable
- [ ] All requirements 100% complete

---

## Common Issues in S7 QC Context

### Issue 1: Integration Point Mismatch

**Problem:** Feature calls another feature's method with wrong parameters

❌ **WRONG:**
```python
## Feature A calls Feature B
result = feature_b.calculate_score(player_name)
## But Feature B expects: calculate_score(player_id: int)
## TypeError at runtime
```

✅ **CORRECT:**
```python
## Verified from feature_b/scorer.py:123
## def calculate_score(self, player_id: int) -> float:

player_id = self.get_player_id(player_name)
result = feature_b.calculate_score(player_id)  # Correct type
```

---

### Issue 2: Missing Error Handling

**Problem:** Error case not handled, causing crash

❌ **WRONG:**
```python
data = json.load(open('config.json'))
## If config.json doesn't exist → FileNotFoundError → crash
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
    print("Starting item analysis...")
    results = analyze_players()
    print(f"Analyzed {len(results)} items")

    save_results(results)
    print(f"Results saved to {RESULTS_FILE}")
    print("Analysis complete!")
```

---

### Issue 4: Test Failure Not Blocking

**Problem:** Agent proceeds despite failing tests

❌ **WRONG:**
```bash
$ {TEST_COMMAND}
...
45 passed, 2 failed

## Agent: "Most tests pass, proceeding to S7.P3" ❌
```

✅ **CORRECT:**
```bash
$ {TEST_COMMAND}
...
45 passed, 2 failed

## Agent: "2 tests failing, must fix before proceeding"
## Fix both test failures
## Re-run tests → 47 passed ✅
## Now ready to proceed
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
- [ ] 3 consecutive rounds with ZERO issues found, OR user opted to stop at the 2-round checkpoint (see master protocol Exit Criteria)
- [ ] All 7 master dimensions checked every round
- [ ] All 9 S7 QC dimensions checked every round
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

### S7.P2: Feature Validation Loop

**When:** After S7.P1 (Smoke Testing) passes, after S6 (Execution) complete

**Validates:** Implemented feature code

**Process:**
1. Use this validation loop protocol
2. Check all 16 dimensions (7 master + 9 S7 QC)
3. Exit when 3 consecutive clean rounds
4. Proceed to S7.P3 (Final Review)

**Replaces:** Old sequential 3-round QC with restart protocol

**Key Difference:**
- **Old:** Round 1 (Integration) → Round 2 (Consistency) → Round 3 (Success) → Any issue → RESTART from beginning
- **New:** Check ALL concerns EVERY round → Fix issues immediately → Continue validation until 3 consecutive clean

**Important:** S7.P2 uses fix-and-continue (NOT restart to S7.P1). The CLAUDE.md restart protocol applies to S7.P1 smoke testing only (Part N fails → restart from Part 1). If S7.P2 finds issues, fix immediately and continue — do NOT restart to S7.P1.

---

## Example Validation Round Sequence

```text
Round 1: Sequential + Test Verification
- Run tests: 2 failures (test_trade_validation, test_edge_case)
- Fix: Debug and fix both test failures
- Re-run tests: All pass ✅
- Sequential code review: Found integration point mismatch (Feature B interface)
- Fix: Update call to feature_b.calculate_score() with correct parameter type
- Check all 16 dimensions
- Issues found: 3 total
- Clean counter: 0

Round 2: Reverse + Integration Focus
- Run tests: All pass ✅
- Reverse code review: Found missing error handling (FileNotFoundError)
- Fix: Add try/except with fallback
- Integration focus: Traced data flow F1→F2→F3, all correct
- Check all 16 dimensions
- Issues found: 1 total
- Clean counter: 0

Round 3: Spot-Checks + E2E
- Run tests: All pass ✅
- Random spot-checks: 6 functions checked, all correct
- E2E verification: Traced from CLI to output, complete flow works
- Check all 16 dimensions
- Issues found: 0 ✅
- Clean counter: 1

Round 4: Repeat Validation
- Run tests: All pass ✅
- Fresh eyes, different reading pattern
- Check all 16 dimensions
- Issues found: 0 ✅
- Clean counter: 2

Round 5: Final Sweep
- Run tests: All pass ✅
- Complete re-read of implementation
- Check all 16 dimensions
- Issues found: 0 ✅
- Clean counter: 3 → VALIDATION COMPLETE ✅

Total: 5 rounds, 4 issues fixed, 3 consecutive clean rounds achieved
Ready for S7.P3 (Final Review)
```

---

## Common False Negatives (Issues Missed in Insufficient Validation)

**Purpose:** Learn from historical validation failures to prevent recurrence

**Context:** This section was added after Feature 01 (field experience) revealed that initial validation rounds missed critical security vulnerabilities due to "checkbox validation" rather than rigorous investigation.

**Critical Lesson:** "Fresh eyes" validation must be GENUINE skepticism, not a perfunctory exercise.

---

### Security Vulnerabilities

**Why Easy to Miss:**
- Code "looks reasonable" on surface
- Requires thinking like an attacker (not just "does it work")
- Confirmation bias: "It works, so it must be secure"

**Common Missed Issues:**

**1. Path Traversal (File Serving)**
- **Symptom:** serve_file(filename) endpoint with no validation
- **Attack:** `GET /api/files/../../config/secrets.yaml`
- **Impact:** Read arbitrary files on server
- **Why Missed:** Agent focused on "Does it serve the file?" not "Can it serve wrong files?"
- **Prevention:** Always check filename validation + path resolution + boundary verification

**2. SQL Injection**
- **Symptom:** `query = f"SELECT * FROM users WHERE id = {user_id}"`
- **Attack:** user_id = "1 OR 1=1" → Returns all users
- **Impact:** Data breach
- **Why Missed:** Agent verified "query works" not "query is safe"
- **Prevention:** Always use parameterized queries, never string concatenation

**3. Command Injection**
- **Symptom:** `os.system(f"convert {user_filename} output.png")`
- **Attack:** user_filename = "input.jpg; rm -rf /"
- **Impact:** Server compromise
- **Why Missed:** Agent tested "normal filename" not "malicious filename"
- **Prevention:** Always use subprocess with list (not shell=True)

**Validation Approach to Catch These:**
- Ask: "What if user provides malicious input?"
- Check: Input validation present?
- Verify: Using safe APIs (parameterized queries, subprocess list)?
- Reference: Use `reference/security_checklist.md` for systematic security review

---

### Off-by-One Errors in Edge Cases

**Why Easy to Miss:**
- Code works for "normal" cases
- Off-by-one only manifests at boundaries
- Tests don't cover edge cases

**Common Missed Issues:**

**1. Array Indexing**
- **Symptom:** `for i in range(len(items) + 1): item = items[i]`
- **Bug:** IndexError on last iteration (items[len(items)] doesn't exist)
- **Why Missed:** Agent tested with small arrays, never hit boundary
- **Prevention:** Verify loop ranges match array bounds exactly

**2. Slice Operations**
- **Symptom:** `assets.splice(MAX_ENTRIES)` to keep items 0-9
- **Question:** Does it keep 10 items or 11?
- **Answer:** Keeps 10 (removes from index 10 onwards) ✅ CORRECT
- **Why Checked:** Agent verified with MAX_ENTRIES=10, indices 0-9 = 10 items
- **Prevention:** Manually trace slice boundaries with example indices

**3. Range Comparisons**
- **Symptom:** `if rank < 50:` vs `if rank <= 50:`
- **Question:** Is rank 50 included?
- **Why Missed:** Spec may say "top 50" (ambiguous: <50 or <=50?)
- **Prevention:** Verify against spec acceptance criteria explicitly

---

### Type Mismatches at Integration Boundaries

**Why Easy to Miss:**
- Python's dynamic typing masks type errors
- Type hints not always enforced
- Tests may coincidentally pass with wrong types

**Common Missed Issues:**

**1. Return Type Mismatch**
- **Symptom:** Feature A expects dict, Feature B returns tuple
- **Impact:** TypeError: 'tuple' object is not subscriptable
- **Why Missed:** Agent didn't trace integration boundary
- **Prevention:** Read both sides of integration, verify types match

**2. Optional Parameter Handling**
- **Symptom:** `if negative_prompt:` (falsy check)
- **Question:** What if negative_prompt == "" (empty string)?
- **Answer:** Empty string is falsy, won't be included in payload
- **Why Verified:** Agent checked frontend sends only non-empty (`.trim()` check)
- **Prevention:** Trace optional param handling from caller to callee

**3. None vs Default Value**
- **Symptom:** `def func(param=None):` but expects int
- **Impact:** TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
- **Why Missed:** Tests always provide value, never test None case
- **Prevention:** Check if default value matches type hint

---

### Missing Error Handling for Rare Scenarios

**Why Easy to Miss:**
- "Happy path" testing (inputs always valid)
- Edge cases not documented in spec
- "It should never happen" assumptions

**Common Missed Issues:**

**1. File Operations**
- **Missing:** try/except for FileNotFoundError, PermissionError
- **Impact:** Crash instead of graceful degradation
- **Why Missed:** Tests always use files that exist
- **Prevention:** Check EVERY file operation has error handling

**2. External API Failures**
- **Missing:** Timeout, ConnectionError, HTTPError handling
- **Impact:** Application hangs or crashes
- **Why Missed:** Tests mock API (never test network failures)
- **Prevention:** Verify try/except catches requests.exceptions

**3. localStorage Disabled**
- **Missing:** try/catch for localStorage.setItem() quota exceeded
- **Impact:** Silent failure or crash
- **Why Missed:** Tests in browser with localStorage enabled
- **Prevention:** Check graceful degradation when storage unavailable

---

### Hard-Coded Values That Should Be Config

**Why Easy to Miss:**
- Code works with hard-coded values
- Refactoring deferred ("will fix later")
- "Zero tech debt tolerance" not enforced

**Common Missed Issues:**

**1. Magic Numbers**
- **Symptom:** `if len(data) > 1000:` (why 1000?)
- **Fix:** `MAX_DATA_SIZE = 1000` (named constant) or config file
- **Why Missed:** Agent focused on logic, not maintainability
- **Prevention:** Search for numeric literals (except 0, 1, -1)

**2. File Paths**
- **Symptom:** `Path("backend/temp_images")` (hard-coded relative path)
- **Risk:** Breaks if working directory changes
- **Fix:** Config variable or use `__file__` for relative paths
- **Why Missed:** Works in current environment
- **Prevention:** Check all Path() calls use config or absolute paths

**3. API Endpoints**
- **Symptom:** `url = "https://api.example.com/v1/endpoint"`
- **Risk:** Can't switch environments (dev/staging/prod)
- **Fix:** Environment variable `EXTERNAL_API_URL`
- **Why Missed:** Works for POC
- **Prevention:** Check all external URLs from config

---

### Validation Approach to Avoid False Negatives

**1. Read Spec FIRST (Before Implementation)**
- Understand requirements before verifying code
- Check "Does code do what spec asks?" not just "Does code work?"

**2. Assume Everything Is Wrong**
- Question every design decision
- Ask "Why was it done this way?"
- Look for alternative approaches that might be better

**3. Think Like an Attacker**
- Ask "How could a malicious user exploit this?"
- Check input validation, path resolution, SQL/command injection

**4. Verify Edge Cases**
- Empty input, max input, boundary values (0, -1, MAX_INT)
- Array boundaries (first, last, empty)
- Error scenarios (file not found, network failure, quota exceeded)

**5. Trace Integration Boundaries**
- Read BOTH sides (caller and callee)
- Verify types match, error propagation correct

**6. Use Empirical Verification**
- grep_search for TODO|FIXME|XXX (ZERO tolerance)
- Read actual files (not from memory)
- Provide file:line evidence for all claims

**7. Different Reading Patterns Each Round**
- Round 1: Sequential (first to last)
- Round 2: Reverse (last to first)
- Round 3: Random spot-checks + suspicious areas

**8. Self-Check: "Would I bet my reputation this is bug-free?"**
- If hesitation → investigate deeper
- If confident → document evidence (file:line references)

---

## Summary

**S7 Feature QC Validation Loop:**
- **Extends:** Master Validation Loop Protocol (7 universal dimensions)
- **Adds:** 9 S7 QC-specific dimensions
- **Total:** 16 dimensions checked every round
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
