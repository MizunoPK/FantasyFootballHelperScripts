# League Config Auto Update - Feature Planning

---

## AGENT STATUS (Read This First)

**Current Phase:** COMPLETE
**Current Step:** Implementation finished
**Next Action:** Move to done/ folder

### Full Workflow Checklist

> **Instructions:** Update this checklist as you complete each step.

**PLANNING PHASE** (feature_planning_guide.md)
- [x] Phase 1: Initial Setup
  - [x] Create folder structure
  - [x] Move notes file
  - [x] Create README.md (this file)
  - [x] Create league_config_auto_update_specs.md
  - [x] Create league_config_auto_update_checklist.md
  - [x] Create league_config_auto_update_lessons_learned.md
- [x] Phase 2: Deep Investigation
  - [x] Analyze notes thoroughly
  - [x] Research codebase patterns
  - [x] Populate checklist with questions
  - [x] Update specs with context
- [x] Phase 3: Report and Pause
  - [x] Present findings to user
  - [x] Wait for user direction
- [x] Phase 4: Resolve Questions
  - [x] All checklist items resolved (6/6)
  - [x] Specs updated with all decisions
- [x] Planning Complete - Ready for Implementation

**DEVELOPMENT PHASE** (feature_development_guide.md)
- [x] Phase 1: Add INJURY_PENALTIES to PRESERVE_KEYS
- [x] Phase 2: Create update_configs_folder() method
- [x] Phase 3: Update SimulationManager to use update_configs_folder()
- [x] Phase 4: Add tests (11 new tests)
- [x] All tests pass (2184/2184 = 100%)

---

## What This Is

Fixing the automatic update of `data/configs/` folder after iterative simulation creates a new `optimal_*` folder. Currently the code just copies files, but it should:
1. Preserve certain parameters from original config
2. Apply MATCHUP → SCHEDULE mapping for week files
3. Update all other parameters from optimal files

## Why We Need This

The current implementation (`shutil.copy2()` in SimulationManager.py:841-845) overwrites important user-maintained settings like CURRENT_NFL_WEEK and NFL_SEASON. This breaks the workflow because users have to manually restore these values after every optimization run.

## Scope

**IN SCOPE:**
- Fix SimulationManager to use smart update logic instead of raw copy
- Add INJURY_PENALTIES to preserved parameters
- Apply MATCHUP → SCHEDULE mapping for week-specific files
- Preserve user-maintained parameters in all file updates

**OUT OF SCOPE:**
- Changing the optimal folder output format
- Adding new parameters to optimization
- Modifying the optimization algorithm itself

## Key Context for Future Agents

### Current Implementation (Broken)

**SimulationManager.py:837-848:**
```python
if self.auto_update_league_config:
    data_configs_path = Path(__file__).parent.parent / "data" / "configs"
    if data_configs_path.exists():
        for config_file in ['league_config.json', 'week1-5.json', 'week6-11.json', 'week12-17.json']:
            src = final_folder / config_file
            dst = data_configs_path / config_file
            if src.exists():
                shutil.copy2(src, dst)  # <-- PROBLEM: Raw copy overwrites preserved params
```

### Existing Smart Update Logic

**ResultsManager.py:647-733** has `update_league_config()` that:
- Preserves: CURRENT_NFL_WEEK, NFL_SEASON, MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS
- Missing: INJURY_PENALTIES (user requested this)
- Maps: MATCHUP_SCORING → SCHEDULE_SCORING (MIN_WEEKS, IMPACT_SCALE, WEIGHT)
- Only works for single files, not the folder structure

### Config File Structure

```
data/configs/
├── league_config.json    # Base params (CURRENT_NFL_WEEK, NFL_SEASON, MAX_POSITIONS, etc.)
├── week1-5.json          # Week-specific (MATCHUP_SCORING, SCHEDULE_SCORING, etc.)
├── week6-11.json
└── week12-17.json
```

### Parameters to Preserve (User Requirements)

| Parameter | File | Reason |
|-----------|------|--------|
| CURRENT_NFL_WEEK | league_config.json | User-maintained, changes weekly |
| NFL_SEASON | league_config.json | User-maintained, changes yearly |
| MAX_POSITIONS | league_config.json | League-specific roster rules |
| FLEX_ELIGIBLE_POSITIONS | league_config.json | League-specific roster rules |
| INJURY_PENALTIES | league_config.json | **Missing from current implementation** |

### MATCHUP → SCHEDULE Mapping

For week files (week1-5.json, etc.):
- `SCHEDULE_SCORING.MIN_WEEKS` = `MATCHUP_SCORING.MIN_WEEKS`
- `SCHEDULE_SCORING.IMPACT_SCALE` = `MATCHUP_SCORING.IMPACT_SCALE`
- `SCHEDULE_SCORING.WEIGHT` = `MATCHUP_SCORING.WEIGHT`

## How to Continue This Work

1. Check the AGENT STATUS section above for current phase and step
2. Read `league_config_auto_update_specs.md` for specifications
3. Read `league_config_auto_update_checklist.md` for open questions
4. Continue from the current step in the workflow checklist
