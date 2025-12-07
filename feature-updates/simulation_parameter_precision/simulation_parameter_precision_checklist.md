# Simulation Parameter Precision - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `simulation_parameter_precision_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## Algorithm/Logic Questions

- [x] **Precision detection algorithm:** How to detect decimal places from float values?
  - **RESOLVED:** Option C - Explicit precision in PARAM_DEFINITIONS
  - Each entry becomes a 3-tuple: `(min, max, precision)`
  - Example: `'SAME_POS_BYE_WEIGHT': (0.0, 0.5, 1)` for 1 decimal place
  - Trailing zeros matter, so explicit is required

- [x] **Integer parameter handling:** How to detect and handle integer parameters?
  - **RESOLVED:** Use precision=0 in PARAM_DEFINITIONS
  - Example: `'NORMALIZATION_MAX_SCALE': (100, 175, 0)` → generates integers
  - No detection needed - explicitly specified

- [x] **Mixed precision handling:** When min and max have different precisions
  - **RESOLVED:** Not applicable with explicit precision
  - The precision field specifies exactly what precision to use
  - No ambiguity about `(0.0, 0.05)` - user specifies precision=1 or precision=2

---

## Architecture Questions

- [x] **Implementation location:** Where should precision logic live?
  - **RESOLVED:** Option C - Precision stored in PARAM_DEFINITIONS itself
  - This follows naturally from Q1's resolution (explicit precision as 3-tuples)
  - Helper functions still needed for generating discrete ranges from the stored precision

- [x] **Unify with existing discrete method?:** Should `generate_discrete_parameter_values()` be merged?
  - **RESOLVED:** Option A - Unify into one method
  - `generate_discrete_parameter_values()` will be merged into precision-aware approach
  - DRAFT_ORDER_FILE uses precision=0 like other integers
  - File-loading logic moves into the unified method

---

## Edge Cases

- [x] **Full enumeration behavior:** When `num_test_values >= possible_values`
  - **RESOLVED:** Option A - Return ALL possible values in order
  - Optimal value placed first
  - Remaining values in ascending order
  - Deterministic and reproducible

- [x] **Optimal value handling:** When returning subset
  - **RESOLVED:** Option A - Optimal first, then random samples
  - Always include optimal value as first element
  - Fill remaining slots with random samples from other possible values

- [x] **Floating-point precision errors:** How to handle accumulation errors?
  - **RESOLVED:** Option A - Use `round()` after each step
  - Apply `round(value, precision)` after each increment
  - Sufficient for precision levels 0-2

- [x] **Zero edge case:** Parameters with min=0
  - **RESOLVED:** Not applicable with explicit precision
  - Precision is specified directly in PARAM_DEFINITIONS (3rd element of tuple)
  - No need to detect precision from zero values

---

## Testing & Validation

- [x] **Test coverage:** What tests are needed?
  - **RESOLVED:** Option C - Comprehensive coverage
  - Unit tests for `_generate_discrete_range()` helper
  - Unit tests for `generate_parameter_values()` with precision levels 0, 1, 2
  - Edge case tests: full enumeration, optimal value inclusion
  - Tests verifying each PARAM_DEFINITIONS entry generates valid values
  - Integration tests confirming generated configs contain discrete values

---

## Parameter Analysis

Current PARAM_DEFINITIONS and their implied precision:

| Parameter | Range | Implied Precision | Possible Values |
|-----------|-------|-------------------|-----------------|
| `NORMALIZATION_MAX_SCALE` | (100, 175) | 0 (int) | 76 |
| `SAME_POS_BYE_WEIGHT` | (0.0, 0.5) | 1 | 6 |
| `DIFF_POS_BYE_WEIGHT` | (0.0, 0.3) | 1 | 4 |
| `PRIMARY_BONUS` | (50, 100) | 0 (int) | 51 |
| `SECONDARY_BONUS` | (50, 100) | 0 (int) | 51 |
| `DRAFT_ORDER_FILE` | (1, 100) | 0 (int) | 100 |
| `ADP_SCORING_WEIGHT` | (1.00, 4.00) | 2 | 301 |
| `ADP_SCORING_STEPS` | (5, 30) | 0 (int) | 26 |
| `PLAYER_RATING_SCORING_WEIGHT` | (1.00, 4.00) | 2 | 301 |
| `TEAM_QUALITY_SCORING_WEIGHT` | (0.00, 3.0) | 2* | 301 |
| `TEAM_QUALITY_MIN_WEEKS` | (2, 12) | 0 (int) | 11 |
| `PERFORMANCE_SCORING_WEIGHT` | (0.00, 3.00) | 2 | 301 |
| `PERFORMANCE_SCORING_STEPS` | (0.10, 0.40) | 2 | 31 |
| `PERFORMANCE_MIN_WEEKS` | (2, 14) | 0 (int) | 13 |
| ... | ... | ... | ... |

*Note: `(0.00, 3.0)` has mixed precision - need to clarify handling

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Precision detection algorithm | Option C - Explicit precision in PARAM_DEFINITIONS as 3-tuples | 2025-12-07 |
| Integer parameter handling | Use precision=0 in PARAM_DEFINITIONS | 2025-12-07 |
| Mixed precision handling | Not applicable - explicit precision eliminates ambiguity | 2025-12-07 |
| Implementation location | Precision stored in PARAM_DEFINITIONS (Option C consequence) | 2025-12-07 |
| Zero edge case | Not applicable with explicit precision | 2025-12-07 |
| Unify with existing discrete method | Option A - Unify into one method | 2025-12-07 |
| Full enumeration behavior | Option A - Return ALL values in order, optimal first | 2025-12-07 |
| Optimal value handling | Option A - Optimal first, then random samples | 2025-12-07 |
| Floating-point precision errors | Option A - Use round() after each step | 2025-12-07 |
| Test coverage | Option C - Comprehensive (unit + edge cases + PARAM_DEFINITIONS + integration) | 2025-12-07 |
