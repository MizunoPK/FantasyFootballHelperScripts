# Bye Week Penalty Formula Update

## Summary
Updated the bye week penalty calculation from a simple linear formula to a position-scaled formula that accounts for roster depth at each position.

---

## New Formula

```
Bye Week Penalty = (Same-Position Conflicts / Max Position Slots) × BASE_BYE_PENALTY
```

Where:
- **Same-Position Conflicts** = Number of roster players at the same position with the same bye week
- **Max Position Slots** = Maximum allowed players at that position (from `MAX_POSITIONS`)
- **BASE_BYE_PENALTY** = 18.85 (configurable constant)

---

## Rationale

### Why This Makes Sense

1. **Proportional Impact**: Positions with more depth get proportionally smaller penalties per conflict
   - Having 1/2 QBs on bye = 50% of position depth unavailable
   - Having 2/4 RBs on bye = 50% of position depth unavailable
   - Both situations are equally severe and get the same penalty (9.43 points)

2. **Fair Scaling**: Shallow positions (K, DST) get immediate full penalty
   - 1 kicker with bye week conflict = (1/1) × 18.85 = **18.85 penalty** (100% of position)
   - Makes sense because you literally cannot field the position that week

3. **Realistic Construction**: Reflects actual roster constraints
   - You can afford to have multiple RBs with the same bye week when you have 4 slots
   - You cannot afford to have multiple kickers with the same bye week when you only have 1 slot

---

## Examples with BASE_BYE_PENALTY = 18.85

### Kicker (Max Slots: 1)
- **0 conflicts** → (0/1) × 18.85 = **0.00** penalty
- **1 conflict** → (1/1) × 18.85 = **18.85** penalty (full penalty!)

### QB (Max Slots: 2)
- **0 conflicts** → (0/2) × 18.85 = **0.00** penalty
- **1 conflict** → (1/2) × 18.85 = **9.43** penalty (50%)

### RB (Max Slots: 4)
- **0 conflicts** → (0/4) × 18.85 = **0.00** penalty
- **1 conflict** → (1/4) × 18.85 = **4.71** penalty (25%)
- **2 conflicts** → (2/4) × 18.85 = **9.43** penalty (50%)
- **3 conflicts** → (3/4) × 18.85 = **14.14** penalty (75%)

### WR (Max Slots: 4)
- Same as RB (both have max 4 slots)

### TE (Max Slots: 2)
- Same as QB (both have max 2 slots)

---

## Files Updated

### 1. Core Calculation
**File**: `draft_helper/core/scoring_engine.py`
- **Method**: `compute_bye_penalty_for_player()`
- **Lines**: 306-319
- **Change**: Replaced simple `count × BASE_BYE_PENALTY` with `(count / max_slots) × BASE_BYE_PENALTY`

### 2. Simulation Code
**File**: `draft_helper/simulation/team_strategies.py`
- **Method**: `rank_available_players()`
- **Lines**: 302-307
- **Change**: Updated to use same position-scaled formula
- **Method**: `_calculate_bye_conflicts()`
- **Lines**: 335-347
- **Change**: Updated to only count same-position conflicts

### 3. Documentation
**File**: `kicker_scoring_breakdown.md`
- Updated with new formula explanation and examples

---

## Testing

### Unit Tests
- ✅ `test_draft_helper.py::test_bye_week_penalty_calculation` - Passes
- ✅ Created comprehensive test suite in `test_bye_week_penalty_formula.py`

### Test Coverage
All scenarios validated:
1. ✅ No conflicts (empty roster)
2. ✅ Kicker position (max 1 slot)
3. ✅ QB position (max 2 slots) - 1 conflict
4. ✅ RB position (max 4 slots) - 1, 2, 3 conflicts
5. ✅ Different bye weeks (no conflict)
6. ✅ Different positions (no conflict)
7. ✅ Exclude self in trade mode

**Result**: All tests pass ✓

---

## Impact on Scoring

### Before (Old Formula)
```
1 QB conflict  = 1 × 18.85 = 18.85 penalty
2 RB conflicts = 2 × 18.85 = 37.70 penalty
```
**Problem**: Having 2 RBs with same bye week was penalized MORE than having 1 QB with same bye week, even though RBs have more depth (4 slots vs 2 slots).

### After (New Formula)
```
1 QB conflict  = (1/2) × 18.85 = 9.43 penalty  (50% of position)
2 RB conflicts = (2/4) × 18.85 = 9.43 penalty  (50% of position)
```
**Solution**: Both scenarios get the same penalty because they represent the same proportion of position depth unavailable.

---

## Backwards Compatibility

### Breaking Changes
- Penalty values will change for existing rosters
- Simulations using old penalty values will produce different results

### Migration
- No code changes needed for users
- Penalty calculation is centralized and automatically applied everywhere
- Tests updated and passing

---

## Configuration

The formula uses these configurable values from `draft_helper_config.py`:

```python
BASE_BYE_PENALTY = 18.85  # Base penalty multiplier

MAX_POSITIONS = {
    QB: 2,
    RB: 4,
    WR: 4,
    TE: 2,
    FLEX: 1,
    K: 1,
    DST: 1,
}
```

To adjust the penalty severity, modify `BASE_BYE_PENALTY`. The position scaling happens automatically based on `MAX_POSITIONS`.

---

## Key Design Decisions

1. **Position-specific scaling**: Each position's penalty scales based on its roster depth
2. **Same-position only**: Only players at the same position count as conflicts
3. **Linear scaling**: Penalty grows linearly with the fraction of position depth affected
4. **Centralized calculation**: Single method (`compute_bye_penalty_for_player`) used everywhere
5. **Exclude self option**: Trade mode can exclude the player being evaluated from conflict count

---

## Future Considerations

- Could add non-linear scaling (e.g., exponential) if 75% position depth on bye should be MORE than 3x as bad as 25%
- Could add cross-position penalties for FLEX-eligible positions (currently not implemented)
- Could add week-specific multipliers (playoffs vs regular season)

---

**Date**: 2025-10-05
**Updated By**: Claude Code
**Version**: 2.0 (Position-Scaled Formula)
