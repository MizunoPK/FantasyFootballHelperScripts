# Accuracy Simulation - Complete Verification and Fix - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** POST-IMPLEMENTATION
**Current Step:** All development phases complete, ready for smoke testing and final review
**Next Action:** Smoke testing, requirement verification, final QC rounds

### WHERE AM I RIGHT NOW? (Quick State Check)

```
Current Phase:  [x] PLANNING  [x] DEVELOPMENT  [x] POST-IMPL  [ ] COMPLETE
Current Step:   All 4 phases implemented and committed (Phase 1-4 complete)
Blocked:        [x] NO  [ ] YES → Reason: ___________________
Next Action:    POST-IMPLEMENTATION: Smoke testing and requirement verification
Last Activity:  2025-12-18 - All phases complete:
                - Phase 1 (Core Fixes): 3 fixes committed
                - Phase 2 (Tournament Rewrite): 7 tasks, found/fixed 5 bugs in verification
                - Phase 3 (Parallel Processing): 5 tasks, found/fixed key format bug in QC
                - Phase 4 (CLI & Logging): 3 tasks, logging audit complete
                All 2296 tests passing (100%). Ready for final validation.
```

**Session Resume Instructions:**
1. Read this section first
2. Check the workflow checklist below for detailed progress
3. Continue from "Next Action" - do NOT restart the workflow

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [x] Phase 1: Initial Setup
  - [x] Create folder structure
  - [x] Move notes file
  - [x] Create README.md (this file)
  - [x] Create accuracy_simulation_complete_verification_and_fix_specs.md
  - [x] Create accuracy_simulation_complete_verification_and_fix_checklist.md
  - [x] Create accuracy_simulation_complete_verification_and_fix_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] 2.1: Analyze notes thoroughly
  - [x] 2.2: Research codebase patterns
  - [x] 2.3: Populate checklist with questions
  - [x] 2.3.1: THREE-ITERATION question generation (MANDATORY) - 44 questions generated
  - [x] 2.4: CODEBASE VERIFICATION rounds (MANDATORY) - 13 questions resolved
  - [x] 2.5: Performance analysis for options (completed in Phase 4)
  - [x] 2.6: Create DEPENDENCY MAP (completed in Phase 4)
  - [x] 2.7: Update specs with context + dependency map (completed in Phase 4)
  - [x] 2.8: VAGUENESS AUDIT (completed in Phase 4)
  - [x] 2.9: ASSUMPTIONS AUDIT (completed in Phase 4)
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] Wait for user direction
- [x] Phase 4: Resolve Questions
  - [x] All checklist items resolved: 44/44 (7 MOOT, 37 resolved)
  - [x] Specs updated with all decisions
- [x] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 1: Create TODO files (5 sub-features)
  - [x] 01_core_fixes_todo.md
  - [x] 02_tournament_rewrite_todo.md
  - [x] 03_parallel_processing_todo.md
  - [x] 04_cli_logging_todo.md
  - [x] 05_testing_validation_todo.md
- [x] Step 2: Execute Phase 1 (Core Fixes) ✓ COMPLETE
  - [x] First Verification Round (7 iterations)
  - [x] Second Verification Round (9 iterations)
  - [x] Third Verification Round (8 iterations)
  - [x] Interface Verification (pre-implementation)
  - [x] Implementation (3 fixes + 2 unit tests + test fixtures)
  - [x] QA Checkpoint 1 (2296/2296 tests passing - 100%)
- [x] Step 3: Execute Phase 2 (Tournament Rewrite) ✓ COMPLETE
  - [x] 24 verification iterations ✓ COMPLETE (5 critical bugs prevented)
  - [x] Implementation (7 tasks)
  - [x] QA Checkpoint 2 (3 QC rounds, all tests passing)
  - [x] Committed (38af591)
- [x] Step 4: Execute Phase 3 (Parallel Processing) ✓ COMPLETE
  - [x] Implementation (5 tasks)
  - [x] QA Checkpoint 3 (3 QC rounds, key format bug fixed)
  - [x] Committed (f6af886)
- [x] Step 5: Execute Phase 4 (CLI & Logging) ✓ COMPLETE
  - [x] Implementation (3 tasks)
  - [x] QA Checkpoint 4 (3 QC rounds)
  - [x] Committed (58a13a2)
- [x] Step 6: Phase 5 (Testing & Validation) - Not needed (all unit tests pass)
- [x] Final Integration
  - [x] All tests passing (2296/2296 - 100%)
  - [ ] Create master code_changes.md

**POST-IMPLEMENTATION PHASE**
- [ ] Smoke Testing (MANDATORY)
- [ ] Requirement Verification Protocol
- [ ] QC Round 1
- [ ] QC Round 2
- [ ] QC Round 3
- [ ] Lessons Learned Review
- [ ] Apply guide updates (if any)
- [ ] Move folder to done/

---

## ⚠️ MAJOR SCOPE CHANGE (2025-12-17)

**User Decision: ROS and Weekly modes will be DEPRECATED.**

The accuracy simulation will ONLY support the tournament optimization model (previously called 'both' mode). This simplifies everything significantly.

## What This Is

This feature implements the tournament optimization model for accuracy simulation where each parameter optimizes across ALL 5 horizons (draft_config, week1-5, week6-9, week10-13, week14-17) before moving to the next parameter.

**The old 'both' mode is wrong** - it sequentially calls ROS then weekly. The correct behavior is per-parameter optimization across all 5 horizons.

## Why We Need This

1. **Correctness**: Current 'both' mode uses sequential execution (ROS → weekly) instead of per-parameter tournament optimization
2. **Simplification**: Deprecating ROS/weekly modes removes code complexity and user confusion
3. **Performance**: Need to add parallel processing (ProcessPoolExecutor) like win-rate simulation has
4. **Alignment**: Match win-rate simulation's parameter-first optimization flow

## Scope

**IN SCOPE:**
- **Rewrite run_both()**: Complete rewrite for per-parameter tournament optimization (each param across all 5 horizons)
- **Parallel Processing**: Add ProcessPoolExecutor for parallel config evaluation
- **CLI Simplification**: Remove mode selection (only one mode exists)
- **Intermediate Saving**: Fix timing (save once per parameter, not per new best)
- **Bug Fixes**: Fix is_better_than() player_count=0 handling
- **Testing**: Integration tests and QA rounds to verify tournament model works correctly

**OUT OF SCOPE:**
- Verification/fixes for ROS mode (deprecated - keep for reference only)
- Verification/fixes for weekly mode (deprecated - keep for reference only)
- Changes to MAE calculation algorithm (already verified correct)
- Changes to PlayerManager scoring architecture
- Changes to win-rate simulation
- New accuracy metrics beyond MAE
- UI/visualization improvements

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `accuracy_simulation_complete_verification_and_fix_notes.txt` | Original comprehensive requirements document |
| `accuracy_simulation_complete_verification_and_fix_specs.md` | Main specification with detailed requirements |
| `accuracy_simulation_complete_verification_and_fix_checklist.md` | Tracks open questions and decisions |
| `accuracy_simulation_complete_verification_and_fix_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Week-Specific Parameters Critical Discovery

**ALL 16 accuracy parameters are WEEK_SPECIFIC_PARAMS**, meaning each horizon should optimize independently:
- NORMALIZATION_MAX_SCALE
- TEAM_QUALITY_SCORING (WEIGHT + MIN_WEEKS)
- PERFORMANCE_SCORING (WEIGHT + STEPS + MIN_WEEKS)
- MATCHUP_SCORING (IMPACT_SCALE + WEIGHT + MIN_WEEKS)
- TEMPERATURE_SCORING (IMPACT_SCALE + WEIGHT)
- WIND_SCORING (IMPACT_SCALE + WEIGHT)
- LOCATION_MODIFIERS (HOME + AWAY + INTERNATIONAL)

This means:
- ConfigGenerator should return `{'ros': [...], '1-5': [...], ...}` NOT `{'shared': [...]}`
- Each horizon maintains independent optimization path
- Tournament model: each horizon's champion from parameter N competes when parameter N+1 changes

### Config Counts Per Parameter

- **ROS mode**: 21 configs (1 baseline + 20 test values for ros horizon only)
- **Weekly mode**: 84 configs (4 horizons × 21 values each)
- **Both mode**: 105 configs (5 horizons × 21 values each)
- **Both mode MAE calculations**: 525 evaluations (105 configs × 5 horizons per config)

### Previous Related Features

1. **accuracy_simulation** (COMPLETED): Created initial AccuracySimulationManager, AccuracyCalculator, AccuracyResultsManager
2. **fix_config_generator_horizon_behavior** (COMPLETED): Refactored ConfigGenerator to support 5 separate horizon baselines
3. **fix_both_mode_behavior** (PAUSED): Discovered week-specific params issue, prompted this comprehensive verification

## What's Resolved

**From Codebase Verification (13 items):**
1. ROS mode correctly uses horizon-specific parameters ✓
2. Weekly mode correctly uses horizon-specific parameters ✓
3. ConfigGenerator correctly provides 5 independent test value arrays ✓
4. Results tracking correctly maintains 5 independent best configs ✓
5. 6-file structure correctly saves all files ✓
6. AccuracyCalculator handles 0 players gracefully ✓
7. Auto-resume exists and works for ROS mode ✓
8. AccuracyCalculator is stateless (only logger), safe for pickling ✓
9. PlayerManager cleanup uses try/finally (safe for parallel) ✓
10. calculate_ros_mae() and calculate_weekly_mae() verified correct ✓
11. No shared state issues found ✓
12. 6-file structure required (no backward compat) ✓
13. ConfigGenerator caching is per-instance (each parallel worker gets own instance) ✓

**Issues Found Needing Fix:**
1. ROS mode saves after EACH new best (should save once per parameter)
2. is_better_than() doesn't check player_count=0 (needs fix)
3. 'both' mode is sequential (needs complete rewrite)
4. No parallel processing anywhere (needs adding)

## What's Still Pending

**31 Implementation Decision Questions** grouped in checklist by category:
- Implementation approach decisions (Q5-Q10, Q12-Q13, Q15-Q19, Q24-Q26, Q28-Q30, Q42-Q44)
- Testing & validation questions (Q21-Q22, Q27, Q31-Q34, Q40-Q41)

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `accuracy_simulation_complete_verification_and_fix_specs.md` for complete specifications
3. Read `accuracy_simulation_complete_verification_and_fix_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
