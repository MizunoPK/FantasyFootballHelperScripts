# Feature 01: week_18_data_folder_creation - Discovery Findings

**Research Date:** 2025-12-31
**Researcher:** Agent

---

## Components Identified

**Main Script:**
- `compile_historical_data.py` (root level)
  - Lines 113-147: `create_output_directories()` - Creates week_01 through week_17 folders
  - Lines 142-144: Loop creates folders based on `REGULAR_SEASON_WEEKS` constant
  - Line 209: Calls `generate_weekly_snapshots()` to generate data

**Constants Module:**
- `historical_data_compiler/constants.py`
  - Line 88: `REGULAR_SEASON_WEEKS = 17` - **KEY CONSTANT**
  - This constant controls how many week folders are created

**Weekly Snapshot Generator:**
- `historical_data_compiler/weekly_snapshot_generator.py`
  - Lines 119-138: `generate_all_weeks()` - Generates snapshots for weeks 1-17
  - Line 135: Loop uses `REGULAR_SEASON_WEEKS` constant
  - Lines 140-177: `_generate_week_snapshot()` - Creates individual week snapshot
  - Creates both CSV and JSON files for each week

---

## Current Data Flow

**Week Folder Creation:**
```python
# compile_historical_data.py, line 142-144
for week in range(1, REGULAR_SEASON_WEEKS + 1):
    week_dir = weeks_dir / f"week_{week:02d}"
    week_dir.mkdir(exist_ok=True)
```

Result: Creates week_01, week_02, ..., week_17

**Snapshot Generation:**
```python
# weekly_snapshot_generator.py, line 135
for week in range(1, REGULAR_SEASON_WEEKS + 1):
    self._generate_week_snapshot(players, weeks_dir, week)
```

Result: Generates data for weeks 1-17

**Week N Snapshot Contains:**
- `players.csv`: Actual points for weeks 1 to N-1, projected for N to 17
- `players_projected.csv`: All projected values
- Position-specific JSON files

**The Problem:**
- Week 17 folder has projections for week 17 (pre-game data)
- No week 18 folder exists to contain ACTUAL week 17 results
- Pattern breaks: week_N+1 should have actuals from week_N, but week_18 doesn't exist

---

## Data Structure

**Week Snapshot Contents:**
Each week_NN folder contains:
- `players.csv` - Smart values (actuals for past, projections for future)
- `players_projected.csv` - Point-in-time projections
- `qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`

**Output Directory Structure:**
```
simulation/sim_data/{YEAR}/
├── season_schedule.csv
├── game_data.csv
├── team_data/{32 team CSVs}
└── weeks/
    ├── week_01/
    ├── week_02/
    ...
    └── week_17/  ← CURRENT: Last folder
        └── week_18/  ← NEEDED: Week 17 actuals
```

---

## Edge Cases Identified

1. **Week 18 is not a regular season week**
   - NFL regular season is 17 weeks (2021+)
   - Week 18 folder would contain week 17 ACTUALS, not week 18 projections
   - Week 18 folder is special-purpose (validation only)

2. **Data for week 18 snapshot**
   - Should contain all ACTUAL points through week 17
   - No projections needed (season over)
   - Still need to maintain same file structure for consistency

3. **Constant modification vs special case**
   - Option A: Change `REGULAR_SEASON_WEEKS` to 18 (affects entire system?)
   - Option B: Create week_18 as special case (separate logic)
   - Need to understand impact on other parts of system

4. **JSON vs CSV generation**
   - Both formats supported via flags `GENERATE_CSV`, `GENERATE_JSON`
   - Week 18 should support both formats for consistency

---

## Integration Points

**Files to Modify:**
1. `compile_historical_data.py`
   - `create_output_directories()` - Add week_18 folder creation

2. `historical_data_compiler/weekly_snapshot_generator.py`
   - `generate_all_weeks()` - Generate week_18 snapshot
   - `_generate_week_snapshot()` - Handle week_18 special case

3. Potentially `historical_data_compiler/constants.py`
   - May need to add `VALIDATION_WEEK = 18` constant
   - OR modify `REGULAR_SEASON_WEEKS` (requires impact analysis)

**No changes needed for:**
- `player_data_fetcher.py` - Already fetches full season data
- `json_exporter.py` - Should work automatically if snapshot generator is updated

---

## Questions for User

1. **Constant modification approach:**
   - Should we modify `REGULAR_SEASON_WEEKS` to 18?
   - Or create separate logic for week_18 as validation-only folder?
   - Impact: Does changing REGULAR_SEASON_WEEKS affect other parts of the system?

2. **Week 18 snapshot content:**
   - Week 18 should contain ALL actuals through week 17, with NO projections?
   - Or should it follow the same pattern (actuals 1-17, projections for 18+)?

3. **File format consistency:**
   - Week 18 should generate same files as other weeks (CSV + JSON)?
   - Or minimal set for validation only?

---

## Testing Strategy

**Unit Tests:**
- Test `create_output_directories()` creates week_18 folder
- Test `generate_all_weeks()` generates week_18 snapshot
- Test week_18 contains week 17 actuals

**Integration Tests:**
- Run compile_historical_data.py and verify week_18 exists
- Verify week_18 data format matches other weeks
- Verify week_18 contains correct actual values

---

## Next Steps

1. Create checklist.md with open questions
2. Update spec.md with technical details (after user confirms approach)
3. Ask user ONE question at a time to resolve uncertainties
