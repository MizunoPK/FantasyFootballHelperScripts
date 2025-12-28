# Integrate New Player Data Into League Helper - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** PLANNING
**Current Step:** Phase 3 - Presenting Findings to User
**Next Action:** Await user decisions on architecture questions

### WHERE AM I RIGHT NOW? (Quick State Check)

```
Current Phase:  [x] PLANNING  [ ] DEVELOPMENT  [ ] POST-IMPL  [ ] COMPLETE
Current Step:   Phase 3 - Presenting findings to user
Blocked:        [ ] NO  [x] YES → Reason: Awaiting user decisions
Next Action:    Get user decisions on field mapping strategy and file update approach
Last Activity:  2025-12-26 - Completed Phase 2 investigation, created comprehensive checklist and dependency map
```

**Session Resume Instructions:**
1. Read this section first
2. Check the workflow checklist below for detailed progress
3. Continue from "Next Action" - do NOT restart the workflow

---

## 📖 Active Development Guide

**Current Phase:** PLANNING
**Active Guide:** `feature-updates/guides/feature_planning_guide.md`
**Critical Section:** Phase 2 - Investigation

⚠️ **AGENTS: Re-read the active guide section before major decisions!**

**Guide by Phase:**
- **PLANNING:** `feature_planning_guide.md` ← CURRENT
- **TODO_CREATION:** `todo_creation_guide.md`
- **IMPLEMENTATION:** `implementation_execution_guide.md`
- **POST_IMPLEMENTATION:** `post_implementation_guide.md`

**Update this section when transitioning between phases.**

---

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
  - [x] 2.4: CODEBASE VERIFICATION rounds (MANDATORY)
  - [x] 2.5: Performance analysis for options
  - [x] 2.6: Create DEPENDENCY MAP
  - [x] 2.7: Update specs with context + dependency map
  - [x] 2.8: ASSUMPTIONS AUDIT (list all assumptions)
- [ ] Phase 3: Report and Pause
  - [ ] Present findings to user
  - [ ] Wait for user direction
- [ ] Phase 4: Resolve Questions
  - [ ] All checklist items resolved [x]
  - [ ] Specs updated with all decisions
- [ ] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [ ] Step 1: Create TODO file
- [ ] Step 2-7: Complete all 24 verification iterations
- [ ] Interface Verification (pre-implementation)
- [ ] Implementation
  - [ ] Create code_changes.md
  - [ ] Execute TODO tasks
  - [ ] Tests passing (100%)

**POST-IMPLEMENTATION PHASE**
- [ ] Requirement Verification Protocol
- [ ] QC Round 1-3
- [ ] SMOKE TESTING PROTOCOL
- [ ] Lessons Learned Review
- [ ] Move folder to done/

---

## What This Is

Migration of the League Helper system from CSV-based player data storage (players.csv, players_projected.csv, drafted_data.csv) to a new JSON-based player data structure stored in /data/player_data/ with position-specific files (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json).

## Why We Need This

1. **New data structure already in place**: Previous features have established the JSON-based player data structure
2. **Consistency**: League Helper should use the same data format as other parts of the system
3. **Richer data**: JSON structure supports additional stats that will be needed by future features
4. **Simplified workflow**: Eliminates need for separate drafted_data.csv file

## Scope

**IN SCOPE:**
- Modify PlayerManager to read from JSON files instead of CSV files
- Update FantasyPlayer instantiation to work with JSON data structure
- Handle changes to drafted field (drafted_by with team name instead of 0/1/2)
- Handle changes to locked field (boolean instead of 0/1)
- Verify all stats and fields are accessible from JSON structure
- Ensure League Helper functionality works exactly as before

**OUT OF SCOPE:**
- Changes to how data is displayed or used (only data loading)
- New features using the additional stats (just ensure they're accessible)
- Changes to the JSON data structure itself (already established)
- Changes to simulation or other modules (League Helper only)

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `integrate_new_player_data_into_league_helper_notes.txt` | Original scratchwork notes from user |
| `integrate_new_player_data_into_league_helper_specs.md` | Main specification with detailed requirements |
| `integrate_new_player_data_into_league_helper_checklist.md` | Tracks open questions and decisions |
| `integrate_new_player_data_into_league_helper_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Data Structure Changes

**Old (CSV):**
- players.csv: All players with stats
- players_projected.csv: Projected stats
- drafted_data.csv: Separate file tracking drafted status

**New (JSON):**
- /data/player_data/qb_data.json (and rb, wr, te, k, dst)
- Single source with all stats including drafted_by field
- Boolean locked field instead of 0/1

### Field Mapping Changes

**Drafted Status:**
- OLD: `drafted` column with values 0/1/2
- NEW: `drafted_by` column with team name string
  - drafted=0 → drafted_by=""
  - drafted=1 → drafted_by != "" and drafted_by != FANTASY_TEAM_NAME
  - drafted=2 → drafted_by == FANTASY_TEAM_NAME

**Locked Status:**
- OLD: `locked` column with values 0/1
- NEW: `locked` field with boolean True/False

## What's Resolved

- JSON file locations and structure verified (6 position files in /data/player_data/)
- Current CSV loading mechanism identified (PlayerManager.load_players_from_csv line 142)
- Field differences documented (drafted_by vs drafted, locked boolean vs int, projected_points array vs week_N_points)
- All 8 files using drafted field identified
- drafted_data.csv usage tracked (4 files)
- Dependency map created showing data flow
- FANTASY_TEAM_NAME constant location verified (constants.py line 19: "Sea Sharp")

## What's Still Pending

**Critical Architecture Decisions Needed:**
1. FantasyPlayer field strategy: Keep int/individual fields (minimal changes) OR migrate to string/bool/array (cleaner long-term)?
2. File update strategy: Write to JSON, continue writing CSV, or make read-only?
3. drafted_data.csv fate: Eliminate file and DraftedDataWriter class?

**Data Mapping Questions:**
4. bye_week field location in JSON (not visible in sample)
5. projected_points vs actual_points - which maps to week_N_points?
6. Additional stats (passing/rushing/receiving) - store or ignore?
7. Empty drafted_by confirmation - is "" the "not drafted" value?

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `integrate_new_player_data_into_league_helper_specs.md` for complete specifications
3. Read `integrate_new_player_data_into_league_helper_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
