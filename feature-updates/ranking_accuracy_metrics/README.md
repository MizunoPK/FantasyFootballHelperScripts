# Ranking Accuracy Metrics - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** DEVELOPMENT (Sub-Feature Structure)
**Current Step:** STEP 0 Complete - Feature broken into 5 sub-features
**Next Action:** Begin Sub-Feature 01 (core_metrics) - Iteration 1

### WHERE AM I RIGHT NOW? (Quick State Check)

```
Current Phase:  [ ] PLANNING  [ ] DEVELOPMENT  [X] POST-IMPL  [ ] COMPLETE
Current Step:   All 5 sub-features COMPLETE, ready for Post-Implementation QC
Blocked:        [X] NO  [ ] YES → Reason: ___________________
Next Action:    Begin Post-Implementation Phase (Requirement Verification + 3 QC Rounds)
Last Activity:  2025-12-21 - Completed sub-feature 05 (testing verification)
```

**Session Resume Instructions:**
1. Read this section first
2. Check the workflow checklist below for detailed progress
3. Continue from "Next Action" - do NOT restart the workflow

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [X] Phase 1: Initial Setup
  - [X] Create folder structure
  - [X] Move notes file
  - [X] Create README.md (this file)
  - [X] Create {feature_name}_specs.md
  - [X] Create {feature_name}_checklist.md
  - [X] Create {feature_name}_lessons_learned.md
- [X] Phase 2: Deep Investigation
  - [X] 2.1: Analyze notes thoroughly
  - [X] 2.2: Research codebase patterns
  - [X] 2.3: Populate checklist with questions
  - [X] 2.3.1: THREE-ITERATION question generation (MANDATORY)
  - [X] 2.4: CODEBASE VERIFICATION rounds (MANDATORY)
  - [X] 2.5: Performance analysis for options
  - [X] 2.6: Create DEPENDENCY MAP (ready to add to specs)
  - [X] 2.7: Update specs with context + dependency map (pending Phase 4)
  - [X] 2.8: VAGUENESS AUDIT (Q47 in checklist)
  - [X] 2.9: ASSUMPTIONS AUDIT (covered in checklist questions)
  - [X] 2.10: TESTING REQUIREMENTS ANALYSIS (Q31-Q36 in checklist)
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] User chose: resolve items one-by-one
- [x] Phase 4: Resolve Questions
  - [x] All checklist items resolved (47/47)
  - [ ] Specs updated with all decisions (next step)
- [ ] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 0: Sub-Feature Analysis - Feature broken into 5 sub-features
- [x] Sub-Feature 01: Core Metrics (01_core_metrics_todo.md) ✓ COMPLETE (commit: 64f3c56)
  - [x] 24 verification iterations
  - [x] Implementation (Tasks 1.1-1.4)
  - [x] Tests passing (100% - 15/15 new tests)
  - [x] Commit: "Phase 1 (core-metrics): Implement ranking metric calculations"
- [x] Sub-Feature 02: Data Structure (02_data_structure_todo.md) ✓ COMPLETE (commit: fc830b1)
  - Depends on: Sub-feature 01 ✓
  - [x] 24 verification iterations
  - [x] Implementation (Tasks 2.1-2.2)
  - [x] Tests passing (100% - 41/41 tests, 10 new)
  - [x] Commit: "Phase 2 (data-structure): Add RankingMetrics and extend AccuracyConfigPerformance"
- [x] Sub-Feature 03: Integration (03_integration_todo.md) ✓ COMPLETE (commit: ada8e90)
  - Depends on: Sub-features 01, 02 ✓
  - [x] Implementation (Tasks 3.1-3.3)
  - [x] Tests passing (100% - 608/608 simulation tests)
  - [x] Commit: "Phase 3 (integration): Wire ranking metrics into AccuracySimulationManager"
- [x] Sub-Feature 04: Output (04_output_todo.md) ✓ COMPLETE (commit: e8a5fdb)
  - Depends on: Sub-features 01, 02, 03 ✓
  - [x] Implementation (Tasks 4.1-4.2)
  - [x] Tests passing (100% - 41/41 tests)
  - [x] Commit: "Phase 4 (output): Update results display for ranking metrics"
- [x] Sub-Feature 05: Testing (05_testing_todo.md) ✓ COMPLETE (commit: 74855ad)
  - Depends on: All previous sub-features ✓
  - [x] Test verification complete (Tasks 5.1-5.5)
  - [x] Tests passing (100% - 608/608 simulation tests)
  - [x] Commit: "Phase 5 (testing): Verify comprehensive test coverage for ranking metrics"

**POST-IMPLEMENTATION PHASE**
- [x] Requirement Verification Protocol (complete - 100% coverage)
- [x] QC Round 1 (complete - 1 issue found and fixed)
- [x] Fix Issue #1 (update _log_parameter_summary method) - FIXED
- [x] QC Round 2 (complete - no issues found)
- [x] QC Round 3 (complete - no issues found)
- [x] Lessons Learned Review (complete - 1 guide recommendation documented)
- [x] All QC reports and lessons learned committed
- [ ] Move folder to done/ (final step)

**FEATURE COMPLETE** - Ready for production use

---

## What This Is

A replacement for Mean Absolute Error (MAE) in the accuracy simulation system. Instead of optimizing for exact point prediction accuracy, this feature optimizes for **ranking accuracy** - how well the scoring system identifies which players will outperform others. This produces configs that actually help with fantasy football decisions.

## Why We Need This

1. **Current accuracy simulation produces unusable configs** - It disables most scoring features (TEAM_QUALITY=0.0, PERFORMANCE=0.01, MATCHUP=0.03) to minimize MAE, but these configs perform poorly for actual decisions
2. **MAE is the wrong optimization target** - Fantasy decisions depend on relative rankings, not exact point totals. A config that's off by 2 points per player but correctly ranks them is better than one that's off by 1 point but gets rankings wrong
3. **Misalignment with win-rate simulation** - Win-rate sim achieves 77.8% with features enabled, but accuracy sim says optimal = features disabled. This makes accuracy sim useless for validation

## Scope

**IN SCOPE:**
- Replace MAE with pairwise decision accuracy as primary metric
- Add top-N overlap accuracy (how many predicted top-10 are actually top-10)
- Add Spearman rank correlation
- Calculate all metrics per-position (QB, RB, WR, TE)
- Integrate into AccuracySimulationManager to optimize for ranking metrics
- Keep MAE as diagnostic metric (not optimization target)

**OUT OF SCOPE:**
- Changes to win-rate simulation (already working correctly)
- Changes to the league helper scoring system
- New data sources or APIs

## Sub-Feature Breakdown

This feature has been broken into 5 sub-features per feature_development_guide.md STEP 0:

1. **01_core_metrics** - Implement ranking calculations (AccuracyCalculator)
   - Pairwise accuracy, Top-N overlap, Spearman correlation
   - Add scipy dependency
   - No dependencies on other sub-features

2. **02_data_structure** - Create RankingMetrics dataclass
   - Extend AccuracyConfigPerformance with ranking fields
   - Update is_better_than() to use pairwise_accuracy
   - Depends on: Sub-feature 01

3. **03_integration** - Wire into AccuracySimulationManager
   - Aggregate metrics across weeks/positions
   - Fisher z-transformation for Spearman
   - Depends on: Sub-features 01, 02

4. **04_output** - Update results display
   - JSON output, console logging
   - Threshold warnings
   - Depends on: Sub-features 01, 02, 03

5. **05_testing** - Comprehensive test suite
   - Unit tests, integration tests, parallel execution
   - Depends on: All previous sub-features

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `ranking_accuracy_metrics_notes.txt` | Original scratchwork notes from user |
| `ranking_accuracy_metrics_specs.md` | Main specification with detailed requirements |
| `ranking_accuracy_metrics_checklist.md` | Tracks open questions and decisions |
| `ranking_accuracy_metrics_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Current Problem with MAE
The current accuracy simulation finds "optimal" configs by minimizing Mean Absolute Error across all player predictions. This penalizes variance even when that variance correctly identifies player value differences. Result: Configs that minimize error but make bad decisions.

### Expected Outcome After This Feature
Accuracy-optimal configs will enable scoring features (weights > 0.5) and align with win-rate optimal configs. This makes accuracy simulation valuable for rapid iteration and weekly lineup optimization.

## What's Resolved
- Feature objective is clear from notes
- Primary metric identified: Pairwise decision accuracy
- Codebase architecture understood (AccuracyCalculator, AccuracySimulationManager, results storage)
- Data flow verified (player data format includes all needed fields)
- Libraries available (pandas for correlations, numpy for array ops - no new dependencies needed)
- 47 questions identified across 11 categories (algorithm, architecture, performance, testing, etc.)

## What's Still Pending
- All 47 checklist items need user decisions or investigation
- Dependency map needs to be added to specs
- Per-position implementation details
- Performance optimization strategy
- Integration approach finalization

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `ranking_accuracy_metrics_specs.md` for complete specifications
3. Read `ranking_accuracy_metrics_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
