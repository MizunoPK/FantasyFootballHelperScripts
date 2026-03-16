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

1. [🚨 MANDATORY READING PROTOCOL](#🚨-mandatory-reading-protocol)
2. [Overview](#overview)
3. [🛑 Critical Rules (Feature-Specific)](#🛑-critical-rules-feature-specific)
4. [Prerequisites Checklist](#prerequisites-checklist)
5. [Workflow Overview](#workflow-overview)
6. [Part 1: Import Test (Feature-Specific)](#part-1-import-test-feature-specific)
7. [Part 2: Entry Point Test (Feature-Specific)](#part-2-entry-point-test-feature-specific)
8. [Part 3: E2E Execution Test (Feature-Specific - CRITICAL)](#part-3-e2e-execution-test-feature-specific---critical)
9. [Pass/Fail Criteria](#passfail-criteria)
10. [Common Feature-Specific Issues](#common-feature-specific-issues)
11. [🛑 MANDATORY CHECKPOINT 1](#🛑-mandatory-checkpoint-1)
12. [Next Steps](#next-steps)
13. [Summary](#summary)
14. [Exit Criteria](#exit-criteria)

---
## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Smoke Testing — including when resuming a prior session — you MUST:**

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

## 🚫 FORBIDDEN SHORTCUTS

You CANNOT:
- Skip Part 2 (Entry Point Test) or Part 3 (E2E Execution Test) because Part 1 (Import Test) passed — all 3 parts are mandatory; Part 3 is marked CRITICAL because it validates actual runtime behavior
- Declare smoke testing complete based on Part 1 results alone — Part 3's E2E test with real data verification is required before proceeding to S7.P2

If you are about to do any of the above: STOP and re-read the relevant section.

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
- [ ] `implementation_checklist.md` all requirements verified
- [ ] All code committed to git (clean working directory)
- [ ] Tests per Testing Approach (read EPIC_README):
  - Option A (smoke only): Mini-QC checkpoints passed — no automated test prerequisite
  - Option B (integration scripts): Integration test script created (may have partial passes from S6)
  - Option C (unit tests): Unit tests passing for algorithmic functions identified in S5 (100%)
  - Option D (both): Both unit tests passing AND integration script created

**Files that must exist:**
- [ ] `feature_XX_{name}/spec.md` (primary specification)
- [ ] `feature_XX_{name}/checklist.md` (planning decisions)
- [ ] `feature_XX_{name}/implementation_plan.md` (implementation guidance)
- [ ] `feature_XX_{name}/implementation_checklist.md` (progress tracking and requirement verification)
- [ ] For Options B/D: Integration test script at location per `Integration Test Convention:` in EPIC_README

**Verification:**
- [ ] For Options C/D: Run `{UNIT_TEST_COMMAND}` → exit code 0
- [ ] For Options B/D: Run `{INTEGRATION_SCRIPT_COMMAND}` → verify script runs (full pass not yet required)
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

### First: Read the Epic's Testing Approach

Read `Testing Approach:` from EPIC_README (at epic folder root). This determines which Part 3 path to follow.

---

### Path B/D — Integration Script Opted In

**📖 See `reference/smoke_testing_pattern.md` → "Part 3 Detail: Testing Approach Paths" → "Path B/D" for the full process.**

Run the feature's integration test script per the `Integration Test Convention:` in EPIC_README. The script encodes all 6 manual validation steps — run it and verify exit code 0.

---

### Path A/C — Manual 6-Step E2E Process

**📖 See `reference/smoke_testing_pattern.md` → "Part 3 Detail: Testing Approach Paths" → "Path A/C" for the full 6-step process** (test artifact creation, environment prep, test data, execution, output structure validation, data values validation, log check).

**📖 Mandatory logging requirements:** `reference/smoke_testing_pattern.md` → "Mandatory Logging Requirements"

For Option C: unit tests are a prerequisite from S6, not a replacement for Part 3 — the manual E2E smoke test still runs to validate real-data behavior.

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

**📖 See `reference/smoke_testing_pattern.md` → "Platform-Specific Considerations" for Windows file locking with log handlers (`PermissionError` / `WinError 32` during temp directory cleanup).**

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

S7.P1 is complete when all 3 parts pass per the Pass/Fail Criteria above and Agent Status is updated.

---
---

## Next Phase

**After completing S7.P1 (Smoke Testing):**

- Smoke testing passed (all 3 parts clean, REAL data verified)
- Proceed to: `stages/s7/s7_p2_qc_rounds.md` (QC Rounds)

**See also:** `prompts_reference_v2.md` → "Starting S7.P2" prompt

---

**END OF STAGE S7.P1 GUIDE**
