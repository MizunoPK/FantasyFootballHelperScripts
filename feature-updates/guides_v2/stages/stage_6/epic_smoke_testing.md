# STAGE 6a: Epic Smoke Testing Guide

🚨 **MANDATORY READING PROTOCOL**

**Before starting this stage:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update epic EPIC_README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check EPIC_README.md Agent Status for current step
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Quick Start

**What is this stage?**
Epic Smoke Testing is the first validation step for the complete epic after ALL features are implemented. Unlike feature-level smoke testing (Stage 5c), this stage tests ALL features working together as a cohesive system, executing the evolved epic_smoke_test_plan.md and validating cross-feature integration.

**When do you use this guide?**
- After ALL features have completed Stage 5e
- No pending bug fixes
- epic_smoke_test_plan.md has been evolved through Stages 1, 4, and 5e
- Ready to validate epic as a whole

**Key Outputs:**
- ✅ All features verified complete (Stage 5e)
- ✅ Epic smoke test plan executed (all parts passed)
- ✅ Cross-feature integration verified (features work together)
- ✅ Epic-level workflows tested end-to-end
- ✅ Data values validated (not just structure)

**Time Estimate:**
20-30 minutes for 3-feature epics, 30-60 minutes for 5+ feature epics

**Exit Condition:**
Epic Smoke Testing is complete when ALL parts of epic_smoke_test_plan.md pass, all cross-feature integration scenarios work correctly, and data values are verified (not just structure)

---

## Critical Rules

```
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL features MUST complete Stage 5e before starting
   - Verify EVERY feature shows "Stage 5e complete" in EPIC_README.md
   - Verify no pending features or bug fixes
   - Do NOT start if any feature is incomplete

2. ⚠️ Use EVOLVED epic_smoke_test_plan.md (NOT original)
   - Plan evolved through Stages 1 → 4 → 5e updates
   - Reflects ACTUAL implementation (not initial assumptions)
   - Contains integration scenarios added during Stage 5e

3. ⚠️ Epic testing ≠ Feature testing
   - Feature testing (5c): Tests feature in isolation
   - Epic testing (6a): Tests ALL features working together
   - Focus: Cross-feature workflows, integration points

4. ⚠️ Validate DATA VALUES (not just structure)
   - ❌ BAD: "File exists, looks good"
   - ✅ GOOD: `assert df['adp_multiplier'].between(0.5, 1.5).all()`
   - Verify actual data values match expected ranges

5. ⚠️ If smoke testing fails → Fix issues, RESTART Step 2
   - Do NOT proceed to QC rounds with failing smoke tests
   - Fix ALL issues found
   - Re-run entire smoke testing process
   - Do NOT skip any parts

6. ⚠️ Execute ALL parts of epic_smoke_test_plan.md
   - Part 1: Epic-level import tests
   - Part 2: Epic-level entry point tests
   - Part 3: Epic end-to-end execution tests
   - Part 4: Cross-feature integration tests
```

---

## Critical Decisions Summary

**This stage has ONE critical decision point:**

### Decision Point: Smoke Testing Result (PASS/FAIL)

**Question:** Did ALL parts of smoke testing pass?
- **If ALL PASSED:** Proceed to STAGE_6b (Epic QC Rounds)
- **If ANY FAILED:** Fix issues, RESTART Step 2 (re-run all parts)
- **Impact:** Cannot proceed to QC rounds with failing smoke tests

**Why this matters:** Smoke testing validates basic epic functionality. If it fails, deeper QC will also fail. Fix foundational issues first.

---

## Prerequisites Checklist

**Before starting Epic Smoke Testing (STAGE_6a), verify:**

□ **ALL features complete:**
  - EVERY feature shows "Stage 5e complete" in EPIC_README.md Epic Progress Tracker
  - All features show ✅ in Stage 5e column
  - No features with "In progress" or "Not started" status

□ **No pending bug fixes:**
  - No `bugfix_{priority}_{name}/` folders with incomplete status
  - If bug fix folders exist, they're at Stage 5c (complete)

□ **Epic smoke test plan evolved:**
  - epic_smoke_test_plan.md shows "Last Updated" from RECENT Stage 5e
  - Update History table shows ALL features contributed updates
  - Test scenarios reflect ACTUAL implementation

□ **Original epic request available:**
  - `{epic_name}.txt` file exists in feature-updates/ folder
  - Contains user's original epic request

□ **EPIC_README.md ready:**
  - Epic Progress Tracker shows all features at 5e
  - Agent Status section exists

**If any prerequisite fails:**
- ❌ Do NOT start Epic Smoke Testing
- Complete missing prerequisites first
- Return to STAGE_6a when all prerequisites met

---

## Workflow Overview

```
STAGE 6a: Epic Smoke Testing
│
├─> STEP 1: Pre-QC Verification
│   ├─ Verify all features at Stage 5e
│   ├─ Verify no pending bug fixes
│   ├─ Read evolved epic_smoke_test_plan.md
│   └─ Read original epic request
│
├─> STEP 2: Epic Smoke Testing
│   ├─ Part 1: Epic-level import tests
│   ├─ Part 2: Epic-level entry point tests
│   ├─ Part 3: Epic end-to-end execution tests
│   ├─ Part 4: Cross-feature integration tests
│   └─ Verify ALL output DATA values
│
└─> Decision: Smoke Testing Result
    ├─ PASS → Proceed to STAGE_6b
    └─ FAIL → Fix issues, RESTART Step 2
```

---

## STEP 1: Pre-QC Verification

**Objective:** Verify epic is ready for Stage 6 validation.

---

### Step 1.1: Verify All Features Complete

**Read EPIC_README.md "Epic Progress Tracker" section:**

```markdown
## Epic Progress Tracker
| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_adp_integration | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_02_matchup_system | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_03_performance_tracker | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
```

**Verify:** EVERY feature shows ✅ in Stage 5e column.

**If ANY feature is incomplete:**
- STOP Stage 6a
- Complete the incomplete feature first
- Return to Stage 6a when ALL features at 5e

**Document verification:**
```markdown
**Pre-QC Verification:**
- Total features: {N}
- Features at Stage 5e: {M}
- Verification: {✅ ALL COMPLETE / ❌ {X} INCOMPLETE}
```

---

### Step 1.2: Verify No Pending Bug Fixes

**Check epic folder for any `bugfix_{priority}_{name}/` folders:**

```bash
ls feature-updates/{epic_name}/
```

**Look for:** Any folders starting with `bugfix_`

**If bug fix folders exist:**
- Read their README.md for completion status
- If incomplete → Complete bug fix first
- If complete → Verify they're at Stage 5c (bug fixes don't do 5d/5e)

**Document verification:**
```markdown
**Bug Fix Check:**
- Bug fix folders found: {N}
- All complete: {✅ YES / ❌ NO}
- Status: {READY / BLOCKED}
```

---

### Step 1.3: Read Evolved Epic Smoke Test Plan

**Use Read tool to load `epic_smoke_test_plan.md`:**

**Example structure:**
```markdown
# Epic Smoke Test Plan: {epic_name}

**Last Updated:** Stage 5e (feature_03_performance_tracker) - 2025-12-30

## Update History
| Stage | Feature | Date | Changes Made |
|-------|---------|------|--------------|
| 1 | (initial) | 2025-12-15 | Created placeholder test plan |
| 4 | (all features) | 2025-12-20 | Updated based on deep dive findings |
| 5e | feature_01 | 2025-12-25 | Added ADP integration scenarios |
| 5e | feature_02 | 2025-12-28 | Added matchup system cross-checks |
| 5e | feature_03 | 2025-12-30 | Added performance tracking E2E tests |

## Test Scenarios

### Scenario 1: Complete Draft Workflow
**Added:** Stage 4
**Updated:** Stage 5e (feature_01, feature_02, feature_03)

**What to test:** Draft mode with all features enabled
**How to test:** `python run_league_helper.py --mode draft --week 1`
**Expected result:**
- ADP multipliers applied to all players
- Matchup difficulty reflected in scores
- Performance tracking initialized

[... more scenarios ...]
```

**Verify:**
- Plan shows "Last Updated" from RECENT Stage 5e (not Stage 1 or 4)
- Update History table shows ALL features contributed updates
- Test scenarios reflect ACTUAL implementation (not original assumptions)

**Document verification:**
```markdown
**Epic Smoke Test Plan Review:**
- Last updated: {Stage and date}
- Features contributed: {N}/{M}
- Integration scenarios: {count}
- Status: {✅ READY / ❌ OUTDATED}
```

---

### Step 1.4: Read Original Epic Request

**Use Read tool to load `{epic_name}.txt` (the user's original request):**

**Example:**
```
Epic Request: Improve Draft Helper System

Goals:
- Integrate ADP data for market wisdom
- Add matchup-based projections
- Track player performance vs projections

Expected Outcome:
User can make better draft decisions by seeing:
1. Market consensus (ADP)
2. Matchup difficulty
3. Historical accuracy of projections
```

**Why this matters:** Stage 6 validates against THIS original vision, not intermediate specs that may have evolved.

**Document review:**
```markdown
**Original Epic Request Review:**
- Epic name: {name}
- Primary goals: {N}
- Expected outcomes: {list}
- Status: {✅ REVIEWED}
```

---

### Step 1.5: Update Agent Status

**Update EPIC_README.md Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** EPIC_FINAL_QC
**Current Step:** Step 1 complete, starting Step 2 (Epic Smoke Testing)
**Current Guide:** stages/stage_6/epic_smoke_testing.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}
**Critical Rules from Guide:**
- ALL features at Stage 5e (verified)
- Use EVOLVED epic_smoke_test_plan.md (not original)
- Test cross-feature integration (not just individual features)
- Validate DATA VALUES (not just structure)

**Progress:** Step 1 complete (Pre-QC Verification)
**Next Action:** Step 2 - Execute epic_smoke_test_plan.md
**Blockers:** None
```

---

## STEP 2: Epic Smoke Testing

**Objective:** Execute evolved epic_smoke_test_plan.md to verify epic works end-to-end.

**Critical Distinction:**
- **Feature smoke testing (Stage 5c):** Tests individual feature in isolation
- **Epic smoke testing (Stage 6a):** Tests ALL features working together as a cohesive system

---

### Step 2.1: Part 1 - Epic-Level Import Tests

**Objective:** Verify all new modules can be imported together without conflicts.

**Execute EACH import test from epic_smoke_test_plan.md:**

**Example tests:**
```python
# Test 1: Import all feature modules
python -c "from feature_01 import AdpIntegration; from feature_02 import MatchupSystem; from feature_03 import PerformanceTracker"

# Test 2: Import main entry points
python -c "from league_helper import DraftMode, AnalysisMode"

# Test 3: Import utilities used by multiple features
python -c "from utils import player_matching, data_loader"
```

**Expected:** No import errors, no circular dependencies, no missing modules.

**If imports fail:**
- Document exact error with full traceback
- Identify which feature's module is causing the issue
- Fix import issues (may require code changes)
- Re-run Part 1

**Document results:**
```markdown
### Part 1: Epic-Level Import Tests

**Status:** {✅ PASSED / ❌ FAILED}

**Tests Executed:** {N}
**Tests Passed:** {M}

**Failed Tests:**
{If any, list with error messages}

**Issues Found:**
{Any import conflicts, circular dependencies, missing modules}
```

**If Part 1 fails:**
- STOP - Do not proceed to Part 2
- Fix all import issues
- Re-run Part 1 until all tests pass

---

### Step 2.2: Part 2 - Epic-Level Entry Point Tests

**Objective:** Verify epic-level entry points start correctly and display proper help/options.

**Execute EACH entry point test from epic_smoke_test_plan.md:**

**Example tests:**
```bash
# Test 1: Draft mode entry point
python run_league_helper.py --mode draft --help

# Test 2: Analysis mode entry point
python run_league_helper.py --mode analysis --help

# Test 3: Performance tracking mode
python run_league_helper.py --mode performance --help

# Test 4: Verify new options from features are available
python run_league_helper.py --mode draft --help | grep "adp"
python run_league_helper.py --mode draft --help | grep "matchup"
```

**Expected:**
- Help text displays correctly
- No crashes or errors
- Correct options shown (including new feature options)
- Option descriptions are accurate

**If entry points fail:**
- Document exact error
- Identify which feature's entry point is causing the issue
- Fix entry point issues
- Re-run Part 2

**Document results:**
```markdown
### Part 2: Epic-Level Entry Point Tests

**Status:** {✅ PASSED / ❌ FAILED}

**Entry Points Tested:** {N}
**Entry Points Passed:** {M}

**Failed Tests:**
{If any, list with error messages}

**Issues Found:**
{Any crashes, missing options, incorrect descriptions}
```

**If Part 2 fails:**
- STOP - Do not proceed to Part 3
- Fix all entry point issues
- Re-run Part 2 until all tests pass

---

### Step 2.3: Part 3 - Epic End-to-End Execution Tests

**Objective:** Execute epic-level workflows with REAL data and verify correct DATA VALUES.

**⚠️ CRITICAL:** Verify DATA VALUES, not just structure:
- ✅ GOOD: `assert df['adp_multiplier'].between(0.5, 1.5).all()`
- ❌ BAD: "File exists, looks good"

**Execute EACH scenario from epic_smoke_test_plan.md:**

**Example Scenario 1: Complete Draft Workflow**
```bash
python run_league_helper.py --mode draft --week 1 --iterations 10
```

**Expected result with DATA VALUE verification:**
```python
# Load output file
df = pd.read_csv('output/draft_recommendations.csv')

# Verify ADP multipliers applied (Feature 01)
assert 'adp_multiplier' in df.columns
assert df['adp_multiplier'].between(0.5, 1.5).all()
assert df['adp_multiplier'].notna().all()

# Verify matchup difficulty reflected (Feature 02)
assert 'matchup_difficulty' in df.columns
assert df['matchup_difficulty'].isin(['easy', 'medium', 'hard']).all()

# Verify performance tracking initialized (Feature 03)
assert 'performance_score' in df.columns
assert df['performance_score'].between(0, 100).all()

# Verify final scores show combined effects
assert 'final_score' in df.columns
assert df['final_score'] != df['base_score']  # Multipliers applied
```

**Example Scenario 2: Analysis Workflow**
```bash
python run_league_helper.py --mode analysis --player "Patrick Mahomes"
```

**Expected result:**
```python
# Load output
with open('output/player_analysis.json', 'r') as f:
    data = json.load(f)

# Verify all features contributed data
assert 'adp_data' in data  # Feature 01
assert 'matchup_projections' in data  # Feature 02
assert 'historical_performance' in data  # Feature 03

# Verify data values are reasonable
assert 0 < data['adp_data']['rank'] <= 500
assert 0.5 <= data['adp_data']['multiplier'] <= 1.5
assert data['matchup_projections']['difficulty'] in ['easy', 'medium', 'hard']
assert 0 <= data['historical_performance']['accuracy'] <= 100
```

**Execute ALL scenarios** from epic_smoke_test_plan.md.

**Document results:**
```markdown
### Part 3: Epic End-to-End Execution Tests

**Status:** {✅ PASSED / ❌ FAILED}

**Scenarios Tested:** {N}
**Scenarios Passed:** {M}

**Scenario Results:**
- Scenario 1 (Draft Workflow): {✅ PASSED / ❌ FAILED}
  - ADP multipliers verified: {✅}
  - Matchup difficulty verified: {✅}
  - Performance tracking verified: {✅}

- Scenario 2 (Analysis Workflow): {✅ PASSED / ❌ FAILED}
  - ADP data verified: {✅}
  - Matchup projections verified: {✅}
  - Historical performance verified: {✅}

[... more scenarios ...]

**Issues Found:**
{Any incorrect data values, missing fields, wrong ranges}
```

**If Part 3 fails:**
- STOP - Do not proceed to Part 4
- Fix all execution issues
- Re-run Part 3 until all scenarios pass with correct DATA VALUES

---

### Step 2.4: Part 4 - Cross-Feature Integration Tests

**Objective:** Execute integration scenarios that test feature INTERACTIONS (not individual features).

**Why this matters:** Integration scenarios test how features work TOGETHER:
- Do Feature 01 outputs correctly feed into Feature 02?
- Do features conflict or interfere with each other?
- Do combined multipliers produce expected results?

**Execute EACH integration scenario from epic_smoke_test_plan.md:**

**Example Integration Scenario 1: ADP + Matchup Integration**
```markdown
**Scenario:** ADP + Matchup Integration
**Added:** Stage 5e (feature_02_matchup_system)

**What to test:** Verify ADP multipliers don't override matchup difficulty

**How to test:**
1. Run draft mode with both features enabled
2. Find player with high ADP (top 10) facing tough matchup
3. Verify final score shows BOTH effects

**Expected result:**
- Player with ADP=5 (mult≈1.2) + tough matchup (mult≈0.8)
- Final score = base * 1.2 * 0.8 ≈ base * 0.96
```

**Verification code:**
```python
# Find player matching criteria
player = df[(df['adp_rank'] <= 10) & (df['matchup_difficulty'] == 'hard')].iloc[0]

# Verify both multipliers applied
assert 1.1 <= player['adp_multiplier'] <= 1.3  # High ADP bonus
assert 0.7 <= player['matchup_multiplier'] <= 0.9  # Tough matchup penalty

# Verify final score shows BOTH effects
expected_score = player['base_score'] * player['adp_multiplier'] * player['matchup_multiplier']
assert abs(player['final_score'] - expected_score) < 0.01
```

**Example Integration Scenario 2: Performance Tracking Feedback Loop**
```markdown
**Scenario:** Performance Tracking Affects ADP Confidence
**Added:** Stage 5e (feature_03_performance_tracker)

**What to test:** Verify performance history adjusts ADP confidence

**How to test:**
1. Run analysis for player with poor historical accuracy
2. Verify ADP multiplier is dampened by low confidence

**Expected result:**
- Player with ADP=10 normally gets mult≈1.15
- But with 30% accuracy, confidence dampens to mult≈1.05
```

**Execute ALL integration scenarios** from epic_smoke_test_plan.md.

**Document results:**
```markdown
### Part 4: Cross-Feature Integration Tests

**Status:** {✅ PASSED / ❌ FAILED}

**Integration Scenarios Tested:** {N}
**Integration Scenarios Passed:** {M}

**Scenario Results:**
- ADP + Matchup Integration: {✅ PASSED / ❌ FAILED}
  - Both multipliers verified: {✅}
  - Combined effect correct: {✅}

- Performance Tracking Feedback: {✅ PASSED / ❌ FAILED}
  - Confidence dampening verified: {✅}
  - ADP adjustment correct: {✅}

[... more scenarios ...]

**Issues Found:**
{Any feature conflicts, incorrect interactions, missing feedback loops}
```

**If Part 4 fails:**
- STOP - Document ALL failures
- Fix all integration issues
- Re-run Part 4 until all scenarios pass

---

### Step 2.5: Document Epic Smoke Testing Results

**Create summary in epic_smoke_test_plan.md:**

```markdown
---

## Epic Smoke Testing Results (Stage 6a)

**Date:** {YYYY-MM-DD}
**Status:** {✅ PASSED / ❌ FAILED}

**Part 1 (Import Tests):** {✅ PASSED / ❌ FAILED}
- Tests executed: {N}
- Tests passed: {M}
- Issues found: {list or "None"}

**Part 2 (Entry Points):** {✅ PASSED / ❌ FAILED}
- Entry points tested: {N}
- Entry points passed: {M}
- Issues found: {list or "None"}

**Part 3 (E2E Tests):** {✅ PASSED / ❌ FAILED}
- Scenarios tested: {N}
- Scenarios passed: {M}
- DATA VALUES verified: {✅ YES / ❌ NO}
- Issues found: {list or "None"}

**Part 4 (Integration Tests):** {✅ PASSED / ❌ FAILED}
- Integration scenarios tested: {N}
- Integration scenarios passed: {M}
- Issues found: {list or "None"}

**Overall Status:** {✅ ALL PASSED / ❌ FAILURES FOUND}

**Issues to Fix:**
{If any failures, list all issues with details}

**Next Steps:**
{If PASSED: "Proceed to STAGE_6b (Epic QC Rounds)"}
{If FAILED: "Fix issues listed above, RESTART Step 2"}
```

---

### Step 2.6: Handle Smoke Testing Failures (If Any)

**If ANY part of smoke testing failed:**

**DO NOT:**
- ❌ Proceed to Stage 6b with failing tests
- ❌ Mark issues as "minor" or "acceptable"
- ❌ Skip failed scenarios

**DO:**
1. **Document ALL failures** in epic_smoke_test_plan.md results section
2. **Create bug fixes** for integration issues (if needed)
   - Use bug fix workflow: Stage 2 → 5a → 5b → 5c
   - Bug fixes for epic-level issues go in epic folder
3. **Fix issues** directly in feature code (if simple fixes)
4. **RESTART Step 2** - Re-run ALL parts:
   - Part 1: Import tests
   - Part 2: Entry point tests
   - Part 3: E2E execution tests
   - Part 4: Integration tests
5. **Update epic_smoke_test_plan.md** if tests revealed missing scenarios

**Example bug fix creation:**
```markdown
**Issue:** ADP + Matchup integration produces incorrect combined score

**Root Cause:** Multipliers applied in wrong order

**Fix Required:** Update PlayerManager.calculate_final_score() to apply multipliers correctly

**Action:** Create bugfix_high_multiplier_order/
```

---

### Step 2.7: Update Agent Status (After Smoke Testing Passes)

**Update EPIC_README.md Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** EPIC_FINAL_QC
**Current Step:** Step 2 complete (Epic Smoke Testing PASSED)
**Current Guide:** stages/stage_6/epic_smoke_testing.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** STAGE_6a complete (Epic Smoke Testing)
**Next Action:** Transition to Epic QC Rounds
**Next Guide:** stages/stage_6/epic_qc_rounds.md
**Blockers:** None

**Smoke Testing Results:**
- Import tests: ✅ {N}/{N} passed
- Entry point tests: ✅ {M}/{M} passed
- E2E execution tests: ✅ {K}/{K} passed
- Integration tests: ✅ {L}/{L} passed
- Overall: ✅ ALL PASSED
```

---

## Completion Criteria

**STAGE_6a (Epic Smoke Testing) is complete when ALL of these are true:**

### Pre-QC Verification Complete
- [ ] All features verified at Stage 5e (checked EPIC_README.md)
- [ ] No pending bug fixes (checked epic folder)
- [ ] epic_smoke_test_plan.md reviewed (evolved from Stages 1, 4, 5e)
- [ ] Original epic request reviewed ({epic_name}.txt)

### Epic Smoke Testing Complete
- [ ] Part 1: ALL import tests passed
- [ ] Part 2: ALL entry point tests passed
- [ ] Part 3: ALL E2E execution tests passed with DATA VALUES verified
- [ ] Part 4: ALL cross-feature integration tests passed

### Results Documented
- [ ] Epic smoke testing results section created in epic_smoke_test_plan.md
- [ ] All test results documented (pass/fail for each part)
- [ ] DATA VALUE verification documented (not just structure)
- [ ] Any issues documented with details

### Agent Status Updated
- [ ] EPIC_README.md Agent Status shows STAGE_6a complete
- [ ] Next action: Transition to Epic QC Rounds (stages/stage_6/epic_qc_rounds.md)
- [ ] No blockers

**If ANY item unchecked → STAGE_6a NOT complete**

**When ALL items checked:**
✅ STAGE_6a COMPLETE
→ Proceed to STAGE_6b (Epic QC Rounds)

---

## Common Mistakes to Avoid

```
┌─────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection   │
└─────────────────────────────────────────────────────────────┘

❌ "One feature is at 5d, close enough to 5e, I'll proceed"
   ✅ STOP - ALL features must be at 5e, no exceptions

❌ "Epic smoke test plan was updated in Stage 4, that's recent enough"
   ✅ STOP - Must be updated in Stage 5e (reflects actual implementation)

❌ "Imports work, that's enough for Part 1"
   ✅ STOP - Also check for circular dependencies, no warnings

❌ "File exists and has data, Part 3 passes"
   ✅ STOP - Must verify ACTUAL DATA VALUES (ranges, formats, correctness)

❌ "Features work individually, integration will be fine"
   ✅ STOP - Must test cross-feature integration explicitly (Part 4)

❌ "One integration test failed but others passed, I'll proceed"
   ✅ STOP - ALL tests must pass, fix failures and RESTART

❌ "I'll skip smoke testing and go straight to QC rounds"
   ✅ STOP - Smoke testing is MANDATORY before QC rounds

❌ "Epic smoke testing is the same as feature smoke testing"
   ✅ STOP - Epic tests ALL features together, feature tests isolation
```

---

## Next Stage

**After completing STAGE_6a:**

📖 **READ:** `stages/stage_6/epic_qc_rounds.md`
🎯 **GOAL:** Execute 3 QC rounds validating epic cohesion and integration
⏱️ **ESTIMATE:** 30-60 minutes (3 rounds)

**Stage 6b will:**
- QC Round 1: Cross-feature integration validation
- QC Round 2: Epic cohesion and consistency
- QC Round 3: End-to-end success criteria
- Document findings for each round
- Restart protocol if any issues found

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting STAGE_6b.

---

*End of stages/stage_6/epic_smoke_testing.md*
