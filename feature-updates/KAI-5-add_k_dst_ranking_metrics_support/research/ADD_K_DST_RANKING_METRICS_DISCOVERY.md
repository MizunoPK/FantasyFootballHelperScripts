# Feature 1: Add K and DST Support to Ranking Metrics - Discovery Findings

**Research Date:** 2026-01-08
**Researcher:** Agent
**Grounded In:** Epic Intent (user's explicit requests from epic notes)

---

## Epic Intent Summary

**User requested:** "Add Kicker (K) and Defense/Special Teams (DST) positions to ranking-based accuracy metrics (pairwise accuracy, top-N accuracy, Spearman correlation)"

**Components user mentioned:**
- AccuracyCalculator.py (lines 258, 544)
- positions list
- position_data dict
- Pairwise accuracy, Top-N accuracy, Spearman correlation
- AccuracyResultsManager
- by_position dictionary
- Data files: k_data.json, dst_data.json

**This research focused on user-mentioned components ONLY.**

---

## Research Task 1: Position Hardcoding

**Objective:** Find ALL places where position lists are hardcoded to 4 positions

**Commands Executed:**
```bash
grep -rn "QB.*RB.*WR.*TE" simulation/accuracy/ --include="*.py"
grep -rn "\['QB'.*'RB'.*'WR'.*'TE'\]" simulation/accuracy/ --include="*.py"
grep -rn "position_data\s*=" simulation/accuracy/ --include="*.py"
grep -rn "positions\s*=" simulation/accuracy/ --include="*.py"
```

**Findings:**

### Code Location 1: aggregate_season_results() - Line 258
**File:** `simulation/accuracy/AccuracyCalculator.py`
**Line:** 258
**Code:**
```python
position_data = {'QB': {}, 'RB': {}, 'WR': {}, 'TE': {}}
```

**Purpose:** Initializes dict to aggregate per-position metrics across multiple seasons

**Why this needs changing:**
- Line 283 has check: `if pos in position_data:`
- If K/DST not in this dict, metrics calculated in line 544 will be **silently dropped** during aggregation
- This is the "silent drop" bug mentioned in epic notes line 99

**Method signature:**
```python
def aggregate_season_results(
    self,
    season_results: List[Tuple[str, 'AccuracyResult']]
) -> 'AccuracyResult':
```

**Lines 280-291 show the aggregation loop:**
```python
# Aggregate per-position metrics
if result.by_position:
    for pos, metrics in result.by_position.items():
        if pos in position_data:  # LINE 283 - DROPS K/DST if not in dict
            position_data[pos]['pairwise'].append(metrics.pairwise_accuracy)
            position_data[pos]['top_5'].append(metrics.top_5_accuracy)
            position_data[pos]['top_10'].append(metrics.top_10_accuracy)
            position_data[pos]['top_20'].append(metrics.top_20_accuracy)

            if not np.isnan(metrics.spearman_correlation):
                z = np.arctanh(metrics.spearman_correlation)
                position_data[pos]['spearman_z'].append(z)
```

---

### Code Location 2: calculate_ranking_metrics_for_season() - Line 544
**File:** `simulation/accuracy/AccuracyCalculator.py`
**Line:** 544
**Code:**
```python
positions = ['QB', 'RB', 'WR', 'TE']
```

**Purpose:** Defines which positions to calculate ranking metrics for per-season

**Why this needs changing:**
- Controls which positions are processed in the per-week loop (lines 557-580)
- K and DST data exists but is skipped due to this list

**Method signature:**
```python
def calculate_ranking_metrics_for_season(
    self,
    player_data_by_week: Dict[int, List[Dict[str, Any]]]
) -> Tuple[RankingMetrics, Dict[str, RankingMetrics]]:
```

**Lines 547-554 show position_data creation:**
```python
# Accumulators for per-position metrics (average across weeks)
position_data = {pos: {
    'pairwise_sum': 0.0,
    'top_5_sum': 0.0,
    'top_10_sum': 0.0,
    'top_20_sum': 0.0,
    'spearman_z_values': [],
    'week_count': 0
} for pos in positions}  # Uses line 544 positions list
```

---

### Documentation Locations (No Code Changes Needed)
**File:** `simulation/accuracy/AccuracyCalculator.py`
**Line 351:** Docstring mentions "Position to filter ('QB', 'RB', 'WR', 'TE')"
**Line 535:** Docstring mentions "position': Player position (QB, RB, WR, TE)"

**Assessment:** These are comments/docstrings - will update naturally when code changes

---

## Research Task 2: Position String Comparisons

**Objective:** Find any code that explicitly checks position values

**Commands Executed:**
```bash
grep -rn "position\s*==\s*['\"]" simulation/accuracy/ --include="*.py"
grep -rn "position\s*in\s*\[" simulation/accuracy/ --include="*.py"
```

**Findings:**
- **NO matches found**
- No special-case logic for specific positions
- All position filtering is done generically via the positions list
- **Conclusion:** K/DST will be treated identically to QB/RB/WR/TE once added to positions list

---

## Research Task 3: Data File Position Strings

**Objective:** Confirm K and DST position strings in historical data match expected values

**Commands Executed:**
```bash
cat simulation/sim_data/2024/weeks/week_01/k_data.json | grep -o '"position":\s*"[^"]*"' | sort -u
cat simulation/sim_data/2024/weeks/week_01/dst_data.json | grep -o '"position":\s*"[^"]*"' | sort -u
```

**Findings:**
- K data: `"position": "K"` (exact match)
- DST data: `"position": "DST"` (exact match)

**Verification:** Position strings match expected values exactly

**Data format confirmed:** JSON files contain position field that will match filter at lines 364, 430, 491

---

## Research Task 4: Unit Tests

**Objective:** Identify which test files need new test cases for K/DST

**Commands Executed:**
```bash
find tests/ -name "*accuracy*.py" -type f
grep -rn "QB.*RB.*WR.*TE" tests/ --include="*accuracy*.py"
```

**Findings:**

### Test File: tests/integration/test_accuracy_simulation_integration.py
**Found:** Line 293 already includes K and DST:
```python
'MAX_POSITIONS': {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
```

**Assessment:** Test config already supports K/DST - no hardcoded 4-position assertions found

**Action Required:**
- Verify test still passes after adding K/DST to ranking metrics
- May need to add specific test cases for K/DST ranking metric calculations
- Check if test validates by_position dict contents

---

## Research Task 5: AccuracyResultsManager

**Objective:** Verify results storage/loading doesn't assume 4 positions

**Commands Executed:**
```bash
grep -rn "QB.*RB.*WR.*TE" simulation/accuracy/AccuracyResultsManager.py
grep -rn "by_position" simulation/accuracy/AccuracyResultsManager.py -A 3 -B 3
```

**Findings:**
- **NO hardcoded position lists found**
- Uses dynamic iteration: `for pos, metrics in self.by_position.items()` (line 176)

**Code snippets showing dynamic handling:**

**Line 107:** `self.by_position = by_position or {}`
**Lines 167-177:** Serialization uses dict iteration
```python
if self.by_position:
    result['by_position'] = {
        pos: {
            'pairwise_accuracy': metrics.pairwise_accuracy,
            'top_5_accuracy': metrics.top_5_accuracy,
            'top_10_accuracy': metrics.top_10_accuracy,
            'top_20_accuracy': metrics.top_20_accuracy,
            'spearman_correlation': metrics.spearman_correlation
        }
        for pos, metrics in self.by_position.items()  # Dynamic iteration
    }
```

**Lines 205-208:** Deserialization uses dict keys
```python
by_position = {}
if 'by_position' in data:
    for pos, metrics_dict in data['by_position'].items():  # Handles any position keys
        by_position[pos] = RankingMetrics(...)
```

**Conclusion:** AccuracyResultsManager automatically handles arbitrary position keys - NO changes needed

---

## Research Task 6: Logging and Output

**Objective:** Verify logging doesn't hardcode position lists

**Commands Executed:**
```bash
grep -rn "logger.*QB|logger.*positions" simulation/accuracy/ --include="*.py"
grep -rn "print.*QB|print.*positions" simulation/accuracy/ --include="*.py"
```

**Findings:**
- **NO matches found**
- No logging statements hardcoding position lists
- Logging uses dynamic position variables (e.g., f"Not enough {position} players")

**Example from line 368:**
```python
self.logger.debug(f"Not enough {position} players for pairwise accuracy")
```

**Conclusion:** Logging will automatically display K/DST when added - NO changes needed

---

## Research Task 7: Config Files

**Objective:** Check if optimal config files have position-specific sections

**Commands Executed:**
```bash
find simulation/simulation_configs/accuracy_optimal_* -name "*.json" -type f | head -1 | xargs cat | grep -A 5 "by_position"
```

**Findings:**
- **No accuracy_optimal_* config files found**
- Likely haven't run accuracy simulation yet

**Conclusion:** Config save/load logic (AccuracyResultsManager) already handles arbitrary position keys (see Research Task 5)

---

## Metric Calculation Methods

**Read actual source code to understand implementation:**

### Method 1: calculate_pairwise_accuracy()
**File:** `simulation/accuracy/AccuracyCalculator.py`
**Lines:** 360-390
**Filter:** `if player.get('position') == position and player.get('actual', 0) >= 3.0:` (line 364)
**Implementation:** Compares all pairs, counts correct predictions
**K/DST compatibility:** ✅ Yes - ordinal ranking works with any score distribution

### Method 2: calculate_top_n_accuracy()
**File:** `simulation/accuracy/AccuracyCalculator.py`
**Lines:** 425-455
**Filter:** `if player.get('position') == position and player.get('actual', 0) >= 3.0:` (line 430)
**Implementation:** Set intersection of predicted top-N vs actual top-N
**K/DST compatibility:** ✅ Yes - set-based, not affected by score distribution

### Method 3: calculate_spearman_correlation()
**File:** `simulation/accuracy/AccuracyCalculator.py`
**Lines:** 488-520
**Filter:** `if player.get('position') == position and player.get('actual', 0) >= 3.0:` (line 491)
**Implementation:** Spearman rank correlation between projected and actual
**K/DST compatibility:** ✅ Yes - rank-based, robust to score distribution differences

**Filtering Note:** Epic notes line 171 confirms "Current filtering (actual >= 3.0) is acceptable for K/DST"

---

## Edge Cases Identified

**From reading existing code:**

1. **Small sample size handling** (lines 367, 437, 495)
   - Methods return 0.0 if insufficient players
   - K: ~32 players per week → pairwise needs >= 2 ✅
   - DST: 32 teams → top-N needs >= N players ✅
   - For top-20: Only 32 DST total → will trigger "less than top-20" warning (line 438-440)
   - **Resolution:** Epic notes line 129 says defer adaptive top-N - acceptable for now

2. **Zero variance handling** (line 502-507)
   - Spearman returns NaN if zero variance
   - Already handled correctly (returns 0.0)
   - Works for K/DST

3. **Tie handling** (line 381-382)
   - Pairwise skips ties in actual scores
   - Works for K/DST

---

## Research Completeness

**Components researched:**
- ✅ AccuracyCalculator.py (READ source code lines 250-570)
- ✅ Positions list hardcoding (found 2 locations)
- ✅ Position string comparisons (none found)
- ✅ Data file position strings (verified K and DST)
- ✅ AccuracyResultsManager (READ source code, confirmed dynamic)
- ✅ Unit tests (found 1 file, already has K/DST config)
- ✅ Logging (confirmed dynamic)
- ✅ Config files (none exist yet, save/load logic handles arbitrary positions)

**Evidence collected:**
- File paths: `simulation/accuracy/AccuracyCalculator.py`, `simulation/accuracy/AccuracyResultsManager.py`, `tests/integration/test_accuracy_simulation_integration.py`
- Line numbers: 258, 283, 351, 364, 430, 491, 535, 544
- Actual code snippets: Copied above for all critical sections
- Data verification: Confirmed position strings "K" and "DST"

**Ready for Phase 1.5 audit.**

---

## Summary of Required Changes

### Code Changes (MINIMUM 2 lines)
1. **Line 258:** Change `position_data = {'QB': {}, 'RB': {}, 'WR': {}, 'TE': {}}`
   to `position_data = {'QB': {}, 'RB': {}, 'WR': {}, 'TE': {}, 'K': {}, 'DST': {}}`

2. **Line 544:** Change `positions = ['QB', 'RB', 'WR', 'TE']`
   to `positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']`

### Documentation Updates
- Update docstrings at lines 351, 535 to mention all 6 positions
- Update `docs/simulation/ACCURACY_SIMULATION_FLOW_VERIFIED.md` (per epic notes line 355)

### Test Updates
- Verify `tests/integration/test_accuracy_simulation_integration.py` passes
- Consider adding explicit K/DST ranking metric test cases

### NO Changes Needed
- ✅ AccuracyResultsManager (already dynamic)
- ✅ Logging (already dynamic)
- ✅ Config save/load (already dynamic)
- ✅ Metric calculation methods (already position-agnostic)
- ✅ Filtering logic (already accepts K/DST data)

---

**Next Steps:**
- Phase 1.5: Verify research completeness (MANDATORY GATE)
- STAGE_2b Phase 2: Update spec.md with these findings
- STAGE_2b Phase 2.5: Spec-to-Epic alignment check
