# Sub-Feature 2: RankingMetrics Data Structure - Implementation TODO

**Parent Feature:** ranking_accuracy_metrics
**Dependencies:** Sub-feature 01 (core_metrics) must be complete
**Scope:** Create RankingMetrics dataclass and extend AccuracyConfigPerformance

---

## Iteration Progress Tracker

### Compact View (Quick Status)

```
R1: □□□□□□□ (0/7)   R2: □□□□□□□□□ (0/9)   R3: □□□□□□□□ (0/8)
```

**Current:** Iteration 1
**Confidence:** HIGH (narrow scope, clear pattern)
**Blockers:** Sub-feature 01 must be complete

### Detailed View

| Round | Iterations | Status |
|-------|------------|--------|
| First (7) | [ ]1 [ ]2 [ ]3 [ ]4 [ ]5 [ ]6 [ ]7 | 0/7 |
| Second (9) | [ ]8 [ ]9 [ ]10 [ ]11 [ ]12 [ ]13 [ ]14 [ ]15 [ ]16 | 0/9 |
| Third (8) | [ ]17 [ ]18 [ ]19 [ ]20 [ ]21 [ ]22 [ ]23 [ ]24 | 0/8 |

---

## Implementation Tasks

### Task 2.1: Create RankingMetrics Dataclass

- **File:** `simulation/accuracy/AccuracyResultsManager.py` (add at top after imports)
- **Similar to:** AccuracyResult dataclass in AccuracyCalculator.py:27-51
- **Status:** [ ] Not started

**Implementation (from Q11):**
```python
from dataclasses import dataclass

@dataclass
class RankingMetrics:
    """
    Ranking-based accuracy metrics for a configuration.

    Attributes:
        pairwise_accuracy (float): % of pairwise comparisons correct (0.0-1.0)
        top_5_accuracy (float): % overlap in top-5 predictions (0.0-1.0)
        top_10_accuracy (float): % overlap in top-10 predictions (0.0-1.0)
        top_20_accuracy (float): % overlap in top-20 predictions (0.0-1.0)
        spearman_correlation (float): Rank correlation coefficient (-1.0 to +1.0)
    """
    pairwise_accuracy: float
    top_5_accuracy: float
    top_10_accuracy: float
    top_20_accuracy: float
    spearman_correlation: float
```

### Task 2.2: Extend AccuracyConfigPerformance with Ranking Metrics

- **File:** `simulation/accuracy/AccuracyResultsManager.py:45-150`
- **Status:** [ ] Not started

**Changes:**
1. Add fields to `__init__` (line ~61):
```python
def __init__(
    self,
    config_dict: dict,
    mae: float,
    player_count: int,
    total_error: float,
    config_id: Optional[str] = None,
    timestamp: Optional[str] = None,
    param_name: Optional[str] = None,
    test_idx: Optional[int] = None,
    base_horizon: Optional[str] = None,
    overall_metrics: Optional[RankingMetrics] = None,  # NEW
    by_position: Optional[Dict[str, RankingMetrics]] = None  # NEW
) -> None:
    # ... existing code ...
    self.overall_metrics = overall_metrics
    self.by_position = by_position or {}
```

2. Update `is_better_than()` method (line ~90-116):
```python
def is_better_than(self, other: 'AccuracyConfigPerformance') -> bool:
    """
    Check if this configuration is better than another.

    Uses pairwise_accuracy as primary metric (from Q12).
    Falls back to MAE if ranking metrics not available (backward compat).
    """
    # Reject invalid configs
    if self.player_count == 0:
        return False

    if other is None:
        return True

    if other.player_count == 0:
        return False

    # Use ranking metrics if available (Q12)
    if self.overall_metrics and other.overall_metrics:
        return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy

    # Fallback to MAE for backward compat (Q25)
    return self.mae < other.mae
```

3. Update `to_dict()` method (line ~118-127):
```python
def to_dict(self) -> dict:
    """Convert to dictionary for JSON serialization."""
    result = {
        'config_id': self.config_id,
        'mae': self.mae,
        'player_count': self.player_count,
        'total_error': self.total_error,
        'timestamp': self.timestamp,
        'config': self.config_dict
    }

    # Add ranking metrics if available
    if self.overall_metrics:
        result['pairwise_accuracy'] = self.overall_metrics.pairwise_accuracy
        result['top_5_accuracy'] = self.overall_metrics.top_5_accuracy
        result['top_10_accuracy'] = self.overall_metrics.top_10_accuracy
        result['top_20_accuracy'] = self.overall_metrics.top_20_accuracy
        result['spearman_correlation'] = self.overall_metrics.spearman_correlation

    if self.by_position:
        result['by_position'] = {
            pos: {
                'pairwise_accuracy': metrics.pairwise_accuracy,
                'top_5_accuracy': metrics.top_5_accuracy,
                'top_10_accuracy': metrics.top_10_accuracy,
                'top_20_accuracy': metrics.top_20_accuracy,
                'spearman_correlation': metrics.spearman_correlation,
                'mae': 0.0  # Placeholder, will be added in sub-feature 3
            }
            for pos, metrics in self.by_position.items()
        }

    return result
```

4. Update `from_dict()` method (line ~129-147):
```python
@classmethod
def from_dict(cls, data: dict) -> 'AccuracyConfigPerformance':
    """Create from dictionary (with backward compat for Q25)."""
    mae = data['mae']
    player_count = data['player_count']
    total_error = data.get('total_error', mae * player_count)

    # Load ranking metrics if available (Q25 backward compat)
    overall_metrics = None
    if 'pairwise_accuracy' in data:
        overall_metrics = RankingMetrics(
            pairwise_accuracy=data['pairwise_accuracy'],
            top_5_accuracy=data['top_5_accuracy'],
            top_10_accuracy=data['top_10_accuracy'],
            top_20_accuracy=data['top_20_accuracy'],
            spearman_correlation=data['spearman_correlation']
        )

    # Load per-position metrics if available
    by_position = {}
    if 'by_position' in data:
        for pos, metrics_dict in data['by_position'].items():
            by_position[pos] = RankingMetrics(
                pairwise_accuracy=metrics_dict['pairwise_accuracy'],
                top_5_accuracy=metrics_dict['top_5_accuracy'],
                top_10_accuracy=metrics_dict['top_10_accuracy'],
                top_20_accuracy=metrics_dict['top_20_accuracy'],
                spearman_correlation=metrics_dict['spearman_correlation']
            )

    return cls(
        config_dict=data['config'],
        mae=mae,
        player_count=player_count,
        total_error=total_error,
        config_id=data.get('config_id'),
        timestamp=data.get('timestamp'),
        overall_metrics=overall_metrics,
        by_position=by_position
    )
```

### QA CHECKPOINT 2: Data Structure Complete

- **Status:** [ ] Not started
- **Test command:** `python -m pytest tests/simulation/test_AccuracyResultsManager.py -v`
- **Verify:**
  - [ ] RankingMetrics can be created
  - [ ] AccuracyConfigPerformance accepts new fields
  - [ ] is_better_than() uses pairwise_accuracy
  - [ ] to_dict() includes ranking metrics
  - [ ] from_dict() handles old format (no ranking metrics)
  - [ ] from_dict() handles new format (with ranking metrics)

---

## Algorithm Traceability Matrix

| Spec Section | Algorithm | Code Location |
|--------------|-----------|---------------|
| Q11 | Nested structure with RankingMetrics | RankingMetrics dataclass + AccuracyConfigPerformance fields |
| Q12 | Primary metric = pairwise_accuracy | is_better_than() method |
| Q25 | Backward compatibility | from_dict() checks for ranking metrics, uses MAE fallback |

---

## Progress Notes

**Last Updated:** 2025-12-21 18:20
**Current Status:** Sub-feature TODO created, awaiting sub-feature 01 completion
**Blockers:** Sub-feature 01 must be complete before starting

---

## Sub-Feature Completion Checklist

- [ ] Sub-feature 01 complete (DEPENDENCY)
- [ ] All 24 verification iterations complete
- [ ] Interface verification complete
- [ ] All implementation tasks complete
- [ ] QA checkpoint passed
- [ ] Unit tests passing (100%)
- [ ] Code changes documented
- [ ] Lessons learned captured
- [ ] Changes committed with message: "Phase 2 (data-structure): Add RankingMetrics and extend AccuracyConfigPerformance"
