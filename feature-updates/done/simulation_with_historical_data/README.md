# Simulation with Historical Data - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** COMPLETE
**Current Step:** All tasks finished
**Next Action:** Feature complete - folder moved to done/

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [x] Phase 1: Initial Setup
  - [x] Create folder structure
  - [x] Move notes file
  - [x] Create README.md (this file)
  - [x] Create simulation_with_historical_data_specs.md
  - [x] Create simulation_with_historical_data_checklist.md
  - [x] Create simulation_with_historical_data_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] Analyze notes thoroughly
  - [x] Research codebase patterns (SimulationManager, ParallelLeagueRunner, SimulatedLeague)
  - [x] Populate checklist with questions (4 architecture questions, error handling, edge cases)
  - [x] Update specs with context (data flow, file mapping, investigation findings)
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] Wait for user direction
- [x] Phase 4: Resolve Questions
  - [x] All checklist items resolved
  - [x] Specs updated with all decisions
- [x] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 1: Create TODO file
- [x] Step 2: First Verification Round (7 iterations) - Found Task 2.6 (Week.py)
- [x] Step 3: Create questions file (if needed) - No questions needed
- [x] Step 4: Update TODO with answers - N/A (no questions)
- [x] Step 5: Second Verification Round (9 iterations) - Removed Task 3.2 (reuse existing)
- [x] Step 6: Third Verification Round (8 iterations) - Implementation ready
- [x] Implementation (17 tasks) - ALL COMPLETE
- [x] Tests passing (100%) - 2161/2161 tests pass

**POST-IMPLEMENTATION PHASE**
- [x] Requirement Verification Protocol - 16/16 requirements verified
- [x] QC Round 1 - Initial review PASSED
- [x] QC Round 2 - Deep verification PASSED
- [x] QC Round 3 - Final skeptical review PASSED
- [x] Lessons Learned Review - 2 lessons captured
- [x] Apply guide updates - Added to feature_planning_guide.md
- [x] Move folder to done/

---

## What This Is

Updating the simulation system to use historical NFL season data compiled by the `compile_historical_data.py` script. Instead of testing configurations against a single season, configs will be evaluated across ALL available historical seasons (2021+) to produce more robust and validated results.

## Why We Need This

1. **Better validation** - Testing configs across multiple seasons provides more reliable results
2. **Historical backtesting** - Validates scoring algorithms and strategies against known outcomes
3. **Reduced overfitting** - Configs that work across multiple years are more likely to work in future seasons
4. **Leverage new data** - Uses the comprehensive historical data recently compiled

## Scope

**IN SCOPE:**
- Detecting and loading historical season folders (`20XX/`) in `sim_data/`
- Running simulations across all available seasons per config
- Aggregating win rates across all seasons
- Using week-specific data for draft and weekly matchups
- Loading `players.csv` and `players_projected.csv` from appropriate week folders

**OUT OF SCOPE:**
- Modifying the historical data compiler (`compile_historical_data.py`)
- Changing the simulation's core scoring algorithms
- Adding new simulation modes (we're updating existing modes)
- Changing the output folder format of the historical data compiler

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `simulation_with_historical_data_notes.txt` | Original scratchwork notes from user |
| `simulation_with_historical_data_specs.md` | Main specification with detailed requirements |
| `simulation_with_historical_data_checklist.md` | Tracks open questions and decisions |
| `simulation_with_historical_data_lessons_learned.md` | Captures issues to improve the guides |
| `simulation_with_historical_data_todo.md` | Implementation tasks and verification tracking |

## Key Context for Future Agents

### Historical Data Structure (from compile_historical_data.py)

```
simulation/sim_data/{YEAR}/
├── season_schedule.csv       # Full season schedule with bye weeks
├── game_data.csv             # Game results with weather data
├── team_data/                # 32 team CSV files
│   └── {TEAM}.csv
└── weeks/                    # Weekly point-in-time snapshots
    └── week_01...week_17/
        ├── players.csv       # "Smart values" (actuals for past, projected for future)
        └── players_projected.csv
```

### Current Simulation Structure (single season)

```
simulation/sim_data/
├── players.csv               # Current player data
├── teams_week_1.csv          # Current team rankings
└── ...
```

### Key Integration Points

The simulation system needs to be updated to:
1. Find all `20XX/` folders in `sim_data/`
2. For each config tested, simulate across ALL seasons
3. For draft simulation: Use `weeks/week_01/players.csv` and `players_projected.csv`
4. For weekly matchups: Use `weeks/week_XX/players.csv` for the week being simulated

## What's Resolved

- Historical data format is documented (see historical-data-compiler)
- Data contains all 17 weeks of regular season
- Player data includes both actuals and projections per week

## Implementation Summary

**All 17 tasks have been implemented:**

1. **SimulationManager Changes:**
   - Added `_discover_seasons()` for auto-detecting historical seasons (20XX/ folders)
   - Added `_validate_season_strict()` for fail-fast validation
   - Added `_run_season_simulations_with_weeks()` for multi-season execution
   - Added deprecation warnings to legacy single-season methods

2. **SimulatedLeague Changes:**
   - Updated to 17-week season (was 16)
   - Added week data pre-loading cache (`_preload_all_weeks()`, `_parse_players_csv()`, `_load_week_data()`)
   - Week-specific data loaded before each week's matchups

3. **Week.py Changes:**
   - Updated validation from 1-16 to 1-17 weeks

4. **PlayerManager Changes:**
   - Added `set_player_data()` for cache-based data updates

**All 2161 tests pass (100%)**

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `simulation_with_historical_data_specs.md` for complete specifications
3. Read `simulation_with_historical_data_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
