# Bug Fix Specification: Wrong Data Folder

**Created:** 2025-12-31
**Priority:** HIGH
**Status:** Stage 2 Complete - Ready for Stage 5a

---

## Bug Summary

**Current Behavior (WRONG):**
- Feature 2 updates `data/player_data/*.json` (6 files)
- Main league helper data files

**Expected Behavior (CORRECT):**
- Feature 2 updates `simulation/sim_data/2025/weeks/week_XX/*.json`
- All 18 weeks (week_01 through week_18)
- 6 position files per week: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
- Total: 108 files (18 weeks × 6 positions)

**Root Cause:**
- Epic scope misunderstood during planning
- Feature 2 (utils/adp_updater.py) hardcoded to wrong path
- All tests validated wrong folder

---

## Technical Requirements

### 1. File Structure Differences

**OLD (data/player_data/qb_data.json):**
```json
{
  "qb_data": [
    {"id": "123", "name": "Josh Allen", "average_draft_position": 170.0, ...}
  ]
}
```

**NEW (simulation/sim_data/2025/weeks/week_01/qb_data.json):**
```json
[
  {"id": "3918298", "name": "Josh Allen", "average_draft_position": 170.0, ...}
]
```

**Key Difference:** Simulation files are **direct JSON arrays** (NOT wrapped in position key)

---

### 2. Required Changes to Feature 2 (utils/adp_updater.py)

**Current Function Signature:**
```python
def update_player_adp_values(
    adp_df: pd.DataFrame,
    data_folder: Path
) -> Dict[str, Any]:
    """
    Update player ADP values in JSON files.

    Args:
        adp_df: DataFrame with columns ['player_name', 'adp', 'position']
        data_folder: Path to data folder (currently expects data/)
    """
```

**New Function Signature:**
```python
def update_player_adp_values(
    adp_df: pd.DataFrame,
    sim_data_folder: Path
) -> Dict[str, Any]:
    """
    Update player ADP values in simulation JSON files across all weeks.

    Args:
        adp_df: DataFrame with columns ['player_name', 'adp', 'position']
        sim_data_folder: Path to simulation data folder (simulation/sim_data/2025/weeks/)
    """
```

**Required Logic Changes:**

1. **Iterate through all week folders:**
   - Discover week folders dynamically (week_01, week_02, ..., week_18)
   - Process each week folder sequentially
   - Log progress per week

2. **Handle direct JSON array structure:**
   - Load: `json.load(f)` returns list directly (not dict with position key)
   - Update: Modify list elements directly
   - Save: Write list directly (not wrapped in dict)

3. **Maintain atomic writes per file:**
   - Write to `.tmp` file first
   - Replace original on success
   - 108 atomic operations total (18 weeks × 6 positions)

4. **Updated match report:**
   - Report should aggregate across all weeks
   - Show per-week statistics (optional)
   - Final summary shows total matched/unmatched

---

### 3. Required Changes to Unit Tests

**File:** `tests/utils/test_adp_updater.py` (18 tests)

**Current Test Structure:**
- Uses `tmp_path` to create mock `data/player_data/` structure
- Creates wrapped JSON: `{"qb_data": [...]}`
- Tests single folder update

**New Test Structure:**
- Create mock `simulation/sim_data/2025/weeks/` structure
- Create multiple week folders (week_01, week_02, etc.)
- Create direct JSON arrays (no wrapper)
- Test multi-week updates
- Verify all weeks get updated consistently

**New Test Cases Needed:**
1. `test_updates_all_week_folders` - Verify all 17 weeks updated
2. `test_handles_direct_array_structure` - Verify no wrapper dict
3. `test_per_week_atomic_writes` - Verify each file uses atomic pattern
4. `test_match_report_aggregates_across_weeks` - Verify report combines all weeks

---

### 4. Required Changes to Epic E2E Test

**File:** `feature-updates/fix_2025_adp/epic_e2e_test.py`

**Current Validation:**
- Checks `data/player_data/*.json` files
- Verifies 6 files updated

**New Validation:**
- Checks `simulation/sim_data/2025/weeks/week_XX/*.json` files
- Verifies 102 files updated (17 weeks × 6 positions)
- Random sampling across weeks to verify consistency
- Checks direct array structure

---

### 5. Required Changes to User Test Script

**File:** `feature-updates/fix_2025_adp/test_full_csv.py`

**Current Verification:**
- Shows stats for `data/player_data/` files
- Sample QBs from single file

**New Verification:**
- Shows stats across all 17 weeks
- Sample QBs from random weeks (verify consistency)
- Display per-week update counts
- Verify all weeks have same match rate

---

## Implementation Checklist

**Core Implementation:**
- [ ] 1. Update function to accept sim_data_folder parameter
- [ ] 2. Discover week folders dynamically (glob pattern: week_*)
- [ ] 3. Iterate through each week folder
- [ ] 4. Load JSON as direct array (not wrapped dict)
- [ ] 5. Match players within each week
- [ ] 6. Update ADP values in each week's arrays
- [ ] 7. Write back as direct arrays (atomic writes)
- [ ] 8. Aggregate match report across all weeks
- [ ] 9. Log progress per week (INFO level)

**Testing:**
- [ ] 10. Update unit tests for multi-week structure
- [ ] 11. Update unit tests for direct array structure
- [ ] 12. Add test for all weeks updated
- [ ] 13. Add test for consistent updates across weeks
- [ ] 14. Update epic E2E test validation
- [ ] 15. Update user test script verification

**Documentation:**
- [ ] 16. Update function docstring
- [ ] 17. Update code comments for multi-week logic

---

## Edge Cases & Error Handling

**1. Missing week folders:**
- If fewer than 18 weeks found, log WARNING
- Continue with available weeks

**2. Malformed JSON in week folder:**
- If JSON can't be parsed, FAIL entire operation (all-or-nothing)
- Log ERROR with specific file that failed
- Raise appropriate exception with clear message

**3. Direct JSON array structure:**
- All simulation files use direct arrays (no wrapper dict)
- Load and save as arrays directly
- If wrapper dict found, raise ValueError (unexpected structure)

**4. Permission errors during atomic write:**
- If can't write to any file, FAIL entire operation
- Raise PermissionError with clear message
- Use atomic writes to prevent partial corruption

---

## Acceptance Criteria

1. ✅ All 18 week folders processed (week_01 through week_18)
2. ✅ All 6 position files updated per week (108 total files)
3. ✅ ADP values match FantasyPros CSV data across all weeks
4. ✅ Direct JSON array structure preserved (no wrapper dict)
5. ✅ Atomic writes used for all 102 files
6. ✅ Match report aggregates across all weeks
7. ✅ Unmatched players retain default ADP 170.0 in all weeks
8. ✅ Unit tests pass (100%)
9. ✅ Epic E2E test validates all weeks
10. ✅ User test script verifies correct folders

---

## Open Questions (checklist.md)

{To be populated during deep dive}
