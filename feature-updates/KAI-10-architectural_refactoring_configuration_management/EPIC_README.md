## Epic: architectural_refactoring_configuration_management

**Created:** 2026-02-18
**Status:** IN PROGRESS
**Total Features:** 8

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 3 — S3 Cross-Feature Sanity Check
**Active Guide:** `guides_v2/stages/s3/s3_epic_planning_approval.md`
**Last Guide Read:** 2026-02-18 (S2.P2 complete; transitioning to S3)

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```

**You are here:** ➜ Stage 3 (S3 — Epic Planning Approval)

**S2 Wave Status**
- [x] Wave 1: Feature 01 S2 ✅ COMPLETE (spec approved, all 4 checklist Qs answered — 2026-02-18; spec updated 2026-02-18 per user correction)
  - Design precedents set: @dataclass Settings, create_settings_from_dict(), direct import, graceful E2E file handling
  - ⚠️ CORRECTION (2026-02-18): NO separate --debug flag. Universal args are --e2e-test + --log-level only (2, not 3). --e2e-test serves both E2E testing and debugging purposes.
- [x] Wave 2: Features 02-07 S2 ✅ COMPLETE (all 6 secondary agents finished — 2026-02-18)
  - Feature 02 (Secondary-A): ✅ Gate 3 approved — 5 args, 3 files
  - Feature 03 (Secondary-B): ✅ Gate 3 approved — 8 args, 1 file
  - Feature 04 (Secondary-C): ✅ Gate 3 approved — 8 args, 4 files
  - Feature 05 (Secondary-D): ✅ Gate 3 approved — 11 args, 2 files
  - Feature 06 (Secondary-E): ✅ Gate 3 approved — 11 args, 2 files
  - Feature 07 (Secondary-F): ✅ Gate 3 approved — 12 args, ~10 files
- [x] S2.P2 Cross-Feature Alignment ✅ COMPLETE (2026-02-18)
  - 21 pairwise pairs checked (3 Validation Loop rounds)
  - 4 conflicts found; all resolved or accepted-by-design
  - Key resolution: F07 REQ-07 updated with graceful skip (C-02)
  - Key note: F03 has implementation dependency on F01 REQ-09 (fetch_game_data signature) — implement F01 before F03
  - Comparison matrix: `research/S2_P2_COMPARISON_MATRIX_GROUP_2.md`
- [ ] Wave 3: Feature 08 S2 ⏳ BLOCKED (needs S3 + S4 complete)

---

## Agent Status

**Debugging Active:** NO
**Last Updated:** 2026-02-18
**Current Stage:** S3 — Cross-Feature Sanity Check
**Current Phase:** Starting S3 (transitioning from S2.P2)
**Current Step:** S2 fully complete (all waves + S2.P2 alignment) → ready to start S3
**Current Guide:** `stages/s3/s3_epic_planning_approval.md`
**Guide Last Read:** 2026-02-18 (will read at S3 start)

**Critical Rules:**
- S2.P2 complete: 4 conflicts found, all resolved; comparison matrix at research/S2_P2_COMPARISON_MATRIX_GROUP_2.md
- F03 implementation dependency on F01: F01 must be implemented before F03 (fetch_game_data signature)
- Feature 08 (integration test framework) still needs S2 — blocked until after S4

**Progress:** S2 ✅ fully complete (Wave 1 + Wave 2 + S2.P2) | S3 → next
**Next Action:** Read S3 guide and begin Cross-Feature Sanity Check
**Blockers:** None

---

## Epic Overview

**Epic Goal:**
Comprehensive architectural refactoring of all 7 runner scripts to establish consistent configuration management via CLI-based configuration with dependency injection, fast E2E test modes, debug support, and an integration test framework.

**Epic Scope:**
- IN: All 7 runner scripts, constructor parameter pattern, CLI args, E2E modes, debug mode, integration test framework, documentation
- OUT: Config file support (YAML/TOML), API mocking, GUI, CI/CD integration, new features/algorithms

**Key Outcomes:**
1. Zero CLI constants in config/constants files — argparse defaults are single source of truth
2. Constructor parameter pattern (dependency injection) used across all 7 scripts
3. Each script has E2E test mode completing in ≤3 minutes

**Original Request:** `feature-updates/KAI-10-architectural_refactoring_configuration_management/architectural_refactoring_configuration_management_notes.txt`

---

## Feature Dependency Groups (S2 Only)

**Wave Structure (3-wave group-based parallelization):**

| Wave | Features | Parallelization | Start Condition | Rationale |
|------|----------|-----------------|-----------------|-----------|
| Wave 1 | Feature 01 | Solo | Start immediately | Sets design precedents (constructor pattern, settings dict structure, E2E behavior) that inform Wave 2 specs |
| Wave 2 | Features 02-07 | All parallel | Feature 01 S2 complete | Each covers a different script; no inter-dependencies; all reference F01 spec for design patterns |
| Wave 3 | Feature 08 | Solo | Features 01-07 all S2 complete + S3 + S4 done | Integration test framework needs all 7 feature specs for complete CLI arg lists, E2E mode behaviors, and test file names |

**Dependency Rationale:**
- Features 02-07 have NO spec-level dependencies on each other (different scripts, no shared data structures)
- Features 02-07 reference Feature 01 spec for design pattern guidance (not structural dependencies)
- Feature 08 has TRUE spec dependencies: needs actual CLI arg names, E2E behaviors, and test file locations from all 7 features

---

## Epic Progress Tracker

**Overall Status:** 0/8 features complete

| Feature | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 | Done |
|---------|----|----|----|----|----|----|-------|-------|------|
| F01: refactor_player_data_fetcher | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F02: schedule_fetcher_cli | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F03: game_data_fetcher_cli | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F04: historical_compiler_cli | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F05: win_rate_simulation_e2e | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F06: accuracy_simulation_e2e | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F07: league_helper_cli | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F08: integration_test_framework | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |

**S9 - Epic Final QC:** ◻️ NOT STARTED
**S10 - Epic Cleanup:** ◻️ NOT STARTED

---

## Workflow Checklist

**S1 - Epic Planning:**
- [x] Epic folder created
- [x] Notes file in place
- [x] EPIC_README.md created (this file)
- [x] DISCOVERY.md created and user-approved (2026-02-18)
- [x] EPIC_TICKET.md created and user-validated (2026-02-18)
- [x] All 8 feature folders created
- [x] All per-feature files created (README.md, spec.md, checklist.md, lessons_learned.md × 8)
- [x] Initial epic_smoke_test_plan.md created
- [x] epic_lessons_learned.md created
- [x] research/ folder + README.md created
- [x] GUIDE_ANCHOR.md created
- [x] Parallelization assessment offered to user (Step 5.8-5.9) — user chose Group-Based Parallel (Option A)
- [x] S1 complete / transitioned to S2 (Step 6)

**S2 - Feature Deep Dives:**
- [x] Wave 1: Feature 01 S2 complete (spec.md + checklist.md user-approved — 2026-02-18)
- [x] Wave 2: Features 02-07 S2 all complete (parallel execution — all Gate 3 approved — 2026-02-18)
- [x] S2.P2 Cross-Feature Alignment complete (21 pairs, 4 conflicts resolved — 2026-02-18)
- [ ] Wave 3: Feature 08 S2 complete (BLOCKED until after S4)
- [x] Features 01-07 have spec.md complete and user-approved
- [x] Features 01-07 have checklist.md resolved
- [x] ALL feature README.md files created

**S3 - Cross-Feature Sanity Check:**
- [ ] All specs compared systematically
- [ ] Conflicts resolved
- [ ] User sign-off obtained (Gate 4.5)

**S4 - Epic Testing Strategy:**
- [ ] epic_smoke_test_plan.md updated based on deep dives
- [ ] Integration points identified
- [ ] Epic success criteria defined

**S9 - Epic Final QC:**
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] Epic QC rounds passed (all 3 rounds)
- [ ] End-to-end validation passed

**S10 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Guides updated based on lessons learned
- [ ] Final commits made
- [ ] Epic moved to done/ folder

---

## Guide Deviation Log

No deviations from guides.

---

## Epic Completion Summary

{To be filled in S10}
