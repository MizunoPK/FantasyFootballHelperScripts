# Fix 'both' Mode Behavior - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** PLANNING
**Current Step:** Phase 2 Complete - Ready for Phase 3
**Next Action:** Phase 3 - Present findings to user and wait for direction

### WHERE AM I RIGHT NOW? (Quick State Check)

```
Current Phase:  [x] PLANNING  [ ] DEVELOPMENT  [ ] POST-IMPL  [ ] COMPLETE
Current Step:   Phase 2 complete, ready for Phase 3 (user direction)
Blocked:        [x] NO  [ ] YES → Reason: ___________________
Next Action:    Phase 3: Present findings to user, wait for direction
Last Activity:  2025-12-17 16:45 - Completed codebase research, generated 28 questions
Progress:       THREE-ITERATION questions complete, ready for user input
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
  - [x] 2.3.1: THREE-ITERATION question generation (MANDATORY)
  - [x] 2.4: CODEBASE VERIFICATION rounds (via file reads)
  - [ ] 2.5: Performance analysis for options (deferred to user Q&A)
  - [ ] 2.6: Create DEPENDENCY MAP (deferred to user Q&A)
  - [ ] 2.7: Update specs with context + dependency map (after user input)
  - [ ] 2.8: VAGUENESS AUDIT (after user input)
  - [ ] 2.9: ASSUMPTIONS AUDIT (after user input)
- [ ] Phase 3: Report and Pause
  - [ ] Present findings to user
  - [ ] Wait for user direction
- [ ] Phase 4: Resolve Questions
  - [ ] All checklist items resolved [x]
  - [ ] Specs updated with all decisions
- [ ] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [ ] Step 1: Create TODO file
- [ ] Step 2: First Verification Round (7 iterations)
- [ ] Step 3: Create questions file (if needed)
- [ ] Step 4: Update TODO with answers
- [ ] Step 5: Second Verification Round (9 iterations)
- [ ] Step 6: Third Verification Round (8 iterations)
- [ ] Interface Verification (pre-implementation)
- [ ] Implementation
  - [ ] Create code_changes.md
  - [ ] Execute TODO tasks
  - [ ] Tests passing (100%)

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

## What This Is

This feature fixes the accuracy simulation's 'both' mode to correctly evaluate each configuration across all 5 time horizons (ROS + 4 weekly ranges) simultaneously, rather than optimizing them sequentially. This implements true tournament-style optimization where each horizon's optimal config competes independently.

## Why We Need This

1. **Correctness**: Current 'both' mode runs ROS optimization completely, then weekly optimization completely - this tests each config twice instead of once
2. **Efficiency**: Testing each config once (with 5 accuracy calculations) is faster than sequential ROS→weekly approach
3. **Better Parameters**: Finding parameters that work well across ALL time horizons simultaneously produces more robust predictions

## Scope

**IN SCOPE:**
- Rewrite `run_both()` to evaluate all 5 horizons per config
- Create `_evaluate_config_both()` method
- Implement parallel processing with ProcessPoolExecutor (8 workers default)
- Add `--max-workers` and `--use-processes` CLI flags
- Support iterative base config behavior (5 different bases per parameter)
- Tournament model: each horizon's champion competes independently

**OUT OF SCOPE:**
- Changes to ROS-only or weekly-only modes
- Changes to accuracy calculation algorithms
- Changes to results storage format (already 6-file structure from previous fixes)

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `fix_both_mode_behavior_notes.txt` | Original scratchwork notes from user |
| `fix_both_mode_behavior_specs.md` | Main specification with detailed requirements |
| `fix_both_mode_behavior_checklist.md` | Tracks open questions and decisions |
| `fix_both_mode_behavior_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### ConfigGenerator Fix Completed

**IMPORTANT**: This feature was previously blocked by a ConfigGenerator bug (merging all horizon files into single baseline). That bug has been FIXED as of 2025-12-17 (commit b0cf69f).

ConfigGenerator now:
- Supports 6-file structure (draft_config.json + league_config.json + 4 week configs)
- Stores 5 separate baseline configs (no merging)
- Generates test values per horizon independently
- Provides configs on demand by horizon + test index

### Current Implementation Problem

The `run_both()` method currently calls `run_ros_optimization()` followed by `run_weekly_optimization()`, which means configs are tested twice - once for ROS accuracy, once for weekly accuracy. This is incorrect.

### Desired Tournament Behavior

Each parameter optimization should:
1. Start from 5 different base configs (one best from each horizon from previous parameter)
2. Generate test configs by varying the current parameter
3. For each config: evaluate across ALL 5 horizons (ROS + 4 weekly)
4. Track 5 independent "champions" (best for each horizon)
5. Save 5 different optimal configs for next parameter

## What's Resolved

*(Will be populated during Phase 4)*

## What's Still Pending

*(Will be populated during Phase 2)*

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `fix_both_mode_behavior_specs.md` for complete specifications
3. Read `fix_both_mode_behavior_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
