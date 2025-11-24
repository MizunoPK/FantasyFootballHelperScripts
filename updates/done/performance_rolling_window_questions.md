# Performance Rolling Window Update - Questions

## Context
After researching the codebase, I've identified several implementation details that need clarification before proceeding.

**Note**: The `calculate_consistency()` method (lines 167-225) is **unused** in the 10-step scoring algorithm - only `calculate_performance_deviation()` is called via `_apply_performance_multiplier()`. This update will focus solely on performance deviation and will also clean up the unused consistency code.

---

## Question 1: MIN_WEEKS Range for Simulation

**Context**: The specification suggests range 2-8 for PERFORMANCE_MIN_WEEKS. However, existing MIN_WEEKS parameters use different ranges:

**Current ConfigGenerator ranges**:
- `TEAM_QUALITY_MIN_WEEKS`: (3, 6)
- `MATCHUP_MIN_WEEKS`: (3, 6)

**Spec suggestion**: 2-8 weeks

**Question**: What range should PERFORMANCE_MIN_WEEKS use?

A) **(2, 8)** - As specified in the update file (wider range, allows more optimization exploration)

B) **(3, 6)** - Match existing MIN_WEEKS ranges (consistency with other parameters)

C) **(2, 6)** - Allow minimum of 2 (more responsive) but cap at 6 (matches others)

**Recommendation**: Option A - Follow the specification. Performance scoring may benefit from different optimal window sizes than team rankings.

---

## Question 2: Rolling Window Behavior Clarification

**Context**: Need to clarify exact rolling window semantics.

**Spec example**:
```python
# New: for week in range(max(1, self.config.current_nfl_week - min_weeks), self.config.current_nfl_week)
```

**Question**: If MIN_WEEKS=4 and CURRENT_NFL_WEEK=6:

A) **Use weeks 2-5** (exactly 4 weeks in window: `range(6-4, 6)` = `range(2, 6)`)

B) **Use weeks 3-5** (3 complete weeks, start = max(1, 6-4) = 2, but need 4 weeks minimum?)

**Clarification needed**: The spec's formula `range(max(1, current_week - min_weeks), current_week)` produces `range(2, 6)` = weeks [2, 3, 4, 5]. This gives 4 weeks (weeks that have occurred before week 6).

**Question**: Is this interpretation correct - rolling window uses the LAST MIN_WEEKS completed weeks?

**Expected Answer**: Yes, use the last MIN_WEEKS completed weeks. If current_week=6 and MIN_WEEKS=4, analyze weeks 2, 3, 4, 5.

---

## Question 3: Insufficient Data Behavior

**Context**: When `current_nfl_week <= MIN_WEEKS`, there aren't enough weeks in the rolling window.

**Example**: If MIN_WEEKS=4 and current_week=3:
- Rolling window would be `range(max(1, 3-4), 3)` = `range(1, 3)` = weeks [1, 2]
- Only 2 weeks available, but MIN_WEEKS requires 4

**Question**: How should this be handled?

A) **Return None** - Insufficient data, same as current behavior when not enough valid weeks

B) **Use available weeks** - If fewer than MIN_WEEKS weeks exist, use all available (weeks 1-2 in example)

**Recommendation**: Option A - Maintain consistency with MIN_WEEKS as both window size AND minimum requirement. Return None for insufficient data.

---

## Summary

Please provide answers to these questions so I can finalize the implementation plan:

1. MIN_WEEKS range: (A) 2-8, (B) 3-6, or (C) 2-6
2. Rolling window interpretation: Confirm last MIN_WEEKS completed weeks
3. Insufficient data: (A) Return None, or (B) Use available weeks

---

## Answers

1. **(A) 2-8** - Follow the specification, allow wider optimization range
2. **Yes, confirmed** - Use the last MIN_WEEKS completed weeks
3. **(A) Return None** - Maintain MIN_WEEKS as both window size and minimum requirement
