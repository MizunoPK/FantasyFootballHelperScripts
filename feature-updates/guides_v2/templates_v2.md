# Templates v2: Epic & Feature File Templates

**Version:** 2.0
**Last Updated:** 2025-12-30
**Purpose:** Standard templates for all epic and feature documentation files

---

## Overview

This document contains templates for all files used in the v2 epic workflow. Copy these templates when creating new epics, features, or bug fixes.

**Templates Included:**
1. Epic README Template (`EPIC_README.md`)
2. Feature README Template (`feature_XX_{name}/README.md`)
3. Epic Smoke Test Plan Template (`epic_smoke_test_plan.md`)
4. Bug Fix Notes Template (`bugfix_{priority}_{name}/notes.txt`)
5. Feature Spec Template (`spec.md`)
6. Feature Checklist Template (`checklist.md`)
7. Feature TODO Template (`todo.md`)
8. Epic Lessons Learned Template (`epic_lessons_learned.md`)
9. Feature Lessons Learned Template (`lessons_learned.md`)

---

## 1. Epic README Template

**Filename:** `EPIC_README.md`
**Location:** `feature-updates/{epic_name}/EPIC_README.md`
**Created:** Stage 1 (Epic Planning)
**Updated:** Throughout all stages

```markdown
# Epic: {epic_name}

**Created:** {YYYY-MM-DD}
**Status:** {IN PROGRESS / COMPLETE}
**Total Features:** {N}

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage X - {stage name}
**Active Guide:** `guides_v2/{guide_name}.md`
**Last Guide Read:** {YYYY-MM-DD HH:MM}

**Stage Workflow:**
```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC
```

**You are here:** ➜ Stage {X}

**Critical Rules for Current Stage:**
1. {Rule 1 from current guide}
2. {Rule 2 from current guide}
3. {Rule 3 from current guide}
4. {Rule 4 from current guide}
5. {Rule 5 from current guide}

**Before Proceeding to Next Step:**
- [ ] Read guide: `guides_v2/{current_guide}.md`
- [ ] Acknowledge critical requirements
- [ ] Verify prerequisites from guide
- [ ] Update this Quick Reference Card

---

## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Stage:** Stage {X} - {stage name}
**Current Phase:** {PLANNING / IMPLEMENTATION / QC}
**Current Step:** {Specific step name - e.g., "QC Round 2 (Consistency)"}
**Current Guide:** `{guide_file_name}.md`
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Critical Rules from Guide:**
- {Rule 1 - e.g., "24 iterations mandatory, no skipping"}
- {Rule 2 - e.g., "Update Agent Status after each round"}
- {Rule 3 - e.g., "STOP if confidence < Medium"}
- {Rule 4 - e.g., "RESTART Post-Implementation if ANY issues found"}
- {Rule 5 - e.g., "Verify against ACTUAL implementation"}

**Progress:** {X/Y items complete}
**Next Action:** {Exact next task with guide step reference}
**Blockers:** {List any issues or "None"}

---

## Epic Overview

**Epic Goal:**
{Concise description of what this epic achieves - pulled from original {epic_name}.txt request}

**Epic Scope:**
{High-level scope - what's included and what's excluded}

**Key Outcomes:**
1. {Outcome 1}
2. {Outcome 2}
3. {Outcome 3}

**Original Request:** `feature-updates/{epic_name}.txt`

---

## Epic Progress Tracker

**Overall Status:** {X/Y features complete}

| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |
| feature_02_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |
| feature_03_{name} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} | {✅/◻️} |

**Legend:**
- ✅ = Complete
- ◻️ = Not started or in progress

**Stage 6 - Epic Final QC:** {✅ COMPLETE / ◻️ NOT STARTED / 🔄 IN PROGRESS}
- Epic smoke testing passed: {✅/◻️}
- Epic QC rounds passed: {✅/◻️}
- Epic PR review passed: {✅/◻️}
- End-to-end validation passed: {✅/◻️}
- Date completed: {YYYY-MM-DD or "Not complete"}

**Stage 7 - Epic Cleanup:** {✅ COMPLETE / ◻️ NOT STARTED / 🔄 IN PROGRESS}
- Final commits made: {✅/◻️}
- Epic moved to done/ folder: {✅/◻️}
- Date completed: {YYYY-MM-DD or "Not complete"}

---

## Feature Summary

### Feature 01: {feature_name}
**Folder:** `feature_01_{name}/`
**Purpose:** {Brief description}
**Status:** {Stage X complete}
**Dependencies:** {List other features or "None"}

### Feature 02: {feature_name}
**Folder:** `feature_02_{name}/`
**Purpose:** {Brief description}
**Status:** {Stage X complete}
**Dependencies:** {List other features or "None"}

### Feature 03: {feature_name}
**Folder:** `feature_03_{name}/`
**Purpose:** {Brief description}
**Status:** {Stage X complete}
**Dependencies:** {List other features or "None"}

{Continue for all features...}

---

## Bug Fix Summary

**Bug Fixes Created:** {N}

{If no bug fixes: "No bug fixes created yet"}

{If bug fixes exist:}

### Bug Fix 1: {name}
**Folder:** `bugfix_{priority}_{name}/`
**Priority:** {high/medium/low}
**Discovered:** {Stage X - {feature or epic level}}
**Status:** {Stage 5c complete / In progress}
**Impact:** {Brief description of what bug affected}

{Repeat for all bug fixes...}

---

## Epic-Level Files

**Created in Stage 1:**
- `EPIC_README.md` (this file)
- `epic_smoke_test_plan.md` - How to test the complete epic
- `epic_lessons_learned.md` - Cross-feature insights

**Feature Folders:**
- `feature_01_{name}/` - {Brief purpose}
- `feature_02_{name}/` - {Brief purpose}
- `feature_03_{name}/` - {Brief purpose}

**Bug Fix Folders (if any):**
- `bugfix_{priority}_{name}/` - {Brief description}

---

## Workflow Checklist

**Stage 1 - Epic Planning:**
- [ ] Epic folder created
- [ ] All feature folders created
- [ ] Initial `epic_smoke_test_plan.md` created
- [ ] `EPIC_README.md` created (this file)
- [ ] `epic_lessons_learned.md` created

**Stage 2 - Feature Deep Dives:**
- [ ] ALL features have `spec.md` complete
- [ ] ALL features have `checklist.md` resolved
- [ ] ALL feature `README.md` files created

**Stage 3 - Cross-Feature Sanity Check:**
- [ ] All specs compared systematically
- [ ] Conflicts resolved
- [ ] User sign-off obtained

**Stage 4 - Epic Testing Strategy:**
- [ ] `epic_smoke_test_plan.md` updated based on deep dives
- [ ] Integration points identified
- [ ] Epic success criteria defined

**Stage 5 - Feature Implementation:**
- [ ] Feature 1: 5a→5b→5c→5d→5e complete
- [ ] Feature 2: 5a→5b→5c→5d→5e complete
- [ ] Feature 3: 5a→5b→5c→5d→5e complete
- [ ] {List all features}

**Stage 6 - Epic Final QC:**
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] Epic QC rounds passed (all 3 rounds)
- [ ] Epic PR review passed (all 11 categories)
- [ ] End-to-end validation vs original request passed

**Stage 7 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Documentation verified complete
- [ ] Guides updated based on lessons learned (if needed)
- [ ] Final commits made
- [ ] Epic moved to `feature-updates/done/{epic_name}/`

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

| Timestamp | Stage | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|
| {YYYY-MM-DD HH:MM} | {Stage X} | {What was skipped/changed} | {Why agent deviated} | {Consequence - e.g., "QC failed, rework required"} |

**Rule:** If you deviate from guide, DOCUMENT IT HERE immediately.

{If no deviations: "No deviations from guides"}

---

## Epic Completion Summary

{This section filled out in Stage 7}

**Completion Date:** {YYYY-MM-DD}
**Start Date:** {YYYY-MM-DD}
**Duration:** {N days}

**Features Implemented:** {N}
**Bug Fixes Created:** {N}

**Final Test Pass Rate:** {X/Y tests passing} ({percentage}%)

**Epic Location:** `feature-updates/done/{epic_name}/`
**Original Request:** `feature-updates/{epic_name}.txt`

**Key Achievements:**
- {Achievement 1}
- {Achievement 2}
- {Achievement 3}

**Lessons Applied to Guides:**
- {Guide update 1 or "None"}
- {Guide update 2 or "None"}
```

---

## 2. Feature README Template

**Filename:** `README.md`
**Location:** `feature-updates/{epic_name}/feature_XX_{name}/README.md`
**Created:** Stage 1 (Epic Planning) or Stage 2 (Feature Deep Dive)
**Updated:** Throughout feature implementation (Stages 2-5e)

```markdown
# Feature: {feature_name}

**Created:** {YYYY-MM-DD}
**Status:** {Stage X complete}

---

## Feature Context

**Part of Epic:** {epic_name}
**Feature Number:** {N} of {total}
**Created:** {YYYY-MM-DD}

**Purpose:**
{1-2 sentence description of what this feature does and why it's needed}

**Dependencies:**
- **Depends on:** {List features this depends on, or "None"}
- **Required by:** {List features that depend on this, or "Unknown yet" or "None"}

**Integration Points:**
- {Other features this integrates with, or "None (standalone feature)"}

---

## Agent Status

**Last Updated:** {YYYY-MM-DD HH:MM}
**Current Phase:** {PLANNING / TODO_CREATION / IMPLEMENTATION / POST_IMPLEMENTATION / COMPLETE}
**Current Step:** {Specific step - e.g., "Iteration 12/24", "QC Round 2"}
**Current Guide:** `{guide_name}.md`
**Guide Last Read:** {YYYY-MM-DD HH:MM}

**Progress:** {X/Y items complete}
**Next Action:** {Exact next task - e.g., "Complete Iteration 13: Integration Gap Check"}
**Blockers:** {List any issues or "None"}

---

## Feature Stages Progress

**Stage 2 - Feature Deep Dive:**
- [ ] `spec.md` created and complete
- [ ] `checklist.md` created (all items resolved or marked pending)
- [ ] `lessons_learned.md` created
- [ ] README.md created (this file)
- [ ] Stage 2 complete: {✅/◻️}

**Stage 5a - TODO Creation:**
- [ ] 24 verification iterations complete
- [ ] Iteration 4a: TODO Specification Audit PASSED
- [ ] Iteration 23a: Pre-Implementation Spec Audit (ALL 4 PARTS PASSED)
- [ ] Iteration 24: Implementation Readiness PASSED
- [ ] `todo.md` created
- [ ] `questions.md` created (or documented "no questions")
- [ ] Stage 5a complete: {✅/◻️}

**Stage 5b - Implementation:**
- [ ] All TODO tasks complete
- [ ] All unit tests passing (100%)
- [ ] `implementation_checklist.md` created and all verified
- [ ] `code_changes.md` created and updated
- [ ] Stage 5b complete: {✅/◻️}

**Stage 5c - Post-Implementation:**
- [ ] Smoke testing (3 parts) passed
- [ ] QC Round 1 passed
- [ ] QC Round 2 passed
- [ ] QC Round 3 passed
- [ ] PR Review (11 categories) passed
- [ ] `lessons_learned.md` updated with Stage 5c insights
- [ ] Stage 5c complete: {✅/◻️}

**Stage 5d - Cross-Feature Alignment:**
- [ ] Reviewed all remaining feature specs
- [ ] Updated remaining specs based on THIS feature's actual implementation
- [ ] Documented features needing rework (or "none")
- [ ] No significant rework needed for other features
- [ ] Stage 5d complete: {✅/◻️}

**Stage 5e - Epic Testing Plan Update:**
- [ ] `epic_smoke_test_plan.md` reviewed
- [ ] Test scenarios updated based on actual implementation
- [ ] Integration points added to epic test plan
- [ ] Update History table in epic test plan updated
- [ ] Stage 5e complete: {✅/◻️}

---

## Files in this Feature

**Core Files:**
- `README.md` - This file (feature overview and status)
- `spec.md` - **Primary specification** (detailed requirements)
- `checklist.md` - Tracks resolved vs pending decisions
- `lessons_learned.md` - Feature-specific insights

**Planning Files (Stage 5a):**
- `todo.md` - Implementation task list (created in Stage 5a)
- `questions.md` - Questions for user (created in Stage 5a, or documented "no questions")

**Implementation Files (Stage 5b):**
- `implementation_checklist.md` - Continuous spec verification during coding
- `code_changes.md` - Documentation of all code changes

**Research Files (if needed):**
- `research/` - Directory containing research documents

---

## Feature-Specific Notes

{Optional section for any feature-specific context, gotchas, or important notes}

{Example:}
**Design Decisions:**
- {Decision 1 and rationale}
- {Decision 2 and rationale}

**Known Limitations:**
- {Limitation 1}
- {Limitation 2}

**Testing Notes:**
- {Important testing considerations}

---

## Completion Summary

{This section filled out after Stage 5e}

**Completion Date:** {YYYY-MM-DD}
**Start Date:** {YYYY-MM-DD}
**Duration:** {N days}

**Lines of Code Changed:** {~N} (approximate)
**Tests Added:** {N}
**Files Modified:** {N}

**Key Accomplishments:**
- {Accomplishment 1}
- {Accomplishment 2}
- {Accomplishment 3}

**Challenges Overcome:**
- {Challenge 1 and solution}
- {Challenge 2 and solution}

**Stage 5d Impact on Other Features:**
- {Feature X: Updated spec.md to reflect...}
- {Or: "No impact on other features"}
```

---

## 3. Epic Smoke Test Plan Template

**Filename:** `epic_smoke_test_plan.md`
**Location:** `feature-updates/{epic_name}/epic_smoke_test_plan.md`
**Created:** Stage 1 (Epic Planning)
**Updated:** Stage 4 (Epic Testing Strategy), Stage 5e (after each feature)

```markdown
# Epic Smoke Test Plan: {epic_name}

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** {YYYY-MM-DD} (Stage 1)
**Last Updated:** {YYYY-MM-DD} (Stage {X})

---

## Epic Success Criteria

**The epic is successful if:**

1. {Measurable criterion 1}
   - Example: "All 6 position files (QB, RB, WR, TE, K, DST) created in data/player_data/"

2. {Measurable criterion 2}
   - Example: "Each position file contains >100 players with complete stats"

3. {Measurable criterion 3}
   - Example: "Draft recommendations include ADP multipliers and matchup difficulty"

4. {Measurable criterion 4}
   - Example: "Performance tracking data persisted to CSV with accuracy scores"

{Add 3-7 measurable success criteria}

**Epic is considered SUCCESSFUL when ALL criteria above are met.**

---

## Update History

**Track when and why this plan was updated:**

| Date | Stage | Feature | What Changed | Why |
|------|-------|---------|--------------|-----|
| {YYYY-MM-DD} | Stage 1 | (initial) | Initial plan created | Epic planning based on assumptions |
| {YYYY-MM-DD} | Stage 4 | (all features) | Updated based on deep dives | Discovered {N} integration points, refined scenarios |
| {YYYY-MM-DD} | Stage 5e | feature_01 | Added ADP integration scenarios | Feature 1 implementation revealed specific multiplier ranges |
| {YYYY-MM-DD} | Stage 5e | feature_02 | Added matchup cross-check scenarios | Feature 2 integration with Feature 1 needs validation |
| {YYYY-MM-DD} | Stage 5e | feature_03 | Added performance tracking E2E tests | Feature 3 implementation added CSV persistence |

**Current version is informed by:**
- Stage 1: Initial assumptions
- Stage 4: Deep dive findings (Stages 2-3)
- Stage 5e updates: {List features that have updated this plan}

---

## Test Scenarios

**Instructions for Agent:**
- Execute EACH scenario listed below
- Verify ACTUAL DATA VALUES (not just "file exists")
- Document results in Stage 6

---

### Part 1: Epic-Level Import Tests

**Purpose:** Verify all epic modules can be imported together

**Scenario 1: Import All Epic Modules**
```python
python -c "from feature_01.{module} import {Class1}; from feature_02.{module} import {Class2}; from feature_03.{module} import {Class3}"
```

**Expected Result:**
- No import errors
- No circular dependency errors
- All modules load successfully

---

### Part 2: Epic-Level Entry Point Tests

**Purpose:** Verify epic-level entry points start correctly

**Scenario 2: Epic Entry Point Help**
```bash
python run_{epic_main}.py --help
```

**Expected Result:**
- Help text displays correctly
- All expected options shown
- No crashes or errors

**Scenario 3: Epic Entry Point Validation**
```bash
python run_{epic_main}.py --mode {mode1} --option {value}
```

**Expected Result:**
- Entry point starts without errors
- Correct mode activated
- Expected output format

---

### Part 3: Epic End-to-End Execution Tests

**Purpose:** Execute complete epic workflows with REAL data

**Scenario 4: Complete Epic Workflow ({workflow_name})**
```bash
python run_{epic_main}.py --mode {mode} --week {N} --iterations {N}
```

**Expected Result:**
- Command completes successfully (exit code 0)
- Output files created: {list expected files}
- **DATA VERIFICATION (CRITICAL):**
  - File 1: {specific data check - e.g., "df['adp_multiplier'].between(0.5, 1.5).all()"}
  - File 2: {specific data check - e.g., "len(df) > 100"}
  - File 3: {specific data check - e.g., "df['final_score'].notna().all()"}

**Scenario 5: Epic Workflow with Edge Case ({edge_case_name})**
```bash
python run_{epic_main}.py --mode {mode} --{edge_case_flag}
```

**Expected Result:**
- {Expected behavior for edge case}
- Error handling graceful (if expected to fail)
- {Specific validation checks}

{Add 3-5 end-to-end execution test scenarios}

---

### Part 4: Cross-Feature Integration Tests

**Purpose:** Test feature interactions and integration points

**Scenario 6: Feature 01 ↔ Feature 02 Integration**

**Added:** Stage 5e (feature_02_{name})

**What to test:** Verify Feature 01 data correctly consumed by Feature 02

**How to test:**
1. {Step 1 - e.g., "Run Feature 01 to generate ADP data"}
2. {Step 2 - e.g., "Run Feature 02 with ADP data enabled"}
3. {Step 3 - e.g., "Verify both features' effects in final output"}

**Expected result:**
- Feature 01 output: {specific data - e.g., "adp_multiplier calculated for all players"}
- Feature 02 consumption: {specific check - e.g., "final_score reflects both ADP and matchup"}
- Integration point: {specific validation - e.g., "adp_multiplier * matchup_difficulty applied correctly"}

**Scenario 7: Feature 01 ↔ Feature 03 Integration**

**Added:** Stage 5e (feature_03_{name})

**What to test:** Verify Feature 03 tracks Feature 01 data

**How to test:**
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Expected result:**
- {Specific expected outcome}
- {Data validation checks}

**Scenario 8: Three-Way Integration (Features 01, 02, 03)**

**Added:** Stage 5e (feature_03_{name})

**What to test:** Verify all three features work together cohesively

**How to test:**
1. {Step 1 - complete workflow using all features}
2. {Step 2 - verify each feature's contribution}
3. {Step 3 - validate final output}

**Expected result:**
- {Expected final outcome}
- {Data validations showing all three features contributed}

{Add integration scenarios for each feature interaction}

---

## High-Level Test Categories

**Instructions for Agent:**
- These categories are FLEXIBLE - create specific scenarios as needed during Stage 5e/6
- Base scenarios on ACTUAL implementation (not assumptions)

---

### Category 1: Error Handling Validation

**What to test:** Epic handles errors gracefully across all features

**Agent will create scenarios for:**
- Missing data files (each feature)
- Invalid input parameters
- API failures (if applicable)
- Cross-feature error propagation

---

### Category 2: Performance Validation

**What to test:** Epic performance acceptable with realistic data

**Agent will create scenarios for:**
- Full dataset processing time (< {N} seconds)
- Memory usage with large datasets
- No performance regressions from baseline

---

### Category 3: Edge Cases

**What to test:** Epic handles edge cases correctly

**Agent will create scenarios for:**
- {Edge case 1 discovered during implementation}
- {Edge case 2 discovered during implementation}
- {Edge case 3 discovered during implementation}

{Add more categories as needed}

---

## Execution Checklist (For Stage 6)

**Part 1: Import Tests**
- [ ] Scenario 1: Import All Epic Modules - {✅ PASSED / ❌ FAILED}

**Part 2: Entry Point Tests**
- [ ] Scenario 2: Epic Entry Point Help - {✅ PASSED / ❌ FAILED}
- [ ] Scenario 3: Epic Entry Point Validation - {✅ PASSED / ❌ FAILED}

**Part 3: E2E Execution Tests**
- [ ] Scenario 4: Complete Epic Workflow - {✅ PASSED / ❌ FAILED}
- [ ] Scenario 5: Epic Workflow with Edge Case - {✅ PASSED / ❌ FAILED}
- [ ] {Additional scenarios...}

**Part 4: Cross-Feature Integration Tests**
- [ ] Scenario 6: Feature 01 ↔ Feature 02 - {✅ PASSED / ❌ FAILED}
- [ ] Scenario 7: Feature 01 ↔ Feature 03 - {✅ PASSED / ❌ FAILED}
- [ ] Scenario 8: Three-Way Integration - {✅ PASSED / ❌ FAILED}
- [ ] {Additional integration scenarios...}

**Overall Status:** {ALL PASSED / FAILURES - See details above}

---

## Notes

{Optional section for additional context, gotchas, or testing notes}

**Testing Environment:**
- {Required data files}
- {Required configuration}
- {Prerequisites for testing}

**Known Issues:**
- {Issue 1 and workaround}
- {Or: "None"}
```

---

## 4. Bug Fix Notes Template

**Filename:** `notes.txt`
**Location:** `feature-updates/{epic_name}/bugfix_{priority}_{name}/notes.txt`
**Created:** When bug discovered (during any stage)
**Purpose:** User-verified description of the bug and proposed fix

```
BUG FIX: {name}
Priority: {high/medium/low}
Discovered: {YYYY-MM-DD}
Discovered During: Stage {X} - {feature_name or "epic-level"}

----

ISSUE DESCRIPTION:

{Clear, concise description of the bug/issue}

What's wrong:
- {Symptom 1}
- {Symptom 2}
- {Symptom 3}

How discovered:
- {How the issue was found - e.g., "QC Round 2 revealed...", "User reported...", "Epic smoke testing failed..."}

Impact:
- {What doesn't work because of this bug}
- {Severity - e.g., "Epic smoke testing fails", "Feature produces incorrect results", "Minor UI issue"}

----

ROOT CAUSE (if known):

{Analysis of why the bug exists}

{Example:}
During Feature 02 implementation (Stage 5b), the interface between Feature 01 and Feature 02 was enhanced to include both multiplier and rank. Feature 01's get_adp_multiplier() method was not updated to return the tuple format, causing Feature 02 to fail when trying to unpack the return value.

{If root cause unknown: "Root cause not yet determined - will investigate in Stage 2 (Deep Dive)"}

----

PROPOSED SOLUTION:

{How to fix the bug}

{Example:}
Update Feature 01's get_adp_multiplier() method to return a tuple (multiplier, rank) instead of just float multiplier. This will align Feature 01's interface with Feature 02's expectations.

Changes needed:
- File: league_helper/util/PlayerManager.py
- Method: get_adp_multiplier()
- Change: Return (multiplier, adp_rank) tuple instead of just multiplier
- Testing: Verify Feature 02 can successfully unpack the tuple

{If solution not yet known: "Solution TBD - will design in Stage 2 (Deep Dive)"}

----

VERIFICATION PLAN:

{How to verify the fix works}

1. {Test scenario 1}
2. {Test scenario 2}
3. {Test scenario 3}

{Example:}
1. Re-run epic smoke testing (Stage 6, Part 4: Cross-Feature Integration)
2. Verify Scenario 6 (Feature 01 ↔ Feature 02 Integration) now passes
3. Verify Feature 02 can successfully unpack adp_data tuple
4. Verify final_score calculation includes both adp_multiplier and adp_rank effects

Expected result after fix:
- {Expected outcome 1}
- {Expected outcome 2}

----

USER VERIFICATION:

{This section filled out by USER - agent presents notes and asks user to verify/update}

User comments:
{User adds any clarifications, corrections, or additional context}

User approval: {YES / NO / NEEDS CHANGES}
Approved by: {Username}
Approved date: {YYYY-MM-DD}
```

---

## 5. Feature Spec Template

**Filename:** `spec.md`
**Location:** `feature-updates/{epic_name}/feature_XX_{name}/spec.md`
**Created:** Stage 2 (Feature Deep Dive)
**Purpose:** PRIMARY specification for implementation

```markdown
# Feature Specification: {feature_name}

**Part of Epic:** {epic_name}
**Feature Number:** {N}
**Created:** {YYYY-MM-DD}
**Last Updated:** {YYYY-MM-DD}

---

## Feature Overview

**What:** {1-2 sentence description of what this feature does}

**Why:** {1-2 sentences explaining why this feature is needed}

**Who:** {Who benefits from this feature - e.g., "End users", "Draft helper users", "System administrators"}

---

## Functional Requirements

### Requirement 1: {Requirement Name}
**Description:** {Detailed description of the requirement}

**Acceptance Criteria:**
- {Criterion 1}
- {Criterion 2}
- {Criterion 3}

**Example:**
{Concrete example showing requirement in action}

### Requirement 2: {Requirement Name}
**Description:** {Detailed description}

**Acceptance Criteria:**
- {Criteria...}

**Example:**
{Example...}

{Continue for all functional requirements (typically 3-7)}

---

## Technical Requirements

### Algorithms

**Algorithm 1: {Algorithm Name}**
**Purpose:** {What this algorithm does}

**Inputs:**
- {Input 1}: {Type} - {Description}
- {Input 2}: {Type} - {Description}

**Process:**
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Outputs:**
- {Output 1}: {Type} - {Description}

**Edge Cases:**
- {Edge case 1 and handling}
- {Edge case 2 and handling}

**Example Calculation:**
```
Input: player_name="Patrick Mahomes", adp=5
Process:
  1. Fetch ADP data: adp_value = 5
  2. Calculate multiplier: mult = 1.0 + (50 - adp) / 100 = 1.45
  3. Clamp to range: mult = max(0.5, min(1.5, 1.45)) = 1.45
Output: (multiplier=1.45, adp_rank=5)
```

{Repeat for all algorithms}

---

### Data Structures

**Data Structure 1: {Name}**
**Purpose:** {What this data structure represents}

**Fields:**
```python
{
    "field1": {type},  # Description
    "field2": {type},  # Description
    "field3": {type}   # Description
}
```

**Example:**
```python
{
    "player_name": "Patrick Mahomes",
    "adp_rank": 5,
    "adp_multiplier": 1.45
}
```

{Repeat for all data structures}

---

### Interfaces

**Interface 1: {Interface Name}**
**Provider:** {Which module/class provides this}
**Consumer:** {Which modules/classes consume this}

**Method Signature:**
```python
def method_name(param1: Type1, param2: Type2) -> ReturnType:
    """Brief description"""
```

**Parameters:**
- `param1` (Type1): Description
- `param2` (Type2): Description

**Returns:**
- `ReturnType`: Description

**Raises:**
- `ErrorType1`: When {condition}
- `ErrorType2`: When {condition}

**Example Usage:**
```python
result = provider.method_name("value1", 123)
# result: (1.45, 5)
```

{Repeat for all interfaces}

---

## Integration Points

### Integration with {Other Feature/System}

**Direction:** {This feature provides TO / consumes FROM}
**Data Passed:** {Description of data}
**Interface:** {Reference to interface above}

**Example Flow:**
```
Feature 01 (ADP Integration)
  ↓ provides adp_data: (multiplier, rank)
Feature 02 (Matchup System)
  ↓ consumes adp_data, provides matchup_difficulty
Feature 03 (Performance Tracker)
  ↓ consumes both adp_data and matchup_difficulty
```

{Repeat for all integration points}

---

## Error Handling

**Error Scenario 1: {Scenario Name}**
**Condition:** {When this error occurs}
**Handling:** {How to handle it}
**User Message:** "{Error message shown to user}"
**Logged:** {What gets logged}

**Example:**
```python
try:
    adp_data = fetch_adp_data(player_name)
except DataProcessingError as e:
    logger.error(f"ADP data not found for {player_name}: {e}")
    return (1.0, 999)  # Default: no ADP bonus, rank 999 (unknown)
```

{Repeat for all error scenarios}

---

## Testing Strategy

**Unit Tests:**
- {Test category 1 - e.g., "Algorithm calculations with various inputs"}
- {Test category 2 - e.g., "Edge case handling"}
- {Test category 3 - e.g., "Error conditions"}

**Integration Tests:**
- {Integration test 1 - e.g., "Feature 01 → Feature 02 data flow"}
- {Integration test 2 - e.g., "Feature 02 → Feature 03 data flow"}

**Smoke Tests (Feature-Level):**
- {Smoke test 1 - e.g., "Import test"}
- {Smoke test 2 - e.g., "Entry point test"}
- {Smoke test 3 - e.g., "E2E execution test with data validation"}

---

## Non-Functional Requirements

**Performance:**
- {Requirement - e.g., "Process all players in < 2 seconds"}

**Scalability:**
- {Requirement - e.g., "Handle 500+ players without degradation"}

**Reliability:**
- {Requirement - e.g., "Gracefully handle missing data files"}

**Maintainability:**
- {Requirement - e.g., "Follow project coding standards"}

---

## Out of Scope

**Explicitly NOT included in this feature:**
- {Item 1 that might be expected but isn't included}
- {Item 2}
- {Item 3}

{Example: "ADP data fetching - uses existing data files, doesn't fetch from external APIs"}

---

## Open Questions

{Questions that need answers before/during implementation}

**Question 1:** {Question text}
**Status:** {RESOLVED / PENDING / BLOCKED}
**Answer:** {Answer if resolved}
**Asked:** {YYYY-MM-DD}
**Resolved:** {YYYY-MM-DD or "Not yet"}

{If no open questions: "No open questions"}

---

## Implementation Notes

{Any additional context, design decisions, or notes for implementers}

**Design Decisions:**
- {Decision 1 and rationale}
- {Decision 2 and rationale}

**Implementation Tips:**
- {Tip 1}
- {Tip 2}

**Gotchas:**
- {Gotcha 1 to watch out for}
- {Gotcha 2}

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| {YYYY-MM-DD} | {Agent/User} | Initial spec created | Stage 2 (Feature Deep Dive) |
| {YYYY-MM-DD} | {Agent/User} | {Change description} | {Reason - e.g., "Stage 5d alignment update based on Feature 01 implementation"} |
```

---

## 6. Feature Checklist Template

**Filename:** `checklist.md`
**Location:** `feature-updates/{epic_name}/feature_XX_{name}/checklist.md`
**Created:** Stage 2 (Feature Deep Dive)
**Purpose:** Track resolved vs pending decisions

```markdown
# Feature Checklist: {feature_name}

**Part of Epic:** {epic_name}
**Last Updated:** {YYYY-MM-DD}

---

## Purpose

This checklist tracks decisions and open items for the feature. Items marked `[x]` are resolved. Items marked `[ ]` are pending.

**Stage 2 (Feature Deep Dive) is complete when ALL items are marked `[x]`.**

---

## Functional Decisions

- [x] Feature scope defined
- [x] Functional requirements documented (spec.md)
- [ ] {Pending decision 1}
- [ ] {Pending decision 2}

---

## Technical Decisions

- [x] Algorithms defined and documented
- [x] Data structures specified
- [x] Interfaces designed
- [ ] {Pending technical decision 1}
- [ ] {Pending technical decision 2}

---

## Integration Decisions

- [x] Integration points identified
- [x] Data flow documented
- [ ] {Pending integration decision}

---

## Error Handling Decisions

- [x] Error scenarios identified
- [x] Error handling strategy defined
- [ ] {Pending error handling decision}

---

## Testing Decisions

- [x] Unit test strategy defined
- [x] Integration test strategy defined
- [x] Smoke test scenarios identified
- [ ] {Pending testing decision}

---

## Open Questions

- [ ] {Open question 1 - needs answer before implementation}
- [ ] {Open question 2}

{When all questions resolved, mark them [x]}

---

## Dependencies

- [x] Feature 01 interface verified (if depends on other features)
- [ ] {Pending dependency verification}

{If no dependencies: "No dependencies"}

---

## Stage 2 Completion Status

**Total Items:** {N}
**Resolved:** {X}
**Pending:** {Y}

**Stage 2 Complete?** {YES (all items [x]) / NO (Y items pending)}

**If NO, do NOT proceed to Stage 5a until all items resolved.**
```

---

## 7. Feature TODO Template

**Filename:** `todo.md`
**Location:** `feature-updates/{epic_name}/feature_XX_{name}/todo.md`
**Created:** Stage 5a (TODO Creation)
**Purpose:** Implementation task list with complete traceability

```markdown
# Feature TODO: {feature_name}

**Part of Epic:** {epic_name}
**Created:** {YYYY-MM-DD} (Stage 5a)
**Status:** {IN PROGRESS / COMPLETE}

---

## Verification Summary

**24 Verification Iterations:** {PASSED / IN PROGRESS}
**Iteration 4a (TODO Specification Audit):** {PASSED / PENDING}
**Iteration 23a (Pre-Implementation Spec Audit):** {PASSED / PENDING}
**Iteration 24 (Implementation Readiness):** {PASSED / PENDING}

**Ready to Implement?** {YES / NO}

---

## Implementation Tasks

### Phase 1: Core Algorithm Implementation

**Task 1: Implement {AlgorithmName}**
**File:** `{path/to/file.py}`
**Function/Class:** `{function_or_class_name}`
**Spec Reference:** spec.md - Section "Algorithms" → Algorithm 1
**Description:** {Brief description of what this task does}

**Subtasks:**
- [ ] Create function signature
- [ ] Implement step 1: {description}
- [ ] Implement step 2: {description}
- [ ] Handle edge case: {case 1}
- [ ] Handle edge case: {case 2}
- [ ] Add docstring
- [ ] Add type hints

**Acceptance:**
- Returns correct output for normal inputs
- Handles all edge cases as specified
- Follows project coding standards

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

---

**Task 2: Implement {DataStructure}**
**File:** `{path/to/file.py}`
**Class:** `{class_name}`
**Spec Reference:** spec.md - Section "Data Structures" → Data Structure 1
**Description:** {Brief description}

**Subtasks:**
- [ ] {Subtask 1}
- [ ] {Subtask 2}

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

{Continue for all Phase 1 tasks...}

---

### Phase 2: Integration Implementation

**Task 5: Implement Interface to {OtherFeature}**
**File:** `{path/to/file.py}`
**Method:** `{method_name}`
**Spec Reference:** spec.md - Section "Interfaces" → Interface 1
**Description:** {Description}

**Subtasks:**
- [ ] {Subtask 1}
- [ ] {Subtask 2}

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

{Continue for all Phase 2 tasks...}

---

### Phase 3: Error Handling Implementation

**Task 8: Implement Error Handling for {Scenario}**
**File:** `{path/to/file.py}`
**Spec Reference:** spec.md - Section "Error Handling" → Error Scenario 1
**Description:** {Description}

**Subtasks:**
- [ ] {Subtask 1}
- [ ] {Subtask 2}

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

{Continue for all Phase 3 tasks...}

---

### Phase 4: Testing Implementation

**Task 10: Write Unit Tests for {Algorithm}**
**File:** `tests/feature_XX_{name}/test_{module}.py`
**Spec Reference:** spec.md - Section "Testing Strategy"
**Description:** {Description}

**Subtasks:**
- [ ] Test normal inputs
- [ ] Test edge cases
- [ ] Test error conditions
- [ ] Verify 100% code coverage for algorithm

**Status:** {NOT STARTED / IN PROGRESS / COMPLETE}

{Continue for all Phase 4 tasks...}

---

## Algorithm Traceability Matrix

**Purpose:** Map every algorithm in spec.md to exact code location

| Algorithm (from spec.md) | File | Function/Method | Line Numbers | Status |
|---------------------------|------|-----------------|--------------|--------|
| Algorithm 1: {name} | {file.py} | {function_name()} | Lines {N}-{M} | {IMPLEMENTED / TODO} |
| Algorithm 2: {name} | {file.py} | {function_name()} | Lines {N}-{M} | {IMPLEMENTED / TODO} |

{All algorithms from spec.md MUST be listed here}

---

## Interface Verification Matrix

**Purpose:** Verify all interfaces match actual implementations

| Interface (from spec.md) | Provider File | Provider Method | Consumer File | Consumer Method | Verified |
|---------------------------|---------------|-----------------|---------------|-----------------|----------|
| Interface 1: {name} | {provider.py} | {method()} | {consumer.py} | {method()} | {YES / NO} |
| Interface 2: {name} | {provider.py} | {method()} | {consumer.py} | {method()} | {YES / NO} |

{All interfaces from spec.md MUST be listed here}

---

## Integration Points Checklist

**Purpose:** Track all integration points

| Integration Point | This Feature | Other Feature | Data Passed | Interface | Status |
|-------------------|--------------|---------------|-------------|-----------|--------|
| To Feature 02 | Provides | Consumes | {data description} | {interface name} | {IMPLEMENTED / TODO} |
| From Feature 01 | Consumes | Provides | {data description} | {interface name} | {IMPLEMENTED / TODO} |

{All integration points from spec.md MUST be listed here}

---

## Progress Tracking

**Total Tasks:** {N}
**Completed:** {X}
**In Progress:** {Y}
**Not Started:** {Z}

**Overall Progress:** {X/N} ({percentage}%)

**Current Phase:** Phase {N} - {phase name}
**Next Task:** Task {N} - {task name}

---

## Blockers

{List any blockers preventing task completion}

**Blocker 1:**
- **Task Affected:** Task {N}
- **Issue:** {Description of blocker}
- **Resolution:** {How to resolve or "TBD"}
- **Status:** {BLOCKED / RESOLVED}

{If no blockers: "No blockers"}

---

## Completion Checklist

**Before marking TODO complete:**
- [ ] ALL tasks marked COMPLETE
- [ ] Algorithm Traceability Matrix: All algorithms implemented
- [ ] Interface Verification Matrix: All interfaces verified
- [ ] Integration Points: All integration points implemented
- [ ] All unit tests written and passing (100%)
- [ ] No blockers remain

**TODO Complete?** {YES / NO}
```

---

## 8. Epic Lessons Learned Template

**Filename:** `epic_lessons_learned.md`
**Location:** `feature-updates/{epic_name}/epic_lessons_learned.md`
**Created:** Stage 1 (Epic Planning)
**Updated:** Throughout all stages (after each feature completion)

```markdown
# Epic Lessons Learned: {epic_name}

**Epic Overview:** {Brief description of epic}
**Date Range:** {start_date} - {end_date}
**Total Features:** {N}
**Total Bug Fixes:** {N}

---

## Purpose

This document captures:
- **Cross-feature insights** (patterns observed across multiple features)
- **Systemic issues** (problems affecting multiple features)
- **Guide improvements** (updates needed for guides_v2/)
- **Workflow refinements** (process improvements for future epics)

**This is separate from per-feature lessons_learned.md files** (which capture feature-specific insights).

---

## Stage 1 Lessons Learned (Epic Planning)

**What Went Well:**
- {Positive observation 1}
- {Positive observation 2}

**What Could Be Improved:**
- {Improvement opportunity 1}
- {Improvement opportunity 2}

**Insights for Future Epics:**
- {Insight 1}
- {Insight 2}

**Guide Improvements Needed:**
- {Guide file name}: {Specific improvement needed}
- {Or: "None identified"}

---

## Stage 2 Lessons Learned (Feature Deep Dives)

{Lessons captured AFTER all features complete Stage 2}

### Cross-Feature Patterns

**Pattern 1:** {Pattern observed across features}
- Observed in: {List features}
- Impact: {How this affected development}
- Recommendation: {What to do differently}

**Pattern 2:** {Another pattern}
- {Details...}

### Feature-Specific Highlights

**Feature 01 ({name}):**
- Key lesson: {Lesson from this feature's Stage 2}
- Application to other features: {How this applies beyond Feature 01}

**Feature 02 ({name}):**
- Key lesson: {Lesson}
- Application: {Application}

{Repeat for all features}

### What Went Well

- {Positive observation 1}
- {Positive observation 2}

### What Could Be Improved

- {Improvement 1}
- {Improvement 2}

### Guide Improvements Needed

- `STAGE_2_feature_deep_dive_guide.md`: {Specific improvement}
- {Or: "None identified"}

---

## Stage 3 Lessons Learned (Cross-Feature Sanity Check)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**Conflicts Discovered:**
- {Conflict 1 and resolution}
- {Conflict 2 and resolution}
- {Or: "No conflicts discovered"}

**Insights for Future Epics:**
- {Insight}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

---

## Stage 4 Lessons Learned (Epic Testing Strategy)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**epic_smoke_test_plan.md Evolution:**
- Changes from Stage 1 → Stage 4: {Summary of how test plan evolved}
- Integration points discovered: {N}
- Key insights: {Insights about testing strategy}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

---

## Stage 5 Lessons Learned (Feature Implementation)

{Capture lessons AFTER EACH feature completes Stage 5e}

### Feature 01 ({name}) - Stages 5a through 5e

**Stage 5a (TODO Creation):**
- What went well: {Observation}
- What could improve: {Improvement}
- 24 iterations experience: {Any issues with specific iterations}

**Stage 5b (Implementation):**
- What went well: {Observation}
- Challenges: {Challenges encountered and solutions}

**Stage 5c (Post-Implementation):**
- Smoke testing results: {Summary}
- QC rounds: {Any issues found and resolved}
- PR review: {Insights}

**Stage 5d (Cross-Feature Alignment):**
- Features affected: {List features whose specs were updated}
- Key updates: {Summary of spec updates}

**Stage 5e (Epic Testing Plan Update):**
- Test scenarios added: {N}
- Integration scenarios: {Summary}

---

### Feature 02 ({name}) - Stages 5a through 5e

{Repeat structure for Feature 02}

---

### Feature 03 ({name}) - Stages 5a through 5e

{Repeat structure for Feature 03}

---

### Cross-Feature Implementation Patterns

**Pattern 1:** {Pattern observed during implementation}
- Observed in: {List features}
- Impact: {How this affected development}
- Recommendation: {What to do differently}

---

### Guide Improvements Needed from Stage 5

**From Feature 01:**
- `STAGE_5aa_round1_guide.md`: {Specific improvement}
- `STAGE_5ca_smoke_testing_guide.md`: {Specific improvement}

**From Feature 02:**
- {Guide improvements}

**From Feature 03:**
- {Guide improvements}

---

## Stage 6 Lessons Learned (Epic Final QC)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**Epic-Level Issues Found:**
- {Issue 1 and resolution}
- {Or: "No epic-level issues found"}

**epic_smoke_test_plan.md Effectiveness:**
- Scenarios that caught issues: {List}
- Scenarios that should be added: {List or "None"}
- Overall assessment: {Assessment of test plan quality}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

---

## Stage 7 Lessons Learned (Epic Cleanup)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**Documentation Quality:**
- {Assessment of final documentation completeness}

**Guide Improvements Needed:**
- {Guide improvements or "None"}

---

## Cross-Epic Insights

{High-level insights applicable beyond this epic}

**Systemic Patterns:**
- {Pattern 1 observed across ALL features}
- {Pattern 2}

**Workflow Refinements:**
- {Refinement 1 for future epics}
- {Refinement 2}

**Tool/Process Improvements:**
- {Improvement 1}
- {Improvement 2}

---

## Recommendations for Future Epics

**Top 5 Recommendations:**
1. {Recommendation 1 - actionable and specific}
2. {Recommendation 2}
3. {Recommendation 3}
4. {Recommendation 4}
5. {Recommendation 5}

**Do These Things:**
- {Practice to continue}
- {Practice to continue}

**Avoid These Things:**
- {Anti-pattern to avoid}
- {Anti-pattern to avoid}

---

## Guide Updates Applied

{Track which guides were updated based on lessons from THIS epic}

**Guides Updated:**
- `{guide_name}.md` (v2.{X}): {What was updated}
- `{guide_name}.md` (v2.{X}): {What was updated}

**CLAUDE.md Updates:**
- {Updates made or "None"}

**Date Applied:** {YYYY-MM-DD}

---

## Metrics

**Epic Duration:** {N} days
**Features:** {N}
**Bug Fixes:** {N}
**Tests Added:** {N}
**Files Modified:** {N}
**Lines of Code Changed:** ~{N}

**Stage Durations:**
- Stage 1: {N} days
- Stage 2: {N} days (all features)
- Stage 3: {N} days
- Stage 4: {N} days
- Stage 5: {N} days (all features)
- Stage 6: {N} days
- Stage 7: {N} days

**QC Restart Count:**
- Stage 5c restarts: {N} (across all features)
- Stage 6 restarts: {N}

**Test Pass Rates:**
- Final pass rate: {percentage}% ({X}/{Y} tests)
- Tests added by this epic: {N}
```

---

## 9. Feature Lessons Learned Template

**Filename:** `lessons_learned.md`
**Location:** `feature-updates/{epic_name}/feature_XX_{name}/lessons_learned.md`
**Created:** Stage 2 (Feature Deep Dive)
**Updated:** After Stages 5a, 5b, 5c

```markdown
# Feature Lessons Learned: {feature_name}

**Part of Epic:** {epic_name}
**Feature Number:** {N}
**Created:** {YYYY-MM-DD}
**Last Updated:** {YYYY-MM-DD}

---

## Purpose

This document captures lessons specific to THIS feature's development. This is separate from epic_lessons_learned.md (which captures cross-feature patterns).

---

## Stage 2 Lessons Learned (Feature Deep Dive)

**What Went Well:**
- {Positive observation 1}
- {Positive observation 2}

**What Could Be Improved:**
- {Improvement opportunity 1}
- {Improvement opportunity 2}

**Key Decisions:**
- {Decision 1 and rationale}
- {Decision 2 and rationale}

**Gotchas Discovered:**
- {Gotcha 1}
- {Gotcha 2}

---

## Stage 5a Lessons Learned (TODO Creation)

**24 Verification Iterations Experience:**
- Iterations that were most valuable: {List iterations and why}
- Iterations where issues were found: {List and what was caught}
- Iterations that seemed redundant: {List and why - helps improve guide}

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

**Complexity Assessment:**
- Initial complexity estimate: {LOW / MEDIUM / HIGH}
- Actual complexity: {LOW / MEDIUM / HIGH}
- Variance explanation: {Why estimate was off, if applicable}

---

## Stage 5b Lessons Learned (Implementation)

**What Went Well:**
- {Positive observation}

**Challenges Encountered:**
- **Challenge 1:** {Description}
  - Solution: {How it was resolved}
  - Time impact: {How much extra time}

- **Challenge 2:** {Description}
  - Solution: {Solution}
  - Time impact: {Impact}

**Deviations from Spec:**
- {Deviation 1 and justification}
- {Or: "No deviations from spec"}

**Code Quality Notes:**
- {Note 1}
- {Note 2}

---

## Stage 5c Lessons Learned (Post-Implementation)

**Smoke Testing Results:**
- Part 1 (Import): {PASSED / Issues found and fixed}
- Part 2 (Entry Point): {PASSED / Issues found and fixed}
- Part 3 (E2E Execution): {PASSED / Issues found and fixed}

**QC Rounds Results:**
- QC Round 1: {PASSED / Issues found and fixed}
- QC Round 2: {PASSED / Issues found and fixed}
- QC Round 3: {PASSED / Issues found and fixed}

**PR Review Results:**
- Categories with issues: {List or "None"}
- Key improvements made: {List}

**QC Restart Count:** {N} (if > 0, explain why restart was needed)

**What Went Well:**
- {Positive observation}

**What Could Be Improved:**
- {Improvement}

---

## Implementation Insights

**Algorithm Performance:**
- {Algorithm 1}: {Performance notes}
- {Algorithm 2}: {Performance notes}

**Data Structure Choices:**
- {Choice 1 and rationale}
- {Choice 2 and rationale}

**Integration Challenges:**
- {Challenge 1 with other features and solution}
- {Or: "No integration challenges"}

**Testing Insights:**
- {Insight 1}
- {Insight 2}

---

## Recommendations

**For Similar Features in Future Epics:**
- Do: {Recommendation 1}
- Do: {Recommendation 2}
- Avoid: {Anti-pattern 1}
- Avoid: {Anti-pattern 2}

**For This Feature's Maintenance:**
- {Maintenance note 1}
- {Maintenance note 2}

---

## Guide Improvements Needed

{Specific improvements needed for guides_v2/ based on THIS feature's experience}

**Stage 5a TODO Creation:**
- STAGE_5aa_round1_guide.md: {Improvement 1 or "None"}
- STAGE_5ab_round2_guide.md: {Improvement 1 or "None"}
- STAGE_5ac_round3_guide.md: {Improvement 1 or "None"}

**STAGE_5b_implementation_execution_guide.md:**
- {Improvement 1 or "None"}

**Stage 5c Post-Implementation:**
- STAGE_5ca_smoke_testing_guide.md: {Improvement 1 or "None"}
- STAGE_5cb_qc_rounds_guide.md: {Improvement 1 or "None"}
- STAGE_5cc_final_review_guide.md: {Improvement 1 or "None"}

{If no guide improvements needed: "No guide improvements identified from this feature"}

---

## Metrics

**Feature Duration:** {N} days
**LOC Changed:** ~{N}
**Tests Added:** {N}
**Files Modified:** {N}

**Stage Durations:**
- Stage 2: {N} days
- Stage 5a: {N} days
- Stage 5b: {N} days
- Stage 5c: {N} days
- Stage 5d: {N} days
- Stage 5e: {N} days

**Test Pass Rate:** {percentage}% ({X}/{Y} tests)
```

---

## Summary

These templates provide standardized structure for all epic and feature documentation. When starting a new epic or feature:

1. **Copy the appropriate template**
2. **Replace all `{placeholders}` with actual values**
3. **Update sections as work progresses**
4. **Keep documentation current** (especially Agent Status and Progress Tracker)

**Templates serve as:**
- Starting points for new work
- Checklists to ensure completeness
- Standards for consistency across epics
- Context preservation for future agents

---

**END OF TEMPLATES v2**
