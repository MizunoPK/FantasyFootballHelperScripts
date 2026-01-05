# End-to-End Data Flow - Feature 01

**Purpose:** Trace data from entry point through all transformations to output

**Created:** 2026-01-03 (Stage 5a Round 1 - Iteration 5)
**Updated:** 2026-01-03 (Stage 5a Round 2 - Iteration 12 - RE-VERIFICATION)

**⚠️ CRITICAL RE-VERIFICATION:** This flow was re-verified after Round 2 to catch any new transformations added during test strategy, edge case enumeration, or config analysis.

---

## Data Flow: Win Rate Sim JSON Verification

### Entry Point

**Source:** JSON files in week folders
- Location: `simulation/sim_data/{year}/weeks/week_{NN}/`
- Files: 6 position files per week (qb_data.json, rb_data.json, wr_data.json, te_data.json, k_data.json, dst_data.json)
- Format: JSON arrays of player dictionaries

**Example JSON Structure:**
```json
{
  "id": "3918298",
  "name": "Josh Allen",
  "position": "QB",
  "drafted_by": "",
  "locked": false,
  "projected_points": [20.8, 20.8, ..., 20.8],  // Array of 17 values
  "actual_points": [0.0, 0.0, ..., 23.2]         // Array of 17 values
}
```

---

### Step 1: Week Data Preloading (Algorithm 2)

**Method:** `_preload_all_weeks()` (SimulatedLeague.py lines 269-336)

**Input:**
- self.data_folder: Path to simulation/sim_data/2025/
- weeks/ subfolder with week_01 through week_18

**Process:**
1. For each week 1-17:
   - Identify projected_folder = weeks/week_{week_num:02d}
   - Identify actual_folder = weeks/week_{week_num+1:02d}  (week_N+1 pattern)

2. For week 17 specifically:
   - projected_folder = week_17  (projected_points[16])
   - actual_folder = week_18     (actual_points[16])

3. Parse data from both folders (calls Step 2)

4. Cache result:
   - week_data_cache[week_num] = {'projected': ..., 'actual': ...}

**Output:** Dictionary of week data cached for simulation use

**Transformations:**
- Physical folder structure → Cached data structure
- Week_N+1 pattern applied (actual data from next week's folder)

**Edge Case Handling:**
- Missing week_N folder → Log warning, skip week
- Missing week_N+1 folder → Fallback to projected data
- Missing weeks/ folder → Early return (legacy mode)

---

### Step 2: JSON File Parsing (Algorithm 1)

**Method:** `_parse_players_json(week_folder, week_num, week_num_for_actual)` (SimulatedLeague.py lines 363-440)

**Input:**
- week_folder: Path to week_NN folder
- week_num: Week number for array indexing (1-17)
- week_num_for_actual: Optional override for actual_points indexing

**Process:**
1. For each of 6 position files:
   - Read JSON file → Python list of dicts
   - For each player dict:
     - Extract player data (Step 3: Field Conversions)
     - Add to players dict keyed by player ID

2. Return combined players dict

**Output:** Dict[int, Dict[str, str]] - Player data with single-value fields

**Transformations:**
- JSON file → Python data structures
- Multiple position files → Single players dict
- Array-based fields → Single values (via Step 3)

**Edge Case Handling:**
- Missing JSON file → Log warning, continue with other files
- Malformed JSON → Log error, skip file
- Empty JSON array → Return empty dict for that position
- All files missing → Return empty dict (no players)

---

### Step 3: Field Type Conversions (Algorithm 3)

**Part of:** `_parse_players_json()` method (SimulatedLeague.py lines 413-434)

**Input:** Player dict from JSON with array-based fields

**Process (applied to EACH player):**

**Conversion 3a: projected_points (Array → Single Value)**
```python
# Input: projected_points = [20.8, 21.2, 19.5, ..., 20.8]  (17 values)
# Extract: projected_points[week_num - 1]
# Output: "20.8" (string with single value for this week)
```
- Lines 413-417
- Zero-based indexing: week 1 = index 0, week 17 = index 16
- Bounds checking: If array too short, default to 0.0

**Conversion 3b: actual_points (Array → Single Value)**
```python
# Input: actual_points = [0.0, 0.0, 0.0, ..., 23.2]  (17 values)
# Extract: actual_points[actual_week - 1]
# Output: "23.2" (string with single value for this week)
```
- Lines 419-423
- actual_week = week_num_for_actual if provided, else week_num
- For week 17: actual_week = 18 → actual_points[17] from week_18 data
- Bounds checking: If array too short, default to 0.0

**Conversion 3c: locked (Boolean → String)**
```python
# Input: locked = false  (boolean)
# Convert: bool → int → string
# Output: "0" (string)
```
- Line 431
- false → 0 → "0"
- true → 1 → "1"
- Maintains CSV format compatibility

**Conversion 3d: drafted_by (No Change)**
```python
# Input: drafted_by = ""  (string)
# Output: "" (same string)
```
- Line 430
- No conversion needed

**Output:** Player dict with single-value fields:
```python
{
  'id': "3918298",
  'name': "Josh Allen",
  'position': "QB",
  'drafted_by': "",
  'locked': "0",
  'projected_points': "20.8",
  'actual_points': "23.2"
}
```

**Transformations:**
- Array[17] → Single value (week-specific extraction)
- Boolean → String
- JSON types → CSV-compatible string types

**Edge Case Handling:**
- Array index out of bounds → Default to 0.0
- Null values in array → Default to 0.0
- Missing fields → Use defaults (empty string, False, empty array)

---

### Step 4: Simulation Execution (Existing Code - Not Modified)

**Method:** Various simulation methods in SimulatedLeague

**Input:** Cached week data from Step 1

**Process:**
1. Simulation uses week_data_cache[week_num]
2. Accesses 'projected' and 'actual' player data
3. Runs simulations with player scores

**Output:** Simulation results (win rates, draft strategies)

**Data Flow:**
- Cached data → Simulation logic → Results

**Note:** This step is NOT modified by this feature. We only verify the data loading works correctly.

---

## End-to-End Flow Diagram

```
┌─────────────────────────────────────────┐
│ Entry: JSON Files in week_NN folders   │
│ simulation/sim_data/2025/weeks/week_01/ │
│ - qb_data.json, rb_data.json, etc.     │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│ STEP 1: _preload_all_weeks()           │
│ - For weeks 1-17                        │
│ - Identify week_N and week_N+1 folders  │
│ - Week 17: week_17 + week_18            │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│ STEP 2: _parse_players_json()          │
│ - Read 6 position JSON files           │
│ - Parse to Python dicts                 │
│ - Combine into single players dict     │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│ STEP 3: Field Type Conversions         │
│ - projected_points[week-1] → "20.8"    │
│ - actual_points[week-1] → "23.2"       │
│ - locked (bool) → "0" or "1" (string)  │
│ - drafted_by (string) → (no change)    │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│ Cached Data: week_data_cache[1-17]     │
│ {                                       │
│   1: {'projected': {...}, 'actual': {...}}, │
│   2: {'projected': {...}, 'actual': {...}}, │
│   ...                                   │
│   17: {'projected': {...}, 'actual': {...}} │
│ }                                       │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│ STEP 4: Simulation Execution            │
│ (Existing code - not modified)          │
│ - Use cached data for simulations       │
│ - Calculate win rates                   │
└───────────────┬─────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────┐
│ Output: Simulation Results              │
│ (Win rates, draft strategies, etc.)     │
└─────────────────────────────────────────┘
```

---

## Data Transformations Summary

| Step | Input Format | Output Format | Transformation |
|------|--------------|---------------|----------------|
| 1 | Folder paths (week_NN) | Cached data structure | Folder navigation + week_N+1 pattern |
| 2 | JSON files (6 per week) | Python dict (players by ID) | JSON parsing + merge |
| 3 | Array-based fields | Single-value string fields | Array indexing + type conversion |
| 4 | Cached player data | Simulation results | Simulation logic (unchanged) |

---

## Verification Points

**Step 1 Verification (Task 4, 6, 7, 9):**
- ✅ Verify week_N+1 pattern works (week 17 uses week_18)
- ✅ Verify week_18 folder exists and has data
- ✅ Verify missing folder fallback works

**Step 2 Verification (Task 2, 6, 7, 8):**
- ✅ Verify all 6 position files loaded
- ✅ Verify missing file handling (warning + continue)
- ✅ Verify malformed JSON handling

**Step 3 Verification (Task 3, 6, 7, 8):**
- ✅ Verify array indexing correct (week 1 = index 0, week 17 = index 16)
- ✅ Verify locked conversion (boolean → "0"/"1")
- ✅ Verify projected/actual extraction from arrays
- ✅ Verify bounds checking (array < 17 elements)

**Step 4 Verification (Task 7, 11):**
- ✅ Verify simulation runs without errors
- ✅ Verify results are correct

---

## Round 2 Re-Verification (Iteration 12)

**Date:** 2026-01-03
**Verified By:** Stage 5a Round 2 - Iteration 12

### New Data Transformations Discovered in Round 2?

**Answer:** NO ❌

**Analysis:**
- Iteration 8 (Test Strategy): No new transformations, only tests for existing flow
- Iteration 9 (Edge Case Enumeration): Added edge case handling docs, no new transformations
- Iteration 10 (Config Impact): No config changes, no new transformations
- Iteration 11 (Algorithm Re-verify): Confirmed all transformations in algorithms

### Data Flow Gaps Check

**Verification:**
- ✅ Step 1 outputs feed into Step 2 (week folders → JSON parsing)
- ✅ Step 2 outputs feed into Step 3 (player dicts → field conversions)
- ✅ Step 3 outputs feed into Step 4 (single-value fields → cached data)
- ✅ Step 4 uses cached data (simulation execution)

**No gaps found:** ✅

### Edge Case Flow Paths

**New in Round 2:** Documented edge case paths for each step

**Step 1 Edge Cases:**
- Missing week_N folder → Log warning → Skip week (data flow stops for that week)
- Missing week_N+1 folder → Log warning → Use projected as fallback (data flow continues)
- Missing weeks/ folder → Early return → Legacy mode (data flow uses different source)

**Step 2 Edge Cases:**
- Missing JSON file → Log warning → Continue with other files (partial data flow)
- Malformed JSON → Log error → Skip file (partial data flow)
- All files missing → Return empty dict (empty data flow, no crash)

**Step 3 Edge Cases:**
- Array index out of bounds → Use default 0.0 (data flow continues with default)
- Null values in array → Use default 0.0 (data flow continues with default)
- Missing fields → Use defaults (data flow continues with safe values)

**All edge paths documented:** ✅

### TODO Task Coverage

| Data Flow Step | TODO Tasks | Coverage |
|----------------|-----------|----------|
| Step 1: Preloading | Tasks 4, 6, 7, 9 | ✅ 100% |
| Step 2: JSON Parsing | Tasks 2, 6, 7, 8 | ✅ 100% |
| Step 3: Conversions | Tasks 3, 6, 7, 8 | ✅ 100% |
| Step 4: Simulation | Tasks 7, 11 | ✅ 100% |

**All steps have corresponding TODO tasks:** ✅

---

## Iteration 12 Complete

**Re-Verification Status:** ✅ PASSED

**Evidence:**
- ✅ Re-checked data flow against Round 2 additions
- ✅ Verified no new transformations in Iterations 8-11
- ✅ Documented edge case flow paths for all steps
- ✅ Confirmed no gaps in data flow (all steps connected)
- ✅ Verified all flow steps have TODO task coverage
- ✅ Created comprehensive flow diagram

**Conclusion:** End-to-End Data Flow remains accurate and complete after Round 2. Edge case paths added for completeness.

**Next:** Iteration 13 - Dependency Version Check
