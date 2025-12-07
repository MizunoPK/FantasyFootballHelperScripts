# TODO: Different Player Bye Penalty Implementation

**Objective**: Add `DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY` parameter that penalizes bye week overlaps with different positions (separate from same-position overlaps handled by `BASE_BYE_PENALTY`).

**Status**: Iteration 3 Complete - Ready for Implementation

---

## Verification Summary (Iteration 3 - Final)

**Integration Point Analysis**:
- `get_bye_week_penalty()` called from: PlayerManager._apply_bye_week_penalty (line 837)
- `score_player()` called from: TradeSimTeam (line 35, 37), AddToRosterModeManager, StarterHelperModeManager, TradeSimulatorModeManager, SimulatedLeague, and test files
- TradeSimTeam passes `roster=self.team` parameter (line 35, 37) - confirms roster parameter pattern is widely used
- No circular dependency risks identified between ConfigManager and PlayerManager

**Mock Object Requirements**:
- ConfigManager mocking: Use tmp_path to create actual JSON files (pattern from test_PlayerManager_scoring.py lines 36-184)
- PlayerManager mocking: Use `PlayerManager.__new__()` then set attributes (pattern from test_PlayerManager_scoring.py lines 211-220)
- FantasyTeam mocking: Use `Mock(spec=FantasyTeam)` with mocked `get_matching_byes_in_roster` (pattern from test_PlayerManager_scoring.py lines 200-205)
- Test fixture pattern: `@pytest.fixture` with `tmp_path` for temporary config files (lines 36-95 in test_PlayerManager_scoring.py)

**Test Fixture Patterns Identified**:
```python
# ConfigManager test fixture pattern (from test_ConfigGenerator.py):
@pytest.fixture
def temp_config_file(tmp_path):
    config = {...}  # Full config dict
    config_file = tmp_path / "league_config.json"
    config_file.write_text(json.dumps(config))
    return config_file

# ConfigManager instantiation:
config_manager = ConfigManager(tmp_path)  # Pass folder, not file
```

**Rollback/Cleanup Requirements**:
- No database or persistent state changes - only JSON file modifications
- Old simulation results are immutable snapshots - don't require migration
- If implementation fails mid-phase: revert ConfigManager changes before PlayerManager changes (dependency order)
- Test failures should not leave partial state - each test uses isolated tmp_path fixtures

**File Path Construction**:
- ConfigManager expects data folder path: `ConfigManager(data_folder_path)`
- PlayerManager expects players.csv file path: `pm.file_str = str(data_folder / "players.csv")`
- ConfigGenerator expects config file path: `ConfigGenerator(config_file_path)`
- All paths should be absolute (use Path.resolve() if needed)

**Failure Scenarios and Handling**:
- Missing DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY in config → ValueError (ConfigManager line 226 pattern)
- Invalid parameter type → ValueError during extraction (ConfigManager line 231 pattern)
- Roster parameter None → Use self.team.roster fallback (PlayerManager line 822 pattern)
- Bye week None → Filtered during consistency calculation, safe to compare
- Player position invalid → Caught during CSV load (PlayerManager line 154)

**Critical Integration Points**:
1. **ConfigManager → PlayerManager**: `get_bye_week_penalty()` signature change requires updating PlayerManager caller (only 1 location - line 837)
2. **ConfigGenerator → SimulatedLeague**: New parameter automatically included in generated configs (no special handling needed)
3. **PlayerManager → TradeSimTeam**: Roster parameter already passed correctly (line 35, 37)
4. **Test mocking**: Must mock ConfigManager.get_bye_week_penalty with new signature: `(num_same_pos: int, num_diff_pos: int) → float`

**Risk Areas**:
- ⚠️ **Signature change to get_bye_week_penalty**: Only 1 caller but must update it correctly
- ⚠️ **Manual roster iteration logic**: Must correctly exclude player being scored (check player.id equality)
- ⚠️ **FLEX position handling**: Must use player.position (actual RB/WR/TE), never "FLEX" string
- ⚠️ **Test coverage**: Must test both same-position and different-position overlaps separately and combined

**Pre-commit Validation Checkpoints**:
1. After Phase 1 (Config system): Run config loading tests
2. After Phase 2 (Logic implementation): Run PlayerManager scoring tests + full suite
3. After Phase 3 (Simulation): Run ConfigGenerator tests + manual config generation test
4. After Phase 4 (Unit tests): Run ALL tests with 100% pass requirement
5. After Phase 5-6 (Docs/manual testing): Final full test suite + integration test
6. Phase 7: Final validation before marking complete

**Verification Iterations Summary**:
- ✅ **3 iterations completed** (minimum requirement met)
- ✅ **15 requirements added** after initial draft (new tests, error handling, logging, integration points)
- ✅ **Key patterns identified**: tmp_path fixtures, Mock(spec=Class), PlayerManager.__new__() pattern, roster parameter handling
- ✅ **Critical dependencies**: get_bye_week_penalty signature change must happen atomically with PlayerManager update
- ✅ **Risk mitigation**: Isolated test fixtures prevent state contamination, ConfigManager validates all parameters

---

## Verification Summary (Iteration 2)

**Error Handling Patterns Identified**:
- ConfigManager uses `ValueError` for missing/invalid parameters (lines 226, 231, 256, 289, 300, 306)
- PlayerManager validates positions against `Constants.MAX_POSITIONS` (line 154)
- Roster parameter pattern: check `if roster is not None:` then use it, else use `self.team.roster` (line 822)
- No explicit None checking for player attributes - assumes data is valid from CSV loader

**Logging Patterns Identified**:
- Use `self.logger.debug()` for step-by-step scoring calculations (lines 669-719)
- Format: `f"Step X - Description for {p.name}: {score:.2f}"`
- Existing bye penalty logging: `f"Step 8 - After bye penalty for {p.name}: {player_score:.2f}"`
- No detailed penalty breakdown logging currently - should add for new different-position counts

**Data Validation Findings**:
- Position validation done during CSV load, not during scoring
- Bye week None values filtered during consistency calculation, not explicitly validated
- No bounds checking on penalty parameter values after loading
- ConfigManager validates structure but not value ranges

**Configuration Management Findings**:
- Old simulation results don't need migration - they're immutable snapshots
- New parameter will be required in all new configs (added to `required_params` list)
- ConfigGenerator automatically includes new parameters in generated configs
- Simulation README documents parameter addition process (lines 324-336)

**Additional Research**:
- Checked simulation README for parameter addition guidelines
- Verified error handling patterns in ConfigManager
- Confirmed logging format used throughout PlayerManager
- Validated roster parameter handling approach

---

## Verification Summary (Iteration 1)

**Files Researched**:
- `league_helper/util/ConfigManager.py` - Configuration loading (lines 453-454 for get_bye_week_penalty)
- `league_helper/util/PlayerManager.py` - Bye penalty implementation (line 809 for _apply_bye_week_penalty)
- `league_helper/util/FantasyTeam.py` - get_matching_byes_in_roster method (line 712)
- `simulation/ConfigGenerator.py` - Parameter optimization system
- `data/league_config.json` - Current config structure
- `tests/league_helper/util/test_PlayerManager_scoring.py` - Existing bye tests

**Key Findings**:
1. FantasyTeam.get_matching_byes_in_roster() only counts same-position overlaps - need to implement different-position counting in PlayerManager
2. No ConfigManager test file exists - need to create from scratch
3. Only 1 call to get_bye_week_penalty (in PlayerManager line 837) - minimal update scope
4. Simulation config templates in `simulation/simulation_configs/` will inherit parameter automatically
5. get_matching_byes_in_roster signature: `(bye_week: int, position: str, is_rostered: bool)`
6. The 9-step algorithm documentation in PlayerManager.py header needs updating

**Missing Requirements Identified**: None - all requirements covered in initial TODO

---

## Phase 1: Add Parameter to Configuration System

### Task 1.1: Add DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY to ConfigKeys
- **File**: `league_helper/util/ConfigManager.py`
- **Location**: ConfigKeys class (around line 56)
- **Action**: Add `DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY = "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY"` constant

### Task 1.2: Update ConfigManager to load new parameter
- **File**: `league_helper/util/ConfigManager.py`
- **Location**: ConfigManager class
- **Actions**:
  - Add `self.different_player_bye_overlap_penalty: float = 0.0` to `__init__` (around line 153)
  - Add key to `required_params` list in `_extract_parameters()` (around line 243)
  - Extract parameter value in `_extract_parameters()`: `self.different_player_bye_overlap_penalty = self.parameters[self.keys.DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY]` (around line 265)

### Task 1.3: Add parameter to league_config.json
- **File**: `data/league_config.json`
- **Location**: parameters section (after BASE_BYE_PENALTY, around line 9)
- **Action**: Add `"DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 5`

---

## Phase 2: Implement Bye Week Penalty Calculation Logic

### Task 2.1: Update _apply_bye_week_penalty method
- **File**: `league_helper/util/PlayerManager.py`
- **Location**: `_apply_bye_week_penalty()` method (line 809)
- **Reference Implementation**: FantasyTeam.get_matching_byes_in_roster (line 712)
- **Current Logic**:
  ```python
  # Current code (simplified):
  num_matching_byes = self.team.get_matching_byes_in_roster(p.bye_week, p.position, p.is_rostered())
  penalty = self.config.get_bye_week_penalty(num_matching_byes)
  ```
- **New Logic**:
  ```python
  # Count same-position overlaps (existing)
  num_same_position = count of roster players with same bye_week AND same position (excluding scored player)

  # Count different-position overlaps (NEW)
  num_different_position = count of roster players with same bye_week AND different position

  # Calculate combined penalty
  penalty = self.config.get_bye_week_penalty(num_same_position, num_different_position)
  ```
- **Implementation Steps**:
  1. Iterate through roster parameter (or self.team.roster if None)
  2. For each roster player: check if bye_week matches
  3. If match: determine if same position (count toward same_pos) or different (count toward diff_pos)
  4. Exclude player being scored (check player.id equality)
  5. Handle FLEX: use player.position (actual RB/WR), never compare against "FLEX"
  6. Update reason string: `"Bye Overlaps: {same_pos} same-position, {diff_pos} different-position"`
- **Edge Cases**:
  - Player being scored already on roster: exclude from counts
  - FLEX assigned players: use their actual position attribute
  - Empty roster: both counts = 0
  - Custom roster parameter: iterate that instead of self.team.roster

### Task 2.2: Update get_bye_week_penalty method in ConfigManager
- **File**: `league_helper/util/ConfigManager.py`
- **Location**: `get_bye_week_penalty()` method (line 453)
- **Current Implementation**:
  ```python
  def get_bye_week_penalty(self, num_matching_byes: int):
      return self.base_bye_penalty * num_matching_byes
  ```
- **New Implementation**:
  ```python
  def get_bye_week_penalty(self, num_same_position_byes: int, num_different_position_byes: int):
      same_penalty = self.base_bye_penalty * num_same_position_byes
      diff_penalty = self.different_player_bye_overlap_penalty * num_different_position_byes
      return same_penalty + diff_penalty
  ```
- **Note**: Only one caller exists (PlayerManager line 837), so signature change is safe

### Task 2.3: Update PlayerManager header documentation
- **File**: `league_helper/util/PlayerManager.py`
- **Location**: Module docstring (lines 1-29)
- **Action**: Update "The 9-step scoring algorithm" section (line 17-26)
- **Current**: "8. Bye Week Penalty (roster conflicts)"
- **New**: "8. Bye Week Penalty (same-position and different-position roster conflicts)"
- **Additional**: Add explanation in module docstring about the two separate penalty types

---

## Phase 3: Update Simulation System

### Task 3.1: Add parameter definition to ConfigGenerator
- **File**: `simulation/ConfigGenerator.py`
- **Location**: PARAM_DEFINITIONS dict (around line 42)
- **Action**: Add `'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY': (10.0, 0.0, 50.0)` (using values from Q1.3 answer)

### Task 3.2: Add to PARAMETER_ORDER list
- **File**: `simulation/ConfigGenerator.py`
- **Location**: PARAMETER_ORDER list (around line 63)
- **Action**: Add `'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY'` after `'BASE_BYE_PENALTY'`

### Task 3.3: Update generate_all_parameter_value_sets
- **File**: `simulation/ConfigGenerator.py`
- **Location**: `generate_all_parameter_value_sets()` method (around line 201)
- **Action**: Add value set generation for DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY (similar to BASE_BYE_PENALTY pattern)

### Task 3.4: Update generate_single_parameter_variations
- **File**: `simulation/ConfigGenerator.py`
- **Location**: `generate_single_parameter_variations()` method (around line 299)
- **Action**: Add elif branch for 'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY' parameter

### Task 3.5: Update config_to_combination
- **File**: `simulation/ConfigGenerator.py`
- **Location**: `config_to_combination()` method (around line 359)
- **Action**: Extract DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY from config

### Task 3.6: Update combination_to_config
- **File**: `simulation/ConfigGenerator.py`
- **Location**: `combination_to_config()` method (around line 391)
- **Action**: Set params['DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY'] from combination

---

## Phase 4: Create Unit Tests

### Task 4.1: Create ConfigManager test file and add bye penalty tests
- **File**: `tests/league_helper/util/test_ConfigManager.py` (**CREATE NEW FILE**)
- **Test Structure**: Follow pattern from test_PlayerManager_scoring.py
- **Required Imports**:
  ```python
  import pytest
  from pathlib import Path
  from unittest.mock import Mock, patch, mock_open
  from league_helper.util.ConfigManager import ConfigManager, ConfigKeys
  ```
- **Test Fixtures**:
  - `sample_config_dict`: Dict with all required parameters including DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY
  - `temp_config_file`: Creates temporary league_config.json with tmp_path
- **Tests to Implement**:
  1. `test_load_config_with_different_player_bye_penalty`: Verify parameter loads correctly
  2. `test_get_bye_week_penalty_with_same_position_only`: Call get_bye_week_penalty(2, 0), expect BASE_BYE × 2
  3. `test_get_bye_week_penalty_with_different_position_only`: Call get_bye_week_penalty(0, 3), expect DIFF_BYE × 3
  4. `test_get_bye_week_penalty_with_mixed_overlaps`: Call get_bye_week_penalty(2, 3), expect (BASE × 2) + (DIFF × 3)
  5. `test_get_bye_week_penalty_with_zero_overlaps`: Call get_bye_week_penalty(0, 0), expect 0
  6. `test_config_validation_fails_when_parameter_missing`: Remove parameter from config, expect ValueError
- **Mocking Strategy**: Use tmp_path to create actual JSON files for realistic testing

### Task 4.2: Update PlayerManager bye week penalty tests
- **File**: `tests/league_helper/util/test_PlayerManager_scoring.py`
- **Tests**:
  - Test same-position overlaps only
  - Test different-position overlaps only
  - Test mixed same and different position overlaps
  - Test player being scored is excluded from counts
  - Test FLEX position handling (counted by actual position)
  - Test with custom roster parameter

### Task 4.3: Add ConfigGenerator tests
- **File**: `tests/simulation/test_config_generator.py`
- **Tests**:
  - Test DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY in parameter definitions
  - Test parameter in generated combinations
  - Test config_to_combination extracts parameter
  - Test combination_to_config sets parameter

---

## Phase 5: Update Documentation

### Task 5.1: Update inline code comments
- **Files**: ConfigManager.py, PlayerManager.py
- **Actions**:
  - Add docstring updates explaining new parameter
  - Update method comments for _apply_bye_week_penalty
  - Add example calculations in comments

### Task 5.2: Update README/CLAUDE.md
- **Files**: README.md, CLAUDE.md (if applicable)
- **Actions**:
  - Document new parameter and its purpose
  - Explain rationale for separate different-position penalty
  - Add example calculation showing both penalties working together

### Task 5.3: Update simulation documentation
- **File**: `simulation/README.md`
- **Actions**:
  - Document new parameter in optimization system
  - Update parameter count and list

---

## Phase 6: Manual Testing and Validation

### Task 6.1: Test with realistic roster scenario
- Create test scenario with multiple bye week overlaps
- Verify both penalties calculate correctly
- Check that player being scored is excluded
- Validate FLEX players use actual position

### Task 6.2: Run full test suite
- **Command**: `python tests/run_all_tests.py`
- **Requirement**: 100% pass rate before proceeding

### Task 6.3: Test simulation system
- Generate sample configuration with new parameter
- Verify ConfigGenerator creates valid configs
- Run short simulation to ensure no errors

---

## Phase 7: Final Verification and Commit

### Task 7.1: Run pre-commit validation
- Execute full test suite
- Verify no regressions
- Check all documentation updated

### Task 7.2: Create code changes documentation
- **File**: `updates/different_player_bye_penalty_code_changes.md`
- Document all changes with file paths, line numbers, before/after code

### Task 7.3: Final requirement verification
- Re-read original requirements file
- Verify all requirements implemented
- Check question answers reflected in implementation

### Task 7.4: Move files to done folder
- Move `updates/different_player_bye_penalty.txt` to `updates/done/`
- Move code changes file to `updates/done/`
- Delete questions file

---

## Notes

- Keep this TODO file updated with progress
- Mark tasks as complete as they're finished
- If issues arise, document them here
- All tests must pass before marking objective complete
