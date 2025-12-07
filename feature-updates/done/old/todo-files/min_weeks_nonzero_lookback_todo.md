# TODO: MIN_WEEKS Non-Zero Lookback Enhancement

## Objective
Update all scoring methods that use MIN_WEEKS parameter to look back further in time to find MIN_WEEKS total weeks with non-zero/valid values, skipping bye weeks and injury weeks.

## Status: COMPLETE - All Implementation Done

---

## User Question Answers (Integrated)

**Q1: Maximum lookback limit?**
- **Answer**: Option B - 2x MIN_WEEKS limit
- Look back at most (2 × MIN_WEEKS) weeks from current week
- Example: MIN_WEEKS=3 → look back max 6 weeks
- Balances data freshness with availability

**Q2: Insufficient data handling?**
- **Answer**: Option A/C - Strict MIN_WEEKS requirement
- Keep MIN_WEEKS as a strict requirement
- Return None if MIN_WEEKS valid weeks cannot be found
- Maintains consistency with parameter's documented meaning

**Q3: Zero handling?**
- **Answer**: Option A - Keep current skip behavior
- Skip any week with actual=0 OR projected=0
- Simple, consistent with existing logic
- A week with 0 actual points is a week without performance data

---

## Key Findings from First Verification Round (Iterations 1-5)

### MIN_WEEKS Usage in league_config.json
Found 4 scoring sections using MIN_WEEKS:
1. **TEAM_QUALITY_SCORING** - MIN_WEEKS: 5 (line 81)
2. **PERFORMANCE_SCORING** - MIN_WEEKS: 3 (line 96)
3. **MATCHUP_SCORING** - MIN_WEEKS: 5 (line 111)
4. **SCHEDULE_SCORING** - MIN_WEEKS: 5 (line 127)

### Code Locations Using MIN_WEEKS

1. **player_scoring.py:167-269** - `calculate_performance_deviation()`
   - Uses MIN_WEEKS as rolling window size AND minimum requirement
   - Current logic: Analyzes weeks `[current_week - min_weeks, current_week - 1]`
   - Skips weeks where `actual_points == 0` (line 221)
   - **BUT**: Still requires min_weeks valid entries or returns None (line 254)
   - **PROBLEM**: If bye week is in the window, fewer than min_weeks valid weeks may exist

2. **TeamDataManager.py:104-188** - `_calculate_rankings()`
   - Uses TEAM_QUALITY_MIN_WEEKS for offensive/defensive rankings
   - Uses MATCHUP_MIN_WEEKS for position-specific defense rankings
   - Already skips bye weeks at team level (lines 148-150, 174-176)
   - **Not affected by player bye weeks** - this is team-level data

3. **ConfigManager.py:303-328** - MIN_WEEKS getters
   - `get_team_quality_min_weeks()` -> returns 5
   - `get_matchup_min_weeks()` -> returns 5
   - `get_schedule_min_weeks()` -> returns 5
   - Performance MIN_WEEKS accessed directly via `config.performance_scoring[MIN_WEEKS]`

### Analysis: Which Code Actually Needs Changes?

1. **PERFORMANCE_SCORING** - **NEEDS CHANGE**
   - `player_scoring.py:calculate_performance_deviation()` uses player's weekly points
   - Current: Looks at fixed window `[current_week - min_weeks, current_week - 1]`
   - Problem: If player had bye week in this window, insufficient valid weeks
   - Solution: Look back further to collect min_weeks non-zero weeks

2. **TEAM_QUALITY_SCORING** - **NO CHANGE NEEDED**
   - Uses team offensive/defensive ranks from TeamDataManager
   - Already handles bye weeks at team level (skips all-zero weeks)
   - Player's bye week doesn't affect team rankings

3. **MATCHUP_SCORING** - **NO CHANGE NEEDED**
   - Uses opponent's defense ranking from TeamDataManager
   - Already handles bye weeks at team level
   - Player's bye week doesn't affect opponent's defense ranking

4. **SCHEDULE_SCORING** - **NO CHANGE NEEDED**
   - Uses future opponent schedule data
   - Not affected by player's past bye weeks

### Conclusion
**Only Performance Multiplier needs modification** to handle player bye weeks properly.

---

## Phase 1: Research and Discovery (COMPLETE)

### 1.1 Identify MIN_WEEKS Usage in league_config.json
- [x] Read league_config.json to find all MIN_WEEKS parameters
- [x] Document each parameter and its purpose
- [x] Identify which scoring multipliers use MIN_WEEKS

### 1.2 Find All Code References to MIN_WEEKS
- [x] Search codebase for MIN_WEEKS usage
- [x] Identify all files that read MIN_WEEKS from config
- [x] Document the methods/functions that use MIN_WEEKS for calculations

### 1.3 Analyze Current Week Data Collection Logic
- [x] Found: `calculate_performance_deviation()` in player_scoring.py
- [x] Current logic uses fixed rolling window
- [x] Already skips weeks where actual == 0, BUT still requires min_weeks count

---

## Phase 2: Implementation

### 2.1 Modify calculate_performance_deviation()
**File**: `league_helper/util/player_scoring.py` (lines 167-269)

Current logic:
```python
start_week = max(1, self.config.current_nfl_week - min_weeks)
for week in range(start_week, self.config.current_nfl_week):
    # collect deviations, skip if actual == 0
if len(deviations) < min_weeks:
    return None  # Problem: bye week reduces count
```

**New logic (per user answers)**:
```python
# Calculate maximum lookback limit (2x MIN_WEEKS per Q1 answer)
max_lookback = min_weeks * 2
earliest_week = max(1, self.config.current_nfl_week - max_lookback)

# Look back from current_week - 1, collect min_weeks non-zero weeks
deviations = []
week = self.config.current_nfl_week - 1

while len(deviations) < min_weeks and week >= earliest_week:
    # Get week data
    # If valid (actual > 0 and projected > 0), add to deviations (per Q3 answer)
    # Decrement week

# Return None if insufficient data (strict MIN_WEEKS per Q2 answer)
if len(deviations) < min_weeks:
    return None
```

- [x] Change from fixed window to dynamic lookback
- [x] Add max_lookback = min_weeks * 2 limit
- [x] Collect exactly min_weeks valid (non-zero) weeks
- [x] Stop when min_weeks weeks found OR earliest_week reached
- [x] Return None only if truly insufficient data exists within lookback limit

### 2.2 Edge Case Handling (Answers Integrated)
- [x] Rookie with few games → Returns None (strict MIN_WEEKS)
- [x] Multiple consecutive bye/injury weeks → Lookback finds older valid weeks
- [x] Maximum lookback limit: 2x MIN_WEEKS weeks

---

## Phase 3: Testing

### 3.1 Update Existing Unit Tests
**File**: `tests/league_helper/util/test_player_scoring.py`

Existing tests found (lines 374-448):
- `test_calculate_performance_deviation_with_sufficient_data`
- `test_calculate_performance_deviation_returns_none_for_dst`
- `test_calculate_performance_deviation_insufficient_data`
- `test_calculate_performance_deviation_skips_zero_actual`
- `test_calculate_performance_deviation_skips_zero_projected`

- [x] Verify existing tests still pass with new logic
- [x] Update any tests that depend on fixed window behavior

### 3.2 Add New Unit Tests
- [x] Test: Player with bye week in recent history gets proper min_weeks calculation
- [x] Test: Dynamic lookback finds valid weeks past bye week
- [x] Test: Multiple consecutive zero weeks handled correctly
- [x] Test: Max lookback limit (2x MIN_WEEKS) is respected
- [x] Test: Returns None when data outside lookback window
- [x] Test: Uses most recent valid weeks first

### 3.3 Run Full Test Suite
- [x] Execute `python tests/run_all_tests.py`
- [x] Ensure 100% pass rate (2023 tests passed)
- [x] Fix any failing tests

---

## Phase 4: Documentation and Finalization

### 4.1 Update Documentation
- [x] Update `docs/scoring_v2/05_performance_multiplier.md`
  - Document dynamic lookback behavior
  - Document 2x MIN_WEEKS limit
  - Update example scenarios
- [x] Add comments explaining new lookback logic in code

### 4.2 Final Verification
- [x] Re-verify all requirements from original spec are met
- [x] Run pre-commit validation (2023 tests passed)
- [x] Manual testing of affected functionality

### 4.3 Completion
- [x] Move objective file to updates/done/
- [x] Delete questions file
- [x] Update code changes documentation

---

## Files Affected

| File | Change Type | Description |
|------|-------------|-------------|
| `league_helper/util/player_scoring.py` | MODIFY | Update `calculate_performance_deviation()` |
| `tests/league_helper/util/test_player_scoring.py` | MODIFY | Update/add tests |
| `docs/scoring_v2/05_performance_multiplier.md` | MODIFY | Update documentation |

**Files NOT Affected** (confirmed through verification):
- `league_helper/util/TeamDataManager.py` - Team-level, already handles bye weeks
- `league_helper/util/ConfigManager.py` - No changes needed
- `data/league_config.json` - No changes needed

---

## Verification Summary

### First Round (Iterations 1-5) - COMPLETE
- **Iterations Completed**: 5/5
- **Requirements Covered**: Identified primary affected code
- **Key Finding**: Only PERFORMANCE_SCORING needs changes (not all 4)
- **Pattern Identified**: Current performance uses fixed window, needs dynamic lookback
- **Critical Dependencies**: ProjectedPointsManager for projected values
- **Risk Areas**: Edge cases with rookies, multiple consecutive zeros
- **Questions Created**: 3 questions about lookback limits, data handling, zero handling

### Second Round (Iterations 6-12) - COMPLETE
- **Iterations Completed**: 7/7
- **User Answers Integrated**: Yes
  - Q1: 2x MIN_WEEKS lookback limit
  - Q2: Strict MIN_WEEKS requirement
  - Q3: Keep current zero-skip behavior

### Iteration 10 Skeptical Re-Verification Results
- ✅ `calculate_performance_deviation()` verified at line 167
- ✅ MIN_WEEKS parameters verified at lines 81, 96, 111, 127
- ✅ Fixed window logic verified at lines 202, 208
- ✅ MIN_WEEKS strict check verified at line 254
- ✅ Test class verified at line 374
- ✅ Documentation file verified
- ✅ Team quality/matchup/schedule confirmed using team-level data
- **Confidence Level: HIGH** - All claims verified from fresh codebase research

---

## Progress Tracking
**Note to future agents**: Keep this file updated as you complete tasks. Check off completed items and add notes about any issues encountered or decisions made.

Last Updated: IMPLEMENTATION COMPLETE - All phases finished successfully
