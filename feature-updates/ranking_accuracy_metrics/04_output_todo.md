# Sub-Feature 4: Results Output - Implementation TODO

**Parent Feature:** ranking_accuracy_metrics
**Dependencies:** Sub-features 01, 02, 03 must be complete
**Scope:** Update JSON output, console display, success warnings

---

## Iteration Progress Tracker

```
R1: □□□□□□□ (0/7)   R2: □□□□□□□□□ (0/9)   R3: □□□□□□□□ (0/8)
```

**Current:** Iteration 1
**Confidence:** HIGH (simple formatting/logging)
**Blockers:** Sub-features 01, 02, 03 must be complete

---

## Implementation Tasks

### Task 4.1: Extend JSON Output

- **File:** `simulation/accuracy/AccuracyResultsManager.py`
- **Location:** save_optimal_configs() method
- **Status:** [ ] Not started

**Note:** AccuracyConfigPerformance.to_dict() already includes ranking metrics (from sub-feature 02), so JSON output should automatically include them. Verify this works correctly.

### Task 4.2: Update Console Output

- **File:** `simulation/accuracy/AccuracySimulationManager.py`
- **Location:** Logging statements during config evaluation
- **Status:** [ ] Not started

**Implementation (from Q30):**
```python
self.logger.info(
    f"Config {config_id} | "
    f"Pairwise: {overall_metrics.pairwise_accuracy:.1%} | "
    f"Top-10: {overall_metrics.top_10_accuracy:.1%} | "
    f"Spearman: {overall_metrics.spearman_correlation:.2f} | "
    f"MAE: {mae:.2f} (diag)"
)
```

### QA CHECKPOINT 4: Output Complete

- **Test:** Run E2E simulation, inspect output
- **Verify:**
  - [ ] JSON contains all ranking metrics
  - [ ] Console shows ranking metrics prominently
  - [ ] MAE marked as diagnostic
  - [ ] Old results files still loadable

---

## Sub-Feature Completion Checklist

- [ ] Sub-features 01, 02, 03 complete
- [ ] All 24 verification iterations complete
- [ ] Tasks complete
- [ ] Changes committed with message: "Phase 4 (output): Update results display for ranking metrics"
