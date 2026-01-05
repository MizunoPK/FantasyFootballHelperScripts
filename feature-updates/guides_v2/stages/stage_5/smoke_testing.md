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

1. **Read the smoke testing pattern:** `reference/smoke_testing_pattern.md`
   - Understand universal smoke testing workflow (3 parts)
   - Review critical rules that apply to ALL smoke testing
   - Study common mistakes to avoid

2. **Use the phase transition prompt** from `prompts/stage_5_prompts.md`
   - Find "Starting Stage 5c (Phase 1): Smoke Testing" prompt
   - Speak it out loud (acknowledge requirements)
   - List critical requirements from this guide

3. **Update README Agent Status** with:
   - Current Phase: POST_IMPLEMENTATION_SMOKE_TESTING
   - Current Guide: stages/stage_5/smoke_testing.md
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "3 parts MANDATORY", "Part 3 verify DATA VALUES", "Re-run ALL 3 if ANY fails"
   - Next Action: Smoke Test Part 1 - Import test

4. **Verify all prerequisites** (see checklist below)

5. **THEN AND ONLY THEN** begin smoke testing

**This is NOT optional.** Reading both the pattern and this guide ensures you don't skip critical validation steps.

---

## Quick Start

**What is this stage?**
Feature-level smoke testing validates that your individual feature works end-to-end with REAL data. This is testing in ISOLATION (not with other features). See `reference/smoke_testing_pattern.md` for universal workflow.

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

## 🛑 Critical Rules (Feature-Specific)

**📖 See `reference/smoke_testing_pattern.md` for universal critical rules.**

**Feature-specific rules for Stage 5ca:**

```
┌─────────────────────────────────────────────────────────────┐
│ FEATURE-SPECIFIC RULES - Add to README Agent Status         │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ Test feature IN ISOLATION
   - Do NOT test with other features
   - Use feature's own input/output
   - Epic-level integration tested in Stage 6

2. ⚠️ If smoke testing fails → Fix issues, restart from Part 1
   - After fixing → Re-run ALL 3 parts
   - Do NOT proceed to QC Rounds (Stage 5cb) until all parts pass

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

**From Stage 5b (Implementation):**
- [ ] All TODO tasks marked done in `todo.md`
- [ ] All unit tests passing (100% pass rate)
- [ ] `code_changes.md` fully updated with all changes
- [ ] `implementation_checklist.md` all requirements verified
- [ ] All code committed to git (clean working directory)

**Files that must exist:**
- [ ] `feature_XX_{name}/spec.md` (primary specification)
- [ ] `feature_XX_{name}/checklist.md` (planning decisions)
- [ ] `feature_XX_{name}/todo.md` (implementation tasks)
- [ ] `feature_XX_{name}/code_changes.md` (change documentation)
- [ ] `feature_XX_{name}/implementation_checklist.md` (requirement verification)

**Verification:**
- [ ] Run `python tests/run_all_tests.py` → exit code 0
- [ ] Check `git status` → no uncommitted implementation changes
- [ ] Review implementation_checklist.md → all items marked verified

**If ANY prerequisite not met:** Return to Stage 5b and complete it first.

---

## Workflow Overview

**📖 See `reference/smoke_testing_pattern.md` for universal workflow details.**

**Feature-specific workflow for Stage 5ca:**

```
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
   If PASS → Document, proceed to Stage 5cb
   If FAIL → Fix, RE-RUN ALL 3 PARTS
```

---

## Part 1: Import Test (Feature-Specific)

**📖 See `reference/smoke_testing_pattern.md` for universal import test pattern.**

**Feature-specific implementation:**

### Step 1: Identify Feature Modules

Check `code_changes.md` for list of NEW or MODIFIED files for THIS feature:

```markdown
## Files Changed (example)
- NEW: league_helper/util/PlayerRatingManager.py
- MODIFIED: league_helper/LeagueHelper.py
- MODIFIED: run_league_helper.py
```

### Step 2: Test Each Module Import

```bash
# Test new modules
python -c "from league_helper.util.PlayerRatingManager import PlayerRatingManager"
python -c "import league_helper.util.PlayerRatingManager"

# Test modified modules still import
python -c "from league_helper.LeagueHelper import LeagueHelper"
python -c "import run_league_helper"
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
- Example: `python run_league_helper.py --mode rating_helper`
- Example: `python run_simulation.py --use-ratings`

### Step 2: Test Feature Help

```bash
# If feature adds new mode
python run_league_helper.py --mode rating_helper --help

# If feature adds new flag
python run_simulation.py --help
# (verify --use-ratings appears in help text)
```

### Step 3: Test Feature Initialization

```bash
# Basic startup test (dry-run or help mode)
python run_league_helper.py --mode rating_helper --dry-run
```

**Expected:**
- Help text displays (if `--help`)
- Feature initializes without crashing (if dry-run)
- Error messages are helpful (not stack traces)

---

## Part 3: E2E Execution Test (Feature-Specific - CRITICAL)

**📖 See `reference/smoke_testing_pattern.md` for universal E2E test pattern and data validation examples.**

**Feature-specific implementation:**

### Step 1: Identify Feature Workflow

From `spec.md`, identify the primary use case:

**Example spec excerpt:**
```markdown
## Primary Use Case
User runs rating helper mode to apply ADP-based player rating multipliers
to draft recommendations, updating 6 position-specific JSON files with
multiplier values between 0.5 and 1.5 based on ADP ranges.
```

### Step 2: Prepare Real Input Data

**Use PRODUCTION or PRODUCTION-LIKE data:**
- ✅ Real player CSV files from `data/`
- ✅ Real league config from `data/league_config.json`
- ❌ NOT test fixtures
- ❌ NOT mocked data

### Step 3: Execute Feature End-to-End

```bash
# Run feature with real data
python run_league_helper.py --mode rating_helper --data-folder ./data
```

**Monitor for:**
- Script completes without crashes
- No unexpected errors/warnings in logs
- Output files created

### Step 4: CRITICAL - Verify Output DATA VALUES

**📖 See pattern file for data validation examples.**

**Feature-specific validation (example for rating multiplier feature):**

```python
import json
from pathlib import Path

# Feature updates 6 position files
positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']

for pos in positions:
    pos_file = Path(f"data/{pos.lower()}_ratings.json")

    # Part 3a: Structure validation
    assert pos_file.exists(), f"{pos} file missing"

    with open(pos_file) as f:
        data = json.load(f)
    assert len(data) > 0, f"{pos} file is empty"

    # Part 3b: DATA VALUE validation (CRITICAL)
    first_player = data[0]

    # Verify multiplier field exists and has value
    assert 'adp_multiplier' in first_player, f"{pos} missing adp_multiplier field"
    assert first_player['adp_multiplier'] is not None, f"{pos} multiplier is None"

    # Verify multiplier is in expected range (from spec: 0.5 to 1.5)
    multiplier = first_player['adp_multiplier']
    assert 0.5 <= multiplier <= 1.5, f"{pos} multiplier {multiplier} out of range"

    # Verify multiplier is not placeholder (common bug)
    assert multiplier != 1.0, f"{pos} multiplier is placeholder value (1.0)"

    # Sample check: At least some players have non-1.0 multipliers
    multipliers = [p['adp_multiplier'] for p in data[:10]]
    non_default = [m for m in multipliers if m != 1.0]
    assert len(non_default) > 0, f"{pos} all multipliers are default (1.0)"

print("✅ All 6 positions have valid multiplier data")
```

**Key validation points:**
1. ✅ Files exist (structure)
2. ✅ Files have data (not empty)
3. ✅ Fields exist (schema)
4. ✅ Values are correct type (float not string)
5. ✅ Values in expected range (0.5-1.5 from spec)
6. ✅ Values are NOT placeholders (not all 1.0)
7. ✅ Sample actual data looks reasonable

**If validation reveals issues:**
- Document what failed and why
- Identify root cause (algorithm bug, config issue, mock mismatch)
- Fix ALL issues
- RE-RUN ALL 3 PARTS from Part 1

---

## Pass/Fail Criteria

**📖 See `reference/smoke_testing_pattern.md` for universal pass criteria.**

**Feature-specific criteria:**

**✅ PASS if:**
- Part 1: All feature modules import successfully
- Part 2: Feature mode/options work correctly
- Part 3: Feature executes end-to-end AND output data values verified correct

**❌ FAIL if:**
- Part 1: Any import errors
- Part 2: Help missing, crashes on startup
- Part 3: Execution crashes OR output missing OR **data values incorrect/missing/placeholder**

**If FAIL:**
1. Document failure in feature README
2. Identify root cause
3. Fix ALL issues found
4. RE-RUN ALL 3 PARTS (not just failed part)
5. Do NOT proceed to Stage 5cb until all parts pass

---

## Common Feature-Specific Issues

### Issue 1: Feature Works in Tests But Not with Real Data

**Symptom:** Unit tests pass (100%) but Part 3 fails with real data

**Root Cause:** Mocked dependencies behave differently than real dependencies

**Example:**
```python
# Test mocked this to return 170.0 for all players
mock_api.get_adp.return_value = 170.0

# But real API returns None for some players (not in database)
# Feature crashed on None value
```

**Fix:** Update implementation to handle real-world edge cases (None, missing data, API errors)

### Issue 2: Output Structure Correct But Values Wrong

**Symptom:** Files created, have rows, but all values are zeros/placeholders

**Root Cause:** Forgot to actually populate data (just created structure)

**Example:**
```python
# WRONG - creates structure but doesn't populate
players = []
for p in raw_data:
    players.append({'name': p.name, 'multiplier': 1.0})  # Placeholder!

# CORRECT - actually calculate values
players = []
for p in raw_data:
    multiplier = calculate_multiplier(p.adp)  # Real calculation
    players.append({'name': p.name, 'multiplier': multiplier})
```

**Fix:** Verify algorithms are actually executing (not just creating placeholders)

### Issue 3: Works for Some Categories But Not All

**Symptom:** QB file correct but other positions missing/wrong

**Root Cause:** Algorithm only tested with one category, doesn't generalize

**Fix:** Verify implementation works for ALL categories (loop through all in Part 3)

---

## Re-Reading Checkpoint

**After completing all 3 parts:**

1. **Re-read Critical Rules** (top of this guide)
2. **Re-read Pattern File** (`reference/smoke_testing_pattern.md` - Common Mistakes section)
3. **Verify data VALUES inspected** (not just "file exists")
4. **Update README Agent Status**

---

## Next Steps

**If ALL 3 parts PASSED:**
- ✅ Document smoke test results in feature README
- ✅ Update Agent Status: "Smoke Testing COMPLETE"
- ✅ Proceed to **Stage 5cb: QC Rounds**

**If ANY part FAILED:**
- ❌ Fix ALL issues identified
- ❌ RE-RUN ALL 3 PARTS from Part 1
- ❌ Do NOT proceed to QC Rounds until clean pass

---

## Summary

**Feature-Level Smoke Testing validates:**
- Feature modules import correctly (Part 1)
- Feature entry point works (Part 2)
- Feature executes end-to-end with REAL data producing CORRECT values (Part 3)

**Key Differences from Epic-Level:**
- Tests feature in ISOLATION (not with other features)
- 3 parts only (no Part 4 cross-feature integration)
- Next stage: QC Rounds for THIS feature (Stage 5cb)

**Critical Success Factors:**
- Use REAL data (not test fixtures)
- Verify DATA VALUES (not just structure)
- Re-run ALL parts if any fail
- Document all results

**📖 For universal patterns and detailed examples, see:**
`reference/smoke_testing_pattern.md`

---

**END OF STAGE 5ca GUIDE**
