## Epic: architectural_refactoring_configuration_management

**Created:** 2026-02-18
**Status:** IN PROGRESS
**Total Features:** 8

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 5 — S5 Implementation Planning (F01 first)
**Active Guide:** `guides_v2/stages/s5/s5_v2_validation_loop.md`
**Last Guide Read:** 2026-02-18 (S4 complete for all F01-F07)

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
↓        ↓        ↓        ↓        ↓           ↓        ↓
Epic  Features  Sanity  Testing  Implementation  Epic    Done
Plan  Deep Dive  Check  Strategy  (per feature)   QC
```

**You are here:** ➜ Stage 5 (S5 — Implementation Planning, starting with F01)

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
- [ ] Wave 3: Feature 08 S2 ⏳ UNBLOCKED (S3 + S4 complete — ready to start)

---

## Agent Status

**Debugging Active:** NO
**Last Updated:** 2026-02-18
**Current Stage:** S4 COMPLETE — transitioning to S5
**Current Phase:** S5 pending (start with F01)
**Current Step:** S4 done — all 7 test_strategy.md files created and validated; F08 S2 now unblocked
**Current Guide:** `stages/s5/s5_v2_validation_loop.md`
**Guide Last Read:** 2026-02-18

**Critical Rules:**
- F03 implementation dependency on F01: F01 must be implemented before F03
- F08 S2 now UNBLOCKED (S4 complete for all F01-F07) — can begin F08 S2 before or after S5 starts
- Gate 5 is MANDATORY — cannot proceed to S6 without user-approved implementation_plan.md

**Progress:** S3 ✅ (Gate 4.5 passed) | S4 ✅ (all 7 test_strategy.md complete)
**Next Action:** Start S5 for F01 — read s5_v2_validation_loop.md guide
**Blockers:** None

---

## Epic Overview

**Epic Goal:**
Comprehensive architectural refactoring of all 7 runner scripts to establish consistent configuration management via CLI-based configuration with dependency injection, fast E2E test modes, and an integration test framework.

**Epic Scope:**
- IN: All 7 runner scripts, constructor parameter pattern, CLI args, E2E modes (`--e2e-test`), integration test framework (F08), documentation
- OUT: Config file support (YAML/TOML), API mocking, GUI, CI/CD integration, new features/algorithms, separate `--debug` flag (removed — `--e2e-test` serves both purposes)

**Key Outcomes:**
1. Zero CLI constants in config/constants files — argparse defaults are single source of truth
2. Constructor parameter pattern (dependency injection) used across all 7 scripts
3. Each script has `--e2e-test` mode completing in ≤180 seconds (3 minutes)
4. All 7 scripts have consistent universal args: `--e2e-test` (flag) + `--log-level` (str, choices=DEBUG/INFO/WARNING/ERROR/CRITICAL)

**Original Request:** `feature-updates/KAI-10-architectural_refactoring_configuration_management/architectural_refactoring_configuration_management_notes.txt`

---

## Feature Summary (S3 — from S2 Deep Dives)

| Feature | Script | Key Args Added | Key Design Approach | Files Modified |
|---------|--------|---------------|---------------------|----------------|
| F01: refactor_player_data_fetcher | `run_player_fetcher.py` | 17 total (13 new + 2 universal + 2 preserved) | @dataclass Settings, create_settings_from_dict(), direct import, graceful E2E skip for drafted_data.csv | ~8 files |
| F02: schedule_fetcher_cli | `run_schedule_fetcher.py` | 5 total (3 new + 2 universal) | Direct params (no dataclass), already uses direct import, max_weeks=1 for E2E | 3 files |
| F03: game_data_fetcher_cli | `run_game_data_fetcher.py` | 8 total (4 existing + 2 universal + --request-timeout + --historical-season) | Direct params, remove os.chdir, remove config import; **depends on F01 REQ-09** | 1 file |
| F04: historical_compiler_cli | `compile_historical_data.py` | 8 total (4 existing + 2 universal + --timeout + --rate-limit-delay) | Direct params, tempfile for E2E output, --verbose preserved (maps to DEBUG) | 4 files |
| F05: win_rate_simulation_e2e | `run_win_rate_simulation.py` | 11 total (9 existing + 2 universal) | Direct params, E2E forces mode=single/sims=1/workers=1, graceful skip if data missing | 2 files |
| F06: accuracy_simulation_e2e | `run_accuracy_simulation.py` | 11 total (10 existing + --e2e-test; normalizes --log-level to uppercase) | Direct params, --log-level normalized via type=str.upper, graceful skip if data missing | 2 files |
| F07: league_helper_cli | `run_league_helper.py` | 12 total (10 new + 2 universal; --enable-log-file preserved) | @dataclass Settings, execute_e2e() per mode manager, graceful skip if league_config.json missing | ~10 files |
| F08: integration_test_framework | `run_all_integration_tests.py` (new) | — | Master runner + per-script CLI integration test runners; F08 S2 blocked until after S4 | ~8 new files |

**Implementation Note:** F01 before F03 (F03 runner depends on F01 REQ-09: `request_timeout` param added to `fetch_game_data()`)

---

## Epic Architecture Decisions (S3 — Consolidated from S2 Specs)

1. **No --debug flag:** Removed from all 7 scripts. `--e2e-test` serves both E2E testing and debugging. For verbose output: `--e2e-test --log-level DEBUG`. (Design correction 2026-02-18)

2. **Universal args are exactly 2:** `--e2e-test` (flag, default False) and `--log-level` (str, choices=DEBUG/INFO/WARNING/ERROR/CRITICAL, default='INFO'). All 7 scripts have both.

3. **Two Settings patterns:** Scripts with standalone internal modules (F01: LeagueDataFetcher, F07: LeagueHelperManager) use `@dataclass Settings` + `create_settings_from_dict()`. Runner-as-main scripts (F02-F06) pass args directly without a Settings dataclass.

4. **Graceful skip in E2E mode:** Scripts depending on local data files (F01, F05, F06, F07) exit 0 with an info log when required files are absent in E2E mode. F04 uses tempfile (always succeeds). F02/F03 fetch fresh from APIs (no skip needed).

5. **Argparse defaults are single source of truth:** All config imports for CLI-configurable values removed from runners. Hardcoded argparse defaults (e.g., season=2025, week=17) replace config fallbacks. Behavior identical from user perspective.

6. **--log-level case:** F01-F05, F07 use case-sensitive uppercase choices. F06 normalizes via `type=str.upper` (accepts lowercase too) for backward compatibility with its existing lowercase choices.

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
| F01: refactor_player_data_fetcher | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F02: schedule_fetcher_cli | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F03: game_data_fetcher_cli | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F04: historical_compiler_cli | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F05: win_rate_simulation_e2e | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F06: accuracy_simulation_e2e | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| F07: league_helper_cli | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
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
- [x] S3.P1: epic_smoke_test_plan.md updated with concrete scenarios (S3 version — 2026-02-18)
- [x] S3.P2: EPIC_README.md refined with feature summaries + architecture decisions (2026-02-18)
- [x] S3.P3: Gate 4.5 — User approval obtained (2026-02-18)

**S4 - Feature Testing Strategy (per feature):**
- [x] F01 test_strategy.md created and validated (87 tests — 2026-02-18)
- [x] F02-F07 test_strategy.md files created and validated (F02: 38, F03: 42, F04: 46, F05: 38, F06: 40, F07: 54 — 2026-02-18)
- [ ] F08 S2 complete (now UNBLOCKED — ready to start)

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
