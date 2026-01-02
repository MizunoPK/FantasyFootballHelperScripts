# Epic: integrate_new_player_data_into_simulation

**Created:** 2026-01-01
**Status:** IN PROGRESS
**Total Features:** TBD (will be determined after Phase 2 analysis)

---

## 🎯 Quick Reference Card (Always Visible)

**Current Stage:** Stage 4 - Epic Testing Strategy COMPLETE ✅
**Active Guide:** `guides_v2/STAGE_5aa_round1_guide.md` (ready to read)
**Last Guide Read:** 2026-01-01 (Stage 4 guide)

**Stage Workflow:**
```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
  ↓         ↓         ↓         ↓         ↓         ↓         ↓
Epic    Features  Sanity   Testing   Impl     Epic      Done
Plan    Deep Dive  Check   Strategy  (5a-5e)  QC
 ✅        ✅        ✅        ✅        ➜
```

**You are here:** ➜ Ready for Stage 5 (Feature Implementation)

**Critical Rules for Stage 5a (Round 1):**
1. Read STAGE_5aa_round1_guide.md (start with Round 1)
2. Execute iterations 1-7 + Iteration 4a MANDATORY GATE
3. Iteration 4a: TODO Specification Audit (must pass before Round 2)
4. Create detailed TODO with acceptance criteria
5. Verify all interfaces against actual source code
6. Use phase transition prompt from prompts_reference_v2.md

**Before Proceeding to Stage 5a:**
- [ ] Read guide: `guides_v2/STAGE_5aa_round1_guide.md`
- [ ] Acknowledge critical requirements
- [ ] Verify Stage 4 complete (epic_smoke_test_plan.md updated)
- [ ] Choose first feature to implement
- [ ] Update this Quick Reference Card (after Round 1 complete)

---

## Agent Status

**Last Updated:** 2026-01-02 (Stage 5d complete for feature_01)
**Current Stage:** Feature 01 - Stage 5d COMPLETE ✅ → Ready for Stage 5e
**Current Phase:** CROSS_FEATURE_ALIGNMENT → Transition to TESTING_PLAN_UPDATE
**Current Step:** Stage 5d complete - ready for Stage 5e (Testing Plan Update)
**Current Guide:** `STAGE_5e_post_feature_testing_update_guide.md` (ready to read)
**Guide Last Read:** 2026-01-02 (Stage 5d guide)

**Critical Rules from Stage 5e:**
- Update epic_smoke_test_plan.md based on feature_01 actual implementation
- Add integration points discovered during implementation
- Reassess test scenarios based on real code
- Keep testing plan current as epic evolves

**Progress:** Feature 01 Stage 5d COMPLETE
- All remaining features reviewed (feature_02) ✅
- Spec updates applied (minor logging pattern clarification) ✅
- No features needing rework ✅
- Epic README updated with alignment review summary ✅
- feature_02 ready for Stage 5a ✅

**Next Action:** Begin Stage 5e (Testing Plan Update) for feature_01 - Read STAGE_5e_post_feature_testing_update_guide.md
**Blockers:** None

**User Sign-Off:** ✅ Approved on 2026-01-01 (Stage 3)

**Features Completed Through Stage 5d:**
1. ✅ feature_01_win_rate_sim_json_integration (Win Rate Sim JSON integration)
   - Implementation: COMPLETE (100% test pass rate, 2463/2463 tests)
   - Stage 5d: COMPLETE (feature_02 spec aligned)
   - Ready for: Stage 5e (Testing Plan Update)
2. ⏸️ feature_02_accuracy_sim_json_integration (Accuracy Sim JSON integration)
   - Spec updated based on feature_01 implementation (minor logging updates)
   - Ready for: Stage 5a (TODO Creation)

**Total Components:**
- 6 Python files affected across both features
- Shared patterns identified (player_data/ subfolder, array indexing)
- Intentional differences documented (caching vs on-demand)

---

## Epic Overview

**Epic Goal:**
Update the Simulation module (both Win Rate Sim and Accuracy Sim) to work with the new JSON-based player data structure instead of the legacy players.csv and players_projected.csv format. This epic restores simulation functionality that was broken when the league helper module transitioned to positional JSON files.

**Epic Scope:**
- **IN SCOPE:**
  - Update Win Rate Sim to load JSON files from week folders instead of CSV files
  - Update Accuracy Sim to load JSON files from week folders instead of CSV files
  - Handle changes to field names (drafted_by, locked, projected_points, actual_points)
  - Verify Week 17 scoring uses correct folders (week_17 for projected, week_18 for actual)
- **OUT OF SCOPE:**
  - Changing simulation logic or algorithms (maintain same functionality)
  - Updating simulation user interface or command-line arguments
  - Adding new features to simulations

**Key Outcomes:**
1. Win Rate Sim and Accuracy Sim maintain same functionality as before
2. Both simulations correctly load JSON files from week folders
3. Field name changes (drafted_by, locked, projected_points, actual_points arrays) handled correctly
4. Week 17 assessment uses week_17 folders for projected_points and week_18 folders for actual_points

**Original Request:** `integrate_new_player_data_into_simulation_notes.txt`

---

## Epic Progress Tracker

**Overall Status:** 0/2 features complete (feature_01 at Stage 5d ✅, feature_02 ready for Stage 5a)

| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5a | Stage 5b | Stage 5c | Stage 5d | Stage 5e |
|---------|---------|---------|---------|---------|----------|----------|----------|----------|----------|
| feature_01_win_rate_sim_json_integration | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ◻️ |
| feature_02_accuracy_sim_json_integration | ✅ | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ | ◻️ |

**Legend:**
- ✅ = Complete
- ◻️ = Not started or in progress

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

### Feature 01: Win Rate Simulation JSON Integration
**Folder:** `feature_01_win_rate_sim_json_integration/`
**Purpose:** Update Win Rate Sim to load player data from 6 position-specific JSON files per week instead of CSV files
**Status:** Stage 2 complete ✅
**Dependencies:** None (foundation feature)
**Key Details:**
- 4 files to modify (SimulationManager, SimulatedLeague, DraftHelperTeam, SimulatedOpponent)
- ~150 LOC, MEDIUM complexity
- Needs JSON parsing method to extract week-specific data from arrays
- Pre-loads and caches all 17 weeks for performance

### Feature 02: Accuracy Simulation JSON Integration
**Folder:** `feature_02_accuracy_sim_json_integration/`
**Purpose:** Update Accuracy Sim to load player data from JSON files, verify Week 17/18 logic, ensure DEF/K evaluation is correct
**Status:** Stage 2 complete ✅
**Dependencies:** None (parallel to Feature 1)
**Key Details:**
- 2 files to modify (AccuracySimulationManager, ParallelAccuracyRunner)
- ~40-50 LOC, LOW complexity
- Simpler than Feature 1: just file copying, no parsing needed
- Loads 1 week per evaluation (on-demand, no caching)
- Week 17/18 and DEF/K are validation tasks (no code changes needed)

---

## Stage 5d Alignment Review Summary

**Completed:** 2026-01-02 (after feature_01 Stage 5cc completion)
**Reviewed Features:** 1 (feature_02_accuracy_sim_json_integration)
**Features Needing Rework:** 0

### feature_02_accuracy_sim_json_integration Review

**Status:** Minor updates applied - Continue to Stage 5a ✅

**Findings:**
- Spec was already 95% aligned with feature_01 implementation
- 1 minor misalignment found: Error handling comment

**Updates Applied:**
- Updated error handling comment to reflect proactive logging pattern from feature_01
- Calling code should log warnings (not assume PlayerManager will)
- Logging pattern: `self.logger.warning(f"Missing {position_file}...")`
- Updated spec.md with feature_01 reference (SimulatedLeague.py:235)
- Updated checklist.md Question 7 with actual approach

**Impact:**
- MINOR - Just comment clarification, no algorithm changes
- Ready to proceed to Stage 5a normally
- No rework needed

**Commit:** feat/KAI-3: Update feature_02 spec based on feature_01 implementation (d1cfb7a)

---

## Bug Fix Summary

**Bug Fixes Created:** 0

No bug fixes created yet

---

## Epic-Level Files

**Created in Stage 1:**
- `EPIC_README.md` (this file) - ✅
- `epic_smoke_test_plan.md` - ✅ (INITIAL VERSION - will update in Stages 4, 5e)
- `epic_lessons_learned.md` - ✅
- `research/` folder - ✅
- `GUIDE_ANCHOR.md` - ✅
- `integrate_new_player_data_into_simulation_notes.txt` - ✅ (original epic request)

**Feature Folders:**
- `feature_01_win_rate_sim_json_integration/` - Win Rate Sim JSON integration
- `feature_02_accuracy_sim_json_integration/` - Accuracy Sim JSON integration

**Bug Fix Folders:**
None

---

## Workflow Checklist

**Stage 1 - Epic Planning:**
- [x] Git branch created (epic/KAI-3)
- [x] EPIC_TRACKER.md updated
- [x] Initial commit made
- [x] Epic folder created
- [x] Epic request file moved and renamed
- [x] EPIC_README.md created (this file)
- [x] All feature folders created (user approved, 2 features)
- [x] Initial `epic_smoke_test_plan.md` created
- [x] `epic_lessons_learned.md` created
- [x] `research/` folder created
- [x] `GUIDE_ANCHOR.md` created

**Stage 2 - Feature Deep Dives:**
- [ ] ALL features have `spec.md` complete (1/2 done)
- [ ] ALL features have `checklist.md` resolved (1/2 done)
- [x] ALL feature `README.md` files created

**Stage 3 - Cross-Feature Sanity Check:**
- [ ] All specs compared systematically
- [ ] Conflicts resolved
- [ ] User sign-off obtained

**Stage 4 - Epic Testing Strategy:**
- [ ] `epic_smoke_test_plan.md` updated based on deep dives
- [ ] Integration points identified
- [ ] Epic success criteria defined

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

No deviations from guides

---

## Epic Completion Summary

{This section filled out in Stage 7}
