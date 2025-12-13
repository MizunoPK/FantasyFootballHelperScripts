# Week-Specific Point Normalization - Requirements Checklist

> **IMPORTANT**: When marking items as resolved, also update `week_specific_point_normalization_specs.md`
> with full implementation details. The checklist tracks status; the specs file is
> the implementation specification.

---

## General Decisions

- [x] **Default Value Strategy:** Remove NORMALIZATION_MAX_SCALE from base config entirely, or keep as default?
  - **RESOLVED:** Remove entirely from base config. Week configs are the required source.
- [x] **Week-Specific Values:** What value should each week range have? (1-5, 6-9, 10-13, 14-17)
  - **RESOLVED:** Weeks 1-5: 163, Weeks 6-9: 153, Weeks 10-13: 143, Weeks 14-17: 133

---

## Configuration File Changes

### league_config.json

**File-level decisions:**
- [x] Remove NORMALIZATION_MAX_SCALE: **Yes**
- [x] Keep as optional fallback: **No**

### week1-5.json

**Parameters to add:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| `NORMALIZATION_MAX_SCALE` | [x] 163 | Early season |

### week6-9.json

**Parameters to add:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| `NORMALIZATION_MAX_SCALE` | [x] 153 | Mid-early season |

### week10-13.json

**Parameters to add:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| `NORMALIZATION_MAX_SCALE` | [x] 143 | Mid-late season |

### week14-17.json

**Parameters to add:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| `NORMALIZATION_MAX_SCALE` | [x] 133 | Late season / playoffs |

---

## Code Changes

### ConfigManager.py

- [x] **Required params list:** Is NORMALIZATION_MAX_SCALE in `required_params`?
  - Current: Line 950 includes `self.keys.NORMALIZATION_MAX_SCALE`
  - **Action:** Keep in required list - param will come from merged week config
  - The merge happens before validation, so it will be present

- [ ] **Validation logic:** Does `_extract_parameters()` need modification?
  - Current: Extracts at line 975
  - **Action:** No change needed - extraction happens after merge

- [ ] **Fallback handling:** What if week config is missing and base has no NORMALIZATION_MAX_SCALE?
  - **Decision:** Error is appropriate - week configs are required source

### ResultsManager.py

- [ ] **Move NORMALIZATION_MAX_SCALE:** From BASE_CONFIG_PARAMS to WEEK_SPECIFIC_PARAMS
  - Current: Line 242 in BASE_CONFIG_PARAMS
  - **Action:** Move to WEEK_SPECIFIC_PARAMS (line 255)
  - This enables per-week optimization in simulation

### ConfigGenerator.py

- [x] **Param classification:** Is NORMALIZATION_MAX_SCALE classified correctly?
  - `is_base_param()` at line 269: Currently returns True
  - `is_week_specific_param()` at line 294: Currently returns False
  - **Action:** Will automatically change once ResultsManager lists are updated (uses those constants)

- [ ] **PARAM_MAPPING:** Line 231 mapping needs update?
  - Current: `'NORMALIZATION_MAX_SCALE': 'NORMALIZATION_MAX_SCALE'`
  - **Action:** No change needed - direct mapping still correct

- [ ] **Value set generation:** Line 609-613 generates NORMALIZATION_MAX_SCALE values
  - **Action:** Review if per-week generation is automatic or needs update

---

## Testing

- [ ] **Identify affected tests:** Count tests with NORMALIZATION_MAX_SCALE in mock configs
  - Found references in: test_simulation_manager.py, test_ResultsManager.py, test_config_generator.py, test_ConfigManager_*.py, integration tests

- [ ] **Update test fixtures:** Ensure mock configs include NORMALIZATION_MAX_SCALE appropriately

- [ ] **New test cases needed:**
  - [ ] Test ConfigManager loads NORMALIZATION_MAX_SCALE from week config
  - [ ] Test ConfigManager handles missing NORMALIZATION_MAX_SCALE gracefully
  - [ ] Test simulation optimizes week-specific NORMALIZATION_MAX_SCALE

---

## Edge Cases

- [ ] **Legacy config compatibility:** Single league_config.json (no configs folder) still works?
- [ ] **Missing week config:** What if week{N}-{M}.json doesn't exist?
- [ ] **Invalid week number:** Week outside 1-17 range (handled by existing validation)

---

## Data Source Summary

| Data | Source | Status |
|------|--------|--------|
| Current NORMALIZATION_MAX_SCALE | `league_config.json` line 8 | Verified: 163 |
| Week config merge logic | `ConfigManager._load_week_config()` | Verified: Exists |
| Param classification | `ConfigGenerator.is_base_param()` | Verified: Currently base |

---

## Resolution Log

| Item | Resolution | Date |
|------|------------|------|
| Default Value Strategy | Option B: Remove entirely from base config. Week configs required. | 2025-12-13 |
| Week-Specific Values | 1-5: 163, 6-9: 153, 10-13: 143, 14-17: 133 (decreasing by 10) | 2025-12-13 |
| Simulation Optimization | Yes: Move to WEEK_SPECIFIC_PARAMS for per-week optimization | 2025-12-13 |
