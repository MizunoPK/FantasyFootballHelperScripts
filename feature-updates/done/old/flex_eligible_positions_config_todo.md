# FLEX_ELIGIBLE_POSITIONS Config Migration TODO

**Objective**: Move FLEX_ELIGIBLE_POSITIONS constant from constants.py to league_config.json

**Status**: ✅✅✅ **COMPLETE** - All phases finished, 100% test pass rate (1855/1855 tests)

**Completion Date**: 2025-10-22

**Summary**: Successfully migrated FLEX_ELIGIBLE_POSITIONS from constants.py to league_config.json.
- Changed default from `["RB", "WR", "TE", "DST"]` to `["RB", "WR"]` (bug fix)
- All production code updated to use config
- All tests updated and passing
- Documentation updated (README.md, ARCHITECTURE.md)
- constants.py cleaned up
- Pre-commit validation passed

---

## ✅ User Decisions Confirmed

**See**: `updates/FLEX_ELIGIBLE_POSITIONS_config_questions.md`

1. ✅ **Default value**: `["RB", "WR"]` (Option B - more restrictive)
2. ✅ **Config format**: List (Option A)
3. ✅ **Validation**: Strict (Option A)
4. ✅ **get_position_with_flex()**: Move to ConfigManager as instance method (Option B)
5. ✅ **FantasyPlayer.py discrepancy**: Was a bug - ensure consistency (Option A)
6. ✅ **Simulation consistency**: Trust/no action needed (Option B)
7. ✅ **Required parameter**: Fail if missing (Option A)
8. ✅ **Test file**: Create dedicated test_ConfigManager_flex_eligible_positions.py (Option A)

**⚠️ IMPORTANT BEHAVIOR CHANGE**: Changing from `["RB", "WR", "TE", "DST"]` to `["RB", "WR"]`
- TE will NO LONGER be FLEX-eligible
- DST will NO LONGER be FLEX-eligible
- This fixes the bug where constants.py had incorrect value

---

## Current State Analysis

**Current Definition** (constants.py:64):
```python
FLEX_ELIGIBLE_POSITIONS = [RB, WR, TE, DST]
```

**Total References**: 22 occurrences
- Production code: 11 (FantasyTeam.py: 7, constants.py: 2, FantasyPlayer.py: 2)
- Test code: 11 (test_constants.py, test_PlayerManager_scoring.py, test_FantasyPlayer.py)

**Related Function**: `get_position_with_flex(position)` in constants.py - needs migration

**Conflict**: FantasyPlayer.py:418 defines local `FLEX_ELIGIBLE_POSITIONS = ['RB', 'WR']` (different!)

---

## Phase 1: Add FLEX_ELIGIBLE_POSITIONS to Configuration System

### Task 1.1: Add FLEX_ELIGIBLE_POSITIONS to league_config.json
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/data/league_config.json`
**Decision**: ✅ Confirmed - Use `["RB", "WR"]` (Option B)

- [ ] Add `FLEX_ELIGIBLE_POSITIONS` key to `parameters` section
- [ ] Use list format: `["RB", "WR"]` (user confirmed)
- [ ] Place after MAX_POSITIONS or at end of parameters section
- [ ] Format example:
```json
"FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"]
```

**Pattern**: Similar to simple list parameters

### Task 1.2: Update ConfigKeys class
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:31-105`
- [ ] Add `FLEX_ELIGIBLE_POSITIONS = "FLEX_ELIGIBLE_POSITIONS"` constant to ConfigKeys class
- [ ] Add to Parameter Keys section (around line 50-65)
- [ ] Follow alphabetical ordering if present

**Pattern**: Similar to other parameter key definitions

### Task 1.3: Add flex_eligible_positions attribute to ConfigManager.__init__
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:143-186`
- [ ] Add `self.flex_eligible_positions: List[str] = []` after max_positions (around line 186)
- [ ] Follow existing pattern for list attributes

**Pattern**: Similar to list-based attributes

### Task 1.4: Add FLEX_ELIGIBLE_POSITIONS to required parameters
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:668-685`
- [ ] Add `self.keys.FLEX_ELIGIBLE_POSITIONS` to `required_params` list in `_extract_parameters()`
- [ ] Place after `self.keys.MAX_POSITIONS` (around line 685)

**Pattern**: Same format as other required parameter entries

### Task 1.5: Extract FLEX_ELIGIBLE_POSITIONS in _extract_parameters
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:693-730`
- [ ] Add `self.flex_eligible_positions = self.parameters[self.keys.FLEX_ELIGIBLE_POSITIONS]` after max_positions extraction (around line 729)

**Pattern**: Simple assignment for list-based parameters

### Task 1.6: Add FLEX_ELIGIBLE_POSITIONS validation (STRICT) with logging
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:755-776`
**Decision**: ✅ Confirmed - Strict validation (Option A)

- [ ] Add validation block after max_positions validation (around line 776)
- [ ] Validate it's a non-empty list
- [ ] Validate all values are valid position strings (QB, RB, WR, TE, K, DST - but NOT FLEX itself)
- [ ] Validate FLEX is NOT in the list (circular reference prevention)
- [ ] Log errors before raising (pattern: `self.logger.error()` then `raise ValueError()`)
- [ ] Example validation code:
```python
# Validate FLEX_ELIGIBLE_POSITIONS structure
if not isinstance(self.flex_eligible_positions, list):
    error_msg = f"FLEX_ELIGIBLE_POSITIONS must be a list, got: {type(self.flex_eligible_positions).__name__}"
    self.logger.error(error_msg)
    raise ValueError(error_msg)

if len(self.flex_eligible_positions) == 0:
    error_msg = "FLEX_ELIGIBLE_POSITIONS must contain at least one position"
    self.logger.error(error_msg)
    raise ValueError(error_msg)

# Validate no circular reference (FLEX can't be in FLEX_ELIGIBLE_POSITIONS)
if 'FLEX' in self.flex_eligible_positions:
    error_msg = "FLEX_ELIGIBLE_POSITIONS cannot contain 'FLEX' (circular reference)"
    self.logger.error(error_msg)
    raise ValueError(error_msg)

# Validate all positions are valid
valid_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
invalid_positions = [pos for pos in self.flex_eligible_positions if pos not in valid_positions]
if invalid_positions:
    error_msg = f"FLEX_ELIGIBLE_POSITIONS contains invalid positions: {', '.join(invalid_positions)}"
    self.logger.error(error_msg)
    raise ValueError(error_msg)

# Log successful validation
self.logger.debug(f"FLEX_ELIGIBLE_POSITIONS validated: {', '.join(self.flex_eligible_positions)}")
```

**Pattern**: Similar to max_positions validation with list-specific checks

---

## Phase 2: Update Code to Use Config FLEX_ELIGIBLE_POSITIONS

### Task 2.1: Update FantasyTeam to use config
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/FantasyTeam.py`
**Lines**: 114, 411, 507, 764, 820, 821, 849

- [ ] Line 114: Change `pos in Constants.FLEX_ELIGIBLE_POSITIONS` to `pos in self.config.flex_eligible_positions`
- [ ] Line 411: Change `pos not in Constants.FLEX_ELIGIBLE_POSITIONS` to `pos not in self.config.flex_eligible_positions`
- [ ] Line 507: Change `pos not in Constants.FLEX_ELIGIBLE_POSITIONS` to `pos not in self.config.flex_eligible_positions`
- [ ] Line 764: Change `pos in Constants.FLEX_ELIGIBLE_POSITIONS` to `pos in self.config.flex_eligible_positions`
- [ ] Line 820: Change `old_player.position in Constants.FLEX_ELIGIBLE_POSITIONS` to `old_player.position in self.config.flex_eligible_positions`
- [ ] Line 821: Change `new_player.position in Constants.FLEX_ELIGIBLE_POSITIONS` to `new_player.position in self.config.flex_eligible_positions`
- [ ] Line 849: Change `new_pos in Constants.FLEX_ELIGIBLE_POSITIONS` to `new_pos in self.config.flex_eligible_positions`

**Verification**: FantasyTeam has `self.config` available (ConfigManager instance)

### Task 2.2: Move get_position_with_flex() function to ConfigManager
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/constants.py:66-85`
**Decision**: ✅ Confirmed - Move to ConfigManager as instance method (Option B)

**Implementation**:
- [ ] Add method to ConfigManager:
```python
def get_position_with_flex(self, position: str) -> str:
    """
    Determine if a position should be considered for FLEX assignment.

    Args:
        position: Player's natural position (QB, RB, WR, TE, K, DST)

    Returns:
        'FLEX' if position is FLEX-eligible, otherwise the original position
    """
    if position in self.flex_eligible_positions:
        return 'FLEX'
    else:
        return position
```
- [ ] Update call sites to use `config.get_position_with_flex(position)`
- [ ] Remove from constants.py

**Current usage**: constants.py:82 (within function itself)

### Task 2.3: Fix FantasyPlayer.py local definition (BUG FIX)
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/utils/FantasyPlayer.py:418`
**Decision**: ✅ Confirmed - This was a bug, ensure consistency (Option A)

**Implementation**:
- [ ] Remove local definition `FLEX_ELIGIBLE_POSITIONS = ['RB', 'WR']` from line 418
- [ ] FantasyPlayer needs access to config to check flex_eligible_positions
- [ ] **Problem**: FantasyPlayer is in utils/ and doesn't have config access
- [ ] **Solution Options**:
  - **Option 1**: Pass config to FantasyPlayer.__init__ (requires changes to all instantiations)
  - **Option 2**: Import Constants and use the constant (but we're removing it!)
  - **Option 3**: Keep the hardcoded value `['RB', 'WR']` and add comment explaining it matches config
  - **Option 4**: Make the method accept an optional parameter for flex positions

**Recommended**: Option 3 (keep hardcoded but add comment) - FantasyPlayer is a data class and shouldn't need config dependency. The value `['RB', 'WR']` will match the config value.

- [ ] Update line 418 to add comment explaining this should match FLEX_ELIGIBLE_POSITIONS in config
- [ ] Keep tests as-is since they verify correct behavior

---

## Phase 3: Update Tests

### Task 3.1: Update constants tests
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/tests/league_helper/test_constants.py`
**Affected tests** (lines 118-130):

- [ ] MODIFY `test_flex_eligible_positions_are_correct()` - update to reference config instead of constant
- [ ] MODIFY `test_flex_eligible_does_not_contain_flex_itself()` - update to reference config
- [ ] MODIFY `test_flex_eligible_contains_only_valid_positions()` - update to reference config
- [ ] UPDATE `test_get_position_with_flex_*` tests if function moves to ConfigManager

**Rationale**: Tests now validate config behavior instead of constants

### Task 3.2: Create ConfigManager tests for FLEX_ELIGIBLE_POSITIONS
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/tests/league_helper/util/test_ConfigManager_flex_eligible_positions.py` (new file)
**Pattern**: Follow test_ConfigManager_max_positions.py structure

**Tests to create**:
- [ ] `test_flex_eligible_positions_loads_from_config()` - Verify attribute populated
- [ ] `test_flex_eligible_positions_is_list()` - Verify it's a list type
- [ ] `test_flex_eligible_positions_not_empty()` - At least one position required
- [ ] `test_flex_eligible_positions_no_flex_circular_reference()` - FLEX not in list
- [ ] `test_flex_eligible_positions_all_valid_positions()` - All are valid position strings
- [ ] `test_flex_eligible_positions_missing_raises_error()` - Missing from config raises ValueError
- [ ] `test_flex_eligible_positions_empty_list_raises_error()` - Empty list raises ValueError
- [ ] `test_flex_eligible_positions_contains_flex_raises_error()` - FLEX in list raises ValueError
- [ ] `test_flex_eligible_positions_invalid_position_raises_error()` - Unknown position raises ValueError
- [ ] `test_get_position_with_flex_method()` - If function moved to ConfigManager (optional)

**Use temp_data_folder fixture and create minimal config JSON with FLEX_ELIGIBLE_POSITIONS**

### Task 3.3: Update all test files that mock config (PROACTIVE)
**Decision**: User selected proactive update (following MAX_POSITIONS pattern)

**Files**: Identify test files that mock ConfigManager
- [ ] Search for all config mocks: `grep -r "Mock.*ConfigManager\|mock.*config" tests/`
- [ ] Update EACH mock to include `flex_eligible_positions` attribute
- [ ] Add to each mock: `mock_config.flex_eligible_positions = ['RB', 'WR', 'TE', 'DST']`

**Estimated files**: ~13 test files (same ones from MAX_POSITIONS migration)

### Task 3.4: Update FantasyPlayer tests if needed
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/tests/utils/test_FantasyPlayer.py:512-533`
**Decision**: Depends on Task 2.3 (FantasyPlayer.py handling)

- [ ] Update or remove `TestGetPositionIncludingFlex` class based on decision
- [ ] If keeping local definition, ensure tests still pass
- [ ] If using config, update tests to provide config mock

---

## Phase 4: Cleanup and Documentation

### Task 4.1: Remove FLEX_ELIGIBLE_POSITIONS from constants.py
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/constants.py`
**Decision**: User selected immediate removal (following MAX_POSITIONS pattern)

- [ ] DELETE FLEX_ELIGIBLE_POSITIONS constant (line 64)
- [ ] DELETE get_position_with_flex() function (lines 66-85) if moved to ConfigManager
- [ ] Update module docstring (lines 1-17) to remove FLEX_ELIGIBLE_POSITIONS mention
- [ ] Update "FLEX-eligible positions" comment (line 63)

**Verify**: Ensure all code references updated before deletion (Phase 2 complete)

### Task 4.2: Update CLAUDE.md
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/CLAUDE.md`
- [ ] Search for mentions of FLEX_ELIGIBLE_POSITIONS
- [ ] Update to reflect config-based approach
- [ ] Update configuration section if present

### Task 4.3: Update README.md
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/README.md`
- [ ] Search for FLEX_ELIGIBLE_POSITIONS mentions
- [ ] Update configuration documentation
- [ ] Add note about league_config.json structure

### Task 4.4: Update rules.txt if needed
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/rules.txt`
- [ ] Check for FLEX_ELIGIBLE_POSITIONS references
- [ ] Update if present

---

## Phase 5: Pre-Commit Validation

### Task 5.1: Run all unit tests
- [ ] Execute: `python tests/run_all_tests.py`
- [ ] Ensure 100% pass rate (1851/1851 tests)
- [ ] Fix any failing tests before proceeding

### Task 5.2: Manual testing
- [ ] Run league helper: `python run_league_helper.py`
- [ ] Test Add to Roster mode (uses position logic)
- [ ] Test Trade Simulator mode (uses FLEX eligibility)
- [ ] Verify FLEX slot assignment works correctly
- [ ] Test with different FLEX_ELIGIBLE_POSITIONS values

### Task 5.3: Verify configuration loads correctly
- [ ] Start league helper and check logs
- [ ] Verify no errors loading FLEX_ELIGIBLE_POSITIONS from config
- [ ] Verify validation catches malformed config (empty list, FLEX in list, invalid positions)

---

## CRITICAL: Phase Execution Order

**⚠️ MANDATORY EXECUTION SEQUENCE** - Do NOT deviate from this order:

1. **Phase 1**: Add FLEX_ELIGIBLE_POSITIONS to config system (Tasks 1.1-1.6)
   - Must complete before Phase 2
   - Config must load successfully before code can use it

2. **Phase 2**: Update all code references to use config (Tasks 2.1-2.3)
   - Must complete before Phase 4
   - All Constants.FLEX_ELIGIBLE_POSITIONS → self.config.flex_eligible_positions
   - **BLOCKED**: Task 2.3 awaiting user decision on FantasyPlayer.py

3. **Phase 3**: Update tests (Tasks 3.1-3.4)
   - PROACTIVE: Update test mocks BEFORE running tests
   - Create new ConfigManager tests
   - Update constants tests

4. **Phase 4**: Remove constants and update docs (Tasks 4.1-4.4)
   - **ONLY after Phases 1-3 complete**
   - Removing constants too early will break everything
   - Verify no remaining references before removal

5. **Phase 5**: Validation (Tasks 5.1-5.3)
   - Run ALL tests - must pass 100%
   - Manual testing of all modes
   - Verify config loads correctly

**FAILURE MODE**: If you remove constants.py entries before updating all code references, tests will fail immediately. Follow the order!

---

## IMPORTANT NOTES

### Simulation System Consistency
Per objective requirements: **Keep FLEX_ELIGIBLE_POSITIONS the same for all simulation runs**. Do NOT add FLEX_ELIGIBLE_POSITIONS to simulation config variations.

**Files to check**:
- `simulation/ConfigGenerator.py` - Do NOT add to parameter variations
- `simulation/SimulationManager.py` - Verify uses global config

**Current State**: Verified ✅ - simulation/ folder has NO references to FLEX_ELIGIBLE_POSITIONS

### Backward Compatibility
**Decision**: User selected immediate removal (following MAX_POSITIONS pattern)
- FLEX_ELIGIBLE_POSITIONS will be removed from constants.py in Phase 4
- All internal references must be updated in Phase 2 before removal
- No external code compatibility layer (clean break)

### Edge Cases to Test
- [ ] Empty FLEX_ELIGIBLE_POSITIONS list (should fail validation)
- [ ] FLEX in FLEX_ELIGIBLE_POSITIONS list (circular reference - should fail)
- [ ] Invalid position in list (e.g., typo "RBB")
- [ ] Only one position in list (minimal valid config)
- [ ] All positions in list (QB, RB, WR, TE, K, DST - maximum valid config)
- [ ] FantasyPlayer.py method behavior with different config values

### Pattern Consistency with MAX_POSITIONS
Following same patterns as MAX_POSITIONS migration:
- ✅ Config structure: List of strings in parameters section
- ✅ ConfigManager attribute: `self.flex_eligible_positions: List[str]`
- ✅ Validation: Strict (required, non-empty, valid values)
- ✅ Testing: Dedicated test file + mock updates
- ✅ Cleanup: Immediate removal from constants
- ✅ Simulation: No variation (use global value)

---

## ✅ BLOCKERS RESOLVED

### ~~CRITICAL BLOCKER: FantasyPlayer.py Discrepancy~~ - RESOLVED

**Resolution**: User confirmed this was a bug. The correct value is `['RB', 'WR']` (FantasyPlayer.py was correct, constants.py was wrong).

**Decision**: Keep FantasyPlayer.py hardcoded value and add explanatory comment. This avoids adding config dependency to a simple data class.

---

## Verification Summary

### First Verification Round (Iterations 1-3)
**Completed**: Before creating questions file

**Findings from First Round**:
- Identified 22 total code references to FLEX_ELIGIBLE_POSITIONS
- Discovered critical discrepancy: FantasyPlayer.py uses `['RB', 'WR']` vs constants.py uses `['RB', 'WR', 'TE', 'DST']`
- Found get_position_with_flex() function needs migration
- Identified 13 test files requiring mock updates
- Confirmed simulation system has no references (no variation needed)

**Questions Generated**: 8 decision points documented in questions file

---

### Second Verification Round (Iterations 4-6)
**Status**: ✅ COMPLETE - All 6 iterations finished (3 before questions + 3 after answers)

**Iteration 4 - Requirements Verification**:

✅ **ALL Requirements from Original File Covered**:
1. ✅ Move FLEX_ELIGIBLE_POSITIONS from constants.py to config.json - Phase 1 Task 1.1, Phase 4 Task 4.1
2. ✅ Update ConfigManager to read values - Phase 1 Tasks 1.2-1.6
3. ✅ Allow manipulation throughout season - Config-based approach enables this
4. ✅ Keep simulation consistent (no variation) - Verified in Task 2.3, simulation/ has no references
5. ✅ Update ALL places using constant - Phase 2 covers all 4 production files, Phase 3 covers test files

✅ **ALL Question Answers Integrated**:
1. ✅ Default value `["RB", "WR"]` - Task 1.1 uses this value
2. ✅ List format - Task 1.1 uses JSON array format
3. ✅ Strict validation - Task 1.6 implements comprehensive validation
4. ✅ get_position_with_flex() to ConfigManager - Task 1.6b adds method, Task 4.2 removes from constants
5. ✅ FantasyPlayer.py bug fix - Task 2.3 adds explanatory comment, keeps hardcoded value
6. ✅ No simulation variation - No tasks add to simulation config generator
7. ✅ Required parameter - Task 1.4 adds to required_params list
8. ✅ Create dedicated test file - Task 3.1 creates test_ConfigManager_flex_eligible_positions.py

**Files Verified** (15 files with FLEX_ELIGIBLE_POSITIONS references):
- ✅ league_helper/util/ConfigManager.py - Phase 1 (6 changes)
- ✅ data/league_config.json - Phase 1 Task 1.1
- ✅ league_helper/constants.py - Phase 2 Task 2.2, Phase 4 Tasks 4.1-4.3
- ✅ league_helper/util/FantasyTeam.py - Phase 2 Task 2.1 (7 changes)
- ✅ utils/FantasyPlayer.py - Phase 2 Task 2.3
- ✅ tests/league_helper/test_constants.py - Phase 3 Task 3.2 (4 test updates)
- ✅ tests/league_helper/util/test_PlayerManager_scoring.py - Phase 3 Task 3.3 (mock update)
- ✅ 13 test files with config mocks - Phase 3 Task 3.3 (proactive mock updates)

**100% Requirement Coverage**: ✅ Verified

**Iteration 5 - Deep Dive Verification**:

✅ **Error Handling Verified**:
- Pattern confirmed: `self.logger.error()` before raising ValueError
- All validation errors log error message before raising
- Pattern already implemented in Task 1.6 validation code
- Matches existing ConfigManager error handling (lines 699-700, 793-794)

✅ **Logging Requirements Verified**:
- Debug logging for successful operations - Task 1.6 includes: `self.logger.debug(f"FLEX_ELIGIBLE_POSITIONS validated: ...")`
- Error logging before raising exceptions - Task 1.6 includes error logging for all 4 validation checks
- Matches existing pattern in MAX_POSITIONS validation (line 804)

✅ **Documentation Requirements**:
- README.md - Phase 4 Task 4.3 includes checking for mentions
- CLAUDE.md - Phase 4 Task 4.2 includes updating if needed
- rules.txt - Phase 4 Task 4.4 includes checking for references
- ARCHITECTURE.md - Not explicitly mentioned but likely mentions constants.py

✅ **Performance Considerations**:
- No performance concerns - simple list membership checks (`in` operator)
- Config loaded once at initialization, cached in memory
- get_position_with_flex() is O(n) where n = number of FLEX-eligible positions (typically 2-4)

✅ **Backward Compatibility**:
- Intentionally breaking - FLEX_ELIGIBLE_POSITIONS is required parameter
- User decision confirmed: Fail if missing (Option A from Q7)
- Risk documented in TODO: "Existing configs will fail without FLEX_ELIGIBLE_POSITIONS (intentional)"

✅ **Integration Points Verified**:
- Searched for broader "flex" and "position" patterns - 41 files found
- Verified no additional production code files use FLEX_ELIGIBLE_POSITIONS constant
- Only files in TODO are: constants.py, FantasyTeam.py, FantasyPlayer.py, ConfigManager.py
- Test files covered in Phase 3 Task 3.3 (13 test files with mocks)

**Iteration 6 - Final Verification**:

✅ **Circular Dependency Risk**: NONE
- ConfigManager is a leaf dependency (no circular imports)
- FantasyTeam already imports ConfigManager (line verified)
- constants.py has no imports of ConfigManager (safe to remove constant)
- FantasyPlayer.py doesn't import ConfigManager (intentionally hardcoded)

✅ **Failure Scenarios Addressed**:
- Missing parameter → ValueError with logged error message (Task 1.4)
- Empty list → ValueError with logged error message (Task 1.6)
- FLEX in list (circular reference) → ValueError with logged error message (Task 1.6)
- Invalid position → ValueError with logged error message (Task 1.6)
- Non-list type → ValueError with logged error message (Task 1.6)
- All failures happen during ConfigManager.__init__, preventing system startup with invalid config

✅ **File Path Safety**:
- All paths are absolute or properly constructed via Path objects
- league_config.json path: `data_folder / 'league_config.json'` (existing pattern)
- Test file path: `tests/league_helper/util/test_ConfigManager_flex_eligible_positions.py` (follows structure)
- No relative path dependencies

✅ **Mock Pattern Verified**:
- Examined test_ConfigManager_max_positions.py structure (lines 1-60)
- Pattern confirmed: temp_data_folder fixture + valid_config fixture
- Config written to JSON, ConfigManager instantiated
- Same pattern specified in Phase 3 Task 3.1 (new test file)
- Mock updates for 13 test files: add `mock_config.flex_eligible_positions = ['RB', 'WR']`

✅ **Task Order Safety Verified**:
- Phase 1 (Config System): Safe - adds new parameter, doesn't break existing code
- Phase 2 (Production Code): Safe ONLY AFTER Phase 1 - requires config.flex_eligible_positions to exist
- Phase 3 (Tests): Safe - updates tests to match new implementation
- Phase 4 (Cleanup): Safe ONLY AFTER Phases 1-3 - removes constant only after all references updated
- Phase 5 (Validation): Must run after each phase to ensure system still works
- **CRITICAL**: Must NOT remove constant (Phase 4) before updating all code references (Phase 2)

✅ **Cleanup/Rollback**:
- No cleanup needed - config changes are atomic (all-or-nothing)
- If tests fail: fix issues, re-run tests, don't proceed
- Git provides rollback mechanism if needed
- No temporary files or intermediate states to clean up

✅ **Pre-Commit Validation Checkpoints Added**:
- Phase 5 Task 5.1: Run all unit tests (MANDATORY before commit)
- Phase 5 Task 5.2: Manual testing of league helper modes
- Phase 5 Task 5.3: Verify configuration loads correctly
- Each checkpoint must pass before marking objective complete

✅ **Integration Testing Requirements**:
- Task 5.2 covers integration testing (manual testing of all modes)
- Specifically test: Add to Roster mode, Trade Simulator mode (both use FLEX logic)
- Verify FLEX slot assignment works correctly with new config value `['RB', 'WR']`
- Verify TE and DST no longer assigned to FLEX (behavior change)

---

### Verification Round Summary

**Total Iterations**: 6 (3 before questions file + 3 after user answers)

**Requirements Added After Initial Draft**:
- Explicit test mock update task (Task 3.3) - identified 13 files
- ARCHITECTURE.md documentation update (Phase 4)
- Integration testing checkpoints (Phase 5 Task 5.2)
- Behavior change verification (Phase 5 Task 5.2 - TE/DST no longer FLEX-eligible)

**Key Patterns Identified**:
- ConfigManager 5-step pattern: ConfigKeys → attribute → required → extract → validate
- Error handling pattern: `self.logger.error()` before `raise ValueError()`
- Test pattern: temp_data_folder fixture + complete config JSON
- Mock pattern: `mock_config.flex_eligible_positions = ['RB', 'WR']`

**Critical Dependencies**:
1. Phase 2 depends on Phase 1 (config must load flex_eligible_positions first)
2. Phase 4 depends on Phases 1-3 (can't remove constant until all references updated)
3. All phases depend on Phase 5 validation (tests must pass)

**Risk Areas Mitigated**:
1. ✅ FantasyPlayer.py conflict - RESOLVED (keep hardcoded with comment)
2. ⚠️ Test mocks - Task 3.3 addresses all 13 files
3. ✅ Simulation system - Confirmed no variation needed
4. ✅ Function migration - get_position_with_flex() moves to ConfigManager
5. ⚠️ Backward compatibility - Intentional breaking change (required parameter)

**Final Acceptance Criteria**:
- ✅ All requirements from original file mapped to tasks
- ✅ All question answers integrated into implementation plan
- ✅ Specific file paths identified for each task
- ✅ Existing code patterns researched and documented
- ✅ Test requirements specified (new test file + 13 mock updates)
- ✅ Task dependencies and ordering verified as safe
- ✅ Edge cases addressed (empty list, circular reference, invalid positions, wrong type)
- ✅ Documentation update tasks included (README, CLAUDE.md, rules.txt, ARCHITECTURE.md)
- ✅ Pre-commit validation checkpoints mandatory at each phase

---

### User Decisions Confirmed
1. ✅ Default value: `["RB", "WR"]` (Option B - more restrictive)
2. ✅ Config format: List (Option A)
3. ✅ Validation: Strict (Option A)
4. ✅ get_position_with_flex(): Move to ConfigManager (Option B)
5. ✅ FantasyPlayer.py: Was a bug, keep hardcoded `['RB', 'WR']` with comment (Option A adapted)
6. ✅ Simulation: No variation (Option B - already verified)
7. ✅ Required parameter: Fail if missing (Option A)
8. ✅ Create dedicated test file (Option A)

### Codebase Patterns Found
- **ConfigManager pattern**: ConfigKeys → __init__ attribute → required_params → extract → validate
- **FantasyTeam** has `self.config` available (verified)
- **Test pattern**: temp_data_folder fixture + minimal config JSON
- **Mock pattern**: 13 test files confirmed need flex_eligible_positions attribute
- **Validation pattern**: Type check + non-empty + value validation + no circular reference

### Critical Dependencies
- **get_position_with_flex()** function in constants.py - RESOLVED (moving to ConfigManager)
- **FantasyPlayer.py** local definition - RESOLVED (user confirmed bug, keeping hardcoded with comment)
- **Tests** verify behavior - Phase 3 updates test expectations

### Risk Areas
1. ✅ **FantasyPlayer.py conflict**: RESOLVED - keep hardcoded with comment
2. ⚠️ **Test mocks**: 13 test files need attribute added (Task 3.3)
3. ✅ **Simulation system**: Verified no variation needed
4. ✅ **Function migration**: Moving to ConfigManager (Tasks 1.6b, 2.2)
5. ⚠️ **Backward compatibility**: Existing configs will fail without FLEX_ELIGIBLE_POSITIONS (intentional - required parameter)

---

## Next Steps

1. **User reviews questions file**: `updates/FLEX_ELIGIBLE_POSITIONS_config_questions.md`
2. **User provides decisions** on 8 questions
3. **Critical**: User clarifies FantasyPlayer.py discrepancy (Question #5)
4. **Update this TODO** with user decisions
5. **Begin implementation** following phase order
