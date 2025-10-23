# Bye Scaling Penalties - Code Changes Documentation

**Objective**: Replace BASE_BYE_PENALTY and DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY with SAME_POS_BYE_WEIGHT and DIFF_POS_BYE_WEIGHT, implementing median-based exponential penalty calculation.

**Status**: ✅ Complete

**Started**: 2025-10-23
**Completed**: 2025-10-23

---

## Phase 1: Configuration Changes

### File: data/league_config.json

**Status**: ✅ Complete

**Changes**:
- Line 9: Removed `"BASE_BYE_PENALTY": 41.3376210022945`
- Line 10: Removed `"DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 1.9523025294345953`
- Line 9 (new): Added `"SAME_POS_BYE_WEIGHT": 1.0`
- Line 10 (new): Added `"DIFF_POS_BYE_WEIGHT": 1.0`

**Before**:
```json
"NORMALIZATION_MAX_SCALE": 141.67703079140796,
"BASE_BYE_PENALTY": 41.3376210022945,
"DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 1.9523025294345953,
"INJURY_PENALTIES": {
```

**After**:
```json
"NORMALIZATION_MAX_SCALE": 141.67703079140796,
"SAME_POS_BYE_WEIGHT": 1.0,
"DIFF_POS_BYE_WEIGHT": 1.0,
"INJURY_PENALTIES": {
```

**Rationale**: Replace linear penalty parameters with exponential weight parameters for new median-based algorithm.

---

### File: league_helper/util/ConfigManager.py - Part 1: Configuration Keys and Attributes

**Status**: ✅ Complete

**Changes**:
- Line 55-56: Replaced `BASE_BYE_PENALTY` with `SAME_POS_BYE_WEIGHT` and `DIFF_POS_BYE_WEIGHT` in ConfigKeys
- Line 174-175: Replaced `self.base_bye_penalty` with `self.same_pos_bye_weight` and `self.diff_pos_bye_weight` attributes
- Line 737-738: Updated required_params list to include new parameter keys
- Line 762-763: Updated parameter extraction to load new values from config

**Before (ConfigKeys)**:
```python
NORMALIZATION_MAX_SCALE = "NORMALIZATION_MAX_SCALE"
BASE_BYE_PENALTY = "BASE_BYE_PENALTY"
INJURY_PENALTIES = "INJURY_PENALTIES"
```

**After (ConfigKeys)**:
```python
NORMALIZATION_MAX_SCALE = "NORMALIZATION_MAX_SCALE"
SAME_POS_BYE_WEIGHT = "SAME_POS_BYE_WEIGHT"
DIFF_POS_BYE_WEIGHT = "DIFF_POS_BYE_WEIGHT"
INJURY_PENALTIES = "INJURY_PENALTIES"
```

**Rationale**: Update ConfigManager to recognize and load new weight parameters instead of old linear penalty values.

---

### File: league_helper/util/ConfigManager.py - Part 2: Bye Penalty Algorithm

**Status**: ✅ Complete

**Changes**:
- Line 20: Added `import statistics`
- Line 30: Added `from utils.FantasyPlayer import FantasyPlayer`
- Lines 382-462: Completely rewrote `get_bye_week_penalty()` method

**Before (signature)**:
```python
def get_bye_week_penalty(self, num_same_position: int, num_different_position: int = 0) -> float:
```

**After (signature)**:
```python
def get_bye_week_penalty(self, same_pos_players: List[FantasyPlayer], diff_pos_players: List[FantasyPlayer]) -> float:
```

**Algorithm Changes**:
- **Old**: Linear penalty with bye week scaling: `(BASE_BYE * scale * count) + (DIFF_BYE * scale * count)`
- **New**: Median-based exponential scaling: `(same_median_total ** SAME_POS_BYE_WEIGHT) + (diff_median_total ** DIFF_POS_BYE_WEIGHT)`

**Key Features**:
- Internal helper function `calculate_player_median()` for each player
- Filters out None and zero values from weekly data (weeks 1-17)
- Comprehensive error handling with StatisticsError catch
- Debug logging for transparency (shows medians, weights, and final penalty)
- Warning logging when players have no valid weekly data

**Rationale**: Implement new median-based penalty algorithm that scales exponentially with player impact, removing the time-based bye week scaling in favor of value-based scaling.

---

## Phase 2: Algorithm Implementation

### File: league_helper/util/player_scoring.py

**Status**: ✅ Complete

**Changes**:
- Lines 620-678: Updated `_apply_bye_week_penalty()` method to collect player lists and pass to ConfigManager

**Before**:
```python
num_same_position = 0
num_different_position = 0
# ... counting logic ...
num_same_position += 1
num_different_position += 1
penalty = self.config.get_bye_week_penalty(num_same_position, num_different_position)
```

**After**:
```python
same_pos_players = []
diff_pos_players = []
# ... collection logic ...
same_pos_players.append(roster_player)
diff_pos_players.append(roster_player)
penalty = self.config.get_bye_week_penalty(same_pos_players, diff_pos_players)
```

**Key Changes**:
- Line 639-640: Changed from count variables to player lists
- Line 663: Append to `same_pos_players` instead of incrementing counter
- Line 666: Append to `diff_pos_players` instead of incrementing counter
- Line 669: Pass player lists to ConfigManager instead of counts
- Line 675: Use `len(same_pos_players)` and `len(diff_pos_players)` for reason string
- Updated docstring to reflect median-based exponential scaling algorithm
- **PRESERVED**: Check for bye week already passed (line 646) ✅

**Rationale**: Update caller to provide player objects instead of counts, enabling ConfigManager to calculate medians from weekly data.

---

## Phase 3: Simulation Updates

### File: simulation/ConfigGenerator.py

**Status**: ✅ Complete

**Changes**:
- Lines 12-13: Updated docstring to reflect new parameters
- Lines 56-57: Replaced old parameters in PARAM_DEFINITIONS with new weight parameters
- Lines 115-116: Updated PARAMETER_ORDER list
- Lines 263-275: Updated generate_all_parameter_value_sets() method
- Lines 512-517: Updated generate_single_parameter_configs() method
- Lines 583-584: Updated _extract_combination_from_config() method
- Lines 631-632: Updated create_config_dict() method

**Parameter Definition Changes**:
```python
# Before
'BASE_BYE_PENALTY': (10.0, 0.0, 200.0),
'DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY': (10.0, 0.0, 200.0),

# After
'SAME_POS_BYE_WEIGHT': (0.2, 0.0, 3.0),
'DIFF_POS_BYE_WEIGHT': (0.2, 0.0, 3.0),
```

**Rationale**: Update simulation system to optimize new exponential weight parameters instead of linear penalty values. Conservative ranges (±0.2, [0, 3]) prevent extreme exponential effects during optimization.

---

## Phase 4: Test Updates

**Status**: ✅ Complete (1910/1910 tests passing - 100%)

**Changes Completed**:
- Batch replaced `BASE_BYE_PENALTY` with `SAME_POS_BYE_WEIGHT` and `DIFF_POS_BYE_WEIGHT` in all test config fixtures
- Updated `test_ConfigManager_thresholds.py` bye penalty tests to use new median-based algorithm with mock FantasyPlayer objects
- Fixed `test_PlayerManager_scoring.py`: Added weekly points data to mock players in 6 bye penalty tests
- Fixed `test_player_scoring.py`: Added weekly points data to test_score_player_with_bye_penalty
- Fixed `test_config_generator.py`: Updated all 9 tests with new parameter names in test data and assertions
- Fixed `test_simulation_integration.py`: Updated integration test with new parameter names

**Test Files Modified**:
- `tests/league_helper/util/test_ConfigManager_thresholds.py` - Algorithm tests updated
- `tests/league_helper/util/test_PlayerManager_scoring.py` - 79/79 tests passing
- `tests/league_helper/util/test_player_scoring.py` - 31/31 tests passing
- `tests/simulation/test_config_generator.py` - 32/32 tests passing
- `tests/integration/test_simulation_integration.py` - 16/16 tests passing

**Fix Pattern Applied**:
```python
# Add weekly points to mock players for median calculation
rb = FantasyPlayer(id=99, name="Other RB", team="BUF", position="RB", bye_week=7)
rb.week_1_points = 18.0
rb.week_2_points = 20.0
rb.week_3_points = 22.0  # Median = 20.0
```

**Result**: All 1910 tests passing (100%). Phase 4 complete.

---

## Phase 5: Documentation Updates

**Status**: ✅ Complete

**Changes Made**:

### File: README.md
- Line 277: Updated configuration parameter description
  - Before: `bye_week_penalty_[position]`: Penalties for bye week clustering
  - After: `SAME_POS_BYE_WEIGHT` / `DIFF_POS_BYE_WEIGHT`: Weights for median-based bye week penalty calculation

### File: ARCHITECTURE.md
- Lines 202-209: Updated bye week penalty description with new algorithm details
  - Added detailed explanation of median-based exponential penalty calculation
  - Documented 4-step calculation process
- Line 286: Updated ConfigManager method signature
  - Before: `get_bye_week_penalty(self, position: str) -> float`
  - After: `get_bye_week_penalty(self, same_pos_players: List[FantasyPlayer], diff_pos_players: List[FantasyPlayer]) -> float`
- Line 673: Updated simulation optimization parameters
  - Before: `bye_week_penalty_qb/rb/wr/te/k/dst` - Bye penalties (6 params)
  - After: `SAME_POS_BYE_WEIGHT` / `DIFF_POS_BYE_WEIGHT` - Bye penalty exponential weights (2 params)
- Line 850: Clarified bye penalty calculation method
  - Before: Apply bye week penalty (from config)
  - After: Apply median-based bye week penalty (from config)

**Rationale**: Update all user-facing documentation to reflect the new median-based exponential bye penalty algorithm, ensuring developers and users understand the new system.

---

## Phase 6: Validation

**Status**: ✅ Complete

**Final Validation Results**:
- ✅ All 1910 unit tests passing (100%)
- ✅ No regressions introduced
- ✅ New median-based algorithm working correctly
- ✅ Documentation updated and accurate
- ✅ Code changes documented comprehensively

**Test Suite Breakdown**:
- Integration tests: 25/25 passing
- League helper tests: 1000+ passing
- Simulation tests: 500+ passing
- Data fetcher tests: 200+ passing
- Utility tests: 185+ passing

**Implementation Complete**: All phases finished successfully. The bye week penalty system has been successfully migrated from linear time-based scaling to median-based exponential scaling.

---

## Summary

**Files Modified**: 9/9 ✅
- [x] data/league_config.json
- [x] league_helper/util/ConfigManager.py
- [x] league_helper/util/player_scoring.py
- [x] simulation/ConfigGenerator.py
- [x] tests/league_helper/util/test_ConfigManager_thresholds.py
- [x] tests/league_helper/util/test_player_scoring.py
- [x] tests/league_helper/util/test_PlayerManager_scoring.py
- [x] tests/simulation/test_config_generator.py
- [x] tests/integration/test_simulation_integration.py

**Tests Passing**: 1910/1910 (100%) ✅

**Implementation Status**: ✅ COMPLETE

**Phase Summary**:
- ✅ Phase 1: Configuration changes - Complete
- ✅ Phase 2: Algorithm implementation - Complete
- ✅ Phase 3: Simulation updates - Complete
- ✅ Phase 4: Test updates - Complete
- ✅ Phase 5: Documentation updates - Complete
- ✅ Phase 6: Final validation - Complete

**Completion Date**: 2025-10-23
