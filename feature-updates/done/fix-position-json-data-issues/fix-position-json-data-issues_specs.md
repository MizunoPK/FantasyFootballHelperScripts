# Fix Position JSON Data Issues

## Objective

Fix four critical data quality issues in the position JSON export feature that make it non-functional despite passing all QC rounds. The feature has correct structure but wrong data semantics, producing zeros for all stats and identical projected/actual arrays.

---

## High-Level Requirements

### Issue #1: File Naming - Remove Timestamps and Prefix

**Current Behavior (WRONG):**
- Files: `new_qb_data_20251224_133017.json`, `new_rb_data_20251224_133017.json`, etc.
- Location: `feature-updates/` folder
- Files accumulate with each run (12 files from 2 runs instead of 6)
- "new_" prefix not needed
- Timestamps not needed

**Required Behavior (CORRECT):**
- Files: `qb_data.json`, `rb_data.json`, `wr_data.json`, `te_data.json`, `k_data.json`, `dst_data.json`
- Location: `data/player_data/` folder (subdirectory of root data folder)
- Each run overwrites previous files
- No timestamps, no prefix
- Matches pattern of `players.csv` (not `players_TIMESTAMP.csv`)

**Rationale:**
- Files represent current state of player data
- No need for historical versions (git provides version control)
- Simpler for downstream consumers (always read same filename)
- Prevents file accumulation
- Consistent with other output files (`data/players.csv`, `data/team_data/*.csv`)

**Technical Details:**
- Location: `player-data-fetcher/player_data_exporter.py` line 454
- Current: Uses `DataFileManager.save_json_data(output_data, prefix, create_latest=False)`
- DataFileManager adds timestamps by default
- Prefix is "new_{position}_data"
- **Fix:** Write files directly using same pattern as `players.csv` export (lines 678-708)
  - Path: `Path(__file__).parent / '../data/{position}_data.json'`
  - Direct write with `open()` or `aiofiles.open()`
  - No DataFileManager, no timestamps, no caps

---

### Issue #2: Projected Points - Use ESPN Pre-Game Projections

**Current Behavior (WRONG):**
- `projected_points` array contains IDENTICAL values to `actual_points` for all 16 completed weeks
- Both arrays use same data source (actual results)
- Example: Josh Allen Week 1-5
  - projected_points: [38.76, 11.82, 23.02, 24.86, 19.42]
  - actual_points: [38.76, 11.82, 23.02, 24.86, 19.42]
  - **IDENTICAL - THIS IS THE BUG**

**Required Behavior (CORRECT):**
- `projected_points` should contain what ESPN predicted BEFORE the game
- `actual_points` should contain what actually happened in the game
- Arrays should be DIFFERENT (players rarely score exactly what was projected)
- Example: Josh Allen Week 1
  - projected_points[0]: 25.5 (pre-game ESPN projection)
  - actual_points[0]: 38.76 (what actually happened)

**Data Sources:**
- Projected points (pre-game): ESPN `stats[week].stats` (statSourceId=1)
- Actual points (post-game): ESPN `stats[week].appliedStats` (statSourceId=0)

**Technical Details:**
- Location: `player-data-fetcher/player_data_exporter.py` lines 535-578
- `_get_projected_points_array()` currently uses `player.week_{week}_points`
- `_get_actual_points_array()` currently uses `espn_data.week_{week}_points`
- Both use same source (actual results)
- Fix: Extract projected from statSourceId=1, actual from statSourceId=0
- Calculate fantasy points from stat values using scoring settings

**Rationale:**
- This is a PRIMARY USE CASE of the feature (compare projections vs actuals)
- Critical for analyzing projection accuracy
- Without this, feature provides no value for accuracy analysis

---

### Issue #3: Stat Arrays - Implement ESPN Stat Extraction

**Current Behavior (WRONG):**
- ALL stat arrays filled with zeros for ALL weeks (including 16 completed weeks)
- Example: Josh Allen (QB with 16 completed games)
  - passing.completions: [0.0, 0.0, 0.0, 0.0, 0.0, ...]  # ALL ZEROS
  - passing.yards: [0.0, 0.0, 0.0, 0.0, 0.0, ...]        # ALL ZEROS
  - passing.tds: [0.0, 0.0, 0.0, 0.0, 0.0, ...]          # ALL ZEROS
- 7 TODO comments in code indicating deferred work
- Comments reference correct stat IDs but return zeros
- Feature marked as "partial" in QC with "low impact" assessment

**Required Behavior (CORRECT):**
- Stat arrays should contain actual weekly statistics from ESPN
- Example: Josh Allen weeks 1-7 (week 7 is bye)
  - passing.completions: [23, 19, 18, 20, 22, 24, 0, ...]
  - passing.yards: [232, 180, 258, 215, 280, 323, 0, ...]
  - passing.tds: [2, 0, 2, 1, 3, 3, 0, ...]
- Week 7 (index 6) = 0 (bye week)
- Week 17 (index 16) = 0 (not yet played)
- Weeks 1-6, 8-16 = real stat values from ESPN

**Data Source:**
- ESPN `stats[week].appliedStats` dictionary (statSourceId=0)
- Keys are stat IDs: '0' = passing attempts, '1' = completions, '3' = yards, '4' = TDs, etc.
- All 31 stat IDs already researched and documented in `FINAL_STAT_RESEARCH_COMPLETE.md`

**Implementation Required:**
Remove all 7 TODO comments and implement stat extraction in:
1. `_extract_passing_stats()` (line 580-591)
2. `_extract_rushing_stats()` (line 593-601)
3. `_extract_receiving_stats()` (line 603-612)
4. `_extract_misc_stats()` (line 614-637)
5. `_extract_kicking_stats()` (line 639-652)
6. `_extract_defense_stats()` (line 654-669)
7. `_get_actual_points_array()` (line 572 - remove TODO)

**Stat ID Mappings (Already Documented):**
- Passing: stat_0 (attempts), stat_1 (completions), stat_3 (yards), stat_4 (TDs), stat_20 (INT), stat_64 (sacks)
- Rushing: stat_23 (attempts), stat_24 (yards), stat_25 (TDs)
- Receiving: stat_53 (receptions), stat_58 (targets), stat_42 (yards), stat_43 (TDs)
- Kicking: stat_83 (FG made), stat_85 (FG missed), stat_86 (XP made), stat_88 (XP missed)
- Defense: stat_95 (INT), stat_96 (fumbles recovered), stat_98 (safety), stat_99 (sacks), stat_94 (def TD), stat_120 (pts against), stat_127 (yds against), stat_114+115 (return yds), stat_101+102 (return TDs)
- Misc: stat_68 (fumbles), stat_19+26+44+62 (2-pt conversions by position)

**Rationale:**
- This is the ENTIRE PURPOSE of the detailed stat arrays
- Users need week-by-week passing yards, rushing TDs, receptions, etc.
- Critical for detailed player analysis
- Without this data, JSON files are far less useful than CSV
- **Feature cannot achieve primary use case without this**

---

### Issue #4: Complete Deferred Work - Use Researched Stat IDs

**Context:**
- All 31 ESPN stat IDs were researched and documented during original feature planning
- Implementation code includes comments referencing these stat IDs
- Code was shipped with placeholder zeros and TODO comments
- QC accepted this as "partial work" with "low impact"
- **This demonstrates the exact process failure the recent guide updates were designed to prevent**

**Required:**
- Remove ALL TODO comments from production code
- Remove "Placeholder implementation" comments
- Ensure all researched stat IDs are actually used in implementation
- No deferred work should remain

**This is not new work - it's completing work that was:**
1. ✅ Planned (stat research done)
2. ✅ Researched (all 31 stat IDs documented)
3. ✅ Commented in code (stat IDs referenced)
4. ❌ Never implemented (zeros returned instead)

---

## Files to Modify

### File 1: player-data-fetcher/player_data_models.py

**Add raw_stats field to ESPNPlayerData model:**
```python
class ESPNPlayerData(BaseModel):
    # ... existing fields ...

    # Store raw stats array for stat extraction in position JSON export
    raw_stats: Optional[List[Dict[str, Any]]] = None
```

**Rationale:** Minimal memory overhead, stores only what's needed for stat extraction

---

### File 2: player-data-fetcher/espn_client.py

**Populate raw_stats during parsing (line ~1824):**
```python
projection = ESPNPlayerData(
    id=id,
    name=name,
    # ... other fields ...
    raw_stats=player_info.get('stats', [])  # NEW: Store stats array
)
```

**Rationale:** Capture stats array during initial parsing, no additional API calls needed

---

### File 3: player-data-fetcher/player_data_exporter.py

**Line 454** - Change file saving logic
- Remove DataFileManager usage
- Write directly to `data/player_data/` folder with fixed filenames
- Reuse `players.csv` export pattern (lines 678-708)
- Filenames: `data/player_data/qb_data.json`, `data/player_data/rb_data.json`, etc.

**Lines 535-578** - Fix projected_points and actual_points
- `_get_projected_points_array()`: Extract from `espn_data.raw_stats` (statSourceId=1)
  - Pattern from `compile_historical_data.py`:
    ```python
    for week in range(1, 18):
        projected_points = None
        for stat in espn_data.raw_stats:
            if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 1:
                projected_points = stat.get('appliedTotal')
        projected_points_array.append(projected_points if projected_points else 0.0)
    ```
- `_get_actual_points_array()`: Extract from `espn_data.raw_stats` (statSourceId=0)
  - Pattern from `compile_historical_data.py`:
    ```python
    for week in range(1, 18):
        actual_points = None
        for stat in espn_data.raw_stats:
            if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 0:
                actual_points = stat.get('appliedTotal')
        actual_points_array.append(actual_points if actual_points else 0.0)
    ```
- **Key:** TWO stat entries per week - statSourceId=0 (actual) and statSourceId=1 (projected)
- **Both use `appliedTotal`** - the difference is which stat entry you read from
- Remove TODO comment on line 572

**Lines 580-669** - Implement stat extraction (remove 6 TODO placeholders)
- All methods now extract from `espn_data.raw_stats` array
- Use helper method `_extract_stat_value(raw_stats, week, stat_id)` to get individual stat values
- Methods to update:
  - `_extract_passing_stats()` (lines 580-591)
  - `_extract_rushing_stats()` (lines 593-601)
  - `_extract_receiving_stats()` (lines 603-612)
  - `_extract_misc_stats()` (lines 614-637) - **REMOVE two_pt field** (decision: not worth complexity)
  - `_extract_kicking_stats()` (lines 639-652)
  - `_extract_defense_stats()` (lines 654-669)

**Add new helper methods:**
```python
def _extract_stat_value(self, raw_stats: List[Dict], week: int, stat_id: str) -> float:
    """Extract a single stat value from raw_stats array for a specific week.

    Pattern from compile_historical_data.py:
    - Find stat entry with scoringPeriodId == week AND statSourceId == 0
    - Extract from appliedStats dict using stat_id as string key
    - Return 0.0 if not found
    """
    for stat in raw_stats:
        if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 0:
            applied_stats = stat.get('appliedStats', {})
            value = applied_stats.get(stat_id, 0.0)
            return float(value) if value else 0.0
    return 0.0

def _extract_combined_stat(self, raw_stats: List[Dict], week: int, stat_ids: List[str]) -> float:
    """Sum multiple stat IDs (for return yards, 2PT conversions, etc.)."""
    total = 0.0
    for stat_id in stat_ids:
        total += self._extract_stat_value(raw_stats, week, stat_id)
    return total
```

---

## Implementation Summary

### Data Flow (After Fix)

```
ESPN API
  ↓
espn_client.py parses response
  ↓ (stores stats array)
ESPNPlayerData(raw_stats=[...])
  ↓
player_data_exporter.py
  ↓ (extracts from raw_stats)
Position JSON files with real data
  ↓
Written to data/player_data/qb_data.json, etc.
```

### Key Changes

1. **ESPNPlayerData model:** Add `raw_stats` field
2. **ESPN parsing:** Populate `raw_stats` during initial parse
3. **Projected points:** Extract from raw_stats with statSourceId=1, use `appliedTotal`
4. **Actual points:** Extract from raw_stats with statSourceId=0, use `appliedTotal`
5. **Stat arrays:** Extract from raw_stats statSourceId=0 entry, use `appliedStats` dict
6. **File writing:** Direct write to data/ folder (bypass DataFileManager)

### ESPN API Pattern (from compile_historical_data.py)

**Per Week, Two Stat Entries:**
- Entry 1: `statSourceId=0` → actual game results
  - `appliedTotal`: actual fantasy points
  - `appliedStats`: individual stats (yards, TDs, etc.)
- Entry 2: `statSourceId=1` → pre-game projections
  - `appliedTotal`: projected fantasy points
  - `appliedStats`: projected individual stats (not used)

**Our Usage:**
- `projected_points` array: Extract `appliedTotal` from statSourceId=1 entries
- `actual_points` array: Extract `appliedTotal` from statSourceId=0 entries
- Stat detail arrays: Extract from `appliedStats` dict in statSourceId=0 entries

---

## Testing & Validation Requirements

### 1. Filename Validation
- Verify exact filenames: `data/player_data/qb_data.json`, `data/player_data/rb_data.json`, `data/player_data/wr_data.json`, `data/player_data/te_data.json`, `data/player_data/k_data.json`, `data/player_data/dst_data.json`
- Verify correct location: `data/player_data/` folder (subdirectory of root data folder)
- Verify files overwrite (run twice, count should remain 6 not 12)
- Verify no file accumulation

### 2. Projected vs Actual Points Validation
- Verify `projected_points` ≠ `actual_points` for completed weeks
- Both should have non-zero values for completed non-bye weeks
- Week 17 should have projection but no actual (not yet played)
- Spot-check Josh Allen Week 1 against ESPN website

### 3. Stat Arrays Validation
- Verify stat arrays contain non-zero values for completed weeks
- Verify bye weeks show 0 in all arrays
- Verify future weeks (Week 17) show 0 in all arrays
- Verify stat arrays NOT all zeros
- Spot-check Josh Allen Week 1 passing yards against ESPN website (~232 yards)

### 4. External Source Spot-Check (MANDATORY)
- Manually verify at least one player (Josh Allen) Week 1 stats against ESPN.com
- Confirm passing yards, passing TDs, rushing yards, actual points match
- This is CRITICAL to validate data semantics, not just structure

### 5. All Positions Validation
- Test all 6 positions (QB, RB, WR, TE, K, DST)
- Verify projected ≠ actual for each
- Verify stat arrays not all zeros for each

### 6. Array Length Validation
- Verify all arrays are exactly 17 elements
- Verify for all positions

### 7. Smoke Test
- Run full end-to-end test
- Verify all validation criteria pass
- Document results

---

## Success Criteria

Feature is COMPLETE when ALL of the following are true:

1. ✅ Files named `data/player_data/qb_data.json`, `data/player_data/rb_data.json`, etc. (no timestamps, no "new_" prefix)
2. ✅ Files in `data/player_data/` folder (subdirectory of root data folder)
3. ✅ Files overwrite on each run (no accumulation)
4. ✅ `projected_points` ≠ `actual_points` for completed weeks
5. ✅ All stat arrays contain real ESPN data for completed weeks
6. ✅ Stat arrays show 0 for bye weeks and future weeks
7. ✅ Spot-check against ESPN.com confirms data accuracy
8. ✅ All 6 positions exhibit correct behavior
9. ✅ All arrays exactly 17 elements
10. ✅ NO TODO comments in production code
11. ✅ All unit tests pass (100%)
12. ✅ Feature achieves PRIMARY USE CASE (view detailed stats, compare projections vs actuals)

**CRITICAL:** Feature is NOT complete if it has correct structure but wrong data semantics (the exact problem we're fixing).

---

## Priority

**CRITICAL** - Feature is non-functional without these fixes

**Why Critical:**
1. Feature cannot achieve primary use case (view stats, analyze projections)
2. All research already completed (no blockers)
3. Demonstrates process failure (validates recent guide updates)
4. User cannot use the feature in its current state

---

## Context from Original Feature

### Background
- Original feature: `feature-updates/player-data-fetcher-new-data-format/`
- Feature passed all QC rounds with 94.9% verification score
- Feature was marked "complete" despite having 7 TODO comments
- Feature was accepted with "partial work" as "low impact"
- **This is the FIRST TEST of the new "no partial work" guides**

### What Was Correct in Original Implementation
- File structure (JSON schema, field names, nesting)
- Array lengths (17 elements)
- Field naming ("receiving" not "recieving")
- Return stats only in DST (not in other positions)
- DraftedRosterManager integration
- All 2335 unit tests passing

### What Changed During This Fix
- **REMOVED:** "two_pt" field from misc stats (decision: not worth complexity of aggregating 4 stat IDs)

### What Was Wrong in Original Implementation
- File naming (timestamps added)
- Projected points data source (wrong statSourceId)
- Stat arrays (all zeros, not implemented)
- Deferred work accepted as "partial"

### Key Reference Files
- Stat research: `feature-updates/player-data-fetcher-new-data-format/FINAL_STAT_RESEARCH_COMPLETE.md`
- Current implementation: `player-data-fetcher/player_data_exporter.py`
- QC reports: `feature-updates/player-data-fetcher-new-data-format/qc_round_*.md`
- Requirement verification: `feature-updates/player-data-fetcher-new-data-format/requirement_verification_report.md`

---

## Notes

- This is a DATA QUALITY fix, not a STRUCTURAL fix
- All necessary research already completed
- No new research or investigation needed beyond understanding current implementation
- Fix primarily involves using existing research and removing placeholder code
- **This feature demonstrates EXACTLY why "no partial work" guides were needed**
