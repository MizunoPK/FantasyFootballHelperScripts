# Epic: improve_configurability_of_scripts

**Created:** 2026-01-28
**Status:** IN PROGRESS (S1 complete, S2 beginning)
**Total Features:** 9 (user-approved)

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** S8.P1 - Cross-Feature Alignment (Feature 01 Implementation Complete)
**Active Guide:** `guides_v2/stages/s8/s8_p1_cross_feature_alignment.md`
**Last Guide Read:** 2026-01-31

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
 ✅   ✅   ✅   ✅     ✅ ✅ ✅ 🔄       ↓        ↓
Epic  Features Sanity Testing Feature_01  Epic    Done
Plan  Deep Dive Check Strategy  Complete    QC
```

**You are here:** 🔄 S8.P1 (Feature 01 complete, aligning remaining features)

**Critical Rules for Current Stage:**
1. REVIEW ALL REMAINING FEATURES (Not just "related" ones)
2. COMPARE TO ACTUAL IMPLEMENTATION (Not the plan)
3. UPDATE SPECS PROACTIVELY (Don't wait for implementation)
4. MARK FEATURES NEEDING SIGNIFICANT REWORK
5. DOCUMENT INSIGHTS IN SPEC
6. UPDATE CHECKLIST.MD TOO
7. CHECK DEPENDENCIES (Both directions)
8. NO "PROBABLY FINE" ASSUMPTIONS

**S7 Completion Status (Feature 01):**
- [x] S7.P1 Smoke Testing PASSED
- [x] S7.P2 QC Rounds PASSED (3 rounds, zero final issues)
- [x] S7.P3 Final Review PASSED (1 minor fix, zero tech debt)
- [x] Feature-level commit made
- [x] All tests passing (2518/2518)

**Next Action:** Identify remaining features (02-09), sequentially review each spec against Feature 01 actual code

---

## Agent Status

**Debugging Active:** NO
**Last Updated:** 2026-02-01 18:30
**Current Stage:** S10.P1 - Guide Update from Lessons Learned COMPLETE
**Current Phase:** GUIDE_UPDATES_APPLIED
**Current Step:** Guide updates complete, resume epic work at S5 for Feature 10
**Current Guide:** `stages/s10/s10_p1_guide_update_workflow.md`
**Guide Last Read:** 2026-02-01

**S10.P1 Summary:**
- Proposals: 11 (11 approved, 0 modified, 0 rejected)
- Guides updated: 18 files
- Commits: 2 (guide updates + tracking)
- Priority breakdown: 5 P0, 4 P1, 2 P2, 0 P3

**Epic Work Status:** S4 complete for Feature 10, ready to resume at S5 (Implementation Planning)

**Missed Requirement Details:**
- **Name:** feature_10_refactor_player_fetcher
- **Discovered During:** S8.P1 (Cross-Feature Alignment)
- **Discovery:** Feature 01 uses config override pattern; constructor pattern is better design
- **User Decision:** Create new feature (Option 1)
- **Priority:** Medium
- **Sequence Position:** Between Feature 07 and Feature 08
- **Approach:** Refactor Feature 01 to use constructor parameters instead of config overrides

**Paused Work:**
- **Paused Stage:** S8.P1 (Cross-Feature Alignment)
- **Paused Feature:** Feature 01 (player_fetcher) - complete through S7
- **Paused Task:** Reviewing remaining feature specs (02-09) against Feature 01 implementation
- **Progress When Paused:** 1/8 features reviewed (Feature 02 analysis complete)
- **Resume Point:** After Feature 10 S2/S3/S4 complete, resume Feature 02-09 spec alignment
- **Resume File:** `feature_02_schedule_fetcher/S8_P1_ALIGNMENT_ANALYSIS.md` (continue from Feature 03)

**Missed Requirement Protocol Progress:**
- ✅ Phase 1: Discovery & User Decision COMPLETE
- 🔄 Phase 2: Planning (S2 Deep Dive) - IN PROGRESS
- ◻️ Phase 3: Realignment (S3 Cross-Feature Sanity Check) - NOT STARTED
- ◻️ Phase 4: Realignment (S4 Epic Testing Update) - NOT STARTED
- ◻️ Phase 5: Resume Previous Work - NOT STARTED

**Next Action:** Create feature_10_refactor_player_fetcher/ folder, begin S2 deep dive
**Blockers:** None

**Note:** Groups 2 & 3 remain paused (Feature 08 awaiting Group 1 specs ✅, Feature 09 awaiting Groups 1 & 2 specs)

---

## Epic Overview

**Epic Goal:**
Make runner scripts configurable with argument-based control over behavior, add debug mode support, and create integration test runners for end-to-end testing with multiple argument combinations.

**Epic Scope:**

**In Scope:**
- Add argument-based configuration to all runner scripts (7 scripts)
- Create fast E2E test modes (~3 min max per script) for integration testing
- Add debug mode logging support across all scripts
- Create per-script integration test runners (test multiple argument combinations)
- Create master integration test runner (runs all individual test runners)
- Update documentation for new testing workflows
- Scripts to modify: run_league_helper.py, run_player_fetcher.py, run_schedule_fetcher.py, run_win_rate_simulation.py, run_accuracy_simulation.py, run_game_data_fetcher.py, compile_historical_data.py

**Out of Scope:**
- Modifying scoring algorithms or business logic
- Adding new features to league helper modes
- Changing simulation algorithms
- Modifying data fetching API logic

**Key Outcomes:**
1. All 7 runner scripts accept command-line arguments for configuration
2. Each script has E2E test mode that completes in ~3 minutes
3. All scripts support debug logging mode
4. 7 individual integration test runners (one per script)
5. 1 master integration test runner
6. Documentation updated with testing workflows

**Original Request:** `improve_configurability_of_scripts_notes.txt`

---

## Feature Dependency Groups

**Lesson Learned Applied (2026-01-30):** Features should be grouped by dependencies and executed in sequential groups

**Group 1 (Independent - ✅ S2 COMPLETE):**
- Feature 01: player_fetcher ✅ S2 Complete (2026-01-30)
- Feature 02: schedule_fetcher ✅ S2 Complete (2026-01-30)
- Feature 03: game_data_fetcher ✅ S2 Complete (2026-01-30)
- Feature 04: historical_compiler ✅ S2 Complete (2026-01-30) ⭐ JUST COMPLETED
- Feature 05: win_rate_simulation ✅ S2 Complete (2026-01-30)
- Feature 06: accuracy_simulation ✅ S2 Complete (2026-01-30)
- Feature 07: league_helper ✅ S2 Complete (2026-01-30)

**Group 1 Status:** ✅ 7/7 COMPLETE - All specs approved and ready for S3!

**Group 2 (Depends on Group 1 Specs - NOT STARTED YET):**
- Feature 08: integration_test_framework ⏸️ PAUSED (waiting for Group 1)
  - **Needs:** Features 1-7 spec.md files (argument lists, E2E mode specs, debug mode details)
  - **Why:** Integration tests need to know what CLI arguments exist for each script
  - **Start After:** All Group 1 features complete S2

**Group 3 (Depends on Group 2 Specs - NOT STARTED YET):**
- Feature 09: documentation ⏸️ PAUSED (waiting for Groups 1 & 2)
  - **Needs:** Features 1-8 spec.md files (complete epic scope to document)
  - **Why:** Documentation describes all features and their requirements
  - **Start After:** Feature 08 completes S2

**Execution Plan:**
- **Current:** Group 1 S2 execution (parallel, 6/7 complete)
- **Next:** Group 2 spawn after Feature 04 completes S2
- **Then:** Group 3 spawn after Feature 08 completes S2
- **Finally:** S3 (Cross-Feature Sanity Check) after all groups complete S2

---

## Missed Requirements Handled

**Total Missed Requirements:** 1

| # | Name | Option | Priority | Created | Sequence Position | S2 | S3 | S4 | Implemented | Status |
|---|------|--------|----------|---------|-------------------|----|----|----|-----------|----|
| 1 | feature_10_refactor_player_fetcher | New Feature | Medium | 2026-01-31 | Between F07 and F08 | 🔄 | ◻️ | ◻️ | ◻️ | Planning |

**Legend:**
- ✅ = Complete
- 🔄 = In Progress
- ◻️ = Not Started

---

## Epic Progress Tracker

**Overall Status:** 0/10 features complete (1 missed requirement added, Feature 01 at S8.P1 paused)
- ✅ **Group 1: 7/7 S2 COMPLETE, S3 COMPLETE, S4 COMPLETE** (Round 1 complete)
- ✅ **Group 2: 1/1 S2 COMPLETE, S3 COMPLETE, S4 COMPLETE** (Round 2 complete)
- ✅ **Group 3: 1/1 S2 COMPLETE, S3 COMPLETE, S4 COMPLETE** (Round 3 COMPLETE)
- 🔄 **Feature 01: S5-S7 COMPLETE, S8.P1 PAUSED** (for Feature 10 planning)
- 🔄 **Feature 10: S2 IN PROGRESS** (Missed requirement - refactor Feature 01)

**Updated Sequence (with Feature 10 inserted):**
1. feature_01_player_fetcher → feature_02_schedule_fetcher → ... → feature_07_league_helper
2. **feature_10_refactor_player_fetcher** ← NEW (between F07 and F08)
3. feature_08_integration_test_framework → feature_09_documentation

| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 |
|---------|-----|-----|-----|-----|-----|-----|-----|-------|-------|
| feature_01_player_fetcher | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 🔄 | ◻️ |
| feature_02_schedule_fetcher | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_03_game_data_fetcher | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_04_historical_compiler | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_05_win_rate_simulation | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_06_accuracy_simulation | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_07_league_helper | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| **feature_10_refactor_player_fetcher** | ✅ | 🔄 | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_08_integration_test_framework | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_09_documentation | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |

**Legend:**
- ✅ = Complete
- ◻️ = Not started or in progress

**S1 - Epic Planning:**
- [x] Git branch created (epic/KAI-7)
- [x] EPIC_TRACKER.md updated
- [x] Epic folder created
- [x] Epic request file moved
- [x] EPIC_README.md created
- [x] Epic analysis complete
- [x] **S1.P3 Discovery Phase complete** (2 iterations, 5 questions resolved, user-approved)
- [x] **DISCOVERY.md created and approved** (Comprehensive Script-Specific Argparse approach)
- [x] Feature breakdown proposed and user-approved (9 features, 1 per script)
- [x] Epic ticket created and user-validated
- [x] Epic structure created (feature folders, test plan, etc.)
- [x] Parallelization assessment (9 features = 89% S2 time reduction)
- [x] User chose PARALLEL work for S2
- [x] Generate handoff packages (complete - 8 secondary agents)
- [x] **Secondary agents notified** (S1.P3 complete, can proceed with S2.P1)
- [ ] Transition to S2 (parallel mode) - secondary agents can now begin

---

<!-- BEGIN SECONDARY-A PROGRESS -->
## Feature 02 Progress (Secondary-A)

**Last Updated:** 2026-01-30
**Current Stage:** S2 COMPLETE - Waiting for Sync Point 1
**Current Step:** All S2 phases complete, awaiting Primary to run S3
**Blockers:** None
**Next Action:** Wait for Primary to complete S3, then proceed to S5 for Feature 02

**S2 Progress:**
- ✅ S2.P1 (Research Phase) - COMPLETE (Research Audit PASSED, 4 files read, 7 code snippets)
- ✅ S2.P2 (Specification Phase) - COMPLETE (Gate 2 PASSED, 2 questions answered)
- ✅ S2.P3 (Refinement Phase) - COMPLETE (Acceptance criteria approved 2026-01-30)

**S2 Completion:** 2026-01-30
**Acceptance Criteria:** User approved
**Ready for Sync:** YES
<!-- END SECONDARY-A PROGRESS -->

---

<!-- BEGIN SECONDARY-B PROGRESS -->
## Feature 03 Progress (Secondary-B)

**Last Updated:** 2026-01-30 00:30
**Current Stage:** S2 COMPLETE
**Current Step:** Waiting for Primary to run S3
**Blockers:** None
**Next Action:** Awaiting S3 (Cross-Feature Sanity Check)

**S2 Progress:**
- ✅ S2.P1 (Research Phase) - COMPLETE (Phase 1.5 audit PASSED)
- ✅ S2.P2 (Specification Phase) - COMPLETE (Phase 2.5 alignment PASSED, Gate 2 PASSED)
- ✅ S2.P3 (Refinement Phase) - COMPLETE (Gate 4 PASSED - 2026-01-30)

**S2 Completion:** 2026-01-30
**Acceptance Criteria:** User approved
**Ready for Sync:** YES
<!-- END SECONDARY-B PROGRESS -->

---

<!-- BEGIN SECONDARY-C PROGRESS -->
## Feature 04 Progress (Secondary-C)

**Last Updated:** 2026-01-30
**Current Stage:** S2 COMPLETE - Waiting for Sync Point 1
**Current Step:** All S2 phases complete, awaiting Primary to run S3
**Blockers:** None
**Next Action:** Wait for Primary to complete S3, then proceed to S5 for Feature 04

**S2 Progress:**
- ✅ S2.P1 (Research Phase) - COMPLETE (Research Audit PASSED, 3 files read)
- ✅ S2.P2 (Specification Phase) - COMPLETE (Gate 3 PASSED, 6 questions answered)
- ✅ S2.P3 (Refinement Phase) - COMPLETE (Acceptance criteria approved 2026-01-30)

**S2 Completion:** 2026-01-30
<!-- END SECONDARY-C PROGRESS -->

---

<!-- BEGIN SECONDARY-D PROGRESS -->
## Feature 05 Progress (Secondary-D)

**Last Updated:** 2026-01-30 16:16
**Current Stage:** S2 COMPLETE - Awaiting S3
**Current Step:** S2.P3 complete, sent completion signal to Primary
**Blockers:** None
**Next Action:** Wait for Primary to coordinate S3 (Cross-Feature Sanity Check)

**S2 Progress:**
- ✅ S2.P1 (Research Phase) - COMPLETE
- ✅ S2.P2 (Specification Phase) - COMPLETE (Gate 3 PASSED)
- ✅ S2.P3 (Refinement Phase) - COMPLETE (Acceptance Criteria APPROVED)

**S2 Completion Details:**
- Completion timestamp: 2026-01-30 16:16
- Checklist questions resolved: 1/1
- Requirements documented: 7 (all with traceability)
- Acceptance criteria: User approved 2026-01-30 16:15
- Cross-feature alignment: Skipped (first feature to S2.P3)
- Ready for S3: YES
<!-- END SECONDARY-D PROGRESS -->

---

<!-- BEGIN SECONDARY-E PROGRESS -->
## Feature 06 Progress (Secondary-E)

**Last Updated:** 2026-01-30 22:29
**Current Stage:** S2 COMPLETE - Waiting for Sync Point 1
**Current Step:** All S2 phases complete, awaiting Primary to run S3
**Blockers:** None
**Next Action:** Wait for Primary to complete S3, then proceed to S5 for Feature 06

**S2 Progress:**
- ✅ S2.P1 (Research Phase) - COMPLETE (Gate 1 PASSED)
- ✅ S2.P2 (Specification Phase) - COMPLETE (Gate 2 PASSED, 1 question resolved)
- ✅ S2.P3 (Refinement Phase) - COMPLETE (Acceptance criteria approved 2026-01-30 22:29 UTC)

**S2 Completion:** 2026-01-30
**Acceptance Criteria:** User approved
**Final Spec:** 12 requirements (all traced to epic/user decisions)
**Ready for Sync:** YES
<!-- END SECONDARY-E PROGRESS -->

---

<!-- BEGIN SECONDARY-G PROGRESS -->## Feature 08 Progress (Secondary-G)**Last Updated:** 2026-01-29 03:32**Current Stage:** S2.P2 (Specification Phase - Starting)**Current Step:** Awaiting S2.P2 phase transition prompt**Blockers:** None**Next Action:** Use "Starting S2.P2" prompt and begin Specification Phase**S2 Progress:**- ✅ S2.P1 (Research Phase) - COMPLETE (Gate 1 PASSED)- ⏳ S2.P2 (Specification Phase) - Starting- ⏳ S2.P3 (Refinement Phase) - Not Started**S2.P1 Completed:** 2026-01-29 03:30**Research:** 8 questions answered, 7,085 words documentation created<!-- END SECONDARY-G PROGRESS -->

---

<!-- BEGIN SECONDARY-H PROGRESS -->
## Feature 09 Progress (Secondary-H)

**Last Updated:** 2026-01-29 03:02
**Current Stage:** S2.P1 (Research Phase - Phase 0)
**Current Step:** Reading DISCOVERY.md (Phase 0 Step 0.1)
**Blockers:** None
**Next Action:** Read DISCOVERY.md, verify Discovery Context in spec.md

**S2 Progress:**
- ⏳ S2.P1 (Research Phase) - Phase 0 In Progress
- ⏳ S2.P2 (Specification Phase) - Not Started
- ⏳ S2.P3 (Refinement Phase) - Not Started
<!-- END SECONDARY-H PROGRESS -->

---

## Epic-Level Files

**Created in S1:**
- `EPIC_README.md` (this file)
- `EPIC_TICKET.md` - User-validated epic outcomes
- `epic_smoke_test_plan.md` - Initial test plan (will update in S4/S8.P2)
- `epic_lessons_learned.md` - Cross-feature insights
- `GUIDE_ANCHOR.md` - Resumption instructions
- `improve_configurability_of_scripts_notes.txt` - Original epic request
- `research/` - Epic-level research folder

**Feature Folders:**
- `feature_01_player_fetcher/`
- `feature_02_schedule_fetcher/`
- `feature_03_game_data_fetcher/`
- `feature_04_historical_compiler/`
- `feature_05_win_rate_simulation/`
- `feature_06_accuracy_simulation/`
- `feature_07_league_helper/`
- `feature_08_integration_test_framework/`
- `feature_09_documentation/`

## Feature Summary

### Feature 01: player_fetcher
**Folder:** `feature_01_player_fetcher/`
**Purpose:** Add argument support and debug logging to player data fetcher
**Status:** S1 complete
**Dependencies:** None (establishes patterns)

### Feature 02: schedule_fetcher
**Folder:** `feature_02_schedule_fetcher/`
**Purpose:** Add argument support and debug logging to schedule data fetcher
**Status:** S1 complete
**Dependencies:** None (benefits from Feature 01 patterns)

### Feature 03: game_data_fetcher
**Folder:** `feature_03_game_data_fetcher/`
**Purpose:** Enhance existing arguments and add debug logging to game data fetcher
**Status:** S1 complete
**Dependencies:** None

### Feature 04: historical_compiler
**Folder:** `feature_04_historical_compiler/`
**Purpose:** Enhance historical data compiler with debug logging and E2E mode
**Status:** S1 complete
**Dependencies:** None

### Feature 05: win_rate_simulation
**Folder:** `feature_05_win_rate_simulation/`
**Purpose:** Add E2E mode and debug logging to win rate simulation
**Status:** S1 complete
**Dependencies:** None

### Feature 06: accuracy_simulation
**Folder:** `feature_06_accuracy_simulation/`
**Purpose:** Add E2E mode and debug logging to accuracy simulation
**Status:** S1 complete
**Dependencies:** None (benefits from Feature 05 patterns)

### Feature 07: league_helper
**Folder:** `feature_07_league_helper/`
**Purpose:** Add argument support and E2E test flows to league helper
**Status:** S1 complete
**Dependencies:** None (benefits from all previous), Blocks Feature 08

### Feature 08: integration_test_framework
**Folder:** `feature_08_integration_test_framework/`
**Purpose:** Create integration test runners for all scripts
**Status:** S1 complete
**Dependencies:** Features 01-07, Blocks Feature 09

### Feature 09: documentation
**Folder:** `feature_09_documentation/`
**Purpose:** Update documentation with new arguments and testing workflows
**Status:** S1 complete
**Dependencies:** Feature 08

### Feature 10: refactor_player_fetcher (MISSED REQUIREMENT)
**Folder:** `feature_10_refactor_player_fetcher/`
**Purpose:** Refactor Feature 01 to use constructor parameter pattern instead of config override pattern
**Status:** S2 in progress
**Dependencies:** Feature 01 complete (architecture refactoring)
**Created:** 2026-01-31 (Missed requirement discovered during S8.P1 alignment)
**Sequence:** Between Feature 07 and Feature 08
**Priority:** Medium (establish consistent pattern before integration testing)

---

## Workflow Checklist

**S1 - Epic Planning:**
- [x] Epic folder created
- [x] Epic request file moved and renamed
- [x] EPIC_README.md created
- [ ] Epic analysis complete
- [ ] Feature breakdown proposed
- [ ] User approved feature breakdown
- [ ] Epic ticket created
- [ ] User validated epic ticket
- [ ] All feature folders created
- [ ] Initial `epic_smoke_test_plan.md` created
- [ ] `epic_lessons_learned.md` created
- [ ] `research/` folder created
- [ ] `GUIDE_ANCHOR.md` created
- [ ] Parallelization assessment completed
- [ ] Ready for S2 transition

**S2 - Feature Deep Dives:**
{Will be populated after S1 complete}

**S3 - Cross-Feature Sanity Check:**
{Will be populated after S2 complete}

**S4 - Epic Testing Strategy:**
- [x] epic_smoke_test_plan.md updated (all 10 features)
- [x] Integration points identified (7 integration points)
- [x] Epic success criteria defined (11 measurable criteria)
- [x] 🚨 Gate 4.5: User approval of test plan (PASSED 2026-02-01)

**S5-S8 - Feature Implementation:**
{Will be populated after S4 complete}

**S9 - Epic Final QC:**
{Will be populated after S5-S8 complete}

**S10 - Epic Cleanup:**
{Will be populated after S9 complete}

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

| Timestamp | Stage | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|
| - | - | - | - | - |

**Rule:** If you deviate from guide, DOCUMENT IT HERE immediately.

No deviations from guides yet.

---

## Epic Completion Summary

{This section will be filled out in S10}

---

<!-- BEGIN SECONDARY-F PROGRESS -->
## Feature 07 Progress (Secondary-F)

**Last Updated:** 2026-01-30 23:16
**Current Stage:** S2 COMPLETE
**Current Step:** Awaiting Primary S3/S4 (Cross-Feature Sanity Check)
**Blockers:** None
**Next Action:** Wait for Primary to signal S3/S4 complete

**S2 Progress:**
- ✅ S2.P1 (Research Phase) - COMPLETE (Gate 1 PASSED)
- ✅ S2.P2 (Specification Phase) - COMPLETE (Gate 2 PASSED)
- ✅ S2.P3 (Refinement Phase) - COMPLETE (User approval received)

**S2 Completion Summary:**
- Completion Date: 2026-01-30 23:16
- Requirements: 6 (all with traceability)
- Questions Resolved: 5 (all user-approved)
- Acceptance Criteria: USER APPROVED
- Ready for S3: Yes
<!-- END SECONDARY-F PROGRESS -->
