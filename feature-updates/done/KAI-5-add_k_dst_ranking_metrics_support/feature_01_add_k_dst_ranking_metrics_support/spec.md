# Feature 1: Add K and DST Support to Ranking Metrics

---

## Epic Intent (User's Original Request)

**⚠️ CRITICAL:** All requirements below MUST trace back to this section.

**Problem This Feature Solves:**

"Currently, these positions are only evaluated using MAE (fallback metric), while QB/RB/WR/TE use pairwise accuracy (primary metric)."
(Source: Epic notes line 14)

"Ranking Metrics: Only 4 positions evaluated (QB, RB, WR, TE)"
(Source: Epic notes line 29)

---

**User's Explicit Requests:**

1. "Add Kicker (K) and Defense/Special Teams (DST) positions to ranking-based accuracy metrics (pairwise accuracy, top-N accuracy, Spearman correlation)"
   (Source: Epic notes line 14)

2. "Execute all 7 research tasks from epic request systematically"
   (Source: Epic notes line 177 - Research Tasks section)

3. "Only proceed with implementation after research is complete."
   (Source: Epic notes line 300)

4. "Start with simple fix (just add K/DST to positions list), then evaluate if adaptive top-N is needed based on results."
   (Source: Epic notes line 129 - defer adaptive top-N as optional enhancement)

---

**User's Constraints:**

- "⚠️ IMPORTANT: Before making changes, complete thorough research"
  (Source: Epic notes line 72)

- "Start with simple fix (just add K/DST to positions list)"
  (Source: Epic notes line 129 - defer adaptive top-N enhancement)

- "Current filtering (actual >= 3.0) is acceptable for K/DST"
  (Source: Epic notes line 171 - don't change existing filtering logic)

---

**Out of Scope (User Explicitly Deferred):**

- "Position-specific top-N thresholds" - Listed as "Nice to Have", not "Must Have"
  (Source: Epic notes line 361)

- "Separate logging for K/DST vs. skill position metrics" - Listed as "Nice to Have"
  (Source: Epic notes line 362)

- "Performance comparison report" - Listed as "Nice to Have"
  (Source: Epic notes line 363)

- "Adaptive Top-N Metrics (Optional Enhancement)" - Explicitly deferred for future evaluation
  (Source: Epic notes lines 103-129)

---

**User's End Goal:**

"Weather/Location Parameters: K and DST are most affected by: TEMPERATURE_IMPACT_SCALE / TEMPERATURE_SCORING_WEIGHT, WIND_IMPACT_SCALE / WIND_SCORING_WEIGHT, LOCATION_HOME / LOCATION_AWAY / LOCATION_INTERNATIONAL. These 7 of 16 parameters (44%!) are currently optimized using MAE-only feedback for the positions they impact most."
(Source: Epic notes lines 50-55)

"Completeness: The simulation claims to optimize 'prediction accuracy' but only measures ranking quality for 4 of 6 positions."
(Source: Epic notes line 62)

---

**Technical Components Mentioned by User:**

- **AccuracyCalculator.py** (Epic notes lines 30, 74, 162, 429)
- **positions list** at line 544 (Epic notes line 78)
- **position_data dict** at line 258 (Epic notes line 87)
- **Pairwise accuracy** calculations (Epic notes lines 33, 60)
- **Top-N accuracy** calculations (Epic notes line 34)
- **Spearman correlation** calculations (Epic notes line 35)
- **AccuracyResultsManager** (Epic notes line 250)
- **by_position** dictionary (Epic notes lines 259, 348)
- **Data files:** simulation/sim_data/*/k_data.json and dst_data.json (Epic notes lines 221-224)

---

**Agent Verification:**

- [x] Re-read epic notes file: 2026-01-08 15:15
- [x] Extracted exact quotes (not paraphrases)
- [x] Cited line numbers for all quotes
- [x] Identified out-of-scope items (adaptive top-N, performance reports, separate logging)
- [x] Understand user's goal: Enable ranking metrics for K/DST to properly optimize weather/location parameters

---

## Objective

Execute thorough research to identify all code locations requiring changes, then implement K/DST support in ranking-based accuracy metrics (pairwise accuracy, top-N accuracy, Spearman correlation) in the accuracy simulation.

## Components Affected

**Classes to Modify:**

### 1. AccuracyCalculator (`simulation/accuracy/AccuracyCalculator.py`)

**Source:** Epic notes line 74: "File: `simulation/accuracy/AccuracyCalculator.py`"
**Traceability:** Direct user specification

**Changes Required:**

#### Change 1: aggregate_season_results() - Line 258
**Current code:**
```python
position_data = {'QB': {}, 'RB': {}, 'WR': {}, 'TE': {}}
```

**New code:**
```python
position_data = {'QB': {}, 'RB': {}, 'WR': {}, 'TE': {}, 'K': {}, 'DST': {}}
```

**Source:** Epic notes lines 87-93 specify exact change
**Traceability:** Direct user specification
**Why needed:** Line 283 check (`if pos in position_data:`) will silently drop K/DST metrics if not in dict (epic notes line 99)

#### Change 2: calculate_ranking_metrics_for_season() - Line 544
**Current code:**
```python
positions = ['QB', 'RB', 'WR', 'TE']
```

**New code:**
```python
positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
```

**Source:** Epic notes lines 78-84 specify exact change
**Traceability:** Direct user specification
**Why needed:** Controls which positions are processed in per-week loop (lines 557-580)

#### Documentation Updates (Lines 351, 535)
**Docstrings mentioning position examples:**
- Line 351: "Position to filter ('QB', 'RB', 'WR', 'TE')" → Update to include K, DST
- Line 535: "'position': Player position (QB, RB, WR, TE)" → Update to include K, DST

**Source:** Derived requirement (docstrings should match code)
**Traceability:** Documentation consistency requirement

---

**Files NOT Requiring Changes (verified in research):**

- ✅ **AccuracyResultsManager** - Already handles arbitrary position keys dynamically (lines 107, 176, 207)
- ✅ **Metric calculation methods** - Already position-agnostic (pairwise, top-N, Spearman accept position parameter)
- ✅ **Logging** - Already uses dynamic position variables (f-strings)
- ✅ **Filtering logic** - Already accepts K/DST data (position field matches at lines 364, 430, 491)

**Source:** Research findings (Phase 1)
**Traceability:** Evidence from READ tool calls to AccuracyCalculator.py and AccuracyResultsManager.py

---

## Requirements

### Requirement 1: Add K and DST to Ranking Metric Calculations

**Description:** Include Kicker (K) and Defense/Special Teams (DST) positions in pairwise accuracy, top-N accuracy, and Spearman correlation calculations

**Source:** Epic notes line 14: "Add Kicker (K) and Defense/Special Teams (DST) positions to ranking-based accuracy metrics (pairwise accuracy, top-N accuracy, Spearman correlation)"
**Traceability:** Direct user request (primary epic goal)

**Implementation:**
- Modify positions list at line 544 to include 'K' and 'DST'
- Modify position_data dict at line 258 to include 'K' and 'DST' keys
- Verify all 3 metrics calculate correctly for K/DST data

**Acceptance Criteria:**
- K and DST appear in by_position dictionary with all 5 metrics
- Simulation logs show K/DST ranking metrics during optimization
- Saved config files include K/DST in by_position section

---

### Requirement 2: Maintain Existing Filtering Logic

**Description:** Use existing filtering threshold (actual >= 3.0 points) for K and DST positions

**Source:** Epic notes line 171: "Current filtering (actual >= 3.0) is acceptable for K/DST"
**Traceability:** Direct user constraint (don't change existing logic)

**Implementation:**
- NO changes to lines 364, 430, 491 (existing filters)
- Filters already work generically for any position

**Acceptance Criteria:**
- K players with < 3 points excluded (e.g., kicker scored 0)
- DST with < 3 points excluded (poor performances)
- Filtering behavior consistent with QB/RB/WR/TE

---

### Requirement 3: Update Documentation

**Description:** Update accuracy simulation documentation to reflect all 6 positions in ranking metrics

**Source:** Epic notes line 355: "Documentation updated in `ACCURACY_SIMULATION_FLOW_VERIFIED.md`"
**Traceability:** Direct user request (Must Have acceptance criterion)

**Implementation:**
- Update "Per-Position Metrics" section to note all 6 positions
- Remove caveat about K/DST being MAE-only
- Add note about small sample size considerations (N=32 for K/DST)

**Acceptance Criteria:**
- Documentation no longer states "ranking metrics for QB/RB/WR/TE only"
- K and DST explicitly mentioned in per-position metrics section

---

### Requirement 4: Add Unit Test Coverage for K/DST

**Description:** Add test cases validating K and DST ranking metric calculations

**Source:** Derived requirement
**Traceability:** User requested implementation (epic line 14), testing is logically required to verify correctness

**Implementation:**
- Test pairwise accuracy with K data (discrete scoring: 0, 3, 6, 9)
- Test pairwise accuracy with DST data (including negative scores)
- Test top-N accuracy with small sample size (N=32)
- Test Spearman correlation with K/DST scoring patterns
- Verify existing integration test passes with K/DST

**Acceptance Criteria:**
- All unit tests pass (100% pass rate)
- K-specific and DST-specific test cases added
- Integration test validates by_position includes K and DST keys

---

### Requirement 5: Verify Small Sample Size Handling

**Description:** Confirm ranking metrics handle small sample size (N=32 for K/DST) without errors

**Source:** Derived requirement
**Traceability:** Epic notes line 137 discusses small sample size concern, need to verify graceful handling

**Implementation:**
- Verify top-20 accuracy warning for small pools (epic notes line 106-108)
- Confirm methods return 0.0 if insufficient data (< 2 players)
- Document that top-20 = 62.5% of all kickers (may not be meaningful)

**Acceptance Criteria:**
- No crashes or errors with N=32 sample size
- Appropriate debug logging for small samples
- Metrics calculate correctly (may have higher variance)

---

**Requirements Summary:**

- ✅ Requirement 1: Direct user request (epic line 14) - PRIMARY GOAL
- ✅ Requirement 2: Direct user constraint (epic line 171) - MAINTAIN EXISTING
- ✅ Requirement 3: Direct user request (epic line 355) - DOCUMENTATION
- ✅ Requirement 4: Derived (testing required for correctness)
- ✅ Requirement 5: Derived (handle edge case identified in epic notes)

**Total Requirements:** 5 (3 direct user requests, 2 derived)

---

## Data Structures

### Input Data Format

**Format:** JSON files with position field

**Source:** Research Task 3 verified actual data files
**Traceability:** Epic notes line 221-224 specify checking data files

**Verified Structure:**
```json
{
  "position": "K",
  "name": "Justin Tucker",
  "projected": 9.5,
  "actual": 12.0
}
```

**Position field values:**
- K data: `"position": "K"` (verified in simulation/sim_data/2024/weeks/week_01/k_data.json)
- DST data: `"position": "DST"` (verified in simulation/sim_data/2024/weeks/week_01/dst_data.json)

**Source:** Bash verification in Research Task 3
**Traceability:** Grep output confirming exact position strings

---

### Internal Representation

**AccuracyResult.by_position dictionary:**

**Before (4 positions):**
```python
{
  'QB': RankingMetrics(...),
  'RB': RankingMetrics(...),
  'WR': RankingMetrics(...),
  'TE': RankingMetrics(...)
}
```

**After (6 positions):**
```python
{
  'QB': RankingMetrics(...),
  'RB': RankingMetrics(...),
  'WR': RankingMetrics(...),
  'TE': RankingMetrics(...),
  'K': RankingMetrics(...),
  'DST': RankingMetrics(...)
}
```

**Source:** Epic notes line 348: "AccuracyResult.by_position includes 'K' and 'DST' keys"
**Traceability:** Direct acceptance criterion from epic

---

## Algorithms

### Ranking Metrics Calculation (No Changes)

**Source:** Research verified metric methods are position-agnostic
**Traceability:** Read tool calls to lines 360-520 in AccuracyCalculator.py

**All 3 metrics use identical pattern:**
1. Filter players by position and actual >= 3.0
2. Calculate metric using filtered data
3. Return result (or 0.0 if insufficient data)

**Pairwise Accuracy** (lines 360-390):
- Compares all pairs, counts correct predictions
- Works with any score distribution (ordinal ranking)

**Top-N Accuracy** (lines 425-455):
- Set intersection of predicted top-N vs actual top-N
- Works with any score distribution (set-based)

**Spearman Correlation** (lines 488-520):
- Rank correlation between projected and actual
- Robust to score distribution differences

**K/DST Compatibility:** ✅ All 3 metrics are rank-based, handle K/DST scoring patterns correctly

**Source:** Epic notes lines 158-159: "Ranking metrics are actually MORE appropriate for K/DST than MAE"
**Traceability:** User analysis in epic notes

---

### Edge Case Handling

**Source:** Derived requirements (edge cases discovered during research)

1. **Small sample size (N < 2):**
   - All methods return 0.0 if insufficient players
   - Already implemented at lines 367, 437, 495
   - Works for K/DST

2. **Top-20 with N=32 pool:**
   - Epic notes line 106: "Top-20 accuracy = 62.5% of all kickers (not meaningful)"
   - Will trigger debug log at line 438-440
   - Acceptable behavior (user deferred adaptive top-N)

3. **Zero variance:**
   - Spearman returns NaN if zero variance
   - Already handled at line 502-507 (returns 0.0)
   - Works for K/DST

4. **Ties in actual scores:**
   - Pairwise skips ties at line 381-382
   - Works for K/DST

**Source:** Code inspection during Research Phase
**Traceability:** READ tool calls verified existing edge case handling

---

## Dependencies

**This feature depends on:**

- **Data files:** simulation/sim_data/*/k_data.json and dst_data.json
  - Source: Epic notes line 221-224
  - Status: ✅ Exist and verified (Research Task 3)

- **AccuracyResultsManager.by_position dynamic handling**
  - Source: Research Task 5
  - Status: ✅ Already handles arbitrary position keys (lines 107, 176, 207)

**This feature blocks:** None (only feature in epic)

**This feature is independent of:** All other features (standalone)

---

## Out of Scope (User Explicitly Deferred)

**From Epic Intent section:**

1. **Position-specific top-N thresholds** - Nice to Have (epic line 361)
   - Defer: Epic notes line 129: "Start with simple fix"
2. **Separate logging for K/DST** - Nice to Have (epic line 362)
3. **Performance comparison report** - Nice to Have (epic line 363)
4. **Adaptive Top-N Metrics** - Optional Enhancement (epic lines 103-129)

**Source:** Epic Intent section, lines 50-60
**Traceability:** User explicitly marked as out of scope

---

**Status:** Specification complete with traceability (Stage 2 - STAGE_2b Phase 2)
**Next:** Phase 2.5 - Spec-to-Epic Alignment Check (MANDATORY GATE)
