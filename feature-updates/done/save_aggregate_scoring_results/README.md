# Save Aggregate Scoring Results - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** COMPLETE ✅
**Current Step:** All phases complete - Feature ready for finalization
**Next Action:** Move folder to done/ and commit

### WHERE AM I RIGHT NOW? (Quick State Check)

```
Current Phase:  [ ] PLANNING  [ ] DEVELOPMENT  [ ] POST-IMPL  [x] COMPLETE
Current Step:   All verification complete - ready to finalize
Blocked:        [x] NO  [ ] YES → Reason: ___________________
Next Action:    Move to done/ and commit changes
Last Activity:  2025-12-22 - Smoke test PASSED, lessons learned documented, zero issues found
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
  - [x] Create save_aggregate_scoring_results_specs.md
  - [x] Create save_aggregate_scoring_results_checklist.md
  - [x] Create save_aggregate_scoring_results_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] 2.1: Analyze notes thoroughly
  - [x] 2.2: Research codebase patterns
  - [x] 2.3: Populate checklist with questions
  - [x] 2.3.1: THREE-ITERATION question generation (MANDATORY)
  - [x] 2.4: CODEBASE VERIFICATION rounds (MANDATORY) - Round 1 & Round 2 complete
  - [x] 2.4.1: EXECUTION PATH COVERAGE analysis (MANDATORY)
  - [x] 2.5: Performance analysis for options
  - [x] 2.6: Create DEPENDENCY MAP (completed in Phase 1, verified in Phase 2)
  - [x] 2.7: Update specs with context + dependency map
  - [x] 2.8: VAGUENESS AUDIT (flagged all ambiguous phrases)
  - [x] 2.9: ASSUMPTIONS AUDIT (completed)
  - [x] 2.10: TESTING REQUIREMENTS ANALYSIS (MANDATORY)
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] User walked through questions one-by-one
- [x] Phase 4: Resolve Questions
  - [x] All 10 user decision questions resolved
  - [x] Specs updated with all decisions
  - [x] Checklist updated with all resolutions
- [x] Planning Complete - Ready for Implementation ✅

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 0: Sub-feature analysis (1 of 6 criteria → single TODO)
- [x] Step 1: Create TODO file
- [x] Step 2: First Verification Round (7 iterations) ✓
- [x] Step 3: Create questions file (SKIPPED - no questions needed)
- [x] Step 4: Update TODO with answers (SKIPPED - no questions)
- [x] Step 5: Second Verification Round (9 iterations) ✓
- [x] Step 6: Third Verification Round (8 iterations) ✓
- [x] Implementation ✅
  - [x] SaveCalculatedPointsManager.py created
  - [x] LeagueHelperManager.py integrated (menu item 5)
  - [x] Unit tests created (8 new tests)
  - [x] Unit tests updated (14 LeagueHelperManager tests)
  - [x] All 2335 tests pass (100%)

**POST-IMPLEMENTATION PHASE** ✅ **COMPLETE**
- [x] Requirement Verification Protocol (38/38 requirements verified)
- [x] Smoke Testing (end-to-end with real data - PASSED)
- [x] QC Round 1 (code review + integration - PASSED)
- [x] QC Round 2 (deep verification + semantic diff - PASSED)
- [x] QC Round 3 (adversarial review - PASSED)
- [x] Lessons Learned Review (zero issues found)
- [x] Apply guide updates (none needed - guides worked perfectly)
- [ ] Move folder to done/ ← **NEXT STEP**
- [ ] Commit changes

---

## What This Is

A new menu mode in the League Helper that saves calculated projected points for all players to JSON files in the historical_data folder structure. This feature also copies relevant data files (players.csv, configs/, team_data/, etc.) from the main data folder into historical_data for archival purposes.

## Why We Need This

1. **Historical Data Archive**: Create a permanent record of how players were scored at specific points in the season
2. **Analysis & Comparison**: Enable comparing scoring algorithms across different weeks or seasons
3. **Reproducibility**: Store both input data (copied files) and output data (calculated scores) together
4. **Decouple from player-data-fetcher**: Move historical data saving responsibility from fetcher to league helper where it's more appropriate

## Scope

**IN SCOPE:**
- New top-level menu item "Save Calculated Projected Points"
- Save calculated scores to JSON format: `{player_id: calculated_points}`
- Use same scoring logic as StarterHelper mode
- Handle both weekly (week 1-17) and season-long (week 0) scoring
- Copy relevant data files from data/ to data/historical_data/{SEASON}/{WEEK}/
- Output paths:
  - Weekly: `data/historical_data/{SEASON}/{WEEK}/calculated_projected_points.json`
  - Season-long: `data/historical_data/{SEASON}/calculated_season_long_projected_points.json`

**OUT OF SCOPE:**
- Modifying player-data-fetcher (that's a separate task)
- Loading or using the saved JSON files (future enhancement)
- Comparing scores across weeks (analysis feature for later)
- UI for visualizing historical data

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `save_aggregate_scoring_results_notes.txt` | Original scratchwork notes from user |
| `save_aggregate_scoring_results_specs.md` | Main specification with detailed requirements |
| `save_aggregate_scoring_results_checklist.md` | Tracks open questions and decisions |
| `save_aggregate_scoring_results_todo.md` | Implementation TODO and iteration tracking |
| `save_aggregate_scoring_results_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Menu System Integration
- Need to understand how LeagueHelperManager handles menu modes
- New mode should appear at top level (not nested in submenu)
- Menu label: "Save Calculated Projected Points"

### Scoring Logic
- Must match StarterHelper scoring exactly
- Need to identify the specific method call and parameters used by StarterHelper
- Scoring differs between weekly (specific week) and season-long (week 0)

### Historical Data Structure
- Folder structure: `data/historical_data/{SEASON}/{WEEK}/`
- Need to understand what files player-data-fetcher currently copies
- Files to copy: players.csv, players_projected.csv, game_data.csv, drafted_data.csv, team_data/, configs/

## What's Resolved

**From Phase 1:**
- Feature objective is clear
- Output file format defined (JSON with player_id keys)
- Output paths specified for weekly vs season-long

**From Phase 2 Investigation (Completed 2025-12-22):**
- **Codebase patterns identified:**
  - Menu integration: 5-step pattern documented (import, init, menu, dispatch, method)
  - Scoring logic: StarterHelper parameters confirmed (lines 405-419)
  - Files to copy: players.csv, players_projected.csv, game_data.csv, drafted_data.csv, team_data/, configs/
  - Week format: Zero-padded (f"{week:02d}") to match existing pattern
  - Idempotent behavior: Skip if folder exists (like player-data-fetcher)
  - Error handling: Warning for missing files, continue operation

- **Performance analysis:**
  - Expected execution: 1-4 seconds (acceptable for menu operation)
  - Bottleneck: File copying (~36 writes) slower than scoring
  - Recommendation: Sequential loop (no parallelization needed)

- **Execution paths:**
  - Single path: Menu selection → execute() → return
  - No parallel/async/batch variants

- **Testing requirements:**
  - 4 integration points identified
  - Smoke test criteria defined
  - Expected outputs documented

- **Vagueness audit:** All vague phrases resolved or added to checklist

- **Question generation:** 3 iterations completed, 46 total questions identified

## All User Decisions Resolved ✅

All 10 questions have been answered:

1. ✅ **Mode manager structure:** Full mode manager (Option A)
2. ✅ **ConfigManager error handling:** Trust initialization (Option A)
3. ✅ **Config files to copy:** Copy entire data/configs/ folder
4. ✅ **drafted_data.csv:** Copy for roster state (Option A)
5. ✅ **Progress display:** Summary message only (Option C)
6. ✅ **JSON metadata:** Simple format, no wrapper (Option A)
7. ✅ **Parallelization:** Sequential loop (Option A)
8. ✅ **Player filtering:** All available players (Option A)
9. ✅ **Season-long scoring:** use_weekly_projection=False (Option A)
10. ✅ **JSON precision:** Round to 2 decimals (Option B)

## Planning Phase Complete Summary

**Phase 2 Investigation:**
- 11 items RESOLVED from codebase
- 34 questions generated across 3 iterations
- All vague phrases resolved
- Execution path analysis complete
- Performance analysis complete
- Testing requirements defined

**Phase 3 & 4 Resolution:**
- 10 user decisions made
- All decisions documented in specs and checklist
- Implementation approach fully defined

**Ready for Development Phase** per feature_development_guide.md

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `save_aggregate_scoring_results_specs.md` for complete specifications
3. Read `save_aggregate_scoring_results_checklist.md` to see all resolved decisions
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
