# Week-Specific Point Normalization

## Objective

Move `NORMALIZATION_MAX_SCALE` from the base `league_config.json` into week-specific configuration files, allowing each week range to have its own normalization scale value.

---

## High-Level Requirements

### 1. Configuration Changes

- **Remove from base config:** Remove `NORMALIZATION_MAX_SCALE` from `data/configs/league_config.json`
- **Add to week configs:** Add `NORMALIZATION_MAX_SCALE` to each of the 4 week-specific config files:
  - `data/configs/week1-5.json`
  - `data/configs/week6-9.json`
  - `data/configs/week10-13.json`
  - `data/configs/week14-17.json`

### 2. Code Updates (If Needed)

- **ConfigManager:** May need to update required parameter validation to allow NORMALIZATION_MAX_SCALE in week configs
- **ConfigGenerator:** May need to classify NORMALIZATION_MAX_SCALE as week-specific for simulation optimization
- **League Helper:** Should work with existing merge logic (week config overrides base)
- **Simulation:** May need updates to optimize NORMALIZATION_MAX_SCALE per week range

### 3. Output/Deliverables

```
data/configs/
├── league_config.json        # NORMALIZATION_MAX_SCALE removed
├── week1-5.json              # NORMALIZATION_MAX_SCALE added
├── week6-9.json              # NORMALIZATION_MAX_SCALE added
├── week10-13.json            # NORMALIZATION_MAX_SCALE added
└── week14-17.json            # NORMALIZATION_MAX_SCALE added
```

---

## Resolved Implementation Details

### Decision 1: Default Value Strategy
**Decision:** Remove entirely from base config
**Reasoning:** Week configs are the authoritative source. No fallback needed.

### Decision 2: Week-Specific Values
| Week Range | Value |
|------------|-------|
| Weeks 1-5 | 163 |
| Weeks 6-9 | 153 |
| Weeks 10-13 | 143 |
| Weeks 14-17 | 133 |

**Pattern:** Decreasing by 10 per week range (higher scale early season, lower late season)

### Decision 3: Simulation Optimization
**Decision:** Yes - enable per-week optimization
**Implementation:** Move `NORMALIZATION_MAX_SCALE` from `BASE_CONFIG_PARAMS` to `WEEK_SPECIFIC_PARAMS` in `ResultsManager.py`

### ConfigManager Behavior
- Keep `NORMALIZATION_MAX_SCALE` in required params list (line 950)
- The merge happens before validation: week config values are merged over base
- After merge, `NORMALIZATION_MAX_SCALE` will be present from week config
- No code changes needed to ConfigManager - existing merge logic handles it

### ConfigGenerator Behavior
- Classification will automatically update once `ResultsManager` lists change
- `is_base_param('NORMALIZATION_MAX_SCALE')` will return False
- `is_week_specific_param('NORMALIZATION_MAX_SCALE')` will return True
- Value set generation may need review for per-week handling

### Test Impact
- ~47 references across ~24 test files use `NORMALIZATION_MAX_SCALE: 100` in mock configs
- Tests using legacy single-file configs will need week config mocks added
- Integration tests may need updates for new config structure

---

## Implementation Notes

### Files to Modify

| File | Change |
|------|--------|
| `data/configs/league_config.json` | Remove `NORMALIZATION_MAX_SCALE: 163` |
| `data/configs/week1-5.json` | Add `NORMALIZATION_MAX_SCALE: 163` |
| `data/configs/week6-9.json` | Add `NORMALIZATION_MAX_SCALE: 153` |
| `data/configs/week10-13.json` | Add `NORMALIZATION_MAX_SCALE: 143` |
| `data/configs/week14-17.json` | Add `NORMALIZATION_MAX_SCALE: 133` |
| `simulation/ResultsManager.py` | Move param from BASE_CONFIG_PARAMS to WEEK_SPECIFIC_PARAMS |
| ~24 test files | Update mock configs to include NORMALIZATION_MAX_SCALE |

### Dependencies

- ConfigManager must successfully load week configs
- Existing week config merge logic should handle the change

### Reusable Code

- Week config merge logic already exists in `ConfigManager._load_week_config()` (lines 261-296)
- Week config file selection exists in `ConfigManager._get_week_config_filename()` (lines 231-259)

### Testing Strategy

- All existing unit tests must pass (100% pass rate)
- Verify ConfigManager correctly loads NORMALIZATION_MAX_SCALE from week configs
- Verify simulation can optimize week-specific NORMALIZATION_MAX_SCALE values
- Verify legacy single-file configs still work (for backward compatibility)

---

## Status: READY FOR IMPLEMENTATION
