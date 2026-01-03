# Feature: Accuracy Simulation JSON Verification and Cleanup

**Created:** 2026-01-02
**Status:** Stage 1 complete (folder created)

---

## Feature Context

**Part of Epic:** integrate_new_player_data_into_simulation
**Feature Number:** 2 of 3
**Created:** 2026-01-02

**Purpose:**
Verify Accuracy Simulation correctly uses JSON player data through PlayerManager, ensure proper week-specific data loading, and update all documentation to reflect JSON-based data loading.

**Dependencies:**
- **Depends on:** None (parallel to Feature 01)
- **Required by:** Feature 03 (cross-simulation testing depends on this being complete)

**Integration Points:**
- Feature 03 uses Accuracy Sim for integration testing
- AccuracySimulationManager._create_player_manager() is the core component to verify
- Uses PlayerManager from league_helper (already migrated to JSON)

---

## Agent Status

**Last Updated:** 2026-01-03 (STAGE_2c complete - All questions resolved)
**Current Phase:** SPECIFICATION_COMPLETE
**Current Step:** STAGE_2 Complete - Ready for STAGE_3 (Cross-Feature Sanity Check)
**Current Guide:** stages/stage_2/phase_2_refinement.md
**Guide Last Read:** 2026-01-03

**Progress:** Stage 2 COMPLETE
**Next Action:** Wait for all features to complete Stage 2, then begin Stage 3
**Blockers:** None

**Specification Summary:**
- Requirements: 7 (all traced to epic or user answers)
- Questions resolved: 4/4 (100%)
- User answers:
  - Q1: Comprehensive verification (code review + manual + tests)
  - Q2: Add comprehensive PlayerManager integration tests
  - Q3: Add dedicated Week 17 test
  - Q4: Align edge cases with Win Rate Sim
- Scope creep: 0
- Missing requirements: 0
- Acceptance criteria: 11 criteria approved

---

## Feature Stages Progress

**Stage 2 - Feature Deep Dive:**
- [x] `spec.md` created and complete ✅
- [x] `checklist.md` created (all items resolved) ✅
- [x] `lessons_learned.md` created ✅
- [x] README.md created (this file) ✅
- [x] Stage 2 complete: ✅ (2026-01-03)

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
- `README.md` - This file (feature overview and status) ✅
- `spec.md` - **Primary specification** (will be created in Stage 2)
- `checklist.md` - Tracks resolved vs pending decisions (will be created in Stage 2)
- `lessons_learned.md` - Feature-specific insights (will be created in Stage 2)

**Planning Files (Stage 5a):**
- `todo.md` - Implementation task list (created in Stage 5a)
- `questions.md` - Questions for user (created in Stage 5a, or documented "no questions")

**Implementation Files (Stage 5b):**
- `implementation_checklist.md` - Continuous spec verification during coding
- `code_changes.md` - Documentation of all code changes

**Research Files (if needed):**
- Located in epic-level `research/` directory

---

## Feature-Specific Notes

**Key Components to Verify:**
- `simulation/accuracy/AccuracySimulationManager.py` - Core orchestration class
- `simulation/accuracy/AccuracyCalculator.py` - MAE calculation logic
- `league_helper/util/PlayerManager.py` - JSON loading (already migrated)

**Critical Logic:**
- `_create_player_manager()` method that creates temp dir with player_data/
- Copying 6 JSON files from week folder to player_data/
- Verify PlayerManager.load_players_from_json() works in simulation context

**Known Context:**
- Accuracy Sim already updated to copy JSON files (lines 361-373)
- Uses temporary directory structure for each config test
- Different data flow than Win Rate Sim (uses PlayerManager, not direct parsing)

---

## Completion Summary

{This section will be filled out after Stage 5e}
