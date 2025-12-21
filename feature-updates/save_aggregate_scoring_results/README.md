# Save Aggregate Scoring Results - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** PLANNING
**Current Step:** Phase 1 Complete - Moving to Phase 2 Investigation
**Next Action:** Research codebase to understand menu system, scoring patterns, and historical data structure

### WHERE AM I RIGHT NOW? (Quick State Check)

```
Current Phase:  [x] PLANNING  [ ] DEVELOPMENT  [ ] POST-IMPL  [ ] COMPLETE
Current Step:   Phase 1 Complete - Starting Phase 2
Blocked:        [x] NO  [ ] YES → Reason: ___________________
Next Action:    Begin codebase investigation for menu integration and scoring patterns
Last Activity:  2025-12-19 - Created initial planning files
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
- [ ] Phase 2: Deep Investigation
  - [ ] 2.1: Analyze notes thoroughly
  - [ ] 2.2: Research codebase patterns
  - [ ] 2.3: Populate checklist with questions
  - [ ] 2.3.1: THREE-ITERATION question generation (MANDATORY)
  - [ ] 2.4: CODEBASE VERIFICATION rounds (MANDATORY)
  - [ ] 2.5: Performance analysis for options
  - [ ] 2.6: Create DEPENDENCY MAP
  - [ ] 2.7: Update specs with context + dependency map
  - [ ] 2.8: ASSUMPTIONS AUDIT (list all assumptions)
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

A new menu mode in the League Helper that saves calculated projected points for all players to JSON files in the historical_data folder structure. This feature also copies relevant data files (players.csv, teams_week_N.csv, etc.) from the main data folder into historical_data for archival purposes.

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
- Files to copy likely include: players.csv, teams_week_N.csv, league_config.json

## What's Resolved
- Feature objective is clear
- Output file format defined (JSON with player_id keys)
- Output paths specified for weekly vs season-long

## What's Still Pending
- Menu integration approach
- Exact scoring method and parameters to use
- List of files to copy to historical_data
- Error handling for missing folders or data
- Season/week detection logic

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `save_aggregate_scoring_results_specs.md` for complete specifications
3. Read `save_aggregate_scoring_results_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
