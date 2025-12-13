# Week-Specific Point Normalization - Code Changes

## Summary

Moved `NORMALIZATION_MAX_SCALE` from base config to week-specific configs, enabling per-week optimization in simulation.

---

## Files Modified

### 1. data/configs/league_config.json

**Change:** Removed `NORMALIZATION_MAX_SCALE` parameter

```diff
-    "NORMALIZATION_MAX_SCALE": 163,
```

**Reason:** Parameter now lives in week-specific configs

---

### 2. data/configs/week1-5.json

**Change:** Added `NORMALIZATION_MAX_SCALE: 163`

```json
"parameters": {
    "NORMALIZATION_MAX_SCALE": 163,
    ...
}
```

---

### 3. data/configs/week6-9.json

**Change:** Added `NORMALIZATION_MAX_SCALE: 153`

```json
"parameters": {
    "NORMALIZATION_MAX_SCALE": 153,
    ...
}
```

---

### 4. data/configs/week10-13.json

**Change:** Added `NORMALIZATION_MAX_SCALE: 143`

```json
"parameters": {
    "NORMALIZATION_MAX_SCALE": 143,
    ...
}
```

---

### 5. data/configs/week14-17.json

**Change:** Added `NORMALIZATION_MAX_SCALE: 133`

```json
"parameters": {
    "NORMALIZATION_MAX_SCALE": 133,
    ...
}
```

---

### 6. simulation/ResultsManager.py

**Change:** Moved `NORMALIZATION_MAX_SCALE` from `BASE_CONFIG_PARAMS` to `WEEK_SPECIFIC_PARAMS`

**Before (line 242):**
```python
BASE_CONFIG_PARAMS = [
    'CURRENT_NFL_WEEK',
    'NFL_SEASON',
    'NFL_SCORING_FORMAT',
    'NORMALIZATION_MAX_SCALE',  # <-- was here
    'SAME_POS_BYE_WEIGHT',
    ...
]
```

**After (line 255):**
```python
WEEK_SPECIFIC_PARAMS = [
    'NORMALIZATION_MAX_SCALE',  # <-- moved here
    'PLAYER_RATING_SCORING',
    ...
]
```

**Impact:**
- `ConfigGenerator.is_base_param('NORMALIZATION_MAX_SCALE')` now returns `False`
- `ConfigGenerator.is_week_specific_param('NORMALIZATION_MAX_SCALE')` now returns `True`
- Simulation can optimize this parameter independently per week range

---

## Integration Verification

| Requirement | Implementation | Verified |
|-------------|----------------|----------|
| Remove from base config | `league_config.json` edited | Yes |
| Add to week1-5.json with value 163 | Added to parameters section | Yes |
| Add to week6-9.json with value 153 | Added to parameters section | Yes |
| Add to week10-13.json with value 143 | Added to parameters section | Yes |
| Add to week14-17.json with value 133 | Added to parameters section | Yes |
| Enable per-week simulation optimization | Moved to WEEK_SPECIFIC_PARAMS | Yes |

---

## Data Flow Verification

### ConfigManager Loading (League Helper)
```
run_league_helper.py
  → LeagueHelperManager.__init__()
  → ConfigManager.__init__(data_folder)
  → ConfigManager._load_config()
  → ConfigManager._load_week_config(week=15)  # Current week
  → Loads week14-17.json (weeks 14-17 range)
  → parameters.update(week_params)  # Merges NORMALIZATION_MAX_SCALE: 133
  → ConfigManager._extract_parameters()
  → self.normalization_max_scale = 133  # Week-specific value used
```

### ResultsManager Saving (Simulation)
```
run_simulation.py --mode iterative
  → SimulationManager.run_iterative_optimization()
  → ResultsManager.save_optimal_configs_folder()
  → ResultsManager._extract_week_params()
  → NORMALIZATION_MAX_SCALE in WEEK_SPECIFIC_PARAMS  # Now included
  → Written to each week{N}-{M}.json file
```

---

## Test Results

**All 2221 tests pass (100%)**

No test changes were required because:
1. Tests that use mock configs include NORMALIZATION_MAX_SCALE directly in their mock data
2. The ConfigManager merge logic already handles week-specific parameters correctly
3. The parameter extraction happens after the merge, so it works regardless of source

---

## Quality Control Rounds

### QC Round 1: Initial Quality Review
- **Reviewed:** 2025-12-13
- **Issues Found:** None
- **Status:** PASSED

Verified all requirements from spec:
| Requirement | Verified |
|-------------|----------|
| Remove from league_config.json | ✓ |
| Add to week1-5.json (163) | ✓ |
| Add to week6-9.json (153) | ✓ |
| Add to week10-13.json (143) | ✓ |
| Add to week14-17.json (133) | ✓ |
| Move to WEEK_SPECIFIC_PARAMS | ✓ |
| Not in BASE_CONFIG_PARAMS | ✓ |

---

### QC Round 2: Deep Verification Review
- **Reviewed:** 2025-12-13
- **Issues Found:** Outdated docstring examples in ConfigGenerator.py
- **Issues Fixed:** Updated `is_base_param()` and `is_week_specific_param()` examples
- **Status:** PASSED (issue fixed)

Verified data flow:
1. ConfigManager loads base config (no NORMALIZATION_MAX_SCALE)
2. ConfigManager loads week config (has NORMALIZATION_MAX_SCALE)
3. Merge happens (parameters.update)
4. Required params check passes (NORMALIZATION_MAX_SCALE present from merge)
5. Parameter extraction works correctly

---

### QC Round 3: Final Skeptical Review
- **Reviewed:** 2025-12-13
- **Issues Found:** Fallback test fixture in test_simulation_integration.py had NORMALIZATION_MAX_SCALE in base_config instead of week_params
- **Issues Fixed:** Moved parameter to week_params for consistency
- **Status:** PASSED (issue fixed)

All 2221 tests pass (100%)
