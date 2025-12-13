# Week-Specific Point Normalization - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** COMPLETE
**Current Step:** Implementation complete, all tests passing
**Next Action:** Commit changes

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step. This is your persistent state across sessions.

**PLANNING PHASE** (feature_planning_guide.md)
- [x] Phase 1: Initial Setup
  - [x] Create folder structure
  - [x] Move notes file
  - [x] Create README.md (this file)
  - [x] Create week_specific_point_normalization_specs.md
  - [x] Create week_specific_point_normalization_checklist.md
  - [x] Create week_specific_point_normalization_lessons_learned.md
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
- [x] Implementation (simple feature - direct implementation)
- [x] Tests passing (100% - 2221 tests)

**POST-IMPLEMENTATION PHASE**
- [x] All tests passing (2221 tests, 100%)
- [x] QC Round 1: Initial Quality Review - PASSED
- [x] QC Round 2: Deep Verification Review - PASSED (fixed docstring examples)
- [x] QC Round 3: Final Skeptical Review - PASSED (fixed test fixture)
- [x] Committed: eb8a7da

---

## What This Is

Move the `NORMALIZATION_MAX_SCALE` parameter from the base `league_config.json` into the week-specific config files (`week1-5.json`, `week6-9.json`, `week10-13.json`, `week14-17.json`). This allows the normalization scale to vary by week range, enabling more precise scoring calibration as the NFL season progresses.

## Why We Need This

1. **Season Dynamics:** Point projections and actual scoring patterns change throughout the season - early weeks have more uncertainty, late weeks have more data
2. **Optimization Results:** Simulation testing has shown that different `NORMALIZATION_MAX_SCALE` values perform better in different week ranges
3. **Consistency with Other Week-Specific Params:** Other scoring parameters (PLAYER_RATING, MATCHUP, etc.) are already week-specific; NORMALIZATION_MAX_SCALE should follow the same pattern

## Scope

**IN SCOPE:**
- Move `NORMALIZATION_MAX_SCALE` from `league_config.json` to week-specific configs
- Update all 4 week-specific config files with their own values
- Update `ConfigManager` if needed to handle the parameter from week configs
- Update simulation `ConfigGenerator` if needed to support week-specific NORMALIZATION_MAX_SCALE
- Update any tests that reference this parameter

**OUT OF SCOPE:**
- Changing the normalization algorithm itself
- Adding new week-specific parameters beyond NORMALIZATION_MAX_SCALE
- Changing the week range definitions (1-5, 6-9, 10-13, 14-17)

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `week_specific_point_normalization_notes.txt` | Original scratchwork notes from user |
| `week_specific_point_normalization_specs.md` | Main specification with detailed requirements |
| `week_specific_point_normalization_checklist.md` | Tracks open questions and decisions |
| `week_specific_point_normalization_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Current Config Structure

**Base config (`league_config.json`):**
- Contains `NORMALIZATION_MAX_SCALE: 163` (current value)
- Contains other base params: NFL week, season, scoring format, bye weights, etc.

**Week configs (`week{N}-{M}.json`):**
- Already contain week-specific scoring parameters (PLAYER_RATING_SCORING, MATCHUP_SCORING, etc.)
- Do NOT currently contain NORMALIZATION_MAX_SCALE
- Merged over base config based on CURRENT_NFL_WEEK

### ConfigManager Loading Flow

1. Load `league_config.json` (base params)
2. Extract `CURRENT_NFL_WEEK` from base params
3. Determine week config file (e.g., week 7 → `week6-9.json`)
4. Load week config and merge its `parameters` over base
5. Week-specific values override base values for same keys

### Key Code Locations

- **ConfigManager:** `league_helper/util/ConfigManager.py`
  - Lines 950-975: Required params list and extraction
  - Lines 893-912: Week config merge logic
- **ConfigGenerator:** `simulation/ConfigGenerator.py`
  - Lines 90, 195: NORMALIZATION_MAX_SCALE param definitions
  - Lines 231, 269, 294: Base vs week-specific param classification
  - Lines 599-613: Value set generation

## What's Resolved

1. **Default Value Strategy:** Remove entirely from base config - week configs are required source
2. **Week-Specific Values:**
   - Weeks 1-5: 163
   - Weeks 6-9: 153
   - Weeks 10-13: 143
   - Weeks 14-17: 133
3. **Simulation Optimization:** Yes - move to WEEK_SPECIFIC_PARAMS for per-week optimization

## What's Still Pending

(None - planning complete)

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `week_specific_point_normalization_specs.md` for complete specifications
3. Read `week_specific_point_normalization_checklist.md` to see what's resolved vs pending
4. Continue from the current step in the workflow checklist
5. **Update the AGENT STATUS section** as you complete steps
