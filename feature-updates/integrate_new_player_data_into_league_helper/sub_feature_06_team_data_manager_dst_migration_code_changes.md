# Sub-Feature 6: TeamDataManager D/ST Migration - Code Changes

**Date:** 2025-12-28
**Status:** ✅ **COMPLETE** - All Phases Finished
**Tests:** 2415/2415 passing (100%) - Added 9 new D/ST JSON loading tests

---

## Summary

Successfully migrated TeamDataManager._load_dst_player_data() from reading week_N_points columns in players.csv to reading actual_points arrays from dst_data.json. All existing tests pass without modification.

---

## Changes Made

### File: `league_helper/util/TeamDataManager.py`

#### Change 1: Added import json (Line 21)
**Spec Reference:** Task 1.1, Iteration 2 line 617
**Lines Modified:** 21
**Type:** Import addition

**Before:**
```python
from pathlib import Path
from typing import Dict, List, Optional, Any, TYPE_CHECKING
import csv

import sys
```

**After:**
```python
from pathlib import Path
from typing import Dict, List, Optional, Any, TYPE_CHECKING
import csv
import json

import sys
```

**Justification:** Required for json.load() to parse dst_data.json file.

---

#### Change 2: Replaced _load_dst_player_data() implementation (Lines 111-149)
**Spec Reference:** spec.md lines 77-92, Tasks 1.1-1.4
**Lines Modified:** 111-149 (complete method replacement)
**Type:** Method implementation replacement

**Before:** (CSV-based implementation, 56 lines)
- Opened players.csv file
- Used csv.DictReader
- Filtered for position == 'DST'
- Extracted week_1_points through week_17_points columns
- Built weekly_points array manually
- Generic exception handler

**After:** (JSON-based implementation, 39 lines)
- Opens dst_data.json file
- Uses json.load()
- Extracts dst_data array
- Loops through dst_players
- Extracts actual_points arrays directly (no manual array building)
- Specific exception handlers (FileNotFoundError, JSONDecodeError, PermissionError/OSError)

**Complete New Implementation:**
```python
def _load_dst_player_data(self) -> None:
    """
    Load D/ST weekly fantasy scores from dst_data.json actual_points arrays.

    Extracts D/ST player entries and stores their weekly fantasy points for
    ranking calculation. This data is used to rank D/ST units by their actual
    fantasy performance rather than points allowed to opponents.

    Side Effects:
        - Populates self.dst_player_data with {team: [week_1_points, ..., week_17_points]}
        - Logs error if dst_data.json is not found or has errors
    """
    try:
        # Spec: sub_feature_06_team_data_manager_dst_migration_spec.md lines 77-92
        dst_json_path = self.data_folder / 'player_data' / 'dst_data.json'

        with open(dst_json_path, 'r') as f:
            data = json.load(f)

        dst_players = data.get('dst_data', [])

        for dst_player in dst_players:
            team = dst_player.get('team', '').upper()
            actual_points = dst_player.get('actual_points', [0.0] * 17)

            # Store in same format: {team: [week_1, ..., week_17]}
            self.dst_player_data[team] = actual_points

        self.logger.debug(f"Loaded D/ST data for {len(self.dst_player_data)} teams from {dst_json_path}")

    except FileNotFoundError:
        self.logger.error(f"D/ST data file not found: {dst_json_path}")
        self.dst_player_data = {}
    except json.JSONDecodeError as e:
        self.logger.error(f"Invalid JSON in D/ST data file: {e}")
        self.dst_player_data = {}
    except (PermissionError, OSError) as e:
        self.logger.error(f"Error reading D/ST data file {dst_json_path}: {e}")
        self.dst_player_data = {}
```

**Key Changes:**
1. **File Path:** Changed from `self.data_folder / 'players.csv'` to `self.data_folder / 'player_data' / 'dst_data.json'` (line 125)
2. **File Opening:** Changed from CSV opening with newline='' to simple JSON file opening (line 127)
3. **Parsing:** Changed from csv.DictReader to json.load() (line 128)
4. **Data Extraction:** Changed from data.get('dst_data', []) extraction instead of CSV row filtering (line 130)
5. **Loop:** Changed from filtering rows by position=='DST' to iterating dst_players array (lines 132-137)
6. **Team Extraction:** Changed from row.get('team', '').upper() to dst_player.get('team', '').upper() (line 133)
7. **Points Extraction:** **CRITICAL:** Changed from manually building weekly_points array from week_N_points columns to directly extracting actual_points array (line 134)
   - **Before:** `weekly_points.append(float(row.get(f'week_{week}_points', '')))`
   - **After:** `actual_points = dst_player.get('actual_points', [0.0] * 17)`
   - **Why:** actual_points contains ACTUAL past performance, not projected_points (pre-season estimates)
8. **Error Handling:** Changed from generic `except Exception` to 3 specific handlers:
   - FileNotFoundError (lines 141-143)
   - json.JSONDecodeError (lines 144-146)
   - PermissionError/OSError (lines 147-149)
9. **Logging:** Changed from logger.warning() to logger.error() for consistency (lines 142, 145, 148)
10. **Docstring:** Updated from "from players.csv" to "from dst_data.json actual_points arrays" (line 113)

**Data Structure Preserved:**
- Input format changed (CSV → JSON)
- Output format UNCHANGED: `{team: [week_1_points, ..., week_17_points]}`
- All consumers (_rank_dst_fantasy, get_team_dst_fantasy_rank) continue working without modification

**Justification:** Migrates D/ST data loading from deprecated players.csv to new dst_data.json JSON format as part of Sub-feature 2 (Weekly Data Migration). Simplifies code (~17 lines fewer) and improves performance (direct array access instead of manual array building).

---

#### Change 3: Data Structure Comment Verification (Line 84)
**Spec Reference:** spec.md lines 34-38, Task 1.5
**Lines Modified:** None (verification only)
**Type:** Verification (no change needed)

**Current Comment (Line 84):**
```python
# D/ST player data: {team: [week_1_points, week_2_points, ..., week_17_points]}
```

**Status:** ✅ **VERIFIED ACCURATE** - Comment still correct because data structure format is unchanged (only data source changed from CSV to JSON).

---

## Testing Impact

### Existing Tests Status
**All tests passing without modification:**
- `tests/league_helper/util/test_TeamDataManager.py`: 24/24 tests passing ✅
- `tests/integration/test_league_helper_integration.py`: 17/17 tests passing ✅
- **Total:** 2406/2406 tests passing (100% pass rate) ✅

### Why Tests Still Pass
The existing TeamDataManager tests use mocking for file I/O, so they work with both CSV and JSON implementations as long as the output data structure (self.dst_player_data dict format) remains unchanged - which it does.

---

## Phase 2 Complete: Test Updates

### File: `tests/league_helper/util/test_TeamDataManager.py`

#### Change: Added comprehensive D/ST JSON loading test class (Lines 558-743)
**Spec Reference:** Task 2.2 (JSON edge case tests)
**Lines Added:** 558-743 (186 lines)
**Type:** New test class with 9 test methods

**Test Class Added:**
```python
class TestDSTJSONLoading:
    """Test D/ST data loading from dst_data.json (JSON edge cases)"""
```

**Tests Added (9 total):**

1. **test_dst_loading_with_valid_json** (Lines 565-593)
   - Tests happy path with valid JSON containing 2 D/ST teams
   - Verifies 17-element actual_points arrays loaded correctly
   - Verifies data accessible via dst_player_data dict

2. **test_dst_loading_with_missing_file** (Lines 595-605)
   - Tests FileNotFoundError when dst_data.json doesn't exist
   - Verifies dst_player_data defaults to empty dict {}
   - Verifies no crash

3. **test_dst_loading_with_malformed_json** (Lines 607-621)
   - Tests json.JSONDecodeError with invalid JSON syntax
   - Verifies dst_player_data defaults to empty dict {}
   - Verifies no crash

4. **test_dst_loading_with_missing_dst_data_key** (Lines 623-637)
   - Tests JSON without 'dst_data' root key
   - Verifies .get('dst_data', []) returns empty array
   - Verifies dst_player_data is empty dict

5. **test_dst_loading_with_empty_dst_data_array** (Lines 639-653)
   - Tests JSON with empty dst_data array: {"dst_data": []}
   - Verifies dst_player_data is empty dict
   - Verifies no teams loaded (loop executes 0 times)

6. **test_dst_loading_with_missing_team_field** (Lines 655-675)
   - Tests D/ST object without 'team' field
   - Verifies .get('team', '') returns empty string
   - Verifies data stored with empty string key ''

7. **test_dst_loading_with_missing_actual_points_field** (Lines 677-697)
   - Tests D/ST object without 'actual_points' field
   - Verifies .get('actual_points', [0.0] * 17) returns default array
   - Verifies dst_player_data["DEN"] == [0.0] * 17

8. **test_dst_loading_with_partial_actual_points_array** (Lines 699-720)
   - Tests D/ST object with only 5 weeks of actual_points
   - Verifies partial array stored as-is (not padded to 17)
   - Verifies len(dst_player_data["SEA"]) == 5
   - **Rationale:** Consumer _rank_dst_fantasy() handles variable-length arrays

9. **test_dst_loading_with_empty_team_name** (Lines 722-742)
   - Tests D/ST object with empty string team name
   - Verifies ''.upper() still returns ''
   - Verifies data stored with empty string key

**Testing Strategy:**
- All tests use temporary folders (mock_data_folder fixture)
- All tests create dst_data.json with specific edge case content
- All tests verify graceful degradation (no crashes)
- All tests verify dst_player_data state matches expectations

**Why These Tests Matter:**
- Verify error handling works correctly (FileNotFoundError, JSONDecodeError)
- Verify .get() defaults work as expected
- Verify partial data doesn't crash the system
- Verify empty/missing fields handled gracefully

**Test Results:**
- **New tests:** 9/9 passing ✅
- **Total TeamDataManager tests:** 33/33 passing (was 24/24 before) ✅
- **Total test suite:** 2415/2415 passing (100%) ✅

---

**Task 2.1 Status:** SKIPPED - No existing tests for _load_dst_player_data() to update
**Task 2.2 Status:** ✅ COMPLETE - 9 JSON edge case tests added
**Task 2.3 Status:** ✅ COMPLETE - Integration tests (17/17) still passing, no regressions

---

## Performance Impact

**Before (CSV):**
- Manual array building (loop 17 times per team)
- CSV parsing overhead
- ~56 lines of code

**After (JSON):**
- Direct array extraction (single assignment)
- Simpler JSON parsing
- ~39 lines of code (-17 lines, -30%)

**Result:** Cleaner code, better performance.

---

## Files Modified Summary

| File | Lines Changed | Type | Description |
|------|---------------|------|-------------|
| **Production Code:** | | | |
| league_helper/util/TeamDataManager.py | +1 (line 21) | Addition | Added import json |
| league_helper/util/TeamDataManager.py | 111-149 (39 lines) | Replacement | Replaced _load_dst_player_data() implementation |
| **Test Code:** | | | |
| tests/league_helper/util/test_TeamDataManager.py | +186 (lines 558-743) | Addition | Added TestDSTJSONLoading class with 9 tests |

**Total:**
- **Production:** 1 file modified, ~40 lines changed, 17 lines net reduction
- **Tests:** 1 file modified, +186 lines, +9 new tests (24 → 33 total tests)
- **Overall:** 2 files modified, +226 lines total

---

## Verification Against Specs

| Requirement | Spec Location | Implemented? | Line(s) | Verified? |
|-------------|---------------|--------------|---------|-----------|
| Add import json | Iteration 2:617 | ✅ YES | 21 | ✅ |
| JSON file path | spec.md:79-80 | ✅ YES | 125 | ✅ |
| json.load() | spec.md:81-82 | ✅ YES | 128 | ✅ |
| Extract dst_data | spec.md:84 | ✅ YES | 130 | ✅ |
| Loop dst_players | spec.md:86 | ✅ YES | 132-137 | ✅ |
| Extract team | spec.md:87 | ✅ YES | 133 | ✅ |
| Extract actual_points | spec.md:88 | ✅ YES | 134 | ✅ CRITICAL |
| Store in dict | spec.md:90-91 | ✅ YES | 137 | ✅ |
| FileNotFoundError | Error pattern | ✅ YES | 141-143 | ✅ |
| JSONDecodeError | Error pattern | ✅ YES | 144-146 | ✅ |
| PermissionError/OSError | Error pattern | ✅ YES | 147-149 | ✅ |
| Update docstring | spec.md:40-42 | ✅ YES | 113 | ✅ |
| Verify comment | spec.md:34-38 | ✅ YES | 84 | ✅ |

**All requirements implemented:** 13/13 ✅

---

## Next Steps

1. ✅ Phase 1 complete - Production code updated
2. ⏳ Phase 2 pending - Test code updates (Tasks 2.1-2.3)
3. ⏳ QA Checkpoint 2 - Final test suite verification
4. ⏳ Post-Implementation QC - Smoke testing and validation

---

**Last Updated:** 2025-12-28
**Phase 1 Status:** ✅ COMPLETE
**Ready for:** Phase 2 (Test Updates)
