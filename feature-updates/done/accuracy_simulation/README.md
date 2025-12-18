# Accuracy Simulation - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** DEVELOPMENT
**Current Step:** Implementation - Ready to Begin
**Next Action:** Start Phase 1: Folder Restructuring (Task 1.1)

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [x] Phase 1: Initial Setup
  - [x] Create folder structure
  - [x] Move notes file
  - [x] Create README.md (this file)
  - [x] Create accuracy_simulation_specs.md
  - [x] Create accuracy_simulation_checklist.md
  - [x] Create accuracy_simulation_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] Analyze notes thoroughly
  - [x] Research codebase patterns
  - [x] Populate checklist with questions
  - [x] Update specs with context
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] Codebase verification rounds completed (2 rounds)
- [x] Phase 4: Resolve Questions
  - [x] All checklist items resolved
  - [x] Specs updated with all decisions
- [x] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 1: Create TODO file
- [x] Step 2: First Verification Round (7 iterations)
  - [x] Iterations 1-3: Standard verification
  - [x] Iteration 4: Algorithm Traceability
  - [x] Iteration 5: End-to-End Data Flow
  - [x] Iteration 6: Skeptical Re-verification
  - [x] Iteration 7: Integration Gap Check
- [x] Step 3: Create questions file (if needed) - SKIPPED (no questions needed)
- [x] Step 4: Update TODO with answers - N/A
- [x] Step 5: Second Verification Round (9 iterations)
  - [x] Iterations 8-10: Standard verification
  - [x] Iteration 11: Algorithm Traceability
  - [x] Iteration 12: End-to-End Data Flow
  - [x] Iteration 13: Skeptical Re-verification
  - [x] Iteration 14: Integration Gap Check
  - [x] Iterations 15-16: Standard verification
- [x] Step 6: Third Verification Round (8 iterations)
  - [x] Iterations 17-18: Fresh Eyes Review
  - [x] Iteration 19: Algorithm Deep Dive
  - [x] Iteration 20: Edge Case Verification
  - [x] Iteration 21: Test Coverage Planning
  - [x] Iteration 22: Skeptical Re-verification #3
  - [x] Iteration 23: Integration Gap Check #3
  - [x] Iteration 24: Implementation Readiness
- [ ] Implementation (10 phases, 28 tasks)
- [ ] Tests passing (100%)

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

A new simulation mode that tests the **accuracy** of the scoring algorithm by comparing calculated projected points to actual player performance, rather than simulating drafts and matches to measure win rate. This allows optimization of config parameters to maximize prediction accuracy instead of (or in addition to) win rate.

## Critical Distinction: Strategy vs Prediction

| Simulation | Purpose | Config Files | Represents |
|------------|---------|--------------|------------|
| **Win Rate** | Draft STRATEGY | `league_config.json` | How to pick players during draft |
| **Accuracy** | Player PREDICTION | `draft_config.json` + weekly configs | How accurately we predict performance |

## Why We Need This

1. **Separation of concerns** - Win Rate optimizes draft *strategy*, Accuracy optimizes player *prediction*
2. **Better in-season decisions** - Starter Helper and Trade Simulator need accurate predictions, not draft strategy
3. **New draft_config.json** - Add to Roster Mode will use its own config optimized for ROS accuracy
4. **Two evaluation modes** - ROS accuracy (for draft_config.json) and weekly accuracy (for week-specific configs)

## Scope

**IN SCOPE:**
- New accuracy simulation mode alongside existing win-rate simulation
- Refactor simulation folder to separate shared classes from mode-specific classes
- Season-long projection accuracy evaluation
- Week-by-week projection accuracy evaluation
- Parameter optimization loop similar to win-rate simulation
- Rename existing run_simulation.py to run_win_rate_simulation.py
- Create new run_accuracy_simulation.py

**OUT OF SCOPE:**
- Changes to the core scoring algorithm itself
- Changes to the Add to Roster Mode functionality
- Changes to other modes (Starter Helper, Trade Simulator, etc.)

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `accuracy_simulation_notes.txt` | Original scratchwork notes from user |
| `accuracy_simulation_specs.md` | Main specification with detailed requirements |
| `accuracy_simulation_checklist.md` | Tracks open questions and decisions |
| `accuracy_simulation_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Relationship to Win-Rate Simulation
The existing simulation system runs mock drafts and matches to determine which config parameters produce the highest win rate. This new accuracy simulation uses the same parameter iteration approach but evaluates configs differently - by measuring how close projected points are to actual points.

### Scoring Algorithm Connection (RESOLVED)
The `ScoredPlayer` object returned by `score_player()` already contains a `projected_points` field with the un-normalized calculated projection. Formula: `(score / normalization_scale) * max_projection`. No additional code needed to extract this.

### Shared Architecture (RESOLVED)
- **Fully reusable**: `ConfigGenerator.py`, `PARAM_DEFINITIONS`, week-range structure (1-5, 6-9, 10-13, 14-17)
- **Win-rate specific**: `SimulatedLeague`, `Week`, `DraftHelperTeam`, `SimulatedOpponent`
- **New for accuracy**: `AccuracySimulationManager`, `AccuracyResultsManager`, `PlayerAccuracyCalculator`

### Data Sources (RESOLVED)
- Weekly actuals: `sim_data/{year}/weeks/week_XX/players.csv`
- Weekly projections: `sim_data/{year}/weeks/week_XX/players_projected.csv`
- Season actuals: `sim_data/{year}/players_actual.csv`
- Season projections: `sim_data/{year}/players_projected.csv`

## What's Resolved (ALL ITEMS - Planning Complete)

See `accuracy_simulation_specs.md` for complete specifications. Key decisions:

- **Accuracy metric**: MAE (Mean Absolute Error) - single metric, lower is better
- **Scope**: FULL - includes accuracy sim, folder restructure, Win Rate changes, Add to Roster changes, ConfigManager updates
- **ROS evaluation**: Week 1 only - pre-season predictions vs actual season totals
- **Player filtering**: Exclude 0 actual points, no projection threshold, no minimum games, equal weighting
- **17 parameters to optimize**: NORMALIZATION, PLAYER_RATING, TEAM_QUALITY, PERFORMANCE, MATCHUP, TEMPERATURE, WIND, LOCATION params
- **SCHEDULE syncs with MATCHUP**: Keep SCHEDULE_IMPACT_SCALE, WEIGHT, MIN_WEEKS equal to MATCHUP values
- **--mode options**: ros, weekly, both (default=both, runs ROS first)
- **Migration**: All-at-once, keep sys.path.append pattern
- **Auto-copy disabled**: Manual copy only (disable in win-rate sim too)
- **Missing draft_config.json**: Error with helpful message (no silent fallback)

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `accuracy_simulation_specs.md` for complete specifications
3. Read `accuracy_simulation_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
