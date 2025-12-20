# Move Player Rating to League Config - Code Changes

## Implementation Summary

Successfully moved PLAYER_RATING_SCORING from WEEK_SPECIFIC_PARAMS to BASE_CONFIG_PARAMS.

**Result:** All 2296 tests passing (100%)

---

## Code Changes

### 1. simulation/shared/ResultsManager.py

**Location:** Lines 252 and 257

**Change 1 - Add to BASE_CONFIG_PARAMS (Line 252):**
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
    'PLAYER_RATING_SCORING'  # ← ADDED
]
```

**Change 2 - Remove from WEEK_SPECIFIC_PARAMS (Line 257):**
```python
WEEK_SPECIFIC_PARAMS = [
    'NORMALIZATION_MAX_SCALE',
    # 'PLAYER_RATING_SCORING',  # ← REMOVED
    'TEAM_QUALITY_SCORING',
    'PERFORMANCE_SCORING',
    'MATCHUP_SCORING',
    'SCHEDULE_SCORING',
    'TEMPERATURE_SCORING',
    'WIND_SCORING',
    'LOCATION_MODIFIERS'
]
```

**Impact:**
- PLAYER_RATING_SCORING now saved in league_config.json
- No longer appears in week*.json horizon files
- ConfigGenerator automatically adapts (imports these lists)

---

### 2. run_win_rate_simulation.py

**Location:** Line 64

**Change - Add to PARAMETER_ORDER:**
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
    'PLAYER_RATING_SCORING_WEIGHT',  # ← ADDED
]
```

**Impact:**
- Win-rate simulation now optimizes PLAYER_RATING_SCORING_WEIGHT
- Total win-rate parameters: 6 (was 5)

---

### 3. tests/simulation/test_ResultsManager.py

**4 test updates to expect PLAYER_RATING_SCORING in base config instead of week configs**

**Change 1 - test_save_optimal_configs_folder_week_configs_have_week_params (Line 1144):**
```python
# Week config should NOT have base params (including PLAYER_RATING_SCORING which moved to base)
assert "CURRENT_NFL_WEEK" not in week_config["parameters"]
assert "NFL_SEASON" not in week_config["parameters"]
assert "PLAYER_RATING_SCORING" not in week_config["parameters"]  # ← ADDED
```

**Change 2 - test_save_optimal_configs_folder_base_config_has_base_params (Line 1113):**
```python
# Base config should have base params (including PLAYER_RATING_SCORING which moved to base)
assert "CURRENT_NFL_WEEK" in base_config["parameters"]
assert "NFL_SEASON" in base_config["parameters"]
assert "PLAYER_RATING_SCORING" in base_config["parameters"]  # ← ADDED
```

**Change 3 - test_save_and_load_round_trip_6_files (Lines 1649-1656):**
```python
# Verify base params preserved (including PLAYER_RATING_SCORING which moved to base)
assert loaded_base["parameters"]["ADP_SCORING"]["WEIGHT"] == 1.0
assert "PLAYER_RATING_SCORING" in loaded_base["parameters"]  # ← ADDED
assert loaded_base["parameters"]["PLAYER_RATING_SCORING"]["WEIGHT"] == 2.0  # ← ADDED

# Verify week params preserved in all horizons
for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
    assert horizon in loaded_weeks
    assert "TEAM_QUALITY_SCORING" in loaded_weeks[horizon]["parameters"]  # ← CHANGED from PLAYER_RATING
    assert loaded_weeks[horizon]["parameters"]["TEAM_QUALITY_SCORING"]["WEIGHT"] == 1.5
```

**Change 4 - test_draft_config_contains_week_specific_params (Lines 1568-1572):**
```python
# Should have week-specific params (not PLAYER_RATING_SCORING which moved to base)
assert "TEAM_QUALITY_SCORING" in draft_config["parameters"]
# Should NOT have base params
assert "ADP_SCORING" not in draft_config["parameters"]
assert "PLAYER_RATING_SCORING" not in draft_config["parameters"]  # ← ADDED
```

**Impact:**
- 65/65 tests passing in test_ResultsManager.py
- Tests verify correct config structure

---

### 4. tests/simulation/test_config_generator.py

**3 test updates to use TEAM_QUALITY_SCORING_WEIGHT instead of PLAYER_RATING_SCORING_WEIGHT**

Since PLAYER_RATING_SCORING_WEIGHT is now a shared/base parameter (not horizon-specific), tests needed to use a different horizon-specific parameter as an example.

**Change 1 - test_generate_horizon_test_values_for_horizon_param (Lines 1122-1137):**
```python
# TEAM_QUALITY_SCORING_WEIGHT is week-specific  # ← CHANGED comment
test_values = generator.generate_horizon_test_values('TEAM_QUALITY_SCORING_WEIGHT')  # ← CHANGED param

# Should have all 5 horizon keys
assert 'ros' in test_values
assert '1-5' in test_values
assert '6-9' in test_values
assert '10-13' in test_values
assert '14-17' in test_values
assert len(test_values) == 5

# Each horizon should have 6 values
for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
    assert len(test_values[horizon]) == 6
    # First value should be baseline (1.5)  # ← CHANGED expected value
    assert test_values[horizon][0] == 1.5  # ← CHANGED from 2.0
```

**Change 2 - test_get_config_for_horizon_with_horizon_param (Lines 1161-1167):**
```python
test_values = generator.generate_horizon_test_values('TEAM_QUALITY_SCORING_WEIGHT')  # ← CHANGED param

# Get config for 'ros' horizon with test_index 2
config = generator.get_config_for_horizon('ros', 'TEAM_QUALITY_SCORING_WEIGHT', 2)  # ← CHANGED param

# Should have the test value from 'ros' array
assert config['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == test_values['ros'][2]  # ← CHANGED path
```

**Change 3 - test_update_baseline_for_horizon_with_horizon_param (Lines 1191-1202):**
```python
# Create new config with updated horizon param
new_config = copy.deepcopy(generator.baseline_configs['ros'])
new_config['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] = 5.0  # ← CHANGED param path

# Update only 'ros' horizon
generator.update_baseline_for_horizon('ros', new_config)

# Only 'ros' should be updated
assert generator.baseline_configs['ros']['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 5.0  # ← CHANGED

# Other horizons should still have original value (1.5)  # ← CHANGED expected value
assert generator.baseline_configs['1-5']['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.5  # ← CHANGED
assert generator.baseline_configs['6-9']['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.5  # ← CHANGED
```

**Impact:**
- 52/52 tests passing in test_config_generator.py
- Tests now use appropriate horizon-specific parameter for examples

---

### 5. tests/simulation/test_AccuracyResultsManager.py

**8 test updates - 3 for config structure, 5 for _sync_schedule_params**

**Pre-existing Bug Fix:**
The _sync_schedule_params method was using flat parameter names but configs use nested structures. Fixed both the method and its tests.

**Test Config Updates (3 tests):**

**Change 1 - test_save_optimal_configs (Lines 239-266):**
```python
# Use real WEEK_SPECIFIC_PARAMS parameters with nested structure
config_ros = {'TEAM_QUALITY_SCORING': {'WEIGHT': 1.5}}  # ← CHANGED to nested
config_week = {'MATCHUP_SCORING': {'WEIGHT': 1.2}}  # ← CHANGED to nested
result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)

results_manager.add_result('ros', config_ros, result)
results_manager.add_result('week_1_5', config_week, result)

# ... verification code ...

assert 'TEAM_QUALITY_SCORING' in saved_config['parameters']  # ← CHANGED verification
assert saved_config['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.5  # ← CHANGED to nested
```

**Change 2 - test_save_optimal_configs_syncs_schedule (Lines 422-442):**
```python
# Use nested structure matching actual config format
config = {
    'MATCHUP_SCORING': {  # ← CHANGED to nested
        'IMPACT_SCALE': 0.8,
        'WEIGHT': 0.15,
        'MIN_WEEKS': 3
    }
}
result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)
results_manager.add_result('ros', config, result)

optimal_path = results_manager.save_optimal_configs()

with open(optimal_path / "draft_config.json") as f:
    saved_config = json.load(f)

# SCHEDULE params should mirror MATCHUP in parameters section (nested structure)
params = saved_config['parameters']
assert 'SCHEDULE_SCORING' in params  # ← CHANGED to nested verification
assert params['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.8
assert params['SCHEDULE_SCORING']['WEIGHT'] == 0.15
assert params['SCHEDULE_SCORING']['MIN_WEEKS'] == 3
```

**Change 3 - test_save_intermediate_results_syncs_schedule (Lines 447-463):**
```python
# Use nested structure matching actual config format
config = {
    'MATCHUP_SCORING': {  # ← CHANGED to nested
        'IMPACT_SCALE': 0.7
    }
}
result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)
results_manager.add_result('ros', config, result)

intermediate_path = results_manager.save_intermediate_results(0, 'TEST')

# Check the standard config file (draft_config.json for 'ros')
with open(intermediate_path / "draft_config.json") as f:
    saved_data = json.load(f)

# SCHEDULE params should mirror MATCHUP in parameters section (nested structure)
assert 'SCHEDULE_SCORING' in saved_data['parameters']  # ← CHANGED to nested
assert saved_data['parameters']['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.7
```

**_sync_schedule_params Unit Tests (4 tests):**

**Change 4 - test_sync_schedule_params_all_matchup_params (Lines 369-384):**
```python
# Use nested structure
config = {
    'MATCHUP_SCORING': {  # ← CHANGED to nested
        'IMPACT_SCALE': 0.8,
        'WEIGHT': 0.15,
        'MIN_WEEKS': 3
    },
    'OTHER_PARAM': 'value'
}

synced = results_manager._sync_schedule_params(config)

assert 'SCHEDULE_SCORING' in synced  # ← CHANGED to nested verification
assert synced['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.8
assert synced['SCHEDULE_SCORING']['WEIGHT'] == 0.15
assert synced['SCHEDULE_SCORING']['MIN_WEEKS'] == 3
assert synced['OTHER_PARAM'] == 'value'  # Other params preserved
```

**Change 5 - test_sync_schedule_params_partial (Lines 387-400):**
```python
config = {
    'MATCHUP_SCORING': {  # ← CHANGED to nested
        'IMPACT_SCALE': 0.5
    },
    'OTHER_PARAM': 'value'
}

synced = results_manager._sync_schedule_params(config)

assert 'SCHEDULE_SCORING' in synced  # ← CHANGED to nested
assert synced['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.5
assert 'WEIGHT' not in synced['SCHEDULE_SCORING']  # ← CHANGED to nested
assert 'MIN_WEEKS' not in synced['SCHEDULE_SCORING']
```

**Change 6 - test_sync_schedule_params_no_matchup (Lines 402-409):**
```python
config = {'OTHER_PARAM': 'value'}

synced = results_manager._sync_schedule_params(config)

assert 'SCHEDULE_SCORING' not in synced  # ← CHANGED to nested
assert synced == config
```

**Change 7 - test_sync_schedule_params_preserves_original (Lines 413-427):**
```python
config = {
    'MATCHUP_SCORING': {  # ← CHANGED to nested
        'IMPACT_SCALE': 0.8
    },
    'SCHEDULE_SCORING': {  # ← CHANGED to nested
        'IMPACT_SCALE': 0.5  # Different value
    }
}

synced = results_manager._sync_schedule_params(config)

# Original unchanged
assert config['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.5  # ← CHANGED to nested
# Synced has MATCHUP value
assert synced['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.8  # ← CHANGED to nested
```

**Impact:**
- 30/30 tests passing in test_AccuracyResultsManager.py
- Fixed pre-existing bug in _sync_schedule_params

---

### 6. simulation/accuracy/AccuracyResultsManager.py

**Location:** Lines 243-280

**Pre-existing Bug Fix - _sync_schedule_params method:**

Updated to handle nested config structures (MATCHUP_SCORING → SCHEDULE_SCORING) instead of flat parameter names.

```python
def _sync_schedule_params(self, config: dict) -> dict:
    """
    Sync SCHEDULE params with MATCHUP params.

    SCHEDULE and MATCHUP should use the same values because schedule strength
    is a forward-looking version of matchup strength. Keeping them in sync
    ensures consistent opponent evaluation.

    Params synced:
    - SCHEDULE_SCORING.IMPACT_SCALE = MATCHUP_SCORING.IMPACT_SCALE
    - SCHEDULE_SCORING.WEIGHT = MATCHUP_SCORING.WEIGHT
    - SCHEDULE_SCORING.MIN_WEEKS = MATCHUP_SCORING.MIN_WEEKS

    Args:
        config: Configuration dictionary to update (nested structure)

    Returns:
        dict: Updated config with synced SCHEDULE params
    """
    import copy
    synced = copy.deepcopy(config)

    # Handle nested structure: MATCHUP_SCORING -> SCHEDULE_SCORING
    if 'MATCHUP_SCORING' in synced:
        matchup = synced['MATCHUP_SCORING']
        schedule = synced.get('SCHEDULE_SCORING', {})

        # Copy relevant fields from MATCHUP to SCHEDULE
        if 'IMPACT_SCALE' in matchup:
            schedule['IMPACT_SCALE'] = matchup['IMPACT_SCALE']
        if 'WEIGHT' in matchup:
            schedule['WEIGHT'] = matchup['WEIGHT']
        if 'MIN_WEEKS' in matchup:
            schedule['MIN_WEEKS'] = matchup['MIN_WEEKS']

        synced['SCHEDULE_SCORING'] = schedule

    return synced
```

**Impact:**
- Fixed pre-existing bug (method was using flat params but system uses nested)
- Now matches ResultsManager._apply_matchup_to_schedule_mapping pattern
- All SCHEDULE sync tests now pass

---

## Test Results

**Final Status:** All 2296 tests passing (100%)

**Test Breakdown:**
- test_ResultsManager.py: 65/65 (100%)
- test_config_generator.py: 52/52 (100%)
- test_AccuracyResultsManager.py: 30/30 (100%)
- All other test files: 2149/2149 (100%)

**Test Failures Fixed:**
- 3 failures from PLAYER_RATING location change (test_ResultsManager.py)
- 3 failures from using wrong example param (test_config_generator.py)
- 3 failures from flat param structure (test_AccuracyResultsManager.py - config tests)
- 1 pre-existing bug discovered and fixed (_sync_schedule_params method + 4 tests)

---

## Backward Compatibility

**ConfigManager is resilient to parameter location:**
- Can load configs with PLAYER_RATING_SCORING in week files (old format)
- Can load configs with PLAYER_RATING_SCORING in league_config.json (new format)
- Uses `parameters.update(prediction_params)` which merges configs
- No migration needed for existing configs

**Automatic adaptation:**
- ConfigGenerator imports BASE_CONFIG_PARAMS and WEEK_SPECIFIC_PARAMS from ResultsManager
- Changing the lists automatically changes save/load behavior
- No code changes needed in ConfigGenerator itself

---

## Verification

**Manual verification performed:**
- Created test config with nested TEAM_QUALITY_SCORING structure
- Verified AccuracyResultsManager correctly saves nested params
- Confirmed SCHEDULE sync creates nested SCHEDULE_SCORING structure

**Integration testing:**
- All unit tests pass
- Parameter location change verified through test assertions
- Config save/load roundtrip verified

---

## Additional Updates

**Documentation updated:**
- feature-updates/validate_all_winrate_params.txt: Updated to include PLAYER_RATING_SCORING_WEIGHT as 6th parameter
- run_win_rate_simulation.py comments: Added description of PLAYER_RATING_SCORING_WEIGHT purpose

---

## Summary

**Total Changes:**
- 3 core implementation changes (ResultsManager.py x2, run_win_rate_simulation.py x1)
- 11 test updates (4 + 3 + 3 + 1 bug fix)
- 1 pre-existing bug fix (AccuracyResultsManager._sync_schedule_params)
- 2 documentation updates

**Impact:**
- PLAYER_RATING_SCORING now correctly classified as base/strategy parameter
- Win-rate simulation will optimize PLAYER_RATING_SCORING_WEIGHT
- Accuracy simulation will NOT optimize it (correct behavior)
- All tests passing (100%)
- Backward compatible
