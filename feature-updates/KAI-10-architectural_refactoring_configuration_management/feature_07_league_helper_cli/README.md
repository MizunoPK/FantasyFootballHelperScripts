## Feature: league_helper_cli

**Created:** 2026-02-18
**Status:** S1 complete — S2 pending

---

## Feature Context

**Part of Epic:** architectural_refactoring_configuration_management (KAI-10)
**Feature Number:** 07 of 08
**Created:** 2026-02-18

**Purpose:**
Refactor `run_league_helper.py` (currently has only --enable-log-file) to expose all configurable constants as CLI arguments (~12 args: --mode, --config-path, --data-folder, --recommendation-count, --min-waiver-improvement, --min-trade-improvement, --logging-to-file, --logging-file, --league-id, --week, --season, --team-id, plus universal args) and apply the constructor parameter pattern from Feature 01.

**Dependencies:**
- **Depends on:** Feature 01 spec (for design precedents — Wave 2 starts after Feature 01 S2 completes)
- **Required by:** Feature 08 (integration test framework)

**Integration Points:**
- Follows constructor parameter pattern defined by Feature 01
- Largest Wave 2 scope: 5 interactive modes that must all work non-interactively in E2E mode
- Feature 08 wraps this feature's E2E test mode (must run all 5 modes) in `test_league_helper_cli.py`

---

## Agent Status

**Last Updated:** 2026-02-18
**Current Phase:** PLANNING
**Current Step:** S1 complete — awaiting Feature 01 S2 completion before starting Wave 2
**Current Guide:** `stages/s2/s2_feature_deep_dive.md`
**Guide Last Read:** Not yet read

**Progress:** 0/5 S2 items complete
**Next Action:** Wait for Feature 01 S2 complete, then read s2_feature_deep_dive.md and begin S2
**Blockers:** Feature 01 S2 must complete first (Wave 2 dependency)

---

## Feature Stages Progress

**S2 - Feature Deep Dive:**
- [x] `spec.md` created (seeded in S1)
- [ ] `spec.md` complete (user-approved, Gate 3)
- [ ] `checklist.md` resolved (all items answered)
- [x] `lessons_learned.md` created
- [x] README.md created (this file)
- [ ] S2 complete: ◻️

**S5 v2 - Implementation Planning:**
- [ ] Phase 1: Draft Creation complete (~70% quality baseline)
- [ ] Phase 2: Validation Loop complete (3 consecutive clean rounds)
  - [ ] All 11 S5-specific dimensions validated
  - [ ] All 7 master dimensions validated
  - [ ] Total validation rounds executed: 0
- [ ] `implementation_plan.md` created and user-approved (Gate 5)
- [ ] `questions.md` created (or documented "no questions")
- [ ] S5 v2 complete: ◻️

**S6 - Implementation Execution:**
- [ ] All implementation tasks complete
- [ ] All unit tests passing (100%)
- [ ] `implementation_checklist.md` created and all verified
- [ ] S6 complete: ◻️

**S7 - Implementation Testing & Review:**
- [ ] Smoke testing (3 parts) passed
- [ ] Validation Loop passed (3 consecutive clean rounds)
- [ ] All 11 dimensions checked every round
- [ ] PR Review (11 categories) passed
- [ ] `lessons_learned.md` updated with S7 insights
- [ ] S7 complete: ◻️

**S8.P1 - Cross-Feature Alignment:**
- [ ] Reviewed all remaining feature specs
- [ ] Updated remaining specs based on THIS feature's actual implementation
- [ ] Documented features needing rework (or "none")
- [ ] No significant rework needed for other features
- [ ] S8.P1 complete: ◻️

**S8.P2 - Epic Testing Plan Update:**
- [ ] `epic_smoke_test_plan.md` reviewed
- [ ] Test scenarios updated based on actual implementation
- [ ] Integration points added to epic test plan
- [ ] Update History table in epic test plan updated
- [ ] S8.P2 complete: ◻️

---

## Files in this Feature

**Core Files:**
- `README.md` - This file (feature overview and status)
- `spec.md` - **Primary specification** (detailed requirements)
- `checklist.md` - Tracks resolved vs pending decisions
- `lessons_learned.md` - Feature-specific insights

**Planning Files (S5):**
- `implementation_plan.md` - Implementation build guide (created in S5, user-approved)
- `questions.md` - Questions for user (created in S5, or documented "no questions")

**Implementation Files (S6):**
- `implementation_checklist.md` - Continuous spec verification during coding

---

## Feature-Specific Notes

**Key Technical Scope:**
- `run_league_helper.py` currently has only 1 arg: --enable-log-file
- 5 interactive modes (draft, optimizer, trade, data editor, viewer) must all support automated E2E flow
- E2E test mode: run all 5 modes sequentially, debug-sized datasets (2 recommendations, 1 trade, top 50 players), no user prompts, total ≤180s
- Largest scope in Wave 2 — interactive mode automation is the main complexity
- ~12 script-specific CLI args to add + 3 universal args

---

## Completion Summary

{This section filled out after S8.P2}
