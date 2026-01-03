# Algorithm Traceability Matrix - Feature 01

**Purpose:** Map every algorithm mentioned in spec.md to actual code locations

**Created:** 2026-01-03 (Stage 5a Round 1 - Iteration 4)
**Updated:** 2026-01-03 (Stage 5a Round 2 - Iteration 11 - RE-VERIFICATION)

**⚠️ CRITICAL RE-VERIFICATION:** This matrix was re-verified after Round 2 to catch any new algorithms added during test strategy, edge case enumeration, or config analysis.

---

## Algorithm 1: JSON File Parsing

**Spec Reference:** Requirement 2 (spec.md lines 152-166)
**Algorithm Type:** Data Loading + Transformation
**Code Location:** `simulation/win_rate/SimulatedLeague.py` lines 363-440
**Method:** `_parse_players_json(week_folder: Path, week_num: int, week_num_for_actual: Optional[int] = None)`

**Input:**
- week_folder: Path to week_NN folder (e.g., simulation/sim_data/2025/weeks/week_01/)
- week_num: Week number for projected_points indexing (1-17)
- week_num_for_actual: Optional week number for actual_points indexing

**Output:**
- Dict[int, Dict[str, Any]]: Player data keyed by player ID with single-value fields (matching CSV format)

**Algorithm Steps:**
1. Iterate through 6 position files: qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json
2. For each file:
   - Read JSON, parse to list of player dicts
   - For each player:
     - Extract projected_points array, get value at [week_num - 1] (zero-based)
     - Extract actual_points array, get value at [actual_week - 1] (zero-based)
     - Convert locked boolean to string "0"/"1"
     - Build player dict with single values (id, name, position, drafted_by, locked, projected_points, actual_points)
3. Return combined player dict keyed by player ID

**Edge Cases Handled (Verified in Iteration 9):**
- Missing JSON file: Log warning, continue (line 400) - Edge Case 13
- Array index out of bounds: Default to 0.0 (lines 414-423) - Edge Cases 6, 7, 12
- Empty JSON array: Default to 0.0 (lines 414-423) - Edge Case 6
- Malformed JSON: try/except catches ValueError, KeyError, TypeError (lines 405, 435-437) - Edge Cases 2, 3, 5
- week_num_for_actual=None: Default to week_num (line 391) - Normal operation
- Null values in array: Handled by type conversion or defaults - Edge Case 23
- All position files missing: Returns empty dict, no crash - Edge Case 14

---

## Algorithm 2: Week_N+1 Data Loading Pattern

**Spec Reference:** Requirement 4 (spec.md lines 192-215)
**⚠️ SPEC ERROR:** spec.md line 201 references `_preload_week_data()` but actual method is `_preload_all_weeks()`
**Algorithm Type:** Data Loading + Orchestration
**Code Location:** `simulation/win_rate/SimulatedLeague.py` lines 269-336
**Method:** `_preload_all_weeks()`

**Input:**
- self.data_folder: Path to simulation/sim_data/{year}/
- Implicit: weeks/ subfolder with week_01 through week_18

**Output:**
- self.week_data_cache: Dict[int, Dict] with keys 1-17, values {'projected': Dict, 'actual': Dict}

**Algorithm Steps:**
1. For each week_num in range(1, 18):
   - Construct projected_folder = weeks/week_{week_num:02d}
   - Construct actual_folder = weeks/week_{week_num+1:02d}  (week_N+1 pattern)
   - If projected_folder doesn't exist: Log warning, skip week
   - Parse projected data from week_N folder: _parse_players_json(projected_folder, week_num)
   - If actual_folder exists:
     - Parse actual data from week_N+1 folder: _parse_players_json(actual_folder, week_num, week_num_for_actual=week_num+1)
   - Else (week_N+1 doesn't exist):
     - Use projected data as fallback (actual_data = projected_data)
   - Cache both datasets: week_data_cache[week_num] = {'projected': ..., 'actual': ...}

**Edge Cases Handled (Verified in Iteration 9):**
- Missing week_N folder: Log warning, skip week (lines 304-306) - Edge Case 15
- Missing week_N+1 folder: Fallback to projected data (lines 316-322) - Edge Case 16
- Week 17 limitation: No week_18 folder triggers fallback (line 316 comment) - Edge Case 10
- Missing weeks/ folder (legacy mode): Early return (lines 290-292) - Edge Case 18

**Week 17 Specific Behavior:**
- projected_folder = week_17 (projected_points[16] from week_17 data)
- actual_folder = week_18 (actual_points[16] from week_18 data)
- Uses week_num_for_actual=18 parameter to extract correct array index

---

## Algorithm 3: Field Type Conversions

**Spec Reference:** Requirement 3 (spec.md lines 169-189)
**Algorithm Type:** Data Transformation
**Code Location:** `simulation/win_rate/SimulatedLeague.py` lines 413-434
**Part of:** `_parse_players_json()` method

**Conversions Performed:**

### Conversion 3a: locked (Boolean → String)
**Line:** 431
**Input:** player_dict.get('locked', False) - boolean from JSON
**Output:** str(int(...)) - string "0" or "1"
**Logic:** Convert boolean to int (0 or 1), then to string
**Reason:** Compatibility with CSV format (CSV had string values)

### Conversion 3b: projected_points (Array → Single Value)
**Lines:** 413-417
**Input:** player_dict.get('projected_points', []) - array[17] of floats
**Output:** str(projected) - string with single float value
**Logic:** Extract value at index [week_num - 1], default to 0.0 if array too short
**Reason:** CSV format had single column, simulation expects single value per week

### Conversion 3c: actual_points (Array → Single Value)
**Lines:** 419-423
**Input:** player_dict.get('actual_points', []) - array[17] of floats
**Output:** str(actual) - string with single float value
**Logic:** Extract value at index [actual_week - 1], default to 0.0 if array too short
**Reason:** CSV format had single column, simulation expects single value per week

### Conversion 3d: drafted_by (No Change)
**Line:** 430
**Input:** player_dict.get('drafted_by', '') - string from JSON
**Output:** Same string
**Logic:** No conversion needed (both CSV and JSON use string)

---

## Algorithm 4: Deprecated CSV Parsing (TO BE DELETED)

**Spec Reference:** Requirement 1 (spec.md lines 137-149)
**Algorithm Type:** Data Loading (DEPRECATED)
**Code Location:** `simulation/win_rate/SimulatedLeague.py` lines 338-361
**Method:** `_parse_players_csv(filepath: Path)`
**Status:** MARKED FOR DELETION

**Implementation Note:** This method is deprecated and no longer called. Task 1 will delete it.

**Verification:**
- Grep search confirmed NO calls to _parse_players_csv() exist in codebase
- Method marked DEPRECATED in docstring (lines 342-343)

---

## Algorithm Summary

**Total Algorithms:** 4 (unchanged from Round 1)
- Algorithm 1: JSON File Parsing (ACTIVE - needs verification)
- Algorithm 2: Week_N+1 Data Loading (ACTIVE - needs verification)
- Algorithm 3: Field Type Conversions (ACTIVE - needs verification)
- Algorithm 4: CSV Parsing (DEPRECATED - will be deleted)

**All algorithm locations verified** by reading actual source code (DO NOT ASSUME compliance).

---

## Round 2 Re-Verification (Iteration 11)

**Date:** 2026-01-03
**Verified By:** Stage 5a Round 2 - Iteration 11

### New Algorithms Discovered in Round 2?

**Answer:** NO ❌

**Analysis:**
- Iteration 8 (Test Strategy): Added tests for existing algorithms, no new algorithms
- Iteration 9 (Edge Case Enumeration): Identified 25 edge cases, all handled by existing algorithms
- Iteration 10 (Config Impact): No config changes, no new algorithms

### Edge Case Handling Updates

**Changes from Round 1:**
- ✅ Verified all 25 edge cases map to existing algorithms
- ✅ Updated Algorithm 1 edge case list (added 4 edge cases)
- ✅ Updated Algorithm 2 edge case list (added 1 edge case)
- ✅ Cross-referenced with edge_cases.md

### Algorithm Count Verification

**Round 1 Count:** 4 algorithms
**Round 2 Count:** 4 algorithms (unchanged)
**New Algorithms Added:** 0
**Algorithms Removed:** 0 (Algorithm 4 will be deleted, but still tracked)

### Matrix Completeness Check

**Algorithms in Spec.md:** 3 active algorithms (Requirements 1-4)
**Algorithms in Matrix:** 3 active + 1 deprecated = 4 total
**Missing Algorithms:** 0 ✅

### TODO Task Coverage

| Algorithm | TODO Tasks | Coverage |
|-----------|-----------|----------|
| Algorithm 1: JSON Parsing | Tasks 2, 3, 6, 7, 8 | ✅ 100% |
| Algorithm 2: Week_N+1 Loading | Tasks 4, 6, 7, 9 | ✅ 100% |
| Algorithm 3: Field Conversions | Tasks 3, 6, 7, 8 | ✅ 100% |
| Algorithm 4: CSV Parsing (DELETE) | Task 1 | ✅ 100% |

**All algorithms have corresponding TODO tasks:** ✅

---

## Iteration 11 Complete

**Re-Verification Status:** ✅ PASSED

**Evidence:**
- ✅ Re-checked algorithm matrix against Round 2 additions
- ✅ Verified no new algorithms discovered in Iterations 8-10
- ✅ Updated edge case handling documentation
- ✅ Confirmed matrix is STILL complete (4 algorithms)
- ✅ Verified all algorithms have TODO task coverage

**Conclusion:** Algorithm Traceability Matrix remains accurate and complete after Round 2. No updates needed beyond edge case clarifications.

**Next:** Iteration 12 - End-to-End Data Flow (Re-verify)
