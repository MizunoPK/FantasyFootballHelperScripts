# Bye Scaling Penalties - Questions for User

This file contains questions that arose during the first verification round (3 iterations of codebase research). Your answers will be integrated into the implementation plan during the second verification round.

---

## Q1: Default Parameter Values

**Question**: What should the initial values be for the new weight parameters?

**Context**:
- Current config has: BASE_BYE_PENALTY=41.34, DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY=1.95
- New parameters use exponential scaling instead of linear multiplication
- Formula: `(same_pos_median_total ** SAME_POS_BYE_WEIGHT) + (diff_pos_median_total ** DIFF_POS_BYE_WEIGHT)`

**Options**:
A) Start with weight=1.0 for both (no exponential scaling, just use raw median sum)
B) Start with weight=2.0 for same-position, weight=1.5 for different-position (moderate exponential scaling)
C) Start with weight=0.5 for both (dampened penalty, square root effect)
D) Other (please specify)

**Recommendation**: Option A (weight=1.0) for initial values, then use simulation to optimize

**Your answer**: Option A

---

## Q2: Simulation Parameter Ranges

**Question**: What ranges should be used for simulation optimization of the new weight parameters?

**Context**:
- ConfigGenerator.PARAM_DEFINITIONS specifies (range_val, min_val, max_val) for each parameter
- Example: 'BASE_BYE_PENALTY': (10.0, 0.0, 200.0) means ±10 from optimal, bounded [0, 200]
- Weight parameters likely need different ranges since they're exponential multipliers

**Options**:
A) 'SAME_POS_BYE_WEIGHT': (0.2, 0.0, 3.0), 'DIFF_POS_BYE_WEIGHT': (0.2, 0.0, 3.0)
   - Small range (±0.2), bounded [0, 3]
   - Conservative: prevents extreme exponential effects

B) 'SAME_POS_BYE_WEIGHT': (0.5, 0.0, 5.0), 'DIFF_POS_BYE_WEIGHT': (0.5, 0.0, 5.0)
   - Medium range (±0.5), bounded [0, 5]
   - Balanced: allows moderate exploration

C) 'SAME_POS_BYE_WEIGHT': (1.0, 0.0, 10.0), 'DIFF_POS_BYE_WEIGHT': (1.0, 0.0, 10.0)
   - Large range (±1.0), bounded [0, 10]
   - Aggressive: explores wide range of exponential scaling

D) Different ranges for same vs diff (e.g., same-pos has wider range)

E) Other (please specify)

**Recommendation**: Option A initially, can increase range later if needed

**Your answer**: Option A

---

## Q3: Bye Week Scaling

**Question**: Should we keep the existing bye week scaling (based on remaining bye weeks in season)?

**Context**:
- **Current implementation** (ConfigManager.get_bye_week_penalty lines 418-435):
  - Calculates scale_factor = bye_weeks_remaining / TOTAL_BYE_WEEKS (9 total bye weeks)
  - Week 1-4 (before byes): scale=1.0 (full penalty)
  - Week 8 (mid-season): scale=0.67 (reduced penalty)
  - Week 14+ (after byes): scale=0.0 (no penalty)
  - Penalty formula: `(base * scale * count) + (diff * scale * count)`

- **New algorithm**: Uses exponential scaling on median values
  - Could apply scale_factor to final result: `((same ** weight) + (diff ** weight)) * scale_factor`
  - Or could skip scaling entirely (exponential scaling may be sufficient)

**Options**:
A) Keep bye week scaling - apply to final penalty: `result * scale_factor`
B) Remove bye week scaling - exponential scaling handles time-based weighting
C) Apply scaling before exponential: `(same * scale) ** weight + (diff * scale) ** weight`
D) Other approach (please specify)

**Recommendation**: Option A (keep scaling, apply to final result) - maintains existing time-based logic

**Your answer**: Option B. Remove the scaling and just do what the txt file mentions

---

## Q4: Median Calculation - Data Source

**Question**: Which weekly data should we use for median calculation?

**Context**:
- FantasyPlayer has week_1_points through week_17_points attributes
- These can be: actual past scores OR projected future scores (depending on data source)
- Spec says "calculate median score from their week 1-18 scores"

**Options**:
A) Use ALL weeks (1-17), regardless of current NFL week
   - Pro: Uses all available data, consistent across season
   - Con: Includes future projections which may be less reliable

B) Use only PAST weeks (1 to CURRENT_NFL_WEEK-1)
   - Pro: Uses only actual historical data (more reliable)
   - Con: Early season has less data, median may be less accurate
   - Similar to calculate_performance_deviation pattern (line 239 in player_scoring.py)

C) Use ALL weeks but weight past weeks more heavily
   - Pro: Balances historical accuracy with future projections
   - Con: More complex, may not match spec exactly

D) Other (please specify)

**Recommendation**: Option A (all weeks 1-17) to match spec "week 1-18 scores" (note: only 17 weeks exist)

**Your answer**:
Option A

---

## Q5: Median Calculation - Handling Missing/Zero Data

**Question**: How should we handle weeks with missing (None) or zero points?

**Context**:
- Weekly points can be None (no data available)
- Weekly points can be 0.0 (player didn't play, bye week, or benched)
- Existing pattern in calculate_consistency (lines 166-173):
  ```python
  if points is not None and float(points) > 0:
      weekly_points.append(float(points))
  ```
  - Skips both None AND zero values

**Options**:
A) Skip both None and zero (follow existing pattern)
   - Pro: Consistent with existing code
   - Con: Bye weeks are legitimately 0, excluding them may skew median

B) Skip None, include zeros
   - Pro: More accurate median (includes actual 0-point games)
   - Con: Bye weeks artificially lower median

C) Skip None, include zeros except for player's own bye week
   - Pro: Most accurate (excludes only known bye, includes real 0s)
   - Con: More complex logic

D) Other (please specify)

**Recommendation**: Option A (skip both None and zeros) - maintains consistency with existing patterns

**Your answer**: Option A

---

## Q6: Median Calculation - Edge Cases

**Question**: What should median be when a player has insufficient valid weekly data?

**Context**:
- After filtering None/zeros, a player might have 0, 1, or 2 valid weeks
- statistics.median() requires at least 1 value
- Need default value for empty lists

**Options**:
A) Return 0.0 for players with no valid data
   - Pro: No penalty contribution (neutral)
   - Con: May hide data quality issues

B) Return a small default value (e.g., 5.0 points)
   - Pro: Provides minimal penalty even with no data
   - Con: Arbitrary choice of default value

C) Log warning and return 0.0
   - Pro: Makes data issues visible in logs
   - Con: May create log spam

D) Require minimum weeks (like MIN_WEEKS=3), return 0.0 if insufficient
   - Pro: Ensures statistical reliability
   - Con: More complex

E) Other (please specify)

**Recommendation**: Option C (log warning, return 0.0) - balances safety with visibility

**Your answer**: Option C

---

## Q7: Method Signature Design

**Question**: What should the new signature for get_bye_week_penalty() be?

**Context**:
- **Current signature** (line 378): `get_bye_week_penalty(num_same_position: int, num_different_position: int) -> float`
- **New algorithm needs**: access to actual player objects to calculate medians from weekly data
- **Caller** (_apply_bye_week_penalty in player_scoring.py) already has:
  - `p` (player being scored)
  - `roster` (full roster list)
  - Can collect same-pos and diff-pos players before calling

**Options**:
A) Pass full roster + player being scored: `get_bye_week_penalty(player: FantasyPlayer, roster: List[FantasyPlayer]) -> float`
   - Pro: ConfigManager does all filtering and calculation
   - Con: ConfigManager needs to import FantasyPlayer, may create circular dependency risk

B) Pass pre-filtered player lists: `get_bye_week_penalty(same_pos_players: List[FantasyPlayer], diff_pos_players: List[FantasyPlayer]) -> float`
   - Pro: Separation of concerns (caller does filtering, ConfigManager does calculation)
   - Con: Requires ConfigManager to import FantasyPlayer (still potential circular dependency)

C) Keep current signature, add helper method: Keep `get_bye_week_penalty(num_same, num_diff)` for backward compatibility, add `calculate_bye_penalty_from_roster(player, roster)` that does median calculation
   - Pro: No breaking changes
   - Con: More complex, two methods doing similar things

D) Other approach (please specify)

**Recommendation**: Option B (pass pre-filtered lists) - best separation of concerns, caller already has the data

**Additional consideration**: Need to verify if importing FantasyPlayer in ConfigManager creates circular dependencies. Initial check shows no circular dependency risk.

**Your answer**: Option B


ALSO: PLEASE MAKE SURE TO STILL NOT APPLY ANY BYE WEEK PENELTY IF THE PLAYER'S BYE WEEK HAS ALREADY PASSED

---

## Summary of Recommendations

Based on codebase research, here are the recommended answers:

1. **Q1 (Default values)**: A - Start with weight=1.0 for both
2. **Q2 (Simulation ranges)**: A - Conservative ranges (±0.2, bounded [0, 3])
3. **Q3 (Bye week scaling)**: A - Keep scaling, apply to final result
4. **Q4 (Data source)**: A - Use all weeks 1-17
5. **Q5 (Missing/zero data)**: A - Skip both None and zeros (existing pattern)
6. **Q6 (Edge cases)**: C - Log warning and return 0.0
7. **Q7 (Method signature)**: B - Pass pre-filtered player lists

These recommendations prioritize:
- Consistency with existing code patterns
- Conservative initial values (optimize via simulation later)
- Maintaining existing bye week scaling logic
- Clear separation of concerns

Please review and provide your answers above. After receiving your answers, I will proceed with the second verification round (3 more iterations) to integrate your decisions into the implementation plan.
