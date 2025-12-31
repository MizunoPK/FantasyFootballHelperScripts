# Feature 01: week_18_data_folder_creation

**Part of Epic:** bug_fix-compile-historical-data-missing-final-week-stats
**Feature Number:** 1 of 2
**Created:** 2025-12-31
**Last Updated:** 2025-12-31 12:02

---

## Objective

Update the compile historical data script to create a week_18 folder containing week 17 actual player performance results, maintaining the consistent data flow pattern where week_N+1 contains actual results from week_N.

---

## Current System Analysis

### Files Identified

**Main Script:**
- `compile_historical_data.py` (root level)
  - Line 113-147: `create_output_directories()` creates week folders
  - Line 142-144: Loop `for week in range(1, REGULAR_SEASON_WEEKS + 1)` creates week_01 through week_17
  - Line 209: Calls `generate_weekly_snapshots()` to populate data

**Constants Module:**
- `historical_data_compiler/constants.py`
  - Line 88: `REGULAR_SEASON_WEEKS = 17` (controls folder creation)

**Snapshot Generator:**
- `historical_data_compiler/weekly_snapshot_generator.py`
  - Line 119-138: `generate_all_weeks()` generates snapshots
  - Line 135: Loop `for week in range(1, REGULAR_SEASON_WEEKS + 1)` generates weeks 1-17
  - Line 140-177: `_generate_week_snapshot()` creates individual week data

### Current Data Flow

**Folder Structure Created:**
```
simulation/sim_data/{YEAR}/weeks/
├── week_01/
├── week_02/
...
└── week_17/  ← Last folder (contains week 17 PROJECTIONS)
```

**Week N Snapshot Contains:**
- `players.csv` - Actual points for weeks 1 to N-1, projected for N to 17
- `players_projected.csv` - Point-in-time projections
- Position JSON files: `qb_data.json`, `rb_data.json`, etc.

**The Problem:**
- Week 17 folder has PRE-GAME projections for week 17
- No week_18 folder exists to contain ACTUAL results from week 17
- Pattern breaks: week_N+1 should have actuals from week_N

---

## Scope

**What's included in THIS feature:**
- Update `compile_historical_data.py` to create week_18 folder
- Update `weekly_snapshot_generator.py` to generate week_18 snapshot
- Week_18 snapshot will contain week 17 actual results
- Maintain data format consistency with existing week folders
- Support both CSV and JSON output formats
- Ensure existing functionality unchanged (weeks 1-17)

**What's NOT included:**
- Simulation system changes (that's Feature 02)
- Validation of simulation data usage (that's Feature 02)
- Changes to data fetching APIs (out of scope - data already fetched)
- Changing NFL season structure (17 weeks is correct)

---

## Components Affected

**Files to Modify:**

1. **`historical_data_compiler/constants.py`**
   - **Change:** Add new constant `VALIDATION_WEEKS = 18`
   - **Keep:** `REGULAR_SEASON_WEEKS = 17` (unchanged - semantically correct)
   - **Rationale:** Separate constants for "regular season weeks" vs "weeks to generate for validation"

2. **`compile_historical_data.py`**
   - Method: `create_output_directories()` (lines 113-147)
   - **Change:** Update line 142 loop to use `VALIDATION_WEEKS` instead of `REGULAR_SEASON_WEEKS`
   - **Result:** Creates week_01 through week_18 folders

3. **`historical_data_compiler/weekly_snapshot_generator.py`**
   - Method: `generate_all_weeks()` (lines 119-138)
   - **Change:** Update line 135 loop to use `VALIDATION_WEEKS` instead of `REGULAR_SEASON_WEEKS`
   - **Result:** Generates snapshots for weeks 1-18
   - Method: `_generate_week_snapshot()` (lines 140-177)
   - **Change:** Add special case for week 18 - use all actuals, no projections
   - **Logic:** `if current_week == 18: populate with actuals 1-17 only`

**No Changes Needed:**
- `player_data_fetcher.py` - Already fetches complete season data
- `json_exporter.py` - Automatically works for week 18 (no changes needed)
- `schedule_fetcher.py` - Schedule already complete
- `game_data_fetcher.py` - Game data already complete

**Note:** Week 18 uses same file generation logic as weeks 1-17, just with special data content (all actuals)

---

## Dependencies

**Prerequisites:** None (foundation feature)

**Blocks:** Feature 02 (simulation data flow validation requires week_18 to exist)

**External Dependencies:**
- Player data must be fetched through week 17 (already working)
- ESPN API provides actual points for all 17 weeks (already working)

---

## Implementation Approach (CONFIRMED)

**Constant Strategy:**
- Add `VALIDATION_WEEKS = 18` constant to `constants.py`
- Keep `REGULAR_SEASON_WEEKS = 17` (semantically correct - NFL regular season)
- Use `VALIDATION_WEEKS` for folder creation and snapshot generation
- Week 18 = validation week containing week 17 actuals

**Rationale:**
- Semantically clear: Regular season IS 17 weeks, validation needs 18
- Safe: No risk of breaking code that uses REGULAR_SEASON_WEEKS
- Maintainable: Clear intent in code

**Week 18 Data Content:**
- Week 18 `players.csv`: Actual points for weeks 1-17 ONLY (no projections)
- Week 18 `players_projected.csv`: Same as players.csv (all actuals, no projections)
- Both files identical for week 18 (season is over, no future weeks to project)
- Maintains file format compatibility (same CSV columns as other weeks)

**Rationale:**
- Season ends after week 17 - no future weeks exist
- Simplest for simulation validation (just read actual values)
- Clear semantics: week_18 = final season actuals

**Week 18 File Format:**
- Week 18 generates same files as weeks 1-17:
  - CSV files: `players.csv`, `players_projected.csv`
  - JSON files: `qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`
- Complete consistency with other week folders
- Controlled by same GENERATE_CSV and GENERATE_JSON flags

**Rationale:**
- Perfect consistency with weeks 1-17 (no special cases)
- No additional complexity (existing logic handles it)
- Future-proof for any tools that consume week_18 data

## Open Questions

**🚨 REMAINING QUESTIONS:**

See `checklist.md` for detailed questions that need user confirmation.

Remaining questions:
1. ~~Constant modification approach~~ ✅ RESOLVED (Option B - VALIDATION_WEEKS)
2. ~~Week 18 snapshot content~~ ✅ RESOLVED (Option A - All actuals, no projections)
3. ~~File format requirements~~ ✅ RESOLVED (Option A - Full format)

**ALL QUESTIONS RESOLVED** - Ready to proceed with implementation planning

---

## Estimates

- Implementation items: ~15-20 (will refine after questions resolved)
- Risk level: MEDIUM (need to understand constant impact on system)
- Priority: HIGH (Feature 02 depends on this)

---

## Testing Strategy

**Will define after questions resolved - test strategy depends on implementation approach**

Likely tests:
- Unit test: `create_output_directories()` creates week_18
- Unit test: `generate_all_weeks()` generates week_18
- Unit test: Week_18 contains week 17 actuals
- Integration test: Full compile script creates week_18
- Integration test: Week_18 data format matches other weeks

---

## Change Log

| Date | Changed By | What Changed | Why |
|------|------------|--------------|-----|
| 2025-12-31 | Agent | Initial spec created | Stage 1 (Epic Planning) |
| 2025-12-31 | Agent | Added technical details from research | Stage 2 Phase 1 (Targeted Research) |
| 2025-12-31 | Agent | Updated with Question 1 answer (Option B) | Stage 2 Phase 3 (Question Resolution) |
| 2025-12-31 | Agent | Updated with Question 2 answer (Option A) | Stage 2 Phase 3 (Question Resolution) |
| 2025-12-31 | Agent | Updated with Question 3 answer (Option A) | Stage 2 Phase 3 (Question Resolution) |

---

**Status:** Stage 2 Phase 1 complete (Targeted Research)
**Next:** Phase 2 - Create checklist.md with open questions, then ask user ONE question at a time
