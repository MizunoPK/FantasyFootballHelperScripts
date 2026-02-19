## Epic: game_data_fetcher_cli

**Created:** 2026-02-19
**Status:** IN PROGRESS
**Total Features:** 1

---

## Quick Reference Card (Always Visible)

**Current Stage:** Stage 1 - Epic Planning
**Active Guide:** `guides_v2/stages/s1/s1_epic_planning.md`
**Last Guide Read:** 2026-02-19 (session start)

**Stage Workflow:**
```
S1 → S2 → S3 → S4 → [S5→S6→S7→S8] → S9 → S10
```

**You are here:** S1 — Epic Planning (Step 3: Discovery Phase)

**Critical Rules for Current Stage:**
1. Discovery Phase MANDATORY — cannot create feature folders until approved
2. Discovery Loop: 3 consecutive clean iterations required
3. Feature breakdown needs user approval before epic ticket
4. Epic ticket needs user validation before folder creation
5. Update Agent Status after EACH major step

**Before Proceeding to Next Step:**
- [ ] Read guide: `guides_v2/stages/s1/s1_epic_planning.md`
- [ ] Acknowledge critical requirements
- [ ] Verify prerequisites from guide
- [ ] Update this Quick Reference Card

---

## Agent Status

**Debugging Active:** NO
**Last Updated:** 2026-02-19 (S3 complete, Gate 4.5 approved)
**Current Stage:** S4 — Feature Testing Strategy
**Current Phase:** TESTING_STRATEGY
**Current Step:** S3 complete — ready for S4
**Current Guide:** `stages/s4/s4_feature_testing_strategy.md`
**Guide Last Read:** —

**Critical Rules from Guide:**
- Read full S4 guide before starting
- Test-driven: define tests BEFORE implementation
- Update Agent Status after S4

**Progress:** S1 + S2 + S3 complete
**Next Action:** Read S4 guide and create test_strategy.md for feature_01
**Blockers:** None

---

## Epic Overview

**Epic Goal:**
Refactor `run_game_data_fetcher.py` to add universal CLI args (`--e2e-test`, `--log-level`), script-specific args (`--request-timeout`, `--historical-season`), remove the `os.chdir()` anti-pattern, remove config imports, wire log-level to `setup_logger()`, and implement E2E test mode. Mirrors the KAI-10 Feature 01 pattern applied to the game data fetcher runner.

**Epic Scope:**
Modify 1 runner script + create 1 test file.

**Key Outcomes:**
1. `run_game_data_fetcher.py` has 8 CLI args (4 existing + 4 new) with no config imports
2. `--e2e-test` mode completes in ≤180s, writes to `/tmp/game_data_e2e_test.csv` only
3. `os.chdir()` eliminated — sys.path only (like player_fetcher pattern)

**Architecture Decisions (S2 approved):**
- `parse_args(argv=None)` extracted as module-level function (enables unit testing of defaults)
- E2E output: fixed path `/tmp/game_data_e2e_test.csv` (not random tmpdir — user preference: always fixed paths)
- All 5 KAI-10 S2 design decisions carried forward unchanged

**Original Request:** `feature-updates/requests/cli-enhancements/game_data_fetcher_cli_notes.txt`

---

## Epic Progress Tracker

**Overall Status:** 0/1 features complete

| Feature | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8.P1 | S8.P2 |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_game_data_fetcher_cli | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | N/A | ◻️ |

**S9 - Epic Final QC:** ◻️ NOT STARTED
**S10 - Epic Cleanup:** ◻️ NOT STARTED

---

## Feature Summary

### Feature 01: game_data_fetcher_cli
**Folder:** `feature_01_game_data_fetcher_cli/`
**Purpose:** Refactor run_game_data_fetcher.py — add 4 CLI args, remove os.chdir, remove config imports, add tests
**Status:** S2 complete (Gate 3 approved 2026-02-19)
**Dependencies:** None (KAI-10 F01 already modified game_data_fetcher.py)

---

## Feature Dependency Groups (S2 Only)

All features independent — single S2 wave (only 1 feature).

---

## Epic-Level Files

**Created in S1:**
- `EPIC_README.md` (this file)
- `DISCOVERY.md` — Epic-level source of truth
- `epic_smoke_test_plan.md` — Initial placeholder (will update in S4)
- `epic_lessons_learned.md` — Epic insights
- `research/` — Research documents

**Feature Folders:**
- `feature_01_game_data_fetcher_cli/` — Runner refactor + tests

---

## Workflow Checklist

**S1 - Epic Planning:**
- [x] Git branch created (epic/KAI-11)
- [x] EPIC_TRACKER.md updated
- [x] EPIC_README.md created (this file)
- [x] DISCOVERY.md created
- [x] Discovery approved by user
- [x] Feature breakdown approved by user
- [x] Epic ticket created and user-validated
- [x] All feature folders created
- [x] epic_smoke_test_plan.md created
- [x] epic_lessons_learned.md created
- [x] research/ folder created
- [x] GUIDE_ANCHOR.md created
- [x] Parallelization assessment completed (Step 5.8-5.9) — N/A (1 feature)
- [x] S1 complete, ready for S2

**S2 - Feature Deep Dive:**
- [x] feature_01 spec.md complete (Gate 3 approved 2026-02-19)
- [x] feature_01 checklist.md resolved (7 items, all resolved)
- [x] feature_01 README.md created
- [x] S2.P2 comparison matrix created (N/A — 1 feature, 0 pairs)
- [x] S2 complete

**S3 - Cross-Feature Sanity Check:**
- [x] epic_smoke_test_plan.md updated to S3 version (8 scenarios, concrete commands)
- [x] EPIC_README.md documentation refined (architecture decisions documented)
- [x] Gate 4.5 approved by user
- [x] S3 complete

**S4 - Feature Testing Strategy:**
- [ ] feature_01 test_strategy.md created and validated

**S5 - Feature Implementation:**
- [ ] Feature 01: S5→S6→S7→S8 complete

**S9 - Epic Final QC:**
- [ ] Epic smoke testing passed
- [ ] Epic QC rounds passed
- [ ] End-to-end validation passed

**S10 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Documentation verified
- [ ] Final commits made
- [ ] Epic moved to done/

---

## Bug Fix Summary

No bug fixes created yet.

---

## Guide Deviation Log

No deviations from guides.

---

## Epic Completion Summary

{To be filled in S10}
