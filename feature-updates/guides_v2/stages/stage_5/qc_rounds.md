# STAGE 5cb: QC Rounds Guide (Post-Implementation - Part 2)

**Purpose:** Comprehensive quality control through 3 validation rounds to ensure feature correctness, data quality, and completeness.

**Stage Flow Context:**
```
Stage 5ca (Smoke Testing) →
→ [YOU ARE HERE: Stage 5cb - QC Rounds] →
→ Stage 5cc (Final Review) → Stage 5d (Cross-Feature Alignment)
```

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting QC Rounds, you MUST:**

1. **Use the phase transition prompt** from `prompts_reference_v2.md`
   - Find "Starting Stage 5cb (QC Rounds)" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from this guide

2. **Update README Agent Status** with:
   - Current Phase: POST_IMPLEMENTATION (QC Rounds)
   - Current Guide: STAGE_5cb_qc_rounds_guide.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "3 rounds MANDATORY", "QC restart if ANY issues", "Round 3 = zero issues or restart"
   - Next Action: QC Round 1 - Basic Validation

3. **Verify all prerequisites** (see checklist below)

4. **THEN AND ONLY THEN** begin QC rounds

**This is NOT optional.** Reading this guide ensures you complete all validation rounds.

---

## Quick Start

**What is this stage?**
QC Rounds is the comprehensive validation phase where you perform 3 progressively deeper quality checks (Basic Validation, Deep Verification, Final Skeptical Review) with zero tech debt tolerance and mandatory restart if issues found.

**When do you use this guide?**
- Stage 5ca complete (Smoke Testing passed all 3 parts)
- Ready for comprehensive quality validation
- Before final review

**Key Outputs:**
- ✅ Round 1 PASSED: Basic Validation (<3 critical issues, 100% requirements met)
- ✅ Round 2 PASSED: Deep Verification (all Round 1 issues resolved, zero new critical)
- ✅ Round 3 PASSED: Final Skeptical Review (ZERO issues found)
- ✅ All issues fixed with zero tech debt
- ✅ Ready for Stage 5cc (Final Review)

**Time Estimate:**
30-60 minutes (all 3 rounds, assuming no major issues)

**Exit Condition:**
QC Rounds are complete when all 3 rounds pass (Round 3 with ZERO issues), no tech debt remains, and you're ready to proceed to Final Review

---

## 🛑 Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL 3 ROUNDS ARE MANDATORY
   - Cannot skip any round
   - Must complete in order (Round 1 → 2 → 3)
   - Each round has DIFFERENT focus

2. ⚠️ QC RESTART PROTOCOL
   - If Round 1: ≥3 critical issues OR <100% requirements met → RESTART
   - If Round 2: Any Round 1 issues unresolved OR new critical issues → RESTART
   - If Round 3: ANY issues found → RESTART
   - Restart = Re-run smoke testing + all 3 QC rounds

3. ⚠️ NO PARTIAL WORK ACCEPTED - ZERO TECH DEBT TOLERANCE
   - "File structure correct but data pending" = INCOMPLETE (not acceptable)
   - "Method exists but returns placeholder values" = INCOMPLETE (not acceptable)
   - "Stat arrays created but filled with zeros" = INCOMPLETE (not acceptable)
   - "90% complete, will finish later" = INCOMPLETE (not acceptable)
   - Rule: If feature cannot achieve 100% of spec requirements, it's INCOMPLETE
   - NO shortcuts, NO "temporary" solutions, NO deferred work
   - Feature must be production-ready with ZERO tech debt

4. ⚠️ EACH ROUND HAS UNIQUE FOCUS
   - Round 1: Basic validation (does it work?)
   - Round 2: Deep verification (does it work correctly?)
   - Round 3: Skeptical review (is it ACTUALLY complete?)
   - Cannot skip rounds - each catches different issues

5. ⚠️ DATA VALUES NOT JUST STRUCTURE
   - Every round must verify data VALUES are correct
   - Example: Don't just check "column exists", verify values make sense
   - Example: Don't just check "logs exist", verify no unexpected WARNINGs

6. ⚠️ RE-READING CHECKPOINTS
   - After Round 1 → re-read "Common Mistakes"
   - After Round 2 → re-read critical rules
   - Before Round 3 → re-read spec with fresh eyes

7. ⚠️ ALGORITHM VERIFICATION
   - Implementation must match spec EXACTLY
   - Re-check Algorithm Traceability Matrix from Stage 5a
   - Every algorithm in spec must map to exact code location
   - Code behavior must match spec behavior

8. ⚠️ 100% REQUIREMENT COMPLETION
   - ALL spec requirements must be implemented
   - ALL checklist items must be verified
   - NO "we'll add that later" items
   - Feature is DONE or NOT DONE (no partial credit)
```

---

## Critical Decisions Summary

**Stage 5cb has 3 major decision points (RESTART triggers):**

### Decision Point 1: QC Round 1 Outcome (CONTINUE/RESTART)
**Question:** Does Round 1 meet acceptance criteria?
- **Acceptance criteria:**
  - <3 critical issues found
  - 100% requirements met (no partial implementations)
- **If Round 1 FAILS (≥3 critical OR <100% requirements):**
  - ❌ RESTART from smoke testing
  - Re-run Stage 5ca (all 3 smoke test parts)
  - Re-run ALL 3 QC rounds after smoke testing passes
- **If Round 1 PASSES (<3 critical AND 100% requirements):**
  - ✅ Proceed to QC Round 2
- **Impact:** Skipping restart allows broken features to proceed

---

### Decision Point 2: QC Round 2 Outcome (CONTINUE/RESTART)
**Question:** Are ALL Round 1 issues resolved AND zero new critical issues found?
- **Acceptance criteria:**
  - ALL Round 1 issues resolved (none remaining)
  - Zero new critical issues found in Round 2
- **If Round 2 FAILS (any Round 1 issues unresolved OR new critical issues):**
  - ❌ RESTART from smoke testing
  - Re-run Stage 5ca (all 3 smoke test parts)
  - Re-run ALL 3 QC rounds
- **If Round 2 PASSES (Round 1 issues resolved AND zero new critical issues):**
  - ✅ Proceed to QC Round 3
- **Impact:** Partial fixes or new issues indicate unstable implementation

---

### Decision Point 3: QC Round 3 Outcome (COMPLETE/RESTART)
**Question:** ZERO issues found in skeptical fresh-eyes review?
- **Acceptance criteria:**
  - ZERO issues found (critical, medium, or minor)
  - Spec re-read confirms 100% implementation
  - Fresh-eyes review finds no gaps
- **If Round 3 FAILS (ANY issues found):**
  - ❌ RESTART from smoke testing
  - Fix ALL issues
  - Re-run Stage 5ca + ALL 3 QC rounds
  - Round 3 is zero-tolerance checkpoint
- **If Round 3 PASSES (ZERO issues):**
  - ✅ QC Rounds complete
  - Proceed to Stage 5cc (Final Review)
- **Impact:** Round 3 is final chance to catch issues before feature completion

---

**Summary:** QC Rounds have ZERO TECH DEBT TOLERANCE
- Any restart = re-run smoke testing + all 3 QC rounds
- Partial implementations NOT accepted
- "90% done, will finish later" = INCOMPLETE = RESTART
- Feature must be 100% production-ready or RESTART

---

## Prerequisites Checklist

**Verify these BEFORE starting QC Rounds:**

**From Stage 5ca (Smoke Testing):**
- [ ] All 3 smoke test parts passed
- [ ] Part 3 verified OUTPUT DATA VALUES (not just "file exists")
- [ ] Feature executes end-to-end without crashes
- [ ] Output data is correct and reasonable

**Unit Tests:**
- [ ] Run `python tests/run_all_tests.py` → exit code 0
- [ ] All unit tests passing (100% pass rate)

**Documentation:**
- [ ] `code_changes.md` fully updated
- [ ] `implementation_checklist.md` all requirements verified
- [ ] Smoke test results documented in README Agent Status

**If ANY prerequisite not met:** Return to Stage 5ca and complete it first.

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   QC ROUNDS WORKFLOW                        │
└─────────────────────────────────────────────────────────────┘

QC Round 1: Basic Validation
   ├─ Unit tests pass (100%)
   ├─ Code matches spec structurally
   ├─ Tests use real objects (not excessive mocking)
   ├─ Output files validate CONTENT (not just existence)
   ├─ Interfaces verified against actual classes
   ↓
   Pass criteria: <3 critical issues, 100% requirements met
   If PASS → Round 2
   If FAIL → QC Restart Protocol

Re-Reading Checkpoint #1
   ↓ Re-read "Common Mistakes"

QC Round 2: Deep Verification
   ├─ Baseline comparison (if similar feature exists)
   ├─ Output validation (values in range, no zeros/nulls)
   ├─ No regressions (new feature doesn't break existing)
   ├─ Log quality (no unexpected WARNING/ERROR)
   ├─ Semantic diff check (intentional vs accidental changes)
   ├─ Edge cases handled
   ↓
   Pass criteria: ALL Round 1 issues resolved + zero new critical issues
   If PASS → Round 3
   If FAIL → QC Restart Protocol

Re-Reading Checkpoint #2
   ↓ Re-read Critical Rules

QC Round 3: Final Skeptical Review
   ├─ Re-read spec.md with fresh eyes
   ├─ Re-check Algorithm Traceability Matrix
   ├─ Re-run smoke test final time
   ├─ Final question: "Is feature ACTUALLY complete?"
   ↓
   Pass criteria: ZERO issues found
   If PASS → Proceed to Stage 5cc
   If FAIL (ANY issues) → QC Restart Protocol

QC Restart Protocol (if triggered)
   ↓ Fix ALL issues
   ↓ Re-run smoke testing (all 3 parts)
   ↓ Re-run QC Round 1, 2, 3 (fresh validation)
   ↓ Continue until all rounds pass
```

---

## QC Round 1: Basic Validation

**Purpose:** Verify fundamental correctness (tests, structure, interfaces)

**Pass Criteria:** <3 critical issues, 100% of requirements met

---

### Round 1 Checklist

Work through each section systematically. Check ALL boxes.

---

#### 1. Unit Tests Validation

- [ ] Run `python tests/run_all_tests.py` → exit code 0
- [ ] All new tests pass (100% pass rate)
- [ ] Tests use REAL objects (not excessive mocking)
  - ✅ Good: Mock file I/O, external APIs
  - ❌ Bad: Mock internal classes that should be tested
- [ ] Tests verify behavior (not just "method was called")

**Real-World Example - Excessive Mocking:**
```python
# ❌ BAD - Mocking everything, not testing real behavior
def test_calculate_score(mock_config, mock_player, mock_multiplier):
    mock_multiplier.return_value = 1.5
    mock_player.projected_points = 100
    result = calculate_score(mock_player, mock_config)
    assert result == 150  # This just tests your mock, not real code

# ✅ GOOD - Use real objects, mock only external dependencies
def test_calculate_score(real_config, real_player):
    # real_player is actual FantasyPlayer object
    # real_config is actual ConfigManager object
    result = calculate_score(real_player, real_config)
    assert result > real_player.projected_points  # Tests real calculation
```

---

#### 2. Code Structure Validation

- [ ] Code matches spec.md structure
- [ ] All spec requirements have corresponding code
- [ ] Algorithm Traceability Matrix still valid (from Stage 5a iteration 4)
  - Every algorithm in spec maps to exact code location
  - Code behavior matches spec behavior
- [ ] No placeholder implementations (e.g., `pass`, `return None`)

**Verification:**
```markdown
## Algorithm Traceability Matrix Verification

Algorithm from spec: "Calculate ADP multiplier based on rank"
Implementation location: PlayerManager._calculate_adp_multiplier() (line 234)
Behavior verified: ✅ Matches spec (multiplier = 1.0 + (500-rank)/500 * 0.5)
```

---

#### 3. Output File Validation

- [ ] All expected output files created
- [ ] **Output files contain CORRECT DATA** (not just structure)
  - ❌ "File has 1000 rows" - not sufficient
  - ✅ "File has 1000 rows, avg value 245.3, no zeros" - good
- [ ] **Per-category verification** (not just totals)
  - If feature processes multiple categories (positions, file types, etc.)
  - Verify EACH category has correct data
  - Example: "QB files: 18 updated, RB files: 18 updated, ..., DST files: 18 updated"
  - Don't just check "108 files updated" - verify per-category counts
- [ ] File formats match spec (CSV columns, JSON structure, etc.)
- [ ] No empty files where data expected

**Example:**
```python
# Verify output file quality
df = pd.read_csv("data/output.csv")

# Structure checks
assert len(df) == 1000, f"Expected 1000 rows, got {len(df)}"
assert 'player_name' in df.columns, "Missing player_name column"

# Data quality checks (not just structure)
assert df['projected_points'].mean() > 200, "Average points too low"
assert df['projected_points'].max() < 500, "Max points unreasonably high"
assert not df['player_name'].isnull().any(), "Some player names are null"
```

---

#### 4. Interface Verification

- [ ] All external interfaces verified against actual classes (not assumptions)
- [ ] Method signatures match actual source code
- [ ] Return types match actual implementations
- [ ] No broken imports or missing dependencies

**Verification:**
```markdown
## Interface Verification

Dependency: ConfigManager.get_adp_multiplier()

Assumed signature: get_adp_multiplier(adp: int) -> float
Actual signature (ConfigManager.py:234): get_adp_multiplier(adp: int) -> Tuple[float, int]

⚠️ MISMATCH FOUND - Code expects float, actual returns tuple
Fix: Updated code to handle tuple return (multiplier, rating)
```

---

#### 5. Runner Script Validation

- [ ] Entry point scripts tested with `--help`
- [ ] **Entry point scripts tested with E2E execution** (not just --help)
- [ ] Error messages are helpful (not stack traces for user errors)
- [ ] Script handles invalid inputs gracefully

---

#### 6. Documentation Validation

- [ ] code_changes.md accurately reflects all changes
- [ ] implementation_checklist.md all items verified
- [ ] No TODOs or FIXMEs in committed code
- [ ] Comments explain "why" not "what"

---

### Round 1 Execution

1. **Work through checklist systematically** (don't skip items)

2. **Document any issues found:**
   ```markdown
   ## QC Round 1 Issues

   ### Critical Issues
   1. Output file contains all zeros for projected_points column
      - Location: data/players_projected.csv
      - Expected: Real projection values (100-400 range)
      - Root cause: Mock data used instead of real API call
      - Impact: Feature doesn't work (primary use case fails)

   2. Interface mismatch - ConfigManager.get_adp_multiplier()
      - Expected return: float
      - Actual return: Tuple[float, int]
      - Impact: Code crashes when calling this method

   ### Minor Issues
   1. Missing docstring on calculate_adp_multiplier()
      - Location: league_helper/util/PlayerRatingManager.py:45
      - Impact: Low (documentation quality)
   ```

3. **Evaluate pass criteria:**
   - Critical issues: {count}
   - Requirements met: {percentage}%
   - **Pass if:** <3 critical issues AND 100% requirements met
   - **Fail if:** ≥3 critical issues OR <100% requirements met

4. **Decision:**
   - **If PASS:** Document results, proceed to Round 2
   - **If FAIL:** Follow QC Restart Protocol (see below)

**Example - Round 1 Results:**
```markdown
## QC Round 1 Results

**Issues Found:**
- Critical issues: 2
- Minor issues: 1

**Requirements Met:** 92% (23/25 requirements verified)

**Pass Criteria Evaluation:**
- Critical issues: 2 (<3) ✅
- Requirements met: 92% (>80%) ✅

**DECISION: PASS**

**Next Action:** Proceed to QC Round 2 (Deep Verification)

**Issues to address in Round 2:**
- Verify critical issues are actually fixed (not just "looks fixed")
- Verify no new issues introduced by fixes
```

---

## 🔄 Re-Reading Checkpoint #1

**STOP - Before proceeding to Round 2:**

1. **Re-read "Common Mistakes to Avoid" section below**
2. **Verify you didn't fall into any anti-patterns**
3. **Confirm Round 1 actually passed** (not just "close enough")
4. **Update README Agent Status:**
   ```markdown
   Guide Last Re-Read: {timestamp}
   Checkpoint: QC Round 1 complete, starting QC Round 2
   Round 1 Result: PASS (2 critical issues, 1 minor issue, 92% requirements met)
   ```

---

## QC Round 2: Deep Verification

**Purpose:** Deep dive into data quality, integration, and edge cases

**Pass Criteria:** ALL issues from Round 1 resolved + zero new critical issues

---

### Round 2 Checklist

Work through each section systematically. Check ALL boxes.

---

#### 1. Baseline Comparison (if similar feature exists)

- [ ] Identify similar feature in codebase (if any)
- [ ] Compare file structure (new feature follows same patterns?)
- [ ] Compare data format (consistent with existing features?)
- [ ] Compare integration patterns (uses same interfaces?)
- [ ] Document INTENTIONAL differences (and why they're needed)
- [ ] Verify new feature matches codebase conventions

**Example:**
```markdown
## Baseline Comparison: ADP Integration vs Player Rating Integration

Similar feature: Player Rating Integration (feature_03)

File structure: ✅ CONSISTENT
- Both use {feature}_Manager.py pattern
- Both store data in data/player_data/

Data format: ✅ CONSISTENT
- Both use CSV with standard columns
- Both use float for multiplier values

Integration: ⚠️ DIFFERENT (intentional)
- Player Rating uses ConfigManager.get_rating_multiplier()
- ADP uses NEW method ConfigManager.get_adp_multiplier()
- Reason: ADP requires different curve (exponential vs linear)
- Documented in: code_changes.md section 3

Conclusion: Differences are intentional and justified
```

---

#### 2. Statistical Output Validation (Values, not just structure)

**Purpose:** Comprehensive statistical validation to catch data loading bugs, calculation errors, and unrealistic values.

**CRITICAL:** This validation prevented Feature 02 catastrophic bug (99.8% zeros in output). Statistical checks catch bugs that basic structure checks miss.

**Relationship to Part 3b (Smoke Testing):**
- Part 3b (STAGE_5ca) performed initial statistical validation during smoke testing
- This Round 2 validation RE-PERFORMS the same checks to verify fixes haven't introduced regressions
- Between Part 3b and Round 2, you may have fixed Round 1 issues - those fixes could introduce new bugs
- ALWAYS re-run statistical validation in Round 2 even if Part 3b passed
- Think of Part 3b as "first check" and Round 2 as "verify fixes didn't break anything"

---

**Manual Validation Checklist:**

- [ ] Open actual output files (CSV, JSON, etc.)
- [ ] Verify data values are in expected range
  - Example: Projected points between 0-500 (not -999 or 10000000)
- [ ] Verify no zeros where real data expected
- [ ] Verify no nulls where values required
- [ ] Verify no placeholder text ("TODO", "N/A", "test")
- [ ] Verify calculations are correct (spot-check a few rows manually)

---

**Statistical Validation (MANDATORY for numeric columns):**

For EACH numeric column in output data, perform these 5 statistical checks:

**1. Zero Percentage Check**
```python
zero_count = (df[col] == 0.0).sum()
zero_pct = (zero_count / total_count) * 100
print(f"Zero percentage: {zero_pct:.1f}% ({zero_count}/{total_count})")

# Automatic fail condition
assert zero_pct < 90.0, f"🔴 CRITICAL: {zero_pct:.1f}% zeros (>90% threshold)"
```

**Why:** >90% zeros indicates data loading bug (Feature 02 pattern)

---

**2. Variance Check**
```python
if non_zero_count > 1:
    std_dev = statistics.stdev(values)
    mean = statistics.mean(values)
    print(f"Mean: {mean:.2f}, Std Dev: {std_dev:.2f}")

    # Automatic fail condition
    assert std_dev > 0, f"🔴 CRITICAL: Zero variance (all values are {mean})"
```

**Why:** Standard deviation = 0 means all values are identical (calculation bug)

---

**3. Realistic Range Check**
```python
actual_min = df[col].min()
actual_max = df[col].max()
print(f"Range: [{actual_min:.2f}, {actual_max:.2f}]")
print(f"Expected range: [{domain_min}, {domain_max}]")

# Automatic fail condition
assert domain_min <= actual_min <= domain_max * 10, "🔴 CRITICAL: Min outside realistic range"
assert domain_min <= actual_max <= domain_max * 10, "🔴 CRITICAL: Max outside realistic range"
```

**Domain-specific ranges:**
- `actual_points`: 0-50 (NFL: typical game points)
- `projected_points`: 0-400 (NFL season: typical season points)
- `adp_multiplier`: 0.5-2.0 (typical multiplier range)
- `win_rate`: 0.0-1.0 (probability range)

---

**4. Non-Zero Count Check**
```python
non_zero_count = (df[col] > 0).sum()
non_zero_pct = (non_zero_count / total_count) * 100
print(f"Non-zero count: {non_zero_count}/{total_count} ({non_zero_pct:.1f}%)")

# Automatic fail conditions
assert non_zero_count > 0, f"🔴 CRITICAL: 0 have non-zero values (100% zeros)"
assert non_zero_pct > 10.0, f"🔴 CRITICAL: Only {non_zero_pct:.1f}% non-zero (<10% threshold)"
```

**Why:** <10% non-zero indicates suspiciously low data (loading issue)

---

**5. Distribution Sanity Check**
```python
if non_zero_count >= 4:
    q1 = df[col].quantile(0.25)
    median = df[col].quantile(0.50)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    print(f"Distribution: Q1={q1:.2f}, Median={median:.2f}, Q3={q3:.2f}, IQR={iqr:.2f}")

    # Automatic fail condition
    assert iqr > 0, f"🔴 CRITICAL: Zero IQR (no spread in data)"
```

**Why:** Zero IQR means quartiles are identical (unrealistic for real data)

---

**Complete Validation Function:**

```python
def validate_statistical_output(df, col_name, domain_min, domain_max):
    """
    Comprehensive statistical validation for output data column.

    Catches:
    - Data loading bugs (>90% zeros)
    - Calculation bugs (zero variance)
    - Unrealistic values (outside domain range)
    - Suspiciously low data (<10% non-zero)

    Args:
        df: DataFrame with output data
        col_name: Column to validate
        domain_min: Minimum realistic value for this domain
        domain_max: Maximum realistic value for this domain

    Returns:
        dict with validation results {'status': 'PASSED'|'FAILED', ...}
    """
    import statistics

    print(f"\n=== Statistical Output Validation: {col_name} ===")

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

    if actual_min < domain_min * 0.1 or actual_max > domain_max * 10:
        failures.append(f"🔴 CRITICAL: Values outside realistic range by 10x")

    if non_zero_pct < 10.0 and zero_count > 0:
        failures.append(f"🔴 CRITICAL: Only {non_zero_pct:.1f}% non-zero values (<10% threshold)")

    # Report results
    if failures:
        print("\n❌ VALIDATION FAILED:")
        for failure in failures:
            print(f"  {failure}")
        return {'status': 'FAILED', 'failures': failures}
    else:
        print("\n✅ VALIDATION PASSED")
        return {'status': 'PASSED'}


# Usage in QC Round 2:
import pandas as pd

df = pd.read_csv("output.csv")

# Validate each numeric column with domain-appropriate ranges
results = []
results.append(validate_statistical_output(df, 'actual_points', domain_min=0, domain_max=50))
results.append(validate_statistical_output(df, 'projected_points', domain_min=0, domain_max=400))
results.append(validate_statistical_output(df, 'adp_multiplier', domain_min=0.5, domain_max=2.0))
results.append(validate_statistical_output(df, 'win_rate', domain_min=0.0, domain_max=1.0))

# Check if any validations failed
failed = [r for r in results if r.get('status') == 'FAILED']
if failed:
    print(f"\n🔴 QC Round 2 FAILED: {len(failed)} columns failed statistical validation")
    print("Trigger QC Restart Protocol")
else:
    print(f"\n✅ All {len(results)} columns passed statistical validation")
```

---

**Critical Question Checklist:**

Before marking Round 2 complete, answer these questions:

**Data Reality Checks:**
- [ ] If I saw these values in production, would I be suspicious?
- [ ] Are zero percentages realistic for this domain?
- [ ] Is the variance what I'd expect for real data?
- [ ] Are the min/max values possible in the real world?
- [ ] Do quartiles show reasonable spread?

**Feature 02 Prevention:**
- [ ] Did I see "(0 have non-zero values)" anywhere?
  - If YES → AUTOMATIC FAIL (Feature 02 bug pattern)
- [ ] Is >90% of data zeros?
  - If YES → AUTOMATIC FAIL (data loading issue)
- [ ] Is standard deviation = 0?
  - If YES → AUTOMATIC FAIL (all same value)
- [ ] Is <10% of data non-zero?
  - If YES → AUTOMATIC FAIL (suspiciously low)

**Domain Knowledge:**
- [ ] Do these values make sense for this feature's domain?
- [ ] Would a domain expert agree these values look right?
- [ ] Are relationships between columns sensible?
  - Example: projected_points should correlate with adp_rank

**Calculation Verification:**
- [ ] Did I spot-check calculations manually (not just automated checks)?
- [ ] Do calculated values match expected formulas from spec?
- [ ] Are edge case calculations correct (min/max values)?

---

**Automatic Fail Conditions (QC Restart Protocol):**

If you see ANY of these, IMMEDIATELY trigger QC Restart Protocol:

❌ **"(0 have non-zero values)"** - CRITICAL BUG (Feature 02 exact pattern)
❌ **>90% zeros** - Data loading issue
❌ **Standard deviation = 0** - All values identical (calculation bug)
❌ **<10% non-zero values** - Suspiciously low data
❌ **Min/max outside realistic range by 10x** - Absurd values
❌ **Zero IQR** - No spread in data (unrealistic)
❌ **Answer "I would be suspicious" to production question** - Trust your instincts

---

**Feature 02 Example - How Statistical Validation Would Have Caught The Bug:**

**What actually happened (WITHOUT statistical validation):**

```markdown
QC Round 2 - Basic Data Quality Check:
✅ Row count: 2500 (expected)
✅ Column 'actual_points': Exists
✅ No nulls in actual_points
✅ Sum of actual_points: 0.1 (> 0, so "has data")

Marked PASSED, proceeded to Round 3
Bug survived to user final review
```

**What would have happened (WITH statistical validation):**

```markdown
QC Round 2 - Statistical Output Validation:

Column: actual_points
Zero percentage: 99.8% (2499/2500) 🔴 CRITICAL: >90% threshold
Non-zero count: 1/2500 (0.04%) 🔴 CRITICAL: <10% threshold
Mean: 0.00004, Std Dev: 0.002
Range: [0.0, 0.1]

❌ VALIDATION FAILED:
  🔴 CRITICAL: 99.8% zeros (>90% threshold)
  🔴 CRITICAL: Only 0.04% non-zero values (<10% threshold)

QC Round 2 FAILED - Trigger QC Restart Protocol

Root cause investigation:
- Loading week_N folder for actuals (should load week_N+1)
- Week N games not complete yet → all actual_points[N] = 0.0
- Only 1 player has 0.1 points (test data artifact)

Fix applied:
- Changed to load week_N+1 folder for actuals
- Re-tested statistical validation

Post-fix validation:
Zero percentage: 0.1% (2/2500) ✅
Non-zero count: 2498/2500 (99.9%) ✅
Mean: 15.3, Std Dev: 8.2 ✅
Range: [0.0, 48.7] ✅

✅ VALIDATION PASSED
```

**Result:** Bug caught in QC Round 2 instead of user final review (3 stages earlier)

---

**Real-World Example:**
```markdown
## Round 2 - Statistical Output Validation

File: data/player_data/qb_data_with_adp.csv

=== Statistical Output Validation: projected_points ===
✓ Zero percentage: 0.0% (0/128)
✓ Non-zero count: 128/128 (100.0%)
✓ Mean: 245.30, Std Dev: 68.42
✓ Range: [150.2, 385.7]
  Expected range: [0, 400]
✓ Distribution: Q1=189.5, Median=238.2, Q3=295.8, IQR=106.3

✅ VALIDATION PASSED

=== Statistical Output Validation: adp_multiplier ===
✓ Zero percentage: 0.0% (0/128)
✓ Non-zero count: 128/128 (100.0%)
✓ Mean: 1.12, Std Dev: 0.18
✓ Range: [0.87, 1.48]
  Expected range: [0.5, 2.0]
✓ Distribution: Q1=0.98, Median=1.10, Q3=1.25, IQR=0.27

✅ VALIDATION PASSED

=== Statistical Output Validation: adp_rank ===
✓ Zero percentage: 9.4% (12/128)
⚠️  Non-zero count: 116/128 (90.6%)
✓ Mean: 98.5, Std Dev: 72.3
✓ Range: [1.0, 287.0]
  Expected range: [1, 500]
✓ Distribution: Q1=45.0, Median=89.5, Q3=142.0, IQR=97.0

⚠️  WARNING: 9.4% zeros (players not in ADP data)
Investigation: ADP data only covers top 300 players
Spec review: Spec says "use default multiplier for unranked players"
Conclusion: ✅ Working as intended (zeros represent unranked players)

✅ VALIDATION PASSED (with justified zeros)

---

All 3 columns passed statistical validation
Ready to continue Round 2 checklist
```

---

#### 3. Regression Testing

- [ ] Run ALL unit tests (not just new ones)
- [ ] Verify existing features still work
- [ ] Check that new feature didn't break existing functionality
- [ ] Review changed files (git diff) for unintended modifications

**Verification:**
```bash
# Run full test suite
python tests/run_all_tests.py

# Result: 2,247 tests passed, 0 failed ✅

# Verify no regression in existing modes
python run_league_helper.py --mode draft --dry-run  # ✅ Works
python run_league_helper.py --mode starter --dry-run  # ✅ Works
python run_league_helper.py --mode trade --dry-run  # ✅ Works
```

---

#### 4. Log Quality Verification

- [ ] Run feature and capture logs
- [ ] **No unexpected WARNING messages** (review each one)
- [ ] **No ERROR messages** (unless testing error paths)
- [ ] Log messages are helpful for debugging (not cryptic)
- [ ] No excessive logging (log spam)
- [ ] No sensitive data logged (passwords, API keys, PII)

**Example - Log Quality Issues:**
```markdown
## Log Quality Check

Total log messages: 1,247
- DEBUG: 1,189
- INFO: 52
- WARNING: 6
- ERROR: 0

WARNING messages review:
1. "Player 'J.Smith' missing ADP data, using default multiplier 1.0" (×5)
   - Status: Expected (not all players in ADP data)
   - Action: No change needed

2. "ADP data file timestamp is 7 days old"
   - Status: Expected (data refreshed weekly)
   - Action: No change needed

Conclusion: ✅ No unexpected WARNINGs, log quality is good
```

---

#### 5. Semantic Diff Check

- [ ] Review `git diff` for all changed files
- [ ] Categorize changes:
  - **Intentional:** Expected from feature implementation
  - **Accidental:** Formatting, whitespace, unrelated code
- [ ] Flag accidental changes for cleanup

**Example:**
```bash
# Review non-whitespace changes
git diff --ignore-all-space

# Find accidental formatting changes
git diff --word-diff
```

```markdown
## Semantic Diff Analysis

Files changed: 8

Intentional changes (feature-related):
- league_helper/util/PlayerManager.py: Added load_adp_data() method ✅
- league_helper/util/FantasyPlayer.py: Added adp_multiplier field ✅
- league_helper/util/ConfigManager.py: Added get_adp_multiplier() ✅

Accidental changes (not feature-related):
- league_helper/util/ConfigManager.py: Lines 45-67 re-indented
  - Not related to feature
  - Action: Revert whitespace changes
- utils/csv_utils.py: Added blank line at EOF
  - Not related to feature
  - Action: Revert formatting change
```

---

#### 6. Edge Case Validation

- [ ] Review spec.md "Edge Cases" section
- [ ] Verify each edge case handled in code
- [ ] Test edge cases manually (if not covered by unit tests):
  - Empty inputs
  - Maximum/minimum values
  - Null/undefined values
  - Concurrent access (if applicable)

---

#### 7. Error Handling Verification

- [ ] Try to trigger error conditions (invalid input, missing files, etc.)
- [ ] Verify error messages are helpful
- [ ] Verify errors don't crash the application
- [ ] Verify errors are logged appropriately
- [ ] Verify error recovery works (if applicable)

**Example:**
```markdown
## Error Handling Verification

Test 1: Missing ADP data file
- Command: rm data/adp_rankings.csv && python run_league_helper.py --mode draft
- Expected: Error logged, feature continues with default multipliers
- Actual: ✅ "ADP file not found, using default multipliers" logged, no crash

Test 2: Malformed ADP CSV
- Setup: Corrupted CSV (missing column headers)
- Expected: Error logged, feature continues with default multipliers
- Actual: ✅ "Invalid ADP file format" logged, no crash

Test 3: Invalid ADP value in CSV
- Setup: ADP rank = -5 (invalid)
- Expected: Warning logged, player gets default multiplier
- Actual: ✅ "Invalid ADP rank -5 for player X, using default" logged

Conclusion: ✅ All error scenarios handled gracefully
```

---

### Round 2 Execution

1. **Work through checklist systematically**

2. **Document findings:**
   ```markdown
   ## QC Round 2 Deep Verification

   ### Round 1 Issues Resolution
   ✅ Issue #1 (zeros in output): RESOLVED - Real API data now used
   ✅ Issue #2 (interface mismatch): RESOLVED - Code updated to handle tuple

   ### New Findings
   1. Data Quality: 12 players have invalid rank 0
      - Root cause: Not all players in ADP data source
      - Severity: Minor (affects 9% of players)
      - Fix: Changed default from 0 to NaN
      - Status: FIXED and re-verified

   2. Log Quality: No issues found ✅

   3. Semantic Diff: 2 accidental whitespace changes
      - Files: ConfigManager.py, csv_utils.py
      - Impact: None (cosmetic only)
      - Action: Reverted whitespace changes

   4. Baseline Comparison: Consistent with existing patterns ✅
   ```

3. **Evaluate pass criteria:**
   - Round 1 issues resolved: {yes/no}
   - New critical issues: {count}
   - **Pass if:** ALL Round 1 issues resolved AND zero new critical issues
   - **Fail if:** Any Round 1 issues unresolved OR new critical issues found

4. **Decision:**
   - **If PASS:** Proceed to Round 3
   - **If FAIL:** Follow QC Restart Protocol

**Example - Round 2 Results:**
```markdown
## QC Round 2 Results

**Round 1 Issues:**
- Issue #1 (zeros in output): ✅ RESOLVED
- Issue #2 (interface mismatch): ✅ RESOLVED

**New Findings:**
- Critical issues: 0
- Minor issues: 2 (invalid ranks, whitespace changes)
- Both minor issues: FIXED

**Pass Criteria Evaluation:**
- All Round 1 issues resolved: ✅
- New critical issues: 0 ✅

**DECISION: PASS**

**Next Action:** Proceed to QC Round 3 (Final Skeptical Review)
```

---

## 🔄 Re-Reading Checkpoint #2

**STOP - Before proceeding to Round 3:**

1. **Re-read "Critical Rules" section at top of this guide**
2. **Verify Round 1 AND Round 2 both passed**
3. **Confirm you actually verified data VALUES** (not just structure)
4. **Update README Agent Status:**
   ```markdown
   Guide Last Re-Read: {timestamp}
   Checkpoint: QC Round 2 complete, starting QC Round 3
   Round 2 Result: PASS (all Round 1 issues resolved, 0 new critical issues)
   ```

---

## QC Round 3: Final Skeptical Review

**Purpose:** Fresh-eyes review to catch anything missed in previous rounds

**Pass Criteria:** ZERO issues found (if issues found → QC Restart Protocol)

**Mindset:** Approach this as if you're reviewing someone else's code for the first time. Be skeptical.

---

### Round 3 Checklist

Work through each section with fresh perspective. Be ruthlessly skeptical.

---

#### 1. Re-read Spec with Fresh Eyes

- [ ] Open spec.md
- [ ] Read each requirement as if seeing it for first time
- [ ] For each requirement, verify implementation actually achieves it:
  - Not just "code exists for this"
  - But "code correctly implements this"
- [ ] **Verify EACH item in lists** (e.g., if spec says "all 6 positions", verify ALL 6)
  - Don't assume "code processes list" means "code processes ALL items in list"
  - Example: Spec says "update 6 positions (QB, RB, WR, TE, K, DST)"
  - Verify: QB ✓, RB ✓, WR ✓, TE ✓, K ✓, DST ✓ (not just "positions updated")
- [ ] Check for subtle misinterpretations

**Real-World Example:**
```markdown
## Spec Re-Reading Results

Spec requirement: "Add ADP multiplier to draft recommendations"

Round 1/2 verified:
✅ ADP multiplier calculation exists
✅ ADP multiplier stored in player object
✅ ADP multiplier displayed in output

Round 3 catches:
❌ ADP multiplier calculated but NOT applied to final score

Issue: Code calculates multiplier but forgets to multiply final_score by it
Location: FantasyPlayer.calculate_total_score() line 245
Fix: Added `final_score *= self.adp_multiplier`

This would have been caught by re-reading spec with fresh eyes.
```

---

#### 2. Re-check Algorithm Traceability Matrix

- [ ] Open Algorithm Traceability Matrix (from Stage 5a iteration 4)
- [ ] For each algorithm:
  - Find the code location listed in matrix
  - Read the actual code
  - Verify code behavior matches spec algorithm
- [ ] Check for algorithm drift (implementation slightly different from spec)

**Verification:**
```markdown
## Algorithm Traceability Re-Check

Matrix Entry #3:
Algorithm: "Calculate ADP multiplier using exponential curve"
Spec formula: multiplier = 1.0 + (500 - rank) / 500 * 0.5
Code location: PlayerManager._calculate_adp_multiplier() line 234

Code inspection:
```python
def _calculate_adp_multiplier(self, adp_rank):
    if adp_rank is None or adp_rank <= 0:
        return 1.0
    return 1.0 + (500 - adp_rank) / 500 * 0.5
```

Verification: ✅ Code matches spec exactly
```

---

#### 3. Re-check Integration Points

- [ ] Review Integration Gap Check (from Stage 5a iterations 7, 14, 23)
- [ ] Verify every new method has a caller
- [ ] Verify no orphan code (written but never used)
- [ ] Trace data flow end-to-end:
  - Input → Processing → Output
  - Verify each step actually happens

**Verification:**
```markdown
## Integration Points Re-Check

New method: PlayerManager.load_adp_data()
Caller: PlayerManager.load_players() line 180 ✅
Verified: Method is actually called ✅

Data flow trace:
1. load_adp_data() reads CSV ✅
2. _match_player_to_adp() assigns ranks ✅
3. _calculate_adp_multiplier() computes multiplier ✅
4. calculate_total_score() applies multiplier ✅ (FIXED in this round!)

No orphan code found ✅
```

---

#### 4. Re-run Smoke Test (Final Time)

- [ ] Re-run all 3 smoke test parts (Import, Entry Point, E2E)
- [ ] Even if they passed before, run again (fixes can introduce regressions)
- [ ] Verify output data VALUES still correct
- [ ] Compare output to expected output from spec test plan section

**Why re-run:** Fixes in Rounds 1 & 2 might have introduced new bugs

---

#### 5. Review Question Answers

- [ ] Open questions.md (if it exists)
- [ ] Re-read user's answers to your questions
- [ ] Verify implementation actually follows user's answers
- [ ] Check for misinterpretations of user's intent

---

#### 6. Final Skeptical Questions

Ask yourself these questions honestly:

- [ ] **"Does this feature actually work?"**
  - Not "tests pass" but "does it DO what user wants?"

- [ ] **"Would I ship this to production?"**
  - If hesitation: What's making you hesitant?

- [ ] **"Is the feature COMPLETE or just FUNCTIONAL?"**
  - FUNCTIONAL: It works in happy path
  - COMPLETE: It works in all cases, handles errors, has good UX

- [ ] **"What happens if..."**
  - ...file doesn't exist?
  - ...user provides invalid input?
  - ...data is missing/corrupted?
  - ...multiple features interact?

- [ ] **"Did I verify data VALUES or just structure?"**
  - Be honest: Did you actually open output files and check data?

- [ ] **"Is this actually better than before?"**
  - Does feature improve the system?
  - Or does it add complexity without clear benefit?

---

#### 7. Compare to Test Plan

- [ ] Open spec.md "Test Plan" or "Validation" section
- [ ] For each test scenario listed:
  - Run that scenario manually
  - Verify actual output matches expected output from spec
- [ ] If spec doesn't have test plan: Create one now (and update spec)

---

### Round 3 Execution

1. **Work through checklist with skeptical mindset**

2. **Document findings:**
   ```markdown
   ## QC Round 3 Final Review

   ### Issues Found
   1. ADP multiplier calculated but not applied to final score
      - Severity: CRITICAL (feature doesn't work)
      - Location: FantasyPlayer.calculate_total_score()
      - Fix: Added multiplication step
      - This triggers QC Restart Protocol

   {If ZERO issues: State "Zero issues found - feature is complete"}

   ### Skeptical Review Results
   - Feature actually works: {yes/no after fix}
   - Would ship to production: {yes/no}
   - Feature is COMPLETE (not just functional): {yes/no}
   - Data values verified (not just structure): yes
   - Better than before: yes

   ### Final Verification
   - Smoke tests re-run: {pass/fail}
   - Algorithm Traceability Matrix: verified
   - Integration points: verified
   - Test plan scenarios: all passed
   ```

3. **Evaluate pass criteria:**
   - Issues found: {count}
   - **Pass if:** ZERO issues found
   - **Fail if:** ANY issues found

4. **Decision:**
   - **If PASS (zero issues):** Proceed to Stage 5cc
   - **If FAIL (any issues):** Follow QC Restart Protocol

---

## 🚨 QC RESTART PROTOCOL

**This protocol is CRITICAL. If ANY issues found in QC rounds, you MUST follow this protocol.**

---

### When to Trigger QC Restart

**Trigger immediately if:**
- QC Round 1 finds ≥3 critical issues OR <100% requirements met
- QC Round 2 finds any Round 1 issues unresolved OR new critical issues
- QC Round 3 finds ANY issues (zero tolerance in Round 3)

**Do NOT trigger for:**
- Minor documentation issues (missing docstrings)
- Style issues (formatting, naming)
- Non-critical refactoring opportunities

**When in doubt:** If the issue affects CORRECTNESS or COMPLETENESS → Restart

---

### QC Restart Steps

**1. STOP all work immediately**
- Do not proceed to next QC round
- Do not "just fix this one thing"
- Do not rationalize "it's not that bad"

**2. Document the issues requiring restart:**
```markdown
## QC Restart Triggered

Trigger point: QC Round 3
Date: {YYYY-MM-DD}

Critical issues found:
1. ADP multiplier calculated but not applied to final score
   - Impact: Feature doesn't actually work (primary use case fails)
   - Root cause: Forgot to add multiplication step in calculate_total_score()
   - Location: FantasyPlayer.calculate_total_score() line 245

Restart required because: Round 3 found critical issue (zero tolerance)
```

**3. Fix ALL issues:**
- Don't just fix the ones you found
- Look for related issues (if one bug exists, are there others?)
- Fix root causes (not just symptoms)
- Update tests to catch these issues

**4. COMPLETELY RESTART Post-Implementation:**

**YOU MUST RE-RUN EVERYTHING:**

- [ ] **Re-run Smoke Testing** (Stage 5ca)
  - Part 1: Import Test
  - Part 2: Entry Point Test
  - Part 3: E2E Execution Test (verify DATA VALUES)

- [ ] **Re-run QC Round 1**
  - Don't assume it still passes
  - Fixes can introduce new issues
  - Fresh validation required

- [ ] **Re-run QC Round 2**
  - All checks from scratch
  - Baseline comparison again
  - Log quality verification again

- [ ] **Re-run QC Round 3**
  - Fresh-eyes skeptical review
  - Re-check Algorithm Traceability Matrix
  - Re-run final smoke test

**5. Document restart results:**
```markdown
## QC Restart Results

Issues fixed:
✅ Issue #1: Added `final_score *= self.adp_multiplier` at line 245

Post-restart validation:
✅ Smoke testing: ALL 3 PARTS PASSED
✅ QC Round 1: PASSED (<3 critical, 100% requirements)
✅ QC Round 2: PASSED (all resolved, no new issues)
✅ QC Round 3: PASSED (ZERO issues found)

Ready to proceed to Stage 5cc (Final Review).
```

---

### Why Complete Restart is Required

**Real-World Example:**

```
Initial QC Round 1: Found critical issue with output data (all zeros)
Developer fixed: Updated data calculation logic
Developer thought: "I'll just continue to QC Round 2"

PROBLEM: The fix introduced new bug (now some data is negative, which is impossible)

If developer had re-run Smoke Test Part 3 after fix:
→ Would have caught negative values immediately
→ Would have fixed before proceeding

Instead, negative values discovered in QC Round 3:
→ Had to restart entire Post-Implementation
→ Total time wasted: 4 hours
→ If had restarted properly after first fix: 30 minutes
```

**The rule:** Fixes can introduce new bugs. ALWAYS re-validate everything after fixes.

---

## Completion Criteria

**Stage 5cb is complete when ALL of the following are true:**

- [x] QC Round 1 passed (<3 critical issues, 100% requirements met)
- [x] QC Round 2 passed (all Round 1 issues resolved, zero new critical issues)
- [x] QC Round 3 passed (ZERO issues found in skeptical review)
- [x] All re-reading checkpoints completed
- [x] README Agent Status updated after each round
- [x] If QC restart was triggered, fully completed (smoke + all 3 rounds)

**If ALL criteria met:** Proceed to Stage 5cc (Final Review)

**If ANY criteria not met:** Do NOT proceed until all are met

---

## Common Mistakes to Avoid

### Anti-Pattern 1: Skipping QC Rounds

**❌ Mistake:**
"QC Round 1 passed, Round 2 looks similar, I'll skip to Round 3"

**Why wrong:** Each round has DIFFERENT focus:
- Round 1: Basic validation (structure, tests)
- Round 2: Deep verification (data quality, logs, baseline)
- Round 3: Fresh-eyes skeptical review

**Round 2 catches issues Round 1 misses** (data quality, log spam, semantic diff)

**✅ Correct:** Complete ALL 3 rounds, every time, no exceptions

---

### Anti-Pattern 2: "Fix and Continue" (Not Restarting)

**❌ Mistake:**
```
QC Round 1 finds critical issue
Developer fixes issue
Developer continues to QC Round 2 (doesn't restart)
```

**Why wrong:** Fix might introduce new bugs. Must re-validate everything.

**✅ Correct:** Follow QC Restart Protocol (re-run smoke testing, Round 1, 2, 3)

---

### Anti-Pattern 3: Superficial QC Round 3

**❌ Mistake:**
"Already did Round 1 and 2, Round 3 is just a formality, I'll skim it"

**Why wrong:** Round 3 catches subtle issues that previous rounds missed

**Real example:** Round 3 re-reading spec caught "ADP multiplier calculated but not applied"

**✅ Correct:** Round 3 = Fresh eyes, skeptical mindset, actually re-read everything

---

### Anti-Pattern 4: Batch Fixes Without Re-Validation

**❌ Mistake:**
```
QC finds 5 issues
Fix all 5 issues in one batch
Continue to next round (don't re-test)
```

**Why wrong:** Fixes can conflict with each other, introduce new bugs

**✅ Correct:** Follow QC Restart Protocol (re-validate after fixes)

---

## Prerequisites for Next Stage

**Before transitioning to Stage 5cc (Final Review), verify:**

**QC Rounds Complete:**
- [ ] QC Round 1: PASSED
- [ ] QC Round 2: PASSED
- [ ] QC Round 3: PASSED (zero issues)

**Documentation:**
- [ ] All issues documented (even if resolved)
- [ ] README Agent Status updated after each round
- [ ] If restart occurred, restart results documented

**Verification:**
- [ ] Feature is COMPLETE (not just functional)
- [ ] Would ship to production with confidence
- [ ] Data values verified (not just structure)
- [ ] All spec requirements met (100%)

**If ALL verified:** Ready for Stage 5cc (Final Review)

**If ANY unverified:** Complete Stage 5cb first

---

## Next Stage

**After completing QC Rounds:**

📖 **READ:** `STAGE_5cc_final_review_guide.md`
🎯 **GOAL:** Production readiness through PR review, lessons learned, final verification
⏱️ **ESTIMATE:** 45-60 minutes

**Stage 5cc will:**
- PR Review Checklist (11 categories)
- Lessons Learned Capture (update guides immediately)
- Final Verification
- Completion check before Stage 5d

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting Stage 5cc.

---

*End of STAGE_5cb_qc_rounds_guide.md*
