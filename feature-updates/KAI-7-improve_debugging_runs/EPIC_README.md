# Epic: improve_debugging_runs

**Created:** 2026-01-20
**Status:** IN PROGRESS
**Total Features:** 3

---

## Quick Reference Card (Always Visible)

**Current Stage:** Stage 1 - Epic Planning (Complete)
**Active Guide:** `guides_v2/stages/s2/s2_feature_deep_dive.md`
**Last Guide Read:** 2026-01-20 12:00

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
  ↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```

**You are here:** S1 Complete, Ready for S2

**Critical Rules for Next Stage (S2):**
1. Read S2 guide before starting each feature
2. Complete S2.P1 Research, S2.P2 Specification, S2.P3 Refinement for each feature
3. User approves checklist.md (Gate 3) before proceeding
4. Do NOT mark checklist items as resolved autonomously

**Before Proceeding to S2:**
- [x] Discovery complete and approved
- [x] Epic ticket validated
- [x] Feature folders created
- [x] Initial specs with Discovery Context created

---

## Agent Status

**Last Updated:** 2026-01-20 12:00
**Current Stage:** Stage 1 - Epic Planning (Complete)
**Current Phase:** TRANSITION
**Current Step:** S1 Complete - Ready for S2
**Current Guide:** `stages/s1/s1_epic_planning.md`
**Guide Last Read:** 2026-01-20 12:00

**Critical Rules from Guide:**
- S1 complete when all structure created
- Feature folders and specs ready for S2
- Next: Start S2 with Feature 01

**Progress:** 6/6 steps complete
**Next Action:** Begin S2 - Feature Deep Dive for Feature 01
**Blockers:** None

---

## Initial Scope Assessment

**Epic Size:** MEDIUM (3-5 features expected)
**Complexity:** Medium - Requires understanding interactive components and creating non-interactive wrappers
**Risk Level:** Low - Additive changes, no modification to existing logic

**Components Identified:**

| Component | Entry Point | Current State | Interactive? |
|-----------|-------------|---------------|--------------|
| League Helper (4 modes) | `run_league_helper.py` | Menu-driven | YES |
| Player Data Fetcher | `run_player_fetcher.py` | TBD | TBD |
| Win Rate Simulation | `run_win_rate_simulation.py` | CLI with modes | Partial |
| Accuracy Simulation | `run_accuracy_simulation.py` | CLI with args | NO |
| Game Data Fetcher | `run_game_data_fetcher.py` | CLI with args | NO |
| Schedule Data Fetcher | `run_schedule_fetcher.py` | Async CLI | NO |

**Key Observations:**
1. Win Rate and Accuracy Sims already have CLI args for single-run testing
2. League Helper is the most complex - 4 interactive modes
3. Data fetchers already have CLI args, may just need validation wrappers

---

## Epic Overview

**Epic Goal:**
Create automated debug/test runs for each script to make smoke testing easier, particularly enabling agents to test independently without user interaction.

**Epic Scope:**
Create debugging versions of all major scripts that can run non-interactively with log output.

**Key Outcomes:**
1. Automated test runs that create log files
2. Non-interactive smoke testing for all major components
3. Agents can validate functionality independently

**Original Request:** `improve_debugging_runs_notes.txt`

---

## Epic Progress Tracker

**Overall Status:** 0/3 features complete

| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_debug_infrastructure | Done | - | - | - | - | - | - | - | - |
| feature_02_league_helper_debug | Done | - | - | - | - | - | - | - | - |
| feature_03_unified_debug_runner | Done | - | - | - | - | - | - | - | - |

**S9 - Epic Final QC:** Not Started
**S10 - Epic Cleanup:** Not Started

---

## Feature Summary

### Feature 01: debug_infrastructure
**Folder:** `feature_01_debug_infrastructure/`
**Purpose:** Shared debug utilities, logging setup, and configuration
**Status:** S1 Complete - Ready for S2
**Dependencies:** None (foundation feature)
**Size:** SMALL

### Feature 02: league_helper_debug
**Folder:** `feature_02_league_helper_debug/`
**Purpose:** Non-interactive debug mode for all 5 League Helper modes
**Status:** S1 Complete - Ready for S2
**Dependencies:** Feature 01
**Size:** MEDIUM

### Feature 03: unified_debug_runner
**Folder:** `feature_03_unified_debug_runner/`
**Purpose:** Single script to run all debug tests with aggregated reporting
**Status:** S1 Complete - Ready for S2
**Dependencies:** Features 01 and 02
**Size:** MEDIUM

---

## Bug Fix Summary

**Bug Fixes Created:** 0

No bug fixes created yet

---

## Epic-Level Files

**Created in S1:**
- `EPIC_README.md` (this file)
- `DISCOVERY.md` - Discovery findings and user answers
- `EPIC_TICKET.md` - Epic acceptance criteria and success indicators
- `epic_smoke_test_plan.md` - How to test the complete epic
- `epic_lessons_learned.md` - Lessons learned throughout epic

**Feature Folders:**
- `feature_01_debug_infrastructure/` - Shared debug utilities
- `feature_02_league_helper_debug/` - League Helper debug mode
- `feature_03_unified_debug_runner/` - Unified debug runner

---

## Workflow Checklist

**S1 - Epic Planning:**
- [x] Git branch created (epic/KAI-7)
- [x] EPIC_TRACKER.md updated
- [x] Epic folder created
- [x] `EPIC_README.md` created (this file)
- [x] DISCOVERY.md created and user-approved
- [x] Feature breakdown approved
- [x] Epic ticket created and validated
- [x] Feature folders created
- [x] `epic_smoke_test_plan.md` created
- [x] `epic_lessons_learned.md` created

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
- [ ] Feature 01 (debug_infrastructure): S5→S6→S7→S8 complete
- [ ] Feature 02 (league_helper_debug): S5→S6→S7→S8 complete
- [ ] Feature 03 (unified_debug_runner): S5→S6→S7→S8 complete

**S9 - Epic Final QC:**
- [ ] Epic smoke testing passed
- [ ] Epic QC rounds passed
- [ ] Epic PR review passed
- [ ] End-to-end validation passed

**S10 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Documentation verified complete
- [ ] Guides updated based on lessons learned
- [ ] Final commits made
- [ ] Epic moved to `feature-updates/done/`

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide

| Timestamp | Stage | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|

No deviations from guides

---

## Epic Completion Summary

{This section filled out in S10}
