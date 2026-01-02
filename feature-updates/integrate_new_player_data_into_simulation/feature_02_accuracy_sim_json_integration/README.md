# Feature: Accuracy Simulation JSON Integration

**Created:** 2026-01-01
**Status:** Planning (Stage 1 complete)

---

## Feature Context

**Part of Epic:** integrate_new_player_data_into_simulation
**Feature Number:** 2 of 2
**Created:** 2026-01-01

**Purpose:**
Update the Accuracy Simulation subsystem to load player data from position-specific JSON files (6 per week) instead of the legacy players.csv and players_projected.csv format. This includes verifying Week 17 scoring uses the correct folders (week_17 for projected, week_18 for actual) and ensuring DEF/K positions are evaluated correctly.

**Dependencies:**
- **Depends on:** None (parallel to Feature 1)
- **Required by:** None

**Integration Points:**
- None (standalone feature - Accuracy Sim operates independently from Win Rate Sim)

---

## Agent Status

**Last Updated:** 2026-01-01
**Current Phase:** STAGE_2_COMPLETE
**Current Step:** All 5 phases complete
**Current Guide:** `STAGE_2_feature_deep_dive_guide.md`
**Guide Last Read:** 2026-01-01

**Critical Rules from Guide:**
- Targeted research for THIS feature only (not entire epic)
- NEVER assume - investigate codebase first (Lesson from Feature 1)
- ONE question at a time (don't batch questions)
- Only confirmed info in spec.md
- Checklist all [x] required before complete

**Progress:** ✅ 5/5 phases complete
- Phase 1: Targeted Research (COMPLETE - ACCURACY_SIM_DISCOVERY.md)
- Phase 2: Update Spec & Checklist (COMPLETE - spec.md, checklist.md)
- Phase 3: Question Resolution (COMPLETE - all 7 questions resolved via Feature 1 findings)
- Phase 4: Scope Adjustment (COMPLETE - scope manageable, no split needed)
- Phase 5: Cross-Feature Alignment (COMPLETE - documented in spec.md)

**Next Action:** Ready for Stage 3 (Cross-Feature Sanity Check)
**Blockers:** None

---

## Feature Stages Progress

**Stage 2 - Feature Deep Dive:**
- [x] `spec.md` created and complete
- [x] `checklist.md` created (all items resolved or marked pending)
- [x] `lessons_learned.md` created
- [x] README.md created (this file)
- [x] Stage 2 complete: ✅

**Stage 5a - TODO Creation:**
- [ ] 24 verification iterations complete
- [ ] Iteration 4a: TODO Specification Audit PASSED
- [ ] Iteration 23a: Pre-Implementation Spec Audit (ALL 4 PARTS PASSED)
- [ ] Iteration 24: Implementation Readiness PASSED
- [ ] `todo.md` created
- [ ] `questions.md` created (or documented "no questions")
- [ ] Stage 5a complete: ◻️

**Stage 5b - Implementation:**
- [ ] All TODO tasks complete
- [ ] All unit tests passing (100%)
- [ ] `implementation_checklist.md` created and all verified
- [ ] `code_changes.md` created and updated
- [ ] Stage 5b complete: ◻️

**Stage 5c - Post-Implementation:**
- [ ] Smoke testing (3 parts) passed
- [ ] QC Round 1 passed
- [ ] QC Round 2 passed
- [ ] QC Round 3 passed
- [ ] PR Review (11 categories) passed
- [ ] `lessons_learned.md` updated with Stage 5c insights
- [ ] Stage 5c complete: ◻️

**Stage 5d - Cross-Feature Alignment:**
- [ ] Reviewed all remaining feature specs
- [ ] Updated remaining specs based on THIS feature's actual implementation
- [ ] Documented features needing rework (or "none")
- [ ] No significant rework needed for other features
- [ ] Stage 5d complete: ◻️

**Stage 5e - Epic Testing Plan Update:**
- [ ] `epic_smoke_test_plan.md` reviewed
- [ ] Test scenarios updated based on actual implementation
- [ ] Integration points added to epic test plan
- [ ] Update History table in epic test plan updated
- [ ] Stage 5e complete: ◻️

---

## Files in this Feature

**Core Files:**
- `README.md` - This file (feature overview and status)
- `spec.md` - Primary specification (detailed requirements) - **NOT YET CREATED**
- `checklist.md` - Tracks resolved vs pending decisions - **NOT YET CREATED**
- `lessons_learned.md` - Feature-specific insights - **NOT YET CREATED**

**Planning Files (Stage 5a):**
- `todo.md` - Implementation task list (will be created in Stage 5a)
- `questions.md` - Questions for user (will be created in Stage 5a if needed)

**Implementation Files (Stage 5b):**
- `implementation_checklist.md` - Continuous spec verification during coding (will be created in Stage 5b)
- `code_changes.md` - Documentation of all code changes (will be created in Stage 5b)

---

## Feature-Specific Notes

**Files to Modify:**
- `simulation/accuracy/AccuracySimulationManager.py` - Player data loading for accuracy calculations
- `simulation/accuracy/ParallelAccuracyRunner.py` - Parallel execution with JSON data

**Key Changes Required:**
- Replace CSV file paths with JSON file paths (6 position files per week)
- Parse JSON structure with projected_points/actual_points arrays
- Handle new field names (drafted_by, locked)
- Verify Week 17 logic: week_17 folders for projected_points, week_18 folders for actual_points
- Verify DEF and K positions are evaluated correctly
- Maintain all existing accuracy calculation logic (no algorithm changes)

**Special Validation:**
- Week 17/18 folder usage (explicitly mentioned in epic request)
- DEF and K evaluation (explicitly mentioned in epic request)

---

## Completion Summary

{This section will be filled out after Stage 5e}
