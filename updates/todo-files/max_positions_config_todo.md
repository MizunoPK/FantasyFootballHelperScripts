# MAX_POSITIONS Config Migration TODO

**Objective**: Move MAX_POSITIONS constant from constants.py to league_config.json

**Status**: Draft - awaiting verification iterations

**Keep this file updated**: As you complete tasks, mark them as DONE and add notes about any issues encountered or decisions made. This ensures continuity if work spans multiple sessions.

---

## Phase 1: Add MAX_POSITIONS to Configuration System

### Task 1.1: Add MAX_POSITIONS to league_config.json
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/data/league_config.json`
**Decision**: User confirmed use current values with abbreviated keys (Format A)

- [ ] Add `MAX_POSITIONS` key to `parameters` section
- [ ] Use abbreviated position keys: QB, RB, WR, TE, K, DST, FLEX
- [ ] Values (confirmed by user): QB: 2, RB: 4, WR: 4, FLEX: 2, TE: 1, K: 1, DST: 1
- [ ] Place after DRAFT_ORDER or at end of parameters section
- [ ] Format example:
```json
"MAX_POSITIONS": {
  "QB": 2,
  "RB": 4,
  "WR": 4,
  "FLEX": 2,
  "TE": 1,
  "K": 1,
  "DST": 1
}
```

**Pattern**: Similar to INJURY_PENALTIES structure (dict with string keys)

### Task 1.2: Update ConfigKeys class
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:31-105`
- [ ] Add `MAX_POSITIONS = "MAX_POSITIONS"` constant to ConfigKeys class
- [ ] Add to Parameter Keys section (around line 50-65)
- [ ] Follow alphabetical ordering if present

**Pattern**: Similar to `INJURY_PENALTIES` key definition

### Task 1.3: Add max_positions attribute to ConfigManager.__init__
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:143-186`
- [ ] Add `self.max_positions: Dict[str, int] = {}` after injury_penalties (around line 171)
- [ ] Follow existing pattern for dict attributes

**Pattern**: Similar to `self.injury_penalties: Dict[str, float] = {}` (line 171)

### Task 1.4: Add MAX_POSITIONS to required parameters
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:668-685`
- [ ] Add `self.keys.MAX_POSITIONS` to `required_params` list in `_extract_parameters()`
- [ ] Place after `self.keys.DRAFT_ORDER` (around line 684)

**Pattern**: Same format as other required parameter entries

### Task 1.5: Extract MAX_POSITIONS in _extract_parameters
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:693-710`
- [ ] Add `self.max_positions = self.parameters[self.keys.MAX_POSITIONS]` after draft_order extraction (around line 710)

**Pattern**: Similar to `self.injury_penalties = self.parameters[self.keys.INJURY_PENALTIES]` (line 699)

### Task 1.6: Add MAX_POSITIONS validation (STRICT) with logging
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py:715-735`
**Decision**: User selected strict validation (Option A)

- [ ] Add validation block after draft_order validation (around line 740)
- [ ] Validate all required positions present: QB, RB, WR, TE, K, DST, FLEX
- [ ] Validate all values are positive integers (> 0)
- [ ] Log errors before raising (pattern: `self.logger.error()` then `raise ValueError()`)
- [ ] Include descriptive error messages with actual vs expected values
- [ ] Example validation code:
```python
# Validate MAX_POSITIONS structure
required_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX']
missing_positions = [pos for pos in required_positions if pos not in self.max_positions]
if missing_positions:
    error_msg = f"MAX_POSITIONS missing required positions: {', '.join(missing_positions)}"
    self.logger.error(error_msg)
    raise ValueError(error_msg)

# Validate all values are positive integers
for pos, limit in self.max_positions.items():
    if not isinstance(limit, int) or limit <= 0:
        error_msg = f"MAX_POSITIONS[{pos}] must be a positive integer, got: {limit} (type: {type(limit).__name__})"
        self.logger.error(error_msg)
        raise ValueError(error_msg)

# Optional: Log successful validation
self.logger.debug(f"MAX_POSITIONS validated: {sum(self.max_positions.values())} total roster spots")
```

**Pattern**: Similar to injury_penalties validation (lines 716-724) with error logging pattern from lines 486-487

---

## Phase 2: Update Code to Use Config MAX_POSITIONS

### Task 2.1: Update PlayerManager to use config
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/PlayerManager.py`
**Lines**: 172, 437-438

- [ ] Line 172: Change `if player.position not in Constants.MAX_POSITIONS:` to `if player.position not in self.config.max_positions:`
- [ ] Line 437: Change `for pos in Constants.MAX_POSITIONS.keys():` to `for pos in self.config.max_positions.keys():`
- [ ] Line 438: Change `max_count = Constants.MAX_POSITIONS[pos]` to `max_count = self.config.max_positions[pos]`

**Verification**: PlayerManager has `self.config` available (ConfigManager instance)

### Task 2.2: Update FantasyTeam to use config
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/FantasyTeam.py`
**Lines**: 102, 155, 161, 412, 418, 420, 516, 520, 525, 554, 639, 757, 765, 773, 844, 850

- [ ] Line 102: Change `{pos: 0 for pos in Constants.MAX_POSITIONS.keys()}` to `{pos: 0 for pos in self.config.max_positions.keys()}`
- [ ] Line 155: Change `if pos not in Constants.MAX_POSITIONS:` to `if pos not in self.config.max_positions:`
- [ ] Line 161: Change `Constants.MAX_POSITIONS[pos]` to `self.config.max_positions[pos]`
- [ ] Line 412: Change `Constants.MAX_POSITIONS[pos]` to `self.config.max_positions[pos]`
- [ ] Line 418: Change `Constants.MAX_POSITIONS[pos]` to `self.config.max_positions[pos]`
- [ ] Line 420: Change `Constants.MAX_POSITIONS[Constants.FLEX]` to `self.config.max_positions[Constants.FLEX]`
- [ ] Line 516: Change `Constants.MAX_POSITIONS[pos]` to `self.config.max_positions[pos]`
- [ ] Line 520: Change `Constants.MAX_POSITIONS[Constants.FLEX]` to `self.config.max_positions[Constants.FLEX]`
- [ ] Line 525: Change both `Constants.MAX_POSITIONS[pos]` and `Constants.MAX_POSITIONS[Constants.FLEX]` to config versions
- [ ] Line 554: Change `Constants.MAX_POSITIONS.get(pos, 0)` to `self.config.max_positions.get(pos, 0)`
- [ ] Line 639: Change `Constants.MAX_POSITIONS[natural_pos]` to `self.config.max_positions[natural_pos]`
- [ ] Line 757: Change `Constants.MAX_POSITIONS[pos]` to `self.config.max_positions[pos]`
- [ ] Line 765: Change `Constants.MAX_POSITIONS[Constants.FLEX]` to `self.config.max_positions[Constants.FLEX]`
- [ ] Line 773: Change both occurrences to config versions
- [ ] Line 844: Change `Constants.MAX_POSITIONS[new_pos]` to `self.config.max_positions[new_pos]`
- [ ] Line 850: Change `Constants.MAX_POSITIONS[Constants.FLEX]` to `self.config.max_positions[Constants.FLEX]`

**Verification**: FantasyTeam has `self.config` available (ConfigManager instance passed in __init__)

### Task 2.3: Update trade_analyzer to use config
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/trade_simulator_mode/trade_analyzer.py`
**Lines**: 67, 326, 386, 395

- [ ] Line 67: Change `{pos: 0 for pos in Constants.MAX_POSITIONS.keys()}` to `{pos: 0 for pos in self.config.max_positions.keys()}`
- [ ] Line 326: Change `{pos: [] for pos in Constants.MAX_POSITIONS.keys()}` to `{pos: [] for pos in self.config.max_positions.keys()}`
- [ ] Line 386: Change `{pos: 0 for pos in Constants.MAX_POSITIONS.keys()}` to `{pos: 0 for pos in self.config.max_positions.keys()}`
- [ ] Line 395: Change `Constants.MAX_POSITIONS[position]` to `self.config.max_positions[position]`

**Verification**: TradeAnalyzer has `self.config` available (ConfigManager instance)

---

## Phase 2.5: Handle MAX_PLAYERS Dependency

### Task 2.5.1: Calculate MAX_PLAYERS dynamically as property
**Decision**: User selected Option B - Calculate dynamically

**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/ConfigManager.py`
- [ ] Add property method after max_positions attribute (around line 180):
```python
@property
def max_players(self) -> int:
    """
    Calculate total roster size as sum of MAX_POSITIONS.

    Returns:
        int: Total maximum players allowed (sum of all position limits)
    """
    return sum(self.max_positions.values())
```

### Task 2.5.2: Update all MAX_PLAYERS references to use config property
**Files to update** (14 occurrences):
- [ ] PlayerManager.py: line 455 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] FantasyTeam.py: line 105 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] FantasyTeam.py: line 115 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] FantasyTeam.py: line 149 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] FantasyTeam.py: line 266 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] FantasyTeam.py: line 338 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] FantasyTeam.py: line 560 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] FantasyTeam.py: line 561 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] FantasyTeam.py: line 729 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] AddToRosterModeManager.py: line 128 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] AddToRosterModeManager.py: line 134 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] AddToRosterModeManager.py: line 345 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] AddToRosterModeManager.py: line 363 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`
- [ ] AddToRosterModeManager.py: line 412 - Change `Constants.MAX_PLAYERS` to `self.config.max_players`

**Note**: AddToRosterModeManager does not have self.config directly, need to verify access path

### Task 2.5.3: Update error messages referencing MAX_POSITIONS
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/util/FantasyTeam.py:773`
- [ ] Update ValueError message to use self.config.max_positions instead of Constants.MAX_POSITIONS
- [ ] Verify message formatting still clear after change

---

## Phase 3: Update Tests

### Task 3.1: Remove MAX_POSITIONS/MAX_PLAYERS tests from constants test
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/tests/league_helper/test_constants.py`
**Affected tests** (lines 122-140):
- [ ] REMOVE `test_max_positions_contains_all_positions()` (lines 122-125)
- [ ] REMOVE `test_max_positions_values_are_positive()` (lines 127-131)
- [ ] REMOVE `test_max_positions_sums_to_max_players()` (lines 133-136)
- [ ] REMOVE `test_max_players_is_15()` (lines 138-140)

**Rationale**: These constants no longer exist; validation moved to ConfigManager tests (Task 3.2)

### Task 3.2: Add ConfigManager tests for MAX_POSITIONS
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/tests/league_helper/util/test_ConfigManager_max_positions.py` (new file)
**Pattern**: Follow test_ConfigManager_thresholds.py structure

**Tests to create**:
- [ ] `test_max_positions_loads_from_config()` - Verify max_positions attribute populated
- [ ] `test_max_positions_contains_all_required_positions()` - QB, RB, WR, TE, K, DST, FLEX present
- [ ] `test_max_positions_values_are_positive_integers()` - All values > 0 and type int
- [ ] `test_max_positions_missing_position_raises_error()` - Missing QB/RB/etc raises ValueError
- [ ] `test_max_positions_invalid_value_raises_error()` - Negative/zero/non-int raises ValueError
- [ ] `test_max_positions_extra_position_allowed()` - Unknown position key doesn't fail (or does, based on strict validation)
- [ ] `test_max_players_property_calculates_sum()` - Verify max_players == sum(max_positions.values())
- [ ] `test_max_players_property_equals_15()` - With default values, max_players == 15

**Use temp_data_folder fixture and create minimal config JSON with MAX_POSITIONS**

### Task 3.3: Update all test files that mock config (PROACTIVE)
**Decision**: User selected proactive update (Option B) - update all mocks before running tests

**Files**: 13 test files identified that mock ConfigManager
- [ ] Search for all config mocks: `grep -r "Mock.*ConfigManager\|mock.*config" tests/`
- [ ] Update EACH mock to include `max_positions` attribute
- [ ] Add to each mock: `mock_config.max_positions = {'QB': 2, 'RB': 4, 'WR': 4, 'FLEX': 2, 'TE': 1, 'K': 1, 'DST': 1}`
- [ ] Handle `max_players` property in mocks:
  - Option A: Add as simple attribute: `mock_config.max_players = 15`
  - Option B: Use PropertyMock: `type(mock_config).max_players = PropertyMock(return_value=15)`
  - **Recommended**: Option A for simplicity (mocks don't need dynamic calculation)

**Test files identified** (13 total):
1. tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py
2. tests/league_helper/util/test_PlayerManager_scoring.py
3. tests/league_helper/trade_simulator_mode/test_trade_analyzer.py
4. tests/league_helper/trade_simulator_mode/test_trade_simulator.py
5. tests/simulation/test_SimulatedLeague.py
6. tests/simulation/test_manual_simulation.py
7. tests/league_helper/test_LeagueHelperManager.py
8. tests/league_helper/starter_helper_mode/test_StarterHelperModeManager.py
9. tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py
10. tests/league_helper/util/test_ProjectedPointsManager.py
11. tests/simulation/test_DraftHelperTeam.py
12. tests/simulation/test_ParallelLeagueRunner.py
13. tests/simulation/test_simulation_manager.py

### Task 3.4: Update tests that reference Constants.MAX_POSITIONS
**Files**: Test files found in grep search
- [ ] Update any tests that import or use Constants.MAX_POSITIONS
- [ ] Change to use config.max_positions instead
- [ ] Ensure test fixtures provide proper config mock

---

## Phase 4: Cleanup and Documentation

### Task 4.1: Remove MAX_POSITIONS and MAX_PLAYERS from constants.py
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/league_helper/constants.py`
**Decision**: User selected Option B - Remove immediately (no deprecation period)

- [ ] DELETE MAX_POSITIONS constant (lines 60-68)
- [ ] DELETE MAX_PLAYERS constant (line 71)
- [ ] Update module docstring (lines 1-17) to remove MAX_POSITIONS mention
- [ ] Update "Roster construction limits" comment section
- [ ] Keep FLEX_ELIGIBLE_POSITIONS constant (still needed for position logic)

**Affected lines**:
- Lines 60-68: MAX_POSITIONS dict definition
- Line 71: MAX_PLAYERS = 15
- Lines 7-9: Module docstring mentions

**Verify**: Ensure all code references updated before deletion (Phase 2 complete)

### Task 4.2: Update CLAUDE.md
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/CLAUDE.md`
- [ ] Search for mentions of MAX_POSITIONS
- [ ] Update to reflect config-based approach
- [ ] Update configuration section if present

### Task 4.3: Update README.md
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/README.md`
- [ ] Search for MAX_POSITIONS mentions
- [ ] Update configuration documentation
- [ ] Add note about league_config.json structure

### Task 4.4: Update rules.md if needed
**File**: `/home/kai/code/FantasyFootballHelperScriptsRefactored/rules.md`
- [ ] Check for MAX_POSITIONS references
- [ ] Update if present

---

## Phase 5: Pre-Commit Validation

### Task 5.1: Run all unit tests
- [ ] Execute: `python tests/run_all_tests.py`
- [ ] Ensure 100% pass rate
- [ ] Fix any failing tests before proceeding

### Task 5.2: Manual testing
- [ ] Run league helper: `python run_league_helper.py`
- [ ] Test Add to Roster mode (uses draft_player which checks MAX_POSITIONS)
- [ ] Test Trade Simulator mode (uses position counting)
- [ ] Verify roster limits are enforced correctly

### Task 5.3: Verify configuration loads correctly
- [ ] Start league helper and check logs
- [ ] Verify no errors loading MAX_POSITIONS from config
- [ ] Verify validation catches malformed config

---

## CRITICAL: Phase Execution Order

**⚠️ MANDATORY EXECUTION SEQUENCE** - Do NOT deviate from this order:

1. **Phase 1**: Add MAX_POSITIONS to config system (Tasks 1.1-1.6)
   - Must complete before Phase 2
   - Config must load successfully before code can use it

2. **Phase 2**: Update all code references to use config (Tasks 2.1-2.3)
   - Must complete before Phase 2.5
   - All Constants.MAX_POSITIONS → self.config.max_positions

3. **Phase 2.5**: Handle MAX_PLAYERS (Tasks 2.5.1-2.5.3)
   - Add max_players property to ConfigManager
   - Update all Constants.MAX_PLAYERS → self.config.max_players
   - Must complete before Phase 4 (constants removal)

4. **Phase 3**: Update tests (Tasks 3.1-3.4)
   - PROACTIVE: Update test mocks BEFORE running tests
   - Create new ConfigManager tests
   - Remove old constants tests

5. **Phase 4**: Remove constants and update docs (Tasks 4.1-4.4)
   - **ONLY after Phases 1-3 complete**
   - Removing constants too early will break everything
   - Verify no remaining references before removal

6. **Phase 5**: Validation (Tasks 5.1-5.3)
   - Run ALL tests - must pass 100%
   - Manual testing of all modes
   - Verify config loads correctly

**FAILURE MODE**: If you remove constants.py entries before updating all code references, tests will fail immediately. Follow the order!

---

## IMPORTANT NOTES

### Simulation System Consistency
Per objective requirements: **Keep MAX_POSITIONS the same for all simulation runs**. Do NOT add MAX_POSITIONS to simulation config variations. The simulation system should use the global league_config.json value, not per-simulation values.

**Files to check**:
- `simulation/ConfigGenerator.py` - Do NOT add MAX_POSITIONS to parameter variations
- `simulation/SimulationManager.py` - Verify uses global config

### Backward Compatibility
**Decision**: User selected immediate removal (no deprecation period)
- MAX_POSITIONS and MAX_PLAYERS will be removed from constants.py in Phase 4
- All internal references must be updated in Phase 2 before removal
- No external code compatibility layer (clean break)

### Edge Cases to Test
- [ ] Empty roster (no players to count)
- [ ] Full roster at all position limits
- [ ] FLEX overflow scenarios (RB/WR exceeding limits)
- [ ] Invalid position in config (e.g., typo "RBB")
- [ ] Missing position in config
- [ ] Negative or zero limits in config

---

## Verification Summary

**Iterations Completed**: 6/6 (Both rounds complete! ✅)
- First round (3 iterations): ✅ COMPLETE
- Second round (3 iterations): ✅ COMPLETE
- **Status**: Ready for implementation

**User Decisions Integrated**:
1. ✅ MAX_PLAYERS: Calculate dynamically as `@property`
2. ✅ Constants: Remove immediately (no deprecation)
3. ✅ Default values: QB:2, RB:4, WR:4, FLEX:2, TE:1, K:1, DST:1
4. ✅ Config format: Use abbreviations (QB, RB, WR, etc.)
5. ✅ Validation: Strict (require all positions, positive integers)
6. ✅ Testing: Update mocks proactively

**Requirements Identified**:
1. Move MAX_POSITIONS from constants.py to league_config.json ✅
2. Update ConfigManager to read values ✅
3. Update all code references (PlayerManager, FantasyTeam, TradeAnalyzer) ✅
4. Keep same for simulation runs (no per-simulation variation) ✅
5. Handle MAX_PLAYERS dependency (calculate dynamically) ✅
6. Update error messages that reference MAX_POSITIONS ✅
7. Remove MAX_POSITIONS/MAX_PLAYERS from constants.py ✅

**Codebase Patterns Found**:
- **ConfigManager pattern**: ConfigKeys → __init__ attribute → required_params → extract → validate
- **All target classes** already have `self.config` available (verified: FantasyTeam line 64, PlayerManager, TradeAnalyzer)
- **Test pattern**: temp_data_folder fixture + minimal config JSON (from test_ConfigManager_thresholds.py)
- **Mock pattern**: 13 test files mock config, will need max_positions attribute added
- **Validation pattern**: Required keys check + structure validation + value range validation
- **Error handling**: ValueError with descriptive messages for invalid config

**Dependencies Identified**:
- **CRITICAL**: MAX_PLAYERS (constants.py line 71) tightly coupled to MAX_POSITIONS
  - Used in 14 places: PlayerManager (1), FantasyTeam (7), AddToRosterModeManager (5)
  - Test validates: `sum(MAX_POSITIONS.values()) == MAX_PLAYERS`
  - **Recommended approach**: Calculate dynamically as property to avoid duplication
- **Simulation independence verified**: ConfigGenerator.py does NOT vary MAX_POSITIONS ✅
- **Error message dependency**: FantasyTeam.py:773 includes MAX_POSITIONS in ValueError message

**Risk Areas**:
1. **MAX_PLAYERS consistency**: Must maintain sum(max_positions.values()) == max_players relationship
2. **Test mocks**: 13 test files need max_positions attribute added to config mocks
3. **Simulation system**: Must use global league_config.json, not per-simulation values (verified ✅)
4. **Backward compatibility**: Existing code may depend on Constants.MAX_POSITIONS
5. **Error messages**: Must update ValueError messages that reference MAX_POSITIONS/MAX_PLAYERS

**Iteration 4-6 Refinements**:
- ✅ AddToRosterModeManager confirmed to have self.config (line 78)
- ✅ No circular import risks (ConfigManager only imports standard lib + constants + logging)
- ✅ Error handling pattern: log error, then raise ValueError with descriptive message
- ✅ Logging pattern: debug for success, error before exceptions
- ✅ Test constants.py has 4 tests to remove/migrate (lines 122-140)
- ✅ Test mocks can use simple attribute for max_players (no PropertyMock needed)
- ✅ Phase execution order documented with mandatory sequence
- ✅ Critical failure mode identified: removing constants before updating references

**Integration Points Verified**:
- ConfigManager → (used by) → PlayerManager, FantasyTeam, TradeAnalyzer, All mode managers ✅
- No reverse dependencies that could cause circular imports ✅
- Simulation system uses global config (ConfigGenerator verified) ✅
