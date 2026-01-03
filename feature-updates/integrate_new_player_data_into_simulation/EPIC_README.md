# Epic: integrate_new_player_data_into_simulation

**Created:** 2026-01-02
**Status:** IN PROGRESS
**Total Features:** TBD (pending Phase 3 breakdown)

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 2 - Feature Deep Dive (Feature 01)
**Active Guide:** `guides_v2/stages/stage_2/phase_0_research.md`
**Last Guide Read:** Not yet (will read when starting Stage 2)

**Stage Workflow:**
```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC
  ✅
```

**You are here:** ➜ Stage 2 (ready to start feature_01 deep dive)

**Critical Rules for Current Stage (Stage 2):**
1. Read ENTIRE guide before starting (use Read tool)
2. Use phase transition prompt from prompts_reference_v2.md (MANDATORY)
3. Extract epic intent from notes and ticket (Phase 0)
4. Conduct targeted research, not exhaustive search (Phase 1)
5. Pass research audit with all 5 checkpoints (Phase 1.5)

**Before Proceeding to Next Step:**
- [x] Read guide: `guides_v2/stages/stage_1/epic_planning.md`
- [x] Acknowledge critical requirements (phase transition prompt used)
- [x] Verify prerequisites from guide (all verified)
- [ ] Update this Quick Reference Card after each phase

---

## Agent Status

**Last Updated:** 2026-01-03 (Feature 01 Stage 5e COMPLETE - Epic Testing Plan Update)
**Current Stage:** Feature 01 COMPLETE - Ready for next feature
**Current Phase:** FEATURE_01_COMPLETE
**Current Step:** Proceed to Feature 02 Stage 5a (TODO Creation Round 1)
**Current Guide:** Will read `stages/stage_5/round1_todo_creation.md` for Feature 02
**Guide Last Read:** 2026-01-03 16:35 (post_feature_testing_update.md - COMPLETE)

**Critical Rules from Guide:**
- ✅ Updated test plan based on ACTUAL implementation (not specs)
- ✅ Added discovered integration points and edge cases
- ✅ Kept scenarios executable and specific
- ✅ Documented update rationale in Update History
- ✅ Committed test plan changes

**Stage 5e Completion Summary:**
- ✅ Reviewed Feature 01 actual implementation code
- ✅ Identified 6 updates to epic_smoke_test_plan.md
- ✅ Added Criterion 6: Graceful Error Handling
- ✅ Added Integration Point 6: Player ID Data Type (int)
- ✅ Updated Test Scenario 1: Statistical validation (non-zero percentages)
- ✅ Added Test Scenario 8: Edge Case Handling (4 critical tests)
- ✅ Updated Update Log with rationale
- ✅ All updates based on actual implementation discoveries

**Feature 01 Complete - Full Workflow:**
- ✅ Stage 5a: TODO Creation (3 rounds, 24 iterations)
- ✅ Stage 5b: Implementation Execution (3 code changes, 14 tests added)
- ✅ Stage 5c: Post-Implementation (smoke testing + 3 QC rounds + final review)
- ✅ Stage 5d: Cross-Feature Alignment (Features 02 & 03 specs updated)
- ✅ Stage 5e: Epic Testing Plan Update (6 updates to epic smoke test plan)

**Progress:** Feature 01 COMPLETE, ready to start Feature 02
**Next Action:** Use "Starting Stage 5a Round 1" prompt for Feature 02
**Blockers:** None

**Testing Strategy Summary:**
- 5 measurable epic success criteria defined
- 8 specific test scenarios created
- 5 integration points identified
- Test execution order documented

**Notes:**
- Branch epic/KAI-3 already created from previous attempt
- Starting fresh with clean slate (previous work was buggy and incomplete)
- Epic request clearly states to verify all previous work and remove anything incorrect

**Phase 2 Analysis Findings:**
- Win Rate Sim (SimulatedLeague.py): Already has `_parse_players_json()` method, already loading JSON
- Accuracy Sim (AccuracySimulationManager.py): Already copies JSON files to temp player_data/ folder
- PlayerManager: Has `load_players_from_json()` (new) and deprecated `load_players_from_csv()`
- JSON deprecation date: 2025-12-30 (3 days ago - very recent transition)
- Week 17 fix already implemented in SimulatedLeague `_parse_players_json()` with week_num_for_actual parameter
- Main issues: Outdated documentation, lingering CSV references, need verification of correctness

---

## Epic Overview

**Epic Goal:**
Update both Win Rate Simulation and Accuracy Simulation to use JSON-based player data (from player_data folder with positional JSON files) instead of CSV-based data (players.csv and players_projected.csv). Ensure both simulations maintain the same functionality as before the JSON file introduction was made, while correctly handling the new data format with weekly arrays for drafted_by, locked, projected_points, and actual_points fields.

**Epic Scope:**
- **Included:**
  - Update Win Rate Sim to load from JSON files in week_X folders
  - Update Accuracy Sim to load from JSON files in week_X folders
  - Update both sims to handle new field structure (arrays instead of individual columns)
  - Verify Week 17 assessment (use week_17 for projected_points, week_18 actual_points for week 17 games)
  - Remove all references to players.csv and players_projected.csv in simulation code
  - Verify all previous partial work for correctness and completeness

- **Excluded:**
  - Changes to league_helper module (already updated to use JSON)
  - Changes to player data format itself (JSON structure is established)
  - New simulation features beyond maintaining existing functionality

**Key Outcomes:**
1. Both simulations successfully load and use JSON player data from week_X folders
2. Week 17 correctly uses week_17 projected_points and week_18 actual_points
3. All simulation functionality works as it did with CSV data
4. No CSV file dependencies remain in simulation code
5. Previous buggy/incomplete work verified and corrected or removed

**Original Request:** `integrate_new_player_data_into_simulation_notes.txt` (moved from feature-updates/)

---

## Initial Scope Assessment

**Size:** MEDIUM (estimated 3-4 features)
**Complexity:** MODERATE (verification and cleanup of existing partial implementation)
**Risk Level:** MEDIUM (existing code partially works, need to verify correctness without breaking)

**Estimated Components Affected:**
- `simulation/win_rate/SimulatedLeague.py` - Verify JSON loading, remove CSV references, update docs
- `simulation/win_rate/SimulationManager.py` - Update documentation
- `simulation/accuracy/AccuracySimulationManager.py` - Verify JSON loading works correctly
- `simulation/accuracy/AccuracyCalculator.py` - Verify it uses PlayerManager correctly
- Docstrings across simulation module - Remove outdated CSV references
- Tests for both simulations - Update to use JSON, verify week 17 handling

**Existing Work to Verify:**
- SimulatedLeague `_parse_players_json()` implementation (week_N+1 fix logic)
- AccuracySimulationManager player_data folder copying logic
- PlayerManager JSON loading in simulation context
- All tests still passing with JSON data

---

## Epic Progress Tracker

**Overall Status:** 0/3 features complete

| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_win_rate_sim_verification | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_02_accuracy_sim_verification | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |
| feature_03_cross_simulation_testing | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |

**Legend:**
- ✅ = Complete
- ◻️ = Not started or in progress

**Note:** Stage 3 and Stage 4 are epic-level (not per-feature)

**Stage 6 - Epic Final QC:** ◻️ NOT STARTED
- Epic smoke testing passed: ◻️
- Epic QC rounds passed: ◻️
- Epic PR review passed: ◻️
- End-to-end validation passed: ◻️
- Date completed: Not complete

**Stage 7 - Epic Cleanup:** ◻️ NOT STARTED
- Final commits made: ◻️
- Epic moved to done/ folder: ◻️
- Date completed: Not complete

---

## Feature Summary

### Feature 01: Win Rate Simulation JSON Verification and Cleanup
**Folder:** `feature_01_win_rate_sim_verification/`
**Purpose:** Verify Win Rate Sim correctly uses JSON data, remove deprecated CSV code, update documentation
**Status:** Stage 1 complete (folder created)
**Dependencies:** None

### Feature 02: Accuracy Simulation JSON Verification and Cleanup
**Folder:** `feature_02_accuracy_sim_verification/`
**Purpose:** Verify Accuracy Sim correctly uses JSON data through PlayerManager, update documentation
**Status:** Stage 1 complete (folder created)
**Dependencies:** None (parallel to Feature 01)

### Feature 03: Cross-Simulation Testing and Documentation
**Folder:** `feature_03_cross_simulation_testing/`
**Purpose:** End-to-end testing of both simulations, comprehensive documentation updates
**Status:** Stage 1 complete (folder created)
**Dependencies:** Features 01 and 02 must be complete

---

## Bug Fix Summary

**Bug Fixes Created:** 0

No bug fixes created yet

---

## Epic-Level Files

**Created in Stage 1:**
- `EPIC_README.md` (this file) ✅
- `EPIC_TICKET.md` (user-validated outcomes) ✅
- `integrate_new_player_data_into_simulation_notes.txt` (original request) ✅
- `epic_smoke_test_plan.md` (initial placeholder) ✅
- `epic_lessons_learned.md` ✅
- `GUIDE_ANCHOR.md` (resumption instructions) ✅
- `research/` folder ✅

**Feature Folders:**
- `feature_01_win_rate_sim_verification/` (README, spec, checklist, lessons_learned) ✅
- `feature_02_accuracy_sim_verification/` (README, spec, checklist, lessons_learned) ✅
- `feature_03_cross_simulation_testing/` (README, spec, checklist, lessons_learned) ✅

**Bug Fix Folders (if any):**
None yet

---

## Workflow Checklist

**Stage 1 - Epic Planning:**
- [x] Epic folder created (Step 1.1)
- [x] Epic request file moved and renamed (Step 1.2)
- [x] EPIC_README.md created (Step 1.3)
- [x] Epic analyzed, components identified (Phase 2)
- [x] Feature breakdown proposed to user (Phase 3)
- [x] Epic ticket created and user-validated (Steps 3.6-3.7)
- [x] All feature folders created (Phase 4)
- [x] Initial `epic_smoke_test_plan.md` created (Phase 4)
- [x] `epic_lessons_learned.md` created (Phase 4)
- [x] `research/` folder created (Phase 4)
- [x] `GUIDE_ANCHOR.md` created (Phase 4)

**Stage 2 - Feature Deep Dives:**
- [x] ALL features have `spec.md` complete ✅
- [x] ALL features have `checklist.md` resolved ✅
- [x] ALL feature `README.md` files created ✅

**Stage 3 - Cross-Feature Sanity Check:**
- [x] All specs compared systematically ✅
- [x] Conflicts resolved (0 found, 0 resolved) ✅
- [x] User sign-off obtained (2026-01-03) ✅

**Stage 4 - Epic Testing Strategy:**
- [x] `epic_smoke_test_plan.md` updated based on deep dives ✅
- [x] Integration points identified (5 integration points) ✅
- [x] Epic success criteria defined (5 measurable criteria) ✅

**Stage 5 - Feature Implementation:**
{Will be populated after feature breakdown}

**Stage 6 - Epic Final QC:**
- [ ] Epic smoke testing passed (all 4 parts)
- [ ] Epic QC rounds passed (all 3 rounds)
- [ ] Epic PR review passed (all 11 categories)
- [ ] End-to-end validation vs original request passed

**Stage 7 - Epic Cleanup:**
- [ ] All unit tests passing (100%)
- [ ] Documentation verified complete
- [ ] Guides updated based on lessons learned (if needed)
- [ ] Final commits made
- [ ] Epic moved to `feature-updates/done/integrate_new_player_data_into_simulation/`

---

## Guide Deviation Log

**Purpose:** Track when agent deviates from guide (helps identify guide gaps)

| Timestamp | Stage | Deviation | Reason | Impact |
|-----------|-------|-----------|--------|--------|
| 2026-01-02 | Stage 1 | Skipped Step 1.0 (git branch creation) | Branch epic/KAI-3 already created from previous attempt | None - branch already exists and is correct |

---

## Epic Completion Summary

{This section will be filled out in Stage 7}
