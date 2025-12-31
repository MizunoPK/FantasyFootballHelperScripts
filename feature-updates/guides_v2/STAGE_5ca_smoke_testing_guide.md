# STAGE 5ca: Smoke Testing Guide (Post-Implementation - Part 1)

**Purpose:** Verify the feature actually runs and produces correct output through mandatory 3-part smoke testing.

**Stage Flow Context:**
```
Stage 5a (TODO Creation) → Stage 5b (Implementation) →
→ [YOU ARE HERE: Stage 5ca - Smoke Testing] →
→ Stage 5cb (QC Rounds) → Stage 5cc (Final Review) →
→ Stage 5d (Cross-Feature Alignment)
```

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Smoke Testing, you MUST:**

1. **Use the phase transition prompt** from `prompts_reference_v2.md`
   - Find "Starting Stage 5ca (Smoke Testing)" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from this guide

2. **Update README Agent Status** with:
   - Current Phase: POST_IMPLEMENTATION (Smoke Testing)
   - Current Guide: STAGE_5ca_smoke_testing_guide.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "3 parts MANDATORY", "Part 3 verify DATA VALUES", "Re-run ALL 3 if ANY fails"
   - Next Action: Smoke Test Part 1 - Import test

3. **Verify all prerequisites** (see checklist below)

4. **THEN AND ONLY THEN** begin smoke testing

**This is NOT optional.** Reading this guide ensures you don't skip critical validation steps.

---

## Quick Start

**Goal:** Verify the feature actually works with REAL data (not just "tests pass").

**3 Mandatory Parts:**
1. **Part 1: Import Test** - Modules load without errors
2. **Part 2: Entry Point Test** - Script starts correctly
3. **Part 3: E2E Execution Test** - Feature runs end-to-end, OUTPUT DATA VALUES correct

**Critical:** Part 3 must verify ACTUAL DATA VALUES, not just "file exists"

**If ANY part fails:** Fix issues → Re-run ALL 3 parts → Then proceed to Stage 5cb

**Output artifacts:**
- ✅ Part 1 passed (all imports successful)
- ✅ Part 2 passed (entry point works)
- ✅ Part 3 passed (E2E execution with correct data values)

---

## 🛑 Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 3 PARTS ARE MANDATORY
   - Cannot skip any part
   - Must complete in order (Part 1 → 2 → 3)

2. ⚠️ PART 3 MUST VERIFY DATA VALUES
   - Not just "file exists"
   - Not just "file has rows"
   - Verify ACTUAL DATA VALUES are correct
   - Example: If spec says "player passing yards", verify actual yards (not zeros)

3. ⚠️ IF ANY PART FAILS, RE-RUN ALL 3 PARTS
   - Don't just re-run the failed part
   - Fixes can introduce new issues
   - All 3 parts must pass on SAME run

4. ⚠️ USE REAL DATA (Not test fixtures)
   - Part 3 must use production-like data
   - Test fixtures hide integration issues
   - Real data catches mock assumption failures

5. ⚠️ DOCUMENT ALL RESULTS
   - Even if all parts pass
   - Include what was tested, what passed, data samples
   - Update README Agent Status after smoke testing complete

6. ⚠️ WHY SMOKE TESTING IS CRITICAL
   - Real-world case: Feature passed 2,369 unit tests (100%)
   - Smoke testing revealed output files missing 80% of required data
   - Mocks test expectations, not reality
```

---

## Prerequisites Checklist

**Verify these BEFORE starting Smoke Testing:**

**From Stage 5b (Implementation):**
- [ ] All TODO tasks marked done in `todo.md`
- [ ] All unit tests passing (100% pass rate)
- [ ] `code_changes.md` fully updated with all changes
- [ ] `implementation_checklist.md` all requirements verified
- [ ] All code committed to git (clean working directory)

**Files that must exist:**
- [ ] `feature_XX_{name}_spec.md` (primary specification)
- [ ] `feature_XX_{name}_checklist.md` (planning decisions)
- [ ] `feature_XX_{name}_todo.md` (implementation tasks)
- [ ] `feature_XX_{name}_code_changes.md` (change documentation)
- [ ] `feature_XX_{name}_implementation_checklist.md` (requirement verification)

**Verification:**
- [ ] Run `python tests/run_all_tests.py` → exit code 0
- [ ] Check `git status` → no uncommitted implementation changes
- [ ] Review implementation_checklist.md → all items marked verified

**If ANY prerequisite not met:** Return to Stage 5b and complete it first.

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│              SMOKE TESTING WORKFLOW (3 Parts)               │
└─────────────────────────────────────────────────────────────┘

Part 1: Import Test
   ↓ Verify all new modules import successfully
   ↓ (Catches: Import errors, circular dependencies, missing __init__.py)
   ↓
   If PASS → Part 2
   If FAIL → Fix issues, re-run Part 1

Part 2: Entry Point Test
   ↓ Verify script starts and handles arguments correctly
   ↓ (Catches: Argument parsing errors, initialization crashes, config issues)
   ↓
   If PASS → Part 3
   If FAIL → Fix issues, re-run Parts 1 & 2

Part 3: E2E Execution Test (CRITICAL)
   ↓ Execute feature end-to-end with REAL data
   ↓ Verify OUTPUT DATA VALUES are correct (not just "file exists")
   ↓ (Catches: Mock assumption failures, data quality issues, integration bugs)
   ↓
   If PASS → Document results, proceed to Stage 5cb
   If FAIL → Fix issues, RE-RUN ALL 3 PARTS

Re-Reading Checkpoint
   ↓ Re-read Critical Rules
   ↓ Confirm data VALUES verified (not just structure)
   ↓ Update README Agent Status
   ↓
   Proceed to Stage 5cb (QC Rounds)
```

---

## Part 1: Import Test

**Goal:** Verify module loads without errors

**Purpose:** Catch basic integration issues before testing functionality

---

### Process

1. **Identify all new Python modules created in this feature**
   - Check `code_changes.md` for list of new files
   - Example: `league_helper/util/PlayerRatingManager.py`

2. **For each module, run import test:**
   ```bash
   python -c "import module.path.ClassName"
   ```

3. **Verify no errors**
   - Expected: No output (success)
   - If error: Note error message for fixing

---

### What This Catches

- Import errors (missing dependencies)
- Circular dependencies
- Module initialization crashes
- Missing `__init__.py` files
- Syntax errors
- Name errors in imports

---

### Example

```bash
# If feature added: league_helper/util/PlayerRatingManager.py

# Test 1: Import manager class
python -c "from league_helper.util.PlayerRatingManager import PlayerRatingManager"
# Expected: No output (success)
# If error: Fix import issues, re-run Part 1

# Test 2: Import helper functions (if any)
python -c "from league_helper.util.PlayerRatingManager import calculate_rating"
# Expected: No output (success)

# Test 3: Import entire module
python -c "import league_helper.util.PlayerRatingManager"
# Expected: No output (success)
```

---

### Pass Criteria

✅ **PASS if:** All new modules import successfully with zero errors

❌ **FAIL if:** Any import errors occur

---

### If Part 1 Fails

1. **Note the error message**
   ```markdown
   ## Part 1 Import Test - FAILED

   Module: league_helper/util/PlayerRatingManager.py
   Error: ModuleNotFoundError: No module named 'player_rating_api'

   Root cause: Missing dependency in requirements.txt
   Fix: Added 'player-rating-api==1.2.0' to requirements.txt
   ```

2. **Fix the issue**
   - Add missing dependencies
   - Fix circular imports
   - Add missing `__init__.py`
   - Fix syntax errors

3. **Re-run Part 1**
   - Test ALL imports again (not just the failed one)
   - Verify all pass

4. **Then proceed to Part 2**

---

## Part 2: Entry Point Test

**Goal:** Verify script starts correctly and handles arguments properly

**Purpose:** Catch initialization and argument handling issues

---

### Process

1. **Identify entry point script**
   - Usually: `run_league_helper.py`, `run_simulation.py`, etc.
   - Check spec.md "Usage" section if unclear

2. **Test help output:**
   ```bash
   python run_script.py --help
   ```
   - Expected: Shows help text, exits cleanly
   - Verify: Feature-specific help text is present (if applicable)

3. **Test invalid argument handling:**
   ```bash
   python run_script.py --invalid-arg
   ```
   - Expected: Error message like "Unknown argument: --invalid-arg"
   - NOT expected: Stack trace crash

4. **Test script starts (if feature adds new mode):**
   ```bash
   python run_script.py --mode feature_mode --help
   ```
   - Expected: Mode-specific help or graceful error
   - NOT expected: Crash on initialization

---

### What This Catches

- Argument parsing errors
- Script initialization crashes
- Missing configuration files
- Unhelpful error messages
- Mode-specific initialization issues

---

### Example

```bash
# Test 1: Help works
python run_league_helper.py --help
# Expected: Shows help text including new mode (if added)
# ✅ PASS: Help displays correctly

# Test 2: Invalid arg handled gracefully
python run_league_helper.py --invalid-mode
# Expected: "Error: Unknown mode: invalid-mode"
# ✅ PASS: Error message helpful, no stack trace

# Test 3: Feature mode help (if feature adds mode)
python run_league_helper.py --mode rating_helper --help
# Expected: Mode-specific help text
# ✅ PASS: Shows rating helper mode options

# Test 4: Feature mode starts (basic check)
python run_league_helper.py --mode rating_helper --dry-run
# Expected: Script starts, shows "Dry run mode" message
# ✅ PASS: Initialization successful
```

---

### Pass Criteria

✅ **PASS if:**
- `--help` displays help text (includes feature additions if applicable)
- Invalid arguments produce helpful error messages (not stack traces)
- Script starts without initialization crashes
- Feature-specific modes/options work correctly

❌ **FAIL if:**
- Help is missing or incomplete
- Invalid arguments cause crashes
- Script crashes on initialization
- Configuration errors not handled gracefully

---

### If Part 2 Fails

1. **Document the failure**
   ```markdown
   ## Part 2 Entry Point Test - FAILED

   Test: python run_league_helper.py --mode rating_helper
   Error: KeyError: 'rating_multiplier_ranges' in ConfigManager.__init__

   Root cause: Missing config section in league_config.json
   Fix: Added rating_multiplier_ranges to league_config.json template
   ```

2. **Fix the issue**
   - Update argument parsing
   - Fix initialization code
   - Add missing configuration
   - Improve error messages

3. **Re-run Part 1 AND Part 2**
   - Fixes can affect imports
   - Both parts must pass on same run

4. **Then proceed to Part 3**

---

## Part 3: E2E Execution Test (CRITICAL - Verify OUTPUT DATA)

**Goal:** Execute feature end-to-end with REAL data and verify output CONTENT is correct

**⚠️ THIS IS THE MOST IMPORTANT SMOKE TEST**

**Do NOT just check "file exists" - verify **file CONTENT** is correct**

---

### Process

1. **Identify feature's primary use case from spec.md**
   - Example: "Apply player rating multiplier to draft recommendations"
   - Example: "Generate weekly team rankings based on performance"

2. **Prepare real input data (not test fixtures)**
   - Use production data or production-like data
   - Test fixtures can hide integration issues
   - Example: Real player CSV, real team data

3. **Execute feature end-to-end:**
   ```bash
   python run_script.py --mode feature_mode
   ```
   - Let feature run completely
   - Capture any error messages

4. **CRITICAL: Verify output DATA VALUES are correct**

   **❌ NOT SUFFICIENT:**
   ```python
   assert Path("output.csv").exists()  # Just checks file exists
   ```

   **✅ REQUIRED:**
   ```python
   output_file = Path("output.csv")
   assert output_file.exists()

   # Actually READ and VERIFY data
   df = pd.read_csv(output_file)

   # Verify data quality
   assert len(df) > 0, "Output file is empty"
   assert not df['projected_points'].isnull().all(), "All projected_points are null"
   assert df['projected_points'].sum() > 0, "All projected_points are zero"

   # Verify data makes sense
   top_player = df.iloc[0]
   assert top_player['projected_points'] > 100, "Top player has unreasonably low score"
   assert top_player['player_name'] != "", "Player name is empty"
   ```

---

### What This Catches

**Critical issues unit tests miss:**
- Mock assumption failures (tests passed but real code doesn't work)
- Data quality issues (zeros instead of real values, nulls, placeholders)
- Integration bugs (modules don't work together)
- Configuration errors (wrong paths, missing files)
- Algorithm bugs (wrong calculations with real data)

**Real-World Example:**
```
Feature: Add ADP multiplier to player scoring

Unit tests: 2,369 tests passed (100%)
Code review: Looked good

Smoke Test Part 3:
❌ FAILED - All ADP values were 0.0

Root cause: Integration bug - ADP data file path incorrect
Fix: Corrected path in ConfigManager
Re-ran Part 3: ✅ PASSED - ADP values now correct (1.2-50.5 range)

Time saved: 8 hours (would have taken much longer to debug in production)
```

---

### Example - Good vs Bad Part 3

**❌ BAD - Structure Only:**
```python
# Smoke Test Part 3 (INSUFFICIENT)
def test_feature_smoke():
    # Run feature
    subprocess.run(["python", "run_league_helper.py", "--mode", "draft"])

    # Check file exists
    assert Path("data/draft_recommendations.csv").exists()

    print("Smoke test passed!")  # ❌ NO - didn't verify data!
```

**✅ GOOD - Verify Data Values:**
```python
# Smoke Test Part 3 (CORRECT)
def test_feature_smoke():
    # Run feature with REAL data
    result = subprocess.run(
        ["python", "run_league_helper.py", "--mode", "draft"],
        capture_output=True,
        text=True
    )

    # Verify execution success
    assert result.returncode == 0, f"Feature crashed: {result.stderr}"

    # Verify output file exists
    output_file = Path("data/draft_recommendations.csv")
    assert output_file.exists(), "Output file not created"

    # READ actual data
    df = pd.read_csv(output_file)

    # Verify data quality (not just structure)
    assert len(df) > 0, "Output file is empty"
    assert len(df) >= 10, f"Only {len(df)} recommendations (expected ≥10)"

    # Verify required columns exist
    required_cols = ['player_name', 'position', 'projected_points', 'adp_multiplier']
    for col in required_cols:
        assert col in df.columns, f"Missing column: {col}"

    # Verify data VALUES are correct (not zeros/nulls/placeholders)
    assert not df['projected_points'].isnull().all(), "All projected_points are null"
    assert df['projected_points'].sum() > 0, "All projected_points are zero"
    assert not df['adp_multiplier'].isnull().all(), "All adp_multiplier are null"
    assert df['adp_multiplier'].sum() > 0, "All adp_multiplier are zero"

    # Verify values make sense
    top_rec = df.iloc[0]
    assert top_rec['projected_points'] > 100, "Top recommendation has unreasonably low score"
    assert 0.8 <= top_rec['adp_multiplier'] <= 1.5, "ADP multiplier out of expected range"
    assert top_rec['player_name'] != "", "Player name is empty"
    assert top_rec['position'] in ['QB', 'RB', 'WR', 'TE'], "Invalid position"

    # Compare to expected output (if spec has examples)
    # From spec: "Top QB should be Patrick Mahomes with ~350 points"
    qb_recs = df[df['position'] == 'QB']
    assert len(qb_recs) > 0, "No QB recommendations"
    top_qb = qb_recs.iloc[0]
    assert 300 <= top_qb['projected_points'] <= 400, "Top QB score out of expected range"

    print("✅ Smoke test PASSED with data validation!")
```

---

### Specific Validations by Feature Type

**Data Processing Features:**
- Verify row counts match expected (no data loss)
- Verify calculations correct (spot-check a few rows manually)
- Verify no null values where data should exist
- Verify value ranges make sense

**Ranking/Scoring Features:**
- Verify rankings in correct order (highest to lowest)
- Verify score values in expected range
- Verify no ties where shouldn't be (if applicable)
- Verify multipliers actually applied (compare to baseline)

**File Generation Features:**
- Verify file format correct (CSV columns, JSON structure)
- Verify file content complete (not partial data)
- Verify file encoding correct (no garbled text)
- Verify file can be read by consumers

**API Integration Features:**
- Verify API called successfully (check logs)
- Verify API response parsed correctly
- Verify API data stored correctly
- Verify fallback behavior if API fails

---

### Pass Criteria

✅ **PASS if:**
- Feature executes without crashes
- Output files created in correct locations
- **Output DATA VALUES are correct** (not zeros, nulls, placeholders)
- Data values match expectations from spec
- Primary use case from spec.md is achievable
- Manual inspection confirms data looks right

❌ **FAIL if:**
- Feature crashes
- Output files missing or empty
- Output data is zeros, nulls, or placeholder values
- Data values don't match spec expectations
- Data ranges don't make sense
- Primary use case cannot be achieved

---

### If Part 3 Fails

1. **Document the failure in detail**
   ```markdown
   ## Part 3 E2E Execution Test - FAILED

   Primary use case: Apply ADP multiplier to draft recommendations

   Test execution: python run_league_helper.py --mode draft

   Results:
   ✅ Script ran without crash
   ✅ Output file created: data/draft_recommendations.csv
   ❌ Data validation FAILED:
      - Column 'adp_multiplier': All values are 0.0 (expected: 0.8-1.5 range)
      - Column 'adp_rank': All values are 0 (expected: 1-500 range)

   Data sample (first 3 rows):
   | player_name    | position | projected_points | adp_multiplier | adp_rank |
   |----------------|----------|------------------|----------------|----------|
   | Patrick Mahomes| QB       | 342.5            | 0.0            | 0        |
   | Christian MC   | RB       | 298.2            | 0.0            | 0        |
   | Tyreek Hill    | WR       | 285.1            | 0.0            | 0        |

   Root cause analysis:
   - ADP data file path in ConfigManager is incorrect
   - Path: "data/rankings/adp.csv" (spec says "data/adp_rankings.csv")
   - ADP data never loaded, all players defaulted to 0

   Fix applied:
   - Updated ConfigManager.py line 156: path = "data/adp_rankings.csv"
   - Verified adp_rankings.csv exists and has correct format
   ```

2. **Fix ALL issues**
   - Don't just fix what you found
   - Look for related issues (if one bug exists, are there others?)
   - Fix root causes (not symptoms)

3. **RE-RUN ALL 3 SMOKE TEST PARTS**
   - ⚠️ Do NOT just re-run Part 3
   - Fixes can introduce new import/initialization issues
   - All 3 parts must pass on SAME run

4. **Document retest results**
   ```markdown
   ## Smoke Test Retest Results

   After fix: Updated ADP file path

   Part 1 (Import Test): ✅ PASSED (all imports successful)
   Part 2 (Entry Point Test): ✅ PASSED (script starts correctly)
   Part 3 (E2E Execution Test): ✅ PASSED with data validation

   Part 3 data verification:
   - Column 'adp_multiplier': Values range 0.85-1.42 ✅
   - Column 'adp_rank': Values range 1-487 ✅
   - Top player (Patrick Mahomes): rank 2, multiplier 1.42 ✅
   - Manual spot-check: Top 10 players have expected ADP ranks ✅

   All smoke tests PASSED. Ready for Stage 5cb (QC Rounds).
   ```

---

## Smoke Testing Completion

**After ALL 3 parts pass:**

1. **Document smoke test results in README Agent Status**
   ```markdown
   **Progress:** Smoke testing complete (all 3 parts passed)
   **Part 1:** Import Test - PASSED
   **Part 2:** Entry Point Test - PASSED
   **Part 3:** E2E Execution Test - PASSED (data values verified)
   **Data Validation:** Top player score 342.5, ADP multiplier 1.42, rank 2
   **Next Action:** Proceed to Stage 5cb (QC Round 1)
   ```

2. **Update Epic Checklist**
   ```markdown
   - [x] Feature_XX smoke testing passed
   ```

3. **Proceed to Stage 5cb (QC Round 1)**

---

**If ANY part failed and you fixed it:**
- ⚠️ **Re-run ALL 3 smoke test parts** (fixes can introduce new issues)
- Don't proceed to Stage 5cb until all 3 parts pass on same run
- Document what failed, what was fixed, and retest results

---

## 🔄 Re-Reading Checkpoint

**STOP - Before proceeding to Stage 5cb:**

1. **Re-read "Critical Rules" section at top of this guide**
   - Did you verify OUTPUT DATA VALUES? (not just "file exists")
   - Did all 3 parts pass?
   - If you fixed issues, did you re-run ALL 3 parts?

2. **Verify you actually verified data**
   - Did you open output files and inspect actual data?
   - Did you verify values make sense (not zeros, nulls)?
   - Did you compare to expected output from spec?

3. **Confirm all 3 smoke test parts passed**
   - Part 1: Import Test ✅
   - Part 2: Entry Point Test ✅
   - Part 3: E2E Execution Test ✅ (with data validation)

4. **Update README Agent Status:**
   ```markdown
   Guide Last Re-Read: {timestamp}
   Checkpoint: Smoke testing complete, ready for QC Round 1
   Next Guide: STAGE_5cb_qc_rounds_guide.md
   ```

---

## Common Mistakes to Avoid

### Anti-Pattern 1: "File Exists" Validation

**❌ Mistake:**
```python
# Smoke Test Part 3
assert Path("output.csv").exists()  # NOT SUFFICIENT
print("Smoke test passed!")
```

**Why wrong:** File might exist but be empty, contain zeros, or have wrong data

**✅ Correct:**
```python
# Smoke Test Part 3
assert Path("output.csv").exists()

# Actually verify DATA
df = pd.read_csv("output.csv")
assert len(df) > 0, "Output file is empty"
assert not df['score'].isnull().all(), "All scores are null"
assert df['score'].sum() > 0, "All scores are zero"
```

---

### Anti-Pattern 2: Skipping Part 3 Data Verification

**❌ Mistake:**
"File was created and has 1000 rows, that's good enough"

**Why wrong:** Rows might be all zeros, nulls, or placeholder data

**✅ Correct:** Actually inspect data values, verify they make sense

---

### Anti-Pattern 3: Not Re-Running All Parts After Fixes

**❌ Mistake:**
```
Part 3 failed
Fixed the issue
Re-ran only Part 3
```

**Why wrong:** Fix might have broken imports or initialization

**✅ Correct:** Always re-run ALL 3 parts after ANY fix

---

### Anti-Pattern 4: Using Test Fixtures Instead of Real Data

**❌ Mistake:**
"I'll use test fixtures for Part 3, they're easier to verify"

**Why wrong:** Test fixtures hide integration issues with real data

**✅ Correct:** Use production or production-like data for Part 3

---

## Prerequisites for Next Stage

**Before transitioning to Stage 5cb (QC Rounds), verify:**

**Smoke Testing Complete:**
- [ ] Part 1 (Import Test): PASSED
- [ ] Part 2 (Entry Point Test): PASSED
- [ ] Part 3 (E2E Execution Test): PASSED with DATA VALUES verified

**Documentation:**
- [ ] Smoke test results documented in README Agent Status
- [ ] If failures occurred, documented what failed, fix, retest results
- [ ] Epic Checklist updated: `- [x] Feature_XX smoke testing passed`

**Data Validation:**
- [ ] Actually opened output files and inspected data
- [ ] Verified data values are correct (not zeros, nulls, placeholders)
- [ ] Verified data ranges make sense
- [ ] Primary use case from spec achievable

**Ready for Next Stage:**
- [ ] All 3 parts passed on SAME run (no mix of old/new results)
- [ ] Confident feature works with real data
- [ ] No critical issues found

**If ALL verified:** Ready for Stage 5cb (QC Rounds)

**If ANY unverified:** Complete smoke testing first

---

## Next Stage

**After completing smoke testing:**

📖 **READ:** `STAGE_5cb_qc_rounds_guide.md`
🎯 **GOAL:** Comprehensive quality control through 3 validation rounds
⏱️ **ESTIMATE:** 1-2 hours

**Stage 5cb will:**
- QC Round 1: Basic validation (tests, structure, interfaces)
- QC Round 2: Deep verification (baseline, logs, data quality)
- QC Round 3: Final skeptical review (fresh eyes, re-read specs)

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Stage 5cb.

---

*End of STAGE_5ca_smoke_testing_guide.md*
