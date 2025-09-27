# Drafted Data CSV Loading Reversal - Implementation TODO

## [SUMMARY] Objective Overview
Reverse the approach for loading drafted_data.csv into player data. Instead of checking each player against the CSV during data fetching, we will:
1. Fetch all player data first without considering drafted values
2. At the end, iterate through drafted_data.csv entries
3. For each CSV entry, search the player data to find the matching player
4. Update player's drafted value to 1 (if not MY_TEAM_NAME) or 2 (if MY_TEAM_NAME)

## [TARGET] Master Plan

### Phase 1: Analysis and Design
- [x] **1.1** Analyze current player_data_exporter.py structure to understand data flow
- [x] **1.2** Identify all code locations that currently handle drafted data during fetching
- [x] **1.3** Design new post-processing approach for CSV loading
- [x] **1.4** Plan code refactoring to reuse existing fuzzy matching logic

**Analysis Results:**
- Current drafted logic is in `_espn_player_to_fantasy_player()` method (lines 327-331)
- Uses `self.drafted_data_loader.find_drafted_state()` for each player during conversion
- Post-processing will be added as new method called after `get_fantasy_players()`

### Phase 2: Core Implementation
- [x] **2.1** Create new post-processing method in player_data_exporter.py
- [x] **2.2** Modify main export flow to skip drafted data during initial fetch
- [x] **2.3** Implement CSV-to-player-data matching logic (reverse of current approach)
- [x] **2.4** Refactor DraftedDataLoader to support the new search direction
- [x] **2.5** Update drafted value assignment logic (1 for others, 2 for MY_TEAM_NAME)

### Phase 3: Code Cleanup
- [x] **3.1** Remove old drafted data loading logic from individual player processing
- [x] **3.2** Clean up unused methods and imports in DraftedDataLoader (kept for backward compatibility)
- [ ] **3.3** Update configuration documentation and comments
- [ ] **3.4** Ensure LOAD_DRAFTED_DATA_FROM_FILE toggle still works correctly

### Phase 4: Testing and Validation
- [x] **4.1** Run existing unit tests to ensure no regressions (14/14 tests passing)
- [x] **4.2** Create new unit tests for the reversed search approach (2 comprehensive tests added)
- [ ] **4.3** Test with actual data to verify all 15 CSV players are found
- [ ] **4.4** Verify no false positives (should still be 15 total drafted=2)
- [ ] **4.5** Test edge cases (missing players, name variations)

### Phase 5: Documentation and Cleanup
- [ ] **5.1** Update CLAUDE.md with new architecture approach
- [ ] **5.2** Update any relevant README sections
- [ ] **5.3** Update code comments to reflect new approach
- [ ] **5.4** Move drafted_data_update.txt to done folder

## [NOTE] Context Notes
- **Current Issue**: "Jacory Croskey-Merritt" and potentially other players are missed due to fuzzy matching failures when searching CSV for each player
- **New Approach Benefits**:
  - Search only 15 CSV entries instead of 2000+ players
  - More aggressive matching possible since we know these players should exist
  - Guaranteed to find all CSV players if they exist in player data
  - Simpler logic flow: fetch all data first, then post-process

## [OK] Clarification Responses (from user)
1. **Configuration**: Keep `LOAD_DRAFTED_DATA_FROM_FILE` toggle working the same way
2. **Error Handling**: Log warning and continue if CSV player not found in data
3. **Matching Strategy**: Exact matching first (last name, then first name, check position/team), then fuzzy fallback
4. **Performance**: Optimize for large player datasets where possible
5. **Data Preservation**: Keep `PRESERVE_DRAFTED_VALUES` functionality - both toggles may be used situationally
6. **Testing**: Create test CSV with problematic names for comprehensive unit testing

## ? Key Technical Changes
1. **player_data_exporter.py**: [OK] Added post-processing step after all data is fetched
   - Modified `get_fantasy_players()` to call `self.drafted_data_loader.apply_drafted_data_to_players(fantasy_players)`
   - Updated `_espn_player_to_fantasy_player()` to skip CSV loading during individual processing
2. **DraftedDataLoader**: [OK] Added new `apply_drafted_data_to_players()` method with reverse search
   - 4-strategy progressive matching: exact full name -> last name -> first name -> fuzzy matching
   - Optimized lookup dictionaries for performance with large player datasets
   - Maintains all existing methods for backward compatibility
3. **Configuration**: [OK] Toggle behavior preserved - `LOAD_DRAFTED_DATA_FROM_FILE` works as before
4. **Testing**: [OK] Comprehensive unit test coverage (14/14 tests passing)
   - 2 new tests specifically for reverse search approach
   - Tests both enabled and disabled scenarios
   - Validates progressive matching strategies

## ? Progress Tracking
**Remember to update this file as you complete each task to maintain context for future sessions.**

### Session History
#### Session 1 (Previous)
- [x] Created comprehensive TODO file
- [x] Read and understood objective requirements
- [x] Completed analysis phase (1.1-1.4)

#### Session 2 (Current)
- [x] Implemented new `apply_drafted_data_to_players` method with 4-strategy progressive matching
- [x] Modified `get_fantasy_players` to use post-processing approach
- [x] Cleaned up old drafted data loading from individual player processing
- [x] Created comprehensive unit tests (2 new tests, 14/14 total passing)
- [x] Updated TODO progress tracking
- [ ] **Next**: Real-world testing with actual CSV data

## [WARNING] Important Notes
- Preserve all existing functionality when LOAD_DRAFTED_DATA_FROM_FILE = False
- Maintain backward compatibility with current configuration options
- Keep the fuzzy matching logic but adapt it for reverse search direction
- Ensure performance improvements (should be faster with fewer searches)