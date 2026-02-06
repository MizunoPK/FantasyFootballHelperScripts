# Epic: logging_refactoring

**Created:** 2026-02-06
**Status:** IN PROGRESS
**Total Features:** 7 (determined after Discovery Phase)

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 1 - Epic Planning
**Active Guide:** `guides_v2/stages/s1/s1_epic_planning.md`
**Last Guide Read:** 2026-02-06 18:50

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
  ↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```

**You are here:** ➜ Stage 1

**Critical Rules for Current Stage:**
1. CREATE GIT BRANCH BEFORE ANY CHANGES (Step 1.0) ✅ COMPLETE
2. DISCOVERY PHASE IS MANDATORY (Step 3)
3. DISCOVERY LOOP UNTIL 3 CONSECUTIVE CLEAN ITERATIONS
4. USER MUST APPROVE feature breakdown before creating epic ticket
5. CREATE EPIC TICKET and get user validation (Steps 4.6-4.7)

**Before Proceeding to Next Step:**
- [x] Read guide: `guides_v2/stages/s1/s1_epic_planning.md`
- [x] Acknowledge critical requirements
- [x] Verify prerequisites from guide
- [x] Update this Quick Reference Card

---

## Agent Status

**Debugging Active:** NO
**Last Updated:** 2026-02-06 21:15
**Current Stage:** S1 Complete → Guide Analysis Complete
**Current Phase:** GUIDE GAP ANALYSIS
**Current Step:** Completed comprehensive analysis of group-based S2 parallelization gaps
**Current Guide:** Multiple guides analyzed (s1, s2, s3, parallel work guides)
**Guide Last Read:** 2026-02-06 21:00 (s1, s2, s3 guides)

**Critical Rules:**
- **S2 GROUP-BASED:** Group 1 (F01) completes S2 first, then Group 2 (F02-07) does S2 in parallel
- After S2 complete: Groups don't matter, proceed with S3 (epic-level) then S4, then S5-S8 (feature-sequential)
- **GUIDE ANALYSIS COMPLETE:** 8 gaps identified preventing group-based S2 parallelization
- **ANALYSIS DOCUMENT:** `research/GROUP_BASED_S2_PARALLELIZATION_INTENDED_FLOW.md` (31 pages, comprehensive)

**Progress:** S1 COMPLETE, guide gap analysis COMPLETE
**Next Action:** Await user direction (proceed with S2 or address guide gaps first)
**Blockers:** None

---

## Epic Overview

**Epic Goal:**
Improve logging infrastructure across all major scripts with centralized log management, automated rotation, quality improvements to Debug/Info logs, and CLI toggle for file logging.

**Epic Scope:**
- Root-level logs/ folder with script-specific subfolders
- Timestamped .log files with 500-line cap
- Automatic log rotation (max 50 logs per folder, auto-delete oldest)
- Quality improvements to Debug and Info level logs
- CLI argument to toggle file logging on/off
- .gitignore update for logs folder

**Key Outcomes:**
1. Centralized log management with organized folder structure
2. Automated log rotation preventing disk space issues
3. Improved log quality for better debugging and user awareness
4. User control over file logging via CLI

**Original Request:** `feature-updates/KAI-8-logging_refactoring/logging_refactoring_notes.txt`

---

## Initial Scope Assessment

**Epic Size:** MEDIUM (3-5 features expected)
**Complexity:** MEDIUM-HIGH (system-wide changes, subjective log quality evaluation)
**Risk Level:** MEDIUM (affects all logging infrastructure, but existing LoggingManager reduces risk)

**Major Components Affected:**
1. utils/LoggingManager.py - Core logging infrastructure (rotation strategy, folder organization)
2. Main entry scripts (6+ scripts) - CLI argument integration:
   - run_league_helper.py
   - run_player_fetcher.py (player-data-fetcher)
   - run_accuracy_simulation.py (accuracy_sim)
   - run_win_rate_simulation.py (win_rate_sim)
   - run_schedule_fetcher.py (schedule-data-fetcher)
   - run_game_data_fetcher.py (likely historical_data_compiler)
3. Multiple modules - Log quality improvements (league_helper/, simulation/, utils/, player-data-fetcher/)
4. .gitignore - Add logs/ folder
5. tests/utils/test_LoggingManager.py - Update tests

**Existing Patterns to Leverage:**
- LoggingManager already provides centralized logging setup
- Uses RotatingFileHandler (currently size-based, needs line-based)
- run_accuracy_simulation.py has --log-level CLI precedent
- Auto-generated timestamped log files (YYYYMMDD format)

**Expected Feature Breakdown (preliminary):**
1. LoggingManager infrastructure (folder structure, line-based rotation, max 50 logs cleanup)
2. CLI integration across all scripts (toggle file logging on/off)
3. Log quality audit and improvements (Debug/Info logs system-wide)
4. .gitignore update (may bundle with Feature 1)

**Time-Box for Discovery:** 2-3 hours (MEDIUM epic)

---

## Epic Progress Tracker

**Overall Status:** 0 features (to be determined after Discovery Phase)

**S1 - Epic Planning:** 🔄 IN PROGRESS
- [x] Git branch created (epic/KAI-8)
- [x] EPIC_TRACKER.md updated
- [x] Epic folder created
- [x] Epic notes moved to epic folder
- [x] EPIC_README.md created (this file)
- [x] Epic Analysis complete (Step 2)
- [x] Discovery Phase complete (Step 3 - user approved)
- [x] Feature breakdown approved (Step 4 - 7 features)
- [x] Epic ticket validated (Step 4.6-4.7 - user approved)
- [ ] Epic structure created (Step 5)
- [ ] Transition to S2 (Step 6)

---

## Feature Summary

**Total Features:** 7

1. **Feature 01: core_logging_infrastructure** - Custom LineBasedRotatingHandler, centralized logs/ folder, 500-line rotation, max 50 files cleanup, .gitignore update
2. **Feature 02: league_helper_logging** - CLI flag and log quality for league_helper
3. **Feature 03: player_data_fetcher_logging** - CLI flag and log quality for player-data-fetcher
4. **Feature 04: accuracy_sim_logging** - CLI flag and log quality for accuracy_sim
5. **Feature 05: win_rate_sim_logging** - CLI flag and log quality for win_rate_sim
6. **Feature 06: historical_data_compiler_logging** - CLI flag and log quality for historical_data_compiler
7. **Feature 07: schedule_fetcher_logging** - CLI flag and log quality for schedule_fetcher

## Feature Tracking

| Feature | S2 Complete | S8.P2 Complete | Status |
|---------|-------------|----------------|--------|
| 01: core_logging_infrastructure | ☐ | ☐ | NOT STARTED |
| 02: league_helper_logging | ☐ | ☐ | NOT STARTED |
| 03: player_data_fetcher_logging | ☐ | ☐ | NOT STARTED |
| 04: accuracy_sim_logging | ☐ | ☐ | NOT STARTED |
| 05: win_rate_sim_logging | ☐ | ☐ | NOT STARTED |
| 06: historical_data_compiler_logging | ☐ | ☐ | NOT STARTED |
| 07: schedule_fetcher_logging | ☐ | ☐ | NOT STARTED |

## Feature Dependency Groups (S2 Only)

**Group-Based S2 Parallelization Strategy:**

**Group 1 (Foundation - S2 Sequential):**
- Feature 01: core_logging_infrastructure
- Dependencies: None
- **S2 Workflow:** Complete S2 alone FIRST
- **Why first:** Defines LineBasedRotatingHandler API and LoggingManager integration that Group 2 needs to reference in their specs

**Group 2 (Scripts - S2 Parallel after Group 1's S2):**
- Feature 02: league_helper_logging
- Feature 03: player_data_fetcher_logging
- Feature 04: accuracy_sim_logging
- Feature 05: win_rate_sim_logging
- Feature 06: historical_data_compiler_logging
- Feature 07: schedule_fetcher_logging
- Dependencies: Feature 01's spec (need to know setup_logger API to write their specs)
- **S2 Workflow:** After Group 1 completes S2, all 6 features do S2 in parallel
- **Why parallel:** Independent from each other, only need Group 1's spec as reference

**After S2:**
- Groups no longer matter
- S3, S4: Epic-level stages (all features together)
- S5-S8: Standard feature-by-feature sequential workflow
- S9, S10: Epic-level stages

**S2 Time Savings:**
- Sequential S2 (all 7): 7 × 2h = 14 hours
- Group-based S2: Group 1 (2h) + Group 2 parallel (2h) = 4 hours
- **Savings: 10 hours (71% reduction in S2 time)**

---

## Epic-Level Files

**Created in S1:**
- `EPIC_README.md` (this file) ✅
- `logging_refactoring_notes.txt` (original request) ✅
- `DISCOVERY.md` ✅
- `EPIC_TICKET.md` ✅
- `epic_smoke_test_plan.md` ✅
- `epic_lessons_learned.md` ✅
- `GUIDE_ANCHOR.md` ✅
- `research/` folder ✅

**Feature Folders Created (S1 Step 5):**
- `feature_01_core_logging_infrastructure/` ✅ (README.md, spec.md, checklist.md, lessons_learned.md)
- `feature_02_league_helper_logging/` ✅ (README.md, spec.md, checklist.md, lessons_learned.md)
- `feature_03_player_data_fetcher_logging/` ✅ (README.md, spec.md, checklist.md, lessons_learned.md)
- `feature_04_accuracy_sim_logging/` ✅ (README.md, spec.md, checklist.md, lessons_learned.md)
- `feature_05_win_rate_sim_logging/` ✅ (README.md, spec.md, checklist.md, lessons_learned.md)
- `feature_06_historical_data_compiler_logging/` ✅ (README.md, spec.md, checklist.md, lessons_learned.md)
- `feature_07_schedule_fetcher_logging/` ✅ (README.md, spec.md, checklist.md, lessons_learned.md)

---

## Workflow Checklist

**S1 - Epic Planning:**
- [x] Git branch created (epic/KAI-8)
- [x] EPIC_TRACKER.md updated
- [x] Epic folder created
- [x] Epic notes moved
- [x] EPIC_README.md created
- [x] Epic Analysis complete
- [x] Discovery Phase complete
- [x] Feature breakdown approved by user
- [x] Epic ticket created and user-validated
- [x] All feature folders created (7 features, 28 files)
- [x] Initial `epic_smoke_test_plan.md` created
- [x] `epic_lessons_learned.md` created
- [x] `research/` folder created
- [x] `GUIDE_ANCHOR.md` created
- [x] Feature Dependency Analysis complete (Step 5.7.5)
- [x] Parallelization assessment completed (Step 5.8-5.9)
- [x] User chose: GROUP-BASED PARALLEL WORK (Group 1 sequential, Group 2 parallel with 6 agents)
- [x] Lesson learned documented: Group-based parallelization for dependencies

**S2 - Feature Deep Dives:**
- Not started

**S3 - Cross-Feature Sanity Check:**
- Not started

**S4 - Epic Testing Strategy:**
- Not started

**S5-S8 - Feature Implementation:**
- Not started

**S9 - Epic Final QC:**
- Not started

**S10 - Epic Cleanup:**
- Not started

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

No deviations from guides

---

## Epic Completion Summary

{This section filled out in S10}
