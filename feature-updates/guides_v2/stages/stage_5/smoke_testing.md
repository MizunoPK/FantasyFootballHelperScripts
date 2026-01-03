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
   - Current Guide: stages/stage_5/smoke_testing.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "3 parts MANDATORY", "Part 3 verify DATA VALUES", "Re-run ALL 3 if ANY fails"
   - Next Action: Smoke Test Part 1 - Import test

3. **Verify all prerequisites** (see checklist below)

4. **THEN AND ONLY THEN** begin smoke testing

**This is NOT optional.** Reading this guide ensures you don't skip critical validation steps.

---

## Quick Start

**What is this stage?**
Smoke Testing is the first post-implementation validation where you verify the feature works end-to-end with REAL data through 3 mandatory parts: import test, entry point test, and E2E execution test with data value inspection.

**When do you use this guide?**
- Stage 5b complete (Implementation Execution finished)
- Feature code is written
- Ready to validate with real data

**Key Outputs:**
- ✅ Part 1 PASSED: Import Test (all modules load without errors)
- ✅ Part 2 PASSED: Entry Point Test (script starts correctly)
- ✅ Part 3 PASSED: E2E Execution Test (feature runs end-to-end, data values verified)
- ✅ Data values inspected (not zeros, nulls, or placeholders)
- ✅ Ready for Stage 5cb (QC Rounds)

**Time Estimate:**
15-30 minutes

**Exit Condition:**
Smoke Testing is complete when ALL 3 parts pass (including data value verification in Part 3), output files are inspected and confirmed correct, and you're ready to proceed to QC Rounds

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

## Critical Decisions Summary

**Stage 5ca has 1 MANDATORY GATE (Part 3 - E2E Execution):**

### Decision Point 1: Part 3 - E2E Execution Test (PASS/FAIL)
**Question:** Does Part 3 pass with CORRECT DATA VALUES (not just "file exists")?

**Part 3 has 2 sub-parts (BOTH must pass):**
- **Part 3a:** Run E2E test with REAL data, verify output file structure/format
- **Part 3b:** Data Sanity Validation - Verify ACTUAL DATA VALUES are correct (statistical checks)

**If Part 3 FAILS (either 3a or 3b):**
- ❌ STOP smoke testing
- Fix the issue(s)
- Re-run ALL 3 PARTS (not just Part 3)
- Do NOT proceed to Stage 5cb (QC Rounds) until ALL 3 parts pass

**If Part 3 PASSES (both 3a and 3b with correct data values):**
- ✅ Smoke testing complete
- Proceed to Stage 5cb (QC Rounds)

**Impact:** Skipping Part 3b data validation allows "successful" features that produce wrong data (real-world case: 80% of required data missing despite 100% test pass rate)

---

**Secondary Decision: If ANY Part Fails During Smoke Testing**
**Question:** After fixing issues, re-run from Part 1 or just re-run failed part?
- **ALWAYS re-run ALL 3 PARTS from beginning**
- Fixes can introduce new import/integration issues
- All 3 parts must pass on SAME run
- **Impact:** Partial re-runs miss cascading failures from fixes

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

5. **CRITICAL: Verify data values for EACH category/type**

   **If feature processes multiple categories (positions, file types, etc.):**
   - Don't just check totals - verify PER-CATEGORY
   - Sample one item from each category and check actual data values
   - Example: If updating 6 positions (QB, RB, WR, TE, K, DST), verify data for ALL 6

   **Example:**
   ```python
   # Feature updates 6 position files
   positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']

   for pos in positions:
       pos_file = Path(f"data/{pos.lower()}_data.json")
       assert pos_file.exists(), f"{pos} file missing"

       # Verify data VALUES (not just file exists)
       with open(pos_file) as f:
           data = json.load(f)
       assert len(data) > 0, f"{pos} file is empty"

       # Check first player has updated data
       first_player = data[0]
       assert first_player['adp'] != 170.0, f"{pos} ADP not updated (still placeholder)"
       assert first_player['adp'] > 0, f"{pos} ADP is invalid"
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

   All smoke tests PASSED. Ready for Part 3b (Data Sanity Validation).
   ```

---

## Part 3b: Data Sanity Validation - Statistical Checks (CRITICAL)

**Goal:** Verify output data is statistically realistic (not all zeros, has variance, in expected range)

**Historical Context:** Feature 02 catastrophic bug - smoke testing showed "(0 have non-zero actual points)" but was marked PASS anyway. All actual_points were 0.0, making MAE calculations meaningless. This section would have caught that bug immediately.

**⚠️ THIS IS A MANDATORY ADDITION TO PART 3**

---

### Why This Matters

**Part 3 verified:** Data exists, structure correct, values > 0

**Part 3b verifies:** Data is REALISTIC for the domain (NFL scoring, player stats, etc.)

**Example of bug Part 3 missed but Part 3b catches:**
```python
# Part 3 checks:
assert df['actual_points'].sum() > 0  # ✅ PASSED (sum = 0.1)

# But data looks like:
# actual_points: [0.0, 0.0, 0.0, ..., 0.1, 0.0, 0.0]  # Only 1 non-zero!

# Part 3b catches this:
zero_pct = (df['actual_points'] == 0.0).sum() / len(df) * 100
assert zero_pct < 90%, f"Zero percentage too high: {zero_pct}%"  # ❌ FAILED (99.5% zeros)
```

---

### Statistical Validation Process

**Run these checks ON THE SAME OUTPUT DATA from Part 3:**

---

#### Check 1: Zero Percentage

**Purpose:** Detect if data is mostly zeros (common bug pattern)

**Method:**
```python
# Calculate zero percentage for each numeric column
for col in ['actual_points', 'projected_points', 'adp_multiplier']:
    if col in df.columns:
        zero_count = (df[col] == 0.0).sum()
        total_count = len(df)
        zero_pct = (zero_count / total_count) * 100

        print(f"{col}: {zero_pct:.1f}% zeros ({zero_count}/{total_count})")

        # CRITICAL: Fail if >90% zeros
        assert zero_pct < 90.0, f"{col} has {zero_pct:.1f}% zeros (too high - data loading issue?)"
```

**Pass criteria:** < 90% zeros
**Typical good value:** 20-40% zeros (some players didn't play, some weeks incomplete)

**AUTOMATIC FAIL if:**
- "0 have non-zero values" (100% zeros)
- >90% zeros (almost all zeros)

---

#### Check 2: Variance Check

**Purpose:** Detect if all values are the same (no variance)

**Method:**
```python
import statistics

for col in ['actual_points', 'projected_points', 'adp_multiplier']:
    if col in df.columns:
        values = df[col].tolist()

        # Calculate standard deviation
        if len(values) > 1:
            std_dev = statistics.stdev(values)
            mean = statistics.mean(values)

            print(f"{col}: mean={mean:.2f}, std_dev={std_dev:.2f}")

            # CRITICAL: Fail if stddev = 0 (all same value)
            assert std_dev > 0, f"{col} has zero variance (all values are {mean})"
        else:
            print(f"⚠️  {col}: Only 1 value, cannot calculate variance")
```

**Pass criteria:** std_dev > 0
**Typical good value:** std_dev > 5.0 for scoring data

**AUTOMATIC FAIL if:**
- std_dev = 0 (all values identical)
- std_dev < 0.1 (suspiciously low variance)

---

#### Check 3: Realistic Range Check

**Purpose:** Verify values are in domain-realistic ranges (NFL scoring, not random numbers)

**Method:**
```python
# Define realistic ranges for your domain
realistic_ranges = {
    'actual_points': (0, 50),      # NFL: 0-50 points per game typical
    'projected_points': (0, 400),  # NFL season: 0-400 points typical
    'adp_multiplier': (0.5, 2.0),  # Multipliers: 0.5x to 2.0x typical
    'adp_rank': (1, 500),          # ADP: 1-500 valid range
}

for col, (min_expected, max_expected) in realistic_ranges.items():
    if col in df.columns:
        actual_min = df[col].min()
        actual_max = df[col].max()

        print(f"{col}: range [{actual_min:.2f}, {actual_max:.2f}] (expected [{min_expected}, {max_expected}])")

        # Warn if outside expected range (not automatic fail, but suspicious)
        if actual_min < min_expected or actual_max > max_expected:
            print(f"⚠️  {col} outside expected range - verify this is correct")

        # CRITICAL: Fail if values are absurdly wrong
        assert actual_min >= -100, f"{col} min value ({actual_min}) is absurdly negative"
        assert actual_max <= 10000, f"{col} max value ({actual_max}) is absurdly high"
```

**Pass criteria:** Values in reasonable range for domain
**Typical good value:** Within expected min/max, no absurd outliers

---

#### Check 4: Non-Zero Count

**Purpose:** Verify enough players have non-zero values (not just 1-2 players)

**Method:**
```python
for col in ['actual_points', 'projected_points']:
    if col in df.columns:
        non_zero_count = (df[col] > 0).sum()
        total_count = len(df)
        non_zero_pct = (non_zero_count / total_count) * 100

        print(f"{col}: {non_zero_count}/{total_count} have non-zero values ({non_zero_pct:.1f}%)")

        # CRITICAL: Fail if 0 non-zero values (Feature 02 bug pattern)
        assert non_zero_count > 0, f"{col}: CRITICAL BUG - 0 have non-zero values"

        # CRITICAL: Fail if <10% non-zero (suspiciously low)
        assert non_zero_pct > 10.0, f"{col}: Only {non_zero_pct:.1f}% non-zero (data loading issue?)"
```

**Pass criteria:** > 10% non-zero values
**Typical good value:** 50-80% non-zero (most players have values)

**AUTOMATIC FAIL if:**
- "(0 have non-zero values)" - CRITICAL BUG
- < 10% non-zero - suspiciously low

---

#### Check 5: Distribution Sanity

**Purpose:** Verify data distribution makes sense (not all min, all max, or bimodal when shouldn't be)

**Method:**
```python
for col in ['actual_points', 'projected_points']:
    if col in df.columns:
        values = df[col].tolist()

        # Calculate quartiles
        q1 = df[col].quantile(0.25)
        median = df[col].quantile(0.50)
        q3 = df[col].quantile(0.75)

        print(f"{col}: Q1={q1:.2f}, Median={median:.2f}, Q3={q3:.2f}")

        # Check for suspicious distributions
        if q1 == median == q3:
            print(f"⚠️  {col}: All quartiles equal - suspicious distribution")

        # Verify reasonable spread
        iqr = q3 - q1  # Interquartile range
        print(f"{col}: IQR={iqr:.2f}")

        assert iqr > 0, f"{col}: Zero IQR (no spread in data)"
```

**Pass criteria:** Reasonable distribution (quartiles differ, IQR > 0)

---

### Complete Example - Data Sanity Validation

```python
def validate_data_sanity(df, col_name, domain_min, domain_max):
    """
    Comprehensive sanity check for a data column.

    Args:
        df: DataFrame with output data
        col_name: Column to validate
        domain_min: Minimum realistic value for this domain
        domain_max: Maximum realistic value for this domain

    Returns:
        dict with validation results
    """
    import statistics

    print(f"\n=== Data Sanity Validation: {col_name} ===")

    if col_name not in df.columns:
        print(f"⚠️  Column '{col_name}' not found in data")
        return {'status': 'SKIPPED', 'reason': 'Column not found'}

    values = df[col_name].tolist()
    total_count = len(values)

    # Check 1: Zero percentage
    zero_count = (df[col_name] == 0.0).sum()
    zero_pct = (zero_count / total_count) * 100
    print(f"✓ Zero percentage: {zero_pct:.1f}% ({zero_count}/{total_count})")

    # Check 2: Non-zero count
    non_zero_count = total_count - zero_count
    non_zero_pct = (non_zero_count / total_count) * 100
    print(f"✓ Non-zero count: {non_zero_count}/{total_count} ({non_zero_pct:.1f}%)")

    # Check 3: Variance
    if non_zero_count > 1:
        std_dev = statistics.stdev(values)
        mean = statistics.mean(values)
        print(f"✓ Mean: {mean:.2f}, Std Dev: {std_dev:.2f}")
    else:
        std_dev = 0
        mean = values[0] if values else 0
        print(f"⚠️  Insufficient data for variance (only {non_zero_count} non-zero values)")

    # Check 4: Range
    actual_min = df[col_name].min()
    actual_max = df[col_name].max()
    print(f"✓ Range: [{actual_min:.2f}, {actual_max:.2f}]")
    print(f"  Expected range: [{domain_min}, {domain_max}]")

    # Check 5: Distribution
    if non_zero_count >= 4:
        q1 = df[col_name].quantile(0.25)
        median = df[col_name].quantile(0.50)
        q3 = df[col_name].quantile(0.75)
        iqr = q3 - q1
        print(f"✓ Distribution: Q1={q1:.2f}, Median={median:.2f}, Q3={q3:.2f}, IQR={iqr:.2f}")
    else:
        print(f"⚠️  Insufficient data for distribution analysis")
        iqr = 0

    # CRITICAL VALIDATIONS (automatic fail)
    failures = []

    if non_zero_count == 0:
        failures.append(f"🔴 CRITICAL: 0 have non-zero values (100% zeros)")

    if zero_pct > 90.0:
        failures.append(f"🔴 CRITICAL: {zero_pct:.1f}% zeros (>90% threshold)")

    if std_dev == 0 and non_zero_count > 1:
        failures.append(f"🔴 CRITICAL: Zero variance (all values are {mean})")

    if actual_min < domain_min * 10 or actual_max > domain_max * 10:
        failures.append(f"🔴 CRITICAL: Values outside realistic range by 10x")

    if non_zero_pct < 10.0 and zero_count > 0:
        failures.append(f"🔴 CRITICAL: Only {non_zero_pct:.1f}% non-zero values (<10% threshold)")

    # Report results
    if failures:
        print("\n❌ SANITY CHECK FAILED:")
        for failure in failures:
            print(f"  {failure}")
        return {'status': 'FAILED', 'failures': failures}
    else:
        print("\n✅ SANITY CHECK PASSED")
        return {'status': 'PASSED'}

# Usage in smoke test:
df = pd.read_csv("output.csv")

# Validate each numeric column
validate_data_sanity(df, 'actual_points', domain_min=0, domain_max=50)
validate_data_sanity(df, 'projected_points', domain_min=0, domain_max=400)
validate_data_sanity(df, 'adp_multiplier', domain_min=0.5, domain_max=2.0)
```

---

### Critical Question Checklist

**Before marking Part 3b PASSED, answer these questions:**

```markdown
## Part 3b Critical Questions

**Data Reality Checks:**
- [ ] If I saw these values in production, would I be suspicious?
- [ ] Are zero percentages realistic for this domain?
- [ ] Is the variance what I'd expect for real data?
- [ ] Are the min/max values possible in the real world?

**Feature 02 Prevention:**
- [ ] Did I see "(0 have non-zero values)" anywhere?
  - If YES → AUTOMATIC FAIL (Feature 02 bug pattern)
- [ ] Is >90% of data zeros?
  - If YES → AUTOMATIC FAIL (data loading issue)
- [ ] Is standard deviation = 0?
  - If YES → AUTOMATIC FAIL (all same value)

**Domain Knowledge:**
- [ ] Do these values make sense for NFL scoring?
- [ ] Are player stats in realistic ranges?
- [ ] Would a domain expert agree these values look right?
```

**All questions must be answered YES (or NO for fail conditions) to pass Part 3b.**

---

### AUTOMATIC FAIL Conditions

**Part 3b automatically FAILS if ANY of these are true:**

```
❌ "(0 have non-zero values)" - CRITICAL BUG (Feature 02 pattern)
❌ >90% zeros - Data loading issue
❌ Standard deviation = 0 - All values identical
❌ <10% non-zero values - Suspiciously low
❌ Min/max outside realistic range by 10x - Absurd values
❌ Answer "I would be suspicious" to production question
```

**If ANY automatic fail condition is true:**
1. Mark Part 3b as FAILED
2. Document which condition failed
3. Fix the underlying issue (usually data loading or calculation bug)
4. Re-run ALL smoke test parts (1, 2, 3, 3b)

---

### Feature 02 Example - How Part 3b Would Have Caught The Bug

**What actually happened (WITHOUT Part 3b):**
```
Part 3 E2E Execution Test: ✅ PASSED
- Feature executed without crash
- Output files created
- Data structure correct
- Sum of actual_points > 0  # Sum was 0.1 (barely > 0)

Smoke testing marked PASSED
Bug survived to user final review
```

**What would have happened (WITH Part 3b):**
```
Part 3b Data Sanity Validation: ❌ FAILED

actual_points validation:
- Zero percentage: 99.8% (2499/2500) 🔴 CRITICAL: >90% threshold
- Non-zero count: 1/2500 (0.04%) 🔴 CRITICAL: <10% threshold
- Std Dev: 0.02
- Range: [0.0, 0.1]

🔴 AUTOMATIC FAIL: "(0 have non-zero values)" pattern detected
🔴 AUTOMATIC FAIL: 99.8% zeros (>90% threshold)

Root cause: Loading week_N folder instead of week_N+1 for actuals
Result: All actual_points[N] are 0.0 (week N not complete yet)

Fix: Load week_N+1 folder for actuals
Retest: Part 3b PASSED (0.1% zeros, reasonable variance)
```

**Part 3b would have caught the bug immediately and prevented it from reaching implementation.**

---

### Pass Criteria for Part 3b

✅ **PASS if:**
- Zero percentage < 90% for all numeric columns
- At least 10% of values are non-zero
- Standard deviation > 0 (data has variance)
- Values in realistic range for domain
- No automatic fail conditions triggered
- Answer "NO" to "would I be suspicious in production?"

❌ **FAIL if:**
- ANY automatic fail condition triggered
- Zero percentage >= 90%
- Non-zero percentage < 10%
- Standard deviation = 0
- Values absurdly outside realistic range
- Answer "YES" to "would I be suspicious in production?"

---

## Smoke Testing Completion

**After ALL 4 parts pass (1, 2, 3, 3b):**

1. **Document smoke test results in README Agent Status**
   ```markdown
   **Progress:** Smoke testing complete (all 4 parts passed: Import, Entry Point, E2E Execution, Data Sanity)
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
   Next Guide: stages/stage_5/qc_rounds.md
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

## Stage 5ca Complete Checklist (Smoke Testing)

**Smoke Testing is COMPLETE when ALL of these are true:**

### All 3 Parts Passed
- [ ] Part 1: Import Test PASSED (all modules load without errors)
- [ ] Part 2: Entry Point Test PASSED (script starts correctly)
- [ ] Part 3: E2E Execution Test PASSED (feature runs end-to-end)
  - [ ] Part 3a: Output file structure/format correct
  - [ ] Part 3b: DATA VALUES verified (not just file exists)

### Data Validation Complete
- [ ] Actually opened output files and inspected data
- [ ] Verified data values are correct (not zeros, nulls, placeholders)
- [ ] Verified data ranges make sense (statistical checks passed)
- [ ] Primary use case from spec is achievable with actual data

### All 3 Parts on SAME Run
- [ ] If ANY part failed during testing, re-ran ALL 3 parts from beginning
- [ ] All 3 parts passed on SAME test run (no mix of old/new results)
- [ ] No issues introduced by fixes

### Documentation Complete
- [ ] Smoke test results documented in feature README Agent Status
- [ ] If failures occurred, documented: what failed, fix applied, retest results
- [ ] Epic EPIC_README.md updated: Feature smoke testing marked complete

**If ANY item unchecked → Smoke Testing NOT complete**

**Critical Verification:**
- Part 3b data validation is MANDATORY (not optional)
- Used REAL data (not test fixtures)
- Confident feature works with production-like data

**When ALL items checked:**
✅ Stage 5ca COMPLETE
→ Proceed to Stage 5cb (QC Rounds)

**Next Guide:** `stages/stage_5/qc_rounds.md`

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

📖 **READ:** `stages/stage_5/qc_rounds.md`
🎯 **GOAL:** Comprehensive quality control through 3 validation rounds
⏱️ **ESTIMATE:** 1-2 hours

**Stage 5cb will:**
- QC Round 1: Basic validation (tests, structure, interfaces)
- QC Round 2: Deep verification (baseline, logs, data quality)
- QC Round 3: Final skeptical review (fresh eyes, re-read specs)

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Stage 5cb.

---

*End of stages/stage_5/smoke_testing.md*
