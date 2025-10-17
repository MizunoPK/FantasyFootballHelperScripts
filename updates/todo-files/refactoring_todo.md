# Refactoring Project - TODO Tracking

**Objective**: Comprehensive codebase refactoring including testing, documentation, structure improvements, and code quality enhancements.

**Scope**: All 80 Python files across the entire project
**Approach**: Testing first, then documentation, then cleanup/quality
**Phasing**: Directory-by-directory with commits after each

---

## TODO File Maintenance

**IMPORTANT**: Keep this file updated as you complete tasks. Mark tasks with:
- `[ ]` - Not started
- `[IN PROGRESS]` - Currently working on
- `[DONE]` - Completed

Update progress notes after each session in case a new Claude agent needs to continue the work.

---

## ITERATION 1: Initial TODO Creation

### High-Level Task Breakdown

Based on refactoring.txt requirements:
1. ✅ Add comprehensive unit tests for every function (edge cases)
2. ✅ Add comprehensive code comments, function/class descriptions
3. ✅ Reorganize files for readability
4. ✅ Improve modularity (break up large files if needed)
5. ✅ Eliminate duplicate code
6. ✅ Remove unused variables/functions/classes
7. ✅ Update README and CLAUDE documentation
8. ✅ Improve logging (DEBUG for spam, INFO for important)
9. ✅ Identify code quality improvements
10. ✅ Author attribution (Kai Mizuno) in all files
11. ✅ Remove all date references from docstrings

### Directory Structure (80 files to refactor)

```
league_helper/              (17 files)
├── util/                  (10 files)
├── add_to_roster_mode/     (1 file)
├── starter_helper_mode/    (1 file)
├── trade_simulator_mode/   (3 files)
└── modify_player_data_mode/ (2 files)

utils/                      (7 files)

player-data-fetcher/        (7 files)
nfl-scores-fetcher/         (7 files)
simulation/                 (11 files)

tests/                      (13 test modules - enhance/add)
Root scripts/               (4 files)
Documentation/              (README, CLAUDE.md, new ARCHITECTURE.md)
```

### Testing Requirements Summary

**Files WITHOUT Tests (CRITICAL)**:
- AddToRosterModeManager.py - NO TESTS
- FantasyTeam.py - NO TESTS (748 lines, fundamental)
- TeamDataManager.py - NO TESTS
- user_input.py - NO TESTS
- data_file_manager.py - NO TESTS
- DraftedRosterManager.py - NO TESTS
- LoggingManager.py - NO TESTS
- TeamData.py - NO TESTS
- **All player-data-fetcher files** - NO TESTS
- **All nfl-scores-fetcher files** - NO TESTS

**Files WITH Tests (Enhance)**:
- ConfigManager (26 tests) - add edge cases
- PlayerManager (62 tests) - add edge cases
- StarterHelper (24 tests) - review
- TradeSimulator (80 tests) - review
- ModifyPlayerData (20 tests) - review
- Simulation (41 tests) - review

**Integration Tests**: Create new comprehensive integration test suite

### Documentation Requirements Summary

**Author Attribution**: Add "Author: Kai Mizuno" to 65 files missing it
**Date Removal**: Remove dates from 15 files
**Comment Density**: Heavy - document nearly all functions
**Docstring Format**: Google style, standardized

---

## PHASE 1: LEAGUE HELPER UTILS (Foundation)

**Directory**: `league_helper/util/` (10 files, 2800+ lines)
**Why first**: Foundation for all modes

### Testing Tasks

#### [ ] 1.1: Create comprehensive tests for FantasyTeam.py
**File**: `tests/league_helper/util/test_FantasyTeam.py`
**Priority**: CRITICAL - 748 lines, no direct tests
**Estimated tests**: 50-100 tests
**Coverage areas**:
- Initialization and roster loading
- `can_draft()` - all edge cases (position limits, FLEX logic, roster full)
- `draft_player()` - success and failure cases
- `remove_player()` - success and failure cases
- `replace_player()` - same position, FLEX eligible swaps, invalid swaps
- `_assign_player_to_slot()` - all slot assignment scenarios
- `flex_eligible()` - RB/WR/other position checks
- Slot assignment tracking (`slot_assignments` dict)
- Position count tracking (`pos_counts` dict)
- Bye week tracking (`bye_week_counts` dict)
- Draft order tracking
- `get_matching_byes_in_roster()` - various bye week scenarios
- `validate_roster_integrity()` - detect all error conditions
- `get_slot_assignment()` - player slot lookups
- `optimize_flex_assignments()` - FLEX optimization logic
- `get_optimal_slot_for_player()` - slot determination
- Edge cases: Invalid positions, roster limits, FLEX boundary conditions

#### [ ] 1.2: Create comprehensive tests for TeamDataManager.py
**File**: `tests/league_helper/util/test_TeamDataManager.py`
**Priority**: HIGH - 210 lines, no direct tests
**Estimated tests**: 20-30 tests
**Coverage areas**:
- Initialization and CSV loading
- `get_team_offensive_rank()` - valid/invalid teams
- `get_team_defensive_rank()` - valid/invalid teams
- `get_team_opponent()` - valid/invalid teams
- `get_rank_difference()` - offensive and defensive players
- `is_matchup_available()` - various data states
- `reload_team_data()` - reload functionality
- Edge cases: Missing teams.csv, corrupt data, missing opponents

#### [ ] 1.3: Create tests for user_input.py
**File**: `tests/league_helper/util/test_user_input.py`
**Priority**: MEDIUM - 19 lines, simple but untested
**Estimated tests**: 5-10 tests
**Coverage areas**:
- `show_list_selection()` - valid selections, invalid input, quit option
- Mock user input scenarios
- Edge cases: Empty lists, invalid indices

#### [ ] 1.4: Enhance existing PlayerManager tests
**File**: `tests/league_helper/util/test_PlayerManager_scoring.py`
**Current**: 62 tests
**Action**: Add edge case tests for:
- Scoring with missing data (None values)
- Boundary conditions for thresholds
- Extreme values (very high/low scores)
- CSV loading edge cases
- Roster operations edge cases
**Estimated additional tests**: 15-20 tests

#### [ ] 1.5: Enhance existing ConfigManager tests
**File**: `tests/league_helper/util/test_ConfigManager_thresholds.py`
**Current**: 26 tests
**Action**: Add edge case tests for:
- Invalid JSON structure
- Missing required fields
- Boundary threshold values
- Invalid data types
**Estimated additional tests**: 10-15 tests

#### [ ] 1.6: Review and enhance DraftedDataWriter tests
**File**: `tests/league_helper/util/test_DraftedDataWriter.py`
**Current**: 24 tests
**Action**: Review coverage, add edge cases if needed
**Estimated additional tests**: 5-10 tests

#### [ ] 1.7: Review and enhance ProjectedPointsManager tests
**File**: `tests/league_helper/util/test_ProjectedPointsManager.py`
**Current**: 13 tests
**Action**: Review coverage, add edge cases if needed
**Estimated additional tests**: 5-10 tests

#### [ ] 1.8: Review and enhance ScoredPlayer tests
**File**: `tests/league_helper/util/test_ScoredPlayer.py`
**Current**: 17 tests
**Action**: Review coverage, add edge cases if needed
**Estimated additional tests**: 3-5 tests

#### [ ] 1.9: Review and enhance player_search tests
**File**: `tests/league_helper/util/test_player_search.py`
**Current**: 33 tests
**Action**: Review coverage, add edge cases if needed
**Estimated additional tests**: 5-10 tests

### Documentation Tasks

#### [ ] 1.10: Add author attribution to all util files
**Files**: All 10 files in `league_helper/util/`
**Action**: Add "Author: Kai Mizuno" to file-level docstring where missing
**Files to update**: Check each file, add if missing

#### [ ] 1.11: Remove date references
**Files**: Check all util files for "Last Updated" or date stamps
**Action**: Remove all date references

#### [ ] 1.12: Add heavy inline comments to FantasyTeam.py
**File**: `league_helper/util/FantasyTeam.py` (748 lines)
**Action**: Document nearly every method with inline comments
**Focus**: Complex slot logic, FLEX assignments, validation

#### [ ] 1.13: Add heavy inline comments to PlayerManager.py
**File**: `league_helper/util/PlayerManager.py` (890 lines)
**Action**: Document scoring logic, roster operations
**Focus**: 9-step scoring algorithm, CSV operations

#### [ ] 1.14: Add heavy inline comments to ConfigManager.py
**File**: `league_helper/util/ConfigManager.py` (686 lines)
**Action**: Document threshold logic, configuration validation
**Focus**: Multiplier calculations, JSON structure

#### [ ] 1.15: Add/enhance comments for remaining util files
**Files**: TeamDataManager, DraftedDataWriter, ProjectedPointsManager, ScoredPlayer, player_search, user_input
**Action**: Add comprehensive inline comments

#### [ ] 1.16: Standardize all docstrings to Google style
**Files**: All util files
**Action**: Ensure consistent format, add examples where helpful

### Code Organization Tasks

#### [ ] 1.17: Reorganize FantasyTeam.py methods
**File**: `league_helper/util/FantasyTeam.py`
**Action**: Group methods by functionality
- Public draft operations
- Public roster queries
- Public validation methods
- Private slot management
- Private validation helpers
**Note**: Keep as single file (don't split)

#### [ ] 1.18: Reorganize PlayerManager.py methods
**File**: `league_helper/util/PlayerManager.py`
**Action**: Group methods by functionality
- Public scoring methods
- Public roster operations
- Public data loading
- Private scoring helpers
- Private validation helpers
**Note**: Keep as single file (don't split)

#### [ ] 1.19: Reorganize ConfigManager.py methods
**File**: `league_helper/util/ConfigManager.py`
**Action**: Group methods by functionality
- Public configuration access
- Public multiplier getters
- Private loading and validation
**Note**: Keep as single file (don't split)

### Code Quality Tasks

#### [ ] 1.20: Scan for duplicate code in util directory
**Action**: Identify repeated patterns (5+ identical lines appearing 2+ times)
**Extract to**: Shared utility methods if appropriate

#### [ ] 1.21: Remove unused imports in util files
**Action**: Scan all util files, remove unused imports

#### [ ] 1.22: Remove unused functions/variables in util files
**Action**: Identify unreferenced code, document in code_changes.md, remove

#### [ ] 1.23: Improve logging in util files
**Action**: Add logging where missing, adjust levels (DEBUG/INFO/WARNING/ERROR)
**Focus**: FantasyTeam operations, PlayerManager scoring, ConfigManager loading

### Validation Tasks

#### [ ] 1.24: Run full test suite after util refactoring
**Command**: `python tests/run_all_tests.py`
**Requirement**: 100% pass rate

#### [ ] 1.25: Create code_changes.md entry for util/ refactoring
**File**: `updates/refactoring_code_changes.md`
**Action**: Document all changes made to util directory

#### [ ] 1.26: COMMIT - League Helper Utils Complete
**Pre-commit checklist**:
- All tests pass (100%)
- All files have author attribution
- All dates removed
- All comments added
- Code organized
- Duplicates removed
- Unused code removed
- Logging improved
**Commit message**: "Refactor league_helper/util - tests, docs, cleanup"

---

## PHASE 2: ADD TO ROSTER MODE

**Directory**: `league_helper/add_to_roster_mode/` (1 file)
**Why second**: First mode to refactor, currently NO TESTS

### Testing Tasks

#### [ ] 2.1: Create comprehensive tests for AddToRosterModeManager.py
**File**: `tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py` (NEW)
**Priority**: CRITICAL - 242 lines, NO TESTS
**Estimated tests**: 30-40 tests
**Coverage areas**:
- Initialization
- `start_interactive_mode()` - mocked user interactions
- `get_recommendations()` - scoring with draft_round bonus
- `_display_roster_by_draft_rounds()` - output validation
- `_match_players_to_rounds()` - round assignment logic
- `_get_current_round()` - round calculation
- Draft player flow - success and failure cases
- Roster full scenarios
- No available players scenarios
- Edge cases: Empty roster, full roster, FLEX assignments

### Documentation Tasks

#### [ ] 2.2: Add author attribution
**File**: `league_helper/add_to_roster_mode/AddToRosterModeManager.py`
**Action**: Verify "Author: Kai Mizuno" present

#### [ ] 2.3: Remove date references
**Action**: Check for and remove any date stamps

#### [ ] 2.4: Add heavy inline comments
**File**: `AddToRosterModeManager.py`
**Action**: Document all methods with inline comments
**Focus**: Draft recommendation logic, round matching, user interaction flow

#### [ ] 2.5: Standardize docstrings
**Action**: Ensure Google style format throughout

### Code Organization Tasks

#### [ ] 2.6: Reorganize methods by functionality
**Action**: Group public interface, recommendations, display, private helpers

### Code Quality Tasks

#### [ ] 2.7: Check for duplicate code
**Action**: Compare with other mode managers, extract common patterns

#### [ ] 2.8: Remove unused imports/variables
**Action**: Clean up unused code

#### [ ] 2.9: Improve logging
**Action**: Add comprehensive logging for draft operations

### Validation Tasks

#### [ ] 2.10: Run full test suite
**Command**: `python tests/run_all_tests.py`
**Requirement**: 100% pass rate

#### [ ] 2.11: Update code_changes.md
**Action**: Document AddToRoster refactoring

#### [ ] 2.12: COMMIT - Add to Roster Mode Complete
**Commit message**: "Refactor add_to_roster_mode - tests, docs, cleanup"

---

## PHASE 3: STARTER HELPER MODE

**Directory**: `league_helper/starter_helper_mode/` (1 file)
**Tests**: 24 existing tests - review and enhance

### Testing Tasks

#### [ ] 3.1: Review and enhance StarterHelperModeManager tests
**File**: `tests/league_helper/starter_helper_mode/test_StarterHelperModeManager.py`
**Current**: 24 tests
**Action**: Add edge case tests for:
- Optimal lineup generation with various roster compositions
- FLEX optimization scenarios
- Injury filtering edge cases
- Week-specific scoring edge cases
- Empty roster scenarios
**Estimated additional tests**: 10-15 tests

### Documentation Tasks

#### [ ] 3.2: Add author attribution
**File**: `league_helper/starter_helper_mode/StarterHelperModeManager.py`
**Action**: Verify/add "Author: Kai Mizuno"

#### [ ] 3.3: Remove date references
**Action**: Check and remove dates

#### [ ] 3.4: Add heavy inline comments
**Action**: Document all methods with inline comments
**Focus**: Lineup optimization, FLEX logic, injury filtering

#### [ ] 3.5: Standardize docstrings
**Action**: Ensure Google style

### Code Organization Tasks

#### [ ] 3.6: Reorganize methods by functionality
**Action**: Group public interface, lineup generation, optimization, display helpers

### Code Quality Tasks

#### [ ] 3.7: Check for duplicate code
**Action**: Compare with other modes

#### [ ] 3.8: Remove unused code
**Action**: Clean up

#### [ ] 3.9: Improve logging
**Action**: Add logging for lineup decisions

### Validation Tasks

#### [ ] 3.10: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 3.11: Update code_changes.md
**Action**: Document StarterHelper refactoring

#### [ ] 3.12: COMMIT - Starter Helper Mode Complete
**Commit message**: "Refactor starter_helper_mode - tests, docs, cleanup"

---

## PHASE 4: TRADE SIMULATOR MODE

**Directory**: `league_helper/trade_simulator_mode/` (3 files: TradeSimulatorModeManager, TradeSimTeam, TradeSnapshot)
**Tests**: 80 existing tests - review and enhance
**Note**: TradeSimulatorModeManager is 1068 lines - consider breaking up

### Testing Tasks

#### [ ] 4.1: Review and enhance TradeSimulator tests
**Files**: `test_trade_simulator.py` (41 tests), `test_manual_trade_visualizer.py` (39 tests)
**Current**: 80 tests total
**Action**: Add edge case tests for:
- Complex multi-player trades
- Trade validation edge cases
- Roster limit scenarios
- Score calculation edge cases
- Visualization edge cases
**Estimated additional tests**: 15-20 tests

### Documentation Tasks

#### [ ] 4.2: Add author attribution to all 3 files
**Files**: TradeSimulatorModeManager, TradeSimTeam, TradeSnapshot
**Action**: Verify/add "Author: Kai Mizuno"

#### [ ] 4.3: Remove date references
**Action**: Check all 3 files

#### [ ] 4.4: Add heavy inline comments to TradeSimulatorModeManager
**File**: `TradeSimulatorModeManager.py` (1068 lines)
**Action**: Document nearly all methods
**Focus**: Trade logic, visualization, scoring

#### [ ] 4.5: Add comments to TradeSimTeam and TradeSnapshot
**Action**: Document helper classes

#### [ ] 4.6: Standardize docstrings
**Action**: All 3 files, Google style

### Code Organization Tasks

#### [ ] 4.7: Consider breaking up TradeSimulatorModeManager
**File**: `TradeSimulatorModeManager.py` (1068 lines)
**Decision point**: Evaluate if breaking into visualization.py + core logic improves clarity
**Action**: If beneficial, split into:
- `TradeSimulatorModeManager.py` (core logic)
- `trade_visualization.py` (display/formatting helpers)
**Otherwise**: Reorganize methods within single file

#### [ ] 4.8: Reorganize methods by functionality
**Action**: Group public interface, trade operations, scoring, visualization

### Code Quality Tasks

#### [ ] 4.9: Check for duplicate code
**Action**: Identify repeated patterns in trade logic

#### [ ] 4.10: Remove unused code
**Action**: Clean up

#### [ ] 4.11: Improve logging
**Action**: Add logging for trade operations

### Validation Tasks

#### [ ] 4.12: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 4.13: Update code_changes.md
**Action**: Document TradeSimulator refactoring

#### [ ] 4.14: COMMIT - Trade Simulator Mode Complete
**Commit message**: "Refactor trade_simulator_mode - tests, docs, cleanup"

---

## PHASE 5: MODIFY PLAYER DATA MODE

**Directory**: `league_helper/modify_player_data_mode/` (2 files: ModifyPlayerDataModeManager, __init__)
**Tests**: 20 existing tests - review and enhance

### Testing Tasks

#### [ ] 5.1: Review and enhance ModifyPlayerData tests
**File**: `tests/league_helper/modify_player_data_mode/test_modify_player_data_mode.py`
**Current**: 20 tests
**Action**: Add edge case tests for:
- Invalid player selections
- Invalid data modifications
- Boundary value modifications
- CSV update failures
**Estimated additional tests**: 10-15 tests

### Documentation Tasks

#### [ ] 5.2: Add author attribution
**File**: `ModifyPlayerDataModeManager.py`
**Action**: Verify/add "Author: Kai Mizuno"

#### [ ] 5.3: Remove date references
**Action**: Check and remove

#### [ ] 5.4: Add heavy inline comments
**Action**: Document all methods

#### [ ] 5.5: Standardize docstrings
**Action**: Google style

### Code Organization Tasks

#### [ ] 5.6: Reorganize methods by functionality
**Action**: Group by operation type

### Code Quality Tasks

#### [ ] 5.7: Check for duplicate code
**Action**: Compare with other modes

#### [ ] 5.8: Remove unused code
**Action**: Clean up

#### [ ] 5.9: Improve logging
**Action**: Add logging for data modifications

### Validation Tasks

#### [ ] 5.10: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 5.11: Update code_changes.md
**Action**: Document ModifyPlayerData refactoring

#### [ ] 5.12: COMMIT - Modify Player Data Mode Complete
**Commit message**: "Refactor modify_player_data_mode - tests, docs, cleanup"

---

## PHASE 6: LEAGUE HELPER CORE

**Files**: `league_helper/LeagueHelperManager.py`, `league_helper/constants.py`, `league_helper/__init__.py`

### Testing Tasks

#### [ ] 6.1: Create tests for LeagueHelperManager
**File**: `tests/league_helper/test_LeagueHelperManager.py` (NEW)
**Estimated tests**: 15-20 tests
**Coverage areas**:
- Initialization
- Manager coordination
- Menu display
- Mode routing
- Data reload between menu displays
- Edge cases: Missing data files, invalid configurations

#### [ ] 6.2: Create tests for constants.py
**File**: `tests/league_helper/test_constants.py` (NEW)
**Estimated tests**: 5-10 tests
**Coverage**: Validate all constants are defined correctly

### Documentation Tasks

#### [ ] 6.3: Add author attribution
**Files**: LeagueHelperManager, constants
**Action**: Verify/add

#### [ ] 6.4: Remove date references
**Action**: Check and remove

#### [ ] 6.5: Add heavy inline comments
**Action**: Document all methods in LeagueHelperManager

#### [ ] 6.6: Standardize docstrings
**Action**: Google style

### Code Quality Tasks

#### [ ] 6.7: Check for duplicate code
**Action**: Review initialization patterns

#### [ ] 6.8: Remove unused code
**Action**: Clean up

#### [ ] 6.9: Improve logging
**Action**: Add logging for application lifecycle

### Validation Tasks

#### [ ] 6.10: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 6.11: Update code_changes.md
**Action**: Document core refactoring

#### [ ] 6.12: COMMIT - League Helper Core Complete
**Commit message**: "Refactor league_helper core - tests, docs, cleanup"

---

## PHASE 7: SHARED UTILS

**Directory**: `utils/` (7 files: csv_utils, data_file_manager, DraftedRosterManager, error_handler, FantasyPlayer, LoggingManager, TeamData)
**Tests**: Only FantasyPlayer has tests (4 tests) - need comprehensive tests for all

### Testing Tasks

#### [ ] 7.1: Review and enhance FantasyPlayer tests
**File**: `tests/utils/test_FantasyPlayer.py`
**Current**: 4 tests
**Action**: Add comprehensive tests for:
- All field initialization
- `from_dict()` factory method
- `is_available()` method
- All property getters
- String representation
- Edge cases: Missing data, invalid data types
**Estimated additional tests**: 20-25 tests

#### [ ] 7.2: Create comprehensive tests for csv_utils.py
**File**: `tests/utils/test_csv_utils.py` (NEW)
**Priority**: HIGH - 357 lines, heavily used, NO TESTS
**Estimated tests**: 30-40 tests
**Coverage areas**:
- `validate_csv_columns()` - valid/invalid columns
- `read_csv_with_validation()` - various CSV formats
- `write_csv_with_backup()` - backup creation
- `write_csv_async()` - async operations
- `read_dict_csv()` - dictionary format
- `write_dict_csv()` - dictionary writing
- `merge_csv_files()` - merging operations
- `safe_csv_read()` - error handling
- `csv_column_exists()` - column checking
- Edge cases: Missing files, corrupt CSV, encoding issues, empty files

#### [ ] 7.3: Create comprehensive tests for data_file_manager.py
**File**: `tests/utils/test_data_file_manager.py` (NEW)
**Priority**: HIGH - 529 lines, NO TESTS
**Estimated tests**: 40-50 tests
**Coverage areas**:
- All file loading methods
- All file writing methods
- Path resolution
- Error handling for missing/corrupt files
- Edge cases

#### [ ] 7.4: Create comprehensive tests for DraftedRosterManager.py
**File**: `tests/utils/test_DraftedRosterManager.py` (NEW)
**Priority**: HIGH - 562 lines, NO TESTS
**Estimated tests**: 30-40 tests
**Coverage areas**:
- Roster loading from CSV
- Player drafted status management
- Roster queries
- CSV updates
- Edge cases

#### [ ] 7.5: Create comprehensive tests for error_handler.py
**File**: `tests/utils/test_error_handler.py` (NEW)
**Priority**: MEDIUM - 581 lines, NO TESTS
**Estimated tests**: 25-35 tests
**Coverage areas**:
- Custom exception classes
- Error context managers
- Error decorators
- Error handling functions
- Edge cases: Nested errors, missing context

#### [ ] 7.6: Create comprehensive tests for LoggingManager.py
**File**: `tests/utils/test_LoggingManager.py` (NEW)
**Priority**: MEDIUM - 162 lines, NO TESTS
**Estimated tests**: 15-20 tests
**Coverage areas**:
- Logger setup
- Logger retrieval
- Log level configuration
- File logging
- Edge cases: Invalid configurations

#### [ ] 7.7: Create comprehensive tests for TeamData.py
**File**: `tests/utils/test_TeamData.py` (NEW)
**Priority**: MEDIUM - 250 lines, NO TESTS
**Estimated tests**: 20-25 tests
**Coverage areas**:
- TeamData class initialization
- `load_teams_from_csv()` function
- Field access and validation
- Edge cases: Missing fields, invalid data

### Documentation Tasks

#### [ ] 7.8: Add author attribution to all utils files
**Files**: All 7 utils files
**Action**: Verify/add "Author: Kai Mizuno"

#### [ ] 7.9: Remove date references
**Files**: csv_utils has "Last Updated: September 2025" - remove
**Action**: Check all 7 files

#### [ ] 7.10: Add heavy inline comments to csv_utils.py
**File**: `utils/csv_utils.py` (357 lines)
**Action**: Already well-commented, enhance where needed

#### [ ] 7.11: Add heavy inline comments to data_file_manager.py
**File**: `utils/data_file_manager.py` (529 lines)
**Action**: Document all file operations

#### [ ] 7.12: Add heavy inline comments to DraftedRosterManager.py
**File**: `utils/DraftedRosterManager.py` (562 lines)
**Action**: Document roster management logic

#### [ ] 7.13: Add heavy inline comments to error_handler.py
**File**: `utils/error_handler.py` (581 lines)
**Action**: Document error handling patterns

#### [ ] 7.14: Add comments to remaining utils files
**Files**: FantasyPlayer, LoggingManager, TeamData
**Action**: Add comprehensive comments

#### [ ] 7.15: Standardize all docstrings to Google style
**Files**: All utils files

### Code Organization Tasks

#### [ ] 7.16: Reorganize large utils files
**Files**: data_file_manager, DraftedRosterManager, error_handler
**Action**: Group methods by functionality within files

### Code Quality Tasks

#### [ ] 7.17: Check for duplicate code in utils
**Action**: Identify repeated patterns across utils

#### [ ] 7.18: Remove unused imports/code
**Action**: Clean up all utils files

#### [ ] 7.19: Improve logging in utils
**Action**: Add appropriate logging

### Validation Tasks

#### [ ] 7.20: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 7.21: Update code_changes.md
**Action**: Document utils refactoring

#### [ ] 7.22: COMMIT - Shared Utils Complete
**Commit message**: "Refactor utils - tests, docs, cleanup"

---

## PHASE 8: PLAYER DATA FETCHER

**Directory**: `player-data-fetcher/` (7 files: config, espn_client, fantasy_points_calculator, player_data_constants, player_data_exporter, player_data_fetcher_main, player_data_models, progress_tracker)
**Tests**: NONE - need basic smoke tests
**Note**: espn_client is 1009 lines

### Testing Tasks

#### [ ] 8.1: Create basic smoke tests for player_data_fetcher_main
**File**: `tests/player_data_fetcher/test_player_data_fetcher_main.py` (NEW)
**Priority**: BASIC smoke tests only
**Estimated tests**: 10-15 tests
**Coverage**: Basic initialization, configuration loading, error handling

#### [ ] 8.2: Create basic tests for espn_client
**File**: `tests/player_data_fetcher/test_espn_client.py` (NEW)
**Priority**: BASIC smoke tests (mock httpx)
**Estimated tests**: 15-20 tests
**Coverage**: Client initialization, basic API call mocking, error handling

#### [ ] 8.3: Create basic tests for fantasy_points_calculator
**File**: `tests/player_data_fetcher/test_fantasy_points_calculator.py` (NEW)
**Estimated tests**: 10-15 tests
**Coverage**: Scoring calculations for different positions

#### [ ] 8.4: Create basic tests for player_data_exporter
**File**: `tests/player_data_fetcher/test_player_data_exporter.py` (NEW)
**Estimated tests**: 10-15 tests
**Coverage**: Export to CSV/JSON/Excel

#### [ ] 8.5: Create basic tests for player_data_models
**File**: `tests/player_data_fetcher/test_player_data_models.py` (NEW)
**Estimated tests**: 10-15 tests
**Coverage**: Model initialization and validation

#### [ ] 8.6: Create basic tests for progress_tracker
**File**: `tests/player_data_fetcher/test_progress_tracker.py` (NEW)
**Estimated tests**: 5-10 tests
**Coverage**: Progress tracking operations

#### [ ] 8.7: Create basic tests for config
**File**: `tests/player_data_fetcher/test_config.py` (NEW)
**Estimated tests**: 5-10 tests
**Coverage**: Configuration loading and validation

### Documentation Tasks

#### [ ] 8.8: Add author attribution to all fetcher files
**Files**: All 7 player-data-fetcher files
**Action**: Verify/add "Author: Kai Mizuno"
**Note**: espn_client already has it

#### [ ] 8.9: Remove date references
**Files**: espn_client has "Last Updated: September 2025" - remove

#### [ ] 8.10: Add heavy inline comments to espn_client
**File**: `player-data-fetcher/espn_client.py` (1009 lines)
**Action**: Document API interaction logic

#### [ ] 8.11: Add comments to remaining fetcher files
**Action**: Document all files comprehensively

#### [ ] 8.12: Standardize docstrings
**Action**: Google style for all files

### Code Organization Tasks

#### [ ] 8.13: Consider breaking up espn_client.py
**File**: `espn_client.py` (1009 lines)
**Decision**: Evaluate if splitting improves clarity
**If split**: Consider player_client.py, matchup_client.py, etc.
**Otherwise**: Reorganize methods within file

#### [ ] 8.14: Reorganize methods in large files
**Action**: Group by functionality

### Code Quality Tasks

#### [ ] 8.15: Check for duplicate code
**Action**: Identify patterns

#### [ ] 8.16: Remove unused code
**Action**: Clean up

#### [ ] 8.17: Improve logging
**Action**: Add comprehensive logging

### Validation Tasks

#### [ ] 8.18: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 8.19: Update code_changes.md
**Action**: Document fetcher refactoring

#### [ ] 8.20: COMMIT - Player Data Fetcher Complete
**Commit message**: "Refactor player-data-fetcher - tests, docs, cleanup"

---

## PHASE 9: NFL SCORES FETCHER

**Directory**: `nfl-scores-fetcher/` (7 files: config, nfl_api_client, nfl_scores_exporter, nfl_scores_fetcher_main, nfl_scores_models, scores_constants)
**Tests**: NONE - need basic smoke tests

### Testing Tasks

#### [ ] 9.1: Create basic smoke tests for nfl_scores_fetcher_main
**File**: `tests/nfl_scores_fetcher/test_nfl_scores_fetcher_main.py` (NEW)
**Estimated tests**: 10-15 tests

#### [ ] 9.2: Create basic tests for nfl_api_client
**File**: `tests/nfl_scores_fetcher/test_nfl_api_client.py` (NEW)
**Estimated tests**: 15-20 tests (mock API calls)

#### [ ] 9.3: Create basic tests for nfl_scores_exporter
**File**: `tests/nfl_scores_fetcher/test_nfl_scores_exporter.py` (NEW)
**Estimated tests**: 10-15 tests

#### [ ] 9.4: Create basic tests for nfl_scores_models
**File**: `tests/nfl_scores_fetcher/test_nfl_scores_models.py` (NEW)
**Estimated tests**: 10-15 tests

#### [ ] 9.5: Create basic tests for config
**File**: `tests/nfl_scores_fetcher/test_config.py` (NEW)
**Estimated tests**: 5-10 tests

### Documentation Tasks

#### [ ] 9.6: Add author attribution to all files
**Files**: All 7 nfl-scores-fetcher files

#### [ ] 9.7: Remove date references
**Action**: Check all files

#### [ ] 9.8: Add heavy inline comments
**Action**: Document all files

#### [ ] 9.9: Standardize docstrings
**Action**: Google style

### Code Organization Tasks

#### [ ] 9.10: Reorganize methods in large files
**Action**: Group by functionality

### Code Quality Tasks

#### [ ] 9.11: Check for duplicate code
**Action**: Compare with player-data-fetcher for shared patterns

#### [ ] 9.12: Remove unused code
**Action**: Clean up

#### [ ] 9.13: Improve logging
**Action**: Add comprehensive logging

### Validation Tasks

#### [ ] 9.14: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 9.15: Update code_changes.md
**Action**: Document scores fetcher refactoring

#### [ ] 9.16: COMMIT - NFL Scores Fetcher Complete
**Commit message**: "Refactor nfl-scores-fetcher - tests, docs, cleanup"

---

## PHASE 10: SIMULATION

**Directory**: `simulation/` (11 files)
**Tests**: 41 existing tests - review and enhance

### Testing Tasks

#### [ ] 10.1: Review and enhance ConfigGenerator tests
**File**: `tests/simulation/test_config_generator.py`
**Current**: 23 tests
**Action**: Add edge cases
**Estimated additional tests**: 10-15 tests

#### [ ] 10.2: Review and enhance SimulationManager tests
**File**: `tests/simulation/test_simulation_manager.py`
**Current**: 18 tests
**Action**: Add edge cases
**Estimated additional tests**: 10-15 tests

#### [ ] 10.3: Create tests for untested simulation files
**Files**: ConfigPerformance, DraftHelperTeam, manual_simulation, ParallelLeagueRunner, ProgressTracker, ResultsManager, SimulatedLeague, SimulatedOpponent, Week, utils/scheduler
**Action**: Create basic tests for each
**Estimated tests**: 50-70 tests across all files

### Documentation Tasks

#### [ ] 10.4: Add author attribution to all simulation files
**Files**: All 11 simulation files

#### [ ] 10.5: Remove date references
**Action**: Check all files

#### [ ] 10.6: Add heavy inline comments
**Action**: Document all simulation logic

#### [ ] 10.7: Standardize docstrings
**Action**: Google style

### Code Organization Tasks

#### [ ] 10.8: Reorganize large simulation files
**Action**: Group by functionality

### Code Quality Tasks

#### [ ] 10.9: Check for duplicate code
**Action**: Identify patterns

#### [ ] 10.10: Remove unused code
**Action**: Clean up

#### [ ] 10.11: Improve logging
**Action**: Add logging

### Validation Tasks

#### [ ] 10.12: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 10.13: Update code_changes.md
**Action**: Document simulation refactoring

#### [ ] 10.14: COMMIT - Simulation Complete
**Commit message**: "Refactor simulation - tests, docs, cleanup"

---

## PHASE 11: ROOT SCRIPTS

**Files**: `run_league_helper.py`, `run_player_fetcher.py`, `run_scores_fetcher.py`, `run_simulation.py`, `run_pre_commit_validation.py`

### Testing Tasks

#### [ ] 11.1: Create tests for root scripts
**Files**: Create test files for each script
**Estimated tests**: 20-30 tests total
**Coverage**: Argument parsing, main execution flow, error handling

### Documentation Tasks

#### [ ] 11.2: Add author attribution to all scripts
**Files**: All 5 root scripts

#### [ ] 11.3: Remove date references
**Action**: Check all scripts

#### [ ] 11.4: Add heavy inline comments
**Action**: Document script logic

#### [ ] 11.5: Standardize docstrings
**Action**: Google style

### Code Quality Tasks

#### [ ] 11.6: Check for duplicate code
**Action**: Extract common patterns

#### [ ] 11.7: Remove unused code
**Action**: Clean up

#### [ ] 11.8: Improve logging
**Action**: Add logging

### Validation Tasks

#### [ ] 11.9: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 11.10: Update code_changes.md
**Action**: Document root scripts refactoring

#### [ ] 11.11: COMMIT - Root Scripts Complete
**Commit message**: "Refactor root scripts - tests, docs, cleanup"

---

## PHASE 12: INTEGRATION TESTS

**Priority**: HIGH - comprehensive integration tests across modules

### Testing Tasks

#### [ ] 12.1: Create integration tests for league helper workflow
**File**: `tests/integration/test_league_helper_integration.py` (NEW)
**Estimated tests**: 20-30 tests
**Coverage**:
- Full draft workflow (add multiple players)
- Starter helper with drafted roster
- Trade simulator with full roster
- Mode transitions and data persistence
- Error recovery scenarios

#### [ ] 12.2: Create integration tests for data fetcher workflow
**File**: `tests/integration/test_data_fetcher_integration.py` (NEW)
**Estimated tests**: 10-15 tests
**Coverage**:
- Fetch → Export → Load in league helper
- Data format consistency
- Error handling across pipeline

#### [ ] 12.3: Create integration tests for simulation workflow
**File**: `tests/integration/test_simulation_integration.py` (NEW)
**Estimated tests**: 10-15 tests
**Coverage**:
- Config generation → Simulation → Results
- Multi-config simulation runs
- Error scenarios

### Validation Tasks

#### [ ] 12.4: Run full test suite
**Requirement**: 100% pass rate

#### [ ] 12.5: Update code_changes.md
**Action**: Document integration tests

#### [ ] 12.6: COMMIT - Integration Tests Complete
**Commit message**: "Add comprehensive integration tests"

---

## PHASE 13: DOCUMENTATION

### README Tasks

#### [ ] 13.1: Write comprehensive README.md
**Sections**:
1. Project Overview
2. Features (list 4 modes + fetchers + simulation)
3. Installation & Setup
4. Quick Start Guide
5. Usage Examples (for each mode)
6. Data Files (what they contain, format)
7. Configuration (league_config.json)
8. Testing (how to run tests)
9. Development Guidelines (point to CLAUDE.md)
10. License/Author

**Estimated length**: 500-1000 lines

### CLAUDE.md Updates

#### [ ] 13.2: Update CLAUDE.md with testing standards
**Add section**: Comprehensive testing guidelines based on patterns used

#### [ ] 13.3: Update CLAUDE.md with file structure
**Update section**: Current file organization after refactoring

#### [ ] 13.4: Add refactoring guidelines to CLAUDE.md
**New section**: When and how to refactor code

### ARCHITECTURE.md Creation

#### [ ] 13.5: Create ARCHITECTURE.md
**Sections**:
1. System Overview
2. Component Architecture
3. Data Flow
4. Manager Hierarchy
5. Mode System Design
6. Configuration System
7. Testing Architecture
8. Extension Points

**Estimated length**: 800-1200 lines

### Validation Tasks

#### [ ] 13.6: Review all documentation for consistency
**Action**: Ensure README, CLAUDE.md, ARCHITECTURE.md align

#### [ ] 13.7: Update code_changes.md
**Action**: Document documentation work

#### [ ] 13.8: COMMIT - Documentation Complete
**Commit message**: "Complete comprehensive documentation - README, ARCHITECTURE, CLAUDE updates"

---

## FINAL VALIDATION

### [ ] 14.1: Run complete test suite one final time
**Command**: `python tests/run_all_tests.py`
**Requirement**: 100% pass rate
**Expected**: 600-800+ tests passing

### [ ] 14.2: Verify all files have author attribution
**Action**: Scan all 80 Python files for "Author: Kai Mizuno"

### [ ] 14.3: Verify all dates removed
**Action**: Scan all files for "Last Updated" or date references

### [ ] 14.4: Verify all files have heavy comments
**Action**: Spot check files for comment density

### [ ] 14.5: Run linting check
**Action**: Run any linters to ensure code quality

### [ ] 14.6: Manual smoke test all modes
**Action**: Run league helper, test each mode interactively

### [ ] 14.7: Manual smoke test fetchers
**Action**: Run player fetcher and scores fetcher

### [ ] 14.8: Manual smoke test simulation
**Action**: Run simulation

### [ ] 14.9: Finalize code_changes.md
**Action**: Complete documentation of all changes

### [ ] 14.10: FINAL COMMIT
**Commit message**: "Complete comprehensive refactoring - final validation"

---

## PROJECT COMPLETION CHECKLIST

- [ ] All 80 Python files refactored
- [ ] 600-800+ tests created/enhanced (100% passing)
- [ ] All files have "Author: Kai Mizuno"
- [ ] All date references removed
- [ ] Heavy inline comments added everywhere
- [ ] All docstrings standardized to Google style
- [ ] Code reorganized for readability
- [ ] Duplicate code extracted
- [ ] Unused code removed
- [ ] Logging improved throughout
- [ ] README.md written (comprehensive)
- [ ] ARCHITECTURE.md created
- [ ] CLAUDE.md updated
- [ ] Integration tests created
- [ ] All commits made with 100% test pass rate
- [ ] code_changes.md complete

---

## VERIFICATION SUMMARY (6 ITERATIONS COMPLETED)

### Iteration 1: Initial TODO Creation
- Created comprehensive task breakdown for all 80 files
- Organized by 13 phases (directory-by-directory)
- Identified 10+ core refactoring objectives from refactoring.txt

### Iteration 2: Requirements Cross-Reference
- ✅ Re-read refactoring.txt - 10 requirements identified
- ✅ Re-read refactoring_questions.md answers - all confirmed
- **Findings**:
  - 345 existing test functions (good foundation)
  - Only 1 file with TODO/FIXME comments (very clean codebase)
  - FantasyTeam.py has 2 public methods missing docstrings (set_score, get_matching_byes_in_roster)

### Iteration 3: Codebase Pattern Analysis
- **Files analyzed**: 53 main Python files (20 league_helper + 7 utils + 26 fetchers/simulation)
- **Classes found**: 46 manager/model classes
- **Large files identified** (>500 lines):
  1. TradeSimulatorModeManager: 1068 lines (consider breaking up)
  2. PlayerManager: 890 lines
  3. FantasyTeam: 749 lines
  4. ConfigManager: 686 lines
  5. error_handler: 582 lines
  6. DraftedRosterManager: 562 lines
  7. data_file_manager: 529 lines
- **Logging coverage**: FantasyTeam has 51 logger calls (good coverage)
- **Duplicate function names**: NONE found across managers (excellent modularity)

### Iteration 4: Test Infrastructure Analysis
- **Existing tests**: 345 test functions across 13 modules
- **Test files using fixtures**: 9 files (good reusability)
- **Mock usage**: 687 mock usages (excellent test isolation)
- **Mode managers**: 4 found (AddToRoster, StarterHelper, TradeSimulator, ModifyPlayerData)
- **CRITICAL GAP**: NO integration tests exist - need to create tests/integration/ directory
- **Error handling analysis**:
  - PlayerManager: Only 3 try blocks (needs improvement)
  - csv_utils: 9 try blocks, 13 raises (good)
  - error_handler: 11 try blocks, 10 raises (excellent)

### Iteration 5: Documentation Quality Analysis
- **Mode managers**: 4 confirmed
- **Integration test directory**: Does NOT exist (must create)
- **Docstring quality**:
  - ConfigManager: Good (Args=10, Returns=8, Raises=5, Examples=2)
  - PlayerManager: Needs improvement (Args=7, Returns=7, Raises=0, Examples=2)
  - TeamDataManager: Needs improvement (Args=6, Returns=6, Raises=0, Examples=0)
- **Mock patterns**: Using unittest.mock (standard, appropriate)

### Iteration 6: Code Quality Patterns
- **Print statements found**: 177 in main code (SHOULD USE LOGGING!)
- **Import organization**:
  - FantasyTeam: ✅ Organized
  - csv_utils: ✅ Organized
  - AddToRosterModeManager: ❌ Needs reorganization
- **__pycache__ presence**: Normal Python cache files (not an issue)

---

## CRITICAL FINDINGS FROM VERIFICATION

### High Priority Issues to Address:
1. **NO integration tests** - Must create comprehensive integration test suite
2. **177 print statements** - Replace with proper logging (DEBUG/INFO levels)
3. **Missing Raises sections** - PlayerManager & TeamDataManager docstrings incomplete
4. **2 methods missing docstrings** - FantasyTeam.set_score and get_matching_byes_in_roster
5. **Import organization** - AddToRosterModeManager needs cleanup
6. **Error handling** - PlayerManager has minimal try/catch blocks (only 3)

### Key Patterns Identified for Reuse:
- **Test fixtures** - conftest.py provides good test infrastructure
- **Mock patterns** - Extensive use of unittest.mock throughout tests
- **Error handling** - error_handler.py and csv_utils.py show excellent patterns
- **Logging** - FantasyTeam.py shows good logger usage (51 calls)
- **Docstring format** - ConfigManager.py shows exemplary Google style

### Code Reuse Opportunities:
- **CSV operations** - csv_utils.py already provides shared utilities (leverage more)
- **Error handling** - error_handler.py provides decorators and context managers
- **Logging setup** - LoggingManager.py provides centralized configuration
- **No duplicate function names** - Managers are well-modularized (no extraction needed)

### Risk Areas Identified:
- **Large files** - TradeSimulatorModeManager (1068 lines) may need breaking up
- **Complex logic** - FantasyTeam slot management (748 lines, complex FLEX logic)
- **API calls** - player-data-fetcher and nfl-scores-fetcher need mocked tests
- **Integration points** - No tests covering mode-to-mode workflows

---

## UPDATED TODO PRIORITIES BASED ON VERIFICATION

### Immediate Actions (Before Starting Phase 1):
1. ✅ Create tests/integration/ directory structure
2. ✅ Document print statement locations for logging conversion
3. ✅ Add Raises sections to PlayerManager/TeamDataManager docstrings
4. ✅ Add docstrings to FantasyTeam missing methods
5. ✅ Reorganize AddToRosterModeManager imports

### Additional Tasks Added to Phases:

**Phase 1 (league_helper/util/) - ADD**:
- [ ] Task 1.27: Replace print statements with logging (find ~20-30 in util/)
- [ ] Task 1.28: Add Raises sections to all PlayerManager docstrings
- [ ] Task 1.29: Add Raises sections to all TeamDataManager docstrings
- [ ] Task 1.30: Add docstrings to FantasyTeam.set_score and get_matching_byes_in_roster
- [ ] Task 1.31: Improve error handling in PlayerManager (add try/catch blocks)

**Phase 2 (add_to_roster_mode/) - ADD**:
- [ ] Task 2.13: Reorganize imports (std lib → third party → local)
- [ ] Task 2.14: Replace print statements with logging

**Phase 12 (integration tests) - EXPAND**:
- [ ] Task 12.7: Create tests/integration/__init__.py
- [ ] Task 12.8: Create comprehensive fixture library for integration tests
- [ ] Task 12.9: Test mode coordination and data persistence
- [ ] Task 12.10: Test error recovery across modes

**All Phases - ADD**:
- [ ] For each phase: Convert print() to logger.info() or logger.debug()
- [ ] For each phase: Verify error handling with try/catch blocks
- [ ] For each phase: Ensure all public methods have Raises sections in docstrings

---

## REQUIREMENTS TRACEABILITY MATRIX

Mapping refactoring.txt requirements to TODO tasks:

| Requirement | TODO Tasks | Status |
|-------------|-----------|--------|
| 1. Comprehensive unit tests + edge cases | Tasks 1.1-11.1 (all testing tasks) | ✅ Planned |
| 2. Comprehensive comments/descriptions + author | Tasks 1.10-13.7 (all doc tasks) | ✅ Planned |
| 3. Reorganize files for readability | Tasks 1.17-11.6 (all org tasks) | ✅ Planned |
| 4. Improve modularity (break up files) | Tasks 4.7, 8.13 (large file decisions) | ✅ Planned |
| 5. Eliminate duplicate code | Tasks 1.20-11.6 (duplicate checks) | ✅ Planned |
| 6. Update README/CLAUDE docs | Tasks 13.1-13.5 (documentation) | ✅ Planned |
| 7. Remove unused code | Tasks 1.21-11.7 (unused removal) | ✅ Planned |
| 8. Improve logging (DEBUG/INFO) | Tasks 1.23-11.8 + NEW print→log tasks | ✅ Planned |
| 9. Identify code quality improvements | Embedded in all phases | ✅ Planned |
| 10. Author attribution (Kai Mizuno) | Tasks 1.10-11.2 (author tasks) | ✅ Planned |
| 11. Remove date references | Tasks 1.11-11.3 (date removal) | ✅ Planned |

**Coverage**: 100% of requirements mapped to specific tasks ✅

---

## ESTIMATED TEST COUNT BY PHASE

Based on verification analysis:

| Phase | Current Tests | New Tests | Enhanced Tests | Total After |
|-------|---------------|-----------|----------------|-------------|
| 1. league_helper/util/ | 179 | 50-100 | 30-40 | 260-320 |
| 2. add_to_roster_mode/ | 0 | 30-40 | 0 | 30-40 |
| 3. starter_helper_mode/ | 24 | 0 | 10-15 | 34-39 |
| 4. trade_simulator_mode/ | 80 | 0 | 15-20 | 95-100 |
| 5. modify_player_data_mode/ | 20 | 0 | 10-15 | 30-35 |
| 6. league_helper core | 0 | 20-30 | 0 | 20-30 |
| 7. utils/ | 4 | 130-180 | 20-25 | 154-209 |
| 8. player-data-fetcher/ | 0 | 65-90 | 0 | 65-90 |
| 9. nfl-scores-fetcher/ | 0 | 50-75 | 0 | 50-75 |
| 10. simulation/ | 41 | 50-70 | 20-30 | 111-141 |
| 11. root scripts | 0 | 20-30 | 0 | 20-30 |
| 12. integration tests | 0 | 40-60 | 0 | 40-60 |
| **TOTAL** | **345** | **455-675** | **105-145** | **909-1169** |

**Expected final test count**: ~900-1200 tests (from current 345)
**Test coverage target**: Comprehensive for all files

---

## PROGRESS TRACKING

**Current Phase**: VERIFICATION COMPLETE (6 iterations)
**Next Step**: Begin Phase 1 - League Helper Utils
**Total Iterations Performed**: 6 (exceeded minimum 3 requirement)
**Requirements Coverage**: 100% mapped to tasks
**Critical Gaps Identified**: 7 (integration tests, print statements, docstrings, error handling)
**Estimated Total Time**: 50-70+ hours of work (increased from 40-60 based on findings)
**Estimated Commits**: 13-15 commits
**Estimated Tests Added**: 560-824 new/enhanced tests

---

**Note**: This TODO file will be updated as work progresses. Keep it current for session continuity.
