## Epic: architectural_refactoring_configuration_management

**Created:** 2026-02-18
**Status:** IN PROGRESS
**Total Features:** 8

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 2 — S2 Wave 1 (Feature 01 solo)
**Active Guide:** `guides_v2/stages/s2/s2_p1_spec_creation_refinement.md`
**Last Guide Read:** 2026-02-18 (read s2_feature_deep_dive.md router + s2_primary_agent_group_wave_guide.md)

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```

**You are here:** ➜ Stage 2 (S2.P1 — Wave 1, Feature 01)

**S2 Wave Status**
- [x] Wave 1: Feature 01 S2 ✅ COMPLETE (spec approved, all 4 checklist Qs answered — 2026-02-18)
  - Design precedents set: @dataclass Settings, create_settings_from_dict(), direct import, graceful E2E file handling
- [ ] Wave 2: Features 02-07 S2 🚀 READY (handoff packages generated, awaiting agent spawn)
  - Feature 02 (Secondary-A): ⏳ not started
  - Feature 03 (Secondary-B): ⏳ not started
  - Feature 04 (Secondary-C): ⏳ not started
  - Feature 05 (Secondary-D): ⏳ not started
  - Feature 06 (Secondary-E): ⏳ not started
  - Feature 07 (Secondary-F): ⏳ not started
- [ ] Wave 3: Feature 08 S2 ⏳ BLOCKED (needs Wave 2 complete + S3 + S4)

---

## Agent Status

**Debugging Active:** NO
**Last Updated:** 2026-02-18
**Current Stage:** S2 — Wave 2 (Features 02-07 parallel)
**Current Phase:** WAVE_TRANSITION → awaiting user to spawn 6 secondary agents
**Current Step:** Wave 1 ✅ complete → handoff packages generated → Wave 2 ready to start
**Current Guide:** `stages/s2/s2_primary_agent_group_wave_guide.md`
**Guide Last Read:** 2026-02-18

**Critical Rules:**
- Wave 2: 6 secondary agents execute S2.P1 in parallel (Features 02-07)
- Secondary agents stop after S2.P1.I3 — Primary (me) runs S2.P2 for Wave 2
- After Wave 2 S2.P2 → Final S2.P2 across ALL features (cross-group alignment)
- Feature 01 spec.md is design reference for all Wave 2 features

**Progress:** Wave 1 ✅ S2 complete | Wave 2 🚀 ready to start (handoff packages in feature folders)
**Next Action:** User spawns 6 secondary agents (one per Feature 02-07) with handoff packages
**Blockers:** None — waiting for user to spawn Wave 2 agents

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
| F01: refactor_player_data_fetcher | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F02: schedule_fetcher_cli | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F03: game_data_fetcher_cli | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F04: historical_compiler_cli | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F05: win_rate_simulation_e2e | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F06: accuracy_simulation_e2e | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F07: league_helper_cli | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
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
- [ ] Wave 2: Features 02-07 S2 all complete (parallel execution — 6 secondary agents)
- [ ] Wave 3: Feature 08 S2 complete
- [ ] ALL features have spec.md complete
- [ ] ALL features have checklist.md resolved
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
