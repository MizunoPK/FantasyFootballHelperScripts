# 4 Week Configs - COMPLETE

---

## AGENT STATUS (Read This First)

**Current Phase:** COMPLETE
**Current Step:** All done - ready to move to done/
**Next Action:** None - implementation complete

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [x] Phase 1: Initial Setup
  - [x] Create folder structure
  - [x] Move notes file
  - [x] Create README.md (this file)
  - [x] Create 4_week_configs_specs.md
  - [x] Create 4_week_configs_checklist.md
  - [x] Create 4_week_configs_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] Analyze notes thoroughly
  - [x] Research codebase patterns
  - [x] Populate checklist with questions
  - [x] Update specs with context
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] Wait for user direction
- [x] Phase 4: Resolve Questions
  - [x] All checklist items resolved [x]
  - [x] Specs updated with all decisions
- [x] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Step 1: Create TODO file
- [x] Step 2: First Verification Round (7 iterations)
- [x] Step 3: Create questions file (if needed)
- [x] Step 4: Update TODO with answers
- [x] Step 5: Second Verification Round (9 iterations)
- [x] Step 6: Third Verification Round (8 iterations)
- [x] Implementation
  - [x] Create code_changes.md
  - [x] Execute TODO tasks
  - [x] Tests passing (100%)

**POST-IMPLEMENTATION PHASE**
- [x] Requirement Verification Protocol
- [x] QC Round 1
- [x] QC Round 2
- [x] QC Round 3
- [x] Lessons Learned Review
- [x] Apply guide updates (if any)
- [x] Move folder to done/

---

## What This Is

Update the fantasy football helper system from 3 week-specific config files to 4 week-specific config files. This change splits the season into more granular week ranges for better scoring parameter optimization.

**Current Structure (3 configs):**
- weeks 1-5 → `week1-5.json`
- weeks 6-11 → `week6-11.json`
- weeks 12-17 → `week12-17.json`

**New Structure (4 configs):**
- weeks 1-5 → `week1-5.json` (unchanged)
- weeks 6-9 → `week6-9.json` (new)
- weeks 10-13 → `week10-13.json` (new)
- weeks 14-17 → `week14-17.json` (new)

## Why We Need This

1. More granular week-specific parameter tuning for mid-season and late-season
2. Better separation between "mid-season" (6-9), "stretch run" (10-13), and "playoffs" (14-17)
3. Improved simulation accuracy with 4 distinct scoring periods

## Scope

**IN SCOPE:**
- Update `ConfigManager._get_week_config_filename()` method
- Update simulation system (SimulationManager, ConfigGenerator, ResultsManager)
- Create new config files in `data/configs/`
- Update all related tests
- Update all hardcoded week range references

**OUT OF SCOPE:**
- Changes to scoring algorithms themselves
- Changes to config parameter structure (only file organization)
- Migration tool for existing simulation_configs strategies

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `4_week_configs_notes.txt` | Original scratchwork notes from user |
| `4_week_configs_specs.md` | Main specification with detailed requirements |
| `4_week_configs_checklist.md` | Tracks open questions and decisions |
| `4_week_configs_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Core Implementation Location

The primary logic that maps week numbers to config files is in:
- `league_helper/util/ConfigManager.py` lines 231-256: `_get_week_config_filename()` method

### Files Requiring Changes

**Source Files:**
1. `league_helper/util/ConfigManager.py` - Week-to-filename mapping
2. `simulation/ConfigGenerator.py` - Required files list, week config loading
3. `simulation/SimulationManager.py` - Week file mapping, config initialization
4. `simulation/ResultsManager.py` - Week file mappings, save/load logic

**Data Files:**
1. `data/configs/week6-11.json` → Delete (or keep as backup)
2. `data/configs/week12-17.json` → Delete (or keep as backup)
3. `data/configs/week6-9.json` → Create new
4. `data/configs/week10-13.json` → Create new
5. `data/configs/week14-17.json` → Create new

**Test Files:**
1. `tests/league_helper/util/test_ConfigManager_week_config.py` - Primary test file
2. Plus 14 other test files with week config references

### Key Mappings to Change

| Location | Current | New |
|----------|---------|-----|
| ConfigManager._get_week_config_filename | 1-5, 6-11, 12-17 | 1-5, 6-9, 10-13, 14-17 |
| SimulationManager.week_file_mapping | '1-5', '6-11', '12-17' | '1-5', '6-9', '10-13', '14-17' |
| ResultsManager.WEEK_PARAMS | Implicit 3-range | Implicit 4-range |
| ConfigGenerator.required_files | 3 week files | 4 week files |

## What's Resolved
- Week ranges: 1-5, 6-9, 10-13, 14-17
- File naming: No zero-padding (`week6-9.json`, not `week06-09.json`)
- New config content: Copy from existing `week6-11.json` and `week12-17.json`
- Strategy folders: Manual update by user as needed
- Backward compatibility: None - 4-file structure only

## What's Still Pending
- Nothing - all questions resolved, ready for implementation

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `4_week_configs_specs.md` for complete specifications
3. Read `4_week_configs_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
