# Smoke Testing Pattern (Reference)

**Purpose:** Generic smoke testing workflow applicable to both feature-level (S7.P1) and epic-level (S9.P1) testing.

**This is a REFERENCE PATTERN.** Actual guides:
- **Feature-level:** `stages/s7/s7_p1_smoke_testing.md`
- **Epic-level:** `stages/s9/s9_p1_epic_smoke_testing.md`

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

```
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

### 1. ALL Parts Are MANDATORY
- Cannot skip any part
- Must complete in order (Part 1 → 2 → 3 → [4 if epic])
- Each part validates different aspect

### 2. Part 3 MUST Verify DATA VALUES
```python
# ❌ NOT SUFFICIENT:
assert Path("output.csv").exists()  # Just checks file exists

# ✅ REQUIRED:
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

```
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
# WRONG - only checks file exists
assert Path("output.csv").exists()

# CORRECT - verifies data values
df = pd.read_csv("output.csv")
assert df['score'].between(0, 500).all()
assert df['projected_points'].sum() > 0
```

### ❌ Mistake 2: Using Test Fixtures for Part 3
```python
# WRONG - test fixtures hide integration issues
test_data = create_mock_players()  # Mocked data

# CORRECT - use real production-like data
real_data = pd.read_csv("data/real_players.csv")  # Real data
```

### ❌ Mistake 3: Partial Re-run After Failure
```python
# WRONG - only re-running failed Part 3
# (skipping Parts 1 & 2)

# CORRECT - re-running ALL 3 parts from Part 1
# Fixes can affect earlier parts
```

### ❌ Mistake 4: Accepting Placeholder/Zero Data
```python
# WRONG - data exists but values are wrong
assert len(df) > 0  # File has rows, but all zeros

# CORRECT - verify data values are reasonable
assert df['projected_points'].sum() > 0  # Not all zeros
assert df['adp'].min() > 0  # Not placeholder values
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
- **Next Stage:** S9.P2 (Epic QC Rounds) if passed
- **Restart Destination:** S9.P1 Step 1 (complete epic smoke testing)

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
