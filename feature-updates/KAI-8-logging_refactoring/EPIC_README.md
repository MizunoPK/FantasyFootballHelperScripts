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
**Last Updated:** 2026-02-12 06:20
**Current Stage:** S9.P2 COMPLETE - Ready for S9.P3 (User Testing)
**Current Phase:** EPIC_QC_COMPLETE
**Current Step:** S9.P2 complete - 3 consecutive clean rounds achieved (ZERO issues found)
**Previous Guide:** stages/s9/s9_p2_epic_qc_rounds.md (COMPLETE)
**Current Guide:** stages/s9/s9_p3_user_testing.md (NEXT - not yet read)
**Guide Last Read:** 2026-02-12 06:18 (s9_p2_epic_qc_rounds.md)
**Validation Results:** 3 rounds, 0 issues found, 0 issues fixed, 100% quality
**Clean Round Counter:** 3 (COMPLETE)

**S8.P2 Results (Feature 05):**
- Reviewed Feature 05 actual implementation (run_win_rate_simulation.py, simulation/win_rate/ modules)
- Compared to epic_smoke_test_plan.md: Test 2.4 (CLI flag) and Scenario 3.4 (E2E) already accurate
- No new integration points discovered (uses Feature 01's LineBasedRotatingHandler as expected)
- No edge cases requiring epic-level testing (feature unit tests handle edge cases)
- Logger setup pattern (setup_logger() once, get_logger() in modules) is implementation detail
- **Decision:** Option A (NO CHANGE) - implementation matched expectations
- **Action:** Updated Update History table only (line 67 added)

**S8.P1 Results (Feature 05):**
- Feature 06 (historical_data_compiler_logging): ✅ Zero updates needed - spec correctly aligned with Feature 05 pattern
- Feature 07 (schedule_fetcher_logging): ✅ Updated - aligned logger setup pattern (entry script calls setup_logger() ONCE, modules call get_logger())
- Key insight: Feature 05 uses cleaner pattern than originally spec'd for Feature 07
- Significant rework assessment: NO features need return to S1/S2/S5 (all minor updates only)

**Feature 01 Status:**
- ✅ S2-S8 COMPLETE (all stages done)

**Feature 02 Status:**
- ✅ S2-S8 COMPLETE (all stages done)

**Feature 03 Status:**
- ✅ S2-S8 COMPLETE (all stages done)
- Implementation: 38/38 requirements, 13 tasks, 6 phases
- Testing: 330/330 tests passing (100%)
- Quality: 0 issues (smoke testing, 3 QC rounds, PR review)
- S8: Cross-feature alignment complete (4 features reviewed, 0 updates needed)

**Feature 04 Status:**
- ✅ S2-S8 COMPLETE (all stages done)
- Implementation: 10 tasks across 4 phases (CLI flag + logging enhancements)
- Testing: 2581/2581 tests passing (100%, includes 58 Feature 04-specific tests)
- Quality: 67 issues found and fixed in PR review (test coverage gap, imports, documentation)
- S7: Smoke testing passed, 3 QC rounds passed (0 issues), PR review passed (2 consecutive clean rounds)
- Production-ready: Feature 04 fully validated and complete

**Feature 05 Status:**
- ✅ S2-S8 COMPLETE (spec approved, implemented, tested, aligned, epic testing updated)
- Implementation: 33/33 requirements (CLI flag + log quality audits)
- Testing: 2621/2621 tests passing (100%, includes 44 Feature 05-specific tests)
- Quality: 0 issues (6 consecutive clean validation rounds)
- S8.P1: Reviewed Features 06-07 specs, Feature 07 updated for logger pattern alignment
- S8.P2: Epic testing plan reviewed, no new scenarios needed

**Feature 06 Status:**
- ✅ S2-S8 COMPLETE (spec approved, implemented, tested, aligned, epic testing updated)
- Implementation: 15/15 requirements (CLI flag + log quality audits)
- Testing: 2639/2639 tests passing (100%, includes 18 Feature 06-specific tests)
- Quality: 0 issues (3 smoke test parts, 6 QC rounds, 3 PR review rounds)
- S8.P1: Reviewed Feature 07 spec, updated for error parsing WARNING alignment
- S8.P2: Epic testing plan reviewed, no new scenarios needed (implementation matched expectations)

**Feature 07 Status:**
- ✅ S2-S8 COMPLETE (all stages passed, production-ready)
- ✅ S8.P1 COMPLETE (twice - aligned against Feature 05 AND Feature 06 before implementation)
  - First alignment (Feature 05): Logger setup pattern (get_logger() in modules)
  - Second alignment (Feature 06): Error parsing promoted to WARNING level
- ✅ S8.P2 COMPLETE (epic testing plan reviewed and updated)
  - Reviewed actual implementation (run_schedule_fetcher.py, ScheduleFetcher.py)
  - Decision: NO CHANGE (implementation matched test plan expectations)
  - Updated Update History table in epic_smoke_test_plan.md
  - Test 2.6 and Scenario 3.6 remain accurate
- Testing: 2658/2658 tests passing (100%, includes 37 Feature 07-specific tests)
- S7 Validation: All 3 rounds CLEAN (S7.P1 smoke test, S7.P2 feature QC, S7.P3 PR review)
- Quality: Zero-defect implementation (0 issues found in 6 validation rounds total)
- Production-ready: Feature 07 fully validated and complete

**Progress:** 7/7 features complete S2-S8 (ALL features done)
**Next Action:** S9 (Epic Final QC) - Read stages/s9/s9_p1_epic_smoke_testing.md
**S8 Summary (Feature 07 - FINAL):**
- **S8.P1:** SKIPPED - No remaining features to align (all 7 complete)
- **S8.P2:** Reviewed epic_smoke_test_plan.md, updated Update History table
  - Feature 07 implementation matched test plan expectations (zero changes needed)
  - All 7 features now reviewed in S8.P2
  - Test plan current and ready for S9 execution
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

**Overall Status:** 7 features (S1 ✅, S2 ✅, S3 ✅)

**S1 - Epic Planning:** ✅ COMPLETE
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

**Total Features:** 7 (1 foundation + 6 per-script implementations)

### Feature 01: core_logging_infrastructure (Foundation)
**What:** Custom LineBasedRotatingHandler with 500-line rotation, centralized logs/ folder structure, max 50 files cleanup, .gitignore update, LoggingManager integration
**Key Components:**
- `utils/LineBasedRotatingHandler.py` (new class, ~150 lines)
- `utils/LoggingManager.py` (modified setup_logger and path generation)
- `.gitignore` line 71 (add `logs/`)
**Integration Points:** Provides infrastructure for Features 02-07 via setup_logger() API
**Dependencies:** None (foundation must complete first)

### Feature 02: league_helper_logging
**What:** --enable-log-file CLI flag via subprocess wrapper (sys.argv forwarding), log quality improvements to 316 logger calls across 17 league_helper modules
**Key Components:**
- `run_league_helper.py` (add argparse, forward to subprocess)
- `league_helper/LeagueHelperManager.py` (add argparse, wire to setup_logger)
- 17 module files (improve DEBUG/INFO log quality)
**Logger Name:** "league_helper" → creates logs/league_helper/
**Dependencies:** Feature 01 (requires LineBasedRotatingHandler)

### Feature 03: player_data_fetcher_logging
**What:** --enable-log-file CLI flag via subprocess wrapper, log quality improvements to player-data-fetcher modules
**Key Components:**
- `run_player_fetcher.py` (add argparse, forward to subprocess)
- `player_data_fetcher.py` (add argparse, wire to setup_logger)
- Player data fetcher modules (improve log quality)
**Logger Name:** "player_data_fetcher" → creates logs/player_data_fetcher/
**Dependencies:** Feature 01

### Feature 04: accuracy_sim_logging
**What:** --enable-log-file CLI flag (direct entry, already has argparse), log quality improvements to accuracy simulation modules
**Key Components:**
- `run_accuracy_simulation.py` (add flag, wire to setup_logger)
- `simulation/accuracy/` modules (improve log quality)
**Logger Name:** "accuracy_simulation" → creates logs/accuracy_simulation/
**Dependencies:** Feature 01

### Feature 05: win_rate_sim_logging
**What:** --enable-log-file CLI flag (direct entry, replace hardcoded constant), log quality improvements to win rate simulation modules
**Key Components:**
- `run_win_rate_simulation.py` (add argparse, replace LOG_FILE_PATH constant)
- `simulation/win_rate/` modules (improve log quality)
**Logger Name:** "win_rate_simulation" → creates logs/win_rate_simulation/
**Dependencies:** Feature 01

### Feature 06: historical_data_compiler_logging
**What:** --enable-log-file CLI flag (direct entry), log quality improvements to historical data compiler modules
**Key Components:**
- `compile_historical_data.py` (add argparse, wire to setup_logger)
- Historical data compiler modules (improve log quality)
**Logger Name:** "historical_data_compiler" → creates logs/historical_data_compiler/
**Dependencies:** Feature 01

### Feature 07: schedule_fetcher_logging
**What:** --enable-log-file CLI flag (async main entry), log quality improvements to schedule fetcher modules
**Key Components:**
- `run_schedule_fetcher.py` (add argparse to async main, wire to setup_logger)
- Schedule fetcher modules (improve log quality)
**Logger Name:** "schedule_fetcher" → creates logs/schedule_fetcher/
**Dependencies:** Feature 01

---

## Epic-Level Architecture

### Architectural Pattern: Foundation + Per-Script Integration

**Design Decision:** Split epic into 1 foundation feature + 6 per-script features (not monolithic)
- **Rationale:** Enables parallel S2 work (Group 2 features in parallel after Group 1), modular implementation, isolated testing
- **Alternative considered:** Single monolithic feature (rejected due to 60 files, 939 logger calls - too large)

### Integration Contract (Feature 01 → Features 02-07)

**Contract 1: Logger Name = Folder Name**
- Each script uses unique snake_case logger name matching its folder name
- Example: "league_helper" creates logs/league_helper/
- No validation enforced (trusts callers per user decision Q4)

**Contract 2: log_file_path=None**
- Scripts do NOT specify custom paths
- LoggingManager auto-generates: logs/{logger_name}/{logger_name}-{YYYYMMDD_HHMMSS}.log

**Contract 3: log_to_file from CLI**
- File logging OFF by default (opt-in via --enable-log-file flag)
- Scripts wire CLI flag to setup_logger(log_to_file=args.enable_log_file)

### Data Flow

```
User runs script with --enable-log-file
  ↓
Script entry point (argparse)
  ↓
Wire flag → setup_logger(log_to_file=True)
  ↓
LoggingManager creates LineBasedRotatingHandler
  ↓
Handler writes to logs/{script_name}/{script_name}-{timestamp}.log
  ↓
Rotation at 500 lines → new timestamped file
  ↓
Cleanup when 51st file created → delete oldest
```

### Scope Boundaries

**In Scope:**
- 6 main entry scripts (league_helper, player-data-fetcher, accuracy_sim, win_rate_sim, historical_data_compiler, schedule_fetcher)
- 939 total logger.debug/info calls across 60 files
- Centralized logs/ folder with script-specific subfolders
- CLI toggle for file logging (OFF by default)
- Log quality improvements (DEBUG: tracing, INFO: user awareness)

**Out of Scope:**
- Other scripts (run_simulation.py, run_scores_fetcher.py) - not included per Discovery
- WARNING/ERROR/CRITICAL log levels (not part of epic scope)
- Custom log rotation intervals (hardcoded 500 lines per user decision Q2)
- Custom max files limits (hardcoded 50 files per user decision Q2)
- Log file compression or archival
- Remote log shipping or centralized logging servers

### Key Constraints

1. **Backward Compatibility:** LoggingManager.setup_logger() signature unchanged (Features 02-07 work without modification)
2. **File Logging Default:** OFF (users must opt-in via --enable-log-file)
3. **Hardcoded Limits:** 500 lines, 50 files (not configurable per user decision Q2)
4. **No Validation:** Trusts callers for logger names and paths (per user decisions Q4, Q6)
5. **Append Mode:** Always append to existing log files if script re-run (per user decision Q3)

## Feature Tracking

| Feature | S2 Complete | S4 Complete | S7 Complete | S8 Complete | Status |
|---------|-------------|-------------|-------------|-------------|--------|
| 01: core_logging_infrastructure | ☑️ | ☑️ | ☑️ | ☑️ | ✅ COMPLETE (S2-S8 done, production-ready) |
| 02: league_helper_logging | ☑️ | ☐ | ☐ | ☑️ | SPEC UPDATED (ready for S4 after Feature 01 S8.P2) |
| 03: player_data_fetcher_logging | ☑️ | ☐ | ☐ | ☑️ | SPEC UPDATED (ready for S4 after Feature 01 S8.P2) |
| 04: accuracy_sim_logging | ☑️ | ☐ | ☐ | ☑️ | SPEC UPDATED (ready for S4 after Feature 01 S8.P2) |
| 05: win_rate_sim_logging | ☑️ | ☐ | ☐ | ☑️ | SPEC UPDATED (ready for S4 after Feature 01 S8.P2) |
| 06: historical_data_compiler_logging | ☑️ | ☐ | ☐ | ☑️ | SPEC UPDATED (ready for S4 after Feature 01 S8.P2) |
| 07: schedule_fetcher_logging | ☑️ | ☐ | ☐ | ☑️ | SPEC UPDATED (ready for S4 after Feature 01 S8.P2) |

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
- [x] Wave 1 (Group 1): Feature 01 completed S2.P1 + S2.P2
- [x] Wave 2 (Group 2): Features 02-07 completed S2.P1 in parallel
- [x] S2.P2 cross-feature alignment: 21 pairwise comparisons, 0 conflicts
- [x] Validation Loop passed (3 consecutive clean rounds)
- [x] All 7 features have user-approved specs
- [x] Time: 4 hours total (vs 14h sequential) - 71% time savings

**S3 - Epic Planning & Approval:**
- [x] S3.P1: Epic Testing Strategy complete (epic_smoke_test_plan.md updated with 33 scenarios)
- [x] S3.P2: Epic Documentation Refinement complete (EPIC_README.md enhanced with feature summaries and architecture)
- [x] S3.P3: Gate 4.5 User Approval obtained (2026-02-06)
- [x] Cross-feature comparison complete (done in S2.P2: 21 pairs, 0 conflicts)
- [x] Validation Loops passed (S3.P1: 3 clean rounds, S3.P2: 3 clean rounds)
- [x] All features aligned and conflict-free

**S4 - Feature Testing Strategy (Per-Feature):**
- [ ] Feature 01: test_strategy.md created
- [ ] Feature 02: test_strategy.md created
- [ ] Feature 03: test_strategy.md created
- [ ] Feature 04: test_strategy.md created
- [ ] Feature 05: test_strategy.md created
- [ ] Feature 06: test_strategy.md created
- [ ] Feature 07: test_strategy.md created
- [ ] All features have >90% test coverage planned

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
