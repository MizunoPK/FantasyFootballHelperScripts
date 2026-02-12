# S9.P1: Epic Smoke Testing

**Purpose:** Validate the complete epic end-to-end with ALL features working together through mandatory 4-part smoke testing.

**File:** `s9_p1_epic_smoke_testing.md`

**Stage Flow Context:**
```text
S8 (ALL features complete) →
→ [YOU ARE HERE: S9.P1 - Epic Smoke Testing] →
→ S9.P2 (Epic QC Validation Loop) → S9.P3 (User Testing) → S9.P4 (Epic Final Review) → S10
```

---

## 🚨 MANDATORY READING PROTOCOL

**BEFORE starting Epic Smoke Testing, you MUST:**

1. **Read the smoke testing pattern:** `reference/smoke_testing_pattern.md`
   - Understand universal smoke testing workflow
   - Review critical rules that apply to ALL smoke testing
   - Study common mistakes to avoid

2. **Use the phase transition prompt** from `prompts/s9_prompts.md`
   - Find "Starting S9: Epic Final QC" prompt
   - Acknowledge critical requirements
   - List requirements from this guide

3. **Update EPIC_README.md Agent Status** with:
   - Current Phase: S9.P1 - Epic Smoke Testing
   - Current Guide: `stages/s9/s9_p1_epic_smoke_testing.md`
   - Guide Last Read: {YYYY-MM-DD HH:MM}
   - Critical Rules: "4 parts MANDATORY", "Use EVOLVED test plan", "Verify DATA VALUES", "Restart if ANY fails"
   - Next Action: Execute Step 1 - Pre-QC Verification

4. **Verify all prerequisites** (see checklist below)

5. **THEN AND ONLY THEN** begin epic smoke testing

**This is NOT optional.** Reading both the pattern and this guide ensures you validate the epic correctly.

---

## Table of Contents

1. [🚨 MANDATORY READING PROTOCOL](#-mandatory-reading-protocol)
2. [Overview](#overview)
3. [🛑 Critical Rules (Epic-Specific)](#-critical-rules-epic-specific)
4. [Prerequisites Checklist](#prerequisites-checklist)
5. [Workflow Overview](#workflow-overview)
6. [STEP 1: Pre-QC Verification](#step-1-pre-qc-verification)
7. [Epic Progress Tracker](#epic-progress-tracker)
8. [Part 1: Epic Import Test](#part-1-epic-import-test)
9. [Part 2: Epic Entry Point Test](#part-2-epic-entry-point-test)
10. [Part 3: Epic E2E Execution Test (CRITICAL)](#part-3-epic-e2e-execution-test-critical)
11. [Part 4: Cross-Feature Integration Test (EPIC-SPECIFIC)](#part-4-cross-feature-integration-test-epic-specific)
12. [Pass/Fail Criteria](#passfail-criteria)
13. [Epic Issue Handling Protocol](#epic-issue-handling-protocol)
14. [🛑 MANDATORY CHECKPOINT 1](#-mandatory-checkpoint-1)
15. [Next Steps](#next-steps)
16. [Summary](#summary)
17. [Exit Criteria](#exit-criteria)

---


## Overview

**What is this guide?**
Epic-level smoke testing validates that ALL features work together as a cohesive system. Unlike feature-level testing (S7 (Testing & Review)), this tests cross-feature integration and epic-wide workflows. See `reference/smoke_testing_pattern.md` for universal patterns.

**When do you use this guide?**
- After ALL features have completed S8.P2 (Epic Testing Update)
- No pending bug fixes
- epic_smoke_test_plan.md has been evolved through Stages 1, 4, and 5e
- Ready to validate epic as a whole

**Key Outputs:**
- ✅ Part 1 PASSED: Epic-level import tests
- ✅ Part 2 PASSED: Epic-level entry point tests
- ✅ Part 3 PASSED: Epic E2E execution tests (data values verified)
- ✅ Part 4 PASSED: Cross-feature integration tests
- ✅ Ready for S9.P2 (Epic QC Validation Loop)

**Time Estimate:**
20-30 minutes for 3-feature epics, 30-60 minutes for 5+ feature epics

**Exit Condition:**
Epic Smoke Testing is complete when ALL 4 parts of epic_smoke_test_plan.md pass, all cross-feature integration scenarios work correctly, and data values are verified

---

## 🛑 Critical Rules (Epic-Specific)

**📖 See `reference/smoke_testing_pattern.md` for universal critical rules.**

**Epic-specific rules for S9:**

```text
┌─────────────────────────────────────────────────────────────┐
│ EPIC-SPECIFIC RULES - Add to EPIC_README Agent Status       │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ ALL features MUST complete S8.P2 (Epic Testing Update) before starting
   - Verify EVERY feature shows "S8.P2 (Epic Testing Update) complete" in EPIC_README.md
   - Do NOT start if any feature is incomplete

2. ⚠️ Use EVOLVED epic_smoke_test_plan.md (NOT original)
   - Plan evolved through S1 → S4 → S8.P2 updates
   - Reflects ACTUAL implementation (not initial assumptions)
   - Contains integration scenarios added during S8.P2 (Epic Testing Update)

3. ⚠️ Epic testing ≠ Feature testing
   - Feature testing (5c): Tests feature in isolation
   - Epic testing (6a): Tests ALL features working together
   - Focus: Cross-feature workflows, integration points

4. ⚠️ If smoke testing fails → Fix issues, re-run from Part 1
   - Do NOT proceed to QC validation loop with failing smoke tests
   - After fixing → Re-run smoke testing from Part 1
   - Do NOT skip any parts

5. ⚠️ Execute ALL 4 parts of epic_smoke_test_plan.md
   - Part 1: Epic-level import tests
   - Part 2: Epic-level entry point tests
   - Part 3: Epic end-to-end execution tests
   - Part 4: Cross-feature integration tests (EPIC-SPECIFIC)
```

**Universal rules (from pattern file):**
- All parts mandatory
- Verify DATA VALUES (not just structure)
- Use REAL data (not test fixtures)
- Re-run ALL parts if any fail
- See `reference/smoke_testing_pattern.md` for complete list

---

## Prerequisites Checklist

**Before starting Epic Smoke Testing (S9.P1), verify:**

**ALL features complete:**
- [ ] EVERY feature shows "S8.P2 (Epic Testing Update) complete" in EPIC_README.md Epic Progress Tracker
- [ ] All features show ✅ in S8.P2 (Epic Testing Update) column
- [ ] No features with "In progress" or "Not started" status

**No pending bug fixes:**
- [ ] No `bugfix_{priority}_{name}/` folders with incomplete status
- [ ] If bug fix folders exist, they're at S7 (Testing & Review) (complete)

**Epic smoke test plan evolved:**
- [ ] epic_smoke_test_plan.md shows "Last Updated" from RECENT S8.P2 (Epic Testing Update)
- [ ] Update History table shows ALL features contributed updates
- [ ] Test scenarios reflect ACTUAL implementation

**Original epic request available:**
- [ ] `{epic_name}.txt` file exists in feature-updates/ folder
- [ ] Contains user's original epic request

**EPIC_README.md ready:**
- [ ] Epic Progress Tracker shows all features at 5e
- [ ] Agent Status section exists

**If any prerequisite fails:**
- ❌ Do NOT start Epic Smoke Testing
- Complete missing prerequisites first
- Return to S9.P1 when all prerequisites met

---

## Workflow Overview

**📖 See `reference/smoke_testing_pattern.md` for universal workflow details.**

**Epic-specific workflow for S9:**

```text
┌─────────────────────────────────────────────────────────────┐
│          EPIC-LEVEL SMOKE TESTING (4 Parts)                 │
└─────────────────────────────────────────────────────────────┘

STEP 1: Pre-QC Verification
   ↓ Verify all features at S8.P2 (Epic Testing Update)
   ↓ Read evolved epic_smoke_test_plan.md
   ↓ Read original epic request
   ↓
   Proceed to STEP 2

STEP 2: Epic Smoke Testing (4 Parts)

Part 1: Epic Import Test
   ↓ Import all modules from ALL features
   ↓ Verify epic-wide imports work
   ↓
   If PASS → Part 2
   If FAIL → Fix, re-run Part 1

Part 2: Epic Entry Point Test
   ↓ Test epic-level workflows start correctly
   ↓ Verify all feature modes accessible
   ↓
   If PASS → Part 3
   If FAIL → Fix, re-run Parts 1 & 2

Part 3: Epic E2E Execution Test (CRITICAL)
   ↓ Execute epic workflows with REAL data
   ↓ Verify epic-level output DATA VALUES correct
   ↓
   If PASS → Part 4
   If FAIL → Fix, RE-RUN ALL PARTS

Part 4: Cross-Feature Integration Test (EPIC-SPECIFIC)
   ↓ Execute integration scenarios from test plan
   ↓ Verify features work together correctly
   ↓ Verify data flows between features
   ↓
   If PASS → Document, proceed to S9.P2
   If FAIL → Fix, RE-RUN ALL 4 PARTS
```

---

## STEP 1: Pre-QC Verification

**Objective:** Verify epic is ready for S9 validation.

### Step 1.1: Verify All Features Complete

**Read EPIC_README.md "Epic Progress Tracker" section:**

```markdown
## Epic Progress Tracker
| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 (Testing & Review) | S8.P1 (Cross-Feature Alignment) | S8.P2 (Epic Testing Update) |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_02 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| feature_03 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
```

**Verify:** EVERY feature shows ✅ in S8.P2 (Epic Testing Update) column.

**If ANY feature incomplete:** STOP S6, complete the incomplete feature first.

### Step 1.2: Verify No Pending Bug Fixes

Check epic folder for any `bugfix_{priority}_{name}/` folders. If found, verify they're complete (S7 (Testing & Review) done).

### Step 1.3: Read Evolved Epic Smoke Test Plan

**Read `epic_smoke_test_plan.md`:**
- Check "Last Updated" timestamp (should be recent from S8.P2 (Epic Testing Update))
- Review "Update History" table (all features should have entries)
- Identify all test scenarios to execute
- Note integration points between features

### Step 1.4: Read Original Epic Request

**Read `{epic_name}.txt`:**
- Review user's original goals
- Understand epic success criteria
- Keep in mind for Part 3 validation

---

## Part 1: Epic Import Test

**📖 See `reference/smoke_testing_pattern.md` for universal import test pattern.**

**Epic-specific implementation:**

Test that ALL feature modules can be imported together (no conflicts):

```bash
## Import key modules from each feature
python -c "from feature_01.MainClass import MainClass"
python -c "from feature_02.HelperClass import HelperClass"
python -c "from feature_03.ManagerClass import ManagerClass"

## Verify no import conflicts or circular dependencies
```

**Pass:** All epic modules import successfully
**Fail:** Any import errors → Fix, re-run Part 1

---

## Part 2: Epic Entry Point Test

**📖 See `reference/smoke_testing_pattern.md` for universal entry point test pattern.**

**Epic-specific implementation:**

Test that epic-level workflows can be initiated:

```bash
## Test help includes all feature modes
python run_script.py --help
## (verify all features' modes/options appear)

## Test each feature's mode is accessible
python run_script.py --mode feature_01_mode --help
python run_script.py --mode feature_02_mode --help
python run_script.py --mode feature_03_mode --help
```

**Pass:** All feature modes accessible, help complete
**Fail:** Missing modes, crashes → Fix, re-run Parts 1 & 2

---

## Part 3: Epic E2E Execution Test (CRITICAL)

**📖 See `reference/smoke_testing_pattern.md` for universal E2E test pattern and data validation examples.**

**Epic-specific implementation:**

Execute epic-level workflows from `epic_smoke_test_plan.md`:

### Step 1: Execute Each Test Scenario

From epic_smoke_test_plan.md, execute each scenario:

**Example scenario:**
```markdown
### Scenario 1: Complete Draft Workflow
1. Fetch player data (Feature 01)
2. Apply ratings (Feature 02)
3. Generate recommendations (Feature 03)
```

**Execute:**
```bash
## Step-by-step or combined workflow
python run_script.py --complete-draft-workflow --data-folder ./data
```

### Step 2: CRITICAL - Verify Epic Output DATA VALUES

**📖 See pattern file for data validation examples.**

**Epic-specific validation:**

```python
## Verify epic-level outputs have correct data
from pathlib import Path
import json

## Check final epic output (combines all features)
epic_output = Path("data/draft_recommendations_final.json")
assert epic_output.exists(), "Epic output file missing"

with open(epic_output) as f:
    data = json.load(f)

## Verify data from ALL features integrated correctly
assert len(data) > 0, "Epic output is empty"

## Verify Feature 01 data present (player info)
assert all('player_name' in p for p in data), "Missing player names (Feature 01)"

## Verify Feature 02 data present (ratings)
assert all('rating' in p for p in data), "Missing ratings (Feature 02)"

## Verify Feature 03 data present (recommendations)
assert all('draft_position' in p for p in data), "Missing positions (Feature 03)"

## Verify values are CORRECT (not placeholders)
assert data[0]['rating'] != 0.0, "Ratings are placeholder values"
assert data[0]['draft_position'] > 0, "Positions are invalid"

print("✅ Epic output integrates all features correctly")
```

**If validation fails:** Document issue, fix, RE-RUN ALL 4 PARTS

---

## Part 4: Cross-Feature Integration Test (EPIC-SPECIFIC)

**This part is UNIQUE to epic-level smoke testing.**

**Objective:** Verify features work together correctly.

### Step 1: Identify Integration Points

From `epic_smoke_test_plan.md`, identify cross-feature integration scenarios:

**Example integration points:**
```markdown
- Feature 01 → Feature 02: Player data passed to rating system
- Feature 02 → Feature 03: Ratings used in recommendations
- Feature 03 → Feature 01: Recommendations update player rankings
```

### Step 2: Execute Integration Scenarios

For EACH integration point, verify data flows correctly:

```python
## Integration Test: Feature 01 → Feature 02
from feature_01.PlayerDataManager import PlayerDataManager
from feature_02.RatingSystem import RatingSystem

## Get data from Feature 01
player_mgr = PlayerDataManager()
players = player_mgr.get_all_players()

## Pass to Feature 02
rating_sys = RatingSystem()
rated_players = rating_sys.apply_ratings(players)

## Verify integration works
assert len(rated_players) == len(players), "Data lost in integration"
assert all(hasattr(p, 'rating') for p in rated_players), "Ratings not applied"
assert rated_players[0].rating > 0, "Rating values invalid"

print("✅ Feature 01 → Feature 02 integration works")
```

### Step 3: Verify Error Propagation

Test that errors propagate correctly across feature boundaries:

```python
## Test error handling at integration point
try:
    invalid_data = None
    rating_sys.apply_ratings(invalid_data)
    assert False, "Should have raised error for invalid data"
except ValueError as e:
    assert "Invalid player data" in str(e), "Error message unclear"
    print("✅ Error propagation works correctly")
```

### Step 4: Verify Interface Compatibility

Ensure features use compatible interfaces:

```python
## Verify Feature 02 accepts Feature 01's output format
from feature_01.PlayerDataManager import Player
from feature_02.RatingSystem import RatingSystem

sample_player = Player(name="Test", position="QB")
rating_sys = RatingSystem()

## This should work without errors
result = rating_sys.rate_player(sample_player)
assert result is not None, "Interface mismatch between features"

print("✅ Interface compatibility verified")
```

**Pass Criteria:**
- All integration scenarios execute successfully
- Data flows correctly between features
- Error propagation works
- Interfaces are compatible

**Fail Criteria:**
- Integration point fails
- Data format mismatches
- Errors not propagated
- Interface incompatibilities

**If Part 4 fails:** Fix integration issues, RE-RUN ALL 4 PARTS from Part 1

---

## Pass/Fail Criteria

**📖 See `reference/smoke_testing_pattern.md` for universal pass criteria.**

**Epic-specific criteria:**

**✅ PASS if:**
- Part 1: All epic modules import successfully
- Part 2: All feature modes accessible
- Part 3: Epic workflows execute AND output data values verified correct
- Part 4: Cross-feature integration works correctly

**❌ FAIL if:**
- Part 1: Any import errors or conflicts
- Part 2: Missing modes, crashes
- Part 3: Workflow crashes OR output missing OR **data values incorrect**
- Part 4: Integration points fail OR data format mismatches

**If FAIL:**
1. Document failure in EPIC_README.md
2. Identify root cause (integration issue, interface mismatch, data flow problem)
3. Fix ALL issues found
4. RE-RUN ALL 4 PARTS from Part 1
5. Do NOT proceed to S9.P2 until all parts pass

---

## Epic Issue Handling Protocol

**If issues found during smoke testing:**

### Minor Issues (Fix Immediately)
- Naming inconsistencies
- Comment improvements
- Documentation gaps

**Fix immediately, re-run affected tests, continue**

### Critical Issues (Re-run Required)
- Integration point failures
- Data corruption across features
- Interface incompatibilities
- Epic workflow crashes

**Follow epic debugging protocol:**
1. Create `epic_name/debugging/ISSUES_CHECKLIST.md`
2. Enter debugging protocol (see `debugging/debugging_protocol.md`)
3. After ALL issues resolved → **Re-run smoke testing from Part 1**
4. Re-run all 4 parts of smoke testing

**Note:** Once smoke testing passes, S9.P2 uses validation loop (fix and continue). Restart from S9.P1 only required if user testing (S9.P3) finds bugs.

---

## 🛑 MANDATORY CHECKPOINT 1

**You have completed all 4 parts of Epic Smoke Testing**

⚠️ STOP - DO NOT PROCEED TO S9.P2 YET

**REQUIRED ACTIONS:**
1. [ ] Use Read tool to re-read "Critical Rules" section (top of this guide)
2. [ ] Use Read tool to re-read `reference/smoke_testing_pattern.md` (Common Mistakes section)
3. [ ] Verify data VALUES inspected for epic-level outputs (not just "file exists")
4. [ ] Verify cross-feature integration tested (Part 4) - actual data flow between features
5. [ ] Update EPIC_README.md Agent Status:
   - Current Guide: "stages/s9/s9_p2_epic_qc_rounds.md"
   - Current Step: "S9.P1 complete, ready to start S9.P2 Validation Loop"
   - Last Updated: [timestamp]
6. [ ] Output acknowledgment: "✅ CHECKPOINT 1 COMPLETE: Re-read Critical Rules and Pattern File, verified epic-level data values and integration"

**Why this checkpoint exists:**
- 95% of agents skip epic-level integration testing in Part 4
- Missing integration tests causes 80% of production failures
- 3 minutes of re-reading prevents epic-wide rework

**ONLY after completing ALL 6 actions above, proceed to Next Steps section**

---

## Next Steps

**If ALL 4 parts PASSED:**
- Document epic smoke test results in EPIC_README.md
- Update Agent Status: "Epic Smoke Testing COMPLETE"
- Proceed to **S9.P2: Epic QC Validation Loop** (12 dimensions, 3 consecutive clean rounds)

**If ANY part FAILED:**
- Fix ALL issues identified
- If critical issues → Follow epic debugging protocol
- RE-RUN ALL 4 PARTS from Part 1
- Do NOT proceed to S9.P2 until clean pass

---

## Summary

**Epic-Level Smoke Testing validates:**
- All feature modules work together (Part 1)
- Epic workflows are accessible (Part 2)
- Epic executes end-to-end with REAL data producing CORRECT values (Part 3)
- Features integrate correctly (Part 4)

**Key Differences from Feature-Level:**
- Tests ALL features TOGETHER (not in isolation)
- 4 parts (adds Part 4: Cross-Feature Integration)
- Uses EVOLVED test plan (updated through Stages 1, 4, S8.P2)
- Next: S9.P2 uses validation loop (12 dimensions, 3 consecutive clean rounds)

**Critical Success Factors:**
- Verify ALL features complete S8.P2 (Epic Testing Update) first
- Use evolved test plan (reflects actual implementation)
- Verify DATA VALUES (not just structure)
- Test cross-feature integration (Part 4)
- Re-run ALL parts if any fail

**📖 For universal patterns and detailed examples, see:**
`reference/smoke_testing_pattern.md`


## Exit Criteria

**Epic Smoke Testing (S9.P1) is complete when ALL of these are true:**

- [ ] All steps in this phase complete as specified
- [ ] Agent Status updated with phase completion
- [ ] Ready to proceed to next phase

**If any criterion unchecked:** Complete missing items before proceeding

---
---

**END OF S9.P1 GUIDE**
