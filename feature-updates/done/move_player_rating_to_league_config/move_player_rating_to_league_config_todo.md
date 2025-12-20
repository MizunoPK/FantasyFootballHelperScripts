# Move Player Rating to League Config - Implementation TODO

> **STATUS**: Created - Ready for Verification Rounds

---

## Implementation Tasks

### 1. Update ResultsManager.py - Add PLAYER_RATING_SCORING to BASE_CONFIG_PARAMS

**File**: `simulation/shared/ResultsManager.py`
**Line**: 252 (after 'ADP_SCORING')
**Action**: Add `'PLAYER_RATING_SCORING'` to BASE_CONFIG_PARAMS list

**Before**:
```python
BASE_CONFIG_PARAMS = [
    'CURRENT_NFL_WEEK',
    'NFL_SEASON',
    'NFL_SCORING_FORMAT',
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    'INJURY_PENALTIES',
    'DRAFT_ORDER_BONUSES',
    'DRAFT_ORDER_FILE',
    'DRAFT_ORDER',
    'MAX_POSITIONS',
    'FLEX_ELIGIBLE_POSITIONS',
    'ADP_SCORING'
]
```

**After**:
```python
BASE_CONFIG_PARAMS = [
    'CURRENT_NFL_WEEK',
    'NFL_SEASON',
    'NFL_SCORING_FORMAT',
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    'INJURY_PENALTIES',
    'DRAFT_ORDER_BONUSES',
    'DRAFT_ORDER_FILE',
    'DRAFT_ORDER',
    'MAX_POSITIONS',
    'FLEX_ELIGIBLE_POSITIONS',
    'ADP_SCORING',
    'PLAYER_RATING_SCORING'  # ← ADD THIS
]
```

**Verification**:
- [ ] Line added in correct location
- [ ] Syntax correct (comma after previous item, no comma after this one)
- [ ] Formatting matches existing style

---

### 2. Update ResultsManager.py - Remove PLAYER_RATING_SCORING from WEEK_SPECIFIC_PARAMS

**File**: `simulation/shared/ResultsManager.py`
**Line**: 257
**Action**: Remove `'PLAYER_RATING_SCORING',` from WEEK_SPECIFIC_PARAMS list

**Before**:
```python
WEEK_SPECIFIC_PARAMS = [
    'NORMALIZATION_MAX_SCALE',
    'PLAYER_RATING_SCORING',
    'TEAM_QUALITY_SCORING',
    'PERFORMANCE_SCORING',
    'MATCHUP_SCORING',
    'SCHEDULE_SCORING',
    'TEMPERATURE_SCORING',
    'WIND_SCORING',
    'LOCATION_MODIFIERS'
]
```

**After**:
```python
WEEK_SPECIFIC_PARAMS = [
    'NORMALIZATION_MAX_SCALE',
    'TEAM_QUALITY_SCORING',
    'PERFORMANCE_SCORING',
    'MATCHUP_SCORING',
    'SCHEDULE_SCORING',
    'TEMPERATURE_SCORING',
    'WIND_SCORING',
    'LOCATION_MODIFIERS'
]
```

**Verification**:
- [ ] Line removed completely
- [ ] No syntax errors (list still valid)
- [ ] Formatting matches existing style

---

### 3. Update run_win_rate_simulation.py - Add PLAYER_RATING_SCORING_WEIGHT to PARAMETER_ORDER

**File**: `run_win_rate_simulation.py`
**Line**: 63 (after 'ADP_SCORING_WEIGHT')
**Action**: Add `'PLAYER_RATING_SCORING_WEIGHT',` to PARAMETER_ORDER list

**Before**:
```python
PARAMETER_ORDER = [
    # Bye Week Penalties - affects roster construction decisions
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    # Draft Order Bonuses - affects position priority during draft
    'PRIMARY_BONUS',
    'SECONDARY_BONUS',
    # ADP Scoring - affects how much market wisdom influences picks
    'ADP_SCORING_WEIGHT',
]
```

**After**:
```python
PARAMETER_ORDER = [
    # Bye Week Penalties - affects roster construction decisions
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    # Draft Order Bonuses - affects position priority during draft
    'PRIMARY_BONUS',
    'SECONDARY_BONUS',
    # ADP Scoring - affects how much market wisdom influences picks
    'ADP_SCORING_WEIGHT',
    # Player Rating Scoring - affects expert consensus ranking influence
    'PLAYER_RATING_SCORING_WEIGHT',
]
```

**Verification**:
- [ ] Line added in correct location
- [ ] Comment added explaining purpose
- [ ] Syntax correct (comma after this item)
- [ ] Formatting matches existing style

---

## Testing Tasks

### Unit Tests to Update

**1. Test ResultsManager Parameter Lists**

File: `tests/simulation/test_ResultsManager.py` (or equivalent)

Update tests that verify BASE_CONFIG_PARAMS and WEEK_SPECIFIC_PARAMS:
- [ ] Verify PLAYER_RATING_SCORING is IN BASE_CONFIG_PARAMS
- [ ] Verify PLAYER_RATING_SCORING is NOT IN WEEK_SPECIFIC_PARAMS
- [ ] Run tests: `python -m pytest tests/simulation/test_ResultsManager.py -v`

**2. Test Win-Rate Simulation Parameter Order**

File: `tests/root_scripts/test_root_scripts.py` (or equivalent)

Update tests that verify PARAMETER_ORDER:
- [ ] Verify PLAYER_RATING_SCORING_WEIGHT is in win-rate PARAMETER_ORDER
- [ ] Run tests: `python -m pytest tests/root_scripts/test_root_scripts.py -v`

### Integration Tests

**1. Config Save/Load Test**

Test that configs are saved with PLAYER_RATING_SCORING in correct location:
- [ ] Run minimal win-rate sim: `python run_win_rate_simulation.py iterative --sims 1 --test-values 1`
- [ ] Verify output league_config.json contains PLAYER_RATING_SCORING
- [ ] Verify output week1-5.json does NOT contain PLAYER_RATING_SCORING
- [ ] Verify ConfigManager can load the new config structure

**2. Backward Compatibility Test**

Test that old configs still load:
- [ ] Use existing config with PLAYER_RATING_SCORING in week files
- [ ] Verify ConfigManager loads it without errors
- [ ] Verify draft mode can use it

**3. Full Test Suite**

Run all tests to ensure no breakage:
- [ ] `python tests/run_all_tests.py`
- [ ] All tests must pass (100% pass rate)

---

## Verification Checklist

### Code Changes Verification
- [ ] All 3 files modified correctly
- [ ] No syntax errors introduced
- [ ] Formatting matches existing code style
- [ ] Comments added where appropriate

### Functional Verification
- [ ] Win-rate simulation includes PLAYER_RATING_SCORING_WEIGHT in optimization
- [ ] Accuracy simulation does NOT try to optimize PLAYER_RATING_SCORING
- [ ] league_config.json contains PLAYER_RATING_SCORING after sim run
- [ ] week*.json files do NOT contain PLAYER_RATING_SCORING after sim run

### Backward Compatibility Verification
- [ ] Old configs (PLAYER_RATING_SCORING in week files) still load
- [ ] ConfigManager finds parameter regardless of location
- [ ] Draft mode works with both old and new config structures

### Test Coverage Verification
- [ ] Unit tests updated for list membership
- [ ] Integration tests pass
- [ ] All existing tests still pass
- [ ] No regressions introduced

---

## Implementation Notes

**Dependencies**:
- No new dependencies
- Uses existing ConfigGenerator logic
- Uses existing ResultsManager filtering methods

**Risk Assessment**:
- **Very Low Risk** - Only list membership changes
- ConfigGenerator imports lists, automatically adapts
- ConfigManager is resilient to parameter location
- Backward compatible by design

**Rollback Plan**:
- Simple: revert the 3 line changes
- Old configs continue working
- No data migration needed

---

## Status Tracking

- [ ] All code changes implemented
- [ ] All unit tests updated and passing
- [ ] All integration tests passing
- [ ] Full test suite passing (100%)
- [ ] Backward compatibility verified
- [ ] Code changes documented
- [ ] Ready for QC review
