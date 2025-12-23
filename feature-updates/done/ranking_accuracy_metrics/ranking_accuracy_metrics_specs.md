# Ranking Accuracy Metrics

## Objective

Replace Mean Absolute Error (MAE) with ranking-based accuracy metrics in the accuracy simulation system. This will produce optimal configs that actually help with fantasy football decisions by correctly identifying relative player value rather than minimizing prediction error.

---

## High-Level Requirements

### 1. New Ranking Metrics

**Primary Metric: Pairwise Decision Accuracy**
- For every pair of players at the same position, determine if our scoring correctly predicts which player will score more fantasy points
- Metric value: Percentage of pairwise comparisons where prediction matches actual result (0.0-1.0)
- This is the PRIMARY optimization target (replaces MAE)

**Secondary Metrics:**

- **Top-N Overlap Accuracy**
  - How many of our top-N predicted players are actually in the top-N scorers?
  - Calculate for multiple N values: top 5, top 10, top 20
  - Per-position calculation
  - Metric value: Percentage overlap (0.0-1.0)

- **Spearman Rank Correlation**
  - Statistical measure of ranking order similarity
  - Range: -1.0 (perfect inverse) to +1.0 (perfect match)
  - Standard statistical measure for validation

**Positional Breakdown:**
- All metrics calculated separately for QB, RB, WR, TE
- Allows identification of which scoring features help which positions

### 2. Integration with Accuracy Simulation

- Modify AccuracySimulationManager to optimize for pairwise accuracy instead of MAE
- Best config = highest pairwise accuracy (not lowest MAE)
- Keep MAE calculation as diagnostic metric (for comparison)
- Results include all metrics for analysis

### 3. Output Format

Results should include comprehensive metrics:
```json
{
  "config_id": "...",
  "pairwise_accuracy": 0.68,
  "top_5_accuracy": 0.80,
  "top_10_accuracy": 0.75,
  "top_20_accuracy": 0.70,
  "spearman_correlation": 0.82,
  "mae": 3.45,  // diagnostic only
  "by_position": {
    "QB": {
      "pairwise_accuracy": 0.71,
      "top_10_accuracy": 0.80,
      "spearman_correlation": 0.85,
      "mae": 2.1
    },
    "RB": {
      "pairwise_accuracy": 0.66,
      "top_10_accuracy": 0.70,
      "spearman_correlation": 0.78,
      "mae": 3.8
    },
    "WR": {
      "pairwise_accuracy": 0.65,
      "top_10_accuracy": 0.65,
      "spearman_correlation": 0.75,
      "mae": 4.2
    },
    "TE": {
      "pairwise_accuracy": 0.72,
      "top_10_accuracy": 0.85,
      "spearman_correlation": 0.88,
      "mae": 2.5
    }
  }
}
```

---

## Open Questions (To Be Resolved)

*Will be populated during Phase 2 investigation*

---

## Resolved Implementation Details

*Will be populated during Phase 4 as checklist items are resolved*

---

## Expected Outcomes

### Before (MAE Optimization):
```
TEAM_QUALITY_SCORING   WEIGHT: 0.0    ← Disabled
PERFORMANCE_SCORING    WEIGHT: 0.01   ← Disabled
MATCHUP_SCORING        WEIGHT: 0.03   ← Disabled
MAE: 3.33 points
Pairwise Accuracy: ~55-60% (estimated)
```

### After (Ranking Accuracy Optimization):
```
TEAM_QUALITY_SCORING   WEIGHT: 0.5-2.0  ← Enabled
PERFORMANCE_SCORING    WEIGHT: 2.0-4.0  ← Enabled
MATCHUP_SCORING        WEIGHT: 1.0-3.0  ← Enabled
MAE: 3.8-4.2 points (slightly higher, acceptable)
Pairwise Accuracy: 68-72% (much better decisions)
```

### Benefits:
- ✓ Accuracy simulation produces configs that actually help with decisions
- ✓ Aligns accuracy optimization with win-rate optimization
- ✓ Validates that scoring features provide value
- ✓ Can confidently use accuracy-optimal configs for starter decisions
- ✓ Better understanding of which features help which positions

---

## Implementation Notes

### Files to Modify
*Will be identified during Phase 2 investigation*

### Dependencies
*Will be identified during Phase 2 investigation*

### Reusable Code
*Will be identified during Phase 2 investigation*

### Testing Strategy
*Will be defined during Phase 2 investigation*

---

## Status: PLANNING (Phase 1 Complete)
