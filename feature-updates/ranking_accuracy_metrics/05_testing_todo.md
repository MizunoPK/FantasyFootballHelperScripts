# Sub-Feature 5: Comprehensive Testing - Implementation TODO

**Parent Feature:** ranking_accuracy_metrics
**Dependencies:** Sub-features 01, 02, 03, 04 must be complete
**Scope:** Unit tests, integration tests, parallel execution tests

---

## Iteration Progress Tracker

```
R1: □□□□□□□ (0/7)   R2: □□□□□□□□□ (0/9)   R3: □□□□□□□□ (0/8)
```

**Current:** Iteration 1
**Confidence:** HIGH (test writing, clear patterns)
**Blockers:** All previous sub-features must be complete

---

## Implementation Tasks

### Task 5.1: Unit Tests for Pairwise Accuracy

- **File:** `tests/simulation/test_AccuracyCalculator.py`
- **Status:** [ ] Not started

**Test cases (from Q32):**
- Perfect ranking (100% accuracy)
- Random ranking (~50% accuracy)
- Inverse ranking (0% accuracy)
- Ties in projections
- Ties in actuals
- Empty data
- Single player
- Filtering (actual >= 3)

### Task 5.2: Unit Tests for Top-N Accuracy

- **File:** `tests/simulation/test_AccuracyCalculator.py`
- **Status:** [ ] Not started

**Test cases:**
- Perfect overlap (100%)
- No overlap (0%)
- Partial overlap
- N values: 5, 10, 20
- Per-position separation

### Task 5.3: Unit Tests for Spearman Correlation

- **File:** `tests/simulation/test_AccuracyCalculator.py`
- **Status:** [ ] Not started

**Test cases:**
- Perfect correlation (+1.0)
- No correlation (0.0)
- Inverse correlation (-1.0)
- Compare to hand-calculated examples (Q33)
- Verify scipy.spearmanr matches expected
- Zero-variance edge case

### Task 5.4: Integration Test for Full Simulation

- **File:** `tests/simulation/test_AccuracySimulationManager.py`
- **Status:** [ ] Not started

**Test scenarios:**
- Run simulation with small dataset
- Verify all metrics calculated
- Verify best config selected by pairwise_accuracy
- Verify per-position metrics
- Verify JSON output structure
- Use real objects (not excessive mocking)

### Task 5.5: Parallel Execution Test

- **File:** `tests/simulation/test_ParallelAccuracyRunner.py`
- **Status:** [ ] Not started

**Verify:**
- Ranking metrics are parallel-safe
- Results serialize across processes
- Run with ProcessPoolExecutor

### QA CHECKPOINT 5: All Tests Passing

- **Test command:** `python tests/run_all_tests.py`
- **Verify:**
  - [ ] All unit tests pass (100%)
  - [ ] All integration tests pass
  - [ ] Parallel execution tests pass
  - [ ] No errors or warnings

---

## Sub-Feature Completion Checklist

- [ ] All previous sub-features complete
- [ ] All 24 verification iterations complete
- [ ] All test tasks complete
- [ ] QA checkpoint passed (100% tests passing)
- [ ] Changes committed with message: "Phase 5 (testing): Add comprehensive tests for ranking metrics"

---

## Final Feature Completion

After this sub-feature is complete and committed:
- [ ] Run final E2E validation
- [ ] Review all lessons learned
- [ ] Move entire feature folder to done/
- [ ] Final commit: "Complete ranking_accuracy_metrics feature"
