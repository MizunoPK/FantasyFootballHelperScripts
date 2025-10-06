# TODO: JSON Parameter Configuration Implementation

**Objective**: Migrate 23 scoring parameters from config files to JSON-based parameter management system

**Important**: After completing each phase, run the full pre-commit validation protocol (automated script: `python run_pre_commit_validation.py`) and commit changes. Update this file with progress after each step.

---

## Phase 1: Create ParameterJsonManager and Infrastructure

### 1.1 Create ParameterJsonManager class ✅/❌
- **Location**: `shared_files/parameter_json_manager.py`
- **Requirements**:
  - Load JSON parameter files with nested structure for INJURY_PENALTIES
  - Validate all 23 parameters on load using existing validation utilities
  - Clear error messages for missing/malformed files (exit on error)
  - Support both dict-style and attribute-style access
  - Store metadata (config_name, description)
- **Parameters to support (23 total)**:
  1. ADP_EXCELLENT_MULTIPLIER
  2. ADP_GOOD_MULTIPLIER
  3. ADP_POOR_MULTIPLIER
  4. BASE_BYE_PENALTY
  5. DRAFT_ORDER_PRIMARY_BONUS
  6. DRAFT_ORDER_SECONDARY_BONUS
  7. INJURY_PENALTIES (nested: LOW, MEDIUM, HIGH)
  8. MATCHUP_EXCELLENT_MULTIPLIER
  9. MATCHUP_GOOD_MULTIPLIER
  10. MATCHUP_NEUTRAL_MULTIPLIER
  11. MATCHUP_POOR_MULTIPLIER
  12. MATCHUP_VERY_POOR_MULTIPLIER
  13. NORMALIZATION_MAX_SCALE
  14. PLAYER_RATING_EXCELLENT_MULTIPLIER
  15. PLAYER_RATING_GOOD_MULTIPLIER
  16. PLAYER_RATING_POOR_MULTIPLIER
  17. TEAM_EXCELLENT_MULTIPLIER
  18. TEAM_GOOD_MULTIPLIER
  19. TEAM_POOR_MULTIPLIER
  20. CONSISTENCY_LOW_MULTIPLIER
  21. CONSISTENCY_MEDIUM_MULTIPLIER
  22. CONSISTENCY_HIGH_MULTIPLIER
- **Status**: ⬜ Not Started
- **Notes**:

### 1.2 Create unit tests for ParameterJsonManager ✅/❌
- **Location**: `shared_files/tests/test_parameter_json_manager.py`
- **Test Coverage**:
  - Valid JSON loading (nested INJURY_PENALTIES structure)
  - Invalid JSON handling (malformed, missing file, missing parameters)
  - Parameter access (dict and attribute style)
  - Validation (all 23 parameters, ranges, types)
  - Error messages and exit behavior
- **Status**: ⬜ Not Started
- **Notes**:

### 1.3 Update shared_files/parameters.json to nested structure ✅/❌
- **Action**: Convert INJURY_PENALTIES from flat to nested structure
- **Before**:
  ```json
  "INJURY_PENALTIES_HIGH": 78.22,
  "INJURY_PENALTIES_MEDIUM": 4.68
  ```
- **After**:
  ```json
  "INJURY_PENALTIES": {
    "LOW": 0,
    "MEDIUM": 4.68,
    "HIGH": 78.22
  }
  ```
- **Status**: ⬜ Not Started
- **Notes**:

### 1.4 Run Phase 1 validation and commit ✅/❌
- **Actions**:
  - Run: `python run_pre_commit_validation.py`
  - Verify exit code 0 (all tests pass)
  - Commit with message: "Add ParameterJsonManager with nested structure support"
- **Status**: ⬜ Not Started
- **Exit Code**:
- **Notes**:

---

## Phase 2: Integrate ParameterJsonManager into Draft Helper

### 2.1 Update DraftHelper constructor ✅/❌
- **File**: `draft_helper/draft_helper.py`
- **Changes**:
  - Add `parameter_json_path` parameter to constructor
  - Initialize ParameterJsonManager
  - Store reference for use throughout class
- **Status**: ⬜ Not Started
- **Notes**:

### 2.2 Update run_draft_helper.py ✅/❌
- **File**: `run_draft_helper.py`
- **Changes**:
  - Default to `shared_files/parameters.json`
  - Pass parameter_json_path to DraftHelper constructor
  - Add error handling for missing file
- **Status**: ⬜ Not Started
- **Notes**:

### 2.3 Replace all parameter references in DraftHelper ✅/❌
- **Files to check**:
  - `draft_helper/draft_helper.py`
  - `draft_helper/core/scoring_engine.py`
  - `draft_helper/core/normalization_calculator.py`
  - `draft_helper/core/draft_order_calculator.py`
  - `draft_helper/core/injury_scorer.py`
  - `draft_helper/core/bye_week_scorer.py`
  - `draft_helper/core/adp_scorer.py`
  - `draft_helper/core/player_rating_scorer.py`
  - `draft_helper/core/team_quality_scorer.py`
  - `draft_helper/core/consistency_scorer.py`
- **Action**: Replace config imports with ParameterJsonManager access
- **Status**: ⬜ Not Started
- **Notes**:

### 2.4 Remove 23 parameters from draft_helper_config.py ✅/❌
- **File**: `shared_files/configs/draft_helper_config.py`
- **Remove**:
  - All ADP multipliers (3)
  - BASE_BYE_PENALTY
  - DRAFT_ORDER_PRIMARY_BONUS, DRAFT_ORDER_SECONDARY_BONUS
  - INJURY_PENALTIES dict (3 values)
  - NORMALIZATION_MAX_SCALE
  - All player rating multipliers (3)
  - All team quality multipliers (3)
  - All consistency multipliers (3)
- **Keep**: All other settings (MAX_POSITIONS, DRAFT_ORDER structure, etc.)
- **Status**: ⬜ Not Started
- **Notes**:

### 2.5 Update draft_helper unit tests ✅/❌
- **Files**: All files in `draft_helper/tests/`
- **Action**: Update tests to use ParameterJsonManager or mock JSON loading
- **Status**: ⬜ Not Started
- **Notes**:

### 2.6 Run Phase 2 validation and commit ✅/❌
- **Actions**:
  - Run: `python run_pre_commit_validation.py`
  - Verify exit code 0 (all tests pass)
  - Test draft_helper interactively
  - Commit with message: "Integrate JSON parameters into draft helper"
- **Status**: ⬜ Not Started
- **Exit Code**:
- **Notes**:

---

## Phase 3: Integrate ParameterJsonManager into Starter Helper

### 3.1 Update StarterHelper/LineupOptimizer constructor ✅/❌
- **Files**:
  - `starter_helper/lineup_optimizer.py`
  - Any other relevant starter helper files
- **Changes**:
  - Add `parameter_json_path` parameter to constructor
  - Initialize ParameterJsonManager
  - Store reference for use throughout class
- **Status**: ⬜ Not Started
- **Notes**:

### 3.2 Update run_starter_helper.py ✅/❌
- **File**: `run_starter_helper.py`
- **Changes**:
  - Default to `shared_files/parameters.json`
  - Pass parameter_json_path to constructor
  - Add error handling for missing file
- **Status**: ⬜ Not Started
- **Notes**:

### 3.3 Replace all parameter references in Starter Helper ✅/❌
- **Files to check**:
  - `starter_helper/lineup_optimizer.py`
  - `starter_helper/matchup_calculator.py`
  - Any other files using the 5 matchup multipliers or 3 consistency multipliers
- **Action**: Replace config imports with ParameterJsonManager access
- **Affected parameters**:
  - MATCHUP_EXCELLENT_MULTIPLIER
  - MATCHUP_GOOD_MULTIPLIER
  - MATCHUP_NEUTRAL_MULTIPLIER
  - MATCHUP_POOR_MULTIPLIER
  - MATCHUP_VERY_POOR_MULTIPLIER
  - CONSISTENCY_LOW_MULTIPLIER
  - CONSISTENCY_MEDIUM_MULTIPLIER
  - CONSISTENCY_HIGH_MULTIPLIER
- **Status**: ⬜ Not Started
- **Notes**:

### 3.4 Remove matchup/consistency parameters from starter_helper_config.py ✅/❌
- **File**: `shared_files/configs/starter_helper_config.py`
- **Remove**: MATCHUP_MULTIPLIERS dict (all 5 multiplier ranges)
- **Keep**: All other settings (STARTING_LINEUP_REQUIREMENTS, etc.)
- **Status**: ⬜ Not Started
- **Notes**:

### 3.5 Update starter_helper unit tests ✅/❌
- **Files**: All files in `starter_helper/tests/`
- **Action**: Update tests to use ParameterJsonManager or mock JSON loading
- **Status**: ⬜ Not Started
- **Notes**:

### 3.6 Ensure draft_helper's starter_helper uses same parameters ✅/❌
- **File**: `draft_helper/draft_helper.py` (or wherever starter helper is instantiated)
- **Action**: Pass the same parameter_json_path to starter helper when called from draft helper
- **Status**: ⬜ Not Started
- **Notes**:

### 3.7 Run Phase 3 validation and commit ✅/❌
- **Actions**:
  - Run: `python run_pre_commit_validation.py`
  - Verify exit code 0 (all tests pass)
  - Test starter_helper interactively
  - Commit with message: "Integrate JSON parameters into starter helper"
- **Status**: ⬜ Not Started
- **Exit Code**:
- **Notes**:

---

## Phase 4: Update Simulation System

### 4.1 Create ParameterCombinationGenerator ✅/❌
- **Location**: `draft_helper/simulation/parameter_combination_generator.py`
- **Purpose**: Read parameter_sets JSON files and generate all combinations
- **Requirements**:
  - Read files from `draft_helper/simulation/parameters/parameter_sets/`
  - Generate all combinations of parameter arrays
  - Save to `draft_helper/simulation/parameters/parameter_runs/`
  - Naming: `{parameter_set_name}_0.json`, `{parameter_set_name}_1.json`, etc.
  - Support nested INJURY_PENALTIES structure
- **Status**: ⬜ Not Started
- **Notes**:

### 4.2 Create unit tests for ParameterCombinationGenerator ✅/❌
- **Location**: `draft_helper/simulation/tests/test_parameter_combination_generator.py`
- **Test Coverage**:
  - Load parameter_sets files
  - Generate correct number of combinations
  - Output files have correct format
  - Nested structure preserved
  - File naming convention correct
- **Status**: ⬜ Not Started
- **Notes**:

### 4.3 Update simulation to use parameter_runs files ✅/❌
- **Files**:
  - `draft_helper/simulation/simulation_engine.py` (or main simulation file)
  - `run_simulation.py`
- **Changes**:
  - Remove ParameterInjector usage
  - Generate parameter_runs files upfront from parameter_sets
  - Loop through parameter_runs files
  - Pass each JSON file path to DraftHelper and StarterHelper
  - Update result files to include parameter JSON filename
- **Status**: ⬜ Not Started
- **Notes**:

### 4.4 Remove ParameterInjector class ✅/❌
- **Files to delete/modify**:
  - `draft_helper/simulation/parameter_injector.py` (delete if exists)
  - Any test files for ParameterInjector (delete)
- **Status**: ⬜ Not Started
- **Notes**:

### 4.5 Update simulation unit tests ✅/❌
- **Files**: All simulation test files
- **Action**: Remove ParameterInjector tests, add ParameterCombinationGenerator tests
- **Status**: ⬜ Not Started
- **Notes**:

### 4.6 Create test parameter_sets file for integration testing ✅/❌
- **Location**: `draft_helper/simulation/parameters/parameter_sets/test_set.json`
- **Purpose**: Small test file with 2-3 values per parameter for testing
- **Action**: Create dummy file that won't be changed
- **Status**: ⬜ Not Started
- **Notes**:

### 4.7 Run Phase 4 validation and commit ✅/❌
- **Actions**:
  - Run: `python run_pre_commit_validation.py`
  - Verify exit code 0 (all tests pass)
  - Test simulation with small parameter set
  - Commit with message: "Replace ParameterInjector with combination generator"
- **Status**: ⬜ Not Started
- **Exit Code**:
- **Notes**:

---

## Phase 5: Comprehensive Testing and Verification

### 5.1 Systematic parameter verification ✅/❌
- **Action**: Go through each of the 23 parameters systematically
- **Verify**:
  - Parameter is loaded correctly from JSON
  - Parameter is accessed correctly in all locations
  - Parameter produces expected behavior (spot check calculations)
  - No hardcoded values remain
- **Checklist**:
  - [ ] ADP_EXCELLENT_MULTIPLIER
  - [ ] ADP_GOOD_MULTIPLIER
  - [ ] ADP_POOR_MULTIPLIER
  - [ ] BASE_BYE_PENALTY
  - [ ] DRAFT_ORDER_PRIMARY_BONUS
  - [ ] DRAFT_ORDER_SECONDARY_BONUS
  - [ ] INJURY_PENALTIES.LOW
  - [ ] INJURY_PENALTIES.MEDIUM
  - [ ] INJURY_PENALTIES.HIGH
  - [ ] MATCHUP_EXCELLENT_MULTIPLIER
  - [ ] MATCHUP_GOOD_MULTIPLIER
  - [ ] MATCHUP_NEUTRAL_MULTIPLIER
  - [ ] MATCHUP_POOR_MULTIPLIER
  - [ ] MATCHUP_VERY_POOR_MULTIPLIER
  - [ ] NORMALIZATION_MAX_SCALE
  - [ ] PLAYER_RATING_EXCELLENT_MULTIPLIER
  - [ ] PLAYER_RATING_GOOD_MULTIPLIER
  - [ ] PLAYER_RATING_POOR_MULTIPLIER
  - [ ] TEAM_EXCELLENT_MULTIPLIER
  - [ ] TEAM_GOOD_MULTIPLIER
  - [ ] TEAM_POOR_MULTIPLIER
  - [ ] CONSISTENCY_LOW_MULTIPLIER
  - [ ] CONSISTENCY_MEDIUM_MULTIPLIER
  - [ ] CONSISTENCY_HIGH_MULTIPLIER
- **Status**: ⬜ Not Started
- **Notes**:

### 5.2 Add integration tests with different parameter files ✅/❌
- **Action**: Add tests to interactive integration suite
- **Requirements**:
  - Create 2-3 dummy parameter JSON files for testing
  - Test loading different files
  - Verify parameter values are used
  - Keep dummy files in test directory (won't be changed)
- **Status**: ⬜ Not Started
- **Notes**:

### 5.3 Run complete test suite ✅/❌
- **Actions**:
  - Run: `python run_pre_commit_validation.py`
  - Verify 100% pass rate (577+ tests)
  - All unit tests pass
  - All startup tests pass
  - All interactive integration tests pass
- **Status**: ⬜ Not Started
- **Exit Code**:
- **Test Count**:
- **Notes**:

### 5.4 Manual integration testing ✅/❌
- **Test Scenarios**:
  - [ ] Draft helper loads and runs with default parameters.json
  - [ ] Starter helper loads and runs with default parameters.json
  - [ ] Draft helper's starter helper uses same parameters
  - [ ] Simulation generates parameter_runs files correctly
  - [ ] Simulation runs with generated parameter files
  - [ ] Error handling for missing/malformed JSON files
  - [ ] All 8 draft helper menu options work correctly
  - [ ] Point calculations match expected behavior
- **Status**: ⬜ Not Started
- **Notes**:

### 5.5 Run Phase 5 validation and commit ✅/❌
- **Actions**:
  - Run: `python run_pre_commit_validation.py`
  - Verify exit code 0
  - Commit with message: "Add comprehensive parameter verification and tests"
- **Status**: ⬜ Not Started
- **Exit Code**:
- **Notes**:

---

## Phase 6: Documentation and Finalization

### 6.1 Create parameters folder README ✅/❌
- **Location**: `shared_files/parameters/README.md`
- **Content**:
  - Description of each of the 23 parameters
  - Valid ranges and types
  - How parameters affect scoring
  - Example parameter files
  - How to create custom parameter files
  - Nested INJURY_PENALTIES structure explanation
- **Status**: ⬜ Not Started
- **Notes**:

### 6.2 Update CLAUDE.md ✅/❌
- **File**: `CLAUDE.md`
- **Updates**:
  - Document JSON parameter system
  - Update configuration section
  - Add parameter JSON workflow
  - Document default parameter locations
  - Update simulation workflow with parameter_sets and parameter_runs
  - Remove references to old config parameters
- **Status**: ⬜ Not Started
- **Notes**:

### 6.3 Update module README files ✅/❌
- **Files**:
  - `draft_helper/README.md`
  - `starter_helper/README.md`
  - `draft_helper/simulation/README.md`
- **Action**: Update to reflect JSON parameter system
- **Status**: ⬜ Not Started
- **Notes**:

### 6.4 Update config file documentation ✅/❌
- **Files**:
  - `shared_files/configs/draft_helper_config.py`
  - `shared_files/configs/starter_helper_config.py`
- **Action**: Update Quick Configuration Guide sections to reflect removed parameters
- **Status**: ⬜ Not Started
- **Notes**:

### 6.5 Run final validation and commit ✅/❌
- **Actions**:
  - Run: `python run_pre_commit_validation.py`
  - Verify exit code 0
  - Verify all documentation is accurate
  - Commit with message: "Complete JSON parameter system documentation"
- **Status**: ⬜ Not Started
- **Exit Code**:
- **Notes**:

---

## Phase 7: Move to Done

### 7.1 Final verification checklist ✅/❌
- **Verify**:
  - [ ] All 23 parameters moved to JSON
  - [ ] No hardcoded parameter values remain
  - [ ] All tests pass (100%)
  - [ ] Draft helper works with JSON parameters
  - [ ] Starter helper works with JSON parameters
  - [ ] Simulation uses parameter_runs system
  - [ ] Documentation updated
  - [ ] Integration tests pass
  - [ ] Error handling works correctly
- **Status**: ⬜ Not Started
- **Notes**:

### 7.2 Move files to done folder ✅/❌
- **Actions**:
  - Move `potential_updates/config_as_json.txt` to `potential_updates/done/`
  - Delete `potential_updates/config_as_json_questions.md`
  - Keep this TODO file for reference
- **Status**: ⬜ Not Started
- **Notes**:

---

## Important Reminders

1. **Run pre-commit validation after EVERY phase** using `python run_pre_commit_validation.py`
2. **Update this TODO file** with status (✅/❌) and notes after each step
3. **Do not skip any steps** - each phase leaves the repo in a testable state
4. **100% test pass rate required** before moving to next phase
5. **Commit after each phase** with clear, descriptive messages
6. **No emojis in commit messages**
7. **Test interactively** in addition to automated tests
8. **Systematic parameter verification** - check each of the 23 parameters individually

---

## Progress Tracking

**Current Phase**: Phase 1
**Current Step**: 1.1
**Overall Status**: Not Started
**Last Updated**: 2025-10-06
**Last Validation Exit Code**: N/A
**Total Test Count**: 577 (baseline)

---

## Notes and Issues

*(Add any issues, blockers, or important observations here as you progress)*
