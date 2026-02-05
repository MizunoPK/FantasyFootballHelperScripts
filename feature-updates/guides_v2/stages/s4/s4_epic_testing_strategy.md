# S4: Epic Testing Strategy Guide

🚨 **MANDATORY READING PROTOCOL**

**Before starting this guide:**
1. Use Read tool to load THIS ENTIRE GUIDE
2. Acknowledge critical requirements (see "Critical Rules" section below)
3. Verify prerequisites (see "Prerequisites Checklist" section below)
4. Update epic EPIC_README.md Agent Status with guide name + timestamp

**DO NOT proceed without reading this guide.**

**After session compaction:**
- Check epic EPIC_README.md Agent Status for current phase
- READ THIS GUIDE again (full guide, not summary)
- Continue from "Next Action" in Agent Status

---

## Overview

**What is this guide?**
Epic Testing Strategy is where you update the epic_smoke_test_plan.md with concrete test scenarios based on the actual feature specs, replacing the S1 placeholder assumptions with specific integration points and measurable success criteria.

**When do you use this guide?**
- S3 complete (user has approved complete plan)
- All feature specs are finalized
- Ready to define epic-wide testing strategy

**Key Outputs:**
- ✅ epic_smoke_test_plan.md updated from placeholder to concrete scenarios
- ✅ Integration points between features identified
- ✅ Measurable success criteria defined
- ✅ Test plan marked as "S4 version - will update in S8.P2 (Epic Testing Update)"
- ✅ Ready for S5 (Feature Implementation)

**Time Estimate:**
30-45 minutes

**Exit Condition:**
S4 is complete when epic_smoke_test_plan.md contains specific test scenarios (not vague categories), integration points are documented, and the update is logged with rationale for changes from S1

**FOR DEPENDENCY GROUP EPICS:**

S4 runs ONCE PER ROUND (not just once at end):

- **Round 1 S4:** Update test plan with Group 1 features (+ validation loop)
- **Round 2 S4:** Update test plan with Group 2 features (+ validation loop)
- **Round 3 S4:** Update test plan with Group 3 features (+ validation loop)

**Test plan evolves incrementally** - Each round adds new features and validates complete plan.

---

## Critical Rules

```text
┌─────────────────────────────────────────────────────────────┐
│ CRITICAL RULES - These MUST be copied to README Agent Status │
└─────────────────────────────────────────────────────────────┘

1. ⚠️ S3 (user approval) MUST be complete before S4
   - Cannot update testing strategy without approved plan

2. ⚠️ epic_smoke_test_plan.md is MAJOR UPDATE (not minor tweak)
   - S1 version was placeholder (assumptions)
   - S4 version is concrete (based on actual specs)
   - Replace high-level categories with specific scenarios

3. ⚠️ Identify ALL integration points between features
   - Where features interact
   - Data passed between features
   - Shared resources (files, config, classes)

4. ⚠️ Define MEASURABLE success criteria
   - Not "feature works" (too vague)
   - Yes "all 4 features create expected output files" (specific)

5. ⚠️ Test plan will update AGAIN in S8.P2 (Epic Testing Update)
   - S4: Based on SPECS (planned implementation)
   - S8.P2 (Epic Testing Update): Based on ACTUAL CODE (real implementation)
   - Mark clearly as "S4 version - will update in S8.P2 (Epic Testing Update)"

6. ⚠️ Include both feature-level AND epic-level tests
   - Feature tests: Individual feature works
   - Epic tests: Features work TOGETHER

7. ⚠️ Mark update in Update Log
   - Document what changed from S1 to S4
   - Why changes were made

8. ⚠️ Update epic EPIC_README.md Epic Completion Checklist
   - Mark S4 items complete
```markdown

---

## Prerequisites Checklist

**Verify BEFORE starting S4:**

□ S3 (Cross-Feature Sanity Check) complete
□ User approved implementation plan (documented in epic EPIC_README.md)
□ All feature specs complete and conflict-free
□ epic_smoke_test_plan.md exists (created in S1)
□ Have read all feature specs to understand:
  - What each feature does
  - How features interact
  - What outputs features create

**If any prerequisite fails:**
- ❌ STOP - Do NOT proceed with S4
- Complete missing prerequisites
- Document blocker in Agent Status

---

## Workflow Overview

```text
┌──────────────────────────────────────────────────────────────┐
│                    STAGE 4 WORKFLOW                          │
└──────────────────────────────────────────────────────────────┘

Step 1: Review Initial Test Plan
   ├─ Read epic_smoke_test_plan.md (S1 version)
   ├─ Identify placeholders and assumptions
   └─ Note what needs updating

Step 2: Identify Integration Points
   ├─ Review all feature specs
   ├─ Map data flows between features
   ├─ Identify shared resources
   └─ Document integration points

Step 3: Define Epic Success Criteria
   ├─ Based on original epic request
   ├─ Based on approved feature plan
   ├─ Make criteria MEASURABLE
   └─ Document what "success" looks like

Step 4: Create Specific Test Scenarios
   ├─ Convert high-level categories to concrete tests
   ├─ Add specific commands to run
   ├─ Define expected outputs
   └─ Document failure indicators

Step 5: Update epic_smoke_test_plan.md
   ├─ Replace placeholder content
   ├─ Add all new sections
   ├─ Mark as "S4 version"
   └─ Update Update Log

Step 6: Mark S4 Complete
   ├─ Update epic EPIC_README.md
   └─ Transition to S5
```markdown

---

## Step 1: Review Initial Test Plan

### Step 1.1: Read Current epic_smoke_test_plan.md

Read the file created in S1.

**It should have:**
- Version marker: "INITIAL (S1)"
- Epic Success Criteria (high-level, vague)
- Specific Commands/Scenarios (placeholder / TBD)
- High-Level Test Categories (general ideas)
- Update Log (one entry from S1)

**Example from S1:**

```markdown
## Epic Success Criteria (INITIAL - WILL REFINE)

**The epic is successful if:**
1. Draft helper uses new data sources (vague)
2. Recommendations are more accurate (not measurable)
3. No errors occur (too broad)

## Specific Commands/Scenarios (PLACEHOLDER)

### Test 1: Run Draft Helper
```bash
# Command TBD after S2 deep dives
```markdown
**Expected result:** TBD
```markdown

### Step 1.2: Identify What Needs Updating

**Questions to answer:**
- What are the ACTUAL outputs from features? (now we know from specs)
- What are the ACTUAL integration points? (discovered in S3)
- What specific commands can we run? (specs define entry points)
- What measurable criteria define success? (based on feature objectives)

**Mark sections needing major updates:**
- [ ] Epic Success Criteria → Make specific and measurable
- [ ] Specific Commands → Add actual commands from specs
- [ ] Integration Points → Add from S3 findings
- [ ] Test Categories → Convert to concrete scenarios

---

## Step 2: Identify Integration Points

### Step 2.1: Review Feature Dependencies

From S3 sanity check and feature specs:

```bash
Feature 1 (ADP Integration)
  ├─ Creates: data/rankings/adp.csv
  ├─ Modifies: FantasyPlayer (adds adp_value, adp_multiplier)
  └─ Used by: Feature 4

Feature 2 (Injury Assessment)
  ├─ Creates: data/player_info/injury_reports.csv
  ├─ Modifies: FantasyPlayer (adds injury_status, injury_multiplier)
  └─ Used by: Feature 4

Feature 3 (Schedule Analysis)
  ├─ Creates: data/rankings/schedule_strength.csv
  ├─ Modifies: FantasyPlayer (adds schedule_strength)
  └─ Used by: Feature 4

Feature 4 (Recommendation Engine)
  ├─ Reads: FantasyPlayer fields from Features 1, 2, 3
  ├─ Calculates: total_score using ALL multipliers
  └─ Outputs: Updated recommendations
```markdown

### Step 2.2: Map Data Flows

**Create integration point map:**

```markdown
## Integration Points Identified

### Integration Point 1: FantasyPlayer Data Model
**Features Involved:** All features (1, 2, 3, 4)
**Type:** Shared data structure
**Flow:**
- Feature 1 adds: adp_value, adp_multiplier fields
- Feature 2 adds: injury_status, injury_multiplier fields
- Feature 3 adds: schedule_strength field
- Feature 4 reads: ALL above fields

**Test Need:** Verify all fields present after all features run

---

### Integration Point 2: Scoring Algorithm
**Features Involved:** Features 1, 2, 3, 4
**Type:** Computational dependency
**Flow:**
- Feature 1: score *= adp_multiplier
- Feature 2: score *= injury_multiplier
- Feature 3: score *= schedule_strength
- Feature 4: Combines all multipliers

**Test Need:** Verify final score includes all multipliers

---

### Integration Point 3: Data File Locations
**Features Involved:** Features 1, 2, 3
**Type:** File system interaction
**Flow:**
- Feature 1 creates: data/rankings/adp.csv
- Feature 2 creates: data/player_info/injury_reports.csv
- Feature 3 creates: data/rankings/schedule_strength.csv
- All files must exist for Feature 4 to work

**Test Need:** Verify all data files created in correct locations
```markdown

---

## Step 3: Define Epic Success Criteria

### Step 3.1: Review Epic Request

Re-read original epic request (`{epic_name}_notes.txt`):

**Example:**
```text
Goal: Improve draft helper with more data sources to make better recommendations
```markdown

### Step 3.2: Review Approved Feature Plan

From S3:
- 4 features approved
- Feature 4 is integration point
- Dependencies mapped

### Step 3.3: Create MEASURABLE Success Criteria

**Convert vague goals to measurable criteria:**

**BEFORE (S1):**
```text
1. Draft helper uses new data sources (vague)
2. Recommendations are more accurate (not measurable)
3. No errors occur (too broad)
```markdown

**AFTER (S4):**
```markdown
## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: All Data Files Created
✅ **MEASURABLE:** Verify these files exist:
- `data/rankings/adp.csv` (from Feature 1)
- `data/player_info/injury_reports.csv` (from Feature 2)
- `data/rankings/schedule_strength.csv` (from Feature 3)

**Verification:** `ls data/rankings/ data/player_info/` shows all 3 files

---

### Criterion 2: All Multipliers Applied
✅ **MEASURABLE:** Run draft helper and verify player scores include:
- ADP multiplier contribution (Feature 1)
- Injury multiplier contribution (Feature 2)
- Schedule strength contribution (Feature 3)

**Verification:**
1. Load player data
2. Check FantasyPlayer object has all fields: adp_multiplier, injury_multiplier, schedule_strength
3. Verify total_score calculation includes all three

---

### Criterion 3: Recommendations Updated
✅ **MEASURABLE:** Draft recommendations list shows:
- At least 10 players ranked
- Each player has total_score > 0
- Scores reflect new data sources (compare before/after)

**Verification:** Run draft helper in add_to_roster_mode, verify recommendation output

---

### Criterion 4: No Errors in E2E Workflow
✅ **MEASURABLE:** Run complete workflow without errors:
1. Load all data files (Features 1, 2, 3)
2. Calculate scores (Feature 4)
3. Generate recommendations
4. Exit code 0 (success)

**Verification:** `python run_league_helper.py --mode draft` exits with code 0

---

### Criterion 5: Integration Test Passes
✅ **MEASURABLE:** Integration test verifies:
- All features loaded successfully
- All multipliers present in final score
- Score differs from baseline (data sources had impact)

**Verification:** `python tests/integration/test_draft_helper_integration.py` passes
```markdown

---

## Step 4: Create Specific Test Scenarios

### Step 4.1: Convert High-Level Categories to Concrete Tests

**BEFORE (S1):**
```markdown
## High-Level Test Categories

### Category 1: Cross-Feature Integration
**What to test:** {General idea of integration points}
**Specific scenarios:** TBD in S4
```markdown

**AFTER (S4):**
```markdown
## Specific Test Scenarios

### Test Scenario 1: Data File Creation (Features 1, 2, 3)

**Purpose:** Verify all features create their data files in correct locations

**Steps:**
1. Clear data directories: `rm -rf data/rankings/* data/player_info/*`
2. Run Feature 1: Load ADP data
3. Run Feature 2: Load injury data
4. Run Feature 3: Load schedule data

**Expected Results:**
✅ `data/rankings/adp.csv` exists and contains >100 rows
✅ `data/player_info/injury_reports.csv` exists and contains >50 rows
✅ `data/rankings/schedule_strength.csv` exists and contains >30 rows

**Failure Indicators:**
❌ Any file missing → Feature failed to create output
❌ File exists but empty → Feature ran but no data loaded
❌ File in wrong location → Feature not following spec

**Command to verify:**
```bash
test -f data/rankings/adp.csv && echo "Feature 1 OK" || echo "Feature 1 FAILED"
test -f data/player_info/injury_reports.csv && echo "Feature 2 OK" || echo "Feature 2 FAILED"
test -f data/rankings/schedule_strength.csv && echo "Feature 3 OK" || echo "Feature 3 FAILED"
```markdown

---

### Test Scenario 2: FantasyPlayer Field Integration (All Features)

**Purpose:** Verify all features add their fields to FantasyPlayer model

**Steps:**
1. Run league helper with all features enabled
2. Load player data
3. Inspect first player object

**Expected Results:**
✅ Player object has field: `adp_value` (Feature 1)
✅ Player object has field: `adp_multiplier` (Feature 1)
✅ Player object has field: `injury_status` (Feature 2)
✅ Player object has field: `injury_multiplier` (Feature 2)
✅ Player object has field: `schedule_strength` (Feature 3)

**Failure Indicators:**
❌ Missing field → Feature didn't modify FantasyPlayer
❌ Field exists but None → Feature didn't populate data

**Command to verify:**
```python
# In Python REPL
from league_helper.util.PlayerManager import PlayerManager
pm = PlayerManager(data_folder="data/")
players = pm.load_players()
p = players[0]
print(f"ADP: {p.adp_value}, {p.adp_multiplier}")
print(f"Injury: {p.injury_status}, {p.injury_multiplier}")
print(f"Schedule: {p.schedule_strength}")
# All should print values (not None)
```markdown

---

### Test Scenario 3: Multiplier Application (Feature 4)

**Purpose:** Verify Feature 4 includes ALL multipliers in score calculation

**Steps:**
1. Create test player with known multipliers:
   - adp_multiplier = 1.2
   - injury_multiplier = 0.9
   - schedule_strength = 1.1
   - base_score = 100
2. Calculate total_score
3. Verify result

**Expected Results:**
✅ total_score = 100 * 1.2 * 0.9 * 1.1 = 118.8
✅ Calculation includes ALL three new multipliers

**Failure Indicators:**
❌ total_score = 100 → No multipliers applied
❌ total_score = 108 → Missing one multiplier
❌ total_score != 118.8 → Incorrect calculation

**Command to verify:**
```python
# Unit test
def test_all_multipliers_applied():
    player = FantasyPlayer(...)
    player.projected_points = 100
    player.adp_multiplier = 1.2
    player.injury_multiplier = 0.9
    player.schedule_strength = 1.1

    score = player.calculate_total_score()

    assert abs(score - 118.8) < 0.01, f"Expected 118.8, got {score}"
```markdown

---

### Test Scenario 4: End-to-End Workflow

**Purpose:** Verify complete draft helper workflow with all features

**Steps:**
1. Start league helper: `python run_league_helper.py --mode draft`
2. Select player position (e.g., "QB")
3. View recommendations
4. Exit

**Expected Results:**
✅ Program starts without errors
✅ Recommendations displayed (10+ players)
✅ Each player has total_score > 0
✅ Program exits cleanly (exit code 0)

**Failure Indicators:**
❌ Import error → Module integration issue
❌ No recommendations → Scoring calculation failed
❌ Crash during execution → Runtime error in integration

**Command to verify:**
```bash
python run_league_helper.py --mode draft <<EOF
QB
exit
EOF
echo "Exit code: $?"  # Should be 0
```text
```bash

### Step 4.2: Add Integration-Specific Tests

Based on integration points from Step 2:

```markdown
### Test Scenario 5: Data File Integration (Feature 4 depends on 1, 2, 3)

**Purpose:** Verify Feature 4 can load data from Features 1, 2, 3

**Setup:**
- Ensure Features 1, 2, 3 have created their data files

**Steps:**
1. Run Feature 4 (recommendation engine)
2. Verify it loads all data sources
3. Verify no file-not-found errors

**Expected Results:**
✅ Feature 4 successfully loads data/rankings/adp.csv
✅ Feature 4 successfully loads data/player_info/injury_reports.csv
✅ Feature 4 successfully loads data/rankings/schedule_strength.csv
✅ No error messages in logs

**Failure Indicators:**
❌ FileNotFoundError → Feature 4 can't find data file
❌ Parse error → Data file in wrong format
❌ Empty data → Data file exists but no content

---

### Test Scenario 6: Scoring Baseline Comparison

**Purpose:** Verify new features CHANGE scores (not just add zero)

**Setup:**
- Get baseline score (without Features 1, 2, 3 active)
- Run with Features 1, 2, 3 active

**Steps:**
1. Load player "Patrick Mahomes"
2. Calculate score WITHOUT new features: baseline_score
3. Calculate score WITH new features: new_score
4. Compare

**Expected Results:**
✅ new_score != baseline_score (features had impact)
✅ new_score differs by at least 5% (material impact)

**Failure Indicators:**
❌ new_score == baseline_score → Features not applied
❌ new_score < 0 → Calculation error
```markdown

---

## Step 5: Update epic_smoke_test_plan.md

### Step 5.1: Update File Header

```markdown
# Epic Smoke Test Plan: {epic_name}

**Purpose:** Define how to validate the complete epic end-to-end

**⚠️ VERSION: STAGE 4 (Updated after deep dives)**
- Created: {S1 date}
- Last Updated: {S4 date}
- Based on: Feature specs from Stages 2-3, approved plan
- Quality: CONCRETE - Specific tests based on actual feature designs
- Next Update: S8.P2 (Epic Testing Update) (after each feature implementation - will add more tests)

**Update History:**
- S1: Initial placeholder (assumptions only)
- S4: **MAJOR UPDATE** - Added specific tests, integration points, measurable criteria
- S8.P2 (Epic Testing Update): (Pending) Will update after each feature implementation
```markdown

### Step 5.2: Replace Epic Success Criteria

Replace vague criteria with measurable ones from Step 3:

```markdown
## Epic Success Criteria

{Paste measurable criteria from Step 3.3}
```markdown

### Step 5.3: Replace Specific Commands Section

Replace TBD placeholders with concrete tests from Step 4:

```markdown
## Specific Test Scenarios

**These tests MUST be run for epic-level validation:**

{Paste Test Scenario 1 from Step 4.1}

{Paste Test Scenario 2 from Step 4.1}

{Paste Test Scenario 3 from Step 4.1}

{Paste Test Scenario 4 from Step 4.1}

{Paste Test Scenario 5 from Step 4.2}

{Paste Test Scenario 6 from Step 4.2}
```markdown

### Step 5.4: Update High-Level Test Categories

Keep categories but add specific guidance:

```markdown
## High-Level Test Categories

**Agent will create additional scenarios for these categories during S8.P2 (Epic Testing Update):**

### Category 1: Cross-Feature Integration
**What to test:** Features working together correctly
**Known integration points:**
- FantasyPlayer model (all features modify)
- Scoring algorithm (all features contribute)
- Data file dependencies (Feature 4 needs 1, 2, 3)

**S8.P2 (Epic Testing Update) will add:** Specific tests after seeing actual implementation

---

### Category 2: Error Handling
**What to test:** Graceful degradation when data missing or invalid
**Known error scenarios:**
- Missing data files (Features 1, 2, 3)
- Invalid data formats
- Player not found in data source

**S8.P2 (Epic Testing Update) will add:** Specific error scenarios discovered during implementation

---

### Category 3: Performance
**What to test:** Epic doesn't slow down significantly
**Known performance concerns:**
- Loading 3 new data files
- Applying 3 additional multipliers

**S8.P2 (Epic Testing Update) will add:** Performance benchmarks after implementation
```markdown

### Step 5.5: Update Update Log

```markdown
## Update Log

| Date | Stage | What Changed | Why |
|------|-------|--------------|-----|
| {S1 date} | S1 | Initial plan created | Epic planning - assumptions only |
| {S4 date} | S4 | **MAJOR UPDATE** | Based on feature specs (Stages 2-3) |

**S4 changes:**
- Added 6 specific test scenarios (was TBD)
- Replaced vague success criteria with 5 measurable criteria
- Identified 6 integration points between features
- Added concrete commands and expected outputs
- Documented failure indicators for each test

**Current version is informed by:**
- S1: Initial assumptions from epic request
- **S4: Feature specs and approved implementation plan** ← YOU ARE HERE
- S8.P2 (Epic Testing Update): (Pending) Will update after each feature implementation

**Next update:** S8.P2 (Epic Testing Update) after each feature completes (will add implementation-specific tests)
```markdown

---

## Step 6: S4 Validation Loop (MANDATORY)

**Similar to S3 Final Validation Loop, but for epic test plan.**

**Goal:** Achieve 2-3 consecutive clean loops with ZERO issues in test plan

**Loop Process:**
1. Update epic_smoke_test_plan.md with new features (completed in Step 5)
2. Review test plan skeptically from chosen perspective:
   - Are all new features covered with specific test scenarios?
   - Do integration points include new dependencies?
   - Are success criteria updated for new components?
   - Is test execution order still logical?
   - Are edge cases covered?
3. Find issues (missing tests, inconsistent validation, unclear scenarios)
4. Resolve ALL issues (same zero-tolerance standard as S3)
5. Loop again with fresh perspective
6. **Exit condition:** 2-3 consecutive clean loops (ZERO issues found)

**Validation Perspectives to Use:**
1. **Test Coverage Reviewer** (Loop 1): Every feature has specific test scenarios
2. **Integration Validator** (Loop 2): All cross-feature integration points tested
3. **User Acceptance Tester** (Loop 3): Success criteria clear and measurable

**Why this matters:**
- Epic test plan is critical for S9 validation
- One-pass updates miss edge cases and gaps
- Skeptical validation catches missing test coverage
- Quality standard: Same rigor as S3 (zero tolerance for issues)

**Time Investment:**
- 2-3 loops: ~15-30 minutes total
- Prevents S9 rework: Saves 1-2 hours

**Documentation:**
Create validation log in epic_smoke_test_plan.md Update Log:
- Loop 1: [perspective] - [N issues found] - [resolutions]
- Loop 2: [perspective] - [N issues found] - [resolutions]
- Loop 3: [perspective] - 0 issues found ✅
- Exit: 2 consecutive clean loops achieved

**Historical context:** KAI-7 added S4 validation loop requirement after discovering one-pass updates missed integration points and test coverage gaps.

---

## Step 7: Mark S4 Complete

### Step 7.1: Update epic EPIC_README.md

**Epic Completion Checklist:**

```markdown
**S4 - Epic Testing Strategy:**
- [x] epic_smoke_test_plan.md updated
- [x] Integration points identified (6 integration points)
- [x] Epic success criteria defined (5 measurable criteria)
- [ ] 🚨 Gate 4.5: User approval of test plan (MANDATORY - must complete before S5)
```markdown

**Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** USER_APPROVAL
**Current Step:** Waiting for Gate 4.5 (Epic Test Plan Approval)
**Current Guide:** stages/s4/s4_epic_testing_strategy.md
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** S4 updates complete, awaiting user approval of test plan
**Next Action:** Present epic_smoke_test_plan.md to user for approval (Gate 4.5)
**Blockers:** None

**Testing Strategy:** epic_smoke_test_plan.md updated with 6 test scenarios, 5 success criteria
```markdown

### Step 7.2: Present Test Plan to User (🚨 GATE 4.5 - MANDATORY)

**🚨 CRITICAL:** You MUST get user approval of epic_smoke_test_plan.md before proceeding to S5.

**Why this gate exists:**
- Agent needs to know EXACTLY how to test work BEFORE creating implementation plans
- User can adjust test strategy early (cheap to change at S4 vs expensive at S5 Round 3)
- Test strategy should guide implementation planning (not vice versa)
- Addresses guide-updates.txt #10: "Have the testing plan be presented to the user and confirmed for each feature and the epic as a whole. Do this EARLY so that the agent knows how to test the work itself."

**Present to user:**

```markdown
🚨 **Gate 4.5: Epic Test Plan Approval Required**

I've updated the epic testing strategy in `epic_smoke_test_plan.md` based on the feature specs from Stages 2-3.

**Summary of epic_smoke_test_plan.md:**
- **Success Criteria:** {N} measurable criteria defined
- **Test Scenarios:** {N} specific test scenarios identified
- **Integration Points:** {N} cross-feature integration points documented
- **Data Quality Checks:** Verify VALUES (not just structure)
- **Concrete Commands:** Specific commands and expected outputs documented

**Key test scenarios include:**
1. {Scenario 1 summary}
2. {Scenario 2 summary}
3. {Scenario 3 summary}
...

**Why approval is needed now:**
- I need to know EXACTLY how to test this work BEFORE creating implementation plans (S5)
- Test requirements will guide how I structure implementation tasks and test strategy
- Changes to test plan are cheap now, expensive after 22 verification iterations

**Please review `epic_smoke_test_plan.md` and:**
- ✅ Approve if test strategy looks correct
- ❌ Request changes if test strategy needs adjustment

**Questions to consider:**
- Do the success criteria measure what matters to you?
- Are the test scenarios comprehensive enough?
- Are there additional integration points I should test?
- Do the data quality checks verify the right values?

**I cannot proceed to S5 (Implementation Planning) without your approval.**
```bash

**Wait for user response.**

**If user approves:**
- Mark Gate 4.5 as ✅ PASSED in EPIC_README.md
- Add timestamp to User Approval section in epic_smoke_test_plan.md
- Proceed to Step 6.3

**If user requests changes:**
- Revise epic_smoke_test_plan.md based on feedback
- Re-present for approval
- Repeat until user approves

**Evidence of passing Gate 4.5:**
- User says "approved" or "looks good" or equivalent
- Gate 4.5 checkbox marked ✅ in EPIC_README.md
- User Approval section in epic_smoke_test_plan.md completed with timestamp

### Step 6.3: Announce Transition (After Gate 4.5 Passes)

```markdown
✅ **S4 (Epic Testing Strategy) Complete**

**epic_smoke_test_plan.md updated and approved:**
- Added 5 measurable success criteria
- Created 6 specific test scenarios
- Identified 6 integration points
- Documented concrete commands and expected outputs
- ✅ User approved test plan (Gate 4.5 PASSED)

**Changes from S1:**
- Replaced placeholder "TBD" with actual test commands
- Converted vague criteria to measurable criteria
- Added integration tests between features

**Test plan evolution:**
- S1: Assumptions (no implementation knowledge)
- S4: Concrete (based on feature specs) ← CURRENT (USER APPROVED)
- S8.P2 (Epic Testing Update): Will update after EACH feature implementation

**Next: S5 (Feature Implementation)**

Now that I know EXACTLY how to test this work (user-approved test plan), I'll transition to S5 to begin implementation planning for the first feature.

Following `stages/s5/s5_p1_planning_round1.md` (Round 1) to create comprehensive implementation plan with 22 verification iterations across 3 rounds.
```markdown

**Update EPIC_README.md Agent Status:**

```markdown
## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** IMPLEMENTATION
**Current Step:** Ready to begin S5 (Feature Implementation)
**Current Guide:** stages/s5/s5_p1_planning_round1.md
**Guide Last Read:** NOT YET (will read when starting S5 - Round 1)

**Progress:** S4 complete, testing strategy approved by user (Gate 4.5 ✅)
**Next Action:** Begin S5 (Implementation Planning) for first feature
**Blockers:** None

**Testing Strategy:** epic_smoke_test_plan.md approved with 6 test scenarios, 5 success criteria
```markdown

---

## Exit Criteria

**S4 is complete when ALL of these are true:**

□ epic_smoke_test_plan.md updated with:
  - Version marked "STAGE 4" (not "INITIAL")
  - Epic Success Criteria section: 3-5 MEASURABLE criteria
  - Specific Test Scenarios section: 4-6 concrete tests with commands
  - High-Level Test Categories: Guidance for S8.P2 (Epic Testing Update) updates
  - Update Log: S4 entry documenting changes
□ Integration points identified and documented:
  - Where features interact
  - Data flows between features
  - Shared resources
□ All test scenarios have:
  - Purpose statement
  - Specific steps to execute
  - Expected results (measurable)
  - Failure indicators (what errors mean)
  - Commands or code to verify
□ Success criteria are MEASURABLE:
  - Not "feature works"
  - Yes "file exists with >100 rows"
□ Epic EPIC_README.md updated:
  - Epic Completion Checklist: S4 items checked
  - Agent Status: Phase = IMPLEMENTATION, ready for S5

**If any item unchecked:**
- ❌ S4 is NOT complete
- ❌ Do NOT proceed to S5
- Complete missing items first

---

## Common Mistakes to Avoid

```text
┌────────────────────────────────────────────────────────────┐
│ "If You're Thinking This, STOP" - Anti-Pattern Detection  │
└────────────────────────────────────────────────────────────┘

❌ "S1 test plan looks good enough"
   ✅ STOP - S1 was placeholder, S4 needs major update

❌ "I'll add general tests like 'verify features work'"
   ✅ STOP - Tests must be SPECIFIC and MEASURABLE

❌ "I'll skip integration point mapping, seems obvious"
   ✅ STOP - Must explicitly document where features interact

❌ "Test commands can be TBD, we'll figure it out in S5"
   ✅ STOP - S4 should have actual commands from specs

❌ "Success criteria: 'Epic achieves goals'"
   ✅ STOP - Too vague, must be measurable (files exist, tests pass, etc.)

❌ "I'll just list tests, don't need expected results"
   ✅ STOP - Each test needs expected results and failure indicators

❌ "Let me start implementing features"
   ✅ STOP - S5 (TODO creation) comes BEFORE implementation

❌ "This test plan is final, won't change"
   ✅ STOP - Plan will update in S8.P2 (Epic Testing Update) after each feature
```markdown

---

## Real-World Example

**Epic:** Improve Draft Helper

**S1 Plan (Placeholder):**
```bash
Success Criteria:
1. Draft helper improved (vague)
2. More data sources used (not measurable)

Specific Tests: TBD
```markdown

**S4 Plan (After deep dives):**
```text
Success Criteria:
1. ✅ All 3 data files exist: adp.csv, injury_reports.csv, schedule_strength.csv
2. ✅ FantasyPlayer has 5 new fields (3 values + 2 multipliers)
3. ✅ calculate_total_score() includes all 3 new multipliers
4. ✅ Draft recommendations show >10 players with score >0
5. ✅ Integration test passes: test_draft_helper_integration.py

Specific Tests:
Test 1: Verify data files created
  Command: ls data/rankings/ data/player_info/
  Expected: 3 files present

Test 2: Verify FantasyPlayer fields
  Command: Python REPL inspection
  Expected: All fields present and populated

Test 3: Verify multiplier application
  Command: Unit test with known values
  Expected: score = base * 1.2 * 0.9 * 1.1

Test 4: E2E workflow
  Command: python run_league_helper.py --mode draft
  Expected: Recommendations displayed, exit code 0

Test 5: Integration test
  Command: python tests/integration/test_draft_helper_integration.py
  Expected: All assertions pass

Test 6: Baseline comparison
  Command: Compare scores before/after features
  Expected: Scores differ by >5%
```

---

## README Agent Status Update Requirements

**Update epic EPIC_README.md Agent Status at these points:**

1. ⚡ After reviewing initial test plan (Step 1)
2. ⚡ After identifying integration points (Step 2)
3. ⚡ After defining success criteria (Step 3)
4. ⚡ After creating test scenarios (Step 4)
5. ⚡ After updating epic_smoke_test_plan.md (Step 5)
6. ⚡ After marking S4 complete (Step 6)

---

## Prerequisites for S5

**Before transitioning to S5, verify:**

□ S4 completion criteria ALL met
□ epic_smoke_test_plan.md shows "STAGE 4" version (not "INITIAL")
□ Test plan has 4-6 specific test scenarios with commands
□ Success criteria are measurable (not vague)
□ Epic EPIC_README.md shows:
  - Epic Completion Checklist: S4 items checked
  - Agent Status: Phase = IMPLEMENTATION
□ Integration points documented

**If any prerequisite fails:**
- ❌ Do NOT transition to S5
- Complete missing prerequisites

---

## Next Stage

**After completing S4:**

📖 **READ:** `stages/s5/s5_p1_planning_round1.md` (start with Round 1)
🎯 **GOAL:** Create comprehensive TODO for first feature (22 verification iterations across 3 rounds)
⏱️ **ESTIMATE:** 2-3 hours per feature (split across 3 rounds)

**S5 will:**
- Execute 24 mandatory verification iterations
- Create detailed TODO with acceptance criteria for every task
- Verify all interfaces against actual source code
- Ensure implementation readiness before coding

**Remember:** Use the phase transition prompt from `prompts_reference_v2.md` when starting S5.

---

*End of stages/s4/s4_epic_testing_strategy.md*
