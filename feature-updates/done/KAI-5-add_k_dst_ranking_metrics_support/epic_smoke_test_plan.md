# Epic Smoke Test Plan: add_k_dst_ranking_metrics_support

**Purpose:** Define how to validate the complete epic end-to-end

**Created:** 2026-01-08 (Stage 1)
**Last Updated:** 2026-01-09 (Stage 5e)

**⚠️ VERSION: STAGE 5e (Updated after feature implementation)**
- Created: 2026-01-08 (Stage 1)
- Last Updated: 2026-01-09 (Stage 5e)
- Based on: ACTUAL implementation from Feature 1 (add K/DST ranking metrics)
- Quality: VALIDATED - Specific tests based on actual code and QC findings
- Next Update: Stage 6 (after epic testing - will mark results)

---

## Epic Success Criteria

**The epic is successful if ALL of these criteria are met:**

### Criterion 1: K and DST Added to Position Lists
✅ **MEASURABLE:** Verify AccuracyCalculator.py line 258 and 544 include K and DST
- Line 258: `position_data = {'QB': {}, 'RB': {}, 'WR': {}, 'TE': {}, 'K': {}, 'DST': {}}`
- Line 544: `positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']`

**Verification:** Read AccuracyCalculator.py lines 258 and 544, confirm K and DST present

---

### Criterion 2: by_position Dictionary Contains All 6 Positions
✅ **MEASURABLE:** Run accuracy simulation and verify AccuracyResult.by_position has 6 keys
- Expected keys: 'QB', 'RB', 'WR', 'TE', 'K', 'DST'
- Each key has RankingMetrics with 5 values (pairwise, top-5, top-10, top-20, spearman)

**Verification:**
```python
# After running accuracy simulation
result = accuracy_calculator.calculate_ranking_metrics_for_season(player_data)
overall_metrics, by_position = result
assert len(by_position) == 6, f"Expected 6 positions, got {len(by_position)}"
assert 'K' in by_position, "K missing from by_position"
assert 'DST' in by_position, "DST missing from by_position"
```

---

### Criterion 3: K/DST Metrics Are Non-Zero
✅ **MEASURABLE:** Verify K and DST metrics have realistic values (not 0.0 or NaN)
- Pairwise accuracy > 0 and < 1.0
- Top-N accuracy values > 0 and < 1.0
- Spearman correlation between -1.0 and 1.0

**Verification:**
```python
k_metrics = by_position['K']
assert k_metrics.pairwise_accuracy > 0.0, "K pairwise is zero"
assert k_metrics.top_5_accuracy > 0.0, "K top-5 is zero"

dst_metrics = by_position['DST']
assert dst_metrics.pairwise_accuracy > 0.0, "DST pairwise is zero"
assert dst_metrics.spearman_correlation != 0.0, "DST Spearman is zero"
```

---

### Criterion 4: All Unit Tests Pass (100%)
✅ **MEASURABLE:** Run full test suite with exit code 0
- All existing tests continue to pass
- New K/DST test cases added and passing

**Verification:**
```bash
python tests/run_all_tests.py
echo "Exit code: $?"  # Should be 0
```

---

### Criterion 5: Documentation Updated
✅ **MEASURABLE:** ACCURACY_SIMULATION_FLOW_VERIFIED.md reflects all 6 positions
- No longer states "ranking metrics for QB/RB/WR/TE only"
- Explicitly mentions K and DST in per-position metrics section

**Verification:** Read docs/simulation/ACCURACY_SIMULATION_FLOW_VERIFIED.md, confirm K/DST mentioned

---

## Update History

**Track when and why this plan was updated:**

| Date | Stage | Feature | What Changed | Why |
|------|-------|---------|--------------|-----|
| 2026-01-08 | Stage 1 | (initial) | Initial plan created | Epic planning based on assumptions |
| 2026-01-08 | Stage 4 | (all features) | **MAJOR UPDATE** | Based on feature spec and research findings |
| 2026-01-09 | Stage 5e | Feature 1 | **MINOR ADDITIONS** | Based on ACTUAL implementation and QC findings |

**Stage 4 changes:**
- Added 5 measurable success criteria (was vague assumptions)
- Created 4 specific test scenarios with Python commands
- Documented integration points (N/A - single feature)
- Added concrete verification steps for each criterion
- Replaced TBD commands with actual Python/bash code

**Stage 5e changes (2026-01-09):**
- Added Test Scenario 5: Performance Impact Verification
  - Rationale: QC Round 2 (Validation 2.6) measured +42.04% impact
  - Ensures < 1 second execution time threshold
- Added Test Scenario 6: Edge Case Handling
  - Rationale: QC Round 2 (Validation 2.5) tested 6 specific edge cases
  - Covers empty data, N=1, filtered players, perfect/worst predictions, mixed weeks
- Added Test Scenario 7: Filtering Behavior Verification
  - Rationale: QC Round 2 (Validation 2.4) verified >= 3.0 filter for K/DST
  - Ensures position-agnostic filtering works correctly
- Updated Category 1 with specific edge case tests from implementation
- Implementation matched test plan expectations (no major surprises)

**Current version is informed by:**
- Stage 1: Initial assumptions from epic request
- Stage 4: Feature spec from Stages 2-3, research findings
- **Stage 5e: ACTUAL implementation from Feature 1 (K/DST ranking metrics)** ← YOU ARE HERE

**Next update:** Stage 6 after epic testing (will mark execution results)

---

## Specific Test Scenarios

**These tests MUST be run for epic-level validation:**

### Test Scenario 1: Import and Module Verification

**Purpose:** Verify AccuracyCalculator module imports without errors

**Steps:**
```bash
python -c "from simulation.accuracy.AccuracyCalculator import AccuracyCalculator; print('Import successful')"
```

**Expected Results:**
✅ Module imports without ImportError
✅ Prints "Import successful"

**Failure Indicators:**
❌ ImportError → Syntax error in AccuracyCalculator.py
❌ ModuleNotFoundError → File path incorrect

---

### Test Scenario 2: Position Lists Verification

**Purpose:** Verify K and DST added to hardcoded positions lists

**Steps:**
```python
from simulation.accuracy.AccuracyCalculator import AccuracyCalculator
import inspect

# Read source code to verify changes
source = inspect.getsource(AccuracyCalculator)

# Check line 258 area (aggregate_season_results method)
assert "'K'" in source and "'DST'" in source, "K or DST missing from source"
print("✅ K and DST found in AccuracyCalculator source")
```

**Expected Results:**
✅ Source code contains 'K' and 'DST' strings
✅ Both positions added to position_data dict and positions list

**Failure Indicators:**
❌ K or DST not found → Code changes not applied
❌ Only found in comments → Changes not in actual code

---

### Test Scenario 3: K/DST Ranking Metrics Calculation

**Purpose:** Verify ranking metrics calculate correctly for K and DST positions

**Steps:**
```python
from simulation.accuracy.AccuracyCalculator import AccuracyCalculator

# Create test data for K position
k_test_data = {
    1: [  # Week 1
        {'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 12.0},
        {'position': 'K', 'name': 'K2', 'projected': 8.0, 'actual': 6.0},
        {'position': 'K', 'name': 'K3', 'projected': 7.0, 'actual': 9.0},
    ]
}

calc = AccuracyCalculator()
overall, by_position = calc.calculate_ranking_metrics_for_season(k_test_data)

# Verify K metrics calculated
assert 'K' in by_position, "K not in by_position dict"
k_metrics = by_position['K']
assert k_metrics.pairwise_accuracy > 0.0, "K pairwise is 0.0"
assert k_metrics.top_5_accuracy >= 0.0, "K top-5 is invalid"
print(f"✅ K metrics: pairwise={k_metrics.pairwise_accuracy:.3f}")
```

**Expected Results:**
✅ 'K' key exists in by_position dictionary
✅ K metrics have realistic values (pairwise > 0, top-N >= 0, spearman calculated)
✅ No NaN or None values

**Failure Indicators:**
❌ 'K' not in by_position → K not added to positions list (line 544)
❌ Metrics are 0.0 or NaN → Calculation error
❌ KeyError → K added to line 544 but not line 258 (silent drop bug)

---

### Test Scenario 4: Integration Test Validation

**Purpose:** Verify existing integration test passes with K/DST support

**Steps:**
```bash
python -m pytest tests/integration/test_accuracy_simulation_integration.py -v
```

**Expected Results:**
✅ All integration tests pass
✅ Test validates by_position includes K and DST keys
✅ No regression in existing QB/RB/WR/TE tests

**Failure Indicators:**
❌ Test fails → Integration issue with K/DST
❌ KeyError on 'K' or 'DST' → Position not properly integrated
❌ Assertion failure on position count → Expected 6, got 4

---

### Test Scenario 5: Performance Impact Verification

**Purpose:** Verify adding K/DST positions does not cause unacceptable performance degradation

**Steps:**
```python
import time
from simulation.accuracy.AccuracyCalculator import AccuracyCalculator

# Create test data with all 6 positions (85 players/week, 17 weeks)
test_data_6pos = {week: [
    *[{'position': 'QB', 'name': f'QB{i}', 'projected': 25.0-i, 'actual': 24.0-i+(week%3)} for i in range(10)],
    *[{'position': 'RB', 'name': f'RB{i}', 'projected': 20.0-i*0.5, 'actual': 19.0-i*0.5+(week%4)} for i in range(20)],
    *[{'position': 'WR', 'name': f'WR{i}', 'projected': 18.0-i*0.3, 'actual': 17.0-i*0.3+(week%5)} for i in range(25)],
    *[{'position': 'TE', 'name': f'TE{i}', 'projected': 12.0-i*0.5, 'actual': 11.0-i*0.5+(week%2)} for i in range(10)],
    *[{'position': 'K', 'name': f'K{i}', 'projected': 9.0-i*0.3, 'actual': 9.0-i*0.3+(week%3)} for i in range(10)],
    *[{'position': 'DST', 'name': f'DST{i}', 'projected': 12.0-i*0.5, 'actual': 12.0-i*0.5+(week%4)} for i in range(10)],
] for week in range(1, 18)}

calc = AccuracyCalculator()

# Measure performance
start = time.time()
for _ in range(3):  # 3 runs for average
    overall, by_position = calc.calculate_ranking_metrics_for_season(test_data_6pos)
elapsed = (time.time() - start) / 3

print(f"Average time: {elapsed:.4f}s")
assert elapsed < 1.0, f"Performance unacceptable: {elapsed:.4f}s >= 1.0s"
print("✅ Performance acceptable (< 1 second)")
```

**Expected Results:**
✅ Average execution time < 1.0 second
✅ Performance impact within acceptable threshold (measured +42% during QC)
✅ All 6 positions calculate correctly

**Failure Indicators:**
❌ Time >= 1.0s → Unacceptable performance degradation
❌ Crash or error → K/DST causing algorithmic issues

**Implementation Notes:**
- During QC Round 2 (Validation 2.6), measured +42.04% impact (6.94ms)
- Within 50% threshold documented in spec.md
- Baseline (4 pos): 0.0165s, New (6 pos): 0.0234s

---

### Test Scenario 6: Edge Case Handling

**Purpose:** Verify edge cases discovered during implementation are handled gracefully

**Steps:**
```python
from simulation.accuracy.AccuracyCalculator import AccuracyCalculator

calc = AccuracyCalculator()

# Edge Case 1: Empty K/DST data (no players)
test_empty = {1: [
    {'position': 'QB', 'name': 'QB1', 'projected': 25.0, 'actual': 28.0},
]}
overall, by_pos = calc.calculate_ranking_metrics_for_season(test_empty)
assert 'K' in by_pos and 'DST' in by_pos, "K/DST missing when no players"
assert by_pos['K'].pairwise_accuracy == 0.0, "K should return 0.0 when empty"
print("✅ Edge Case 1: Empty K/DST handled")

# Edge Case 2: Single player (N=1, insufficient for pairwise)
test_single = {1: [
    {'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 9.0},
]}
overall, by_pos = calc.calculate_ranking_metrics_for_season(test_single)
assert by_pos['K'].pairwise_accuracy == 0.0, "N=1 should return 0.0"
print("✅ Edge Case 2: Single player (N=1) handled")

# Edge Case 3: All players filtered (< 3.0 actual)
test_filtered = {1: [
    {'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 0.0},
    {'position': 'K', 'name': 'K2', 'projected': 8.0, 'actual': 2.0},
]}
overall, by_pos = calc.calculate_ranking_metrics_for_season(test_filtered)
assert by_pos['K'].pairwise_accuracy == 0.0, "All filtered should return 0.0"
print("✅ Edge Case 3: All filtered players handled")

# Edge Case 4: Perfect predictions
test_perfect = {1: [
    {'position': 'K', 'name': 'K1', 'projected': 12.0, 'actual': 12.0},
    {'position': 'K', 'name': 'K2', 'projected': 9.0, 'actual': 9.0},
    {'position': 'K', 'name': 'K3', 'projected': 6.0, 'actual': 6.0},
]}
overall, by_pos = calc.calculate_ranking_metrics_for_season(test_perfect)
assert by_pos['K'].pairwise_accuracy == 1.0, "Perfect should return 1.0"
print("✅ Edge Case 4: Perfect predictions handled")

# Edge Case 5: Worst predictions
test_worst = {1: [
    {'position': 'K', 'name': 'K1', 'projected': 12.0, 'actual': 3.0},
    {'position': 'K', 'name': 'K2', 'projected': 9.0, 'actual': 6.0},
    {'position': 'K', 'name': 'K3', 'projected': 6.0, 'actual': 9.0},
]}
overall, by_pos = calc.calculate_ranking_metrics_for_season(test_worst)
assert by_pos['K'].pairwise_accuracy == 0.0, "Worst should return 0.0"
print("✅ Edge Case 5: Worst predictions handled")

# Edge Case 6: Mixed multi-week data
test_mixed = {
    1: [{'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 12.0},
        {'position': 'K', 'name': 'K2', 'projected': 8.0, 'actual': 9.0}],
    2: [{'position': 'QB', 'name': 'QB1', 'projected': 25.0, 'actual': 28.0}],  # No K
    3: [{'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 6.0},
        {'position': 'K', 'name': 'K2', 'projected': 8.0, 'actual': 9.0}],
}
overall, by_pos = calc.calculate_ranking_metrics_for_season(test_mixed)
assert 'K' in by_pos, "K should be present in mixed weeks"
print("✅ Edge Case 6: Mixed multi-week data handled")

print("✅ All 6 edge cases handled gracefully")
```

**Expected Results:**
✅ All 6 edge cases return appropriate values (0.0 or 1.0 as expected)
✅ No crashes, no NaN values
✅ Graceful handling of empty data, single player, filtered players

**Failure Indicators:**
❌ NaN values → Zero variance handling broken
❌ Crash on N=1 → Insufficient data check missing
❌ KeyError → Position not initialized correctly

**Implementation Notes:**
- All 6 edge cases tested during QC Round 2 (Validation 2.5)
- Verified no crashes, no NaN, correct 0.0/1.0 returns

---

### Test Scenario 7: Filtering Behavior Verification

**Purpose:** Verify >= 3.0 actual points filter works correctly for K and DST positions

**Steps:**
```python
from simulation.accuracy.AccuracyCalculator import AccuracyCalculator

calc = AccuracyCalculator()

# Test K filtering with mixed scores (some < 3.0, some >= 3.0)
test_k_filter = {1: [
    {'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 9.0},   # included
    {'position': 'K', 'name': 'K2', 'projected': 8.0, 'actual': 2.0},   # excluded (< 3.0)
    {'position': 'K', 'name': 'K3', 'projected': 7.0, 'actual': 6.0},   # included
]}

result = calc.calculate_pairwise_accuracy(test_k_filter[1], 'K')
# If filtering works, K2 (actual=2.0) is excluded, leaving K1 and K3
# K1 (proj=9.0) vs K3 (proj=7.0): K1 projected higher
# K1 (actual=9.0) vs K3 (actual=6.0): K1 actually higher
# Prediction correct → pairwise = 1.0
assert result == 1.0, f"K filtering failed: expected 1.0, got {result}"
print(f"✅ K filtering works: pairwise={result:.3f} (K2 with actual=2.0 excluded)")

# Test DST filtering
test_dst_filter = {1: [
    {'position': 'DST', 'name': 'DST1', 'projected': 12.0, 'actual': 15.0},  # included
    {'position': 'DST', 'name': 'DST2', 'projected': 11.0, 'actual': 1.0},   # excluded (< 3.0)
    {'position': 'DST', 'name': 'DST3', 'projected': 10.0, 'actual': 8.0},   # included
]}

result_dst = calc.calculate_pairwise_accuracy(test_dst_filter[1], 'DST')
assert result_dst == 1.0, f"DST filtering failed: expected 1.0, got {result_dst}"
print(f"✅ DST filtering works: pairwise={result_dst:.3f} (DST2 with actual=1.0 excluded)")

print("✅ >= 3.0 filter works correctly for K and DST")
```

**Expected Results:**
✅ Players with actual < 3.0 excluded from calculations
✅ K and DST use same filter as QB/RB/WR/TE (position-agnostic)
✅ Pairwise accuracy calculates correctly after filtering

**Failure Indicators:**
❌ Players with actual < 3.0 included → Filter not applied
❌ Different filter threshold for K/DST → Position-specific logic added (wrong)
❌ Incorrect pairwise values → Filter changed comparison logic

**Implementation Notes:**
- Filtering logic at lines 364, 430, 491 already position-agnostic
- Verified during QC Round 2 (Validation 2.4) - Requirement 2
- No code changes to filters (correct behavior preserved)

---

## High-Level Test Categories

**Agent will create additional scenarios for these categories during Stage 5e:**

### Category 1: Edge Case Handling
**What to test:** Small sample size (N=32 for K/DST) handled correctly
**Known edge cases:**
- Top-20 accuracy with only 32 total players (debug warning expected)
- Zero variance in scores (Spearman returns 0.0)
- Ties in actual scores (pairwise skips ties)

**Stage 5e added (2026-01-09):** Test Scenario 6 with 6 specific edge cases:
1. Empty K/DST data (no players) → returns 0.0
2. Single player (N=1) → returns 0.0
3. All players filtered (< 3.0 actual) → returns 0.0
4. Perfect predictions → returns 1.0
5. Worst predictions → returns 0.0
6. Mixed multi-week data → averages correctly

**Verified:** All edge cases tested during Feature 1 QC Round 2 (Validation 2.5)

---

### Category 2: Cross-Season Aggregation
**What to test:** K/DST metrics aggregate correctly across multiple seasons
**Known aggregation points:**
- Line 258: position_data dict controls aggregation
- Line 283: `if pos in position_data:` check (K/DST must be in dict)

**Stage 5e will add:** Multi-season aggregation tests

---

### Category 3: Data Quality Verification
**What to test:** K/DST metrics have realistic values
**Known quality checks:**
- Pairwise accuracy: 0.0 to 1.0 (not NaN)
- Top-N accuracy: 0.0 to 1.0 (may be lower for small N)
- Spearman correlation: -1.0 to 1.0

**Stage 5e will add:** Threshold checks for unrealistic values

---

## Execution Checklist (For Stage 6)

**Part 1: Import Tests**
- [x] Scenario 1: Import and Module Verification - ✅ PASSED

**Part 2: Code Verification Tests**
- [x] Scenario 2: Position Lists Verification - ✅ PASSED

**Part 3: Functional Tests**
- [x] Scenario 3: K/DST Ranking Metrics Calculation - ✅ PASSED (K pairwise=0.667, spearman=0.500)

**Part 4: Integration Tests**
- [x] Scenario 4: Integration Test Validation - ✅ PASSED (14/14 tests)

**Part 5: Implementation-Specific Tests (Added Stage 5e)**
- [x] Scenario 5: Performance Impact Verification - ✅ PASSED (0.0240s < 1.0s threshold)
- [x] Scenario 6: Edge Case Handling (6 cases) - ✅ PASSED (all 6 cases handled correctly)
- [x] Scenario 7: Filtering Behavior Verification - ✅ PASSED (>= 3.0 filter works for K/DST)

**Part 6: Success Criteria Validation**
- [x] Criterion 1: K and DST Added to Position Lists - ✅ PASSED
- [x] Criterion 2: by_position Dictionary Contains All 6 Positions - ✅ PASSED
- [x] Criterion 3: K/DST Metrics Are Non-Zero - ✅ PASSED (K/DST both > 0.0)
- [x] Criterion 4: All Unit Tests Pass (100%) - ✅ PASSED (2,485/2,485 tests)
- [x] Criterion 5: Documentation Updated - ✅ PASSED

**Overall Status:** ✅ COMPLETE (Executed 2026-01-09 - ALL PASSED, ZERO ISSUES)
**Total Scenarios:** 7 (4 from Stage 4 + 3 from Stage 5e)
**Issues Found:** 0

---

## Notes

**Testing Environment:**
- Requires: simulation/sim_data/ with K and DST JSON files
- Requires: Existing accuracy simulation setup
- Prerequisites: Python environment with all dependencies

**Known Considerations:**
- Small sample size for K/DST (32 players each) may result in different metric values than QB/RB/WR/TE
- Top-N thresholds may not be as meaningful for K/DST (top-20 = 62.5% of all kickers)
