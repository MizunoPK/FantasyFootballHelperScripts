## Epic: Architectural Refactoring of Configuration Management

**Created:** 2026-02-13
**Status:** IN PROGRESS
**Total Features:** TBD (to be determined in Discovery Phase)

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 1 - Epic Planning
**Active Guide:** `guides_v2/stages/s1/s1_epic_planning.md`
**Last Guide Read:** 2026-02-13 (full guide read complete)

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
  ↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```

**You are here:** ➜ Stage 1 (Step 1 complete, starting Step 2)

**Critical Rules for S1:**
1. CREATE GIT BRANCH BEFORE ANY CHANGES (Step 1.0) - ✅ COMPLETE
2. DISCOVERY PHASE IS MANDATORY (Step 3) - Every epic must go through Discovery
3. DISCOVERY LOOP UNTIL 3 CONSECUTIVE CLEAN ITERATIONS - Continue until no questions
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
**Last Updated:** 2026-02-13 15:45
**Current Stage:** Stage 1 - Epic Planning
**Current Phase:** PLANNING
**Current Step:** Step 1 complete (Initial Setup), starting Step 2 (Epic Analysis)
**Current Guide:** `stages/s1/s1_epic_planning.md`
**Guide Last Read:** 2026-02-13 15:45

**Critical Rules from Guide:**
- "Create git branch BEFORE any changes" - ✅ COMPLETE (epic/KAI-10 created)
- "Discovery is MANDATORY for every epic"
- "Discovery Loop continues until 3 consecutive clean iterations"
- "User must approve feature breakdown before epic ticket"
- "Epic ticket becomes immutable after user validation"

**Progress:** 1/6 S1 steps complete (Initial Setup done)
**Next Action:** Step 2 - Epic Analysis (read epic request, identify goals, estimate scope)
**Blockers:** None

---

## Epic Overview

**Epic Goal:**
Establish consistent, maintainable configuration management pattern across all 7 runner scripts through dependency injection, comprehensive CLI arguments, E2E test modes, and integration test framework.

**Epic Scope:**
- Refactor all 7 scripts to constructor parameter pattern (dependency injection)
- Add CLI arguments for every configurable setting (~60+ args total)
- Implement fast E2E test modes (≤3 minutes per script)
- Create integration test framework (7 test runners + master runner)
- Single source of truth (CLI argparse defaults only, no config duplication)

**Key Outcomes:**
1. All 7 runner scripts use constructor parameter pattern (not direct config imports)
2. 60+ CLI arguments expose all configurable settings
3. Each script completes E2E test in ≤180 seconds
4. 100% unit test pass rate maintained (2,754 tests)
5. Integration test framework validates all argument combinations

**Original Request:** `architectural_refactoring_configuration_management_notes.txt` (updated and validated 2026-02-13)

**Post-KAI-9 Status:**
- Scope reduced by ~20% (KAI-9 removed 9 config constants from player-data-fetcher)
- Feature 01 scope: 23 args → 14 args (-39%)
- Estimated effort: 30-50h (reduced from 40-60h)
- Epic size: LARGE (reduced from VERY LARGE)

---

## Epic Progress Tracker

**Overall Status:** 0/TBD features complete (features TBD in Discovery Phase)

| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| TBD | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |

**Legend:**
- ✅ = Complete
- ◻️ = Not started or in progress

**S9 - Epic Final QC:** ◻️ NOT STARTED
- Epic smoke testing passed: ◻️
- Epic QC rounds passed: ◻️
- Epic PR review passed: ◻️
- End-to-end validation passed: ◻️
- Date completed: Not complete

**S10 - Epic Cleanup:** ◻️ NOT STARTED
- Final commits made: ◻️
- Epic moved to done/ folder: ◻️
- Date completed: Not complete

---

## Feature Summary

*Features will be defined during Discovery Phase (S1 Step 3)*

*Expected features based on proposal:*
- Feature 01: player_fetcher (14 CLI args, constructor pattern, debug/E2E modes)
- Feature 02: schedule_fetcher (5 CLI args, debug/E2E modes)
- Feature 03: game_data_fetcher (enhance existing argparse, debug/E2E modes)
- Feature 04: historical_compiler (enhance existing argparse, debug/E2E modes)
- Feature 05: win_rate_simulation (add --e2e-test flag)
- Feature 06: accuracy_simulation (add --e2e-test flag)
- Feature 07: league_helper (12 CLI args, mode manager refactoring, debug/E2E modes)
- Feature 08: integration_test_framework (7 test runners + master runner)
- Feature 09: documentation (README, ARCHITECTURE, integration testing guide)
- Feature 10: refactor_player_fetcher (CRITICAL - establishes architectural pattern)

*Note: Final feature breakdown will be determined through Discovery Phase research and user approval*

---

## Feature Dependency Groups (S2 Only)

*To be determined after Discovery Phase and feature breakdown approval*

---

## Epic-Level Files

**Created in S1:**
- `EPIC_README.md` (this file) - ✅ Created
- `architectural_refactoring_configuration_management_notes.txt` (moved from feature-updates/) - ✅ Created
- `epic_smoke_test_plan.md` - ◻️ Not created yet
- `epic_lessons_learned.md` - ◻️ Not created yet
- `DISCOVERY.md` - ◻️ Not created yet (Step 3)
- `EPIC_TICKET.md` - ◻️ Not created yet (Step 4.6)
- `GUIDE_ANCHOR.md` - ◻️ Not created yet (Step 5.5)
- `research/` folder - ◻️ Not created yet (Step 5.4)

**Feature Folders:**
*To be created in Step 5 after Discovery approval*

---

## Workflow Checklist

**S1 - Epic Planning:**
- [x] Git branch created (`epic/KAI-10`)
- [x] EPIC_TRACKER.md updated
- [x] Epic folder created
- [x] Epic request file moved
- [x] `EPIC_README.md` created (this file)
- [ ] Epic Analysis complete (Step 2)
- [ ] Discovery Phase complete (Step 3) - MANDATORY
- [ ] Feature breakdown approved by user (Step 4)
- [ ] Epic ticket created and validated (Steps 4.6-4.7)
- [ ] All feature folders created (Step 5)
- [ ] `epic_smoke_test_plan.md` created (Step 5.2)
- [ ] `epic_lessons_learned.md` created (Step 5.3)
- [ ] `research/` folder created (Step 5.4)
- [ ] `GUIDE_ANCHOR.md` created (Step 5.5)
- [ ] Parallelization assessment completed (Step 5.8-5.9)
- [ ] User chose parallelization mode for S2

**S2 - Feature Deep Dives:**
- [ ] ALL features have `spec.md` complete
- [ ] ALL features have `checklist.md` resolved
- [ ] ALL feature `README.md` files created

**S3 - Cross-Feature Sanity Check:**
- [ ] All specs compared systematically
- [ ] Conflicts resolved
- [ ] User sign-off obtained

**S4 - Epic Testing Strategy:**
- [ ] `epic_smoke_test_plan.md` updated based on deep dives
- [ ] Integration points identified
- [ ] Epic success criteria defined

**S5-S8 - Feature Implementation:**
- [ ] Feature loop not started yet

**S9 - Epic Final QC:**
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] Epic QC rounds passed (all 3 rounds)
- [ ] Epic PR review passed (all 11 categories)
- [ ] End-to-end validation vs original request passed

**S10 - Epic Cleanup:**
- [ ] All unit tests passing (100% - currently 2,754 tests)
- [ ] Documentation verified complete
- [ ] Guides updated based on lessons learned (if needed)
- [ ] Final commits made
- [ ] Epic moved to `feature-updates/done/KAI-10-architectural_refactoring_configuration_management/`

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

| Timestamp | Stage | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|
| No deviations yet | - | - | - | - |

**Rule:** If you deviate from guide, DOCUMENT IT HERE immediately.

---

## Epic Completion Summary

*This section will be filled out in S10*
