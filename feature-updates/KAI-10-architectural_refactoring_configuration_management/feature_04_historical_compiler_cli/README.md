## Feature: historical_compiler_cli

**Created:** 2026-02-18
**Status:** S1 complete — S2 pending

---

## Feature Context

**Part of Epic:** architectural_refactoring_configuration_management (KAI-10)
**Feature Number:** 04 of 08
**Created:** 2026-02-18

**Purpose:**
Enhance `compile_historical_data.py` with universal CLI arguments (--debug, --e2e-test, --log-level), add missing script-specific args (~6 more: --weeks, --validate, --clean, --timeout, --rate-limit-delay, --skip-backups), remove REQUEST_TIMEOUT and RATE_LIMIT_DELAY from constants.py, apply the constructor parameter pattern, and implement E2E test mode ≤180s.

**Dependencies:**
- **Depends on:** Feature 01 spec (for design precedents — Wave 2 starts after Feature 01 S2 completes)
- **Required by:** Feature 08 (integration test framework)

**Integration Points:**
- Follows constructor parameter pattern defined by Feature 01
- Already has 4 args (--year, --verbose, --enable-log-file, --output-dir) to preserve
- Feature 08 wraps this feature's E2E test mode in integration test runner

---

## Agent Status

**Last Updated:** 2026-02-18
**Current Phase:** S2.P1 COMPLETE
**Current Step:** Gate 3 passed — spec.md and checklist.md user-approved 2026-02-18
**Current Guide:** `stages/s2/s2_p1_spec_creation_refinement.md`
**Guide Last Read:** 2026-02-18

**Progress:** 3/5 S2 items complete (spec.md approved, checklist.md approved, RESEARCH_NOTES.md created)
**Next Action:** STOP — waiting for Primary to run S2.P2 across all Wave 2 features
**Blockers:** None — S2.P1 complete, READY_FOR_SYNC = true

---

## Feature Stages Progress

**S2 - Feature Deep Dive:**
- [x] `spec.md` created (seeded in S1)
- [x] `spec.md` complete (user-approved, Gate 3 — 2026-02-18)
- [x] `checklist.md` resolved (all items answered, Gate 3 — 2026-02-18)
- [x] `lessons_learned.md` created
- [x] README.md created (this file)
- [x] `RESEARCH_NOTES.md` created
- [ ] S2 complete (Primary runs S2.P2): ◻️

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
- `compile_historical_data.py` already has 4 args: --year, --verbose, --enable-log-file, --output-dir
- Must maintain backward compatibility with --verbose (maps to DEBUG logging) and existing args
- `historical_data_compiler/constants.py` has REQUEST_TIMEOUT=30.0 and RATE_LIMIT_DELAY=0.3 — these must be removed and replaced with CLI args
- ~6 new script-specific args: --weeks, --validate, --clean, --timeout, --rate-limit-delay, --skip-backups
- E2E test mode: compile 1 season, skip backups, ≤180s

---

## Completion Summary

{This section filled out after S8.P2}
