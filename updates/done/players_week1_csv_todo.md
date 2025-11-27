# TODO: Create players_week1.csv File

## Objective
Create a new file `players_week1.csv` that combines data from `data/players.csv` and `data/players_projected.csv` with specific column mappings, default values, and calculated fields.

## Requirements Summary
1. **Source columns from players.csv**: id, name, team, position, bye_week, average_draft_position
2. **Source columns from players_projected.csv**: week_1_points through week_17_points
3. **Default values**:
   - drafted: 0
   - locked: 0
   - injury_status: ACTIVE
4. **Calculated fields**:
   - fantasy_points: Sum of all week_1_points through week_17_points from projected file
   - player_rating: Normalized 0-100 based on ADP within each position (lowest ADP = 100 best, highest ADP = 0 worst)
   - **CLARIFICATION**: Lower ADP means player is drafted earlier = better player = rating of 100

---

## Phase 1: Research and Planning
**Status**: IN PROGRESS

### Task 1.1: Understand existing data structures
- [x] Read players.csv header and sample data
- [x] Read players_projected.csv header and sample data
- [ ] Identify all unique positions in players.csv
- [ ] Understand ADP range per position
- [ ] Document join key (id column)

### Task 1.2: Research existing CSV utilities
- [ ] Review utils/csv_utils.py for reusable functions
- [ ] Check if similar data merging exists in codebase
- [ ] Identify logging patterns to follow

### Task 1.3: Determine output file location
- [ ] Confirm output location: data/players_week1.csv
- [ ] Check if file already exists
- [ ] Determine if backup is needed

---

## Phase 2: Implementation

### Task 2.1: Create script to generate players_week1.csv
- [ ] Create Python script (location TBD based on research)
- [ ] Load players.csv
- [ ] Load players_projected.csv
- [ ] Merge on 'id' column
- [ ] Select required columns from players.csv
- [ ] Add week columns from players_projected.csv
- [ ] Set default values (drafted=0, locked=0, injury_status=ACTIVE)
- [ ] Calculate fantasy_points as sum of week columns
- [ ] Calculate player_rating with position-based ADP normalization
- [ ] Write output to data/players_week1.csv

### Task 2.2: Implement player_rating calculation
- [ ] Group players by position
- [ ] Find min/max ADP per position
- [ ] Apply normalization formula: `rating = 100 * (max_adp - player_adp) / (max_adp - min_adp)`
  - min_adp (best player, e.g., 5.09) → rating = 100
  - max_adp (worst player, e.g., 170.06) → rating = 0
- [ ] Handle edge cases (single player in position → use 50.0, same ADP for all → use 50.0)

---

## Phase 3: Testing

### Task 3.1: Unit tests
- [ ] Create test file: tests/test_players_week1_generator.py
- [ ] Test column selection from players.csv
- [ ] Test week column extraction from players_projected.csv
- [ ] Test default value assignment
- [ ] Test fantasy_points calculation
- [ ] Test player_rating normalization per position
- [ ] Test edge cases (missing data, single player position)

### Task 3.2: Validation
- [ ] Verify output file has correct columns
- [ ] Verify all players from both source files are present
- [ ] Verify player_rating is within 0-100 range
- [ ] Verify fantasy_points matches sum of weeks
- [ ] Run existing unit tests to ensure no regressions

---

## Phase 4: Documentation and Cleanup

### Task 4.1: Documentation
- [ ] Update README.md if needed
- [ ] Add inline comments to script
- [ ] Document script usage

### Task 4.2: Final validation
- [ ] Run all unit tests: python tests/run_all_tests.py
- [ ] Manual verification of output file
- [ ] Move update files to done folder

---

## Progress Tracking
- [x] Phase 1 complete (Research and Planning)
- [x] Phase 2 complete (Implementation)
- [x] Phase 3 complete (Testing - 20 new tests, 2190 total passing)
- [x] Phase 4 complete (Documentation and Cleanup)
- [x] All unit tests passing (100%)
- [x] Objective complete

## Final Results
- **Script created**: `generate_players_week1.py` (root level)
- **Tests created**: `tests/root_scripts/test_generate_players_week1.py` (20 tests)
- **Output generated**: `data/players_week1.csv` (710 players)
- **All 2190 tests passing**: 100% success rate

---

## Notes
- Keep this file updated as tasks are completed
- Run pre-commit validation after each phase
- Ensure 100% test pass rate before marking complete

---

## Verification Summary
*To be updated after each verification iteration*

### First Verification Round (5 iterations)

#### Iteration 1: Initial Verification ✅
**Completed**: Yes

**Codebase Research Findings**:
1. **Unique Positions**: RB, WR, QB, TE, K, DST (6 positions)
2. **ADP Ranges by Position**:
   - RB: min=5.09, max=170.06, count=168
   - WR: min=5.46, max=170.00, count=241
   - QB: min=20.67, max=170.00, count=90
   - TE: min=21.35, max=170.10, count=140
   - K: min=90.04, max=169.93, count=39
   - DST: min=86.89, max=169.67, count=32

3. **CSV Utilities Available**:
   - `utils/csv_utils.py` provides `read_csv_with_validation()`, `write_csv_with_backup()`, `merge_csv_files()`
   - Uses pandas for DataFrame operations
   - Error handling with `error_context()`

4. **Existing player_rating Calculation** (from espn_client.py lines 2103-2115):
   - Currently uses positional ranking (not ADP)
   - Formula: `normalized = 1 + ((rank - max_rank) / (min_rank - max_rank)) * 99`
   - Edge case: If min == max, use 50.0

5. **File Structure Discovery**:
   - players.csv columns: id, name, team, position, bye_week, fantasy_points, injury_status, drafted, locked, average_draft_position, player_rating, week_1_points through week_17_points
   - players_projected.csv columns: id, name, week_1_points through week_17_points
   - Join key: `id` column (both files have it)

6. **Important Note**:
   - User requests player_rating based on ADP (different from codebase pattern that uses positional ranking)
   - Need to clarify if this is intentional deviation from existing pattern

**Questions Identified for User**:
1. The existing codebase calculates player_rating from ESPN positional rankings, not ADP. Should we use ADP as requested, or follow existing pattern?
2. ~~For player_rating formula: should lowest ADP be 100 (best) or 0?~~ **RESOLVED**: User confirmed lowest ADP = 100 (best player)
3. Output column order - should it match players.csv exactly?
4. Should the script be a one-time utility or integrated into the player-data-fetcher pipeline?
5. Where should the script be placed - root level or in a utility folder?

---

#### Iteration 2: Deep Dive Verification ✅
**Completed**: Yes

**Additional Research Findings**:

1. **Script Template Found**: `simulation/normalize_player_ratings.py`
   - Perfect template for a one-time utility script
   - Uses proper logging, error handling, pandas operations
   - Follows project patterns for Path handling, error_context

2. **Run Script Pattern**: `run_player_fetcher.py`
   - Root-level runner scripts use subprocess to call module scripts
   - For simple utilities, direct execution is also acceptable

3. **Test Pattern**: `tests/utils/test_csv_utils.py`
   - Uses pytest fixtures with `tmp_path` for temp file creation
   - Each test class covers one function
   - Uses `pytest.raises` for error assertions
   - Creates sample CSVs with pandas DataFrames

4. **Key Implementation Details**:
   - Script should be at project root: `generate_players_week1.py`
   - Or in utils: `utils/generate_players_week1.py`
   - Test file: `tests/utils/test_generate_players_week1.py`
   - Use pandas for merging DataFrames on 'id' column

5. **Edge Cases to Handle**:
   - Players in players.csv but not in players_projected.csv (or vice versa)
   - Missing/NaN ADP values
   - Division by zero (all players in position have same ADP)
   - Positions with only one player

**Data Flow Clarification**:
- players.csv has week data that is ACTUAL performance (historical)
- players_projected.csv has week data that is PROJECTED performance
- User wants players_week1.csv to use PROJECTED week data

---

#### Iteration 3: Deep Dive Verification ✅
**Completed**: Yes

**Integration and Edge Case Analysis**:

1. **ID Matching Verified**:
   - players.csv: 710 unique IDs
   - players_projected.csv: 710 unique IDs
   - 100% overlap - no orphan records
   - No NaN ADP values found

2. **Column Order** (from players.csv):
   ```
   id, name, team, position, bye_week, fantasy_points, injury_status,
   drafted, locked, average_draft_position, player_rating,
   week_1_points ... week_17_points
   ```

3. **Formula Verification** (user clarified):
   - Formula: `rating = 100 * (max_adp - player_adp) / (max_adp - min_adp)`
   - Lowest ADP (e.g., RB with 5.09) → 100 (best)
   - Highest ADP (e.g., RB with 170.06) → 0 (worst)
   - This aligns with: lower ADP = drafted earlier = better player

4. **Existing Pattern Match**:
   - Existing codebase uses ESPN positional rankings, not ADP
   - User explicitly wants ADP-based calculation for this file
   - This is an intentional deviation for simulation purposes

**Questions Remaining**:
- Q1 (ADP vs rankings): Still needs user confirmation
- Q3 (Column order): Assume match players.csv exactly
- Q4 (One-time vs pipeline): Likely one-time utility
- Q5 (Script location): Root level recommended

---

#### Iteration 4: Enhanced Technical Detail ✅
**Completed**: Yes

**Implementation-Specific Details**:

1. **Formula Validation** (tested with real data):
   ```python
   # QB example:
   # Josh Allen (ADP=20.67) → rating = 100.00 ✅
   # Worst QB (ADP=170.00) → rating = 0.00 ✅

   rating = 100 * (max_adp - player_adp) / (max_adp - min_adp)
   ```

2. **Fantasy Points Calculation**:
   ```python
   week_cols = [f'week_{i}_points' for i in range(1, 18)]
   fantasy_points = df[week_cols].sum(axis=1)
   # Example: Jahmyr Gibbs → 311.47 total projected points
   ```

3. **Merge Strategy**:
   ```python
   # Merge on 'id' column (inner join since 100% overlap confirmed)
   merged = players_df.merge(projected_df, on='id', suffixes=('', '_proj'))
   ```

4. **Output Column Selection**:
   ```python
   output_columns = [
       'id', 'name', 'team', 'position', 'bye_week',
       'fantasy_points',  # CALCULATED
       'injury_status',   # DEFAULT: 'ACTIVE'
       'drafted',         # DEFAULT: 0
       'locked',          # DEFAULT: 0
       'average_draft_position',
       'player_rating',   # CALCULATED from ADP
       # Week columns from projected file
       'week_1_points', 'week_2_points', ... 'week_17_points'
   ]
   ```

5. **Performance Considerations**:
   - Use pandas vectorized operations for calculations
   - GroupBy for position-based ADP normalization
   - Single pass through data sufficient

---

#### Iteration 5: SKEPTICAL RE-VERIFICATION ✅
**Completed**: Yes

**Fresh Verification Results**:

1. **File Verification** ✅:
   - players.csv: 710 rows, exists
   - players_projected.csv: 710 rows, exists

2. **Column Names Verified** ✅:
   - players.csv: id, name, team, position, bye_week, fantasy_points, injury_status, drafted, locked, average_draft_position, player_rating, week_1_points...week_17_points
   - players_projected.csv: id, name, week_1_points...week_17_points

3. **Data Types** ✅:
   - id: int64 (both files, compatible)
   - average_draft_position: float64

4. **Week Column Content Difference Verified** ✅:
   - Player 4429795 (Jahmyr Gibbs):
     - players.csv week_1_points: 15.00 (ACTUAL)
     - projected.csv week_1_points: 18.42 (PROJECTED)
   - Confirmed: using projected data is correct

5. **Position Values** ✅:
   - Exactly 6 positions: RB, WR, QB, TE, K, DST

6. **ADP Data Quality** ✅:
   - No NaN values
   - No negative values
   - Range: 5.09 to 170.10

7. **Formula Correctness Re-verified** ✅:
   - Best RB (ADP=5.09) → rating = 100.00
   - Worst RB (ADP=170.06) → rating = 0.00

**Corrections Made**: None - all prior assumptions were correct.

**Confidence Level**: HIGH - All claims validated with fresh codebase research.

---

### First Verification Round Summary
- **Total Iterations**: 5/5 ✅
- **Skeptical Re-verification**: Complete ✅
- **Requirements Coverage**: All requirements from original specification covered
- **Key Patterns Identified**:
  - Use `simulation/normalize_player_ratings.py` as template
  - Follow `tests/utils/test_csv_utils.py` test patterns
  - Use pandas for merging and calculations
- **Questions for User**: 4 remaining (see questions file)

---

## User Answers Received ✅

1. **player_rating method**: Use ADP as requested
2. **Output file location**: `data/players_week1.csv`
3. **Script location**: Root-level `generate_players_week1.py`
4. **Column order**: Match `players.csv` exactly

---

## Second Verification Round (7 iterations)

#### Iterations 6-9: Standard Verification with User Answers ✅
**Completed**: Yes

**Implementation Details Verified**:

1. **Column Order** (28 columns total):
   - Metadata: id, name, team, position, bye_week, fantasy_points, injury_status, drafted, locked, average_draft_position, player_rating
   - Week data: week_1_points through week_17_points

2. **Merge Strategy Verified**:
   - Inner join on 'id' column produces 710 rows (100% match)
   - Need to handle duplicate 'name' column (name_proj) after merge
   - Solution: Select only required columns after merge

3. **Calculations Verified**:
   - fantasy_points = sum of week_1_points through week_17_points from projected
   - player_rating per position: `100 * (max_adp - player_adp) / (max_adp - min_adp)`
   - All positions achieve 0.00 to 100.00 range

4. **Pandas Warning to Address**:
   - FutureWarning about groupby.apply() on grouping columns
   - Solution: Use `include_groups=False` in apply()

---

#### Iteration 10: SKEPTICAL RE-VERIFICATION ✅
**Completed**: Yes

**Fresh Verification Results**:

1. **Requirements Re-check** ✅:
   - All 4 original requirements still correctly captured
   - User answers correctly integrated

2. **Implementation Issue Found** ✅:
   - After merge, duplicate 'name_proj' column appears
   - Solution: Select only the 28 required columns in exact order

3. **All Claims Verified** ✅:
   - File paths correct
   - Column names correct
   - Data types compatible
   - Formula produces expected results

**Corrections Made**:
- Added explicit column selection to avoid duplicate columns after merge
- Need to use `include_groups=False` to avoid pandas warning

---

#### Iterations 11-12: Final Preparation ✅
**Completed**: Yes

**Final Implementation Plan**:

1. **Script**: `generate_players_week1.py` at project root
2. **Test File**: `tests/root_scripts/test_generate_players_week1.py`
3. **Output**: `data/players_week1.csv`

**Implementation Steps**:
```python
# 1. Load source files
players_df = pd.read_csv('data/players.csv')
projected_df = pd.read_csv('data/players_projected.csv')

# 2. Merge on 'id' - get required columns from each
merged = players_df[['id', 'name', 'team', 'position', 'bye_week', 'average_draft_position']].merge(
    projected_df[['id'] + week_cols], on='id'
)

# 3. Calculate fantasy_points (sum of weeks from projected)
merged['fantasy_points'] = merged[week_cols].sum(axis=1)

# 4. Set default values
merged['injury_status'] = 'ACTIVE'
merged['drafted'] = 0
merged['locked'] = 0

# 5. Calculate player_rating per position (using transform to avoid warning)
def calc_position_rating(adp, min_adp, max_adp):
    if min_adp == max_adp:
        return 50.0
    return 100 * (max_adp - adp) / (max_adp - min_adp)

merged['player_rating'] = merged.groupby('position')['average_draft_position'].transform(
    lambda x: calc_position_rating(x, x.min(), x.max())
)

# 6. Select columns in exact order
output_cols = ['id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
               'injury_status', 'drafted', 'locked', 'average_draft_position',
               'player_rating'] + week_cols
output_df = merged[output_cols]

# 7. Write to CSV
output_df.to_csv('data/players_week1.csv', index=False)
```

---

### Second Verification Round Summary
- **Total Iterations**: 12/12 ✅
- **Both Skeptical Re-verifications**: Complete ✅
- **All Requirements Covered**: Yes
- **All User Answers Integrated**: Yes
- **Implementation Ready**: Yes
