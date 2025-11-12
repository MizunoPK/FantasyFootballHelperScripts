# Player Rating Fixes - TODO

## Objective
Replace tier-based player rating calculation with normalized positional rankings (1-100 scale) in both player-data-fetcher and simulation systems.

## High-Level Phases

### Phase 1: Research Current Implementation
- [ ] Locate ESPN client code in player-data-fetcher
- [ ] Identify where player ratings are currently calculated
- [ ] Understand current tier-based rating system
- [ ] Find where rankings object is accessed
- [ ] Map data flow from rankings to player_rating field

### Phase 2: Update Player-Data-Fetcher (ESPN Client)
**File: player-data-fetcher/espn_client.py**

- [ ] **Step 2.1: Add preprocessing pass** (around line 1300, after Week 1 preprocessing)
  - [ ] Create first pass loop through all players to collect positional ranks
  - [ ] Build dictionary: {position: {'min': min_rank, 'max': max_rank}}
  - [ ] Extract positional_rank using existing logic (lines 1418-1482)
  - [ ] Track min/max rank for each position (QB, RB, WR, TE, K, DST)
  - [ ] **Error Handling**: Handle players with no positional_rank (set to None, skip in min/max calculation)
  - [ ] **Logging**: Log min/max for each position at INFO level after collection
  - [ ] **Edge Case**: If position has 0 players with ranks, set min=max=None

- [ ] **Step 2.2: Store raw positional rank** (in main loop around line 1484)
  - [ ] Instead of converting positional_rank to player_rating immediately
  - [ ] Store positional_rank temporarily in ESPNPlayerData object
  - [ ] Set player_rating to None temporarily

- [ ] **Step 2.3: Add post-processing normalization** (after line 1573, before return)
  - [ ] Loop through all projections
  - [ ] For each player, normalize their positional_rank using formula:
    - normalized = 1 + ((rank - max_rank) / (min_rank - max_rank)) * 99
    - This gives: min_rank (best) → 100, max_rank (worst) → 1
  - [ ] Set player_rating to normalized value
  - [ ] **Error Handling**:
    - [ ] Handle division by zero: if min_rank == max_rank, set rating to 50.0 (neutral)
    - [ ] Handle missing positional_rank: keep player_rating as None (will use fallback)
    - [ ] Handle missing min/max for position: use fallback rating calculation
  - [ ] **Logging**:
    - [ ] Log normalization progress at DEBUG level (every 100 players)
    - [ ] Log count of players normalized vs players using fallback at INFO level
    - [ ] Warn if more than 10% of players use fallback
  - [ ] **Data Validation**:
    - [ ] Assert all normalized ratings are between 1 and 100
    - [ ] Log warning if rating is exactly 1 or 100 (edge case check)

- [ ] **Step 2.4: Update data model comment**
  - [ ] Update player_data_models.py line 45 comment
  - [ ] Change from: "0-100 scale from ESPN position-specific consensus rankings"
  - [ ] Change to: "0-100 scale normalized from ESPN position-specific rankings (100=best, 1=worst within position)"

- [ ] **Step 2.5: Remove/deprecate old method**
  - [ ] Remove _convert_positional_rank_to_rating() (line 1168)
  - [ ] Remove tier-based calculation logic (lines 1186-1198)

- [ ] **Step 2.6: Test player-data-fetcher**
  - [ ] Run player data fetcher
  - [ ] Verify player_rating values are between 1-100
  - [ ] Verify best player at each position has rating ~100
  - [ ] Verify worst player at each position has rating ~1

### Phase 3: Update Simulation System
**Files: simulation/sim_data/players_*_backup.csv**

- [ ] **Step 3.1: Create normalization script**
  - [ ] Create new script: simulation/normalize_player_ratings.py
  - [ ] Import logging: from utils.LoggingManager import setup_logger, get_logger
  - [ ] Import CSV utilities: from utils.csv_utils import read_csv_with_validation
  - [ ] Import error handling: from utils.error_handler import error_context, DataProcessingError
  - [ ] Read players_projected_backup.csv using pandas
  - [ ] Read players_actual_backup.csv using pandas
  - [ ] CSV structure: id, name, team, position, bye_week, fantasy_points, injury_status, drafted, locked, average_draft_position, **player_rating**, week_1_points, ...
  - [ ] **Error Handling**: Validate required columns exist (id, position, player_rating)
  - [ ] **Error Handling**: Handle file not found with clear error message
  - [ ] **Logging**: Log script start, file paths, and row counts at INFO level

- [ ] **Step 3.2: Calculate min/max per position**
  - [ ] Group players by position (QB, RB, WR, TE, K, DST)
  - [ ] For each position, find min(player_rating) and max(player_rating)
  - [ ] Store in dict: {position: {'min': X, 'max': Y}}
  - [ ] **Error Handling**: Skip players with NaN or None player_rating
  - [ ] **Error Handling**: Handle positions with only 1 player (min == max)
  - [ ] **Logging**: Log min/max for each position at INFO level
  - [ ] **Data Validation**: Verify min <= max for all positions

- [ ] **Step 3.3: Normalize player_rating values**
  - [ ] For each player in both CSV files:
    - [ ] Get their position's min/max from step 3.2
    - [ ] Apply formula: normalized = 1 + ((old_rating - max) / (min - max)) * 99
    - [ ] This converts: old min (best) → 100, old max (worst) → 1
    - [ ] Update player_rating column with normalized value
  - [ ] **Error Handling**:
    - [ ] Handle division by zero: if min == max, set rating to 50.0
    - [ ] Handle missing player_rating: preserve original None/NaN value
    - [ ] Handle position not in min/max dict: log warning, preserve original
  - [ ] **Logging**:
    - [ ] Log normalization progress for each file at INFO level
    - [ ] Log count of normalized players per position
  - [ ] **Data Validation**:
    - [ ] Verify all normalized values are between 1 and 100
    - [ ] Count and log any values outside range

- [ ] **Step 3.4: Write new CSV files**
  - [ ] Write players_projected.csv with normalized values
  - [ ] Write players_actual.csv with normalized values
  - [ ] Preserve all other columns unchanged (order and names)
  - [ ] Preserve encoding (utf-8)
  - [ ] Verify CSV format matches original structure (same columns, same order)
  - [ ] **Error Handling**: Use try-except for file write operations
  - [ ] **Error Handling**: Create backup of existing files if they exist
  - [ ] **Logging**: Log output file paths and row counts at INFO level

- [ ] **Step 3.5: Validate results**
  - [ ] Check player_rating values are between 1-100
  - [ ] Verify best players have ratings near 100
  - [ ] Verify worst players have ratings near 1
  - [ ] Spot-check a few known players manually

- [ ] **Step 3.6: Test simulation**
  - [ ] Run simulation with new data files
  - [ ] Verify no errors loading CSV files
  - [ ] Check that player ratings are used correctly

### Phase 4: Testing
**Files: tests/player-data-fetcher/test_espn_client.py**

- [ ] **Step 4.1: Update ESPN client tests**
  - [ ] Update/replace tests for _convert_positional_rank_to_rating() (lines 226-314 in test_espn_client.py)
  - [ ] Replace with tests for new normalization logic
  - [ ] Test normalization formula: 1 + ((rank - max) / (min - max)) * 99
  - [ ] Test edge cases: single player position, all same rank, etc.
  - [ ] Verify _get_positional_rank_from_overall() tests still pass (lines 315-410)

- [ ] **Step 4.2: Add integration tests**
  - [ ] Test full _parse_espn_data() flow with new rating calculation
  - [ ] Verify preprocessing pass collects min/max correctly
  - [ ] Verify post-processing normalizes all players
  - [ ] Test with mock ESPN API data

- [ ] **Step 4.3: Create simulation normalization tests**
  - [ ] Create tests/simulation/test_normalize_player_ratings.py
  - [ ] Test reading backup CSV files
  - [ ] Test min/max calculation per position
  - [ ] Test normalization formula
  - [ ] Test writing output CSV files

- [ ] **Step 4.4: Run all unit tests**
  - [ ] Run: python tests/run_all_tests.py
  - [ ] Ensure 100% pass rate (required)
  - [ ] Fix any failing tests

- [ ] **Step 4.5: Manual testing**
  - [ ] Run player-data-fetcher: python run_player_fetcher.py
  - [ ] Inspect output CSV player_rating values
  - [ ] Run simulation: python run_simulation.py
  - [ ] Verify simulation loads new CSV files correctly

### Phase 5: Documentation

- [ ] **Step 5.1: Update scoring documentation**
  - [ ] Update docs/scoring/03_player_rating_multiplier.md
  - [ ] Replace tier-based formula description with normalization formula
  - [ ] Update "Formula" section (lines 19-22)
  - [ ] Add new "Recent Updates" entry documenting this change
  - [ ] Update code implementation references (lines 25-26)

- [ ] **Step 5.2: Update README if needed**
  - [ ] Check if README.md mentions player rating calculation
  - [ ] Update if tier-based system is referenced

- [ ] **Step 5.3: Update CLAUDE.md if needed**
  - [ ] Check if CLAUDE.md references player rating calculation
  - [ ] Update project structure if new files added

- [ ] **Step 5.4: Update code comments**
  - [ ] Update docstrings in espn_client.py for new methods
  - [ ] Update comments explaining rating calculation
  - [ ] Remove outdated tier references

### Phase 6: Final Validation & Completion
- [ ] Run pre-commit validation protocol
- [ ] Execute requirement verification protocol
- [ ] Finalize code changes documentation
- [ ] Move files to updates/done/

## Anticipated File Modifications
- player-data-fetcher/data_sources/espn_client.py (or similar ESPN client file)
- simulation/SimulationManager.py (or data processing file)
- simulation/sim_data/players_projected.csv
- simulation/sim_data/players_actual.csv
- tests/player-data-fetcher/test_*.py (unit tests)
- tests/simulation/test_*.py (unit tests)

## Testing Requirements
- Unit tests for normalization calculation logic
- Unit tests for min/max rank detection
- Unit tests for edge cases (single player position, etc.)
- Integration test for full player-data-fetcher run
- Integration test for simulation data generation

## Documentation Updates
- Update technical documentation for player_rating calculation method
- Update any references to tier-based rating system

## Progress Tracking
This TODO file will be updated after each phase completion to track progress. Each completed task will be marked with [x]. New tasks discovered during implementation will be added with appropriate phase assignment.

**Important**: Keep this file updated throughout implementation in case a new session needs to continue the work.

---

## Verification Summary

### Iteration 1: Initial Verification (Completed)

**Requirements Coverage**:
- ✅ Requirement 1: Extract current week's ranking from rankings object → Covered in Phase 2, Step 2.1
- ✅ Requirement 2: Create position-to-min/max-rank mapping → Covered in Phase 2, Step 2.1
- ✅ Requirement 3: Normalize ranks to 1-100 scale → Covered in Phase 2, Step 2.3
- ✅ Requirement 4: Set player_rating to normalized value → Covered in Phase 2, Step 2.3
- ✅ Requirement 5: Update simulation backup CSV files → Covered in Phase 3
- ✅ Requirement 6: Create new players_projected.csv and players_actual.csv → Covered in Phase 3, Steps 3.3-3.4

**Key Codebase Patterns Identified**:
1. **Two-pass processing pattern**: ESPN client already uses preprocessing loop for Week 1 (lines 1300-1319)
   - Can extend this pattern for min/max rank collection
2. **Player rating calculation location**: espn_client.py lines 1414-1505
   - Uses `_convert_positional_rank_to_rating()` method (line 1168) - needs replacement
3. **Rankings extraction**: Lines 1442-1482 extract positional_rank from ESPN API
   - This logic can be reused in preprocessing pass
4. **CSV structure**: Both backup files have same structure with player_rating column at index 10
5. **Test coverage**: Extensive tests exist for current tier-based system (test_espn_client.py:226-314)
   - These tests need updating for new normalization approach

**File Paths Confirmed**:
- ESPN client: `player-data-fetcher/espn_client.py`
- Player data model: `player-data-fetcher/player_data_models.py`
- Backup CSVs: `simulation/sim_data/players_projected_backup.csv`, `simulation/sim_data/players_actual_backup.csv`
- Output CSVs: `simulation/sim_data/players_projected.csv`, `simulation/sim_data/players_actual.csv`
- Tests: `tests/player-data-fetcher/test_espn_client.py`
- Documentation: `docs/scoring/03_player_rating_multiplier.md`

**Existing Code to Reuse**:
- Positional rank extraction logic (espn_client.py:1418-1482)
- Preprocessing loop pattern (espn_client.py:1300-1319)
- Position mappings (ESPN_POSITION_MAPPINGS constant)
- CSV utilities from utils.csv_utils module

**Critical Dependencies**:
1. Phase 2 must complete before Phase 3 (simulation depends on new calculation method)
2. Phase 3 can run independently to create new CSV files
3. Phase 4 testing requires both Phase 2 and Phase 3 complete
4. Phase 1 research is complete

**Edge Cases Identified**:
1. Positions with only 1 player (min == max, causes division by zero)
2. Players without rankings data (need fallback)
3. Week 1 special handling (uses draft ranks instead of ROS)
4. Fallback to older week rankings when current week unavailable

**Next Steps for Iteration 2**:
- Deep dive into error handling strategies
- Research logging patterns
- Identify additional integration points
- Refine task order and dependencies

### Iteration 2: Deep Dive Verification (Completed)

**Error Handling Strategy Added**:
1. **ESPN Client (Phase 2)**:
   - Handle missing positional_rank (set to None, skip from min/max)
   - Handle division by zero when min == max (set rating to 50.0 neutral)
   - Handle missing min/max dict entries (use fallback calculation)
   - Preserve existing try-except patterns around API calls
2. **Simulation Normalization (Phase 3)**:
   - Validate required CSV columns before processing
   - Handle file not found with clear error message
   - Skip players with NaN/None player_rating values
   - Handle division by zero (min == max → rating 50.0)
   - Create backups before overwriting existing files
   - Use try-except for all file I/O operations

**Logging Pattern Applied**:
- **DEBUG level**: Detailed progress (every 100 players), diagnostic info
- **INFO level**: Milestones (start/complete), min/max values, counts, file paths
- **WARNING level**: Recoverable issues (>10% fallback usage, missing data)
- **ERROR level**: Serious failures (file not found, validation errors)
- Pattern matches existing ESPN client logging (espn_client.py:171-568)

**Data Validation Requirements**:
1. **Input Validation**:
   - CSV column presence check before processing
   - Verify min <= max for all positions
   - Check for NaN/None values in player_rating column
2. **Output Validation**:
   - Assert all normalized ratings between 1 and 100
   - Count and log outliers or edge cases
   - Verify output CSV structure matches input

**Additional Utilities Identified**:
- `utils.csv_utils.read_csv_with_validation()` - for validated CSV reading with pandas
- `utils.error_handler.error_context()` - for structured error logging
- `utils.LoggingManager.get_logger()` - for consistent logging
- Custom exceptions: `FileOperationError`, `DataProcessingError`

**Documentation Needs Identified**:
1. **Docstrings**: New methods need Google-style docstrings
2. **Inline Comments**: Explain normalization formula and edge cases
3. **Scoring Docs**: Update docs/scoring/03_player_rating_multiplier.md
4. **Code Comments**: Remove tier-based references, add normalization explanation

**Performance Considerations**:
- Two-pass processing adds ~50% overhead but necessary for normalization
- Pandas operations for CSV should be efficient for ~1000 player dataset
- No additional API calls needed (reusing existing rank extraction)

**Integration Points Confirmed**:
1. ESPNPlayerData model already supports player_rating field (no schema changes)
2. Existing fallback logic (lines 1486-1505) remains functional
3. Test infrastructure exists and needs updates (not new test files)
4. No changes needed to config.py or constants files

**Next Steps for Iteration 3**:
- Verify no circular dependencies
- Confirm cleanup operations if errors occur mid-process
- Final review of task ordering and dependencies
- Validate no missing requirements

### Iteration 3: Final Verification (Completed)

**Circular Dependency Check**: ✅ PASSED
- espn_client.py → player_data_models.py (one-way, no circular)
- simulation modules → PlayerManager/ConfigManager (one-way, no circular)
- normalize_player_ratings.py (new) → utils modules (one-way, no circular)
- No circular dependencies detected

**Integration Point Analysis**:
1. **Data Model** (player_data_models.py:45):
   - `player_rating: Optional[float]` already exists - NO MODEL CHANGES NEEDED
   - Field comment says "0-100 scale" - matches our normalization ✅
   - Only comment update needed to reflect new calculation method
2. **PlayerManager** (league_helper/util/PlayerManager.py:559):
   - Uses player_rating as input parameter to score_player()
   - Reads value but doesn't calculate it - TRANSPARENT to our changes ✅
3. **player_scoring.py** (league_helper/util/player_scoring.py):
   - Consumes player_rating values for scoring calculations
   - No knowledge of calculation method - TRANSPARENT to our changes ✅
4. **Simulation** (simulation/*.py):
   - Reads player_rating from CSV files
   - Doesn't calculate ratings - TRANSPARENT to our changes ✅

**Cleanup Operations** (if errors occur mid-process):
1. **ESPN Client**:
   - If preprocessing fails → return empty projections list (existing pattern)
   - If normalization fails → existing fallback logic handles it (lines 1486-1505)
   - No persistent state to clean up (all in-memory operations)
2. **Simulation Normalization Script**:
   - Create backups before overwriting files (Step 3.4)
   - Use try-except around file writes (Step 3.4)
   - If normalization fails → original backup files remain untouched
   - If write fails → error logged, existing files unchanged

**Task Ordering Validation**:
```
Phase 1 (Research) → Complete
Phase 2 (ESPN Client) → Must complete before any player-data-fetcher runs
Phase 3 (Simulation CSV) → Can run independently OR after Phase 2
Phase 4 (Testing) → Requires Phase 2 AND Phase 3 complete
Phase 5 (Documentation) → Can overlap with Phase 4
Phase 6 (Final Validation) → Requires all phases complete
```
- **Dependency chain is valid** ✅
- Phase 2 and Phase 3 are independent and can be developed in parallel
- Testing requires both to validate full system

**Missing Requirements Check**:
- ✅ Requirement 1: Extract current week's ranking → Covered (Phase 2, Step 2.1)
- ✅ Requirement 2: Compile position min/max → Covered (Phase 2, Step 2.1)
- ✅ Requirement 3: Normalize ranks 1-100 → Covered (Phase 2, Step 2.3)
- ✅ Requirement 4: Set player_rating → Covered (Phase 2, Step 2.3)
- ✅ Requirement 5: Read backup CSVs → Covered (Phase 3, Step 3.1)
- ✅ Requirement 6: Calculate CSV min/max → Covered (Phase 3, Step 3.2)
- ✅ Requirement 7: Create new CSVs → Covered (Phase 3, Steps 3.3-3.4)
- **NO MISSING REQUIREMENTS** ✅

**Backward Compatibility**:
- Existing fallback logic preserved (lines 1486-1505)
- ESPNPlayerData model unchanged (no breaking changes)
- CSV file format unchanged (same columns, same order)
- Downstream consumers (PlayerManager, scoring) unaffected

**Code Quality Requirements Met**:
- ✅ Error handling strategies defined
- ✅ Logging patterns specified (DEBUG/INFO/WARNING/ERROR)
- ✅ Data validation requirements documented
- ✅ Edge cases identified and handled
- ✅ Docstring format requirements noted (Google style)
- ✅ Testing strategy defined (unit + integration)
- ✅ Documentation updates specified

**Pre-Implementation Checklist**:
- ✅ All 6 requirements from original file covered in TODO
- ✅ Specific file paths identified for all changes
- ✅ Existing code patterns researched and documented
- ✅ Error handling and logging strategies defined
- ✅ Test updates planned and specified
- ✅ Documentation updates identified
- ✅ No circular dependencies or integration conflicts
- ✅ Task dependencies validated
- ✅ 3 verification iterations complete (6 total across both rounds)

**READY FOR IMPLEMENTATION** ✅

---

## User Decisions (Step 4 of Rules Protocol)

User has approved all recommendations from questions file. Implementation will proceed with:

1. **Formula Direction**: Best player (min_rank) → 100, Worst player (max_rank) → 1 ✅
2. **Division by Zero**: Use 50.0 (neutral rating) when min == max ✅
3. **Old Method Removal**: Remove `_convert_positional_rank_to_rating()` completely ✅
4. **Simulation Script**: Standalone manual script (can be deleted after use) ✅
5. **CSV Backup**: Direct overwrite (backup files already exist with "_backup" suffix) ✅
6. **Test Updates**: Parallel development (update tests as each phase completes) ✅
7. **Data Model Comment**: Update to detailed description with normalization method ✅
8. **Logging Level**: INFO level for development (balanced verbosity) ✅
9. **Phase Order**: Sequential - Phase 2 (ESPN client) first, then Phase 3 (simulation) ✅
10. **Fallback Behavior**: Use existing fallback calculation (lines 1486-1505) ✅

**Decision Date**: 2025-11-05
**Status**: Ready to proceed with second verification round

---

## Second Verification Round (Steps 5 - 3 More Iterations Required)

Now executing 3 additional verification iterations with user decisions integrated:

### Iteration 4 (Second Round - Iteration 1): User Decisions Integration

**Validating User Decisions Reflected in TODO Tasks**:

✅ **Decision 1 (Formula)**: Reflected in Phase 2, Step 2.3
- Task correctly specifies: min_rank (best) → 100, max_rank (worst) → 1
- Formula: `normalized = 1 + ((rank - max_rank) / (min_rank - max_rank)) * 99`
- ✅ VERIFIED: Formula produces correct direction

✅ **Decision 2 (Division by Zero)**: Reflected in Phase 2, Step 2.3 and Phase 3, Step 3.3
- Error handling: "if min_rank == max_rank, set rating to 50.0 (neutral)"
- ✅ VERIFIED: Both ESPN client and simulation use same approach

✅ **Decision 3 (Old Method Removal)**: Reflected in Phase 2, Step 2.4
- Task specifies: "Remove _convert_positional_rank_to_rating() (line 1168)"
- Task specifies: "Remove tier-based calculation logic (lines 1186-1198)"
- ✅ VERIFIED: Complete removal planned

✅ **Decision 4 (Simulation Script)**: Reflected in Phase 3, Step 3.1
- Task specifies: "Create new script: simulation/normalize_player_ratings.py"
- Standalone script approach confirmed
- ✅ VERIFIED: Script is independent, can be run manually

✅ **Decision 5 (CSV Backup)**: Reflected in Phase 3, Step 3.4
- Task specifies: "Write players_projected.csv with normalized values"
- Direct overwrite approach (no timestamped backups needed)
- ✅ VERIFIED: Backup files already exist with "_backup" suffix

✅ **Decision 6 (Test Updates)**: Reflected in Phase 4, Step 4.1
- Task specifies updating tests for each phase
- Parallel development approach
- ✅ VERIFIED: Tests updated alongside implementation

✅ **Decision 7 (Data Model Comment)**: NEW TASK NEEDED
- Need to add task to update player_data_models.py:45 comment
- ❌ MISSING: Add to Phase 2 tasks

✅ **Decision 8 (Logging Level)**: Reflected throughout Phase 2 and Phase 3
- INFO level logging specified in multiple steps
- ✅ VERIFIED: Consistent logging approach

✅ **Decision 9 (Phase Order)**: Reflected in task dependencies
- Phase 2 (ESPN client) before Phase 3 (simulation)
- ✅ VERIFIED: Correct sequential order

✅ **Decision 10 (Fallback Behavior)**: Reflected in Phase 2, Step 2.3
- Error handling: "Handle missing positional_rank: keep player_rating as None (will use fallback)"
- Existing fallback at lines 1486-1505 remains
- ✅ VERIFIED: Fallback logic preserved

**New Tasks Required**:
1. Add task to Phase 2 for updating player_data_models.py:45 comment (Decision 7)

**Updated Task Count**: 6 phases, 28 steps → 30 steps after addition

### Iteration 5 (Second Round - Iteration 2): Implementation Details Refinement

**Refining Task Specificity Based on User Decisions**:

**Phase 2, Step 2.1 - Preprocessing Pass Implementation**:
- **Confirmed Approach**: Extend existing Week 1 preprocessing pattern (lines 1300-1319)
- **Data Structure**: `position_rank_ranges = {'QB': {'min': 1.0, 'max': 25.0, 'count': 25}, ...}`
- **Position List**: ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
- **Edge Case Handling**: If position has 0 players with ranks, skip from dict
- **Logging Example**: `self.logger.info(f"Position rank ranges - QB: 1.0-25.0 (25 players), RB: 1.0-50.0 (50 players), ...")`

**Phase 2, Step 2.2 - Temporary Storage**:
- **Challenge**: ESPNPlayerData model doesn't have positional_rank field
- **Solution**: Store in temporary dict: `player_positional_ranks = {player_id: positional_rank}`
- **Alternative**: Add positional_rank as transient variable (not saved to CSV)
- **Chosen Approach**: Use temporary dict (cleaner, no model changes)

**Phase 2, Step 2.3 - Normalization Formula Details**:
- **Formula**: `normalized = 1 + ((rank - max_rank) / (min_rank - max_rank)) * 99`
- **Example (QB with min=1.0, max=25.0)**:
  - QB1 (rank=1.0): `1 + ((1.0 - 25.0) / (1.0 - 25.0)) * 99 = 1 + (1.0 * 99) = 100.0` ✅
  - QB13 (rank=13.0): `1 + ((13.0 - 25.0) / (1.0 - 25.0)) * 99 = 1 + (0.5 * 99) = 50.5` ✅
  - QB25 (rank=25.0): `1 + ((25.0 - 25.0) / (1.0 - 25.0)) * 99 = 1 + (0.0 * 99) = 1.0` ✅
- **Formula Validation**: ✅ CORRECT - Best gets 100, worst gets 1

**Phase 2, Step 2.4 - Data Model Comment Update**:
- **File**: player-data-fetcher/player_data_models.py
- **Line**: 45
- **Current**: `player_rating: Optional[float] = None  # 0-100 scale from ESPN position-specific consensus rankings`
- **New**: `player_rating: Optional[float] = None  # 0-100 scale normalized from ESPN position-specific rankings (100=best, 1=worst within position)`
- **Additional**: Add note about normalization in class docstring

**Phase 2, Step 2.5 - Method Removal**:
- **Lines to Delete**: 1168-1198 (31 lines)
- **Impact**: Tests at lines 226-314 in test_espn_client.py will fail
- **Mitigation**: Update tests in Phase 4 immediately after

**Phase 3, Script Architecture**:
- **Script Name**: `simulation/normalize_player_ratings.py`
- **Main Function**: `normalize_simulation_data()`
- **Helper Functions**:
  - `calculate_position_ranges(df: pd.DataFrame) -> Dict[str, Dict[str, float]]`
  - `normalize_rating(rating: float, min_val: float, max_val: float) -> float`
- **CLI Arguments**: Optional `--backup-dir` for custom backup location
- **Estimated Runtime**: ~1 second for ~1000 players

**Mock/Test Data Patterns**:
- **Unit Test Mock Data**: Need 5-10 players per position with varying ranks
- **Integration Test**: Use real data subset (10% sample)
- **Edge Case Tests**: Single player position, all same rank, missing ranks

**Performance Optimization Considerations**:
- **Two-Pass Overhead**: ~10-15% increase in processing time
- **Memory Usage**: Temporary dict stores ~1000 entries (negligible)
- **CSV Processing**: Pandas operations on ~1000 rows (fast, <1 second)
- **No Optimization Needed**: Current approach is efficient

**Rollback Strategy**:
- **If ESPN Client Fails**: Revert espn_client.py changes via git
- **If Tests Fail**: Fix tests before proceeding to Phase 3
- **If Simulation Fails**: Backup files remain untouched, can retry
- **Git Strategy**: Commit after each phase completion

**Integration Testing Strategy**:
1. Phase 2 complete → Run player-data-fetcher → Verify CSV output
2. Phase 3 complete → Run simulation → Verify it loads new CSVs
3. Both complete → End-to-end test of full system

### Iteration 6 (Second Round - Iteration 3): Final Pre-Implementation Verification

**Final Requirements Cross-Check**:
- ✅ Requirement 1 (Extract current week ranking): Phase 2, Step 2.1 - preprocessing pass
- ✅ Requirement 2 (Compile position min/max): Phase 2, Step 2.1 - position_rank_ranges dict
- ✅ Requirement 3 (Normalize ranks 1-100): Phase 2, Step 2.3 - formula validated
- ✅ Requirement 4 (Set player_rating): Phase 2, Step 2.3 - post-processing loop
- ✅ Requirement 5 (Read backup CSVs): Phase 3, Step 3.1 - pandas read
- ✅ Requirement 6 (Calculate CSV min/max): Phase 3, Step 3.2 - groupby position
- ✅ Requirement 7 (Create new CSVs): Phase 3, Steps 3.3-3.4 - normalize and write
- **COVERAGE: 7/7 (100%)** ✅

**User Decision Integration Check**:
- ✅ All 10 decisions reflected in tasks
- ✅ Missing task added (data model comment)
- ✅ Formula direction validated with examples
- ✅ Division by zero handling specified
- ✅ Old method removal planned
- ✅ Simulation script architecture defined
- **INTEGRATION: 100%** ✅

**Task Dependency Validation**:
```
Phase 1 (Research) → COMPLETE
    ↓
Phase 2 (ESPN Client):
    Step 2.1 (Preprocessing) → Step 2.2 (Storage) → Step 2.3 (Normalization)
    ↓                                                       ↓
    Step 2.4 (Data Model) ← parallel with → Step 2.5 (Remove Old Method)
    ↓
    Step 2.6 (Test ESPN Client)
    ↓
Phase 3 (Simulation CSV):
    Step 3.1 (Script Setup) → Step 3.2 (Calculate min/max) → Step 3.3 (Normalize)
    ↓
    Step 3.4 (Write CSVs) → Step 3.5 (Validate) → Step 3.6 (Test Simulation)
    ↓
Phase 4 (Testing):
    Step 4.1 (Update Tests) → parallel with → Step 4.2 (Integration Tests)
    ↓
    Step 4.3 (Simulation Tests) → Step 4.4 (Run All Tests) → Step 4.5 (Manual Testing)
    ↓
Phase 5 (Documentation):
    Step 5.1-5.4 (All documentation updates in parallel)
    ↓
Phase 6 (Final Validation):
    Pre-commit → Requirement Verification → Finalize → Move to Done
```
- **DEPENDENCIES: VALID** ✅

**Risk Assessment**:
1. **Low Risk**:
   - Data model comment update (single line change)
   - Simulation CSV normalization (standalone script, backup files exist)
   - Documentation updates (no code impact)
2. **Medium Risk**:
   - ESPN client normalization (two-pass processing adds complexity)
   - Test updates (must keep 100% pass rate)
3. **High Risk Items**: None identified
4. **Mitigation**: Commit after each phase, comprehensive testing, existing fallback logic

**Resource Requirements**:
- **Time Estimate**:
  - Phase 2: 2-3 hours (ESPN client implementation + testing)
  - Phase 3: 1-2 hours (simulation script + testing)
  - Phase 4: 1-2 hours (test updates + validation)
  - Phase 5: 30-60 minutes (documentation)
  - Phase 6: 30 minutes (final validation)
  - **Total: 5-8 hours**
- **Dependencies**: None (all tools and libraries available)
- **Expertise Required**: Python, pandas, unit testing

**Pre-Implementation Final Checklist**:
- ✅ All 7 requirements mapped to specific tasks
- ✅ All 10 user decisions integrated into plan
- ✅ Missing task identified and added (data model comment)
- ✅ Formula validated with mathematical examples
- ✅ Implementation details refined (data structures, functions, patterns)
- ✅ Error handling strategies comprehensive
- ✅ Logging patterns consistent
- ✅ Test strategy defined
- ✅ Rollback strategy documented
- ✅ Performance impact assessed (minimal)
- ✅ Integration testing strategy defined
- ✅ No circular dependencies
- ✅ No breaking changes to downstream consumers
- ✅ Backward compatibility maintained (fallback logic preserved)
- ✅ Task dependencies validated with flow diagram
- ✅ Risk assessment complete (low-medium risk, no high risk)

**Second Verification Round Summary**:
- **Iterations Completed**: 3 (Iterations 4, 5, 6)
- **Total Iterations (Both Rounds)**: 6 ✅
- **User Decisions Integrated**: 10/10 ✅
- **Requirements Coverage**: 7/7 (100%) ✅
- **Tasks Refined**: 30 steps across 6 phases ✅
- **Implementation Details**: Fully specified ✅

**VERIFICATION COMPLETE - READY TO BEGIN IMPLEMENTATION** ✅

---

## Implementation Readiness Confirmation

**All Protocol Requirements Met**:
- ✅ Step 1: Draft TODO file created
- ✅ Step 2: First verification round (3 iterations) completed
- ✅ Step 3: Questions file created and reviewed with user
- ✅ Step 4: TODO updated with user's answers
- ✅ Step 5: Second verification round (3 iterations) completed
- ✅ Total: 6 verification iterations completed as required

**Ready to Proceed with Implementation**: YES ✅

Beginning Phase 2 implementation...
