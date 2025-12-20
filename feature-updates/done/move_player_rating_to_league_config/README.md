# Move Player Rating to League Config - Work in Progress

---

## AGENT STATUS (Read This First)

**Current Phase:** POST-IMPLEMENTATION
**Current Step:** All QC rounds complete, lessons learned documented
**Next Action:** Ready to move folder to done/

### WHERE AM I RIGHT NOW? (Quick State Check)

```
Current Phase:  [X] PLANNING  [X] DEVELOPMENT  [X] POST-IMPL  [ ] COMPLETE
Current Step:   Post-implementation complete, ready for completion
Blocked:        [X] NO  [ ] YES
Next Action:    Move folder to feature-updates/done/
Last Activity:  2025-12-19 - All QC rounds passed, lessons learned documented
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
  - [X] Create move_player_rating_to_league_config_specs.md
  - [X] Create move_player_rating_to_league_config_checklist.md
  - [X] Create move_player_rating_to_league_config_lessons_learned.md
- [X] Phase 2: Deep Investigation
  - [X] 2.1: Analyze notes thoroughly
  - [X] 2.2: Research codebase patterns
  - [X] 2.3: Populate checklist with questions
  - [X] 2.3.1: THREE-ITERATION question generation (MANDATORY)
  - [X] 2.4: CODEBASE VERIFICATION rounds (MANDATORY)
  - [X] 2.5: Performance analysis for options
  - [X] 2.6: Create DEPENDENCY MAP
  - [X] 2.7: Update specs with context + dependency map
  - [X] 2.8: ASSUMPTIONS AUDIT (list all assumptions)
- [X] Phase 3: Report and Pause
  - [X] Present findings to user
  - [ ] Wait for user direction (IN PROGRESS)
- [ ] Phase 4: Resolve Questions
  - [X] All checklist items resolved [x]
  - [X] Specs updated with all decisions
- [X] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [X] Step 1: Create TODO file
- [X] Step 2: First Verification Round (7 iterations)
- [X] Step 3: Create questions file (if needed)
- [X] Step 4: Update TODO with answers
- [X] Step 5: Second Verification Round (9 iterations)
- [X] Step 6: Third Verification Round (8 iterations)
- [X] Interface Verification (pre-implementation)
- [X] Implementation
  - [X] Create code_changes.md
  - [X] Execute TODO tasks
  - [X] Tests passing (100%)

**POST-IMPLEMENTATION PHASE**
- [X] Requirement Verification Protocol
- [X] QC Round 1 (Code Quality - PASS)
- [X] QC Round 2 (Integration Testing - PASS)
- [X] QC Round 3 (Final Review - APPROVED)
- [X] Lessons Learned Review (5 lessons documented)
- [ ] Apply guide updates (user decision)
- [ ] Move folder to done/

---

## What This Is

Moving the PLAYER_RATING_SCORING configuration from week-specific horizon files (week1-5.json, etc.) to the base league_config.json, since it is only used in Draft/Add-to-Roster mode and should be optimized by win-rate simulation (not accuracy simulation).

## Why We Need This

1. **Correct Scope**: PLAYER_RATING_SCORING affects draft strategy, not weekly predictions - it should be a base parameter
2. **Correct Optimization**: Win-rate simulation should optimize this parameter (like other draft params), not accuracy simulation
3. **Config Structure Consistency**: Base/strategy parameters belong in league_config.json, prediction parameters belong in horizon files

## Scope

**IN SCOPE:**
- Moving PLAYER_RATING_SCORING from WEEK_SPECIFIC_PARAMS to BASE_CONFIG_PARAMS
- Updating ConfigGenerator to handle this parameter as a base param
- Updating win-rate simulation to optimize PLAYER_RATING_SCORING
- Removing PLAYER_RATING_SCORING from accuracy simulation parameter list
- Updating existing config files (data/configs/) to reflect new structure
- Updating tests to reflect the new parameter location

**OUT OF SCOPE:**
- Changing the PLAYER_RATING_SCORING algorithm or scoring logic
- Modifying how Draft mode uses PLAYER_RATING_SCORING
- Changes to other simulation parameters
- Performance improvements or refactoring unrelated to this move

### Files in This Folder

| File | Purpose |
|------|---------|
| `README.md` | This file - context and status for agents |
| `move_player_rating_to_league_config_notes.txt` | Original scratchwork notes from user |
| `move_player_rating_to_league_config_specs.md` | Main specification with detailed requirements |
| `move_player_rating_to_league_config_checklist.md` | Tracks open questions and decisions |
| `move_player_rating_to_league_config_lessons_learned.md` | Captures issues to improve the guides |

## Key Context for Future Agents

### Config Structure
The codebase has two types of configuration parameters:
- **BASE_CONFIG_PARAMS**: Draft strategy and league settings (in league_config.json)
- **WEEK_SPECIFIC_PARAMS**: Weekly prediction scoring parameters (in week*.json horizon files)

PLAYER_RATING_SCORING is currently classified as WEEK_SPECIFIC but should be BASE_CONFIG because it's only used in draft mode, not weekly predictions.

### Two Simulation Systems
- **Win-rate simulation**: Optimizes draft strategy parameters (should include PLAYER_RATING_SCORING)
- **Accuracy simulation**: Optimizes weekly prediction parameters (should exclude PLAYER_RATING_SCORING)

## What's Resolved
- **All checklist items** - Complete investigation done, all questions answered
- **Implementation approach** - 3 line changes identified (see specs.md)
- **Backward compatibility** - Verified ConfigManager handles both old and new config structures
- **Dependency map** - Complete module dependency diagram created
- **Testing strategy** - Test plan defined in checklist

## What's Still Pending
- **User approval** - Waiting for user to approve implementation
- **Implementation** - Ready to proceed once approved

## How to Continue This Work

1. **Check the AGENT STATUS section above** for current phase and step
2. Read `move_player_rating_to_league_config_specs.md` for complete specifications
3. Read `move_player_rating_to_league_config_checklist.md` to see what's resolved vs pending
4. Continue from Phase 2.1 - Analyze notes thoroughly
5. **Update the AGENT STATUS section** as you complete steps
