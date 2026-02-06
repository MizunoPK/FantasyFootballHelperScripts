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

## Table of Contents

1. [Overview](#overview)
2. [Critical Rules](#critical-rules)
3. [Prerequisites Checklist](#prerequisites-checklist)
4. [Workflow Overview](#workflow-overview)
5. [Step 1: Review Initial Test Plan](#step-1-review-initial-test-plan)
6. [Epic Success Criteria (INITIAL - WILL REFINE)](#epic-success-criteria-initial---will-refine)
7. [Specific Commands/Scenarios (PLACEHOLDER)](#specific-commandsscenarios-placeholder)
8. [Step 2: Identify Integration Points](#step-2-identify-integration-points)
9. [Integration Points Identified](#integration-points-identified)
10. [Step 3: Define Epic Success Criteria](#step-3-define-epic-success-criteria)
11. [Epic Success Criteria](#epic-success-criteria)
12. [Step 4: Create Specific Test Scenarios](#step-4-create-specific-test-scenarios)
13. [Step 5: Update epic_smoke_test_plan.md](#step-5-update-epic_smoke_test_planmd)
14. [Epic Success Criteria](#epic-success-criteria-1)
15. [Specific Test Scenarios](#specific-test-scenarios)
16. [High-Level Test Categories](#high-level-test-categories)
17. [Update Log](#update-log)
18. [Step 6: S4 Validation Loop (MANDATORY)](#step-6-s4-validation-loop-mandatory)
19. [Step 7: Mark S4 Complete and Request Gate 4.5 Approval](#step-7-mark-s4-complete-and-request-gate-45-approval)
20. [Epic Test Plan Ready for Approval](#epic-test-plan-ready-for-approval)

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
```

---

## Prerequisites Checklist

**Verify BEFORE starting S4:**

□ S3 (Cross-Feature Sanity Check) complete with user approval (Gate 4.5 passed)
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
```

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
```
## Command TBD after S2 deep dives
```markdown
**Expected result:** TBD
```

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
```

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
```

---

## Step 3: Define Epic Success Criteria

### Step 3.1: Review Epic Request

Re-read original epic request (`{epic_name}_notes.txt`):

**Example:**
```text
Goal: Improve draft helper with more data sources to make better recommendations
```

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
```

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
```

---

## Step 4: Create Specific Test Scenarios

### Step 4.1: Convert High-Level Categories to Concrete Tests

**Goal:** Transform abstract test categories into specific, executable test scenarios

**Test Scenario Format:**
```markdown
### Test Scenario {N}: {Name}

**Context:** {What features/components this tests}
**Steps:** {Specific commands or actions}
**Expected Output:** {Concrete, measurable output}
**Success Criteria:** {Specific pass conditions}
```

**Example Scenarios:**

### Test Scenario 1: Data File Creation

**Context:** Features 1-3 create data files (CSV/JSON)
**Steps:**
1. Delete existing data files
2. Run: `python run_league_helper.py --mode draft`
3. Check data/ directory

**Expected Output:**
- All data files created with valid content
- CSV/JSON formats parseable

**Success Criteria:**
- [ ] All required files created
- [ ] Files contain valid data
- [ ] No errors during creation

---

### Test Scenario 2: End-to-End Workflow

**Context:** Complete feature workflow with all integrations
**Steps:**
1. Run: `python run_league_helper.py --mode {primary_mode}`
2. Execute feature-specific actions
3. Verify output includes all expected data

**Expected Output:**
- All features contribute to final result
- No missing data or errors

**Success Criteria:**
- [ ] All features integrated correctly
- [ ] Output matches expected format
- [ ] No errors or warnings

---

**Additional Scenario Types:**
- **Error Handling:** Test missing dependencies, invalid config, corrupt data
- **Edge Cases:** Boundary conditions, empty inputs, max values
- **Performance:** Response times, large dataset handling
- **Backward Compatibility:** Old data formats, deprecated features

**Complete examples:** See `reference/stage_4/test_scenario_templates.md` for 6+ detailed scenarios

### Step 4.2: Document Each Test Scenario

Add all scenarios to `epic_smoke_test_plan.md` in structured format shown above.

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
```

### Step 5.2: Replace Epic Success Criteria

Replace vague criteria with measurable ones from Step 3:

```markdown
## Epic Success Criteria

{Paste measurable criteria from Step 3.3}
```

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
```

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
```

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
```

---

## Step 6: S4 Validation Loop (MANDATORY)

**Goal:** Validate epic test plan completeness through iterative review

**Exit Condition:** 3 consecutive clean rounds (zero issues found)

### Validation Process

**Each Round:**
1. **Review test plan** against checklist:
   - [ ] All features have test scenarios
   - [ ] Integration points tested
   - [ ] Success criteria measurable
   - [ ] Edge cases covered
   - [ ] Performance criteria defined

2. **Find issues:** Any gaps, missing scenarios, unclear criteria

3. **Fix immediately:** Update epic_smoke_test_plan.md, no deferrals

4. **Document round:** Record issues found and fixed

5. **Repeat:** Continue until 3 consecutive clean rounds

**Common Issues:**
- Missing integration point tests
- Vague success criteria ("works correctly" vs "returns 200 status")
- Incomplete edge case coverage
- No performance baselines

**Maximum 10 rounds:** Escalate to user if exceeding

---

## Step 7: Mark S4 Complete and Request Gate 4.5 Approval

**Prerequisites:**
- [ ] Validation loop complete (3 consecutive clean rounds)
- [ ] epic_smoke_test_plan.md updated with all scenarios
- [ ] All integration points documented
- [ ] Success criteria measurable

### Gate 4.5: Epic Test Plan Approval (MANDATORY)

**Present to user:**

```markdown
## Epic Test Plan Ready for Approval

S4 (Epic Testing Strategy) is complete.

**Test Plan Summary:**
- Features covered: {N} features
- Test scenarios: {M} scenarios
- Integration points: {K} tested
- Validation: {R} rounds, 3 clean rounds achieved

**Coverage:**
- Feature functionality: {list features}
- Integration: {list integration points}
- Edge cases: {summary}
- Performance: {criteria}

**Review:** `feature-updates/KAI-{N}-{epic_name}/epic_smoke_test_plan.md`

**Do you approve this epic test plan?**

If approved: I'll proceed to S5 (Implementation Planning) for Feature 01
If changes needed: I'll update the test plan
```

**Wait for explicit user approval** before proceeding to S5.

**Handle Response:**
- **If APPROVED:** Mark S4 complete, update Agent Status, proceed to S5
- **If CHANGES:** Update test plan, re-validate, re-present
- **If REJECTED:** Return to appropriate step (2, 3, or 4), restart from there

---

### Update Agent Status

**After approval:**
- Mark S4 complete in EPIC_README.md
- Update Agent Status: Ready for S5 (Feature 01)
- Set Current Guide: `stages/s5/s5_p1_planning_round1.md`

---

## Exit Criteria

**S4 (Epic Testing Strategy) is complete when ALL of the following are true:**

### Test Plan Quality
- [ ] epic_smoke_test_plan.md exists and is complete
- [ ] All features have dedicated test scenarios
- [ ] Integration points identified and have test scenarios
- [ ] Epic success criteria are measurable and specific
- [ ] Edge cases enumerated and have test coverage
- [ ] Performance criteria defined (if applicable)

### Validation Complete
- [ ] Validation Loop completed (3 consecutive clean rounds)
- [ ] Zero deferred issues (all gaps fixed immediately)
- [ ] Test plan internally consistent

### User Approval
- [ ] Gate 4.5 approval requested
- [ ] User explicitly approved epic test plan
- [ ] Any requested changes incorporated

### Documentation Updated
- [ ] EPIC_README.md Agent Status updated with S4 complete
- [ ] Update history in epic_smoke_test_plan.md documents S4 creation
- [ ] Next stage identified: S5 (Feature 01 Implementation Planning)

**If ALL criteria met:** ✅ Proceed to S5 (Implementation Planning) for Feature 01

---

**S4 Complete - Proceed to S5**

---

*End of stages/s4/s4_epic_testing_strategy.md*
