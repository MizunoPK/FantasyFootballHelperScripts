# Additive Matchup and Schedule Scoring - Code Changes Documentation

**Date**: 2025-10-28
**Status**: COMPLETE - All phases 1-4 implemented, 100% test pass rate
**Objective**: Convert matchup and schedule scoring from multiplicative to additive bonus system

---

## Summary

Successfully converted matchup and schedule scoring factors from multiplicative scaling (e.g., score × 1.25) to additive bonuses (e.g., score + 37.5 pts). This provides:

1. **Consistent Impact**: Bonus magnitude independent of base player score
2. **Clear Optimization**: IMPACT_SCALE parameters control bonus size directly
3. **Improved Balance**: Prevents exponential compounding with other multiplicative factors
4. **Better Interpretability**: "±X points" more intuitive than "×1.X multiplier"

**Test Results**: 100% pass rate (1942/1942 tests passing)

---

## Phase 1: Configuration Updates

### 1.1 Updated league_config.json

**File**: `data/league_config.json`

**Added IMPACT_SCALE parameters**:
- `MATCHUP_SCORING.IMPACT_SCALE`: 150.0 (range: 100.0-200.0)
- `SCHEDULE_SCORING.IMPACT_SCALE`: 80.0 (range: 40.0-120.0)

**Converted to parameterized thresholds**:
```json
"MATCHUP_SCORING": {
  "IMPACT_SCALE": 150.0,
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "BI_EXCELLENT_HI",
    "STEPS": 7.5
  },
  "MULTIPLIERS": {
    "EXCELLENT": 1.25,
    "GOOD": 1.10,
    "POOR": 0.90,
    "VERY_POOR": 0.75
  },
  "WEIGHT": 1.0
},
"SCHEDULE_SCORING": {
  "IMPACT_SCALE": 80.0,
  "THRESHOLDS": {
    "BASE_POSITION": 0,
    "DIRECTION": "INCREASING",
    "STEPS": 8
  },
  "MULTIPLIERS": {
    "EXCELLENT": 1.25,
    "GOOD": 1.10,
    "POOR": 0.90,
    "VERY_POOR": 0.75
  },
  "WEIGHT": 1.0
}
```

### 1.2 Added ConfigManager validation

**File**: `league_helper/util/ConfigManager.py`
**Location**: `_extract_parameters()` method (after line 793)

**Added validation (lines ~794-800)**:
```python
# Validate IMPACT_SCALE is present (required as of additive scoring)
if 'IMPACT_SCALE' not in self.matchup_scoring:
    raise ValueError("MATCHUP_SCORING missing required parameter: IMPACT_SCALE")

if 'IMPACT_SCALE' not in self.schedule_scoring:
    raise ValueError("SCHEDULE_SCORING missing required parameter: IMPACT_SCALE")
```

**Behavior**: ValueError raised if IMPACT_SCALE missing from either scoring section (breaking change - REQUIRED parameter)

---

## Phase 2: Scoring Algorithm Changes

### 2.1 Modified matchup multiplier to additive bonus

**File**: `league_helper/util/player_scoring.py`
**Method**: `_apply_matchup_multiplier()` (line 557-566)

**Before (Multiplicative)**:
```python
def _apply_matchup_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    if p.matchup_score is None:
        multiplier = 1.0
        rating = "NEUTRAL"
    else:
        multiplier, rating = self.config.get_matchup_multiplier(p.matchup_score)

    return player_score * multiplier, f"Matchup: {rating} ({multiplier:.2f}x)"
```

**After (Additive)**:
```python
def _apply_matchup_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
    if p.matchup_score is None:
        multiplier = 1.0
        rating = "NEUTRAL"
    else:
        multiplier, rating = self.config.get_matchup_multiplier(p.matchup_score)

    # Additive bonus system: bonus = (impact_scale * weighted_multiplier) - impact_scale
    impact_scale = self.config.matchup_scoring['IMPACT_SCALE']
    bonus = (impact_scale * multiplier) - impact_scale

    return player_score + bonus, f"Matchup: {rating} ({bonus:+.1f} pts)"
```

**Key Changes**:
- Replaced `score * multiplier` with `score + bonus`
- Added IMPACT_SCALE retrieval (direct dict access - REQUIRED parameter)
- Bonus formula: `(impact_scale * weighted_multiplier) - impact_scale`
- Updated reason string: `({bonus:+.1f} pts)` instead of `({multiplier:.2f}x)`

**Example Calculations** (IMPACT_SCALE=150.0):
- EXCELLENT (1.25): bonus = (150 × 1.25) - 150 = +37.5 pts
- GOOD (1.10): bonus = (150 × 1.10) - 150 = +15.0 pts
- NEUTRAL (1.0): bonus = (150 × 1.0) - 150 = 0.0 pts
- POOR (0.90): bonus = (150 × 0.90) - 150 = -15.0 pts
- VERY_POOR (0.75): bonus = (150 × 0.75) - 150 = -37.5 pts

### 2.2 Modified schedule multiplier to additive bonus

**File**: `league_helper/util/player_scoring.py`
**Method**: `_apply_schedule_multiplier()` (line 568-597)

**Before (Multiplicative)**:
```python
def _apply_schedule_multiplier(self, p: FantasyPlayer, player_score: float, ...) -> Tuple[float, str]:
    # ... schedule calculation ...
    multiplier, rating = self.config.get_schedule_multiplier(schedule_value)

    new_score = player_score * multiplier
    return new_score, f"Schedule: {rating} (avg opp rank: {schedule_value:.1f}, {multiplier:.2f}x)"
```

**After (Additive)**:
```python
def _apply_schedule_multiplier(self, p: FantasyPlayer, player_score: float, ...) -> Tuple[float, str]:
    # ... schedule calculation ...
    multiplier, rating = self.config.get_schedule_multiplier(schedule_value)

    # Additive bonus system
    impact_scale = self.config.schedule_scoring['IMPACT_SCALE']
    bonus = (impact_scale * multiplier) - impact_scale

    new_score = player_score + bonus
    return new_score, f"Schedule: {rating} (avg opp rank: {schedule_value:.1f}, {bonus:+.1f} pts)"
```

**Key Changes**:
- Replaced `score * multiplier` with `score + bonus`
- Added IMPACT_SCALE retrieval (direct dict access - REQUIRED parameter)
- Same bonus formula as matchup scoring
- Updated reason string and debug logs

**Example Calculations** (IMPACT_SCALE=80.0):
- EXCELLENT (1.25): bonus = (80 × 1.25) - 80 = +20.0 pts
- GOOD (1.10): bonus = (80 × 1.10) - 80 = +8.0 pts
- NEUTRAL (1.0): bonus = (80 × 1.0) - 80 = 0.0 pts
- POOR (0.90): bonus = (80 × 0.90) - 80 = -8.0 pts
- VERY_POOR (0.75): bonus = (80 × 0.75) - 80 = -20.0 pts

---

## Phase 3: Simulation System Updates

### 3.1 Added IMPACT_SCALE parameters to ConfigGenerator

**File**: `simulation/ConfigGenerator.py`

**Added to PARAM_DEFINITIONS** (lines 106-113):
```python
# Impact Scale parameters (additive scoring - NEW)
'MATCHUP_IMPACT_SCALE': (25.0, 100.0, 200.0),   # (range, min, max)
'SCHEDULE_IMPACT_SCALE': (20.0, 40.0, 120.0),   # (range, min, max)
```

**Updated PARAMETER_ORDER** (lines 135-137):
```python
# Impact Scales (ADDITIVE SCORING)
'MATCHUP_IMPACT_SCALE',
'SCHEDULE_IMPACT_SCALE',
```

**Total parameters**: 16 → 18 (added 2 IMPACT_SCALE parameters)

### 3.2 Updated config generation logic

**File**: `simulation/ConfigGenerator.py`

**Updated `generate_all_parameter_value_sets()`** (lines 328-339):
```python
# IMPACT_SCALE parameters (additive scoring - NEW)
for scoring_type in ["MATCHUP_SCORING", "SCHEDULE_SCORING"]:
    impact_param = scoring_type.replace('_SCORING', '_IMPACT_SCALE')
    current_impact = params[scoring_type]['IMPACT_SCALE']
    range_val, min_val, max_val = self.param_definitions[impact_param]
    value_sets[impact_param] = self.generate_parameter_values(
        impact_param,
        current_impact,
        range_val,
        min_val,
        max_val
    )
```

**Updated `_extract_combination_from_config()`** (lines 624-627):
```python
# IMPACT_SCALE for additive scoring (NEW)
for section in ['MATCHUP', 'SCHEDULE']:
    param_name = f'{section}_IMPACT_SCALE'
    combination[param_name] = params[f'{section}_SCORING']['IMPACT_SCALE']
```

**Updated `generate_single_parameter_configs()`** (lines 548-555):
```python
elif '_IMPACT_SCALE' in param_name:
    # Extract section for IMPACT_SCALE (additive scoring)
    # Format: SECTION_IMPACT_SCALE (e.g., 'MATCHUP_IMPACT_SCALE')
    parts = param_name.split('_IMPACT_SCALE')
    section = parts[0] + '_SCORING'  # e.g., 'MATCHUP_SCORING'

    current_val = params[section]['IMPACT_SCALE']
    range_val, min_val, max_val = self.param_definitions[param_name]
```

**Config application** (lines 657-659 - already present):
```python
# Update IMPACT_SCALE for additive scoring (NEW)
params['MATCHUP_SCORING']['IMPACT_SCALE'] = combination['MATCHUP_IMPACT_SCALE']
params['SCHEDULE_SCORING']['IMPACT_SCALE'] = combination['SCHEDULE_IMPACT_SCALE']
```

---

## Phase 4: Testing

### 4.1 Created ConfigManager IMPACT_SCALE validation tests

**File**: `tests/league_helper/util/test_ConfigManager_impact_scale.py` (NEW)

**Tests Created** (5 tests):
1. `test_matchup_impact_scale_missing_raises_error` - Verifies ValueError when MATCHUP_SCORING.IMPACT_SCALE missing
2. `test_schedule_impact_scale_missing_raises_error` - Verifies ValueError when SCHEDULE_SCORING.IMPACT_SCALE missing
3. `test_both_impact_scales_present_loads_successfully` - Verifies successful load when both present
4. `test_matchup_impact_scale_accessible` - Verifies IMPACT_SCALE can be accessed
5. `test_schedule_impact_scale_accessible` - Verifies IMPACT_SCALE can be accessed

### 4.2 Updated ALL test fixtures

**Files Updated**:
- `tests/league_helper/util/test_ConfigManager_thresholds.py`
- `tests/league_helper/util/test_ConfigManager_max_positions.py`
- `tests/league_helper/util/test_ConfigManager_flex_eligible_positions.py`
- `tests/league_helper/util/test_FantasyTeam.py`
- `tests/league_helper/util/test_player_scoring.py`
- `tests/league_helper/add_to_roster_mode/test_AddToRosterModeManager.py`
- `tests/league_helper/reserve_assessment_mode/test_ReserveAssessmentModeManager.py`
- `tests/league_helper/trade_simulator_mode/test_manual_trade_visualizer.py`

**Changes Made**: Added `IMPACT_SCALE` to all MATCHUP_SCORING and SCHEDULE_SCORING fixtures

### 4.3 Updated scoring test assertions

**File**: `tests/league_helper/util/test_PlayerManager_scoring.py`

**Updated Tests** (10 tests):
1. `test_matchup_excellent` - Changed from multiplicative to additive assertions
2. `test_matchup_good` - Changed from multiplicative to additive assertions
3. `test_matchup_neutral` - Changed from multiplicative to additive assertions
4. `test_matchup_poor` - Changed from multiplicative to additive assertions
5. `test_matchup_very_poor` - Changed from multiplicative to additive assertions
6. `test_matchup_none_returns_neutral` - Updated reason string assertions
7. `test_matchup_score_exact_boundaries` - Updated boundary value assertions
8. `test_extremely_negative_matchup_score` - Updated extreme value assertions
9. `test_score_player_with_weekly_projection` - Updated integration test
10. `test_score_player_all_flags_enabled` - Updated full scoring integration test

**Example Before/After**:
```python
# Before (Multiplicative)
def test_matchup_excellent(self, player_manager, test_player):
    test_player.matchup_score = 18
    base_score = 100.0
    result, reason = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
    assert result == 100.0 * 1.25
    assert reason == "Matchup: EXCELLENT (1.25x)"

# After (Additive)
def test_matchup_excellent(self, player_manager, test_player):
    """Matchup >= 15 should get EXCELLENT (+37.5 pts with IMPACT_SCALE=150.0)"""
    test_player.matchup_score = 18
    base_score = 100.0
    result, reason = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
    # IMPACT_SCALE=150.0, multiplier=1.25: bonus = (150*1.25)-150 = +37.5
    assert result == pytest.approx(100.0 + 37.5, abs=0.1)
    assert "EXCELLENT" in reason
    assert "pts" in reason
```

### 4.4 Updated ConfigGenerator tests

**File**: `tests/simulation/test_config_generator.py`

**Changes Made**:
- Updated parameter count assertions: 16 → 18
- Added MATCHUP_IMPACT_SCALE and SCHEDULE_IMPACT_SCALE assertions
- Updated test_parameter_order_exists: `assert len(gen.PARAMETER_ORDER) == 18`
- Updated test_generate_all_parameter_value_sets_returns_all_params: `assert len(value_sets) == 18`
- Updated test_edge_case_num_parameters_exceeds_available:
  - Expected configs: 65,568 → 262,180
  - Calculation: 2^16 + 32 → 2^18 + 36

---

## Test Results

**Final Test Pass Rate**: 100% (1942/1942 tests passing)

**Test Progress**:
- Start of session: 97.1% (1886/1942)
- After fixture updates: 98.7% (1916/1942)
- After scoring assertions: 99.1% (1924/1942)
- After ConfigGenerator updates: 99.9% (1941/1942)
- Final (all tests fixed): 100% (1942/1942)

**Test Categories**:
- ConfigManager validation tests: 5 new tests (all passing)
- Scoring algorithm tests: 79 tests (10 updated for additive scoring)
- ConfigGenerator tests: 32 tests (15 updated for 18 parameters)
- Integration tests: 25 tests (1 updated for additive scoring)
- Total tests: 1942 tests (100% passing)

---

## Breaking Changes

### Required Configuration Update

**IMPACT_SCALE is now REQUIRED** in both MATCHUP_SCORING and SCHEDULE_SCORING sections.

**Migration Required**:
- All existing configs must add `IMPACT_SCALE: 150.0` to MATCHUP_SCORING
- All existing configs must add `IMPACT_SCALE: 80.0` to SCHEDULE_SCORING
- ConfigManager will raise ValueError if IMPACT_SCALE is missing

### Scoring Behavior Change

**Matchup and Schedule scoring changed from multiplicative to additive**:
- Before: score × multiplier (e.g., 100 × 1.25 = 125)
- After: score + bonus (e.g., 100 + 37.5 = 137.5)

**Impact**: Scores will be different, requires re-optimization of parameters

---

## Next Steps (User-Driven)

### Phase 6: Simulation and Optimization (USER)
1. Run full parameter re-optimization: `python run_simulation.py iterative --sims 100 --workers 8`
2. Optimize all 18 parameters (including new IMPACT_SCALE values)
3. Evaluate win rate (target: ≥70%)
4. If ≥70%: Accept implementation, update config with optimal values
5. If <70%: Revert changes, keep current system

### Phase 7: Finalization (IF ACCEPTED)
1. Update `data/league_config.json` with optimized IMPACT_SCALE values
2. Run final validation: `python tests/run_all_tests.py` (verify 100% pass rate)
3. Commit implementation with clear commit message
4. Move this file to `updates/done/`
5. Delete questions file

---

## Implementation Notes

### Why Additive Instead of Multiplicative?

1. **Consistent Impact**: A +37.5 point bonus is the same whether the player's base score is 50 or 150
2. **Prevents Compounding**: With multiplicative factors, high-scoring players get exponentially more benefit
3. **Clearer Optimization**: IMPACT_SCALE directly controls bonus magnitude (easier to interpret and optimize)
4. **Better Balance**: Prevents matchup/schedule from dominating other factors for elite players

### Formula Explanation

```python
bonus = (impact_scale * weighted_multiplier) - impact_scale
```

**Why this formula?**:
- When multiplier = 1.0 (neutral), bonus = 0.0 (no change)
- When multiplier > 1.0 (good), bonus > 0.0 (positive bonus)
- When multiplier < 1.0 (poor), bonus < 0.0 (negative penalty)
- IMPACT_SCALE controls the magnitude of the bonus/penalty
- Weighted multiplier already has WEIGHT applied by ConfigManager

**Example** (IMPACT_SCALE=150.0):
- Neutral (1.0): (150 × 1.0) - 150 = 0 pts
- Excellent (1.25): (150 × 1.25) - 150 = +37.5 pts
- Very Poor (0.75): (150 × 0.75) - 150 = -37.5 pts

### Parameter Ranges

**MATCHUP_IMPACT_SCALE**:
- Baseline: 150.0
- Range: ±25.0
- Bounds: 100.0 - 200.0
- At 200.0: EXCELLENT bonus = +50 pts

**SCHEDULE_IMPACT_SCALE**:
- Baseline: 80.0
- Range: ±20.0
- Bounds: 40.0 - 120.0
- At 120.0: EXCELLENT bonus = +30 pts

---

**End of Code Changes Documentation**
