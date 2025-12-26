# Smoke Test Protocol - Historical Data JSON Generation

**Feature:** JSON file generation for historical data compiler
**Purpose:** Manual validation of JSON generation functionality
**Created:** 2025-12-26

---

## Prerequisites

Before running smoke tests:
- [x] All unit tests passing (2,369/2,369 = 100%)
- [x] Integration tests passing
- [x] Code review complete
- [ ] Smoke tests executed

---

## Test Environment

**Test Data Requirements:**
- Historical NFL season data (2023 recommended)
- At least 1-3 weeks of data for validation
- Mix of player positions (QB, RB, WR, TE, K, DST)

**Test Command:**
```bash
python compile_historical_data.py --year 2023 --weeks 1-3
```

---

## Smoke Test Parts

### Part 1: Import Test

**Purpose:** Verify all modules import correctly

**Test:**
```bash
python -c "from historical_data_compiler import json_exporter; print('Import successful')"
```

**Expected Output:**
```
Import successful
```

**Pass Criteria:**
- [x] No import errors
- [x] No module not found errors
- [x] Clean exit

---

### Part 2: Generation Test

**Purpose:** Verify JSON files are generated alongside CSV files

**Test:**
```bash
# Set toggles in compile_historical_data.py
GENERATE_CSV = True
GENERATE_JSON = True

# Run historical data compiler
python compile_historical_data.py --year 2023 --weeks 1-3
```

**Expected Output Structure:**
```
simulation/sim_data/2023/
├── weeks/
│   ├── week_01/
│   │   ├── players.csv              (CSV - existing)
│   │   ├── players_projected.csv    (CSV - existing)
│   │   ├── qb_data.json             (JSON - NEW)
│   │   ├── rb_data.json             (JSON - NEW)
│   │   ├── wr_data.json             (JSON - NEW)
│   │   ├── te_data.json             (JSON - NEW)
│   │   ├── k_data.json              (JSON - NEW)
│   │   └── dst_data.json            (JSON - NEW)
│   ├── week_02/
│   │   └── (same structure)
│   └── week_03/
│       └── (same structure)
```

**Pass Criteria:**
- [ ] All 6 JSON files generated per week
- [ ] CSV files still generated (backward compatibility)
- [ ] Both formats coexist in same folder
- [ ] No errors during generation
- [ ] Console output shows JSON generation logs

---

### Part 3: JSON Structure Validation

**Purpose:** Verify JSON files match expected schema

**Test:**
```python
import json
from pathlib import Path

# Load QB data for week 1
with open('simulation/sim_data/2023/weeks/week_01/qb_data.json') as f:
    qb_data = json.load(f)

# Validate structure
assert isinstance(qb_data, list), "Root should be array"
assert len(qb_data) > 0, "Should have players"

# Check first player structure
player = qb_data[0]
required_fields = [
    'id', 'name', 'team', 'position', 'injury_status',
    'drafted_by', 'locked', 'average_draft_position',
    'player_rating', 'projected_points', 'actual_points'
]

for field in required_fields:
    assert field in player, f"Missing field: {field}"

# Validate arrays are 17 weeks
assert len(player['projected_points']) == 17, "Should have 17 weeks"
assert len(player['actual_points']) == 17, "Should have 17 weeks"

# Validate position-specific stats
if player['position'] == 'QB':
    assert 'passing' in player, "QB should have passing stats"

print("✅ JSON structure validation passed")
```

**Pass Criteria:**
- [ ] All required fields present
- [ ] Arrays have 17 elements (one per week)
- [ ] Position-specific stats included
- [ ] Data types correct (numbers, strings, booleans, null)
- [ ] No extra/unknown fields

---

### Part 4: Point-in-Time Logic Validation

**Purpose:** Verify point-in-time logic is correctly applied

**Test:**
```python
import json

# Load week 1 data
with open('simulation/sim_data/2023/weeks/week_01/qb_data.json') as f:
    week1_data = json.load(f)

# Load week 8 data
with open('simulation/sim_data/2023/weeks/week_08/qb_data.json') as f:
    week8_data = json.load(f)

# Find same player in both weeks
player_w1 = next(p for p in week1_data if p['id'] == '<PLAYER_ID>')
player_w8 = next(p for p in week8_data if p['id'] == '<PLAYER_ID>')

# Week 1 validation
print("Week 1 - Point-in-Time Logic:")
print(f"  actual_points[0]: {player_w1['actual_points'][0]}")     # Should be 0.0 (future)
print(f"  actual_points[1]: {player_w1['actual_points'][1]}")     # Should be 0.0 (current)
print(f"  projected_points[0]: {player_w1['projected_points'][0]}")  # Should be week 1 projection

# Week 8 validation
print("\nWeek 8 - Point-in-Time Logic:")
print(f"  actual_points[0]: {player_w8['actual_points'][0]}")     # Should be actual (past)
print(f"  actual_points[6]: {player_w8['actual_points'][6]}")     # Should be actual (past)
print(f"  actual_points[7]: {player_w8['actual_points'][7]}")     # Should be 0.0 (current)
print(f"  projected_points[7]: {player_w8['projected_points'][7]}")  # Should be week 8 projection
print(f"  projected_points[16]: {player_w8['projected_points'][16]}") # Should also be week 8 projection

# Validation assertions
assert player_w1['actual_points'][0] == 0.0, "Week 1: Future weeks should be 0.0"
assert player_w8['actual_points'][0] > 0.0, "Week 8: Week 1 should have actual points"
assert player_w8['actual_points'][7] == 0.0, "Week 8: Current week should be 0.0"

print("\n✅ Point-in-time logic validation passed")
```

**Pass Criteria:**
- [ ] Week 1: All actual_points are 0.0 (all future weeks)
- [ ] Week 8: Weeks 1-7 have actual points, weeks 8-17 are 0.0
- [ ] Week 8: All future projected_points use week 8's projection
- [ ] Bye weeks are 0.0 in all arrays
- [ ] Player ratings differ between week 1 and week 8

---

### Part 5: Toggle Behavior Validation

**Purpose:** Verify CSV/JSON toggles work correctly

**Test 1: CSV Only**
```python
# Set in compile_historical_data.py
GENERATE_CSV = True
GENERATE_JSON = False

# Run compiler
python compile_historical_data.py --year 2023 --weeks 1
```

**Expected:**
- [ ] CSV files generated
- [ ] No JSON files generated
- [ ] No errors

**Test 2: JSON Only**
```python
# Set in compile_historical_data.py
GENERATE_CSV = False
GENERATE_JSON = True

# Run compiler (use different output dir to avoid conflict)
python compile_historical_data.py --year 2023 --weeks 1
```

**Expected:**
- [ ] JSON files generated
- [ ] No CSV files generated
- [ ] No errors

**Test 3: Neither (Edge Case)**
```python
# Set in compile_historical_data.py
GENERATE_CSV = False
GENERATE_JSON = False

# Run compiler
python compile_historical_data.py --year 2023 --weeks 1
```

**Expected:**
- [ ] Week folders created but empty of data files
- [ ] Warning logged about no output
- [ ] No errors (graceful handling)

---

## Post-Smoke Test Validation

### Data Consistency Check

Compare JSON vs CSV for same week to ensure consistency:

**Test:**
```python
import json
import csv

# Load JSON
with open('simulation/sim_data/2023/weeks/week_05/qb_data.json') as f:
    json_data = {p['id']: p for p in json.load(f)}

# Load CSV
with open('simulation/sim_data/2023/weeks/week_05/players.csv') as f:
    csv_data = {r['id']: r for r in csv.DictReader(f) if r['position'] == 'QB'}

# Compare
for player_id in json_data:
    if player_id in csv_data:
        json_player = json_data[player_id]
        csv_player = csv_data[player_id]

        # Compare basic fields
        assert json_player['name'] == csv_player['name']
        assert json_player['team'] == csv_player['team']
        assert json_player['position'] == csv_player['position']

        # Compare fantasy points (total)
        json_total = sum(json_player['actual_points']) + sum(json_player['projected_points'][:len([p for p in json_player['actual_points'] if p == 0])])
        csv_total = float(csv_player['fantasy_points'])

        # Should be similar (within rounding)
        assert abs(json_total - csv_total) < 5.0, f"Totals differ: {json_total} vs {csv_total}"

print("✅ Data consistency check passed")
```

**Pass Criteria:**
- [ ] Player counts match between JSON and CSV
- [ ] Basic fields consistent (name, team, position)
- [ ] Fantasy point totals approximately match (within rounding)
- [ ] No data corruption

---

## Smoke Test Checklist

### Pre-Test
- [ ] All unit tests passing (2,369/2,369)
- [ ] Code review complete
- [ ] Test data available (2023 season)

### During Test
- [ ] ✅ Part 1: Import test passed
- [ ] ✅ Part 2: Generation test passed
- [ ] ✅ Part 3: Structure validation passed
- [ ] ✅ Part 4: Point-in-time validation passed
- [ ] ✅ Part 5: Toggle validation passed

### Post-Test
- [ ] Data consistency check passed
- [ ] No errors in logs
- [ ] Performance acceptable (<5 min for 3 weeks)
- [ ] File sizes reasonable (<10MB per JSON file)

---

## Known Issues / Limitations

(Document any issues found during smoke testing)

- None at this time

---

## Sign-Off

**Smoke Tests Completed By:** _____________
**Date:** _____________
**Result:** PASS / FAIL
**Notes:**

