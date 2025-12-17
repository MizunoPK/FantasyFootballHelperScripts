# Fix ConfigGenerator Horizon Behavior - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** DEVELOPMENT COMPLETE ✅
**Current Step:** All 5 Phases implemented + All tests passing (100%)
**Next Action:** Post-Implementation Phase - Requirement Verification and QC Rounds

### WHERE AM I RIGHT NOW? (Quick State Check)

```
Current Phase:  [COMPLETE] PLANNING  [COMPLETE] DEVELOPMENT  [→] POST-IMPL  [ ] COMPLETE
Current Step:   ALL 5 PHASES COMPLETE + All Tests Fixed
Blocked:        [x] NO  [ ] YES → Reason: ___________________
Next Action:    Begin Post-Implementation Phase (Requirement Verification Protocol)
Last Activity:  2025-12-17 - Test fixes complete: 100% pass rate (2293/2293 tests)
Progress:       Phases 1-5: 100% DONE ✅ | Tests: 2293/2293 (100%) ✅ | Ready for QC
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
  - [x] Create {feature_name}_specs.md
  - [x] Create {feature_name}_checklist.md
  - [x] Create {feature_name}_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] 2.1: Analyze notes thoroughly
  - [x] 2.2: Research codebase patterns
  - [x] 2.3: Populate checklist with questions
  - [x] 2.3.1: THREE-ITERATION question generation (MANDATORY) - 40 questions generated
  - [x] 2.4: CODEBASE VERIFICATION rounds (MANDATORY) - Round 2 complete, 7 findings documented
  - [x] 2.5: Performance analysis for options - Documented in checklist Q33-Q35
  - [x] 2.6: Create DEPENDENCY MAP - Complete in specs.md
  - [x] 2.7: Update specs with context + dependency map - Complete
  - [x] 2.8: VAGUENESS AUDIT - Complete, no vague language found
  - [x] 2.9: ASSUMPTIONS AUDIT - Complete, 8 assumptions documented
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] Wait for user direction
- [x] Phase 4: Resolve Questions
  - [x] All checklist items resolved [x] - 40/40 complete (100%)
  - [x] Specs updated with all decisions
- [x] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 1: Create TODO file
- [x] Step 2-6: All 24 Verification Iterations COMPLETE (200 findings)
- [x] Interface Verification - All contracts verified ✅
- [x] Implementation - ALL 5 PHASES COMPLETE ✅
  - [x] Created code_changes.md
  - [x] Phase 1: ConfigPerformance (HORIZONS, HORIZON_FILES) - 100% ✅
  - [x] Phase 2: ResultsManager 6-file support - 100% ✅
  - [x] Phase 3: ConfigGenerator core refactor - 100% ✅
  - [x] Phase 4: SimulationManager integration - 100% ✅
  - [x] Phase 5: AccuracySimulationManager integration - 100% ✅
  - [x] Test pass rate: 2293/2293 (100%) ✅ - TARGET ACHIEVED

**POST-IMPLEMENTATION PHASE**
- [ ] Requirement Verification Protocol
- [ ] QC Round 1
- [ ] QC Round 2
- [ ] QC Round 3
- [ ] Lessons Learned Review
- [ ] Apply guide updates (if any)
- [ ] Move folder to done/

---

## What This Is

This feature fixes ConfigGenerator's horizon behavior to support true "tournament" optimization where each horizon's optimal config from parameter N competes independently when testing parameter N+1. Currently, ConfigGenerator merges all 5 horizon files into a single baseline, which defeats the purpose of having separate optimal configs per horizon.

## Why We Need This

1. **Correctness**: Current behavior merges all horizon configs into one, so all test configs start from same baseline instead of each horizon's optimal value
2. **Tournament Model**: Each horizon's champion should compete with new parameter values independently
3. **Affects Both Simulations**: Win-rate and accuracy simulations both have this bug
4. **Breaking Change**: Will change optimal parameters found (more thorough exploration)

## Scope

**IN SCOPE:**
- Refactor ConfigGenerator to store 5 separate baseline configs (no merging)
- Generate test values per horizon (5 arrays, one per horizon)
- Provide configs on demand by horizon + test index
- Update win-rate SimulationManager to use new interface
- Update accuracy AccuracySimulationManager to use new interface
- Deprecate NUM_PARAMETERS_TO_TEST (only one parameter at a time)

**OUT OF SCOPE:**
- Changes to parameter definitions or ranges
- Changes to results tracking or optimal config selection
- Changes to parallel execution patterns
- UI/CLI changes beyond deprecating NUM_PARAMETERS_TO_TEST

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `fix_config_generator_horizon_behavior_notes.txt` | Original feature request notes |
| `fix_config_generator_horizon_behavior_specs.md` | Main specification with detailed requirements |
| `fix_config_generator_horizon_behavior_checklist.md` | Tracks open questions and decisions |
| `fix_config_generator_horizon_behavior_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Current Problem
ConfigGenerator.load_baseline_from_folder() merges all 5 horizon files (draft_config.json, week1-5.json, week6-9.json, week10-13.json, week14-17.json) into a single unified config. This means all test configs for parameter N start from the same baseline, instead of each horizon starting from its own optimal value from parameter N-1.

### Desired Tournament Behavior
For parameter N, ConfigGenerator should:
1. Load all 5 horizon baseline configs separately (no merging)
2. Generate test values for each horizon independently
3. Provide complete configs on demand: "Give me config for horizon X, test value Y, parameter Z"

### Impact
- 5x more configs tested per parameter (5 horizons × N test values instead of just N test values)
- This is the INTENDED behavior per original design
- More computationally expensive but finds better optimal parameters

## Key Findings from Phase 2 Investigation

### Critical Discovery: Accuracy Sim Is Ahead
- **Accuracy simulation ALREADY has 6-file support** including draft_config.json
- **Win-rate simulation is BEHIND** - still uses 5-file structure
- This feature will bring win-rate sim up to parity with accuracy sim

### Codebase State (7 findings from Round 2 verification):
1. Both ConfigGenerator and ResultsManager currently require exactly 5 files (no draft_config.json)
2. Accuracy sim's AccuracyResultsManager already saves draft_config.json (ahead of win-rate)
3. Win-rate sim has NO references to draft_config.json (confirmed user's statement)
4. WEEK_RANGES constant exists in ConfigPerformance.py: `["1-5", "6-9", "10-13", "14-17"]`
5. Accuracy sim uses DIFFERENT naming: `'week_1_5'` (underscores) vs `'1-5'` (hyphens)
6. BASE_CONFIG_PARAMS and WEEK_SPECIFIC_PARAMS exist in ResultsManager
7. ConfigGenerator already has `is_base_config_param()` and `is_week_specific_param()` methods

### Files Requiring Updates:
- `simulation/shared/ConfigGenerator.py` - Add 6-file support, horizon-based interface
- `simulation/shared/ResultsManager.py` - Update required_files from 5 to 6
- `simulation/win_rate/SimulationManager.py` - Use new ConfigGenerator interface
- `simulation/accuracy/AccuracySimulationManager.py` - Use new ConfigGenerator interface

### Open Questions: 40 questions across 3 iterations
- File structure & loading (Q1-Q4)
- ConfigGenerator interface (Q5-Q9)
- Horizon naming & constants (Q10-Q11)
- Data structures (Q12-Q13)
- Win-rate integration (Q14-Q17)
- Accuracy integration (Q18-Q21)
- Interface design (Q22-Q23)
- ResultsManager changes (Q24-Q26)
- Error handling (Q27-Q29)
- Testing (Q30-Q32)
- Performance (Q33-Q35)
- Deprecation (Q36-Q38)
- Implementation strategy (Q39-Q40)

## What's Resolved
- ✅ Feature scope defined with 6-file structure
- ✅ High-level approach documented
- ✅ NUM_PARAMETERS_TO_TEST deprecation decided
- ✅ Phase 2 investigation complete (40 questions generated, 7 findings documented)
- ✅ Dependency map created
- ✅ Vagueness audit complete
- ✅ Assumptions documented (8 total)
- ✅ Phase 3: Findings presented to user
- ✅ Phase 4: All 40 checklist questions resolved (100%)
- ✅ Interface design finalized (unified auto-detection interface)
- ✅ Specs updated with all resolutions
- ✅ **PLANNING PHASE COMPLETE**
- ✅ **Phase 1 (ConfigPerformance) - 100% complete**
- ✅ **Phase 2 (ResultsManager) - 100% complete**
- ✅ **Phase 3 (ConfigGenerator) - Core implementation complete**

## Current State Summary (2025-12-17)

### ✅ ALL WORK COMPLETE:

**Phase 1: ConfigPerformance Constants**
- Added HORIZONS and HORIZON_FILES constants
- 22 tests written and passing
- All 73/73 ConfigPerformance tests passing

**Phase 2: ResultsManager 6-File Support**
- Updated required_files, week_range_files mappings
- Added 'ros' horizon support for draft_config.json
- 7 tests added/modified, all passing
- All 65/65 ResultsManager tests passing

**Phase 3: ConfigGenerator Core Refactor**
- Refactored __init__() - new 2-parameter signature
- Refactored load_baseline_from_folder() - returns 5 horizon configs
- Implemented generate_horizon_test_values() - auto-detects param type
- Implemented get_config_for_horizon() - returns config with test value
- Implemented update_baseline_for_horizon() - smart baseline updates
- Added 3 helper methods for param extraction/application
- Added backward compatibility properties
- All 52/52 ConfigGenerator tests passing ✅

**Phase 4: SimulationManager Integration**
- Updated to use new 2-parameter ConfigGenerator interface
- Optimization loop refactored for horizon-based test values
- Saves all 6 files including draft_config.json
- All tests passing ✅

**Phase 5: AccuracySimulationManager Integration**
- Updated to use new 2-parameter ConfigGenerator interface
- Tournament model implemented (per-horizon optimization)
- All tests passing ✅

### 📊 Final Test Metrics:
- **Overall**: 2293/2293 tests passing (100%) ✅
- **All Phases**: 100% passing
- **Integration Tests**: All passing
- **Ready for Post-Implementation Phase**

### 🎯 Key Files Modified:
1. `simulation/shared/ConfigPerformance.py` - HORIZONS and HORIZON_FILES constants
2. `simulation/shared/ResultsManager.py` - 6-file structure support
3. `simulation/shared/ConfigGenerator.py` - Complete horizon-based refactor
4. `simulation/win_rate/SimulationManager.py` - New interface integration
5. `simulation/accuracy/AccuracySimulationManager.py` - Tournament model
6. All test files updated and passing

## Implementation Complete ✅
- **Development Phase**: 100% COMPLETE
- **Test Pass Rate**: 100% (2293/2293)
- **Next**: Post-Implementation Phase (Requirement Verification + 3 QC Rounds)

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `fix_config_generator_horizon_behavior_specs.md` for complete specifications
3. Read `fix_config_generator_horizon_behavior_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
