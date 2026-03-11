# S7.P1: Smoke Testing

**File:** `s7_p1_smoke_testing.md`

**Purpose:** Verify the feature actually runs and produces correct output through mandatory 3-part smoke testing.

**Stage Flow Context:**
```text
S5 (Implementation Planning) → S6 (Implementation Execution) →
→ [YOU ARE HERE: S7.P1 - Smoke Testing] →
→ S7.P2 (Validation Loop) → S7.P3 (Final Review) →
→ S8 (Post-Feature Alignment)
```

---


## Table of Contents

1. [S7.P1: Smoke Testing](#s7p1-smoke-testing)
2. [🚨 MANDATORY READING PROTOCOL](#🚨-mandatory-reading-protocol)
3. [Overview](#overview)
4. [🛑 Critical Rules (Feature-Specific)](#🛑-critical-rules-feature-specific)
5. [Prerequisites Checklist](#prerequisites-checklist)
6. [Workflow Overview](#workflow-overview)
7. [Part 1: Import Test (Feature-Specific)](#part-1-import-test-feature-specific)
8. [Part 2: Entry Point Test (Feature-Specific)](#part-2-entry-point-test-feature-specific)
9. [Part 3: E2E Execution Test (Feature-Specific - CRITICAL)](#part-3-e2e-execution-test-feature-specific---critical)
10. [Test Scenario: Rating Multiplier Feature](#test-scenario-rating-multiplier-feature)
11. [🚨 MANDATORY LOGGING REQUIREMENTS](#🚨-mandatory-logging-requirements)
12. [Pass/Fail Criteria](#passfail-criteria)
13. [Platform-Specific Considerations](#platform-specific-considerations)
14. [Common Feature-Specific Issues](#common-feature-specific-issues)
15. [🛑 MANDATORY CHECKPOINT 1](#🛑-mandatory-checkpoint-1)
16. [Next Steps](#next-steps)
17. [Summary](#summary)
18. [Exit Criteria](#exit-criteria)

---
## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Smoke Testing, you MUST:**

1. **Read the smoke testing pattern:** `reference/smoke_testing_pattern.md`
   - Understand universal smoke testing workflow (3 parts)
   - Review critical rules that apply to ALL smoke testing
   - Study common mistakes to avoid

2. **Use the phase transition prompt** from `prompts/s5_s8_prompts.md`
   - Find "Starting S7.P1: Smoke Testing" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from this guide

3. **Update README Agent Status** with:
   - Current Phase: POST_IMPLEMENTATION_SMOKE_TESTING
   - Current Guide: stages/s7/s7_p1_smoke_testing.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "3 parts MANDATORY", "Part 3 verify DATA VALUES", "Re-run ALL 3 if ANY fails"
   - Next Action: Smoke Test Part 1 - Import test

4. **Verify all prerequisites** (see checklist below)

5. **THEN AND ONLY THEN** begin smoke testing

**This is NOT optional.** Reading both the pattern and this guide ensures you don't skip critical validation steps.

---

## Overview

**What is this guide?**
Feature-level smoke testing validates that your individual feature works end-to-end with REAL data. This is testing in ISOLATION (not with other features). See `reference/smoke_testing_pattern.md` for universal workflow.

**When do you use this guide?**
- S6 complete (Implementation Execution finished)
- Feature code is written
- Ready to validate with real data

**Key Outputs:**
- ✅ Part 1 PASSED: Import Test (all modules load without errors)
- ✅ Part 2 PASSED: Entry Point Test (script starts correctly)
- ✅ Part 3 PASSED: E2E Execution Test (feature runs end-to-end, data values verified)
- ✅ Data values inspected (not zeros, nulls, or placeholders)
- ✅ Ready for S7.P2

**Time Estimate:**
15-30 minutes

**Exit Condition:**
Smoke Testing is complete when ALL 3 parts pass (including data value verification in Part 3), output files are inspected and confirmed correct, and you're ready to proceed to Validation Loop

---

## 🛑 Critical Rules (Feature-Specific)

**📖 See `reference/smoke_testing_pattern.md` for universal critical rules.**

**Feature-specific rules for S7.P1:**

```text
┌─────────────────────────────────────────────────────────────┐
│ FEATURE-SPECIFIC RULES - Add to README Agent Status         │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Test feature IN ISOLATION
   - Do NOT test with other features
   - Use feature's own input/output
   - Epic-level integration tested in S9

2. ⚠️ If smoke testing fails → Fix issues, restart from Part 1
   - After fixing → Re-run ALL 3 parts
   - Do NOT proceed to Validation Loop (S7.P2) until all parts pass

3. ⚠️ Document results in feature README
   - Update feature README.md Agent Status
   - Include smoke test results
   - List which parts passed and data samples inspected
```

**Universal rules (from pattern file):**
- ALL 3 parts mandatory
- Part 3 MUST verify data VALUES (not just structure)
- Use REAL data (not test fixtures)
- Re-run ALL parts if ANY fail
- See `reference/smoke_testing_pattern.md` for complete list

---

## Prerequisites Checklist

**Verify these BEFORE starting Smoke Testing:**

**From S6 (Implementation):**
- [ ] All implementation tasks marked done in `implementation_checklist.md`
- [ ] All unit tests passing (100% pass rate)
- [ ] `implementation_checklist.md` all requirements verified
- [ ] All code committed to git (clean working directory)

**Files that must exist:**
- [ ] `feature_XX_{name}/spec.md` (primary specification)
- [ ] `feature_XX_{name}/checklist.md` (planning decisions)
- [ ] `feature_XX_{name}/implementation_plan.md` (implementation guidance)
- [ ] `feature_XX_{name}/implementation_checklist.md` (progress tracking and requirement verification)

**Verification:**
- [ ] Run `{TEST_COMMAND}` → exit code 0
- [ ] Check `git status` → no uncommitted implementation changes
- [ ] Review implementation_checklist.md → all items marked verified

**If ANY prerequisite not met:** Return to S6 and complete it first.

---

## Workflow Overview

**📖 See `reference/smoke_testing_pattern.md` for universal workflow details.**

**Feature-specific workflow for S7.P1:**

```python
┌─────────────────────────────────────────────────────────────┐
│       FEATURE-LEVEL SMOKE TESTING (3 Parts)                 │
└─────────────────────────────────────────────────────────────┘

Part 1: Import Test
   ↓ Import all NEW/MODIFIED modules for THIS feature
   ↓ Verify no import errors
   ↓
   If PASS → Part 2
   If FAIL → Fix, re-run Part 1

Part 2: Entry Point Test
   ↓ Test script starts with feature mode/options
   ↓ Verify help text includes feature additions
   ↓
   If PASS → Part 3
   If FAIL → Fix, re-run Parts 1 & 2

Part 3: E2E Execution Test (CRITICAL)
   ↓ Execute FEATURE workflow with REAL data
   ↓ Verify feature output DATA VALUES correct
   ↓ Check each output category (if multiple)
   ↓
   If PASS → Document, proceed to S7.P2
   If FAIL → Fix, RE-RUN ALL 3 PARTS
```

---

## Part 1: Import Test (Feature-Specific)

**📖 See `reference/smoke_testing_pattern.md` for universal import test pattern.**

**Feature-specific implementation:**

### Step 1: Identify Feature Modules

Check git history for list of NEW or MODIFIED files for THIS feature:

```bash
git log --oneline --name-status origin/main..HEAD
```

This shows all files changed in this feature branch.

### Step 2: Test Each Module Import

```bash
## Test new modules
python -c "from [module].util.PlayerRatingManager import PlayerRatingManager"
python -c "import [module].util.PlayerRatingManager"

## Test modified modules still import
python -c "from [module].LeagueHelper import LeagueHelper"
python -c "import run_[module]"
```

### Step 3: Verify Results

**Expected:** No output (silence = success)

**If errors:** See pattern file for common fixes (missing dependencies, circular imports, missing `__init__.py`)

---

## Part 2: Entry Point Test (Feature-Specific)

**📖 See `reference/smoke_testing_pattern.md` for universal entry point test pattern.**

**Feature-specific implementation:**

### Step 1: Identify Feature Entry Point

From `spec.md` "Usage" section, identify how feature is invoked:
- Example: `python run_[module].py --mode rating_helper`
- Example: `python [run_script].py --use-ratings`

### Step 2: Test Feature Help

```bash
## If feature adds new mode
python run_[module].py --mode rating_helper --help

## If feature adds new flag
python [run_script].py --help
## (verify --use-ratings appears in help text)
```

### Step 3: Test Feature Initialization

```bash
## Basic startup test (dry-run or help mode)
python run_[module].py --mode rating_helper --dry-run
```

**Expected:**
- Help text displays (if `--help`)
- Feature initializes without crashing (if dry-run)
- Error messages are helpful (not stack traces)

---

## Part 3: E2E Execution Test (Feature-Specific - CRITICAL)

**📖 See `reference/smoke_testing_pattern.md` for universal E2E test pattern and data validation examples.**

**🚨 REQUIRED TEST ARTIFACTS (Middle Ground Approach):**

Before executing E2E testing, create standardized test artifacts in epic folder:

1. **Test Scenario Documentation:** `SHAMT-{N}-{epic_name}/test_scenario.md`
   - Document standard test scenario for this feature
   - Include input data sources (which files, what values)
   - Document expected behavior and outputs
   - Describe validation criteria

2. **Expected Results Documentation:** `SHAMT-{N}-{epic_name}/expected_results.md`
   - Document expected output structure
   - Include expected value ranges (from spec)
   - List edge cases to verify
   - Define pass/fail criteria

**Benefits:**
- ✅ Maintains flexible feature-specific testing approach
- ✅ Adds documentation consistency across features
- ✅ Enables easier review and verification
- ✅ Provides reference for future modifications

**Standardized 6-Step E2E Testing Process:**

### Step 1: Prepare Environment

**Ensure clean state and dependencies:**
```bash
## Verify virtual environment activated
which python  # Should show venv path

## Ensure clean state (optional)
python -m pip install -e .  # If using editable install
```

**Verify:**
- [ ] Python environment is correct
- [ ] Dependencies are installed
- [ ] No stale processes running

---

### Step 2: Prepare Standardized Test Data

**📖 Reference:** `SHAMT-{N}-{epic_name}/test_scenario.md` (created during Part 3 setup)

**Use PRODUCTION or PRODUCTION-LIKE data:**
- ✅ Real data CSV files from `data/`
- ✅ Real league config from `data/league_config.json`
- ❌ NOT test fixtures (unless specifically testing edge cases)
- ❌ NOT mocked data

**Document test scenario:**
- Input data sources (which files, what values)
- Expected behavior from spec.md
- Feature-specific validation criteria

**Example from test_scenario.md:**
```markdown
## Test Scenario: Rating Multiplier Feature

**Input Data:**
- data/players_2024.csv (300+ items)
- data/league_config.json (standard scoring)

**Expected Behavior:**
- Apply rank-based multipliers (0.5 to 1.5 range)
- Update 6 position-specific JSON files
- Multipliers calculated per rank priority ranges from spec

**Validation Criteria:**
- All 6 position files updated
- Multipliers in correct range (0.5-1.5)
- No placeholder values (all 1.0)
```

---

### Step 3: Execute Feature End-to-End

**Run feature with production data:**
```bash
python run_[module].py --mode {feature_mode} --data-folder ./data
```

**Example:**
```bash
python run_[module].py --mode rating_helper --data-folder ./data
```

**Monitor for:**
- [ ] Script completes without crashes
- [ ] No unexpected errors/warnings in logs
- [ ] Output files created
- [ ] Execution time reasonable (not hanging)

---

### Step 4: Validate Output Structure

**📖 Reference:** `SHAMT-{N}-{epic_name}/expected_results.md`

**Check output file structure:**
```python
from pathlib import Path
import json

## Verify expected output files exist
expected_files = ['qb_ratings.json', 'rb_ratings.json', 'wr_ratings.json',
                  'te_ratings.json', 'k_ratings.json', 'dst_ratings.json']

for filename in expected_files:
    filepath = Path(f"data/{filename}")
    assert filepath.exists(), f"Missing output file: {filename}"

    # Verify file has data (not empty)
    with open(filepath) as f:
        data = json.load(f)
    assert len(data) > 0, f"{filename} is empty"

    # Verify expected fields present
    first_item = data[0]
    assert 'rank_multiplier' in first_item, f"{filename} missing rank_multiplier field"

print("✅ Output structure validated")
```

**Verify:**
- [ ] All expected output files exist
- [ ] Files contain data (not empty)
- [ ] Required fields present (from spec)
- [ ] No null/empty/placeholder values in structure

---

### Step 5: Validate Output Data Values (CRITICAL)

**📖 See pattern file for data validation examples.**

**📖 Refer to `SHAMT-{N}-{epic_name}/expected_results.md` for validation criteria**

**⚠️ CRITICAL: Don't just check structure - verify actual data correctness**

**Feature-specific validation (example for rating multiplier feature):**

```python
import json
from pathlib import Path

## Feature updates 6 position files
positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']

for pos in positions:
    pos_file = Path(f"data/{pos.lower()}_ratings.json")

    # Part 3a: Structure validation
    assert pos_file.exists(), f"{pos} file missing"

    with open(pos_file) as f:
        data = json.load(f)
    assert len(data) > 0, f"{pos} file is empty"

    # Part 3b: DATA VALUE validation (CRITICAL)
    first_item = data[0]

    # Verify multiplier field exists and has value
    assert 'rank_multiplier' in first_item, f"{pos} missing rank_multiplier field"
    assert first_item['rank_multiplier'] is not None, f"{pos} multiplier is None"

    # Verify multiplier is in expected range (from spec: 0.5 to 1.5)
    multiplier = first_item['rank_multiplier']
    assert 0.5 <= multiplier <= 1.5, f"{pos} multiplier {multiplier} out of range"

    # Verify multiplier is not placeholder (common bug)
    assert multiplier != 1.0, f"{pos} multiplier is placeholder value (1.0)"

    # Sample check: At least some items have non-1.0 multipliers
    multipliers = [p['rank_multiplier'] for p in data[:10]]
    non_default = [m for m in multipliers if m != 1.0]
    assert len(non_default) > 0, f"{pos} all multipliers are default (1.0)"

print("✅ All 6 positions have valid multiplier data")
```

**Key validation points:**
1. ✅ Values are correct type (float not string)
2. ✅ Values in expected range (0.5-1.5 from spec)
3. ✅ Values are NOT placeholders (not all 1.0)
4. ✅ Calculations produce varied results (not uniform)
5. ✅ Edge cases handled correctly (high rank, low rank, missing rank)

**Pass Criteria:**
- All values in expected range from spec
- Non-uniform distribution (feature actually ran)
- Edge cases produce valid values
- No errors or exceptions in calculations

---

## 🚨 MANDATORY LOGGING REQUIREMENTS

**All features MUST include appropriate logging for observability:**

### Required Log Messages:
1. **Feature Entry** - Log when feature is activated
2. **Key Data Processing** - Log important data transformations
3. **Feature Results** - Log feature outputs/calculations
4. **Error Handling** - Log feature-specific errors

### Log Level Guidelines:
- **logger.info()**: Feature activation, important results
- **logger.debug()**: Detailed processing steps
- **logger.warning()**: Non-critical issues, fallbacks
- **logger.error()**: Feature failures, critical issues

### Example Logging (Python):
```python
logger = get_logger()
logger.info(f"Draft helper mode activated for league: {league_name}")
logger.debug(f"Processing {len(items)} items for recommendations")
logger.info(f"Generated {len(recommendations)} recommendations")
logger.error(f"Failed to load record data: {e}", exc_info=True)
```

### Validation in Smoke Testing:
- Part 3 Step 6: Check logs for feature-specific messages
- Missing logs = smoke test failure
- Logs must show feature activation and key operations

---

### Step 6: Check Application Logs

**Check for feature-specific log messages:**
```bash
## Check application logs for feature activity
grep "feature_name\|important_keyword" logs/application.log
## Or check recent logs
tail -100 logs/application.log | grep -i "feature"
```

**Required validations:**
- [ ] Feature activation logged (from logging requirements above)
- [ ] Key data processing logged
- [ ] Feature results logged
- [ ] No unexpected errors or warnings
- [ ] Log messages clearly show feature behavior

**If logs missing or insufficient:**
- Add required logging (see Mandatory Logging Requirements above)
- Re-run E2E test after adding logs
- Verify logs show observable feature behavior

**If validation reveals issues:**
- Document what failed and why
- Identify root cause (algorithm bug, config issue, data mismatch)
- Fix ALL issues
- RE-RUN ALL 3 PARTS from Part 1

---

## Pass/Fail Criteria

**📖 See `reference/smoke_testing_pattern.md` for universal pass criteria.**

**Feature-specific criteria:**

**✅ PASS if:**
- Part 1: All feature modules import successfully
- Part 2: Feature mode/options work correctly
- Part 3: All 6 steps passed:
  - Step 1: Environment prepared
  - Step 2: Test data identified and documented
  - Step 3: Feature executes end-to-end without crashes
  - Step 4: Output structure validated
  - Step 5: Output data values verified correct (CRITICAL)
  - Step 6: Application logs show feature behavior

**❌ FAIL if:**
- Part 1: Any import errors
- Part 2: Help missing, crashes on startup
- Part 3: ANY step fails:
  - Environment not clean
  - Execution crashes
  - Output structure wrong
  - **Data values incorrect/missing/placeholder** (most common failure)
  - Logs missing or show errors

**If FAIL:**
1. Document failure in feature README
2. Identify root cause
3. Fix ALL issues found
4. RE-RUN ALL 3 PARTS (not just failed part)
5. Do NOT proceed to S7.P2 until all parts pass

---

## Platform-Specific Considerations

### Windows File Locking

When testing logging functionality on Windows, file handlers may keep log files open, preventing temporary directory cleanup.

**Solution:** Add cleanup code to close handlers before temp directory cleanup:

```python
def _close_logger_handlers(logger):
    """Close all handlers to release file locks (Windows)."""
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

## In test:
try:
    # Test logging functionality
    logger = setup_debug_logging("test_component")
    logger.info("Test message")
finally:
    _close_logger_handlers(logger)
    # Now temp directory can be cleaned up
```

**When this applies:**
- Testing file logging on Windows
- Using temporary directories with log files
- Seeing "PermissionError" or "WinError 32" during cleanup

---

## Common Feature-Specific Issues

### Issue 1: Feature Works in Tests But Not with Real Data

**Symptom:** Unit tests pass (100%) but Part 3 fails with real data

**Root Cause:** Mocked dependencies behave differently than real dependencies

**Example:**
```python
## Test mocked this to return 170.0 for all items
mock_api.get_rank.return_value = 170.0

## But real API returns None for some items (not in database)
## Feature crashed on None value
```

**Fix:** Update implementation to handle real-world edge cases (None, missing data, API errors)

### Issue 2: Output Structure Correct But Values Wrong

**Symptom:** Files created, have rows, but all values are zeros/placeholders

**Root Cause:** Forgot to actually populate data (just created structure)

**Example:**
```python
## WRONG - creates structure but doesn't populate
items = []
for p in raw_data:
    items.append({'name': p.name, 'multiplier': 1.0})  # Placeholder!

## CORRECT - actually calculate values
items = []
for p in raw_data:
    multiplier = calculate_multiplier(p.rank)  # Real calculation
    items.append({'name': p.name, 'multiplier': multiplier})
```

**Fix:** Verify algorithms are actually executing (not just creating placeholders)

### Issue 3: Works for Some Categories But Not All

**Symptom:** QB file correct but other positions missing/wrong

**Root Cause:** Algorithm only tested with one category, doesn't generalize

**Fix:** Verify implementation works for ALL categories (loop through all in Part 3)

---

## 🛑 MANDATORY CHECKPOINT 1

**You have completed all 3 parts of Smoke Testing**

⚠️ STOP - DO NOT PROCEED TO S7.P2 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Critical Rules" section (top of this guide)
2. [ ] Use Read tool to re-read `reference/smoke_testing_pattern.md` (Common Mistakes section)
3. [ ] Verify data VALUES inspected (not just "file exists") for all 3 parts
4. [ ] Update feature README Agent Status:
   - Current Guide: "stages/s7/s7_p2_qc_rounds.md"
   - Current Step: "S7.P1 complete, ready to start S7.P2 Validation Loop"
   - Last Updated: [timestamp]
5. [ ] Output acknowledgment: "✅ CHECKPOINT 1 COMPLETE: Re-read Critical Rules and Pattern File, verified data values inspected"

**Why this checkpoint exists:**
- 90% of agents pass smoke testing without inspecting actual data values
- "File exists" checks miss 70% of data corruption issues
- 2 minutes of re-reading prevents hours of debugging in production

**ONLY after completing ALL 5 actions above, proceed to Next Steps section**

---

## Next Steps

**If ALL 3 parts PASSED:**
- ✅ Document smoke test results in feature README
- ✅ Update Agent Status: "Smoke Testing COMPLETE"
- ✅ Proceed to **S7.P2: Validation Loop**

**If ANY part FAILED:**
- ❌ Fix ALL issues identified
- ❌ RE-RUN ALL 3 PARTS from Part 1
- Do NOT proceed to Validation Loop until clean pass

---

## Summary

**Feature-Level Smoke Testing validates:**
- Feature modules import correctly (Part 1)
- Feature entry point works (Part 2)
- Feature executes end-to-end with REAL data producing CORRECT values (Part 3)

**Key Differences from Epic-Level:**
- Tests feature in ISOLATION (not with other features)
- 3 parts only (no Part 4 cross-feature integration)
- Next stage: Validation Loop for THIS feature (S7.P2)

**Critical Success Factors:**
- Use REAL data (not test fixtures)
- Verify DATA VALUES (not just structure)
- Re-run ALL parts if any fail
- Document all results

**📖 For universal patterns and detailed examples, see:**
`reference/smoke_testing_pattern.md`


## Exit Criteria

**Smoke Testing (S7.P1) is complete when ALL of these are true:**

- [ ] All steps in this phase complete as specified
- [ ] Agent Status updated with phase completion
- [ ] Ready to proceed to next phase

**If any criterion unchecked:** Complete missing items before proceeding

---
---

## Next Phase

**After completing S7.P1 (Smoke Testing):**

- Smoke testing passed (all 3 parts clean, REAL data verified)
- Proceed to: `stages/s7/s7_p2_qc_rounds.md` (QC Rounds)

**See also:** `prompts_reference_v2.md` → "Starting S7.P2" prompt

---

**END OF STAGE S7.P1 GUIDE**
