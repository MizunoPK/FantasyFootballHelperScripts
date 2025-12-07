# MAX_POSITIONS Config Migration - Code Changes

**Objective**: Move MAX_POSITIONS constant from constants.py to league_config.json
**Status**: Planning complete, awaiting user answers to questions before implementation
**Date Started**: 2025-10-22

---

## Implementation Status

**Phase 1: Add MAX_POSITIONS to Configuration System** - ⏳ Not started (awaiting Q&A)
**Phase 2: Update Code to Use Config MAX_POSITIONS** - ⏳ Not started
**Phase 2.5: Handle MAX_PLAYERS Dependency** - ⏳ Not started (pending Q1 answer)
**Phase 3: Update Tests** - ⏳ Not started
**Phase 4: Cleanup and Documentation** - ⏳ Not started
**Phase 5: Pre-Commit Validation** - ⏳ Not started

---

## Code Changes

### Phase 1: Configuration System Changes

*Changes will be documented here as implementation progresses*

### Phase 2: Code Reference Updates

*Changes will be documented here as implementation progresses*

### Phase 2.5: MAX_PLAYERS Handling

*Approach will be determined by user answer to Question 1*

### Phase 3: Test Updates

*Changes will be documented here as implementation progresses*

### Phase 4: Documentation Updates

*Changes will be documented here as implementation progresses*

---

## Files Modified

(To be populated during implementation)

**Config Files**:
- [ ] `data/league_config.json` - Add MAX_POSITIONS parameter

**Source Code**:
- [ ] `league_helper/util/ConfigManager.py` - Add max_positions loading and validation
- [ ] `league_helper/util/PlayerManager.py` - Update MAX_POSITIONS references
- [ ] `league_helper/util/FantasyTeam.py` - Update MAX_POSITIONS references
- [ ] `league_helper/trade_simulator_mode/trade_analyzer.py` - Update MAX_POSITIONS references
- [ ] `league_helper/add_to_roster_mode/AddToRosterModeManager.py` - Update MAX_PLAYERS references
- [ ] `league_helper/constants.py` - Add deprecation notice (or remove, pending Q2)

**Tests**:
- [ ] `tests/league_helper/test_constants.py` - Update or remove MAX_POSITIONS tests
- [ ] 13 test files with config mocks - Add max_positions attribute
- [ ] New ConfigManager tests for MAX_POSITIONS validation

**Documentation**:
- [ ] `CLAUDE.md` - Update references to MAX_POSITIONS
- [ ] `README.md` - Update configuration documentation
- [ ] `rules.md` - Update if needed

---

## Verification Summary

**First Verification Round**: ✅ Complete (3 iterations)
- Requirements fully identified and mapped to tasks
- Codebase patterns researched and documented
- Dependencies and risk areas identified
- Questions formulated based on ambiguities

**Second Verification Round**: ⏳ Pending (after user answers questions)
- Will perform 3 more iterations to refine based on answers
- Will validate question answers are fully integrated into plan
- Will finalize implementation details and task order

---

## Notes

- All classes that use MAX_POSITIONS already have `self.config` available ✅
- Simulation system does NOT vary MAX_POSITIONS (verified in ConfigGenerator.py) ✅
- MAX_PLAYERS constant is tightly coupled - decision needed on handling strategy
- 13 test files will need config mocks updated with max_positions attribute

---

*This file will be updated incrementally as each task is completed, then moved to updates/done/ when objective is complete.*
