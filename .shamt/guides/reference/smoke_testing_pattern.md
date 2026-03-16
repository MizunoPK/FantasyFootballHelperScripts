# Smoke Testing Pattern (Reference)

**Purpose:** Generic smoke testing workflow applicable to both feature-level (S7.P1) and epic-level (S9.P1) testing.

**This is a REFERENCE PATTERN.** Actual guides:
- **Feature-level:** `stages/s7/s7_p1_smoke_testing.md`
- **Epic-level:** `stages/s9/s9_p1_epic_smoke_testing.md`

---

## Table of Contents

1. [What is Smoke Testing?](#what-is-smoke-testing)
2. [Common Smoke Testing Structure](#common-smoke-testing-structure)
3. [Universal Critical Rules](#universal-critical-rules)
4. [Part 1: Import Test (Universal Pattern)](#part-1-import-test-universal-pattern)
5. [Part 2: Entry Point Test (Universal Pattern)](#part-2-entry-point-test-universal-pattern)
6. [Part 3: E2E Execution Test (Universal Pattern - CRITICAL)](#part-3-e2e-execution-test-universal-pattern---critical)
7. [Part 4: Cross-Feature Integration (Epic-Level Only)](#part-4-cross-feature-integration-epic-level-only)
8. [Restart Protocol](#restart-protocol)
9. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
10. [Scope-Specific Differences](#scope-specific-differences)
11. [Part 3 Detail: Testing Approach Paths](#part-3-detail-testing-approach-paths)
12. [Mandatory Logging Requirements](#mandatory-logging-requirements)
13. [Platform-Specific Considerations](#platform-specific-considerations)
14. [Summary](#summary)

---

## What is Smoke Testing?

**Definition:** Smoke testing is the first validation step after implementation where you verify the system actually runs end-to-end with REAL data through mandatory structured parts.

**Purpose:**
- Catch basic integration issues before deeper QC
- Verify output produces correct DATA VALUES (not just structure)
- Use REAL data (not test fixtures) to expose mock assumption failures

**Scope-Specific Implementation:**
- **Feature-level (S7.P1):** Tests individual feature in isolation
- **Epic-level (S9.P1):** Tests ALL features working together as cohesive system

---

## Common Smoke Testing Structure

**All smoke testing follows this pattern:**

```python
Part 1: Import Test
   ↓ Verify modules load without errors
   ↓ Catches: Import errors, circular dependencies, missing __init__.py
   ↓
   If PASS → Part 2
   If FAIL → Fix issues, re-run Part 1

Part 2: Entry Point Test
   ↓ Verify script/system starts correctly
   ↓ Catches: Argument parsing errors, initialization crashes, config issues
   ↓
   If PASS → Part 3
   If FAIL → Fix issues, re-run Parts 1 & 2

Part 3: End-to-End Execution Test (CRITICAL)
   ↓ Execute with REAL data
   ↓ Verify OUTPUT DATA VALUES are correct (not just "file exists")
   ↓ Catches: Mock assumption failures, data quality issues, integration bugs
   ↓
   If PASS → [Scope-specific next step]
   If FAIL → Fix issues, RE-RUN ALL PARTS

[Optional Part 4: Epic-level only]
   Cross-Feature Integration Tests
```

---

## Universal Critical Rules

**These rules apply to ALL smoke testing (feature or epic):**

### 0. ZERO TOLERANCE FOR ERRORS (CRITICAL)

```python
ZERO TOLERANCE FOR ERRORS DURING SMOKE TESTING

1. Every test must PASS - "runs without crashing" is NOT passing
2. ANY error (including import errors) requires immediate investigation
3. "Environment issue" is NEVER an acceptable explanation without proof:
   - Prove the code works in a proper environment
   - If you can't prove it, it's a CODE BUG until proven otherwise
4. Must test with production-like environment (venv with all dependencies)
5. Never assume "because X works, Y must work" - verify independently

Before marking smoke test as PASSED:
- [ ] All components returned exit code 0
- [ ] No import errors in any output
- [ ] Expected output/behavior observed (not just "no crash")
- [ ] If using subprocess, verified child uses correct Python interpreter
- [ ] If any errors occurred, documented root cause (not just "environment")

HISTORICAL CASE: All 6 components failed with ModuleNotFoundError during
S9 smoke testing. Agent marked as PASSED assuming "environment issue".
Root cause: Code bug (hardcoded 'python' instead of sys.executable).
This could have caused weeks of debugging if not caught.
```

### 1. ALL Parts Are MANDATORY
- Cannot skip any part
- Must complete in order (Part 1 → 2 → 3 → [4 if epic])
- Each part validates different aspect

### 2. Part 3 MUST Verify DATA VALUES
```python
## ❌ NOT SUFFICIENT:
assert Path("output.csv").exists()  # Just checks file exists

## ✅ REQUIRED:
output_file = Path("output.csv")
assert output_file.exists()

## Actually READ and VERIFY data
df = pd.read_csv(output_file)

## Verify data quality
assert len(df) > 0, "Output file is empty"
assert not df['projected_value'].isnull().all(), "All projected_value are null"
assert df['projected_value'].sum() > 0, "All projected_value are zero"

## Verify data makes sense
top_player = df.iloc[0]
assert top_item['projected_value'] > 100, "Top item has unreasonably low score"
assert top_item['item_name'] != "", "Item name is empty"
```

### 3. If ANY Part Fails, RE-RUN ALL PARTS
- Don't just re-run the failed part
- Fixes can introduce new issues in earlier parts
- All parts must pass on SAME run
- This ensures clean validation state

### 4. Use REAL Data (Not Test Fixtures)
- Part 3 (E2E) must use production-like data
- Test fixtures hide integration issues
- Real data catches mock assumption failures
- **Real-world case:** Feature passed 2,369 unit tests (100%) but smoke testing revealed output files missing 80% of required data

### 5. Document ALL Results
- Even if all parts pass
- Include: What was tested, what passed, data samples inspected
- Update README Agent Status after smoke testing complete
- Provides evidence for QC rounds

---

## Part 1: Import Test (Universal Pattern)

**Goal:** Verify modules load without errors

**Process:**
1. Identify all new/modified modules
2. For each module, run import test:
   ```bash
   python -c "import module.path.ClassName"
   ```
3. Verify no errors (Expected: No output = success)

**What This Catches:**
- Import errors (missing dependencies)
- Circular dependencies
- Module initialization crashes
- Missing `__init__.py` files
- Syntax errors
- Name errors in imports

**Pass Criteria:**
- ✅ **PASS:** All modules import successfully with zero errors
- ❌ **FAIL:** Any import errors occur

**If Part 1 Fails:**
1. Note error message
2. Fix issue (add dependencies, fix circular imports, add `__init__.py`, fix syntax)
3. Re-run Part 1 (test ALL imports again)
4. Then proceed to Part 2

---

## Part 2: Entry Point Test (Universal Pattern)

**Goal:** Verify script/system starts correctly and handles arguments properly

**Process:**
1. Identify entry point script
2. Test help output: `python run_script.py --help`
3. Test invalid argument handling: `python run_script.py --invalid-arg`
4. Test script starts (if applicable): `python run_script.py --mode test_mode --help`

**What This Catches:**
- Argument parsing errors
- Script initialization crashes
- Missing configuration files
- Unhelpful error messages
- Mode-specific initialization issues

**Pass Criteria:**
- ✅ **PASS:** `--help` displays correctly, invalid arguments produce helpful errors (not stack traces), script starts without crashes
- ❌ **FAIL:** Help missing/incomplete, crashes on invalid arguments, initialization crashes

**If Part 2 Fails:**
1. Document the failure (command, error, root cause)
2. Fix issue (update argument parsing, fix initialization, add config, improve errors)
3. Re-run Part 1 AND Part 2 (fixes can affect imports)
4. Then proceed to Part 3

---

## Part 3: E2E Execution Test (Universal Pattern - CRITICAL)

**Goal:** Execute end-to-end with REAL data and verify output CONTENT is correct

**⚠️ THIS IS THE MOST IMPORTANT SMOKE TEST**

**Process:**
1. Identify primary use case from spec
2. Prepare REAL input data (not test fixtures)
3. Execute end-to-end
4. **CRITICAL:** Verify output DATA VALUES are correct

**Data Validation Requirements:**

**For EACH category/type being processed:**
- Don't just check totals - verify PER-CATEGORY
- Sample one item from each category and check actual data values
- Example: If processing 6 positions (QB, RB, WR, TE, K, DST), verify data for ALL 6

**Example verification:**
```python
## Feature updates 6 position files
positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']

for pos in positions:
    pos_file = Path(f"data/{pos.lower()}_data.json")
    assert pos_file.exists(), f"{pos} file missing"

    # Verify data VALUES (not just file exists)
    with open(pos_file) as f:
        data = json.load(f)
    assert len(data) > 0, f"{pos} file is empty"

    # Check first item has updated data
    first_item = data[0]
    assert first_item['rank'] != 170.0, f"{pos} rank priority not updated (still placeholder)"
    assert first_item['rank'] > 0, f"{pos} rank priority is invalid"
```

**What This Catches:**
- Mock assumption failures (tests passed but real code doesn't work)
- Data quality issues (zeros instead of real values, nulls, placeholders)
- Integration point failures (mocked dependencies behave differently)
- Edge cases tests missed (real data has more variety than fixtures)
- Configuration mismatches (test vs production config differences)

**Pass Criteria:**
- ✅ **PASS:** Executes without crashes, output files exist, DATA VALUES verified correct (not zeros/nulls/placeholders), all categories have valid data
- ❌ **FAIL:** Crashes during execution, output files missing, data values incorrect/missing/placeholder

**If Part 3 Fails:**
1. Document failure (what failed, error message, which data invalid)
2. Identify root cause (mocked dependency mismatch, algorithm bug, config issue, missing edge case handling)
3. Fix ALL issues
4. RE-RUN ALL 3 PARTS FROM PART 1
5. Do NOT skip to Part 3 - full re-validation required

---

## Part 4: Cross-Feature Integration (Epic-Level Only)

**Goal:** Verify features work together correctly

**Only applicable to epic-level smoke testing (S9.P1)**

**Process:**
1. Identify cross-feature workflows (from epic_smoke_test_plan.md)
2. Execute integration scenarios
3. Verify data flows correctly between features
4. Verify interface compatibility
5. Verify error propagation across features

**What This Catches:**
- Interface mismatches between features
- Data format incompatibilities
- Error handling gaps at feature boundaries
- Workflow integration failures

**Pass Criteria:**
- ✅ **PASS:** All integration scenarios execute successfully, data flows correctly between features, interfaces compatible
- ❌ **FAIL:** Integration point failures, data format mismatches, workflow breaks

**If Part 4 Fails:**
1. Document which integration point failed
2. Fix integration issues
3. RE-RUN ALL 4 PARTS FROM PART 1

---

## Restart Protocol

**Universal rule for ALL smoke testing:**

```text
IF any part fails:
  1. Fix ALL issues found
  2. RE-RUN ALL PARTS from Part 1
  3. Do NOT skip to failed part
  4. ALL parts must pass on SAME run

WHY complete restart?
- Fixes can introduce new issues in earlier parts
- Import fixes can affect entry points
- Entry point fixes can affect E2E execution
- Clean validation state required
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Checking Structure Instead of Values
```python
## WRONG - only checks file exists
assert Path("output.csv").exists()

## CORRECT - verifies data values
df = pd.read_csv("output.csv")
assert df['score'].between(0, 500).all()
assert df['projected_value'].sum() > 0
```

### ❌ Mistake 2: Using Test Fixtures for Part 3
```python
## WRONG - test fixtures hide integration issues
test_data = create_mock_players()  # Mocked data

## CORRECT - use real production-like data
real_data = pd.read_csv("data/real_players.csv")  # Real data
```

### ❌ Mistake 3: Partial Re-run After Failure
```python
## WRONG - only re-running failed Part 3
## (skipping Parts 1 & 2)

## CORRECT - re-running ALL 3 parts from Part 1
## Fixes can affect earlier parts
```

### ❌ Mistake 4: Accepting Placeholder/Zero Data
```python
## WRONG - data exists but values are wrong
assert len(df) > 0  # File has rows, but all zeros

## CORRECT - verify data values are reasonable
assert df['projected_value'].sum() > 0  # Not all zeros
assert df['rank'].min() > 0  # Not placeholder values
```

---

## Scope-Specific Differences

### Feature-Level Smoke Testing (S7.P1)
- **Scope:** Individual feature in isolation
- **Parts:** 3 parts (Import, Entry Point, E2E)
- **Data:** Feature-specific input/output
- **Next Stage:** S7.P2 if passed
- **Restart Destination:** Part 1 of this feature's smoke testing

### Epic-Level Smoke Testing (S9.P1)
- **Scope:** ALL features working together
- **Parts:** 4 parts (Import, Entry Point, E2E, Cross-Feature Integration)
- **Data:** Epic-level workflows with multiple features
- **Next Stage:** S9.P2 (Epic Validation Loop) if passed
- **Restart Destination:** S9.P1 Step 1 (complete epic smoke testing)

---

## Part 3 Detail: Testing Approach Paths

Before starting Part 3, read `Testing Approach:` from EPIC_README. This determines which path to follow.

### Path B/D — Integration Script Opted In

Run the feature's integration test script instead of the manual 6-step process.

1. **Read `Integration Test Convention:` from EPIC_README** for script location and invocation command
2. **Run the integration test script:**
   ```bash
   {invocation command from EPIC_README}
   ```
3. **The script must pass (exit code 0)** — the 6 manual steps are encoded in the script
4. **If the script fails:** investigate root cause, fix, restart from Part 1

**Note:** `test_scenario.md` and `expected_results.md` test artifacts are superseded by the integration test script for Options B/D — they do not need to be created separately.

**If Part 3 passes:** proceed to next stage (S7.P2 or S9.P2).

---

### Path A/C — Manual 6-Step E2E Process

**Required Test Artifacts (before executing):**

Create in the epic folder before starting Part 3:
1. **`SHAMT-{N}-{epic_name}/test_scenario.md`** — document the standard test scenario:
   - Input data sources (which files, what values)
   - Expected behavior and outputs
   - Validation criteria
2. **`SHAMT-{N}-{epic_name}/expected_results.md`** — document expected results:
   - Expected output structure
   - Expected value ranges (from spec)
   - Edge cases to verify
   - Pass/fail criteria

**Step 1: Prepare Environment**

```bash
which python  # Should show venv path
python -m pip install -e .  # If using editable install
```

Verify:
- [ ] Python environment is correct
- [ ] Dependencies are installed
- [ ] No stale processes running

**Step 2: Prepare Test Data**

Reference `test_scenario.md`. Use production or production-like data:
- ✅ Real data from `data/` directory
- ❌ NOT test fixtures (unless testing edge cases specifically)
- ❌ NOT mocked data

Document what was used: input files, values, expected behavior.

**Step 3: Execute End-to-End**

```bash
python run_[module].py --mode {feature_mode} --data-folder ./data
```

Verify:
- [ ] Script completes without crashes
- [ ] No unexpected errors in logs
- [ ] Output files created
- [ ] Execution time reasonable

**Step 4: Validate Output Structure**

Reference `expected_results.md`. Verify:
- [ ] All expected output files exist
- [ ] Files contain data (not empty)
- [ ] Required fields present (from spec)
- [ ] No null/empty/placeholder values in structure

**Step 5: Validate Output Data Values (CRITICAL)**

See data validation examples in the universal Part 3 section above. Key checks:
- Values in expected range (from spec)
- Non-uniform distribution (feature actually ran calculations)
- Edge cases handled correctly
- No placeholder values remaining

**Step 6: Check Application Logs**

See the **Mandatory Logging Requirements** section below for required log types.

```bash
grep "feature_keyword" logs/application.log
tail -100 logs/application.log | grep -i "feature"
```

Verify:
- [ ] Feature activation logged
- [ ] Key data processing logged
- [ ] Feature results logged
- [ ] No unexpected errors or warnings

If logs are missing or insufficient: add required logging, re-run E2E test, verify logs show observable feature behavior.

---

## Mandatory Logging Requirements

All features must include appropriate logging for observability. Logs are validated in Part 3 Step 6.

### Required Log Messages

1. **Feature Entry** — log when feature is activated
2. **Key Data Processing** — log important data transformations
3. **Feature Results** — log feature outputs/calculations
4. **Error Handling** — log feature-specific errors

### Log Level Guidelines

- **`logger.info()`**: Feature activation, important results
- **`logger.debug()`**: Detailed processing steps
- **`logger.warning()`**: Non-critical issues, fallbacks
- **`logger.error()`**: Feature failures, critical issues

### Example

```python
logger = get_logger()
logger.info(f"Feature mode activated for: {context_name}")
logger.debug(f"Processing {len(items)} items")
logger.info(f"Generated {len(results)} results")
logger.error(f"Failed to process: {e}", exc_info=True)
```

Missing logs = Part 3 Step 6 failure. Smoke testing requires visible evidence that the feature ran.

---

## Platform-Specific Considerations

### Windows: File Locking with Log Handlers

When testing logging functionality on Windows, file handlers may keep log files open, preventing temporary directory cleanup.

**Problem:** `PermissionError` or `WinError 32` during cleanup of temporary directories that contain log files.

**Solution:** Close log handlers before temp directory cleanup:

```python
def _close_logger_handlers(logger):
    """Close all handlers to release file locks (Windows)."""
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

# In test:
try:
    logger = setup_debug_logging("test_component")
    logger.info("Test message")
finally:
    _close_logger_handlers(logger)
    # Now temp directory can be cleaned up
```

**When this applies:**
- Testing file logging on Windows
- Using temporary directories with log files
- Seeing `PermissionError` or `WinError 32` during cleanup

---

## Summary

**Key Principles:**
1. All parts mandatory (no skipping)
2. Verify DATA VALUES (not just structure)
3. Use REAL data (not fixtures)
4. Re-run ALL parts if any fail
5. Document all results

**Purpose:**
- Catch integration issues early
- Expose mock assumption failures
- Validate with real-world data
- Ensure production readiness

**Remember:** Smoke testing takes 15-30 minutes but prevents hours of debugging later. NEVER skip data value verification.

---

*For actual implementation guides, see:*
- Feature-level: `stages/s7/s7_p1_smoke_testing.md`
- Epic-level: `stages/s9/s9_p1_epic_smoke_testing.md`
