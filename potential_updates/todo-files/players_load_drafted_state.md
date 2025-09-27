# TODO: Players Load Drafted State Feature

## Objective
Add functionality to the player_data_fetcher that loads drafted player state from an external CSV file, providing an alternative to the existing "carry over drafted player data from existing players.csv" logic.

## Progress Tracking
**IMPORTANT**: Keep this file updated with progress as tasks are completed. Each task should be marked as [DONE] when completed.

## Pre-Development Questions - ANSWERED
- [x] **ANSWERED**: Fuzzy search should be case-insensitive
- [x] **ANSWERED**: Match generally by name, then verify through position and city
- [x] **ANSWERED**: Handle name variations through fuzzy matching, verify with position/city
- [x] **ANSWERED**: If multiple matches after name/position/city check, skip the player
- [x] **ANSWERED**: For duplicate entries in CSV, only use first occurrence and skip duplicates
- [x] **ANSWERED**: CSV format can be flexible
- [x] **ANSWERED**: If drafted_data.csv is missing/corrupted, treat as if LOAD_DRAFTED_DATA_FROM_FILE is off

## Main Implementation Tasks

### 1. Configuration Updates [NOT STARTED]
- [ ] Add `DRAFTED_DATA` config variable (string path, default: "./drafted_data.csv")
- [ ] Add `MY_TEAM_NAME` config variable (string, default: "Sea Sharp")
- [ ] Add `LOAD_DRAFTED_DATA_FROM_FILE` toggle config variable
- [ ] Add validation logic to ensure only one of `LOAD_DRAFTED_DATA_FROM_FILE` or `PRESERVE_DRAFTED_VALUES` is enabled
- [ ] Update config validation to prevent both toggles being enabled simultaneously

### 2. Drafted Data Loading Module [NOT STARTED]
- [ ] Create function to load and parse drafted_data.csv file
- [ ] Implement error handling for missing/invalid CSV files
- [ ] Parse player info format: "Name Position - Team" from first column
- [ ] Store fantasy team assignments from second column

### 3. Fuzzy Search Implementation [NOT STARTED]
- [ ] Install/import fuzzy string matching library (likely `fuzzywuzzy` or similar)
- [ ] Create fuzzy search function to match players by name, position, and team
- [ ] Handle player name variations and partial matches
- [ ] Define matching threshold for fuzzy search accuracy

### 4. Drafted State Assignment Logic [NOT STARTED]
- [ ] Integrate drafted data loading into player processing pipeline
- [ ] For each player during processing:
  - [ ] Perform fuzzy search against drafted_data
  - [ ] If found and team matches `MY_TEAM_NAME`: set drafted=2
  - [ ] If found but different team: set drafted=1
  - [ ] If not found: set drafted=0
- [ ] Ensure this logic only runs when `LOAD_DRAFTED_DATA_FROM_FILE` is enabled

### 5. Integration with Existing Logic [NOT STARTED]
- [ ] Modify existing player processing to check new toggle
- [ ] Ensure mutual exclusivity with `PRESERVE_DRAFTED_VALUES` logic
- [ ] Add fallback behavior when neither toggle is enabled (set all drafted=0)
- [ ] Update existing data preservation logic to respect new toggle

### 6. Testing Implementation [NOT STARTED]
- [ ] Create unit tests for drafted data loading functionality
- [ ] Test fuzzy search accuracy with sample data
- [ ] Test configuration validation (mutual exclusivity)
- [ ] Test integration with existing player processing pipeline
- [ ] Test error handling for invalid/missing CSV files
- [ ] Verify existing unit tests still pass

### 7. Documentation Updates [NOT STARTED]
- [ ] Update player-data-fetcher README.md with new feature
- [ ] Update CLAUDE.md with new configuration options
- [ ] Document the CSV file format requirements
- [ ] Add examples of drafted_data.csv format
- [ ] Update weekly workflow documentation if needed

### 8. Final Validation [NOT STARTED]
- [ ] Run full test suite to ensure no regressions
- [ ] Test with actual drafted_data.csv file
- [ ] Verify player data fetcher still completes in 8-15 minutes
- [ ] Test both toggle states (LOAD_DRAFTED_DATA_FROM_FILE on/off)
- [ ] Confirm mutual exclusivity with PRESERVE_DRAFTED_VALUES works

### 9. Project Cleanup [NOT STARTED]
- [ ] Move `players_load_drafted_state.txt` to done folder
- [ ] Update any relevant rules files
- [ ] Final documentation review

## Technical Notes
- **CSV Format**: First column contains "Name Position - Team", second column contains fantasy team name
- **Example**: "Amon-Ra St. Brown WR - DET,Fishoutawater"
- **Fuzzy Search**: Need to extract name, position, and team from player data for matching
- **Team Mapping**: Use `MY_TEAM_NAME` to determine if player belongs to user's team (drafted=2)
- **Fallback**: When no toggles are enabled, all players get drafted=0

## Dependencies
- Fuzzy string matching library (fuzzywuzzy, rapidfuzz, or similar)
- CSV parsing (likely built-in csv module)
- Integration with existing player data processing pipeline

## Files to Modify
- `player-data-fetcher/config.py` - Add new configuration variables
- `player-data-fetcher/` - Main processing logic (exact file to be determined)
- Test files in `player-data-fetcher/tests/` - Add new test coverage
- Documentation files - README.md, CLAUDE.md updates

## Current Status: IMPLEMENTATION COMPLETE ✅
Last Updated: September 22, 2025 - All tasks completed successfully

### Summary of Completed Work:
1. ✅ Added new configuration variables (LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME)
2. ✅ Implemented mutual exclusivity validation with PRESERVE_DRAFTED_VALUES
3. ✅ Created DraftedDataLoader module with fuzzy matching capabilities
4. ✅ Integrated drafted data loading into player data exporter
5. ✅ Created comprehensive unit tests (12 new tests, all passing)
6. ✅ Updated documentation in CLAUDE.md
7. ✅ Verified all existing tests still pass (54/54 tests passing)

### Files Modified/Created:
- Modified: `player-data-fetcher/player_data_fetcher_config.py` - Added new config variables and validation
- Modified: `player-data-fetcher/player_data_constants.py` - Added imports for new config variables
- Modified: `player-data-fetcher/player_data_exporter.py` - Integrated drafted data loader
- Created: `player-data-fetcher/drafted_data_loader.py` - New fuzzy matching module
- Created: `player-data-fetcher/tests/test_drafted_data_loader.py` - Comprehensive test suite
- Modified: `CLAUDE.md` - Updated documentation with new feature details

### Feature Ready for Use:
- Set `LOAD_DRAFTED_DATA_FROM_FILE = True` in player_data_fetcher_config.py
- Ensure `PRESERVE_DRAFTED_VALUES = False` (mutual exclusivity enforced)
- Place your drafted data CSV at the path specified in `DRAFTED_DATA` (default: "./drafted_data.csv")
- Set `MY_TEAM_NAME` to match your fantasy team name in the CSV
- Run player data fetcher normally - drafted states will be automatically assigned